# Claim 3 method

The primary route is an independently reconstructed symbolic derivation using
the reverse triangle inequality and the exact Gaussian second moment. The
executable verifier checks the certificate hash and exact rational witnesses.
A separately implemented checker imports no code from the primary verifier.

Two controls must fail:

1. Replacing `beta=1/m` by `1/(2m)` violates the inequality at
   `z_i=m,z_i'=0`.
2. Replacing Gaussian data by Cauchy data violates the finite-`L2` assumption;
   the difference is Cauchy with scale two and has divergent second moment.

The verifier raises or exits nonzero if the positive certificate fails, if the
independent checker fails, or if either negative control unexpectedly passes.

