"""Create reproducible ROOT_V70 release ZIP and perform real extract/hash/test checks.
Prerequisite: python run_all.py; python experiments/browser_smoke.py.
"""
from __future__ import annotations
import hashlib,json,os,subprocess,sys,tempfile,zipfile
from pathlib import Path
root=Path(__file__).resolve().parent
zip_path=root.parent/'ROOT_V70_多星体元素空间运动微观引力_统一场论新突破点科研总集.zip'
for p in root.rglob('__pycache__'):
    import shutil;shutil.rmtree(p)
report=json.loads((root/'results/verification.json').read_text(encoding='utf-8'))
browser=json.loads((root/'results/browser_verification.json').read_text(encoding='utf-8'))
if not report['success'] or not browser['success']: raise RuntimeError('tests must pass before release')
files=sorted([p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name not in ('SHA256SUMS.txt','RELEASE_CHECK.json')])
manifest='\n'.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(root).as_posix() for p in files)+'\n'
(root/'SHA256SUMS.txt').write_text(manifest,encoding='utf-8')
metadata={
 'version':'ROOT V70','date':'2026-11-17',
 'scientific_status':'NO proof of four-force unification / independent G / empirical fifth force',
 'tests':report['tail'], 'browser_interaction_checks':len(browser['checks']),
 'browser_success':browser['success'], 'browser_method':browser['url_scheme'],
 'sha256_source_files':len(files),
 'includes_previous_archive':(root/'archive/ROOT_V69_历史版.zip').is_file(),
 'planet_models':9,'gravity_scenarios':54,'synthetic_design_rows':162,
 'important':'All toy material and source scalar charges are arbitrary SYNTHETIC inputs.'
}
(root/'RELEASE_CHECK.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding='utf-8')
allfiles=sorted([p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts])
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7,allowZip64=True) as z:
    for file in allfiles:z.write(file,arcname='ROOT_V70/'+file.relative_to(root).as_posix())
with zipfile.ZipFile(zip_path) as z:
    if z.testzip() is not None:raise RuntimeError('CRC check failed')
    zip_count=len(z.namelist())
    with tempfile.TemporaryDirectory(prefix='ROOT_V70_extract_') as tmp:
        z.extractall(tmp)
        ext=Path(tmp)/'ROOT_V70'
        sha=subprocess.run([sys.executable,'verify_package.py'],cwd=ext,capture_output=True,text=True)
        if sha.returncode:raise RuntimeError('manifest check '+sha.stdout+sha.stderr)
        unit=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=ext,capture_output=True,text=True)
        if unit.returncode:raise RuntimeError('extraction tests '+unit.stderr[-1000:])
        extraction_tail=unit.stderr.splitlines()[-4:]
final={**metadata, 'zip_path':str(zip_path),'zip_size_bytes':zip_path.stat().st_size,
       'zip_entries':zip_count,'zip_crc_test':True,'extracted_sha256_check':sha.stdout.strip(),
       'extracted_tests_tail':extraction_tail,'extracted_tests_success':True,
       'zip_sha256':hashlib.sha256(zip_path.read_bytes()).hexdigest()}
(root.parent/'ROOT_V70_验收结果.json').write_text(json.dumps(final,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(final,ensure_ascii=False,indent=2))
