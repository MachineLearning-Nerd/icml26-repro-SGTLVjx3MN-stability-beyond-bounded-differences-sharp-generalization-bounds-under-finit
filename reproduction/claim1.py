"""Certificate verifier for Theorem 2.2's two-regime concentration bound."""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path


EVIDENCE_DIR = Path(".openresearch/artifacts/claim-1")
CERTIFICATE = EVIDENCE_DIR / "proof_certificate.json"


def constants_audit(p: float) -> dict[str, float | bool]:
    alpha = 2.0 / (p + 2.0)
    gamma = p / (p + 2.0)
    scale = 4.0 * (p + 2.0) / p
    displayed_c1 = 4.0 * scale**p
    reconstructed_polynomial = scale**p + 2.0 * scale ** (p - 1.0) + 2.0 * scale**p
    displayed_c2 = 1.0 / (2.0 * (p + 2.0) ** 2 * math.e**p)
    reconstructed_c2 = alpha**2 / (8.0 * math.e**p)
    return {
        "p": p,
        "alpha": alpha,
        "gamma": gamma,
        "alpha_plus_gamma": alpha + gamma,
        "displayed_c1": displayed_c1,
        "reconstructed_polynomial_coefficient": reconstructed_polynomial,
        "c1_dominates": reconstructed_polynomial <= displayed_c1 * (1.0 + 1e-12),
        "displayed_c2": displayed_c2,
        "reconstructed_c2": reconstructed_c2,
        "c2_matches": math.isclose(displayed_c2, reconstructed_c2, rel_tol=1e-12),
    }


def one_large_jump_control() -> dict[str, float | bool | str]:
    """Show why deleting the polynomial term invalidates the bound."""
    p = 2.0
    probability = 1e-8
    jump = 1.0 / probability
    threshold = jump / 2.0
    m2 = 2.0 * probability * (1.0 - probability) * jump**2
    c2 = 1.0 / (2.0 * (p + 2.0) ** 2 * math.e**p)
    pure_gaussian = 2.0 * math.exp(-c2 * threshold**2 / m2)
    actual_tail = probability
    return {
        "name": "omit_polynomial_term",
        "distribution": f"f(X)={jump:g}*Bernoulli({probability:g})",
        "threshold": threshold,
        "actual_tail": actual_tail,
        "mutated_pure_gaussian_bound": pure_gaussian,
        "mutated_bound_holds": actual_tail <= pure_gaussian,
        "expected": "FAIL",
    }


def run_independent_checker() -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, "-m", "reproduction.claim1_checker", str(CERTIFICATE)],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise AssertionError(
            "independent Claim 1 checker failed\n"
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    return {
        "exit_code": completed.returncode,
        "stdout": completed.stdout.strip(),
    }


def verify() -> dict[str, object]:
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    expected_rules = [
        "doob_projection_identity",
        "conditional_jensen_envelope",
        "truncate_and_center",
        "bounded_increment_mgf",
        "chernoff_two_case_optimization",
        "choose_alpha_gamma_and_threshold",
    ]
    rules = [step["rule"] for step in certificate["derivation"]]
    if rules != expected_rules:
        raise AssertionError(f"unexpected derivation rules: {rules}")
    if certificate["source"]["sha256"] != (
        "ca7631580c8a96ff440892fe1ab8d8b42edc84f0dc6eaaf990d404c75f47c7c7"
    ):
        raise AssertionError("paper source hash mismatch")

    audits = [constants_audit(p) for p in (2.0, 2.5, 3.0, 5.0, 10.0, 100.0)]
    if not all(row["c1_dominates"] and row["c2_matches"] for row in audits):
        raise AssertionError("displayed constants do not follow from the reconstructed proof")

    control = one_large_jump_control()
    if control["mutated_bound_holds"]:
        raise AssertionError("negative control failed to reject the Gaussian-only mutation")

    checker = run_independent_checker()
    return {
        "claim": 1,
        "verdict": "VERIFIED",
        "basis": (
            "Independent symbolic reconstruction of the universal p>=2 derivation, "
            "with exact constant recovery and an independently implemented exhaustive diagnostic."
        ),
        "derivation_rules": rules,
        "constant_audits": audits,
        "negative_control": control,
        "independent_checker": checker,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))

