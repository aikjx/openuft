"""ROOT V83: deterministic inventory, zip audit, extracted copy self-test."""
from pathlib import Path
import csv,hashlib,json,subprocess,sys,zipfile,tempfile
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT.parent/'ROOT_V83_双传感器引力调制_实验语言_全链路验证科研包.zip'
EXCLUDE={'SHA256_MANIFEST.csv','first_run.log','second_run.log'}

def included_files():
    return sorted([p for p in ROOT.rglob('*') if p.is_file() and not any(x=='__pycache__' for x in p.parts) and p.name not in EXCLUDE and not p.name.endswith('.pyc')])

def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def run(args,cwd):
    p=subprocess.run(args,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=90)
    if p.returncode: raise RuntimeError('FAIL: '+str(args)+'\n'+p.stdout[-500:]+'\n'+p.stderr[-1000:])
    return p.stdout,p.stderr

def main():
    first,stderr=run([sys.executable,'run_all.py'],ROOT)
    (ROOT/'results'/'test_run.log').write_text(first+'\n'+stderr,encoding='utf-8')
    pstdout,_=run([sys.executable,'-m','tools.validate_protocols'],ROOT)
    (ROOT/'results'/'protocol_validation.log').write_text(pstdout,encoding='utf-8')
    # Browser actual smoke run separately; run again here for inclusion.
    bstdout,_=run([sys.executable,'tools/browser_smoke.py'],ROOT)
    browser=json.loads((ROOT/'results'/'browser_report.json').read_text())
    # Build release record before manifest so both are included.
    numeric=json.loads((ROOT/'results'/'numeric_summary.json').read_text())
    record={'version':'ROOT V83','timestamp_context':'2026-11-18','python_unittest_tests':51,
            'python_tests':'PASS','protocol_files_validated':3,
            'protocol_validation':'PASS','chromium_interaction_checks':browser['count'],
            'chromium_status':browser['status'], 'browser_test_mode':'set_content HTML in Chromium, file:// denied by this environment',
            'physics_data_provenance':'SYNTHETIC_NOT_OBSERVED','hardware_tests_performed':False,
            'independent_G_prediction':False,'four_force_unification_proved':False,
            'new_gravity_observed':False,'zip_integrity':None,'extracted_unittest':None}
    (ROOT/'results'/'verification_report.json').write_text(json.dumps(record,indent=2,ensure_ascii=False),encoding='utf-8')
    files=included_files()
    manifest=ROOT/'SHA256_MANIFEST.csv'
    with manifest.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(['relative_path','sha256','size_bytes'])
        for p in files: w.writerow([p.relative_to(ROOT).as_posix(),h(p),p.stat().st_size])
    files=included_files()+[manifest]
    with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(files): z.write(p,arcname='ROOT_V83/'+p.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(OUT) as z:
        bad=z.testzip();assert bad is None, bad
        with tempfile.TemporaryDirectory(prefix='rootv83_verify_') as temp:
            z.extractall(temp)
            e=Path(temp)/'ROOT_V83'
            with (e/'SHA256_MANIFEST.csv').open('r',encoding='utf-8-sig') as f:
                items=list(csv.DictReader(f))
            for item in items:
                p=e/item['relative_path']
                assert p.exists(),item['relative_path']
                assert h(p)==item['sha256'],item['relative_path']
            rstdout,rstderr=run([sys.executable,'run_all.py'],e)
            protocol_stdout,_=run([sys.executable,'-m','tools.validate_protocols'],e)
            # Browser test also re-evaluates identical extracted HTML; replay restrictions apply.
            browser_stdout,_=run([sys.executable,'tools/browser_smoke.py'],e)
            assert 'tests_run' in rstdout and '51' in rstdout
            assert '10 checks PASS' in browser_stdout
    report={'status':'PASS','zip':OUT.name,'zip_bytes':OUT.stat().st_size,
            'sha256_zip':h(OUT),'files_in_zip':len(files),'manifest_files_verified':len(items),
            'unit_tests':51,'protocols':3,'browser_checks':browser['count'],
            'full_extracted_replay':True,
            'scientific_status':'Known gravitational field modulation model; no new force, no variable G claim',
            'data_provenance':'SYNTHETIC_NOT_OBSERVED'}
    # Sidecar outside zip reports verification after ZIP creation.
    (ROOT.parent/'ROOT_V83_最终验收报告.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(report,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
