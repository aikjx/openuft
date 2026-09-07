# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib
import json
import os
ROOT=Path(__file__).resolve().parent/'openuft'
def write(rel,body):
    p=ROOT/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(body.rstrip()+'\n',encoding='utf-8')
layout=json.loads((ROOT/'00_governance/layout.json').read_text(encoding='utf-8'))
descriptions=[
'明确本体系研究问题、负责人、范围、里程碑和停止条件。',
'记录原始文献、准确出处、模型相关解读和基准；公共书目用链接引用。',
'明确原始公设、本体、自由度、尺度与适用边界；来源摘要不等于已完成公设审查。',
'统一符号、单位、度规约定、场空间、初值与边界条件。',
'逐步列出本体系前提、借用定理、近似和输出方程；不得循环论证。',
'审查证明前提、量纲、守恒、稳定性、因果性及已知极限；数值样本不替代一般证明。',
'在检验之前明确可观测量、参数与基准差异；区分拟合和独立预测。',
'管理本体系源码、配置、测试与运行；共同基准显式声明依赖，专属算法不得放入公共总筐。',
'保存原始/派生数据、来源、许可、单位和处理链；一份数据只有一个主位置。',
'区分实现验证、数值收敛和独立观测检验，链接实际运行与数据版本。',
'记录统计、系统、离散化和模型误差；报告敏感性与参数可辨识性。',
'保留反例、负结果、预设失效阈值和范围收缩，不能因结果不利而删除。',
'逐条链接本体系公设与证据，区分数学结论、数值检查、观测支持、猜想与被反驳主张。',
'本体系原著、正文、图表及补充材料；跨体系综述保留共同主文件并建立引用。',
'记录具体版本、审查人、意见、逐条回复和独立复现；自评不等于同行评审。',
'发布时冻结版本、代码提交、数据、环境、校验和与引用；未发布时保持草稿状态。',
'保留本体系旧版本、前提变化、停止原因和替代入口；历史标题不代表当前科学状态。']
for sid in layout['systems']+['_template']:
    base=ROOT/'01_systems'/sid
    meta=json.loads((base/'system.json').read_text(encoding='utf-8'))
    for stage,desc in zip(layout['stages'],descriptions):
        p=base/stage
        entries=sorted(x for x in p.iterdir() if x.name!='README.md')
        navigation='\n\n现有条目：\n\n'+'\n'.join('- ['+x.name+']('+x.name+('/' if x.is_dir() else '')+')' for x in entries) if entries else '\n\n当前尚无本阶段独立产物；不因目录存在而标记完成。'
        write('01_systems/'+sid+'/'+stage+'/README.md','# '+stage+'\n\n所属独立体系：['+meta['title']+'](../README.md)。\n\n'+desc+'\n\n[身份与基础前提](../system.json) · [来源](../sources.md) · [证据登记](../claims.csv)'+navigation)
    if sid.startswith('p'):
        plan=base/'00_project/plan.md'
        write(plan.relative_to(ROOT).as_posix(),'# 待建模计划\n\n独立方向：'+meta['title']+'。\n\n负责人、公设、版本和退出条件：待定义。原候选关键词关联不作为已建立理论的证据。\n\n[身份登记](../system.json)')
write('00_governance/README.md','# 项目治理\n\n[独立体系设计与最优性判断](INDEPENDENT_SYSTEMS_DESIGN.md) · [全部实际目录分析](DIRECTORY_AUDIT.md) · [体系总登记](system_registry.json) · [机器目录审计](directory_audit.json)\n\n[生命周期](WORKFLOW.md) · [文件索引](catalog/README.md) · [迁移说明](MIGRATION_GUIDE.md) · [验证记录](VALIDATION.md)\n\n当前主轴是 01_systems 中的具体体系；旧六路线分析保存在历史区，不再指导当前目录。')
write('00_governance/MIGRATION_GUIDE.md','# 当前迁移说明\n\n最新布局以 [独立大体系](../01_systems/README.md) 为主轴，取代原六条宽泛路线。\n\n[拆分理由与路径变化](INDEPENDENT_SYSTEMS_DESIGN.md) · [本轮逐文件映射](../90_archive/migrations/20260907_independent_systems/manifest.json) · [本轮完整快照](../90_archive/migrations/20260907_independent_systems/before.zip)\n\n本轮保存 393 个迁移前文件；上一轮 193 文件快照仍在。检查器按两轮映射验证文件仍可定位。原暂存状态没有重置，没有自动提交。恢复时先解压到独立目录。')
write('00_governance/VALIDATION.md','# 独立体系拆分验证\n\n- 16 个独立容器：12 个有来源的研究体系/分支，4 个待建模方向；另含模板。\n- 各体系 17 个生命周期阶段、独立身份与证据登记。\n- 三个 GAQ v3 章节按原文行号提取，检查器核对原著哈希与摘录内容。\n- 两轮迁移快照分别保存 193 和 393 个文件，按映射检查原件可恢复与目标存在。\n- 拆分后 triad、D5、D0、V2 四个入口实际运行，全部退出码 0。\n\n[原始命令、工作目录及输出](independent_systems_execution.json)。运行成功是执行检查，不是理论认证；历史输出的 STRICT/VERIFIED 标签未经本次科学审定。\n\n当前结构与内部文件链接用 `python verify.py` 检查；目录统计以 [自动审计](DIRECTORY_AUDIT.md) 为准。')
write('02_shared/README.md','# 共享基础\n\n[公共协议](protocols/README.md) · [参考文献](references/README.md) · [共同常数与经典函数](computation/README.md) · [经典基准演示](baselines/README.md)\n\n候选体系专属代码、公设、论文和结论归 01_systems。共享只表示复用，不能授予某个体系科学认可。')
write('03_comparative/README.md','# 跨体系研究\n\n[体系独立入口](../01_systems/README.md) · [比较登记](comparison_matrix.csv) · [比较方案](comparison/README.md) · [综合候选](synthesis/README.md) · [跨体系原著](source_collections/README.md) · [物理领域](physics_domains/README.md) · [应用](applications/README.md)\n\n比较需同一观测量、单位、数据划分与评价准则，注明每个体系的公设版本；组合不能自动继承上游结论。')
write('90_archive/README.md','# 全局历史归档\n\n[旧研究材料](legacy/README.md) · [当前独立体系设计](../00_governance/INDEPENDENT_SYSTEMS_DESIGN.md) · [最近迁移快照](migrations/20260907_independent_systems/before.zip) · [最近映射](migrations/20260907_independent_systems/manifest.json)\n\nlayout_reviews 保存原六路线骨架及分析；legacy_tools 保存失效工具。已明确归属的理论资料已进入各独立体系，历史区不再作为它们的唯一入口。')
# Mark lineage ambiguity explicitly without asserting all versions share identical axioms.
write('01_systems/s12_light_speed_helix/13_publications/manuscript/终极报告系列/README.md','# 报告系列的前提边界\n\nv5/v6 明确采用空间光速螺旋公设；v3/v4 是垂直原理与螺旋几何前驱报告，不能默认公设完全一致；v2 是更广泛的跨体系综述。此目录按报告谱系保存完整版本，不表示它们共享同一冻结公设。\n\n逐版本结论必须标明版本与具体假设；若前驱形成独立活跃公设体系，再登记新体系 ID。GAQ v6 质量谱属于 S09，不属于这个 v6 序列。')
manifest_path=ROOT/'90_archive/migrations/20260907_independent_systems/manifest.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
for row in manifest['files']:row['sha256_after']=hashlib.sha256((ROOT/row['new']).read_bytes()).hexdigest()
manifest['after_hash_note']='After hashes record migration completion; regenerated catalogs may change later. Before snapshot hashes are immutable.'
write(manifest_path.relative_to(ROOT).as_posix(),json.dumps(manifest,ensure_ascii=False,indent=2))
src=Path(__file__).resolve();dst=ROOT/'90_archive/migrations/20260907_independent_systems'/src.name
assert str(dst.resolve()).startswith(str(ROOT.resolve())+os.sep)
src.rename(dst)
print('Updated current navigation and all system stage boundaries')
