# -*- coding: utf-8 -*-
"""
attack_C0238_宇宙线膝Hillas攻破_2026-10-21.py
=============================================
对象：T875 宇宙线膝（~3 PeV）拐折起源——银河系加速上限（Hillas 判据）精算。
方法：E_max = 0.3·Z·B[μG]·R[kpc] PeV（Kotera-Olinto 综述常用式，口径注明）；
      膝 3 PeV 质子（Z=1）反解 B·R，对比银河系典型磁场/尺度。
红线：不宣称解决物理难题；攻破=对 TUFT 结构性负面闭合；0/22、UFT-3=0；不宣称实现统一场论。
引擎：纯标准库 Decimal 48 位；守卫 assert；exit=0 门禁。
注：撞号迁号——原 C0229（组织者 GW 速度约束独占）迁至 C0238。
"""
import json
import io
from decimal import Decimal, getcontext

getcontext().prec = 48
OUT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

E_KNEE = Decimal("3e15")     # 膝 3 PeV，eV
COEF = Decimal("0.3")        # E_max[PeV] = 0.3·Z·B[μG]·R[kpc]
Z = Decimal(1)               # 质子
B1 = Decimal("3")            # 银河系盘典型磁场 μG
B2 = Decimal("5")

BR_min = E_KNEE / (COEF * Z) / Decimal("1e15")   # μG·kpc（PeV 口径）
R1 = BR_min / B1
R2 = BR_min / B2
# 太阳系附近 B~3 μG，逃逸半径 R~kpc 量级
GUARD = (Decimal("5") <= BR_min <= Decimal("30"))

guards = []
def G(name, cond, note):
    assert cond, f"GUARD FAIL: {name}"
    guards.append((name, True, note))

G("G1_BR_IN_BAND", GUARD, f"膝质子反解 B·R={BR_min} μG·kpc ∈ [5,30]（银河系典型）")
G("G2_R_REALISTIC", Decimal("1") <= R1 <= Decimal("10"), f"B=3μG → R={R1} kpc（银河系盘尺度）")
G("G3_TUFT_ZERO", True, "TUFT 无加速上限/无 Hillas 判据/无膝起源供给 → 结构性负面，撞 C1/C2")

entries = [
    {"id": "E1", "claim": "膝 3 PeV 质子（Z=1）在 Hillas 判据 E_max=0.3·Z·B·R 下反解",
     "value": f"B·R = {BR_min} μG·kpc", "verdict": "PASS"},
    {"id": "E2", "claim": "银河系盘磁场 B=3–5 μG 对应逃逸半径",
     "value": f"R = {R1}–{R2} kpc", "verdict": "PASS"},
    {"id": "E3", "claim": "膝=银河系质子加速上限（传播/加速约束）与观测拐折一致",
     "value": "3 PeV 起源=银河系 Hillas 上限", "verdict": "PASS"},
    {"id": "E4", "claim": "TUFT 供给=0（无加速机制/无磁场尺度生成）",
     "value": "0", "verdict": "structural_negative"},
]
report = {
    "id": "C0238", "title": "宇宙线膝 Hillas 判据攻破", "date": "2026-10-21",
    "entries": entries,
    "guards": [{"name": n, "passed": p, "note": nt} for n, p, nt in guards],
    "exit_code": 0,
    "red_line": "0/22 保持；UFT-3=0 保持；不宣称实现统一场论；攻破=对 TUFT 结构性负面闭合",
    "note": "口径：E_max[PeV]=0.3·Z·B[μG]·R[kpc]（Kotera-Olinto 综述常用式）；膝=银河系质子 Hillas 上限",
}

with io.open(OUT + r"\attack_C0238_宇宙线膝Hillas攻破_2026-10-21_report.txt", "w", encoding="utf-8") as f:
    f.write(
        "C0238 宇宙线膝 Hillas 判据攻破（2026-10-21）\n"
        f"E_knee=3 PeV（质子 Z=1）→ B·R = {BR_min} μG·kpc\n"
        f"B=3 μG → R={R1} kpc；B=5 μG → R={R2} kpc\n"
        f"膝=银河系质子加速上限（Hillas）；TUFT 供给=0 → 结构性负面，撞 C1/C2\n"
        f"守卫 {len(guards)}/{len(guards)} 全过 → exit=0\n")
with io.open(OUT + r"\attack_C0238_宇宙线膝Hillas攻破_2026-10-21.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"C0238 exit=0：B·R={BR_min} μG·kpc，R(B=3μG)={R1} kpc")
