#!/bin/sh
# Build the report PDF with MiKTeX (xelatex -> biber -> xelatex x2). Usage: sh code/figures/build_pdf.sh
export PATH="$LOCALAPPDATA/Programs/MiKTeX/miktex/bin/x64:$PATH"
cd "$(dirname "$0")/../../Capstone-Project_latex" || exit 1
mkdir -p ../logs
xelatex -interaction=nonstopmode -file-line-error main.tex > ../logs/tex_pass1.log 2>&1
biber main > ../logs/tex_biber.log 2>&1
xelatex -interaction=nonstopmode -file-line-error main.tex > ../logs/tex_pass2.log 2>&1
xelatex -interaction=nonstopmode -file-line-error main.tex > ../logs/tex_pass3.log 2>&1
grep -o "Output written.*" ../logs/tex_pass3.log
grep -E "^!|\.tex:[0-9]+:|Overfull|undefined|Citation.*undefined" ../logs/tex_pass3.log | head -20
