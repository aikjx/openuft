"""Scientific-claim gates: report the difference between test status and physical evidence."""
import json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
summary=json.loads((ROOT/'results/summary.json').read_text(encoding='utf-8'))
checks={
    'has_JPL_input_values':True,
    'mathematical_finite_sphere_integral_crosschecked':summary['status']['mathematical_kernel_crosscheck'],
    'external_raw_gravity_observations_ingested':summary['assumptions']['observational_data_ingested'],
    'novel_force_observed':summary['status']['new_gravity_detected'],
    'four_force_unification_proven':summary['status']['four_force_unification_proved'],
    'fundamental_G_derived_without_empirical_input':False,
    'helix_generates_SM_gauge_group_derived':False,
    'full_energy_momentum_and_quantum_consistency_proven':False,
}
report={
  'scientific_status':'UNPROVEN_AND_NOT_EMPIRICALLY_VALIDATED',
  'numerical_tests':'PASS',
  'claim_gates':checks,
  'conclusion':'Finite-size Yukawa is calculable but illustrative parameters produce a substantial surface-gravity discrepancy. Do not label unified field theory as proven.',
}
(ROOT/'results/claims_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('CLAIM AUDIT:', report['scientific_status'])
for k,v in checks.items():print(('YES' if v else 'NO '),k)
