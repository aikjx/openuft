#!/usr/bin/env python3
"""Create publication-oriented PNGs from generated CSV. Optional matplotlib.
Core calculations/tests run without plotting dependencies.
"""
from pathlib import Path
import csv
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent

def read(name):
    with (P/'results'/name).open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))

crit=read('critical_sensitivity.csv')
x=[float(a['distance_from_critical']) for a in crit]
y=[float(a['radion_range_L0']) for a in crit]
plt.figure(figsize=(8,4.8))
plt.loglog(x,y,marker='o')
plt.xlabel('Fractional distance to critical point, delta')
plt.ylabel('Radion range / reference length L0')
plt.title('ROOT V147: a light radion near the stability boundary')
plt.grid(True,alpha=.25)
plt.tight_layout();plt.savefig(P/'figures'/'near_critical_range.png',dpi=160);plt.close()

prof=read('conditional_radion_force.csv')
x=[float(a['r_over_lambda']) for a in prof]
y=[float(a['force_fraction']) for a in prof]
plt.figure(figsize=(8,4.8))
plt.plot(x,y)
plt.xlabel('Separation / Yukawa range')
plt.ylabel('Additional force / bare tensor Newton force')
plt.title('Conditional brane-matter radion: alpha = 1/2')
plt.ylim(0,.54)
plt.grid(True,alpha=.25)
plt.tight_layout();plt.savefig(P/'figures'/'conditional_fifth_force.png',dpi=160);plt.close()

vac=read('flux_vacuum_scan.csv')
n=[int(a['n']) for a in vac if a['radius_min']]
r=[float(a['radius_min']) for a in vac if a['radius_min']]
plt.figure(figsize=(8,4.8))
plt.scatter(n,r,s=80)
plt.xlabel('Signed integer flux n')
plt.ylabel('Homogeneous stable radius / L0')
plt.title('Flux sign degeneracy: n and -n stabilize identically')
plt.xticks(range(-4,5))
plt.grid(True,alpha=.25)
plt.tight_layout();plt.savefig(P/'figures'/'flux_sign_degeneracy.png',dpi=160);plt.close()
print('Three charts saved to figures/')
