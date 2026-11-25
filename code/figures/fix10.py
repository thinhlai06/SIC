p = r"c:\SIC\code\figures\make_diagrams.py"
s = open(p, encoding="utf-8").read()
reps = [
    ('"B1 · B2 · M1 · M2", "5 epochs · B1: 3 seeds",\n                                              "B2, M1, M2: 1 seed"', '"B1 · B2 · M1", "15 epochs · B1: 2 seeds",\n                                              "B2, M1: 1 seed"'),
    ("one independent job per GPU · B1 · B2 · M1 · M2", "one independent job per GPU · B1 · B2 · M1"),
]
for a, b in reps:
    assert a in s, a[:50]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
print("ok")
