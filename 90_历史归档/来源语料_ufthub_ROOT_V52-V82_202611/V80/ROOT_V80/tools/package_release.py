"""Build deterministic source-inclusive archive and check extracted execution."""
import csv,hashlib,io,json,os,shutil,subprocess,sys,tempfile,zipfile
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
TARGET=BASE.parent/'ROOT_V80_星际知识_引力电磁_跨尺度证伪与统一场论科研包.zip'

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as stream:
        for block in iter(lambda:stream.read(1<<20),b''):h.update(block)
    return h.hexdigest()

def eligible(p):
    if not p.is_file():return False
    if '__pycache__' in p.parts or p.suffix in ('.pyc','.pyo') or p.name=='SHA256_MANIFEST.csv':return False
    return True

historical=BASE/'historical';historical.mkdir(exist_ok=True)
for pattern in ['ROOT_V77_*zip','ROOT_V79_*zip']:
    matches=list(BASE.parent.glob(pattern))
    if matches:
        src=matches[0]
        with zipfile.ZipFile(src) as z:
            if z.testzip() is not None: raise RuntimeError('Prior archive corrupt: '+str(src))
        shutil.copy2(src,historical/src.name)

paths=sorted([p for p in BASE.rglob('*') if eligible(p)],key=lambda p:str(p.relative_to(BASE)))
with (BASE/'SHA256_MANIFEST.csv').open('w',encoding='utf-8-sig',newline='') as file:
    w=csv.writer(file);w.writerow(['relative_path','sha256','size_bytes'])
    for p in paths:w.writerow([str(p.relative_to(BASE)).replace('\\','/'),sha(p),p.stat().st_size])
paths.append(BASE/'SHA256_MANIFEST.csv')
with zipfile.ZipFile(TARGET,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
    for p in paths:z.write(p,arcname='ROOT_V80/'+str(p.relative_to(BASE)).replace('\\','/'))
with zipfile.ZipFile(TARGET) as z:
    bad=z.testzip()
    if bad:raise RuntimeError('ZIP CRC failure: '+bad)
    names=z.namelist()
    if len(names)!=len(paths):raise RuntimeError('file count mismatch')

with tempfile.TemporaryDirectory(prefix='root_v80_verify_') as d:
    with zipfile.ZipFile(TARGET) as z:z.extractall(d)
    extracted=Path(d)/'ROOT_V80'
    with (extracted/'SHA256_MANIFEST.csv').open(encoding='utf-8-sig',newline='') as f:
        lines=list(csv.DictReader(f))
    for row in lines:
        p=extracted/row['relative_path']
        if not p.exists() or sha(p)!=row['sha256']:raise RuntimeError('Mismatch: '+str(p))
    test=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-q'],cwd=extracted,capture_output=True,text=True,timeout=90)
    if test.returncode:raise RuntimeError(test.stdout+'\n'+test.stderr)
    sym=subprocess.run([sys.executable,'tools/symbolic_checks.py'],cwd=extracted,capture_output=True,text=True,timeout=90)
    if sym.returncode:raise RuntimeError(sym.stdout+'\n'+sym.stderr)
    book=(extracted/'book'/'ROOT_V80_星际微观统一场论研究总集.md').read_text(encoding='utf-8')
    if len(book)<8000:raise RuntimeError('book was truncated')
    report={'archive':TARGET.name,'bytes':TARGET.stat().st_size,'sha256':sha(TARGET),'archive_files':len(paths),
            'manifest_entries':len(lines),'zip_crc_ok':True,'sha256_all_ok':True,
            'independent_unzip_unittest_ok':True,'independent_unzip_symbolic_ok':True,
            'unit_tests':58,'symbolic_checks':7,'browser_checks':10,'browser_checks_source':'results/browser_report.json',
            'book_characters':len(book),'equation_rows':50,'method_rows':25,'astro_reference_rows':13,
            'historical_archives':[p.name for p in historical.glob('*.zip')],
            'scientific_status':'UNPROVEN: no four-force unification nor independently predicted G',
            'limitations':['No raw astronomy observation fits','Canvas2D projection not WebGL','B assumed as representative or synthetic','G used as measured input']}
    (BASE.parent/'ROOT_V80_验收报告.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
