"""Grad-CAM for timm Vision Transformers (CPU friendly) + shared preprocessing for the demo / analysis.

Grad-CAM (Selvaraju et al., 2017) on the output tokens of the last transformer block:
  weights_c = mean over patch tokens of d(score)/d(activation_c);  cam = ReLU(sum_c weights_c * activation_c)
The 14x14 patch map is up-sampled to the input size.
"""
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image

MEAN, STD = (0.485, 0.456, 0.406), (0.229, 0.224, 0.225)
THR, MIN_FRAC, MARGIN, SIZE = 15, 0.01, 0.02, 224      # identical to code/preprocess/preprocess.py


def retina_box(im):
    w, h = im.size
    s = 512.0 / max(w, h)
    small = im.resize((max(1, int(w * s)), max(1, int(h * s))))
    g = np.asarray(small).max(axis=2) > THR
    rows = np.where(g.mean(axis=1) >= MIN_FRAC)[0]
    cols = np.where(g.mean(axis=0) >= MIN_FRAC)[0]
    if len(rows) == 0 or len(cols) == 0:
        return (0, 0, w, h)
    x0, x1 = cols.min() / s, (cols.max() + 1) / s
    y0, y1 = rows.min() / s, (rows.max() + 1) / s
    mx, my = (x1 - x0) * MARGIN, (y1 - y0) * MARGIN
    return (max(0, int(x0 - mx)), max(0, int(y0 - my)), min(w, int(x1 + mx)), min(h, int(y1 + my)))


def preprocess(im):
    """Same pipeline as the training cache: crop retina -> pad to square -> 224x224. Returns (PIL 224, tensor 1x3x224x224)."""
    im = im.convert("RGB")
    im = im.crop(retina_box(im))
    w, h = im.size
    s = max(w, h)
    canvas = Image.new("RGB", (s, s), (0, 0, 0))
    canvas.paste(im, ((s - w) // 2, (s - h) // 2))
    im224 = canvas.resize((SIZE, SIZE), Image.LANCZOS)
    a = (np.asarray(im224, dtype=np.float32) / 255.0 - np.array(MEAN, dtype=np.float32)) / np.array(STD, dtype=np.float32)
    return im224, torch.from_numpy(a.transpose(2, 0, 1)).unsqueeze(0)


def load_vit(ckpt_path, arch="vit_large_patch16_224"):
    import timm
    m = timm.create_model(arch, pretrained=False, num_classes=5, global_pool="avg", img_size=224)
    sd = torch.load(ckpt_path, map_location="cpu")
    m.load_state_dict({k: (v.float() if v.is_floating_point() else v) for k, v in sd.items()})
    return m.eval()


def gradcam_vit(model, x, target=None):
    """x: 1x3x224x224. Returns (probs[5], target_class, cam[224,224] in 0..1)."""
    store = {}
    blk = model.blocks[-1]

    def fwd(_, __, out):
        store["a"] = out
        out.register_hook(lambda g: store.__setitem__("g", g))

    h = blk.register_forward_hook(fwd)
    model.zero_grad()
    x = x.clone().requires_grad_(True)
    logits = model(x)
    probs = torch.softmax(logits, 1)[0].detach().numpy()
    t = int(logits.argmax(1)) if target is None else int(target)
    logits[0, t].backward()
    h.remove()
    a, g = store["a"][0, 1:], store["g"][0, 1:]            # drop CLS token -> 196 x C
    w = g.mean(0)
    cam = torch.relu((a * w).sum(1)).detach().reshape(14, 14)[None, None]
    cam = F.interpolate(cam, size=(SIZE, SIZE), mode="bilinear", align_corners=False)[0, 0].numpy()
    cam = (cam - cam.min()) / (cam.max() - cam.min() + 1e-8)
    return probs, t, cam


def overlay(im224, cam, alpha=0.45):
    import matplotlib.cm as cm
    heat = (cm.jet(cam)[..., :3] * 255).astype(np.uint8)
    out = (np.asarray(im224).astype(np.float32) * (1 - alpha) + heat.astype(np.float32) * alpha).clip(0, 255).astype(np.uint8)
    return Image.fromarray(out)


if __name__ == "__main__":      # smoke test with a tiny random ViT
    import timm
    m = timm.create_model("vit_tiny_patch16_224", pretrained=False, num_classes=5, global_pool="avg").eval()
    im, x = preprocess(Image.fromarray((np.random.rand(300, 400, 3) * 255).astype(np.uint8)))
    p, t, cam = gradcam_vit(m, x)
    print("probs", p.round(3), "target", t, "cam", cam.shape, cam.min(), cam.max())
