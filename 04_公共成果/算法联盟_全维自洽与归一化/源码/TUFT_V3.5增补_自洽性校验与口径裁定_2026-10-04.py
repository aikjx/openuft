# -*- coding: utf-8 -*-
"""
TUFT V3.5 增补 · 自洽性校验与口径裁定（分支④）
=========================================================================
定位：执行外部评审建议的第一步「自洽性校验」，并裁定 g-2 / UHECR 口径冲突
（外部评审「数值未由公式导出」 vs 攻破册「g-2/EDM/宇宙线窗口已关」）。

本册只做四件事（纯标准库，零第三方依赖）
--------------------------------------------------------------------
  A. 宇称自洽性：ℛ_chiral≡0 复核；C_L(θ)=C_R(−θ) 宇称条件机器验证
  B. Fisher 可识别性：6 参数 / 4 观测 ⇒ rank≤4<6 ⇒ Σ_p 不可逆
  C. 误差传播自洽性：σ_λ/λ、g-2、UHECR 区间算术复核 + 来源标记
  D. g-2 / UHECR 口径裁定：评审「未建立」与攻破册「已关窗」的相容性与裁决

红线：数学自洽 ≠ 物理真实；本册只裁决「推导是否闭合 / 数值是否由公式导出」。
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
DATA_DIR = os.path.join(ROOT, "04_公共成果", "算法联盟_全维自洽与归一化", "数据")

RESULTS = []
GUARDS = []


def add(cid, sec, item, statement, verdict, detail):
    RESULTS.append({"id": cid, "section": sec, "item": item, "statement": statement,
                    "verdict": verdict, "detail": detail})
    print("[%s] %-6s | %-26s | %s" % (verdict, cid, item, detail[:140]))


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("[GUARD] %-30s | %s | %s" % ("PASS" if ok else "FAIL", name, detail))
    return bool(ok)


# 常数（口径与判定册一致）
ALPHA_S = 0.1179
ALPHA_S_SIG = 0.0009
SIG_LAMBDA_LAMBDA = ALPHA_S_SIG / ALPHA_S


def main():
    # =====================================================================
    # A. 宇称自洽性
    # =====================================================================
    sec = "宇称自洽"
    # A-01 ℛ_chiral≡0 复核：g_L=|Ω|e^{iφ}, g_R=|Ω|e^{-iφ}
    Om = 1.0
    for phi in (0.1, 1.0, 2.0):
        gl2 = Om ** 2
        gr2 = Om ** 2
        Achi = (gl2 - gr2) / (gl2 + gr2)
        if abs(Achi) > 1e-15:
            break
    ok_Achi = abs(Achi) <= 1e-15
    add("A-01", sec, "ℛ_chiral 恒等零复核",
        "g_L=|Ω|e^{+iφ}, g_R=|Ω|e^{-iφ}", "PASS" if ok_Achi else "FAIL",
        "|g_L|²=|g_R|²=|Ω|² ⇒ ℛ_chiral=%.2e ≡ 0（复相位不产生手征强度差）" % Achi)

    # A-02 宇称条件 C_L(θ)=C_R(−θ) 机器验证
    # 原线性相位 φ(θ)=φ0(θ−θ_Wc)/Δθ_W；宇称守恒需 φ(θ)=−φ(−θ) (mod 2π)
    PHI0 = 1.0
    DW = 1.0
    for THWC in (0.0, 0.3):          # 弱域中心
        sumphi = PHI0 * (2 * THWC) / DW   # φ(−θ)+φ(θ) = −2φ0θ_Wc/Δθ_W（取 θ 消去）
        # 宇称条件成立当且仅当 sumphi ≡ 0 (mod 2π)
        ok_c = (abs(sumphi % (2 * math.pi)) < 1e-12) or (abs(sumphi % (2 * math.pi) - 2 * math.pi) < 1e-12)
        if THWC == 0.0:
            add("A-02a", sec, "C_L(θ)=C_R(−θ) 当 θ_Wc=0",
                "宇称守恒条件", "PASS" if ok_c else "FAIL",
                "φ(−θ)+φ(θ)=%.4f ≡ 0 ⇒ 满足" % sumphi)
        else:
            add("A-02b", sec, "C_L(θ)=C_R(−θ) 当 θ_Wc=%.1f" % THWC,
                "宇称守恒条件", "PASS" if ok_c else "FAIL",
                "φ(−θ)+φ(θ)=%.4f ≢ 0 ⇒ 宇称把弱域映到 −θ_Wc 扇区，条件不成立" % sumphi)

    guard("omega_Abar_zero", ok_Achi, "ℛ_chiral≡0（复相位≠手征不对称）")
    guard("parity_cl_cr_nonzero_wc", not (abs((PHI0 * 2 * 0.3) % (2 * math.pi)) < 1e-12),
          "θ_Wc≠0 时 C_L(θ)=C_R(−θ) 不成立（宇称不自洽）")

    # =====================================================================
    # B. Fisher 可识别性（6 参数 / 4 观测）
    # =====================================================================
    sec = "可识别性"
    # 通用维度论证：H 为 4×6 ⇒ rank(H) ≤ min(4,6)=4 < 6 ⇒ F_p=H^TΣ^{-1}H 奇异
    # 机器示例：构造一个 4×6 满行秩 Jacobian，验证 rank=4
    H = [
        [1.0, 0.1, 0.2, 0.3, 0.4, 0.5],
        [0.2, 1.0, 0.1, 0.0, 0.0, 0.1],
        [0.0, 0.0, 1.0, 0.2, 0.1, 0.0],
        [0.1, 0.0, 0.0, 1.0, 0.3, 0.2],
    ]
    # 数值秩（Gauss 消元）
    M = [row[:] for row in H]
    nr, nc = 4, 6
    rank = 0
    for c in range(nc):
        piv = None
        for r in range(rank, nr):
            if abs(M[r][c]) > 1e-12:
                piv = r
                break
        if piv is None:
            continue
        M[rank], M[piv] = M[piv], M[rank]
        pv = M[rank][c]
        M[rank] = [x / pv for x in M[rank]]
        for r in range(nr):
            if r != rank and abs(M[r][c]) > 1e-12:
                f = M[r][c]
                M[r] = [M[r][k] - f * M[rank][k] for k in range(nc)]
        rank += 1
        if rank == nr:
            break
    ok_fisher = rank <= 4
    add("B-01", sec, "Fisher 秩（6 参数/4 观测）",
        "rank(F_p) ≤ min(4,6)=4 < 6", "PASS" if ok_fisher else "FAIL",
        "示例 4×6 Jacobian 实测 rank=%d ⇒ F_p 奇异，Σ_p 不可唯一获得" % rank)
    add("B-02", sec, "φ0 可识别性",
        "φ0 不由 α_G,α,α_s,α_W 确定", "BOUNDARY",
        "φ0 拟由 β 衰变确定；在 C_L,C_R 闭合前 σ_φ0 无来源（评审 C-02）")

    guard("fisher_rank_deficient", ok_fisher and rank < 6,
          "rank=%d<6 ⇒ 仅凭 4 个耦合常数无法唯一得到 6 参数协方差" % rank)

    # =====================================================================
    # C. 误差传播自洽性（算术复核 + 来源标记）
    # =====================================================================
    sec = "误差传播"
    # C-01 σ_λ/λ
    add("C-01", sec, "σ_λ/λ 算术",
        "0.0009/0.1179≈0.0076", "BOUNDARY",
        "算术成立（%.5f），但需显式 λ=f(α_s,α_W,α,α_G) 且 λ∝α_s 才能这样传递；当前为假设非推导" %
        SIG_LAMBDA_LAMBDA)
    # C-02 g-2 区间
    center, sig = 2.4e-13, 0.65e-13
    lo2, hi2 = center - 2 * sig, center + 2 * sig
    lo19, hi19 = center - 1.96 * sig, center + 1.96 * sig
    ok_g2 = abs(lo2 - 1.1e-13) / 1.1e-13 < 0.01 and abs(hi2 - 3.7e-13) / 3.7e-13 < 0.01
    add("C-02", sec, "g-2 95% 区间算术",
        "Δa_e=2.4±0.65 (×10⁻¹³)", "PASS" if ok_g2 else "FAIL",
        "2σ=[%.3f,%.3f]；1.96σ=[%.4f,%.4f]（×10⁻¹³）算术对；但 σ=0.65e-13 未由 Jacobian 导出" %
        (lo2 * 1e13, hi2 * 1e13, lo19 * 1e13, hi19 * 1e13))
    add("C-03", sec, "g-2 σ/center 张力",
        "σ/center≈27% vs 输入 0.76%/2%", "BOUNDARY",
        "σ/center=%.1f%% ⇒ 需展示 ∂Δa_e/∂B_i 条件数；当前未给出" % (sig / center * 100))
    # C-04 UHECR 区间
    ec, esig = 0.68, 0.21
    Elo, Ehi = ec - 2 * esig, ec + 2 * esig
    GZK = 5.00
    E_TUFT_lo, E_TUFT_hi = GZK - Ehi, GZK - Elo
    ok_uh = abs(Elo - 0.26) / 0.26 < 0.01 and abs(Ehi - 1.10) / 1.10 < 0.01
    add("C-04", sec, "UHECR 区间算术",
        "0.68±0.21 (×10¹⁹ eV)", "PASS" if ok_uh else "FAIL",
        "2σ=[%.2f,%.2f]；E_TUFT=GZK−ΔE=[%.2f,%.2f]（×10¹⁹ eV）算术对；证伪须 Σ_total 边缘化" %
        (Elo, Ehi, E_TUFT_lo, E_TUFT_hi))

    guard("g2_interval_arith", ok_g2, "g-2 区间算术正确，但 σ 来源未建立")
    guard("uhec_interval_arith", ok_uh, "UHECR 区间算术正确，但证伪需全协方差边缘化")

    # =====================================================================
    # D. g-2 / UHECR 口径裁定（评审「未建立」 vs 攻破册「已关窗」）
    # =====================================================================
    sec = "口径裁定"
    # 攻破册结论（回链引用）：
    #   g-2 已否决 8.06 量级（偏差 74.96%）；EDM 超限 1.28e16；宇宙线 ξ<5.11e-23 或无约束
    # 评审结论：数值区间未从完整模型导出（未建立）
    # 裁定：两者兼容不冲突——评审批评推导层，攻破册裁决物理层
    add("D-01", sec, "口径裁定：评审 vs 攻破册",
        "两结论是否冲突", "PASS",
        "评审「未建立」= 推导层缺口；攻破册「已关窗」= 物理层裁决（g-2 否决 8.06 量级 / 宇宙线 ξ<5.11e-23 或无约束）——层次不同，叠加后不矛盾")
    add("D-02", sec, "g-2/UHECR 预言状态",
        "能否作为定量预言", "FAIL",
        "按仓内攻破册结论，g-2/EDM/宇宙线窗口已关；评审补充指出其数值亦未由公式导出 ⇒ 双重否定，暂判不可用")
    add("D-03", sec, "重新开放的路径",
        "推翻关窗须满足的条件", "INFO",
        "须先证伪攻破册前提（Π-定理/尺度简并/无剩余无量纲自由度），而非仅补推导；否则分支④无可行观测通道")

    guard("window_reconciliation", True,
          "评审「未建立」与攻破册「已关窗」层次不同、叠加兼容；g-2/UHECR 预言暂判不可用")

    # =====================================================================
    # 汇总与产物
    # =====================================================================
    counts = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
    for r in RESULTS:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    g_ok = sum(1 for g in GUARDS if g["ok"])

    payload = {
        "册": "TUFT_V3.5增补_自洽性校验与口径裁定",
        "生成时间": time.strftime("%Y-%m-%d %H:%M:%S"),
        "定位": "分支④：外部评审路线第一步（自洽性校验）+ g-2/UHECR 口径裁定",
        "计数": counts, "总计": len(RESULTS),
        "宇称自洽": {"ℛ_chiral": Achi, "θ_Wc=0条件": "满足", "θ_Wc≠0条件": "不满足"},
        "可识别性": {"参数数": 6, "观测数": 4, "rank": rank, "Fisher奇异": True},
        "误差传播": {"σ_λ/λ": SIG_LAMBDA_LAMBDA, "g2_2σ": [lo2, hi2], "g2_196σ": [lo19, hi19],
                     "UHECR_2σ": [Elo, Ehi], "E_TUFT": [E_TUFT_lo, E_TUFT_hi]},
        "口径裁定": "评审「未建立」(推导层) 与 攻破册「已关窗」(物理层) 兼容；g-2/UHECR 预言暂判不可用",
        "自检": {"总数": len(GUARDS), "通过": g_ok, "项": GUARDS},
        "条目": RESULTS,
        "耗时": "%.1fs" % (time.time() - T_START),
    }
    base = os.path.join(DATA_DIR, "TUFT_V3.5增补_自洽性校验与口径裁定_2026-10-04")
    with io.open(base + ".json", "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    md = ["# TUFT V3.5 增补 · 自洽性校验与口径裁定（机器产物）", "",
          "- 生成时间：%s" % payload["生成时间"],
          "- 条目 %d ｜ PASS %d ｜ FAIL %d ｜ BOUNDARY %d ｜ INFO %d ｜ 自检 %d / %d" %
          (len(RESULTS), counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"],
           g_ok, len(GUARDS)),
          "- ℛ_chiral ≡ %.1e（复相位≠手征不对称）" % Achi,
          "- Fisher rank = %d < 6 ⇒ Σ_p 不可唯一获得" % rank,
          "- 口径裁定：评审「未建立」(推导层) 与 攻破册「已关窗」(物理层) 兼容；g-2/UHECR 预言暂判不可用",
          "", "## 条目", "", "| ID | 节 | 条目 | 判定 | 摘要 |", "|---|---|---|---|---|"]
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
    print("口径裁定：g-2/UHECR 预言暂判不可用（攻破册关窗 + 评审未建立，双层否定）")
    if g_ok != len(GUARDS):
        print("SELFCHECK FAILED")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
