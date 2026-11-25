"""Validation curves of the 5-epoch runs and of the interrupted 8-epoch runs (M1, B2).
The 8-epoch runs were cancelled by the platform before the end of the schedule, so they have validation curves only.
Epoch records are parsed from the *.out logs (JSON after 'EPOCH').
Usage: python budget_curves.py <logs dir with 5-epoch *_log.csv> <k3 dir with *_e8.out> <out.png> <out_epochs.json>"""
import json
import os
import re
import sys

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker

logs, k3, out, out_json = sys.argv[1:5]
COL = {"B2": "#E69F00", "M1": "#193DB0"}


def parse(path):
    rows = []
    for line in open(path, encoding="utf-8", errors="ignore"):
        m = re.search(r"EPOCH (\{.*\})", line)
        if m:
            rows.append(json.loads(m.group(1)))
    return pd.DataFrame(rows)


runs = {}
for name, e5, e8 in [("B2", "b2_s0", "b2_s0_e8"), ("M1", "m1_s0", "m1_s0_e8")]:
    runs[name] = (pd.read_csv(os.path.join(logs, e5 + "_log.csv")), parse(os.path.join(k3, e8 + ".out")))
fig, axs = plt.subplots(1, 2, figsize=(10, 4))
for ax, col, lab in zip(axs, ["val_qwk", "val_macro_f1"], ["QWK", "macro-F1"]):
    for name, (d5, d8) in runs.items():
        ax.plot(d5["epoch"], d5[col], "-o", ms=3, color=COL[name], label=f"{name} 5 epochs (finished)")
        ax.plot(d8["epoch"], d8[col], "--s", ms=3, color=COL[name], alpha=0.8, label=f"{name} 8 epochs (interrupted)")
    ax.set_title(f"EyePACS-validation {lab}")
    ax.set_xlabel("epoch")
    ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
axs[0].legend(fontsize=7)
plt.tight_layout()
plt.savefig(out, dpi=170)
res = {n: {"epochs_5": d5.val_qwk.round(4).tolist(), "epochs_8_partial": d8.val_qwk.round(4).tolist(),
           "macro_f1_5": d5.val_macro_f1.round(4).tolist(), "macro_f1_8_partial": d8.val_macro_f1.round(4).tolist()}
       for n, (d5, d8) in runs.items()}
json.dump(res, open(out_json, "w"), indent=1)
print(json.dumps(res, indent=1))
