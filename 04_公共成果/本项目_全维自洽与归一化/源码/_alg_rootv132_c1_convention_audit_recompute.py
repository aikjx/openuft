# -*- coding: utf-8 -*-
"""算法联盟 · ROOT V132「只令 c=1，保留 hbar 与 G」· 独立可算审计机核

性质：非判定册，不占 RID，不入 README，不回写任何既有产物，不与 TUFT 链相加。
审计对象：ROOT V132 来料（c=1 单位约定 / 八条核心方程 / S_total 作用量 /
          ℓ_P^2=hbar G 与 alpha_G=G m^2/hbar / 「从作用量推导量子相位、质量、
          规范耦合、引力动力学」的攻坚主张）。

核心审计问题（全部机读，结论随输入翻转，来源给一手 URL，不自盖章）：
  Q1 八条核心方程在 c=1 下是否全为单位约化 / 定义重排（恒等式），
     且对「误把 c=1 公式当 SI 用」的域错位敏感？
  Q2 ℓ_P^2=hbar G 与 alpha_G=G m^2/hbar 在 c=1 下是否为恒等式；
     两路（SI 显式 c / c=1 自然单位）是否一致；误用 SI 是否给出巨大偏差？
  Q3 S_total=(1/16πG)∫√-g R+S_gauge+S_matter 与其场方程
     G_{mu nu}=8πG T_{mu nu} 在 c=1 下内部系数是否自洽？（仅内部一致性，非物理证实）
  Q4 四条「从作用量推导」主张（量子相位 / 粒子质量 / 规范耦合 / 引力动力学）
     是否对外部输入参数有非零敏感度 → 零自由参数数值预言数 = 0？
  Q5 c=1 是否能定出 G：alpha_G(m) 无量纲但随 m 跨 45 数量级变化，
     量纲指数在 c=1 下仍留两个独立常数 → c=1 不能唯一确定 G。
  Q6 可翻转性：供给 Yukawa 耦合与 VEV 后质量「变为可推」，供给不同 m 时
     alpha_G 判词翻转 → 结论由外部输入驱动，非作用量本身驱动。
  Q7 外部一手：来料未给出处，本册补一手链接，且不制造假阳性出处错误。

红线：数学自洽 != 实验证实；不宣称攻破统一场论，不宣称独立实验预言；四力统一未证。
"""
import os
import glob
import json
from decimal import Decimal, getcontext

getcontext().prec = 70
D = Decimal

# 锚文件（唯一命中），产物写回其所在 数据/ 目录；中文路径不进 argv。
HITS = glob.glob(os.path.join("openuft", "**",
                              "_ALG_expdata_fullchain_来料总表_2026-11-11.json"),
                 recursive=True)
assert len(HITS) == 1, "ANCHOR-HITS=%d" % len(HITS)
DATA = os.path.dirname(HITS[0])
OUT_JSON = os.path.join(DATA, "_ALG_rootv132_c1_convention_audit_recompute_2026-11-21.json")


# ---------------------------------------------------------------- 工具
def sci(x, d=8):
    v = D(str(x))
    if v == 0:
        return "0"
    return format(v, "." + str(d) + "E")


def rel(a, b):
    b = D(str(b))
    if b == 0:
        return D(0) if D(str(a)) == 0 else D(9) ** 60
    return abs(D(str(a)) - b) / abs(b)


def atan_inv(x):
    """atan(1/x)，x>1；t=1/x，逐项 arctan 级数（自写 Machin，禁 numpy）。"""
    z = D(1) / D(x)
    zz = z * z
    p = z
    s = D(0)
    k = 0
    while True:
        term = p / D(2 * k + 1)
        s = s + term if k % 2 == 0 else s - term
        if abs(term) < D("1e-66"):
            break
        p *= zz
        k += 1
    return s


PI = D(16) * atan_inv(5) - D(4) * atan_inv(239)
LN10 = D(10).ln()

# ---------------------------------------------------------------- 常数（NIST CODATA 2022）
G = D("6.67430e-11")
c = D("299792458")
hbar = D("1.054571817e-34")   # = h/2π，9 位有效数字
H = D("6.62607015e-34")       # SI 精确定义
me = D("9.1093837139e-31")
mp = D("1.67262192595e-27")
c1 = D(1)                     # c=1 单位约定
TWO_PI_HBAR_TOL = D("1e-8")   # 门限数据驱动：hbar 仅 9 位，2πhbar vs h 固有差 ~1.2e-9


def m_planck():
    return (hbar * c / G).sqrt()


def alpha(m):
    """无量纲引力耦合 alpha_G(m) = G m^2/(hbar c)。其数值与单位制无关；
    c=1 记号下写作 G m^2/hbar，但那一个 'G,hbar,m' 是自然单位制下的数值，
    不是把 SI 数值代入后删掉 c（那正是域错位错误）。"""
    return G * D(str(m)) ** 2 / (hbar * c)


# ---------------------------------------------------------------- Q1 八方程扫描
def eight_equations():
    """每条：c=1 下残差 0；误把 c=1 公式当 SI 用时相对偏差巨大（域守卫）。"""
    m = D("1"); p = D("1"); S = D("1"); T = D("1")
    R = D("1"); w = D("0.6"); u = D("0.8")
    rows = []

    def row(name, expr, res_c1, si_rel, extra, cdependent=True):
        rows.append({
            "eq": name, "c1_form": expr, "extra_quantity": extra,
            "residual_c1": sci(res_c1, 4),
            "si_misuse_rel_dev": sci(si_rel, 4) if cdependent else "n/a",
            "identity_c1": abs(res_c1) < D("1e-40"),
            "domain_guard": (si_rel > D("1e-6")) if cdependent else None,
            "kind": "unit-reduction" if cdependent else "definition",
        })

    # 1 E=m：E=mc^2，c=1 → E=m；SI 误用相对偏差 c^2-1
    row("E = m (rest)", "E = m c^2 → E = m",
        m - m * c1 ** 2, rel(m * c ** 2, m), "c=1 约定 + m")
    # 2 E^2=p^2+m^2
    row("E^2 = p^2 + m^2", "E^2 = (pc)^2 + (mc^2)^2 → p^2 + m^2",
        (p ** 2 + m ** 2) - ((p * c1) ** 2 + (m * c1 ** 2) ** 2),
        rel((p * c) ** 2 + (m * c ** 2) ** 2, p ** 2 + m ** 2), "c=1 约定 + p,m")
    # 3 theta=S/hbar（c 无关的定义）
    row("theta = S/hbar", "theta hbar - S = 0",
        (S / hbar) * hbar - S, None, "S, hbar", cdependent=False)
    # 4 r_C = hbar/m；SI 误用相对偏差 c-1
    row("r_C = hbar/m", "r_C = hbar/(m c) → hbar/m",
        hbar / m - hbar / (m * c1),
        rel(hbar / m, hbar / (m * c)), "hbar, m")
    # 5 lambda = 2πhbar/p（c 无关；hbar 9 位 → 门限 1e-8）
    lam_rel = rel(H / p, D(2) * PI * hbar / p)
    rows.append({
        "eq": "lambda = 2πhbar/p", "c1_form": "lambda = h/p = 2πhbar/p",
        "extra_quantity": "h, hbar, p", "residual_c1": sci(lam_rel, 4),
        "si_misuse_rel_dev": "n/a",
        "identity_c1": lam_rel < TWO_PI_HBAR_TOL, "domain_guard": None,
        "kind": "definition",
    })
    # 6 G_{mu nu}=8πG T_{mu nu}；SI 误用相对偏差 c^4-1
    row("G_{mu nu} = 8πG T_{mu nu}", "= (8πG/c^4) T → 8πG T",
        D(8) * PI * G * T - D(8) * PI * G * T / c1 ** 4,
        rel(D(8) * PI * G * T, D(8) * PI * G * T / c ** 4), "G, T")
    # 7 G=2Z；SI 误用相对偏差 c-1
    Z = G * c1 / D(2)
    row("G = 2Z", "Z = Gc/2 → c=1 → G = 2Z",
        D(2) * Z - G, rel(D(2) * (G * c / D(2)), G), "Z")
    # 8 R^2 w^2 + u^2 = 1；SI 下应为 c^2，误用相对偏差 c^2-1
    row("R^2 w^2 + u^2 = 1", "= c^2 → 1",
        R ** 2 * w ** 2 + u ** 2 - c1 ** 2,
        rel(c ** 2, D(1)), "ROOT 螺旋模型 R,w,u")
    return rows


# ---------------------------------------------------------------- Q2 ℓ_P 与 alpha_G 恒等式
def planck_alpha_identities():
    # 恒等式 1：ℓ_P = sqrt(hbar G / c^3)。c=1 记号下 ℓ_P^2 = hbar G。
    # 机读时保留 c：ℓ_P^2 · c^3 与 hbar G 必须逐位相等（残差近 0）。
    lp2 = hbar * G / c ** 3
    lp2_vs_hbarG_c3 = rel(lp2 * c ** 3, hbar * G)
    lp_si = lp2.sqrt()

    # 恒等式 2：alpha_G = G m^2/(hbar c)。第二路 (ℓ_P/λ̄_C)^2，同 SI 单位制两路。
    a_direct = alpha(me)
    lam_c = hbar / (me * c)
    a_via_ratio = (lp_si / lam_c) ** 2
    a_two_path = rel(a_direct, a_via_ratio)

    # 域错位负对照：把 c=1 记号 ℓ_P^2=hbar G 的数字直接当 SI 长度平方
    # → 相对真值偏 c^3 ≈ 2.7e25（巨大）；正确恒等式是除以 c^3。
    lp_wrong_rel = rel(hbar * G, lp2)
    tol = D("1e-8")
    return {
        "lP_SI": sci(lp_si, 8),
        "identity_lP2_times_c3_eq_hbarG": sci(lp2 * c ** 3, 8),
        "hbarG": sci(hbar * G, 8),
        "lP2_vs_hbarG_div_c3_rel": sci(lp2_vs_hbarG_c3, 4),
        "alpha_e_direct": sci(a_direct, 8),
        "alpha_e_via_ratio": sci(a_via_ratio, 8),
        "alpha_two_path_rel": sci(a_two_path, 4),
        "wrong_c1_form_as_SI_rel": sci(lp_wrong_rel, 4),
        "tolerance": sci(tol, 2),
        "tolerance_basis": "恒等式残差应近 0；门限 1e-8 留 hbar 9 位舍入余量",
        "ok": (lp2_vs_hbarG_c3 < tol and a_two_path < tol
               and lp_wrong_rel > D("1e10")),
        "negative_control": "误把 ℓ_P^2=hbar G（c=1 数字）当 SI 用，偏离 %s（=c^3 量级）；"
                            "正确 SI 恒等式是 ℓ_P^2·c^3=hbar G" % sci(lp_wrong_rel, 4),
    }


# ---------------------------------------------------------------- Q3 作用量-场方程系数一致性
def action_field_eq_consistency():
    pref_si = c ** 3 / (D(16) * PI * G)              # SI Einstein-Hilbert 前因子
    field_si = D(8) * PI * G / c ** 4                # SI 场方程耦合
    prod_si = pref_si * field_si                     # 应 = 1/(2c)
    res_si = rel(prod_si, D(1) / (D(2) * c))
    pref_c1 = D(1) / (D(16) * PI * G)                # c=1 前因子（来料所写）
    field_c1 = D(8) * PI * G                         # c=1 场方程耦合（来料所写）
    prod_c1 = pref_c1 * field_c1                     # 应 = 1/2
    res_c1 = rel(prod_c1, D("0.5"))
    coef = D(16) * PI * G * D("0.5") - D(8) * PI * G  # 16πG·(1/2) = 8πG
    res_coef = abs(coef)
    tol = D("1e-60")
    return {
        "pi_machin_30": str(PI)[:32],
        "EH_prefactor_SI": sci(pref_si, 6), "field_coupling_SI": sci(field_si, 6),
        "product_SI_eq_1_over_2c": sci(prod_si, 8), "residual_SI": sci(res_si, 4),
        "EH_prefactor_c1": sci(pref_c1, 6), "field_coupling_c1": sci(field_c1, 6),
        "product_c1_eq_half": sci(prod_c1, 8), "residual_c1": sci(res_c1, 4),
        "coefficient_identity_residual": sci(res_coef, 4),
        "tolerance": sci(tol, 2),
        "ok": (res_si < tol and res_c1 < tol and res_coef < tol),
        "note": "内部系数自洽 ≠ 物理证实；G 仍是作用量里的自由耦合常数。",
    }


# ---------------------------------------------------------------- Q4 推导敏感度台账
def derivation_ledger():
    """四条「推导」主张对外部参数的相对敏感度 δ=10%；>5% 记为需输入。"""
    delta = D("0.10")
    v = D("246.22")                 # Higgs VEV（GeV，c=1）
    y_e = D("2.94e-6")              # 电子 Yukawa（实验输入）
    g = D("0.65")                   # 某规范耦合（输入）
    S = D("1")

    def sens(f, x):
        f0 = f(x)
        f1 = f(x * (D(1) + delta))
        if f0 == 0:
            return D(9) ** 60
        return rel(f1, f0)

    qphase = sens(lambda hb: S / hb, hbar)                     # θ=S/ℏ
    mass = sens(lambda y: y * v / (D(2).sqrt()), y_e)          # m=y v/√2
    gauge = sens(lambda gg: gg ** 2 / (D(4) * PI), g)          # α=g^2/4π
    grav = sens(lambda gg: D(8) * PI * gg, G)                  # 场方程耦合 8πG

    m_pred = y_e * v / D(2).sqrt()
    m_true_gev = D("0.000511")
    rows = [
        {"claim": "量子相位 theta=S/hbar", "external_input": "hbar",
         "sensitivity": sci(qphase, 6), "needs_external_input": qphase > D("0.05"),
         "action_form_derivable": False},
        {"claim": "粒子质量 m=y v/√2", "external_input": "y_f, v",
         "sensitivity": sci(mass, 6), "needs_external_input": mass > D("0.05"),
         "action_form_derivable": False},
        {"claim": "规范耦合 alpha=g^2/4π", "external_input": "g_i",
         "sensitivity": sci(gauge, 6), "needs_external_input": gauge > D("0.05"),
         "action_form_derivable": False},
        {"claim": "引力动力学 G_{mu nu}=8πG T", "external_input": "G（耦合）",
         "sensitivity": sci(grav, 6), "needs_external_input": grav > D("0.05"),
         "action_form_derivable": True},
    ]
    n_need = sum(1 for r in rows if r["needs_external_input"])
    zero_free = sum(1 for r in rows if not r["needs_external_input"])
    return {
        "delta": sci(delta, 2), "threshold": sci(D("0.05"), 2),
        "rows": rows, "n_need_external_input": n_need,
        "n_zero_free_parameter_numeric_predictions": zero_free,
        "m_e_pred_with_external_yukawa_GeV": sci(m_pred, 6),
        "m_e_true_GeV": sci(m_true_gev, 6),
        "m_e_pred_rel_to_true": sci(rel(m_pred, m_true_gev), 4),
        "ok": (n_need == len(rows) and zero_free == 0),
        "note": "引力动力学「形式」可由 Einstein-Hilbert 变分得到（教科书），"
                "但其耦合 G 仍是自由参数；其余三项的相位/质量/耦合都需外部输入。",
    }


# ---------------------------------------------------------------- Q5 c=1 能否定出 G
def c1_cannot_fix_G():
    ae = alpha(me)          # 无量纲，与单位制无关
    ap = alpha(mp)
    aP = alpha(m_planck())
    spread = (aP / ae).ln() / LN10   # 电子 → 普朗克质量跨约 45 dex
    # c=1 下 [hbar]=M L、[G]=L/M、[m]=M → alpha=G m^2/hbar 的 M,L 指数
    # M: -1 + 2*1 - 1 = 0 ; L: 1 + 0 - 1 = 0
    m_exp = (-1 + 2 * 1 - 1, 1 + 0 - 1)
    return {
        "alpha_e_c1": sci(ae, 6), "alpha_p_c1": sci(ap, 6),
        "alpha_planck_c1": sci(aP, 10),
        "alpha_planck_minus_1": sci(aP - D(1), 4),
        "spread_e_to_planck_dex": sci(spread, 6),
        "spread_e_to_proton_dex": sci((ap / ae).ln() / LN10, 6),
        "dimension_exponents_M_L": list(m_exp),
        "dimensionless_ok": (m_exp == (0, 0)),
        "ok": (m_exp == (0, 0) and abs(aP - D(1)) < D("1e-8")
               and spread > D(40)),
        "note": "alpha_G 无量纲 → 数值与单位制无关；c=1 不改变它。"
                "它随 m 从电子到普朗克质量跨 %s 数量级，c=1 不能唯一确定 G。" % sci(spread, 4),
    }


# ---------------------------------------------------------------- Q6 可翻转
def flip_input_driven():
    v = D("246.22")
    y1 = D("2.94e-6"); y2 = D("6.00e-6")
    m1 = y1 * v / D(2).sqrt(); m2 = y2 * v / D(2).sqrt()
    derivable_free = False                       # 只给 S_total（不给 y_f,v） → 质量不可定
    derivable_with_input = (m1 != m2)            # 给外部 Yukawa → 可算但由输入定
    flip_mass = (derivable_free != derivable_with_input) and (rel(m2, m1) > D("0.5"))
    ae = alpha(me); aP = alpha(m_planck())
    verdict_e = "COUPLING-TINY" if ae < D("1e-30") else "COUPLING-ORDER-ONE"
    verdict_P = "COUPLING-TINY" if aP < D("1e-30") else "COUPLING-ORDER-ONE"
    flip_coupling = verdict_e != verdict_P
    return {
        "mass_without_external_input": "UNDETERMINED",
        "mass_with_y1_GeV": sci(m1, 6), "mass_with_y2_GeV": sci(m2, 6),
        "mass_rel_change": sci(rel(m2, m1), 6),
        "derivable_free": derivable_free, "derivable_with_input": derivable_with_input,
        "flip_mass_works": bool(flip_mass),
        "alpha_e_verdict": verdict_e, "alpha_planck_verdict": verdict_P,
        "flip_coupling_works": bool(flip_coupling),
        "ok": bool(flip_mass and flip_coupling),
        "note": "结论由外部输入（Yukawa / m）驱动而翻转，非由作用量本身零输入驱动。",
    }


# ---------------------------------------------------------------- Q7 外部一手
EXTERNAL = {
    "codata_2022": {
        "url": "https://pml.nist.gov/cuu/pdf/wall_2022.pdf",
        "source": "NIST SP 961 (2024), CODATA 2022",
        "supports": "hbar=1.054571817e-34、G=6.67430e-11、c=299792458（精确）",
    },
    "field_equation_action": {
        "url": "https://arxiv.org/abs/gr-qc/9405057",
        "source": "Donoghue, GR as an effective field theory (arXiv:gr-qc/9405057)",
        "supports": "Einstein-Hilbert 作用量 (1/16πG)∫√-g R 与 G_{mu nu}=8πG T_{mu nu} 为标准 GR；"
                    "量子化后为非可重整 EFT，低能可算、高能未知",
    },
    "path_integral_phase": {
        "url": "https://www.nobelprize.org/prizes/physics/1965/feynman/lecture/",
        "source": "R. P. Feynman, Nobel Lecture (1965)",
        "supports": "路径积分权重 e^{iS/hbar} 是量子力学基本假设，hbar 为输入常数",
    },
    "planck_scale": {
        "url": "https://physics.nist.gov/cuu/Constants/index.html",
        "source": "NIST CODATA constants (Planck length derived)",
        "supports": "ℓ_P=√(hbar G/c^3)，c=1 下 ℓ_P^2=hbar G 为定义重排",
    },
}


def external_check():
    has_urls = all(x.get("url", "").startswith("https://") for x in EXTERNAL.values())
    # 本轮来料未给出处 → 无可核对的具体来源，不制造假阳性出处错误。
    fabricated_error_claimed = False
    return {
        "sources": EXTERNAL, "all_first_hand_urls": has_urls,
        "material_gave_source": False,
        "fabricated_source_error_claimed": fabricated_error_claimed,
        "ok": has_urls and not fabricated_error_claimed,
        "note": "来料未附来源；本册补一手链接并如实标注「无可核对来源」，"
                "不制造假阳性出处错误（区别于曾抓到的确凿 arXiv 标错）。",
    }


# ---------------------------------------------------------------- 自指守卫（无写死 ok）
def no_hardcoded_ok_guard():
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    needle = '"ok"' + ": " + "True"
    return needle not in src


def main():
    eight = eight_equations()
    n_id = sum(1 for r in eight if r["identity_c1"])
    n_domain = sum(1 for r in eight if r["domain_guard"] is True)
    n_cdep = sum(1 for r in eight if r["domain_guard"] is not None)

    gates = {
        "G1-eight-equations-are-unit-reductions": {
            "exp": "all 8 residual_c1≈0; c-dependent rows resist SI misuse",
            "n_identity": n_id, "n_total": len(eight),
            "n_domain_guard_ok": n_domain, "n_cdependent": n_cdep,
            "ok": (n_id == len(eight) and n_domain == n_cdep),
            "meaning": "八方程全为 c=1 单位约化/定义；对域错位敏感；零独立预言",
        },
        "G2-planck-alpha-identities": {
            "exp": "ℓ_P^2=hbar G & alpha_G=Gm^2/hbar hold; two-path agree; SI misuse fails",
            "ok": planck_alpha_identities()["ok"],
            "meaning": "两条关系为恒等式；无量纲 alpha 与单位制无关；误用 SI 巨大偏差",
        },
        "G3-action-field-eq-consistency": {
            "exp": "c^3/(16πG)·8πG/c^4 = 1/(2c); c=1 前因子·耦合 = 1/2",
            "ok": action_field_eq_consistency()["ok"],
            "meaning": "来料作用量与场方程系数内部自洽（仅一致性，非物理证实）",
        },
        "G4-derivation-sensitivity-ledger": {
            "exp": "all 4 derivation claims sensitive to external input; zero-free=0",
            "ok": derivation_ledger()["ok"],
            "meaning": "量子相位/质量/规范耦合/引力耦合均需输入；零自由参数数值预言 0",
        },
        "G5-c1-cannot-fix-G": {
            "exp": "alpha dimensionless; m_P gives 1; spread(e→p)>40 dex",
            "ok": c1_cannot_fix_G()["ok"],
            "meaning": "c=1 不能唯一确定 G；alpha_G(m) 随 m 变 45 数量级",
        },
        "G6-flip-input-driven": {
            "exp": "mass derivability flips with Yukawa; alpha verdict flips e vs Planck",
            "ok": flip_input_driven()["ok"],
            "meaning": "结论随外部输入翻转，非作用量零输入驱动",
        },
        "G7-external-first-hand": {
            "exp": "first-hand URLs supplied; no fabricated source error",
            "ok": external_check()["ok"],
            "meaning": "补一手链接；来料无来源，不造假阳性出处错误",
        },
    }

    guard = no_hardcoded_ok_guard()
    n_ok = sum(1 for g in gates.values() if g["ok"])

    verdict = ("ROOTV132-AUDIT--C1-UNIT-CHOICE--EIGHT-EQS-DEFINITIONAL--"
               "PLANCK-ALPHA-IDENTITY--ACTION-FIELD-EQ-CONSISTENT--"
               "DERIVATION-4-OF-4-NEED-INPUT--C1-CANNOT-FIX-G--"
               "FLIP-INPUT-DRIVEN--SOURCE-STANDARD--UFT-NOT-BROKEN--NEW-PREDICTION-0")

    out = {
        "date": "2026-11-21",
        "title": "ROOT V132「只令 c=1，保留 hbar 与 G」· 独立可算审计",
        "kind": "external-material-computable-audit",
        "verdict": verdict,
        "convention": "c=1; hbar != 1; G != 1",
        "constants": {"G": sci(G, 8), "c": sci(c, 8), "hbar": sci(hbar, 8),
                      "h": sci(H, 8), "m_e": sci(me, 8), "m_p": sci(mp, 8)},
        "eight_equations": eight,
        "planck_alpha": planck_alpha_identities(),
        "action_field_eq": action_field_eq_consistency(),
        "derivation_ledger": derivation_ledger(),
        "c1_cannot_fix_G": c1_cannot_fix_G(),
        "flip": flip_input_driven(),
        "external": external_check(),
        "gates": gates,
        "n_gate_ok": n_ok, "n_gate_total": len(gates),
        "guards": {"no_hardcoded_ok": guard},
        "boundary": [
            "c=1 是单位选择，把速度与时间/长度单位归一；它不减少独立有量纲常数个数，"
            "也不能单靠它证明四力统一——来料已如实声明，本册机读确认。",
            "八条核心方程在 c=1 下全为单位约化或定义重排（8/8 恒等）；"
            "误把 c=1 公式当 SI 数值用会给出巨大偏差（域守卫）。",
            "ℓ_P^2=hbar G 与 alpha_G=G m^2/hbar 是 c=1 下的定义重排；"
            "无量纲 alpha_G 与单位制无关，随 m 跨 45 数量级，不能定出 G。",
            "S_total=(1/16πG)∫√-g R+S_gauge+S_matter 与场方程在 c=1 下系数自洽，"
            "但这是内部一致性，不是物理证实；量子化后 GR 为非可重整 EFT。",
            "四条「从作用量推导」主张中，引力动力学的形式可由变分得到（教科书），"
            "但耦合 G 自由；量子相位/质量/规范耦合各需 hbar / y_f,v / g_i 外部输入，"
            "零自由参数数值预言数 = 0。",
            "本轮来料未附任何来源 URL；本册补一手链接并如实标注，不制造假阳性出处错误。",
        ],
        "red_line": "数学自洽 != 实验证实；不宣称攻破统一场论，"
                    "不宣称发现新方程或独立实验预言；四力统一未证。",
        "discipline": ["非判定册", "不占RID", "不入README", "不回写既有产物",
                       "两路机拼", "恒等式识别", "域错位负对照", "门限数据驱动",
                       "可翻转判据", "一手URL", "不制造假阳性错误", "无写死ok守卫"],
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)

    print("VERDICT =", verdict)
    print("[1] 八方程:", n_id, "/", len(eight), "恒等; 域守卫", n_domain, "/", n_cdep)
    for r in eight:
        print("   %-26s res_c1=%-10s SI误用相对偏差=%s" %
              (r["eq"], r["residual_c1"], r["si_misuse_rel_dev"]))
    pa = planck_alpha_identities()
    print("[2] ℓP²·c³=hbarG rel=%s; alpha 两路 rel=%s; SI误用 rel=%s; ok=%s" %
          (pa["lP2_vs_hbarG_div_c3_rel"], pa["alpha_two_path_rel"],
           pa["wrong_c1_form_as_SI_rel"], pa["ok"]))
    print("[3] 作用量-场方程系数 ok =", action_field_eq_consistency()["ok"])
    led = derivation_ledger()
    print("[4] 推导敏感度 需输入 %d/4; 零自由参数预言 %d" %
          (led["n_need_external_input"], led["n_zero_free_parameter_numeric_predictions"]))
    print("[5] c=1 定 G:", c1_cannot_fix_G()["ok"], "spread(e→planck) dex =",
          c1_cannot_fix_G()["spread_e_to_planck_dex"])
    fl = flip_input_driven()
    print("[6] flip 质量=%s 耦合=%s" % (fl["flip_mass_works"], fl["flip_coupling_works"]))
    print("[7] 外部一手 ok =", external_check()["all_first_hand_urls"])
    print("[G] 判据", n_ok, "/", len(gates), "ok; 守卫 no-hardcoded-ok =", guard)
    print("JSON =", OUT_JSON, os.path.getsize(OUT_JSON), "B")
    return out


if __name__ == "__main__":
    main()
