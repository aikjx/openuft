"""Build one verified ZIP containing ROOT V67 and V66 history.
Do not claim this verifies an underlying field theory: it verifies file integrity only.
"""
from pathlib import Path
import hashlib,zipfile,subprocess,tempfile,json,sys,os
r=Path(__file__).resolve().parent
zpath=r.parent/'ROOT_V67_四力统一场论_全维推导审计与数值模拟科研总集.zip'
for p in r.rglob('__pycache__'):
    import shutil
    shutil.rmtree(p)
files=sorted(p for p in r.rglob('*') if p.is_file() and p.name not in {'FILE_SHA256_MANIFEST.txt'} and p.suffix not in ('.pyc',))
manifest=['# SHA-256 for all listed files at the time of packaging.','']
for p in files:
    manifest.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(r).as_posix())
(r/'FILE_SHA256_MANIFEST.txt').write_text('\n'.join(manifest)+'\n',encoding='utf-8')
files=sorted(p for p in r.rglob('*') if p.is_file() and p.suffix !='.pyc')
with zipfile.ZipFile(zpath,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
    for p in files:
        z.write(p,arcname='ROOT_V67/'+p.relative_to(r).as_posix())
with zipfile.ZipFile(zpath) as z:
    bad=z.testzip()
    if bad:raise RuntimeError('Corrupt archive member: '+bad)
    member_count=len(z.namelist())
    with tempfile.TemporaryDirectory() as tmp:
        z.extractall(tmp)
        extracted=Path(tmp)/'ROOT_V67'
        proc=subprocess.run([sys.executable,str(extracted/'VERIFY_PACKAGE.py')],capture_output=True,text=True,timeout=90)
        if proc.returncode:raise RuntimeError('EXTRACTED MANIFEST FAILED:'+proc.stdout+proc.stderr)
        print('extracted-manifest:',proc.stdout.strip())
        test=subprocess.run([sys.executable,str(extracted/'run_all.py')],capture_output=True,text=True,timeout=90)
        if test.returncode:raise RuntimeError('EXTRACTED TEST FAILED:'+test.stdout+test.stderr)
        print('extracted-tests:',test.stdout[:210].strip())
report={'zip_name':zpath.name,'bytes':zpath.stat().st_size,'sha256':hashlib.sha256(zpath.read_bytes()).hexdigest(),
 'members':member_count,'manifest_verified_after_extract':True,'automated_tests_pass_after_extract':True,
 'mathematical_claim':'A verified software package, not a physics proof of unified interactions.'}
(r.parent/'ROOT_V67_打包验收报告.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
