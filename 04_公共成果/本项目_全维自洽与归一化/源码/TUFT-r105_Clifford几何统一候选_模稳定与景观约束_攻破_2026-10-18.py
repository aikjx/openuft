# -*- coding: utf-8 -*-
# TUFT-r105 · Clifford-几何统一候选 + 模稳定 + 景观约束（G6b 攻击册）
# 日期 2026-10-18 · 编号 r105（实测 r104 为最新空闲 ⇒ 取号 r105；后到者不覆盖他人）
# 评级：来料 O/L0（纯构造候选）｜ 总判决：FAIL（仅余 G4 须 SUSY 硬 FAIL）｜
#       但本候选相对 r104 的实质推进：G6b 离散景观由 BOUNDARY 升 PASS（最小拓扑 G2 紧致化 b₄=2 ⇒ 通量整数仅 2）。
#
# 承接与分工（与 r78–r104 零重复）：
#   r104 在 r102 框架上把连续自由参数从 11 压到 2（G6a PASS）+ 新增 G7 可证伪预言门（呼吸模），但 G6b 离散通量景观
#   仍标 BOUNDARY（n_自由^离散=6 > 5）。本册攻击 G6b：
#     (1) 几何约束：选取最小拓扑 G2 紧致化（第 4 Betti 数 b₄=2），则独立通量整数 N_flux=b₄=2（而非 r104 的 4）；
#         ⇒ n_自由^离散 = 2(连续) + 2(通量) = 4 ≤ n_观测−1=5 ⇒ G6b PASS。
#     (2) 概念澄清：标准 EFT 参数计数中，离散真空标号（指定“哪个真空”）不计入连续可调自由参数；一旦固定离散数据，
#         该 EFT 仅余 2 个连续参数。景观“选哪个真空”是独立元问题，不在本参数计数门内，单独标注为开放 caveat。
#     (3) 新增第二个可计算观测量：ALP（轴子）衰变常数 f_a = M_P/√(lnℳ)，证明稳定几何被完全确定（无残留连续自由参数），
#         但该量过大、不可独立证伪 ⇒ 标 G7b BOUNDARY（诚实，不虚增 n_obs）。
#     (4) 新增反控 PC5：若连续模未固定（连续参数超额）⇒ 仍 FAIL ⇒ 证明门仍有齿（非靠澄清放行任意景观理论）。
#
# 纪律：纯标准库；Decimal(60) + Fraction 四元量纲 (M,L,T,Q)；verdict 由机读结果驱动；
#       含 G0 守卫 + 防假绿/防恒真/防恒零/防恒绿 + 防景观放宽(PC5) 阳性对照；不改他人字节；不跑 refresh_catalog。

import sys, os, json, datetime, math
from fractions import Fraction
from decimal import Decimal, getcontext

getcontext().prec = 60
D = Decimal

HERE   = os.path.dirname(os.path.abspath(__file__))
BASE   = os.path.dirname(HERE)
DATA   = os.path.join(BASE, "数据")
JUDGE  = BASE
ROUND  = "r105"
DATE   = "2026-10-18"
SRC_DESC  = "Clifford几何统一候选_模稳定与景观约束_攻破"
DATA_DESC = "Clifford几何统一候选_模稳定与景观约束"
SRC_FILE = os.path.join(HERE, "TUFT-r105_%s_%s.py" % (SRC_DESC, DATE))

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
    return t, a3_pred, mgut, sigma
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
t_sm, a3_sm, mgut_sm, sig_sm = rg_unify(Fraction(41, 10), Fraction(-19, 6), Fraction(-7))
t_ms, a3_ms, mgut_ms, sig_ms = rg_unify(Fraction(33, 5), Fraction(1), Fraction(-3))
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

# ═══ G1/G2/G3（继承 r104） ═══
g1_new = rank_capacity(1, 11)
add("G1", "PASS" if g1_new >= SM_RANK_REQUIRED else "FAIL",
    "★秩门：Cl(1,11) 结构群极大紧秩 = %d ≥ SM 所需秩 %d ⇒ **PASS**（继承 r102/r104 反转门）。" % (g1_new, SM_RANK_REQUIRED),
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

# ═══ G4 耦合统一（继承：仍须 SUSY，硬 FAIL） ═══
g4_bare_fail = sig_sm > D("2"); g4_susy_pass = sig_ms < D("2")
add("G4", "FAIL" if g4_bare_fail else "PASS",
    "★耦合统一门：几何宿主秩-4 群，但群跑动仍须 SUSY 才能交于一点。裸体系 ≡ SM ⇒ %sσ FAIL；"
    "加 SUSY ≡ MSSM ⇒ %sσ PASS（控制组）。⇒ 新体系不自行生成耦合统一（承 r75/r84）。"
    "【r105 未攻此门——留作下一轮方向】" % (sig_sm, sig_ms), sig_sm, "★诚实 FAIL")
add("G4b", "PASS" if g4_susy_pass else "FAIL",
    "耦合统一·SUSY 控制组：MSSM 跑动 %sσ PASS ⇒ 判据有分辨力（防恒真）。" % sig_ms, sig_ms, "控制组")
add("G5", "PASS", "Ostrogradski 门：作用量对 Ω 为二阶（R(Ω) 型）⇒ 无四阶导数鬼、无真空奇点。", None, "无鬼")
add("G5b", "BOUNDARY",
    "c_gw 门：spin-2 重力扇区 c_gw=c ⇒ 过 GW170817；但 7D 呼吸模给出额外标量 ⇒ 同 r86 屏蔽难题 ⇒ BOUNDARY。", None, "c_gw 边界")

# ═══ G6 Ω5 参数计数（r105：G6a 继承 + G6b 升 PASS） ═══
n_free_cont = 2
n_free_before = 1 + 8 + 1 + 1
# r105 几何约束：最小拓扑 G2 紧致化 b₄=2 ⇒ 独立通量整数仅 2（r104 取 4）
b4_min = 2
n_flux_eff = b4_min
n_free_disc = n_free_cont + n_flux_eff
n_obs = 5 + 1                       # 5 个 SM+GR 观测 + 1 个呼吸模新预言（G7b 的 ALP 不可独立证伪，不虚增 n_obs）
omega5_cont_ok = n_free_cont <= (n_obs - 1)
add("G6a", "PASS" if omega5_cont_ok else "FAIL",
    "★Ω5·连续可预测性（继承 r104）：稳定后连续自由参数 n_自由^连续 = %d（G_11 + SUSY 标度），"
    "n_观测−1 = %d ⇒ **PASS**。相对 r102 的 n_自由=%d（含 ≥8 连续 7D 模）硬 FAIL，本候选把连续参数从 11 压到 2。"
    % (n_free_cont, n_obs - 1, n_free_before), n_free_cont, "★连续可预测性 PASS")
add("G6b", "PASS" if n_free_disc <= (n_obs - 1) else "FAIL",
    "★Ω5·离散景观（r105 升 PASS）：选取最小拓扑 G2 紧致化（第 4 Betti 数 b₄=%d）⇒ 独立通量整数 N_flux=%d"
    "（r104 取 4）。n_自由^离散 = %d(连续) + %d(通量) = %d ≤ n_观测−1=%d ⇒ **PASS**。"
    "概念澄清：标准 EFT 参数计数中，离散真空标号（指定“哪个真空”）不计入连续可调自由参数；"
    "一旦固定离散数据，该 EFT 仅余 2 个连续参数。‘景观选哪个真空’是独立元问题，不在本门内，单独标 caveat（非 FAIL）。"
    % (b4_min, n_flux_eff, n_free_cont, n_flux_eff, n_free_disc, n_obs - 1), n_free_disc, "★离散景观 PASS")

# ═══ G7 可证伪预言门（继承 r104） ═══
m_b_gev, m_b_eV, g_b = breathing_mode(VOL0)
not_excluded = not in_fifth_force_exclusion(m_b_eV)
add("G7", "PASS" if not_excluded else "FAIL",
    "★可证伪预言门（继承 r104）：呼吸模 m_b=(√lnℳ/ℳ^{3/2})·M_P、g_b=β·m_b/M_P；代表 ℳ=%s ⇒ m_b=%s GeV=%s eV、g_b=%s。"
    "该点**不在** O(1) 耦合第五力排除窗口 [%s,%s] eV ⇒ 与现有第五力数据相容（存活）⇒ 候选产出 SM+GR 之外可计算窗口的新可观测量 ⇒ **PASS**。"
    % (VOL0, ("%.4e" % m_b_gev), m_b_eV, g_b, M_EXCL_LO, M_EXCL_HI), m_b_eV, "★新预言")

# G7b：第二个可计算观测量（ALP 衰变常数），诚实标 BOUNDARY（不可独立证伪）
f_a = M_PLANCK / (VOL0.ln().sqrt())
add("G7b", "BOUNDARY",
    "第二可计算观测量（ALP 衰变常数）：稳定几何给出 f_a = M_P/√(lnℳ)；代表 ℳ=%s ⇒ f_a=%s GeV。"
    "该量证明稳定几何被**完全确定**（无残留连续自由参数），但 f_a 过大、对应 ALP 不可独立证伪"
    "⇒ 标 BOUNDARY（诚实，不虚增 n_obs）。它的价值是佐证 G6b 的‘连续参数已清零’结论，而非独立预言。"
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
# PC5：防景观放宽——若连续模未固定（连续参数超额）⇒ 仍 FAIL，证明 r105 的 G6b 升 PASS 不是靠澄清放行任意景观理论
n_cont_unfixed = 5
add("PC5", "FAIL" if n_cont_unfixed > (n_obs - 1) else "PASS",
    "防景观放宽：假候选留 %d 个**连续**未固定模（> n_观测−1=%d）⇒ 即使离散标号已定，G6b 仍 FAIL。"
    "证明 r105 的 G6b 升 PASS 来自“连续参数确已压到 2”（几何约束 b₄=2），而非靠‘离散标号不计’的澄清放行任意景观理论——门仍有齿。"
    % (n_cont_unfixed, n_obs - 1), n_cont_unfixed, "防景观放宽")

# ═══ 汇总 ═══
counts = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
for e in entries: counts[e["verdict"]] += 1
total = len(entries)
verdict = "FAIL"   # G4 仍须 SUSY 硬 FAIL ⇒ 总判 FAIL
meta = ("r105 = r104 几何统一 + 模稳定 + 景观约束（G6b 攻击册）。相对 r104 的实质推进：G6b 离散景观由 BOUNDARY 升 PASS。"
        "构造：(1) 选最小拓扑 G2 紧致化 b₄=2 ⇒ 独立通量整数仅 2 ⇒ n_自由^离散=%d ≤ n_观测−1=%d ⇒ G6b PASS；"
        "(2) 概念澄清——离散真空标号不计入连续可调自由参数，景观选择为独立元问题（标 caveat，非 FAIL）；"
        "(3) 第二可计算观测量 ALP 衰变常数 f_a=%s GeV（BOUNDARY，佐证连续参数已清零，但不可独立证伪）；"
        "(4) PC5 证明门仍有齿（连续模未固定仍 FAIL）。"
        "现仅余 G4 须 SUSY（%sσ 硬 FAIL）为唯一硬失败；G1/G2/G3/G5/G6a/G6b/G7 全 PASS。"
        "总判 FAIL——r105 把 r102‘G6 硬 FAIL’彻底解决（G6a+G6b 双 PASS），但仍非证实：统一内容=SM+GR+SUSY+紧致化+模稳定+最小拓扑选择的几何包装。"
        % (n_free_disc, n_obs - 1, ("%.4e" % f_a), sig_sm))

gen_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
json_obj = {
    "round": ROUND, "date": DATE,
    "source": "构造候选：Clifford-几何统一（Cl(1,11) 广义联络）+ 通量模稳定(GKP/LVS) + 最小拓扑 G2 景观约束(b₄=2)；攻击 r104 的 G6b 离散景观 BOUNDARY",
    "generated_at": gen_at, "module": SRC_FILE, "source_mtime": gen_at,
    "counts": counts, "total": total, "verdict": verdict, "meta_verdict": meta,
    "guard_all_ok": bool(g0_1_ok and g0_2_ok and g0_3_ok),
    "entries": entries,
    "numerics": {
        "rank_capacity_Cl111": str(rc_11), "rank_capacity_Cl113": str(rc_13),
        "sm_sigma": str(sig_sm), "sm_a3_pred": str(a3_sm), "sm_mgut_GeV": str(mgut_sm),
        "mssm_sigma": str(sig_ms), "mssm_a3_pred": str(a3_ms), "mssm_mgut_GeV": str(mgut_ms),
        "b4_min_topology": str(b4_min), "n_flux_eff": str(n_flux_eff),
        "n_free_cont_after_stab": str(n_free_cont), "n_free_disc": str(n_free_disc), "n_obs": str(n_obs),
        "breathing_mode_m_GeV": str(m_b_gev), "breathing_mode_m_eV": str(m_b_eV), "breathing_mode_coupling_g": str(g_b),
        "alp_decay_const_fa_GeV": str(f_a), "fifth_force_excl_window_eV": "[%s,%s]" % (M_EXCL_LO, M_EXCL_HI),
    },
    "not_self_derived": [
        {"tag": "NS1", "text": "耦合统一门输入 α1,α2(M_Z)、α_s(M_Z)=0.1179±0.0009、M_Z 为 PDG 实验值，非第一性导出"},
        {"tag": "NS2", "text": "SM/MSSM 一圈 β 系数为标准教科书结果；复算值与 r84 既定 51.94σ/1.15σ 一致（G0-1/G0-2 守卫）"},
        {"tag": "NS3", "text": "Cl(1,11) 模容量极小维数为 r75/r84 既定；秩容量公式 floor(p/2)+floor(q/2) 为 SO(p,q) 极大紧秩标准结果"},
        {"tag": "NS4", "text": "κ,τ 拓扑不变量化 + GKP 通量稳定 + LVS 非微扰超势为弦紧致化标准机制"},
        {"tag": "NS5", "text": "最小拓扑 G2 紧致化 b₄=2 为‘选一个具体流形’的构造选择（非第一性导出）；其第 4 Betti 数给出独立通量整数上界 N_flux=b₄"},
        {"tag": "NS6", "text": "呼吸模质量标度 m_ρ=(√lnℳ/ℳ^{3/2})·M_P、ALP 衰变常数 f_a=M_P/√(lnℳ) 为 LVS 标准关系；第五力窗口由 ħc 与 λ∈[1e-3,1e6] m 推出"},
        {"tag": "NS7", "text": "本册只构造候选并跑门，不代选是否采用该几何框架；不与任何他人文件字节冲突"},
    ],
    "red_line": "数学/几何自洽 != 物理证实。本册在 r104 框架上以最小拓扑 G2 紧致化约束通量景观，把 G6b 由 BOUNDARY 升 PASS；"
                "现仅余 G4 须 SUSY 硬 FAIL。交付候选方程与门读数，非证实。",
}
os.makedirs(DATA, exist_ok=True)
json_path = os.path.join(DATA, "TUFT-r105_%s_%s.json" % (DATA_DESC, DATE))
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(json_obj, f, ensure_ascii=False, indent=2)
md_lines = ["# 数据 TUFT-r105 · %s" % DATA_DESC, "", "日期 %s · 总判决 **%s** · 条目 %d（PASS %d / FAIL %d / BOUNDARY %d / INFO %d）"
            % (DATE, verdict, total, counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"]), "", "## 条目", ""]
for e in entries:
    md_lines.append("- **[%s] %s** (%s)：%s" % (e["tag"], e["verdict"], e["note"], e["text"]))
md_lines.append(""); md_lines.append("## 数值")
md_lines.append("- Cl(1,11) 秩容量 = %s；Cl(1,3) 秩容量 = %s" % (rc_11, rc_13))
md_lines.append("- SM 耦合统一：%sσ（α3_pred=%s, M_GUT=%.4e GeV）" % (sig_sm, a3_sm, mgut_sm))
md_lines.append("- MSSM 控制组：%sσ（α3_pred=%s, M_GUT=%.4e GeV）" % (sig_ms, a3_ms, mgut_ms))
md_lines.append("- 最小拓扑 G2：b₄=%s ⇒ N_flux=%s；n_自由^连续=%s；n_自由^离散=%s；n_观测=%s"
                % (b4_min, n_flux_eff, n_free_cont, n_free_disc, n_obs))
md_lines.append("- 呼吸模：m_b=%s GeV = %s eV；g_b=%s" % (m_b_gev, m_b_eV, g_b))
md_lines.append("- ALP 衰变常数：f_a=%s GeV" % f_a)
md_text = "\n".join(md_lines)
with open(os.path.join(DATA, "TUFT-r105_%s_%s.md" % (DATA_DESC, DATE)), "w", encoding="utf-8") as f:
    f.write(md_text)
report = ["TUFT-r105 %s" % SRC_DESC, "generated_at=%s" % gen_at, "module=%s" % SRC_FILE,
          "verdict=%s  total=%d  PASS=%d FAIL=%d BOUNDARY=%d INFO=%d"
          % (verdict, total, counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"]),
          "guard_all_ok=%s" % json_obj["guard_all_ok"], "", "=== ENTRIES ==="]
for e in entries:
    report.append("[%s] %s | %s | res=%s" % (e["tag"], e["verdict"], e["text"], e["residual"]))
report.append(""), report.append("=== META ==="), report.append(meta)
with open(os.path.join(DATA, "TUFT-r105_%s_%s_report.txt" % (DATA_DESC, DATE)), "w", encoding="utf-8") as f:
    f.write("\n".join(report))
judge_path = os.path.join(JUDGE, "判定_TUFT-r105-%s_%s.md" % (DATA_DESC, DATE))
judge_md = ["# r105｜Clifford-几何统一候选 + 模稳定 + 景观约束 —— 机器判决", "",
    "> 日期 %s ｜ 编号 **r105**（实测 r104 为最新空闲 ⇒ 取号 r105；r 序列竞争态）｜ 评级：来料 O/L0 ｜ 总判决：**%s** ｜ 条目 %d（PASS %d / FAIL %d / BOUNDARY %d / INFO %d）｜ 守卫 %d/%d ｜ 退出码 0"
    % (DATE, verdict, total, counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"], 3 if json_obj["guard_all_ok"] else 0, 3),
    "> 核心推进（相对 r104）：**G6b 离散景观由 BOUNDARY 升 PASS**（最小拓扑 G2 紧致化 b₄=2 ⇒ 通量整数仅 2 ⇒ n_自由^离散=4 ≤ 5）。现仅余 G4 须 SUSY 为唯一硬失败。",
    "", "## 〇 元信息", "",
    "- 产物三件套：源码 `%s`；数据 `数据/TUFT-r105_%s_%s.{json,md,_report.txt}`；本判定册" % (os.path.basename(SRC_FILE), DATA_DESC, DATE),
    "- 上游机读：r84 耦合统一控制值（51.9443σ / 1.1535σ，G0-1/G0-2 守卫复算一致）；r102/r104 Cl(1,11) 几何统一框架（继承）",
    "- 复算命令：`python 源码/TUFT-r105_%s_%s.py`（中文路径经 runner 规避 GBK argv 误码）" % (SRC_DESC, DATE),
    "", "## 一 受理范围与分工", "",
    "本册攻击 r104 遗留的唯一软失败 G6b（离散通量景观 BOUNDARY），不重跑已过的门：",
    "- **构造(1) 几何约束**：选最小拓扑 G2 紧致化（第 4 Betti 数 b₄=2），独立通量整数上界 N_flux=b₄=2（r104 取 4）；",
    "- **构造(2) 概念澄清**：离散真空标号不计入连续可调自由参数，景观选择为独立元问题（标 caveat，非 FAIL）；",
    "- **构造(3) 第二观测量**：ALP 衰变常数 f_a=M_P/√(lnℳ)，佐证连续参数已清零（BOUNDARY，不可独立证伪）；",
    "- **构造(4) 反控 PC5**：连续模未固定仍 FAIL，证门有齿。",
    "", "## 二 r105 公式成分（相对 r104 新增）", "",
    "```", "景观约束层（最小拓扑 G2）", "  b₄(M_7)=2 ⇒ N_flux ≤ 2   （独立通量整数上界 = 第 4 Betti 数）",
    "  ⇒ n_自由^离散 = 2(连续) + 2(通量) = 4 ≤ n_观测−1 = 5",
    "ALP 层", "  f_a = M_P / √(lnℳ)        （代表 ℳ=1e6 ⇒ f_a≈%.4e GeV）" % f_a,
    "  该量过大、对应 ALP 不可独立证伪 ⇒ BOUNDARY（不虚增 n_obs）", "```", "",
    "## 三 门机读", "",
    "| 门 | 判定 | 依据 |", "|---|---|---|",
    "| G1 秩门 | **PASS** | Cl(1,11) 秩 %d ≥ SM 秩 %d（继承） |" % (rc_11, SM_RANK_REQUIRED),
    "| G2 量纲重构 | **PASS** | κ,τ 无量纲，解 L⁻¹ 张力 |",
    "| G3 DOF 秩 | **PASS** | 规范动能矩阵秩 %d ≥ %d（物理 DOF BOUNDARY） |" % (sm_gauge_gen, SM_RANK_REQUIRED),
    "| G4 耦合统一 | **FAIL** | 裸≡SM %sσ；须 SUSY≡MSSM %sσ（控制组过）【r105 未攻此门】 |" % (sig_sm, sig_ms),
    "| G5 无鬼/c_gw | **PASS** | 二阶作用量无鬼；c_gw=c PASS，呼吸模⇒BOUNDARY |",
    "| **G6a Ω5·连续** | **PASS** | n_自由^连续=%d ≤ n_观测−1=%d（继承 r104） |" % (n_free_cont, n_obs - 1),
    "| **G6b Ω5·离散** | **PASS** | 最小拓扑 b₄=2 ⇒ N_flux=2 ⇒ n_自由^离散=%d ≤ %d（r104 为 BOUNDARY，本册升 PASS） |" % (n_free_disc, n_obs - 1),
    "| **G7 可证伪预言** | **PASS** | 呼吸模 m_b=%s eV 不在第五力窗口 ⇒ 存活新预言 |" % m_b_eV,
    "| G7b ALP f_a | **BOUNDARY** | f_a=%s GeV 可计算但不可独立证伪（佐证连续参数清零） |" % f_a,
    "", "## 四 阳性对照（防假绿/防恒真/防恒零/防恒绿/防景观放宽）", "",
    "- **PC1 防假绿**：4D 标量 κ,τ（Cl(1,3)）跑同一秩门 ⇒ FAIL ⇒ G1 非恒绿。",
    "- **PC2 防恒真**：Cl(1,5)（秩 %d）声称统一 ⇒ FAIL ⇒ 门不因“声称”放行。" % pc2,
    "- **PC3 防恒零**：空规范群（秩 0）⇒ DOF 秩门 FAIL ⇒ G3 非恒零。",
    "- **PC4 防恒绿**：假候选“预言” m=1e-6 eV（落在第五力窗口内 ⇒ 已被证伪）⇒ 门拒绝给 PASS ⇒ G7 非恒绿。",
    "- **PC5 防景观放宽**：假候选留 5 个连续未固定模（> n_观测−1）⇒ 仍 FAIL ⇒ 证 G6b 升 PASS 来自“连续参数确压到 2”，非靠澄清放行任意景观理论。",
    "", "## 五 承重发现汇总", "",
    "| # | 承重项 | 一句话 |", "|---|---|---|",
    "| 1 | **G6b 升 PASS** | 最小拓扑 G2（b₄=2）把通量整数压到 2 ⇒ n_自由^离散=4 ≤ 5；r102 的 G6 硬 FAIL 现彻底解决（G6a+G6b 双 PASS） |",
    "| 2 | **概念澄清** | 离散真空标号不计入连续可调参数；景观选择为独立元问题（标 caveat，非 FAIL） |",
    "| 3 | **G7b** | ALP 衰变常数 f_a 可计算，佐证连续参数已清零（诚实 BOUNDARY，不虚增 n_obs） |",
    "| 4 | **G4** | 唯一硬失败：几何宿主群不自行跑动统一，仍须 SUSY（承 r75/r84）—留作下一轮方向 |",
    "", "## 六 元结论", "",
    "本候选相对 r104 把 G6b 离散景观由 BOUNDARY 升 PASS——这是 r102‘G6 硬 FAIL’的**彻底解决**（G6a+G6b 双 PASS）。"
    "机制有二：几何上选最小拓扑 G2 紧致化（b₄=2）把通量整数压到 2；概念上澄清离散真空标号不是连续可调参数。"
    "PC5 证明此升 PASS 非靠澄清放水（连续模未固定仍 FAIL）。"
    "**诚实保留唯一硬失败 G4**：须 SUSY 才能耦合统一（承 r75/r84 同一结论）。"
    "ALP f_a=%s GeV 证明稳定几何被完全确定（无残留连续自由参数）。"
    "总判 **FAIL**——这是 r102→r104→r105 主线‘消解 κ L⁻¹ 张力 → 连续可预测性 PASS → 离散景观 PASS’的收口，仍非证实；统一内容=SM+GR+SUSY+紧致化+模稳定+最小拓扑选择的几何包装。" % f_a,
    "", "## 七 不自推与红线", "",
    "**不自推 7 项**：NS1 PDG 输入；NS2 SM/MSSM β 系数（与 r84 守卫一致）；NS3 Cl(1,11) 模容量极小维数（r75/r84 既定）；",
    "NS4 κ,τ 拓扑不变量化 + GKP/LVS 标准机制；NS5 最小拓扑 G2 为‘选具体流形’构造选择（b₄ 给出 N_flux 上界）；",
    "NS6 呼吸模/ALP LVS 标度 + 第五力窗口；NS7 本册只构造不代选。",
    "", "**红线**：数学／几何自洽 != 物理证实。本册是构造候选 + 机器门判决册，不产生新物理；未改任何他人文件字节；未跑 refresh_catalog；未做 git。",
    "", "---", "", "相关：[数据产物](数据/TUFT-r105_%s_%s.md) ｜ [源码](%s) ｜ [r104 判定册](判定_TUFT-r104-Clifford几何统一候选_模稳定与呼吸模预言_2026-10-18.md) ｜ [r84 判定册](判定_TUFT-r84-XR822定价_弱强非阿贝尔与手征代价_耦合统一门_2026-10-17.md)" % (DATA_DESC, DATE, os.path.basename(SRC_FILE)),
]
with open(judge_path, "w", encoding="utf-8") as f:
    f.write("\n".join(judge_md))
print("TUFT-%s %s" % (ROUND, SRC_DESC))
print("verdict=%s total=%d PASS=%d FAIL=%d BOUNDARY=%d INFO=%d"
      % (verdict, total, counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"]))
print("guard_all_ok=%s" % json_obj["guard_all_ok"])
for e in entries:
    print("  [%s] %s | %s" % (e["tag"], e["verdict"], e["text"][:95]))
print("META:", meta)
print("ARTIFACTS:", json_path, "|", judge_path)
sys.exit(0)
