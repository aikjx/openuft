from __future__ import annotations
import json,math
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sys import path
R=Path(__file__).resolve().parents[1]
path.insert(0,str(R))
from src.physics import Rig,common_amplitude,yukawa_amplitude_per_alpha,source_geometry_uncertainty
j=json.loads((R/'results/numerical_summary.json').read_text(encoding='utf-8'))
rig=Rig()
xs=[.26+k*1.4/199 for k in range(200)]
fig,ax=plt.subplots(figsize=(8,4.5));ax.plot(xs,[common_amplitude(rig,x)/1e-9 for x in xs],label='Newton common odd signal')
ax.plot(xs,[(common_amplitude(rig,x)+.08*yukawa_amplitude_per_alpha(rig,x,.25))/1e-9 for x in xs],label='Newton + synthetic alpha=0.08',linestyle='--')
ax.set_yscale('log');ax.set_xlabel('Source center distance d (m)');ax.set_ylabel('Common signal amplitude (nm/s^2)');ax.legend();ax.grid(alpha=.25);fig.tight_layout();fig.savefig(R/'results/distance_curves.png',dpi=170);plt.close(fig)
fig,ax=plt.subplots(figsize=(8,4.5));
for sc,marker in [('NULL','o'),('INJECTED','s'),('CONFOUNDED','^')]:
    v=j['scenarios'][sc]['points'];
    ax.errorbar([x['distance_m'] for x in v],[x['signal']/1e-9 for x in v],yerr=[x['sem']/1e-9 for x in v],label='SYNTHETIC '+sc,marker=marker,linestyle='none',capsize=3)
ax.plot(xs,[common_amplitude(rig,x)/1e-9 for x in xs],label='Newton prediction',linestyle='--')
ax.set_yscale('log');ax.set_xlabel('Distance (m)');ax.set_ylabel('SOURCE-SHAM (nm/s^2)');ax.grid(alpha=.25);ax.legend(fontsize=8);fig.tight_layout();fig.savefig(R/'results/synthetic_distance_fit.png',dpi=170);plt.close(fig)
fig,ax=plt.subplots(figsize=(8,4.5));
sc=['NULL','INJECTED','CONFOUNDED'];m=[j['scenarios'][k]['fit']['newton_yukawa_offset'] for k in sc]
ax.errorbar(range(3),[z['alpha_yukawa'] for z in m],yerr=[z['alpha_se'] for z in m],marker='o',capsize=6,linestyle='none')
ax.axhline(0,linestyle='--');ax.axhline(.08,linestyle=':');ax.set_xticks(range(3),sc)
ax.set_ylabel('Fitted alpha (1 sigma, formal only)');ax.set_title('CONFOUNDED is 0 true new force, yet fitted positive');ax.grid(alpha=.25);fig.tight_layout();fig.savefig(R/'results/false_positive_counterexample.png',dpi=170);plt.close(fig)
fig,ax=plt.subplots(figsize=(8,4.5));
lams=[.05+k*8/250 for k in range(250)]
ratio=[yukawa_amplitude_per_alpha(rig,.5,v)/common_amplitude(rig,.5) for v in lams]
ax.plot(lams,ratio);ax.axhline(1,linestyle='--');ax.set_xlabel('Assumed force range lambda (m)');ax.set_ylabel('Yukawa basis / Newton basis (at d=0.5m)')
ax.set_title('Long-range model becomes degenerate with Newton scaling');ax.grid(alpha=.25);fig.tight_layout();fig.savefig(R/'results/long_range_degeneracy.png',dpi=170);plt.close(fig)
fig,ax=plt.subplots(figsize=(8,4.5));
d=.5;b=source_geometry_uncertainty(rig,d)
items={k:abs(v) for k,v in b['terms_m_s2'].items()}
ax.barh(list(items),[v/1e-9 for v in items.values()]);ax.set_xlabel('1-sigma example contribution (nm/s^2)');ax.set_title('Illustrative budget only; not an instrument measurement');fig.tight_layout();fig.savefig(R/'results/uncertainty_budget.png',dpi=170);plt.close(fig)
print('Generated 5 PNG plots')
