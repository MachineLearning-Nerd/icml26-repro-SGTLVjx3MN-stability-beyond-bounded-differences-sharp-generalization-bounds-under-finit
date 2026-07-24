# Claim 5 method

The primary result is a proof-by-counterexample, not a Monte Carlo run. The
complete stated finite domain contains exactly two partitions, both of which
are enumerated with rational arithmetic. The verifier checks Assumptions 3.6
and 3.8 pointwise, symmetry, finite moments, the event probability, both
displayed variance proxies, and the strict contradiction.

An independent module reconstructs the witness without importing the primary
verifier. It also completely enumerates all Boolean symmetric set functions
on the declared `(N,m)=(4,2)` and `(5,2)` grids for Theorem 3.9.

The control replaces the paper's `|1/u-1/m|` reassignment coefficient by
`1/u+1/m`. On the counterexample swap, the displayed envelope is zero and
fails to cover the actual increment two; the corrected envelope is two and
passes exactly.
