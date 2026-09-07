# -*- coding: utf-8 -*-
"""Current independent-system layout audit. Counts and classifies every directory."""
from pathlib import Path
import json
import os
from collections import Counter

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'00_governance'

def main():
    layout=json.loads((OUT/'layout.json').read_text(encoding='utf-8'))
    registry=json.loads((OUT/'system_registry.json').read_text(encoding='utf-8'))['systems']
    titles={s['id']:s['title'] for s in registry};titles['_template']='新体系模板'
    kinds={s['id']:s['kind'] for s in registry}
    stage_names=dict(zip(layout['stages'],['立项','文献','公设','数学形式','推导','一致性','预测','计算','数据','验证','不确定度','证伪','结论','论文','评审','发布','归档']))
    roles={'00_governance':'项目规则、索引及审计','01_systems':'按基础前提独立管理体系','02_shared':'共同方法、常数与基准','03_comparative':'显式跨体系比较及组合','04_publications':'跨体系综述与公共展示','90_archive':'历史布局及迁移证据','99_inbox':'归属未定的输入','.github':'协作平台配置'}
    subroles={'src':'主实现','tests':'实现与回归断言','runs':'独立运行记录','configs':'配置输入','notebooks':'交互探索','raw':'原始数据主副本','processed':'可溯源派生数据','external':'外部来源与获取说明','manuscript':'原著与论文','figures':'图表及生成来源','supplement':'补充说明'}
    files=[p for p in ROOT.rglob('*') if p.is_file()]
    direct=Counter(p.parent for p in files)
    recursive=Counter()
    for path in files:
        for parent in path.parents:
            if parent==ROOT:break
            recursive[parent]+=1
    records=[]
    for p in sorted(q for q in ROOT.rglob('*') if q.is_dir()):
        rel=p.relative_to(ROOT).as_posix();parts=rel.split('/')
        if parts[0] not in roles:raise ValueError('Unknown root '+rel)
        role=roles[parts[0]];reason='职责范围与理论主文件分离';risk='目录齐备不代表工作完成'
        owner=parts[0]
        if parts[0]=='01_systems' and len(parts)>1:
            if parts[1] not in titles:raise ValueError('Unknown system '+rel)
            owner=parts[1];role=titles[owner];reason='该体系拥有独立身份、证据及发布位置';risk='与相关体系可有谱系关系，不能自动继承证据'
            if len(parts)>2:
                if parts[2] not in stage_names:raise ValueError('Unknown stage '+rel)
                role += ' / '+stage_names[parts[2]];reason='以本体系为作用域保留此生命周期职责'
                if len(parts)>3:role += ' / '+subroles.get(parts[3],parts[3]);reason='本体系内的专题或资料分组，避免流入公共总筐'
                if parts[2]=='90_archive':risk='体系历史保留原始表述，不表示科学认可'
                if kinds.get(owner)=='unformulated_direction':risk='待建模方向，尚无具体公设，不计为已建立理论'
        elif parts[0]=='90_archive':reason='保留历史分析和逐字节快照';risk='旧布局说明与工具不得作为当前约定'
        elif parts[:2]==['02_shared','computation']:risk='仅共同常数和经典演示；候选理论实现归各体系'
        elif parts[:2]==['03_comparative','source_collections']:reason='跨体系原著只有一份主文件，独立章节可溯源';risk='摘录是派生产物，不是互相独立的原始证据'
        elif parts[0]=='99_inbox':risk='需审理归属与负责人，不能堆积为新的总筐'
        records.append({'path':rel,'owner':owner,'direct_files':direct[p],'recursive_files':recursive[p],'role':role,'reason':reason,'risk':risk})
    directions=sum(s['kind']=='unformulated_direction' for s in registry)
    payload={'directory_count':len(records),'file_count':len(files),'system_containers':len(registry),'research_modules':len(registry)-directions,'unformulated_directions':directions,'records':records}
    (OUT/'directory_audit.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    text='# 独立体系布局：全部目录审计\n\n[设计与最优性分析](INDEPENDENT_SYSTEMS_DESIGN.md) · [类型与扩展](SCALABILITY_REVIEW.md) · [机器清单](directory_audit.json)。\n\n当前扫描 {} 个实际目录、{} 个文件；{} 个研究模块与 {} 个待建模方向独立管理，另有模板。类型不证明科学状态或来源有效性。历史目录也逐项列出；不展开 ZIP。递归文件数不可相加作为总数。目录职责由路径规则判定，不表示逐篇科学审定。\n\n| 目录 | 主归属 | 直接/递归文件 | 职责 | 设置理由 | 边界 |\n|---|---|---:|---|---|---|\n'.format(len(records),len(files),len(registry)-directions,directions)
    for r in records:
        target=os.path.relpath(ROOT/r['path'],OUT).replace('\\','/')
        text+='| [{}]({}/) | {} | {}/{} | {} | {} | {} |\n'.format(r['path'],target,r['owner'],r['direct_files'],r['recursive_files'],r['role'],r['reason'],r['risk'])
    (OUT/'DIRECTORY_AUDIT.md').write_text(text,encoding='utf-8')
    print('Audited {} directories; {} independent containers'.format(len(records),len(registry)))

if __name__=='__main__':main()
