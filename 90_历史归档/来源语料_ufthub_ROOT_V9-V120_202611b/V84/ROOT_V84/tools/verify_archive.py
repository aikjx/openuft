"""Verify final ZIP via independent extraction and rerun."""
from pathlib import Path
import tempfile,zipfile,hashlib,csv,subprocess,sys,json
ROOT=Path(__file__).resolve().parents[1]
ARCH=ROOT.parent/'ROOT_V84_多距离引力调制_有限尺寸第五力_假信号反例_可复现科研包.zip'
def verify():
    with tempfile.TemporaryDirectory(prefix='ROOT_V84_verify_') as tmp:
        with zipfile.ZipFile(ARCH) as z:
            assert z.testzip() is None
            z.extractall(tmp)
            entries=len(z.infolist())
        root=Path(tmp)/'ROOT_V84'
        with (root/'SHA256_MANIFEST.csv').open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
        for row in rows:
            p=root/row['relative_path']
            assert p.is_file() and p.stat().st_size==int(row['size_bytes'])
            assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],str(p)
        cmds=[('unittest',[sys.executable,'run_all.py']),('symbolic',[sys.executable,'tools/symbolic_checks.py']),('numpy_quad',[sys.executable,'tools/independent_reference.py'])]
        checks=[]
        for name,cmd in cmds:
            r=subprocess.run(cmd,cwd=root,capture_output=True,text=True,timeout=40)
            assert r.returncode==0,(name,r.stdout,r.stderr)
            checks.append(name)
        return {'zip_integrity_pass':True,'zip_entries':entries,'verified_hashes':len(rows),'independent_extract_checks':checks,'all_pass':True,'science_status':'SIMULATED_ONLY'}
if __name__=='__main__':print(json.dumps(verify(),ensure_ascii=False,indent=2))
