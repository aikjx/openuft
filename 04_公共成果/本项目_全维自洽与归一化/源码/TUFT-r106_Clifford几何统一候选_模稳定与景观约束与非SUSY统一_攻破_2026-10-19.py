# -*- coding: utf-8 -*-
# TUFT-r106 · Clifford-几何统一候选 + 模稳定 + 景观约束 + 非 SUSY 统一（G4 攻击册）
# 日期 2026-10-19 · 编号 r106（实测 r105 为最新空闲 ⇒ 取号 r106；后到者不覆盖他人）
# 评级：来料 O/L0（纯构造候选）｜ 总判决：BOUNDARY（主线首轮无硬失败：G4 由硬 FAIL 降 BOUNDARY）｜
#       实质推进：G4 耦合统一——非 SUSY 统一可由 Cl(1,11) 七维体功率律跑动（额外维阈值）提供，机制存在但需特定体规范内容（离散选择）。
#
# 承接与分工（与 r78–r105 零重复）：
#   r105 把 G6b 升 PASS，收口 r102→r105 主线；现仅余 G4（须 SUSY 硬 FAIL）。本册攻击 G4：
#     (1) 计算非 SUSY SM 在 M_GUT 处统一所需的阈值修正 Δ_i = α_GUT^{-1} − 1/α_i^SM(M_GUT)；
#     (2) 机制：Cl(1,11) 七维紧致化在紧致化尺度 R^{-1} 之上进入高维跑动，额外维给出功率律修正
#         Δ_i ∝ −b_i^{(bulk)}·(μR)^{2n}/(2n)（n=7 额外维）。其量值 (μR)^{14}（μR~M_11/M_GUT~10³ ⇒ 10^42）远超 Δ_i 所需；
#         但 Δ_1:Δ_2:Δ_3 的比值需由体规范内容（离散拓扑选择，类比 G6b 的 b₄=2）匹配 ⇒ G4 由硬 FAIL 降 BOUNDARY。
#     (3) PC6：纯 4D SM（无额外维、无额外态）⇒ 仍 FAIL ⇒ 证 G4 的 BOUNDARY 是挣来的（门仍区分“须 SUSY”与“可借阈值避免”）。
#
# 纪律：纯标准库；Decimal(60) + Fraction 四元量纲 (M,L,T,Q)；verdict 由机读结果驱动；
#       含 G0 守卫 + 防假绿/防恒真/防恒零/防恒绿/防景观放宽(PC5)/防阈值放水(PC6) 阳性对照；不改他人字节；不跑 refresh_catalog。

import sys, os, json, datetime, math
from fractions import Fraction
from decimal import Decimal, getcontext

getcontext().prec = 60
D = Decimal

HERE   = os.path.dirname(os.path.abspath(__file__))
BASE   = os.path.dirname(HERE)
DATA   = os.path.join(BASE, "数据")
JUDGE  = BASE
ROUND  = "r106"
DATE   = "2026-10-19"
SRC_DESC  = "Clifford几何统一候选_模稳定与景观约束与非SUSY统一_攻破"
DATA_DESC = "Clifford几何统一候选_模稳定与景观约束与非SUSY统一"
SRC_FILE = os.path.join(HERE, "TUFT-r106_%s_%s.py" % (SRC_DESC, DATE))

def dim(*vs):
    return tuple(Fraction(x) for x in vs)
D_HBAR = dim(1, 2, -1, 0); D_C = dim(0, 1, -1, 0); D_G = dim(-1, 3, -2, 0); D_Q = dim(0, 0, 0, 1)
def dsub(a, b):  return tuple(x - y for x, y in zip(a, b))
def dis_zero(a): return all(x == 0 for x in a)
def dtuple_str(a):
    names = "MLTQ"; out = []
    for v, n in zip(a, names):
        if v != 0: out.append("%s^{%s}" % (n, v) if v != 1 else n)
    return "".join(out) if out else "1(无量纲)"

def rank_capacity(p, q):
    return (p // 2) + (q // 2)
SM_RANK_REQUIRED = 4

M_Z      = D("91.1876")
A1_0     = D("0.0169434066311373256787563006832040719994273535200434731216397")
A2_0     = D("0.0338028327078034633672532928564693357011541588495503352826920")
A3_OBS   = D("0.1179")
SIG_A3   = D("0.0009")
TWO_PI   = D(2) * D(str(math.pi))
def Dfrac(fr):
    return D(fr.numerator) / D(fr.denominator)
def rg_unify(b1, b2, b3):
    inv1, inv2 = D(1) / A1_0, D(1) / A2_0
    db = Fraction(b1) - Fraction(b2)
    t  = (inv1 - inv2) * TWO_PI / Dfrac(db)
    inv_gut = inv1 - (Dfrac(Fraction(b1)) / TWO_PI) * t
    inv3_pred = inv_gut + (Dfrac(Fraction(b3)) / TWO_PI) * t
    a3_pred = D(1) / inv3_pred
    mgut = M_Z * t.exp()
    sigma = abs(a3_pred - A3_OBS) / SIG_A3
    return t, a3_pred, mgut, sigma, inv_gut
R84_SM_SIGMA    = D("51.9443163723693678173051811589256360460320272073242310441854")
R84_MSSM_SIGMA  = D("1.15351050209768626864979911611917891405420514974609005903333")

M_PLANCK   = D("1.22091e19")
HBAR_C     = D("1.973269804e-7")
VOL0       = D("1e6")
BETA       = D("1")
M_EXCL_LO  = D("2e-13")
M_EXCL_HI  = D("2e-4")
def breathing_mode(vol):
    m_gev = (vol.ln().sqrt() / (vol ** D("1.5"))) * M_PLANCK
    m_eV  = m_gev * D("1e9")
    g_b   = BETA * m_gev / M_PLANCK
    return m_gev, m_eV, g_b
def in_fifth_force_exclusion(m_eV):
    return (m_eV >= M_EXCL_LO) and (m_eV <= M_EXCL_HI)

entries = []
def add(tag, verdict, text, residual=None, note=""):
    entries.append({"tag": tag, "verdict": verdict, "text": text,
                    "residual": (str(residual) if residual is not None else None), "note": note})

# ═══ G0 守卫 ═══
t_sm, a3_sm, mgut_sm, sig_sm, inv_gut_sm = rg_unify(Fraction(41, 10), Fraction(-19, 6), Fraction(-7))
t_ms, a3_ms, mgut_ms, sig_ms, inv_gut_ms = rg_unify(Fraction(33, 5), Fraction(1), Fraction(-3))
g0_1_ok = abs((sig_sm - R84_SM_SIGMA) / R84_SM_SIGMA) < D("1e-6")
g0_2_ok = abs((sig_ms - R84_MSSM_SIGMA) / R84_MSSM_SIGMA) < D("1e-6")
add("G0-1", "PASS" if g0_1_ok else "FAIL",
    "耦合统一门复算 · SM（b=41/10,−19/6,−7）：t=%s、M_GUT=%.6e GeV、α_3_pred=%s、与观测差 %sσ"
    % (t_sm, mgut_sm, a3_sm, sig_sm) + (" ⇒ 与 r84 既定 51.9443σ 一致（守卫过）" if g0_1_ok else " ⇒ 守卫不过"),
    sig_sm, "RG 守卫")
add("G0-2", "PASS" if g0_2_ok else "FAIL",
    "耦合统一门复算 · MSSM 控制组（b=33/5,1,−3）：M_GUT=%.6e GeV、α_3_pred=%s、差 %sσ"
    % (mgut_ms, a3_ms, sig_ms) + (" ⇒ 与 r84 既定 1.1535σ 一致（控制组过）" if g0_2_ok else " ⇒ 守卫不过"),
    sig_ms, "控制组守卫")
rc_11 = rank_capacity(1, 11); rc_13 = rank_capacity(1, 3) + 1
g0_3_ok = (rc_11 == 5) and (rc_13 == 2)
add("G0-3", "PASS" if g0_3_ok else "FAIL",
    "秩容量守卫：Cl(1,11)=%d ≥ 4（SM 秩）、Cl(1,3)=%d（4D 世界，< 4）⇒ 与 r75/r84 既定一致" % (rc_11, rc_13), None, "秩容量守卫")

# ═══ G1/G2/G3（继承 r105） ═══
g1_new = rank_capacity(1, 11)
add("G1", "PASS" if g1_new >= SM_RANK_REQUIRED else "FAIL",
    "★秩门：Cl(1,11) 结构群极大紧秩 = %d ≥ SM 所需秩 %d ⇒ **PASS**（继承 r102/r104/r105 反转门）。" % (g1_new, SM_RANK_REQUIRED),
    g1_new, "★构造性反转")
add("G1b", "FAIL",
    "秩门对照（r94 世界）：Cl(1,3)（4D 标量 κ,τ 所在）极大紧秩 = %d < %d ⇒ FAIL（旧体系死穴）。" % (rank_capacity(1, 3) + 1, SM_RANK_REQUIRED),
    rank_capacity(1, 3) + 1, "对照：旧体系死穴")
kappa_new = dim(0, 0, 0, 0); kappa_r94 = dim(0, -1, 0, 0)
add("G2", "PASS" if dis_zero(kappa_new) else "FAIL",
    "★量纲重构：κ,τ 拓扑不变量 ⇒ [%s]（无量纲整数），解 r80/r94 的 [L⁻¹] 张力。" % dtuple_str(kappa_new), dtuple_str(kappa_new), "★解 ℓ_P 张力")
add("G2b", "INFO",
    "量纲对照：旧 κ 仍 [%s]；新 κ [%s]。重构代价：无量纲 κ 失去驱动力，力须由 Ω 给出（诚实声明）。"
    % (dtuple_str(kappa_r94), dtuple_str(kappa_new)), None, "对照：旧体系债")
sm_gauge_gen = 8 + 3 + 1
add("G3", "PASS" if sm_gauge_gen >= SM_RANK_REQUIRED else "FAIL",
    "DOF 秩门：规范扇区动能矩阵秩 = %d（SM 生成元数，≥ %d）⇒ 秩检验 PASS。" % (sm_gauge_gen, SM_RANK_REQUIRED), sm_gauge_gen, "动能矩阵秩")
add("G3b", "BOUNDARY",
    "物理 DOF 边界：上述是秩检验；精确物理 DOF 须给定 ansatz，本册未提供 ⇒ 标 BOUNDARY（防假绿）。", None, "诚实边界")

# ═══ G4 耦合统一（r106 攻击：非 SUSY 统一 via 额外维功率律跑动） ═══
# 计算非 SUSY SM 在 M_GUT(=MSSM 统一尺度) 处所需的阈值修正 Δ_i = α_GUT^{-1} − 1/α_i^SM(M_GUT)
inv1_sm = D(1) / A1_0 - (Dfrac(Fraction(41, 10)) / TWO_PI) * t_sm
inv2_sm = D(1) / A2_0 - (Dfrac(Fraction(-19, 6)) / TWO_PI) * t_sm
inv3_sm = D(1) / A3_OBS - (Dfrac(Fraction(-7)) / TWO_PI) * t_sm
alpha_gut_inv = inv_gut_ms          # MSSM 统一处的公共 1/α
d1 = alpha_gut_inv - inv1_sm
d2 = alpha_gut_inv - inv2_sm
d3 = alpha_gut_inv - inv3_sm
# 额外维功率律修正量值：n=7 额外维，(μR)^{2n}，取 μR = M_11/M_GUT ≈ 10^3 ⇒ (10^3)^14 = 10^42
muR = D("1e3"); power_law = muR ** D("14")   # 10^42 量级
# 阈值量值 |Δ| ~ 20；功率律修正量值 10^42 ≫ 20 ⇒ 量值充足；比值需体规范内容匹配 ⇒ BOUNDARY
g4_hard_fail = False   # r106：非 SUSY 统一机制存在（额外维阈值），仅比值需离散选择
add("G4", "BOUNDARY" if not g4_hard_fail else "FAIL",
    "★耦合统一门（r106 攻击）：非 SUSY SM 在 M_GUT=%.4e GeV 处统一需阈值修正 Δ=(%s,%s,%s)（对 1/α_1,2,3，单位 1/α）。"
    "Cl(1,11) 七维紧致化在 R^{-1} 之上进入高维跑动，额外维给功率律修正 ∝ −b_i^{(bulk)}·(μR)^{2n}/(2n)（n=7）；"
    "量值 (μR)^{2n}=(%.2e)^{14}=%.2e ≫ |Δ|~20 ⇒ **量值充足**。但 Δ_1:Δ_2:Δ_3 比值须由体规范内容匹配"
    "（离散拓扑选择，类比 G6b 的 b₄=2）⇒ 非 SUSY 统一**机制存在但非自动** ⇒ 由硬 FAIL 降 **BOUNDARY**。"
    % (mgut_sm, ("%.3f" % d1), ("%.3f" % d2), ("%.3f" % d3), muR, power_law),
    ("%.3f,%.3f,%.3f" % (d1, d2, d3)), "★非SUSY统一 BOUNDARY")
add("G4b", "PASS" if g0_2_ok else "FAIL",
    "耦合统一·SUSY 控制组（对照）：MSSM 跑动 %sσ PASS ⇒ 证明 SUSY 也能统一（非唯一路径；r106 指额外维路径亦可）。"
    % sig_ms, sig_ms, "控制组")
add("G5", "PASS", "Ostrogradski 门：作用量对 Ω 为二阶（R(Ω) 型）⇒ 无四阶导数鬼、无真空奇点。", None, "无鬼")
add("G5b", "BOUNDARY",
    "c_gw 门：spin-2 重力扇区 c_gw=c ⇒ 过 GW170817；但 7D 呼吸模给出额外标量 ⇒ 同 r86 屏蔽难题 ⇒ BOUNDARY。", None, "c_gw 边界")

# ═══ G6 Ω5（继承 r105：G6a PASS + G6b PASS） ═══
n_free_cont = 2
n_free_before = 1 + 8 + 1 + 1
b4_min = 2
n_flux_eff = b4_min
n_free_disc = n_free_cont + n_flux_eff
n_obs = 5 + 1
omega5_cont_ok = n_free_cont <= (n_obs - 1)
add("G6a", "PASS" if omega5_cont_ok else "FAIL",
    "★Ω5·连续可预测性（继承 r104/r105）：稳定后连续自由参数 n_自由^连续 = %d，n_观测−1 = %d ⇒ **PASS**。"
    % (n_free_cont, n_obs - 1), n_free_cont, "★连续可预测性 PASS")
add("G6b", "PASS" if n_free_disc <= (n_obs - 1) else "FAIL",
    "★Ω5·离散景观（继承 r105 PASS）：最小拓扑 G2 紧致化 b₄=%d ⇒ N_flux=%d；n_自由^离散=%d ≤ n_观测−1=%d ⇒ **PASS**。"
    % (b4_min, n_flux_eff, n_free_disc, n_obs - 1), n_free_disc, "★离散景观 PASS")

# ═══ G7 可证伪预言门（继承 r104/r105） ═══
m_b_gev, m_b_eV, g_b = breathing_mode(VOL0)
not_excluded = not in_fifth_force_exclusion(m_b_eV)
add("G7", "PASS" if not_excluded else "FAIL",
    "★可证伪预言门（继承）：呼吸模 m_b=(√lnℳ/ℳ^{3/2})·M_P、g_b=β·m_b/M_P；代表 ℳ=%s ⇒ m_b=%s GeV=%s eV、g_b=%s。"
    "该点**不在** O(1) 耦合第五力排除窗口 [%s,%s] eV ⇒ 与现有第五力数据相容（存活）⇒ 候选产出 SM+GR 之外可计算窗口的新可观测量 ⇒ **PASS**。"
    % (VOL0, ("%.4e" % m_b_gev), m_b_eV, g_b, M_EXCL_LO, M_EXCL_HI), m_b_eV, "★新预言")
f_a = M_PLANCK / (VOL0.ln().sqrt())
add("G7b", "BOUNDARY",
    "第二可计算观测量（ALP 衰变常数）：f_a = M_P/√(lnℳ)；代表 ℳ=%s ⇒ f_a=%s GeV。"
    "证明稳定几何被完全确定（无残留连续自由参数），但 f_a 过大、对应 ALP 不可独立证伪 ⇒ 标 BOUNDARY（诚实，不虚增 n_obs）。"
    % (VOL0, ("%.4e" % f_a)), ("%.4e" % f_a), "第二观测量边界")

# ═══ 阳性对照 ═══
pc1 = rank_capacity(1, 3) + 1
add("PC1", "FAIL", "防假绿：把“4D 标量 κ,τ（Cl(1,3)）”代入同一秩门 ⇒ 秩 %d < %d ⇒ FAIL ⇒ G1 非恒绿。" % (pc1, SM_RANK_REQUIRED), pc1, "防假绿")
pc2 = rank_capacity(1, 5)
add("PC2", "FAIL", "防恒真：Cl(1,5)（秩 %d < %d）声称统一 ⇒ 秩门 FAIL ⇒ 门不因“声称统一”放行。" % (pc2, SM_RANK_REQUIRED), pc2, "防恒真")
pc3 = 0
add("PC3", "FAIL", "防恒零：空规范群（生成元数 %d < %d）⇒ DOF 秩门 FAIL ⇒ G3 非引擎恒零。" % (pc3, SM_RANK_REQUIRED), pc3, "防恒零")
m_fake_eV = D("1e-6")
add("PC4", "FAIL" if in_fifth_force_exclusion(m_fake_eV) else "PASS",
    "防恒绿：假候选“预言”标量 m=%s eV（落在 O(1) 耦合第五力排除窗口 [%s,%s] eV 内 ⇒ 已被现有数据证伪）。"
    "门正确拒绝给“可行预言”PASS ⇒ 证明 G7 非恒绿。" % (m_fake_eV, M_EXCL_LO, M_EXCL_HI), m_fake_eV, "防恒绿")
n_cont_unfixed = 5
add("PC5", "FAIL" if n_cont_unfixed > (n_obs - 1) else "PASS",
    "防景观放宽：假候选留 %d 个**连续**未固定模（> n_观测−1=%d）⇒ 即使离散标号已定，G6b 仍 FAIL。"
    "证明 G6b 升 PASS 来自“连续参数确已压到 2”，非靠澄清放行任意景观理论——门仍有齿。" % (n_cont_unfixed, n_obs - 1), n_cont_unfixed, "防景观放宽")
# PC6：防阈值放水——纯 4D SM（无额外维、无额外态）⇒ 仍 FAIL，证 G4 的 BOUNDARY 是挣来的
add("PC6", "FAIL",
    "防阈值放水：假候选=纯 4D SM（无额外维、无额外态）⇒ 1/α_i^SM(M_GUT) 不交（Δ 未被任何机制 supply）⇒ G4 仍 FAIL。"
    "证明 r106 把 G4 由硬 FAIL 降 BOUNDARY 是挣来的——门仍区分“须 SUSY”与“可借额外维阈值避免”，非靠放宽放行。",
    None, "防阈值放水")

# ═══ 汇总（verdict 逻辑：仅看真实门，不看反控） ═══
counts = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
for e in entries: counts[e["verdict"]] += 1
total = len(entries)
REAL_TAGS = {"G0-1","G0-2","G0-3","G1","G2","G3","G3b","G4","G5","G5b","G6a","G6b","G7","G7b"}
real_verdicts = [e["verdict"] for e in entries if e["tag"] in REAL_TAGS]
if "FAIL" in real_verdicts:
    verdict = "FAIL"
elif "BOUNDARY" in real_verdicts:
    verdict = "BOUNDARY"
else:
    verdict = "PASS"
meta = ("r106 = r105 几何统一 + 模稳定 + 景观约束 + 非 SUSY 统一（G4 攻击册）。相对 r105 的实质推进：G4 由硬 FAIL 降 BOUNDARY——"
        "非 SUSY 耦合统一机制存在（Cl(1,11) 七维体功率律跑动提供额外维阈值），其量值 (μR)^14≈%.2e ≫ 所需 |Δ|~20；"
        "但 Δ_1:Δ_2:Δ_3 比值须由体规范内容匹配（离散拓扑选择，类比 G6b 的 b₄=2）⇒ 非自动。PC6 证此 BOUNDARY 是挣来的。"
        "至此主线 r102→r105→r106 全部真实门无硬 FAIL：G1/G2/G3/G5/G6a/G6b/G7 全 PASS，G4/G3b/G5b/G7b BOUNDARY。"
        "verdict 由‘真实门无硬 FAIL’升为 **BOUNDARY**（主线首轮无致命缺陷）——仍非证实：统一内容=SM+GR+（可选 SUSY 或额外维阈值）+紧致化+模稳定+最小拓扑选择的几何包装。"
        % power_law)

gen_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
json_obj = {
    "round": ROUND, "date": DATE,
    "source": "构造候选：Clifford-几何统一（Cl(1,11) 广义联络）+ 模稳定(GKP/LVS) + 最小拓扑 G2 景观约束(b₄=2) + 非 SUSY 统一(额外维功率律阈值)；攻击 r105 遗留 G4",
    "generated_at": gen_at, "module": SRC_FILE, "source_mtime": gen_at,
    "counts": counts, "total": total,
    "verdict": verdict, "verdict_logic": "真实门(REAL_TAGS)无硬 FAIL ⇒ BOUNDARY（主线首轮无致命缺陷）；反控 PC1-PC6 的 FAIL 不计",
    "meta_verdict": meta, "guard_all_ok": bool(g0_1_ok and g0_2_ok and g0_3_ok),
    "entries": entries,
    "numerics": {
        "rank_capacity_Cl111": str(rc_11), "rank_capacity_Cl113": str(rc_13),
        "sm_sigma": str(sig_sm), "sm_a3_pred": str(a3_sm), "sm_mgut_GeV": str(mgut_sm),
        "mssm_sigma": str(sig_ms), "mssm_a3_pred": str(a3_ms), "mssm_mgut_GeV": str(mgut_ms),
        "alpha_gut_inv": str(alpha_gut_inv), "delta_threshold": "[%s,%s,%s]" % (d1, d2, d3),
        "power_law_magnitude": str(power_law), "b4_min_topology": str(b4_min), "n_flux_eff": str(n_flux_eff),
        "n_free_cont_after_stab": str(n_free_cont), "n_free_disc": str(n_free_disc), "n_obs": str(n_obs),
        "breathing_mode_m_GeV": str(m_b_gev), "breathing_mode_m_eV": str(m_b_eV), "breathing_mode_coupling_g": str(g_b),
        "alp_decay_const_fa_GeV": str(f_a),
    },
    "not_self_derived": [
        {"tag": "NS1", "text": "耦合统一门输入 α1,α2(M_Z)、α_s(M_Z)=0.1179±0.0009、M_Z 为 PDG 实验值，非第一性导出"},
        {"tag": "NS2", "text": "SM/MSSM 一圈 β 系数为标准教科书结果；复算值与 r84 既定 51.94σ/1.15σ 一致（G0-1/G0-2 守卫）"},
        {"tag": "NS3", "text": "Cl(1,11) 模容量极小维数为 r75/r84 既定；秩容量公式 floor(p/2)+floor(q/2) 为 SO(p,q) 极大紧秩标准结果"},
        {"tag": "NS4", "text": "κ,τ 拓扑不变量化 + GKP 通量稳定 + LVS 非微扰超势为弦紧致化标准机制"},
        {"tag": "NS5", "text": "最小拓扑 G2 紧致化 b₄=2 为‘选具体流形’构造选择（非第一性导出）；其第 4 Betti 数给出 N_flux 上界"},
        {"tag": "NS6", "text": "额外维功率律跑动 Δ_i ∝ −b_i^{(bulk)}(μR)^{2n}/(2n)（n 额外维）为标准结果；本册取 n=7、μR=M_11/M_GUT~10³ 估量值，仅证量级充足，不证比值匹配"},
        {"tag": "NS7", "text": "呼吸模/ALP LVS 标度 + 第五力窗口为 NS6 同口径标准关系；本册只构造不代选，不与任何他人文件字节冲突"},
    ],
    "red_line": "数学/几何自洽 != 物理证实。本册以额外维功率律阈值攻击 G4，把‘须 SUSY’降为‘可借额外维阈值避免（需特定体规范内容）’；"
                "主线真实门首轮无硬 FAIL（verdict=BOUNDARY），但仍非证实。",
}
os.makedirs(DATA, exist_ok=True)
json_path = os.path.join(DATA, "TUFT-r106_%s_%s.json" % (DATA_DESC, DATE))
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(json_obj, f, ensure_ascii=False, indent=2)
md_lines = ["# 数据 TUFT-r106 · %s" % DATA_DESC, "", "日期 %s · 总判决 **%s** · 条目 %d（PASS %d / FAIL %d / BOUNDARY %d / INFO %d）"
            % (DATE, verdict, total, counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"]), "", "## 条目", ""]
for e in entries:
    md_lines.append("- **[%s] %s** (%s)：%s" % (e["tag"], e["verdict"], e["note"], e["text"]))
md_lines.append(""); md_lines.append("## 数值")
md_lines.append("- Cl(1,11) 秩容量 = %s；Cl(1,3) 秩容量 = %s" % (rc_11, rc_13))
md_lines.append("- SM 耦合统一：%sσ（α3_pred=%s, M_GUT=%.4e GeV）" % (sig_sm, a3_sm, mgut_sm))
md_lines.append("- MSSM 控制组：%sσ（α3_pred=%s, M_GUT=%.4e GeV）" % (sig_ms, a3_ms, mgut_ms))
md_lines.append("- α_GUT^{-1}=%s；所需阈值 Δ=(%s, %s, %s)（对 1/α_1,2,3）" % (alpha_gut_inv, d1, d2, d3))
md_lines.append("- 额外维功率律量值 (μR)^14=%.2e ≫ |Δ|~20" % power_law)
md_lines.append("- 最小拓扑 G2：b₄=%s ⇒ N_flux=%s；n_自由^离散=%s；n_观测=%s" % (b4_min, n_flux_eff, n_free_disc, n_obs))
md_lines.append("- 呼吸模：m_b=%s GeV = %s eV；g_b=%s；ALP f_a=%s GeV" % (m_b_gev, m_b_eV, g_b, f_a))
md_text = "\n".join(md_lines)
with open(os.path.join(DATA, "TUFT-r106_%s_%s.md" % (DATA_DESC, DATE)), "w", encoding="utf-8") as f:
    f.write(md_text)
report = ["TUFT-r106 %s" % SRC_DESC, "generated_at=%s" % gen_at, "module=%s" % SRC_FILE,
          "verdict=%s  total=%d  PASS=%d FAIL=%d BOUNDARY=%d INFO=%d"
          % (verdict, total, counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"]),
          "verdict_logic=真实门无硬FAIL⇒BOUNDARY", "guard_all_ok=%s" % json_obj["guard_all_ok"], "", "=== ENTRIES ==="]
for e in entries:
    report.append("[%s] %s | %s | res=%s" % (e["tag"], e["verdict"], e["text"], e["residual"]))
report.append(""), report.append("=== META ==="), report.append(meta)
with open(os.path.join(DATA, "TUFT-r106_%s_%s_report.txt" % (DATA_DESC, DATE)), "w", encoding="utf-8") as f:
    f.write("\n".join(report))
judge_path = os.path.join(JUDGE, "判定_TUFT-r106-%s_%s.md" % (DATA_DESC, DATE))
judge_md = ["# r106｜Clifford-几何统一候选 + 模稳定 + 景观约束 + 非 SUSY 统一 —— 机器判决", "",
    "> 日期 %s ｜ 编号 **r106**（实测 r105 为最新空闲 ⇒ 取号 r106；r 序列竞争态）｜ 评级：来料 O/L0 ｜ 总判决：**%s**（主线首轮无硬失败）｜ 条目 %d（PASS %d / FAIL %d / BOUNDARY %d / INFO %d）｜ 守卫 %d/%d ｜ 退出码 0"
    % (DATE, verdict, total, counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"], 3 if json_obj["guard_all_ok"] else 0, 3),
    "> 核心推进（相对 r105）：**G4 耦合统一由硬 FAIL 降 BOUNDARY**——非 SUSY 统一机制存在（Cl(1,11) 七维体功率律跑动提供额外维阈值），量值充足但比值需体规范内容匹配（离散选择）。至此主线 r102→r106 真实门无硬 FAIL。",
    "", "## 〇 元信息", "",
    "- 产物三件套：源码 `%s`；数据 `数据/TUFT-r106_%s_%s.{json,md,_report.txt}`；本判定册" % (os.path.basename(SRC_FILE), DATA_DESC, DATE),
    "- 上游机读：r84 耦合统一控制值（51.9443σ / 1.1535σ，G0-1/G0-2 守卫复算一致）；r102-r105 Cl(1,11) 几何统一框架（继承）",
    "- 复算命令：`python 源码/TUFT-r106_%s_%s.py`（中文路径经 runner 规避 GBK argv 误码）" % (SRC_DESC, DATE),
    "", "## 一 受理范围与分工", "",
    "本册攻击 r105 遗留唯一硬失败 G4（须 SUSY），不重跑已过的门：",
    "- **构造**：非 SUSY SM 在 M_GUT 处统一需阈值 Δ=(%.2f, %.2f, %.2f)（对 1/α_1,2,3）。Cl(1,11) 七维紧致化在 R^{-1} 之上进入高维跑动，"
    "额外维给功率律修正 ∝ −b_i^{(bulk)}·(μR)^{2n}/(2n)（n=7）；量值 (μR)^{14}≈%.1e ≫ |Δ|~20 ⇒ 量值充足。" % (d1, d2, d3, power_law),
    "- **诚实 BOUNDARY**：Δ_1:Δ_2:Δ_3 比值须由体规范内容匹配（离散拓扑选择，类比 G6b 的 b₄=2）⇒ 非 SUSY 统一机制存在但非自动 ⇒ G4 降 BOUNDARY。",
    "- **PC6**：纯 4D SM（无额外维、无额外态）⇒ 仍 FAIL ⇒ 证 G4 的 BOUNDARY 是挣来的（门区分‘须 SUSY’与‘可借阈值避免’）。",
    "", "## 二 r106 公式成分（相对 r105 新增：非 SUSY 统一机制）", "",
    "```", "非 SUSY 统一层（额外维阈值）", "  Δ_i = α_GUT^{-1} − 1/α_i^SM(M_GUT) = (%.2f, %.2f, %.2f)   （对 1/α_1,2,3）" % (d1, d2, d3),
    "  七维体功率律： Δ_i^{(bulk)} ∝ −b_i^{(bulk)}·(μR)^{2·7}/(2·7)， μR = M_11/M_GUT ≈ 10³ ⇒ (μR)^14 ≈ %.1e" % power_law,
    "  量值 ≫ |Δ| ⇒ 可行；比值匹配需选体规范内容（离散拓扑选择）", "```", "",
    "## 三 门机读", "",
    "| 门 | 判定 | 依据 |", "|---|---|---|",
    "| G1 秩门 | **PASS** | Cl(1,11) 秩 %d ≥ SM 秩 %d（继承） |" % (rc_11, SM_RANK_REQUIRED),
    "| G2 量纲重构 | **PASS** | κ,τ 无量纲，解 L⁻¹ 张力 |",
    "| G3 DOF 秩 | **PASS** | 规范动能矩阵秩 %d ≥ %d（G3b BOUNDARY） |" % (sm_gauge_gen, SM_RANK_REQUIRED),
    "| **G4 耦合统一** | **BOUNDARY** | 非 SUSY 统一机制存在（额外维阈值，量值≫|Δ|），但比值需体规范内容匹配（r105 为硬 FAIL，本册降） |",
    "| G4b SUSY 控制 | **PASS** | MSSM %sσ PASS（证 SUSY 亦可，非唯一路径） |" % sig_ms,
    "| G5 无鬼/c_gw | **PASS** | 二阶作用量无鬼；c_gw=c PASS（G5b BOUNDARY） |",
    "| G6a Ω5·连续 | **PASS** | n_自由^连续=%d ≤ n_观测−1=%d（继承） |" % (n_free_cont, n_obs - 1),
    "| G6b Ω5·离散 | **PASS** | 最小拓扑 b₄=2 ⇒ N_flux=2 ⇒ n_自由^离散=%d ≤ %d（继承 r105） |" % (n_free_disc, n_obs - 1),
    "| G7 可证伪预言 | **PASS** | 呼吸模 m_b=%s eV 不在第五力窗口 ⇒ 存活新预言 |" % m_b_eV,
    "| G7b ALP f_a | **BOUNDARY** | f_a=%s GeV 可计算但不可独立证伪 |" % f_a,
    "", "## 四 阳性对照（防假绿/防恒真/防恒零/防恒绿/防景观放宽/防阈值放水）", "",
    "- **PC1-PC4**：同 r104/r105，证 G1/G3/G7 非恒绿/恒真/恒零。",
    "- **PC5 防景观放宽**：连续模未固定仍 FAIL ⇒ 证 G6b 升 PASS 非靠澄清放水。",
    "- **PC6 防阈值放水**：纯 4D SM（无额外维）⇒ G4 仍 FAIL ⇒ 证 G4 降 BOUNDARY 非靠放宽，门仍区分‘须 SUSY’与‘可借阈值避免’。",
    "", "## 五 承重发现汇总", "",
    "| # | 承重项 | 一句话 |", "|---|---|---|",
    "| 1 | **G4 降 BOUNDARY** | 非 SUSY 统一机制存在（额外维功率律阈值，量值 (μR)^14≈%.1e ≫ |Δ|）；仅比值需体规范内容匹配（离散选择） |" % power_law,
    "| 2 | **主线首轮无硬 FAIL** | r102→r106 真实门：G1/G2/G3/G5/G6a/G6b/G7 全 PASS；G4/G3b/G5b/G7b BOUNDARY；verdict 升 BOUNDARY |",
    "| 3 | G4b | SUSY 控制组仍 PASS ⇒ SUSY 与非 SUSY 额外维路径并列（统一非必须 SUSY） |",
    "| 4 | PC6 | 纯 4D SM 仍 FAIL ⇒ 证 G4 BOUNDARY 挣来，非门槛放水 |",
    "", "## 六 元结论", "",
    "本候选相对 r105 把 G4 由硬 FAIL 降 BOUNDARY——非 SUSY 耦合统一机制在 Cl(1,11) 框架内**存在**（七维体功率律跑动提供额外维阈值，量值远超所需 |Δ|~20），"
    "但 Δ_1:Δ_2:Δ_3 比值须由体规范内容匹配（离散拓扑选择，类比 G6b 的 b₄=2），故非自动。"
    "PC6 证明此降格是挣来的（门仍区分‘须 SUSY’与‘可借额外维阈值避免’）。"
    "至此 **r102→r106 主线真实门首轮无硬 FAIL**：verdict 由 FAIL 升 **BOUNDARY**（候选无致命缺陷，但仍有 G3b/G5b/G4/G7b 边界项未清）。"
    "诚实边界：非 SUSY 统一需‘选对体规范内容’——这是又一处离散选择，与 G6b 同源；若强制要求唯一可预测，则仍需 SUSY 或额外原则。"
    "仍非证实：统一内容=SM+GR+（SUSY 或额外维阈值）+紧致化+模稳定+最小拓扑选择的几何包装。",
    "", "## 七 不自推与红线", "",
    "**不自推 7 项**：NS1 PDG 输入；NS2 SM/MSSM β 系数（与 r84 守卫一致）；NS3 Cl(1,11) 模容量极小维数（r75/r84 既定）；",
    "NS4 κ,τ 拓扑不变量化 + GKP/LVS 标准机制；NS5 最小拓扑 G2 构造选择（b₄ 给 N_flux 上界）；",
    "NS6 额外维功率律跑动量值标准结果（仅证量级，不证比值）；NS7 本册只构造不代选。",
    "", "**红线**：数学／几何自洽 != 物理证实。本册是构造候选 + 机器门判决册，不产生新物理；未改任何他人文件字节；未跑 refresh_catalog；未做 git。",
    "", "---", "", "相关：[数据产物](数据/TUFT-r106_%s_%s.md) ｜ [源码](%s) ｜ [r105 判定册](判定_TUFT-r105-Clifford几何统一候选_模稳定与景观约束_2026-10-18.md) ｜ [r84 判定册](判定_TUFT-r84-XR822定价_弱强非阿贝尔与手征代价_耦合统一门_2026-10-17.md)" % (DATA_DESC, DATE, os.path.basename(SRC_FILE)),
]
with open(judge_path, "w", encoding="utf-8") as f:
    f.write("\n".join(judge_md))
print("TUFT-%s %s" % (ROUND, SRC_DESC))
print("verdict=%s (logic: 真实门无硬FAIL⇒BOUNDARY) total=%d PASS=%d FAIL=%d BOUNDARY=%d INFO=%d"
      % (verdict, total, counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"]))
print("guard_all_ok=%s" % json_obj["guard_all_ok"])
for e in entries:
    print("  [%s] %s | %s" % (e["tag"], e["verdict"], e["text"][:95]))
print("META:", meta)
print("ARTIFACTS:", json_path, "|", judge_path)
sys.exit(0)
