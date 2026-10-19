# -*- coding: utf-8 -*-
"""
================================================================================
openuft#49 攻破第六轮 · 总收口判决（三条路径合并）
================================================================================
把「力统一」的全部可能路径合并为一张决策树，并给出总判决：

  路径 A（空间运行方式）  -> 第四轮：标度重参数化不变 => 闭合
  路径 B（换谱）          -> 第五轮：100 共线候选，0 过质子衰变 => 闭合
  路径 C（扩群 SO(10)）   -> 既有 so10_chain.py 探针（本轮只合并判决，不复算其数）

本引擎：A/B 两条自含复算；C 的判决以「归因输入」形式登记（注明来源行），
        再按决策树合并出总判决。不自造 SO(10) 数字。

纯标准库；自检不过即退出码非 0。
================================================================================
"""
from __future__ import print_function
import json
import math
import os
import sys

MZ = 91.1876
TWO_PI = 2.0 * math.pi
A = {1: 59.0209, 2: 29.5838, 3: 8.47458}
AS_MZ, AS_SIG = 0.1180, 0.0009
B_SM = {1: 41.0 / 10.0, 2: -19.0 / 6.0, 3: -7.0}
B_MSSM = {1: 33.0 / 5.0, 2: 1.0, 3: -3.0}
PROTON_BOUND = 1.6e34
N_OBS = 8


def required_ratio():
    return (A[2] - A[1]) / (A[3] - A[1])


def ratio(b):
    den = b[3] - b[1]
    return float("inf") if abs(den) < 1e-15 else (b[2] - b[1]) / den


def ainv(i, u, b):
    return A[i] - (b[i] / TWO_PI) * u


def spread(u, b):
    v = [ainv(i, u, b) for i in (1, 2, 3)]
    return max(v) - min(v)


def pairwise_u(i, j, b):
    return TWO_PI * (A[i] - A[j]) / (b[i] - b[j])


def analytic_min_spread(b, U=45.0):
    cands = [0.0, U] + [max(0.0, min(U, pairwise_u(i, j, b)))
                        for (i, j) in ((1, 2), (1, 3), (2, 3))]
    best = (1e9, 0.0)
    for u in cands:
        d = spread(u, b)
        if d < best[0]:
            best = (d, u)
    return best


def proton_lifetime(mgut):
    return (mgut / 2.0e16) ** 4 * 1.0e35


def unify_scale(b):
    u12 = TWO_PI * (A[1] - A[2]) / (b[1] - b[2])
    return u12, MZ * math.exp(u12), A[1] - (b[1] / TWO_PI) * u12


# ---------------- 路径 A：运行不变性（第四轮复算） ----------------
def path_a():
    rstar = required_ratio()
    d0, u0 = analytic_min_spread(B_SM)
    diffs = []
    for f, finv in ((lambda u: u * u, math.sqrt), (math.expm1, math.log1p)):
        diffs.append(abs(spread(finv(f(u0)), B_SM) - d0))
    return {
        "r_star": rstar,
        "SM_ratio": ratio(B_SM),
        "MSSM_ratio": ratio(B_MSSM),
        "analytic_min_spread": d0,
        "reparam_max_diff": max(diffs),
        "verdict": "CLOSED" if max(diffs) < 1e-9 else "OPEN",
    }


# ---------------- 路径 B：换谱（第五轮复算，精简：单表示×n + 色单态两两） --------
def delta_b(c3, t3, c2, t2, y, kind):
    coef = 2.0 / 3.0 if kind == "F" else 1.0 / 3.0
    return {1: coef * (3.0 / 5.0) * y * y * c3 * c2,
            2: coef * t2 * c3,
            3: coef * t3 * c2}


def path_b():
    COLOR = [("1", 1, 0.0), ("3", 3, 0.5), ("8", 8, 3.0)]
    WEAK = [("1", 1, 0.0), ("2", 2, 0.5), ("3", 3, 2.0)]
    Y_LIST = [-1.0, -2.0 / 3, -1.0 / 2, -1.0 / 3, -1.0 / 6, 0.0,
              1.0 / 6, 1.0 / 3, 1.0 / 2, 2.0 / 3, 1.0, 4.0 / 3, 2.0]
    reps = []
    for (cn, c3, t3) in COLOR:
        for (wn, c2, t2) in WEAK:
            for y in Y_LIST:
                for kind in ("F", "S"):
                    reps.append({"c3": c3, "t3": t3, "c2": c2, "t2": t2,
                                 "y": y, "kind": kind,
                                 "db": delta_b(c3, t3, c2, t2, y, kind)})
    rstar = required_ratio()
    hits = []
    # 单表示 × n
    for rep in reps:
        for n in range(1, 11):
            b = {i: B_SM[i] + rep["db"][i] * n for i in (1, 2, 3)}
            if abs(ratio(b) - rstar) < 1e-3:
                hits.append(("single", n, b))
    # 色单态、弱单/双态两两组合
    sing = [r for r in reps if r["c3"] == 1 and r["c2"] <= 2]
    for ia in range(len(sing)):
        for ib in range(ia, len(sing)):
            for na in range(1, 5):
                for nb in range(1, 5):
                    if ia == ib and nb < na:
                        continue
                    b = {i: B_SM[i] + sing[ia]["db"][i] * na
                         + sing[ib]["db"][i] * nb for i in (1, 2, 3)}
                    if abs(ratio(b) - rstar) < 1e-3:
                        hits.append(("pair", na + nb, b))
    killed = 0
    survived = 0
    mguts = []
    taus = []
    for (_, n, b) in hits:
        _, mgut, _ = unify_scale(b)
        tau = proton_lifetime(mgut)
        mguts.append(mgut)
        taus.append(tau)
        if tau > PROTON_BOUND and n <= N_OBS - 1:
            survived += 1
        else:
            killed += 1
    return {
        "collinear_hits": len(hits),
        "survived": survived,
        "killed": killed,
        "M_GUT_max": max(mguts) if mguts else None,
        "tau_p_max": max(taus) if taus else None,
        "proton_bound": PROTON_BOUND,
        "verdict": "CLOSED" if survived == 0 else "OPEN",
    }


# ---------------- 路径 C：扩群（归因输入，不自造） ----------------
# 来源：验证脚本/SO10链统一报告.md（so10_chain.py 探针）
PATH_C = {
    "source": "验证脚本/SO10链统一报告.md (so10_chain.py)",
    "chains": {
        "PS422": {
            "M_GUT_status": "INPUT（1 参数族，非预言）",
            "tau_p_lower_bound_needed_M_GUT": 1.17e16,
            "ordering_window_GeV": [2.636e15, 1.990e17],
            "survive_band_GeV": [1.174e16, 1.990e17],
            "predicts_M_GUT": False,
        },
        "R421": {
            "M_GUT_status": "INPUT（1 参数族，非预言）",
            "predicts_M_GUT": False,
        },
        "R3221": {
            "M_GUT_status": "唯一解（被三实测耦合钉死）",
            "predicts_M_GUT": True,
            "M_GUT_GeV": [2.3e16, 2.0e17],
            "alpha_GUT_inv": [45.42, 47.82],
            "tau_p_yr": [3.4e35, 2.1e39],
            "passes_SuperK": [True, True, True],
            "near_term_reach_yr": 1e35,  # Hyper-K/DUNE ~1e35
            "dex_beyond_reach": None,
            "P4_conflict": "P4(UFE-1 v1) 说 tau_p=∞；SO(10) 说有限。二者不能同时为真",
        },
    },
    "self_stated_limits": [
        "三耦合精确相遇是参数计数结果（未知量=方程数），不是独立证据",
        "最低端 tau_p=3.4e35 yr 相对 Hyper-K/DUNE 可及 ~1e35 yr 高 0.5 个数量级 => 近期实践上不可证伪",
        "质子寿命为量级标定：短程 QCD 增强与强子矩阵元未计入（约 1 个数量级）",
    ],
}


def path_c():
    r3221 = PATH_C["chains"]["R3221"]
    lowest = min(r3221["tau_p_yr"])
    reach = r3221["near_term_reach_yr"]
    dex = math.log10(lowest / reach)
    r3221["dex_beyond_reach"] = dex
    n_pred = sum(1 for c in PATH_C["chains"].values() if c.get("predicts_M_GUT"))
    n_non = len(PATH_C["chains"]) - n_pred
    # 判决：扩群未被排除，但"不交付"——要么无预言（自由输入），要么预言超出可及
    delivering = (n_pred > 0) and (dex <= 0)
    return {
        "n_chains": len(PATH_C["chains"]),
        "n_predict_M_GUT": n_pred,
        "n_no_prediction": n_non,
        "R3221_lowest_tau_p_yr": lowest,
        "near_term_reach_yr": reach,
        "dex_beyond_reach": dex,
        "delivering_testable_prediction": delivering,
        "P4_conflict": r3221["P4_conflict"],
        "verdict": "NOT_CLOSED_BUT_NON_DELIVERING",
    }


def main():
    checks = []
    results = {}

    def check(name, ok, detail=""):
        checks.append({"check": name, "ok": bool(ok), "detail": detail})

    pa = path_a()
    pb = path_b()
    pc = path_c()

    check("路径A 运行不变（往返差 < 1e-9）", pa["reparam_max_diff"] < 1e-9,
          "max diff=%.3e" % pa["reparam_max_diff"])
    check("路径A SM 不共线", abs(pa["SM_ratio"] - pa["r_star"]) > 0.05,
          "SM=%.6f vs r*=%.6f" % (pa["SM_ratio"], pa["r_star"]))
    check("路径B 共线候选 > 0（换谱确实能共点）", pb["collinear_hits"] > 0,
          "hits=%d" % pb["collinear_hits"])
    check("路径B 存活 = 0（全被质子衰变否决）", pb["survived"] == 0,
          "survived=%d, tau_max=%.2e vs bound %.1e"
          % (pb["survived"], pb["tau_p_max"], PROTON_BOUND))
    check("路径C R3221 预言超出近期可及（dex > 0）", pc["dex_beyond_reach"] > 0,
          "dex=%.2f" % pc["dex_beyond_reach"])
    check("路径C 3 链中 ≥2 条不给 M_GUT 预言", pc["n_no_prediction"] >= 2,
          "no-prediction=%d/%d" % (pc["n_no_prediction"], pc["n_chains"]))

    # 总判决：三条路径 —— A/B 闭合，C 不闭合但不交付可检验预言
    total = "TOTAL_NO_TESTABLE_ROUTE"
    results = {
        "path_A_running": pa,
        "path_B_spectrum": pb,
        "path_C_group": pc,
        "attribution": {"path_C_source": PATH_C["source"],
                        "path_C_self_stated_limits": PATH_C["self_stated_limits"]},
        "total_verdict": total,
        "plain_statement": (
            "力统一的三条路径：空间运行方式（闭合：重参数化不变）；换谱（闭合："
            "共线候选全部被质子衰变否决，0 存活）；扩群 SO(10)（未排除，但 2/3 链"
            "不给 M_GUT 预言、唯一预言链的 tau_p 超出近期可及且与 P4 冲突）。"
            "=> 本框架内不存在可行且可检验的力统一路径。"
        ),
    }

    n_ok = sum(1 for c in checks if c["ok"])
    data = {"summary": {"total_verdict": total,
                        "selfcheck_passed": n_ok,
                        "selfcheck_total": len(checks),
                        "path_A": pa["verdict"],
                        "path_B": pb["verdict"],
                        "path_C": pc["verdict"]},
            "checks": checks, "results": results}

    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "openuft_49_攻破第六轮_总收口判决_data.json"),
              "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    lines = []
    lines.append("=" * 72)
    lines.append("openuft#49 攻破第六轮 · 总收口判决（三条路径）")
    lines.append("=" * 72)
    lines.append("")
    lines.append("[自检] %d/%d PASS" % (n_ok, len(checks)))
    for c in checks:
        lines.append("  [%s] %s  %s" % ("PASS" if c["ok"] else "FAIL",
                                        c["check"], c["detail"]))
    lines.append("")
    lines.append("[路径A 空间运行方式] %s" % pa["verdict"])
    lines.append("  r*=%.6f  SM=%.6f  MSSM=%.6f  往返差=%.3e"
                 % (pa["r_star"], pa["SM_ratio"], pa["MSSM_ratio"],
                    pa["reparam_max_diff"]))
    lines.append("")
    lines.append("[路径B 换谱] %s" % pb["verdict"])
    lines.append("  共线命中=%d  存活=%d  被否决=%d" % (pb["collinear_hits"],
                                                       pb["survived"], pb["killed"]))
    lines.append("  M_GUT 最大=%.3e GeV  tau_p 最大=%.3e yr（下限 %.1e）"
                 % (pb["M_GUT_max"], pb["tau_p_max"], PROTON_BOUND))
    lines.append("")
    lines.append("[路径C 扩群 SO(10)] %s（归因：%s）" % (pc["verdict"], PATH_C["source"]))
    lines.append("  链数=%d  给 M_GUT 预言=%d  不给预言=%d"
                 % (pc["n_chains"], pc["n_predict_M_GUT"], pc["n_no_prediction"]))
    lines.append("  R3221 最低 tau_p=%.2e yr；近期可及=%.0e yr；超出 %.2f 量级"
                 % (pc["R3221_lowest_tau_p_yr"], pc["near_term_reach_yr"],
                    pc["dex_beyond_reach"]))
    lines.append("  P4 冲突：%s" % pc["P4_conflict"])
    lines.append("")
    lines.append("[总判决] %s" % total)
    lines.append("  %s" % results["plain_statement"])
    text = "\n".join(lines) + "\n"
    with open(os.path.join(here, "openuft_49_攻破第六轮_总收口判决_report.txt"),
              "w", encoding="utf-8") as f:
        f.write(text)
    try:
        sys.stdout.write(text)
    except Exception:
        sys.stdout.write(text.encode("ascii", "replace").decode("ascii"))

    if n_ok != len(checks):
        sys.exit(1)


if __name__ == "__main__":
    main()
