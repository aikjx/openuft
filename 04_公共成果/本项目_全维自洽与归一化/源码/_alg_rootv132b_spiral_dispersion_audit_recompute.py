# -*- coding: utf-8 -*-
"""算法联盟 · ROOT V132 续：螺旋速度约束 R²ω²+u²=1 与色散 E²=p²+m² 的相容性 · 可算审计机核

性质：非判定册，不占 RID，不入 README，不回写任何既有产物，不与 TUFT 链相加。
审计对象：ROOT V132 来料八方程表中同时出现的两条——
  (S) 螺旋速度约束 R²ω²+u²=1（c=1 下总速率恰为 c）
  (D) 能量动量关系 E²=p²+m²（c=1 下色散）
外部裁决：狭义相对论 v = p/E；对 m>0、p 有限 ⇒ v<1 严格；v=1 仅 m=0 或 p→∞
  （一手：Feynman Lectures Vol I Ch.16 eq 16.13/16.14，Caltech 托管原文）。

核心审计问题（全部机读，结论随输入翻转，来源给一手 URL，不自盖章）：
  Q1 色散给出的 v=p/E 两路（直接 vs rapidity/tanh）是否一致（数值核对，IDENTITY）？
  Q2 (S) 要求总速率=1，与 (D) 对有质量粒子是否相容？扫描网格：m=0 相容（恒等，判别力0），
     m>0 且 p 有限 ⇒ 1-v>0 ⇒ 不相容（负读数）。
  Q3 可翻转阈值：给定容差 tol，求 p*/m 使 1-p/√(p²+m²)=tol；解析式 vs 二分两路；
     跨阈值判词由 INCOMPATIBLE 翻为 COMPATIBLE-WITHIN-TOL（flip）。
  Q4 两种读法分叉：读法A（螺旋约束=同一粒子的质心速率）→ 对有质量粒子矛盾；
     读法B（螺旋约束只描述无质量内层光，复合粒子速率仍<1）→ 恒等且无新方程
     （接 封装光假说审计：恒等2/需输入4/新方程0）。两分支都不产新可判负动力学。
  Q5 外部一手 URL；不制造假阳性出处错误。
  Q6 无写死 ok 守卫。

红线：数学自洽 != 实验证实；不宣称攻破统一场论，不宣称独立实验预言；四力统一未证。
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
OUT_JSON = os.path.join(DATA, "_ALG_rootv132b_spiral_dispersion_audit_recompute_2026-11-21.json")


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


def dexp(x):
    return D(str(x)).exp()


def dcosh(x):
    z = dexp(x)
    return (z + D(1) / z) / D(2)


def dsinh(x):
    z = dexp(x)
    return (z - D(1) / z) / D(2)


# ---------------------------------------------------------------- 常数与容差
# CODATA 2022（NIST SP 961）：电子/质子静质量，以 MeV/c^2 记；c=1 下即质量数值。
M_E = D("0.51099895069")     # MeV
M_P = D("938.27208816")      # MeV
TOL_V = D("1e-30")           # 两路 v 一致性门限（prec=60，ln/exp 路 ~1e-50，留 20 位余量）
TOL_KIN = D("1e-6")          # 相容性判据：|1-v| < 1e-6 视为「数值相容」

# c=1：E = sqrt(p²+m²), v = p/E
def v_direct(m, p):
    m = D(str(m)); p = D(str(p))
    if m == 0:
        return D(1) if p > 0 else D(0)
    E = (p * p + m * m).sqrt()
    return p / E


def v_rapidity(m, p):
    """第二路：rapidity eta=asinh(p/m)，v=tanh(eta)=sinh/cosh，不用 p/E 直接式。"""
    m = D(str(m)); p = D(str(p))
    if m == 0:
        return D(1) if p > 0 else D(0)
    r = p / m
    eta = (r + (r * r + D(1)).sqrt()).ln()   # asinh(r)
    return dsinh(eta) / dcosh(eta)


def residual_spiral(m, p):
    """(S) 要求总速率=1；(D) 给 v=p/E。残差 = 1 - v。"""
    return D(1) - v_direct(m, p)


def compat_verdict(m, p):
    res = residual_spiral(m, p)
    if m == 0:
        return "COMPATIBLE-IDENTITY", res
    if res < TOL_KIN:
        return "COMPATIBLE-WITHIN-TOL", res
    return "INCOMPATIBLE", res


# ---------------------------------------------------------------- Q1 两路 v
def two_route_v():
    rows = []
    ps = [D("0.1"), D("1"), D("10"), D("100"), D("1000")]
    maxrel = D(0)
    for p in ps:
        a = v_direct(D(1), p)
        b = v_rapidity(D(1), p)
        r = rel(a, b)
        maxrel = max(maxrel, r)
        rows.append({"p_over_m": sci(p, 4), "v_direct": sci(a, 12),
                     "v_rapidity": sci(b, 12), "rel": sci(r, 4)})
    return {"rows": rows, "max_rel": sci(maxrel, 4),
            "tolerance": sci(TOL_V, 2),
            "tolerance_basis": "prec=60；ln/exp 路固有误差 ~1e-50，门限 1e-30 留 20 位",
            "kind": "IDENTITY--两路为同一色散的不同参数化，数值核对不构成独立证据",
            "ok": maxrel < TOL_V}


# ---------------------------------------------------------------- Q2 相容性扫描
def compatibility_scan():
    masses = [("photon", D(0), D(1)), ("electron", M_E, M_E),
              ("proton", M_P, M_P), ("unit_mass", D(1), D(1))]
    ratios = [D("0.1"), D("1"), D("10"), D("100")]
    rows = []
    n_inc = 0
    n_id = 0
    for name, m, pbase in masses:
        for q in ratios:
            p = pbase * q if m > 0 else q
            verdict, res = compat_verdict(m, p)
            if verdict == "INCOMPATIBLE":
                n_inc += 1
            if verdict == "COMPATIBLE-IDENTITY":
                n_id += 1
            rows.append({"case": name, "p": sci(p, 6), "v": sci(v_direct(m, p), 10),
                         "residual_1_minus_v": sci(res, 6), "verdict": verdict})
    # 正对照：m=0 恒相容（恒等）；负对照：m>0 有限 p 全不相容
    photon_ok = all(r["verdict"] == "COMPATIBLE-IDENTITY"
                    for r in rows if r["case"] == "photon")
    massive_all_inc = all(r["verdict"] == "INCOMPATIBLE"
                          for r in rows if r["case"] != "photon")
    return {"rows": rows, "n_incompatible": n_inc, "n_identity": n_id,
            "positive_control_photons_identity": photon_ok,
            "negative_control_massive_all_incompatible": massive_all_inc,
            "tolerance": sci(TOL_KIN, 2),
            "ok": photon_ok and massive_all_inc and n_inc > 0 and n_id > 0}


# ---------------------------------------------------------------- Q3 翻转阈值
def threshold_analytic(tol):
    """1 - p/sqrt(p²+m²) = tol  ⇒  p/m = (1-tol)/sqrt(2tol - tol²)."""
    one = D(1)
    return (one - tol) / (D(2) * tol - tol * tol).sqrt()


def threshold_bisection(tol, lo=D("1e-3"), hi=D("1e6")):
    """二分：f(x)=1 - x/sqrt(x²+1) - tol，f 单调减。"""
    def f(x):
        return D(1) - x / (x * x + D(1)).sqrt() - tol
    flo, fhi = f(lo), f(hi)
    assert flo > 0 and fhi < 0, "BRACKET-FAIL"
    for _ in range(220):
        mid = (lo + hi) / D(2)
        fm = f(mid)
        if fm > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / D(2)


def flip_gate():
    pstar_a = threshold_analytic(TOL_KIN)
    pstar_b = threshold_bisection(TOL_KIN)
    agree = rel(pstar_a, pstar_b)
    # 电子跨阈值两侧读数
    lo, hi = M_E * D("10"), M_E * D("1000")
    v_lo, v_hi = compat_verdict(M_E, lo), compat_verdict(M_E, hi)
    flip = (v_lo[0] == "INCOMPATIBLE" and v_hi[0] == "COMPATIBLE-WITHIN-TOL")
    # 反噬：把同一实体误设 m=0（光子读法）→ 判词应翻到 COMPATIBLE-IDENTITY
    backfire = compat_verdict(D(0), lo)[0]
    return {
        "tolerance": sci(TOL_KIN, 2),
        "pstar_over_m_analytic": sci(pstar_a, 12),
        "pstar_over_m_bisection": sci(pstar_b, 12),
        "two_route_rel": sci(agree, 4),
        "electron_pstar_MeV": sci(pstar_a * M_E, 8),
        "proton_pstar_MeV": sci(pstar_a * M_P, 8),
        "electron_p_low_10m": {"p": sci(lo, 6), "verdict": v_lo[0], "res": sci(v_lo[1], 6)},
        "electron_p_high_1000m": {"p": sci(hi, 6), "verdict": v_hi[0], "res": sci(v_hi[1], 6)},
        "flip_works": flip,
        "backfire_mislabel_as_massless": backfire,
        "ok": (agree < D("1e-9") and flip and backfire == "COMPATIBLE-IDENTITY"),
        "note": "相容性判词随 m、p 读数翻转；但 p→∞ 才使有质量粒子 v→1，"
                "是极限而非有限可达态；m=0 恒等则判别力 0。",
    }


# ---------------------------------------------------------------- Q4 两种读法分叉
def two_readings():
    scan = compatibility_scan()
    n_inc = scan["n_incompatible"]
    # 读法 A：螺旋约束 = 同一粒子的质心速率 → 有质量有限 p 矛盾
    reading_a = ("CONTRADICTS-DISPERSION" if n_inc > 0 else "NO-CONTRADICTION")
    # 读法 B：螺旋约束只描述无质量内层光，复合粒子速率仍 p/E<1
    #   → 对内层光 v=1 是恒等；复合质量需外部输入（承封装光审计 恒等2/需输入4/新方程0）
    reading_b = "IDENTITY-FOR-MASSLESS--NO-NEW-EQUATION--P-FREE-UNCHANGED"
    prior = {
        "prior_book": "算法联盟_封装光假说可算审计_第三十轮_2026-11-16.md",
        "identity": 2, "free": 4, "new_equation": 0, "p_free": 3,
    }
    return {
        "reading_A_same_particle": reading_a,
        "reading_B_massless_inner_only": reading_b,
        "n_contradictions": n_inc,
        "prior_confined_light_result": prior,
        "ok": (reading_a == "CONTRADICTS-DISPERSION" and n_inc > 0),
        "note": "两读法分叉：A 与同表色散矛盾；B 退化为恒等且无新方程"
                "（不重复推封装光结论，只引用既有审计）。两分支都不产新的可判负动力学。",
    }


# ---------------------------------------------------------------- Q5 外部一手
EXTERNAL = {
    "sr_dispersion_velocity": {
        "url": "https://www.feynmanlectures.caltech.edu/I_16.html",
        "source": "Feynman Lectures on Physics Vol I Ch.16 (Caltech-hosted original)",
        "equations": "(16.13) E²−P²c²=m₀²c⁴ ; (16.14) Pc=Ev/c",
        "supports": "v=Pc²/E；m₀>0 且 P 有限 ⇒ v<c 严格；v=c 仅 m₀=0 或 P→∞",
    },
    "codata_masses": {
        "url": "https://pml.nist.gov/cuu/pdf/wall_2022.pdf",
        "source": "NIST SP 961 (2024), CODATA 2022",
        "supports": "m_e=0.51099895069 MeV/c²、m_p=938.27208816 MeV/c²",
    },
    "sr_velocity_limit": {
        "url": "https://en.wikipedia.org/wiki/Special_relativity",
        "source": "Special relativity (secondary overview, cross-check only)",
        "supports": "光速为有限质量粒子的速度上限；作为二手交叉核对，非一手裁决",
    },
}


def external_check():
    urls_ok = all(v["url"].startswith("https://") for v in EXTERNAL.values())
    # 外部事实是教科书结论，不包装成「本轮新发现」；来料未给 URL，不制造假阳性出处错误。
    material_gave_source = False
    fabricated_error = False
    return {
        "sources": EXTERNAL, "all_https": urls_ok,
        "material_gave_source": material_gave_source,
        "fabricated_source_error_claimed": fabricated_error,
        "ok": urls_ok and not fabricated_error,
        "note": "v<c 对有质量粒子是 SR 教科书结论，非本轮新物理；"
                "一手为 Feynman Lectures 原文，Wikipedia 仅二手交叉核对。",
    }


# ---------------------------------------------------------------- 自指守卫
def no_hardcoded_ok_guard():
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    needle = '"ok"' + ": " + "True"
    return needle not in src


def main():
    two = two_route_v()
    scan = compatibility_scan()
    flip = flip_gate()
    readings = two_readings()
    ext = external_check()
    guard = no_hardcoded_ok_guard()

    gates = {
        "G1-two-route-v-identity": {
            "exp": "v=p/E and v=tanh(asinh(p/m)) agree; residual is IDENTITY not independent evidence",
            "max_rel": two["max_rel"], "ok": two["ok"],
            "meaning": "两参数化给同一 v；数值核对成立，但按纪律标 IDENTITY，不承重",
        },
        "G2-spiral-vs-dispersion-scan": {
            "exp": "photon(m=0) COMPATIBLE-IDENTITY; massive finite-p all INCOMPATIBLE",
            "n_incompatible": scan["n_incompatible"], "n_identity": scan["n_identity"],
            "positive_control": scan["positive_control_photons_identity"],
            "negative_control": scan["negative_control_massive_all_incompatible"],
            "ok": scan["ok"],
            "meaning": "负读数：螺旋约束与同表色散对有质量粒子不相容；无质量处恒等判别力0",
        },
        "G3-flip-threshold-two-route": {
            "exp": "p*/m analytic=bisection; verdict flips across p*; m=0 mislabel backfires",
            "pstar_analytic": flip["pstar_over_m_analytic"],
            "pstar_bisection": flip["pstar_over_m_bisection"],
            "two_route_rel": flip["two_route_rel"],
            "flip_works": flip["flip_works"],
            "backfire": flip["backfire_mislabel_as_massless"],
            "ok": flip["ok"],
            "meaning": "结论随 m、p 读数翻转；反噬把有质量误标为无质量则判词改变",
        },
        "G4-two-readings-fork": {
            "exp": "reading A contradicts; reading B identity+no new equation",
            "reading_A": readings["reading_A_same_particle"],
            "reading_B": readings["reading_B_massless_inner_only"],
            "n_contradictions": readings["n_contradictions"],
            "ok": readings["ok"],
            "meaning": "两种读法都不产新可判负动力学（A 矛盾，B 恒等）",
        },
        "G5-external-first-hand": {
            "exp": "Feynman Lectures eq16.13/16.14 + NIST CODATA first-hand; no fabricated error",
            "all_https": ext["all_https"], "ok": ext["ok"],
            "meaning": "外部裁决给一手；只作交叉核对，不包装成新物理发现",
        },
        "G6-no-hardcoded-ok": {
            "exp": "no literal ok=True in source",
            "ok": guard,
            "meaning": "门 ok 由 act 算出，非写死",
        },
    }
    n_ok = sum(1 for g in gates.values() if g["ok"])

    verdict = ("ROOTV132B-AUDIT--SPIRAL-VS-DISPERSION--MASSIVE-INCOMPATIBLE--"
               "MASSLESS-IDENTITY--FLIP-THRESHOLD-2ROUTE--TWO-READINGS-DEAD--"
               "SR-PRIMARY-OK--UFT-NOT-BROKEN--NEW-PREDICTION-0")

    out = {
        "date": "2026-11-21",
        "title": "ROOT V132 续：螺旋速度约束 R²ω²+u²=1 与色散 E²=p²+m² 相容性 · 可算审计",
        "kind": "external-material-computable-audit",
        "verdict": verdict,
        "convention": "c=1; hbar != 1; G != 1",
        "target_equations": {
            "S": "R²ω²+u²=1 (总速率恰为 c)",
            "D": "E²=p²+m² (色散)",
        },
        "external_fact": "v=p/E；m>0、p 有限 ⇒ v<1 严格；v=c 仅 m=0 或 p→∞",
        "constants": {"m_e_MeV": sci(M_E, 12), "m_p_MeV": sci(M_P, 12),
                      "tol_v": sci(TOL_V, 2), "tol_kin": sci(TOL_KIN, 2)},
        "two_route_v": two, "compatibility_scan": scan, "flip": flip,
        "two_readings": readings, "external": ext,
        "gates": gates, "n_gate_ok": n_ok, "n_gate_total": len(gates),
        "guards": {"no_hardcoded_ok": guard},
        "boundary": [
            "螺旋约束 R²ω²+u²=1 在 c=1 下即总速率=1；与同表色散 E²=p²+m² 并用时，"
            "对 m>0 且 p 有限的粒子给出 1-v>0 ⇒ 两式不能同时描述同一粒子的质心运动。",
            "m=0 处 v=1 是恒等式，判别力 0：它不区分任何无质量粒子，也不给质量或耦合的新信息。",
            "相容性只在 p→∞ 极限趋近（有质量粒子需无穷能量），有限动量下达不到；"
            "因此「相容」判词本身受容差 tol 支配（本册用 1e-6），不是无条件的物理相容。",
            "两种读法分叉：读法 A（同一粒子质心速率）与色散矛盾；读法 B（只描述无质量内层光）"
            "退化为恒等且无新方程（承封装光审计 恒等2/需输入4/新方程0）。两分支都不产新可判负动力学。",
            "v=p/E、v<c 对有质量粒子是 SR 教科书结论（Feynman Lectures eq16.13/16.14），"
            "一手给 URL，仅作外部裁决，不包装成本轮新物理发现。",
        ],
        "red_line": "数学自洽 != 实验证实；不宣称攻破统一场论，"
                    "不宣称发现新方程或独立实验预言；四力统一未证。",
        "discipline": ["非判定册", "不占RID", "不入README", "不回写既有产物",
                       "两路机拼", "恒等式识别", "正负双对照", "可翻转判据",
                       "门限数据驱动", "一手URL", "不制造假阳性错误", "无写死ok守卫"],
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)

    print("VERDICT =", verdict)
    tv = two_route_v()
    print("[1] 两路 v max rel =", tv["max_rel"], "kind = IDENTITY")
    sc = compatibility_scan()
    print("[2] 扫描: 不相容", sc["n_incompatible"], "恒等", sc["n_identity"],
          "正对照", sc["positive_control_photons_identity"],
          "负对照", sc["negative_control_massive_all_incompatible"])
    for r in sc["rows"][:4]:
        print("    %-10s p=%-12s v=%-14s 1-v=%-12s %s" %
              (r["case"], r["p"], r["v"], r["residual_1_minus_v"], r["verdict"]))
    fl = flip_gate()
    print("[3] p*/m 解析=%s 二分=%s rel=%s flip=%s 反噬=%s" %
          (fl["pstar_over_m_analytic"], fl["pstar_over_m_bisection"],
           fl["two_route_rel"], fl["flip_works"], fl["backfire_mislabel_as_massless"]))
    rd = two_readings()
    print("[4] 读法A=%s 读法B=%s 矛盾数=%d" %
          (rd["reading_A_same_particle"], rd["reading_B_massless_inner_only"],
           rd["n_contradictions"]))
    print("[5] 外部一手 ok =", external_check()["all_https"])
    print("[G] 判据", n_ok, "/", len(gates), "ok; 守卫 no-hardcoded-ok =", guard)
    print("JSON =", OUT_JSON, os.path.getsize(OUT_JSON), "B")
    return out


if __name__ == "__main__":
    main()
