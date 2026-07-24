# Claim 2 source audit

Theorem 2.6 is anchored at
`https://ar5iv.labs.arxiv.org/html/2606.06855#S2.Thmtheorem6` in the source
with SHA-256
`ca7631580c8a96ff440892fe1ab8d8b42edc84f0dc6eaaf990d404c75f47c7c7`.
It quantifies over every `1<p<2`, every `Q>=1`, every `z>0`, independent
coordinates, measurable `f`, and valid pointwise replace-one envelopes.

The displayed proof's equation (61) asserts

`P(|D_i|>y) <= P(|H_i(X_i,X_i')|>y)`.

This implication is not furnished by conditional Jensen and is false in
general even for the minimal valid envelope. Let `X~Bernoulli(3/5)`,
`f(X)=X`, and `H(X,X')=|X-X'|`. At `y=3/10`,
`P(|f-Ef|>y)=1`, while `P(H>y)=12/25`. This is a counterexample to the proof
step, not to Theorem 2.6: the theorem's second term is still present.

The primary comparison source arXiv:2512.10012 develops modern martingale
Fuk–Nagaev inequalities, but its heavy-tailed McDiarmid corollary assumes a
higher conditional moment `q>2`; it therefore does not independently certify
the exact lower-moment `1<p<2`, all-`Q` statement here.

