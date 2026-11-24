"""Metrics, bootstrap CIs, figures and LaTeX tables from the saved test-set logits (CPU, local).

Input : <npz_dir>/<run>_<split>.npz  with logits [N,5], feats [N,D] (fp16), y [N]   (split in eyepacs_test, ddr_test)
        runs.json  {"B1": ["b1_s0", ...], "B2": [...], "M1": [...], "M2": [...]}   (first run of each model = seed 0)
Output: <out>/results.json, <out>/results_tables.tex, figures e01..e05, a03/a04 (t-SNE)

The test sets are never used to choose anything: this script only summarises frozen-checkpoint predictions.
Usage: python analyze.py --npz-dir DIR --runs runs.json --out OUT [--boot 1000] [--tsne 1500]
"""
import argparse
import json
import os

import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--npz-dir", required=True)
ap.add_argument("--runs", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--boot", type=int, default=1000)
ap.add_argument("--tsne", type=int, default=1500)
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
RUNS = json.load(open(a.runs))
MODELS = [m for m in ["B1", "B2", "M1", "M2"] if m in RUNS]
SPLITS = ["eyepacs_test", "ddr_test"]
SPN = {"eyepacs_test": "EyePACS-test (in-domain)", "ddr_test": "DDR-test (out-of-domain)"}
COL = {"B1": "#7F7F7F", "B2": "#E69F00", "M1": "#193DB0", "M2": "#2E9E5B"}
K = 5


def load(run, sp):
    z = np.load(os.path.join(a.npz_dir, f"{run}_{sp}.npz"))
    return z["logits"].astype(np.float64), z["y"].astype(int), z["feats"]


def softmax(l):
    e = np.exp(l - l.max(1, keepdims=True))
    return e / e.sum(1, keepdims=True)


def qwk(y, p):
    O = np.bincount(y * K + p, minlength=K * K).reshape(K, K).astype(float)
    E = np.outer(O.sum(1), O.sum(0)) / O.sum()
    W = (np.arange(K)[:, None] - np.arange(K)[None, :]) ** 2 / (K - 1) ** 2
    den = (W * E).sum()
    return 1.0 - (W * O).sum() / den if den > 0 else 0.0


def macro_f1(y, p):
    f = []
    for c in range(K):
        tp = np.sum((y == c) & (p == c)); fp = np.sum((y != c) & (p == c)); fn = np.sum((y == c) & (p != c))
        f.append(0.0 if tp == 0 else 2 * tp / (2 * tp + fp + fn))
    return float(np.mean(f))


def recalls(y, p):
    return [float(np.mean(p[y == c] == c)) if np.any(y == c) else float("nan") for c in range(K)]


def auc_binary(t, s):
    """Rank-based AUC (Mann-Whitney), handles ties."""
    from scipy.stats import rankdata
    n1 = t.sum(); n0 = len(t) - n1
    if n1 == 0 or n0 == 0:
        return float("nan")
    r = rankdata(s)
    return float((r[t == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def all_metrics(y, logit):
    pr = softmax(logit); p = pr.argmax(1)
    ref = (y >= 2).astype(int); s = pr[:, 2:].sum(1)
    return dict(qwk=qwk(y, p), macro_f1=macro_f1(y, p), acc=float(np.mean(p == y)), auc_ref=auc_binary(ref, s),
                recall=recalls(y, p))


# ---------------------------------------------------------------- point estimates (all seeds)
res = {m: {sp: [] for sp in SPLITS} for m in MODELS}
data = {}
for m in MODELS:
    for r in RUNS[m]:
        for sp in SPLITS:
            lg, y, ft = load(r, sp)
            res[m][sp].append(all_metrics(y, lg))
            data[(m, r, sp)] = (lg, y, ft)
            y0 = data[(MODELS[0], RUNS[MODELS[0]][0], sp)][1]
            assert len(y) == len(y0) and (y == y0).all(), f"label order differs for {r}/{sp}"
out = {"models": {}, "n": {}}
for sp in SPLITS:
    out["n"][sp] = int(len(data[(MODELS[0], RUNS[MODELS[0]][0], sp)][1]))
for m in MODELS:
    out["models"][m] = {}
    for sp in SPLITS:
        L = res[m][sp]
        d = {}
        for k in ["qwk", "macro_f1", "acc", "auc_ref"]:
            v = np.array([x[k] for x in L]); d[k] = dict(mean=float(v.mean()), std=float(v.std(ddof=0)), per_seed=v.tolist())
        rc = np.array([x["recall"] for x in L]); d["recall_mean"] = np.nanmean(rc, 0).tolist()
        out["models"][m][sp] = d
    q_in = [x["qwk"] for x in res[m]["eyepacs_test"]]; q_out = [x["qwk"] for x in res[m]["ddr_test"]]
    dq = np.array(q_in) - np.array(q_out)
    out["models"][m]["delta_qwk"] = dict(mean=float(dq.mean()), std=float(dq.std(ddof=0)), per_seed=dq.tolist())

# ---------------------------------------------------------------- bootstrap (seed-0 runs, shared resamples => paired)
rng = np.random.RandomState(12345)
base = {sp: {m: data[(m, RUNS[m][0], sp)] for m in MODELS} for sp in SPLITS}
boot = {sp: {m: {k: [] for k in ["qwk", "macro_f1", "acc", "auc_ref"]} for m in MODELS} for sp in SPLITS}
for sp in SPLITS:
    y = base[sp][MODELS[0]][1]
    N = len(y)
    P = {m: softmax(base[sp][m][0]) for m in MODELS}
    for b in range(a.boot):
        idx = rng.randint(0, N, N)
        for m in MODELS:
            pr = P[m][idx]; yy = y[idx]; pp = pr.argmax(1)
            boot[sp][m]["qwk"].append(qwk(yy, pp)); boot[sp][m]["macro_f1"].append(macro_f1(yy, pp))
            boot[sp][m]["acc"].append(float(np.mean(pp == yy)))
            boot[sp][m]["auc_ref"].append(auc_binary((yy >= 2).astype(int), pr[:, 2:].sum(1)))
    print("bootstrap done", sp, flush=True)
for m in MODELS:
    for sp in SPLITS:
        for k in ["qwk", "macro_f1", "acc", "auc_ref"]:
            v = np.array(boot[sp][m][k])
            out["models"][m][sp][k]["ci95_seed0"] = [float(np.nanpercentile(v, 2.5)), float(np.nanpercentile(v, 97.5))]
    d = np.array(boot["eyepacs_test"][m]["qwk"]) - np.array(boot["ddr_test"][m]["qwk"])
    out["models"][m]["delta_qwk"]["ci95_seed0"] = [float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))]
pairs = [(x, y_) for x, y_ in [("M1", "B2"), ("M1", "B1"), ("M2", "M1"), ("M2", "B2")] if x in MODELS and y_ in MODELS]
out["paired_diff_qwk_ddr"] = {}
for x, y_ in pairs:
    d = np.array(boot["ddr_test"][x]["qwk"]) - np.array(boot["ddr_test"][y_]["qwk"])
    out["paired_diff_qwk_ddr"][f"{x}-{y_}"] = dict(mean=float(d.mean()), ci95=[float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))],
                                                     p_le_0=float(np.mean(d <= 0)))
out["paired_diff_delta_qwk"] = {}
for x, y_ in pairs:
    dx = np.array(boot["eyepacs_test"][x]["qwk"]) - np.array(boot["ddr_test"][x]["qwk"])
    dy = np.array(boot["eyepacs_test"][y_]["qwk"]) - np.array(boot["ddr_test"][y_]["qwk"])
    d = dx - dy
    out["paired_diff_delta_qwk"][f"{x}-{y_}"] = dict(mean=float(d.mean()), ci95=[float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))])
json.dump(out, open(os.path.join(a.out, "results.json"), "w"), indent=2)

# ---------------------------------------------------------------- figures
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
GR = ["0", "1", "2", "3", "4"]

# e01 confusion matrices (row-normalised), seed 0
fig, axs = plt.subplots(len(SPLITS), len(MODELS), figsize=(3.4 * len(MODELS), 6.6))
for i, sp in enumerate(SPLITS):
    for j, m in enumerate(MODELS):
        lg, y, _ = base[sp][m]
        p = lg.argmax(1)
        C = np.bincount(y * K + p, minlength=K * K).reshape(K, K).astype(float)
        Cn = C / np.maximum(C.sum(1, keepdims=True), 1)
        ax = axs[i, j]
        ax.imshow(Cn, cmap="Blues", vmin=0, vmax=1)
        for r in range(K):
            for c in range(K):
                ax.text(c, r, f"{Cn[r, c]:.2f}", ha="center", va="center", fontsize=8, color="white" if Cn[r, c] > 0.5 else "black")
        ax.set_xticks(range(K)); ax.set_yticks(range(K)); ax.set_xticklabels(GR); ax.set_yticklabels(GR)
        ax.set_title(f"{m} – {'EyePACS' if i == 0 else 'DDR'}", fontsize=10)
        if j == 0:
            ax.set_ylabel("reference grade")
        if i == len(SPLITS) - 1:
            ax.set_xlabel("predicted grade")
plt.tight_layout(); plt.savefig(os.path.join(a.out, "e01_confusion_all.png"), dpi=170); plt.close()

# e02 ROC referable
fig, axs = plt.subplots(1, 2, figsize=(10, 4.4))
for ax, sp in zip(axs, SPLITS):
    for m in MODELS:
        lg, y, _ = base[sp][m]
        s = softmax(lg)[:, 2:].sum(1); t = (y >= 2).astype(int)
        o = np.argsort(-s); tt = t[o]
        tpr = np.concatenate([[0], np.cumsum(tt) / tt.sum()]); fpr = np.concatenate([[0], np.cumsum(1 - tt) / (1 - tt).sum()])
        ax.plot(fpr, tpr, color=COL[m], label=f"{m} (AUC {auc_binary(t, s):.3f})")
    ax.plot([0, 1], [0, 1], "k:", lw=1)
    ax.set_title(SPN[sp]); ax.set_xlabel("1 − specificity"); ax.set_ylabel("sensitivity"); ax.legend(loc="lower right", fontsize=8)
plt.tight_layout(); plt.savefig(os.path.join(a.out, "e02_roc_referable.png"), dpi=170); plt.close()

# e03 per-grade recall on DDR (seed mean)
fig, ax = plt.subplots(figsize=(8, 4))
w = 0.8 / len(MODELS)
for j, m in enumerate(MODELS):
    ax.bar(np.arange(K) + j * w - 0.4 + w / 2, out["models"][m]["ddr_test"]["recall_mean"], w, color=COL[m], label=m)
ax.set_xticks(range(K)); ax.set_xticklabels([f"grade {g}" for g in GR]); ax.set_ylabel("recall"); ax.set_ylim(0, 1.05)
ax.set_title("Per-grade recall on DDR-test"); ax.legend(ncol=len(MODELS), fontsize=8)
plt.tight_layout(); plt.savefig(os.path.join(a.out, "e03_perclass_recall_ddr.png"), dpi=170); plt.close()

# e04 in vs out QWK with CI (seed-0 bootstrap) and seed mean markers
fig, ax = plt.subplots(figsize=(8, 4.2))
w = 0.38
for j, sp in enumerate(SPLITS):
    xs = np.arange(len(MODELS)) + (j - 0.5) * w
    mean = [out["models"][m][sp]["qwk"]["per_seed"][0] for m in MODELS]      # seed 0, same run as the CI
    smean = [out["models"][m][sp]["qwk"]["mean"] for m in MODELS]
    lo = [out["models"][m][sp]["qwk"]["ci95_seed0"][0] for m in MODELS]; hi = [out["models"][m][sp]["qwk"]["ci95_seed0"][1] for m in MODELS]
    err = np.array([np.array(mean) - np.array(lo), np.array(hi) - np.array(mean)]).clip(min=0)
    ax.bar(xs, mean, w, color=[COL[m] for m in MODELS], alpha=1.0 if j == 0 else 0.55, edgecolor="black", linewidth=0.6,
           label="in-domain (EyePACS-test)" if j == 0 else "out-of-domain (DDR-test)", yerr=err, capsize=3)
    if len(out["models"][MODELS[0]][sp]["qwk"]["per_seed"]) > 1:
        ax.plot(xs, smean, "k_", markersize=14, mew=2)
ax.set_xticks(range(len(MODELS))); ax.set_xticklabels(MODELS); ax.set_ylabel("QWK"); ax.set_ylim(0, 1)
ax.set_title("QWK in-domain (solid) vs. out-of-domain (light), 95% bootstrap CI");
from matplotlib.patches import Patch
ax.legend(handles=[Patch(fc="gray", ec="k", label="in-domain: EyePACS-test"), Patch(fc="gray", alpha=0.5, ec="k", label="out-of-domain: DDR-test")], fontsize=8)
plt.tight_layout(); plt.savefig(os.path.join(a.out, "e04_in_vs_out_qwk.png"), dpi=170); plt.close()

# e05 forest plot: DDR QWK CI and paired differences
fig, axs = plt.subplots(1, 2, figsize=(11, 3.6))
for i, m in enumerate(MODELS):
    d = out["models"][m]["ddr_test"]["qwk"]; c0 = d["per_seed"][0]
    axs[0].errorbar(c0, i, xerr=[[c0 - d["ci95_seed0"][0]], [d["ci95_seed0"][1] - c0]], fmt="o", color=COL[m], capsize=4)
axs[0].set_yticks(range(len(MODELS))); axs[0].set_yticklabels(MODELS); axs[0].set_xlabel("QWK on DDR-test (seed 0)"); axs[0].set_title("QWK with 95% bootstrap CI")
for i, (k, d) in enumerate(out["paired_diff_qwk_ddr"].items()):
    axs[1].errorbar(d["mean"], i, xerr=[[d["mean"] - d["ci95"][0]], [d["ci95"][1] - d["mean"]]], fmt="s", color="black", capsize=4)
axs[1].axvline(0, color="red", ls="--"); axs[1].set_yticks(range(len(out["paired_diff_qwk_ddr"]))); axs[1].set_yticklabels(list(out["paired_diff_qwk_ddr"]))
axs[1].set_xlabel("difference in QWK on DDR-test"); axs[1].set_title("Paired bootstrap differences (95% CI)")
plt.tight_layout(); plt.savefig(os.path.join(a.out, "e05_bootstrap_ci.png"), dpi=170); plt.close()

# a03 / a04 t-SNE of encoder features (seed 0), coloured by dataset and by grade
from sklearn.manifold import TSNE
rs = np.random.RandomState(0)
sel = {sp: rs.choice(out["n"][sp], min(a.tsne, out["n"][sp]), replace=False) for sp in SPLITS}
fig3, ax3 = plt.subplots(1, len(MODELS), figsize=(4.2 * len(MODELS), 4.2))
fig4, ax4 = plt.subplots(1, len(MODELS), figsize=(4.2 * len(MODELS), 4.2))
ax3 = np.atleast_1d(ax3); ax4 = np.atleast_1d(ax4)
tsne_stats = {}
for j, m in enumerate(MODELS):
    F = np.concatenate([base[sp][m][2][sel[sp]].astype(np.float32) for sp in SPLITS])
    Y = np.concatenate([base[sp][m][1][sel[sp]] for sp in SPLITS])
    D = np.concatenate([np.full(len(sel[sp]), i) for i, sp in enumerate(SPLITS)])
    F = (F - F.mean(0)) / (F.std(0) + 1e-6)
    Z = TSNE(n_components=2, perplexity=30, init="pca", random_state=0).fit_transform(F)
    for i, sp in enumerate(SPLITS):
        ax3[j].scatter(Z[D == i, 0], Z[D == i, 1], s=3, alpha=0.5, color=["#193DB0", "#E65100"][i], label="EyePACS-test" if i == 0 else "DDR-test")
    ax3[j].set_title(m); ax3[j].set_xticks([]); ax3[j].set_yticks([])
    for g in range(K):
        ax4[j].scatter(Z[Y == g, 0], Z[Y == g, 1], s=3, alpha=0.5, color=plt.cm.viridis(g / 4), label=f"grade {g}")
    ax4[j].set_title(m); ax4[j].set_xticks([]); ax4[j].set_yticks([])
    # simple quantitative companion: 5-NN domain mixing (fraction of neighbours from the other dataset; 0.5 = perfectly mixed)
    from sklearn.neighbors import NearestNeighbors
    nn = NearestNeighbors(n_neighbors=6).fit(F)
    nb = nn.kneighbors(F, return_distance=False)[:, 1:]
    mix = float(np.mean(D[nb] != D[:, None]))
    tsne_stats[m] = dict(knn_other_domain_fraction=mix)
    print("t-SNE", m, "kNN other-domain fraction", round(mix, 3), flush=True)
ax3[0].legend(markerscale=4, fontsize=8); ax4[0].legend(markerscale=4, fontsize=8)
fig3.tight_layout(); fig3.savefig(os.path.join(a.out, "a03_tsne_domain.png"), dpi=170)
fig4.tight_layout(); fig4.savefig(os.path.join(a.out, "a04_tsne_grade.png"), dpi=170)
out["tsne_domain_mixing"] = tsne_stats
json.dump(out, open(os.path.join(a.out, "results.json"), "w"), indent=2)

# ---------------------------------------------------------------- LaTeX tables (numbers come only from results.json)
def f3(d):
    return f"{d['mean']:.3f}" + (f" $\\pm$ {d['std']:.3f}" if len(d["per_seed"]) > 1 else "")


def ci(d):
    lo, hi = d["ci95_seed0"]
    return f"[{lo:.3f}, {hi:.3f}]"


T = []
T.append("% Auto-generated by code/eval/analyze.py from results.json. Do not edit by hand.")
T.append("\\begin{tabularx}{\\textwidth}{l c c c c}")
T.append("\\toprule")
T.append("\\textbf{Model} & \\textbf{QWK (EyePACS-test)} & \\textbf{QWK (DDR-test)} & \\textbf{95\\% CI (DDR, seed 0)} & $\\boldsymbol{\\Delta}$\\textbf{QWK} \\\\")
T.append("\\midrule")
for m in MODELS:
    r = out["models"][m]
    T.append(f"{m} & {f3(r['eyepacs_test']['qwk'])} & {f3(r['ddr_test']['qwk'])} & {ci(r['ddr_test']['qwk'])} & {f3(r['delta_qwk'])} \\\\")
T.append("\\bottomrule")
T.append("\\end{tabularx}")
open(os.path.join(a.out, "table_qwk.tex"), "w").write("\n".join(T))
T = ["% Auto-generated", "\\begin{tabularx}{\\textwidth}{l l c c c c}", "\\toprule",
     "\\textbf{Test set} & \\textbf{Model} & \\textbf{QWK} & \\textbf{Macro-F1} & \\textbf{AUC (referable)} & \\textbf{Accuracy} \\\\", "\\midrule"]
for sp in SPLITS:
    for m in MODELS:
        r = out["models"][m][sp]
        T.append(f"{'EyePACS' if sp == 'eyepacs_test' else 'DDR'} & {m} & {f3(r['qwk'])} & {f3(r['macro_f1'])} & {f3(r['auc_ref'])} & {f3(r['acc'])} \\\\")
    if sp == SPLITS[0]:
        T.append("\\midrule")
T += ["\\bottomrule", "\\end{tabularx}"]
open(os.path.join(a.out, "table_secondary.tex"), "w").write("\n".join(T))
T = ["% Auto-generated", "\\begin{tabularx}{\\textwidth}{l c c c c c}", "\\toprule",
     "\\textbf{Model (DDR-test)} & \\textbf{Grade 0} & \\textbf{Grade 1} & \\textbf{Grade 2} & \\textbf{Grade 3} & \\textbf{Grade 4} \\\\", "\\midrule"]
for m in MODELS:
    T.append(m + " & " + " & ".join(f"{v:.3f}" for v in out["models"][m]["ddr_test"]["recall_mean"]) + " \\\\")
T += ["\\bottomrule", "\\end{tabularx}"]
open(os.path.join(a.out, "table_recall.tex"), "w").write("\n".join(T))
print("done ->", a.out)
