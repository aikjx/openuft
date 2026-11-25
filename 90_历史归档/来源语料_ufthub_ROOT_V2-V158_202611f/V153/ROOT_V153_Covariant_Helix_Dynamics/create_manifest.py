"""Regenerate manifest after intentional source/figure modifications."""
from pathlib import Path
import hashlib
import json
root=Path(__file__).resolve().parent
files={}
for p in sorted(root.rglob('*')):
    if not p.is_file() or '__pycache__' in p.parts: continue
    if p.name in ('manifest.json','create_manifest.py'): continue
    rel=p.relative_to(root).as_posix()
    files[rel]=hashlib.sha256(p.read_bytes()).hexdigest()
(root/'manifest.json').write_text(json.dumps({
    'version':'ROOT V153','date':'2026-11-25',
    'description':'Math/program audit only, NOT a proof of unification',
    'files':files},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Created manifest for',len(files),'files')
