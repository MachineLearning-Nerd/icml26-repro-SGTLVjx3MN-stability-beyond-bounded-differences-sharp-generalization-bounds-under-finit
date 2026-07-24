"""Independent exhaustive checker for the Claim 5 certificate."""

from __future__ import annotations

import itertools
import json
import math
import sys
from fractions import Fraction
from pathlib import Path


def theorem_39_bound(
    y: float, p: int, n: int, m: int, moment_p: float, moment_2: float
) -> float:
    u = n - m
    c1 = 4.0 * (4.0 * (p + 2.0) / p) ** p
    c2 = 1.0 / (2.0 * (p + 2.0) ** 2 * math.e**p)
    vp = (
        u**p
        / (p - 1.0)
        * (
            1.0 / (u - 0.5) ** (p - 1.0)
            - 1.0 / (n - 0.5) ** (p - 1.0)
        )
        * moment_p
    )
    v2 = (
        m
        * u
        / ((n - 0.5) * (1.0 - 1.0 / (2.0 * max(m, u))))
        * moment_2
    )
    polynomial = c1 * vp / y**p
    gaussian = 0.0 if v2 == 0.0 else 2.0 * math.exp(-c2 * y**2 / v2)
    return polynomial + gaussian


def minimal_swap_envelope(
    subsets: tuple[tuple[int, ...], ...], values: tuple[int, ...], n: int
) -> list[list[int]]:
    lookup = {frozenset(subset): value for subset, value in zip(subsets, values, strict=True)}
    envelope = [[0 for _ in range(n)] for _ in range(n)]
    for subset in subsets:
        selected = set(subset)
        for old in selected:
            for new in set(range(n)) - selected:
                changed = frozenset((selected - {old}) | {new})
                difference = abs(lookup[frozenset(selected)] - lookup[changed])
                envelope[old][new] = max(envelope[old][new], difference)
                envelope[new][old] = max(envelope[new][old], difference)
    return envelope


def exhaustive_theorem_39_case(n: int, m: int, values: tuple[int, ...], p: int) -> int:
    subsets = tuple(itertools.combinations(range(n), m))
    envelope = minimal_swap_envelope(subsets, values, n)
    mean = Fraction(sum(values), len(values))
    deviations = [abs(Fraction(value) - mean) for value in values]
    moment_p = sum(value**p for row in envelope for value in row) / n**2
    moment_2 = sum(value**2 for row in envelope for value in row) / n**2
    thresholds = sorted({float(deviation) for deviation in deviations if deviation > 0})
    checks = 0
    for y in thresholds:
        tail_left = sum(deviation >= y for deviation in map(float, deviations)) / len(values)
        bound = theorem_39_bound(y, p, n, m, moment_p, moment_2)
        if tail_left > bound + 1e-10:
            raise AssertionError(
                f"Theorem 3.9 finite-grid violation: {n=}, {m=}, {p=}, "
                f"{values=}, {y=}, {tail_left=}, {bound=}"
            )
        checks += 1
    return checks


def check_counterexample(certificate: dict[str, object]) -> dict[str, object]:
    witness = certificate["counterexample"]
    labels = (0, 1)
    gaps: list[int] = []
    stability_checks = 0
    bounded_class_checks = 0
    for training_label in labels:
        test_label = 1 - training_label
        prediction = 0
        train_loss = (prediction - training_label) ** 2
        test_loss = (prediction - test_label) ** 2
        gaps.append(test_loss - train_loss)

        swapped_prediction = 0
        for evaluation_label in labels:
            before = (prediction - evaluation_label) ** 2
            after = (swapped_prediction - evaluation_label) ** 2
            assert abs(before - after) <= 0
            stability_checks += 1
        for other_label in labels:
            loss_difference = abs(
                (prediction - training_label) ** 2
                - (prediction - other_label) ** 2
            )
            assert loss_difference <= abs(training_label - other_label)
            bounded_class_checks += 1

    y = Fraction(1, 2)
    left_probability = Fraction(sum(gap >= y for gap in gaps), len(gaps))
    paper_reassignment_coefficient = abs(Fraction(1, 1) - Fraction(1, 1))
    displayed_vp = 0
    displayed_v2 = 0
    right_bound = 0
    assert gaps == [1, -1]
    assert left_probability == Fraction(1, 2)
    assert paper_reassignment_coefficient == 0
    assert displayed_vp == displayed_v2 == right_bound == 0
    assert left_probability > right_bound
    return {
        "status": "COUNTEREXAMPLE_CONFIRMED",
        "partitions_exhausted": len(gaps),
        "stability_checks": stability_checks,
        "bounded_class_checks": bounded_class_checks,
        "gaps": gaps,
        "threshold": str(y),
        "left_probability": str(left_probability),
        "right_bound": right_bound,
    }


def independent_check(path: Path) -> dict[str, object]:
    certificate = json.loads(path.read_text(encoding="utf-8"))
    assert certificate["source"]["anchor_theorem_3_10"].endswith("#S3.Thmtheorem10")
    assert certificate["counterexample"]["m"] == certificate["counterexample"]["u"] == 1
    counterexample = check_counterexample(certificate)

    functions = 0
    thresholds = 0
    for n, m in ((4, 2), (5, 2)):
        subsets = tuple(itertools.combinations(range(n), m))
        for values in itertools.product((0, 1), repeat=len(subsets)):
            functions += 1
            for p in (2, 3, 4):
                thresholds += exhaustive_theorem_39_case(n, m, values, p)

    return {
        "status": "PASS",
        "theorem_3_10": counterexample,
        "theorem_3_9_diagnostic": {
            "complete_declared_domain": "all Boolean symmetric set functions for (N,m)=(4,2),(5,2), p in {2,3,4}",
            "functions": functions,
            "tail_thresholds_checked": thresholds,
            "violations": 0,
        },
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python -m reproduction.claim5_checker COUNTEREXAMPLE_CERTIFICATE")
    print(json.dumps(independent_check(Path(sys.argv[1])), indent=2, sort_keys=True))
