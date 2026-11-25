from pathlib import Path
import csv,json,math,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from model import *
from dimensions import audit

def run():
    root=Path(__file__).resolve().parents[1]
    results=root/'results';results.mkdir(exist_ok=True)
    h=LightHelix.from_curvature_torsion(0.6,0.8)
    boosted,D=h.boost_along_axis(0.3)
    field=spacetime_berry_field(theta=math.pi/4,theta_gradient=(0.,0.25,0.,0.),phi_gradient=(2.,0.,0.,0.))
    out={
      'scope':'Model/analytic tests only; no observational confirmation of ROOT',
      'units':'c=1; hbar and G remain dimensional and independent',
      'helix':{'a_L':h.radius,'omega_invL':h.omega,'u':h.axial,'kappa_invL':h.curvature,'tau_invL':h.torsion,'pitch_L':h.pitch,'period_L':1/h.frequency,'frame_omega_invL':norm(h.darboux(0.23))},
      'boost_beta_0p3':{'D':D,'omega_geometric_ratio':boosted.omega/h.omega,'energy_ratio_if_massless_tangent':D,'energy_to_geom_frequency_ratio_change':D**2,'axial_velocity':boosted.axial,'new_curvature':boosted.curvature,'new_torsion':boosted.torsion},
      'berry':{'connection_theta_pi2':berry_connection_theta_phi(math.pi/2),'curvature_theta_pi2':berry_curvature_theta_phi(math.pi/2),'flux_analytic':berry_flux_analytic(),'chern':berry_flux_analytic()/(2*math.pi),'flux_numeric_midpoint':berry_flux_midpoint(300,320), 'induced_F_t_x':field[0][1], 'induced_F_x_t':field[1][0], 'induced_F_pfaffian':pfaffian4(field), 'pfaffian_two_textures':pfaffian4(sum_two_forms(spacetime_berry_field(math.pi/2,[1,0,0,0],[0,2,0,0]), spacetime_berry_field(math.pi/2,[0,0,1,0],[0,0,0,2]))), 'generic_E_parallel_B_pfaffian':pfaffian4([[0.,1.,0.,0.],[-1.,0.,0.,0.],[0.,0.,0.,1.],[0.,0.,-1.,0.]]), 'uniform_polar_angle_F':spacetime_berry_field(math.pi/2,[0,0,0,0],[1,0,0,0])[0][1]},
      'stueckelberg':{'pure_gauge_B':stueckelberg_B([1,2,3,4],[1,2,3,4]),'gauge_mass_invL_g0p2_f3':vector_inverse_length_mass(.2,3),'dispersion_k2_g0p2_f3':relative_dispersion(2,.2,3),'gap_over_hbar_invL':.2*3},
      'unit_audit':audit(),
      'theory_state':{'lightlike_free_spatial_helix':'inconsistent without interactions/background: non-geodesic','three_perpendicular_forces_universal':'refuted by counterexamples','scalar_phase_alone_generates_physical_F':'false when pure gauge','spinor_texture_induces_U1_curvature':'verified identity','SU3_SU2_U1_from_helix':'not derived','four_force_unification':'not established'}
    }
    (results/'numerical.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    with (results/'curvature_reconstruction.csv').open('w',newline='',encoding='utf-8') as f:
      w=csv.writer(f);w.writerow(['kappa_invL','tau_invL','radius_L','omega_invL','axial','pitch_L','residual_speed2','residual_kappa','residual_tau'])
      for ka in [0.02,0.1,0.3,0.6,1.0,3.,12.]:
        for ta in [-10.,-1.,-0.8,-0.1,0.,0.1,0.8,1.,10.]:
          v=LightHelix.from_curvature_torsion(ka,ta)
          w.writerow([ka,ta,v.radius,v.omega,v.axial,v.pitch,v.transverse**2+v.axial**2-1,v.curvature-ka,v.torsion-ta])
    with (results/'boost_sweep.csv').open('w',newline='',encoding='utf-8') as f:
      w=csv.writer(f);w.writerow(['beta','D_energy_ratio','omega_geom_ratio','energy_per_omega_geom_ratio','kappa_boosted','tau_boosted','speed_residual'])
      for beta in [-.8,-.5,-.3,0.,.3,.5,.8]:
        h2,d=h.boost_along_axis(beta)
        w.writerow([beta,d,h2.omega/h.omega,d**2,h2.curvature,h2.torsion,h2.transverse**2+h2.axial**2-1])
    with (results/'berry_flux_sweep.csv').open('w',newline='',encoding='utf-8') as f:
      w=csv.writer(f);w.writerow(['winding','flux_exact','flux_midpoint','chern_exact','absolute_error'])
      for n in [-3,-2,-1,0,1,2,3]:
        exact=berry_flux_analytic(n);num=berry_flux_midpoint(1000,16,n)
        w.writerow([n,exact,num,n,abs(num-exact)])
    print(json.dumps(out,ensure_ascii=False,indent=2))
    print('Saved numeric outputs to',results)

if __name__=='__main__':run()
