import math, unittest, random, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.gravitylab import *

class Physics(unittest.TestCase):
    def setUp(self): self.r=Rig()
    def test_geometry(self): self.r.validate()
    def test_reject_bad_geometry(self):
        with self.assertRaises(ValueError): Rig(distance_m=.25,baseline_m=.2,source_radius_m=.2).validate()
    def test_reject_zero_distance(self):
        with self.assertRaises(ValueError): acceleration_x(0,0,100)
    def test_symmetry_odd(self):
        a=source_observables(self.r,1);b=source_observables(self.r,-1)
        self.assertAlmostEqual(a['common'],-b['common'],places=20)
    def test_symmetry_even(self):
        a=source_observables(self.r,1);b=source_observables(self.r,-1)
        self.assertAlmostEqual(a['gradient'],b['gradient'],places=18)
    def test_theory_closed_forms(self):
        for s in [-1,1]:
            a=source_observables(self.r,s);f=theoretical_signals(self.r)
            self.assertAlmostEqual(a['common'],s*f['common_odd_amplitude'],places=20)
            self.assertAlmostEqual(a['gradient'],f['gradient_even'],places=18)
    def test_reversal_difference(self):
        a=source_observables(self.r,1);b=source_observables(self.r,-1)
        self.assertAlmostEqual(a['common']-b['common'],theoretical_signals(self.r)['common_plus_minus_change'],places=20)
    def test_mass_linear(self):
        a=theoretical_signals(self.r)['common_odd_amplitude'];b=theoretical_signals(Rig(mass_kg=200))['common_odd_amplitude']
        self.assertAlmostEqual(b/a,2)
    def test_geometry_large_d_point_limit(self):
        r=Rig(distance_m=100,source_radius_m=.1)
        val=theoretical_signals(r)['common_odd_amplitude']
        self.assertAlmostEqual(val/(G*r.mass_kg/r.distance_m**2),1,delta=1e-5)
    def test_field_energy(self): self.assertAlmostEqual(field_energy_joule(.1,.001),.01*.001/(2*MU0))
    def test_energy_quad(self): self.assertAlmostEqual(field_energy_joule(.2,.001)/field_energy_joule(.1,.001),4)
    def test_energy_transfer_zero_monopole(self):
        v=generate_all(ROOT);self.assertEqual(v['electromagnetic']['monopole_delta_g_if_only_internal_transfer_m_s2'],0.)
    def test_uncertainty_positive(self): self.assertGreater(uncertainty_budget(self.r)['rss_m_s2'],0.)
    def test_baseline_uncertainty_derivative(self):
        r=self.r
        eps=1e-6
        plus=theoretical_signals(Rig(mass_kg=r.mass_kg,distance_m=r.distance_m,baseline_m=r.baseline_m+eps))["common_odd_amplitude"]
        minus=theoretical_signals(Rig(mass_kg=r.mass_kg,distance_m=r.distance_m,baseline_m=r.baseline_m-eps))["common_odd_amplitude"]
        fd=(plus-minus)/(2*eps)
        model=uncertainty_budget(r,sigma_mass_kg=0,sigma_distance_m=0,sigma_baseline_m=2*eps,sigma_tilt_rad=0)["terms_m_s2"]["baseline_m"]/(2*eps)
        self.assertAlmostEqual(fd/model,1,delta=1e-8)
    def test_distance_dominates(self):
        u=uncertainty_budget(self.r)['terms_m_s2'];self.assertGreater(abs(u['distance_m']),abs(u['mass_kg']))
    def test_abba_balance(self):
        x=abba_sides(50)
        self.assertEqual(sum(x),0)
        for i in range(0,len(x),4):
            self.assertEqual(sum(x[i:i+4]),0)
            self.assertEqual(sum((j-1.5)*x[i+j] for j in range(4)),0)
    def test_lockin_exact(self):
        x=abba_sides(30)
        z=[{'side':s,'common_m_s2':3*s+100+2*i} for i,s in enumerate(x)]
        self.assertAlmostEqual(estimate_odd_abba(z)['amplitude'],3,places=12)
    def test_lockin_reject_invalid(self):
        with self.assertRaises(ValueError): estimate_odd_abba([{'side':1,'common_m_s2':2}])
    def test_synthetic_mass_recovery(self):
        m=generate_mass_run(self.r,128,83011,True)
        d=generate_mass_run(self.r,128,83022,False)
        val=compare_mass_dummy(m,d)
        true=theoretical_signals(self.r)['common_odd_amplitude']
        self.assertLess(abs(val['adjusted_amplitude']-true),5*val['standard_error'])
    def test_synthetic_gradient_recovery(self):
        m=generate_mass_run(self.r,128,83011,True)
        val=estimate_even_gradient(m)
        th=theoretical_signals(self.r)['gradient_even']
        self.assertLess(abs(val['gradient_mean_s2']-th),5*val['gradient_se_s2'])
    def test_dummy_artifact_nonzero(self):
        d=generate_mass_run(self.r,128,83022,False)
        a=estimate_odd_abba(d)
        self.assertGreater(a['amplitude'],0)
    def test_em_signal_below_noise(self):
        energy=field_energy_joule(.1,.001)
        g=point_mass_gravity_at_distance(energy_mass_kg(energy),.2)
        self.assertLess(g,1e-20)
    def test_em_dummy_statistical_null(self):
        a=estimate_odd_abba(generate_em_run(seed=83033),'signal_m_s2')
        b=estimate_odd_abba(generate_em_run(seed=83044),'signal_m_s2')
        self.assertLess(abs(a['amplitude']-b['amplitude']),5*math.hypot(a['standard_error'],b['standard_error']))
    def test_source_outside(self):
        self.assertGreater(self.r.distance_m-self.r.baseline_m/2,self.r.source_radius_m)
    def test_two_sensor_consistency(self):
        d=source_observables(self.r,1)
        self.assertAlmostEqual(d['common'],(d['left']+d['right'])/2)
    def test_fixed_seed_repro(self):
        a=generate_mass_run(self.r,2,1,True);b=generate_mass_run(self.r,2,1,True)
        self.assertEqual(a,b)
    def test_g_uncertainty_finite(self): self.assertGreater(G_U,0)

class Parametric(unittest.TestCase):
    pass

# Distinct geometry / parity / scaling cases make a broad reproducible regression set.
for idx,m in enumerate((1.,10.,100.,500.,1000.)):
    def f(self,m=m):
        r=Rig(mass_kg=m)
        q=source_observables(r,1)
        self.assertGreater(q['common'],0)
        self.assertGreater(q['gradient'],0)
    setattr(Parametric,f'test_mass_{idx}',f)
for idx,d in enumerate((.43,.5,.75,1.,3.,10.)):
    def f(self,d=d):
        r=Rig(distance_m=d)
        q=source_observables(r,1)
        self.assertAlmostEqual(q['common'],theoretical_signals(r)['common_odd_amplitude'],places=20)
    setattr(Parametric,f'test_distance_{idx}',f)
for idx,bb in enumerate((.02,.05,.10,.20,.30)):
    def f(self,bb=bb):
        r=Rig(baseline_m=bb)
        p=source_observables(r,1);n=source_observables(r,-1)
        self.assertAlmostEqual(p['gradient'],n['gradient'],places=18)
    setattr(Parametric,f'test_baseline_{idx}',f)
for idx,B in enumerate((0.,.001,.01,.05,.1,.5,1.,2.)):
    def f(self,B=B):
        u=field_energy_joule(B,.001)
        self.assertGreaterEqual(u,0)
        self.assertAlmostEqual(energy_mass_kg(u),u/C**2)
    setattr(Parametric,f'test_magnetic_{idx}',f)

if __name__=='__main__': unittest.main()
