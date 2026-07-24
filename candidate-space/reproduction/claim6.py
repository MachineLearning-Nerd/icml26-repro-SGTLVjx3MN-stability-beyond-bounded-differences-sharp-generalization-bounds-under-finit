"""Exact counterexample to the meta-learning bound in Theorem 3.14."""

from __future__ import annotations

import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path


EVIDENCE_DIR = Path(".openresearch/artifacts/claim-6")
CERTIFICATE = EVIDENCE_DIR / "counterexample_certificate.json"


def exact_counterexample() -> dict[str, object]:
    """Enumerate both meta-training tasks and both independent test tasks."""
    rows: list[dict[str, int | str]] = []
    gaps: list[Fraction] = []
    for meta_theta in (0, 1):
        prediction = 1 - meta_theta
        empirical_loss = (prediction - meta_theta) ** 2
        population_losses = [
            (prediction - new_theta) ** 2 for new_theta in (0, 1)
        ]
        population_risk = Fraction(sum(population_losses), len(population_losses))
        gap = Fraction(empirical_loss) - population_risk
        gaps.append(gap)
        rows.append(
            {
                "meta_task_theta": meta_theta,
                "prediction": prediction,
                "empirical_meta_risk": empirical_loss,
                "population_meta_risk": str(population_risk),
                "gap": str(gap),
            }
        )

    y = Fraction(1, 4)
    event_probability = Fraction(sum(gap >= y for gap in gaps), len(gaps))
    return {
        "m": 1,
        "n": 2,
        "p": 3,
        "meta_distribution": "uniform over D0=point-mass at label 0 and D1=point-mass at label 1",
        "algorithm": (
            "read theta from the sole meta-training task; return a task learner "
            "that ignores its task data and predicts 1-theta"
        ),
        "loss": "squared loss",
        "states": rows,
        "assumption_3_12_i": True,
        "assumption_3_12_ii": True,
        "assumption_3_12_iii": True,
        "H": 0,
        "G": 0,
        "M": 0,
        "all_required_moments_finite": True,
        "threshold_y": str(y),
        "left_probability": str(event_probability),
        "bias_shift": 0,
        "displayed_polynomial_numerator": 0,
        "displayed_gaussian_variance": 0,
        "right_bound": 0,
        "contradiction": event_probability > 0,
    }


def whole_task_replacement_control() -> dict[str, object]:
    """Expose the proof's unassumed whole-task replacement."""
    loss_change_when_theta_flips = 1
    stated_h = 0
    corrected_whole_task_h = 1
    return {
        "name": "whole_task_replacement",
        "stated_neighbor_changes_task_distribution": False,
        "proof_neighbor_can_change_task_distribution": True,
        "loss_change_when_task_flips": loss_change_when_theta_flips,
        "stated_H_covers_proof_neighbor": loss_change_when_theta_flips <= stated_h,
        "corrected_task_level_H_covers_proof_neighbor": (
            loss_change_when_theta_flips <= corrected_whole_task_h
        ),
        "expected": "stated assumption FAIL; corrected whole-task control PASS",
    }


def run_independent_checker() -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, "-m", "reproduction.claim6_checker", str(CERTIFICATE)],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise AssertionError(
            "independent Claim 6 checker failed\n"
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
    if certificate["theorem_3_14"]["quantifier"] != "all y>0":
        raise AssertionError("Theorem 3.14 quantifier was weakened")

    counterexample = exact_counterexample()
    premises = (
        counterexample["assumption_3_12_i"],
        counterexample["assumption_3_12_ii"],
        counterexample["assumption_3_12_iii"],
        counterexample["all_required_moments_finite"],
    )
    if not all(premises):
        raise AssertionError("counterexample violates Assumption 3.12")
    if not counterexample["contradiction"]:
        raise AssertionError("counterexample does not contradict Theorem 3.14")

    control = whole_task_replacement_control()
    if control["stated_H_covers_proof_neighbor"]:
        raise AssertionError("stated within-task stability unexpectedly covers a whole task")
    if not control["corrected_task_level_H_covers_proof_neighbor"]:
        raise AssertionError("corrected whole-task stability control did not pass")

    checker = run_independent_checker()
    return {
        "claim": 6,
        "verdict": "FALSIFIED",
        "confidence": "HIGH",
        "falsified_object": "Theorem 3.14",
        "reason": (
            "All three stated stability envelopes vanish on point-mass tasks, "
            "yet meta-distribution variation creates a deterministic gap 1/2."
        ),
        "counterexample": counterexample,
        "proof_assumption_mismatch": {
            "assumption": "replace one within-task observation while D_j stays fixed",
            "proof_equation_104": "replace the entire task S_j by an iid task S'_j",
        },
        "negative_control": control,
        "independent_checker": checker,
        "limitations": (
            "The verdict concerns the exact universal theorem under the stated "
            "Assumption 3.12. A theorem with genuine whole-task meta-stability "
            "may remain valid."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
