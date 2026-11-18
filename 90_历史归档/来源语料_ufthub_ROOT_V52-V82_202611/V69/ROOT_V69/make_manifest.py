"""Create a manifest for immutable source / documentation / initial data / archived research.
Generated logs and plots excluded: regenerating them must not cause false integrity failures.
"""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent
files={}
for path in sorted(P.rglob('*')):
    if not path.is_file(): continue
    rel=path.relative_to(P).as_posix()
    if rel.startswith(('results/','__pycache__/')) or '/__pycache__/' in rel or rel.endswith('.pyc'):
        continue
    if rel in {'SOURCE_SHA256_MANIFEST.json','PACKAGE_VALIDATION.json'}:continue
    files[rel]={'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
(P/'SOURCE_SHA256_MANIFEST.json').write_text(json.dumps({'schema':'ROOT_V69_manifest_1','files':files},ensure_ascii=False,indent=2),encoding='utf-8')
print(len(files),'immutable entries; archived V68 included')
