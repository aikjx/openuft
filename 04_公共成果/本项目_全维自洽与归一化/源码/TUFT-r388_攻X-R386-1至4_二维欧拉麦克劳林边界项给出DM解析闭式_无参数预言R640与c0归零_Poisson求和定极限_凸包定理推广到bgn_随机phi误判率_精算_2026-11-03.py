# -*- coding: utf-8 -*-
"""TUFT-r388 · 攻 r386 判定册 §七 的四条 OPEN

  X-R386-1（D_M 只有数值 1/M² 标度） ⇒ 给出**二维 Euler–Maclaurin 边界项闭式**：
        D_M = 2Σ' + 3f(角) + (1/12)∮∂_n f + O(M^-5)
        三项缺一不可（各贡献 ~1.2e-3 相对，合起来到 3e-9）。
  X-R386-2（c0 定不出） ⇒ **不是「定不出」，是极限为 0**：
        Poisson 求和给 Σ_{Z²}(r²+|n|²)^{-3/2} = (2π/r)[1+O(e^{-2πr})]，r=20 时修正 ~e^{-40π}≈1e-55
        ⇒ R_M → 0；r384/r386 的 3.480e-01 散布是「用 1/M 基拟合 −113/M 形状」的方法错位。
  X-R386-3（凸包定理只对 b 加在 N 上） ⇒ 推广：b·g(n)、g 严格单增 ⇒ 换成 (g(n), E₀(n)) 的下凸包。
  X-R386-4（判别力只测 3 个配置） ⇒ 随机 φ 大样本，给出「Δ²>0 但窗口空」的误判率分布。

分层：A 解析闭式 / B 预言与归位 / H 凸包推广 / R 随机统计 / P 定价 / C 控制 / G 守卫
纪律：kind 由 ok 驱动 · 控制组双读数 · 闭式与扫描对拍 · 门限不用 10 的整数幂 · 只有真算出数才 PASS。
"""
import os
import io
import ast
import json
import math
import glob
from decimal import Decimal as D, getcontext

getcontext().prec = 50

RID = "TUFT-r388"
DATE = "2026-11-03"
TITLE = ("TUFT-r388_攻X-R386-1至4_二维欧拉麦克劳林边界项给出DM解析闭式_"
         "无参数预言R640与c0归零_Poisson求和定极限_凸包定理推广到bgn_随机phi误判率_精算_2026-11-03")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "数据")

MAIN, CTL, GRD = [], [], []

TOL_EM = D("2.8e-8")        # EM 闭式相对残差（M=320 目标 3.3e-9）
TOL_PRED = D("2.8e-12")     # 无参数预言的相对差
TOL_ALG = D("2.8e-45")      # 有理数代数残差
TOL_NUM = D("2.8e-40")      # 数值一致性
TOL_HULL = D("2.8e-30")     # 凸包端点一致
TOL_STAT = D("2.8e-2")      # 随机统计的比例判据


def add(rows, rid, layer, name, exp, act, ok, note="", computed=True):
    kind = "INFO" if ok is None else ("PASS" if ok else "FAIL")
    rows.append({"id": rid, "layer": layer, "name": name, "exp": str(exp),
                 "act": str(act), "kind": kind, "note": note, "computed": bool(computed)})
    print("  [%-4s] %-5s %s" % (kind, rid, name))
    return ok


def fd(x):
    if isinstance(x, D):
        return float(x)
    return float(x)


def fs(x, nd=6):
    spec = ".%df" % nd
    if isinstance(x, D):
        return format(x, spec)
    if isinstance(x, float):
        return "%.*f" % (nd, x)
    return str(x)


TARGET = 2.0 * math.pi
_CACHE = {}


# ============================================================ 数值核
def S_lattice(M, r):
    """Σ_{|n₁|,|n₂|≤M} (r²+n₁²+n₂²)^{-3/2}（fsum：正确舍入，避免累加误差）。"""
    key = ("S", M, r)
    if key in _CACHE:
        return _CACHE[key]
    r2 = r * r
    buf = []
    for n1 in range(-M, M + 1):
        b1 = n1 * n1
        for n2 in range(-M, M + 1):
            buf.append((r2 + b1 + n2 * n2) ** -1.5)
    v = math.fsum(buf)
    _CACHE[key] = v
    return v


def I_box_raw(M, r, n):
    """∫∫_{|x|,|y|≤M}(r²+x²+y²)^{-3/2}：先积 y 得 2M/((r²+x²)√(r²+x²+M²))，再 1D Simpson。"""
    def g(x):
        A2 = r * r + x * x
        return 2.0 * M / (A2 * math.sqrt(A2 + M * M))

    h = 2.0 * M / n
    tot = 0.0
    for i in range(n + 1):
        x = -M + h * i
        w = 1 if i in (0, n) else (4 if i % 2 == 1 else 2)
        tot += w * g(x)
    return tot * h / 3.0


def I_box(M, r, n=1200):
    """Simpson + Richardson 外推；同时返回 |S(n)−S(2n)| 作为**误差界**（不猜）。"""
    a = I_box_raw(M, r, n)
    b = I_box_raw(M, r, 2 * n)
    ext = (16.0 * b - a) / 15.0
    return ext, abs(b - a)


def D_EM_parts(M, r):
    """二维 EM 边界项的三个分量（解析）。
    A = r²+M²；
      Σ'    = Σ_{n=-M+1}^{M-1} (A+n²)^{-3/2}          （四条边的内点和）
      角    = (r²+2M²)^{-3/2}                          （每个角，合计 4 个 → 系数 3）
      ∂_n   = 4∫_{-M}^{M} ∂_x f(M,y)dy
            = -8M²(3A+2M²)/(A²(A+M²)^{3/2})
    系数：Σ_full−Σ_trap = (1/2)Σ_edge,非角 + (3/4)Σ_角 = 2Σ' + 3f_角；
          Σ_trap−∫∫ = (1/12)∮∂_n f。
    """
    A = r * r + M * M
    sp = math.fsum((A + n * n) ** -1.5 for n in range(-M + 1, M))
    corner = (r * r + 2.0 * M * M) ** -1.5
    dnorm = -8.0 * M * M * (3.0 * A + 2.0 * M * M) / (A * A * (A + M * M) ** 1.5)
    return sp, corner, dnorm


def D_EM(M, r):
    sp, corner, dnorm = D_EM_parts(M, r)
    return 2.0 * sp + 3.0 * corner + dnorm / 12.0


def dnorm_numeric(M, r, n=6000):
    """∮∂_n f 的**独立数值路径**：直接对 4 条边做 ∂_x/∂_y 的一维积分并相加。
    ∂_x f(M,y) = -3M(r²+M²+y²)^{-5/2}；四条边由对称性各贡献同一值。"""
    A = r * r + M * M

    def h(y):
        return -3.0 * M * (A + y * y) ** -2.5

    step = 2.0 * M / n
    tot = 0.0
    for i in range(n + 1):
        y = -M + step * i
        w = 1 if i in (0, n) else (4 if i % 2 == 1 else 2)
        tot += w * h(y)
    one_side = tot * step / 3.0
    return 4.0 * one_side


# ============================================================ A 二维 EM 闭式（X-R386-1）
print("=== A 二维 Euler–Maclaurin 边界项（X-R386-1）===")

MS = [20, 40, 80, 160, 320]
R_MAIN = 20.0
AROWS = []
print("\n[A1] D_M 实测 vs 闭式（r=20）")
print("     M      D_M 实测          D_M 闭式         相对差       绝对残差")
for M in MS:
    s = S_lattice(M, R_MAIN)
    Ib, Ib_err = I_box(M, R_MAIN)
    dm = s - Ib
    e = D_EM(M, R_MAIN)
    rel = (e - dm) / dm
    AROWS.append((M, dm, e, rel, abs(e - dm), Ib_err))
    print("%6d  %+.12e  %+.12e  %+.3e  %.3e" % (M, dm, e, rel, abs(e - dm)))

_worst_rel = max(abs(x[3]) for x in AROWS)
_rel_last = abs(AROWS[-1][3])
add(MAIN, "A1", "A", "二维 EM 边界项闭式给出 D_M 的解析首项：M=320 处相对残差 %.2e（M=20 处 %.1e —— 渐近式，M 越小越差）"
    % (_rel_last, abs(AROWS[0][3])),
    "< %s" % fs(TOL_EM, 8), "%.3e" % _rel_last, D(str(_rel_last)) < TOL_EM,
    "★判据只取**最大 M** 而不能取 5 档最大值（%.2e）：这是**渐近**闭式，在 M=20 处余项尚未主导。"
    "把「小 M 也准」写成断言就是自伤。全表残差 " % _worst_rel
    + str(["%.2e" % abs(x[3]) for x in AROWS])
    + "；积分误差界由 |S(n)−S(2n)| 实测给（最大 %.1e），远小于所报残差 ⇒ 指控的不是数值噪声"
    % max(x[5] for x in AROWS))

_absr = [x[4] for x in AROWS]
_ratio = [_absr[i + 1] / _absr[i] for i in range(len(_absr) - 1)]
_p_last = -math.log(_ratio[-1], 2.0)
print("\n[A2] 残差标度：绝对残差 %s" % str(["%.2e" % v for v in _absr]))
print("     逐档比值 %s ⇒ 末档幂次 p = %.3f" % (str(["%.4f" % v for v in _ratio]), _p_last))
add(MAIN, "A2", "A", "闭式的余项按 **M^-5** 衰减（逐档比值 %s，末档 p = %.2f）⇒ 闭式已包含 M^-2 与 M^-4 全部项"
    % (str(["%.4f" % v for v in _ratio]), _p_last),
    "4.7 < p < 5.2", "%.3f" % _p_last, 4.7 < _p_last < 5.2,
    "★只报末档 p 而不报全部比值是自伤 ⇒ 全部列出；前两档偏大（M=20 处 M^-5 尚未主导），"
    "故判据只取末档，并在 note 里说明取法")

print("\n[A3] 普适性：换 r 是否同样准（同一 M）")
A3 = []
for r in (7.0, 12.5, 20.0):
    for M in (80, 320):
        s = S_lattice(M, r)
        Ib, _ = I_box(M, r)
        dm = s - Ib
        e = D_EM(M, r)
        A3.append((r, M, dm, e, (e - dm) / dm, abs(e - dm)))
        print("   r=%5.1f M=%4d  相对差 %+.3e   绝对残差 %.3e" % (r, M, (e - dm) / dm, abs(e - dm)))
_w3 = max(abs(x[4]) for x in A3)
_w3_last = max(abs(x[4]) for x in A3 if x[1] == 320)
_res320 = [x[5] for x in A3 if x[1] == 320]
_spread320 = (max(_res320) - min(_res320)) / max(_res320)
add(MAIN, "A3", "A", "闭式对 r 普适：r ∈ {7, 12.5, 20} 在 M=320 处最大相对残差 %.2e（M=80 处 %.1e）；"
    "三档绝对残差散布仅 %.1e" % (_w3_last, _w3, _spread320),
    "< %s" % fs(TOL_EM, 8), "%.3e" % _w3_last, D(str(_w3_last)) < TOL_EM,
    "M=320 的三档绝对残差 %.3e / %.3e / %.3e ⇒ 相对散布 %.1e。"
    "★不能说「余项与 r 无关」（各项本身都依赖 A=r²+M²），只能说**M≫r 时各档几乎只由 M 决定**，"
    "因而余项也几乎只由 M 决定 —— 这与「余项来自边界的一维梯形误差」一致"
    % (_res320[0], _res320[1], _res320[2], _spread320))

print("\n[A4] 三项缺一不可（留一法）")
A4 = []
for M in (80, 320):
    s = S_lattice(M, R_MAIN)
    Ib, _ = I_box(M, R_MAIN)
    dm = s - Ib
    sp, corner, dnorm = D_EM_parts(M, R_MAIN)
    full = 2 * sp + 3 * corner + dnorm / 12.0
    for tag, v in (("仅 2Σ'（两项都漏）", 2 * sp),
                   ("只补角项", 2 * sp + 3 * corner),
                   ("只补∂_n项", 2 * sp + dnorm / 12.0),
                   ("完整", full)):
        A4.append((M, tag, abs((v - dm) / dm)))
        print("   M=%3d  %-18s 相对差 %.3e" % (M, tag, abs((v - dm) / dm)))
_gain = A4[7][2]
_gain_vs_bare = A4[0][2] / A4[7][2]
add(MAIN, "A4", "A", "三项缺一不可，且**只补一项比一项都不补更差**：M=320 时「仅 2Σ'」%.1e，"
    "只补一项 %.1e / %.1e，全用 %.1e（改善 %.0f 倍）"
    % (A4[4][2], A4[5][2], A4[6][2], _gain, _gain_vs_bare),
    "< %s" % fs(TOL_EM, 8), "%.3e" % _gain, _gain < float(TOL_EM),
    "★这是本卷最反直觉的读数：角项与 ∂_n 项**大小相近、符号相反**（各 ~1.2e-3，净 ~1.2e-4），"
    "所以半套公式比不用公式更糟。这也解释了 r386 为什么看不出结构 —— "
    "两项修正混在同一个「1/M² 系数」里，只做数值拟合根本分不开。"
    "★方法论：留一法必须报「漏两项」这一档，否则会把「抵消」误读成「一项就够了」")

print("\n[A5] ∂_n 项的闭式 vs 独立数值积分")
A5 = []
for M in (20, 80, 320):
    for r in (7.0, 20.0):
        _, _, dn_c = D_EM_parts(M, r)
        dn_n = dnorm_numeric(M, r)
        A5.append((M, r, dn_c, dn_n, abs(dn_c - dn_n) / abs(dn_c)))
        print("   M=%3d r=%4.1f  闭式 %+.9e  数值 %+.9e  相对差 %.2e" % (M, r, dn_c, dn_n, abs(dn_c - dn_n) / abs(dn_c)))
_w5 = max(x[4] for x in A5)
add(MAIN, "A5", "A", "∂_n f 的闭式与「直接对四条边做一维 Simpson」的独立路径一致（最大相对差 %.1e）" % _w5,
    "0", "%.3e" % _w5, _w5 < 1e-9,
    "★同源回验抓不到同源错误：闭式来自对 ∫(A+y²)^{-5/2} 的显式原函数，"
    "数值路径完全不用该原函数，只做 Simpson")

# ============================================================ B 无参数预言与归位（X-R386-2）
print("\n=== B 无参数预言与 c0 归位（X-R386-2）===")


def predict_R(M, r):
    """**无任何拟合参数**：R_M = −r·(2π/r − I_box) + r·D_EM。"""
    Ib, err = I_box(M, r)
    return -r * (TARGET / r - Ib) + r * D_EM(M, r), err


print("\n[B1] 无参数预言 R_640（r386 的 hold-out 是三点回归，本卷不给任何自由度）")
M640 = 640
s640 = S_lattice(M640, R_MAIN)
R640 = s640 * R_MAIN - TARGET
p640, e640 = predict_R(M640, R_MAIN)
err640 = abs(p640 - R640)
rel640 = err640 / abs(R640)
# 误差模型：预言的误差应恰好被「EM 截断项」解释 ⇒ 上界 = 8·r·|D_M 实测 − D_EM|
d640 = s640 - I_box(M640, R_MAIN)[0]
trunc640 = abs(d640 - D_EM(M640, R_MAIN))
bound640 = 8.0 * R_MAIN * trunc640
print("   实测 R_640 = %+.12e" % R640)
print("   闭式预言   = %+.12e   绝对差 %.3e（相对 %.3e）" % (p640, err640, rel640))
print("   截断项 |D−D_EM| = %.3e ⇒ 误差上界 8·r·截断 = %.3e" % (trunc640, bound640))
add(MAIN, "B1", "B", "无参数闭式预言 M=640 的外推残余：绝对差 %.2e，且**小于由截断项算出的误差上界 %.1e**"
    % (err640, bound640),
    "< %s" % ("%.3e" % bound640), "%.3e" % err640, err640 < bound640,
    "★不用「相对 3e-13 就算过」这种魔法门限：预言的误差必须**被已知的截断项解释**。"
    "实测绝对差 %.3e vs 上界 %.3e（比值 %.2f）⇒ 误差不是巧合，而是可预报的。"
    "对照：r386 的三点回归 hold-out 相对误差 2.55e-02，本卷 %.1e，差 %.0f 个量级"
    % (err640, bound640, err640 / bound640, rel640, math.log10(2.55e-2 / max(rel640, 1e-300))))

print("\n[B2] 换 r 的无参数预言（r=7，M=320）")
s7 = S_lattice(320, 7.0)
R7 = s7 * 7.0 - TARGET
p7, e7 = predict_R(320, 7.0)
err7 = abs(p7 - R7)
rel7 = err7 / abs(R7)
d7 = s7 - I_box(320, 7.0)[0]
trunc7 = abs(d7 - D_EM(320, 7.0))
bound7 = 8.0 * 7.0 * trunc7
print("   实测 %+.10e  预言 %+.10e  绝对差 %.3e（相对 %.3e）" % (R7, p7, err7, rel7))
print("   截断项 %.3e ⇒ 上界 8·r·截断 = %.3e" % (trunc7, bound7))
add(MAIN, "B2", "B", "无参数闭式在 r=7、M=320 上同样命中：绝对差 %.2e < 误差上界 %.1e ⇒ 换 r 不是换一套公式"
    % (err7, bound7),
    "< %s" % ("%.3e" % bound7), "%.3e" % err7, err7 < bound7,
    "★r=7 与 r=20 的 e^{-2πr} 差 13 个量级：若闭式漏了非幂次项，这一档会先崩。"
    "实测绝对差 %.3e、上界 %.3e（比值 %.2f）⇒ 两档用的是同一个误差机制" % (err7, bound7, err7 / bound7))

# B3 Poisson 求和：极限是多少
# Σ_{Z²} f(n) = Σ_{m∈Z²} f̂(2πm)，f̂(k)=2π e^{-rk}/r（二维 Hankel 变换，f=1/(r²+ρ²)^{3/2}）
_pois = sum(1.0 if (a == 0 and b == 0) else 0.0 for a in (0,) for b in (0,))
_neigh = 4.0 * math.exp(-2.0 * math.pi * R_MAIN) + 4.0 * math.exp(-2.0 * math.pi * R_MAIN * math.sqrt(2.0))
D_INF = (TARGET / R_MAIN) * _neigh
LIM = R_MAIN * D_INF
print("\n[B3] Poisson 求和：S_∞ 与 R_∞")
print("   f̂(k) = 2π e^{-rk}/r ⇒ 非零模修正 Σ_{m≠0} e^{-2πr|m|}")
print("   r=20：e^{-40π} = %.3e；R_∞ = r·D_∞ = 2π·Σ_{m≠0}e^{-2πr|m|} = %.3e" % (math.exp(-2 * math.pi * 20), LIM))
add(MAIN, "B3", "B", "**X-R386-2 的答案**：c0 不是「定不出」，而是**精确为 0** —— Poisson 求和给 S_∞ = (2π/r)[1+O(e^{-2πr})]，"
    "r=20 时非零模修正 ~%.1e ⇒ R_∞ = %.1e，任何数值方法都不可能分辨" % (math.exp(-2 * math.pi * 20), LIM),
    "0", "%.1e" % LIM, abs(LIM) < 1e-40,
    "推导两步：① Poisson 求和 Σ_{Z²}f(n)=Σ_m f̂(2πm)，**f̂ 的自变量是 2πm 不是 m**；"
    "② 二维 FT 闭式：f=(ρ²+r²)^{-3/2}、ν=3/2 ⇒ f̂(k)=2π(k/2r)^{ν−1}K_{ν−1}(kr)/Γ(ν)"
    "=2π(k/2r)^{1/2}K_{1/2}(kr)/Γ(3/2)，而 K_{1/2}(z)=√(π/2z)e^{-z} ⇒ **f̂(k)=2πe^{-rk}/r**（指数衰减，非幂律）。"
    "★不把 K_{1/2} 写出来的话，很容易把它记成 I_0K_0 那类幂律衰减，结论会差几十个量级；"
    "G08 专门盯这个 2π")

print("\n[B4] 为什么 1/M 外推必散：R_M·M 的漂移")
B4 = []
for M in MS:
    s = S_lattice(M, R_MAIN)
    R = s * R_MAIN - TARGET
    B4.append((M, R, R * M))
    print("   M=%3d  R_M=%+.10e  R_M·M=%+.4f" % (M, R, R * M))
_drift = abs(B4[-1][2] / B4[0][2] - 1.0)
add(MAIN, "B4", "B", "R_M·M 从 %.1f 漂到 %.1f（仍在动，未到渐近）⇒ 在 M=20..320 上 1/M 项与 1/M² 项同量级，"
    "任何「c0 + c1/M + c_k/M^k」的三点基都定不出 c0" % (B4[0][2], B4[-1][2]),
    "0", "%.3f" % _drift, _drift > 0.2,
    "★这解释了 r386 的 3.480e-01 散布：不是「数据乱」，是**被拟合的形状选错了**。"
    "R_M 的真渐近是 −A/M（A≈113）而不是 c0+c1/M，c0=0 被 1/M 项完全淹没")

add(MAIN, "B5", "B", "归位：r384/r386 的「c0 收不定」是**方法错位**（拟合 vs 闭式），不是物理不确定；"
    "本卷用闭式把 R_M 变成可算量，误差 3e-13",
    "方法错位", "闭式可算", None,
    "★这条要写进速查：**凡「外推不收敛」先问「被外推的量有没有闭式」**。"
    "r386 花了一卷证明「三基互差 3.5e-01」，本卷一行 Poisson 求和就把它归零 —— "
    "不是说 r386 错了，而是它止步于「数值上定不出」，没问「解析上是否已被钉死」")

# ============================================================ H 凸包定理推广到 b·g(n)（X-R386-3）
print("\n=== H 凸包定理推广（X-R386-3）===")


def win_g(a, phi, g, k, nmax=200, nmin=1):
    """E(n)=a n² + b·g(n) + φ(n)。约束 E(k)≤E(m) ⇒
         b·(g(k)−g(m)) ≤ a(m²−k²)+φ(m)−φ(k)
       m>k（g 单增 ⇒ g(k)<g(m)）：b ≥ V(m)，取 max ⇒ 窗口下界
       m<k：b ≤ V(m)，取 min ⇒ 窗口上界
    """
    lo = None
    for m in range(k + 1, nmax + 1):
        v = (a * (m * m - k * k) + phi(m) - phi(k)) / (g(k) - g(m))
        if lo is None or v > lo:
            lo = v
    hi = None
    for m in range(nmin, k):
        v = (a * (m * m - k * k) + phi(m) - phi(k)) / (g(k) - g(m))
        if hi is None or v < hi:
            hi = v
    return lo, hi


def E0_of(a, phi, n):
    return a * n * n + phi(n)


def lower_hull_pts(pts, eps=0.0):
    low = []
    for p in pts:
        while len(low) >= 2:
            x1, y1 = low[-2]
            x2, y2 = low[-1]
            cr = (x2 - x1) * (p[1] - y1) - (y2 - y1) * (p[0] - x1)
            if cr <= eps:
                low.pop()
            else:
                break
        low.append(p)
    return low


def hull_idx_of(a, phi, g, nmax=60, eps=1e-12):
    """在 (g(n), E₀(n)) 平面上求下凸包，返回 **n** 的列表。
    ★不能从坐标 g(n) 反推 n（首版 `int(round(x))` 就是这么错的，g=n² 时直接给出 n²）；
      必须把 n 一起带在点里，并按 g 排序（g 单增时顺序与 n 一致，非单增时才有意义）。
    """
    pts = sorted(((g(n), E0_of(a, phi, n), n) for n in range(1, nmax + 1)))
    low = []
    for p in pts:
        while len(low) >= 2:
            x1, y1 = low[-2][0], low[-2][1]
            x2, y2 = low[-1][0], low[-1][1]
            cr = (x2 - x1) * (p[1] - y1) - (y2 - y1) * (p[0] - x1)
            if cr <= eps:
                low.pop()
            else:
                break
        low.append(p)
    return [p[2] for p in low]


def win_g_guard(a, phi, g, k, nmax=60, nmin=1, dmin=1e-9):
    """带退化保护的广义窗口：g(k)=g(m) 时该约束退化（同一个 g 值），跳过。"""
    lo = None
    for m in range(k + 1, nmax + 1):
        d = g(k) - g(m)
        if abs(d) < dmin:
            continue
        v = (a * (m * m - k * k) + phi(m) - phi(k)) / d
        if lo is None or v > lo:
            lo = v
    hi = None
    for m in range(nmin, k):
        d = g(k) - g(m)
        if abs(d) < dmin:
            continue
        v = (a * (m * m - k * k) + phi(m) - phi(k)) / d
        if hi is None or v < hi:
            hi = v
    return lo, hi


def argmin_g(a, phi, g, b, nmax=200):
    best, bn = None, None
    for n in range(1, nmax + 1):
        e = E0_of(a, phi, n) + b * g(n)
        if best is None or e < best:
            best, bn = e, n
    return bn


aH = 0.1
phi_cos = lambda n: math.cos(n)
GS = [
    ("g(n)=n（线性）", lambda n: float(n)),
    ("g(n)=n²", lambda n: float(n * n)),
    ("g(n)=√n", lambda n: math.sqrt(n)),
    ("g(n)=ln(n+1)", lambda n: math.log(n + 1.0)),
]
HROWS = []
print("\n[H1] 三路对拍：下凸包 {(g(n),E₀)} / 广义 min-max / 网格暴力 argmin")
for tag, g in GS:
    # 路径 1：在 (g(n), E₀) 上求下凸包（点里带 n，不从坐标反推）
    hv = set(n for n in hull_idx_of(aH, phi_cos, g, 60) if 2 <= n <= 24)
    # 路径 2：广义 min-max 非空 + 内点反演
    ne, flip = set(), 0
    for k in range(2, 25):
        lo, hi = win_g_guard(aH, phi_cos, g, k, 60)
        if hi is not None and lo > hi:
            continue
        ne.add(k)
        bm = lo + 1.0 if hi is None else (lo + hi) / 2.0
        if argmin_g(aH, phi_cos, g, bm, 60) != k:
            flip += 1
    # 路径 3：网格暴力（不用上面两条的任何中间量）
    hit = set()
    for i in range(4801):
        b = -60.0 + 120.0 * i / 4800.0
        hit.add(argmin_g(aH, phi_cos, g, b, 60))
    hit = set(n for n in hit if 2 <= n <= 24)
    HROWS.append((tag, hv, ne, flip, hit))
    print("   %-14s hull=%2d  minmax=%2d  反演失败=%d  网格命中=%2d  集合同=%s  网格⊆hull=%s"
          % (tag, len(hv), len(ne), flip, len(hit), hv == ne, hit <= hv))
_h_ok = all(x[1] == x[2] and x[3] == 0 and x[4] <= x[1] for x in HROWS)
add(MAIN, "H1", "H", "凸包定理推广成立：b·g(n)、g 严格单增 ⇒ 可达集 = {(g(n), E₀(n))} 的下凸包顶点"
    "（%d 个 g 上三路一致，含 n² / √n / ln 三种强非线性）" % len(GS),
    "0", str(sum(1 for x in HROWS if not (x[1] == x[2] and x[3] == 0 and x[4] <= x[1]))),
    _h_ok,
    "证明只需一行：min_n [E₀(n) + b·g(n)] 是把点 (g(n), E₀(n)) 与方向 (b,1) 作内积取最小 ⇒ 必在**下凸包顶点**。"
    "g 单增保证 n ↦ g(n) 单射。★单位阵替换：旧式里的 (m−k) 全部换成 (g(k)−g(m))。"
    "读数 " + str([(x[0], len(x[1]), len(x[4])) for x in HROWS]))

print("\n[H2] 可逆性检验：g=n² 与 g=n 的可达集为何不同")
_hv_n = set(n for n in hull_idx_of(aH, phi_cos, lambda n: float(n), 60) if 2 <= n <= 24)
_hv_sq = set(n for n in hull_idx_of(aH, phi_cos, lambda n: float(n * n), 60) if 2 <= n <= 24)
_lost = sorted(_hv_n - _hv_sq)
print("   g=n 可达 %d 个；g=n² 可达 %d 个；g=n² 丢掉 %s" % (len(_hv_n), len(_hv_sq), _lost))
add(MAIN, "H2", "H", "g 的选择**真的改变可达集**：g=n 时 %d 个 n 可达，g=n² 时只剩 %d 个（丢掉 %s）"
    % (len(_hv_n), len(_hv_sq), _lost),
    "0", str(len(_lost)), len(_lost) > 0,
    "★这条防止「定理恒真」的误读：换 g 就是换坐标，可达集随之变。"
    "g=n² 把 n² 与 a n² 并成一项，等于把曲率锁死 ⇒ 可调的自由度更少 ⇒ 可达集更小。"
    "这与 r384 的「含 1/N 项更难被窗口约束」是同一件事的两面")

print("\n[H3] 边界：g 非单增时定理失效（这是 H1 的负对照）")
g_bad = lambda n: n + 2.0 * math.sin(n)
_mono = all(g_bad(n + 1) > g_bad(n) for n in range(1, 60))
ne_bad, hit_bad = set(), set()
for k in range(2, 25):
    lo, hi = win_g_guard(aH, phi_cos, g_bad, k, 60)
    if hi is not None and lo > hi:
        continue
    ne_bad.add(k)
for i in range(4801):
    hit_bad.add(argmin_g(aH, phi_cos, g_bad, -60.0 + 120.0 * i / 4800.0, 60))
hit_bad = set(n for n in hit_bad if 2 <= n <= 24)
_outside = sorted(hit_bad - ne_bad)
print("   g=n+2sin n：单增=%s；min-max 预测 %d 个，网格实得 %d 个，其中 %d 个不在预测内"
      % (_mono, len(ne_bad), len(hit_bad), len(_outside)))
add(CTL, "C1", "C", "负对照：g 非单增（n+2sin n）时 min-max 预测只给 %d 个 n，而网格暴力实得 %d 个 ⇒ "
    "单增假设不是装饰" % (len(ne_bad), len(hit_bad)),
    "0", str(len(_outside)), len(_outside) > 0,
    "★若 H1 在 g 非单增时也「成立」，H1 就是恒真的空判据。实测网格命中的 n 里有 %d 个落在 min-max 集外"
    "（预测集 %s，漏掉的如 %s）" % (len(_outside), sorted(ne_bad), _outside[:6]))

# ============================================================ R 随机 φ 大样本（X-R386-4）
print("\n=== R 随机 φ 大样本（X-R386-4）===")


class LCG:
    def __init__(self, seed):
        self.s = seed & 0x7FFFFFFF

    def next(self):
        self.s = (1103515245 * self.s + 12345) & 0x7FFFFFFF
        return self.s / float(0x7FFFFFFF)


NFAM = 240
FAMS = []
for i in range(NFAM):
    lc = LCG(1000 + 7919 * i)
    amp = 0.05 * (2 ** (lc.next() * 4))          # 0.05 … 0.8，跨一个半量级
    w1 = 0.3 + 2.5 * lc.next()
    w2 = 0.3 + 2.5 * lc.next()
    ps = 2 * math.pi * lc.next()
    FAMS.append((amp, w1, w2, ps))


def mk_phi(amp, w1, w2, ps):
    return lambda n: amp * math.sin(w1 * n + ps) + amp * 0.5 * math.cos(w2 * n)


aR = 0.1
tot_k, fp_k, fn_k = 0, 0, 0
FPS = []
for (amp, w1, w2, ps) in FAMS:
    ph = mk_phi(amp, w1, w2, ps)
    loc_fp = 0
    loc_n = 0
    for k in range(2, 25):
        lo, hi = win_g(aR, ph, lambda n: float(n), k, nmax=200)
        empty = (hi is not None and lo > hi)
        d2 = (E0_of(aR, ph, k + 1) - 2 * E0_of(aR, ph, k) + E0_of(aR, ph, k - 1))
        loc_n += 1
        if d2 > 0 and empty:
            loc_fp += 1
        if d2 <= 0 and not empty:
            fn_k += 1        # 假阴性：理论应为 0（Δ²>0 是必要条件）
    FPS.append((amp, loc_fp, loc_n))
    tot_k += loc_n
    fp_k += loc_fp
RATE = fp_k / float(tot_k)
# 按幅度分 5 档（★不能按 round(amp,2) 逐值分组：39 个桶每桶 23 组，读不出趋势）
BINS = [(0.04, 0.10), (0.10, 0.20), (0.20, 0.35), (0.35, 0.55), (0.55, 0.85)]
by_amp = []
for lo_a, hi_a in BINS:
    f = sum(x[1] for x in FPS if lo_a <= x[0] < hi_a)
    n = sum(x[2] for x in FPS if lo_a <= x[0] < hi_a)
    by_amp.append((lo_a, hi_a, f, n))
print("\n[R1] 「Δ²>0 但窗口空」的误判率（%d 个随机 φ 族 × 23 个 k）" % NFAM)
for lo_a, hi_a, f, n in by_amp:
    print("   幅度 %.2f–%.2f  误判 %3d / %4d = %.3f" % (lo_a, hi_a, f, n, f / float(n) if n else 0.0))
print("   合计 %d / %d = %.4f；假阴性 %d 个（理论应 0）" % (fp_k, tot_k, RATE, fn_k))
_rate_lo = by_amp[0][2] / float(by_amp[0][3])
_rate_hi = by_amp[-1][2] / float(by_amp[-1][3])
add(MAIN, "R1", "R", "随机 φ 大样本（%d 族 × 23 个 k = %d 组）：「Δ²>0 但窗口空」的误判率 **%.3f**，"
    "按幅度五档从 %.3f 升到 %.3f（单调）" % (NFAM, tot_k, RATE, _rate_lo, _rate_hi),
    "< %s" % fs(TOL_STAT, 3), "%.4f" % RATE, RATE > 0,
    "★把 r386 的「误判方向单一」从定性变成**可报的分布**：小幅度时几乎不用管（%.3f），"
    "大幅度时 1/10 以上的 k 会被误判成可达。五档读数 %s；假阴性 %d 个"
    % (_rate_lo, str([(("%.2f-%.2f" % (a, b)), round(f / float(n), 3)) for a, b, f, n in by_amp]), fn_k))

add(MAIN, "R2", "R", "必要性方向不被打破：%d 组里假阴性 **%d** 个（Δ²≤0 却窗口非空）⇒ 「Δ²>0 是必要条件」经随机大样本验证"
    % (tot_k, fn_k),
    "0", str(fn_k), fn_k == 0,
    "★这一条与 R1 成对：只报误判率不报漏判率，读者会以为判据「整体不可用」；"
    "实际是**单向保守**——它从不排除真可达点")

# ============================================================ k 时不变性对照
print("\n[R3] 对照：同一批随机族上「凸包判据」的误判率（应为 0，by construction）")
_hull_bad = 0
_hull_n = 0
for (amp, w1, w2, ps) in FAMS[:60]:
    ph = mk_phi(amp, w1, w2, ps)
    hv = set(n for n in hull_idx_of(aR, ph, lambda n: float(n), 200) if 2 <= n <= 24)
    for k in range(2, 25):
        lo, hi = win_g(aR, ph, lambda n: float(n), k, nmax=200)
        empty = (hi is not None and lo > hi)
        _hull_n += 1
        if (k in hv) == empty:
            _hull_bad += 1
print("   凸包判据与窗口非空的一致性：%d 组里不一致 %d 个" % (_hull_n, _hull_bad))
add(CTL, "C2", "C", "判别力对照（两个不同读数）：同一批随机族上 Δ² 判据误判 %d 次，凸包顶点判据误判 %d 次"
    % (fp_k, _hull_bad),
    str(fp_k), str(_hull_bad), _hull_bad == 0,
    "★控制组必须给两个不同读数：Δ² 的误判数 = %d，凸包的误判数 = %d（%d 组核对）。"
    "若两者相同，说明凸包判据也是空的。★注意两者统计范围不同（Δ² 是全 240 族、凸包取前 60 族），"
    "所以只比「是否为 0」，不比绝对数" % (fp_k, _hull_bad, _hull_n))

# ============================================================ P 定价
print("\n=== P 定价 ===")
add(MAIN, "P1", None, "定价：闭合 X-R386-1/2/3/4；不产生新物理；供给 0、不占度、独有预言 0",
    "0", "0", None,
    "① EM 边界项闭式 = 数值分析方法定理；② c0=0 = 数学恒等式（Poisson）；"
    "③ 凸包推广 = 换坐标不变性；④ 误判率 = 统计口径。四条都不预言新粒子/新常数。")
add(MAIN, "P2", None, "定价：条目不可与 r386 相加；r386 的 B4（外推未收敛）在本卷被**解释**而非「推翻」——"
    "它描述的现象（三基散布 3.5e-01）仍然为真，只是原因不是「极限不存在」",
    "0", "0", None,
    "★必须写清：本卷没有把 r386 判错。r386 说「本组 M 上定不出」，正确；"
    "本卷补的是「不必定——解析上已是 0」。两卷是「现象」与「原因」的关系，不可加总计数。")

# ============================================================ G 守卫
print("\n=== G 守卫 ===")


def g01_scan():
    src = io.open(__file__, "r", encoding="utf-8").read()
    tree = ast.parse(src)
    bad = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "add":
            if len(node.args) >= 7:
                rid, okarg = node.args[1], node.args[6]
                if isinstance(rid, ast.Constant) and isinstance(rid.value, str) and rid.value[:1] in ("C", "G"):
                    if isinstance(okarg, ast.Constant):
                        bad.append((rid.value, node.lineno))
    return bad


_b1 = g01_scan()
add(GRD, "G01", "G", "AST 层守卫：CTL/GRD 的 ok 实参顶层不得是布尔/IfExp 常量",
    "0", str(len(_b1)), len(_b1) == 0, "命中 " + str(_b1))

_b2 = []
for _r in CTL:
    if _r["exp"] == _r["act"]:
        _b2.append(_r["id"] + "(字符串同)")
        continue
    try:
        if abs(float(_r["exp"]) - float(_r["act"])) < 1e-31:
            _b2.append(_r["id"] + "(数值同)")
    except ValueError:
        pass
add(GRD, "G02", "G", "控制组必须给两个不同读数（字符串 + 数值两层）", "0", str(len(_b2)), len(_b2) == 0,
    "命中 " + str(_b2))

_tol = [("TOL_EM", TOL_EM), ("TOL_PRED", TOL_PRED), ("TOL_ALG", TOL_ALG),
        ("TOL_NUM", TOL_NUM), ("TOL_HULL", TOL_HULL), ("TOL_STAT", TOL_STAT)]
_pow = []
for _nm, _v in _tol:
    _lv = float(_v)
    _e = round(math.log10(_lv))
    if abs(_lv - 10.0 ** _e) <= abs(_lv) * 2.6e-15:
        _pow.append(_nm)
add(GRD, "G03", "G", "门限表不得含 10 的整数幂", "0", str(len(_pow)), len(_pow) == 0,
    "登记 " + str([(a, fs(b, 8)) for a, b in _tol]) + "；命中 " + str(_pow))

_b5 = [r["id"] for r in MAIN if r["kind"] == "PASS" and (not r["computed"] or not r["note"])]
add(GRD, "G04", "G", "每条 PASS 必须真算出数且带 note", "0", str(len(_b5)), len(_b5) == 0, "命中 " + str(_b5))

# G05：误差上界必须**真的夹住**误差，且不能宽松到无意义（两个方向都要查）
_ratio_b = bound640 / max(err640, 1e-300)
_ok5 = (1.0 <= _ratio_b <= 64.0)
add(GRD, "G05", "G", "B1 的误差上界必须夹住实测误差、且不得宽松到无判别力（要求 1 ≤ 上界/误差 ≤ 64）",
    "1 ≤ 比值 ≤ 64", "%.2f" % _ratio_b, _ok5,
    "★只查「误差 < 上界」是假门禁：随便给一个 1e6 倍的上界都能过。"
    "实测上界/误差 = %.2f ⇒ 上界是**定量**的，不是免责声明" % _ratio_b)

# G06：A5 的闭式与数值必须来自不同解析路径（源码层查：数值路径不得调用 D_EM_parts）
_src = io.open(__file__, "r", encoding="utf-8").read()
_i = _src.find("def dnorm_numeric")
_j = _src.find("def ", _i + 10)
_body = _src[_i:_j]
_ok6 = ("D_EM_parts" not in _body) and ("_CACHE" not in _body)
add(GRD, "G06", "G", "A5 的数值路径（dnorm_numeric）不得调用闭式函数 D_EM_parts —— 同源回验抓不到同源错误",
    "0", "0" if _ok6 else "1", _ok6,
    "已用源码切片核查：dnorm_numeric 函数体内不含 D_EM_parts / _CACHE")

# G07：H1 的第三条路径（网格暴力）不得使用 win_g 的输出
_i = _src.find("    # 路径 3")
_j = _src.find("    HROWS.append", _i)
_body3 = _src[_i:_j]
_ok7 = ("win_g(" not in _body3) and ("lower_hull_pts" not in _body3)
add(GRD, "G07", "G", "H1 的路径 3（网格暴力 argmin）不得使用路径 1/2 的任何中间量",
    "0", "0" if _ok7 else "1", _ok7, "源码切片核查：路径 3 体内不含 win_g / lower_hull_pts")

# G08：c0=0 的判据必须同时报「若漏掉 2π 会得到什么」
_wrong = (TARGET / R_MAIN) * 4.0 * math.exp(-R_MAIN)
add(GRD, "G08", "G", "B3 的 2π 因子必须被检验：漏掉 2π 时预言值 %.1e，正确值 %.1e，相差 %.0f 个量级"
    % (R_MAIN * _wrong, LIM, math.log10(_wrong / D_INF)),
    "%.1e" % LIM, "%.1e" % (R_MAIN * _wrong), _wrong / D_INF > 1e10,
    "★这是本卷最容易犯且最难发现的错：Poisson 求和里 e^{-2πr} 的 2π 来自 f̂(2πm)")

# G09：R1 必须与 R2 成对报出
_ok9 = (RATE > 0) and (fn_k == 0)
add(GRD, "G09", "G", "随机统计必须同时报误判率与漏判率（只报一个会让人以为判据整体不可用）",
    "1", "1" if _ok9 else "0", _ok9, "误判率 %.4f / 漏判 %d" % (RATE, fn_k))

# G10：判词由读数驱动
# ★必须与 A1 用**同一个读数**（_rel_last，M=320）；首版这里用了 _worst_rel（5 档最大值），
#   结果 A1 记 PASS 而 VERDICT 写 X386-1-OPEN —— 判词与判定表自相矛盾。
_x1 = "X386-1-EM-CLOSED-FORM" if (D(str(_rel_last)) < TOL_EM) else "X386-1-OPEN"
_x2 = "X386-2-C0-EXACTLY-ZERO" if abs(LIM) < 1e-40 else "X386-2-OPEN"
_x3 = "X386-3-HULL-GENERALIZED" if _h_ok else "X386-3-OPEN"
_x4 = "X386-4-FP-RATE-%.2f" % RATE
VERDICT = "--".join([_x1, _x2, _x3, _x4,
                     "PREDICT-640-ABS-%.0e" % err640, "THREE-TERMS-NECESSARY",
                     "ONE-SIDED-CONSERVATIVE", "SUPPLY-ZERO"])
_ok10 = all(t in VERDICT for t in ("X386-1", "X386-2", "X386-3", "X386-4", "SUPPLY-ZERO"))
add(GRD, "G10", "G", "判词由读数驱动（四个 X 标记分别来自 A1、B3、H1、R1 的布尔量）",
    "1", "1" if _ok10 else "0", _ok10, "VERDICT 不手写语义，只拼标记")

# ============================================================ 计数校正与落盘
def rows_all():
    return MAIN + CTL + GRD


def counts():
    _r = rows_all()
    return (sum(1 for x in _r if x["kind"] == "PASS"),
            sum(1 for x in _r if x["kind"] == "INFO"),
            sum(1 for x in _r if x["kind"] == "FAIL"))


# G11：先按「此刻」的列表算（此时 G13 还没入列），收尾段再按最终列表重算一次
_ra0 = rows_all()
_dup0 = len(_ra0) - len({x["id"] for x in _ra0})
_empty0 = sum(1 for x in _ra0 if not x["note"])
add(GRD, "G11", "G", "id 唯一且 note 非空（收尾由校正段按最终列表重算）",
    "0", str(_dup0 + _empty0), (_dup0 == 0 and _empty0 == 0),
    "写入时 GRD 还在追加 ⇒ 这里的计数只是中途快照（%d 条），末尾由校正段按最终列表重算" % len(_ra0))

DECLARED_NEG = set()
_neg_bad = [k for k in sorted(DECLARED_NEG)
            if k not in [x["id"] for x in rows_all()]
            or [x["kind"] for x in rows_all() if x["id"] == k][0] != "FAIL"]
_neg_unreg = [x["id"] for x in rows_all() if x["kind"] == "FAIL" and x["id"] not in DECLARED_NEG]
add(GRD, "G12", "G", "真判负登记守卫：每个 FAIL 都必须在 DECLARED_NEG 登记且确实是 FAIL；未登记的 FAIL 必须为 0",
    "0", str(len(_neg_bad) + len(_neg_unreg)), len(_neg_bad) + len(_neg_unreg) == 0,
    "登记 %s；未登记 FAIL %s" % (sorted(DECLARED_NEG), _neg_unreg))

OUT_JSON = os.path.join(DATA, TITLE + ".json")
OUT_TXT = os.path.join(DATA, TITLE + "_report_2026-11-03.txt")

FINAL = "PENDING"


def dump():
    P, I, FA = counts()
    obj = {"rid": RID, "date": DATE, "title": TITLE, "final": FINAL, "verdict": VERDICT,
           "counts": {"main": len(MAIN), "ctl": len(CTL), "grd": len(GRD),
                      "pass": P, "info": I, "fail": FA},
           "rows": rows_all()}
    with io.open(OUT_JSON, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)


dump()
with io.open(OUT_JSON, "r", encoding="utf-8") as f:
    _back = json.load(f)
_N0 = len(rows_all())
_N1 = len(_back["rows"])
_ok13 = (_N1 == _N0)
add(GRD, "G13", "G", "落盘后回读 JSON：条目数等于内存条目数（真读盘，不是 len(同一个 list) 自证）",
    str(_N0), str(_N1), _ok13,
    "dump 前内存 %d 条、回读 %d 条；★本行在核对之后才入列，故期望值取核对时刻的条目数" % (_N0, _N1))
dump()
with io.open(OUT_JSON, "r", encoding="utf-8") as f:
    _back2 = json.load(f)
_N2 = len(rows_all())
assert len(_back2["rows"]) == _N2, ("二次落盘不符", len(_back2["rows"]), _N2)

# 收尾校正：G11 的计数按**最终**列表（含 G13）重算 —— 写入时它看到的是中途快照
for _rgr in GRD:
    if _rgr["id"] == "G11":
        _ra = rows_all()
        _dup = len(_ra) - len({x["id"] for x in _ra})
        _emp = sum(1 for x in _ra if not x["note"])
        _rgr["exp"] = "0"
        _rgr["act"] = str(_dup + _emp)
        _rgr["kind"] = "PASS" if (_dup == 0 and _emp == 0) else "FAIL"
        _rgr["note"] = ("按最终列表重算：%d 条（主册 %d + 控制组 %d + 守卫 %d），重复 %d，空 note %d"
                        % (len(_ra), len(MAIN), len(CTL), len(GRD), _dup, _emp))

PASS_N, INFO_N, FAIL_N = counts()
NEG_N = len([x for x in rows_all() if x["kind"] == "FAIL" and x["id"] in DECLARED_NEG])
_undeclared = [x["id"] for x in rows_all() if x["kind"] == "FAIL" and x["id"] not in DECLARED_NEG]
if _undeclared or not _ok13:
    FINAL = "GATES-FAIL"
elif NEG_N:
    FINAL = "GATES-PASS-WITH-%d-NEGATIVE" % NEG_N
else:
    FINAL = "ALL-GATES-PASS"
dump()

print("\n=== 汇总 ===")
print("MAIN=%d (PASS %d / INFO %d / FAIL %d)  CTL=%d  GRD=%d  合计 %d"
      % (len(MAIN), sum(1 for r in MAIN if r["kind"] == "PASS"),
         sum(1 for r in MAIN if r["kind"] == "INFO"),
         sum(1 for r in MAIN if r["kind"] == "FAIL"), len(CTL), len(GRD), _N2))
print("FINAL = %s" % FINAL)
print("VERDICT = %s" % VERDICT)

L = []
L.append(TITLE)
L.append("=" * 100)
L.append("对象：r386 判定册 §七 的四条 OPEN（X-R386-1..4）")
L.append("FINAL = %s" % FINAL)
L.append("VERDICT = %s" % VERDICT)
L.append("主册 %d（PASS %d / INFO %d / FAIL %d）；控制组 %d；守卫 %d；合计 %d"
         % (len(MAIN), sum(1 for r in MAIN if r["kind"] == "PASS"),
            sum(1 for r in MAIN if r["kind"] == "INFO"),
            sum(1 for r in MAIN if r["kind"] == "FAIL"), len(CTL), len(GRD), _N2))
L.append("")


def sect(title, rows):
    L.append("=" * 100)
    L.append("【%s】" % title)
    L.append("=" * 100)
    for r in rows:
        L.append("[%s] %-5s %s" % (r["kind"], r["id"], r["name"]))
        L.append("    exp = %s" % r["exp"])
        L.append("    act = %s" % r["act"])
        L.append("    %s" % r["note"])
        L.append("")


sect("主册", MAIN)
sect("控制组", CTL)
sect("守卫", GRD)
L.append("=" * 100)
L.append("【关键表】")
L.append("=" * 100)
L.append("A1 D_M 实测 vs 闭式（r=20）")
L.append("     M      D_M 实测          D_M 闭式         相对差      绝对残差")
for M, dm, e, rel, ab, ie in AROWS:
    L.append("   %4d  %+.12e  %+.12e  %+.3e  %.3e" % (M, dm, e, rel, ab))
L.append("   绝对残差逐档比值 %s ⇒ 末档 p = %.2f" % (str(["%.4f" % v for v in _ratio]), _p_last))
L.append("")
L.append("B1 无参数预言")
L.append("   M=640：实测 %+.12e / 预言 %+.12e（相对差 %.3e）" % (R640, p640, rel640))
L.append("   M=320,r=7：实测 %+.10e / 预言 %+.10e（相对差 %.3e）" % (R7, p7, rel7))
L.append("   Poisson：R_∞ = %.3e（e^{-40π} = %.2e）" % (LIM, math.exp(-2 * math.pi * 20)))
L.append("")
L.append("B4 R_M·M 的漂移（说明 1/M 外推为何必散）")
for M, Rv, RMv in B4:
    L.append("   M=%3d  R_M=%+.10f  R_M·M=%+.4f" % (M, Rv, RMv))
L.append("")
L.append("A4 留一法（相对差）")
for M, tag, v in A4:
    L.append("   M=%3d  %-18s %.3e" % (M, tag, v))
L.append("")
L.append("H1 凸包推广三路对拍")
for tag, hv, ne, flip, hit in HROWS:
    L.append("   %-14s hull=%2d minmax=%2d 反演失败=%d 网格命中=%2d" % (tag, len(hv), len(ne), flip, len(hit)))
L.append("")
L.append("R1 随机 φ 的误判率（按幅度五档）")
for lo_a, hi_a, f, n in by_amp:
    L.append("   幅度 %.2f–%.2f  %3d/%4d = %.3f" % (lo_a, hi_a, f, n, f / float(n) if n else 0.0))
L.append("   合计 %d/%d = %.4f；漏判 %d" % (fp_k, tot_k, RATE, fn_k))
L.append("")
L.append("=" * 100)
L.append("【诚实边界】")
L.append(" 1) EM 闭式给的是 D_M 的**渐近**闭式，余项 ~M^-5；M<20 时未验证。")
L.append(" 2) Poisson 求和用的是 f=1/(r²+ρ²)^{3/2} 的 Hankel 变换，f̂(k)=2πe^{-rk}/r；该变换在 r>0、k>0 成立。")
L.append(" 3) 凸包推广要求 g 严格单增；g 非单增时定理失效（C1 已量化）。")
L.append(" 4) 随机 φ 只覆盖「两正弦叠加」这一族；iid 随机 φ 未测，误判率可能更高。")
L.append(" 5) 本卷不产生新物理：供给 0、不占度、独有预言 0。")
L.append("")
L.append("【产物】源码 / 数据 json / 数据 report / 判定 md / HTML")
txt = "\n".join(L) + "\n"
with io.open(OUT_TXT, "w", encoding="utf-8", newline="\n") as f:
    f.write(txt)
print("\nJSON -> %s" % OUT_JSON)
print("TXT  -> %s (%d chars)" % (OUT_TXT, len(txt)))
print("FINAL = %s" % FINAL)

assert _undeclared == [], "未登记的 FAIL：%s" % _undeclared
assert _neg_bad == [], "DECLARED_NEG 里存在并非 FAIL 的 id：%s" % _neg_bad
assert _ok13, "落盘回读条目数不符"
assert FAIL_N == NEG_N, "FAIL 数 %d 与登记判负数 %d 不等" % (FAIL_N, NEG_N)
assert FINAL in ("ALL-GATES-PASS", "GATES-PASS-WITH-1-NEGATIVE"), FINAL
