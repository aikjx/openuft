from pathlib import Path
import sys, math, json, csv, hashlib, platform
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from root_v132 import *

root=Path(__file__).resolve().parents[1]
a=ALPHA_CODATA22
hax=helix_for_geo_alpha(a)
htr=helix_for_geo_alpha(a,mapping='transverse')
R=reduced_compton_si()
hC=helix_for_geo_alpha(a,radius=R)
Egeo=quantum_wire_geometric_potential(M_E_SI,hC.kappa)/E_CHARGE
result={
 'reference': 'CODATA 2022, c=1 only theoretical convention; SI c used for numeric conversion',
 'alpha_inverse': ALPHA_INV_CODATA22,
 'alpha_inverse_standard_uncertainty': ALPHA_INV_SIGMA,
 'alpha': a,
 'alpha_error_approx': ALPHA_INV_SIGMA/ALPHA_INV_CODATA22**2,
 'bohr_radius_m': bohr_radius_si(),
 'reduced_compton_m': R,
 'ratio_reduced_compton_to_bohr': R/bohr_radius_si(),
 'bohr_ionization_ev_ideal': bohr_energy_ev(),
 'electron_rest_energy_ev': M_E_SI*C_FOR_SI_CONVERSIONS**2/E_CHARGE,
 'h_planck_J_s': H_PLANCK_SI,
 'hbar_J_s': HBAR_SI,
 'geometry_candidates':{
  'alpha_equals_axial':{'radius_units_R':hax.radius,'omega_units_invR':hax.omega,'u':hax.axial_speed,'kappa_units_invR':hax.kappa,'tau_units_invR':hax.tau,'ratio_tau_kappa':hax.tau/hax.kappa,'pitch_over_2pi_radius':hax.pitch/(2*math.pi*hax.radius),'pitch_over_radius':hax.pitch/hax.radius,'integrated_torsion_per_turn':hax.torsion_per_turn},
  'alpha_equals_transverse':{'radius_units_R':htr.radius,'omega_units_invR':htr.omega,'u':htr.axial_speed,'kappa_units_invR':htr.kappa,'tau_units_invR':htr.tau,'ratio_tau_kappa':htr.tau/htr.kappa,'pitch_over_2pi_radius':htr.pitch/(2*math.pi*htr.radius),'pitch_over_radius':htr.pitch/htr.radius,'integrated_torsion_per_turn':htr.torsion_per_turn}
 },
 'boosted_example':{'beta':0.6,'u_original':hax.h_geo,'u_after_boost':hax.boosted_axial(0.6).h_geo},
 'constrained_wire_geometric_energy_ev_if_R_compton':Egeo,
 'geometric_energy_abs_over_bohr_binding':abs(Egeo)/bohr_energy_ev(),
 'independent_electromagnetic_definition_from_SI_constants':alpha_from_charge_si(),
 'alpha_qed_running_caution':'α(q²) runs with momentum transfer; a single fixed spatial pitch is insufficient',
 'status':'conditional identities and counterexamples; not a first principles derivation of h, hbar, alpha, mass or four-force unification'
}
(root/'data/calculation_results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')

with (root/'data/helix_parameter_scan.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['axial_fraction_u','transverse_fraction','kappa_R','tau_R','tau_over_kappa','integrated_torsion_one_turn_rad','ratio_pitch_2piR'])
 for u in np.linspace(-.95,.95,191):
  h=Helix(1,float(math.sqrt(1-u*u)),float(u))
  w.writerow([f'{u:.12g}',f'{h.normalized_curvature:.14g}',f'{h.kappa:.14g}',f'{h.tau:.14g}',f'{h.tau/h.kappa:.14g}',f'{h.torsion_per_turn:.14g}',f'{h.pitch/(2*math.pi*h.radius):.14g}'])

with (root/'data/boost_scan.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['boost_beta','u_original','u_transformed','alpha_reference'])
 for beta in np.linspace(-.9,.9,181):
  w.writerow([f'{beta:.8g}',f'{a:.16g}',f'{hax.boosted_axial(float(beta)).h_geo:.16g}',f'{a:.16g}'])

# Figure 1 dimensionless helix one turn in two conventions; axis ranges differ wildly
fig=plt.figure(figsize=(12,4.5))
for i,(name,h) in enumerate([('Candidate A: axial fraction = alpha',hax),('Candidate B: transverse fraction = alpha',htr)],start=1):
 ax=fig.add_subplot(1,2,i,projection='3d')
 phase=np.linspace(0,2*math.pi,500)
 x=np.cos(phase);y=np.sin(phase);z=h.axial_speed/h.omega*phase
 ax.plot(x,y,z,lw=2)
 ax.set_title(name,fontsize=10);ax.set_xlabel('x / R');ax.set_ylabel('y / R');ax.set_zlabel('z / R')
 ax.set_box_aspect((1,1,max(0.3, min(4,abs(z[-1])/2))))
fig.tight_layout();fig.savefig(root/'figures/two_equally_valid_alpha_embeddings.png',dpi=160);plt.close(fig)

fig,ax=plt.subplots(figsize=(9,4.5));bs=np.linspace(-.9,.9,501)
ax.plot(bs,[hax.boosted_axial(float(b)).h_geo for b in bs],label='Geometric axial fraction in boosted frame')
ax.axhline(a,linestyle='--',label='Measured alpha (fixed reference low-energy coupling)')
ax.set_xlabel('Lorentz boost beta along helix axis');ax.set_ylabel('Dimensionless fraction');ax.set_title('Direct identification h_geo = alpha fails boost covariance');ax.grid(alpha=.3);ax.legend(fontsize=9);fig.tight_layout();fig.savefig(root/'figures/lorentz_boost_counterexample.png',dpi=160);plt.close(fig)

fig,ax=plt.subplots(figsize=(8,4.5))
ax.bar(['Bohr ideal binding\n13.606 eV','Constrained quantum-wire\n|Vgeo| at R=Compton'],[bohr_energy_ev(),abs(Egeo)])
ax.set_yscale('log');ax.set_ylabel('Energy (eV, logarithmic)');ax.set_title('Model-dependent confinement: geometrical potential is NOT atomic binding');fig.tight_layout();fig.savefig(root/'figures/model_dependent_geometric_potential.png',dpi=160);plt.close(fig)

fig,ax=plt.subplots(figsize=(8,4.5))
rr=np.logspace(-3,3,300)
ax.plot(rr,[helix_for_geo_alpha(a,radius=float(r)).kappa for r in rr],label='curvature kappa')
ax.plot(rr,[helix_for_geo_alpha(a,radius=float(r)).tau for r in rr],label='torsion tau')
ax.set_xscale('log');ax.set_yscale('log');ax.set_xlabel('Helix radius R (arbitrary length units)');ax.set_ylabel('Inverse length');ax.set_title('Same alpha_geo for arbitrary length scale');ax.legend();ax.grid(alpha=.3);fig.tight_layout();fig.savefig(root/'figures/scale_degeneracy.png',dpi=160);plt.close(fig)
print(json.dumps({k:v for k,v in result.items() if k not in ['geometry_candidates']},indent=2,ensure_ascii=False))
