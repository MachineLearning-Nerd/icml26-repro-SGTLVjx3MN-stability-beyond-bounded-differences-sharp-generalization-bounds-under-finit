# Current verification — Claim 3

> This page supersedes the historical finite-sample moment proxy. The old page
> remains preserved as **Historical rejected baseline**.

## Exact claim and source

[Assumption 3.1](https://ar5iv.labs.arxiv.org/html/2606.06855#S3.Thmtheorem1)
requires, for every replaced coordinate, a pointwise loss increment bounded by
`beta H(z_i,z_i')`, where `H` has a finite `p`-th moment for some `p>=2`.
Remark 3.2 states that this strictly extends deterministic uniform stability.
The retrieved paper bytes have SHA-256
`ca7631580c8a96ff440892fe1ab8d8b42edc84f0dc6eaaf990d404c75f47c7c7`.

## Exact witness

Let the data be iid `N(0,1)`, let `A_S` be the sample mean, and use the
nonnegative loss `ell(A_S,z)=|A_S|`. For every real sample and replacement,

`||A_S|-|A_{S^i}|| <= |A_S-A_{S^i}| = |z_i-z_i'|/m`.

Therefore `beta=1/m` and `H(z,z')=|z-z'|`. Since
`Z-Z'~N(0,2)`, `E H^2=2`. Yet for every finite bound `B`, setting
`z_i=m(B+1)`, `z_i'=0`, and all other coordinates to zero gives loss increment
`B+1>B`. The deterministic uniform-stability diameter is therefore infinite.

| Audit item | Result |
| --- | --- |
| Exact replace-one inequality | PASS |
| `p=2` moment | `E H^2=2` |
| Uniform-stability supremum | Infinite |
| Independent checker | Must exit 0 |
| Halved-beta control | Must FAIL: `1 > 1/2` |
| Cauchy control | Must FAIL: no finite second moment |
| Verdict | **VERIFIED** |

Fixed command: `uv run --locked python -m reproduction.run_all`.
The environment is Python 3.12 with the committed `uv.lock`; numerical thread
pools are limited to one thread. Raw certificate:
[`raw_results.json`](../../../.openresearch/artifacts/claim-3/raw_results.json).
Primary verifier: [`claim3.py`](../../../reproduction/claim3.py). Independent
checker: [`claim3_checker.py`](../../../reproduction/claim3_checker.py).

## Limitations

This verifies Claim 3’s definition and strict-extension implication. It does
not claim that this minimal witness is a useful predictor, and it does not
verify Theorem 3.4.

