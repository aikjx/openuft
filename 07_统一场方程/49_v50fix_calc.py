# -*- coding: utf-8 -*-
"""openuft/07_统一场方程 · 编号 49 = 系列 51 · V50 修复草案卷锚点
250-digit anchors (repair of A2 to Frenet-Serret closed-dimension form):
  helix R=1, h=1: kappa = R/(R^2+h^2), tau = h/(R^2+h^2)
    -> kappa^2+tau^2 = 1/(R^2+h^2) = 0.5 ; (omega/c)^2 = 0.5
    omega/c = sqrt(0.5); lambda = 2 pi / sqrt(kappa^2+tau^2) = 2 pi sqrt(2)
  MM constraint: log10(1.5e-9)
  D mod 8 = 2 allowed MW dims: 2, 10, 18, 26, 34 (D=10 superstring, vol 26)
Writes 49_v50fix_calc_results.json
"""
import json
import mpmath as mp

mp.mp.dps = 250
res = {}

R = mp.mpf("1")
h = mp.mpf("1")
kap = R / (R**2 + h**2)
tau = h / (R**2 + h**2)
kap2tau2 = kap**2 + tau**2
oc = mp.sqrt(mp.mpf("0.5"))
lam = 2 * mp.pi / mp.sqrt(kap2tau2)

res["A2_repair_anchors"] = {
  "kappa (R=1,h=1)": mp.nstr(kap, 250),
  "tau (R=1,h=1)": mp.nstr(tau, 250),
  "kappa^2+tau^2 = 1/(R^2+h^2)": mp.nstr(kap2tau2, 250),
  "omega/c = sqrt(0.5)": mp.nstr(oc, 250),
  "lambda = 2 pi sqrt(2)": mp.nstr(lam, 250),
  "note": "A2' 修复版 κ²+τ²=(ω/c)² 量纲闭合（L⁻²）；数值演示=常曲率常挠率螺旋线恒等式（微分几何，非新物理）",
}

res["constraint_anchors"] = {
  "MM_log10(1.5e-9)": mp.nstr(mp.log10(mp.mpf("1.5e-9")), 250),
  "MW_allowed_dims": "D ≡ 2 (mod 8)：2, 10, 18, 26, 34（D=10 超弦，26 卷已证）",
  "note": "MM 干涉实验：光速各向同性 Δc/c<1.5×10⁻⁹（文献）；A1' 修复为经验公理",
}

res["repair_verdict"] = {
  "A1": "可修：降级为经验公理（光锥因果+MM 约束），非拓扑不变量——已修",
  "A2": "可修：量纲闭合版 κ²+τ²=(ω/c)²（Frenet–Serret 恒等式）；ℓ_P 退场——已修，但内容=定义式，仍需动力学才有预测力",
  "A3": "不可修：D=32≡0 (mod 8) 无 Majorana–Weyl；坚持 32 维须放弃手征 SM——删除 32 维，改 D=10（已建）或标维数 OPEN",
  "A4": "可给操作定义草案：模稳定（生成规则）+超对称破缺（终止）+CODATA 阈值（判据）——仍 OPEN",
  "verdict": "修复版 A1'+A2'+D 未定+A4' 仍无推导链——按 V50 纪律标 OPEN；A2' 可与真实微分几何对话（螺旋恒等式）",
}

print(json.dumps(res, ensure_ascii=False, indent=2))
with open(r"D:\a10\aikjx\code\my_lib\openuft\07_统一场方程\49_v50fix_calc_results.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("\nOK -> 49_v50fix_calc_results.json")
