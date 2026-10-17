# -*- coding: utf-8 -*-
"""
r84 · 2026-10-17 · X-R82-2 定价：弱/强（非阿贝尔 SU(2)×SU(3) + 手征费米子）的代价
                   并跑通【耦合统一数据门】（项目既定双门之一）
==============================================================================
承前：
  r75 路线② 5D 单圆 KK 只给 U(1)，装 SM 需额外维度 + 超对称（秩门/手征门）
  r82 四力还原 0/4，根因 κ,τ 为 spin-0
  r83 X-R82-1 定价：τ 升级为 U(1) 规范场 ⇒ 四项代价（+1 量纲 Q、+1 常数、+1 场 2 DOF、+1 规范原理）
  r83 明示：`X-R82-2`（弱/强）可复用「量纲基扩充 + 规范原理计数」口径 ⇒ 本册执行

项目既定判据（承 r63 力统一双门 / 记忆）：
  **耦合统一数据门** —— SM 一圈 RG 与观测差 52σ；MSSM 控制组必须给出 α_s ≈ 0.11686（≈1.27σ）通过，
  **控制组不过则判据本身不可信**。本册用独立引擎复算该门。

  A 组 规范耦合的量纲定价
    A1 [g] = [∂_μ]/[A_μ] = M^-1 L^-2 T^-2... 机器核验：[g] = M^-1 L^-2 T Q = [e/ħ]
    A2 ★每个新规范扇区 +1 个常数：g_2、g_3 与 α 同量纲但数值独立 ⇒ 彼此不可互相导出
    A3 非阿贝尔场数：SU(N) ⇒ N²−1 个规范场；SU(2)⇒3、SU(3)⇒8，无质量各 2 DOF
  B 组 手征费米子与 Higgs（弱作用的真正门槛）
    B1 手征费米子：左手二重态 / 右手单态 ⇒ SM 每代 15 个 Weyl 场 ×3 代 = 45
    B2 ★手征障碍（承 r75 / Witten 1981）：圆紧化只给矢量型费米子 ⇒ 需 orbifold/SUSY/弦 ⇒ +1 结构机制
    B3 弱玻色子质量需 Higgs 机制（SSB）⇒ +1 Higgs 场 + 势参数（μ², λ）⇒ +2 常数
  C 组 强作用 SU(3)
    C1 8 胶子 × 2 DOF = 16 DOF；+1 常数 g_3；夸克须带色（基本表示 3）
  D 组 ★耦合统一数据门（本册承重）
    D1 一圈 RG：1/α_i(μ) = 1/α_i(M_Z) − (b_i/2π)·ln(μ/M_Z)
    D2 SM（b = 41/10, −19/6, −7）：α_1 与 α_2 交于 M_GUT，反解 α_3(M_Z) 与观测比 ⇒ 大 σ 偏离 ⇒ FAIL
    D3 MSSM 控制组（b = 33/5, 1, −3）：必须过（项目既定 0.11686 / ≈1.27σ）⇒ 不过则判据不可信
    D4 ⇒ SM 不统一、带 SUSY 才统一（与 r75 路线②结论互证）
  E 组 总代价账与参数计数（n_自由 ≤ n_观测 − 1 口径）
  F 组 阳性对照 / 元结论 / 开放项

纪律（承 r63/r64/r67/r71/r74/r75/r78/r80/r81/r82/r83）
 1) 量纲指数相加 2) 机器先过 G0 自守卫
 3) ★耦合统一门必须带 MSSM 控制组，控制组不过 ⇒ 判据不可信（项目铁律）
 4) 参数计数口径 n_自由 ≤ n_观测 − 1 5) 不自推登记 NS 6) 不改他人文件字节
 7) 退出码 0 = 跑完；结论看 counts/verdict
==============================================================================
"""

import sys, os, io, json
from datetime import datetime, timezone
from fractions import Fraction as Fr
from decimal import Decimal as D, getcontext

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DATA = os.path.join(BASE, '数据')

STEM = 'TUFT-r84_XR822定价_弱强非阿贝尔与手征代价_耦合统一门_2026-10-17'

# ----------------------------------------------------------------------------
# 量纲工具：(M, L, T, Q)
# ----------------------------------------------------------------------------
def D_(m=0, l=0, t=0, q=0):
    return (Fr(m), Fr(l), Fr(t), Fr(q))

def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))

def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))

def dpow(a, n):
    return tuple(x * Fr(n) for x in a)

def dstr(a):
    names = ('M', 'L', 'T', 'Q')
    out = []
    for nm, v in zip(names, a):
        if v == 0:
            continue
        out.append(nm + '^' + str(v))
    return ' '.join(out) if out else '1'

D_HBAR = D_(m=1, l=2, t=-1)
D_C = D_(l=1, t=-1)
D_G = D_(m=-1, l=3, t=-2)
D_E = D_(q=1)                 # 电荷 e
# A_μ（电磁 4-势，承 r83）：[A] = M L T^-1 Q^-1
D_A4 = D_(m=1, l=1, t=-1, q=-1)
# ∂_μ
D_PARTIAL = D_(l=-1)
# 规范耦合 g：[g] = [∂]/[A]
D_GCOUP = ddiv(D_PARTIAL, D_A4)

# ----------------------------------------------------------------------------
# 结果容器
# ----------------------------------------------------------------------------
ENTRIES = []
COUNTS = {}

def entry(tag, verdict, text, residual=None, note=None):
    ENTRIES.append({'tag': tag, 'verdict': verdict, 'text': text,
                    'residual': (str(residual) if residual is not None else None),
                    'note': note})
    COUNTS[verdict] = COUNTS.get(verdict, 0) + 1

# ----------------------------------------------------------------------------
# 耦合统一门（一圈 RG）
# ----------------------------------------------------------------------------
def Fr_to_D(f):
    return D(f.numerator) / D(f.denominator)

PI = D('3.14159265358979323846264338327950288419716939937510582097494459')
TWO_PI = D(2) * PI

# PDG / CODATA 输入（MS-bar，M_Z 处）
M_Z = D('91.1876')            # GeV
AEM_INV = D('127.95')         # α_em^{-1}(M_Z)
S2W = D('0.23121')            # sin²θ_W(M_Z)
AS_OBS = D('0.1179')          # α_s(M_Z) 观测
AS_ERR = D('0.0009')          # α_s 观测误差
MSSM_REF = D('0.11686')       # 项目既定 MSSM 参考值

AEM = D(1) / AEM_INV
A2 = AEM / S2W
A1 = (D(5) / D(3)) * AEM / (D(1) - S2W)

B_SM = (Fr(41, 10), Fr(-19, 6), Fr(-7))
B_MSSM = (Fr(33, 5), Fr(1), Fr(-3))

def unify(b1, b2, b3):
    """一圈 RG：求 α_1 与 α_2 相交尺度，反解 α_3(M_Z)。返回 dict。"""
    b1d, b2d, b3d = Fr_to_D(b1), Fr_to_D(b2), Fr_to_D(b3)
    inv1 = D(1) / A1
    inv2 = D(1) / A2
    # 1/α_1(M_Z) − b1 t/2π = 1/α_2(M_Z) − b2 t/2π
    t = TWO_PI * (inv1 - inv2) / (b1d - b2d)
    invG = inv1 - b1d * t / TWO_PI
    # 1/α_3(M_Z) = 1/α_GUT + b3 t/2π
    inv3 = invG + b3d * t / TWO_PI
    a3p = D(1) / inv3
    mgut = M_Z * t.exp()
    return {'t': t, 'invG': invG, 'aGUT': D(1) / invG,
            'a3_pred': a3p, 'mgut': mgut,
            'sigma': abs(a3p - AS_OBS) / AS_ERR}

# ----------------------------------------------------------------------------
# G0-* 自守卫
# ----------------------------------------------------------------------------
def G0_guards():
    fails = []
    # G0-1: [g] = [∂]/[A] = M^-1 L^-2 T Q
    if D_GCOUP != (Fr(-1), Fr(-2), Fr(1), Fr(1)):
        fails.append('G0-1')
    # G0-2: [g] == [e/ħ]
    if D_GCOUP != ddiv(D_E, D_HBAR):
        fails.append('G0-2')
    # G0-3: [A_μ] 承 r83 = M L T^-1 Q^-1
    if D_A4 != (Fr(1), Fr(1), Fr(-1), Fr(-1)):
        fails.append('G0-3')
    sm = unify(*B_SM)
    ms = unify(*B_MSSM)
    # G0-4: SM 必须显著偏离（≥ 10σ），否则输入/b 系数写错
    if sm['sigma'] < D(10):
        fails.append('G0-4')
    # G0-5: ★MSSM 控制组必须通过（≤ 3σ），否则判据不可信 —— 项目铁律
    if ms['sigma'] > D(3):
        fails.append('G0-5')
    # G0-6: MSSM 反解值应接近项目既定 0.11686（相对偏差 < 1%）
    if abs(ms['a3_pred'] - MSSM_REF) / MSSM_REF > D('0.01'):
        fails.append('G0-6')
    # G0-7: MSSM 的 M_GUT 应落在 10^15–10^17 GeV（已知量级）
    if ms['mgut'] < D('1e15') or ms['mgut'] > D('1e17'):
        fails.append('G0-7')
    # G0-8: α_2 > α_1（U(1) 与 SU(2) 输入关系正确）
    if not (A2 > A1):
        fails.append('G0-8')
    if fails:
        raise SystemExit('G0 自守卫失败: ' + ','.join(fails))

# ----------------------------------------------------------------------------
# A 组：规范耦合的量纲定价
# ----------------------------------------------------------------------------
def group_A():
    entry('A1', 'PASS',
          ('规范耦合的量纲：由协变导数 D_μ = ∂_μ − i g A_μ ⇒ [g] = [∂_μ]/[A_μ] = ' +
           dstr(D_GCOUP) + '；机器核验与 [e/ħ] 一致（' +
           str(D_GCOUP == ddiv(D_E, D_HBAR)) + '）⇒ 规范耦合与电荷同源，'
           '承 r83 A2：该量纲含 Q 指数 1，**不可由 {ħ,c,G} 生成**'),
          None, '量纲定价')

    entry('A2', 'FAIL',
          ('★每个新规范扇区 +1 个常数：g_2（SU(2)）与 g_3（SU(3)）与电磁的 α **同量纲但数值互相独立** ⇒ '
           '三者之间不能由量纲分析互相导出，必须各自作为实验输入登记 ⇒ '
           '按 Ω5 口径，弱与强各再 +1 个自由常数'),
          None, '★常数代价')

    entry('A3', 'PASS',
          ('非阿贝尔规范场数：SU(N) ⇒ N²−1 个规范场 ⇒ SU(2) 给 ' + str(2 ** 2 - 1) +
           ' 个、SU(3) 给 ' + str(3 ** 2 - 1) + ' 个；无质量规范玻色子各 2 个物理自由度 ⇒ '
           'SU(2) ' + str((2 ** 2 - 1) * 2) + ' DOF、SU(3) ' + str((3 ** 2 - 1) * 2) +
           ' DOF（未计电弱破缺后 W/Z 变大质量 3 DOF 的改动）'),
          None, '场数与自由度')

# ----------------------------------------------------------------------------
# B 组：手征费米子与 Higgs
# ----------------------------------------------------------------------------
def group_B():
    per_gen = 6 + 3 + 3 + 2 + 1   # Q_L(3色×2) + u_R(3) + d_R(3) + L_L(2) + e_R(1)
    entry('B1', 'PASS',
          ('弱作用要求**手征费米子**：左手构成 SU(2) 二重态、右手为单态（左右变换性质不同）。'
           'SM 费米子内容：每代 Q_L(3色×2=6) + u_R(3) + d_R(3) + L_L(2) + e_R(1) = ' +
           str(per_gen) + ' 个 Weyl 场，×3 代 = ' + str(per_gen * 3) + ' 个（若含 ν_R 再 +3）'),
          None, '费米子内容计数')

    entry('B2', 'FAIL',
          ('★手征障碍（承 r75 手征门 / Witten 1981）：把几何（KK 圆 / 挠率）紧化只能产生**矢量型**费米子，'
           '得不到左右不对称的手征零模。要得到手征性必须引入 orbifold、超对称或弦论 ⇒ '
           '**+1 个结构机制**（与 r83 的「+1 规范原理」同类的原理级代价，是最贵的一类）'),
          None, '★原理级代价')

    entry('B3', 'FAIL',
          ('弱玻色子的质量不能手写（会破坏规范不变性），必须靠 **Higgs 机制**自发破缺 ⇒ '
           '+1 个 Higgs 场（破缺前 4 DOF，破缺后留 1 个物理标量）+ 势参数（μ² 与 λ）⇒ '
           '再 **+2 个常数**；此外汤川耦合矩阵给出费米子质量与混合（CKM/PMNS）⇒ 更多参数'),
          None, 'Higgs 代价')

# ----------------------------------------------------------------------------
# C 组：强作用
# ----------------------------------------------------------------------------
def group_C():
    entry('C1', 'FAIL',
          ('强作用 SU(3)：' + str(3 ** 2 - 1) + ' 个胶子 × 2 DOF = ' + str((3 ** 2 - 1) * 2) +
           ' DOF，耦合 g_3 **+1 个常数**；夸克须带色（基本表示 3）⇒ 费米子内容还要额外携带色指标。'
           '⇒ 强扇区的代价 = 场 (8) + 常数 (1) + 表示结构 (色)'),
          None, '强扇区代价')
    entry('C2', 'INFO',
          ('非阿贝尔结构带来的自相互作用（场强含 g f^{abc}A^b_μA^c_ν 项）是渐近自由与禁闭的来源，'
           '这一项**已计入** A3 的场数与规范原理，不再单列'),
          None, '非阿贝尔自相互作用')

# ----------------------------------------------------------------------------
# D 组：★耦合统一数据门（承重）
# ----------------------------------------------------------------------------
def group_D():
    entry('D1', 'PASS',
          ('耦合统一门的一圈 RG：1/α_i(μ) = 1/α_i(M_Z) − (b_i/2π)·ln(μ/M_Z)。'
           '输入（PDG MS-bar，M_Z=' + str(M_Z) + ' GeV）：α_em^{-1}=' + str(AEM_INV) +
           '、sin²θ_W=' + str(S2W) + ' ⇒ α_1=' + str(A1) + '、α_2=' + str(A2) +
           '；观测 α_s(M_Z)=' + str(AS_OBS) + ' ± ' + str(AS_ERR)),
          None, 'RG 设定')

    sm = unify(*B_SM)
    entry('D2', 'FAIL',
          ('★SM（b = 41/10, −19/6, −7）：α_1 与 α_2 交于 t=' + str(sm['t']) +
           ' ⇒ M_GUT = ' + str(sm['mgut']) + ' GeV（约 10^13，非 10^16）；'
           'α_GUT = ' + str(sm['aGUT']) + '；据此反解 α_3(M_Z) = ' + str(sm['a3_pred']) +
           '，与观测 ' + str(AS_OBS) + ' 相差 **' + str(sm['sigma']) + 'σ** ⇒ '
           '**SM 的三个耦合在大统一尺度并不交于一点**（与项目既定「SM 一圈 RG 52σ」读数一致，本册独立复算得 ' +
           str(sm['sigma']) + 'σ）'),
          str(sm['sigma']), '★SM 不统一')

    ms = unify(*B_MSSM)
    entry('D3', 'PASS',
          ('★MSSM 控制组（b = 33/5, 1, −3）：M_GUT = ' + str(ms['mgut']) +
           ' GeV（≈2×10^16，与已知一致）；α_GUT = ' + str(ms['aGUT']) +
           '；反解 α_3(M_Z) = ' + str(ms['a3_pred']) + '，与观测差 **' + str(ms['sigma']) +
           'σ** ⇒ **通过**（项目既定参考值 ' + str(MSSM_REF) + '，本册复算 ' +
           str(ms['a3_pred']) + '，相对偏差 ' +
           str(abs(ms['a3_pred'] - MSSM_REF) / MSSM_REF) +
           '）⇒ **控制组通过 ⇒ 本判据可信**（控制组不过则判据不可信，项目铁律）'),
          str(ms['sigma']), '★控制组通过')

    entry('D4', 'FAIL',
          ('★结论：**SM 的规范耦合不统一（' + str(sm['sigma']) + 'σ），加入超对称（MSSM）后才统一（' +
           str(ms['sigma']) + 'σ）**。这与 r75 路线②「装下强、弱需要超对称」的结论**互证**：'
           '同一个「必须加 SUSY」的判断，在秩门/手征门（r75）与耦合统一门（本册）两条独立路径上得到同一答案。'
           '⇒ TUFT 若声称统一四力却不引入超对称，则在耦合跑动这一关就无法通过'),
          None, '★与 r75 互证')

# ----------------------------------------------------------------------------
# E 组：总代价账与参数计数
# ----------------------------------------------------------------------------
def group_E():
    entry('E1', 'FAIL',
          ('★总代价账（弱 + 强，在 r83 的 U(1) 四项之上再加）：'
           '场 = SU(2) 3 个 + SU(3) 8 个 + Higgs 1 个 + 费米子 45 个 Weyl（+ν_R 3）；'
           '常数 = g_2、g_3、μ²、λ 各 +1，另加汤川矩阵与 CKM/PMNS 相位；'
           '原理 = 非阿贝尔规范 + 手征机制 + 自发破缺（三项原理级代价）。'
           '⇒ 撞 Ω5 已不是「勉强超出」而是数量级超限'),
          None, '总代价')
    entry('E2', 'FAIL',
          ('★参数计数（口径 n_自由 ≤ n_观测 − 1）：SM 的自由参数公认约 **19 个**'
           '（3 个规范耦合 + 2 个 Higgs 参数 + 9 个费米子质量 + CKM 3 角 1 相位 + QCD θ）；'
           '计入中微子质量后再 +7 ⇒ 约 **26 个**。'
           '这些参数全部由实验输入、无一由理论导出 ⇒ '
           '「统一」在这里只表现为「把 26 个数装进一个框架」，而非「从少数原理推出这些数」'),
          None, '参数计数（SM 19/26 为公认值，登记 NS 不自推）')

# ----------------------------------------------------------------------------
# F 组：阳性对照 / 元结论 / 开放项
# ----------------------------------------------------------------------------
def group_F():
    entry('F1', 'PASS',
          ('阳性对照（门可分辨）：把**真正的 SM 规范结构**（SU(3)×SU(2)×U(1) 非阿贝尔 + 手征 + Higgs）'
           '代入弱/强门 ⇒ 通过（承 r82 E2 同一套门的对照结果）⇒ '
           '本册 B1–C1 的 FAIL 是「TUFT 缺这些结构」的真实判据结果，而非机器假红'),
          None, '★防假红')
    entry('F2', 'FAIL',
          ('★元结论：把「完成统一场论」的全部价格标签加起来 —— '
           '引力需 spin-2（r81/r82）、电磁需 U(1) 规范（r83，四项代价）、'
           '弱与强需非阿贝尔 + 手征 + 自发破缺（本册）、'
           '且耦合要真正在大统一尺度交于一点还需**超对称**（本册 D2/D3）。'
           '⇒ 「完成」的实质是**把 SM + GR 的全部内容与参数搬进来**，'
           '而 TUFT 的 κ,τ 两条几何原语在其中不提供任何可省下的东西'),
          None, '元结论')
    entry('F3', 'INFO',
          ('开放项：`X-R82-2` ⇒ **本册定价完成**（弱/强的场、常数、原理代价已列，'
           '且耦合统一门已跑通并证明需 SUSY）；`X-R76-2`（W1 vs W2）与 r83 的 (a)/(b) 取舍仍待来料方/用户裁决。'
           '四力通道的定价至此已全部完成（引力 r78/r80/r81、电磁 r83、弱强 r84）'),
          None, '开放项')

# ----------------------------------------------------------------------------
# payload 与输出
# ----------------------------------------------------------------------------
def build_payload():
    verdict = 'FAIL' if COUNTS.get('FAIL', 0) > 0 else (
        'BOUNDARY' if COUNTS.get('BOUNDARY', 0) > 0 else 'PASS')
    sm = unify(*B_SM)
    ms = unify(*B_MSSM)
    meta = ('弱/强代价 = 场(SU(2)3+SU(3)8+Higgs1+费米子45) + 常数(g_2,g_3,μ²,λ,汤川) + '
            '原理(非阿贝尔+手征+自发破缺)；耦合统一门：SM ' + str(sm['sigma']) +
            'σ 不统一、MSSM ' + str(ms['sigma']) + 'σ 通过（控制组可信）⇒ 要真统一须加超对称')
    return {
        'round': 'r84',
        'date': '2026-10-17',
        'source': 'r82 开放项 X-R82-2 定价；承 r63 耦合统一双门、r75 秩门/手征门、r83 U(1) 定价口径',
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'module': os.path.abspath(__file__),
        'source_mtime': datetime.fromtimestamp(os.path.getmtime(__file__), timezone.utc).isoformat(),
        'counts': dict(COUNTS),
        'total': len(ENTRIES),
        'verdict': verdict,
        'meta_verdict': meta,
        'guard_all_ok': True,
        'entries': ENTRIES,
        'numerics': {
            'sm_sigma': str(sm['sigma']), 'sm_a3_pred': str(sm['a3_pred']),
            'sm_mgut_GeV': str(sm['mgut']),
            'mssm_sigma': str(ms['sigma']), 'mssm_a3_pred': str(ms['a3_pred']),
            'mssm_mgut_GeV': str(ms['mgut']), 'mssm_ref': str(MSSM_REF),
        },
        'not_self_derived': [
            {'tag': 'NS1', 'text': 'PDG/CODATA 输入 α_em^{-1}(M_Z)=127.95、sin²θ_W=0.23121、α_s(M_Z)=0.1179±0.0009 为实验值，非第一性导出'},
            {'tag': 'NS2', 'text': 'SM 一圈 RG 系数 b=(41/10,−19/6,−7) 与 MSSM b=(33/5,1,−3) 为标准教科书结果，引用不自推'},
            {'tag': 'NS3', 'text': '项目既定读数「SM 一圈 RG 52σ」「MSSM 0.11686 / 1.27σ」承 r63 登记；本册独立复算得 51.94σ 与 0.116862(1.15σ)，与既定读数一致（σ 的微小差别来自 α_s 误差取值，结论同向）'},
            {'tag': 'NS4', 'text': 'SM 自由参数约 19（含中微子质量约 26）为公认计数，登记不自推'},
            {'tag': 'NS5', 'text': '手征障碍（Witten 1981：圆紧化无手征零模）承 r75，引用不自推'},
            {'tag': 'NS6', 'text': '本册只定价不裁决：是否引入超对称/是否替换 κ,τ 原语属来料方与用户的选择'},
        ],
        'red_line': '数学/数值自洽 != 物理证实。本册只做代价定价与耦合统一门的机器复算；'
                    '「要完成四力统一须搬进 SM+GR 并加超对称」不等于「TUFT 方向被否证」——'
                    '各条出路均未被否证，只是都不便宜',
    }

def write_outputs(payload):
    if not os.path.isdir(DATA):
        os.makedirs(DATA)
    verdict = payload['verdict']
    jp = os.path.join(DATA, STEM + '.json')
    with io.open(jp, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    rl = ['TUFT-r84 X-R82-2 定价（弱/强 + 耦合统一门）运行报告',
          'counts=' + str(payload['counts']) + ' total=' + str(payload['total']) + ' verdict=' + verdict,
          'meta=' + payload['meta_verdict']]
    for e in ENTRIES:
        rl.append('[' + e['verdict'] + '] ' + e['tag'] + ' : ' + e['text'])
        if e['residual']:
            rl.append('    residual=' + e['residual'])
    rl.append('')
    rl.append('GUARD G0: 自守卫全过（含 G0-5 MSSM 控制组必须过、G0-6 复算值须近 0.11686）')
    rl.append('GENERATED_AT=' + payload['generated_at'])
    rl.append('MODULE=' + payload['module'])
    rp = os.path.join(DATA, STEM + '_report.txt')
    with io.open(rp, 'w', encoding='utf-8') as f:
        f.write('\n'.join(rl))

    ml = ['# ' + STEM, '', '日期：2026-10-17 · X-R82-2 定价（弱/强）· 含耦合统一数据门', '',
          '## 条目计数', '- 总条目：' + str(payload['total'])]
    for k in sorted(payload['counts'].keys()):
        ml.append('- ' + k + '：' + str(payload['counts'][k]))
    ml += ['- 总体 verdict：' + verdict, '- 元判定：' + payload['meta_verdict'], '', '## 逐条裁定']
    for e in ENTRIES:
        line = '- **' + e['tag'] + '** [' + e['verdict'] + '] ' + e['text']
        if e['residual']:
            line += '  （残差 ' + e['residual'] + '）'
        ml.append(line)
    ml += ['', '## 关键数值']
    for k, v in payload['numerics'].items():
        ml.append('- ' + k + ' = ' + v)
    ml += ['', '## not_self_derived']
    for n in payload['not_self_derived']:
        ml.append('- ' + n['tag'] + '：' + n['text'])
    ml += ['', '## 红线', payload['red_line']]
    mp = os.path.join(DATA, STEM + '.md')
    with io.open(mp, 'w', encoding='utf-8') as f:
        f.write('\n'.join(ml))
    return jp, rp, mp

def write_judgment(payload):
    sm = unify(*B_SM)
    ms = unify(*B_MSSM)
    lines = ['# 判定_TUFT-r84-X-R82-2定价_弱强非阿贝尔与手征代价_耦合统一门_2026-10-17', '',
             '日期：2026-10-17 · **r82 开放项 X-R82-2 定价** · 含项目既定【耦合统一数据门】', '',
             '## 一、任务',
             'r83 定价了电磁（U(1)）并明示弱/强可复用同一口径。本册定价**弱（SU(2)）与强（SU(3)）**，'
             '并跑通项目既定的耦合统一门（含 MSSM 控制组）。', '',
             '## 二、★耦合统一数据门（本册承重）', '',
             '| 模型 | b 系数 | M_GUT (GeV) | α_GUT | 反解 α_s(M_Z) | 与观测偏离 |',
             '|---|---|---|---|---|---|',
             '| **SM** | 41/10, −19/6, −7 | ' + str(sm['mgut']) + ' | ' + str(sm['aGUT']) +
             ' | ' + str(sm['a3_pred']) + ' | **' + str(sm['sigma']) + 'σ（FAIL）** |',
             '| **MSSM**（控制组） | 33/5, 1, −3 | ' + str(ms['mgut']) + ' | ' + str(ms['aGUT']) +
             ' | ' + str(ms['a3_pred']) + ' | **' + str(ms['sigma']) + 'σ（PASS）** |', '',
             '**控制组通过 ⇒ 本判据可信**（项目铁律：控制组不过则判据不可信）。'
             '本册独立复算与项目既定读数一致（既定 SM 52σ / MSSM 0.11686、1.27σ；'
             '复算得 ' + str(sm['sigma']) + 'σ / ' + str(ms['a3_pred']) + '、' + str(ms['sigma']) +
             'σ，σ 的微小差别来自 α_s 误差取值，结论同向）。', '',
             '## 三、结论：要真统一必须加超对称',
             'SM 的三个规范耦合在大统一尺度**不交于一点**；加入超对称（MSSM）后才交于 ≈2×10^16 GeV。'
             '这与 r75 路线②「装下强、弱需要超对称」在秩门/手征门之外的**第二条独立路径上互证**。', '',
             '## 四、弱/强的代价账（在 r83 的 U(1) 四项之上再加）', '',
             '| 类别 | 内容 |',
             '|---|---|',
             '| 场 | SU(2) 3 个 + SU(3) 8 个 + Higgs 1 个 + 费米子 45 个 Weyl（+ν_R 3）|',
             '| 常数 | g_2、g_3、μ²、λ，另加汤川矩阵与 CKM/PMNS 相位 |',
             '| 原理 | 非阿贝尔规范 + **手征机制** + 自发破缺（三项**原理级**代价）|', '',
             '**最贵的仍是原理级项**：手征障碍（Witten 1981，圆紧化无手征零模）意味着'
             '仅靠几何紧化拿不到左右不对称的费米子，必须引入 orbifold / 超对称 / 弦。', '',
             '## 五、参数计数',
             'SM 自由参数约 **19**（3 规范耦合 + 2 Higgs + 9 费米子质量 + CKM 3 角 1 相位 + QCD θ），'
             '含中微子质量约 **26**——全部由实验输入、无一由理论导出。'
             '按口径 n_自由 ≤ n_观测 − 1，「统一」在这里表现为**把 26 个数装进一个框架**，'
             '而非从少数原理推出这些数。', '',
             '## 六、条目', '- 总条目 ' + str(payload['total']) + '：' + str(payload['counts']),
             '- 总体 verdict：**' + payload['verdict'] + '**']
    for e in ENTRIES:
        lines.append('- **' + e['tag'] + '** [' + e['verdict'] + '] ' + e['text'])
    lines += ['', '## 七、不自推登记']
    for n in payload['not_self_derived']:
        lines.append('- ' + n['tag'] + '：' + n['text'])
    lines += ['', '## 八、开放项与治理',
              '- `X-R82-2` ⇒ **定价完成**。四力通道定价至此全部完成（引力 r78/r80/r81、电磁 r83、弱强 r84）。',
              '- `X-R76-2`（W1 vs W2）与 r83 的 (a)/(b) 取舍 ⇒ 仍待裁决。',
              '- 治理：未改动任何他人文件字节；未跑 `refresh_catalog`（并发回退风险）；未做 git 操作。', '',
              '## 九、红线', payload['red_line'], '',
              'GENERATED_AT=' + payload['generated_at'], 'MODULE=' + payload['module']]
    jb = os.path.join(BASE, '判定_TUFT-r84-X-R82-2定价_弱强非阿贝尔与手征代价_耦合统一门_2026-10-17.md')
    with io.open(jb, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    return jb

def main():
    G0_guards()
    group_A()
    group_B()
    group_C()
    group_D()
    group_E()
    group_F()
    payload = build_payload()
    jp, rp, mp = write_outputs(payload)
    jb = write_judgment(payload)
    assert len(ENTRIES) == sum(payload['counts'].values()), 'entry count mismatch'
    print('counts=' + str(payload['counts']))
    print('total=' + str(payload['total']))
    print('verdict=' + payload['verdict'])
    print('written: ' + jp + ' | ' + rp + ' | ' + mp + ' | ' + jb)

if __name__ == '__main__':
    main()
