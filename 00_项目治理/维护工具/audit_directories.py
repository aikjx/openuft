# -*- coding: utf-8 -*-
"""Current independent-system layout audit. Counts and classifies every directory."""
from pathlib import Path
import json
import os
import subprocess
import sys
from collections import Counter

ROOT=Path(__file__).resolve().parents[2]
GOV=ROOT/'00_项目治理'
OUT=GOV/'审计记录'


def tracked_files(root: Path) -> list[Path]:
    """返回 root 下**被 git 跟踪**的文件（相对 root 的绝对路径）。

    `git ls-files` 在子目录中执行时输出相对该子目录的路径，正好与审计记录里的
    相对链接一致。索引里已删除的文件会被 exists() 过滤掉。

    不在 git 仓库中时（例如打包导出）退回 rglob，此时不再保证与干净副本一致。
    """
    try:
        proc = subprocess.run(['git', 'ls-files', '-z'], cwd=str(root),
                              capture_output=True, timeout=120)
        ok = proc.returncode == 0
    except (OSError, subprocess.SubprocessError):
        ok = False
    if not ok:
        return [p for p in root.rglob('*') if p.is_file()]
    # git 按字节输出路径，一律用 surrogateescape 解码，避免遇到非 UTF-8 文件名直接崩
    names = [n for n in proc.stdout.decode('utf-8', 'surrogateescape').split('\0') if n]
    out = []
    for name in names:
        p = root / name
        if p.is_file():
            out.append(p)
    return out

def main():
    layout=json.loads((GOV/'layout.json').read_text(encoding='utf-8'))
    registry=json.loads((GOV/'system_registry.json').read_text(encoding='utf-8'))['systems']
    titles={s.get('directory',s['id']):s['title'] for s in registry};titles['新体系模板']='新体系模板'
    kinds={s.get('directory',s['id']):s['kind'] for s in registry}
    stage_names=dict(zip(layout['stages'],['立项','文献','公设','数学形式','推导','一致性','预测','计算','数据','验证','不确定度','证伪','结论','论文','评审','发布','归档']))
    roles={'00_项目治理':'项目规则、索引及审计','01_独立体系':'按基础前提独立管理体系','02_共享基础':'共同方法、常数与基准','03_跨体系研究':'显式跨体系比较及组合','04_公共成果':'跨体系综述与公共展示','05_全球研究':'全球文献覆盖、翻译及协作','06_统一体系层':'给独立体系建立可并列比较的坐标系，处理同名异义与谱系关系','07_统一场方程':'给出可推导可验证的正式理论核心（UFE-1）','90_历史归档':'历史布局及迁移证据','99_待整理资料':'归属未定的输入','.github':'协作平台配置'}
    # 注意：并发会话新建的 书籍/ 未登记进 layout.json（其 README 明确写了"不改
    # layout.json"），故此处**不**给它硬编码职责，让它走下面的未登记通道被点出来，
    # 而不是由审计脚本替它默认补登记。
    # 兜底：审计工具应当**报告**违规而不是被违规卡死。
    # 此前每新增一个顶层目录（先是 06_统一体系层，紧接着是会话有意新建但未登记进
    # layout.json 的 书籍/），重跑即 ValueError: Unknown root XXX，整份审计停摆。
    # 现改为：layout.json 已登记或有职责说明的照常处理；其余顶层目录照样进表，
    # 但职责标为未登记、边界栏点名缺失，并在结尾汇总告警。
    unregistered: set[str] = set()
    subroles={'源码':'主实现','测试':'实现与回归断言','运行记录':'独立运行记录','配置':'配置输入','交互笔记':'交互探索','原始数据':'原始数据主副本','处理后数据':'可溯源派生数据','外部数据':'外部来源与获取说明','论文正文':'原著与论文','图表':'图表及生成来源','补充材料':'补充说明'}
    # 扫描必须以**git 已跟踪**的文件为准，不能用 rglob 扫工作区。
    # 原因：DIRECTORY_AUDIT.md 里的每条记录都是指向目标目录的相对链接，而发布流程会在
    # 干净副本里跑 verify.py 检查全仓链接。rglob 会把只含被忽略内容的目录
    # （__pycache__/、只装了 font/js 却被忽略的 _shared/ 等）也列进表，
    # 这些目录不被 git 跟踪 -> 干净副本里根本不存在 -> 发布被自己的文档判成
    # "Broken link" 而中止（实际发生：FAIL: 18 issues）。
    files=tracked_files(ROOT)
    direct=Counter(p.parent for p in files)
    recursive=Counter()
    for path in files:
        for parent in path.parents:
            if parent==ROOT:break
            recursive[parent]+=1
    records=[]
    dirs=sorted({parent for path in files for parent in path.parents if parent!=ROOT and parent.is_relative_to(ROOT)})
    # 顶层目录同样只看跟踪内容：一个目录若在磁盘上存在却毫无跟踪文件，
    # 它不会出现在审计表里，再告警就很费解。
    for _top in {p.relative_to(ROOT).as_posix().split('/')[0] for p in dirs}:
        if _top not in roles:
            unregistered.add(_top)
            roles[_top] = '未登记顶层目录'
    for p in dirs:
        rel=p.relative_to(ROOT).as_posix();parts=rel.split('/')
        role=roles[parts[0]];reason='职责范围与理论主文件分离';risk='目录齐备不代表工作完成'
        owner=parts[0]
        if parts[0] in unregistered:
            reason='该顶层目录不在 00_项目治理/layout.json 的 sections 中'
            risk='未登记顶层目录：需确认应补登治理文件，还是误建于 openuft 根'
        if parts[0]=='01_独立体系' and len(parts)>1:
            if parts[1] not in titles:raise ValueError('Unknown system '+rel)
            owner=parts[1];role=titles[owner];reason='该体系拥有独立身份、证据及发布位置';risk='与相关体系可有谱系关系，不能自动继承证据'
            if len(parts)>2:
                if parts[2] not in stage_names:raise ValueError('Unknown stage '+rel)
                role += ' / '+stage_names[parts[2]];reason='以本体系为作用域保留此生命周期职责'
                if len(parts)>3:role += ' / '+subroles.get(parts[3],parts[3]);reason='本体系内的专题或资料分组，避免流入公共总筐'
                if parts[2]=='90_历史归档':risk='体系历史保留原始表述，不表示科学认可'
                if kinds.get(owner)=='unformulated_direction':risk='待建模方向，尚无具体公设，不计为已建立理论'
        elif parts[0]=='90_历史归档':reason='保留历史分析和逐字节快照';risk='旧布局说明与工具不得作为当前约定'
        elif parts[:2]==['02_共享基础','公共计算']:risk='仅共同常数和经典演示；候选理论实现归各体系'
        elif parts[:2]==['03_跨体系研究','跨体系原著']:reason='跨体系原著只有一份主文件，独立章节可溯源';risk='摘录是派生产物，不是互相独立的原始证据'
        elif parts[0]=='99_待整理资料':risk='需审理归属与负责人，不能堆积为新的总筐'
        records.append({'path':rel,'owner':owner,'direct_files':direct[p],'recursive_files':recursive[p],'role':role,'reason':reason,'risk':risk})
    directions=sum(s['kind']=='unformulated_direction' for s in registry)
    payload={'directory_count':len(records),'file_count':len(files),'system_containers':len(registry),'research_modules':len(registry)-directions,'unformulated_directions':directions,'records':records}
    (OUT/'directory_audit.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    text='# 独立体系布局：全部目录审计\n\n[设计与最优性分析](../目录设计/INDEPENDENT_SYSTEMS_DESIGN.md) · [类型与扩展](../目录设计/SCALABILITY_REVIEW.md) · [机器清单](directory_audit.json)。\n\n当前扫描 {} 个实际目录、{} 个**git 已跟踪**文件（未跟踪与 .gitignore 忽略的内容如 __pycache__/ 不计入——本表每条记录都指回真实目录链接，计入未被 git 收录的目录会让发布流程在干净副本里读到断链）；{} 个研究模块与 {} 个待建模方向独立管理，另有模板。类型不证明科学状态或来源有效性。历史目录也逐项列出；不展开 ZIP。递归文件数不可相加作为总数。目录职责由路径规则判定，不表示逐篇科学审定。\n\n| 目录 | 主归属 | 直接/递归文件 | 职责 | 设置理由 | 边界 |\n|---|---|---:|---|---|---|\n'.format(len(records),len(files),len(registry)-directions,directions)
    for r in records:
        target=os.path.relpath(ROOT/r['path'],OUT).replace('\\','/')
        text+='| [{}]({}/) | {} | {}/{} | {} | {} | {} |\n'.format(r['path'],target,r['owner'],r['direct_files'],r['recursive_files'],r['role'],r['reason'],r['risk'])
    (OUT/'DIRECTORY_AUDIT.md').write_text(text,encoding='utf-8')
    print('Audited {} directories; {} independent containers'.format(len(records),len(registry)))
    if unregistered:
        print('WARNING 未登记顶层目录 {} 个：{}'.format(len(unregistered), '、'.join(sorted(unregistered))),
              file=sys.stderr)

if __name__=='__main__':main()
