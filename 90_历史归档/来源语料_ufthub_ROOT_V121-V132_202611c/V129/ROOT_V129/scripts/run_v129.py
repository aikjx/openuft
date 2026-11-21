"""One-command reproducibility: algebra -> numeric data -> figures."""
import json, sys, pathlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from v129_core import audit_snapshot, electric_charges, kk_mass, rest_compton_radius, M_E

def main():
    result=ROOT/'results'; figdir=ROOT/'figures'
    result.mkdir(exist_ok=True); figdir.mkdir(exist_ok=True)
    obj=audit_snapshot()
    (result/'v129_exact_and_numeric.json').write_text(json.dumps(obj,indent=2,ensure_ascii=False),encoding='utf-8')
    import csv
    with (result/'mass_charge_spectrum_SYNTHETIC.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['KK_n','mass_in_electron_units','charge_in_e_units'])
        for n in range(0,251):
            w.writerow([n, kk_mass(n,rest_compton_radius())/M_E,n])
    ns=np.arange(0,251)
    fig,ax=plt.subplots(figsize=(7,4.5))
    ax.plot(ns,ns,label='toy KK mass / electron mass')
    ax.axhline(obj['muon_to_electron_mass_ratio'],ls='--',label='observed muon/electron mass ratio')
    ax.set(xlabel='mode number n (also toy electric charge in e units)',ylabel='mass / electron mass',title='ROOT V129: KK mass-charge locking (synthetic)')
    ax.legend();fig.tight_layout();fig.savefig(figdir/'KK_mass_charge_lock_SYNTHETIC.png',dpi=150);plt.close(fig)
    xs=np.linspace(-0.25,0.25,301)
    nu=np.array([float(electric_charges(str(float(z)))['neutrino']) for z in xs])
    e=np.array([float(electric_charges(str(float(z)))['electron']) for z in xs])
    fig,ax=plt.subplots(figsize=(7,4.5)); ax.plot(xs,nu,label='neutrino Q/e'); ax.plot(xs,e,label='electron Q/e');
    ax.axvline(0,ls='--');ax.set(xlabel='hypercharge ambiguity x (with right-handed neutrino)',ylabel='electric charge in e units',title='ROOT V129: anomaly-free family (synthetic algebra)')
    ax.legend();fig.tight_layout();fig.savefig(figdir/'hypercharge_family_SYNTHETIC.png',dpi=150);plt.close(fig)
    print(json.dumps(obj,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
