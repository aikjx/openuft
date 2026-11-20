import sys,json,unittest
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from topology import load_v98_xyz,projected_crossings,fox_determinant,lifted_polygon,torus_knot
from dimensional_audit import audit
from variational import prepare,reduced_finite_difference
class TestV99(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=json.loads((ROOT/'results/V99_NUMERICAL_AUDIT_THEORY.json').read_text())
        cls.points=load_v98_xyz(ROOT/'inputs/V98_3D_TRAJECTORY.csv')
    def test_results_provenance(self):self.assertIn('NOT EXPERIMENT',self.result['classification'])
    def test_has_all_three_source_orders(self):self.assertEqual([x['order'] for x in self.result['intersection_crosscheck']],[13,17,21])
    def test_all_orders_have_four_intersections(self):
        for row in self.result['intersection_crosscheck']:
            with self.subTest(order=row['order']):self.assertEqual(len(row['intersections']),4)
    def test_distinct_times_each_intersection(self):
        for row in self.result['intersection_crosscheck']:
            for v in row['intersections']:
                self.assertGreater(v['t2_norm']-v['t1_norm'],2.)
    def test_source_independent_small_separations(self):
        for row in self.result['intersection_crosscheck']:
            for v in row['intersections']:self.assertLess(v['separation_m'],2e-12)
    def test_different_velocities_at_intersections(self):
        for row in self.result['intersection_crosscheck']:
            for v in row['intersections']:self.assertGreater(v['velocity_separation_over_v'],.005)
    def test_intersection_k_sequence(self):
        for row in self.result['intersection_crosscheck']:
            self.assertEqual([x['k'] for x in row['intersections']],[1,2,3,4])
    def test_return_closure_seed_small(self):
        for x in self.result['intersection_crosscheck']:self.assertLess(x['return_position_m'],2e-12)
    def test_raw_projected_crossings(self):self.assertEqual(len(projected_crossings(self.points)),32)
    def test_raw_topology_rejected(self):
        with self.assertRaises(ValueError):fox_determinant(self.points)
    def test_raw_near_zero_crossing_height(self):
        self.assertLess(self.result['topology']['raw_min_height_gap_m'],1e-12)
    def test_trefoil_fox_3(self):self.assertEqual(fox_determinant(torus_knot(2,3),(.4,.2,.88),1e-8)['determinant'],3)
    def test_torus_2_5_fox_5(self):self.assertEqual(fox_determinant(torus_knot(2,5),(.4,.2,.88),1e-8)['determinant'],5)
    def test_unknot_determinant_1(self):self.assertEqual(fox_determinant(torus_knot(1,1),(.4,.2,.88),1e-8)['determinant'],1)
    def test_perturbed_is_not_physical(self):self.assertTrue(self.result['topology']['perturbed_polygon_is_NOT_physical_solution'])
    def test_perturbed_polygon_embedded_projection(self):
        q=lifted_polygon(self.points,1.5e-7)
        for view in ((0,0,1),(.45,.22,.866),(.55,.3,.77)):
            with self.subTest(view=view):self.assertGreater(fox_determinant(q,view,1e-10)['min_height_gap_m'],1e-8)
    def test_perturbed_knot_det_9(self):
        for item in self.result['topology']['lifted_polygon_knot_determinant_checks'].values():
            self.assertEqual(item['determinant'],9)
    def test_fd_trace_near_2(self):
        for x in self.result['reduced_map_finite_difference']:self.assertLess(abs(x['trace']-2),1e-7)
    def test_fd_det_near_1(self):
        for x in self.result['reduced_map_finite_difference']:self.assertLess(abs(x['det']-1),1e-7)
    def test_variational_trace_near_2(self):
        for x in self.result['reduced_map_variational']:self.assertLess(abs(x['trace']-2),1e-7)
    def test_variational_det_near_1(self):
        for x in self.result['reduced_map_variational']:self.assertLess(abs(x['det']-1),1e-7)
    def test_reduced_map_has_nontrivial_shear(self):
        self.assertGreater(abs(self.result['reduced_map_variational'][-1]['matrix'][1][0]),1e-5)
    def test_eigenvalues_stability_not_certified(self):self.assertIn('No certified full nonlinear stability',self.result['open'])
    def test_source_order_return_consistency(self):
        rows=self.result['intersection_crosscheck']
        x=[float(r['intersections'][0]['radius_m']) for r in rows]
        self.assertLess(max(x)-min(x),1e-7)
    def test_dimension_audit(self):self.assertGreaterEqual(audit()['count'],20)
    def test_flux_hold_p_phi_initial(self):
        model=prepare(json.loads((ROOT/'inputs/V98_SUMMARY.json').read_text()),source_order=13)
        y=model['initial'];u=model['init_on_section'](y[2],0)
        self.assertLess(np.linalg.norm(y-u),1e-9)
    def test_local_poincare_center_return(self):
        model=prepare(json.loads((ROOT/'inputs/V98_SUMMARY.json').read_text()),source_order=13)
        data=reduced_finite_difference(model,h=1e-5)
        self.assertLess(data['return_residual'],1e-7)
    def test_speed_is_subluminal(self):self.assertLess(json.loads((ROOT/'inputs/V98_SUMMARY.json').read_text())['conditions']['beta'],1)
if __name__=='__main__':unittest.main(verbosity=2)
