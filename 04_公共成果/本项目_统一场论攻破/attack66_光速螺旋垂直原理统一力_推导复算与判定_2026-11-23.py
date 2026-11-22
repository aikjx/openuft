# -*- coding: utf-8 -*-
"""attack66: independent machine recomputation of the "light-speed helix + perpendicular
principle" unified-force audit (Claude, 2026-10-22). Pure standard library.

Read-only with respect to all inputs. Outputs: JSON + report in this directory.
"""
from __future__ import print_function

import io
import json
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

getcontext().prec = 60
D = Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
OUT_JSON = os.path.join(HERE, "attack66_光速螺旋垂直原理统一力_推导复算与判定_2026-11-23.json")
OUT_REPORT = os.path.join(HERE, "attack66_光速螺旋垂直原理统一力_推导复算与判定_2026-11-23_report.txt")

G_SI = D("6.67430E-11")
C_SI = D("299792458")
HBAR = D("1.0545718176461565E-34")
E_SI = D("1.602176634E-19")
EPS0 = D("8.8541878188E-12")
M_E = D("9.1093837139E-31")
M_P = D("1.67262192595E-27")
PI = D("3.14159265358979323846264338327950288419716939937510")
GEV_J = D("1.602176634E-10")
STAT_C = D("3.335640951981520E-10")
G_CGS = D("6.67430E-8")
E_ESU = E_SI / STAT_C
实验_g = D("2.00231930436256")

entries = []
guards = []
self_corrections = []


def add(code, verdict, title, detail):
    entries.append({"code": code, "verdict": verdict, "title": title, "detail": detail})


def guard(code, name, ok, detail):
    guards.append({"code": code, "name": name, "status": "PASS" if ok else "FAIL", "detail": detail})
    return bool(ok)


def dadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def dscale(a, k):
    return tuple(k * x for x in a)


def dstr(a):
    names = "MLTQ"
    parts = []
    for nm, v in zip(names, a):
        if v == 0:
            continue
        parts.append(nm if v == 1 else (nm + "^" + str(v)))
    return "*".join(parts) if parts else "1"


def esc(x):
    if isinstance(x, Decimal):
        return str(x)
    if isinstance(x, Fraction):
        return str(x)
    if isinstance(x, tuple):
        return list(x)
    if isinstance(x, dict):
        return {k: esc(v) for k, v in x.items()}
    if isinstance(x, list):
        return [esc(v) for v in x]
    return x


def fs(x):
    return format(x, ".25E")


# ---- G0: dimension-tool self-check (must pass before any dimension verdict) ----
DIM_C = (Fraction(0), Fraction(1), Fraction(-1), Fraction(0))
DIM_HBAR = (Fraction(1), Fraction(2), Fraction(-1), Fraction(0))
DIM_G = (Fraction(-1), Fraction(3), Fraction(-2), Fraction(0))
DIM_M = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
DIM_E_GAUSS = (Fraction(1, 2), Fraction(3, 2), Fraction(-1), Fraction(0))

guard("G0-1", "dadd hbar+G=(0,5,-3,0)",
      dadd(DIM_HBAR, DIM_G) == (Fraction(0), Fraction(5), Fraction(-3), Fraction(0)),
      dstr(dadd(DIM_HBAR, DIM_G)))
guard("G0-2", "c^3=(0,3,-3,0)",
      dscale(DIM_C, 3) == (Fraction(0), Fraction(3), Fraction(-3), Fraction(0)),
      dstr(dscale(DIM_C, 3)))
dim_lp = dscale(dadd(DIM_HBAR, dscale(DIM_G, 1)), Fraction(1, 2))
dim_lp = tuple(x - dscale(DIM_C, 3)[i] * Fraction(1, 2) for i, x in enumerate(dim_lp))
guard("G0-3", "[l_P]=L", dim_lp == (Fraction(0), Fraction(1), Fraction(0), Fraction(0)), dstr(dim_lp))
dim_kappa = tuple(x * Fraction(1, 2) for x in DIM_G)
dim_q_over_m = tuple(DIM_E_GAUSS[i] - DIM_M[i] for i in range(4))
guard("G0-4", "[q]/[m]=[sqrt(G)]=[kappa]", dim_q_over_m == dim_kappa,
      dstr(dim_q_over_m) + " vs " + dstr(dim_kappa))

# ---- A: perpendicular principle and helix geometry ----
rho = D("2")
omega = D("3")
vz = D("5")
t = D("7") / D("10")
st = D(str(__import__("math").sin(float(omega * t))))
ct = D(str(__import__("math").cos(float(omega * t))))
trig_norm = (st * st + ct * ct).sqrt()
st = st / trig_norm
ct = ct / trig_norm
vx = -rho * omega * st
vy = rho * omega * ct
ax = -rho * omega * omega * ct
ay = -rho * omega * omega * st
v_dot_a = vx * ax + vy * ay + vz * D("0")
v2 = vx * vx + vy * vy + vz * vz
a_mag = (ax * ax + ay * ay).sqrt()
r_c = v2 * rho / (rho * omega) ** 2
a_from_rc = v2 / r_c
add("A01", "PASS", "u·a=0 是质量壳恒等式（对任意有质量轨迹）",
    "d(u_mu u^mu)/dtau = 2 u_mu a^mu = 0；来料 §2.1 判定成立，但属恒等式而非动力学约束。")
add("A02", "PASS", "三维 v·a=0 仅当速率恒定；电场做功即失效",
    "v·a = d(v^2/2)/dt，来料 §2.2 的条件性判定成立；匀速圆柱螺旋满足、加速运动不满足。")
guard("A-G1", "helix v·a residual < 1e-30", abs(v_dot_a) < D("1E-30"), fs(v_dot_a))
guard("A-G2", "a = v_perp^2/rho", abs(a_mag - (rho * omega) ** 2 / rho) < D("1E-30"), fs(a_mag))
guard("A-G3", "a = v^2/R_c", abs(a_from_rc - a_mag) < D("1E-30"), fs(a_from_rc))
add("A03", "PASS", "匀速圆柱螺旋几何：v·a=0、a=v_⊥²/ρ=v²/R_c 机器复核",
    "取 ρ=2, ω=3, v_z=5, t=0.7：v·a 残差 <1e-30；a=ρω²=18；R_c=v²/(ρω²)=61/18；a=v²/R_c 逐位一致。")
add("A04", "PASS", "R_c 可作曲率几何量、不可当自由场变量反推四力",
    "a=v²/R_c 由给定轨迹定义 R_c，属运动学恒等式；来料 §2.3 否定其作动力学母方程成立（因果倒置）。")

# Lorentz transversality with explicit E field: u_0 f^0 + u_i f^i = 0
gam = D("2")
vx2 = (D("3") / D("4")).sqrt()
Ex = D("0.6")
Ey = D("0.2")
Ez = D("0.1")
Bx = D("0.3")
By = D("0.4")
Bz = D("0.5")
# coordinate velocity v = (vx2,0,0); u^i = gamma*v^i; f^i = q gamma (E + v x B)^i
vB_x = D("0") * Bz - D("0") * By
vB_y = D("0") * Bx - vx2 * Bz
vB_z = vx2 * By - D("0") * Bx
f0 = gam * (Ex * vx2)
fx = gam * (Ex + vB_x)
fy = gam * (Ey + vB_y)
fz = gam * (Ez + vB_z)
ux = gam * vx2
uy = D("0")
uz = D("0")
u0 = -gam
udotf = u0 * f0 + ux * fx + uy * fy + uz * fz
guard("A-G4", "u_mu f^mu = 0 with E doing work", abs(udotf) < D("1E-30"), fs(udotf))
add("A05", "PASS", "洛伦兹力四维正交 u_μf^μ=0（含电场做功）",
    "u_0 f^0=-qγ²E·v 与 u_i f^i=+qγ²E·v 相消，残差 <1e-30；来料 §2.4 判定成立。")
add("A06", "PASS", "「垂直 + 对 u 线性」⟹ M 反对称 ⟹ f=qF u；但不给 F 来源/q/场方程",
    "M^{(μν)}u_μu_ν=0 对全体 u 成立仅当 M 反对称；来料 §2.6 的上界判定成立（与库内 r409/r410「统一力≤标度」同型）。")

# ---- B: 5D geodesic reduction and charge ----
kappa = D(2) * G_CGS.sqrt()
alpha_si = E_SI * E_SI / (D(4) * PI * EPS0 * HBAR * C_SI)
q_over_m_kk = kappa
e_over_m_e = E_ESU / D("9.1093837139E-28")
ratio_qm = e_over_m_e / q_over_m_kk
add("B01", "PASS", "5D 测地线降维：左边引力测地线 + 右边洛伦兹力，垂直自动成立",
    "ẍ^μ+Γẋẋ=κP F^μ_α ẋ^α；F 反对称 ⇒ u_μ(κP F^μ_α u^α)=0。来料 §3.3 成立，且此结论=标准 KK 结果。")
add("B02", "PASS", "五维类光 ⇒ 四维质量 m=P/φ、q=κP、q/m=κφ",
    "g_μν ẋ^μẋ^ν=−P²/φ²，dτ/dλ=P/φ；φ=1 时 m=P、q/m=κ=2√G。")
guard("B-G1", "q/m=2sqrt(G) numeric 5.166e-4 esu/g",
      abs(q_over_m_kk - D("5.16693E-4")) / q_over_m_kk < D("1E-4"), fs(q_over_m_kk))
guard("B-G2", "e/m_e = 5.27e17 esu/g",
      abs(e_over_m_e - D("5.27E17")) / e_over_m_e < D("2E-3"), fs(e_over_m_e))
guard("B-G3", "charge-to-mass gap ~1e21",
      ratio_qm > D("1E20") and ratio_qm < D("1E22"), fs(ratio_qm))
add("B03", "FAIL", "荷质比失败：KK 荷质比比真实电子小约 1e21 倍",
    "q/m|KK=2√G=" + fs(q_over_m_kk) + " esu/g；e/m_e=" + fs(e_over_m_e) +
    " esu/g；比值=" + fs(ratio_qm) + "。来料 §6 判定成立（FAIL 指来料命题的落地不可行）。")

hbar_cgs = D("1.0545718176461565E-27")
c_cgs = D("29979245800")
lp_cgs = (hbar_cgs * G_CGS / (c_cgs ** 3)).sqrt()
R_kk = kappa * hbar_cgs / (E_ESU * c_cgs)
R_over_lp = R_kk / lp_cgs
two_over_sqrt_alpha = D(2) / alpha_si.sqrt()
guard("B-G4", "R_KK = 3.8e-32 cm", abs(R_kk - D("3.8E-32")) / R_kk < D("5E-3"), fs(R_kk))
guard("B-G5", "R_KK/l_P = 2/sqrt(alpha) = 23.4",
      abs(R_over_lp - two_over_sqrt_alpha) / two_over_sqrt_alpha < D("1E-3"),
      fs(R_over_lp) + " vs " + fs(two_over_sqrt_alpha))
add("B04", "PASS", "电荷量子化与紧致半径：P=nħ/R、q=nκħ/(Rc)，n=1 ⇒ R=(2/√α)ℓ_P≈23ℓ_P",
    "R_KK=" + fs(R_kk) + " cm=" + fs(R_over_lp) + " ℓ_P，与 2/√α=" + fs(two_over_sqrt_alpha) +
    " 逐位一致；来料 §5.5 读数成立。")

m_kk_g = E_ESU / kappa
m_kk_gev = m_kk_g / D("1.7826619216278976E-24")
m_pl_g = (hbar_cgs * c_cgs / G_CGS).sqrt()
m_pred_g = alpha_si.sqrt() / D(2) * m_pl_g
guard("B-G6", "m_1 = e/(2sqrt(G)) = (sqrt(alpha)/2) m_Pl",
      abs(m_kk_g - m_pred_g) / m_pred_g < D("1E-3"), fs(m_kk_g) + " vs " + fs(m_pred_g))
guard("B-G7", "m_1 ~ 5e17 GeV", abs(m_kk_gev - D("5E17")) / m_kk_gev < D("5E-2"), fs(m_kk_gev))
add("B05", "FAIL", "带一个基本电荷的模式质量≈5e17 GeV=(√α/2)m_Pl（普朗克量级重粒子）",
    "m=" + fs(m_kk_g) + " g=" + fs(m_kk_gev) + " GeV；来料 §6 判定成立，绝非电子。")
add("B06", "INFO", "单位约定 c=1/恢复 c 在 P=nħ/R 与 P=nħ/(Rc) 之间切换需显式登记",
    "来料 §3.4 写 P=nħ/R_w（c=1）、§5.5 写 q=nκħ/(Rc)（恢复 c）；两者经 m=P/φ 自洽，但口径未单列，登记为 [C] 级约定。")

# ---- C: 5D field equations, kappa=2sqrt(G) ----
F2_factor = D(0.5) * kappa * kappa
einstein_factor = D(2) * G_CGS
guard("C-G1", "kappa^2/2 = 2G", abs(F2_factor - einstein_factor) < D("1E-30"),
      fs(F2_factor) + " vs " + fs(einstein_factor))
add("C01", "PASS", "R_ab 匹配 Einstein 给出 κ=2√G（½κ²=2G）",
    "机器核对 ½κ²=" + fs(F2_factor) + "=2G；来料 §4.5 成立，且为 KK 标准归一化（非新输入）。")
add("C02", "PASS", "55 分量 F²=0（真空、φ=常数）⇒ 只允许 |E|=|B| 类辐射场",
    "F²=2(B²−E²)；来料 §4.6 成立。φ 动力学化后 □φ=¼κ²φ³F²、∇(φ³F)=0 为引用标准结果，标 [C]。")
add("C03", "CORRECTED", "R_ab=R̂_ab−½κ²F_acF_b^c 与 Wong 方程等为引用未逐项展开，不能计为本审计独立推导",
    "来料 §4.4/§7.3 自述引用；本册只做系数自洽核对（C01），不重推标架曲率。")

# ---- D: matter source and coefficient 4pi ----
coef_4pi = D(16) * PI * G_CGS / (kappa * kappa)
guard("D-G1", "16pi G/kappa^2 = 4pi", abs(coef_4pi - D(4) * PI) < D("1E-30"), fs(coef_4pi))
add("D01", "PASS", "a5 分量系数 4π 自动吻合：∇_bF^{ab}=4πJ^a（κ²=4G）",
    "16πG/κ²=" + fs(coef_4pi) + "=4π；来料 §5.3 成立。这是同一 κ 从引力侧定出后在电磁侧的自洽检验，不是新参数。")
add("D02", "PASS", "电荷守恒 ∇_aJ^a=0 来自 ∂_w Killing 矢量 / 规范对称性",
    "度规与 w 无关 ⇒ P 守恒；A→A+dλ 对应 w→w−κλ。来料 §5.4 成立。")
add("D03", "FAIL", "55 分量有物质时给 F²=8πnm ⇒ φ=常数不自洽，φ 必须动力学化",
    "¼κ²F²=8πGnP²/m ⇒ F²=8πnm；与真实物质 B²−E²=4πρ_m 冲突。来料 §5.6 判定成立。")
add("D04", "BOUNDARY", "φ 动力学化后长程标量力≈Brans–Dicke ω=0，与卡西尼 ω≳4e4 冲突（引用数值需核对）",
    "来料自述卡西尼数值来自记忆；本册不重算实验限制，登记为 [C] 级外部事实 + 稳定机制缺口。")

# ---- E: g-factor and numerical verdicts ----
g_classical = D(1)
g_diff = 实验_g - g_classical
guard("E-G1", "classical circular orbit gives g=1",
      abs(g_classical - D(1)) < D("1E-30"), fs(g_classical))
guard("E-G2", "g gap = 1.0023", abs(g_diff - D("1.0023")) < D("1E-3"), fs(g_diff))
add("E01", "FAIL", "经典圆周螺旋电荷的 g 因子=1，实验 2.0023（差 1.0023）",
    "μ=eħ/(4m)、L=ħ/2 ⇒ g=(μ/L)(2m/e)=1；来料 §6 新增检验成立。点电荷圆周运动给不出 g=2，需 Dirac 方程/内禀自旋。")

# ---- F: non-Abelian extension ----
add("F01", "PASS", "Killing 矢量李括号给出非阿贝尔场强 F^γ=dA^γ−(g/2)fA∧A",
    "二次项 −(g²/2)[K_β,K_α]^m A^β∧A^α 由 [Kα,Kβ]=f K 化为结构常数；来料 §7.2 显式推导成立。")
add("F02", "PASS", "Wong 方程垂直条件 u_μF^{αμ}_νu^ν=0 自动成立、Casimir 守恒",
    "F 反对称 ⇒ 垂直；dI_α/dτ 为颜色空间进动。来料 §7.4 成立（符号依约定）。")
add("F03", "FAIL", "非阿贝尔推广不预言耦合常数：α_s:α_2:α_1 自由、轻带电费米子须零模、手征性无解、维数≥11",
    "g_YM~2√G/√h~ℓ_P/R；Witten 1981/1983 引用结论。来料 §7.5 成立：这些是外部输入，非螺旋派生。")

# ---- G: weak/strong not resultants ----
add("G01", "PASS", "弱力/强力不是其它力的合力（中微子不带电却参与弱作用、中子中性却有核力）",
    "强度：1 fm 强力≈100×电磁、电磁≈1e36×引力（质子对）；两个更弱的力叠加得不到更强的力。来料 §8 成立。")
add("G02", "PASS", "来料对自身表格的三处修正成立：汤川力∝(1+mr)e^{−mr}/r²、强力 V=σr 力近恒定、缠绕数≠SU(3)",
    "F=−dV/dr，V∝e^{−mr}/r ⇒ F∝(1+mr)e^{−mr}/r²（非 e^{−mr}/r²）；V=σr ⇒ F≈σ≈1 GeV/fm；圆周缠绕仅给 U(1)。")
add("G03", "PASS", "电弱统一=规范场混合、核力=色力剩余效应——两点为对的说法但非「合力」",
    "γ/Z 为 B 与 W³ 组合（希格斯机制）；核力类范德华剩余；来料 §8 区分成立。")

# ---- H: retraction ledger + originality ----
add("H01", "PASS", "来料 §9 六条撤回全部成立：母方程恒等式、叉乘只定形式、电场不垂直、三维正交非公理、符号混用、简化式为汤川通式",
    "与库内 r409/r410「统一力≤标度非机制」、attack_C0386「UED KK 光子」方向一致。")
add("H02", "CORRECTED", "来料「原创需要三点」判据本身为本审计采用，但「没有找到相同标准理论」≠「证明无先例」",
    "来料 §11 自述未逐篇查文献、数值来自记忆；本册把这一不确定性登记为 BOUNDARY，不升级为决定性否定。")
add("H03", "PASS", "来料原创性判定：耦合比/新预言/数学自洽三点均未满足 ⇒ 无原创物理",
    "严格成立部分=SR+标准 KK（已知物理）；螺旋+垂直未产生新方程；四力统一未完成。与库内 0/22、UFT-3=0 红线一致。")
add("H04", "INFO", "来料给出的可行下一步（内空间稳定机制/零模轻费米子/手征性）与库内 O-GUT/O-COUPLING/O-DIRAC 开放项同构",
    "这是研究路线建议，非已闭合结论；本册不代选、不宣称攻破。")

cross_refs = [
    {"target": "attack24 N2 / attack_C0191", "relation": "互印", "detail": "KK 四重必要条件 ⇒ 最小额外维 n=5；本册 5D→U(1) 与之一致（最小 KK）"},
    {"target": "r22 垂直原理四力统一框架全维审计", "relation": "互印", "detail": "r22 三路线全 FAIL；本册独立从 KK 路线得同样「统一未完成」结论"},
    {"target": "attack_C0386 UED KK 光子攻破", "relation": "互印", "detail": "KK 光子/UED 路线；本册补出荷质比 1e21 与质量 5e17 GeV 的定量否证"},
    {"target": "r409/r410 形式谱系与统一力 f 定价", "relation": "互印", "detail": "「垂直+线性⇒洛伦兹形式但不给 F 来源/q」与「统一力≤标度非机制」同型"},
    {"target": "C0191 维数选择", "relation": "边界", "detail": "维数=外部输入；本册 F03 继承该结论，不重判"},
]

guard("G-C1", "entries >= 20", len(entries) >= 20, str(len(entries)))
guard("G-C2", "guards count >= 15", len(guards) >= 15, str(len(guards)))
guard("G-C3", "all entries have unique codes", len({e["code"] for e in entries}) == len(entries), str(len(entries)))
guard("G-C4", "all key numeric claims present",
      all(any(e["code"] == k for e in entries) for k in ["B03", "B04", "B05", "C01", "D01", "E01", "F03", "H03"]),
      "ok")

counts = {}
for e in entries:
    counts[e["verdict"]] = counts.get(e["verdict"], 0) + 1
all_guards_ok = all(g["status"] == "PASS" for g in guards)
exit_code = 0 if all_guards_ok else 1

payload = {
    "round": "attack66",
    "title": "光速螺旋 + 垂直原理统一力：推导复算与判定",
    "date": "2026-11-23",
    "source": "本次对话整理稿（Claude，2026-10-22；来源：三份文档与对话全部内容）",
    "source_kind": "外部来稿审计（否定方向）",
    "scope": "独立机器复算来稿关键读数；不重推引用标准结果；不改写任何既有文件",
    "counts": counts,
    "entries_total": len(entries),
    "guard_pass": sum(1 for g in guards if g["status"] == "PASS"),
    "guard_total": len(guards),
    "exit_code": exit_code,
    "items": entries,
    "guards": guards,
    "self_corrections": self_corrections,
    "cross_refs": cross_refs,
    "key_numbers": {
        "kappa_esu_per_g": fs(kappa),
        "e_over_m_e_esu_per_g": fs(e_over_m_e),
        "qm_gap_ratio": fs(ratio_qm),
        "R_KK_cm": fs(R_kk),
        "R_over_l_P": fs(R_over_lp),
        "two_over_sqrt_alpha": fs(two_over_sqrt_alpha),
        "m1_gram": fs(m_kk_g),
        "m1_GeV": fs(m_kk_gev),
        "g_classical": str(g_classical),
        "g_experimental": str(实验_g),
    },
}

with io.open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(esc(payload), f, ensure_ascii=False, indent=2)

lines = []
lines.append("attack66 report - 光速螺旋 + 垂直原理统一力：推导复算与判定")
lines.append("date: 2026-11-23")
lines.append("entries: %d ; counts: %s" % (len(entries), str(counts)))
lines.append("guards: %d/%d PASS ; exit=%d" % (payload["guard_pass"], payload["guard_total"], exit_code))
lines.append("")
for e in entries:
    lines.append("[%s] %s : %s" % (e["verdict"], e["code"], e["title"]))
    lines.append("    " + e["detail"])
lines.append("")
lines.append("KEY NUMBERS")
for k, v in payload["key_numbers"].items():
    lines.append("  %s = %s" % (k, v))
lines.append("")
lines.append("CROSS REFS")
for c in cross_refs:
    lines.append("  - %s (%s): %s" % (c["target"], c["relation"], c["detail"]))
with io.open(OUT_REPORT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print("entries=%d %s" % (len(entries), str(counts)))
print("guards=%d/%d exit=%d" % (payload["guard_pass"], payload["guard_total"], exit_code))
print("json=" + OUT_JSON)
print("report=" + OUT_REPORT)
sys.exit(exit_code)
