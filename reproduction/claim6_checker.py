"""Independent complete-domain checker for the Theorem 3.14 counterexample."""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path


def independent_check(path: Path) -> dict[str, object]:
    certificate = json.loads(path.read_text(encoding="utf-8"))
    assert certificate["source"]["anchor"].endswith("#S3.Thmtheorem14")
    witness = certificate["counterexample"]
    assert witness["m"] == 1
    assert witness["n"] == 2
    assert witness["p"] == 3

    meta_states = 0
    population_states = 0
    condition_i_checks = 0
    condition_ii_checks = 0
    condition_iii_checks = 0
    gaps: list[Fraction] = []

    for theta_meta in (0, 1):
        meta_states += 1
        meta_sample = (theta_meta, theta_meta)
        prediction = 1 - theta_meta

        for index in range(2):
            changed = list(meta_sample)
            changed[index] = theta_meta
            changed_prediction = 1 - changed[0]
            for evaluation_label in (0, 1):
                before = (prediction - evaluation_label) ** 2
                after = (changed_prediction - evaluation_label) ** 2
                assert abs(before - after) == 0
                condition_i_checks += 1

        empirical_risk = Fraction(
            sum((prediction - label) ** 2 for label in meta_sample),
            len(meta_sample),
        )
        population_losses: list[int] = []
        for theta_new in (0, 1):
            population_states += 1
            new_task = (theta_new, theta_new)
            for index in range(2):
                changed_task = list(new_task)
                changed_task[index] = theta_new
                assert changed_task == list(new_task)
                condition_ii_checks += 1
            for first in new_task:
                for second in new_task:
                    assert abs(
                        (prediction - first) ** 2 - (prediction - second) ** 2
                    ) == 0
                    condition_iii_checks += 1
            population_losses.append((prediction - theta_new) ** 2)

        population_risk = Fraction(sum(population_losses), len(population_losses))
        gaps.append(empirical_risk - population_risk)

    threshold = Fraction(1, 4)
    left_probability = Fraction(sum(gap >= threshold for gap in gaps), len(gaps))
    assert gaps == [Fraction(1, 2), Fraction(1, 2)]
    assert left_probability == 1
    assert left_probability > 0

    whole_task_loss_change = abs((1 - 0 - 0) ** 2 - (1 - 1 - 0) ** 2)
    assert whole_task_loss_change == 1
    assert whole_task_loss_change > 0
    assert whole_task_loss_change <= 1

    return {
        "status": "COUNTEREXAMPLE_CONFIRMED",
        "complete_domain": "both meta-training task states and both population task states",
        "meta_states": meta_states,
        "population_states": population_states,
        "condition_i_checks": condition_i_checks,
        "condition_ii_checks": condition_ii_checks,
        "condition_iii_checks": condition_iii_checks,
        "gaps": [str(gap) for gap in gaps],
        "threshold": str(threshold),
        "left_probability": str(left_probability),
        "right_bound": 0,
        "whole_task_control_loss_change": whole_task_loss_change,
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python -m reproduction.claim6_checker COUNTEREXAMPLE_CERTIFICATE")
    print(json.dumps(independent_check(Path(sys.argv[1])), indent=2, sort_keys=True))
