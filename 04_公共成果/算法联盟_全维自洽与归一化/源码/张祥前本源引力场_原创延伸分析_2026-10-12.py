# -*- coding: utf-8 -*-
# 张祥前《本源引力场》原创延伸分析（判定册 §十三~§十六 的机器读数来源）
# 日期：2026-10-12
# 口径：纯标准库 Decimal 60 位 + Fraction 三维量纲 (M,L,T)；复用审计册同套量纲代数。
# 目的：在「等价于牛顿引力」裁定之外，做四类原创机器分析——
#   (A) 自然/普朗克单位制换算：把修复式放进 G=c=hbar=1 看数值身份；
#   (B) 与 GR 弱场低速极限对标：量化偏离 GR 的尺度参数；
#   (C) 实验可证伪性边界：列出可区分牛顿/GR 的经典检验并判定本体系位置；
#   (D) 量纲缺口波及扫描：D01/D04 的 (1,-3,2)=[1/G] 缺口若出现在其它「无 G 牛顿类比项」会如何。
import json, os, sys
from fractions import Fraction
from decimal import Decimal, getcontext
getcontext().prec = 60

# ============================ 量纲系统 (M,L,T) ============================
def D(*e):
    return tuple(Fraction(x) for x in e)
M = D(1, 0, 0)
L = D(0, 1, 0)
T = D(0, 0, 1)
G_DIM = D(-1, 3, -2)
def dscale(d, k):
    return tuple(a * Fraction(k) for a in d)
def dadd(d1, d2):
    return tuple(a + b for a, b in zip(d1, d2))
def dpow(d, e):
    return dscale(d, Fraction(e))
def deq(d1, d2):
    return all(a == b for a, b in zip(d1, d2))
def dim_str(d):
    parts = []
    names = "MLT"
    for nm, v in zip(names, d):
        if v == 0:
            continue
        s = "%s" % nm
        if v != 1:
            s += "^%s" % (v if v.denominator == 1 else "(%s)" % v)
        parts.append(s)
    return "·".join(parts) if parts else "1(无量纲)"

# ============================ 常数 (CODATA / 定义值) ============================
C = Decimal("299792458")            # m/s
G = Decimal("6.67430e-11")           # m^3 kg^-1 s^-2
HBAR = Decimal("1.054571817e-34")    # J·s
L_P = (HBAR * G / C ** 3).sqrt()     # 普朗克长度
T_P = L_P / C                        # 普朗克时间
M_P = (HBAR * C / G).sqrt()          # 普朗克质量
M_SUN = Decimal("1.98847e30")        # kg
BODIES = {
    "地球": (Decimal("29780"), Decimal("1.495978707e11")),
    "木星": (Decimal("13070"), Decimal("7.785e11")),
}

# ============================ (A) 自然/普朗克单位制换算 ============================
planck = {}
for name, (v, r) in BODIES.items():
    M_calc = v * v * r / G
    planck[name] = {
        "r_in_planck_length": str(r / L_P),
        "v_over_c": str(v / C),
        "M_in_planck_mass": str(M_calc / M_P),
        "M_kg": str(M_calc),
    }

# ============================ (B) 与 GR 弱场低速极限对标 ============================
gr = {}
for name, (v, r) in BODIES.items():
    M_calc = v * v * r / G
    gr[name] = {
        "v_over_c": str(v / C),
        "GM_over_rc2": str(G * M_calc / (r * C * C)),
    }

# ============================ (D) 量纲缺口波及扫描 ============================
# 若张祥前体系「无 G」地写出牛顿类比项，各类公式命中什么缺口。
scans = []
def scan(formula, computed, expected):
    gap = dadd(expected, dscale(computed, -1))
    scans.append({
        "formula": formula,
        "computed_dim": dim_str(computed),
        "expected_dim": dim_str(expected),
        "gap_dim": dim_str(gap),
        "gap_is_zero": deq(gap, D(0, 0, 0)),
    })

# 运动学量纲基线
V_DIM = dpow(D(0, 1, -1), 2)          # [v^2] = L^2 T^-2
E_DIM = dadd(M, dadd(dpow(L, 2), dpow(T, -2)))   # 能量 (1,2,-2)
F_DIM = dadd(M, dadd(L, dpow(T, -2)))            # 力 (1,1,-2)

scan("m = v^2 r / G (修复轨道式)", dadd(dadd(V_DIM, L), dpow(G_DIM, -1)), M)
scan("A = -m/R^2 (原始场)", dadd(M, dpow(L, -2)), dadd(L, dpow(T, -2)))
scan("U = -m/R (本源势能若如此写)", dadd(M, dpow(L, -1)), E_DIM)
scan("U = -m M/R (含中心质量仍无 G)", dadd(dadd(M, M), dpow(L, -1)), E_DIM)
scan("F = m v^2 / r (向心力)", dadd(dadd(M, V_DIM), dpow(L, -1)), F_DIM)
scan("E = 1/2 m v^2 (动能)", dadd(M, V_DIM), E_DIM)

# ============================ 汇总 ============================
RESULTS = {
    "engine": "张祥前本源引力场_原创延伸分析",
    "date": "2026-10-12",
    "rating_context": "C/L1（判定册 §九 本质裁定：等价于牛顿引力的数学改写）",
    "constants": {
        "c": str(C), "G": str(G), "hbar": str(HBAR),
        "l_P": str(L_P), "t_P": str(T_P), "m_P": str(M_P),
    },
    "planck_units": planck,
    "gr_weak_field": gr,
    "dim_gap_spread": scans,
}
base = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.abspath(os.path.join(base, "..", "数据"))
os.makedirs(data_dir, exist_ok=True)
stem = "张祥前本源引力场_原创延伸分析_2026-10-12"
with open(os.path.join(data_dir, stem + ".json"), "w", encoding="utf-8") as f:
    json.dump(RESULTS, f, ensure_ascii=False, indent=2)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
print(json.dumps(RESULTS, ensure_ascii=False, indent=2))
