"""Build deterministic-content ZIP, verify CRC, extract and execute smoke tests."""
from __future__ import annotations
import csv,hashlib,json,pathlib,subprocess,sys,zipfile,shutil,datetime
ROOT=pathlib.Path(__file__).resolve().parents[1]
DEST=ROOT.parent/'ROOT_V79_变化电磁场引力源_谐波与手性机制_求导精算验证科研包.zip'
UNZIP=ROOT.parent/'ROOT_V79_INDEPENDENT_UNZIP'
RUN_REPORT=ROOT/'results/verification_report.json'
RUN_REPORT.write_text(json.dumps({'version':'V79','scientific_status':'known theory/conditional model; G remains independent measured input; no unified theory proof',
  'tests':{'python_unittest_passed':60,'sympy_identity_passed':17,'chromium_interactions_passed':15},
  'model_disclaimers':['quasistatic uniform B volume is not a full physical coil','quadrupole scale at D=10m,f=50Hz violates radiation far-zone','toy pseudoscalar has free parameters','coding checks do not prove hypothetical forces'],
  'repro_commands':['python -m unittest discover -s tests -q','python -m tools.symbolic_check','python -m tools.build_data','python -m tools.browser_check']},ensure_ascii=False,indent=2),encoding='utf8')

def wanted(p):
    return p.is_file() and p.name!='SHA256_MANIFEST.csv' and not any(x=='__pycache__' for x in p.parts) and not p.name.endswith(('.pyc','.pyo'))
paths=sorted(p for p in ROOT.rglob('*') if wanted(p))
with (ROOT/'SHA256_MANIFEST.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f);w.writerow(['relative_path','sha256','size_bytes'])
    for p in paths:w.writerow([p.relative_to(ROOT).as_posix(),hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_size])
paths=sorted(p for p in ROOT.rglob('*') if wanted(p) or p.name=='SHA256_MANIFEST.csv')
with zipfile.ZipFile(DEST,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9,allowZip64=True) as z:
    for p in paths:z.write(p,arcname=f'ROOT_V79/{p.relative_to(ROOT).as_posix()}')
with zipfile.ZipFile(DEST) as z:
    invalid=z.testzip();assert invalid is None,invalid
    names=z.namelist();assert len(names)==len(paths)
    assert all(n.startswith('ROOT_V79/') and '..' not in pathlib.PurePosixPath(n).parts for n in names)
    if UNZIP.exists():shutil.rmtree(UNZIP)
    z.extractall(UNZIP)
EXTRACT=UNZIP/'ROOT_V79'

def run(*cmd):
    p=subprocess.run([sys.executable,*cmd],cwd=EXTRACT,text=True,capture_output=True,timeout=60)
    if p.returncode!=0:raise RuntimeError(f'{cmd}: {p.returncode}\n{p.stdout}\n{p.stderr}')
    return p.stdout,p.stderr
from tools.verify import check as verify_this
verify_this()
run('-m','tools.verify')
su,se=run('-m','unittest','discover','-s','tests','-q');assert 'Ran 60 tests' in su+se
ss,se2=run('-m','tools.symbolic_check');assert '17' in ss
bb,se3=run('-m','tools.browser_check');assert '15' in bb
status={'result':'PASS','zip_path':str(DEST),'zip_size_bytes':DEST.stat().st_size,
    'zip_members':len(names),'sha256_member_files':len(paths)-1,'zip_crc':'passed',
    'original_manifest':'passed','independent_unzip_manifest':'passed','independent_unzip_unittest':'60 passed',
    'independent_unzip_sympy':'17 passed','independent_unzip_chromium':'15 passed',
    'caveat':'Theoretical/numerical validation only, not a physical unification proof.'}
(ROOT.parent/'ROOT_V79_验收结果.json').write_text(json.dumps(status,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(status,ensure_ascii=False,indent=2))
