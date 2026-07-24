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
| Independent reconstruction | PASS: checks `8/8`, `8/8`, `16/16` |
| Whole-task replacement with `H=0` | FAIL as intended: change `1>0` |
| Genuine task-level envelope 1 | Corrected control PASS |
| Verdict | **FALSIFIED** |

Equation (104) exposes the missing premise: it replaces an entire task
`S_j` by `S'_j`, not the within-task neighbor from Assumption 3.12(i).

The fixed command is `uv run --locked python -m reproduction.run_all`.
Run `11ff7b12-f2dd-4ef2-bdfd-ea3641701954` completed locally in
approximately 10 orchestrated seconds at Git SHA
`7012a238962fd3e18a1f2f67a4f78ebbf69fc7c1`.

Evidence bundle:
[`contract`](../../evidence/claim-6/claim_contract.json) ·
[`source audit`](../../evidence/claim-6/source_audit.md) ·
[`method`](../../evidence/claim-6/method.md) ·
[`raw results`](../../evidence/claim-6/raw_results.json) ·
[`counterexample`](../../evidence/claim-6/counterexample_certificate.json) ·
[`checker output`](../../evidence/claim-6/checker_output.txt) ·
[`control output`](../../evidence/claim-6/negative_control_output.txt) ·
[`limitations`](../../evidence/claim-6/limitations.md) ·
[`EVAL`](../../evidence/claim-6/EVAL.md).
Code:
[`primary verifier`](../../reproduction/claim6.py) ·
[`independent checker`](../../reproduction/claim6_checker.py).
