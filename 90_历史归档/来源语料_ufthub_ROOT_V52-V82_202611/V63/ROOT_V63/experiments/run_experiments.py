"""Generate reproducible ROOT V63 numerical tables (stdlib; optional figures)."""
from __future__ import annotations
from pathlib import Path
import sys, csv, json, math
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src import physics as p
DATA=ROOT/'data'; DATA.mkdir(exist_ok=True)
RESULTS=ROOT/'results'; RESULTS.mkdir(exist_ok=True)


def save_csv(filename,fields,rows):
    with (DATA/filename).open('w',newline='',encoding='utf-8-sig') as fp:
        w=csv.DictWriter(fp,fieldnames=fields);w.writeheader();w.writerows(rows)


def main():
    helix_rows=[]
    for a in range(0,91,5):
        h=p.helix(1.,a)
        helix_rows.append({'angle_deg':a,'v_phi_over_c':h.azimuthal_m_s/p.C,
                           'v_z_over_c':h.axial_m_s/p.C,
                           'curvature_m_inv':h.curvature_m_inv,
                           'torsion_m_inv':h.torsion_m_inv,
                           'accel_over_c2_per_m':h.acceleration_m_s2/p.C**2})
    save_csv('helix_geometry.csv',helix_rows[0].keys(),helix_rows)
    lp=p.planck_length_m()
    scan=[]
    for N in (1,2,4,8,16,32,64,128):
        for xi in (0.,1/12,1/6,0.25):
            gi=p.induced_G(N,lp,xi)
            scan.append({'N':N,'xi':xi,'ell_over_planck':1.,
                         'G_ind_over_G_observed':gi/p.G_CODATA_2022 if math.isfinite(gi) else 'infinite',
                         'sign_and_status': 'positive_formal' if gi>0 and math.isfinite(gi) else 'negative_or_degenerate',
                         'massless_mu':0., 'bare_inverse_G':0.})
    save_csv('induced_G_scan.csv',scan[0].keys(),scan)
    calibration=[]
    for N in (1,2,4,8,16,32,64,128):
        ell=p.calibrated_length_m(N=N)
        calibration.append({'N':N,'fitted_ell_m':ell,'fitted_ell_over_lp':ell/lp,
                            'reconstructed_G_m3_kg1_s2':p.induced_G(N,ell),
                            'is_independent_prediction':False})
    save_csv('inverse_calibration_NOT_prediction.csv',calibration[0].keys(),calibration)
    mass=[]
    for idx in range(0,41):
        mu=idx/10
        mass.append({'mu':mu,'proper_time_weight_F_mu':p.proper_time_mass_factor(mu)})
    save_csv('mass_decoupling.csv',mass[0].keys(),mass)
    yuk=[]
    for idx in range(0,51):
        x=idx/5
        yuk.append({'r_over_range':x,'alpha_y':0.1,
                    'delta_g_over_g_newton':p.yukawa_relative_accel(.1,x,1.)})
    save_csv('hypothetical_yukawa_NO_data.csv',yuk[0].keys(),yuk)
    earth=[]
    for altitude in (0.,100_000.,400_000.,1_000_000.):
        earth.append({'altitude_m':altitude,'spherical_newton_g_m_s2':p.earth_g_m_s2(altitude),
                      'gravity_model':'point mass / spherical approximation',
                      'is_geodetic_measurement':False})
    save_csv('earth_newton_reference.csv',earth[0].keys(),earth)
    modes=[]
    for mass_kg in (0.,1e-35,1e-34,1e-33):
        mode=p.cylindrical_wave_mode(.1,10,50.,mass_kg)
        modes.append({'n':10,'radius_m':.1,'kz_m_inv':50.,'rest_mass_kg':mass_kg,
                      'omega_rad_s':mode.omega_rad_s,'v_phi_over_c':mode.group_v_phi_m_s/p.C,
                      'v_z_over_c':mode.group_v_z_m_s/p.C,
                      'total_group_speed_over_c':mode.group_speed_m_s/p.C})
    save_csv('cylinder_wave_modes.csv',modes[0].keys(),modes)
    # Self-consistency only; NOT observational tests of a new hypothesis.
    data={
        'edition':'ROOT V63','generated_by':'experiments/run_experiments.py',
        'epistemic_status':'kinematical identities + known EFT method + illustrative model assumptions',
        'codata_2022':{'G_m3_kg1_s2':p.G_CODATA_2022,'G_std':p.G_STD,'c_m_s':p.C,
                       'h_exact_j_s':p.H,'hbar_j_s':p.HBAR,
                       'derived_planck_length_m':lp},
        'induced_gravity':{'regulator':'sharp proper-time cutoff','loop_order':1,
                           'matter':'N free real scalar fields','bare_inverse_G_assumed':0.,
                           'positive_sign_condition_for_massless_scalar':'xi<1/6',
                           'formula':'1/G=N (1-6xi) hbar F(mu)/(12pi c^3 ell^2)',
                           'parameter_degeneracy':'N, xi, ell, m, bare 1/G, regulator unpredicted',
                           'single_scalar_inverse_fitted_length_m':p.calibrated_length_m(),
                           'UV_cutoff_energy_j_from_length':p.cutoff_energy_j(p.calibrated_length_m()),
                           'vacuum_energy_formal_magnitude_j_m3':p.vacuum_energy_magnitude_j_m3(p.calibrated_length_m())},
        'geometry':{'helix_speed_is_prescribed':'v=c','not_allowed_as_massive_point_worldline':True,
                    'wave_mode':'idealized cylinder shell free dispersion; not microscopic model of gravity'},
        'audit_previous_claims':{'alpha_proposal':p.old_alpha_guess(),
                                  'alpha_CODATA_2022':7.2973525643e-3,
                                  'alpha_guess_relative_error':(p.old_alpha_guess()/7.2973525643e-3-1),
                                  'proton_mass_ratio_wrong_expression':p.old_mass_ratio_guess(),
                                  'alleged_value':1836.15267343},
        'proof_status':{
             'helix_curvature_torsion':'proved within curve model',
             'cylindrical_massless_mode_dispersion':'proved within stipulated wave equation',
             'one_loop_scalar_induced_R':'proved conditionally in proper-time regularization',
             'independent_G_from_helix':'UNPROVED',
             'four_force_unification':'UNPROVED',
             'no_new_published_physics_claim':'confirmed'
        }
    }
    (RESULTS/'numerical_summary.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Generated 7 CSV files + numerical_summary.json')
    print('G =',p.G_CODATA_2022,'lp =',lp)
    print('ell_fit N=1=',p.calibrated_length_m())
    print('alpha_guess error=',data['audit_previous_claims']['alpha_guess_relative_error'])
    print('G_ind(ell_P,N=1,xi=0)/G_measured=',p.induced_G(1,lp)/p.G_CODATA_2022)

    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        print('Optional matplotlib not installed: skipping pre-rendered figures')
        return
    def plot_xy(x,y,xlabel,ylabel,filename,logx=False,logy=False):
        fig,ax=plt.subplots(figsize=(7.8,4.8)); ax.plot(x,y,marker='o',markersize=3)
        if logx:ax.set_xscale('log')
        if logy:ax.set_yscale('log')
        ax.set_xlabel(xlabel);ax.set_ylabel(ylabel);ax.grid(alpha=.28)
        fig.tight_layout();fig.savefig(RESULTS/filename,dpi=160);plt.close(fig)
    plot_xy([r['N'] for r in calibration],[r['fitted_ell_over_lp'] for r in calibration],
            'number N of toy scalar species','ell_fit / Planck length (inverse fit)','fitted_length_vs_N.png')
    plot_xy([r['mu'] for r in mass],[r['proper_time_weight_F_mu'] for r in mass],
            'mu = m c ell / hbar','mass decoupling F(mu)','mass_cutoff_suppression.png')
    plot_xy([r['angle_deg'] for r in helix_rows],[r['curvature_m_inv'] for r in helix_rows],
            'helix angle (deg)','curvature at R=1m (1/m)','helix_curvature.png')
    print('Generated 3 pre-rendered figures')

if __name__=='__main__':main()
