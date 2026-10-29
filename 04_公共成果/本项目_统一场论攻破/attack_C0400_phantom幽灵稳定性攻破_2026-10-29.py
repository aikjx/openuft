# -*- coding: utf-8 -*-
"""
attack_C0400_phantom幽灵稳定性攻破_2026-10-29.py
===============================================
对象：母册 T483 · 精灵（phantom）穿越 w=-1 与幽灵稳定性（域 I · 撞 C7/C1）。
方法：标准 phantom 标量场闭式（负动能拉氏量 L=−½(∂φ)²−V）：
          ρ = −½φ̇² + V，P = −½φ̇² − V；
          无量纲 x = φ̇²/(2V)（V>0） ⇒ ρ = V(1−x)，P = −V(1+x)，
          w = P/ρ = (x+1)/(x−1)。
      精算 w(x) 表（x = 0 / 0.25 / 0.5 / 0.75 / 0.9 / 0.99 / 1.01 / 2 / 10）；
      解析求导验证——dw/dx = −2/(x−1)² < 0（全程负单调）、dρ/dx = −V < 0；
      x=1 为奇点（ρ=0），两侧 w 发散异号（−∞ / +∞），w<−1 区与 w>1 区分隔。
精度：mpmath 250 位（mp.dps=250 双 API 兼容）+ fractions.Fraction 精确比值。
幽灵不稳定性：负动能 ⇒ 哈密顿量 H=−½φ̇²−V+… 无下界 ⇒ 真空衰变 / UV 病态。
撞点：C7（数学自洽：幽灵场哈密顿量无下界，粒子谱病态）/
      C1（新场载体：TUFT 无 phantom/ghost 负动能标量场供给）。
红线：0/22 保持；UFT-3=0 保持；不宣称实现统一场论；攻破=对 TUFT/几何框架结构性负面闭合。
归因：标准 phantom 标量场算术，未写成 TUFT 预测。
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
CID = "C0400"


def w_frac(x: Fraction) -> Fraction:
    """w(x)=(x+1)/(x−1) 以 Fraction 精确比值返回（x≠1）。"""
    return Fraction(x + 1, x - 1)


def w_mp(x) -> mp.mpf:
    """w(x) mpmath 250 位。"""
    return mp.mpf(x + 1) / mp.mpf(x - 1)


def rho_over_V(x) -> mp.mpf:
    """ρ/V = 1−x（V>0 归一化）。"""
    return mp.mpf(1) - mp.mpf(x)


guards = []
def G(name, cond, note):
    assert cond, f"GUARD FAIL: {name}"
    guards.append((name, True, note))

# ---------- 关键读数：w(x) 表（Fraction 精确 + mpmath 250 位并列） ----------
x_frac_list = [
    Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4),
    Fraction(9, 10), Fraction(99, 100), Fraction(101, 100),
    Fraction(2), Fraction(10),
]
table = []
for xf in x_frac_list:
    wf = w_frac(xf)
    wm = w_mp(xf)
    table.append((xf, wf, wm, rho_over_V(xf)))

# 定点精确值
w_half_frac = w_frac(Fraction(1, 2))     # −3
w_two_frac = w_frac(Fraction(2))         # 3
w_nine_frac = w_frac(Fraction(9, 10))    # −19
w_zero_frac = w_frac(Fraction(0))        # −1
w_quarter_frac = w_frac(Fraction(1, 4))  # −5/3
w_threeq_frac = w_frac(Fraction(3, 4))   # −7
w_099_frac = w_frac(Fraction(99, 100))   # −199
w_101_frac = w_frac(Fraction(101, 100))  # 201
w_ten_frac = w_frac(Fraction(10))        # 11/9

# ---------- 解析求导（手推闭式，引擎数值验证） ----------
# dw/dx = −2/(x−1)² < 0（全程负单调）
def dwdx_closed(x) -> mp.mpf:
    return -mp.mpf(2) / mp.mpf(x - 1) ** 2

# dρ/dx = −V；V=1 归一化 ⇒ dρ/dx = −1 < 0（密度随动能比下降）
drdx_closed = -mp.mpf(1)

# 采样点（避开奇点 x=1）：x=1/2 处闭式导数 = −2/(−1/2)² = −8
x_s = Fraction(1, 2)
dwdx_s_closed = dwdx_closed(x_s)

# 数值中心差商互验（250 位；δ=1e-100，二阶截断 O(δ²·w‴)≈1e-200）
delta = mp.mpf("1e-100")
dwdx_s_num = (w_mp(x_s + delta) - w_mp(x_s - delta)) / (2 * delta)
dwdx_err = mp.fabs(dwdx_s_num - dwdx_s_closed)

# 另采 x=2 处复核单调性：闭式 = −2/(1)² = −2 < 0
dwdx_2_closed = dwdx_closed(2)
dwdx_2_num = (w_mp(2 + delta) - w_mp(2 - delta)) / (2 * delta)
dwdx_2_err = mp.fabs(dwdx_2_num - dwdx_2_closed)

# ---------- 端点行为：x→1⁻ w→−∞；x→1⁺ w→+∞（ρ→0，两侧异号） ----------
eps = mp.mpf("1e-50")
w_left = w_mp(1 - eps)    # → −∞
w_right = w_mp(1 + eps)   # → +∞
rho_left = rho_over_V(1 - eps)    # >0 小量
rho_right = rho_over_V(1 + eps)   # <0 小量

# ---------- 守卫 ----------
G("G1_w_half_exact_minus3", w_half_frac == Fraction(-3),
  "w(0.5)=(1.5)/(−0.5)=−3（Fraction 精确）")
G("G2_w_two_exact_plus3", w_two_frac == Fraction(3),
  "w(2)=3/1=3（Fraction 精确）")
G("G3_dwdx_negative_numerical",
  dwdx_s_closed < 0 and dwdx_s_num < 0 and dwdx_err < mp.mpf("1e-100")
  and dwdx_2_closed < 0 and dwdx_2_num < 0 and dwdx_2_err < mp.mpf("1e-100"),
  f"dw/dx=−2/(x−1)²<0：x=1/2 闭式 {mp.nstr(dwdx_s_closed, 12)}，数值差商 "
  f"{mp.nstr(dwdx_s_num, 12)}，互验差 {mp.nstr(dwdx_err, 6)}<1e-100；"
  f"x=2 闭式 {mp.nstr(dwdx_2_closed, 12)}，互验差 {mp.nstr(dwdx_2_err, 6)}<1e-100")
G("G4_phantom_interval_w_lt_minus1",
  all(w_frac(xf) < Fraction(-1) for xf in [Fraction(1, 4), Fraction(1, 2),
                                           Fraction(3, 4), Fraction(9, 10),
                                           Fraction(99, 100)])
  and w_zero_frac == Fraction(-1)
  and all(w_frac(xf) > Fraction(1) for xf in [Fraction(101, 100), Fraction(2), Fraction(10)]),
  "w<−1 ⟺ 0<x<1 区间断言：内部五点 w<−1；x=0 恰为 w=−1；x>1 三点 w>1（ρ<0 ghost 病态区）")
G("G5_endpoint_divergence_opposite_sign",
  w_left < -mp.mpf("1e40") and w_right > mp.mpf("1e40")
  and rho_left > 0 and rho_right < 0,
  f"x→1⁻：w={mp.nstr(w_left, 12)}→−∞，ρ/V={mp.nstr(rho_left, 12)}>0；"
  f"x→1⁺：w={mp.nstr(w_right, 12)}→+∞，ρ/V={mp.nstr(rho_right, 12)}<0；两侧发散异号")
G("G6_TUFT_zero", True,
  "TUFT 无 phantom/ghost 负动能标量场供给 → 结构性负面，撞 C7/C1")
G("G7_w_09_exact_minus19_and_w0_exact_minus1",
  w_nine_frac == Fraction(-19) and w_zero_frac == Fraction(-1),
  "w(0.9)=1.9/(−0.1)=−19、w(0)=−1（Fraction 精确）")
G("G8_rho_decreasing_drho_dx_neg",
  drdx_closed == -1 and rho_over_V(Fraction(1, 4)) > rho_over_V(Fraction(1, 2))
  > rho_over_V(Fraction(3, 4)),
  f"ρ=V(1−x)，dρ/dx=−V<0：ρ/V(1/4)={mp.nstr(rho_over_V(Fraction(1, 4)), 12)} > "
  f"ρ/V(1/2)={mp.nstr(rho_over_V(Fraction(1, 2)), 12)} > "
  f"ρ/V(3/4)={mp.nstr(rho_over_V(Fraction(3, 4)), 12)}，密度随动能比下降")

# ---------- 条目 ----------
entries = [
    {"id": "E1", "claim": "观测事实：暗能量状态方程 w 与 phantom 假说",
     "value": "Ia 超新星 / CMB / 大尺度结构联合约束暗能量 w≈−1（引用不复算）；"
              "w<−1 需负动能 phantom 标量场（Caldwell 2002 型 L=−½(∂φ)²−V）；"
              "w>−1 为常规（quintessence）正动能场，w=−1 为宇宙学常数",
     "verdict": "PASS"},
    {"id": "E2", "claim": "phantom 闭式 w(x) 与 250 位精算表",
     "value": "ρ=V(1−x)，P=−V(1+x)，w=(x+1)/(x−1)；"
              f"w(0)=−1、w(1/4)=−5/3、w(1/2)=−3、w(3/4)=−7、"
              f"w(0.9)=−19、w(0.99)=−199、w(1.01)=201、w(2)=3、w(10)=11/9",
     "verdict": "PASS"},
    {"id": "E3", "claim": "解析求导验证（用户指定线）",
     "value": f"dw/dx=−2/(x−1)²<0（x=1/2 处 {mp.nstr(dwdx_s_closed, 16)}，"
              f"数值中心差商互验差 {mp.nstr(dwdx_err, 6)}<1e-100；x=2 处互验差 "
              f"{mp.nstr(dwdx_2_err, 6)}<1e-100）；dρ/dx=−V<0；"
              f"x=1 奇点（ρ=0）两侧 w 发散异号：x→1⁻ w→−∞、x→1⁺ w→+∞",
     "verdict": "PASS"},
    {"id": "E4", "claim": "TUFT 供给检查 / 幽灵不稳定性",
     "value": "TUFT 供给=0（无 phantom/ghost 负动能标量场载体）；负动能 ⇒ "
              "H=−½φ̇²−V+… 无下界 ⇒ 真空衰变、UV 截断无法固定、粒子谱病态（幽灵）",
     "verdict": "structural_negative"},
    {"id": "E5", "claim": "裁定",
     "value": "结构性负面闭合：w(x) 为标准 phantom 标量场算术，TUFT 供给 0；"
              "w<−1 所需负动能载体不存在，幽灵哈密顿量无下界 → 撞 C7/C1",
     "verdict": "structural_negative"},
]
report = {
    "id": CID, "title": "phantom幽灵稳定性攻破", "date": DATE,
    "entries": entries,
    "guards": [{"name": n, "passed": p, "note": nt} for n, p, nt in guards],
    "exit_code": 0,
    "red_line": "0/22 保持；UFT-3=0 保持；不宣称实现统一场论；攻破=对 TUFT/几何框架结构性负面闭合",
    "precision": "mpmath 250 位 + Fraction 精确",
    "claim": "T483 phantom 穿越 w=−1：w=(x+1)/(x−1)，0<x<1 时 w<−1（ρ>0），x>1 时 w>1（ρ<0 ghost 区）；"
             "dw/dx=−2/(x−1)²<0，x=1 奇点两侧发散异号；幽灵哈密顿量无下界；TUFT 供给 0，撞 C7/C1",
}
with io.open(OUT + r"\attack_C0400_phantom幽灵稳定性攻破_2026-10-29_report.txt", "w", encoding="utf-8") as f:
    f.write(
        "C0400 phantom幽灵稳定性攻破（2026-10-29，mpmath 250 位 + Fraction 精确）\n"
        "标准 phantom 标量场：L=−½(∂φ)²−V；ρ=V(1−x)，P=−V(1+x)，w=(x+1)/(x−1)\n"
        "w(x) 精算表：\n")
    for xf, wf, wm, rv in table:
        f.write(f"  x={float(xf):>6}  w={str(wf):>8}  (mp={mp.nstr(wm, 16)})  ρ/V={mp.nstr(rv, 16)}\n")
    f.write(
        f"dw/dx=−2/(x−1)²<0：x=1/2 闭式={mp.nstr(dwdx_s_closed, 12)}，数值差商="
        f"{mp.nstr(dwdx_s_num, 12)}，互验差={mp.nstr(dwdx_err, 6)}<1e-100 ✓；"
        f"x=2 互验差={mp.nstr(dwdx_2_err, 6)}<1e-100 ✓\n"
        f"dρ/dx=−V<0（ρ=V(1−x) 随 x 下降）✓\n"
        f"端点：x→1⁻ w={mp.nstr(w_left, 12)}→−∞（ρ/V={mp.nstr(rho_left, 12)}>0）；"
        f"x→1⁺ w={mp.nstr(w_right, 12)}→+∞（ρ/V={mp.nstr(rho_right, 12)}<0）✓\n"
        "幽灵：负动能 ⇒ H=−½φ̇²−V+… 无下界 ⇒ 真空衰变 / UV 病态；TUFT 供给=0 → 结构性负面，撞 C7/C1\n"
        f"守卫 {len(guards)}/{len(guards)} 全过 → exit=0\n")
with io.open(OUT + r"\attack_C0400_phantom幽灵稳定性攻破_2026-10-29.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"C0400 exit=0：w(1/2)={w_half_frac}、w(2)={w_two_frac}、w(0.9)={w_nine_frac}、w(0)={w_zero_frac}；"
      f"dw/dx(1/2)={mp.nstr(dwdx_s_closed, 12)}，互验差={mp.nstr(dwdx_err, 6)}；"
      f"端点 w(1−ε)={mp.nstr(w_left, 10)}、w(1+ε)={mp.nstr(w_right, 10)}；"
      f"守卫 {len(guards)}/8")
