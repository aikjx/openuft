"""Create deterministic static manifest after all research and tests are finished."""
from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parent
files=sorted((p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and '.pytest_cache' not in p.parts
    and p.name not in ('CHECKSUMS.sha256','MANIFEST.json') and not p.name.endswith(('.pyc','.pyo'))),key=lambda p:str(p.relative_to(root)))
rows=[{'path':str(p.relative_to(root)), 'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
manifest={'research_name':'ROOT V111 Noether/metric-variation audit',
  'date':'2026-11-20', 'scientific_status':'conditional existing EFT mechanics; no solved four-force unification',
  'historical_issues':396,'file_count':len(rows),'files':rows}
(root/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
rows.append({'path':'MANIFEST.json','sha256':hashlib.sha256((root/'MANIFEST.json').read_bytes()).hexdigest()})
(root/'CHECKSUMS.sha256').write_text('\n'.join(x['sha256']+'  '+x['path'] for x in rows)+'\n',encoding='utf-8')
print('Manifest',len(rows),'hashed including manifest')
