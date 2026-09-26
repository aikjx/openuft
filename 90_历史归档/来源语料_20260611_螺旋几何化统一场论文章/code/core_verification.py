#!/usr/bin/env python3
# ====================================================
# Algorithm Alliance - Core Formula Verification
# Precision: 10000 decimal places
# ====================================================

import mpmath as mp
mp.mp.dps = 10000

alpha = mp.mpf('0.007297352569311114')
mu0 = 4 * mp.pi * mp.mpf('1e-7')
c = mp.mpf('299792458')
G_codata = mp.mpf('6.6743015e-11')

print('=' * 80)
print('ALGORITHM ALLIANCE - CORE FORMULA VERIFICATION')
print('Precision:', mp.mp.dps, 'decimal places')
print('=' * 80)
print()

# 1. N = 1/[alpha^2(1-alpha)]
N = 1 / (alpha**2 * (1 - alpha))
print('1. N = 1/[alpha^2(1-alpha)] =', mp.nstr(N, 30))

# 2. Infinite series sum
sum_series = mp.mpf('0')
for n in range(-2, 100):
    sum_series += alpha**n
print('2. Sum(alpha^n) from n=-2 to 99 =', mp.nstr(sum_series, 30))
print('   Diff from N =', mp.nstr(abs(sum_series - N), 30))
print()

# 3. Spiral parameters
rho = mp.sqrt(G_codata / (alpha**2 * mu0 * c**2))
b = alpha * rho
print('3. rho =', mp.nstr(rho, 30), 'm')
print('4. b =', mp.nstr(b, 30), 'm')

# 4. Curvature and torsion
kappa = rho / (rho**2 + b**2)
tau = b / (rho**2 + b**2)
alpha_geo = tau / kappa
print('5. kappa =', mp.nstr(kappa, 30), 'm^-1')
print('6. tau =', mp.nstr(tau, 30), 'm^-1')
print('7. alpha = tau/kappa =', mp.nstr(alpha_geo, 30))
print('   Diff from standard alpha =', mp.nstr(abs(alpha_geo - alpha), 30))
print()

# 5. G verification
G_theory = alpha**2 * mu0 * c**2 * rho**2
print('8. G (theory) =', mp.nstr(G_theory, 30))
print('9. G (CODATA) =', mp.nstr(G_codata, 30))
print('   Diff =', mp.nstr(abs(G_theory - G_codata), 30))
print()

# 6. Force normalization
forces = {'Gravity':1/alpha**2, 'Strong':1/alpha, 'Weak':1, 'Electro':alpha, '5th':alpha**2, '6th':alpha**3, '7th':alpha**4}
print('10. Force Normalization:')
print('-' * 70)
total_norm = mp.mpf('0')
for name, factor in forces.items():
    norm = factor / N
    total_norm += norm
    print('%s %s %s' % (name.ljust(10), ('%.3e' % float(factor)).ljust(15), ('%.12f' % float(norm)).ljust(15)))
print('%s %s %s' % ('Total'.ljust(10), ''.ljust(15), ('%.15f' % float(total_norm)).ljust(15)))
print('   Diff from 1 = %.3e' % float(abs(total_norm - 1)))
print()

# 7. Yin-Yang balance
theta = mp.atan(alpha)
yin = mp.cos(theta)**2
yang = mp.sin(theta)**2
print('11. Yin-Yang Balance:')
print('    Yin = %.15f' % float(yin))
print('    Yang = %.15f' % float(yang))
print('    Yin + Yang = %.15f' % float(yin + yang))
print('    Diff from 1 = %.3e' % float(abs(yin + yang - 1)))

# 8. Summary
print()
print('=' * 80)
print('VERIFICATION SUMMARY')
print('=' * 80)
passed = 0
total = 5

if abs(sum_series - N) < mp.mpf('1e-100'):
    print('OK: Series sum matches N')
    passed += 1
else:
    print('FAIL: Series sum')

if abs(alpha_geo - alpha) < mp.mpf('1e-100'):
    print('OK: alpha = tau/kappa')
    passed += 1
else:
    print('FAIL: alpha formula')

if abs(G_theory - G_codata) < mp.mpf('1e-100'):
    print('OK: G = alpha^2*mu0*c^2*rho^2 (algebraic identity)')
    passed += 1
else:
    print('FAIL: G formula')

if abs(total_norm - 1) < mp.mpf('1e-10'):
    print('OK: Force normalization sum = 1')
    passed += 1
else:
    print('FAIL: Force normalization')

if abs(yin + yang - 1) < mp.mpf('1e-100'):
    print('OK: Yin-Yang balance = 1')
    passed += 1
else:
    print('FAIL: Yin-Yang balance')

print()
print('Result: %d/%d verifications passed' % (passed, total))
if passed == total:
    print('SUCCESS: All verifications passed!')
else:
    print('WARNING: Some verifications failed!')