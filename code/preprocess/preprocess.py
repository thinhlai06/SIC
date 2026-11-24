"""GD1.2 preprocessing (CPU only): crop retina -> pad to square -> 224x224 -> cache JPEG.

The SAME pipeline is applied to every image of every dataset. DDR statistics are
never used to tune any parameter (all constants are fixed a priori).

Outputs (/kaggle/working):
  cache/<split>/<name>.jpg        224x224 RGB JPEG (quality 95, no chroma subsampling)
  manifest.csv                    split,image,level,src_w,src_h,box,fallback,dhash
  preprocess_report.json          counts, fallback rate, timing
  p01_before_after_crop.png       visual check
  p02_phash_check.png/.json       EyePACS <-> DDR near-duplicate check
"""
import glob
import json
import os
import time
from concurrent.futures import ProcessPoolExecutor

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image

OUT = "/kaggle/working"
SIZE = 224
THR = 15          # pixel value (0-255) below which a pixel is "background"
MIN_FRAC = 0.01   # a row/column counts as retina if >=1% of its pixels are above THR
MARGIN = 0.02     # extra margin around the crop box (fraction of box size)
t0 = time.time()


def log(*a):
    print(f"[{time.time() - t0:7.1f}s]", *a, flush=True)


def find_dir(pattern):
    hits = [h for h in glob.glob(pattern) if os.path.isdir(h)]
    return sorted(hits)[0] if hits else None


EYE = find_dir("/kaggle/input/resized-2015-2019*") or find_dir("/kaggle/input/datasets/*/resized-2015-2019*")
DDR = find_dir("/kaggle/input/ddr-dataset*") or find_dir("/kaggle/input/datasets/*/ddr-dataset*")
log("EYE", EYE, "| DDR", DDR)
lab = glob.glob(EYE + "/**/trainLabels15.csv", recursive=True)[0]
lab_dir = os.path.dirname(lab)
tr = pd.read_csv(os.path.join(lab_dir, "trainLabels15.csv"))
te = pd.read_csv(os.path.join(lab_dir, "testLabels15.csv"))
tr_dir = glob.glob(EYE + "/resized train 15")[0]
te_dir = glob.glob(EYE + "/resized test 15")[0]
grading = glob.glob(DDR + "/**/DR_grading", recursive=True)[0]
ddr = pd.read_csv(os.path.join(grading, "test.txt"), sep=r"\s+", header=None, names=["image", "level"])
ddr = ddr[ddr.level != 5].reset_index(drop=True)  # drop ungradable

jobs = []
for _, r in tr.iterrows():
    jobs.append(("eyepacs_train", r["image"], int(r["level"]), os.path.join(tr_dir, r["image"] + ".jpg")))
for _, r in te.iterrows():
    sp = "eyepacs_val" if r["Usage"] == "Public" else "eyepacs_test"
    jobs.append((sp, r["image"], int(r["level"]), os.path.join(te_dir, r["image"] + ".jpg")))
for _, r in ddr.iterrows():
    jobs.append(("ddr_test", r["image"].replace(".jpg", ""), int(r["level"]), os.path.join(grading, "test", r["image"])))
for sp in ["eyepacs_train", "eyepacs_val", "eyepacs_test", "ddr_test"]:
    os.makedirs(f"{OUT}/cache/{sp}", exist_ok=True)
log("jobs", len(jobs), pd.Series([j[0] for j in jobs]).value_counts().to_dict())


def retina_box(im):
    """Bounding box (x0,y0,x1,y1) of the non-black region, in original pixel coordinates."""
    w, h = im.size
    s = 512.0 / max(w, h)
    small = im.resize((max(1, int(w * s)), max(1, int(h * s))))
    g = np.asarray(small).max(axis=2) > THR
    rows = np.where(g.mean(axis=1) >= MIN_FRAC)[0]
    cols = np.where(g.mean(axis=0) >= MIN_FRAC)[0]
    if len(rows) == 0 or len(cols) == 0:
        return (0, 0, w, h), True
    x0, x1 = cols.min() / s, (cols.max() + 1) / s
    y0, y1 = rows.min() / s, (rows.max() + 1) / s
    mx, my = (x1 - x0) * MARGIN, (y1 - y0) * MARGIN
    box = (max(0, int(x0 - mx)), max(0, int(y0 - my)), min(w, int(x1 + mx)), min(h, int(y1 + my)))
    return box, False


def to_square(im):
    w, h = im.size
    s = max(w, h)
    canvas = Image.new("RGB", (s, s), (0, 0, 0))
    canvas.paste(im, ((s - w) // 2, (s - h) // 2))
    return canvas


def dhash(im224):
    a = np.asarray(im224.convert("L").resize((9, 8), Image.BILINEAR), dtype=np.int16)
    bits = (a[:, 1:] > a[:, :-1]).flatten()
    v = 0
    for b in bits:
        v = (v << 1) | int(b)
    return v


def process(job):
    split, name, level, path = job
    try:
        im = Image.open(path).convert("RGB")
        w, h = im.size
        box, fb = retina_box(im)
        out = to_square(im.crop(box)).resize((SIZE, SIZE), Image.LANCZOS)
        out.save(f"{OUT}/cache/{split}/{name}.jpg", quality=95, subsampling=0)
        return (split, name, level, w, h, ",".join(map(str, box)), int(fb), f"{dhash(out):016x}", "")
    except Exception as e:  # noqa
        return (split, name, level, 0, 0, "", 1, "", repr(e))


if __name__ == "__main__":
    n_proc = os.cpu_count() or 4
    log("cpu count", n_proc)
    rows = []
    with ProcessPoolExecutor(max_workers=n_proc) as ex:
        for i, r in enumerate(ex.map(process, jobs, chunksize=64)):
            rows.append(r)
            if i % 5000 == 0:
                log("done", i, "/", len(jobs))
    man = pd.DataFrame(rows, columns=["split", "image", "level", "src_w", "src_h", "box", "fallback", "dhash", "error"])
    man.to_csv(f"{OUT}/manifest.csv", index=False)
    rep = {
        "n": len(man),
        "per_split": man.split.value_counts().to_dict(),
        "errors": int((man.error != "").sum()),
        "fallback_whole_image": man.groupby("split").fallback.sum().to_dict(),
        "seconds": time.time() - t0,
    }
    log(rep)

    # ---------------- before/after figure (fixed random seed, 6 per dataset)
    rng = np.random.RandomState(0)
    fig, axs = plt.subplots(4, 6, figsize=(18, 12))
    for r_i, (sp, label) in enumerate([("eyepacs_train", "EyePACS"), ("ddr_test", "DDR")]):
        sub = man[(man.split == sp) & (man.error == "")].sample(6, random_state=0)
        for c, (_, row) in enumerate(sub.iterrows()):
            src = [j for j in jobs if j[0] == sp and j[1] == row["image"]][0][3]
            axs[2 * r_i, c].imshow(Image.open(src).convert("RGB").resize((256, 256 * row.src_h // max(row.src_w, 1))))
            axs[2 * r_i, c].set_title(f"{label} original {row.src_w}x{row.src_h}", fontsize=8)
            axs[2 * r_i + 1, c].imshow(Image.open(f"{OUT}/cache/{sp}/{row['image']}.jpg"))
            axs[2 * r_i + 1, c].set_title("processed 224x224", fontsize=8)
    for a in axs.ravel():
        a.axis("off")
    plt.tight_layout()
    plt.savefig(f"{OUT}/p01_before_after_crop.png", dpi=110)
    plt.close()

    # ---------------- near-duplicate check: DDR-test vs all EyePACS (dHash Hamming distance)
    ok = man[man.error == ""]
    d_h = np.array([int(x, 16) for x in ok[ok.split == "ddr_test"].dhash], dtype=np.uint64)
    e_h = np.array([int(x, 16) for x in ok[ok.split != "ddr_test"].dhash], dtype=np.uint64)
    lut = np.array([bin(i).count("1") for i in range(256)], dtype=np.uint8)
    mins = np.zeros(len(d_h), dtype=np.int32)
    for i, h in enumerate(d_h):
        x = np.bitwise_xor(e_h, h).view(np.uint8).reshape(-1, 8)
        mins[i] = lut[x].sum(axis=1).min()
    dup = {"n_ddr": int(len(d_h)), "n_eyepacs": int(len(e_h)),
           "min_dist_hist": {int(k): int(v) for k, v in zip(*np.unique(np.minimum(mins, 20), return_counts=True))},
           "ddr_with_dist_le_4": int((mins <= 4).sum()), "ddr_with_dist_le_8": int((mins <= 8).sum())}
    log("phash", dup)
    json.dump(dup, open(f"{OUT}/p02_phash_check.json", "w"), indent=2)
    plt.figure(figsize=(7, 4))
    plt.hist(np.minimum(mins, 30), bins=range(0, 32), color="#193DB0")
    plt.axvline(4.5, color="r", ls="--", label="near-duplicate threshold (<=4 bits of 64)")
    plt.xlabel("min Hamming distance of dHash to any EyePACS image")
    plt.ylabel("DDR-test images")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{OUT}/p02_phash_check.png", dpi=200)
    plt.close()
    rep["phash"] = dup
    json.dump(rep, open(f"{OUT}/preprocess_report.json", "w"), indent=2, default=str)
    log("done")
