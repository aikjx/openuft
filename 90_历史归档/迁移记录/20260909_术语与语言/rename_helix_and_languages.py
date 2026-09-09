# -*- coding: utf-8 -*-
"""One-time user-directed terminology change; keep bibliographic authors intact."""
from pathlib import Path
import csv
import hashlib
import json
import os
import zipfile
ROOT=Path(__file__).resolve().parents[2]
OLD='S02_张祥前空间运动与统一力';NEW='S02_空间光速螺旋统一力'
base=ROOT/'90_历史归档/迁移记录/20260909_术语与语言'
if (base/'变更清单.json').exists():raise SystemExit('Already applied')
replacements=[(OLD,NEW),('s02_zhang_space_motion','s02_light_speed_helix_force'),('张祥前空间运动与统一力','空间光速螺旋统一力'),('张祥前统一力','空间光速螺旋统一力'),('张祥前空间运动','空间光速螺旋运动'),('张祥前统一场论','空间光速螺旋统一场论'),('zhang_unified_force','helix_unified_force'),('zhang_force','helix_force'),('大统一力方程（张祥前）','空间光速螺旋统一力方程')]
changes=[]
for p in ROOT.rglob('*'):
    if not p.is_file() or '90_历史归档' in p.relative_to(ROOT).parts or p.suffix not in ['.md','.py','.json','.csv','.cff','.yml']:continue
    if p==Path(__file__).resolve():continue
    try:before=p.read_text(encoding='utf-8-sig')
    except UnicodeDecodeError:continue
    after=before
    for old,new in replacements:after=after.replace(old,new)
    newpath=p.relative_to(ROOT).as_posix().replace(OLD,NEW).replace('zhang_force.py','helix_force.py')
    if after!=before or newpath!=p.relative_to(ROOT).as_posix():changes.append((p,newpath,after,p.read_bytes()))
base.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(base/'变更前原件.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p,_,_,raw in changes:z.writestr(p.relative_to(ROOT).as_posix(),raw)
source=ROOT/'01_独立体系'/OLD;target=ROOT/'01_独立体系'/NEW
assert source.is_dir() and not target.exists()
assert str(source.resolve()).startswith(str(ROOT.resolve())+os.sep) and str(target.resolve()).startswith(str(ROOT.resolve())+os.sep)
source.rename(target)
oldcode=target/'07_计算复现/源码/zhang_force.py';newcode=oldcode.with_name('helix_force.py');oldcode.rename(newcode)
records=[]
for p,newpath,after,raw in changes:
    dst=ROOT/newpath;dst.write_text(after,encoding='utf-8')
    records.append({'old':p.relative_to(ROOT).as_posix(),'new':newpath,'sha256_before':hashlib.sha256(raw).hexdigest()})
(base/'变更清单.json').write_text(json.dumps({'scope':'名称、目录、标识与引用入口修订；历史原件保留','files':records},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
config_path=ROOT/'00_项目治理/国际化配置.json';config=json.loads(config_path.read_text(encoding='utf-8'))
if not any(x['语言代码']=='ja' for x in config['语言版本']):config['语言版本'].append({'语言代码':'ja','显示名称':'日本語（可选）','入口':'05_全球研究/03_多语种协作/日语/项目介绍.md','范围':'项目参与摘要，非全库翻译；待独立语言审查'})
config_path.write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
translations=ROOT/'05_全球研究/03_多语种协作/翻译登记.csv'
with translations.open(encoding='utf-8-sig',newline='') as f:reader=csv.DictReader(f);fields=reader.fieldnames;rows=list(reader)
if not any(x['目标语言']=='ja' for x in rows):rows.append(dict(zip(fields,['T002','国际参与说明.md','2026-09-09参与说明摘要','ja','05_全球研究/03_多语种协作/日语/项目介绍.md','自动辅助整理','摘要草稿待独立语言审查',''])))
with translations.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
for rel in ['README.md','INDEX.md','QUICKSTART.md']:
    p=ROOT/rel;text=p.read_text(encoding='utf-8-sig');note='\n\n[English](05_全球研究/03_多语种协作/英语/项目介绍.md) · [日本語](05_全球研究/03_多语种协作/日语/项目介绍.md) · [参考文献](02_共享基础/参考资料/BIBLIOGRAPHY.md)\n'
    line=text.find('\n');p.write_text(text[:line]+note+text[line:],encoding='utf-8')
meta_path=target/'system.json';meta=json.loads(meta_path.read_text(encoding='utf-8'));meta['bibliography_ids']=['ZXQ2024'];meta['naming_note']='体系按空间光速螺旋物理描述命名；S02 为统一力专题，S12 为综合研究。作者只作来源署名。'
meta_path.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
citation='Zhang X Q. Unified Field Theory (Academic Edition): Extraterrestrial Technology[M]. Hope Grace Publishing, 2024. ISBN: 978-1966423058.'
for sid in [NEW,'S12_空间光速螺旋统一体系']:
    p=ROOT/'01_独立体系'/sid/'01_文献来源/README.md'
    p.write_text(p.read_text(encoding='utf-8')+'\n## 引用来源 ZXQ2024\n\n'+citation+'\n\n书目信息由用户提供；本次未取得书籍全文，未核对具体命题对应页码。体系名称使用“空间光速螺旋”，作者姓名仅用于来源归属。\n\n[统一参考文献](../../../02_共享基础/参考资料/BIBLIOGRAPHY.md)。\n',encoding='utf-8')
print('Renamed S02 and registered Japanese; changed files:',len(records))
