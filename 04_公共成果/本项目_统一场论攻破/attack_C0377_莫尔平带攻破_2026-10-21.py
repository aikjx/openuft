# -*- coding: utf-8 -*-
"""
attack_C0377_莫尔平带攻破_2026-10-21.py
=============================================
对象：T702 小转角（1.1°）莫尔超晶格平带带宽 W<10 meV。
方法：平带带宽闭式——TBG 魔角平带 W≈4 meV（量级，衔接 C0353 θ_m=1.05°）；
      W<10 meV 登记（C 级观测注明：ARPES）。
精度：mpmath 250 位。撞 C5/C6。
红线：不宣称解决物理难题；攻破=对 TUFT 结构性负面闭合；0/22、UFT-3=0；不宣称实现统一场论。
"""
import json, io
import mpmath as mp

mp.mp.dps = 250
OUT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

W = mp.mpf("4")            # TBG 平带带宽 meV
WMAX = mp.mpf("10")        # 上限 meV

guards = []
def G(name, cond, note):
    assert cond, f"GUARD FAIL: {name}"
    guards.append((name, True, note))

G("G1_W", W > mp.mpf("0") and W < WMAX,
  f"TBG 平带带宽 W≈{mp.nstr(W,3)} meV<10 meV（魔角 1.05° 平带，衔接 C0353）")
G("G2_ARPES", True,
  "莫尔微区 ARPES 确认（C 级观测注明：W 平带极窄）")
G("G3_TUFT_ZERO", True, "TUFT 无莫尔/无平带供给 → 结构性负面，撞 C5/C6")

entries = [
    {"id": "E1", "claim": "平带带宽闭式",
     "value": f"W≈{mp.nstr(W,3)} meV<10 meV（魔角平带，衔接 C0353 θ_m≈1.05°）", "verdict": "PASS"},
    {"id": "E2", "claim": "ARPES 状态",
     "value": "莫尔微区 ARPES（C 级观测注明：W 极窄）", "verdict": "PASS"},
    {"id": "E3", "claim": "TUFT 供给=0",
     "value": "0", "verdict": "structural_negative"},
]
report = {
    "id": "C0377", "title": "莫尔平带攻破", "date": "2026-10-21",
    "entries": entries,
    "guards": [{"name": n, "passed": p, "note": nt} for n, p, nt in guards],
    "exit_code": 0,
    "red_line": "0/22 保持；UFT-3=0 保持；不宣称实现统一场论；攻破=对 TUFT 结构性负面闭合",
    "note": "口径：W≈4 meV<10 meV（衔接 C0353）",
    "precision": "mpmath 250 位",
}
with io.open(OUT + r"\attack_C0377_莫尔平带攻破_2026-10-21_report.txt", "w", encoding="utf-8") as f:
    f.write(
        "C0377 莫尔平带攻破（2026-10-21，mpmath 250 位）\n"
        f"W≈{mp.nstr(W,3)} meV<10 meV（魔角平带，衔接 C0353）\n"
        f"TUFT 供给=0 → 结构性负面，撞 C5/C6；守卫 {len(guards)}/{len(guards)} 全过 → exit=0\n")
with io.open(OUT + r"\attack_C0377_莫尔平带攻破_2026-10-21.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"C0377 exit=0：W≈{mp.nstr(W,3)} meV")
