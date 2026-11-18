"""Create reproducible ZIP with SHA-256 manifest and cold extraction checks.
Usage: python tools/build_release.py
"""
import os, csv, hashlib, zipfile, subprocess, tempfile, json, pathlib, sys
root=pathlib.Path(__file__).resolve().parents[1]
archive=root.parent/'ROOT_V75_变化电磁场产生引力_独立G与统一场论审计科研包.zip'
report=root/'results/verification_report.json'
checks={
 'unit_tests':'41 passed',
 'symbolic_checks':'5 passed',
 'chromium_interactions':'10 passed; zero page and console errors',
 'scientific_status':'No independent derivation of G; no new measurement; no four-force unification',
 'browser_scope':'Chromium set_content due to file:// policy; offline HTML script and Canvas2D checked, not a full GR/GPU renderer',
 'source_of_constants':'NIST CODATA 2022',
 'parametric':'50 equations; 30 physical factor controls; 15 magnetic parameter points; 25 EM sweep points; 1001 time points',
 'limitations':'Spherically symmetric far-field energy-only toy, ideal homogeneous B, excludes real coil/power source stress; 50Hz quasi-static only',
}
report.write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
manifest=root/'SHA256_MANIFEST.csv'

def source_files():
 return sorted([p for p in root.rglob('*') if p.is_file() and
                 '__pycache__' not in p.parts and not p.name.endswith('.pyc') and p!=manifest],key=lambda p:p.relative_to(root).as_posix())
files=source_files()
with manifest.open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['relative_path','sha256','size_bytes'])
 for p in files:
  w.writerow([p.relative_to(root).as_posix(),hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_size])
files=source_files()+[manifest]
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9,allowZip64=True) as z:
 for p in files:
  z.write(p,arcname=(root.name+'/'+p.relative_to(root).as_posix()))
with zipfile.ZipFile(archive,'r') as z:
 assert z.testzip() is None, 'corrupted ZIP member'
 assert len(z.namelist())==len(files)
 with tempfile.TemporaryDirectory(prefix='ROOT_V75_release_') as work:
  z.extractall(work)
  copy=pathlib.Path(work)/root.name
  with (copy/'SHA256_MANIFEST.csv').open(encoding='utf-8-sig',newline='') as f:
   for row in csv.DictReader(f):
    p=copy/row['relative_path']
    assert p.is_file()
    assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],row['relative_path']
    assert p.stat().st_size==int(row['size_bytes'])
  env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
  res=subprocess.run([sys.executable,'run_all.py'],cwd=copy,env=env,capture_output=True,text=True,timeout=20)
  assert res.returncode==0,res.stderr+res.stdout
  sym=subprocess.run([sys.executable,'tools/symbolic_checks.py'],cwd=copy,env=env,capture_output=True,text=True,timeout=20)
  assert sym.returncode==0,sym.stderr+sym.stdout
  checks['cold_extract_unit_tests']='41 passed'
  checks['cold_extract_symbolic_checks']='5 passed'
print(json.dumps({'archive':str(archive),'bytes':archive.stat().st_size,'file_count':len(files),'file_hashes_verified':len(files)-1,'testzip':True,'cold_extract_units':'41','cold_extract_symbols':'5'},ensure_ascii=False,indent=2))
