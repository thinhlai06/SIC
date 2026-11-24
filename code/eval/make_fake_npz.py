"""Synthetic logits/features to unit-test analyze.py (NOT real results). Usage: python make_fake_npz.py <out_dir>"""
import json
import os
import sys

import numpy as np

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
rs = np.random.RandomState(0)
runs = {}
YS = {}
for m, noise in [("B1", 2.2), ("B2", 1.8), ("M1", 1.4), ("M2", 1.2)]:
    runs[m] = [f"{m.lower()}_s0", f"{m.lower()}_s1"]
    for r in runs[m]:
        for sp, n, pri in [("eyepacs_test", 3000, [.74, .07, .15, .02, .02]), ("ddr_test", 1500, [.5, .05, .36, .02, .07])]:
            if sp not in YS:
                YS[sp] = rs.choice(5, n, p=pri)
            y = YS[sp]
            lg = rs.randn(n, 5) * noise
            lg[np.arange(n), y] += 2.0
            ft = (rs.randn(n, 32) + np.eye(5)[y] @ rs.randn(5, 32) * 2 + (1.5 if sp == "ddr_test" else 0)).astype(np.float16)
            np.savez_compressed(os.path.join(out, f"{r}_{sp}.npz"), logits=lg.astype(np.float32), feats=ft, y=y)
json.dump(runs, open(os.path.join(out, "runs.json"), "w"))
print("fake data written")
