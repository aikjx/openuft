# -*- coding: utf-8 -*-
"""
§32 50/50̄ 分解级跑动：Δb 精确值
=================================
用 SU(5) 50 表示的完整 SM 分解（权重格程序严格验证）确定对 c1=3/α₂−2/α₃−1/α₁
组合的精确 β 贡献，检验 §31 的 Δb* 门槛（10TeV [1.9,5.2]、1TeV [4.2,9.8]）。

分解（权重格直接聚类，见 §32 主文档附录 C）：
50 = (6,3,1/3) ⊕ (3̄,1,1/3) ⊕ (8,2,−1/2) ⊕ (3,2,7/6) ⊕ (6̄,1,−4/3) ⊕ (1,1,2)
     [18]        [3]        [16]        [6]        [6]         [1]   = 50
超荷 y 为 Q−T3 下标（PDG 约定）。

T 值（标准）：SU(3): T(3)=T(3̄)=1/2, T(6)=T(6̄)=5/2, T(8)=3
           SU(2): T(2)=1/2, T(3)=2
T1 = (3/5)·Σ_R y²（GUT 归一化）
Δb_c1 = 3·b2 − 2·b3 − b1 = 3·T2 − 2·T3 − T1
"""
import json, math

# ---------------- 分解与每分量 T ----------------
# (标签, SU(3)表示, SU(2)表示, 超荷y, 维数)
COMP = [
    ("(6,3,1/3)",  "6",  "3",  1/3,   18),
    ("(3̄,1,1/3)", "3b", "1",  1/3,    3),
    ("(8,2,−1/2)", "8",  "2", -1/2,   16),
    ("(3,2,7/6)",  "3",  "2",  7/6,    6),
    ("(6̄,1,−4/3)","6b", "1", -4/3,    6),
    ("(1,1,2)",    "1",  "1",  2,      1),
]
T3_SU3 = {"3": 0.5, "3b": 0.5, "6": 2.5, "6b": 2.5, "8": 3.0, "1": 0.0}
T2_SU2 = {"2": 0.5, "3": 2.0, "1": 0.0}

def comp_T(c):
    """返回 (T3, T2, T1) 分量级"""
    label, r3, r2, y, dim = c
    T3 = T3_SU3[r3] * (3 if r2 == "3" else 2 if r2 == "2" else 1)  # SU(3) index × SU(2) 多重度
    T2 = T2_SU2[r2] * (6 if r3 in ("6","6b") else 8 if r3 == "8" else 3 if r3 in ("3","3b") else 1)
    T1 = (3.0/5.0) * dim * y*y
    return T3, T2, T1

rows = []
for c in COMP:
    T3, T2, T1 = comp_T(c)
    rows.append({"comp": c[0], "dim": c[4], "y": c[3], "T3": T3, "T2": T2, "T1": T1,
                 "d_b": 3*T2 - 2*T3 - T1})

T3tot = sum(r["T3"] for r in rows)
T2tot = sum(r["T2"] for r in rows)
T1tot = sum(r["T1"] for r in rows)

res = {}
# ---------------- V1: 分解维数 + index 统一 ----------------
res["V1_decomp"] = {
    "sum_dims": sum(r["dim"] for r in rows),
    "expected": 50,
    "T3_total": T3tot, "T2_total": T2tot, "T1_total": T1tot,
    "T50_expected": 35.0/2.0,
    "index_unified": abs(T3tot - T2tot) < 1e-9 and abs(T2tot - T1tot) < 1e-9
}

# ---------------- V2: 完整 50 的 Δb_c1 = 0 ----------------
d_b_full = 3*T2tot - 2*T3tot - T1tot
res["V2_full_repr"] = {
    "d_b_c1_full_50": d_b_full,
    "comment": "完整 SU(5) 表示对 c1 组合零贡献（§31 '50→~10' 量级估算修正为 0）"
}

# ---------------- V3: 分裂模型（doublet-triplet splitting）----------------
# 方案 S1: 双重态类分量（SU(2) 非单态）在区间活跃（色类先积分出）
dual = [r for r in rows if r["comp"] in ("(6,3,1/3)", "(8,2,−1/2)", "(3,2,7/6)")]
sing = [r for r in rows if r["comp"] not in ("(6,3,1/3)", "(8,2,−1/2)", "(3,2,7/6)")]
T3d = sum(r["T3"] for r in dual); T2d = sum(r["T2"] for r in dual); T1d = sum(r["T1"] for r in dual)
T3s = sum(r["T3"] for r in sing); T2s = sum(r["T2"] for r in sing); T1s = sum(r["T1"] for r in sing)
d_b_S1 = 3*T2d - 2*T3d - T1d   # 双重态类活跃
d_b_S2 = 3*T2s - 2*T3s - T1s   # 色类活跃
res["V3_split"] = {
    "S1_doublet_active": d_b_S1,
    "S2_singlet_active": d_b_S2,
    "check_S1_plus_S2_eq_full": abs((d_b_S1 + d_b_S2) - d_b_full) < 1e-9,
    "pair_50_50bar": {"S1": 2*d_b_S1, "S2": 2*d_b_S2}
}

# ---------------- V4: M_extra 反推（10TeV 复活带 κ∈[38,149]）----------------
# κ(δ)=exp((5π/6)δ), δ=Δb·ln(M_extra/M_GUT)/2π
M_GUT = 1.341e16
c1_coef = 5*math.pi/6.0
def kappa(delta): return math.exp(c1_coef*delta)
def delta_of_kappa(k): return math.log(k)/c1_coef

band10 = (38.0, 149.0)
d_lo, d_hi = delta_of_kappa(band10[0]), delta_of_kappa(band10[1])
res["V4_band10"] = {
    "delta_star": [d_lo, d_hi],
    "M_extra_over_MGUT_db15": [math.exp(2*math.pi*d/d_b_S1) for d in (d_lo, d_hi)],
    "M_extra_over_MGUT_db30": [math.exp(2*math.pi*d/(2*d_b_S1)) for d in (d_lo, d_hi)],
    "s31_threshold": [1.9, 5.2],
    "comment": "Δb=15: M_extra∈[1.79,2.23]M_GUT; Δb=30(50+50̄): M_extra∈[1.34,1.49]M_GUT —— 阈值分离 ln(M_extra/M_GUT)~0.3–0.8 处于 GUT 阈值不确定度内"
}

# 1TeV 复活带（κ∈[3.2e3,1.25e4]）——微扰界对照
band1 = (3.2e3, 1.25e4)
d1_lo, d1_hi = delta_of_kappa(band1[0]), delta_of_kappa(band1[1])
M_pl = 1.22e19
M_Hc = 9.32e15  # §27 两循环（含 Hc 入 β）标度
k_HK = 1.25e4
M_Hc_eff_HK = M_Hc * kappa(delta_of_kappa(k_HK))
res["V5_1TeV_excl"] = {
    "delta_star_1TeV": [d1_lo, d1_hi],
    "M_extra_over_MGUT_db15": [math.exp(2*math.pi*d/d_b_S1) for d in (d1_lo, d1_hi)],
    "M_Hc_eff_at_kappa_HK": M_Hc_eff_HK,
    "M_Pl": M_pl,
    "excluded": M_Hc_eff_HK > M_pl,
    "comment": "1TeV 复活带匹配 Δb=15 需 M_extra~3.6M_GUT，但 κ_HK 端 M_Hc_eff>M_Pl 非物理 → 排除强化"
}

# ---------------- V6: 汇总 ----------------
ok = (res["V1_decomp"]["sum_dims"] == 50 and res["V1_decomp"]["index_unified"]
      and abs(d_b_full) < 1e-9
      and abs(d_b_S1 - 15.0) < 1e-9 and abs(d_b_S2 + 15.0) < 1e-9
      and res["V5_1TeV_excl"]["excluded"])
res["V6_summary"] = {
    "verified": ok,
    "fingerprint": "可检验模型指纹：GUT 标度额外 50/50̄ 对 + doublet-triplet 分裂，Δb_c1=±15/±30（完整表示 0）"
}

out = {"section": 32, "section_name": "50/50̄ 分解级跑动（Δb 精确值）",
       "component_rows": rows, "results": res}
with open("§32_50分解级跑动数据.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

# ---------------- 控制台输出 ----------------
print("=" * 62)
print("[V1] SU(5) 50 分解（权重格程序交叉验证）")
for r in rows:
    print(f"  {r['comp']:<12} dim={r['dim']:2d}  T3={r['T3']:6.2f} T2={r['T2']:6.2f} T1={r['T1']:6.2f}  Δb_i={r['d_b']:7.2f}")
print(f"  总维数={res['V1_decomp']['sum_dims']} (期望 50)  T3=T2=T1={T3tot}={T2tot}={T1tot} (=35/2 ✓)")
print("[V2] 完整 50 表示 Δb_c1 = 3·T2−2·T3−T1 =", round(d_b_full, 10), "→ §31'50→~10'修正为 0")
print(f"[V3] 分裂模型：双重态类活跃 Δb=+{d_b_S1:.0f}；色类活跃 Δb={d_b_S2:.0f}；50+50̄ 对 ±{2*d_b_S1:.0f}/±{2*d_b_S2:.0f}")
print("[V4] 10TeV 复活带（κ∈[38,149]，Δb*∈[1.9,5.2]）：")
print(f"     Δb=15  → M_extra∈[{res['V4_band10']['M_extra_over_MGUT_db15'][0]:.2f},{res['V4_band10']['M_extra_over_MGUT_db15'][1]:.2f}]M_GUT")
print(f"     Δb=30  → M_extra∈[{res['V4_band10']['M_extra_over_MGUT_db30'][0]:.2f},{res['V4_band10']['M_extra_over_MGUT_db30'][1]:.2f}]M_GUT")
print(f"[V5] 1TeV：Δb=15 需 M_extra~{res['V5_1TeV_excl']['M_extra_over_MGUT_db15'][0]:.2f}M_GUT；κ_HK 端 M_Hc_eff={res['V5_1TeV_excl']['M_Hc_eff_at_kappa_HK']:.3e} > M_Pl={M_pl:.2e} ✗ 排除")
print(f"[V6] 判定 verified={ok}")
print("exit 0")
