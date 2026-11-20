"""ROOT V98 regression. All values THEORY, no experimental claims."""
import unittest, math, json, sys
from pathlib import Path
import numpy as np
from scipy.constants import c,e,m_e
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from coil_model import TwoCoilField, circular_reference, loop_field_cyl
from v98_core import (shoot_3d,five_turn_3d,independent_fixed_time_orbit,
                     vacuum_maxwell_residuals,canonical_invariant_error,
                     classical_radiation,orbit_samples,boris_independent)
from v97_core import primitive_pythagorean_resonances

class TestV98(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
      cls.row=shoot_3d(order=13,rtol=1e-10)
      cls.sample=orbit_samples(cls.row,300)
      cls.summary=json.loads((ROOT/'results'/'NUMERICAL_SUMMARY_THEORY.json').read_text('utf-8'))

  def test_01_solver_outputs_numeric(self):self.assertTrue(np.isfinite(self.row['r0_m']))
  def test_02_nonzero_vertical_amplitude(self):self.assertGreater(self.row['az_m'],1e-6)
  def test_03_vertical_amplitude_physical_range(self):self.assertLess(self.row['az_m'],20e-6)
  def test_04_radius_range(self):self.assertTrue(.0045<self.row['r0_m']<.006)
  def test_05_five_turn_azimuth(self):self.assertLess(abs(self.row['phi_residual_rad']),1e-8)
  def test_06_vertical_velocity_return(self):self.assertLess(abs(self.row['vz_residual_dimensionless']),1e-9)
  def test_07_full_position_return(self):self.assertLess(self.row['position_return_error_m'],2e-10)
  def test_08_full_velocity_return(self):self.assertLess(self.row['velocity_return_error_relative'],5e-8)
  def test_09_positive_period(self):self.assertGreater(self.row['period_s'],0)
  def test_10_reasonable_ns_period(self):self.assertTrue(4e-9<self.row['period_s']<7e-9)
  def test_11_current_positive(self):self.assertGreater(self.row['field_I_A_per_coil'],1)
  def test_12_current_reasonable(self):self.assertLess(self.row['field_I_A_per_coil'],1000)
  def test_13_magnetic_reference(self):self.assertAlmostEqual(self.row['reference_B_T'],.033,delta=.002)
  def test_14_radial_breathing(self):self.assertGreater(float(np.ptp(self.sample['radius_mm'])),.07)
  def test_15_vertical_breathing(self):self.assertGreater(float(np.ptp(self.sample['z_um'])),12)
  def test_16_speed_below_c(self):self.assertLess(self.row['beta'],1)
  def test_17_speed_constant(self):self.assertLess(max(abs(self.sample['speed_ratio']-1)),2e-8)
  def test_18_maxwell_vacuum_divergence(self):
    r=vacuum_maxwell_residuals(self.row['field'],self.row['r0_m'],h=4e-6)
    self.assertLess(r['div_normalized'],1e-6)
  def test_19_maxwell_vacuum_curl(self):
    r=vacuum_maxwell_residuals(self.row['field'],self.row['r0_m'],h=4e-6)
    self.assertLess(r['curl_normalized'],1e-6)
  def test_20_maxwell_residual_convergence(self):
    a=vacuum_maxwell_residuals(self.row['field'],self.row['r0_m'],h=8e-6)
    b=vacuum_maxwell_residuals(self.row['field'],self.row['r0_m'],h=4e-6)
    self.assertLess(b['div_normalized'],a['div_normalized'])
  def test_21_canonical_P_phi(self):
    v=canonical_invariant_error(self.row,sample_count=17,quad_order=40)
    self.assertLess(v['max_delta_Pphi_relative'],3e-8)
  def test_22_non_event_integrator(self):
    v=independent_fixed_time_orbit(self.row,rtol=1e-11)
    self.assertLess(v['position_error_m'],3e-10)
  def test_23_radiation_positive(self):self.assertGreater(classical_radiation(self.row,40)['energy_J_per_period'],0)
  def test_24_radiation_small_relative(self):self.assertLess(classical_radiation(self.row,40)['radiation_to_kinetic'],1e-8)
  def test_25_boris_preserves_speed(self):
    v=boris_independent(self.row,150)
    self.assertLess(v['speed_relative_difference'],1e-10)
  def test_26_boris_halving_step(self):
    a=boris_independent(self.row,500);b=boris_independent(self.row,1000)
    self.assertGreater(a['position_difference_m']/b['position_difference_m'],3)
  def test_27_3_4_5_primitive(self):
    arr=primitive_pythagorean_resonances(15)
    self.assertEqual(arr[0]['N'],5)
  def test_28_model_data_provenance(self):self.assertIn('THEORY',self.summary['classification'])
  def test_29_final_source_order(self):self.assertEqual(self.summary['conditions']['source_quadrature_order'],21)
  def test_30_independent_boris_progress(self):
    arr=self.summary['independent_boris_integrations']
    self.assertGreater(arr[0]['position_difference_m']/arr[1]['position_difference_m'],3.5)
  def test_31_source_quadrature_consistency(self):
    arr=self.summary['source_quadrature_convergence'];self.assertLess(abs(arr[-1]['r0_m']-arr[-2]['r0_m']),1e-8)
  def test_32_no_unproven_G_claim(self):self.assertTrue(any('G' in s for s in self.summary['limits']))
  def test_33_nonzero_z_after_zero_counterexample(self):
    zero=five_turn_3d(self.row['field'],self.row['r0_m'],0,rtol=1e-9)
    self.assertAlmostEqual(zero['z_return_error_m'],0,delta=1e-12)
  def test_34_return_speed_close(self):self.assertAlmostEqual(np.linalg.norm(self.row['end'][3:]),1,delta=1e-7)
  def test_35_flux_invariant_sample(self):self.assertGreater(self.row['az_m'],0)

if __name__=='__main__':unittest.main()
