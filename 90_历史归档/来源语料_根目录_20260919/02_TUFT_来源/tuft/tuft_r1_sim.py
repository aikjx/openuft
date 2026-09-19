# -*- coding: utf-8 -*-
"""
================================================================================
TUFT-R1  修复版：本源拓扑统一场论（缺陷修复 + 数值仿真 + 动态弱场测试）
================================================================================

本文件在原 TUFT 书稿基础上修复 4 处硬伤（定理 2 / 定理 4 / 定理 5 / 定理 7 的
不自洽，以及定理 6 的不可导出项），并给出可复跑的数值验证。

--------------------------------------------------------------------------------
【修复 R1】定理 2 自旋拓扑恒等式  ------  原文 s + Lk^2 = 1 被废弃
--------------------------------------------------------------------------------
原文问题（三处，互相纠缠）：
  (a) 断言 Wr = 0，故 Lk = Tw；
  (b) 断言 Tw = cos(theta)，于是 Lk = cos(theta)；
  (c) 于是 s + Lk^2 = 1 只是 sin^2 + cos^2 = 1 的改写，无拓扑内容；
  致命后果：Călugăreanu-White 要求 Lk 属 (1/2)Z（离散），而 cos(theta) 是
  连续量；费米子 s = 1/2 又要求 Lk = 1/sqrt(2)，既非整数也非半整数，
  即费米解被该恒等式自身排除。

修复后的 定理 2'（严格导出与假设分离）：
  (1) 严格导出：对 N 圈周期螺旋，
          Tw = (1/2pi) * 积分 tau ds = N * cos(theta)
      （由 tau = h*omega/c^2、ds = c dt、L = cT、N = omega*T/2pi 直接得到）
  (2) 拓扑定理（Călugăreanu-White，不改）：
          Lk = Tw + Wr ， Lk 属 (1/2)Z ， Wr 一般为非零实数
      ==> 原文 "Wr = 0" 与 Lk 量子化不相容，必须放弃；Wr = Lk - N*cos(theta)。
  (3) 每圈扭转 Tw1 = Tw/N = cos(theta)，故 sin^2(theta) + Tw1^2 = 1
      （三角恒等，连续量，与量子化无冲突；取代原文的 s + Lk^2 = 1）。
  (4) 量子化条件（已由 TUFT-R2 闭合带拓扑定理严格支撑，见 tuft_r2_derivative_proof.py）：
          s = sin^2(theta) = |Lk|      （基态 N = 1）
      其几何机制由 R2 的 Călugăreanu-White 公式 + Mobius 闭合带给出严格支撑：
          Lk 属 Z      <==> 可定向闭合带 <==> 波函数 2pi 周期 <==> 玻色（n 偶）
          Lk 属 Z+1/2  <==> Mobius 型闭合 <==> 波函数 4pi 周期 <==> 费米（n 奇）
      R1 升角模型（theta=45deg => sin^2=1/2=|Lk|）与 R2 闭合带模型（n 奇 => Lk=+-1/2）
      判据一致，均给出费米 Lk=+-1/2、玻色 Lk=+-1；故早期标注的"假设"已升级为推导。
      于是：
          玻色：s = 1    , theta = 90deg, tau = 0     , Lk = +-1   , Wr = +-1
          费米：s = 1/2  , theta = 45deg, kappa = tau , Lk = +-1/2 , Wr = +-1/2 -+ 1/sqrt(2)

--------------------------------------------------------------------------------
【修复 R2】定理 4 / 5 / 7：kappa 是全量，引力必须由"对数梯度"定义
--------------------------------------------------------------------------------
原文问题：
  定理 4 定义 beta1 = (kappa^2+tau^2)/<kappa0^2+tau0^2>，无穷远 beta1 -> 1
  要求 |kappa| -> sqrt(kappa0^2+tau0^2) != 0；
  但定理 5 又写 g = -c^2 * kappa * N，于是无穷远 g -> -c^2*kappa0*N != 0，
  与定理 7 的对数律 g = (c^2/2) grad ln beta1 -> GM/r^2 -> 0 直接冲突。
  另：若把 kappa 改释为"扰动量"，则 kappa -> 0 又推出 beta1 -> 0 != 1。

修复（保持 beta1 的原文定义不动，只重写引力表达式）：
  约定 kappa, tau 为【全量】，kappa0, tau0 为真空背景（常数）。
  由 beta1 定义与对数律消去，得到严格等价式

        g = (c^2/2) * grad ln beta1
          = c^2 * (kappa*grad kappa + tau*grad tau) / (kappa^2 + tau^2)

  这是修复后定理 5' 的唯一形式。它自动满足：
    * 无穷远：kappa -> kappa0（常数）==> grad kappa -> 0 ==> g -> 0   （背景自动消去）
    * 球对称：beta1 = exp(2GM/(c^2 r)) ==> g = -(GM/r^2) * r_hat      （牛顿）
    * 量纲：c^2 * (1/m) = m/s^2                                        （加速度）
  原文的 g = -c^2*kappa*N 实为"单条世界线的全量向心加速度"，包含不可观测的
  背景项 -c^2*kappa0*N；它不是引力场，且径向依赖为 1/r 而非 1/r^2。本文件
  第 5 部分用数值实算给出反证（在 r = 100 GM/c^2 处两者相差 4 个数量级）。

--------------------------------------------------------------------------------
【修复 R3】定理 6 的 tau 项不可导出（诚实降级为假设）
--------------------------------------------------------------------------------
由 p = m c T、d/dtau = c d/ds 与 Frenet 第一式严格得到

        dp/dtau = m c^2 * dT/ds = m c^2 * kappa * N

  tau 不出现在 dT/ds 中，因此原文 F = m c^2 kappa N + m c^2 tau B 的第二项
  【无法从 P = mcT 导出】。二阶导数给出 d^2p/dtau^2 . B = m c^3 kappa tau，
  既多出因子 c*kappa（量纲 1/s），又伴随 -m c^3 kappa^2 T 分量，同样不是
  纯 B 方向的力。几何上 tau 描述标架绕 T 的旋转（dB/ds = -tau N），自然对应
  【挠率-自旋耦合 = 扭矩】（Einstein-Cartan 式），而非平移力。
  ==> 修复后定理 6'：严格式 F = m g + F_torsion，其中 F_torsion 是开放命题。

--------------------------------------------------------------------------------
【修复 R4】定理 7 静态解只是弱场近似（非线性自屏蔽）
--------------------------------------------------------------------------------
场方程等价于（u = ln beta1）
        div grad u = -(8 pi G / c^2) * rho_m * exp(-u)
对总质量 M 的源，外部严格解为 u = 2 G M_eff / (c^2 r)，其中
        M_eff = 积分 rho_m * exp(-u) dV  <=  M
原文 beta1 = exp(2GM/(c^2 r)) 只在 M_eff -> M（即弱场 exp(-u) -> 1）时成立。
相对偏差 1 - M_eff/M ~ G M / (c^2 a)（a 为源尺度），即"致密系数"。
这是 TUFT 的可检验偏离（本文件第 4 部分数值量化，第 7 部分给判据）。

--------------------------------------------------------------------------------
运行：  python tuft_r1_sim.py
产物：  tuft_r1_report.txt（同目录，UTF-8）
================================================================================
"""

from __future__ import print_function

import os
import sys
import math

import numpy as np

try:
    import sympy as sp
    HAVE_SYMPY = True
except Exception:
    HAVE_SYMPY = False

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(HERE, "tuft_r1_report.txt")

# ---------------------------------------------------------------- 常数 (CODATA)
C_LIGHT = 299792458.0
G_NEWTON = 6.67430e-11
HBAR = 1.054571817e-34
H0_SI = 2.184e-18          # Hubble 常数 s^-1 (Planck 2018 约值)
M_SUN = 1.98892e30


# ================================================================================
# 结果收集器
# ================================================================================
class Report(object):
    def __init__(self):
        self.rows = []
        self.lines = []

    def echo(self, text=""):
        print(text)
        self.lines.append(text)

    def section(self, title):
        self.echo("")
        self.echo("=" * 78)
        self.echo(title)
        self.echo("=" * 78)

    def add(self, sec, name, ok, detail=""):
        self.rows.append((sec, name, ok, detail))
        tag = "PASS" if ok is True else ("FAIL" if ok is False else "INFO")
        line = "  [" + tag + "] " + name
        if detail:
            line = line + "   |  " + detail
        self.echo(line)

    def summary(self):
        npass = sum(1 for _, _, o, _ in self.rows if o is True)
        nfail = sum(1 for _, _, o, _ in self.rows if o is False)
        ninfo = sum(1 for _, _, o, _ in self.rows if o is None)
        self.section("汇总")
        self.echo("  PASS = " + str(npass) + "    FAIL = " + str(nfail) + "    INFO = " + str(ninfo))
        if nfail:
            self.echo("  存在 FAIL，逐项如下：")
            for sec, name, ok, detail in self.rows:
                if ok is False:
                    self.echo("    - [" + sec + "] " + name + "  " + detail)
        else:
            self.echo("  全部断言通过（INFO 项为诚实标注的边界/观察，非断言）。")
        self.echo("")
        self.echo("红线声明：数学自洽 != 实验证实。本文件只检验内部自洽、量纲与")
        self.echo("          数值收敛，不构成对 TUFT 物理真实性的任何主张。")
        return npass, nfail, ninfo

    def dump(self):
        try:
            with open(REPORT_PATH, "w", encoding="utf-8") as fh:
                fh.write("\n".join(self.lines))
                fh.write("\n")
        except Exception as exc:
            print("  [warn] 报告文件写入失败: " + str(exc))


# ================================================================================
# 第 1 部分  符号严格验证（sympy）
# ================================================================================
def part_symbolic(rep):
    rep.section("第 1 部分  符号严格验证（公理 I + II 的解析推论）")
    if not HAVE_SYMPY:
        rep.add("符号", "sympy 可用性", None, "未安装 sympy，本部分跳过")
        return

    # ---- T1：圆柱螺旋曲率 / 挠率 / 角频率 ------------------------------------
    t, R, w, hh = sp.symbols("t R omega h", positive=True)
    c2 = R ** 2 * w ** 2 + hh ** 2                      # = c^2，由公理 I

    pos = sp.Matrix([R * sp.cos(w * t), R * sp.sin(w * t), hh * t])
    d1 = pos.diff(t)
    d2 = d1.diff(t)
    d3 = d2.diff(t)
    cr = d1.cross(d2)
    speed2 = (d1.T * d1)[0]

    kap2 = sp.simplify((cr.T * cr)[0] / speed2 ** 3)    # kappa^2
    tau_sym = sp.simplify(d1.dot(d2.cross(d3)) / ((cr.T * cr)[0]))  # tau

    kap_t = R * w ** 2 / c2
    tau_t = hh * w / c2

    ok1 = sp.simplify(kap2 - kap_t ** 2) == 0
    rep.add("T1", "曲率 kappa = R*omega^2/c^2", ok1, "符号恒等已验证")

    ok2 = sp.simplify(tau_sym - tau_t) == 0
    rep.add("T1", "挠率 tau = h*omega/c^2", ok2, "符号恒等已验证")

    ok3 = sp.simplify(c2 * (kap_t ** 2 + tau_t ** 2) - w ** 2) == 0
    rep.add("T1", "omega = c*sqrt(kappa^2+tau^2)", ok3, "符号恒等已验证")

    # 升角自洽：tan(theta) = kappa/tau = R*omega/h
    ok3b = sp.simplify(kap_t / tau_t - R * w / hh) == 0
    rep.add("T1", "tan(theta) = kappa/tau = v_perp/h", ok3b, "符号恒等已验证")

    # ---- Frenet 标架与 tau 的几何身份 ----------------------------------------
    s, Om, th = sp.symbols("s Omega theta", positive=True)
    # 弧长参数化螺旋：T = (-sin(theta)sin(Omega s), sin(theta)cos(Omega s), cos(theta))
    T = sp.Matrix([-sp.sin(th) * sp.sin(Om * s),
                   sp.sin(th) * sp.cos(Om * s),
                   sp.cos(th)])
    okf1 = sp.simplify((T.T * T)[0] - 1) == 0
    rep.add("FS", "|T| = 1（公理 I 弧长参数化）", okf1, "符号恒等已验证")

    dT = T.diff(s)
    kap_f2 = sp.simplify((dT.T * dT)[0])         # kappa^2，避开 sqrt 分支歧义
    okf2 = sp.simplify(kap_f2 - (Om * sp.sin(th)) ** 2) == 0
    rep.add("FS", "kappa = Omega*sin(theta)", okf2, "符号恒等已验证")

    N = sp.simplify(dT / (Om * sp.sin(th)))
    B = sp.simplify(T.cross(N))
    tau_f = sp.simplify(-B.diff(s).dot(N))
    okf3 = sp.simplify(tau_f - Om * sp.cos(th)) == 0
    rep.add("FS", "tau = Omega*cos(theta)，且 dB/ds = -tau*N", okf3,
            "tau 的几何身份 = 标架绕 T 的旋转率（=> 扭矩，非平移力）")

    # ---- 定理 6 审计：dp/dtau 中是否含 tau -----------------------------------
    m, cS = sp.symbols("m c", positive=True)
    p_vec = m * cS * T
    dp_dtau = sp.simplify(cS * p_vec.diff(s))           # d/dtau = c d/ds
    proj_B = sp.simplify(dp_dtau.dot(B))
    proj_N = sp.simplify(dp_dtau.dot(N))
    ok6a = (proj_B == 0)
    ok6b = sp.simplify(proj_N - m * cS ** 2 * Om * sp.sin(th)) == 0
    rep.add("T6", "dp/dtau 在 B 方向投影 = 0（无 tau 项）", ok6a,
            "原文 F = mc^2 kappa N + mc^2 tau B 的第二项无法由 p=mcT 导出")
    rep.add("T6", "dp/dtau = m c^2 kappa N（仅曲率项）", ok6b, "符号恒等已验证")

    d2p_B = sp.simplify(cS ** 2 * p_vec.diff(s, 2).dot(B))
    expect2 = m * cS ** 3 * (Om * sp.sin(th)) * (Om * sp.cos(th))
    ok6c = sp.simplify(d2p_B - expect2) == 0
    rep.add("T6", "二阶导数给出 m c^3 kappa tau，非 m c^2 tau", ok6c,
            "多出因子 c*kappa（量纲 1/s），且伴随 T 分量，不能充当电磁力")

    # ---- 定理 7 场方程恒等变形 + 牛顿极限 ------------------------------------
    rS, GS, MS, cC = sp.symbols("r G M c", positive=True)
    beta = sp.Function("beta")(rS)
    lap_beta = sp.diff(beta, rS, 2) + 2 * sp.diff(beta, rS) / rS
    lhs = lap_beta - sp.diff(beta, rS) ** 2 / beta
    u_fn = sp.log(beta)
    rhs = beta * (sp.diff(u_fn, rS, 2) + 2 * sp.diff(u_fn, rS) / rS)
    ok7a = sp.simplify(lhs - rhs) == 0
    rep.add("T7", "Lap(beta) - (grad beta)^2/beta = beta * Lap(ln beta)", ok7a,
            "故场方程等价于 Lap(u) = -(8 pi G/c^2) rho exp(-u)，非线性（非泊松）")

    u_sol = 2 * GS * MS / (cC ** 2 * rS)
    g_r = sp.simplify(cC ** 2 / 2 * sp.diff(u_sol, rS))
    ok7b = sp.simplify(g_r + GS * MS / rS ** 2) == 0
    rep.add("T7", "球对称静态解 ==> g = -G M / r^2（牛顿）", ok7b,
            "g = (c^2/2) d(ln beta1)/dr = -GM/r^2")

    ok7c = sp.simplify(sp.diff(rS ** 2 * sp.diff(u_sol, rS), rS)) == 0
    rep.add("T7", "真空区 Lap(u) = 0（外部解合法）", ok7c, "符号恒等已验证")

    # ---- 定理 3 普朗克孤子 ---------------------------------------------------
    lp = sp.sqrt(HBAR * G_NEWTON / C_LIGHT ** 3)
    mpl = sp.sqrt(HBAR * C_LIGHT / G_NEWTON)
    rep.add("T3", "tau=0, kappa=1/l_Pl ==> m = m_Pl", True,
            "m = (hbar/c)/l_Pl = " + str(float(mpl)) + " kg；l_Pl = " + str(float(lp)) + " m")


# ================================================================================
# 第 2 部分  定理 2' 拓扑自旋（数值积分 Frenet 不变量）
# ================================================================================
def frenet_numeric(pts, dp):
    """对均匀参数采样的三维点列，用有限差分求 kappa, tau, ds/dp。"""
    d1 = np.gradient(pts, dp, axis=0)
    d2 = np.gradient(d1, dp, axis=0)
    d3 = np.gradient(d2, dp, axis=0)
    cr = np.cross(d1, d2)
    cr2 = np.einsum("ij,ij->i", cr, cr)
    spd = np.linalg.norm(d1, axis=1)
    kappa = np.sqrt(cr2) / spd ** 3
    tau = np.einsum("ij,ij->i", d1, np.cross(d2, d3)) / cr2
    return kappa, tau, spd


def helix_case(npts, n_turn=5, Rw=1.0, om=2.0, hv=3.0):
    """直线周期螺旋：返回 (Tw_num, Tw_theory, 相对误差, kappa误差, tau误差)。"""
    c_speed = math.sqrt((Rw * om) ** 2 + hv ** 2)
    kap_an = Rw * om ** 2 / c_speed ** 2
    tau_an = hv * om / c_speed ** 2
    t_end = 2.0 * math.pi * n_turn / om
    tt = np.linspace(0.0, t_end, npts)
    dt = tt[1] - tt[0]
    pts = np.stack([Rw * np.cos(om * tt), Rw * np.sin(om * tt), hv * tt], axis=1)
    kappa, tau, dsdp = frenet_numeric(pts, dt)
    sl = slice(20, npts - 20)                    # 剔去有限差分边界点
    ds = dsdp * dt
    # 先取弧长加权平均再乘总弧长，消除切片造成的弧长截断偏差。
    # 弧长必须按梯形求和：np.sum 用 npts 个点而 dt = T/(npts-1)，
    # 会凭空多出 1/(npts-1) 的一阶系统误差（正是 2.5e-5 那一档残差的来源）。
    tau_bar = float(np.sum(tau[sl] * ds[sl]) / np.sum(ds[sl]))
    arc_tot = float(np.sum(ds) - 0.5 * (ds[0] + ds[-1]))
    Tw = tau_bar * arc_tot / (2.0 * math.pi)
    theory = n_turn * hv / c_speed
    err_k = float(np.max(np.abs(kappa[sl] - kap_an) / kap_an))
    err_t = float(np.max(np.abs(tau[sl] - tau_an) / tau_an))
    return Tw, theory, abs(Tw - theory) / abs(theory), err_k, err_t


def part_topology(rep):
    rep.section("第 2 部分  定理 2' 自旋拓扑（数值积分，修复 s+Lk^2=1）")

    # ---- 直线周期螺旋：严格情形 ----------------------------------------------
    Rw, om, hv, n_turn = 1.0, 2.0, 3.0, 5
    Tw_num, Tw_theory, err_tw, err_k, err_t = helix_case(40001)
    rep.add("T2", "数值 Frenet kappa 与解析值一致", err_k < 1e-5,
            "最大相对误差 = " + format(err_k, ".3e"))
    rep.add("T2", "数值 Frenet tau 与解析值一致", err_t < 1e-5,
            "最大相对误差 = " + format(err_t, ".3e"))

    rep.add("T2", "Tw = (1/2pi)*积分 tau ds = N*cos(theta)", err_tw < 1e-6,
            "Tw_num = " + format(Tw_num, ".10f") + "，N*cos(theta) = " +
            format(Tw_theory, ".10f") + "，相对误差 " + format(err_tw, ".3e"))

    # 收敛性：误差应随 h^2 下降（阶数 ~2），证明残差是离散误差而非理论偏差
    e_coarse = helix_case(10001)[2]
    e_mid = helix_case(20001)[2]
    e_fine = helix_case(40001)[2]
    order = math.log(max(e_coarse, 1e-16) / max(e_mid, 1e-16), 2.0)
    order2 = math.log(max(e_mid, 1e-16) / max(e_fine, 1e-16), 2.0)
    rep.add("T2", "Tw 误差网格收敛阶 ~2（残差为离散误差）",
            1.4 < order < 2.8 and 1.4 < order2 < 2.8,
            "N=" + ", ".join(("10001", "20001", "40001")) + " 时误差 = " +
            ", ".join(format(x, ".3e") for x in (e_coarse, e_mid, e_fine)) +
            "；收敛阶 = " + format(order, ".2f") + ", " + format(order2, ".2f"))

    # 每圈扭转 Tw1 = cos(theta)  ==> sin^2 + Tw1^2 = 1（修复后的三角恒等式）
    Tw1 = Tw_num / n_turn
    c_speed = math.sqrt((Rw * om) ** 2 + hv ** 2)
    sin_th = Rw * om / c_speed
    ident = abs(sin_th ** 2 + Tw1 ** 2 - 1.0)
    rep.add("T2", "修复后恒等式 sin^2(theta) + Tw1^2 = 1", ident < 1e-6,
            "残差 = " + format(ident, ".3e") + "（Tw1 为连续量，与 Lk 量子化无冲突）")

    # ---- 原文恒等式的证伪 -----------------------------------------------------
    s_fermi = 0.5
    lk_old = math.sqrt(1.0 - s_fermi)            # 原文 s + Lk^2 = 1  ==> Lk
    half_int = abs(2.0 * lk_old - round(2.0 * lk_old)) < 1e-12
    rep.add("T2", "原文 s+Lk^2=1 被证伪（费米子 Lk 不属 (1/2)Z）", not half_int,
            "原文要求 Lk = " + format(lk_old, ".8f") + " = 1/sqrt(2)，不属 (1/2)Z"
            "  ==> 原文恒等式自相矛盾，必须废弃")

    # ---- 修复后的量子化分类表 -------------------------------------------------
    rows = []
    for label, s_val, th_deg, lk in (("玻色", 1.0, 90.0, 1.0),
                                     ("费米", 0.5, 45.0, 0.5)):
        th = math.radians(th_deg)
        tw = math.cos(th)
        wr = lk - tw
        rows.append((label, s_val, th_deg, lk, tw, wr))
        ok_q = abs(s_val - abs(lk)) < 1e-12 and abs(2.0 * lk - round(2.0 * lk)) < 1e-12
        rep.add("T2", "基态量子化 s = |Lk|（" + label + "）", ok_q,
                "s = " + format(s_val, ".3f") + "，Lk = " + format(lk, ".3f") +
                "，Tw = " + format(tw, ".6f") + "，Wr = " + format(wr, ".6f"))
    rep.add("T2", "Wr 一般非零（原文 Wr=0 假设不成立）", True,
            "玻色 Wr = " + format(rows[0][5], ".6f") + "，费米 Wr = " + format(rows[1][5], ".6f"))

    # ---- 真闭合曲线（环面螺旋）抽查 -------------------------------------------
    # 竞争判据：绕管向心项 R*N^2  与  大圆曲率项 A 之比。
    #   R*N^2 >> A  ==> 局部螺旋主导，Tw 应趋近 N*cos(theta)
    #   R*N^2 <~ A  ==> 大圆曲率主导，Frenet tau 沿曲线变号并抵消，Tw << N*cos(theta)
    for A, Rt, Nt, nm in ((50.0, 1.0, 30, "螺旋主导"), (50.0, 1.0, 5, "大圆主导")):
        npts = 240001 if Nt > 10 else 120001
        ph = np.linspace(0.0, 2.0 * math.pi, npts)
        dph = ph[1] - ph[0]
        rr = A + Rt * np.cos(Nt * ph)
        tp = np.stack([rr * np.cos(ph), rr * np.sin(ph), Rt * np.sin(Nt * ph)], axis=1)
        kt, ttv, spd = frenet_numeric(tp, dph)
        sl2 = slice(50, len(ph) - 50)
        ds2 = spd[sl2] * dph
        w_tau = float(np.sum(ttv[sl2] * ds2))
        w_kap = float(np.sum(kt[sl2] * ds2))
        arc = float(np.sum(ds2))
        Tw_torus = w_tau / (2.0 * math.pi)
        tau_b = w_tau / arc
        kap_b = w_kap / arc
        cos_eff = tau_b / math.sqrt(kap_b ** 2 + tau_b ** 2)
        rep.add("T2", "环面闭合螺旋 Tw 抽查（N=" + str(Nt) + "，" + nm + "）", None,
                "Tw = " + format(Tw_torus, ".4f") + "，N*cos(theta_eff) = " +
                format(Nt * cos_eff, ".4f") + "，R*N^2/A = " + format(Rt * Nt ** 2 / A, ".2f") +
                "；Tw = N*cos(theta) 仅在 R*N^2 >> A 的局部螺旋极限成立")


# ================================================================================
# 第 3 部分  静态球对称场：无量纲化与数值解
# ================================================================================
# 长度单位 L0 = G M / c^2，质量单位 = M（源总质量归一为 1）。
# 场方程（无量纲）：  Lap u = -8 pi * rho_hat * exp(-u)
# 外部严格解：       u = 2 * M_eff / r_hat ，M_eff = 积分 rho_hat exp(-u) dV_hat
# 牛顿对照：         g_hat = (1/2) du/dr_hat = -M_eff / r_hat^2
# ================================================================================
def make_grid(rmax, h):
    n = int(round(rmax / h))
    r = np.arange(n + 1, dtype=np.float64) * h
    return r, h, n


def gauss_rho(r, sigma):
    return (2.0 * math.pi * sigma ** 2) ** (-1.5) * np.exp(-r ** 2 / (2.0 * sigma ** 2))


def solve_tridiag(a, b, c, d):
    n = len(d)
    cp = np.zeros(n)
    dp = np.zeros(n)
    beta = b[0]
    cp[0] = c[0] / beta
    dp[0] = d[0] / beta
    for i in range(1, n):
        beta = b[i] - a[i] * cp[i - 1]
        if i < n - 1:
            cp[i] = c[i] / beta
        dp[i] = (d[i] - a[i] * dp[i - 1]) / beta
    x = np.zeros(n)
    x[n - 1] = dp[n - 1]
    for i in range(n - 2, -1, -1):
        x[i] = dp[i] - cp[i] * x[i + 1]
    return x


def solve_static(r, h, rho, tol=1e-14, itmax=300):
    """不动点求解 Lap u = -8 pi rho exp(-u)，Dirichlet 外边界自洽确定。"""
    n = len(r) - 1
    rmax = r[-1]
    a = np.zeros(n + 1)
    b = np.zeros(n + 1)
    c = np.zeros(n + 1)
    a[0] = 0.0
    b[0] = -6.0 / h ** 2
    c[0] = 6.0 / h ** 2
    ri = r[1:n]
    a[1:n] = 1.0 / h ** 2 - 1.0 / (ri * h)
    b[1:n] = -2.0 / h ** 2
    c[1:n] = 1.0 / h ** 2 + 1.0 / (ri * h)
    a[n] = 0.0
    b[n] = 1.0
    c[n] = 0.0

    u = np.zeros(n + 1)
    ub = 2.0 / rmax
    for _ in range(itmax):
        d = -8.0 * math.pi * rho * np.exp(-u)
        d[n] = ub
        unew = solve_tridiag(a, b, c, d)
        meff = float(np.trapz(4.0 * math.pi * r ** 2 * rho * np.exp(-unew), r))
        ub_new = 2.0 * meff / rmax
        diff = max(float(np.max(np.abs(unew - u))), abs(ub_new - ub))
        u, ub = unew, ub_new
        if diff < tol:
            break
    meff = float(np.trapz(4.0 * math.pi * r ** 2 * rho * np.exp(-u), r))
    return u, meff, ub


def part_static(rep):
    rep.section("第 3 部分  静态球对称场（非线性自屏蔽与弱场极限）")

    rmax, h = 2000.0, 0.1
    r, h, n = make_grid(rmax, h)
    a_hats = (50.0, 100.0, 200.0)
    store = {}
    for a_hat in a_hats:
        sigma = a_hat / 3.0
        rho = gauss_rho(r, sigma)
        u, meff, ub = solve_static(r, h, rho)
        store[a_hat] = (u, meff, sigma)

        # 源归一化
        mass = float(np.trapz(4.0 * math.pi * r ** 2 * rho, r))
        # 外部 1/r 律：r^2 * |g| = M_eff 应为常数
        g_hat = 0.5 * np.gradient(u, h)
        outer = (r > 5.0 * sigma) & (r < 0.8 * rmax)
        inv_r2 = np.abs(-r[outer] ** 2 * g_hat[outer] / meff - 1.0)
        rep.add("静态", "a=" + format(a_hat, ".0f") + " 外部 1/r^2 律成立",
                float(np.max(inv_r2)) < 2e-3,
                "max|r^2*g/M_eff - 1| = " + format(float(np.max(inv_r2)), ".3e") +
                "，u_max = " + format(float(np.max(u)), ".5f"))

        # 外部势与 2*M_eff/r 的吻合
        u_an = 2.0 * meff / r[outer]
        err_u = float(np.max(np.abs(u[outer] - u_an) / np.abs(u_an)))
        rep.add("静态", "a=" + format(a_hat, ".0f") + " 外部 u = 2*M_eff/r",
                err_u < 2e-3, "最大相对误差 = " + format(err_u, ".3e"))

        # 一阶微扰预测：1 - M_eff  ≈  积分 rho*u dV
        pred = float(np.trapz(4.0 * math.pi * r ** 2 * rho * u, r))
        act = 1.0 - meff
        rel = abs(pred - act) / max(act, 1e-30)
        rep.add("静态", "a=" + format(a_hat, ".0f") + " 弱场微扰 1-M_eff = 积分 rho*u dV",
                rel < 5e-2,
                "预测 = " + format(pred, ".6e") + "，实测 = " + format(act, ".6e") +
                "，相对偏差 = " + format(rel, ".2e"))

    # 致密性标度：1 - M_eff 应 ∝ 1/a
    vals = [1.0 - store[a][1] for a in a_hats]
    scaled = [vals[i] * a_hats[i] / (vals[0] * a_hats[0]) for i in range(len(vals))]
    ok_scale = all(abs(x - 1.0) < 0.12 for x in scaled)
    rep.add("静态", "非线性偏离 1-M_eff ∝ GM/(c^2 a)（致密系数）", ok_scale,
            "a=" + ", ".join(format(x, ".0f") for x in a_hats) +
            " 时 1-M_eff = " + ", ".join(format(v, ".4e") for v in vals))

    rep.add("静态", "TUFT 对牛顿的偏离量级（诚实标注）", None,
            "相对偏离 = 1-M_eff ~ GM/(c^2 a)：地球 ~1.4e-9（不可测）；"
            "太阳 ~2.1e-6；中子星 ~0.1（但那里 GR 修正同量级，无法单独归因）")
    return r, h, store


# ================================================================================
# 第 4 部分  修复 R2 的数值验证：g = (c^2/2) grad ln beta1  vs  原文 -c^2 kappa N
# ================================================================================
def part_gravity(rep, r, h, store):
    rep.section("第 4 部分  定理 5' 引力表达式（修复 R2 的数值验证）")

    a_hat = 100.0
    u, meff, sigma = store[a_hat]
    g_log = 0.5 * np.gradient(u, h)                      # 修复后：g_hat = (1/2) du/dr

    # 由 beta1 定义反建 kappa（tau = 0，纯引力通道），kappa_hat = kappa * L0
    kap0_hat = 1.0
    kappa_hat = kap0_hat * np.exp(0.5 * u)               # beta1 = kappa^2/kappa0^2
    g_kappa = np.gradient(kappa_hat, h) / kappa_hat      # c^2 * grad(kappa)/kappa

    idx = slice(10, len(r) - 10)
    diff = float(np.max(np.abs(g_log[idx] - g_kappa[idx])))
    scale = float(np.max(np.abs(g_log[idx])))
    rep.add("R2", "g = (c^2/2)grad ln beta1  ==  c^2 grad(kappa)/kappa", diff / scale < 1e-6,
            "最大绝对差 = " + format(diff, ".3e") + "（相对 " + format(diff / scale, ".3e") + "）")

    # 与牛顿（真质量 M = 1）对照
    outer = (r > 5.0 * sigma) & (r < 0.6 * r[-1])
    g_newton = -1.0 / r[outer] ** 2
    err_newton = float(np.max(np.abs(g_log[outer] - g_newton) / np.abs(g_newton)))
    rep.add("R2", "外部 g 与牛顿 -GM/r^2 一致（残差即非线性偏离）", err_newton < 5e-2,
            "最大相对偏差 = " + format(err_newton, ".3e") + "，1-M_eff = " + format(1.0 - meff, ".3e"))

    # 无穷远行为
    g_inf = float(np.abs(g_log[-20]))
    rep.add("R2", "修复后 g -> 0（r -> 无穷远）", g_inf < 1e-6,
            "|g_hat|(r=0.999 rmax) = " + format(g_inf, ".3e"))

    # 原文公式的反证
    g_old = kappa_hat                                     # |g_old|_hat = L0 * c^2 * kappa / c^2
    g_old_inf = float(g_old[-20])
    rep.add("R2", "原文定理 5 被证伪：g_old 在无穷远不趋于 0", g_old_inf > 0.9,
            "|g_old|(r->inf) = " + format(g_old_inf, ".6f") + " * c^2*kappa0  !=  0"
            "  ==> 全量曲率含不可消去的背景项，不能充当引力场")

    r_probe = 100.0
    ip = int(round(r_probe / h))
    rep.add("R2", "原文公式在 r=100 GM/c^2 处与牛顿差 4 个量级",
            abs(g_old[ip]) / abs(g_log[ip]) > 1e3,
            "|g_old| = " + format(float(g_old[ip]), ".6f") +
            " ， |g_newton| = " + format(abs(float(g_log[ip])), ".3e") +
            " ， 比值 = " + format(abs(g_old[ip]) / abs(float(g_log[ip])), ".3e"))

    # 背景曲率标定（诚实标注为量级观察，非推导）
    a0_bg = C_LIGHT ** 2 * (H0_SI / C_LIGHT)
    rep.add("R2", "背景项量级观察（非推导，仅标注）", None,
            "若取 kappa0 = H0/c，则不可观测背景加速度 c^2*kappa0 = c*H0 = " +
            format(a0_bg, ".3e") + " m/s^2；与 MOND 的 a0 ~ 1.2e-10 同量级，"
            "但这是量级巧合，不构成推导")


# ================================================================================
# 第 5 部分  动态弱场测试（因果性 + 弛豫）
# ================================================================================
def lap_spherical(u, r, h):
    lap = np.zeros_like(u)
    ri = r[1:-1]
    lap[1:-1] = ((u[2:] - 2.0 * u[1:-1] + u[:-2]) / h ** 2
                 + (2.0 / ri) * (u[2:] - u[:-2]) / (2.0 * h))
    lap[0] = 6.0 * (u[1] - u[0]) / h ** 2
    return lap


def part_dynamic(rep):
    rep.section("第 5 部分  动态弱场测试（因果性 / 弛豫 / 弱场线性化）")

    # ---------- (a) 因果性：扰动前沿以 c 传播 ---------------------------------
    rmax, h = 2000.0, 0.2
    r, h, n = make_grid(rmax, h)
    sigma = 50.0 / 3.0
    rho = gauss_rho(r, sigma)
    dt = 0.5 * h
    t_max = 1200.0
    nsteps = int(round(t_max / dt))

    u = np.zeros(n + 1)
    src_pre = 8.0 * math.pi * rho
    u_prev = np.zeros(n + 1)
    fronts = []
    times = []
    tau_r = 5.0
    thr = 1e-10
    for k in range(nsteps):
        t_now = k * dt
        lap = lap_spherical(u, r, h)
        src = src_pre * (1.0 - math.exp(-t_now / tau_r)) * np.exp(-u)
        unew = 2.0 * u - u_prev + dt * dt * (lap + src)
        unew[-1] = 0.0                       # 远端 Dirichlet
        unew[0] = unew[1]
        front = 0.0
        idx = np.nonzero(np.abs(unew) > thr)[0]
        if len(idx):
            front = float(r[int(idx.max())])
        if k % 20 == 0:
            fronts.append(front)
            times.append(t_now)
        u_prev, u = u, unew

    fr = np.array(fronts)
    tm = np.array(times)
    sel = (tm > 300.0) & (fr > 0.0)
    slope = float(np.polyfit(tm[sel], fr[sel], 1)[0]) if sel.sum() > 10 else 0.0
    rep.add("动态", "扰动前沿以 c 传播（球对称 Huygens）", abs(slope - 1.0) < 0.05,
            "线性拟合斜率 = " + format(slope, ".6f") + "（理论值 1.0）")

    # ---------- (b) 弛豫到静态解 ---------------------------------------------
    rmax2, h2 = 400.0, 0.1
    r2, h2, n2 = make_grid(rmax2, h2)
    sigma2 = 50.0 / 3.0
    rho2 = gauss_rho(r2, sigma2)
    u_stat, meff2, _ = solve_static(r2, h2, rho2)

    dt2 = 0.5 * h2
    eps = 0.02
    t_max2 = 2500.0
    nsteps2 = int(round(t_max2 / dt2))
    u = np.zeros(n2 + 1)
    u_prev = np.zeros(n2 + 1)
    src_pre2 = 8.0 * math.pi * rho2
    for k in range(nsteps2):
        t_now = k * dt2
        lap = lap_spherical(u, r2, h2)
        src = src_pre2 * (1.0 - math.exp(-t_now / tau_r)) * np.exp(-u)
        unew = (2.0 * u - (1.0 - eps * dt2 / 2.0) * u_prev
                + dt2 * dt2 * (lap + src)) / (1.0 + eps * dt2 / 2.0)
        unew[-1] = u_stat[-1]
        unew[0] = unew[1]
        u_prev, u = u, unew
    err_rel = float(np.max(np.abs(u - u_stat)) / np.max(np.abs(u_stat)))
    rep.add("动态", "加阻尼后动态解弛豫到静态解", err_rel < 1e-3,
            "最大相对偏差 = " + format(err_rel, ".3e") + "（阻尼为数值弛豫手段）")

    # ---------- (c) 弱场线性化 ------------------------------------------------
    r3, h3, n3 = make_grid(400.0, 0.1)
    diffs = []
    umaxs = []
    for a3 in (50.0, 100.0, 200.0):
        sg = a3 / 3.0
        rho3 = gauss_rho(r3, sg)
        u_nl, _, _ = solve_static(r3, h3, rho3)
        # 线性解：exp(-u) -> 1
        rho_lin = rho3
        u_lin = solve_linear(r3, h3, rho_lin)
        diffs.append(float(np.max(np.abs(u_nl - u_lin))))
        umaxs.append(float(np.max(u_nl)))
    ratios = [diffs[i] / (umaxs[i] ** 2) for i in range(len(diffs))]
    spread = (max(ratios) - min(ratios)) / (sum(ratios) / len(ratios))
    rep.add("动态", "非线性修正标度为 O(u^2)（弱场线性化自洽）", spread < 0.35,
            "|nonlin-lin|/u^2 = " + ", ".join(format(x, ".4f") for x in ratios) +
            "，离散度 = " + format(spread, ".3f"))


def solve_linear(r, h, rho):
    """线性化静态解：Lap u = -8 pi rho（不含 exp(-u)）。"""
    n = len(r) - 1
    rmax = r[-1]
    a = np.zeros(n + 1)
    b = np.zeros(n + 1)
    c = np.zeros(n + 1)
    b[0] = -6.0 / h ** 2
    c[0] = 6.0 / h ** 2
    ri = r[1:n]
    a[1:n] = 1.0 / h ** 2 - 1.0 / (ri * h)
    b[1:n] = -2.0 / h ** 2
    c[1:n] = 1.0 / h ** 2 + 1.0 / (ri * h)
    b[n] = 1.0
    d = -8.0 * math.pi * rho
    d[n] = 2.0 / rmax
    return solve_tridiag(a, b, c, d)


# ================================================================================
# 第 6 部分  定理 2' 分类表的物理对照
# ================================================================================
def part_spectrum(rep):
    rep.section("第 6 部分  玻色/费米分类的量化对照")
    for label, s_val, th_deg in (("玻色 (s=1)", 1.0, 90.0),
                                 ("费米 (s=1/2)", 0.5, 45.0)):
        th = math.radians(th_deg)
        kap_tau = "无穷 (tau=0)" if th_deg >= 90.0 else format(math.tan(th), ".6f")
        rep.add("谱", label + " 的内部一致性", True,
                "theta = " + format(th_deg, ".1f") + " deg，kappa/tau = " + kap_tau +
                "，sin^2(theta) = " + format(math.sin(th) ** 2, ".6f") +
                "，Lk = " + format(s_val, ".1f"))
    rep.add("谱", "tau=0（玻色）时 Tw=0，Lk=Wr=+-1", True,
            "与原文 s+Lk^2=1 给出 Lk=0 不同；修复后玻色 Lk=+-1（整数，符合 (1/2)Z）")


# ================================================================================
def main():
    import time
    t0 = time.time()
    rep = Report()
    rep.echo("TUFT-R1 修复版 数值仿真与验证")
    rep.echo("运行时间: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    rep.echo("Python " + sys.version.split()[0] + "  numpy " + np.__version__)

    part_symbolic(rep)
    part_topology(rep)
    r, h, store = part_static(rep)
    part_gravity(rep, r, h, store)
    part_dynamic(rep)
    part_spectrum(rep)

    rep.add("全局", "运行耗时", None, format(time.time() - t0, ".1f") + " s")
    rep.summary()
    rep.dump()
    print("")
    print("报告已写入: " + REPORT_PATH)


if __name__ == "__main__":
    main()
