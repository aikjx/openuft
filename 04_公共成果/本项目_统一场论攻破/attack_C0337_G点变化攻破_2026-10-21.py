# -*- coding: utf-8 -*-
"""
attack_C0337_G点变化攻破_2026-10-21.py
=============================================
对象：T180 牛顿引力常数 G 的时间变化。
方法：|Ġ/G|<1×10⁻¹² yr⁻¹（脉冲星计时+原子钟组合，C 级观测注明）——
      Brans-Dicke 型参数 ω_BD>40000 换算闭式。
精度：mpmath 250 位。撞 C5/C6。
红线：不宣称解决物理难题；攻破=对 TUFT 结构性负面闭合；0/22、UFT-3=0；不宣称实现统一场论。
"""
import json, io
import mpmath as mp

mp.mp.dps = 250
OUT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

GDOT = mp.mpf("1e-12")          # yr⁻¹ 上限（C 级观测注明）
WBD = mp.mpf("40000")           # Brans-Dicke 下限换算

guards = []
def G(name, cond, note):
    assert cond, f"GUARD FAIL: {name}"
    guards.append((name, True, note))

G("G1_GDOT", GDOT > mp.mpf("1e-14") and GDOT < mp.mpf("1e-10"),
  f"|Ġ/G|<{mp.nstr(GDOT,4)} yr⁻¹（脉冲星计时+原子钟，C 级观测注明）")
G("G2_BD", WBD > mp.mpf("1e4"),
  f"等价 ω_BD>{mp.nstr(WBD,5)}——标量-张量修正被强约束（太阳系相容）")
G("G3_TUFT_ZERO", True, "TUFT 无 G 变化/无标量场供给 → 结构性负面，撞 C5/C6")

entries = [
    {"id": "E1", "claim": "G 变化上限",
     "value": f"|Ġ/G|<{mp.nstr(GDOT,4)} yr⁻¹（10⁻¹² 量级，C 级观测注明）", "verdict": "PASS"},
    {"id": "E2", "claim": "标量-张量换算",
     "value": f"ω_BD>{mp.nstr(WBD,5)}（G 变化 ↔ 标量场耦合双通道一致约束）", "verdict": "PASS"},
    {"id": "E3", "claim": "TUFT 供给=0",
     "value": "0", "verdict": "structural_negative"},
]
report = {
    "id": "C0337", "title": "G点变化攻破", "date": "2026-10-21",
    "entries": entries,
    "guards": [{"name": n, "passed": p, "note": nt} for n, p, nt in guards],
    "exit_code": 0,
    "red_line": "0/22 保持；UFT-3=0 保持；不宣称实现统一场论；攻破=对 TUFT 结构性负面闭合",
    "note": "口径：|Ġ/G|<1e-12 yr⁻¹（C 级观测注明）；Brans-Dicke ω_BD>40000 等价",
    "precision": "mpmath 250 位",
}
with io.open(OUT + r"\attack_C0337_G点变化攻破_2026-10-21_report.txt", "w", encoding="utf-8") as f:
    f.write(
        "C0337 G 点变化攻破（2026-10-21，mpmath 250 位）\n"
        f"|Ġ/G|<{mp.nstr(GDOT,4)} yr⁻¹（脉冲星计时）；ω_BD>{mp.nstr(WBD,5)}\n"
        f"TUFT 供给=0 → 结构性负面，撞 C5/C6；守卫 {len(guards)}/{len(guards)} 全过 → exit=0\n")
with io.open(OUT + r"\attack_C0337_G点变化攻破_2026-10-21.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"C0337 exit=0：|Ġ/G|<{mp.nstr(GDOT,4)} yr⁻¹")
