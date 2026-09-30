# -*- coding: utf-8 -*-
"""
tuft_htuft_cosmic_string_v1.py
==============================

H-TUFT 螺旋宇宙弦随机引力波背景（SGWB）求解器 —— **脚手架（非预言）**

红线（与卷二十七 §0 一致，守 TUFT「数学自洽 ≠ 实验证实」）：
- 原稿 §11 使用 `jax`（本机不可用）；本文件用 numpy 复刻，语义等价。
- 原稿的 Ω_GW 是**单一幂律参数化**：n_gw = 0.5 + α_t·Q_hel，α_t=0.04 是**自由参数**，
  谱指数偏移**没有**第一性来源；手征分量前置因子 0.06 同样是**任意常数**。
- 标准宇宙弦 SGWB 的谱形来自弦网络模拟（BOS/VDOS 类），其特征是「上升-峰值-截断」，
  **不是**原稿的纯幂律。本文件用 `omega_gw_shape_ref` 给出**示意**峰形做对照，
  但明确声明：真实谱须引用具体模拟，本示意不可作为物理曲线使用。
- 本文件**不声称**产生任何可检验预言；输出的 Ω_GW、手征幅值均为**人为量级**，
  不能与 PTA/LISA/CMB-S4 灵敏度直接比对。

依赖 numpy；不引入新假设。
"""

import hashlib
import os
import sys

import numpy as np

try:  # Windows GBK 控制台防 UnicodeEncodeError
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


# ----------------------------------------------------------------------
# 1) 原稿（卷二十七 §11）唯象参数化：单一幂律 + 高斯「手征」包
# ----------------------------------------------------------------------
def omega_gw_phenom(f, f_star, A_gw, Q_hel, alpha_t):
    """原稿唯象式。

    n_gw = 0.5 + alpha_t * Q_hel     # 谱指数由自由参数 alpha_t 决定（未导出）
    Omega = A_gw * (f/f_star)**n_gw  # 纯幂律（无平台、无截断）
    chi   = 0.06 * Q_hel * A_gw * exp(-(f/f_star - 1)**2)  # 0.06 任意常数
    """
    n_gw = 0.5 + alpha_t * Q_hel
    omega = A_gw * (f / f_star) ** n_gw
    chi = 0.06 * Q_hel * A_gw * np.exp(-((f / f_star - 1.0) ** 2))
    return omega, chi, n_gw


# ----------------------------------------------------------------------
# 2) 参照：宇宙弦 SGWB 的「上升-峰值-截断」示意峰形（非具体模拟）
# ----------------------------------------------------------------------
def omega_gw_shape_ref(f, f_star, A_gw, p_rise=3.0):
    """示意性 peak 模板：f<<f* 上升 ~ x^p_rise；f>>f* 衰减 ~ x^-1。

    声明：真实宇宙弦 SGWB 谱须由网络模拟给出，本式仅用于**对照形状**，
    说明原稿「纯幂律」缺少特征峰/截断，**不得**作为物理曲线引用。
    """
    x = f / f_star
    return A_gw * x ** p_rise / (1.0 + x ** (p_rise + 1.0))


# ----------------------------------------------------------------------
# 3) BBN 能量注入的**量级**粗检（示意上限，非精确约束）
# ----------------------------------------------------------------------
def bbn_gw_density_check(f, omega, bound=1.0e-5):
    """对 Ω_GW(f) 做 ∫ dln f 得到总引力波能量密度占比，与量级上限比较。

    bound=1e-5 是文献常用的**数量级**近似上限（ΔN_eff/Ω_GW h² 类约束的量级），
    此处仅作「是否显然越界」的量级检查，不构成精确 BBN 计算。
    """
    lnf = np.log(f)
    total = np.trapezoid(omega, lnf) if hasattr(np, "trapezoid") else np.trapz(omega, lnf)
    return total, total / bound


def sha256_of_this_file():
    path = os.path.abspath(__file__)
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def _demo():
    print("=" * 76)
    print("H-TUFT 螺旋宇宙弦 SGWB 引擎 · 脚手架实跑（非预言）")
    print("红线：数学自洽 ≠ 实验证实；谱指数/手征幅值均为人为参数")
    print("=" * 76)

    # 原稿常量（卷二十七 §11）
    f_star = 1.0e-9      # 特征频率 nHz
    A_gw = 1.2e-10       # 人为幅度
    alpha_t = 0.04       # 自由参数
    f_vals = np.logspace(-10, -7, 200)

    print("[A] 原稿参数化输出（Q_hel = 1,2,3）")
    for Q in (1, 2, 3):
        omega, chi, n_gw = omega_gw_phenom(f_vals, f_star, A_gw, Q, alpha_t)
        print(
            "    Q_hel=%d  n_gw=%.3f  最大Omega_GW=%.3e  手征分量峰值=%.3e"
            % (Q, n_gw, np.max(omega), np.max(np.abs(chi)))
        )

    print("[B] 谱指数来源审计：n_gw 完全由自由参数 alpha_t 决定")
    for at in (0.00, 0.04, 0.20):
        print(
            "    alpha_t=%.2f -> n_gw(Q=1,2,3) = %.3f, %.3f, %.3f"
            % (at, 0.5 + at * 1, 0.5 + at * 2, 0.5 + at * 3)
        )
    print("    注：alpha_t=0 即退化为普通宇宙弦的常数谱指数 0.5；偏移无第一性来源。")

    print("[C] 手征分量幅值审计：chi ~ 0.06 * Q_hel * A_gw（0.06 任意，无推导）")
    for Q in (1, 2, 3):
        _, chi, _ = omega_gw_phenom(np.array([f_star]), f_star, A_gw, Q, alpha_t)
        print("    Q_hel=%d -> chi(f=f*)/A_gw = %.3f" % (Q, abs(chi[0]) / A_gw))

    print("[D] 形状对照：原稿纯幂律 vs 宇宙弦 SGWB 参照峰形（示意）")
    omega_ph, _, _ = omega_gw_phenom(f_vals, f_star, A_gw, 1, alpha_t)
    omega_ref = omega_gw_shape_ref(f_vals, f_star, A_gw)
    arg_ph, arg_ref = int(np.argmax(omega_ph)), int(np.argmax(omega_ref))
    print("    原稿峰值 @ f/f* = %.3e（落在区间端点=单调幂律，无内禀峰）"
          % (f_vals[arg_ph] / f_star))
    print("    参照峰值 @ f/f* = %.3e（内禀峰，有截断）"
          % (f_vals[arg_ref] / f_star))
    print("    => 原稿「谱指数随 Q_hel 分段偏移」不改变『无峰无截断』的事实。")

    print("[E] BBN 量级粗检（示意上限 1e-5，非精确约束）")
    omega_ph1, _, _ = omega_gw_phenom(f_vals, f_star, A_gw, 1, alpha_t)
    total, ratio = bbn_gw_density_check(f_vals, omega_ph1)
    print("    总 Omega_GW ~ %.3e  ;  ratio/bound = %.3e" % (total, ratio))
    print("    注：A_gw 是人为小量，故『通过』BBN 不构成预言——它是参数选择的结果。")

    print("-" * 76)
    print("诚实结论：引擎输出 = 可调参数驱动的量级，不携带可检验物理量；")
    print("          手征偏振、谱指数偏移均缺机制，须先补『弦网络模拟 + 手征来源』。")
    print("script SHA256 = %s" % sha256_of_this_file())


if __name__ == "__main__":
    _demo()
