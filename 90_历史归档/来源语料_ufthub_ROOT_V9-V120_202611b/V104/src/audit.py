"""Conservative 369-row triage; preserve original claims and do not invent completion."""
import csv
from pathlib import Path
from collections import Counter

SUPPLEMENT_V92 = {
'H01':'用 Minkowski 号规写 UμUμ=-c²，并在 3 个惯性系中验证 v<c。',
'H02':'严格推导恒定圆柱螺旋的 κ、τ、ω、v 等式及全部适用条件。',
'H03':'对质量非零粒子检验 E²=p²c²+m²c⁴，不得预设实际三速度=c。',
'H04':'在真空 Maxwell 方程中检验自由传播的波矢、能流和偏振是否对应真实螺旋轨迹。',
'H05':'对非零轴向 Lorentz boost 计算三维挠率变化，寻找协变替代量。',
'H06':'构造相同轨迹对应不同 EM 场的反例；多速度探针反演设计矩阵需满秩。',
'H07':'从 qv×B 和相对论动量推出 ω=qB/(γm)，独立积分交叉核验。',
'H08':'从 p=γmv 推导纵向 γ³m dv/dt 与法向 γmv²κ，并检查单位。',
'H09':'从候选作用量导出 QCD SU(3) 色荷表示、跑动及禁闭的受控极限。',
'H10':'导出弱相互作用的手征性、混合角和中微子质量并与实验相符。',
'H11':'以平直时空强制弯曲路径及曲时空自由落体构造双向反例。',
'H12':'维度解析证明 c、κ、τ、ω 不含 M 量纲，不足以唯一构造 G。',
'H13':'给出独立测定的 κ* 与无量纲系数，不得以 G 反推尺度。',
'H14':'以 SI 基本维度证明 F⊥=γmv²κ，并排除不配维公式。',
'H15':'分别写 Frenet 联络、规范联络及 Levi-Civita 联络的变换定律。',
'H16':'完整说明是否引入优选系，并以实验界限约束 Lorentz 破缺。',
'H17':'对候选刚性世界线作用量求变分，排除幽灵和能量下界问题。',
'H18':'证明单速度反问题核的维度，并给出 3 个非共线速度差的满秩方案。',
'H19':'区分波函数时间相位 E/ħ 与轨道角频率，并给出可测连接。',
'H20':'独立预测电子质量和长度，而不是用康普顿长度定义回代质量。',
'H21':'从自旋群表示、交换统计及观测量恢复半整数自旋。',
'H22':'加入经典/量子辐射账本、Schott 项和反作用误差估计。',
'H23':'清楚定义 3 速度、4 速度、固有时及 Lorentz 因子，反例测试。',
'H24':'同时给出牛顿、Maxwell、GR、标准模型正确极限及无异常作用量。',
'H25':'规定磁场/速度扫描和 boost 的测量量、统计误差及拒绝域。',
'H26':'给出内部相位自由度的协变状态空间，说明它不等同于质心轨迹。',
'H27':'对有质量粒子检验 v→c 时 γ→∞，明确公设失效边界。',
'H28':'候选轨道频率在弱场独立推导 ω²=GM/R³ 并通过天文观测。',
'H29':'在无事后参数拟合下得到 GR+SM 之外可证伪的定量预言。',
'H30':'在干净环境重新运行代数、数值、ODE 与独立积分并记录失败。',
'H31':'在无循环前提下计算 G、强弱耦合并恢复重整化群行为。',
'H32':'给出量子几何动力学和可区别于经典描述的观测预言。',
}

SCOPE_NOTE='Automated evidence-class triage; NOT independent proof for each historic claim.'


def categorize(row):
    st=row['status_or_current_result'].upper()
    ident=row['id']
    if ident in {'A01','A02','A03','A07','A08','A09','A10','A11'}:
        return ('DIAGNOSTIC_CLOSED_GOAL_OPEN','旧公式错误/循环论证的诊断完成；原先承诺的第一性预测尚未获得')
    if ident in {'V101-008','V102-06','V103-364','V103-365','V103-368','V103-369'}:
        return ('OPEN_FOUNDATIONAL','需要连续模型、协变量子理论或无循环耦合的独立证明')
    if ident in {'H06','H27','I16','J03','J09','V94-006'}:
        return ('DIAGNOSTIC_CLOSED_GOAL_OPEN','反例或方法障碍已识别；原动力学或连续场证明仍未完成')
    if ident in {'H14','H15','H19','H20','V101-004'}:
        return ('CONDITIONAL_RESULT_ONLY','概念区分、量纲或反例在限定条件下成立')
    if ident=='H30':
        return ('MODEL_OR_SOFTWARE_ONLY','仅完成指定数学与程序原型验收')
    if ident=='V103-361':
        return ('CONDITIONAL_THEOREM','静态保守场无法补偿周期辐射；时变驱动仍需另行研究')
    if 'EXPERIMENT' in st or '实验' in st:
        return ('REQUIRES_REAL_EXPERIMENT','模拟和软件测试不能代替真实测量')
    if ('OPEN' in st or '开放' in st or '未解决' in st or '待' in st):
        return ('OPEN_RESEARCH','需按原验收条件补充证明或观测')
    if st in {'CLOSED_MATH','CLOSED_MATH_NO_GO'}:
        return ('DIAGNOSTIC_CLOSED_GOAL_OPEN','数学/反例审计已给出；不自动完成更高层物理目标')
    if any(k in st for k in ('NUMERIC','NUMERICAL','MODEL','PROTOTYPE','ENGINEERING','SOFTWARE','FINITE_TIME','LINEARIZED')):
        return ('MODEL_OR_SOFTWARE_ONLY','限定模型或工程测试；不得当作精确连续物理理论认证')
    if any(k in st for k in ('PROVEN','PROOF','MATH','CONDITIONAL','THEOREM','NO_GO','反例','不可能性','已否定','已验证','已澄清','维度形式')):
        return ('CONDITIONAL_RESULT_ONLY','已知数学/指定条件结论；仍需检查原验收目标范围')
    if any(k in st for k in ('BASELINE','KNOWN','ESTABLISHED','STANDARD','PHYSICS')):
        return ('KNOWN_BASELINE','已有物理知识基准，不等于新统一理论')
    return ('MANUAL_REVIEW_REQUIRED','历史标签范围不够明确，需独立补证')


def triage(src,dst):
    with open(src,encoding='utf-8-sig',newline='') as f:
        rows=list(csv.DictReader(f))
    assert len(rows)==369, f'Expected 369, found {len(rows)}'
    ids=[r['id'] for r in rows]
    # Historic ledger has 24 duplicated H01-H24 identifiers across V92 and V95.
    # Preserve original IDs, repair only new machine-readable canonical keys.
    assert len(set(ids))==345, 'Unexpected historical duplicate-ID pattern'
    out=[]
    for r in rows:
        group,note=categorize(r)
        canonical_id=(('V95-'+r['id']) if r['id'].startswith('H') and r['source_version']=='V95' else
                      ('V92-'+r['id']) if r['id'].startswith('H') and r['source_version']=='V91/V92' else r['id'])
        supplemental=(SUPPLEMENT_V92.get(r['id']) if r['source_version']=='V91/V92' else None)
        criterion=r['acceptance_criterion'] or supplemental
        assert criterion, f'Missing acceptance criterion for {canonical_id}'
        out.append({
            'canonical_id':canonical_id,'id':r['id'], 'issue':r['issue'], 'legacy_status':r['status_or_current_result'],
            'new_evidence_class':group,'completion_level':'NOT_CERTIFIED_AS_FULL_FOUR_FORCE_UNIFICATION',
            'independent_audit_note':note,
            'acceptance_criterion_unmodified':r['acceptance_criterion'],
            'supplemental_acceptance_if_missing':supplemental if not r['acceptance_criterion'] else '',
            'effective_acceptance_criterion':criterion,
            'source_version':r['source_version'],
        })
    assert len({r['canonical_id'] for r in out})==369,'canonical issue IDs must be unique'
    dst=Path(dst);dst.parent.mkdir(parents=True,exist_ok=True)
    with open(dst,'w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
    return Counter(x['new_evidence_class'] for x in out)
