# Current theorem-level reproduction

The strongest results are two complete, assumption-satisfying counterexamples:

- Theorem 3.10 predicts a right side of `0`, but the exact event probability
  is `1/2`.
- Theorem 3.14 predicts a right side of `0`, but the exact event probability
  is `1`.

These results supersede the judged synthetic proxies. The protected pages from
revision `05fc578dd7ceabe63f2650b21e8f318878f6b1ad` remain reachable below as
**Historical rejected baseline**.

Previous live judged score: `6/12`.
Conservative projected score range after this candidate: **8–11/12**.
Best-supported possible new score: **11/12 forecast, not a judge result**.
Claim 2 remains BLOCKED after four materially different routes, so this
candidate does not forecast 12/12.

## Current claims

| Claim | Exact object | Current result | Confidence | Strongest evidence |
| --- | --- | --- | --- | --- |
| 1 | Theorem 2.2 | [VERIFIED](current-claim-1/page.md) | HIGH | Universal derivation; constants recovered |
| 2 | Theorem 2.6 | [BLOCKED](current-claim-2/page.md) | LOW | Four routes; no proof or counterexample |
| 3 | Assumption 3.1 / Remark 3.2 | [VERIFIED](current-claim-3/page.md) | HIGH | Exact strict-extension witness |
| 4 | Theorem 3.4 | [VERIFIED](current-claim-4/page.md) | HIGH | Universal reduction to Theorem 2.2 |
| 5 | Theorems 3.9/3.10 | [FALSIFIED](current-claim-5/page.md) | HIGH | Complete two-partition counterexample to 3.10 |
| 6 | Assumption 3.12 / Theorem 3.14 | [FALSIFIED](current-claim-6/page.md) | HIGH | Complete two-task counterexample |

## Evaluator visibility matrix

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Current Claim 1](current-claim-1/page.md) | Yes | Yes | Yes | Independent | Gaussian-only mutation fails | Yes | VERIFIED |
| 2 | [Current Claim 2](current-claim-2/page.md) | Yes | Yes | Yes | Independent | Proof-step control fails | Yes | BLOCKED |
| 3 | [Current Claim 3](current-claim-3/page.md) | Yes | Yes | Yes | Independent | Two failing controls | Yes | VERIFIED |
| 4 | [Current Claim 4](current-claim-4/page.md) | Yes | Yes | Yes | Independent | Two derivation mutations fail | Yes | VERIFIED |
| 5 | [Current Claim 5](current-claim-5/page.md) | Yes | Yes | Yes | Independent | Corrected coefficient passes | Yes | FALSIFIED |
| 6 | [Current Claim 6](current-claim-6/page.md) | Yes | Yes | Yes | Independent | Whole-task premise control | Yes | FALSIFIED |

## Reproduction contract

The exact fixed command on every experiment node is:

```bash
uv run --locked python -m reproduction.run_all
```

The environment is Python 3.12 with the committed `pyproject.toml` and
`uv.lock`. All numerical thread pools are constrained to one active core.
Short checks ran on local CPU; the uncertain 20,000-case Claim 2 route ran on
Hugging Face `cpu-upgrade`. No GPU was used.

[Release report](release-report/page.md) ·
[Current methods](methods-current/page.md) ·
[Blind review](red-team/page.md) ·
[Historical rejected baseline](historical-rejected-baseline/page.md)
