#!/usr/bin/env python3
"""ROOT V131 independent algebra/numeric audit. Python 3.9+, stdlib only.
In derivations c=1, hbar and G are not set to 1. SI constants appear
only where translating a dimensionful example to seconds/eV.
"""
from __future__ import annotations
import csv
import json
import math
import random
from decimal import Decimal, localcontext
from pathlib import Path

HERE = Path(__file__).resolve().parent
C_SI = 299_792_458.0  # m/s, exact SI definition, conversion only


def roots_x(x: float, sigma: int):
    """Dimensionless omega/k and v_g for constant b/k=x; real stable branch."""
    if sigma not in (-1, 1) or 1.0 - sigma*x <= 0:
        return None
    w = math.sqrt(1.0 - sigma*x)
    vg = (2.0 - sigma*x) / (2.0*w)
    delta_v2 = x*x/(4.0*(1.0 - sigma*x))
    return w, vg, delta_v2


def state_rhs(y, *, k: float, eta: float, f: float, mass: float, sigma: int):
    a, ad, th, thd = y
    add = -(k*k - sigma*eta*thd*k)*a
    thdd = -mass*mass*th - eta*sigma*k*a*ad/(f*f)
    return (ad, add, thd, thdd)


def energy(y, *, k: float, f: float, mass: float):
    a, ad, th, thd = y
    return 0.5*(ad*ad + k*k*a*a) + 0.5*f*f*(thd*thd + mass*mass*th*th)


def rk4_step(y, h, **params):
    def add(s, d, c):
        return tuple(a+c*b for a, b in zip(s, d))
    a = state_rhs(y, **params)
    b = state_rhs(add(y, a, h/2), **params)
    c = state_rhs(add(y, b, h/2), **params)
    d = state_rhs(add(y, c, h), **params)
    return tuple(v + h*(aa+2*bb+2*cc+dd)/6
                 for v, aa, bb, cc, dd in zip(y, a, b, c, d))


def main():
    tests = []
    def verify(label, condition, info=None):
        if not condition:
            raise AssertionError(f"FAILED: {label}: {info}")
        tests.append(label)

    # Plane circular polarization: local invariants and Poynting vector.
    for sigma in (-1, 1):
        for n in range(2048):
            phase = 2*math.pi*n/2048
            ex, ey = math.cos(phase), sigma*math.sin(phase)
            bx, by = -ey, ex
            verify_ok = (abs(ex*bx+ey*by)<1e-12 and
                         abs((ex*ex+ey*ey)-(bx*bx+by*by))<1e-12 and
                         abs(ex*by-ey*bx-1.0)<1e-12)
            if not verify_ok: raise AssertionError(f"EM invariants {sigma} {n}")
    verify('4096 phases: E·B=0, E²=B², S parallel to +z', True)

    rng = random.Random(131)
    tested = 0
    for _ in range(5000):
        x = rng.uniform(-0.95,0.95)
        for sigma in (-1,1):
            w, vg, dsq = roots_x(x, sigma)
            if abs((vg*vg-1.0)-dsq)>2e-12:
                raise AssertionError('Group velocity dispersion identity')
            tested += 1
    verify('10000 stable helicity-branch dispersion identities', tested==10000)

    for sig, x in [(+1, .1),(+1, 1.01),(-1,-1.01)]:
        actual = roots_x(x,sig)
        expected_stable = (1-sig*x)>0
        verify('stability sign for (sigma,b/k)=('+str(sig)+','+str(x)+')', (actual is not None)==expected_stable)

    # Extremely small frequency splitting: high precision required.
    with localcontext() as ctx:
        ctx.prec=70
        wav = Decimal('550e-9')
        k = Decimal(str(2*math.pi))/wav  # accurately enough for physical example
        b = Decimal('1e-6')
        L = Decimal('1000')
        x = b/k
        sqplus = (Decimal(1)+x).sqrt()
        sqminus = (Decimal(1)-x).sqrt()
        beta_exact = b*L/(sqplus+sqminus)  # exact fixed-k phase rotation at t=L
        beta_approx = b*L/Decimal(2)
        vg_sq_offset = x*x/(Decimal(4)*(Decimal(1)-x))
        verify('high-precision delta beta approaches bL/2', abs(beta_exact-beta_approx)<Decimal('1e-25'))
        verify('group v_g²-1 positive but tiny (no signal-front claim)', vg_sq_offset>0)
        example = dict(
            wavelength_m=float(wav), k_per_m=float(k), b_per_m=float(b),
            relative_x=float(x), distance_m=float(L),
            beta_exact_rad=float(beta_exact), beta_approx_rad=float(beta_approx),
            beta_deg=float(beta_exact*Decimal(180)/Decimal(str(math.pi))),
            vg_plus_squared_minus_1=float(vg_sq_offset),
            unstable_band_k_per_m=[0.,float(b)],
            maximal_growth_k_per_m=float(b/2),
            maximal_growth_per_m=float(b/2),
            illustrative_growth_time_s=float((Decimal(2)/b)/Decimal(str(C_SI))),
        )

    # Backreaction! Real helical spatial mode: A=a(t)*(cos kz, -sigma sin kz,0).
    # E=-a_dot*u, B=sigma*k*a*u, so E·B=-sigma*k*a*a_dot.
    # The EM gain and scalar loss cancel in energy derivative.
    params = dict(k=1.0, eta=1.0, f=1.0, mass=0.0, sigma=+1)
    y = (0.001, 0.0, 0.0, 2.0)  # initial effective b=2>k; unstable frozen background
    E0 = energy(y,k=params['k'],f=params['f'],mass=params['mass'])
    rows=[]
    h=.002
    max_err=0.0
    for i in range(4001):
        t=i*h
        Ecur=energy(y,k=params['k'],f=params['f'],mass=params['mass'])
        max_err=max(max_err,abs(Ecur-E0))
        if i%100==0:
            rows.append([round(t,6),*y,Ecur,Ecur-E0])
        if i<4000:
            y=rk4_step(y,h,**params)
    verify('coupled EM-scalar backreaction conserves total energy', max_err<1e-8, max_err)
    verify('initial b>k and backreaction changes theta_dot', y[3]<2.0)
    verify('EM mode gains energy from scalar field', abs(y[0])>0.001)
    with open(HERE/'backreaction_timeseries.csv','w',newline='',encoding='utf-8') as fp:
        writer=csv.writer(fp)
        writer.writerow(['t_natural_length','A','A_dot','theta','theta_dot','E_total','E_drift'])
        writer.writerows(rows)

    obs_deg=.277; obs_err_deg=.057
    obs=dict(beta_deg=obs_deg, sigma_deg=obs_err_deg,
             beta_rad=math.radians(obs_deg), sigma_rad=math.radians(obs_err_deg),
             inferred_eta_delta_theta=2*math.radians(obs_deg),
             inferred_eta_delta_theta_one_sigma=2*math.radians(obs_err_deg),
             caveat='illustrative mapping only: observational foreground/calibration systematics unresolved; no independent eta or theta determination')
    results=dict(name='ROOT V131 math/numeric audit', python_standard_library_only=True,
                 c_in_analytic_equations=1, hbar_set_to_one=False, G_set_to_one=False,
                 testing_scope='algebra, numerical integration, and dimensional illustrative calculations; no experimental validation of ROOT',
                 number_of_named_tests=len(tests),tests=tests,
                 em_invariant_phase_samples=4096,dispersion_samples=10000,
                 example=example, backreaction=dict(initial_energy=E0,final_energy=energy(y,k=1,f=1,mass=0),max_absolute_energy_drift=max_err,initial_theta_dot=2.,final_theta_dot=y[3],final_A=y[0],time_interval=8.0,step=.002),
                 published_cosmic_birefringence=obs)
    (HERE/'verification_results.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(results,indent=2,ensure_ascii=False))

if __name__=='__main__':
    main()
