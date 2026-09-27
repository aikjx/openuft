"""Focused document extraction; never executes source physics programs."""
from pathlib import Path
import json, re, sys, os, hashlib
from datetime import datetime, timezone
from collections import Counter
import networkx as nx
from graphify.detect import detect, save_manifest
from graphify.cache import check_semantic_cache, save_semantic_cache
from graphify.build import build_from_json, make_id
from graphify.extractors.base import _file_stem
from graphify.cluster import cluster, score_all
from graphify.analyze import god_nodes, surprising_connections, suggest_questions
from graphify.report import generate
from graphify.export import to_json, to_html
from graphify.diagnostics import diagnose_extraction, format_diagnostic_report

ROOT=Path('D:/a10/aikjx/code/my_lib/openuft/01_独立体系/S14_挠率统一场论TUFT/13_论文与成果/论文正文')
OUT=Path(__file__).resolve().parent
SPEC=Path('C:/Users/mo/.codex/skills/graphify/references/extraction-spec.md')
os.chdir(OUT)
# Repository policy requires Chinese research directory names. Redirect only
# this process's cache layout; never patch the installed library or source docs.
import graphify.cache as graph_cache
def chinese_cache_dir(root=OUT,kind='ast',prompt_fp=None):
    base=OUT/'图谱缓存'/'缓存'/('语义缓存' if kind=='semantic' else '语义深度缓存' if kind=='semantic-deep' else '结构缓存')
    if prompt_fp:base=base/('提取版本_p'+prompt_fp)
    base.mkdir(parents=True,exist_ok=True)
    return base
graph_cache.cache_dir=chinese_cache_dir
def write(name,data):
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
OUT.joinpath('.graphify_python').write_text(sys.executable,encoding='utf-8')
OUT.joinpath('.graphify_root').write_text(str(ROOT),encoding='utf-8')
raw=detect(ROOT,cache_root=OUT)
files=sorted(p for p in ROOT.glob('tuft_*.md'))
assert len(files)==29,len(files)
texts={str(p):p.read_text(encoding='utf-8-sig') for p in files}
det=dict(raw)
det['files']={'document':[str(p) for p in files]}
det['total_files']=len(files)
det['total_words']=sum(len(t.split()) for t in texts.values())
det['scope_note']='原始检测33项；授权聚焦顶层29份tuft_*.md，排除README及3份原稿。'
write('.graphify_detect.json',det)
cn,ce,ch,uncached=check_semantic_cache([str(p) for p in files],root=ROOT,prompt_file=SPEC,cache_root=OUT)
print('Corpus:',len(files),'docs;',det['total_words'],'whitespace-delimited words; cache hits',len(files)-len(uncached))
# Extraction is a deliberately focused new view: not an exhaustive formula inventory.
nodes=[]; edges=[]; byfile={}; concepts={}; seen_edges=set()
def nid(p,key): return make_id(_file_stem(Path(p).relative_to(ROOT)),key)
def loc(p,needle):
    for i,line in enumerate(texts[str(p)].splitlines(),1):
        if needle in line: return i,line
    raise ValueError((str(p),needle))
def node(p,key,label,needle,kind='rationale',rationale='',status='source_assertion'):
    p=str(p); ln,quote=loc(p,needle)
    n={'id':nid(p,key),'label':label,'file_type':kind,'source_file':p,
       'source_location':f'{p}:{ln}','rationale':rationale,
       'epistemic_status':status,'source_quote':quote,'source_url':None,
       'captured_at':None,'author':None,'contributor':None}
    nodes.append(n); return n['id']
def edge(s,t,p,needle,relation='references',confidence='EXTRACTED',score=1.0,rationale=''):
    # One relation per directed pair avoids simple-DiGraph silent collapse.
    if (s,t) in seen_edges:return
    seen_edges.add((s,t)); ln,quote=loc(p,needle)
    edges.append({'source':s,'target':t,'relation':relation,'confidence':confidence,
                  'confidence_score':score,'source_file':str(p),
                  'source_location':f'{p}:{ln}','source_quote':quote,
                  'rationale':rationale,'weight':1.0})
for p in files:
    title=next(l[2:] for l in texts[str(p)].splitlines() if l.startswith('# '))
    unique='document_'+hashlib.sha256(p.name.encode()).hexdigest()[:12]
    byfile[p.name]=node(p,unique,title,'# ',kind='document',rationale='正文来源节点；标题或PASS标签不是本图对物理真值的认证。')

# Explicit local citations: bare file mentions and Markdown citations are corpus facts.
for p in files:
    text=texts[str(p)]
    for name,target in byfile.items():
        if name!=p.name and name in text:
            edge(byfile[p.name],target,p,name,'cites')

def concept(filename,key,label,needle,rationale,status='source_assertion'):
    p=ROOT/filename
    ident=node(p,key,label,needle,rationale=rationale,status=status)
    concepts[key]=(ident,p,needle)
    edge(byfile[filename],ident,p,needle,'references')
    return ident
def depends(a,b,filename,needle,confidence='EXTRACTED',score=1.,rationale=''):
    edge(concepts[a][0],concepts[b][0],ROOT/filename,needle,'depends_on',confidence,score,rationale)

concept('tuft_统一场论_完成版_终版陈述.md','completion_scope','完成仅限写形：非四力统一','仅指**作用量完备','来源自己限制完成含义；本图保留此边界，未重新认证全部作用量。','declared_limitation')
concept('tuft_统一场论_完成版_终版陈述.md','torsion_split','挠率代数分解 24=4+4+16','24 = 4','反对称三阶张量的代数分解；分量维数不等于传播自由度。','algebraic_structure')
concept('tuft_统一场论_完成版_终版陈述.md','axial_dynamics','轴挠率单模传播：需完整拉氏量','轴挠率（赝标量）','正文只列L_T^axial名字与谱表，未给完整系数和约束；4维轴向分量不能自动当1个传播自由度。','review_required')
concept('tuft_统一场论_完成版_终版陈述.md','weyl_condition','b+4c=0：适用几何必须限定','y = (b + 4c)/2','无挠Levi-Civita曲率二次型可如此换基；独立Cartan联络含挠时不能直接推广无鬼充分性。','review_required')
concept('tuft_统一场论_完成版_终版陈述.md','r2_normalization','曲率平方前因子存在量纲风险','曲率二次型须以','自然单位[κ]=-2，[R²]=4，1/κ²使密度为8；若α无量纲，则与正文7/7配平声明冲突。','review_required')
concept('tuft_统一场论_完成版_终版陈述.md','unification_missing','群选择、耦合映射、量子化未完成','**未完成的**','本图将这些作为明确开放接口，而非使用标题认定已统一。','declared_limitation')
concept('tuft_统一场论_完成版_终版陈述.md','compact_group_overclaim','直积是唯一选择：只记来源断言','直积是唯一选择','非紧群不能嵌入紧致群不推出所有统一方案不可达；只否定此种嵌入，应限定no-go范围。','review_required')
concept('tuft_公理化_文稿_修订版.md','cartan','Cartan几何与内部规范丛并列','公理0′','需要焊接形式e和自旋联络ω；内部规范丛另加，不能据并列宣称耦合归一。','adopted_geometric_framework')
concept('tuft_公理化_文稿_修订版.md','sm_inputs','SU3×SU2×U1：外部规范输入','内部规范群','该内部群与规范物质结构是接入项，不是由时空挠率导出的结论。','adopted_input')
concept('tuft_公理化_文稿_修订版.md','scalar_eom','标量Euler-Lagrange条件式','□φ = V′(φ)','只有耦合RT被定义为合法标量后，φ的条件变分才有明确意义；不可据φ变分宣称几何场方程全闭合。','conditional_derivation')
concept('tuft_公理化_文稿_修订版.md','torsion_kinetic','T²代数项与挠率传播项区分','`T²` 不含 `∂T`','纯T²为代数项；含联络导数的曲率项需单独分析谱与约束。','conditional_derivation')
concept('tuft_公理化_文稿_修订版.md','nieh_yan','Nieh–Yan恰当形式与整数化条件','公理6′','恒等式NY=d(e∧T)与整数化不同：一般积分依赖边界、归一化和几何尺度；正文没有一般整值性证明。','review_required')
concept('tuft_公理化_文稿_修订版.md','phenomenological_anchors','θ0、V0、Λeff为外锚','三者只能外锚','势能真空位置与尺度是输入，不能据代数求驻点宣称解释了11/16。','adopted_input')
concept('tuft_公理化_修复优化报告.md','xi_no_go','ξ三视界约束：具体耦合边界','ξ 三视界不相容','来源对该ΩRT形式的尺度审查；不是所有挠率模型的否定定理。','source_model_result')
concept('tuft_相位pi_文稿_修订版.md','mobius_frame','Möbius标架翻转与4π复原','半扭转（莫比乌斯）','法向半扭转可直接验证；它是几何路径性质，尚非量子旋量物理推导。','geometric_construction')
concept('tuft_相位pi_文稿_修订版.md','rotation_bridge','标架绕行与空间旋转桥梁未证','待证明的对应','来源明确区分沿带绕行、外部SO3旋转和交换操作。','declared_limitation')
concept('tuft_相位pi_文稿_修订版.md','open_gauss_curve','半整数Gauss链接：端点需复查','`−0.4999`','奇半扭转单侧法向偏移q(2π)≠q(0)，不能直接当两条不交闭曲线的Gauss链接数；数值半整数不是通常链接整值定理。','review_required')
concept('tuft_r2_全维求导证明验证精算报告.md','spin_from_lk','s=|Lk|：几何到自旋对应输入','自旋量子数','计算Tw或标架周期不自行给出SO3/SU2量子表示、算符代数或旋转生成元；保留来源声称。','review_required')
concept('tuft_续篇_全维求导精算报告.md','exchange_input','交换相位含循环输入','循环输入','来源审查明确：先定义费米子半整数再算-1，不是独立自旋统计证明。','declared_limitation')
concept('tuft_全维分析续篇_自旋统计泡利手性.md','su2_adopted','SU2自旋表示：赋以而非导出','**赋以**而非**导出**','方向向量不满足算符SU2代数；需真正量子表示。','adopted_input')
concept('tuft_全维分析续篇_自旋统计泡利手性.md','pauli_conditional','反对称波函数⇒同态Slater为零','Slater 行列式恒为','代数结论成立的前提是已选择反对称统计；不逆推几何已导出统计。','conditional_derivation')
concept('tuft_全维分析续篇_自旋统计泡利手性.md','mass_scale_input','合法质量式仍缺尺度生成','尺度生成机制','m=ℏ√(κ²+τ²)/c量纲合法，但输入结尺度与康普顿关系不是电子质量数值独立预言。','declared_limitation')
concept('tuft_全维分析续篇_自旋统计泡利手性.md','weak_chirality','弱手性映射仍为定性假设','γ̂₅ ∝ T̂/|T̂|','γ5矩阵与三维方向矢量不能类型等同；W/Z耦合和V-A未由总作用量导出。','declared_limitation')
concept('tuft_色挠率_SU3_文稿_修订版.md','qcd_adopted','标准QCD拉氏量被采用','这是**标准 QCD 拉氏量**','文稿明确SU3与QCD是外部采用项。','adopted_input')
concept('tuft_色挠率_SU3_文稿_修订版.md','su3_mapping_open','T^a→A^a及K→Q²映射开放','对应关系**待建立**','没有规范协变构造、约束或几何能标映射，就无法导出QCD。','declared_limitation')
concept('tuft_色挠率_SU3_文稿_修订版.md','qcd_limit_conflict','跑动公式K→0与文稿文字冲突','K→0` 时**增强**','正b0公式α0/[1+b0α0 ln(Ksat/K)]在K→0为0，不增强或趋1/b0；只记录待修正断言。','review_required')
concept('tuft_色挠率_SU3_文稿_修订版.md','nonlinear_confinement','K∝r积分给r²：非线性弦势','V ~ ∫ r','其余因子常数时此积分标度成立；不能宣称已证明QCD一般禁闭。','conditional_derivation')
concept('tuft_四力统一_文稿_修订版.md','product_not_prediction','直积规范群不自动约束耦合','不能"归一"','并列EH+YM+Dirac不会自动替代标准模型参数或导出唯一统一能标。','declared_limitation')
concept('tuft_四力统一_文稿_修订版.md','sm_parameters','继承SM自由参数','19 个自由参数','参数计数取正文口径；不能代表包含中微子质量扩展的所有SM版本。','adopted_input')
concept('tuft_B_根因溯源报告.md','beta_identity','β∇²lnβ恒等式与条件源项','β1 · ∇²(ln β1)','β>0时成立；exp(-u)依赖先选择β层场方程。','conditional_derivation')
concept('tuft_收口_修复优化方案报告.md','beta_model_choice','β层场方程是修复选择','属**修复时的选择**','来源追溯原稿未给β层方程；后续自屏蔽和波形结论依赖模型选择。','declared_model_assumption')
concept('tuft_B_自屏蔽_数值求解报告.md','screening_model','自屏蔽数值解及波形代理','δh/h ~ (1−M_eff/M)','静态质量比不能自动给完整双星波形；来源LIGO排除结论需真实动力学映射与数据似然复核。','review_required')
concept('tuft_B_UV完成报告.md','uv_phenomenology','UV填回为唯象选型','UV 模型（唯象）','S(u)=exp(-u)sqrt(1+(u/uUV)^2)是新增模型函数，不是高阶几何作用量推导的UV完成。','declared_model_assumption')
concept('tuft_续篇B_挠率引力波.md','scalar_wave_mapping','δu径向应变映射需场方程','h_radial=δu','标量波方程不能直接认证GR张量偏振或所有度规响应；需场方程、规范和探测器响应。','review_required')
concept('tuft_黑洞热力学_文稿_修订版.md','bh_inputs','BH温度熵采用标准结果','ħc³/(8πGk_BM)','修正量纲并采用标准Hawking/BH关系不等于挠率态计数或信息问题已解。','adopted_input')
concept('tuft_黑洞热力学_文稿_修订版.md','singularity_boundary','曲率有界≠测地完备','测地线不完备','需完整解与因果/测地延拓证明。','declared_limitation')
concept('tuft_暴胀CMB_文稿_修订版.md','cmb_failure','原势慢滚预言未闭合','2 个观测量','正文展示参数要求冲突，不应从势能驻点计算跳到CMB已统一。','source_model_result')
concept('tuft_判据门禁.md','dimension_only','量纲门禁不认证物理正确','不校验物理正确性','精确量纲PASS只检验登记表达式，不认证语义、场方程或实验。','declared_limitation')
concept('tuft_全维度验证总报告.md','source_pass_scope','验证标签的证据范围','# ','来源总报告的PASS/FAIL是内部登记口径；本图不扩大为全部物理证明。','declared_limitation')

depends('axial_dynamics','torsion_split','tuft_统一场论_完成版_终版陈述.md','迹 4 + 张量 16')
depends('axial_dynamics','weyl_condition','tuft_统一场论_完成版_终版陈述.md','轴分量 + 无 Weyl','AMBIGUOUS',.2,'来源采用该条件；其对完整独立联络无鬼性的充分性尚未认证。')
depends('completion_scope','unification_missing','tuft_统一场论_完成版_终版陈述.md','**未完成的**')
depends('completion_scope','r2_normalization','tuft_统一场论_完成版_终版陈述.md','量纲 7/7','AMBIGUOUS',.2,'来源称完成依赖配平，但实际所写前因子须重审。')
depends('completion_scope','cartan','tuft_统一场论_完成版_终版陈述.md','Cartan 几何','INFERRED',.85)
depends('completion_scope','xi_no_go','tuft_统一场论_完成版_终版陈述.md','ξ 三视界 no-go','INFERRED',.85)
depends('scalar_eom','phenomenological_anchors','tuft_公理化_文稿_修订版.md','V(φ) = V₀','INFERRED',.95)
depends('cartan','sm_inputs','tuft_公理化_文稿_修订版.md','**并列**','INFERRED',.95,'表示并列模型接口，非数学上Cartan必然要求SM。')
depends('spin_from_lk','mobius_frame','tuft_r2_全维求导证明验证精算报告.md','Möbius 标架','INFERRED',.85)
depends('spin_from_lk','rotation_bridge','tuft_相位pi_文稿_修订版.md','待证明的对应','AMBIGUOUS',.2,'待建立物理桥梁；图上边表示缺口，不表示成立。')
depends('pauli_conditional','exchange_input','tuft_全维分析续篇_自旋统计泡利手性.md','两费米子总波函数反对称','INFERRED',.85)
depends('exchange_input','su2_adopted','tuft_全维分析续篇_自旋统计泡利手性.md','1/2-旋量的表示论','INFERRED',.75)
depends('qcd_adopted','su3_mapping_open','tuft_色挠率_SU3_文稿_修订版.md','其与挠率的对应关系','AMBIGUOUS',.2,'标准QCD不需要该映射；TUFT从挠率导出QCD才需要，尚缺。')
depends('product_not_prediction','sm_parameters','tuft_四力统一_文稿_修订版.md','继承 **19 个自由参数**')
depends('beta_identity','beta_model_choice','tuft_收口_修复优化方案报告.md','R1 补入的','INFERRED',.95)
depends('screening_model','beta_identity','tuft_B_自屏蔽_数值求解报告.md','exp(−u)','INFERRED',.95)
depends('uv_phenomenology','screening_model','tuft_B_UV完成报告.md','46.82%','INFERRED',.85)

extraction={'nodes':nodes,'edges':edges,'hyperedges':[],'input_tokens':0,'output_tokens':0,
            'audit_note':'人工聚焦语义提取；token计费未知，0仅表示没有调用独立付费提取后端。'}
write('.graphify_ast.json',{'nodes':[],'edges':[],'input_tokens':0,'output_tokens':0})
write('.graphify_semantic.json',extraction)
saved=save_semantic_cache(nodes,edges,[],root=ROOT,allowed_source_files=[str(p) for p in files],prompt_file=SPEC,cache_root=OUT)
write('proof_extraction.json',extraction)
write('.graphify_extract.json',extraction)
summary=diagnose_extraction(extraction,directed=True,root=str(ROOT))
write('graph_health.json',summary)
print(format_diagnostic_report(summary))
G=build_from_json(extraction,root=str(ROOT),directed=True)
if not G.number_of_nodes(): raise RuntimeError('Empty graph')
communities=cluster(G)
cohesion=score_all(G,communities)
def community_label(members):
    labels=' '.join(G.nodes[n].get('label','') for n in members)
    choices=[('公理与挠率动力学',['公理','挠率代数','曲率平方','Cartan','无鬼']),
             ('自旋统计与拓扑桥梁',['自旋','相位','Möbius','Slater','链接','旋转']),
             ('强弱作用与规范输入',['SU(3)','QCD','SU3','四力','规范','弱手性']),
             ('引力自屏蔽与模型选择',['自屏蔽','UV','β','续篇·选项 B','引力波','收口']),
             ('黑洞热力学与奇点边界',['黑洞','BH','测地']),
             ('宇宙学与慢滚检验',['暴胀','CMB','慢滚']),
             ('全书总账与验证门禁',['总索引','全书','全景','门禁','全维度验证','跨册'])]
    scores=[sum(labels.count(k) for k in keys) for _,keys in choices]
    return choices[scores.index(max(scores))][0] if max(scores)>0 else '统一目标与证明边界'
labels={cid:community_label(members) for cid,members in communities.items()}
curated={0:'自旋统计接口与引力波续篇',1:'自屏蔽源项与UV选型',
         2:'终版作用量与传播谱边界',3:'Cartan公理与规范外部输入',
         4:'莫比乌斯标架与旋转桥梁',5:'跨册判据与审查引文',
         6:'宇宙学慢滚与全书总账',7:'SU3接入与色挠率映射',
         8:'四力直积与参数继承',9:'黑洞热力学与奇点边界',
         10:'公理化修复与ξ尺度限制',11:'R1到R4验证标签边界'}
if len(communities)==12:labels=curated
# Duplicate communities retain distinguishable labels without implying new physics.
counts=Counter(labels.values())
labels={cid:(label+f'（组{cid}）' if counts[label]>1 else label) for cid,label in labels.items()}
gods=god_nodes(G); surprises=surprising_connections(G,communities)
questions=suggest_questions(G,communities,labels)
questions += [{'question':q,'community_id':None,'why':'追溯输入、适用条件与尚未闭合的物理桥梁。'} for q in
              ['Möbius标架4π复原与费米交换反对称之间缺哪一步独立证明？',
               '终版作用量的R²前因子与无鬼条件依赖哪些几何和量纲约定？',
               'SU(3)色挠率主张哪些是标准模型输入，哪些是尚缺的映射？']]
if not to_json(G,communities,str(OUT/'graph.json'),community_labels=labels):raise RuntimeError('Shrink guard')
report=generate(G,communities,cohesion,labels,gods,surprises,det,{'input':0,'output':0},str(ROOT),suggested_questions=questions)
warning_nodes=[n for n in nodes if n.get('epistemic_status')=='review_required']
intro='# TUFT 正文证明依赖图：阅读地图，不是证明认证\n\n'
intro+='范围：顶层29份tuft_*.md。原始目录33项检测后，排除README与原稿子目录3份。仅聚焦论证接口和正文显式引文，未穷举全部公式，也未执行原有物理脚本。\n\n'
intro+='边方向：论点 → 所采用的输入/前提；文档 → 所引用的文档。EXTRACTED=正文确实这么说，绝不表示其数学或物理内容已成立。AMBIGUOUS表示桥梁或适用性未证。节点epistemic_status与rationale保留来源断言的地位。\n\n'
intro+='成本：本机内联语义提取，无独立API调用；实际宿主token不可读取，图工具计数0不是零工作量。缓存、manifest、脚本和全部产物均写入本输出目录，未改源正文。\n\n'
intro+='工具限制：graphify benchmark已运行，但其内置示例问题未匹配中文图节点，返回No matching nodes found；因此不报告token压缩成绩。有向图无边折叠；健康检查中的7条“无向折叠”只是反向引文对在假设改成无向图时的结果，本产物保持方向。\n\n'
intro+='## 必须重审的来源断言\n\n'
for n in warning_nodes:intro+=f"- **{n['label']}**：{n['rationale']}（{Path(n['source_file']).name}，{n['source_location'].rsplit(':',1)[-1]}行）\n"
intro+='\n## 图完整性\n\n'+format_diagnostic_report(summary)+'\n\n'
(OUT/'GRAPH_REPORT.md').write_text(intro+report,encoding='utf-8')
write('.graphify_labels.json',{str(k):v for k,v in labels.items()})
write('.graphify_analysis.json',{'communities':{str(k):v for k,v in communities.items()},'cohesion':{str(k):v for k,v in cohesion.items()},'gods':gods,'surprises':surprises,'questions':questions})
if not to_html(G,communities,str(OUT/'graph.html'),community_labels=labels):raise RuntimeError('HTML guard')
# The stock exporter uses a CDN. Verify SRI and embed its already-pinned runtime
# so this deliverable is a single, offline HTML file.
import urllib.request, base64
html_path=OUT/'graph.html'; html=html_path.read_text(encoding='utf-8')
match=re.search(r'<script src="([^"]+)"\s+integrity="sha384-([^"]+)"\s+crossorigin="anonymous"></script>',html)
if match:
    runtime=urllib.request.urlopen(match.group(1),timeout=30).read()
    digest=base64.b64encode(hashlib.sha384(runtime).digest()).decode()
    if digest!=match.group(2):raise RuntimeError('Pinned HTML runtime SRI mismatch')
    html=html[:match.start()]+'<script>'+runtime.decode('utf-8').replace('</script','<\\/script')+'</script>'+html[match.end():]
html=html.replace('<html lang="en">','<html lang="zh-CN">')
html=html.replace('<title>graphify - graphify-out/graph.html</title>','<title>TUFT正文证明依赖图 · 来源断言不是证明认证</title>')
html=html.replace('<body>','<body><div style="position:fixed;top:0;left:0;z-index:10;padding:6px 12px;background:#2b1720;color:#ffd9a0;font-size:12px">29份正文 · 来源断言≠证明认证 · 箭头表示引用或所依赖前提 · 10项断言需复查</div>',1)
html_path.write_text(html,encoding='utf-8')
# Explicit output path: save_manifest's default would otherwise create nested graphify-out.
save_manifest({'document':[str(p) for p in files]},manifest_path=str(OUT/'manifest.json'),root=ROOT,scan_corpus=[str(p) for p in files])
write('cost.json',{'runs':[{'date':datetime.now(timezone.utc).isoformat(),'files':29,'input_tokens':None,'output_tokens':None,'separate_extraction_api_calls':0}],'note':'Host token usage unavailable; no paid extractor backend used.'})
write('corpus_manifest.json',{'files':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'lines':len(texts[str(p)].splitlines())} for p in files],'source_root':str(ROOT),'scope':'top-level tuft_*.md'})
write('build_summary.json',{'nodes':G.number_of_nodes(),'edges':G.number_of_edges(),'communities':len(communities),'community_labels':labels,'review_required_nodes':len(warning_nodes),'health':summary,'cached_files':saved,'coverage':'29 document nodes plus focused claim/input/limitation nodes; not proof certification'})
print('Built',G.number_of_nodes(),'nodes,',G.number_of_edges(),'edges,',len(communities),'communities; cached',saved,'files; review-required',len(warning_nodes))
