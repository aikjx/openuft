"""Run V66 suite, optional original V65 and V64 suite from archival ZIP.

Required: Python 3.10+, stdlib. Optional: scipy/matplotlib/playwright.
No claim of scientific experiment from software pass counts.
"""
from pathlib import Path
import subprocess,sys,tempfile,zipfile,json,datetime
ROOT=Path(__file__).resolve().parent

def test_suite(cwd,tag):
    res=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=cwd,
                       stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
    (ROOT/'results'/f'test_{tag}.txt').write_text(res.stdout,encoding='utf-8')
    import re
    m=re.search(r'Ran\s+(\d+)\s+tests?',res.stdout)
    count=int(m.group(1)) if m else 0
    print(tag, 'PASS' if res.returncode==0 else 'FAIL',count)
    if res.returncode!=0: print(res.stdout[-2500:])
    return res.returncode,count

def main():
    (ROOT/'results').mkdir(exist_ok=True)
    code,n=test_suite(ROOT,'v66')
    total=n
    status={'v66':{'exit_code':code,'number_of_tests':n}}
    archive=ROOT/'archive'/'ROOT_V65_研究基线.zip'
    if archive.exists():
        with tempfile.TemporaryDirectory(prefix='root_v66_baseline_') as tmp:
            with zipfile.ZipFile(archive) as z:
                bad=z.testzip()
                if bad:raise RuntimeError(f'old baseline corrupted: {bad}')
                z.extractall(tmp)
            old=Path(tmp)/'ROOT_V65'
            if old.exists():
                for tag,folder in [('v65',old),('v64',old/'legacy_v64')]:
                    c,k=test_suite(folder,tag)
                    status[tag]={'exit_code':c,'number_of_tests':k}
                    total+=k
                    if c!=0: code=1
            else:
                status['v65']={'error':'missing ROOT_V65/ prefix in archive'}
                code=1
    else:status['v65']={'not_run':'archive not present'}
    status['total_tests_attempted']=total
    status['all_success']=code==0
    status['scientific_warning']='Software regressions are NOT experimental confirmation or GUT proof'
    status['date_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    (ROOT/'results'/'verification_report.json').write_text(json.dumps(status,ensure_ascii=False,indent=2),encoding='utf-8')
    print('TEST TOTAL',total,'PASS' if code==0 else 'FAIL')
    raise SystemExit(code)
if __name__=='__main__':main()
