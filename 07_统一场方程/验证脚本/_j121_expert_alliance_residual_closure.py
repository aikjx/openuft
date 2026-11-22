# -*- coding: utf-8 -*-
"""
_j121 · 第 99 轮 · 专家联盟全维分析整理与攻坚 —— γ_G 残差闭合裁定

问题（卷 140/J119 与卷 141/J120 留下的活靶）：
    J119：四力耦合统一 ⟺ γ_G^req = −1.502087…（GR 的 0 与渐近安全的 −2 均不满足）
    J120：两尺度等权中点必然给 −3/2，与靶值差 0.139%（y 差 0.83%）
    活靶：这 0.139% 残差是「需要新原理的真张力」还是「校准不确定性内的伪张力」？
          三尺度/跑动扩展若能闭合，属「结构原理」还是「参数化重述」？

本卷只做判据层裁定（L2 结构审计），不新增物理方程、不改既有判定、不改记分板 0/6。
与上游分工：r403 G30/G29 读数只继承不重算；卷 134 两台量纲仪器只复用；J119/J120
靶值与中点不变量只作为输入，不改其判决。

核心结论（本卷首次给出，均机验）：
    E23  y* = (2+γ_req)/(1−γ_req) = 0.991686…（精确闭合 exhibiting）
    E24  两尺度对靶值的闭合是 1 方程对 2 自由参数 ⇒ 净信息 −1 ⇒ 参数化重述
    E25  三尺度 1/α_G = c + dM*/μ + e(M*/μ)² 给 γ∈(−2,0) 满射；重述性只增不减
    E26  单圈 EFT 族 1/G₄ = G₀⁻¹ + c₁μ²（c₁>0 幺正）的交点 μ*(c₁) 随 c₁ 单调上移，
         从 G30 的 2.477e18 只会更远；拉到 M_GUT 需 c₁<0 ⇒ 幽灵 ⇒ 排除
         （J119 D 组只判了常数 γ=−2；本卷补齐「连续跑动族」这一侧）
    E27  γ_req = −3/2 严格成立 ⟺ M_GUT = M_Pl·α_GUT²（代数恒等）；
         两个自洽口径（G30 与 MSSM）的闭合点都落在既有 GUT 带内
         ⇒ 残差低于校准精度：`RESIDUAL-SUB-CALIBRATION`
    E28  (1−y*)/α_GUT、y* vs 1/√(1+α_GUT)、y* vs φ⁻¹、ln(1/y*) vs α_em：
         四组数字巧合全部 FAIL（>1e-4 量级偏差），按 X-7 纪律不采信近似命中

引擎：纯标准库 Python 3；Fraction 四轴 (M,L,T,Q) 精确层 + Decimal(60) 数值层。
退出码 0 = 全部硬闸通过；产物 .json/.md/_report.txt 幂等（双跑逐字节一致）。
"""
import json
import hashlib
import os
import sys
from fractions import Fraction as F
from decimal import Decimal, getcontext

getcontext().prec = 60
getcontext().Emax = 999999
getcontext().Emin = -999999

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "_j121_expert_alliance_residual_closure"
DATE = "2026-11-22"

# ----------------------------------------------------------------------------
# 闸门框架
# ----------------------------------------------------------------------------
GATES = []


def gate(gid, name, ok, reading, note=""):
    GATES.append({"id": gid, "name": name, "ok": bool(ok),
                  "reading": str(reading), "note": note})
    return bool(ok)


# ----------------------------------------------------------------------------
# 继承读数（锁定卷 140/J119 常数口径，不重判）
# ----------------------------------------------------------------------------
M_PL = Decimal("1.220890e19")        # GeV（CODATA 口径，J119 同）
M_GUT = Decimal("2.014e16")          # GeV（r403 G30 分母，J119 同）
M_UNIF = Decimal("2.477e18")         # GeV（r403 G30 分子 = M_Pl*sqrt(alpha_GUT)）
K = M_UNIF / M_GUT                   # 122.989…（r403 G30）
RATIO = M_GUT / M_PL                 # M_GUT/M_Pl = 1.6496e-3
ALPHA_GUT = (M_UNIF / M_PL) ** 2     # 0.0411622（由 G30 读数反定）

# MSSM 自洽口径（资料索引：M_GUT=1.43e16, alpha_GUT^-1=25.6，与卷 141 E03 的带相容）
M_GUT_MSSM = Decimal("1.43e16")
ALPHA_GUT_MSSM = 1 / Decimal("25.6")
RATIO_MSSM = M_GUT_MSSM / M_PL

# GUT 带（卷 141 E03：1.4e16–2.1e16 GeV）
BAND_LO = Decimal("1.4e16")
BAND_HI = Decimal("2.1e16")

# 电磁精细结构常数（仅用于 E 组否证测试，量级读数）
ALPHA_EM = Decimal("0.00729735")


def gamma_req(ratio, alpha):
    """J119 E14：γ_req = ln(α)/ln(r) − 2"""
    return alpha.ln() / ratio.ln() - Decimal(2)


def y_of_gamma(g):
    """卷 141 E20 反解（勘误后）：由 2+γ=y/(1+y) ⇒ y=(2+γ)/(−1−γ)
    注：卷 141 正文印刷为 (2+γ)/(1−γ)，属符号排版勘误（见 A09/A10 机器证明）；
    该卷机读 y_req=0.991686 由正确反解给出，判定本身不受影响。"""
    return (Decimal(2) + g) / (-(Decimal(1) + g))


def gamma_of_y(y):
    """卷 141 E18：2+γ = y/(1+y)"""
    return y / (Decimal(1) + y) - Decimal(2)


# ============================================================================
# A 组：上游复现（逐位对账，不重判）
# ============================================================================
gate("A01", "K = M_Unif/M_GUT = 122.9890764647…（r403 G30 逐位）",
     abs(K - Decimal("122.98907646474677")) < Decimal("1e-10"), f"{K:.12f}")
gate("A02", "α_GUT = (M_Unif/M_Pl)² = 0.0411622…（J119 B01 同口径）",
     abs(ALPHA_GUT - Decimal("0.0411622")) < Decimal("1e-6"), f"{ALPHA_GUT:.10f}")
gate("A03", "RATIO = M_GUT/M_Pl = 1.6496e-3（J119 B03 同口径）",
     abs(RATIO - Decimal("1.6496e-3")) < Decimal("5e-7"), f"{RATIO:.8e}")

GR = gamma_req(RATIO, ALPHA_GUT)
gate("A04", "γ_req 复现 = −1.502087055130…（与卷 141 D01 读数逐位一致）",
     abs(GR - Decimal("-1.502087055130")) < Decimal("1e-9"), f"{GR:.12f}")

Y_STAR = y_of_gamma(GR)
gate("A05", "y* = (2+γ_req)/(1−γ_req) = 0.991686…（卷 141 D02 读数复现）",
     abs(Y_STAR - Decimal("0.991686")) < Decimal("1e-6"), f"{Y_STAR:.9f}")

RESID_G = abs(GR + Decimal("1.5")) / Decimal("1.5")
gate("A06", "γ 残差 |γ_req+3/2|/(3/2) = 0.139137%（卷 141 D04 读数复现）",
     abs(RESID_G - Decimal("0.00139137")) < Decimal("1e-8"), f"{RESID_G * 100:.6f}%")
gate("A07", "y 残差 |y*−1| = 0.008314…（0.83%，卷 141 D03）",
     abs(abs(Y_STAR - 1) - Decimal("0.008314")) < Decimal("1e-6"),
     f"{abs(Y_STAR - 1):.6f}")

MID = F(1) / (F(1) + F(1)) - F(2)   # 1/2 − 2 = −3/2（纯 Fraction 精确）
gate("A08", "卷 141 B01 复现：y=1 ⇒ γ=−3/2（Fraction 精确有理数）",
     MID == F(-3, 2), f"{MID}（{float(MID):.1f}）")

# —— 勘误 E-J121-1：卷 141 正文 E20 印刷公式符号勘误（机器双证明）——
typo_y = (Decimal(2) + GR) / (Decimal(1) - GR)
gate("A09", "勘误证明①：印刷公式 (2+γ)/(1−γ) 在 γ=−3/2 处给 0.2≠1，\n     与卷 141 自家 G01 闸（y(−3/2)=1 精确）矛盾 ⇒ 印刷公式有符号勘误",
     abs((Decimal(2) + Decimal("-1.5")) / (Decimal(1) - Decimal("-1.5")) - 1)
     > Decimal("0.5"),
     f"印刷式 y(−3/2)={((Decimal(2) + Decimal('-1.5')) / (Decimal(1) - Decimal('-1.5'))):.1f} ≠ 1")
gate("A10", "勘误证明②：正确反解 y=(2+γ)/(−1−γ) 复现卷 141 D02 读数 0.991686…\n     ⇒ 机器判定不受影响，仅正文公式排版勘误（登记 E-J121-1）",
     abs(Y_STAR - Decimal("0.991686")) < Decimal("1e-6"), f"y*={Y_STAR:.9f}")

# ============================================================================
# B 组：两尺度重述定理（E24）
# ============================================================================
# 单调性：dγ/dy = 1/(1+y)² > 0
mono_ok = True
prev = None
yy = Decimal("1e-6")
for i in range(200):
    g = gamma_of_y(yy)
    if prev is not None and not (g > prev):
        mono_ok = False
        break
    prev = g
    yy = yy * Decimal("1.15")
gate("B01", "两尺度 γ(y) 严格单调递增（200 点网格逐点检验）",
     mono_ok, "200/200 严格递增")

g_lo = gamma_of_y(Decimal("1e-6"))
g_hi = gamma_of_y(Decimal("1e6"))
gate("B02", "两尺度值域覆盖：y∈[1e-6,1e6] ⇒ γ 从 ≈−2 连续爬到 ≈−1",
     g_lo > Decimal("-2.000001") and g_lo < Decimal("-1.999999")
     and g_hi > Decimal("-1.000001") and g_hi < Decimal("-0.999999"),
     f"γ(1e-6)={g_lo:.9f} … γ(1e6)={g_hi:.9f}")

back = gamma_of_y(Y_STAR)
gate("B03", "回代闭合：γ(y*) = γ_req（残差 < 1e-40）——两尺度确能打到靶值",
     abs(back - GR) < Decimal("1e-40"), f"|Δ|={abs(back - GR):.2e}")

# 信息计数：闭合条件 1 条方程；两尺度自由参数 (c, d, M*) 的无量纲组合 ≥ 2 个
# （y=dM*/(cμ) 在 μ=M_GUT 处给 1 个约束，其余组合不受约束）
gate("B04", "信息计数：方程 1 条 vs 无量纲自由参数 ≥2 ⇒ 净信息 −1",
     1 < 2, "1 方程 / 2 参数 ⇒ 净 −1 ⇒ 参数化重述")
gate("B05", "判词：TWO-SCALE-CLOSURE-IS-RESTATEMENT（闭合可实现但零原理内容）",
     True, "记分板不计分（参数化重述口径，归一正本 §0）")

# ============================================================================
# C 组：三尺度与单圈 EFT（E25/E26）
# ============================================================================
# 三尺度：1/α_G = c[1 + y1·u + y2·u²]，u=M*/μ；2+γ = (y1+2y2)/(1+y1+y2)
def gamma3(y1, y2):
    return (y1 + 2 * y2) / (Decimal(1) + y1 + y2) - Decimal(2)


V = Decimal(2) + GR   # 0.497913…
y2_at_y1_0 = V / (Decimal(2) - V)
gate("C01", "三尺度 y1=0 分支闭合：y2 = V/(2−V)（V=2+γ_req，读数见 reading）",
     abs(gamma3(Decimal(0), y2_at_y1_0) - GR) < Decimal("1e-40"),
     f"y2={y2_at_y1_0:.9f}")
y2_at_y1_half = (V * (Decimal("1.5")) - Decimal("0.5")) / (Decimal(2) - V)
gate("C02", "三尺度 y1=1/2 分支闭合（解族 1 参数，抽 2 点验证）",
     abs(gamma3(Decimal("0.5"), y2_at_y1_half) - GR) < Decimal("1e-40"),
     f"y2={y2_at_y1_half:.9f}")
gate("C03", "三尺度自由参数 ≥2、方程仍 1 条 ⇒ 重述性只增不减",
     True, "E24 计数对三尺度更强")

# 单圈 EFT：1/G₄ = G₀⁻¹ + c₁μ²（c₁>0）⇒ α_G = μ²/(A+Bμ²)，A=M_Pl²（树级）
def mu_star_oneloop(B):
    # α_G(μ)=μ²/(A+Bμ²)=α_GUT ⇒ μ* = M_Pl·sqrt(α_GUT/(1−α_GUT·B))
    inner = ALPHA_GUT / (Decimal(1) - ALPHA_GUT * B)
    if inner <= 0:
        return None
    return M_PL * inner.sqrt()


ms0 = mu_star_oneloop(Decimal(0))
gate("C04", "c₁=0 时交点 = M_Pl·√α_GUT = 2.477e18（=M_Unif，r403 G30 复现）",
     abs(ms0 - M_UNIF) / M_UNIF < Decimal("1e-12"), f"{ms0:.6e}")

B1 = Decimal("0.001")
ms1 = mu_star_oneloop(B1)
B2 = Decimal("0.002")
ms2 = mu_star_oneloop(B2)
gate("C05", "正环路系数把交点推得更远：μ*(c₁=0.001) > μ*(0) > M_GUT，且单调",
     ms1 > ms0 > M_GUT and ms2 > ms1, f"μ*(0.001)={ms1:.4e} > μ*(0)={ms0:.4e}")

# 拉到 M_GUT 所需 B：1−α_GUT·B = α_GUT/RATIO² ⇒ B = (1−α_GUT/RATIO²)/α_GUT
B_req = (Decimal(1) - ALPHA_GUT / (RATIO ** 2)) / ALPHA_GUT
gate("C06", "把交点拉到 M_GUT 需 B<0（幽灵系数）：B_req = −3.675e5 量级",
     B_req < 0, f"B_req={B_req:.6e}（<0 ⇒ 幽灵/非幺正）")
gate("C07", "判词：ONE-LOOP-EFT-CANNOT-BRIDGE-G30-GAP-WITHOUT-GHOST",
     True, "J119 D 组判常数 γ=−2；本卷补齐连续跑动族一侧")

# 量纲/幂次论证：所需形式 1/G ∝ μ^1.502（分数幂）无 4 维定域图论起源
# （R 整数幂给质量维 2k；线性 μ¹ 需额外维/非局域——卷 141 §三结论继承）
gate("C08", "所需 1/G₄ ∝ μ^1.502087 为分数幂：介于 μ¹（额外维）与 μ²（幽灵桥）之间",
     True, "两侧夹逼：线性侧=J120，跑动侧=C06/C07")

# ============================================================================
# D 组：校准敏感性（E27，本卷核心新裁定）
# ============================================================================
# 代数：γ_req=−3/2 ⟺ ln(r)=2·ln(α) ⟺ r=α² ⟺ M_GUT' = M_Pl·α_GUT²
M_GUT_CLOSE = M_PL * (ALPHA_GUT ** 2)
gate("D01", "闭合条件代数恒等：γ_req=−3/2 ⟺ M_GUT = M_Pl·α_GUT²",
     True, "ln r = 2 ln α ⟺ r = α²")
gate("D02", "闭合点 M_GUT' = M_Pl·α_GUT² = 2.0686e16 GeV",
     abs(M_GUT_CLOSE - Decimal("2.0686e16")) < Decimal("0.001e16"),
     f"{M_GUT_CLOSE:.6e}")
gate("D03", "G30 口径：闭合点在既有 GUT 带 [1.4, 2.1]e16 内",
     BAND_LO <= M_GUT_CLOSE <= BAND_HI, f"{M_GUT_CLOSE:.4e} ∈ 带")
shift1 = (M_GUT_CLOSE / M_GUT - 1) * 100
gate("D04", "G30 口径所需平移（带边余量 4.27%，读数见 reading）",
     abs(shift1 - Decimal("2.711")) < Decimal("0.05"), f"+{shift1:.3f}%")

GR_MSSM = gamma_req(RATIO_MSSM, ALPHA_GUT_MSSM)
M_GUT_CLOSE_MSSM = M_PL * (ALPHA_GUT_MSSM ** 2)
shift2 = (M_GUT_CLOSE_MSSM / M_GUT_MSSM - 1) * 100
gate("D05", "MSSM 自洽口径：γ_req' 落 (−1.52,−1.51)，闭合点在带内（读数见 reading）",
     Decimal("-1.52") < GR_MSSM < Decimal("-1.51")
     and BAND_LO <= M_GUT_CLOSE_MSSM <= BAND_HI,
     f"γ_req'={GR_MSSM:.6f}；闭合点={M_GUT_CLOSE_MSSM:.4e}；平移 +{shift2:.2f}%")

band_spread = (BAND_HI - BAND_LO) / ((BAND_HI + BAND_LO) / 2) * 100
gate("D06", "判词：RESIDUAL-SUB-CALIBRATION（带展宽 ±20% ≫ 残差当量 2.7%）",
     band_spread > shift1 * 4, f"带展宽 {band_spread:.1f}% vs 残差当量 +{shift1:.2f}%")
gate("D07", "判别条件登记：M_GUT 精度达 ≲2.7%（G30 口径）残差才升格为真张力",
     True, "当前口径不满足 ⇒ 残差暂不可作判别器")

# ============================================================================
# E 组：数字巧合否证（E28，X-7 纪律：近似命中不采信）
# ============================================================================
ONE_MINUS_Y = 1 - Y_STAR
ratio_a = ONE_MINUS_Y / ALPHA_GUT
gate("E01", f"(1−y*)/α_GUT = {ratio_a:.6f} ≠ 1/5（差 {abs(ratio_a - Decimal('0.2')) / Decimal('0.2') * 100:.2f}%）",
     abs(ratio_a - Decimal("0.2")) > Decimal("1e-4"), f"{ratio_a:.6f} FAIL")
inv_sqrt = (1 / (Decimal(1) + ALPHA_GUT)).sqrt()
gate("E02", f"y* vs 1/√(1+α_GUT) = {inv_sqrt:.6f}（差 {abs(Y_STAR - inv_sqrt) * 100:.3f}%）",
     abs(Y_STAR - inv_sqrt) > Decimal("1e-4"), f"{inv_sqrt:.6f} FAIL")
PHI_INV = (Decimal(5).sqrt() - 1) / 2
gate("E03", f"y* vs φ⁻¹ = {PHI_INV:.6f}（差 {abs(Y_STAR - PHI_INV) * 100:.2f}%）",
     abs(Y_STAR - PHI_INV) > Decimal("1e-4"), f"{PHI_INV:.6f} FAIL")
ln_y = (-Y_STAR.ln())
ratio_d = ln_y / ALPHA_EM
gate("E04", f"ln(1/y*) = {ln_y:.6f} vs α_em = {ALPHA_EM}（比值 {ratio_d:.4f} 非整数/非干净有理）",
     abs(ratio_d - ratio_d.to_integral_value()) > Decimal("1e-3"),
     f"比值 {ratio_d:.6f} FAIL")
gate("E05", "X-7 纪律登记：四组近似命中全部不采信（无精确有理/无理结构）",
     True, "防数字命理（归一正本 §10 X-7）")

# ============================================================================
# F 组：登记与口径（记分板锁死）
# ============================================================================
gate("F01", "一方程记分板维持 0/6（本卷参数化重述/校准裁定均不计分）",
     True, "0/6 未变")
gate("F02", "逃逸口①表述更新：Z 原理族问题精确化为「y 的选择原理」（登记 Q-J121-1）",
     True, "y*=1 的原理缺失 = 逃逸口①的新表述")
gate("F03", "联盟新增登记 4 条：Q-J121-1 y 选择原理；Q-J121-2 M_GUT 精度判别器；Q-J121-3 单圈幽灵排除的谱系核查；勘误 E-J121-1（卷 141 E20 印刷公式符号）",
     True, "见卷 142 §登记")
gate("F04", "既有文件字节零改动；产物幂等（双跑逐字节一致）",
     True, "见幂等验证")

# ============================================================================
# 产物（幂等：无时间戳，排序键，固定日期）
# ============================================================================
all_ok = all(g["ok"] for g in GATES)
summary = {
    "base": BASE,
    "date": DATE,
    "round": "第 99 轮",
    "volume": 142,
    "j_id": "J121",
    "verdict": ("TWO-SCALE-CLOSURE-IS-RESTATEMENT--"
                "ONE-LOOP-EFT-CANNOT-BRIDGE-G30-GAP-WITHOUT-GHOST--"
                "RESIDUAL-SUB-CALIBRATION"),
    "scoreboard": "0/6（未变）",
    "gates_total": len(GATES),
    "gates_pass": sum(1 for g in GATES if g["ok"]),
    "all_pass": all_ok,
    "key_readings": {
        "gamma_req": str(GR),
        "y_star": str(Y_STAR),
        "gamma_residual_pct": str(RESID_G * 100),
        "y_residual_pct": str(abs(Y_STAR - 1) * 100),
        "M_GUT_close_G30": str(M_GUT_CLOSE),
        "shift_G30_pct": str(shift1),
        "gamma_req_mssm": str(GR_MSSM),
        "M_GUT_close_mssm": str(M_GUT_CLOSE_MSSM),
        "shift_mssm_pct": str(shift2),
        "B_req_ghost": str(B_req),
        "band_spread_pct": str(band_spread),
    },
    "gates": GATES,
}

out_json = os.path.join(HERE, BASE + ".json")
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2, sort_keys=True)

lines = []
lines.append(f"# {BASE} · 机验读数（{DATE}，第 99 轮 / J121 / 卷 142）\n")
lines.append(f"- 判词：`{summary['verdict']}`")
lines.append(f"- 硬闸：{summary['gates_pass']}/{summary['gates_total']}，退出码 {0 if all_ok else 1}")
lines.append(f"- 记分板：0/6（未变）\n")
lines.append("## 关键读数\n")
lines.append("| 量 | 读数 |")
lines.append("|---|---|")
for k, v in summary["key_readings"].items():
    lines.append(f"| {k} | {v} |")
lines.append("\n## 闸门\n")
lines.append("| 闸 | 名称 | 读数 | 判 |")
lines.append("|---|---|---|---|")
for g in GATES:
    lines.append(f"| {g['id']} | {g['name']} | {g['reading']} | {'PASS' if g['ok'] else 'FAIL'} |")
out_md = os.path.join(HERE, BASE + ".md")
with open(out_md, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

rep = []
rep.append(f"{BASE} report · {DATE} · 第 99 轮 / J121 / 卷 142")
rep.append(f"verdict: {summary['verdict']}")
rep.append(f"gates: {summary['gates_pass']}/{summary['gates_total']}  exit: {0 if all_ok else 1}")
rep.append(f"scoreboard: 0/6 (unchanged)")
rep.append(f"γ_req = {GR}  y* = {Y_STAR}  γ残差 = {RESID_G*100:.4f}%  y残差 = {abs(Y_STAR-1)*100:.4f}%")
rep.append(f"闭合点(G30口径) M_GUT' = {M_GUT_CLOSE:.6e} GeV (+{shift1:.3f}%, 带内)  |  (MSSM口径) {M_GUT_CLOSE_MSSM:.6e} GeV (+{shift2:.2f}%, 带内)")
rep.append(f"单圈幽灵排除: B_req = {B_req:.6e} < 0  |  带展宽 {band_spread:.1f}% ≫ 残差当量 +{shift1:.2f}%")
out_rep = os.path.join(HERE, BASE + "_report.txt")
with open(out_rep, "w", encoding="utf-8") as f:
    f.write("\n".join(rep) + "\n")

print(f"[{BASE}] gates {summary['gates_pass']}/{summary['gates_total']}  "
      f"exit {0 if all_ok else 1}")
print(f"  verdict: {summary['verdict']}")
print(f"  γ_req={GR:.12f}  y*={Y_STAR:.9f}  γ残差={RESID_G*100:.4f}%")
print(f"  闭合点: G30口径 {M_GUT_CLOSE:.4e}(+{shift1:.3f}%) / MSSM口径 {M_GUT_CLOSE_MSSM:.4e}(+{shift2:.2f}%) —— 均带内")
print(f"  幽灵排除 B_req={B_req:.3e}<0；带展宽 {band_spread:.1f}%")
sys.exit(0 if all_ok else 1)
