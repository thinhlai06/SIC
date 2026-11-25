p = r"c:\SIC\Capstone-Project_latex\chapter03.tex"
c = open(p, encoding="utf-8").read()
reps = [("0.008 QWK on the validation set and 0.016 on DDR", "0.008 QWK on the validation set and 0.020 on DDR"),
        ("whereas DDR labels are a consensus of several graders; part", "whereas DDR was graded by a team of seven trained graders (Section~\ref{subsec:target_domain}); part"),
        ("DDR labels also come from a consensus of several graders and are probably cleaner than the single-grader EyePACS labels.", "DDR was graded by a team of trained graders and its labels are probably cleaner than the single-grader EyePACS labels.")]
for a, b in reps:
    assert a in c, a[:40]
    c = c.replace(a, b)
open(p, "w", encoding="utf-8").write(c)
print("ok")
