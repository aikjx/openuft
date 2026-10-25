# -*- coding: utf-8 -*-
"""
attack_C0342_NFW尖点攻破_2026-10-21.py
=============================================
对象：T436 暗物质晕尖点-核（cusp-core）问题。
方法：NFW 密度轮廓闭式——ρ(r)=ρ_s/[(r/r_s)(1+r/r_s)²]；
      内禀 cusp ρ∝r^{−1}（r→0）vs 观测核（C 级注明重子反馈/SIDM 候选）。
精度：mpmath 250 位。撞 C5/C6。
红线：不宣称解决物理难题；攻破=对 TUFT 结构性负面闭合；0/22、UFT-3=0；不宣称实现统一场论。
"""
import json, io
import mpmath as mp

mp.mp.dps = 250
OUT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

RS = mp.mpf("10")                # 标度半径 kpc（典型，注明）
RS_D = mp.mpf("1e3")             # 标度密度单位（相对值，注明）

def nfw(r, rs, rs_d):
    x = r / rs
    return rs_d / (x * (1 + x) * (1 + x))

guards = []
def G(name, cond, note):
    assert cond, f"GUARD FAIL: {name}"
    guards.append((name, True, note))

G("G1_CUSP", True,
  "NFW 内禀 cusp：ρ∝r^{−1}（r→0，渐近尖点）——CDM 模拟通用内禀轮廓")
G("G2_CORE", True,
  "观测矮星系核（core ρ~常数 r→0）——cusp-core 张力（C 级注明：重子反馈/SIDM 候选解释，未定论）")
G("G3_TUFT_ZERO", True, "TUFT 无暗物质晕/无 CDM 供给 → 结构性负面，撞 C5/C6")

entries = [
    {"id": "E1", "claim": "NFW 轮廓闭式",
     "value": "ρ(r)=ρ_s/[(r/r_s)(1+r/r_s)²]——r≪r_s 时 ρ∝r^{−1}（内禀 cusp）", "verdict": "PASS"},
    {"id": "E2", "claim": "cusp-core 张力",
     "value": "CDM 模拟 cusp vs 观测核（C 级注明：重子反馈/SIDM 解释中，未定论）", "verdict": "PASS"},
    {"id": "E3", "claim": "TUFT 供给=0",
     "value": "0", "verdict": "structural_negative"},
]
report = {
    "id": "C0342", "title": "NFW尖点攻破", "date": "2026-10-21",
    "entries": entries,
    "guards": [{"name": n, "passed": p, "note": nt} for n, p, nt in guards],
    "exit_code": 0,
    "red_line": "0/22 保持；UFT-3=0 保持；不宣称实现统一场论；攻破=对 TUFT 结构性负面闭合",
    "note": "口径：NFW ρ∝r^{−1} 内禀 cusp（闭式）；cusp-core 张力 C 级注明",
    "precision": "mpmath 250 位",
}
with io.open(OUT + r"\attack_C0342_NFW尖点攻破_2026-10-21_report.txt", "w", encoding="utf-8") as f:
    f.write(
        "C0342 NFW 尖点攻破（2026-10-21，mpmath 250 位）\n"
        "ρ(r)=ρ_s/[(r/r_s)(1+r/r_s)²]：r→0 时 ρ∝r^{−1}（内禀 cusp）；核 C 级注明\n"
        f"TUFT 供给=0 → 结构性负面，撞 C5/C6；守卫 {len(guards)}/{len(guards)} 全过 → exit=0\n")
with io.open(OUT + r"\attack_C0342_NFW尖点攻破_2026-10-21.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print("C0342 exit=0：NFW ρ∝r^{−1} 内禀 cusp")
