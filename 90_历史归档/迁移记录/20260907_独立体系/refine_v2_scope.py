# -*- coding: utf-8 -*-
"""One-time correction: the broad v2 review is not specific to S12."""
from pathlib import Path
from urllib.parse import unquote
import hashlib
import json
import os
import re
ROOT=Path(__file__).resolve().parents[3]
old=ROOT/'01_独立体系/S12_空间光速螺旋统一体系/13_论文与成果/论文正文/终极报告系列/v2_20260905.md'
new=ROOT/'03_跨体系研究/跨体系原著/综合综述_v2_20260905.md'
assert old.is_file() and not new.exists()
assert ROOT.name=='openuft'
old.rename(new)
pattern=re.compile(r'(!?\[[^\]\n]*\]\()([^\s)]+)(\))')
for p in ROOT.rglob('*.md'):
    if '90_历史归档' in p.relative_to(ROOT).parts:continue
    def fix(m):
        target=m.group(2)
        if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:',target) or target.startswith('#'):return m.group(0)
        path,sep,anchor=target.partition('#')
        parent=old.parent if p==new else p.parent
        dest=Path(os.path.normpath(str(parent/unquote(path))))
        if dest==old:dest=new
        if p!=new and dest!=new:return m.group(0)
        return m.group(1)+os.path.relpath(dest,p.parent).replace('\\','/')+(sep+anchor if sep else '')+m.group(3)
    body=p.read_text(encoding='utf-8-sig');updated=pattern.sub(fix,body)
    if updated!=body:p.write_text(updated,encoding='utf-8')
manifest=ROOT/'90_历史归档/迁移记录/20260907_独立体系/manifest.json'
data=json.loads(manifest.read_text(encoding='utf-8'))
for row in data['files']:
    if row['new']==old.relative_to(ROOT).as_posix():
        row['new']=new.relative_to(ROOT).as_posix()
        row['sha256_after']=hashlib.sha256(new.read_bytes()).hexdigest()
manifest.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
readme=old.parent/'README.md'
text=readme.read_text(encoding='utf-8').replace('v2 是更广泛的跨体系综述。','v2 是更广泛的跨体系综述，已移入跨体系原著区。')
text+='\n[跨体系 v2 原著]('+os.path.relpath(new,readme.parent).replace('\\','/')+')。\n'
readme.write_text(text,encoding='utf-8')
collection=new.parent/'README.md'
collection.write_text(collection.read_text(encoding='utf-8')+'\n[广泛跨体系综述 v2](综合综述_v2_20260905.md) 涉及多个候选，不归属单一 S12 公设。\n',encoding='utf-8')
print('Moved broad v2 review to cross-system source collection')
