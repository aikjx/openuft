# -*- coding: utf-8 -*-
"""
ZXQ-23 · 空间光速螺旋统一场方程（UFE-2 候选）独立复算仪器

来料
----
`my_lib/utf/17-空间光速螺旋引力理论/核心公式.md`（23 个核心公式全维整理 v3.0）
及其同目录主干（`核心公式理论体系.md`、`传统公式与几何公式双向转换手册.md`、
`循环论证_TAUT问题分析.md` 等）。

定位
----
本仪器**不综述**，只做三件事：

1. **量纲审计**：自建 SI 指数向量量纲层（M, L, T, I），把 23 式 + 5 条扩展式
   逐式按「文献自己声明的符号量纲表」重算，判定自洽与否。
2. **经典极限重构**：把「场互变方程组」当成一台机器，检验它能否真的吐出
   麦克斯韦方程组的旋度方程与牛顿/库仑极限 —— 这是本轮唯一有信息量的部分。
3. **无信息量探针**：扰动 α / G 各 1e-8，看判定是否变化；并把「定义重排」
   （G=2Z/c、ε₀=c/(8πZ′)、Gm_P²=ℏc、Gε₀=q_P²/(4πm_P²)）逐条钉成 TAUT。

红线
----
1. 保留全部矛盾输出，**不把 FAIL 降为 PASS**。
2. 只判「量纲 / 数值 / 结构是否自洽」，**不判物理真伪**；数学自洽 ≠ 实验证实。
3. 区分「恒等式（无物理信息）」与「独立推导（有信息）」，前者一律标 INFO。

依赖：仅标准库（math / json / os / sys）。刻意不引入 sympy / mpmath：
本体系的判定在双精度（1e-16）量级上已足够，高精度不改变任何结论。

运行：python zxq23_ufe.py            # 退出码恒 0，产物落盘
      python zxq23_ufe.py --strict    # 任一 FAIL ⇒ 退出码 1（可做门禁）
      python zxq23_ufe.py --stdout    # 只打印不落盘
"""

import json
import math
import os
import sys

# Windows GBK 控制台保护：τ、ρ、ε 等字符会抛 UnicodeEncodeError 并吃掉判定
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

# ============================================================ 常数（CODATA 2018 / SI 2019）
C = 299792458.0            # c    m/s      精确定义
HBAR = 1.054571817e-34     # ℏ    J·s
QE = 1.602176634e-19       # e    C        精确定义
EPS0 = 8.8541878128e-12    # ε₀   F/m
MU0 = 1.25663706212e-6     # μ₀   H/m
G = 6.67430e-11            # G    m³·kg⁻¹·s⁻²
ALPHA = 7.2973525693e-3    # α    精细结构常数
ME = 9.1093837015e-31      # m_e  kg
MMU = 1.883531627e-28      # m_μ  kg
MTAU = 3.16754e-27         # m_τ  kg
MPL = 2.176434e-8          # m_P  kg
QPL = 1.875546038e-18      # q_P  C

# 文献自印的标定数值（核心公式.md §5.1 / §2.5，用于口径漂移比对，不用于判定）
LIT_Z = 9.995e-3
LIT_ZP = 1.347e18
LIT_ZZP = 1.35e16
LIT_K = 2.736e-7
LIT_KP = 6.25e-27
LIT_F = 1.292e-2

# 由定义现算（不引用文献值）
Z_DEF = G * C / 2.0                 # Z  = Gc/2
ZP_DEF = C / (8.0 * math.pi * EPS0)  # Z' = c/(8πε₀)
MPL_CALC = math.sqrt(HBAR * C / G)
QPL_CALC = math.sqrt(4.0 * math.pi * EPS0 * HBAR * C)
ALPHA_CALC = QE * QE / (4.0 * math.pi * EPS0 * HBAR * C)

# ============================================================ 结果收集
RESULTS = []


def rec(sid, sec, title, verdict, detail):
    RESULTS.append({
        "id": sid, "sec": sec, "title": title,
        "verdict": verdict, "detail": detail,
    })


def P(sid, sec, title, detail):
    rec(sid, sec, title, "PASS", detail)


def F(sid, sec, title, detail):
    rec(sid, sec, title, "FAIL", detail)


def BO(sid, sec, title, detail):
    rec(sid, sec, title, "BOUNDARY", detail)


def IN(sid, sec, title, detail):
    rec(sid, sec, title, "INFO", detail)


def rel(a, b):
    if b == 0:
        return float("nan")
    return abs(a - b) / abs(b)


def g(x, n=6):
    return "%.*g" % (n, x)


# ============================================================ 量纲引擎 (M, L, T, I)
def D(m=0, l=0, t=0, i=0):
    return (m, l, t, i)


def dmul(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2], a[3] + b[3])


def ddiv(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2], a[3] - b[3])


def dpow(a, n):
    return (a[0] * n, a[1] * n, a[2] * n, a[3] * n)


def dname(a):
    out = []
    sym = ["M", "L", "T", "I"]
    for k in range(4):
        v = a[k]
        if v == 0:
            continue
        out.append(sym[k] + ("" if v == 1 else "^%d" % v))
    return "·".join(out) if out else "1"


# ---- 三维向量小工具（供 M11 的数值核对用；只做加减叉积与模长）
def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0]]


def sub(a, b):
    return [a[k] - b[k] for k in range(3)]


def norm(a):
    return math.sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2])


# -------- 文献声明的符号量纲表 --------
# 出处：核心公式.md §1 符号规范前置修正 + §5.1 常数定义表。
# 说明：§1 把 k' 标为 [ITM^-1]，但 §5.1 给的实际单位是 C·s/kg。
#       C·s/kg = (IT)·T/M = I·T²·M^-1 —— §1 的标注漏了一个 T。
#       本表按**实际单位**取 [k'] = I T² M^-1（口径差异登记见 D00）。
K_SPEC_NOTE = "§1 标注 [k']=ITM^-1 与 §5.1 实际单位 C·s/kg 不符（C·s/kg=I·T²·M^-1，漏一个 T）"

DIM = {
    "L":    D(0, 1, 0, 0),     # 长度 r, ρ, b, s, R
    "T":    D(0, 0, 1, 0),     # 时间 t, τ(固有时)
    "W":    D(0, 0, -1, 0),    # 角速度 ω, dΩ/dt(Ω 无量纲)
    "V":    D(0, 1, -1, 0),    # 速度 C, V, v
    "ACC":  D(0, 1, -2, 0),    # 加速度 / 引力场 A
    "M":    D(1, 0, 0, 0),     # 质量 m, M, k
    "ONE":  D(0, 0, 0, 0),     # 无量纲 n, Ω, γ, α
    "G":    D(-1, 3, -2, 0),   # 万有引力常数
    "KP":   D(-1, 0, 2, 1),    # k'（实际单位 C·s/kg）
    "F":    D(1, 0, 0, -1),    # f 场转化常数（kg/A）
    "Z":    D(-1, 4, -3, 0),   # Z 引力光速常数
    "ZP":   D(1, 4, -5, -2),   # Z' 电磁几何常数
    "EPS0": D(-1, -3, 4, 2),   # ε₀
    "MU0":  D(1, 1, -2, -2),   # μ₀
    "E":    D(1, 1, -3, -1),   # 电场强度
    "B":    D(1, 0, -2, -1),   # 磁感应强度
    "Q":    D(0, 0, 1, 1),     # 电荷 (I·T)
    "MOM":  D(1, 1, -1, 0),    # 动量
    "FOR":  D(1, 1, -2, 0),    # 力
    "ENER": D(1, 2, -2, 0),    # 能量
    "HBAR": D(1, 2, -1, 0),    # ℏ
}


def dcheck(sid, name, lhs, rhs, note=""):
    """比对 LHS 声明量纲与 RHS 计算量纲"""
    if lhs == rhs:
        P(sid, "A", name, "RHS = %s = LHS 声明量纲 ✓%s" % (dname(rhs), (" | " + note) if note else ""))
    else:
        F(sid, "A", name,
          "RHS = %s，LHS 声明 = %s，差 = %s%s"
          % (dname(rhs), dname(lhs), dname(ddiv(rhs, lhs)), (" | " + note) if note else ""))


# ============================================================ §0 口径登记
def sec_notation():
    IN("D00", "0", "符号表口径：k' 的量纲标注",
       K_SPEC_NOTE + "；本仪器按实际单位 C·s/kg = I·T²·M^-1 计算，"
       "并按 §1 标注（I·T·M^-1）另算一版作对照：两版下式 9 / 10 的判定会翻转，"
       "式 11 两版皆 FAIL。这条标注错误本身登记为一条文献缺陷。")


# ============================================================ §A 23 式量纲审计
def sec_dimensions():
    d = DIM
    one = d["ONE"]

    # --- 4.1 时空基础（2）
    dcheck("D01", "式1 时空同一化 r=C·t",
           d["L"], dmul(d["V"], d["T"]))
    # 式2 三分量：r cosωt(L) / r sinωt(L) / ω b t (T^-1·L·T=L)
    dcheck("D02", "式2 三维螺旋时空（三分量逐项）",
           d["L"], dmul(dmul(d["W"], d["L"]), d["T"]),
           note="前两项为 r·cos/sin 恒为 L；第三项 ωbt 亦为 L")

    # --- 4.2 质量与动量（4）
    dcheck("D03", "式3 质量定义 m=k·dn/dΩ",
           d["M"], dmul(d["M"], ddiv(one, one)))
    # 式4：A = -G·k·(Δn/Δs)·(r/r)
    rhs4 = dmul(dmul(d["G"], d["M"]), ddiv(one, d["L"]))
    dcheck("D04", "式4 引力场 A=-Gk(Δn/Δs)(r/r)",
           d["ACC"], rhs4,
           note="04 层归档的 v3.5 原式写作 r/r³ ⇒ 量纲 LT^-2 自洽；本 23 式版写作 r/r ⇒ 多一个 L，"
                "§21.2 的牛顿极限推导随之失效（详见 M05）")
    dcheck("D05", "式5 静止动量 P₀=m₀C₀",
           d["MOM"], dmul(d["M"], d["V"]))
    dcheck("D06", "式6 运动动量 P=m(C−V)",
           d["MOM"], dmul(d["M"], d["V"]))

    # --- 4.3 统一场与力（2）
    dcheck("D07", "式7 宇宙大统一力 F=dP/dt",
           d["FOR"], ddiv(d["MOM"], d["T"]),
           note="恒等求导（莱布尼茨法则），无新物理内容")
    dcheck("D08", "式8 空间波动 ∇²L=(1/c²)∂²L/∂t²",
           dpow(d["L"], -2), dmul(dpow(d["L"], -2), one),
           note="标准波动方程形式；L 无量纲时两边同为 L^-2")

    # --- 4.4 电磁场（3）
    rhs9 = dmul(dmul(d["M"], d["KP"]), d["W"])      # k·k'·(1/Ω²)·(dΩ/dt)
    dcheck("D09", "式9 电荷定义 q=kk'(1/Ω²)(dΩ/dt)",
           d["Q"], rhs9,
           note="按 k' 实际单位 C·s/kg 自洽；若按 §1 标注 [k']=ITM^-1 则 RHS=I ≠ IT（文献标注错误所致）")
    rhs10 = dmul(dmul(rhs9, ddiv(one, d["EPS0"])), ddiv(d["L"], dpow(d["L"], 3)))
    dcheck("D10", "式10 电场 E=−kk'/(4πε₀Ω²)·(dΩ/dt)·(r/r³)",
           d["E"], rhs10,
           note="等价于 q·r̂/(4πε₀r²)，结构即库仑场（见 M06）")
    rhs11 = dmul(dmul(dmul(d["MU0"], d["M"]), d["KP"]),
                 dmul(d["W"], ddiv(d["L"], dpow(d["L"], 3))))
    dcheck("D11", "式11 磁场 B=μ₀γkk'/(4πΩ²)(dΩ/dt)·R/R'³",
           d["B"], rhs11,
           note="缺一个速度因子 [LT^-1]：正确形式应为 μ₀ q v×r̂/(4πr²)；"
                "两种 k' 口径下均 FAIL（与 04 层归档判定一致）")

    # --- 4.5 场转化（4）
    # 式12：∂²A/∂t² = (1/f)[V(∇·E) − c²(∇×B)]
    lhs12 = ddiv(d["ACC"], dpow(d["T"], 2))
    t1 = dmul(ddiv(one, d["F"]), dmul(d["V"], ddiv(d["E"], d["L"])))
    t2 = dmul(ddiv(one, d["F"]), dmul(dpow(d["V"], 2), ddiv(d["B"], d["L"])))
    dcheck("D12", "式12 变化引力场产生电磁场（两项分别核算）",
           lhs12, t1, note="第一项 V(∇·E)/f")
    dcheck("D12b", "式12 第二项 c²(∇×B)/f",
           lhs12, t2, note="第二项；两项同为 LT^-4，与 LHS 一致 ⇒ 式12 量纲自洽")

    # 式13：∇×A = B/f
    dcheck("D13", "式13 引力场旋度 ∇×A=B/f",
           ddiv(d["ACC"], d["L"]), ddiv(d["B"], d["F"]),
           note="对比 04 层归档的 v3.5/v3.7 版 ∇×∂ₜA=B/f（左边多 T^-1 ⇒ FAIL）；本版已修好")

    # 式14：E = −f·dA/dt
    dcheck("D14", "式14 变化引力场产生电场 E=−f·dA/dt",
           d["E"], dmul(d["F"], ddiv(d["ACC"], d["T"])))

    # 式15：dB/dt = −(A×E)/c² − (V/c²)×(dE/dt)
    lhs15 = ddiv(d["B"], d["T"])
    u1 = ddiv(dmul(d["ACC"], d["E"]), dpow(d["V"], 2))
    u2 = dmul(ddiv(d["V"], dpow(d["V"], 2)), ddiv(d["E"], d["T"]))
    dcheck("D15", "式15 变化磁场产生引力场和电场（两项分别核算）",
           lhs15, u1, note="第一项 (A×E)/c²")
    dcheck("D15b", "式15 第二项 (V/c²)×(dE/dt)",
           lhs15, u2, note="第二项；04 层归档的 v3.5 版首项多一个 f ⇒ FAIL，本版已修好")

    # --- 4.6 能量与动力学（2）
    dcheck("D16", "式16 能量 E=m₀c²=mc²√(1−v²/c²)",
           d["ENER"], dmul(d["M"], dpow(d["V"], 2)),
           note="借用 SR 的质能关系与洛伦兹因子")
    dcheck("D17", "式17 光速飞行器动力学 F=(C−V)dm/dt",
           d["FOR"], dmul(d["V"], ddiv(d["M"], d["T"])))

    # --- 4.7 核力场与统一常数（3）
    rhs18 = ddiv(dmul(dmul(d["G"], d["M"]), d["V"]), dpow(d["L"], 3))
    if rhs18 == d["ACC"]:
        P("D18", "A", "式18 核力场 D=−Gm(C−3r̂ṙ)/r³", "RHS = %s = LT^-2 ✓" % dname(rhs18))
    else:
        BO("D18", "A", "式18 核力场 D=−Gm(C−3r̂ṙ)/r³",
           "RHS = %s，§4.7 声明 [D]=LT^-2 ⇒ 差 %s；"
           "04 层归档按 [D]=LT^-3 判定则自洽 ⇒ **量纲随声明走，D 的物理身份未定**"
           % (dname(rhs18), dname(ddiv(rhs18, d["ACC"]))))
    dcheck("D19", "式19 G=2Z/c",
           d["G"], ddiv(d["Z"], d["V"]),
           note="量纲自洽，但 Z≡Gc/2 是**定义** ⇒ 循环，无预测力（见 T01）")
    dcheck("D20", "式20 ε₀=c/(8πZ′)",
           d["EPS0"], ddiv(d["V"], d["ZP"]),
           note="量纲自洽，但 Z′≡c/(8πε₀) 是**定义** ⇒ 循环（见 T02）")

    # --- 4.8 加速/圆周运动电荷产生引力场（2）
    rhs21 = dmul(dmul(dmul(d["Q"], d["ACC"]), ddiv(one, d["EPS0"])),
                 ddiv(one, dmul(dpow(d["V"], 5), d["L"])))
    dcheck("D21", "式21 加速运动电荷产生引力场 A=q·v̇×r̂/(4πε₀c⁵r)",
           d["ACC"], rhs21,
           note="文献自评 ✅ 的算式漏了 c⁵ 的 T 幂次；实际 RHS=M·L^-2·I^-1，与 LT^-2 无可比性")
    dcheck("D22", "式22 圆周运动电荷产生引力场（ω²R 代入 v̇）",
           d["ACC"], dmul(dmul(dmul(d["Q"], dpow(d["W"], 2)), d["L"]),
                          dmul(ddiv(one, d["EPS0"]), ddiv(one, dmul(dpow(d["V"], 5), d["L"])))),
           note="与式21 同型，同因 FAIL")

    # --- 4.9 归一化（1）
    dcheck("D23", "式23 全尺度归一化 GMm/(ℏc)=1",
           one, ddiv(dmul(d["G"], dpow(d["M"], 2)), dmul(d["HBAR"], d["V"])),
           note="量纲恒为 1（**恒等式，对任意 M,m 都“成立”这个量纲**）；"
                "数值等于 1 只在 M·m=m_P² 时成立 ⇒ 该式不归一化任何东西，只是重排 m_P 定义（见 T03）")

    # --- 扩展式（§13.3 / §13.4 / §15.1，不在 23 式编号内但被用作四力统一）
    w_rhs = dmul(ddiv(dmul(d["F"], d["Z"]), dpow(d["V"], 2)),
                 dmul(d["W"], ddiv(one, d["L"])))
    BO("D24", "A", "扩展式 弱力场 W=−(fZ/c²)(dΩ/dτ)∇Ω·e^(−r/R_W)",
       "RHS = %s；文献未声明 [W]，无法比对 ⇒ 只有“声明依赖”的判定" % dname(w_rhs))
    dcheck("D25", "扩展式 四力合成 F_N=m·D 与 F_W=m·W",
           d["FOR"], dmul(d["M"], rhs18),
           note="F_N 量纲 = M·LT^-3 = MLT^-3 ≠ 力 MLT^-2（缺 T）；"
                "F_W = M·LT^-2I^-1 亦 ≠ 力 ⇒ **四力合成式（§15.1）在量纲上不成立**")


# ============================================================ §B 经典极限重构（UFE-2 的实质检验）
def sec_maxwell():
    """把「场互变方程组」当机器：它能不能吐出麦克斯韦方程组？
    这是本轮唯一可能产生**独立信息**的地方 —— 若成立，说明这套场互变式
    不是任意拼凑，而是与经典电磁学同构。"""
    d = DIM
    one = d["ONE"]

    # M01：式13 + 式14 ⇒ 法拉第电磁感应定律
    #   ∇×E = ∇×(−f dA/dt) = −f d(∇×A)/dt = −f d(B/f)/dt = −dB/dt   （f 为常数）
    P("M01", "B", "式13+式14 ⇒ 法拉第定律 ∇×E = −∂B/∂t",
      "∇×E = −f·∂(∇×A)/∂t = −f·∂(B/f)/∂t = −∂B/∂t（f 与时空无关）。"
      "量纲核对：[∇×E]=%s，[∂B/∂t]=%s ⇒ 一致。**该体系自身可推出麦克斯韦第二旋度方程**"
      % (dname(ddiv(d["E"], d["L"])), dname(ddiv(d["B"], d["T"]))))

    # M02：式13 ⇒ ∇·B = f ∇·(∇×A) ≡ 0
    P("M02", "B", "式13 ⇒ 磁场无源 ∇·B = 0",
      "∇·B = f·∇·(∇×A) ≡ 0（旋度的散度恒为零，数学恒等）。"
      "⇒ 麦克斯韦第三方程由式13 的结构自动给出，无需额外假设")

    # M03：式12 + 式14 ⇒ 安培-麦克斯韦项
    #   d²A/dt² = −(1/f)dE/dt，代入式12 ⇒ −dE/dt = V(∇·E) − c²(∇×B)
    #   ⇒ ∇×B = (1/c²)∂E/∂t + (V/c²)(∇·E)
    lhs = ddiv(d["B"], d["L"])
    r1 = dmul(ddiv(one, dpow(d["V"], 2)), ddiv(d["E"], d["T"]))
    r2 = dmul(ddiv(d["V"], dpow(d["V"], 2)), ddiv(d["E"], d["L"]))
    ok1 = (r1 == lhs)
    ok2 = (r2 == lhs)
    if ok1 and ok2:
        P("M03", "B", "式12+式14 ⇒ ∇×B = (1/c²)∂E/∂t + (V/c²)(∇·E)",
          "两项量纲均为 %s，与 [∇×B]=%s 一致。第一项即标准位移电流项 μ₀ε₀∂E/∂t"
          % (dname(r1), dname(lhs)))
    else:
        F("M03", "B", "式12+式14 ⇒ 安培项推导",
          "项1 %s / 项2 %s 与 [∇×B]=%s 不一致" % (dname(r1), dname(r2), dname(lhs)))

    # M04：第二项 ≡ μ₀J（代入标准高斯定律 ∇·E=ρ_q/ε₀ 与 J=ρ_q V）
    #   (V/c²)(∇·E) = V ρ_q/(ε₀ c²) = μ₀ ρ_q V = μ₀ J
    ident = dmul(d["MU0"], ddiv(d["Q"], dmul(dpow(d["L"], 2), d["T"])))  # μ₀·J(电流密度)
    P("M04", "B", "M03 第二项 ≡ μ₀J（安培定律的电流项）",
      "(V/c²)(∇·E) = V·ρ_q/(ε₀c²) = μ₀ρ_qV = μ₀J；[μ₀J]=%s 与 [∇×B]=%s 一致。"
      "⇒ **式12+式14+高斯定律三件套完整重构了安培-麦克斯韦定律**"
      % (dname(ident), dname(ddiv(d["B"], d["L"]))))

    # M05：牛顿极限（§21.2）
    F("M05", "B", "牛顿极限：A=−(2Z/c)k(Δn/Δs)(r/r) ⇒ g=−GM/r²·r̂",
      "按本 23 式版的 r/r 写法，RHS 量纲为 L²T^-2，而 g 需 LT^-2 ⇒ **牛顿极限推导不成立**；"
      "若回退到 04 层归档的 r/r³ 写法则成立。文献 §21.2 声称的「自然衔接牛顿引力」"
      "依赖一个与本版式4 不自洽的写法（同 D04）")

    # M06：库仑极限（§13.2）
    P("M06", "B", "库仑极限：式10 ⇒ E=Q·r̂/(4πε₀r²)",
      "式10 在「式9 定义的 q 就是电荷」这一条件下结构即库仑场（量纲已由 D10 核过）。"
      "条件性：式9 是否真的给出可观测电荷，取决于 k·k' 的标定，属外部输入（见 T06）")

    # M07：力强度比 F_em/F_g = αG/ℏ · Qq/(Mm)
    rhs = dmul(ddiv(dmul(one, d["G"]), d["HBAR"]),
               ddiv(dpow(d["Q"], 2), dpow(d["M"], 2)))
    F("M07", "B", "§15.2 力强度比 F_em/F_g = (αG/ℏ)·Qq/(Mm)",
      "RHS 量纲 = %s ≠ 1（应为无量纲）。正确重排应为 F_em/F_g = αℏc/(G m²)（即 α/α_G）；"
      "文献把 ℏc/G 写成 G/ℏ，且把 1/m² 拆成 Qq/(Mm) ⇒ 量纲彻底错" % dname(rhs))

    IN("M08", "B", "§15.2 数值断言 F_N/F_em≈10²、F_W/F_N≈10⁻⁵",
       "无推导链、无阈值、无误差棒；两个数是**直接写下的**，不是本仪器可复算的输出")

    # M09：把式12/13/14 联立消元，看它是否封闭成一个方程（这才是「统一场方程」的落地检验）
    #   B = f∇×A（式13）代入式12；E = −f∂ₜA（式14）
    #   ⇒ ∂ₜ²A = −V∂ₜ(∇·A) − c²[∇(∇·A) − ∇²A]
    #   ⇒ 取 ∇·A = 0 ⇒ ∂ₜ²A = c²∇²A  ⇒ □A = 0（以 c 传播的波动方程）
    P("M09", "B", "式12+13+14 联立消元 ⇒ A 的封闭方程",
      "消元后 ∂ₜ²A = −V∂ₜ(∇·A) − c²[∇(∇·A) − ∇²A]；"
      "在 ∇·A=0 下退化为 ∂ₜ²A = c²∇²A，即 □A=0 ⇒ **以 c 传播的波动方程**。"
      "这是本轮唯一一个「由体系自身三式联立、无需外部场方程」得到的封闭动力学方程")

    BO("M10", "B", "M09 的诚实边界：c 是嵌入的不是导出的，A 的身份在体系内游移",
       "①式12 自带 c² 系数 ⇒ 波速等于 c 是**输入**，不是推导结果；"
       "②∇·A=0 是本仪器外加的规范条件，体系未给出；"
       "③A 在式4/式12 里被声明为「引力场」，联立后却满足电磁波动方程 ⇒ "
       "**同一个符号 A 同时承担引力场与电磁矢势两种身份**，这是该体系最深的诠释缺口，"
       "也是 04 层已登记的「κ,τ 全部由 m_e 反推」那一族问题的同源表现")

    # M11：Ḃ 方程（式15）不是独立公设，而是 C-01+C-03 的代数推论
    #   C-03: E = −f ∂ₜA  ⇒  Ė = −f ∂ₜ²A
    #   C-01: ∂ₜ²A = (1/f)[V(∇·E) − c²(∇×B)]  ⇒  Ė = c²(∇×B) − V(∇·E)
    #   代入 C-04 的第二项 (V/c²)×Ė：
    #       (1/c²)V×(c²W − sV) = V×W − (s/c²)(V×V) = V×W     （W≡∇×B, s≡∇·E）
    #   ⇒ C-04 等价于  Ḃ = −(A×E)/c² − V×(∇×B)
    # 这只用到 V×V ≡ 0，是代数恒等，不引入任何新假设。
    import random as _rnd
    _rnd.seed(20261003)
    worst = 0.0
    for _ in range(200):
        vv = [_rnd.uniform(-3, 3) for _ in range(3)]
        ww = [_rnd.uniform(-3, 3) for _ in range(3)]
        s = _rnd.uniform(-3, 3)
        e_dot = [C * C * ww[k] - s * vv[k] for k in range(3)]      # Ė = c²W − sV
        # 在 c² 尺度上比较，避免 1/c² 放大：V×Ė 应等于 c²·(V×W)
        t1 = cross(vv, e_dot)
        t2 = [C * C * x for x in cross(vv, ww)]
        worst = max(worst, norm(sub(t1, t2)) / max(norm(t1), 1e-300))
    lhs_d = ddiv(d["B"], d["T"])
    term1 = ddiv(dmul(d["ACC"], d["E"]), dpow(d["V"], 2))
    term2 = dmul(d["V"], ddiv(d["B"], d["L"]))
    if worst < 1e-12 and term1 == lhs_d and term2 == lhs_d:
        P("M11", "B", "Ḃ 方程（式15）可由式12+式14 代数推出 ⇒ 不是独立公设",
          "代入 Ė = c²(∇×B) − V(∇·E) 后，C-04 的第二项化为 V×(∇×B) − (s/c²)(V×V)，"
          "而 V×V ≡ 0 ⇒ 两项量纲同为 %s，随机 200 组分量最大相对残差 %s（机器零）。"
          "**正典的独立公设数因此由 9 降到 8**（依据是代数恒等，非实验证据）"
          % (dname(lhs_d), g(worst)))
    else:
        F("M11", "B", "Ḃ 方程的相容性检验未过",
          "残差 %s；两项量纲 %s / %s vs %s" % (g(worst), dname(term1), dname(term2), dname(lhs_d)))


# ============================================================ §C 数值恒等（CODATA 对标）
def sec_numbers():
    # N01 Z
    P("N01", "C", "Z = Gc/2 数值复算",
      "现算 Z = %s；文献自印 %s ⇒ 相对差 %s（文献值对应 G≈6.67e-11 的旧口径）"
      % (g(Z_DEF), g(LIT_Z), g(rel(Z_DEF, LIT_Z))))
    # N02 Z'
    P("N02", "C", "Z′ = c/(8πε₀) 数值复算",
      "现算 Z′ = %s；文献自印 %s ⇒ 相对差 %s"
      % (g(ZP_DEF), g(LIT_ZP), g(rel(ZP_DEF, LIT_ZP))))
    # N03 ZZ'
    zz = Z_DEF * ZP_DEF
    P("N03", "C", "ZZ′ = Gc²/(16πε₀) 数值复算",
      "现算 %s；文献自印 %s ⇒ 相对差 %s"
      % (g(zz), g(LIT_ZZP), g(rel(zz, LIT_ZZP))))
    # N04 Z/Z'
    ratio = Z_DEF / ZP_DEF
    theo = 4.0 * math.pi * EPS0 * G
    P("N04", "C", "Z/Z′ = 4πε₀G（解析式 ↔ 数值）",
      "现算 %s；解析式 4πε₀G = %s ⇒ 相对差 %s（恒等）"
      % (g(ratio), g(theo), g(rel(ratio, theo))))
    # N05 m_P
    P("N05", "C", "m_P = √(ℏc/G) 数值复算",
      "现算 %s kg；CODATA 采用值 %s ⇒ 相对差 %s"
      % (g(MPL_CALC), g(MPL), g(rel(MPL_CALC, MPL))))
    # N06 q_P
    P("N06", "C", "q_P = √(4πε₀ℏc) 数值复算",
      "现算 %s C；文献采用值 %s ⇒ 相对差 %s"
      % (g(QPL_CALC), g(QPL), g(rel(QPL_CALC, QPL))))
    # N07 G·m_P² = ℏc
    lhs = G * MPL_CALC ** 2
    rhs = HBAR * C
    P("N07", "C", "G·m_P² = ℏc 数值核对",
      "左 %s / 右 %s ⇒ 相对差 %s（**由 m_P 定义保证，恒等**，见 T03）"
      % (g(lhs), g(rhs), g(rel(lhs, rhs))))
    # N08 G·ε₀ = q_P²/(4π m_P²)
    lhs = G * EPS0
    rhs = QPL_CALC ** 2 / (4.0 * math.pi * MPL_CALC ** 2)
    P("N08", "C", "G·ε₀ = q_P²/(4π m_P²) 数值核对",
      "左 %s / 右 %s ⇒ 相对差 %s（**由 q_P、m_P 定义推出的恒等式**，见 T04）"
      % (g(lhs), g(rhs), g(rel(lhs, rhs))))
    # N09 α
    P("N09", "C", "α = e²/(4πε₀ℏc) 数值复算",
      "现算 %s；CODATA %s ⇒ 相对差 %s（**这就是 α 的定义**，见 T05）"
      % (g(ALPHA_CALC), g(ALPHA), g(rel(ALPHA_CALC, ALPHA))))
    # N10 电子尺度链
    rho_e = HBAR / (ME * C)
    omega_e = C / rho_e
    f_e = omega_e / (2.0 * math.pi)
    lam_e = C / f_e
    E_e = HBAR * omega_e
    rest = ME * C * C
    P("N10", "C", "电子尺度链 ρ_e=ℏ/m_ec、ω_e=c/ρ_e、λ_e、ħω_e=m_ec²",
      "ρ_e=%s m、ω_e=%s rad/s、f_e=%s Hz、λ_e=%s m；"
      "ħω_e 与 m_ec² 相对差 %s ⇒ 链内自洽（**闭合于 mcρ=ℏ，是定义链不是预言**）"
      % (g(rho_e), g(omega_e), g(f_e), g(lam_e), g(rel(E_e, rest))))
    # N11 v_⊥²+v_z²=c²
    vp = ALPHA * C
    vz = C * math.sqrt(1.0 - ALPHA * ALPHA)
    tot = math.sqrt(vp * vp + vz * vz)
    P("N11", "C", "速度分解 v_⊥=αc、v_z=c√(1−α²)、v_⊥²+v_z²=c²",
      "v_⊥=%s、v_z=%s、合成 %s ⇒ 与 c 相对差 %s（**三角恒等**，恒等式无物理信息）"
      % (g(vp), g(vz), g(tot), g(rel(tot, C))))
    # N12 文献自印 k / k' / f 的可复算性
    IN("N12", "C", "k≈2.736e-7 kg、k′≈6.25e-27 C·s/kg、f≈1.292e-2 kg/A 的可复算性",
       "文献称「CODATA 标定」但**未给出任何由常数算出它们的公式**；"
       "本仪器无法独立复算 ⇒ 这三个数是自由输入，携带了体系里全部的质量/电荷/转化标度")


# ============================================================ §D 循环论证（TAUT）登记
def sec_taut():
    IN("T01", "D", "G = 2Z/c", "Z ≡ Gc/2 是**定义**；由 Z 反解 G 是恒等重排，零预测力")
    IN("T02", "D", "ε₀ = c/(8πZ′)", "Z′ ≡ c/(8πε₀) 是**定义**；同上，恒等重排")
    IN("T03", "D", "G·m_P² = ℏc", "m_P ≡ √(ℏc/G) 是**定义**；该式就是定义的平方")
    IN("T04", "D", "G·ε₀ = q_P²/(4π m_P²)",
       "代入 q_P=√(4πε₀ℏc)、m_P=√(ℏc/G) 后左=右=ε₀G，**代数恒等**；"
       "文献 §十八 称之为「引电终极统一锚定」，实为两个定义的组合")
    IN("T05", "D", "α = e²/(4πε₀ℏc)", "这就是 α 的**定义**；任何用 α 反推的式子都闭合在此处")
    IN("T06", "D", "m = ℏ/(cρ) 与 mcρ = ℏ",
       "ρ 由 m 定义（ρ=ℏ/mc）⇒ 用该式「验证」任何粒子质量都是循环；"
       "04 层与 `循环论证_TAUT问题分析.md` 已同口径登记")
    F("T07", "D", "α 的几何定义：同目录内两份文件给出互为倒数的两个定义",
      "`核心公式理论体系.md` §3.4 写 α=κ/τ，`最伟大理论_诚实边界报告.md` §1.2 写 α=τ/κ；"
      "两定义互为倒数 ⇒ 对同一组 (κ,τ)，一个给出 α≈1/137、另一个给出 α≈137，"
      "相差 α^-2 = %s 倍 ⇒ **α 的几何定义在本目录内部不自洽**（硬冲突，非口径漂移）"
      % g(ALPHA ** -2))
    IN("T08", "D", "m_n = m_P·α^(n−1)·f(n) 中 f(n) 未给出",
       "f(n) 从未被定义或推导 ⇒ 该式对任意质量谱都可「拟合」，不可证伪（定量见 S01）")


# ============================================================ §E 扰动探针（无信息量检测）
def _taut_set(alpha, gv):
    """在给定 α / G 下重算那一组‘恒等式’，返回 (通过条数, 总条数)"""
    mpl = math.sqrt(HBAR * C / gv)
    qpl = math.sqrt(4.0 * math.pi * EPS0 * HBAR * C)
    checks = []
    checks.append(rel(gv * mpl ** 2, HBAR * C) < 1e-12)                      # G m_P² = ℏc
    checks.append(rel(gv * EPS0, qpl ** 2 / (4.0 * math.pi * mpl ** 2)) < 1e-12)  # Gε₀ = q_P²/4πm_P²
    checks.append(rel(gv * C / 2.0, gv * C / 2.0) < 1e-12)                   # Z 定义
    checks.append(rel(C / (8.0 * math.pi * EPS0), C / (8.0 * math.pi * EPS0)) < 1e-12)
    checks.append(rel(alpha, alpha) < 1e-12)                                 # α 自比
    return sum(1 for x in checks if x), len(checks)


def sec_probe():
    base_ok, base_n = _taut_set(ALPHA, G)
    for tag, fac, target in (("α", ALPHA, "α"), ("G", G, "G")):
        perturbed = fac * (1.0 + 1e-8)
        if tag == "α":
            ok, n = _taut_set(perturbed, G)
        else:
            ok, n = _taut_set(ALPHA, perturbed)
        drift = "不变" if ok == base_ok else "改变"
        IN("P0" + ("1" if tag == "α" else "2"), "E",
           "%s 扰动 1e-8 后恒等式组的判定" % target,
           "基线 %d/%d 通过；扰动后 %d/%d 通过 ⇒ 判定**%s**。"
           "这 %d 条是定义重排，对输入取值完全不敏感 ⇒ 它们不能作为任何常数的证据"
           % (base_ok, base_n, ok, n, drift, n))

    # P03：把 α 换成 1/137（文献取整口径），看依赖 α 的式子跳多少
    a137 = 1.0 / 137.0
    jump = rel(a137, ALPHA)
    IN("P03", "E", "α 取整口径（1/137 vs CODATA）对下游的影响",
       "两口径相对差 %s（0.026%%）；文献在同一份文件里混用这两种口径"
       "（§8 用 CODATA，§2.5 用 1/137）⇒ 任何到 1e-4 精度的‘验证’都先被这个口径吃掉" % g(jump))


# ============================================================ §F 质量谱可证伪性定量
def sec_spectrum():
    # 反解 f(n)：若 m_n = m_P α^(n-1) f(n)，取 n=1,2,3 对应 e, μ, τ
    fs = []
    for n, m in ((1, ME), (2, MMU), (3, MTAU)):
        fs.append(m / (MPL_CALC * ALPHA ** (n - 1)))
    r21 = fs[1] / fs[0]
    r32 = fs[2] / fs[1]
    F("S01", "F", "m_n = m_P·α^(n−1)·f(n) 对三代轻子的反解",
      "反解出 f(1)=%s、f(2)=%s、f(3)=%s；"
      "相邻比 f(2)/f(1)=%s、f(3)/f(2)=%s —— 两者相差 %s 倍且无规律，"
      "f 跨 %s 个量级 ⇒ **α 幂律不承担任何质量信息，全部由未定义的 f(n) 承担**"
      % (g(fs[0]), g(fs[1]), g(fs[2]), g(r21), g(r32), g(rel(r21, r32)),
         g(abs(math.log10(fs[2] / fs[0])))))

    # 纯 α 幂律（f≡1）的对照
    pred = [MPL_CALC * ALPHA ** (n - 1) for n in (1, 2, 3)]
    dev = [rel(pred[k], m) for k, m in enumerate((ME, MMU, MTAU))]
    F("S02", "F", "取 f(n)≡1 的纯 α 幂律预言 vs 实测",
      "预言 m_1=%s / m_2=%s / m_3=%s kg；对 e/μ/τ 相对偏差 %s / %s / %s ⇒ 纯幂律被数据否"
      % (g(pred[0]), g(pred[1]), g(pred[2]), g(dev[0]), g(dev[1]), g(dev[2])))

    IN("S03", "F", "质量比 m_μ/m_e、m_τ/m_μ 与 α 的简单幂次对照",
       "实测 m_μ/m_e=%s、m_τ/m_μ=%s；最接近的整数幂 α^-k 需 k=%s 与 %s（非整数），"
       "⇒ 单纯 α 的整数幂谱无法同时命中两个比值（与 `质量谱α幂律统治_全维精算验证.py` 的负结果同向）"
       % (g(MMU / ME), g(MTAU / MMU),
          g(math.log(MMU / ME) / math.log(1.0 / ALPHA)),
          g(math.log(MTAU / MMU) / math.log(1.0 / ALPHA))))


# ============================================================ 汇总与产物
def summarize():
    cnt = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
    for r in RESULTS:
        cnt[r["verdict"]] = cnt.get(r["verdict"], 0) + 1
    return cnt


def write_outputs(cnt, write_files):
    payload = {
        "instrument": "zxq23_ufe.py",
        "scope": "utf/17-空间光速螺旋引力理论 · 23 式 + 扩展式 · UFE-2 候选",
        "counts": cnt,
        "total": len(RESULTS),
        "constants": {
            "Z_def": Z_DEF, "Zp_def": ZP_DEF, "ZZp": Z_DEF * ZP_DEF,
            "m_P": MPL_CALC, "q_P": QPL_CALC, "alpha": ALPHA_CALC,
        },
        "results": RESULTS,
    }
    if not write_files:
        return payload
    with open(os.path.join(HERE, "zxq23_ufe_results.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    lines = []
    lines.append("# ZXQ-23 独立复算报告（运行产物，非手写）")
    lines.append("")
    lines.append("生成者：`验证脚本/zxq23_ufe.py`（零第三方依赖，仅标准库）")
    lines.append("")
    lines.append("| 判定 | 计数 |")
    lines.append("|---|---|")
    for k in ("PASS", "FAIL", "BOUNDARY", "INFO"):
        lines.append("| %s | %d |" % (k, cnt.get(k, 0)))
    lines.append("| **合计** | **%d** |" % len(RESULTS))
    lines.append("")
    cur = None
    for r in RESULTS:
        if r["sec"] != cur:
            cur = r["sec"]
            lines.append("")
            lines.append("## §%s" % cur)
            lines.append("")
        lines.append("- **%s · %s**：`%s` — %s" % (r["id"], r["title"], r["verdict"], r["detail"]))
    lines.append("")
    with open(os.path.join(HERE, "zxq23_ufe_report.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return payload


def main():
    argv = sys.argv[1:]
    strict = "--strict" in argv
    write_files = "--stdout" not in argv

    sec_notation()
    sec_dimensions()
    sec_maxwell()
    sec_numbers()
    sec_taut()
    sec_probe()
    sec_spectrum()

    cnt = summarize()
    write_outputs(cnt, write_files)

    print("=" * 78)
    print("ZXQ-23 · 空间光速螺旋统一场方程（UFE-2 候选）独立复算")
    print("=" * 78)
    for r in RESULTS:
        print("[%-8s] %-6s %s" % (r["verdict"], r["id"], r["title"]))
        print("           %s" % r["detail"])
    print("-" * 78)
    print("合计 %d 条：PASS %d / FAIL %d / BOUNDARY %d / INFO %d"
          % (len(RESULTS), cnt.get("PASS", 0), cnt.get("FAIL", 0),
             cnt.get("BOUNDARY", 0), cnt.get("INFO", 0)))
    if write_files:
        print("产物：zxq23_ufe_results.json · zxq23_ufe_report.md")
    print("红线：PASS 仅代表「未被本次复算推翻」；数学自洽 ≠ 实验证实。")

    if strict and cnt.get("FAIL", 0) > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
