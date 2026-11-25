p = r"c:\SIC\Capstone-Project_latex\preamble.tex"
lines = open(p, encoding="utf-8").read().split("\n")
for i, l in enumerate(lines):
    if "keywordstyle" in l:
        lines[i] = "\\lstset{keywordstyle=\\color{SamsungBlue}, basicstyle=\\footnotesize\\ttfamily}"
        print("fixed line", i + 1)
open(p, "w", encoding="utf-8").write("\n".join(lines))
for f in ["preamble.tex", "chapter03.tex", "chapter02.tex", "chapter01.tex", "chapter04.tex", "appendices.tex"]:
    t = open(r"c:\SIC\Capstone-Project_latex" + "\\" + f, encoding="utf-8").read()
    bad = [hex(ord(ch)) for ch in set(t) if ord(ch) < 32 and ch not in "\n\r"]
    print(f, bad)
