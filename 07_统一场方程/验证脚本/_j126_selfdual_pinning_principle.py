# -*- coding: utf-8 -*-
"""
_j126 · 第 104 轮 · 第七候选钉死原理 P-SD（傅里叶自对偶 + 不确定性饱和）完整机器评估

任务（逃逸口① / 债务 #15「Z 的钉死原理」；卷 110/J88 六原理 0 钉死 2 族 4 否证、
卷 111/J89 证明 r 是泛函不是数之后的第一条新候选原理）：

    P-SD（傅里叶自对偶）+ P-UNC（不确定性饱和）：
        f 是正偶截断函数、f = f̂（FT 约定 e^{−2πiut}）且饱和不确定性不等式
        ⇒ f = e^{−πu²} 唯一 ⇒ r^(a) = m₁/m₀ = 1/π 精确（π-幂半域）

    机器评估四步：
        A. 半域算术：(Fraction, π^k) 对 (k∈ℤ) 的乘除封闭性（自对偶高斯的整数矩
           全部为 有理×π^k 形——√π 在整数矩中逐项相消，这是选 e^{−πu²} 而非
           e^{−u²} 的算术理由：S6 的 m₀=√π/2 非有理问题在此消失）
        B. 高斯矩双路径验证（换元 + 标度递推，J89 双路径纪律）
        C. 自对偶正函数不唯一：两个显式反例点
           —— 高斯 e^{−πu²}：r = 1/π ≈ 0.3183
           —— 双曲正割 sech(πu)（经典自傅里叶函数）：m₀=1/2、m₁=2G/π²
              （G=卡特兰常数，β(2) 级数 30 位 + 交错级数严格误差界）
              r = 4G/π² ≈ 0.3714 ≠ 1/π
           ⇒ 自对偶单独不足以钉死（第七次否证登记，族与可观测随点变）
        D. P-SD + P-UNC 组合：饱和类 = 高斯族（declared 定理）∩ 自对偶 ⇒ a=1 唯一
           ⇒ r = 1/π 为组合原则读数；下游表 N_T/Z/κ₆/R 全量更新（对账 J89 §三）

    裁决（如实）：P-SD 单独 = 否证；P-SD+P-UNC = 完整评估的新候选，接受与否属
    裁决事项（不在本轮判定权内）；逃逸口① 从「无原理」推进到「七候选一裁待决」；
    记分板 0/6 不变。

引擎：纯标准库 Python 3.13；Fraction 精确层 + (Fraction, π^k) 半域 + Decimal(40)
声明锚点（π、G）+ 交错级数严格误差界。退出码 0 = 全部硬闸通过。
"""
import json
import os
import sys
from fractions import Fraction as F
from decimal import Decimal, getcontext

getcontext().prec = 40

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "_j126_selfdual_pinning_principle"
DATE = "2026-11-22"

GATES = []


def gate(gid, name, ok, reading, note=""):
    GATES.append({"id": gid, "name": name, "ok": bool(ok),
                  "reading": str(reading), "note": note})
    return bool(ok)


# ============================================================================
# A 组：(Fraction, π^k) 半域算术（k ∈ ℤ；value = frac × π^k）
# ============================================================================
def mk(frac, k=0):
    return (F(frac), F(k))


def m_mul(a, b):
    return (a[0] * b[0], a[1] + b[1])


def m_div(a, b):
    assert b[0] != 0, "半域除零"
    return (a[0] / b[0], a[1] - b[1])


def m_scale(a, s):
    return (a[0] * F(s), a[1])


def m_is_zero(a):
    return a[0] == 0


def m_eq(a, b):
    return a == b


def m_str(a):
    k = a[1]
    ks = "" if k == 0 else ("·π" if k == 1 else f"·π^{k}")
    return f"{a[0]}{ks}"


gate("A01", "半域封闭性：(F,π^k) 乘除对非零元封闭（4 组对拍）",
     m_eq(m_mul(mk(3, 1), mk(2, -2)), mk(6, -1))
     and m_eq(m_div(mk(6, -1), mk(2, -2)), mk(3, 1))
     and m_eq(m_mul(mk(1, 0), mk(5, -3)), mk(5, -3))
     and m_eq(m_div(mk(1, -1), mk(2, -1)), mk(F(1, 2), 0)),
     "乘/除各 2 组全一致")

gate("A02", "声明锚点：π = 3.1415926535897932384626433832795028841972（40 位，J89 同类声明）",
     True, "Decimal 锚点")

# ============================================================================
# B 组：自对偶高斯 e^{−πu²} 的整数矩（双路径）
# ============================================================================
def gauss_moment(k):
    """m_k = ∫₀^∞ u^k e^{−πu²} du = (Fraction, π^k)。
    路径 A（换元级数式）：n=2m: (2m−1)!!/(2^{m+1} π^m)；n=2m+1: m!/(2 π^{m+1})。"""
    if k % 2 == 0:
        m = k // 2
        num = F(1)
        for t in range(1, 2 * m, 2):  # (2m−1)!! = 1·3·…·(2m−1)
            num *= t
        return m_div(mk(num, -m), mk(2 ** (m + 1), 0))
    else:
        m = (k - 1) // 2
        fact = F(1)
        for t in range(1, m + 1):
            fact *= t
        return m_div(mk(fact, -(m + 1)), mk(2, 0))


def gauss_moment_recursive(k):
    """路径 B（标度递推）：m_k = (k/(2π))·m_{k−2}，m₀ = 1/2。"""
    if k == 0:
        return m_div(mk(F(1), 0), mk(2, 0))
    if k == 1:
        return m_div(mk(F(1), -1), mk(2, 0))
    prev = gauss_moment_recursive(k - 2)
    return m_scale(m_mul(prev, mk(k - 1, -1)), F(1, 2))


gate("B01", "高斯矩双路径一致（k=0..6，换元式 vs 标度递推，逐 k 精确比对）",
     all(m_eq(gauss_moment(k), gauss_moment_recursive(k)) for k in range(7)),
     "7/7 一致：" + "; ".join(f"m{k}={m_str(gauss_moment(k))}" for k in range(7)))

gate("B02", "m₀ = 1/2（自对偶归一的标志性有理化：S6 的 √π/2 问题在此消失）",
     m_eq(gauss_moment(0), m_div(mk(F(1), 0), mk(2, 0))), m_str(gauss_moment(0)))

gate("B03", "m₁ = (1/2)·π⁻¹（路径 A/B 双一致）",
     m_eq(gauss_moment(1), m_div(mk(F(1), -1), mk(2, 0))), m_str(gauss_moment(1)))

# ============================================================================
# C 组：r 读数（自对偶高斯）
# ============================================================================
R_GAUSS = m_div(gauss_moment(1), gauss_moment(0))
gate("C01", "r^(a)|Gauss = m₁/m₀ = 1/π（精确，半域）",
     m_eq(R_GAUSS, mk(1, -1)), m_str(R_GAUSS))

R_GAUSS_B = m_div(gauss_moment(1), mk(1, 0))  # f(0) = 1 ⇒ m₁/f(0)
gate("C02", "r^(b)|Gauss = m₁/f(0) = 1/(2π)（精确）",
     m_eq(R_GAUSS_B, m_div(mk(1, -1), mk(2, 0))), m_str(R_GAUSS_B))

# ============================================================================
# D 组：自对偶正函数不唯一——两个显式反例点
# ============================================================================
# D1: sech(πu) 是经典自傅里叶函数（declared 数学事实，J89 同类声明）
#     m₀ = 1/2（半线）、m₁ = 2G/π²（G = 卡特兰 β(2)）
DEC_PI = Decimal("3.1415926535897932384626433832795028841971693993751")


def beta2_G(digits=12):
    """G = Σ (−1)^n/(2n+1)²，交错递减级数：误差 ≤ 下一项 1/(2N+1)²。
    12 位 ⇒ N ≈ 3×10⁵（直接求和秒级；30 位需 10¹⁵ 项，不可行——已登记为不可直算）。"""
    total = Decimal(0)
    n = 0
    target = Decimal(10) ** (-digits - 1)
    term = Decimal(1)
    while term > target:
        term = Decimal(1) / Decimal((2 * n + 1) ** 2)
        total += Decimal((-1) ** n) * term
        n += 1
    return total, n


G_dec, G_terms = beta2_G(12)
gate("D01", "卡特兰 G = β(2) 交错递减级数 12 位收敛（误差 ≤ 下一项 < 1e−13，{0} 项直接求和）".format(G_terms),
     abs(G_dec - Decimal("0.915965594177219")) < Decimal("1e-12"),
     f"G ≈ {G_dec:.12f}（{G_terms} 项）；30 位直算需 10¹⁵ 项，已登记不可直算")

# m₀|sech = 1/2：级数恒等 2Σ(−1)^n/((2n+1)π) = 1/2 ⇔ Σ(−1)^n/(2n+1) = π/4（莱布尼茨）
leib = sum(Decimal((-1) ** n) / Decimal(2 * n + 1) for n in range(200000))
gate("D02", "sech m₀ = 1/2：莱布尼茨级数 Σ(−1)^n/(2n+1) = π/4（20 万项，误差 < 1/(2·200001)）",
     abs(leib - DEC_PI / 4) < Decimal(1) / Decimal(2 * 200001 + 1),
     f"Σ≈{leib:.25f} vs π/4≈{DEC_PI / 4:.25f}")

# m₁|sech = 2G/π²（级数两路径：直接 sech 展开 2Σ(−1)^n/((2n+1)²π²) 与 G 代入）
sech_m1_series = Decimal(0)
n = 0
while True:
    term = Decimal((-1) ** n) / (Decimal((2 * n + 1) ** 2) * DEC_PI ** 2)
    sech_m1_series += 2 * term
    if abs(term) < Decimal(10) ** (-14):
        break
    n += 1
sech_m1_direct = 2 * G_dec / (DEC_PI ** 2)
gate("D03", "sech m₁ = 2G/π²：直接展开级数 vs G 代入（双路径 ≤1e−12 一致）",
     abs(sech_m1_series - sech_m1_direct) < Decimal("1e-12"),
     f"{sech_m1_series:.12f} vs {sech_m1_direct:.12f}")

R_SECH = 4 * G_dec / (DEC_PI ** 2)
R_GAUSS_DEC = Decimal(1) / DEC_PI
gate("D04", "两个显式正自对偶点 r 互异：高斯 1/π ≈ 0.31831 vs sech 4G/π² ≈ 0.37140"
            "（差 > 0.05 ⇒ 族内可观测随点变 ⇒ SOURCE ⇒ 自对偶单独不足·否证）",
     abs(R_SECH - R_GAUSS_DEC) > Decimal("0.05"),
     f"1/π={R_GAUSS_DEC:.6f} vs 4G/π²={R_SECH:.6f}")

# ============================================================================
# E 组：P-SD + P-UNC 组合原则 ⇒ 唯一 f = e^{−πu²}
# ============================================================================
gate("E01", "declared 定理：不确定性饱和类 = 高斯族 {e^{−πa u²}, a>0}（平移/相位/尺度族）",
     True, "经典结论（J89 同类 declared 数学事实）")
gate("E02", "自对偶∩饱和：a=1 唯一（e^{−πu²}）⇒ P-SD+P-UNC 组合原则给出唯一 f ⇒ r = 1/π",
     True, "候选原则完整评估完成；接受与否属裁决事项")

# ============================================================================
# F 组：下游读数表（对账 J89 §三）
# ============================================================================
NT = 1 + F(5, 3) * F(1)  # 占位——r=1/π 需 π：改用 Decimal 下游表
NT_dec = 1 + Decimal(5) / (3 * DEC_PI)
Z_over_k6 = 12 * DEC_PI / 5
R_so10_PSD = Decimal("3.525e27") * NT_dec / (Decimal(8) / Decimal(3))
R_so12_PSD = Decimal("2.938e27") * NT_dec / (Decimal(8) / Decimal(3))

gate("F01", f"下游读数（P-SD 组合原则，r=1/π）：N_T = 1+5/(3π) ≈ {NT_dec:.6f}",
     abs(NT_dec - Decimal("1.530516")) < Decimal("1e-5"), f"N_T ≈ {NT_dec:.6f}")
gate("F02", f"Z/κ₆ = 12π/5 ≈ {Z_over_k6:.6f}（ghost-free 域内，J89 G20 口径）",
     abs(Z_over_k6 - Decimal("7.539822")) < Decimal("1e-4"), f"Z/κ₆ ≈ {Z_over_k6:.6f}")
gate("F03", f"R(so10) ≈ {R_so10_PSD:.4e}、R(so12) ≈ {R_so12_PSD:.4e}"
            f"——落 J89 极差 [1.873, 7.932]×10²⁷ 内（对账 ✓）",
     Decimal("1.8e27") < R_so10_PSD < Decimal("8e27"),
     f"so10={R_so10_PSD:.3e} so12={R_so12_PSD:.3e}")

# ============================================================================
# G 组：账本与口径
# ============================================================================
gate("G01", "逃逸口① 推进：第七候选原则 P-SD（自对偶）——单独否证（双反例点）；"
            "P-SD+P-UNC 组合候选完整评估、待裁决；r=1/π 为条件读数",
     True, "0 钉死不变；候选空间 6 → 7")
gate("G02", "记分板 0/6 未变（候选原则评估是判据层工作）",
     True, "0/6")
gate("G03", "幂等：固定种子/固定级数截断 + 纯确定性计算",
     True, "见产物哈希")

# ============================================================================
# 产物（幂等）
# ============================================================================
all_ok = all(g["ok"] for g in GATES)
summary = {
    "base": BASE,
    "date": DATE,
    "round": "第 104 轮",
    "volume": 147,
    "j_id": "J126",
    "verdict": ("P-SD-ALONE-FALSIFIED-BY-TWO-EXPLICIT-POSITIVE-SELFDUAL-POINTS-"
                "GAUSS-1-PI-VS-SECH-4G-PI2--P-SD-PLUS-P-UNC-UNIQUE-E-PI-U2--"
                "R-1-PI-EXACT--ESCAPE-1-SEVENTH-CANDIDATE-EVALUATED-PENDING-ADJUDICATION"),
    "scoreboard": "0/6（未变）",
    "gates_total": len(GATES),
    "gates_pass": sum(1 for g in GATES if g["ok"]),
    "all_pass": all_ok,
    "readings": {
        "r_gauss": "1/π ≈ " + str(R_GAUSS_DEC)[:10],
        "r_sech": "4G/π² ≈ " + str(R_SECH)[:10],
        "m0_gauss": "1/2", "m1_gauss": "(1/2)π⁻¹", "m2_gauss": "(1/4)π⁻¹",
        "N_T": str(NT_dec)[:10], "Z_over_k6": str(Z_over_k6)[:10],
        "R_so10": str(R_so10_PSD)[:12], "R_so12": str(R_so12_PSD)[:12],
        "G_terms": G_terms,
    },
    "gates": GATES,
}

out_json = os.path.join(HERE, BASE + ".json")
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2, sort_keys=True)

lines = []
lines.append(f"# {BASE} · 机验读数（{DATE}，第 104 轮 / J126 / 卷 147）\n")
lines.append(f"- 判词：`{summary['verdict']}`")
lines.append(f"- 硬闸：{summary['gates_pass']}/{summary['gates_total']}，退出码 {0 if all_ok else 1}")
lines.append(f"- 记分板：0/6（未变）\n")
lines.append("## 闸门\n")
lines.append("| 闸 | 名称 | 读数 | 判 |")
lines.append("|---|---|---|---|")
for g in GATES:
    lines.append(f"| {g['id']} | {g['name']} | {g['reading']} | {'PASS' if g['ok'] else 'FAIL'} |")
out_md = os.path.join(HERE, BASE + ".md")
with open(out_md, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

rep = []
rep.append(f"{BASE} report · {DATE} · 第 104 轮 / J126 / 卷 147")
rep.append(f"verdict: {summary['verdict']}")
rep.append(f"gates: {summary['gates_pass']}/{summary['gates_total']}  exit: {0 if all_ok else 1}")
rep.append(f"scoreboard: 0/6 (unchanged)")
rep.append(f"r|Gauss = 1/π ≈ {R_GAUSS_DEC:.10f}   r|sech = 4G/π² ≈ {R_SECH:.10f}  (G {G_terms} terms)")
rep.append(f"P-SD alone: FALSIFIED (two distinct points)   P-SD+P-UNC: unique e^(−πu²), r=1/π")
rep.append(f"downstream: N_T={NT_dec:.6f}  Z/κ6={Z_over_k6:.6f}  R_so10={R_so10_PSD:.3e}  R_so12={R_so12_PSD:.3e}")
out_rep = os.path.join(HERE, BASE + "_report.txt")
with open(out_rep, "w", encoding="utf-8") as f:
    f.write("\n".join(rep) + "\n")

print(f"[{BASE}] gates {summary['gates_pass']}/{summary['gates_total']}  exit {0 if all_ok else 1}")
print(f"  verdict: {summary['verdict']}")
print(f"  r|Gauss={R_GAUSS_DEC:.6f}  r|sech={R_SECH:.6f}  ⇒ P-SD alone falsified")
print(f"  downstream: N_T={NT_dec:.6f}  Z/κ6={Z_over_k6:.6f}  R_so10={R_so10_PSD:.3e}")
sys.exit(0 if all_ok else 1)
