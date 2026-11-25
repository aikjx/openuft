"""Deterministic illustrative geometry figures and metadata (NOT observed data)."""
from pathlib import Path
import sys, math, json, csv
import numpy as np
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from root_v152.core import (vector_phase,tensor_phase,helical_geometry,dimensional_audit,
 simple_gravitational_wave,spin2_tt_amplitude,linearized_riemann,
 linearized_einstein,spin2_gauge_shift,photon_amplitude,field_strength_fourier)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

r=ROOT/'results'; f=ROOT/'figures';r.mkdir(exist_ok=True);f.mkdir(exist_ok=True)
angles=np.linspace(-math.pi,math.pi,401)
rows=[]
for angle in angles:
    v_plus, v_minus=vector_phase([0,0,1],float(angle))
    t_plus, t_minus=tensor_phase([0,0,1],float(angle))
    rows.append({'angle_rad':float(angle),'spin1_real':float(v_plus.real),'spin1_imag':float(v_plus.imag),
      'spin2_real':float(t_plus.real),'spin2_imag':float(t_plus.imag),
      'spin1_phase_error':float(abs(v_plus-np.exp(-1j*angle))),
      'spin2_phase_error':float(abs(t_plus-np.exp(-2j*angle)))})
with (r/'rotation_scan.csv').open('w',newline='',encoding='utf-8') as out:
    writer=csv.DictWriter(out,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)

plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':140})
fig, ax=plt.subplots(figsize=(8.4,4.5))
ax.plot(angles,np.array([p['spin1_real'] for p in rows]),label='helicity +1: Re phase')
ax.plot(angles,np.array([p['spin2_real'] for p in rows]),label='helicity +2: Re phase')
ax.set(xlabel='Rotation around propagation axis (radians)',ylabel='Real part of rotation eigenvalue',title='One orthogonal frame, different helicities')
ax.grid(alpha=.2);ax.legend(loc='lower left');fig.tight_layout();fig.savefig(f/'helicity_one_vs_two.png');plt.close(fig)

fig,ax=plt.subplots(figsize=(8.4,4.5))
ax.plot(angles,np.array([p['spin1_phase_error'] for p in rows]),label='vector helicity error')
ax.plot(angles,np.array([p['spin2_phase_error'] for p in rows]),label='tensor helicity error')
ax.set(xlabel='Rotation angle (radians)',ylabel='Absolute complex error',title='Numerical precision of helicity rotation identities')
ax.grid(alpha=.2);ax.legend();fig.tight_layout();fig.savefig(f/'rotation_identity_residuals.png');plt.close(fig)

# Transverse ring under tensor + and cross perturbations (rescaled schematic h=0.2)
phases=[0,math.pi/4,math.pi/2]
t=np.linspace(0,2*math.pi,180)
ring=np.stack((np.cos(t),np.sin(t)))
fig,axes=plt.subplots(1,3,figsize=(10,3.7))
for i,(ax,phase) in enumerate(zip(axes,phases)):
    tensor=np.array([[math.cos(phase),math.sin(phase)],[math.sin(phase),-math.cos(phase)]])
    deformation=(np.eye(2)+0.12*tensor)@ring
    ax.plot(ring[0],ring[1],'--',linewidth=1,label='undeformed')
    ax.plot(deformation[0],deformation[1],linewidth=2,label='tensor wave')
    ax.set_aspect('equal');ax.set_xlim(-1.3,1.3);ax.set_ylim(-1.3,1.3)
    ax.set_title('phase = '+str(round(phase,2)))
    ax.set_xticks([]);ax.set_yticks([])
axes[0].legend(loc='lower left',fontsize=7)
fig.suptitle('Spin-2 transverse, trace-free distortion (amplified schematic)');fig.tight_layout();fig.savefig(f/'gravitational_wave_tt_ring.png');plt.close(fig)

k,h=spin2_tt_amplitude(frequency=2.0)
xi=np.array([.1,-.2,.3,.4])
R=linearized_riemann(k,h)
Rg=linearized_riemann(k,h+spin2_gauge_shift(k,xi))
kA,eps=photon_amplitude(2.0)
F=field_strength_fourier(kA,eps)
Fg=field_strength_fourier(kA,eps+.7*kA)
results={
 'version':'ROOT V152',
 'interpretation':'All results are mathematics/model consistency checks, not evidence for unified forces.',
 'c_equals_one':True,'hbar_equals_one':False,'G_equals_one':False,
 'geometry':helical_geometry(.6,1,.8),
 'phase_error_max_spin1':max(x['spin1_phase_error'] for x in rows),
 'phase_error_max_spin2':max(x['spin2_phase_error'] for x in rows),
 'maxwell_gauge_field_strength_error':float(np.max(np.abs(F-Fg))),
 'spin2_riemann_gauge_error':float(np.max(np.abs(R-Rg))),
 'spin2_Einstein_equation_residual':float(np.max(np.abs(linearized_einstein(k,h)))),
 'gravitational_wave_example':simple_gravitational_wave(),
 'dimensional_audit':dimensional_audit(),
 'coupling_underdetermination_demo': {'g_a':.1,'g_b':.3,'same_free_field_equations':True,
    'source_response_g_squared_ratio':(.3/.1)**2,
    'interpretation':'Coupling is undetermined by polarization geometry.'},
 'limitations':['Spin-1 and spin-2 fields are independently specified','No derivation of standard-model gauge group or its coupling constants','No particle-spectrum/chirality derivation','No experimental validation of ROOT hypothesis']}
(r/'metrics.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Generated deterministic metrics, 401-angle CSV scan, and 3 plots.')
