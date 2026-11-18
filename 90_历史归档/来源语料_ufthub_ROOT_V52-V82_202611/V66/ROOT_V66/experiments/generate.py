"""Deterministic numerical reproducibility, synthetic data clearly labeled."""
import csv, json, math, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src import root_v66 as M


def write_csv(name,columns,rows):
    p=ROOT/'data'/name
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        wr=csv.writer(f);wr.writerow(columns);wr.writerows(rows)
    return p


def main():
    (ROOT/'data').mkdir(exist_ok=True);(ROOT/'results').mkdir(exist_ok=True)
    pitch_rows=[]
    for j in range(-89,90):
        h=M.helix_from_radius_pitch(2.0,math.radians(j),1.)
        pitch_rows.append([j,h.kappa,h.tau,h.omega,h.tangential_speed,h.axial_speed])
    write_csv('MATH_helix_geometry.csv',['pitch_deg','curvature_per_R','torsion_per_R','omega','vtheta','vaxial'],pitch_rows)

    induction=[]
    for i in range(241):
        mu=10**(-5+7*i/240)
        f=M.threshold_F(mu)
        induction.append([mu,f,1-f])
    write_csv('TOY_induced_gravity_threshold.csv',['mu_m_over_UV','proper_time_F','subtracted_fraction'],induction)

    gfit=[]
    for n in [1,2,3,4,8,16,32,64,128,256,512,1024]:
        ell=M.reverse_fit_length(n)
        gfit.append([n,ell,ell/M.planck_length(),1/M.inverse_G_induced(n,0,ell), 'REVERSE_FIT_NOT_PREDICTION'])
    write_csv('FIT_not_prediction_G_degeneracy.csv',['N','ell_m','ell_over_LPlanck','fitted_G','status'],gfit)

    fifth=[]
    for j in range(141):
        delta=10**(-20+14*j/140)
        eta=M.fifth_force_eta(delta,0.,0.)
        fifth.append([delta,eta,int(M.pass_microscope_toy(delta,0.))])
    write_csv('TOY_Microscope_fifthforce.csv',['alpha_composition_A','eotvos_eta','within_illustrative_95_interval'],fifth)

    cassini=[]
    for i in range(241):
        fp=10**(-5+4*i/240)
        gamma=M.ppn_gamma_massless_scalar(1,fp)
        ratio=M.cavendish_massless_scalar_G(1,fp)/(1/(8*math.pi))
        cassini.append([fp,gamma,ratio,int(M.pass_cassini_toy(1,fp))])
    write_csv('TOY_Cassini_gamma_scalar_tensor.csv', ['Fprime','PPN_gamma','Cavendish_to_tensor_G','within_illustrative_95_interval'],cassini)

    earth=[]
    for h in range(0,1000001,25000):
        earth.append([h,M.spherical_earth_g(h),M.dipole_B(0,h),M.dipole_B(math.pi/2,h)])
    write_csv('TOY_Earth_spherical_dipole.csv',['altitude_m','g_m_per_s2','B_equator_T','B_pole_T'],earth)

    # Bessel scalar cylinder, model parameters m=q=k=A=a=1 toy units,
    # boundary q*a=j_1,1 with k=0.7,m=0.4 (not physical Earth source).
    try:
        from scipy.integrate import quad
        from scipy.special import jv,jn_zeros
        j=float(jn_zeros(1,1)[0]);a=1.;q=j/a;k=.7;mass=.4;A=.7
        omega=math.sqrt(q*q+k*k+mass*mass)
        # T00 = |dtPsi|² + |gradPsi|² + m²|Psi|²
        # radial f=A*J1(qr), gradient²=f_r² + (1/r² +k²)f².
        def density(r):
            f=A*jv(1,q*r)
            df=A*q*.5*(jv(0,q*r)-jv(2,q*r))
            return (omega*omega+k*k+mass*mass)*f*f + df*df + (f/r)**2 if r else 2*(A*q/2)**2
        numerical,err=quad(lambda r:2*math.pi*r*density(r),0,a,epsabs=1e-11)
        # integrate radial gradient + (1/r²)F² = q² * ∫F², boundary zero;
        # total U/L = 2 omega² * ∫ |Psi|² = 2 ω² πa² A²J2(j)²
        exact=2*omega**2*math.pi*a*a*A*A*jv(2,j)**2
        bessel={'omega':omega,'j11':j,'analytical_U_per_L':exact,'numerical_U_per_L':numerical,
                'relative_error':abs(exact-numerical)/abs(exact),'quad_error_estimate':err,
                'status':'TOY complex scalar cylinder with Dirichlet boundary'}
        with (ROOT/'data'/'TOY_KG_cylindrical_energy.csv').open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.writer(f);w.writerow(['r','energy_density_arbitrary_units'])
            for i in range(301):
                r=a*i/300;w.writerow([r,density(r)])
    except ImportError:
        bessel={'status':'NOT RUN; requires SciPy'}

    lplanck=M.planck_length()
    ep=math.sqrt(M.HBAR*M.C**5/M.G)
    rho_planck=M.vacuum_energy_from_cutoff_energy(ep)
    rho_de_schematic=5.3e-10 # rough observational order-of-magnitude; not a fit
    summary={
       'version':'ROOT V66','physical_status':'FOUR_FORCE_UNIFICATION_OPEN',
       'CODATA_2022_G':M.G,'CODATA_2022_alpha':M.ALPHA_2022,
       'candidate_alpha':M.alpha_candidate(),
       'alpha_relative_error_ppm':M.residual_ppm(M.alpha_candidate(),M.ALPHA_2022),
       'incorrect_mass_ratio_formula_56pi':56*math.pi,
       'observed_mass_ratio':M.MASS_RATIO_2022,
       'Schwarzschild_ISCO_in_GM_over_c2':6,
       'Earth_spherical_g_m_per_s2':M.spherical_earth_g(0),
       'Planck_length_m_using_measured_G':lplanck,
       'planck_energy_J_using_measured_G':ep,
       'sharp_cutoff_zero_point_density_J_per_m3':rho_planck,
       'toy_dark_energy_order_J_per_m3':rho_de_schematic,
       'log10_unrenormalized_vacuum_to_dark_energy_ratio':math.log10(rho_planck/rho_de_schematic),
       'Cassini_gamma_center':1+2.1e-5,'Cassini_gamma_sigma':2.3e-5,
       'microscope_eta_center':-1.5e-15,'microscope_stat':2.3e-15,'microscope_syst':1.5e-15,
       'microscope_illustrative_95_interval':M.microscope_illustrative_interval(),
       'bessel_KG_energy':bessel,
       'references_type':'CODATA PDG MICROSCOPE Cassini NASA; see sources.md',
       'warnings':['All field scans synthetic / illustrative','G already supplied in Earth and induced inverse fit',
                   'Reference measurements are not an original independent experiment']
    }
    (ROOT/'results'/'numerical_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        # use matplotlib defaults, no manual colors or styles
        def save(name,x,y,xlabel,ylabel,title,xlog=False,ylog=False):
            fig,ax=plt.subplots(figsize=(7.6,4.4))
            ax.plot(x,y)
            if xlog:ax.set_xscale('log')
            if ylog:ax.set_yscale('log')
            ax.set_xlabel(xlabel);ax.set_ylabel(ylabel);ax.set_title(title)
            ax.grid(alpha=.25);fig.tight_layout()
            fig.savefig(ROOT/'results'/name,dpi=160)
            plt.close(fig)
        save('helix_curvature.png',[x[0] for x in pitch_rows],[x[1] for x in pitch_rows],
             'pitch angle (degree)','curvature (1/m)','Mathematical circular helix curvature')
        save('mass_cutoff.png',[x[0] for x in induction],[x[1] for x in induction],
             'mass / UV cutoff','F(mu)','Proper-time scheme threshold, synthetic',xlog=True)
        save('earth_gravity.png',[x[0]/1000 for x in earth],[x[1] for x in earth],
             'altitude (km)','g (m/s²)','Spherical Earth approximation')
        save('microscope_test.png',[x[0] for x in fifth],[abs(x[1]) for x in fifth],
             'synthetic composition coupling difference','abs(Eotvos eta)','Illustrative fifth-force exclusions',xlog=True,ylog=True)
        save('cassini_ppn_gamma.png',[x[0] for x in cassini],[1-x[1] for x in cassini],
             'Fprime at F0=1, K0=1','1 - gamma','Massless scalar-tensor PPN toy',xlog=True,ylog=True)
        if bessel.get('relative_error') is not None:
            r=[i/300 for i in range(301)];dens=[density(x) for x in r]
            save('KG_energy_density.png',r,dens,'r / radius','energy density (toy)','KG helical phase cylinder')
    except ImportError:
        pass
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
