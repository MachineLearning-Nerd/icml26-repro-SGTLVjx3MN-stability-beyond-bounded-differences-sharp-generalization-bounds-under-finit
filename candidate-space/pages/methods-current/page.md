# Current methods

The paper's six items are mathematical claims, so each contract preserves the
exact source assumptions, domain, and quantifiers. Universal theorems are
accepted only through a reconstructed symbolic implication or an exact
counterexample—not through Monte Carlo extrapolation.

Each claim bundle contains:

- `claim_contract.json` and a source audit tied to paper SHA-256
  `ca7631580c8a96ff440892fe1ab8d8b42edc84f0dc6eaaf990d404c75f47c7c7`;
- executable primary and independent checkers;
- raw JSON or proof/counterexample certificates;
- intended-to-fail controls;
- limitations, exact command, Git SHA, CPU allocation, and runtime.

The cumulative command exits nonzero if a checker or required control does not
behave as specified:

```bash
uv run --locked python -m reproduction.run_all
```

Claim 2 used four routes because confidence remained LOW: proof audit,
complete declared finite enumeration, a weaker independent derivation, and a
dedicated assumption-valid falsification search. It remains BLOCKED.

The complete environment is in [`pyproject.toml`](../../pyproject.toml) and
[`uv.lock`](../../uv.lock). The cumulative entrypoint is
[`reproduction/run_all.py`](../../reproduction/run_all.py).
