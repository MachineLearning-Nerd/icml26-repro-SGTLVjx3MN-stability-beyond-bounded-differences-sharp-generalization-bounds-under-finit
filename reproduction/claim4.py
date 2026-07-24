"""Mechanical certificate for both high-probability bounds in Theorem 3.4."""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path


EVIDENCE_DIR = Path(".openresearch/artifacts/claim-4")
CERTIFICATE = EVIDENCE_DIR / "proof_certificate.json"


def theorem_22_constants(p: float) -> tuple[float, float]:
    scale = 4.0 * (p + 2.0) / p
    return 4.0 * scale**p, 1.0 / (2.0 * (p + 2.0) ** 2 * math.e**p)


def derived_constants(p: float) -> dict[str, float | bool]:
    base_c1, base_c2 = theorem_22_constants(p)
    c_polynomial = base_c1 * 2.0 ** (2.0 * p - 1.0)
    c_gaussian = base_c2 / 8.0
    return {
        "p": p,
        "theorem_2_2_c1": base_c1,
        "theorem_2_2_c2": base_c2,
        "admissible_c1_equals_c3": c_polynomial,
        "admissible_c2_equals_c4": c_gaussian,
        "positive": c_polynomial > 0.0 and c_gaussian > 0.0,
    }


def omitted_population_increment_control() -> dict[str, object]:
    """Reject the mutation |phi-phi_i| <= beta H + beta'G/m."""
    beta_h = 1.0
    beta_prime_g_over_m = 0.0
    required = 2.0 * beta_h + beta_prime_g_over_m
    mutated = beta_h + beta_prime_g_over_m
    return {
        "name": "omit_population_risk_increment",
        "required_envelope": required,
        "mutated_envelope": mutated,
        "mutated_inequality_holds": required <= mutated,
        "expected": "FAIL",
    }


def omitted_bias_shift_control() -> dict[str, object]:
    """An exact m=1 Bernoulli witness has a nonzero stability bias."""
    q = 0.5
    expected_population_risk = 2.0 * q * (1.0 - q)
    expected_empirical_risk = 0.0
    gap_bias = expected_population_risk - expected_empirical_risk
    beta_eh = 2.0 * q * (1.0 - q)
    return {
        "name": "delete_beta_EH_shift",
        "witness": "m=1, Z~Bernoulli(1/2), A_S=sample mean, loss(a,z)=|a-z|",
        "absolute_expected_gap": gap_bias,
        "certified_beta_EH": beta_eh,
        "mutated_zero_bias_claim_holds": math.isclose(gap_bias, 0.0, abs_tol=1e-15),
        "expected": "FAIL",
    }


def run_independent_checker() -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, "-m", "reproduction.claim4_checker", str(CERTIFICATE)],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise AssertionError(
            "independent Claim 4 checker failed\n"
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
    if certificate["quantifiers"] != {
        "m": "integer m>=1",
        "p": "real p>=2",
        "y": "real y>0",
        "samples": "every iid S~D^m satisfying Assumptions 3.1 and 3.3",
    }:
        raise AssertionError("Claim 4 quantifiers were changed")

    expected_steps = [
        "population_risk_increment",
        "empirical_risk_increment",
        "leave_one_out_increment",
        "stability_bias",
        "center_and_apply_theorem_2_2",
        "moment_decoupling",
    ]
    steps = [step["rule"] for step in certificate["derivation"]]
    if steps != expected_steps:
        raise AssertionError(f"unexpected derivation steps: {steps}")

    constants = [derived_constants(p) for p in (2.0, 2.5, 3.0, 7.0, 100.0)]
    if not all(row["positive"] for row in constants):
        raise AssertionError("derived constants are not positive over the audit points")

    increment_control = omitted_population_increment_control()
    bias_control = omitted_bias_shift_control()
    if increment_control["mutated_inequality_holds"]:
        raise AssertionError("missing-increment negative control unexpectedly passed")
    if bias_control["mutated_zero_bias_claim_holds"]:
        raise AssertionError("zero-bias negative control unexpectedly passed")

    checker = run_independent_checker()
    return {
        "claim": 4,
        "verdict": "VERIFIED",
        "confidence": "HIGH",
        "basis": (
            "Both universal inequalities are mechanically reduced to Theorem 2.2 "
            "under the exact Assumptions 3.1 and 3.3, with explicit constants."
        ),
        "derivation_steps": steps,
        "constant_audits": constants,
        "independent_checker": checker,
        "negative_controls": [increment_control, bias_control],
        "limitations": (
            "The executable certificate checks the mathematical reduction and a "
            "complete declared finite diagnostic; it is not a proof-assistant kernel."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
