"""Audit a release ZIP: CRC, SHA-256, clean extraction and unit tests.
Needs no third-party dependencies. Use after build_manifest.py.
"""
from __future__ import annotations
import csv,hashlib,io,json,subprocess,sys,tempfile,zipfile
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
ZIP=BASE.parent/'ROOT_V77_G与光速c_全维公式推导_精算验证_统一场论关系研究包.zip'
root='ROOT_V77/'
files=sorted(p for p in BASE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc')
with zipfile.ZipFile(ZIP,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9,allowZip64=True) as z:
    for p in files:
        z.write(p,root+p.relative_to(BASE).as_posix())
with zipfile.ZipFile(ZIP) as z:
    assert z.testzip() is None,'CRC check failed'
    names=set(z.namelist())
    expected={root+p.relative_to(BASE).as_posix() for p in files}
    assert names==expected, 'ZIP unexpected or missing members'
    raw=z.read(root+'SHA256_MANIFEST.csv').decode('utf-8-sig')
    rows=list(csv.DictReader(io.StringIO(raw)))
    for row in rows:
        blob=z.read(root+row['relative_path'])
        assert len(blob)==int(row['size_bytes']),'size mismatch: '+row['relative_path']
        assert hashlib.sha256(blob).hexdigest()==row['sha256'],'hash mismatch: '+row['relative_path']
    with tempfile.TemporaryDirectory(prefix='root_v77_release_') as td:
        target=Path(td)
        z.extractall(target)
        new=target/'ROOT_V77'
        # Clean-room re-run of all standard-library tests.
        cmd=[sys.executable,'-m','unittest','discover','-s','tests','-q']
        completed=subprocess.run(cmd,cwd=new,capture_output=True,text=True,timeout=60)
        assert completed.returncode==0, completed.stdout+'\n'+completed.stderr
        assert 'Ran 58 tests' in completed.stderr, completed.stderr
        # Compare result identities without requiring graphing libs.
        evalcmd=[sys.executable,'-m','src.cli','summary']
        result=subprocess.run(evalcmd,cwd=new,capture_output=True,text=True,timeout=60)
        assert result.returncode==0,result.stderr
        parsed=json.loads(result.stdout)
        assert abs(parsed['quantities']['Z_SI']-0.010004524012147)<1e-15
    report={'archive':ZIP.name,'size_bytes':ZIP.stat().st_size,
            'zip_crc':'PASSED','zip_member_count':len(names),'sha256_entries':len(rows),
            'sha256_checks':'PASSED','clean_extraction':'PASSED',
            'extracted_unit_tests':'58 PASSED',
            'extracted_cli_numeric':'PASSED',
            'scientific_scope':'Software, calculations, conditional theory checks; not a new physical measurement or a prediction of G from c',
            'sha256_zip':hashlib.sha256(ZIP.read_bytes()).hexdigest()}
    out=BASE.parent/'ROOT_V77_验收报告.json'
    out.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(report,indent=2,ensure_ascii=False))
