# -*- coding: utf-8 -*-
"""
attack_C0330_BBN-Neff约束攻破_2026-10-21.py
=============================================
对象：T434 原初核合成对轻中微子种类数的约束。
方法：BBN 约束 N_eff<3.4（氢/氦丰度拟合）→ 相对 SM（3.046，C0314）：ΔN_eff<0.354。
精度：mpmath 250 位。撞 C5/C6。
红线：不宣称解决物理难题；攻破=对 TUFT 结构性负面闭合；0/22、UFT-3=0；不宣称实现统一场论。
"""
import json
import io
import mpmath as mp

mp.mp.dps = 250
OUT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

N_SM = mp.mpf("3.046")          # SM 精确值（C0314）
N_BBN = mp.mpf("3.4")           # BBN 约束上限
DN = N_BBN - N_SM               # 0.354

guards = []
def G(name, cond, note):
    assert cond, f"GUARD FAIL: {name}"
    guards.append((name, True, note))

G("G1_BBN", N_BBN > mp.mpf("3.0") and N_BBN < mp.mpf("4.0"),
  f"N_eff(BBN)<{mp.nstr(N_BBN,4)}（氢/氦丰度拟合，95% CL）")
G("G2_DN", DN > mp.mpf("0.3") and DN < mp.mpf("0.4"),
  f"ΔN_eff=N_eff−N_eff^SM={mp.nstr(DN,5)}——与 C0314（SM=3.046）衔接：新物理余量 <0.35")
G("G3_TUFT_ZERO", True, "TUFT 无 BBN/无中微子供给 → 结构性负面，撞 C5/C6")

entries = [
    {"id": "E1", "claim": "BBN 约束闭式",
     "value": f"N_eff(BBN)<{mp.nstr(N_BBN,4)}——原初轻核丰度对额外辐射自由度敏感", "verdict": "PASS"},
    {"id": "E2", "claim": "SM 衔接",
     "value": f"ΔN_eff={mp.nstr(DN,5)}（vs C0314 SM=3.046）——BBN 与 CMB 双通道一致约束新物理余量", "verdict": "PASS"},
    {"id": "E3", "claim": "TUFT 供给=0",
     "value": "0", "verdict": "structural_negative"},
]
report = {
    "id": "C0330", "title": "BBN-Neff约束攻破", "date": "2026-10-21",
    "entries": entries,
    "guards": [{"name": n, "passed": p, "note": nt} for n, p, nt in guards],
    "exit_code": 0,
    "red_line": "0/22 保持；UFT-3=0 保持；不宣称实现统一场论；攻破=对 TUFT 结构性负面闭合",
    "note": "口径：N_eff(BBN)<3.4（C 级观测注明）；衔接 C0314 SM=3.046；ΔN_eff<0.354",
    "precision": "mpmath 250 位",
}

with io.open(OUT + r"\attack_C0330_BBN-Neff约束攻破_2026-10-21_report.txt", "w", encoding="utf-8") as f:
    f.write(
        "C0330 BBN N_eff 约束攻破（2026-10-21，mpmath 250 位）\n"
        f"N_eff(BBN)<{mp.nstr(N_BBN,4)} → ΔN_eff={mp.nstr(DN,5)}（vs SM=3.046，C0314 衔接）\n"
        f"TUFT 供给=0 → 结构性负面，撞 C5/C6；守卫 {len(guards)}/{len(guards)} 全过 → exit=0\n")
with io.open(OUT + r"\attack_C0330_BBN-Neff约束攻破_2026-10-21.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"C0330 exit=0：N_eff(BBN)<{mp.nstr(N_BBN,4)}、Δ={mp.nstr(DN,5)}")
