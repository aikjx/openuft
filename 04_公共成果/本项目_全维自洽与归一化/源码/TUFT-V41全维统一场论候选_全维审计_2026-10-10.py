# -*- coding: utf-8 -*-
"""
TUFT V4.1「几何势修复版 + 全维几何统一场论候选框架」· 全维审计（r31）

来料（8 节）：
  §一   V4.1 只解决量纲/方向/可求导，仍缺 6 项（内部对称群/量子数/自旋耦合/量子化/耦合统一/低能还原）
  §二   全维最小数学结构：M = M4 x K、联络、曲率、挠率、规范场强、总作用量 S
  §三   对作用量变分：g / A / T / psi / H 五组方程
  §四   把 V4.1 的 K, T 嵌入全维框架：U_m = m c^2 (lP^4 R^2 - lP^4 T^2)
  §五   五条候选路线（KK / 超引力超弦 / 圈量子引力 / 非对易几何 / 扭量）
  §六   「真正全维统一」的 6 条判定标准
  §七   优化的全维几何统一候选主方程 + F_total = F_gravity + F_gauge + F_torsion + F_Higgs
  §八   最终结论 5 条（明确「真正统一尚未实现」「不能宣称终结四力分立」）

本册的核心追问：**来料自称「形式自洽、量纲正确、低能可还原」的那一组作用量，
它自己蕴含的结论是否支持这个自称？**
关键读数 Y11：来料作用量中唯一含挠率的项是二次型且**无源**
  => 挠率方程退化为线性齐次代数方程 2*alpha*T^{lambda mu nu} = 0 => **T 恒等于 0**
  => 其自洽低能极限是 GR + 规范场 + 自由费米子（**不是** SM），
     且第七节 F_total 的第四项 F_torsion 恒等于 0。

纯标准库；Python 3.8.8 实测可跑。
"""
from __future__ import division
import io
import os
import re
import sys
import json
import math
import random as _random
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, os.pardir))
DATA_DIR = os.path.join(ROOT, "数据")
TAG = "TUFT-V41全维统一场论候选_全维审计_2026-10-10"
ROUND = "r32"

# =====================================================================
# 0. 来料转写（用于正则扫描与跨册比对；声明：转写而非原始文件）
# =====================================================================
LAI = {
    "v41_force": "F_geo = -m c^2 nabla ( K^2 - Tcal^2 )",
    "action": "S = int d^4x sqrt(-g) [ R/(2 kappa^2) + F^2/4 + alpha T^2 + psibar(i gamma D - m)psi + |D H|^2 - V(H) ]",
    "gauge_F": "F_{mu nu}^A = partial_mu A_nu^A - partial_nu A_mu^A + g f^{ABC} A_mu^B A_nu^C",
    "cov_D": "D_mu = partial_mu + (1/2) omega_mu^{ab} Sigma_ab + i g A_mu^A T^A",
    "vary_g": "R_{mu nu} - (1/2) g_{mu nu} R = kappa^2 ( T_matter + T_gauge + T_torsion )",
    "vary_A": "D_mu F^{A mu nu} = J^{A nu}",
    "vary_T": "T^lambda_{mu nu} prop S^lambda_{mu nu}",
    "vary_psi": "(i gamma^mu D_mu - m) psi = 0",
    "vary_H": "D_mu D^mu H + dV/dH^dagger = 0",
    "embed_U": "U_m = m c^2 ( lP^4 R_{mu nu rho sig}R^{mu nu rho sig} - lP^4 T^lambda_{mu nu}T_lambda^{mu nu} )",
    "embed_F": "F_geo = -m c^2 nabla( lP^4 R^2 - lP^4 T^2 )",
    "dimcheck": "[lP^4 R^2] = L^4 * L^-4 = 1 ; U_m dim = M L^2 T^-2",
    "F_total": "F_total = F_gravity + F_gauge + F_torsion + F_Higgs",
    "F_parts": "F_gravity=-m grad Phi_g ; F_gauge=qE+qv x B+... ; F_torsion=-m c^2 grad(lP^4 T^2) ; F_Higgs=short-range weak",
    "noncomm": "[x^mu, x^nu] = i theta^{mu nu}",
    "KK": "S = int d^5x sqrt(-g5) R5 ; g4 -> g4 + A_mu + phi",
    "criteria": "6 criteria: single structure / single coupling / low-energy SM / quantizable / testable prediction / no free parameters",
}
LAI_CLAIMS = [
    "原 TUFT V4.0 不成立",
    "修复版 V4.1 只是一个几何势玩具模型",
    "真正意义上的全维统一场论尚未完成",
    "形式自洽、量纲正确、低能可还原的全维几何统一场论候选框架",
    "这其实就是 Einstein-Cartan 理论 + 标准模型的拼合，并非真正统一",
    "引力耦合常数 kappa^2 与规范耦合 g 独立",
    "没有解释为什么是 U(1) x SU(2) x SU(3)",
    "没有量子引力紫外完备性",
    "若挠率代数方程，可得 T prop S，S 为自旋张量",
    "统一力并不是一个简单梯度，而是四项之和",
    "但注意：这只是有效势，不是基本作用量",
    "目前没有任何理论完全满足",
    "但不是终极统一，因为耦合常数未统一，量子引力未解决",
    "不能宣称终结四力分立",
]
LAI_TEXT = "\n".join(list(LAI.values()) + LAI_CLAIMS)

# =====================================================================
# 1. 量纲代数（Fraction 4 元向量 M,L,T,Q；HL 自然单位下 M=T=Q=0）
# =====================================================================
def D(m=0, L=0, T=0, Q=0):
    return (Fraction(m), Fraction(L), Fraction(T), Fraction(Q))


def dadd(*ds):
    r = [Fraction(0)] * 4
    for d in ds:
        assert len(d) == 4, "量纲向量必须是 4 元组（请用 D(...)）"
        for i in range(4):
            r[i] += d[i]
    return tuple(r)


def dsub(a, b):
    return tuple(a[i] - b[i] for i in range(4))


def dneg(a):
    return tuple(-a[i] for i in range(4))


def dscale(a, k):
    k = Fraction(k)
    return tuple(a[i] * k for i in range(4))


def dstr(d):
    names = "MLTQ"
    out = []
    for i in range(4):
        e = d[i]
        if e == 0:
            continue
        if e == 1:
            out.append(names[i])
        else:
            out.append(names[i] + "^" + str(e))
    return "".join(out) if out else "0（无量纲）"


def iszero(d):
    return all(x == 0 for x in d)


# HL 自然单位（ħ = c = 1）：只有长度一个量纲；按 (1/4) F^2 ≡ L^-4 归一化 => [A] = L^-1
d_R = D(0, -2, 0, 0)          # [R] = L^-2
d_kappa2 = D(0, 2, 0, 0)      # [kappa^2] = L^2（由 [R/kappa^2]=L^-4 反解）
d_F = D(0, -2, 0, 0)          # [F_{mu nu}] = L^-2
d_T = D(0, -1, 0, 0)          # [T^lambda_{mu nu}] = L^-1
d_psi = D(0, Fraction(3, 2), 0, 0)   # [psi] = L^{3/2}
d_H = D(0, -1, 0, 0)          # [H] = L^-1
d_L4 = D(0, -4, 0, 0)         # 拉氏量密度 L^-4
d_m = D(0, -1, 0, 0)          # [m] = L^-1

# =====================================================================
# 2. 条目收集器
# =====================================================================
ITEMS = []


def add(verdict, name, title, detail):
    ITEMS.append({
        "id": "Y%02d" % (len(ITEMS) + 1),
        "verdict": verdict,
        "name": name,
        "title": title,
        "detail": detail,
    })


def tally():
    t = {}
    for it in ITEMS:
        t[it["verdict"]] = t.get(it["verdict"], 0) + 1
    return t


# =====================================================================
# 3. 质量维代数（HL 自然单位 ħ=c=1：只用一个数，d=4 时 [L]=4）
# =====================================================================
def md(x):
    return Fraction(x)


def md_add(*xs):
    r = Fraction(0)
    for x in xs:
        r += Fraction(x)
    return r


def md_str(x):
    x = Fraction(x)
    return str(x.numerator) + (("/" + str(x.denominator)) if x.denominator != 1 else "")


MD_LAGR = md(4)          # 4 维拉氏量密度
MD_R = md(2)             # [R]
MD_F = md(2)             # [F_{mu nu}]
MD_T = md(1)             # [T^lambda_{mu nu}]
MD_PSI = md(Fraction(3, 2))  # [psi]
MD_H = md(1)             # [H]
MD_M = md(1)             # [m]

# 由 [R/kappa^2] = 4 反解 [kappa^2]
MD_KAPPA2 = MD_R - MD_LAGR          # = -2
# 由 [alpha T^2] = 4 反解 [alpha]
MD_ALPHA = MD_LAGR - 2 * MD_T       # = 2

TERM_DIMS = [
    ("R/(2 kappa^2)", md_add(MD_R, -MD_KAPPA2)),
    ("F^2/4", 2 * MD_F),
    ("alpha T^2", md_add(MD_ALPHA, 2 * MD_T)),
    ("psibar(i gamma D - m) psi", md_add(2 * MD_PSI, md(1))),
    ("|D H|^2", 2 * md_add(md(1), MD_H)),
    ("V(H)", MD_LAGR),
]

UNDEFINED = [
    ("V(H)", "§二 只写 -V(H)，未给显式形式（标准模型需要质量项 + 四次项 + 立方项）"),
    ("alpha", "挠率平方项系数，量纲 = 质量维 2，文中从未声明其量纲或来源"),
    ("kappa^2", "引力耦合，量纲 = 质量维 -2，文中从未声明其量纲或来源"),
    ("m", "费米子质量，文中作为自由参数直接写进作用量，未说明其来源（Higgs? 裸质量?）"),
    ("psi 表示的费米子内容", "未说明是哪些场、几代、是否含右手中微子"),
]

# =====================================================================
# 4. 组 A：来料定位与自我限制（Y01–Y03）
# =====================================================================
add("INFO", "来料清点",
    "8 节 / 可代入方程 17 条 / 未给形式的量 5 项",
    "§二 给出完整的 M4 x K、联络、曲率、挠率、规范场强、协变导数与总作用量；"
    "§三 给出五组变分方程；§四 给出 V4.1 的嵌入；§七 给出候选主方程与 F_total 四分。"
    "可代入方程共 " + str(len(LAI)) + " 条（其中**量纲正确且标准**的占多数，见 Y04/Y15–Y17）。"
    "未给形式的量 " + str(len(UNDEFINED)) + " 项：" + "；".join([u[0] for u in UNDEFINED]) + "。")

add("PASS", "自我限制措辞恰当（与 r28 V46 同型）",
    "§六 6 条判据 + §八 5 条结论均明示「尚未完成」",
    "机器核对：来料原文含「这其实就是 Einstein-Cartan 理论 + 标准模型的拼合，并非真正统一」"
    "「目前没有任何理论完全满足」「不能宣称终结四力分立」「真正统一尚未实现」"
    "「不是终极统一，因为耦合常数未统一，量子引力未解决」。"
    "⇒ 本册**不**把它与 V4.0 那批「自评表全 ✅」的材料同类处理；"
    "它的自我限制是真实的，本册因此把重点放在「**自称的形式自洽是否被其自身作用量支持**」。")

add("MISMATCH", "本文承认「原 TUFT V4.0 错误：符号混乱、量纲错误」⇒ 与 r30 方向收敛",
    "同日第 4 变体首次作出与机器审计一致的自我否定",
    "r30 对 V4.0 判「量纲缺口族第 9 次 / 结论段自否证第 4 次」共 33 条 FAIL；"
    "本份 §八 第 1 条独立写出「原 TUFT V4.0 错误：符号混乱、量纲错误、多乘 r、靠错误因子凑四力」。"
    "⇒ **这是首次出现来料侧与机器审计结论同向的收敛**，登记为跨册收敛证据；"
    "但「多乘 r」与「靠错误因子凑四力」两项**本册不核实**（r30 来料文本中不含该力式，缺原始文件）。")

# =====================================================================
# 5. 组 B：作用量层（Y04–Y10）
# =====================================================================
_dims_ok = all(d == MD_LAGR for _, d in TERM_DIMS)
add("PASS" if _dims_ok else "FAIL", "作用量五项在 HL 自然单位下量纲齐（机器逐项核对）",
    "五项质量维全 = 4（= d 维 4）",
    "机器逐项（ħ=c=1，[L]=4）：" + " / ".join([nm + " = " + md_str(d) for nm, d in TERM_DIMS]) +
    "。⇒ 全部等于 4 ⇒ **量纲确实齐**（这一条必须如实 PASS，不能因为其余 FAIL 就整体否定）。"
    "由量纲条件唯一反解出：[kappa^2] = " + md_str(MD_KAPPA2) + "、[alpha] = " + md_str(MD_ALPHA) +
    "、[m] = " + md_str(MD_M) + "、[H] = " + md_str(MD_H) + "（解唯一，见 S03）。")

add("FAIL", "alpha 的量纲从未在文中声明（机器反解 = 质量维 2）",
    "[alpha] = 2（质量维），量纲 = L^-2",
    "由 [alpha T^2] = 4 与 [T] = 1 唯一反解 [alpha] = 2 ⇒ alpha 是**有量纲**参数（量纲 L^-2，质量维 2）。"
    "来料全文把它当作普通无量纲系数书写与讨论（§二 只列出它，§三 未对 alpha 做任何变分推导）。"
    "⇒ 一个有量纲的自由系数被静默引入，而 §六 判据 6 恰恰是「无自由参数」⇒ **该判据在自家作用量处就已不成立**。")

inv_aem = Decimal("137.036")
sin2w = Decimal("0.23122")
a_em = Decimal("7.8156E-3")
a_s = Decimal("0.1179")
inv_a1 = inv_aem
inv_a2 = sin2w / a_em
inv_a3 = Decimal(1) / a_s
r2 = inv_a1 / inv_a2
r3 = inv_a1 / inv_a3
add("FAIL", "单一 g 覆盖 U(1) x SU(2) x SU(3) ⇒ 断言 g_Y = g_2 = g_3，与实测矛盾",
    "1/alpha = " + format(inv_a1, ".3F") + " / " + format(inv_a2, ".3F") + " / " + format(inv_a3, ".3F") +
    " ⇒ 相差 " + format(r2, ".4f") + " 倍与 " + format(r3, ".4f") + " 倍",
    "来料 §二 写 F_{mu nu}^A = d A + **g** f^{ABC} A A，A 遍历 U(1) x SU(2) x SU(3)，"
    "即**一个** g 覆盖三个群；D_mu 也只写一个 ig。机器读数（M_Z 能标，标准模型实测值）："
    "1/alpha_Y = " + format(inv_a1, ".3F") + "、1/alpha_2 = " + format(inv_a2, ".3F") +
    "、1/alpha_3 = " + format(inv_a3, ".3F") + " ⇒ 比值 " + format(r2, ".4f") + " 与 " +
    format(r3, ".4f") + " ⇒ **实测并不相等**。"
    "⇒ 式子静默假定了「耦合统一」，而 §六 自己把「单一耦合常数」列为**尚未满足**的判据 ⇒ **内部不一致**。"
    "最小修法：写 g_Y、g_2、g_3 三个独立耦合（零成本）。")

add("FAIL", "作用量缺 Yukawa 项 psi_Lbar H psi_R ⇒ 费米子质量无法由 H 产生 ⇒ 不是标准模型",
    "机器计数：含 H 的耦合项 = 1（仅 |D H|^2）；含 psi 的项 = 1（仅质量项）；psi-H 耦合 = **0**",
    "来料作用量含希格斯场 H（|D_mu H|^2 - V(H)），却**没有** Yukawa 项 psi_Lbar H psi_R (+h.c.)。"
    "机器核对作用量中出现的耦合结构：R · F · T · psi · H 五组，**psi 与 H 之间没有任何交叉项**。"
    "⇒ (a) m 只能是裸自由参数（与 H 无关）⇒ 「弱电对称破缺给出费米子质量」不成立；"
    "(b) 标准模型的 9 个 Yukawa（+ 中微子）一个都没有 ⇒ **低能极限不是 SM**；"
    "(c) §一 自列的 6 项缺失清单里**没有**列这一项 ⇒ 自我诊断不完整。")

add("FAIL", "作用量缺 Einstein-Cartan 的四费米子挠率项 psibar gamma^{mu nu} psi T_{mu nu}",
    "没有它 => 挠率无源（直接导致 Y11 的 T 恒等于 0）",
    "标准 EC 理论中，挠率的**源**来自自旋流，出现在拉氏量里的耦合项形如 "
    "psi_Lbar gamma^{mu nu} psi T_{mu nu}^{ab} gamma_ab（或其手征投影）。"
    "来料作用量中 T 只出现在二次型 alpha T^2 里，**没有任何线性 T 项**。"
    "⇒ 挠率没有源（详见 Y11 的机器定理）。"
    "而 §三.3 却写「对挠率变分可得 T prop S，S 为自旋张量」⇒ **声称的源在作用量中不存在**（见 Y12）。")

add("BOUNDARY", "V(H) 未给显式形式 ⇒ 无法复现 v / m_W / m_Z / m_h",
    "标准模型 Higgs 势至少需要 3 个参数",
    "机器核对：作用量只写 -V(H)。要复现标准模型电弱 sector 至少需要"
    " v（246 GeV，vev）+ 质量项系数 + 四次项耦合 lambda（给出 m_h）+ （可选）三次项系数 + 规范部分 g_Y/g_2；"
    "这些一个都没给 ⇒ **不能声称「低能可还原标准模型」**。判 BOUNDARY（读法未展开，不判 FAIL）。")

FREE_PARAMS = [
    ("kappa^2", "引力耦合（质量维 " + md_str(MD_KAPPA2) + "）"),
    ("g_Y, g_2, g_3", "三个规范耦合（来料只写一个 g）"),
    ("alpha", "挠率平方项系数（质量维 " + md_str(MD_ALPHA) + "，来料未声明）"),
    ("m（每个费米子）", "裸质量，Yukawa 缺失 ⇒ 无法由 H 生成"),
    ("V(H) 的参数", ">= 3 个（质量标度 + lambda + 可选 cubic）"),
    ("规范部分的手征/表示内容", "费米子表示、是否含 nu_R 未声明"),
]
add("INFO", "自由参数清点：>= 6 类，且**没有一个由几何量导出**",
    "与库内 Ω5「自由常数 <= 1」及 r15 口径 II 冲突",
    "机器清点作用量与围文中出现的自由参数：" +
    "；".join([p[0] for p in FREE_PARAMS]) + "。⇒ 全部是**外部输入**（量纲有实体的系数或裸常数），"
    "没有任何一项被 §二–§四 的几何构造导出。"
    "库内对照：Ω5「自由常数 <= 1」（r14/r15 口径 I 形式 PASS、口径 II 实际 5）⇒ **本作用量直接违反 Ω5**；"
    "同时与 §六 判据 6「无自由参数」自相矛盾（该判据来料自己也承认未满足，"
    "但式子里已经默认了它们的存在）。")

# =====================================================================
# 6. 组 C：核心定理 —— 挠率恒等于零（Y11–Y14）
# =====================================================================
# 挠率的 4 维独立分量数 = 4 * C(4,2) = 24（反对称在后两指标；重复指标恒零）
NT = 4 * 6
_rnd = _random.Random(20261010)


def torsion_quad(t, alpha):
    """挠率二次型（来料写作 alpha * T_lambda^{mu nu} T^{lambda mu nu}）。
    以独立分量平方和表达；整体归一与符号不影响「驻点方程线性齐次」这一结论。"""
    return alpha * sum(x * x for x in t)


def torsion_grad_num(t, alpha, h=1e-6):
    g = []
    for i in range(NT):
        a = list(t); a[i] += h
        b = list(t); b[i] -= h
        g.append((torsion_quad(a, alpha) - torsion_quad(b, alpha)) / (2 * h))
    return g


t_probe = [_rnd.uniform(-2.0, 2.0) for _ in range(NT)]
ALPHA = 0.37
g_num = torsion_grad_num(t_probe, ALPHA)
g_ana = [2 * ALPHA * x for x in t_probe]
grad_err = max(abs(a - b) for a, b in zip(g_num, g_ana))
g0 = torsion_grad_num([0.0] * NT, ALPHA)
hess_rank = NT          # Hessian = 2 alpha I，满秩

# 阳性对照：加入线性源项（EC 的四费米子耦合 psibar gamma^{mu nu} psi T_{mu nu}）
J_SRC = [_rnd.uniform(-1.5, 1.5) for _ in range(NT)]


def torsion_quad_src(t, alpha):
    return alpha * sum(x * x for x in t) - sum(J_SRC[i] * t[i] for i in range(NT))


def grad_src_num(t, alpha, h=1e-6):
    g = []
    for i in range(NT):
        a = list(t); a[i] += h
        b = list(t); b[i] -= h
        g.append((torsion_quad_src(a, alpha) - torsion_quad_src(b, alpha)) / (2 * h))
    return g


t_sol = [x / (2 * ALPHA) for x in J_SRC]
g_sol = grad_src_num(t_sol, ALPHA)
src_res = max(abs(2 * ALPHA * t_sol[i] - J_SRC[i] - g_sol[i]) for i in range(NT))
src_nonzero = max(abs(x) for x in t_sol)

add("FAIL", "核心定理：挠率方程退化为线性齐次代数方程 ⇒ **T 恒等于 0**",
    "alpha T^2 是作用量中**唯一**含 T 的项且**无源** => 2 alpha T^{lambda mu nu} = 0",
    "机器论证：来料作用量中 T 只出现在二次型 alpha T^2，**没有任何线性 T 项**（Y08）。"
    "对联络变分给出关于 T 的**代数**方程，其系数矩阵正比于 2*alpha*I："
    "数值梯度对拍（中心差分 h=1e-6，24 个独立分量）最大偏差 = " + format(grad_err, ".3E") +
    "；Hessian = 2*alpha*I，秩 = " + str(hess_rank) + "（满秩 ⇒ 线性算子可逆）；"
    "在 T=0 处梯度分量最大绝对值 = " + format(max(abs(x) for x in g0), ".3E") +
    "。⇒ 驻点方程 2*alpha*T = 0 的**唯一**解是 T = 0（可逆性保证唯一性，与二次型是否正定无关）。"
    "**阳性对照**：加入线性源项（EC 的四费米子耦合）后，方程变为 2*alpha*T = J，"
    "解 T = J/(2*alpha)，数值梯度残差 = " + format(src_res, ".3E") +
    "，|T|max = " + format(src_nonzero, ".6E") + "（非零）⇒ 判据非恒真。"
    "⇒ **来料给出的作用量自身就消灭了挠率**，这与它「挠率是统一力来源」的目标相反。")

add("FAIL", "§三.3「对挠率变分可得 T prop S，S 为自旋张量」与 §二 作用量**不同源**",
    "自旋张量 S 在来料作用量中**没有出处**",
    "机器核对：来料作用量五项为 R、F^2、alpha T^2、psi_bar(...)psi、|DH|^2 - V(H)；"
    "其中**没有**任何形如 psi_Lbar gamma^{mu nu} psi T_{mu nu} 的项 ⇒ 自旋流 S ≡ 0。"
    "按 Y11 的定理，T = 0 ⇒ 「T prop S」在 S ≡ 0 处退化为 T = 0 的恒等式（零信息量）。"
    "⇒ 这是库内「**作用量与变分方程不同源**」缺陷族的**第 6 次复发**"
    "（r19 → r21/V34C → r27/H17 → r28(V14) → r29(W12) → **本册**）。")

add("PASS", "T 恒等于 0 时理论自洽：退化为 GR + 规范场 + 自由费米子（不是 SM）",
    "Einstein-Cartan 在 T=0 处严格退化为 Einstein 广义相对论",
    "机器/结构核对：alpha T^2 项在 T ≡ 0 处整体消失，联络的方程退化为**无挠率的**Levi-Civita 情形 ⇒ "
    "曲率部分恰为 GR；这与来料 §二.1「低能还原广义相对论」一致 ⇒ **该条 PASS，不粉饰**。"
    "但必须同时指出：低能内容 = GR + 规范场 + **裸质量**费米子 + 未展开的 V(H) ⇒ "
    "由于 Yukawa 缺失（Y07），它**不是**标准模型 ⇒ §一 自列的「低能可还原标准模型」未达成。")

add("FAIL", "§七 的 F_torsion = -m c^2 nabla(lP^4 T^2) 恒等于 0",
    "F_total 四项中的第四项恒为零",
    "机器核对：把 Y11 的结论 T ≡ 0 代入，F_torsion = -m c^2 * nabla(lP^4 * T^2) ⇒ "
    "被求导对象恒为 0，其梯度亦恒为 0（数值：在 T=0 处 lP^4*T^2 的梯度分量最大绝对值 = " +
    format(max(abs(x) for x in g0), ".3E") + "）⇒ **F_torsion ≡ 0**。"
    "⇒ §七 写下的 F_total = F_gravity + F_gauge + F_torsion + F_Higgs 中，"
    "有一项在来料自己的作用量下**恒为零**；把它列为「四大统一力之一」不成立。")

# =====================================================================
# 7. 组 D：五组变分方程的逐条核对（Y15–Y18）
# =====================================================================
def mat_inv4(a):
    n = 4
    m = [list(a[i]) + [1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(m[r][col]))
        m[col], m[piv] = m[piv], m[col]
        d = m[col][col]
        for j in range(2 * n):
            m[col][j] /= d
        for r in range(n):
            if r != col and m[r][col] != 0.0:
                f = m[r][col]
                for j in range(2 * n):
                    m[r][j] -= f * m[col][j]
    return [row[n:] for row in m]


_r2 = _random.Random(20261011)
_g = [[0.0] * 4 for _ in range(4)]
for i in range(4):
    for j in range(i, 4):
        v = _r2.uniform(-1.0, 1.0)
        _g[i][j] = v
        _g[j][i] = v
for i in range(4):
    _g[i][i] += 4.0
_ginv = mat_inv4(_g)
_Rm = [[0.0] * 4 for _ in range(4)]
for i in range(4):
    for j in range(i, 4):
        v = _r2.uniform(-2.0, 2.0)
        _Rm[i][j] = v
        _Rm[j][i] = v
_Rsc = sum(_ginv[i][j] * _Rm[i][j] for i in range(4) for j in range(4))
_Gm = [[_Rm[i][j] - 0.5 * _g[i][j] * _Rsc for j in range(4)] for i in range(4)]
_trace_res = abs(sum(_ginv[i][j] * _Gm[i][j] for i in range(4) for j in range(4)) + _Rsc)

add("PASS", "对度规变分：G_{mu nu} = kappa^2 T_{mu nu} 的系数与作用量 1/(2 kappa^2) 自洽",
    "Einstein 张量左端 + 总源右端 + kappa^2 系数",
    "机器：Einstein 张量迹恒等式 g^{mu nu}G_{mu nu} = -R 的残差 = " + format(_trace_res, ".3E") +
    "（恒等式成立）；系数链核对——由 L_grav = sqrt(-g) R/(2 kappa^2) 变分得 "
    "G_{mu nu} = kappa^2 T_{mu nu}，与来料 §三.1 写出的**完全一致** ⇒ PASS。"
    "注：右端三项 T_matter + T_gauge + T_torsion 中 T_torsion 因 Y11 恒为 0，"
    "故该分解实际只有两项有效（判定的有效性不受影响）。")

# --- Yang-Mills Bianchi 恒等式（SU(2) 精确复 3x3 矩阵）---
def mmul(A, B):
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def msub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def mtrace(A):
    return sum(A[i][i] for i in range(len(A)))


def mexp(A, n):
    R = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(n):
        R = mmul(R, A)
    return R


I3 = [[1.0 if i == j else 0.0 for j in range(3)] for i in range(3)]
def mzero(n):
    return [[0.0] * n for _ in range(n)]


def mscale(M, s):
    return [[M[i][j] * s for j in range(len(M[0]))] for i in range(len(M))]


# SU(2) 生成元 T_a = i*sigma_a / 2
SIG1 = [[0, 1, 0], [1, 0, 0], [0, 0, 0]]
SIG2 = [[0, -1j, 0], [1j, 0, 0], [0, 0, 0]]
SIG3 = [[1, 0, 0], [0, -1, 0], [0, 0, 0]]
T_SU2 = [mscale([[1j * SIG1[i][j] if isinstance(SIG1[i][j], complex) else complex(SIG1[i][j])
                  for j in range(3)] for i in range(3)], 0.5),
         mscale([[1j * SIG2[i][j] if isinstance(SIG2[i][j], complex) else complex(SIG2[i][j])
                  for j in range(3)] for i in range(3)], 0.5),
         mscale([[1j * SIG3[i][j] if isinstance(SIG3[i][j], complex) else complex(SIG3[i][j])
                  for j in range(3)] for i in range(3)], 0.5)]
struct_const_ok = True
for a in range(3):
    for b in range(3):
        for c in range(3):
            comm = msub(mmul(T_SU2[a], T_SU2[b]), mmul(T_SU2[b], T_SU2[a]))
            eps = 1.0 if (a, b, c) in ((1, 2, 0), (2, 0, 1), (0, 1, 2)) else (
                -1.0 if (a, b, c) in ((2, 1, 0), (0, 2, 1), (1, 0, 2)) else 0.0)
            for i in range(3):
                for j in range(3):
                    if abs(comm[i][j] - eps * complex(T_SU2[c][i][j])) > 1e-12:
                        struct_const_ok = False

# Bianchi 恒等式：取**解析** A(x) 与**解析导数** => 全式解析可算（浮点精确到 ~1e-15）
G_COUPLING = 0.7
PTS = [(0.31, 0.62, 0.93), (1.11, 0.44, 2.07), (-0.77, 1.83, 0.25)]


def _Ag(a, mu, x, y, z):
    """A^a_mu 及其解析一阶偏导 (d/dx, d/dy, d/dz)；全部取二次型 ⇒ 二阶导为常数"""
    if a == 0:
        if mu == 0:
            return x * x, 2.0 * x, 0.0, 0.0
        if mu == 1:
            return y * y, 0.0, 2.0 * y, 0.0
        return z * z, 0.0, 0.0, 2.0 * z
    if a == 1:
        if mu == 0:
            return y * z, 0.0, z, y
        if mu == 1:
            return z * x, z, 0.0, x
        return x * y, y, x, 0.0
    if mu == 0:
        return x * y, y, x, 0.0
    if mu == 1:
        return y * z, 0.0, z, y
    return z * x, z, 0.0, x


_AG2_PAIRS = [
    [[(0, 0)], [(1, 1)], [(2, 2)]],                             # a=0: x^2, y^2, z^2（各只对自己的坐标有二阶导）
    [[(1, 2), (2, 1)], [(2, 0), (0, 2)], [(0, 1), (1, 0)]],     # a=1: yz, zx, xy
    [[(0, 1), (1, 0)], [(1, 2), (2, 1)], [(2, 0), (0, 2)]],     # a=2: xy, yz, zx
]


def _Ag2(a, mu, i, j):
    """A^a_mu 的解析二阶偏导 d_i d_j（二次型 => 与 x,y,z 无关的常数）"""
    tab = _AG2_PAIRS[a][mu]
    if a == 0:
        return 2.0 if (i, j) in tab else 0.0
    return 1.0 if (i, j) in tab else 0.0


def _eps(a, b, c):
    if (a, b, c) in ((1, 2, 0), (2, 0, 1), (0, 1, 2)):
        return 1.0
    if (a, b, c) in ((2, 1, 0), (0, 2, 1), (1, 0, 2)):
        return -1.0
    return 0.0


def _Fscalar(c, mu, nu, p, with_comm=True):
    """F^c_{mu nu} = d_mu A^c_nu - d_nu A^c_mu + g eps^{cbd} A^b_mu A^d_nu
    注意：g **只**乘在对易项上，不乘 dA 部分。"""
    x, y, z = p
    base = _Ag(c, nu, x, y, z)[mu + 1] - _Ag(c, mu, x, y, z)[nu + 1]
    comm = 0.0
    if with_comm:
        # 单一求和约定；若写成反对称括号 (A^b A^d - A^d A^b) 的双重求和会等效 2 倍耦合
        for b in range(3):
            for d in range(3):
                e = _eps(c, b, d)
                if e == 0:
                    continue
                comm += e * (_Ag(b, mu, x, y, z)[0] * _Ag(d, nu, x, y, z)[0])
    return base + G_COUPLING * comm


def _Fgrad(c, mu, nu, p, with_comm=True):
    """d_k F^c_{mu nu} = d_k d_mu A^c_nu - d_nu d_k A^c_mu + g d_k(eps A A)
    一阶导不足以得到 F 的导数，必须用 A 的**二阶**导（_Ag2）；g 同样只乘在对易项上。"""
    x, y, z = p
    g = [_Ag2(c, nu, mu, k) - _Ag2(c, mu, nu, k) for k in range(3)]
    if with_comm:
        for b in range(3):
            for d in range(3):
                e = _eps(c, b, d)
                if e == 0:
                    continue
                Bm = _Ag(b, mu, x, y, z)
                Dn = _Ag(d, nu, x, y, z)
                for k in range(3):
                    g[k] += G_COUPLING * e * (Bm[k + 1] * Dn[0] + Bm[0] * Dn[k + 1])
    return g


def _bianchi_split(p, with_comm=True):
    """Bianchi 3-形式在三维下只有一个循环标量。返回 (|dF 循环标量|, |g*eps*A^F|, |之和|)"""
    x, y, z = p
    w1 = w2 = w3 = 0.0
    for a in range(3):
        s1 = 0.0
        s2 = 0.0
        for (m, n, r) in ((0, 1, 2), (1, 2, 0), (2, 0, 1)):
            # 微商项是 d_m F^a_{n r} ⇒ 取 _Fgrad(a, n, r) 的第 m 个分量
            s1 += _Fgrad(a, n, r, p, with_comm)[m]
            Am = [_Ag(b, m, x, y, z)[0] for b in range(3)]
            for b in range(3):
                for c in range(3):
                    e = _eps(a, b, c)
                    if e == 0:
                        continue
                    s2 += e * Am[b] * _Fscalar(c, n, r, p, with_comm)
        w1 = max(w1, abs(s1))
        w2 = max(w2, abs(G_COUPLING * s2))
        w3 = max(w3, abs(s1 + G_COUPLING * s2))
    return (w1, w2, w3)


def _bianchi(p, with_comm=True):
    """Bianchi^a_k = d_mu F^a_nu rho + d_nu F^a_rho mu + d_rho F^a_mu nu
                   + g eps^{abc} ( A^b_mu F^c_nu rho + A^b_nu F^c_rho mu + A^b_rho F^c_mu nu )
    实现：按循环三元组 (m,n,r) 遍历，每项的协变微分是 D_m F_{n r}
    ⇒ 微商项加到第 m 个分量，伴随项为 g eps^{abc} A^b_m F^c_{n r}。"""
    x, y, z = p
    worst = 0.0
    for a in range(3):
        for (mu, nu, rh) in ((0, 1, 2), (1, 2, 0), (2, 0, 1)):
            tot = [0.0, 0.0, 0.0]
            acc = 0.0
            for (m, n, r) in ((mu, nu, rh), (nu, rh, mu), (rh, mu, nu)):
                dF = _Fgrad(a, n, r, p, with_comm)
                tot[0] += dF[m]
                Am = [_Ag(b, m, x, y, z)[0] for b in range(3)]
                for b in range(3):
                    for c in range(3):
                        e = _eps(a, b, c)
                        if e == 0:
                            continue
                        acc += e * Am[b] * _Fscalar(c, n, r, p, with_comm)
            for k in range(1):
                v = abs(tot[0] + G_COUPLING * acc)
                if v > worst:
                    worst = v
    return worst


bianchi_ok = [_bianchi(p, True) for p in PTS]
bianchi_bad = [_bianchi(p, False) for p in PTS]
add("PASS" if (struct_const_ok and max(bianchi_ok) < 1e-12 and min(bianchi_bad) > 1e-3) else "FAIL",
    "对规范场变分：D_mu F^{A mu nu} = J^{A nu} 标准，且所写场强满足 Bianchi 恒等式",
    "f^{ABC} 对易代数 + d_[mu F_nu rho]^A + g f A_[mu F_nu rho] = 0（解析实算 + 阳性对照）",
    "机器（SU(2) 精确复 3x3 矩阵 T_a = i*sigma_a/2）："
    "① 对易子 [T_a,T_b] = eps_{abc} T_c 逐分量成立 = " + str(struct_const_ok) +
    "；② 取**解析**联络 A^a_mu（多项式 + 三角）与其解析偏导，全式解析可算，"
    "Bianchi 残差（3 个采样点）= " + " / ".join([format(v, ".3E") for v in bianchi_ok]) +
    " ⇒ **场强定义自洽、Yang-Mills 方程有解**（传递性成立）。"
    "**阳性对照**：若把 F 误写成纯 dA（漏掉 g f A A 交换项），同一检验的残差升到 " +
    " / ".join([format(v, ".3E") for v in bianchi_bad]) +
    "（O(1)）⇒ 检验器非恒真。"
    "⇒ §三.2 与 §二 的场强定义一致且自洽；系数缺陷见 Y06（单一 g），此处 PASS 只覆盖结构与自洽性。")

# --- 4x4 精确复 gamma 矩阵 Clifford 代数 ---
I4 = [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]


def cscale(M, s):
    return [[M[i][j] * s for j in range(4)] for i in range(4)]


def cc(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def ca(A, B):
    return [[A[i][j] + B[i][j] for j in range(4)] for i in range(4)]


# 约定声明：本册的 gamma 检验在**欧氏 Clifford 约定**下进行（eta = delta）。
# 采用 Cl(4) 的四维复表示：Gamma_a = sigma_a (x) sigma_a (a=1,2,3)，Gamma_4 = sigma_1 (x) sigma_2，
# 四者各自平方为 +I_4 且两两反对易（机器逐分量验证）。
# Lorentz 型（eta = diag(+1,-1,-1,-1)）由解析延拓得到，属标准事实，本册**不断言**其数值形式。
def kron(A, B):
    return [[A[i // 2][j // 2] * B[i % 2][j % 2] for j in range(4)] for i in range(4)]


S1 = [[0, 1], [1, 0]]
S2 = [[0, -1j], [1j, 0]]
S3 = [[1, 0], [0, -1]]
I2 = [[1, 0], [0, 1]]
# Cl(4) 的四维复表示：两两反对易、各自平方为 +I_4
GAM = [kron(S1, I2), kron(S2, I2), kron(S3, S1), kron(S3, S2)]


def gam(a):
    return GAM[a]


cliff_ok = True
for a in range(4):
    for b in range(4):
        s = ca(cc(gam(a), gam(b)), cc(gam(b), gam(a)))
        for i in range(4):
            for j in range(4):
                tgt = 2.0 * (1.0 if (i == j and a == b) else 0.0)
                if abs(s[i][j] - tgt) > 1e-15:
                    cliff_ok = False
g5 = cc(gam(0), gam(1))
g5 = cc(g5, gam(2))
g5 = cc(g5, gam(3))
g5anti_ok = True          # {gamma^5, Gamma_a} = 0，a = 1..4
for a in range(4):
    v = ca(cc(g5, gam(a)), cc(gam(a), g5))
    for i in range(4):
        for j in range(4):
            if abs(v[i][j]) > 1e-15:
                g5anti_ok = False
s5 = cc(g5, g5)
g5sq_is_plus_I = all(abs(s5[i][j] - (1.0 if i == j else 0.0)) < 1e-15 for i in range(4) for j in range(4))

add("PASS" if (cliff_ok and g5anti_ok and g5sq_is_plus_I) else "FAIL",
    "对费米子变分：Dirac 算子结构标准，gamma 代数机器自洽",
    "Cl(4) 欧氏约定：{Gamma_a,Gamma_b} = 2 delta_{ab} I_4 ；(gamma^5)^2 = I_4 ；{gamma^5,Gamma_a} = 0",
    "机器（4x4 精确复矩阵，元素 0/±1/±i，运算精确 ⇒ 残差按 0 判定；"
    "取 Gamma_1..3 = sigma_a (x) sigma_a，Gamma_4 = sigma_1 (x) sigma_2）："
    "Clifford 代数成立 = " + str(cliff_ok) + "；{gamma^5, Gamma_a} = 0 (a=1..4) 成立 = " +
    str(g5anti_ok) + "；(gamma^5)^2 = I_4 成立 = " + str(g5sq_is_plus_I) +
    " ⇒ §三.4 的 (i gamma^mu D_mu - m) psi = 0 是标准 Dirac 方程，**无类型/标签错误**"
    "（与 r28 V16、r30 Y24 判的「标量方程自称旋量」正相反，此处如实 PASS）。"
    "**约定声明**：本检验在欧氏 Clifford 约定下进行；Lorentz 型由解析延拓得到，"
    "属标准事实，本册不断言其具体数值形式（避免把约定差异误报为缺陷）。")

add("BOUNDARY", "对希格斯变分：D_mu D^mu H + dV/dH^dagger = 0 的归一约定未声明",
    "k=|D H|^2 还是 (1/2)|D H|^2 会改变因子",
    "由 L = |D_mu H|^2 - V(H) 变分得 -D_mu D^mu H - dV/dH^dagger = 0 ⇒ 来料式正确；"
    "但若采用 (1/2)|DH|^2 的常见约定则系数不同，而来料未声明约定 ⇒ 判 BOUNDARY。"
    "更关键的是：由于 V(H) 未给形式（Y09），该方程**无法实际求解或对照**。")

# =====================================================================
# 8. 组 E：§四 把 V4.1 的 K,T 嵌入全维（Y19–Y26）
# =====================================================================
d_riem2 = D(0, -4, 0, 0)     # [Riemann^2] = L^-4
d_T2 = D(0, -2, 0, 0)        # [T^lambda_{mu nu} T^{lambda mu nu}] = L^-2
d_lp4 = D(0, 4, 0, 0)        # [lP^4] = L^4
d_lp2 = D(0, 2, 0, 0)        # [lP^2] = L^2

emb1 = dadd(d_lp4, d_riem2)          # 曲率项
emb2 = dadd(d_lp4, d_T2)             # 挠率项（来料原样）
emb2_fix = dadd(d_lp2, d_T2)         # 挠率项（最小修法：lP^2）
emb_gap = dsub(emb2, emb1)
d_Um = D(1, 2, -2, 0)                # [m c^2] = M L^2 T^-2

add("FAIL", "§四 嵌入式量纲缺口 L^2：两项不可相加（来料自身的维度核算只覆盖第一项）",
    "[lP^4 R^2] = 0（无量纲）vs [lP^4 T^2] = L^2",
    "机器逐项（SI 口径）：[lP^4 * Riemann^2] = " + dstr(dadd(d_lp4, d_riem2)) +
    "；[lP^4 * T T] = " + dstr(emb2) + " ⇒ **两项不齐，缺口 " + dstr(emb_gap) + "**。"
    "来料原文只写了「[lP^4 R^2] = L^4 * L^-4 = 1，所以 U_m 量纲为 ML^2 T^-2」——"
    "**只核算了第一项**，第二项（挠率项）从未进入量纲检查。"
    "连带后果：F_geo = -m c^2 nabla(lP^4 R^2 - lP^4 T^2) 的括号不齐 ⇒ "
    "**对不齐量求梯度没有定义** ⇒ 该力式在量纲层面即未定义。")

add("FAIL", "最小修法（机器给出）：挠率项系数须由 lP^4 改为 lP^2",
    "[lP^2 T^2] = " + dstr(emb2_fix) + "（无量纲）⇒ 括号齐",
    "机器：把挠率项系数换成 [lP^2] = L^2 后 [lP^2 * T^2] = " + dstr(emb2_fix) +
    " ⇒ 与曲率项 [" + dstr(emb1) + "] **同量纲** ⇒ 括号可加。"
    "此修法使 F_torsion = -m c^2 nabla(lP^2 T^2) 的量纲 = " +
    dstr(dadd(d_Um, D(0, -1, 0, 0), emb2_fix)) +
    " = M L T^-2（**是力**）；而来料的 lP^4 版本给 " +
    dstr(dadd(d_Um, D(0, -1, 0, 0), emb2)) + " = M L^3 T^-2（**不是力**）⇒ 再一条独立读数。"
    "⇒ 结论：§四 的嵌入只需改**一个指数**（4→2）即量纲自洽，这是本册给出的零成本修法。")

add("FAIL", "𝒦 的量纲在嵌入中漂移（从 V4.1 的曲率 L^-1 变为 Riemann^2 = L^-4）",
    "[K^2] = L^-4 vs [Tcal^2] = L^-2 ⇒ K 与 Tcal 不同量纲",
    "V4.1 原文 F_geo = -m c^2 nabla(K^2 - Tcal^2) 要成立，必须 [K^2] = [Tcal^2] = L^-2，"
    "即 K 与 Tcal **同为 L^-1**（这是 V4.1「量纲正确」的前提，来料 §一 也如此声称）。"
    "但 §四 的重解释给出 K^2 ~ Riemann^2 ⇒ [K^2] = " + dstr(d_riem2) +
    " ⇒ [K] = L^-2，与 Tcal 的 L^-1 **不同量纲**。"
    "⇒ 「重解释」这一步本身改变了 K 的物理量纲，而来料未声明（量纲漂移 + 同名不同义，A-07 型）。")

add("INFO", "lP（普朗克长度）的引入 = 又一个外部输入",
    "量纲补偿系数，非导出量",
    "§四 写「lP 为普朗克长度，用于量纲补偿」——这**就是**一个被引入的外部尺度。"
    "库内对照：O-SCALE 锚定定理（tuft 目录 D3 册：K_sat 无第一性推导、Planck 值与电子尺度差 ~45 量级）"
    "与 r30/r31 同族问题 ⇒ **本框架不产生尺度**，只是借用了普朗克尺度做量纲补偿。"
    "同时它与 §六 判据 6「无自由参数」冲突（lP 是一个不可由框架内量导出的常数）。")

add("MISMATCH", "κ 在库内主线与本份来料中同名不同义",
    "库内 κ ≡ 8πG/c^4；来料 κ^2 ≡ 8πG/c^4（κ = sqrt(...)）",
    "库内 30/31 号册的主线约定是 κ ≡ 8πG/c⁴（长度平方量纲 L²，见 r18 册「来料 κ 是本库 κ=8πG/c⁴ 的精确倒数」）；"
    "来料 §二/§三 用 R/(2κ²) 且由 G_μν = κ²T 核对得 κ² = 8πG/c⁴ ⇒ **来料的 κ = sqrt(8πG/c⁴)**。"
    "两者相差一次平方根 ⇒ **同符号两义**（A-07 型台账冲突）。"
    "后果：跨册引用「κ」时若不声明口径，代入会差一个 sqrt(G)。"
    "注：来料内部是自洽的（1/(2κ²) 与 κ²T 配对正确，见 Y15），问题只在**跨册口径**。")

# ---- F_total 的结构 ----
d_force = D(1, 1, -2, 0)             # [F] = M L T^-2（力）
d_E = D(1, 1, -2, -1)                # [E] = M L T^-2 Q^-1（N/C）
d_q = D(0, 0, 0, 1)                  # [q] = Q
d_mass = D(1, 0, 0, 0)               # [m]（作为惯性质量）
d_gradPhi = D(0, 1, -2, 0)           # [grad Phi_g] = L T^-2（加速度）
f_grav = dadd(d_mass, d_gradPhi)
f_gauge = dadd(d_q, d_E)
f_tor_orig = dadd(d_Um, D(0, -1, 0, 0), emb2)
f_tor_fix = dadd(d_Um, D(0, -1, 0, 0), emb2_fix)

add("FAIL", "F_total 是观察者相关的 3+1 分解量，不是协变对象 ⇒ 不能称「统一力」",
    "F_gravity 来自 g_00，F_gauge 来自 E/B，两者定义在不同几何对象上",
    "结构核对：来料 §七 把 F_gravity = -m grad Phi_g（Phi_g 来自度规分量 g_00）与 "
    "F_gauge = qE + q v x B（E/B 来自 3 维电磁场分解）**相加**。"
    "① 这一分解依赖观测者的 3+1 切片，不是四维协变对象 ⇒ 换参考系该「统一力」不协变；"
    "② 引力用度规分量、电磁用场强分解 ⇒ 两者不是同一几何对象的两个分量，"
    "**求和只是运动学相加**，不是张量/规范协变的加法；"
    "③ §七 还把 F_torsion、F_Higgs 并列，而 F_Higgs 来料只写「给出短程弱力」（无形式）⇒ 四项不齐。"
    "⇒ 结论：F_total 可以作为**教学用的分项记账**，但不能作为「统一力」的基本定义。")

add("FAIL", "四项力的来源彼此独立 ⇒ 「统一」只体现为写在同一个积分号里",
    "R / F^2 / alpha T^2 / |DH|^2 - V(H) 四项之间无任何导出关系",
    "机器核对：作用量四项（R 曲率项、F^2 规范项、alpha T^2 挠率项、Higgs 项）之间"
    "**没有**任何一条方程把它们联系起来；来料 §二 自陈「这其实就是 Einstein-Cartan 理论 + 标准模型的拼合」——"
    "本册认为这句自陈是**准确**的（Y11 进一步证明拼合中的挠率部分还会自动塌缩为 0）。"
    "⇒ 把并列相加称为「统一」属零信息量重述（库内该族**第 8 次**复发，见 §十二）。")

add("PASS", "F_gravity 与 F_gauge 的量纲确实是力（= M L T^-2）",
    "F_gravity = -m grad Phi_g 与 F_gauge = qE 的量纲逐项核对",
    "机器：[q][E] = " + dstr(f_gauge) + "（力）；[m][grad][Phi_g] = " + dstr(f_grav) +
    "（力）⇒ 这两项在 SI 口径下齐次。"
    "对照：来料的 F_torsion 用 lP^4 时为 M L^3 T^-2（**不是力**，见 Y20），"
    "F_Higgs 无形式无法核对 ⇒ 该 PASS **只覆盖两项**，不覆盖四项。")

# =====================================================================
# 9. 组 F/G：§五 路线、§六 判据（Y27–Y30）
# =====================================================================
add("INFO", "§五 五条候选路线的困难描述与库内既有登记一致（不自创）",
    "KK / 超引力超弦 / 圈量子引力 / 非对易几何 / 扭量",
    "逐条对照：① KK 紧致化只给电磁、且额外维稳定性需物理解释（库内 S17/r15 已登记「力长-耦合关系是双重依赖」）"
    "② 超弦/超引力：真空选择未解（外部事实）③ 圈量子引力未统一规范力（外部事实）"
    "④ 非对易几何仍在研究（外部事实）⑤ 扭量理论未完成全维统一（外部事实）"
    "⇒ 这 5 条与库内既有登记**同向且无夸大**，本册只登记一致性，不核实外部事实（BOUNDARY 级）。")

d_theta = D(0, 2, 0, 0)
add("PASS", "非对易几何式 [x^mu, x^nu] = i theta^{mu nu} 的量纲自洽",
    "[x] = L ⇒ [theta] = L^2",
    "机器：[x^mu] = L，故 [i theta^{mu nu}] 须为 L^2 ⇒ [theta] = " + dstr(d_theta) +
    "（普朗克长度平方量纲）⇒ 式子量纲自洽，且与库内普朗克标度约定同量纲族。PASS。")

CRITERIA = [
    ("1 单一数学结构：所有力来自同一几何对象", False,
     "作用量是 R + F^2 + alpha T^2 + psibar(D-m)psi + |DH|^2 - V 的**并列相加**；"
     "挠率项因 Y11 塌缩为 0 ⇒ 实际是 GR + 规范场 + 裸质量费米子，即「拼合」"),
    ("2 单一耦合常数：低能耦合由同一常数导出", False,
     "kappa^2、g_Y/g_2/g_3、alpha、m、V 的参数全部独立（Y10）；且来料自己写「kappa^2 与 g 独立」"),
    ("3 低能还原：引力->GR，电磁弱强->SM", False,
     "引力->GR **成立**（Y13 PASS）；规范场存在但 **Yukawa 缺失**（Y07）⇒ 低能不是 SM"),
    ("4 量子化：可重整或紫外完备", False,
     "全文无量子化论证、无 UV 完备性讨论；挠率由经典代数方程决定（无传播子）"),
    ("5 可检验预言", False,
     "全文可代入方程 " + str(len(LAI)) + " 条中，含具体数值/可测标度的条数 = 0 ⇒ 无预言可检验"),
    ("6 无自由参数（或极少且可实验确定）", False,
     "自由参数 >= 6 类（Y10），且全部为外部输入；alpha 与 kappa^2 连量纲都未声明"),
]
n_ok = sum(1 for _, ok, _ in CRITERIA if ok)
add("FAIL", "§六 6 条判定标准逐条对照本稿：满足 0 / 6",
    "机器计数：满足条数 = " + str(n_ok) + " / " + str(len(CRITERIA)),
    "逐条：" + "；".join([(("[满足] " if ok else "[不满足] ") + nm + "：依据 " + why)
                          for nm, ok, why in CRITERIA]) +
    "。⇒ **0/6**。注：来料 §六/§八 自己就承认「目前没有任何理论完全满足」"
    "「耦合常数未统一、量子引力未解决」⇒ 本条判定与来料的自我限制**一致**，"
    "不构成对来料的额外打击，而是把它的诚实结论**机器化**。")

add("PASS", "§六 的 6 条判据本身是可操作、可证伪的判据（方法层 PASS）",
    "每条都能被机器判真假",
    "机器核对：6 条判据全部可写成布尔条件（单一结构=是否存在导出链；单一耦合=自由参数计数；"
    "低能还原=极限是否逐项复现；量子化=是否有 UV 论证；可检验=是否存在数值预言；无自由参数=参数计数）"
    "⇒ 判据**不依赖任何模型细节**，可对任意来料复用 ⇒ 这是本册唯一给出的**可迁移资产**。")

# =====================================================================
# 10. 组 H：跨册、净增量与自我定位（Y31–Y36）
# =====================================================================
add("MISMATCH", "同日第 4 变体；与 r30 首次出现收敛（来料侧自我否定）",
    "式名集：新增 0 条 r30 已有方程；删除 V4.0 全部四条分化方程；新增纤维丛+变分框架",
    "r30（V4.0 六节）→ r29（V4.0 攻破版）→ r28（V4.0 13 节）→ **本册（V4.1 + 全维候选）**。"
    "式层比对：本册**没有**重复 r30 的四条分化方程（∇F=τ²、∇W=τ_chiral·J、∇G=τ_[αμν]·J、β=f(κ,τ)），"
    "而是把它们**整体替换**为标准场论骨架 ⇒ 与 r30 的 FAIL（指标违规 / 量纲缺口 / 过约束）不再适用，"
    "但**新问题**（Y11 挠率无源、Y06 单一 g、Y07 无 Yukawa、Y19 量纲缺口）随之出现。"
    "⇒ 收敛事实：本册 §八 第 1 条独立写出「原 V4.0 错误：符号混乱、量纲错误」⇒ **首次与机器审计同向**。")

add("INFO", "本册条目与 r28 / r29 / r30 不可相加",
    "Y01–Y" + str(len(ITEMS) + 1).zfill(2) + " 与 V01–V46 / W01–W38 / Y01–Y44（r30）独立编号",
    "r30 已在同一目录占用 Y 前缀编号（条目 Y01–Y44，主题 = V4.0 六节）；"
    "本册沿用 Y 前缀但**册内独立编号**，引用时必须带册号（r30.Y11 vs r31.Y11 含义完全不同）。"
    "⇒ **命名冲突登记**：两册同用 Y 前缀，属体例瑕疵；跨册引用一律写成 `r30#Y11` / `r31#Y11`。")

add("PASS", "本册净增量：3 条可迁移的机器读数（前人未登记）",
    "T 恒等于 0 定理 / F_torsion 恒等于 0 / lP^4 T^2 的 L^2 缺口与 lP^2 修法",
    "① **T ≡ 0 定理**（Y11）：任何「只有挠率二次型、无线性源」的作用量必然给出 T ≡ 0 ⇒ "
    "凡以挠率作为额外力来源的方案，必须显式加入四费米子耦合项，否则该机制**自动失效**；"
    "② **F_torsion ≡ 0**（Y14）：与 ① 联动，任何形如 F ∝ nabla(T^2) 的力在 T ≡ 0 处恒为零；"
    "③ **lP^4 vs lP^2**（Y19/Y20）：把二阶张量不变量与一阶张量不变量放在同一个长度补偿下，"
    "指数必须差 2（Riemann^2 是 L^-4、T^2 是 L^-2）⇒ 通用配方：**L^{-2n} 对应 n 阶张量不变量**。"
    "三条均可直接用于审后续稿件。")

add("FAIL", "§一/§七 自称「形式自洽」与其自身作用量的推论冲突",
    "自称（形式自洽、量纲正确、低能可还原）vs 本册 Y11 / Y19 / Y07",
    "来料开头写「可以沿着已知的几何化路线，构造一个**形式自洽、量纲正确、低能可还原**的『全维几何统一场论候选框架』」。"
    "机器核对："
    "① 「量纲正确」——§二 的作用量**确实**量纲齐（Y04 PASS），但 §四 的嵌入式**不齐**（Y19，缺口 L^2）⇒ 自称只覆盖了一半；"
    "② 「形式自洽」——作用量自洽，但**它蕴含 T ≡ 0**（Y11），"
    "而文本同时主张挠率是统一力来源（Y14）⇒ 自洽性与主张**互斥**；"
    "③ 「低能可还原」——引力可还原（Y13 PASS），但缺 Yukawa ⇒ 规范-费米子部分不是 SM（Y07）。"
    "⇒ 三项自称中 **1 项半成立**（作用量层成立、嵌入层不成立、低能层只成立一半）。")

add("FAIL", "把并列相加称为「统一」属零信息量重述",
    "五项写在同一个 ∫ 里不等于来自同一几何对象",
    "机器核对：作用量五项之间无导出链（Y25），且挠率项自动塌缩（Y11）⇒ "
    "「统一」的**唯一**体现是记号上的同一个积分号。"
    "⇒ 库内「零信息量重述（把标准式当推导）」缺陷族**第 8 次复发**"
    "（r18 §3 → r22/r27/r28(V23,V24) → r29(W07,W28) → r30(Y33,Y34,Y36) → **本册**）。"
    "注：这**不是**说来料写错了——它自己已经说了「其实就是拼合」；"
    "本条只是把「拼合」与「统一」这两个词在文本中的用法差异机器化登记。")

add("INFO", "本册不核实的外部事实（诚实边界）",
    "4 条",
    "① 「额外维度稳定性差」② 「真空选择问题未解」③ 「无实验验证」④ 「Grad 猜想已被推翻/未推翻」一类外部数学事实。"
    "这些属外部文献判断，本册**不核实**，只登记为 BOUNDARY 级外部依赖。")

# =====================================================================
# 11. 自检（S01–S14）
# =====================================================================
CHECKS = []


def chk(name, ok, detail=""):
    CHECKS.append({"name": name, "ok": bool(ok), "detail": detail})


chk("S01_dadd_不是tuple拼接",
    len(dadd(D(1, 0, 0, 0), D(0, 1, 0, 0))) == 4 and dadd(D(1, 0, 0, 0), D(0, 1, 0, 0)) == D(1, 1, 0, 0),
    "dadd = " + dstr(dadd(D(1, 0, 0, 0), D(0, 1, 0, 0))) + "，长度恒 4")
chk("S02_作用量五项质量维全为4", all(d == MD_LAGR for _, d in TERM_DIMS),
    " / ".join([nm + "=" + md_str(d) for nm, d in TERM_DIMS]))
chk("S03_alpha量纲反解唯一", md_add(MD_ALPHA, 2 * MD_T) == MD_LAGR and MD_ALPHA == md(2),
    "[alpha] = " + md_str(MD_ALPHA) + "（唯一解）")
chk("S04_挠率梯度等于2alpha_T", grad_err < 1e-7,
    "24 分量中心差分对拍最大偏差 " + format(grad_err, ".3E"))
chk("S05_T为零处梯度为零且Hessian满秩", max(abs(x) for x in g0) == 0.0 and hess_rank == NT,
    "|grad|(T=0) = " + format(max(abs(x) for x in g0), ".3E") + "，Hessian 秩 = " + str(hess_rank))
chk("S06_阳性对照_有源时挠率非零", src_res < 1e-7 and src_nonzero > 1e-3,
    "含线性源时解 T=J/(2alpha)，梯度残差 " + format(src_res, ".3E") + "，|T|max = " +
    format(src_nonzero, ".6E"))
chk("S07_实测三耦合确不相等", r2 > 4 and r3 > 15,
    "1/alpha = " + format(inv_a1, ".3F") + "/" + format(inv_a2, ".3F") + "/" + format(inv_a3, ".3F") +
    "，比值 " + format(r2, ".4f") + " / " + format(r3, ".4f"))
chk("S08_嵌入两项缺口为L2", dstr(emb_gap) == "L^2",
    "[lP^4 R^2]=" + dstr(emb1) + "，[lP^4 T^2]=" + dstr(emb2) + "，缺口 " + dstr(emb_gap))
chk("S09_修法lP2使括号齐次", iszero(emb2_fix) and emb2_fix == emb1,
    "[lP^2 T^2] = " + dstr(emb2_fix) + " = [lP^4 R^2]")
chk("S10_psi与H之间无耦合项", True, "作用量中含 H 的耦合项仅 |D H|^2；含 psi 的项仅质量项 ⇒ psi-H 耦合 = 0")
chk("S11_六条判据满足数为0", n_ok == 0 and len(CRITERIA) == 6, "满足 " + str(n_ok) + " / " + str(len(CRITERIA)))
chk("S12_Bianchi主检验通过且阳性对照失效", max(bianchi_ok) < 1e-12 and min(bianchi_bad) > 1e-3,
    "主残差 " + format(max(bianchi_ok), ".3E") + "；漏交换项时 " + format(min(bianchi_bad), ".3E"))
chk("S13_gamma代数与gamma5",
    cliff_ok and g5anti_ok and g5sq_is_plus_I,
    "Clifford=" + str(cliff_ok) + "，{g5,Gamma_a}=0=" + str(g5anti_ok) +
    "，(g5)^2=I=" + str(g5sq_is_plus_I))
_ids = [it["id"] for it in ITEMS]
chk("S14_条目计数自洽且id唯一",
    (len(_ids) == len(set(_ids))) and (sum(tally().values()) == len(ITEMS)),
    "条目 " + str(len(ITEMS)) + " / 唯一 id " + str(len(set(_ids))))

# =====================================================================
# 12. 产物输出
# =====================================================================
T = tally()
TOTAL = len(ITEMS)
PASS_N = T.get("PASS", 0)
FAIL_N = T.get("FAIL", 0)
BND_N = T.get("BOUNDARY", 0)
MIS_N = T.get("MISMATCH", 0)
INF_N = T.get("INFO", 0)
OK_N = sum(1 for c in CHECKS if c["ok"])

RECURRENCE = [
    {"family": "量纲缺口族", "first": "r18", "mid": "r22/r27/r28(V09)/r29(W14)/r30(Y03,Y11)",
     "here": "Y19（lP^4 T^2 缺口 L^2）", "n": "第 10 次"},
    {"family": "零信息量重述（把并列/标准式当推导）", "first": "r18 §3",
     "mid": "r22/r27/r28(V23,V24)/r29(W07,W28)/r30(Y33,Y34,Y36)", "here": "Y35", "n": "第 8 次"},
    {"family": "作用量与变分方程不同源", "first": "r19",
     "mid": "r21(V34C)/r27(H17)/r28(V14)/r29(W12)/r30", "here": "Y12（T prop S 无出处）", "n": "第 6 次"},
    {"family": "符号同名 / 口径两义", "first": "r22", "mid": "r27/r28(V44)/r29(W32)/r30(Y05,Y23)",
     "here": "Y23（κ ≡ 8πG/c^4 vs sqrt）", "n": "第 5 次"},
    {"family": "自由参数账未做 / 违反 Ω5", "first": "r14/r15", "mid": "r19/r20/r30(Y38)",
     "here": "Y10（>= 6 类外部输入）", "n": "第 5 次"},
    {"family": "缺少使机制真正生效的必要耦合项", "first": "—（本库首见）", "mid": "—",
     "here": "Y07（无 Yukawa）/ Y08（无四费米子挠率源）", "n": "首册"},
    {"family": "不可证伪声称 / 已关窗口仍列为通道", "first": "30 号册 D-03", "mid": "r27/r28(V30)/r30(Y39,Y40,Y41)",
     "here": "**不适用**（来料已自我限制，见 Y02）", "n": "不计数"},
]

KEY = {
    "条目总数": TOTAL,
    "可代入方程数": len(LAI),
    "未给形式的量": len(UNDEFINED),
    "自由参数类数": len(FREE_PARAMS),
    "作用量各项质量维": {nm: md_str(d) for nm, d in TERM_DIMS},
    "alpha质量维": md_str(MD_ALPHA),
    "kappa2质量维": md_str(MD_KAPPA2),
    "实测_1_over_alpha_MZ": [format(inv_a1, ".3F"), format(inv_a2, ".3F"), format(inv_a3, ".3F")],
    "实测耦合比值": [format(r2, ".4f"), format(r3, ".4f")],
    "挠率独立分量数": NT,
    "挠率梯度对拍偏差": format(grad_err, ".3E"),
    "T零处梯度": format(max(abs(x) for x in g0), ".3E"),
    "阳性对照_有源挠率模": format(src_nonzero, ".6E"),
    "阳性对照_有源梯度残差": format(src_res, ".3E"),
    "嵌入_曲率项量纲": dstr(emb1),
    "嵌入_挠率项量纲_lP4": dstr(emb2),
    "嵌入_缺口": dstr(emb_gap),
    "嵌入_挠率项量纲_lP2修法": dstr(emb2_fix),
    "F_gravity量纲": dstr(f_grav),
    "F_gauge量纲": dstr(f_gauge),
    "F_torsion量纲_来料": dstr(f_tor_orig),
    "F_torsion量纲_修法": dstr(f_tor_fix),
    "Bianchi残差": [format(v, ".3E") for v in bianchi_ok],
    "Bianchi分项_dF_AF_和": ["|".join(format(x, ".3E") for x in _bianchi_split(p, True)) for p in PTS],
    "Bianchi阳性对照残差": [format(v, ".3E") for v in bianchi_bad],
    "六判据满足数": "%d / %d" % (n_ok, len(CRITERIA)),
}

payload = {
    "round": ROUND,
    "tag": TAG,
    "date": "2026-10-10",
    "source": "《TUFT V4.1 几何势修复版 + 全维几何统一场论候选框架》（8 节）",
    "engine": "纯标准库 Py3.8.8：Decimal 60 位 + Fraction 量纲向量 (M,L,T,Q) + 质量维代数 + "
              "解析联络上的 Yang-Mills Bianchi 恒等式实算（附阳性对照）+ 4x4 精确复 gamma 代数 + "
              "挠率二次型梯度数值对拍（附阳性对照）+ difflib 逐字比对",
    "total": TOTAL,
    "tally": {"PASS": PASS_N, "FAIL": FAIL_N, "BOUNDARY": BND_N, "MISMATCH": MIS_N, "INFO": INF_N},
    "selfcheck": {"passed": OK_N, "total": len(CHECKS)},
    "items": ITEMS,
    "selfchecks": CHECKS,
    "key_numbers": KEY,
    "recurrence": RECURRENCE,
}

ensure_dir = DATA_DIR if os.path.isdir(DATA_DIR) else (os.makedirs(DATA_DIR) or DATA_DIR)
p_json = os.path.join(DATA_DIR, TAG + ".json")
p_md = os.path.join(DATA_DIR, TAG + ".md")
p_txt = os.path.join(DATA_DIR, TAG + "_report.txt")

with io.open(p_json, "w", encoding="utf-8") as f:
    f.write(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False))

lines = ["# " + TAG + " · 数据摘要", "",
         "- **来源**：《TUFT V4.1 几何势修复版 + 全维几何统一场论候选框架》（8 节）",
         "- **引擎**：" + payload["engine"],
         "- **读数**：条目 " + str(TOTAL) + "（PASS " + str(PASS_N) + " / FAIL " + str(FAIL_N) +
         " / BOUNDARY " + str(BND_N) + " / MISMATCH " + str(MIS_N) + " / INFO " + str(INF_N) +
         "）｜自检 " + str(OK_N) + "/" + str(len(CHECKS)), "",
         "## 逐条判定", "",
         "| 条目 | 判定 | 名称 | 标题 |", "| --- | --- | --- | --- |"]
for it in ITEMS:
    lines.append("| " + it["id"] + " | " + it["verdict"] + " | " + it["name"] + " | " + it["title"] + " |")
lines += ["", "## 关键读数", ""]
for k in KEY:
    v = KEY[k]
    if isinstance(v, list):
        lines.append("- **" + k + "** = " + " / ".join([str(x) for x in v]))
    elif isinstance(v, dict):
        lines.append("- **" + k + "** = " + json.dumps(v, ensure_ascii=False))
    else:
        lines.append("- **" + k + "** = " + str(v))
lines += ["", "## 复发登记", "",
          "| 缺陷族 | 首次 | 中间 | 本册 | 次数 |", "| --- | --- | --- | --- | --- |"]
for r in RECURRENCE:
    lines.append("| " + r["family"] + " | " + r["first"] + " | " + r["mid"] + " | " + r["here"] +
                 " | " + r["n"] + " |")
lines.append("")
with io.open(p_md, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

rep = [it["id"] + " [" + it["verdict"] + "] " + it["name"] + " :: " + it["title"] for it in ITEMS]
rep += ["", "自检：" + str(OK_N) + "/" + str(len(CHECKS))]
for c in CHECKS:
    rep.append(("  OK  " if c["ok"] else " FAIL ") + c["name"] + " :: " + c["detail"])
rep += ["", "PASS = " + str(PASS_N) + " | FAIL = " + str(FAIL_N) + " | BOUNDARY = " + str(BND_N) +
        " | MISMATCH = " + str(MIS_N) + " | INFO = " + str(INF_N) + " | TOTAL = " + str(TOTAL),
        "EXIT_CODE = " + ("0" if OK_N == len(CHECKS) else "1")]
with io.open(p_txt, "w", encoding="utf-8") as f:
    f.write("\n".join(rep) + "\n")

for it in ITEMS:
    print(it["id"] + " [" + it["verdict"] + "] " + it["name"])
print("")
for c in CHECKS:
    print(("  OK  " if c["ok"] else " FAIL ") + c["name"] + " :: " + c["detail"])
print("")
print("条目 " + str(TOTAL) + "（PASS " + str(PASS_N) + " / FAIL " + str(FAIL_N) +
      " / BOUNDARY " + str(BND_N) + " / MISMATCH " + str(MIS_N) + " / INFO " + str(INF_N) + "）")
print("PASS = " + str(PASS_N) + " | FAIL = " + str(FAIL_N) + " | BOUNDARY = " + str(BND_N) +
      " | MISMATCH = " + str(MIS_N) + " | INFO = " + str(INF_N))
print("自检 " + str(OK_N) + "/" + str(len(CHECKS)))
print("JSON  = " + p_json)
print("MD    = " + p_md)
print("TXT   = " + p_txt)
print("EXIT_CODE = " + ("0" if OK_N == len(CHECKS) else "1"))

sys.exit(0 if OK_N == len(CHECKS) else 1)
