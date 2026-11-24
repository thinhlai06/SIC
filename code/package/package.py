"""GD1.2b: QA + packaging of the preprocessing output (CPU only).

Reads the output of kernel `sic-dr-preprocess` (mounted as an input), verifies it,
copies the small report files, and packs the cached JPEGs into a few big tar files
so that listing/downloading the result needs only a handful of API calls.

Outputs (/kaggle/working):
  eyepacs_train.tar, eyepacs_val.tar, eyepacs_test.tar, ddr_test.tar
  manifest.csv, preprocess_report.json, p01_before_after_crop.png,
  p02_phash_check.png, p02_phash_check.json, qa_report.json
"""
import glob
import json
import os
import shutil
import tarfile
import time

import pandas as pd
from PIL import Image

OUT = "/kaggle/working"
t0 = time.time()


def log(*a):
    print(f"[{time.time() - t0:7.1f}s]", *a, flush=True)


hits = glob.glob("/kaggle/input/**/manifest.csv", recursive=True)
log("manifest candidates:", hits)
SRC = os.path.dirname(hits[0])
log("SRC", SRC, os.listdir(SRC)[:20])

small = ["manifest.csv", "preprocess_report.json", "p01_before_after_crop.png",
         "p02_phash_check.png", "p02_phash_check.json"]
for f in small:
    p = os.path.join(SRC, f)
    if os.path.exists(p):
        shutil.copy(p, OUT)
        log("copied", f)
    else:
        log("MISSING", f)

man = pd.read_csv(os.path.join(SRC, "manifest.csv"))
qa = {"manifest_rows": int(len(man)), "per_split": man.split.value_counts().to_dict(),
      "errors": int((man.error.fillna("") != "").sum()),
      "fallback_whole_image": man.groupby("split").fallback.sum().astype(int).to_dict()}

# per-split QA: file exists, size is 224x224 (checked on a sample), then tar
bad_size = {}
missing = {}
for sp in ["eyepacs_train", "eyepacs_val", "eyepacs_test", "ddr_test"]:
    d = os.path.join(SRC, "cache", sp)
    files = set(os.listdir(d))
    names = man[man.split == sp].image.astype(str).tolist()
    missing[sp] = int(sum((n + ".jpg") not in files for n in names))
    samp = sorted(files)[:: max(1, len(files) // 300)]
    bad_size[sp] = int(sum(Image.open(os.path.join(d, f)).size != (224, 224) for f in samp))
    log(sp, "files", len(files), "manifest", len(names), "missing", missing[sp], "bad_size_in_sample", bad_size[sp])
    with tarfile.open(f"{OUT}/{sp}.tar", "w") as tf:   # no compression: JPEGs are already compressed
        for f in sorted(files):
            tf.add(os.path.join(d, f), arcname=f"{sp}/{f}")
    log("tar written", sp, os.path.getsize(f"{OUT}/{sp}.tar") / 1e6, "MB")
qa["missing_files"] = missing
qa["bad_size_in_sample"] = bad_size
qa["tar_mb"] = {sp: round(os.path.getsize(f"{OUT}/{sp}.tar") / 1e6, 1)
                for sp in ["eyepacs_train", "eyepacs_val", "eyepacs_test", "ddr_test"]}
json.dump(qa, open(f"{OUT}/qa_report.json", "w"), indent=2)
log("QA", qa)
log("done")
