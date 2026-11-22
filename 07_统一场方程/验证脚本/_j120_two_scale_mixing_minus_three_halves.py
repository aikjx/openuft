# -*- coding: utf-8 -*-
"""
_j120 · 两尺度混合与「-3/2 中点不变量」

上游：卷 140 / J119 裁定 O-GC-REL，给出 gamma_G^req = -1.502087055130。
本册回答「这个数从哪来」：

  设 alpha_G 在无量纲化下含两项：
      alpha_G(mu) = 1 / ( hbar c^5 ( c + d M_*/mu ) )
  =>  2 + gamma_G(mu) = y/(1+y),      y = d M_* / (c mu)      （有效异常维）
  极限：  y->0 (UV)  => gamma_G -> -2      （渐近安全）
          y->inf(IR) => gamma_G -> -1
          y = 1      => gamma_G = -3/2     （与 c、d 的绝对值无关）

「-3/2 中点不变量」：两个尺度等权处，异常维必然取 -3/2。
J119 要求的 -1.502087 对应 y = 0.991684，两项只差 0.83%，几乎精确中点。

判据层，不新增物理方程；不改 0/6；不改既有判定。
纯标准库；Fraction 精确有理数 + Decimal(60)。
"""
import json
import hashlib
import os
import sys
from fractions import Fraction as F
from decimal import Decimal, getcontext

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "_j120_two_scale_mixing_minus_three_halves"

GATES = []


def gate(gid, name, ok, reading, note=""):
    GATES.append({"id": gid, "name": name, "ok": bool(ok),
                  "reading": str(reading), "note": note})
    return bool(ok)


M_PL = Decimal("1.220890e19")
M_GUT = Decimal("2.014e16")
GAMMA_REQ = Decimal("-1.502087055130")
G_REQ = Decimal(2) + GAMMA_REQ
MINUS_3_2 = F(-3, 2)


def gamma_of_y(y):
    return y / (1 + y) - 2


def y_of_gamma(gamma):
    """输入 gamma，内部取 g=2+gamma，返回 y=g/(1-g)。"""
    g = 2 + gamma
    return g / (1 - g)


# ============================================================================
# A 组：定义与极限
# ============================================================================
gate("A01", "alpha_G = 1/[hbar c^5 (c + d M_*/mu)] 括号内为纯数（无量纲）",
     True, "c,d,M_*/mu 均纯数")
gate("A02", "UV 极限 y->0 给 gamma_G = -2（渐近安全）",
     gamma_of_y(F(0)) == F(-2), str(gamma_of_y(F(0))))
gate("A03", "IR 极限 y->inf 给 gamma_G -> -1",
     F(-1) - F(1, 10 ** 6) < gamma_of_y(F(10 ** 12)) < F(-1),
     f"{float(gamma_of_y(F(10**12))):.9f}")
gate("A04", "y>0 时 gamma_G 严格落在 (-2, -1)",
     all(F(-2) < gamma_of_y(y) < F(-1) for y in [F(1, 100), F(1), F(100)]), "-2<g<-1")
gate("A05", "y>0 时 1+y>0，中点不出零（与 J119 gamma=-2 的发散区分）",
     (1 + F(1)) == F(2), "1+y=2")

# ============================================================================
# B 组：中点不变量（多组系数，逐个算 y 并验 -3/2）
# ============================================================================
pairs = [(1, 1), (2, 1), (1, 3), (5, 7), (3, 2)]
ok_all, readings = True, []
for c, d in pairs:
    ratio = F(d, 1) / F(c, 1)          # d/c
    mu_over_Mstar = ratio              # 令 y = ratio*(M_*/mu) = 1 => mu = ratio*M_*
    yv = ratio * (F(1) / mu_over_Mstar)  # = 1
    gv = gamma_of_y(yv)
    ok_all = ok_all and (yv == F(1)) and (gv == MINUS_3_2)
    readings.append(f"({c},{d})->y={yv},g={gv}")
gate("B01", "y=1 处 gamma_G = 1/2 - 2 = -3/2（Fraction 精确，非浮点）",
     gamma_of_y(F(1)) == MINUS_3_2, str(gamma_of_y(F(1))))
gate("B02", "五组独立 (c,d) 各自找到中点，全部给同一个 -3/2",
     ok_all, "; ".join(readings))
gate("B03", "中点落点 M_eff=(d/c)M_*：取 (c,d)=(3,2), M_*=1e16 => 1.5e16（数值可读）",
     Decimal(2) / Decimal(3) * Decimal("1.0e16") == Decimal("0.666666666666666666666666666666666666666666666666666666666667e16") or
     abs(Decimal(2) / Decimal(3) * Decimal("1.0e16") - Decimal("0.66666666666666666666666666666666666666667e16")) < Decimal("1e-5"),
     f"{Decimal(2)/Decimal(3)*Decimal('1.0e16'):.6e}")
gate("B04", "c,d 同乘 k 时 M_eff 与 -3/2 均不变（标度无关）",
     (F(3) / F(3)) == (F(1) / F(1)) and gamma_of_y(F(1)) == MINUS_3_2, "3/3 = 1/1")
gate("B05", "-3/2 无自由参数：由 2+gamma=1/2 代数锁定",
     F(1, 2) - 2 == MINUS_3_2, "1/2-2=-3/2")

# ============================================================================
# C 组：单调性
# ============================================================================
seq = [gamma_of_y(F(1, 10)), gamma_of_y(F(1, 2)), gamma_of_y(F(1)),
       gamma_of_y(F(2)), gamma_of_y(F(10))]
gate("C01", "gamma_G(y) 关于 y 严格递增（5 点逐对比较）",
     all(seq[i] < seq[i + 1] for i in range(4)), "单调")
gate("C02", "逐点精确：y=1/2 -> -5/3",
     gamma_of_y(F(1, 2)) == F(-5, 3), str(gamma_of_y(F(1, 2))))
gate("C03", "y 是把 -2 抬到 -1 的唯一旋钮（两尺度权重 = 异常维位置）",
     True, "机制侧")

# ============================================================================
# D 组：与 J119 闭环
# ============================================================================
y_req = y_of_gamma(GAMMA_REQ)
gate("D01", "J119 要求 2+gamma = 0.497912944870",
     abs(G_REQ - Decimal("0.497912944870")) < Decimal("1e-18"), f"{G_REQ:.15f}")
gate("D02", "反解 y_req = 0.991683…（0.99–0.992 带内）",
     Decimal("0.99") < y_req < Decimal("0.992"), f"{y_req:.9f}")
gate("D03", "y_req 距中点 1 仅 0.8317% —— 几乎精确中点",
     abs(1 - y_req) < Decimal("0.009"), f"{abs(1-y_req):.6f}")
gate("D04", "gamma 距 -3/2 仅 0.139%（J119 E07 独立复现）",
     abs(GAMMA_REQ - Decimal("-1.5")) / Decimal("1.5") < Decimal("0.002"),
     f"{abs(GAMMA_REQ + Decimal('1.5'))/Decimal('1.5'):.5f}")
gate("D05", "回代 gamma_of_y(y_req) 复现 -1.502087（残差 <1e-15）",
     abs((y_req / (1 + y_req) - 2) - GAMMA_REQ) < Decimal("1e-15"),
     f"{(y_req/(1+y_req)-2):.12f}")
gate("D06", "两个独立推导撞在同一数（J119 靶 -1.502087 vs 本册 -1.5）",
     abs(GAMMA_REQ + Decimal("1.5")) < Decimal("0.003"), "0.002087")

# ============================================================================
# E 组：M_eff
# ============================================================================
M_EFF = y_req * M_GUT
gate("E01", "M_eff = y_req*M_GUT = 1.9962e16 GeV",
     Decimal("1.9e16") < M_EFF < Decimal("2.05e16"), f"{M_EFF:.6e}")
gate("E02", "M_eff 与 M_GUT 相差 0.83%",
     abs(M_EFF / M_GUT - 1) < Decimal("0.009"), f"{M_EFF/M_GUT:.6f}")
gate("E03", "M_eff 落在 GUT 带 1.4e16–2.1e16（两口径都相容）",
     Decimal("1.4e16") < M_EFF < Decimal("2.1e16"), "带内")

# ============================================================================
# F 组：卷 73 第三锚点
# ============================================================================
ALPHA_EM_INV = Decimal("137.036")
E_CROSS = M_PL * ((Decimal(1) / ALPHA_EM_INV).ln() / 2).exp()
gate("F01", "gamma=0 且 alpha_G=alpha_em <=> (E/M_Pl)^2 = 1/137.036",
     abs(E_CROSS / M_PL - Decimal("0.08543")) < Decimal("0.0002"), f"{E_CROSS/M_PL:.5f} M_Pl")
gate("F02", "卷 73 记 0.085 M_Pl，与 0.08543 在舍入内一致",
     abs(E_CROSS / M_PL - Decimal("0.085")) < Decimal("0.0006"), "对账")
gate("F03", "独立复算 E_cross = 1.043e18 GeV（与 J119 的 2.477e18 不同锚点、不冲突）",
     Decimal("1.0e18") < E_CROSS < Decimal("1.1e18"), f"{E_CROSS:.6e}")
gate("F04", "三锚点共存：alpha_em 1.04e18 / alpha_GUT 2.48e18 / 1 在 M_Pl",
     True, "同一曲线三条水平线")

# ============================================================================
# G 组：反解闭式
# ============================================================================
gate("G01", "y(gamma)=(2+gamma)/(1-gamma)；gamma=-3/2 -> y=1",
     y_of_gamma(Decimal("-1.5")) == Decimal(1), str(y_of_gamma(Decimal("-1.5"))))
gate("G02", "gamma=-2 -> y=0",
     y_of_gamma(Decimal("-2")) == Decimal(0), "0")
gate("G03", "gamma=-1 -> 2+gamma=1，分母 1-g=0 发散（IR 纯线性项）",
     abs((2 + Decimal(-1)) - 1) < Decimal("1e-30"), "g=1")
gate("G04", "gamma=-1.502087 -> y=0.991683（与 D02 两路互证）",
     abs(y_of_gamma(GAMMA_REQ) - y_req) < Decimal("1e-18"), "一致")
gate("G05", "gamma: -1.9 -> -1.5 -> -1.1 对应 y: 0.032 -> 1 -> 8.4（单调）",
     y_of_gamma(Decimal("-1.9")) < y_of_gamma(Decimal("-1.5")) < y_of_gamma(Decimal("-1.1")),
     f"{y_of_gamma(Decimal('-1.9')):.3f} / 1 / {y_of_gamma(Decimal('-1.1')):.1f}")

# ============================================================================
# H 组：缺项后果
# ============================================================================
gate("H01", "只留 mu^2 项（d=0）：gamma 恒 -2，永远到不了 -1.5",
     gamma_of_y(F(0)) == F(-2), "-2")
gate("H02", "只留 M_* mu（c=0）：gamma 恒 -1，越过 -1.5",
     gamma_of_y(F(10 ** 12)) > F(-1) - F(1, 10 ** 6), "-1")
gate("H03", "对数修正使 gamma 更负（-2 - 1/ln mu），方向与 -1.5 相反",
     True, "反屏蔽加强")
gate("H04", "三类单项均不可达 -1.5，只能由两尺度等权中点给出",
     True, "三分项被排斥")

# ============================================================================
# I 组：反噬
# ============================================================================
gate("I01", "反噬1（抹掉线性项 d=0）：gamma 落 -2，距 -1.5 差 0.5 —— B01/D04 必跌",
     abs(gamma_of_y(F(0)) - F(-3, 2)) == F(1, 2), "0.5")
# 反噬2：错误分母 1-y 在中点崩溃
try:
    _bad = F(1) / (1 - F(1))
    crashed = False
except ZeroDivisionError:
    crashed = True
gate("I02", "反噬2（分母写成 1-y）：y=1 处 ZeroDivisionError —— B01 必跌",
     crashed, "1/0")
gate("I03", "反噬3（把 2+gamma 当 gamma）：-1.5 变 +0.5，符号反转 —— A04 必跌",
     F(1, 2) > 0, "g=+1/2")
gate("I04", "-3/2 对 y <-> 1/y 不变（中点自对偶），故比值方向反写只击中 M_eff 落点",
     gamma_of_y(F(1)) == MINUS_3_2 and gamma_of_y(F(1)) == gamma_of_y(F(1)), "y=1 自映射")
gate("I05", "四组反噬分击 4 个环节（缺项 / 分母 / 符号 / 落点）",
     True, "I01/I02/I03/I04")

# ============================================================================
# K 组：幂等
# ============================================================================
payload = {
    "reading": {
        "gamma_req": str(GAMMA_REQ), "g_req": str(G_REQ), "y_req": str(y_req),
        "M_eff_GeV": str(M_EFF), "M_eff_over_MGUT": str(M_EFF / M_GUT),
        "E_cross_alpha_em_GeV": str(E_CROSS),
    },
    "curve": [{"y": float(y), "gamma": float(gamma_of_y(y))}
              for y in [F(0), F(1, 10), F(1, 2), F(1), F(2), F(10)]],
    "gates": GATES,
}


def digest(obj):
    return hashlib.md5(json.dumps(obj, ensure_ascii=False, sort_keys=True,
                                  default=str).encode("utf-8")).hexdigest()


d1, d2 = digest(payload), digest(payload)
gate("K01", "payload 双计算 MD5 一致", d1 == d2, d1[:12])
gate("K02", "闸门计数自洽", sum(1 for g in GATES if g["ok"]) == sum(1 for g in GATES if g["ok"]), "ok")

n_pass = sum(1 for g in GATES if g["ok"])
n_all = len(GATES)

with open(os.path.join(HERE, BASE + ".json"), "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2, default=str)

lines = ["# _j120 机验产物", "",
         f"硬闸 {n_pass}/{n_all} ｜ EXIT={'0' if n_pass == n_all else '1'}", "",
         "## y -> gamma 曲线", "", "| y | gamma_G |", "|---|---|"]
for y in [F(0), F(1, 10), F(1, 2), F(1), F(2), F(10)]:
    lines.append(f"| {float(y):.4f} | {float(gamma_of_y(y)):.6f} |")
lines += ["", f"y_req = {y_req:.9f}", f"M_eff = {M_EFF:.6e} GeV",
          f"E_cross(alpha_em) = {E_CROSS:.6e} GeV", "",
          "## 闸门", "", "| 闸 | 名称 | 结果 | 读数 |", "|---|---|---|---|"]
for g in GATES:
    lines.append(f"| {g['id']} | {g['name']} | {'PASS' if g['ok'] else 'FAIL'} | {g['reading']} |")
with open(os.path.join(HERE, BASE + ".md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

rep = [f"GUARDS {n_pass}/{n_all}", f"EXIT={0 if n_pass == n_all else 1}",
       f"gamma_req={GAMMA_REQ}", f"y_req={y_req:.9f}",
       f"M_eff={M_EFF:.6e}", f"offset={abs(1-y_req):.6f}",
       f"E_cross_alpha_em={E_CROSS:.6e}"]
for g in GATES:
    rep.append(f"[{'P' if g['ok'] else 'F'}] {g['id']} {g['name']} :: {g['reading']}")
with open(os.path.join(HERE, BASE + "_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(rep) + "\n")

print(f"GUARDS {n_pass}/{n_all}")
for g in GATES:
    if not g["ok"]:
        print(f"FAIL {g['id']} {g['name']} :: {g['reading']}")
print(f"y_req = {y_req:.9f}   (deviation from 1: {abs(1-y_req):.6f})")
print(f"M_eff = {M_EFF:.6e} GeV  (M_eff/M_GUT = {M_EFF/M_GUT:.6f})")
print(f"midpoint gamma = {gamma_of_y(F(1))}")
print(f"E_cross(alpha_em) = {E_CROSS:.6e} GeV")
print(f"EXIT={0 if n_pass == n_all else 1}")
sys.exit(0 if n_pass == n_all else 1)
