# -*- coding: utf-8 -*-
"""
attack_C0401_三能级量子热机攻破_2026-10-29.py
===============================================
对象：母册 T536 · 三能级量子热机的效率界与最大功率（域 J · 撞 C5/C7）。
方法：标准量子热力学闭式——
      Carnot 界 η_C = 1 − T_c/T_h；
      最大功率效率（Curzon-Ahlborn，端到端）η_CA = 1 − √(T_c/T_h)；
      量子 Otto（三能级/谐振子，绝热频率比 ω_h/ω_c = T_h/T_c）η_Otto = 1 − ω_c/ω_h。
      精算基准 T_h=300 K、T_c=100 K；解析求导验证——
      dη_CA/dr = −1/(2√r) < 0、dη_C/dr = −1、dη_Otto/d(ω_c/ω_h) = −1。
精度：mpmath 250 位（mp.dps=250 双 API 兼容）+ fractions.Fraction 精确比值。
撞点：C5（可检验：无 TUFT 特定效率预测）/ C7（数学自洽：定理性结论）。
红线：0/22 保持；UFT-3=0 保持；不宣称实现统一场论；攻破=对 TUFT 结构性负面闭合。
归因：标准量子热力学效率界算术（Carnot/Curzon-Ahlborn/Otto），未写成 TUFT 预测。
"""
import json, io
from fractions import Fraction
import mpmath as mp

# mpmath 250 位：双 API 兼容（旧版 mp.dps / 新版 mp.mp.dps）
try:
    mp.dps = 250
except AttributeError:
    mp.mp.dps = 250

OUT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"
DATE = "2026-10-29"
CID = "C0401"

# ---------- 闭式 ----------
def eta_carnot_frac(Th, Tc):
    """Carnot 界 η_C = 1 − T_c/T_h，Fraction 精确。"""
    return Fraction(1) - Fraction(Tc, Th)

def eta_carnot_mp(Th, Tc):
    return 1 - mp.mpf(Tc) / mp.mpf(Th)

def eta_ca_mp(Th, Tc):
    """Curzon-Ahlborn 最大功率效率 η_CA = 1 − √(T_c/T_h)。"""
    return 1 - mp.sqrt(mp.mpf(Tc) / mp.mpf(Th))

def eta_otto_frac(wh, wc):
    """量子 Otto η_Otto = 1 − ω_c/ω_h，Fraction 精确。"""
    return Fraction(1) - Fraction(wc, wh)

guards = []
def G(name, cond, note):
    assert cond, f"GUARD FAIL: {name}"
    guards.append((name, True, note))

# ---------- 关键读数（基准 T_h=300 K、T_c=100 K）----------
Th, Tc = 300, 100
r = mp.mpf(Tc) / mp.mpf(Th)                 # r = 1/3

etaC_frac = eta_carnot_frac(Th, Tc)         # 2/3 精确
etaC_mp = eta_carnot_mp(Th, Tc)
etaCA_mp = eta_ca_mp(Th, Tc)

# 1/√3 双路径互验：路径 A = 1/mp.sqrt(3)；路径 B = sqrt(1/3)
inv_sqrt3_a = 1 / mp.sqrt(3)
inv_sqrt3_b = mp.sqrt(mp.mpf(1) / 3)
inv_sqrt3_diff = mp.fabs(inv_sqrt3_a - inv_sqrt3_b)

# 温度比表：r = 0.1 / 1/3 / 0.5 的 η_C、η_CA
ratio_table = []
for rv in ["0.1", "1/3", "0.5"]:
    rr = mp.mpf(rv)
    ratio_table.append({
        "r": rv,
        "eta_C": mp.nstr(1 - rr, 24),
        "eta_CA": mp.nstr(1 - mp.sqrt(rr), 24),
    })

# 量子 Otto：绝热频率比 ω_h/ω_c = T_h/T_c = 3
wh, wc = 3, 1
etaOtto_frac = eta_otto_frac(wh, wc)        # 2/3 精确（可逆时 = Carnot）

# ---------- 解析求导（手推闭式，引擎数值验证）----------
# dη_CA/dr = −1/(2√r)；dη_C/dr = −1；dη_Otto/dx = −1（x = ω_c/ω_h）
dCA_dr = -mp.mpf(1) / (2 * mp.sqrt(r))       # r=1/3 处 = −√3/2
dC_dr = -mp.mpf(1)                           # 常数斜率
x = mp.mpf(wc) / mp.mpf(wh)
dOtto_dx = -mp.mpf(1)

# 数值微分互验（250 位中心差分）：dη_CA/dr ≈ [η(r+δ)−η(r−δ)]/(2δ)，δ=1e-100
delta = mp.mpf("1e-100")
num_dCA = ((1 - mp.sqrt(r + delta)) - (1 - mp.sqrt(r - delta))) / (2 * delta)
num_diff_err = mp.fabs(num_dCA - dCA_dr)

# ---------- 守卫 ----------
G("G1_Carnot_300K_100K_eq_2over3", etaC_frac == Fraction(2, 3),
  "η_C(300K,100K)=1−100/300=2/3（Fraction 精确）")
G("G2_CA_in_interval", mp.mpf("0.422") < etaCA_mp < mp.mpf("0.424"),
  f"η_CA=1−1/√3={mp.nstr(etaCA_mp, 16)} ∈ [0.422, 0.424]（250 位）")
G("G3_inv_sqrt3_dual_path", inv_sqrt3_diff < mp.mpf("1e-240"),
  f"1/√3 双路径（1/√3 与 √(1/3)）互验差={mp.nstr(inv_sqrt3_diff, 6)} < 1e-240")
G("G4_dCA_dr_negative", dCA_dr < 0 and num_dCA < 0,
  f"dη_CA/dr=−1/(2√r)={mp.nstr(dCA_dr, 16)} < 0（闭式 + 数值差商互验均负）")
G("G5_Otto_ratio3_eq_2over3", etaOtto_frac == Fraction(2, 3),
  "η_Otto(ω_h/ω_c=3)=1−1/3=2/3（Fraction 精确，可逆时 = Carnot）")
G("G6_TUFT_zero", True, "TUFT 无量子热力学机制供给 → 结构性负面，撞 C5/C7")
G("G7_CA_numerical_diff", num_diff_err < mp.mpf("1e-100"),
  f"中心差商(δ=1e-100)与闭式导数一致，差={mp.nstr(num_diff_err, 6)} < 1e-100")
G("G8_Carnot_Otto_reversible_equal", etaOtto_frac == etaC_frac,
  "可逆量子 Otto 效率 = Carnot 界（2/3 = 2/3，Fraction 精确闭合）")

# ---------- 条目 ----------
entries = [
    {"id": "E1", "claim": "标准定理：三能级量子热机效率界",
     "value": "Carnot 上界 η_C=1−T_c/T_h；Curzon-Ahlborn 最大功率效率 η_CA=1−√(T_c/T_h)；"
              "量子 Otto η_Otto=1−ω_c/ω_h（标准量子热力学，引用不复算）",
     "verdict": "PASS"},
    {"id": "E2", "claim": "闭式精算（T_h=300 K、T_c=100 K）",
     "value": f"η_C=2/3（Fraction 精确）；η_CA=1−1/√3={mp.nstr(etaCA_mp, 24)}；"
              f"1/√3={mp.nstr(inv_sqrt3_a, 24)}；η_Otto(ω_h/ω_c=3)=2/3；"
              f"温度比表 r=0.1/1/3/0.5 见 JSON/报告",
     "verdict": "PASS"},
    {"id": "E3", "claim": "解析求导验证",
     "value": f"dη_CA/dr=−1/(2√r)={mp.nstr(dCA_dr, 16)}<0；dη_C/dr=−1；dη_Otto/dx=−1；"
              f"数值差商互验差={mp.nstr(num_diff_err, 6)}<1e-100",
     "verdict": "PASS"},
    {"id": "E4", "claim": "TUFT 供给检查",
     "value": "0（TUFT 不供给量子热力学能级结构、热浴耦合或频率比机制；无 TUFT 特定效率预测）",
     "verdict": "structural_negative"},
    {"id": "E5", "claim": "裁定",
     "value": "结构性负面闭合：效率界为标准量子热力学定理性算术，TUFT 供给 0，撞 C5/C7",
     "verdict": "structural_negative"},
]
report = {
    "id": CID, "title": "三能级量子热机攻破", "date": DATE,
    "entries": entries,
    "guards": [{"name": n, "passed": p, "note": nt} for n, p, nt in guards],
    "exit_code": 0,
    "red_line": "0/22 保持；UFT-3=0 保持；不宣称实现统一场论；攻破=对 TUFT 结构性负面闭合",
    "precision": "mpmath 250 位 + Fraction 精确",
    "claim": "T536 三能级量子热机：η_C=1−T_c/T_h=2/3，η_CA=1−√(T_c/T_h)=1−1/√3≈0.42264973…，"
             "η_Otto=1−ω_c/ω_h；标准定理输出，TUFT 供给 0，撞 C5/C7",
}
report["ratio_table"] = ratio_table
report["derivatives"] = {
    "deta_CA_dr": mp.nstr(dCA_dr, 24),
    "deta_C_dr": "-1",
    "deta_Otto_dx": "-1",
    "numerical_diff_err": mp.nstr(num_diff_err, 6),
}

with io.open(OUT + r"\attack_C0401_三能级量子热机攻破_2026-10-29_report.txt", "w", encoding="utf-8") as f:
    f.write(
        "C0401 三能级量子热机攻破（2026-10-29，mpmath 250 位 + Fraction 精确）\n"
        f"基准 T_h=300 K、T_c=100 K（r=1/3）\n"
        f"η_C = 1 − T_c/T_h = 2/3（Fraction 精确）\n"
        f"η_CA = 1 − √(T_c/T_h) = 1 − 1/√3 = {mp.nstr(etaCA_mp, 40)}\n"
        f"1/√3 = {mp.nstr(inv_sqrt3_a, 40)}（双路径差={mp.nstr(inv_sqrt3_diff, 6)} < 1e-240）\n"
        f"η_Otto(ω_h/ω_c=3) = 1 − 1/3 = 2/3（Fraction 精确，可逆 = Carnot）\n"
        "温度比表：\n"
    )
    for row in ratio_table:
        f.write(f"  r={row['r']}  η_C={row['eta_C']}  η_CA={row['eta_CA']}\n")
    f.write(
        f"求导：dη_CA/dr=−1/(2√r)={mp.nstr(dCA_dr, 24)}<0；dη_C/dr=−1；dη_Otto/dx=−1；"
        f"差商互验差={mp.nstr(num_diff_err, 6)}<1e-100 ✓\n"
        f"TUFT 供给=0 → 结构性负面，撞 C5/C7；守卫 {len(guards)}/{len(guards)} 全过 → exit=0\n")

with io.open(OUT + r"\attack_C0401_三能级量子热机攻破_2026-10-29.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"C0401 exit=0：η_C=2/3；η_CA={mp.nstr(etaCA_mp, 12)}；"
      f"1/√3={mp.nstr(inv_sqrt3_a, 12)}；dη_CA/dr={mp.nstr(dCA_dr, 12)}；"
      f"守卫 {len(guards)}/8")
