"""Reproduce all precomputed numeric results without a network connection."""
import csv,json,math
from pathlib import Path
from src import core as p
root=Path(__file__).resolve().parents[1]
out=root/'results'; out.mkdir(exist_ok=True)
U=p.magnetic_energy(10,1)
N={'version':'ROOT V78','date':'2026-11-17','reference':'CODATA 2022 G, fixed SI c, approximate vacuum mu0',
   'G_is_input_not_prediction':True,
   'G':p.G_CODATA,'G_uncertainty':p.G_STANDARD_UNCERTAINTY,'c':p.C,
   'Z':p.z_from_g(),'u_Z':p.G_STANDARD_UNCERTAINTY*p.C/2,
   'magnetic_energy_10T_1m3_J':U,'magnetic_equivalent_mass_kg':p.em_equivalent_mass(U),
   'added_energy_far_field_monopole_at_10m_m_s2':p.far_field_monopole_g(U,10),
   'field_induced_E_energy_fraction_50Hz_r1m':p.induction_energy_ratio_sphere(2*math.pi*50,1),
   'laboratory_1mm_redshift':p.gravitational_redshift_small_height(9.81,.001),
   'photon_wave_null_invariants':p.wave_invariants((1e6,0,0),(0,1e6/p.C,0)),
   'plane_wave_energy_density_J_m3':p.em_energy_density((1e6,0,0),(0,1e6/p.C,0)),
   'synthetic_regression':p.experiment_synthetic_beta(),
   'source_geometry_yukawa':{'alpha':1,'R':p.EARTH_R,'lambda':1e6,'r':p.EARTH_R,
        'point':p.yukawa_ratio_point(1,p.EARTH_R,1e6),
        'sphere':p.yukawa_ratio_sphere(1,p.EARTH_R,p.EARTH_R,1e6)},
   'closed_energy_ledger_delta_joule':p.ClosedEnergyLedger(100e6,25e6,1e6).check()[2],
   'conclusion':'Corrected source bookkeeping and operational null experiments; gravity constant origin still open.'}
(out/'numerical_summary.json').write_text(json.dumps(N,indent=2,ensure_ascii=False),encoding='utf8')
with (root/'data'/'magnetic_field_scan.csv').open('w',newline='',encoding='utf8') as f:
    w=csv.writer(f);w.writerow(['B_T','energy_per_m3_J','equiv_mass_kg','far_field_g_at_10m_m_s2'])
    for j in range(0,101):
        B=j/2;energy=p.magnetic_energy(B,1)
        w.writerow([B,energy,p.em_equivalent_mass(energy),p.far_field_monopole_g(energy,10)])
with (root/'data'/'yukawa_finite_source_scan.csv').open('w',newline='',encoding='utf8') as f:
    w=csv.writer(f);w.writerow(['range_km','point_source_ratio_alpha1','uniform_earth_sphere_ratio_alpha1','correction_factor'])
    for i in range(1,101):
        lam=10**(2+(i-1)*4/99)*1000
        a=p.yukawa_ratio_point(1,p.EARTH_R,lam)
        b=p.yukawa_ratio_sphere(1,p.EARTH_R,p.EARTH_R,lam)
        w.writerow([lam/1000,a,b,(b/a if a else None)])
with (root/'data'/'orientation_energy.csv').open('w',newline='',encoding='utf8') as f:
    w=csv.writer(f);w.writerow(['angle_deg','u_individual_sum_J_m3','cross_J_m3','u_total_J_m3'])
    for j in range(0,181):
        E1=(1e6,0,0); rad=math.radians(j);E2=(1e6*math.cos(rad),1e6*math.sin(rad),0)
        w.writerow([j,2*p.elec_energy_density(1e6),p.e_cross_energy(E1,E2),p.em_energy_density(p.add(E1,E2),(0,0,0))])
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(8,4.8)); bs=[i/2 for i in range(101)]
    ax.plot(bs,[p.far_field_monopole_g(p.magnetic_energy(b,1),10) for b in bs]);ax.set_xlabel('B (T)');ax.set_ylabel('Far-field g estimate (m/s^2)');ax.set_title('External added energy only; not a complete apparatus');fig.tight_layout();fig.savefig(out/'added_magnetic_energy_g.png',dpi=160);plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,4.8));ll=[10**(2+i*4/100)*1000 for i in range(101)]
    ax.semilogx([x/1000 for x in ll],[p.yukawa_ratio_sphere(1,p.EARTH_R,p.EARTH_R,x) for x in ll],label='Uniform sphere')
    ax.semilogx([x/1000 for x in ll],[p.yukawa_ratio_point(1,p.EARTH_R,x) for x in ll],label='Point source')
    ax.legend();ax.set_xlabel('Yukawa range (km)');ax.set_ylabel('Delta g / g_N for alpha=1');ax.set_title('Hypothetical force, not observed');fig.tight_layout();fig.savefig(out/'yukawa_source_geometry.png',dpi=160);plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,4.8));theta=[math.radians(i) for i in range(181)]
    ax.plot(range(181),[2*p.elec_energy_density(1e6)+p.EPS0*1e12*math.cos(x) for x in theta]);ax.set_xlabel('E1 E2 angle (degrees)');ax.set_ylabel('Total E energy density (J/m^3)');ax.set_title('Exact quadratic cross term');fig.tight_layout();fig.savefig(out/'electric_cross_angle.png',dpi=160);plt.close(fig)
    print('Generated 3 PNG figures.')
except ImportError:
    print('SKIP plots: matplotlib absent; numerical files generated')
print('Wrote results/numerical_summary.json and 3 CSV sweeps')
