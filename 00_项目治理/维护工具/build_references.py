# -*- coding: utf-8 -*-
"""Normalize the existing bibliography and global source register without inventing metadata."""
from pathlib import Path
import csv
import difflib
import html
import json
import os
import re
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'02_共享基础/参考资料'
def clean(s):return html.unescape(re.sub('<[^>]+>','',s))
def norm(s):return re.sub(r'[^\w]+','',clean(s).lower())
def author(a):return (a.get('family',a.get('name',''))+' '+a.get('given','')).strip()
records=[]
records.append({'id':'ZXQ2024','citation':'Zhang X Q. Unified Field Theory (Academic Edition): Extraterrestrial Technology[M]. Hope Grace Publishing, 2024. ISBN: 978-1966423058.','status':'用户提供；未取得全文，出版社和 ISBN 尚未独立核实','title':'Unified Field Theory (Academic Edition): Extraterrestrial Technology','author':'Zhang, X Q','year':'2024','publisher':'Hope Grace Publishing','isbn':'978-1966423058','type':'book','url':''})
metadata=json.loads((BASE/'文献元数据.json').read_text(encoding='utf-8'))
resolved=[r for r in metadata if r['status']=='metadata_retrieved']
legacy=BASE/'原参考文献待核底稿.md'
if not legacy.exists():legacy.write_bytes((BASE/'BIBLIOGRAPHY.md').read_bytes())
old=legacy.read_text(encoding='utf-8')
lines=[x[2:] for x in old.split('## H.')[0].splitlines() if x.startswith('- ')]
used=set()
for i,line in enumerate(lines,1):
    title_match=re.search(r'"([^"]+)"',line)
    if not title_match:title_match=re.search(r'\), \*([^*]+)\*',line)
    title=title_match.group(1) if title_match else line
    best=max(resolved,key=lambda r:difflib.SequenceMatcher(None,norm(title),norm(r['metadata']['title'][0])).ratio())
    ratio=difflib.SequenceMatcher(None,norm(title),norm(best['metadata']['title'][0])).ratio()
    rid='REF{:03d}'.format(i)
    if ratio>.90:
        m=best['metadata'];used.add(best['requested_doi']);authors=m.get('author',[])
        names=', '.join(author(a) for a in authors[:3])+(', et al' if len(authors)>3 else '')
        year=str(m.get('published',{}).get('date-parts',[['年份待核']])[0][0]);journal=clean(m.get('container-title',[''])[0]);title=clean(m['title'][0]);volume=m.get('volume','');issue=m.get('issue','');pages=m.get('page',m.get('article-number',''))
        cite='{}. {}[J]. {}, {}{}{}{}. DOI: {}.'.format(names,title,journal,year,', '+volume if volume else '', '('+issue+')' if issue else '', ': '+pages if pages else '',m['DOI'])
        records.append({'id':rid,'citation':cite,'status':'已核对 DOI 注册元数据；不表示审查正文','title':title,'author':' and '.join((a.get('family',a.get('name',''))+', '+a.get('given','')).strip(', ') for a in authors[:3])+(' and others' if len(authors)>3 else ''),'year':year,'journal':journal,'volume':volume,'number':issue,'pages':pages,'doi':m['DOI'],'url':'https://doi.org/'+m['DOI'],'type':'article'})
    elif 'Sorkin' in line:
        records.append({'id':rid,'citation':'Sorkin R D. Causal Sets: Discrete Gravity[M]//Gomberoff A, Marolf D, eds. Lectures on Quantum Gravity. Springer, 2005: 305–327. DOI: 10.1007/0-387-24992-3_7.','status':'出版社页面核对；原列表 2007 更正为 2005','author':'Sorkin, Rafael D.','title':'Causal Sets: Discrete Gravity','booktitle':'Lectures on Quantum Gravity','publisher':'Springer','year':'2005','pages':'305--327','doi':'10.1007/0-387-24992-3_7','url':'https://link.springer.com/chapter/10.1007/0-387-24992-3_7','type':'incollection'})
    elif 'mpmath Development' in line:
        records.append({'id':rid,'citation':'mpmath developers. mpmath: Python library for arbitrary-precision floating-point arithmetic[CP/OL]. https://mpmath.org/ (accessed 2026-09-09).','status':'官网核对；软件版本应由运行环境另行登记，不沿用任意 2024 年份','title':'mpmath: Python library for arbitrary-precision floating-point arithmetic','author':'{mpmath developers}','url':'https://mpmath.org/','type':'misc'})
    else:
        year_match=re.search(r'\((\d{4})\)',line);year=year_match.group(1) if year_match else ''
        names=line.split(' (',1)[0]
        citation=re.sub(r'\*','',line).rstrip('.')+'.'
        if title_match:
            tail=line[title_match.end():].strip(' *,')
            kind='M' if line.find('), *')>=0 else 'J'
            if 'Salam' in line:kind='M'
            tail=clean(tail).replace('*','')
            volume_match=re.match(r'^(.*?)\s+([A-Z]?\d.+)$',tail)
            if kind=='J' and volume_match:
                citation='{}. {}[J]. {}, {}, {}.'.format(names,title,volume_match.group(1),year,volume_match.group(2))
            else:
                citation='{}. {}[{}]. {}, {}.'.format(names,title,kind,tail,year)
        records.append({'id':rid,'citation':citation,'status':'按原有条目规范化；未独立核实版次、完整页码或出版元数据','title':title,'author':names,'year':year,'type':'misc','url':''})

# Preserve earlier additional reading entries rather than silently dropping them.
reading=[('READ01','Griffiths D. Introduction to Elementary Particles[M]. 2008.','Introduction to Elementary Particles'),('READ02','Peskin M E, Schroeder D V. An Introduction to Quantum Field Theory[M]. 1995.','An Introduction to Quantum Field Theory'),('READ03','Press W H, et al. Numerical Recipes[M]. 2007.','Numerical Recipes')]
for rid,cite,title in reading:records.append({'id':rid,'citation':cite,'title':title,'type':'misc','url':'','status':'保留原进一步阅读条目；版次与出版社待核实'})
with (ROOT/'05_全球研究/01_文献来源/文献登记.csv').open(encoding='utf-8-sig',newline='') as f:
    for row in csv.DictReader(f):
        cite='{}. {}[EB/OL]. {}. {} (accessed 2026-09-09).'.format(row['原作者'],row['原题名'],row['年份'],row['原始链接'])
        records.append({'id':'GLOBAL'+row['路线编号'][1:],'citation':cite,'author':row['原作者'].replace(';',' and'),'title':row['原题名'],'year':row['年份'] if row['年份'].isdigit() else '', 'url':row['原始链接'],'type':'misc','status':'沿用全球文献登记 '+row['来源编号']+' 的入口核实范围；arXiv 条目按在线版本引用'})
internal=[('LOCAL01','全维度修订v2.md'),('LOCAL02','完整严格证明.md'),('LOCAL03','绝热与纯圆周精确.md'),('LOCAL04','P5_梯度磁场精确性_R11/README.md'),('LOCAL05','v6_20260906_FINAL.md')]
for rid,filename in internal:
    matches=[p for p in ROOT.rglob(filename.split('/')[-1]) if '90_历史归档' not in p.relative_to(ROOT).parts and (filename in p.as_posix())]
    if matches:
        p=sorted(matches)[0];rel=os.path.relpath(p,BASE).replace('\\','/')
        records.append({'id':rid,'citation':'AI科技星. {}[R]. 项目内部研究稿，2026；版本以文件为准。'.format(p.stem),'title':p.stem,'author':'{AI科技星}','year':'2026','type':'misc','url':'','local_path':p.relative_to(ROOT).as_posix(),'local_link':rel,'status':'项目内部资料；未登记外部出版或同行评审'})

for row in records:row['citation']=row['citation'].replace('..','.')
body='# 统一参考文献与引用规则\n\n[结构化引用登记](引用登记.csv) · [BibTeX](references.bib) · [DOI 元数据及失败记录](文献元数据.json) · [原列表底稿](原参考文献待核底稿.md)。\n\n体系按物理内容命名；作者姓名用于来源署名。原题名保留原语言，不将他人著作归为本项目原创。引用登记只表示出处，不证明其中主张成立。\n\n## 用户指定著作\n\n'
body+='**[ZXQ2024]** '+records[0]['citation']+'\n\n'+records[0]['status']+'。未掌握具体页码时，不把项目某条公式断言为已由该书证明。\n\n## 经典、数学与软件文献\n\n'
for r in records[1:]:
    if r['id']=='GLOBAL01':body+='\n## 全球路线原始入口\n\n'
    if r['id']=='LOCAL01':body+='\n## 本项目内部研究稿\n\n'
    body+='**[{}]** {}\n\n核实范围：{}。'.format(r['id'],r['citation'],r['status'])
    if r.get('url'):body+=' [来源]('+r['url']+')。'
    if r.get('local_link'):body+=' [当前文件]('+r['local_link']+')。'
    body+='\n\n'
body+='## 正文引用与语言版本\n\n正文使用稳定编号，例如 [ZXQ2024]，并在能查到原文时补充具体页码/章节。书目数据由用户提供或尚未独立核实时，保留此状态，不猜测 DOI、页码、版次或译者。\n\n英文、日语摘要使用同一套引用编号和原文题名；只翻译说明文字，不虚构英文版、日文版或译本 ISBN。\n\n[English](../../05_全球研究/03_多语种协作/英语/项目介绍.md) · [日本語](../../05_全球研究/03_多语种协作/日语/项目介绍.md)。\n'
(BASE/'BIBLIOGRAPHY.md').write_text(body,encoding='utf-8')
with (BASE/'引用登记.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['id','citation','status','url','local_path'],extrasaction='ignore');w.writeheader();w.writerows(records)
def escape(s):return str(s).replace('\\','\\textbackslash{}').replace('{','\\{').replace('}','\\}').replace('&','\\&').replace('%','\\%').replace('_','\\_')
bib='% DOI metadata checked where indicated; unresolved fields are deliberately omitted.\n\n'
for r in records:
    bib+='@'+r['type']+'{'+r['id']+',\n'
    for key in ['author','title','year','publisher','journal','booktitle','volume','number','pages','doi','isbn','url']:
        if r.get(key):bib+='  '+key+' = {'+str(r[key]).replace('&','\\&').replace('%','\\%')+'},\n'
    bib+='  note = {'+r['status']+'}\n}\n\n'
(BASE/'references.bib').write_text(bib,encoding='utf-8')
print('References:',len(records),'DOI metadata entries:',len(resolved),'Internal entries:',sum(x['id'].startswith('LOCAL') for x in records))
