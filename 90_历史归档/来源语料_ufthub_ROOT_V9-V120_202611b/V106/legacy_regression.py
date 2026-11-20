"""Run original V105 archive unchanged in an isolated temporary directory."""
from pathlib import Path
import zipfile,tempfile,subprocess,sys
ROOT=Path(__file__).resolve().parent

def run():
  archive=ROOT/'archive'/'ROOT_V105_original.zip'
  with tempfile.TemporaryDirectory(prefix='root_v106_legacy_') as td:
    out=Path(td)
    with zipfile.ZipFile(archive) as z:
      if z.testzip() is not None:raise RuntimeError('legacy archive CRC failed')
      for item in z.infolist():
        dst=(out/item.filename).resolve()
        if not dst.is_relative_to(out.resolve()):raise RuntimeError('unsafe zip path')
      z.extractall(out)
    proc=subprocess.run([sys.executable,'run_all.py'],cwd=out,capture_output=True,text=True,timeout=120)
    print('V105 legacy exit:',proc.returncode,'\n',proc.stdout[-2000:],proc.stderr[-2000:])
    if proc.returncode:raise RuntimeError('legacy regression failed')
    return True
if __name__=='__main__':run()
