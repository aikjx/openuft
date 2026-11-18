from __future__ import annotations
import csv,json,math,pathlib,sys
P=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(P/'src'))
from microgravity import *
D=P/'data';R=P/'results';D.mkdir(exist_ok=True);R.mkdir(exist_ok=True)

def csv_write(path,headers,rows):
    with open(path,'w',encoding='utf-8-sig',newline='') as f:
        writer=csv.writer(f);writer.writerow(headers);writer.writerows(rows)

catalog=source_taxonomy()
csv_write(D/'31类微观现象与引力源归类.csv',['微观现象','分类','状态','计算与误判提示'],catalog)

angles=[]
for deg in range(0,181,5):
    rad=math.radians(deg);E1=(1e6,0.,0.);E2=(1e6*math.cos(rad),1e6*math.sin(rad),0.)
    z=em_superposition_identity(E1,(0.,0.,0.),E2,(0.,0.,0.))
    angles.append([deg,round(z['u1'],12),round(z['u2'],12),round(z['cross'],12),round(z['total'],12),round(z['total']/z['u1'],12)])
csv_write(D/'电场角度交叉能量扫描.csv',['夹角_deg','u1_Jm3','u2_Jm3','cross_Jm3','u_total_Jm3','相对于单场'],angles)

Bscan=[]
for b in [0,0.1,.5,1,2,5,10,15,20,30,50]:
    u=em_energy_density((0.,0.,0.),(0.,0.,b))
    U=4*math.pi/3*u
    Bscan.append([b,u,U,U/C**2,spherical_monopole_delta_g(U,2.)])
csv_write(D/'磁场能量与等效质量扫描.csv',['B_T','u_Jm3','sphere_1m_U_J','equivalent_mass_kg','ideal_monopole_delta_g_at_2m_ms2'],Bscan)

phases=[]
for deg in range(0,361,5):
    ph=math.radians(deg)
    phases.append([deg,quantum_two_level_energy(1,2,.2,math.pi/4,ph)])
csv_write(D/'两态量子相干的能量期望.csv',['相位_deg','玩具模型能量单位'],phases)

closed=[]
a=Ledger(1e9,0,0,0)
for fraction in [0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1.]:
    b=a.transfer_to_field(a.battery*fraction)
    closed.append([fraction,b.battery,b.field,b.total(),b.total()/C**2])
csv_write(D/'封闭电池场能转移账本.csv',['能量转移比例','battery_J','field_J','total_J','total_equivalent_mass_kg'],closed)

example_10t_1m3=em_energy_density((0,0,0),(0,0,10))
example_1mv=em_energy_density((1e6,0,0),(0,0,0))
example_sphere=sphere_field_energy(10,1)
summary={
 'release':'ROOT V76','disclaimer':'Numerical verification of established and explicitly conditional physics, not new experimental validation nor G prediction.',
 'CODATA_reference_year':2022,'constants':{'G_m3_kg_s2':G,'c_m_s':C,'eps0_F_m':EPS0,'mu0_H_m':MU0},
 'electric_1MV_m_1m3':{'energy_J':example_1mv,'equivalent_mass_kg':example_1mv/C**2},
 'magnetic_10T_1m3':{'energy_J':example_10t_1m3,'equivalent_mass_kg':example_10t_1m3/C**2},
 'magnetic_10T_ideal_sphere_radius1m':{'energy_J':example_sphere,'equivalent_mass_kg':example_sphere/C**2,'farfield_monopole_at_2m_ms2':spherical_monopole_delta_g(example_sphere,2)},
 'thermal_1kg_water_1K_illustrative':{'heat_capacity_assumed_J_kgK':4184,'energy_J':4184,'delta_mass_kg':4184/C**2},
 'deuteron_binding':{'binding_energy_MeV':DEUTERON_BINDING_MEV,'mass_defect_kg':nuclear_binding_mass_defect()},
 'redshift_1mm_standard_g':redshift_fraction(.001),
 'two_equal_opposing_photons_each_1J':{'single_photon_invariant_mass_kg':0,'two_photon_system_mass_kg':two_photon_invariant_mass(1,1,math.pi)},
 'cross_electric_E1_E2_1MV_m':{'parallel_total_Jm3':em_energy_density((2e6,0,0),(0,0,0)), 'perpendicular_total_Jm3':em_energy_density((1e6,1e6,0),(0,0,0)),'antiparallel_total_Jm3':0},
 'ledger_conservation':{'initial_J':a.total(),'final_J':a.transfer_to_field(1e8).total()},
 'taxonomy_count':len(catalog)
}
(R/'numerical_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
    plt.figure(figsize=(8,4.5));plt.plot([r[0] for r in angles],[r[4] for r in angles],label='Total energy density')
    plt.plot([r[0] for r in angles],[r[1]+r[2] for r in angles],'--',label='Sum without cross term')
    plt.xlabel('Angle (degrees)');plt.ylabel('Energy density (J/m3)');plt.title('Electrostatic superposition: cross energy');plt.legend();plt.grid(alpha=.25);plt.tight_layout();plt.savefig(R/'chart_01_electric_cross_terms.png',dpi=150);plt.close()
    plt.figure(figsize=(8,4.5));plt.plot([r[0] for r in Bscan],[r[3] for r in Bscan]);plt.xlabel('B (T)');plt.ylabel('Equivalent field energy / c² (kg)');plt.title('Ideal sphere radius 1 m: field energy equivalent mass');plt.grid(alpha=.25);plt.tight_layout();plt.savefig(R/'chart_02_magnetic_energy_mass.png',dpi=150);plt.close()
    plt.figure(figsize=(8,4.5));plt.plot([r[0] for r in phases],[r[1] for r in phases]);plt.xlabel('Relative phase (degrees)');plt.ylabel('Energy expectation (toy units)');plt.title('Quantum coherent two-level example (not extra gravity)');plt.grid(alpha=.25);plt.tight_layout();plt.savefig(R/'chart_03_quantum_phase_expectation.png',dpi=150);plt.close()
    plt.figure(figsize=(8,4.5));plt.plot([r[0] for r in closed],[r[1]/1e9 for r in closed],label='Battery energy');plt.plot([r[0] for r in closed],[r[2]/1e9 for r in closed],label='Field energy');plt.plot([r[0] for r in closed],[r[3]/1e9 for r in closed],label='Total closed energy',linewidth=2.5);plt.xlabel('Fraction transferred');plt.ylabel('Energy (GJ)');plt.title('Energy ledger: redistribution is not mass creation');plt.legend();plt.grid(alpha=.25);plt.tight_layout();plt.savefig(R/'chart_04_closed_ledger.png',dpi=150);plt.close()
except ImportError:
    print('Optional matplotlib not installed: CSV and JSON were generated; PNG skipped')

print(json.dumps(summary,ensure_ascii=False,indent=2))
