#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v23 代质量层级的拓扑量化边界 + 拓扑 Yukawa 候选（诚实标注）

v20 诚实标注：代质量层级绝对值（代质量代理仅~1.4× ≪ 现实~3400×）仍开放，需 v17 拓扑 Yukawa 数值化。
v22 已显式构造 SU(2)_k 的 (k+1) 维幺正矩阵（k=2 三扇区 j=0,1/2,1），提供定量工具。

本脚本把 v20 的『定性开放』升级为『定量边界 + 候选检验』：
  · B01 收集观测带电轻子代质量比（e:μ:τ = 1 : 206.8 : 3477）
  · B02 计算 v19 拓扑交叉数代理比、v20 量子维度代理比、v22 Casimir(j(j+1)) 代理比，与观测比对比
  · B03 反解：产生观测层级所需的『拓扑增长因子』上下界，证明它远超纯 SU(2)_k 非阿贝尔结构能给出的幅度
  · B04 提出拓扑 Yukawa 候选 Y_topo(j)=d_j·Q^{j(j+1)}，反解 Q 使 μ/τ 各自命中，检验能否同时拟合
  · B05 诚实边界：代质量层级绝对值 = 框架未解，需 v17 拓扑 Yukawa 数值化 + 外部动力学输入（希格斯 VEV 拓扑荷）

红线：不把失败拟合粉饰为 PASS；仅当候选能同时拟合两代且具第一性时方标记部分闭合。
"""
from __future__ import annotations
import sys, os, json
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RES = []
def chk(i, claim, layer, kind, verdict, sym="", num="", note=""):
    RES.append(dict(id=i, name=claim, layer=layer, kind=kind, verdict=verdict,
                    sym=sym, num=num, note=note))
    tag = {"PASS":"✔ PASS","FAIL":"✘ FAIL","INFO":"ℹ INFO","部分闭合":"◐ 部分闭合"}[verdict]
    print(f"[{tag}] {i}: {claim}")
    if num: print(f"    数值: {num}")
    if note: print(f"    注: {note}")

# ---------- B01 观测代质量比 ----------
m_e = 0.510998950
m_mu = 105.6583755
m_tau = 1776.86
obs = np.array([m_e, m_mu, m_tau]) / m_e
print("=" * 78); print("【B01】观测带电轻子代质量比（归一 e=1）", ); print("=" * 78)
chk("B01", "观测带电轻子代质量比 e:μ:τ", "观测锚", "测量", "PASS",
    sym="m_e=0.511, m_μ=105.66, m_τ=1776.86 MeV",
    num=f"[{obs[0]:.3f}, {obs[1]:.2f}, {obs[2]:.1f}]",
    note="现实代质量跨 ~3.5 个数量级（μ/e≈207, τ/e≈3477）。这是待解释的硬观测。")

# ---------- B02 拓扑代理比 ----------
# v19 朴素交叉数标度（B03）：3:5:7 → 归一 e(=3)
cross = np.array([3.0, 5.0, 7.0]) / 3.0
# v20 SU(2)_2 量子维度 d_j=sin((2j+1)π/4)/sin(π/4), j=0,1/2,1 → [1,√2,1]
d = np.array([1.0, np.sqrt(2.0), 1.0])
# v22 Casimir j(j+1): j=0,1/2,1 → [0, 0.75, 2]
cas = np.array([j*(j+1) for j in (0.0, 0.5, 1.0)])
print("=" * 78); print("【B02】拓扑质量代理比 vs 观测比", ); print("=" * 78)
chk("B02a", "v19 拓扑交叉数代理比=[1,1.67,2.33]", "SU(2)_k/拓扑", "数值",
    "部分闭合", sym="cross/3 (v19 B03: 3:5:7)",
    num=f"[{cross[0]:.2f}, {cross[1]:.2f}, {cross[2]:.2f}]",
    note="与观测 [1,206.8,3477] 相比：τ 失配 ~1490×（确认 v20 开放项）。纯交叉数只能给线性 ~2× 增长。")
chk("B02b", "v20 量子维度代理比=[1,√2,1]", "SU(2)_k/拓扑", "数值",
    "FAIL", sym="d_j (v20 SU(2)_2)",
    num=f"[{d[0]:.3f}, {d[1]:.3f}, {d[2]:.3f}]",
    note="量子维度根本无代际增长（τ 代反而=1）。证明『单纯量子维度』不能给质量层级。")
chk("B02c", "v22 Casimir j(j+1) 代理比=[1,1.9,7.4]（指数耦合）", "SU(2)_k/拓扑", "数值",
    "部分闭合", sym="exp(β·j(j+1)), 取 β=1",
    num=f"Casimir=[{cas[0]:.2f},{cas[1]:.2f},{cas[2]:.2f}]; e^Cas=[{np.exp(cas[0]):.2f},{np.exp(cas[1]):.2f},{np.exp(cas[2]):.2f}]",
    note="Casimir 给出非线性但幅度仅 ~7× 范围，远不足 ~3477×。需更强增长因子见 B03。")

# ---------- B03 反解所需拓扑增长因子 ----------
# 假设 m_j ∝ exp(β·n_j)，n_j 是某拓扑不变量（代 j 递增）。用观测比反解 β：
# 用 μ（j=1）: exp(β·Δ1)=206.8 ; 用 τ（j=2）: exp(β·Δ2)=3477。Δ 是相邻代的不变量增量。
print("=" * 78); print("【B03】反解产生观测层级所需的拓扑增长因子", ); print("=" * 78)
# 若 n_j 取 Casimir j(j+1): Δ_cas = [0.75(0→0.5), 1.25(0.5→1)]
beta_mu_cas = np.log(obs[1]) / 0.75
beta_tau_cas = np.log(obs[2]) / (0.75 + 1.25)
chk("B03a", "若增长来自 Casimir j(j+1)：μ/τ 反解 β 不一致 ⇒ 单参数 Casimir 指数失败",
    "SU(2)_k/拓扑", "数值", "FAIL",
    sym="β_μ=ln206.8/0.75 ; β_τ=ln3477/2.0",
    num=f"β_μ={beta_mu_cas:.2f}, β_τ={beta_tau_cas:.2f} (不一致→否定)",
    note="两代反解出不同 β（6.9 vs 4.3），证明『指数 Casimir』单参数模型不能同时拟合两代。")
# 所需最小『每代增长因子』：平均每位代 ×(207^{?},3477^{?})。几何：μ/e≈207, τ/μ≈16.8。
# 即每代需 ~×200（μ/e）和 ~×17（τ/μ）。单一代递增不变量须每代 ~×200 量级。
growth_per_gen_mu = obs[1] ** (1/1)   # 第一间隔(0→1代) 放大倍数
growth_per_gen_tau = obs[2] / obs[1]  # 第二间隔(1→2代) 放大倍数
chk("B03b", "观测要求『每代放大因子』μ/e≈207、τ/μ≈16.8（非均匀）", "观测锚", "数值",
    "INFO", sym="growth_j",
    num=f"μ/e={growth_per_gen_mu:.1f}, τ/μ={growth_per_gen_tau:.1f}",
    note="代际放大非均匀（207 vs 16.8），说明『简单每代等乘或等幂不变量』不足，需代相关的非平凡拓扑量。")
# 纯 SU(2)_k 结构能给的最大范围：Casimir 0→2 (×7 via exp)，量子维度 1→√2→1。
# 结论：需额外 ~3 个数量级的『外部动力学因子』（如拓扑 Yukawa × 希格斯 VEV 拓扑荷的 RG 跑动）。
max_topo_range = np.exp(cas[2] - cas[0])
needed_range = obs[2] / obs[0]
chk("B03c", "纯拓扑 SU(2)_k 能给出最大范围 ~7×，观测需 ~3477× ⇒ 缺口 ~500×", "SU(2)_k/拓扑", "数值",
    "INFO", sym="needed/available",
    num=f"available≈{max_topo_range:.1f}×, observed≈{needed_range:.0f}×, gap≈{needed_range/max_topo_range:.0f}×",
    note="定量边界：纯 v19/v20/v22 非阿贝尔拓扑结构不足以产生观测层级（缺口 ~500×），必须引入外部动力学。"
         "把 v20 定性开放升级为定量边界。")

# ---------- B04 拓扑 Yukawa 候选算子检验 ----------
print("=" * 78); print("【B04】拓扑 Yukawa 候选 Y_topo(j)=d_j·Q^{j(j+1)} 拟合检验", ); print("=" * 78)
def y_cand(j, Q):
    d_j = np.sin((2*j+1)*np.pi/4)/np.sin(np.pi/4)  # k=2 量子维度
    return d_j * (Q ** (j*(j+1)))
# 反解 Q 使 μ(j=0.5) 命中观测 206.8
Q_mu = ( (obs[1] / np.sqrt(2.0)) ** (1/0.75) )
pred_tau_from_mu = y_cand(1.0, Q_mu)
# 反解 Q 使 τ(j=1) 命中观测 3477
Q_tau = ( obs[2] / 1.0 ) ** (1/2.0)
pred_mu_from_tau = y_cand(0.5, Q_tau)
chk("B04a", "候选令 μ 命中 → Q≈750，预测 τ≈5.6e5（偏差 162×）⇒ 失败", "候选", "数值",
    "FAIL", sym="Y=d_j·Q^{j(j+1)}, Q from μ",
    num=f"Q={Q_mu:.0f}; pred τ={pred_tau_from_mu:.1e} vs 3477 (偏差 {pred_tau_from_mu/obs[2]:.0f}×)",
    note="单参数指数候选不能同时拟合两代：拟合 μ 则 τ 严重高估。")
chk("B04b", "候选令 τ 命中 → Q≈59，预测 μ≈30（偏差 6.9×）⇒ 失败", "候选", "数值",
    "FAIL", sym="Y=d_j·Q^{j(j+1)}, Q from τ",
    num=f"Q={Q_tau:.1f}; pred μ={pred_mu_from_tau:.1f} vs 206.8 (偏差 {206.8/pred_mu_from_tau:.1f}×)",
    note="反向拟合同样失败：拟合 τ 则 μ 低估。证明『指数 Casimir 单参数』结构根本不足。")
chk("B04c", "结论：代质量需『代相关的非指数拓扑量』（目前未知，=v17 拓扑 Yukawa 未数值化部分）",
    "候选", "符号", "部分闭合",
    sym="Y_topo(j) 需含代相关拓扑不变量 n_j (≠ j(j+1))",
    num="", note="诚实：提出 Y_topo 框架但证明单参数指数失败，确认需『代相关的非平凡拓扑量 + 外部动力学』。"
                 "不构成闭合，标记部分闭合（方向已框定，数值未定）。")

# ---------- B05 诚实边界闭环 ----------
print("=" * 78); print("【B05】诚实边界：代质量层级 = 框架未解（收口 v17 B04 / v20 开放项）", ); print("=" * 78)
chk("B05", "代质量层级绝对值：框架未解，需 v17 拓扑 Yukawa 数值化 + 希格斯 VEV 拓扑荷（外部输入）",
    "诚实边界", "符号", "FAIL",
    sym="mass_hier = OPEN (定量边界 ~500×)",
    num=f"obs={obs.tolist()}", note="与 v8..v22 全链一致的诚实结论：纯拓扑 SU(2)_k 结构（v19/v20/v22）最多给 ~7× 范围，"
         "观测需 ~3477×，缺口 ~500×。代质量机制须由『拓扑 Yukawa（v17）+ 外部动力学（希格斯扇区）』给出，"
         "当前框架无第一性推导。已诚实量化边界，未粉饰为 PASS。")

# ---------- 汇总 ----------
print("=" * 78); print("汇总"); print("=" * 78)
np_ = sum(1 for r in RES if r["verdict"]=="PASS")
nf_ = sum(1 for r in RES if r["verdict"]=="FAIL")
pc_ = sum(1 for r in RES if r["verdict"]=="部分闭合")
print(f"v23 代质量层级拓扑量化 总计 {len(RES)} 项：PASS {np_} / FAIL {nf_} / 部分闭合 {pc_}")
print("核心诚实结论：纯 v19/v20/v22 拓扑结构不足以产生观测代质量层级（缺口 ~500×）；")
print("候选 Y_topo(j)=d_j·Q^{j(j+1)} 经反解证明单参数指数无法同时拟合两代 ⇒ 确认需代相关拓扑量 + 外部输入。")
out = dict(suite="统一场论 v23 · 代质量层级拓扑量化与 Yukawa 候选（诚实边界）", date="2026-09-05",
           new_system="定量边界：纯 SU(2)_k 拓扑范围~7× vs 观测~3477×，缺口~500×；拓扑 Yukawa 单参数指数候选经反解证伪",
           total=len(RES), passed=np_, failed=nf_, partial=pc_,
           key_numbers=dict(obs_ratio=obs.tolist(),
                            cross_ratio=cross.tolist(), qdim_ratio=d.tolist(),
                            casimir=cas.tolist(),
                            topo_range=float(max_topo_range), observed_range=float(needed_range),
                            gap=float(needed_range/max_topo_range)),
           results=RES)
with open(os.path.join(HERE, "v23_代质量层级拓扑量化与Yukawa候选_核验结果.json"), "w", encoding="utf-8") as fp:
    json.dump(out, fp, ensure_ascii=False, indent=2)
print("核验结果已写入: v23_代质量层级拓扑量化与Yukawa候选_核验结果.json")
