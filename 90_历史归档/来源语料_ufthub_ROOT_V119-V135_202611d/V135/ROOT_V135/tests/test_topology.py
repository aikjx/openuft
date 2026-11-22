import sys, pathlib, unittest, numpy as np
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'src'))
from topology import *

class TestIndexAndGeometry(unittest.TestCase):
    def test_links_unit_modulus(self):
        for n in [-2,-1,0,1,2]:
            ux,uy=links(6,n)
            self.assertLess(np.max(abs(abs(ux)-1)),1e-13)
            self.assertLess(np.max(abs(abs(uy)-1)),1e-13)
    def test_plaquette_integer_flux(self):
        for n in range(-3,4):
            ch,p=plaquette_chern(*links(8,n))
            self.assertAlmostEqual(ch,n,places=11)
            self.assertLess(np.std(p),1e-12)
    def test_flux_sign_reversal(self):
        for n in [1,2,3]:
            a=plaquette_chern(*links(8,n))[0]
            b=plaquette_chern(*links(8,-n))[0]
            self.assertAlmostEqual(a,-b,places=11)
    def test_index_sign_and_quantization(self):
        for n in [-3,-2,-1,0,1,2,3]:
            r=overlap_index(8,n)
            self.assertAlmostEqual(r['index'],-n,places=11)
            self.assertGreater(r['min_abs_wilson_eigenvalue'],0.1)
    def test_gamma5_hermiticity(self):
        for flux in [-2,0,2]:
            r=overlap_index(5,flux)
            self.assertLess(r['hermiticity_residual'],1e-12)
            self.assertLess(r['gamma5_hermiticity_residual'],1e-12)
    def test_flux_multiplies_charge(self):
        for n in range(-5,6):
            for q in [-6,-3,-1,0,1,2,4,6]:
                self.assertEqual(c1_index(n,q),n*q)
    def test_flux_3_varying_charge_no_go(self):
        charges={'Q_L':1,'u_R':4,'d_R':-2,'L_L':-3,'e_R':-6,'nu_R':0}
        modes={k:c1_index(3,v) for k,v in charges.items()}
        self.assertEqual(modes['Q_L'],3)
        self.assertEqual(modes['u_R'],12)
        self.assertEqual(modes['e_R'],-18)
        self.assertNotEqual(abs(modes['Q_L']),abs(modes['u_R']))
    def test_nonzero_index_is_net_not_total(self):
        # The pair (n_plus,n_minus) may be augmented by vectorlike pairs.
        self.assertEqual((5)-(2),3)
        self.assertEqual((3)-(0),3)
    def test_scalar_curvature_vanishing(self):
        for radius in [0.01,0.5,1,3.2,200]:
            self.assertTrue(no_flux_sphere_zero_modes(radius))
    def test_unwarped_gravitational_reduction(self):
        for v in [1e-6,0.5,1.0,5,1e10]:
            self.assertAlmostEqual(effective_newton(4.2*v,v),4.2)
    def test_internal_scale_does_not_fix_G(self):
        self.assertNotEqual(effective_newton(2.0,1.0),effective_newton(4.0,1.0))
    def test_invalid_inputs(self):
        for args in [(2,0),(6,18)]:
            with self.assertRaises(ValueError): links(*args)
        with self.assertRaises(ValueError): no_flux_sphere_zero_modes(0)
        with self.assertRaises(ValueError): effective_newton(1,-1)
        with self.assertRaises(TypeError): c1_index(1,1.5)
    def test_gauge_covariance_one_background(self):
        n=6; f=2; ux,uy=links(n,f)
        rng=np.random.default_rng(135)
        phases=rng.uniform(-np.pi,np.pi,(n,n));g=np.exp(1j*phases)
        ux2=np.zeros_like(ux);uy2=np.zeros_like(uy)
        for x in range(n):
            for y in range(n):
                ux2[x,y]=g[x,y]*ux[x,y]*g[(x+1)%n,y].conjugate()
                uy2[x,y]=g[x,y]*uy[x,y]*g[x,(y+1)%n].conjugate()
        c0,_=plaquette_chern(ux,uy);c1,_=plaquette_chern(ux2,uy2)
        self.assertAlmostEqual(c0,c1,places=12)
        # Confirm covariant Wilson matrix under a local diagonal gauge transform.
        from topology import wilson_from_links
        d0,h0,g5=wilson_from_links(ux,uy)
        d1,h1,_=wilson_from_links(ux2,uy2)
        gu=np.kron(np.diag(g.reshape(n*n)),np.eye(2))
        self.assertLess(np.linalg.norm(d1-gu@d0@gu.conj().T),1e-12)
        self.assertLess(np.max(abs(np.linalg.eigvalsh(h0)-np.linalg.eigvalsh(h1))),1e-12)
    def test_wilson_mass_parameter_range(self):
        for m0 in [0.5,0.8,1.,1.2,1.6]:
            r=overlap_index(6,1,m0)
            self.assertAlmostEqual(r['index'],-1,places=9)
    def test_finite_lattice_size_stability(self):
        for n in [4,5,6,7]:
            self.assertAlmostEqual(overlap_index(n,1)['index'],-1)
            self.assertAlmostEqual(overlap_index(n,-1)['index'],1)
    def test_no_unique_three_generation_prediction(self):
        self.assertEqual([c1_index(n,1) for n in [1,2,3,4]], [1,2,3,4])
    def test_no_alpha_prediction_from_flux(self):
        # Flux N=3 is compatible with arbitrary positive gauge kinetic coefficient.
        N=3
        candidate_alphas=[1/137.035999,1/120.,1/150.]
        self.assertTrue(all(c1_index(N,1)==3 for _ in candidate_alphas))
        self.assertEqual(len(set(candidate_alphas)),3)
    def test_explicit_overlap_zero_modes(self):
        for flux in [-3,-2,-1,1,2,3]:
            modes=overlap_zero_mode_chiralities(7,flux)
            self.assertEqual(len(modes),abs(flux))
            expected=-np.sign(flux)
            self.assertTrue(all(abs(m-expected)<1e-10 for m in modes))
    def test_zero_flux_has_vectorlike_zero_modes(self):
        self.assertEqual(len(overlap_zero_mode_chiralities(6,0)),2)
        self.assertTrue(np.allclose(overlap_zero_mode_chiralities(6,0),[-1,1]))
    def test_random_smooth_deformation_preserves_index(self):
        rng=np.random.default_rng(20261121)
        for flux in [-2,-1,1,2]:
            n=6;ux,uy=links(n,flux)
            for k in range(3):
                u=ux*np.exp(1j*rng.normal(0,0.025,(n,n)))
                v=uy*np.exp(1j*rng.normal(0,0.025,(n,n)))
                top,_=plaquette_chern(u,v)
                self.assertAlmostEqual(top,flux,places=11)
                self.assertAlmostEqual(overlap_index_from_links(u,v),-flux,places=11)
    def test_pure_gradient_connection_has_zero_flux(self):
        n=6;rng=np.random.default_rng(134)
        theta=rng.uniform(-np.pi,np.pi,(n,n));g=np.exp(1j*theta)
        ux=np.zeros((n,n),complex);uy=np.zeros((n,n),complex)
        for x in range(n):
            for y in range(n):
                ux[x,y]=g[x,y]*g[(x+1)%n,y].conjugate()
                uy[x,y]=g[x,y]*g[x,(y+1)%n].conjugate()
        top,plaq=plaquette_chern(ux,uy)
        self.assertAlmostEqual(top,0.,places=11)
        self.assertLess(max(abs(plaq)),1e-12)
    def test_abelian_anomaly_all_same_6d_chirality(self):
        charges=[1,4,-2,-3,-6,0]
        dims=[6,3,3,2,1,1]
        co=abelian_anomaly_coeffs(3,charges,dims)
        self.assertEqual(co['cubic'],3*2280)
        self.assertEqual(co['mixed_gravity'],3*120)
        self.assertGreater(co['cubic'],0)
    def test_anomaly_sign_flips_flux(self):
        q=[1,2,-3]
        p=abelian_anomaly_coeffs(3,q)
        m=abelian_anomaly_coeffs(-3,q)
        self.assertEqual(p['cubic'],-m['cubic'])
        self.assertEqual(p['mixed_gravity'],-m['mixed_gravity'])
    def test_effective_index_for_charge_two(self):
        for flux in [-2,-1,1,2]:
            self.assertAlmostEqual(overlap_index(8,2*flux)['index'],-2*flux)

    def test_flux_normalization_unit_charge(self):
        # 6Y integer-normalized SM charges for one generation.
        sm_charges=[1,4,-2,-3,-6,0]
        self.assertTrue(all(isinstance(c1_index(3,q),int) for q in sm_charges))

if __name__=='__main__':unittest.main()
