"""Reproducible ZIP creator: include only stable project assets, verify CRC & SHA256.
Usage: python build_release.py [output.zip]. Run inside extracted project.
"""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED,ZipInfo
import hashlib,sys,json
root=Path(__file__).resolve().parent
out=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else root.parent/'ROOT_V64_大统一场论失败原因逐项修复与引力起源精算科研包.zip'
skip_parts={'__pycache__','.pytest_cache','.git','.venv'}
def included():
 for f in root.rglob('*'):
  if f.is_file() and not any(p in skip_parts for p in f.relative_to(root).parts) and not f.name.endswith(('.pyc','.tmp','.log.bak')) and f.name!='FILE_SHA256_MANIFEST.txt':
   yield f
files=sorted(included(),key=lambda x:str(x.relative_to(root)))
manifest='ROOT V64 · SHA256 文件清单 (不包括清单本身)\n'
for f in files:
 h=hashlib.sha256(f.read_bytes()).hexdigest()
 manifest+=f'{h}  {f.relative_to(root).as_posix()}\n'
(root/'FILE_SHA256_MANIFEST.txt').write_text(manifest,encoding='utf-8')
files.append(root/'FILE_SHA256_MANIFEST.txt')
out.parent.mkdir(parents=True,exist_ok=True)
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=9) as z:
 for f in files:
  rel=(Path('ROOT_V64')/f.relative_to(root)).as_posix()
  entry=ZipInfo(rel,date_time=(2026,11,17,0,0,0))
  entry.compress_type=ZIP_DEFLATED;entry.external_attr=(0o644<<16)
  z.writestr(entry,f.read_bytes(),compress_type=ZIP_DEFLATED,compresslevel=9)
with ZipFile(out) as z:
 assert z.testzip() is None
 assert len(z.namelist())==len(files)
 for f in files:
  arc=(Path('ROOT_V64')/f.relative_to(root)).as_posix()
  assert hashlib.sha256(z.read(arc)).digest()==hashlib.sha256(f.read_bytes()).digest()
summary={'zip_path':str(out),'zip_bytes':out.stat().st_size,'files_in_zip':len(files),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'crc_and_hash_verification':'passed'}
print(json.dumps(summary,ensure_ascii=False,indent=2))
(out.parent/'ROOT_V64_压缩包校验_SHA256.txt').write_text(summary['sha256']+'  '+out.name+'\n',encoding='utf-8')
