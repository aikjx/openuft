"""Freeze source SHA256 hashes, build V71 zip, and verify archive by reading every entry."""
from pathlib import Path
from hashlib import sha256
import csv,zipfile,json
P=Path(__file__).resolve().parent
OUT=P.parent/'ROOT_V71_四力统一全方法攻坚_95方程_67路线_有限尺寸实验.zip'
H=P/'SHA256_MANIFEST.csv'
source_dirs={'book','rootv71','tests','archive','web'}
source_files={'README.md','SOURCES.md','RELEASE_NOTES.md','RUN_ALL.sh','RUN_ALL.bat','requirements.txt',
              'generate_catalog.py','generate_methods.py','symbolic_audit.py','experiments.py',
              'build_web.py','browser_smoke.py','run_all.py','make_release.py','verify_release.py'}
fixed=[]
for f in sorted(P.rglob('*')):
    if not f.is_file():continue
    relative=f.relative_to(P).as_posix()
    if '__pycache__' in f.parts or relative=='SHA256_MANIFEST.csv':continue
    if f.parts[len(P.parts)] in source_dirs or relative in source_files or relative.startswith('data/ROOT_V71_全部核心方程') or relative.startswith('data/ROOT_V71_跨学科全部主要方法'):
        fixed.append(f)
with H.open('w',newline='',encoding='utf-8-sig') as h:
    writer=csv.writer(h);writer.writerow(['path','sha256','bytes'])
    for f in fixed:
        writer.writerow([f.relative_to(P).as_posix(),sha256(f.read_bytes()).hexdigest(),f.stat().st_size])
allfiles=[f for f in sorted(P.rglob('*')) if f.is_file() and '__pycache__' not in f.parts]
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
    for f in allfiles: z.write(f,arcname=(P.name+'/'+f.relative_to(P).as_posix()))
with zipfile.ZipFile(OUT,'r') as z:
    bad=z.testzip();assert bad is None,bad
    entries=z.namelist()
    assert len(entries)==len(allfiles)
    assert any(n.endswith('README.md') for n in entries)
    assert any(n.endswith('ROOT_V70_前版研究包.zip') for n in entries)
report={'version':'71.0','zip':OUT.name,'zip_bytes':OUT.stat().st_size,
        'zip_sha256':sha256(OUT.read_bytes()).hexdigest(),
        'zip_files':len(entries),'sha256_source_files':len(fixed),
        'zip_integrity':'pass, testzip read every file',
        'claims':'software validation only; four force unification NOT proven'}
(P.parent/'ROOT_V71_压缩包完整性报告.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
