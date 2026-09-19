# -*- coding: utf-8 -*-
"""
TUFT 后牛顿效应 / 可证伪预言阈值 / 尺度冲突 精算脚本（H9-H12）

红线（ROOT）：
  1. 只原样记录实跑所得判定，不篡改、不粉饰；
  2. 数学自洽 != 物理实证，任何"形式同构"不得记为"复现物理"；
  3. 无法闭合的一律标 OPEN，不得伪闭合。

运行：
  python uft/01-核心公理/TUFT_后牛顿与预言阈值精算.py

产物：
  uft/01-核心公理/TUFT_后牛顿与预言阈值_校验结果.json
"""

import sys
import json
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import mpmath as mp
import sympy as sp

mp.mp.dps = 50

# ---------------------------------------------------------------- 常数（SI, CODATA 2018）
G = mp.mpf("6.67430e-11")
c = mp.mpf("299792458")
hbar = mp.mpf("1.054571817e-34")
m_e = mp.mpf("9.1093837015e-31")
m_p = mp.mpf("1.67262192369e-27")
eV = mp.mpf("1.602176634e-19")
hbar_c_eVm = hbar * c / eV          # 1.97327e-7 eV*m

M_EARTH = mp.mpf("5.9722e24")
R_EARTH = mp.mpf("6.371e6")
M_SUN = mp.mpf("1.98892e30")
R_SUN = mp.mpf("6.957e8")
M_WD = mp.mpf("2.03e30")            # 白矮星（Sirius B 量级）
R_WD = mp.mpf("5.8e6")
M_NS = mp.mpf("2.78e30")            # 中子星 1.4 M_sun
R_NS = mp.mpf("1.2e4")
M_MERCURY_A = mp.mpf("5.7909e10")   # 水星半长轴
E_MERCURY = mp.mpf("0.20563")
T_MERCURY_DAY = mp.mpf("87.969")

ARCSEC_PER_RAD = mp.mpf("206264.806")

RESULTS = []


def record(rid, title, verdict, severity, claim, numbers, note):
    RESULTS.append({
        "id": rid,
        "title": title,
        "verdict": verdict,
        "severity": severity,
        "claim": claim,
        "numbers": numbers,
        "note": note,
    })
    print("[" + verdict + "] " + rid + " " + title)
    for k in numbers:
        print("        " + str(k) + " = " + str(numbers[k]))
    print("        note: " + note)
    print("")


# ================================================================= H9-1
# 定理7 静态解 beta1 = exp(2GM/(c^2 r)) 与 g = (c^2/2) grad ln beta1
# 判定：引力加速度是否【精确】等于牛顿（即零后牛顿修正）
def h9_1_static_solution_equals_newton():
    r, Gm, cc = sp.symbols("r GM c", positive=True)
    beta1 = sp.exp(2 * Gm / (cc ** 2 * r))
    g_tuft = sp.simplify(cc ** 2 / 2 * sp.diff(sp.log(beta1), r))
    g_newton = -Gm / r ** 2
    resid = sp.simplify(g_tuft - g_newton)

    # 数值抽样（地球参数，若干 r）
    samples = {}
    for ratio in [1, 2, 10, 100]:
        rr = R_EARTH * mp.mpf(ratio)
        gg = mp.mpf(mp.mpf(2) * 0)  # placeholder
        gv = mp.mpf(
            repr(float(sp.N(g_tuft.subs({r: float(rr), Gm: float(G * M_EARTH), cc: float(c)}))))
        )
        nv = -G * M_EARTH / rr ** 2
        samples["r/R_E=" + str(ratio)] = mp.fabs((gv - nv) / nv)

    record(
        "H9-1",
        "静态解引力加速度 == 牛顿（零后牛顿修正）",
        "FAIL",
        "P0",
        "beta1=exp(2GM/(c^2 r)) 与 g=(c^2/2)grad ln beta1 联立，对一切 r 恒等还原牛顿 -GM/r^2，"
        "不含任何 1PN 修正项",
        {
            "符号残差 g_TUFT - g_Newton": str(resid),
            "数值相对偏差 r=R_E..100R_E": str([mp.nstr(v, 3) for v in samples.values()]),
        },
        "这不是'弱场兼容牛顿'，而是'在所有 r 上精确等于牛顿'。因此 TUFT 现行静态解对任何"
        "后牛顿可观测量（近日点进动、光线偏折、Shapiro 延迟）的预言为零，与实验直接冲突，"
        "除非另行补充后牛顿机制并重新求解。",
    )


# ================================================================= H9-2
# 水星近日点进动：GR vs TUFT(=0) vs 观测
def h9_2_perihelion():
    gm = G * M_SUN
    per_orbit_rad = 6 * mp.pi * gm / (c ** 2 * M_MERCURY_A * (1 - E_MERCURY ** 2))
    orbits_per_century = mp.mpf("100") * mp.mpf("365.25") / T_MERCURY_DAY
    gr_arcsec = per_orbit_rad * orbits_per_century * ARCSEC_PER_RAD

    obs = mp.mpf("43.11")       # 观测残余（扣除已知行星摄动）
    obs_sigma = mp.mpf("0.45")
    tuft = mp.mpf("0")          # 纯中心牛顿势（TUFT 静态解）=> 零进动

    sigma_gr = mp.fabs(gr_arcsec - obs) / obs_sigma
    sigma_tuft = mp.fabs(tuft - obs) / obs_sigma

    record(
        "H9-2",
        "水星近日点进动：TUFT 预言 0 vs 观测 43.11''/世纪",
        "FAIL",
        "P0",
        "TUFT 静态球对称解只给牛顿中心势，广义相对论近日点进动项在 TUFT 中无对应项",
        {
            "GR 预言 (arcsec/century)": mp.nstr(gr_arcsec, 6),
            "TUFT 预言 (arcsec/century)": mp.nstr(tuft, 6),
            "观测 (arcsec/century)": str(obs) + " +/- " + str(obs_sigma),
            "GR 偏差 (sigma)": mp.nstr(sigma_gr, 4),
            "TUFT 偏差 (sigma)": mp.nstr(sigma_tuft, 4),
        },
        "TUFT 与观测相差约 96 个标准差。仅当 TUFT 另行补出 1PN 项（现未给出）才可能挽救；"
        "补出后必须重新检查是否仍等于定理7 的静态解。",
    )


# ================================================================= H9-3
# 太阳边缘光线偏折：GR 全值 / 牛顿（含等效质量）半值 / 严格 m=0 零值 vs VLBI 观测
def h9_3_light_deflection():
    gm = G * M_SUN
    gr_rad = 4 * gm / (c ** 2 * R_SUN)
    half_rad = 2 * gm / (c ** 2 * R_SUN)      # 若光子按 m=hbar*omega/c^2 受力（牛顿式）
    zero_rad = mp.mpf("0")                    # 若严格 m=0（定理6 F=mc^2(...) 直接给 0）

    gr_arcsec = gr_rad * ARCSEC_PER_RAD
    half_arcsec = half_rad * ARCSEC_PER_RAD

    # 观测：VLBI 给出 PPN gamma - 1 = (-0.8 +/- 1.2)e-4，偏折角正比于 (1+gamma)/2
    gamma_obs = mp.mpf("1") + mp.mpf("-0.8e-4")
    gamma_sigma = mp.mpf("1.2e-4")
    obs_arcsec = gr_arcsec * (1 + gamma_obs) / 2
    obs_sigma_arcsec = gr_arcsec * gamma_sigma / 2

    sigma_half = mp.fabs(half_arcsec - obs_arcsec) / obs_sigma_arcsec
    sigma_zero = mp.fabs(zero_rad * ARCSEC_PER_RAD - obs_arcsec) / obs_sigma_arcsec

    record(
        "H9-3",
        "太阳边缘光线偏折：TUFT 给 0 或半值，观测为全值",
        "FAIL",
        "P0",
        "TUFT 未给出光子测地线/零质量极限的处理；两种可能读法均与 VLBI 观测冲突",
        {
            "GR 全值 (arcsec)": mp.nstr(gr_arcsec, 6),
            "TUFT 半值 (arcsec，若光子带等效质量)": mp.nstr(half_arcsec, 6),
            "TUFT 零值 (arcsec，若严格 m=0)": "0",
            "VLBI 观测 (arcsec)": mp.nstr(obs_arcsec, 8),
            "观测 sigma (arcsec)": mp.nstr(obs_sigma_arcsec, 3),
            "半值偏差 (sigma)": mp.nstr(sigma_half, 4),
            "零值偏差 (sigma)": mp.nstr(sigma_zero, 4),
        },
        "两种读法分别偏离观测 8.33e3 sigma（半值）与 1.67e4 sigma（零值）。TUFT 没有任何可调"
        "参数能在不引入新机制的前提下给出全值偏折。",
    )


# ================================================================= H9-4
# PPN 可映射性（结构性缺口）
def h9_4_ppn_mapping():
    record(
        "H9-4",
        "PPN 参数映射缺失（Shapiro / Cassini / LLR / 引力波相位）",
        "OPEN",
        "P0",
        "TUFT 未给出度规 g_mu_nu，因而 gamma/beta 等 PPN 参数不可计算；Cassini 约束 "
        "gamma-1=(2.1+/-2.3)e-5、LLR 约束 beta-1=(1.2+/-1.1)e-4、LIGO 需要 1PN-3.5PN 相位系数，"
        "TUFT 目前一项都给不出",
        {
            "Cassini gamma-1 上限": "2.3e-5",
            "LLR beta-1 上限": "1.1e-4",
            "LIGO 所需 PN 阶": "1PN .. 3.5PN",
            "TUFT 可给出的 PN 系数个数": "0",
        },
        "这不是'未证明等价 GR'，而是'在 PPN 层面 TUFT 目前没有可计算内容'。"
        "任何 PPN 级别比较都必须先补出度规与 1PN 展开，属于 C 级结构性缺口。",
    )


# ================================================================= H10
# beta1 定义式与指数解联立：反解真空基准 K0 跨天体的不自洽
def h10_k0_reverse_solve():
    bodies = [
        ("地球表面", M_EARTH, R_EARTH),
        ("太阳表面", M_SUN, R_SUN),
        ("白矮星表面", M_WD, R_WD),
        ("中子星表面", M_NS, R_NS),
    ]
    rows = {}
    strict_vals = []
    delta_vals = []
    for name, mm, rr in bodies:
        gm = G * mm
        kappa = gm / (c ** 2 * rr ** 2)          # 由 g = c^2 kappa（修订后定理5）反解的外场曲率
        x = 2 * gm / (c ** 2 * rr)
        beta1 = mp.e ** x
        k0_strict = kappa ** 2 / beta1           # 严格口径：beta1 = kappa^2 / K0
        k0_delta = kappa ** 2 / (beta1 - 1)      # 增量口径：beta1 - 1 = (kappa^2 - K0)/K0
        rows[name] = {
            "kappa_field (1/m)": mp.nstr(kappa, 5),
            "2GM/(c^2 r)": mp.nstr(x, 5),
            "beta1": mp.nstr(beta1, 8),
            "K0 严格口径 (1/m^2)": mp.nstr(k0_strict, 5),
            "特征长度 1/sqrt(K0) 严格 (m)": mp.nstr(1 / mp.sqrt(k0_strict), 5),
            "K0 增量口径 (1/m^2)": mp.nstr(k0_delta, 5),
            "特征长度 1/sqrt(K0) 增量 (m)": mp.nstr(1 / mp.sqrt(k0_delta), 5),
        }
        strict_vals.append(k0_strict)
        delta_vals.append(k0_delta)

    spread_strict = max(strict_vals) / min(strict_vals)
    spread_delta = max(delta_vals) / min(delta_vals)

    # 与两个"自然"候选基准对比
    k0_planck = 1 / (hbar * G / c ** 3)          # 1/l_P^2
    h0 = mp.mpf("2.2e-18")
    k0_cosmo = (h0 / c) ** 2

    record(
        "H10",
        "beta1 定义式与指数解联立：反解真空基准 K0 跨天体漂移",
        "FAIL",
        "P0",
        "由 beta1 = kappa^2/K0（定义）与 beta1 = exp(2GM/(c^2 r))（解）联立反解 K0；"
        "K0 按定义必须是常数，实跑表明它随天体漂移十几个数量级",
        {
            "逐天体反解": str(rows),
            "K0 极差（严格口径）": mp.nstr(spread_strict, 5) + " 倍",
            "K0 极差（增量口径）": mp.nstr(spread_delta, 5) + " 倍",
            "普朗克基准 K0=1/l_P^2": mp.nstr(k0_planck, 5) + " 1/m^2",
            "宇宙学基准 K0=(H0/c)^2": mp.nstr(k0_cosmo, 5) + " 1/m^2",
        },
        "原 H3 只证明同一天体不同 r 处 K0 差 16 倍（幂律 r^-4 暴露）；本条补强：跨天体后 K0 "
        "漂移达 1.22e22 倍（严格口径）/ 2.28e14 倍（增量口径）；反解出的真空特征长度依次为"
        "9.15e15 m（地球）、3.28e14 m（太阳）、2.23e10 m（白矮星）、8.28e4 m（中子星），"
        "彼此相差 11 个数量级，且既不等于普朗克基准（相差 37-101 个数量级）也不等于宇宙学"
        "基准。'真空背景曲率'在此框架内无自洽取值。",
    )


# ================================================================= H11
# 稳态拓扑孤子的几何尺度被质量锁死：sqrt(R^2+b^2) = hbar/(m c)（康普顿尺度）
# vs 粒子点状性实验上限
def h11_soliton_scale():
    R, b, u = sp.symbols("R b u", positive=True)
    kap = R / (R ** 2 + b ** 2)
    tau = b / (R ** 2 + b ** 2)
    Ksq = sp.simplify(kap ** 2 + tau ** 2)
    invK = sp.simplify(sp.sqrt(1 / Ksq))
    identical = sp.simplify(invK - sp.sqrt(R ** 2 + b ** 2))

    def scale(m_kg):
        return hbar / (m_kg * c)

    # 实验点状性（compositeness）上限，保守取值
    e_limit = mp.mpf("1e-19")      # 电子：保守（LEP/LHC 对应可达 2e-20 m）
    p_limit = mp.mpf("1e-18")      # 质子：深度非弹散射部分子尺度
    nu_limit = mp.mpf("1e-19")

    s_e = scale(m_e)
    s_p = scale(m_p)
    m_nu = mp.mpf("0.1") * eV / c ** 2      # 0.1 eV/c^2
    s_nu = scale(m_nu)

    record(
        "H11",
        "稳态孤子几何尺度 = 约化康普顿波长，与粒子点状性实验冲突",
        "FAIL",
        "P0",
        "由定理1（稳态圆柱螺旋解：kappa=R/(R^2+b^2), tau=b/(R^2+b^2)）与定理3"
        "（m=(hbar/c)sqrt(kappa^2+tau^2)）联立，严格推出 sqrt(R^2+b^2)=hbar/(mc)；"
        "该尺度不可通过调节螺旋角 theta 逃避",
        {
            "符号恒等式 1/K - sqrt(R^2+b^2)": str(identical),
            "电子 sqrt(R^2+b^2) (m)": mp.nstr(s_e, 5),
            "电子点状性上限 (m)": mp.nstr(e_limit, 3),
            "电子超出倍数": mp.nstr(s_e / e_limit, 4),
            "质子 sqrt(R^2+b^2) (m)": mp.nstr(s_p, 5),
            "质子部分子尺度上限 (m)": mp.nstr(p_limit, 3),
            "质子超出倍数": mp.nstr(s_p / p_limit, 4),
            "中微子(0.1eV) sqrt(R^2+b^2) (m)": mp.nstr(s_nu, 5),
            "中微子超出倍数": mp.nstr(s_nu / nu_limit, 4),
        },
        "关键点：螺旋半径 R=kappa/K^2 与螺距参数 b=tau/K^2 满足 R^2+b^2=(hbar/mc)^2，"
        "调小 R 必然放大 b（趋向直螺旋、不再闭合），反之亦然；两者无法同时压小。"
        "再叠加 Fenchel 定理（闭合曲线总曲率 >= 2pi，kappa<=K）得弧长下界 L>=2*pi*hbar/(mc)，"
        "电子即 >= 2.43e-12 m。因此'电子是闭合拓扑孤子'与'电子在 1e-19 m 下仍点状'不可兼得。"
        "唯一逃生门是放弃定理1的稳态解、或放弃闭合孤子（定理2/9），代价是拆除自旋-统计分类。",
    )


# ================================================================= H12
# 同一个符号 kappa 的三重身份：孤子自曲率 / 外场曲率 / 真空背景曲率
def h12_kappa_triple_meaning():
    k_soliton_e = m_e * c / hbar             # 定理3：电子自曲率
    k_field_earth = G * M_EARTH / (c ** 2 * R_EARTH ** 2)   # 定理5/7：地球表面外场曲率
    l_p = mp.sqrt(hbar * G / c ** 3)
    k_vac_planck = 1 / l_p                   # 若 K0 取普朗克基准
    k_vac_reverse = mp.sqrt(k_field_earth ** 2 / (mp.e ** (2 * G * M_EARTH / (c ** 2 * R_EARTH))))

    # 若定理6 的力分解使用孤子自曲率，其"电磁项"量级
    f_self = m_e * c ** 2 * k_soliton_e      # |F| = m c^2 kappa
    f_grav = m_e * mp.mpf("9.81")

    record(
        "H12",
        "kappa 语义三义性：同一符号承载相差 50 个数量级的三个量",
        "FAIL",
        "P0",
        "理论全程使用同一个 kappa：定理3 取孤子自曲率、定理5/7 取外场引力曲率、"
        "定理4 的分母 K0 取真空背景曲率；三者从未区分，量级互不相容",
        {
            "孤子自曲率 kappa_soliton（电子） 1/m": mp.nstr(k_soliton_e, 6),
            "外场曲率 kappa_field（地球表面） 1/m": mp.nstr(k_field_earth, 6),
            "真空背景曲率（普朗克口径） 1/m": mp.nstr(k_vac_planck, 6),
            "真空背景曲率（H10 反解口径） 1/m": mp.nstr(k_vac_reverse, 6),
            "孤子/外场 比值": mp.nstr(k_soliton_e / k_field_earth, 4),
            "孤子/普朗克 比值": mp.nstr(k_soliton_e / k_vac_planck, 4),
            "若定理6 用自曲率：|F|=m c^2 kappa (N)": mp.nstr(f_self, 4),
            "电子重力 m g (N)": mp.nstr(f_grav, 4),
            "二者比值": mp.nstr(f_self / f_grav, 4),
        },
        "若定理6 的力分解取孤子自曲率（此处取 tau=0 的纯曲率极限 kappa=K，若取费米角 "
        "theta=45° 则 kappa=K/sqrt(2)、|F|=0.15 N，量级不变），电子自受力约 0.21 N，"
        "比重力大 2.37e28 倍，物理上荒谬；若改取外场曲率，则定理3 的质量公式与定理6 的力"
        "公式必须使用不同的 kappa，而理论没有给出二者的耦合关系（与 H5 场化提升缺口同源）。",
    )


# ================================================================= 预言清单现状盘点
def predictions_inventory():
    items = [
        ("A1 水星近日点进动", "可算", "FAIL", "H9-2"),
        ("A2 太阳边缘光线偏折", "可算", "FAIL", "H9-3"),
        ("A3 Shapiro 延迟 / Cassini", "不可算（无度规、无 PPN）", "OPEN", "H9-4"),
        ("A4 电子/中微子点状性 vs 孤子尺度", "可算", "FAIL", "H11"),
        ("A5 beta1 幂律 vs 指数（K0 一致性）", "可算", "FAIL", "H10/H3"),
        ("A6 费米子自旋 Lk=1/sqrt(2) 非整数", "可算", "FAIL", "H4"),
        ("A7 汤川势 vs Helmholtz 源方程", "可算", "FAIL", "H6"),
        ("B1 引力波 1PN..3.5PN 相位系数", "未给出", "OPEN", "H9-4"),
        ("B2 等效原理违背 eta（MICROSCOPE 1e-15）", "未给出数值", "OPEN", "—"),
        ("B3 精细结构常数时间漂移（原子钟 1e-17/yr）", "未给出数值", "OPEN", "—"),
        ("B4 黑洞阴影/EHT 光子测地线", "未给出", "OPEN", "—"),
        ("B5 拓扑耦合常数 k、g^2、mu 的第一性数值", "只能实验标定", "OPEN", "—"),
        ("C1 孤子内部频率 omega=mc^2/hbar 直接探测", "需 1e20 Hz 量级探针，现不可行", "OPEN", "H11"),
        ("C2 真空基准 K0 的宇宙学起源 / Lambda 关系", "无方程", "OPEN", "H10"),
        ("C3 弱相互作用拓扑突变的能标与产物", "无动力学", "OPEN", "—"),
    ]
    n_fail = sum(1 for it in items if it[2] == "FAIL")
    n_open = sum(1 for it in items if it[2] == "OPEN")
    text = "\n".join("  " + it[0] + " | " + it[1] + " | " + it[2] + " | " + it[3] for it in items)
    record(
        "P-INV",
        "可证伪预言清单现状盘点（15 项）",
        "INFO",
        "—",
        "A 级=现有数据即可判定；B 级=精度逼近但 TUFT 尚未给出数值；C 级=远期或需新实验",
        {
            "A/B/C 逐项状态": "\n" + text,
            "已可判定且失败": str(n_fail) + " 项",
            "尚无可算数值": str(n_open) + " 项",
            "已算出且通过的独立排他预言": "0 项",
        },
        "结论：TUFT 目前没有任何一条'本理论独有、竞争理论不能解释、且已被实验证实'的定量预言。"
        "A 级 6 项在现行解下已被现有数据证伪或内部不自洽；B/C 级全部缺少可算数值。",
    )


def main():
    print("=" * 78)
    print("TUFT 后牛顿 / 预言阈值 / 尺度冲突 精算（H9-H12 + 预言盘点）")
    print("红线：只记录实跑结果，不粉饰；未闭合一律 OPEN")
    print("=" * 78)
    print("")

    h9_1_static_solution_equals_newton()
    h9_2_perihelion()
    h9_3_light_deflection()
    h9_4_ppn_mapping()
    h10_k0_reverse_solve()
    h11_soliton_scale()
    h12_kappa_triple_meaning()
    predictions_inventory()

    n = {}
    for r in RESULTS:
        n[r["verdict"]] = n.get(r["verdict"], 0) + 1
    print("=" * 78)
    print("汇总: " + str(n))
    print("=" * 78)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "TUFT_后牛顿与预言阈值_校验结果.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"summary": n, "results": RESULTS}, f, ensure_ascii=False, indent=2)
    print("写出: " + out)


if __name__ == "__main__":
    main()
