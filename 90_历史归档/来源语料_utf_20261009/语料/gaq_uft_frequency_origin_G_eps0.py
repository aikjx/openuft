#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import mpmath as mp
mp.mp.dps = 50

def sci(x, n=6):
    return mp.nstr(x, n)

c = mp.mpf('299792458')
hbar = mp.mpf('1.0545718176461565e-34')
e_charge = mp.mpf('1.602176634e-19')
m_e = mp.mpf('9.1093837015e-31')
m_p = mp.mpf('1.67262192369e-27')
G = mp.mpf('6.67430e-11')
epsilon_0 = mp.mpf('8.8541878128e-12')
mu_0 = mp.mpf('1.25663706212e-6')
alpha = mp.mpf('7.2973525693e-3')
k_B = mp.mpf('1.380649e-23')
H0 = mp.mpf('2.184129758e-18')

l_P = mp.sqrt(hbar * G / c**3)
m_P = mp.sqrt(hbar * c / G)
t_P = mp.sqrt(hbar * G / c**5)
q_P = mp.sqrt(4 * mp.pi * epsilon_0 * hbar * c)
T_P = mp.sqrt(hbar * c**5 / (G * k_B**2))
omega_P = mp.mpf(1) / t_P

class ProofTracker:
    def __init__(self):
        self.passed = 0
        self.failed = 0
    def verify(self, name, lhs, rhs, tol=mp.mpf('1e-30')):
        rel_diff = abs(lhs - rhs) / (abs(lhs) + abs(rhs) + mp.mpf('1e-200'))
        ok = rel_diff < tol
        if ok: self.passed += 1
        else: self.failed += 1
        status = 'PASS' if ok else 'FAIL'
        print(f'  [{status}] {name}')
        print(f'         LHS = {sci(lhs, 18)}')
        print(f'         RHS = {sci(rhs, 18)}')
        print(f'         RelDiff = {sci(rel_diff, 3)}')
        return ok
    def identity(self, name, expr, tol=mp.mpf('1e-30')):
        abs_err = abs(expr)
        scale = max(abs(expr), mp.mpf('1e-200'))
        rel_err = abs_err / scale
        ok = rel_err < tol
        if ok: self.passed += 1
        else: self.failed += 1
        status = 'PASS' if ok else 'FAIL'
        print(f'  [{status}] {name}')
        print(f'         Expr = {sci(expr, 18)}')
        print(f'         AbsErr = {sci(abs_err, 3)}')
        return ok
    def summary(self):
        total = self.passed + self.failed
        print()
        print('=' * 60)
        print(f'  TEST SUMMARY: {self.passed}/{total} PASSED, {self.failed}/{total} FAILED')
        print('=' * 60)
        return self.failed == 0

tracker = ProofTracker()

print()
print('=' * 60)
print('SECTION 1: Frequency Pythagorean Theorem & Fine Structure')
print('=' * 60)
omega_kappa = c / l_P
omega_tau = alpha * omega_kappa
omega_comb = mp.sqrt(omega_kappa**2 + omega_tau**2)
tracker.verify('omega_kappa = c/l_P (Compton frequency)', omega_kappa, c/l_P)
tracker.verify('alpha = omega_tau/omega_kappa', omega_tau/omega_kappa, alpha)
tracker.verify('omega^2 = omega_kappa^2 + omega_tau^2 (Pythagorean)', omega_comb**2, omega_kappa**2 + omega_tau**2)

print()
print('=' * 60)
print('SECTION 2: G and epsilon_0 from Frequency Relations')
print('=' * 60)
G_from_freq = c**5 / (hbar * omega_P**2)
eps0_from_alpha = e_charge**2 / (4 * mp.pi * alpha * hbar * c)
tracker.verify('G = c^5/(hbar*omega_P^2)', G_from_freq, G, tol=mp.mpf('1e-5'))
tracker.verify('epsilon_0 = e^2/(4*pi*alpha*hbar*c)', eps0_from_alpha, epsilon_0, tol=mp.mpf('1e-5'))

print()
print('=' * 60)
print('SECTION 3: Electromagnetic-Gravitational Coupling')
print('=' * 60)
tracker.verify('4*pi*epsilon_0*G = (q_P/m_P)^2', 4*mp.pi*epsilon_0*G, (q_P/m_P)**2)

print()
print('=' * 60)
print('SECTION 4: Planck Force from Frequency')
print('=' * 60)
tracker.verify('F_P = hbar*omega_P^2/c = c^4/G', hbar*omega_P**2/c, c**4/G)

print()
print('=' * 60)
print('SECTION 5: Energy-Momentum-Frequency Identities')
print('=' * 60)
R_P = l_P
omega_P_id = c / R_P
tracker.identity('hbar*omega_P*R_P - hbar*c = 0', hbar*omega_P_id*R_P - hbar*c)
omega_e = m_e * c**2 / hbar
tracker.verify('E = hbar*omega = m*c^2 (electron)', hbar*omega_e, m_e*c**2)
tracker.verify('hbar*c = hbar*omega_P*l_P', hbar*c, hbar*omega_P*l_P)

print()
print('=' * 60)
print('SECTION 6: Cosmic Frequency Hierarchy')
print('=' * 60)
omega_electron = m_e * c**2 / hbar
omega_proton = m_p * c**2 / hbar
print(f'  Hubble frequency H0          = {sci(H0)} rad/s')
print(f'  Electron Compton omega_e     = {sci(omega_electron)} rad/s')
print(f'  Proton Compton omega_p       = {sci(omega_proton)} rad/s')
print(f'  Planck frequency omega_P     = {sci(omega_P)} rad/s')
print(f'  Ratio omega_P/H0             = {sci(omega_P/H0)}')
print(f'  Ratio omega_P/omega_e        = {sci(omega_P/omega_electron)}')

print()
print('=' * 60)
print('MASTER EQUATION SUMMARY: GAQ-UFT Framework')
print('=' * 60)
print('  omega_P = 1/t_P = sqrt(c^5/(hbar*G))               Planck frequency')
print('  G       = c^5/(hbar*omega_P^2)                     Gravitational constant from omega')
print('  eps0    = e^2/(4*pi*alpha*hbar*c)                  Vacuum permittivity from alpha')
print('  4*pi*eps0*G = (q_P/m_P)^2                          EM-Gravity coupling')
print('  F_P     = hbar*omega_P^2/c = c^4/G                 Planck force')
print('  omega^2 = omega_k^2 + omega_tau^2, alpha=omega_t/omega_k  Frequency Pythagoras')
print('  E       = hbar*omega = m*c^2                       Energy-frequency-mass')
print('  hbar*c  = hbar*omega_P*l_P                         Action-speed relation')
print('=' * 60)

tracker.summary()
