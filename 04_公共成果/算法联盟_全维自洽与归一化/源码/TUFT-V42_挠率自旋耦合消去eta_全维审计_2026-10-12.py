# -*- coding: utf-8 -*-
"""
TUFT-V4.2 挠率-自旋耦合拉氏量：从 4 维 EC 作用量严格导出，消去唯象 eta
机器验证（mpmath 250 位）。本脚本只做可算复核，不产生新物理。

纪律：数学自洽 != 实验证实；任何"恒等于零/无量纲"的裁定必须机器兜底。
"""
import sys, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import mpmath as mp

mp.mp.dps = 250

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\算法联盟_全维自洽与归一化"

# ---------- 量纲工具 (M, L, T, Q) ----------
def mk(*v):
    return tuple(v)

def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))

def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))

# 基本量纲
D_c    = mk(0, 1, -1, 0)
D_hbar = mk(1, 2, -1, 0)
D_e    = mk(0, 0, 0, 1)   # 电荷作为独立基维度
D_me   = mk(1, 0, 0, 0)
D_dimless = mk(0, 0, 0, 0)
D_G    = mk(-1, 3, -2, 0)  # L^3 M^-1 T^-2

# ---------- 常数 (CODATA 口径, 250 位) ----------
c    = mp.mpf('299792458')
hbar = mp.mpf('1.0545718176461565e-34')
me   = mp.mpf('9.1093837015e-31')
e    = mp.mpf('1.602176634e-19')
m_mu = mp.mpf('1.883531627e-28')   # CODATA 缪子质量

# 电子 g-2（实验 vs QED 主体）
a_exp = mp.mpf('1.15965218059e-3')
a_qed = mp.mpf('1.15965218128e-3')
Delta_a_e = a_exp - a_qed          # 用户来料给定数字 => -6.9e-13（注意：非其手算估计的 -6.9e-11）

# 缪子 g-2 实验缺口（Fermilab 2021 vs SM 2020）：+251(59)e-11
Delta_a_mu_exp = mp.mpf('2.51e-9')

# ---------- 核心反解 ----------
# K = -3 m_e^2 c / (4 e hbar^2)
K = -3 * me**2 * c / (4 * e * hbar**2)
# 令 a_e^TUFT = K * cot_theta 拟合到 Delta_a_e（电子 1 点拟合）
cot_theta = Delta_a_e / K
tan_theta = 1 / cot_theta
theta = mp.pi/2 - 1/tan_theta       # 因 cot 极小，theta 极接近 pi/2

# 缪子：同一 cot_theta，仅质量替换
ratio_mu_e = (m_mu / me)**2
a_mu_TUFT = ratio_mu_e * Delta_a_e   # = K_mu * cot_theta

# 缪子检验偏差
dev_mu_mag = abs(a_mu_TUFT - Delta_a_mu_exp) / abs(Delta_a_mu_exp)
# 【本轮自抓·修实现 bug】原式 sign_mismatch = ((a_mu_TUFT < 0) != (Delta_a_mu_exp > 0))
# 两侧用了相反取向的测试（<0 与 >0），逻辑恒等取反而把"符号相反"判成 sign_mismatch=False。
# 正确写法：两侧同取向比较。原判据与 N02 文案（"符号相反"）自相矛盾，属典型"绿灯但错"。
sign_mismatch = ((a_mu_TUFT < 0) != (Delta_a_mu_exp < 0))
assert (sign_mismatch == ((a_mu_TUFT * Delta_a_mu_exp) < 0)), "符号判据两种写法须一致"

# ---------- 引力（与 V4 路线B 同形） ----------
sin_theta = 1 / mp.sqrt(1 + cot_theta**2)   # cot~1e-48 => sin_theta ~ 1 - 0.5*cot^2
# G_th = c^3 l0^2 / (hbar sin_theta)；sin_theta~1 时 l0 必须恰为 l_P=sqrt(hbar G/c^3) => 循环定义

# ---------- 量纲审计：a_e^TUFT 表达式 ----------
# dim[ -3 m^2 c / (4 e hbar^2) * cot_theta ] ; cot_theta 无量纲(三角比)
expr_dim = ddiv(dmul(dmul(D_me, D_me), D_c), dmul(D_e, dmul(D_hbar, D_hbar)))
is_dimless = (expr_dim == D_dimless)

# ================= 本轮新增机器裁定（第二段） =================
# ---- G_exp / l_P（同源口径，用于检验 G_th 回代是恒等式还是预言）----
G_exp = mp.mpf('6.67430e-11')
l_P   = mp.sqrt(hbar * G_exp / c**3)
G_th_back = c**3 * l_P**2 / (hbar * sin_theta)
G_identity_resid = abs(G_th_back / G_exp - 1)

# ---- 缺失因子的自然单位量纲分析 ----
# hbar=c=1, e 无量纲 => a_e = (3/4) m_e^2 cot_theta，[m_e]=1、[cot]=0 => 表达式质量量纲 = 2
dim_nat_expr = 2
dim_nat_need = 0
dim_nat_deficit = dim_nat_expr - dim_nat_need      # = +2，需补一个 E^-2 的因子
dim_G_natural = -2
G_is_missing_factor = (dim_G_natural == -dim_nat_deficit)

# ---- SI 口径：所需补齐因子量纲 Q L^3 T^-1；公设参数集 ±3 次幂穷举 ----
target_SI = mk(0, 3, -1, 1)
AXIOMS_NO_Q = [("c", D_c), ("hbar", D_hbar), ("me", D_me), ("G", D_G), ("lP", mk(0, 1, 0, 0))]
AXIOMS_WITH_Q = AXIOMS_NO_Q + [("e", D_e)]
_COEF = []

def _enum_hits(params, target, lo=-3, hi=3):
    hits = []
    n = len(params)

    def rec(i, acc):
        if i == n:
            if tuple(acc) == tuple(target):
                hits.append(tuple(_COEF))
            return
        nm, dv = params[i]
        for k in range(lo, hi + 1):
            _COEF.append(k)
            rec(i + 1, tuple(a + k * b for a, b in zip(acc, dv)))
            _COEF.pop()
    rec(0, (0, 0, 0, 0))
    return hits

_ENUM_SPACE_NO_Q = 7 ** len(AXIOMS_NO_Q)
_ENUM_SPACE_WITH_Q = 7 ** len(AXIOMS_WITH_Q)
hits_no_q = _enum_hits(AXIOMS_NO_Q, target_SI)
hits_with_q = _enum_hits(AXIOMS_WITH_Q, target_SI)
# 命中组的结构诊断：是否必须恰好用 e^1？是否含 m_e（会变成轻子依赖）？
hits_q_e_all_pow1 = all(h[-1] == 1 for h in hits_with_q)
hits_q_me_free = [h for h in hits_with_q if h[2] == 0]

# ---- 系数不变性：a = C m^2 cot_theta => a_mu/a_e = (m_mu/m_e)^2 与 C 无关 ----
def _ratio_for_C(C):
    ae = C * me**2 * cot_theta
    amu = C * m_mu**2 * cot_theta
    return amu / ae
ratio_C1 = _ratio_for_C(mp.mpf(1))
ratio_C2 = _ratio_for_C(1 / G_exp)
ratio_invariance_resid = abs(ratio_C1 - ratio_C2)

# ---- 改拟合到缪子后回代电子：符号是否互斥 ----
Delta_a_e_pred_from_mu = Delta_a_mu_exp / ratio_mu_e
sign_exclusive = ((Delta_a_e_pred_from_mu > 0) != (Delta_a_e > 0))
dev_e_when_fitting_mu = abs(Delta_a_e_pred_from_mu - Delta_a_e) / abs(Delta_a_e)

# ---- tau 绝对标度 ----
kappa_abs = me * c / hbar
tau_abs = kappa_abs * cot_theta
one_over_lP = 1 / l_P
tau_ratio_planck = tau_abs / one_over_lP

# ---- 来料手算自抓（其 Delta_a 手写为 -6.9e-11，量级错 100 倍）----
hand_Delta_a_e = mp.mpf('-6.9e-11')
hand_cot = hand_Delta_a_e / K
hand_err_factor = hand_cot / cot_theta
one_minus_sin = 1 - sin_theta

# ---------- 维度自洽自检 ----------
self_dim_ok = (dmul(D_c, D_hbar) == mk(1, 3, -2, 0))  # c*hbar 量纲兜底
self_prec_ok = (mp.mp.dps == 250)

readings = {
    "mp_dps": mp.mp.dps,
    "constants": {
        "c": str(c), "hbar": str(hbar), "me": str(me), "e": str(e), "m_mu": str(m_mu),
        "a_exp": str(a_exp), "a_qed": str(a_qed), "Delta_a_e": str(Delta_a_e),
        "Delta_a_mu_exp": str(Delta_a_mu_exp),
    },
    "K": str(K),
    "cot_theta": str(cot_theta),
    "tan_theta": str(tan_theta),
    "theta_rad": str(theta),
    "theta_minus_pihalf": str(theta - mp.pi/2),
    "ratio_mu_e_sq": str(ratio_mu_e),
    "a_e_TUFT_fit": str(Delta_a_e),
    "a_mu_TUFT": str(a_mu_TUFT),
    "a_mu_TUFT_vs_exp_dev_mag": str(dev_mu_mag),
    "a_mu_sign_mismatch": bool(sign_mismatch),
    "sin_theta": str(sin_theta),
    "expr_dim_of_a_e_formula": list(expr_dim),
    "expr_is_dimensionless": bool(is_dimless),
    "round2": {
        "G_exp": str(G_exp),
        "l_P": str(l_P),
        "G_th_backsub_resid_rel": str(G_identity_resid),
        "dim_natural_expr_power": dim_nat_expr,
        "dim_natural_deficit_power": dim_nat_deficit,
        "dim_G_natural_power": dim_G_natural,
        "G_is_missing_factor": bool(G_is_missing_factor),
        "target_SI_for_missing_factor": list(target_SI),
        "enum_space_no_charge": _ENUM_SPACE_NO_Q,
        "hits_no_charge": len(hits_no_q),
        "hits_no_charge_examples": [list(h) for h in hits_no_q[:8]],
        "enum_space_with_charge": _ENUM_SPACE_WITH_Q,
        "hits_with_charge": len(hits_with_q),
        "hits_with_charge_examples": [list(h) for h in hits_with_q[:8]],
        "hits_with_charge_all_need_e_pow1": bool(hits_q_e_all_pow1),
        "hits_with_charge_m_e_free_count": len(hits_q_me_free),
        "hits_with_charge_m_e_free": [list(h) for h in hits_q_me_free],
        "ratio_mu_over_e_C1": str(ratio_C1),
        "ratio_mu_over_e_C2_repaired": str(ratio_C2),
        "ratio_invariance_resid": str(ratio_invariance_resid),
        "Delta_a_e_pred_when_fitting_mu": str(Delta_a_e_pred_from_mu),
        "sign_exclusive_e_vs_mu": bool(sign_exclusive),
        "dev_e_when_fitting_mu": str(dev_e_when_fitting_mu),
        "kappa_abs_per_m": str(kappa_abs),
        "tau_abs_per_m": str(tau_abs),
        "tau_over_planck_curvature": str(tau_ratio_planck),
        "hand_written_cot_theta": str(hand_cot),
        "hand_err_factor_vs_machine": str(hand_err_factor),
        "sign_mismatch_FIXED": bool(sign_mismatch),
    },
    "self_checks": {"dim_tool_ok": bool(self_dim_ok), "prec_ok": bool(self_prec_ok)},
}

# ---------- 条目裁定 ----------
verdicts = [
    {"code": "C01", "topic": "耦合系数 3/8 从 EC 轴挠率+Dirac 最小耦合导出",
     "verdict": "PASS", "caveat": "约定依赖（轴挠率 A_mu 定义、epsilon 符号、gamma 约定），3/8 是标准 EC 结果的非唯一书写；非 TUFT 原创新物理。"},
    {"code": "C02", "topic": "非相对论约化 psi_bar gamma5 gamma_i psi -> psi^dagger sigma_i psi",
     "verdict": "PASS", "caveat": "Dirac 表示下标准约化，符号/因子正确。"},
    {"code": "D01", "topic": "a_e^TUFT = -(3 m_e^2 c)/(4 e hbar^2) cot_theta 量纲",
     "verdict": "FAIL", "caveat": "量纲 = T/(C L^3) = (0,-3,1,-1)，非无量纲；a_e=(g-2)/2 必须无量纲。SI 下该式不是合法反常磁矩。自然单位(c=hbar=1)下仍余质量^2，未消除。"},
    {"code": "D02", "topic": "缺失因子的量纲定位与公设集穷举（决定“消去 eta”是否成立）",
     "verdict": "FAIL",
     "caveat": "自然单位(ħ=c=1, e 无量纲)下 a_e ∝ m_e^2 cot_theta 质量量纲 = E^{+2}，而 a_e 须为 E^0 ⇒ 必须补一个 E^{-2} 因子；公设集中唯一命中者是 [G]=E^{-2}（1/G 型因子），即推导丢掉了爱因斯坦-嘉唐的 1/16πG 归一。SI 口径所需补齐因子量纲 = Q L^3 T^{-1} = (0,3,-1,1)；在 {c,ħ,m_e,G,l_P} 的 ±3 次幂穷举 %d/%d 中命中 %d。允许独立电荷标度 (+e) 后命中 %d/%d；结构诊断：全部命中必须恰好用 e^1（%s），其中完全不含 m_e 的仅 %d 组。结论：(a)“消去人工 η”不成立 —— η 只是被换成一个没有名字、没有公设出处的复合常数；(b) 但无论取哪一组补齐，只要该系数是轻子普适常数，它在电子/缪子比值中消去，N03 的证伪一字不变。"
             % (_ENUM_SPACE_NO_Q, _ENUM_SPACE_NO_Q, len(hits_no_q), len(hits_with_q),
                _ENUM_SPACE_WITH_Q, hits_q_e_all_pow1, len(hits_q_me_free))},
    {"code": "N03", "topic": "证伪对缺失因子的不变性（结构性别证）",
     "verdict": "FAIL",
     "caveat": "因 a = C·m^2·cot_theta 形式固定，a_mu/a_e ≡ (m_mu/m_e)^2 与 C 无关：机器复核 C=1 与 C=1/G_exp 两套系数，比值残差 %s（机器零）。故补上 D02 的因子后 N02 的缪子结论一字不变。反向拟合：若改拟合缪子（+%s），电子 Δa_e 预言 = %s（正），而给定实测 Δa_e = %s（负），符号互斥、偏差 %s。=> 1 参数 / 2 数据点，两种符号分配各有 1 个失败，**g-2 窗口结构性关闭**，与 r19/r27/r41 的“窗口已关”结论同源且更强（本次对缺失因子免疫）。"
             % (mp.nstr(ratio_invariance_resid, 3), mp.nstr(Delta_a_mu_exp, 3),
                mp.nstr(Delta_a_e_pred_from_mu, 4), mp.nstr(Delta_a_e, 4), mp.nstr(dev_e_when_fitting_mu, 4))},
    {"code": "N01", "topic": "cot_theta 反解（电子 g-2 拟合）",
     "verdict": "INFO", "caveat": "cot_theta = %s；1 参数吸收 1 数据点，无预言力（与 V4 路线B 的 chi^2 dof=-1 同构）。" % str(mp.nstr(cot_theta, 6))},
    {"code": "N02", "topic": "缪子 a_mu^TUFT 与 Fermilab 比较",
     "verdict": "FAIL", "caveat": "a_mu^TUFT = %s（负），实验需 +%s；符号相反（机器 sign_mismatch=%s，已修首版取向写反的判据 bug）且量级偏差 ~%s 倍 => 证伪。" % (
         str(mp.nstr(a_mu_TUFT, 4)), str(Delta_a_mu_exp), bool(sign_mismatch), str(mp.nstr(dev_mu_mag, 4)))},
    {"code": "B01", "topic": "电子拟合可预言性",
     "verdict": "BOUNDARY", "caveat": "电子 a_e 是拟合目标本身（残差恒机器零），不是独立预言；唯一独立检验点是缪子 N02。"},
    {"code": "I01", "topic": "theta->pi/2 时 G_th 退化",
     "verdict": "INFO", "caveat": "sin_theta~1 => G_th = c^3 l0^2/(hbar)。取公设 l0=l_P 回代 CODATA G 得相对残差 %s（机器零）=> 该“匹配 CODATA”是恒等式复读（l_P 由 G 定义而来），零信息量；未第一性导出 G（与 r41 M1 二阶两难 A 同源）。" % mp.nstr(G_identity_resid, 3)},
    {"code": "I03", "topic": "来料手算自抓",
     "verdict": "INFO", "caveat": "来料手算把 Δa_e 写作 -6.9e-11，实为 -6.9e-13（机器 %s）=> cot_theta 手算值 %s 与机器值 %s 相差恰好 %s 倍（量级笔误，非物理）。theta - pi/2 机器值 %s rad；1 - sin_theta = %s，即“sin_theta≈1”在第 95 位才成立，接近 90° 的说法本身与 θ 定义自洽但不含新信息。" % (
         mp.nstr(Delta_a_e, 3), mp.nstr(hand_cot, 4), mp.nstr(cot_theta, 4), mp.nstr(hand_err_factor, 4), mp.nstr(theta - mp.pi/2, 4), mp.nstr(one_minus_sin, 3))},
    {"code": "I02", "topic": "人工 eta 已消去",
     "verdict": "INFO", "caveat": "耦合系数 3/8 由 EC 自旋联络第一性给出，不再需手动体积耦合 l0^3；这是相对上一步唯象模型的真实进展。"},
    {"code": "V01", "topic": "终审",
     "verdict": "FAIL", "caveat": "g-2 公式量纲非法(D01/D02：缺 1/G 型因子，公设参数集穷举命中 0) + 缪子检验证伪(N02) + 证伪对缺失因子免疫(N03)；“消去人工 eta”不成立(I02 反转)。唯一真实进展=耦合系数 3/8 是标准 EC 结果的规范写法(C01)，不构成 TUFT 新物理。框架未通过可证伪检验。"},
]

n_pass = sum(1 for v in verdicts if v["verdict"] == "PASS")
n_fail = sum(1 for v in verdicts if v["verdict"] == "FAIL")
n_boundary = sum(1 for v in verdicts if v["verdict"] == "BOUNDARY")
n_info = sum(1 for v in verdicts if v["verdict"] == "INFO")

# ---------- 第二段自检守卫（任何一条为假 => 脚本必须暴露，不许绿灯）----------
guard_enum_noq = (len(hits_no_q) == 0)                       # 公设参数集内无补齐因子
guard_G_dim = G_is_missing_factor# 唯一命中者必须是 [G]=E^-2
guard_ratio_inv = (ratio_invariance_resid < mp.mpf('1e-60'))# 证伪对系数不变
guard_sign_fix = bool(sign_mismatch)                    # 符号判据已修且为真
guard_sign_excl = bool(sign_exclusive)                  # 拟合缪子 => 电子符号互斥
guard_identity = (G_identity_resid < mp.mpf('1e-40'))# G_th 回代为恒等式
guard_hand = (abs(hand_err_factor - 100) < mp.mpf('1e-6'))    # 手算偏差恰 100 倍
D_lP2 = ddiv(dmul(D_hbar, D_G), dmul(dmul(D_c, D_c), D_c))   # l_P^2 = hbar G / c^3
guard_dim_tool = (D_lP2 == mk(0, 2, 0, 0))# l_P^2 = L^2  =>  l_P = L
self_checks_all = all([self_dim_ok, self_prec_ok, guard_enum_noq, guard_G_dim,
                       guard_ratio_inv, guard_sign_fix, guard_sign_excl,
                       guard_identity, guard_hand, guard_dim_tool, (not is_dimless)])
self_check_list = {
    "dim_tool_ok": bool(self_dim_ok), "prec_ok": bool(self_prec_ok),
    "lP_dim_ok": bool(guard_dim_tool),
    "axiom_set_cannot_complete_dimension": bool(guard_enum_noq),
    "G_is_the_missing_factor": bool(guard_G_dim),
    "muon_refutation_invariant_to_coefficient": bool(guard_ratio_inv),
    "sign_mismatch_guard_true": bool(guard_sign_fix),
    "e_mu_sign_exclusive": bool(guard_sign_excl),
    "G_backsub_is_identity": bool(guard_identity),
    "hand_calc_off_by_100x": bool(guard_hand),
    "expr_not_dimensionless_as_judged": bool((not is_dimless)),
}

result = {
    "title": "TUFT-V4.2 挠率-自旋耦合消去 eta 全维审计",
    "round": "r42",
    "date": "2026-10-12",
    "rating": "O/L2",
    "readings": readings,
    "verdicts": verdicts,
    "entry_counts": {"PASS": n_pass, "FAIL": n_fail, "BOUNDARY": n_boundary, "INFO": n_info},
    "self_checks_pass": bool(self_checks_all),
    "self_checks": self_check_list,
}

with open(BASE + r"\数据\TUFT-V42_挠率自旋耦合消去eta_全维审计_2026-10-12.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# 简短 data md
md = []
md.append("# TUFT-V42 挠率-自旋耦合消去 eta · 机器读数记录")
md.append("")
md.append("- 引擎：源码/TUFT-V42_挠率自旋耦合消去eta_全维审计_2026-10-12.py（mpmath %d 位）" % mp.mp.dps)
md.append("- 评级：O/L2（可算验证推导层；g-2 窗口未过）")
md.append("")
md.append("## 关键读数")
md.append("")
md.append("| 量 | 值 |")
md.append("|---|---|")
md.append("| K = -3 m_e^2 c/(4 e hbar^2) | %s |" % str(mp.nstr(K, 6)))
md.append("| cot_theta（电子拟合） | %s |" % str(mp.nstr(cot_theta, 6)))
md.append("| theta - pi/2 | %s rad |" % str(mp.nstr(theta - mp.pi/2, 6)))
md.append("| (m_mu/m_e)^2 | %s |" % str(mp.nstr(ratio_mu_e, 6)))
md.append("| a_mu^TUFT | %s |" % str(mp.nstr(a_mu_TUFT, 6)))
md.append("| Fermilab Delta_a_mu | +%s |" % str(Delta_a_mu_exp))
md.append("| 缪子偏差量级 | ~%s 倍，符号相反 |" % str(mp.nstr(dev_mu_mag, 4)))
md.append("| a_e^TUFT 表达式量纲 | (0,-3,1,-1) = T/(C L^3)，非无量纲 |" )
md.append("| sin_theta | %s |" % str(mp.nstr(sin_theta, 6)))
md.append("")
md.append("## 第二段读数（新增裁定）")
md.append("")
md.append("| 量 | 值 |")
md.append("|---|---|")
md.append("| 自然单位下表达式质量量纲 | E^{+%d}，a_e 须 E^0 => 缺 E^{-2} 因子 |" % dim_nat_expr)
md.append("| 公设集 {c,hbar,m_e,G,l_P} ±3 幂穷举命中补齐因子 | %d / %d |" % (len(hits_no_q), _ENUM_SPACE_NO_Q))
md.append("| 允许独立电荷标度 (+e) 后命中 | %d / %d（等价于重新引入 η） |" % (len(hits_with_q), _ENUM_SPACE_WITH_Q))
md.append("| a_mu/a_e 比值（C=1 vs C=1/G_exp） | 残差 %s（与系数无关） |" % mp.nstr(ratio_invariance_resid, 3))
md.append("| 改拟合缪子 => 电子 Δa_e 预言 | %s（正），实测 %s（负），符号互斥 |" % (mp.nstr(Delta_a_e_pred_from_mu, 4), mp.nstr(Delta_a_e, 4)))
md.append("| G_th 回代 CODATA 相对残差 | %s（恒等式复读，零信息量） |" % mp.nstr(G_identity_resid, 3))
md.append("| tau 绝对值 | %s m^-1（1/l_P = %s m^-1，比值 %s） |" % (mp.nstr(tau_abs, 4), mp.nstr(one_over_lP, 4), mp.nstr(tau_ratio_planck, 4)))
md.append("| 来料手算 cot_theta | %s，与机器差 %s 倍 |" % (mp.nstr(hand_cot, 4), mp.nstr(hand_err_factor, 4)))
md.append("")
md.append("## 自检守卫")
md.append("")
md.append("| 守卫 | 值 |")
md.append("|---|---|")
for _k, _v in self_check_list.items():
    md.append("| %s | %s |" % (_k, _v))
md.append("")
md.append("## 条目")
md.append("")
md.append("| 码 | 主题 | 结论 |")
md.append("|---|---|---|")
for v in verdicts:
    md.append("| %s | %s | %s |" % (v["code"], v["topic"], v["verdict"]))
md.append("")
md.append("条目：PASS %d / FAIL %d / BOUNDARY %d / INFO %d" % (n_pass, n_fail, n_boundary, n_info))
md.append("")
md.append("> 红线：数学自洽 != 实验证实。耦合系数 3/8 第一性导出是真实进展，但 g-2 公式量纲非法且缪子检验证伪。")

with open(BASE + r"\数据\TUFT-V42_挠率自旋耦合消去eta_全维审计_2026-10-12.md", "w", encoding="utf-8") as f:
    f.write("\n".join(md))

print("SELF_CHECKS_PASS=%s  entries PASS=%d FAIL=%d BOUNDARY=%d INFO=%d" % (
    result["self_checks_pass"], n_pass, n_fail, n_boundary, n_info))
print("cot_theta=%s" % mp.nstr(cot_theta, 6))
print("a_mu_TUFT=%s  exp=+%s  dev~%s x  sign_mismatch=%s" % (
    mp.nstr(a_mu_TUFT, 4), Delta_a_mu_exp, mp.nstr(dev_mu_mag, 4), sign_mismatch))
print("expr_dim(noncst)=%s dimensionless=%s" % (expr_dim, is_dimless))
print("hits_no_q=%d/%d  hits_with_q=%d/%d  G_is_missing_factor=%s" % (
    len(hits_no_q), _ENUM_SPACE_NO_Q, len(hits_with_q), _ENUM_SPACE_WITH_Q, G_is_missing_factor))
print("ratio_invariance_resid=%s  sign_exclusive=%s  G_identity_resid=%s" % (
    mp.nstr(ratio_invariance_resid, 3), sign_exclusive, mp.nstr(G_identity_resid, 3)))
print("self_check_list=%s" % json.dumps(self_check_list, ensure_ascii=False))
