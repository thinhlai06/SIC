p3 = r"c:\SIC\Capstone-Project_latex\chapter03.tex"
c = open(p3, encoding="utf-8").read()
i = c.index("\\subsection{Effect of a Longer Training Schedule}")
j = c.index("\\subsection{Summary of the Hypotheses}")
new = r"""\subsection{Effect of a Longer Training Schedule}
\label{subsec:budget_check}

Because the validation QWK was still rising after epoch 5, M1 and B2 were also started with an 8-epoch cosine schedule (a third Kaggle session, two jobs in parallel). This check could \emph{not} be completed: after about 2.5 hours, when B2 had finished epoch 7 and M1 epoch 6, the Kaggle session was cancelled by the platform (the script's own time limit of 240 minutes had not been reached, and no reason was reported). The runs therefore have validation curves but no final evaluation on the test sets, and no DDR number exists for them. There was not enough time before the deadline to repeat them, and they are \emph{not} used in any table of this chapter. Figure~\ref{fig:budget_curves} compares their validation curves with those of the finished 5-epoch runs.

\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.9\textwidth]{figures/t02_budget_curves.jpg}
    \caption{EyePACS-validation QWK (left) and macro-F1 (right) of B2 (orange) and M1 (blue): finished 5-epoch runs (solid) and the interrupted 8-epoch runs (dashed). The dashed runs stopped before the learning rate was annealed.}
    \label{fig:budget_curves}
\end{figure}

For B2 the validation QWK of the 8-epoch run reached 0.686 after epoch 7, higher than the final value of the 5-epoch run (0.668), and was still rising; its macro-F1 also rose (0.510 versus 0.496). For M1 the 8-epoch run reached 0.686 and 0.681 after epochs 5 and 6, which is not higher than the 5-epoch value (0.694), although its learning rate was still far from the end of the cosine schedule. Since the last epochs of a cosine schedule usually bring the largest gain, these partial curves cannot predict the final result. They only indicate that (i) the 5-epoch budget did not let the models converge, (ii) B2 seems to profit at least as much from additional epochs as M1, so the lower in-domain score of B2 at 5 epochs is not simply a sign of weaker pre-training, and (iii) the ranking of B2 and M1 on DDR in Table~\ref{tab:main_qwk} may change with a longer schedule. This remains an open question of the study.

"""
c = c[:i] + new + c[j:]
old = "% [PENDING: finalize the training-budget limitation after the 8-epoch check (k3) is analysed; the items below already hold for the 5-epoch runs.]"
assert old in c
c = c.replace(old, "")
anchor = "    \\item B2, M1 and M2 were trained with a single seed"
add = "    \\item \\textbf{Training budget.} All models were trained for only 5 epochs, the number that fitted the free GPU quota, and the validation QWK was still rising at the end. The attempted 8-epoch check was interrupted by the platform and gave no test result (Section~\\ref{subsec:budget_check}). All comparisons therefore refer to a short, equal budget, and the absolute scores, and possibly the ranking of the models, could change with longer training.\n"
assert anchor in c
c = c.replace(anchor, add + anchor)
open(p3, "w", encoding="utf-8").write(c)

p2 = r"c:\SIC\Capstone-Project_latex\chapter02.tex"
d = open(p2, encoding="utf-8").read()
a = "therefore an additional 8-epoch run of M1 and B2 was trained to measure how much the short budget limits the results (Section~\\ref{subsec:budget_check})."
assert a in d
d = d.replace(a, "therefore an additional 8-epoch run of M1 and B2 was started to measure how much the short budget limits the results; it was interrupted by the platform before completion (Section~\\ref{subsec:budget_check}).")
a = "B2 & Full fine-tuning & 5 and 8 & 0 &"
assert a in d
d = d.replace(a, "B2 & Full fine-tuning & 5 (8, interrupted) & 0 &")
a = "M1 & Full fine-tuning & 5 and 8 & 0 &"
assert a in d
d = d.replace(a, "M1 & Full fine-tuning & 5 (8, interrupted) & 0 &")
open(p2, "w", encoding="utf-8").write(d)

p4 = r"c:\SIC\Capstone-Project_latex\chapter04.tex"
e = open(p4, encoding="utf-8").read()
a = "% [PENDING: add one sentence with the outcome of the 8-epoch check (Section 3.3.8) after k3 is analysed]"
assert a in e
e = e.replace(a, "The validation curves were still rising after five epochs, and an 8-epoch check that would have measured the effect of a longer schedule was interrupted by the compute platform, so the rankings reported here hold for a short, equal training budget.")
open(p4, "w", encoding="utf-8").write(e)

pa = r"c:\SIC\Capstone-Project_latex\appendices.tex"
f = open(pa, encoding="utf-8").read()
a = "5 (8 for the budget check)"
assert a in f
f = f.replace(a, "5")
open(pa, "w", encoding="utf-8").write(f)
print("ok")
