"""One command to execute all ROOT V92 mathematical/software checks; no experimental claims."""
import json,subprocess,sys,os,unittest,time
from pathlib import Path
from src.symbolic_proofs import prove
from src.dimension_audit import build as build_dims
from src.numerical_lab import run as simulate
from src.build_ledger import build as build_ledger
ROOT=Path(__file__).resolve().parents[1]

def main():
  t=time.monotonic()
  symbolic=prove(); dims=build_dims(); ledger=build_ledger(); numerical=simulate()
  suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'),pattern='test*.py',top_level_dir=str(ROOT))
  runner=unittest.TextTestRunner(verbosity=2)
  result=runner.run(suite)
  report={'version':'V92','label':'THEORETICAL_AND_SOFTWARE_VALIDATION_ONLY',
          'symbolic_checks':symbolic['checks'],'dimensional_checks':dims,
          'legacy_and_new_tasks':ledger,'magnetic_calculation_cases':numerical['n_cases_helix'],
          'independent_RK4_momentum_relative_drift':numerical['magnetic_independent_rk4']['momentum_rel_drift'],
          'independent_RK4_orbit_error_in_radii':numerical['magnetic_independent_rk4']['error_in_radii'],
          'unit_tests':result.testsRun,'unit_test_failures':len(result.failures),'unit_test_errors':len(result.errors),
          'elapsed_seconds':time.monotonic()-t,
          'four_force_unification_proved':False,'G_derived_independently':False,'v_equals_c_massive_physical':False,
          'scope':'Math/code verified within declared models; no hardware experiment performed.'}
  (ROOT/'results'/'ACCEPTANCE_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
  print(json.dumps(report,ensure_ascii=False,indent=2))
  if not result.wasSuccessful():raise SystemExit(1)
  return report
if __name__=='__main__':main()
