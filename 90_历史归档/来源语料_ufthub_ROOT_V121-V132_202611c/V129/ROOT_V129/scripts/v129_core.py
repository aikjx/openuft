"""ROOT V129 reproducible algebra checks: established SM anomaly algebra and KK toy limits.
NOT a proof of a new force or four-force unification.
All hypercharges use Q_electric=T3+Y and LEFT-handed Weyl representation convention.
"""
from __future__ import annotations
import math
from fractions import Fraction
import numpy as np
import sympy as sp

H = sp.Rational(1,2)
C = 299792458.0
HBAR = 1.054571817e-34
M_E = 9.1093837015e-31
E_CHARGE = 1.602176634e-19
PLANCK_LENGTH = 1.616255e-35
ALPHA = 1/137.035999177
M_MU_MEV = 105.6583755
M_E_MEV = 0.51099895000


def anomaly_polynomials(right_neutrino=True):
    """Return formal anomaly polynomials for one generation with four Yukawas if nu_R.
    q=Y_{Q_L}, l=Y_{L_L}, h=Y_H. All RH are converted to LH conjugates.
    Normalizations of SU(N)^2U(1) omit common Dynkin index 1/2.
    """
    q, l, h = sp.symbols('q l h')
    a33 = 2*q - (q+h) - (q-h)
    a22 = 3*q + l
    ayyy = 6*q**3 - 3*(q+h)**3 - 3*(q-h)**3 + 2*l**3 -(l-h)**3
    agr = 6*q - 3*(q+h)-3*(q-h)+2*l-(l-h)
    if right_neutrino:
        ayyy -= (l+h)**3
        agr -= l+h
    return {k: sp.factor(v) for k,v in {'SU3SU3Y':a33,'SU2SU2Y':a22,
                                         'YYY':ayyy,'gravgravY':agr}.items()}


def evaluate_anomalies(q, l, h=H, right_neutrino=True):
    q, l, h = map(sp.Rational, (q,l,h))
    syms = sp.symbols('q l h')
    return {k: sp.simplify(v.subs(dict(zip(syms,(q,l,h)))))
            for k,v in anomaly_polynomials(right_neutrino).items()}


def sm_hypercharges(x=sp.Integer(0), include_right_neutrino=True):
    """One-generation SM or x*(B-L) family, after H hypercharge = 1/2 normalization."""
    x=sp.Rational(x)
    q=sp.Rational(1,6)+x/3
    l=-sp.Rational(1,2)-x
    data={'Q_L':q,'u_R':q+H,'d_R':q-H,'L_L':l,'e_R':l-H}
    if include_right_neutrino:
        data['nu_R']=l+H
    return data


def electric_charges(x=sp.Integer(0)):
    x=sp.Rational(x)
    return {'up':sp.Rational(2,3)+x/3,'down':-sp.Rational(1,3)+x/3,
            'neutrino':-x, 'electron':-1-x}


def kk_mass(n: int, radius_m: float, parent_mass_kg: float = 0.0):
    assert radius_m>0 and parent_mass_kg>=0
    return math.hypot(parent_mass_kg, abs(int(n))*HBAR/(radius_m*C))


def kk_charge(n: int, fundamental_charge_c: float=E_CHARGE):
    return int(n)*fundamental_charge_c


def minimal_kk_coupling(radius_m: float):
    """Pure Einstein-Hilbert S1 KK photon coupling, fixed radion convention.
    Formula e_KK=sqrt(2)/(R*M_Pl,reduced) in natural units.
    Does NOT cover general higher dimensional models.
    """
    assert radius_m>0
    return math.sqrt(2)*math.sqrt(8*math.pi)*PLANCK_LENGTH/radius_m


def electromagnetic_coupling():
    return math.sqrt(4*math.pi*ALPHA)


def kk_radius_to_match_em_coupling():
    return math.sqrt(2)*math.sqrt(8*math.pi)*PLANCK_LENGTH/electromagnetic_coupling()


def rest_compton_radius():
    return HBAR/(M_E*C)


def massive_rest_phase(t: float, x: float, v: float, m: float=M_E):
    """Lorentz scalar inertial plane-wave action phase; x is aligned with velocity v."""
    assert abs(v)<C
    gm = 1/math.sqrt(1-(v/C)**2)
    return -(gm*m*C*C*t - gm*m*v*x)/HBAR


def boosted_phase(t, x, v, boost, m=M_E):
    """Return original and boosted phase for same event, same inertial four-momentum."""
    assert abs(v)<C and abs(boost)<C
    gm=1/math.sqrt(1-(v/C)**2)
    gb=1/math.sqrt(1-(boost/C)**2)
    E=gm*m*C*C; p=gm*m*v
    tp=gb*(t-boost*x/C**2)
    xp=gb*(x-boost*t)
    Ep=gb*(E-boost*p)
    pp=gb*(p-boost*E/C**2)
    return -(E*t-p*x)/HBAR, -(Ep*tp-pp*xp)/HBAR


def su2_jacobi(A,B,C_):
    comm=lambda X,Y:X*Y-Y*X
    return sp.simplify(comm(A,comm(B,C_))+comm(B,comm(C_,A))+comm(C_,comm(A,B)))


def audit_snapshot():
    right=anomaly_polynomials(True)
    left=anomaly_polynomials(False)
    ratio=M_MU_MEV/M_E_MEV
    return {'right_neutrino_anomaly_polynomials':{k:str(v) for k,v in right.items()},
            'without_right_neutrino_anomaly_polynomials':{k:str(v) for k,v in left.items()},
            'standard_model_residuals':{k:str(v) for k,v in evaluate_anomalies(sp.Rational(1,6),-sp.Rational(1,2)).items()},
            'right_neutrino_family_examples':{str(x):{k:str(v) for k,v in evaluate_anomalies(sp.Rational(1,6)+x/3,-sp.Rational(1,2)-x).items()} for x in map(sp.Rational,[0,sp.Rational(1,20),sp.Rational(-1,7)])},
            'muon_to_electron_mass_ratio':ratio,
            'KK_charge_predicted_if_muon_index_207_with_electron_index_1':207,
            'electron_compton_radius_m':rest_compton_radius(),
            'EM_dimensionless_coupling':electromagnetic_coupling(),
            'minimal_KK_coupling_at_electron_radius':minimal_kk_coupling(rest_compton_radius()),
            'coupling_mismatch_factor':electromagnetic_coupling()/minimal_kk_coupling(rest_compton_radius()),
            'KK_radius_to_match_EM_m':kk_radius_to_match_em_coupling(),
            'KK_mass_electron_ratio_at_EM_coupling_radius':rest_compton_radius()/kk_radius_to_match_em_coupling(),
            'one_generation_weak_doublets':4,
            'test_type':'symbolic_identity_and_toy_model_counterexamples_only'}
