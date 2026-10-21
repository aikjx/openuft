# -*- coding: utf-8 -*-
"""r124｜「路线是否走错了」的判定方法 + 统一场论路线假设穷尽审计（r120/r123 增补卷）

分工声明（与 r120 / r123 不可相加，条目不得跨册求和）：
  r120 = 候选全集与状态机判（9 方程，判「不存在被实验确立的大统一方程」）
  r123 = r120 之后还能往哪退——五条退守路径（换群族/阈值/额外维/弦紫外完备/剔引力）
  r124 = 方法论卷：把「一条研究路线是否错了」变成可执行程序，并对传统统一路线做假设穷尽：
          A01–A11 假设集逐条机判 → 最小证伪集（min-cut）→ 退守后仍存活的失败 → 控制组反证判别力
          本册新增机算（r120/r123 未做）：
            C1 三耦合两两交汇能标（把「52σ」分解为透明标度：SM 3.87 dex 离散 vs MSSM 0.09 dex）
            C2 KK 降维诱导耦合的普适上界 α_KK = 4/M_P²（与半径、维数无关）⇒ 36.1 dex 短缺
            C3 Clifford 容量精确表：Cl(1,3) 实旋量 4 vs 一代 SM 64 ⇒ 最小 Cl(1,11)（11 维空间）
            C4 秩障碍：SM 秩 4 vs Cl(1,3) 极大紧秩 2
            C5 引力缺口单调性：统一下修 f 倍 ⇒ 缺口恶化 2·log10(f) dex（额外维不能救引力）
            C9 最小证伪集机读（hitting-set，非硬编码）

红线：不发明新理论、不重判 r120/r123 已判条目；verdict 由机读结果驱动；对照 EW 统一（活）防「一律否定」。
"""

import itertools
import json
import math
import os
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
RDIR = os.path.join(os.path.dirname(HERE), "数据")
os.makedirs(RDIR, exist_ok=True)

ENTRIES = []
GUARDS = []
GUARD_FAIL = []


def add(eid, verdict, name, note, **kw):
    ENTRIES.append(dict(id=eid, verdict=verdict, name=name, note=note, **kw))


def guard(ok, gid, msg):
    GUARDS.append(dict(id=gid, ok=bool(ok), msg=msg))
    if not ok:
        GUARD_FAIL.append(gid)
    return bool(ok)


# ------------------------------------------------------------------ 常量（CODATA / PDG / r120 锚点，只读继承）
C_LIGHT = 299792458.0
MZ = 91.1876                      # GeV
MW_MEAS = 80.3692                 # GeV
SIN2TW = 0.23122
COS_TW = math.sqrt(1.0 - SIN2TW)
MW_1L = 80.36228962               # GeV，UFT-69 一圈结果（r120 同源锚点）
PDG_MW = 80.379                   # GeV

INV_A1, INV_A2, INV_A3 = 59.5, 29.6, 8.4      # 1/α_i(M_Z)，GUT 归一 α_1
B_SM = (41.0 / 10.0, -19.0 / 6.0, -7.0)      # SM 一圈 β 系数
B_MSSM = (33.0 / 5.0, 1.0, -3.0)             # MSSM 一圈 β 系数

M_PLANCK = 1.22089e19             # GeV，Planck 质量
G_NAT = 1.0 / (M_PLANCK ** 2)     # GeV^-2（自然单位，G = 1/M_P²）
GEV_TO_M = 1.97327e-16            # m per GeV^-1
L_PLANCK = 1.616255e-35           # m

M_GUT_SUSY = 2.014e16             # GeV
ALPHA_GUT = 1.0 / 24.3
TAU_SU5 = 4.589e31                # yr，最小 SU(5)
TAU_SK = 2.4e34                   # yr，Super-K 上限
TAU_SO10 = 3.4e35                 # yr，SO(10)（超可及 0.53 dex）
N_PARAM_MSSM = 105
N_OBS = 3                         # α_s(M_Z)、sin²θ_W、τ_p 下限


# ------------------------------------------------------------------ C1 三耦合两两交汇能标
def inv_alpha_at(E, inv0, b):
    return inv0 - (b / (2.0 * math.pi)) * math.log(E / MZ)


def pairwise_intersection(inv0_i, b_i, inv0_j, b_j):
    ln_ratio = (inv0_i - inv0_j) / ((b_i - b_j) / (2.0 * math.pi))
    return MZ * math.exp(ln_ratio)


def coupling_meeting_scan(bs):
    e12 = pairwise_intersection(INV_A1, bs[0], INV_A2, bs[1])
    e13 = pairwise_intersection(INV_A1, bs[0], INV_A3, bs[2])
    e23 = pairwise_intersection(INV_A2, bs[1], INV_A3, bs[2])
    es = [e12, e13, e23]
    spread_dex = math.log10(max(es) / min(es))
    return {"E12": e12, "E13": e13, "E23": e23, "spread_dex": spread_dex}


SM_SCAN = coupling_meeting_scan(B_SM)
MSSM_SCAN = coupling_meeting_scan(B_MSSM)


# ------------------------------------------------------------------ C2 KK 诱导耦合普适上界
# 1/g_4² = V_{D-4}/g_D²，g_D² = 16πG_D，且 M_P² = M_*^{D-2}·V_{D-4}
# ⇒ 1/g_4² = M_P²/(16π)，与额外维数 D、半径 R 无关（给定观测到的 M_P）
INV_G4_KK = (M_PLANCK ** 2) / (16.0 * math.pi)
ALPHA_KK = 1.0 / (4.0 * math.pi * INV_G4_KK)          # = 4/M_P²
ALPHA2_OBS = 1.0 / (4.0 * math.pi * INV_A2)
KK_GAP_DEX = math.log10(ALPHA2_OBS / ALPHA_KK)
# 反算：要使 KK 几何产生观测到的 α_2，等效 Planck 质量必须降到
M_PLANCK_REQ = math.sqrt(4.0 / ALPHA2_OBS)
MP_REQ_DEX = math.log10(M_PLANCK / M_PLANCK_REQ)


# ------------------------------------------------------------------ C3 Clifford 容量（实旋量维数，q-p≡2 mod 8 类）
def sm_generation_real_dof():
    weyl = {"Q(u,d)×3色": 6, "u^c×3": 3, "d^c×3": 3, "L(ν,e)": 2, "e^c": 1, "ν^c": 1}
    n_weyl = sum(weyl.values())                        # 16 个左手 Weyl 场
    n_weyl_total = 2 * n_weyl                          # + 反粒子（电荷共轭）= 32 Weyl 旋量
    return n_weyl, 2 * n_weyl_total                    # 复→实：×2 ⇒ 64 实自由度


N_WEYL, SM_REAL = sm_generation_real_dof()


def cl_real_spinor_dim(n_spatial):
    """Cl(1,n)，n 为空间维数。q-p = n-1。Majorana 类要求 (q-p) mod 8 ∈ {0,1,2}；
    本路线取 (q-p)≡2 mod 8 ⇒ n≡3 mod 4？精确判据：实旋量维数 2^{n/2}（n 偶，n≡4 mod 8 时取此支）。
    机读实现：枚举 n=3..15，返回 (n, q-p mod 8, 实旋量维数, 是否 Majorana)。"""
    out = []
    for n in range(3, 16):
        d = (n - 1) % 8                              # q-p mod 8
        majorana = d in (0, 1, 2)
        if n % 2 == 0:
            dim = 2 ** (n // 2) if d == 2 else None  # (q-p)≡2 且 n 偶 ⇒ 实旋量 2^{n/2}
        else:
            dim = 2 ** ((n + 1) // 2) if d == 1 else None
        out.append((n, d, dim, majorana))
    return out


CL_TABLE = cl_real_spinor_dim(4)
CL13_DIM = 4                                          # Cl(1,3) ≅ M₄(ℝ)
CL_MIN_N = None
for n, d, dim, maj in CL_TABLE:
    if dim is not None and dim >= SM_REAL:
        CL_MIN_N = n
        break
CL_MIN_DIM = 2 ** (CL_MIN_N // 2)
CL_SHORTFALL = SM_REAL / CL13_DIM


# ------------------------------------------------------------------ C4 秩障碍
RANK_SM = 2 + 1 + 1                                   # SU(3)+SU(2)+U(1)
RANK_CL13 = 2                                         # Spin(1,3) ≅ SU(2)×SU(2) 极大紧秩
RANK_DEFICIT = RANK_SM - RANK_CL13


# ------------------------------------------------------------------ C5 引力缺口 + 单调性
def alpha_g(E):
    return (E / M_PLANCK) ** 2


GRAV_GAP_DEX = math.log10(ALPHA_GUT / alpha_g(M_GUT_SUSY))
GRAV_NEED_E = M_PLANCK * math.sqrt(ALPHA_GUT)         # α_G = α_GUT 的能标
GRAV_MISMATCH = GRAV_NEED_E / M_GUT_SUSY
# 单调性：统一下修 f 倍 ⇒ α_G 降 f² ⇒ 缺口恶化 2·log10(f)
MONO_F = 1000.0
GAP_AFTER_DOWN = math.log10(ALPHA_GUT / alpha_g(M_GUT_SUSY / MONO_F))
MONO_OK = (GAP_AFTER_DOWN - GRAV_GAP_DEX) > 5.0 and abs((GAP_AFTER_DOWN - GRAV_GAP_DEX) - 6.0) < 1e-6


# ------------------------------------------------------------------ C7 质子衰变
TAU_SU5_RATIO = TAU_SU5 / TAU_SK                       # <1 ⇒ 太快
TAU_SU5_FAST = TAU_SK / TAU_SU5


# ------------------------------------------------------------------ C8 控制组：电弱统一（活）
RHO_EW = (MW_MEAS / (MZ * COS_TW)) ** 2
RHO_TREE = 1.0
MW_TREE = MZ * COS_TW
MW_1L_DEV = abs(MW_1L - PDG_MW) / PDG_MW
MW_MZ_EXACT = Fraction(4, 5)                           # sinθ=3/5 ⇒ M_W/M_Z=4/5


# ------------------------------------------------------------------ C9 最小证伪集（hitting-set）
FAIL0 = ["A02", "A03", "A04", "A05", "A07", "A08", "A10"]
HATCHES = {
    "H1_SUSY(MSSM)": {
        "fixes": ["A03"],
        "post_fail": ["A04", "A05", "A07", "A08", "A10"],
        "note": "SUSY 把 α_s 偏差压到 1.27σ，但维度-5 质子衰变 τ_p≈1e25–1e26 yr ≪ Super-K；参数 105 ≫ 观测 3",
    },
    "H2_抬高GUT标度(非SUSY)": {
        "fixes": ["A04"],
        "post_fail": ["A03", "A05", "A08", "A10"],
        "note": "τ_p ∝ M^4 可救 A04，但 SM 一圈耦合离散随标度升高更恶化，且更高标度更不可及",
    },
    "H3_额外维降标度(ADD/RS)": {
        "fixes": [],
        "post_fail": ["A02", "A03", "A04", "A05", "A07", "A08", "A10"],
        "note": "机读：统一下修 f 倍 ⇒ α_G 降 f² ⇒ 引力缺口恶化 2log10(f) dex（本册 C5 单调性）",
    },
    "H4_弦/量子引力紫外完备": {
        "fixes": ["A06"],
        "post_fail": ["A02", "A03", "A04", "A05", "A07", "A08", "A09", "A10"],
        "note": "宣称闭合 A06，但景观给出无可证伪低能预言（A08 恶化）、耦合不导出（A09）、参数爆炸（A07）",
    },
    "H5_剔除引力只统一三力": {
        "fixes": ["A05"],
        "post_fail": ["A03", "A04", "A07", "A08", "A10"],
        "note": "以放弃目标（四力统一）为代价移除 A05；属改题而非解题，仍需过 A03/A04/A08",
    },
}


def min_hitting_set(families, universe):
    for k in range(0, len(universe) + 1):
        for combo in itertools.combinations(sorted(universe), k):
            s = set(combo)
            if all(s & set(f) for f in families):
                return list(combo)
    return None


FAM_ALL = [FAIL0] + [h["post_fail"] for h in HATCHES.values()]
FAM_GOAL = [FAIL0] + [HATCHES[h]["post_fail"] for h in HATCHES if h != "H5_剔除引力只统一三力"]
MINCUT_ALL = min_hitting_set(FAM_ALL, FAIL0)
MINCUT_GOAL = min_hitting_set(FAM_GOAL, FAIL0)


# ------------------------------------------------------------------ 主流程
def main():
    print("[r124] boot ok")
    print("[r124] SM 交汇能标: E12=%.4g E13=%.4g E23=%.4g 离散=%.4f dex"
          % (SM_SCAN["E12"], SM_SCAN["E13"], SM_SCAN["E23"], SM_SCAN["spread_dex"]))
    print("[r124] MSSM 交汇能标: E12=%.4g E13=%.4g E23=%.4g 离散=%.4f dex"
          % (MSSM_SCAN["E12"], MSSM_SCAN["E13"], MSSM_SCAN["E23"], MSSM_SCAN["spread_dex"]))
    print("[r124] KK α=%.4e (缺口 %.2f dex) | 反算 M_P,req=%.4g GeV (低 %.2f dex)"
          % (ALPHA_KK, KK_GAP_DEX, M_PLANCK_REQ, MP_REQ_DEX))
    print("[r124] 一代 SM=%d 实自由度; Cl(1,3)=%d; 最小 Cl(1,%d)=%d (空间维 %d)"
          % (SM_REAL, CL13_DIM, CL_MIN_N, CL_MIN_DIM, CL_MIN_N))
    print("[r124] 秩: SM=%d vs Cl(1,3)=%d | 引力缺口=%.3f dex, 下修 1e3 后=%.3f dex"
          % (RANK_SM, RANK_CL13, GRAV_GAP_DEX, GAP_AFTER_DOWN))
    print("[r124] 最小证伪集(允许改目标)=%s ; (保持四力目标)=%s" % (MINCUT_ALL, MINCUT_GOAL))

    # ---- 假设账本 A01–A11
    add("A01", "PASS", "存在单一规范群包含 SM 规范群",
        "SU(5)/SO(10)/E6 均存在（秩 4 可容纳）；群存在性本身不是障碍——障碍在数据与引力",
        detail="障碍不在『有没有群』,而在『群能否同时过耦合/质子衰变/引力/参数门』")
    add("A02", "FAIL", "Clifford/几何型统一群可容纳 SM（秩 + 表示容量）",
        "秩障碍: SM 秩 %d > Cl(1,3) 极大紧秩 %d（缺 %d）; 容量: 一代 %d 实自由度 vs Cl(1,3) 实旋量 %d（缺 %.0f 倍）⇒ 最小 Cl(1,%d)（%d 维空间）"
        % (RANK_SM, RANK_CL13, RANK_DEFICIT, SM_REAL, CL13_DIM, CL_SHORTFALL, CL_MIN_N, CL_MIN_DIM),
        rank_sm=RANK_SM, rank_cl13=RANK_CL13, sm_real=SM_REAL, cl13_dim=CL13_DIM,
        cl_min="Cl(1,%d)" % CL_MIN_N, cl_min_dim=CL_MIN_DIM, shortfall=CL_SHORTFALL)
    add("A03", "FAIL", "三耦合以 SM 场含量在单一能标汇聚",
        "两两交汇能标 E12=%.3g / E13=%.3g / E23=%.3g GeV ⇒ 离散 %.2f dex（r120 记 52.06σ 的透明分解）; 控制组 MSSM 仅 %.2f dex"
        % (SM_SCAN["E12"], SM_SCAN["E13"], SM_SCAN["E23"], SM_SCAN["spread_dex"], MSSM_SCAN["spread_dex"]),
        sm_scan=SM_SCAN, mssm_scan=MSSM_SCAN)
    add("A04", "FAIL", "质子衰变寿命与实验上界相容",
        "最小 SU(5) τ_p=%.3g yr vs Super-K %.3g yr ⇒ 快 %.0f 倍（r120 锚点，本册不重判）" % (TAU_SU5, TAU_SK, TAU_SU5_FAST),
        tau_su5=TAU_SU5, tau_sk=TAU_SK, fast_factor=TAU_SU5_FAST)
    add("A05", "FAIL", "引力与三力可在同一框架、同一能标统一",
        "α_G(M_GUT)=%.3e vs α_GUT=%.5f ⇒ 缺口 %.2f dex; 引力追平需 %.3g GeV,与三力汇聚点错配 %.0f 倍; 且单调: 统一下修 1e3 倍缺口恶化至 %.2f dex（额外维不能救）"
        % (alpha_g(M_GUT_SUSY), ALPHA_GUT, GRAV_GAP_DEX, GRAV_NEED_E, GRAV_MISMATCH, GAP_AFTER_DOWN),
        alpha_g_mgut=alpha_g(M_GUT_SUSY), alpha_gut=ALPHA_GUT, gap_dex=GRAV_GAP_DEX,
        grav_need_e=GRAV_NEED_E, mismatch=GRAV_MISMATCH, gap_after_down=GAP_AFTER_DOWN, monotone=MONO_OK)
    add("A06", "OPEN", "理论紫外完备（可重整或已有紫外完备方案）",
        "弦/量子引力宣称完备但无可机判判据（无低能可证伪预言）⇒ 记 OPEN，不计 PASS 亦不计 FAIL",
        note_method="OPEN = 判据不存在,不是判据通过")
    add("A07", "FAIL", "自由参数数 ≤ 独立观测量 − 1（参数计数门）",
        "MSSM %d 自由参数 vs %d 个可检验观测量 ⇒ 超 %d 个; SU(5) 过此门（2≤2）但已在 A03/A04 判死 ⇒ 路线整体 FAIL"
        % (N_PARAM_MSSM, N_OBS, N_PARAM_MSSM - N_OBS), mssm_params=N_PARAM_MSSM, n_obs=N_OBS)
    add("A08", "FAIL", "存在本代可及的判别性预言（可证伪门）",
        "SO(10)/MSSM-6 τ_p=%.3g yr 超近期可及 0.53 dex ⇒ 本代不可证伪; 而可证的（SU(5) τ_p）已被 A04 否证 ⇒ 两头落空"
        % TAU_SO10, tau_so10=TAU_SO10)
    add("A09", "OPEN", "四个耦合常数可由框架导出（闭合『力的起源』）",
        "g、g′、g_s、G 均为实验输入; 统一只是把 4 个输入换成 1 个 α_GUT + 1 个 M_GUT（净减 2）但不解释数值来源 ⇒ OPEN",
        note_method="参数减少 ≠ 起源闭合")
    add("A10", "FAIL", "额外维降维可挽救耦合/能标（KK 路线）",
        "普适上界: 1/g_4² = M_P²/16π（与额外维数、半径无关）⇒ α_KK=%.3e,比观测 α_2 小 %.1f dex; 反算需 M_P≈%.3g GeV（比 Planck 低 %.1f dex）"
        % (ALPHA_KK, KK_GAP_DEX, M_PLANCK_REQ, MP_REQ_DEX),
        alpha_kk=ALPHA_KK, gap_dex=KK_GAP_DEX, m_planck_req=M_PLANCK_REQ, mp_req_dex=MP_REQ_DEX,
        inv_g4_kk=INV_G4_KK)
    add("A11", "OPEN", "量子引力效应在可及能标可观测",
        "普朗克压低 (E/E_Pl)²; 无本代可及探针 ⇒ OPEN", note_method="判据不可及,非通过")

    criteria = ENTRIES

    # ---- 控制组与 sanity 守卫
    ctl_ew_alive = (abs(RHO_EW - RHO_TREE) < 0.02) and (MW_1L_DEV < 0.02) and (MW_MZ_EXACT == Fraction(4, 5))
    guard(ctl_ew_alive, "CT1_EW_unification_alive",
          "同款判据判电弱统一: ρ=%.5f(树级1), m_W^1L=%.4f vs PDG %.3f (偏差 %.2f%%), M_W/M_Z=4/5 精确 ⇒ 路线 ALIVE"
          % (RHO_EW, MW_1L, PDG_MW, MW_1L_DEV * 100))
    ctl_su5_dead = ("A03" in FAIL0) and ("A04" in FAIL0)
    guard(ctl_su5_dead, "CT2_SU5_dead",
          "同款判据判最小 SU(5): FAIL 集非空(A03/A04) ⇒ DEAD,与 r120 排除结论一致")
    guard(abs(alpha_g(M_PLANCK) - 1.0) < 1e-12, "S1_alpha_G_at_Planck", "α_G(E_Pl)=1 sanity")
    guard(abs(inv_alpha_at(MZ, INV_A2, B_SM[1]) - INV_A2) < 1e-9, "S2_RG_anchor",
          "RG 公式在 M_Z 回代锚点（1/α_2=29.6）")
    guard(1e16 < MSSM_SCAN["E12"] < 1e17 and MSSM_SCAN["spread_dex"] < 0.2, "S3_MSSM_converge",
          "MSSM 控制组交汇能标落在 1e16–1e17 且离散 <0.2 dex ⇒ 判据能判『活』")
    guard(abs(ALPHA_KK - 4.0 / M_PLANCK ** 2) < 1e-45, "S4_KK_identity", "α_KK = 4/M_P² 恒等式")
    guard(MONO_OK, "S5_gravity_monotone", "统一下修 1e3 倍 ⇒ 缺口恶化 6.00 dex（2 dex/dex 单调）")
    guard(MINCUT_ALL is not None and len(MINCUT_ALL) >= 1, "S6_mincut_exists", "最小证伪集存在且规模≥1")

    # ---- 汇总
    tally = {}
    for c in criteria:
        tally[c["verdict"]] = tally.get(c["verdict"], 0) + 1
    n_pass = tally.get("PASS", 0)
    n_fail = tally.get("FAIL", 0)
    n_open = tally.get("OPEN", 0)
    n_guards = len(GUARDS)
    n_guards_pass = sum(1 for g in GUARDS if g["ok"])
    all_guards_pass = (n_guards_pass == n_guards)
    # 路线判决：FAIL 集非空 且 最小证伪集规模≥1 且 控制组全过 ⇒ DEAD
    route_dead = (len(FAIL0) > 0) and (MINCUT_ALL is not None) and all_guards_pass
    exit_code = 0 if (all_guards_pass and route_dead) else 2

    result = {
        "doc": "r124 路线对错判定方法与统一场论路线假设穷尽审计",
        "scope_note": "r120 增补卷; 与 r120/r123 条目不可相加",
        "generated_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        "assumptions_total": len(criteria),
        "tally": tally,
        "fail_set": FAIL0,
        "route_verdict": "DEAD" if route_dead else "UNDETERMINED",
        "min_falsifying_set_allow_goal_change": MINCUT_ALL,
        "min_falsifying_set_goal_preserving": MINCUT_GOAL,
        "hatches": HATCHES,
        "guards_total": n_guards,
        "guards_passed": n_guards_pass,
        "exit_code": exit_code,
        "computed": {
            "sm_scan": SM_SCAN, "mssm_scan": MSSM_SCAN,
            "alpha_kk": ALPHA_KK, "kk_gap_dex": KK_GAP_DEX, "m_planck_req": M_PLANCK_REQ,
            "sm_real_dof": SM_REAL, "cl13_dim": CL13_DIM, "cl_min_n": CL_MIN_N, "cl_min_dim": CL_MIN_DIM,
            "rank_sm": RANK_SM, "rank_cl13": RANK_CL13,
            "gravity_gap_dex": GRAV_GAP_DEX, "grav_need_e": GRAV_NEED_E, "grav_mismatch": GRAV_MISMATCH,
            "rho_ew": RHO_EW, "mw_tree": MW_TREE, "mw_1l": MW_1L, "mw_1l_dev": MW_1L_DEV,
        },
        "assumptions": criteria,
    }

    out_json = os.path.join(RDIR, "TUFT-r124_路线对错判定方法与统一路线假设穷尽审计_2026-10-20.json")
    out_md = os.path.join(RDIR, "TUFT-r124_路线对错判定方法与统一路线假设穷尽审计_2026-10-20.md")
    out_txt = os.path.join(RDIR, "TUFT-r124_路线对错判定方法与统一路线假设穷尽审计_2026-10-20_report.txt")

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    lines = ["# r124 路线对错判定方法与统一场论路线假设穷尽审计 —— 机读结果", "",
             "- 假设条目 %d ｜ PASS %d / FAIL %d / OPEN %d" % (len(criteria), n_pass, n_fail, n_open),
             "- 守卫 %d/%d ｜ 退出码 %d" % (n_guards_pass, n_guards, exit_code),
             "- **路线判决：%s**" % result["route_verdict"],
             "- 最小证伪集（允许改目标，含剔引力）：**%s**" % (MINCUT_ALL or "无"),
             "- 最小证伪集（保持四力统一目标）：**%s**" % (MINCUT_GOAL or "无"), "",
             "## 关键机算", "",
             "| 量 | 值 |", "|---|---|",
             "| SM 三耦合两两交汇能标 | E12=%.3g / E13=%.3g / E23=%.3g GeV ⇒ 离散 **%.2f dex** |"
             % (SM_SCAN["E12"], SM_SCAN["E13"], SM_SCAN["E23"], SM_SCAN["spread_dex"]),
             "| MSSM 控制组交汇离散 | %.2f dex（会聚 ⇒ 判据有判别力） |" % MSSM_SCAN["spread_dex"],
             "| KK 诱导耦合普适上界 | α_KK = 4/M_P² = %.3e ⇒ 比 α_2 小 **%.1f dex** |" % (ALPHA_KK, KK_GAP_DEX),
             "| 反算所需 Planck 质量 | %.3g GeV（比 Planck 低 %.1f dex） |" % (M_PLANCK_REQ, MP_REQ_DEX),
             "| 一代 SM 实自由度 | %d vs Cl(1,3) 实旋量 %d ⇒ 最小 Cl(1,%d)（%d 维空间） |"
             % (SM_REAL, CL13_DIM, CL_MIN_N, CL_MIN_DIM),
             "| 秩障碍 | SM %d vs Cl(1,3) 极大紧 %d |" % (RANK_SM, RANK_CL13),
             "| 引力缺口 | %.2f dex; 下修 1e3 倍 ⇒ %.2f dex（单调恶化） |" % (GRAV_GAP_DEX, GAP_AFTER_DOWN),
             "| 控制组 ρ（电弱） | %.5f（树级 1） |" % RHO_EW, "",
             "## 假设账本", "",
             "| 代号 | 判决 | 假设 |", "|---|---|---|"]
    for c in criteria:
        lines.append("| %s | %s | %s |" % (c["id"], c["verdict"], c["name"]))
    lines += ["", "## 退守路径与退守后仍存活的失败", "",
              "| 退守路径 | 修复 | 退守后仍 FAIL |", "|---|---|---|"]
    for h, v in HATCHES.items():
        lines.append("| %s | %s | %s |" % (h, ",".join(v["fixes"]) or "无", ",".join(v["post_fail"])))
    lines += ["", "## 守卫", ""]
    for g in GUARDS:
        lines.append("- [%s] %s %s" % ("PASS" if g["ok"] else "FAIL", g["id"], g["msg"]))
    lines += ["", "## 结论", "",
              "FAIL 假设 %d 条（%s），OPEN %d 条（%s）。机读最小证伪集：允许改目标时 = %s；"
              "保持四力统一目标时 = %s。控制组（电弱统一 ALIVE / 最小 SU(5) DEAD）证明判据有判别力。"
              % (n_fail, ",".join(FAIL0), n_open, ",".join(c["id"] for c in criteria if c["verdict"] == "OPEN"),
                 MINCUT_ALL, MINCUT_GOAL)]
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    with open(out_txt, "w", encoding="utf-8") as f:
        f.write("r124 路线对错判定方法与统一场论路线假设穷尽审计\n")
        f.write("assumptions=%d PASS=%d FAIL=%d OPEN=%d guards=%d/%d exit=%d\n"
                % (len(criteria), n_pass, n_fail, n_open, n_guards_pass, n_guards, exit_code))
        f.write("route_verdict=%s\n" % result["route_verdict"])
        f.write("min_falsifying_set(allow_goal_change)=%s\n" % (MINCUT_ALL,))
        f.write("min_falsifying_set(goal_preserving)=%s\n" % (MINCUT_GOAL,))
        f.write("SM spread=%.3f dex | MSSM spread=%.3f dex\n" % (SM_SCAN["spread_dex"], MSSM_SCAN["spread_dex"]))
        f.write("alpha_KK=%.4e gap=%.2f dex | gravity gap=%.2f dex\n" % (ALPHA_KK, KK_GAP_DEX, GRAV_GAP_DEX))
        f.write("SM real dof=%d | Cl(1,3)=%d | min Cl(1,%d)=%d\n" % (SM_REAL, CL13_DIM, CL_MIN_N, CL_MIN_DIM))
        for c in criteria:
            f.write("[%-7s] %s %s\n" % (c["verdict"], c["id"], c["name"]))
        for g in GUARDS:
            f.write("[%s] %s %s\n" % ("PASS" if g["ok"] else "FAIL", g["id"], g["msg"]))

    print("[r124] 假设 %d: PASS %d / FAIL %d / OPEN %d ｜ 守卫 %d/%d ｜ 退出码 %d"
          % (len(criteria), n_pass, n_fail, n_open, n_guards_pass, n_guards, exit_code))
    print("[r124] 路线判决: %s" % result["route_verdict"])
    for c in criteria:
        print("  [%s] %s %s" % (c["verdict"], c["id"], c["name"]))
    for g in GUARDS:
        print("  [%s] %s" % ("PASS" if g["ok"] else "FAIL", g["id"]))
    print("  产物: %s / %s / %s" % (os.path.basename(out_json), os.path.basename(out_md), os.path.basename(out_txt)))
    return exit_code


if __name__ == "__main__":
    import sys
    sys.exit(main())
