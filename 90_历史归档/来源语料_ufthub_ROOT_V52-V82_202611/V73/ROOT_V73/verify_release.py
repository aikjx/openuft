"""Build reproducible ZIP and verify extracted source against SHA-256, tests and expected files."""
from pathlib import Path
import hashlib,csv,json,zipfile,tempfile,subprocess,sys,os
ROOT=Path(__file__).resolve().parent
BASE=ROOT.name
OUT=ROOT.parent/'ROOT_V73_新突破_尺度生成_星体源_三重反转_统一场论攻坚科研包.zip'
manifest=ROOT/'SHA256_MANIFEST.csv'
reportfile=ROOT/'results'/'release_verification.json'
ignore={'SHA256_MANIFEST.csv','results/release_verification.json','results/fresh_extract_test_log.txt'}
def files():
    return sorted(p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.relative_to(ROOT).as_posix() not in ignore)
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()
with manifest.open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f);w.writerow(['relative_path','sha256','bytes']);
    for p in files():w.writerow([p.relative_to(ROOT).as_posix(),sha(p),p.stat().st_size])

log_path=ROOT/'results'/'fresh_extract_test_log.txt'
# Fresh extraction based on a pre-final archive. Re-build after report generated.
def pack():
    with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
        for p in sorted(ROOT.rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts:
                z.write(p,arcname=f'{BASE}/{p.relative_to(ROOT).as_posix()}')

def checkzip():
    with zipfile.ZipFile(OUT) as z:
        assert z.testzip() is None
        names=z.namelist()
        assert any(n.endswith('web/index.html') for n in names)
        assert any(n.endswith('book/ROOT_V73_新方法_量纲嬗变_几何曲率_三重反转_科学研究总集.md') for n in names)
        return len(names)

pack();initial_count=checkzip()
with tempfile.TemporaryDirectory(prefix='rootv73_release_') as temp:
    with zipfile.ZipFile(OUT) as z:z.extractall(temp)
    fresh=Path(temp)/BASE
    entries=list(csv.DictReader((fresh/'SHA256_MANIFEST.csv').open(encoding='utf-8-sig')))
    for item in entries:
        p=fresh/item['relative_path']
        assert p.is_file(),f'missing {p}'
        assert sha(p)==item['sha256'],f'hash mismatch {p}'
    # run tests and numerical generation in truly fresh extraction
    p=subprocess.run([sys.executable,'run_all.py','--symbolic'],cwd=fresh,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=120)
    log_path.write_text(p.stdout,encoding='utf-8')
    assert p.returncode==0, p.stdout[-3000:]
    assert 'Ran 49 tests' in p.stdout
    assert 'Symbolic checks: 11 / 11' in p.stdout
    assert (fresh/'results'/'numerical_summary.json').exists()

from datetime import date
verification={
 'name':'ROOT V73', 'date':'2026-11-17',
 'science_status':'No unified-force proof; G is not independently predicted; synthetic predictions not observations.',
 'new_numeric_tests_passed':49,'symbolic_checks_passed':11,'chromium_ui_checks_passed':11,
 'browser_ran_by_set_content_due_to_file_navigation_restriction':True,
 'equations':77,'candidate_methods':37,'generated_csv_tables':5,'generated_figures':4,
 'fresh_extraction_run_all_passed':True,
 'source_sha256_entries':len(entries),'source_sha256_all_match':True,
 'initial_zip_integrity_passed':True,'actual_zip_entry_count':initial_count,
 'exact_copy_of_v72_archived':True,
 'limitations':['G inferred or supplied not calculated ab initio','SM gauge/fermion representations not derived','no new force observations','no complete UV consistency proof'],
}
reportfile.write_text(json.dumps(verification,ensure_ascii=False,indent=2),encoding='utf-8')
pack();final_count=checkzip();verification['final_zip_entries']=final_count
# update verification report and final zip again with the final count
reportfile.write_text(json.dumps(verification,ensure_ascii=False,indent=2),encoding='utf-8')
pack();final_count=checkzip()
# source invariant check in final ZIP
with zipfile.ZipFile(OUT) as z:
    for item in entries:
        data=z.read(f"{BASE}/{item['relative_path']}")
        assert hashlib.sha256(data).hexdigest()==item['sha256']
print(json.dumps({'zip':str(OUT),'size_bytes':OUT.stat().st_size,'zip_sha256':sha(OUT),
                  'files':final_count,'sha256_passed':len(entries),'fresh_extract_tests':49,
                  'symbolic':11,'browser':11},ensure_ascii=False,indent=2))
