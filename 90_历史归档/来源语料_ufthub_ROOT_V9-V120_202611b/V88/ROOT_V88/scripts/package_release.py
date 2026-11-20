from pathlib import Path
import csv,hashlib,zipfile,shutil,json,subprocess,sys,os
ROOT=Path(__file__).resolve().parents[1]
OUT=Path('/mnt/data/ROOT_V88_双量子引力纠缠_牛顿爱因斯坦低能统一_经典媒介证伪科研包.zip')
ARCHIVE=Path('/mnt/data/ROOT_V87_量子力学_牛顿引力_爱因斯坦场方程_统一与验证科研包.zip')
assert ARCHIVE.is_file(),'prior version not found'
shutil.copyfile(ARCHIVE,ROOT/'archive'/'ROOT_V87.zip')
MAN=ROOT/'SHA256_MANIFEST.csv'
files=sorted(f for f in ROOT.rglob('*') if f.is_file() and '__pycache__' not in f.parts and f!=MAN)
with MAN.open('w',newline='',encoding='utf-8-sig') as fp:
 w=csv.writer(fp);w.writerow(['path','size_bytes','sha256'])
 for f in files:
  w.writerow([f.relative_to(ROOT).as_posix(),f.stat().st_size,hashlib.sha256(f.read_bytes()).hexdigest()])
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in sorted(f for f in ROOT.rglob('*') if f.is_file() and '__pycache__' not in f.parts):
  z.write(f,(ROOT.name+'/'+f.relative_to(ROOT).as_posix()))
with zipfile.ZipFile(OUT) as z:
 assert z.testzip() is None
 entries={name for name in z.namelist()}
 assert len(entries)==len(files)+1
 for row in list(csv.DictReader(MAN.open(encoding='utf-8-sig'))):
  data=z.read(ROOT.name+'/'+row['path'])
  assert hashlib.sha256(data).hexdigest()==row['sha256']
extract=Path('/mnt/data/ROOT_V88_verify_extract')
if extract.exists():shutil.rmtree(extract)
extract.mkdir()
with zipfile.ZipFile(OUT) as z:z.extractall(extract)
p=extract/ROOT.name
res=subprocess.run([sys.executable,'run_all.py'],cwd=p,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=60)
if res.returncode:print(res.stdout[-3000:],res.stderr[-3000:]);raise RuntimeError('independent extraction tests failed')
res2=subprocess.run([sys.executable,'web/browser_smoke.py'],cwd=p,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=60)
if res2.returncode:print(res2.stdout[-3000:],res2.stderr[-3000:]);raise RuntimeError('extracted browser tests failed')
a=json.loads((ROOT/'results/numerical_summary.json').read_text());b=json.loads((p/'results/numerical_summary.json').read_text())
assert a==b,'re-generated numeric results differ'
proof=(ROOT/'PROOF_STATUS.md').read_text()
assert '未证明' in proof and '经典' in proof
browser=json.loads((p/'results/browser_checks.json').read_text())
assert browser['count']==browser['passed']==17
counts=json.loads((ROOT/'results/catalog_counts.json').read_text())
rep={
 'release':'ROOT V88','date':'2026-11-18','status':'software math test complete, physics proof incomplete',
 'file_count':len(entries),'manifest_verified_files':len(files),'archive_bytes':OUT.stat().st_size,
 'zip_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),
 'python_unit_tests':41,'symbolic_checks':16,'browser_checks':17,
 'equations':counts['equations'],'methods':counts['methods'],'experimental_protocols':3,
 'independent_unzip_and_run':True,'recomputed_summary_same':True,
 'numerical_delta_rad':a['nonlocal_phase_rad'],
 'numerical_concurrence':a['ideal_concurrence'],
 'numerical_negativity':a['ideal_negativity'],
 'dephasing_threshold_per_s':a['critical_local_dephasing_rate_per_mass_per_s_for_1s'],
 'scientific_caveat':'No experimental GIE, no graviton proof, no G derivation or four-force unification',
 'output_zip':str(OUT),
 }
( ROOT/'results'/'release_verification.json').write_text(json.dumps(rep,ensure_ascii=False,indent=2),encoding='utf8')
# release verification report as outside-zip sidecar, as the archive hash cannot include itself
sidecar=Path('/mnt/data/ROOT_V88_最终验收报告.json');sidecar.write_text(json.dumps(rep,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(rep,ensure_ascii=False,indent=2))
