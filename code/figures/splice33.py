import re
p='code/figures/sec33.tex.txt'
s=open(p,encoding='utf-8').read()
def sub(a,b):
    global s
    assert a in s, a[:50]
    s=s.replace(a,b,1)
sub("M1 starts higher than B2 (0.587 versus 0.533 after epoch 1) and keeps a lead on macro-F1 in the middle panel throughout, which is consistent with a better starting point from retinal pre-training;",
    "M1 starts higher than B2 (QWK 0.587 versus 0.533 after epoch 1) and ends with the highest validation macro-F1 of all runs (0.535, against 0.496 for B2), which is consistent with a better starting point from retinal pre-training;")
sub("Every model gains between 0.01 and 0.05 QWK","Every model gains between 0.02 and 0.05 QWK")
sub("The ordering on DDR is unchanged (M2 $>$ B2 $>$ B1 $\\approx$ M1)","The ordering on DDR is unchanged (M2 $>$ B2 $>$ B1 $>$ M1)")
sub("the fraction of the 15 nearest neighbours of a point that belong to the other dataset","the fraction of the five nearest neighbours of a point (in feature space) that belong to the other dataset")
sub("Section~\\ref{sec:objectives}","Section~\\ref{subsec:objectives}")
sub("Chapter~\\ref{chap:conclusion}","Chapter~\\ref{chap:projected_impact}")
i=s.index("For M1 the heat is concentrated"); j=s.index("These maps are qualitative;")
s=s[:i]+("For M1 the heat is concentrated on a few small, isolated spots, several of them with a strong peak, while the heat maps of B2 are much broader and cover large parts of the retina, including the periphery and the border of the field of view, so they are less specific. For the correct M1 cases the peaks lie inside the retina rather than on the black border, which is the minimum expected; but they do not always coincide with the visible lesions (for example the bright exudate in the third column is not the strongest region), so the maps should not be read as lesion detections. Among the wrong cases, the second one is a very bright, washed-out image (reference grade~2, predicted grade~0 by both models) and the third a dark image with little lesion contrast; both are examples where image quality, not only pathology, drives the prediction. ")+s[j:]
open(p,'w',encoding='utf-8').write(s)
c=open('Capstone-Project_latex/chapter03.tex',encoding='utf-8').read()
a=c.index("\section{Modeling}"); b=c.index("\section{User Interface}")
c=c[:a]+s.rstrip()+"\n\n"+c[b:]
c=c.replace("\\section{Modeling}\\label","\\section{Modeling}\\label")
open('Capstone-Project_latex/chapter03.tex','w',encoding='utf-8').write(c)
print('ok')
