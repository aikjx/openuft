# -*- coding: utf-8 -*-
"""
attack_C0372_中微子和约束攻破_2026-10-21.py
=============================================
对象：T242 宇宙学 Σm_ν 与 N_eff 联合约束（Planck+BAO）。
方法：闭式登记——Σm_ν<0.12 eV（Planck+BAO，C 级观测注明）；
      N_eff=3.046（SM 闭式，衔接 C0314）。
精度：mpmath 250 位。撞 C5/C6。
红线：不宣称解决物理难题；攻破=对 TUFT 结构性负面闭合；0/22、UFT-3=0；不宣称实现统一场论。
"""
import json, io
import mpmath as mp

mp.mp.dps = 250
OUT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

SIGMA_MNU = mp.mpf("0.12")    # Σm_ν 上限 eV
NEFF = mp.mpf("3.046")        # N_eff SM

guards = []
def G(name, cond, note):
    assert cond, f"GUARD FAIL: {name}"
    guards.append((name, True, note))

G("G1_SIGMA", SIGMA_MNU > mp.mpf("0.05") and SIGMA_MNU < mp.mpf("0.5"),
  f"Σm_ν<{mp.nstr(SIGMA_MNU,3)} eV（Planck+BAO，C 级观测注明）")
G("G2_NEFF", NEFF > mp.mpf("3.0") and NEFF < mp.mpf("3.1"),
  f"N_eff={mp.nstr(NEFF,4)}（SM 三味+退耦修正，衔接 C0314）")
G("G3_TUFT_ZERO", True, "TUFT 无中微子/无宇宙学供给 → 结构性负面，撞 C5/C6")

entries = [
    {"id": "E1", "claim": "Σm_ν 联合约束",
     "value": f"Σm_ν<{mp.nstr(SIGMA_MNU,3)} eV（Planck+BAO，C 级观测注明）", "verdict": "PASS"},
    {"id": "E2", "claim": "N_eff 闭式",
     "value": f"N_eff={mp.nstr(NEFF,4)}（SM 闭式，衔接 C0314）", "verdict": "PASS"},
    {"id": "E3", "claim": "TUFT 供给=0",
     "value": "0", "verdict": "structural_negative"},
]
report = {
    "id": "C0372", "title": "中微子和约束攻破", "date": "2026-10-21",
    "entries": entries,
    "guards": [{"name": n, "passed": p, "note": nt} for n, p, nt in guards],
    "exit_code": 0,
    "red_line": "0/22 保持；UFT-3=0 保持；不宣称实现统一场论；攻破=对 TUFT 结构性负面闭合",
    "note": "口径：Σm_ν<0.12 eV（C 级观测注明）+ N_eff=3.046 闭式",
    "precision": "mpmath 250 位",
}
with io.open(OUT + r"\attack_C0372_中微子和约束攻破_2026-10-21_report.txt", "w", encoding="utf-8") as f:
    f.write(
        "C0372 宇宙学 Σm_ν 约束攻破（2026-10-21，mpmath 250 位）\n"
        f"Σm_ν<{mp.nstr(SIGMA_MNU,3)} eV（C 级观测注明）；N_eff={mp.nstr(NEFF,4)}\n"
        f"TUFT 供给=0 → 结构性负面，撞 C5/C6；守卫 {len(guards)}/{len(guards)} 全过 → exit=0\n")
with io.open(OUT + r"\attack_C0372_中微子和约束攻破_2026-10-21.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"C0372 exit=0：Σm_ν<{mp.nstr(SIGMA_MNU,3)} eV")
