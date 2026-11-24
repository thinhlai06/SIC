"""Combined training curves (EyePACS-validation QWK, macro-F1, loss) of all runs. Usage: python curves_all.py <dir with *_log.csv> <out.png>"""
import glob
import os
import sys

import matplotlib
import matplotlib.ticker
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

src, out = sys.argv[1], sys.argv[2]
COL = {"b1": "#7F7F7F", "b2": "#E69F00", "m1": "#193DB0", "m2": "#2E9E5B"}
fig, axs = plt.subplots(1, 3, figsize=(15, 4.2))
for f in sorted(glob.glob(os.path.join(src, "*_log.csv"))):
    name = os.path.basename(f)[:-8]            # e.g. m1_s0 or m1_s0_e8
    if name.startswith("bench") or name.startswith("unit"):
        continue
    d = pd.read_csv(f)
    model = name.split("_")[0]
    long_run = name.endswith("_e8") or name.endswith("_e10")
    ls = "--" if long_run else "-"
    for ax, col, lab in zip(axs, ["val_qwk", "val_macro_f1", "val_loss"], ["QWK", "macro-F1", "cross-entropy"]):
        ax.plot(d["epoch"], d[col], ls, marker="o", ms=3, color=COL.get(model, "k"), label=name, alpha=0.9)
        ax.set_title(f"EyePACS-validation {lab}")
        ax.set_xlabel("epoch")
        ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
axs[0].legend(fontsize=7, ncol=2)
plt.tight_layout()
plt.savefig(out, dpi=170)
print("saved", out)
