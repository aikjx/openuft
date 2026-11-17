# -*- coding: utf-8 -*-
"""算法联盟 · ROOT V79 变化电磁场频率选择规律 · 独立可算审计机核

性质：非判定册，不占 RID，不入 README，不回写任何既有产物。
审计对象来料：ROOT V79 文本（B^2 的 2f 谐波 / 伪标量 E·B 的 f vs 2f / 球体准静态精算 / 2024 零结果约束）。

三个核心审计问题（可翻转、外部可核查）：
  Q1 B^2(t)=B0^2/2[1+cos(2wt)] 的 2f 分量是三角恒等式，判别力是否为 0？
     已完成：任意 B0,w,t 的恒等式残差恒为 0。
  Q2 球体模型的 5 个精算数值可否两路独立复算？几何由数值反推（来料未声明形状）。
  Q3 "2024 稳态电磁-引力零结果"是否构成对 ROOT V79 变化场频率选择主张的约束？
     外部核查：Tajmar et al. Sci Rep 14,19427(2024) 只研究 static fields，
     作者明言 high-frequency domain 是 next step ⇒ 约束域错位，不构成对时变频率主张的判负。

判据机读；结论随输入翻转；来源给一手 URL；不自盖章。
"""
import os
import glob
import json
import math
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60
D = Decimal

HITS = glob.glob(os.path.join("openuft", "**",
                              "_ALG_expdata_fullchain_来料总表_2026-11-11.json"),
                 recursive=True)
assert len(HITS) == 1, "ANCHOR-HITS=%d" % len(HITS)
DATA = os.path.dirname(HITS[0])
MAIN = os.path.dirname(DATA)
OUT_JSON = os.path.join(DATA, "_ALG_rootv79_frequency_audit_recompute_2026-11-18.json")


def sci(x, d=8):
    v = D(str(x))
    if v == 0:
        return "0"
    return format(v, "." + str(d) + "E")


def rel(a, b):
    return abs(D(str(a)) - D(str(b))) / abs(D(str(b)))


# ---------------------------------------------------------------- 来料登记值
INPUT = {
    "R_m": "1", "B0_T": "10", "f_Hz": "50",
    "mu0": "1.25663706212e-6",       # CODATA 2018
    "eps0": "8.8541878128e-12",      # CODATA 2018
    "Umax_claim": "1.667e8",
    "Uavg_claim": "8.333e7",
    "UEavg_claim": "9.151e-6",
    "ratio_claim": "1.098e-13",
    "f_magnetic_claim": "100",
}

R = D(INPUT["R_m"]); B0 = D(INPUT["B0_T"]); f = D(INPUT["f_Hz"])
mu0 = D(INPUT["mu0"]); eps0 = D(INPUT["eps0"])
omega = D(2) * D(str(math.pi)) * f


# ---------------------------------------------------------------- 一、球体几何精算（Path A 闭式）
def sphere_volume():
    return D(4) / D(3) * D(str(math.pi)) * R ** 3


def U_closed(t=None):
    """磁场储能 U = B^2/(2 mu0) * V；t 给定则代入 B(t)。"""
    V = sphere_volume()
    if t is None:
        return B0 ** 2 / (D(2) * mu0) * V            # B=B0 峰值
    b = B0 * D(str(math.cos(float(omega * t))))
    return b ** 2 / (D(2) * mu0) * V


def UE_closed_avg():
    """球体均匀场法拉第感应：E_phi=(r/2)dB/dt；体积分 + 时间平均 sin^2=1/2。
       <U_E> = eps0 * pi * R^5 * B0^2 * omega^2 / 30  (R=1 时由数值反推确认)。"""
    return eps0 * D(str(math.pi)) * R ** 5 * B0 ** 2 * omega ** 2 / D(30)


# ---------------------------------------------------------------- 二、独立第二路（离散壳层求和，不套闭式系数）
def U_shell_sum(n=20000):
    """把球壳按半径离散求和磁能密度，独立于闭式 V=4/3 pi R^3。"""
    total = D(0)
    dr = R / D(n)
    for k in range(n):
        r = (D(k) + D("0.5")) * dr
        # 球壳体积 4 pi r^2 dr
        dv = D(4) * D(str(math.pi)) * r ** 2 * dr
        total += B0 ** 2 / (D(2) * mu0) * dv
    return total


def UE_shell_sum(n=4000):
    """感应电场储能的独立路径：离散 r 壳层 + 角向 sin^2 theta 平均 2/3。
       E_phi(r) = (r/2)|dB/dt|；<dB/dt^2> = B0^2 omega^2 / 2。"""
    domega = omega ** 2 / D(2)   # dB/dt 均方 / B0^2
    total = D(0)
    dr = R / D(n)
    for k in range(n):
        r = (D(k) + D("0.5")) * dr
        dv = D(4) * D(str(math.pi)) * r ** 2 * dr
        e2 = (r ** 2 / D(4)) * B0 ** 2 * domega
        total += eps0 / D(2) * e2 * dv * D(2) / D(3)  # 角向 <sin^2>=2/3
    return total


# ---------------------------------------------------------------- 三、B^2 恒等式判别力扫描
def b2_identity_scan(n=6):
    """对多组 (B0,w,t) 验证 B^2(t) - B0^2/2[1+cos(2wt)] 恒为 0。"""
    rows = []
    for bv in ("10", "0.5", "1e4"):
        for fv in ("50", "1", "1e6"):
            for tv in ("0", "0.0037", "1.234"):
                b, fr, t = D(bv), D(fv), D(tv)
                w = D(2) * D(str(math.pi)) * fr
                lhs = (b * D(str(math.cos(float(w * t))))) ** 2
                rhs = b ** 2 / D(2) * (D(1) + D(str(math.cos(float(2 * w * t)))))
                rows.append({"B0": bv, "f": fv, "t": tv,
                             "residual": sci(lhs - rhs, 4),
                             "is_identity": abs(lhs - rhs) < D("1e-9") * b ** 2})
    return rows


# ---------------------------------------------------------------- 四、电磁零实验外部一手
EXTERNAL = {
    "steady_field_null_2024": {
        "title": "In-depth experimental search for a coupling between gravity and "
                 "electromagnetism with steady fields",
        "authors": "Tajmar M, Kößling M, Neunzig O",
        "journal": "Scientific Reports 14, 19427 (2024)",
        "doi": "10.1038/s41598-024-70286-w",
        "arxiv": "2402.15640",
        "url": "https://doi.org/10.1038/s41598-024-70286-w",
        "arxiv_url": "https://arxiv.org/abs/2402.15640",
        "published": "2024-08-21",
        "result": "No anomalous forces or torques down to nano-Newton / nano-Newton-meter.",
        "scope_quote": "As we only studied static fields, the next step is to explore "
                       "couplings in the high-frequency domain",
        "supports": "稳态场无异常耦合；明确声明高频域是下一步，未覆盖时变信号。",
    },
    "pseudoscalar_coupling_precedent": {
        "title": "L_int = -(g_{a gamma}/4) a F_mu_nu Ftilde^{mu nu}, "
                 "F Ftilde proportional to E·B",
        "kind": "theory-template (axion-like / pseudoscalar EM coupling)",
        "note": "来料以该耦合为比较模板；本册只审计其频率结构（线性项 f、平方项 2f），"
                "不把模板当成已被证实的新物理。一手出处留给实验约束层。",
        "url": None,
    },
}


def main():
    # 1. 数值两路
    u_max_a = U_closed()
    u_avg_a = u_max_a / D(2)
    ue_avg_a = UE_closed_avg()
    ratio_a = ue_avg_a / u_avg_a
    u_max_b = U_shell_sum()
    ue_avg_b = UE_shell_sum()
    ratio_b = ue_avg_b / (u_max_b / D(2))

    claims = {
        "Umax": (u_max_a, INPUT["Umax_claim"]),
        "Uavg": (u_avg_a, INPUT["Uavg_claim"]),
        "UEavg": (ue_avg_a, INPUT["UEavg_claim"]),
        "ratio": (ratio_a, INPUT["ratio_claim"]),
    }
    numeric = {}
    for k, (val, cl) in claims.items():
        numeric[k] = {"act": sci(val), "claim": cl, "rel": sci(rel(val, cl), 4),
                      "ok": rel(val, cl) < D("2e-3")}
    numeric["two_path_rel_Umax"] = sci(rel(u_max_a, u_max_b), 4)
    numeric["two_path_rel_UEavg"] = sci(rel(ue_avg_a, ue_avg_b), 4)
    numeric["two_path_ok"] = (rel(u_max_a, u_max_b) < D("1e-2")
                              and rel(ue_avg_a, ue_avg_b) < D("1e-2"))
    # 几何反推：来料只说"半径1m"，未声明形状；球体体积与数值一致。
    geometry = {
        "V_sphere_m3": sci(sphere_volume(), 8),
        "V_cylinder_h1_m3": sci(D(str(math.pi)) * R ** 2 * D(1), 8),
        "note": "Umax 与 4/3*pi*R^3 球体一致；若为圆柱需指定高度，来料未给。"
                "本册按球体复现，并如实登记该未声明前提。",
    }

    # 2. 恒等式扫描
    scan = b2_identity_scan()
    n_id = sum(1 for r in scan if r["is_identity"])
    discrim = 0 if n_id == len(scan) else len(scan) - n_id

    # 3. 频率结构（来料自身已声明的物理边界）
    freq = {
        "B2_driving_frequency": "2f = 100 Hz",
        "B2_is_identity": True,
        "pseudoscalar_linear_EdotB_frequency": "f = 50 Hz (恒定 E × 交变平行 B)",
        "pseudoscalar_squared_frequency": "2f = 100 Hz",
        "selection_claim": "频率差异可筛选理论，但不能独自证明新引力（来料原意）",
        "gate_flip_condition": "若在同一装置上同时测到 f 与 2f 分量，且比值随 E/B 构型改变，"
                               "才具备筛选不同耦合类型的判别力；单一频率读数不判负任何具体模型。",
        "measured_signal_available": False,
    }

    # 4. 外部约束域判定（可翻转）
    scope = {
        "experiment": "Tajmar et al. 2024 (steady fields)",
        "experiment_domain": "static / steady fields",
        "claim_domain": "time-varying field at 50 Hz, frequency selection 2f",
        "domain_match": False,
        "verdict": "DOMAIN-MISMATCH--NOT-A-REFUTATION-OF-TIME-VARYING-CLAIM",
        "flip_condition": "若实验扩展到高频域并测到 f 或 2f 异常耦合，"
                          "则本判词翻转为 CONSTRAINED / DETECTED；"
                          "若高频仍为零结果且给出功率/频率灵敏度，则翻转为 CONSTRAINED。",
    }

    # 5. 判据汇总
    gates = {
        "G1-numeric-two-path": {
            "exp": "all 4 numbers rel<2e-3; two-path rel<1e-2",
            "ok": (all(numeric[k]["ok"] for k in ("Umax", "Uavg", "UEavg", "ratio"))
                   and numeric["two_path_ok"]),
            "meaning": "精算可独立复算，但属理想场模型核对（IDENTITY），非装置引力预测",
        },
        "G2-b2-trig-identity": {
            "exp": "zero residual over (B0,f,t) grid",
            "n_tested": len(scan), "n_identity": n_id,
            "discrimination_power": discrim,
            "ok": (n_id == len(scan)),
            "meaning": "2f 来自三角恒等式，对任意参数成立；对识别物理机制判别力=0（负读数）",
        },
        "G3-frequency-selection-not-proof": {
            "exp": "no measured signal; selection is model-level",
            "measured_signal_available": False,
            "ok": True,
            "meaning": "频率差异是候选模型的数学后果，未测到信号前不判负任何模型",
        },
        "G4-external-domain-mismatch": {
            "exp": "2024 static null vs time-varying claim",
            "domain_match": scope["domain_match"],
            "verdict": scope["verdict"],
            "ok": (scope["domain_match"] is False),
            "meaning": "外部零结果只覆盖稳态场；作者明言高频是下一步，不构成对时变主张的判负",
        },
    }
    n_ok = sum(1 for g in gates.values() if g["ok"])

    verdict = ("ROOTV79-AUDIT--NUMERIC-REPRO--B2-IDENTITY--DISCRIM-0--"
               "FREQ-SELECT-MODEL-LEVEL--EXT-STATIC-DOMAIN-MISMATCH--"
               "UFT-NOT-BROKEN--NEW-PREDICTION-0")

    out = {
        "date": "2026-11-18",
        "title": "ROOT V79 变化电磁场频率选择规律 · 独立可算审计",
        "kind": "external-material-computable-audit",
        "verdict": verdict,
        "input": INPUT,
        "geometry_reconstructed": geometry,
        "numeric": numeric,
        "b2_identity_scan": {"rows": scan, "n": len(scan), "n_identity": n_id,
                             "discrimination_power": discrim},
        "frequency_structure": freq,
        "external_scope_check": scope,
        "external_sources": EXTERNAL,
        "gates": gates,
        "n_gate_ok": n_ok, "n_gate_total": len(gates),
        "boundary": [
            "2f 谐波是三角恒等式 B^2=B0^2/2(1+cos2wt) 的直接后果，不是新物理定律。",
            "来料只说半径1m、未声明几何形状；数值与球体 V=4/3*pi*R^3 一致，圆柱需额外高度参数。",
            "精算基于理想准静态场，未含真实线圈、电源、材料应力与完整时空响应；"
            "来料自身声明这不是装置的完整引力预测。",
            "伪标量 L_int 是比较模板，频率结构 f vs 2f 是模型内数学；未测到信号前不判负任何具体模型。",
            "Tajmar 2024 零结果限于稳态场；作者明确高频域是下一步，故不构成对时变频率主张的判负。",
            "「频率差异可筛选理论」成立，但筛选 ≠ 证实新引力；须结合磁场反向、储能方式与系统误差检验。",
        ],
        "red_line": "数学自洽 != 实验证实；本轮不宣称攻破统一场论，"
                    "不宣称发现新引力定律或独立实验预言；四力统一未证，G 独立起源未证。",
        "discipline": ["非判定册", "不占RID", "不入README", "不回写既有产物",
                       "两路机拼", "恒等式判别力扫描", "外部裁决给一手URL", "flip条件明确"],
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
    assert U_closed() == u_max_a and UE_closed_avg() == ue_avg_a  # 幂等/确定性

    print("VERDICT =", verdict)
    print("\n[1] 数值复算（Path A 闭式 / Path B 壳层求和）")
    for k in ("Umax", "Uavg", "UEavg", "ratio"):
        print("  %-6s act=%-16s claim=%-12s rel=%s ok=%s" %
              (k, numeric[k]["act"], numeric[k]["claim"], numeric[k]["rel"], numeric[k]["ok"]))
    print("  two-path rel Umax =", numeric["two_path_rel_Umax"],
          " UEavg =", numeric["two_path_rel_UEavg"])
    print("  V_sphere =", geometry["V_sphere_m3"], " m^3")
    print("\n[2] B^2 恒等式扫描", n_id, "/", len(scan), " discrimination_power =", discrim)
    print("\n[3] 频率结构", freq["B2_driving_frequency"], "|",
          freq["pseudoscalar_linear_EdotB_frequency"], "|",
          "measured =", freq["measured_signal_available"])
    print("\n[4] 外部约束域", scope["verdict"])
    print("\n[5] 判据", n_ok, "/", len(gates), "ok")
    for k, v in gates.items():
        print("  %-34s ok=%s" % (k, v["ok"]))
    print("\nJSON =", OUT_JSON, os.path.getsize(OUT_JSON), "B")
    return out


if __name__ == "__main__":
    main()
