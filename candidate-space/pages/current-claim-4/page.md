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
| Independent complete declared binary diagnostic | Executed by fixed command |
| Omit population-risk increment | Must FAIL |
| Delete stability-bias shift | Must FAIL |
| Verdict | **VERIFIED** |

The fixed command is `uv run --locked python -m reproduction.run_all`.
Certificate:
[`proof_certificate.json`](../../../.openresearch/artifacts/claim-4/proof_certificate.json).
Primary verifier: [`claim4.py`](../../../reproduction/claim4.py).
Independent checker: [`claim4_checker.py`](../../../reproduction/claim4_checker.py).

The finite diagnostic is not extrapolated into a universal conclusion; the
universal conclusion comes from the symbolic reduction.
