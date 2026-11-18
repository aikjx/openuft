"""Build the actual V67 original manuscript without padding/repeating text."""
from pathlib import Path
import json
p=Path(__file__).resolve().parent
parts=sorted(p.glob('[0-2][0-9]_*.md'))
assert len(parts)==22,(len(parts),[x.name for x in parts])
header='# ROOT V67｜引力起源、空间螺旋与四力大统一：严格证明边界、完整物理审计与可复现实验\n\n'
body=header+'\n\n---\n\n'.join(x.read_text(encoding='utf-8') for x in parts)
(p/'ROOT_V67_统一场论_正式研究总集.md').write_text(body,encoding='utf-8')
count={'version':'V67','chapters':len(parts),'files':[x.name for x in parts],
       'original_manuscript_characters':len(body),'count_includes_markdown_and_math':True,
       'new_unified_field_theory_proof_complete':False}
(p/'manuscript_statistics.json').write_text(json.dumps(count,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in count.items() if k not in ('files',)},ensure_ascii=False))
