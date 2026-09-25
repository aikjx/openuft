# -*- coding: utf-8 -*-
"""
分支 D 配套 · 矛盾修补方案可行性验算

对 `01A_附录_体系不自洽点专项复盘.md` 中提出的每一条修补候选做**数值验算**，
回答同一个问题：这条修补在量纲上能不能成立？成立之后数值还对不对？要付出多少新假设？

红线：只算，不改 verdict，不美化。修补失败就写失败。

依赖：仅标准库。
运行：python patch_feasibility.py
"""

import math
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

C = 299792458.0
HBAR = 1.054571817e-34
QE = 1.602176634e-19
EPS0 = 8.8541878128e-12
MU0 = 1.25663706212e-6
G = 6.67430e-11
ALPHA = 7.2973525693e-3
ME = 9.1093837015e-31
MP = 1.67262192369e-27
LPL = 1.616255e-35

RESULTS = []


def rec(sid, title, verdict, detail):
    RESULTS.append({"id": sid, "sec": "修补验算", "title": title,
                    "verdict": verdict, "detail": detail})


def P(sid, t, d):
    rec(sid, t, "PASS", d)


def F(sid, t, d):
    rec(sid, t, "FAIL", d)


def BO(sid, t, d):
    rec(sid, t, "BOUNDARY", d)


def IN(sid, t, d):
    rec(sid, t, "INFO", d)


def g(x, n=6):
    return "%.*g" % (n, x)


def run():
    RESULTS[:] = []

    coef = ALPHA * ALPHA * MU0 * C * C          # α²μ₀c²  [= M L³ T⁻⁴ I⁻²]
    rho_g = math.sqrt(G / coef)                 # 由 G 反解的 ρ
    rho_ce = HBAR / (ME * C)                    # 电子 ρ_C
    rho_cp = HBAR / (MP * C)                    # 质子 ρ_C

    # ---------------- D1-a：把 ρ 换成荷质比 e/m（量纲修补）
    em = QE / ME
    g_a = coef * em * em
    F("D1-a", "修补候选 a：把 ρ 重新解释为荷质比 e/m（使量纲自洽）",
      "[e/m]=C/kg=M⁻¹TI，代入后 [α²μ₀c²(e/m)²]=M⁻¹L³T⁻²=[G] ✓ 量纲成立。" +
      "但数值：α²μ₀c²=" + g(coef) + "，e/m_e=" + g(em) + " C/kg，" +
      "G_pred=" + g(g_a) + " vs G=" + g(G) + "，偏离 " + g(g_a / G) + " 倍。" +
      "⇒ 量纲修补成功、数值彻底崩塌（且『螺旋半径=荷质比』与体系一几何本体论直接冲突）。")

    # ---------------- D1-b：保留 ρ 为长度，引入带量纲常数 K
    g_b = coef * rho_g * rho_g
    k_needed = G / (coef * rho_ce * rho_ce)
    F("D1-b", "修补候选 b：保留 ρ 为长度，引入带量纲常数 K",
      "若 ρ 取独立来源 ρ_C(e⁻)=" + g(rho_ce) + " m，则 G_pred=" + g(coef * rho_ce * rho_ce) +
      "，需补常数 K=G/G_pred=" + g(k_needed) + "，量纲 [K]=M⁻²L⁻²T²I²。" +
      "⇒ 修补代价 = 引入 1 个**新自由参数**（且无来源），理论自由度 +1；" +
      "若 ρ 取质子 ρ_C=" + g(rho_cp) + " m，K=" + g(G / (coef * rho_cp * rho_cp)) +
      "，取值随粒子而变 ⇒ 该常数还必须是粒子依赖的，自由度进一步膨胀。")

    # ---------------- D1-c：改用 G=c³/[ℏ(κ_G²+τ_G²)]
    l_g = math.sqrt(HBAR * G / (C ** 3))
    inv_l2 = (C ** 3) / (HBAR * G)
    BO("D1-c", "修补候选 c：改用 G=c³/[ℏ(κ_G²+τ_G²)]（C13）",
      "反解 κ_G²+τ_G²=c³/(ℏG)=" + g(inv_l2) + " m⁻² ⇒ ℓ_G=1/√(κ_G²+τ_G²)=" + g(l_g) +
      " m，与普朗克长度 ℓ_P=" + g(LPL) + " m 相对偏差=" +
      g(abs(l_g - LPL) / LPL, 4) + "。" +
      "⇒ 该式与 G=ℏc/m_P² **完全等价**（ℓ_G=ℓ_P），无新增信息；" +
      "要使用它必须先由拓扑定出 ℓ_G=ℓ_P，即新增假设『螺旋总尺度等于普朗克长度』" +
      "（把尺度问题整个搬进 X3）。")

    # ---------------- D2：ρ 独立来源候选
    g_pred_ce = coef * rho_ce * rho_ce
    g_pred_cp = coef * rho_cp * rho_cp
    F("D2-a", "修补候选：用 ρ_C=ℏ/(mc) 作为 ρ 的独立定义",
      "ρ_C(e⁻)=" + g(rho_ce) + " m → G_pred=" + g(g_pred_ce) + "（偏离 " +
      g(G / g_pred_ce) + " 倍）；ρ_C(p)=" + g(rho_cp) + " m → G_pred=" + g(g_pred_cp) +
      "（偏离 " + g(G / g_pred_cp) + " 倍）。" +
      "⇒ ρ 的两个『独立来源』之间相差 " + g(rho_g / rho_ce) +
      " 倍（ρ_G vs ρ_C(e⁻)），且无论取哪个都无法复现 G。" +
      "修补代价：必须再引入一个量纲常数（回到 D1-b），或承认 G 该式不成立。")

    # ---------------- D4：统一 N 的口径
    na = 1.0 / (ALPHA * ALPHA * (1.0 - ALPHA))
    nb = 1.0 / (ALPHA * ALPHA) + 1.0 / ALPHA + 1.0 + ALPHA
    nb137 = 137.0 * 137.0 + 137.0 + 1.0 + 1.0 / 137.0
    na137 = 1.0 / ((1.0 / 137.0) ** 2 * (1.0 - 1.0 / 137.0))
    BO("D4-a", "修补候选：统一 α 口径后 N 的两定义",
      "统一取 CODATA α：N_A=" + g(na, 10) + "，N_B=" + g(nb, 10) + "，差 " +
      g(na - nb, 4) + "（=Σ_{n≥2}αⁿ）。统一取 α=1/137：N_A=" + g(na137, 8) +
      "，N_B=" + g(nb137, 8) + "，差 " + g(na137 - nb137, 4) + "。" +
      "⇒ 统一 α 后两定义差异仅 5e-5 量级，**冲突基本消解**；" +
      "但『四力归一化=1』只在 N_B 口径成立，取 N_A 时缺额 " +
      g(1.0 - (1.0 / (ALPHA * ALPHA) + 1.0 / ALPHA + 1.0 + ALPHA) / na, 4) +
      "（X13），故仍需二选一并放弃另一套诠释。")

    # 体系七暗能量命名 vs 实测
    f5_share = ALPHA * ALPHA / na
    omega_l = 0.69
    F("D4-b", "修补代价核查：α² 项被命名为暗能量，占比与实测差多少",
      "α²/N_A=" + g(f5_share) + "（体系七称『暗能量力』占比）；" +
      "实测暗能量密度参数 Ω_Λ≈" + str(omega_l) + "；相差 " + g(omega_l / f5_share) +
      " 倍。⇒ 若取 N_A（无穷级数）口径，体系七的『α²=暗能量』命名在数值上**相差 8 个数量级**，" +
      "不能作为任何观测支撑；该命名仅为数学项命名（L1/INFO），不构成预言。")

    # ---------------- D5：tanθ = √N 的四种修补
    alpha_obs = ALPHA
    # (a) α=√N ⇒ N=α²
    n_a1 = alpha_obs * alpha_obs
    # (b) N=1/α² ⇒ √N=1/α
    sqrt_nb = 1.0 / alpha_obs
    # (c) tanθ=1/√N
    inv_sqrt_137 = 1.0 / math.sqrt(137.0)
    # (d) N_twist 重命名
    n_twist = alpha_obs * alpha_obs / (1.0 + alpha_obs * alpha_obs)

    F("D5-a", "修补候选 a：承认 α=√N（则 N=α²）",
      "N=α²=" + g(n_a1) + "，与体系三/十的 N≈18917 相差 " + g(18917.0 / n_a1) +
      " 倍 ⇒ 归一化因子、18917 素数锚点、四力占比全部崩塌。代价：整个体系三+体系十报废。")

    F("D5-b", "修补候选 b：把 N 重定义为 1/α²（使 √N=1/α）",
      "√N=1/α=" + g(sqrt_nb) + "，而 α=" + g(alpha_obs) + "，仍差 " +
      g(sqrt_nb / alpha_obs) + " 倍 ⇒ 仍未消解矛盾（只是把矛盾从 1603 倍挪到 18779 倍）。")

    F("D5-c", "修补候选 c：把式改写为 tanθ=1/√N",
      "1/√137=" + g(inv_sqrt_137) + " vs α=" + g(alpha_obs) + "，差 " +
      g(inv_sqrt_137 / alpha_obs) + " 倍 ⇒ 仍不自洽（差 11.7 倍）。")

    BO("D5-d", "修补候选 d：承认 N_twist 与归一化因子 N 是两个不同对象（重命名）",
      "取 α=b/ρ 时 b²/(ρ²+b²)=α²/(1+α²)=" + g(n_twist) + "，它与 N≈18917 无任何数值关系。" +
      "⇒ 唯一自洽的修补是：把拓扑绕数量改名为 N_twist（=" + g(n_twist) +
      "），并声明它与归一化因子 N 无关。" +
      "代价：**体系二『由拓扑本征值推出 N=137』的核心目标彻底落空**（X4 由 open 变为『路径不存在』）。")

    return RESULTS


def counts():
    c = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
    for r in RESULTS:
        c[r["verdict"]] = c.get(r["verdict"], 0) + 1
    return c


def render():
    lines = []
    lines.append("# 矛盾修补方案可行性验算报告")
    lines.append("")
    lines.append("> 生成：`patch_feasibility.py`（分支 D 配套）。只算不判，失败照写。")
    lines.append("")
    c = counts()
    lines.append("| 判定 | 计数 |")
    lines.append("|------|------|")
    for k in ("PASS", "FAIL", "BOUNDARY", "INFO"):
        lines.append("| " + k + " | " + str(c.get(k, 0)) + " |")
    lines.append("")
    for r in RESULTS:
        lines.append("**" + r["id"] + " · [" + r["verdict"] + "] " + r["title"] + "**")
        lines.append("")
        lines.append(r["detail"])
        lines.append("")
    return "\n".join(lines)


def main():
    run()
    text = render()
    print(text)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "patch_feasibility_report.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(text)
    print("[written] " + out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
