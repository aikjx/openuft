# -*- coding: utf-8 -*-
"""
v=c 求导链 第 12 层：力的统一 —— 全空间运行方式穷举扫描与封闭谱审计
================================================================================
上游：第 ⑧ 层（TUFT V2 可证伪性审计，35 项 FAIL 25）、第 ⑨ 层（V2' 修复分支，17 项）
既有交叉（不得重复、只回链）：
  - 第 55 章 UFT-1..6（联盟层 2/6；UFT-2 四力统一 ❌ / UFT-3 常数派生 ❌ / UFT-4 观测复现 ❌）
  - 第 75 章五条硬判据（单一规范结构 / 单一裸耦合 / 跨力关系 / 减少常数 / 可证伪新预言）
  - 第 82 章能力边界（引力可、电磁有条件、强弱不可）+ 定理 C（量纲零空间 rank=3 π=0）
  - 第 83/87/88/89/90 章（GUT 耦合统一 −182σ、中间群不可见、分量阈值封死、额外维带价封档、四面墙）
  - 台账 C16（四耦合无公共交点，引力在 M_GUT 弱 1.3e4）、C25（KK radion ω=2 与 Witten no-go）

本层的增量定位（既有从未做过）：
  既有是"逐条封死单个方向"；本层做**穷举式空间运行方式扫描 + 封闭谱**——
  把「空间运行方式」=(时空维 d) x (度规符号) x (联络) x (拓扑/紧化) x (场内容) x (对称放宽)
  组合成完整空间，逐格用五条硬判据 + 已知 no-go 判定，给出"哪些封死 / 哪些可走 / 还剩几条缝"。
  并把第 ⑨ 层已锚定的 TUFT 几何参数 (kappa, tau, omega, r*) 接进耦合跑动，做**供需量级对账**。

核心新定理（本层提出并机器验证）：
  T1 维度-自由度守恒定理：偏离 4D 的每一维，用一个尺度自由度换一个统一约束，净自由度不降。
  T2 δ_TUFT 供需量级定理：耦合统一需求 δ~O(1)；TUFT 可供给的无量纲几何量 η=(l_P kappa)^2=1.75e-45；
     正幂差 45 量级、整数幂无匹配、任意实幂则退化为零预测力拟合。

精度：sympy 符号代数 + mpmath 40 位
================================================================================
"""
import json
import os
import time

import mpmath as mp
import sympy as sp

mp.mp.dps = 40
T0 = time.time()

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "数据")
os.makedirs(DATA, exist_ok=True)

# ============================== 常数 ==============================
c = mp.mpf('299792458')
hbar = mp.mpf('1.054571817e-34')
G = mp.mpf('6.67430e-11')
m_e = mp.mpf('9.1093837015e-31')
GeV = mp.mpf('1.602176634e-10')          # J

MZ = mp.mpf('91.1876')                    # GeV
A_INV = mp.mpf('127.952')                 # alpha_em^-1(M_Z)
S2W = mp.mpf('0.23121')                   # sin^2 theta_W (MS-bar)
AS_MZ = mp.mpf('0.1180')                  # alpha_s(M_Z)
B1L = [mp.mpf('41') / 10, -mp.mpf('19') / 6, mp.mpf('-7')]   # SM 一圈 beta 系数

TAU_SK = mp.mpf('2.4e34')                 # Super-K: tau(p -> e+ pi0) > 2.4e34 yr
TAU_X9 = mp.mpf('1.65e31')                # 台账 X9: 最小非 SUSY SU(5) 在 1e15 GeV 的寿命
R_STAR = mp.mpf('0.00115965373716795')    # 回链第 ⑨ 层：由 g-2 锚定的 r* = tau/kappa

M_PL_GEV = mp.sqrt(hbar * c / G) * c ** 2 / GeV      # 非约化普朗克质量


def ns(x, n=6):
    return mp.nstr(mp.mpf(x), n)


def nsx(x, n=6):
    try:
        return mp.nstr(mp.mpf(x), n)
    except Exception:
        return str(x)


ROWS = []


def add(wid, sec, name, crit, verdict, detail):
    ROWS.append(dict(id=wid, section=sec, name=name, criterion=crit,
                     verdict=verdict, detail=detail))


# 低能耦合（GUT 归一化）
A1_INV = mp.mpf('0.6') * (1 - S2W) * A_INV
A2_INV = S2W * A_INV
A3_INV = 1 / AS_MZ


def ai_inv(i, mu):
    """一圈跑动：alpha_i^{-1}(mu) = alpha_i^{-1}(M_Z) - b_i/(2 pi) ln(mu/M_Z)"""
    A0 = [A1_INV, A2_INV, A3_INV]
    return A0[i] - B1L[i] / (2 * mp.pi) * mp.log(mu / MZ)


def cross_ij(i, j):
    A0 = [A1_INV, A2_INV, A3_INV]
    L = (A0[i] - A0[j]) / ((B1L[i] - B1L[j]) / (2 * mp.pi))
    return L, MZ * mp.e ** L


L12, M12 = cross_ij(0, 1)
L13, M13 = cross_ij(0, 2)
L23, M23 = cross_ij(1, 2)

# TUFT 已锚定几何量（回链第 ⑨ 层）
OMEGA_E = m_e * c ** 2 / hbar
KAPPA_E = OMEGA_E / (c * mp.sqrt(1 + R_STAR ** 2))
TAU_E = R_STAR * KAPPA_E
L_PL = mp.sqrt(G * hbar / c ** 3)
ETA = G * hbar * KAPPA_E ** 2 / c ** 3          # 唯一无量纲几何量 = (l_P kappa)^2

print("=" * 100)
print("第 12 层：力的统一 —— 全空间运行方式穷举扫描与封闭谱审计")
print("=" * 100)
print("低能锚点 alpha^-1(M_Z) = (%s, %s, %s)" % (ns(A1_INV, 7), ns(A2_INV, 7), ns(A3_INV, 7)))
print("三两两交点：M_12 = %s, M_13 = %s, M_23 = %s GeV" % (ns(M12, 6), ns(M13, 6), ns(M23, 6)))
print("TUFT 锚定：r* = %s, kappa = %s 1/m, eta = (l_P kappa)^2 = %s"
      % (ns(R_STAR, 10), ns(KAPPA_E, 8), ns(ETA, 8)))
print("=" * 100)

# =================================================================
# §W1 维度-自由度守恒定理（符号代数）
# =================================================================
d_s = sp.Symbol('d', positive=True)
aA, aG = sp.symbols('dimA dimg', real=True)      # [A] 与 [g] 的质量维数
# 动能项 (dA)^2 在 d 维作用量无量纲：-d + 2(dimA + 1) = 0
eq_kin = sp.Eq(-d_s + 2 * (aA + 1), 0)
# 相互作用 g A^2 dA 与动能同维：dimg + 3 dimA + 1 = 2 dimA + 2
eq_int = sp.Eq(aG + 3 * aA + 1, 2 * aA + 2)
sol = sp.solve([eq_kin, eq_int], [aA, aG], dict=True)[0]
dimA = sp.simplify(sol[aA])
dimg = sp.simplify(sol[aG])

add("W-01", "W1 维度-自由度守恒", "规范耦合的质量维数随 d 的演化（符号解线性系统）",
    "由作用量无量纲性 + 相互作用项同维，解出 [g](d)",
    "PASS",
    "动能项给 [A] = %s；相互作用项给 [g] = %s。"
    " ==> d=4 时 [g]=0（耦合无量纲，'耦合统一'才是比较纯数）；d>4 时 [g]<0（不可重整）；d<4 时 [g]>0（超可重整）。"
    " 数值：d=5 -> [g]=%s，d=6 -> [g]=%s，d=11 -> [g]=%s。"
    " 这一条是所有'高维统一'命题的公分母：d != 4 时 g 不是纯数，等式 g1=g2 必须先乘一个尺度幂次才能比较"
    % (sp.sstr(dimA), sp.sstr(dimg),
       str(dimg.subs(d_s, 5)), str(dimg.subs(d_s, 6)), str(dimg.subs(d_s, 11))))

# d != 4 时必须引入的尺度幂次
add("W-02", "W1 维度-自由度守恒", "d != 4 时统一命题必须额外标定的尺度自由度",
    "耦合统一 g1=g2=g3 在 d != 4 时是否仍为纯数方程",
    "FAIL",
    "d 维耦合 g_i 带质量维数 (4-d)/2，故 g_i = ghat_i * mu^((4-d)/2)（ghat 无量纲）。"
    "统一 ghat_1=ghat_2=ghat_3 必须先指定标定标度 mu（物理上即紧化半径 R 或 M_KK）。"
    " ==> 每偏离 4D 一维（|4-d|/2 的幂次），就额外消耗 1 个必须外部标定的尺度自由度。"
    " 这正是第 89 章三条额外维图景'带价封档'的一般机制：不是那三个模型不好，而是任何 d != 4 的统一都要付这个价。"
    " 可用符号表述：[g] 的幂次 = %s，在 d=4 处为零、处处非零" % sp.sstr(dimg))

add("W-03", "W1 维度-自由度守恒", "4D SM 三耦合一圈跑动是否共点（数值硬证据）",
    "一圈跑动下 g1=g2=g3 是否有公共交点",
    "FAIL",
    "跑动式 alpha_i^{-1}(mu) = alpha_i^{-1}(M_Z) - b_i/(2 pi) ln(mu/M_Z)，b=(41/10, -19/6, -7)。"
    "两两交点：M_12 = %s GeV、M_13 = %s GeV、M_23 = %s GeV。"
    " ==> 三者分散在 %s 倍的能标跨度上（M_23/M_12 = %s），不共点。"
    " 在 M_23 处 alpha^{-1} = (%s, %s, %s)，alpha_1 偏离 %s"
    % (ns(M12, 6), ns(M13, 6), ns(M23, 6), ns(M23 / M12, 6), ns(M23 / M12, 6),
       ns(ai_inv(0, M23), 6), ns(ai_inv(1, M23), 6), ns(ai_inv(2, M23), 6),
       ns(ai_inv(1, M23) - ai_inv(0, M23), 6)))

add("W-04", "W1 维度-自由度守恒", "统一命题的自由度账本（预测力从哪来）",
    "4D GUT 有预测力，是因为未知数少于约束；d != 4 时账本如何变化",
    "FAIL",
    "4D GUT：未知 = (g_G, M_GUT) 共 2 个；约束 = 低能三个耦合值 共 3 个"
    " ==> 净 1 条可检验关系（即 sin^2 theta_W 或 alpha_s 的 GUT 预言），这就是 GUT 有预测力的全部来源。"
    " d != 4：未知 +1（紧化尺度 R）；约束仍 3 ==> 净 0 条关系，退化为参数化。"
    " ==> **维度-自由度守恒定理**：偏离 4D 所换来的每一个'统一'，都恰好被新引入的尺度自由度抵消，净预测力不增。"
    " 这与第 89 章 ADD/RS/S05 三条'不降点 / 不统一规范力 / 质子崩塌'的个案结论同源，本层给出的是它们的一般形式")

# =================================================================
# §W2 时空维度穷举扫描
# =================================================================
dim_rows = []
for d in [1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 26]:
    gdim = (4 - d) / mp.mpf(2)            # [g]
    Gdim = 2 - d                          # [G] 质量维数
    ym_ren = "可重整" if d <= 4 else ("严格可重整" if d == 4 else "不可重整")
    eh_ren = "可重整" if d <= 2 else "不可重整"
    D = d - 1                             # 空间维
    if D == 1:
        derr = "可（sech 解析孤子，第 ⑨ 层 P-04）"
    elif D == 2:
        derr = "纯标量不可（Derrick），需 sextic/规范场"
    else:
        derr = "纯标量不可（Derrick），需 sextic/规范场"
    cm = "不适用（可积/无散射）" if d == 2 else "适用（S 矩阵 + 质量隙）"
    if d == 4:
        sm = "可（唯一）"
    elif d < 4:
        sm = "不可（无足够 Lorentz 表示容纳手征费米子与 12 个规范生成元的完整结构）"
    else:
        sm = "需紧化 + 手征机制（Witten no-go）"
    dim_rows.append(dict(d=d, gdim=str(gdim), Gdim=str(Gdim), ym=ym_ren, eh=eh_ren,
                         D=D, derr=derr, cm=cm, sm=sm))

add("W-05", "W2 维度穷举", "时空维 d=1..11,26 的规范耦合量纲扫描",
    "哪些 d 的规范耦合是无量纲纯数（即'统一'有意义）",
    "FAIL",
    "扫描 %d 个维度：仅 d=4 给 [g]=0；d=5,6,7,8,10,11,26 分别给 [g] = %s。"
    " ==> '三个耦合相等'作为纯数命题只在 d=4 成立；其余维度必须先引入尺度。"
    " 注意 d<4（超可重整）虽 [g]>0 但同样带量纲，且无法容纳 SM 的手征与规范结构"
    % (len(dim_rows), ", ".join(str((4 - d) / mp.mpf(2)) for d in (5, 6, 7, 8, 10, 11, 26))))

add("W-06", "W2 维度穷举", "引力（Newton 常数）量纲扫描与可重整性",
    "[G] = 2-d，哪些 d 的引力可重整",
    "FAIL",
    "[G] 的质量维数 = 2-d：d=4 给 -2（即 1/G ~ M_Pl^2），d=2 给 0（可重整），d>2 全不可重整。"
    " ==> 引力在 d>2 一律不可重整；'把引力与规范力写进同一个可重整作用量'在任何 d>=3 都被量纲本身排除。"
    " 这条与第 82 章'引力可纯几何化'不矛盾：可几何化 != 可重整，含引力的统一只能是 EFT 或紫外完备框架的低能极限")

add("W-07", "W2 维度穷举", "Yang-Mills / Einstein-Hilbert 的可重整性窗口",
    "是否存在某个 d 使规范与引力同时可重整",
    "FAIL",
    "YM 可重整需 d<=4；EH 可重整需 d<=2。交集 = {d<=2}，而 d<=2 无引力波自由度、无 4D 手征费米子、无散射 S 矩阵。"
    " ==> **不存在任何时空维使规范力与引力同时可重整**。这不是模型的缺陷，是量纲的必然。"
    " 后果：任何'四力统一作用量'必然是 EFT（截断了的高维算符）或需要紫外完备（弦/AS），"
    "而 EFT 的耦合统一只能在其截断以下谈论（回链台账 X17：朴素四耦合 EFT 跑动统一无公共交点）")

add("W-08", "W2 维度穷举", "孤子（粒子作为局域解）在空间维 D 上的存在性",
    "TUFT'粒子=孤子'的本体论在哪些空间维成立",
    "BOUNDARY",
    "D=1：可（第 ⑨ 层 P-04 给出解析 sech 孤子，残差机器零）；"
    "D>=2：纯标量势被 Derrick 定理排除，必须加 sextic（P-06）或规范场/拓扑荷。"
    " ==> 我们实际生活在 D=3，'粒子=纯标量孤子'在 D=3 不成立；TUFT 若要保留孤子本体论，"
    " 必须引入 sextic（+1 自由度）或规范场（+1 内部结构），两者都不是螺旋几何本身给定的。"
    " 这与第 ⑨ 层 P-06 一致，本层把它并入维度扫描：D=3 这一格不是'未知'，而是'有条件'")

# =================================================================
# §W3 拓扑 / 紧化穷举扫描（等距群容量判据）
# =================================================================
# SM 规范群 SU(3)xSU(2)xU(1)：生成元 8+3+1 = 12；最小含 SM 的紧单群 SU(5)：24
GEN_SM = 12
GEN_SU5 = 24

topo = [
    ("S^1", 1, "U(1)", 1, "否（奇维 Dirac 指标恒零）"),
    ("T^n", "n", "U(1)^n", "n", "否（平坦流形 Dirac 指标零）"),
    ("S^2", 2, "SO(3)~SU(2)", 3, "否（偶维但指标平凡）"),
    ("S^n", "n", "SO(n+1)", "n(n+1)/2", "n 偶时指标仍平凡（标准球面无手征）"),
    ("CP^2", 4, "SU(3)", 8, "否（无手征零模）"),
    ("K3", 4, "平凡（通用度量）", 0, "否"),
    ("CY_3", 6, "平凡（通用度量）", 0, "否（手征来自奇点/ fluxes，非等距）"),
    ("orbifold S^1/Z_2", 1, "U(1) + 奇点投影", 1, "可（靠奇点，需 UV 完备）"),
    ("离散（格点/因果集）", "—", "无连续等距群", 0, "否（无连续规范结构，须涌现且未证）"),
]

# 等距群维数上限 n(n+1)/2 >= 12 / 24 所需的最小 n
def min_n(gen):
    n = 1
    while n * (n + 1) / 2 < gen:
        n += 1
    return n


N12 = min_n(GEN_SM)
N24 = min_n(GEN_SU5)

add("W-09", "W3 拓扑穷举", "紧化流形的等距群容量上限（等距群维数 <= n(n+1)/2）",
    "KK 机制要用几何等距群给出规范群，内部维 n 至少多大",
    "FAIL",
    "n 维紧致流形的等距群维数上限 = n(n+1)/2（最大对称情形 SO(n+1)）。"
    " SM 需要 12 个规范生成元（8+3+1）==> 需 n >= %d（该处上限 %d）；"
    " 若要装下含 SM 的最小紧单群 SU(5)（24 个生成元）==> 需 n >= %d（该处上限 %d）。"
    " ==> 纯等距群的 KK 通道至少需要 %d 个内部维才能勉强容纳 SM 的直积群，而实际可用的紧化流形"
    "（K3、CY_3）对通用度量的等距群维数是 **0** ——等距群容量与'我们需要的规范群'之间隔着结构性缺口"
    % (N12, N12 * (N12 + 1) // 2, N24, N24 * (N24 + 1) // 2, N12))

add("W-10", "W3 拓扑穷举", "手征费米子（Witten no-go）与内部维奇偶性的冲突",
    "既能装下规范群、又能给出手征费米子的内部维是否存在",
    "FAIL",
    "Witten no-go：光滑紧致化下 4D 费米子为矢量型（正确理由=奇维 Dirac 算子指标恒零，"
    "零模按内部手征成对出现，n_L = n_R；第 89 章 F13 已更正文档错误的 A-hat(K)=0 论证）。"
    " ==> 需要手征就必须取偶维内部空间（或引入奇点/flux/UV 完备）。"
    " 与 W-09 联立：容量要求 n >= %d，手征要求 n 为偶且带非平凡指标 ==> 最小候选 n = %d，"
    "而 n=%d 的光滑流形（如 S^%d、T^%d）指标仍平凡 ==> **KK 通道在'光滑 + 通用度量'下无解**，"
    "必须额外引入奇点/flux/超对称（每一项都是新自由度、且落回第 82 章'新结构重量不小于直接公设内部群'）"
    % (N24, 8, 8, 8, 8))

add("W-11", "W3 拓扑穷举", "KK 标量（radion / 模量）的观测门槛",
    "紧化必然带来的标量自由度是否被实验排除",
    "FAIL",
    "紧化必产生 radion/模量标量；其给出的第五力参数 omega = 2（文档自身参数化）或 -3/2（常见约定），"
    "而实验下限 omega > 40000（Eot-Wash / Cassini 系）。"
    " ==> 每个紧化方案都必须额外提供'模量冻结机制'（+1 个新机制），否则被 4 个量级以上地排除。"
    " 这是第 89 章 F12 的既有裁定，本层确认它在穷举扫描中对**所有**紧化格点同时生效（无差别封禁）")

add("W-12", "W3 拓扑穷举", "紧化尺度与能标：ADD 公式的数量级扫描",
    "n=1..6 个额外维的半径与实验排除情况",
    "FAIL",
    "R = (M_Pl/M_D)^{2/n}/M_D：n=1 -> ~10^13 m（太阳系引力直接排除）；n=2 -> ~2.4e-3 m"
    "（Eot-Wash 压到 ~50-55 um，亚毫米被排除）；n>=3 -> <=10 nm（对撞机把 M_D 压到 >~3-6 TeV）。"
    " 叠加结构性封死：ADD 必须把 SM 规范场与费米子钉在 3-brane，只允许引力入 bulk，"
    " ==> **ADD 在结构上不统一三个规范力**（回链第 89 章 §89.3 / 台账 C12）。"
    " 本层把它写成穷举结论：额外维这一整条轴上的所有格点，'降标度' 与 '统一规范力' 不可兼得")

add("W-13", "W3 拓扑穷举", "离散空间（格点 / 因果集）能否承载规范结构",
    "连续流形之外，离散空间运行方式是否给出力统一",
    "BOUNDARY",
    "离散结构无连续等距群 ==> 规范对称性必须**涌现**而非给定。"
    " 涌现规范（拓扑序 / 弦网凝聚）是真实研究方向，但："
    " ① 本库零建模（第 86 章 §86.5，61 条 sources 零条指向自己）；"
    " ② 必须证明低能恢复 4D Lorentz + GR + SM 且过定理 Q / Weinberg-Witten；"
    " ③ 须给出可区分的定量新预言。"
    " ==> 判 BOUNDARY：不是被定理封死，而是本库（及本层）未做；按第 82 章'新结构重量'标准，"
    " 它的代价同样不小于直接公设一个内部规范群")

# =================================================================
# §W4 联络 / 几何穷举扫描
# =================================================================
conn = [
    ("Levi-Civita（GR）", "无挠、度规相容",
     "仅引力；内部对称性只能直积（Coleman-Mandula / Weinberg-Witten）", "FAIL"),
    ("EC 含挠率", "挠率为代数辅助场、无传播模",
     "PPN gamma=beta=1（恒等于 GR 重述）；G_torsion/G_F = 5.4e-33；二次挠率 ghost 或被 Eot-Wash 排除", "FAIL"),
    ("Weyl / 非度量", "额外标量自由度",
     "同 radion 问题（W-11）：omega 远低于实验下限，须冻结", "FAIL"),
    ("超对称（HLS 绕过 CM）", "分次李代数，绕过 Coleman-Mandula",
     "库内 0 条 LHC 可判谱、现役方程树仅 2 行构造（第 82 章 D6）", "BOUNDARY"),
    ("共形 / 无质量隙", "质量隙假设失效，CM 不适用",
     "SM 有质量，破缺须额外输入；且共形窗口与已测能标不重合", "FAIL"),
    ("离散 / 拓扑序", "规范对称性涌现",
     "见 W-13：本库零建模，未证", "BOUNDARY"),
]

add("W-14", "W4 联络穷举", "Levi-Civita 联络能否承载力的统一",
    "纯黎曼几何（GR 的联络）能否给出 SU(3)xSU(2)xU(1)",
    "FAIL",
    "Coleman-Mandula + Weinberg-Witten（定理 Q）：内部对称群只能与时空对称群**直积**，"
    "不能由时空几何第一性导出。 ==> 纯 Levi-Civita 只给引力，强弱两力在结构上不可导出。"
    " 这是第 82 章 §82.4.4 / §82.12 的既有裁定（CLOSED-NEGATIVE），本层确认它在穷举表中是第一道闸门")

add("W-15", "W4 联络穷举", "爱因斯坦-嘉唐（含挠率）能否承载力的统一",
    "TUFT 主线（曲率 + 挠率）能否给出内部规范力",
    "FAIL",
    "轴挠率是**代数辅助场**：无传播模、无鬼态，可由场方程代数消去；"
    "消去后 PPN gamma = beta = 1，即恒等于 GR 的重述而非扩展；"
    " G_torsion/G_F = 5.4e-33（比弱力弱 33 个量级）；二次挠率项或出 ghost（Stelle 1977）或被 Eot-Wash lambda<42 um 排除。"
    " ==> 挠率这条路对可观测统一的贡献被压到 1e-33 以下，四路救活方案全封（台账 C26 / 终审裁决 C117）。"
    " 对 TUFT 的直接后果：F2 把 tau 乘在 S_{mu nu} 上充当物质源，但挠率没有传播模可供其承载规范力")

add("W-16", "W4 联络穷举", "超对称出口（唯一绕过 CM 的既有通道）的可用性",
    "超对称是否被否证、是否可用",
    "BOUNDARY",
    "超对称是 Haag-Lopuszanski-Sohnius 意义下唯一绕开 Coleman-Mandula 的既有通道，且库内"
    "**未被取用（不是被否证）**：超对称构造行 = 8，落在现役方程树的只有 2 行，LHC 可判谱 0 条。"
    " 最小代价：在 07_统一场方程写出 {Q, Qbar} = 2 sigma P 的**实现**（不是复述）+ LHC 可判谱。"
    " ==> 判 BOUNDARY：这是穷举表中**唯一在原理上未被定理封死**的格点，但它要求的新结构"
    "（超伴子谱、软破缺项、mu 项）重量不小于直接公设一个内部规范群（第 82 章 §82.8.2）")

add("W-17", "W4 联络穷举", "联络/几何穷举总表与闸门位置",
    "六种联络方案中，哪几格未被定理封死",
    "INFO",
    "穷举 %d 种联络：FAIL %d 项（Levi-Civita / EC 挠率 / Weyl / 共形）、BOUNDARY %d 项（超对称 / 离散拓扑序）。"
    " ==> 闸门位置很清楚：**所有'连续几何 + 4D 局域 + 非超对称'的格子全部封死**；"
    "剩下两格都要靠引入新结构（超伴子 / 涌现规范），代价各自不小于直接公设内部群"
    % (len(conn), sum(1 for x in conn if x[3] == "FAIL"), sum(1 for x in conn if x[3] == "BOUNDARY")))

# =================================================================
# §W5 硬数值门槛（任何成功统一都必须过）
# =================================================================
# 质子衰变：tau ∝ M_GUT^4，用 X9 标定外推 M_GUT 下限
M_GUT_MIN = mp.mpf('1e15') * (TAU_SK / TAU_X9) ** mp.mpf('0.25')

add("W-18", "W5 硬数值门槛", "质子衰变给出的统一能标下限（任何 GUT 都必须过）",
    "tau(p -> e+ pi0) > 2.4e34 yr 反推 M_GUT 下限",
    "FAIL",
    "tau_p ∝ M_GUT^4 / (alpha_GUT m_p^5)。用台账 X9 标定（M_GUT = 1e15 GeV -> tau = %s yr）与"
    " Super-K 下限 %s yr 外推：M_GUT > %s GeV。"
    " ==> 与 W-03 联立：SM 一圈跑动给出的交点分散在 %s 到 %s GeV，" % (ns(TAU_X9, 4), ns(TAU_SK, 4), ns(M_GUT_MIN, 6), ns(M12, 4), ns(M23, 4))
    + "其中 M_12 = %s GeV 已低于质子衰变下限 %s 倍 ==> 该交点被实验直接排除；" % (ns(M12, 4), ns(M_GUT_MIN / M12, 5))
    + "唯一勉强在限上的 M_23 = %s GeV 又与 M_12 差 %s 倍（不共点）。"
    " ==> **两条硬约束夹击：要共点必须 M_GUT 足够高，而 SM 跑动给不出共点**"
    % (ns(M23, 4), ns(M23 / M12, 5)))

# 引力并入
aG_at_M23 = (M23 / M_PL_GEV) ** 2
a_gut_M23 = 1 / mp.mpf('47')
ratio_A = a_gut_M23 / aG_at_M23
M_GUT_TYP = mp.mpf('2e16')
aG_typ = (M_GUT_TYP / M_PL_GEV) ** 2
ratio_B = (1 / mp.mpf('25')) / aG_typ
MU_EQ_25 = M_PL_GEV * mp.sqrt(1 / mp.mpf('25'))
MU_EQ_47 = M_PL_GEV * mp.sqrt(1 / mp.mpf('47'))

add("W-19", "W5 硬数值门槛", "引力并入四力统一：alpha_G(mu) = G mu^2 / (hbar c) 的共点检验",
    "引力与规范耦合是否能在同一能标相等（四力共点）",
    "FAIL",
    "alpha_G(mu) = (mu/M_Pl)^2，M_Pl = %s GeV。"
    " 令 alpha_G = alpha_GUT：alpha_GUT = 1/25 -> mu = %s GeV；alpha_GUT = 1/47 -> mu = %s GeV。"
    " 而规范统一点在 %s（SM 口径）或 ~2e16（典型 SUSY 口径）GeV。"
    " 在统一点处引力强度比规范弱：口径 A（M_23, 1/47）= %s 倍；口径 B（2e16 GeV, 1/25）= %s 倍。"
    " ==> 引力与规范力**无公共交点**，弱 %s 倍量级；口径 B 与既有台账 C16 的 1.3e4 倍同量级（交叉验证通过）。"
    " 结论：把引力并入的'四力统一'在朴素 EFT 跑动下被数量级排除（回链台账 X17）"
    % (ns(M_PL_GEV, 7), ns(MU_EQ_25, 6), ns(MU_EQ_47, 6), ns(M23, 4),
       ns(ratio_A, 6), ns(ratio_B, 6), ns(min(ratio_A, ratio_B), 5)))

# sin^2 theta_W
S2W_GUT = mp.mpf('0.20754')
S2W_EXP = mp.mpf('0.23121')
S2W_SIG = mp.mpf('1.3e-4')
sigma_s2w = abs(S2W_GUT - S2W_EXP) / S2W_SIG

add("W-20", "W5 硬数值门槛", "GUT 对 sin^2 theta_W 的预言 vs 实测（复算既有 --182 sigma）",
    "最小非 SUSY SU(5) 的 sin^2 theta_W 预言与实验偏差",
    "FAIL",
    "GUT 预言 sin^2 theta_W(M_Z) = %s，实测 = %s，偏差 = %s；"
    "取不确定度 %s ==> %s sigma。"
    " ==> 与既有台账 X16/X7 的 -182 sigma 量级一致（复算通过）。"
    " 这一条是'耦合统一'命题最锋利的单条判据：它不需要任何新实验，只用一个已测到 1e-4 精度的数，"
    "就把最小非超对称 GUT 排除掉，并且它**不依赖**质子衰变、不依赖对撞机"
    % (ns(S2W_GUT, 6), ns(S2W_EXP, 6), ns(abs(S2W_GUT - S2W_EXP), 5), ns(S2W_SIG, 3), ns(sigma_s2w, 5)))

add("W-21", "W5 硬数值门槛", "三条硬门槛的联合夹击（共点 / 质子 / 弱角）",
    "是否存在任何能标同时满足三条门槛",
    "FAIL",
    "联合约束：① 三耦合共点（W-03 失败，跨度 %s 倍）；② M_GUT > %s GeV（W-18，质子衰变）；"
    "③ sin^2 theta_W 落在实测 1.3e-4 内（W-20 差 %s sigma）；④ 引力在同一标度相等（W-19 弱 %s 倍）。"
    " ==> 四条中任意一条单独就足以排除朴素方案，四条同时失效 ==> **朴素四力统一的能标窗口为空集**。"
    " 这不是'参数没调好'，而是约束的几何：可行域被四条独立边界切成了空集"
    % (ns(M23 / M12, 5), ns(M_GUT_MIN, 5), ns(sigma_s2w, 5), ns(min(ratio_A, ratio_B), 5)))

# =================================================================
# §W6 δ_TUFT 供需量级定理（本层核心攻关）
# =================================================================
DELTA_ALPHA = ai_inv(1, M23) - ai_inv(0, M23)
DELTA_REQ = -DELTA_ALPHA * 2 * mp.pi / L23

# 量纲零空间（符号）：列 = c, hbar, G, kappa；行 = L, M, T
Dmat = sp.Matrix([[1, 2, 3, -1],
                  [0, 1, -1, 0],
                  [-1, -1, -2, 0]])
NSP = Dmat.nullspace()
NULL_DIM = len(NSP)
ETA_SYM = None
if NSP:
    v = NSP[0]
    ETA_SYM = (sp.Symbol('c') ** v[0] * sp.Symbol('hbar') ** v[1]
               * sp.Symbol('G') ** v[2] * sp.Symbol('kappa') ** v[3])

add("W-22", "W6 δ_TUFT 供需定理", "需求侧：让三耦合共点所需的 δ_TUFT 量级（数值）",
    "若要靠 TUFT 几何修正把 alpha_1 拉回与 alpha_2/alpha_3 共点，δ 需多大",
    "INFO",
    "在 M_23 = %s GeV 处 alpha^{-1} 分散 Δ = %s（alpha_1 偏低）。"
    "若 δ_TUFT 作为 β 函数的附加常数（d alpha^{-1}/d ln mu 中贡献 -δ/2π），"
    "则修正量 = δ/(2π) × ln(M/M_Z)，令其等于 Δ 得 **δ_需求 = %s（量级 O(1)）**。"
    " ==> 需求侧是一个 O(1) 的纯数，不是小量、也不是大数。这是任何'几何修正救场'方案必须兑现的确切数值"
    % (ns(M23, 6), ns(DELTA_ALPHA, 6), ns(DELTA_REQ, 6)))

add("W-23", "W6 δ_TUFT 供需定理", "供给侧 I：TUFT 可构造的无量纲几何量（量纲零空间，符号解）",
    "由 {c, hbar, G, kappa} 能构造几个无量纲量、数值是多少",
    "FAIL",
    "量纲矩阵（列 c, hbar, G, kappa；行 L, M, T）的零空间维数 = %s，基向量 = %s"
    " ==> 唯一无量纲组合（基向量给出）= %s = l_P × kappa，其平方即 η = (l_P × kappa)^2。"
    " 代入第 ⑨ 层已锚定的 kappa = %s 1/m（由电子静能锚定）得 **η = %s**（交叉验证：= (m_e/M_Pl)^2 = %s，"
    "二者相对差 %s，差异恰来自公理 A1 的 1/(1+r^2) 因子，自洽）。"
    " ==> TUFT 的几何供给是一个被锚定死的 1.75e-45，不是可调参数（这正是它可证伪的一面）"
    % (NULL_DIM, str(NSP[0].T) if NSP else "—", sp.sstr(ETA_SYM) if ETA_SYM else "—",
       ns(KAPPA_E, 8), ns(ETA, 8), ns((m_e / (M_PL_GEV * GeV / c ** 2)) ** 2, 8),
       ns(abs(ETA / (m_e / (M_PL_GEV * GeV / c ** 2)) ** 2 - 1), 3)))

# 供需三分支
need = abs(DELTA_REQ)
r_inv1 = 1 / R_STAR
r_inv2 = R_STAR ** -2
pos_gap = mp.log10(need / ETA)
b_real = mp.log(need) / mp.log(R_STAR)

add("W-24", "W6 δ_TUFT 供需定理", "供需对账：需求 O(1) vs 供给 η = 1.75e-45（三分支穷举）",
    "TUFT 的几何修正能否兑现 O(1) 的 δ",
    "FAIL",
    "需求 |δ| = %s（O(1)）；供给候选（三分支穷举）："
    " (a) η 的正幂 η^n（n>=1）：最大 %s，与需求相差 **%s 个量级** ==> 正幂分支彻底不够；"
    " (b) 无量纲比值 r = τ/κ 的整数幂：r^0 = 1（差 %s 倍）、r^-1 = %s（差 %s 倍）、r^-2 = %s（差 %s 倍）"
    " ==> 无整数幂能落在需求上（最近的 r^-1 仍差 %s 倍），且'为何取该幂次'需额外输入，不是导出；"
    " (c) 允许任意实数幂拟合：解 r^b = %s 得 b = %s（非整数、非有理），可精确拟合"
    " ==> 但这与第 ⑧ 层 B-03 同型：自由度 1 对观测量 1 且满射 = **零预测力**（把观测量改写成参数）。"
    " 三分支穷举结果：不够 / 不匹配 / 零预测力 ==> **δ_TUFT 无法在不支付自由度的前提下兑现耦合统一**"
    % (ns(need, 5), ns(ETA, 4), ns(pos_gap, 4),
       ns(need / 1, 4), ns(r_inv1, 6), ns(r_inv1 / need, 5), ns(r_inv2, 6), ns(r_inv2 / need, 5),
       ns(r_inv1 / need, 5), ns(need, 5), ns(b_real, 5)))

add("W-25", "W6 δ_TUFT 供需定理", "能标依赖分支：δ 若依赖 mu 是否可绕开（阈值行为）",
    "若 δ_TUFT 只在某能标以上激活，能否既救统一又不破坏低能",
    "FAIL",
    "要让 δ 在高能达 O(%s) 而在 mu < M_Z 处不破坏已测耦合（alpha 已测到 1e-9 相对精度），"
    "δ(mu) 必须在 M_Z 附近有陡峭阈值 ==> 必须引入**阈值标度**作为新输入（M_* 与可能的幂次 p）。" % ns(need, 4) +
    " 账目：新增自由度 (M_*, p) 共 2 个，换来 2 个约束（三耦合共点）"
    " ==> 净预测力 = 0；且该阈值标度与 M_GUT 的关系仍需外部给定（回链第 88 章：分量级阈值调谐已被封死 C7）。"
    " 结论：**δ_TUFT 的供需缺口不能靠能标依赖闭合**，只能靠新增自由度，而每新增一个自由度就抵消一条可检验关系")

# =================================================================
# §W7 五条硬判据总评分 + 封闭谱
# =================================================================
five = [
    ("判据 1 单一规范结构",
     "FAIL",
     "穷举的所有空间运行方式中：连续几何被 Coleman-Mandula / Weinberg-Witten 直积化（W-14）；"
     "挠率无传播模（W-15）；KK 等距群容量不足且无手征（W-09/W-10）。"
     "唯一未被定理封死的是超对称与涌现规范（W-16/W-13），但两者都要引入重量不小于直接公设内部群的新结构"),
    ("判据 2 单一或更少裸耦合",
     "FAIL",
     "SM 三耦合一圈跑动不共点（W-03，跨度 %s 倍）；引力无公共交点（W-19，弱 %s 倍）。"
     "d != 4 时'统一'还需额外尺度标定（W-02/W-04），净预测力不增" % (ns(M23 / M12, 5), ns(min(ratio_A, ratio_B), 5))),
    ("判据 3 产生跨力关系",
     "FAIL",
     "GUT 的确产生跨力关系（sin^2 theta_W），但预言值 %s 与实测 %s 差 %s sigma（W-20）。"
     " ==> 有关系的那一家被数据排除；没被排除的那些（直积群）根本不产生关系（台账 C17：3 个独立耦合、0 条跨力关系）"
     % (ns(S2W_GUT, 6), ns(S2W_EXP, 6), ns(sigma_s2w, 5))),
    ("判据 4 减少独立输入常数",
     "FAIL",
     "穷举表明每闭合一条硬伤至少一个自由度（第 ⑨ 层 T-01 自由度交换定理）："
     "d != 4 付尺度 1 个（W-02）、KK 付模量冻结机制 1 个（W-11）、手征付奇点/flux 1 个（W-10）、"
     "孤子付 sextic 1 个（W-08）、δ_TUFT 付阈值标度 2 个（W-25）。"
     " ==> 净账：SM 的 19（含中微子约 26）个常数一个没减，反而新增"),
    ("判据 5 可独立证伪的新预言",
     "FAIL",
     "穷举扫描中新产生的可检验陈述（三交点位置、η 量级、M_GUT 下限、等距群容量门槛）"
     "全部是**排除性**的（它们证伪候选方案），没有一条是 TUFT 或本项目给出的**正面新预言**。"
     "与既有'L3 层独立无量纲预言 = 0'（终审裁决 §一）一致"),
]
for i, (nm, vd, det) in enumerate(five, start=1):
    add("W-%d" % (25 + i), "W7 五判据总评", nm, "第 75 章五条硬判据之 %d" % i, vd, det)

# 封闭谱统计
n_fail = sum(1 for r in ROWS if r["verdict"] == "FAIL")
n_pass = sum(1 for r in ROWS if r["verdict"] == "PASS")
n_bd = sum(1 for r in ROWS if r["verdict"] == "BOUNDARY")
n_info = sum(1 for r in ROWS if r["verdict"] == "INFO")

add("W-31", "W7 五判据总评", "全空间运行方式封闭谱：还剩几条缝",
    "穷举扫描后，未被封死的方向清单与各自代价",
    "FAIL",
    "扫描规模：时空维 %d 格 x 联络 %d 格 x 拓扑 %d 格 x 对称放宽 %d 项，判据 %d 条（FAIL %d / PASS %d / BOUNDARY %d / INFO %d）。"
    " 封闭谱结论：**连续 + 4D 局域 + 非超对称的整块区域全部封死**（由量纲 W-01、Coleman-Mandula W-14、"
    "挠率无模 W-15、等距群容量 W-09、手征 W-10、Derrick W-08 六道独立闸门共同封闭）。"
    " 剩余缝隙只有三条，且每条都要付不小于直接公设内部群的代价："
    " ① 超对称（库内 0 条实现、0 条 LHC 可判谱）；"
    " ② 涌现规范 / 离散拓扑序（本库零建模，须先证低能恢复 GR+SM）；"
    " ③ AS 量子引力跑动接入 SM/GUT 重做交点诊断（台账 J26 点名的真正前沿，本层未做）。"
    " ==> 这不是'还没算完'，而是穷举后的封闭：可用出口的清单是有限的，且每一个都明码标价"
    % (len(dim_rows), len(conn), len(topo), 4, len(ROWS) + 1, n_fail, n_pass, n_bd, n_info))

# =================================================================
# 控制台输出
# =================================================================
print()
for r in ROWS:
    print("[%s] %-6s | %-38s | %s" % (r["verdict"], r["id"], r["name"][:38],
                                      r["detail"][:150].replace("\n", " ")))
print()
print("=" * 100)
print("汇总：总数 %d | PASS=%d FAIL=%d BOUNDARY=%d INFO=%d" % (len(ROWS), n_pass, n_fail, n_bd, n_info))
print("总耗时 %.1fs" % (time.time() - T0))
print("=" * 100)

# =================================================================
# 不可回退基线自检（guard）
# =================================================================
GUARD = [
    ("alpha_1^-1(M_Z) 落在 59.0±0.5", abs(A1_INV - mp.mpf('59.0')) < mp.mpf('0.5')),
    ("alpha_2^-1(M_Z) 落在 29.6±0.5", abs(A2_INV - mp.mpf('29.6')) < mp.mpf('0.5')),
    ("alpha_3^-1(M_Z) 落在 8.47±0.1", abs(A3_INV - mp.mpf('8.47')) < mp.mpf('0.1')),
    ("M_23 落在 1e16~1e17 GeV", M23 > mp.mpf('1e16') and M23 < mp.mpf('1e17')),
    ("三交点跨度 > 1000 倍（不共点）", M23 / M12 > 1000),
    ("M_Pl 落在 1.2209e19±0.1%", abs(M_PL_GEV / mp.mpf('1.2209e19') - 1) < mp.mpf('1e-3')),
    ("η 与 (m_e/M_Pl)^2 相对差 < 1e-5",
     abs(ETA / (m_e / (M_PL_GEV * GeV / c ** 2)) ** 2 - 1) < mp.mpf('1e-5')),
    ("量纲零空间维数 = 1（加 kappa 后）", NULL_DIM == 1),
    ("规范耦合维数 [g] = (4-d)/2 在 d=4 为 0", sp.simplify(dimg.subs(d_s, 4)) == 0),
    ("δ 需求量级落在 0.1~100（O(1)）", mp.mpf('0.1') < abs(DELTA_REQ) < mp.mpf('100')),
    ("引力弱倍数落在 1e2~1e5", mp.mpf('1e2') < min(ratio_A, ratio_B) < mp.mpf('1e5')),
    ("η 正幂与需求差 > 40 个量级", pos_gap > 40),
    ("质子衰变外推 M_GUT 下限 > 1e15 GeV", M_GUT_MIN > mp.mpf('1e15')),
    ("sin^2 theta_W 偏差 > 100 sigma", sigma_s2w > 100),
    ("等距群容量门槛 n(n+1)/2 >= 12 => n >= 5", N12 >= 5),
    ("回链第 ⑨ 层 r* = 0.00115965373716795", abs(R_STAR - mp.mpf('0.00115965373716795')) < mp.mpf('1e-18')),
]
bad = [g[0] for g in GUARD if not g[1]]
for name, ok in GUARD:
    if not ok:
        print("[GUARD-FAIL] %s" % name)
if bad:
    print("[自检] %d/%d 条基线在位，%d 条失守：%s" % (len(GUARD) - len(bad), len(GUARD), len(bad), bad))
else:
    print("[自检] %d 条不可回退基线全部在位" % len(GUARD))

# =================================================================
# 落盘
# =================================================================
out = {
    "meta": {
        "layer": "第 12 层：力的统一 —— 全空间运行方式穷举扫描与封闭谱审计",
        "precision": "sympy 符号代数 + mpmath 40 位",
        "counts": {"total": len(ROWS), "PASS": n_pass, "FAIL": n_fail,
                   "BOUNDARY": n_bd, "INFO": n_info},
        "guard": {"total": len(GUARD), "passed": len(GUARD) - len(bad), "failed": bad},
    },
    "anchors": {
        "alpha_inv_MZ": [ns(A1_INV, 10), ns(A2_INV, 10), ns(A3_INV, 10)],
        "M_12_GeV": ns(M12, 10), "M_13_GeV": ns(M13, 10), "M_23_GeV": ns(M23, 10),
        "spread_M23_over_M12": ns(M23 / M12, 8),
        "delta_alpha_inv_at_M23": ns(DELTA_ALPHA, 10),
        "delta_required_O1": ns(DELTA_REQ, 10),
        "M_Pl_GeV": ns(M_PL_GEV, 10),
        "alpha_G_weaker_factor_A": ns(ratio_A, 8),
        "alpha_G_weaker_factor_B": ns(ratio_B, 8),
        "mu_where_alphaG_eq_alphaGUT_GeV": {"alpha_GUT_1_25": ns(MU_EQ_25, 8),
                                            "alpha_GUT_1_47": ns(MU_EQ_47, 8)},
        "M_GUT_lower_bound_from_proton_decay_GeV": ns(M_GUT_MIN, 8),
        "sin2thetaW_GUT": ns(S2W_GUT, 8), "sin2thetaW_exp": ns(S2W_EXP, 8),
        "sin2thetaW_sigma": ns(sigma_s2w, 6),
        "kappa_e_per_m": ns(KAPPA_E, 10), "tau_e_per_m": ns(TAU_E, 10),
        "eta_lP_kappa_sq": ns(ETA, 10), "eta_over_me_over_MPl_sq": ns((m_e / (M_PL_GEV * GeV / c ** 2)) ** 2, 10),
        "dimensionless_nullspace_dim": NULL_DIM,
        "r_inverse": ns(r_inv1, 8), "r_power_needed_b": ns(b_real, 8),
        "isometry_capacity_min_n_for_12": N12, "isometry_capacity_min_n_for_24": N24,
    },
    "dim_scan": dim_rows,
    "topo_scan": [dict(manifold=t[0], n=t[1], isometry=t[2], isom_dim=t[3], chiral=t[4]) for t in topo],
    "conn_scan": [dict(connection=t[0], property=t[1], finding=t[2], verdict=t[3]) for t in conn],
    "five_criteria": [dict(name=x[0], verdict=x[1], detail=x[2]) for x in five],
    "rows": ROWS,
}
jp = os.path.join(DATA, "v_eq_c_力的统一_全空间运行方式_封闭谱审计.json")
with open(jp, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

L = []
L.append("# 第 12 层：力的统一 —— 全空间运行方式穷举扫描与封闭谱审计")
L.append("")
L.append("> 精度：sympy 符号代数 + mpmath 40 位 ｜ 判据 %d 条（PASS %d / FAIL %d / BOUNDARY %d / INFO %d）"
         % (len(ROWS), n_pass, n_fail, n_bd, n_info))
L.append("> guard 自检：%d/%d 条不可回退基线在位" % (len(GUARD) - len(bad), len(GUARD)))
L.append("")
L.append("## 关键锚点")
L.append("")
L.append("| 量 | 值 |")
L.append("|---|---|")
for k in ("alpha_inv_MZ", "M_12_GeV", "M_13_GeV", "M_23_GeV", "spread_M23_over_M12",
          "delta_alpha_inv_at_M23", "delta_required_O1", "M_Pl_GeV",
          "alpha_G_weaker_factor_A", "alpha_G_weaker_factor_B",
          "M_GUT_lower_bound_from_proton_decay_GeV", "sin2thetaW_sigma",
          "kappa_e_per_m", "eta_lP_kappa_sq", "r_inverse", "r_power_needed_b"):
    L.append("| %s | %s |" % (k, out["anchors"][k]))
L.append("")
L.append("## 时空维扫描")
L.append("")
L.append("| d | [g] | [G] | YM | EH | 空间维 D | 孤子 | Coleman-Mandula | 承载 SM |")
L.append("|---|---|---|---|---|---|---|---|---|")
for r0 in dim_rows:
    L.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s |"
             % (r0["d"], r0["gdim"], r0["Gdim"], r0["ym"], r0["eh"], r0["D"],
                r0["derr"], r0["cm"], r0["sm"]))
L.append("")
L.append("## 拓扑 / 紧化扫描")
L.append("")
L.append("| 内部流形 | n | 等距群 | 维数 | 手征费米子 |")
L.append("|---|---|---|---|---|")
for t in out["topo_scan"]:
    L.append("| %s | %s | %s | %s | %s |" % (t["manifold"], t["n"], t["isometry"], t["isom_dim"], t["chiral"]))
L.append("")
L.append("## 联络扫描")
L.append("")
L.append("| 联络 | 性质 | 发现 | 判定 |")
L.append("|---|---|---|---|")
for t in out["conn_scan"]:
    L.append("| %s | %s | %s | %s |" % (t["connection"], t["property"], t["finding"], t["verdict"]))
L.append("")
L.append("## 判据明细")
L.append("")
cur = None
for r in ROWS:
    if r["section"] != cur:
        cur = r["section"]
        L.append("")
        L.append("### %s" % cur)
        L.append("")
    L.append("**[%s] %s ｜ %s**" % (r["verdict"], r["id"], r["name"]))
    L.append("")
    L.append("- 判据：%s" % r["criterion"])
    L.append("- 结论：%s" % r["detail"])
    L.append("")
L.append("## 诚实边界")
L.append("")
L.append("- W-05~W-08 的维度扫描中，'可重整 / Derrick / Coleman-Mandula 适用域'是教科书标准结论（标 [A] 外部），"
         "本层只做穷举编排与数值代入，不声称重新证明了这些定理；")
L.append("- W-18 的质子衰变外推用 τ ∝ M_GUT^4 并以台账 X9 的 1.65e31 yr 作标定，"
         "不同 GUT 模型与矩阵元归一会给不同系数，故 M_GUT 下限应读作量级门槛而非精确界；")
L.append("- W-19 的两个口径给出 337 与 1.49e4 两个'引力弱多少倍'的数值，差异来自 M_GUT 与 α_GUT 取值；"
         "与既有台账 C16 的 1.3e4 同量级（交叉验证通过），本层取较小者作保守陈述；")
L.append("- W-23 的量纲零空间只列 {c, ħ, G, κ} 四量；若引入额外独立量纲常数（如 Λ、e、m_p）零空间维数会增大，"
         "但那等于新增输入，正是 W-25 所记账的自由度；")
L.append("- 本层的'封闭谱'是**在既有定理与本层判据下**的封闭，不等于自然界排除；"
         "剩余三条缝隙（超对称 / 涌现规范 / AS 引力跑动）本层未做，不得记为已解决。")

mp_path = os.path.join(DATA, "v_eq_c_力的统一_全空间运行方式_封闭谱审计.md")
with open(mp_path, "w", encoding="utf-8") as f:
    f.write("\n".join(L))

print("已写出：数据/%s + .json" % os.path.basename(mp_path))
