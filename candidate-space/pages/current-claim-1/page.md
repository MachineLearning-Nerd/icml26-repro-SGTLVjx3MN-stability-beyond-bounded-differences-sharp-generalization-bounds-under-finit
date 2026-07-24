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
| Independent finite-product checker | PASS: 106 functions, 1,854 thresholds |
| Gaussian-only mutation | FAIL as intended: actual `1e-8`, mutated bound `0` |
| Verdict | **VERIFIED** |

The fixed command is `uv run --locked python -m reproduction.run_all`.
Run `b1931020-333d-491b-9e08-2568893659a4` used local CPU, exposed 8
logical CPUs with numerical pools fixed to one active core, and completed in
approximately 10 orchestrated seconds at Git SHA
`b1cd30ca708bc532460da6fc62af0e13d5bad8bf`.

Evidence bundle:
[`contract`](../../evidence/claim-1/claim_contract.json) ·
[`source audit`](../../evidence/claim-1/source_audit.md) ·
[`method`](../../evidence/claim-1/method.md) ·
[`raw results`](../../evidence/claim-1/raw_results.json) ·
[`proof certificate`](../../evidence/claim-1/proof_certificate.json) ·
[`checker output`](../../evidence/claim-1/checker_output.txt) ·
[`control output`](../../evidence/claim-1/negative_control_output.txt) ·
[`limitations`](../../evidence/claim-1/limitations.md) ·
[`EVAL`](../../evidence/claim-1/EVAL.md).
Code:
[`primary verifier`](../../reproduction/claim1.py) ·
[`independent checker`](../../reproduction/claim1_checker.py).

The exhaustive finite grids are diagnostics only. The full theorem is supported
by the independent symbolic derivation, not extrapolated from enumeration.
