"""Grad-CAM examples on DDR-test (CPU): correct and wrong predictions of M1 (and the same images for B2).

Usage:
  python gradcam_examples.py --npz-dir DIR --ddr-tar logs/_pkg/ddr_test.tar --manifest logs/manifest.csv \
      --ckpt M1=path/m1_s0_best.pt [--ckpt B2=path/b2_s0_best.pt] --runs M1=m1_s0,B2=b2_s0 --out evidence_figures/05_analysis
The images are the 224x224 cached files; the npz files hold the saved logits in manifest order (ddr_test rows).
"""
import argparse
import io
import os
import sys
import tarfile

import numpy as np
import pandas as pd
import torch
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "demo"))
from gradcam import MEAN, STD, gradcam_vit, load_vit, overlay  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--npz-dir", required=True)
ap.add_argument("--ddr-tar", required=True)
ap.add_argument("--manifest", required=True)
ap.add_argument("--ckpt", action="append", required=True, help="NAME=path (first one is the main model)")
ap.add_argument("--runs", required=True, help="NAME=run,... mapping model -> run name of the npz files")
ap.add_argument("--out", required=True)
ap.add_argument("--n", type=int, default=3, help="correct and wrong examples each")
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
torch.set_num_threads(max(1, (os.cpu_count() or 4) - 1))
ck = dict(x.split("=", 1) for x in a.ckpt)
runs = dict(x.split("=", 1) for x in a.runs.split(","))
main = list(ck)[0]

man = pd.read_csv(a.manifest)
names = man[man.split == "ddr_test"].image.astype(str).tolist()
z = np.load(os.path.join(a.npz_dir, f"{runs[main]}_ddr_test.npz"))
y, pred = z["y"], z["logits"].argmax(1)
assert len(names) == len(y)
rs = np.random.RandomState(0)
correct = [i for g in (2, 3, 4) for i in rs.permutation(np.where((y == g) & (pred == g))[0])[:1]][: a.n]
wrong_pool = np.where(np.abs(pred - y) >= 2)[0]
wrong = list(rs.permutation(wrong_pool)[: a.n])
sel = [(i, "correct") for i in correct] + [(i, "wrong") for i in wrong]

tf = tarfile.open(a.ddr_tar)
members = {m.name: m for m in tf if m.isfile()}


def load_img(i):
    return Image.open(io.BytesIO(tf.extractfile(members[f"ddr_test/{names[i]}.jpg"]).read())).convert("RGB")


models = {k: load_vit(p) for k, p in ck.items()}
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rows = 1 + len(models)
fig, axs = plt.subplots(rows, len(sel), figsize=(2.6 * len(sel), 2.7 * rows))
mean, std = np.array(MEAN, dtype=np.float32), np.array(STD, dtype=np.float32)
for c, (i, kind) in enumerate(sel):
    im = load_img(i)
    x = torch.from_numpy(((np.asarray(im, dtype=np.float32) / 255.0 - mean) / std).transpose(2, 0, 1)).unsqueeze(0)
    axs[0, c].imshow(im)
    axs[0, c].set_title(f"{kind}: ref {y[i]}", fontsize=9)
    for r, (k, m) in enumerate(models.items(), start=1):
        probs, t, cam = gradcam_vit(m, x)
        axs[r, c].imshow(overlay(im, cam))
        axs[r, c].set_title(f"{k} pred {t}", fontsize=9)
    print("done", c, kind, names[i], flush=True)
for ax in axs.ravel():
    ax.axis("off")
plt.tight_layout()
plt.savefig(os.path.join(a.out, "a01_gradcam_ddr_examples.png"), dpi=160)
print("saved", a.out)
