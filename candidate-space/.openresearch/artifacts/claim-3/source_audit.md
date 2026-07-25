# Claim 3 source audit

Source: ar5iv HTML for arXiv:2606.06855, retrieved 2026-07-24 with the
explicit user agent recorded in the historical source metadata. SHA-256:
`ca7631580c8a96ff440892fe1ab8d8b42edc84f0dc6eaaf990d404c75f47c7c7`.

Assumption 3.1 is anchored at
`https://ar5iv.labs.arxiv.org/html/2606.06855#S3.Thmtheorem1`.
It quantifies over every replaced coordinate `i` and requires

`|ell(A_S,z)-ell(A_{S^i},z)| <= beta H(z_i,z_i')`

with `||H(Z,Z')||_p < infinity` for some fixed `p>=2`. Remark 3.2 says
bounded uniform stability is recovered by `H=1` and that the finite-moment
condition strictly extends those light-tailed regimes.

The exact claim contract therefore needs more than a finite empirical moment:
it needs an assumption-satisfying example that has no finite deterministic
uniform-stability diameter. The Gaussian sample-mean witness supplies this.

For arbitrary real samples, replacing coordinate `i` gives

`A_S-A_{S^i}=(z_i-z_i')/m`.

The reverse triangle inequality then yields

`||A_S|-|A_{S^i}|| <= |A_S-A_{S^i}| = |z_i-z_i'|/m`.

Thus `beta=1/m` and `H(z,z')=|z-z'|` satisfy the assumption pointwise.
For iid standard normals, `Z-Z'~N(0,2)`, hence `E H^2=2<infinity`.
Conversely, for every proposed finite uniform bound `B`, choose one changed
coordinate as `z_i=m(B+1)` and `z_i'=0`, with all others zero. The loss
increment is `B+1>B`; therefore its deterministic supremum is infinite.
