c=open('chapter03.tex',encoding='utf-8').read()
reps=[("width=0.9\textwidth]{figures/u01_demo_upload.jpg}","width=0.62\textwidth]{figures/u01_demo_upload.jpg}"),
("width=0.9\textwidth]{figures/u02_demo_result.jpg}","width=0.78\textwidth]{figures/u02_demo_result.jpg}"),
("width=0.85\textwidth]{figures/e04_inout.jpg}","width=0.7\textwidth]{figures/e04_inout.jpg}"),
("width=\textwidth]{figures/e01_confusion.jpg}","width=0.92\textwidth]{figures/e01_confusion.jpg}"),
("width=\textwidth]{figures/a01_gradcam.jpg}","width=0.92\textwidth]{figures/a01_gradcam.jpg}"),
("width=\textwidth]{figures/e02_roc.jpg}","width=0.85\textwidth]{figures/e02_roc.jpg}"),
("width=\textwidth]{figures/e05_bootstrap.jpg}","width=0.9\textwidth]{figures/e05_bootstrap.jpg}")]
for a,b in reps:
    assert a in c,a; c=c.replace(a,b)
open('chapter03.tex','w',encoding='utf-8').write(c); print('ok')
