import unittest
import numpy as np
from src.physics import *

class TestModel(unittest.TestCase):
    def setUp(self):
        self.k=k_lower(2.4)
        self.ku=k_upper(2.4)

    def test_null(self): self.assertAlmostEqual(self.ku @ ETA @ self.ku,0)
    def test_fourier_k_sign(self): self.assertEqual(self.k[0],-2.4)
    def test_maxwell_antisymmetric(self):
        f=maxwell_field(self.k, np.array([0.,1.,.3,0.]))
        np.testing.assert_allclose(f+f.T,0,atol=1e-14)
    def test_electric_field_nonzero(self):
        f=maxwell_field(self.k, np.array([0.,1.,0.,0.]))
        self.assertAlmostEqual(abs(f[0,1]),2.4)
    def test_gauge_zero(self):
        np.testing.assert_allclose(maxwell_field(self.k,self.k),0,atol=0)
    def test_gauge_equivalence(self):
        a=np.array([0.,1.,.3,0.]); s=-3.3
        np.testing.assert_allclose(maxwell_field(self.k,a+s*self.k),maxwell_field(self.k,a),atol=1e-14)
    def test_divergence_zero(self):
        a=np.array([0.,1.,.3,0.]); f=maxwell_field(self.k,a)
        np.testing.assert_allclose(maxwell_divergence(self.ku,f),0,atol=1e-14)
    def test_longitudinal_pure_gauge(self):
        a=np.array([-1.,0.,0.,1.])
        np.testing.assert_allclose(maxwell_field(self.k,a),0,atol=1e-14)
    def test_spin2_symmetric(self):
        h=spin2_tt(1.,-.7)
        np.testing.assert_allclose(h,h.T)
    def test_spin2_traceless(self):
        self.assertAlmostEqual(np.trace(ETA@spin2_tt(.3,2.)),0)
    def test_spin2_transverse(self):
        np.testing.assert_allclose(self.ku@spin2_tt(.3,2.),0)
    def test_spin2_riemann_nonzero(self):
        self.assertAlmostEqual(linear_riemann(self.k,spin2_tt(1,0))[0,1,0,1],self.k[0]**2/2)
    def test_spin2_pure_gauge_zero(self):
        xi=np.array([1.,2.,3.,4.])
        np.testing.assert_allclose(linear_riemann(self.k,spin2_pure_gauge(self.k,xi)),0,atol=1e-13)
    def test_spin2_gauge_invariance(self):
        h=spin2_tt(1,.3); xi=np.array([1.,2.,3.,4.]); r=linear_riemann(self.k,h)
        np.testing.assert_allclose(linear_riemann(self.k,h+spin2_pure_gauge(self.k,xi)),r,atol=1e-12)
    def test_curvature_symmetry_antisym12(self):
        r=linear_riemann(self.k,spin2_tt(1,.4))
        np.testing.assert_allclose(r+np.swapaxes(r,0,1),0,atol=1e-14)
    def test_curvature_symmetry_antisym34(self):
        r=linear_riemann(self.k,spin2_tt(1,.4))
        np.testing.assert_allclose(r+np.swapaxes(r,2,3),0,atol=1e-14)
    def test_curvature_pair_symmetry(self):
        r=linear_riemann(self.k,spin2_tt(1,.4))
        np.testing.assert_allclose(r,np.transpose(r,(2,3,0,1)),atol=1e-14)
    def test_curvature_bianchi(self):
        r=linear_riemann(self.k,spin2_tt(1,.4))
        np.testing.assert_allclose(r+np.transpose(r,(0,2,3,1))+np.transpose(r,(0,3,1,2)),0,atol=1e-14)
    def test_spin2_other_mode(self):
        r=linear_riemann(self.k,spin2_tt(0,1))
        self.assertAlmostEqual(r[0,1,0,2],self.k[0]**2/2)
    def test_boost_group_metric(self):
        L=lorentz_z(.8)
        np.testing.assert_allclose(L.T@ETA@L,ETA,atol=1e-14)
    def test_boost_cov_vectors(self):
        L=lorentz_z(.6); S=lorentz_cov(.6)
        np.testing.assert_allclose(S,np.linalg.inv(L).T,atol=1e-14)
    def test_boost_invariance_F(self):
        S=lorentz_cov(.6); a=np.array([0.,1.,0.,0.]); f=maxwell_field(self.k,a)
        np.testing.assert_allclose(maxwell_field(S@self.k,S@a),S@f@S.T,atol=1e-13)
    def test_boost_invariance_R(self):
        S=lorentz_cov(.6); h=spin2_tt(.1,1.); r=linear_riemann(self.k,h)
        np.testing.assert_allclose(linear_riemann(S@self.k,S@h@S.T),transform_rank4_cov(r,S),atol=1e-12)
    def test_invalid_beta(self):
        for v in [1.,-1.,1.3]:
            with self.assertRaises(ValueError): lorentz_z(v)
    def test_physical_modes(self):
        e1,e2=vector_physical_modes()
        self.assertAlmostEqual(e1@ETA@e1,1)
        self.assertAlmostEqual(e2@ETA@e2,1)
        self.assertAlmostEqual(e1@ETA@e2,0)
        self.assertAlmostEqual(self.ku@e1,0)
        self.assertAlmostEqual(self.ku@e2,0)
    def test_rotations_orthonormal(self):
        e1,e2=vector_physical_modes()
        for a in [.1,.7,1.9]:
            u,v=rotate_transverse(a,e1,e2)
            self.assertAlmostEqual(u@u,1)
            self.assertAlmostEqual(v@v,1)
            self.assertAlmostEqual(u@v,0)
    def test_helicity_scalar(self):
        for a in [.1,.9,3.]: self.assertEqual(scalar_helicity_phase(a),1.)
    def test_helicity_spin1(self):
        self.assertAlmostEqual(abs(wave_helicity_phase(1,.7)),1)
    def test_helicity_spin2_square(self):
        for a in [.2,1.1]:
            self.assertAlmostEqual(abs(wave_helicity_phase(2,a)-wave_helicity_phase(1,a)**2),0)
    def test_different_couplings_same_free_solution(self):
        # dF=0 and k.F=0 independent of any nonzero g_F in S=-hbar F^2/(4g_F^2)
        a=np.array([0.,1.,0.,0.]); f=maxwell_field(self.k,a)
        for coupling in [.05,.3,1.,2.]:
            np.testing.assert_allclose(maxwell_divergence(self.ku,f)/coupling**2,0,atol=1e-14)


    def test_linear_ricci_vacuum_tt(self):
        np.testing.assert_allclose(linear_ricci(self.k,spin2_tt(.3,-.7)),0,atol=1e-14)
    def test_linear_einstein_vacuum_tt(self):
        np.testing.assert_allclose(linear_einstein(self.k,spin2_tt(1.,2.)),0,atol=1e-14)
    def test_linear_bianchi_identity_off_shell(self):
        k=np.array([2.,.4,-.3,1.])
        h=np.arange(16,dtype=float).reshape(4,4)
        h=(h+h.T)/2
        e=linear_einstein(k,h)
        kup=ETA@k
        np.testing.assert_allclose(kup@e,0,atol=1e-11)
    def test_linear_einstein_gauge_off_shell(self):
        k=np.array([2.,.4,-.3,1.])
        xi=np.array([1.,-.2,.7,-2.])
        np.testing.assert_allclose(linear_einstein(k,spin2_pure_gauge(k,xi)),0,atol=1e-11)
    def test_spin_one_helicity_rotation(self):
        e1,e2=vector_physical_modes()
        circular=(e1+1j*e2)/np.sqrt(2)
        for ang in [.2,.9,1.7]:
            np.testing.assert_allclose(rotation_z4(ang)@circular,np.exp(-1j*ang)*circular,atol=1e-14)
    def test_spin_two_helicity_rotation(self):
        e1,e2=vector_physical_modes()
        circular=(e1+1j*e2)/np.sqrt(2)
        h=np.outer(circular,circular)
        for ang in [.2,.9,1.7]:
            U=rotation_z4(ang)
            np.testing.assert_allclose(U@h@U.T,np.exp(-2j*ang)*h,atol=1e-14)
    def test_field_strength_versus_source_constraint(self):
        # Gauge source term J.A is invariant only for k.J=0 in Fourier space.
        arbitrary=np.array([3.,1.,1.,2.])
        conserved=np.array([2.,0.,0.,2.])
        self.assertNotAlmostEqual(float(self.k@arbitrary),0.)
        self.assertAlmostEqual(float(self.k@conserved),0.)
    def test_tensor_source_conservation(self):
        # h.T interaction shifts by xi_n k_m T^mn, which vanishes if conserved.
        conserved=np.zeros((4,4));conserved[1,1]=1.;conserved[2,2]=2.
        self.assertAlmostEqual(np.linalg.norm(self.ku@conserved),0.)
        nonconserved=conserved.copy();nonconserved[0,0]=1.
        self.assertGreater(np.linalg.norm(self.ku@nonconserved),0.)

if __name__=='__main__': unittest.main()
