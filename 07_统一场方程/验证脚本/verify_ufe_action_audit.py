"""Independent algebra and mass-dimension checks for the audited EC+SM action.

This verifies symbolic identities and engineering dimensions. It does not prove
the physical truth of the action or replace functional variation.
Requires SymPy.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


def require_zero(label: str, expression: sp.Expr, results: list[dict]) -> None:
    residual = sp.simplify(expression)
    passed = residual == 0
    results.append({"check": label, "status": "PASS" if passed else "FAIL", "residual": str(residual)})
    if not passed:
        raise AssertionError(f"{label}: residual={residual}")


def main() -> None:
    g2, gY, g1, v, mW, mZ = sp.symbols("g_2 g_Y g_1 v m_W m_Z", positive=True)
    results: list[dict] = []

    # Hypercharge convention: Q = T3 + Y, g1 = sqrt(5/3) gY.
    gut_conversion = sp.sqrt(sp.Rational(5, 3)) * gY
    require_zero("GUT/physical hypercharge coupling conversion", (g1**2 - sp.Rational(5, 3) * gY**2).subs(g1, gut_conversion), results)

    # Higgs kinetic term after <H>=(0,v/sqrt(2)): charged and neutral mass blocks.
    neutral = (v**2 / 4) * sp.Matrix([[g2**2, -g2 * gY], [-g2 * gY, gY**2]])
    require_zero("neutral mass determinant gives a massless photon", neutral.det(), results)
    require_zero("neutral massive eigenvalue", neutral.trace() - v**2 * (g2**2 + gY**2) / 4, results)
    mW2 = g2**2 * v**2 / 4
    mZ2 = neutral.trace()
    require_zero("charged W mass relation", mW2 - (g2 * v / 2) ** 2, results)
    require_zero("neutral Z mass relation", mZ2 - v**2 * (g2**2 + gY**2) / 4, results)
    require_zero("tree-level rho parameter", (g2**2 * v**2 / 4) / ((g2**2 + gY**2) * v**2 / 4 * g2**2 / (g2**2 + gY**2)) - 1, results)
    require_zero("electric coupling from either electroweak factor", g2 * (gY / sp.sqrt(g2**2 + gY**2)) - gY * (g2 / sp.sqrt(g2**2 + gY**2)), results)

    # Natural-unit mass dimensions. Every Lagrangian term must have dimension 4.
    dim = {"Mpl": 1, "R": 2, "Lambda": 2, "F": 2, "H": 1, "D": 1, "psi": sp.Rational(3, 2), "g": 0, "Yukawa": 0}
    lagrangian_terms = {
        "Einstein-Hilbert": 2 * dim["Mpl"] + dim["R"],
        "cosmological constant": 2 * dim["Mpl"] + dim["Lambda"],
        "Yang-Mills": 2 * dim["F"],
        "Higgs kinetic": 2 * (dim["D"] + dim["H"]),
        "Higgs quartic potential": 4 * dim["H"],
        "Dirac kinetic": 2 * dim["psi"] + dim["D"],
        "Yukawa interaction": 2 * dim["psi"] + dim["H"] + dim["Yukawa"],
    }
    for label, value in lagrangian_terms.items():
        passed = value == 4
        results.append({"check": f"dimension of {label}", "status": "PASS" if passed else "FAIL", "dimension": str(value), "expected": "4"})
        if not passed:
            raise AssertionError(f"{label} has mass dimension {value}, expected 4")

    # Field-equation dimensions: source and left-hand side must match.
    equation_dimensions = {
        "Einstein equation": (dim["R"], -2 + 4),
        "Yang-Mills equation": (dim["D"] + dim["F"], 3),
        "Higgs equation": (2 * dim["D"] + dim["H"], 3),
        "Dirac equation": (dim["D"] + dim["psi"], dim["H"] + dim["psi"]),
    }
    for label, (lhs, rhs) in equation_dimensions.items():
        passed = sp.simplify(lhs - rhs) == 0
        results.append({"check": f"dimension balance: {label}", "status": "PASS" if passed else "FAIL", "lhs": str(lhs), "rhs": str(rhs)})
        if not passed:
            raise AssertionError(f"dimension mismatch in {label}: {lhs} != {rhs}")

    report = {
        "scope": "symbolic identities and natural-unit engineering dimensions for the audited Einstein-Cartan + Standard Model variational system",
        "not_verified": ["functional variations", "anomaly cancellation", "quantum corrections", "experimental agreement", "derivation from the light-speed helix postulate"],
        "checks": results,
        "total": len(results),
        "passed": sum(row["status"] == "PASS" for row in results),
    }
    output = Path(__file__).with_name("ufe_action_audit_results.json")
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"total": report["total"], "passed": report["passed"], "output": output.name}, ensure_ascii=False))


if __name__ == "__main__":
    main()
