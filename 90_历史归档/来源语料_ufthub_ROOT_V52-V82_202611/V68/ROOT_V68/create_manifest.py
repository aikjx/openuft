"""Build immutable-source SHA256 file list. Intended before release and before ZIP creation."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
roots=('src','tests','experiments','book','web','sources','archive','README.md','RELEASE_NOTES.md','requirements-optional.txt','RUN_ALL.sh','RUN_ALL.bat','run_all.py','create_manifest.py','VERIFY_PACKAGE.py')
files=[]
for part in roots:
    p=root/part
    if p.is_file():files.append(p)
    elif p.is_dir():files.extend(q for q in p.rglob('*') if q.is_file() and '__pycache__' not in q.parts and not q.name.endswith('.pyc'))
files=sorted(set(files))
entries=[{'path':str(p.relative_to(root)).replace('\\','/'), 'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
manifest={'description':'Hash list of immutable release files. Re-generated results/data can differ after reruns; verify ZIP CRC separately.','files':entries}
(root/'SOURCE_SHA256_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Immutable files:',len(entries))
