c=open('chapter03.tex',encoding='utf-8').read()
a="    \small\n    \input{tables/table_qwk.tex}"
assert a in c; c=c.replace(a,"    \footnotesize\n    \input{tables/table_qwk.tex}")
a="    \small\n    \input{tables/table_ordinal.tex}"
assert a in c; c=c.replace(a,"    \footnotesize\n    \input{tables/table_ordinal.tex}")
open('chapter03.tex','w',encoding='utf-8').write(c)
d=open('chapter02.tex',encoding='utf-8').read()
a="Eight EyePACS training images: original (top), standard augmentation of B1/B2/M1 (middle) and domain-shift augmentation of M2 (bottom)."
assert a in d; d=d.replace(a,"EyePACS training images: original (top), standard augmentation (middle), domain-shift augmentation of M2 (bottom).")
open('chapter02.tex','w',encoding='utf-8').write(d); print('ok')
