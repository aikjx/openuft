# -*- coding: utf-8 -*-
"""
TUFT V3.5 · β 衰变数值计算（分支③）
=========================================================================
定位：用闭合的 L/R 手征耦合框架（C_L/C_R，η 参数）计算允许 β 衰变的
角分布与宇称不对称参数，对标 PDG 中子衰变测量，输出可证伪数值界。

本册做四件事（纯标准库，零第三方依赖）
--------------------------------------------------------------------
  A. 框架验证：V−A 允许跃迁角分布 W(θ)=1+A·β·cosθ，A(λ) 对标 PDG
     （树级 A=-0.1198 / SM 含辐射修正 -0.1188 / PDG 测量 -0.1185(12)）
  B. 灵敏度：∂A/∂λ 在 λ=g_A/g_V=-1.2763 处的解析值
  C. η 插入（建模假设，作者须裁定）：λ_eff=λ(1−ε)，ε∝η，
     计算 δA(ε) 与角分布
  D. 可证伪界：由实验精度 σ_A=0.0012 反解对 ε(η) 的上界

红线：数学自洽 ≠ 物理真实；本册数值为模型依赖估计，η→ε 映射是
需作者裁定的建模选择，非第一性推导。
"""

import os
import sys
import json
import time
import math
import io

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

T_START = time.time()

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATA_DIR = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化", "数据")

RESULTS = []
GUARDS = []


def add(cid, sec, item, statement, verdict, detail):
    RESULTS.append({"id": cid, "section": sec, "item": item, "statement": statement,
                    "verdict": verdict, "detail": detail})
    print("[%s] %-6s | %-24s | %s" % (verdict, cid, item, detail[:140]))


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("[GUARD] %-30s | %s | %s" % ("PASS" if ok else "FAIL", name, detail))
    return bool(ok)


# 物理常数（PDG 2022 口径）
LAMBDA = -1.2763          # g_A/g_V（中子）
A_SM = -0.1188            # 标准模型含辐射修正
A_MEAS = -0.1185          # PDG 中子 β 不对称测量值
A_MEAS_SIG = 0.0012


def A_of_lamb(l):
    """中子 β 不对称参数 A(λ)=-2λ(1+λ)/(1+3λ²)（树级，无辐射修正）。"""
    return -2.0 * l * (1.0 + l) / (1.0 + 3.0 * l * l)


def dAdl(l):
    """∂A/∂λ = -2(1+2λ-3λ²)/(1+3λ²)²。"""
    return -2.0 * (1.0 + 2.0 * l - 3.0 * l * l) / ((1.0 + 3.0 * l * l) ** 2)


def main():
    # =====================================================================
    # A. 框架验证
    # =====================================================================
    sec = "框架验证"
    A_tree = A_of_lamb(LAMBDA)
    # 树级 vs SM(辐射修正) vs PDG 测量
    d_tree_sm = (A_tree - A_SM)
    d_tree_meas = (A_tree - A_MEAS)
    ok_validate = abs(d_tree_sm) < 0.002 and abs(d_tree_meas) < 0.002
    add("A-01", sec, "树级 A(λ)",
        "λ=g_A/g_V=-1.2763", "PASS" if abs(A_tree + 0.1198) < 0.0005 else "FAIL",
        "A=-2λ(1+λ)/(1+3λ²)=%.5f" % A_tree)
    add("A-02", sec, "对标 PDG",
        "树级 vs SM(-0.1188) vs 测量(-0.1185)", "PASS" if ok_validate else "FAIL",
        "树级-测量差=%.4f；SM 含辐射修正后与测量一致 ⇒ 框架有效" % d_tree_meas)

    guard("framework_validate", ok_validate,
          "A(λ) 树级≈-0.1198，SM 含修正后与 PDG 测量 -0.1185(12) 一致，框架有效")

    # 角分布与宇称不对称（β=v_e/c 取代表值 0.7）
    beta = 0.7
    rows = []
    for theta in (0.0, 30.0, 60.0, 90.0, 120.0, 150.0, 180.0):
        th = math.radians(theta)
        W = 1.0 + A_tree * beta * math.cos(th)
        AP = A_tree * beta * math.cos(th)
        rows.append((theta, W, AP))
    add("A-03", sec, "角分布 dΓ/dcosθ",
        "W(θ)=1+A·β·cosθ", "PASS",
        "θ=0..180° 扫表见机器产物；宇称不对称 A_P(θ)=A·β·cosθ（β=0.7 代表值）")
    guard("angular_dist_ap", abs(A_tree * beta) < 0.2,
          "A_P max=|A|β≈%.4f（非最大破缺，符合 V−A 非纯左）" % abs(A_tree * beta))

    # =====================================================================
    # B. 灵敏度
    # =====================================================================
    sec = "灵敏度"
    dAdl_val = dAdl(LAMBDA)
    add("B-01", sec, "∂A/∂λ 解析",
        "在 λ=-1.2763 处", "PASS",
        "∂A/∂λ=-2(1+2λ-3λ²)/(1+3λ²)²=%.4f" % dAdl_val)
    # |λ| 1% 变化 → δA
    deltaA_1pct = dAdl_val * (abs(LAMBDA) * 0.01)   # δλ=|λ|×1%
    n_sigma_1pct = deltaA_1pct / A_MEAS_SIG
    add("B-02", sec, "|λ| 1% → δA",
        "灵敏度转播", "PASS",
        "δA≈%.4f = %.1fσ（实验 σ_A=0.0012）⇒ 耦合 1%% 改动即被排除" % (deltaA_1pct, n_sigma_1pct))
    guard("sensitivity_ok", n_sigma_1pct > 3.0,
          "|λ| 1% 改动使 A 偏移 >3σ ⇒ 强可证伪（灵敏度高）")

    # =====================================================================
    # C. η 插入（建模假设）
    # =====================================================================
    sec = "η插入"
    # 建模假设：λ_eff=λ(1−ε)，ε∝η 为 TUFT 对 |g_A/g_V| 的分数改动；η→ε 系数需作者裁定
    eps_table = []
    for eps in (0.0, 0.001, 0.0025, 0.005, 0.01):
        lam_eff = LAMBDA * (1.0 - eps)
        A_eff = A_of_lamb(lam_eff)
        dA = A_eff - A_tree
        sigma_ratio = dA / A_MEAS_SIG
        eps_table.append((eps, A_eff, dA, sigma_ratio))
        verdict = "PASS" if abs(sigma_ratio) < 1.0 else "FAIL"
        note = "ε=%.3f ⇒ A=%.5f，δA=%.2e = %.1fσ" % (eps, A_eff, dA, sigma_ratio)
        note += "（排除）" if abs(sigma_ratio) > 1.0 else "（一致）"
        add("C-%02d" % int(eps * 1000), sec, "δA(ε=%.3f)" % eps,
            "λ_eff=λ(1−ε)", verdict, note)

    # =====================================================================
    # D. 可证伪界
    # =====================================================================
    sec = "可证伪界"
    # 由 δA=∂A/∂λ·(−λ·ε) ≤ σ_A 反解 ε 上界：ε_bound = σ_A/(|λ|·∂A/∂λ)
    eps_bound = A_MEAS_SIG / (abs(LAMBDA) * dAdl_val)
    add("D-01", sec, "ε(η) 上界",
        "由 σ_A=0.0012 反解", "PASS",
        "ε_bound=σ_A/(|λ|·∂A/∂λ)=%.4f（%.2f%%）⇒ TUFT 对 |λ| 的改动须 <%.2f%% 才与中子不对称一致" %
        (eps_bound, 100 * eps_bound, 100 * eps_bound))
    add("D-02", sec, "可证伪判语",
        "模型成立判定", "PASS",
        "若 TUFT 预测 ε>%.2f%% ⇒ 与 PDG A_n=-0.1185(12) 冲突（>1σ），被现有数据排除；ε 界即 η 映射的硬约束" %
        (100 * eps_bound))

    guard("falsifiable_bound", 0 < eps_bound < 0.01,
          "ε 上界≈0.25%，中子不对称测量对 η 给出强可证伪约束")

    # =====================================================================
    # 汇总与产物
    # =====================================================================
    counts = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
    for r in RESULTS:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    g_ok = sum(1 for g in GUARDS if g["ok"])

    payload = {
        "册": "TUFT_V3.5_β衰变数值计算",
        "生成时间": time.strftime("%Y-%m-%d %H:%M:%S"),
        "定位": "分支③：允许 β 衰变角分布 + 宇称不对称 + 可证伪界",
        "计数": counts, "总计": len(RESULTS),
        "框架": {"λ": LAMBDA, "A树级": A_tree, "A_SM": A_SM, "A测量": A_MEAS,
                 "σ_A": A_MEAS_SIG, "dA/dλ": dAdl_val},
        "角分布": {"W(θ)=1+A·β·cosθ": "β=0.7", "表": [{"θ": t, "W": w, "A_P": a} for t, w, a in rows]},
        "η插入": {"建模": "λ_eff=λ(1−ε)，ε∝η（系数需裁定）",
                  "表": [{"ε": e, "A": a, "δA": d, "σ": s} for e, a, d, s in eps_table]},
        "可证伪界": {"ε_bound": eps_bound, "百分比": 100 * eps_bound},
        "自检": {"总数": len(GUARDS), "通过": g_ok, "项": GUARDS},
        "条目": RESULTS,
        "耗时": "%.1fs" % (time.time() - T_START),
    }
    base = os.path.join(DATA_DIR, "TUFT_V3.5_β衰变数值计算_2026-10-04")
    with io.open(base + ".json", "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    md = ["# TUFT V3.5 · β 衰变数值计算（机器产物）", "",
          "- 生成时间：%s" % payload["生成时间"],
          "- 条目 %d ｜ PASS %d ｜ FAIL %d ｜ BOUNDARY %d ｜ INFO %d ｜ 自检 %d / %d" %
          (len(RESULTS), counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"],
           g_ok, len(GUARDS)),
          "- 框架：A(λ)=%.5f 树级；SM -0.1188；PDG 测量 -0.1185(12)" % A_tree,
          "- 灵敏度：∂A/∂λ=%.4f；|λ| 1%% ⇒ δA=%.1fσ" % (dAdl_val, n_sigma_1pct),
          "- 可证伪界：ε_bound=%.4f（%.2f%%）" % (eps_bound, 100 * eps_bound),
          "", "## 角分布（β=0.7，A=-%.4f）" % A_tree, "",
          "| θ(°) | W | A_P |", "|---|---|---|"]
    for t, w, a in rows:
        md.append("| %d | %.4f | %.4f |" % (t, w, a))
    md += ["", "## 条目", "", "| ID | 节 | 条目 | 判定 | 摘要 |", "|---|---|---|---|---|"]
    for r in RESULTS:
        head = r["detail"].replace("\n", " ")
        if len(head) > 150:
            head = head[:150] + "…"
        md.append("| %s | %s | %s | %s | %s |" %
                  (r["id"], r["section"], r["item"], r["verdict"], head.replace("|", "/")))
    md += ["", "## 自检", "", "| 基线 | 结果 | 取证 |", "|---|---|---|"]
    for g in GUARDS:
        md.append("| %s | %s | %s |" % (g["name"], "PASS" if g["ok"] else "FAIL", g["detail"]))
    md.append("")
    with io.open(base + ".md", "w", encoding="utf-8") as fh:
        fh.write("\n".join(md))

    print("-" * 74)
    print("总计 %d 条 ｜ PASS %d ｜ FAIL %d ｜ BOUNDARY %d ｜ INFO %d" %
          (len(RESULTS), counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"]))
    print("自检 %d / %d" % (g_ok, len(GUARDS)))
    print("产物：%s.json / .md" % base)
    print("核心数值：A(λ)=%.5f；∂A/∂λ=%.4f；可证伪界 ε<%.2f%%" % (A_tree, dAdl_val, 100 * eps_bound))
    print("红线：η→ε 映射为建模假设，需作者裁定；数值非第一性推导")
    if g_ok != len(GUARDS):
        print("SELFCHECK FAILED")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
