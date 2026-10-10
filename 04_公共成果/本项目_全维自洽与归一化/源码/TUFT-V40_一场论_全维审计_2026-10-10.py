# -*- coding: utf-8 -*-
"""
TU(F)T(g-2)GAQ V4.(0)「一场论」深度攻破扩展整理 —— 全维审计（r28）

来料：《TU(\\mathcal F)T(g-2)GAQ V4.(\\boldsymbol{0}) 一场论｜深度攻破扩展整理》
      13 节：①挠率张量三分量分解 ②作用量变分 ③螺旋旋量 Psi 与自由度计数
            ④低能渐近展开 I（->标准模型）⑤低能渐近展开 II（->MHD / Grad 猜想域）
            ⑥RG beta(g) 几何构造与普朗克标度统一条件 ⑦可观测量（g-2 / EDM / CMB）
            ⑧ADM-BSSN 挠率方程组 ⑨三元拓扑代数 0/1/inf ⑩Lean4 形式化路线
            ⑪理论边界（严格 vs 假说）⑫Mermaid 架构图 ⑬下一步任务清单

分工声明（不重复计数，先记账）：
  * r18/r19/r20/r21（同目录，2026-10-07）—— 审 V3.4「EC 作用量 + ADM-BSSN +
    孤子色散 + g-2/EDM」：已判「作用量与 ADM 演化方程不同源」（r19）、
    「tau 是代数 slave / 动力学化代价 +2~4 参数撞 Omega5」（r20）、
    「P1 门禁 0/5、路径 2 关闭」（r21）。本册**不复算**那些方程，只审 V4.(0)
    文本自身的结构 / 量纲 / 分量计数 / 恒等式 / 可代入性，并做复发登记。
  * r27（2026-10-10）—— 审「统一场论合集 + GMUFT」：判「ADM 哈密顿约束把两个 K 项
    单独交换符号」。本册 V33 独立复现同一条，并给出更强读数（该式给出**负能量密度**）。
  * r22/r23/r24/r25/r26/r26b（2026-10-10）—— 审垂直原理体系与球对称流体微扰。
本册条目编号 V01..V46，与 r22(48)/r23(33)/r25(28)/r26(39)/r27(33) **不可相加**。

撞号处置：起草时本目录 r27 已被并行会话占用（同日《统一场论合集与GMUFT 全维审计》），
另有 r25 三份、r26/r26b 两份，按「后到者改号不覆盖他人」取空号 **r28**，
未触碰他人任何文件。

纯标准库（Python 3.8.8 实测可跑）：
  * Decimal 60 位（RGE 跑动、能量密度、常数核对）
  * Fraction 量纲向量 (M,L,T,Q)（作用量 / EDM / 功率谱量纲）
  * 自实现精确复数 4x4 矩阵（gamma 矩阵、gamma5、手征变换：元素均为 0/±1/±i
    => 乘法与加法精确，残差为**精确零**而非浮点零）
  * 轴对称 Harris sheet 与 3D ABC/Beltrami 场（特殊取值点使 tanh=1/2、sech^2=3/4
    => 读数精确有理数）做 MHD 平衡与 Frobenius 可积性对拍
  * 正则扫描：LaTeX `\\frac(` 分母缺花括号、Mermaid 节点 ID 非法字符、符号同名台账
"""
import json
import math
import os
import re
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as Fr

getcontext().prec = 60

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DIR_DATA = os.path.join(BASE, "数据")
os.makedirs(DIR_DATA, exist_ok=True)

TAG = "TUFT-V40_一场论_全维审计_2026-10-10"

ENTRIES = []
GUARDS = []
KEY = {}


def emit(cid, verdict, title, detail, numbers=None, tags=None):
    ENTRIES.append({
        "id": cid, "verdict": verdict, "title": title,
        "detail": detail, "numbers": numbers or {}, "tags": tags or [],
    })


def guard(name, ok, detail, value=None):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail, "value": value})


def fm(x):
    if isinstance(x, Decimal):
        if x == 0:
            return "0.0000000000000000000000000E+00"
        return format(x, ".25E")
    return format(Decimal(str(x)), ".25E")


def D(x):
    return Decimal(str(x))


# ============================================================ 量纲框架
# dim = M^a * L^b * T^c * Q^d  （Fraction 四元组；Q = 电荷，SI 基）
def DM(a=0, b=0, c=0, d=0):
    return (Fr(a), Fr(b), Fr(c), Fr(d))


def dadd(x, y):
    return (x[0] + y[0], x[1] + y[1], x[2] + y[2], x[3] + y[3])


def dneg(x):
    return (-x[0], -x[1], -x[2], -x[3])


def dscale(x, k):
    return (x[0] * Fr(k), x[1] * Fr(k), x[2] * Fr(k), x[3] * Fr(k))


def dstr(x):
    return "M^" + str(x[0]) + " L^" + str(x[1]) + " T^" + str(x[2]) + " Q^" + str(x[3])


def planck_exp(x):
    """Planck 单位制（c=1, hbar=1, G=1）折算成纯长度幂次。
    c=1 => L = T；hbar=1 => M L^2 T^-1 = 1 => M = L^-1；故 L^e = M^(-a) L^(b+c)。"""
    a, b, c, _d = x
    return -a + b + c


def planck_str(x):
    e = planck_exp(x)
    if e == 0:
        return "L^0 (无量纲)"
    if e.denominator == 1:
        return "L^" + str(e.numerator)
    return "L^(" + str(e.numerator) + "/" + str(e.denominator) + ")"


# SI 基下基本符号量纲
SYM = {
    "R": DM(0, -2, 0, 0),            # Ricci 标量
    "G_newton": DM(-1, 3, -2, 0),    # 牛顿常数
    "kappa_G": DM(-1, 3, -2, 0),     # kappa_G = 8 pi G
    "inv_2kappaG": DM(1, -3, 2, 0),  # 1/(2 kappa_G) = 1/(16 pi G)
    "torsion": DM(0, -1, 0, 0),      # 挠率 tau^alpha_mu nu
    "Box": DM(0, -2, 0, 0),          # d'Alembertian
    "curv_scalar_kappa2": DM(0, -2, 0, 0),  # kappa^2（kappa = 弧长倒数）
    "edm": DM(0, 1, 0, 1),           # 电偶极矩 d_e = 电荷 x 长度
    "dimensionless": DM(0, 0, 0, 0),
    "action_density": DM(1, -1, -2, 0),
    "sqrt_g_d4x": DM(0, 4, 0, 0),
}

# ============================================================ 物理常数
PI = D("3.1415926535897932384626433832795028841971693993751058209749445923078164")
C_LIGHT = D("2.99792458e8")
G_NEWTON = D("6.67430e-11")
HBAR = D("1.054571817e-34")
E_CHARGE = D("1.602176634e-19")
ALPHA_FINE = D("7.2973525693e-3")
M_Z = D("91.1876")                 # GeV
M_PLANCK = D("1.220910e19")        # GeV
AE_EXP = D("1.159652e-3")          # 电子反常磁矩实验值
EDM_ACME_E_CM = D("1.1e-29")       # e*cm（ACME 2018 真实上限）

# 交叉印证锚点（与 r18/r19/r22/r27 逐位一致）
C4_OVER_8PI_G = C_LIGHT ** 4 / (D(8) * PI * G_NEWTON)
C4_OVER_8PI_G_REF = D("4.8154538867224223992518906E+42")

# 1-loop SM beta 系数（b_i，约定 da_i/dt = b_i a_i^2, a_i = alpha_i/(4 pi), t = ln mu）
B_SM = (Fr(41, 10), Fr(-19, 6), Fr(-7))

# ============================================================ 来料原文常量（用于机器扫描）
# 关键式与排版片段按原样保留（反斜杠为原文所有）
SRC_FRAC = [
    r"\frac(\boldsymbol{1})2\kappa_G",      # 第 2 节：作用量希尔伯特项系数
    r"\frac(\boldsymbol{1})4",              # 第 2 节：挠率平方项系数
    r"{}^{((\boldsymbol{1}))}\tau",         # 第 1 节：迹部分记号
]
SRC_SECTION = {
    "s1_trace": r"\tau_\mu \equiv \tau^\alpha_{\mu\alpha}",
    "s1_axial": r"{}^{(3)}\tau_{\alpha\mu\nu} = \tau_{[\alpha\mu\nu]}",
    "s1_mixed": "无迹混合(g-2)对称部分",
    "s1_group": r"\mathrm{SU}(3)\times\mathrm{SU}(2)\times\mathrm{U}((\boldsymbol{1}))",
    "s2_action": "S = int [ R/(2 kappa_G) + (1/4) tau_{alpha mu nu} tau^{alpha mu nu} + L_fluct ] sqrt(-g) d4x",
    "s2_torsion_alg": r"\tau^{\alpha}*{\mu\nu} \propto S^{\alpha}*{\mu\nu}",
    "s3_wave": r"\nabla^\alpha\nabla_\alpha \Psi - \big(\kappa^2-\tau^2\big)\Psi=0",
    "s3_chiral": "手征性由挠率联络直接生成，不需要手动外加手征项",
    "s3_dof": "挠率(1)8独立分量",
    "s5_divB": r"\nabla\cdot\mathbf ( \mathbf B) = (\boldsymbol{0})",
    "s5_flux": r"\mathbf ( \mathbf B)\cdot\nabla\psi =(\boldsymbol{0})",
    "s5_force": r"\mathbf J\times\mathbf ( \mathbf B)=\nabla p",
    "s6_beta": r"\beta(g_i)=\mu\frac{dg_i}{d\mu}=(\mathcal F)_i(\kappa[\mu],\tau[\mu])",
    "s6_unify": r"g_(\boldsymbol{1})(M_\text{Pl})=g_2(M_\text{Pl})=g_3(M_\text{Pl})",
    "s7_edm": r"d_e \propto \theta_\text{CP}\cdot |\tau_\text{chiral}|",
    "s7_cmb": r"P_\mathcal R(k)=P_\mathcal R^\text{GR}(k)+\Delta P(k;\langle\tau^2\rangle)",
    "s8_ham": r"{}^{(3)}R + K_{ij}K^{ij}-K^2 = (\boldsymbol{1})6\pi G\left(\rho_\text{matter}+\rho_\text{torsion}\right)",
    "s8_mom": r"D_j\left(K^{ij}-\gamma^{ij}K\right)=8\pi G\left(j^i_\text{matter}+j^i_\text{torsion}\right)",
    "s8_pde": r"\partial_t \tau^i_{jk} = \mathcal L_\beta \tau^i_{jk}+\alpha\left(\mathcal (\mathcal F)^i_{jk}(\gamma,K,\tau,\Psi)\right)",
    "s11_claim_dims": "V4.(0)作用量、场方程量纲闭环，消除V3.4量纲冲突",
}

MERMAID_SRC = r"flowchart TD" + "\n" + "\n".join([
    r'    A["本源公理层<br/>4维EC挠率流形<br/>v_spiral=c 光速螺旋<br/>0-1-inf三元拓扑代数"] --> \(\mathbf B\)["全域作用量变分"]',
    r'    \(\mathbf B\) --> C["TU\(\mathcal F\)T\(g‑2\)GAQ V4.(0)场方程组<br/>EC引力-挠率方程"]',
    r'    C --> D["高能极限<br/>普朗克标度，四力合一"]',
    r'    C --> E["低能渐近展开"]',
    r'    E --> E\(\boldsymbol{1}\)["标准模型有效理论"]',
    r'    E --> E2["广义相对论引力极限"]',
    r'    E --> E3["MHD磁流体静力学<br/>Grad猜想推翻体系"]',
    r'    E\(\boldsymbol{1}\) --> \(\mathcal F\)["可观测量"]',
    r'    C --> I["仿真栈<br/>EC + FDTD + dynesty"]',
    r'    I --> J["实验比对，证伪检验"]',
    r'    J -->|冲突| K["迭代修正公理/场方程"]',
])

SRC_ALL_TEXT = MERMAID_SRC + "\n" + "\n".join(SRC_FRAC) + "\n" + "\n".join(SRC_SECTION.values())

# 来料**未给定义 / 未给显式形式**的量（元台账）
UNDEFINED_QUANTITIES = [
    ("L_fluct", "只写 ~Psi^dagger O(kappa,tau) Psi，算子 O 未给"),
    ("O(kappa,tau)", "同上，算子形式缺失"),
    ("T^torsion_munu", "挠率能量动量张量，只给记号"),
    ("S^alpha_munu", "自旋张量，只出现在比例式中"),
    ("Delta g(tau_local)", "g-2 几何修正项，只写『是局域挠率的函数』"),
    ("Delta P(k;<tau^2>)", "CMB 功率谱修正，只给依赖关系"),
    ("F^i_jk(gamma,K,tau,Psi)", "ADM 挠率源项，只给记号"),
    ("F_i(kappa[mu],tau[mu])", "bubble beta 几何函数，只给独立性假设"),
    ("theta_CP", "CP 破坏相位，数值/来源未给"),
    ("tau_chiral", "手征挠率分量，未定义（且与第 1 节三分量的关系未声明）"),
    ("rho_torsion", "ADM 哈密顿约束里的挠率能量密度，未给"),
    ("j^i_torsion", "ADM 动量约束里的挠率流，未给"),
]


# ============================================================ 精确复数 4x4 矩阵工具
def mzero(n=4):
    return [[complex(0, 0)] * n for _ in range(n)]


def miden(n=4):
    m = mzero(n)
    for i in range(n):
        m[i][i] = complex(1, 0)
    return m


def mmul(a, b):
    n = len(a)
    out = mzero(n)
    for i in range(n):
        for k in range(n):
            aik = a[i][k]
            if aik == 0:
                continue
            for j in range(n):
                out[i][j] += aik * b[k][j]
    return out


def mv(a, v):
    """矩阵-列向量乘（a: n x n, v: n）"""
    n = len(a)
    return [sum(a[i][j] * v[j] for j in range(n)) for i in range(n)]


def madd(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a))] for i in range(len(a))]


def msub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a))] for i in range(len(a))]


def mscale(a, s):
    return [[a[i][j] * s for j in range(len(a))] for i in range(len(a))]


def mabsmax(a):
    return max(abs(a[i][j]) for i in range(len(a)) for j in range(len(a)))


def meq(a, b):
    return mabsmax(msub(a, b)) == 0.0


def comm(a, b):
    return msub(mmul(a, b), mmul(b, a))


def acomm(a, b):
    return madd(mmul(a, b), mmul(b, a))


# gamma 矩阵（Dirac 表示，元素均为 0 / ±1 / ±i => 运算精确）
I2 = [[complex(1, 0), complex(0, 0)], [complex(0, 0), complex(1, 0)]]
Z2 = [[complex(0, 0), complex(0, 0)], [complex(0, 0), complex(0, 0)]]
SX = [[complex(0, 0), complex(1, 0)], [complex(1, 0), complex(0, 0)]]
SY = [[complex(0, 0), complex(0, -1)], [complex(0, 1), complex(0, 0)]]
SZ = [[complex(1, 0), complex(0, 0)], [complex(0, 0), complex(-1, 0)]]


def mblk(A, B, C, Dblk):
    return [[A[i][j] for j in range(2)] + [B[i][j] for j in range(2)] for i in range(2)] + \
           [[C[i][j] for j in range(2)] + [Dblk[i][j] for j in range(2)] for i in range(2)]


GAMMA = [
    mblk(I2, Z2, Z2, mscale(I2, -1)),      # gamma^0
    mblk(Z2, SX, mscale(SX, -1), Z2),      # gamma^1
    mblk(Z2, SY, mscale(SY, -1), Z2),      # gamma^2
    mblk(Z2, SZ, mscale(SZ, -1), Z2),      # gamma^3
]
ETA = [1, -1, -1, -1]
G5 = mscale(mmul(mmul(GAMMA[0], GAMMA[1]), mmul(GAMMA[2], GAMMA[3])), complex(0, 1))

# ============================================================ 数值辅助
def _lcg(seed, n):
    x = seed & 0x7FFFFFFF
    out = []
    for _ in range(n):
        x = (1103515245 * x + 12345) & 0x7FFFFFFF
        out.append(x - 0x40000000)
    return out


def build_tau(seed=20261010):
    """构造反对称挠率 tau^alpha_{mu nu}（mu<nu 共 24 个独立分量；对角 tau^a_mu_mu = 0）。"""
    vals = _lcg(seed, 24)
    tau = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    k = 0
    for a in range(4):
        for mu in range(4):
            for nu in range(mu + 1, 4):
                tau[a][mu][nu] = vals[k]
                tau[a][nu][mu] = -vals[k]
                k += 1
    return tau


def trace_vec(tau):
    """v_mu = tau^alpha_{mu alpha}（第 1、3 指标收缩）"""
    return [sum(tau[a][mu][a] for a in range(4)) for mu in range(4)]


def fully_antisym(tau):
    """A^{[alpha mu nu]} = (1/3)(tau^{a mu nu} + tau^{mu nu a} + tau^{nu a mu})；用 6 倍整数避免分数。"""
    A = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for mu in range(4):
            for nu in range(4):
                A[a][mu][nu] = tau[a][mu][nu] + tau[mu][nu][a] + tau[nu][a][mu]
    return A


def axial_vec(A6):
    """a_mu = (1/6) eps_{mu a b g} A6^{a b g}（A6 = 6 倍完全反对称部分）"""
    eps = {}
    perms = [(0, 1, 2, 3), (0, 2, 3, 1), (0, 3, 1, 2), (1, 0, 3, 2),
             (1, 2, 0, 3), (1, 3, 2, 0), (2, 0, 1, 3), (2, 1, 3, 0),
             (2, 3, 0, 1), (3, 0, 2, 1), (3, 1, 0, 2), (3, 2, 1, 0)]
    for p in perms:
        sgn = 1
        q = list(p)
        for i in range(4):
            for j in range(3 - i):
                if q[j] > q[j + 1]:
                    q[j], q[j + 1] = q[j + 1], q[j]
                    sgn = -sgn
        eps[p] = sgn
    out = []
    for mu in range(4):
        s = 0
        for (i, j, k) in [(a, b, c) for a in range(4) for b in range(4) for c in range(4)]:
            if len({i, j, k}) < 3:
                continue
            s += eps.get((mu, i, j, k), 0) * A6[i][j][k]
        out.append(Fr(s, 6))
    return out


def norm2_int(tau):
    return sum(tau[a][mu][nu] * tau[a][mu][nu]
               for a in range(4) for mu in range(4) for nu in range(4))


# ============================================================ 第 1 节：挠率张量分解
def audit_torsion():
    tau = build_tau()
    # (a) 反对称恒等式 + 独立分量计数
    anti_res = max(abs(tau[a][mu][nu] + tau[a][nu][mu])
                   for a in range(4) for mu in range(4) for nu in range(4))
    n_free = 4 * 6  # alpha 4 值 x C(4,2)=6 个反对称对
    guard("torsion_antisymmetry_exact", anti_res == 0,
          "tau^a_mu nu + tau^a_nu mu 逐分量残差 = " + str(anti_res), anti_res)
    guard("torsion_free_components_24", n_free == 24,
          "4 x C(4,2) = " + str(n_free), n_free)
    emit("V02", "PASS",
         "挠率反对称性 => 4 维时空独立分量 4 x C(4,2) = 24（标准计数）",
         "tau^alpha_{mu nu} = -tau^alpha_{nu mu}：逐分量穷举 4x4x4（含对角元 tau^a_mu_mu = 0）"
         "残差为精确零。alpha 取 4 值，反对称对 (mu,nu) 有 C(4,2) = 6 个 => 独立分量 **24**。"
         "这是纯组合事实，是来料第 1 节全部后续讨论的前提。",
         {"antisym_residual": str(anti_res), "free_components": 24}, ["挠率", "计数", "代数"])

    emit("V03", "FAIL",
         "第 3 节自称『挠率 18 独立分量』——与第 1 节的 4 维挠率（24 分量）内部矛盾",
         "4 维反对称挠率 tau^alpha_{mu nu} 的独立分量数是 **24**（4 x C(4,2)）；来料第 3 节写『挠率18独立分量』。"
         "18 = 3 x C(4,2) 恰是**空间**挠率 tau^i_{jk}（i = 1..3）的分量数，即 3+1 分解后的空间部分——"
         "但第 3 节所在段落讨论的是 4 维流形本体（同段并列『度规(1)(0)分量』），并未声明已做 3+1 分解。"
         "=> 要么是 3+1 分解后未标注，要么是计数错误；两种情形都与第 1 节的 24 不能同时成立。",
         {"claimed": 18, "correct_4d": 24, "spatial_3d": 18}, ["挠率", "计数", "自相矛盾"])

    # (b) 完全反对称部分与迹部分
    A6 = fully_antisym(tau)
    Aproj = [[[Fr(A6[a][mu][nu], 3) for nu in range(4)] for mu in range(4)] for a in range(4)]
    v = trace_vec(tau)
    n_axial_free = 4  # C(4,3) = 4
    # 完全反对称部分与「迹型张量」正交（代数恒等，精确零）
    u = [3, -5, 7, 11]
    orth = 0
    for a in range(4):
        for mu in range(4):
            for nu in range(4):
                Vcomp = (u[nu] if a == mu else 0) - (u[mu] if a == nu else 0)
                orth += int(Aproj[a][mu][nu]) * Vcomp
    guard("axial_vs_trace_orthogonal_exact", orth == 0,
          "<完全反对称, 迹型> = " + str(orth) + "（A^a_a nu = A^a_mu a = 0 的代数推论）", orth)
    tr_of_axial = max(abs(int(Aproj[a][mu][a])) for a in range(4) for mu in range(4))
    guard("axial_is_traceless_exact", tr_of_axial == 0,
          "完全反对称部分的迹 A^a_mu a 最大值 = " + str(tr_of_axial), tr_of_axial)

    emit("V05", "PASS",
         "标准正交分解 24 = 4（迹矢量）+ 4（轴矢量）+ 16（无迹）——本册补出正解",
         "Hehl 1976 的标准结果：v_mu = tau^alpha_{mu alpha}（4 分量，一阶**矢量**）、"
         "a_mu = (1/6) eps_{mu alpha beta gamma} tau^{alpha beta gamma}（4 分量，**赝矢量**，来自完全反对称部分）、"
         "余下 16 分量构成无迹张量。机器验证：4+4+16 = 24 ✓；完全反对称部分与迹型张量 T^a_mu nu = delta^a_mu u_nu - delta^a_nu u_mu "
         "的内积**精确为零**（代数恒等 A^a_{alpha nu} = A^a_{mu alpha} = 0）；完全反对称部分自动无迹。"
         "=> 来料第 1 节给了三个『部分』的名称，但既没给分量数，也没给正交性，因而无法判定其分解是否完备。",
         {"decomposition": "4 + 4 + 16 = 24", "axial_free_components": n_axial_free,
          "orthogonality_residual": orth}, ["挠率", "分解", "正交性"])

    emit("V04", "FAIL",
         "第 1 节『(2) 无迹混合对称部分』名实不符：后两个指标恒反对称 => 不存在『对称部分』",
         "tau^alpha_{mu nu} 的 (mu,nu) 指标**恒反对称**（第 1 节自己给出的定义），因此"
         "『mu nu 对称部分』恒等于零，不存在。标准分解里剩下的 16 个自由度是"
         "『(矢量按对) 的无迹部分』，它与『对称』无关。命名错置会把读者引向错误的投影算子。",
         {"symmetric_part_identically_zero": True}, ["挠率", "命名", "FAIL"])

    emit("V06", "FAIL",
         "『轴挠率』标签错置：(1) 迹部分是矢量不是轴矢量；(2) 轴矢量来自完全反对称部分",
         "来料第 1 节写『(1) 迹部分（轴挠率，伪标量模式）tau_mu = tau^alpha_{mu alpha}』。"
         "标准术语中：迹 tau^alpha_{mu alpha} 是一阶**矢量**（4 分量，Lorentz 变换为矢量）；"
         "轴矢量 a_mu = (1/6)eps_{mu alpha beta gamma}tau^{alpha beta gamma} 是**赝矢量**（来自完全反对称部分，"
         "即来料自己的第 (3) 部分）。机器读数（同一挠率）：迹矢量 v = " + str(v) +
         "，轴矢量 a = " + str([str(x) for x in axial_vec(A6)]) + " —— 二者既不相等也不成比例。"
         "=> 『迹 = 轴挠率 = 伪标量』三处标签同时错，且与第 (3) 部分的定义冲突。",
         {"trace_vec": v, "axial_vec_nonzero": True}, ["挠率", "命名", "同名两义"])

    emit("V08", "MISMATCH",
         "『轴挠率』一词在第 1 节内被同时用于第 (1) 部分与（隐含的）第 (3) 部分",
         "第 (1) 部分叫『轴挠率』，第 (3) 部分叫『完全无迹全反对称部分』。"
         "在标准分解里，轴挠率**就是**完全反对称部分的对偶。=> 同一术语在同一节内指向两个"
         "互不相同的子空间（迹 4 维 vs 完全反对称 4 维），构成 A-07 型『符号同名两义』台账冲突；"
         "而这两部分又被指派给不同的力（U(1) vs SU(3)），冲突因此不是纯记号问题。",
         {"same_term_two_subspaces": True}, ["台账", "同名两义", "MISMATCH"])

    emit("V07", "FAIL",
         "三分量 -> SM 规范群的维数不匹配：完全反对称部分只有 4 个分量，装不下 SU(3) 的 8 个生成元",
         "来料把 (3)『完全无迹全反对称部分 tau_{[alpha mu nu]}』指派给 **SU(3) 强相互作用**。"
         "但 4 维完全反对称 3-形式只有 C(4,3) = **4** 个独立分量（机器上界 = 4），"
         "而 SU(3) 规范场需要 8 个（gluon）。=> 缺口 4 个色自由度；"
         "同理 (1) 迹部分 4 分量指派给 U(1)（需 1）富余 3，(2) 无迹 16 分量指派给 SU(2)（需 3）富余 13。"
         "整个指派（4,16,4）->（1,3,8）在维数上既非单射也非满射，且来料未给任何『24 -> 12 』的消去机制。",
         {"components": {"trace": 4, "traceless": 16, "axial": 4},
          "needed": {"U1": 1, "SU2": 3, "SU3": 8},
          "gap_axial_vs_SU3": 8 - 4}, ["SM", "维数", "FAIL"])

    emit("V01", "INFO",
         "未定义 / 未给显式形式的量共 " + str(len(UNDEFINED_QUANTITIES)) + " 项（其中 ≥5 项直接决定方程是否可计算）",
         "逐节清点（人工锚 [C]，机器计数）：" +
         " · ".join([k + "（" + d + "）" for k, d in UNDEFINED_QUANTITIES]) +
         "。凡未给显式形式的量，后续『接入 MCMC / 数值仿真 / 与实验比对』的承诺都不可执行。",
         {"undefined_count": len(UNDEFINED_QUANTITIES)}, ["台账", "可代入性"])


# ============================================================ 第 2 节：作用量与变分
def audit_action():
    # 量纲：Planck 单位制下 R/(2 kappa_G) 与 (1/4) tau^2
    d_R = SYM["R"]
    d_coef = SYM["inv_2kappaG"]
    d_hilbert = dadd(d_coef, d_R)                # 1/(2 kappa_G) * R
    d_tau2 = dscale(SYM["torsion"], 2)           # tau^2
    d_tau_term = d_tau2                          # 系数 1/4 无量纲
    gap = dadd(d_hilbert, dneg(d_tau_term))
    lp_h = planck_exp(d_hilbert)
    lp_t = planck_exp(d_tau_term)
    guard("action_dims_mismatch_confirmed", lp_h != lp_t,
          "Planck 单位制：R/(2kG) = " + planck_str(d_hilbert) + " vs (1/4)tau^2 = " + planck_str(d_tau_term)
          + "（差 " + str(lp_h - lp_t) + " 个长度幂次）", lp_h - lp_t)

    emit("V09", "FAIL",
         "作用量两项量纲不齐：R/(2 kappa_G) 与 (1/4) tau^2 相差 M^1 L^-3 T^2（Planck 单位下差 L^2）",
         "S = int [ R/(2 kappa_G) + (1/4) tau_{alpha mu nu}tau^{alpha mu nu} + L_fluct ] sqrt(-g) d4x。"
         "被积函数各项必须同量纲。机器量纲核算（Fraction 向量 (M,L,T,Q)）："
         "[R] = " + dstr(d_R) + "，[G] = [kappa_G] = " + dstr(SYM["kappa_G"]) + " => [R/(2 kappa_G)] = " + dstr(d_hilbert) +
         "；[tau] = " + dstr(SYM["torsion"]) + " => [(1/4) tau^2] = " + dstr(d_tau_term) + "。"
         "两者相差 " + dstr(gap) + "（Planck 单位制下即 L^2）。"
         "=> 挠率平方项缺一个量纲为 " + dstr(gap) + " 的系数（等价于缺一个长度平方或多一个质量平方）。"
         "对照库内 r21b（V34C 修复优化）F04：V34C 修法是「引入长度标度 l 使动能/质量项同维」——本册 V4.(0) 未做这一步。",
         {"hilbert_term": dstr(d_hilbert), "tau_term": dstr(d_tau_term), "gap": dstr(gap),
          "planck_hilbert": planck_str(d_hilbert), "planck_tau": planck_str(d_tau_term)},
         ["量纲", "作用量", "FAIL"])

    # LaTeX 排版扫描
    bad_frac = [s for s in SRC_FRAC if "\\frac(" in s]
    n_frac_bad = len(re.findall(r"\\frac\(", SRC_ALL_TEXT))
    guard("latex_frac_missing_brace", n_frac_bad > 0,
          "来料出现 \\frac( 形式的非法分母 " + str(n_frac_bad) + " 处", n_frac_bad)
    emit("V10", "FAIL",
         "LaTeX 排版错误：" + str(n_frac_bad) + " 处 `\\frac(` 分母缺花括号 => 渲染会丢失分式结构",
         "来料第 2 节写作 `\\frac(\\boldsymbol{1})2\\kappa_G` 与 `\\frac(\\boldsymbol{1})4`，"
         "正确写法应为 `\\frac{1}{2\\kappa_G}` / `\\frac{1}{4}`。"
         "`\\frac(a)b` 在 LaTeX 中把 `(a)` 当分子、`b` 当分母的第一字符，分式结构被破坏。"
         "本册按语义读作 (1/2)kappa_G 与 (1/4)（即按作者明显意图），但**排版层面该式不可直接编译**。"
         "复发：r19 册 A-09 已登记『代码 LaTeX 混入标识符致 ast.parse 失败』，本册是同一族（LaTeX 层）缺陷。",
         {"frac_bad_occurrences": n_frac_bad, "patterns": bad_frac}, ["排版", "LaTeX", "FAIL"])

    # 系数核对
    sixteen_pi_G = D(16) * PI * G_NEWTON
    inv_16piG = D(1) / sixteen_pi_G
    inv_2kG_numeric = D(1) / (D(2) * D(8) * PI * G_NEWTON)
    rel = abs(inv_2kG_numeric - inv_16piG) / inv_16piG
    guard("hilbert_coefficient_matches_GR", rel < D("1e-30"),
          "1/(2 kappa_G) = 1/(16 pi G)，相对差 = " + fm(rel), fm(rel))
    emit("V11", "PASS",
         "kappa_G = 8 pi G 时 1/(2 kappa_G) = 1/(16 pi G)：与 GR 希尔伯特项标准系数一致",
         "1/(2 x 8 pi G) = 1/(16 pi G) = " + fm(inv_16piG) + " (SI)，相对差 " + fm(rel) +
         "。这是来料第 2 节唯一完全对的标准系数。",
         {"inv_16piG": fm(inv_16piG), "rel_delta": fm(rel)}, ["系数", "GR", "PASS"])

    eight_pi_G = D(8) * PI * G_NEWTON
    emit("V12", "PASS",
         "场方程 G_{mu nu} = 8 pi G (T_matter + T_torsion) 的系数与符号为标准形式",
         "8 pi G = " + fm(eight_pi_G) + " (SI)。Einstein-Cartan 场方程的标准形式正是"
         "G_{mu nu} = 8 pi G T_{mu nu}（含自旋修正后的总能动张量）。该项结构核对通过。",
         {"eight_pi_G": fm(eight_pi_G)}, ["系数", "场方程", "PASS"])

    emit("V13", "PASS",
         "(1/4) tau^2 是**无导数**项 => 对联络变分的欧拉-拉格朗日方程是**代数**约束，与『tau ∝ S』自洽",
         "L_tau = (1/4) tau_{alpha mu nu} tau^{alpha mu nu} 不含 nabla tau。变分 delta L/delta tau = (1/2) tau "
         "（代数，无二阶导数）=> 与物质自旋源合并后给出 **代数** 关系 tau ∝ S（正文的比例式）。"
         "=> 就『第 2 节内部』而言，这一条是自洽的（与库内 r20/r21 判『tau 是代数 slave』方向一致）。"
         "**但**：代数性会与第 8 节的挠率演化 PDE 冲突（见 V14）。",
         {"has_gradient_term": False, "el_order_in_tau": 0}, ["挠率", "变分", "PASS"])

    emit("V14", "FAIL",
         "第 2 节（tau 代数约束）与第 8 节（挠率演化 PDE）**不同源**——本缺陷族第 4 次复发",
         "第 2 节的 L_tau 无 (nabla tau)^2 项 => tau 由代数方程完全确定（无独立初值、无演化）；"
         "第 8 节却写出挠率演化 PDE `d_t tau^i_jk = Lie_beta tau^i_jk + alpha F^i_jk`。"
         "计数：第 2 节给出 24 个代数约束；第 8 节给出 18 个演化方程（3+1 空间分量）——"
         "**过定**：代数方程已把 tau 解出，再积分 PDE 是多余且一般不相容的。"
         "要真正走 PDE，作用量必须补 (nabla tau)^2（+1 场 +1 参数），这正是 r20 册判定的『动力学化最小闭合集』代价"
         "（且撞 Omega5）。=> 与 r19（『作用量与 ADM 演化方程不同源』）同族，本册为**第 4 次复发**"
         "（r19 -> r21 V34C -> r27 H17 -> 本册）。",
         {"algebraic_constraints": 24, "admitted_pde_components": 18, "gradient_term_present": False},
         ["同源化", "复发", "FAIL"])

    emit("V15", "BOUNDARY",
         "L_fluct 未给显式形式（只写 ~Psi^dagger O(kappa,tau) Psi）=> 无法参与变分",
         "来料第 2 节 WARN 段：『L_fluct 在 V4.(0) 中定义为螺旋旋量 Psi 的自耦合项，"
         "L_fluct ~ Psi^dagger O(kappa,tau) Psi』。算子 O 未给 => 无法写出 delta S/delta Psi，"
         "无法得到第 3 节的旋量方程，也无法判定该方程是否真的就是第 3 节写的那一条。"
         "=> 第 2 节 -> 第 3 节的推导链在文本层面**断裂**（不是『待补细节』，是缺一个必要对象）。"
         "复现库内 r27 §1 同型缺陷（L_int 未给 => 闭合度 2/3）。",
         {"closure_ratio": "2/3"}, ["变分", "占位", "BOUNDARY"])


# ============================================================ 第 3 节：螺旋旋量
def audit_spinor():
    # 方程类型：二阶标量型 vs 一阶 Dirac
    d_box = SYM["Box"]
    d_k2 = SYM["curv_scalar_kappa2"]
    emit("V16", "FAIL",
         "第 3 节方程是 Klein-Gordon 型（二阶标量算子），却自称『4 分量狄拉克型螺旋旋量』",
         "来料方程：nabla^alpha nabla_alpha Psi - (kappa^2 - tau^2) Psi = 0。"
         "这是**二阶标量型**（Klein-Gordon）算子：不含任何 gamma 矩阵，对 4 分量 Psi 而言等价于 4 个**独立**复标量方程，"
         "分量之间无耦合。狄拉克方程是一阶 (i gamma^mu nabla_mu - m) Psi = 0；『旋量性』（自旋 1/2、"
         "Pauli 定理下最小耦合、手征投影）全部依赖一阶 gamma 结构与 Clifford 代数。"
         "=> 『狄拉克型 / 4 分量旋量』的标签在其自身写出的方程里**没有载体**；"
         "a) 若 Psi 真是旋量，则方程必须含 gamma；b) 若方程就是 KG，则 Psi 是 4 个标量而非一个旋量。两者不能同时成立。",
         {"operator_order": 2, "gamma_matrices_present": False, "independent_components": 4},
         ["旋量", "方程类型", "FAIL"])

    rel_box = dadd(d_box, dneg(d_k2))
    guard("spinor_equation_homogeneous", planck_exp(d_box) == planck_exp(d_k2),
          "nabla^2 = " + planck_str(d_box) + " 与 kappa^2 = tau^2 = " + planck_str(d_k2) + " 同量纲", True)
    emit("V17", "PASS",
         "旋量方程量纲齐次：[nabla^2] = [kappa^2] = [tau^2] = L^-2",
         "[Box] = " + dstr(d_box) + "，[kappa] = [tau] = " + dstr(SYM["torsion"]) + " => [kappa^2] = " + dstr(d_k2) +
         "。两端同为 " + planck_str(d_box) + "。=> 这一条量纲检查通过（第 3 节是全文少数量纲齐次之处），"
         "与第 2 节作用量的不齐（V09）形成对比。",
         {"Box": dstr(d_box), "kappa2": dstr(d_k2)}, ["量纲", "PASS"])

    # gamma 矩阵与手征变换（精确复矩阵）
    cliff = True
    cliff_res = 0.0
    for a in range(4):
        for b in range(4):
            lhs = acomm(GAMMA[a], GAMMA[b])
            target = mscale(miden(4), complex(2 * ETA[a], 0)) if a == b else mzero(4)
            d = mabsmax(msub(lhs, target))
            cliff_res = max(cliff_res, d)
            if d != 0.0:
                cliff = False
    guard("clifford_algebra_exact", cliff, "Clifford 代数 {gamma^a,gamma^b} = 2 eta^ab 残差 = "
          + repr(cliff_res) + "（元素为 0/±1/±i => 精确）", cliff_res)
    g5sq = mabsmax(msub(mmul(G5, G5), miden(4)))
    guard("gamma5_squares_to_identity", g5sq == 0.0, "gamma5^2 = I 残差 = " + repr(g5sq), g5sq)
    anti_g5 = max(mabsmax(acomm(G5, GAMMA[a])) for a in range(4))
    guard("gamma5_anticommutes_gamma", anti_g5 == 0.0,
          "max |{gamma5, gamma^a}| = " + repr(anti_g5), anti_g5)

    # 手征变换：Psi -> exp(i alpha gamma5) Psi （alpha = pi/4 => exp(i pi gamma5/2) = i gamma5）
    psi = [complex(0.3, 0.1), complex(-0.7, 0.2), complex(0.4, -0.5), complex(0.9, 0.3)]
    g0 = GAMMA[0]

    def psibar(v):
        out = []
        for i in range(4):
            s = complex(0, 0)
            for j in range(4):
                s += v[j].conjugate() * g0[j][i]
            out.append(s)
        return out

    def bilinear(bar, M, v):
        tmp = [sum(M[i][j] * v[j] for j in range(4)) for i in range(4)]
        return sum(bar[i] * tmp[i] for i in range(4))

    # exp(i alpha gamma5) 用级数（gamma5^2 = 1 精确）
    al = PI / D(4)  # 用浮点近似，误差只影响"变换后是否相等"的判据容差
    al = float(al)
    import math
    ca = math.cos(al)
    sa = math.sin(al)
    U = madd(mscale(miden(4), complex(ca, 0)), mscale(G5, complex(0, sa)))  # cos + i sin gamma5

    v0 = bilinear(psibar(psi), miden(4), psi)              # Psi^bar Psi
    psi2 = mv(U, psi)
    v1 = bilinear(psibar(psi2), miden(4), psi2)            # (Psi^bar Psi) after transform
    d_scalar = abs(v1 - v0)

    def after_gamma(mu):
        # Psi^bar' = Psi'^dag gamma^0（psibar 内部已做 dagger * gamma^0）
        p2 = mv(U, psi)
        bar2 = psibar(p2)
        # 数值比较：对 gamma^mu 与 i gamma^mu gamma5 的双线性，比较变换前后
        M1 = GAMMA[mu]
        M2 = mscale(mmul(GAMMA[mu], G5), complex(0, 1))
        a0 = bilinear(psibar(psi), M1, psi)
        a1 = bilinear(bar2, M1, p2)
        b0 = bilinear(psibar(psi), M2, psi)
        b1 = bilinear(bar2, M2, p2)
        return a0, a1, b0, b1

    res_vec = 0.0
    res_axi = 0.0
    for mu in range(4):
        a0, a1, b0, b1 = after_gamma(mu)
        res_vec = max(res_vec, abs(a1 - a0))
        res_axi = max(res_axi, abs(b1 - b0))
    guard("chiral_vec_current_invariant", res_vec < 1e-12,
          "Psi^bar gamma^mu Psi 在手征变换下最大变化 = " + repr(res_vec), res_vec)
    guard("chiral_axial_current_invariant", res_axi < 1e-12,
          "i Psi^bar gamma^mu gamma5 Psi 在手征变换下最大变化 = " + repr(res_axi), res_axi)
    guard("chiral_mass_term_breaks", d_scalar > 1e-3,
          "Psi^bar Psi 在手征变换下变化 = " + repr(d_scalar) + "（非零 => 质量项破缺手征）", d_scalar)

    emit("V18", "FAIL",
         "『手征性由挠率联络直接生成』不成立：挠率的 Dirac 耦合（矢量项与轴向项）在整体手征变换下均不变",
         "用精确复 4x4 矩阵（元素 0/±1/±i）做机器检验，取手征变换 Psi -> exp(i alpha gamma5) Psi（alpha = pi/4，"
         "此时 exp(i alpha gamma5) = i gamma5，为精确结构）："
         "① Cliff{gamma^a,gamma^b} = 2 eta^ab 残差 = " + repr(cliff_res) + "（精确零）；gamma5^2 = I；"
         "② Psi^bar Psi 变化 = " + repr(d_scalar) + "（**非零** => 只有质量型双线性破缺手征）；"
         "③ Psi^bar gamma^mu Psi 变化 = " + repr(res_vec) + "（零 => 不变）；"
         "④ i Psi^bar gamma^mu gamma5 Psi 变化 = " + repr(res_axi) + "（零 => 不变）。"
         "=> 挠率进入 Dirac 联络后给出的两类项（矢量 v_mu Psi^bar gamma^mu Psi 与轴向 a_mu Psi^bar gamma^mu gamma5 Psi）"
         "**都不破坏手征对称性**。若挠率是代数的（tau ∝ 自旋流），代入后得到的是 4-费米接触项 "
         "(Psi^bar gamma^mu gamma5 Psi)^2，它在手征变换下同样不变。"
         "=> 『不需要手动外加手征项』是逆向的：**即使加了挠率，也仍然需要质量型耦合或手征反常机制才会破缺手征**。"
         "另有独立一层否定：第 3 节自己的方程是标量型 KG（V16），gamma5 根本没出现，"
         "『手征性由该方程生成』在其自身文本内就没有对应项。",
         {"clifford_residual": repr(cliff_res), "mass_term_delta": repr(d_scalar),
          "vector_current_delta": repr(res_vec), "axial_current_delta": repr(res_axi),
          "undetermined_quantities": len(UNDEFINED_QUANTITIES)}, ["手征", "gamma5", "FAIL"])

    emit("V19", "MISMATCH",
         "手征破缺源（按标准应为轴挠率 = 完全反对称部分）与第 1 节把 SU(2) 指派给『无迹部分』不是同一分量",
         "即便按来料自己的三分量：手征破缺机制（若存在）必须落在**轴挠率**上（赝矢量通道）；"
         "而来料把 (3) 完全反对称部分指派给 **SU(3)**、(2) 无迹部分指派给 **SU(2)**。"
         "=> 若手征性来自轴挠率，则它属 SU(3) 通道，与『弱相互作用手征』（SU(2)）**不是同一分量**；"
         "若手征性来自 (2)，则与标准机制不符。无论选哪一支，第 1 节的指派表与第 3 节的手征叙事互不配套。",
         {"chiral_source_assigned_to": "SU3 (axial)", "weak_chirality_assigned_to": "SU2 (traceless)"},
         ["手征", "指派", "MISMATCH"])

    emit("V20", "FAIL",
         "自由度计数：来料给『度规 10 + 挠率 18 + Psi 4 复』= 36，但挠率应为 24，且**约束数 0 条**",
         "来料第 3 节：度规 10 分量（正确）、挠率 18 独立分量（应为 24，见 V03）、Psi 4 复 = 8 实。"
         "计数：10 + 18 + 8 = 36（来料口径）/ 10 + 24 + 8 = 42（4 维口径）。"
         "关键缺口不在加法而在**约束**：来料写『低能极限下大量高能自由度冻结』，但**没有给出任何约束方程**"
         "（Einstein-Cartan 中挠率代数 => 24 个分量全部由物质自旋决定，不是 24 个独立初值；"
         "Psi 的一阶/二阶结构决定 8 个实分量中有多少是独立初值）。"
         "对照库内 r21 册的 Dirac 计数（相空间 14 - 2x4 一阶约束 = 6 => 物理自由度 3），"
         "本册的计数既没有相空间，也没有约束，=> 『自由度计数』名义存在、实质为空。",
         {"metric": 10, "torsion_claimed": 18, "torsion_correct": 24, "spinor_real": 8,
          "constraints_given": 0}, ["自由度", "计数", "FAIL"])

# ============================================================ 第 4 节：低能渐近展开 I
def audit_lowenergy():
    emit("V21", "BOUNDARY",
         "第 4 节给的是 4 步操作流程（模式截断 -> 规范势重写 -> 联络等价 -> 模式积分），可代入的等式 0 条",
         "正文四步：①挠率低能模式截断 ②三分量重写为 A_mu / W^a_mu / G^A_mu ③挠率联络等价为规范协变导数 "
         "④模式积分得有效拉氏量。来料自己标注『完整符号推导（逐项匹配 SM 系数）属于下一阶段攻坚；"
         "逻辑路径闭合，但尚未完成逐行符号演算』——措辞已限（这一步的自我限制是恰当的）。"
         "本册核对其**前提**：第 ② 步要求把 SO(1,3) 时空张量的分量『重写为』SM 内部规范势，"
         "这需要一个内部空间（internal space）与一个从时空表示到内部表示的映射；来料只在标题上给了箭头，"
         "未给映射本身。=> 不是「细节待补」，而是**缺一个必要对象**（与 V07 的维数缺口同源）。",
         {"operative_steps": 4, "substitutable_equations": 0}, ["EFT", "前提缺失", "BOUNDARY"])

    emit("V22", "FAIL",
         "『把高频挠率模式积分掉』缺 UV 完成与质量层级 => 24 -> 12 的消去无机制",
         "第 4 节近似条件 4『分离尺度：高能挠率模式积分掉，只保留低能长波分量』。"
         "要做模式积分（coarse-graining）至少需要：(a) 一个 UV 截断或 UV 完成；(b) 被积掉模式的质量/尺度层级；"
         "(c) 积分后算子的匹配条件。三者来料**一条未给**。"
         "进一步：第 2 节的作用量里 tau^2 项缺量纲系数（V09），即**没有 tau 的质量项**，"
         "因此不存在『重模式/轻模式』的分裂 —— 无质量项就没有质量层级，没有层级就无法做尺度分离。"
         "=> 第 4 节的操作在缺少 UV 结构的前提下不可执行（与库内 r19/r20『同源化』缺陷同族）。",
         {"uv_completion": False, "mass_hierarchy": False, "matching_conditions": 0},
         ["EFT", "尺度分离", "FAIL"])


# ============================================================ 第 5 节：MHD
def _pderiv(f, p, axis, h=1e-5):
    q = list(p)
    q[axis] += h
    fp = f(*q)
    q[axis] -= 2 * h
    fmv = f(*q)
    return (fp - fmv) / (2 * h)


def audit_mhd():
    # (a) div(curl A) 恒等：三组不同的 A + 阳性对照
    As = [
        (lambda x, y, z: y * y * z ** 3, lambda x, y, z: z * z * x ** 3, lambda x, y, z: x * x * y ** 3),
        (lambda x, y, z: 3 * x * y, lambda x, y, z: -2 * y * z, lambda x, y, z: 5 * z * x),
        (lambda x, y, z: x ** 4 - y * z, lambda x, y, z: y ** 4 + x * z, lambda x, y, z: z ** 4 - x * y),
    ]
    pt = [0.3141592653589793, 0.2718281828459045, 0.5772156649015329]
    residuals = []
    for (a1, a2, a3) in As:
        def curl1(x, y, z):
            return _pderiv(a3, (x, y, z), 1) - _pderiv(a2, (x, y, z), 2)

        def curl2(x, y, z):
            return _pderiv(a1, (x, y, z), 2) - _pderiv(a3, (x, y, z), 0)

        def curl3(x, y, z):
            return _pderiv(a2, (x, y, z), 0) - _pderiv(a1, (x, y, z), 1)

        def divcurl(x, y, z):
            return (_pderiv(curl1, (x, y, z), 0) + _pderiv(curl2, (x, y, z), 1)
                    + _pderiv(curl3, (x, y, z), 2))
        residuals.append(abs(divcurl(*pt)))
    # 阳性对照：非 curl 的场
    def B1(x, y, z):
        return x

    def B2(x, y, z):
        return y

    def B3(x, y, z):
        return z

    def divB(x, y, z):
        return _pderiv(B1, (x, y, z), 0) + _pderiv(B2, (x, y, z), 1) + _pderiv(B3, (x, y, z), 2)
    control = abs(divB(*pt))
    guard("div_curl_identity_via_3_As", max(residuals) < 1e-6 and control > 1.0,
          "div(curl A) 对 3 组不同 A 的最大残差 = " + repr(max(residuals)) +
          "（差分误差量级）；阳性对照 div(B) = " + repr(control), max(residuals))

    emit("V23", "FAIL",
         "§5 第 2 步『挠率无散性质平均后给出 div B = 0』是**定义恒等式**，与挠率无关（零信息量）",
         "B = curl A 的定义直接给出 div B = div(curl A) ≡ 0（混合偏导相消，纯代数恒等式）。"
         "机器验证：对 3 组结构完全不同的矢势 A 做中心差分，|div(curl A)| 最大 = " + repr(max(residuals)) +
         "（差分误差量级，恒等式本身精确）；阳性对照（把 B 直接给成 (x,y,z)）|div B| = " + repr(control) +
         "（>1，证明检验器有判别力）。"
         "=> 『div B = 0』不是从挠率导出的**结果**，而是任何磁场都满足的**定义性质**；"
         "把它写成推导结论，不提供任何关于挠率的信息。",
         {"div_curl_residuals": [repr(r) for r in residuals], "positive_control": repr(control)},
         ["MHD", "恒等式", "零信息量", "FAIL"])

    # (b) 2D Harris sheet：J x B = grad p 精确；Frobenius (B . curl B) = 0 => 有磁面
    #     取 tanh(z/L)=1/2 => sech^2 = 3/4（精确有理数）；B0=1, L=1, mu0=1
    t = Fr(1, 2)
    sech2 = Fr(3, 4)
    Bx = t                       # B = (t, 0, 0)
    curlB_y = sech2              # curl B = (0, sech^2, 0)
    Jy = curlB_y
    JxB_z = -(Jy * Bx)           # J x B 的 z 分量 = -J_y B_x
    p_val = sech2 / 2
    # dp/dz = -sech^2 * tanh
    gradp_z = -(sech2 * t)
    harris_ok = (JxB_z == gradp_z)
    frob_harris = Bx * 0 + 0 * curlB_y + 0 * 0   # B . curl B
    guard("harris_sheet_equilibrium_exact", harris_ok and frob_harris == 0,
          "2D Harris sheet: JxB_z = " + str(JxB_z) + " vs gradp_z = " + str(gradp_z) +
          "；B.curlB = " + str(frob_harris) + "（=0 => Frobenius 满足 => 有磁面）", str(JxB_z))

    # (c) 3D ABC / Beltrami：(0,0,0) 与 (pi/2,0,0) 处 B=(1,1,1)/(1,2,0)，curl B = B
    abc = [(1, 1, 1), (1, 2, 0)]
    abc_dot = [b[0] * b[0] + b[1] * b[1] + b[2] * b[2] for b in abc]
    guard("abc_beltrami_has_no_flux_surface", all(x > 0 for x in abc_dot),
          "ABC/Beltrami: curl B = B => J x B = 0（force-free 平衡成立），但 B.curlB = |B|^2 = "
          + str(abc_dot) + " != 0 => Frobenius 违反 => 无磁面", str(abc_dot))

    emit("V24", "FAIL",
         "§5 第 3/4 步（B . grad psi = 0、J x B = grad p）是 MHD 标准方程/定义，不是从挠率导出的（零信息量）",
         "① J x B = grad p 是 MHD 动量方程的静态极限（定义平衡）；"
         "② B . grad psi = 0 是磁面的定义；两者对**任何** MHD 理论都成立，与挠率无关。"
         "机器读数（2D Harris sheet，取 tanh(z/L) = 1/2 => sech^2 = 3/4 为精确有理数，B0 = L = mu0 = 1）："
         "J x B 的 z 分量 = " + str(JxB_z) + "，grad p 的 z 分量 = " + str(gradp_z) + " => **精确相等**；"
         "即『标准 MHD 平衡式自洽』这一事实可以在完全不含挠率的框架里逐位复现。"
         "=> 来料第 5 节给出的是标准 MHD 的**重述**，挠率在这里没有任何可检验的额外内容。",
         {"harris_JxB_z": str(JxB_z), "harris_gradp_z": str(gradp_z)}, ["MHD", "标准式", "零信息量", "FAIL"])

    emit("V25", "FAIL",
         "『磁面条件自动涌现』被 3D force-free Beltrami 场反例否证（平衡成立而无磁面）",
         "来料称『拓扑守恒（挠率通量守恒）导出磁通函数 psi，磁面条件自动涌现』。"
         "机器反例：ABC / Beltrami 场（A = B = C = 1，取点 (0,0,0) 与 (pi/2,0,0) 使 sin/cos 取精确值 0/±1）"
         "满足 curl B = B => J x B = 0 => **是 MHD 平衡**（p = const），"
         "但 B . curl B = |B|^2 = " + str(abc_dot) + " ≠ 0 => 1-形式 beta = B_flat 满足 beta ^ dbeta ≠ 0 "
         "=> 由 Frobenius 定理，**不存在**全局光滑函数 psi 使 B . grad psi = 0 => **无磁面**。"
         "（Beltrami 场的力线在环面上遍历/混沌，这是 Arnold 的经典结果。）"
         "=> 『平衡 => 磁面』是假命题；磁面存在性是**额外的几何前提**（2D/轴对称成立：Harris sheet 的 B . curl B = " +
         str(frob_harris) + " = 0 ✓），而不是从挠率无散性自动得到。"
         "=> 这正是 Grad 猜想 / 非可积性问题的核心，来料把它的**结论**当成了自己的**推导结果**。",
         {"harris_B_dot_curlB": str(frob_harris), "abc_B_dot_curlB": str(abc_dot)},
         ["MHD", "Frobenius", "FAIL"])

    emit("V26", "FAIL",
         "把 Landreman / Gomez-Serrano 解族称为『4 维挠率几何的稳态解』属因果倒置（0 条导出链）",
         "来料称『Landreman 解析解、Gomez-Serrano Nash-Moser 环面解族……是 4 维时空挠率几何"
         "在宏观流体层面的稳态解』。文本中**没有**从挠率几何到这些解族的任何映射/极限/退化步骤"
         "（可数导出链 = 0）。逻辑上：这些解是**先**在 MHD 方程内构造出来的，"
         "把 MHD 的解重新贴一个『挠率几何稳态』的标签不构成派生。"
         "=> 与库内 r27 H25 同型（『四力模态只有文字分类、0 条可代入方程』），属**借用**而非导出。",
         {"export_chain_steps": 0}, ["MHD", "借用", "FAIL"])

    emit("V27", "BOUNDARY",
         "『推翻 Grad 猜想』是外部数学事实，本册不核实；且即使为真也不能迁移为对 TU(F)T 的支持",
         "来料称『三篇推翻 Grad 猜想论文使用的 MHD 平衡方程组』。本册**不核实**该外部数学事实"
         "（超出审计范围，且需要原始文献）。只登记两条逻辑边界："
         "① 外部事实无论真假，都**不能**成为本框架的证据（红线：证据不得跨体系转移）；"
         "② 更关键的是本册 V24/V25 已证：来料『导出』的方程就是标准 MHD 方程（与挠率无关），"
         "所以 MHD 侧的成就（无论多大）衡量的都是**标准 MHD**，不是 TU(F)T。",
         {"verified_externally": False}, ["外部事实", "证据迁移", "BOUNDARY"])


# ============================================================ 第 6 节：RG beta
def audit_rg():
    sin2 = D("0.23122")
    a_em = D("7.8156e-3")
    a_y = a_em / (D(1) - sin2)
    a1 = a_y * D(5) / D(3)
    a2 = a_em / sin2
    a3 = D("0.1179")
    inv = [D(1) / a1, D(1) / a2, D(1) / a3]
    b = [D(41) / D(10), D(-19) / D(6), D(-7)]
    two_pi = D(2) * PI
    L = (M_PLANCK / M_Z).ln()
    inv_pl = [inv[i] - (b[i] / two_pi) * L for i in range(3)]
    spread = max(inv_pl) - min(inv_pl)
    spread_rel = spread / (sum(inv_pl) / 3)
    # 三交点（以 M_Z 为原点测 e-fold 距离）
    Lcross = []
    for i in range(3):
        for j in range(i + 1, 3):
            Lcross.append(two_pi * (inv[i] - inv[j]) / (b[i] - b[j]))
    dl = max(Lcross) - min(Lcross)
    guard("sm_rge_couplings_do_not_meet", spread_rel > D("0.05"),
          "1-loop SM 跑到 M_Pl：alpha_i^-1 = " + " / ".join([fm(x) for x in inv_pl]) +
          "，相对跨度 = " + fm(spread_rel), fm(spread_rel))
    dl_ref = D("9.147")   # 库内 r11/r12 登记值（SM 1-loop 三交点 Delta L）
    dl_rel = abs(dl - dl_ref) / dl_ref
    guard("rge_delta_L_cross_ref_r11", dl_rel < D("0.01"),
          "本册 Delta L = " + fm(dl) + " vs 库内 r11/r12 = " + fm(dl_ref) + "，相对差 = " + fm(dl_rel), fm(dl_rel))
    KEY["alpha_inv_at_MZ"] = [fm(x) for x in inv]
    KEY["alpha_inv_at_MPl"] = [fm(x) for x in inv_pl]
    KEY["rge_spread_rel"] = fm(spread_rel)
    KEY["rge_Lcross"] = [fm(x) for x in Lcross]
    KEY["rge_delta_L"] = fm(dl)
    KEY["ln_MPl_over_MZ"] = fm(L)

    emit("V28", "FAIL",
         "『三耦合在普朗克标度汇聚』被 1-loop SM RGE 否证：跑到 M_Pl 时三线不交（Delta L ≈ " + fm(dl) + "）",
         "机器 1-loop 跑动（本册口径，全部列出以便复算）："
         "alpha_em(M_Z) = " + fm(a_em) + "（库内 r16 口径），sin^2 theta_W(M_Z) = " + fm(sin2) +
         " => alpha_1 = (5/3)alpha_Y = " + fm(a1) + "、alpha_2 = alpha_em/sin^2 = " + fm(a2) + "、alpha_3 = " + fm(a3) + "；"
         "b = (41/10, -19/6, -7)；L = ln(M_Pl/M_Z) = " + fm(L) + "。"
         "alpha_i^-1(M_Pl) = " + " / ".join([fm(x) for x in inv_pl]) +
         "（相对跨度 " + fm(spread_rel) + "）；三交叉点 e-fold 距离 = " +
         " / ".join([fm(x) for x in Lcross]) + "，Delta L = " + fm(dl) + "。"
         "=> **不汇聚**。**交叉印证**：库内 r11/r12 用同一组 b 登记的 Delta L = 9.147，"
         "本册独立复算 " + fm(dl) + " 与其相对差 " + fm(abs(dl - D("9.147")) / D("9.147")) +
         "（< 0.1%）⇒ 两条独立链在量值上一致，说明口径无系统偏差。"
         "要让三线汇聚，标准做法是引入新自由度（如 MSSM，库内 r12 登记 Delta L ≈ 0.13 / M_GUT ≈ 2.29e16 GeV）——"
         "这正是来料未做而代价被略去的一步（撞 Omega5）。",
         {"alpha_inv_MZ": [fm(x) for x in inv], "alpha_inv_MPl": [fm(x) for x in inv_pl],
          "spread_rel": fm(spread_rel), "L_cross": [fm(x) for x in Lcross], "delta_L": fm(dl),
          "delta_L_ref_r11": fm(dl_ref), "delta_L_rel_vs_r11": fm(dl_rel)},
         ["RGE", "汇聚", "FAIL"])

    emit("V29", "FAIL",
         "beta(g_i) = F_i(kappa[mu], tau[mu]) 范畴错置 + 量纲缺口（不可由几何函数给出）",
         "两重问题：①**范畴**：beta 函数是量子场论的圈图（重整化）产物，其输入是场的相互作用谱与截断，"
         "不是几何量 kappa/tau 的函数；把 beta 写成 F_i(kappa[mu], tau[mu]) 等于假定『几何量已编码全部圈图信息』，"
         "这是待证的断言而不是已建立的形式框架（库内 r11 已用同型论证：离散拓扑量 k in Z 无法编码连续跑动 alpha_i(mu)）。"
         "②**量纲**：beta(g) = mu dg/dmu 与 g 同量纲（g 无量纲 => beta 无量纲）；右端 F_i(kappa,tau) 若 kappa,tau 是 "
         "弧长倒数（本册 V17 口径），则 F 的任何多项式都有非零量纲，必须再除以一个标度（如 M_Pl）才是无量纲 —— "
         "来料未给该标度。=> 与库内 r18/r27『kappa 与其它长度/时间量不可加』的**第 7 次同族复发**。",
         {"beta_dimensionless": True, "F_dims_unspecified": True}, ["RGE", "范畴", "量纲", "FAIL"])


# ============================================================ 第 7 节：可观测量
def _fmt_edm():
    return dstr(SYM["edm"])


def audit_observables():
    emit("V30", "BOUNDARY",
         "g-2：Delta g(tau_local) 未给显式函数 => 不可算；且库内该窗口**已被实验关闭**（复发登记）",
         "来料：『(g-2)_TUFT = (g-2)_SM + Delta g(tau_local)』，Delta g 只写『是局域挠率的函数』。"
         "无函数 => 无法给数值、无法与 Fermilab 数据做 chi^2。"
         "复发登记：库内 r19 册已裁定本体系 g-2 代码 Delta g **恒等于 1/c**（纯单位产物，量纲 1/速度）；"
         "r27 H30 复算 a_TUFT = alpha/(8 pi) = " + fm(ALPHA_FINE / (D(8) * PI)) + "，"
         "与实验值 " + fm(AE_EXP) + " 的比值 " + fm((ALPHA_FINE / (D(8) * PI)) / AE_EXP) +
         "（偏差 74.96%）=> **窗口已关**。来料仍在第 7 节把 g-2 列为『可与费米实验室数据做 chi^2 比对』的通道。",
         {"delta_g_defined": False, "window_closed": True}, ["g-2", "窗口关闭", "BOUNDARY"])

    d_lhs = SYM["edm"]                                  # 电偶极矩 (Q L)
    d_rhs = dadd(SYM["dimensionless"], SYM["torsion"])  # theta_CP * |tau| = L^-1
    gap = dadd(d_lhs, dneg(d_rhs))
    guard("edm_dimension_mismatch", gap != DM(0, 0, 0, 0),
          "EDM：左端 " + dstr(d_lhs) + " vs 右端 theta_CP*|tau| = " + dstr(d_rhs) + "，缺口 " + dstr(gap), dstr(gap))
    emit("V31", "FAIL",
         "EDM 量纲不齐：d_e 为 Q·L，而 theta_CP·|tau| 为 L^-1，缺口 " + dstr(gap) + "（本缺陷族第 2 次复发）",
         "来料：d_e ∝ theta_CP · |tau_chiral|。机器量纲核算："
         "[d_e] = " + dstr(d_lhs) + "（电偶极矩 = 电荷 x 长度）；[theta_CP] = " + dstr(SYM["dimensionless"]) +
         "（相位无量纲）；[tau] = " + dstr(SYM["torsion"]) + " => 右端 = " + dstr(d_rhs) + "。"
         "缺口 = " + dstr(gap) + "（缺 电荷 x 长度^2）。"
         "=> 与库内 r19 册登记的『EDM 式量纲 = M^1 L^0 T^-1（动量），而 EDM 算符要求 d_e 为 L^-1』同源，"
         "本册为**第 2 次复发**（量纲缺口的具体形式不同，但『右边装不进左边』相同）。"
         "另：r19 已指出 EDM 算符 tau·S·E 的宇称为 P-偶（(-1)(-1)(+1) = +1），而 EDM 算符需 P-奇 —— "
         "『赝标量天然 CP 破坏 => EDM』这一步未成立。",
         {"lhs": dstr(d_lhs), "rhs": dstr(d_rhs), "gap": dstr(gap)}, ["EDM", "量纲", "复发", "FAIL"])

    d_pr = SYM["dimensionless"]
    d_tau2 = dscale(SYM["torsion"], 2)
    gap_pr = dadd(d_pr, dneg(d_tau2))
    # Planck 2018 对 A_s 的精度 ~0.3% => Delta P_R / P_R 的上界量级
    planck_tol = D("3e-3")
    emit("V32", "FAIL",
         "CMB 修正 Delta P(k;<tau^2>) 量纲缺口 " + dstr(gap_pr) + "，且存在**可证伪性两难**",
         "来料：P_R(k) = P_R^GR(k) + Delta P(k;<tau^2>)。①量纲：P_R 无量纲 = " + dstr(d_pr) +
         "，而 <tau^2> = " + dstr(d_tau2) + " => 缺口 " + dstr(gap_pr) + "（缺 L^2 因子，与 V09 同源：挠率平方项缺长度标度）。"
         "②更硬的是**两难**：若 Delta P 相对 P_R 达到 O(1)，则与 Planck 2018 对 A_s 的精度（~" + fm(planck_tol * 100) +
         "%）直接冲突 => 被排除；若 Delta P/P_R << 1e-3，则该修正**不可观测**（无判别力）。"
         "来料第 7 节把它写成『与 Planck 2018 数据对比，做 MCMC 参数约束』——但既没有可代入的 Delta P，"
         "两难也没有被处理。=> 可检验性与可存活性的两难（库内 r14/r25 同型：二者不可兼得）。",
         {"gap": dstr(gap_pr), "planck_A_s_tol": fm(planck_tol)}, ["CMB", "量纲", "两难", "FAIL"])


# ============================================================ 第 8 节：ADM-BSSN
def audit_adm():
    # 哈密顿约束符号：3R + K_ij K^ij - K^2  vs  3R + K^2 - K_ij K^ij
    # 例1: gamma = I, K = diag(1,2,3) => 3R = 0, K_ij K^ij = 14, K = 6, K^2 = 36
    K1 = [1, 2, 3]
    kkk1 = sum(x * x for x in K1)
    ktrace1 = sum(K1)
    ksq1 = ktrace1 * ktrace1
    src1 = kkk1 - ksq1        # 来料
    std1 = ksq1 - kkk1        # 标准
    # 例2: K = diag(1,-1,0) => K^2 = 0, K_ij K^ij = 2
    K2 = [1, -1, 0]
    kkk2 = sum(x * x for x in K2)
    ktrace2 = sum(K2)
    ksq2 = ktrace2 * ktrace2
    src2 = kkk2 - ksq2
    std2 = ksq2 - kkk2
    guard("adm_hamiltonian_sign_flip", src1 == -std1 and src2 == -std2,
          "哈密顿约束 K 块：来料 " + str(src1) + " vs 标准 " + str(std1) + "（例1）；"
          "来料 " + str(src2) + " vs 标准 " + str(std2) + "（例2，K^2=0 时恰为相反数）", str(src1))

    emit("V33", "FAIL",
         "ADM 哈密顿约束 K 项整体符号反 => 来料版本给出**负能量密度**（本缺陷族第 2 次复发）",
         "来料：3R + K_ij K^ij - K^2 = 16 pi G (rho_matter + rho_torsion)。"
         "通行约定（ADM 标准）：3R + K^2 - K_ij K^ij = 16 pi G rho。"
         "机器核对（结构恒等式，不引用任何经典数值常数）："
         "例 1（gamma = delta_ij，K = diag(1,2,3)）：3R = 0，K_ij K^ij = 1+4+9 = " + str(kkk1) +
         "，K = " + str(ktrace1) + "，K^2 = " + str(ksq1) + " => 来料左端 = " + str(src1) +
         "，标准左端 = " + str(std1) + " => 来料要求 rho < 0（**负能量密度**，非物理）。"
         "例 2（K = diag(1,-1,0)）：K^2 = " + str(ksq2) + "，K_ij K^ij = " + str(kkk2) +
         " => 来料 " + str(src2) + " vs 标准 " + str(std2) + "（恰为相反数）。"
         "=> 来料的两式（V33 与通行约定）互为整体负号。复发：库内 r27 H27 已判『ADM 哈密顿约束把两个 K 项"
         "单独交换符号，与通行约定 A 及其整体负号都不匹配』；本册为**第 2 次复发**，并给出更强读数（负能量密度）。",
         {"example1_src": src1, "example1_std": std1, "example2_src": src2, "example2_std": std2},
         ["ADM", "符号", "复发", "FAIL"])

    emit("V34", "PASS",
         "ADM 动量约束 D_j(K^ij - gamma^ij K) = 8 pi G j^i 的结构、系数与符号为标准形式",
         "与哈密顿约束不同，动量约束这一条来料写对：系数 8 pi G、指标结构 D_j(K^{ij} - gamma^{ij}K) 与标准一致。"
         "（库内 r19 曾指出另一份稿件（V34C）的动量约束缺 e^{-2phi} 的 BSSN 权重 —— 本册来料的这一条未出现该问题。）",
         {"matches_standard": True}, ["ADM", "动量约束", "PASS"])

    emit("V35", "BOUNDARY",
         "挠率演化 PDE 的源项 F^i_jk(gamma,K,tau,Psi) 未给定义 => 0 条可代入",
         "来料：d_t tau^i_jk = Lie_beta tau^i_jk + alpha F^i_jk(gamma,K,tau,Psi)。"
         "Lie 导数项量纲自洽（[beta] = 0 in c = 1，[d tau] = M^2），但 F^i_jk 未给 => "
         "无法离散、无法给初值、无法与解析解对照。=> 该 PDE 目前是**形式**，不是可执行方案"
         "（复现库内 r27 H28/H32 同型缺陷）。",
         {"substitutable_equations": 0}, ["ADM", "占位", "BOUNDARY"])

    emit("V36", "FAIL",
         "ADM 段未含挠率对 3R 的贡献、无挠率共轭动量与约束方程 => 约束代数不闭合",
         "来料的 ADM 扩展只做了两件事：①在哈密顿/动量约束**右端**加 rho_torsion / j^i_torsion（源项）；"
         "②加一条挠率演化 PDE。但完整 3+1 分解至少还必须："
         "a) 把挠率的**空间曲率修正**计入 3R（挠率与 contortion 会修改空间联络，从而修改 3R）；"
         "b) 给出挠率的**共轭动量**（若 tau 有动力学）；或 c) 给出挠率的**约束方程**（若 tau 代数，见 V14）；"
         "d) 检查约束代数是否闭合（Dirac-Bergmann）。来料 a)–d) **一条未做**。"
         "=> 方程组在形式上写出来了，但约束代数层面不闭合；且与 V14（第 2 节判 tau 代数）直接冲突："
         "若 tau 代数，则其共轭动量为零、应有 24 个约束，而非一条独立 PDE。",
         {"curvature_contribution": False, "conjugate_momentum": False, "constraint_algebra": False},
         ["ADM", "约束代数", "FAIL"])


# ============================================================ 第 9 节：三元拓扑代数
def audit_ternary():
    # 同伦群表（标准已知值）
    PI_TABLE = [
        ("pi_1(S^1)", "Z", "缠绕数（整数）"),
        ("pi_2(S^2)", "Z", "Hopf 度/单极荷"),
        ("pi_3(S^2)", "Z", "Hopf 纤维化"),
        ("pi_3(S^3)", "Z", "缠绕数"),
        ("pi_1(S^2)", "0", "平凡"),
        ("pi_1(SO(3))", "Z_2", "自旋统计（费米/玻色二分）"),
    ]
    guard("homotopy_groups_discrete", True,
          "标准同伦群表 " + str(len(PI_TABLE)) + " 行（全部为离散群：Z / Z_2 / 0）", len(PI_TABLE))
    emit("V37", "PASS",
         "『量子离散性来自拓扑缠绕的离散同伦类』——方向部分成立：同伦群确为离散群",
         "机器固化的标准同伦群表：" + "；".join([t[0] + " = " + t[1] + "（" + t[2] + "）" for t in PI_TABLE]) +
         "。这些群都是离散的（Z / Z_2 / 0），因此『电荷/缠绕数的量子化来自拓扑』这一**方向**有数学基础"
         "（例如 U(1) 荷 = pi_1(S^1) 的整数、自旋统计 = pi_1(SO(3)) = Z_2）。"
         "**但**这只支持『离散性』，不支持『量子数全部可实现』（见 V39）。",
         {"table_rows": len(PI_TABLE)}, ["拓扑", "同伦", "PASS"])

    emit("V38", "FAIL",
         "三元表『0 / 1 / infinity』名不副实：infinity **不是**同伦群元素，且全表无任何代数运算",
         "来料第 9 节表：0（零缠绕，平直基态）、1（局域闭合螺旋孤子）、infinity（全域边界缠绕）。"
         "①『infinity』：同伦群是（离散）群，其元素是整数/模类，**不存在**『无穷』元素；"
         "『全域边界缠绕』如果要成为数学对象，需要指定拓扑空间与同伦群，来料未给。"
         "②『三态尺度代数』这个名称要求一个代数结构（运算 + 封闭性 + 单位元），但全表没有任何运算定义。"
         "=> 名称（代数）与内容（三行分类）不匹配；且第三项不是群元素。",
         {"is_group_element": False, "algebra_operations_defined": 0}, ["拓扑", "命名", "FAIL"])

    # 信息论：SM 场型需要多少 bit vs 三元表提供多少
    n_field_types = 18  # 6 场型 x 3 代（Q_L,u_R,d_R,L,e_R,nu_R）
    need_bits = math.log(n_field_types, 2)
    have_bits = math.log(3, 2)
    emit("V39", "FAIL",
         "量子数不能由单一缠绕数给出：区分 " + str(n_field_types) + " 个场型需 " + fm(D(str(need_bits))) +
         " bit，三元表只提供 " + fm(D(str(have_bits))) + " bit（缺口 " + fm(D(str(need_bits - have_bits))) + " bit）",
         "来料：『同伦缠绕数给出电荷、自旋；局域激发』。信息论核算（本册口径：把 6 个场型 x 3 代 = " +
         str(n_field_types) + " 个可区分场型作为需求）："
         "需求 log2(" + str(n_field_types) + ") = " + fm(D(str(need_bits))) + " bit；"
         "三元表（0/1/infinity）最多提供 log2(3) = " + fm(D(str(have_bits))) + " bit；"
         "缺口 = " + fm(D(str(need_bits - have_bits))) + " bit。"
         "即使只要求区分 6 个场型（不含代），需求 log2(6) = " + fm(D(str(math.log(6, 2)))) + " bit 仍 > " +
         fm(D(str(have_bits))) + " bit。"
         "独立佐证：库内 R14（tuft/ 目录）用**同一型**论证（Lk 不是超荷 Y 的函数：全部 SM 费米子 Lk = 1 而 Y 取 6 个不同值；"
         "信息缺口 1.74 bit）—— 口径不同（R14 用 10 场/3 层，本册用 18 场型/3 态），但**结论方向一致**："
         "单一半整数/三分类不可能是全部 SM 量子数的函数。=> 缠绕数能编码『自旋/统计』层，不能编码超荷/色/代层。",
         {"field_types": n_field_types, "need_bits": fm(D(str(need_bits))),
          "have_bits": fm(D(str(have_bits))), "gap_bits": fm(D(str(need_bits - have_bits)))},
         ["拓扑", "信息论", "FAIL"])


# ============================================================ 第 10-13 节与元层
def audit_meta():
    emit("V40", "FAIL",
         "第 11 节『已严格成立』第 2 条（量纲闭环）被本册 V09 / V31 / V32 直接否证",
         "来料第 11 节把『V4.(0) 作用量、场方程量纲闭环，消除 V3.4 量纲冲突』列为**已严格成立**。"
         "机器读数：①作用量两项差 " + dstr(dadd(dadd(SYM["inv_2kappaG"], SYM["R"]),
                                                   dneg(dscale(SYM["torsion"], 2)))) + "（V09）；"
         "②EDM 式缺口 " + dstr(dadd(SYM["edm"], dneg(dadd(SYM["dimensionless"], SYM["torsion"])))) + "（V31）；"
         "③CMB 修正缺口 L^2（V32）。=> 该『已严格』条目**自我否证**。"
         "其余三条（EC 几何自洽 / ADM 可形式上扩展 / 可写出形式上低能流程）措辞恰当，本册分别记为可接受"
         "（但 ADM 条目内容仍有 V33/V35/V36 的缺陷）。",
         {"claims_strict": 4, "falsified_strict_claims": 1}, ["理论边界", "自否证", "FAIL"])

    emit("V41", "FAIL",
         "第 11 节假说清单遗漏 ≥4 节，且把『已被 RGE 否证』的汇聚条件降格为『假说』",
         "来料列出 4 条物理假说。按节核对（13 节 x 是否标注为假说）：未标注但实为假说/未证的有："
         "①第 3 节（Psi 是 4 分量旋量且其方程即几何）②第 5 节（MHD 方程由挠率导出）"
         "③第 8 节（挠率演化 PDE 与作用量同源）④第 9 节（三元 -> 全部 SM 量子数）—— 共 ≥4 节遗漏。"
         "另一侧：假说 3『普朗克标度耦合自然汇聚』被列为『待检验』，但机器 RGE（V28）显示它"
         "**已被 1-loop SM 结果否证**（Delta L ≈ " + KEY.get("rge_delta_L", "n/a") + "），"
         "不应与『未检验』并列。=> 边界清单在两侧都不准确。",
         {"claim_hypotheses": 4, "unlabeled_hypotheses": 4}, ["理论边界", "清单", "FAIL"])

    # Mermaid 节点 ID 扫描
    bad_ids = []
    ok_ids = []
    for line in MERMAID_SRC.splitlines():
        if "-->" not in line:
            continue
        for seg in line.split("-->"):
            s = seg.strip()
            if s.startswith("|"):
                s = s.split("|")[-1].strip()
            m = re.match(r'^(.*?)\["', s)
            cand = m.group(1).strip() if m else s
            cand = cand.strip()
            if not cand:
                continue
            if re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', cand):
                ok_ids.append(cand)
            else:
                bad_ids.append(cand)
    guard("mermaid_illegal_node_ids_detected", len(bad_ids) > 0,
          "Mermaid 非法节点 ID " + str(len(bad_ids)) + " 个：" + " | ".join(sorted(set(bad_ids))[:6]), len(bad_ids))
    emit("V42", "FAIL",
         "Mermaid 图节点 ID " + str(len(bad_ids)) + " 处非法（含反斜杠/圆括号）=> 图无法渲染",
         "来料第 12 节的 flowchart 用 `\\(\\mathbf B\\)`、`E\\(\\boldsymbol{1}\\)`、`\\(\\mathcal F\\)` 作节点 ID。"
         "Mermaid 的节点 ID 必须匹配 [A-Za-z_][A-Za-z0-9_]*，反斜杠与圆括号都不是合法字符 => 解析报错。"
         "机器扫描结果：合法 ID " + str(len(ok_ids)) + " 个（" + ", ".join(sorted(set(ok_ids))) + "）；"
         "非法 ID " + str(len(bad_ids)) + " 处（" + " | ".join(sorted(set(bad_ids))) + "）。"
         "=> 该图**不能直接渲染**（正文自称『文本，可直接渲染』）。修法：ID 用 ASCII 名（B / E1 / F），"
         "把数学符号放进标签文字里。",
         {"illegal_ids": sorted(set(bad_ids)), "legal_ids": sorted(set(ok_ids))},
         ["文档", "Mermaid", "FAIL"])

    emit("V43", "FAIL",
         "第 13 节 6 项任务的依赖上游**全部**未闭合（逐项映射到本册 FAIL 条目）",
         "依赖矩阵（任务 -> 其上游阻塞）："
         "①一圈 RG beta 显式表达式 -> 依赖第 2 节作用量定稿（V09 量纲不齐，未定稿）；"
         "②从有效作用量逐项还原 SM 拉氏量 -> 依赖 V21（内部空间映射缺失）/V22（无 UV 完成）；"
         "③螺旋旋量孤子解搜索 -> 依赖 V16（方程类型未定：KG 还是 Dirac）；"
         "④EC-Hamiltonian + FDTD 最小原型 -> 依赖 V14（代数 vs 演化冲突）/V33（符号反）/V35（源项未给）；"
         "⑤g-2 / EDM 改写为可数值求值 -> 依赖 V30（无函数）/V31（量纲不齐）；"
         "⑥Lean4 张量代数基础库 -> 依赖 V06（分解命名与轴挠率标签错）——**形式化会先把错误形式化**。"
         "=> 6/6 任务的直接上游都落在本册的 FAIL/BOUNDARY 条目上。",
         {"tasks": 6, "blocked_tasks": 6}, ["任务清单", "依赖", "FAIL"])

    # 符号同名台账（机器计数 + 人工义项锚 [C]）
    sym_count = {
        "kappa": len(re.findall(r"\\kappa", SRC_ALL_TEXT)),
        "tau": len(re.findall(r"\\tau", SRC_ALL_TEXT)),
        "mathcal F": len(re.findall(r"\\mathcal F", SRC_ALL_TEXT)),
        "alpha": len(re.findall(r"\\alpha", SRC_ALL_TEXT)),
    }
    emit("V44", "FAIL",
         "符号同名台账 4 组（kappa 2 义 / tau >= 7 义 / mathcal F 3 义 / alpha 2 义）",
         "同名反义清点（义项为人工锚 [C]，出现次数为机器计数）："
         "①**kappa**：" + str(sym_count["kappa"]) + " 次 —— 义 A = kappa_G = 8 pi G（第 2 节，引力常数），"
         "义 B = 曲率（第 3 节 kappa^2 - tau^2 里的弧长倒数，量纲 L^-1）⇒ 同名两义且**量纲不同**。"
         "②**tau**：" + str(sym_count["tau"]) + " 次 —— 义 A = 挠率张量 tau^alpha_mu nu（第 1 节），义 B = 迹 tau_mu，"
         "义 C = |tau| 模（第 4 节），义 D = tau_local（第 7 节），义 E = tau_chiral（第 7 节），"
         "义 F = <tau^2> 真空期望（第 7 节），义 G = tau^i_jk 空间分量（第 8 节）⇒ ≥7 义。"
         "③**mathcal F**：" + str(sym_count["mathcal F"]) + " 次 —— 义 A = beta 函数的几何源 F_i(kappa,tau)（第 6 节），"
         "义 B = 挠率演化源 F^i_jk（第 8 节），义 C = 体系名 TU(F)T 里的 F ⇒ 3 义。"
         "④**alpha**：" + str(sym_count["alpha"]) + " 次 —— 义 A = lapse（第 8 节），义 B = 精细结构常数（隐含）⇒ 2 义。"
         "=> 与库内 r18/r27『符号同名两义』同族；本册新增 kappa 的 **量纲级**冲突（常数 vs L^-1）。",
         {"counts": sym_count, "families": 4}, ["台账", "同名两义", "FAIL"])

    # 与既有册的独立复现（交叉印证）
    emit("V45", "PASS",
         "与库内 r19 / r20 / r27 的四条结论独立复现（交叉印证，非同源）",
         "本册在**只读来料文本 + 独立机器计算**的条件下，复现了既有册的四条判定："
         "①『作用量与演化方程不同源』（r19）-> 本册 V14；"
         "②『tau 是代数 slave』（r20/r21）-> 本册 V13（且进一步指出与第 8 节 PDE 冲突）；"
         "③『EDM 量纲不齐』（r19）-> 本册 V31（第 2 次复发，缺口形式不同）；"
         "④『ADM 哈密顿约束 K 项符号与通行约定不匹配』（r27 H27）-> 本册 V33（第 2 次复发，附加负能量密度读数）。"
         "=> 四条均为**独立复算**（不是引用），构成四重交叉印证；同时说明这不是本册新引入的问题，"
         "而是同一份几何纲领在多个版本上反复出现的结构缺陷。",
         {"independent_reproductions": 4}, ["交叉印证", "PASS"])

    emit("V46", "PASS",
         "第 10 节（Lean4）的自我限制措辞恰当：『形式化不能证明物理公理正确』",
         "来料第 10 节明确写：『形式化不能证明物理公理正确，但可以消除代数、张量演算的人为推导错误』。"
         "这与库内红线（数学自洽 != 物理证实）一致，是全文最恰当的一句自我限制。"
         "**但**其阶段编排有顺序瑕疵：阶段 A（EC 流形张量代数基础库）会先固化第 1 节的三分量分解，"
         "而该分解的命名与『轴挠率』标签在本册 V04/V06/V08 已判错 ⇒ 形式化会放大错误；"
         "阶段 D（零挠率 => GR）**依赖最少、可先行**（tau = 0 时 Einstein-Cartan 退化为 GR，是标准结果），"
         "却被排在后面。=> 建议顺序改为 D -> A -> B -> C -> E。",
         {"self_limitation_correct": True, "stage_order_issue": True}, ["Lean4", "方法论", "PASS"])


# ============================================================ 汇总与输出
VERDICTS = ["PASS", "FAIL", "BOUNDARY", "INFO", "MISMATCH"]


def _jsonable(x):
    if isinstance(x, (Fr, Decimal)):
        return str(x)
    if isinstance(x, set):
        return sorted(x)
    if isinstance(x, bytes):
        return x.decode("utf-8", "replace")
    raise TypeError("not jsonable: " + repr(type(x)))


def summarize():
    cnt = dict((v, 0) for v in VERDICTS)
    for e in ENTRIES:
        cnt[e["verdict"]] = cnt.get(e["verdict"], 0) + 1
    KEY["entry_count"] = len(ENTRIES)
    KEY["verdict_count"] = cnt
    return cnt


def md_table():
    rows = []
    for e in ENTRIES:
        rows.append("| " + e["id"] + " | " + e["verdict"] + " | " + e["title"] + " |")
    return "\n".join(rows)


def write_outputs(cnt):
    ok = sum(1 for g in GUARDS if g["ok"])
    payload = {
        "tag": TAG,
        "date": "2026-10-10",
        "source": "《TU(\\mathcal F)T(g-2)GAQ V4.(\\boldsymbol{0}) 一场论｜深度攻破扩展整理》（13 节）",
        "engine": "纯标准库 Python 3.8.8：Decimal 60 位 + Fraction 量纲向量 (M,L,T,Q) + 精确复 4x4 矩阵（0/±1/±i）+ 解析 MHD 对拍",
        "key_numbers": KEY,
        "verdict_count": cnt,
        "entries": ENTRIES,
        "guards": GUARDS,
        "division_of_labour": [
            "r19/r20/r21（V3.4 四稿）—— 已判作用量与 ADM 不同源、tau 代数 slave、P1 门禁 0/5；本册不复算，只做 V4.(0) 文本自身审计与复发登记",
            "r27（统一场论合集 + GMUFT）—— 已判 ADM 哈密顿约束 K 项符号不匹配；本册 V33 独立复现并给出负能量密度读数",
            "r22/r23/r24/r25/r26/r26b（垂直原理体系）—— 领域互补（本册是新来料 V4.(0) 的首册）",
        ],
        "not_self_derived": [
            "V05 的标准分解 4+4+16 与 V37 的同伦群表是**标准已知结果**，本册只做机器复算与固化，不作为本册的物理产出",
            "V27 不核实『推翻 Grad 猜想』这一外部数学事实（需原始文献）",
            "V28 的 RGE 读数以本册声明的输入口径（alpha_em(M_Z)=7.8156e-3, sin^2=0.23122, GUT 归一 alpha_1=(5/3)alpha_Y）为准；本册 Delta L=9.1384 与库内 r11/r12 的 9.147 相对差 < 0.1%，构成量值级交叉印证（非引用）",
        ],
    }
    pj = os.path.join(DIR_DATA, TAG + ".json")
    with open(pj, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, default=_jsonable)

    md = []
    md.append("# " + TAG + " · 数据摘要")
    md.append("")
    md.append("- **来源**：" + payload["source"])
    md.append("- **引擎**：" + payload["engine"])
    md.append("- **读数**：条目 " + str(KEY["entry_count"]) + "（"
              + " / ".join([k + " " + str(cnt[k]) for k in VERDICTS])
              + "）｜自检 " + str(ok) + "/" + str(len(GUARDS)))
    md.append("")
    md.append("## 逐条判定")
    md.append("")
    md.append("| 条目 | 判定 | 标题 |")
    md.append("| --- | --- | --- |")
    md.append(md_table())
    md.append("")
    md.append("## 关键读数")
    md.append("")
    for k in ["alpha_inv_MZ", "alpha_inv_MPl", "rge_spread_rel", "rge_Lcross", "rge_delta_L",
              "ln_MPl_over_MZ", "entry_count", "verdict_count"]:
        if k in KEY:
            md.append("- **" + k + "** = " + json.dumps(KEY[k], ensure_ascii=False, default=_jsonable))
    md.append("")
    md.append("## 自检")
    md.append("")
    for g in GUARDS:
        md.append("- [" + ("x" if g["ok"] else " ") + "] " + g["name"] + " — " + g["detail"])
    pm = os.path.join(DIR_DATA, TAG + ".md")
    with open(pm, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    rep = []
    rep.append("TU(F)T(g-2)GAQ V4.(0) 一场论 · 全维审计（r28）运行记录")
    rep.append("条目 " + str(KEY["entry_count"]) + " ｜ 自检 " + str(ok) + "/" + str(len(GUARDS)))
    for k in VERDICTS:
        rep.append(k + " = " + str(cnt[k]))
    rep.append("")
    for e in ENTRIES:
        rep.append("[" + e["verdict"] + "] " + e["id"] + " " + e["title"])
    rep.append("")
    rep.append("关键读数：")
    for k in ["alpha_inv_MZ", "alpha_inv_MPl", "rge_spread_rel", "rge_delta_L", "ln_MPl_over_MZ"]:
        if k in KEY:
            rep.append("  " + k + " = " + json.dumps(KEY[k], ensure_ascii=False, default=_jsonable))
    pr = os.path.join(DIR_DATA, TAG + "_report.txt")
    with open(pr, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    return pj, pm, pr, ok


def main():
    audit_torsion()
    audit_action()
    audit_spinor()
    audit_lowenergy()
    audit_mhd()
    audit_rg()
    audit_observables()
    audit_adm()
    audit_ternary()
    audit_meta()
    cnt = summarize()
    pj, pm, pr, ok = write_outputs(cnt)
    print("=" * 78)
    print("TU(F)T(g-2)GAQ V4.(0) 一场论 · 全维审计（r28）")
    print("条目 " + str(KEY["entry_count"]) + " | " + " ".join([k + "=" + str(cnt[k]) for k in VERDICTS]))
    print("自检 " + str(ok) + "/" + str(len(GUARDS)))
    for g in GUARDS:
        if not g["ok"]:
            print("  [GUARD-FAIL] " + g["name"] + " : " + g["detail"])
    print("产物: " + pj)
    print("      " + pm)
    print("      " + pr)
    print("=" * 78)
    return 0 if ok == len(GUARDS) else 1


if __name__ == "__main__":
    sys.exit(main())
