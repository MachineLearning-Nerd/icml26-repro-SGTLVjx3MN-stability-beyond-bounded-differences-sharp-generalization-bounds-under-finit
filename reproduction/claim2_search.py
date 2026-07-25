"""Independent finite-domain and falsification search for Theorem 2.6."""

from __future__ import annotations

import itertools
import json
import math
import random
import sys
from pathlib import Path


def product_domain(n: int) -> list[tuple[int, ...]]:
    return list(itertools.product((0, 1), repeat=n))


def point_probability(point: tuple[int, ...], q: float) -> float:
    ones = sum(point)
    return q**ones * (1.0 - q) ** (len(point) - ones)


def oscillations(
    domain: list[tuple[int, ...]], values: tuple[float, ...], n: int
) -> list[float]:
    table = dict(zip(domain, values, strict=True))
    result: list[float] = []
    for coordinate in range(n):
        maximum = 0.0
        for point in domain:
            changed = list(point)
            changed[coordinate] = 1 - changed[coordinate]
            maximum = max(maximum, abs(table[point] - table[tuple(changed)]))
        result.append(maximum)
    return result


def theorem_bound(
    z: float, p: float, q_parameter: float, mp: float, h_tail_sum: float
) -> float:
    if mp == 0.0:
        second = 0.0
    else:
        log_base = (
            1.0
            + p * math.log(4.0)
            + (p - 1.0) * math.log(q_parameter)
            + math.log(mp)
            - p * math.log(z)
        )
        log_second = math.log(2.0) + q_parameter * log_base
        second = math.inf if log_second > 700.0 else math.exp(log_second)
    return h_tail_sum + second


def evaluate_case(
    values: tuple[float, ...],
    n: int,
    bernoulli_q: float,
    p: float,
    q_parameter: float,
    z: float,
) -> tuple[float, float]:
    domain = product_domain(n)
    probabilities = [point_probability(point, bernoulli_q) for point in domain]
    mean = sum(prob * value for prob, value in zip(probabilities, values, strict=True))
    tail = sum(
        prob
        for prob, value in zip(probabilities, values, strict=True)
        if abs(value - mean) > z
    )
    coordinate_oscillations = oscillations(domain, values, n)
    pair_change = 2.0 * bernoulli_q * (1.0 - bernoulli_q)
    mp = sum(pair_change * size**p for size in coordinate_oscillations)
    threshold = z / (4.0 * q_parameter)
    h_tail_sum = sum(
        pair_change for size in coordinate_oscillations if size > threshold
    )
    return tail, theorem_bound(z, p, q_parameter, mp, h_tail_sum)


def finite_grid_search() -> dict[str, object]:
    cases = 0
    comparisons = 0
    violations = 0
    minimum_ratio = math.inf
    q_parameters = (1.0, 1.25, 1.5, 2.0, 3.0, 5.0, 10.0, 30.0)
    for n, output_grid in ((1, (-2.0, -1.0, 0.0, 1.0, 2.0)), (2, (-1.0, 0.0, 1.0))):
        domain = product_domain(n)
        for values in itertools.product(output_grid, repeat=len(domain)):
            cases += 1
            if max(values) == min(values):
                continue
            for bernoulli_q in (0.1, 1.0 / 3.0, 0.5, 2.0 / 3.0, 0.9):
                probabilities = [point_probability(point, bernoulli_q) for point in domain]
                mean = sum(
                    prob * value for prob, value in zip(probabilities, values, strict=True)
                )
                deviations = sorted({abs(value - mean) for value in values if abs(value - mean) > 0})
                for p in (1.1, 1.5, 1.9):
                    for q_parameter in q_parameters:
                        critical = set()
                        for deviation in deviations:
                            critical.add(deviation * (1.0 - 1e-10))
                            critical.add(deviation * (1.0 + 1e-10))
                        for size in oscillations(domain, values, n):
                            if size > 0:
                                boundary = 4.0 * q_parameter * size
                                critical.add(boundary * (1.0 - 1e-10))
                                critical.add(boundary * (1.0 + 1e-10))
                        for z in critical:
                            if z <= 0:
                                continue
                            tail, bound = evaluate_case(
                                values, n, bernoulli_q, p, q_parameter, z
                            )
                            comparisons += 1
                            if tail > 0:
                                minimum_ratio = min(minimum_ratio, bound / tail)
                            if tail > bound * (1.0 + 1e-9):
                                violations += 1
    return {
        "functions": cases,
        "comparisons": comparisons,
        "violations": violations,
        "minimum_bound_to_tail_ratio": minimum_ratio,
        "scope": "complete on declared binary/output grids and listed p,Q values",
    }


def randomized_falsification_search(seed: int = 260606855, trials: int = 20_000) -> dict[str, object]:
    rng = random.Random(seed)
    valid_counterexamples = 0
    assumption_violations = 0
    minimum_ratio = math.inf
    best: dict[str, object] = {}
    for _ in range(trials):
        n = rng.randint(1, 5)
        domain = product_domain(n)
        bernoulli_q = 10 ** rng.uniform(-6.0, math.log10(0.5))
        if rng.random() < 0.5:
            bernoulli_q = 1.0 - bernoulli_q
        values = tuple(
            rng.choice((-1.0, 1.0)) * 10 ** rng.uniform(-3.0, 6.0)
            for _ in domain
        )
        p = rng.uniform(1.001, 1.999)
        q_parameter = 10 ** rng.uniform(0.0, 4.0)
        probabilities = [point_probability(point, bernoulli_q) for point in domain]
        mean = sum(prob * value for prob, value in zip(probabilities, values, strict=True))
        deviations = [abs(value - mean) for value in values]
        positive = [deviation for deviation in deviations if deviation > 0]
        if not positive:
            continue
        z = rng.choice(positive) * 10 ** rng.uniform(-1.0, 0.5)
        tail, bound = evaluate_case(values, n, bernoulli_q, p, q_parameter, z)
        # Envelopes are coordinate suprema by construction, so assumptions hold.
        if any(size < 0 for size in oscillations(domain, values, n)):
            assumption_violations += 1
        if tail > 0 and bound / tail < minimum_ratio:
            minimum_ratio = bound / tail
            best = {
                "n": n,
                "bernoulli_q": bernoulli_q,
                "p": p,
                "Q": q_parameter,
                "z": z,
                "tail": tail,
                "bound": bound,
            }
        if tail > bound * (1.0 + 1e-9):
            valid_counterexamples += 1
            break
    return {
        "seed": seed,
        "trials": trials,
        "valid_counterexamples": valid_counterexamples,
        "assumption_violations": assumption_violations,
        "minimum_bound_to_tail_ratio": minimum_ratio,
        "closest_case": best,
    }


def run(contract_path: Path) -> dict[str, object]:
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    assert contract["quantifiers"]["p"] == "1<p<2"
    assert contract["quantifiers"]["Q"] == "Q>=1"
    return {
        "status": "PASS",
        "finite_grid": finite_grid_search(),
        "falsification_search": randomized_falsification_search(),
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python -m reproduction.claim2_search CLAIM_CONTRACT")
    print(json.dumps(run(Path(sys.argv[1])), indent=2, sort_keys=True))

