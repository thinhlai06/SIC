p = r"c:\SIC\Capstone-Project_latex\chapter03.tex"
c = open(p, encoding="utf-8").read()
reps = [
    ("width=0.62\\textwidth]{figures/u01_demo_upload.jpg}", "width=0.5\\textwidth]{figures/u01_demo_upload.jpg}"),
    ("width=0.78\\textwidth]{figures/u02_demo_result.jpg}", "width=0.62\\textwidth]{figures/u02_demo_result.jpg}"),
    ("width=\\textwidth]{figures/a03_tsne_domain.jpg}", "width=0.9\\textwidth]{figures/a03_tsne_domain.jpg}"),
    ("width=\\textwidth]{figures/a04_tsne_grade.jpg}", "width=0.9\\textwidth]{figures/a04_tsne_grade.jpg}"),
    ("width=\\textwidth]{figures/t01_curves_all.jpg}", "width=0.95\\textwidth]{figures/t01_curves_all.jpg}"),
    ("width=0.9\\textwidth]{figures/t02_budget_curves.jpg}", "width=0.8\\textwidth]{figures/t02_budget_curves.jpg}"),
    ("width=\\textwidth]{figures/d04_color_stats_domain_gap.png}", "width=0.92\\textwidth]{figures/d04_color_stats_domain_gap.png}"),
    ("width=\\textwidth]{figures/p04_dup_top_pairs.jpg}", "width=0.92\\textwidth]{figures/p04_dup_top_pairs.jpg}"),
]
for a, b in reps:
    assert a in c, a
    c = c.replace(a, b)
open(p, "w", encoding="utf-8").write(c)
print("ok")
