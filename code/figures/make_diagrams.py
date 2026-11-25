"""Draw the pipeline / system-design / MAE-RETFound diagrams used in the report (Sections 2.2-2.4).
Outputs PNGs (200 dpi, white background) to evidence_figures/06_diagrams/.
Run: python make_diagrams.py
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "evidence_figures", "06_diagrams")
os.makedirs(OUT, exist_ok=True)

BLUE, DARK, LIGHT, GRAY = "#193DB0", "#0D1B67", "#DEE5FA", "#BFBFBF"
GREEN, ORANGE = "#E6F4EA", "#FDEBD3"


def box(ax, x, y, w, h, title, lines=(), fc=LIGHT, ec=BLUE, tc=DARK, fs=10, tfs=11):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=fc, ec=ec, lw=1.6))
    ax.text(x + w / 2, y + h - 0.12, title, ha="center", va="top", fontsize=tfs, fontweight="bold", color=tc)
    if lines:
        ax.text(x + w / 2, y + h - 0.45, "\n".join(lines), ha="center", va="top", fontsize=fs, color="#222222",
                linespacing=1.35)


def arrow(ax, p, q, color=BLUE, style="-|>", ls="-", rad=0.0, lw=1.8):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=16, color=color, lw=lw,
                                 linestyle=ls, connectionstyle=f"arc3,rad={rad}"))


def canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    return fig, ax


def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", os.path.abspath(p))


# ---------------------------------------------------------------- g01 pipeline
def g01():
    fig, ax = canvas(13, 6.0)
    ax.text(6.5, 5.85, "End-to-end workflow: EyePACS (source) → DDR (unseen target)", ha="center",
            fontsize=14, fontweight="bold", color=DARK)
    # row 1
    box(ax, 0.2, 3.7, 2.7, 1.9, "1. Raw data", ["EyePACS: train 35,126", "val 10,906 · test 42,670",
                                              "DDR: test only, 3,759", "(ungradable removed)"], fs=9.5)
    box(ax, 3.6, 3.7, 2.9, 1.9, "2. Preprocessing", ["crop black border", "pad to square → 224×224",
                                                   "JPEG cache · duplicate check", "dHash + NCC (EyePACS ↔ DDR)"], fs=9.5)
    box(ax, 7.2, 3.7, 2.7, 1.9, "3. Training", ["EyePACS-train only", "B1 · B2 · M1 · M2", "5 epochs · B1: 3 seeds",
                                              "B2, M1, M2: 1 seed"], fs=9.5)
    box(ax, 10.3, 3.7, 2.5, 1.9, "4. Model selection", ["best epoch by QWK", "on EyePACS-val", "DDR never used", "→ frozen checkpoint"],
        fc=GREEN, ec="#2E7D32", fs=9.5)
    for a, b in [(2.9, 3.6), (6.5, 7.2), (9.9, 10.3)]:
        arrow(ax, (a + 0.02, 4.65), (b - 0.02, 4.65))
    # row 2 (right to left, under step 4)
    box(ax, 9.4, 0.5, 3.4, 2.3, "5. Final evaluation (once)", ["EyePACS-test (in-domain)", "DDR-test (out-of-domain, main)",
                                                              "once per frozen checkpoint"], fs=9.5)
    box(ax, 4.4, 0.5, 4.2, 2.3, "6. Metrics and analysis", ["QWK (primary) · macro-F1 · recall per grade", "AUC (referable DR) · ΔQWK = in − out",
                                                         "bootstrap 95% CI · confusion matrix · ROC", "Grad-CAM · t-SNE by dataset", "ordinal-decoding variant (val-fitted)"], fs=9.5)
    box(ax, 0.2, 0.5, 3.4, 2.3, "7. Demo and report", ["Gradio web app (local CPU)", "upload → grade + probabilities", "+ Grad-CAM overlay", "LaTeX report (MiKTeX/Overleaf)"], fc=ORANGE,
        ec="#E65100", fs=9.5)
    arrow(ax, (11.55, 3.68), (11.1, 2.82))
    arrow(ax, (9.4, 1.65), (8.6, 1.65))
    arrow(ax, (4.4, 1.65), (3.6, 1.65))
    ax.text(11.9, 3.25, "frozen\ncheckpoint", fontsize=9, color=BLUE, style="italic", ha="left", va="center")
    save(fig, "g01_pipeline.png")


# ---------------------------------------------------------------- g02 system design
def g02():
    fig, ax = canvas(13, 7.4)
    ax.text(6.5, 7.2, "System design: where each component runs", ha="center", fontsize=14, fontweight="bold", color=DARK)
    # lanes
    for (x, w, t) in [(0.1, 3.0, "DATA SOURCES"), (3.4, 5.6, "KAGGLE (cloud, no local GPU needed)"), (9.3, 3.6, "LOCAL MACHINE (CPU)")]:
        ax.add_patch(FancyBboxPatch((x, 0.2), w, 6.5, boxstyle="round,pad=0.02,rounding_size=0.1", fc="#FAFBFE", ec=GRAY, lw=1.2, ls="--"))
        ax.text(x + w / 2, 6.5, t, ha="center", va="top", fontsize=10.5, fontweight="bold", color=BLUE)
    box(ax, 0.3, 4.4, 2.6, 1.6, "EyePACS", ["Kaggle dataset", "(resized 2015 version)"], fs=9.5)
    box(ax, 0.3, 2.4, 2.6, 1.6, "DDR (test split)", ["Kaggle dataset", "DR_grading/test"], fs=9.5)
    box(ax, 0.3, 0.5, 2.6, 1.5, "RETFound weights", ["natureCFP, private", "Kaggle dataset"], fs=9.5, fc=ORANGE, ec="#E65100")
    box(ax, 3.6, 4.5, 2.4, 1.5, "Preprocess kernel", ["CPU · crop, resize,", "cache, dHash"], fs=9.5)
    box(ax, 6.3, 4.5, 2.5, 1.5, "Package kernel", ["CPU · QA + tar files", "(few large files)"], fs=9.5)
    box(ax, 3.6, 2.2, 5.2, 1.9, "Training kernel (GPU, 2 × T4)", ["one independent job per GPU · B1 · B2 · M1 · M2", "logs (CSV/JSON) + curves + best checkpoint", "final evaluation: logits + features on both test sets"], fc=GREEN, ec="#2E7D32", fs=9.5)
    box(ax, 3.6, 0.5, 5.2, 1.3, "Saved outputs", ["best.pt · val logits · *_test.npz (per run)"], fs=9.5)
    box(ax, 9.5, 4.3, 3.2, 1.7, "Analysis (local CPU)", ["bootstrap · ΔQWK · Grad-CAM · t-SNE", "evidence_figures/", "(outputs via Kaggle CLI)"], fs=9.5)
    box(ax, 9.5, 2.4, 3.2, 1.6, "Gradio demo", ["CPU inference", "grade · probabilities · Grad-CAM"], fc=ORANGE, ec="#E65100", fs=9.5)
    box(ax, 9.5, 0.5, 3.2, 1.5, "LaTeX report", ["MiKTeX (XeLaTeX + Biber)", "figures + BibTeX"], fs=9.5)
    arrow(ax, (2.9, 5.2), (3.6, 5.2))
    arrow(ax, (6.0, 5.25), (6.3, 5.25))
    arrow(ax, (7.55, 4.5), (6.5, 4.1))
    arrow(ax, (2.9, 3.2), (3.6, 3.4))
    arrow(ax, (2.9, 1.25), (3.6, 2.5))
    arrow(ax, (6.2, 2.2), (6.2, 1.8))
    arrow(ax, (8.82, 3.3), (9.48, 4.6))
    arrow(ax, (8.82, 1.2), (9.48, 4.45))
    arrow(ax, (11.1, 4.3), (11.1, 4.02))
    arrow(ax, (11.1, 2.4), (11.1, 2.02))
    ax.text(11.2, 2.2, "screenshots", fontsize=8.5, color=BLUE, style="italic", va="center")
    save(fig, "g02_system_design.png")


# ---------------------------------------------------------------- g03 MAE -> RETFound
def g03():
    fig, ax = canvas(13, 6.4)
    ax.text(6.5, 6.2, "From MAE pre-training to DR grading (RETFound, M1)", ha="center", fontsize=14, fontweight="bold", color=DARK)
    ax.text(0.2, 5.65, "Stage A – self-supervised pre-training (done by the RETFound authors, no labels)", fontsize=10.5, color=BLUE, fontweight="bold")
    box(ax, 0.2, 3.5, 2.0, 1.7, "Fundus image", ["224×224", "14×14 patches"], fs=9.5)
    box(ax, 2.7, 3.5, 2.0, 1.7, "Random masking", ["hide 75% of", "patches"], fs=9.5)
    box(ax, 5.2, 3.5, 2.4, 1.7, "ViT-L encoder", ["sees only the", "visible 25%"], fc=GREEN, ec="#2E7D32", fs=9.5)
    box(ax, 8.1, 3.5, 2.2, 1.7, "Light decoder", ["+ mask tokens"], fs=9.5)
    box(ax, 10.8, 3.5, 2.0, 1.7, "Reconstruction", ["loss on masked", "patches (MSE)"], fs=9.5)
    for a, b in [(2.2, 2.7), (4.7, 5.2), (7.6, 8.1), (10.3, 10.8)]:
        arrow(ax, (a, 4.35), (b, 4.35))
    ax.text(0.2, 2.6, "Stage B – supervised fine-tuning on EyePACS-train (our work: M1 / M2; B2 uses ImageNet MAE weights)", fontsize=10.5, color=BLUE, fontweight="bold")
    box(ax, 0.2, 0.5, 2.4, 1.8, "Fundus image", ["standard aug. (M1)", "+ domain-shift aug. (M2)"], fs=9.5)
    box(ax, 3.3, 0.5, 3.0, 1.8, "ViT-L encoder", ["initialised from Stage A", "all patches, layer-wise LR decay"], fc=GREEN, ec="#2E7D32", fs=9.5)
    box(ax, 7.0, 0.5, 2.4, 1.8, "Global pooling", ["average of", "patch tokens"], fs=9.5)
    box(ax, 10.0, 0.5, 2.8, 1.8, "Linear head", ["5 outputs:", "DR grade 0–4"], fc=ORANGE, ec="#E65100", fs=9.5)
    for a, b in [(2.6, 3.3), (6.3, 7.0), (9.4, 10.0)]:
        arrow(ax, (a, 1.4), (b, 1.4))
    arrow(ax, (6.4, 3.5), (4.8, 2.32), color="#2E7D32", ls="--", rad=0.1)
    ax.text(6.7, 3.1, "copy encoder weights (decoder is discarded)", fontsize=9, color="#2E7D32", style="italic", ha="left")
    save(fig, "g03_mae_retfound.png")


if __name__ == "__main__":
    g01()
    g02()
    g03()
