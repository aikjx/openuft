#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sympy as sp
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
sp.Number._prec = 100

alpha_codata = sp.Float(1/137.035999084, 100)
theta_rad = sp.atan(alpha_codata)
theta_deg = sp.N(sp.deg(theta_rad), 100)

tan_theta = sp.N(sp.tan(theta_rad), 100)
sin_theta = sp.N(sp.sin(theta_rad), 100)
cos_theta = sp.N(sp.cos(theta_rad), 100)

alpha_geo = tan_theta
delta_alpha = sp.N(alpha_geo - alpha_codata, 100)

output_path = os.path.join(script_dir, 'precision_results_optimized.txt')
with open(output_path, 'w', encoding='utf-8') as out:
    out.write('alpha_CODATA = ' + str(alpha_codata) + '\n')
    out.write('theta_deg = ' + str(theta_deg) + '\n')
    out.write('alpha_geo = tan(theta) = ' + str(alpha_geo) + '\n')
    out.write('delta_alpha = alpha_geo - alpha_CODATA = ' + str(delta_alpha) + '\n')
    out.write('sin_theta = ' + str(sin_theta) + '\n')
    out.write('cos_theta = ' + str(cos_theta) + '\n')

print('Precision calculation completed. Results saved.')