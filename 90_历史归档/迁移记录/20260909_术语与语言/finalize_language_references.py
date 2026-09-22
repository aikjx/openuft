# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib
import json
import re
import zipfile
ROOT=Path(__file__).resolve().parents[2]
base=ROOT/'90_历史归档/迁移记录/20260909_术语与语言'
manifest_path=base/'变更清单.json';data=json.loads(manifest_path.read_text(encoding='utf-8'))
seen={r['new'] for r in data['files']}
newdir=ROOT/'01_独立体系/S02_空间光速螺旋统一力'
with zipfile.ZipFile(base/'变更前原件.zip','a',zipfile.ZIP_DEFLATED) as z:
    for p in newdir.rglob('*'):
        if not p.is_file() or p.relative_to(ROOT).as_posix() in seen:continue
        new=p.relative_to(ROOT).as_posix();old=new.replace('S02_空间光速螺旋统一力','S02_张祥前空间运动与统一力')
        if '90_历史归档' not in p.relative_to(newdir).parts:continue
        raw=p.read_bytes();z.writestr(old,raw);data['files'].append({'old':old,'new':new,'sha256_before':hashlib.sha256(raw).hexdigest()})
manifest_path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
citation='Zhang X Q. Unified Field Theory (Academic Edition): Extraterrestrial Technology[M]. Hope Grace Publishing, 2024. ISBN: 978-1966423058.'
for p in ROOT.rglob('*.md'):
    if '90_历史归档' in p.relative_to(ROOT).parts:continue
    text=p.read_text(encoding='utf-8-sig');updated=text.replace('大统一力（张祥前）','空间光速螺旋统一力').replace('大统一力(张祥前)','空间光速螺旋统一力').replace('张祥前函数','空间光速螺旋统一力函数')
    updated=re.sub(r'张祥前[.。]\s*《统一场论》[.。]?',citation,updated)
    if updated!=text:p.write_text(updated,encoding='utf-8')
p=newdir/'90_历史归档/README.md';p.write_text(p.read_text(encoding='utf-8').replace('张祥前空间运动与统一力','空间光速螺旋统一力'),encoding='utf-8')
p=ROOT/'05_全球研究/03_多语种协作/README.md'
p.write_text('# 多语种协作\n\n[简体中文](../../README.md) · [English](英语/项目介绍.md) · [日本語](日语/项目介绍.md)\n\n英文目录：`英语/`；日语目录：`日语/`。两者现有内容为项目参与摘要，不是研究正文全译；中文保持默认。\n\n[语言入口](语言入口.md) · [翻译登记](翻译登记.csv) · [国际化配置](../../00_项目治理/国际化配置.json)\n\n引用沿用原作者、原题名与稳定编号，不自行创造译本或 ISBN。翻译草稿与独立语言审查状态分别登记。\n',encoding='utf-8')
p=newdir/'04_理论推导/D5_大统一力方程/README.md';p.write_text(p.read_text(encoding='utf-8')+'\n## 引用来源\n\n[ZXQ2024] '+citation+'\n\n书目由用户提供，具体页码与论证对应尚待原文核对。[统一参考文献](../../../../02_共享基础/参考资料/BIBLIOGRAPHY.md)。\n',encoding='utf-8')
p=ROOT/'02_共享基础/参考资料/README.md';p.write_text(p.read_text(encoding='utf-8')+'\n## 引用文件\n\n[统一参考文献](BIBLIOGRAPHY.md) · [引用登记](引用登记.csv) · [BibTeX](references.bib)。ZXQ2024 使用用户指定书目；其他条目逐条标明元数据核实范围。\n',encoding='utf-8')
for name in ['rename_helix_and_languages.py','finalize_language_references.py']:
    src=ROOT/'00_项目治理/维护工具'/name;dest=base/name
    assert src.is_file() and not dest.exists();src.rename(dest)
print('Completed language entries, source labels and rename ledger')
