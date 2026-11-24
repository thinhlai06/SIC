"""GD1.1 probe: inspect EyePACS (resized) and DDR on Kaggle using CPU only.

Outputs go to /kaggle/working:
  probe_report.json / probe_report.md   summary numbers
  d01_class_dist_eyepacs.png, d02_class_dist_ddr.png
  d03_samples_per_grade.png, d04_color_stats_domain_gap.png, d05_image_sizes.png
This script only READS data and never uses DDR for any model decision.
"""
import glob
import json
import os
import random
import time
from collections import Counter

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image

OUT = "/kaggle/working"
random.seed(0)
np.random.seed(0)
t0 = time.time()
report = {}


def log(*a):
    print(f"[{time.time() - t0:7.1f}s]", *a, flush=True)


# ---------------------------------------------------------------- locate data
def find_dir(pattern):
    hits = [h for h in glob.glob(pattern, recursive=True) if os.path.isdir(h)]
    return sorted(hits)[0] if hits else None


log("top of /kaggle/input:", os.listdir("/kaggle/input"))
for _d in glob.glob("/kaggle/input/*") + glob.glob("/kaggle/input/*/*"):
    log("  mounted:", _d)
# Kaggle mounts datasets either at /kaggle/input/<slug> or /kaggle/input/datasets/<owner>/<slug>
EYE_ROOT = find_dir("/kaggle/input/resized-2015-2019*") or find_dir("/kaggle/input/datasets/*/resized-2015-2019*")
DDR_ROOT = find_dir("/kaggle/input/ddr-dataset*") or find_dir("/kaggle/input/datasets/*/ddr-dataset*")
log("EYE_ROOT", EYE_ROOT, "| DDR_ROOT", DDR_ROOT)
if EYE_ROOT:
    log("EYE_ROOT entries:", os.listdir(EYE_ROOT))
if DDR_ROOT:
    log("DDR_ROOT entries:", os.listdir(DDR_ROOT))

# ------------------------------------------------------------------- EyePACS
lab_dir = find_dir(EYE_ROOT + "/**/labels") or EYE_ROOT
tr = pd.read_csv(os.path.join(lab_dir, "trainLabels15.csv"))
te = pd.read_csv(os.path.join(lab_dir, "testLabels15.csv"))
tr_dir = find_dir(EYE_ROOT + "/**/resized train 15")
te_dir = find_dir(EYE_ROOT + "/**/resized test 15")
log("train dir", tr_dir, "| test dir", te_dir)

tr_files = set(os.listdir(tr_dir))
te_files = set(os.listdir(te_dir))
ext = os.path.splitext(next(iter(tr_files)))[1]
report["eyepacs"] = {
    "n_train_labels": len(tr),
    "n_test_labels": len(te),
    "n_train_files": len(tr_files),
    "n_test_files": len(te_files),
    "image_ext": ext,
    "train_missing_files": int(sum((i + ext) not in tr_files for i in tr["image"])),
    "test_missing_files": int(sum((i + ext) not in te_files for i in te["image"])),
    "val_public": int((te["Usage"] == "Public").sum()),
    "test_private": int((te["Usage"] == "Private").sum()),
    "class_counts_train": tr["level"].value_counts().sort_index().to_dict(),
    "class_counts_val": te[te.Usage == "Public"]["level"].value_counts().sort_index().to_dict(),
    "class_counts_test": te[te.Usage == "Private"]["level"].value_counts().sort_index().to_dict(),
}
log("EyePACS summary", report["eyepacs"])

# ----------------------------------------------------------------------- DDR
grading = find_dir(DDR_ROOT + "/**/DR_grading")
ddr = pd.read_csv(os.path.join(grading, "test.txt"), sep=r"\s+", header=None, names=["image", "level"])
ddr_files = set(os.listdir(os.path.join(grading, "test")))
ddr_ok = ddr[ddr.level != 5].reset_index(drop=True)
report["ddr"] = {
    "n_test_listed": len(ddr),
    "n_test_files": len(ddr_files),
    "missing_files": int(sum(i not in ddr_files for i in ddr["image"])),
    "class_counts_all": ddr["level"].value_counts().sort_index().to_dict(),
    "n_after_dropping_ungradable": len(ddr_ok),
    "class_counts_used": ddr_ok["level"].value_counts().sort_index().to_dict(),
}
log("DDR summary", report["ddr"])


# ------------------------------------------------------------ image statistics
def img_stats(path):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    small = np.asarray(im.resize((128, 128)), dtype=np.float32)
    mx = small.max(axis=2)
    ret = mx > 20  # retina mask (non-black)
    frac = float(ret.mean())
    ys, xs = np.where(ret)
    bbox = (float(xs.max() - xs.min() + 1) / 128, float(ys.max() - ys.min() + 1) / 128) if len(xs) else (0, 0)
    m = small[ret].mean(axis=0) if ret.any() else np.zeros(3)
    return {"w": w, "h": h, "retina_frac": frac, "bbox_w": bbox[0], "bbox_h": bbox[1],
            "r": m[0], "g": m[1], "b": m[2]}


def sample_stats(df, folder, ext_, n):
    rows = []
    for _, r in df.sample(n=min(n, len(df)), random_state=0).iterrows():
        p = os.path.join(folder, r["image"] + ext_)
        try:
            s = img_stats(p)
            s["level"] = int(r["level"])
            s["image"] = r["image"]
            rows.append(s)
        except Exception as e:  # noqa
            log("fail", p, e)
    return pd.DataFrame(rows)


N = 400
log("sampling image stats ...")
st_e = sample_stats(tr, tr_dir, ext, N)
st_d = sample_stats(ddr_ok.assign(image=ddr_ok["image"].str.replace(".jpg", "", regex=False)), os.path.join(grading, "test"), ".jpg", N)
for name, st in [("eyepacs_train_sample", st_e), ("ddr_test_sample", st_d)]:
    report[name] = {
        "n": len(st),
        "width_min_med_max": [int(st.w.min()), int(st.w.median()), int(st.w.max())],
        "height_min_med_max": [int(st.h.min()), int(st.h.median()), int(st.h.max())],
        "retina_frac_mean": float(st.retina_frac.mean()),
        "mean_rgb": [float(st.r.mean()), float(st.g.mean()), float(st.b.mean())],
    }
    log(name, report[name])
st_e.to_csv(f"{OUT}/stats_eyepacs_sample.csv", index=False)
st_d.to_csv(f"{OUT}/stats_ddr_sample.csv", index=False)

# --------------------------------------------------------------------- figures
GR = ["0 None", "1 Mild", "2 Moderate", "3 Severe", "4 PDR"]


def bar(ax, counts, title):
    vals = [counts.get(i, 0) for i in range(5)]
    ax.bar(GR, vals, color="#193DB0")
    for i, v in enumerate(vals):
        ax.text(i, v, f"{v}\n({v / sum(vals):.1%})", ha="center", va="bottom", fontsize=8)
    ax.set_title(title)
    ax.set_ylabel("images")
    ax.tick_params(axis="x", rotation=20)


fig, axs = plt.subplots(1, 3, figsize=(15, 4))
for ax, k, t in zip(axs, ["class_counts_train", "class_counts_val", "class_counts_test"],
                    ["EyePACS train (35,126)", "EyePACS val = Public (10,906)", "EyePACS test = Private (42,670)"]):
    bar(ax, report["eyepacs"][k], t)
plt.tight_layout()
plt.savefig(f"{OUT}/d01_class_dist_eyepacs.png", dpi=200)
plt.close()

fig, ax = plt.subplots(figsize=(6, 4))
bar(ax, report["ddr"]["class_counts_used"], f"DDR test, ungradable removed ({len(ddr_ok)})")
plt.tight_layout()
plt.savefig(f"{OUT}/d02_class_dist_ddr.png", dpi=200)
plt.close()

# sample grid: 5 grades x 2 datasets x 3 images
fig, axs = plt.subplots(6, 5, figsize=(15, 17))
for g in range(5):
    for j in range(3):
        e = st_e[st_e.level == g]
        d = st_d[st_d.level == g]
        if len(e) > j:
            axs[j, g].imshow(Image.open(os.path.join(tr_dir, e.iloc[j]["image"] + ext)).convert("RGB").resize((256, 256)))
        if len(d) > j:
            axs[3 + j, g].imshow(Image.open(os.path.join(grading, "test", d.iloc[j]["image"] + ".jpg")).convert("RGB").resize((256, 256)))
        if j == 0:
            axs[0, g].set_title(GR[g])
for a in axs.ravel():
    a.axis("off")
axs[0, 0].text(-0.05, 0.5, "EyePACS", transform=axs[0, 0].transAxes, rotation=90, ha="right", va="center", fontsize=14)
axs[3, 0].text(-0.05, 0.5, "DDR", transform=axs[3, 0].transAxes, rotation=90, ha="right", va="center", fontsize=14)
plt.tight_layout()
plt.savefig(f"{OUT}/d03_samples_per_grade.png", dpi=120)
plt.close()

# colour / brightness gap
fig, axs = plt.subplots(1, 3, figsize=(15, 4))
for ch, c, ax in zip(["r", "g", "b"], ["tab:red", "tab:green", "tab:blue"], axs):
    ax.hist(st_e[ch], bins=30, alpha=0.55, color=c, label="EyePACS", density=True)
    ax.hist(st_d[ch], bins=30, alpha=0.55, color="k", label="DDR", density=True)
    ax.set_title(f"Mean {ch.upper()} inside retina mask")
    ax.legend()
plt.tight_layout()
plt.savefig(f"{OUT}/d04_color_stats_domain_gap.png", dpi=200)
plt.close()

fig, ax = plt.subplots(figsize=(6, 5))
ax.scatter(st_e.w, st_e.h, s=8, alpha=0.5, label="EyePACS (resized)")
ax.scatter(st_d.w, st_d.h, s=8, alpha=0.5, label="DDR")
ax.set_xlabel("width px")
ax.set_ylabel("height px")
ax.legend()
ax.set_title("Image sizes")
plt.tight_layout()
plt.savefig(f"{OUT}/d05_image_sizes.png", dpi=200)
plt.close()

# ---------------------------------------------------------------------- report
with open(f"{OUT}/probe_report.json", "w") as f:
    json.dump(report, f, indent=2, default=str)
md = ["# Probe report\n", "```json", json.dumps(report, indent=2, default=str), "```\n"]
open(f"{OUT}/probe_report.md", "w").write("\n".join(md))
log("done")
