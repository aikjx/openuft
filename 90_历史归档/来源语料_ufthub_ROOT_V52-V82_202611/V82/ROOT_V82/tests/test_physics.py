import unittest, math, json
from pathlib import Path
from src.gravitylab import *
ROOT=Path(__file__).resolve().parents[1]
class TestGravity(unittest.TestCase):
    def test_mass_reversal(self):
        a=gravity_vector((0,0,0),100,(.5,0,0))[0]
        b=gravity_vector((0,0,0),100,(-.5,0,0))[0]
        self.assertAlmostEqual(a,-b,delta=1e-22)
    def test_mass_value(self):self.assertAlmostEqual(gravity_vector((0,0,0),100,(.5,0,0))[0],G*400,delta=1e-20)
    def test_gravity_units(self): self.assertAlmostEqual(gravity_vector((0,0,0),4,(2,0,0))[0],G,delta=1e-20)
    def test_gravity_zero_mass(self):self.assertEqual(gravity_vector((0,0,0),0,(2,0,0)),(0,0,0))
    def test_bad_source(self):
        with self.assertRaises(ValueError):gravity_vector((0,0,0),1,(0,0,0))
    def test_bad_mass(self):
        with self.assertRaises(ValueError):gravity_vector((0,0,0),-1,(1,0,0))
    def test_near_sphere_center(self):self.assertEqual(sphere_gravity(100,.2,0),0)
    def test_sphere_boundary_continuity(self):self.assertAlmostEqual(sphere_gravity(100,.2,.2*(1-1e-10)),sphere_gravity(100,.2,.2*(1+1e-10)),delta=3e-17)
    def test_shell_theorem(self):self.assertEqual(sphere_gravity(100,.2,1),G*100)
    def test_r_inv_square(self):
        a=sphere_gravity(100,.2,1);b=sphere_gravity(100,.2,2)
        self.assertAlmostEqual(a/b,4,places=10)
    def test_mass_linear(self):self.assertAlmostEqual(sphere_gravity(200,.2,1)/sphere_gravity(100,.2,1),2)
    def test_mass_location_rotate(self):
        x=gravity_vector((0,0,0),100,(1,0,0));y=gravity_vector((0,0,0),100,(0,1,0))
        self.assertAlmostEqual(x[0],y[1],places=20)
    def test_G_relation(self):self.assertAlmostEqual((G*C/2)*2/C,G)
    def test_redshift(self):self.assertAlmostEqual(relativistic_frequency_shift(9.81,.001),1.0915e-19,delta=1e-23)
    def test_centrifugal(self):self.assertEqual(rotation_effect(2,3),12)
class TestEM(unittest.TestCase):
    def test_zero(self):self.assertEqual(em_energy(E=0,B=0,volume=1),0)
    def test_field_flip(self):self.assertAlmostEqual(em_energy(B=10),em_energy(B=-10))
    def test_square_scaling(self):self.assertAlmostEqual(em_energy(B=2)/em_energy(B=1),4)
    def test_volume(self):self.assertAlmostEqual(em_energy(B=1,volume=2)/em_energy(B=1,volume=1),2)
    def test_c_factor(self):self.assertAlmostEqual(mass_equivalent(C*C),1)
    def test_em_far_scaling(self):self.assertAlmostEqual(monopole_gravity_bound(1e6,5)/monopole_gravity_bound(1e6,10),4)
    def test_field_delta(self):self.assertAlmostEqual(field_energy_change(0,2,1),em_energy(B=2))
    def test_EB_self(self):self.assertAlmostEqual(em_energy(E=0,B=1),1/(2*MU0))
    def test_epsilon_consistency(self):self.assertAlmostEqual(MU0*EPS0*C*C,1,places=12)
    def test_interference_positive(self):self.assertAlmostEqual(em_energy(E=1e6)+em_energy(E=1e6)+EPS0*1e12,em_energy(E=2e6))
    def test_interference_destructive(self):self.assertEqual(em_energy(E=1e6-1e6),0)
    def test_negative_energy_change(self):self.assertLess(field_energy_change(1,0,1),0)
    def test_uncertainty_mass(self):self.assertAlmostEqual(point_mass_uncertainty(10,1,1,0),.1)
    def test_uncertainty_distance(self):self.assertAlmostEqual(point_mass_uncertainty(10,1,0,.01),.02)
    def test_em_point_nonexact_note(self):self.assertTrue(monopole_gravity_bound(1e6,10)>0)
class TestProtocol(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.protocols={f.stem.split('protocol_')[1]:json.loads(f.read_text(encoding='utf-8')) for f in (ROOT/'spec').glob('protocol_*.json')}
    def test_three_protocols(self):self.assertEqual(len(self.protocols),3)
    def test_each_valid(self):
        for p in self.protocols.values():self.assertTrue(validate_protocol(p))
    def test_mass_expected(self):
        p=self.protocols['source_mass'];self.assertAlmostEqual(predict(p)['amplitude_m_s2'],2.66972e-8,delta=1e-18)
    def test_em_prediction(self):
        p=self.protocols['em_energy'];self.assertLess(predict(p)['far_field_monopole_m_s2'],1e-23)
    def test_dummy_zero(self):self.assertEqual(predict(self.protocols['dummy_null'])['amplitude_m_s2'],0)
    def test_bad_provenance(self):
        p=json.loads(json.dumps(self.protocols['source_mass']));p['data_provenance']='measured'
        with self.assertRaises(ValueError):validate_protocol(p)
    def test_bad_version(self):
        p=json.loads(json.dumps(self.protocols['source_mass']));p['version']='old'
        with self.assertRaises(ValueError):validate_protocol(p)
    def test_bad_noise(self):
        p=json.loads(json.dumps(self.protocols['source_mass']));p['design']['noise_sigma_m_s2']=-1
        with self.assertRaises(ValueError):validate_protocol(p)
    def test_bad_block(self):
        p=json.loads(json.dumps(self.protocols['source_mass']));p['design']['randomized_blocks']=False
        with self.assertRaises(ValueError):validate_protocol(p)
    def test_bad_count(self):
        p=json.loads(json.dumps(self.protocols['source_mass']));p['design']['samples']=255
        with self.assertRaises(ValueError):validate_protocol(p)
    def test_balanced(self):
        rows,_=simulate(self.protocols['source_mass']);self.assertEqual(sum(r['switch'] for r in rows),0)
    def test_reproducible(self):
        rows1,r1=simulate(self.protocols['source_mass']);rows2,r2=simulate(self.protocols['source_mass'])
        self.assertEqual(rows1,rows2);self.assertEqual(r1,r2)
    def test_signal_recovery(self):
        p=self.protocols['source_mass'];_,res=simulate(p)
        self.assertLess(abs(res['fitted_amplitude_m_s2']-res['input_amplitude_m_s2']),4*res['white_noise_standard_error_m_s2'])
    def test_null_within_four_sigma(self):
        p=self.protocols['dummy_null'];_,res=simulate(p)
        self.assertLess(abs(res['fitted_amplitude_m_s2']),4*res['white_noise_standard_error_m_s2'])
    def test_em_zero_injected(self):
        p=self.protocols['em_energy'];_,res=simulate(p)
        self.assertEqual(res['input_amplitude_m_s2'],0)
    def test_switch_artifact_aliasing(self):
        p=json.loads(json.dumps(self.protocols['source_mass']));p['design']['switch_correlated_artifact_m_s2']=1e-8
        _,with_artifact=simulate(p)
        p['design']['switch_correlated_artifact_m_s2']=0
        _,without_artifact=simulate(p)
        self.assertAlmostEqual(with_artifact['fitted_amplitude_m_s2']-without_artifact['fitted_amplitude_m_s2'],1e-8,delta=1e-20)
    def test_collinear_solver(self):
        with self.assertRaises(ValueError): solve_linear([[1,1],[2,2]],[1,2])
    def test_structural_rank(self):self.assertEqual(structural_degeneracy()['rank'],1)
    def test_uncertainty_with_G(self):self.assertGreater(point_mass_uncertainty(100,.5,0,0,include_G=True),0)
    def test_fit_drifts(self):
        p=json.loads(json.dumps(self.protocols['source_mass']));p['design']['linear_drift_total_m_s2']=2e-7
        _,res=simulate(p);self.assertLess(abs(res['fitted_amplitude_m_s2']-res['input_amplitude_m_s2']),4*res['white_noise_standard_error_m_s2'])
if __name__=='__main__':unittest.main()
