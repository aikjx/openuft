"""Reproduce the neutral Einstein--sextic-scalar branch in report 20.

Run this file to write V3_8_self_gravity_reproduction.json. Importing it does
not solve or write anything. This is a numerical consistency check, not a
proof of stability, particle identification, or a new gravity theory.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import platform

import numpy as np
import scipy
from scipy.integrate import cumulative_trapezoid, simpson, solve_bvp


HOME = Path(__file__).resolve().parent
SEED = HOME / "V3_Qball_profile.csv"
Q_TARGET = 279.1642942626188
COUPLINGS = (0, 1e-7, 1e-6, 1e-5, 1e-4, 3e-4, 1e-3)
SINGULAR = np.zeros((5, 5))
SINGULAR[1, 1] = -2


def solve_background(gravity, charge, radius=100.0, previous=None, tol=1e-9):
    """State is (f, f', physical m, sigma, q/charge); mu=lambda=g6=1."""
    if not (np.all(np.isfinite([gravity, charge, radius, tol]))
            and gravity >= 0 and charge > 0
            and radius > 0 and tol > 0):
        raise ValueError("Require finite G>=0, Q>0, R>0 and tol>0")

    if previous is not None and previous.x[-1] == radius:
        mesh = previous.x
        initial = previous.y.copy()
        frequency = previous.p
    else:
        mesh = np.linspace(0, radius, 2200)
        if previous is not None:
            initial = previous.sol(mesh)
            frequency = previous.p
        else:
            seed = np.genfromtxt(SEED, delimiter=",", names=True)
            names = seed.dtype.names
            f = np.interp(mesh, seed[names[0]], seed[names[1]], right=0)
            derivative = np.interp(mesh, seed[names[0]], seed[names[2]], right=0)
            frequency = np.array([np.sqrt(0.9)])
            density = frequency[0] ** 2 * f ** 2 + derivative ** 2 + potential(f)
            mass = cumulative_trapezoid(4 * np.pi * mesh ** 2 * density,
                                        mesh, initial=0)
            q = cumulative_trapezoid(8 * np.pi * frequency[0] * mesh ** 2 * f ** 2,
                                     mesh, initial=0)
            initial = np.array([f, derivative, mass, np.ones_like(f), q / charge])

    # Scale the charge state to order one; q(R)=Q becomes q_scaled(R)=1.
    initial[4] /= initial[4, -1]

    def rhs(r, y, w):
        f, derivative, mass, lapse_factor, _ = y
        mass_over_r = np.divide(mass, r, out=np.zeros_like(r), where=r != 0)
        metric = 1 - 2 * gravity * mass_over_r
        phase_energy = w[0] ** 2 * f ** 2 / (lapse_factor ** 2 * metric)
        density = phase_energy + metric * derivative ** 2 + potential(f)
        radial_pressure = phase_energy + metric * derivative ** 2 - potential(f)
        mass_derivative = 4 * np.pi * r ** 2 * density
        lapse_derivative = (lapse_factor * 4 * np.pi * gravity * r
                            * (density + radial_pressure) / metric)
        metric_derivative = -2 * gravity * np.divide(
            mass_derivative - mass_over_r, r, out=np.zeros_like(r), where=r != 0
        )
        return np.array([
            derivative,
            -(lapse_derivative / lapse_factor + metric_derivative / metric)
            * derivative + (potential_prime(f) / metric
                             - w[0] ** 2 / (lapse_factor ** 2 * metric ** 2)) * f,
            mass_derivative,
            lapse_derivative,
            8 * np.pi * w[0] * r ** 2 * f ** 2 / (lapse_factor * metric * charge),
        ])

    def boundary(center, exterior, w):
        # The clamp only permits Newton iterations. Acceptance below requires w<1.
        kappa = np.sqrt(max(1 - w[0] ** 2, 1e-12))
        exponent = gravity * exterior[2] * (2 * w[0] ** 2 - 1) / kappa
        beta = kappa + (1 - exponent) / radius
        return np.array([center[1], center[2], center[4],
                         exterior[1] + beta * exterior[0],
                         exterior[3] - 1, exterior[4] - 1])

    solution = solve_bvp(rhs, boundary, mesh, initial, p=frequency,
                         S=SINGULAR, tol=tol, max_nodes=70000)
    sample_r = np.linspace(0, radius, 48001)
    f, _, mass, lapse, _ = solution.sol(sample_r)
    metric = 1 - 2 * gravity * np.divide(
        mass, sample_r, out=np.zeros_like(sample_r), where=sample_r != 0
    )
    accepted = (solution.status == 0 and 0 < solution.p[0] < 1
                and f[0] > 0.1 and np.min(f) > -1e-10
                and np.all(np.isfinite(solution.y))
                and np.min(lapse) > 0 and np.min(metric) > 0)
    if not accepted:
        raise RuntimeError("Rejected G={}, Q={}, R={}, tol={}, status={}, {}".format(
            gravity, charge, radius, tol, solution.status, solution.message))
    return solution


def potential(f):
    return f ** 2 - f ** 4 + f ** 6


def potential_prime(f):
    """Derivative dU(s)/ds evaluated at s=f^2, not dU/df."""
    return 1 - 2 * f ** 2 + 3 * f ** 4


def measure(solution, gravity, charge, tol):
    radius = float(solution.x[-1])
    r = np.linspace(0, radius, 48001)
    f, derivative, mass, lapse, q_scaled = solution.sol(r)
    w = float(solution.p[0])
    metric = 1 - 2 * gravity * np.divide(mass, r, out=np.zeros_like(r), where=r != 0)
    phase = w ** 2 * f ** 2 / (lapse ** 2 * metric)
    density = phase + metric * derivative ** 2 + potential(f)
    radial = phase + metric * derivative ** 2 - potential(f)
    tangential = phase - metric * derivative ** 2 - potential(f)

    def integrate(values):
        return float(4 * np.pi * simpson(r ** 2 * values, x=r))

    adm = float(mass[-1])
    komar = integrate(lapse * (density + radial + 2 * tangential))
    proper = integrate(density / np.sqrt(metric))
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "G": gravity, "Q_target": charge, "R": radius, "solver_tol": tol,
        "nodes": int(len(solution.x)), "solver_status": int(solution.status),
        "max_solver_residual": float(max(solution.rms_residuals)),
        "w": w, "f0": float(f[0]), "sigma0": float(lapse[0]),
        "ADM_mass": adm, "Komar_mass": komar,
        "Komar_minus_ADM": komar - adm,
        "integral_mass_error": integrate(density) - adm,
        "integral_Q_error": integrate(2 * w * f ** 2 / (lapse * metric)) - charge,
        "boundary_Q_error": float(charge * q_scaled[-1] - charge),
        "proper_matter_energy": proper, "proper_energy_minus_ADM": proper - adm,
        "free_particle_energy_minus_ADM": charge - adm,
        "min_N_sampled": float(np.min(metric)), "ftail": float(f[-1]),
    }


def run_reproduction():
    """All seven historical couplings, region refinement and three Q differences."""
    branch = []
    previous = None
    for gravity in COUPLINGS:
        previous = solve_background(gravity, Q_TARGET, previous=previous)
        branch.append(measure(previous, gravity, Q_TARGET, 1e-9))
    base = previous
    refined = solve_background(1e-3, Q_TARGET, radius=140, previous=base, tol=1e-10)
    differences = []
    for step in (1.0, 0.5, 0.25):
        plus = solve_background(1e-3, Q_TARGET + step, previous=base)
        minus = solve_background(1e-3, Q_TARGET - step, previous=base)
        derivative = float((plus.y[2, -1] - minus.y[2, -1]) / (2 * step))
        differences.append({"step": step, "dM_dQ": derivative,
                            "omega": float(base.p[0]),
                            "difference": derivative - float(base.p[0]),
                            "plus_residual": float(max(plus.rms_residuals)),
                            "minus_residual": float(max(minus.rms_residuals))})
    return {
        "scope": "neutral Einstein sextic scalar, fixed Q; no stability proof",
        "versions": {"python": platform.python_version(), "numpy": np.__version__,
                     "scipy": scipy.__version__},
        "sha256": {SEED.name: hashlib.sha256(SEED.read_bytes()).hexdigest(),
                   Path(__file__).name: hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
        "method": "q/Q scaling; adaptive BVP; 48001 point Simpson; reject failed backgrounds",
        "branch": branch, "refinement": measure(refined, 1e-3, Q_TARGET, 1e-10),
        "mass_charge": differences,
        "limits": "finite sampled domains, double precision, no certified error enclosure",
    }


if __name__ == "__main__":
    result = run_reproduction()
    output = HOME / "V3_8_self_gravity_reproduction.json"
    output.write_text(json.dumps(result, indent=2, allow_nan=False), encoding="utf-8")
    print("Reproduction saved to {}".format(output))
    print("Run test_self_gravity_reproduction.py for numerical regression checks.")
