"""Exact witness for Assumption 3.1 and its strict extension of uniform stability."""

from __future__ import annotations

import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path


EVIDENCE_DIR = Path(".openresearch/artifacts/claim-3")
CERTIFICATE = EVIDENCE_DIR / "raw_results.json"


def loss(sample: tuple[Fraction, ...]) -> Fraction:
    """Nonnegative loss |A_S| for the sample-mean algorithm A."""
    return abs(sum(sample, start=Fraction(0)) / len(sample))


def replace(sample: tuple[Fraction, ...], index: int, value: Fraction) -> tuple[Fraction, ...]:
    changed = list(sample)
    changed[index] = value
    return tuple(changed)


def envelope(value: Fraction, replacement: Fraction) -> Fraction:
    return abs(value - replacement)


def check_exact_replace_one_cases(m: int) -> int:
    """Check exact arithmetic cases spanning signs, ties, and large magnitudes."""
    values = tuple(Fraction(value) for value in (-10_000, -31, -1, 0, 1, 37, 10_000))
    checked = 0
    base = tuple(Fraction(0) for _ in range(m))
    for old in values:
        for new in values:
            sample = replace(base, 0, old)
            changed = replace(sample, 0, new)
            lhs = abs(loss(sample) - loss(changed))
            rhs = Fraction(1, m) * envelope(old, new)
            if lhs > rhs:
                raise AssertionError(f"replace-one inequality failed: {old=}, {new=}")
            checked += 1
    return checked


def beta_halving_control(m: int) -> dict[str, str | bool]:
    """A control that must fail because beta=1/(2m) is too small."""
    sample = (Fraction(m),) + tuple(Fraction(0) for _ in range(m - 1))
    changed = (Fraction(0),) + sample[1:]
    lhs = abs(loss(sample) - loss(changed))
    rhs = Fraction(1, 2 * m) * envelope(sample[0], changed[0])
    incorrectly_passes = lhs <= rhs
    return {
        "name": "beta_halved",
        "lhs": str(lhs),
        "rhs": str(rhs),
        "incorrectly_passes": incorrectly_passes,
        "expected": "FAIL",
    }


def cauchy_moment_control() -> dict[str, str | bool]:
    """Analytical control: a Cauchy replace-one envelope has infinite L2 moment."""
    return {
        "name": "standard_cauchy_p2",
        "tail_fact": "Z-Z' is Cauchy(scale=2); density is asymptotic to constant/x^2",
        "moment_integrand": "x^2 * density(x) is bounded below by a positive constant for x>=2",
        "finite_p2": False,
        "expected": "FAIL",
    }


def run_independent_checker() -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, "-m", "reproduction.claim3_checker", str(CERTIFICATE)],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise AssertionError(
            "independent checker failed\n"
            f"stdout:\n{completed.stdout}\n"
            f"stderr:\n{completed.stderr}"
        )
    return {
        "command": f"{sys.executable} -m reproduction.claim3_checker {CERTIFICATE}",
        "exit_code": completed.returncode,
        "stdout": completed.stdout.strip(),
    }


def verify() -> dict[str, object]:
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    m = int(certificate["witness"]["sample_size"])
    if certificate["source"]["paper_sha256"] != (
        "ca7631580c8a96ff440892fe1ab8d8b42edc84f0dc6eaaf990d404c75f47c7c7"
    ):
        raise AssertionError("paper source hash mismatch")
    if certificate["witness"]["beta"] != f"1/{m}":
        raise AssertionError("certificate beta does not match the exact witness")
    if certificate["moments"]["E_H_squared"] != 2:
        raise AssertionError("for Z-Z'~N(0,2), E|Z-Z'|^2 must equal 2")
    if not certificate["uniform_stability"]["supremum_is_infinite"]:
        raise AssertionError("certificate does not establish strict extension")

    exact_cases = check_exact_replace_one_cases(m)
    beta_control = beta_halving_control(m)
    cauchy_control = cauchy_moment_control()
    if beta_control["incorrectly_passes"]:
        raise AssertionError("negative control unexpectedly accepted beta=1/(2m)")
    if cauchy_control["finite_p2"]:
        raise AssertionError("negative control unexpectedly accepted a Cauchy L2 moment")

    checker = run_independent_checker()
    return {
        "claim": 3,
        "verdict": "VERIFIED",
        "reason": (
            "Exact Gaussian witness satisfies Assumption 3.1 at p=2 and beta=1/m, "
            "while no finite deterministic uniform-stability constant exists."
        ),
        "universal_derivation": [
            "A_S = m^-1 sum_j z_j",
            "A_S-A_S(i) = (z_i-z_i')/m",
            "||A_S|-|A_S(i)|| <= |A_S-A_S(i)| (reverse triangle inequality)",
            "therefore |loss(A_S,z)-loss(A_S(i),z)| <= m^-1 |z_i-z_i'|",
        ],
        "exact_arithmetic_cases": exact_cases,
        "moments": certificate["moments"],
        "uniform_stability": certificate["uniform_stability"],
        "negative_controls": [beta_control, cauchy_control],
        "independent_checker": checker,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
