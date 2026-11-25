import io
p = r"c:\SIC\Capstone-Project_latex\chapter03.tex"
c = open(p, encoding="utf-8").read()
bad = chr(12) + "ootnotesize"
print("bad count:", c.count(bad))
c = c.replace(bad, "\\footnotesize")
open(p, "w", encoding="utf-8").write(c)
# scan every tex file for control characters
import glob
for f in glob.glob(r"c:\SIC\Capstone-Project_latex\*.tex"):
    t = open(f, encoding="utf-8").read()
    ctrl = [ch for ch in set(t) if ord(ch) < 32 and ch not in "\n\r\t"]
    tabs = t.count("\t")
    print(f.split("\\")[-1], "ctrl:", [hex(ord(x)) for x in ctrl], "tabs:", tabs)
