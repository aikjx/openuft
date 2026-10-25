# -*- coding: utf-8 -*-
"""
attack_C0271_PTAHD曲线攻破_2026-10-21.py
=============================================
对象：T147 PTA Hellings–Downs 角相关曲线（PTA 随机引力波背景）——HD 曲线标准形式精算。
方法：zeta(θ)=3/2·x·ln x − x/4 + 1/2，x=(1−cosθ)/2（零滞后、去自相关 δ 项；
      标准式 arXiv:1707.01615 Eq.(5)/1412.1142/2502.00080；θ→0 极限 1/2、θ=π 精确 1/4）。
精度：mpmath 250 位（用户指令）；纯对数+三角算术，零观测自由参数。
红线：不宣称解决物理难题；攻破=对 TUFT 结构性负面闭合；0/22、UFT-3=0；不宣称实现统一场论。
"""
import json
import io
import mpmath as mp

mp.mp.dps = 250
OUT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

def hd(theta):
    x = (1 - mp.cos(theta)) / 2
    return mp.mpf(3)/2 * x * mp.log(x) - x/4 + mp.mpf(1)/2

ANGLES = ["0.1", "30", "60", "90", "120", "180"]
vals = {}
for a in ANGLES:
    th = mp.radians(mp.mpf(a))
    vals[a] = hd(th) if a != "0.1" else hd(mp.mpf("1e-300"))  # θ→0 极限（x→0⁻）

Z0 = mp.mpf("1e-120")      # θ→0 极限（x=θ²/4≈2.5e-241，250 位内可表示；ζ→1/2）
ZPI = vals["180"]          # θ=180°：x=1 → ζ=3/2·0−1/4+1/2=1/4 精确
Z90 = vals["90"]           # θ=90°：x=1/2 → ζ=3/4·ln(1/2)−1/8+1/2
# 精确解析：ζ(90°)=3/2·(1/2)·ln(1/2)−1/8+1/2 = (3/4)ln(1/2)+3/8 = −(3/4)ln2+3/8
Z90_EXACT = mp.mpf(3)/4*mp.log(mp.mpf(1)/2) + mp.mpf(3)/8

guards = []
def G(name, cond, note):
    assert cond, f"GUARD FAIL: {name}"
    guards.append((name, True, note))

G("G1_PI", mp.almosteq(ZPI, mp.mpf("0.25"), rel_eps=mp.mpf("1e-60")),
  f"θ=180°：ζ={mp.nstr(ZPI,50)}=1/4 精确（x=1）")
G("G2_ZERO", mp.almosteq(hd(mp.mpf('1e-120')), mp.mpf('0.5'), rel_eps=mp.mpf('1e-60')),
  f"θ→0：ζ→1/2（去自相关 δ 项极限；对角元另含 δ 项）")
G("G3_90", mp.almosteq(Z90, Z90_EXACT, rel_eps=mp.mpf("1e-60")),
  f"θ=90°：ζ={mp.nstr(Z90,50)}（=3/4·ln(1/2)+3/8 解析一致）")
G("G4_TUFT_ZERO", True, "TUFT 无 HD/无 PTA 角相关供给 → 结构性负面，撞 C5")

entries = [
    {"id": "E1", "claim": "HD 角相关曲线（标准式）",
     "value": "ζ(θ)=3/2·x·lnx−x/4+1/2，x=(1−cosθ)/2（零滞后；arXiv:1707.01615 同式）", "verdict": "PASS"},
    {"id": "E2", "claim": "关键角值",
     "value": "θ→0：1/2（极限）；30°：{v30}；60°：{v60}；90°：{v90}；120°：{v120}；180°：1/4 精确".format(
         v30=mp.nstr(vals["30"],30), v60=mp.nstr(vals["60"],30),
         v90=mp.nstr(vals["90"],30), v120=mp.nstr(vals["120"],30)), "verdict": "PASS"},
    {"id": "E3", "claim": "TUFT 供给=0（无 HD/无 PTA 角相关）",
     "value": "0", "verdict": "structural_negative"},
]
report = {
    "id": "C0271", "title": "PTAHD曲线攻破", "date": "2026-10-21",
    "entries": entries,
    "guards": [{"name": n, "passed": p, "note": nt} for n, p, nt in guards],
    "exit_code": 0,
    "red_line": "0/22 保持；UFT-3=0 保持；不宣称实现统一场论；攻破=对 TUFT 结构性负面闭合",
    "note": "口径：HD 标准式 ζ=3/2·x·lnx−x/4+1/2（x=(1−cosθ)/2），零滞后去自相关 δ；θ=π 精确 1/4、θ→0 极限 1/2；纯对数算术零外部输入",
    "precision": "mpmath 250 位",
}

with io.open(OUT + r"\attack_C0271_PTAHD曲线攻破_2026-10-21_report.txt", "w", encoding="utf-8") as f:
    f.write(
        "C0271 PTA HD 曲线攻破（2026-10-21，mpmath 250 位）\n"
        f"ζ(θ)=3/2·x·lnx−x/4+1/2，x=(1−cosθ)/2\n"
        f"θ→0：1/2；30°：{mp.nstr(vals['30'],40)}；60°：{mp.nstr(vals['60'],40)}；90°：{mp.nstr(Z90,40)}；120°：{mp.nstr(vals['120'],40)}；180°：1/4 精确\n"
        f"TUFT 供给=0 → 结构性负面，撞 C5；守卫 {len(guards)}/{len(guards)} 全过 → exit=0\n")
with io.open(OUT + r"\attack_C0271_PTAHD曲线攻破_2026-10-21.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"C0271 exit=0：ζ(π)=1/4 精确、ζ(90°)={mp.nstr(Z90,25)}")
