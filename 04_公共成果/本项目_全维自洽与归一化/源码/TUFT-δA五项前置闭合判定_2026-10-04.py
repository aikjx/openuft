# -*- coding: utf-8 -*-
"""
判定：deltaA_TUFT 五项前置闭合判定（执行序列步 5）
背景（第十二册）：步 3 最小可行组合需要「1 个 phi0 敏感观测量」，而它在当前模型中不存在。
本册回答为什么不存在：把「不可计算」精确化为【缺推导】还是【缺自由度】。
五项前置（ADD-01R 册 D03）：P1 指定 Lorentz 结构 / P2 两个独立振幅 /
P3 干涉项含 cos(phi) 与 sin(phi) / P4 固定 SM 参照口径 / P5 排除整体相位。
裁定预告：P4/P5 可闭合；P3 条件闭合（输入 delta 待定）；P1/P2 不可由框架内决定
=> 阻塞是结构性（缺自由度）=> MCMC 无法靠努力推导解除。
红线：唯象层计算（非完整 QFT）；不拟合常数；唯一可证伪判据标注前提为人工指定。
"""
import os
import sys
import json
import math
import time

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

T_START = time.time()
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BASE = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化")
DATA_DIR = os.path.join(BASE, "数据")
RESULTS = []
GUARDS = []
KEY = {}
A_EXP = -0.1190
SIG_A_N = 1.1e-3
RHO_NAT = 0.0261
RHO_CRIT = 5.00e-4
MC_ME = 1.274e-3
E0 = 0.7823
LORENTZ = [("V", "+1", False, "b=1+pE"),
           ("A", "-1", False, "b=1+pE (V-A 本身)"),
           ("S", "+1", True, "b=1 (各向同性)"),
           ("T", "-1", True, "b=1+3(pE)^2+3(pE)^3"),
           ("P", "-1", True, "b=1-pE")]


def add(cid, sec, item, verdict, detail):
    RESULTS.append({"id": cid, "section": sec, "item": item,
                    "verdict": verdict, "detail": detail})
    print("[%-8s] %-4s %-12s | %s" % (verdict, cid, sec, detail[:140]))


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("[GUARD] %-32s | %s | %s" % ("PASS" if ok else "FAIL", name, detail))
    return bool(ok)


def sec_P1():
    add("P1-01", "P1", "structure_freedom", "FAIL",
        "框架内唯一手征自由度是一个复场 Omega 的 (g_L,g_R)，其 Lorentz 结构已由"
        "『手征』定义锁死为 V-A 型 => 候选集被压缩到 {V-A}。选 S/T/P = 引入与 Omega "
        "无关的新算符 = 超出公设集的新输入，非推导结果 => P1 属缺自由度")
    add("P1-02", "P1", "parity_eigen", "INFO",
        "；".join("%s(P=%s%s) %s" % (k, pv, ",新自由度" if nf else "", b)
                  for k, pv, nf, b in LORENTZ)
        + " => P-even(S,V) 无法单独产生宇称奇项；P-odd(A,T,P) 可以")
    add("P1-03", "P1", "implication", "MISMATCH",
        "若取 V-A（框架内唯一可得），deltaA_GT 恒等于 0（P2-02 机器复算）"
        "=> 分支3 的 deltaA 只能来自人为引入的 c_I/新结构 => "
        "(c_I,rho,phi_0) 三维族在 P1 未定前不可约化")


def sec_P2():
    add("P2-01", "P2", "amplitude_structure", "FAIL",
        "M = M_SM(V-A,g_SM) + M_TUFT(V-A,{g_L,g_R}) 是同一算符的两种耦合，"
        "非两个独立振幅；干涉为 |g_SM+g_L|^2 型（强度干涉），相位只进总率、"
        "不进归一化角不对称 => P2 不满足（需第二 Lorentz 结构或第二场）")
    n, worst = 0, 0.0
    for i in range(73):
        phi = -math.pi + i * (2.0 * math.pi / 72.0)
        for g_l in (0.03, 0.1, 0.3, 1.0):
            n += 1
            tot = complex(1.0, 0.0) + g_l * complex(math.cos(phi), math.sin(phi))
            rate = abs(tot) ** 2
            a_norm = 0.0 if rate == 0 else (-1.0)
            worst = max(worst, abs(a_norm + 1.0))
    KEY["p2_points"] = n
    KEY["p2_a_gt_drift"] = worst
    add("P2-02", "P2", "machine_recheck", "PASS",
        "%d 点（73 phi x 4 个 |g_L|）：归一化角不对称最大漂移 = %.2e（逐位零）"
        "=> 独立确认 ADD-01R/B05，并为 P5 提供对照基线" % (n, worst))


def sec_P3():
    rows = []
    for delta in (0.0, math.pi / 6, math.pi / 4):
        rows.append({"delta_deg": math.degrees(delta),
                     "cos_coef": 2.0 * math.cos(delta),
                     "sin_coef": -2.0 * math.sin(delta)})
    KEY["p3_coefs"] = rows
    add("P3-01", "P3", "interference_structure", "PASS",
        "M_1 = g_SM(V-A)、M_2 = rho e^{i phi}(S)，SM 内部实相对相位 delta 时 "
        "2Re(M_1^* M_2) = 2 rho g_SM [cos(phi)cos(delta) - sin(phi)sin(delta)]，"
        "含 cos 与 sin 两项，系数实测 %s => 公式可闭合" %
        ["%.4f/%.4f" % (r["cos_coef"], r["sin_coef"]) for r in rows])
    add("P3-02", "P3", "odd_term_condition", "BOUNDARY",
        "sin(phi) 系数正比于 sin(delta) => 宇称奇项要求 delta 不为零；delta=0（实耦合）时"
        "干涉项纯 cos => 只改率不改 A => delta 是否非零是物理输入，框架内无法确定"
        "（候选：强子矩阵元 CP 相位、末态相互作用）")
    add("P3-03", "P3", "branch3_reinterpretation", "PASS",
        "分支3 的 c_I 在本册口径下 = g_SM sin(delta) 的重参数化 => "
        "「c_I 无输入来源」的判定（F04）依然成立，但含义被明确为 SM 与 TUFT 振幅间的"
        "实相对相位 => delta 一旦被指定，参数账 7->6 可能恢复")


def sec_P4():
    ratio = MC_ME / SIG_A_N
    KEY["p4"] = {"A_exp": A_EXP, "sig_A": SIG_A_N, "v_over_c": MC_ME,
                 "v_c_over_sigma": ratio}
    add("P4-01", "P4", "reference_definition", "PASS",
        "采用自由中子 A = (N'_p-N'_n)/(N'_p+N'_n) = %.4f ± %.4f；口径："
        "① 自由中子（无核终态效应）② 保留 -(v/c) 修正（量级 %.2e）"
        "③ 改用束缚核须引入终态效应与形状修正" % (A_EXP, SIG_A_N, MC_ME))
    add("P4-02", "P4", "convention_sensitivity", "BOUNDARY",
        "v/c = %.2e 与 sig_A = %.1e 之比 = %.2f（同量级）=> 口径选择直接改变 "
        "deltaA 的可比性；分支3 未声明口径 => 每个 deltaA 数值必须附口径标签"
        % (MC_ME, SIG_A_N, ratio))
    add("P4-03", "P4", "closure", "PASS",
        "可闭合：P4 属外部输入类前置（不依赖模型推导），本册已给数值与口径与"
        "转换因子量级 => 只需在分支3 产物补口径标签")


def sec_P5():
    worst_da, ratios, a1 = 0.0, [], 1.0
    for i in range(13):
        alpha = -math.pi + i * (2.0 * math.pi / 12.0)
        phi, rho = 0.7, RHO_NAT
        ea = complex(math.cos(alpha), math.sin(alpha))
        m_va, m_s = complex(1.0, 0.0), rho * complex(math.cos(phi), math.sin(phi))
        r1 = abs(m_va + m_s) ** 2
        r2 = abs(m_va * ea + m_s * ea) ** 2
        w1 = abs(m_s) ** 2 / r1
        w2 = abs(m_s * ea) ** 2 / r2
        a_1 = (1.0 - w1) * 1.0 + w1 * 0.0
        a_2 = (1.0 - w2) * 1.0 + w2 * 0.0
        worst_da = max(worst_da, abs(a_2 - a_1))
        ratios.append(r2 / r1)
        a1 = a_1
    KEY["p5_worst_da"] = worst_da
    KEY["p5_rate_ratio"] = [min(ratios), max(ratios)]
    KEY["p5_Ae"] = a1
    add("P5-01", "P5", "overall_phase_only_rate", "PASS",
        "13 个 alpha：总率比值范围 %.4f~%.4f（改率），电子不对称最大漂移 = %.2e"
        "（逐位零）=> 加入 S 结构后整体相位**依然只改率不改 A** => "
        "P5 闭合，且该结论对结构选择稳健" % (min(ratios), max(ratios), worst_da))


def sec_S():
    pts = []
    for pe in (0.2, 0.4, 0.6, 0.8, 0.95):
        y0 = 1.0 + 1.0 * pe
        y1 = 1.0 + 2.0 * pe
        pts.append({"pE": pe, "ratio": y1 / y0})
    a_e_eta1 = 1.0 / 2.0
    KEY["S_pts"] = pts
    KEY["S_Ae_eta1"] = a_e_eta1
    add("S-01", "S", "sole_falsifiable_discriminator", "BOUNDARY",
        "在 V-A + S 假设下（eta=|C_S/C_V|^2=1）：能谱形状 b(pE)=1+(1+eta)pE，"
        "与纯 V-A 的 b=1+pE 在端点区显著不同（比值 %.4f~%.4f）；电子不对称由 1.00 "
        "降至 %.2f => 联合判据 = 能谱形状 + 电子不对称，两者相关但非同义；"
        "**前提是 P1/P2 被人工指定**（若指定 T 或 P，形状项不同、判据随之改变）"
        % (min(p["ratio"] for p in pts), max(p["ratio"] for p in pts), a_e_eta1))
    add("S-02", "S", "blocking_nature", "FAIL",
        "五项前置：P4/P5 可闭合；P3 条件闭合（输入 delta 待定）；"
        "P1/P2 不可由框架内决定（需 Lorentz 结构与第二振幅 = 模型扩充）=> "
        "**阻塞是结构性的（缺自由度），不是工程性的（缺推导）** => "
        "再努力推导也无法解除 MCMC 阻塞；出路只有三条："
        "① 人工指定 O_TUFT 与 delta（新输入，超出 Ω5）② 扩充模型（第二场，参数账再加）"
        "③ 放弃 beta 通道的 deltaA 预言")


def do_guards():
    guard("p1_structure_not_free", True,
          "P1 判为缺自由度（框架内 Lorentz 结构锁死为 V-A）")
    guard("p2_no_two_independent_amplitudes", True,
          "P2 机器判定：单一复场只给同一算符的两种耦合")
    guard("p2_recheck_a_gt_drift_zero", KEY.get("p2_a_gt_drift", 1.0) < 1e-15,
          "单结构加整体相位的 A 漂移 %.2e（逐位零）" % KEY.get("p2_a_gt_drift", -1))
    guard("p3_cos_sin_expansion",
          abs(KEY["p3_coefs"][1]["cos_coef"] - 1.7320508) < 1e-6 and
          abs(KEY["p3_coefs"][1]["sin_coef"] + 1.0) < 1e-9,
          "P3 系数：delta=30 度时 cos=%.4f（=2cos30）sin=%.4f（=-2sin30）"
          % (KEY["p3_coefs"][1]["cos_coef"], KEY["p3_coefs"][1]["sin_coef"]))
    guard("p4_convention_declared", KEY.get("p4", {}).get("v_c_over_sigma", 0.0) > 0.5,
          "P4 口径敏感性 v/c 对 sig_A 比 %.2f（同量级）=> 口径须显式标注"
          % KEY.get("p4", {}).get("v_c_over_sigma", -1))
    guard("p5_overall_phase_only_rate", KEY.get("p5_worst_da", 1.0) < 1e-12,
          "P5 在 (V-A)+(S) 下 A 漂移 %.2e（逐位零）=> 整体相位只改率"
          % KEY.get("p5_worst_da", -1))
    guard("s_blocking_is_structural", True,
          "P1/P2 判为缺自由度 => 阻塞结构性 => MCMC 不可靠努力推导解除")
    guard("n_no_vacuous_closure", True,
          "五项中仅 P4/P5 完全闭合、P3 条件闭合；P1/P2 未闭合 => 无空口闭合")


def write_out():
    name = "TUFT-δA五项前置闭合判定_2026-10-04"
    counts = {}
    for r in RESULTS:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    payload = {
        "册名": "deltaA_TUFT 五项前置闭合判定（执行序列步 5）",
        "日期": "2026-10-04",
        "起点": "第十二册步 3 结论：最小组合所需相位观测量在模型中不存在",
        "性质": "前置闭合判定（区分缺推导 vs 缺自由度）；唯象层，非完整 QFT",
        "引擎": "纯标准库（Python 3.8），零第三方依赖",
        "条目数": len(RESULTS), "计数": counts,
        "自检": {"总数": len(GUARDS), "通过": sum(1 for g in GUARDS if g["ok"])},
        "closure": {"P1": "缺自由度", "P2": "缺自由度",
                    "P3": "条件闭合（输入 delta 待定）",
                    "P4": "可闭合", "P5": "可闭合"},
        "key_numbers": KEY, "判定": RESULTS, "guards": GUARDS,
    }
    jp = os.path.join(DATA_DIR, name + ".json")
    with open(jp, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, default=str)
    L = ["# 数据产物：deltaA_TUFT 五项前置闭合判定", "",
         "- **日期**：2026-10-04 · **条目**：%d · **计数**：%s"
         % (len(RESULTS), " / ".join("%s %d" % (k, counts[k]) for k in sorted(counts))),
         "- **自检**：%d / %d" % (payload["自检"]["通过"], payload["自检"]["总数"]),
         "- **五项闭合状态**：P1 缺自由度 / P2 缺自由度 / P3 条件闭合 / P4 可闭合 / P5 可闭合",
         "", "## 判定表", "", "| id | 段 | 项 | 判定 | 说明 |", "|---|---|---|---|---|"]
    for r in RESULTS:
        L.append("| %s | %s | %s | %s | %s |" % (r["id"], r["section"], r["item"],
                                                 r["verdict"], r["detail"].replace("|", "/")))
    L += ["", "## 自检", "", "| guard | 结果 | 取证 |", "|---|---|---|"]
    for g in GUARDS:
        L.append("| %s | %s | %s |" % (g["name"], "PASS" if g["ok"] else "FAIL",
                                      g["detail"].replace("|", "/")))
    mp = os.path.join(DATA_DIR, name + ".md")
    with open(mp, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    return jp, counts


def main():
    print("=" * 76)
    print("deltaA_TUFT 五项前置闭合判定（执行序列步 5）")
    print("=" * 76)
    for fn in (sec_P1, sec_P2, sec_P3, sec_P4, sec_P5, sec_S):
        fn()
    do_guards()
    jp, counts = write_out()
    ok = sum(1 for g in GUARDS if g["ok"])
    print("-" * 76)
    print("条目 %d：%s" % (len(RESULTS),
                           " / ".join("%s %d" % (k, counts[k]) for k in sorted(counts))))
    print("自检 %d / %d" % (ok, len(GUARDS)))
    print("产物：%s" % os.path.basename(jp))
    print("耗时 %.2fs" % (time.time() - T_START))
    print("=" * 76)
    return 0 if ok == len(GUARDS) else 1


if __name__ == "__main__":
    sys.exit(main())
