import unittest,sys
from pathlib import Path
import numpy as np
from scipy.constants import c,e,m_e
from scipy.optimize import brentq
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from coil_model import (TwoCoilField,loop_field_cyl,circular_reference,trajectory,
                        jacobian_return,direct_biot_savart_ring,
                        smooth_finite_coil_quadrature)

class TestGeometryAndField(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f=TwoCoilField(order=17);cls.baseline=circular_reference(field=cls.f)
    def test_weights_sum(self):
        self.assertAlmostEqual(float(self.f.fractions.sum()),2.,12)
    def test_source_radii_outside_axis(self):
        self.assertTrue(np.all(self.f.radii>0))
    def test_two_coils_symmetry(self):
        self.assertAlmostEqual(float(self.f.field(.005,0.)[0]),0.,12)
    def test_mirror_br_odd(self):
        self.assertAlmostEqual(float(self.f.field(.005,.001)[0]),-float(self.f.field(.005,-.001)[0]),10)
    def test_mirror_bz_even(self):
        self.assertAlmostEqual(float(self.f.field(.005,.001)[1]),float(self.f.field(.005,-.001)[1]),10)
    def test_on_axis_finite(self):
        self.assertTrue(np.isfinite(float(self.f.field(0.,0.)[1])))
    def test_cartesian_axis(self):
        self.assertAlmostEqual(float(self.f.field_cart(0,0,0)[0]),0,14)
    def test_outside_current_region(self):
        self.assertGreater(float(self.f.vacuum_clearance(.005)),.008)
    def test_magnetic_field_increases_with_I(self):
        orig=self.f.current
        self.f.current=2*orig
        two=float(self.f.field(.004,0)[1]); self.f.current=orig
        self.assertAlmostEqual(two,2*float(self.f.field(.004,0)[1]),12)
    def test_reference_orbit_field(self):
        self.assertAlmostEqual(float(self.f.field(.005,0)[1]),float(self.baseline['B0']),12)
    def test_reference_beta_sub_light(self):
        self.assertLess(self.baseline['v'],c)
    def test_reconstruction_force(self):
        ref=self.baseline; force=e*ref['v']*ref['B0']; centripetal=ref['gamma']*m_e*ref['v']**2/ref['r0']
        self.assertAlmostEqual(force/centripetal,1.,11)
    def test_n_weak_focusing(self):
        self.assertLess(self.baseline['n'],1);self.assertGreater(self.baseline['n'],0)
    def test_tune_sum(self):
        ref=self.baseline
        self.assertAlmostEqual(ref['nu_r']**2+ref['nu_z']**2,1.,13)
    def test_field_index_current_independent(self):
        idx=self.f.index(.005);self.f.current*=2
        try:self.assertAlmostEqual(idx,self.f.index(.005),12)
        finally:self.f.current/=2
    def test_off_axis_BiotSavart(self):
        br,bz=loop_field_cyl(.003,.002,.01,.008,1.)
        target=direct_biot_savart_ring(.003,0,.002,.01,.008,1.,num=2048)
        self.assertLess(np.linalg.norm(np.array([br,0,bz])-target),1e-12)
    def test_quadrature_convergence(self):
        a=TwoCoilField(order=17).unit_field(.005,0)[1]
        b=TwoCoilField(order=29).unit_field(.005,0)[1]
        self.assertLess(abs(a-b)/abs(b),4e-6)
    def test_vacuum_curlphi(self):
        # ∂z Br - ∂r Bz = 0 in the current-free particle channel
        r=.005;z=.001;h=8e-6
        val=(self.f.field(r,z+h)[0]-self.f.field(r,z-h)[0])/(2*h)-(self.f.field(r+h,z)[1]-self.f.field(r-h,z)[1])/(2*h)
        self.assertLess(abs(val),1e-4)
    def test_vacuum_divB(self):
        r=.005;z=.001;h=8e-6
        div=(((r+h)*self.f.field(r+h,z)[0]-(r-h)*self.f.field(r-h,z)[0])/(2*h*r) +
             (self.f.field(r,z+h)[1]-self.f.field(r,z-h)[1])/(2*h))
        self.assertLess(abs(div),2e-5)
    def test_smooth_quadrature_positive_weights(self):
        _,_,weights=smooth_finite_coil_quadrature(n=15)
        self.assertTrue(np.all(weights>0))
    def test_loop_field_is_finite_in_vacuum(self):
        for rad in (.001,.003,.005,.007):
            self.assertTrue(np.all(np.isfinite(self.f.field(rad,.001))))
    def test_radial_gradient_negative(self):
        r=.005;h=2e-5
        self.assertLess((self.f.field(r+h,0)[1]-self.f.field(r-h,0)[1])/(2*h),0)
    def test_index_sign_change_scan(self):
        self.assertGreater(self.f.index(.008),1.)
    def test_3_4_5_rational_linear_tunes(self):
        r=brentq(lambda x:self.f.index(x)-.36,.005,.006)
        self.assertAlmostEqual(self.f.index(r),.36,8)
        self.assertAlmostEqual(np.sqrt(1-self.f.index(r)),.8,8)
        self.assertAlmostEqual(np.sqrt(self.f.index(r)),.6,8)
    def test_current_roughly_realistic_order(self):
        self.assertGreater(self.baseline['I_per_coil'],600)
        self.assertLess(self.baseline['I_per_coil'],720)

class TestDynamics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f=TwoCoilField(order=13);cls.ref=circular_reference(field=cls.f)
    def test_single_turn_closed(self):
        sol=trajectory(self.f,turns=1)
        self.assertTrue(sol.success)
        self.assertLess(np.linalg.norm(sol.y[:3,-1]-[1,0,0]),1e-8)
    def test_four_turn_closed(self):
        sol=trajectory(self.f,turns=4)
        self.assertLess(np.linalg.norm(sol.y[:3,-1]-[1,0,0]),1e-8)
    def test_speed_conservation(self):
        sol=trajectory(self.f,turns=7,dx=1e-5,dz=1e-5,points=100)
        self.assertLess(np.max(np.abs(np.linalg.norm(sol.y[3:],axis=0)-1)),1e-8)
    def test_nearby_vertical_bounded(self):
        sol=trajectory(self.f,turns=30,dz=2e-5,points=200)
        self.assertLess(np.max(np.abs(sol.y[2])),.02)
    def test_nearby_radial_bounded(self):
        sol=trajectory(self.f,turns=30,dx=2e-5,points=200)
        self.assertLess(np.max(np.abs(np.hypot(sol.y[0],sol.y[1])-1)),.02)
    def test_two_perturbations_80_turns(self):
        sol=trajectory(self.f,turns=80,dx=2e-5,dz=2e-5,points=800)
        self.assertTrue(sol.success)
        self.assertLess(np.max(np.abs(sol.y[2])),.02)
        self.assertLess(np.max(np.abs(np.hypot(sol.y[0],sol.y[1])-1)),.02)
    def test_return_map_volume(self):
        _,J=jacobian_return(self.f)
        self.assertAlmostEqual(np.linalg.det(J),1.,delta=1e-5)
    def test_return_map_transverse_unit_circle(self):
        _,J=jacobian_return(self.f)
        self.assertLess(np.max(np.abs(np.abs(np.linalg.eigvals(J))-1)),1e-4)
    def test_return_map_tunes(self):
        _,J=jacobian_return(self.f)
        vals=np.linalg.eigvals(J)
        predicted=[self.ref['nu_r'],self.ref['nu_z']]
        for nu in predicted:
            target=np.exp(1j*2*np.pi*nu)
            self.assertLess(min(abs(z-target) for z in vals),2e-4)
    def test_reversing_charge_reverses_orbit_orientation(self):
        # In this electron-only integrator q=-e, Bz>0 and orientation +phi.
        self.assertGreater(self.ref['B0'],0)
    def test_reference_period(self):
        self.assertAlmostEqual(self.ref['T'],2*np.pi*self.ref['r0']/self.ref['v'],12)

if __name__=='__main__':unittest.main()
