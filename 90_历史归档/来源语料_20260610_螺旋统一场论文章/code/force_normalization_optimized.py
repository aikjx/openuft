#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sympy as sp
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
sp.Number._prec = 100

alpha = sp.Float(1/137.035999084, 100)
theta_rad = sp.atan(alpha)
theta_deg = sp.N(sp.deg(theta_rad), 100)

cos_theta = sp.N(sp.cos(theta_rad), 100)
sin_theta = sp.N(sp.sin(theta_rad), 100)
tan_theta = sp.N(sp.tan(theta_rad), 100)

F_gravity_factor = sp.N(1 / alpha**2, 100)
F_electric_factor = alpha
F_strong_factor = sp.N(1 / alpha, 100)
F_weak_factor = sp.Float(1, 100)

N = sp.N(F_gravity_factor + F_electric_factor + F_strong_factor + F_weak_factor, 100)

F_gravity_norm = sp.N(F_gravity_factor / N, 100)
F_electric_norm = sp.N(F_electric_factor / N, 100)
F_strong_norm = sp.N(F_strong_factor / N, 100)
F_weak_norm = sp.N(F_weak_factor / N, 100)

total_norm = sp.N(F_gravity_norm + F_electric_norm + F_strong_norm + F_weak_norm, 100)

output_path = os.path.join(script_dir, 'force_normalization_results_optimized.txt')
with open(output_path, 'w', encoding='utf-8') as out:
    out.write('alpha = ' + str(alpha) + '\n')
    out.write('theta_deg = ' + str(theta_deg) + '\n')
    out.write('tan_theta = ' + str(tan_theta) + '\n')
    out.write('tan_theta - alpha = ' + str(sp.N(tan_theta - alpha, 100)) + '\n')
    out.write('total_norm = ' + str(total_norm) + '\n')
    out.write('F_gravity_norm = ' + str(F_gravity_norm) + '\n')
    out.write('F_electric_norm = ' + str(F_electric_norm) + '\n')
    out.write('F_strong_norm = ' + str(F_strong_norm) + '\n')
    out.write('F_weak_norm = ' + str(F_weak_norm) + '\n')

print('Force normalization completed. Results saved.')