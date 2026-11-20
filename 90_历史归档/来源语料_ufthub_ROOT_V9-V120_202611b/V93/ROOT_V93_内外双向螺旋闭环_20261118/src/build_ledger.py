import csv,json
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
old=json.loads((BASE/'ledger'/'V92_REFERENCE_147_original.json').read_text(encoding='utf-8'))
items=[
('环面内外运动坐标模型','MATH_PROVED','轨迹构造且具有正确欧氏半径与连续性'),
('空间周期闭合定理','MATH_PROVED','证明相位 mU,nU 同时为 2π 整数倍'),
('互素整数与最短原始周期','MATH_PROVED','证明 U=2π/gcd(m,n)'),
('半径由内向外往复次数','MATH_PROVED','证明原始周期内 n/g 次内外回环'),
('弧长参数化常速定理','MATH_PROVED','验证 |dr/dt|=v0 对所有正规点成立'),
('V=c 是否为粒子内部客观速度','OPEN_FOUNDATIONAL','给出 Lorentz 协变且不违背粒子谱的内部自由度'),
('内外角速度比','MATH_PROVED','推导 σ 与 Ω 的比值并数值交叉'),
('常角速度与常总速是否兼容','MATH_PROVED_NO_GO','非退化环面曲线 σ 随 u 变化'),
('曲率挠率全路径公式','MATH_PROVED','用三阶导数、叉积和行列式精确给出'),
('曲率零点处理','OPEN_DOMAIN_CASE','开发适用于全参数域的零曲率分段标架'),
('恒定总速度的法向加速度','MATH_PROVED','a=v0²κN 和 a·v=0'),
('SR 质量粒子的三维合力反演','MATH_PROVED_CONDITIONAL','F=γ m v0²κ'),
('质量粒子 beta=1 极限','MATH_PROVED_NO_GO','γ→∞ 且需求有限 κ 时 F 不有限'),
('沿路径磁场逆设计','MODEL_ONLY','导出局部 B，但未构造全局满足 Maxwell 的场'),
('完整 Maxwell 反演电磁装置','OPEN_ENGINEERING','实证全域无散度、线圈边界及轨道稳定'),
('考虑加速电荷的辐射反作用','OPEN_ENGINEERING','给出一致辐射损耗模型及数值积分'),
('匀强 B 下磁矢势环路积分','MATH_PROVED','独立积分和 Stokes 对照'),
('Wilson/AB 量子干涉读数','MODEL_ONLY','添加真实双臂干涉与相位包裹模型'),
('磁通是否仅由曲率挠率唯一决定','MATH_PROVED_NO_GO','同样投影面积但不同 n 可有不同 κ,τ'),
('自封闭是否导致磁通量自动量子化','MATH_PROVED_NO_GO','无额外边界量子条件的连续 B 反例'),
('三维闭环是否形成闭合类时曲线','MATH_PROVED_NO_GO','实验室 t(U)>t(0)；没有封闭时空世界线'),
('结型是否产生新的力常数','OPEN_FOUNDATIONAL','提出能量谱与量子数的独立方程'),
('Fáry–Milnor 总曲率下界检验','KNOWN_THEOREM_AND_NUMERIC','(2,3) trefoil K>4π 与数学定理一致'),
('有向总挠率与拓扑量子数','MATH_PROVED_COUNTEREXAMPLE','积分不需为 2π 整数倍'),
('85 位独立数值积分','NUMERIC_VERIFIED','mpmath 与 SciPy 路径长度和磁通交叉'),
('SI 量纲全配对','SOFTWARE_VERIFIED','40 个量 780 对和 32 个候选等式'),
('内部螺旋的 Lorentz 协变作用量','OPEN_FOUNDATIONAL','从新自由度对称作用量推出可测预测'),
('GR 与内部螺旋的统一导出','OPEN_FOUNDATIONAL','从作用量导出 Einstein 限制和观测'),
('SM 三规范群与自旋粒子谱','OPEN_FOUNDATIONAL','得到 SU3×SU2×U1、手征性及质量谱'),
('独立预言 G 与新力的实验确认','OPEN_FOUNDATIONAL_AND_EXPERIMENT','从不依赖旧 G 的参数推导和实测证伪')]
new=[dict(id=f'V93-{i:03d}',domain='内外往复螺旋闭环/相关场论',issue=issue,v93_status=status,acceptance_criterion=criterion,physical_discovery=False) for i,(issue,status,criterion) in enumerate(items,1)]
full={'baseline_version':'ROOT V92','baseline_count':old['total'],'v93_new_count':len(new),'total':old['total']+len(new),'baseline_original':old,'v93_new':new,'disclaimer':'CLOSED_MATH/VERIFIED belongs to mathematics or code only. Never infer four-force unification.'}
(BASE/'ledger'/'FULL_TRACKER_177.json').write_text(json.dumps(full,ensure_ascii=False,indent=2),encoding='utf-8')
with (BASE/'ledger'/'V93_NEW_30_ISSUES.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['id','domain','issue','v93_status','acceptance_criterion','physical_discovery']);w.writeheader();w.writerows(new)
with (BASE/'ledger'/'ALL_177_FLAT.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['id','issue','status_or_current_result','acceptance_criterion','source_version'])
    for item in old['legacy']+old['new']:
        w.writerow([item.get('id',''),item.get('issue',item.get('question','')),item.get('status',item.get('v92_audit_state','')),item.get('acceptance_criterion',item.get('v92_completion_means','')),'V91/V92'])
    for item in new:w.writerow([item['id'],item['issue'],item['v93_status'],item['acceptance_criterion'],'V93'])
print('Total',len(old['legacy'])+len(old['new'])+len(new))
