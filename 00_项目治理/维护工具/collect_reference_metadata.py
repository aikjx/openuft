# -*- coding: utf-8 -*-
"""Read DOI registration metadata; preserve failures instead of inventing fields."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json
import urllib.request
import urllib.parse

ROOT=Path(__file__).resolve().parents[2]
DOIS=['10.1002/andp.19163540702','10.1103/PhysRev.47.777','10.1007/BF01328531','10.1007/BF01328377','10.1002/andp.19263840404','10.1098/rspa.1928.0023','10.1007/BF01339504','10.1103/PhysRev.96.191','10.1103/PhysRevLett.30.1343','10.1103/PhysRevLett.30.1346','10.1103/PhysRevLett.19.1264','10.1103/PhysRevLett.32.438','10.1016/0003-4916(75)90211-0','10.1016/0370-2693(84)91565-X','10.1016/0550-3213(95)00158-O','10.1103/PhysRevLett.57.2244','10.1007/0-387-24992-3_7','10.1103/PhysRevD.23.347','10.1086/300499','10.1051/0004-6361/201833910','10.1103/PhysRevLett.116.061102','10.1103/PhysRevLett.119.161101','10.1007/BF02345020','10.1103/PhysRevD.7.2333','10.1007/BF01645742','10.7717/peerj-cs.103']
def fetch(doi):
    url='https://api.crossref.org/works/'+urllib.parse.quote(doi,safe='')
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'OpenUFT-reference-audit/1.0','Accept':'application/json'})
        with urllib.request.urlopen(req,timeout=30) as response:data=json.load(response)['message']
        keys=['DOI','type','title','author','container-title','publisher','volume','issue','page','article-number','published','published-print','published-online','ISBN','URL','editor']
        return {'requested_doi':doi,'metadata_source':url,'checked_at':'2026-09-09','status':'metadata_retrieved','metadata':{k:data[k] for k in keys if k in data}}
    except Exception as exc:return {'requested_doi':doi,'status':'unresolved','error':str(exc)}
def main():
    with ThreadPoolExecutor(max_workers=4) as pool:records=list(pool.map(fetch,DOIS))
    (ROOT/'02_共享基础/参考资料/文献元数据.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for row in records:print(row['requested_doi'],row['status'],row.get('metadata',{}).get('title'),row.get('metadata',{}).get('published'))
if __name__=='__main__':main()
