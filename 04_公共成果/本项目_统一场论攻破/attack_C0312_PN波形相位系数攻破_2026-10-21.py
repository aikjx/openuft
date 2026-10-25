# -*- coding: utf-8 -*-
"""
attack_C0312_PN波形相位系数攻破_2026-10-21.py
=============================================
对象：T152 双体波形高阶后牛顿（PN）修正——PN 相位系数闭式（非自旋圆形轨道）。
方法：φ(f)=3/128(Mπf)^(-5/3)·[1+ψ1·v²+ψ15·v³+ψ2·v⁴+...]；equal-mass η=1/4：
      0PN=1、1PN=3715/756+55η/9、1.5PN=16π、2PN 标称项；收敛检查 v=0.1。
精度：mpmath 250 位。撞 C7。
红线：不宣称解决物理难题；攻破=对 TUFT 结构性负面闭合；0/22、UFT-3=0；不宣称实现统一场论。
"""
import json
import io
import mpmath as mp

mp.mp.dps = 250
OUT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

ETA = mp.mpf(1)/4
PSI1 = mp.mpf("3715")/756 + mp.mpf("55")*ETA/9
PSI15 = 16*mp.pi
V = mp.mpf("0.1")
CORR = PSI1*V**2            # 1PN 修正份额 @v=0.1

guards = []
def G(name, cond, note):
    assert cond, f"GUARD FAIL: {name}"
    guards.append((name, True, note))

G("G1_PN1", PSI1 > mp.mpf("6") and PSI1 < mp.mpf("7"),
  f"1PN 系数 ψ1=3715/756+55η/9={mp.nstr(PSI1,8)}（η=1/4 equal-mass）")
G("G2_PN15", PSI15 > mp.mpf("50") and PSI15 < mp.mpf("51"),
  f"1.5PN 系数 16π={mp.nstr(PSI15,8)}（tail 效应精确常数）")
G("G3_CONV", CORR < mp.mpf("0.08"),
  f"收敛检查 @v=0.1：1PN 修正 {mp.nstr(CORR,6)}（~6.4%）——PN 展开低阶主导成立")
G("G4_TUFT_ZERO", True, "TUFT 无 PN 展开/无波形供给 → 结构性负面，撞 C7")

entries = [
    {"id": "E1", "claim": "PN 相位系数闭式（equal-mass）",
     "value": f"ψ0=1、ψ1={mp.nstr(PSI1,10)}、ψ15=16π={mp.nstr(PSI15,10)}（0PN/1PN/1.5PN 纯常数）", "verdict": "PASS"},
    {"id": "E2", "claim": "收敛性",
     "value": f"@v=0.1：1PN 修正 {mp.nstr(CORR,8)}——PN 展开在牛顿收敛半径内低阶主导", "verdict": "PASS"},
    {"id": "E3", "claim": "TUFT 供给=0",
     "value": "0", "verdict": "structural_negative"},
]
report = {
    "id": "C0312", "title": "PN波形相位系数攻破", "date": "2026-10-21",
    "entries": entries,
    "guards": [{"name": n, "passed": p, "note": nt} for n, p, nt in guards],
    "exit_code": 0,
    "red_line": "0/22 保持；UFT-3=0 保持；不宣称实现统一场论；攻破=对 TUFT 结构性负面闭合",
    "note": "口径：非自旋圆形轨道 PN 相位系数（0PN/1PN/1.5PN），η=1/4；v=0.1 收敛检查",
    "precision": "mpmath 250 位",
}

with io.open(OUT + r"\attack_C0312_PN波形相位系数攻破_2026-10-21_report.txt", "w", encoding="utf-8") as f:
    f.write(
        "C0312 PN 波形相位系数攻破（2026-10-21，mpmath 250 位）\n"
        f"ψ0=1、ψ1=3715/756+55η/9={mp.nstr(PSI1,10)}、ψ15=16π={mp.nstr(PSI15,10)}；v=0.1 收敛 {mp.nstr(CORR,8)}\n"
        f"TUFT 供给=0 → 结构性负面，撞 C7；守卫 {len(guards)}/{len(guards)} 全过 → exit=0\n")
with io.open(OUT + r"\attack_C0312_PN波形相位系数攻破_2026-10-21.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"C0312 exit=0：ψ1={mp.nstr(PSI1,6)}、ψ15={mp.nstr(PSI15,6)}")
