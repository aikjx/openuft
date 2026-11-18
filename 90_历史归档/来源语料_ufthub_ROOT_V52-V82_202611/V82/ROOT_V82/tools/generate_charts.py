from pathlib import Path
import sys, csv
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.gravitylab import G,C,MU0
root=Path(__file__).resolve().parents[1]
path=root/'data'/'mass_distance_curve.csv'
with path.open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['distance_m','mass_kg','switch_difference_m_s2']);
 for i in range(16,201):
  r=i/100;w.writerow([r,100,2*G*100/r**2])
with (root/'data'/'em_energy_scan.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['B_tesla','volume_m3','energy_J','equivalent_mass_kg','farfield_g_at_10m_m_s2'])
 for i in range(0,101):
  b=i/100;E=b*b*.001/(2*MU0);w.writerow([b,.001,E,E/C**2,G*E/C**2/100])
try:
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 ds=[i/100 for i in range(16,201)]
 plt.figure(figsize=(8,4.5));plt.plot(ds,[2*G*100/r**2 for r in ds]);plt.xlabel('distance r (m)');plt.ylabel('reversal difference (m/s²)');plt.title('100 kg spherical source-mass reversal: gravity modulation');plt.tight_layout();plt.savefig(root/'results'/'mass_reversal.png',dpi=150);plt.close()
 bs=[i/100 for i in range(101)]
 plt.figure(figsize=(8,4.5));plt.plot(bs,[G*b*b*.001/(2*MU0*C**2*100) for b in bs]);plt.xlabel('B (T)');plt.ylabel('far-field monopole estimate (m/s²)');plt.title('1 L magnetic field: illustrative GR mass monopole, r=10 m');plt.tight_layout();plt.savefig(root/'results'/'em_energy_monopole.png',dpi=150);plt.close()
 print('Charts saved')
except ImportError: print('matplotlib not installed; csv outputs saved, chart generation skipped')
