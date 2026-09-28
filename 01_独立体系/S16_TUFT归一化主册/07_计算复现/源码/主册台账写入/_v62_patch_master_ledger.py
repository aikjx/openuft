# -*- coding: utf-8 -*-
"""v62 参数撤退终检：主册 v7.3->v7.4、E511->E512；台账同步。append-only，勘误#42 held。"""
import io, json

# ---------------- 主册 ----------------
MP = r"D:\a10\aikjx\code\my_lib\openuft\01_独立体系\S16_TUFT归一化主册\13_论文与成果\主册\TUFT_归一化主册_v1.0.md"
t = io.open(MP, encoding="utf-8").read()
lines = t.split("\n")
assert "主册 v7.3" in lines[0], "title v7.3 not found"
lines[0] = lines[0].replace("主册 v7.3", "主册 v7.4", 1)
assert "E1–E511" in lines[0], "E1-E511 not in title"
lines[0] = lines[0].replace("E1–E511", "E1–E512", 1)

v74 = """
> **★★ v7.4（v62 参数撤退终检轮：放开 c_m 后数据到底偏好什么 δω——不预设 H0/H1 直接对合并残差最佳拟合，数据偏好 δω≈+2%（95%上限 +6.77%），而 EHT 锚强制 δω≥+8.82%（c_m=−0.218 端），两带不重叠；阻尼 δτ 经 v41 \\|Im\\| 推导与频率在带内反相关、无单一 c_m 同时兼容两通道；参数撤退救不了，2026-09-26，append-only；独立脚本不 import v58/v59，数字照抄 _out.txt，勘误 #42 held，禁伪闭合）**：先 Read 磁盘 SSOT（v7.3/E1–E511/勘误#42）及 v58/v59 似然脚本与原始输出、v41(E490) 五点灵敏度带表。磁盘起点 **v7.3/E1–E511/勘误#42**，本轮升 **v7.4/E1–E512/勘误#42 held（本轮无新勘误）**；物理四态 **35/61/18/27 冻结**。
>
> **① 方法（独立脚本 `_audit_v62_parameter_retreat.py`，不 import v58/v59，纯标准库 math；复用其数据；数字照抄 `_out.txt`）**：不预设 H0/H1，直接对合并残差做 flat-prior 最佳拟合（加权均值 d_hat=Σδ_i/σ_i²÷Σ1/σ_i²、σ=1/√Σ1/σ_i²）；95% 上限=点估计+1.96σ。c_m→δω 映射用 v41(E490) 五点表（d=−0.05），三点验线性度+五点最小二乘。
>
> **② 数据最佳拟合（复核 v58/v59 逐位一致）**：频率边际化六事件联合 **δω_best=+2.00%±2.43%，95%上限+6.77%**（距 GR +0.82σ）；朴素5事件 −4.29±2.01（95%上限−0.35%）。阻尼边际化联合 **δτ_best=+10.00%±8.51%，95%上限+26.68%**（距 GR +1.17σ）；朴素5 +10.43±8.45。两通道都落 GR 1.2σ 内——数据最偏好 δ≈0。
>
> **③ c_m→δω 映射（v41 E490 五点，照抄）**：c_m=−0.369→+21.17%、−0.331→+19.18%、−0.290→+16.26%、−0.249→+12.42%、−0.218→+8.82%。三点弦斜率 −81.79%/unit，标称中点残差 +1.55pp（占峰谷12.6%，凹向上、线性为近似）；五点最小二乘 **δω(%)=−8.20−81.58·c_m（R²=0.980）**，反演 c_m=(δω+8.20)/(−81.58)。
>
> **④ 反演判定**：数据最佳拟合 δω=+2.00%→c_m=**−0.125**；95%上限 δω=+6.77%→c_m=**−0.184**；GR 极限 δω=0→c_m=**−0.101**——**全部落在 EHT 锚区间[−0.369,−0.218]之外**。EHT 内最靠近 GR 一端 c_m=−0.218 已对应 δω=+8.82%，仍比数据最佳拟合高 **2.80σ**；数据 95% 上限带[≤+6.77%]与 EHT 带[≥+8.82%]差 2.05pp、**不重叠**。
>
> **⑤ 阻尼通道映射（v41 未显式 tabulate δτ(c_m)，但 tabulate \\|Im(c_m)\\|；按 v59 同构 τ比=\\|Im_GR\\|/\\|Im_TUFT\\|=0.0889623/\\|Im_TUFT\\| 推导）**：c_m=−0.369→δτ=+3.8%、−0.331→+24.0%、−0.290→+57.6%、−0.249→+114.2%、−0.218→+186.3%。**频率与阻尼随 c_m 反相关**：频率要小δω→c_m≈−0.218（δτ飙+186%、距数据+20.7σ）；阻尼要小δτ→c_m≈−0.369（δω=+21.17%、距数据+7.9σ）。EHT 带内五点逐点检验**无单一 c_m 同时让两通道落在数据95%内**。
>
> **⑥ E512（参数撤退终检：放开 c_m 后数据仍偏好 δω≈0，EHT 锚强制 δω≥+8.82%，两带不重叠；阻尼与频率在带内反相关、无单一 c_m 同时兼容；参数撤退救不了）**：观测似然/参数约束通道，**不闭合新物理 E 数进四态**；勘误 #42 **held**；四态 **35/61/18/27 冻结**；联盟层 2/6；UFT-3 未解锁。这是参数约束分析不是新预言；为挽救理论把 c_m 调到 ≈−0.1 或正而放弃 EHT 锚=违规调参、不允许。与 v58/v59/v7.3 一致并加强：v58/v59 排除标称点 c_m=−0.29，本轮证明即便 c_m 在整个 EHT 锚区间自由撤退也救不回——参数撤退空间已被数据封死。保留：仅 n0 单模；联合 σ 或被残余 M–χ 简并低估（×1.5 后 95%上限升至+9.9% 恰触 +8.82%，为已承担保守上限不再放大）；带外 c_m>−0.218 为线性外推，但带内端点 δω=+8.82% 是 v41 直接数值非外推。本轮交付：《TUFT_参数撤退终检报告.md》、脚本 `_audit_v62_parameter_retreat.py`/`_out.txt`；openuft 第66章 append §66.25。
"""

new = "\n".join(lines[:2]) + v74 + "\n".join(lines[2:])
io.open(MP, "w", encoding="utf-8").write(new)
chk = io.open(MP, encoding="utf-8").read()
print("master title v7.4:", "主册 v7.4" in chk, "| E1–E512:", "E1–E512" in chk)
print("v7.4 block present:", "v7.4（v62 参数撤退终检轮" in chk)
print("v7.3 block retained:", "v7.3（最终封存轮" in chk)
print("E512 count:", chk.count("E512"), "| master len():", len(chk))

# ---------------- 台账 ----------------
LP = r"D:\a10\aikjx\code\my_lib\openuft\01_独立体系\S16_TUFT归一化主册\13_论文与成果\台账\TUFT_归一化台账_v1.0.json"
d = json.load(io.open(LP, encoding="utf-8"))
d["version"] = "v7.4"
d["date"] = "2026-09-26"
d["last_updated"] = "2026-09-26"
d["latest_round"] = "v7.4_v62_parameter_retreat"
d["equation_range"] = "E1-E512"
d["latest_erratum"] = 42
d["erratum"] = 42
d["v62_parameter_retreat_key_results"] = {
    "round": "v7.4/v62 (parameter-retreat final check: release c_m, what does data prefer?)",
    "source_output": "_audit_v62_parameter_retreat_out.txt",
    "audit_script": "_audit_v62_parameter_retreat.py",
    "method": "pure stdlib math, NOT importing v58/v59; reuses their data; flat-prior best-fit (weighted mean) WITHOUT preset H0/H1; 95% UL=best+1.96sigma",
    "best_fit": {
        "freq_marg_joint_domega_pct": 2.00, "freq_marg_joint_sigma_pct": 2.43, "freq_marg_joint_95UL_pct": 6.77,
        "freq_naive5_domega_pct": -4.29, "freq_naive5_sigma_pct": 2.01,
        "damp_marg_joint_dtau_pct": 10.00, "damp_marg_joint_sigma_pct": 8.51, "damp_marg_joint_95UL_pct": 26.68,
        "damp_naive5_dtau_pct": 10.43, "damp_naive5_sigma_pct": 8.45
    },
    "cm_to_domega_map_v41_E490": {
        "points_pct": {"-0.369": 21.17, "-0.331": 19.18, "-0.290": 16.26, "-0.249": 12.42, "-0.218": 8.82},
        "three_point_chord_slope": -81.79, "mid_residual_pp": 1.55,
        "lsq_fit": "domega_pct = -8.20 - 81.58*c_m", "R2": 0.980,
        "inversion": {"domega_+2.00": -0.125, "domega_+6.77_95UL": -0.184, "domega_0": -0.101},
        "eht_band_min_domega_pct": 8.82, "eht_band_min_at_cm": -0.218
    },
    "cm_to_dtau_derived_from_v41_Im": {
        "note": "v41 did NOT explicitly tabulate dtau(cm); derived via tau_ratio=|Im_GR|/|Im_TUFT|=0.0889623/|Im_TUFT|",
        "points_pct": {"-0.369": 3.8, "-0.331": 24.0, "-0.290": 57.6, "-0.249": 114.2, "-0.218": 186.3}
    },
    "anti_correlation": "freq wants cm~-0.218 (dtau=+186%, +20.7sigma from data); damping wants cm~-0.369 (domega=+21.17%, +7.9sigma); no single cm in band fits both",
    "verdict": "Even releasing c_m, fitting the data requires leaving the EHT anchor; the two observational constraints contradict; parameter retreat cannot save TUFT",
    "E512": "parameter-retreat final check: data prefer domega~0 (95% UL +6.77%); EHT anchor forces domega>=+8.82%; bands do not overlap; anti-correlated with damping channel; no surviving window. Observational/parameter-constraint channel; NOT in four-state.",
    "erratum": "#42 held (no new erratum)",
    "four_state": "35/61/18/27 frozen"
}
d["open_backlog"].append(
    "v7.4/v62 parameter-retreat final check (E512; independent script NOT importing v58/v59; flat-prior best-fit without preset H0/H1). "
    "Data best-fit: freq marginalized joint domega=+2.00%+/-2.43% (95% UL +6.77%); damping marginalized joint dtau=+10.0%+/-8.51% (95% UL +26.68%); both within 1.2sigma of GR. "
    "v41(E490) cm->domega five-point: cm=-0.369->+21.17%, -0.331->+19.18%, -0.290->+16.26%, -0.249->+12.42%, -0.218->+8.82%; LSQ domega=-8.20-81.58*cm (R2=0.980). "
    "Inversion: data domega=+2.00% -> cm=-0.125; 95%UL +6.77% -> cm=-0.184; GR -> cm=-0.101; ALL outside EHT band [-0.369,-0.218]. "
    "EHT-band minimum domega=+8.82% at cm=-0.218 is still 2.80sigma above data best-fit; 95% UL band [<=+6.77%] does not overlap EHT band [>=+8.82%] (gap 2.05pp). "
    "Damping channel: v41 did not tabulate dtau(cm) explicitly; derived from |Im(cm)| via tau ratio=|Im_GR|/|Im_TUFT|: cm=-0.369->dtau=+3.8%, ... -0.218->+186.3%. "
    "FREQUENCY AND DAMPING ANTI-CORRELATE in cm: no single cm in the EHT band fits both channels at 95%. "
    "VERDICT: even releasing c_m, fitting the data requires abandoning the EHT anchor; two observational constraints contradict; parameter retreat cannot save TUFT. "
    "This is parameter-constraint analysis not a new prediction; tuning c_m to ~-0.1 or positive to dodge the EHT anchor is forbidden. "
    "Caveats: n0 single-mode only; joint sigma may be underestimated by residual M-chi degeneracy (x1.5 raises 95%UL to +9.9%, touching +8.82% - already-borne conservative ceiling, not inflated further); out-of-band extrapolation linear, but in-band edge +8.82% is direct v41 numerics. "
    "erratum #42 held; four-state 35/61/18/27 frozen. Deliverables: TUFT_参数撤退终检报告.md + _audit_v62_parameter_retreat.py/_out.txt."
)
io.open(LP, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1))
d2 = json.load(io.open(LP, encoding="utf-8"))
print("ledger version:", d2["version"], "| range:", d2["equation_range"], "| erratum:", d2["latest_erratum"])
print("new key present:", "v62_parameter_retreat_key_results" in d2)
print("open_backlog len:", len(d2["open_backlog"]))
