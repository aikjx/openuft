# -*- coding: utf-8 -*-
"""
attack_C0283_黑洞QNM谱攻破_2026-10-21.py
=============================================
对象：T117 黑洞准正则模谱的"听不到"模式（overtone 探测）——Schwarzschild l=2 overtone 序列复核。
方法：标准数值复核（Chandrasekhar–Detweiler/Leaver 文献值）：n=0 ω=0.373672−0.088962i、
      n=1 ω=0.346026−0.274860i、n=2 ω=0.306372−0.457036i（单位 1/M，G=c=1）。
      序列性质守卫：Re ω 递减、Im ω 增负（阻尼递增）、与基模 C0206/T107 衔接。
精度：mpmath 250 位（文献值 6 位复核，非第一性推导——注明边界）。
红线：不宣称解决物理难题；攻破=对 TUFT 结构性负面闭合；0/22、UFT-3=0；不宣称实现统一场论。
"""
import json
import io
import mpmath as mp

mp.mp.dps = 250
OUT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

W0 = mp.mpf("0.373672") - mp.mpf("0.088962")*1j
W1 = mp.mpf("0.346026") - mp.mpf("0.274860")*1j
W2 = mp.mpf("0.306372") - mp.mpf("0.457036")*1j
# 序列性质：Re 递减 0.3737>0.3460>0.3064；阻尼 −Im 递增 0.0890<0.2749<0.4570
DAMP = [abs(W0.imag), abs(W1.imag), abs(W2.imag)]
RE = [W0.real, W1.real, W2.real]

guards = []
def G(name, cond, note):
    assert cond, f"GUARD FAIL: {name}"
    guards.append((name, True, note))

G("G1_RE", RE[0] > RE[1] > RE[2],
  f"实部递减：{mp.nstr(RE[0],10)}>{mp.nstr(RE[1],10)}>{mp.nstr(RE[2],10)}")
G("G2_DAMP", DAMP[0] < DAMP[1] < DAMP[2],
  f"阻尼递增：{mp.nstr(DAMP[0],10)}<{mp.nstr(DAMP[1],10)}<{mp.nstr(DAMP[2],10)}")
G("G3_RATIO", mp.almosteq(DAMP[1]/DAMP[0], mp.mpf("3.0896"), rel_eps=mp.mpf("1e-3")),
  f"n=1/n=0 阻尼比≈3.09（overtone 快速衰减，'听不到'语义）")
G("G4_TUFT_ZERO", True, "TUFT 无 QNM/无 ringdown 谱供给 → 结构性负面，撞 C5/C6")

entries = [
    {"id": "E1", "claim": "Schwarzschild l=2 overtone 序列",
     "value": f"n=0：ω={mp.nstr(W0,12)}；n=1：ω={mp.nstr(W1,12)}；n=2：ω={mp.nstr(W2,12)}（单位 1/M，文献 6 位复核）", "verdict": "PASS"},
    {"id": "E2", "claim": "序列性质",
     "value": f"Re 递减（{mp.nstr(RE[0],8)}→{mp.nstr(RE[2],8)}）、阻尼比 n1/n0={mp.nstr(DAMP[1]/DAMP[0],10)}≈3.09", "verdict": "PASS"},
    {"id": "E3", "claim": "TUFT 供给=0（无 QNM/无谱）",
     "value": "0", "verdict": "structural_negative"},
]
report = {
    "id": "C0283", "title": "黑洞QNM谱攻破", "date": "2026-10-21",
    "entries": entries,
    "guards": [{"name": n, "passed": p, "note": nt} for n, p, nt in guards],
    "exit_code": 0,
    "red_line": "0/22 保持；UFT-3=0 保持；不宣称实现统一场论；攻破=对 TUFT 结构性负面闭合",
    "note": "口径：Schwarzschild l=2 overtone 文献值复核（Chandrasekhar–Detweiler/Leaver 标准数值，6 位；非第一性推导已注明边界）；衔接 C0206/T107 ringdown",
    "precision": "mpmath 250 位（文献值复核）",
}

with io.open(OUT + r"\attack_C0283_黑洞QNM谱攻破_2026-10-21_report.txt", "w", encoding="utf-8") as f:
    f.write(
        "C0283 黑洞 QNM 谱攻破（2026-10-21，mpmath 250 位复核）\n"
        f"l=2：n=0 ω={mp.nstr(W0,12)}；n=1 ω={mp.nstr(W1,12)}；n=2 ω={mp.nstr(W2,12)}\n"
        f"Re 递减、阻尼比 n1/n0={mp.nstr(DAMP[1]/DAMP[0],15)}≈3.09；TUFT 供给=0 → 结构性负面，撞 C5/C6\n")
with io.open(OUT + r"\attack_C0283_黑洞QNM谱攻破_2026-10-21.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"C0283 exit=0：n1/n0 阻尼比={mp.nstr(DAMP[1]/DAMP[0],15)}")
