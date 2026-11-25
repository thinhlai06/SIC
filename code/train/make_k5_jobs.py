"""Jobs for the continued-training check (K5): 3 more epochs starting from the 5-epoch best checkpoints.
Rule fixed before seeing any result: lower peak learning rate (blr 2e-3 for ViT-L, lr 4e-5 for ResNet-50), 0.25 warm-up epoch,
cosine decay to 1e-6, standard augmentation, new data order (seed 100). Model selection by EyePACS-validation QWK; DDR is not used."""
import json

vit = dict(epochs=3, bs=16, accum=2, blr=2e-3, warmup_epochs=0.25, aug="std", seed=100, gpu=None, final_eval=True,
           save_ckpt=True, time_limit_min=170, pretrained_path="")
jobs = [
    {**vit, "name": "m1_s0_c3", "arch": "retfound", "gpu": 0, "init_ckpt": "m1_s0_best.pt"},
    {**vit, "name": "b2_s0_c3", "arch": "vitl_mae_in", "gpu": 1, "init_ckpt": "b2_s0_best.pt"},
    dict(name="b1_s0_c3", arch="resnet50", gpu=1, seed=100, epochs=3, bs=32, accum=1, blr=None, lr=4e-5, warmup_epochs=0.25,
         aug="std", final_eval=True, save_ckpt=True, time_limit_min=60, pretrained_path="", init_ckpt="b1_s0_best.pt"),
]
json.dump(jobs, open(r"c:\SIC\code\train\jobs_k5.json", "w"), indent=1)
print(len(jobs), "jobs written")
