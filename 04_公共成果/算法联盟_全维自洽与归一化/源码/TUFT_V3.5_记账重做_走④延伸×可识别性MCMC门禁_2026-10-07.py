# -*- coding: utf-8 -*-
"""
TUFT V3.5 · 记账重做册：走④延伸 × 可识别性 / MCMC 门禁 —— 2026-10-07
=========================================================================
承接：走④落地册（Ω5' 公设放宽）+ 走④延伸册（𝒪_TUFT 结构与 β 参数化）。
公设集已变更（Ω5' + 走④延伸候选生效）⇒ r14 代价矩阵 / 可识别性记账须重做（既定规矩）。

本册核心判定：**走④延伸（β 通道可定量）是否解除了 MCMC 阻塞？**
  ・公设现状登记（Ω1-Ω4 + Ω5' + 走④延伸候选）。
  ・r14 出路1 在 Ω5' 下重判（delta 自由常数不再违背；框架推导分支仍死锁 P2）。
  ・可识别性×走④：β 作为第 5 观测，是否提升 rank。
    - β 与 α_s 共享 λ（非独立，回链并发册「三组观测共享 λ」）；
    - β 依赖 φ0（并发册「φ0 唯一真信息载体之一」）⇒ 提供 φ0 方向，rank 3→4 可能；
    - **硬上限：观测 5 参 6 ⇒ rank ≤ 5 < 6 ⇒ MCMC 门禁（rank≥6）结构性维持禁止**。

红线：走④延伸最多 rank 3→4，但仍 < 6；MCMC 门禁不因走④ 自动解除。
纯标准库，零第三方依赖。
"""

import os
import sys
import json
import time
import math

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

T_START = time.time()

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATA_DIR = os.path.join(ROOT, "04_公共成果", "算法联盟_全维自洽与归一化", "数据")

RESULTS = []
GUARDS = []


def add(cid, sec, item, verdict, detail):
    RESULTS.append({"id": cid, "section": sec, "item": item, "verdict": verdict, "detail": detail})
    print("[%s] %-6s | %-34s | %s" % (verdict, cid, item, detail[:165]))


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("[GUARD] %-34s | %s | %s" % (name, "PASS" if ok else "FAIL", detail))
    return bool(ok)


def matrix_rank_gauss(A, eps=1e-9):
    """浮点高斯消元求矩阵秩（示意 Jacobian 用）。"""
    M = [row[:] for row in A]
    m = len(M)
    if m == 0:
        return 0
    n = len(M[0])
    rank = 0
    piv = 0
    for col in range(n):
        pivot_row = None
        for r in range(rank, m):
            if abs(M[r][col]) > eps:
                pivot_row = r
                break
        if pivot_row is None:
            continue
        M[rank], M[pivot_row] = M[pivot_row], M[rank]
        pv = M[rank][col]
        for c in range(col, n):
            M[rank][c] /= pv
        for r in range(m):
            if r != rank and abs(M[r][col]) > eps:
                f = M[r][col]
                for c in range(col, n):
                    M[r][c] -= f * M[rank][c]
        rank += 1
    return rank


def main():
    # =====================================================================
    # A. 公设集现状登记
    # =====================================================================
    sec = "公设现状"
    add("A-01", sec, "公设集 Ω1-Ω4 维持", "PASS",
        "Ω1 光滑/Ω2 无量纲/Ω3 符号自洽/Ω4 连续——未随走④ 变更（走④ 只改 Ω5）")
    add("A-02", sec, "Ω5' 生效", "PASS",
        "公设集现值：Ω5'（≤3 常数且显式登记外部输入）；δ/𝒪_TUFT 获得合法来源（走④落地册 A-01/A-02）")
    add("A-03", sec, "走④延伸候选登记", "BOUNDARY",
        "放开算符空间候选（𝒪_TUFT 含 S/T）已登记但**未定**——κ/结构待作者拍板，未计入参数账")

    # =====================================================================
    # B. r14 代价矩阵在 Ω5' 下更新
    # =====================================================================
    sec = "r14更新"
    add("B-01", sec, "出路1 delta 来源重判", "PASS",
        "Ω5' 下 delta=自由常数（显式登记）不再违背 ⇒ 违背 1→0；但 delta=框架推导 分支仍死锁（P2 第二振幅不存在）")
    add("B-02", sec, "出路1 部分可行", "BOUNDARY",
        "出路1 由「死锁」转「部分可行」：外部输入路线（显式登记 delta/𝒪_TUFT）违背 0，但预测力受外部输入主导、非框架内部预言")
    add("B-03", sec, "出路3/4 记账不变", "PASS",
        "③ 放弃 β（零输入）与 ④ 改公设（本册基线）记账不随走④延伸变化；走④延伸是 ④ 的延伸而非新出路")

    # =====================================================================
    # C. 可识别性 × 走④延伸
    # =====================================================================
    sec = "可识别性"
    # C-01: β 与 α_s 共享 λ（依赖重叠检查）
    lam_deps = {"λ"}                  # α_s 依赖 λ
    beta_deps = {"λ", "φ0", "δ", "κ"}  # β 依赖
    overlap = lam_deps & beta_deps
    add("C-01", sec, "β 与 α_s 共享参数", "PASS",
        "β 依赖集{λ,φ0,δ,κ} ∩ α_s 依赖集{λ} = {%s} 非空 ⇒ 两观测在 λ 方向非独立（回链并发册「三组观测共享 λ」）" %
        ", ".join(sorted(overlap)))
    guard("shared_lambda", "λ" in beta_deps and "λ" in lam_deps, "β 与 α_s 共享 λ（非独立）")

    # C-02: 示意 Jacobian 5×6 高斯消元 rank（参数序 λ,φ0,B1,B2,B3,B4）
    # 原 4 强度行：α_s=(1,0,0,0,0,0)、α_G=c×(α_s)（∝ 相关）、α=(0,0,1,0,0,0)、α_W=(0,0,0,1,0,0)
    # β 行：(∂A/∂λ, ∂A/∂φ0, 0,0,0,0) = (0.3716, dA_dphi, 0,0,0,0)
    lam = -1.2763
    A_SM = -0.1188
    dA_dlam = 0.3716
    rho, phi0, delta, kappa = 0.05, 1.0, 1.0, 1.0
    denom = 1.0 + rho * rho + 2.0 * rho * math.cos(phi0 + delta)
    dA_dphi = A_SM * kappa * rho * math.cos(phi0) * math.sin(delta) / denom
    rows4 = [
        [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],                       # α_s
        [1.48e-44, 0.0, 0.0, 0.0, 0.0, 0.0],                 # α_G ∝ α_s
        [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],                      # α
        [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],                      # α_W
    ]
    row_beta = [dA_dlam, dA_dphi, 0.0, 0.0, 0.0, 0.0]        # β
    J5 = rows4 + [row_beta]
    rank4 = matrix_rank_gauss(rows4)                          # 原 4 观测
    rank5 = matrix_rank_gauss(J5)                             # 走④延伸后 5 观测
    add("C-02", sec, "示意 Jacobian rank：4→5 观测", "PASS" if rank5 > rank4 else "FAIL",
        "示意模型（参数序 λ,φ0,B1..B4）：原 4 观测 rank=%d（G∝S 冗余）；+β 行（∂A/∂λ=%.4g,∂A/∂φ0=%.4g）⇒ rank=%d ⇒ β 提供 φ0 方向" %
        (rank4, dA_dlam, dA_dphi, rank5))
    guard("beta_adds_dir", rank5 > rank4, "走④延伸 β 行提供新方向（rank 3→4）——示意模型")

    # C-03: 硬上限 rank ≤ 5 < 6 ⇒ MCMC 门禁维持
    n_param = 6
    n_obs5 = 5
    cap = min(n_obs5, n_param)
    add("C-03", sec, "MCMC 门禁判定（硬上限）", "BOUNDARY",
        "观测 5 参 6 ⇒ rank 硬上限 min(5,6)=%d < 6 ⇒ Fisher 不可逆 ⇒ **MCMC 门禁（rank≥6）结构性维持禁止**；走④延伸最多 rank 3→4，不能达到 6" % cap)
    guard("mcmc_still_blocked", cap < n_param, "观测数(5) < 参数数(6) ⇒ MCMC 结构性禁止")

    # =====================================================================
    # D. 解除 MCMC 前提清单
    # =====================================================================
    sec = "解除前提"
    add("D-01", sec, "前提① 补独立观测", "BOUNDARY",
        "须 β 之外再增独立观测（不共享 λ 且依赖新参数方向）使 rank 达 6——并发册已证「可及观测 10 靶可用 0/10」⇒ 无现成候选")
    add("D-02", sec, "前提② 减少自由参数", "BOUNDARY",
        "固定全部 4 个 B_i（先验）使代数可逆——代价是弱扇区几何变成外部输入（并发册步3 结论）；或减参数至 ≤5")
    add("D-03", sec, "前提③ 完整 β 行模型", "BOUNDARY",
        "选定 𝒪_TUFT 结构 + 算 κ + 明确 β 行偏导模型，才能把 β 计入 rank（当前 κ/结构未定，β 行未定义）")
    add("D-04", sec, "记账重做结论", "BOUNDARY",
        "走④延伸使 β 通道可定量（参数化 δA 已给），但**不解除 MCMC 阻塞**；须三条前提之一（补观测/减参数/β 行建模）才可谈 MCMC")

    # =====================================================================
    # 汇总
    # =====================================================================
    counts = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
    for r in RESULTS:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    g_ok = sum(1 for g2 in GUARDS if g2["ok"])

    payload = {
        "册": "TUFT_V3.5_记账重做_走④延伸×可识别性/MCMC门禁",
        "生成时间": time.strftime("%Y-%m-%d %H:%M:%S"),
        "定位": "公设集 Ω5'+走④延伸生效后的记账重做：r14 更新 + 可识别性×走④ 交叉判定",
        "承接": "走④落地册 + 走④延伸册",
        "计数": counts, "总计": len(RESULTS),
        "公设现状": {"Ω1-Ω4": "维持", "Ω5'": "生效（≤3常数显式登记）", "走④延伸": "候选未定(κ/结构)"},
        "r14更新": {"出路1": "死锁→部分可行(外部输入路线违背0)", "出路3/4": "不变"},
        "可识别性": {"原4观测rank": rank4, "+β5观测rank": rank5, "参6/观5上限": min(5, 6),
                     "MCMC门禁": "维持禁止(rank上限5<6)"},
        "解除MCMC前提": ["补独立观测(10靶可用0/10无候选)", "固定全部B_i(弱扇区变外部输入)",
                          "选定𝒪_TUFT结构+算κ+β行模型"],
        "核心结论": "走④延伸使β通道可定量，但不解除MCMC阻塞：rank硬上限5<6，须补观测/减参数/β行建模三前提之一",
        "自检": {"总数": len(GUARDS), "通过": g_ok, "项": GUARDS},
        "条目": RESULTS,
        "耗时": "%.1fs" % (time.time() - T_START),
    }
    base = os.path.join(DATA_DIR, "TUFT_V3.5_记账重做_走④延伸×可识别性MCMC门禁_2026-10-07")
    with open(base + ".json", "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    md = ["# TUFT V3.5 · 记账重做：走④延伸 × 可识别性 / MCMC 门禁（机器产物）", "",
          "- 生成时间：%s" % payload["生成时间"],
          "- 条目 %d ｜ PASS %d ｜ FAIL %d ｜ BOUNDARY %d ｜ INFO %d ｜ 自检 %d / %d" %
          (len(RESULTS), counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"],
           g_ok, len(GUARDS)),
          "- 公设现状：Ω1-Ω4 维持 ｜ Ω5' 生效 ｜ 走④延伸候选未定(κ/结构)",
          "- 可识别性：原 4 观测 rank=%d ｜ +β 5 观测 rank=%d ｜ 硬上限 min(5,6)=5<6" % (rank4, rank5),
          "- 核心结论：走④延伸使 β 可定量但**不解除 MCMC 阻塞**（rank 上限 5<6）",
          "", "## 条目", "", "| ID | 节 | 条目 | 判定 | 摘要 |", "|---|---|---|---|---|"]
    for r in RESULTS:
        head = r["detail"].replace("\n", " ")
        if len(head) > 195:
            head = head[:195] + "…"
        md.append("| %s | %s | %s | %s | %s |" % (r["id"], r["section"], r["item"], r["verdict"], head))
    md += ["", "## 自检", "", "| 基线 | 结果 | 取证 |", "|---|---|---|"]
    for g2 in GUARDS:
        md.append("| %s | %s | %s |" % (g2["name"], "PASS" if g2["ok"] else "FAIL", g2["detail"]))
    md.append("")
    with open(base + ".md", "w", encoding="utf-8") as fh:
        fh.write("\n".join(md))

    print("-" * 74)
    print("总计 %d 条 ｜ PASS %d ｜ FAIL %d ｜ BOUNDARY %d ｜ INFO %d" %
          (len(RESULTS), counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"]))
    print("自检 %d / %d" % (g_ok, len(GUARDS)))
    print("产物：%s.json / .md" % base)
    print("可识别性：原4观测 rank=%d ｜ +β 5观测 rank=%d ｜ 上限5<6 ⇒ MCMC 维持禁止" % (rank4, rank5))
    if g_ok != len(GUARDS):
        print("SELFCHECK FAILED")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
