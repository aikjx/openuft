#!/usr/bin/env python3
"""ROOT V87 one-click reproducibility.
Standard mode does not require Chromium; optional --browser invokes headless Chromium.
"""
from pathlib import Path
import sys,subprocess,os,json,re,hashlib
root=Path(__file__).resolve().parent

def run(step,cmd):
 p=subprocess.run([sys.executable,*cmd],cwd=root,capture_output=True,text=True)
 if p.returncode:
  print(f'FAILED: {step}\nSTDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}',file=sys.stderr)
  raise SystemExit(p.returncode)
 print(f'PASS: {step}')
 return p.stdout,p.stderr

def main():
 run('build equation catalog',['scripts/build_catalog.py'])
 run('build four experimental protocols',['scripts/build_protocols.py'])
 out,err=run('Python mathematical and provenance tests',['-m','unittest','discover','-s','tests','-p','test_*.py','-q'])
 m=re.search(r'Ran\s+(\d+)\s+tests',out+'\n'+err)
 if not m:raise RuntimeError('unittest count missing')
 count=int(m.group(1))
 if count<100:raise RuntimeError('insufficient test suite')
 stdout,_=run('independent SymPy symbolic checks',['tests/symbolic_checks.py'])
 symbolic=json.loads(stdout)
 if symbolic['total']<18:raise RuntimeError('symbolic audit incomplete')
 run('generate theory curves + synthetic records',['scripts/generate_results.py'])
 brows=None
 if '--browser' in sys.argv:
  stdout,_=run('Chromium UI functional checks',['web/browser_smoke.py'])
  brows=json.loads(stdout)
 else:
  f=root/'results/browser_verification.json'
  if f.exists():brows=json.loads(f.read_text(encoding='utf8'))
 summary=json.loads((root/'results/numerical_summary.json').read_text(encoding='utf8'))
 equations=json.loads((root/'results/equation_count.json').read_text(encoding='utf8'))
 import csv
 with (root/'data/method_matrix.csv').open(encoding='utf-8-sig') as f:method_count=len(list(csv.DictReader(f)))
 report={
  'research_version':'ROOT V87',
  'date':'2026-11-18',
  'science_status':'LIMITED_KNOWN_LOW_ENERGY_BRIDGE_NOT_FULL_UNIFICATION',
  'python_tests_passed':count,
  'symbolic_checks_passed':symbolic['total'],
  'browser_checks_previously_passed':brows['passed'] if brows else None,
  'browser_provenance':brows.get('render_strategy') if brows else None,
  'catalog_equations':equations['count'],
  'method_matrix_entries':method_count,
  'experiment_protocols':len(list((root/'protocols').glob('*.json'))),
  'gaussian_integral_verification':json.loads((root/'results/independent_integral_check.json').read_text()),
  'representative_earth_1m_clock_fractional':summary['earth_static_clock_1m_fractional'],
  'representative_source_phase_rad':summary['rb87_spherical_phase_source_100kg_0p3m_0p01m_1s']['phase_rad'],
  'all_observations_real':False,
  'all_observations_theory_or_synthetic':True,
  'quantum_gravity_proven':False,
  'G_independently_predicted':False,
  'four_forces_unified':False,
  'full_unification_completion_claim':'NOT_ACHIEVED'
 }
 (root/'results/verification_report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8')
 print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
