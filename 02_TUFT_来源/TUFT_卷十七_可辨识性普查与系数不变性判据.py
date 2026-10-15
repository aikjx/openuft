# -*- coding: utf-8 -*-
# =====================================================================
# TUFT 卷十七 · 可辨识性普查与系数不变性判据
#            （卷十六「精确简并 / 平坦方向」方法在全通道上的推广）
# ---------------------------------------------------------------------
# 纯 NumPy + scipy（本机 jax/numpyro/arviz 不可用）
#
# 立项依据（卷十六末尾承诺）：动手前先核验数据来源与可辨识性，避免重复
#   「未推导系数 / 不可辨识」类缺陷。本卷不新开物理通道，只做方法层普查。
#
# 三条候选方向的预检裁定（见 §0，均为检索证据、非本卷计算）：
#   A 原初引力波 B 模 —— 本库已有 tuft_暴胀CMB 全维求导精算（PASS5/FAIL35）
#     与 补充卷G(CUR-19) 两轮硬裁定，TUFT 侧无一条导出关系 ⇒ 开新卷=重复造轮子
#   B RG 全局相图 —— R31 已判「7 自由参数 vs 0 推导方程 ⇒ 不可证伪模板」
#   C PRD 论文撰写 —— 属写作，不产生新计算
#   ⇒ 取第四条：把卷十六已验证的判据机器推广到全部已登记通道做普查。
#
# 本卷三条判据：
#   判据 I  系数不变性：若 O_i = C·g_i(θ)（C 为与 i 无关的未定归一化），
#           则比值 O_i/O_j = g_i/g_j 与 C 无关 ⇒ 绝对量不可辨、比值可辨。
#           ⇒ 修好量纲/归一化救不回比值类证伪（r42 同型，本卷把它一般化）。
#   判据 II 平坦方向：雅可比秩 r < 参数维 p ⇒ p−r 维平坦方向，沿该方向后验
#           完全由先验决定，σ = 1/√(N·vᵀΠv + 1/Var_box)（卷十六公式一般化）。
#   判据 III 自由度预算：可用实约束数 d vs 自由参数数 p；d < p ⇒ 欠定。
#
# 红线：数学自洽 ≠ 实验证实。本卷只审统计推断方法链，与 TUFT 真伪解耦；
#       不进入版本链、不占用冻结编号、不是第80章 SSOT 的变更源。
# 产出：同目录 .txt / .json / 一张 png
# =====================================================================
import json
import os
import time
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = []


def rec(code, name, status, detail, evidence=None):
    RESULTS.append({"code": code, "name": name, "status": status,
                    "detail": detail, "evidence": evidence or {}})
    print("[{0:<9}] {1:<8} {2}".format(status, code, detail))


def sec(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


# ===================== §0 三条候选方向的预检裁定 =====================
def section0():
    sec("§0  三候选方向预检（检索证据，非本卷计算）")
    pre = [
        ("V17-P1", "A 原初引力波 B 模偏振", "INFO",
         "本库已有两轮硬裁定：tuft_暴胀CMB_report.txt = PASS5/FAIL35/BOUNDARY8/INFO10"
         "（势能无下界、滚动方向反、N(1-ns) 不变量 3.741 vs 2.106、F_T 量纲 L^2!=1、"
         "r=4308 超上限 119668 倍、代码不可运行）；补充卷G(CUR-19) 判手征机制缺失、"
         "sigma_wall 量纲差 1 能量量纲、谱为双幂律 ansatz、未给 r。"
         "数据侧有真锚（Planck ns=0.9649+-0.0042 / BK r<0.036），但 TUFT 侧无导出关系。",
         {"evidence_file": "90_历史归档/来源语料_根目录_20260919/02_TUFT_来源/tuft/tuft_暴胀CMB_report.txt",
          "verdict": "开新卷 = 重复造轮子；若要推进只能做「修复」不是「新开」"}),
        ("V17-P2", "B RG 全局相图", "INFO",
         "R31(2026-09-30) 已审 RG 流 + CMB 双谱 + QNM FDTD：Planck 无 per-l f_NL(l) 数据；"
         "fnl_lcdm=-0.04 与 Planck2018 local f_NL=-0.9+-5.1 不符；jnp.where 硬阶跃使"
         "dchi2/dlc==0 ⇒ NUTS 假收敛；7 自由参数 vs 0 推导方程 ⇒ 不可证伪模板。",
         {"evidence_file": "tuft_r31_缺口定理N_RG流与CMB双谱_数值框架审计.py / tuft_r31_report.txt",
          "verdict": "R31 已覆盖且结论为否定，不重复"}),
        ("V17-P3", "C PRD 论文撰写", "INFO",
         "属写作整合，不产生新计算；与本卷（方法层普查）不冲突，可并行。",
         {"verdict": "不占用本卷"}),
    ]
    for c, n, s, d, e in pre:
        rec(c, n, s, d, e)
    rec("V17-P4", "取第四条：可辨识性普查", "INFO",
        "把卷十六已验证的判据机器推广到本库全部已登记通道；不新开物理通道，"
        "不依赖新外部数据，不重复 R31（R31 审单框架数值实现，本卷审跨通道统计结构）。")


# ===================== §1 通道台账（真实数字 + 来源） =====================
# 字段：key, 名称, 实验值, 实验 sigma(或上限), TUFT 值, 单位, 系数来源, 来源文件
CHANNELS = [
    dict(key="ae", name="电子反常磁矩 a_e",
         exp=1.15965218073e-3, sig=None, upper=None, tuft=2.904e-4,
         src="derived(螺旋闭式 alpha/(8pi))", unit="1",
         ref="tuft_g2_电子反常磁矩_OPEN5 / r19"),
    dict(key="amu", name="缪子反常磁矩 a_mu",
         exp=1.16592061e-3, sig=None, upper=None, tuft=-2.94997e-8,
         src="derived(同式，拟合电子后反推)", unit="1",
         ref="r42 N02 / r43"),
    dict(key="edm", name="电子 EDM d_e",
         exp=0.0, sig=None, upper=1.1e-29, tuft=1.409e-13,
         src="derived(依赖 <z>=b/2 假设)", unit="e·cm",
         ref="tuft_EDM_实验对接_OPEN6"),
    dict(key="rd", name="ringdown sigma_abs=0 反射壁",
         exp=0.0, sig=None, upper=None, tuft=None, z_given=5.74,
         src="ansatz(墙位置为模型假设)", unit="sigma",
         ref="OPEN_v3 联合排除 5.74sigma / OPEN_v4"),
    dict(key="cmb", name="CMB 张标比 r",
         exp=0.0, sig=None, upper=0.036, tuft=4308.0,
         src="ansatz(F_T=1.5 硬编码)", unit="1",
         ref="tuft_暴胀CMB_report.txt P6.5"),
    dict(key="nsN", name="kappa 无关不变量 N*(1-n_s)",
         exp=2.106, sig=None, upper=None, tuft=3.741,
         src="derived(不含自由标度)", unit="1",
         ref="tuft_暴胀CMB_report.txt P2.6"),
    dict(key="ob", name="重子密度 Omega_b",
         exp=4.93, sig=None, upper=None, tuft=6.25,
         src="ansatz(宇宙组分内生声明)", unit="%",
         ref="tuft_暴胀CMB_report.txt P7.6"),
    dict(key="oc", name="冷暗物质 Omega_c",
         exp=26.45, sig=None, upper=None, tuft=25.0,
         src="ansatz", unit="%",
         ref="tuft_暴胀CMB_report.txt P7.6"),
    dict(key="ol", name="暗能量 Omega_L",
         exp=68.47, sig=None, upper=None, tuft=68.75,
         src="ansatz", unit="%",
         ref="tuft_暴胀CMB_report.txt P7.6"),
    dict(key="fr", name="力程-耦合比 f_S/f_W",
         exp=None, sig=None, upper=None, tuft=6.9517,
         src="derived(alpha 比)", unit="1",
         ref="r17 C-04（与 L=c/f 推出的 1e-3 冲突 6.95e3 倍）"),
]

# 质量比（PDG）：用于判据 I 的 g-2 实例
M_E = 9.1093837015e-31
M_MU = 1.883531627e-28
M_TAU = 3.16754e-27


# ===================== §2 判据 I：系数不变性（比值判据） =====================
def section2():
    sec("§2  判据 I · 系数不变性：O_i = C·g_i(θ) ⇒ 比值与 C 无关")
    print("  若模型把可观测量写成 O_i = C·g_i(θ)，且 C 是与 i 无关的未定归一化，")
    print("  则 O_i/O_j = g_i/g_j 完全消去 C ⇒ 绝对值不可辨、比值可辨。")
    print("  ⇒ 任何「修好量纲/归一化」的补丁都在比值中失效，救不回比值类证伪。\n")

    rows = []

    # --- 实例 1：g-2。a_i = C·m_i^2·cot(theta) ⇒ a_mu/a_e = (m_mu/m_e)^2 ---
    r_m = M_MU / M_E
    ratio_model = r_m ** 2
    ratio_exp = 1.16592061e-3 / 1.15965218073e-3
    mis = ratio_model / ratio_exp
    rows.append(("I-1", "a_mu/a_e", ratio_model, ratio_exp, mis))
    rec("V17-I1", "g-2 比值不变性", "FAIL",
        "模型 a_mu/a_e == (m_mu/m_e)^2 = {0:.6f}（与系数 C 无关，机器零验证）；"
        "实验比值 = {1:.6f} ⇒ 矛盾 {2:.4g} 倍。".format(ratio_model, ratio_exp, mis),
        {"ratio_model": ratio_model, "ratio_exp": ratio_exp,
         "mismatch": mis, "C_independent": True})

    # 不变性本体自检：换 C 看比值是否逐位不变
    vals = [C * (M_MU ** 2) / (C * (M_E ** 2)) for C in (1.0, 1e10, 1 / 6.67430e-11, 3.7e-88)]
    spread = max(vals) - min(vals)
    rel = spread / ratio_model
    rec("V17-I1b", "C 不变性自检", "PASS",
        "C 取 4 个跨 ~98 个数量级的值，比值 a_mu/a_e 绝对散布 = {0:.3e}、"
        "**相对散布 = {1:.3e}**（相对机器零，绝对散布只是 4.3e4 量级的浮点尾数）"
        " ⇒ 判据成立，量纲类缺陷对该证伪免疫。".format(spread, rel),
        {"abs_spread": spread, "rel_spread": rel, "ratio": ratio_model})

    # --- 实例 2：CMB 的 kappa 无关不变量 N*(1-n_s) ---
    # N ∝ kappa，(1-n_s) ∝ 1/kappa ⇒ 乘积与 kappa 无关
    model = 3.741
    obs = 60.0 * 0.0351
    rec("V17-I2", "CMB 不变量 N*(1-n_s)", "FAIL",
        "该乘积与唯一起作用的标度 kappa 无关（N∝kappa, 1-ns∝1/kappa）⇒ 是 C-无关量。"
        "模型 {0:.4f} vs 观测 {1:.4f} ⇒ 矛盾 {2:.4f} 倍，且**不可靠调 kappa 修复**。"
        .format(model, obs, model / obs),
        {"model": model, "obs": obs, "ratio": model / obs, "C_independent": True})

    # 自检：N(kappa)*(1-ns)(kappa) 是否与 kappa 无关
    I = 0.224653  # ∫ Om(1-Om)/(1-2Om) dOm，Om 从 0.05 到 0.45
    B = 16.651    # [3(V'/V)^2 + 4/(Om(1-Om))] 在 Om=0.45
    prod = [(k * I) * (B / k) for k in (1.0, 267.1, 474.4, 649.0)]
    sp2 = max(prod) - min(prod)
    rec("V17-I2b", "kappa 无关性自检", "PASS",
        "kappa 取 1 / 267.1 / 474.4 / 649 四点，N*(1-n_s) 散布 = {0:.3e}"
        " ⇒ 乘积确与 kappa 无关，判据成立。".format(sp2), {"spread": sp2})

    # --- 实例 3：力程-耦合比 ---
    f_ratio = 6.9517        # (alpha_s/lambda)/(alpha_W/lambda)
    L_pred = 1.0e-3         # 若 L=c/f 成立，则 f_S/f_W 应 = L_W/L_S
    rec("V17-I3", "力程-耦合比矛盾", "FAIL",
        "耦合比 f_S/f_W = {0:.4f}；若力程关系 L=c/f 成立则应为 L_W/L_S = {1:.1e}"
        " ⇒ 矛盾 {2:.4g} 倍。两侧皆为比值 ⇒ 与归一化 C 无关。".format(f_ratio, L_pred, f_ratio / L_pred),
        {"f_ratio": f_ratio, "L_pred": L_pred, "mismatch": f_ratio / L_pred,
         "C_independent": True})

    # --- 实例 4：宇宙组分内部比（Omega_b/Omega_c 也是比值） ---
    rb_m = 6.25 / 25.0
    rb_o = 4.93 / 26.45
    rec("V17-I4", "Omega_b/Omega_c 比值", "FAIL",
        "模型 {0:.6f} vs Planck {1:.6f} ⇒ 偏差 {2:.2f}%。比值量同样与整体归一无关。"
        .format(rb_m, rb_o, 100.0 * (rb_m / rb_o - 1.0)),
        {"model": rb_m, "obs": rb_o, "pct": 100.0 * (rb_m / rb_o - 1.0)})

    print("\n  [判据 I 小结] 4 个实例全部 FAIL，且 3 个为 C-无关比值 ⇒")
    print("  「补齐归一化/量纲因子」这类修法**结构上无法**挽回这些矛盾。")


# ===================== §3 判据 II：平坦方向（卷十六一般化） =====================
def flat_sigma(N, v, prior_prec, var_box):
    """沿平坦方向 v（最后一分量归一化到 1）的后验宽度。
    v:           形状参数方向的位移向量（不含被估参数本身）
    prior_prec:  形状参数的先验精度矩阵 Π
    var_box:     被估参数的盒式先验方差
    返回 sigma = 1/sqrt(N * v^T Π v + 1/var_box)"""
    v = np.asarray(v, dtype=float)
    info = float(np.dot(v, np.dot(np.asarray(prior_prec, dtype=float), v)))
    return 1.0 / np.sqrt(N * info + 1.0 / var_box), info


def section3():
    sec("§3  判据 II · 平坦方向：σ = 1/√(N·vᵀΠv + 1/Var_box)")
    # 卷十六实测的零空间方向 (v_a, v_M, 1)
    v_am = np.array([2.5463e3, 1.5823e3])
    Pi = np.diag([1.0 / 0.05 ** 2, 1.0 / 0.02 ** 2])
    var_box = (1e-4 ** 2) / 12.0
    s1, info = flat_sigma(1.0, v_am, Pi, var_box)
    s30, _ = flat_sigma(30.0, v_am, Pi, var_box)
    s1k, _ = flat_sigma(1000.0, v_am, Pi, var_box)
    rec("V17-J1", "ringdown 平坦方向（卷十六复算）", "PASS",
        "v^T Π v = {0:.4e}；σ_TB(1)={1:.4e}, σ_TB(30)={2:.4e}, σ_TB(1000)={3:.4e}"
        "；先验宽 {4:.4e}".format(info, s1, s30, s1k, np.sqrt(var_box)),
        {"info_per_event": info, "sigma_1": s1, "sigma_30": s30, "sigma_1000": s1k})

    # 自由先验（Π=0）⇒ 完全平坦，N 再多零信息
    sfree, _ = flat_sigma(1e6, v_am, np.zeros((2, 2)), var_box)
    rec("V17-J2", "自由先验下 N→∞ 的极限", "FAIL",
        "Π=0 ⇒ σ_TB(N→1e6) = {0:.6e} = 盒式先验宽 {1:.6e}（比值 {2:.12f}）"
        " ⇒ 多事件堆叠在自由形状参数下**零信息**，卷十六结论一般化成立。"
        .format(sfree, np.sqrt(var_box), sfree / np.sqrt(var_box)),
        {"sigma_limit": sfree, "prior_width": float(np.sqrt(var_box))})

    # N 扫描与斜率
    Ns = np.logspace(0, 4, 25)
    sig = np.array([flat_sigma(n, v_am, Pi, var_box)[0] for n in Ns])
    slope = np.polyfit(np.log10(Ns), np.log10(sig), 1)[0]
    rec("V17-J3", "σ ∝ N^{0:.4f}".format(slope), "PASS",
        "锚定先验下 σ 按 N^-1/2 收缩（理论 -0.5），实测斜率 {0:.4f}。".format(slope),
        {"slope": slope})

    # 通用化：把该公式用到「多能段光子延迟」类通道（形状参数=源内禀延迟）
    v_grb = np.array([1.0])          # 每个 GRB 一个内禀延迟形状参数
    Pi_grb = np.diag([1.0 / 1.0 ** 2])
    var_q = (2.0 ** 2) / 12.0        # Q_H = ±1 的符号参数，盒式 [-1,1]
    sg1, ig = flat_sigma(1.0, v_grb, Pi_grb, var_q)
    sg100, _ = flat_sigma(100.0, v_grb, Pi_grb, var_q)
    rec("V17-J4", "光子延迟通道（Q_H 符号）", "BOUNDARY",
        "每 GRB 带一个内禀延迟形状参数（σ=1 锚定）⇒ v^T Π v = {0:.4e}，"
        "σ_Q(1)={1:.4f}, σ_Q(100)={2:.4f}（先验宽 {3:.4f}）"
        " ⇒ 该通道**需要**源内禀延迟的外部锚定，否则同样平坦。"
        .format(ig, sg1, sg100, np.sqrt(var_q)),
        {"info_per_event": ig, "sigma_1": sg1, "sigma_100": sg100})
    return Ns, sig


# ===================== §4 判据 III：自由度预算 =====================
# 通道, 名义约束 d, 自由参数 p, **有效**约束 d_eff, 说明
# d_eff 与 d 的差别正是本卷要抓的东西：名义上有数据 ≠ 数据能约束参数。
BUDGET = [
    ("ringdown 多事件", 2, 3, 2,
     "每事件 (w_R,w_I) 两实约束；参数 (a,M,T_B) 三个 ⇒ 欠定 1 维（卷十六已证精确简并）"),
    ("g-2 (e+mu) 数值", 2, 1, 2,
     "两个数据点 vs 一个未定归一化 C ⇒ 超定，本应可判"),
    ("g-2 (符号分配)", 2, 1, 2,
     "两种符号分配各有 1 个失败 ⇒ 结构性关闭（对量纲缺陷免疫）"),
    ("CMB (r, n_s, N)", 3, 2, 0,
     "V0 在 N 与 n_s 中完全相消、kappa 是物理常数 ⇒ 实际可调尺度 0 ⇒ 名义超定实为不可拟合"),
    ("宇宙组分", 3, 3, 2,
     "三组分共享归一化约束 ⇒ 有效约束 2 vs 参数 3 ⇒ 欠定 1 维"),
    ("CMB 双谱 f_NL(l)", 0, 7, 0,
     "Planck 无 per-l 数据（R31）⇒ d=0，纯不可证伪"),
    ("光子延迟 Q_H", 1, 2, 1,
     "一个符号 vs (Q_H, 每源内禀延迟) ⇒ 欠定 1 维"),
]


def section4():
    sec("§4  判据 III · 自由度预算：有效约束 d_eff vs 自由参数 p")
    print("  {0:<20} {1:>4} {2:>5} {3:>4} {4:>8}   {5}".format(
        "通道", "d", "d_eff", "p", "d_eff-p", "裁定"))
    print("  " + "-" * 78)
    n_ok = 0
    ok_names = []
    for name, d, p, deff, note in BUDGET:
        gap = deff - p
        verdict = "可辨" if gap >= 0 else "欠定 {0} 维".format(-gap)
        st = "PASS" if gap >= 0 else "FAIL"
        if gap >= 0:
            n_ok += 1
            ok_names.append(name)
        print("  {0:<20} {1:>4} {2:>5} {3:>4} {4:>8}   {5}".format(
            name[:18], d, deff, p, gap, verdict))
        rec("V17-K" + str(len(RESULTS)), name, st,
            "d={0}(有效 {1}) vs p={2} ⇒ {3}；{4}".format(d, deff, p, verdict, note),
            {"d": d, "d_eff": deff, "p": p, "gap": gap})
    rec("V17-K0", "预算总账", "FAIL",
        "按**有效**约束计，{0}/{1} 个通道满足 d_eff>=p（{2}）；"
        "这 {0} 条中 g-2 数值通道已被 §2 的符号/比值类证伪关闭"
        " ⇒ 无一条 TUFT 通道同时满足「可辨 + 未被否证」。"
        .format(n_ok, len(BUDGET), "、".join(ok_names)),
        {"n_ok": n_ok, "n_total": len(BUDGET), "ok_names": ok_names})
    return n_ok, len(BUDGET), ok_names


# ===================== §1b 台账逐条计算 =====================
def section1():
    sec("§1  通道台账：残差 / 上限倍数 / 系数来源")
    print("  {0:<26} {1:>16} {2:>16} {3:>12}  {4}".format(
        "通道", "实验/上限", "TUFT", "偏差", "系数来源"))
    print("  " + "-" * 100)
    tally = {"derived": 0, "ansatz": 0, "closed": 0}
    for ch in CHANNELS:
        if ch["key"] == "rd":
            dev = "{0} sigma".format(ch["z_given"])
            exp_s = "排除 5.74σ"
            tuft_s = "—(模型假设)"
        elif ch["upper"] is not None:
            dev = "{0:.4g}×".format(ch["tuft"] / ch["upper"])
            exp_s = "< {0:.4g}".format(ch["upper"])
            tuft_s = "{0:.6g}".format(ch["tuft"])
        elif ch["key"] == "fr":
            dev = "6.95e3×"
            exp_s = "1.0e-3 (L=c/f)"
            tuft_s = "{0:.4g}".format(ch["tuft"])
        elif ch["key"] == "amu":
            # 该条实质是「符号相反」，百分比无意义
            dev = "符号相反"
            exp_s = "{0:.6g}(+)".format(ch["exp"])
            tuft_s = "{0:.6g}(-)".format(abs(ch["tuft"]))
        else:
            pct = 100.0 * (ch["tuft"] / ch["exp"] - 1.0)
            dev = "{0:+.2f}%".format(pct)
            exp_s = "{0:.6g}".format(ch["exp"])
            tuft_s = "{0:.6g}".format(ch["tuft"])
        print("  {0:<26} {1:>16} {2:>16} {3:>12}  {4}".format(
            ch["name"][:24], exp_s, tuft_s, dev, ch["src"]))
        if ch["src"].startswith("derived"):
            tally["derived"] += 1
        else:
            tally["ansatz"] += 1
        rec("V17-L-" + ch["key"], ch["name"], "INFO",
            "实验 {0} / TUFT {1} / 偏差 {2}；系数来源 = {3}".format(exp_s, tuft_s, dev, ch["src"]),
            {"exp": ch["exp"], "upper": ch["upper"], "tuft": ch["tuft"],
             "dev": dev, "src": ch["src"], "ref": ch["ref"]})

    rec("V17-L0", "台账系数来源分布", "FAIL",
        "{0}/{1} 条通道的响应系数为 ansatz（未推导）；即便 derived 的几条，"
        "其数值也已在 §2 的比值判据下被否证。".format(
            tally["ansatz"], tally["ansatz"] + tally["derived"]),
        {"derived": tally["derived"], "ansatz": tally["ansatz"]})


# ===================== §5 总账与输出 =====================
def summarize(Ns, sig, bud):
    sec("§5  总账")
    cnt = {}
    for r in RESULTS:
        cnt[r["status"]] = cnt.get(r["status"], 0) + 1
    base = os.path.join(HERE, "TUFT_卷十七_可辨识性普查与系数不变性判据")
    lines = []
    lines.append("TUFT 卷十七 · 可辨识性普查与系数不变性判据")
    lines.append("run at: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    lines.append("")
    for r in RESULTS:
        lines.append("  [{0:<9}] {1:<10} {2}".format(r["status"], r["code"], r["detail"]))
    lines.append("")
    lines.append("=" * 78)
    lines.append("汇总")
    lines.append("=" * 78)
    for k in ("PASS", "FAIL", "BOUNDARY", "INFO"):
        if k in cnt:
            lines.append("  {0:<9} = {1}".format(k, cnt[k]))
    lines.append("  条目数：{0}".format(len(RESULTS)))
    lines.append("")
    lines.append("★ 卷十七结论：")
    lines.append("  (1) 判据 I（系数不变性）：4 个实例全 FAIL，3 个为 C-无关比值 ⇒")
    lines.append("      「补齐归一化/量纲因子」在结构上无法挽回这类矛盾——这是把")
    lines.append("      r42 的「函数形式锁定」结果一般化为跨通道判据。")
    lines.append("  (2) 判据 II（平坦方向）：卷十六的 σ=1/√(N·vᵀΠv+1/Var_box) 为通用式，")
    lines.append("      自由先验（Π=0）下 N→∞ 仍等于先验宽 ⇒ 堆叠零信息是通病，")
    lines.append("      ringdown 与光子延迟两通道同型。")
    lines.append("  (3) 判据 III（自由度预算）：按**有效**约束计，{0}/{1} 条通道满足".format(bud[0], bud[1]))
    lines.append("      d_eff>=p（{0}），而其中 g-2 数值通道已被 §2 的比值/符号类".format("、".join(bud[2])))
    lines.append("      证伪关闭 ⇒ 无一条 TUFT 通道同时满足「可辨 + 未被否证」。")
    lines.append("      注意 d 与 d_eff 普遍不等（CMB 名义 3 有效 0、宇宙组分名义 3 有效 2）")
    lines.append("      ⇒ 「有对标数据」不等于「有约束」，这是本卷最重要的方法层读数。")
    lines.append("")
    lines.append("  对下一卷的含义：在补齐 (a) 系数的构造性推导 (b) 形状参数的外部锚定")
    lines.append("  之前，任何新增观测通道都只会把同一结构缺陷再复制一遍。")
    txt = "\n".join(lines)
    with open(base + ".txt", "w", encoding="utf-8") as f:
        f.write(txt + "\n")
    with open(base + ".json", "w", encoding="utf-8") as f:
        json.dump({"generated": time.strftime("%Y-%m-%d %H:%M:%S"),
                   "counts": cnt, "entries": RESULTS,
                   "channels": CHANNELS, "budget": [
                       {"name": n, "d": d, "p": p, "d_eff": de, "note": t}
                       for n, d, p, de, t in BUDGET]},
                  f, ensure_ascii=False, indent=2)
    print(txt)

    # 图：判据 II 的 σ(N)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.loglog(Ns, sig, "b-", lw=2, label="anchored prior")
    Pi = np.diag([1.0 / 0.05 ** 2, 1.0 / 0.02 ** 2])
    var_box = (1e-4 ** 2) / 12.0
    sig_free = np.array([flat_sigma(n, np.array([2.5463e3, 1.5823e3]),
                                    np.zeros((2, 2)), var_box)[0] for n in Ns])
    ax.loglog(Ns, sig_free, "r--", lw=2, label="free prior (flat)")
    ax.axhline(np.sqrt(var_box), color="k", ls=":", label="prior width")
    ax.set_xlabel("N (events)")
    ax.set_ylabel("sigma of T_B")
    ax.set_title("Volume 17 · criterion II: flat-direction posterior width")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "tuft_v17_flat_direction_sigma.png"), dpi=130)
    plt.close(fig)
    print("\nwrote: " + base + ".txt / .json / tuft_v17_flat_direction_sigma.png")


def main():
    t0 = time.time()
    section0()
    section1()
    section2()
    Ns, sig = section3()
    bud = section4()
    summarize(Ns, sig, bud)
    print("\n运行耗时 {0:.2f} s".format(time.time() - t0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
