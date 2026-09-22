"""Symbolic and numerical audit for the v_total=c helical kinematic chain."""

import sympy as sp


def main() -> None:
    t = sp.symbols("t", real=True)
    R, omega, vz, c = sp.symbols("R omega vz c", positive=True, nonzero=True)

    r = sp.Matrix(
        [
            R * sp.cos(omega * t),
            R * sp.sin(omega * t),
            vz * t,
        ]
    )
    r1 = sp.diff(r, t)
    r2 = sp.diff(r1, t)
    r3 = sp.diff(r2, t)

    speed2 = sp.simplify(r1.dot(r1))
    cross12 = sp.simplify(r1.cross(r2))
    curvature = sp.simplify(sp.sqrt(cross12.dot(cross12)) / speed2 ** sp.Rational(3, 2))
    torsion = sp.simplify(cross12.dot(r3) / cross12.dot(cross12))

    closure_residual = sp.factor(
        curvature**2 + torsion**2 - omega**2 / c**2
    )
    expected_residual = sp.factor(
        omega**2
        * (c**2 - (R**2 * omega**2 + vz**2))
        / (c**2 * (R**2 * omega**2 + vz**2))
    )

    print("speed_squared =", speed2)
    print("curvature     =", curvature)
    print("torsion       =", torsion)
    print("closure       =", closure_residual)
    print("expected form =", expected_residual)
    assert sp.simplify(closure_residual - expected_residual) == 0

    # Normalized numerical audit: c=1, R=0.6, omega=1, vz=0.8.
    vals = {c: 1, R: sp.Rational(3, 5), omega: 1, vz: sp.Rational(4, 5)}
    speed2_num = sp.simplify(speed2.subs(vals))
    kappa_num = sp.simplify(curvature.subs(vals))
    tau_num = sp.simplify(torsion.subs(vals))
    q_num = sp.sqrt(kappa_num**2 + tau_num**2)
    frequency_num = sp.simplify(c * q_num / (2 * sp.pi)).subs(vals)

    assert speed2_num == 1
    assert kappa_num == sp.Rational(3, 5)
    assert tau_num == sp.Rational(4, 5)
    assert q_num == 1
    assert sp.simplify(frequency_num - 1 / (2 * sp.pi)) == 0

    # Inverse map from (R,b) back to (kappa,tau,omega).
    b = sp.symbols("b", positive=True, nonzero=True)
    D = R**2 + b**2
    kappa_inverse = R / D
    tau_inverse = b / D
    q_inverse = sp.sqrt(kappa_inverse**2 + tau_inverse**2)
    assert sp.simplify(q_inverse - 1 / sp.sqrt(D)) == 0

    print("numeric_audit   = PASS")
    print("inverse_map     = PASS")


if __name__ == "__main__":
    main()
