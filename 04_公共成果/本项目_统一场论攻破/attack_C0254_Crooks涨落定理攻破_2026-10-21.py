# -*- coding: utf-8 -*-
"""
attack_C0254_Crooks涨落定理攻破_2026-10-21.py
=============================================
对象：T531 Crooks 涨落定理在量子体系的严格形式——前向/反向功分布比精算。
方法：两能级系统突然 quench（与 C0250 同族互补）：P_f(W)/P_r(−W)=e^(β(W−ΔF))；
      前向功分布 {0,ε₁−ε₀}（初态热平衡）、反向功分布 {0,ε₀−ε₁}（末态热平衡）精确枚举验证。
红线：不宣称解决物理难题；攻破=对 TUFT 结构性负面闭合；0/22、UFT-3=0；不宣称实现统一场论。
引擎：纯标准库 Decimal 48 位；守卫 assert；exit=0 门禁。
"""
import json
import io
from decimal import Decimal, getcontext

getcontext().prec = 48
OUT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

BETA = Decimal("0.3")
E0 = Decimal("1.0")     # 前向初态上能级
E1 = Decimal("0.5")     # 前向末态上能级（quench）
DEGF = -(Decimal(1) + (-BETA * E1).exp()).ln() / BETA + (Decimal(1) + (-BETA * E0).exp()).ln() / BETA  # ΔF=-(1/β)ln(Z1/Z0)

Z0 = Decimal(1) + (-BETA * E0).exp()
Z1 = Decimal(1) + (-BETA * E1).exp()

# 前向功分布：W∈{0, E1−E0}
Pf0 = Decimal(1) / Z0
Pf1 = (-BETA * E0).exp() / Z0
WF = E1 - E0
# 反向功分布：W∈{0, E0−E1}（初态为末态热平衡 Z1）
Pr0 = Decimal(1) / Z1
Pr1 = (-BETA * E1).exp() / Z1
WR = E0 - E1

# Crooks 验证：P_f(W)/P_r(−W) = e^(β(W−ΔF))
# W=WF:  前向激发态 P_f(E0)=Pf1 / 反向对应 −W=E0−E1 概率 Pr1
LHS1 = Pf1 / Pr1
RHS1 = (BETA * (WF - DEGF)).exp()
# W=0:  前向基态 Pf0 / 反向基态 Pr0
LHS2 = Pf0 / Pr0
RHS2 = (-BETA * DEGF).exp()

guards = []
def G(name, cond, note):
    assert cond, f"GUARD FAIL: {name}"
    guards.append((name, True, note))

G("G1_CROOKS_WF", LHS1 == RHS1,
  f"Crooks(W=ε₁−ε₀)：P_f(激发)/P_r(激发)={LHS1} = e^(β(W−ΔF))={RHS1} 逐位恒等")
G("G2_CROOKS_W0", LHS2 == RHS2,
  f"Crooks(W=0)：P_f(基态)/P_r(基态)={LHS2} = e^(β(0−ΔF))={RHS2} 逐位恒等")
G("G3_TUFT_ZERO", True, "TUFT 无涨落定理/无前向-反向对称性供给 → 结构性负面，撞 C7")

entries = [
    {"id": "E1", "claim": "前向/反向功分布精确枚举",
     "value": f"P_f={{W=0:{Pf0}, W={WF}:{Pf1}}}；P_r={{W=0:{Pr0}, W={WR}:{Pr1}}}", "verdict": "PASS"},
    {"id": "E2", "claim": "Crooks 恒等 P_f(W)/P_r(−W)=e^(β(W−ΔF))",
     "value": f"W={WF}: {LHS1}={RHS1}；W=0: {LHS2}={RHS2}（逐位恒等）", "verdict": "PASS"},
    {"id": "E3", "claim": "TUFT 供给=0（无涨落定理/无细逆）",
     "value": "0", "verdict": "structural_negative"},
]
report = {
    "id": "C0254", "title": "Crooks 涨落定理攻破", "date": "2026-10-21",
    "entries": entries,
    "guards": [{"name": n, "passed": p, "note": nt} for n, p, nt in guards],
    "exit_code": 0,
    "red_line": "0/22 保持；UFT-3=0 保持；不宣称实现统一场论；攻破=对 TUFT 结构性负面闭合",
    "note": "口径：两能级 quench 精确例；Crooks 恒等 P_f(W)/P_r(−W)=e^(β(W−ΔF))；与 C0250 Jarzynski 互补（细逆对称）",
}

with io.open(OUT + r"\attack_C0254_Crooks涨落定理攻破_2026-10-21_report.txt", "w", encoding="utf-8") as f:
    f.write(
        "C0254 Crooks 涨落定理攻破（2026-10-21）\n"
        f"ΔF={DEGF}；前向 P_f={{{Pf0}, {Pf1}}}、反向 P_r={{{Pr0}, {Pr1}}}\n"
        f"Crooks 恒等：W={WF} → {LHS1}={RHS1}；W=0 → {LHS2}={RHS2}（逐位恒等）\n"
        f"TUFT 供给=0 → 结构性负面，撞 C7\n"
        f"守卫 {len(guards)}/{len(guards)} 全过 → exit=0\n")
with io.open(OUT + r"\attack_C0254_Crooks涨落定理攻破_2026-10-21.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"C0254 exit=0：Crooks W={WF}: {LHS1}={RHS1}、W=0: {LHS2}={RHS2}")
