# -*- coding: utf-8 -*-
"""
TUFT 宇宙暴胀 / 原初扰动 / CMB 可观测预言 · 全维求导证明与精算
对象：《TUFT 全维统一场论：宇宙暴胀、原初扰动与 CMB 可观测预言》§1-§8
方法：sympy 势能与慢滚符号求导 + scipy 逐行复现原文 ODE + 观测对标（Planck2018 / BICEP-Keck）
红线：数学自洽 != 物理实验证实。
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
REPORT_PATH = os.path.join(HERE, "tuft_暴胀CMB_report.txt")

# 观测锚
NS_OBS = 0.9649          # Planck 2018 (TT,TE,EE+lowE+lensing)
NS_ERR = 0.0042
R_UPPER = 0.036          # BICEP/Keck 2021, r_0.05 < 0.036 (95% CL)
L_P = 1.616255e-35
GEV_INV_M = 1.0 / 1.973269804e-16      # 1 GeV = 1/1.973e-16 m^-1
K_SAT_M = 1.0 / L_P ** 2               # m^-2
K_SAT_GEV2 = (GEV_INV_M / L_P) ** 2    # GeV^2
T_VEV_GEV = 246.0                      # 第一册 §2.3 的挠率真空期望值
T_REH_GEV = 1.0e14
T_EW_GEV = 100.0


class Report(object):
    def __init__(self):
        self.rows = []
        self.lines = []

    def echo(self, t=""):
        print(t)
        self.lines.append(t)

    def section(self, t):
        self.echo("")
        self.echo("=" * 78)
        self.echo(t)
        self.echo("=" * 78)

    def add(self, sec, name, verdict, detail=""):
        self.rows.append((sec, name, verdict, detail))
        line = "  [" + verdict + "] " + name
        if detail:
            line += "   |  " + detail
        self.echo(line)

    def summary(self):
        from collections import Counter
        cnt = Counter(v for _, _, v, _ in self.rows)
        self.section("汇总")
        for k in ["PASS", "FAIL", "BOUNDARY", "INFO"]:
            self.echo("  %-9s = %d" % (k, cnt.get(k, 0)))
        if cnt.get("FAIL"):
            self.echo("  存在 FAIL（真实缺陷）:")
            for sec, name, v, det in self.rows:
                if v == "FAIL":
                    self.echo("    - [" + sec + "] " + name)
        return cnt

    def dump(self):
        with open(REPORT_PATH, "w", encoding="utf-8") as fh:
            fh.write("\n".join(self.lines))
            fh.write("\n")


def V(om, V0=1.0):
    return V0 * om * (1.0 - om)


def dV(om, V0=1.0):
    return V0 * (1.0 - 2.0 * om)


def part1_potential(rep):
    import sympy as sp
    rep.section("§1  暴胀子身份与势能 V=Omega(1-Omega)：形状与稳定性")
    om, V0 = sp.symbols("Omega V0", positive=True)
    Vv = V0 * om * (1 - om)
    rep.add("P1.1", "势能 V(Omega) = V0*Omega*(1-Omega) 的形状", "FAIL",
            "V'' = %s < 0 —— 该势在 (0,1) 上是**凹函数**，唯一驻点是 **Omega=1/2 处的极大值**"
            "（V= V0/4）。原文称'双势阱、两个极小值在 Omega=0 与 Omega=1'："
            "Omega=0/1 只是**边界零点**，中间是**极大值（势垒顶）**，不是势阱。"
            "真正的双势阱是 V=λ(Omega^2-v^2)^2 形式。术语与拓扑均不成立。"
            % sp.simplify(sp.diff(Vv, om, 2)))
    rep.add("P1.2", "Omega=0 是否为稳定初始真空", "FAIL",
            "V'(0) = V0 != 0 -> Omega=0 **不是驻点**（场被推离 0）。原文称'Omega=0 完全无物质的纯真空态'"
            "并作为暴胀前初始态，但该点不稳定、亦非极值。")
    rep.add("P1.3", "Omega_DE = 0.6875 是否为势能亚稳态极小值", "FAIL",
            "V'(0.6875) = V0(1-2*0.6875) = %.4f*V0 != 0，且 V''<0 -> "
            "Omega=0.6875 **既非驻点也非极小值**（在凹函数下降段）。"
            "按运动方程 3H*Omega_dot = -V' = +0.375*V0 > 0 场会**远离**该点奔向 Omega=1。"
            "故'暗能量基底是势能曲面上的亚稳态极小值'与自身势能矛盾。" % (1 - 2 * 0.6875))
    rep.add("P1.4", "动能项与势能项的量纲一致性", "FAIL",
            "L_Omega = 1/2 g^{mu nu} d_mu Omega d_nu Omega - V(Omega)：若 Omega **无量纲**，"
            "则动能项量纲 = M^2，而 V0*Omega*(1-Omega) 量纲 = M^4（能量密度）-> **不匹配**。"
            "要合法须写 1/2 M_P^2 (d Omega)^2 或令 phi = M_P*Omega（此时 Omega_DE=0.6875 这类"
            "无量纲数值需另行解释）。原文未给归一化，导致后续慢滚参数的 kappa 取值约定混乱（见 §2）。")
    rep.add("P1.5", "'暴胀子是内生场、不需额外引入'", "FAIL",
            "势能立即引入自由参数 **V0**（能量标度），且 V0 是全篇唯一未被任何几何量固定的量"
            "（§5 反由 T_reh 反推）。'内生'仅指符号出现在前册作用量的 L_Omega 占位符中，"
            "而该占位符在前册从未给出具体形式 -> 实为**新增输入**。")


def part2_slowroll(rep):
    import sympy as sp
    rep.section("§2  慢滚动力学：方向、e-folds 与谱指数的自洽性（核心）")
    rep.add("P2.1", "运动方程 3H*Omega_dot = -V' 的滚动方向", "FAIL",
            "自 Omega_i = 0.05（左侧）出发，V' = V0(1-2*0.05) = +0.9*V0 > 0 -> "
            "Omega_dot = -V'/(3H) < 0 -> **Omega 减小**、朝 Omega=0 滚，**永远不会到达 0.5**。"
            "原文称'Omega 从 0.05 缓慢滚向 0.5 到达势能极大值'——方向与其自身方程相反"
            "（要爬向极大值需 Omega_dot>0，即 V'<0，需 Omega>0.5 出发）。")

    om = sp.symbols("Omega", positive=True)
    ratio = (1 - 2 * om) / (om * (1 - om))          # V'/V
    eps = sp.Rational(1, 2) * ratio ** 2 / sp.Symbol("kappa")
    eta = -2 / (om * (1 - om)) / sp.Symbol("kappa")
    rep.add("P2.2", "慢滚参数公式形式", "PASS" if True else "",
            "eps = (1/(2 kappa))(V'/V)^2、eta = (1/kappa)(V''/V)、n_s = 1-6eps+2eta、"
            "N = kappa ∫ V/V' dOmega —— 公式**结构**与标准慢滚一致 ✓"
            "（但 kappa 的取值约定见 P2.5/P2.6）。")

    # 数值：e-folds 积分（解析 + 数值）
    def I_int(om_f, om_i):
        xs = np.linspace(om_f, om_i, 400001)
        f = xs * (1.0 - xs) / (1.0 - 2.0 * xs)
        return abs(float(np.trapz(f, xs)))

    I_45 = I_int(0.45, 0.05)
    rep.add("P2.3", "e-folds 积分 kappa ∫_{Om_f}^{Om_i} Om(1-Om)/(1-2Om) dOm", "FAIL",
            "数值积分（0.05 <-> 0.45，正上方被积函数）得 |I| = %.6f；故 **N = %.4f * kappa**。"
            "原文在 kappa=1（其代码取值）下声称 N≈60：实为 N ≈ %.2f，**相差 %.0f 倍**。"
            "另注意方向：该积分沿 Omega **上升**段计；而实际下滚方向（0.05 -> 0）累计 e-folds "
            "仅 0.0421（见 P6.2），且被积函数在 Om_f -> 0.5 时发散（1/(1-2Om)），"
            "故真正的'暴胀结束'点并非极大值点。"
            % (I_45, I_45, I_45, 60.0 / I_45))

    kap_N = 60.0 / I_45
    rep.add("P2.4", "若要 N=60，所需 kappa", "FAIL",
            "kappa = 60/%.6f = %.1f。而按公式约定（epsilon 无量纲要求 kappa 无量纲）"
            "标准取值应为 kappa = 1（普朗克单位下 8 pi G/c^4 归一）-> "
            "需要 kappa 大 %.0f 倍，即势能/普朗克单位错配 %.0f 倍。"
            % (I_45, kap_N, kap_N, kap_N))

    # n_s
    def C_om(o):
        return 3.0 * ((1 - 2 * o) / (o * (1 - o))) ** 2 + 4.0 / (o * (1 - o))

    C45 = C_om(0.45)
    kap_ns = C45 / (1.0 - NS_OBS)
    rep.add("P2.5", "若要 n_s = 0.9649，所需 kappa", "FAIL",
            "1 - n_s = (1/kappa)[3(V'/V)^2 + 4/(Om(1-Om))]；在 Om=0.45 括号值 = %.3f，"
            "故 kappa = %.3f/%.4f = %.1f。与 P2.4 的 kappa = %.1f **不一致**"
            "（相差 %.2f 倍）——同一模型两处'✅ 吻合'彼此矛盾。"
            % (C45, C45, 1.0 - NS_OBS, kap_ns, kap_N, kap_ns / kap_N))

    # kappa 无关不变量
    prod_model = I_45 * C45
    prod_obs = 60.0 * (1.0 - NS_OBS)
    rep.add("P2.6", "kappa 无关不变量 N*(1-n_s) 检验（关键）", "FAIL",
            "N 与 (1-n_s) 均正比/反比于 kappa，故乘积 **与 kappa 无关**："
            "模型在 Om_f=0.45 给 N*(1-n_s) = %.3f * %.3f = **%.3f**；"
            "观测要求 60 * %.4f = **%.3f**。比值 %.2f -> "
            "'N≈60 与 n_s≈0.965 完全吻合'在任何 kappa 下都不同时成立。"
            % (I_45, C45, prod_model, 1.0 - NS_OBS, prod_obs, prod_model / prod_obs))
    # 扫 Om_f 找可同时满足的（Om_f, kappa）
    best = None
    for of in np.linspace(0.06, 0.4999, 3000):
        I_ = I_int(of, 0.05, )
        prod = I_ * C_om(of)
        if abs(prod - prod_obs) < 0.002 and (best is None or abs(prod - prod_obs) < best[0]):
            best = (abs(prod - prod_obs), of, I_, prod, 60.0 / I_)
    if best:
        rep.add("P2.7", "唯一致命处：调 Om_f 能否同时满足 N=60 与 n_s", "FAIL",
                "扫描 Om_f 可找到 Om_f ≈ %.4f 使 N(1-n_s) = %.3f（观测值）；但此时要求 "
                "kappa = 60/I = %.0f —— 仍是 kappa=1 的 %.0f 倍。"
                "即：**必须同时调节 Om_f 与 kappa（两个非物理自由度）**才能复现观测，"
                "而 kappa 是固定常数、V0 完全不影响 N 与 n_s（见 P2.8）-> 模型实际只有 1 个可用标度，"
                "无法同时固定 N 与 n_s。" % (best[1], best[3], best[4], best[4]))
    rep.add("P2.8", "自由参数 V0 对 N 与 n_s 的作用", "FAIL",
            "N = kappa∫V/V' dOm 与 n_s = 1-6eps+2eta 中 **V0 完全相消**（幂次齐次）。"
            "故唯一的势能标度参数 V0 无法调整 N/n_s；模型的可观测预言只由 (Om_i, Om_f, kappa) 决定，"
            "而 kappa 是物理常数 -> 自由度审计：**两个观测量、零个可调尺度参数**。")
    rep.add("P2.9", "慢滚条件在所称初始点 Omega_i=0.05 是否成立", "FAIL",
            "eps(0.05) = (1/2kappa)((1-0.1)/(0.05*0.95))^2 = %.3f/kappa；"
            "kappa=1 时 eps = %.1f **>> 1**（慢滚在起点即失效，暴胀无法启动）；"
            "eta(0.05) = %.1f/kappa。要 eps(0.05)<1 需 kappa > %.1f。"
            % (0.5 * ((1 - 0.1) / (0.05 * 0.95)) ** 2, 0.5 * ((1 - 0.1) / (0.05 * 0.95)) ** 2,
               -2.0 / (0.05 * 0.95), 0.5 * ((1 - 0.1) / (0.05 * 0.95)) ** 2))


def part3_spectra(rep):
    rep.section("§3  原初扰动谱：r、挠率增强因子 F_T 与可判决性")
    om_f = 0.45
    eps_unit = 0.5 * ((1 - 2 * om_f) / (om_f * (1 - om_f))) ** 2
    rep.add("P3.1", "张量-标量比 r = 16*eps（标准关系）", "PASS",
            "P_T = 2 kappa H^2/pi^2、P_R = kappa H^2/(8 pi^2 eps) -> r = 16 eps ✓ 标准关系成立。")
    rep.add("P3.2", "原文自身的 r（不含 F_T）", "FAIL",
            "在 Om=0.45：eps = %.4f/kappa。取 kappa=1（其代码取值）-> eps = %.4f，"
            "r = 16*eps = **%.3f**，被 BICEP/Keck 上限 r<%.3f **超出 %.0f 倍**（模型被直接排除）；"
            "取复现 n_s 所需的 kappa=%.1f -> eps = %.2e，r = %.5f（这才≈原文所称'标准 0.003'）。"
            "即原文的 r 结论依赖于一个被隐式选定的巨大 kappa。"
            % (eps_unit, eps_unit, 16 * eps_unit, R_UPPER, 16 * eps_unit / R_UPPER,
               475.7, eps_unit / 475.7, 16 * eps_unit / 475.7))
    t_gev = T_VEV_GEV * GEV_INV_M
    ratio = t_gev ** 2 / (K_SAT_GEV2 / GEV_INV_M ** 2) ** 2 if False else (t_gev ** 2) / (K_SAT_M ** 2)
    rep.add("P3.3", "挠率增强因子量纲：F_T = 1 + <T>^2/K_sat^2", "FAIL",
            "[T] = L^-1（挠率/联络量纲），[K_sat] = L^-2 -> [<T>^2/K_sat^2] = **L^2** != 1，"
            "并非无量纲修正因子 -> 公式量纲非法。")
    F_T = 1.0 + ratio
    rep.add("P3.4", "F_T 的数值（取第一册 <T> = v = 246 GeV）", "FAIL",
            "<T> = 246 GeV = %.4e m^-1；K_sat = %.4e m^-2 -> <T>^2/K_sat^2 = %.3e -> "
            "**F_T = 1 + %.1e ≈ 1.000...0（小数点后 102 位）**，即增强完全不存在。"
            "而要让 r 从 %.5f 升到 0.01~0.05，需 F_T = %.2f~%.2f（即 3~18 倍增强）"
            "-> 与公式给出值相差 %.0f~%.0f 个数量级。"
            % (t_gev, K_SAT_M, ratio, ratio, 16 * (eps_unit / 475.7),
              0.01 / (16 * eps_unit / 475.7), 0.05 / (16 * eps_unit / 475.7),
              98.0, 102.0))
    rep.add("P3.5", "代码中 F_T = 1.5 与 §3.2 公式的一致性", "FAIL",
            "代码硬编码 F_T = 1.5；而按 §3.2 公式（<T>=246 GeV）F_T ≈ 1，按所需增强应为 3.6~18.2。"
            "三处取值互不一致 -> '挠率增强'没有任何被计算的来源。")
    rep.add("P3.6", "'传统慢滚预言 r≈0.003，TUFT 预言 0.01~0.05'", "FAIL",
            "0.003 并非'传统模型'的预言，而是**本模型自身**在 kappa=475.7 时的 16*eps 值"
            "（= %.5f）。原文把同一模型的数值一半归给'传统'、另一半靠未计算的 F_T 归给 TUFT，"
            "属**同一模型的自我对比**。" % (16 * eps_unit / 475.7))
    rep.add("P3.7", "标量功率谱 P_R = kappa H^2/(8 pi^2 eps)", "PASS", "标准形式 ✓（kappa=1/M_P^2 约定）")
    rep.add("P3.8", "n_s = 1 - 6eps + 2eta 公式结构", "PASS", "标准慢滚公式 ✓（数值问题见 §2）")


def part4_chirality(rep):
    rep.section("§4  原初挠率扰动的手性（Pi_T）审查")
    rep.add("P4.1", "手性来源：'弱相互作用的手性破缺使 T_L != T_R'", "FAIL",
            "能标矛盾：暴胀/重加热能标 T_reh ≈ %.0e GeV，而电弱对称破缺发生在 ≈ %.0f GeV，"
            "二者相差 **%.0f 个数量级**。暴胀期间电弱对称性未破缺 -> 不存在可继承的'弱作用手性破缺'。"
            "以 EW 手性破缺作为原初引力波手性的来源在能标上不成立。"
            % (T_REH_GEV, T_EW_GEV, math.log10(T_REH_GEV / T_EW_GEV)))
    rep.add("P4.2", "Pi_T ≈ 0.05~0.15 的推导", "FAIL",
            "全篇未给左手/右手张量模式的**模式方程、源项或视界外演化**；"
            "0.05~0.15 是直接给定的数 -> 不可计算、不可证伪（数值落在任何区间都无法核对）。")
    rep.add("P4.3", "'传统引力理论预言 Pi_T = 0'", "PASS",
            "纯黎曼几何下宇称守恒、左右手张量谱相等 -> Pi_T = 0 ✓（陈述正确）。")
    rep.add("P4.4", "若存在非零 Pi_T 的观测通道", "BOUNDARY",
            "非零 Pi_T 会在 CMB 产生 **TB / EB** 关联谱，是原理上可测的（LiteBIRD/CMB-S4 目标量级）。"
            "但原文未给任何定量预言（如 Pi_T 与 r、与能标的关系）-> 无法与数据比对。")
    rep.add("P4.5", "Pi_T 与 S14-A2/A3 的内部一致性", "BOUNDARY",
            "首册已判'TUFT 作用量无挠率动能项 -> 挠率为代数约束、真空挠率为零'（B1.9）："
            "若无 T 的独立动力学，则原初挠率涨落也无独立自由度，Pi_T 更无从产生。"
            "本册的挠率扰动与自身作用量存在同一矛盾。")


def part5_reheating(rep):
    rep.section("§5  暴胀结束与重加热审查")
    rep.add("P5.1", "'Omega 滚到 Omega≈0.5 势能极大值，慢滚破坏，暴胀结束'", "FAIL",
            "两处错误：(1) 方向反了（§2.1：从 0.05 出发滚向 0）；"
            "(2) Omega=0.5 是**极大值**，慢滚参数在此处发散（eps -> ∞），"
            "真正需要的是场**越过**该点进入第二侧；原文把'到达极大值'当作结束条件，无动力学依据。")
    rep.add("P5.2", "T_reh ≈ (V0/g_*)^(1/4)", "BOUNDARY",
            "量纲正确（V0^(1/4) = 能量）✓；但标准公式含数值因子 T_reh ≈ (30 V0/(pi^2 g_*))^(1/4)，"
            "原文省略 -> 含 O(1) 因子误差（可修）。")
    rep.add("P5.3", "T_reh ≈ 1e14 GeV 的来源", "FAIL",
            "该数值是**直接给定**的，不是从 V0 算出；而 §1.5 又称 V0'由几何权重势的尺度决定'。"
            "两端互为循环：V0 未定 -> T_reh 取自用户设定 -> 再声称远低于普朗克能标。"
            "数值核对：T_reh = 1e14 GeV 对应 V0 = g_* T_reh^4 = %.3e GeV^4，"
            "而普朗克密度 M_P^4 = %.3e GeV^4 -> V0/M_P^4 = %.2e（需 %.0e 量级调节）。"
            % (106.75 * T_REH_GEV ** 4, 1.2209e19 ** 4, 106.75 * T_REH_GEV ** 4 / 1.2209e19 ** 4,
               T_REH_GEV ** 4 / 1.2209e19 ** 4))
    rep.add("P5.4", "重加热粒子生成：'Omega 振荡 -> 夸克/轻子/规范玻色子/暗物质'", "FAIL",
            "无任何定量：无衰变率 Gamma、无耦合项系数、无再加热温度与粒子的产率计算，"
            "也无暗物质丰度（观测 Omega_dm = 0.2645）。'曲率-挠率形变凝结为粒子'是命名而非机制。")
    rep.add("P5.5", "'TUFT 自动衔接 LambdaCDM'", "BOUNDARY",
            "若暴胀与重加热完成，后续标准热大爆炸演化确实无需改动 -> 逻辑上可衔接；"
            "但这也意味着本册**不产生**辐射/物质主导期的新预言，'衔接'= 回归标准宇宙学。")


def part6_code(rep):
    rep.section("§6  原文仿真代码逐行复现与声称核对")
    from scipy.integrate import solve_ivp
    kappa, V0 = 1.0, 1.0

    def equations(t, y):
        Om, dOm = y
        H = math.sqrt(kappa / 3.0 * (0.5 * dOm ** 2 + V(Om, V0)))
        return [dOm, -3.0 * H * dOm - dV(Om, V0)]

    # (1) 按原文默认设置直接跑
    err = ""
    try:
        solve_ivp(equations, (0.0, 100.0), [0.05, 0.0], t_eval=np.linspace(0.0, 100.0, 2000), method="RK45")
    except Exception as exc:
        err = type(exc).__name__ + ": " + str(exc)
    rep.add("P6.1", "原文代码能否跑完（t∈[0,100]）", "FAIL",
            "按原文默认设置实跑抛异常：**%s** —— 因 V = Omega(1-Omega) 在 [0,1] **之外为负**，"
            "场被推离 Omega=0 后越界使 H^2 < 0（sqrt 域错误）。即'仿真预期输出'的前提不成立。" % err)

    # (2) 域内受限积分（固定步长 RK4，遇 Omega<0 即停）定位越界点
    dt, om, dom, t = 1e-3, 0.05, 0.0, 0.0
    N_acc, t_exit, om_exit, dom_exit = 0.0, None, None, None
    om_max, om_min_seen = om, om
    for _ in range(200000):
        def f(o, d):
            return np.array([d, -3.0 * math.sqrt(kappa / 3.0 * (0.5 * d ** 2 + o * (1.0 - o))) * d
                             - (1.0 - 2.0 * o)])
        k1 = f(om, dom)
        k2 = f(om + 0.5 * dt * k1[0], dom + 0.5 * dt * k1[1])
        k3 = f(om + 0.5 * dt * k2[0], dom + 0.5 * dt * k2[1])
        k4 = f(om + dt * k3[0], dom + dt * k3[1])
        om2 = om + dt / 6.0 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        dom2 = dom + dt / 6.0 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        N_acc += dt * math.sqrt(kappa / 3.0 * (0.5 * dom ** 2 + om * (1.0 - om)))
        t += dt
        om, dom = om2, dom2
        om_max, om_min_seen = max(om_max, om), min(om_min_seen, om)
        if om < 0.0 or dom >= 0.0:
            t_exit, om_exit, dom_exit = t, om, dom
            break
    rep.add("P6.2", "'暴胀子从 0.05 缓慢滚向 0.5，在 N≈60 处到达极大值'", "FAIL",
            "域内受限积分（RK4, dt=1e-3）：Omega 自 0.05 **单调下降**、最大值 %.4f（= 初值），"
            "在 t = %.4f 处**越界到 Omega = %.4f (<0)**（此时 Omega_dot = %.4f）；"
            "**从未接近 0.5**。越界前累计 e-folds = **%.4f**（不是 60）。"
            "方向与'滚向 0.5'相反，且模型在越界处崩溃。" % (om_max, t_exit, om_exit, dom_exit, N_acc))
    rep.add("P6.3", "势能无下界（结构性缺陷）", "FAIL",
            "V = V0*Omega(1-Omega) 在 Omega<0 或 Omega>1 时为**负**，且 Omega -> -inf 时 V -> -inf："
            "势能**无下界**、真空不稳定；H^2 = (kappa/3)(1/2 Omega_dot^2 + V) 随之可为负。"
            "模型缺少场域约束（如 |Omega|<=1 的投影或非多项式势），故 §1 的'双势阱'图像不成立。")

    def stats(o):
        e = 0.5 / kappa * ((1.0 - 2.0 * o) / (o * (1.0 - o))) ** 2
        h = 1.0 / kappa * (-2.0 / (o * (1.0 - o)))
        return e, h, 1.0 - 6.0 * e + 2.0 * h, 16.0 * e * 1.5

    e0, h0, ns0, r0 = stats(0.05)
    e45, h45, ns45, r45 = stats(0.45)
    rep.add("P6.4", "'谱指数 n_s ≈ 0.965，与 Planck 吻合'", "FAIL",
            "kappa=1（代码取值）下：起点 Omega=0.05 给 eps = %.1f、eta = %.1f -> "
            "**n_s(0) = %.1f**（大负值），r(0) = %.1f；轨迹向 Omega->0 演化时 eps -> ∞，n_s -> -∞。"
            "即便取原文声称的结束点 Omega=0.45（轨迹实际到不了），"
            "也只是 n_s = %.2f、r = %.2f —— 均与 0.9649 与 r<%.3f 相距极远。"
            % (e0, h0, ns0, r0, ns45, r45, R_UPPER))
    rep.add("P6.5", "'r ≈ 0.03，在 CMB-S4 可探测范围内'", "FAIL",
            "代码实际给出 r(0) = 16*eps*F_T = %.1f（F_T=1.5），比 BICEP/Keck 上限 r<%.3f "
            "高 %.0f 倍；n_s 与 r 同时被排除 3~6 个量级。'r≈0.03' 在任何 kappa=1 的实现中都不出现。"
            % (r0, R_UPPER, r0 / R_UPPER))
    rep.add("P6.6", "代码硬编码 F_T = 1.5", "FAIL",
            "F_T = 1.5 与 §3.2 公式（<T>=246 GeV -> F_T ≈ 1）矛盾，且无计算来源；"
            "同时 §8 表格又称 r 的目标为 0.01~0.05（对应 F_T 需 3.6~18.2）。三处取值互斥。")
    rep.add("P6.7", "代码可运行性（LaTeX 残渣）", "FAIL",
            "原文代码含 LaTeX 残渣：plt.ylabel(r'$\\Omeg\\(a(t)\\)$')、"
            "plt.axhline(\\(0.965\\), ...) 等；`\\(`、`\\)` 在 Python 中不是合法表达式 -> "
            "**代码按原文粘贴无法运行**（SyntaxError；即便修好，也会在 P6.1 处抛 math domain error）。")
    rep.add("P6.8", "N_t = cumsum(H_t)*mean(diff(t)) 的积分方式", "BOUNDARY",
            "等价于一阶矩形法（步长由 linspace 决定），在 H 变化剧烈段有 O(1) 误差；"
            "应改为 cumtrapz 或求解器 dense output（可修，非主要问题）。")
    rep.add("P6.9", "'仿真预期输出'四条逐条核对", "FAIL",
            "(1) 'Omega 从 0.05 缓慢滚向 0.5' ✗（实测单调降至 0 并越界到负值，"
            "t_exit = %.4f，从未接近 0.5）；"
            "(2) 'H 近似常数、结束后快速下降' ✗（H 自 %.4f 单调下降，暴胀从未发生）；"
            "(3) 'n_s ≈ 0.965' ✗（实测 n_s(0) = %.1f，并随 Omega->0 趋向 -∞）；"
            "(4) 'r ≈ 0.03' ✗（实测 r(0) = %.1f）。四条全部与实跑不符。"
            % (t_exit, math.sqrt(kappa / 3.0 * V(0.05, V0)), ns0, r0))


def part7_chain(rep):
    rep.section("§7  宇宙学全链条与 LambdaCDM 对比表审查")
    rep.add("P7.1", "全链条表（量子引力 -> 暴胀 -> 重加热 -> 辐射 -> 物质 -> 暗能量）", "BOUNDARY",
            "表是**阶段命名**：除暴胀段（本册，且 §2/§6 已判 FAIL）外，其余各段的'TUFT 几何对应'"
            "均无计算（如'辐射主导：挠率行波主导能量密度'与标准辐射主导不同，未给证据）。")
    rep.add("P7.2", "对比表：'LambdaCDM 预言 n_s = 0.965'", "FAIL",
            "概念错误：n_s 是**暴胀模型的参数/预言**，LambdaCDM 不含暴胀动力学，"
            "只把 n_s（及 r）作为拟合参数。故不能写'LambdaCDM 预言 0.965 且与 TUFT 相同'。")
    rep.add("P7.3", "对比表：'LambdaCDM 预言 r ~ 0.003'", "FAIL",
            "同上：纯 LambdaCDM（无原初张量谱）对应 **r = 0**；0.003 是慢滚暴胀模型的数值，"
            "而且正是本模型在 kappa=475.7 时的自值（见 P3.6）。对比表把'传统'与'本模型'混为两方。")
    rep.add("P7.4", "对比表：'暗物质不存在，是曲率形变；直接探测将一无所获'", "BOUNDARY",
            "这是本册**唯一可判决**的强预言（原理上可由 LZ/XENONnT 类实验与宇宙学丰度检验）；"
            "但原文未给任何丰度/截面计算（Omega_dm=0.2645 无法复现），"
            "且'WIMP 未被发现'本身不构成该预言的证据（非 WIMP 粒子暗物质如轴子仍可能）。")
    rep.add("P7.5", "对比表：'H0 张力可由挠率修正消解'", "FAIL",
            "无量化：未给挠率修正对 H(z) 或距离梯度的具体改动（无 Delta H0 表达式）-> 不可检验。")
    rep.add("P7.6", "'宇宙组分 6.25/25/68.75 内生'", "FAIL",
            "首册已判：与 Planck 2018（4.93/26.45/68.47）相比重子偏差 **+26.8%**；"
            "本册未给新计算，'内生'仍是数值声明。（暗能量 68.75 vs 68.47 差 0.41% 接近。）")


def part8_fix(rep):
    rep.section("§8  修复方案（分析 -> 处理 -> 修复 -> 优化）")
    fixes = [
        ("P1.1/P1.3", "势能改注明为'凹函数、Omega=1/2 为极大值'；若要暗能量亚稳态须改用真正的双势阱"
                      "（如 V=λ(Omega^2-Omega_DE^2)^2 + 曲率-挠率修正项）"),
        ("P1.4", "补正则归一化：1/2 M_P^2 (dOmega)^2（或 phi = M_P Omega），使动能/势能量纲一致"),
        ("P2.1", "修正滚动方向：要么改由 Omega>0.5 出发（V'<0 -> 向 0.5 爬），要么把势能翻转为 "
                 "V=V0(1/2-Omega)^2 型（Omega=0.5 为极小值，场向下滚）"),
        ("P2.3-P2.8", "删除'N≈60 ✅'与'n_s≈0.965 ✅'，改为如实标注：kappa=1 时 N=0.24、n_s=-15.7；"
                      "两个目标需 kappa≈250 与 ≈476（互斥）；V0 不影响 N/n_s"),
        ("P3.3/P3.4", "F_T 改为量纲合法的 1 + <T>^2/M_*^4 或 1 + <T>/M_*（须含普朗克量纲因子）；"
                      "删除 1.5 与 0.01~0.05 的任意取值"),
        ("P4.1/P4.2", "删除'弱作用手性破缺'作为暴胀期手性来源（能标差 12 个量级）；"
                      "若要 Pi_T 非零，须给出宇称破坏项（如 Chern-Simons 型 T∧R）及模式方程"),
        ("P5.3", "T_reh 由 V0 计算（含 30/pi^2 因子），或如实声明 V0 为自由标度并登记其微调量级"),
        ("P6.x", "代码：补单位约定；修正滚动方向/终止条件；F_T 与 §3.2 统一；清除 LaTeX 残渣"),
        ("P7.2/P7.3", "对比表改为'慢滚暴胀（本模型）'vs'观测'，不得把 LambdaCDM 写成含 n_s/r 的动力学预言"),
    ]
    for tag, how in fixes:
        rep.add("FIX", "[" + tag + "] " + how, "INFO", "")
    rep.add("FIX.10", "优化：本册降级为'单场暴胀的定性类比 + 观测对标（未通过）'", "BOUNDARY",
            "在补齐(1)正则归一的势能 (2)可复现 N 与 n_s 的参数选择 (3)F_T 的构造性来源 (4)Pi_T 的模式方程 "
            "之前，'TUFT 宇宙学全链条闭环'与'三个核心可证伪预言'均不成立；"
            "唯一原理上可判决的预言是 Pi_T 与'暗物质非粒子'，但当前无定量。")


def main():
    t0 = time.time()
    rep = Report()
    rep.echo("TUFT 宇宙暴胀 / 原初扰动 / CMB 可观测预言 · 全维求导证明与精算")
    rep.echo("run at: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    rep.echo("Python " + sys.version.split()[0] + "  numpy " + np.__version__ + " (scipy solve_ivp)")
    rep.echo("观测锚: Planck2018 n_s = %.4f +/- %.4f ; BICEP/Keck r_0.05 < %.3f" % (NS_OBS, NS_ERR, R_UPPER))
    part1_potential(rep)
    part2_slowroll(rep)
    part3_spectra(rep)
    part4_chirality(rep)
    part5_reheating(rep)
    part6_code(rep)
    part7_chain(rep)
    part8_fix(rep)
    rep.add("全局", "运行耗时", "INFO", "%.2f s" % (time.time() - t0))
    rep.summary()
    rep.dump()
    print("")
    print("report -> " + REPORT_PATH)


if __name__ == "__main__":
    main()
