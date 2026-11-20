"""Independent quick tests; full numerical regeneration is opt-in."""
import sys,subprocess,os,json,zipfile,tempfile,hashlib,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def invoke(argv, cwd=ROOT, env=None):
 print('RUN:', ' '.join(map(str,argv)),flush=True)
 result=subprocess.run(argv,cwd=cwd,env=env,check=False)
 if result.returncode:raise SystemExit(f'failed: {argv}, exit={result.returncode}')

def main():
 parser=argparse.ArgumentParser()
 parser.add_argument('--regenerate',action='store_true')
 parser.add_argument('--historical',action='store_true')
 parser.add_argument('--browser',action='store_true')
 args=parser.parse_args()
 env=os.environ.copy();env['PYTHONPATH']=str(ROOT/'src')
 if not args.regenerate and (ROOT/'CHECKSUMS.sha256').exists():
  invoke([sys.executable,'verify_checksums.py'])
 if args.regenerate:
  invoke([sys.executable,'src/generate_results.py'],env=env)
  invoke([sys.executable,'src/finalize_results.py'],env=env)
  invoke([sys.executable,'src/build_web.py'])
 invoke([sys.executable,'-m','unittest','discover','-s','tests','-v'],env=env)
 invoke([sys.executable,'src/symbolic_audit.py'],env=env)
 info=json.loads((ROOT/'results/NUMERICAL_SUMMARY_THEORY.json').read_text(encoding='utf-8'))
 assert info['classification']['first_primitive_resonance']['N']==5
 assert info['nonlinear_planar_periodic_orbit']['return_position_error_m']<1e-9
 import csv
 with (ROOT/'ledger/ALL_277_ISSUES.csv').open(encoding='utf-8-sig') as f:
  assert len(list(csv.DictReader(f)))==277
 if args.historical:
  with tempfile.TemporaryDirectory() as tmp:
   with zipfile.ZipFile(ROOT/'archive'/'ROOT_V96_original.zip') as z:z.extractall(tmp)
   directories=[p for p in Path(tmp).iterdir() if p.is_dir()]
   if len(directories)!=1:raise RuntimeError('unexpected V96 archive layout')
   prior=directories[0]
   henv=env.copy();henv['PYTHONPATH']=str(prior/'src')
   invoke([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=prior,env=henv)
 if args.browser:invoke([sys.executable,'web/browser_smoke.py'])
 print('ROOT V97 quick verification completed; MODEL/NUMERIC only, not experimental validation.')
if __name__=='__main__':main()
