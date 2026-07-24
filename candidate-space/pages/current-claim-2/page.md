# Current audit — Claim 2

## Exact statement

[Theorem 2.6](https://ar5iv.labs.arxiv.org/html/2606.06855#S2.Thmtheorem6)
quantifies over all independent inputs, valid replace-one envelopes,
`1<p<2`, `Q>=1`, and `z>0`. Its exact bound is

`sum_i P(|H_i|>z/(4Q)) + 2(e 4^p Q^(p-1) M_p/z^p)^Q`.

Source SHA-256:
`ca7631580c8a96ff440892fe1ab8d8b42edc84f0dc6eaaf990d404c75f47c7c7`.

## Four materially different routes

| Route | Method | Outcome |
| --- | --- | --- |
| 1 | Line-by-line displayed-proof audit | Equation (61) unresolved |
| 2 | Complete declared finite grids | Corroboration only |
| 3 | Von Bahr–Esseen fallback derivation | Weaker polynomial bound only |
| 4 | Dedicated assumption-satisfying falsification search | No contradiction unless printed otherwise |

For route 1, `X~Bernoulli(3/5)`, `f(X)=X`, and the minimal valid
`H(X,X')=|X-X'|` give, at `y=3/10`,
`P(|f-Ef|>y)=1` but `P(H>y)=12/25`. Thus the proof's equation (61) is not
valid as stated. The theorem's second term may still cover the example, so this
is not a theorem counterexample.

The fixed command is `uv run --locked python -m reproduction.run_all`.
Contract: [`claim_contract.json`](../../../.openresearch/artifacts/claim-2/claim_contract.json).
Search code: [`claim2_search.py`](../../../reproduction/claim2_search.py).

## Verdict

**BLOCKED.** The exact universal result has neither an independent derivation
nor a valid assumption-satisfying counterexample. The historical Monte Carlo
page remains reachable as **Historical rejected baseline**, but is not current
verification.

