# -*- coding: utf-8 -*-
"""
TUFT 卷二十四 · 奇点消解与黑洞内禀几何（OPEN_v1）· 诚实演示
====================================================
诚实边界声明（红线：数学自洽 != 实验证实；本卷为理论探索提案，
其"TUFT 正则化黑洞已被/可被观测支持、已解决信息悖论"的结论被既有事实
推翻或从未成立，见 §0 勘误）：

  * 据 2026-09-30 更正（记忆 ID 84665624），卷二十三通道 3（黑洞 ringdown
    QNM 频移 / σ_abs=0 反射壁）**已关闭**：OPEN_v3 χ²=33.00(df=2)、
    p=6.83e-8、联合排除 5.74σ；OPEN_v4 显示 TUFT 的 σ_abs=0 反射壁所需
    r_s=2.05M 与 TUFT 自身三尺度（K_sat/康普顿/挠率）差 26.0~26.5 个量级，
    挠率宏观不可用（R6 差 1e28）⇒ 该 L3 窗口已关闭。
    ⇒ 本卷反复引用的"TUFT 黑洞 QNM 频移已被/可由 LIGO ringdown 检验"
      **这一经验支柱已倒**；本卷不声称 TUFT 黑洞与 LIGO 数据吻合。

  * 挠率自耦合 ODE（dR/dr ∝ R − λτ²R，"λτ²>1 截断曲率"）是**唯象 ansatz**，
    并非从 TUFT 作用量变分导出；草稿代码存在内部不一致
    （d2A 在使用前未定义、R 公式引用 d2A、R_eff 与 R 公式不自洽）。
    ⇒ 本卷"曲率被封顶在普朗克量级"是**把结论写进假设**（deus ex machina），
      未对任何 TUFT 第一性原理构成推导。

  * "挠率场承载量子相位信息、保证幺正性"是**断言，无机制、无计算**；
    本卷不声称已实现信息悖论的严格解决。

  * 草稿把"FDTD+RK4 恒星坍缩仿真"写成玩具径向 ODE，且非 FDTD；
    本卷不声称完成了真实坍缩流体动力学仿真。

  * 草稿的"所有扰动模 Re>0 稳定"是**断言，未计算**；本卷用真实（玩具级）
    线性扰动演化替代，并如实报告是否稳定（且明确它非完整 Regge-Wheeler 证明）。

  * 环境：jax/dynesty 未安装。本卷用 numpy + scipy 重写（可运行），
    与卷二十三一致；不依赖 jax。

诚实建模选择（本代码实际采用）：
  数学上"挠率正则化黑洞"等价于已知的 **Hayward 型正则黑洞**
  （结构函数 m(r)=M r³/(r³+g³)），其曲率有界是该结构函数的定义性质，
  **不是 TUFT 推导结果**。本卷把 g 解读为"由挠率 τ 提供的紫外截断尺度"，
  并明确这是**解读而非预言**——TUFT 未给出 g 与 FRG 参数池的任何约束关系。
  因此本代码演示的是"正则黑洞这一数学可能性"，而非"TUFT 预言"。
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import numpy as np
import hashlib
import json


# ========== Hayward 型正则黑洞（本卷解读为"挠率正则化"） ==========
def hayward_metric(r, M, g):
    """结构函数 m(r)=M r^3/(r^3+g^3)。
    g=0 ⇒ 施瓦西（中心奇点）；g>0 ⇒ 正则（中心 A(0)=1，无奇点）。"""
    r = np.asarray(r, dtype=float)
    r3 = r ** 3
    g3 = g ** 3
    m = M * r3 / (r3 + g3)
    A = 1.0 - 2.0 * m / r
    # 安全除法：内视界处 A 可能过零，避免 1/0 警告/inf 污染下游
    B = np.divide(1.0, A, out=np.full_like(A, np.inf), where=np.abs(A) > 1e-300)
    return A, B, m


def torsion_profile(r, g, tau_core):
    """挠率孤子：核心区峰值，外部随 1/r^3 衰减至 0。
    本卷把它解读为 TUFT 挠率场；其幅度 tau_core 是自由参数，未被 TUFT 约束。"""
    r = np.asarray(r, dtype=float)
    g3 = g ** 3
    return tau_core * g3 / (r ** 3 + g3)


def regularity_scan(M=1.0, g=0.5):
    """对比 g>0（正则）与 g=0（施瓦西，奇点）。
    返回逐点 (r, A_reg, B_reg, A_sch)。中心规则性由 A(0+) 是否有限判定。"""
    rows = []
    for r in [1e-4, 1e-3, 1e-2, 0.1, 1.0, 2.0, 5.0, 10.0]:
        A_reg, B_reg, _ = hayward_metric(r, M, g)
        A_sch, _, _ = hayward_metric(r, M, 0.0)
        rows.append((float(r), float(A_reg), float(B_reg), float(A_sch)))
    return rows


# ========== 玩具级径向扰动稳定性（非完整 Regge-Wheeler 证明） ==========
def perturb_toy(M=1.0, g=0.5, ng=400, rmax=20.0, nt=2000, dt=0.02):
    """一维径向标量扰动演化（leapfrog）。在规则背景上放置高斯扰动，
    报告末态最大振幅相对初态是否衰减（稳定指示）。
    明确：这是玩具级方法，证明的是"规则背景上扰动可松弛"，
    不是黑洞模式的严格线性稳定性证明（TUFT 未提供后者）。"""
    r = np.linspace(1e-3, rmax, ng)
    dr = r[1] - r[0]
    A, B, _ = hayward_metric(r, M, g)
    # 径向传播速度 c^2 = 1/B = A；直接取 A 并裁剪，避免内视界 A≈0 处 inf/nan
    c2 = np.clip(A, 1e-6, None)
    psi = np.exp(-((r - 5.0) ** 2) / (2 * 0.5 ** 2))  # 初始高斯扰动
    psi_old = psi.copy()
    psi_new = psi.copy()
    amp0 = float(np.max(np.abs(psi)))
    for _ in range(nt):
        d2psi = np.zeros_like(psi)
        d2psi[1:-1] = (psi[2:] - 2 * psi[1:-1] + psi[:-2]) / dr ** 2
        lap = c2 * d2psi
        psi_new = 2 * psi - psi_old + dt ** 2 * lap
        psi_new[0] = psi_new[1]          # 内边界（核心）近似吸收/反射
        psi_new[-1] = psi_new[-2]        # 外边界近似吸收
        psi_old, psi = psi, psi_new
    amp_end = float(np.max(np.abs(psi)))
    relaxed = bool(amp_end < amp0)
    return amp0, amp_end, relaxed


# ========== 后验审计 + SHA256 ==========
def audit(params, results):
    blob = json.dumps({"params": params, "results": results}, sort_keys=True).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


# ========== 主入口 ==========
def _demo():
    print("=" * 70)
    print("TUFT 卷二十四 · 奇点消解与黑洞内禀几何（OPEN_v1）· 诚实演示")
    print("=" * 70)
    print("诚实前提：本代码演示的是『正则黑洞（Hayward 型）』的数学可能性，")
    print("将其『解读』为挠率正则化；TUFT 未从第一性导出该结构，")
    print("且其经验支柱（LIGO ringdown QNM 频移）已于 2026-09-30 被排除。")
    print("-" * 70)

    M, g, tau_core = 1.0, 0.5, 1.0
    print("[1] 规则性扫描（M=%g, g=%g, τ_core=%g）" % (M, g, tau_core))
    rows = regularity_scan(M, g)
    for r, A_reg, B_reg, A_sch in rows:
        print("    r=%.4g  A_reg=%.6g  B_reg=%.6g  A_施瓦西=%.6g"
              % (r, A_reg, B_reg, A_sch))
    A0_reg = hayward_metric(1e-6, M, g)[0]
    A0_sch = hayward_metric(1e-6, M, 0.0)[0]
    print("    ⇒ 中心 A(0+): 正则=%.6g（有限，无奇点） vs 施瓦西=%.6g（发散）"
          % (A0_reg, A0_sch))
    print("    ⇒ 曲率有界性是 Hayward 类的已知解析性质（Kretschmann 有界），")
    print("      本代码不重复数值计算该有界值，以免引入未经核验的曲率公式。")

    print("-" * 70)
    print("[2] 挠率孤子剖面（解读为 TUFT 挠率场，τ_core 自由、未被 TUFT 约束）")
    rr = np.logspace(-3, 1.5, 8)
    for rv in rr:
        print("    r=%.4g  τ(r)=%.6g" % (rv, torsion_profile(rv, g, tau_core)))
    print("    ⇒ τ(r) 在核心峰值、外部 1/r^3 衰减至 0，整体有界。")

    print("-" * 70)
    print("[3] 玩具级径向扰动稳定性（leapfrog，ng=400, nt=2000）")
    amp0, amp_end, relaxed = perturb_toy(M, g)
    print("    初态最大振幅=%.6g，末态最大振幅=%.6g，振幅减小=%.6g"
          % (amp0, amp_end, amp0 - amp_end))
    print("    ⚠ 本玩具用反射边界，能量守恒（不衰减），故不能据此判定稳定；")
    print("      严格黑洞线性稳定性需 Regge-Wheeler / 拟正则模分析，TUFT 未提供。")

    print("-" * 70)
    print("[4] 诚实结论")
    print("    (a) 正则黑洞（曲率有界、无中心奇点）在数学上成立——")
    print("        但这是 Hayward 类结构的通性，非 TUFT 独有预言。")
    print("    (b) TUFT 未从作用量变分导出 g 与 τ 的关系，g/τ_core 是自由参数。")
    print("    (c) 本卷经验支柱（LIGO ringdown QNM 频移）已关闭(2026-09-30)，")
    print("        故『TUFT 黑洞被观测支持』不成立。")
    print("    (d) 信息悖论『几何幺正性解决』是断言，无机制无计算，未闭合。")
    print("    (e) CUR-08 以 ⏳待检验 登记，并写入上述诚实边界。")
    payload = dict(
        M=M, g=g, tau_core=tau_core,
        A_center_regular=float(A0_reg), A_center_schwarzschild=float(A0_sch),
        perturb_amp0=amp0, perturb_amp_end=amp_end, perturb_relaxed=relaxed,
    )
    print("    SHA256(参数+结果摘要)=%s" % audit(dict(M=M, g=g, tau_core=tau_core),
                                                  payload))
    print("=" * 70)


if __name__ == "__main__":
    _demo()
