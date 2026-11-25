D = r"c:\SIC\Capstone-Project_latex" + "\\"
c = open(D + "chapter03.tex", encoding="utf-8").read()

# ---- 3.3 and 3.4: placeholders (old 5-epoch pilot results removed)
i = c.index("\\section{Modeling}")
j = c.index("\\section{Testing and Improvements}")
ph = r"""\section{Modeling}
\label{sec:modeling}

% [PENDING: Section 3.3 is written when the 15-epoch runs (M1, B2, B1) have finished on Kaggle. Planned content, each with its figure and a descriptive paragraph:
%  3.3.1 Training dynamics (validation QWK / macro-F1 / loss per epoch, did the curves flatten?)         -> t01
%  3.3.2 Main results table (QWK, macro-F1, AUC referable, accuracy; EyePACS-test and DDR-test)
%  3.3.3 Prior-matched in-domain vs out-of-domain comparison, paired bootstrap                             -> e04, e05
%  3.3.4 Per-grade behaviour: confusion matrices, recall                                                  -> e01
%  3.3.5 Referable DR: ROC                                                                                -> e02
%  3.3.6 Effect of the decision rule (ordinal decoding fitted on EyePACS-validation)
%  3.3.7 Interpretability: Grad-CAM, t-SNE                                                                -> a01, a03, a04
%  3.3.8 Summary of H1 and H2]
The models have been trained and are being evaluated at the time of this draft; no result number is reported here before the runs have finished.

\section{User Interface}
\label{sec:user_interface}

% [PENDING: Section 3.4 is written when the final M1 checkpoint is available: screenshots of the upload page and the prediction page (Figures u01, u02), see Section 2.4.3 for the design]
The demo application described in Section~\ref{subsec:demo_design} is run with the final M1 checkpoint once training has finished.

"""
c = c[:i] + ph + c[j:]

# ---- 3.5: problems list
a = "    \\item \\textbf{GPU scheduling.}"
assert a in c
extra = ("    \\item \\textbf{Pilot runs were too short.} A first set of 5-epoch runs reached a QWK of only about 0.7 and the validation curves had not flattened; a continuation attempt and an 8-epoch attempt were also started, but the 8-epoch session was cancelled by the platform because the session timeout had been set to 150 minutes instead of the full run length. All pilot results were discarded and all models were retrained from scratch for 15 epochs with a session timeout of 12 hours.\n")
c = c.replace(a, extra + a)

# ---- error analysis subsection -> pending
k1 = c.index("\\subsection{Error Analysis}")
k2 = c.index("\\subsection{Limitations}")
c = c[:k1] + "% [PENDING: 3.5.4 Error analysis: size and direction of the arg-max errors on DDR (one-grade versus larger errors, under- versus over-grading) and examples of wrong cases, after the final evaluation]\n\n" + c[k2:]

# ---- limitations
l1 = c.index("    \\item The DDR colour statistics were inspected during the EDA")
l2 = c.index("\\end{itemize}", l1)
lim = r"""    \item No domain-generalization method (augmentation or domain-invariant learning) was applied; a model with domain-shift augmentation (M2) was planned but dropped because the GPU quota allowed only two ViT-L runs in parallel. The study therefore measures the robustness of pre-trained representations only.
    \item \textbf{Training budget.} All models were trained for 15 epochs, the largest number that fitted the free GPU quota; the official RETFound recipe uses more. % [PENDING: add whether the validation QWK had flattened at epoch 15]
    \item B2 and M1 were trained with a single seed and B1 with two; the bootstrap intervals measure the sampling noise of the test images, not the variation between training runs, so small differences between M1 and B2 should not be over-interpreted.
    \item All images were reduced to $224\times224$ pixels, which hides small lesions and probably limits the recognition of grade~1; the absolute QWK is therefore below the values published for high-resolution systems, and the conclusions concern the \emph{relative} behaviour of the models under identical conditions.
    \item EyePACS labels come from a single grader per image and are noisy, whereas DDR was graded by a team of seven trained graders (Section~\ref{subsec:ddr}); part of any difference between the two test sets may come from this difference in label quality.
"""
c = c[:l1] + lim + c[l2:]
# remove the M2 limitation sentence fragment in the RETFound bullet
c = c.replace("in-domain EyePACS-test scores of M1 and M2 may be optimistic", "the in-domain EyePACS-test score of M1 may be optimistic")
open(D + "chapter03.tex", "w", encoding="utf-8").write(c)

# ---- chapter 4
p4 = r"""\chapter{Projected Impact}
\label{chap:projected_impact}

\section{Accomplishments and Benefits}
\label{sec:accomplishments}

\subsection{What Was Achieved}
\label{subsec:achieved}

The project delivered a complete, reproducible experiment on the robustness of diabetic retinopathy grading across fundus datasets:
\begin{itemize}[leftmargin=1.5em]
    \item a preprocessing pipeline that converted about 92{,}000 EyePACS and DDR photographs into a common $224\times224$ format, with quality checks, a verified absence of duplicates between the two datasets, and a strict separation of data roles in which DDR is used only once, for the final test;
    \item a training library with the RETFound fine-tuning recipe (layer-wise learning-rate decay, label smoothing, square-root balanced sampling, mixed precision) that runs the comparison on free Kaggle T4 GPUs, with one independent job per GPU;
    \item a controlled comparison of three models (B1 ResNet-50, B2 ViT-L with ImageNet MAE weights, M1 RETFound) with QWK as the primary metric, bootstrap confidence intervals, a prior-matched in-domain versus out-of-domain comparison and an ordinal-decoding variant;
    \item diagnostic analyses (confusion matrices, per-grade recall, ROC for referable DR, error structure, Grad-CAM and t-SNE) and a working English web demo that grades an uploaded fundus photograph and shows the probabilities and a Grad-CAM overlay.
\end{itemize}

\subsection{Main Findings}
\label{subsec:main_findings}

% [PENDING: written after the final results: QWK on DDR and EyePACS for M1, B2, B1; whether H1 and H2 are supported; the effect of the decision rule; what Grad-CAM and t-SNE show]

\subsection{Benefits}
\label{subsec:benefits}

\begin{itemize}[leftmargin=1.5em]
    \item \textbf{For screening practice.} An automated assistant trained on one public dataset and evaluated on a dataset collected in another country shows how far such a tool can support primary-care screening where ophthalmologists are scarce. The demo shows how a tool could present its result with probabilities and a visual explanation.
    \item \textbf{For model selection.} The study gives practitioners a concrete warning: a better in-domain score or a larger pre-training set does not guarantee a better score on a new device or population, and every deployment needs a local test set.
    \item \textbf{For students and future teams.} The scripts, logs and figures form a reproducible template for dataset-shift studies under a small compute budget (free GPUs only), including a leakage-controlled data protocol and a bootstrap-based way to judge differences.
\end{itemize}

\section{Future Improvements}
\label{sec:future_improvements}

\subsection{Limitations of This Study}
\label{subsec:limits_summary}

The limitations in Section~\ref{subsec:limitations} bound the conclusions: only one source and one target dataset, a single training seed for the ViT-L models, a training budget of 15 epochs, an input resolution of 224 pixels, and no domain-generalization method. The interval widths in this report measure only the sampling noise of the test set.

\subsection{Roadmap}
\label{subsec:roadmap}

\begin{enumerate}[leftmargin=1.5em]
    \item \textbf{Higher resolution.} Training at 448 or 512 pixels, with the position embeddings interpolated, should improve the recognition of mild disease (grade~1); this needs more GPU memory and time than the free quota allowed.
    \item \textbf{More seeds and longer schedules.} Three or more seeds per ViT-L model and 30--50 epochs would turn the single-run comparisons into statistically solid ones.
    \item \textbf{Domain-shift augmentation.} A fourth model, RETFound with augmentation that imitates camera differences (colour casts, gamma, blur, compression, as in GDRNet), was planned but could not be trained within the quota; it would show whether augmentation adds robustness on top of retinal pre-training.
    \item \textbf{More domains.} Adding more source datasets (for example Messidor-2 or APTOS) and more target datasets would show whether the findings hold beyond EyePACS $\rightarrow$ DDR and enable leave-one-domain-out evaluation.
    \item \textbf{Methods that target the domain gap directly.} Examples are test-time adaptation of the normalisation statistics, continued self-supervised pre-training on unlabelled target-domain photographs, and training objectives that encourage domain-invariant features.
    \item \textbf{Ordinal and calibrated outputs.} Training with an ordinal loss and calibrating the probabilities would use the grade order during training, not only at decoding, and would make the referral recommendation of the demo more reliable.
    \item \textbf{Clinical validation.} Any real use requires prospective validation with ophthalmologists, a study of fairness across devices and populations, and regulatory review; the present demo is a research prototype only.
\end{enumerate}
"""
open(D + "chapter04.tex", "w", encoding="utf-8").write(p4)
print("ok")
