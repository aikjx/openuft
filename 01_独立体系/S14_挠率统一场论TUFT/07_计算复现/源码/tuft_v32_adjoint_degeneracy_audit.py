# -*- coding: utf-8 -*-
"""
================================================================================
TUFT V3.2  参数拟合分支审计 —— 伴随算子自伴性 + 简并代数结构 数值验证
================================================================================

针对"算法联盟最高权限｜TUFT V3.2 参数拟合后续分支"推导稿做三项机器核验：

  V1  伴随算子自伴性
       原稿写  F*[ψa] = -ψa'' + (2/r)ψa' -3V1 ψs²ψa + 5V2 ψs⁴ψa   （符号翻转）
       本核验在自然加权内积 <f,g>=∫f g 4πr²dr 下，直接检验线性化算子
             L = -d²/dr² - (2/r)d/dr + V(r)，  V(r)=-3V1ψs²+5V2ψs⁴
       是否满足 <L f,g> = <f,L g>（自伴 ⇒ 伴随算子即 L 本身）。
       同时检验原稿翻转版 L_flip = -d²/dr² + (2/r)d/dr + V 是否才是真伴随。
       结论判定：自伴 ⇔ |<Lf,g>-<f,Lg>| 机器零；翻转版 ⇔ |<Lf,g>-<f,L_flip g>| 机器零。

  V2  简并结构 —— (q0,ω0) 乘积分解简并
       观测量 Q0 = q0·ω0·N(ψs)， μ  = q0·ω0·Iμ(ψs)。
       证明 Q0、μ 仅依赖乘积 Π:=q0·ω0（独立于 q0/ω0 之比）。
       构造两对 (q0,ω0) 具有相同乘积但不同比值，展示 Q0、μ 完全相等
       ⇒ 一维连续简并存活于 (q0,ω0) 因子分解，任何仅作用于剖面 (V1,V2) 的
       约束（如 N=ℏ）都无法切断它。

  V3  分支B 的 N=ℏ 是否消除简并 / 是否过度约束剖面
       剖面方程计数：未知 V1,V2 仅 2 个；
       方程： M(V1,V2)=Me ； Iμ/N = μe/Qe ； N(V1,V2)=ℏ。
       3 个方程约束 2 个未知 ⇒ 过定（generic 无解）；且不触及 (q0,ω0) 之比。
       本项为代数计数，直接输出自由度审计。

红线声明：本脚本只做"算子代数/自由度结构"核验，不涉及对 TUFT 物理真实性的
任何主张；不对电子 g 因子等物理解读作判定。
================================================================================
"""
from __future__ import print_function
import os
import sys
import time
import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(HERE, "tuft_v32_adjoint_degeneracy_report.txt")


def _dump(out):
    text = "\n".join(out) + "\n"
    try:
        with open(REPORT_PATH, "w", encoding="utf-8") as fh:
            fh.write(text)
    except Exception as exc:
        out.append("[warn] 报告写入失败: %s" % exc)


def build_operator_matrices(r, psi, V1, V2):
    """在径向网格 r（不含 r=0，r>0）上离散化，返回：
       L     = -d²/dr² -(2/r)d/dr + V   （径向球 Laplacian 的负号，自伴形式）
       L_flip= -d²/dr² +(2/r)d/dr + V   （原稿翻转版候选伴随）
       加权内积权重 w = 4π r² dr
    """
    N = len(r)
    dr = r[1] - r[0]
    # 中心差分二阶导与一阶导（矩阵形式，边界用一阶/中心尽量平滑函数则自动可忽略）
    D1 = np.zeros((N, N))
    D2 = np.zeros((N, N))
    for i in range(N):
        if i > 0:
            D1[i, i - 1] = -1.0 / (2 * dr)
        if i < N - 1:
            D1[i, i + 1] = 1.0 / (2 * dr)
        if i > 0:
            D2[i, i - 1] = 1.0 / dr ** 2
        if i < N - 1:
            D2[i, i + 1] = 1.0 / dr ** 2
        if i > 0 and i < N - 1:
            D2[i, i] = -2.0 / dr ** 2
    # 边界行给 0（平滑测试函数在边界处数值可忽略），不参与统计
    V = -3 * V1 * psi ** 2 + 5 * V2 * psi ** 4
    inv_r = np.zeros(N)
    nz = r > 0
    inv_r[nz] = 1.0 / r[nz]
    L = -D2 - 2 * np.diag(inv_r) @ D1 + np.diag(V)
    L_flip = -D2 + 2 * np.diag(inv_r) @ D1 + np.diag(V)
    w = 4 * np.pi * r ** 2 * dr  # 权重向量（含 dr）
    return L, L_flip, w


def inner(f, g, w):
    return float(np.sum(f * g * w))


def test_adjoint(r, psi, V1, V2, seed=0):
    rng = np.random.default_rng(seed)
    out = []
    L, L_flip, w = build_operator_matrices(r, psi, V1, V2)
    # 多个随机平滑测试函数对
    max_self = 0.0
    max_flip = 0.0
    for trial in range(200):
        f = rng.standard_normal(len(r)) * np.exp(-r) * r ** 2   # 平滑且在边界衰减
        g = rng.standard_normal(len(r)) * np.exp(-r) * r ** 2
        A = inner(L @ f, g, w)            # <Lf,g>
        B = inner(f, L @ g, w)            # <f,Lg>   自伴判定
        C = inner(f, L_flip @ g, w)       # <f,L_flip g> 原稿翻转判定
        # 归一化到参考尺度
        ref = max(abs(A), abs(B), abs(C), 1e-30)
        max_self = max(max_self, abs(A - B) / ref)
        max_flip = max(max_flip, abs(A - C) / ref)
    out.append("  网格 N=%d  r∈[%.3g, %.3g]  dr=%.3g" % (len(r), r[0], r[-1], r[1] - r[0]))
    out.append("  随机测试函数对: 200 (平滑、边界指数衰减)")
    out.append("  max |<Lf,g> - <f,Lg>|/ref        = %.3e   (自伴：应≈机器零)" % max_self)
    out.append("  max |<Lf,g> - <f,L_flip g>|/ref  = %.3e   (原稿翻转版：应≈机器零才算真伴随)" % max_flip)
    if max_self < 1e-10 and max_flip > 1e-6:
        verdict = "PASS: L 在 4πr²dr 加权内积下为自伴 ⇒ 伴随方程应与正向线性化同算子（原稿 +2/r 翻转符号有误）"
    elif max_flip < 1e-10:
        verdict = "FAIL: 翻转版才是伴随（与本分析结论冲突，需复核）"
    else:
        verdict = "BOUNDARY: 内积/网格处理可能有问题，需复核"
    out.append("  判定: " + verdict)
    return out, max_self, max_flip


def test_product_factorization():
    """V2: 展示 Q0、μ 仅依赖乘积 Π=q0·ω0。"""
    out = []
    # 用一个平滑径向剖面代表 ψs（不必是真实孤子，仅验证观测量代数结构）
    r = np.linspace(1e-2, 6.0, 800)
    psi = np.exp(-r) * r ** 2
    N = float(np.trapezoid(4 * np.pi * r ** 2 * psi ** 2, r))
    I_mu = float(np.trapezoid(2 * np.pi * r ** 3 * psi ** 2, r))
    out.append("  取一平滑剖面 ψs∝r²e^{-r}，N=%.6e  Iμ=%.6e" % (N, I_mu))
    pairs = [(1.0, 2.0), (2.0, 1.0), (0.5, 4.0), (4.0, 0.5), (2.0, 1.0), (np.sqrt(2.0), np.sqrt(2.0))]
    out.append("  两对 (q0,ω0) 具有相同乘积 Π=2.0 但不同比值：")
    seen = {}
    for q, w_ in pairs:
        if q * w_ != 2.0:
            continue
        Q0 = q * w_ * N
        mu = q * w_ * I_mu
        key = (round(q, 4), round(w_, 4))
        if key in seen:
            continue
        seen[key] = True
        out.append("    (q0,ω0)=(%.4g,%.4g)  Π=%.3g  Q0=%.6e  μ=%.6e" % (q, w_, q * w_, Q0, mu))
    out.append("  ⇒ Q0、μ 完全相等（只随 Π 变化），(q0,ω0) 之比自由 ⇒ 一维因子分解简并")
    out.append("  判定: PASS（结构性：Q0=q0ω0N、μ=q0ω0Iμ 仅依赖乘积，与 q0/ω0 之比无关）")
    return out


def test_profile_equation_count():
    """V3: 剖面方程计数 —— 分支B 的 N=ℏ 是否过度约束。"""
    out = []
    out.append("  剖面未知数: V1, V2  （共 2 个）")
    out.append("  剖面约束方程: (1) M(V1,V2)=Me  (2) Iμ/N = μe/Qe  (3) N(V1,V2)=ℏ")
    out.append("  方程数 3 > 未知数 2 ⇒ 过定（generic 无解；有解亦是孤立点）")
    out.append("  (q0,ω0): Q0=q0ω0N、μ=q0ω0Iμ 仅定乘积 Π=Qe/N(或 μe/Iμ)，比值 q0/ω0 不受任何目标约束")
    out.append("  判定: PASS（自由度审计：简并存活于 (q0,ω0) 之比，N=ℏ 不消除；分支B 目标是唯一化剖面而非消除简并）")
    return out


def main():
    t0 = time.time()
    out = []
    out.append("TUFT V3.2 分支审计 · 伴随算子自伴性 + 简并结构 数值核验")
    out.append("运行时间: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    out.append("Python %s  numpy %s" % (sys.version.split()[0], np.__version__))
    out.append("")

    # ---- V1 伴随算子自伴性 ----
    out.append("=== V1 伴随算子自伴性核验 ===")
    r = np.linspace(1e-2, 8.0, 2000)
    psi = np.exp(-r) * r ** 2.0          # 测试径向剖面（平滑）
    V1c, V2c = 1.0, 1.0
    v1out, _, _ = test_adjoint(r, psi, V1c, V2c, seed=7)
    out.extend(v1out)
    out.append("")

    # ---- V2 乘积分解简并 ----
    out.append("=== V2 (q0,ω0) 乘积分解简并 ===")
    out.extend(test_product_factorization())
    out.append("")

    # ---- V3 剖面方程计数 ----
    out.append("=== V3 分支B N=ℏ 约束的自由度审计 ===")
    out.extend(test_profile_equation_count())
    out.append("")

    out.append("运行耗时 %.1f s" % (time.time() - t0))
    out.append("红线声明：仅核验算子代数与自由度结构；不构成对 TUFT 物理真实性主张。")
    print("\n".join(out))
    _dump(out)


if __name__ == "__main__":
    main()
