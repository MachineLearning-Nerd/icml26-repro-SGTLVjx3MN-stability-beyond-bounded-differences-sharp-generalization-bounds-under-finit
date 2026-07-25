# Claim 5 source audit

The exact sources are Theorems 3.9 and 3.10 at
`https://ar5iv.labs.arxiv.org/html/2606.06855#S3.Thmtheorem9` and
`https://ar5iv.labs.arxiv.org/html/2606.06855#S3.Thmtheorem10`. The source was
retrieved 2026-07-24 and has SHA-256
`ca7631580c8a96ff440892fe1ab8d8b42edc84f0dc6eaaf990d404c75f47c7c7`.

Theorem 3.9 applies to every symmetric measurable function of a size-`m`
sample drawn uniformly without replacement from a population of size
`N=m+u`. Its Doob exposure coefficient is `u/(N-i)`. Summing its `p`-th
powers and applying the midpoint integral yields the displayed `V_p`; exposing
the smaller side of the partition and telescoping
`1/k^2 <= 1/(k^2-1/4)` yields the displayed `V_2`.

Theorem 3.10 applies Theorem 3.9 to
`phi(S)=R_test(h)-R_train(h)`. Its displayed swap envelope is

`2 beta H + |1/u-1/m| beta' G`.

That coefficient is false even when the algorithm itself is perfectly stable.
For a fixed hypothesis, swapping losses `a` and `b` between the two averages
changes the gap by `(1/u+1/m)|a-b|`, not
`|1/u-1/m||a-b|`.

The exact counterexample uses two labeled points, `m=u=1`, the constant
predictor zero, and squared loss. It exhausts both possible partitions. The
gap is respectively `1` and `-1`. Stability has `H=0`, the singleton
hypothesis class has finite envelope `G=|label-label'|`, and every premise is
satisfied at `p=2`. At `y=1/2`, the left probability is `1/2`, while the
displayed `V'_p` and `V'_2` are both zero and the right side is zero.
