# -*- coding: utf-8 -*-
"""
空间螺旋几何化统一场论 · 开放项精算验证·四期（2026-09-27）
================================================================
覆盖与交叉验证：
  C05   核心：α=sin(1/(137+Δ_top)) 理论 Δ_top=(1/4π²)(χ/(2−2g)) 的数值命中检验
        闭合曲面 χ=2−2g ⇒ Δ_top=1/(4π²)=0.02533029591…
        对照：01A 附录反解值 Δ_top=1/asin(α)−137=0.03599908…
  C16   附带：αⁿ/N 序列 vs 暗能量/暗物质宇宙学占比的量级对应
  C13   附带：G=c³/[ℏ(κ_G²+τ_G²)] 若 κ_G、τ_G 即 C02 曲率挠率 ⇒ 条件式数值
  C40   附带：四组参数 |R'|=c 且 b/A=1/0.5/0.0073/2 复算确认
方法：解析 + mpmath 250 位数值交叉验证
幂等覆盖输出：数据/空间螺旋开放项_精算验证4.json / .md
"""
import mpmath as mp
import json, io, os

mp.mp.dps = 250
pi = mp.pi

alpha_obs = mp.mpf("0.0072973525693")   # CODATA 2018 观测锚
c = mp.mpf("299792458")

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "数据")
OUT_DIR = os.path.abspath(OUT_DIR)

res = {
    "title": "空间螺旋几何化统一场论 · 开放项精算验证·四期",
    "date": "2026-09-27",
    "dps": 250,
    "method": "解析 + mpmath 250 位数值交叉验证",
    "checks": [],
}

def fmt(x, n=16):
    return mp.nstr(x, n)

def rel_err(a, e):
    return abs(a - e) / abs(e) if e != 0 else abs(a)

# =================================================================
# 1. C05 核心：α 拓扑公式数值命中检验
# =================================================================
# Δ_top = (1/4π²)·(χ/(2−2g))；闭合曲面 χ=2−2g（欧拉恒等）⇒ 因子=1
d_top_theory = 1 / (4 * pi**2)            # 0.025330295910584…
alpha_pred = mp.sin(1 / (137 + d_top_theory))
rel_c05 = rel_err(alpha_pred, alpha_obs)
# 反解：命中 α_obs 所需 Δ_top
d_top_fit = 1 / mp.asin(alpha_obs) - 137  # 0.03599908…
# 反解检验（01A 附录 §3.2 交叉）
N_plus_d_fit = 1 / mp.asin(alpha_obs)     # 137.03599908…
inv_alpha = 1 / alpha_obs                 # 137.035999084…
# 若用反解 Δ_top 则 α 精确命中（恒等）：
alpha_from_fit = mp.sin(1 / (137 + d_top_fit))
# 理论 vs 反解 Δ_top 差
d_delta = rel_err(d_top_theory, d_top_fit)
# 观测不确定度（CODATA α 相对不确定度 ~1.5e-10）
rel_unc = mp.mpf("1.5e-10")

res["checks"].append({
    "id": "C05", "name": "α=sin(1/(137+Δ_top)) 理论 Δ_top 数值命中检验",
    "d_top_theory": fmt(d_top_theory) + "（=1/(4π²)，χ/(2−2g)≡1）",
    "alpha_pred": fmt(alpha_pred),
    "alpha_obs": fmt(alpha_obs),
    "rel_diff_pred_vs_obs": fmt(rel_c05) + "（%.4e）" % float(rel_c05),
    "d_top_fit_reverse": fmt(d_top_fit) + "（=1/asin(α)−137，01A 反解）",
    "rel_diff_theory_vs_fit": fmt(d_delta) + "（%.4e，约 30%%）" % float(d_delta),
    "cross_note": "01A 附录 §3.2 用反解值判恒等 PASS；台账 C05 公式用理论值 1/(4π²) ⇒ 两者不并存",
    "conclusion": ("公式层不还原观测：α_pred 与 α_obs 相对差 %s（α 观测不确定度 %s ⇒ 差 ~5 个量级）；"
                   "命中需 Δ_top=%s（反解），与理论值差 %s；Δ_top 无独立理论来源（若自由则恒等零内容）"
                   % (fmt(rel_c05), fmt(rel_unc), fmt(d_top_fit), fmt(d_delta))),
})

# =================================================================
# 2. C16 附带：αⁿ/N 序列 vs 宇宙学占比量级
# =================================================================
# 暗能量/暗物质/重子占比（Planck 2018）：Ω_Λ≈0.6847、Ω_m≈0.3153、Ω_b≈0.0493
Omega_L = mp.mpf("0.6847"); Omega_m = mp.mpf("0.3153"); Omega_b = mp.mpf("0.0493")
seq_rows = []
for N in [mp.mpf("137"), mp.mpf("18907")]:
    row = {"N": fmt(N)}
    for n in range(1, 5):
        row["α^%d/N" % n] = fmt(alpha_obs**n / N)
    row["Ω_Λ"] = fmt(Omega_L); row["Ω_m"] = fmt(Omega_m); row["Ω_b"] = fmt(Omega_b)
    row["量级差"] = "α¹/N 与 Ω 系差 ≥ %d 个量级" % int(mp.floor(mp.log10(Omega_L / (alpha_obs/N))) )
    seq_rows.append(row)
res["checks"].append({
    "id": "C16", "name": "αⁿ/N 序列 vs 暗能量/暗物质占比（量级对应）",
    "rows": seq_rows,
    "conclusion": "无量级对应（α¹/N≈1e-5~1e-7 vs Ω_Λ≈0.68，差 ≥3 个量级）——「命名」无量化支撑（与 00 总纲「高阶力缺验证」一致）",
})

# =================================================================
# 3. C13 附带：G 公式条件式数值（若 κ_G、τ_G 即 C02 曲率挠率）
# =================================================================
# κ=ρ/L²、τ=b/L²（C02）。归一化口径 ρ=1、b=α：κ²+τ²=1/L²=1/(1+α²)
# G_pred = c³/[ℏ·(κ²+τ²)] = c³(1+α²)/ℏ
hbar = mp.mpf("1.0545718176461565e-34")
L2 = 1 + alpha_obs**2
G_pred_norm = c**3 * L2 / hbar
# 物理口径 ρ=3.33128582871e-9（C12 反解）：L²=ρ²(1+α²)
rho_phys = mp.mpf("3.33128582871e-9")
G_pred_phys = c**3 * (rho_phys**2 * L2) / hbar
G_obs = mp.mpf("6.67430e-11")
res["checks"].append({
    "id": "C13", "name": "G=c³/[ℏ(κ_G²+τ_G²)] 条件式检验（κ_G、τ_G= C02 曲率挠率）",
    "G_pred_norm_rho1": fmt(G_pred_norm) + "（归一化 ρ=1）",
    "G_pred_phys": fmt(G_pred_phys) + "（物理 ρ=C12 反解）",
    "G_obs": fmt(G_obs),
    "rel_diff_norm": fmt(rel_err(G_pred_norm, G_obs)) + "（%.3e）" % float(rel_err(G_pred_norm, G_obs)),
    "rel_diff_phys": fmt(rel_err(G_pred_phys, G_obs)) + "（%.3e）" % float(rel_err(G_pred_phys, G_obs)),
    "conclusion": "条件式失败：若 κ_G、τ_G 即 C02 曲率挠率，G 预测偏大 1e52~1e69 量级；κ_G、τ_G 必须由「拓扑」另行定义（C13 open 保留，注明条件式失败）",
})

# =================================================================
# 4. C40 附带：四组参数 |R'|=c 复算
# =================================================================
# 四组 (A,b)：b/A = 1、0.5、0.0073、2；ω√(A²+b²)=c ⇒ |R'|=c
c40_rows = []
for ratio in [mp.mpf("1"), mp.mpf("0.5"), mp.mpf("0.0073"), mp.mpf("2")]:
    A = mp.mpf("1")
    b = A * ratio
    omega = c / mp.sqrt(A*A + b*b)
    Rp_norm = omega * mp.sqrt(A*A + b*b)   # = c 精确
    c40_rows.append({"b/A": fmt(ratio), "ω": fmt(omega, 10), "|R'|": fmt(Rp_norm, 10),
                     "rel_vs_c": fmt(rel_err(Rp_norm, c))})
res["checks"].append({
    "id": "C40", "name": "四组参数 |R'|=c 复算（b/A=1/0.5/0.0073/2）",
    "rows": c40_rows,
    "conclusion": "PASS 复算：四组均精确满足 |R'|=c（偏差 0）⇒ 几何不提供 α 选择力（C40 判定保留成立）",
})

# ---------------- 汇总 ----------------
verdict = ("开放项精算验证·四期：C05 α 拓扑公式数值不命中（α_pred vs α_obs 相对差 %.4e，理论 Δ_top 与反解值差 30%%）"
           "⇒ 建议登记 C66（falsified）；C16 无量级对应（INFO）；C13 条件式失败（open 保留注明）；C40 复算 PASS"
           % float(rel_c05))
res["verdict"] = verdict

os.makedirs(OUT_DIR, exist_ok=True)
json_path = os.path.join(OUT_DIR, "空间螺旋开放项_精算验证4.json")
md_path  = os.path.join(OUT_DIR, "空间螺旋开放项_精算验证4.md")

with io.open(json_path, "w", encoding="utf-8", newline="") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)

md = []
md.append("# 空间螺旋几何化统一场论 · 开放项精算验证·四期")
md.append("")
md.append("| 项 | 值 |")
md.append("|---|---|")
md.append("| 日期 | 2026-09-27 |")
md.append("| 精度 | mpmath **250 位** |")
md.append("| 结论 | C05 数值不命中 ⇒ 建议登记 C66；C16 INFO；C13 条件式失败；C40 复算 PASS |")
md.append("")
md.append("## 1. C05 · α=sin(1/(137+Δ_top)) 理论 Δ_top 数值命中检验（核心）")
md.append("")
md.append("台账公式：Δ_top=(1/4π²)(χ/(2−2g))。闭合曲面欧拉恒等 χ=2−2g ⇒ 因子≡1，理论值：")
md.append("")
md.append("$$\\Delta_{\\rm top}=\\frac{1}{4\\pi^2}=%s$$" % fmt(d_top_theory))
md.append("")
md.append("| 量 | 值 |")
md.append("|---|---|")
md.append("| α_pred=sin(1/(137+1/4π²)) | %s |" % fmt(alpha_pred))
md.append("| α_obs（CODATA 2018） | %s |" % fmt(alpha_obs))
md.append("| 相对差 | **%s**（%.4e） |" % (fmt(rel_c05), float(rel_c05)))
md.append("| 命中所需 Δ_top（反解=1/asin(α)−137） | %s |" % fmt(d_top_fit))
md.append("| 理论 vs 反解 Δ_top 相对差 | **%s**（约 30%%） |" % fmt(d_delta))
md.append("| α 观测相对不确定度 | %s |" % fmt(rel_unc))
md.append("")
md.append("**判定**：α_pred 与 α_obs 相对差 %s（250 位确认，α 观测不确定度 1.5e-10 ⇒ 差约 5 个量级），**数值不命中**。" % fmt(rel_c05))
md.append("01A 附录 §3.2 以**反解值** Δ_top=0.03599908 判该式为恒等 PASS（信息贡献 0）；台账 C05 公式给出**理论值** 1/(4π²)=0.02533——两值相差 30%%，公式不还原观测。")
md.append("若 Δ_top 自由（反解）⇒ 恒等零内容；若 Δ_top 有理论来源（1/4π²）⇒ 数值错误。**两条路均不支持「第一性公式」声称** ⇒ 登记 C66（falsified）。")
md.append("")
md.append("## 2. C16 · αⁿ/N 序列 vs 宇宙学占比")
md.append("")
md.append("| N | α¹/N | α²/N | α³/N | α⁴/N | Ω_Λ | Ω_m | Ω_b |")
md.append("|---|---|---|---|---|---|---|---|")
for r in seq_rows:
    md.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (
        r["N"], r["α^1/N"], r["α^2/N"], r["α^3/N"], r["α^4/N"], r["Ω_Λ"], r["Ω_m"], r["Ω_b"]))
md.append("")
md.append("α¹/N≈1e-5~1e-7 vs Ω_Λ≈0.68：**差 ≥3 个量级**，无量级对应 ⇒ 「命名」无量化支撑（与 00 总纲「高阶力缺验证」一致）。")
md.append("")
md.append("## 3. C13 · G 公式条件式检验")
md.append("")
md.append("若 κ_G、τ_G 即 C02 曲率挠率：G_pred=c³(ρ²+α²ρ²)/ℏ")
md.append("")
md.append("| 口径 | G_pred | G_obs | 相对差 |")
md.append("|---|---|---|---|")
md.append("| 归一化 ρ=1 | %s | %s | %s |" % (fmt(G_pred_norm), fmt(G_obs), fmt(rel_err(G_pred_norm, G_obs))))
md.append("| 物理 ρ=C12 | %s | %s | %s |" % (fmt(G_pred_phys), fmt(G_obs), fmt(rel_err(G_pred_phys, G_obs))))
md.append("")
md.append("**条件式失败**：偏大 1e52~1e69 量级 ⇒ κ_G、τ_G 必须由「拓扑」另行定义（C13 open 保留，注明条件式失败）。")
md.append("")
md.append("## 4. C40 · 四组参数 |R'|=c 复算")
md.append("")
md.append("| b/A | ω | |R'| | 相对差 vs c |")
md.append("|---|---|---|---|")
for r in c40_rows:
    md.append("| %s | %s | %s | %s |" % (r["b/A"], r["ω"], r["|R'|"], r["rel_vs_c"]))
md.append("")
md.append("**PASS 复算**：四组均精确满足 |R'|=c ⇒ 几何不提供 α 选择力（C40 保留成立）。")
md.append("")
md.append("---")
md.append("")
md.append("*算法联盟审计组 · 开放项精算验证·四期 · 2026-09-27*")

with io.open(md_path, "w", encoding="utf-8", newline="") as f:
    f.write("\n".join(md) + "\n")

print("===== 开放项精算验证·四期 =====")
print("C05 Δ_top理论=", fmt(d_top_theory), " α_pred=", fmt(alpha_pred), " vs α_obs=", fmt(alpha_obs),
      " 相对差=", fmt(rel_c05), " 反解Δ_top=", fmt(d_top_fit), " Δ差=", fmt(d_delta))
print("C16 α/N 量级: N=137 →", fmt(alpha_obs/137), " vs Ω_Λ=", fmt(Omega_L))
print("C13 G_pred(归一化)=", fmt(G_pred_norm), " G_pred(物理)=", fmt(G_pred_phys), " vs G_obs=", fmt(G_obs))
print("C40 四组 |R'| 偏差:", "; ".join(r["rel_vs_c"] for r in c40_rows))
print("结论:", verdict)
print("产出:", json_path, "|", md_path)
