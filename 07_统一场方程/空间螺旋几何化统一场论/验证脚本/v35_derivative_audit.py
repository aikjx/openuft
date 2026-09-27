#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TUFT V3.5 · 求导证明验证精算审计
从 openuft JSON 重算：五维敏感度恒等式残差、中心差分收敛阶、伴随交叉一致性、区域外推。
只读已有数据做精算核对，不新增 claim。输出精算判定汇总。
用法： python v35_derivative_audit.py
"""
import os
import json

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
SENS = os.path.join(PARENT, "V3_4_fixed_charge_sensitivity.json")
ADJ = os.path.join(PARENT, "V3_5_adjoint_crosschecks.json")

sens = json.load(open(SENS, "r", encoding="utf-8"))
adj = json.load(open(ADJ, "r", encoding="utf-8"))

print("=" * 64)
print("精算一：五维敏感度变分恒等式核对 dE=w dQ+2E_EM/e de+I2 dmu2-I4 dlam+I6 dg6")
print("=" * 64)
for eta in ["e", "Q", "mu2", "lambda", "g6"]:
    s = sens["sensitivity"][eta]
    print("  d%sE: grad=%.12e envelope=%.12e identity_error=%+.2e"
          % (eta, s["E"], s["envelope"], s["identity_error"]))
print("  最大 |identity_error| =", max(abs(sens["sensitivity"][e]["identity_error"]) for e in sens["sensitivity"]))
print("  矩 I2,I4,I6 =", sens["base"]["moments"])

print("\n" + "=" * 64)
print("精算二：中心差分收敛阶（误差随 step 减半 → ÷4 为二阶）")
print("=" * 64)
def ratios(errs):
    a = [abs(e) for e in errs]
    return [a[i]/a[i+1] for i in range(len(a)-1)]
for key in ["e", "Q", "mu2", "lambda", "g6"]:
    steps = sens["finite_differences"][key]
    Eerr = [s["errors"]["E"] for s in steps]
    print("  %s: step=%s |E误差|=%s → 比率=%s"
          % (key, [s["step"] for s in steps], ["%.1e" % e for e in Eerr],
             ["%.2f" % r for r in ratios(Eerr)]))

print("\n" + "=" * 64)
print("精算三：伴随交叉验证（中性固定荷 dI/dλ 直接法 vs 伴随法）")
print("=" * 64)
for g in adj["grids"]:
    print("  step=%.2f: direct=%.10f adjoint=%.10f duality_error=%+.2e adjoint_residual=%.2e"
          % (g["step"], g["direct_dI_dlambda"], g["adjoint_dI_dlambda"],
             g["duality_error"], g["adjoint_residual"]))
print("  错误版(未约束求导)=", adj["grids"][0]["wrong_unconstrained_derivative"], "(对比正确值~28.23)")

print("\n" + "=" * 64)
print("精算四：区域外推 R=100 → R=140")
print("=" * 64)
b100, b140 = sens["base"], sens["refinement"]["base"]
s100, s140 = sens["sensitivity"]["e"], sens["refinement"]["e_sensitivity"]
print("  E: %.12e -> %.12e  Δ=%.2e" % (b100["E"], b140["E"], b140["E"]-b100["E"]))
print("  dE/de: %.12e -> %.12e  Δ=%.2e" % (s100["E"], s140["E"], s140["E"]-s100["E"]))
print("  e 恒等式残差: %.2e -> %.2e" % (s100["identity_error"], s140["identity_error"]))

print("\n" + "=" * 64)
print("精算判定汇总")
print("=" * 64)
ok_conv = True
for key in ["e", "Q", "mu2", "lambda", "g6"]:
    if not all(3.2 < r < 5.0 for r in ratios([s["errors"]["E"] for s in sens["finite_differences"][key]])):
        ok_conv = False
print("中心差分二阶收敛(比率∈[3.2,5]):", ok_conv)
maxid = max(abs(sens["sensitivity"][e]["identity_error"]) for e in sens["sensitivity"])
maxdu = max(abs(g["duality_error"]) for g in adj["grids"])
print("变分恒等式最大残差 |err|max = %.2e (双精度 eps~2e-16, 高~5量级)" % maxid)
print("伴随直接-对偶最大偏差 |duality|max = %.2e" % maxdu)
print("外推: E Δ=%.1e, dE/de Δ=%.1e" % (b140["E"]-b100["E"], s140["E"]-s100["E"]))
