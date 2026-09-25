"""Finite EH_mu audit, with independent arithmetic and prefix validation.

Requires Python 3, NumPy, and a C++17 compiler named g++.
Run: python reproduce.py
No floating point result from this program is a proof of an asymptotic estimate.
The exact prime-pair counts use integer/Boolean arithmetic.
"""
from pathlib import Path
import json
import math
import subprocess
import tempfile
import numpy as np

ROOT = Path(__file__).resolve().parent
THETAS = [0.40, 0.45, 0.50, 0.55, 0.60]
COLS = ["q", "phi", "end_control_total", "end_control_y", "end_twist",
        "max_control_total", "max_control_y", "max_twist",
        "wrong_control_all_r", "wrong_twist_all_r"]


def modulus_cutoff(E, theta):
    """Exact floor(E^theta) for this experiment's rational theta = k/20."""
    k = round(theta * 20)
    assert abs(theta - k/20) < 1e-12
    target = E**k
    q = math.floor(E**theta)
    while (q+1)**20 <= target:
        q += 1
    while q**20 > target:
        q -= 1
    return q


def arithmetic(E):
    prime = np.ones(E, dtype=bool)
    prime[:2] = False
    for p in range(2, math.isqrt(E - 1) + 1):
        if prime[p]:
            prime[p*p::p] = False
    primes = np.flatnonzero(prime)
    mu = np.ones(E, dtype=np.int8)
    mu[0] = 0
    lam = np.zeros(E)
    for p0 in primes:
        p = int(p0)
        mu[p::p] *= -1
        square = p*p
        if square < E:
            # The stride is p^2, not p. Otherwise almost all composites vanish.
            mu[square::square] = 0
        power = p
        while power < E:
            lam[power] = math.log(p)
            power *= p
    return prime, primes, mu, lam


def trial_mu(n):
    sign, p = 1, 2
    while p*p <= n:
        if n % p == 0:
            n //= p
            sign = -sign
            if n % p == 0:
                return 0
        p += 1
    return -sign if n > 1 else sign


def scan(exe, E, Q):
    result = subprocess.run([str(exe), str(E), str(Q)], check=True,
                            text=True, capture_output=True)
    lines = result.stdout.splitlines()
    meta = lines[0].split()
    meta = {meta[i]: float(meta[i+1]) for i in range(1, len(meta), 2)}
    matrix = np.array([[float(x) for x in line.split()]
                       for line in lines if not line.startswith("#")])
    return meta, matrix


def validate_small(exe):
    E, Q = 200, 40
    _, _, mu, lam = arithmetic(E)
    for n in range(1, E):
        assert int(mu[n]) == trial_mu(n), ("mu", n)
    n = np.arange(E)
    twist = np.zeros(E)
    twist[1:] = lam[1:] * mu[E-n[1:]]
    pref_p, pref_t = np.cumsum(lam), np.cumsum(twist)
    _, rows = scan(exe, E, Q)
    worst = 0.0
    for row in rows:
        q, phi = int(row[0]), int(row[1])
        residues = [r for r in range(q) if math.gcd(r, q) == 1]
        cp = np.array([np.cumsum(lam * (n % q == r)) for r in residues])
        ct = np.array([np.cumsum(twist * (n % q == r)) for r in residues])
        ep, ey, et = abs(cp-pref_p/phi), abs(cp-n/phi), abs(ct-pref_t/phi)
        expected = np.array([ep[:, -1].max(), ey[:, -1].max(), et[:, -1].max(),
                             ep.max(), ey.max(), et.max()])
        worst = max(worst, float(abs(row[2:8]-expected).max()))
        assert np.allclose(row[2:8], expected, rtol=1e-11, atol=1e-10), q
    return {"E": E, "Q": Q, "cuts": "every integer 0 <= y < E",
            "independent_bruteforce_max_absolute_difference": worst,
            "mu_trial_division": "passed for every 1 <= n < 200"}


def icbrt(n):
    x = round(n ** (1/3))
    while (x+1)**3 <= n:
        x += 1
    while x**3 > n:
        x -= 1
    return x


def switching_audit(E, prime, primes, mu, lam):
    """Retain the triangular n < E-D*k domain in divisor switching."""
    D = math.isqrt(E)
    K = (E-2)//D
    phi = np.arange(K+1)
    for p in primes[primes <= K]:
        phi[p::p] -= phi[p::p]//p
    small_divisor = np.zeros(E)
    for d in range(2, D+1):
        if mu[d]:
            small_divisor[d::d] -= int(mu[d])*math.log(d)
    n = np.arange(1, E)
    m = E-n
    S1 = math.fsum((lam[n]*mu[m]**2*small_divisor[m]).tolist())
    F = math.fsum((lam[n]*mu[m]**2*lam[m]).tolist())
    a = np.zeros(E)
    a[1:] = lam[1:]*mu[E-n]
    b = np.zeros(E)
    b[1:] = a[1:]*np.log(E-n)
    pa = np.cumsum(a, dtype=np.longdouble)
    pb = np.cumsum(b, dtype=np.longdouble)
    actual_terms, rectangular_terms, unit_terms, nonunit_terms, center_terms = [], [], [], [], []
    for k in range(1, K+1):
        if not mu[k]:
            continue
        m_valid = np.arange((D+1)*k, E, k)
        term = int(mu[k])*math.fsum((lam[E-m_valid]*mu[m_valid]*np.log(k/m_valid)).tolist())
        actual_terms.append(term)
        m_all = np.arange(k, E, k)
        rectangular_terms.append(int(mu[k])*math.fsum((lam[E-m_all]*mu[m_all]*np.log(k/m_all)).tolist()))
        if math.gcd(k, E) == 1:
            unit_terms.append(term)
            Y = E-D*k-1
            center_terms.append(float(int(mu[k])/int(phi[k])*(math.log(k)*pa[Y]-pb[Y])))
        else:
            nonunit_terms.append(term)
    S2 = math.fsum(actual_terms)
    assert abs(S1+S2-F) < 1e-6, (E, S1+S2-F)
    center = math.fsum(center_terms)
    return {"D": D, "K": K, "S1": S1, "S2_correct_triangular": S2,
            "F_squarefree_complement": F, "identity_residual": S1+S2-F,
            "S2_rectangular_printed_range": math.fsum(rectangular_terms),
            "rectangular_minus_correct": math.fsum(rectangular_terms)-S2,
            "S2_coprime_k": math.fsum(unit_terms),
            "S2_noncoprime_k": math.fsum(nonunit_terms),
            "triangular_uniform_center": center,
            "signed_triangular_error": math.fsum(unit_terms)-center,
            "note": "A finite identity/range audit. A missing printed cutoff alone does not refute the paper's conditional theorem."}


def finite_goldbach(E, prime, primes, mu, lam):
    n = np.arange(1, E)
    complement = E-n
    both_prime = prime[n] & prime[complement]
    ordered = int(both_prime.sum())
    diagonal = int(prime[E//2])
    weighted_prime = math.fsum((lam[n[both_prime]] * lam[complement[both_prime]]).tolist())
    weighted_mangoldt = math.fsum((lam[n] * lam[complement]).tolist())
    power_indices = np.flatnonzero((lam != 0) & ~prime)
    H = math.fsum(float(lam[k]*lam[E-k]) for k in power_indices)
    power = (lam != 0) & ~prime
    J = math.fsum(float(lam[k]*lam[E-k]) for k in power_indices if power[E-k])
    assert abs(weighted_prime - (weighted_mangoldt - 2*H + J)) < 1e-6
    z = icbrt(E)
    rough = np.ones(E, dtype=bool)
    for p in primes[primes <= z]:
        rough[p::p] = False
    mask = prime[n] & (complement > z) & rough[complement]
    W = math.fsum((lam[n[mask]] * mu[complement[mask]]**2).tolist())
    D = math.fsum((lam[n[mask]] * mu[complement[mask]]).tolist())
    central_prime_weight = math.fsum(lam[n[mask & prime[complement]]].tolist())
    assert abs((W-D)/2 - central_prime_weight) < 1e-7
    p_odd = primes[primes > 2]
    singular_upper = 2 * math.prod((1.0 - 1.0/(int(p)-1)**2) for p in p_odd)
    for p in p_odd:
        if E % int(p) == 0:
            singular_upper *= (int(p)-1)/(int(p)-2)
    # The omitted prime tail is bounded by the tail over all integers.
    X = E-1
    singular_lower = singular_upper * (1 - 1/(X-1))
    M = math.fsum((lam[n] * mu[complement]).tolist())
    delta_range = sorted([weighted_mangoldt-S*(E-M)
                         for S in [singular_lower, singular_upper]])
    return {
        "ordered_prime_pairs": ordered, "unordered_prime_pairs": (ordered+diagonal)//2,
        "weighted_prime_pairs": weighted_prime, "weighted_mangoldt_pairs": weighted_mangoldt,
        "M": M, "M_over_E": M/E,
        "proper_prime_power_count_K": int(len(power_indices)),
        "H": H, "J": J, "actual_prime_power_contamination": 2*H-J,
        "elementary_contamination_upper_bound_2Klog2": 2*len(power_indices)*math.log(E)**2,
        "singular_series_tail_bracket_approx": [singular_lower, singular_upper],
        "Delta_tail_bracket_approx": delta_range,
        "bracket_note": "Analytic tail bound is rigorous; displayed endpoints use ordinary double arithmetic, not interval arithmetic.",
        "rough_local_identity": {"z": z, "W": W, "D": D,
            "(W-D)/2": (W-D)/2, "direct_prime_weight": central_prime_weight},
        "scope": "A certificate for this single E only; not an asymptotic proof."}


def main():
    report = {"date": "2026-09-11", "thetas": THETAS,
              "definitions": {
                  "end": "y=E-1; all sums n<=y",
                  "max": "all integer 0<=y<E; exact cut coverage for EH_mu",
                  "control_total_center": "sum(n<=y) Lambda(n) / phi(q)",
                  "control_y_center": "y / phi(q)",
                  "twist_center": "sum(n<=y) Lambda(n) mu(E-n) / phi(q)",
                  "normalization": "Err * log(E)^2 / E; no pass/fail threshold is implied",
                  "precision": "double weights and residue sums; long double global prefixes in C++; no interval arithmetic",
                  "old_bug_mechanism": "odd prime moduli, max over all residues including non-coprime r=0"},
              "validation": {}, "scales": []}
    with tempfile.TemporaryDirectory() as temporary:
        exe = Path(temporary)/"eh_mu_scan"
        subprocess.run(["g++", "-O3", "-std=c++17", str(ROOT/"eh_mu_scan.cpp"), "-o", str(exe)], check=True)
        report["validation"] = validate_small(exe)
        for E in [10_000, 100_000, 1_000_000]:
            Qmax = modulus_cutoff(E, max(THETAS))
            meta, rows = scan(exe, E, Qmax)
            prime, primes, mu, lam = arithmetic(E)
            n = np.arange(1, E)
            independent_M = math.fsum((lam[n] * mu[E-n]).tolist())
            assert abs(meta["M"]-independent_M) < 1e-7
            assert abs(meta["psi"]-math.fsum(lam.tolist())) < 1e-7
            assert np.all(rows[:, 5:8]+1e-7 >= rows[:, 2:5])
            q = rows[:, 0].astype(int)
            fac = math.log(E)**2/E
            summaries = []
            for theta in THETAS:
                Q = modulus_cutoff(E, theta)
                subset = q <= Q
                odd_primes = subset & prime[q] & (q > 2)
                item = {"theta": theta, "Q": Q, "odd_prime_moduli": int(odd_primes.sum())}
                for j, name in enumerate(COLS[2:], 2):
                    item["all_q_"+name] = float(rows[subset, j].sum()*fac)
                    item["odd_prime_q_"+name] = float(rows[odd_primes, j].sum()*fac)
                summaries.append(item)
            case = {"E": E, "psi": meta["psi"], "M": meta["M"],
                    "Mertens_E_minus_1": int(mu.sum()), "summary": summaries,
                    "goldbach": finite_goldbach(E, prime, primes, mu, lam),
                    "switching": switching_audit(E, prime, primes, mu, lam)}
            report["scales"].append(case)
            if E == 1_000_000:
                detail = {"E": E, "columns": COLS, "rows": rows.tolist()}
                (ROOT/"per_modulus_E1000000.json").write_text(json.dumps(detail, ensure_ascii=False, indent=2), encoding="utf-8")
            print(json.dumps({"E": E, "M": meta["M"], "summary": summaries}, ensure_ascii=False), flush=True)
        prime, primes, mu, lam = arithmetic(20)
        tiny = switching_audit(20, prime, primes, mu, lam)
        assert abs(tiny['rectangular_minus_correct']-math.log(3)*math.log(17)) < 1e-12
        report['switching_E20_D4'] = tiny
    (ROOT/"results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Validated and wrote results.json and per_modulus_E1000000.json", flush=True)


if __name__ == "__main__":
    main()
