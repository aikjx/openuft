"""Reconcile the static numeric catalog after any generator bug fix; append source-refinement cross-check."""
from pathlib import Path
from csv import DictWriter
from v97_core import primitive_pythagorean_resonances,TwoCoilField,tune_radius,shoot_planar_resonance
import json
root=Path(__file__).resolve().parents[1]
r=root/'results'
triples=primitive_pythagorean_resonances(100)
with (r/'PYTHAGOREAN_TUNE_CATALOG_THEORY.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=DictWriter(f,fieldnames=triples[0].keys());w.writeheader();w.writerows(triples)
d=json.loads((r/'NUMERICAL_SUMMARY_THEORY.json').read_text())
d['classification']['number_of_primitive_resonances_N_le_100']=len(triples)
d['classification']['first_primitive_resonance']=triples[0]
conv=d['field_quadrature_convergence']
for order in (37,41,49):
 f=TwoCoilField(order=order)
 lr=tune_radius(f)
 s=shoot_planar_resonance(f,amplitude=30e-6,linear_root=lr)
 conv.append({'source_order':order,'linear_radius_m':lr,
      'nonlinear_closed_radius_m':s['r0_m'],
      'phase_residual_rad':s['phase_error_rad'],
      'section_position_error_m':s['return_position_error_m']})
d['numerical_uncertainty_notes']={
 'ode_return_position_m':d['nonlinear_planar_periodic_orbit']['return_position_error_m'],
 'source_quadrature_21_vs_49_radius_delta_m':abs(next(x for x in conv if x['source_order']==21)['nonlinear_closed_radius_m']-next(x for x in conv if x['source_order']==49)['nonlinear_closed_radius_m']),
 'source_quadrature_37_vs_49_radius_delta_m':abs(next(x for x in conv if x['source_order']==37)['nonlinear_closed_radius_m']-next(x for x in conv if x['source_order']==49)['nonlinear_closed_radius_m']),
 'interpretation':'ODE residual is not experimental accuracy; source quadrature converges less rapidly.'}
with (r/'SOURCE_QUADRATURE_PERIODIC_CONVERGENCE_THEORY.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=DictWriter(f,fieldnames=conv[0].keys());w.writeheader();w.writerows(conv)
(r/'NUMERICAL_SUMMARY_THEORY.json').write_text(json.dumps(d,ensure_ascii=False,indent=2))
print(json.dumps({'first':triples[0],'catalog_count':len(triples),'uncertainty':d['numerical_uncertainty_notes']},indent=2))
