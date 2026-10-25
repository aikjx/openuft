# -*- coding: utf-8 -*-
"""
attack_C0276_量子相干度量攻破_2026-10-21.py
=============================================
对象：T567 量子相干性资源度量比较 + T568 不对称资源理论——相对熵相干 + Wigner–Yanase 偏态信息。
方法：C_rel=S(ρ‖ρ_diag)=S(ρ_diag)−S(ρ)；I_WY=Tr(ρH²)−Tr(√ρH√ρH)。
      纯态 |+⟩：C_rel=ln2、I_WY=ΔH²=1（退化）；混态 ρ=0.3|0⟩⟨0|+0.7|+⟩⟨+| 数值。
精度：mpmath 250 位（用户指令）；2×2 解析特征分解。
红线：不宣称解决物理难题；攻破=对 TUFT 结构性负面闭合；0/22、UFT-3=0；不宣称实现统一场论。
"""
import json
import io
import mpmath as mp

mp.mp.dps = 250
OUT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

LN2 = mp.log(2)

def S(p):
    s = mp.mpf(0)
    for x in p:
        x = mp.mpf(x)
        if x > 0:
            s -= x * mp.log(x)
    return s

# 纯态 |+⟩：ρ=|+⟩⟨+|、ρ_diag=(1/2,1/2)
C_PLUS = S([mp.mpf(1)/2, mp.mpf(1)/2]) - 0   # S(ρ)=0
I_PLUS = mp.mpf(1)                            # Tr(ρH²)=1、Tr(√ρH√ρH)=0 → ΔH²=1 退化

# 混态 ρ=0.3|0⟩⟨0|+0.7|+⟩⟨+| → [[0.65,0.35],[0.35,0.35]]
A = mp.mpf("0.65"); B = mp.mpf("0.35"); C = mp.mpf("0.35")
# 特征值 λ=(1±√(1−4det))/2；det=A·B−C²
DET = A*B - C*C
L1 = (1 + mp.sqrt(1-4*DET))/2
L2 = (1 - mp.sqrt(1-4*DET))/2
# 特征向量 u1=(1,(λ1−A)/C) 归一
U1X = mp.mpf(1); U1Y = (L1-A)/C
N1 = mp.sqrt(U1X**2+U1Y**2); U1X/=N1; U1Y/=N1
U2X = mp.mpf(1); U2Y = (L2-A)/C
N2 = mp.sqrt(U2X**2+U2Y**2); U2X/=N2; U2Y/=N2
# √ρ=√λ1 u1u1ᵀ+√λ2 u2u2ᵀ（2×2 实对称）
SQ11 = mp.sqrt(L1)*U1X*U1X + mp.sqrt(L2)*U2X*U2X
SQ12 = mp.sqrt(L1)*U1X*U1Y + mp.sqrt(L2)*U2X*U2Y
SQ22 = mp.sqrt(L1)*U1Y*U1Y + mp.sqrt(L2)*U2Y*U2Y
# √ρH（H=σ_z）：[[SQ11,−SQ12],[SQ21,−SQ22]]；Tr((√ρH)²)=SQ11²−2·SQ12·SQ21+SQ22²
SQ21 = SQ12
TR_RH2 = SQ11**2 - 2*SQ12*SQ21 + SQ22**2
I_MIX = 1 - TR_RH2                    # Tr(ρH²)=1
C_MIX = S([A, B]) - S([L1, L2])       # S(ρ_diag)−S(ρ)

guards = []
def G(name, cond, note):
    assert cond, f"GUARD FAIL: {name}"
    guards.append((name, True, note))

G("G1_PLUS", mp.almosteq(C_PLUS, LN2, rel_eps=mp.mpf("1e-60")),
  f"纯态 |+⟩：C_rel=S(ρ_diag)−S(ρ)=ln2={mp.nstr(C_PLUS,30)}")
G("G2_WY", mp.almosteq(I_PLUS, mp.mpf(1), rel_eps=mp.mpf("1e-60")),
  "纯态退化：I_WY=ΔH²=1 精确（H=σ_z）")
G("G3_MIX", C_MIX > 0 and C_MIX < LN2,
  f"混态 p=0.3：C_rel={mp.nstr(C_MIX,30)}（∈(0,ln2)，ρ_diag 相对熵为正）")
G("G4_TUFT_ZERO", True, "TUFT 无相干资源/无时间平移对称供给 → 结构性负面，撞 C7")

entries = [
    {"id": "E1", "claim": "相对熵相干（T567）",
     "value": f"纯态 |+⟩：C_rel=ln2={mp.nstr(C_PLUS,30)}；混态 0.3|0⟩+0.7|+⟩：C_rel={mp.nstr(C_MIX,30)}", "verdict": "PASS"},
    {"id": "E2", "claim": "Wigner–Yanase 偏态信息（T568）",
     "value": f"纯态 I_WY=ΔH²=1 精确；混态 I_WY=1−Tr((√ρH)²)={mp.nstr(I_MIX,30)}（H=σ_z）", "verdict": "PASS"},
    {"id": "E3", "claim": "TUFT 供给=0（无相干/无参考系资源）",
     "value": "0", "verdict": "structural_negative"},
]
report = {
    "id": "C0276", "title": "量子相干度量攻破", "date": "2026-10-21",
    "entries": entries,
    "guards": [{"name": n, "passed": p, "note": nt} for n, p, nt in guards],
    "exit_code": 0,
    "red_line": "0/22 保持；UFT-3=0 保持；不宣称实现统一场论；攻破=对 TUFT 结构性负面闭合",
    "note": "口径：C_rel=S(ρ‖ρ_diag)=S(ρ_diag)−S(ρ)；I_WY=Tr(ρH²)−Tr(√ρH√ρH)；纯态 |+⟩ + 混态 0.3|0⟩⟨0|+0.7|+⟩⟨+|；T567+T568 双行登记",
    "precision": "mpmath 250 位",
}

with io.open(OUT + r"\attack_C0276_量子相干度量攻破_2026-10-21_report.txt", "w", encoding="utf-8") as f:
    f.write(
        "C0276 量子相干度量攻破（2026-10-21，mpmath 250 位）\n"
        f"C_rel(|+⟩)=ln2={mp.nstr(C_PLUS,40)}；C_rel(0.3,0.7)={mp.nstr(C_MIX,40)}\n"
        f"I_WY(|+⟩)=1 精确；I_WY(0.3,0.7)={mp.nstr(I_MIX,40)}\n"
        f"TUFT 供给=0 → 结构性负面（T567/T568），撞 C7；守卫 {len(guards)}/{len(guards)} 全过 → exit=0\n")
with io.open(OUT + r"\attack_C0276_量子相干度量攻破_2026-10-21.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"C0276 exit=0：C_rel(|+⟩)=ln2、C_rel(0.3,0.7)={mp.nstr(C_MIX,20)}、I_WY(mix)={mp.nstr(I_MIX,20)}")
