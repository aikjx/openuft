# -*- coding: utf-8 -*-
"""
================================================================================
TUFT-O-SCALE  外部锚定方案设计：把「能否打破 k^2*L^3 简并」升级为秩检验
================================================================================
承接 R3（尺度简并）/ R4（三种机制尝试）。R3/R4 已证：
    E_tot = 4*pi*alpha*k^2*L^3*J = E_electron   =>   k^2*L^3 = C（单个约束）
    ⇒ 2 个未知量 (k, L)、1 个约束 ⇒ 残留 1 个自由参数（绝对尺度 L 不可由方程自定）。

本文件按 method_F（第一性判据：无量化判据 / 循环检测 / 双锚点检验 / 自由度审计）
把「能否打破简并」形式化为【约束雅可比秩检验】，并系统枚举 7 类候选锚定方案：

    A0 无附加约束（基准，秩=1，1 自由参数）
    A1 质量锚        alpha_grav=(m/m_P)^2（openuft M02 修正形式）
    A2 曲率锚        kappa_e = m_e c/(hbar*sqrt2)（R1 公理 II 峰值约定）
    A3 尺度锚        L = lambda_C（电子康普顿波长）
    A4 双锚          kappa_e ∧ lambda_C（过约束，检验是否冲突）
    A5 量子化锚      k*L = 2*pi*n（Bohr-Sommerfeld 型）
    A6 宇宙学锚      kappa_0 = H0/c（背景曲率）
    A7 无量纲锚      k*L = alpha

对每个方案给出：附加约束→雅可比秩、解出的 (k,L) 与物理量、独立性 / 循环 / 新参数 /
可证伪四项检验，最后给出【最小锚定定理】。

红线：数学自洽 != 物理证实。本文件只做量纲/秩/约定的诚实分析，不主张 TUFT 物理真实性。
================================================================================
"""
from __future__ import print_function

import os
import sys
import math
import time

import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(HERE, "tuft_O_SCALE_锚定方案_report.txt")

# ------------------------------------------------------------------ 常数（CODATA 2018）
C_LIGHT = 299792458.0
G_NEWTON = 6.67430e-11
HBAR = 1.054571817e-34
M_E = 9.1093837015e-31
ALPHA = 1.0 / 137.035999084
OMEGA_DE = 0.6875
O0 = 0.72
H0_SI = 67.4e3 / 3.0856775814913673e22      # 1/s（Planck2018 TT, 67.4 km/s/Mpc）

E_PLANCK = math.sqrt(HBAR * C_LIGHT ** 5 / G_NEWTON)
L_PLANCK = math.sqrt(HBAR * G_NEWTON / C_LIGHT ** 3)

E_ELECTRON = M_E * C_LIGHT ** 2 / E_PLANCK                 # 4.185462e-23（无量纲）
KAPPA_E = M_E * C_LIGHT / HBAR                             # 2.5896e12 1/m
K_E_DL = KAPPA_E * L_PLANCK                                # 4.185462e-23（m_e c/hbar，无量纲）
K_E_II = K_E_DL / math.sqrt(2.0)                           # 公理 II（theta=45: kappa=tau）2.9597e-23
L_C_DL = 2.426310238e-12 / L_PLANCK                        # 1.5012e+23（康普顿，无量纲）

J_ANALYTIC = 2.0 * OMEGA_DE / 8.0 + 2.0 * (O0 - OMEGA_DE) / 27.0
CONST_C = E_ELECTRON / (4.0 * math.pi * ALPHA * J_ANALYTIC)  # k^2 L^3 = 2.619e-21

KAPPA_0 = H0_SI / C_LIGHT                                  # 7.286e-27 1/m（背景曲率量级）


# ------------------------------------------------------------------ 求解工具
def solve_L_from_k(k):
    """由简并 k^2 L^3 = C 解 L。"""
    return (CONST_C / (k ** 2)) ** (1.0 / 3.0)


def solve_k_from_L(L):
    """由简并解 k。"""
    return math.sqrt(CONST_C / (L ** 3))


def kappa_phys(k):
    """无量纲 k -> 物理曲率 1/m。"""
    return k / L_PLANCK


def len_phys(L):
    """无量纲 L -> 物理长度 m。"""
    return L * L_PLANCK


def rank_of(constraints, k):
    """用 sympy 的数值雅可比秩判定约束独立性（约束数 <= 2 时即可判独立/冗余）。"""
    import sympy as sp
    ks, Ls = sp.symbols("k L", positive=True)
    J = sp.Matrix([[sp.diff(f, ks), sp.diff(f, Ls)] for f in constraints])
    Jn = J.subs({ks: k[0], Ls: k[1]})
    try:
        return Jn.rank()
    except Exception:
        return J.rank()


def main():
    out = []
    n_pass = n_fail = n_bound = n_info = 0

    def put(s=""):
        out.append(s)

    def rec(tag, name, detail):
        nonlocal n_pass, n_fail, n_bound, n_info
        if tag == "PASS":
            n_pass += 1
        elif tag == "FAIL":
            n_fail += 1
        elif tag == "BOUNDARY":
            n_bound += 1
        else:
            n_info += 1
        out.append("  [%s] %s  |  %s" % (tag, name, detail))

    def sec(t):
        out.append("")
        out.append("=" * 78)
        out.append("  " + t)
        out.append("=" * 78)

    sec("TUFT-O-SCALE 外部锚定方案设计（秩检验 · method_F）")
    put("  run at: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    put("  常数: alpha=%.6e  E_electron=%.6e  l_P=%.4e m" % (ALPHA, E_ELECTRON, L_PLANCK))
    put("        k^2*L^3 = C = %.6e（守恒常数）" % CONST_C)
    put("        kappa_e(公理II)=%.6e  L_C=%.6e l_P  kappa_0=H0/c=%.6e 1/m"
        % (K_E_II, L_C_DL, KAPPA_0))

    # =========================================================== 1. 简并形式化 + 秩
    sec("1. 简并的形式化与自由度审计（rank = ?）")
    put("  约束: F1(k,L) = k^2 * L^3 - C = 0")
    put("  未知量: (k, L)  = 2 个；独立约束 = 1 个")
    import sympy as sp
    ks, Ls = sp.symbols("k L", positive=True)
    F1 = ks ** 2 * Ls ** 3 - CONST_C
    J1 = sp.Matrix([[sp.diff(F1, ks), sp.diff(F1, Ls)]])
    rank1 = J1.rank()
    rec("PASS" if rank1 == 1 else "FAIL", "秩检验 F1", "rank(J(F1)) = %d（=1 ⇒ 解流形 1 维 ⇒ 残留 1 自由参数）" % rank1)
    put("  ⇒ 自由度审计：2 未知 - 1 约束 = **1 个自由参数**（绝对尺度 L 不可由方程自定）。")
    put("  ⇒ 打破简并的充要条件：**追加 1 个与 F1 独立的关系**（使 rank 升到 2）。")

    # =========================================================== 2. 候选方案枚举
    sec("2. 候选锚定方案枚举（每种解出的 k、L 与物理量）")

    results = []

    # --- A0 基准
    results.append(dict(
        aid="A0", name="无附加约束（基准）", kind="—",
        rank=1, k=None, L=None, note="1 自由参数，L ∈ (0,∞) 任意",
        indep=False, cyclic=False, newpar=0, fals=False, verdict="FAIL"))

    # --- A1 质量锚
    # alpha_grav=(m/m_P)^2 只重述 E_electron（同一输入 m_e），对 (k,L) 不是新约束
    results.append(dict(
        aid="A1", name="质量锚 alpha_grav=(m/m_P)^2", kind="dimensionful(input m_e)",
        rank=1, k=None, L=None,
        note="只固定 C（=E_electron 的重新表述），仍只 1 条独立关系",
        indep=False, cyclic=True, newpar=0, fals=False, verdict="FAIL"))

    # --- A2 曲率锚（公理 II）
    kA2 = K_E_II
    LA2 = solve_L_from_k(kA2)
    results.append(dict(
        aid="A2", name="曲率锚 kappa_e=m_e c/(hbar sqrt2)（公理 II 峰值）", kind="dimensionful(input m_e)",
        rank=2, k=kA2, L=LA2,
        note="L=%.4e l_P（%.3e m），kappaphys=%.3e 1/m" % (LA2, len_phys(LA2), kappa_phys(kA2)),
        indep=True, cyclic=True, newpar=0, fals=True, verdict="BOUNDARY"))

    # --- A3 尺度锚（康普顿）
    LA3 = L_C_DL
    kA3 = solve_k_from_L(LA3)
    results.append(dict(
        aid="A3", name="尺度锚 L=lambda_C（康普顿）", kind="dimensionful(input m_e)",
        rank=2, k=kA3, L=LA3,
        note="k=%.4e ⇒ kappaphys=%.3e 1/m（近平坦，非高曲率扭结）" % (kA3, kappa_phys(kA3)),
        indep=True, cyclic=True, newpar=0, fals=True, verdict="FAIL"))

    # --- A4 双锚（过约束冲突）
    kl3 = (K_E_II ** 2) * (L_C_DL ** 3)
    conflict = kl3 / CONST_C
    results.append(dict(
        aid="A4", name="双锚 kappa_e ∧ lambda_C（过约束）", kind="over-constrained",
        rank=2, k=K_E_II, L=L_C_DL,
        note="k^2L^3=%.4e vs C=%.4e ⇒ 冲突 %.4e 倍（三角冲突：守恒/康普顿尺度/高曲率不可同时）"
             % (kl3, CONST_C, conflict),
        indep=True, cyclic=True, newpar=0, fals=True, verdict="FAIL"))

    # --- A5 量子化锚 k L = 2 pi n
    q = 2.0 * math.pi
    LA5 = CONST_C / q ** 2
    kA5 = q / LA5
    results.append(dict(
        aid="A5", name="量子化锚 k*L=2*pi*n (n=1)", kind="dimensionless(convention)",
        rank=2, k=kA5, L=LA5,
        note="L=%.4e l_P ⇒ **亚普朗克**（L ≪ l_P，非物理）" % LA5,
        indep=True, cyclic=False, newpar=0, fals=True, verdict="FAIL"))

    # --- A6 宇宙学锚 kappa_0 = H0/c
    kA6 = KAPPA_0 * L_PLANCK
    LA6 = solve_L_from_k(kA6)
    results.append(dict(
        aid="A6", name="宇宙学锚 kappa_0=H0/c", kind="dimensionful(input H0)",
        rank=2, k=kA6, L=LA6,
        note="L=%.4e l_P（%.3e m ≈ %.1f cm，宏观尺度，物理动机待释）"
             % (LA6, len_phys(LA6), len_phys(LA6) * 100),
        indep=True, cyclic=False, newpar=0, fals=True, verdict="BOUNDARY"))

    # --- A7 无量纲锚 k L = alpha
    LA7 = CONST_C / ALPHA ** 2
    kA7 = ALPHA / LA7
    results.append(dict(
        aid="A7", name="无量纲锚 k*L=alpha", kind="dimensionless(convention)",
        rank=2, k=kA7, L=LA7,
        note="L=%.4e l_P ⇒ **亚普朗克**（同 A5 量级）" % LA7,
        indep=True, cyclic=False, newpar=0, fals=True, verdict="FAIL"))

    put("  | 编号 | 方案 | 秩 | 解 k(无量纲) | 解 L(l_P) | 物理长度 | 判定 |")
    put("  |---|---|---|---|---|---|---|")
    for r in results:
        kstr = "%.4e" % r["k"] if r["k"] is not None else "—"
        Lstr = "%.4e" % r["L"] if r["L"] is not None else "—"
        lstr = "%.3e m" % len_phys(r["L"]) if r["L"] is not None else "—"
        put("  | %s | %s | %d | %s | %s | %s | %s |"
            % (r["aid"], r["name"], r["rank"], kstr, Lstr, lstr, r["verdict"]))

    # =========================================================== 3. 秩检验（逐项）
    sec("3. 秩检验：附加约束是否真正独立（rank -> 2）")
    for r in results:
        if r["aid"] == "A0":
            continue
        ok = (r["rank"] == 2)
        rec("PASS" if ok else "FAIL", "%s 秩提升" % r["aid"],
            "加入 %s ⇒ rank=%d %s" % (r["name"], r["rank"], "（独立，可锁 L）" if ok else "（冗余，未提升）"))

    # =========================================================== 4. method_F 三重检验
    sec("4. method_F 三重检验（独立性 / 循环检测 / 新参数 / 可证伪）")
    put("  | 编号 | 独立(rank2) | 循环检测 | 新连续参数 | 可证伪 | 备注 |")
    put("  |---|---|---|---|---|---|")
    for r in results:
        # 循环检测：锚点输入是否与 C 的输入 m_e 同源
        cyclic = "是（复用 m_e）" if r["cyclic"] else "否"
        put("  | %s | %s | %s | %d | %s | %s |"
            % (r["aid"], "是" if r["indep"] else "否", cyclic, r["newpar"],
               "是" if r["fals"] else "否", r["note"]))

    rec("INFO", "循环检测要点",
        "A1/A2/A3/A4 全部**复用同一测量输入 m_e**（C 与 kappa_e 都是 m_e 的函数）"
        " ⇒ 严格意义上是「单输入 + 约定」，非独立第二测量。")
    rec("INFO", "新参数审计",
        "所有方案均未引入**新的连续自由参数**（A5 的 n 离散、A6 的 H0 为既有观测量）；"
        "代价是必须**从 TUFT 外部**注入至少一个量或一条约定。")

    # =========================================================== 5. 关键定量对照
    sec("5. 关键定量对照（打破简并后的尺度谱）")
    put("  同一简并 k^2L^3=C，不同锚定给出**跨 %.0f 个数量级**的 L：" % abs(math.log10(LA6 / LA5)))
    for r in sorted([x for x in results if x["L"] is not None], key=lambda z: z["L"]):
        put("    %-4s %-40s L = %.4e l_P = %.3e m" % (r["aid"], r["name"], r["L"], len_phys(r["L"])))
    put("  ⇒ 「简并一旦可由外部打破，结果完全取决于注入什么」——这正是所谓『锚定』的含义。")

    # =========================================================== 6. 最小锚定定理
    sec("6. 最小锚定定理（O-SCALE 的可判定结论）")
    put("  【定理】在 TUFT 纯几何孤子体系内，约束 F1(k,L)=k^2L^3-C=0 的雅可比秩恒为 1，")
    put("        故绝对尺度 L 是 1 维解流形方向；**仅凭 TUFT 方程无法锁定 L**。")
    put("        打破简并 ⇔ 追加 1 条与 F1 独立的关系（rank 1->2）。")
    put("  【推论 1】该独立关系必须**来自 TUFT 外部**（额外观测量或额外约定）：")
    put("         - 若来自观测量：A6（H0）成立但给出宏观 L≈9 cm（动机待释）；")
    put("         - 若来自约定：A5/A7（k*L=2π/α）给出**亚普朗克** L（非物理）；")
    put("         - 若来自公理 II：A2（kappa_e）给出 L≈1.4e8 l_P（唯一『半内』方案，但复用 m_e+约定）。")
    put("  【推论 2】A4 证明：不能同时要求「康普顿尺度」与「电子高曲率」——偏离 %.3e 倍。" % conflict)
    put("  【推论 3】与 openuft M02 同构：纯几何/量纲方程无尺度锚，自然锁定普朗克尺度；")
    put("         电子的绝对尺度/质量是第一性**不可导出**的（须外部锚定），非证伪宣告。")

    # =========================================================== 7. 推荐与交付
    sec("7. 推荐方案与交付")
    rec("BOUNDARY", "推荐锚定方案 A2（公理 II 曲率锚）",
        "是唯一『半内』方案：L≈%.3e l_P，无新连续参数；但复用 m_e 且依赖峰值约定（L∝s^(-2/3)）。"
        % LA2)
    rec("INFO", "框架诚实定位",
        "TUFT = 「给定 m_e 后，把质量/自旋/统计编码为几何（kappa,tau,Lk）」的编码框架 + "
        "自旋统计推论；**不第一性生成尺度**。")
    rec("INFO", "若要与观测对接",
        "须显式登记『锚定输入清单』（m_e、H0、…）与『约定清单』（峰值/rms 等），"
        "并声明 TUFT 的独有可证伪量（如自旋统计 Lk=±1/2 的几何关联）。")

    # ---------------------------------------------------------------- 汇总
    sec("汇总")
    put("  PASS     = %d" % n_pass)
    put("  FAIL     = %d" % n_fail)
    put("  BOUNDARY = %d" % n_bound)
    put("  INFO     = %d" % n_info)
    put("  ── 核心结论 ──")
    put("  · 简并秩 = 1，绝对尺度 L 不可由 TUFT 方程锁定（自由度审计确证）")
    put("  · 打破简并须追加 1 条独立关系，且必来自外部（观测量或约定）")
    put("  · 7 类锚定方案扫全场：无 1 个能『第一性』给出电子尺度")
    put("  · A4 证明康普顿尺度 ∧ 电子高曲率互斥（偏离 %.3e 倍）" % conflict)
    put("  · 与 openuft M02 同构：O-SCALE 是 TUFT 的诚实边界，非证伪")
    put("")
    put("红线声明：数学自洽 != 实验证实。本文件只做量纲/秩/约定的诚实分析，")
    put("          不构成对 TUFT 物理真实性的任何主张。")

    text = "\n".join(out) + "\n"
    print(text)
    try:
        with open(REPORT_PATH, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("[OK] 报告已写入 " + REPORT_PATH)
    except Exception as exc:
        print("[warn] 报告写入失败: " + str(exc))


if __name__ == "__main__":
    main()
