import unittest, math, random
from src.physics import *
from src.simulation import *

class TestKnownPhysics(unittest.TestCase):
    def test_g_ref(self): self.assertEqual(G_REF,6.67430e-11)
    def test_z(self): self.assertAlmostEqual(z_from_G()*2/C,G_REF,places=23)
    def test_dimensional_gravity(self): self.assertTrue(1.0e-46<alpha_grav(9.1093837139e-31)<2.0e-45)
    def test_newton_q(self): self.assertEqual(radial_shape_newton(),1.)
    def test_mu_orbits(self):
        mu=3.98600435507e14;r=7e6
        p=2*math.pi*math.sqrt(r**3/mu)
        self.assertAlmostEqual(circular_orbit_mu(r,p)/mu,1,places=13)
    def test_common(self):
        self.assertAlmostEqual(two_sensor_common(G_REF*100,.5,.1),3.01270486111111e-8,delta=1e-19)
    def test_grad(self): self.assertAlmostEqual(two_sensor_gradient(G_REF*100,.5,.1),1.15873e-7,delta=1e-12)
    def test_weak_field(self): self.assertTrue(compactness(3.98600435507e14,6371000)<1e-9)
    def test_K(self): self.assertTrue(kretschmann(3.98600435507e14,6371000)>0)
    def test_microscope(self): self.assertAlmostEqual(conservative_95_eta_bound()/1e-15,6.89,delta=.13)
    def test_param_reparam_degenerate(self):
        mu=1.32712440041279419e20
        for k in [0.2,1,10,100]:
            self.assertAlmostEqual((G_REF*k)*(mu/(G_REF*k))/mu,1,places=14)

class TestYukawa(unittest.TestCase):
    def test_alpha0_Q(self):
        for l in [.001, .1,1,10,1e8]: self.assertEqual(radial_shape_point(.3,0,l),1)
    def test_newton_lambda(self):
        self.assertAlmostEqual(radial_shape_point(.3,.1,1e12),1,places=11)
    def test_Q_analytic_numeric(self):
        for r in [.13,.4,1.5,3.7]:
            for l in [.1,.25,1.,9.]:
                eps=1e-6*r
                gp=point_yukawa_acceleration(4.0,r+eps,.09,l,1.1,.8)
                gm=point_yukawa_acceleration(4.0,r-eps,.09,l,1.1,.8)
                g=point_yukawa_acceleration(4.0,r,.09,l,1.1,.8)
                q=-r*(gp-gm)/(2*eps)/(2*g)
                self.assertAlmostEqual(q,radial_shape_point(r,.09,l,1.1,.8),delta=4e-9)
    def test_universal_Q(self):
        r=.5;lam=.25;alpha=.15;u=.27
        eps=1e-6*r
        gp=point_yukawa_acceleration(1,r+eps,alpha,lam,universal=u)
        gm=point_yukawa_acceleration(1,r-eps,alpha,lam,universal=u)
        g=point_yukawa_acceleration(1,r,alpha,lam,universal=u)
        q=-r*(gp-gm)/(2*eps)/(2*g)
        self.assertAlmostEqual(q,radial_shape_point(r,alpha,lam,universal=u),delta=1e-9)
    def test_envelope_zero_radius(self): self.assertAlmostEqual(finite_envelope(0,.2,.3),math.exp(-.2/.3))
    def test_envelope_small(self):
        x=.001;r=.5;lam=2;R=x*lam
        F=3*(x*math.cosh(x)-math.sinh(x))/x**3
        self.assertAlmostEqual(finite_envelope(R,r,lam),F*math.exp(-r/lam),delta=2e-7)
    def test_envelope_medium(self):
        x=.8;lam=.2;rad=x*lam;r=.5
        F=3*(x*math.cosh(x)-math.sinh(x))/x**3
        self.assertAlmostEqual(finite_envelope(rad,r,lam),F*math.exp(-r/lam),delta=2e-14)
    def test_large_no_overflow(self):
        self.assertTrue(math.isfinite(finite_envelope(.19,.2,.0001)))
        self.assertGreaterEqual(finite_envelope(.19,.2,.0001),0)
    def test_sphere_to_point(self):
        for l in [.3,1,10]:
            self.assertAlmostEqual(sphere_acceleration(1,.5,0,.2,l),point_yukawa_acceleration(1,.5,.2,l),delta=1e-10)
    def test_outside_only(self):
        with self.assertRaises(ValueError): sphere_acceleration(1,.1,.2,.1,.3)
    def test_Eotvos(self):
        e=eotvos(.2,.9,1.1,1e-6,.5,.2)
        d=normalized_material_difference(.2,.9,1.1,1e-6,.5,.2)
        self.assertAlmostEqual(e,d,delta=1e-11)
    def test_universal_cancels(self):
        e0=point_yukawa_acceleration(1,.5,.12,.2,.9,1.1,universal=.15)
        e1=point_yukawa_acceleration(1,.5,.12,.2,.9,.5,universal=.15)
        d=(e0-e1)/newton_acceleration(1,.5)
        self.assertAlmostEqual(d,normalized_material_difference(.9,1.1,.5,.12,.5,.2),places=13)
    def test_newton_shape_is_independent_G(self):
        for mu in [1e-4,1e3,1e20]: self.assertAlmostEqual((mu/4)/(mu/16),4.)
    def test_invalid(self):
        with self.assertRaises(ValueError): finite_envelope(.4,.1,.5)
        with self.assertRaises(ValueError): radial_shape_point(.5,.2,-.5)

class TestMatrix(unittest.TestCase):
    def setUp(self):
        self.sources=[(.1,.30,.05),(-.8,.43,.07),(1.2,.56,.09)]
        self.pairs=[(.9,.6),(-.5,.8),(1.2,.3)]
    def test_rank_one_all_minors(self):
        d=exact_factor_matrix(self.sources,self.pairs,.08,.32)
        for a in range(3):
            for b in range(a+1,3):
                for i in range(3):
                    for j in range(i+1,3):
                        det=matrix_rank_one_invariant(d[a][i],d[a][j],d[b][i],d[b][j])
                        self.assertAlmostEqual(det,0,delta=1e-17)
    def test_singular_values(self):
        d=exact_factor_matrix(self.sources,self.pairs,.08,.32)
        s=singular_values(d)
        self.assertLess(s[1]/s[0],1e-13)
    def test_two_mediator_rank2(self):
        src=[(.1,.8,.3,.05),(-.8,.2,.43,.07),(1.2,-.3,.56,.09)]
        pairs=[(.9,.6,-.2,.7),(-.5,.8,.6,.2),(1.2,.3,-.4,.5)]
        mat=two_mediator_matrix(src,pairs,.08,.32,.09,.6)
        ss=singular_values(mat)
        self.assertGreater(ss[1]/ss[0],1e-3)
    def test_seed_reproducible(self):
        d=exact_factor_matrix(self.sources,self.pairs,.08,.32)
        self.assertEqual(gaussian_noisy(d,1e-4,29),gaussian_noisy(d,1e-4,29))
    def test_noisy_rank_fails(self):
        d=exact_factor_matrix(self.sources,self.pairs,.08,.32)
        n=gaussian_noisy(d,1e-3,29)
        self.assertGreater(singular_values(n)[1],0)

if __name__=='__main__':unittest.main()
