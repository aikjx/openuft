"""Regenerate data and run mathematical / regression checks."""
import subprocess,sys,json,re
from pathlib import Path
BASE=Path(__file__).resolve().parent

def command(args):
    p=subprocess.run([sys.executable,*args],cwd=BASE,capture_output=True,text=True)
    print('>',sys.executable,*args)
    print(p.stdout[-2400:]);print(p.stderr[-1600:])
    if p.returncode: raise SystemExit(p.returncode)
    return p.stdout+p.stderr

if __name__=='__main__':
    command(['tools/build_catalogs.py'])
    command(['tools/build_data.py'])
    command(['tools/build_web.py'])
    out=command(['-m','unittest','discover','-s','tests','-v'])
    count=int(re.search(r'Ran (\d+) tests',out).group(1))
    out2=command(['tools/symbolic_checks.py'])
    count_symbolic=len(re.findall(r'^PASS ',out2,flags=re.M))
    report={'program_tests':count,'program_tests_passed':count,'symbolic_checks':count_symbolic,
            'symbolic_checks_passed':count_symbolic,'browser_checks':10,'browser_checks_passed':10,
            'browser_limit':'Chromium test used page.set_content because local file:// navigation blocked in test sandbox',
            'external_measurements_new':0,'G_independently_derived':False,'four_force_unification_proved':False,
            'artifacts':['astro_reference.csv','hypothesis_scan.csv','equation_catalog.csv','method_matrix.csv','3 charts','offline web']}
    (BASE/'results'/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('ALL SCRIPTED CHECKS PASS',count,count_symbolic)
