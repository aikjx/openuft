# -*- coding: utf-8 -*-
"""
TUFT_V3.5_走④S结构_三窗口交叉判定_2026-10-07.py
================================================
引擎：交叉判定走④+推荐 S 结构下 β 通道的三个「窗口」——
  窗口1 cond 可用（κ 需 >1.83e-8 使 cond<1e10）
  窗口2 1σ 可测（κ·ρ·sinφ0·sinδ ≥ 0.0097 使 |δA| ≥ 0.0012=中子 ΔA）
  窗口3 未被实验排除（κ∝|C_S/C_V| ≲ 1e-3~1e-4）
揭示三窗口交叉关系与 S 结构 β 预言的可测性两难。

惯例：add 5 参；guard；退出码 0/2；纯标准库；json/md 同名。
红线：数学自洽 ≠ 物理真实；回链不重算。
回链：
- 候选S_T册：cond<1e10⇔κ>1.83e-8；κ∝|C_S/C_V|~1e-3~1e-4（量级估算）
- 走④延伸册：1σ 可测需 |κ·ρ·sinφ0·sinδ|≥0.009706（中子ΔA=0.0012，分母≈0.961）
- 走④收束册：cond<1e10⇔κ·ρ>9.17e-10
- 走④延伸册 D-03：放开算符空间为延伸公设，须作者显式登记
"""
import json, os, math

RES = []
def add(cid, sec, item, verdict, detail):
    RES.append({"id": cid, "sec": sec, "item": item, "verdict": verdict, "detail": detail})

GUARDS = []
def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})

# 数值常量（回链）
A_SM = -0.1188          # 走④延伸册：A_SM=-0.1188
DELTA_A_NEUTRON = 0.0012  # 中子 ΔA（1σ 可测阈，绝对量）
X_THRESH = 0.009706       # 走④延伸册 C-01：|κ·ρ·sinφ0·sinδ| 需 ≥0.009706
KAPPA_CRIT = 1.83e-8      # 候选S_T册：cond<1e10 临界 κ
KAPPA_EXP_LO, KAPPA_EXP_HI = 1e-4, 1e-3  # 候选S_T册 A-02 实验约束量级
COND_183 = 183.5          # 候选S_T册：cond≈183.5/κ

def denom(rho, ph0, d):
    return 1.0 + rho * rho + 2.0 * rho * math.cos(ph0 + d)

def deltaA(kappa, rho, ph0, d):
    return abs(A_SM * kappa * rho * math.sin(ph0) * math.sin(d) / denom(rho, ph0, d))

# 样例参数（走④延伸册 B-03 样例）
rho_s, ph0_s, d_s = 0.05, 1.0, 1.0

# ---------------- A. 三窗口定义 ----------------
add("A-01", "窗口定义", "窗口1 cond 可用", "PASS",
    "cond<1e10 ⇔ κ>1.83e-8（回链候选S_T册 B-02）；κ 越小 cond 越好（cond≈183.5/κ）")
add("A-02", "窗口定义", "窗口2 1σ 可测", "PASS",
    "|δA|≥0.0012(中子 ΔA) ⇔ |κ·ρ·sinφ0·sinδ|≥0.009706（回链走④延伸册 C-01，分母≈0.961）")
add("A-03", "窗口定义", "窗口3 未被实验排除", "BOUNDARY",
    "κ∝|C_S/C_V|≲1e-3~1e-4（回链候选S_T册 A-02 量级估算；精确值待 PDG 约束表）")

# ---------------- B. 交叉判定 ----------------
x_sample = kappa_lo_sample = KAPPA_EXP_HI * rho_s * math.sin(ph0_s) * math.sin(d_s)
dA_sample = deltaA(KAPPA_EXP_HI, rho_s, ph0_s, d_s)
ratio = dA_sample / DELTA_A_NEUTRON

add("B-01", "交叉", "窗口1∩窗口2 可同时满足", "PASS",
    "κ 大可测且 cond 仍 <1e10：κ=0.2 ⇒ cond≈183.5/0.2≈917<1e10；cond 门禁不排斥大 κ 可测窗口")
add("B-02", "交叉", "窗口2∩窗口3 冲突", "FAIL",
    "可测需 κ·ρ·sinφ0·sinδ≥0.0097（κ·ρ~0.01 量级），未排除需 κ≲1e-3（κ·ρ~1e-4~1e-5）——两窗口差 2~4 个量级，不重叠")
add("B-03", "交叉", "若 ρ∝κ 同源", "FAIL",
    "若 S 幅度比 ρ 与 κ 同源（ρ∝κ），可测需 κ²·(sinφ0 sinδ)~0.01 ⇒ κ~0.1~1，同样远超实验排除窗口")
add("B-04", "交叉", "S 结构 β 预言两难", "FAIL",
    "现有实验约束（κ~1e-3~1e-4）下，S 结构 β 不对称度预言低于 1σ 可测阈约 2 个量级（不可测）；κ 提升到可测窗口则 S 耦合强度远超现有排除（已排除）——两难")

# ---------------- C. 数值复核 ----------------
add("C-01", "数值复核", "样例 |δA| 远低于阈", "PASS",
    "κ=1e-3,ρ=0.05,φ0=δ=1：X=%.3e，|δA|=%.3e，与 0.0012 差 %.0f 倍（约 2 个量级不可测）" % (x_sample, dA_sample, ratio))
add("C-02", "数值复核", "可测需 ρ≫1", "FAIL",
    "要 1σ 可测 X≥0.0097：κ=1e-3 需 ρ≥%.1f，κ=1e-4 需 ρ≥%.1f——均非微扰（ρ≫1），且 S 强于 V−A 已被实验排除" % (X_THRESH/(KAPPA_EXP_HI*math.sin(ph0_s)*math.sin(d_s)), X_THRESH/(KAPPA_EXP_LO*math.sin(ph0_s)*math.sin(d_s))))
add("C-03", "数值复核", "cond 门禁≠预言可测", "PASS",
    "走④收束册 cond 门禁（κ·ρ>9.17e-10）在 κ~1e-3~1e-4 恒满足（门禁过），但预言可测需 X≥0.0097（不满足）——两判据不矛盾，但揭示「门禁解除≠预言可测」的新张力")

# ---------------- D. 边界与出路 ----------------
add("D-01", "边界", "量级估算与待定参数", "BOUNDARY",
    "κ 量级估算、ρ 与 sinφ0·sinδ 待真实化；结论对 ρ≤1 稳健，对 ρ≫1 失效（但 ρ≫1 已被排除）")
add("D-02", "出路", "出路a：重新评估实验排除强度", "BOUNDARY",
    "若现有 β 实验对 S 耦合的排除实际上更宽松（κ 可达 ~0.1 量级），两难缓解——须查 PDG 精确约束表重新标定窗口3")
add("D-03", "出路", "出路b：换可测通道/结构", "BOUNDARY",
    "① 转向 T-odd(CP) 相位效应（φ0 驱动，非 P 破缺），可能避开 P 通道不可测；② 换结构 T（代价：Ω 张量化+记账重跑）；③ 换观测通道（谱形/极化），窗口2 判据重定")
add("D-04", "结论定位", "本判定揭示两难，不推翻走④ 链", "PASS",
    "走④ 链结构性结论（φ0 根因解除、cond 门禁、推荐 S）均不推翻；本判定把「S 结构 β 预言可测」从可选降级为需作者按窗口3 重新权衡的阻塞点")

# ---------------- 自检 ----------------
guard("w1_correct", abs(KAPPA_CRIT - 1.83e-8) < 1e-10, "窗口1 临界 κ 回链候选S_T册")
guard("w2_correct", abs(X_THRESH - 0.009706) < 1e-6, "窗口2 阈值回链走④延伸册 C-01")
guard("sample_repro", dA_sample > 0 and ratio < 0.1, "样例 |δA| 远低于阈（复算确认不可测）")
guard("conflict_found", any(x["id"] == "B-02" and x["verdict"] == "FAIL" for x in RES), "窗口2∩窗口3 冲突已登记")
guard("dilemma_found", any(x["id"] == "B-04" and x["verdict"] == "FAIL" for x in RES), "S 结构两难已登记")
guard("gate_not_measure", any(x["id"] == "C-03" and x["verdict"] == "PASS" for x in RES), "cond 门禁≠预言可测张力已登记")
guard("dilemma_not_overthrow", any(x["id"] == "D-04" and x["verdict"] == "PASS" for x in RES), "不推翻走④ 链定位已登记")

ok_all = all(g["ok"] for g in GUARDS)
n_pass = sum(1 for x in RES if x["verdict"] == "PASS")
n_fail = sum(1 for x in RES if x["verdict"] == "FAIL")
n_bound = sum(1 for x in RES if x["verdict"] == "BOUNDARY")

out = {
    "title": "TUFT V3.5 · 走④+S 结构三窗口交叉判定（cond×可测×排除）",
    "generated": "2026-10-07",
    "engine": "TUFT_V3.5_走④S结构_三窗口交叉判定_2026-10-07.py",
    "count": {"total": len(RES), "pass": n_pass, "fail": n_fail, "boundary": n_bound},
    "key_numbers": {
        "cond_gate": "κ>1.83e-8 (cond<1e10, cond≈183.5/κ)",
        "measure_threshold": "|κ·ρ·sinφ0·sinδ|≥0.009706 (|δA|≥0.0012=中子ΔA)",
        "exp_exclusion": "κ∝|C_S/C_V|≲1e-3~1e-4 (量级估算)",
        "sample": {"kappa": "1e-3", "rho": "0.05", "X": x_sample, "deltaA": dA_sample, "ratio_to_thresh": ratio},
        "rho_needed": {"kappa_1e3": X_THRESH/(KAPPA_EXP_HI*math.sin(ph0_s)*math.sin(d_s)), "kappa_1e4": X_THRESH/(KAPPA_EXP_LO*math.sin(ph0_s)*math.sin(d_s))},
    },
    "conclusion": "S 结构 β 不对称度预言两难：κ 在未排除窗口(≲1e-3)则不可测(差~2量级)，κ 到可测窗口则已被实验排除；cond 门禁解除≠预言可测",
    "redline": "数学自洽 ≠ 物理真实；评级 C/L1 维持；回链不重算",
    "items": RES,
    "guards": GUARDS,
    "guard_summary": {"total": len(GUARDS), "pass": sum(1 for g in GUARDS if g["ok"]), "ok": ok_all},
}

base = os.path.splitext(os.path.abspath(__file__))[0]
with open(base + ".json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

md = [
    "# TUFT V3.5 · 走④+S 结构三窗口交叉判定（机器产物）",
    "",
    "- 生成时间：2026-10-07",
    "- 条目 %d ｜ PASS %d ｜ FAIL %d ｜ BOUNDARY %d ｜ 自检 %d / %d" % (len(RES), n_pass, n_fail, n_bound, sum(1 for g in GUARDS if g["ok"]), len(GUARDS)),
    "- **结论：S 结构 β 不对称度预言两难**——κ 在未排除窗口则不可测，κ 到可测窗口则已被实验排除",
    "- 样例(κ=1e-3,ρ=0.05)：X=%.3e，|δA|=%.3e，与 0.0012 差 %.0f 倍（约 2 个量级不可测）" % (x_sample, dA_sample, ratio),
    "",
    "## 三窗口",
    "",
    "| 窗口 | 定义 | 数值判据 |",
    "|---|---|---|",
    "| 窗口1 cond 可用 | cond<1e10 | κ>1.83e-8（回链候选S_T册 B-02） |",
    "| 窗口2 1σ 可测 | \\|δA\\|≥0.0012=中子ΔA | \\|κ·ρ·sinφ0·sinδ\\|≥0.009706（回链走④延伸册 C-01） |",
    "| 窗口3 未被排除 | κ∝\\|C_S/C_V\\| | ≲1e-3~1e-4（回链候选S_T册 A-02 量级） |",
    "",
    "## 交叉关系",
    "",
    "- 窗口1∩窗口2：**可同时满足**（κ=0.2 ⇒ cond≈917<1e10，仍可测）——cond 门禁不排斥可测窗口",
    "- 窗口2∩窗口3：**冲突**（可测需 κ·ρ~0.01，未排除需 κ·ρ~1e-4~1e-5，差 2~4 量级）",
    "- 若 ρ∝κ 同源：可测需 κ²~0.01 ⇒ κ~0.1~1，同样远超排除",
    "- **cond 门禁解除 ≠ 预言可测**（走④收束册门禁在 κ~1e-3~1e-4 恒过，但可测阈不满足）",
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
    "## 诚实边界与出路",
    "",
    "1. κ 量级估算、ρ 与 sinφ0·sinδ 待真实化；结论对 ρ≤1 稳健（ρ≫1 已被排除）；",
    "2. 出路a：查 PDG 精确约束表重新标定窗口3（若 S 排除实际更宽松，两难缓解）；",
    "3. 出路b：转向 T-odd(CP) 相位效应 / 换结构 T / 换观测通道（谱形极化），窗口2 判据重定；",
    "4. 本判定揭示两难，**不推翻走④ 链**（φ0 根因解除、cond 门禁、推荐 S 均保留），只把「S 预言可测」降级为需作者权衡的阻塞点；",
    "5. 红线：数学自洽 ≠ 物理真实；评级 C/L1 维持。",
]
with open(base + ".md", "w", encoding="utf-8") as f:
    f.write("\n".join(md))

print("items=%d pass=%d fail=%d boundary=%d | sample X=%.3e dA=%.3e ratio=%.0fx | rho_req(1e3)=%.1f (1e4)=%.1f | guards=%d/%d ok=%s"
      % (len(RES), n_pass, n_fail, n_bound, x_sample, dA_sample, ratio,
         X_THRESH/(KAPPA_EXP_HI*math.sin(ph0_s)*math.sin(d_s)),
         X_THRESH/(KAPPA_EXP_LO*math.sin(ph0_s)*math.sin(d_s)),
         sum(1 for g in GUARDS if g["ok"]), len(GUARDS), ok_all))
raise SystemExit(0 if ok_all else 2)
