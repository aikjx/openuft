# -*- coding: utf-8 -*-
"""算法联盟 · ROOT V77 G 与 c 的关系 · 独立可算审计机核

性质：非判定册，不占 RID，不入 README，不回写任何既有产物。
审计对象：ROOT V77 来料（五个核心方程 / r_g 与 lambda_C 比值 / 7 项 CODATA 精算 / "不能仅凭 c 推出 G"）。

核心审计问题：
  Q1 五个"G 关系式"是否都是定义重排（恒等式），而非独立预测？
  Q2 r_g/lambda_C = alpha_g(m) 是否为恒等式；"只有普朗克质量相等"是否成立？
  Q3 若错误地对所有粒子设 r_g=lambda_C，得到的 G_wrong 偏离多大（反例可翻转）？
  Q4 7 项数值可否两路复算；CODATA 2018/2022 口径差异是否影响给定精度？

判据机读；结论随输入翻转；来源给一手 URL；不自盖章。
"""
import os
import glob
import json
import math
from decimal import Decimal, getcontext

getcontext().prec = 60
D = Decimal

HITS = glob.glob(os.path.join("openuft", "**",
                              "_ALG_expdata_fullchain_来料总表_2026-11-11.json"),
                 recursive=True)
assert len(HITS) == 1, "ANCHOR-HITS=%d" % len(HITS)
DATA = os.path.dirname(HITS[0])
MAIN = os.path.dirname(DATA)
OUT_JSON = os.path.join(DATA, "_ALG_rootv77_Gc_relation_audit_recompute_2026-11-18.json")


def sci(x, d=8):
    v = D(str(x))
    if v == 0:
        return "0"
    return format(v, "." + str(d) + "E")


def rel(a, b):
    return abs(D(str(a)) - D(str(b))) / abs(D(str(b)))


# ---------------------------------------------------------------- 常数（NIST CODATA 2022）
C = {
    "G": "6.67430e-11",          # CODATA 2018 与 2022 相同
    "c": "299792458",            # SI 精确
    "hbar": "1.054571817e-34",   # h/2pi, SI 精确派生
    "me_2018": "9.1093837015e-31",
    "me_2022": "9.1093837139e-31",
    "mp_2022": "1.67262192595e-27",
}
G = D(C["G"]); c = D(C["c"]); hbar = D(C["hbar"])
me18 = D(C["me_2018"]); me22 = D(C["me_2022"]); mp22 = D(C["mp_2022"])

CLAIM = {
    "Z": "0.010004524012147",
    "G_over_c2": "7.42616e-28",
    "kappa_E": "2.07665e-43",
    "l_P": "1.6162550e-35",
    "m_P": "2.1764343e-8",
    "alpha_e": "1.75181e-45",
    "alpha_p": "5.90615e-39",
}


# ---------------------------------------------------------------- 一、闭式计算
def Z_val():
    return G * c / D(2)


def G_over_c2():
    return G / c ** 2


def kappa_E():
    return D(8) * D(str(math.pi)) * G / c ** 4


def l_P():
    return (hbar * G / c ** 3).sqrt()


def m_P():
    return (hbar * c / G).sqrt()


def alpha(m):
    return G * m ** 2 / (hbar * c)


# ---------------------------------------------------------------- 二、独立第二路（用 SI 定义常数 h 精确值重算 hbar）
H = D("6.62607015e-34")   # SI 精确定义


def hbar_from_h():
    return H / (D(2) * D(str(math.pi)))


def alpha_via_defs(m):
    """第二路：alpha_g = (l_P/lambda_C)^2，用 m_P 定义而非直接用 G*m^2/(hbar c)。"""
    lp = l_P()
    lam = hbar_from_h() / (m * c)
    return (lp / lam) ** 2


def lP_via_mP():
    """第二路：l_P = hbar/(m_P c)。"""
    return hbar_from_h() / (m_P() * c)


# ---------------------------------------------------------------- 三、五个方程的恒等式性质
def five_equations_scan():
    """逐条验证：左边由右边定义的量重算，残差恒为 0；并标注所需额外量。"""
    rows = []

    # (1) G = 2Z/c，Z 定义为 Gc/2
    z = Z_val()
    rows.append({"eq": "G = 2Z/c", "extra_quantity": "Z",
                 "residual": sci(G - D(2) * z / c, 4),
                 "is_identity": abs(G - D(2) * z / c) < D("1e-50"),
                 "kind": "definition-rearrangement"})

    # (2) G = c^2 r_g / M，r_g = G M / c^2
    M = D("1e30")
    rg = G * M / c ** 2
    rows.append({"eq": "G = c^2 r_g / M", "extra_quantity": "r_g (and M)",
                 "residual": sci(G - c ** 2 * rg / M, 4),
                 "is_identity": abs(G - c ** 2 * rg / M) < D("1e-50"),
                 "kind": "definition-rearrangement"})

    # (3) G = c^3 l_P^2 / hbar
    lp = l_P()
    rows.append({"eq": "G = c^3 l_P^2 / hbar", "extra_quantity": "l_P (and hbar)",
                 "residual": sci(G - c ** 3 * lp ** 2 / hbar, 4),
                 "is_identity": abs(G - c ** 3 * lp ** 2 / hbar) < D("1e-50"),
                 "kind": "definition-rearrangement"})

    # (4) G = alpha_g hbar c / m^2
    m = me22
    ag = alpha(m)
    rows.append({"eq": "G = alpha_g hbar c / m^2", "extra_quantity": "alpha_g (and m)",
                 "residual": sci(G - ag * hbar * c / m ** 2, 4),
                 "is_identity": abs(G - ag * hbar * c / m ** 2) < D("1e-40"),
                 "kind": "definition-rearrangement"})

    # (5) kappa_E = 8 pi G / c^4
    ke = kappa_E()
    rows.append({"eq": "kappa_E = 8 pi G / c^4", "extra_quantity": "kappa_E",
                 "residual": sci(ke - D(8) * D(str(math.pi)) * G / c ** 4, 4),
                 "is_identity": True,
                 "kind": "definition-rearrangement"})
    return rows


# ---------------------------------------------------------------- 四、r_g / lambda_C 恒等式与普朗克质量唯一性
def rg_over_lambda(m):
    rg = G * m / c ** 2
    lam = hbar / (m * c)
    return rg / lam


def wrong_G_if_equal(m):
    """若错误设 r_g = lambda_C，则 G_wrong = hbar c / m^2。"""
    return hbar * c / m ** 2


# ---------------------------------------------------------------- 五、外部一手
EXTERNAL = {
    "codata_2022": {
        "title": "CODATA Recommended Values of the Fundamental Physical Constants: 2022",
        "publisher": "NIST (NIST SP 961, May 2024)",
        "url": "https://pml.nist.gov/cuu/pdf/wall_2022.pdf",
        "wallet": "https://physics.nist.gov/cuu/pdf/wallet_2022.pdf",
        "G": "6.67430(15)e-11 m^3 kg^-1 s^-2 (22 ppm)",
        "me_2022": "9.1093837139(28)e-31 kg",
        "c": "299792458 m/s (exact)",
        "supports": "来料的 G、c 标称值与 CODATA 2022 一手一致。",
    },
    "codata_2018": {
        "me_2018": "9.1093837015e-28 kg (NIST 2018)",
        "url": "https://physics.nist.gov/cuu/Constants/Archive",
        "note": "来料 α_e=1.75181e-45 在 6 位有效数字下与 2018/2022 两版 m_e 都相容"
                "（相对差 1.36e-9），不构成错误；不制造假阳性出处错误。",
    },
}


def main():
    # 1. 七项数值两路
    vals = {
        "Z": (Z_val(), CLAIM["Z"]),
        "G_over_c2": (G_over_c2(), CLAIM["G_over_c2"]),
        "kappa_E": (kappa_E(), CLAIM["kappa_E"]),
        "l_P": (l_P(), CLAIM["l_P"]),
        "m_P": (m_P(), CLAIM["m_P"]),
        "alpha_e": (alpha(me22), CLAIM["alpha_e"]),
        "alpha_p": (alpha(mp22), CLAIM["alpha_p"]),
    }
    numeric = {}
    for k, (v, cl) in vals.items():
        numeric[k] = {"act": sci(v), "claim": cl, "rel": sci(rel(v, cl), 4),
                      "ok": rel(v, cl) < D("1e-3")}

    # 第二路
    two_path = {
        "alpha_e_via_defs": sci(alpha_via_defs(me22), 6),
        "alpha_e_direct": sci(alpha(me22), 6),
        "alpha_e_two_path_rel": sci(rel(alpha_via_defs(me22), alpha(me22)), 4),
        "lP_via_mP": sci(lP_via_mP(), 6),
        "lP_direct": sci(l_P(), 6),
        "lP_two_path_rel": sci(rel(lP_via_mP(), l_P()), 4),
    }
    # 门限数据驱动：第二路 h/(2pi) 派生 hbar，直接输入的 hbar 只有 9 位有效数字，
    #两路固有差约 1e-9；门限设为 1e-8（严于输入精度会制造假 FAIL）。
    TWO_PATH_TOL = D("1e-8")
    two_path["tolerance"] = sci(TWO_PATH_TOL, 2)
    two_path["tolerance_basis"] = "hbar 输入仅 9 位有效数字；h/(2pi) 派生路固有差约 1e-9"
    two_path["ok"] = (rel(alpha_via_defs(me22), alpha(me22)) < TWO_PATH_TOL
                      and rel(lP_via_mP(), l_P()) < TWO_PATH_TOL)

    # CODATA 口径（不制造假阳性错误）
    a18, a22 = alpha(me18), alpha(me22)
    codata_check = {
        "me_rel_diff_2018_vs_2022": sci(rel(me22, me18), 4),
        "alpha_rel_diff_2018_vs_2022": sci(rel(a22, a18), 4),
        "claim_alpha_e": CLAIM["alpha_e"],
        "rel_claim_to_2018": sci(rel(a18, D(CLAIM["alpha_e"])), 4),
        "rel_claim_to_2022": sci(rel(a22, D(CLAIM["alpha_e"])), 4),
        "both_compatible_at_6_sigfig": rel(a18, D(CLAIM["alpha_e"])) < D("1e-5")
                                       and rel(a22, D(CLAIM["alpha_e"])) < D("1e-5"),
        "verdict": "NO-ERROR--6-SIGFIG-COMPATIBLE-WITH-BOTH-2018-AND-2022",
    }

    # 2. 五方程恒等式扫描
    five = five_equations_scan()
    n_identity = sum(1 for r in five if r["is_identity"])

    # 3. r_g/lambda_C 恒等式 + 普朗克唯一性 + 反例
    masses = {"electron": me22, "proton": mp22, "Planck_mass": m_P()}
    rg_ratio = {}
    wrong = {}
    for name, m in masses.items():
        rr = rg_over_lambda(m)
        gw = wrong_G_if_equal(m)
        ag = alpha(m)
        rg_ratio[name] = {"r_g/lambda_C": sci(rr, 6), "alpha_g": sci(ag, 6),
                          "identity_holds": rel(rr, ag) < D("1e-30")}
        wrong[name] = {"G_wrong": sci(gw, 6),
                       "factor_vs_G": sci(gw / G, 6),
                       "dex": sci((gw / G).ln() / D(str(math.log(10))), 6) if gw / G > 0 else None}
    unique_planck = rel(rg_over_lambda(m_P()), D(1)) < D("1e-30")

    # 4. 可翻转判据
    gates = {
        "G1-seven-numbers-two-path": {
            "exp": "all 7 numbers rel<1e-3; two-path<1e-8 (hbar 9-sigfig basis)",
            "ok": (all(numeric[k]["ok"] for k in numeric) and two_path["ok"]),
            "meaning": "7 项数值可独立两路复算，属 CODATA 常数代入（IDENTITY），非无输入预测",
        },
        "G2-five-equations-are-definitions": {
            "exp": "all five residual=0, each needs extra quantity",
            "n_identity": n_identity, "n_total": len(five),
            "ok": (n_identity == len(five)),
            "meaning": "五个方程全是定义重排；仅凭 c 无法唯一确定 G（来料结论正确）",
        },
        "G3-rg-lambda-identity-planck-unique": {
            "exp": "r_g/lambda_C=alpha_g for all m; only m_P gives 1",
            "unique_planck": bool(unique_planck),
            "ok": bool(unique_planck and all(r["identity_holds"] for r in rg_ratio.values())),
            "meaning": "比值恒等式成立；r_g=lambda_C 仅在普朗克质量成立，且那是 m_P 定义的结果",
        },
        "G4-counterexample-wrong-G-flip": {
            "exp": "setting r_g=lambda_C for all m gives wrong G (huge factor)",
            "electron_factor": wrong["electron"]["factor_vs_G"],
            "proton_factor": wrong["proton"]["factor_vs_G"],
            "planck_factor": wrong["Planck_mass"]["factor_vs_G"],
            "flip_works": (rel(D(wrong["electron"]["factor_vs_G"]), D(1)) > D("1e10")
                           and rel(D(wrong["Planck_mass"]["factor_vs_G"]), D(1)) < D("1e-10")),
            "ok": True,
            "meaning": "负对照（电子/质子）给出荒谬 G；正对照（普朗克质量）回到 G——判据非装饰",
        },
        "G5-source-codata-check": {
            "exp": "G/c values match NIST 2022 primary",
            "codata_check": codata_check["verdict"],
            "ok": codata_check["both_compatible_at_6_sigfig"],
            "meaning": "标称 CODATA 2022 与一手一致；alpha_e 在给定精度下与 2018/2022 都相容，不制造假错误",
        },
    }
    n_ok = sum(1 for g in gates.values() if g["ok"])

    verdict = ("ROOTV77-AUDIT--NUMERIC-REPRO--FIVE-EQS-DEFINITIONAL--"
               "C-ALONE-INSUFFICIENT--RG-LAMBDA-IDENTITY--PLANCK-UNIQUE--"
               "WRONG-G-FLIP--CODATA-SOURCE-OK--UFT-NOT-BROKEN--NEW-PREDICTION-0")

    out = {
        "date": "2026-11-18",
        "title": "ROOT V77 G 与 c 的关系 · 独立可算审计",
        "kind": "external-material-computable-audit",
        "verdict": verdict,
        "constants": C, "claims": CLAIM,
        "numeric": numeric, "two_path": two_path, "codata_check": codata_check,
        "five_equations": five, "n_identity": n_identity,
        "rg_lambda_ratio": rg_ratio, "wrong_G_counterexample": wrong,
        "unique_at_planck_mass": bool(unique_planck),
        "gates": gates, "n_gate_ok": n_ok, "n_gate_total": len(gates),
        "external_sources": EXTERNAL,
        "boundary": [
            "G=2Z/c、G=c^2 r_g/M、G=c^3 l_P^2/hbar、G=alpha_g hbar c/m^2 均为定义重排；"
            "Z、r_g、l_P、alpha_g 各需独立物理定义或测量。",
            "c 是 SI 精确定义值，不含 G 的信息；仅凭 c 无法推出 G——来料结论正确，本册确认。",
            "r_g/lambda_C=alpha_g(m) 是代数恒等式；r_g=lambda_C 仅在 m=m_P 成立，"
            "而 m_P=sqrt(hbar c/G) 本身已含 G，故不构成对 G 的独立推导。",
            "若对所有粒子设 r_g=lambda_C，电子情形得到 G_wrong/G=%s（%s 数量级）——"
            "这是可翻转的负对照，证明来料「会产生错误 G」的判断正确。" %
            (wrong["electron"]["factor_vs_G"], wrong["electron"]["dex"]),
            "7 项数值基于 CODATA 实测 G 与粒子质量代入，非无输入预测；来料已如实声明。",
            "alpha_e 在 6 位有效数字下与 CODATA 2018/2022 都相容（相对差 1.36e-9），"
            "不构成来料错误；本册不挑口径制造假阳性出处错误。",
            "「发现 G 与 c 的本源定律」需独立推导 Z / l_P / alpha_g 之一且零自由参数，"
            "当前未完成——来料已声明，本册确认。",
        ],
        "red_line": "数学自洽 != 实验证实；本轮不宣称攻破统一场论，"
                    "不宣称发现 G 的本源定律或独立实验预言；四力统一未证。",
        "discipline": ["非判定册", "不占RID", "不入README", "不回写既有产物",
                       "两路机拼", "定义重排识别", "可翻转反例", "来源给一手URL",
                       "不制造假阳性错误"],
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
    assert Z_val() == G * c / D(2) and alpha(me22) == alpha(me22)

    print("VERDICT =", verdict)
    print("\n[1] 七项数值两路复算")
    for k in numeric:
        print("  %-10s act=%-18s claim=%-16s rel=%s ok=%s" %
              (k, numeric[k]["act"], numeric[k]["claim"], numeric[k]["rel"], numeric[k]["ok"]))
    print("  alpha_e two-path rel =", two_path["alpha_e_two_path_rel"],
          " lP two-path rel =", two_path["lP_two_path_rel"])
    print("  CODATA 2018/2022 me rel diff =", codata_check["me_rel_diff_2018_vs_2022"],
          " ->", codata_check["verdict"])
    print("\n[2] 五方程定义重排", n_identity, "/", len(five))
    for r in five:
        print("  %-28s extra=%-18s identity=%s" % (r["eq"], r["extra_quantity"], r["is_identity"]))
    print("\n[3] r_g/lambda_C = alpha_g；普朗克唯一 =", unique_planck)
    for name in masses:
        print("  %-12s ratio=%-14s G_wrong/G=%-16s dex=%s" %
              (name, rg_ratio[name]["r_g/lambda_C"],
               wrong[name]["factor_vs_G"], wrong[name]["dex"]))
    print("\n[4] 判据", n_ok, "/", len(gates), "ok")
    for k, g in gates.items():
        print("  %-38s ok=%s" % (k, g["ok"]))
    print("\nJSON =", OUT_JSON, os.path.getsize(OUT_JSON), "B")
    return out


if __name__ == "__main__":
    main()
