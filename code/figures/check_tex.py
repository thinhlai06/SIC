"""Static sanity check of the LaTeX report (no LaTeX installation needed):
labels/refs, citations vs. references.bib, balanced environments, forbidden \\subsubsection.
Usage: python check_tex.py <path-to-Capstone-Project_latex>
"""
import glob
import os
import re
import sys

root = sys.argv[1] if len(sys.argv) > 1 else "."
files = [f for f in glob.glob(os.path.join(root, "*.tex")) if not f.endswith("main.tex")]
tex = "\n".join(open(f, encoding="utf8").read() for f in files)
nc = "\n".join(re.sub(r"(?<!\\)%.*", "", l) for l in tex.split("\n"))
labels = set(re.findall(r"\\label\{([^}]+)\}", nc))
refs = set(re.findall(r"\\(?:ref|eqref)\{([^}]+)\}", nc))
print("refs without label:", sorted(refs - labels))
cites = set(k.strip() for m in re.findall(r"\\cite\{([^}]+)\}", nc) for k in m.split(","))
bib = set(re.findall(r"@\w+\{([^,]+),", open(os.path.join(root, "references.bib"), encoding="utf8").read()))
print("cited but not in bib:", sorted(cites - bib))
print("in bib but never cited:", sorted(bib - cites))
for env in ["figure", "table", "equation", "itemize", "enumerate", "tabularx", "lstlisting", "quote", "cases"]:
    b = len(re.findall(r"\\begin\{%s\}" % env, nc))
    e = len(re.findall(r"\\end\{%s\}" % env, nc))
    if b != e:
        print("UNBALANCED", env, b, e)
print("equations:", len(re.findall(r"\\begin\{equation\}", nc)), "| figures:", len(re.findall(r"\\begin\{figure\}", nc)),
      "| tables:", len(re.findall(r"\\begin\{table\}", nc)), "| subsubsection:", nc.count("subsubsection"))
print("braces balanced per file:")
for f in files:
    t = "\n".join(re.sub(r"(?<!\\)%.*", "", l) for l in open(f, encoding="utf8").read().split("\n"))
    t = re.sub(r"\\[{}]", "", t)
    print(" ", os.path.basename(f), t.count("{") - t.count("}"))
figs = set(re.findall(r"includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", nc))
print("missing figure files:", [f for f in figs if not os.path.exists(os.path.join(root, f))])
