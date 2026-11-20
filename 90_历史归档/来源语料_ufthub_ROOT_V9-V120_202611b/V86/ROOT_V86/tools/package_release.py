#!/usr/bin/env python3
"""Release build with file SHA256, zip integrity, fresh-dir reproduce of ALL mandatory tests."""
from pathlib import Path
import os,hashlib,csv,zipfile,json,tempfile,subprocess,sys
root=Path(__file__).resolve().parents[1]
out=root.parent/'ROOT_V86_G来源_星球差异_四力统一_全维漏洞修复_统计证伪科研总集.zip'

def skip(path):
    return any(part in ('__pycache__','.pytest_cache','.git') for part in path.parts) or path.suffix in ('.pyc','.pyo')

# Stable source-stage verification metadata, excluding a self-referential hash record.
report=json.loads((root/'results/run_report.json').read_text(encoding='utf8'))
unit=report['pytest_passed'];symbol=report['symbolic_passed'];browser=report['browser']
assert unit==91 and symbol==19 and browser==20, (unit,symbol,browser)
meta={'version':'ROOT V86','released_date':'2026-11-18','engineering_status':'TESTED on supplied Linux Python/Chromium environment',
    'science_status':'NO independent derivation of G, NO evidence of planet-specific fundamental G, NO four-force unification',
    'unit_tests_passed':unit,'sympy_checks_passed':symbol,'chromium_checks_passed':browser,
    'equations':report['catalog']['equations'],'methods':report['catalog']['methods'],
    'experimental_protocols':4,'synthetic_rng_seed':20261118,
    'confirmed_real_world_new_force':False,'experimental_hardware_attached':False,
    'historical_archive_included':'ROOT_V85_G来源_星球差异_四力统一_双不变量_求导证明精算科研包.zip'}
(root/'results/verification_report.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8')

files=sorted((p for p in root.rglob('*') if p.is_file() and not skip(p) and p.name!='SHA256_MANIFEST.csv'),key=lambda p:p.relative_to(root).as_posix())
with (root/'SHA256_MANIFEST.csv').open('w',encoding='utf-8-sig',newline='') as fd:
    writer=csv.writer(fd);writer.writerow(['relative_path','size_bytes','sha256'])
    for p in files:
        writer.writerow([p.relative_to(root).as_posix(),p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest()])
files.append(root/'SHA256_MANIFEST.csv')
if out.exists():out.unlink()
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8,allowZip64=True) as z:
    for p in files:
        z.write(p,arcname='ROOT_V86/'+p.relative_to(root).as_posix())
with zipfile.ZipFile(out) as z:
    bad=z.testzip()
    if bad:raise AssertionError('bad zip member '+bad)
    for p in files:
        member='ROOT_V86/'+p.relative_to(root).as_posix()
        assert hashlib.sha256(z.read(member)).digest()==hashlib.sha256(p.read_bytes()).digest(), member
    with tempfile.TemporaryDirectory(prefix='root_v86_recheck_') as temp:
        z.extractall(temp)
        rp=Path(temp)/'ROOT_V86'
        # Snapshot hash verification BEFORE regenerated files are overwritten by independent test run.
        with (rp/'SHA256_MANIFEST.csv').open(encoding='utf-8-sig',newline='') as fd:
            rec=list(csv.DictReader(fd))
        for row in rec:
            p=rp/row['relative_path']
            assert p.is_file() and p.stat().st_size==int(row['size_bytes'])
            assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'], row['relative_path']
        pre=json.loads((rp/'results/numerical_summary.json').read_text(encoding='utf8'))
        result=subprocess.run([sys.executable,'run_all.py','--skip-browser'],cwd=rp,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,encoding='utf8',timeout=90)
        if result.returncode:raise RuntimeError('Independent unzip run failed: '+result.stdout[-2000:])
        post=json.loads((rp/'results/numerical_summary.json').read_text(encoding='utf8'))
        assert pre==post, 'synthetic numeric result changed on reproducible rerun'
        # Also verify core test count from independent root.
        r2=json.loads((rp/'results/run_report.json').read_text(encoding='utf8'))
        assert r2['pytest_passed']==unit and r2['symbolic_passed']==symbol
ind={'archive':out.name,'zip_size_bytes':out.stat().st_size,
     'zip_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
     'files_in_zip':len(files),'manifest_entries':len(rec),
     'zip_integrity':True,'independent_extract_manifest_verified':True,
     'independent_run_all_skip_browser':True,'identical_synthetic_numeric_summary':True,
     'unit_tests':unit,'symbolic_checks':symbol,'browser_checks':browser,
     'science_status':'New fifth force and changed G NOT established by these software checks'}
(root.parent/'ROOT_V86_最终验收报告.json').write_text(json.dumps(ind,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(ind,ensure_ascii=False,indent=2))
