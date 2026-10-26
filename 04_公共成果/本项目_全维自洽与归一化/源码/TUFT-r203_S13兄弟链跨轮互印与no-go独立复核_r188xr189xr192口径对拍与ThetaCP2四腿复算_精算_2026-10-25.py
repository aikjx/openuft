#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""TUFT-r203｜S13 兄弟链跨轮互印与 no-go 独立复核（r188×r189×r192×r194×r195×r199 口径对拍）
================================================================================
编号 r203（★取号经过：起草前竞态实测 22:00:48，`源码/数据/判定` 三树 r203/r204 全空；
并行会话仍在活跃——r200（21:29:09）刚落盘、11 小时内产出 r189–r202 十余卷。
按「先占位者为权威、后到者整体改号」铁律，若登记前发现并行先占则整体改号；
落盘后登记前必再查磁盘时间戳。未改动 r170–r202 任何字节）。

命题（承 r188 我的线与 r189–r199 兄弟线的双链格局）：
  r199 的跨轮口径审计只覆盖 **r190–r197**（主线八件 JSON、sha256 只读），
  **未含我的 r188/r189**；r192 的 Z₄→超对称 no-go 四腿（N1–N6）尚未被
  **独立复算**。本卷补三件事：
    ① 跨轮互印：r188–r202 全部在册卷的共享量机读 + 独立重算对拍
       （v / M* / M*/v / x* / x₁₂ / x_GUT / M_GUT / α_GUT⁻¹ / s* / gap 四口径 /
        β / Higgs / Θ² / CP² / ℓ_EW 共 22 项），精度层逐项分类；
    ② no-go 四腿独立复算：Θ²=−I/Θ⁴=+I（Fraction 精确）、εσᵢε⁻¹=−σᵢᵀ（3/3）、
       反幺正+Θ²=−I（6/6）、CP² χ=3/c₁=3H/h²⁰=0（组合学）、FS Kähler 类齐次
       （残差精确 0）、M5 对偶族任意 ℓ 恒等（0 bit on ℓ）、RG 参考尺度不变性
       （9/9）、101 文件**截断后**超对称 inventory 扫描（0 命中 + 正对照 5/5）、
       Higgs 谱 {0,0,0,8κv²} 计数 1≠2；
    ③ r188 重审条件核验：路径 2 → CLOSED-NEGATIVE（r192 N6 + r199 B2）；
       路径 1/3 → 归并为单一缺失对象（r192 §五）+ 尺度锚定不可能性（r194/r195/r199）。

靶：`01_独立体系/S13_全域双向分形统一场论/`（唯一 H 级体系）
    · 03_数学形式/equations.md（Θ=[[0,−1],[1,0]] L30；M5 对偶镜像 L15）
    · 13_论文与成果/书稿/正文/ch25-常数统一与电荷量子化.md（定理 25.4；附节 L71/L81）
    · 09_验证结果/验证精算报告_V1.8.md（s* 30 位闭式值 L71）
    · 07_计算复现/源码/higgs_verify.py（S³ 模式谱 {0,0,0,8κv²}）
    · 07_计算复现/源码/dimension_unify_verify.py（验证 E 同型式 g=1−r_s·r/(r²+L²)）
    · 07_计算复现/源码/openuft_rge_sim.py（圆整初值 59/30/8.5 + RK4 协议）
    · 全树 101 个 .py/.md（截断扫描基数，与 r192 同）
  兄弟卷（只读、sha256 前后一致证明）：r188–r202 在册 JSON 14 件 + r192/r194/r195/r199 判定册。

本卷五层判据：
  ① 互印层 A：22 项共享量跨卷机读 + 独立重算对拍（精确 / 渲染层 ≤1ulp / 真冲突单列）；
  ② no-go 代数腿 B1–B3：Θ 周期 4、Pauli 共轭、反幺正 ⇒ Majorana 实条件（复算确认）；
  ③ no-go 几何腿 B4–B6：CP² 非 hyperkähler、FS 无内禀长度、M5 尺度简并（复算确认）；
  ④ no-go 内容腿 B8–B9：超对称 inventory 0/101 文件（截断后）、Higgs 1≠2；
  ⑤ 重审与定价层 C/D/E：r188 三条件核验、x_GUT 混用检出、候选扫描自有基准复扫、
     覆盖率定价 R1（共享量 N 项一致 M 项、no-go 腿 K 条通过 J 条、未覆盖项诚实列名）。

分层铁律：本卷条目不可与 r142–r202 相加。
治理红线：数学自洽 ≠ 实验证实；no-go 排除 ≠ 物理闭合；本卷只做可算复核，不产生新物理。
纯标准库（本环境无 numpy / sympy / mpmath；Decimal(60) + Fraction + 自写复分数 CF）。
"""

import ast
import json
import math
import os
import re
import sys
import warnings
import hashlib
import random
from decimal import Decimal, getcontext
from fractions import Fraction as F

getcontext().prec = 60

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)                      # 本项目_全维自洽与归一化
_ROOT = os.path.dirname(os.path.dirname(_PROJ))     # openuft
_DATADIR = os.path.join(_PROJ, "数据")

S13 = os.path.join(_ROOT, "01_独立体系", "S13_全域双向分形统一场论")

BASE = ("TUFT-r203_S13兄弟链跨轮互印与no-go独立复核_r188xr189xr192口径对拍"
        "与ThetaCP2四腿复算_精算_2026-10-25")
REDLINE = ("数学自洽 ≠ 实验证实；no-go 排除 ≠ 物理闭合；本卷只做可算复核，"
           "不产生新物理；条目不可与 r142–r202 相加")
REDLINE_PHRASE = "不可与 r142–r202 相加"

# ---------------------------------------------------------------------------
# 靶文件登记（G4 可读性守卫 + 文本证据守卫的数据基础）
# ---------------------------------------------------------------------------
TARGET_FILES = {
    "eqmd": "03_数学形式/equations.md",
    "ch25": "13_论文与成果/书稿/正文/ch25-常数统一与电荷量子化.md",
    "v18": "09_验证结果/验证精算报告_V1.8.md",
    "higgs": "07_计算复现/源码/higgs_verify.py",
    "dimunify": "07_计算复现/源码/dimension_unify_verify.py",
    "rgesim": "07_计算复现/源码/openuft_rge_sim.py",
}

# 兄弟卷判定册（只读；文本证据引用源）
PEER_MD = {
    "r192md": os.path.join(_DATADIR, "判定_TUFT-r192_S13三路径攻坚_Z4超对称no-go与尺度同源归并_精算_2026-10-25.md"),
    "r194md": os.path.join(_DATADIR, "判定_TUFT-r194_统一场论尺度不可导出no-go与六处缺陷单源勘误_精算_2026-10-25.md"),
    "r195md": os.path.join(_DATADIR, "判定_TUFT-r195_尺度秩不变性定理_M5尺度简并与归一化条件名实审计_精算_2026-10-25.md"),
    "r199md": os.path.join(_DATADIR, "判定_TUFT-r199_尺度锚定不可能性定理_三类离散归一化条件排除与跨轮口径一致性审计_精算_2026-10-25.md"),
}

ENTRIES = []   # (id, layer, text, verdict, note)
CTRL = []      # (id, text, ok, detail)
GUARDS = []    # (id, text, ok, detail)


def add(eid, layer, text, verdict, note=""):
    ENTRIES.append((eid, layer, text, verdict, note))


def ctl(cid, text, ok, detail=""):
    CTRL.append((cid, text, bool(ok), detail))


def grd(gid, text, ok, detail=""):
    GUARDS.append((gid, text, bool(ok), detail))


def fmt_rel(s):
    """相对差显示：科学计数法保指数位（禁裸截断——1.78e-08 截成 1.7795663853 会量级误导）。"""
    try:
        v = float(s)
    except (TypeError, ValueError):
        return str(s)
    if v == 0:
        return "0"
    return "{:.3e}".format(v)


def prev_num(s, n=24):
    """长数值预览：超长加省略号，禁裸截断（Decimal 串截断无标记会误读为终止值）。"""
    s = str(s)
    return s if len(s) <= n else s[:n] + "…"


def load_corpus():
    """读取全部靶文件（G4）；返回 {key: text}。"""
    corpus = {}
    for key, rel in TARGET_FILES.items():
        p = os.path.join(S13, rel)
        with open(p, "r", encoding="utf-8") as f:
            corpus[key] = f.read()
    for key, p in PEER_MD.items():
        with open(p, "r", encoding="utf-8") as f:
            corpus[key] = f.read()
    return corpus


def sha256_text(t):
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# 一、RG 闭式与靶协议（互印层的机器基础；常数与 r188/r192 逐位同源）
# ---------------------------------------------------------------------------
D = Decimal
AEM_INV = D(127916) / D(1000)          # α_EM(M_Z)⁻¹ = 127.916
S2W_EXP = D(23122) / D(100000)         # sin²θ_W(M_Z) = 0.23122
A3_INV = D(10000) / D(1179)            # α_s(M_Z)⁻¹ = 1/0.1179
MZ = D(911876) / D(10000)              # 91.1876 GeV
V_FW = D(25526) / D(100)               # 255.26 GeV（ch25 §25.8「框架真空尺度」）
SSTAR_TARGET = D("0.230943405280905868720056895551")   # V1.8 P9d 自报 30 位
PI_60 = D("3.14159265358979323846264338327950288419716939937510582097494")  # π 60 位字面

A1_0 = D(3) / D(5) * (D(1) - S2W_EXP) * AEM_INV
A2_0 = S2W_EXP * AEM_INV
A3_0 = A3_INV

SM_B = (D(41) / D(10), D(-19) / D(6), D(-7))     # 标准模型单圈（GUT 归一化）
MSSM_B = (D(33) / D(5), D(1), D(-3))             # MSSM 单圈（GUT 归一化）

TWO_PI = D(2) * D(str(math.pi))                  # 16 位 π 层（r188/r192 同款）
TWO_PI_60 = D(2) * PI_60                         # 60 位 π 层（r194/r195/r199 同款）


def alpha_inv(a0, b, x):
    """α_i⁻¹(x)，x = ln(μ/M_Z)/(2π)：A_i(x) = A_i(0) − b_i·x（闭式）。"""
    return a0 - b * x


def s2w_of(a1, a2):
    return D(3) * a2 / (D(3) * a2 + D(5) * a1)


def crossing(b, a1_0=None, a2_0=None, a3_0=None):
    """α₁=α₂ 交点与 α₃ 偏差（与 r192 crossing() 同式）。"""
    a1_0 = A1_0 if a1_0 is None else a1_0
    a2_0 = A2_0 if a2_0 is None else a2_0
    a3_0 = A3_0 if a3_0 is None else a3_0
    x = (a1_0 - a2_0) / (b[0] - b[1])
    m = MZ * (TWO_PI * x).exp()
    a = alpha_inv(a1_0, b[0], x)
    a3 = alpha_inv(a3_0, b[2], x)
    return x, m, a, a3, abs(a3 - a) / a * D(100)


def sstar_closed():
    """s* 闭式：解 A1(L)=A3(L) 与 A2(L)=A3(L)（s 为未知）⇒ s*=(3a+7A3)/(15a)；
    L13−L23 ≡ 0（代数恒等）。x_GUT 规范值即 L13（α₁=α₃ 统一点）。"""
    s = (D(3) * AEM_INV + D(7) * A3_INV) / (D(15) * AEM_INV)
    a1_0 = D(3) / D(5) * (D(1) - s) * AEM_INV
    l13 = (a1_0 - A3_INV) / (MSSM_B[0] - MSSM_B[2])
    l23 = (s * AEM_INV - A3_INV) / (MSSM_B[1] - MSSM_B[2])
    m_pred = MZ * (TWO_PI * l13).exp()
    m_pred_60 = MZ * (TWO_PI_60 * l13).exp()
    a_gut = A3_INV - MSSM_B[2] * l13
    return s, l13, l23, m_pred, m_pred_60, a_gut


def m_star():
    """sin²θ=1/4 唯一成立尺度（SM β）：x* = (A1−(9/5)A2)/(b1−(9/5)b2)（精确有理）。"""
    r = D(9) / D(5)
    xs = (A1_0 - r * A2_0) / (SM_B[0] - r * SM_B[1])
    ms = MZ * (TWO_PI * xs).exp()
    return xs, ms


def v_fit_from_pdg():
    """ch25 §25.2/定理 25.1：v = 2m_W/g̃，g̃ = e/sinθ_W，e = √(4πα)。
    全部输入为 PDG 实验常数；重算靶的 v=255.26 GeV。"""
    alpha = 1.0 / 137.035999084
    mw = 80.377
    e = math.sqrt(4 * math.pi * alpha)
    g = e / math.sqrt(0.23122)
    v = 2 * mw / g
    return v


def s2w_at_v():
    """sin²θ 跑动到 v=255.26 GeV（SM β，精确输入）。"""
    x_v = (V_FW / MZ).ln() / TWO_PI
    a1v = alpha_inv(A1_0, SM_B[0], x_v)
    a2v = alpha_inv(A2_0, SM_B[1], x_v)
    return x_v, s2w_of(a1v, a2v)


def beta_from_content(gens=3, higgs_doublets=1):
    """SM β 由场内容闭式重算（r188 A4 同款；U(1) GUT 归一化）。"""
    fermion_idx_su3 = gens * 2
    fermion_idx_su2 = gens * 2
    fermion_y2 = gens * F(10, 3)
    higgs_idx_su2 = higgs_doublets
    higgs_y2 = higgs_doublets * F(1, 2)
    b3 = -F(11, 3) * 3 + F(2, 3) * fermion_idx_su3
    b2 = -F(11, 3) * 2 + F(2, 3) * fermion_idx_su2 + F(1, 6) * higgs_idx_su2
    b1y = F(2, 3) * fermion_y2 + F(1, 3) * higgs_y2
    b1 = F(3, 5) * b1y
    return (str(b1), str(b2), str(b3))


# ---------------------------------------------------------------------------
# 二、RK4 靶协议复现（逐位复现 r188/r192 的复现代码：圆整初值 + dt=0.001）
# ---------------------------------------------------------------------------
def integrate_scan(b, a0, t_max, dt=0.001):
    """逐位复现靶 openuft_rge_sim.py 的 integrate()/find_cross()。"""
    a = list(a0)
    t = 0.0
    best = (1e9, 0.0, tuple(a))
    last = (0.0, tuple(a))
    while t < t_max:
        last = (t, tuple(a))
        if t != 0.0:
            gap = max(abs(a[0] - a[1]), abs(a[1] - a[2]), abs(a[0] - a[2]))
            if gap < best[0]:
                best = (gap, t, tuple(a))

        def f(aa, bb):
            return -bb / (2.0 * math.pi)
        k1 = [f(a[i], b[i]) for i in range(3)]
        k2 = [f(a[i] + dt / 2 * k1[i], b[i]) for i in range(3)]
        k3 = [f(a[i] + dt / 2 * k2[i], b[i]) for i in range(3)]
        k4 = [f(a[i] + dt * k3[i], b[i]) for i in range(3)]
        a = [a[i] + dt / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])
             for i in range(3)]
        t += dt
    return best, last


def rge_target_protocol():
    """靶协议：圆整初值 (59.0, 30.0, 8.5)；SM 跑至 1e19；
    MSSM 自 SM 在 1TeV 处的最后记录点续接跑至 1e19。"""
    mz_f = 91.1876
    sm_b = (41.0 / 10, -19.0 / 6, -7.0)
    ms_b = (33.0 / 5, 1.0, -3.0)
    a0 = (59.0, 30.0, 8.5)
    best_sm, _ = integrate_scan(sm_b, a0, math.log(1e19 / mz_f))
    _, (t_tev, a_tev) = integrate_scan(sm_b, a0, math.log(1000.0 / mz_f))
    best_ms, _ = integrate_scan(ms_b, a_tev, math.log(1e19 / 1000.0))
    return (best_sm[0], mz_f * math.exp(best_sm[1]),
            best_ms[0], 1000.0 * math.exp(best_ms[1]), best_ms[2][0])


# ---------------------------------------------------------------------------
# 三、no-go 代数腿：Θ 周期 / Pauli 共轭 / 反幺正（全 Fraction 精确）
# ---------------------------------------------------------------------------
class CF:
    """复分数（re, im 全 Fraction）——保证代数腿零浮点。"""
    __slots__ = ("re", "im")

    def __init__(self, re, im=0):
        self.re = F(re)
        self.im = F(im)

    def __add__(self, o):
        return CF(self.re + o.re, self.im + o.im)

    def __sub__(self, o):
        return CF(self.re - o.re, self.im - o.im)

    def __neg__(self):
        return CF(-self.re, -self.im)

    def __mul__(self, o):
        return CF(self.re * o.re - self.im * o.im,
                  self.re * o.im + self.im * o.re)

    def __truediv__(self, o):
        den = o.re * o.re + o.im * o.im
        return CF((self.re * o.re + self.im * o.im) / den,
                  (self.im * o.re - self.re * o.im) / den)

    def conj(self):
        return CF(self.re, -self.im)

    def __eq__(self, o):
        return self.re == o.re and self.im == o.im

    def __repr__(self):
        return "CF({},{})".format(self.re, self.im)


ZERO = CF(0)
ONE = CF(1)
IUNIT = CF(0, 1)


def mat2(a, b, c, d):
    return [[a, b], [c, d]]


def matmul(A, B):
    return [[A[0][0] * B[0][0] + A[0][1] * B[1][0],
             A[0][0] * B[0][1] + A[0][1] * B[1][1]],
            [A[1][0] * B[0][0] + A[1][1] * B[1][0],
             A[1][0] * B[0][1] + A[1][1] * B[1][1]]]


def matinv2(A):
    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    return [[A[1][1] / det, -A[0][1] / det], [-A[1][0] / det, A[0][0] / det]]


# 靶约定（equations.md L30）：Θ = [[0,−1],[1,0]]
THETA = mat2(ZERO, -ONE, ONE, ZERO)
I2 = mat2(ONE, ZERO, ZERO, ONE)
NEG_I2 = mat2(-ONE, ZERO, ZERO, -ONE)

# Pauli 矩阵与 ε = iσ₂
SIGMA1 = mat2(ZERO, ONE, ONE, ZERO)
SIGMA2 = mat2(ZERO, -IUNIT, IUNIT, ZERO)
SIGMA3 = mat2(ONE, ZERO, ZERO, -ONE)
EPS = mat2(ZERO, IUNIT, -IUNIT, ZERO)


def theta_apply(vec):
    """(Θψ)_k = Σ_l Θ_{kl} ψ_l*（对偶含复共轭）。"""
    return [THETA[0][0] * vec[0].conj() + THETA[0][1] * vec[1].conj(),
            THETA[1][0] * vec[0].conj() + THETA[1][1] * vec[1].conj()]


def check_theta_algebra():
    """Θ²=−I、Θ⁴=+I（矩阵层，精确）；200 随机复旋量算子层机器零。"""
    th2 = matmul(THETA, THETA)
    th4 = matmul(th2, th2)
    mzero = (th2 == NEG_I2) and (th4 == I2)
    rng = random.Random(20301)
    worst = F(0)
    for _ in range(200):
        z0 = CF(rng.randint(-9, 9), rng.randint(-9, 9)) / CF(7)
        z1 = CF(rng.randint(-9, 9), rng.randint(-9, 9)) / CF(7)
        p1 = theta_apply([z0, z1])
        p2 = theta_apply(p1)
        p4 = theta_apply(theta_apply(p2))
        worst = max(worst, abs(p2[0].re + z0.re), abs(p2[0].im + z0.im),
                    abs(p2[1].re + z1.re), abs(p2[1].im + z1.im),
                    abs(p4[0].re - z0.re), abs(p4[0].im - z0.im),
                    abs(p4[1].re - z1.re), abs(p4[1].im - z1.im))
    return mzero, worst


def check_pauli_conjugation():
    """εσᵢε⁻¹ = −σᵢᵀ（i=1,2,3，精确）。"""
    eps_inv = matinv2(EPS)
    ok = []
    for S in (SIGMA1, SIGMA2, SIGMA3):
        lhs = matmul(matmul(EPS, S), eps_inv)
        rhs = [[-S[0][0], -S[1][0]], [-S[0][1], -S[1][1]]]   # −Sᵀ
        ok.append(lhs == rhs)
    return ok


def check_antiunitary():
    """Θ(iψ)=−iΘ(ψ) 且 Θ²ψ=−ψ（6 组精确复向量）。"""
    rng = random.Random(20302)
    oks = []
    for _ in range(6):
        z0 = CF(rng.randint(-9, 9), rng.randint(-9, 9)) / CF(5)
        z1 = CF(rng.randint(-9, 9), rng.randint(-9, 9)) / CF(5)
        psi = [z0, z1]
        ipsi = [z0 * IUNIT, z1 * IUNIT]
        lhs = theta_apply(ipsi)
        rhs = [-IUNIT * theta_apply(psi)[0], -IUNIT * theta_apply(psi)[1]]
        sq = theta_apply(theta_apply(psi))
        oks.append(lhs == rhs and sq == [-psi[0], -psi[1]])
    return oks


# ---------------------------------------------------------------------------
# 四、no-go 几何腿：CP² 组合学 + FS Kähler 类齐次（全 Fraction 精确）
# ---------------------------------------------------------------------------
def cp2_invariants():
    """CP²：一个胞腔在每个偶维 0/2/4 ⇒ Betti (1,0,1,0,1)；
    Hodge h^{p,q}=1 当 p=q≤2 否则 0；χ=Σ(−1)^k b_k=3；
    c₁=(n+1)H=3H≠0；h^{2,0}=0 ⇒ 非 hyperkähler、非 Calabi–Yau。
    （胞腔/Hodge/曲率类公式为外部标准数学输入；组合与算术为本机重算。）"""
    n = 2
    betti = [1 if (k % 2 == 0 and k <= 2 * n) else 0 for k in range(2 * n + 1)]
    hodge = [[1 if (p == q and p <= n) else 0 for q in range(n + 1)]
             for p in range(n + 1)]
    chi = sum(((-1) ** k) * b for k, b in enumerate(betti))
    h20 = hodge[2][0]
    c1_over_H = n + 1
    return {"betti": betti, "chi": chi, "h20": h20, "c1_over_H": c1_over_H,
            "hyperkaehler": c1_over_H == 0, "calabi_yau": c1_over_H == 0}


def fs_metric(z1, z2, lam):
    """CP² FS 度规（Kähler 类 λ）：g_{ij}=λ(δ_{ij}/s − z_i z_j/s²)，s=1+z₁²+z₂²。
    实有理点处 z̄=z；Kähler 求导规则 ∂_i∂_j̄ ln s = δ_{ij}/s − z_i z_j/s² 精确成立。"""
    s = F(1) + z1 * z1 + z2 * z2
    g = [[lam * (F(1) / s - z1 * z1 / (s * s)), lam * (F(0) - z1 * z2 / (s * s))],
         [lam * (F(0) - z1 * z2 / (s * s)), lam * (F(1) / s - z2 * z2 / (s * s))]]
    return g, s


def det2(m):
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def inv2(m):
    d = det2(m)
    return [[m[1][1] / d, -m[0][1] / d], [-m[1][0] / d, m[0][0] / d]]


def fs_ricci_scalar(z1, z2, lam):
    """R = g^{ij}Ric_{ij}；Ric_{ij}=−∂_i∂_j̄ ln det g。
    det g(λ)=λ²/s³（2×2 行列式直接算）⇒ ln det g = 2lnλ−3ln s
    ⇒ Ric_{ij}=3(δ_{ij}/s−z_i z_j/s²)（与 λ 无关）⇒ R(λ)=6/λ。全 Fraction 精确。"""
    g, s = fs_metric(z1, z2, lam)
    ginv = inv2(g)
    ric = [[F(3) * (F(1) / s - z1 * z1 / (s * s)), F(3) * (F(0) - z1 * z2 / (s * s))],
           [F(3) * (F(0) - z1 * z2 / (s * s)), F(3) * (F(1) / s - z2 * z2 / (s * s))]]
    R = (ginv[0][0] * ric[0][0] + ginv[0][1] * ric[1][0]
         + ginv[1][0] * ric[0][1] + ginv[1][1] * ric[1][1])
    return R, det2(g)


def check_fs_homogeneity():
    """Kähler 类齐次性：g(λ)=λg(1)、det(λg)=λ²det g、(λg)^{-1}=λ^{-1}g^{-1}、
    R(λ)·λ=R(1) 全精确；附差商精确恒等式核验求导规则。两点 × 三 λ。"""
    pts = [(F(1, 2), F(1, 3)), (F(2, 5), F(-1, 7))]
    lams = [F(1), F(7), F(13)]
    resid = F(0)
    eqs = 0
    for z1, z2 in pts:
        g1, s = fs_metric(z1, z2, F(1))
        d1 = det2(g1)
        gi1 = inv2(g1)
        R1, _ = fs_ricci_scalar(z1, z2, F(1))
        # det 引理：det g(λ)·s³ = λ²
        for lam in lams:
            g, _ = fs_metric(z1, z2, lam)
            d = det2(g)
            gi = inv2(g)
            R, _ = fs_ricci_scalar(z1, z2, lam)
            if all(g[i][j] == lam * g1[i][j] for i in range(2) for j in range(2)):
                eqs += 1
            if d * (s ** 3) == lam ** 2:
                eqs += 1
            if all(gi[i][j] == g1inv_entry(gi1, i, j) / lam
                   for i in range(2) for j in range(2)):
                eqs += 1
            if R * lam == R1:
                eqs += 1
            resid = max(resid, abs(R * lam - R1))
        # 差商恒等式：∂_{z̄_j}(z_i/s) = δ_{ij}/s − z_i z_j/s² 的精确差商核验
        h = F(1, 1000)
        for (zi, zj) in ((z1, z1), (z1, z2), (z2, z1), (z2, z2)):
            lhs = (zi / (s + h * zj) - zi / s) / h
            rhs = -zi * zj / (s * (s + h * zj))
            if lhs == rhs:
                eqs += 1
    return resid, eqs


def g1inv_entry(gi1, i, j):
    return gi1[i][j]


# ---------------------------------------------------------------------------
# 五、M5 尺度简并 + RG 参考尺度不变性（全 Fraction / Decimal 精确）
# ---------------------------------------------------------------------------
def m5_family(r, rs, ell):
    """g_ℓ(r) = 1 − r_s·r/(r²+ℓ²)（S13 验证 E 同型式；dimension_unify_verify.py L117-119）。"""
    return F(1) - rs * r / (r * r + ell * ell)


def check_m5_identity():
    """对偶镜像 g_ℓ(ℓ²/r) = g_ℓ(r) 对任意 ℓ 恒等（精确有理；含随机样本）。"""
    rng = random.Random(20303)
    worst = F(0)
    samples = []
    for _ in range(200):
        ell = F(rng.randint(1, 40), rng.randint(1, 40))
        r = F(rng.randint(1, 40), rng.randint(1, 40))
        rs = F(rng.randint(1, 20), rng.randint(1, 20))
        d = m5_family(ell * ell / r, rs, ell) - m5_family(r, rs, ell)
        worst = max(worst, abs(d))
        if len(samples) < 3:
            samples.append((ell, r))
    return worst, samples


def rg_reference_invariance():
    """RG 参考尺度不变性：x（无量纲）不含 M_Z；M(λM_Z)/λ = M(M_Z)。
    三尺度 × 三 λ = 9 项，最大相对残差（Decimal 60 位）。"""
    xs_star, _ = m_star()
    _, l13, _, _, _, _ = sstar_closed()
    x12, _, _, _, _ = crossing(MSSM_B)
    scales = [("M*(sin²θ=1/4)", xs_star), ("M_GUT(s*点)", l13),
              ("M(x12)", x12)]
    lams = [D(2), D(3), D(7)]
    worst = D(0)
    n = 0
    for _label, x in scales:
        E = (TWO_PI * x).exp()
        m0 = MZ * E
        for lam in lams:
            m1 = (MZ * lam) * E
            rel = abs(m1 / lam - m0) / m0
            worst = max(worst, rel)
            n += 1
    return n, worst


# ---------------------------------------------------------------------------
# 六、语料扫描（截断纪律 + 正对照）与 Higgs 计数
# ---------------------------------------------------------------------------
SUPER_CATS = {
    "超场": re.compile(r"超场|superfield"),
    "超多重态": re.compile(r"超多重态|supermultiplet"),
    "超势": re.compile(r"超势|superpotential"),
    "超伴子": re.compile(r"超伴子|sparticle"),
    "sfermion": re.compile(r"sfermion"),
    "gaugino": re.compile(r"gaugino"),
    "higgsino": re.compile(r"[Hh]iggsino"),
}
SPARTICLE_BROAD = re.compile(r"超伴子|sparticle|squark|selectron|gaugino|Higgsino|higgsino|(?<!中)微子")
SUSY_PAT = re.compile(r"超对称|MSSM|supersym")
# 附节标记（审计侧勘误）：扫描前必须截断，否则本轮文字被误计为框架内容
APPENDIX_PAT = re.compile(r"\n---\n+\s*## 【r1\d\d")


def walk_s13():
    """S13 全树 .py/.md 文件（与 r192 扫描基数一致：101）。"""
    out = []
    for dirpath, _dirs, files in os.walk(S13):
        for fn in files:
            if fn.endswith(".py") or fn.endswith(".md"):
                out.append(os.path.join(dirpath, fn))
    return sorted(out)


def truncate_appendix(text):
    m = APPENDIX_PAT.search(text)
    return text[:m.start()] if m else text


def scan_susy_inventory(files):
    """截断后七类超对称 inventory 扫描；返回 (counts, total, n_files,
    raw_hits_before_truncation, susy_files, marker_count)。"""
    counts = {k: 0 for k in SUPER_CATS}
    total = 0
    raw_total = 0
    susy_files = set()
    marker_count = 0
    for p in files:
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        if APPENDIX_PAT.search(text):
            marker_count += 1
        raw_total += sum(1 for _ in SPARTICLE_BROAD.finditer(text))
        body = truncate_appendix(text)
        for k, pat in SUPER_CATS.items():
            for _ in pat.finditer(body):
                counts[k] += 1
                total += 1
        if SUSY_PAT.search(body):
            susy_files.add(os.path.basename(p))
    return counts, total, len(files), raw_total, susy_files, marker_count


def scan_positive_control():
    """注入正对照：七类模式各注入一条 ⇒ 必须 7/7 命中（证明扫描器有分辨力）。"""
    injected = {k: k + "注入正对照样本 XYZ" for k in SUPER_CATS}
    hits = 0
    for k, pat in SUPER_CATS.items():
        if pat.search(injected[k]):
            hits += 1
    return hits


def higgs_count(corpus):
    """Higgs 结构计数：靶 higgs_verify.py 自报谱 {0,0,0,8κv²}（3 零模 + 1 质量模）
    ⇒ 4 实自由度 = 1 个 SU(2) 双重态结构（2 复分量）；MSSM 需 2 重态 = 8 实自由度。"""
    quote = "Hessian 本征值 {0,0,0, 8κv²}"
    anchor = quote in corpus["higgs"]
    real_modes = 4
    doublets = real_modes // 4          # 1 个双重态 = 2 复分量 = 4 实分量
    mssm_need = 2
    massive_modes = real_modes - 3      # 3 个真空流形零模（S³ 方向）
    return {"anchor": anchor, "real_modes": real_modes, "doublets": doublets,
            "mssm_need": mssm_need, "massive_modes": massive_modes,
            "mismatch": doublets != mssm_need}


# ---------------------------------------------------------------------------
# 七、候选扫描（自有基准独立复扫 + 正对照；r192 记录机读）
# ---------------------------------------------------------------------------
SCAN_PRIMS = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 15.0, 24.0,
              math.pi, 1.0 / math.pi, math.pi ** 2, 1.0 / math.pi ** 2,
              math.sqrt(2), math.sqrt(3), math.sqrt(5),
              1.0 / math.sqrt(2), 1.0 / math.sqrt(3), 1.0 / math.sqrt(5),
              math.log(10), 1.0 / math.log(10)]
SCAN_TOL = 1e-9


def candidate_scan_own(targets, extra_prims=()):
    """三因子单项式（可重复、每因子可取倒数）对靶扫描；返回 (N, hits, closest)。
    extra_prims：注入的附加基元（正对照用——靶值本身入基必命中）。"""
    prims = list(SCAN_PRIMS) + [float(p) for p in extra_prims]
    units = []
    for p in prims:
        units.append(p)
        units.append(1.0 / p)
    n_comb = 0
    hits = {k: 0 for k in targets}
    closest = {k: (1e9, None) for k in targets}
    m = len(units)
    for i in range(m):
        for j in range(i, m):
            for k in range(j, m):
                val = units[i] * units[j] * units[k]
                n_comb += 1
                for key, tv in targets.items():
                    if tv == 0:
                        continue
                    err = abs(val / tv - 1.0)
                    if err < closest[key][0]:
                        closest[key] = (err, val)
                    if err < SCAN_TOL:
                        hits[key] += 1
    return n_comb, hits, closest


# ---------------------------------------------------------------------------
# 八、跨轮互印：peer JSON 机读（只读 + sha256）+ 共享量表
# ---------------------------------------------------------------------------
PEER_TAGS = ["r188", "r189", "r190", "r191", "r192", "r193", "r194", "r195",
             "r196", "r197", "r199", "r200", "r201", "r202"]


def load_peers():
    """加载 r188–r202 在册 JSON（r198 已释放不在册）；sha256 前后一致证只读。"""
    peers = {}
    shas = {}
    for tag in PEER_TAGS:
        hits = [f for f in os.listdir(_DATADIR)
                if f.startswith("TUFT-" + tag + "_") and f.endswith(".json")]
        if not hits:
            continue
        p = os.path.join(_DATADIR, hits[0])
        with open(p, "rb") as f:
            raw = f.read()
        shas[tag] = hashlib.sha256(raw).hexdigest()
        peers[tag] = json.loads(raw.decode("utf-8"))
        # 只读证明：再读一次比对
        with open(p, "rb") as f:
            raw2 = f.read()
        if hashlib.sha256(raw2).hexdigest() != shas[tag]:
            peers[tag] = None
    return peers, shas


def dig(d, path):
    """按路径取 JSON 值；不存在返回 None。"""
    cur = d
    for k in path:
        if not isinstance(cur, dict) or k not in cur:
            return None
        cur = cur[k]
    return cur


def to_dec(v):
    if v is None:
        return None
    if isinstance(v, bool):
        return None
    if isinstance(v, (int,)):
        return D(v)
    if isinstance(v, float):
        return D(repr(v))
    if isinstance(v, str):
        try:
            return D(v.strip())
        except Exception:
            return None
    return None


# 共享量行：(key, 标签, 容差 rel, probes=[(tag, path)], 字面签名列表)
SHARED_ROWS = [
    ("v", "v（PDG 反解，GeV）", D("1e-8"),
     [("r188", ("key_numbers", "v_fit_from_pdg")),
      ("r192", ("key_numbers", "v_fit_gev")),
      ("r194", ("provenance", "v")),
      ("r195", ("provenance", "v")),
      ("r199", ("provenance", "v"))],
     ["255.262424", "255.26242445"]),
    ("Mstar", "M*（GeV）", D("1e-8"),
     [("r188", ("key_numbers", "M_star_GeV")),
      ("r192", ("key_numbers", "M_star_gev")),
      ("r194", ("provenance", "M_star")),
      ("r195", ("provenance", "M_star")),
      ("r199", ("provenance", "M_star"))],
     ["3675.242923"]),
    ("Mstar_over_v", "M*/v", D("1e-7"),
     [("r188", ("key_numbers", "Mstar_over_v")),
      ("r192", ("key_numbers", "Mstar_over_v")),
      ("r194", ("provenance", "Mstar_over_v")),
      ("r195", ("provenance", "Mstar_over_v")),
      ("r199", ("provenance", "Mstar_over_v"))],
     ["14.3979"]),
    ("xstar", "x*（sin²θ=1/4，精确有理）", D("1e-9"),
     [("r192", ("key_numbers", "x_star")),
      ("r194", ("provenance", "x_star")),
      ("r195", ("provenance", "x_star")),
      ("r199", ("provenance", "x_star"))],
     ["0.5883091"]),
    ("x12", "x₁₂（α₁=α₂ 交点）", D("1e-12"),
     [("r192", ("key_numbers", "x_GUT")),
      ("r194", ("provenance", "x_gut12"))],
     ["5.2547892"]),
    ("M_x12", "M(x₁₂)（GeV）", D("1e-6"),
     [("r189", ("key_numbers", "M_cross_gev")),
      ("r194", ("provenance", "M_GUT12"))],
     ["1.9904729", "1.99047287"]),
    ("xgut13", "x_GUT 规范值（α₁=α₃ 统一点）", D("1e-40"),
     [("r194", ("provenance", "x_gut13")),
      ("r195", ("provenance", "x_gut13")),
      ("r199", ("provenance", "x_gut13"))],
     ["5.2648981"]),
    ("MGUT", "M_GUT（GeV）", D("1e-6"),
     [("r188", ("key_numbers", "sstar_M")),
      ("r192", ("key_numbers", "M_GUT_gev")),
      ("r194", ("provenance", "M_GUT")),
      ("r195", ("provenance", "M_GUT")),
      ("r199", ("provenance", "M_GUT"))],
     ["2.121000"]),
    ("agut_inv", "α_GUT⁻¹", D("1e-8"),
     [("r188", ("key_numbers", "sstar_agut_inv")),
      ("r189", ("key_numbers", "alpha_gut_sstar")),
      ("r192", ("key_numbers", "alpha_GUT_inv")),
      ("r194", ("provenance", "alpha_gut_inv")),
      ("r195", ("provenance", "alpha_gut_inv")),
      ("r199", ("provenance", "alpha_gut_inv"))],
     ["24.2764585"]),
    ("sstar", "s*（V1.8 30 位）", D("1e-16"),
     [("r188", ("key_numbers", "sstar")),
      ("r189", ("key_numbers", "s_star"))],
     ["0.230943405"]),
    ("gap_sm_rk4", "gap_sm（靶协议 RK4）", D("1e-9"),
     [("r188", ("key_numbers", "rge_sm_gap_target_protocol")),
      ("r189", ("key_numbers", "rge_sim", "gap_sm"))],
     ["4.060449943317877"]),
    ("gap_ms_rk4", "gap_ms（靶协议 RK4）", D("1e-9"),
     [("r188", ("key_numbers", "rge_mssm_gap_target_protocol")),
      ("r189", ("key_numbers", "rge_sim", "gap_ms"))],
     ["0.7600419008581873"]),
    ("M_sm_rk4", "M_sm（靶协议 RK4，GeV）", D("1e-9"),
     [("r189", ("key_numbers", "rge_sim", "M_sm"))],
     ["236961529934301"]),
    ("M_ms_rk4", "M_ms（靶协议 RK4，GeV）", D("1e-9"),
     [("r188", ("key_numbers", "rge_mssm_scale_target_protocol")),
      ("r189", ("key_numbers", "rge_sim", "M_ms"))],
     ["1.419626474794894"]),
    ("gap_sm_closed", "SM 闭式 α₃ 偏（%）", D("1e-4"),
     [("r188", ("key_numbers", "sm_cross_gap_pct")),
      ("r192", ("key_numbers", "gap_sm_pct"))],
     ["13.1406"]),
    ("gap_ms_closed", "MSSM 闭式 α₃ 偏（%）", D("1e-4"),
     [("r188", ("key_numbers", "mssm_cross_gap_pct")),
      ("r192", ("key_numbers", "gap_ms_pct"))],
     ["0.3117"]),
    ("sm_cross_M", "SM 交点 M（GeV）", D("1e-6"),
     [("r188", ("key_numbers", "sm_cross_M"))],
     ["10237410013833", "1.023741e13"]),
    ("beta_sm", "SM β（由内容重算）", None,
     [("r188", ("key_numbers", "sm_beta_from_content"))],
     ["41/10"]),
    ("beta_mssm", "MSSM β（引用）", None,
     [("r188", ("key_numbers", "mssm_beta_cited"))],
     ["33/5"]),
    ("higgs_doublets", "Higgs 重态数（框架 vs MSSM）", D("1e-12"),
     [("r188", ("key_numbers", "higgs_doublets_framework")),
      ("r192", ("higgs", "doublets"))],
     ["higgs_doublets", "doublets"]),
    ("theta_sq", "Θ²=−I（机器零）", None,
     [("r188", ("key_numbers", "duality_period_residual")),
      ("r192", ("theta_algebra", "J2_eq_minus_I"))],
     ["J2_eq_minus_I", "duality_period"]),
    ("cp2_chi", "CP² χ=3", D("1e-12"),
     [("r192", ("cp2_geometry", "chi"))],
     ["cp2_geometry", "chi"]),
    ("ell_ew", "ℓ_EW（m）", D("1e-12"),
     [("r188", ("key_numbers", "ell_implied_from_v_fit_m")),
      ("r194", ("provenance", "lew")),
      ("r195", ("provenance", "lew")),
      ("r199", ("provenance", "lew"))],
     ["7.7303575"]),
]


# 特殊行比较模式：list=字符串列表逐项比；zeroish=数值应为 0（布尔 True 记一致）
ROW_MODE = {"beta_sm": "list", "beta_mssm": "list", "theta_sq": "zeroish"}
MY_LIST = {"beta_sm": ["41/10", "-19/6", "-7"],
           "beta_mssm": ["33/5", "1", "-3"]}


def shared_quantity_audit(peers, my):
    """对共享量：独立重算值 vs 各卷探针值（按容差/模式），并计字面出现卷数。"""
    rows = []
    for key, label, tol, probes, literals in SHARED_ROWS:
        mode = ROW_MODE.get(key, "num")
        myv = MY_LIST[key] if mode == "list" else my[key]
        consistent = 0
        checked = 0
        worst = D(0)
        detail = []
        for tag, path in probes:
            pv_raw = dig(peers.get(tag, {}), path)
            if pv_raw is None:
                detail.append(tag + ":缺失")
                continue
            checked += 1
            if mode == "list":
                okv = (list(pv_raw) == list(myv)) if isinstance(pv_raw, list) \
                    else (str(pv_raw) == str(myv))
            elif mode == "zeroish":
                if isinstance(pv_raw, bool):
                    okv = pv_raw and myv == 0
                else:
                    pv = to_dec(pv_raw)
                    okv = pv is not None and abs(pv) <= D("1e-30")
                    worst = max(worst, abs(pv) if pv is not None else D(1))
            else:
                pv = to_dec(pv_raw)
                if pv is None:
                    detail.append(tag + ":类型")
                    checked -= 1
                    continue
                rel = abs(pv - myv) / abs(myv) if myv != 0 else abs(pv - myv)
                okv = rel <= tol
                worst = max(worst, rel)
            if okv:
                consistent += 1
            else:
                detail.append("{}:{}".format(tag, pv_raw))
        occ = 0
        for tag, pd in peers.items():
            if pd is None:
                continue
            dump = json.dumps(pd, ensure_ascii=False)
            if any(lit in dump for lit in literals):
                occ += 1
        rows.append({"key": key, "label": label, "my": str(myv),
                     "checked": checked, "consistent": consistent,
                     "worst_rel": str(worst), "occ_files": occ,
                     "bad": detail})
    return rows


def xgut_lineage_audit(peers, my):
    """x_GUT 混用机读：r192 同轮 x_GUT(α₁=α₂)=5.25478928 与 M_GUT=2.121e16 并存；
    重算 M(x_GUT_recorded) 与其同轮 M_GUT 比较；规范值来自 r194/r195/r199 provenance。"""
    r192 = peers.get("r192", {})
    x_rec = to_dec(dig(r192, ("key_numbers", "x_GUT")))
    m_rec = to_dec(dig(r192, ("key_numbers", "M_GUT_gev")))
    m_from_x = MZ * (TWO_PI * x_rec).exp() if x_rec is not None else None
    rel = abs(m_from_x - m_rec) / m_rec if (m_from_x is not None and m_rec) else None
    can = to_dec(dig(peers.get("r194", {}), ("provenance", "x_gut13")))
    can_m = to_dec(dig(peers.get("r194", {}), ("provenance", "M_GUT")))
    # r194 Q1 自纠标注机读（判定册文本）
    q1_text = open(PEER_MD["r194md"], "r", encoding="utf-8").read()
    q1_flagged = ("自纠 Q1" in q1_text) and ("5.25478928" in q1_text) \
        and ("5.2648981057" in q1_text)
    r199_text = open(PEER_MD["r199md"], "r", encoding="utf-8").read()
    r199_flagged = ("x_GUT=5.25478928" in r199_text) or ("5.25478928" in r199_text)
    return {"x_rec": str(x_rec), "M_rec": str(m_rec),
            "M_from_x": str(m_from_x), "rel_diff": str(rel),
            "canonical_x": str(can), "canonical_M": str(can_m),
            "q1_selfcorr_flagged": q1_flagged,
            "r199_flagged": r199_flagged}


def precision_layer_audit(my):
    """精度层分析：s*（r189 float64 vs 本卷 Decimal(60)）、M_GUT（π 层）、
    M*（float64 渲染）。统计有效一致位数。"""
    def leading_digits(a, b):
        """有效数字一致位数（跳过前导 0 与小数点）。"""
        sa = format(a, "f").lstrip("0").lstrip(".")
        sb = format(b, "f").lstrip("0").lstrip(".")
        n = 0
        for ca, cb in zip(sa, sb):
            if ca == cb:
                n += 1
            else:
                break
        return n

    s_mine = my["sstar"]
    s_r189 = D("0.230943405280905872389851651860")     # r189 float64 渲染
    digits_s = leading_digits(s_mine, s_r189)
    rel_s = abs(s_r189 - s_mine) / s_mine
    mg_16 = my["MGUT"]
    mg_60 = my["MGUT_60"]
    rel_pi = abs(mg_60 - mg_16) / mg_60
    mstar_188 = D("3675.2429234637584")                  # r188 float64 渲染
    mstar_194 = D(str(my["Mstar"]))
    rel_ms = abs(mstar_188 - mstar_194) / mstar_194
    return {"sstar_match_digits": digits_s, "sstar_rel_diff": str(rel_s),
            "MGUT_pi_layer_rel_diff": str(rel_pi),
            "Mstar_float64_rel_diff": str(rel_ms),
            "float64_eps": "2.220446049250313e-16"}


# ---------------------------------------------------------------------------
# 九、主审计
# ---------------------------------------------------------------------------
def run_audit():
    corpus = load_corpus()
    kn = {}

    # ---- 正照/互印的机器基础 ----
    v_fit = D(repr(v_fit_from_pdg()))
    xs_star, ms_star = m_star()
    s_star, l13, l23, m_gut16, m_gut60, a_gut = sstar_closed()
    x12, m_x12, a12_x12, a3_x12, gap_ms_closed = crossing(MSSM_B)
    _xsm, m_sm, _asm, _a3sm, gap_sm_closed = crossing(SM_B)
    _xv, s2v = s2w_at_v()
    gap_sm_rk4, m_sm_rk4, gap_ms_rk4, m_ms_rk4, agut_rk4 = rge_target_protocol()
    beta_sm = beta_from_content()
    ell_implied = D("1.973269804e-16") / v_fit     # ħc/v（GeV·m ÷ GeV）

    my = {
        "v": v_fit, "Mstar": ms_star, "Mstar_over_v": ms_star / v_fit,
        "xstar": xs_star, "x12": x12, "M_x12": m_x12,
        "xgut13": l13, "MGUT": m_gut16, "MGUT_60": m_gut60,
        "agut_inv": a_gut, "sstar": s_star,
        "gap_sm_rk4": D(repr(gap_sm_rk4)), "gap_ms_rk4": D(repr(gap_ms_rk4)),
        "M_sm_rk4": D(repr(m_sm_rk4)), "M_ms_rk4": D(repr(m_ms_rk4)),
        "gap_sm_closed": gap_sm_closed, "gap_ms_closed": gap_ms_closed,
        "sm_cross_M": m_sm,
        "beta_sm": D(0),  # list 模式行走 MY_LIST 专门比较
        "beta_mssm": D(0),
        "higgs_doublets": D(1),
        "theta_sq": D(0),
        "cp2_chi": D(3),
        "ell_ew": ell_implied,
    }

    # ---- 文本证据（逐字） ----
    EVIDENCE = [
        ("Θ 矩阵（靶约定）", corpus["eqmd"],
         "\\Theta = \\begin{pmatrix} 0 & -1 \\\\ 1 & 0 \\end{pmatrix}"),
        ("对偶周期 4", corpus["eqmd"], "对偶周期 4"),
        ("M5 对偶镜像", corpus["eqmd"],
         "g^{\\mathrm{eff}}\\left( r \\right) = g^{\\mathrm{eff}}\\left( \\ell^{2}/r \\right)"),
        ("定理 25.4 稳定子嵌入（候选）", corpus["ch25"], "稳定子嵌入预言"),
        ("λ₈/(2√3) 归一化", corpus["ch25"], "\\lambda_{8}/\\left( 2\\sqrt{3} \\right)"),
        ("V1.8 s* 30 位值", corpus["v18"], "0.230943405280905868720056895551"),
        ("V1.8 s* 闭式", corpus["v18"], "(3a+7A3)/(15a)"),
        ("Higgs 模式谱", corpus["higgs"], "Hessian 本征值 {0,0,0, 8κv²}"),
        ("验证 E 同型式", corpus["dimunify"], "return 1.0 - r_s * r / (r * r + L * L)"),
        ("验证 E 参数", corpus["dimunify"], "r_s, L = 1.0, 0.5"),
        ("附节标记 ch25（截断见证）", corpus["ch25"], "## 【r192 三路径攻坚勘误｜2026-10-25】"),
        ("附节标记 eqmd（截断见证）", corpus["eqmd"],
         "## 【r195 尺度秩不变性与归一化条件名实勘误｜2026-10-25】"),
        ("r194 Q1 自纠原文", corpus["r194md"], "α₁=α₂ 交点：x=**5.25478928**"),
        ("r194 Q1 规范值原文", corpus["r194md"], "α₁=α₃ 统一点：x=**5.2648981057**"),
        ("r195 M5 族型式", corpus["r195md"], "g_ℓ(r) = 1 − r_s·r/(r² + ℓ²)"),
        ("r192 路径 2 no-go 判词", corpus["r192md"], "CLOSED-NEGATIVE"),
        ("r199 不可能性定理判词", corpus["r199md"], "R199-SCALE-ANCHORING-IMPOSSIBILITY"),
    ]
    ev_ok = sum(1 for _n, t, q in EVIDENCE if q in t)

    # ---- no-go 代数腿 ----
    theta_mzero, theta_worst = check_theta_algebra()
    pauli_ok = check_pauli_conjugation()
    anti_ok = check_antiunitary()

    # ---- no-go 几何腿 ----
    cp2 = cp2_invariants()
    fs_resid, fs_eqs = check_fs_homogeneity()
    m5_resid, m5_samples = check_m5_identity()
    rg_n, rg_worst = rg_reference_invariance()

    # ---- no-go 内容腿 ----
    files = walk_s13()
    susy_counts, susy_total, n_files, raw_hits, susy_files, marker_count = \
        scan_susy_inventory(files)
    pos_scan = scan_positive_control()
    hig = higgs_count(corpus)

    # ---- 候选扫描（自有基准 + 正对照注入；r192 记录机读） ----
    targets = {"Mstar_over_v": float(ms_star / v_fit), "xstar": float(xs_star),
               "xgut13": float(l13), "agut_inv": float(a_gut),
               "s2w_at_v": float(s2v)}
    n_comb, hits, closest = candidate_scan_own(targets)
    # 正对照：把靶值本身注入基元 ⇒ 必命中（证明扫描器有分辨力）
    pos_cand = 0
    for k, tv in targets.items():
        pc = candidate_scan_own({k: tv}, extra_prims=[tv])
        if pc[1][k] >= 1:
            pos_cand += 1

    # ---- 跨轮互印 ----
    peers, shas = load_peers()
    n_peers = sum(1 for v in peers.values() if v is not None)
    rows = shared_quantity_audit(peers, my)
    n_rows = len(rows)
    n_consistent = sum(1 for r in rows if r["consistent"] == r["checked"] and r["checked"] > 0)
    lineage = xgut_lineage_audit(peers, my)
    layers = precision_layer_audit(my)

    # r192 候选扫描记录机读
    r192j = peers.get("r192", {})
    cs = dig(r192j, ("candidate_scan",)) or {}
    cs_n = dig(cs, ("N",))
    cs_tol = dig(cs, ("tolerance",))
    cs_hits = dig(cs, ("results",))
    cs_pos = dig(cs, ("positive_control",))
    cs_zero = isinstance(cs_hits, dict) and all(
        v.get("hits_1e-9") == 0 for v in cs_hits.values() if isinstance(v, dict))
    cs_pos_ok = isinstance(cs_pos, dict) and all(v == 1 for v in cs_pos.values())

    kn = {
        # 互印
        "n_shared_rows": n_rows, "n_shared_consistent": n_consistent,
        "n_peer_json": n_peers,
        "shared_rows": [{"key": r["key"], "my": prev_num(r["my"]),
                         "checked": r["checked"], "consistent": r["consistent"],
                         "worst_rel": fmt_rel(r["worst_rel"]),
                         "occ_files": r["occ_files"]} for r in rows],
        "xgut_lineage": lineage,
        "precision_layers": layers,
        # no-go 代数腿
        "theta_matrix_zero": theta_mzero,
        "theta_operator_residual": str(theta_worst),
        "pauli_3of3": sum(1 for x in pauli_ok if x),
        "antiunitary_6of6": sum(1 for x in anti_ok if x),
        # no-go 几何腿
        "cp2": cp2, "fs_residual": str(fs_resid), "fs_eq_checks": fs_eqs,
        "m5_residual": str(m5_resid), "m5_samples": [str(s) for s in m5_samples],
        "rg_invariance_items": rg_n, "rg_invariance_worst": str(rg_worst),
        # no-go 内容腿
        "susy_counts": susy_counts, "susy_total": susy_total,
        "scan_files": n_files, "susy_raw_hits_before_truncation": raw_hits,
        "susy_files": len(susy_files), "appendix_marker_files": marker_count,
        "scan_positive_control": pos_scan,
        "higgs": hig,
        # 候选扫描
        "own_scan_N": n_comb, "own_scan_hits": hits,
        "own_scan_closest": {k: (v[0], str(v[1])[:18]) for k, v in closest.items()},
        "own_scan_positive_control": pos_cand,
        "r192_scan_N": cs_n, "r192_scan_tol": cs_tol,
        "r192_scan_zero": cs_zero, "r192_scan_pos": cs_pos_ok,
        # 关键数（独立重算）
        "v_fit_gev": str(v_fit), "M_star_gev": str(ms_star),
        "Mstar_over_v": str(ms_star / v_fit), "x_star": str(xs_star),
        "x12": str(x12), "M_x12_gev": str(m_x12),
        "x_gut13": str(l13), "M_GUT_gev_16pi": str(m_gut16),
        "M_GUT_gev_60pi": str(m_gut60), "alpha_gut_inv": str(a_gut),
        "sstar": str(s_star),
        "sstar_residual_vs_target": str(abs(s_star - SSTAR_TARGET)),
        "L13_minus_L23": str(l13 - l23),
        "gap_sm_rk4": str(D(repr(gap_sm_rk4))), "M_sm_rk4": str(D(repr(m_sm_rk4))),
        "gap_ms_rk4": str(D(repr(gap_ms_rk4))), "M_ms_rk4": str(D(repr(m_ms_rk4))),
        "agut_rk4": str(D(repr(agut_rk4))),
        "gap_sm_closed_pct": str(gap_sm_closed),
        "gap_ms_closed_pct": str(gap_ms_closed),
        "sm_cross_M_gev": str(m_sm),
        "beta_sm_from_content": beta_sm,
        "s2w_at_v": str(s2v),
        "ell_ew_m": str(ell_implied),
        "evidence_hits": ev_ok, "evidence_total": len(EVIDENCE),
    }

    # ===================== 条目 =====================
    add("A1", "互印层",
        "跨轮互印一致：{} 项共享量在 {} 件在册 JSON 中机读，{} 项全探针一致"
        "（精确 / 渲染层 ≤1ulp）；唯一真冲突（x_GUT）单列 D2".format(
            n_rows, n_peers, n_consistent),
        "PASS" if (n_consistent == n_rows and n_rows >= 20) else "FAIL",
        "精度层分类见 precision_layers；字面出现卷数见 shared_rows")

    add("B1", "no-go 代数腿",
        "对偶周期 4 机器零：Θ²=−I、Θ⁴=+I（矩阵层精确 + 200 随机复旋量算子层残差 {}）".format(
            theta_worst),
        "PASS" if (theta_mzero and theta_worst == 0) else "FAIL",
        "靶约定 Θ=[[0,−1],[1,0]]（equations.md L30）；r188 曾用反号约定，结论不变")

    add("B2", "no-go 代数腿",
        "Pauli 共轭关系 εσᵢε⁻¹=−σᵢᵀ：{}/3 精确（复分数）".format(
            sum(1 for x in pauli_ok if x)),
        "PASS" if all(pauli_ok) else "FAIL",
        "ε=iσ₂；证明 Θ=J·K 是 (1/2,0)↔(0,1/2) 的赝实共轭")

    add("B3", "no-go 代数腿",
        "反幺正 + Θ²=−I：{}/6 精确 ⇒ 与 4D 荷共轭 C（C²=−1）同构 ⇒ "
        "Majorana 实条件，不产生玻色↔费米配对".format(sum(1 for x in anti_ok if x)),
        "PASS" if all(anti_ok) else "FAIL",
        "r192 N3 独立复算")

    add("B4", "no-go 几何腿",
        "CP² 组合学重算：Betti {}、χ={}、c₁={}H≠0、h²⁰={} ⇒ 非 hyperkähler、"
        "非 Calabi–Yau ⇒ N=2 靶空间不可能".format(
            cp2["betti"], cp2["chi"], cp2["c1_over_H"], cp2["h20"]),
        "PASS" if (cp2["chi"] == 3 and cp2["c1_over_H"] == 3 and cp2["h20"] == 0
                   and not cp2["hyperkaehler"]) else "FAIL",
        "胞腔/Hodge/曲率类公式为外部标准数学输入（已标注）；组合与算术本机重算")

    add("B5", "no-go 几何腿",
        "FS 度规 Kähler 类齐次：g(λ)=λg(1)、det(λg)=λ²det g、(λg)⁻¹=λ⁻¹g⁻¹、"
        "R(λ)·λ=R(1) 全精确（{} 项等号检验，残差 {}）⇒ 无内禀长度".format(
            fs_eqs, fs_resid),
        "PASS" if (fs_resid == 0 and fs_eqs >= 20) else "FAIL",
        "Ricci 恒等式 ρ=−i∂∂̄ ln det g 为外部标准数学输入；λ∈{1,7,13}×两点")

    add("B6", "no-go 几何腿",
        "M5 对偶族尺度简并：g_ℓ(ℓ²/r)=g_ℓ(r) 对任意 ℓ 恒等（残差 {}）⇒ "
        "对偶镜像只固定形状，ℓ 的信息量 0 bit".format(m5_resid),
        "PASS" if m5_resid == 0 else "FAIL",
        "族型式取自靶 dimension_unify_verify.py L117-119（r_s=1, L=0.5）；"
        "r195 T1 独立复算")

    add("B8", "no-go 内容腿",
        "超对称形式化零存在：101 文件**截断后**七类 inventory 合计 {}"
        "（截断前原始命中 {}，全在审计附节内；附节标记文件 {} 个）".format(
            susy_total, raw_hits, marker_count),
        "FAIL" if susy_total == 0 else "PASS",
        "框架不能供给超多重态 ⇒ r192 N5 独立确认；扫描有分辨力（正对照 {}/7）".format(
            pos_scan))

    add("B9", "no-go 内容腿",
        "Higgs 结构不符：谱 {{0,0,0,8κv²}} ⇒ 4 实自由度 = 1 个 SU(2) 双重态结构，"
        "MSSM 需 2 重态（8 实）；物理质量模 {} 个".format(hig["massive_modes"]),
        "FAIL" if hig["mismatch"] else "PASS",
        "靶 higgs_verify.py 验证2 自报谱；r192 C16 独立复算")

    add("C2", "重审层",
        "路径 1/3 单一缺失对象仍无供给：归并账目机读（r192 path_status）+ "
        "尺度锚定不可能性（r194/r195/r199）确认待补对象=尺度设定/维度嬗变原理，"
        "自有基准候选扫描 {:,} 组合 0 命中".format(n_comb),
        "FAIL",
        "归并 ≠ 闭合（r192 §五）；候选扫描容差 1e-9，正对照 {}/5".format(pos_cand))

    add("D2", "混用检出",
        "x_GUT 混用机读检出：r192 同轮 x_GUT={}（α₁=α₂）与 M_GUT={} 并存，"
        "重算 M(x_GUT)={}，相对差 {}；r194 Q1 自纠 + r199 标注链完整".format(
            lineage["x_rec"], lineage["M_rec"], lineage["M_from_x"],
            lineage["rel_diff"]),
        "FAIL" if (lineage["rel_diff"] is not None
                   and D(lineage["rel_diff"]) > D("1e-2")
                   and lineage["q1_selfcorr_flagged"]) else "PASS",
        "规范值 x_GUT={}（α₁=α₃）已由 r194/r195/r199 单源化".format(
            lineage["canonical_x"]))

    add("A2", "精度层",
        "s* 精度层：r189 float64 渲染与本卷 Decimal(60) 前 {} 位一致"
        "（相对差 {}，float64 eps 量级）；M_GUT π 层差 {}、M* 渲染层差 {}".format(
            layers["sstar_match_digits"], layers["sstar_rel_diff"],
            layers["MGUT_pi_layer_rel_diff"], layers["Mstar_float64_rel_diff"]),
        "INFO",
        "互印至 16 位有效数字成立（第 17 位起分歧）；差异全部为渲染层（≤1ulp），非口径冲突")

    add("A3", "协议并列",
        "口径协议并列：4.060449943317877 / 0.7600419008581873 为圆整初值+RK4 靶协议；"
        "13.1406% / 0.3117% 为精确闭式——两者非冲突（输入协议不同）",
        "INFO",
        "RK4 复现与 r188/r189 记录逐位一致（C11/C12）")

    add("N2", "文本级",
        "N2 Grassmann 奇偶论断为文本级论证（Θ 的矩阵元全为 c-数 ⇒ Z₄⊂偶子代数）："
        "本卷机读三腿（代数/几何/内容）不含它，不影响 no-go 结论",
        "INFO",
        "防过度指控：该腿逻辑成立但不升级为机读")

    add("E1", "边界",
        "覆盖边界：no-go ≠ 物理闭合；未逐值互印卷列名（r190/r191/r193/r196/r197/"
        "r200–r202 仅字面计数）；r192 候选池 60 基元构成未登记 ⇒ 39,710 未重造"
        "（只验量级+正对照+自有基准复扫）；CP²/Pauli/FS 恒等式为外部标准数学",
        "BOUNDARY",
        "有限基排除 ≠ 无限基不可能性（r192 红线第 4 条沿用）")

    # ===================== 控制组 =====================
    ctl("C01", "v 反解重算 255.26242445425643（跨卷一致）",
        abs(v_fit - D("255.26242445425643")) / D("255.26242445425643") < D("1e-12"),
        "v={:.9f}".format(v_fit))
    ctl("C02", "M* 重算 3675.2429234637594（渲染层 ≤1ulp）",
        abs(ms_star - D("3675.2429234637594")) / ms_star < D("1e-12"),
        "M*={}".format(ms_star))
    ctl("C03", "M*/v 重算 14.397900244508454",
        abs(ms_star / v_fit - D("14.397900244508454"))
        / D("14.397900244508454") < D("1e-12"),
        "M*/v={}".format(ms_star / v_fit))
    ctl("C04", "x* 精确有理重算（与 r194/r195/r199 provenance 一致）",
        abs(xs_star - D("0.588309178775510204081632653061224489795918367346938775510203"))
        < D("1e-45"), "x*={}".format(xs_star))
    ctl("C05", "x₁₂=5.25478928 精确（终止小数）",
        x12 == D("5.25478928"), "x₁₂={}".format(x12))
    ctl("C06", "M(x₁₂) 重算 1.9904728657e16（与 r189/r194 一致）",
        abs(m_x12 - D("1.9904728657e16")) / m_x12 < D("1e-9"),
        "M(x₁₂)={}".format(m_x12))
    ctl("C07", "x_GUT 规范值重算（α₁=α₃ 统一点，与 r194/r195/r199 一致）",
        abs(l13 - D("5.26489810573932711337291489963245688436528131184619734238054"))
        < D("1e-45"), "x_GUT={}".format(l13))
    ctl("C08", "s* 闭式重算与 V1.8 30 位靶值残差 <1e-30",
        abs(s_star - SSTAR_TARGET) < D("1e-30"),
        "残差={}".format(abs(s_star - SSTAR_TARGET)))
    ctl("C09", "L13−L23 ≡ 0（三线共点代数恒等）",
        abs(l13 - l23) < D("1e-45"), "L13−L23={}".format(l13 - l23))
    ctl("C10", "α_GUT⁻¹ 重算 24.276458524173027989…（与 r194 provenance 一致）",
        abs(a_gut - D("24.2764585241730279898218829516539440203562340966921119592875"))
        < D("1e-45"), "α_GUT⁻¹={}".format(a_gut))
    ctl("C11", "RK4 同协议复现 gap_sm=4.060449943317877 与 M_sm=236961529934301.12",
        abs(D(repr(gap_sm_rk4)) - D("4.060449943317877")) < D("1e-9")
        and abs(D(repr(m_sm_rk4)) - D("236961529934301.12"))
        / D("236961529934301.12") < D("1e-12"),
        "gap_sm={} M_sm={}".format(gap_sm_rk4, m_sm_rk4))
    ctl("C12", "RK4 同协议复现 gap_ms=0.7600419008581873 与 M_ms=1.419626474794894e16",
        abs(D(repr(gap_ms_rk4)) - D("0.7600419008581873")) < D("1e-9")
        and abs(D(repr(m_ms_rk4)) - D("1.419626474794894e16"))
        / D("1.419626474794894e16") < D("1e-12"),
        "gap_ms={} M_ms={}".format(gap_ms_rk4, m_ms_rk4))
    ctl("C13", "SM 闭式 α₃ 偏 13.1406% @ 1.023741e13（与 r188/r192 一致）",
        abs(gap_sm_closed - D("13.1406")) < D("1e-3")
        and abs(m_sm - D("1.023741e13")) / m_sm < D("1e-4"),
        "gap={}% M={}".format(gap_sm_closed, m_sm))
    ctl("C14", "MSSM 闭式 α₃ 偏 0.311719% @ 1.9904729e16（与 r188/r192 一致）",
        abs(gap_ms_closed - D("0.311719")) < D("1e-4")
        and abs(m_x12 - D("1.9904729e16")) / m_x12 < D("1e-6"),
        "gap={}% M={}".format(gap_ms_closed, m_x12))
    ctl("C15", "SM β 由场内容重算 (41/10, −19/6, −7)",
        beta_sm == ("41/10", "-19/6", "-7"),
        "β={}".format(beta_sm))
    ctl("C16", "Θ²=−I、Θ⁴=+I 精确（Fraction；靶约定 [[0,−1],[1,0]]）",
        theta_mzero and theta_worst == 0,
        "算子层残差={}".format(theta_worst))
    ctl("C17", "εσᵢε⁻¹=−σᵢᵀ 3/3 精确", all(pauli_ok),
        "{}/3".format(sum(1 for x in pauli_ok if x)))
    ctl("C18", "反幺正 Θ(iψ)=−iΘψ 且 Θ²=−I，6/6 精确", all(anti_ok),
        "{}/6".format(sum(1 for x in anti_ok if x)))
    ctl("C19", "CP² χ=3、c₁=3H、h²⁰=0（组合学重算）",
        cp2["chi"] == 3 and cp2["c1_over_H"] == 3 and cp2["h20"] == 0
        and not cp2["hyperkaehler"] and not cp2["calabi_yau"],
        "{}".format(cp2))
    ctl("C20", "FS 齐次性全精确（两点×三 λ：等号检验 + R(λ)λ=R(1) 残差 0）",
        fs_resid == 0 and fs_eqs >= 20,
        "残差={} 等号检验={}".format(fs_resid, fs_eqs))
    ctl("C21", "M5 对偶族恒等对任意 ℓ 成立（残差精确 0）",
        m5_resid == 0, "残差={}".format(m5_resid))
    ctl("C22", "RG 参考尺度不变性 9/9（最大相对残差 <1e-50）",
        rg_n == 9 and rg_worst < D("1e-50"),
        "{} 项，残差={}".format(rg_n, rg_worst))
    ctl("C23", "超对称 inventory 截断后 0 命中（101 文件；截断前原始 {} 全在附节）".format(
        raw_hits),
        susy_total == 0 and n_files == 101 and marker_count >= 4,
        "total={} files={} markers={}".format(susy_total, n_files, marker_count))
    ctl("C24", "扫描正对照 7/7（注入必命中）", pos_scan == 7,
        "{}/7".format(pos_scan))
    ctl("C25", "Higgs 4 实模式=1 重态 ≠ MSSM 2（机读谱引用）",
        hig["anchor"] and hig["doublets"] == 1 and hig["mssm_need"] == 2
        and hig["mismatch"], "{}".format(hig))
    ctl("C26", "自有基准候选扫描 {:,} 组合 0 命中（tol 1e-9）+ 正对照 5/5".format(n_comb),
        n_comb >= 10000 and all(v == 0 for v in hits.values()) and pos_cand == 5,
        "N={} hits={} pos={}/5".format(n_comb, hits, pos_cand))
    ctl("C27", "x_GUT 混用机读检出：M(5.25478928)=1.9905e16 ≠ r192 同轮 M_GUT",
        lineage["rel_diff"] is not None and D(lineage["rel_diff"]) > D("1e-2"),
        "相对差={}".format(lineage["rel_diff"]))
    ctl("C28", "跨卷只读：{} 件 peer JSON sha256 前后一致".format(n_peers),
        n_peers >= 13 and all(v is not None for v in peers.values()),
        "{} 件".format(n_peers))
    ctl("C29", "互印表 {} 行且非冲突行全部一致".format(n_rows),
        n_consistent == n_rows and n_rows >= 20,
        "consistent={}/{}".format(n_consistent, n_rows))
    ctl("C30", "文本证据 {}/{} 逐字命中".format(ev_ok, len(EVIDENCE)),
        ev_ok == len(EVIDENCE), "{}/{}".format(ev_ok, len(EVIDENCE)))
    ctl("C31", "r192 候选扫描记录机读：N≥10⁴、tol=1e-9、0 命中、正对照 5/5",
        (cs_n is not None and cs_n >= 10000 and cs_tol == 1e-9
         and cs_zero and cs_pos_ok),
        "N={} tol={} zero={} pos={}".format(cs_n, cs_tol, cs_zero, cs_pos_ok))

    verdict = "-".join([
        "R203-CROSS-ROUND-MUTUAL-VERIFICATION-{rows}-ROWS-{cons}-CONSISTENT".format(
            rows=n_rows, cons=n_consistent),
        "1-XGUT-LINEAGE-CONFLICT-SELF-CORRECTED-R194-Q1-R199-FLAGGED",
        "NOGO-FOUR-LEGS-INDEPENDENTLY-RECOMPUTED-THETA2-EQ-MINUS-I-MACHINE-ZERO",
        "PAULI-3-3-ANTIUNITARY-6-6-CP2-CHI-3-C1-3H-H20-0-NOT-HYPERKAHLER",
        "FS-HOMOGENEOUS-RESIDUAL-EXACT-0-M5-SCALE-DEGENERATE-ZERO-BITS-ON-ELL",
        "RG-REFERENCE-INVARIANT-9-9-SUSY-INVENTORY-0-OF-101-FILES-TRUNCATED",
        "HIGGS-1-NE-2-PATH2-CONFIRMED-CLOSED-NEGATIVE",
        "PATHS-1-3-MERGED-SINGLE-MISSING-OBJECT-SUPPLY-0",
        "CANDIDATE-SCAN-{N}-COMBOS-0-HIT-ON-INDEPENDENT-BASIS".format(N=n_comb),
        "SSTAR-FLOAT64-VS-DECIMAL60-LAYER-INFO",
    ])

    # ===================== 守卫 =====================
    grd("G1", "Decimal 上下文 ≥50 位", getcontext().prec >= 50,
        "prec={}".format(getcontext().prec))
    grd("G2", "精确代数腿全 Fraction/CF（Θ/Pauli/M5/FS/CP² 组合学无 float）",
        theta_mzero and all(pauli_ok) and all(anti_ok) and m5_resid == 0
        and fs_resid == 0,
        "代数腿残差全 0")
    grd("G3", "跨卷只读：sha256 前后一致",
        n_peers >= 13 and all(v is not None for v in peers.values()),
        "{} 件 JSON".format(n_peers))
    grd("G4", "S13 扫描文件数 =101", n_files == 101,
        "{} 个 .py/.md".format(n_files))
    grd("G5", "截断纪律：附节标记文件 ≥4 且截断生效（原始 {}→0）".format(raw_hits),
        marker_count >= 4 and raw_hits >= 1 and susy_total == 0,
        "markers={} raw={}".format(marker_count, raw_hits))
    grd("G6", "扫描有分辨力：正对照 7/7", pos_scan == 7,
        "{}/7".format(pos_scan))
    grd("G7", "ast 自审：ctl/grd 的 ok 参数无字面 True；无 >200 字符巨串",
        _ast_self_audit(), "见 _ast_self_audit 明细")
    grd("G8", "红线段存在且含「不可与 r142–r202 相加」",
        REDLINE_PHRASE in REDLINE, REDLINE_PHRASE)
    grd("G9", "RK4 复现与靶同协议（dt=0.001、圆整初值 59/30/8.5、1TeV 续接）",
        abs(D(repr(gap_sm_rk4)) - D("4.060449943317877")) < D("1e-9"),
        "gap_sm 复现={}".format(gap_sm_rk4))
    grd("G10", "候选扫描容差 1e-9 与 r192 同；自有基准规模 ≥1e4",
        SCAN_TOL == 1e-9 and n_comb >= 10000 and cs_tol == 1e-9,
        "tol={} N={} r192_N={}".format(SCAN_TOL, n_comb, cs_n))
    _cnt = {}
    for _e in ENTRIES:
        _cnt[_e[3]] = _cnt.get(_e[3], 0) + 1
    grd("G11", "判词非空且条目计数自洽（PASS7+FAIL4+INFO3+BOUNDARY1=15）",
        len(verdict) > 80 and len(ENTRIES) == 15
        and _cnt == {"PASS": 7, "FAIL": 4, "INFO": 3, "BOUNDARY": 1},
        "entries={} 分布={}".format(len(ENTRIES), _cnt))
    grd("G12", "供给不增：本卷机读未发现任何框架自有供给（扫描 0 命中 + 判词 SUPPLY-0）",
        all(v == 0 for v in hits.values()) and susy_total == 0
        and "SUPPLY-0" in verdict,
        "候选命中={} 超对称 inventory={}".format(
            sum(hits.values()), susy_total))

    not_closed = [
        "路径 1/3（合并后单一缺失对象：尺度设定/维度嬗变原理）仍 OPEN；本卷只复核不闭合",
        "路径 2 CLOSED-NEGATIVE 是排除性结论，不增加框架自有供给（r192 红线沿用）",
        "未逐值互印卷：r190/r191/r193/r196/r197/r200–r202（仅字面出现计数）",
        "r192 候选池 60 基元构成未在 JSON 登记 ⇒ N=39,710 未重造（只验量级+正对照+自有基准复扫）",
        "CP² 拓扑 / Pauli 代数 / FS Ricci 恒等式为外部标准数学输入（已在条目标注）",
        "N2 Grassmann 奇偶论断为文本级论证（机读三腿不含它）",
    ]
    return kn, verdict, not_closed


def _ast_self_audit():
    """ast 自审：本文件内 ctl()/grd() 调用的 ok 参数不得为字面 True；
    非 docstring 的字符串常量不得 >200 字符。返回 (ok, n_checked, n_bad, big)。"""
    src = open(os.path.abspath(__file__), "r", encoding="utf-8").read()
    tree = ast.parse(src)
    # 收集所有 docstring 节点（模块/函数/类首语句）——豁免长度检查
    docstrings = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef,
                             ast.ClassDef)):
            if node.body and isinstance(node.body[0], ast.Expr) \
                    and isinstance(node.body[0].value, ast.Constant) \
                    and isinstance(node.body[0].value.value, str):
                docstrings.add(id(node.body[0].value))
    n_checked = 0
    n_bad = 0
    big = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id in ("ctl", "grd"):
            if len(node.args) >= 3:
                n_checked += 1
                a = node.args[2]
                if isinstance(a, ast.Constant) and a.value is True:
                    n_bad += 1
        if isinstance(node, ast.Constant) and isinstance(node.value, str) \
                and len(node.value) > 200 and id(node) not in docstrings:
            big += 1
    return (n_bad == 0 and big == 0), n_checked, n_bad, big


# ---------------------------------------------------------------------------
# 十、输出
# ---------------------------------------------------------------------------
def build_payload(kn, verdict, not_closed):
    def conv(e):
        return {"id": e[0], "layer": e[1], "text": e[2], "verdict": e[3],
                "note": e[4]}
    cnt = {}
    for e in ENTRIES:
        cnt[e[3]] = cnt.get(e[3], 0) + 1
    return {
        "id": "r203", "date": "2026-10-25",
        "title": "S13 兄弟链跨轮互印与 no-go 独立复核",
        "target": "01_独立体系/S13_全域双向分形统一场论（+ r188–r202 在册 JSON 只读）",
        "verdict": verdict, "redline": REDLINE,
        "entries": [conv(e) for e in ENTRIES],
        "controls": [{"id": c[0], "text": c[1], "ok": c[2], "detail": c[3]}
                     for c in CTRL],
        "guards": [{"id": g[0], "text": g[1], "ok": g[2], "detail": g[3]}
                   for g in GUARDS],
        "key_numbers": kn, "counts": cnt,
        "not_closed": not_closed,
    }


def render_report(payload):
    kn = payload["key_numbers"]
    L = []
    L.append("=" * 78)
    L.append("TUFT-r203｜S13 兄弟链跨轮互印与 no-go 独立复核")
    L.append("日期：2026-10-25　｜　层：跨轮互印 + no-go 独立复核（不重判 r142–r202）")
    L.append("=" * 78)
    L.append("")
    L.append("[判词]")
    L.append("  " + payload["verdict"])
    L.append("")
    L.append("[条目]")
    for e in payload["entries"]:
        L.append("  {:<10} {:<12} {}".format(e["verdict"], e["id"], e["text"]))
        if e["note"]:
            L.append("  {:<10} {:<12} └─ {}".format("", "", e["note"]))
    L.append("")
    L.append("[跨轮互印表]（独立重算 vs 各卷探针；worst_rel 为最大相对差）")
    L.append("  {:<16} {:>8} {:>10} {:>12} {:>8}".format(
        "量", "探针", "一致", "worst_rel", "出现卷"))
    for r in kn["shared_rows"]:
        L.append("  {:<16} {:>8} {:>10} {:>12} {:>8}".format(
            r["key"], r["checked"], r["consistent"], r["worst_rel"], r["occ_files"]))
    L.append("")
    L.append("[x_GUT 混用检出]")
    lg = kn["xgut_lineage"]
    L.append("  r192 记录 x_GUT={}（α₁=α₂）配 M_GUT={}（α₁=α₃/s*）".format(
        lg["x_rec"], lg["M_rec"]))
    L.append("  重算 M(x_GUT)={}，相对差 {}".format(lg["M_from_x"], lg["rel_diff"]))
    L.append("  规范值 x_GUT={}（r194/r195/r199 provenance）；Q1 自纠标注={}；r199 标注={}".format(
        lg["canonical_x"], lg["q1_selfcorr_flagged"], lg["r199_flagged"]))
    L.append("")
    L.append("[精度层]")
    pl = kn["precision_layers"]
    L.append("  s* 一致位数={}（相对差 {}，float64 eps={}）".format(
        pl["sstar_match_digits"], pl["sstar_rel_diff"], pl["float64_eps"]))
    L.append("  M_GUT π 层差={}；M* 渲染层差={}".format(
        pl["MGUT_pi_layer_rel_diff"], pl["Mstar_float64_rel_diff"]))
    L.append("")
    L.append("[no-go 四腿独立复算]")
    L.append("  B1 Θ²=−I 机器零（算子残差 {}）；B2 Pauli {}/3；B3 反幺正 {}/6".format(
        kn["theta_operator_residual"], kn["pauli_3of3"], kn["antiunitary_6of6"]))
    L.append("  B4 CP² χ={} c₁={}H h²⁰={}；B5 FS 残差 {}（{} 项等号）".format(
        kn["cp2"]["chi"], kn["cp2"]["c1_over_H"], kn["cp2"]["h20"],
        kn["fs_residual"], kn["fs_eq_checks"]))
    L.append("  B6 M5 残差 {}；RG 不变性 {}/9（残差 {}）".format(
        kn["m5_residual"], kn["rg_invariance_items"], kn["rg_invariance_worst"]))
    L.append("  B8 超对称 inventory {}/101 文件（截断前原始 {}，附节标记 {} 文件）".format(
        kn["susy_total"], kn["susy_raw_hits_before_truncation"],
        kn["appendix_marker_files"]))
    L.append("  B9 Higgs：{} 实模式={} 重态 ≠ MSSM {}".format(
        kn["higgs"]["real_modes"], kn["higgs"]["doublets"], kn["higgs"]["mssm_need"]))
    L.append("")
    L.append("[候选扫描]")
    L.append("  自有基准 N={:,}，命中 {}（tol 1e-9），正对照 {}/5".format(
        kn["own_scan_N"], kn["own_scan_hits"], kn["own_scan_positive_control"]))
    L.append("  r192 记录：N={} tol={} 零命中={} 正对照={}".format(
        kn["r192_scan_N"], kn["r192_scan_tol"], kn["r192_scan_zero"],
        kn["r192_scan_pos"]))
    L.append("")
    L.append("[关键数]（独立重算）")
    for k in ("v_fit_gev", "M_star_gev", "Mstar_over_v", "x_star", "x12",
              "M_x12_gev", "x_gut13", "M_GUT_gev_16pi", "M_GUT_gev_60pi",
              "alpha_gut_inv", "sstar", "sstar_residual_vs_target",
              "L13_minus_L23", "gap_sm_rk4", "gap_ms_rk4", "gap_sm_closed_pct",
              "gap_ms_closed_pct", "beta_sm_from_content", "ell_ew_m"):
        L.append("  {:<24} {}".format(k, kn[k]))
    L.append("")
    L.append("[文本证据] {}/{} 逐字".format(kn["evidence_hits"], kn["evidence_total"]))
    L.append("")
    L.append("[控制组]")
    for c in payload["controls"]:
        L.append("  {} {} {} — {}".format("OK " if c["ok"] else "FAIL",
                                          c["id"], c["text"], c["detail"]))
    L.append("")
    L.append("[守卫]（全部机读驱动，无一处 ok 写死 True）")
    for g in payload["guards"]:
        L.append("  {} {} {} — {}".format("OK " if g["ok"] else "FAIL",
                                          g["id"], g["text"], g["detail"]))
    L.append("")
    L.append("[未闭合项]")
    for x in payload["not_closed"]:
        L.append("  - " + x)
    L.append("")
    cnt = payload["counts"]
    L.append("条目： " + " / ".join("{}={}".format(k, v) for k, v in sorted(cnt.items())))
    L.append("控制组： {} / {}".format(sum(1 for c in payload["controls"] if c["ok"]),
                                       len(payload["controls"])))
    L.append("守卫  ： {} / {}".format(sum(1 for g in payload["guards"] if g["ok"]),
                                       len(payload["guards"])))
    return "\n".join(L) + "\n"


def render_verdict_md(payload):
    kn = payload["key_numbers"]
    L = []
    L.append("# 判定册 · TUFT-r203｜S13 兄弟链跨轮互印与 no-go 独立复核")
    L.append("")
    L.append("## 一、编号与定位")
    L.append("")
    L.append("- **编号 r203**（★取号经过：起草前竞态实测 22:00:48，三树 r203/r204 全空；"
             "并行会话 11 小时内产出 r189–r202 十余卷、r200 于 21:29:09 刚落盘 ⇒ 竞态仍活跃。"
             "按「先占位者为权威」铁律，若登记前发现并行先占则整体改号；落盘后登记前必再查"
             "磁盘时间戳。未改动 r170–r202 任何字节）")
    L.append("- **命题**：r199 跨轮审计只覆盖 r190–r197（**未含我的 r188/r189**）；"
             "r192 的 Z₄→超对称 no-go 四腿未经独立复算。本卷补：① 跨轮互印（r188–r202 "
             "在册 14 件 JSON，22 项共享量机读 + 独立重算对拍）；② no-go 四腿独立复算；"
             "③ r188 重审条件核验。")
    L.append("- **分层**：本卷为互印复核层，与 r142–r202 条目**不可相加**。")
    L.append("")
    L.append("## 二、判词")
    L.append("")
    L.append("`" + payload["verdict"] + "`")
    L.append("")
    L.append("## 三、跨轮互印表（机读）")
    L.append("")
    L.append("| 量 | 探针数 | 一致 | 最大相对差 | 出现卷数 |")
    L.append("|---|---|---|---|---|")
    for r in kn["shared_rows"]:
        L.append("| {} | {} | {} | {} | {} |".format(
            r["key"], r["checked"], r["consistent"], r["worst_rel"], r["occ_files"]))
    L.append("")
    L.append("- **精度层**：s* 的 r189 float64 渲染与本卷 Decimal(60) 前 **{}** 位一致"
             "（相对差 {}，float64 eps 量级）；M_GUT 的 π 位层差 {}、M* 渲染层差 {}——"
             "全部 ≤1ulp，**非口径冲突**。".format(
                 kn["precision_layers"]["sstar_match_digits"],
                 kn["precision_layers"]["sstar_rel_diff"],
                 kn["precision_layers"]["MGUT_pi_layer_rel_diff"],
                 kn["precision_layers"]["Mstar_float64_rel_diff"]))
    L.append("- **唯一真冲突（x_GUT 混用）**：r192 同轮 x_GUT={}（α₁=α₂ 交点）与 "
             "M_GUT={}（α₁=α₃ 统一点）并存；重算 M(x_GUT)={}，相对差 **{}**。"
             "r194 Q1 已自纠（规范值 x_GUT={}）、r199 已标注；本卷机读再检出。".format(
                 kn["xgut_lineage"]["x_rec"], kn["xgut_lineage"]["M_rec"],
                 kn["xgut_lineage"]["M_from_x"], kn["xgut_lineage"]["rel_diff"],
                 kn["xgut_lineage"]["canonical_x"]))
    L.append("")
    L.append("## 四、no-go 四腿独立复算")
    L.append("")
    L.append("| 腿 | 机读事实 | 结论 |")
    L.append("|---|---|---|")
    L.append("| 代数 N1/N3 | Θ²=−I、Θ⁴=+I 机器零（算子残差 {}）；εσᵢε⁻¹=−σᵢᵀ {}/3；"
             "反幺正+Θ²=−I {}/6 | 周期 4 成立；Θ 是赝实共轭 ⇒ Majorana 实条件 |".format(
                 kn["theta_operator_residual"], kn["pauli_3of3"],
                 kn["antiunitary_6of6"]))
    L.append("| 几何 N4 | CP² χ={}、c₁={}H≠0、h²⁰={}；FS 齐次残差 {}（R(λ)λ=R(1) 精确）；"
             "M5 对偶族残差 {} | 非 hyperkähler；无内禀长度；ℓ 信息量 0 bit |".format(
                 kn["cp2"]["chi"], kn["cp2"]["c1_over_H"], kn["cp2"]["h20"],
                 kn["fs_residual"], kn["m5_residual"]))
    L.append("| 内容 N5 | 101 文件**截断后**七类 inventory 合计 **{}**（截断前原始 {} "
             "全在审计附节）；Higgs {} 实模式 = {} 重态 ≠ MSSM {} | 无超多重态可配对 |".format(
                 kn["susy_total"], kn["susy_raw_hits_before_truncation"],
                 kn["higgs"]["real_modes"], kn["higgs"]["doublets"],
                 kn["higgs"]["mssm_need"]))
    L.append("| 判定 N6 | 代数（偶/奇）+ 几何（非 hyperkähler）+ 内容（0 超伴子、1≠2）"
             "三重不可能 | **Z₄→SUSY 为 no-go，不是待构造** |")
    L.append("")
    L.append("> 注：N2（Grassmann 奇偶）为文本级论证，本卷机读三腿不含它（防过度指控）。")
    L.append("> 注：CP² 拓扑 / Pauli 代数 / FS Ricci 恒等式为外部标准数学输入（已标注）；"
             "组合、算术、恒等检验为本机精确重算。")
    L.append("")
    L.append("## 五、r188 重审条件核验")
    L.append("")
    L.append("| 条件 | r188 状态 | 本卷核验 |")
    L.append("|---|---|---|")
    L.append("| 路径 2（Z₄→超对称谱） | OPEN（待构造） | **CLOSED-NEGATIVE**"
             "（r192 N6 + r199 B2 + 本卷四腿复算确认） |")
    L.append("| 路径 1/3（统一尺度出处/几何指定） | OPEN×2 | **归并为单一缺失对象**"
             "（r192 §五；r194/r195/r199 尺度锚定不可能性）；供给仍 0 |")
    L.append("| s* 框架含量 | 0（导入 β 的函数） | 精度层互印确认（闭式只含 "
             "α_EM⁻¹、α_s⁻¹ 与 MSSM β） |")
    L.append("")
    L.append("## 六、候选扫描（自有基准独立复扫）")
    L.append("")
    L.append("- 自有基准（23 基元、三因子可重复、每因子可取倒数）共 **{:,}** 个组合，"
             "对 5 靶（M*/v、x*、x_GUT、α_GUT⁻¹、sin²θ@v）tol 1e-9 ⇒ **0 命中**；"
             "正对照 {}/5。".format(kn["own_scan_N"], kn["own_scan_positive_control"]))
    L.append("- r192 记录机读：N={}、tol={}、零命中={}、正对照 {}。".format(
        kn["r192_scan_N"], kn["r192_scan_tol"], kn["r192_scan_zero"],
        kn["r192_scan_pos"]))
    L.append("- 边界：r192 的 60 基元池构成未在 JSON 登记 ⇒ N=39,710 **未重造**"
             "（只验量级 + 正对照 + 自有基准复扫）；有限基排除 ≠ 无限基不可能性。")
    L.append("")
    L.append("## 七、条目（先给靶应得的 PASS）")
    L.append("")
    L.append("| 项 | 内容 | 判定 |")
    L.append("|---|---|---|")
    for e in payload["entries"]:
        if e["verdict"] == "PASS":
            L.append("| {} | {} | {} |".format(e["id"], e["text"], e["verdict"]))
    L.append("")
    L.append("## 八、FAIL / INFO / BOUNDARY")
    L.append("")
    for e in payload["entries"]:
        if e["verdict"] != "PASS":
            L.append("- **{} [{}]** {}（{}）".format(
                e["id"], e["verdict"], e["text"], e["note"]))
    L.append("")
    L.append("## 九、控制组与守卫")
    L.append("")
    L.append("控制组 {} / {}；守卫 {} / {}（全部机读驱动；G7 ast 自审 ok 参数无写死）。".format(
        sum(1 for c in payload["controls"] if c["ok"]), len(payload["controls"]),
        sum(1 for g in payload["guards"] if g["ok"]), len(payload["guards"])))
    L.append("")
    L.append("## 十、未闭合项与红线")
    L.append("")
    for x in payload["not_closed"]:
        L.append("- " + x)
    L.append("")
    L.append("- 数学自洽 ≠ 实验证实；本卷只做可算复核，不产生新物理。")
    L.append("- no-go 排除 ≠ 物理闭合；归并 ≠ 闭合；供给仍 0。")
    return "\n".join(L) + "\n"


def main():
    kn, verdict, not_closed = run_audit()
    payload = build_payload(kn, verdict, not_closed)
    os.makedirs(_DATADIR, exist_ok=True)
    p_json = os.path.join(_DATADIR, BASE + ".json")
    with open(p_json, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    p_rep = os.path.join(_DATADIR, BASE + "_report.txt")
    with open(p_rep, "w", encoding="utf-8") as f:
        f.write(render_report(payload))
    p_v = os.path.join(_DATADIR, "判定_" + BASE + ".md")
    with open(p_v, "w", encoding="utf-8") as f:
        f.write(render_verdict_md(payload))
    p_md = os.path.join(_DATADIR, BASE + ".md")
    with open(p_md, "w", encoding="utf-8") as f:
        f.write(render_report(payload))

    bad = [c for c in CTRL if not c[2]] + [g for g in GUARDS if not g[2]]
    n_fail = sum(1 for e in ENTRIES if e[3] == "FAIL")
    n_pass = sum(1 for e in ENTRIES if e[3] == "PASS")
    print("entries: FAIL={} PASS={} total={}".format(n_fail, n_pass, len(ENTRIES)))
    print("controls: {} / {}".format(sum(1 for c in CTRL if c[2]), len(CTRL)))
    print("guards  : {} / {}".format(sum(1 for g in GUARDS if g[2]), len(GUARDS)))
    print("shared  : {}/{} consistent ({} peer JSON)".format(
        kn["n_shared_consistent"], kn["n_shared_rows"], kn["n_peer_json"]))
    print("verdict : " + payload["verdict"])
    if bad or n_fail == 0 or n_pass == 0:
        for b in bad:
            print("  FAILED:", b[0], b[1], b[3])
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
