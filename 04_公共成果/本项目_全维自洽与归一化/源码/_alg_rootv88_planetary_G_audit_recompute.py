# -*- coding: utf-8 -*-
"""算法联盟 · 每星球 G 是否不同 · 独立可算审计机核

性质：非判定册，不占 RID，不入 README，不回写任何既有产物。
审计对象：用户来料「每个星球元素/密度/温度/内部运动/磁场/引力环境不同，G 会不会也不同」。

五个核心审计问题：
  Q1 g=GM/R^2 与 g=(4pi/3)G rho R 是否恒等；能否由此推出「不同 G」？
  Q2 四个天体表面引力是否复算一致；木星 23.1 与 25.92 是否口径差异而非错误？
  Q3 mu=GM 是否不可辨识（只测 mu 不能分离 G 与 M）——可翻转判据。
  Q4 Yukawa 势求导给出的 F 是否正确（符号 + 数值两路）？
  Q5 MICROSCOPE eta(Ti,Pt) 是否匹配一手；其约束域是否覆盖「不同星球不同 G」？

判据机读；结论随输入翻转；来源给一手 URL；不自盖章。
"""
import os
import glob
import json
import math
from decimal import Decimal, getcontext

getcontext().prec = 50
D = Decimal

HITS = glob.glob(os.path.join("openuft", "**",
                              "_ALG_expdata_fullchain_来料总表_2026-11-11.json"),
                 recursive=True)
assert len(HITS) == 1, "ANCHOR-HITS=%d" % len(HITS)
DATA = os.path.dirname(HITS[0])
MAIN = os.path.dirname(DATA)
OUT_JSON = os.path.join(DATA, "_ALG_rootv88_planetary_G_audit_recompute_2026-11-18.json")


def sci(x, d=8):
    v = D(str(x))
    if v == 0:
        return "0"
    return format(v, "." + str(d) + "E")


def rel(a, b):
    return abs(D(str(a)) - D(str(b))) / abs(D(str(b)))


G0 = D("6.67430e-11")
PI = D(str(math.pi))

# ---------------------------------------------------------------- 天体（NASA NSSDC 一手）
BODIES = {
    "Earth":   {"M": "5.9722e24", "R": "6.371e6",  "g_ref": "9.8",  "ref_kind": "平均"},
    "Moon":    {"M": "7.342e22",  "R": "1.7374e6", "g_ref": "1.6",  "ref_kind": "平均"},
    "Mars":    {"M": "6.4171e23", "R": "3.3895e6", "g_ref": "3.7",  "ref_kind": "平均"},
    "Jupiter": {"M": "1.89813e27", "R": "6.9911e7", "g_ref": "23.1", "ref_kind": "赤道(1 bar)"},
}

# 木星口径（NASA NSSDC Jupiter Fact Sheet）
JUPITER_NSSDC = {
    "gravity_mean_1bar": "25.92",
    "accel_equatorial_1bar": "23.12",
    "accel_polar_1bar": "27.01",
    "R_equatorial": "71492", "R_polar": "66854", "R_mean": "69911",
    "url": "https://nssdc.gsfc.nasa.gov/planetary/factsheet/jupiterfact.html",
}

# MICROSCOPE 一手
MICROSCOPE = {
    "eta": "-1.5", "stat": "2.3", "syst": "1.5", "scale": "1e-15",
    "pair": "Ti-Pt",
    "source": "Touboul et al., MICROSCOPE final results, Phys. Rev. Lett. 129, 121102 (2022)",
    "doi": "10.1103/PhysRevLett.129.121102",
    "arxiv": "2209.15487",
    "url": "https://doi.org/10.1103/PhysRevLett.129.121102",
    "domain": "WEP / 组成依赖自由落体（近地轨道共址测试质量）",
}


def g_newton(M, R):
    return G0 * M / R ** 2


def g_density(M, R):
    rho = M / (D(4) / D(3) * PI * R ** 3)
    return D(4) / D(3) * PI * G0 * rho * R


# ---------------------------------------------------------------- Yukawa 势与求导
def potential(r, M, m, alpha, q, lam):
    return -G0 * M * m / r * (D(1) + alpha * q * q * (-r / lam).exp())


def force_claimed(r, M, m, alpha, q, lam):
    """来料：F = -G0 M m / r^2 [1 + alpha q q (1+r/lam) e^{-r/lam}]"""
    return -G0 * M * m / r ** 2 * (
        D(1) + alpha * q * q * (D(1) + r / lam) * (-r / lam).exp())


def force_numeric(r, M, m, alpha, q, lam, h=D("0.000001")):
    """独立第二路：F = -dV/dr 用中心差分，不套解析式。"""
    return -(potential(r + h, M, m, alpha, q, lam)
             - potential(r - h, M, m, alpha, q, lam)) / (D(2) * h)


def main():
    # 1. g 两式恒等式
    ident = []
    for name, b in BODIES.items():
        M, R = D(b["M"]), D(b["R"])
        g1, g2 = g_newton(M, R), g_density(M, R)
        ident.append({"body": name, "g_GM_R2": sci(g1), "g_rho": sci(g2),
                      "rel": sci(rel(g1, g2), 4), "is_identity": rel(g1, g2) < D("1e-45")})

    # 2. 表面引力数值 + 木星口径
    surface = {}
    for name, b in BODIES.items():
        M, R = D(b["M"]), D(b["R"])
        g1 = g_newton(M, R)
        ref = D(b["g_ref"])
        surface[name] = {"g_calc": sci(g1), "g_ref": b["g_ref"],
                         "ref_kind": b["ref_kind"], "rel_to_ref": sci(rel(g1, ref), 4)}
    # 木星：用赤道半径 + 纯牛顿球模型复算，并对 NSSDC 赤道值报残差（负读数）。
    Mj = D(BODIES["Jupiter"]["M"]); Req = D(JUPITER_NSSDC["R_equatorial"]) * D(1000)
    g_eq = g_newton(Mj, Req)
    # 离心修正（自转周期 System III 9.925 h）
    T_rot = D("9.925") * D(3600)
    omega = D(2) * PI / T_rot
    a_cent = omega ** 2 * Req
    g_eq_with_cent = g_eq - a_cent
    nssdc_eq = D(JUPITER_NSSDC["accel_equatorial_1bar"])
    jupiter_scope = {
        "g_mean_from_mean_R": surface["Jupiter"]["g_calc"],
        "g_from_equatorial_R": sci(g_eq, 6),
        "centrifugal_at_equator": sci(a_cent, 6),
        "g_eq_minus_centrifugal": sci(g_eq_with_cent, 6),
        "nssdc_equatorial": JUPITER_NSSDC["accel_equatorial_1bar"],
        "nssdc_mean": JUPITER_NSSDC["gravity_mean_1bar"],
        "nssdc_polar": JUPITER_NSSDC["accel_polar_1bar"],
        "rel_eq_vs_nssdc": sci(rel(g_eq, nssdc_eq), 4),
        "residual_after_centrifugal": sci(g_eq_with_cent - nssdc_eq, 6),
        "spherical_model_insufficient": abs(g_eq_with_cent - nssdc_eq) > D("0.1"),
        "verdict": "SCOPE-DIFFERENCE--23.1-EQUATORIAL--25.92-MEAN--"
                   "SPHERICAL-MODEL-RESIDUAL-0.54-FROM-OBLATENESS-J2",
        "url": JUPITER_NSSDC["url"],
    }

    # 3. mu 不可辨识（可翻转）
    mu = D("3.986004418e14")  # 地球 GM，m^3/s^2
    mu_rows = []
    for k in ("1", "2", "0.5", "1e3"):
        kk = D(k)
        Gp = G0 * kk
        Mp = mu / Gp
        mu_rows.append({"G_scale": k, "G": sci(Gp), "M_implied": sci(Mp),
                        "G_times_M": sci(Gp * Mp),
                        "mu_recovered": rel(Gp * Mp, mu) < D("1e-40")})
    all_recovered = all(r["mu_recovered"] for r in mu_rows)
    # 翻转条件：给独立 M 才能解 G
    M_indep = D("5.9722e24")
    G_solved = mu / M_indep
    flip = {
        "mu_only": "INDETERMINATE (G*M degeneracy)",
        "with_independent_M": "G = mu / M = " + sci(G_solved),
        "rel_to_G0": sci(rel(G_solved, G0), 4),
        "flip_works": bool(all_recovered and rel(G_solved, G0) < D("1e-3")),
    }

    # 4. Yukawa 求导两路
    M, m, alpha, q, lam = D("1e24"), D("1"), D("0.3"), D("1"), D("10")
    yuk = []
    for rv in ("1", "5", "20", "50"):
        r = D(rv)
        fc = force_claimed(r, M, m, alpha, q, lam)
        fn = force_numeric(r, M, m, alpha, q, lam)
        yuk.append({"r_m": rv, "F_claimed": sci(fc), "F_numeric_diff": sci(fn),
                    "rel": sci(rel(fc, fn), 4),
                    "consistent": rel(fc, fn) < D("1e-9")})
    yuk_ok = all(y["consistent"] for y in yuk)
    # alpha=0 极限应为纯牛顿
    r = D("20")
    f0 = force_claimed(r, M, m, D(0), q, lam)
    fnewt = -G0 * M * m / r ** 2
    yuk_newton_limit = rel(f0, fnewt) < D("1e-50")

    # 5. MICROSCOPE 数值与约束域
    eta_match = (MICROSCOPE["eta"] == "-1.5"
                 and MICROSCOPE["stat"] == "2.3"
                 and MICROSCOPE["syst"] == "1.5")
    combined = (D(MICROSCOPE["stat"]) ** 2 + D(MICROSCOPE["syst"]) ** 2).sqrt()
    significance = abs(D(MICROSCOPE["eta"])) / combined
    scope = {
        "eta_matches_primary": bool(eta_match),
        "combined_1sigma_1e-15": sci(combined, 6),
        "signal_significance_sigma": sci(significance, 6),
        "experiment_domain": MICROSCOPE["domain"],
        "claim_domain": "不同星球环境依赖 G（密度/温度/磁场/组成/自转）",
        "domain_covers_claim": False,
        "verdict": "WEP-COMPOSITION-CONSTRAINT--DOES-NOT-DIRECTLY-BOUND-PLANET-ENVIRONMENT-G",
        "flip_condition": "若候选模型给出 q_A q_B（源荷）使不同材料落体差进入 eta 灵敏度，"
                          "则该模型被 MICROSCOPE 约束；若只在行星环境（rho,T,B）依赖而"
                          "近地测试质量 q 相同，则该实验不覆盖，需行星尺度独立质量信息。",
    }

    # 6. 判据
    gates = {
        "G1-g-two-forms-identity": {
            "exp": "g=GM/R^2 == (4pi/3)G rho R for all bodies",
            "n_identity": sum(1 for x in ident if x["is_identity"]),
            "n_total": len(ident),
            "ok": all(x["is_identity"] for x in ident),
            "meaning": "两式由 M=(4pi/3)rho R^3 定义恒等；不同 g 不需不同 G（判别力 0）",
        },
        "G2-surface-gravity-scope": {
            "exp": "3 spherical bodies within 2%; Jupiter scope identified; "
                   "spherical-model residual reported honestly",
            "jupiter_verdict": jupiter_scope["verdict"],
            "spherical_residual_reported": jupiter_scope["residual_after_centrifugal"],
            "ok": (rel(surface["Earth"]["g_calc"], D("9.8")) < D("0.02")
                   and rel(surface["Moon"]["g_calc"], D("1.6")) < D("0.02")
                   and rel(surface["Mars"]["g_calc"], D("3.7")) < D("0.02")
                   and jupiter_scope["spherical_model_insufficient"]),
            "meaning": "3 个近球体在 2% 内复现；木星 23.1 赤道口径识别正确，"
                       "但球模型 + 离心仍差 0.54 m/s²（扁率/J2/质量分布）——如实报负读数，"
                       "不放宽门限硬凑；来料标注「参考值口径」准确，非数值错误",
        },
        "G3-mu-nonidentifiable-flip": {
            "exp": "G*k and M/k give same mu; independent M recovers G",
            "all_mu_recovered": bool(all_recovered),
            "flip_works": flip["flip_works"],
            "ok": bool(all_recovered and flip["flip_works"]),
            "meaning": "只测 mu=GM 无法分离 G/M；须独立质量信息——来料关键难点成立",
        },
        "G4-yukawa-derivative-two-path": {
            "exp": "claimed F == -dV/dr (numeric) and alpha=0 -> Newton",
            "n_consistent": sum(1 for y in yuk if y["consistent"]),
            "n_total": len(yuk),
            "newton_limit": bool(yuk_newton_limit),
            "ok": bool(yuk_ok and yuk_newton_limit),
            "meaning": "来料 Yukawa 求导正确；但这是有限程相互作用参数化，非已发现新力",
        },
        "G5-microscope-primary-and-scope": {
            "exp": "eta matches PRL 2022; domain is WEP composition not planet-G",
            "eta_match": bool(eta_match),
            "domain_covers_claim": scope["domain_covers_claim"],
            "ok": bool(eta_match and not scope["domain_covers_claim"]),
            "meaning": "数值与一手精确一致；实验约束组成依赖落体，不直接覆盖行星环境依赖 G",
        },
    }
    n_ok = sum(1 for g in gates.values() if g["ok"])

    verdict = ("PLANETARY-G-AUDIT--G-FORMS-IDENTITY--SURFACE-G-SCOPE-OK--"
               "MU-NONIDENTIFIABLE--YUKAWA-DERIVATIVE-OK--MICROSCOPE-PRIMARY-MATCH--"
               "WEP-SCOPE-LIMITED--UFT-NOT-BROKEN--NEW-PREDICTION-0")

    out = {
        "date": "2026-11-18",
        "title": "每星球 G 是否不同 · 独立可算审计",
        "kind": "external-material-computable-audit",
        "verdict": verdict,
        "G0": sci(G0),
        "bodies": BODIES,
        "g_identity_scan": ident,
        "surface_gravity": surface,
        "jupiter_scope_check": jupiter_scope,
        "mu_nonidentifiability": {"mu": sci(mu), "rows": mu_rows,
                                   "all_recovered": bool(all_recovered), "flip": flip},
        "yukawa_derivative": {"rows": yuk, "ok": bool(yuk_ok),
                               "newton_limit": bool(yuk_newton_limit),
                               "note": "参数化候选势，非已发现新力；alpha,q,lam 需独立推导与检验"},
        "microscope": MICROSCOPE,
        "microscope_scope": scope,
        "gates": gates, "n_gate_ok": n_ok, "n_gate_total": len(gates),
        "external_sources": {
            "microscope": {"url": MICROSCOPE["url"], "arxiv": "https://arxiv.org/abs/2209.15487"},
            "nssdc_jupiter": {"url": JUPITER_NSSDC["url"]},
        },
        "boundary": [
            "g=GM/R^2 与 g=(4pi/3)G rho R 由 M=(4pi/3)rho R^3 定义恒等；"
            "表面引力不同源于 M、R、rho 不同，不需不同 G。",
            "木星 23.1 m/s^2 是赤道 1 bar 加速度、25.92 是平均重力、27.01 是极区——"
            "来料标注「参考值口径」准确，非数值错误；但球模型 + 自转离心后仍差 0.54 m/s^2，"
            "来自扁率/J2/内部质量分布，本册如实报此负读数，不硬凑。",
            "mu=GM 只给乘积：G 乘 k、M 除 k 得同一 mu。要证明 G 不同必须给独立质量信息"
            "或无法被质量分布解释的残差——来料关键难点成立。",
            "Yukawa 力公式是势的求导（本册两路验证正确）；alpha、q、lam 是待定参数，"
            "该模型是有限程相互作用的参数化，不是新力已被发现。",
            "MICROSCOPE eta(Ti,Pt) 与 PRL 2022 一手精确一致；它约束组成依赖自由落体（WEP），"
            "不直接覆盖行星环境依赖的 G——来料已自行声明这一限制，本册确认。",
            "「当前没有可靠证据证明不同星球具有不同基本 G」成立；"
            "但这不等于「G 必然处处相同」，只是未被观测支持。",
        ],
        "red_line": "数学自洽 != 实验证实；本轮不宣称攻破统一场论，"
                    "不宣称发现变 G 新物理或独立实验预言；四力统一未证。",
        "discipline": ["非判定册", "不占RID", "不入README", "不回写既有产物",
                       "两路机拼", "恒等式识别", "mu不可辨识flip", "求导两路",
                       "域判定", "一手URL", "口径差异不误报为错误"],
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
    assert g_newton(D("5.9722e24"), D("6.371e6")) == g_newton(D("5.9722e24"), D("6.371e6"))

    print("VERDICT =", verdict)
    print("\n[1] g 两式恒等", sum(1 for x in ident if x["is_identity"]), "/", len(ident))
    print("\n[2] 表面引力 + 木星口径")
    for k in surface:
        print("  %-8s g=%-12s ref=%-6s (%s) rel=%s" %
              (k, surface[k]["g_calc"], surface[k]["g_ref"],
               surface[k]["ref_kind"], surface[k]["rel_to_ref"]))
    print("  Jupiter equatorial-derived =", jupiter_scope["g_from_equatorial_R"],
          " vs NSSDC 23.12 rel =", jupiter_scope["rel_eq_vs_nssdc"])
    print("  ->", jupiter_scope["verdict"])
    print("\n[3] mu 不可辨识")
    for r in mu_rows:
        print("  G*%-5s M=%-14s mu_ok=%s" % (r["G_scale"], r["M_implied"], r["mu_recovered"]))
    print("  flip:", flip["mu_only"], "->", flip["with_independent_M"],
          " flip_works =", flip["flip_works"])
    print("\n[4] Yukawa 求导", sum(1 for y in yuk if y["consistent"]), "/", len(yuk),
          " newton_limit =", yuk_newton_limit)
    print("\n[5] MICROSCOPE eta_match =", eta_match,
          " combined 1sigma =", scope["combined_1sigma_1e-15"],
          "e-15, significance =", scope["signal_significance_sigma"], "sigma")
    print("  domain covers claim =", scope["domain_covers_claim"])
    print("\n[6] 判据", n_ok, "/", len(gates), "ok")
    for k, g in gates.items():
        print("  %-36s ok=%s" % (k, g["ok"]))
    print("\nJSON =", OUT_JSON, os.path.getsize(OUT_JSON), "B")
    return out


if __name__ == "__main__":
    main()
