# -*- coding: utf-8 -*-
"""Enumerate every actual directory and attach an explicit design rule."""
from pathlib import Path
import csv
import json
import os

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '00_项目治理'

# role, retention rationale, boundary/risk, judgement
STAGES = {
    '00_研究立项': ('立项计划与决策', '问题、范围和退出条件需要稳定入口', '计划不得作为结果；负责人和里程碑需要实际填写', '保留'),
    '01_文献来源': ('模型文献与基准', '区分借用知识与本模型新主张', '共同书目引用共享层，不复制多份主记录', '保留'),
    '02_基础公设': ('本体与公设', '后续结论须有显式前提', '模型名称不能代替公设、版本与适用域', '保留；内容待完善'),
    '03_数学形式': ('数学形式与定义', '统一符号、单位和边界约定', '定义与物理假设分别标记', '保留'),
    '04_理论推导': ('方程推导', '保存从前提到方程的演算链', '推导成功不等于理论一致或观测成立', '保留'),
    '05_一致性检查': ('条件性证明与一致性', '分别审查守恒、稳定性、已知极限等', '数值例子不替代一般证明', '保留'),
    '06_可检验预测': ('可测量预测', '先规定可区分量和检验标准', '拟合已有数据与独立预测不得混淆', '保留'),
    '07_计算复现': ('计算实现与复现', '统一管理代码、配置、测试和执行', '输出结论需链接验证层；模板不等于可运行环境', '保留'),
    '08_研究数据': ('数据来源与处理链', '数据身份独立于代码与论文', '只读是约定，尚未由权限强制', '保留'),
    '09_验证结果': ('实现验证与观测检验', '对照预测、数据和基准', '应标注检验类型，不能把内部恒等式当外部验证', '保留'),
    '10_误差与不确定性': ('误差预算与稳健性', '有效数字不能代替不确定度', '必须进入预测和检验设计，不只用于论文末尾', '保留'),
    '11_证伪与反例': ('反例与负结果', '失败记录需要不受最终叙述影响的位置', '链接同一主结果，避免复制不利数据', '保留'),
    '12_研究结论': ('证据约束下的结论', '把数学、数值、观测与未验证主张分开', '必须追溯公设与证据版本', '保留'),
    '13_论文与成果': ('模型论文材料', '叙述、图表和补充材料有出版职责', '跨模型综述放公共出版层', '保留'),
    '14_独立评审': ('评审与独立复现', '保存意见、回复和独立检查过程', '自评不等于外部认可；允许贯穿所有阶段', '保留'),
    '15_版本发布': ('冻结版本与发布清单', '引用和复现需要确定版本', '发布不自动代表同行评审通过', '保留'),
    '90_历史归档': ('模型内历史', '保留替代关系与停止原因', '模型稳定入口不删除；跨模型历史进入根归档', '保留'),
}
SUB = {
    '07_计算复现/源码': ('模型专属源码', '主实现集中，避免阶段间重复算法', '历史阶段入口可以保留，但依赖要显式', '保留'),
    '07_计算复现/交互笔记': ('交互探索', '保留研究过程及演示', '正式结果须能从干净状态顺序复算', '按工作量使用'),
    '07_计算复现/配置': ('参数与算法配置', '输入与输出分离有利于复现', '记录单位、版本及默认值', '保留'),
    '07_计算复现/测试': ('自动断言与回归', '实现正确性需要独立检查入口', '测试通过不代表理论正确', '保留；当前多为模板'),
    '07_计算复现/运行记录': ('逐次运行记录', '执行命令、环境及失败状态可追踪', 'run_template.json 不是已完成运行', '保留'),
    '08_研究数据/原始数据': ('原始数据主副本', '保留输入原貌', '不要与 external 重复保管同一主副本', '保留'),
    '08_研究数据/处理后数据': ('派生数据', '处理过程与原件分离', '须链接输入 data_id 和生成 run_id', '保留'),
    '08_研究数据/外部数据': ('外部来源与获取元数据', '明确来源、许可、版本及获取方式', '若存原件必须确定唯一主位置，避免与 raw 冲突', '边界需执行约束'),
    '13_论文与成果/论文正文': ('正文与参考文献', '面向出版读者组织叙述', '结论证据仍保留在研究阶段', '保留'),
    '13_论文与成果/图表': ('图表与生成来源', '出版图可追踪到运行', '不要手工复制后失去版本关系', '保留'),
    '13_论文与成果/补充材料': ('补充材料', '提供读者所需复现说明', '不复制完整数据仓库', '保留'),
}
TOP = {
    '.github': ('协作平台配置', '平台固定路径要求', '不属于理论模块；现有模板不意味着有 CI', '保留'),
    '.github/ISSUE_TEMPLATE': ('问题反馈模板', '规范外部输入', '不能取代正式证据登记', '保留'),
    '00_项目治理': ('全局治理', '规则与研究内容职责分离', '避免将治理文档当科学认证', '保留'),
    '00_项目治理/资料索引': ('生成索引与历史总表', '提供全局查找视图', '目录索引不构成理论归属审查', '保留'),
    '00_项目治理/维护工具': ('目录维护工具', '生成视图可重复更新', '应有覆盖检查，不能静默遗漏新目录', '保留'),
    '01_models': ('研究路线主轴', '优先按前提追踪论证', '六路线并不互斥或穷尽', '保留'),
    '02_共享基础': ('共享研究资产', '复用时保留单一主位置', '共享不等于不含假设', '保留'),
    '02_共享基础/公共计算': ('共享计算工具', 'H01/H04 已有共同依赖', '缺少完整环境发布契约', '保留并补工程约束'),
    '02_共享基础/公共计算/源码': ('共享源码根', '为 Python 包提供一致导入根', '当前靠入口定位；将来可评估正式打包', '保留'),
    '02_共享基础/公共计算/源码/三重奏统一场': ('历史复算实现', '多个入口调用同一实现', '历史 STRICT/VERIFIED 标签未获本次科学认证', '保留并审查假设'),
    '02_共享基础/研究规范': ('共同研究方法', '方法约定集中维护', '旧阶段名及历史证据分层需统一解释', '保留；需语义修订'),
    '02_共享基础/研究规范/审计方法': ('历史审计方法材料', '保留误差与开放问题的已有来源', '方法文档含历史主张，不自动成为中立协议', '有条件保留'),
    '02_共享基础/参考资料': ('数学、文献与术语', '统一公共背景与引用入口', '原始来源与内部总结应明确区分', '保留'),
    '03_跨体系研究': ('跨模型分析', '比较结论的范围超过单模型', '必须冻结前提、数据与评价准则', '保留'),
    '03_跨体系研究/比较方案': ('比较方案与结果', '研究公平对照关系', '总登记表在父层，具体报告放此', '保留'),
    '03_跨体系研究/物理领域': ('按物理领域的次级视图', '统一候选涉及多个物理主题', '用链接组织，不再复制模型主文件', '保留为视图'),
    '03_跨体系研究/综合研究': ('综合候选', '组合前提须显式讨论兼容性', '不能将各路线结论直接相加', '保留'),
    '03_跨体系研究/应用研究': ('应用可行性探索', '为公共应用方向提供入口', '与比较不是同一职责；增长后再考虑独立', '暂保留的折中'),
    '04_公共成果': ('跨模型传播', '综合叙述没有唯一单模型归属', '明确区分历史报告、草稿和正式出版', '保留'),
    '04_公共成果/历史综合报告': ('历史综合报告', '暂不拆散未审查的理论系列', '放在出版层不代表已发表或已验证', '暂保留；归属待审'),
    '04_公共成果/可视化': ('公共可视化', '支持跨模型解释', '模型专属图回到模型论文层', '保留'),
    '90_历史归档': ('跨项目历史与迁移证据', '保证演变可追溯', '不参加当前研究成熟度判断', '保留'),
    '90_历史归档/历史资料': ('历史研究系列', '保留原有版本关系', '历史标题和结论待审', '保留'),
    '90_历史归档/历史工具': ('废弃工具', '保存旧操作逻辑供追溯', '不得作为当前运行入口', '保留只供查阅'),
    '90_历史归档/迁移记录': ('迁移记录集合', '结构变更需要恢复依据', '不要把当前活跃研究放入这里', '保留'),
    '90_历史归档/迁移记录/20260907_完整布局': ('本次迁移快照与映射', '恢复 193 个迁移前文件字节', '只代表该时间点；脚本不是可随时重跑的入口', '保留'),
    '99_待整理资料': ('待审资料与研究问题', '未知归属无需猜测', '缺少负责人、期限和处置监测', '保留并补管理'),
}
SPECIAL = {
    'D5_大统一力方程': '保留 H01 的既有力方程推导与复算入口',
    'D0_作用量变分求导': '保留 H04 的既有作用量推导与复算入口',
    'P1_螺旋三重奏_TS1': '保留三重奏命题相关历史论证',
    'P3_归纳闭合_R9': '保留归纳闭合的条件与证明过程',
    'P4_绝热三重奏_R10': '保留绝热与特殊极限研究',
    'P5_梯度磁场精确性_R11': '保留梯度磁场命题专题入口',
    'P6_谱理论框架_R7R8': '保留谱理论专题证明资料',
    'V2_mpmath高精度': '保留多精度数值复算入口',
}
AUDITS = {
    'A1_误差预算': '误差预算历史资料；数值精度与模型误差必须区分',
    'A4_诚实声明与开放问题': '开放问题历史清单；结论需链接模型当前版本',
    'A5_证据分层标注': '历史层级体系；需与当前证据类型建立明确映射',
    'A6_AI科技星认证': '历史自评记录；目录名称不证明外部认证',
}
REPORTS = {'求导证明v3', '全维修订版v2', '终极报告系列', '综述修订'}
LEGACY = {'GAQ_UFT_v1_几何原子', 'GAQ_UFT_v3_三大新体系', 'GAQ_UFT_v4_全维统一', 'GAQ_UFT_v5_cħ几何化', 'GAQ_UFT_v6_质量谱', '20260907前目录'}
INBOX = {'暗能量本质', '暗物质直接探测', '大统一完成', '黑洞信息悖论', '强相互作用精确化', '人工场实验验证', '弯曲时空三重奏', '弦论_LQG统一', '引力非重整化突破', 'CMB_B模观测'}

def classify(rel, models):
    if rel in TOP: return TOP[rel]
    parts = rel.split('/')
    if parts[0] == '01_models' and len(parts) >= 2 and parts[1] in models + ['新体系模板']:
        if len(parts) == 2:
            if parts[1] == '新体系模板': return ('新增路线模板', '保证新路线拥有同一职责集合', '模板不是第七条理论；空字段必须按实际填写', '保留')
            title = json.loads((ROOT / rel / 'model.json').read_text(encoding='utf-8'))['title']
            return (title + '路线容器', '同一前提下研究材料形成稳定主路径', '公设版本尚待完善；交叉关系见主文第 5 节', '保留；边界待科学定义')
        tail = '/'.join(parts[2:])
        if tail in STAGES: return STAGES[tail]
        if tail in SUB: return SUB[tail]
        if len(parts) == 4 and parts[3] in SPECIAL:
            return (SPECIAL[parts[3]], '沿用已有专题分组减少迁移破坏', '命名与历史证明标签未重新审定；不必推广为全部模型必建目录', '保留历史专题')
    if len(parts) == 4 and '/'.join(parts[:3]) == '02_共享基础/研究规范/审计方法' and parts[3] in AUDITS:
        return (AUDITS[parts[3]], '保留原有方法与审计资料的出处', '不能作为当前证据等级的自动认证', '有条件保留；需语义审查')
    if len(parts) == 3 and '/'.join(parts[:2]) == '04_公共成果/历史综合报告' and parts[2] in REPORTS:
        return (parts[2] + '历史作品系列', '保留系列版本与上下文', '理论归属、发表状态和科学结论均待审', '暂保留历史分组')
    if len(parts) == 3 and '/'.join(parts[:2]) == '90_历史归档/历史资料' and parts[2] in LEGACY:
        return (parts[2] + '历史版本', '保存既有研究或布局演变', '历史内容与旧链接不表示当前约定', '保留归档')
    if len(parts) == 2 and parts[0] == '99_待整理资料' and parts[1] in INBOX:
        return (parts[1] + '待研究问题', '为未立项主题保留入口', '标题不代表成果；须指定模型归属、负责人和处置日期', '暂保留；待审理')
    raise ValueError('Unclassified directory: ' + rel)

def main():
    layout = json.loads((OUT / 'layout.json').read_text(encoding='utf-8'))
    dirs = sorted(p for p in ROOT.rglob('*') if p.is_dir())
    files = [p for p in ROOT.rglob('*') if p.is_file()]
    records = []
    for p in dirs:
        rel = p.relative_to(ROOT).as_posix()
        role, rationale, boundary, decision = classify(rel, layout['models'])
        descendants = [f for f in files if p in f.parents]
        direct = [f for f in descendants if f.parent == p]
        records.append({'path': rel, 'direct_files': len(direct), 'recursive_files': len(descendants), 'role': role, 'rationale': rationale, 'boundary': boundary, 'decision': decision})
    model_stats = []
    for model in layout['models']:
        base = ROOT / '01_models' / model
        meta = json.loads((base / 'model.json').read_text(encoding='utf-8'))
        with (base / 'claims.csv').open(encoding='utf-8', newline='') as f:
            claims = list(csv.DictReader(f))
        with (base / '08_研究数据/data_registry.csv').open(encoding='utf-8', newline='') as f:
            data = list(csv.DictReader(f))
        model_stats.append({'id': model, 'postulates_count': len(meta['postulates']), 'hypothesis_revision': meta['hypothesis_revision'], 'claims_rows': len(claims), 'data_rows': len(data), 'python_files': len(list(base.rglob('*.py')))})
    readme_only = sum(1 for p in dirs if {f.name for f in files if p in f.parents} == {'README.md'})
    stats = {'directory_count_excluding_root': len(dirs), 'covered_directory_count': len(records), 'unclassified_count': 0, 'file_count': len(files), 'readme_only_subtrees': readme_only, 'note': 'README-only is a filename heuristic, not a claim that its prose is empty. Overlapping recursive counts must not be summed.', 'models': model_stats}
    (OUT / 'directory_audit.json').write_text(json.dumps({'date': '2026-09-07', 'statistics': stats, 'directories': records}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    body = '# 全部实际目录逐项分析\n\n生成日期：2026-09-07。[主论证与最优性评估](DIRECTORY_DESIGN_REVIEW.md) · [生成器](维护工具/audit_directories.py) · [机器可读清单](directory_audit.json)。\n\n'
    body += '## 实测范围\n\n扫描 openuft 下全部实际目录，包括 .github、模板、历史专题与迁移目录；不展开 ZIP 内部虚拟路径。根目录不计入目录数量，根文件职责见主文。\n\n'
    body += '- 实际目录：{}；已分析：{}；未归类：0。\n- 当前文件：{}。\n- 递归文件名集合仅为 README.md 的目录：{}；这是占位倾向指标，不代表正文无研究内容。\n\n'.format(len(dirs), len(records), len(files), readme_only)
    body += '目录的递归文件数包含子目录，不能逐行相加求总数。职责与边界由显式规则逐项匹配，不根据文件数量推断科学成熟度。\n\n'
    body += '## 模型登记现状\n\n| 模型 | 公设条数 | 公设版本 | 命题记录行 | 数据记录行 | 模型内 Python 文件 |\n|---|---:|---|---:|---:|---:|\n'
    for s in model_stats:
        body += '| {id} | {postulates_count} | {revision} | {claims_rows} | {data_rows} | {python_files} |\n'.format(revision=s['hypothesis_revision'] or '未填写', **s)
    body += '\n模型内 Python 文件数不包括共享引擎；零条登记不说明不存在散落正文，只说明尚未录入这些登记表。\n\n## 逐目录结论\n\n'
    group = None
    for row in records:
        current = row['path'].split('/')[0]
        if current != group:
            body += '\n### ' + current + '\n\n| 目录 | 直接/递归文件 | 职责 | 保留理由 | 边界与风险 | 判断 |\n|---|---:|---|---|---|---|\n'
            group = current
        target = os.path.relpath(ROOT / row['path'], OUT).replace('\\', '/')
        body += '| [{}]({}/) | {}/{} | {} | {} | {} | {} |\n'.format(row['path'], target, row['direct_files'], row['recursive_files'], row['role'], row['rationale'], row['boundary'], row['decision'])
    (OUT / 'DIRECTORY_AUDIT.md').write_text(body, encoding='utf-8')
    print(json.dumps(stats, ensure_ascii=True))

if __name__ == '__main__':
    main()
