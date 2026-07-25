# Release report and score forecast

- Previous live judged score: `6/12`
- Conservative projected score range after the proposed change: **8–11/12**
- Best-supported possible new score: **11/12 forecast, not a judge result**

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | ---: | ---: | --- | --- | --- |
| 1 | 1 | 2 | HIGH | VERIFIED | Universal derivation recovers both regimes and exact constants; residual risk is evaluator acceptance of a checked symbolic certificate rather than a proof assistant. |
| 2 | 1 | 1 | LOW | BLOCKED | Four distinct routes are complete; equation (61) fails, but neither the universal theorem nor a valid counterexample is established. |
| 3 | 1 | 2 | HIGH | VERIFIED | Exact Gaussian witness has finite `L2` stability and infinite deterministic uniform-stability diameter. |
| 4 | 1 | 2 | HIGH | VERIFIED | Both exact bounds reduce mechanically to Theorem 2.2 with explicit constants; residual risk is proof-certificate review. |
| 5 | 1 | 2 | HIGH | FALSIFIED | Complete assumption-satisfying counterexample gives event probability `1/2` and displayed bound `0`. |
| 6 | 1 | 2 | HIGH | FALSIFIED | Complete two-task counterexample satisfies all three clauses and gives event probability `1` and displayed bound `0`. |

Current total score remains **6/12** until the live judge evaluates a new
revision. The conservative projected total is **8–11/12**; the
best-supported possible total is **11/12**.

The protected Hugging Face Head and Judge Head are both
`05fc578dd7ceabe63f2650b21e8f318878f6b1ad`. The winning cumulative
release-audit branch is `orx/final-evaluator-visible-release-audit` at
`09b7046a1fe2ecde1d10d6e013df3bbe8ebd59da`; run
`ceb74baa-d007-4cd7-b0f0-f154c09e2713` completed in 15 seconds with every
claim and release gate passing.

All six claim assessments changed from the previous judge's TOY description:
Claims 1, 3, and 4 now have exact VERIFIED certificates; Claims 5 and 6 have
exact FALSIFIED certificates; Claim 2 is explicitly BLOCKED. Claim 2 remains
BLOCKED because its exact universal `Q`-dependent theorem has neither an
independent derivation nor an assumption-satisfying counterexample after four
routes.

The exact publication action, after every gate passes, is a text-only upload
to the existing Space `DineshAI/SGTLVjx3MN`, preserving its binary assets and
historical pages. No second Space will be created. The published text will
then be mirrored to GitHub `main`, whose use is presentation-only rather than
an experiment run.

## Compute and command

Every node uses:

```bash
uv run --locked python -m reproduction.run_all
```

Local runs exposed 8 logical CPUs but constrained numerical pools to one
active core, completing in about 10 orchestrated seconds. Claim 2 ran on
Hugging Face `cpu-upgrade` in 26 seconds; 64 logical CPUs were visible and
the code still constrained pools to one active core. No GPU was used. The
backend logs did not expose a billed amount, so cost is recorded as unknown
rather than guessed.

## Experiment tree

`Historical rejected baseline → Claim 3 → Claim 1 → Claim 2 → Claim 4 →
Claim 5 → Claim 6 → evaluator-visible release candidate → final
evaluator-visible release audit`.

The first release candidate passed every claim check but correctly stopped
when its audit detected that Git ignore rules had omitted the hidden evidence
mirror. The winning release-audit child force-includes that mirror and reran
the identical fixed command successfully. The current
`orx/publication-ready-release-manifest` child adds this immutable provenance
and changes no claim logic.
The winning scientific branch is
`orx/claim-6-exact-meta-learning-counterexample` at Git SHA
`7012a238962fd3e18a1f2f67a4f78ebbf69fc7c1`. The exact release branch SHA
is reported after its immutable cumulative run and is also recoverable from
the published Space revision.

## Release evidence

[Visibility matrix](../index.md#evaluator-visibility-matrix) ·
[Blind review](../red-team/page.md) ·
[Historical rejected baseline](../historical-rejected-baseline/page.md) ·
[Machine-readable visibility matrix](../../evidence/release/visibility-matrix.csv) ·
[Old/new subset proof](../../evidence/release/old-new-subset.json) ·
[Secret scan](../../evidence/release/secret-scan.txt) ·
[Release gates](../../evidence/release/release-gates.json) ·
[Exact upload allowlist](../../evidence/release/text-upload-allowlist.txt) ·
[Candidate SHA-256 manifest](../../evidence/release/candidate-manifest.sha256) ·
[Commands executed](../../evidence/release/commands-executed.txt)
