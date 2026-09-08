"""Build hypothesis-led navigation without relocating original research files."""
from pathlib import Path
import hashlib
import json
import os
import re

ROOT = Path(__file__).resolve().parent
ROUTES = [
    ('历史路线01_空间运动', '空间运行与螺旋运动', '空间运动、速度场或螺旋结构是否能够产生可观测的场？', ['螺旋', '三重奏', 'frenet', '三重奏研究']),
    ('h02_space_compression', '空间压缩与密度梯度', '空间压缩量如何定义、测量，并与质量、引力及场方程联系？', ['空间压缩', '空间密度', '压缩空间']),
    ('h03_matter_driven', '物体驱动与源场耦合', '物体运动及源分布如何驱动场，场又如何反作用于物体？', ['物体驱动', '物体运动', '大统一力方程']),
    ('历史路线04_几何作用量', '几何与作用量', '给定几何结构与作用量，能否一致导出动力学和已知极限？', ['作用量', '变分', '几何化', 'derivation']),
    ('h05_gauge_symmetry', '规范对称与相互作用', '规范群、对称破缺及耦合能否形成一致的统一描述？', ['规范', '电弱', '强力', '核力', 'su3', 'su2']),
    ('h06_quantum_emergence', '量子结构与涌现', '量子自由度或微观结构如何产生时空及有效相互作用？', ['量子', '自旋', '质量谱', '黑洞熵']),
]
STAGES = [
    ('00_assumptions', '假设与边界', '列出原始假设、可替代假设、适用尺度和明确排除的情况。假设不能作为验证结果。'),
    ('01_definitions', '数学定义与量纲', '定义变量、单位、场的类型、坐标约定、可观测量，以及源项和边界条件。'),
    ('02_derivations', '方程推导', '逐步给出输入、使用的假设、变换和输出；标注额外假设与已知理论输入，避免循环推导。'),
    ('03_proofs', '数学证明与一致性', '记录命题、前提和证明；检查守恒、对称性、稳定性、因果性及适用极限。数值样本不替代一般证明。'),
    ('04_predictions', '可区分预测', '输出可测量量、参数依赖、误差范围，以及与基准理论不同的预测。'),
    ('05_verification', '复现与实验对照', '登记代码版本、命令、依赖、数据来源、拟合参数与独立检验数据；区分符号检查、数值检查和实验检验。'),
    ('06_falsification', '反例与证伪', '先列失效阈值，再记录反例、失败运行、替代解释及适用范围收缩。不得隐藏负结果。'),
    ('07_conclusions', '结论与未解问题', '分别记录已证明命题、证据支持、未验证猜想、被反驳结论和下一步；链接证据编号。'),
]

def write(rel, body):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.rstrip() + '\n', encoding='utf-8')

def link(source, target):
    return os.path.relpath(ROOT / target, (ROOT / source).parent).replace('\\', '/')

def main():
    manifest = ROOT / '00_index/structure_manifest.json'
    if manifest.exists():
        originals = json.loads(manifest.read_text(encoding='utf-8'))['original_files']
    else:
        originals = []
        for p in sorted(ROOT.rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts and p.name != Path(__file__).name:
                originals.append({'path': p.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()})
        for name in ['README.md', 'INDEX.md', 'WORKFLOW.md', 'QUICKSTART.md', 'MIGRATION_GUIDE.md']:
            backup = ROOT / '95_history_archive/20260907前目录' / name
            backup.parent.mkdir(parents=True, exist_ok=True)
            backup.write_bytes((ROOT / name).read_bytes())
    records = []
    for item in originals:
        p = ROOT / item['path']
        content = p.read_text(encoding='utf-8', errors='replace') if p.suffix in ['.md', '.py', '.txt'] else ''
        haystack = (item['path'] + '\n' + content).lower()
        tags = [rid for rid, _, _, keywords in ROUTES if any(k.lower() in haystack for k in keywords)]
        records.append(dict(item, routes=tags, classification='关键词候选关联，非理论归属或证据认证'))
    write('00_index/structure_manifest.json', json.dumps({'classification_policy': '原文件全量登记；关键词仅生成多标签候选索引，须人工核对论证前提。', 'original_files': originals, 'records': records}, ensure_ascii=False, indent=2))
    for rid, title, question, _ in ROUTES:
        base = '01_hypotheses/' + rid
        body = '# ' + rid.upper() + ' · ' + title + '\n\n研究问题：' + question + '\n\n状态：待建模／待审查。下列历史关联材料尚未逐项核实，不能据此宣布该路线成立。\n\n'
        body += '\n'.join('- [{}：{}]({}/README.md)'.format(i, title2, stage) for i, (stage, title2, _) in enumerate(STAGES))
        body += '\n\n[候选资料索引](sources.md) · [跨体系比较](../../02_comparison/README.md) · [研究记录模板](../../03_research_protocol/claim_template.md)'
        write(base + '/README.md', body)
        for stage, title2, instruction in STAGES:
            write(base + '/' + stage + '/README.md', '# ' + title2 + '\n\n所属路线：[' + title + '](../README.md)\n\n' + instruction + '\n\n当前内容：待补充。使用[研究记录模板](../../../03_research_protocol/claim_template.md)，为每个研究问题创建独立记录并链接上下游。')
        source = base + '/sources.md'
        selected = [r for r in records if rid in r['routes']]
        write(source, '# 候选资料 · ' + title + '\n\n按名称与正文关键词关联；可能存在误匹配，跨路线引用不代表假设兼容。原文件保持原路径。\n\n' + ('\n'.join('- [{}]({})'.format(r['path'], link(source, r['path'])) for r in selected) if selected else '尚未找到关键词匹配的既有材料，需要独立建模。'))
    write('01_hypotheses/README.md', '# 理论假设与独立研究路线\n\n以不同假设为主轴，逐条完成“假设 → 定义 → 推导 → 证明 → 预测 → 检验 → 证伪 → 结论”。各路线允许竞争、交叉和淘汰，不预设最终统一场论已成立。\n\n' + '\n'.join('- [{}：{}]({}/README.md) — {}'.format(rid.upper(), title, rid, q) for rid, title, q, _ in ROUTES) + '\n\n新体系使用稳定的 h07、h08 等编号与相同八阶段结构；先登记假设差异，再引用共享材料。')
    matrix = '# 跨体系比较与统一候选筛选\n\n只有在定义、前提和适用范围兼容时，才可合并推导。路线相似、曲线拟合或公式外观一致不构成统一证明。\n\n| 路线 | 原始假设 | 动力学闭合 | 已知极限 | 独特预测 | 独立实验 | 反例 | 当前判定 |\n|---|---|---|---|---|---|---|---|\n'
    matrix += '\n'.join('| [{}](../01_hypotheses/{}/README.md) | 待明确 | 待检验 | 待检验 | 待提出 | 待提供 | 待搜索 | 待审查 |'.format(t, r) for r, t, _, _ in ROUTES)
    matrix += '\n\n比较维度：本体与自由度、量纲、对称性、源场反馈、守恒律、稳定性、因果性、相对论极限、量子极限、四种相互作用、参数可识别性、误差与复现成本。每个单元格的更新必须引用研究记录。\n\n## 合并与淘汰规则\n\n1. 同一现象使用相同数据、单位、边界条件与误差模型比较。\n2. 分清用于拟合的数据与用于检验的数据，记录自由参数数目。\n3. 遇到冲突保留冲突记录，不能从互不兼容前提拼接方程。\n4. 被反例否定的路线保留失败原因、适用范围和历史版本。\n5. 综合候选必须给出共同假设、完整推导链、跨领域检验与未解决缺口。\n\n[统一候选登记](../04_synthesis/README.md)'
    write('02_comparison/README.md', matrix)
    write('03_research_protocol/claim_template.md', '# 研究记录模板\n\n- 编号：Hxx-Cxxx\n- 标题与版本：\n- 路线与阶段：\n- 状态：假设／已形式化／条件性证明／数值支持／实验支持／被反驳／未决\n- 问题与适用范围：\n- 前提及上游记录编号：\n- 变量、单位、源项与边界条件：\n- 推导或证明步骤：\n- 已知理论输入与独立导出的内容：\n- 可测预测与基准理论差异：\n- 代码、版本、依赖、复现命令及随机种子：\n- 数据来源、版本、拟合与独立检验划分：\n- 不确定度、参数数目与证伪阈值：\n- 正结果、负结果与反例：\n- 结论及证据链接：\n- 下游预测／检验／结论编号：\n- 未解问题与下一步：')
    write('03_research_protocol/README.md', '# 全链路研究规则\n\n每项结论通过稳定编号关联假设、推导、预测、代码、数据、结果和反例。先使用[记录模板](claim_template.md)，再将关联结论登记到[比较表](../02_comparison/README.md)。\n\n数学证明只证明前提下的命题；符号或数值检查须明确覆盖范围；实验支持须提供可追溯数据与误差分析。历史材料中的“严格证明”“终极”“认证”等标签保留为原文表述，不自动转为新的证据状态。\n\n共享方法继续使用 10/20/30/40 目录，源代码放 70_source_code，领域对照放 50_physics_domains。路线内写假设特有内容并链接共享材料，避免多份真源。')
    write('04_synthesis/README.md', '# 综合与统一候选\n\n当前未在本次目录整理中确立任何统一场论。\n\n候选登记应包含：候选编号、兼容的路线及版本、共同假设、冲突处理、作用量或闭合动力学、已知理论极限、四种相互作用覆盖、独立预测、实验与误差证据、未解决问题、淘汰条件。\n\n仅在[跨体系比较](../02_comparison/README.md)中建立证据链后更新结论；论文标题与数值精度不能代替物理验证。')
    catalog = '# 既有资料全量分类索引\n\n全部原文件按原目录登记；理论标签为关键词候选关联，未匹配项明确保留“待归属”。源文件不移动、不删除。\n\n| 文件 | 原分类 | 候选路线 |\n|---|---|---|\n'
    for r in records:
        catalog += '| [{}]({}) | {} | {} |\n'.format(r['path'], link('00_index/material_catalog.md', r['path']), r['path'].split('/')[0], ', '.join(r['routes']) or '共享／待归属')
    write('00_index/material_catalog.md', catalog)
    rootbody = '# openuft · 多假设统一场论研究\n\n通过不同理论体系分别建模、推导、分析和检验，比较其适用范围与冲突，逐步筛选统一场论候选。研究目标不等于已达成结论。\n\n作者：AI科技星 · 研究组织：AI科技星\n\n## 主目录\n\n| 目录 | 职责 |\n|---|---|\n'
    dirs = [('00_index', '全量资料索引与历史导航'), ('01_hypotheses', '核心入口：空间运行、空间压缩、物体驱动等独立体系'), ('02_comparison', '跨体系比较、冲突、反例与筛选'), ('03_research_protocol', '证据分级与全链路记录模板'), ('04_synthesis', '综合结论与统一候选'), ('10_D_求导_derivation', '共享推导方法'), ('20_P_证明_proof', '共享数学证明材料'), ('30_V_验证_verification', '共享验证材料'), ('40_A_精算_audit', '误差、证伪与审计'), ('50_physics_domains', '跨物理领域对照'), ('60_application', '应用探索'), ('70_source_code', '代码与复现工具'), ('80_visualization', '可视化'), ('90_paper_论文', '论文与报告'), ('95_history_archive', '历史版本'), ('99_inbox_future', '待研究问题'), ('docs', '共享数学与文献资料')]
    rootbody += '\n'.join('| [{}]({}/README.md) | {} |'.format(d, d, purpose) for d, purpose in dirs)
    rootbody += '\n\n## 阅读顺序\n\n1. 在 [理论路线](01_hypotheses/README.md) 选择体系，阅读八阶段目录及候选资料。\n2. 按 [研究协议](03_research_protocol/README.md) 建立可追溯记录。\n3. 在 [比较矩阵](02_comparison/README.md) 对照预测与证据。\n4. 在 [综合区](04_synthesis/README.md) 登记候选、冲突和缺口。\n\n既有文件通过[全量分类索引](00_index/material_catalog.md)访问；[迁移说明](MIGRATION_GUIDE.md)记录本次布局调整。历史文档内的成熟度数字与已证标签未在本次整理中重新验证。'
    write('README.md', rootbody)
    write('INDEX.md', '# openuft 导航\n\n[总体布局](README.md) · [理论路线](01_hypotheses/README.md) · [全量资料](00_index/material_catalog.md) · [比较矩阵](02_comparison/README.md) · [研究协议](03_research_protocol/README.md) · [统一候选](04_synthesis/README.md)')
    write('QUICKSTART.md', '# 快速开始\n\n1. 打开[理论路线](01_hypotheses/README.md)，选择一个可检验问题。\n2. 阅读该路线 sources.md，核对原文前提。\n3. 复制[记录模板](03_research_protocol/claim_template.md)到对应阶段，补全上游编号与边界条件。\n4. 完成推导、预测和独立检验后更新[比较表](02_comparison/README.md)。\n\n目录检查：在 openuft 目录运行 `python reorganize_structure.py --check`。此命令检查资料保全与新增导航链接，不验证物理理论。')
    write('WORKFLOW.md', '# 研究工作流\n\n选定路线 → 明确假设 → 数学定义 → 方程推导 → 条件性证明 → 可区分预测 → 数值及实验检验 → 反例审计 → 路线结论 → 跨体系比较 → 综合候选。\n\n每一阶段均使用[研究记录模板](03_research_protocol/claim_template.md)，保留失败结果与上下游编号。没有实验数据时明确标为待验证，不能跳过检验升级为物理结论。\n\n[研究路线入口](01_hypotheses/README.md) · [完整研究协议](03_research_protocol/README.md)')
    write('MIGRATION_GUIDE.md', '# 布局调整 · 2026-09-07\n\n新增 01_hypotheses 至 04_synthesis，以不同假设为主轴，旧方法目录作为共享资料层。所有原有资料保持原路径；本次重写的五份入口文档原文保存在 [旧布局归档](95_history_archive/20260907前目录/README.md)。\n\n新增六条独立路线，每条具备八阶段目录与候选资料索引。空间压缩等缺少明确材料的路线标记待建模，不编造推导结果。关键词匹配仅帮助查找，允许多标签，并保留未匹配材料。\n\n[全量资料清单](00_index/material_catalog.md)与[原始文件校验记录](00_index/structure_manifest.json)用于追溯。旧报告中的链接和成熟度表述属于历史材料，未做全库修订。重新生成导航：`python reorganize_structure.py`；只读检查：`python reorganize_structure.py --check`。')

def check():
    data = json.loads((ROOT / '00_index/structure_manifest.json').read_text(encoding='utf-8'))
    replaced = {'README.md', 'INDEX.md', 'WORKFLOW.md', 'QUICKSTART.md', 'MIGRATION_GUIDE.md'}
    errors = []
    for r in data['original_files']:
        p = ROOT / ('95_history_archive/20260907前目录/' + r['path'] if r['path'] in replaced else r['path'])
        if not p.exists():
            errors.append('Missing original: ' + r['path'])
        elif hashlib.sha256(p.read_bytes()).hexdigest() != r['sha256']:
            errors.append('Changed original: ' + r['path'])
    pages = [ROOT / x for x in replaced] + [ROOT / '00_index/material_catalog.md']
    for d in ['01_hypotheses', '02_comparison', '03_research_protocol', '04_synthesis']:
        pages.extend((ROOT / d).rglob('*.md'))
    for p in pages:
        for target in re.findall(r'\]\(([^)]+)\)', p.read_text(encoding='utf-8')):
            if '://' not in target and not (p.parent / target.split('#')[0]).exists():
                errors.append('Broken link: ' + str(p) + ' -> ' + target)
    for rid, _, _, _ in ROUTES:
        for stage, _, _ in STAGES:
            if not (ROOT / '01_hypotheses' / rid / stage / 'README.md').exists():
                errors.append('Missing stage: ' + rid + '/' + stage)
    if errors:
        raise SystemExit('\n'.join(errors))
    print('PASS: {} original files preserved; {} navigation pages checked; 6 routes x 8 stages.'.format(len(data['original_files']), len(pages)))

if __name__ == '__main__':
    import sys
    if '--check' not in sys.argv:
        main()
    check()
