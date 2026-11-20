"""Model-level tests; not proof of an experimentally realized effect."""
import unittest,math
import numpy as np
from scipy.constants import c,e,m_e
from v97_core import (
    primitive_pythagorean_resonances, TwoCoilField, tune_radius,
    circular_reference, planar_return, shoot_planar_resonance,
    five_turn_fixed_time, independent_planar_apsidal_angle,
    canonical_angular_momentum_relative_error,circular_radiation_per_turn,
    normalized_rhs)

class TestPythagoreanClassification(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.triples=primitive_pythagorean_resonances(100)
    def test_first(self): self.assertEqual(self.triples[0]['triple'],'4:3:5')
    def test_minimal_five(self): self.assertEqual(min(x['N'] for x in self.triples),5)
    def test_all_integer_identity(self):
        for x in self.triples:self.assertEqual(x['a']**2+x['b']**2,x['N']**2)
    def test_all_primitive(self):
        for x in self.triples:self.assertEqual(math.gcd(x['a'],x['b']),1)
    def test_n_in_interval(self):
        for x in self.triples:self.assertTrue(0<x['n_index']<1)
    def test_tune_sum(self):
        for x in self.triples:self.assertAlmostEqual(x['nu_r']**2+x['nu_z']**2,1,places=14)
    def test_3_4_5(self): self.assertEqual(self.triples[0]['n_index'],.36)
    def test_5_12_13(self): self.assertEqual(self.triples[1]['N'],13)
    def test_8_15_17(self): self.assertEqual(self.triples[2]['N'],17)
    def test_number_bounded(self): self.assertTrue(all(x['N']<=100 for x in self.triples))
    def test_special_case_empty(self): self.assertEqual(primitive_pythagorean_resonances(4),[])

class TestPhysicalModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.field=TwoCoilField(order=17)
        cls.r0=tune_radius(cls.field)
        cls.shoot=shoot_planar_resonance(cls.field,linear_root=cls.r0)
    def test_radius(self): self.assertTrue(.0051<self.r0<.0052)
    def test_index(self): self.assertAlmostEqual(self.field.index(self.r0),9/25,places=8)
    def test_linear_tunes(self):
        d=circular_reference(r0=self.r0,field=self.field)
        self.assertAlmostEqual(d['nu_r'],.8,places=6)
        self.assertAlmostEqual(d['nu_z'],.6,places=6)
    def test_vacuum_clearance(self):self.assertGreater(self.field.vacuum_clearance(self.r0),.008)
    def test_current_finite(self):
        d=circular_reference(r0=self.r0,field=self.field)
        self.assertTrue(500<d['I_per_coil']<800)
    def test_positive_beta(self):
        ref=circular_reference(r0=self.r0,field=self.field)
        self.assertLess(ref['v'],c)
    def test_bracket(self):
        self.assertLess(self.shoot['bracket_phase_rad'][0],0)
        self.assertGreater(self.shoot['bracket_phase_rad'][1],0)
    def test_nonlinear_shift_nonzero(self):
        self.assertTrue(-100e-9<self.shoot['nonlinear_shift_m']<-60e-9)
    def test_planar_phase(self): self.assertLess(abs(self.shoot['phase_error_rad']),1e-8)
    def test_planar_position_return(self):self.assertLess(self.shoot['return_position_error_m'],1e-10)
    def test_planar_velocity_return(self):self.assertLess(self.shoot['return_velocity_relative'],1e-7)
    def test_planar_position_z(self):self.assertLess(abs(self.shoot['final_state'][2]),1e-12)
    def test_planar_velocity_vz(self):self.assertLess(abs(self.shoot['final_state'][5]),1e-12)
    def test_five_turn_phase(self): self.assertLess(abs(self.shoot['phi_radians']-10*np.pi),1e-8)
    def test_inner_turning_less(self):
        d=independent_planar_apsidal_angle(self.field,self.shoot['r0_m'],quad_n=24)
        self.assertLess(d['inner_turning_m'],self.shoot['r0_m'])
    def test_independent_quadrature(self):
        d=independent_planar_apsidal_angle(self.field,self.shoot['r0_m'],quad_n=24)
        self.assertLess(abs(d['four_cycle_phase_error_rad']),2e-6)
    def test_canonical_conservation(self):
        circular_reference(r0=self.shoot['r0_m'],field=self.field) # restore mutable field current
        self.assertLess(canonical_angular_momentum_relative_error(
            self.field,self.shoot['r0_m'],self.shoot['orbit']),3e-8)
    def test_speed_conservation(self):
        y=self.shoot['orbit'].y
        self.assertLess(float(np.max(np.abs(np.linalg.norm(y[3:],axis=0)-1))),1e-9)
    def test_static_magnetic_no_work(self):
        y=self.shoot['orbit'].y[:,len(self.shoot['orbit'].t)//2]
        R=y[:3]*self.shoot['r0_m']; B=self.field.field_cart(*R)
        self.assertAlmostEqual(float(np.dot(y[3:],np.cross(y[3:],B))),0,places=14)
    def test_reference_v_less_c(self):self.assertLess(.1*c,c)
    def test_radiation_nonzero(self):
        d=circular_radiation_per_turn(.1,self.shoot['r0_m'])
        self.assertGreater(d['radiated_power_W'],0)
        self.assertLess(d['energy_per_turn_J']/d['electron_kinetic_energy_J'],1e-8)
    def test_reference_five_turn_not_nonlinear_closed(self):
        d=five_turn_fixed_time(self.field,self.r0,dx=30e-6,dz=30e-6)
        self.assertGreater(d['position_return_m'],1e-9)
    def test_amplitude_detuning_trend(self):
        small=five_turn_fixed_time(self.field,self.r0,dx=5e-6,dz=5e-6)
        large=five_turn_fixed_time(self.field,self.r0,dx=30e-6,dz=30e-6)
        self.assertGreater(large['position_return_m'],5*small['position_return_m'])
    def test_10e_30e_root_continuation(self):
        shot10=shoot_planar_resonance(self.field,amplitude=10e-6,linear_root=self.r0)
        self.assertGreater(shot10['r0_m'],self.shoot['r0_m'])
        self.assertLess(shot10['return_position_error_m'],1e-9)
    def test_field_gradient(self):
        self.assertLess(self.field.field(self.r0+1e-5,0)[1],self.field.field(self.r0-1e-5,0)[1])
    def test_reference_circle_force(self):
        ref=circular_reference(r0=self.r0,field=self.field)
        force=e*ref['v']*ref['B0']
        self.assertAlmostEqual(force,ref['gamma']*m_e*ref['v']**2/self.r0,delta=force*1e-12)

if __name__=='__main__':unittest.main()
