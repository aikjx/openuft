# -*- coding: utf-8 -*-
"""
================================================================================
openuft#49 攻破第五轮 · 「换谱」路径完备扫描（共线判据 + 质子衰变 + 参数计数）
================================================================================
第四轮已证：只有改变粒子谱 b_i 才能改变力统一判决（空间运行方式=重参数化，不变）。
本轮正面扫描「换谱」这条路是否走得通：

  一圈共线判据（第四轮主定理）：
      r ≡ (b2-b1)/(b3-b1)  必须等于  r* ≡ (A2-A1)/(A3-A1)
  其中 A_i = α_i^{-1}(M_Z) 为实测。

  扫描对象：SM 表示 (R3,R2)_Y 上的新 Weyl 费米子 / 复标量，单表示 × n 份，
           以及色单态低维表示的少量组合。
  三道门同时施加：
      G-collinear :  |r - r*| < 1e-3
      G-proton    :  τ_p ≈ (M_GUT/2e16)^4 × 1e35 yr  >  1.6e34 yr (Super-K)
      G-parameter :  新多重态数 n_new  <=  n_obs - 1 = 7

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

# 实测（GUT 归一化）α_i^{-1}(M_Z)
A = {1: 59.0209, 2: 29.5838, 3: 8.47458}
AS_MZ, AS_SIG = 0.1180, 0.0009

# 1-loop β（da^{-1}/dlnμ = -b/2π）
B_SM = {1: 41.0 / 10.0, 2: -19.0 / 6.0, 3: -7.0}
B_MSSM = {1: 33.0 / 5.0, 2: 1.0, 3: -3.0}

PROTON_BOUND = 1.6e34  # yr, Super-K
N_OBS = 8
N_FREE_MAX = N_OBS - 1

# 表示：(名称, SU3 dim, SU3 T, SU2 dim, SU2 T)
COLOR = [
    ("1", 1, 0.0),
    ("3", 3, 0.5),
    ("8", 8, 3.0),
]
WEAK = [
    ("1", 1, 0.0),
    ("2", 2, 0.5),
    ("3", 3, 2.0),
]
# 超荷 Y（Q = T3 + Y 约定）
Y_LIST = [-1.0, -2.0 / 3, -1.0 / 2, -1.0 / 3, -1.0 / 6,
          0.0, 1.0 / 6, 1.0 / 3, 1.0 / 2, 2.0 / 3,
          1.0, 4.0 / 3, 2.0]


def required_ratio():
    return (A[2] - A[1]) / (A[3] - A[1])


def ratio(b):
    den = b[3] - b[1]
    if abs(den) < 1e-15:
        return float("inf")
    return (b[2] - b[1]) / den


def delta_b(c3, t3, c2, t2, y, kind):
    """单个新多重态的一圈 β 贡献。
    kind='F'（Weyl 费米子，系数 2/3）或 'S'（复标量，系数 1/3）。
    T1 = (3/5) Y^2 * dim3 * dim2。
    """
    coef = 2.0 / 3.0 if kind == "F" else 1.0 / 3.0
    d3, d2 = c3, c2
    T3 = t3 * d2
    T2 = t2 * d3
    T1 = (3.0 / 5.0) * y * y * d3 * d2
    return {1: coef * T1, 2: coef * T2, 3: coef * T3}


def b_sm_anchor():
    """用公式复算 SM 的 b=(41/10,-19/6,-7) 做自检。"""
    f = []
    # Q_L(3,2,1/6), u_R(3,1,2/3), d_R(3,1,-1/3), L(1,2,-1/2), e_R(1,1,-1), nu_R(1,1,0)
    f.append((3, 0.5, 2, 0.5, 1.0 / 6, "F"))
    f.append((3, 0.5, 1, 0.0, 2.0 / 3, "F"))
    f.append((3, 0.5, 1, 0.0, -1.0 / 3, "F"))
    f.append((1, 0.0, 2, 0.5, -1.0 / 2, "F"))
    f.append((1, 0.0, 1, 0.0, -1.0, "F"))
    f.append((1, 0.0, 1, 0.0, 0.0, "F"))
    b = {1: 0.0, 2: -11.0 / 3.0 * 2.0, 3: -11.0 / 3.0 * 3.0}
    for (c3, t3, c2, t2, y, k) in f:
        d = delta_b(c3, t3, c2, t2, y, k)
        for i in (1, 2, 3):
            b[i] += 3.0 * d[i]  # 3 代
    # Higgs (1,2,1/2) 复标量
    d = delta_b(1, 0.0, 2, 0.5, 1.0 / 2, "S")
    for i in (1, 2, 3):
        b[i] += d[i]
    return b


def collinear(b, tol=1e-3):
    return abs(ratio(b) - required_ratio()) < tol


def unify_scale(b):
    """返回 (u12, M_GUT, alpha_GUT^{-1})；要求 b1!=b2。"""
    if abs(b[1] - b[2]) < 1e-15:
        return None
    u12 = TWO_PI * (A[1] - A[2]) / (b[1] - b[2])
    mgut = MZ * math.exp(u12)
    agut_inv = A[1] - (b[1] / TWO_PI) * u12
    return u12, mgut, agut_inv


def proton_lifetime(mgut):
    """粗略维度-6 估计（与 R12 同口径）：τ_p ≈ (M_GUT/2e16)^4 × 1e35 yr。"""
    return (mgut / 2.0e16) ** 4 * 1.0e35


def build_rep_catalog():
    reps = []
    for (cn, c3, t3) in COLOR:
        for (wn, c2, t2) in WEAK:
            for y in Y_LIST:
                for kind in ("F", "S"):
                    reps.append({
                        "name": "(%s,%s)_%g/%s" % (cn, wn, y, kind),
                        "c3": c3, "t3": t3, "c2": c2, "t2": t2,
                        "y": y, "kind": kind,
                        "db": delta_b(c3, t3, c2, t2, y, kind),
                        "nstates": c3 * c2,
                    })
    return reps


def eval_content(dbs, n_multiplet):
    """dbs: list of delta_b dict（含各自重数已乘）。"""
    b = dict(B_SM)
    for d in dbs:
        for i in (1, 2, 3):
            b[i] += d[i]
    r = ratio(b)
    rstar = required_ratio()
    coll = abs(r - rstar) < 1e-3
    out = {
        "b": [b[1], b[2], b[3]],
        "ratio": r,
        "collinear": coll,
        "n_new": n_multiplet,
    }
    if coll:
        us = unify_scale(b)
        if us:
            u12, mgut, agut_inv = us
            tau = proton_lifetime(mgut)
            out["M_GUT"] = mgut
            out["alpha_GUT_inv"] = agut_inv
            out["tau_p_yr"] = tau
            out["proton_ok"] = tau > PROTON_BOUND
            out["param_ok"] = n_multiplet <= N_FREE_MAX
            out["survives"] = out["proton_ok"] and out["param_ok"]
        else:
            out["M_GUT"] = None
            out["survives"] = False
    else:
        out["M_GUT"] = None
        out["survives"] = False
    return out


def main():
    results = []
    checks = []

    def rec(name, value, detail=""):
        results.append({"name": name, "value": value, "detail": detail})

    def check(name, ok, detail=""):
        checks.append({"check": name, "ok": bool(ok), "detail": detail})

    rstar = required_ratio()
    rec("required_ratio_r_star", rstar, "(A2-A1)/(A3-A1)")

    # ---------- 自检：SM/MSSM 比值与判别 ----------
    b_sm = b_sm_anchor()
    check("SM β 复算锚点 = (4.1,-3.1667,-7)",
          abs(b_sm[1] - 4.1) < 1e-9 and abs(b_sm[2] + 19.0 / 6) < 1e-9
          and abs(b_sm[3] + 7.0) < 1e-9,
          "got (%.6f,%.6f,%.6f)" % (b_sm[1], b_sm[2], b_sm[3]))
    check("SM 比值 ≠ r*（不共线）", abs(ratio(b_sm) - rstar) > 0.05,
          "SM r=%.5f vs r*=%.5f" % (ratio(b_sm), rstar))
    check("MSSM 比值 ≈ r*（共线）", abs(ratio(B_MSSM) - rstar) < 2e-3,
          "MSSM r=%.5f vs r*=%.5f" % (ratio(B_MSSM), rstar))

    # ---------- 扫描 1：单表示 × n ----------
    reps = build_rep_catalog()
    rec("catalog_size", len(reps), "表示×类型 基数")

    single_hits = []
    for rep in reps:
        for n in range(1, 11):
            d = {i: rep["db"][i] * n for i in (1, 2, 3)}
            ev = eval_content([d], n)
            if ev["collinear"]:
                single_hits.append({
                    "rep": rep["name"], "n": n,
                    "b": ev["b"], "M_GUT": ev.get("M_GUT"),
                    "tau_p_yr": ev.get("tau_p_yr"),
                    "proton_ok": ev.get("proton_ok"),
                    "param_ok": ev.get("param_ok"),
                    "survives": ev["survives"],
                })
    rec("single_rep_collinear_hits", single_hits,
        "单表示×n 命中共线的条目")

    # ---------- 扫描 2：色单态低维表示的两两组合 ----------
    singlets = [r for r in reps
                if r["c3"] == 1 and r["c2"] <= 2]  # 色单态、弱单/双态
    pair_hits = []
    for idx_a in range(len(singlets)):
        for idx_b in range(idx_a, len(singlets)):
            ra = singlets[idx_a]
            rb = singlets[idx_b]
            for na in range(1, 5):
                for nb in range(1, 5):
                    if idx_a == idx_b and nb < na:
                        continue
                    db = {i: ra["db"][i] * na + rb["db"][i] * nb for i in (1, 2, 3)}
                    n_new = na + nb
                    ev = eval_content([db], n_new)
                    if ev["collinear"]:
                        pair_hits.append({
                            "reps": [ra["name"], rb["name"]],
                            "n": [na, nb],
                            "b": ev["b"],
                            "M_GUT": ev.get("M_GUT"),
                            "tau_p_yr": ev.get("tau_p_yr"),
                            "proton_ok": ev.get("proton_ok"),
                            "param_ok": ev.get("param_ok"),
                            "survives": ev["survives"],
                        })
    rec("pair_collinear_hits_count", len(pair_hits),
        "色单态两两组合命中共线数")
    rec("pair_collinear_hits_sample", pair_hits[:40], "前 40 条")

    # ---------- 汇总三门的存活 ----------
    all_hits = single_hits + pair_hits
    survivors = [h for h in all_hits if h["survives"]]
    proton_killed = [h for h in all_hits if not h.get("proton_ok", True)]
    param_killed = [h for h in all_hits if h.get("proton_ok", False)
                    and not h.get("param_ok", True)]
    rec("total_collinear_hits", len(all_hits), "共线命中总数")
    rec("survivors", survivors, "三门同时通过")
    rec("proton_killed_count", len(proton_killed), "共线但被质子衰变否决")
    rec("param_killed_count", len(param_killed), "共线且质子过关但参数计数否决")

    # 自检：MSSM 作为控制组应通过共线、且其 M_GUT 给出 τ_p 允许；但需 SUSY（外部）
    us_m = unify_scale(B_MSSM)
    tau_m = proton_lifetime(us_m[1]) if us_m else 0.0
    check("MSSM 控制组共线且 M_GUT≈2e16", us_m is not None
          and abs(math.log10(us_m[1]) - 16.3) < 0.25,
          "M_GUT=%.3e" % (us_m[1] if us_m else 0))
    rec("MSSM_control", {"M_GUT": us_m[1] if us_m else None,
                         "tau_p_yr": tau_m,
                         "note": "需 N=1 SUSY（~105 参数），非几何导出；LHC 未见；维度-5 质子衰变排除"},
        "控制组：不是换谱（是换对称性）")

    # ---------- 判决 ----------
    # 诚实：若 survivors 非空，如实列出；若为空，判"换谱闭合"
    verdict = "PASS_spectrum_path_closed" if len(survivors) == 0 else "OPEN_survivors_found"
    summary = {
        "verdict": verdict,
        "required_ratio": rstar,
        "SM_ratio": ratio(b_sm),
        "MSSM_ratio": ratio(B_MSSM),
        "catalog_size": len(reps),
        "single_scan_entries": len(reps) * 10,
        "pair_scan_entries": len(singlets) * (len(singlets) + 1) // 2 * 16,
        "collinear_hits": len(all_hits),
        "proton_killed": len(proton_killed),
        "param_killed": len(param_killed),
        "survivors": len(survivors),
        "selfcheck_passed": 0,
        "selfcheck_total": len(checks),
    }
    summary["selfcheck_passed"] = sum(1 for c in checks if c["ok"])

    data = {"summary": summary, "checks": checks, "results": results}
    here = os.path.dirname(os.path.abspath(__file__))
    jpath = os.path.join(here, "openuft_49_攻破第五轮_换谱路径完备扫描_data.json")
    with open(jpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    lines = []
    lines.append("=" * 72)
    lines.append("openuft#49 攻破第五轮 · 换谱路径完备扫描")
    lines.append("=" * 72)
    lines.append("")
    lines.append("[自检] %d/%d PASS" % (sum(1 for c in checks if c["ok"]), len(checks)))
    for c in checks:
        lines.append("  [%s] %s  %s" % ("PASS" if c["ok"] else "FAIL",
                                        c["check"], c["detail"]))
    lines.append("")
    lines.append("[共线判据] r* = (A2-A1)/(A3-A1) = %.6f" % rstar)
    lines.append("  SM r=%.6f (差 %.4f)" % (ratio(b_sm), abs(ratio(b_sm) - rstar)))
    lines.append("  MSSM r=%.6f (差 %.5f)" % (ratio(B_MSSM), abs(ratio(B_MSSM) - rstar)))
    lines.append("")
    lines.append("[扫描规模] 表示基数=%d, 单表示×n 条目=%d, 色单态两两组合条目=%d"
                 % (len(reps), len(reps) * 10, summary["pair_scan_entries"]))
    lines.append("")
    lines.append("[共线命中] 总计 %d 条" % len(all_hits))
    lines.append("  被质子衰变否决: %d" % len(proton_killed))
    lines.append("  质子过关但参数计数否决: %d" % len(param_killed))
    lines.append("  三门同时存活: %d" % len(survivors))
    if survivors:
        lines.append("  --- 存活样本（全部如实列出）---")
        for s in survivors[:200]:
            nm = s.get("rep") or "+".join(s.get("reps", []))
            lines.append("    %s  n=%s  M_GUT=%.3e  tau_p=%.3e" %
                         (nm, s.get("n"), s["M_GUT"], s["tau_p_yr"]))
    lines.append("")
    lines.append("[控制组] MSSM: M_GUT=%.3e, tau_p~%.3e yr, 但需 N=1 SUSY（非换谱）"
                 % (us_m[1] if us_m else 0, tau_m))
    lines.append("")
    lines.append("[判决] %s" % verdict)
    text = "\n".join(lines) + "\n"
    rpath = os.path.join(here, "openuft_49_攻破第五轮_换谱路径完备扫描_report.txt")
    with open(rpath, "w", encoding="utf-8") as f:
        f.write(text)
    try:
        sys.stdout.write(text)
    except Exception:
        sys.stdout.write(text.encode("ascii", "replace").decode("ascii"))

    if summary["selfcheck_passed"] != len(checks):
        sys.exit(1)


if __name__ == "__main__":
    main()
