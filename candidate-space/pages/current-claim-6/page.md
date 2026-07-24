# Current verification — Claim 6

> Supersedes the pooled-versus-single-task proxy page, which remains preserved
> as **Historical rejected baseline**.

## Exact result: Theorem 3.14 is falsified

[Assumption 3.12](https://ar5iv.labs.arxiv.org/html/2606.06855#S3.Thmtheorem12)
only replaces an observation within a fixed task distribution.
[Theorem 3.14](https://ar5iv.labs.arxiv.org/html/2606.06855#S3.Thmtheorem14)
claims its bound for every `y>0`. The source SHA-256 is
`ca7631580c8a96ff440892fe1ab8d8b42edc84f0dc6eaaf990d404c75f47c7c7`.

Let the meta-distribution be uniform over two point-mass tasks: all labels are
zero in `D0` and all labels are one in `D1`. Set `m=1,n=2`. The meta-algorithm
reads the constant label `theta` and returns a task learner that ignores its
input task and predicts `1-theta`. Use squared loss.

All three clauses hold with `H=G=M=0`: an iid within-task replacement from a
point mass is unchanged, the learner ignores its task sample, and iid test
observations within a point-mass task are identical. Every required moment is
finite at the common `p=3`.

| Meta-training task | Prediction | Empirical risk | Population risk | Gap |
| ---: | ---: | ---: | ---: | ---: |
| `D0` | 1 | 1 | `1/2` | `1/2` |
| `D1` | 0 | 1 | `1/2` | `1/2` |

At `y=1/4`, the event has probability one. The shift, polynomial numerator,
and Gaussian variance are all zero, so the right side is zero.

| Evidence | Result |
| --- | --- |
| Complete meta-training states | 2 of 2 |
| Complete fresh-task states | 2 of 2 per calculation |
| Assumption 3.12(i)–(iii) | PASS pointwise |
| Left probability | `1` |
| Displayed right bound | `0` |
| Independent reconstruction | Must exit 0 |
| Whole-task replacement with `H=0` | Must FAIL |
| Genuine task-level envelope 1 | Corrected control PASS |
| Verdict | **FALSIFIED** |

Equation (104) exposes the missing premise: it replaces an entire task
`S_j` by `S'_j`, not the within-task neighbor from Assumption 3.12(i).

The fixed command is `uv run --locked python -m reproduction.run_all`.
Counterexample:
[`counterexample_certificate.json`](../../../.openresearch/artifacts/claim-6/counterexample_certificate.json).
Primary verifier: [`claim6.py`](../../../reproduction/claim6.py).
Independent checker: [`claim6_checker.py`](../../../reproduction/claim6_checker.py).
