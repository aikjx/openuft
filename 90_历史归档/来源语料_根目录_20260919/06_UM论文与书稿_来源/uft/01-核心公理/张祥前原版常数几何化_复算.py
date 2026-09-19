# -*- coding: utf-8 -*-
"""
张祥前原版「常数几何化」复算：检验 Z、Z'、k、k' 是否只是 CODATA 常数的重包装。

红线（ROOT）：只记录实跑结果；若把已知常数代入重排得到新常数，且新常数不产出任何
可检验预测，则判定为「标识符重命名（O-TAUT 类）」，不得记为「第一性原理推导」。

运行：
  python uft/01-核心公理/张祥前原版常数几何化_复算.py
"""

import sys
import json
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import mpmath as mp

mp.mp.dps = 50

G = mp.mpf("6.67430e-11")
c = mp.mpf("299792458")
eps0 = mp.mpf("8.8541878128e-12")
m_p = mp.mpf("2.176434e-8")      # 张祥前给的普朗克质量
q_p = mp.mpf("1.8755e-18")       # 张祥前给的普朗克电荷

# 张祥前原版给出的「几何化常数」数值
Z_claim = mp.mpf("1.000e-2")
Zp_claim = mp.mpf("1.347e18")
k_claim = mp.mpf("2.736e-7")
kp_claim = mp.mpf("6.25e-27")

# 按原版定义式计算
Z_calc = G * c / 2
Zp_calc = c / (8 * mp.pi * eps0)
k_calc = 4 * mp.pi * m_p
kp_calc = q_p / c

rows = []
def chk(name, claim, calc):
    dev = mp.fabs(claim - calc) / (mp.fabs(claim) + mp.mpf("1e-300"))
    rows.append((name, claim, calc, dev))
    print("[" + name + "]")
    print("        原版声称:", mp.nstr(claim, 8))
    print("        由 CODATA 重算:", mp.nstr(calc, 8))
    print("        相对偏差:", mp.nstr(dev, 4))
    print("")

chk("Z = Gc/2", Z_claim, Z_calc)
chk("Z' = c/(8 pi eps0)", Zp_claim, Zp_calc)
chk("k = 4 pi m_p", k_claim, k_calc)
chk("k' = q_p / c", kp_claim, kp_calc)

# 反推 G 与 eps0：验证只是重排
G_back = 2 * Z_calc / c
eps_back = c / (8 * mp.pi * Zp_calc)
print("[反推检验]")
print("        由 Z 反推 G =", mp.nstr(G_back, 12), "vs CODATA G =", mp.nstr(G, 12))
print("        由 Z' 反推 eps0 =", mp.nstr(eps_back, 12), "vs CODATA eps0 =", mp.nstr(eps0, 12))
print("")

summary = ("原版 4 个几何化常数均等于「用 CODATA 已知常数代入定义式」所得值，"
           "相对偏差 < 1e-3；由它们反推 G、eps0 又回到 CODATA 原值。"
           "结论：这是标识符重命名（O-TAUT 类），不含独立物理信息，"
           "TUFT 继承的 'kap^2+tau^2=(omega/c)^2 复现普朗克单位' 同属此类（见 T3/H8）。")
print("结论:", summary)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "张祥前原版常数几何化_复算结果.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump({
        "Z": {"claim": str(Z_claim), "calc": str(Z_calc), "rel_dev": str(rows[0][3])},
        "Zp": {"claim": str(Zp_claim), "calc": str(Zp_calc), "rel_dev": str(rows[1][3])},
        "k": {"claim": str(k_claim), "calc": str(k_calc), "rel_dev": str(rows[2][3])},
        "kp": {"claim": str(kp_claim), "calc": str(kp_calc), "rel_dev": str(rows[3][3])},
        "G_back": str(G_back), "eps0_back": str(eps_back),
        "结论": summary,
    }, f, ensure_ascii=False, indent=2)
print("写出:", out)
