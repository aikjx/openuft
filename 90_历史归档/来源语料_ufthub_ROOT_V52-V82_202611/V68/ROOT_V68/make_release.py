"""Build verified ZIP with root directory ROOT_V68. Excludes cache files."""
from pathlib import Path
import zipfile,hashlib,json,subprocess,sys
root=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(root/'create_manifest.py')],cwd=root,check=True)
subprocess.run([sys.executable,str(root/'VERIFY_PACKAGE.py')],cwd=root,check=True)
out=root.parent/'ROOT_V68_引力常数_规范群_量子一致性三大证明缺口科研总集.zip'
paths=[p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and not p.suffix=='.pyc']
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8,allowZip64=True) as z:
    for p in sorted(paths):z.write(p,arcname='ROOT_V68/'+str(p.relative_to(root)).replace('\\','/'))
with zipfile.ZipFile(out) as z:
    failure=z.testzip();names=z.namelist()
    if failure:raise RuntimeError('ZIP CRC failure: '+failure)
    if len(names)!=len(paths):raise RuntimeError('ZIP missing files')
report={'zip':out.name,'archive_bytes':out.stat().st_size,'zip_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
        'file_count':len(names),'zip_crc':'PASS','immutable_source_manifest':'PASS',
        'science_state':'OPEN: G independent prediction, complete GUT and experimental discovery unproven'}
(root.parent/'ROOT_V68_发布验收报告.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
