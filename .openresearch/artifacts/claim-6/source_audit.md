# Claim 6 source audit

Assumption 3.12 and Theorem 3.14 are at
`https://ar5iv.labs.arxiv.org/html/2606.06855#S3.Thmtheorem12` and
`https://ar5iv.labs.arxiv.org/html/2606.06855#S3.Thmtheorem14`. The source was
retrieved 2026-07-24 and has SHA-256
`ca7631580c8a96ff440892fe1ab8d8b42edc84f0dc6eaaf990d404c75f47c7c7`.

Assumption 3.12(i) changes one observation in one task, drawing its replacement
from the same fixed task distribution `D_j`. Clause (ii) changes one
observation in the new task's training sample. Clause (iii) changes the test
observation. Theorem 3.14 claims its bound for every `y>0`.

Equation (104) of the proof instead introduces `S^(j)` by replacing the entire
task dataset `S_j` with an iid task `S'_j`. That operation can change the
latent task distribution and is not a neighbor controlled by clause (i). The
proof nevertheless bounds it by one `H`.

Let the meta-distribution be uniform over the point masses at labels zero and
one, with `m=1,n=2`. The meta-algorithm reads the constant label `theta` from
its sole meta-training task and returns a task learner that ignores its task
and predicts `1-theta`. Use squared loss.

Every stated within-task replacement is unchanged, the task learner ignores
its task sample, and iid test observations within a point-mass task coincide.
Thus `H=G=M=0` satisfies all three clauses with the common `p=3`.

Empirical meta-risk is one and conditional population meta-risk is one half.
The gap is one half in both complete meta-training states. At `y=1/4`, the
left probability is one and the displayed right bound is zero.
