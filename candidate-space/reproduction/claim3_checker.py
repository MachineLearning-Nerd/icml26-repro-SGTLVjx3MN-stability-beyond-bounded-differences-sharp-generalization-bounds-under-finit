"""Independent checker for the Claim 3 certificate.

This module deliberately imports no implementation from ``reproduction.claim3``.
It checks the raw certificate and reconstructs the finite witnesses using exact
rational arithmetic.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path


def independent_check(path: Path) -> dict[str, object]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    witness = raw["witness"]
    m = int(witness["sample_size"])
    assert m >= 1
    assert Fraction(witness["beta"]) == Fraction(1, m)
    assert witness["distribution"] == "standard_normal"
    assert witness["envelope"] == "abs(z-z_prime)"

    # Independent exact reconstruction of the beta-halving counterexample.
    old, new = Fraction(m), Fraction(0)
    lhs = abs(abs(old / m) - abs(new / m))
    correct_rhs = Fraction(1, m) * abs(old - new)
    mutated_rhs = Fraction(1, 2 * m) * abs(old - new)
    assert lhs == correct_rhs == 1
    assert lhs > mutated_rhs

    # Z-Z'~N(0,2), so its second moment is Var(Z-Z')=2.
    assert raw["moments"]["p"] == 2
    assert raw["moments"]["E_H_squared"] == 2

    # For any proposed finite uniform bound B, the family old=m(B+1), new=0
    # has loss increment B+1. Check representative exact members; the symbolic
    # affine formula is recorded in the certificate for the quantified step.
    for bound in (0, 1, 10, 10_000):
        old = Fraction(m * (bound + 1))
        increment = abs(abs(old / m) - 0)
        assert increment == bound + 1
        assert increment > bound
    assert raw["uniform_stability"]["witness_family"] == "z_i=m*(B+1), z_i_prime=0"
    assert raw["uniform_stability"]["supremum_is_infinite"] is True

    return {
        "status": "PASS",
        "certificate": str(path),
        "checks": [
            "beta equals 1/m",
            "Gaussian L2 moment equals 2",
            "halved-beta mutation rejected",
            "unbounded uniform-stability witness family reconstructed",
        ],
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python -m reproduction.claim3_checker RAW_RESULTS_JSON")
    print(json.dumps(independent_check(Path(sys.argv[1])), indent=2, sort_keys=True))
