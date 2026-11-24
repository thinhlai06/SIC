"""Does ordinal decoding (expected grade + thresholds fitted on EyePACS-VAL only) raise QWK compared with argmax?
Usage: python decode_check.py <npz-dir> <run> <val_logits.npy> <manifest.csv>
Val labels come from the manifest (eyepacs_val rows, in the same order as the training script loaded them)."""
import sys

import numpy as np
import pandas as pd

npz, run, vl, man = sys.argv[1:5]
K = 5


def qwk(y, p):
    O = np.bincount(y * K + p, minlength=K * K).reshape(K, K).astype(float)
    E = np.outer(O.sum(1), O.sum(0)) / O.sum()
    W = (np.arange(K)[:, None] - np.arange(K)[None, :]) ** 2 / (K - 1) ** 2
    return 1 - (W * O).sum() / (W * E).sum()


def sm(l):
    e = np.exp(l - l.max(1, keepdims=True))
    return e / e.sum(1, keepdims=True)


def fit_thresholds(score, y, init=(0.5, 1.5, 2.5, 3.5)):
    t = np.array(init, float)
    best = qwk(y, np.digitize(score, t))
    for _ in range(3):
        for i in range(4):
            for c in np.linspace(t[i] - 0.6, t[i] + 0.6, 49):
                tt = t.copy(); tt[i] = c
                if np.all(np.diff(tt) > 0):
                    q = qwk(y, np.digitize(score, tt))
                    if q > best:
                        best, t = q, tt
    return t, best


m = pd.read_csv(man)
yv_all = m[(m.split == "eyepacs_val") & (m.error.fillna("") == "")].level.astype(int).values
lg = np.load(vl)
n = len(lg)
yv = yv_all[:n]                       # full validation set when val_max == 0
assert n == len(yv_all), "val logits are a subset; labels order not recoverable"
ev = (sm(lg) * np.arange(K)).sum(1)
t, q_fit = fit_thresholds(ev, yv)
print(f"{run}: VAL argmax QWK {qwk(yv, lg.argmax(1)):.4f} | VAL expected-grade+fitted thresholds {q_fit:.4f} (thresholds {np.round(t, 2)})")
for sp in ["eyepacs_test", "ddr_test"]:
    z = np.load(f"{npz}/{run}_{sp}.npz")
    y, l2 = z["y"], z["logits"]
    e2 = (sm(l2) * np.arange(K)).sum(1)
    print(f"   {sp}: argmax {qwk(y, l2.argmax(1)):.4f} | expected-grade (val-fitted thresholds) {qwk(y, np.digitize(e2, t)):.4f}")
