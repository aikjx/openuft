from pathlib import Path
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
BASE=Path(__file__).resolve().parents[1]
FIG=BASE/'figures';FIG.mkdir(exist_ok=True)
with (BASE/'results'/'flux_index.csv').open() as f:r=list(csv.DictReader(f))
x=[int(z['flux']) for z in r]
y=[int(float(z['index'])) for z in r]
c=[int(z['zero_mode_count']) for z in r]
fig,ax=plt.subplots(figsize=(8,4.5))
ax.plot(x,[-i for i in y],'o-',label='Negative lattice overlap index')
ax.plot(x,x,'k--',linewidth=1,label='Input Chern number')
ax.set(xlabel='U(1) flux N',ylabel='Index / integer',title='Lattice index matches topology (orientation adjusted)')
ax.grid(alpha=.25);ax.legend();fig.tight_layout();fig.savefig(FIG/'01_flux_index.png',dpi=165);plt.close(fig)
fig,ax=plt.subplots(figsize=(8,4.5))
ax.bar(x,c)
ax.set(xlabel='Flux N',ylabel='Total exact overlap zero modes',title='A nonzero topological index protects chiral modes')
ax.set_xticks(x);fig.tight_layout();fig.savefig(FIG/'02_chiral_zero_modes.png',dpi=165);plt.close(fig)
with (BASE/'results'/'gauge_deformation.csv').open() as f:d=list(csv.DictReader(f))
sc=[float(z['phase_noise_std_rad']) for z in d]
om=[float(z['matches_nominal_flux_and_index'])/float(z['repetitions']) for z in d]
ma=[float(z['lattice_index_equals_minus_chern'])/float(z['repetitions']) for z in d]
fig,ax=plt.subplots(figsize=(8,4.5))
ax.plot(sc,om,'o-',label='Nominal flux and lattice index both unchanged')
ax.plot(sc,ma,'s--',label='Measured Chern and index agree')
ax.set(xlabel='Random link phase noise (radians)',ylabel='Fraction',ylim=(-.05,1.05),title='Topological robustness within lattice admissibility')
ax.grid(alpha=.25);ax.legend();fig.tight_layout();fig.savefig(FIG/'03_gauge_deformation.png',dpi=165);plt.close(fig)
