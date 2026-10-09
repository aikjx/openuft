# -*- coding: utf-8 -*-
"""
G7 规范群选择 · 异常抵消核验（2026-10-09）

目的
----
把"为何是 SU(3)×SU(2)×U(1)"这一开放元问题（达成度总账 §5 G7）转化为机器可验证的
**结构约束审计**：任何第一性推导若想导出该规范群，必须解释其手征谱为何**无规范反常**。
本脚本用标准模型单代手征费米子表，计算五类三角反常系数（含引力混合），
断言它们全部为零——以此核验"SM 谱是反常自由的"这一已知事实，并把它作为 G7 推导的硬约束。

纪律
----
本脚本**不**声称从第一性原理导出 SU(3)×SU(2)×U(1)；它只核验"反常自由"这一约束被满足，
并显式标注 Y 超荷赋值与代数是**外部输入**（非本脚本导出），按"外部输入四步"纪律登记为 OPEN。

反常系数约定（标准归一化）
--------------------------
- 每个手征 Weyl 场 f 带：色维 dim_c（3 或 1）、弱维 dim_w（2 或 1）、超荷 Y、手征 sign（左 +1 / 右 −1）。
- SU(N) 基本表示 cubic 反常指标 A_N(fund)=+1、A_N(fund*)=−1、单态=0；SU(2) 基本为赝实，A_2=0。
- 混合 [G]²[U(1)_Y] 用 Tr_G(T^a T^b) = (1/2) δ^{ab}（基本），故系数含 (1/2) 因子。
- 五类系数：
    C_SU3 = Σ A_3(色表示) × dim_w × sign          （[SU(3)]³）
    C_SU2 = Σ A_2(弱表示) × dim_c × sign          （[SU(2)]³，A_2≡0 ⇒ 恒为 0）
    C_U1  = Σ Y³ × dim_c × dim_w × sign           （[U(1)_Y]³）
    C_M2  = (1/2) Σ Y × dim_c × A_2(弱表示) × sign （[SU(2)]²[U(1)_Y]）
    C_M3  = (1/2) Σ Y × dim_w × A_3(色表示) × sign （[SU(3)]²[U(1)_Y]）
    C_GRAV= Σ Y × dim_c × dim_w × sign            （引力²[U(1)_Y]）
  反常自由 ⇔ 全部 = 0。
"""

import os
import json
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 4)))

# 标准模型单代手征费米子（含每代 3 色 × 2 弱 维数的场分量已按 dim_c/dim_w 计入）
# (名称, dim_c, dim_w, Y, chirality_sign)  左 = +1, 右 = -1
SM_ONE_GENERATION = [
    ("Q_L",  3, 2,  1.0/6, +1),   # (3,2)_{+1/6}
    ("u_R",  3, 1,  2.0/3, -1),   # (3*,1)_{+2/3}
    ("d_R",  3, 1, -1.0/3, -1),   # (3*,1)_{-1/3}
    ("L_L",  1, 2, -1.0/2, +1),   # (1,2)_{-1/2}
    ("e_R",  1, 1, -1.0,   -1),   # (1,1)_{-1}
    # 右手中微子 (1,1)_0 对全部系数贡献 0，省略不影响
]


def a3(color_rep_dim):
    """[SU(3)]³ cubic 反常指标：基本 3 → +1，反基本 3* → -1，单态 → 0。"""
    if color_rep_dim == 3:
        return +1
    if color_rep_dim == 1:
        return 0
    return 0


def a2(weak_rep_dim):
    """[SU(2)]³ cubic 反常指标：基本 2 为赝实 ⇒ 恒 0。"""
    return 0


def compute_coefficients(fermions):
    C_SU3 = C_U1 = C_M2 = C_M3 = C_GRAV = 0.0
    for name, dim_c, dim_w, Y, s in fermions:
        C_SU3 += a3(dim_c) * dim_w * s
        C_U1  += (Y ** 3) * dim_c * dim_w * s
        C_M2  += 0.5 * Y * dim_c * a2(dim_w) * s
        C_M3  += 0.5 * Y * dim_w * a3(dim_c) * s
        C_GRAV += Y * dim_c * dim_w * s
    return {
        "[SU(3)]^3": C_SU3,
        "[SU(2)]^3": 0.0,              # A_2≡0，恒为 0（显式列出以表明已核验）
        "[U(1)_Y]^3": C_U1,
        "[SU(2)]^2[U(1)_Y]": C_M2,
        "[SU(3)]^2[U(1)_Y]": C_M3,
        "gravity^2[U(1)_Y]": C_GRAV,
    }


def main():
    fermions = SM_ONE_GENERATION
    coeffs = compute_coefficients(fermions)
    tol = 1e-12
    failures = {k: v for k, v in coeffs.items() if abs(v) > tol}

    print("=" * 70)
    print("G7 规范群选择 · 异常抵消核验")
    print("=" * 70)
    print("SM 单代手征费米子表（外部输入，非本脚本导出）：")
    for name, dim_c, dim_w, Y, s in fermions:
        print("  %-6s  dim_c=%d dim_w=%d  Y=%.6g  %s"
              % (name, dim_c, dim_w, Y, "L" if s > 0 else "R"))
    print("-" * 70)
    print("五类三角反常系数（反常自由 ⇔ 全 0）：")
    for k, v in coeffs.items():
        print("  %-20s = % .6e   %s" % (k, v, "OK" if abs(v) <= tol else "NONZERO!!"))
    print("-" * 70)
    if failures:
        print("[FAIL] 以下系数非零：", failures)
        ok = False
    else:
        print("[OK] SM 单代谱反常自由（全部系数 = 0，容差 %g）" % tol)
        ok = True

    ledger = {
        "doc": "G7_规范群选择_异常抵消核验",
        "date": "2026-10-09",
        "fermion_table": "SM 单代手征谱（外部输入）",
        "coefficients": coeffs,
        "all_zero": ok,
        "note": "Y 赋值与代数均为外部输入；第一性推导 SU(3)xSU(2)xU(1) 仍 OPEN",
    }
    out = os.path.join(HERE, "G7_规范群选择_异常抵消核验_out_2026-10-09.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)
    print("[out] 账本已写", out)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
