# Evaluator-blind pre-publication review

The review used a fresh directory assembled from the exact judged Space
revision plus only the candidate text overlay. It began at `README.md`,
`logbook.json`, and `pages/index.md`. No OpenResearch logs, experiment
descriptions, unpublished branches, or repository-only knowledge supplied
missing evidence.

## First pass

Files opened from the canonical traversal:

- `README.md`, `logbook.json`, `pages/index.md`;
- `pages/current-claim-{1,2,3,4,5,6}/page.md`;
- `pages/methods-current/page.md`, `pages/release-report/page.md`,
  `pages/red-team/page.md`, and
  `pages/historical-rejected-baseline/page.md`;
- every evidence-bundle link and both executable-code links on each current
  claim page;
- `pyproject.toml`, `uv.lock`, and `reproduction/run_all.py`.

The reviewer located the exact source statement and quantifiers, assumptions,
inline numerical or symbolic result, raw JSON, primary verifier, independent
checker, intended control, limitations, fixed command, locked environment,
claim Git SHA, seed where stochastic, CPU allocation, and runtime for every
claim. The traversal found all six current verdicts and did not mistake a
historical proxy for the current verifier.

Conclusions not yet verifiable in pass one:

1. the red-team record itself still said `pending`;
2. the exact text upload allowlist and candidate SHA-256 manifest did not yet
   exist;
3. the old/new subset proof and secret scan were not yet linked.

These were release-engineering gaps, not scientific evidence gaps.

## Fixes

The candidate adds this completed review, a machine-readable visibility
matrix, old/new subset proof, secret-scan result, exact upload allowlist,
candidate SHA-256 manifest, and release-gate record. The canonical red-team
page links this record, and the release report links the release evidence.

## Mandatory repeated pass

`POST_FIX_REVIEW_STATUS=PASS`

A second fresh assembly began again from the judged revision plus the
candidate text overlay. The reviewer repeated the canonical traversal without
repository context. Results:

- all 16 navigation entries resolved;
- all 74 reachable Markdown files had zero broken local links;
- every one of the six claim rows exposed every required evidence category;
- the upload allowlist exactly matched all 187 candidate text files;
- all 185 non-self-referential manifest entries matched;
- all 17 judged paths remained present;
- the five historical evidence pages at their original paths and eight
  archived historical text files were byte-identical;
- the strict credential scan matched zero files.

Files opened were the same canonical and linked files listed in the first
pass, plus `evidence/release/visibility-matrix.csv`,
`old-new-subset.json`, `secret-scan.txt`, `text-upload-allowlist.txt`,
`candidate-manifest.sha256`, and `release-gates.json`.

Conclusions not verifiable after fixes: none. Claim 2 is still scientifically
BLOCKED, visibly and intentionally; that is a claim verdict, not an evidence
discovery failure.
