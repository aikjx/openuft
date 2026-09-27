# -*- coding: utf-8 -*-
"""
P01/P02/P04 待建模方向 · 可建模性终审（算法联盟 triage）
纯标准库。用法: python p_directions_triage.py

不伪造研究：对三个仍 unformulated 的方向，机器化审计其本库内是否存在
[独立主张/公设/自身材料/可检验预言]，并对名称隐含的朴素机械本体做经验封死精算。
输出结构化裁决，不改动体系身份。
"""
import os, re, json, math

ROOT=r'D:\a10\aikjx\code\my_lib\openuft'
SYS=os.path.join(ROOT,'01_独立体系')
dirs={'P01':'P01_空间压缩与密度本体','P02':'P02_物体驱动与源场本体','P04':'P04_量子结构与时空涌现候选'}

def read(rel):
    p=os.path.join(ROOT,rel)
    return io_open(p) if os.path.exists(p) else ''
def io_open(p):
    with open(p,encoding='utf-8') as f: return f.read()

GOV=('.github/','CHANGELOG','CONTRIBUTING','FAQ','ROADMAP','WORKFLOW','MIGRATION','QUICKSTART','INDEX.md','/docs/','00_项目治理/资料索引')

print('='*92)
print(' A. 内容审计（计数；判定"是否存在可建模的本库独立内容"）')
print('='*92)
audit={}
for tag,d in dirs.items():
    base=os.path.join(SYS,d)
    sj=json.loads(io_open(os.path.join(base,'system.json')))
    src=io_open(os.path.join(base,'sources.md'))
    links=re.findall(r'\]\(([^)]+)\)',src)
    own=[u for u in links if not u.startswith('http') and (('/'+d+'/') in (u.replace('\\','/')) )]
    gov=[u for u in links if any(g in u.replace('\\','/') for g in GOV)]
    # 是否含"未找到/待定义/尚无"空声明
    empty_flag=bool(re.search(r'尚未找到|待定义|尚无独立|需要独立建模',src))
    # 体系内非 README 占位的实质文件（.md/.py 且 >0 且非模板）
    substantive=0
    for dp,_,fs in os.walk(base):
        if '90_历史归档' in dp: continue
        for fn in fs:
            if fn.endswith(('.md','.py')) and fn not in ('README.md','sources.md','review_template.md','release_template.md','run_template.md'):
                if os.path.getsize(os.path.join(dp,fn))>300: substantive+=1
    audit[tag]=dict(id=sj['id'],npost=len(sj.get('postulates',[])),nlinks=len(links),
                    nown=len(own),ngov=len(gov),empty=empty_flag,nsub=substantive)
    print(f"\n[{tag}] {sj['id']}  ({d})")
    print(f"  postulates 公设数                : {audit[tag]['npost']}")
    print(f"  sources 链接总数                 : {audit[tag]['nlinks']}")
    print(f"   ├ 指向本体系自身目录的链接       : {audit[tag]['nown']}   <- 独立材料")
    print(f"   └ 指向.github/CHANGELOG等治理件 : {audit[tag]['ngov']}   <- 自动误关联")
    print(f"  含'尚未找到/待定义/尚无'空声明    : {audit[tag]['empty']}")
    print(f"  体系内实质文件(>300B,非模板)      : {audit[tag]['nsub']}")
    buildable = audit[tag]['npost']>0 or audit[tag]['nown']>0 or audit[tag]['nsub']>0
    audit[tag]['buildable']=buildable
    print(f"  => 是否存在可建模独立内容         : {'是' if buildable else '否（空标签）'}")

print()
print('='*92)
print(' B. 朴素机械本体的经验封死：洛伦兹不变性 → 等效"以太风"速度精算')
print('='*92)
c=2.99792458e8
# MM 往返平均速各向异性与以太风：Δc/c ≈ (1/2)(v/c)^2 （二阶，O(1) 干涉仪几何因子）
def v_ether(dc2): return c*math.sqrt(2*dc2)
cases=[("Michelson-Morley 1887（实测报道上限 v<6.64 km/s）",6.64e3,None),
       ("低温光学腔 Müller 2003 Δc/c=2.6e-15",None,2.6e-15),
       ("旋转光学腔 Herrmann 2009 Δc/c=1e-17",None,1.0e-17),
       ("Brillet-Hall 类一年数据 Δc/c≈1e-18",None,1.0e-18)]
print(f"{'检验':<46}{'Δc/c':>11}{'等效以太风 v_eth':>18}")
v0=6.64e3
for name,v,dc in cases:
    if v is not None:
        dc_eff=0.5*(v/c)**2
        print(f"{name:<46}{dc_eff:11.1e}{v:>13.2f} m/s ({v/1000:.2f} km/s)")
    else:
        ve=v_ether(dc)
        print(f"{name:<46}{dc:11.0e}{ve:>13.3f} m/s")
ve17=v_ether(1e-17); ve18=v_ether(1e-18)
print()
print(f"现代实验把等效以太风从上界 6.64 km/s 压到 {ve18:.2f}–{ve17:.2f} m/s")
print(f"速度改善倍数: {v0/ve17:.2e}（对 1e-17）~ {v0/ve18:.2e}（对 1e-18）")
print(f"Δc/c 改善: 从 ~{0.5*(v0/c)**2:.1e} 到 1e-17/1e-18，约 {0.5*(v0/c)**2/1e-18:.1e} 倍（对1e-18）")
print("Hughes-Drever 质量/时钟各向异性：原始 δ~1e-15，冷阱现代相对限制 ~1e-22(电子)–1e-27(核子)，")
print("  绝对能级各向异性 ~1e-25 GeV（原始0.04 Hz）以下；SME κ_{e-} 光子扇区前沿 ~3e-30（预印本低温硅腔）。")

print()
print('='*92)
print(' C. 裁决')
print('='*92)
verdict={
 'P01':('EMPTY_LABEL + 朴素优越系介质版本经验封死',
   '无独立主张/公设/材料（sources 自陈"尚未找到"）。名称隐含的"空间被压缩成密度"若取带优越参考系的机械介质本体，'
   '其以太风/各向异性已被 Δc/c≲1e-17、质量各向异性≲1e-22..1e-27 封死；其洛伦兹协变的合理内涵（应力-能量张量、'
   '连续介质密度、GR 度规形变）已被标准连续介质力学与广义相对论覆盖，亦在 S02/S12/S13 中以候选形式出现。'
   '不构成可研究候选：无主张可证伪，不能标 falsified；保持 unformulated，建议归档或并入 S02/S13。'),
 'P02':('EMPTY_LABEL + 朴素发射说/源场版本经验封死',
   'sources 仅自动关联到 S02/S12 既有文件，自身零内容。"物体驱动/发射源场"若取机械发射说（类似 corpuscular/Le Sage），'
   '与洛伦兹协变、能量守恒、拖曳/吸收热灾难等冲突，且优越系版本被 Δc/c≲1e-17 封死；洛伦兹协变的场源版本就是'
   '标准场论 Tμν→Gμν 与 GR，非新本体。不构成可研究候选；保持 unformulated，建议归档或并入。'),
 'P04':('真实主流领域，但本库零原创建模',
   '"量子结构→时空涌现"在主流真实存在（AdS/CFT、Ryu-Takayanagi S=A/4G_N、Jacobson 纠缠平衡导出 Einstein 方程、'
   'ER=EPR、causal set、LQG/spin-foam、It-from-Qubit），但 sources 全为对 S01/S03..S12 与治理文件的关键词误关联，'
   '本体系无微观自由度、无哈密顿量、无纠缠结构、无导出。不能借 RT/Jacobson 给 openuft 螺旋本体背书（那些框架不依赖螺旋）。'
   '保持 unformulated；复活门槛=先给微观 DOF+动力学，再导出低能可与 GR+QFT 区分的可检验量。'),
}
for tag,(code,desc) in verdict.items():
    print(f"\n[{tag}] {audit[tag]['id']}  裁决码: {code}")
    print('  '+desc)

print()
print('='*92)
print(' D. 处置（不改身份枚举；诚实保持 unformulated，落终审文档+复活门槛）')
print('='*92)
print(""" 三者均【不升级】为 candidate_framework（无公设可升），也【不标 falsified】（无主张可否）。
 正确状态：维持 kind=unformulated_direction/status=unformulated，但在 00_研究立项/ 落《可建模性终审》，
 写明裁决码、经验封死边界（P01/P02）、主流领域地图与复活最小门槛（P04），并在书籍第86章总登记。
 18 体系处置由此闭环：S01–S14 各有审计结论，P03 升级为候选，P01/P02/P04 终审为空标签/零建模。
 算法联盟价值对称体现：敢建（P03）也敢判空（P01/P02/P04），绝不以编造公设冒充统一进度。UFT 仍 2/6。""")
