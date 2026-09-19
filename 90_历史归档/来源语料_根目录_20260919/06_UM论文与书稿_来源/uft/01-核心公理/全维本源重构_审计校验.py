# -*- coding: utf-8 -*-
"""
《全维本源重构》稿件 审计校验
============================
对《全维本源重构：v_total=c、曲率 kappa - 挠率 tau - 角频率 omega 的统一场第一性原理理论》
逐条做量化审计：哪些是真导出、哪些是假设、哪些是内部矛盾。

姊妹文档: 全维本源重构_整理版.md
依赖: sympy, numpy（numpy 用于复用同目录 4D_Frenet_第三不变量_校验.py 的 Gram 行列式法）

判定口径:
  PASS = 稿件该处成立
  FAIL = 稿件该处内部矛盾 / 声称"导出"但不成立
  OPEN = 需要外部物理输入，本体系不可导出
  INFO = 成立但无信息量（恒等式/循环论证），不得作为"闭环"证据
"""

import sys
import io
import math
import contextlib
import importlib.util

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import sympy as sp

RESULTS = []


def record(cid, title, verdict, detail=""):
    if isinstance(verdict, bool):
        verdict = "PASS" if verdict else "FAIL"
    RESULTS.append((cid, title, verdict, detail))
    line = "[" + verdict + "] " + cid + " " + title
    if detail:
        line = line + "  |  " + str(detail)
    print(line)


def section(name):
    print("")
    print("=== " + name + " ===")


# ============================================================
# N1. 引力符号：稿件 3.4 与 4 节互相矛盾
# ============================================================
def check_gravity_sign():
    section("N1. 引力场方向与统一动力学是否自洽")

    m, c, kap = sp.symbols("m c kappa", positive=True)
    n1, n2, n3 = sp.symbols("n1 n2 n3")
    N = sp.Matrix([n1, n2, n3])

    g_paper = -c ** 2 * kap * N          # 3.4 节: g = -c^2 kappa N
    F_paper = m * c ** 2 * kap * N       # 4  节: F = +mc^2 kappa N
    diff = sp.simplify(F_paper - m * g_paper)
    ok = diff == sp.zeros(3, 1)
    record("N1", "牛顿第二律一致性：F 应等于 m*g（稿件 3.4 与 4 节）",
           ok, "F - m*g = " + str(diff.T) + "；kappa>0 时非零 => 两式符号相反")

    # 主论 v2.1 修正版：g = +c^2 kappa N（N 指向曲率中心即指向质量）
    g_fixed = c ** 2 * kap * N
    record("N1b", "改用 v2.1 号 g=+c^2*kappa*N 后与 F=mc^2*kappa*N 一致",
           sp.simplify(F_paper - m * g_fixed) == sp.zeros(3, 1),
           "球对称场中 N=-r_hat，g=-c^2*kappa*r_hat 指向质量（吸引）")


# ============================================================
# N2. 电荷定义的量纲
# ============================================================
def check_charge_dimension():
    section("N2. 电荷定义 q ~ oint tau dS 的量纲")

    L, M, T, I = sp.symbols("L M T I", positive=True)
    dim_tau = 1 / L          # 挠率 [L^-1]
    dim_ds = L               # 线元
    dim_dS = L ** 2          # 面元
    dim_charge = I * T       # 电荷 [A*s]

    area_form = sp.simplify(dim_tau * dim_dS)
    line_form = sp.simplify(dim_tau * dim_ds)

    record("N2", "稿件 q ~ oint tau dS 的量纲应为电荷 I*T",
           sp.simplify(area_form - dim_charge) == 0,
           "[tau*dS] = " + str(area_form) + "，量纲为长度，不是电荷")

    record("N2b", "改用 v2.1 线积分 q = q_tau * (1/2pi) oint tau ds 则无量纲",
           sp.simplify(line_form - 1) == 0,
           "[tau*ds] = 1，乘以电荷量子 q_tau 后才得电荷")


# ============================================================
# N3. 世界线曲率与引力场曲率被当作同一个量使用
# ============================================================
def check_curvature_conflation():
    section("N3. 世界线曲率 vs 引力场曲率：混用的量化后果")

    hbar = 1.054571817e-34
    cc = 299792458.0
    G = 6.67430e-11
    M_E = 5.9722e24
    R_E = 6.371e6

    kap_field = G * M_E / (cc ** 2 * R_E ** 2)          # 地表引力场曲率
    g_check = cc ** 2 * kap_field
    m_implied = hbar * kap_field / cc                   # 若把该 kappa 代入拓扑质量公式
    kap_for_earth = M_E * cc / hbar                     # 要得到地球质量所需的 kappa

    record("N3", "地表曲率代入教材式(4)得到的质量 vs 地球质量",
           False,
           "kappa_f=" + "{:.4e}".format(kap_field) + " m^-1, "
           "c^2*kappa_f=" + "{:.4f}".format(g_check) + " m/s^2 (OK), "
           "但 m=hbar*kappa/c=" + "{:.3e}".format(m_implied) + " kg vs M_E=" +
           "{:.3e}".format(M_E) + " kg")
    record("N3b", "同一 kappa 两种角色的量级差",
           False,
           "产生地球质量需 kappa=" + "{:.3e}".format(kap_for_earth) +
           " m^-1，与地表场曲率相差 " +
           "{:.2e}".format(kap_for_earth / kap_field) + " 倍 => 两个 kappa 不可混用（需 O7 桥接）")


# ============================================================
# N4. 45 度升角：Lk 整数性 与 s+Lk^2=1 的两难
# ============================================================
def check_spin_topology():
    section("N4. 费米子 45 度：环绕数两难")

    val = sp.sqrt(sp.Rational(1, 2))
    record("N4", "稿件自身恒等式 s+Lk^2=1 在 s=1/2 时强制 Lk=1/sqrt2",
           sp.simplify(val ** 2 - sp.Rational(1, 2)) == 0,
           "Lk=" + str(sp.nsimplify(val)) + "=" + "{:.6f}".format(math.sqrt(0.5)) +
           "，不是整数，违反闭合环带 Lk in Z")

    record("N4b", "若强行要求 Lk in Z（Wilczek/CW 要求），则 s+Lk^2=1 被迫放弃",
           False,
           "两难：Wr=0 => Lk=cos(eta)=0.7071 非整数；Wr!=0 => Lk!=cos(eta) => s+Lk^2=1 不成立。"
           "稿件同时用了两者，45 度不是 CW 定理的导出结论（属 O1 输入 s=1/2）")

    # N 圈闭合候选修复的可达性扫描（对上一轮提出的候选方案做定量否证）
    best = None
    for Nk in range(1, 300001):
        x = Nk / math.sqrt(2.0)
        err = abs(x - round(x))
        if best is None or err < best[1]:
            best = (Nk, err, round(x))
    record("N4c", "N 圈闭合补偿方案的可达性（扫描 N<=3e5）",
           "FAIL" if best[1] > 0 else "PASS",
           "最优 N=" + str(best[0]) + " 时 |N/sqrt2 - " + str(best[2]) + "| = " +
           "{:.3e}".format(best[1]) + "；N/sqrt2 永远不是整数（sqrt2 无理），"
           "严格整数不可达，且需 Wr 补偿 => 撤回该候选修复（仅可作数值近似方案）")


# ============================================================
# N5. 3D Frenet 描述世界线是否为维度欠账
# ============================================================
def check_dimension_deficit():
    section("N5. 维度欠账：4D 世界线需要 3 个广义曲率")

    path = "4D_Frenet_第三不变量_校验.py"
    try:
        spec = importlib.util.spec_from_file_location("frenet4d", path)
        mod = importlib.util.module_from_spec(spec)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            spec.loader.exec_module(mod)
        import numpy as np
        grid = np.linspace(0, 6 * math.pi, 8000)
        kap0 = mod.generalized_curvatures(mod.build_curve(0.0), grid)
        kap4 = mod.generalized_curvatures(mod.build_curve(0.3), grid)
        lo, hi = 400, -400
        k3_0 = float(np.abs(kap0[lo:hi, 2]).mean())
        k3_4 = float(np.abs(kap4[lo:hi, 2]).mean())
        record("N5", "纯 3D 螺旋 kappa3 退化为 0（稿件可用 3D Frenet）",
               k3_0 < 1e-4, "kappa3=" + "{:.3e}".format(k3_0))
        record("N5b", "含第四维运动的世界线 kappa3 非零（此时 kappa,tau 不足以确定曲线）",
               False,
               "kappa3=" + "{:.4f}".format(k3_4) +
               "；曲线论基本定理在 R^4 要求 3 个曲率 => 稿件公理 II 引述的"
               "「kappa,tau 唯一确定曲线」只成立于 3D（需明示世界线嵌入维数，见 O12）")
    except Exception as exc:  # noqa: BLE001
        record("N5", "复用 4D_Frenet_第三不变量_校验.py 失败", "OPEN", str(exc))


# ============================================================
# N6/N7. 稿件中被当作"闭环"的两处其实无信息量
# ============================================================
def check_tautologies():
    section("N6/N7. 循环论证辨识")

    hbar, c, w, kap = sp.symbols("hbar c omega kappa", positive=True)
    # 输入: m c^2 = hbar omega，且 omega = c*sqrt(kappa^2+tau^2)
    tau = sp.symbols("tau", positive=True)
    m_expr = hbar * w / c ** 2
    back = sp.simplify(m_expr.subs(w, c * sp.sqrt(kap ** 2 + tau ** 2)) - hbar / c * sp.sqrt(kap ** 2 + tau ** 2))
    record("N6", "稿件第 5 节电子算例：由 mc^2=hbar*omega 出发又回到它自身",
           "INFO" if back == 0 else "FAIL",
           "残差=" + str(back) + " => 恒等式复核，未产生任何可测量的新数值（不构成预言）")

    # 普朗克边界：kappa = 1/l_p 是输入而非导出
    hbar_v = 1.054571817e-34
    cc = 299792458.0
    lp = math.sqrt(hbar_v * 6.67430e-11 / cc ** 3)
    for L_test, label in [(lp, "普朗克长度"), (1.0, "1 米")]:
        mv = hbar_v / (cc * L_test)
        if label == "1 米":
            m_any = mv
    record("N7", "式(4) 对任意参考长度都成立 => kappa=1/l_p 是输入，非导出",
           "INFO",
           "kappa=1/l_p -> m=" + "{:.3e}".format(hbar_v / (cc * lp)) + " kg；"
           "同一公式取 kappa=1/(1 m) -> m=" + "{:.3e}".format(m_any) +
           " kg，说明该步不含普朗克尺度的选择判据")


# ============================================================
# N8. 稿件第 7 节开放清单的完备性
# ============================================================
def check_open_list():
    section("N8. 开放项清单完备性")

    listed = {"G 的数值", "弱相互作用相变方程", "精细结构常数", "宇宙学边界条件"}
    registry = {
        "O2": "自旋覆盖范围（s in (0,1] 无法容纳自旋 2 / 0）",
        "O3": "无质量粒子（m>0 恒成立，光子无容身处）",
        "O4": "与洛伦兹力兼容（tau*B 项不依赖速度、不显含外场）",
        "O5": "电荷量子 q_tau 数值",
        "O7": "世界线曲率 kappa_w <-> 场曲率 kappa_f 桥接",
        "O8": "完整协变波动方程组的源项",
        "O11": "可判别实验预言",
        "O12": "4D 第三曲率 kappa_3 缺失",
        "O13": "联络层非度规性 Q 缺失",
        "O14": "四相互作用 vs 三几何自由度数量失配",
        "O15": "非齐次麦克斯韦 / epsilon_0 不可导出",
        "O16": "光子质量容身处与 gamma 曲率预算上限",
    }
    missing = [k + " " + v for k, v in registry.items()]
    record("N8", "稿件第 7 节仅列 4 项，仓库登记缺 " + str(len(missing)) + " 项",
           False,
           "已列：" + "、".join(sorted(listed)) + "；缺：" + "；".join(missing))


def main():
    print("《全维本源重构》稿件审计校验")
    check_gravity_sign()
    check_charge_dimension()
    check_curvature_conflation()
    check_spin_topology()
    check_dimension_deficit()
    check_tautologies()
    check_open_list()

    np_ = sum(1 for r in RESULTS if r[2] == "PASS")
    nf = sum(1 for r in RESULTS if r[2] == "FAIL")
    no = sum(1 for r in RESULTS if r[2] == "OPEN")
    ni = sum(1 for r in RESULTS if r[2] == "INFO")
    print("")
    print("---- 汇总 ----")
    print("总判定: " + str(len(RESULTS)) +
          "  PASS=" + str(np_) + "  FAIL=" + str(nf) +
          "  OPEN=" + str(no) + "  INFO=" + str(ni))
    print("")
    print("口径：FAIL = 稿件内部矛盾或越权声称；INFO = 成立但无信息量，不得当作『闭环』证据；")
    print("      OPEN = 必须外部物理输入。三者都不是程序 bug。")


if __name__ == "__main__":
    main()
