p = r"c:\SIC\code\figures\make_diagrams.py"
s = open(p, encoding="utf-8").read()
reps = [
    ("(our work: M1 / M2; B2 uses ImageNet MAE weights)", "(our work: M1; B2 uses ImageNet MAE weights)"),
    ('["standard aug. (M1)", "+ domain-shift aug. (M2)"]', '["standard augmentation", "(crop, flip, rotation, jitter)"]'),
]
for a, b in reps:
    assert a in s, a[:50]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
print("ok")
