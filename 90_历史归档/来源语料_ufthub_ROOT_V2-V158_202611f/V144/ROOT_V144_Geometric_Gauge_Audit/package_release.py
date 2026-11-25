#!/usr/bin/env python3
"""Build reproducible V144 ZIP, verify SHA-256 and test extracted copy."""
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent
OUTPUT=ROOT.parent/'ROOT_V144_Geometric_Gauge_Audit_Complete.zip'


def files_to_pack():
    return [f for f in sorted(ROOT.rglob('*')) if f.is_file() and
            '__pycache__' not in f.parts and f.suffix!='.pyc' and
            '.pytest_cache' not in f.parts]


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as fp:
        for block in iter(lambda:fp.read(1<<20),b''):
            h.update(block)
    return h.hexdigest()


def main():
    print('[1/5] regenerate results and tests')
    subprocess.run([sys.executable,str(ROOT/'run_all.py')],check=True,cwd=ROOT)
    manifest=ROOT/'manifest.sha256'
    content=''.join(f'{digest(f)}  {f.relative_to(ROOT).as_posix()}\n' for f in files_to_pack() if f!=manifest)
    manifest.write_text(content,encoding='utf-8')
    archive_files=files_to_pack()
    print('[2/5] create ZIP (DEFLATE 9)')
    with zipfile.ZipFile(OUTPUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for f in archive_files:
            z.write(f,arcname=f'{ROOT.name}/{f.relative_to(ROOT).as_posix()}')
    with zipfile.ZipFile(OUTPUT) as z:
        print('[3/5] ZIP CRC integrity')
        assert z.testzip() is None
        assert len(z.namelist())==len(archive_files)
        with tempfile.TemporaryDirectory(prefix='root_v144_check_') as tmp:
            z.extractall(tmp)
            extracted=Path(tmp)/ROOT.name
            print('[4/5] compare each file SHA-256')
            for row in (extracted/'manifest.sha256').read_text(encoding='utf-8').splitlines():
                expected, rel=row.split('  ',1)
                path=extracted/rel
                assert path.is_file() and digest(path)==expected,rel
            print('[5/5] independently rerun extracted project')
            subprocess.run([sys.executable,str(extracted/'run_all.py')],check=True,cwd=extracted,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            # verify rerun generated data matches original stored checksum
            for rel in ['results/summary.json','results/symbolic.json','results/group_algebra.json',
                        'results/kk_electron.json','results/mass_coupling_scan.csv']:
                assert digest(extracted/rel)==digest(ROOT/rel),f'nondeterministic {rel}'
            # unittest includes runtime duration; assert semantic identity, not elapsed seconds.
            import re
            def normalize_log(p):
                return re.sub(r'Ran (\d+) tests in [0-9.]+s',r'Ran \1 tests in <elapsed>s',p.read_text(encoding='utf-8'))
            assert normalize_log(extracted/'results/tests.log')==normalize_log(ROOT/'results/tests.log'),'nondeterministic tests.log excluding runtime'
    print('ZIP:',OUTPUT)
    print('ZIP size bytes:',OUTPUT.stat().st_size)
    print('files including manifest:',len(archive_files))
    print('SHA256 of zip:',digest(OUTPUT))
    print('PASS: fresh test suite, ZIP CRC, hashes, extracted rerun, result reproducibility')

if __name__=='__main__': main()
