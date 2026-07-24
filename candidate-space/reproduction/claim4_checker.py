"""Independent checker for the Theorem 3.4 proof certificate."""

from __future__ import annotations

import itertools
import json
import math
import sys
from fractions import Fraction
from pathlib import Path


def theorem_bound(
    y: float, p: float, m: int, beta: float, beta_prime: float, ehp: float, egp: float, eh2: float, eg2: float
) -> float:
    base_c1 = 4.0 * (4.0 * (p + 2.0) / p) ** p
    base_c2 = 1.0 / (2.0 * (p + 2.0) ** 2 * math.e**p)
    c1 = base_c1 * 2.0 ** (2.0 * p - 1.0)
    c2 = base_c2 / 8.0
    polynomial = c1 * (
        m * beta**p * ehp + beta_prime**p * egp / m ** (p - 1.0)
    ) / y**p
    variance = m * beta**2 * eh2 + beta_prime**2 * eg2 / m
    gaussian = 0.0 if variance == 0.0 else 2.0 * math.exp(-c2 * y**2 / variance)
    return polynomial + gaussian


def bernoulli_probability(sample: tuple[int, ...], q: Fraction) -> Fraction:
    ones = sum(sample)
    return q**ones * (1 - q) ** (len(sample) - ones)


def exact_binary_diagnostic(m: int, q: Fraction, p: int) -> int:
    domain = list(itertools.product((0, 1), repeat=m))
    probabilities = [bernoulli_probability(sample, q) for sample in domain]
    population_risks: list[Fraction] = []
    empirical_risks: list[Fraction] = []
    loo_risks: list[Fraction] = []

    for sample in domain:
        mean = Fraction(sum(sample), m)
        population_risks.append(q * abs(mean - 1) + (1 - q) * abs(mean))
        empirical_risks.append(
            sum((abs(mean - z) for z in sample), start=Fraction(0)) / m
        )
        loo_terms: list[Fraction] = []
        for i, z in enumerate(sample):
            if m == 1:
                # Define the empty-sample algorithm as zero for this diagnostic.
                loo_mean = Fraction(0)
            else:
                loo_mean = Fraction(sum(sample) - z, m - 1)
            loo_terms.append(abs(loo_mean - z))
        loo_risks.append(sum(loo_terms, start=Fraction(0)) / m)

    expected_population = sum(
        (prob * risk for prob, risk in zip(probabilities, population_risks, strict=True)),
        start=Fraction(0),
    )
    if m == 1:
        previous_expected_population = q
    else:
        smaller_domain = list(itertools.product((0, 1), repeat=m - 1))
        previous_expected_population = sum(
            (
                bernoulli_probability(sample, q)
                * (q * abs(Fraction(sum(sample), m - 1) - 1)
                   + (1 - q) * abs(Fraction(sum(sample), m - 1)))
                for sample in smaller_domain
            ),
            start=Fraction(0),
        )

    beta = 1.0 / m
    beta_prime = 1.0
    pair_difference = float(2 * q * (1 - q))
    bias_shift = beta * pair_difference
    checks = 0

    for risks, shift in (
        (empirical_risks, bias_shift),
        (
            loo_risks,
            float(abs(expected_population - previous_expected_population)),
        ),
    ):
        deviations = [
            abs(float(population - risk))
            for population, risk in zip(population_risks, risks, strict=True)
        ]
        thresholds = sorted(
            {
                max(1e-8, deviation - shift)
                for deviation in deviations
                if deviation > shift + 1e-10
            }
        )
        for y in thresholds:
            tail = sum(
                float(prob)
                for prob, deviation in zip(probabilities, deviations, strict=True)
                if deviation > y + shift + 1e-12
            )
            bound = theorem_bound(
                y,
                float(p),
                m,
                beta,
                beta_prime,
                pair_difference,
                pair_difference,
                pair_difference,
                pair_difference,
            )
            if tail > bound + 1e-10:
                raise AssertionError(
                    f"finite diagnostic violation: {m=}, {q=}, {p=}, {y=}, {tail=}, {bound=}"
                )
            checks += 1
    return checks


def independent_check(path: Path) -> dict[str, object]:
    certificate = json.loads(path.read_text(encoding="utf-8"))
    assert certificate["theorem"]["first_target"] == "population risk minus empirical risk"
    assert certificate["theorem"]["second_target"] == "population risk minus leave-one-out risk"
    assert certificate["assumptions"] == ["Assumption 3.1", "Assumption 3.3"]
    assert certificate["derived_constants"]["c1_equals_c3"] == "C1(p)*2^(2p-1)"
    assert certificate["derived_constants"]["c2_equals_c4"] == "C2(p)/8"

    cases = 0
    tail_thresholds = 0
    for m in range(1, 9):
        for q in (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)):
            for p in (2, 3, 4):
                cases += 1
                tail_thresholds += exact_binary_diagnostic(m, q, p)

    return {
        "status": "PASS",
        "complete_declared_domain": "all binary samples for m=1..8, q in {1/4,1/2,3/4}, p in {2,3,4}",
        "cases": cases,
        "tail_thresholds_checked": tail_thresholds,
        "scope": "diagnostic only; universal support is the symbolic reduction",
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python -m reproduction.claim4_checker PROOF_CERTIFICATE")
    print(json.dumps(independent_check(Path(sys.argv[1])), indent=2, sort_keys=True))
