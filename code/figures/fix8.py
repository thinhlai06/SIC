"""Scope reduction: three models (B1, B2, M1), 15 epochs, no M2 / H3. Patches chapter01, chapter02, chapter03 (3.1-3.2), appendices."""
import re

D = r"c:\SIC\Capstone-Project_latex" + "\\"


def load(f):
    return open(D + f, encoding="utf-8").read()


def save(f, s):
    open(D + f, "w", encoding="utf-8").write(s)


def sub(s, a, b, count=1):
    assert a in s, "NOT FOUND: " + a[:70]
    return s.replace(a, b, count)


# ------------------------------------------------------------------ chapter 1
c = load("chapter01.tex")
c = sub(c, "Two ideas promise robustness: (i) representations learned by SSL on large and varied unlabelled retinal collections, and (ii) augmentation that imitates the differences between cameras and sites, as in the FundusAug module of GDRNet \\cite{gdrnet2023}. Both are attractive, but their benefit in a strictly controlled \\emph{train-on-one-dataset, test-on-another} protocol has to be measured and not assumed.",
        "Two ideas promise robustness: (i) representations learned by SSL on large and varied unlabelled retinal collections, and (ii) augmentation that imitates the differences between cameras and sites, as in the FundusAug module of GDRNet \\cite{gdrnet2023}. This project studies the first idea; the second is left for future work (Section~\\ref{sec:future_improvements}). The benefit of SSL pre-training in a strictly controlled \\emph{train-on-one-dataset, test-on-another} protocol has to be measured and not assumed.")
c = sub(c, "Do self-supervised pre-training on retinal images (RETFound) and domain-shift augmentation help a DR grading model keep its performance when it is trained on EyePACS and tested on the unseen DDR dataset, and by how much?",
        "Does self-supervised pre-training on retinal images (RETFound) help a DR grading model keep its performance when it is trained on EyePACS and tested on the unseen DDR dataset, and by how much?")
c = sub(c, "We formulate three hypotheses, each", "We formulate two hypotheses, each")
c = sub(c, "    \\item[H3.] Adding domain-shift augmentation (M2) reduces this drop further compared with M1.\n", "")
c = sub(c, "Train and compare four models: B1 (ResNet-50, ImageNet), B2 (ViT-L, ImageNet MAE), M1 (RETFound) and M2 (RETFound with domain-shift augmentation), using three random seeds for the inexpensive ResNet-50 baseline and one seed for the ViT-L models because of the GPU budget.",
        "Train and compare three models for 15 epochs each: B1 (ResNet-50, ImageNet), B2 (ViT-L, ImageNet MAE) and M1 (RETFound), using two random seeds for the inexpensive ResNet-50 baseline and one seed for the ViT-L models because of the GPU budget.")
c = sub(c, "Domain generalization is limited to data augmentation, because only one labelled source domain is available.",
        "No domain-generalization algorithm (augmentation, domain-invariant learning) is applied; the study measures how robust the representations of the pre-trained models are, because only one labelled source domain is available.")
c = sub(c, "RETFound fine-tuning (M1), domain-shift augmentation (M2), training scripts", "RETFound fine-tuning (M1), training scripts")
save("chapter01.tex", c)

# ------------------------------------------------------------------ chapter 2
d = load("chapter02.tex")
d = sub(d, "The four models compared. All are fine-tuned", "The three models compared. All are fine-tuned")
d = sub(d, "        M2 & ViT-L/16 (RETFound)      & as M1                           & M1 plus domain-shift augmentation: isolates the effect of augmentation \\\\\n", "")
d = sub(d, "M1 versus M2 tells whether domain-shift augmentation adds robustness. ", "")
d = sub(d, "A linear probe (frozen encoder with a trainable linear head), which would measure the quality of the frozen representations alone, was considered but dropped because of the limited time; all four models are fully fine-tuned.",
        "A fourth model (M2: RETFound with domain-shift augmentation) and a linear probe (frozen encoder with a trainable linear head) were part of the original plan but were dropped because of the limited GPU time; all three models are fully fine-tuned.")
# augmentation subsection
i = d.index("\\subsection{Domain-Shift Augmentation for M2}")
j = d.index("\\subsection{Evaluation Metrics}")
aug = r"""\subsection{Data Augmentation}
\label{subsec:augmentation}

All models use the same standard augmentation, applied only to the training images: random resized crop (scale 0.6--1), horizontal flip, rotation up to $20^\circ$ and light brightness/contrast jitter. The validation and test images are only normalised. No augmentation that imitates differences between cameras (colour casts, gamma, blur, JPEG compression), such as the FundusAug module of GDRNet \cite{gdrnet2023}, is used: such a model (M2) was part of the original plan, but the GPU budget allowed only two ViT-L runs in parallel, and the comparison of retinal and ImageNet pre-training (B2 versus M1) was given priority. Section~\ref{sec:future_improvements} lists it as future work.

"""
d = d[:i] + aug + d[j:]
d = sub(d, "For B1, which was trained with three seeds,", "For B1, which was trained with two seeds,")
d = sub(d, "the four models are trained on EyePACS-train only", "the three models are trained on EyePACS-train only")
save("chapter02.tex", d)

# ------------------------------------------------------------------ chapter 3 (3.1, 3.2)
e = load("chapter03.tex")
e = sub(e, "The standard and the domain-shift variants are described in Section~\\ref{subsec:dg_aug}; the validation and test images only receive the normalisation of step~6.",
        "The augmentation is described in Section~\\ref{subsec:augmentation}; the validation and test images only receive the normalisation of step~6.")
e = sub(e, "This is a first, quantitative argument for including colour augmentation (gain, gamma, jitter) in model M2.",
        "This is a first, quantitative sign that the models will meet a colour shift at test time.")
e = sub(e, "The EDA leads to four concrete decisions and one limitation:", "The EDA leads to three concrete decisions and one observation:")
e = sub(e, "    \\item Include colour and quality augmentation in M2 (colour gap).\n", "")
k1 = e.index("    \\item \\emph{Limitation:} the colour statistics of DDR were looked at")
k2 = e.index("\\end{itemize}", k1)
e = e[:k1] + "    \\item \\emph{Observation:} the colour gap suggests that colour augmentation could help; it was not applied in this study (Section~\\ref{subsec:augmentation}), so the colour shift remains in the test conditions.\n" + e[k2:]
save("chapter03.tex", e)

# ------------------------------------------------------------------ appendices
a = load("appendices.tex")
a = sub(a, "5                       & Best epoch", "15                      & Best epoch")
a = sub(a, "B1; seed 0 only for B2, M1, M2", "B1 (seeds 0, 1); seed 0 only for B2 and M1")
a = sub(a, "0, 1, 2                 &", "0, 1                    &")
save("appendices.tex", a)
print("ok")
