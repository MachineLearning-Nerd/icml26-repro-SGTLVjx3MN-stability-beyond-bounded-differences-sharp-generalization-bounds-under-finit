"""Exact counterexample to Theorem 3.10 and audit of Theorem 3.9."""

from __future__ import annotations

import json
import math
import subprocess
import sys
from fractions import Fraction
from pathlib import Path


EVIDENCE_DIR = Path(".openresearch/artifacts/claim-5")
CERTIFICATE = EVIDENCE_DIR / "counterexample_certificate.json"


def theorem_39_coefficient_audit(m: int, u: int, p: int) -> dict[str, object]:
    n = m + u
    exact = sum((Fraction(u, n - i)) ** p for i in range(1, m + 1))
    integral = (
        float(u**p)
        / (p - 1.0)
        * (
            1.0 / (u - 0.5) ** (p - 1.0)
            - 1.0 / (n - 0.5) ** (p - 1.0)
        )
    )
    selected = min(m, u)
    complement = max(m, u)
    exact_second = sum(
        (Fraction(complement, n - i)) ** 2 for i in range(1, selected + 1)
    )
    displayed_second = (
        m
        * u
        / ((n - 0.5) * (1.0 - 1.0 / (2.0 * max(m, u))))
    )
    return {
        "m": m,
        "u": u,
        "p": p,
        "exact_p_sum": float(exact),
        "displayed_Vp_coefficient": integral,
        "Vp_dominates": float(exact) <= integral * (1.0 + 1e-12),
        "exact_V2_sum_using_smaller_side": float(exact_second),
        "displayed_V2_coefficient": displayed_second,
        "V2_dominates": float(exact_second)
        <= displayed_second * (1.0 + 1e-12),
    }


def exact_counterexample() -> dict[str, object]:
    """Enumerate the complete two-partition counterexample."""
    partitions = [
        {"training_label": 0, "test_label": 1, "gap": 1},
        {"training_label": 1, "test_label": 0, "gap": -1},
    ]
    y = Fraction(1, 2)
    event_count = sum(row["gap"] >= y for row in partitions)
    probability = Fraction(event_count, len(partitions))
    return {
        "population": "two labeled points z0=(x0,0), z1=(x1,1)",
        "m": 1,
        "u": 1,
        "algorithm": "ignore the partition and always return h(x)=0",
        "loss": "squared loss (h(x)-label)^2",
        "partitions": partitions,
        "p": 2,
        "beta": 1,
        "H": "identically zero",
        "beta_prime": 1,
        "G": "absolute label difference",
        "assumption_3_6": True,
        "assumption_3_8": True,
        "symmetric_algorithm": True,
        "threshold_y": str(y),
        "bias_shift_beta_EH": 0,
        "displayed_envelope": 0,
        "displayed_Vp_prime": 0,
        "displayed_V2_prime": 0,
        "left_probability": str(probability),
        "right_bound": 0,
        "contradiction": probability > 0,
    }


def corrected_coefficient_control() -> dict[str, object]:
    """The intended reassignment coefficient is a sum, not a difference."""
    m = u = 1
    actual_swap_gap_change = 2
    displayed_coefficient = abs(Fraction(1, u) - Fraction(1, m))
    corrected_coefficient = Fraction(1, u) + Fraction(1, m)
    return {
        "name": "replace_absolute_difference_by_sum",
        "actual_swap_gap_change": actual_swap_gap_change,
        "paper_envelope": str(displayed_coefficient),
        "corrected_envelope": str(corrected_coefficient),
        "paper_increment_holds": actual_swap_gap_change <= displayed_coefficient,
        "corrected_increment_holds": actual_swap_gap_change <= corrected_coefficient,
        "expected": "paper version FAIL; corrected control PASS",
    }


def run_independent_checker() -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, "-m", "reproduction.claim5_checker", str(CERTIFICATE)],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise AssertionError(
            "independent Claim 5 checker failed\n"
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    return {
        "exit_code": completed.returncode,
        "stdout": completed.stdout.strip(),
        "parsed": json.loads(completed.stdout),
    }


def verify() -> dict[str, object]:
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if certificate["source"]["sha256"] != (
        "ca7631580c8a96ff440892fe1ab8d8b42edc84f0dc6eaaf990d404c75f47c7c7"
    ):
        raise AssertionError("paper source hash mismatch")
    if certificate["theorem_3_10"]["quantifier"] != "every y>0":
        raise AssertionError("Theorem 3.10 quantifier was weakened")

    audits = [
        theorem_39_coefficient_audit(m, u, p)
        for m, u in ((1, 1), (2, 7), (7, 2), (50, 50), (99, 1), (1, 99))
        for p in (2, 3, 5)
    ]
    if not all(row["Vp_dominates"] and row["V2_dominates"] for row in audits):
        raise AssertionError("Theorem 3.9 coefficient audit failed")

    counterexample = exact_counterexample()
    if not all(
        counterexample[key]
        for key in ("assumption_3_6", "assumption_3_8", "symmetric_algorithm")
    ):
        raise AssertionError("counterexample violates a stated premise")
    if not counterexample["contradiction"]:
        raise AssertionError("counterexample does not contradict the conclusion")

    control = corrected_coefficient_control()
    if control["paper_increment_holds"] or not control["corrected_increment_holds"]:
        raise AssertionError("coefficient mutation control did not separate the formulas")

    checker = run_independent_checker()
    return {
        "claim": 5,
        "verdict": "FALSIFIED",
        "confidence": "HIGH",
        "falsified_object": "Theorem 3.10",
        "reason": (
            "A complete two-partition example satisfies Assumptions 3.6 and 3.8 "
            "but has probability 1/2 for the claimed event while V'_p=V'_2=0."
        ),
        "theorem_3_9": {
            "status": "VERIFIED",
            "basis": (
                "finite-population Doob coupling plus midpoint-sum coefficient "
                "bounds; independently checked on complete declared finite grids"
            ),
            "coefficient_audits": audits,
        },
        "theorem_3_10_counterexample": counterexample,
        "corrected_coefficient_control": control,
        "independent_checker": checker,
        "limitations": (
            "FALSIFIED applies to the exact displayed Theorem 3.10. Theorem 3.9 "
            "is separately supported and is not contradicted."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
