# -*- coding: utf-8 -*-
from pathlib import Path
import ast
import csv
import hashlib
import json
import os
import re
import zipfile

ROOT=Path(__file__).resolve().parent/'openuft'
assert ROOT.resolve()==Path(r'D:\a10\aikjx\code\my_lib\openuft').resolve()
MIG='90_archive/migrations/20260907_independent_systems'
if (ROOT/MIG/'before.zip').exists(): raise SystemExit('Already migrated')
def write(rel,text):
    p=ROOT/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.rstrip()+'\n',encoding='utf-8')
def link(source,target): return os.path.relpath(ROOT/target,(ROOT/source).parent).replace('\\','/')
systems=[
('s01_triad_kinematics','螺旋三重奏与谱几何','mathematical_framework','曲线曲率、挠率及运动生成元；不自动引入统一场论本体'),
('s02_zhang_space_motion','张祥前空间运动与统一力','candidate_theory','空间运动与 P=m(c-v)、F=dP/dt 的统一力假设'),
('s03_gaq_geometric_atom','GAQ 几何原子与作用量子','candidate_theory','离散几何元胞、作用量子化、曲率—能量对应及信息—质量对应'),
('s04_ieg_information_gravity','IEG 信息熵引力','candidate_theory','几何信息场、信息熵与引力动力学的联系'),
('s05_hdu_higher_dimensions','HDU 高维紧致化统一','candidate_theory','高维几何、紧致化及低维常数的投影关系'),
('s06_tcl_topological_chirality','TCL 拓扑手征锁定','candidate_theory','边界态、手征与费米子代结构的对应'),
('s07_gaq_complex_curvature','GAQ 复曲率融合体系','composite_candidate','v4 复曲率 κ+iτ 及 IEG/HDU/TCL 组合假设'),
('s08_gaq_geometrized_constants','GAQ 常数几何化体系','extension_candidate','v5 将 c、hbar 的独立地位改写为几何关系；与 v4 分开审查'),
('s09_gaq_mass_spectrum','GAQ 粒子质量谱体系','extension_candidate','v6 代结构、质量比与 Yukawa/QCD 几何化探索'),
('s10_frequency_helix_ontology','频率本源与复螺旋宇宙','candidate_theory','振动本体、作用量子及复曲率轨迹三项原理'),
('s11_gmuft_geometric_coupling','GMUFT 几何自由度与耦合','candidate_framework','曲率、挠率、拖拽与引力—电磁对应；完整场方程待建立'),
('s12_light_speed_helix','空间光速螺旋统一体系','candidate_theory','空间光速螺旋 v=c 为本源公设的统一场论报告系列'),
('p01_space_compression','空间压缩与密度本体','unformulated_direction','保留原 H02 独立方向；具体公设尚未建立'),
('p02_matter_source','物体驱动与源场本体','unformulated_direction','保留原 H03 独立方向；不与张祥前统一力自动等同'),
('p03_gauge_unification','规范对称统一候选','unformulated_direction','保留原 H05 独立方向；需要具体群、表示和作用量'),
('p04_quantum_emergence','量子结构与时空涌现候选','unformulated_direction','保留原 H06 独立方向；需要微观自由度和动力学'),
]
S={i:(title,kind,premise) for i,title,kind,premise in systems}
old_layout=json.loads((ROOT/'00_governance/layout.json').read_text(encoding='utf-8'))
stages=old_layout['stages']
template={p.relative_to(ROOT/'01_models/_template').as_posix():p.read_text(encoding='utf-8') for p in (ROOT/'01_models/_template').rglob('*.md')}
rules={
'01_models/h01_space_motion/04_derivations/D5_大统一力方程':'01_systems/s02_zhang_space_motion/04_derivations/D5_大统一力方程',
'01_models/h01_space_motion/05_consistency':'01_systems/s01_triad_kinematics/05_consistency',
'01_models/h01_space_motion/09_validation':'01_systems/s01_triad_kinematics/09_validation',
'01_models/h04_geometry_action/04_derivations/D0_作用量变分求导':'02_shared/baselines/classical_action/D0_作用量变分求导',
'02_shared/computation/src/triad_uft/physics.py':'02_shared/computation/src/physics_constants.py',
'02_shared/computation/src/triad_uft/derivations.py':'02_shared/computation/src/classical_derivations.py',
'02_shared/computation/src/triad_uft':'01_systems/s01_triad_kinematics/07_computation/src/triad_uft',
'90_archive/legacy/GAQ_UFT_v1_几何原子':'01_systems/s03_gaq_geometric_atom/90_archive/gaq_v1_collection',
'90_archive/legacy/GAQ_UFT_v3_三大新体系/三大新体系_v3.md':'03_comparative/source_collections/GAQ_v3_three_systems.md',
'90_archive/legacy/GAQ_UFT_v3_三大新体系':'01_systems/s03_gaq_geometric_atom/90_archive/gaq_early_extensions',
'90_archive/legacy/GAQ_UFT_v4_全维统一':'01_systems/s07_gaq_complex_curvature/13_publications/manuscript/gaq_v4',
'90_archive/legacy/GAQ_UFT_v5_cħ几何化':'01_systems/s08_gaq_geometrized_constants/13_publications/manuscript/gaq_v5',
'90_archive/legacy/GAQ_UFT_v6_质量谱':'01_systems/s09_gaq_mass_spectrum/13_publications/manuscript/gaq_v6',
'90_archive/legacy/宇宙本源_217KB_巨文档.md':'01_systems/s10_frequency_helix_ontology/13_publications/manuscript/频率螺旋_原著.md',
'90_archive/legacy/G_eps0_全维分析.md':'01_systems/s11_gmuft_geometric_coupling/13_publications/manuscript/G_eps0_全维分析.md',
'90_archive/legacy/大统一方程全集.md':'01_systems/s12_light_speed_helix/13_publications/manuscript/大统一方程全集.md',
'04_publications/legacy_reports/终极报告系列':'01_systems/s12_light_speed_helix/13_publications/manuscript/终极报告系列',
'01_models/h02_space_compression':'01_systems/p01_space_compression',
'01_models/h03_matter_driven':'01_systems/p02_matter_source',
'01_models/h05_gauge_symmetry':'01_systems/p03_gauge_unification',
'01_models/h06_quantum_emergence':'01_systems/p04_quantum_emergence',
'01_models':'90_archive/layout_reviews/six_route_layout',
}
for name in ['DIRECTORY_DESIGN_REVIEW.md','DIRECTORY_AUDIT.md','directory_audit.json','tools/audit_directories.py']:
    rules['00_governance/'+name]='90_archive/layout_reviews/six_route_analysis/'+name
def mapped(rel):
    for src,dst in sorted(rules.items(),key=lambda x:len(x[0]),reverse=True):
        if rel==src or rel.startswith(src+'/'): return dst+rel[len(src):]
    return rel
originals=sorted(p for p in ROOT.rglob('*') if p.is_file())
records=[{'old':p.relative_to(ROOT).as_posix(),'new':mapped(p.relative_to(ROOT).as_posix()),'sha256_before':hashlib.sha256(p.read_bytes()).hexdigest()} for p in originals]
snapshot=ROOT/MIG/'before.zip';snapshot.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(snapshot,'w',zipfile.ZIP_DEFLATED) as z:
    for p in originals:z.write(p,p.relative_to(ROOT).as_posix())
for row in records:
    src,dst=ROOT/row['old'],ROOT/row['new']
    if src!=dst:
        assert str(src.resolve()).startswith(str(ROOT.resolve())+os.sep)
        assert str(dst.resolve()).startswith(str(ROOT.resolve())+os.sep)
        if dst.exists():raise RuntimeError('Collision '+str(dst))
        dst.parent.mkdir(parents=True,exist_ok=True);src.rename(dst)
# Repair existing Markdown targets according to the exact source-file location.
pat=re.compile(r'(!?\[[^\]\n]*\]\()([^\s)]+)(\))')
from urllib.parse import unquote
for row in records:
    p=ROOT/row['new']
    if p.suffix!='.md' or '90_archive' in p.relative_to(ROOT).parts:continue
    def rep(m):
        t=m.group(2)
        if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:',t) or t.startswith('#'):return m.group(0)
        path,sep,frag=t.partition('#');old=Path(os.path.normpath(str((ROOT/row['old']).parent/unquote(path))))
        try:dest=ROOT/mapped(old.relative_to(ROOT).as_posix())
        except ValueError:dest=old
        return m.group(1)+os.path.relpath(dest,p.parent).replace('\\','/')+(sep+frag if sep else '')+m.group(3)
    p.write_text(pat.sub(rep,p.read_text(encoding='utf-8-sig')),encoding='utf-8')
for p in sorted(ROOT.rglob('*'),key=lambda p:len(p.parts),reverse=True):
    if p.is_dir() and not any(p.iterdir()):
        assert str(p.resolve()).startswith(str(ROOT.resolve())+os.sep);p.rmdir()

origins={
's01_triad_kinematics':[('01_systems/s01_triad_kinematics/05_consistency/P1_螺旋三重奏_TS1/研究总报告.md','三重奏专题与谱几何研究')],
's02_zhang_space_motion':[('01_systems/s02_zhang_space_motion/04_derivations/D5_大统一力方程/README.md','D5 统一力定义与复算')],
's03_gaq_geometric_atom':[('01_systems/s03_gaq_geometric_atom/90_archive/gaq_v1_collection/几何原子_v1.md','公理 A1–A5；后续全集保留谱系但不假设前提完全相同')],
's07_gaq_complex_curvature':[('01_systems/s07_gaq_complex_curvature/13_publications/manuscript/gaq_v4/v4_全维统一.md','摘要、五公理与三体系融合')],
's08_gaq_geometrized_constants':[('01_systems/s08_gaq_geometrized_constants/13_publications/manuscript/gaq_v5/v5_cħ几何化.md','摘要及 v4→v5 常数地位变更')],
's09_gaq_mass_spectrum':[('01_systems/s09_gaq_mass_spectrum/13_publications/manuscript/gaq_v6/v6_质量谱_几何化.md','摘要、SO(3) 代结构及质量比探索')],
's10_frequency_helix_ontology':[('01_systems/s10_frequency_helix_ontology/13_publications/manuscript/频率螺旋_原著.md','总序三条原理')],
's11_gmuft_geometric_coupling':[('01_systems/s11_gmuft_geometric_coupling/13_publications/manuscript/G_eps0_全维分析.md','第 V 节 GMUFT 框架及第 VIII 节限制')],
's12_light_speed_helix':[('01_systems/s12_light_speed_helix/13_publications/manuscript/终极报告系列/v6_20260906_FINAL.md','核心公理及第 I 节；与 GAQ v6 不是同一个版本序列')],
}
source='03_comparative/source_collections/GAQ_v3_three_systems.md'
lines=(ROOT/source).read_text(encoding='utf-8').splitlines(keepends=True)
chapter_records=[]
for sid,start,end in [('s04_ieg_information_gravity',48,112),('s05_hdu_higher_dimensions',113,182),('s06_tcl_topological_chirality',183,256)]:
    target='01_systems/'+sid+'/02_assumptions/source_chapter.md'
    excerpt=''.join(lines[start-1:end]);write(target,excerpt)
    origins[sid]=[(target,'GAQ v3 原文独立章节；保留原主张，不表示审定'),(source,'完整原著；章节为派生摘录')]
    chapter_records.append({'system_id':sid,'source':source,'source_sha256':hashlib.sha256((ROOT/source).read_bytes()).hexdigest(),'start_line':start,'end_line':end,'derived_path':target,'extracted_text_sha256':hashlib.sha256(excerpt.encode('utf-8')).hexdigest()})
deps={
's07_gaq_complex_curvature':['s03_gaq_geometric_atom','s04_ieg_information_gravity','s05_hdu_higher_dimensions','s06_tcl_topological_chirality'],
's08_gaq_geometrized_constants':['s07_gaq_complex_curvature'],
's09_gaq_mass_spectrum':['s08_gaq_geometrized_constants','s06_tcl_topological_chirality'],
}
for sid,title,kind,premise in systems+[('_template','新独立体系模板','template','必须根据来源定义公设签名')]:
    base='01_systems/'+sid
    for rel,body in template.items():
        if rel in ['README.md','sources.md']:continue
        if not (ROOT/base/rel).exists():
            # Scaffold copy only; references use new shared roots at the same depth.
            write(base+'/'+rel,body.replace('新假设路线模板',title))
    sources=[{'path':path,'locator':loc} for path,loc in origins.get(sid,[])]
    if sid.startswith('p'):
        sources=[{'path':base+'/sources.md','locator':'原宽泛路线候选索引；尚无独立公设来源'}]
    meta={'id':sid,'title':title,'kind':kind,'status':'unreviewed' if not sid.startswith('p') else 'unformulated','hypothesis_revision':None,'premise_summary':premise,'premise_status':'原文主张的归属摘要；非科学认证','postulates':[],'source_records':sources,'related_systems':deps.get(sid,[]),'code_dependencies':['02_shared/computation/src'] if sid in ['s01_triad_kinematics','s02_zhang_space_motion'] else [],'owner':None}
    write(base+'/system.json',json.dumps(meta,ensure_ascii=False,indent=2))
    write(base+'/README.md','# '+title+'\n\n编号：`'+sid+'`；类型：`'+kind+'`。\n\n基础前提：'+premise+'。\n\n独立管理公设、推导、代码、数据、结论及发布，不继承其他体系的证据等级。当前科学状态：待审查；空模板不表示研究完成。\n\n[体系身份](system.json) · [来源与谱系](sources.md) · [体系总表](../README.md)\n\n| 生命周期 | 入口 |\n|---|---|\n'+'\n'.join('| '+stage+' | [说明]('+stage+'/README.md) |' for stage in stages)+'\n\n'+('上游体系：'+', '.join('['+x+'](../'+x+'/README.md)' for x in deps.get(sid,[])) if deps.get(sid) else '目前没有声明对其他候选体系的结论依赖。'))
    if not sid.startswith('p'):
        write(base+'/sources.md','# 来源与边界\n\n'+('\n'.join('- ['+loc+']('+link(base+'/sources.md',path)+')' for path,loc in origins.get(sid,[])) or '待录入具体原始资料。')+'\n\n归属按原文明示的前提与章节判断；目录独立不表示理论已经成立，也不表示各体系毫无亲缘关系。版本名称只在本体系内解释。')
    write(base+'/claims.csv','claim_id,hypothesis_revision,statement,assumptions,derivation,prediction,run_id,data_id,uncertainty,evidence_level,status,reviewer') if not (ROOT/base/'claims.csv').exists() else None
    if not (ROOT/base/'08_data/data_registry.csv').exists():write(base+'/08_data/data_registry.csv','data_id,source_url,version,retrieved_at,license,units,sha256,local_path,processing_run_id')
    write(base+'/07_computation/runs/run_template.json',json.dumps({'run_id':None,'system_id':sid,'claim_ids':[],'code_revision':None,'command':None,'environment':None,'parameters':{},'input_data_ids':[],'outputs':[],'exit_code':None},ensure_ascii=False,indent=2))
    # Obsolete model.json is retained as a legacy identity rather than a second active identity.
    old=ROOT/base/'model.json'
    if old.exists():
        dst=ROOT/base/'90_archive/previous_model_identity.json';dst.parent.mkdir(parents=True,exist_ok=True);old.rename(dst)
        for row in records:
            if row['new']==base+'/model.json':row['new']=base+'/90_archive/previous_model_identity.json'

# Split the former mixed implementation into system-specific and baseline modules.
baseline=ROOT/'02_shared/computation/src/classical_derivations.py'
body=baseline.read_text(encoding='utf-8');tree=ast.parse(body)
fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='zhang_unified_force')
bodylines=body.splitlines(keepends=True);zhang=''.join(bodylines[fn.lineno-1:fn.end_lineno])
basebody=''.join(bodylines[:fn.lineno-1]+bodylines[fn.end_lineno:])
basebody=basebody.replace('from . import physics','import physics_constants as physics').replace(', "zhang_unified_force"','')
write('02_shared/computation/src/classical_derivations.py',basebody)
bootstrap='from pathlib import Path\nimport sys\nROOT = next(p for p in Path(__file__).resolve().parents if (p / "02_shared" / "computation" / "src").is_dir())\nsys.path.insert(0, str(ROOT / "02_shared" / "computation" / "src"))\n'
write('01_systems/s02_zhang_space_motion/07_computation/src/zhang_force.py','# -*- coding: utf-8 -*-\n'+bootstrap+'import math\nimport physics_constants as physics\n\n'+zhang)
package='01_systems/s01_triad_kinematics/07_computation/src/triad_uft'
write(package+'/physics.py','# Shared historical constants; no independent copy.\n'+bootstrap+'from physics_constants import *\n')
write(package+'/derivations.py','# Classical baseline compatibility import.\n'+bootstrap+'from classical_derivations import *\n')
for path,module,src in [
('01_systems/s02_zhang_space_motion/04_derivations/D5_大统一力方程/D5_大统一力方程.py','import zhang_force as derivations','01_systems/s02_zhang_space_motion/07_computation/src'),
('02_shared/baselines/classical_action/D0_作用量变分求导/D0_作用量变分求导.py','import classical_derivations as derivations','02_shared/computation/src'),
('01_systems/s01_triad_kinematics/09_validation/V2_mpmath高精度/verify_V2.py',None,'01_systems/s01_triad_kinematics/07_computation/src')]:
    p=ROOT/path;text=p.read_text(encoding='utf-8')
    text=text.replace('SRC = str(PROJECT_ROOT / "02_shared" / "computation" / "src")','SRC = str(PROJECT_ROOT / "'+src+'")')
    if module:text=text.replace('from triad_uft import derivations',module)
    write(path,text)
write('02_shared/computation/README.md','# 共享计算基础\n\n这里只保留共同常数与经典演示，不保管候选理论主实现。\n\n- [物理常数](src/physics_constants.py)\n- [经典变分演示](src/classical_derivations.py)\n- [D0 入口](../baselines/classical_action/D0_作用量变分求导/README.md)\n\n三重奏算法移入 S01；张祥前统一力函数移入 S02。历史常数和演示的科学说明仍需审查。')
write('02_shared/baselines/README.md','# 基准演示\n\n[经典作用量示例](classical_action/README.md)。数学方法与既有理论演示不单独冒充新的宇宙本体。')
write('02_shared/baselines/classical_action/README.md','# 经典作用量\n\n[D0 变分复算](D0_作用量变分求导/README.md)。此入口不等价于 GAQ 几何原子体系。')
write('03_comparative/source_collections/README.md','# 跨体系原著\n\n[GAQ v3 完整原著](GAQ_v3_three_systems.md)同时包含 IEG、HDU、TCL。各体系保留独立章节摘录，原著只有一份主文件；摘录来源和行号见 [溯源登记](../../00_governance/chapter_provenance.json)。')
write('00_governance/chapter_provenance.json',json.dumps(chapter_records,ensure_ascii=False,indent=2))
write('01_systems/README.md','# 独立大体系总入口\n\n按原始公设、机制及明确分支识别体系，不再按“几何/量子”等宽泛标签装入六个总筐。前十二项有原文专题或独立章节；后四项是保留的待建模方向，不能视为已建立理论。\n\n| 独立目录 | 体系 | 类型 | 基础前提 |\n|---|---|---|---|\n'+'\n'.join('| ['+sid+']('+sid+'/README.md) | '+title+' | '+kind+' | '+premise+' |' for sid,title,kind,premise in systems)+'\n\n[为何这样拆分](../00_governance/INDEPENDENT_SYSTEMS_DESIGN.md) · [新体系模板](_template/README.md)。各体系采用相同生命周期，但拥有自己的身份、来源、证据、代码与发布入口。')
write('README.md','# OpenUFT · 独立理论体系研究\n\n## 先选大体系\n\n[全部独立体系](01_systems/README.md)：12 个有原文依据的研究体系/分支，4 个独立待建模方向。研究框架、组合候选和扩展分支分别注明类型，目录存在不表示理论成立。\n\n'+'\n'.join('- ['+title+'](01_systems/'+sid+'/README.md)' for sid,title,kind,premise in systems)+'\n\n## 全局支持\n\n[项目治理](00_governance/README.md) · [共同方法](02_shared/README.md) · [跨体系比较](03_comparative/README.md) · [综合出版](04_publications/README.md) · [历史归档](90_archive/README.md) · [待审输入](99_inbox/README.md)\n\n[重新拆分的分析与依据](00_governance/INDEPENDENT_SYSTEMS_DESIGN.md) · [全部目录分析](00_governance/DIRECTORY_AUDIT.md) · [文件索引](00_governance/catalog/material_catalog.md)\n\n每个体系内部：立项、文献、公设、数学形式、推导、一致性、预测、计算、数据、验证、不确定度、证伪、结论、论文、评审、发布、归档。\n\n结构检查：`python verify.py`。')
write('INDEX.md','# 导航\n\n[独立大体系](01_systems/README.md) · [拆分依据](00_governance/INDEPENDENT_SYSTEMS_DESIGN.md) · [逐目录分析](00_governance/DIRECTORY_AUDIT.md) · [全量文件](00_governance/catalog/material_catalog.md)')
write('QUICKSTART.md','# 快速开始\n\n1. 在 [大体系总表](01_systems/README.md) 选择具体体系；未知资料进入 99_inbox。\n2. 阅读 system.json 和 sources.md，确认原始前提，不因相同公式自动合并体系。\n3. 登记该体系 claims.csv，链接本体系推导、运行、数据及结论。\n4. 在 openuft 根目录运行 `python verify.py`。\n5. 三重奏复算：进入 `01_systems/s01_triad_kinematics/07_computation/src` 执行 `python -m triad_uft.verify`。\n\n[迁移与独立边界](00_governance/INDEPENDENT_SYSTEMS_DESIGN.md)。')
layout={'sections':['00_governance','01_systems','02_shared','03_comparative','04_publications','90_archive','99_inbox'],'systems':[sid for sid,_,_,_ in systems],'stages':stages,'identity_file':'system.json'}
write('00_governance/layout.json',json.dumps(layout,ensure_ascii=False,indent=2))
write('00_governance/system_registry.json',json.dumps({'systems':[json.loads((ROOT/'01_systems'/sid/'system.json').read_text(encoding='utf-8')) for sid,_,_,_ in systems]},ensure_ascii=False,indent=2))
with (ROOT/'03_comparative/comparison_matrix.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.writer(f);w.writerow(['comparison_id','observable','baseline','system_id','hypothesis_revision','free_parameters','data_ids','prediction','uncertainty','metric','run_id','status'])
    for sid,_,_,_ in systems:w.writerow(['','','',sid,'','','','','','','','not_tested'])
# Current governance replaces former six-route claims; historical analysis is retained.
for rel in ['00_governance/WORKFLOW.md','00_governance/CONTRIBUTING.md','00_governance/FAQ.md','00_governance/ROADMAP.md']:
    p=ROOT/rel;text=p.read_text(encoding='utf-8').replace('01_models','01_systems').replace('model.json','system.json').replace('六条','各独立').replace('H01-C0001','S01-C0001').replace('H01-D0001','S01-D0001')
    write(rel,text)
write('00_governance/DIRECTORY_DESIGN_REVIEW.md','# 目录设计评估：已更新\n\n此前六路线结构不足以满足独立体系要求，已被新的 [独立体系设计分析](INDEPENDENT_SYSTEMS_DESIGN.md) 取代。\n\n[旧分析仅供追溯](../90_archive/layout_reviews/six_route_analysis/DIRECTORY_DESIGN_REVIEW.md)；其 262 目录统计不再描述当前布局。')
for row in records:
    row['sha256_after']=hashlib.sha256((ROOT/row['new']).read_bytes()).hexdigest()
write(MIG+'/manifest.json',json.dumps({'snapshot':'before.zip','original_file_count':len(records),'files':records},ensure_ascii=False,indent=2))
dest=ROOT/MIG/Path(__file__).name
Path(__file__).resolve().rename(dest)
print('Migrated',len(records),'files; created',len(systems),'independent containers')
