import sys,csv,json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.gravitylab import G,Rig,theoretical_signals,field_energy_joule
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
except ImportError:
    print('matplotlib unavailable; skipping optional PNG plots')
    sys.exit(0)

def readcsv(name):
    with (ROOT/'data'/name).open('r',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
r=Rig()
dist=[.4+i*.01 for i in range(161)]
y=[theoretical_signals(Rig(distance_m=d))['common_odd_amplitude'] for d in dist]
plt.figure(figsize=(9,5));plt.plot(dist,y);plt.xlabel('Source center distance (m)');plt.ylabel('Common odd gravity amplitude (m/s^2)');plt.title('ROOT V83: predicted movable mass signal');plt.grid(alpha=.3);plt.tight_layout();plt.savefig(ROOT/'results'/'mass_distance_curve.png',dpi=150);plt.close()
rows=readcsv('source_mass_SYNTHETIC.csv');n=80
plt.figure(figsize=(9,5));plt.plot([int(z['index']) for z in rows[:n]],[float(z['common_m_s2']) for z in rows[:n]],label='Synthetic observed common channel');plt.step([int(z['index']) for z in rows[:n]],[int(z['side'])*theoretical_signals(r)['common_odd_amplitude'] for z in rows[:n]],where='mid',label='Ideal gravitational part');plt.xlabel('Sample index');plt.ylabel('m/s^2');plt.title('ROOT V83: synthetic ABBA signal and model');plt.legend();plt.grid(alpha=.3);plt.tight_layout();plt.savefig(ROOT/'results'/'abba_synthetic.png',dpi=150);plt.close()
B=[i*.01 for i in range(201)];U=[field_energy_joule(b,.001) for b in B]
plt.figure(figsize=(9,5));plt.plot(B,U);plt.xlabel('Ideal B (T)');plt.ylabel('Ideal stored magnetic energy (J)');plt.title('ROOT V83: electromagnetic energy bookkeeping');plt.grid(alpha=.3);plt.tight_layout();plt.savefig(ROOT/'results'/'em_energy_curve.png',dpi=150);plt.close()
print('3 plots created')
