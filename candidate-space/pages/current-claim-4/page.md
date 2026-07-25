# Current verification — Claim 4

> Supersedes the regularized-versus-unregularized proxy page, which remains
> preserved as **Historical rejected baseline**.

## Exact theorem

[Theorem 3.4](https://ar5iv.labs.arxiv.org/html/2606.06855#S3.Thmtheorem4)
quantifies over every `m>=1`, every `y>0`, and every iid learning problem
satisfying Assumptions 3.1 and 3.3 for a common `p>=2`. It gives one shifted
tail bound for `|R-R_emp|` and one centered tail bound for `|R-R_loo|`.
The source SHA-256 is
`ca7631580c8a96ff440892fe1ab8d8b42edc84f0dc6eaaf990d404c75f47c7c7`.

## Universal certificate

Changing coordinate `i` gives the common envelope
`2 beta H_i + beta' G_i/m` for both centered targets. For `q` in `{2,p}`,

`sum_i E|2 beta H_i + beta'G_i/m|^q`

is at most

`2^(2q-1)m beta^q E|H|^q + 2^(q-1)(beta')^q E|G|^q/m^(q-1)`.

Applying Theorem 2.2 proves both displayed forms with explicit admissible
constants `c1=c3=C1(p)2^(2p-1)` and `c2=c4=C2(p)/8`. The stability coupling
also gives the required `|E(R-R_emp)|<=beta E H`, while exchangeability gives
`E(R-R_loo)=R_m-R_(m-1)`.

| Evidence | Result |
| --- | --- |
| Universal six-step symbolic reduction | PASS |
| Explicit constants depend only on `p` | PASS |
| Independent complete declared binary diagnostic | PASS: 72 cases, 465 tail thresholds |
| Omit population-risk increment | FAIL as intended: `2<=1` is false |
| Delete stability-bias shift | FAIL as intended: exact bias is `1/2` |
| Verdict | **VERIFIED** |

The fixed command is `uv run --locked python -m reproduction.run_all`.
Run `e1126a83-08d5-4584-943c-8bb028bea9ca` completed locally in
approximately 10 orchestrated seconds at Git SHA
`a8be89f5e9dd072e349c21bb435ff3fe965dd04f`.

Evidence bundle:
[`contract`](../../evidence/claim-4/claim_contract.json) ·
[`source audit`](../../evidence/claim-4/source_audit.md) ·
[`method`](../../evidence/claim-4/method.md) ·
[`raw results`](../../evidence/claim-4/raw_results.json) ·
[`proof certificate`](../../evidence/claim-4/proof_certificate.json) ·
[`checker output`](../../evidence/claim-4/checker_output.txt) ·
[`control output`](../../evidence/claim-4/negative_control_output.txt) ·
[`limitations`](../../evidence/claim-4/limitations.md) ·
[`EVAL`](../../evidence/claim-4/EVAL.md).
Code:
[`primary verifier`](../../reproduction/claim4.py) ·
[`independent checker`](../../reproduction/claim4_checker.py).

The finite diagnostic is not extrapolated into a universal conclusion; the
universal conclusion comes from the symbolic reduction.
