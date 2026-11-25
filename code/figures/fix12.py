D = r"c:\SIC\Capstone-Project_latex" + "\\"
d = open(D + "chapter02.tex", encoding="utf-8").read()
a = "All four models see the same preprocessed images, the same splits and the same training budget; only the initial weights (and, for M2, the augmentation) differ."
assert a in d
d = d.replace(a, "All three models see the same preprocessed images, the same splits and the same training budget; only the architecture and the initial weights differ.")
open(D + "chapter02.tex", "w", encoding="utf-8").write(d)
print("ok")
