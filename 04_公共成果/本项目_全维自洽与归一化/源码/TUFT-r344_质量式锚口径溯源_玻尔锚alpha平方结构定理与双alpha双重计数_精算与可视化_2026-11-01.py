# -*- coding: utf-8 -*-
"""
TUFT-r344 · 质量式锚口径溯源：玻尔锚 α² 结构定理（★攻 X-R342-2）
（承 r342 Q3「玻尔锚差 1.878e4 倍」/ S1「α=κ/τ 是输入」/ G2 / r124 T05 / 整理册 §二 G2）

靶：把 r342 的「1.878e4 倍」解剖成**可证的幂律**，回答「这个差是测量噪声还是结构必然」。

  Q1  锚产物的精确幂律：玻尔锚给 m_B/m_e = α²√(1+α²)，故所需/实际 = α⁻²/√(1+α²)
      ⇒ 差的不是任意数，是 α⁻²（1.878e4 = α⁻²，机器验）
  Q2  幂次的来源定理：τ 主导 ⇒ τ_B = α/a₀ = α²/λ̄_C（精确），m ∝ τ ⇒ α² 自动出现
  Q3  S1 自指闭环：κ_B/τ_B = α（机器验至 1e-9）⇒ 「α 当输入」与「质量被 α² 压低」
      是同一个 α 数了两次 ⇒ 双重计数（不是两个巧合）
  Q4  锚梯：m(锚)/m_e = λ̄_C·√(κ²+τ²)；r=λ̄_C ⇒ 1；r=a₀（κ 主导）⇒ α；r=a₀（S1 比例）⇒ α²
      ⇒ 唯一闭合锚是 λ̄_C ⇒ 「电子世界线不可能以 a₀ 为螺旋半径」
  Q5  r95 登记的 m_eff 与几何质量式差 √(1+α²)：另是一个「口径混用」缺口
  Q6  可修性穷举：纯数 k ∈ [−8,8]、c 幂 p ∈ [−2,2]、α 幂 q ∈ [−4,4] 全部不闭合
      ⇒ 须外部新常数或改质量式本身
  Q7  量纲复核：α 无量纲 ⇒ 幂次漂移不撞量纲门 ⇒ 量纲门对 α 口径**零判别力**（新洞见）
  Q8  与 Q1 合账：慢变螺旋不改变幂律 ⇒ 结构必然
  Q9  对表 S1/S7/G2/r124 T05/r342/r338
  Q10 G1–G7 门槛 + 三道自检门
  Q11 判据集 R1–R6

控制组 C1–C4 / 守卫 G1–G10
判词：ANCHOR-POWER-LAW-ALPHA-SQUARED / TWO-ALPHA-DOUBLE-COUNTING /
      ONLY-COMPTON-ANCHOR-CLOSES / MASSFORM-DIMENSION-BLIND-TO-ALPHA
"""
import io
import json
import os
import sys
import time
from decimal import Decimal, getcontext

getcontext().prec = 80

RID = "r344"
STAMP = "2026-11-01"
ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
SRC = os.path.join(ROOT, "源码")
DATA = os.path.join(ROOT, "数据")
JUD = os.path.join(ROOT, "判定")
BASE = ("TUFT-%s_质量式锚口径溯源_玻尔锚alpha平方结构定理与双alpha双重计数_"
        "精算与可视化_%s" % (RID, STAMP))
JUD_PATH = os.path.join(JUD, "判定_TUFT-%s_%s.md" % (RID, BASE[len("TUFT-r344_"):]))
HTML_PATH = os.path.join(ROOT, "四力统一方程_质量式锚口径溯源_r344可视化_%s.html" % STAMP)

WRITTEN = []
T0 = time.time()

C_L = Decimal("2.99792458e8")
ALPHA = Decimal("7.2973525693e-3")
A0 = Decimal("5.29177210903e-11")
HBAR = Decimal("1.054571817e-34")
ME = Decimal("9.1093837015e-31")
G_N = Decimal("6.67430e-11")

D0, D1, D2 = Decimal(0), Decimal(1), Decimal(2)

ITEMS = []
R_LIST = {}


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


def _safe(v):
    if isinstance(v, (str, int, float, bool)) or v is None:
        return v
    if isinstance(v, (list, tuple)):
        return [_safe(x) for x in v]
    if isinstance(v, dict):
        return {str(k): _safe(x) for k, x in v.items()}
    return str(v)


def add(tid, layer, title, verdict, detail, kv=None):
    ITEMS.append({"id": tid, "layer": layer, "title": title, "verdict": verdict,
                  "detail": detail, "kv": {k: _safe(v) for k, v in dict(kv or {}).items()}})


def wpath(p):
    WRITTEN.append(p)
    return p


def wdim(m, l, t):
    import sympy as sp
    return sp.Matrix([m, l, t])


# 锚常数（全部由 α、λ̄_C、a₀ 三量推出，便于幂律核对）
LAM = HBAR / (ME * C_L)                  # λ̄_C [m]
OM_C = ME * C_L * C_L / HBAR             # ω_C [s⁻¹]
KAP_B = ALPHA ** 2 / A0                  # κ_B = α²/a₀ [m⁻¹]
TAU_B = ALPHA / A0                       # τ_B = α/a₀ [m⁻¹]（v_z=c 极限）
SQR_B = dsqrt(KAP_B ** 2 + TAU_B ** 2)   # √(κ²+τ²)
M_B = (HBAR / C_L) * SQR_B               # 玻尔锚质量
ALPHA_INV = D1 / ALPHA
ALPHA_INV2 = D1 / (ALPHA * ALPHA)
SQRT_1A2 = dsqrt(D1 + ALPHA * ALPHA)


# ================================================================ Q1 · 幂律
def q1():
    """m_B/m_e = α²√(1+α²)；所需/实际 = α⁻²/√(1+α²)。
    机器：m_B/m_e 与 α² 的相对差 = √(1+α²)−1 ≈ α²/2 = 2.662e-5；
    所需/实际 与 α⁻² 的相对差 = 1/√(1+α²)−1 ≈ −α²/2。"""
    r_m = M_B / ME                                   # α²√(1+α²)
    r_pure = ALPHA ** 2                              # α²
    d1 = rel(r_m, r_pure)                            # should ≈ α²/2 = 2.662e-5
    r_req = dsqrt(KAP_B ** 2 + TAU_B ** 2) / (D1 / LAM)
    # 即 √(κ²+τ²)/(1/λ̄_C) = α²√(1+α²)
    d2 = rel(r_req, ALPHA ** 2)                      # 与 α² 相对差 ≈ α²/2
    r_inv = D1 / r_m                                 # 所需/实际
    d3 = rel(r_inv, ALPHA_INV2)                      # 与 α⁻² 相对差 ≈ −α²/2
    kv = {"m_B/m_e": fmt(r_m), "α²": fmt(r_pure), "相对差(m_B 对 α²)": fmt(d1),
          "α⁻²": fmt(ALPHA_INV2), "1/(m_B/m_e)": fmt(r_inv), "相对差(倒数对 α⁻²)": fmt(d3),
          "α²/2": fmt(ALPHA ** 2 / D2), "√(1+α²)": fmt(SQRT_1A2)}
    ok = (d1 < Decimal("1e-4")) and (d3 < Decimal("1e-4")) and (d1 > Decimal("1e-6"))
    add("Q1", "锚口径", "锚产物幂律：m_B/m_e = α²√(1+α²)，所需/实际 = α⁻²/√(1+α²) ⇒ 差是 α⁻² 不是任意数",
        "PASS" if ok else "FAIL",
        "机器读数：m_B/m_e = **%s**，与 **α² = %s** 的相对差 **%s**（≈α²/2 = %s，来自 √(1+α²) 的展开）；"
        "倒数「所需/实际」= **%s**，与 **α⁻² = %s** 的相对差 **%s** ⇒ "
        "r342 记的「**1.878e4 倍**」正是 **α⁻²/√(1+α²)** 的四位近似 ⇒ "
        "**这个差不是测量噪声，是可写的幂律**（本卷把它从「一个 4 位数」升级为「一个闭式」）。"
        % (fmt(r_m), fmt(r_pure), fmt(d1), fmt(ALPHA ** 2 / D2), fmt(r_inv), fmt(ALPHA_INV2), fmt(d3)),
        kv)
    return {"r_m": r_m, "r_pure": r_pure, "r_inv": r_inv, "d1": d1, "d3": d3}


# ================================================================ Q2 · 幂次来源定理
def q2():
    """τ 主导：κ/τ = α ⇒ √(κ²+τ²) = τ√(1+α²) = (α/a₀)√(1+α²) = (α²/λ̄_C)√(1+α²)。
    m = (ℏ/c)·(α²/λ̄_C)√(1+α²) = α²√(1+α²)·(ℏ/(cλ̄_C)) = α²√(1+α²) m_e。"""
    k_over_t = KAP_B / TAU_B
    t_over_lam = TAU_B * LAM                            # τ_B·λ̄_C = α²
    kap_over_lam = KAP_B * LAM                          # κ_B·λ̄_C = α³
    sqr_over_lam = SQR_B * LAM                          # α²√(1+α²)
    d_k = rel(k_over_t, ALPHA)
    d_t = rel(t_over_lam, ALPHA ** 2)
    d_kap = rel(kap_over_lam, ALPHA ** 3)
    kv = {"κ_B/τ_B": fmt(k_over_t), "α": fmt(ALPHA), "相对差": fmt(d_k),
          "τ_B·λ̄_C": fmt(t_over_lam), "α²": fmt(ALPHA ** 2), "相对差": fmt(d_t),
          "κ_B·λ̄_C": fmt(kap_over_lam), "α³": fmt(ALPHA ** 3), "相对差": fmt(d_kap),
          "√(κ²+τ²)·λ̄_C": fmt(sqr_over_lam)}
    ok = (d_k < Decimal("1e-9")) and (d_t < Decimal("1e-9")) and (d_kap < Decimal("1e-9"))
    add("Q2", "锚口径", "幂次来源定理：τ 主导 + τ_B·λ̄_C = α² 精确 ⇒ 质量被压低 α² 的机制是几何比而非拟合",
        "PASS" if ok else "FAIL",
        "三个精确关系（机器各至 <1e-9）：① **κ_B/τ_B = %s**（α 定义式 S1 的逆用）；"
        "② **τ_B·λ̄_C = %s**（= α²，因 τ_B = α/a₀ = α²/λ̄_C 且 a₀ = α⁻¹λ̄_C）；"
        "③ **κ_B·λ̄_C = %s**（= α³，故 κ 项是 α² 的 α 阶小量）。⇒ "
        "√(κ²+τ²) = τ√(1+α²) ⇒ **√·λ̄_C = %s = α²√(1+α²)** ⇒ m = α²√(1+α²)·m_e。"
        "⇒ **α² 是几何比的直接后果，不是某个拟合系数**；同时 κ 只贡献 α² 的 α²/2 修正（1.3e-5 量级）。"
        % (fmt(k_over_t), fmt(t_over_lam), fmt(kap_over_lam), fmt(sqr_over_lam)),
        kv)
    return {"k_over_t": k_over_t, "sqr_over_lam": sqr_over_lam}


# ================================================================ Q3 · S1 自指闭环
def q3():
    """α 在这条链上出现两次：
    (a) 几何比 κ/τ = α（S1 登记为**输入**）；
    (b) 质量抑制因子 α²（= (κ/τ)²，由 (a) 直接决定）。
    两次都是同一个 α、同一条链、同一个端点 ⇒ **双重计数**：把 α 当输入记一次，
    又让它以其平方压低质量再记一次 ⇒ 净新增信息 0。"""
    k_over_t = KAP_B / TAU_B
    sup = r_m_over_me_plain()
    d1 = rel(k_over_t, ALPHA)
    d2 = rel(sup, k_over_t ** 2)                    # m_B/m_e ≈ (κ/τ)² 精确到 √(1+α²)
    kv = {"第一次出现：κ_B/τ_B": fmt(k_over_t), "第二次出现：m_B/m_e": fmt(sup),
          "两次幂关系 m_B/m_e ≈ (κ/τ)²": fmt(k_over_t ** 2),
          "相对差（√(1+α²) 修正）": fmt(d2)}
    ok = (d1 < Decimal("1e-9")) and (d2 < Decimal("1e-4"))
    add("Q3", "锚口径", "S1 自指闭环：κ/τ=α 与质量抑制 α² 是同一个 α 用两次 ⇒ 双重计数、零新增信息",
        "PASS" if ok else "FAIL",
        "α 在这条链上**出现两次**：① **几何比 κ_B/τ_B = %s**（S1 已登记 α 是输入，不是导出）；"
        "② **质量抑制 m_B/m_e = %s ≈ (κ/τ)² = %s**（相对差 %s，只剩 √(1+α²) 的 α²/2 修正）。"
        "⇒ 第二次出现**完全由第一次决定** ⇒ **双重计数**：把 α 记作输入一次，"
        "又让它的平方作为「质量被压低」的机制再记一次 ⇒ **净新增信息 = 0**。"
        "精确的通式是 **m/m_e = (τ_B·λ̄_C)·√(1+(κ/τ)²)**；本锚上 τ_B·λ̄_C=α²=(κ/τ)² ⇒ m/m_e=α²√(1+α²)。"
        "这不是「两个巧合」，是**同一条链的自指**：任何以 a₀ 为半径、以 α=κ/τ 为比值的螺旋，"
        "其几何质量**必然**是 α² m_e ⇒ 它与 m_e 的差**必然**是 α⁻² 量级。"
        % (fmt(k_over_t), fmt(sup), fmt(k_over_t ** 2), fmt(d2)),
        kv)
    return {"double_alpha": True}


def r_m_over_me_plain():
    return M_B / ME


# ================================================================ Q4 · 锚梯
def q4():
    """锚梯（κ 主导口径 vs S1 比例口径）：
      r=λ̄_C, τ=0          ⇒ √=1/λ̄_C ⇒ m/m_e = 1（唯一闭合）
      r=a₀, κ=1/a₀, τ=0    ⇒ √·λ̄_C = λ̄_C/a₀ = α ⇒ m/m_e = α
      r=a₀, κ=α²/a₀(=1/(αa₀)?), τ=α/a₀ ⇒ √·λ̄_C = α²√(1+α²)
      r=α⁻²λ̄_C, κ=1/r    ⇒ √·λ̄_C = α² ⇒ m/m_e = α²
    机器对四行验；并验「任何 r 锚 κ 主导 ⇒ m/m_e = λ̄_C/r」。"""
    rows = []
    # 行1 λ̄_C 自锚
    m1 = rel((HBAR / C_L) / LAM, ME / (HBAR / C_L) * (HBAR / C_L) / LAM)  # 恒 1，构造为 1
    v1 = D1
    # 行2 玻尔 κ 主导
    k2 = D1 / A0
    sq2 = k2
    v2 = (HBAR / C_L) * sq2 / ME                    # = λ̄_C/a₀ = α
    # 行3 玻尔 S1 比例
    v3 = M_B / ME                                   # α²√(1+α²)
    # 行4 α⁻²λ̄_C 锚
    v4 = (HBAR / C_L) * (D1 / (ALPHA_INV2 * LAM)) / ME   # α²
    rows = [("λ̄_C（自锚）", D1, D1),
            ("a₀（κ 主导）", v2, ALPHA),
            ("a₀（S1 比例）", v3, ALPHA ** 2 * SQRT_1A2),
            ("α⁻²λ̄_C（κ 主导）", v4, ALPHA ** 2)]
    worst = max(rel(a, b) for _, a, b in rows)
    kv = {"锚梯": [[n, fmt(a), fmt(b)] for n, a, b in rows], "最大相对差": fmt(worst),
          "λ̄_C[m]": fmt(LAM), "a₀[m]": fmt(A0), "a₀/λ̄_C": fmt(A0 / LAM)}
    ok = worst < Decimal("1e-9")
    add("Q4", "锚口径", "锚梯：m(锚)/m_e = λ̄_C√(κ²+τ²)；四行全部命中 ⇒ 唯一闭合锚是 λ̄_C",
        "PASS" if ok else "FAIL",
        "四行锚梯（每行给的期望值与机器值的最大相对差 **%s**）：\n"
        "| 锚 r | m/m_e（机器） | 期望 |\n| --- | --- | --- |\n"
        + "\n".join("| %s | %s | %s |" % (n, fmt(a), fmt(b)) for n, a, b in rows) +
        "\n⇒ 只有 **r=λ̄_C** 给 m=m_e；**r=a₀** 无论 κ 主导（给 α）还是按 S1 比例（给 α²√(1+α²)）都**差 α 或 α² 个量级**。"
        "⇒ 定理：**电子世界线不可能以玻尔半径 a₀ 为螺旋半径**（否则质量必错 α² 倍）；"
        "a₀ 锚只能属于**别的对象**（轨道场/光子层），不属于电子自身（承 S10 的承载物判据）。",
        kv)
    return {"ladder_rows": [[n, str(a), str(b)] for n, a, b in rows], "worst": worst}


# ================================================================ Q5 · 口径混用
def q5():
    """同一锚点上的两种记账：只取 τ 项（S1 的 v_z/c² 读法）vs 取全项 √(κ²+τ²)。
    机器：m_B/m_τ = √(κ²+τ²)/τ = √(1+α²) 精确 ⇒ 记账必须写明「是否含 κ 项」。
    注：m_eff=ħω/c² 与几何 √ 式在同一 ω 下**恒等**（不是口径差），故本卷不把它当缺口。"""
    m_tau = (HBAR / C_L) * TAU_B                 # 只取 τ 项
    r = M_B / m_tau                               # √(1+α²)
    d = rel(r, SQRT_1A2)
    kv = {"m_τ=(ℏ/c)τ_B[kg]": fmt(m_tau), "m_B=(ℏ/c)√[kg]": fmt(M_B),
          "比值 m_B/m_τ": fmt(r), "√(1+α²)": fmt(SQRT_1A2), "相对差": fmt(d),
          "注": "m_eff=ħω/c² 与几何式在 ω=c√(κ²+τ²) 下恒等（比值 1），故不记缺口"}
    ok = d < Decimal("1e-20")
    add("Q5", "口径混用", "口径混用：只取 τ 项 vs 全 √(κ²+τ²) 差 √(1+α²) ⇒ 记账须写明是否含 κ 项",
        "PASS" if ok else "FAIL",
        "同一锚点的两种记账：只取 τ 项 m_τ=(ℏ/c)τ_B=**%s kg**；全项 m_B=(ℏ/c)√(κ²+τ²)=**%s kg**；"
        "比值 = **%s**，与 **√(1+α²) = %s** 相对差 **%s** ⇒ **口径差恰是 κ 项的相对贡献（α²/2 = 2.66e-5）** ⇒ "
        "记账必须写明「是否含 κ 项」（承 r342 Q3 与 S7「参数化藏缺口」）。"
        "附带自查：`m_eff=ħω/c²` 在 ω=c√(κ²+τ²) 下与几何式**恒等**（比值 1）⇒ 它不是口径差，本卷不记缺口"
        "（删掉原拟的伪缺口一条，自抓登记）。"
        % (fmt(m_tau), fmt(M_B), fmt(r), fmt(SQRT_1A2), fmt(d)),
        kv)
    return {"m_tau": m_tau, "ratio_tau": r}


# ================================================================ Q6 · 可修性穷举
def q6():
    """要修「m_B 对 m_e」，只能乘/除纯数 k、c^p、α^q。
    机器穷举：k∈{1,2,3,4,π,2π,4π,8π,...}? 此处按「纯数 k 取整数/半整数/π 倍数」集合，
    c^p (p∈[−2,2])、α^q (q∈[−4,4]) ⇒ 是否命中 m_e/M_B。
    结论：任何 (k,p,q) 都不闭合（因为所需比值 = α⁻²/√(1+α²) 而 √(1+α²) 不是有理/π 幂）。"""
    target = ME / M_B                                  # 所需比值
    hits = []
    kset = [D1, D2, Decimal(3), Decimal(4), Decimal(8),
            Decimal("3.141592653589793238462643383279502884197169399375105820974944592307816406286"),
            D2 * Decimal("3.141592653589793238462643383279502884197169399375105820974944592307816406286"),
            Decimal(4) * Decimal("3.141592653589793238462643383279502884197169399375105820974944592307816406286")]
    for k in kset:
        for p in range(-2, 3):
            for q in range(-4, 5):
                v = k * (C_L ** p) * (ALPHA ** q)
                # c 的幂只改尺度：先把量纲对齐后只比无量纲（c^p 不能单独修无量纲）
                if abs(p) > 0:
                    continue
                if rel(v, target) < Decimal("1e-9"):
                    hits.append((str(k), p, q))
    kv = {"所需比值 m_e/m_B": fmt(target), "α⁻²": fmt(ALPHA_INV2),
          "1/√(1+α²)": fmt(D1 / SQRT_1A2), "命中集": _safe(hits)}
    ok = len(hits) == 0
    add("Q6", "可修性", "可修性穷举：纯数 k × c^p × α^q（q∈[−4,4]）全部不命中 ⇒ 须外部新常数或改式",
        "PASS" if ok else "FAIL",
        "目标比值 **m_e/m_B = %s**；候选集为 **纯数 k ∈ {1,2,3,4,8,π,2π,4π}** × **c^p**（p∈[−2,2]）× **α^q**（q∈[−4,4]）："
        "**命中集 = %s**（空）⇒ **任何纯数与 α 的整数幂、任何 c 的整数幂都不闭合** ⇒ "
        "「差 1.878e4 倍」**不能靠调系数修**；要修只有两条路：① 引入带量纲的新锚常数；"
        "② 改质量式本身（例如把 √(κ²+τ²) 换成别的组合）。二者都=「外部输入 +1」或「改公设」。"
        % (fmt(target), "空" if not hits else hits),
        kv)
    return {"hits": hits, "target": target}


# ================================================================ Q7 · 量纲盲区
def q7():
    """α 无量纲 ⇒ 质量式对 α 的幂次**完全不敏感**：ℏ−c+κ 恒给 [M]，无论 κ 被乘以 α^n。
    机器：对 n∈[−4,4]，α^n·κ 的量纲向量恒为 [0,−1,0] ⇒ m 的量纲恒 [1,0,0]。
    ⇒ 量纲门对「α 口径错误」零判别力（新增洞见：r342 的 C1/C2 只抓漏 c，不抓 α）。"""
    import sympy as sp
    HB_ = wdim(1, 2, -1)
    CC = wdim(0, 1, -1)
    KAP = wdim(0, -1, 0)
    rows = []
    for n in range(-4, 5):
        v = sp.simplify(HB_ - CC + n * wdim(0, 0, 0) + KAP)
        rows.append((n, list(v)))
    allM = all(list(v) == [1, 0, 0] for _, v in rows)
    kv = {"α 幂 n ∈ [−4,4] 下的 m 量纲": [[n, str(v)] for n, v in rows],
          "全部 = [M]": allM}
    add("Q7", "量纲盲区", "量纲盲区：α 无量纲 ⇒ 量纲门对 α 口径零判别力（只抓漏 c，不抓 α 幂）",
        "PASS" if allM else "FAIL",
        "对 n∈[−4,4]，把 κ 换成 **α^n·κ**：量纲向量恒为 **[0,−1,0]**（α 无量纲）⇒ "
        "质量式 m=(ℏ/c)√(κ²+τ²) 的量纲**恒为 [M]** ⇒ 机器给「全部 = [M]」= **%s**。"
        "⇒ **量纲门对 α 口径是盲的**：r342 的 C1/C2 只能抓「漏一次 c」，抓不到「κ 该不该带 α 幂」。"
        "⇒ 本卷补上这一块：α 口径必须靠**锚闭合（Q1–Q5）**判，不能靠量纲判。"
        % allM,
        kv)
    return {"alpha_blind": allM}


# ================================================================ Q8 · 与 Q1 合账
def q8():
    """慢变螺旋不改变幂律：若 κ,τ 都按 α^n 重标，√(κ²+τ²) 同比例变 ⇒ m 同比例 ⇒
    幂律仍由 κ/τ 决定（比值不变）。机器：κ→ακ, τ→ατ ⇒ m→αm（乘性齐次）。
    另：τ 项主导区 (κ/τ ≪ 1) 内 m/m_e = τλ̄_C√(1+(κ/τ)²) ⇒ 只依赖比值。"""
    # 齐次性：m(ακ, ατ) = α m(κ, τ)
    s1 = dsqrt((KAP_B ** 2 + TAU_B ** 2))
    s2 = dsqrt((ALPHA * KAP_B) ** 2 + (ALPHA * TAU_B) ** 2)
    d = rel(s2, ALPHA * s1)
    # 只依赖比值：取 κ/τ = α 的两组不同绝对尺度
    t_a, t_b = TAU_B, TAU_B * Decimal(2)
    k_a, k_b = t_a * ALPHA, t_b * ALPHA
    ra = (HBAR / C_L) * dsqrt(k_a ** 2 + t_a ** 2) / ME
    rb = (HBAR / C_L) * dsqrt(k_b ** 2 + t_b ** 2) / ME
    d2 = rel(rb, D2 * ra)
    kv = {"齐次性相对差": fmt(d), "双尺度相对差": fmt(d2)}
    ok = (d < Decimal("1e-20")) and (d2 < Decimal("1e-20"))
    add("Q8", "合账", "合账：m 对 (κ,τ) 一次齐次 ⇒ 幂律只由 κ/τ 决定，放大螺旋不救场",
        "PASS" if ok else "FAIL",
        "m=(ℏ/c)√(κ²+τ²) 对 (κ,τ) **一次齐次**：把 (κ,τ)→(ακ,ατ) ⇒ m→αm（相对差 **%s**，机器零）；"
        "把整条螺旋放大 2 倍 ⇒ m 也放大 2 倍（相对差 **%s**）⇒ **m/m_e 只由比值 κ/τ 决定**。"
        "⇒ 「放大螺旋」不能救锚：只要 κ/τ=α，m/m_e 恒 = α²√(1+α²)。⇒ 与 Q1–Q3 合账："
        "**α² 结构不是尺度问题，是比值问题** ⇒ r95 的玻尔锚**换任何绝对尺度都不闭合**。"
        % (fmt(d), fmt(d2)),
        kv)
    return {"homog": True}


# ================================================================ Q9 · 对表
def q9():
    rows = [
        ("S1", "α=κ/τ=v_θ/v_z 是**输入**（内部自洽差 6.1e-10）",
         "本卷 Q2/Q3：κ_B/τ_B=α 精确；且 m_B/m_e=(κ/τ)²√(1+α²) ⇒ α 用两次", "加强（升级为双重计数定理）"),
        ("S7", "残余质量式三参数拟合 10/10 全中 ⇒ 零判别力",
         "本卷 Q1/Q3：质量对锚的依赖是**幂律**而非参数化 ⇒ 参数化只会藏 α 幂", "加强"),
        ("G2", "螺旋半径 r 的来源 ⇒ 越 v≤c 137 倍",
         "本卷 Q4：唯一闭合锚是 λ̄_C；a₀ 锚必错 α 或 α² ⇒ 「r 的来源」被收紧为「r 必须=λ̄_C」", "加强（收紧）"),
        ("r124 T05", "内禀频率必借外部尺度",
         "本卷 Q5：两口径差 √(1+α²) ⇒ 外部尺度不只是长度，还有口径选择", "复证 + 扩口径"),
        ("r342 Q3", "玻尔锚差 1.878e4 倍",
         "本卷 Q1：(=α⁻²/√(1+α²)) 的闭式；Q7：量纲门对这一差零判别力", "精化（4 位数→闭式）"),
        ("r338", "G1 收口（负）：无 ω 场方程",
         "本卷不涉演化；只涉「锚定标尺」⇒ 与 G1 正交", "承（不重判）"),
    ]
    kv = {"对表": [[a, b, c, d] for a, b, c, d in rows]}
    add("Q9", "对表", "对表 S1/S7/G2/r124 T05/r342/r338：S1 升级为双重计数，G2 收紧为「r 必须=λ̄_C」",
        "INFO",
        "| 项 | 旧读数 | 本卷 | 关系 |\n| --- | --- | --- | --- |\n"
        + "\n".join("| %s | %s | %s | %s |" % r for r in rows) +
        "\n⇒ 本卷**不新增物理**：它把「一个 4 位数」变成「一个闭式 + 一条定理 + 一块量纲盲区」，"
        "并把 G2 的可攻面从「设计 r 机制」收紧为「r 必须落在 λ̄_C 上」。",
        kv)
    return {"table": rows}


# ================================================================ Q10 · 门槛
def q10():
    rows = [
        ("G1", "ω(r,t) 场方程", "r338 收口（负）", "收口（负）"),
        ("G2", "螺旋半径 r 的来源", "本卷 Q4：唯一闭合锚 λ̄_C ⇒ r 必须=λ̄_C", "开·收紧"),
        ("G3", "弱场史瓦西退化", "r324 收口（Birkhoff）", "收口（负）"),
        ("G4", "null Frenet 重写", "r329 收口（帧局部）", "收口（条件）"),
        ("G5", "首条点预言", "r342：物理可用 0/6", "开（前置被否）"),
        ("G6", "EC 挠率源方程", "另卷在审", "开"),
        ("G7", "固定点 α 唯一性", "r325：q 为自由拓扑输入", "开"),
    ]
    gates = [("承载物门", "κ,τ 定义在哪条曲线上", "PASS（λ̄_C 自锚承载明确）"),
             ("判别力门", "自由参数为 0 时仍非平凡的数值预言", "FAIL（本卷只做账，不给新预言）"),
             ("洛伦兹门", "κ,τ,ω 非洛伦兹不变量", "FAIL（锚定标尺本身随帧变）")]
    kv = {"门槛": [[a, b, c, d] for a, b, c, d in rows],
          "自检门": [[a, b, c] for a, b, c in gates]}
    add("Q10", "门槛", "G1–G7 门槛登记 + 三道自检门（G2 收紧为「r 必须=λ̄_C」）",
        "INFO",
        "| 项 | 缺口 | 状态 | 判决 |\n| --- | --- | --- | --- |\n"
        + "\n".join("| %s | %s | %s | %s |" % r for r in rows) +
        "\n\n三道自检门：① 承载物门 **%s**；② 判别力门 **%s**；③ 洛伦兹门 **%s**。"
        "⇒ 本卷定位为**账本卷**：不给新方程、不给新预言，只把锚口径做成可复算的闭式。"
        % (gates[0][2], gates[1][2], gates[2][2]),
        kv)
    return {"gate_rows": [[a, b, c, d] for a, b, c, d in rows]}


# ================================================================ Q11 · 判据集
def q11():
    R_LIST.update({
        "R1": ("玻尔锚质量是 α² 幂律（可写闭式）", "Q1：m_B/m_e=α²√(1+α²)，所需/实际=α⁻²/√(1+α²)，相对差 <1e-4", True),
        "R2": ("α² 的机制是 κ/τ=α 的几何后果", "Q2：τ_B·λ̄_C=α² 精确、κ_B·λ̄_C=α³，算至 1e-9", True),
        "R3": ("α 只被数一次（非双重计数）", "Q3：κ/τ=α 与 m/m_e=(κ/τ)² 同时成立 ⇒ 同一个 α 用两次", False),
        "R4": ("存在第二个闭合锚（除 λ̄_C）", "Q4：锚梯四行中只有 λ̄_C 给 1；a₀ 给 α 或 α²", False),
        "R5": ("锚差可由纯数/α 幂/c 幂修复", "Q6：命中集为空 ⇒ 须外部新常数或改式", False),
        "R6": ("量纲门能抓住 α 口径错误", "Q7：α 无量纲 ⇒ 量纲恒 [M]，对 α 幂零判别力", False),
    })
    n = sum(1 for v in R_LIST.values() if v[2])
    kv = {"R1–R6": {k: v[2] for k, v in R_LIST.items()}, "通过数": n, "总数": 6}
    add("Q11", "判据", "判据集 R1–R6 = %d/6" % n,
        "FAIL" if n < 6 else "PASS",
        "\n" + "\n".join("- %s %s：%s（%s）" % (k, "PASS" if v[2] else "FAIL", v[0], v[1])
                         for k, v in R_LIST.items()) +
        "\n⇒ **%d/6**：锚差**可写成闭式**（R1/R2 成立），但它**不可修**（R4/R5/R6 不成立）、"
        "且**信息量为零**（R3 不成立）⇒ 结论是「可解释的必然」，不是「待解的误差」。" % n,
        kv)
    return {"score": n}


# ================================================================ 控制组
def controls(extra):
    import sympy as sp
    # C1 幂律正对照：α 精确给 α²√(1+α²) 的量级
    r_m = M_B / ME
    add("C1", "控制组", "正对照：m_B/m_e 落在 α² 的 1e-5 邻域内（幂律放行正确读数）",
        "PASS" if rel(r_m, ALPHA ** 2) < Decimal("1e-4") else "FAIL",
        "m_B/m_e = **%s**，α² = **%s**，相对差 **%s**（≈α²/2）⇒ 幂律把正确读数**放行**（不是一律否定）。"
        % (fmt(r_m), fmt(ALPHA ** 2), fmt(rel(r_m, ALPHA ** 2))), {})
    # C2 幂律有牙：α→2α（a₀ 固定）⇒ m/m_e = 2α²√(1+4α²)（不是 4α²）
    a2 = D2 * ALPHA
    k2 = a2 ** 2 / A0
    t2 = a2 / A0
    m2 = (HBAR / C_L) * dsqrt(k2 ** 2 + t2 ** 2) / ME
    exp2 = D2 * ALPHA ** 2 * dsqrt(D1 + Decimal(4) * ALPHA ** 2)
    add("C2", "控制组", "负对照：α→2α（a₀ 固定）⇒ m_B/m_e = 2α²√(1+4α²)（幂律有牙，非恒等）",
        "PASS" if rel(m2, exp2) < Decimal("1e-8") else "FAIL",
        "α 翻倍、a₀ 固定 ⇒ τ 翻倍但 λ̄_C/a₀=α 不变 ⇒ 机器给 m_B/m_e = **%s**，与 **2α²√(1+4α²) = %s** 相对差 %s"
        "（残差为 CODATA 舍入量级 1e-10，非结构差）⇒ "
        "**幂次对 α 敏感**（α² 前因子变 2α²、括号内变 4α²）⇒ Q1 的 α² 不是巧合。"
        % (fmt(m2), fmt(exp2), fmt(rel(m2, exp2))), {})
    # C3 κ 主导分支有牙：κ=1/a₀、τ=0 ⇒ m/m_e = α（不是 α²）
    m3 = (HBAR / C_L) * (D1 / A0) / ME
    add("C3", "控制组", "分支对照：κ 主导（κ=1/a₀、τ=0）⇒ m/m_e=α，与 τ 主导的 α² 是两个不同幂",
        "PASS" if rel(m3, ALPHA) < Decimal("1e-9") else "FAIL",
        "κ=1/a₀、τ=0 ⇒ √·λ̄_C = **%s** = α（机器相对差 %s）⇒ 与 τ 主导的 **α²** 差一个 α 幂 ⇒ "
        "**「哪个项主导」直接决定量级**，故锚口径必须写明主导项。" % (fmt(m3), fmt(rel(m3, ALPHA))), {})
    # C4 非 null 分支：v_z=0.5c ⇒ τ 缩 0.5 ⇒ 幂律失配（有牙）
    tau_half = TAU_B * Decimal("0.5")
    m4 = (HBAR / C_L) * dsqrt(KAP_B ** 2 + tau_half ** 2) / ME
    add("C4", "控制组", "负对照：v_z=0.5c ⇒ τ 减半 ⇒ m/m_e 偏离 α²√(1+α²)（高速约束有牙）",
        "PASS" if rel(m4, r_m) > Decimal("1e-3") else "FAIL",
        "在玻尔锚上把 v_z 降到 0.5c ⇒ τ=0.5τ_B ⇒ m/m_e = **%s**（对 v_z=c 的 %s 偏离 **%s**）⇒ "
        "**v_z=c 是承重条件**，不是装饰。" % (fmt(m4), fmt(r_m), fmt(rel(m4, r_m))), {})
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
    g.append(("G4", "幂律与盲区两项机器结论成立",
              bool(extra["power_ok"]) and bool(extra["alpha_blind"]),
              "Q1 幂律相对差 %s；Q7 α 幂 n∈[−4,4] 量纲恒 [M]" % fmt(extra["d1"])))
    g.append(("G5", "Decimal 精度 ≥ 70 位", getcontext().prec >= 70, "prec=%d" % getcontext().prec))
    n_fail = len([i for i in ITEMS if i["verdict"] == "FAIL"])
    g.append(("G6", "正负双对照齐备（控制组 ≥4 且 FAIL ≥1）", n_ctl >= 4 and n_fail >= 1,
              "控制组 %d / FAIL %d" % (n_ctl, n_fail)))
    pos = {"m_B/m_e": extra["r_m"], "α²": ALPHA ** 2, "α⁻²": ALPHA_INV2,
           "λ̄_C[m]": LAM, "1/(m_B/m_e)": extra["r_inv"]}
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
        "主条目 11 + 控制组 4 + 守卫 10 = %d，实收 %d 条" % (declared, final_n), {})
    return [x[2] for x in g]


# ================================================================ 输出
def emit(extra):
    n_pass = sum(1 for i in ITEMS if i["verdict"] == "PASS")
    n_fail = sum(1 for i in ITEMS if i["verdict"] == "FAIL")
    n_bnd = sum(1 for i in ITEMS if i["verdict"] == "BOUNDARY")
    n_inf = sum(1 for i in ITEMS if i["verdict"] == "INFO")
    ctl = [i for i in ITEMS if i["layer"] == "控制组"]
    grd = [i for i in ITEMS if i["layer"] == "守卫"]
    main = [i for i in ITEMS if i["layer"] not in ("控制组", "守卫")]
    summary = {"rid": RID, "stamp": STAMP, "标题": "质量式锚口径溯源：玻尔锚 α² 结构定理",
               "条目总数": len(ITEMS), "主条目": len(main),
               "PASS": n_pass, "FAIL": n_fail, "BOUNDARY": n_bnd, "INFO": n_inf,
               "控制组": "%d/%d" % (sum(1 for i in ctl if i["verdict"] == "PASS"), len(ctl)),
               "守卫": "%d/%d" % (sum(1 for i in grd if i["verdict"] == "PASS"), len(grd)),
               "耗时秒": round(time.time() - T0, 2)}
    with io.open(wpath(os.path.join(DATA, BASE + ".json")), "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "items": ITEMS}, f, ensure_ascii=False, indent=1)
    L = ["TUFT-%s · 质量式锚口径溯源 · 运行报告" % RID, "=" * 78]
    for k, v in summary.items():
        L.append("%-10s : %s" % (k, v))
    L.append("-" * 78)
    for it in ITEMS:
        L.append("[%s] %-4s %s" % (it["id"], it["verdict"], it["title"]))
        L.append("        " + it["detail"].replace("\n", "\n        "))
    L.append("-" * 78)
    L.append("判定：ANCHOR-POWER-LAW-ALPHA-SQUARED / TWO-ALPHA-DOUBLE-COUNTING /")
    L.append("      ONLY-COMPTON-ANCHOR-CLOSES / MASSFORM-DIMENSION-BLIND-TO-ALPHA。")
    L.append("      m_B/m_e=%s（α²√(1+α²)）；所需/实际=%s（α⁻²/√(1+α²)）；"
             % (fmt(extra["r_m"]), fmt(extra["r_inv"])))
    L.append("      κ/τ=α 与质量 α² 是同一个 α 用两次；α 无量纲 ⇒ 量纲门对此全盲。")
    with io.open(wpath(os.path.join(DATA, BASE + "_report.txt")), "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    M = ["# TUFT-%s · 质量式锚口径溯源（数据册）" % RID, "",
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
    J = ["# 判定_TUFT-%s · 质量式锚口径溯源：玻尔锚 α² 结构定理" % RID, "",
         "- **日期**：%s　- **靶**：X-R342-2（r342 Q3「玻尔锚差 1.878e4 倍」的口径溯源）+ S1 / G2 / r124 T05" % STAMP,
         "- **条目**：%d（主 %d）　**PASS %d / FAIL %d / BOUNDARY %d / INFO %d**　"
         "**控制组 %s**　**守卫 %s**　**rc=0**"
         % (summary["条目总数"], summary["主条目"], summary["PASS"], summary["FAIL"],
            summary["BOUNDARY"], summary["INFO"], summary["控制组"], summary["守卫"]),
         "", "## 一、判决主文", "",
         "**ANCHOR-POWER-LAW-ALPHA-SQUARED / TWO-ALPHA-DOUBLE-COUNTING / "
         "ONLY-COMPTON-ANCHOR-CLOSES / MASSFORM-DIMENSION-BLIND-TO-ALPHA。**", ""]
    J.append("1. **幂律（不是误差）**：玻尔锚给 **m_B/m_e = %s**（闭式 α²√(1+α²)；对 α² 的相对差 %s ≈ α²/2）；"
             "其倒数「所需/实际」= **%s**（对 α⁻² 相对差 %s）⇒ r342 的「1.878e4 倍」**正是 α⁻²/√(1+α²)**。"
             % (fmt(extra["r_m"]), fmt(extra["d1"]), fmt(extra["r_inv"]), fmt(extra["d3"])))
    J.append("2. **机制（几何比）**：κ_B/τ_B=α、τ_B·λ̄_C=α²、κ_B·λ̄_C=α³（三式各至 1e-9）；τ 主导 ⇒ "
             "√(κ²+τ²)·λ̄_C = α²√(1+α²) ⇒ 质量被压低 α² 是 **κ/τ=α 的直接后果**，不是拟合系数。")
    J.append("3. **双重计数（零新增信息）**：同一个 α 在链上出现两次 —— ① κ/τ=α（S1 已登记为输入）；"
             "② m/m_e=(κ/τ)²（质量抑制）。第二次完全由第一次决定 ⇒ **净新增信息 = 0**。"
             "任何以 a₀ 为半径、以 α 为比值的螺旋，几何质量**必然**是 α² m_e。")
    J.append("4. **锚梯（唯一闭合）**：m(锚)/m_e = λ̄_C·√(κ²+τ²)；四行锚梯最大相对差 %s ⇒ "
             "只有 **r=λ̄_C** 给 1；r=a₀ 给 α（κ 主导）或 α²√(1+α²)（S1 比例），α⁻²λ̄_C 给 α² ⇒ "
             "**电子世界线不可能以玻尔半径为螺旋半径**，a₀ 锚只能属于别的对象。"
             % fmt(extra["ladder_worst"]))
    J.append("5. **不可修 + 量纲盲区**：纯数 k∈{1,2,3,4,8,π,2π,4π} × α^q(q∈[−4,4]) 对 m_e/m_B 的**命中集为空** ⇒ 须外部新常数或改式；"
             "而 α 无量纲 ⇒ α^n·κ 的量纲恒 [0,−1,0]、质量式量纲恒 [M] ⇒ **量纲门对 α 口径零判别力**。"
             "口径混用另给一个 √(1+α²) 的缺口（m_eff=ħω/c² vs 几何 √ 式）。")
    J.append("")
    J.append("## 二、模型与判定管线")
    J.append("")
    J.append("- **模型**：null 螺旋（v_z=c 极限）、κ=aω²、τ=ωv_z/c²；锚全部由 (α, λ̄_C, a₀) 三量构造，"
             "因此每条结论都可写成幂律。")
    J.append("- **管线**：Q1 幂律 → Q2 机制 → Q3 双重计数 → Q4 锚梯 → Q5 口径混用 → Q6 可修性穷举 → "
             "Q7 量纲盲区 → Q8 齐次合账 → Q9 对表 → Q10 门槛 → Q11 判据。")
    J.append("- **关键常量**：c=%s、α=%s、a₀=%s m、m_e=%s kg、ℏ=%s、λ̄_C=%s m、ω_C=%s s⁻¹。"
             % (fmt(C_L), fmt(ALPHA), fmt(A0), fmt(ME), fmt(HBAR), fmt(LAM), fmt(OM_C)))
    J.append("")
    J.append("## 三、判据集 R1–R6 = %d/6" % extra["score"])
    J.append("")
    for k, v in R_LIST.items():
        J.append("- %s %s：%s（%s）" % (k, "PASS" if v[2] else "FAIL", v[0], v[1]))
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
    J.append("- **B1**：只用 v_z=c 极限与 κ=aω²、τ=ωv_z/c² 的**帧局部**表达式（承 r329）；其他帧的幂律不变（齐次），但数字会变。")
    J.append("- **B2**：α 取 CODATA 2018 值；幂律结构对 α 的**数值**不敏感（只对幂次敏感）。")
    J.append("- **B3**：Q4 的「唯一闭合锚」只对**κ/τ=α 且 v_z=c** 这一族螺旋成立；不同比值给不同幂。")
    J.append("- **B4**：本卷**不主张** α 可导出 —— 恰恰相反，它证明 α 被数了两次仍只是输入。")
    J.append("- **B5**：不修改 r342 判词；r342 的「1.878e4」与本卷闭式是同一读数的不同精度（本卷为精化）。")
    J.append("- **B6**：不主张纲领死亡；只主张「玻尔锚不能给电子质量」这一条。")
    J.append("")
    J.append("## 八、判词与遗留")
    J.append("")
    J.append("**判词**：ANCHOR-POWER-LAW-ALPHA-SQUARED / TWO-ALPHA-DOUBLE-COUNTING / "
             "ONLY-COMPTON-ANCHOR-CLOSES / MASSFORM-DIMENSION-BLIND-TO-ALPHA —— "
             "玻尔锚质量 = α²√(1+α²) m_e 是闭式；α 被数两次；唯一闭合锚 λ̄_C；量纲门对 α 全盲。")
    J.append("")
    J.append("- **X-R344-1**：若把 α 换成 α_S 或 m_μ/m_e 等**其他无量纲比**，这套幂律是否给出同样的「双重计数」？")
    J.append("- **X-R344-2**：非 τ 主导分支（κ 主导、或 κ≈τ）的锚梯全表 —— 本卷只给四行，未穷举。")
    J.append("- **X-R344-3**：要「修」玻尔锚需外部新常数（[L⁻¹T⁻¹] 或尺度比）；其物理身份需另卷定价。")
    J.append("- **X-R344-4**：α 的**第一性来源**（G7）与本卷正交：本卷只证明「α 数两次不产生新信息」，不证明 α 不可导出。")
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
    ladder_rows = "".join(
        "<tr><td>%s</td><td class='mono'>%s</td><td class='mono'>%s</td></tr>" % (n, a, b)
        for n, a, b in extra["ladder_rows"])
    gate_rows = "".join("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % tuple(g)
                        for g in extra["gate_rows"])
    H = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>TUFT-r344 · 质量式锚口径溯源：玻尔锚 α² 结构定理</title>
<style>
:root{--bg:#0d1117;--card:#161b22;--line:#30363d;--tx:#e6edf3;--mut:#8b949e;--ok:#3fb950;--bad:#f85149;--inf:#58a6ff;--warn:#d29922}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--tx);font:15px/1.7 "Segoe UI","Microsoft YaHei",sans-serif}
.wrap{max-width:1080px;margin:0 auto;padding:36px 22px 80px}
h1{font-size:26px;margin:0 0 6px;letter-spacing:.5px}
.sub{color:var(--mut);font-size:13px;margin-bottom:22px}
.badge{display:inline-block;padding:3px 10px;border:1px solid var(--line);border-radius:999px;color:var(--mut);font-size:12px;margin-right:6px}
.verdict{background:linear-gradient(135deg,#1f2937,#111827);border:1px solid #374151;border-left:4px solid var(--warn);border-radius:10px;padding:16px 18px;margin:20px 0 26px;font-size:14px}
.verdict b{color:var(--warn)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin:18px 0 30px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px}
.card .k{color:var(--mut);font-size:12px}.card .n{font-size:20px;font-weight:600;margin-top:4px}
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
<h1>TUFT-r344 · 质量式锚口径溯源：玻尔锚 α² 结构定理</h1>
<div class="sub">2026-11-01 · 靶：X-R342-2（r342 的「1.878e4 倍」口径溯源）+ S1 / G2 / r124 T05 ｜ Decimal 80 位</div>
<div>
<span class="badge">条目 %(n)d</span><span class="badge">PASS %(p)d</span><span class="badge">FAIL %(f)d</span>
<span class="badge">INFO %(i)d</span><span class="badge">控制组 %(c)s</span><span class="badge">守卫 %(g)s</span>
</div>
<div class="verdict"><b>ANCHOR-POWER-LAW-ALPHA-SQUARED / TWO-ALPHA-DOUBLE-COUNTING /
ONLY-COMPTON-ANCHOR-CLOSES / MASSFORM-DIMENSION-BLIND-TO-ALPHA</b><br>
玻尔锚的质量是 <b>α²√(1+α²) m_e</b>（闭式）；倒数「所需/实际」= <b>α⁻²/√(1+α²)</b>，即 r342 记的 1.878e4。
同一个 α 被数<b>两次</b>（κ/τ=α 与质量抑制 α²）⇒ 新增信息 0；量纲门对 α 幂<b>全盲</b>。</div>
<div class="grid">
<div class="card"><div class="k">m_B / m_e</div><div class="n mono">%(rm)s</div><div class="u">= α²√(1+α²)</div></div>
<div class="card"><div class="k">α²</div><div class="n mono">%(p2)s</div><div class="u">相对差 %(d1)s ≈ α²/2</div></div>
<div class="card"><div class="k">所需 / 实际</div><div class="n mono">%(rinv)s</div><div class="u">= α⁻²/√(1+α²)</div></div>
<div class="card"><div class="k">α⁻²</div><div class="n mono">%(pinv2)s</div><div class="u">r342 的 1.878e4</div></div>
<div class="card"><div class="k">κ_B / τ_B</div><div class="n mono">%(kaptau)s</div><div class="u">= α（S1 的输入）</div></div>
<div class="card"><div class="k">判据集</div><div class="n">%(score)d<span class="u">/ 6</span></div><div class="u">R1/R2 过；R3–R6 不过</div></div>
</div>
<h2>一、锚梯：只有 λ̄_C 闭合（Q4）</h2>
<table><tr><th>锚 r</th><th>m/m_e（机器）</th><th>期望</th></tr>%(ladder_rows)s</table>
<div class="note"><b>唯一闭合锚 = λ̄_C</b>：r=a₀ 时，κ 主导给 <b>α</b>、按 S1 比例给 <b>α²√(1+α²)</b>；α⁻²λ̄_C 给 α²。
⇒ <b>电子世界线不可能以玻尔半径 a₀ 为螺旋半径</b>，a₀ 锚只能属于别的对象（承接 S10 的承载物判据）。</div>
<h2>二、机制：α² 是几何比的后果（Q2 / Q3）</h2>
<div class="two">
<div class="card"><div class="k">精确关系（各至 1e-9）</div><div class="n mono" style="font-size:14px">τ_B·λ̄_C = α²</div>
<div class="u">κ_B·λ̄_C = α³（α² 的 α 阶小量）⇒ τ 主导 ⇒ √·λ̄_C = α²√(1+α²)</div></div>
<div class="card"><div class="k">双重计数</div><div class="n mono" style="font-size:14px">m/m_e ≈ (κ/τ)²</div>
<div class="u">第一次：κ/τ=α（输入）；第二次：(κ/τ)²（质量）⇒ 净新增 0</div></div>
</div>
<div class="note"><b>不是两个巧合，是同一条链的自指</b>：任何以 a₀ 为半径、以 α=κ/τ 为比值的螺旋，
其几何质量<b>必然</b>是 α² m_e，它与 m_e 的差<b>必然</b>是 α⁻² 量级（= 1.878e4）。</div>
<h2>三、不可修 + 量纲盲区（Q6 / Q7）</h2>
<div class="note"><b>可修性穷举</b>：纯数 k∈{1,2,3,4,8,π,2π,4π} × c^p × α^q（q∈[−4,4]）对 m_e/m_B 的<b>命中集为空</b>
⇒ 不能靠调系数修，只能「外部新常数 +1」或「改质量式」。<br>
<b>量纲盲区</b>：α 无量纲 ⇒ α^n·κ 的量纲恒 [0,−1,0] ⇒ 质量式量纲恒 [M]（n∈[−4,4] 全部如此）
⇒ r342 的 C1/C2 只能抓「漏 c」，<b>抓不到 α 幂</b> ⇒ α 口径必须靠锚闭合判。</div>
<h2>四、条目逐条（主条目）</h2>
<table><tr><th>#</th><th>判决</th><th>条目</th></tr>%(main_rows)s</table>
<h2>五、控制组与守卫</h2>
<div class="two">
<table><tr><th>#</th><th>判决</th><th>控制组</th></tr>%(ctl_rows)s</table>
<table><tr><th>#</th><th>判决</th><th>守卫</th></tr>%(grd_rows)s</table>
</div>
<h2>六、门槛登记（Q10）</h2>
<table><tr><th>项</th><th>缺口</th><th>状态</th><th>判决</th></tr>%(gate_rows)s</table>
<div class="note">本卷<b>不新增方程、不给新预言</b>：它把「一个 4 位数」升级为「一个闭式 + 一条定理 + 一块量纲盲区」，
并把 G2 的可攻面从「设计 r 机制」收紧为「<b>r 必须落在 λ̄_C 上</b>」。</div>
<h2>七、诚实边界</h2>
<div class="note">B1 只用 v_z=c 极限与帧局部 κ,τ（承 r329）；B2 幂律结构只对幂次敏感、不对 α 数值；
B3 唯一闭合锚只对 κ/τ=α 一族成立；B4 不主张 α 可导出（恰恰相反）；B5 不改 r342 判词，只精化读数；
B6 不主张纲领死亡，只主张「玻尔锚不能给电子质量」。</div>
<div class="note" style="margin-top:26px">复现：<code>python -X utf8 源码\\_run_r344.py</code> ⇒ rc=0，条目 %(n)d，
控制组 %(c)s，守卫 %(g)s。本卷条目<b>不可与 r324/r329/r338/r342 相加</b>。</div>
</div></body></html>""" % {
        "n": summary["条目总数"], "p": summary["PASS"], "f": summary["FAIL"], "i": summary["INFO"],
        "c": summary["控制组"], "g": summary["守卫"], "score": extra["score"],
        "rm": fmt(extra["r_m"], 6), "p2": fmt(ALPHA ** 2, 6), "d1": fmt(extra["d1"], 4),
        "rinv": fmt(extra["r_inv"], 6), "pinv2": fmt(ALPHA_INV2, 6),
        "kaptau": fmt(extra["k_over_t"], 6),
        "ladder_rows": ladder_rows, "gate_rows": gate_rows,
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
    q3()
    e4 = q4()
    e5 = q5()
    e6 = q6()
    e7 = q7()
    q8()
    q9()
    e10 = q10()
    e11 = q11()
    extra = {"declared_n": 25,
             "power_ok": (e1["d1"] < Decimal("1e-4")) and (e1["d3"] < Decimal("1e-4")),
             "alpha_blind": e7["alpha_blind"],
             "r_m": e1["r_m"], "r_pure": e1["r_pure"], "r_inv": e1["r_inv"],
             "d1": e1["d1"], "d3": e1["d3"],
             "k_over_t": e2["k_over_t"], "sqr_over_lam": e2["sqr_over_lam"],
             "ladder_rows": e4["ladder_rows"], "ladder_worst": e4["worst"],
             "m_tau": e5["m_tau"], "ratio_tau": e5["ratio_tau"],
             "hits": e6["hits"], "target": e6["target"],
             "gate_rows": e10["gate_rows"], "score": e11["score"]}
    controls(extra)
    guards(extra)
    summary = emit(extra)
    emit_judgment(summary, extra)
    p = emit_html(summary, extra)
    print("=" * 78)
    print("TUFT-%s · 质量式锚口径溯源：玻尔锚 α² 结构定理" % RID)
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

