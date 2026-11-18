"""Assemble and independently verify ROOT V76 ZIP. No upload or publication."""
from __future__ import annotations
import csv,hashlib,json,pathlib,subprocess,sys,tempfile,zipfile,os
from datetime import date
ROOT=pathlib.Path(__file__).resolve().parents[1]
ARCHIVE=ROOT.parent/'ROOT_V76_微观能动张量累加_量子交叉项_引力本源科研包.zip'
EXCLUDE={'SHA256_MANIFEST.csv','results/verification_report.json'}

def files():
    return sorted(p for p in ROOT.rglob('*') if p.is_file() and not (set(p.parts)&{'__pycache__','.pytest_cache'}) and not p.name.endswith('.pyc'))

def rel(p):return str(p.relative_to(ROOT)).replace('\\','/')

def sha(b):return hashlib.sha256(b).hexdigest()

def verify_previous():
    # Repeat tests and independent symbolic+offline browser once before packaging.
    run=lambda argv:subprocess.run(argv,cwd=ROOT,text=True,capture_output=True,timeout=45,check=True)
    t=run([sys.executable,'run_all.py'])
    assert 'Ran 75 tests' in (t.stdout+t.stderr) and 'OK' in (t.stdout+t.stderr)
    s=run([sys.executable,'tools/symbolic_checks.py'])
    assert 'PASS 8' in (s.stdout+s.stderr)
    b=json.loads((ROOT/'results/browser_smoke.json').read_text(encoding='utf-8'))
    assert b['passed']==b['total']==16 and not b['page_errors'] and not b['console_errors']
    return {'unittest_passed':75,'sympy_passed':8,'chromium_passed':16}

def main():
    checks=verify_previous()
    report={'release':'ROOT V76','created':str(date.today()),'model_status':'existing/conditional equations numerically checked; new four-force unification not proven',
    'tests':checks,'catalog':{'micro_phenomena':31,'equations':50,'research_methods':30,'data_scans':4,'figures':4,'book_chapters':18},
    'web_rendering':'Canvas2D (no WebGL claim)','laboratory_data_present':False,'g_predicted_independently':False,
    'archive_zip_complete':True,'manifest_excludes':['SHA256_MANIFEST.csv','results/verification_report.json'],
    'warnings':['field-only spherical monopole is a conditional estimate','closed-system energy accounting mandatory','mathematical tests do not confirm new physics']}
    (ROOT/'results/verification_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    tracked=[p for p in files() if rel(p) not in EXCLUDE]
    with (ROOT/'SHA256_MANIFEST.csv').open('w',encoding='utf-8-sig',newline='') as out:
        writer=csv.writer(out);writer.writerow(['path','sha256','bytes'])
        for p in tracked:
            b=p.read_bytes();writer.writerow([rel(p),sha(b),len(b)])
    sources=files()
    with zipfile.ZipFile(ARCHIVE,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
        for p in sources:z.write(p,arcname='ROOT_V76/'+rel(p))
    with zipfile.ZipFile(ARCHIVE) as z:
        assert z.testzip() is None
        assert len(z.namelist())==len(sources)
        for p in sources: assert sha(z.read('ROOT_V76/'+rel(p)))==sha(p.read_bytes()), rel(p)
    with tempfile.TemporaryDirectory(prefix='v76_independent_') as td:
        with zipfile.ZipFile(ARCHIVE) as z:z.extractall(td)
        E=pathlib.Path(td)/'ROOT_V76'
        with (E/'SHA256_MANIFEST.csv').open(encoding='utf-8-sig',newline='') as f:
            for row in csv.DictReader(f):
                p=E/row['path']; assert p.exists() and sha(p.read_bytes())==row['sha256'],row['path']
        env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
        t=subprocess.run([sys.executable,'run_all.py'],cwd=E,text=True,capture_output=True,env=env,timeout=45,check=True)
        assert 'Ran 75 tests' in (t.stdout+t.stderr)
        s=subprocess.run([sys.executable,'tools/symbolic_checks.py'],cwd=E,text=True,capture_output=True,env=env,timeout=45,check=True)
        assert 'PASS 8' in (s.stdout+s.stderr)
    print(json.dumps({'archive':str(ARCHIVE),'bytes':ARCHIVE.stat().st_size,'file_count':len(sources),'sha256_source_entries':len(tracked),'independent_extract_and_tests':True,**checks},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
