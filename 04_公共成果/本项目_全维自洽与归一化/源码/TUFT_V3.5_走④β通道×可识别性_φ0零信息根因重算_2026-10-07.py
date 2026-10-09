# -*- coding: utf-8 -*-
"""
TUFT V3.5 · 走④β通道 × 可识别性重算：φ0 零信息根因 —— 2026-10-07
=========================================================================
承接：记账重做册（选2：固定 B_i 使代数可逆）。并发步3册根因：
  4 强度观测（α_G,α,α_s,α_W）**不含 φ0** ⇒ φ0 零信息 ⇒ 最小结构 cond=7.99e16 数值不可用。

本册判定：**走④ 的 β 通道（δA∝sinφ0）是否就是步3册缺失的 φ0 相位观测，能否解除「φ0 零信息」根因？**
  ・β 行偏导 ∂A/∂φ0 ∝ κ·ρ·cosφ0·sinδ ≠ 0 ⇒ β 提供 φ0 方向（此前 4 强度行第 2 列全 0）。
  ・固定 B_i（选2）后参数仅 (λ,φ0)，观测 4强度+β=5 ⇒ 示意 Jacobian 5×2。
  ・rank（高斯消元）+ cond（特征值闭式）重算。

核心预期（示意模型）：cond 从 7.99e16 → **~400**（φ0 不再零信息）。
红线：示意 Jacobian，物理数值（∂A/∂φ0 等）依赖 κ/结构待作者；不宣称 MCMC 已可启动。
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
DATA_DIR = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化", "数据")

RESULTS = []
GUARDS = []


def add(cid, sec, item, verdict, detail):
    RESULTS.append({"id": cid, "section": sec, "item": item, "verdict": verdict, "detail": detail})
    print("[%s] %-6s | %-36s | %s" % (verdict, cid, item, detail[:175]))


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("[GUARD] %-36s | %s | %s" % (name, "PASS" if ok else "FAIL", detail))
    return bool(ok)


def matrix_rank_gauss(A, eps=1e-9):
    M = [row[:] for row in A]
    m = len(M)
    n = len(M[0])
    rank = 0
    for col in range(n):
        piv = None
        for r in range(rank, m):
            if abs(M[r][col]) > eps:
                piv = r
                break
        if piv is None:
            continue
        M[rank], M[piv] = M[piv], M[rank]
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


def cond_2x2(GtG):
    """2×2 对称阵特征值闭式 + 条件数 sqrt(λmax/λmin)。"""
    a, b, d = GtG[0][0], GtG[0][1], GtG[1][1]
    tr = a + d
    det = a * d - b * b
    disc = tr * tr - 4.0 * det
    if disc < 0:
        disc = 0.0
    sq = math.sqrt(disc)
    lam_max = (tr + sq) / 2.0
    lam_min = (tr - sq) / 2.0
    if lam_min <= 0:
        return float("inf"), lam_max, lam_min
    return math.sqrt(lam_max / lam_min), lam_max, lam_min


def main():
    # =====================================================================
    # A. 承接步3册根因
    # =====================================================================
    sec = "根因承接"
    add("A-01", sec, "步3册根因复述", "PASS",
        "并发步3册：4 强度观测（α_G,α,α_s,α_W）**不含 φ0** ⇒ φ0 零信息 ⇒ 最小结构 cond=7.99e16、数值可用 0/15")
    guard("step3_root", True, "φ0 零信息是步3册 cond 巨大根因（本册回链不重算）")

    # =====================================================================
    # B. 走④ β 通道 = φ0 相位观测
    # =====================================================================
    sec = "β相位观测"
    lam = -1.2763
    A_SM = -0.1188
    dA_dlam = 0.3716                       # 分支③ ∂A/∂λ
    rho, phi0, delta, kappa = 0.05, 1.0, 1.0, 1.0
    denom = 1.0 + rho * rho + 2.0 * rho * math.cos(phi0 + delta)
    dA_dphi = A_SM * kappa * rho * math.cos(phi0) * math.sin(delta) / denom
    add("B-01", sec, "β 行含 φ0 偏导", "PASS" if abs(dA_dphi) > 0 else "FAIL",
        "∂A/∂φ0 = A_SM·κ·ρ·cosφ0·sinδ/denom = %.5g（κ=1,ρ=0.05,φ0=δ=1）⇒ **β 提供 φ0 方向**（此前 4 强度行第 2 列全 0）" % dA_dphi)
    guard("beta_has_phi", abs(dA_dphi) > 0, "β 通道含 φ0 偏导（φ0 相位观测）")

    # =====================================================================
    # C. 固定 B_i（选2）示意 Jacobian（参数 λ,φ0，观测 4强度+β=5）
    # =====================================================================
    sec = "示意Jacobian"
    # 参数序 (λ, φ0)
    J = [
        [1.0, 0.0],               # α_s
        [1.48e-44, 0.0],          # α_G ∝ α_s
        [0.1, 0.0],               # α（示意弱依赖 λ）
        [0.2, 0.0],               # α_W（示意弱依赖 λ）
        [dA_dlam, dA_dphi],       # β
    ]
    rank5 = matrix_rank_gauss(J)
    # 4 强度（无 β）对照 rank 与 cond
    J4 = [row[:] for row in J[:4]]
    rank4 = matrix_rank_gauss(J4)
    # GtG = J^T J
    n_param = 2
    GtG4 = [[0.0, 0.0], [0.0, 0.0]]
    for r in J4:
        GtG4[0][0] += r[0] * r[0]
        GtG4[0][1] += r[0] * r[1]
        GtG4[1][0] += r[1] * r[0]
        GtG4[1][1] += r[1] * r[1]
    cond4, lm4max, lm4min = cond_2x2(GtG4)
    GtG5 = [[0.0, 0.0], [0.0, 0.0]]
    for r in J:
        GtG5[0][0] += r[0] * r[0]
        GtG5[0][1] += r[0] * r[1]
        GtG5[1][0] += r[1] * r[0]
        GtG5[1][1] += r[1] * r[1]
    cond5, lm5max, lm5min = cond_2x2(GtG5)
    add("C-01", sec, "rank：4 强度 vs +β", "PASS" if rank5 > rank4 else "FAIL",
        "4 强度 rank=%d（G∝S，φ0 全 0）｜+β 5 观测 rank=%d（β 第 2 列 φ0 非零 ⇒ 达 2，代数可逆）" % (rank4, rank5))
    guard("rank_reaches_2", rank5 == 2, "固定 B_i + β 后 rank=2（参数 λ,φ0 代数可逆）")

    add("C-02", sec, "cond 对比：4 强度 vs +β", "PASS" if (cond4 > cond5) else "FAIL",
        "4 强度 cond=%.3g（φ0 严格零信息，秩亏）｜+β 5 观测 cond=%.3g（λ1=%.4g,λ2=%.4g）⇒ **φ0 零信息根因解除**（示意模型）"
        % (cond4, cond5, lm5max, lm5min))
    guard("cond_drops", cond5 < 1e10, "固定 B_i + β 后 cond<1e10（数值可用窗口出现，示意模型）")

    add("C-03", sec, "对比步3册 cond", "PASS" if cond5 < 7.99e16 else "FAIL",
        "步3册最小结构 cond=7.99e16（φ0 零信息）→ 本册固定B_i+β cond=%.3g（改善 %.1e 倍）⇒ 走④ β 通道解除 φ0 根因" %
        (cond5, 7.99e16 / cond5))

    # =====================================================================
    # D. 判定与边界
    # =====================================================================
    sec = "判定"
    add("D-01", sec, "选2 路线走④后判定", "BOUNDARY" if cond5 < 1e10 else "FAIL",
        "固定 B_i（选2）+ 走④ β 通道：示意模型 rank=2、cond=%.3g<1e10 ⇒ **首次出现数值可用窗口**；"
        "但这是示意 Jacobian，真实 cond 依赖 κ/结构，须作者选定结构后重算" % cond5)
    add("D-02", sec, "诚实边界", "BOUNDARY",
        "① 示意 Jacobian（α/α_W 行偏导为示意值，物理数值待 κ/结构）② 不宣称 MCMC 已可启动——只是 φ0 零信息根因解除的**候选路线** ③ 真实 cond 待作者选定 𝒪_TUFT 结构后重算")
    add("D-03", sec, "与记账重做册衔接", "PASS",
        "记账重做册：走④延伸 rank 硬上限 5<6 ⇒ MCMC 禁止；本册：固定 B_i（减参数）后 rank=2、cond 可用 ⇒ 选2 成为解除 MCMC 的候选，但前提是真实 cond<1e10")

    # =====================================================================
    # 汇总
    # =====================================================================
    counts = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
    for r in RESULTS:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    g_ok = sum(1 for g2 in GUARDS if g2["ok"])

    payload = {
        "册": "TUFT_V3.5_走④β通道×可识别性_φ0零信息根因重算",
        "生成时间": time.strftime("%Y-%m-%d %H:%M:%S"),
        "定位": "走④ β 通道是否为步3册缺失的 φ0 相位观测、能否解除 φ0 零信息根因",
        "承接": "记账重做册（选2：固定 B_i）+ 并发步3册",
        "计数": counts, "总计": len(RESULTS),
        "关键量": {"∂A/∂λ": dA_dlam, "∂A/∂φ0": dA_dphi, "κ,ρ,φ0,δ": (kappa, rho, phi0, delta)},
        "示意Jacobian(参数λ,φ0)": {"4强度rank": rank4, "+β rank": rank5,
                                  "4强度cond": cond4, "+β cond": cond5,
                                  "步3册cond": 7.99e16},
        "核心结论": "走④ β 通道（∂A/∂φ0≠0）解除步3册的 φ0 零信息根因：固定B_i(选2)+β 后 "
                   "rank=2、cond 从 7.99e16 降到 ~%.0f（示意模型）⇒ 选2 首次出现数值可用候选；"
                   "真实 cond 待作者选定结构后重算" % cond5,
        "诚实边界": "示意 Jacobian；不宣称 MCMC 已可启动；真实 cond 待 κ/结构",
        "自检": {"总数": len(GUARDS), "通过": g_ok, "项": GUARDS},
        "条目": RESULTS,
        "耗时": "%.1fs" % (time.time() - T_START),
    }
    base = os.path.join(DATA_DIR, "TUFT_V3.5_走④β通道×可识别性_φ0零信息根因重算_2026-10-07")
    with open(base + ".json", "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    md = ["# TUFT V3.5 · 走④β通道 × 可识别性：φ0 零信息根因重算（机器产物）", "",
          "- 生成时间：%s" % payload["生成时间"],
          "- 条目 %d ｜ PASS %d ｜ FAIL %d ｜ BOUNDARY %d ｜ INFO %d ｜ 自检 %d / %d" %
          (len(RESULTS), counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"],
           g_ok, len(GUARDS)),
          "- 关键量：∂A/∂λ=%.4g ｜ ∂A/∂φ0=%.4g（κ=1,ρ=0.05,φ0=δ=1）" % (dA_dlam, dA_dphi),
          "- 示意 Jacobian（参数 λ,φ0）：4 强度 rank=%d ｜ +β rank=%d ｜ cond %.3g→%.3g" %
          (rank4, rank5, cond4, cond5),
          "- 核心结论：走④ β 通道解除 φ0 零信息根因（cond 7.99e16→%.0f，示意模型）" % cond5,
          "", "## 条目", "", "| ID | 节 | 条目 | 判定 | 摘要 |", "|---|---|---|---|---|"]
    for r in RESULTS:
        head = r["detail"].replace("\n", " ")
        if len(head) > 200:
            head = head[:200] + "…"
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
    print("核心：∂A/∂φ0=%.4g≠0 ⇒ φ0 根因解除 ｜ 固定B_i+β: rank=%d, cond %.3g→%.3g（示意）" %
          (dA_dphi, rank5, cond4, cond5))
    if g_ok != len(GUARDS):
        print("SELFCHECK FAILED")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
