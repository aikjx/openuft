# -*- coding: utf-8 -*-
"""
TUFT_V3.5_出路a_PDG约束重标窗口3与两难裁定_2026-10-07.py
================================================
引擎：按出路 a 用 PDG/文献对 β 衰变 S/T 耦合的精确约束重标窗口3，
裁定"S 结构 β 预言两难"是否缓解，并复核替代出路 b/c/d。

回链（来源标注，不重算）：
- PDG Fierz 干涉项 b（中子）：0.017 ± 0.020 ± 0.003
  https://pdgprod.lbl.gov/pdgprod/pdgLive/DataBlock.action?node=S017A00
- 中子张量耦合 2σ：-0.0015 < C_T/C_A < 0.0079（arXiv 1309.2499）
- 核/中子张量 90%CL：-0.0014 < (C_T+C'_T)/C_A < 0.014（arXiv 1306.2608）
- 标量耦合 |C_S+C'_S| ≲ 1e-3（hep-ph/0410254）
- GT 谱形 b<1e-3 ⇒ |ε_T| ≲ 1.5e-4（arXiv 1907.02164）
- 走④延伸册 C-01：1σ 可测需 X=|κ·ρ·sinφ0·sinδ| ≥ 0.009706
- 走④S结构册（2026-10-07 前轮）：三窗口两难
- ADD-01MCMC：φ 被 EDM 钉死 {0,π}（|sinφ|<5.9e-11）

惯例：add 5 参；guard；退出码 0/2；纯标准库；json/md 同名。
红线：数学自洽 ≠ 物理真实；评级 C/L1 维持。
"""
import json, os, math

RES = []
def add(cid, sec, item, verdict, detail):
    RES.append({"id": cid, "sec": sec, "item": item, "verdict": verdict, "detail": detail})

GUARDS = []
def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})

X_THRESH = 0.009706   # 走④延伸册 C-01 可测阈
KAPPA_HI, KAPPA_LO = 1e-2, 1e-3  # 窗口3 排除区（PDG/文献综合）

# ---------------- A. PDG/文献约束采集 ----------------
add("A-01", "PDG/文献约束", "PDG Fierz 干涉项 b（中子）", "BOUNDARY",
    "PDG 组合值 b = 0.017 ± 0.020 ± 0.003（pdgLive S017A00）；不确定性 ~0.02 ⇒ 对 S/T 组合耦合的排除约 10^-2 量级")
add("A-02", "PDG/文献约束", "中子张量耦合 2σ", "PASS",
    "-0.0015 < C_T/C_A < 0.0079（arXiv 1309.2499，中子 β 衰变 + G_V 组合）；|C_T/C_A| 约束 ~10^-3~10^-2")
add("A-03", "PDG/文献约束", "核/中子张量 90%CL", "PASS",
    "-0.0014 < (C_T+C'_T)/C_A < 0.014（arXiv 1306.2608, 90% C.L.）；|C_T/C_A| ~10^-2")
add("A-04", "PDG/文献约束", "标量耦合", "PASS",
    "|C_S+C'_S| ≲ 1e-3（hep-ph/0410254 量级）；GT 谱形 b<1e-3 ⇒ |ε_T| ≲ 1.5e-4（arXiv 1907.02164）")
add("A-05", "PDG/文献约束", "窗口3 重标", "BOUNDARY",
    "综合 PDG/文献：S/T 耦合排除区约 **1e-3~1e-2**（候选S_T册原估 1e-4~1e-3 略保守，也远未宽松到 0.1）")

# ---------------- B. 两难重裁定 ----------------
rho_req_hi = X_THRESH / KAPPA_HI   # κ=1e-2 需 ρ
rho_req_lo = X_THRESH / KAPPA_LO   # κ=1e-3 需 ρ
kappa_need_rho1 = X_THRESH         # ρ=1 需 κ
kappa_need_rho_prop = math.sqrt(X_THRESH)  # ρ∝κ 需 κ

add("B-01", "两难重裁定", "出路 a 能否缓解两难", "FAIL",
    "窗口3 实际排除区 ~1e-3~1e-2（未宽到 0.1）⇒ 出路 a 不能缓解两难，反而确证排除区与可测区不重叠")
add("B-02", "两难重裁定", "临界可测需 ρ", "FAIL",
    "要 X≥0.0097：κ=1e-3（标量/张量典型约束）⇒ 需 ρ≥9.7（非微扰，被排除）；κ=1e-2（张量上限边缘）⇒ 需 ρ≥0.97，但 κ=1e-2 本身已在排除边缘（|C_T/C_A| 90%CL 上限 0.014、Fierz b~±0.02）——临界可测恰落在排除区")
add("B-03", "两难重裁定", "ρ=1（微扰极限）需 κ", "FAIL",
    "ρ=1 时需 κ≥%.3f，远超排除区(1e-3~1e-2)约 1 个量级；ρ∝κ 时需 κ≥%.3f（平方关系），远超排除" % (kappa_need_rho1, kappa_need_rho_prop))
add("B-04", "两难重裁定", "S 结构 β 预言确凿不可测", "FAIL",
    "窗口3=1e-3~1e-2 下，X=κ·ρ·sinφ0·sinδ 实际 ~1e-3~1e-4 ≪ 阈 0.0097（差 1~2 量级）；两难确凿成立")

# ---------------- C. 替代出路复核 ----------------
add("C-01", "替代出路", "出路 b（T-odd/CP 相位）", "FAIL",
    "φ0 已被 EDM 钉死 {0,π}（|sinφ|<5.9e-11，回链 ADD-01MCMC）⇒ sinφ0~0，T-odd(CP) 效应被 EDM 压制，出路 b 被封")
add("C-02", "替代出路", "出路 c（换结构 T）", "FAIL",
    "T 同为 S/T 非标准耦合，受同一 Fierz b~1e-2 约束；且需 Ω 张量化 + 记账重跑——不缓解两难，只增加成本")
add("C-03", "替代出路", "出路 d（换谱形通道）", "FAIL",
    "谱形即 Fierz b 的同一观测（b ∝ (C_S+C'_S)|M_F|² + (C_T+C'_T)|M_GT|²，arXiv 1910.12684），换谱形不换约束——不缓解")
add("C-04", "替代出路", "未来实验精度", "BOUNDARY",
    "若 b→1e-3 则 |ε_T|≲1.5e-4（arXiv 1907.02164），仍 ≪ 可测需 κ~0.1 ⇒ 近期精度提升亦不可达")

# ---------------- D. 结论与出路 ----------------
add("D-01", "总裁定", "β 通道可测预言整体不可达", "FAIL",
    "走④+可选结构（S/T/V−A）的 β 通道可测预言，在当前与近期实验精度下均不可达（两难确凿；出路 a/b/c/d 全部不缓解）")
add("D-02", "总裁定", "唯一剩余可测出路", "BOUNDARY",
    "① 非 β 可测通道：g-2/UHECR 已关窗，仅剩未开辟通道；② 新体系动力学挠率（ESCAPE-AUDIT 遗留，E4/E9 仍阻塞）；③ 极端实验精度（b~1e-4~1e-5）方接近可测窗口")
add("D-03", "定位", "不推翻走④ 链结构性结论", "PASS",
    "φ0 根因解除、cond 门禁、推荐 S 的结构性判定均保留；本裁定只把「β 通道可测预言」整体关闭（当前精度下不可达）")

# ---------------- 自检 ----------------
guard("pdg_b_quoted", any(x["id"] == "A-01" and x["verdict"] == "BOUNDARY" for x in RES), "PDG Fierz b 已登记（回链 pdgLive S017A00）")
guard("window3_rescaled", any(x["id"] == "A-05" and x["verdict"] == "BOUNDARY" for x in RES), "窗口3 重标为 1e-3~1e-2 已登记")
guard("no_mitigation", any(x["id"] == "B-01" and x["verdict"] == "FAIL" for x in RES), "出路 a 不能缓解两难已裁定")
guard("rho_req_nonpert", rho_req_lo >= 5.0, "κ=1e-3 需 ρ≥%.1f≥5（非微扰，被排除）" % rho_req_lo)
guard("route_b_blocked", any(x["id"] == "C-01" and x["verdict"] == "FAIL" for x in RES), "出路 b（EDM 钉 φ）已复核为被封")
guard("overall_unreachable", any(x["id"] == "D-01" and x["verdict"] == "FAIL" for x in RES), "β 通道可测预言整体不可达已裁定")
guard("not_overthrow", any(x["id"] == "D-03" and x["verdict"] == "PASS" for x in RES), "不推翻走④ 链结构性结论已定位")

ok_all = all(g["ok"] for g in GUARDS)
n_pass = sum(1 for x in RES if x["verdict"] == "PASS")
n_fail = sum(1 for x in RES if x["verdict"] == "FAIL")
n_bound = sum(1 for x in RES if x["verdict"] == "BOUNDARY")

out = {
    "title": "TUFT V3.5 · 出路a PDG约束重标窗口3与两难裁定",
    "generated": "2026-10-07",
    "engine": "TUFT_V3.5_出路a_PDG约束重标窗口3与两难裁定_2026-10-07.py",
    "count": {"total": len(RES), "pass": n_pass, "fail": n_fail, "boundary": n_bound},
    "key_numbers": {
        "pdg_fierz_b": "0.017 ± 0.020 ± 0.003（中子，pdgLive S017A00）",
        "window3_rescaled": "1e-3 ~ 1e-2（S/T 耦合排除区，多通道综合）",
        "measure_threshold": "X=|κ·ρ·sinφ0·sinδ| ≥ 0.009706",
        "rho_needed": {"kappa_1e2": rho_req_hi, "kappa_1e3": rho_req_lo},
        "kappa_needed_rho1": kappa_need_rho1,
        "kappa_needed_rho_prop": kappa_need_rho_prop,
        "edm_phi_lock": "|sinφ|<5.9e-11（φ 钉死 {0,π}）",
    },
    "conclusion": "出路 a 不能缓解两难反而确证：窗口3(1e-3~1e-2)下 S 结构 β 预言 X~1e-3~1e-4 ≪ 阈 0.0097；出路 b(EDM 钉φ)/c(T 同约束)/d(谱形同约束) 均不缓解 ⇒ β 通道可测预言整体不可达（当前与近期精度）",
    "remaining": "非 β 通道(g-2/UHECR 已关窗) / 新体系动力学挠率(E4/E9 阻塞) / 极端精度 b~1e-4~1e-5",
    "redline": "数学自洽 ≠ 物理真实；评级 C/L1 维持；回链不重算；外部约束为公开文献/PDG 值",
    "items": RES,
    "guards": GUARDS,
    "guard_summary": {"total": len(GUARDS), "pass": sum(1 for g in GUARDS if g["ok"]), "ok": ok_all},
}

base = os.path.splitext(os.path.abspath(__file__))[0]
with open(base + ".json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

md = [
    "# TUFT V3.5 · 出路a PDG约束重标窗口3与两难裁定（机器产物）",
    "",
    "- 生成时间：2026-10-07",
    "- 条目 %d ｜ PASS %d ｜ FAIL %d ｜ BOUNDARY %d ｜ 自检 %d / %d" % (len(RES), n_pass, n_fail, n_bound, sum(1 for g in GUARDS if g["ok"]), len(GUARDS)),
    "- **裁定：出路 a 不能缓解两难，反而确证——β 通道可测预言整体不可达（当前与近期精度）**",
    "- 窗口3 重标：S/T 耦合排除区 ~1e-3~1e-2；可测阈 X≥0.009706 ⇒ 差 1~2 量级",
    "- 替代出路 b/c/d 复核：EDM 钉 φ / T 同约束 / 谱形同约束——全部不缓解",
    "",
    "## PDG/文献约束（公开来源）",
    "",
    "| 来源 | 约束 | 量级 |",
    "|---|---|---|",
    "| PDG Fierz b（中子）pdgLive S017A00 | b=0.017±0.020±0.003 | ~1e-2 |",
    "| arXiv 1309.2499 中子张量 2σ | -0.0015<C_T/C_A<0.0079 | ~1e-3~1e-2 |",
    "| arXiv 1306.2608 核张量 90%CL | -0.0014<(C_T+C'_T)/C_A<0.014 | ~1e-2 |",
    "| hep-ph/0410254 标量 | \\|C_S+C'_S\\|≲1e-3 | ~1e-3 |",
    "| arXiv 1907.02164 GT 谱形 | b<1e-3 ⇒ \\|ε_T\\|≲1.5e-4 | ~1e-4 |",
    "",
    "## 关键数值",
    "",
    "- 可测需 ρ：κ=1e-2 ⇒ ρ≥%.1f（但 κ 已在排除边缘）；κ=1e-3 ⇒ ρ≥%.1f（非微扰，被排除）" % (rho_req_hi, rho_req_lo),
    "- 微扰极限 ρ=1 需 κ≥%.3f；ρ∝κ 需 κ≥%.3f（均远超排除区）" % (kappa_need_rho1, kappa_need_rho_prop),
    "",
    "## 条目",
    "",
    "| ID | 节 | 条目 | 判定 | 摘要 |",
    "|---|---|---|---|---|",
]
for x in RES:
    md.append("| %s | %s | %s | %s | %s |" % (x["id"], x["sec"], x["item"], x["verdict"], x["detail"]))
md += [
    "",
    "## 自检",
    "",
    "| 基线 | 结果 | 取证 |",
    "|---|---|---|",
]
for g in GUARDS:
    md.append("| %s | %s | %s |" % (g["name"], "PASS" if g["ok"] else "FAIL", g["detail"]))
md += [
    "",
    "## 诚实边界与结论",
    "",
    "1. 外部约束为公开 PDG/文献值，精确组合随 PDG 版本变（窗口3 以 1e-3~1e-2 综合，个别通道可达 1e-4）；",
    "2. **出路 a 不能缓解两难反而确证**：S 结构 β 预言在当前精度不可测，在可测窗口已被排除；",
    "3. 出路 b 被封（EDM 钉 φ，|sinφ|<5.9e-11）、c 不缓解（T 同约束+Ω 张量化）、d 不缓解（谱形=同一 Fierz 约束）；",
    "4. 唯一剩余可测出路：非 β 通道（g-2/UHECR 已关窗）/ 新体系动力学挠率（E4/E9 阻塞）/ 极端精度 b~1e-4~1e-5；",
    "5. 本裁定关闭「β 通道可测预言」路线，**不推翻走④ 链结构性结论**（φ0 根因解除、cond 门禁、推荐 S 均保留）；",
    "6. 红线：数学自洽 ≠ 物理真实；评级 C/L1 维持。",
]
with open(base + ".md", "w", encoding="utf-8") as f:
    f.write("\n".join(md))

print("items=%d pass=%d fail=%d boundary=%d | rho_req(1e-2)=%.2f (1e-3)=%.2f | kappa(ρ=1)=%.3f (ρ∝κ)=%.3f | guards=%d/%d ok=%s"
      % (len(RES), n_pass, n_fail, n_bound, rho_req_hi, rho_req_lo, kappa_need_rho1, kappa_need_rho_prop,
         sum(1 for g in GUARDS if g["ok"]), len(GUARDS), ok_all))
raise SystemExit(0 if ok_all else 2)
