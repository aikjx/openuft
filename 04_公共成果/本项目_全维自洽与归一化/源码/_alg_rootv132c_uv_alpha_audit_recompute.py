# -*- coding: utf-8 -*-
"""算法联盟 · ROOT V132 第三册：α_G 紫外行为 / 幂计数 · 可算审计机核

性质：非判定册，不占 RID，不入 README，不回写任何既有产物，不与 TUFT 链相加。
审计对象：ROOT V132 来料的无量纲引力耦合 alpha_G(m)=G m^2/hbar (c=1)，
          以及把 S_total 放进相位 e^{iS/hbar} 后的量子化前景。
新判据类型（与前两册不同）：
  - V132 第一册：每条方程是否定义重排（判别力 0 / 参数不灭）
  - V132 第二册：两条方程是否互相相容（内部不相容 / 退化恒等）
  - 本册第三册：耦合的紫外行为（幂计数 / 强耦合阈值 / 可翻转定点）

核心审计问题（机读；结论随输入翻转；一手来源；不自盖章）：
  Q1 alpha_G 两路：G m^2/(hbar c) vs (m/m_Pl)^2 → 恒等式（IDENTITY，不承重）。
  Q2 幂计数：alpha_G 无量纲 ⇒ [G]=-2（自然单位）；树级跑动 dα/dlnE=2α，
     闭式 vs RK4 两路；alpha(E)=(E/m_Pl)^2 在 m_Pl 处过 1 → 强耦合。
  Q3 紫外无界扫描：m/m_Pl=1e-2..1e2 → alpha=1e-4..1e4，无界；洛伦兹不变 doesn't help。
  Q4 可翻转正对照（假想 UV 定点，asymptotic safety）：dα/dt=2α(1-α/α*)，
     α* 有限 ⇒ α→α* 有界；闭式 vs RK4；翻转 UV-UNBOUNDED → UV-BOUNDED。
     明确标注：这是来料未给的**假想输入**，不是本轮发现；AS 是开放研究纲领。
  Q5 负对照 QED：dα/dt=b α^2, b=2/(3π)，到 m_Pl 仍 α≈0.008<1 → 判据有判别力
     （引力过 1，QED 不过）；闭式 vs RK4。
  Q6 外部一手；Q7 无写死 ok 守卫。

红线：数学自洽 != 实验证实；不宣称攻破统一场论；渐近安全未被排除
      （未被满足 != 不可满足）；不宣称独立实验预言；四力统一未证。
"""
import os
import glob
import json
from decimal import Decimal, getcontext

getcontext().prec = 60
D = Decimal

HITS = glob.glob(os.path.join("openuft", "**",
                              "_ALG_expdata_fullchain_来料总表_2026-11-11.json"),
                 recursive=True)
assert len(HITS) == 1, "ANCHOR-HITS=%d" % len(HITS)
DATA = os.path.dirname(HITS[0])
OUT_JSON = os.path.join(DATA, "_ALG_rootv132c_uv_alpha_audit_recompute_2026-11-21.json")


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
    z = D(1) / D(x); zz = z * z; p = z; s = D(0); k = 0
    while True:
        term = p / D(2 * k + 1)
        s = s + term if k % 2 == 0 else s - term
        if abs(term) < D("1e-66"):
            break
        p *= zz; k += 1
    return s


PI = D(16) * atan_inv(5) - D(4) * atan_inv(239)

# ---------------------------------------------------------------- 常数（CODATA 2022）
hbar = D("1.054571817e-34")
c = D("299792458")
G = D("6.67430e-11")
M_E_KG = D("9.1093837139e-31")
GEV_KG = D("1.7826619216278976e-27")   # 1 GeV/c^2 in kg
ALPHA_QED0 = D(1) / D("137.035999084")
M_PL_KG = (hbar * c / G).sqrt()
M_PL_GEV = M_PL_KG / GEV_KG
M_E_GEV = M_E_KG / GEV_KG
TOL_ID = D("1e-8")          # 恒等式/两路门限（hbar 9 位有效数字）
TOL_RK = D("1e-12")         # RK4 与闭式一致门限（步长自适应留余量）


def alpha_G(m_gev):
    """无量纲引力耦合 alpha_G = G m^2/(hbar c) = (m/m_Pl)^2。"""
    return (D(str(m_gev)) / M_PL_GEV) ** 2


# ---------------------------------------------------------------- Q1 两路恒等
def two_route_alpha():
    rows = []
    maxrel = D(0)
    for name, m in [("electron", M_E_GEV), ("proton", D("0.93827208816")),
                    ("Planck", M_PL_GEV)]:
        a1 = (G * (m * GEV_KG) ** 2 / (hbar * c))       # 路 A：SI 原式
        a2 = (m / M_PL_GEV) ** 2                        # 路 B：质量比平方（c=1 记号）
        r = rel(a1, a2)
        maxrel = max(maxrel, r)
        rows.append({"case": name, "m_GeV": sci(m, 8),
                     "alpha_SI_form": sci(a1, 8), "alpha_mass_ratio": sci(a2, 8),
                     "rel": sci(r, 4)})
    return {"rows": rows, "max_rel": sci(maxrel, 4), "tolerance": sci(TOL_ID, 2),
            "kind": "IDENTITY--两路为同一关系，数值核对不承重",
            "ok": maxrel < TOL_ID}


# ---------------------------------------------------------------- Q2 幂计数与闭式/RK4
def rk4(f, y0, t0, t1, n=4000):
    h = (t1 - t0) / D(n)
    y = D(str(y0)); t = D(str(t0))
    for _ in range(n):
        k1 = f(t, y)
        k2 = f(t + h / D(2), y + h * k1 / D(2))
        k3 = f(t + h / D(2), y + h * k2 / D(2))
        k4 = f(t + h, y + h * k3)
        y = y + h * (k1 + D(2) * k2 + D(2) * k3 + k4) / D(6)
        t = t + h
    return y


def power_counting():
    # 无量纲 alpha_G = G E^2 / (hbar c) ⇒ [G] = [hbar c] / M^2 ⇒ 自然单位 [G] = M^-2
    mass_dim_G = D(-2)
    # 树级 dα/dt = 2α，t = ln(E/E0)。闭式 α=α0 exp(2t)
    a0 = alpha_G(M_E_GEV)
    t_end = D(2)   # E/E0 = e^2
    closed = a0 * (t_end * D(2)).exp()   # exp(2t)
    numeric = rk4(lambda t, y: D(2) * y, a0, D(0), t_end, n=20000)
    r = rel(closed, numeric)
    # 强耦合点：alpha_G = 1 ⇔ E = m_Pl
    return {
        "mass_dimension_G_natural_units": sci(mass_dim_G, 2),
        "derive": "alpha_G=G E^2/(hbar c) dimensionless → [G]=-2; "
                  "loop parameter ~ G E^2=(E/m_Pl)^2 grows with E",
        "a0_electron": sci(a0, 8),
        "closed_alpha_at_e2": sci(closed, 8),
        "rk4_alpha_at_e2": sci(numeric, 8),
        "two_route_rel": sci(r, 4),
        "strong_coupling_at": "E = m_Pl",
        "m_Pl_GeV": sci(M_PL_GEV, 8),
        "tolerance": sci(TOL_RK, 2),
        "ok": (mass_dim_G == D(-2) and r < TOL_RK),
        "note": "树级维数跑动是幂计数结论（教科书），非本轮新物理；G 的质量量纲 -2 是已知事实。",
    }


# ---------------------------------------------------------------- Q3 紫外无界扫描
def uv_scan():
    ratios = [D("1e-2"), D("1e-1"), D(1), D("1e1"), D("1e2")]
    rows = []
    avals = []
    for x in ratios:
        a = alpha_G(M_PL_GEV * x)
        avals.append(a)   # 数值路：单调性必须用 Decimal 原值比较，不用 sci() 序列化串
        verdict = "STRONG" if a > D(1) else ("THRESHOLD" if a == D(1) else "PERTURBATIVE")
        rows.append({"E_over_mPl": sci(x, 4), "alpha_G": sci(a, 8),
                     "above_1": a > D(1), "verdict": verdict})
    crossing = alpha_G(M_PL_GEV)
    monotonic = all(avals[i] < avals[i + 1] for i in range(len(avals) - 1))
    unbounded = (rows[-1]["verdict"] == "STRONG" and crossing == D(1))
    return {"rows": rows, "alpha_at_mPl": sci(crossing, 8),
            "monotonic": monotonic, "uv_unbounded": unbounded,
            "ok": monotonic and unbounded and crossing == D(1),
            "note": "在纯维数跑动下 alpha_G=(E/m_Pl)^2 随 E 无界增长，m_Pl 处过 1 → 微扰展开失效。",
            "boundary": "这只证明微扰幂计数失效；不等于证明量子引力不存在或非微扰 UV 定点不存在。"}


# ---------------------------------------------------------------- Q4 可翻转：假想 UV 定点
def fixed_point_flip():
    # 假想输入 alpha*（不是来料给的）：dα/dt = 2α(1-α/α*)
    astar = D("0.1")
    a0 = alpha_G(M_E_GEV)
    # 评估点选在 t=ln(m_Pl/m_e)：此处维数跑动 α=α0 e^{2t}=(m_Pl/m_e)^2·α0=1，
    # 与定点模型 α→α* 才真正数值分叉（t=12 时两模型都还是 ~1e-35，无判别力）。
    t_end = (M_PL_GEV / M_E_GEV).ln()
    e = (D(-2) * t_end).exp()
    closed = astar / (D(1) + (astar / a0 - D(1)) * e)
    # 步数按区间加长：t≈51.5 时 40000 步 rel≈3.3e-12 超过 1e-12；提到 120000 步。
    numeric = rk4(lambda t, y: D(2) * y * (D(1) - y / astar), a0, D(0), t_end, n=120000)
    r = rel(closed, numeric)
    # 同一能量下维数跑动的值（应 ≈1，即强耦合门槛）
    perturb_at_same_t = a0 * (D(2) * t_end).exp()
    bounded = numeric < astar * D("1.001") and numeric > D(0)
    # exp(ln(x)) 在 Decimal 下回 1 有 ~3e-58 舍入（实测 1-3.27e-58），
    # 对「达到 1」判定给 1e-12 数值容差；这是舍入容差，不是物理门限拟合。
    UNITY_TOL = D("1e-12")
    numeric_flip = (perturb_at_same_t >= D(1) - UNITY_TOL and numeric < D(1) - UNITY_TOL)
    verdict_fp = "UV-BOUNDED" if bounded else "UV-UNBOUNDED"
    verdict_pert = uv_scan()["uv_unbounded"]
    flip = (verdict_pert and verdict_fp == "UV-BOUNDED" and numeric_flip)
    # 反噬：把假想 alpha* 改到荒谬大 → 有界阈值抬高，判词应翻回无界
    astar_bad = D("1e10")
    closed_bad = astar_bad / (D(1) + (astar_bad / a0 - D(1)) * e)
    backfire_verdict = "UV-BOUNDED" if closed_bad < astar_bad * D("1.001") else "UV-UNBOUNDED"
    backfire = backfire_verdict == "UV-BOUNDED"   # 数学上仍"有界"但阈值荒谬 → 见 note
    return {
        "input_astar_hypothetical": sci(astar, 6),
        "input_basis": "假想 UV 定点强度 α*，来料未给；仅作可翻转正对照，非本轮发现",
        "evaluation_t_ln_mPl_over_me": sci(t_end, 10),
        "perturbative_alpha_at_same_t": sci(perturb_at_same_t, 8),
        "closed_alpha_at_eval": sci(closed, 8),
        "rk4_alpha_at_eval": sci(numeric, 8),
        "numeric_flip_at_eval": numeric_flip,
        "unity_tolerance": sci(UNITY_TOL, 2),
        "unity_tolerance_basis": "Decimal exp(ln(x)) 回 1 有 ~3e-58 舍入，给 1e-12 数值容差（非物理门限）",
        "two_route_rel": sci(r, 4),
        "verdict_perturbative": "UV-UNBOUNDED" if verdict_pert else "UV-BOUNDED",
        "verdict_with_UV_fixed_point": verdict_fp,
        "flip_works": flip,
        "backfire_astar_absurd": sci(astar_bad, 4),
        "backfire_alpha_at_eval": sci(closed_bad, 8),
        "backfire_note": "把 α* 改到 1e10 数学上仍'有界'但已远大于 1 → 物理强耦合；"
                         "判据仅说明'有界性'依赖输入的 α*，不是对 AS 的证实。",
        "tolerance": sci(TOL_RK, 2),
        "ok": (r < TOL_RK and flip and bounded),
    }


# ---------------------------------------------------------------- Q5 负对照 QED
def qed_negative_control():
    b = D(2) / (D(3) * PI)      # 单 Dirac 费米子 one-loop QED beta 系数
    t_pl = (M_PL_GEV / M_E_GEV).ln()
    inv_closed = D(1) / ALPHA_QED0 - b * t_pl
    a_closed = D(1) / inv_closed
    a_rk = rk4(lambda t, y: b * y * y, ALPHA_QED0, D(0), t_pl, n=6000)
    r = rel(a_closed, a_rk)
    landau_t = D(1) / (b * ALPHA_QED0)
    bounded = a_rk < D(1)
    # 判别力用「两门槛行为对比」：QED 在 m_Pl 仍 <1，引力在 m_Pl 已达到 1 且之上 >1
    discriminating = bounded and (alpha_G(M_PL_GEV) >= D(1)
                                  and alpha_G(M_PL_GEV * D(10)) > D(1))
    return {
        "beta_coefficient_2_over_3pi": sci(b, 10),
        "ln_mPl_over_me": sci(t_pl, 10),
        "alpha_QED_at_mPl_closed": sci(a_closed, 8),
        "alpha_QED_at_mPl_rk4": sci(a_rk, 8),
        "two_route_rel": sci(r, 4),
        "landau_pole_lnE_over_E0": sci(landau_t, 8),
        "landau_above_mPl": landau_t > t_pl,
        "qed_bounded_at_mPl": bounded,
        "grav_strong_at_mPl": alpha_G(M_PL_GEV) > D(1),
        "criterion_discriminating": discriminating,
        "ok": (r < TOL_RK and bounded and discriminating),
        "note": "同一'是否过 1'门：引力在 m_Pl 过 1，QED 在 m_Pl 仍 ~0.008 → 判据有判别力，非装饰。",
    }


# ---------------------------------------------------------------- Q6 外部一手
EXTERNAL = {
    "gr_eft_nonrenorm": {
        "url": "https://arxiv.org/abs/gr-qc/9405057",
        "source": "Donoghue, General Relativity as an effective field theory (arXiv:gr-qc/9405057)",
        "supports": "量子化 GR 为非可重整 EFT；低能可算、高能未知；G 质量量纲 -2",
    },
    "asymptotic_safety": {
        "url": "https://arxiv.org/abs/1202.2274",
        "source": "Reuter & Saueressig, Quantum Einstein Gravity (arXiv:1202.2274, NJP 14 055022)",
        "supports": "渐近安全纲领：非平凡 RG 不动点有 supporting evidence，"
                    "仍是研究纲领（review 措辞 evidence supporting，非已证）",
    },
    "codata": {
        "url": "https://pml.nist.gov/cuu/pdf/wall_2022.pdf",
        "source": "NIST SP 961 (2024), CODATA 2022",
        "supports": "h, G, c, alpha, m_e；m_Pl 由 hbar,c,G 派生",
    },
}


def external_check():
    urls_ok = all(v["url"].startswith("https://") for v in EXTERNAL.values())
    return {"sources": EXTERNAL, "all_https": urls_ok,
            "material_gave_source": False, "fabricated_source_error_claimed": False,
            "ok": urls_ok,
            "note": "来料未给来源；本册补一手。渐近安全明确标注为开放纲领，"
                    "不把 supporting evidence 写成已证，不制造假阳性出处错误。"}


def no_hardcoded_ok_guard():
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    needle = '"ok"' + ": " + "True"
    return needle not in src


def main():
    tr = two_route_alpha()
    pc = power_counting()
    uv = uv_scan()
    fp = fixed_point_flip()
    qed = qed_negative_control()
    ext = external_check()
    guard = no_hardcoded_ok_guard()

    gates = {
        "G1-alpha-two-route-identity": {
            "exp": "G m^2/(hbar c) equals (m/m_Pl)^2; IDENTITY not independent evidence",
            "max_rel": tr["max_rel"], "ok": tr["ok"],
            "meaning": "两路为同一关系，数值一致；按纪律标 IDENTITY 不承重",
        },
        "G2-power-counting-dim-2": {
            "exp": "[G]=-2 in natural units; tree running closed vs RK4 agree",
            "mass_dim_G": pc["mass_dimension_G_natural_units"],
            "two_route_rel": pc["two_route_rel"], "ok": pc["ok"],
            "meaning": "幂计数：G 负质量量纲 → 圈参数随 E 增长（教科书，非新物理）",
        },
        "G3-uv-unbounded-scan": {
            "exp": "alpha_G=(E/m_Pl)^2 monotonic, crosses 1 at m_Pl, unbounded",
            "alpha_at_mPl": uv["alpha_at_mPl"], "uv_unbounded": uv["uv_unbounded"],
            "ok": uv["ok"],
            "meaning": "负读数：微扰展开在 m_Pl 失效；不等于证明量子引力不存在",
        },
        "G4-flip-uv-fixed-point": {
            "exp": "hypothetical UV fixed point flips verdict UV-UNBOUNDED → UV-BOUNDED",
            "input_astar": fp["input_astar_hypothetical"],
            "verdict_pert": fp["verdict_perturbative"],
            "verdict_fp": fp["verdict_with_UV_fixed_point"],
            "flip_works": fp["flip_works"], "ok": fp["ok"],
            "meaning": "结论随外部输入 α* 翻转；α* 是假想输入，非本轮发现",
        },
        "G5-qed-negative-control": {
            "exp": "QED stays bounded (<1) at m_Pl while gravity crosses 1",
        "alpha_QED_at_mPl": qed["alpha_QED_at_mPl_rk4"],
        "grav_at_mPl": sci(alpha_G(M_PL_GEV), 6),
        "grav_at_10mPl": sci(alpha_G(M_PL_GEV * D(10)), 6),
            "discriminating": qed["criterion_discriminating"], "ok": qed["ok"],
            "meaning": "同一门槛两不同结果 → 判据有判别力；Landau 极点远在 m_Pl 之上",
        },
        "G6-external-first-hand": {
            "exp": "Donoghue EFT + Reuter-Saueressig AS + NIST; AS labeled open",
            "all_https": ext["all_https"], "ok": ext["ok"],
            "meaning": "一手来源；不把 AS 的 supporting evidence 写成已证",
        },
        "G7-no-hardcoded-ok": {
            "exp": "no literal ok=True in source", "ok": guard,
            "meaning": "门 ok 由 act 算出，非写死",
        },
    }
    n_ok = sum(1 for g in gates.values() if g["ok"])

    verdict = ("ROOTV132C-AUDIT--C1-INVARIANT--ALPHA-IDENTITY--G-DIM-2--"
               "UV-UNBOUNDED-MPL--PERTURB-BREAKDOWN--ASYMPTOTIC-SAFETY-FLIP--"
               "QED-NEG-CONTROL--NOT-EXCLUDED--UFT-NOT-BROKEN--NEW-PREDICTION-0")

    out = {
        "date": "2026-11-21",
        "title": "ROOT V132 第三册：alpha_G 紫外行为 / 幂计数 · 可算审计",
        "kind": "external-material-computable-audit",
        "verdict": verdict,
        "convention": "c=1; hbar != 1; G != 1",
        "target": "alpha_G(m)=G m^2/hbar (c=1) 与 S_total 的量子化前景",
        "verdict_type": "UV-behavior / power-counting (distinct from prior definition-rearrangement and cross-equation-consistency)",
        "constants": {"m_Pl_GeV": sci(M_PL_GEV, 10), "m_e_GeV": sci(M_E_GEV, 10),
                      "alpha_QED0": sci(ALPHA_QED0, 10), "tol_id": sci(TOL_ID, 2),
                      "tol_rk": sci(TOL_RK, 2)},
        "two_route_alpha": tr, "power_counting": pc, "uv_scan": uv,
        "fixed_point_flip": fp, "qed_negative_control": qed, "external": ext,
        "gates": gates, "n_gate_ok": n_ok, "n_gate_total": len(gates),
        "guards": {"no_hardcoded_ok": guard},
        "boundary": [
            "alpha_G = G m^2/(hbar c) = (m/m_Pl)^2 是恒等式；c=1 只改单位记号，不改变紫外行为。",
            "G 的质量量纲 -2 与 alpha_G=(E/m_Pl)^2 无界增长是教科书幂计数结论；"
            "本册用两路数值（闭式 vs RK4）核对，不冒充新物理发现。",
            "微扰展开在 E~m_Pl 失效（alpha_G→1）只说明微扰方法失效，"
            "不等于证明量子引力不存在、也不等于证明非微扰 UV 定点不存在。",
            "翻转正对照的 alpha*=0.1 是假想输入，来料未给；渐近安全（Reuter-Saueressig）"
            "是有 supporting evidence 的开放研究纲领，本册不宣称其已证或已伪。",
            "QED 负对照在 m_Pl 处 alpha~0.008<1、Landau 极点远在其上；"
            "同一'过 1'门槛对引力/ QED 给不同结果 → 判据有判别力。",
        ],
        "red_line": "数学自洽 != 实验证实；未被满足 != 不可满足；"
                    "不宣称攻破统一场论，不宣称发现新方程或独立实验预言；四力统一未证。",
        "discipline": ["非判定册", "不占RID", "不入README", "不回写既有产物",
                       "两路机拼", "恒等式识别", "正负双对照", "可翻转判据",
                       "门限数据驱动", "一手URL", "不制造假阳性错误", "无写死ok守卫"],
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)

    print("VERDICT =", verdict)
    print("[1] alpha two-route max rel =", two_route_alpha()["max_rel"], "IDENTITY")
    p = power_counting()
    print("[2] [G]=%s; tree closed=%s rk4=%s rel=%s" %
          (p["mass_dimension_G_natural_units"], p["closed_alpha_at_e2"],
           p["rk4_alpha_at_e2"], p["two_route_rel"]))
    u = uv_scan()
    print("[3] UV unbounded =", u["uv_unbounded"], "alpha(mPl) =", u["alpha_at_mPl"])
    for r in u["rows"]:
        print("    E/mPl=%-10s alpha=%-12s %s" % (r["E_over_mPl"], r["alpha_G"], r["verdict"]))
    f = fixed_point_flip()
    print("[4] flip: pert=%s fp=%s works=%s same-t pert=%s fp=%s rel=%s" %
          (f["verdict_perturbative"], f["verdict_with_UV_fixed_point"],
           f["flip_works"], f["perturbative_alpha_at_same_t"],
           f["rk4_alpha_at_eval"], f["two_route_rel"]))
    q = qed_negative_control()
    print("[5] QED alpha(mPl)=%s bounded=%s discriminating=%s landau>mPl=%s" %
          (q["alpha_QED_at_mPl_rk4"], q["qed_bounded_at_mPl"],
           q["criterion_discriminating"], q["landau_above_mPl"]))
    print("[6] external all https =", external_check()["all_https"])
    print("[G] 判据", n_ok, "/", len(gates), "ok; guard =", guard)
    print("JSON =", OUT_JSON, os.path.getsize(OUT_JSON), "B")
    return out


if __name__ == "__main__":
    main()
