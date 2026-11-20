"""Package ROOT V89, verify SHA-256/ZIP, unzip to fresh dir, rerun math/browser tests."""
from pathlib import Path
import json,hashlib,csv,shutil,subprocess,sys,zipfile,datetime
ROOT=Path(__file__).resolve().parents[1]
DEST=Path('/mnt/data')
ZIP=DEST/'ROOT_V89_量子引力_牛顿后牛顿EFT_经典媒介证伪与高精度计算科研包.zip'
OLD=DEST/'ROOT_V88_双量子引力纠缠_牛顿爱因斯坦低能统一_经典媒介证伪科研包.zip'
ARCH=ROOT/'archive/ROOT_V88.zip'
ARCH.parent.mkdir(parents=True,exist_ok=True)
if not OLD.is_file():raise SystemExit('V88 historical archive missing')
shutil.copy2(OLD,ARCH)

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for part in iter(lambda:f.read(2<<20),b''):h.update(part)
    return h.hexdigest()

exclude=lambda p: ('__pycache__' in p.parts or '.pytest_cache' in p.parts or p.suffix in ('.pyc',) or p.name=='SHA256_MANIFEST.csv')
all_files=lambda:sorted(p for p in ROOT.rglob('*') if p.is_file() and not exclude(p))
# Tests on source and browser first
p=subprocess.run([sys.executable,'run_all.py'],cwd=ROOT,check=True,text=True,capture_output=True)
print(p.stdout[-1400:])
q=subprocess.run([sys.executable,'web/browser_smoke.py'],cwd=ROOT,check=True,text=True,capture_output=True)
print(q.stdout)
unit=json.loads((ROOT/'results/test_report.json').read_text())
browser=json.loads((ROOT/'results/browser_checks.json').read_text())
counts=json.loads((ROOT/'results/catalog_counts.json').read_text())
protocols=list((ROOT/'protocols').glob('*.json'))
for path in protocols:
    obj=json.loads(path.read_text(encoding='utf8'))
    assert obj['simulation_only'] and not obj['hardware_connected']
# record test status before hashing; archive check will follow
pre={'version':'ROOT_V89','date':'2026-11-18','validation_level':'mathematical/software, not real experiment',
    'unit_tests_passed':unit['test_count'],'symbolic_passed':unit['symbolic_passed'],
    'chromium_passed':browser['passed'],'chromium_total':browser['count'],
    'equation_catalog':counts['equations'],'method_matrix':counts['methods'],
    'protocol_count':len(protocols),'csv_synthetic':len(list((ROOT/'data').glob('*SYNTHETIC.csv'))),
    'quantum_gravity_discovery':False,'G_predicted_without_external_parameter':False,
    'four_forces_unified':False,'requires_independent_physical_replication':True}
(ROOT/'results/pre_release_report.json').write_text(json.dumps(pre,ensure_ascii=False,indent=2),encoding='utf8')
entries=[(p.relative_to(ROOT).as_posix(),p.stat().st_size,sha(p)) for p in all_files()]
with (ROOT/'SHA256_MANIFEST.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['relative_path','size_bytes','sha256']);w.writerows(entries)
files=all_files()+[ROOT/'SHA256_MANIFEST.csv']
with zipfile.ZipFile(ZIP,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
    for f in sorted(files): z.write(f,arcname='ROOT_V89/'+f.relative_to(ROOT).as_posix())

assert zipfile.ZipFile(ZIP).testzip() is None
verify=DEST/'ROOT_V89_verify_extract'
if verify.exists():shutil.rmtree(verify)
verify.mkdir()
with zipfile.ZipFile(ZIP) as z:
    bad=[name for name in z.namelist() if name.startswith('/') or '..' in Path(name).parts]
    assert not bad,bad
    z.extractall(verify)
extracted=verify/'ROOT_V89'
with (extracted/'SHA256_MANIFEST.csv').open(encoding='utf-8-sig',newline='') as f:
    rd=csv.DictReader(f)
    each=list(rd)
    for row in each:
        a=extracted/row['relative_path']
        assert a.is_file() and sha(a)==row['sha256'] and a.stat().st_size==int(row['size_bytes']),a
res=subprocess.run([sys.executable,'run_all.py'],cwd=extracted,check=True,text=True,capture_output=True)
resb=subprocess.run([sys.executable,'web/browser_smoke.py'],cwd=extracted,check=True,text=True,capture_output=True)
a=json.loads((extracted/'results/numerical_summary.json').read_text())
b=json.loads((ROOT/'results/numerical_summary.json').read_text())
assert a['phase_terms']==b['phase_terms']
assert a['decimal_90_digit_filter']==b['decimal_90_digit_filter']
assert json.loads((extracted/'results/test_report.json').read_text())['test_count']==unit['test_count']
assert json.loads((extracted/'results/browser_checks.json').read_text())['passed']==browser['passed']
final={**pre,'zip_filename':ZIP.name,'zip_bytes':ZIP.stat().st_size,'zip_sha256':sha(ZIP),
    'zip_entry_count':len(files),'source_files_sha256_checked':len(each),
    'zip_testzip':'PASS','independent_unpack_sha256':'PASS',
    'independent_replay_unit':'PASS','independent_replay_chromium':'PASS',
    'numeric_reports_identical':'PASS','historical_V88_archive':'INCLUDED',
    'scientific_claim':'validated simulation, no independent observation'}
(DEST/'ROOT_V89_最终验收报告.json').write_text(json.dumps(final,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(final,ensure_ascii=False,indent=2))
