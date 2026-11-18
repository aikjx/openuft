"""Create distributable ZIP with complete CRC + extraction + no-dependency test verification."""
from pathlib import Path
import zipfile,subprocess,hashlib,json,os,tempfile,shutil,sys
P=Path(__file__).resolve().parent
ZIP=P.parent/'ROOT_V69_地球引力_星体密度_元素组成_空间运动_统一场论审计科研总集.zip'
report={'name':ZIP.name,'science':'OPEN: not four-force unified; no independent prediction of G',
        'tests_v69':54,'tests_v68_regression':75,'browser_smoke_checks':14,'types_of_bodies':10,
        'reviewed_scenarios':30,'earth_model':'WGS84-like ellipsoid, J2 first zonal, rotation; not EGM2008',
        'magnetic_field':'No IGRF coefficient implementation; B-energy stress only',
        'rendering':'Canvas2D 3D perspective, not WebGL','zip_full_extraction_test':None}
(P/'results/release_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
with zipfile.ZipFile(ZIP,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8,allowZip64=True) as z:
    for path in sorted(P.rglob('*')):
        if not path.is_file():continue
        rel=path.relative_to(P)
        if any(part=='__pycache__' for part in rel.parts) or path.suffix=='.pyc':continue
        z.write(path,arcname='ROOT_V69/'+rel.as_posix())
with zipfile.ZipFile(ZIP) as z:
    bad=z.testzip()
    if bad:raise RuntimeError('Corrupt member '+bad)
    names=z.namelist();report['zip_members']=len(names);report['zip_size_bytes']=ZIP.stat().st_size
    with tempfile.TemporaryDirectory(prefix='rootv69_extracted_') as tmp:
        z.extractall(tmp)
        root=Path(tmp)/'ROOT_V69'
        complete=subprocess.run([sys.executable,str(root/'verify_package.py')],capture_output=True,text=True,timeout=40)
        assert complete.returncode==0,complete.stdout+complete.stderr
        tst=subprocess.run([sys.executable,str(root/'run_all.py')],capture_output=True,text=True,timeout=60)
        assert tst.returncode==0,tst.stdout+tst.stderr
        recheck=subprocess.run([sys.executable,str(root/'verify_package.py')],capture_output=True,text=True,timeout=40)
        assert recheck.returncode==0,recheck.stdout+recheck.stderr
        verify=json.loads(tst.stdout)
        report['extracted_run']={'status':verify['status'],'tests_run':verify['tests_run'],'passed':verify['passed']}
        report['zip_full_extraction_test']='PASS'
report['zip_sha256']=hashlib.sha256(ZIP.read_bytes()).hexdigest()
print(json.dumps(report,ensure_ascii=False,indent=2))
(P/'results/FINAL_ZIP_RELEASE_VERIFICATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
# The final outside-the-archive report captures post-release extraction tests, archive includes prerelease release_validation file.
