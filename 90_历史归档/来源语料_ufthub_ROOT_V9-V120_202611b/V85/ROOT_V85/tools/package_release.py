"""Atomic research release with independent extraction and re-run verification."""
from pathlib import Path
import zipfile,hashlib,csv,json,subprocess,tempfile,sys,os,shutil
root=Path(__file__).resolve().parents[1]
manifest=root/'SHA256_MANIFEST.csv'
archives=sorted((root/'history').glob('ROOT_V*.zip'))
num=json.loads((root/'results'/'numerical_summary.json').read_text())
sym=json.loads((root/'results'/'symbolic_report.json').read_text())
browser=json.loads((root/'results'/'browser_report.json').read_text())
quad=json.loads((root/'results'/'independent_volume_integral.json').read_text())
catalog=json.loads((root/'results'/'catalog_summary.json').read_text())
run=json.loads((root/'results'/'run_report.json').read_text())
assert all(x['exit_code']==0 for x in run['tasks'])
assert sym['passed']==sym['total']
assert browser['passed']==browser['total']
assert quad['relative_error']<1e-11
report={'version':'ROOT V85','date':'2026-11-18','engineering_status':'TESTED',
        'science_status':'Mathematical derivations and synthetic hypothesis tests; NO independent G prediction; NO observed fifth force; NO four-force unification',
        'unit_tests':54,'symbolic_checks':sym['passed'],'browser_checks':browser['passed'],
        'independent_quadrature_relative_error':quad['relative_error'],
        'equations':catalog['equations'],'methods':catalog['methods'],
        'previous_milestone_zips_included':[p.name for p in archives],
        'repro_command':'python run_all.py',
        'website':'web/index.html',
        'data_warning':'Data marked SYNTHETIC refer to hypothetical calculations, never observed new physics'}
(root/'results'/'verification_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
files=sorted([p for p in root.rglob('*') if p.is_file() and p != manifest and '__pycache__' not in p.parts and not p.name.endswith('.pyc')],key=lambda p:str(p.relative_to(root)))
with manifest.open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['relative_path','size_bytes','sha256'])
 for p in files:
  w.writerow([str(p.relative_to(root)),p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest()])
files.append(manifest)
zip_path=root.parent/'ROOT_V85_G来源_星球差异_四力统一_双不变量_求导证明精算科研包.zip'
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for p in files:z.write(p,arcname='ROOT_V85/'+str(p.relative_to(root)))
with zipfile.ZipFile(zip_path) as z:
 corruption=z.testzip()
 assert corruption is None,corruption
 assert len(z.namelist())==len(files)
 assert all(n.startswith('ROOT_V85/') for n in z.namelist())
 with tempfile.TemporaryDirectory(prefix='v85_verified_',dir=str(root.parent)) as t:
  z.extractall(t)
  ext=Path(t)/'ROOT_V85'
  with (ext/'SHA256_MANIFEST.csv').open('r',encoding='utf-8-sig',newline='') as f:
   entries=list(csv.DictReader(f))
  for entry in entries:
   p=ext/entry['relative_path']
   assert p.stat().st_size==int(entry['size_bytes'])
   assert hashlib.sha256(p.read_bytes()).hexdigest()==entry['sha256'],p
  proc=subprocess.run([sys.executable,'run_all.py'],cwd=ext,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=90)
  assert proc.returncode==0,proc.stdout+'\n'+proc.stderr
  rerun=json.loads((ext/'results'/'numerical_summary.json').read_text())
  assert abs(rerun['scalar_hypothesis_example']['Q_at_0p35m']-num['scalar_hypothesis_example']['Q_at_0p35m'])<1e-14
  assert (ext/'web'/'index.html').exists()
  recheck=proc.stdout.strip().splitlines()
final={**report,'archive_path':str(zip_path),'archive_size_bytes':zip_path.stat().st_size,
 'archive_sha256':hashlib.sha256(zip_path.read_bytes()).hexdigest(),
 'file_count':len(files),'manifest_verified_entries':len(entries),
 'zip_integrity':'PASS','independent_extract_manifest':'PASS','independent_extract_run_all':'PASS','independent_rerun_last_lines':recheck[-4:]}
(root.parent/'ROOT_V85_最终验收报告.json').write_text(json.dumps(final,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(final,ensure_ascii=False,indent=2))
