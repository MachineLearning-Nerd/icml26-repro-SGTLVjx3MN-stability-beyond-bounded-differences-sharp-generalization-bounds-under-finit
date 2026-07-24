"""Independent finite-product and algebra checker for the Claim 1 certificate."""

from __future__ import annotations

import itertools
import json
import math
import sys
from pathlib import Path


def theorem_bound(z: float, p: float, mp: float, m2: float) -> float:
    scale = 4.0 * (p + 2.0) / p
    c1 = 4.0 * scale**p
    c2 = 1.0 / (2.0 * (p + 2.0) ** 2 * math.e**p)
    polynomial = c1 * mp / z**p
    gaussian = 0.0 if m2 == 0.0 else 2.0 * math.exp(-c2 * z**2 / m2)
    return polynomial + gaussian


def probability_of_point(point: tuple[int, ...], q: float) -> float:
    ones = sum(point)
    return q**ones * (1.0 - q) ** (len(point) - ones)


def coordinate_oscillations(
    domain: list[tuple[int, ...]], values: tuple[int, ...], n: int
) -> list[float]:
    lookup = dict(zip(domain, values, strict=True))
    oscillations: list[float] = []
    for coordinate in range(n):
        maximum = 0.0
        for point in domain:
            changed = list(point)
            changed[coordinate] = 1 - changed[coordinate]
            maximum = max(maximum, abs(lookup[point] - lookup[tuple(changed)]))
        oscillations.append(maximum)
    return oscillations


def check_function(values: tuple[int, ...], n: int, q: float, p: float) -> int:
    domain = list(itertools.product((0, 1), repeat=n))
    probabilities = [probability_of_point(point, q) for point in domain]
    mean = sum(prob * value for prob, value in zip(probabilities, values, strict=True))
    deviations = [abs(value - mean) for value in values]
    oscillations = coordinate_oscillations(domain, values, n)
    pair_change_probability = 2.0 * q * (1.0 - q)
    mp = sum(pair_change_probability * oscillation**p for oscillation in oscillations)
    m2 = sum(pair_change_probability * oscillation**2 for oscillation in oscillations)

    thresholds = sorted({deviation for deviation in deviations if deviation > 1e-14})
    checks = 0
    for threshold in thresholds:
        # The left limit is the worst point in each constant-tail interval.
        tail_left = sum(
            prob
            for prob, deviation in zip(probabilities, deviations, strict=True)
            if deviation + 1e-14 >= threshold
        )
        bound = theorem_bound(threshold, p, mp, m2)
        if tail_left > bound + 1e-10:
            raise AssertionError(
                f"finite-product violation: {n=}, {q=}, {p=}, {values=}, "
                f"{threshold=}, {tail_left=}, {bound=}"
            )
        checks += 1
    return checks


def independent_check(path: Path) -> dict[str, object]:
    certificate = json.loads(path.read_text(encoding="utf-8"))
    assert certificate["theorem"]["p_domain"] == "p>=2"
    assert certificate["theorem"]["z_domain"] == "z>0"
    assert certificate["constants"]["c1"] == "4*(4*(p+2)/p)^p"
    assert certificate["constants"]["c2"] == "1/(2*(p+2)^2*e^p)"

    functions_checked = 0
    thresholds_checked = 0
    for n, output_grid in ((1, (-2, -1, 0, 1, 2)), (2, (-1, 0, 1))):
        domain_size = 2**n
        for values in itertools.product(output_grid, repeat=domain_size):
            functions_checked += 1
            for q in (1.0 / 3.0, 0.5, 2.0 / 3.0):
                for p in (2.0, 3.0, 4.0):
                    thresholds_checked += check_function(values, n, q, p)

    return {
        "status": "PASS",
        "functions_checked": functions_checked,
        "tail_thresholds_checked": thresholds_checked,
        "scope": "all functions on the declared finite grids; diagnostic only",
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python -m reproduction.claim1_checker PROOF_CERTIFICATE")
    print(json.dumps(independent_check(Path(sys.argv[1])), indent=2, sort_keys=True))

