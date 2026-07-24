# Current verification — Claim 5

> Supersedes the without-replacement variance proxy page, which remains
> preserved as **Historical rejected baseline**.

## Exact result: Theorem 3.10 is falsified

[Theorem 3.10](https://ar5iv.labs.arxiv.org/html/2606.06855#S3.Thmtheorem10)
uses the swap envelope
`2 beta H + |1/u-1/m| beta' G`. Its quantifier is every `y>0`.
The source SHA-256 is
`ca7631580c8a96ff440892fe1ab8d8b42edc84f0dc6eaaf990d404c75f47c7c7`.

Consider the fixed population of two labeled points with labels zero and one,
`m=u=1`, the symmetric algorithm that always returns `h(x)=0`, and squared
loss. The algorithm is perfectly stable, so Assumption 3.6 holds with
`beta=1,H=0`. The singleton hypothesis class satisfies Assumption 3.8 with
`beta'=1,G(z,z')=|label(z)-label(z')|`, whose moments are finite for every
`p`.

There are exactly two partitions:

| Training label | Test label | `R-Rhat` |
| ---: | ---: | ---: |
| 0 | 1 | 1 |
| 1 | 0 | -1 |

At `p=2,y=1/2`, the left probability is `1/2`. Because `m=u`,
`|1/u-1/m|=0`; because `H=0`, both displayed `V'_p` and `V'_2` are zero.
The right side is therefore zero. The exact claimed inequality becomes
`1/2 <= 0`.

| Evidence | Result |
| --- | --- |
| Every partition enumerated | 2 of 2 |
| Assumption 3.6 | PASS pointwise |
| Assumption 3.8 | PASS pointwise |
| Left probability | `1/2` |
| Displayed right bound | `0` |
| Independent reconstruction | PASS: 2/2 partitions |
| Replace difference by `1/u+1/m` | Corrected control PASS |
| Verdict | **FALSIFIED** |

The error is the reassignment coefficient: moving losses between test and
train changes their difference with coefficient `1/u+1/m`, not
`|1/u-1/m|`.

## Theorem 3.9

[Theorem 3.9](https://ar5iv.labs.arxiv.org/html/2606.06855#S3.Thmtheorem9)
is separately supported by a finite-population Doob coupling, exact
midpoint/telescoping coefficient bounds, and a complete declared finite-grid
diagnostic over 1,088 functions and 5,688 tail thresholds with zero
violations. It is not contradicted by this example.

The fixed command is `uv run --locked python -m reproduction.run_all`.
Run `7c209bd3-e2e3-4242-bf78-66647277d855` completed locally in
approximately 10 orchestrated seconds at Git SHA
`95b65f4c47b378582b9346c6575f252fbb64e1cc`.

Evidence bundle:
[`contract`](../../evidence/claim-5/claim_contract.json) ·
[`source audit`](../../evidence/claim-5/source_audit.md) ·
[`method`](../../evidence/claim-5/method.md) ·
[`raw results`](../../evidence/claim-5/raw_results.json) ·
[`counterexample`](../../evidence/claim-5/counterexample_certificate.json) ·
[`checker output`](../../evidence/claim-5/checker_output.txt) ·
[`control output`](../../evidence/claim-5/negative_control_output.txt) ·
[`limitations`](../../evidence/claim-5/limitations.md) ·
[`EVAL`](../../evidence/claim-5/EVAL.md).
Code:
[`primary verifier`](../../reproduction/claim5.py) ·
[`independent checker`](../../reproduction/claim5_checker.py).
