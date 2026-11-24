"""CPU unit test of train_lib.run(final_eval=True) with a tiny ViT and synthetic images.
Usage: python unit_final_eval.py <data_dir_with_eyepacs_train_val_and_manifest> <work_dir>
"""
import os
import shutil
import sys

import pandas as pd

data, work = sys.argv[1], sys.argv[2]
os.makedirs(work, exist_ok=True)
os.environ["SIC_DATA"], os.environ["SIC_WORK"] = data, work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import train_lib as T  # noqa: E402

man = pd.read_csv(os.path.join(data, "manifest.csv"))
for sp, src in [("eyepacs_test", "eyepacs_val"), ("ddr_test", "eyepacs_val")]:
    os.makedirs(os.path.join(data, sp), exist_ok=True)
    rows = man[man.split == src].copy()
    for n in rows.image.astype(str):
        shutil.copy(os.path.join(data, src, n + ".jpg"), os.path.join(data, sp, n + ".jpg"))
    rows["split"] = sp
    man = pd.concat([man[man.split != sp], rows])
man.to_csv(os.path.join(data, "manifest.csv"), index=False)
open(os.path.join(data, "READY_TEST"), "w").write("ok")

T.run(dict(name="unit_fe", arch="vit_tiny_test", aug="std", epochs=2, bs=4, accum=1, blr=1e-3, num_workers=0,
           final_eval=True, pretrained_path=""))
print(sorted(os.listdir(work)))
