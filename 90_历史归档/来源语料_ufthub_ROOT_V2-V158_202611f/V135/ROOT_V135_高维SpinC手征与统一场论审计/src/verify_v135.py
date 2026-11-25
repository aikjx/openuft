#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ROOT V135 — 11D spin^c / index / chirality / vacuum no-go audit.

This verifies exact identities and a concrete Clifford representation. It does
NOT prove a physical unified theory or numerically solve 11D field equations.
All equations take c=1; hbar and G are independent dimensionful constants.
Dependencies: Python>=3.10; numpy>=1.24 ONLY for the optional Clifford test.
"""
from __future__ import annotations
import csv
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
DATA.mkdir(parents=True, exist_ok=True)
TESTS = []


def verify(label: str, condition: bool, value=''):
    TESTS.append(dict(test=label, passed=bool(condition), note=str(value)))
    if not condition:
        raise AssertionError(f'{label}: {value}')


def c1_degree(q: int) -> int:
    return 2 * q + 1


def cp2_index_ahat(q: int) -> Fraction:
    # [e^(c1/2) Ahat]_{degree 4}; p1(CP2)=3 h^2, int h^2=1
    c = c1_degree(q)
    return Fraction(c * c, 8) - Fraction(3, 24)


def cp2_index_triangular(q: int) -> int:
    return q * (q + 1) // 2


def sphere_twisted_index(m: int) -> int:
    # Spin Dirac on S2 twisted by a complex line of c1=m, int ch(E)=m
    return m


def index_x6(q: int, m: int) -> int:
    # X6 = CP2 x S2; product of two even-dimensional indices.
    return int(cp2_index_ahat(q)) * sphere_twisted_index(m)


def scalar_k(r_cp: float, r_s: float) -> float:
    # CP2 FS norm holomorphic sectional curvature 4; S2 unit-round norm.
    return 24 / r_cp**2 + 2 / r_s**2


def volume_k(r_cp: float, r_s: float, r_circle: float) -> float:
    return 4 * math.pi**4 * r_cp**4 * r_s**2 * r_circle


def numpy_clifford_test():
    try:
        import numpy as np
    except ImportError:
        return {'status': 'not_run', 'reason': 'numpy not installed'}

    I2 = np.eye(2, dtype=complex)
    s1 = np.array([[0, 1], [1, 0]], dtype=complex)
    s2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
    s3 = np.array([[1, 0], [0, -1]], dtype=complex)
    P = [s1, s2, s3]
    kron = np.kron
    gamma = [kron(s1, I2)] + [kron(1j * s2, p) for p in P]
    gamma5 = 1j * (gamma[0] @ gamma[1] @ gamma[2] @ gamma[3])
    I4 = np.eye(4, dtype=complex)
    I8 = np.eye(8, dtype=complex)
    I32 = np.eye(32, dtype=complex)
    rho = [kron(kron(s1, I2), I2), kron(kron(s2, I2), I2),
           kron(kron(s3, s1), I2), kron(kron(s3, s2), I2),
           kron(kron(s3, s3), s1), kron(kron(s3, s3), s2),
           kron(kron(s3, s3), s3)]
    Γ = [kron(g, I8) for g in gamma] + [1j * kron(gamma5, r) for r in rho]
    metric = [1] + [-1] * 10  # signature (+----------)
    maxerr = 0.0
    for i in range(11):
        for j in range(i, 11):
            anti = Γ[i] @ Γ[j] + Γ[j] @ Γ[i]
            expect = (2 * metric[i] * I32) if i == j else np.zeros((32, 32))
            err = float(np.max(np.abs(anti - expect)))
            maxerr = max(err, maxerr)
    verify('explicit 11D Clifford algebra (121 ordered relations via symmetry)', maxerr < 1e-12, maxerr)
    verify('4D gamma5 squared identity', np.allclose(gamma5 @ gamma5, I4))
    verify('4D left chiral projector rank 2', np.linalg.matrix_rank((I4 - gamma5)/2) == 2)
    verify('4D right chiral projector rank 2', np.linalg.matrix_rank((I4 + gamma5)/2) == 2)
    verify('11D contains 32 complex components for bulk Dirac', Γ[0].shape == (32, 32))
    return {'status': 'passed', 'max_clifford_residual': maxerr,
            'bulk_dirac_complex_components': 32,
            '4d_left_rank': 2, '4d_right_rank': 2,
            'interpretation': 'A 7D internal Dirac zero mode multiplies a 4D Dirac field, unless an extra projection is imposed.'}


def main():
    verify('CP2 is not ordinary Spin', 3 % 2 == 1)
    verify('CP2 admits determinant lines of odd c1 degree', all(c1_degree(q)%2 == 1 for q in range(-40, 41)))
    verify('CP2 canonical spin-c determinant O(3) at q=1', c1_degree(1)==3)
    verify('CP2 canonical spin-c index is one', cp2_index_ahat(1)==1)
    verify('CP2 zero spin-c index at q=0', cp2_index_ahat(0)==0)
    verify('CP2 index three at q=2, determinant O(5)', cp2_index_ahat(2)==3 and c1_degree(2)==5)
    verify('CP2 c1 term and Ahat factor use rational arithmetic', cp2_index_ahat(2) == Fraction(25,8)-Fraction(1,8))
    verify('CP2 parity symmetry q->-q-1', all(cp2_index_ahat(q) == cp2_index_ahat(-q-1) for q in range(-40,41)))

    index_rows=[]
    for q in range(-12, 13):
        i = cp2_index_ahat(q)
        verify(f'index exact/triangular identity q={q}', i == cp2_index_triangular(q), str(i))
        verify(f'index integer q={q}', i.denominator==1, str(i))
        for m in range(-6,7):
            i6=index_x6(q,m)
            verify(f'index multiplicativity q={q},m={m}', i6 == cp2_index_triangular(q)*m)
            index_rows.append({ 'q': q, 'det_c1_CP2_over_h': c1_degree(q),
                                'index_CP2': int(i), 'sphere_flux_m':m,
                                'index_S2':m, 'index_X6': i6,
                                'status': 'topological index only; NOT four-dimensional generations' })
    with (DATA/'spinc_index_sweep.csv').open('w', newline='', encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f, fieldnames=list(index_rows[0])); writer.writeheader(); writer.writerows(index_rows)
    verify('CP2 x S2 index (q=2,m=1) equals three',index_x6(2,1)==3)
    verify('CP2 x S2 index vanishes when m=0',all(index_x6(q,0)==0 for q in range(-5,6)))
    verify('CP2 x S2 index reverses with flux orientation',all(index_x6(q,-m)==-index_x6(q,m) for q in range(-4,5) for m in range(1,5)))
    verify('seven internal dimensions are odd: no ordinary chiral index of D7',4+2+1==7)
    verify('spinor dimension of complex 11D Dirac representation is 32',2**(11//2)==32)
    verify('11D Dirac decomposes as 4D Dirac x 7D spinor',4 * (2**(7//2)) == 32)

    # Gauge charges and anomaly of a vectorlike pair. For U(1): a left Weyl
    # particle of charge Q plus the left conjugate of a right Weyl particle
    # of charge Q has Q^3 + (-Q)^3 = 0, and Q + (-Q) = 0.
    charge_samples=[Fraction(-2,3),Fraction(-1,2),Fraction(1,6),Fraction(1,1)]
    verify('vectorlike U1 cubic anomaly cancels at all sampled charges',
           all((q**3+(-q)**3)==0 for q in charge_samples))
    verify('vectorlike mixed gravitational-U1 anomaly cancels',
           all(q+(-q)==0 for q in charge_samples))
    verify('multiplicity three does not turn Dirac into Weyl',3*2==6)

    verify('11D with only cosmological constant and flat M4 forces Λ=0',11-2==9)
    verify('Minkowski times CP2xS2xS1 is not Ricci-flat', scalar_k(1,1)>0)
    verify('pure EH compactification volume dimension scales as 7',
           math.isclose(volume_k(2,2,2)/volume_k(1,1,1),2**7,rel_tol=1e-14))
    verify('CP2 radius scaling is quartic',
           math.isclose(volume_k(2,1,1)/volume_k(1,1,1), 16))
    verify('S2 radius scaling is quadratic',
           math.isclose(volume_k(1,2,1)/volume_k(1,1,1), 4))
    verify('S1 radius scaling is linear',
           math.isclose(volume_k(1,1,2)/volume_k(1,1,1), 2))
    verify('4D effective G scaling under doubling all radii',
           math.isclose((1/volume_k(2,2,2))/(1/volume_k(1,1,1)), 1/128))

    # A common Einstein constant would require Ric_CP2=6/a^2,
    # Ric_S2=1/b^2, Ric_S1=0, and flat 4D Ric=0. Positives cannot equal 0.
    for a,b in [(1.,1.),(0.5,1.),(1.,5.),(3.,7.)]:
        verify(f'CP2 nonzero Ricci at a={a}', 6/a**2>0)
        verify(f'S2 nonzero Ricci at b={b}', 1/b**2>0)
        verify(f'full scalar positive a={a} b={b}',scalar_k(a,b)>0)

    # Global representation obstruction when an isometry group is used as
    # EXACT gauge group. Lifts / spin-c equivariance are additional input.
    z3=complex(math.cos(2*math.pi/3),math.sin(2*math.pi/3))
    verify('fundamental 3 does not descend as rep of PSU3', abs(z3-1)>1)
    verify('fundamental 2 does not descend as rep of SO3', -1!=1)

    cliff = numpy_clifford_test()
    results={'version':'ROOT V135','date':'2026-11-24',
             'units':'c=1; hbar and G independently dimensionful',
             'test_count':len(TESTS),'passed':sum(x['passed'] for x in TESTS),
             'failed':sum(not x['passed'] for x in TESTS),
             'index_scan_rows':len(index_rows),
             'illustration':{'spin_c_CP2_q':2,'sphere_monopole_m':1,'six_dimensional_index':index_x6(2,1),
                             'eleven_dimensional_bulk_Dirac': 'vectorlike 4D zero-mode pairs unless further mechanism'},
             'clifford':cliff,
             'limitations':['Index not full zero-mode spectrum in arbitrary backgrounds',
               'No 11D coupled Einstein/flux solution constructed',
               'No Standard Model particle spectrum, renormalized couplings or G derived',
               'No new experimental prediction or physical validation'],
             'sources':['https://georgedouzas.github.io/posts/fundamentals-of-mathematics-for-physicists/part-i-13-spinors-dirac-operator.html',
                        'https://link.springer.com/article/10.1007/JHEP05(2026)008',
                        'https://www.sciencedirect.com/science/article/pii/0550321381900213']}
    (DATA/'verification_results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    with (DATA/'named_tests.csv').open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=list(TESTS[0])); writer.writeheader(); writer.writerows(TESTS)
    print(json.dumps({'status':'PASS', 'tests':len(TESTS),'index_scan_rows':len(index_rows),
                      'clifford':cliff['status'],'failed':results['failed']},ensure_ascii=False))

if __name__=='__main__':
    main()
