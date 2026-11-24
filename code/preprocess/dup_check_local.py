"""Local re-check of EyePACS <-> DDR near-duplicates (CPU, reads the packaged 224x224 tar files in memory).

Why: the Kaggle dHash check (9x8 grayscale) flagged 94% of DDR images as 'near-duplicates' (distance <= 4 of 64 bits).
That is expected for a coarse hash: all fundus photographs are a bright disc on a black background.
Here each image is turned into a vessel/lesion-sensitive descriptor (64x64 grayscale, high-pass filtered,
zero-mean, unit-norm) and compared by normalised cross-correlation (NCC) against all EyePACS images.
True duplicates (even re-compressed / re-scaled / brightness-changed) must give NCC close to 1.

Usage: python -I dup_check_local.py <dir with the 4 tar files> <out dir>
Outputs: dup_ncc_hist.png, dup_top_pairs.png, dup_check_report.json, dup_selftest in the report.
"""
import io
import json
import os
import sys
import tarfile
import time

import numpy as np
from PIL import Image, ImageFilter

SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
t0 = time.time()


def descriptor(im):
    g = im.convert("L").resize((64, 64), Image.BOX)
    a = np.asarray(g, dtype=np.float32)
    b = np.asarray(g.filter(ImageFilter.GaussianBlur(3)), dtype=np.float32)
    d = (a - b).ravel()
    d -= d.mean()
    n = np.linalg.norm(d)
    return d / n if n > 1e-6 else d


def load_tar(name):
    feats, names, thumbs = [], [], []
    with tarfile.open(os.path.join(SRC, name + ".tar")) as tf:
        for m in tf:
            if not m.isfile():
                continue
            im = Image.open(io.BytesIO(tf.extractfile(m).read())).convert("RGB")
            feats.append(descriptor(im))
            names.append(m.name)
    print(f"[{time.time() - t0:6.0f}s] {name}: {len(names)} images", flush=True)
    return np.stack(feats).astype(np.float32), names


ddr_f, ddr_n = load_tar("ddr_test")
eye_f, eye_n = [], []
for sp in ["eyepacs_train", "eyepacs_val", "eyepacs_test"]:
    f, n = load_tar(sp)
    eye_f.append(f)
    eye_n += n
eye_f = np.concatenate(eye_f)


def best_match(q, ref, chunk=500):
    best, idx = np.full(len(q), -1.0, np.float32), np.zeros(len(q), np.int64)
    for i in range(0, len(q), chunk):
        s = q[i:i + chunk] @ ref.T
        j = s.argmax(1)
        best[i:i + chunk] = s[np.arange(len(j)), j]
        idx[i:i + chunk] = j
    return best, idx


ncc, idx = best_match(ddr_f, eye_f)
print(f"[{time.time() - t0:6.0f}s] DDR->EyePACS NCC done; max {ncc.max():.3f}, p99 {np.percentile(ncc, 99):.3f}", flush=True)

# self-test: perturb 300 DDR images (re-compress, rescale, brightness) and search them among EyePACS+originals
rng = np.random.RandomState(0)
pick = rng.choice(len(ddr_n), 300, replace=False)
pert = []
with tarfile.open(os.path.join(SRC, "ddr_test.tar")) as tf:
    members = [m for m in tf if m.isfile()]
    for i in pick:
        im = Image.open(io.BytesIO(tf.extractfile(members[i]).read())).convert("RGB")
        im = im.resize((200, 200), Image.BILINEAR).resize((224, 224), Image.BILINEAR)
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=60); buf.seek(0)
        im = Image.open(buf).convert("RGB")
        im = Image.eval(im, lambda v: min(255, int(v * 1.15)))
        pert.append(descriptor(im))
pert = np.stack(pert).astype(np.float32)
st = (pert @ ddr_f.T)[np.arange(300), pick]          # NCC with its own original
st_other = np.sort(pert @ ddr_f.T, axis=1)[:, -2]    # best NCC with any OTHER DDR image
print(f"self-test: NCC(perturbed, original) min {st.min():.3f} median {np.median(st):.3f}; "
      f"best NCC with a different image median {np.median(st_other):.3f}", flush=True)

thr = 0.95
rep = dict(n_ddr=len(ddr_n), n_eyepacs=len(eye_n), ncc_max=float(ncc.max()), ncc_p99=float(np.percentile(ncc, 99)),
           ncc_median=float(np.median(ncc)), ddr_with_ncc_ge_0_95=int((ncc >= 0.95).sum()),
           ddr_with_ncc_ge_0_90=int((ncc >= 0.90).sum()), ddr_with_ncc_ge_0_80=int((ncc >= 0.80).sum()),
           selftest_perturbed_vs_original_min=float(st.min()), selftest_perturbed_vs_original_median=float(np.median(st)),
           selftest_best_other_ddr_median=float(np.median(st_other)), threshold=thr)
json.dump(rep, open(os.path.join(OUT, "dup_check_report.json"), "w"), indent=2)
print(json.dumps(rep, indent=2))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(7, 4))
ax.hist(ncc, bins=60, color="#193DB0", label="DDR vs. best EyePACS match")
ax.hist(st, bins=20, color="#E65100", alpha=0.8, label="self-test: perturbed copy vs. its original")
ax.axvline(thr, color="red", ls="--", label=f"duplicate threshold ({thr})")
ax.set_xlabel("normalised cross-correlation of vessel/lesion descriptor")
ax.set_ylabel("images")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "dup_ncc_hist.png"), dpi=200)

top = np.argsort(-ncc)[:6]
fig, axs = plt.subplots(2, 6, figsize=(15, 5.2))
with tarfile.open(os.path.join(SRC, "ddr_test.tar")) as td:
    dm = {m.name: m for m in td if m.isfile()}
    for c, i in enumerate(top):
        axs[0, c].imshow(Image.open(io.BytesIO(td.extractfile(dm[ddr_n[i]]).read())))
        axs[0, c].set_title(f"DDR  NCC={ncc[i]:.2f}", fontsize=8)
for c, i in enumerate(top):
    nm = eye_n[idx[i]]
    tarname = nm.split("/")[0] + ".tar"
    with tarfile.open(os.path.join(SRC, tarname)) as te:
        axs[1, c].imshow(Image.open(io.BytesIO(te.extractfile(nm).read())))
        axs[1, c].set_title("most similar EyePACS", fontsize=8)
for a in axs.ravel():
    a.axis("off")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "dup_top_pairs.png"), dpi=150)
print(f"[{time.time() - t0:6.0f}s] done")
