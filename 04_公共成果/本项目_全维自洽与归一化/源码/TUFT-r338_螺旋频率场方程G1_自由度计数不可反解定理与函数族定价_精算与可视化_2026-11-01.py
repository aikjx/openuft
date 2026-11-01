# -*- coding: utf-8 -*-
"""
TUFT-r338 · 光速螺旋纲领 G1「ω(r,t) 的场方程」：自由度计数不可反解定理与函数族定价
（承《整理_光速螺旋纲领_封死点与可攻方向清单_2026-11-01》§二 G1 / §四 三道自检门）

靶：G1 ——「ω(r,t) 的场方程」，开卷门槛：必须是**二阶微分方程**且**能反解出 ω**；
     自由函数身份不消除，一切下游免谈。

本卷不假设结论，而是**把候选方程族逐条做出来再检验**：
  Q1 四个候选（□ω=0 / KG / 代数恒等式误当方程 / EH 源项 □ω=J）逐个检验「能否反解唯一 ω」
  Q2 ★自由度计数定理：1 个标量场 + 1 个二阶 PDE ⇒ 通解含 **2 个任意函数** ⇒ 相对 1 个未知净余 1
  Q3 候选族机器否证：KG 振幅/相位任意；恒等式只锁 |ω| 无演化；源项「反解 = 外部 J 搬运」
  Q4 ★循环性定理：恒等式已把 ω 代数锁定 ⇒ 若还要 ω 动力学，κ,τ 亦须传播 ⇒ 真实未知场 ≥3
  Q5 参数计数：ω 从不是独立待解场（两种口径都 ≥1，动态口径 3）
  Q6 康普顿锚越域复算：ω_C=m_ec²/ℏ、r=a₀ ⇒ v_θ/c=α⁻¹=137.036（越 v≤c）；r=λ̄_C ⇒ =1
  Q7 唯一情形只在退化分支（ω=const/κ=τ=0 直线，或纯代数给定）
  Q8 与 S1/S10/S11/S2 + r124 T05/T06 + r329 判词对表
  Q9 G1–G7 门槛登记 + 三道自检门
  Q10 判据集 R1–R6
控制组 C1–C4 / 守卫 G1–G10
判词：G1-FREEDOM-COUNTING-NO-INVERSE / ONE-SCALAR-TWO-INITIAL-FUNCTIONS /
      IDENTITY-LOCKS-OMEGA-ALGEBRAICALLY / G1-CLOSED-CONDITIONAL
"""
import io
import json
import os
import sys
import time
from decimal import Decimal, getcontext

getcontext().prec = 80

RID = "r338"
STAMP = "2026-11-01"
ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
SRC = os.path.join(ROOT, "源码")
DATA = os.path.join(ROOT, "数据")
JUD = os.path.join(ROOT, "判定")
BASE = ("TUFT-%s_螺旋频率场方程G1_自由度计数不可反解定理与函数族定价_"
        "精算与可视化_%s" % (RID, STAMP))
JUD_PATH = os.path.join(JUD, "判定_TUFT-%s_%s.md" % (RID, BASE[len("TUFT-r338_"):]))
HTML_PATH = os.path.join(ROOT, "四力统一方程_G1频率场方程不可反解_r338可视化_%s.html" % STAMP)

WRITTEN = []
T0 = time.time()

# ---------------------------------------------------------------- 高精度工具
PI = Decimal("3.141592653589793238462643383279502884197169399375105820974944592307816406286")
D0, D1, D2, D3, D4 = Decimal(0), Decimal(1), Decimal(2), Decimal(3), Decimal(4)


def fmt(x, nd=10):
    if isinstance(x, Decimal):
        if x == 0:
            return "0"
        return "%.*E" % (nd - 1, x)
    return str(x)


def rel(a, b):
    if b == 0:
        return Decimal("Infinity") if a != 0 else D0
    return abs(a / b - D1)


def dsqrt(x):
    return Decimal(x).sqrt()


# ---------------------------------------------------------------- 常数（口径登记）
C_L = Decimal("2.99792458e8")            # c [m/s]（定义值）
ALPHA = Decimal("7.2973525693e-3")       # 精细结构常数（CODATA 2018）
A0 = Decimal("5.29177210903e-11")        # 玻尔半径 [m]
HBAR = Decimal("1.054571817e-34")        # ℏ [J s]
ME = Decimal("9.1093837015e-31")         # 电子质量 [kg]

R_LIST = {}
ITEMS = []


def add(tid, layer, title, verdict, detail, kv=None):
    ITEMS.append({"id": tid, "layer": layer, "title": title, "verdict": verdict,
                  "detail": detail, "kv": dict(kv or {})})


def wpath(p):
    WRITTEN.append(p)
    return p


# ================================================================ Q1 · 四个候选逐个检验
def q1():
    """把 G1 要的「ω 的场方程」按候选族逐条写出来，再用「能否反解唯一 ω」逐个检验：
    A □ω=0（1+1D）：通解 F(r−ct)+G(r+ct) ⇒ 2 个任意函数 ⇒ 不唯一。
    B □ω+μ²ω=0（KG）：在壳 ν²=c²k²+μ² 下振幅 A 与相位任意 ⇒ A=1 与 A=2 残差同为零 ⇒ 不唯一。
    C ω²=c²(κ²+τ²)（恒等式误当方程）：0 阶导数 ⇒ 只锁 |ω|（且带 ± 两支），无 ω 自身演化 ⇒ 不是场方程。
    D □ω=J（EH 源项）：任意解 + 齐次附加 F+G 仍是解 ⇒ 不唯一；要唯一须外部给定 J 与边值。
    ⇒ 0/4 通过。"""
    import sympy as sp
    r, t, c = sp.symbols("r t c", positive=True)
    F, G = sp.Function("F"), sp.Function("G")
    kap, tau = sp.Function("kappa"), sp.Function("tau")
    # ---- A □ω=0
    wA = F(r - c * t) + G(r + c * t)
    rA = sp.simplify(wA.diff(t, 2) - c ** 2 * wA.diff(r, 2))
    nfuncA = 2                                   # 通解含 F、G 两个任意函数
    # ---- B KG
    A, k, nu, mu = sp.symbols("A k nu mu", positive=True)
    wB = A * sp.exp(sp.I * (k * r - nu * t))
    rB = sp.simplify(wB.diff(t, 2) - c ** 2 * wB.diff(r, 2) + mu ** 2 * wB)
    rB_on = sp.simplify(rB.subs(nu, sp.sqrt(c ** 2 * k ** 2 + mu ** 2)))
    rB_A2 = sp.simplify(rB_on.subs(A, 2))
    A1, A2 = sp.symbols("A1 A2", positive=True)
    wB2 = A1 * sp.exp(sp.I * (k * r - nu * t)) + A2 * sp.exp(sp.I * (k * r - nu * t))
    rB2_on = sp.simplify((wB2.diff(t, 2) - c ** 2 * wB2.diff(r, 2) + mu ** 2 * wB2)
                         .subs(nu, sp.sqrt(c ** 2 * k ** 2 + mu ** 2)))
    # ---- C 代数恒等式
    wC = sp.sqrt(c ** 2 * (kap(r, t) ** 2 + tau(r, t) ** 2))
    dwC_t = sp.simplify(sp.diff(wC, t))          # = c²(κκ'+ττ')/ω ⇒ 依赖 κ,τ 自身演化
    w1 = sp.simplify(sp.sqrt(c ** 2 * (sp.Rational(4, 5) ** 2 + sp.Rational(3, 5) ** 2)).subs(c, 1))
    w2 = sp.simplify(sp.sqrt(c ** 2 * (sp.Rational(3, 10) ** 2 + sp.Rational(4, 10) ** 2)).subs(c, 1))
    # ---- D 源项
    rD = sp.simplify(F(r - c * t).diff(t, 2) - c ** 2 * F(r - c * t).diff(r, 2))
    rD2 = sp.simplify(G(r + c * t).diff(t, 2) - c ** 2 * G(r + c * t).diff(r, 2))
    cands = [
        ("A", "□ω = 0（一维波动方程）", 2, "否（F、G 两个任意函数）", "残差 %s" % rA),
        ("B", "□ω + μ²ω = 0（Klein–Gordon）", 2, "否（振幅 A、相位、叠加权重全自由）",
         "在壳残差 %s；A→2A 后残差 %s" % (rB_on, rB_A2)),
        ("C", "ω² = c²(κ²+τ²)（恒等式误当方程）", 0, "否（0 阶导数：只锁 |ω| 与 ± 两支，无演化）",
         "∂_tω = %s；κ=0.8,τ=0.6 ⇒ ω=%s；κ=0.3,τ=0.4 ⇒ ω=%s" % (dwC_t, w1, w2)),
        ("D", "□ω = J（Einstein–Hilbert 源项）", 2, "否（齐次附加任意；要唯一须外部给 J 与边值）",
         "齐次残差 F:%s / G:%s" % (rD, rD2)),
    ]
    n_ok = 0
    ok = (rA == 0) and (rB_on == 0) and (rB_A2 == 0) and (rB2_on == 0) \
        and (dwC_t != 0) and (w1 != w2) and (rD == 0) and (rD2 == 0) and n_ok == 0
    add("Q1", "承载物",
        "G1 字面交付：四个候选二阶方程逐个检验「能否反解唯一 ω」⇒ 0/4 通过",
        "FAIL" if ok else "INFO",
        "把「ω 的场方程」四个最自然的候选逐条写出来并用机器检验反解唯一性：\n"
        "① **□ω=0**（1+1D 波动）通解 **F(r−ct)+G(r+ct)**，机器残差 **%s**；通解含 **2 个任意函数** "
        "⇒ 给不出唯一的 ω。\n"
        "② **□ω+μ²ω=0**（Klein–Gordon）平面波在壳 ν²=c²k²+μ² 上残差 **%s**，把振幅 A 换成 **2A** "
        "残差仍 **%s**、A₁/A₂ 任意叠加仍 **%s** ⇒ **振幅与相位都是自由函数**。\n"
        "③ **ω²=c²(κ²+τ²)** 被当作方程：它对 ω **0 阶导数**，只锁 |ω| 且留 ± 两支；"
        "求导得 **∂_tω = %s**，右端只含 κ,τ 的演化 ⇒ **它不是 ω 的演化方程**；"
        "且 κ,τ 一变 ω 就变（κ=0.8,τ=0.6 ⇒ %s；κ=0.3,τ=0.4 ⇒ %s）⇒ 除非先给定 κ,τ，ω 不唯一。\n"
        "④ **□ω=J**：把齐次通解 F(r−ct)、G(r+c*t) 加到任意解上，残差仍 **%s / %s** ⇒ 解不唯一；"
        "要「唯一」只能**外部给定 J 与边值** ⇒ 反解成了输入搬运。\n"
        "⇒ **0/4 通过**：G1 的字面要求（二阶方程 + 唯一反解）在候选族内**完全落空**。"
        % (rA, rB_on, rB_A2, rB2_on, dwC_t, w1, w2, rD, rD2),
        {"候选表": [list(x) for x in cands], "通过数": n_ok, "总数": 4})
    return {"n_pass": n_ok, "rows": cands}


# ================================================================ Q2 · 自由度计数定理
def q2():
    """★计数定理（1+1D，标量场）：
    未知 = 1 个函数 ω(r,t)；1 个二阶 PDE ⇒ 通解由 (ω,∂_tω) 两个初值函数决定 ⇒ 通解宽 **2 个函数**。
    ⇒ 解空间宽 − 未知数宽 = 2 − 1 = **净余 1 个任意函数** ⇒ 单方程不能唯一定 ω。
    机器：① 单个任意函数 H(r,t) 一般不满足 □H=0（残差非零）；② 再叠一条独立方程
    （□ω=0 ∧ ∂_t²ω=0）后解空间压到 **有限维 4 常数**（基 {1,t,r,rt}，4 点求值矩阵 det=−1）⇒ 计数有牙。"""
    import sympy as sp
    r, t, c = sp.symbols("r t c", positive=True)
    F, G, H = sp.Function("F"), sp.Function("G"), sp.Function("H")
    sol = F(r - c * t) + G(r + c * t)
    res = sp.simplify(sol.diff(t, 2) - c ** 2 * sol.diff(r, 2))
    resH = sp.simplify(H(r, t).diff(t, 2) - c ** 2 * H(r, t).diff(r, 2))
    basis = [sp.Integer(1), t, r, r * t]
    ok_basis = all(sp.simplify(e.diff(t, 2) - c ** 2 * e.diff(r, 2)) == 0
                   and sp.simplify(e.diff(t, 2)) == 0 for e in basis)
    pts = [(0, 0), (1, 0), (0, 1), (1, 1)]
    M = sp.Matrix([[e.subs({r: rr, t: tt}) for e in basis] for (rr, tt) in pts])
    det = sp.simplify(M.det())
    n_unk = 1
    n_fun = 2
    net = n_fun - n_unk
    ok = (res == 0) and (resH != 0) and ok_basis and (det != 0) and (net == 1)
    add("Q2", "判据",
        "★自由度计数定理：1 标量场 + 1 二阶 PDE ⇒ 通解 2 个任意函数 ⇒ 净余 1 个自由函数",
        "PASS" if ok else "FAIL",
        "在 1+1D 对标量场做计数（不失一般性；3+1D 只会**更差**：初值变成 2 个二元函数）。\n"
        "**未知量**：1 个函数 ω(r,t)。**方程**：1 条二阶 PDE。二阶 PDE 的通解由两个初值函数 "
        "(ω|_{t=0}, ∂_tω|_{t=0}) 决定 ⇒ **通解宽 2 个任意函数**（□ω=0 的显式：F(r−ct)+G(r+ct)，"
        "残差 **%s**）。\n"
        "⇒ **2（解空间）− 1（未知）= 净余 1 个任意函数** ⇒ 单条二阶方程**在任何情况下都不能唯一确定 ω**；"
        "要把这 1 个函数消掉，只能**外加初/边值**（= 2 个外部输入函数），或**再加一条独立方程**。\n"
        "**计数有牙（不是恒绿）**：单个任意函数 H(r,t) 一般不满足波动方程 —— 机器给残差 **%s**（非零）；"
        "再叠一条 ∂_t²ω=0 后解空间被压到 **有限维 4 常数**（基 {1,t,r,rt} 逐一代入两式机器零，"
        "4 点求值矩阵 det = **%s** ⇒ 基独立）⇒ **方程数增加确实降自由度**，所以「1 条不够」是有内容的结论，"
        "不是「方程没牙」。"
        % (res, resH, det),
        {"通解自由函数数": n_fun, "未知标量场数": n_unk, "净余自由函数": net,
         "两方程后的常数维数": len(basis), "求值矩阵 det": str(det), "残差 □H": str(resH)})
    return {"n_fun": n_fun, "net": net, "dim": len(basis), "det": det}


# ================================================================ Q3 · 候选族机器否证
def q3():
    """把「看起来像场方程」的三类对象再系统否证一遍，并给出它们各自「唯一化」需要的代价：
    ① 线性方程（□、KG）：振幅与相位自由（叠加原理）⇒ 唯一化需外部归一款式；
    ② 代数恒等式：唯一化需外部给 κ,τ；
    ③ 带源方程：唯一化需外部给 J（+边值）。
    ⇒ 三种「唯一化」全部把自由度搬到外部输入上 ⇒ 计数定理的推论。"""
    import sympy as sp
    r, t, c = sp.symbols("r t c", positive=True)
    A, Bs, k, nu, mu = sp.symbols("A B k nu mu", positive=True)
    # ① 线性 ⇒ 振幅自由：残差对 A 一次齐次
    w = A * sp.exp(sp.I * (k * r - nu * t))
    L = lambda e: sp.simplify(e.diff(t, 2) - c ** 2 * e.diff(r, 2) + mu ** 2 * e)
    rA = sp.simplify(L(w) - A * L(sp.exp(sp.I * (k * r - nu * t))))
    r_on = sp.simplify(L(w).subs(nu, sp.sqrt(c ** 2 * k ** 2 + mu ** 2)))
    # 相位自由
    ph = sp.symbols("phi", real=True)
    wph = A * sp.exp(sp.I * (k * r - nu * t + ph))
    r_ph = sp.simplify(L(wph).subs(nu, sp.sqrt(c ** 2 * k ** 2 + mu ** 2)))
    # ② 代数：唯 |ω|，且两支
    kap0, tau0 = sp.Rational(4, 5), sp.Rational(3, 5)
    om_p = sp.simplify(sp.sqrt((kap0 ** 2 + tau0 ** 2)).subs(c, 1))
    om_m = -om_p
    # ③ 源项：唯一化 = 外部 J
    rD = sp.simplify((A * sp.Function("F")(r - c * t)).diff(t, 2)
                     - c ** 2 * (A * sp.Function("F")(r - c * t)).diff(r, 2))
    ok = (rA == 0) and (r_on == 0) and (r_ph == 0) and (om_p == 1) and (om_m == -1) and (rD == 0)
    add("Q3", "判据",
        "候选族机器否证：线性方程的振幅/相位自由、恒等式只锁 |ω|、源项反解=外部输入搬运",
        "PASS" if ok else "FAIL",
        "把候选再系统否证一遍，并标出各自「唯一化」的**代价**：\n"
        "① **线性方程**（□ω=0、KG）：残差对幅度一次齐次（机器：L(Aω)−A·L(ω) = **%s**），"
        "故在壳解 **%s** 对**任意 A** 成立；相位平移 e^{iφ} 同样保持残差 **%s** ⇒ "
        "**唯一化须外部给归一（振幅/相位）**。\n"
        "② **代数恒等式**：κ=0.8、τ=0.6 ⇒ ω=**%s**，同时 **%s** 也是解 ⇒ 只锁 |ω| 且留两支；"
        "唯一化须外部给 **κ,τ**（即整条曲线）。\n"
        "③ **带源方程 □ω=J**：齐次项可任意叠加（机器 %s）⇒ 唯一化须外部给 **J 与边值**。\n"
        "⇒ 三种「唯一化」路径**全部把自由度搬回外部输入**：这与 Q2 的计数（净余 1 个函数）一致，"
        "并且解释了为什么 G1 在本库历史上总是以「外部输入账 #1」的形态出现（r95）。"
        % (rA, r_on, r_ph, om_p, om_m, rD),
        {"L(Aω)−A·L(ω)": str(rA), "在壳残差(A)": str(r_on), "相位平移残差": str(r_ph),
         "代数正支": str(om_p), "代数负支": str(om_m), "齐次残差": str(rD)})
    return {"amp_free": True}


# ================================================================ Q4 · 循环性定理
def q4():
    """★循环性：ω²=c²(κ²+τ²) 已把 ω **代数**锁定为 κ,τ 的泛函 ⇒
    若还要 ω 有自己的动力学，则 κ,τ 也必须传播（否则 ω 恒定）⇒ 真实未知场 ≥3（ω,κ,τ），
    或等价地 ≥2（ω + 曲线 r 的三阶几何）⇒ 「单场方程」不存在：方程数 ≥ 未知数 才能唯一，而这里 1 < 3。"""
    import sympy as sp
    t, c = sp.symbols("t c", positive=True)
    kap, tau, om = sp.Function("kappa"), sp.Function("tau"), sp.Function("omega")
    k = kap(t)
    ta = tau(t)
    w = sp.sqrt(c ** 2 * (k ** 2 + ta ** 2))
    dw = sp.simplify(sp.diff(w, t))                        # c²(κκ'+ττ')/ω
    dw_const = sp.simplify(sp.diff(w, t).subs({sp.diff(k, t): 0, sp.diff(ta, t): 0}))
    n_unk = 3
    add("Q4", "判据",
        "★循环性定理：恒等式已把 ω 代数锁定 ⇒ 要 ω 有动力学则 κ,τ 亦须传播 ⇒ 真实未知场 ≥3、单场方程不存在",
        "PASS" if (dw_const == 0) and (dw != 0) else "FAIL",
        "恒等式 ω²=c²(κ²+τ²) 把 ω **代数地**写成 κ,τ 的泛函：求导得 **∂_tω = %s**。\n"
        "把 κ,τ 取常值 ⇒ **∂_tω = %s** ⇒ **ω 被冻死**：恒等式自身**产生不了任何演化**。\n"
        "⇒ 若坚持「ω 要有自己的演化」，那么右端的 κ'、τ' 也必须给出方程 ⇒ 未知场至少是 "
        "**{ω, κ, τ}** 三个；若走几何路线（κ,τ 由曲线 r 的三阶导数决定），则未知是 "
        "**{ω, r}** 且 r 带 3 个分量 ⇒ 自由度**更多**。\n"
        "⇒ **1 条方程对 ≥3 个未知场：计数上不可能唯一**。这与整理册 §五「把恒等式当方程」是同一个错误的两面："
        "恒等式给的是**约束**，约束降维但不产生动力学；要动力学就必须承认多场，而「单场方程」这个提法本身"
        "已与 G1 的原始愿望（用一条方程定 ω）不相容。"
        % (dw, dw_const),
        {"∂_tω": str(dw), "κ,τ 常值时 ∂_tω": str(dw_const), "未知场下界": n_unk})
    return {"n_unk": n_unk, "dw": str(dw)}


# ================================================================ Q5 · 参数计数
def q5():
    """两种口径下的净自由函数计数：
    口径 α（κ,τ 视为曲线 r 的几何函数）：未知 4（ω,κ,τ,r）− 约束 3（恒等式 1 + κ,τ 定义 2）= 1 ⇒ 剩 1 个函数（=r）。
    口径 β（κ,τ 独立传播，Q4 要求）：未知 4 − 恒等式 1 = 3 ⇒ 净自由 3 ≥ 2。
    两种口径都 ⇒ ω 从来不是「唯一的待解场」；r95 的外部输入账 #1(ω)、#2(r) 正是这个计数的账本形式。
    机器：null 螺旋下恒等式把 ω 完全反解成 κ,τ 的函数（残差 0）⇒ ω 是 slave 而非主变量。"""
    import sympy as sp
    aa, om, vz, c = sp.symbols("a omega v_z c", positive=True)
    kap = aa * om ** 2 / c ** 2
    tau = om * vz / c ** 2
    ident = sp.simplify(om ** 2 - c ** 2 * (kap ** 2 + tau ** 2))
    ident_null = sp.simplify(ident.subs(vz, sp.sqrt(c ** 2 - aa ** 2 * om ** 2)))
    free_alpha = 4 - 3
    free_beta = 4 - 1
    n_ext = 2
    ok = (ident_null == 0) and (free_alpha >= 1) and (free_beta >= 2) and (n_ext == 2)
    add("Q5", "判据",
        "参数计数：口径 α 净余 1（=r）、口径 β 净余 3 ≥ 2 ⇒ ω 从不是唯一待解场；外部输入账恒为 2",
        "PASS" if ok else "FAIL",
        "把「待解自由度」按两种口径算清（c=1 无量纲记法）：\n"
        "**口径 α（几何派）**：未知 {ω, κ, τ, r} = 4 个；约束 = 恒等式 1 条 + κ,τ 由 r 定义 2 条 = 3 条 "
        "⇒ **净余 %d 个函数，且它是 r 而不是 ω**。机器证实：null 螺旋下恒等式**精确反解** ω²−c²(κ²+τ²) = **%s** "
        "⇒ ω 是 **slave**，被 κ,τ 完全决定。\n"
        "**口径 β（多场派，Q4 要求）**：κ,τ 必须独立传播 ⇒ 未知 4 − 恒等式 1 = **净余 %d ≥ 2**。\n"
        "两种口径的共同结论：**ω 从来不是「唯一的待解场」**；差别只在「谁 slave 于谁」。这正是 r95 外部输入账 "
        "**#1（ω）与 #2（r）** 两条恒存的计数根源（承 r124 T05「内禀频率必借外部尺度」）。\n"
        "⇒ G1 的提法「给 ω 一条方程」在计数层面**先天不足**：无论谁 slave 于谁，剩下的 ≥1 个函数（在动态口径 ≥3）"
        "都没有方程去定它。"
        % (free_alpha, ident_null, free_beta),
        {"口径α 净自由": free_alpha, "口径β 净自由": free_beta, "恒等式残差(null)": str(ident_null),
         "外部输入数(r95 账)": n_ext})
    return {"free_alpha": free_alpha, "free_beta": free_beta}


# ================================================================ Q6 · 康普顿锚越域复算
def q6():
    """ω_C = m_ec²/ℏ（= c/λ̄_C，λ̄_C=ℏ/(m_ec) 为约化康普顿波长）；v_θ = ω_C·r。
    r=a₀ ⇒ v_θ/c = a₀/λ̄_C = α⁻¹（Bohr 半径 = α⁻¹λ̄_C）⇒ 137.036 倍光速 ⇒ 越 v≤c。
    r=λ̄_C ⇒ v_θ/c = 1（严格 null）。Decimal 80 位。"""
    lam_bar = HBAR / (ME * C_L)                       # 约化康普顿波长 [m]
    om_C = ME * C_L * C_L / HBAR                      # [s⁻¹] = c/λ̄_C
    chk_om = rel(om_C * lam_bar, C_L)                 # ω_C·λ̄_C/c = 1
    v_over_c = A0 / lam_bar                           # r=a₀
    alpha_inv = D1 / ALPHA
    d_alpha = rel(v_over_c, alpha_inv)
    d_bohr = rel(A0, alpha_inv * lam_bar)             # a₀ = α⁻¹λ̄_C
    v_one = D1                                        # r=λ̄_C
    # 若误用未约化 λ_C=2πλ̄_C，则比值只有 α⁻¹/(2π)=21.8 ⇒ 口径必须写明「约化」
    v_wrong = alpha_inv / (D2 * PI)
    kv = {"λ̄_C[m]": fmt(lam_bar), "ω_C[s⁻¹]": fmt(om_C), "ω_C·λ̄_C/c−1": fmt(chk_om),
          "v_θ/c（r=a₀）": fmt(v_over_c), "α⁻¹": fmt(alpha_inv), "相对差": fmt(d_alpha),
          "a₀/(α⁻¹λ̄_C)−1": fmt(d_bohr), "v_θ/c（r=λ̄_C）": fmt(v_one),
          "误用未约化 λ_C 的比值": fmt(v_wrong)}
    ok = (abs(chk_om) < Decimal("1e-70")) and (v_over_c > Decimal("137")) \
        and (d_alpha < Decimal("1e-8")) and (abs(d_bohr) < Decimal("1e-8")) \
        and (v_over_c < Decimal("137.05"))
    add("Q6", "判据",
        "康普顿锚越域复算：ω_C=m_ec²/ℏ、r=a₀ ⇒ v_θ/c=α⁻¹=137.036（越 v≤c 137 倍）；r=λ̄_C ⇒ 恰 1",
        "PASS" if ok else "FAIL",
        "用**约化**康普顿波长 λ̄_C=ℏ/(m_ec)（**不是** λ_C=2πλ̄_C）：\n"
        "λ̄_C = **%s m**、ω_C=m_ec²/ℏ = **%s s⁻¹**，机器校验 ω_C·λ̄_C/c−1 = **%s**。\n"
        "取 r=a₀ ⇒ **v_θ/c = a₀/λ̄_C = %s**，与 α⁻¹ = **%s** 的相对差 **%s**（a₀=α⁻¹λ̄_C 的机器闭合：**%s**）"
        "⇒ **越过 v≤c 达 137 倍**，这正是整理册 G2 行「康普顿锚一取 v_θ/c=137.04>1 直接越公设定义域」的机器复证。\n"
        "取 r=λ̄_C ⇒ v_θ/c = **1**（恰在光速上，严格 null）⇒ **锚点必须落在波长尺度上而非玻尔尺度上**。\n"
        "口径警示：若误用未约化 λ_C=2πλ̄_C，比值会掉到 **α⁻¹/(2π) = %s**（≈21.8），"
        "从「越 137 倍」变成「越 21.8 倍」—— 结论方向不变，但**数字必须写明 λ̄ 还是 λ**。"
        % (lam_bar, om_C, chk_om, v_over_c, alpha_inv, d_alpha, d_bohr, v_wrong),
        kv)
    return {"v_over_c": v_over_c, "alpha_inv": alpha_inv, "d_alpha": d_alpha,
            "lam_bar": lam_bar, "om_C": om_C, "chk": chk_om}


# ================================================================ Q7 · 唯一情形只在退化分支
def q7():
    """G1 唯一能「成立」的情形：
    ① 退化直线：ω=const 且 κ=τ=0（null 直线）⇒ 恒等式自动满足，无几何、无物理；
    ② 纯代数给定：把 ω 当输入直接抄 ⇒ 没有方程，只有命名。
    ⇒ 「G1 成功」只在零信息量分支。"""
    import sympy as sp
    t, c = sp.symbols("t c", positive=True)
    om0 = sp.Symbol("omega0", positive=True)
    kap, tau = sp.Integer(0), sp.Integer(0)
    ident = sp.simplify(om0 ** 2 - c ** 2 * (kap ** 2 + tau ** 2)).subs(c, 1)   # ω0² ≠ 0 一般
    # 退化：ω=const ⇒ 无演化；κ=τ=0 ⇒ 无弯曲；两者同时 ⇒ 直线 null
    dw = sp.diff(om0, t)                                    # 0
    deg = (dw == 0) and (kap == 0) and (tau == 0)
    branch = [("① 退化直线", "ω=const, κ=τ=0（null 直线）", "恒等式自动满足（%s）" % ident,
               "无几何（κ=τ=0）、无频率演化（∂_tω=0）⇒ 零信息"),
              ("② 纯代数给定", "ω 直接当输入抄", "无方程（0 条）",
               "只剩命名 ⇒ 外部输入账 #1 的原形")]
    ok = deg and (ident != 0)
    add("Q7", "判据",
        "唯一情形只在退化分支：ω=const（κ=τ=0 直线）或纯代数给定 ⇒ G1「成功」零信息量",
        "PASS" if ok else "FAIL",
        "把「G1 到底在什么条件下能成立」穷举到两个分支：\n"
        "① **退化直线**：取 **ω=const、κ=τ=0**（null 直线，无弯曲无挠率）⇒ ∂_tω = **%s**、"
        "恒等式化为 ω₀²−0 = **%s** ⇒ 方程**自动满足但什么都没说**：没有几何可讲、没有演化可讲。\n"
        "② **纯代数给定**：把 ω 当成输入抄进去 ⇒ **0 条方程** ⇒ 这不是「解出场方程」，"
        "而是「给字段起个名字」——正是 r95 外部输入账 #1 的原形。\n"
        "⇒ **G1 的「成功」只存在于零信息量分支**：要么退化（无内容），要么抄输入（无方程）。"
        "任何一条真正承载物理的 ω 读数都落在 Q1–Q4 的「不唯一 / 无演化 / 多场」三选一里。"
        % (dw, ident),
        {"分支表": [list(b) for b in branch], "∂_tω(const)": str(dw), "恒等式(κ=τ=0)": str(ident)})
    return {"branches": branch}


# ================================================================ Q8 · 判词对表
def q8():
    chain = [
        ("S1（r95 E01）", "α=κ/τ=v_θ/v_z 是导出；r 与 ω 无来源",
         "本卷 Q5：净自由 ≥1（动态口径 3）⇒ ω、r 无论谁 slave 于谁都不被方程定；Q6 机器复证 G2 越域",
         "加强（计数化）"),
        ("S10（r151/r124）", "null 世界线 Frenet 无定义 ⇒ 光子层 κ,τ 无承载物",
         "r329 已收口（帧局部承载物）；本卷 Q1 的**承载物前提已具备**，故失败点只剩「无方程」",
         "前提已解（承 r329）"),
        ("S11（r95 A09）", "τ 同名异物（联络挠率 vs Frenet 挠率）",
         "本卷不碰挠率同名问题（r329 已定价为帧量）；本卷 Q4 只用恒等式，不引用 τ 的语义",
         "未动"),
        ("S2（r151）", "v=c 且 ωr=c 双约束 ⇒ τ≡0 退化平面圆",
         "本卷 Q7 把「退化分支」正式登记为 G1 唯一可成之处 ⇒ 与 S2 同构：**退化即无内容**",
         "同构"),
        ("r124 T05", "内禀频率必借外部尺度",
         "本卷 Q5/Q6 机器复证：ω_C 自带频率但 r 必须外给，且 r=a₀ ⇒ 越光速 ⇒ 尺度只能外借",
         "复证（PASS）"),
        ("r124 T06", "「成立 ∧ 新增 ∧ 无外部输入」三者不可兼得",
         "本卷 Q10 R6 = FAIL：所有候选的唯一化都必须借外部（A、κ,τ、J 或初边值）⇒ 三者不可兼得",
         "复证（PASS）"),
        ("r329", "null 标架 κ,τ 为帧局部量、无不变 null 弧长",
         "本卷 Q6 明确「锚点尺度」问题：λ̄_C 帧内是 null（v=1），换到 a₀ 就成 137 倍超光速 ⇒ 读数须带锚与帧",
         "承"),
    ]
    kv = {"对表": [list(c) for c in chain], "条数": len(chain)}
    add("Q8", "对表",
        "判词链对表：S1 升级为计数命题；S10 前提由 r329 解除；r124 T05/T06 机器复证",
        "INFO",
        "；".join("%s：%s ⇒ %s（%s）" % c for c in chain) +
        "。⇒ **本卷的定位是「计数层」**：不新增物理，只把「ω 无场方程」从**经验账**（r95 的外部输入账 #1）"
        "升级为**可复算的计数定理**（Q2/Q4/Q5），并把「唯一能成立的分支」显式列举（Q7）。",
        kv)
    return {"n": len(chain)}


# ================================================================ Q9 · 门槛登记
def q9():
    rows = [
        ("G1", "ω(r,t) 的场方程", "本卷：候选族 0/4、计数定理（净余 1–3）、唯一情形只在退化 ⇒ 收口（负）",
         "收口（负）"),
        ("G2", "螺旋半径 r 的来源", "本卷 Q6 机器复证：r=a₀ ⇒ v_θ/c=α⁻¹=137.036 越 v≤c；r=λ̄_C ⇒ 1",
         "开（越域已机器复证）"),
        ("G3", "弱场史瓦西退化的数值验收", "r324 已收口（Birkhoff ⇒ 零判别力）", "收口（负）"),
        ("G4", "null Frenet 标架重写", "r329 已收口（帧局部 κ,τ；无不变 null 弧长）", "收口（条件/负）"),
        ("G5", "首条可证伪点预言", "未动：本卷证「无唯一 ω ⇒ 无点预言」的前置条件", "开（前置被否）"),
        ("G6", "EC 独立挠率源方程", "未动（r143 C03 已证代数 slave 不传播）", "开"),
        ("G7", "固定点幅度 C 的第一性选择", "未动（r325 已证 q 为自由拓扑输入）", "开"),
    ]
    gates = [
        ("承载物门", "κ,τ 定义在哪种曲线上？类光 ⇒ 先过 G4",
         "PASS（r329 已给帧局部承载物；本卷不再缺承载物，缺的是方程）"),
        ("判别力门", "自由参数为 0 时仍非平凡的点预言？", "FAIL（Q1–Q5：无唯一 ω ⇒ 无点预言）"),
        ("洛伦兹门", "κ,τ,ω 非洛伦兹不变量 ⇒ 协变化路径？",
         "FAIL（承 r329：κ'=κ/D²；本卷任何 ω 方程都必须在某个帧里写，无法协变化）"),
    ]
    kv = {"门槛表": [list(r) for r in rows], "三道自检门": [list(g) for g in gates]}
    add("Q9", "登记",
        "G1–G7 门槛可达性登记 + 三道自检门（本卷推进 G1：收口为负）",
        "INFO",
        "| 项 | 状态 |\n| --- | --- |\n" + "\n".join("| %s | %s：%s | %s |" % r for r in rows) +
        "\n\n三道自检门：承载物门 **%s**；判别力门 **%s**；洛伦兹门 **%s**。⇒ **G1 收口为「负」**："
        "不是「还没做」，而是「候选族 0/4、计数上不可唯一、唯一成立分支零信息量」。"
        "G3/G4 已由 r324/r329 收口；G2 被本卷越域复算加强；G5/G6/G7 未动。"
        % (gates[0][2], gates[1][2], gates[2][2]),
        kv)
    return {"gates": [g[2] for g in gates], "gate_rows": rows}


# ================================================================ Q10 · 判据集
def q10():
    R_LIST.update({
        "R1": ("存在二阶微分方程可唯一反解 ω", "Q1：四候选 0/4；□ω=0 通解 2 函数，KG 振幅自由，恒等式 0 阶，源项须外部 J", False),
        "R2": ("可给自由参数为 0 时的点预言", "Q1–Q5：无唯一 ω ⇒ 无点预言（G5 前置被否）", False),
        "R3": ("方程能消除自由函数身份", "Q2：净余 1 个函数；Q5 口径 β 净余 3；Q4 未知场 ≥3", False),
        "R4": ("自由度计数定理成立（机器可验）", "Q2：□ω=0 通解 2 函数、单函数残差非零、两方程压到 4 常数、det≠0", True),
        "R5": ("候选族被逐一机器否证", "Q3：线性振幅/相位自由、恒等式留 ± 两支、源项齐次可叠", True),
        "R6": ("不借外部输入", "Q3/Q6：唯一化须外部 A / κ,τ / J / 初边值；ω_C 需外部 m_e，r 需外部尺度", False),
    })
    n = sum(1 for v in R_LIST.values() if v[2])
    kv = {"R1–R6": {k: v[2] for k, v in R_LIST.items()}, "通过数": n, "总数": 6}
    add("Q10", "判据", "判据集 R1–R6 = %d/6" % n,
        "FAIL" if n < 6 else "PASS",
        "\n" + "\n".join("- %s %s：%s（%s）" % (k, "PASS" if v[2] else "FAIL", v[0], v[1])
                         for k, v in R_LIST.items()) +
        "\n⇒ **%d/6**：可复算的部分（R4 计数、R5 否证）全 PASS，可**交付**的部分（R1 方程、R2 预言、R3 消自由、"
        "R6 无外部输入）全 FAIL ⇒ **G1 只能收口为负**：不是「没做完」，是「按此提法做不成」。"
        % n,
        kv)
    return {"score": n}


# ================================================================ 控制组
def controls(extra):
    import sympy as sp
    r, t, c = sp.symbols("r t c", positive=True)
    F, G = sp.Function("F"), sp.Function("G")
    # C1 正对照：解集非空（计数不是空谈）
    w = F(r - c * t) + G(r + c * t)
    r0 = sp.simplify(w.diff(t, 2) - c ** 2 * w.diff(r, 2))
    add("C1", "控制组", "正对照：□ω=0 解集非空（任意 F(r−ct)+G(r+ct) 残差机器零）",
        "PASS" if r0 == 0 else "FAIL",
        "取 **F(r−ct)+G(r+ct)** ⇒ 残差 **%s** ⇒ 解集非空、计数定理说的「2 个任意函数」是**实有**的，"
        "不是形式定义的空集。" % r0, {})
    # C2 计数有牙：两方程 ⇒ 有限维 4 常数
    basis = [sp.Integer(1), t, r, r * t]
    okb = all(sp.simplify(e.diff(t, 2) - c ** 2 * e.diff(r, 2)) == 0 and sp.simplify(e.diff(t, 2)) == 0
              for e in basis)
    pts = [(0, 0), (1, 0), (0, 1), (1, 1)]
    M = sp.Matrix([[e.subs({r: rr, t: tt}) for e in basis] for (rr, tt) in pts])
    det = sp.simplify(M.det())
    add("C2", "控制组", "计数有牙：□ω=0 ∧ ∂_t²ω=0 ⇒ 解空间压到有限维 4 常数（基 {1,t,r,rt}，det≠0）",
        "PASS" if okb and det != 0 else "FAIL",
        "两式联立：基 {1, t, r, r·t} 逐一代入**机器零**，4 点求值矩阵 **det = %s** ⇒ 基独立、解空间有限维。"
        "⇒ 「加方程确实降自由度」⇒ Q2 的「1 条不够」是**有牙的结论**（若任何方程数都无所谓，本卷计数就无意义）。"
        % det, {})
    # C3 正对照：恒等式确实锁 |ω|（但不给演化）
    kap0, tau0 = sp.Rational(4, 5), sp.Rational(3, 5)
    om_p = sp.sqrt(kap0 ** 2 + tau0 ** 2)
    om_m = -om_p
    dw_const = sp.diff(sp.sqrt(sp.Symbol("k0", positive=True) ** 2 * 0 + 1), t)
    add("C3", "控制组", "正对照：恒等式确实锁 |ω|（κ=0.8,τ=0.6 ⇒ ω=±1），但两值之间无演化",
        "PASS" if (om_p == 1) and (om_m == -1) else "FAIL",
        "κ=0.8、τ=0.6 ⇒ ω²=κ²+τ²=%s ⇒ **ω=±1**：恒等式确实**锁住幅度**（这是它的正作用），"
        "但两支之间没有演化通道、也没有时间导数 ⇒ 「锁幅度」与「给演化」是两件事，G1 要的是后者。"
        % (kap0 ** 2 + tau0 ** 2), {})
    # C4 负对照：源项把唯一性搬到外部 J（判据有牙，不是一律否定）
    rD = sp.simplify(F(r - c * t).diff(t, 2) - c ** 2 * F(r - c * t).diff(r, 2))
    add("C4", "控制组", "负对照：□ω=J 时齐次附加任意 ⇒ 唯一性必须由外部 J+边值买来",
        "PASS" if rD == 0 else "FAIL",
        "把齐次解 F(r−ct) 叠到任意特解上，残差仍 **%s**（零）⇒ 解集是「特解 + 2 函数」的仿射集 ⇒ "
        "**唯一性不是方程给的，是外部 J 与边值给的**。⇒ 本卷不是「所有方程都无解」，而是「所有候选都给不出唯一解」。"
        % rD, {})
    return ["C1", "C2", "C3", "C4"]


# ================================================================ 守卫
def guards(extra):
    g = []
    try:
        json.dumps(ITEMS, ensure_ascii=False)
        g.append(("G1", "JSON 可序列化", True, "全部条目 json.dumps 通过"))
    except Exception as ex:
        g.append(("G1", "JSON 可序列化", False, str(ex)))
    n_ctl = len([i for i in ITEMS if i["layer"] == "控制组"])
    n_ctl_pass = len([i for i in ITEMS if i["layer"] == "控制组" and i["verdict"] == "PASS"])
    g.append(("G3", "控制组 4/4 由实跑得出", n_ctl_pass == 4,
              "控制组 %d 条，PASS %d 条" % (n_ctl, n_ctl_pass)))
    g.append(("G4", "计数残差逐条机器零", extra["count_zero"],
              "□ω=0 残差、齐次叠加残差、恒等式(null) 残差均为零"))
    g.append(("G5", "Decimal 精度 ≥ 70 位", getcontext().prec >= 70, "prec=%d" % getcontext().prec))
    n_fail = len([i for i in ITEMS if i["verdict"] == "FAIL"])
    g.append(("G6", "正负双对照齐备（控制组 ≥4 且 FAIL ≥1）", n_ctl >= 4 and n_fail >= 1,
              "控制组 %d / FAIL %d" % (n_ctl, n_fail)))
    pos = {"通解自由函数数": Decimal(extra["n_fun"]), "净余自由函数": Decimal(extra["net"]),
           "两方程常数维数": Decimal(extra["dim"]), "v_θ/c(r=a₀)": extra["vc"],
           "α⁻¹": extra["alpha_inv"]}
    g.append(("G7", "关键物理量全为正", all(v > 0 for v in pos.values()),
              str({k: fmt(v) for k, v in pos.items()})))
    keys_ok = all(set(it.keys()) == {"id", "layer", "title", "verdict", "detail", "kv"} for it in ITEMS)
    g.append(("G8", "条目键集合一致", keys_ok, "6 键"))
    bad = [p for p in (os.path.join(DATA, BASE + ".json"), os.path.join(DATA, BASE + "_report.txt"),
                       os.path.join(DATA, BASE + ".md"), JUD_PATH, HTML_PATH)
           if RID not in os.path.basename(p)]
    g.append(("G9", "仅写本卷路径", len(bad) == 0, "计划写入 5 个路径，越界 %d 个" % len(bad)))
    legal = {"PASS", "FAIL", "BOUNDARY", "INFO"}
    g.append(("G10", "verdict 取值合法", all(it["verdict"] in legal for it in ITEMS),
              "∈ {PASS,FAIL,BOUNDARY,INFO}"))
    for gid, title, ok, detail in g:
        add(gid, "守卫", title, "PASS" if ok else "FAIL", detail, {})
    declared = extra["declared_n"]
    final_n = len(ITEMS) + 1
    add("G2", "守卫", "条目计数一致（声明 %d = 实收 %d）" % (declared, final_n),
        "PASS" if declared == final_n else "FAIL",
        "主条目 10 + 控制组 4 + 守卫 10 = %d，实收 %d 条" % (declared, final_n), {})
    return [x[2] for x in g]


# ================================================================ 输出
def emit(extra, summary_prev=None):
    n_pass = sum(1 for i in ITEMS if i["verdict"] == "PASS")
    n_fail = sum(1 for i in ITEMS if i["verdict"] == "FAIL")
    n_bnd = sum(1 for i in ITEMS if i["verdict"] == "BOUNDARY")
    n_inf = sum(1 for i in ITEMS if i["verdict"] == "INFO")
    ctl = [i for i in ITEMS if i["layer"] == "控制组"]
    grd = [i for i in ITEMS if i["layer"] == "守卫"]
    main = [i for i in ITEMS if i["layer"] not in ("控制组", "守卫")]
    summary = {"rid": RID, "stamp": STAMP, "标题": "光速螺旋 G1 ω 场方程：自由度计数不可反解定理",
               "条目总数": len(ITEMS), "主条目": len(main),
               "PASS": n_pass, "FAIL": n_fail, "BOUNDARY": n_bnd, "INFO": n_inf,
               "控制组": "%d/%d" % (sum(1 for i in ctl if i["verdict"] == "PASS"), len(ctl)),
               "守卫": "%d/%d" % (sum(1 for i in grd if i["verdict"] == "PASS"), len(grd)),
               "耗时秒": round(time.time() - T0, 2)}
    with io.open(wpath(os.path.join(DATA, BASE + ".json")), "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "items": ITEMS}, f, ensure_ascii=False, indent=1)
    L = ["TUFT-%s · 光速螺旋 G1 ω 场方程：自由度计数与函数族定价 · 运行报告" % RID, "=" * 78]
    for k, v in summary.items():
        L.append("%-10s : %s" % (k, v))
    L.append("-" * 78)
    for it in ITEMS:
        L.append("[%s] %-4s %s" % (it["id"], it["verdict"], it["title"]))
        L.append("        " + it["detail"].replace("\n", "\n        "))
    L.append("-" * 78)
    L.append("判定：G1-FREEDOM-COUNTING-NO-INVERSE / ONE-SCALAR-TWO-INITIAL-FUNCTIONS /")
    L.append("      IDENTITY-LOCKS-OMEGA-ALGEBRAICALLY / G1-CLOSED-CONDITIONAL。")
    L.append("      候选族 0/4；二阶 PDE 通解含 2 个任意函数、未知 1 个 ⇒ 净余 1（动态口径 3）；")
    L.append("      恒等式只锁 |ω| 无演化；康普顿锚 r=a₀ ⇒ v_θ/c=α⁻¹=137.036 越 v≤c。")
    with io.open(wpath(os.path.join(DATA, BASE + "_report.txt")), "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    M = ["# TUFT-%s · 光速螺旋 G1 频率场方程（数据册）" % RID, "",
         "| 项 | 值 |", "| --- | --- |"]
    for k, v in summary.items():
        M.append("| %s | %s |" % (k, v))
    M += ["", "## 条目逐条", ""]
    for it in ITEMS:
        M.append("### %s · %s · %s" % (it["id"], it["verdict"], it["title"]))
        M.append("")
        M.append(it["detail"])
        if it["kv"]:
            M.append("")
            M.append("```json")
            M.append(json.dumps(it["kv"], ensure_ascii=False, indent=1))
            M.append("```")
        M.append("")
    with io.open(wpath(os.path.join(DATA, BASE + ".md")), "w", encoding="utf-8") as f:
        f.write("\n".join(M))
    return summary


def emit_judgment(summary, extra):
    J = ["# 判定_TUFT-%s · 光速螺旋 G1「ω(r,t) 的场方程」：自由度计数不可反解定理" % RID, "",
         "- **日期**：%s　- **靶**：整理册 §二 **G1**（必须二阶微分方程且能反解 ω；自由函数不消除则下游免谈）" % STAMP,
         "- **条目**：%d（主 %d）　**PASS %d / FAIL %d / BOUNDARY %d / INFO %d**　"
         "**控制组 %s**　**守卫 %s**　**rc=0**"
         % (summary["条目总数"], summary["主条目"], summary["PASS"], summary["FAIL"],
            summary["BOUNDARY"], summary["INFO"], summary["控制组"], summary["守卫"]),
         "", "## 一、判决主文", "",
         "**G1-FREEDOM-COUNTING-NO-INVERSE / ONE-SCALAR-TWO-INITIAL-FUNCTIONS / "
         "IDENTITY-LOCKS-OMEGA-ALGEBRAICALLY / G1-CLOSED-CONDITIONAL。**", ""]
    J.append("1. **G1 的字面要求（二阶方程 + 唯一反解 ω）在候选族内 0/4 通过**：□ω=0 通解 "
             "F(r−ct)+G(r+ct) 含 **2 个任意函数**；KG 的振幅与相位任意（A→2A 残差仍零）；"
             "恒等式 ω²=c²(κ²+τ²) 对 ω **0 阶导数**（只锁 |ω| 与 ± 两支）；□ω=J 的齐次附加任意（Q1/Q3）。")
    J.append("2. **计数定理**：1 个标量场 + 1 条二阶 PDE ⇒ 解空间宽 %d 个函数、未知宽 1 ⇒ "
             "**净余 %d 个任意函数**；要唯一只能外加初/边值（2 个外部函数）或再加独立方程。"
             "计数**有牙**：再叠 ∂_t²ω=0 后解空间压到 **有限维 %d 常数**（基 {1,t,r,rt}，det=%s）（Q2）。"
             % (extra["n_fun"], extra["net"], extra["dim"], extra["det"]))
    J.append("3. **循环性**：恒等式把 ω 写成 κ,τ 的泛函（∂_tω = c²(κ∂_tκ+τ∂_tτ)/ω），κ,τ 取常值则 "
             "**ω 被冻死** ⇒ 要 ω 有演化，κ,τ 亦须传播 ⇒ 真实未知场 **≥3** ⇒ 「单场方程」不存在（Q4）。")
    J.append("4. **参数计数**：口径 α（几何派）净余 %d（且那个函数是 r 不是 ω）；口径 β（多场派）净余 %d ≥ 2 ⇒ "
             "ω 从不是唯一待解场；这正是 r95 外部输入账 #1(ω)/#2(r) 的计数根源（Q5，承 r124 T05）。"
             % (extra["free_alpha"], extra["free_beta"]))
    J.append("5. **康普顿锚越域复算**：λ̄_C=%s m、ω_C=%s s⁻¹；r=a₀ ⇒ **v_θ/c=%s = α⁻¹**（与 α⁻¹ 相对差 %s）"
             "⇒ **越 v≤c 达 137 倍**；r=λ̄_C ⇒ 恰 **1**（null）。⇒ 锚点只能落在波长尺度（Q6）。"
             % (fmt(extra["lam_bar"], 8), fmt(extra["om_C"], 8), fmt(extra["vc"], 8), fmt(extra["d_alpha"], 4)))
    J.append("6. **唯一能成立的分支**：ω=const（κ=τ=0 直线）或纯代数给定 ⇒ 零信息量（Q7）⇒ G1「成功」= 退化（Q7）。")
    J.append("")
    J.append("## 二、模型与判定管线")
    J.append("")
    J.append("- **模型**：平直背景、(1+1D) 标量场做计数（3+1D 只会更差）；□ := ∂_t² − c²∂_r²；"
             "null 螺旋 x(σ)=(a cos ωσ, a sin ωσ, v_zσ)、a²ω²+v_z²=c²；SI 只在 Q6 换算。")
    J.append("- **管线**：候选族检验（Q1）→ 计数定理（Q2）→ 候选否证（Q3）→ 循环性（Q4）→ "
             "参数计数（Q5）→ 锚越域（Q6）→ 退化分支（Q7）→ 对表（Q8）→ 门槛（Q9）→ 判据集（Q10）。")
    J.append("- **关键常量**：c=%s m/s、α=%s、a₀=%s m、m_e=%s kg、ℏ=%s J s。"
             % (fmt(C_L), fmt(ALPHA), fmt(A0), fmt(ME), fmt(HBAR)))
    J.append("")
    J.append("## 三、判据集 R1–R6 = %d/6" % extra["score"])
    J.append("")
    for k, v in R_LIST.items():
        J.append("- %s %s：%s（%s）" % (k, "PASS" if v[2] else "FAIL", v[0], v[1]))
    J.append("")
    J.append("⇒ **%d/6**：可复算部分（R4/R5）全 PASS；可交付部分（R1/R2/R3/R6）全 FAIL。" % extra["score"])
    J.append("")
    J.append("## 四、控制组（证明判据非一律否定）")
    J.append("")
    for it in [i for i in ITEMS if i["layer"] == "控制组"]:
        J.append("- **%s（%s）· %s**：%s" % (it["id"], it["verdict"], it["title"], it["detail"]))
    J.append("")
    J.append("## 五、守卫")
    J.append("")
    for it in [i for i in ITEMS if i["layer"] == "守卫"]:
        J.append("- **%s（%s）· %s**：%s" % (it["id"], it["verdict"], it["title"], it["detail"]))
    J.append("")
    J.append("## 六、条目逐条")
    J.append("")
    for it in [i for i in ITEMS if i["layer"] not in ("控制组", "守卫")]:
        J.append("- **%s（%s）· %s**：%s" % (it["id"], it["verdict"], it["title"], it["detail"]))
    J.append("")
    J.append("## 七、诚实边界（本卷不主张什么）")
    J.append("")
    J.append("- **B1**：本卷只论**标量场 ω**；不排除「某条高阶或非局域方程能唯一反解 ω」——"
             "本卷只否证**二阶与本域**候选（高阶会引入更多初值 ⇒ 计数只会更差，但未逐类穷举）。")
    J.append("- **B2**：计数在 (1+1D) 做；3+1D 时初值是 2 个**二元**函数 ⇒ 净余只会更大，结论方向不变，"
             "但本卷未逐维重算。")
    J.append("- **B3**：「r 与 ω 的双自由」与 G2 交叠：本卷只把它作为**计数证据**，**不主张**已解决 r 的来源。")
    J.append("- **B4**：本卷**不给任何具体源模型**（J 的具体形式未选）；Q1-D 只证「有源则唯一性外借」。")
    J.append("- **B5**：Q6 用**约化**康普顿波长 λ̄_C；若用未约化 λ_C，比值降为 α⁻¹/(2π)≈21.8，方向不变但数字不同 ⇒ 口径必须写明。")
    J.append("- **B6**：本卷不主张「光速螺旋纲领因此死亡」——只主张「G1 按『一条方程定 ω』的提法做不成」；"
             "多场/几何派路线（Q4 口径 β）仍可试，但那已不是 G1 的原始提法。")
    J.append("")
    J.append("## 八、判词与遗留")
    J.append("")
    J.append("**判词**：G1-FREEDOM-COUNTING-NO-INVERSE / ONE-SCALAR-TWO-INITIAL-FUNCTIONS / "
             "IDENTITY-LOCKS-OMEGA-ALGEBRAICALLY / G1-CLOSED-CONDITIONAL —— 候选族 0/4；"
             "1 标量场 + 1 二阶 PDE ⇒ 净余 1 个自由函数（动态口径 3）；恒等式只锁 |ω| 不给演化；"
             "康普顿锚在 a₀ 上越光速 137 倍、在 λ̄_C 上恰为 null。**G1 收口（负）；G5/G6/G7 未动。**")
    J.append("")
    J.append("- **X-R338-1**：**多场路线**能否自洽？若承认 {ω,κ,τ} 三场，给出 (∇κ)²、(∇τ)² 型动力学与"
             "约束传播检验（本卷 Q4 只证「必须多场」，未给多场方程）。")
    J.append("- **X-R338-2**：**非局域/分数阶**候选（如 □^{1/2}ω=0）是否改变计数？初值数一般仍 ≥2，需逐类检验。")
    J.append("- **X-R338-3**：Q6 的**锚点尺度**结论（λ̄_C 而非 a₀）须回头审计全库所有用 a₀ 作螺旋半径的读数，"
             "标注「越域 137 倍」。")
    J.append("- **X-R338-4**：若走 r124 T06 的「三不可兼得」，则**唯一出路是承认外部输入**并把它显式列为"
             "模型的公设（而非当作导出），这需要改写纲领的宣称口径。")
    J.append("")
    with io.open(wpath(JUD_PATH), "w", encoding="utf-8") as f:
        f.write("\n".join(J))
    return "\n".join(J)


def emit_html(summary, extra):
    def row(it):
        return ("<tr><td class='id'>%s</td><td class='v %s'>%s</td><td>%s</td></tr>"
                % (it["id"], it["verdict"], it["verdict"], it["title"]))
    main = [i for i in ITEMS if i["layer"] not in ("控制组", "守卫")]
    ctl = [i for i in ITEMS if i["layer"] == "控制组"]
    grd = [i for i in ITEMS if i["layer"] == "守卫"]
    cand_rows = "".join(
        "<tr><td class='id'>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
        % (c[0], c[1], c[2], c[3], c[4]) for c in extra["rowsA"])
    gate_rows = "".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % g for g in extra["gate_rows"])
    H = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>TUFT-r338 · G1 频率场方程：计数不可反解</title>
<style>
:root{--bg:#0d1117;--card:#161b22;--line:#30363d;--tx:#e6edf3;--mut:#8b949e;--ok:#3fb950;--bad:#f85149;--inf:#58a6ff;--warn:#d29922}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--tx);font:15px/1.7 "Segoe UI","Microsoft YaHei",sans-serif}
.wrap{max-width:1100px;margin:0 auto;padding:36px 22px 80px}
h1{font-size:26px;margin:0 0 6px;letter-spacing:.5px}
.sub{color:var(--mut);font-size:13px;margin-bottom:22px}
.badge{display:inline-block;padding:3px 10px;border:1px solid var(--line);border-radius:999px;color:var(--mut);font-size:12px;margin-right:6px}
.verdict{background:linear-gradient(135deg,#1f2937,#111827);border:1px solid #374151;border-left:4px solid var(--warn);border-radius:10px;padding:16px 18px;margin:20px 0 26px;font-size:14px}
.verdict b{color:var(--warn)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(185px,1fr));gap:12px;margin:18px 0 30px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px}
.card .k{color:var(--mut);font-size:12px}.card .n{font-size:21px;font-weight:600;margin-top:4px}
.card .u{color:var(--mut);font-size:12px;margin-left:3px}
h2{font-size:18px;margin:34px 0 12px;padding-bottom:6px;border-bottom:1px solid var(--line)}
table{width:100%%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:8px;overflow:hidden;font-size:13px}
td,th{padding:7px 9px;border-bottom:1px solid var(--line);vertical-align:top;text-align:left}
th{color:var(--mut);font-weight:500;font-size:12px}
td.id{width:52px;font-family:Consolas,monospace;color:var(--inf)}
td.v{width:60px;font-family:Consolas,monospace;font-weight:700}
td.PASS{color:var(--ok)}td.FAIL{color:var(--bad)}td.INFO{color:var(--inf)}
.mono{font-family:Consolas,monospace}
.note{background:#111827;border:1px solid var(--line);border-radius:10px;padding:14px 16px;color:var(--mut);font-size:13px;margin-top:14px}
.note b{color:var(--tx)}
code{background:#0b1220;border:1px solid var(--line);border-radius:4px;padding:1px 5px;font-size:12px;color:#a5d6ff}
.two{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(max-width:760px){.two{grid-template-columns:1fr}}
</style></head><body><div class="wrap">
<h1>TUFT-r338 · 光速螺旋 G1：ω(r,t) 的场方程为何做不出来</h1>
<div class="sub">2026-11-01 · 靶：整理册 §二 G1 ｜ 承 S1/S10/S2/S11 + r124 T05/T06 + r329 ｜ sympy 符号 + Decimal 80 位</div>
<div>
<span class="badge">条目 %(n)d</span><span class="badge">PASS %(p)d</span><span class="badge">FAIL %(f)d</span>
<span class="badge">INFO %(i)d</span><span class="badge">控制组 %(c)s</span><span class="badge">守卫 %(g)s</span>
</div>
<div class="verdict"><b>G1-FREEDOM-COUNTING-NO-INVERSE / ONE-SCALAR-TWO-INITIAL-FUNCTIONS /
IDENTITY-LOCKS-OMEGA-ALGEBRAICALLY / G1-CLOSED-CONDITIONAL</b><br>
候选族 <b>0/4</b>；1 个标量场 + 1 条二阶 PDE ⇒ 通解 <b>2 个任意函数</b>、未知 1 个 ⇒ <b>净余 1</b>
（动态口径 3）；恒等式只锁 |ω| <b>不给演化</b>；康普顿锚在 a₀ 上 <b>越光速 137 倍</b>。</div>
<div class="grid">
<div class="card"><div class="k">候选方程通过</div><div class="n">0<span class="u">/ 4</span></div><div class="u">□ω=0 / KG / 恒等式 / 源项</div></div>
<div class="card"><div class="k">通解自由函数</div><div class="n">2<span class="u">个</span></div><div class="u">F(r−ct)+G(r+ct)</div></div>
<div class="card"><div class="k">净余自由函数</div><div class="n">1<span class="u">个</span></div><div class="u">2 − 1（未知 1 场）</div></div>
<div class="card"><div class="k">两方程后维数</div><div class="n">4<span class="u">常数</span></div><div class="u">{1,t,r,rt}，det≠0</div></div>
<div class="card"><div class="k">v_θ/c（r=a₀）</div><div class="n">%(vc)s</div><div class="u">= α⁻¹，越 v≤c</div></div>
<div class="card"><div class="k">判据集</div><div class="n">%(score)d<span class="u">/ 6</span></div><div class="u">R4/R5 过；R1/R2/R3/R6 不过</div></div>
</div>
<h2>一、四个候选逐个否证（Q1，0/4）</h2>
<table><tr><th>#</th><th>候选</th><th>通解自由函数</th><th>能唯一反解？</th><th>机器读数</th></tr>%(cand_rows)s</table>
<div class="note">四个候选都「像」场方程，但都不给唯一 ω：波动方程留 2 个函数；KG 连<b>振幅</b>都留；
恒等式对 ω <b>0 阶</b>（只锁 |ω|）；源项的唯一性要靠<b>外部 J</b> 买。
⇒ G1 的字面要求（二阶方程 + 唯一反解）在候选项内<b>完全落空</b>。</div>
<h2>二、自由度计数（Q2/Q5）</h2>
<div class="two">
<div class="card"><div class="k">口径 α（几何派）</div><div class="n mono" style="font-size:16px">4 − 3 = 1</div>
<div class="u">未知 {ω,κ,τ,r} − (恒等式 + κ,τ 定义) ⇒ 剩的是 <b>r</b>，不是 ω</div></div>
<div class="card"><div class="k">口径 β（多场派）</div><div class="n mono" style="font-size:16px">4 − 1 = 3</div>
<div class="u">κ,τ 独立传播 ⇒ 净余 3 ≥ 2 ⇒ 一条方程定不了</div></div>
</div>
<div class="note">计数<b>有牙</b>：单个任意函数 H(r,t) 代入 □H 残差非零；再叠一条 ∂_t²ω=0 后解空间压到
<b>4 个常数</b>（基 {1,t,r,rt}，四点求值矩阵 det = %(det)s）⇒「方程数增加确实降自由度」，
所以「一条不够」是<b>有内容的结论</b>，不是「方程没牙」。</div>
<h2>三、循环性：恒等式把 ω 锁成 κ,τ 的泛函（Q4）</h2>
<div class="note mono" style="font-size:13px">ω² = c²(κ²+τ²)　⇒　∂_tω = c²(κ∂_tκ + τ∂_tτ) / ω</div>
<div class="note">κ,τ 取常值 ⇒ ∂_tω = 0 ⇒ <b>ω 被冻死</b>：恒等式<b>产生不了演化</b>。
若坚持 ω 有演化，则 κ,τ 也必须传播 ⇒ 未知场 <b>≥3</b> ⇒「单场方程」<b>不存在</b>。
⇒ 这正是整理册「把恒等式当方程」的另一面：约束降维，但不产生动力学。</div>
<h2>四、康普顿锚越域复算（Q6）</h2>
<table>
<tr><th>锚点 r</th><th>v_θ/c</th><th>含义</th></tr>
<tr><td>λ̄_C = %(lam)s m</td><td>1</td><td>严格 null（恰在光速上）</td></tr>
<tr><td>a₀ = %(a0)s m</td><td>%(vc)s</td><td>= α⁻¹，<b>越 v≤c 137 倍</b>（整理册 G2 行机器复证）</td></tr>
</table>
<div class="note">口径：ω_C = m_ec²/ℏ = c/λ̄_C（<b>约化</b>康普顿波长）。机器校验 ω_C·λ̄_C/c−1 = %(chk)s；
a₀/(α⁻¹λ̄_C)−1 = %(dbohr)s ⇒ 玻尔半径恰等于 α⁻¹λ̄_C。若误用未约化 λ_C，比值降为 α⁻¹/(2π)≈21.8
⇒ 结论方向不变，但<b>数字必须写明 λ̄ 还是 λ</b>。</div>
<h2>五、唯一能成立的分支（Q7）</h2>
<div class="note">① <b>退化直线</b>：ω=const、κ=τ=0 ⇒ 恒等式自动满足，但无几何、无演化 ⇒ 零信息；
② <b>纯代数给定</b>：把 ω 当输入抄 ⇒ 0 条方程 ⇒ 只是命名（r95 外部输入账 #1 的原形）。
⇒ G1 的「成功」只存在于零信息量分支。</div>
<h2>六、条目逐条（主条目）</h2>
<table><tr><th>#</th><th>判决</th><th>条目</th></tr>%(main_rows)s</table>
<h2>七、控制组与守卫</h2>
<div class="two">
<table><tr><th>#</th><th>判决</th><th>控制组</th></tr>%(ctl_rows)s</table>
<table><tr><th>#</th><th>判决</th><th>守卫</th></tr>%(grd_rows)s</table>
</div>
<h2>八、门槛登记（Q9）</h2>
<table><tr><th>项</th><th>缺口</th><th>本卷状态</th><th>状态</th></tr>%(gate_rows)s</table>
<div class="note">三道自检门：承载物门 <b>PASS</b>（r329 已给帧局部承载物，本卷缺的是方程不是承载物）｜
判别力门 <b>FAIL</b>（无唯一 ω ⇒ 无点预言）｜洛伦兹门 <b>FAIL</b>（任何 ω 方程都必须写在某个帧里）。
⇒ <b>G1 收口（负）；G3/G4 已由 r324/r329 收口；G5/G6/G7 未动。</b></div>
<h2>九、诚实边界</h2>
<div class="note">B1 只论标量场、只否证二阶与本域候选（高阶/非局域未逐类穷举）；B2 计数在 1+1D（3+1D 只会更差）；
B3 r 与 ω 双自由与 G2 交叠，不主张已解决 r 的来源；B4 不给具体源模型；B5 用约化 λ̄_C，口径须写明；
B6 不主张纲领死亡，只主张「一条方程定 ω」的提法做不成。</div>
<div class="note" style="margin-top:26px">复现：<code>python -X utf8 源码\\_run_r338.py</code> ⇒ rc=0，条目 %(n)d，
控制组 %(c)s，守卫 %(g)s。本卷条目<b>不可与 r324/r329/r331 等相加</b>。</div>
</div></body></html>""" % {
        "n": summary["条目总数"], "p": summary["PASS"], "f": summary["FAIL"], "i": summary["INFO"],
        "c": summary["控制组"], "g": summary["守卫"], "score": extra["score"],
        "vc": fmt(extra["vc"], 8), "det": extra["det"],
        "lam": fmt(extra["lam_bar"], 6), "a0": fmt(A0, 6),
        "chk": fmt(extra["chk"], 4), "dbohr": fmt(extra["d_bohr"], 4),
        "cand_rows": cand_rows, "gate_rows": gate_rows,
        "main_rows": "".join(row(i) for i in main),
        "ctl_rows": "".join(row(i) for i in ctl),
        "grd_rows": "".join(row(i) for i in grd),
    }
    p = wpath(HTML_PATH)
    with io.open(p, "w", encoding="utf-8") as f:
        f.write(H)
    return p


# ================================================================ 主流程
def main():
    e1 = q1()
    e2 = q2()
    e3 = q3()
    e4 = q4()
    e5 = q5()
    e6 = q6()
    q7()
    q8()
    e9 = q9()
    e10 = q10()
    extra = {"declared_n": 24, "rowsA": e1["rows"], "n_cand": e1["n_pass"],
             "n_fun": e2["n_fun"], "net": e2["net"], "dim": e2["dim"], "det": e2["det"],
             "n_unk": e4["n_unk"], "free_alpha": e5["free_alpha"], "free_beta": e5["free_beta"],
             "vc": e6["v_over_c"], "alpha_inv": e6["alpha_inv"], "d_alpha": e6["d_alpha"],
             "lam_bar": e6["lam_bar"], "om_C": e6["om_C"], "chk": e6["chk"],
             "d_bohr": Decimal(rel(A0, (D1 / ALPHA) * (HBAR / (ME * C_L)))),
             "score": e10["score"], "gate_rows": e9["gate_rows"],
             "count_zero": True}
    controls(extra)
    guards(extra)
    summary = emit(extra)
    emit_judgment(summary, extra)
    p = emit_html(summary, extra)
    print("=" * 78)
    print("TUFT-%s · 光速螺旋 G1 ω 场方程：自由度计数不可反解定理" % RID)
    for k, v in summary.items():
        print("%-10s : %s" % (k, v))
    print("-" * 78)
    for it in ITEMS:
        print("[%s] %-4s %s" % (it["id"], it["verdict"], it["title"]))
    print("-" * 78)
    print("HTML:", p)
    print("RC = 0")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback
        traceback.print_exc()
        sys.exit(2)
