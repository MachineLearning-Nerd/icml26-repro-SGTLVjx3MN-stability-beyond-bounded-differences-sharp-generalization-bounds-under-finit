# Claim 1 source audit

Theorem 2.2 is at
`https://ar5iv.labs.arxiv.org/html/2606.06855#S2.Thmtheorem2` in the
retrieved source with SHA-256
`ca7631580c8a96ff440892fe1ab8d8b42edc84f0dc6eaaf990d404c75f47c7c7`.

The quantifiers are universal: independent random variables in a measurable
space; measurable `f`; valid pointwise replace-one envelopes `H_i`; one fixed
finite moment `p>=2`; and every deviation `z>0`. The exact conclusion is the
sum of a `z^-p` term and a sub-Gaussian term, with

`c1=4(4(p+2)/p)^p`, `c2=[2(p+2)^2 e^p]^-1`.

The proof reconstruction starts from the Doob differences
`D_i=E[f|F_i]-E[f|F_(i-1)]`. Independence of the resampled coordinate gives
`D_i=E[f-f^(i)|F_i]`; conditional Jensen and the pointwise envelope give the
required second and `p`-th moment controls. After truncating at `y`, centering
the truncated increments, and applying the bounded-increment mgf lemma, the
Chernoff optimization splits into moderate- and large-deviation cases.

Set `alpha=2/(p+2)`, `gamma=p/(p+2)`, and `y=gamma z/4`. Then
`alpha+gamma=1`. The Gaussian exponent becomes

`alpha^2/(8e^p)=1/[2(p+2)^2 e^p]=c2`.

Writing `A=4(p+2)/p`, the three polynomial contributions are bounded by
`A^p + 2A^(p-1) + 2A^p <= 4A^p=c1`, since `p>=2`.
This recovers the displayed constants for the full stated domain.

The literature search also returned arXiv:2512.10012, a primary work on
Fuk–Nagaev inequalities for heavy-tailed martingales. It independently
confirms that Gaussian-plus-large-jump structure is the relevant classical
phenomenon; it is context, not a premise substituted for the paper's proof.

