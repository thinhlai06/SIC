"""K6: continued training (3 more epochs) of M2 and of B1 seeds 1, 2 — same rule as K5 (see make_k5_jobs.py)."""
import json

vit = dict(epochs=3, bs=16, accum=2, blr=2e-3, warmup_epochs=0.25, seed=100, final_eval=True, save_ckpt=True,
           time_limit_min=170, pretrained_path="")
r50 = dict(arch="resnet50", epochs=3, bs=32, accum=1, blr=None, lr=4e-5, warmup_epochs=0.25, aug="std", final_eval=True,
           save_ckpt=True, time_limit_min=60, pretrained_path="")
jobs = [
    {**vit, "name": "m2_s0_c3", "arch": "retfound", "aug": "dg", "gpu": 0, "init_ckpt": "m2_s0_best.pt"},
    {**r50, "name": "b1_s1_c3", "gpu": 1, "seed": 101, "init_ckpt": "b1_s1_best.pt"},
    {**r50, "name": "b1_s2_c3", "gpu": 1, "seed": 102, "init_ckpt": "b1_s2_best.pt"},
]
json.dump(jobs, open(r"c:\SIC\code\train\jobs_k6.json", "w"), indent=1)
print(len(jobs), "jobs written")
