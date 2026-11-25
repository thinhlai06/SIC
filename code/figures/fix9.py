D = r"c:\SIC\Capstone-Project_latex" + "\\"


def load(f):
    return open(D + f, encoding="utf-8").read()


def save(f, s):
    open(D + f, "w", encoding="utf-8").write(s)


d = load("chapter02.tex")
# training length paragraph
i = d.index("\\paragraph{Training length.}")
j = d.index("\\subsection{Class Imbalance and Loss Function}")
tl = r"""\paragraph{Training length.} All models are trained from the pre-trained weights for \textbf{15 epochs} with the cosine schedule above (two warm-up epochs), so that the comparison uses an identical budget. The number was chosen as the largest that fitted the compute quota: a speed benchmark on Kaggle T4 GPUs measured about 36 training images per second for ViT-L at batch size 16 (peak memory 8.4\,GB) when one job uses the GPU alone, about 30 images per second when two jobs run in parallel, and about 192 images per second for ResNet-50. One ViT-L epoch (35{,}126 images plus the validation pass) therefore takes about 21 minutes and a 15-epoch ViT-L run about 5.3 hours; one Kaggle session may run at most 12 hours. A first pilot of 5 epochs showed that the validation QWK had not yet flattened, so all models were retrained from scratch with the longer schedule; the pilot results are not reported.
% [PENDING: add the measured wall-clock time of each final run (from the *_summary.json files)]

"""
d = d[:i] + tl + d[j:]
d = d.replace("$T_w$ the warm-up steps (one epoch)", "$T_w$ the warm-up steps (two epochs)")
# experiment matrix
i = d.index("Table~\\ref{tab:experiments} lists the runs that were actually trained.")
j = d.index("\\section{System Design}")
em = r"""Table~\ref{tab:experiments} lists the runs. The compute quota allows one Kaggle session with two GPUs at a time, and a ViT-L run of 15 epochs occupies one GPU for more than five hours. B2 and M1 therefore run in parallel with one seed (seed 0) each, and the inexpensive ResNet-50 baseline B1 runs afterwards on each GPU with two seeds (0 and 1). A third ViT-L model (M2, with domain-shift augmentation) and the linear-probe experiments of the original plan were dropped for the same reason. Consequently the seed-to-seed spread can be reported only for B1; differences between M1 and B2 are judged with the paired bootstrap on the test images (Section~\ref{subsec:metrics}), which measures test-set sampling noise but not training-seed noise. This limitation is stated again in Section~\ref{subsec:limitations}.

\begin{table}[htbp]
    \centering
    \caption{Experiment matrix (all runs: 15 epochs, trained from the pre-trained weights).}
    \label{tab:experiments}
    \begin{tabularx}{\textwidth}{l p{4.2cm} c X}
        \toprule
        \textbf{ID} & \textbf{Training mode} & \textbf{Seeds} & \textbf{Purpose} \\
        \midrule
        B1 & Full fine-tuning, ResNet-50 & 0, 1 & Conventional baseline \\
        B2 & Full fine-tuning, ViT-L (ImageNet MAE) & 0 & Same architecture as M1, no retinal pre-training \\
        M1 & Full fine-tuning, ViT-L (RETFound) & 0 & Main model \\
        \bottomrule
    \end{tabularx}
\end{table}

"""
d = d[:i] + em + d[j:]
save("chapter02.tex", d)

a = load("appendices.tex")
a = a.replace("1 warm-up epoch, final rate", "2 warm-up epochs, final rate")
save("appendices.tex", a)
print("ok")
