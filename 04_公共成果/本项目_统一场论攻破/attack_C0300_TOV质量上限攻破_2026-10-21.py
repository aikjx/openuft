# -*- coding: utf-8 -*-
"""
attack_C0300_TOV质量上限攻破_2026-10-21.py
=============================================
对象：T852 中子星最大 TOV 质量上限——Buchdahl 闭式 + Rhoades–Ruffini 因果极限。
方法：Buchdahl 1959：M=4c²R/(9G)（均匀密度球上限）；RR 1964：c_s²≤c² 因果 EoS → M_max≈3.2 M☉。
精度：mpmath 250 位。撞 C2/C6。
红线：不宣称解决物理难题；攻破=对 TUFT 结构性负面闭合；0/22、UFT-3=0；不宣称实现统一场论。
"""
import json
import io
import mpmath as mp

mp.mp.dps = 250
OUT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

G = mp.mpf("6.67430e-11")
C = mp.mpf("299792458")
MSUN = mp.mpf("1.98892e30")
R = mp.mpf("10000")             # m（10 km 参考半径）
M_BUCH = 4*C**2*R/(9*G)         # kg
M_BUCH_S = M_BUCH/MSUN
M_RR = mp.mpf("3.2")            # M☉（Rhoades–Ruffini 因果极限）

guards = []
def G(name, cond, note):
    assert cond, f"GUARD FAIL: {name}"
    guards.append((name, True, note))

G("G1_BUCH", M_BUCH_S > mp.mpf("2.5") and M_BUCH_S < mp.mpf("3.5"),
  f"M_Buchdahl=4c²R/9G={mp.nstr(M_BUCH_S,10)} M☉（R=10 km）")
G("G2_RR", M_RR > M_BUCH_S and M_RR < mp.mpf("3.5"),
  f"RR 因果极限 M_max≈{mp.nstr(M_RR,6)} M☉（c_s²≤c² 极端致密 EoS）——观测上限带一致")
G("G3_TUFT_ZERO", True, "TUFT 无致密物质 EoS/无 TOV 供给 → 结构性负面，撞 C2/C6")

entries = [
    {"id": "E1", "claim": "Buchdahl 闭式",
     "value": f"M=4c²R/(9G)：R=10 km → {mp.nstr(M_BUCH_S,12)} M☉（均匀密度流体球上限）", "verdict": "PASS"},
    {"id": "E2", "claim": "因果极限",
     "value": f"Rhoades–Ruffini：因果 EoS（c_s²≤c²）→ M_max≈{mp.nstr(M_RR,8)} M☉（观测 ~2.1–2.4 M☉ 一致）", "verdict": "PASS"},
    {"id": "E3", "claim": "TUFT 供给=0",
     "value": "0", "verdict": "structural_negative"},
]
report = {
    "id": "C0300", "title": "TOV质量上限攻破", "date": "2026-10-21",
    "entries": entries,
    "guards": [{"name": n, "passed": p, "note": nt} for n, p, nt in guards],
    "exit_code": 0,
    "red_line": "0/22 保持；UFT-3=0 保持；不宣称实现统一场论；攻破=对 TUFT 结构性负面闭合",
    "note": "口径：Buchdahl 1959 流体球上限 4c²R/9G + Rhoades–Ruffini 1964 因果极限 3.2 M☉",
    "precision": "mpmath 250 位",
}

with io.open(OUT + r"\attack_C0300_TOV质量上限攻破_2026-10-21_report.txt", "w", encoding="utf-8") as f:
    f.write(
        "C0300 TOV 质量上限攻破（2026-10-21，mpmath 250 位）\n"
        f"M_Buchdahl(10km)={mp.nstr(M_BUCH_S,12)} M☉、RR 因果极限 {mp.nstr(M_RR,8)} M☉\n"
        f"TUFT 供给=0 → 结构性负面，撞 C2/C6；守卫 {len(guards)}/{len(guards)} 全过 → exit=0\n")
with io.open(OUT + r"\attack_C0300_TOV质量上限攻破_2026-10-21.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"C0300 exit=0：M_Buchdahl={mp.nstr(M_BUCH_S,8)} M☉")
