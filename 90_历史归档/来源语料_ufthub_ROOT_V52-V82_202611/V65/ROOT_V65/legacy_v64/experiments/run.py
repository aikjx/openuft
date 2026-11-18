"""Reproduce all V64 plots/data; Python stdlib; matplotlib optional.
All examples are *toy model calculations* or *reverse fits*, NOT observations.
"""
import sys, math, csv, json, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src import root_v64 as p
O=ROOT/'data'; R=ROOT/'results'
O.mkdir(exist_ok=True);R.mkdir(exist_ok=True)

def output_csv(name,fields,rows):
 with (O/name).open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.writer(f);w.writerow(fields);w.writerows(rows)

mode=p.HelicalKGMode(a=1,k=.75,mu=.4,amplitude=1)
radii, fractions,energy=p.integrate_radial(mode,4000)
E_exact=mode.energy_per_length_exact()
assert abs(energy/E_exact-1)<3e-7
# Input cylindrical line-mass 10 kg/m; a=0.1m. Energy distribution gives dimensionless mass fractions only.
a_phys=.1;line_mass=10.
field_rows=[]
for j in range(0,len(radii),10):
 rr=radii[j]
 f=fractions[j]
 g=p.line_gravity(line_mass, max(.00001,rr*a_phys),f)
 field_rows.append((round(rr,6),round(rr*a_phys,7),f,mode.energy_density(rr),g))
output_csv('helical_KG_energy_and_line_gravity_TOY.csv', ['r_over_a','radius_m','enclosed_energy_fraction','T00_natural_arbitrary_amplitude','g_m_s2_G_INPUT_line_mass_INPUT'],field_rows)

helix_rows=[]
for a in range(0,91,2):
 h=p.helix(1.,a,1.0) # speed=1 for nondimensional plot, no massive particle worldline
 helix_rows.append((a,h.tangential_speed,h.axial_speed,h.curvature,h.torsion,h.centripetal_accel))
output_csv('helix_geometry_MATH.csv',['lambda_deg','v_phi_over_v','v_z_over_v','curvature_inv_R','torsion_inv_R','acceleration_v2_over_R'],helix_rows)

lp=p.planck_length(); inverse_rows=[]
for N in (1,4,16,64):
 for x in (.3,.5,1,2,4):
  inverse=p.inverse_G_induced(N,lp*x)
  inverse_rows.append((N,x,1/(inverse*p.G_OBS),p.inverse_fit_length(N)/lp))
output_csv('induced_gravity_SCHEME_DEPENDENT.csv',['N','ell_over_lPlanck_G_OBS_INPUT','G_ind_over_G_OBS','inverse_fit_ell_over_lPlanck_NOT_PREDICTION'],inverse_rows)

mass_rows=[]
for i in range(0,101,2):
 mu=i/25
 mass_rows.append((mu,p.proper_time_factor(mu)))
output_csv('proper_time_cutoff_mass_factor_TOY.csv',['mu','F_mu'],mass_rows)

yuk_rows=[]
for t in range(1,101):
 u=t/10
 yuk_rows.append((u,p.yukawa_g_ratio(.1,u,1),p.yukawa_g_ratio(-.1,u,1)))
output_csv('yukawa_DEFINITION_NOT_NEW_PREDICTION.csv',['r_over_range','delta_g_div_g_alpha_plus_0p1','delta_g_div_g_alpha_minus_0p1'],yuk_rows)

summary={
 'project':'ROOT V64 - conditional math and audit only','G_observed_CODATA_2022_m3_kg_s2':p.G_OBS,
 'planck_length_m_DEFINES_G_not_prediction':lp,
 'inverse_fit_minimal_ell_m_NOT_prediction':p.inverse_fit_length(),
 'inverse_fit_minimal_ell_over_planck':p.inverse_fit_length()/lp,
 'helical_wave_cavity':{'n':1,'radius_natural':mode.a,'k_natural':mode.k,'mu_natural':mode.mu,
     'q_natural':mode.q,'omega_natural':mode.omega,'axial_group_v_over_c':mode.axial_group_speed,
     'analytic_energy_per_length_natural':E_exact,'integrated_energy_per_length_natural':energy,
     'integration_relative_error':abs(energy/E_exact-1)},
 'cylindrical_gravity_TOY':{'chosen_mass_per_length_kg_m':line_mass,'chosen_radius_m':a_phys,
     'g_outside_at_r_0p3_m_m_s2':p.line_gravity(line_mass,.3),
     'G_is_observational_input':True,'geometry_infinite_cylinder':True},
 'mass_factor_mu1':p.proper_time_factor(1),
 'alpha_old_guess':p.bad_alpha_guess(),'alpha_CODATA_2022':p.ALPHA_OBS,
 'alpha_relative_error':p.bad_alpha_guess()/p.ALPHA_OBS-1,
 'proton_mass_guess_56pi':p.bad_mass_ratio_guess(),
 'meaning':'These are mathematical/model checks. No proof of a unified interaction or prediction of Newton G.'}
(R/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')

try:
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 def plot_save(title,x,y,xlabel,ylabel,filename):
  plt.figure(figsize=(8,4.5));plt.plot(x,y);plt.grid(alpha=.25);plt.title(title);plt.xlabel(xlabel);plt.ylabel(ylabel);plt.tight_layout();plt.savefig(R/filename,dpi=160);plt.close()
 plot_save('Conditional KG helical mode: radial energy density', [r for r in radii[::4]],[mode.energy_density(r) for r in radii[::4]],'radius / cylinder radius','T00 (natural units, arbitrary amplitude)','wave_energy.png')
 plot_save('Helical motion: curvature and torsion', [r[0] for r in helix_rows],[r[3] for r in helix_rows],'helix angle (degree)','curvature, R=1','helix_curvature.png')
 plt.figure(figsize=(8,4.5));plt.plot([r[0] for r in helix_rows],[r[3] for r in helix_rows],label='curvature R=1');plt.plot([r[0] for r in helix_rows],[r[4] for r in helix_rows],label='torsion R=1');plt.legend();plt.grid(alpha=.25);plt.xlabel('angle degree');plt.title('Frenet curve geometry; no field law implied');plt.tight_layout();plt.savefig(R/'helix_geometry.png',dpi=160);plt.close()
 plot_save('Proper-time mass threshold F(mu)',[r[0] for r in mass_rows],[r[1] for r in mass_rows],'mu=m c ell / hbar','F(mu)','mass_threshold.png')
 plot_save('Toy Yukawa modification; not derived from helix',[r[0] for r in yuk_rows],[r[1] for r in yuk_rows],'distance/range','delta g / gN','yukawa_toy.png')
 plt.figure(figsize=(8,4.5));plt.plot([r[1] for r in field_rows],[r[4] for r in field_rows]);plt.grid(alpha=.25);plt.xlabel('radius (m)');plt.ylabel('g (m/s²)');plt.title('Externally normalized helical KG density; G input');plt.tight_layout();plt.savefig(R/'line_gravity.png',dpi=160);plt.close()
except ImportError:
 (R/'plots_note.txt').write_text('matplotlib not installed; CSV and JSON are complete. PNG plot generation skipped.',encoding='utf-8')

print(json.dumps(summary,indent=2,ensure_ascii=False))
