"""Four-route audit of Theorem 2.6 (the p in (1,2) regime)."""

from __future__ import annotations

import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path


EVIDENCE_DIR = Path(".openresearch/artifacts/claim-2")
CONTRACT = EVIDENCE_DIR / "claim_contract.json"


def proof_step_control() -> dict[str, object]:
    """Exact counterexample to equation (61)'s tail-comparison proof step.

    This does not falsify Theorem 2.6; its second term can still cover the
    example. It establishes that the displayed proof route is incomplete.
    """
    q = Fraction(3, 5)
    # X~Bernoulli(q), f(X)=X. D=f-Ef has magnitudes 2/5 and 3/5.
    threshold = Fraction(3, 10)
    d_tail = Fraction(1)
    # Minimal H(X,X')=|X-X'| is nonzero with probability 2q(1-q)=12/25.
    h_tail = 2 * q * (1 - q)
    return {
        "paper_step": "Equation (61): P(|P_i(g)|>y) <= P(|H_i(X_i,X_i')|>y)",
        "distribution": "X~Bernoulli(3/5), f(X)=X, H(X,X')=|X-X'|",
        "threshold": str(threshold),
        "projection_tail": str(d_tail),
        "envelope_tail": str(h_tail),
        "step_holds": d_tail <= h_tail,
        "interpretation": "proof-step counterexample only; not a theorem counterexample",
    }


def run_search() -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, "-m", "reproduction.claim2_search", str(CONTRACT)],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise AssertionError(
            "Claim 2 independent search failed\n"
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    return {
        "exit_code": completed.returncode,
        "stdout": completed.stdout.strip(),
        "parsed": json.loads(completed.stdout),
    }


def verify() -> dict[str, object]:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    if contract["source"]["sha256"] != (
        "ca7631580c8a96ff440892fe1ab8d8b42edc84f0dc6eaaf990d404c75f47c7c7"
    ):
        raise AssertionError("paper source hash mismatch")
    if contract["quantifiers"]["p"] != "1<p<2" or contract["quantifiers"]["Q"] != "Q>=1":
        raise AssertionError("Claim 2 quantifiers were weakened")

    route1 = proof_step_control()
    if route1["step_holds"]:
        raise AssertionError("proof-gap control unexpectedly passed equation (61)")
    search = run_search()
    parsed = search["parsed"]
    if parsed["finite_grid"]["violations"] != 0:
        raise AssertionError("finite-grid search found a theorem counterexample")
    if parsed["falsification_search"]["valid_counterexamples"] != 0:
        raise AssertionError("randomized search found a theorem counterexample")
    if parsed["falsification_search"]["assumption_violations"] != 0:
        raise AssertionError("search admitted an invalid envelope")

    routes = [
        {
            "route": 1,
            "method": "line-by-line displayed-proof audit",
            "result": "UNRESOLVED",
            "detail": route1,
        },
        {
            "route": 2,
            "method": "complete enumeration on declared finite product grids",
            "result": "CORROBORATED_NOT_PROVED",
            "detail": parsed["finite_grid"],
        },
        {
            "route": 3,
            "method": "independent von Bahr-Esseen fallback reconstruction",
            "result": "WEAKER_BOUND_ONLY",
            "detail": {
                "bound": "P(|f-Ef|>z) <= C_p * sum_i E|H_i|^p/z^p",
                "limitation": "does not recover the exact Q-dependent tail form",
            },
        },
        {
            "route": 4,
            "method": "dedicated assumption-satisfying falsification search",
            "result": "NO_COUNTEREXAMPLE_FOUND",
            "detail": parsed["falsification_search"],
        },
    ]
    return {
        "claim": 2,
        "verdict": "BLOCKED",
        "confidence": "LOW",
        "reason": (
            "The exact universal Q-dependent theorem was not independently derived; "
            "the paper's displayed equation (61) is false in general. Exhaustive and "
            "randomized searches found no valid theorem counterexample, so FALSIFIED "
            "would also be unjustified."
        ),
        "routes": routes,
        "independent_search": search,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
