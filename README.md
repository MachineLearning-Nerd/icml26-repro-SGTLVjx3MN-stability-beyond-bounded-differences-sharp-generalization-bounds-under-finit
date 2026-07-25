# Exact claim-by-claim reproduction of arXiv:2606.06855

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-SGTLVjx3MN-stability-beyond-bounded-differences-sharp-generalization-bounds-under-finit/blob/main/notebooks/stability_beyond_bounded.py)

This project tests the six judged claims of “Stability beyond Bounded
Differences: Sharp Generalization Bounds under Finite \(L_p\) Moments.”
The previous Space revision received **6/12**, with every item judged TOY.
The current cumulative evidence is theorem-level: Claims 1, 3, and 4 are
VERIFIED; Claims 5 and 6 are FALSIFIED by complete assumption-satisfying
counterexamples; Claim 2 remains BLOCKED after four distinct routes.

The strongest numerical contradictions are exact, not estimated:

| Paper claim | Paper conclusion at the witness | Observed exact result | Assessment |
| --- | --- | --- | --- |
| Theorem 3.10 | event probability `<= 0` | event probability `1/2` | FALSIFIED |
| Theorem 3.14 | event probability `<= 0` | event probability `1` | FALSIFIED |

The Claim 5 witness exhausts both partitions of a two-point population. The
Claim 6 witness exhausts both meta-training task states and both fresh-task
states. No dataset or tolerance is selected from the theorem formula.

Compute followed the agreed CPU-only policy. Short, one-core checks ran
locally in about 10 orchestrated seconds each. The uncertain Claim 2 search
ran on Hugging Face `cpu-upgrade` for 26 seconds; the allocation exposed 64
logical CPUs, but the code constrained numerical pools to one active core.
No GPU was used.

- [Illustrated technical report](reports/stability-beyond-bounded/report.md)
- [Self-contained marimo tutorial](notebooks/stability_beyond_bounded.py)
- [Evaluator-visible candidate](candidate-space/pages/index.md)

## Experiment log

Every formal experiment used the exact same command:
`uv run --locked python -m reproduction.run_all`.

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
| --- | --- | --- | --- | --- |
| `main` | Public README, report, notebook, and release surface | Not run as an experiment (publication surface) | Presentation-only | None |
| [`orx/historical-rejected-baseline`](https://github.com/MachineLearning-Nerd/icml26-repro-SGTLVjx3MN-stability-beyond-bounded-differences-sharp-generalization-bounds-under-finit/tree/orx/historical-rejected-baseline) | Freeze judged proxy baseline | `uv run --locked python -m reproduction.run_all` | Historical rejected baseline; TOY only | Local CPU, ~10s |
| [`orx/claim-3-strict-extension-certificate`](https://github.com/MachineLearning-Nerd/icml26-repro-SGTLVjx3MN-stability-beyond-bounded-differences-sharp-generalization-bounds-under-finit/tree/orx/claim-3-strict-extension-certificate) | Exact finite-\(L_2\), non-uniform witness | `uv run --locked python -m reproduction.run_all` | Claim 3 VERIFIED | Local CPU, ~10s |
| [`orx/claim-1-exact-nagaev-derivation`](https://github.com/MachineLearning-Nerd/icml26-repro-SGTLVjx3MN-stability-beyond-bounded-differences-sharp-generalization-bounds-under-finit/tree/orx/claim-1-exact-nagaev-derivation) | Reconstruct Theorem 2.2 and constants | `uv run --locked python -m reproduction.run_all` | Claim 1 VERIFIED | Local CPU, ~10s |
| [`orx/claim-2-four-route-audit`](https://github.com/MachineLearning-Nerd/icml26-repro-SGTLVjx3MN-stability-beyond-bounded-differences-sharp-generalization-bounds-under-finit/tree/orx/claim-2-four-route-audit) | Proof audit, enumeration, weaker derivation, falsification search | `uv run --locked python -m reproduction.run_all` | Claim 2 BLOCKED | HF `cpu-upgrade`, 26s |
| [`orx/claim-4-exact-generalization-certificate`](https://github.com/MachineLearning-Nerd/icml26-repro-SGTLVjx3MN-stability-beyond-bounded-differences-sharp-generalization-bounds-under-finit/tree/orx/claim-4-exact-generalization-certificate) | Reduce both Theorem 3.4 bounds | `uv run --locked python -m reproduction.run_all` | Claim 4 VERIFIED | Local CPU, ~10s |
| [`orx/claim-5-exact-without-replacement-certificate`](https://github.com/MachineLearning-Nerd/icml26-repro-SGTLVjx3MN-stability-beyond-bounded-differences-sharp-generalization-bounds-under-finit/tree/orx/claim-5-exact-without-replacement-certificate) | Audit Theorem 3.9; exact counterexample to 3.10 | `uv run --locked python -m reproduction.run_all` | Claim 5 FALSIFIED | Local CPU, ~10s |
| [`orx/claim-6-exact-meta-learning-counterexample`](https://github.com/MachineLearning-Nerd/icml26-repro-SGTLVjx3MN-stability-beyond-bounded-differences-sharp-generalization-bounds-under-finit/tree/orx/claim-6-exact-meta-learning-counterexample) | Exact counterexample to Theorem 3.14 | `uv run --locked python -m reproduction.run_all` | Claim 6 FALSIFIED | Local CPU, ~10s |
| [`orx/evaluator-visible-release-candidate`](https://github.com/MachineLearning-Nerd/icml26-repro-SGTLVjx3MN-stability-beyond-bounded-differences-sharp-generalization-bounds-under-finit/tree/orx/evaluator-visible-release-candidate) | Cumulative public artifact and regression suite | `uv run --locked python -m reproduction.run_all` | Claims passed; release gate caught an ignored hidden evidence mirror | Local CPU, ~20s |
| [`orx/final-evaluator-visible-release-audit`](https://github.com/MachineLearning-Nerd/icml26-repro-SGTLVjx3MN-stability-beyond-bounded-differences-sharp-generalization-bounds-under-finit/tree/orx/final-evaluator-visible-release-audit) | Force-include hidden mirror and rerun every gate | `uv run --locked python -m reproduction.run_all` | PASS: every claim and release gate | Local CPU, 15s |
| [`orx/publication-ready-release-manifest`](https://github.com/MachineLearning-Nerd/icml26-repro-SGTLVjx3MN-stability-beyond-bounded-differences-sharp-generalization-bounds-under-finit/tree/orx/publication-ready-release-manifest) | Record immutable winning run and exact publication manifest | `uv run --locked python -m reproduction.run_all` | Publication candidate inheriting the passed suite | Local CPU, estimated <5 min |

## Reproduce

Install `uv`, then run:

```bash
uv sync --locked
uv run --locked python -m reproduction.run_all
```

Every accepted verifier exits nonzero if its certificate, independent checker,
or required control fails. Claim 2 intentionally prints `BLOCKED`; it is not
converted into a pass.

## Historical rejected baseline

The experiment root preserves the toy-scale state judged **6/12**. Its six
checks remain labeled as proxies and are rerun only as historical regression
evidence. They do not verify the paper's universal theorems.
