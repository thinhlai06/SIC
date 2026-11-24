"""Build jobs_main.json for the real runs.  Usage: python make_main_jobs.py --vit-epochs 4 --r50-epochs 6 --plan "gpu0:M1:0,M2:0;gpu1:B2:0,B1:0,B1:1,B1:2"
Entries are MODEL:SEED. Models: M1 (RETFound), M2 (RETFound + domain-shift aug), B2 (ViT-L MAE ImageNet), B1 (ResNet-50)."""
import argparse
import json

ap = argparse.ArgumentParser()
ap.add_argument("--vit-epochs", type=int, required=True)
ap.add_argument("--r50-epochs", type=int, required=True)
ap.add_argument("--plan", required=True)
ap.add_argument("--bs", type=int, default=16)
ap.add_argument("--accum", type=int, default=2)
ap.add_argument("--time-limit-min", type=int, default=0)
ap.add_argument("--tag", default="", help="suffix for run names, e.g. _e8")
ap.add_argument("--out", default="jobs_main.json")
a = ap.parse_args()
jobs = []
for lane in a.plan.split(";"):
    g, items = lane.split(":", 1)
    gpu = int(g.replace("gpu", ""))
    for it in items.split(","):
        m, seed = it.split(":")
        seed = int(seed)
        base = dict(name=f"{m.lower()}_s{seed}{a.tag}", seed=seed, gpu=gpu, final_eval=True, save_ckpt=True,
                    time_limit_min=a.time_limit_min)
        if m in ("M1", "M2"):
            base.update(arch="retfound", pretrained_path="RETFound_mae_natureCFP.pth", epochs=a.vit_epochs,
                        bs=a.bs, accum=a.accum, aug="dg" if m == "M2" else "std")
        elif m == "B2":
            base.update(arch="vitl_mae_in", pretrained_path="mae_pretrain_vit_large.pth", epochs=a.vit_epochs,
                        bs=a.bs, accum=a.accum, aug="std")
        elif m == "B1":
            base.update(arch="resnet50", pretrained_path="resnet50_tv_in1k.safetensors", epochs=a.r50_epochs,
                        bs=32, accum=1, blr=None, lr=1e-4, aug="std")
        else:
            raise ValueError(m)
        jobs.append(base)
json.dump(jobs, open(a.out, "w"), indent=1)
print(len(jobs), "jobs ->", a.out)
