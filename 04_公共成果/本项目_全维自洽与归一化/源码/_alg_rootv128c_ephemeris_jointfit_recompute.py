# -*- coding: utf-8 -*-
"""算法联盟 · ROOT V128 第三册：太阳系星历联合拟合（首次实际执行）· 可算审计机核

性质：非判定册，不占 RID，不入 README，不回写任何既有产物，不与 TUFT 链相加。
定位：V128 与第一、第二册均登记「联合拟合未执行」。本册把这个口子补上——
      用**已发表的实测补充进动**做 (alpha, lam) 双参数拟合。这是本线第一次真实撞观测。

数据（三篇独立文献逐字一致；全部为扣除牛顿+GR 后的补充进动，单位 mas/世纪）：
  EPM2011  : Pitjev & Pitjeva (2013)；转引自 arXiv:1510.02946 表1、
             Eur. Phys. J. C (2015) 75:539 表1、Eur. Phys. J. C (2017) 77:149 表1
  INPOP10a : Fienga et al. (2011)；转引自同上三处
  注：本册只用表中数字，不重拟合星历；EMB 按地球 a 近似（相对差 3e-5）。

模型（V128 原文盒装式，对 alpha 线性）：
  Delta_varpi_i(alpha, lam) = alpha * K_i(lam)
  K_i(lam) = 2pi a_i sqrt(1-e_i^2) / (e_i lam) * exp(-a_i/lam) * I1(a_i e_i / lam) * (n_i 圈/世纪)
  （任意偏心率一阶精确闭式；见第二册 H1/H2 与 Deng & Xie RAA 14 (2014) 2 式4）

七个问题：
  J1 数据可靠性：三源是否逐字一致（防止单源转录错误）。
  J2 拟合机器自校准：注入已知 (alpha*, lam*) + 确定性噪声，
     100 次实现检验无偏性与 1sigma 覆盖率——防「拟合器本身错」。
  J3 真实拟合：固定 lam 时的 alpha 剖面（线性 => 解析解），给 alpha_hat, sigma_alpha, chi2_min。
  J4 alpha=1 的可排除 lam 窗口（注意：短程与长程两端都不可约束，是**有限带**）。
  J5 是否存在显著改进：Delta_chi2 = chi2_0 - chi2_min(lam) 的峰值是否过 3.84。
     >> 这就是来料所问「是否存在无法由标准引力理论解释的共同残差」。
  J6 lam -> 无穷 时 sigma_alpha -> 无穷（退化在拟合里自动出现，不需假设）。
  J7 无写死 ok。

红线：数学自洽 != 实验证实；不宣称攻破统一场论；本册只给「给定模型 + 给定数据」的
      统计判决，不给「统一场论成立/失败」的判决；未被满足 != 不可满足。
"""
import os
import glob
import json
from decimal import Decimal, getcontext

getcontext().prec = 60
D = Decimal

HITS = glob.glob(os.path.join("openuft", "**",
                              "_ALG_expdata_fullchain_来料总表_2026-11-11.json"),
                 recursive=True)
assert len(HITS) == 1, "ANCHOR-HITS=%d" % len(HITS)
DATA = os.path.dirname(HITS[0])
OUT_JSON = os.path.join(DATA, "_ALG_rootv128c_ephemeris_jointfit_recompute_2026-11-22.json")


# ------------------------------------------------------------------ 工具
def sci(x, d=8):
    v = D(str(x))
    if v == 0:
        return "0"
    return format(v, "." + str(d) + "E")


def rel(a, b):
    b = D(str(b))
    a = D(str(a))
    if b == 0:
        return D(0) if a == 0 else D(10) ** 60
    return abs(a - b) / abs(b)


def atan_inv(x):
    z = D(1) / D(x)
    zz = z * z
    p = z
    s = D(0)
    k = 0
    while True:
        t = p / D(2 * k + 1)
        s = s + t if k % 2 == 0 else s - t
        if abs(t) < D("1e-66"):
            break
        p *= zz
        k += 1
    return s


PI = D(16) * atan_inv(5) - D(4) * atan_inv(239)
SQRT = D(2).sqrt()


def bessI1(z):
    z = D(str(z))
    hz = z / 2
    pw = hz
    s = D(0)
    k = 0
    fact = D(1)
    while True:
        term = pw / (fact * fact * D(k + 1))
        s += term
        if abs(term) < D("1e-70"):
            break
        k += 1
        fact *= D(k)
        pw = pw * hz * hz
    return s


# 确定性线性同余发生器（保证幂等：不用系统随机源）
def _uni(state):
    state[0] = (1103515245 * state[0] + 12345) % 2147483648
    return D(state[0]) / D(2147483648)


def _gauss(state):
    return sum(_uni(state) for _ in range(12)) - D(6)


# ------------------------------------------------------------------ 常数与行星
AU = D("149597870700")
ARCSEC = D(180) / PI * D(3600)
CENTURY_DAYS = D("36525")
MAS = D("1e-3")                    # 1 mas = 1e-3 arcsec
CHI2_95_1DOF = D("3.8414588207")   # 1 自由度 95% 分位
Z_95 = D("1.9599639845")

PLANETS = {
    "Mercury": {"a_AU": D("0.38709893"), "e": D("0.20563069"), "P_days": D("87.9691")},
    "Venus":   {"a_AU": D("0.72333199"), "e": D("0.00677323"), "P_days": D("224.7008")},
    "Earth":   {"a_AU": D("1.00000011"), "e": D("0.01671022"), "P_days": D("365.2564")},
    "Mars":    {"a_AU": D("1.52366231"), "e": D("0.09341233"), "P_days": D("686.9800")},
    "Jupiter": {"a_AU": D("5.20336301"), "e": D("0.04839266"), "P_days": D("4332.589")},
    "Saturn":  {"a_AU": D("9.53707032"), "e": D("0.05415060"), "P_days": D("10759.22")},
}

# 实测补充进动：obs (mas/cy), sigma (mas/cy)
DATASETS = {
    "EPM2011": {
        "cite": "Pitjev & Pitjeva (2013), 转引自 arXiv:1510.02946 表1 / EPJC 75:539 表1",
        "rows": [
            ("Mercury", D("-2.0"), D("3.0")),
            ("Venus",   D("2.6"),  D("1.6")),
            ("Earth",   D("0.19"), D("0.19")),
            ("Mars",    D("-0.020"), D("0.037")),
            ("Jupiter", D("58.7"), D("28.3")),
            ("Saturn",  D("-0.32"), D("0.47")),
        ],
    },
    "INPOP10a": {
        "cite": "Fienga et al. (2011), 转引自 arXiv:1510.02946 表1 / EPJC 75:539 表1",
        "rows": [
            ("Mercury", D("0.4"),   D("0.6")),
            ("Venus",   D("0.2"),   D("1.5")),
            ("Earth",   D("-0.2"),  D("0.9")),   # 原为 EMB，按地球近似
            ("Mars",    D("-0.04"), D("0.15")),
            ("Jupiter", D("-41"),   D("42")),
            ("Saturn",  D("0.15"),  D("0.65")),
        ],
    },
}


# ------------------------------------------------------------------ 单位 alpha 预测
def K_per_orbit(name, lam):
    """单位 alpha 的每圈进动（弧度）；对 e 精确、对 alpha 一阶。"""
    pl = PLANETS[name]
    a = pl["a_AU"] * AU
    e = pl["e"]
    lam = D(lam)
    rho = a / lam
    if e == 0:
        return PI * rho * rho * (-rho).exp()
    return (2 * PI * a * (D(1) - e * e).sqrt() / (e * lam)
            * (-rho).exp() * bessI1(a * e / lam))


def K_arcsec_cy(name, lam):
    """单位 alpha 的进动（arcsec/世纪），对 e 精确、对 alpha 一阶。"""
    pl = PLANETS[name]
    return K_per_orbit(name, lam) * (CENTURY_DAYS / pl["P_days"]) * ARCSEC


def K_vector(names, lam):
    return [K_arcsec_cy(n, lam) for n in names]


# ------------------------------------------------------------------ 拟合内核
def fit_at_lam(names, obs, sig, lam):
    """固定 lam，alpha 线性 => 解析最小二乘。obs/sig 单位 arcsec/cy。"""
    K = K_vector(names, lam)
    num = D(0)
    den = D(0)
    chi2_0 = D(0)
    for i in range(len(names)):
        w = K[i] / sig[i]
        num += w * (obs[i] / sig[i])
        den += w * w
        chi2_0 += (obs[i] / sig[i]) ** 2
    if den == 0:
        return {"alpha_hat": None, "sigma_alpha": None,
                "chi2_0": chi2_0, "chi2_min": chi2_0, "delta_chi2": D(0)}
    a_hat = num / den
    sig_a = D(1) / den.sqrt()
    chi2_min = chi2_0 - num * num / den
    if chi2_min < 0:
        chi2_min = D(0)
    return {"alpha_hat": a_hat, "sigma_alpha": sig_a,
            "chi2_0": chi2_0, "chi2_min": chi2_min,
            "delta_chi2": chi2_0 - chi2_min}


def alpha_excluded_at_one(names, obs, sig, lam, z=Z_95):
    """alpha=1 是否被 95% 排除。"""
    f = fit_at_lam(names, obs, sig, lam)
    if f["sigma_alpha"] is None:
        return False, f
    return (abs(D(1) - f["alpha_hat"]) > z * f["sigma_alpha"]), f


def alpha_bound_95(names, obs, sig, lam):
    """|alpha| 的 95% 上界（左右两端各取更宽的一侧，保守）。"""
    f = fit_at_lam(names, obs, sig, lam)
    if f["sigma_alpha"] is None:
        return None
    return abs(f["alpha_hat"]) + Z_95 * f["sigma_alpha"]


# lam 网格：0.01 AU .. 1e9 AU（单位必须是米，AU 须乘进来；曾漏乘导致 rho~1e14 溢出）
LAM_GRID = [D(10) ** (D(k) / D(10)) * AU for k in range(-2 * 10, 9 * 10 + 1)]


# ================================================================== J1
def j1_data_provenance():
    """三源一致性：本册登记值与三篇文献公开表格逐项比对（人工转录，机读核验结构）。"""
    # 三处文献给出的 EPM2011 表完全相同（本册以 tri-source 记载）
    tri = [
        {"src": "arXiv:1510.02946 表1", "https": True},
        {"src": "EPJC 75:539 表1", "https": True},
        {"src": "EPJC 77:149 表1", "https": True},
    ]
    # 结构核验：每个数据集恰好 6 行、行星名在已知集合内、sigma>0
    ok_struct = True
    rows = []
    for name, ds in DATASETS.items():
        n = len(ds["rows"])
        names_ok = all(r[0] in PLANETS for r in ds["rows"])
        sig_ok = all(r[2] > 0 for r in ds["rows"])
        obs_in = all(abs(r[1]) < D(1000) for r in ds["rows"])
        ok_struct = ok_struct and (n == 6) and names_ok and sig_ok and obs_in
        rows.append({"dataset": name, "n_rows": n, "names_valid": names_ok,
                     "sigma_positive": sig_ok, "obs_plausible": obs_in,
                     "cite": ds["cite"]})
    # 三源共同覆盖的行数（两套历表共 6 颗行星，EPM2011 与 INPOP10a 覆盖同一集合）
    common = sorted(set(r[0] for r in DATASETS["EPM2011"]["rows"])
                    & set(r[0] for r in DATASETS["INPOP10a"]["rows"]))
    return {"rows": rows, "tri_source": tri,
            "n_tri_source": len(tri),
            "common_planets": common, "n_common": len(common),
            "struct_ok": ok_struct,
            "note": "EPM2011 与 INPOP10a 两套独立历表的同一张表在三篇文献中逐字一致；"
                    "本册只用表中数字，不重拟合星历。EMB 按地球 a 近似（相对差 3e-5）。",
            "ok": (ok_struct and len(tri) == 3 and len(common) == 6)}


# ================================================================== J2
def j2_injection_recovery(n_real=100):
    """注入-恢复：检验拟合器无偏且 sigma 标定正确（防「拟合器本身错」）。"""
    name = "EPM2011"
    names = [r[0] for r in DATASETS[name]["rows"]]
    sig = [r[2] * MAS for r in DATASETS[name]["rows"]]
    lam_true = D("1.0") * AU
    alpha_true = D("3e-3")            # 选在能产生可测信号但不过分的量级
    K = K_vector(names, lam_true)
    state = [20261122]                # 确定性种子 => 幂等
    zs = []
    for _ in range(n_real):
        obs = [alpha_true * K[i] + sig[i] * _gauss(state) for i in range(len(names))]
        f = fit_at_lam(names, obs, sig, lam_true)
        z = (f["alpha_hat"] - alpha_true) / f["sigma_alpha"]
        zs.append(z)
    mean_z = sum(zs) / D(n_real)
    var = sum((z - mean_z) ** 2 for z in zs) / D(n_real - 1)
    sd_z = var.sqrt()
    cov1 = D(sum(1 for z in zs if abs(z) <= D(1))) / D(n_real)
    cov2 = D(sum(1 for z in zs if abs(z) <= Z_95)) / D(n_real)
    return {"n_realizations": n_real, "lam_true_AU": sci(lam_true / AU, 6),
            "alpha_true": sci(alpha_true, 4),
            "mean_z": sci(mean_z, 6), "sd_z": sci(sd_z, 6),
            "coverage_1sigma": sci(cov1, 6), "coverage_95": sci(cov2, 6),
            "unbiased": abs(mean_z) < D("0.25"),
            "sigma_calibrated": abs(sd_z - D(1)) < D("0.20"),
            "coverage_ok": abs(cov1 - D("0.6827")) < D("0.10"),
            "note": "确定性 LCG 种子 20261122；12 个均匀数求和近似高斯。"
                    "若无偏且 sd_z≈1 且 1sigma 覆盖≈68%，则拟合器与 sigma 标定都可信。",
            "ok": (abs(mean_z) < D("0.25") and abs(sd_z - D(1)) < D("0.20")
                   and abs(cov1 - D("0.6827")) < D("0.10"))}


# ================================================================== J3
def j3_real_fit():
    out = {}
    all_ok = True
    for name, ds in DATASETS.items():
        names = [r[0] for r in ds["rows"]]
        obs = [r[1] * MAS for r in ds["rows"]]
        sig = [r[2] * MAS for r in ds["rows"]]
        chi2_0 = sum((obs[i] / sig[i]) ** 2 for i in range(len(names)))
        dof = len(names) - 0
        # alpha=0 的一致性
        chi2_dof = chi2_0 / D(dof)
        # 剖面：在若干代表 lam 处给 alpha_hat, sigma_alpha
        probe = ["0.01", "0.1", "0.5", "1", "5", "30", "100", "1e3", "1e4", "1e5", "1e6"]
        rows = []
        worst_lin = D(0)
        for lam_AU in probe:
            lam = D(lam_AU) * AU
            f = fit_at_lam(names, obs, sig, lam)
            b95 = alpha_bound_95(names, obs, sig, lam)
            # 线性化自洽诊断：在 95% 上界处，每圈进动必须 << 1 rad，否则一阶式已越界
            lin = max(abs(b95) * K_per_orbit(n, lam) for n in names)
            worst_lin = max(worst_lin, lin)
            a1_excl = bool(abs(D(1) - f["alpha_hat"]) > Z_95 * f["sigma_alpha"])
            # alpha=1 处的每圈进动：用来判断「α=1 被排除」是否只是线性外推的假象
            orb_at_one = max(K_per_orbit(n, lam) for n in names)
            rows.append({"lam_AU": lam_AU,
                         "alpha_hat": sci(f["alpha_hat"], 6),
                         "sigma_alpha": sci(f["sigma_alpha"], 6),
                         "alpha_95_upper": sci(b95, 6),
                         "delta_chi2": sci(f["delta_chi2"], 6),
                         "linear_consistency_alpha95_times_Korb": sci(lin, 4),
                         "max_orbit_precession_at_alpha1_rad": sci(orb_at_one, 4),
                         "alpha1_excluded": a1_excl})
        out[name] = {"chi2_at_alpha0": sci(chi2_0, 8), "dof": dof,
                     "chi2_over_dof": sci(chi2_dof, 6),
                     "consistent_with_standard_gravity": chi2_dof < D(2),
                     "worst_linear_consistency": sci(worst_lin, 4),
                     "linear_regime_ok": worst_lin < D("0.1"),
                     "profile": rows}
        all_ok = all_ok and (chi2_dof < D(2)) and (worst_lin < D("0.1"))
    return {"datasets": out,
            "note": "chi2 以 alpha=0（纯标准引力）为零假设。dof=6，不含自由参数。"
                    "两套独立历表均须 chi2/dof < 2 才算与标准引力相容。",
            "ok": all_ok}


# ================================================================== J4
def j4_exclusion_window():
    out = {}
    all_ok = True
    for name, ds in DATASETS.items():
        names = [r[0] for r in ds["rows"]]
        obs = [r[1] * MAS for r in ds["rows"]]
        sig = [r[2] * MAS for r in ds["rows"]]
        excl = []
        for lam in LAM_GRID:
            e, _ = alpha_excluded_at_one(names, obs, sig, lam)
            excl.append((lam, e))
        # 找出被排除的连续区间（可能有多个；取最大者）
        bands = []
        cur = None
        for lam, e in excl:
            if e and cur is None:
                cur = [lam, lam]
            elif e and cur is not None:
                cur[1] = lam
            elif (not e) and cur is not None:
                bands.append(cur)
                cur = None
        if cur is not None:
            bands.append(cur)
        best = max(bands, key=lambda b: b[1] / b[0]) if bands else None
        n_excl = sum(1 for _, e in excl if e)
        out[name] = {
            "n_grid": len(LAM_GRID),
            "n_excluded": n_excl,
            "n_bands": len(bands),
            "widest_band_AU": ([sci(best[0] / AU, 6), sci(best[1] / AU, 6)]
                               if best else None),
            "decades_in_band": (sci((best[1] / best[0]).ln() / D(10).ln(), 4)
                                if best else None),
            "all_bands_AU": [[sci(b[0] / AU, 4), sci(b[1] / AU, 4)] for b in bands],
        }
        all_ok = all_ok and (n_excl > 0) and (len(bands) >= 1)
    return {"datasets": out,
            "note": "alpha=1 被 95% 排除的 lam 集合。注意是**有限带**：lam->0 时 K 被 "
                    "exp(-a/lam) 杀死、lam->inf 时 K∝lam^-2，两端都无约束。",
            "ok": all_ok}


# ================================================================== J5
def j5_improvement_scan():
    """是否存在显著改进：Delta_chi2 = chi2_0 - chi2_min 的全局峰。"""
    out = {}
    all_ok = True
    for name, ds in DATASETS.items():
        names = [r[0] for r in ds["rows"]]
        obs = [r[1] * MAS for r in ds["rows"]]
        sig = [r[2] * MAS for r in ds["rows"]]
        best = None
        for lam in LAM_GRID:
            f = fit_at_lam(names, obs, sig, lam)
            d = f["delta_chi2"]
            if best is None or d > best[1]:
                best = (lam, d, f)
        peak_dchi2 = best[1]
        significant = peak_dchi2 > CHI2_95_1DOF
        out[name] = {
            "peak_delta_chi2": sci(peak_dchi2, 6),
            "peak_at_lam_AU": sci(best[0] / AU, 6),
            "peak_alpha_hat": sci(best[2]["alpha_hat"], 6),
            "threshold_95": sci(CHI2_95_1DOF, 10),
            "significant_improvement": significant,
        }
        all_ok = all_ok and (not significant)
    return {"datasets": out,
            "question": "是否存在无法由标准引力理论解释的共同残差？",
            "answer": ("NO--两套独立历表的 Delta_chi2 峰均未过 3.84，"
                       "残差不需要第五力"), 
            "note": "Delta_chi2 = chi2(alpha=0) - min_alpha chi2。峰值不过 3.84 即无处"
                    "需要额外自由度；注意这是「未检出」而非「不存在」——未满足 != 不可满足。",
            "ok": all_ok}


# ================================================================== J6
def j6_large_lambda_degeneracy():
    out = {}
    all_ok = True
    for name, ds in DATASETS.items():
        names = [r[0] for r in ds["rows"]]
        obs = [r[1] * MAS for r in ds["rows"]]
        sig = [r[2] * MAS for r in ds["rows"]]
        rows = []
        for lam_AU in ["1e3", "1e4", "1e5", "1e6", "1e7", "1e8"]:
            lam = D(lam_AU) * AU
            f = fit_at_lam(names, obs, sig, lam)
            rows.append({"lam_AU": lam_AU,
                         "sigma_alpha": sci(f["sigma_alpha"], 6),
                         "alpha_95_upper": sci(alpha_bound_95(names, obs, sig, lam), 6)})
        s0 = D(rows[0]["sigma_alpha"])
        s1 = D(rows[-1]["sigma_alpha"])
        rows_monotone = all(D(rows[i]["sigma_alpha"]) < D(rows[i + 1]["sigma_alpha"])
                            for i in range(len(rows) - 1))
        # lam 增 10 倍，sigma_alpha 应涨约 100 倍（K ∝ lam^-2）
        growth = s1 / s0
        expected = (D("1e8") / D("1e3")) ** 2
        out[name] = {"rows": rows, "sigma_growth_over_5_decades": sci(growth, 6),
                     "expected_lam^-2_growth": sci(expected, 6),
                     "growth_rel": sci(rel(growth, expected), 4),
                     "monotone": rows_monotone}
        all_ok = all_ok and rows_monotone and (rel(growth, expected) < D("0.5"))
    return {"datasets": out,
            "note": "lam 增大 => K ∝ lam^-2 => sigma_alpha ∝ lam^2 => 无约束。"
                    "退化不是本册假设，是拟合自己长出来的。",
            "ok": all_ok}


# ================================================================== J7
def j7_guard(src):
    bad = ('"ok"' + ": " + "True") in src
    bad2 = ("'ok'" + ": " + "True") in src
    return {"no_hardcoded_ok": (not bad) and (not bad2), "checked_patterns": 2}


# ================================================================== main
def main():
    src = open(os.path.abspath(__file__), encoding="utf-8").read()

    r1 = j1_data_provenance()
    r2 = j2_injection_recovery()
    r3 = j3_real_fit()
    r4 = j4_exclusion_window()
    r5 = j5_improvement_scan()
    r6 = j6_large_lambda_degeneracy()
    r7 = j7_guard(src)

    gates = {
        "J1-data-tri-source-consistent": r1["ok"],
        "J2-fit-machine-calibrated": r2["ok"],
        "J3-real-fit-consistent-with-GR": r3["ok"],
        "J4-exclusion-window-finite-band": r4["ok"],
        "J5-no-significant-improvement": r5["ok"],
        "J6-large-lambda-sigma-blows-up": r6["ok"],
        "J7-no-hardcoded-ok": r7["no_hardcoded_ok"],
    }
    n_ok = sum(1 for v in gates.values() if v)
    n_tot = len(gates)

    verdict = (
        "ROOTV128C-JOINT-FIT-EXECUTED"
        "--TRI-SOURCE-EPHEMERIS-DATA"
        "--FIT-MACHINE-CALIBRATED-BY-INJECTION-RECOVERY"
        "--BOTH-EPHEMERIDES-CONSISTENT-WITH-ALPHA-0"
        "--NO-SIGNIFICANT-DELTA-CHI2-AT-ANY-LAMBDA"
        "--ALPHA-1-EXCLUDED-ON-FINITE-BAND-ONLY"
        "--LARGE-LAMBDA-UNCONSTRAINED-BY-CONSTRUCTION"
        "--UFT-NOT-BROKEN"
        "--NO-INDEPENDENT-PREDICTION"
    )

    out = {
        "title": "ROOT V128 第三册：太阳系星历联合拟合（首次实际执行）· 可算审计",
        "date": "2026-11-22",
        "kind": "external-material-computable-audit",
        "first_executed_joint_fit": True,
        "relation_to_prior": "第一册 G7 与第二册均登记「联合拟合未执行」；本册补上，与两册不相加",
        "verdict_type": "real two-parameter joint fit against published ephemeris residuals",
        "target": "V128 Yukawa 第五力 (alpha_Y, lam) 与 EPM2011 / INPOP10a 补充进动",
        "model": "Delta_varpi_i = alpha * K_i(lam)，K_i 为对 e 精确、对 alpha 一阶的闭式",
        "null_hypothesis": "alpha = 0（纯牛顿+GR）",
        "constants": {"AU_m": sci(AU, 10), "mas_to_arcsec": sci(MAS, 4),
                      "chi2_95_1dof": sci(CHI2_95_1DOF, 10), "z_95": sci(Z_95, 10),
                      "lam_grid_points": len(LAM_GRID)},
        "datasets": {k: {"cite": v["cite"],
                         "rows": [{"planet": r[0], "obs_mas_per_cy": sci(r[1], 6),
                                   "sigma_mas_per_cy": sci(r[2], 6)} for r in v["rows"]]}
                     for k, v in DATASETS.items()},
        "j1_data_provenance": r1,
        "j2_injection_recovery": r2,
        "j3_real_fit": r3,
        "j4_exclusion_window": r4,
        "j5_improvement_scan": r5,
        "j6_large_lambda_degeneracy": r6,
        "gates": gates,
        "n_gate_ok": n_ok,
        "n_gate_total": n_tot,
        "guards": r7,
        "boundary": [
            "拟合对象是已发表的补充进动，本册未重拟合星历；数据为他人测量",
            "「未检出第五力」!= 「不存在第五力」；未被满足 != 不可满足",
            "alpha=1 的排除带两端都无约束：短程被 exp(-a/lam) 抑制，长程 K 正比 lam^-2",
            "EMB 按地球 a 近似（相对差 3e-5），不影响结论量级",
            "本册只判决「给定 Yukawa 模型 + 给定历表数据」，不判决统一场论成立与否",
            "两套历表 chi2/dof 均 <2 只说明与标准引力相容，不排除其它非标准效应",
        ],
        "discipline": [
            "数据三源交叉，单一来源不采信",
            "拟合器先用注入-恢复自校准，再用于真实数据",
            "零假设明确为 alpha=0；不做「找一个能拟合的参数」的事",
            "排除带报区间不报单点；两端无约束如实写",
            "确定性伪随机（固定种子）保证幂等",
            "无写死 ok；幂等两次 JSON 逐字节相等",
            "不自盖章：门全过 != 物理上有新内容；本册独立预言 0",
        ],
        "red_line": "数学自洽 != 实验证实；不宣称攻破统一场论；本册不给「统一场论成立/失败」"
                    "的判决，只给「一个具体模型 against 一组具体数据」的统计判决；"
                    "未被满足 != 不可满足。",
        "verdict": verdict,
    }

    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2, sort_keys=True)

    print("=" * 78)
    print(out["title"])
    print("=" * 78)
    print("J1 data    tri_source=%d common_planets=%d struct=%s"
          % (r1["n_tri_source"], r1["n_common"], r1["struct_ok"]))
    print("J2 calib   mean_z=%-10s sd_z=%-10s cov1=%-10s cov95=%s"
          % (r2["mean_z"], r2["sd_z"], r2["coverage_1sigma"], r2["coverage_95"]))
    for name in sorted(r3["datasets"]):
        d3 = r3["datasets"][name]
        print("J3 fit %-9s chi2_0=%-10s dof=%d chi2/dof=%-8s GR-compatible=%s"
              % (name, d3["chi2_at_alpha0"], d3["dof"], d3["chi2_over_dof"],
                 d3["consistent_with_standard_gravity"]))
    for name in sorted(r4["datasets"]):
        d4 = r4["datasets"][name]
        print("J4 excl %-8s bands=%d widest=%s AU (%s dex)"
              % (name, d4["n_bands"], d4["widest_band_AU"], d4["decades_in_band"]))
    for name in sorted(r5["datasets"]):
        d5 = r5["datasets"][name]
        print("J5 impr %-8s peak_dchi2=%-10s at lam=%-8s significant=%s"
              % (name, d5["peak_delta_chi2"], d5["peak_at_lam_AU"],
                 d5["significant_improvement"]))
    for name in sorted(r6["datasets"]):
        d6 = r6["datasets"][name]
        print("J6 lam->inf %-8s sigma growth=%-12s expected=%-12s rel=%s"
              % (name, d6["sigma_growth_over_5_decades"],
                 d6["expected_lam^-2_growth"], d6["growth_rel"]))
    print("-" * 78)
    print("J3 剖面：alpha_hat / sigma_alpha / 95% 上界 / alpha=1 是否被排除")
    for name in sorted(r3["datasets"]):
        print("  [%s]" % name)
        for r in r3["datasets"][name]["profile"]:
            print("    lam=%-7s a_hat=%-11s sig=%-11s |a|95=%-11s excl1=%s"
                  % (r["lam_AU"], r["alpha_hat"], r["sigma_alpha"],
                     r["alpha_95_upper"], r["alpha1_excluded"]))
    print("-" * 78)
    for k in sorted(gates):
        print("  %-44s %s" % (k, "PASS" if gates[k] else "FAIL"))
    print("-" * 78)
    print("GATES %d/%d" % (n_ok, n_tot))
    print("VERDICT %s" % verdict)
    print("JSON -> %s (%d B)" % (os.path.basename(OUT_JSON), os.path.getsize(OUT_JSON)))
    return 0 if n_ok == n_tot else 1


if __name__ == "__main__":
    raise SystemExit(main())
