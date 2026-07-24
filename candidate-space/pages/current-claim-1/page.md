# Current verification — Claim 1

> Supersedes the Monte Carlo page, which remains preserved as
> **Historical rejected baseline**.

## Exact theorem

[Theorem 2.2](https://ar5iv.labs.arxiv.org/html/2606.06855#S2.Thmtheorem2)
quantifies over every independent product distribution, measurable `f`, valid
finite-`Lp` replace-one envelopes for fixed `p>=2`, and every `z>0`. It states

`P(|f-Ef|>z) <= c1 M_p/z^p + 2 exp(-c2 z^2/M_2)`,

where `M_q=sum_i E|H_i|^q`,
`c1=4(4(p+2)/p)^p`, and `c2=1/[2(p+2)^2 e^p]`.
The source SHA-256 is
`ca7631580c8a96ff440892fe1ab8d8b42edc84f0dc6eaaf990d404c75f47c7c7`.

## Universal derivation and checks

The current route reconstructs the Doob projection identity, conditional
Jensen envelope, truncation/centering, bounded-increment mgf step, two-case
Chernoff optimization, and final parameter choice. With
`alpha=2/(p+2)`, `gamma=p/(p+2)`, `y=gamma z/4`, the Gaussian exponent is
exactly `c2`. With `A=4(p+2)/p`, all polynomial contributions satisfy
`A^p+2A^(p-1)+2A^p <= 4A^p=c1`.

| Evidence | Result |
| --- | --- |
| Universal symbolic reconstruction | PASS |
| Displayed constants | Recovered |
| Independent finite-product checker | Must exit 0 |
| Gaussian-only mutation | Must FAIL on one-large-jump control |
| Verdict | **VERIFIED** |

The fixed command is `uv run --locked python -m reproduction.run_all`.
Raw certificate:
[`proof_certificate.json`](../../../.openresearch/artifacts/claim-1/proof_certificate.json).
Primary verifier: [`claim1.py`](../../../reproduction/claim1.py).
Independent checker: [`claim1_checker.py`](../../../reproduction/claim1_checker.py).

The exhaustive finite grids are diagnostics only. The full theorem is supported
by the independent symbolic derivation, not extrapolated from enumeration.

