# Claim 4 source audit

The exact source is Theorem 3.4 at
`https://ar5iv.labs.arxiv.org/html/2606.06855#S3.Thmtheorem4`, retrieved
2026-07-24. The source SHA-256 is
`ca7631580c8a96ff440892fe1ab8d8b42edc84f0dc6eaaf990d404c75f47c7c7`.

The theorem quantifies over every `m>=1`, every `y>0`, and every iid learning
problem satisfying Assumptions 3.1 and 3.3 with a common finite moment
`p>=2`. It has two conclusions: a tail bound for `|R-R_emp|` shifted by
`beta E H`, and a tail bound for
`|R-R_loo-(R_m-R_(m-1))|`. In each conclusion the polynomial numerator is
`m beta^p E|H|^p + (beta')^p E|G|^p/m^(p-1)` and the Gaussian variance scale is
`m beta^2 E|H|^2 + (beta')^2 E|G|^2/m`. Its constants may depend only on `p`.

The proof certificate makes those constants explicit. If `C1(p),C2(p)` are
Theorem 2.2's constants, then both conclusions hold with
`c1=c3=C1(p)2^(2p-1)` and `c2=c4=C2(p)/8`. These are not asserted to be the
smallest constants.

For the empirical target, changing coordinate `i` changes population risk by
at most `beta H_i` and empirical risk by at most
`beta H_i+beta'G_i/m`. For the leave-one-out target, the corresponding
envelope is no larger. The stability coupling gives
`|E(R-R_emp)|<=beta E H`; exchangeability gives the exact leave-one-out mean
`R_m-R_(m-1)`. Theorem 2.2 then applies to the centered targets.
