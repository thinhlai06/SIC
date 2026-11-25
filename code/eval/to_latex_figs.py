"""Copy the result figures of the final analysis to evidence_figures/ and to Capstone-Project_latex/figures (compressed JPEG),
and the generated tables to Capstone-Project_latex/tables.
Usage: python to_latex_figs.py <results dir>   (expects e01..e05, a01, a03, a04, t01_curves_all.png in that dir)"""
import os
import shutil
import sys

from PIL import Image

R = sys.argv[1]
ROOT = r"c:\SIC"
E = os.path.join(ROOT, "evidence_figures")
F = os.path.join(ROOT, "Capstone-Project_latex", "figures")
T = os.path.join(ROOT, "Capstone-Project_latex", "tables")
os.makedirs(T, exist_ok=True)
plan = {  # file in results dir -> (evidence subfolder, latex name)
    "t01_curves_all.png": ("03_training", "t01_curves_all"),
    "e01_confusion_all.png": ("04_evaluation", "e01_confusion"),
    "e02_roc_referable.png": ("04_evaluation", "e02_roc"),
    "e03_perclass_recall_ddr.png": ("04_evaluation", None),
    "e04_in_vs_out_qwk.png": ("04_evaluation", "e04_inout"),
    "e05_bootstrap_ci.png": ("04_evaluation", "e05_bootstrap"),
    "a01_gradcam_ddr_examples.png": ("05_analysis", "a01_gradcam"),
    "a03_tsne_domain.png": ("05_analysis", "a03_tsne_domain"),
    "a04_tsne_grade.png": ("05_analysis", "a04_tsne_grade"),
}
for fn, (sub, name) in plan.items():
    src = os.path.join(R, fn)
    if not os.path.exists(src):
        print("missing", fn)
        continue
    os.makedirs(os.path.join(E, sub), exist_ok=True)
    shutil.copy(src, os.path.join(E, sub, fn))
    if name:
        im = Image.open(src).convert("RGB")
        if im.size[0] > 1800:
            im = im.resize((1800, int(im.size[1] * 1800 / im.size[0])), Image.LANCZOS)
        im.save(os.path.join(F, name + ".jpg"), quality=88, optimize=True)
        print("figure", name)
for fn in os.listdir(R):
    if fn.startswith("table_") and fn.endswith(".tex"):
        shutil.copy(os.path.join(R, fn), os.path.join(T, fn))
        print("table", fn)
