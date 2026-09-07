# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib
import json
import os
import re
import zipfile

ROOT = Path(__file__).resolve().parent / 'openuft'
assert ROOT.resolve() == Path(r'D:\a10\aikjx\code\my_lib\openuft').resolve()
routes = [('h01_space_motion','空间运行与螺旋运动'),('h02_space_compression','空间压缩与密度梯度'),('h03_matter_driven','物体驱动与源场耦合'),('h04_geometry_action','几何与作用量'),('h05_gauge_symmetry','规范对称与相互作用'),('h06_quantum_emergence','量子结构与涌现')]
stages = [
('00_project','立项与研究计划','研究问题、负责人、范围、里程碑、风险、停止条件和决策日志。'),
('01_literature','文献与基准理论','记录作者、年份、DOI/URL、页码和适用范围；区分原始文献与二手解释。'),
('02_assumptions','宇宙模型与假设','明确本体、自由度、时空观、因果结构、原始公设、尺度和可替代假设。'),
('03_formalism','数学形式与定义','符号、单位、度规号差、场空间、作用量、源项、边界条件与初值。'),
('04_derivations','方程推导','逐步列出输入公设、使用的定理、额外近似和输出方程，禁止循环论证。'),
('05_consistency','证明与理论一致性','检验量纲、对称性、守恒、良定性、稳定性、因果性及已知极限；量子模型另查幺正性与反常。数值例子不替代一般证明。'),
('06_predictions','可检验预测','给出可观测量、参数、适用尺度、误差和相对基准的差异；预先确定检验标准。'),
('07_computation','计算与复现','源码、环境、配置、随机种子、测试、运行清单和输出；每次运行使用独立 run_id。'),
('08_data','数据与溯源','原始数据只读保留；登记来源、许可、单位、校准、选择效应、处理步骤和校验和。'),
('09_validation','数值验证与观测检验','区分实现正确性、数值收敛和独立观测检验；隔离拟合与检验数据，报告基准及残差。'),
('10_uncertainty','不确定度与稳健性','分别记录统计、系统、离散化和模型误差；保留协方差、敏感性、参数可辨识性和多重比较处理。'),
('11_falsification','反例与证伪','记录预设阈值、负结果、失效范围、替代解释；失败记录不得因结果不利而删除。'),
('12_conclusions','结论与开放问题','将数学结论、数值证据、观测支持、未验证主张和被反驳主张分开，逐条链接证据。'),
('13_publications','论文与传播','正文、参考文献、图表源文件、补充材料和投稿版本；图表追溯到数据与运行。'),
('14_review','评审与独立复现','自查、同行意见、逐条回复、独立复现记录和利益冲突；自评不是外部认证。'),
('15_releases','发布与长期保存','发布清单、版本、代码提交、环境、数据标识、许可、引用元数据、校验和与勘误。'),
('90_archive','历史与终止路线','保留旧版本、终止原因及替代版本链接；归档不表示研究结论得到认可。')]
stage_map = dict(zip(['00_assumptions','01_definitions','02_derivations','03_proofs','04_predictions','05_verification','06_audit','07_falsification','08_conclusions'], ['02_assumptions','03_formalism','04_derivations','05_consistency','06_predictions','09_validation','10_uncertainty','11_falsification','12_conclusions']))
prefixes = {'00_index':'00_governance/catalog','01_hypotheses':'01_models','02_comparison':'03_comparative/comparison','03_research_protocol':'02_shared/protocols','04_synthesis':'03_comparative/synthesis','50_physics_domains':'03_comparative/physics_domains','60_application':'03_comparative/applications','70_source_code':'02_shared/computation','80_visualization':'04_publications/visualizations','90_paper_论文':'04_publications/legacy_reports','95_history_archive':'90_archive/legacy','99_inbox_future':'99_inbox','docs':'02_shared/references'}
topdocs = ['CHANGELOG.md','CONTRIBUTING.md','FAQ.md','ROADMAP.md','WORKFLOW.md','MIGRATION_GUIDE.md']
def mapped(rel):
    parts = rel.split('/')
    if parts[0] in topdocs: return '00_governance/' + rel
    if rel in ['verify.py','reorganize_structure.py']: return '90_archive/legacy_tools/' + rel
    if parts[0] == '01_hypotheses' and len(parts)>2: parts[2] = stage_map.get(parts[2],parts[2])
    if parts[0] == '70_source_code' and len(parts)>1 and parts[1]=='triad_uft': parts.insert(1,'src')
    parts[0] = prefixes.get(parts[0],parts[0])
    return '/'.join(parts)
def write(rel,body):
    p=ROOT/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(body.rstrip()+'\n',encoding='utf-8')
def link(src,dst): return os.path.relpath(ROOT/dst,(ROOT/src).parent).replace('\\','/')
originals = sorted(p for p in ROOT.rglob('*') if p.is_file())
snapshot=ROOT/'90_archive/migrations/20260907_full_layout/before.zip'
if snapshot.exists(): raise SystemExit('Migration already applied; refusing to overwrite snapshot')
inventory=[{'old':p.relative_to(ROOT).as_posix(),'new':mapped(p.relative_to(ROOT).as_posix()),'sha256_before':hashlib.sha256(p.read_bytes()).hexdigest()} for p in originals]
snapshot.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(snapshot,'w',zipfile.ZIP_DEFLATED) as z:
    for p in originals: z.write(p,p.relative_to(ROOT).as_posix())
for row in inventory:
    src,dst=ROOT/row['old'],ROOT/row['new']
    assert src.resolve().is_relative_to(ROOT.resolve()) if hasattr(src.resolve(),'is_relative_to') else str(src.resolve()).startswith(str(ROOT.resolve())+os.sep)
    if src!=dst:
        if dst.exists(): raise RuntimeError('Collision: '+str(dst))
        dst.parent.mkdir(parents=True,exist_ok=True); src.rename(dst)
# Resolve obsolete method links left by the previous migration.
aliases={}
for row in inventory:
    old=row['old']; parts=old.split('/')
    if old.startswith('01_hypotheses/') and len(parts)>3:
        method={'02_derivations':'10_D_求导_derivation','03_proofs':'20_P_证明_proof','05_verification':'30_V_验证_verification'}.get(parts[2])
        if method and parts[3]!='README.md': aliases[method+'/'+ '/'.join(parts[3:])]=old
    if old.startswith('03_research_protocol/audit_methodology/'):
        aliases['40_A_精算_audit/'+old.split('audit_methodology/',1)[1]]=old
for method,kind in [('10_D_求导_derivation','D_求导'),('20_P_证明_proof','P_证明'),('30_V_验证_verification','V_验证')]: aliases[method+'/README.md']='03_research_protocol/method_'+kind+'.md'
aliases['40_A_精算_audit/README.md']='03_research_protocol/audit_methodology/README.md'
pattern=re.compile(r'(!?\[[^\]\n]*\]\()([^\s)]+)(\))')
for row in inventory:
    p=ROOT/row['new']
    if p.suffix!='.md' or row['new'].startswith('90_archive/'): continue
    body=p.read_text(encoding='utf-8-sig')
    def repl(m):
        target=m.group(2)
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target) or target.startswith('#'): return m.group(0)
        path,sep,frag=target.partition('#')
        from urllib.parse import unquote
        absold=Path(os.path.normpath(str((ROOT/row['old']).parent/unquote(path))))
        try: rel=absold.relative_to(ROOT).as_posix()
        except ValueError:
            dest=absold
        else: dest=ROOT/mapped(aliases.get(rel,rel))
        return m.group(1)+os.path.relpath(dest,p.parent).replace('\\','/')+(sep+frag if sep else '')+m.group(3)
    write(row['new'],pattern.sub(repl,body))
# Remove only verified-empty directories within the explicitly named workspace.
for p in sorted(ROOT.rglob('*'),key=lambda p:len(p.parts),reverse=True):
    if p.is_dir() and not any(p.iterdir()):
        assert str(p.resolve()).startswith(str(ROOT.resolve())+os.sep)
        p.rmdir()

sections={'00_governance':'项目治理、总索引、研究流程和迁移记录','01_models':'按宇宙认知与基础假设分开的六条研究路线','02_shared':'共享研究协议、数学文献和复现工具','03_comparative':'跨模型公平比较、物理领域检验和综合候选','04_publications':'跨模型综述、公共图表和待确认归属的历史报告','90_archive':'历史资料、旧工具及完整迁移快照','99_inbox':'尚未立项、归属待审的输入与问题'}
for d,desc in sections.items(): write(d+'/README.md','# '+d+'\n\n'+desc+'。\n\n[返回总入口](../README.md)')
model_index='# 理论大模块\n\n主分类轴是基础假设与宇宙模型。六条路线是研究容器，彼此可能交叉；不是互斥的完备物理学分类。未制定公设与可检验预测前，不能称为成立的理论。\n\n| 模块 | 研究方向 |\n|---|---|\n'
for rid,title in routes:
    model_index+='| '+rid+' | ['+title+']('+rid+'/README.md) |\n'
write('01_models/README.md',model_index+'\n新增路线从 [_template](_template/README.md) 复制；建立 model.json 后登记，不复制其他路线的结论作为证据。')
for rid,title in routes+[('_template','新假设路线模板')]:
    base='01_models/'+rid
    existing=(ROOT/base/'README.md').read_text(encoding='utf-8')
    write(base+'/model.json',json.dumps({'id':rid,'title':title,'status':'unreviewed' if rid!='_template' else 'template','owner':None,'hypothesis_revision':None,'ontology':None,'spacetime':None,'degrees_of_freedom':[],'postulates':[],'scope':None,'baseline_models':[],'cross_model_dependencies':[],'evidence_status':'未进行本次科学内容审查'},ensure_ascii=False,indent=2))
    intro=existing.split('## 全链路导航')[0].split('## 关键结论')[0]
    write(base+'/README.md','# '+title+' · '+rid+'\n\n'+intro.split('\n',1)[-1]+'\n\n本次仅完成研究组织与复现路径整理；历史正文的科学主张尚未重新审定。身份与假设边界见 [model.json](model.json)。\n\n| 目录 | 职责 |\n|---|---|\n'+'\n'.join('| ['+s+']('+s+'/README.md) | '+t+' |' for s,t,_ in stages)+'\n\n[资料关联](sources.md) · [证据登记](claims.csv) · [总流程](../../00_governance/WORKFLOW.md)')
    for s,t,desc in stages:
        path=ROOT/base/s/'README.md'
        old=path.read_text(encoding='utf-8') if path.exists() else ''
        write(base+'/'+s+'/README.md','# '+t+'\n\n所属模块：['+title+'](../README.md)\n\n'+desc+'\n\n当前阶段需依据实际产物审查，不因目录存在而视为完成。\n'+('\n## 既有阶段记录\n\n'+old if old else ''))
    write(base+'/claims.csv','claim_id,hypothesis_revision,statement,assumptions,derivation,prediction,run_id,data_id,uncertainty,evidence_level,status,reviewer')
    write(base+'/00_project/plan.md','# 研究计划\n\n- 负责人：待指定\n- 核心问题：待细化为可检验命题\n- 原始假设与竞争解释：见 model.json\n- 里程碑与退出条件：待制定\n- 最近决定 / 日期 / 理由 / 证据：待登记')
    for sub,desc in {'07_computation/src':'模型专属源码；跨模型复用库须显式声明依赖。','07_computation/notebooks':'探索笔记；稳定计算应提取为可运行脚本。','07_computation/configs':'参数配置与单位；禁止未记录的手动参数。','07_computation/tests':'实现、解析极限、收敛与回归检查。','07_computation/runs':'每个 run_id 独立保存命令、环境、种子、日志和输出；失败运行也保存。','08_data/raw':'来源原件，登记校验和后不覆盖。','08_data/processed':'派生数据，链接原始数据与变换脚本。','08_data/external':'第三方数据的来源、版本、授权及获取步骤。','13_publications/manuscript':'论文源文件与参考文献。','13_publications/figures':'图表源文件与生成命令。','13_publications/supplement':'补充推导、数据说明和复现材料。'}.items():
        write(base+'/'+sub+'/README.md','# '+sub.split('/')[-1]+'\n\n'+desc)
    write(base+'/08_data/data_registry.csv','data_id,source_url,version,retrieved_at,license,units,sha256,local_path,processing_run_id')
    write(base+'/07_computation/runs/run_template.json',json.dumps({'run_id':None,'model_id':rid,'claim_ids':[],'code_revision':None,'command':None,'environment':None,'parameters':{},'seed':None,'input_data_ids':[],'outputs':[],'exit_code':None,'started_at':None},ensure_ascii=False,indent=2))
    write(base+'/14_review/review_template.md','# 评审记录\n\n审查人 / 日期 / 版本：待填\n\n假设是否显式？推导有无隐含输入？已知极限是否恢复？预测是否独立于拟合数据？误差与负结果是否完整？复现命令是否成功？\n\n逐条意见、作者回复、证据位置、处置状态：待登记。')
    write(base+'/15_releases/release_template.md','# 发布清单\n\n版本 / 日期 / 审查状态 / 代码提交：待填\n\n公设版本、结论登记、数据来源、环境、运行清单、文件 SHA-256、许可与引用：待填。\n\n尚未解决的问题和勘误入口：待填。未经外部审查不得标注同行评审通过。')

write('README.md','# OpenUFT · 多模型统一场论研究\n\n以不同基础假设、宇宙认知与建模机制组织研究。目标是探索统一描述；目录规范和计算通过都不等于统一场论成立。本布局是适合本项目的研究约定，不声称存在唯一通用的物理学目录标准。\n\n## 大模块\n\n| 目录 | 用途 |\n|---|---|\n'+'\n'.join('| ['+d+']('+d+'/README.md) | '+desc+' |' for d,desc in sections.items())+'\n\n## 六条独立路线\n\n'+'\n'.join('- ['+title+'](01_models/'+rid+'/README.md)' for rid,title in routes)+'\n\n每条路线覆盖：立项 → 文献 → 假设 → 数学形式 → 推导 → 一致性 → 预测 → 计算与数据 → 验证 → 不确定度 → 证伪 → 结论 → 论文 → 评审 → 发布与归档。允许迭代返回前序阶段。\n\n[快速开始](QUICKSTART.md) · [全量文件索引](00_governance/catalog/material_catalog.md) · [研究流程](00_governance/WORKFLOW.md) · [迁移说明](00_governance/MIGRATION_GUIDE.md)\n\n结构检查：`python verify.py`。该命令只检查组织完整性，不判定科学正确性。')
write('INDEX.md','# 导航\n\n[大模块入口](README.md) · [理论路线](01_models/README.md) · [全部文件](00_governance/catalog/material_catalog.md)')
write('QUICKSTART.md','# 快速开始\n\n1. 在 [理论路线](01_models/README.md) 选择基础假设相符的模块。\n2. 完成 model.json 与 00_project/plan.md，登记假设版本。\n3. 在 claims.csv 建立命题编号，沿阶段目录链接推导、预测、数据和运行。\n4. 运行 `python verify.py` 检查结构。\n5. 复算共享历史引擎：从 openuft 进入 `02_shared/computation/src` 后运行 `python -m triad_uft.verify`。输出中的历史证据标签需另行审查。\n\n未知归属资料先进入 [99_inbox](99_inbox/README.md)。')
write('00_governance/WORKFLOW.md','# 物理研究全生命周期\n\n本文件是项目内部约定，不是国际标准认证。各阶段可迭代，允许“不适用”但必须写明理由，不要求每个阶段机械配备脚本。\n\n| 阶段 | 必备研究内容 |\n|---|---|\n'+'\n'.join('| '+s+' · '+t+' | '+desc+' |' for s,t,desc in stages)+'\n\n## 证据与阶段门\n\n- 立项门：问题、原始假设、模型边界与基准明确。\n- 理论门：定义与推导可追踪，一致性条件与失败项已记录。\n- 预测门：冻结预测、参数拟合范围和失效阈值后使用独立检验数据。\n- 复现门：记录代码提交、环境、命令、数据版本、种子和输出校验和；他人可复算。\n- 结论门：分别标记 conjecture、mathematical_result、numerical_check、observational_support、refuted；这些是证据类型，不是自动晋级分数。\n- 发布门：论文、图表、证据登记、审查记录与发布清单齐备。外部审查必须有真实记录。\n\n## 归属与命名\n\n每件资料只有一个主存放位置。按论证的原始假设归属；跨路线通过相对链接和 model.json 依赖登记关联。关键词命中只构成候选关联。理论路线可以重叠，混合模型须声明组合假设与版本，不能直接合并结论。\n\n目录使用稳定英文 snake_case；现有中文研究文件保留名称。命题建议 H01-C0001，数据 H01-D0001，运行采用日期和唯一后缀；登记后不复用编号。\n\n共享引擎含历史理论假设，不自动视为模型无关基准。历史认证、自评标签、拟合吻合与数值精度均不能替代独立实验。被证伪路线保留原稳定路径和负结果，记录状态与替代版本。')
write('02_shared/computation/README.md','# 共享计算工具\n\n现有源码位于 [src/triad_uft](src/triad_uft/)。H01 与 H04 的既有复算脚本依赖此库，因此保留一个共享实现。库中的理论假设与证据标签继承历史版本，未在目录迁移中科学审定。\n\n从本目录的 src 执行 `python -m triad_uft.verify`。各模型专属代码放在各自 07_computation/src。环境与依赖以实际运行记录为准。')
write('03_comparative/README.md','# 跨模型研究\n\n[比较](comparison/README.md) · [综合候选](synthesis/README.md) · [物理领域](physics_domains/README.md) · [应用](applications/README.md)\n\n比较须使用相同可观测量、单位、数据划分、参数计数和评价准则。缺失证据填写未检验；不能靠主张数量或自评等级判定优胜。\n\n[比较登记](comparison_matrix.csv)')
write('03_comparative/comparison_matrix.csv','comparison_id,observable,baseline,model_id,hypothesis_revision,free_parameters,data_ids,prediction,uncertainty,metric,run_id,status\n'+ '\n'.join(',,, '+r+',,,,,,,,not_tested' for r,_ in routes))
write('04_publications/README.md','# 跨模型出版资料\n\n[历史综合报告](legacy_reports/README.md) · [公共可视化](visualizations/README.md)\n\n此处保存既有综合性报告，尚未逐篇确认假设归属与审稿状态。单模型新论文放入该模型 13_publications；公共综述引用模型结论版本，不复制未经审查的主张为共同结论。')
write('90_archive/README.md','# 归档\n\n[历史资料](legacy/README.md) · [本次迁移记录](migrations/20260907_full_layout/manifest.json) · [迁移前完整快照](migrations/20260907_full_layout/before.zip)\n\nlegacy_tools 中的脚本仅用于历史查阅，不作为当前入口。快照逐字节保存本次修改前的文件，包含原有未提交编辑。恢复时解压到独立目录核对，不直接覆盖正在工作的目录。')
# Repair executable lookup after relocation, without modifying research formulae.
for p in (ROOT/'01_models').rglob('*.py'):
    body=p.read_text(encoding='utf-8')
    body=body.replace('SRC = os.path.normpath(os.path.join(HERE, "..", "..", "70_source_code"))','from pathlib import Path\nPROJECT_ROOT = next(p for p in Path(__file__).resolve().parents if (p / "02_shared" / "computation" / "src").is_dir())\nSRC = str(PROJECT_ROOT / "02_shared" / "computation" / "src")')
    p.write_text(body,encoding='utf-8')
write('00_governance/MIGRATION_GUIDE.md','# 2026-09-07 全生命周期重布局\n\n原始文件全部纳入快照和逐文件 SHA-256 清单；已有暂存与未暂存修改均按迁移开始时磁盘内容保留，未执行 git reset、提交或暂存。\n\n| 原目录 | 新目录 |\n|---|---|\n'+'\n'.join('| '+k+' | '+v+' |' for k,v in prefixes.items())+'\n\n原 00–08 阶段按语义迁入新阶段；空的 D/P/V/A 遗留目录移除。旧 verify.py 与 reorganize_structure.py 存入 legacy_tools，当前 verify.py 采用新结构。修复三处复算入口对共享源码的路径查找。历史综合论文与 GAQ 系列保留整体归档，归属未审定时不强行划入单一假设路线。\n\n[迁移清单](../90_archive/migrations/20260907_full_layout/manifest.json) · [完整快照](../90_archive/migrations/20260907_full_layout/before.zip)\n\n校验命令：`python verify.py`。快照只作恢复依据；历史文本中的旧路径与历史工具不代表当前运行约定。')
for row in inventory:
    row['sha256_after']=hashlib.sha256((ROOT/row['new']).read_bytes()).hexdigest()
write('90_archive/migrations/20260907_full_layout/manifest.json',json.dumps({'snapshot':'before.zip','original_file_count':len(inventory),'files':inventory},ensure_ascii=False,indent=2))
write('00_governance/layout.json',json.dumps({'sections':list(sections),'models':[r for r,_ in routes],'stages':[s for s,_,_ in stages]},indent=2))
print('Migrated',len(inventory),'original files; snapshot:',snapshot)
