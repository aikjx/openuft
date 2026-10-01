# -*- coding: utf-8 -*-
"""
tuft_scale_transmutation_attack_v1.py
=====================================

【攻坚】H-TUFT 内生标度：正面攻击**定理 C**（无跑动 ⇒ 无第一性尺度）
—— 判定「唯一未被阻断的内生标度路」是否真的存在。

本轮要回答的唯一问题：
  能否**在保留 H-TUFT/TUFT 的定义**（`α` 为**拓扑不变量的常数系数**）的前提下，
  实现 `beta_alpha != 0`（跑动）从而由**维度嬗变** `Lambda = M*exp(-1/(b g^2))`
  **内生**生成标度？

本文件的结论（见 `_demo` 与结论段）：
  **不能** —— 但原因是**结构性的、更深的**：定理 A 与定理 C **同源**。
  - 定理 A（严格，变分法）：拓扑项为全导数 ⇒ `dS/dg = 0` ⇒ **无局部效应**；
  - 无局部插入 ⇒ **不存在 `propto alpha` 的局部反项** ⇒ `beta_alpha ≡ 0` ⇒ 定理 C。
  故 **A ⟹ C**：打破 C **必须**先打破 A（放弃「`alpha` 为拓扑常数」）。

同时诚实记录：**维度嬗变本身是真机制**（本文件实跑展示它自 O(0.1) 耦合自然产生层级）
——它只是**需要**一个跑动耦合（`b g^2 != 0`），而该耦合在框架内**不存在**；
引入它 = 引入**非拓扑动力学自由度**（新场）= **外生输入**。

依赖 numpy；不引入新假设。
"""

import hashlib
import os
import sys

import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

M_PL_GEV = 1.2209e19        # 普朗克质量 [GeV]
V_EW_GEV = 246.0            # 电弱标度 [GeV]
LAMBDA_QCD_GEV = 0.2        # QCD 标度 [GeV]


# ----------------------------------------------------------------------
# 第 1 部分：定理 A ⟹ 定理 C 的**可跑演示**
#   一维玩具：S[phi] = int dtheta [ 0.5*(phi')^2 + alpha*phi' ]
#   - `alpha*phi'` 是**全导数**项（拓扑项的一维原型）；
#   - 严格结果：内部点的泛函导数 dS/dphi_i = -phi'' 与 alpha **无关**；
#   - 且周期性下 int phi' dtheta = 2*pi*n（拓扑量子化）。
#   => 无局部插入 => 无局部反项 => beta_alpha = 0。
# ----------------------------------------------------------------------
def action_1d(phi, h, alpha):
    d = np.diff(phi) / h
    return float(np.sum(0.5 * d ** 2 * h) + alpha * np.sum(d * h))


def numeric_local_grad(phi, h, alpha):
    """数值泛函导数 dS/dphi_i（中心差分）。"""
    eps = 1e-7
    g = np.zeros_like(phi)
    for i in range(len(phi)):
        p = phi.copy(); p[i] += eps
        m = phi.copy(); m[i] -= eps
        g[i] = (action_1d(p, h, alpha) - action_1d(m, h, alpha)) / (2 * eps)
    return g


def local_grad_1d(phi, h):
    """内部点离散泛函导数 `dS/dphi_k`。

    **注意：本函数没有 `alpha` 参数** —— 因为 `alpha` 项在内部点**精确相消**：
        dS/dphi_k = [(phi_k-phi_{k-1})/h + alpha] + [-(phi_{k+1}-phi_k)/h - alpha]
                  = (2phi_k - phi_{k-1} - phi_{k+1})/h      （alpha 完全消失）
    这正是「全导数项无局部效应」（定理 A）的离散形式。
    """
    g = np.zeros_like(phi)
    g[1:-1] = (2.0 * phi[1:-1] - phi[:-2] - phi[2:]) / h
    return g


def part1_A_implies_C():
    n_grid, n_wind, amp = 256, 1, 0.5
    h = 2.0 * np.pi / (n_grid - 1)
    theta = np.linspace(0.0, 2.0 * np.pi, n_grid)
    # phi 含非零曲率项（使局部泛函导数 O(1)，避免退化为机器噪声）
    phi = n_wind * theta + amp * np.sin(theta)

    g_ana = local_grad_1d(phi, h)                    # 解析（无 alpha 插槽）
    interior = slice(1, -1)
    scale = float(np.max(np.abs(g_ana[interior]))) or 1.0

    # 数值交叉核对：显式用两种 alpha 计算泛函导数
    g_num0 = numeric_local_grad(phi, h, 0.0)
    g_num10 = numeric_local_grad(phi, h, 10.0)
    dev_num = float(np.max(np.abs(g_num0[interior] - g_num10[interior])))
    dev_ana0 = float(np.max(np.abs(g_ana[interior] - g_num0[interior])))
    dev_ana10 = float(np.max(np.abs(g_ana[interior] - g_num10[interior])))

    S0, S10 = action_1d(phi, h, 0.0), action_1d(phi, h, 10.0)
    boundary = 10.0 * (phi[-1] - phi[0])

    return dict(scale=scale, dev_num=dev_num, dev_ana0=dev_ana0, dev_ana10=dev_ana10,
                rel_dev_num=dev_num / scale,
                S0=S0, S10=S10, boundary=boundary,
                topological_int=2.0 * np.pi * n_wind, amp=amp)


# ----------------------------------------------------------------------
# 第 2 部分：维度嬗变（真机制，但不是本框架的机制）
# ----------------------------------------------------------------------
def dim_transmutation(M, b_g2):
    """一阶维度嬗变：Lambda = M * exp(-1/(b g^2))。b_g2 = b*g^2。"""
    if b_g2 <= 0.0:
        return M            # beta = 0 ⇒ 无嬗变 ⇒ 标度 = 输入标度
    return M * np.exp(-1.0 / b_g2)


def required_bg2(M, Lambda):
    """要得到层级 M -> Lambda，所需的 *跑动量* b*g^2。"""
    return 1.0 / np.log(M / Lambda)


# ----------------------------------------------------------------------
# 第 3 部分：破坏 C 的「代价账」——必须放弃什么
# ----------------------------------------------------------------------
def cost_table():
    return [
        ("alpha 为拓扑常数系数", "保留", "若保留 ⇒ beta=0 ⇒ 无内生标度（定理 C）"),
        ("引入跑动耦合 g (beta!=0)", "必须", "g 乘**局部**算符 ⇒ 该项**非**拓扑"),
        ("引入动力学场 phi (dilaton/axion)", "必须", "phi 的势需新标度/新参数 ⇒ 外生输入"),
        ("『内生导出』这一宣称", "放弃", "所得标度由**新输入**（g 或 phi 的势）决定"),
    ]


def _demo():
    print("=" * 74)
    print("攻坚：H-TUFT 内生标度 —— 正面攻击定理 C")
    print("=" * 74)

    print("\n" + "-" * 74)
    print("[1] 定理 A ⟹ 定理 C 的可跑演示（一维玩具：全导数项无局部效应）")
    print("-" * 74)
    r = part1_A_implies_C()
    print("  S[phi] = int dtheta [ 0.5*(phi')^2 + alpha*phi' ] ,  phi = n*theta + %.1f*sin(theta)" % r["amp"])
    print("  解析泛函导数：dS/dphi_k = (2*phi_k - phi_{k-1} - phi_{k+1})/h  —— **式中无 alpha**")
    print("  内部点典型量级 max|dS/dphi_i| = %.4e（非退化）" % r["scale"])
    print("  数值交叉核对（显式用 alpha=0 与 alpha=10 各自计算）：")
    print("    两者内部点最大偏差 = %.3e   => 相对偏差 %.3e" % (r["dev_num"], r["rel_dev_num"]))
    print("    与解析式偏差：alpha=0 -> %.3e ; alpha=10 -> %.3e（中心差分精度）" % (
        r["dev_ana0"], r["dev_ana10"]))
    print("  => 内部点**精确不受 alpha 影响** —— 全导数项无局部效应（定理 A）。")
    print("  总作用量差 S(alpha=10)-S(alpha=0) = %.6f ；解析 |delta_alpha|*2*pi*n = %.6f" % (
        r["S10"] - r["S0"], r["boundary"]))
    print("  => alpha 只改变**边界/拓扑**量，不改变任何局部插入。")
    print("  => 无局部插入 ⇒ 无 **propto alpha 的局部反项** ⇒ beta_alpha = 0（定理 C）。")

    print("\n" + "-" * 74)
    print("[2] 维度嬗变是**真机制**（诚实：不抹功）")
    print("-" * 74)
    print("  Lambda = M * exp(-1/(b g^2)) ，M = M_Pl = %.3e GeV" % M_PL_GEV)
    print("  %-12s %-16s %s" % ("b*g^2", "Lambda (GeV)", "Lambda/M_Pl"))
    for bg2 in (0.0, 0.02, 0.05, 0.1, 0.2, 0.5):
        L = dim_transmutation(M_PL_GEV, bg2)
        print("  %-12.3f %-16.4e %.4e" % (bg2, L, L / M_PL_GEV))
    print("  => b*g^2 = 0（beta=0）时 Lambda = M_Pl ⇒ **无层级**（定理 C）。")
    print("  => b*g^2 ~ 0.1 时即得 ~1e-5 层级 ⇒ 机制**有效**，但**需要跑动**。")

    print("\n" + "-" * 74)
    print("[3] 得到真实层级所需的「跑动量」（= 需要的输入）")
    print("-" * 74)
    for name, L in (("v_EW", V_EW_GEV), ("Lambda_QCD", LAMBDA_QCD_GEV)):
        req = required_bg2(M_PL_GEV, L)
        print("  %-12s : Lambda/M_Pl = %.3e  =>  需 b*g^2 = %.4f  =>  g^2 = %.4f/b" % (
            name, L / M_PL_GEV, req, req))
    print("  => 需指定一个 **O(0.1) 的耦合值**（比 1e-17 自然，故机制值得用）。")
    print("  => 但若该系数是**拓扑**系数，则 b = 0，方程退化 ⇒ 在框架内**不可用**。")

    print("\n" + "-" * 74)
    print("[4] 破坏 C 的代价账（必须放弃什么）")
    print("-" * 74)
    for item, action, why in cost_table():
        print("  [%-4s] %-32s %s" % (action, item, why))

    print("\n" + "=" * 74)
    print("结论（攻坚结果）")
    print("=" * 74)
    print("  ① 定理 C **不能**被单独打破：打破它**必须**先放弃定理 A 的前提")
    print("     （『alpha 为拓扑不变量的常数系数』）。")
    print("  ② 故 A 与 C **同源**：拓扑 ⇒ 全导数 ⇒ 无局部效应 ⇒ 无局部反项 ⇒ beta=0。")
    print("  ③ 维度嬗变本身有效，但它需要**非拓扑的跑动耦合**；引入它 = 引入新场")
    print("     = **外生输入** ⇒ 『内生标度』这一宣称**失败**（但理论**可以**借外力成功）。")
    print("  ④ 唯一诚实出路：**承认外部锚定**（锚定不是罪，冒充『导出』才是）。")


def _selfhash():
    with open(os.path.abspath(__file__), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


if __name__ == "__main__":
    _demo()
    print("\n" + "-" * 74)
    print("本文件 SHA256 =", _selfhash())
    print("定位：攻坚/划界工具（非预言）。数学自洽 != 实验证实。")
