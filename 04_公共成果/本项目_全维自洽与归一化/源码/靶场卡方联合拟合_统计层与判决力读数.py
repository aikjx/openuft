# -*- coding: utf-8 -*-
"""
靶场卡方联合拟合 · 统计层与判决力读数（可复跑）
================================================

本册补的是 openuft 判别式体系里**唯一缺的一层：统计量**。

为什么必须补
------------
仓库已有的判别式全部回答「**能不能派生**」：

    V / V3 / V4 / V5（信息论与秩层）          —— 04_公共成果/…/源码/无量纲靶场审计.py
    定理 C（量纲不可行）· D（旋钮零空间）· H（几何作用量）· F/G/T（算子谱）
    定理 I/J/K/L（靶独立性秩 · 纯数因子 · 可达性）

单靶的「判决力」也已有仪器（07_统一场方程/…/验证脚本/spiral_c35_beta_universality.py）。
但**没有人回答**：多个靶**联合**起来时，某个参数被约束到几位？χ² 多大？自由度是多少？
协方差如何影响结论？——这正是本册的范围。

关键事实（本册的动因）
----------------------
`源码/claims_schema_升级.py` 已给 19 个独立体系的 claims.csv 加出两列
`prediction_value` / `prediction_urel`（UFT-3 登记必填），**但至今没有任何引擎消费它们**：
登记链路是「能登记、无人算」。本册即那个「算」——登记看板会现场扫描全部体系的这两列。

口径（红线：不新造判据）
------------------------
1. 靶表**不新建**：一律复用 `源码/无量纲靶场审计.py` 的 10 靶定义与观测值（单一真源）。
2. 信息增益判别式 **V 不重写**：命中条目直接调上游 `verdict_v()`。
3. 自由度一律走**秩口径**（定理 I：$h_{\\rm eff}=\\operatorname{rank}(J)$），不新造计法。
4. 本册只加**统计量**：$\\chi^2$ / $p$ / $\\delta_{\\min}$ / 协方差矩阵 / 自由度 $\\nu$。
5. 相关系数反解用定理 $\\Sigma_{cov}$ 的**可识别性判据**，并与上游发布读数做回归断言。

统计口径（三段，闭合式，无需求逆）
----------------------------------
    单靶      χ²ᵢ = ((Tᵢ−Oᵢ)/σᵢ)²,   σᵢ = hypot(|Oᵢ|·u_obs, |Tᵢ|·u_th)
              pᵢ  = erfc(√(χ²ᵢ/2))                      (1 dof 生存函数)
              δ_min = σᵢ·√χ²_crit(1, CL)                 「理论至少偏离实测多少才能被判出」
    联合·独立 χ² = Σ χ²ᵢ;                    ν = n_eff − rank(J)
    联合·共模 χ² = Σ wᵢ(rᵢ − ε̂)², wᵢ = 1/σᵢ², ε̂ = Σwᵢrᵢ/Σwᵢ    (把共同观测作为 nuisance profile 掉)
              ν = n_eff − 1 − rank(J)

    χ²_crit(1, 0.95) = 2·erfinv(0.95)²  —— **闭式算出，不硬编码**。
    共模观测 ⇒ Σ = σ²·𝟙 = 秩亏（rank 1 < n）⇒ 只有「差值组合」可判：
    这正是 C51「标定靶 = 最佳靶」的统计一般化。

判定的两条轴（必须分开读，否则会把「自洽」误读成「证据」）
----------------------------------------------------------
    轴 A（自洽性）  χ² ≤ χ²_crit          → 自洽 / 被观测排除
    轴 B（可检验性）Δ_th ≥ δ_min           → 有判别力 / 零判别力
                    （Δ_th = 该机制**所能产生**的最大偏离，必须由条目显式声明）

    四态综合：<br>
      PASS     = 轴 A 自洽 **且** 轴 B 有判别力（真正的可检验预言）<br>
      FAIL     = 轴 A 被排除，**或** 声称是预言却零判别力（不可判 $\\ne$ 通过）<br>
      BOUNDARY = 判别力判定依赖**外部假设**（σ_obs 假设 / Δ_th 未声明）<br>
      INFO     = 恒等式对照（自洽但零增益，不构成证据）

诚实边界（先读）
----------------
1. **本模块不会自己产生 L3**。目标登记为 0 时读数必然是「不可判」——
   要改变 L3，仍需某个体系**真的给出一个无量纲数 + 误差棒**（唯一路线是动力学本征值）。
2. **χ² ≈ 0 不等于证据**：10 靶里是否存在「非拟合的第一性预言 + 独立观测」对，
   本册会如实报数（对照算例表里的发现）。
3. 任意相关矩阵（非共模、非独立）本轮**不收**——需矩阵求逆与秩分解，
   记为 OPEN，不假装已支持。
4. σ_obs 若为外部假设（如历表约束量级）⇒ 该条只能判 BOUNDARY。

产出：数据/靶场卡方联合拟合.json + 数据/靶场卡方联合拟合.md

用法：
    python 靶场卡方联合拟合_统计层与判决力读数.py
    python 靶场卡方联合拟合_统计层与判决力读数.py --teeth
"""

import os
import sys
import json
import time
import importlib.util
from fractions import Fraction

from mpmath import mp, mpf, erfc, erfinv, sqrt, gammainc, inf, nstr

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.dont_write_bytecode = True           # 不向仓库写入 .pyc（导入上游脚本时）
# 与上游《无量纲靶场审计》一致取 dps=80：上游在模块级改的是同一个 mp 单例，
# 此处显式声明并（在导入后）复位，避免读数依赖导入顺序。
mp.dps = 80

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT_DIR = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化", "数据")
UPSTREAM = os.path.join(HERE, "无量纲靶场审计.py")
REGISTRY_CHECKER = os.path.join(HERE, "靶场登记列校验_写入侧门禁.py")

CL = mpf("0.95")
CHI2_CRIT_1 = 2 * erfinv(CL) ** 2         # 1 dof 的 95% 临界值（闭式）

# ---------------------------------------------------------------------------
# 一、外部输入表（引上游，附回归断言）
# ---------------------------------------------------------------------------
# 锚的相对不确定度：引《派生核算 VII》定理 Σ_cov 的 UNC_REL（s14 体系无此表，故此处登记来源）
ANCHOR_UREL = {
    "c": 0.0, "hbar": 0.0, "e": 0.0, "k_B": 0.0,
    "G": 2.2e-5, "eps0": 1.5e-10, "m_e": 3.0e-10,
    "m_mu": 2.2e-8, "m_p": 3.1e-10, "m_P": 1.1e-5,
}
# CODATA 括号形式公布的**比值**（尾数, 末位不确定度），用于反解相关系数
RATIO_PUB = {
    "m_p_over_me": ("1836.15267343", "11"),
    "m_mu_over_me": ("206.7682830", "46"),
}
DELTA_RATIO_READ = mpf("0.10")           # 比值不确定度的相对读取精度（1 位有效数字基准）
IDENT_MARGIN = mpf("3")                  # 可识别性门槛（定理 Σ_cov）

# 上游发布的回归基准（本册实现必须复现；不复现则报 FAIL）
SIGMA_COV_EXPECT = {
    "m_p_over_me": {"rho": mpf("0.9812"), "margin_lo": mpf("200"), "margin_hi": mpf("300"),
                    "identifiable": True},
    "m_mu_over_me": {"margin_lo": mpf("0.05"), "margin_hi": mpf("0.20"),
                     "identifiable": False},
}


def load_upstream():
    """导入上游靶表引擎（同一真源，不复制靶表）。"""
    spec = importlib.util.spec_from_file_location("wudi_targets", UPSTREAM)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mp.dps = 80                          # 上游模块级会改同一个 mp 单例，显式复位
    return mod


# ---------------------------------------------------------------------------
# 二、统计原语
# ---------------------------------------------------------------------------

def chi2_crit(dof=1, cl=CL):
    """1 dof 的临界值用 erfinv 闭式；dof>1 用 gammainc 反解（无闭式，标记为近似）。"""
    if dof == 1:
        return 2 * erfinv(cl) ** 2
    lo, hi = mpf(0), mpf(1000)
    for _ in range(200):
        mid = (lo + hi) / 2
        if sf_chi2(mid, dof) > 1 - cl:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def sf_chi2(x, dof):
    """卡方生存函数 P(X > x)（上不完全 gamma 正则化）。"""
    if x <= 0:
        return mpf(1)
    if dof == 1:
        return erfc(sqrt(x / 2))
    return gammainc(mpf(dof) / 2, x / 2, inf, regularized=True)


def hypot2(a, b):
    return sqrt(a * a + b * b)


def fmt_p_str(s):
    """p 值显示：数值下溢时给**界**，不给伪造精度（如 2.4e-2905382）。"""
    if s is None:
        return "—"
    try:
        if mpf(s) < mpf("1e-300"):
            return "≈0（< 1e-300）"
    except Exception:
        return str(s)
    return str(s)


def single_reading(theory, obs, sigma_obs, sigma_th, delta_th, cl=CL):
    """单靶读数：χ²、p、δ_min、两轴判定。delta_th=None 表示未声明机制幅度。"""
    sigma = hypot2(sigma_obs, sigma_th)
    if sigma <= 0:
        return {"sigma": mpf(0), "chi2": None, "p": None, "delta_min": None,
                "axis_a": "FAIL", "axis_b": "UNDECLARED",
                "note": "σ ≤ 0：不确定度未定义（Σ 非正定）"}
    r = theory - obs
    chi2 = (r / sigma) ** 2
    p = sf_chi2(chi2, 1) if chi2 < mpf(1e6) else mpf(0)
    delta_min = sigma * sqrt(CHI2_CRIT_1)
    axis_a = "pass" if chi2 <= CHI2_CRIT_1 else "fail"
    if delta_th is None:
        axis_b, ratio = "UNDECLARED", None
    else:
        ratio = delta_th / delta_min
        axis_b = "testable" if ratio >= 1 else "zero_power"
    return {"sigma": sigma, "residual": r, "chi2": chi2, "p": p,
            "delta_min": delta_min, "axis_a": axis_a, "axis_b": axis_b,
            "delta_th": delta_th, "power_ratio": ratio}


def verdict_axes(reading, kind):
    """把两条轴合成为四态。kind: identity_control / prediction / synthetic_control

    注意：两条轴的标签先做**大小写归一**再比较——首版曾因轴 A 写成 `fail` 而这里比
    的是 `FAIL`，使「轴 A 被排除」这一支永远走不到（SU(5) 因此被判成「零判别力」
    而不是「被排除」，理由错、结论偶然相同）。这是本册自查修掉的真 bug。
    """
    a = reading["axis_a"].upper()
    b = reading["axis_b"].upper()
    if a == "FAIL":
        return "FAIL", "轴 A：χ² 超过临界值 ⇒ 被观测排除"
    if b == "UNDECLARED":
        if kind == "identity_control":
            return "INFO", "轴 B：恒等式不产生偏离（Δ_th ≡ 0）⇒ 自洽但零判别力、零增益"
        return "BOUNDARY", "轴 B：未声明机制幅度 Δ_th ⇒ 判别力不可评（自洽 ≠ 可检验）"
    if b == "ZERO_POWER":
        if kind == "identity_control":
            return "INFO", "轴 B：恒等式 Δ_th < δ_min ⇒ 零判别力、零增益"
        return "FAIL", "轴 B：Δ_th < δ_min ⇒ 零独立判别力（不可判，按 FAIL 计，不作通过）"
    if kind == "synthetic_control":
        return "INFO", "合成对照（不入台账）：两轴均过 ⇒ 仪器通过"
    return "PASS", "两轴均过：自洽且有判别力"


def frac_rank(rows):
    """整数/有理矩阵的精确秩（Fraction 高斯消元，避免浮点伪秩）。"""
    m = [[Fraction(c) for c in row] for row in rows]
    if not m:
        return 0
    ncol = len(m[0])
    rank, row = 0, 0
    for col in range(ncol):
        piv = None
        for i in range(row, len(m)):
            if m[i][col] != 0:
                piv = i
                break
        if piv is None:
            continue
        m[row], m[piv] = m[piv], m[row]
        inv = Fraction(1) / m[row][col]
        m[row] = [v * inv for v in m[row]]
        for i in range(len(m)):
            if i != row and m[i][col] != 0:
                f = m[i][col]
                m[i] = [a - f * b for a, b in zip(m[i], m[row])]
        row += 1
        rank += 1
        if row == len(m):
            break
    return rank


def ratio_u_rel(value_str, digits_str):
    """'1836.15267343(11)' → 相对不确定度（(11) 作用于末两位小数）。"""
    v = mpf(value_str)
    decimals = len(value_str.split(".")[1]) if "." in value_str else 0
    unc = mpf(digits_str) * mpf(10) ** (-decimals)
    return unc / v


def reverse_rho(urel_i, urel_j, urel_ratio):
    """定理 Σ_cov：由公布比值反解相关系数 + 可识别性余量。返回 (rho, margin)。"""
    a, b, sr = mpf(urel_i), mpf(urel_j), mpf(urel_ratio)
    num = a * a + b * b - sr * sr
    rho = num / (2 * a * b)
    margin = abs(num) / (2 * DELTA_RATIO_READ * sr * sr)
    return rho, margin


def identifiable(rho, margin):
    """定理 Σ_cov 的可识别性判据：余量过门槛 **且** |ρ| ≤ 1（两条都必要，
    缺后者会把「解析解越界」当成有效相关）。"""
    return margin > IDENT_MARGIN and abs(rho) <= 1


def joint_independent(rows, rank_j):
    """独立观测：χ² = Σχ²ᵢ，ν = n_eff − rank(J)。"""
    n_eff = len(rows)
    chi2 = sum((r["residual"] / r["sigma"]) ** 2 for r in rows)
    nu = n_eff - rank_j
    return {"mode": "independent", "n_eff": n_eff, "rank_j": rank_j, "nu": nu,
            "chi2": chi2, "p": sf_chi2(chi2, nu) if nu > 0 else None,
            "sigma_rank": n_eff}


def joint_shared_observation(rows, rank_j):
    """共模观测：把共同观测 ε 作为 nuisance profile 掉（闭合式）。
    Σ = σ²·𝟙 ⇒ 秩亏（rank(Σ)=1 < n）⇒ 只有差值组合可判。"""
    w = [1 / (r["sigma"] ** 2) for r in rows]
    sw = sum(w)
    eps_hat = sum(wi * r["residual"] for wi, r in zip(w, rows)) / sw
    chi2 = sum(wi * (r["residual"] - eps_hat) ** 2 for wi, r in zip(w, rows))
    n_eff = len(rows)
    nu = n_eff - 1 - rank_j
    return {"mode": "shared_observation", "n_eff": n_eff, "rank_j": rank_j, "nu": nu,
            "chi2": chi2, "p": sf_chi2(chi2, nu) if nu > 0 else None,
            "sigma_rank": 1, "eps_hat": eps_hat,
            "note": "Σ = σ²·𝟙 秩亏（rank=1 < n）：共同观测方向被 profile 掉，只有差值判"}


# ---------------------------------------------------------------------------
# 三、条目表
# ---------------------------------------------------------------------------
# kind: identity_control（真实数据恒等式）· falsification_control（真实数据被排除）
#       · synthetic_control（合成，仅仪器校准）· prediction（登记预言，将来由 claims.csv 注入）
#
# J：对数导数行 ∂lnT/∂ln(锚)（整数指数）—— 秩口径的唯一输入（定理 I）。
# group：联合拟合分组；corr：该组的观测相关模式。

def build_entries(up):
    E = []
    # --- A1：真实数据恒等式 α_grav(e) ≡ (m_e/m_P)²（上游定理 W / V0-a 的去重规则）---
    E.append({
        "entry_id": "IDENT-alpha_grav_e",
        "kind": "identity_control",
        "group": "ident",
        "corr": "independent",
        "target_key": "alpha_grav_e",
        "obs": up.M_E / up.M_P,                       # 与上游同一批常数
        "theory": (up.M_E / up.M_P) ** 2,             # 恒等式右侧（由锚复算）
        "theory_urel": mpf(0),
        "delta_th": mpf(0),                            # 恒等式不产生偏离
        "J": {"m_e": 2, "m_P": -2},
        "n_free": 0,
        "note": "α_grav(e) ≡ (m_e/m_P)² 为恒等式（消耗 m_e、m_P 两锚）",
    })
    # --- A2：真实数据被排除对照 SU(5) 树级 sin²θ_W = 3/8 ---
    E.append({
        "entry_id": "SU5-sin2_thetaW",
        "kind": "falsification_control",
        "group": "ident",
        "corr": "independent",
        "target_key": "sin2_thetaW",
        "obs": mpf("0.23122"),
        "theory": mpf(3) / mpf(8),
        "theory_urel": mpf(0),                         # 树级预言是精确数
        "delta_th": mpf(0),
        "J": {},
        "n_free": 0,
        "note": "SU(5) 树级 sin²θ_W = 3/8（教科书级被排除预言，用作仪器的非退化对照）",
    })
    # --- B：合成对照（三人造靶，同一合成观测，共模）覆盖三条统计路径 ---
    SYN_OBS, SYN_UREL = mpf("1.0"), mpf("0.01")
    for tag, off, note in (("aligned", mpf(0), "理论=观测 ⇒ χ² = 0"),
                           ("one-sigma", mpf("0.01"), "理论=观测+1σ ⇒ χ² = 1，仍自洽"),
                           ("five-sigma", mpf("0.05"), "理论=观测+5σ ⇒ χ² = 25，应被排除")):
        E.append({
            "entry_id": "SYN-" + tag,
            "kind": "synthetic_control",
            "group": "synth",
            "corr": "shared_observation",
            "target_key": None,                        # 人造靶，不入 10 靶表
            "obs": SYN_OBS,
            "obs_urel": SYN_UREL,
            "theory": SYN_OBS + off,
            "theory_urel": mpf(0),
            "delta_th": mpf("0.10"),                   # 声明机制幅度 10σ
            "J": {},
            "n_free": 0,
            "note": "合成对照（不入台账）：" + note,
        })
    return E


# 判决力上界读数（C48–C51）：无配对观测，只用 (δ_th, σ) 两轴判据
READINGS = [
    {"id": "C50", "name": "C25 高阶本征能级谱宽（n=6）", "target": "alpha",
     "delta_th": "1.08887e-75", "delta_th_kind": "relative", "sigma": "1.5e-10",
     "sigma_source": "α 的观测相对不确定度", "sigma_is_assumption": False,
     "ref": "判定_空间螺旋V22收官_全链_2026-09-26.md §1.2"},
    {"id": "C51-金星", "name": "金星近日点进动几何修正", "target": "近日点进动",
     "delta_th": "4.9330717e-3", "delta_th_kind": "absolute", "sigma": "0.1",
     "sigma_unit": "角秒/百年", "sigma_source": "历表约束量级（外部假设，待核实）",
     "sigma_is_assumption": True,
     "ref": "判定_空间螺旋V22收官_全链_2026-09-26.md §2.4"},
    {"id": "C51-地球", "name": "地球近日点进动几何修正", "target": "近日点进动",
     "delta_th": "1.5885551e-3", "delta_th_kind": "absolute", "sigma": "0.1",
     "sigma_unit": "角秒/百年", "sigma_source": "历表约束量级（外部假设，待核实）",
     "sigma_is_assumption": True,
     "ref": "判定_空间螺旋V22收官_全链_2026-09-26.md §2.4"},
]


# ---------------------------------------------------------------------------
# 四、登记看板（消费 claims.csv 的 prediction_value / prediction_urel）
# ---------------------------------------------------------------------------

UFT3_COLS = ("prediction_value", "prediction_urel")


def load_registry_checker():
    """登记列语义的**单一真源**：导入 `靶场登记列校验_写入侧门禁.py`。

    理由（仓库教训：「同一校验逻辑多处复制时豁免口径必须对齐」）：这两列的
    数值解析与合法/非法判定只应有一处实现。本层**不再自行解析**，而是委派；
    写入侧门禁与统计层因此天然同口径。
    """
    spec = importlib.util.spec_from_file_location("tau_registry_checker", REGISTRY_CHECKER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def scan_registry(checker):
    """委派给单一真源；另外把**适用范围外**的台账（07 层 5 列口径）计入文件清单，
    以便看板表逐文件列全（该行按「无 UFT-3 列」显示，不判违规）。"""
    rows, paths = checker.scan_registry()
    for o in checker.scan_out_of_scope():
        paths.append(o["file"])
    return rows, paths


# ---------------------------------------------------------------------------
# 五、牙齿（变异体 + 阳性对照）
# ---------------------------------------------------------------------------

def run_teeth(up):
    T = []

    def rec(name, ok, detail):
        T.append({"name": name, "ok": bool(ok), "detail": detail})

    # T1 σ 缩小 10× ⇒ χ² 必须抬升 100×（若实现把 σ 用错，倍数就不是 100）
    base = single_reading(mpf("1.01"), mpf("1.0"), mpf("0.01"), mpf(0), mpf("0.1"))
    tight = single_reading(mpf("1.01"), mpf("1.0"), mpf("0.001"), mpf(0), mpf("0.1"))
    ratio = tight["chi2"] / base["chi2"]
    rec("T1 σ 缩小 10× ⇒ χ² 抬升 100×", abs(ratio - 100) < mpf("1e-20"),
        "实测倍数 %s" % nstr(ratio, 8))

    # T2 理论=观测 且 Δ_th=0 ⇒ 不得判 PASS（必须 INFO/零判别力）
    r0 = single_reading(mpf("1.0"), mpf("1.0"), mpf("0.01"), mpf(0), mpf(0))
    v0, _ = verdict_axes(r0, "identity_control")
    rec("T2 χ²=0 且 Δ_th=0 ⇒ 不判 PASS", v0 == "INFO" and r0["chi2"] == 0,
        "判定 %s，χ² = %s" % (v0, nstr(r0["chi2"], 3)))

    # T3 σ ≤ 0 ⇒ 必须报 FAIL（Σ 非正定），不得静默算出 χ²
    r_neg = single_reading(mpf("2.0"), mpf("1.0"), mpf(0), mpf(0), mpf("1"))
    rec("T3 σ ≤ 0 ⇒ 报 FAIL 而非静默", r_neg["axis_a"] == "FAIL" and r_neg["chi2"] is None,
        "axis_a=%s，χ²=%s" % (r_neg["axis_a"], r_neg["chi2"]))

    # T4 ρ 越界（|ρ|>1）⇒ 即便余量过门槛也必须判不可识别（两条判据都必要）
    rho_bad, margin_bad = reverse_rho(1.0e-10, 1.0e-10, 1.0e-8)
    rec("T4 |ρ|>1 ⇒ 即便余量过门槛亦判不可识别",
        abs(rho_bad) > 1 and margin_bad > IDENT_MARGIN
        and not identifiable(rho_bad, margin_bad),
        "ρ̂ = %s，余量 %s（> %s）但 |ρ̂|>1 ⇒ 拒收"
        % (nstr(rho_bad, 6), nstr(margin_bad, 4), nstr(IDENT_MARGIN, 3)))

    # T5 条目为空 ⇒ 不得输出联合 χ²
    empty = joint_independent([], 0)
    rec("T5 空条目 ⇒ 无联合 χ² 且 ν ≤ 0", empty["chi2"] == 0 and empty["nu"] <= 0,
        "ν = %d（无自由度 ⇒ p 不给）" % empty["nu"])

    # T6 自由度走秩口径：构造 rank(J) = 2 的两条目，ν 必须 = 2 − 2 = 0
    rows2 = [{"residual": mpf("0.01"), "sigma": mpf("0.01")},
             {"residual": mpf("0.01"), "sigma": mpf("0.01")}]
    j2 = frac_rank([[1, -2], [2, -4]])          # 两行成比例 ⇒ 秩 1
    j3 = frac_rank([[1, 0], [0, 1]])            # 秩 2
    rec("T6 ν 走秩口径（秩 1 → ν=1；秩 2 → ν=0）",
        joint_independent(rows2, j2)["nu"] == 1 and joint_independent(rows2, j3)["nu"] == 0,
        "rank=1⇒ν=1；rank=2⇒ν=0")

    # T7 共模观测 ⇒ Σ 秩亏 ⇒ 只有差值判（χ² 必须小于把观测当独立的 Σχ²ᵢ）
    rows3 = [{"residual": mpf("0.00"), "sigma": mpf("0.01")},
             {"residual": mpf("0.01"), "sigma": mpf("0.01")},
             {"residual": mpf("0.05"), "sigma": mpf("0.01")}]
    ji = joint_independent(rows3, 0)
    js = joint_shared_observation(rows3, 0)
    naive = sum((r["residual"] / r["sigma"]) ** 2 for r in rows3)
    rec("T7 共模 Σ 秩亏 ⇒ 判别式不同于独立 Σχ²ᵢ",
        js["sigma_rank"] == 1 and js["chi2"] < naive and ji["chi2"] == naive,
        "共模 χ² = %s vs Σχ²ᵢ = %s" % (nstr(js["chi2"], 6), nstr(naive, 6)))

    # T8 p 值边界：χ²=0 ⇒ p=1；χ²=χ²_crit ⇒ p=0.05；χ²→∞ ⇒ p→0
    rec("T8 p 值边界（0⇒1；临界⇒0.05；大⇒0）",
        sf_chi2(mpf(0), 1) == 1
        and abs(sf_chi2(CHI2_CRIT_1, 1) - mpf("0.05")) < mpf("1e-20")
        and sf_chi2(mpf("1e4"), 1) < mpf("1e-100"),
        "p(0)=1；p(χ²_crit)=%s" % nstr(sf_chi2(CHI2_CRIT_1, 1), 10))

    # P1 阳性对照：定理 Σ_cov 回归（上游发布读数必须被复现）
    sr_p = ratio_u_rel(*RATIO_PUB["m_p_over_me"])
    sr_m = ratio_u_rel(*RATIO_PUB["m_mu_over_me"])
    rho_p, mar_p = reverse_rho(ANCHOR_UREL["m_p"], ANCHOR_UREL["m_e"], sr_p)
    rho_m, mar_m = reverse_rho(ANCHOR_UREL["m_mu"], ANCHOR_UREL["m_e"], sr_m)
    exp = SIGMA_COV_EXPECT
    ok_p1 = (abs(rho_p - exp["m_p_over_me"]["rho"]) < mpf("5e-4")
             and exp["m_p_over_me"]["margin_lo"] < mar_p < exp["m_p_over_me"]["margin_hi"]
             and exp["m_mu_over_me"]["margin_lo"] < mar_m < exp["m_mu_over_me"]["margin_hi"]
             and identifiable(rho_p, mar_p) and not identifiable(rho_m, mar_m))
    rec("P1 阳性对照：定理 Σ_cov 回归（ρ=+0.9812 / 余量 254× 与 0.11×）", ok_p1,
        "ρ(m_p/m_e)=%s 余量=%s 可识别=%s；m_μ/m_e ρ=%s 余量=%s 可识别=%s"
        % (nstr(rho_p, 6), nstr(mar_p, 5), identifiable(rho_p, mar_p),
           nstr(rho_m, 6), nstr(mar_m, 4), identifiable(rho_m, mar_m)))

    # P2 阳性对照：α_grav(e) ≡ (m_e/m_P)² ⇒ χ²≈0 且零增益（V<0）
    e_ident = build_entries(up)[0]
    obs = up.build_targets()[5]        # alpha_grav_e
    th = e_ident["theory"]
    sig = abs(mpf(obs["value"])) * mpf(obs["urel"])
    chi2_i = ((th - mpf(obs["value"])) / sig) ** 2
    V, code, _ = up.verdict_v(1, 0, 2)
    rec("P2 阳性对照：α_grav_e ≡ (m_e/m_P)² 自洽（χ²≈0）但 V<0 无增益",
        chi2_i < mpf("1e-12") and code == "C" and V < 0,
        "χ² = %s，V = %s（码 %s）" % (nstr(chi2_i, 4), V, code))
    return T


# ---------------------------------------------------------------------------
# 六、主流程
# ---------------------------------------------------------------------------

def analyse(up, entries):
    targets = {t["key"]: t for t in up.build_targets()}
    def obs_of(e):
        if e["target_key"] is None:                     # 合成靶
            return e["obs"], mpf(e["obs_urel"])
        t = targets[e["target_key"]]
        return mpf(t["value"]), mpf(t["urel"])

    # 逐条目读数
    rows = []
    for e in entries:
        obs, obs_urel = obs_of(e)
        sigma_obs = abs(obs) * obs_urel
        sigma_th = abs(e["theory"]) * mpf(e["theory_urel"])
        rd = single_reading(mpf(e["theory"]), obs, sigma_obs, sigma_th, e["delta_th"])
        verdict, why = verdict_axes(rd, e["kind"])
        n_anchor = len([k for k, v in e["J"].items() if v != 0])
        V = code = None
        if rd["chi2"] is not None and rd["chi2"] <= CHI2_CRIT_1:
            V, code, _ = up.verdict_v(1, e["n_free"], n_anchor)
        rows.append({"entry_id": e["entry_id"], "kind": e["kind"], "group": e["group"],
                     "target": e["target_key"] or "（合成靶）",
                     "theory": nstr(mpf(e["theory"]), 12), "obs": nstr(obs, 12),
                     "obs_urel": nstr(obs_urel, 4), "J": e["J"], "n_free": e["n_free"],
                     "n_anchor": n_anchor, "V": (None if V is None else float(V)),
                     "V_code": code, "note": e["note"],
                     "sigma": nstr(rd["sigma"], 8),
                     "chi2": (None if rd["chi2"] is None else nstr(rd["chi2"], 8)),
                     "p": (None if rd["p"] is None else nstr(rd["p"], 8)),
                     "delta_min": (None if rd["delta_min"] is None else nstr(rd["delta_min"], 8)),
                     "delta_th": nstr(mpf(e["delta_th"]), 8),
                     "power_ratio": (None if rd["power_ratio"] is None
                                     else nstr(rd["power_ratio"], 6)),
                     "axis_a": rd["axis_a"], "axis_b": rd["axis_b"],
                     "verdict": verdict, "reason": why})

    # 联合拟合（按组）
    joints = []
    for gname in sorted({e["group"] for e in entries}):
        grp = [e for e in entries if e["group"] == gname]
        keys = sorted({k for e in grp for k in e["J"]})
        Jrows = [[Fraction(e["J"].get(k, 0)) for k in keys] for e in grp]
        rj = frac_rank(Jrows)
        cal = [{"residual": single_reading(
                    mpf(e["theory"]), obs_of(e)[0],
                    abs(obs_of(e)[0]) * obs_of(e)[1],
                    abs(e["theory"]) * mpf(e["theory_urel"]),
                    e["delta_th"])["residual"],
                "sigma": single_reading(
                    mpf(e["theory"]), obs_of(e)[0],
                    abs(obs_of(e)[0]) * obs_of(e)[1],
                    abs(e["theory"]) * mpf(e["theory_urel"]),
                    e["delta_th"])["sigma"]} for e in grp]
        mode = grp[0]["corr"]
        joint = (joint_independent(cal, rj) if mode == "independent"
                 else joint_shared_observation(cal, rj))
        joint["group"] = gname
        joint["keys"] = keys
        joint["entries"] = [e["entry_id"] for e in grp]
        joint["n"] = len(grp)
        joint["chi2"] = nstr(joint["chi2"], 8)
        joint["p"] = None if joint["p"] is None else nstr(joint["p"], 8)
        if "eps_hat" in joint:
            joint["eps_hat"] = nstr(joint["eps_hat"], 8)
        joint["verdict"] = (
            "FAIL" if (joint["nu"] > 0 and mpf(joint["p"]) < (1 - CL))
            else ("BOUNDARY" if joint["nu"] <= 0 else "PASS"))
        joint["reason"] = (
            "ν ≤ 0：无自由度（条目数不足以约束）⇒ 只报诊断，不给 p"
            if joint["nu"] <= 0 else
            ("p ≥ 0.05：与数据自洽" if joint["verdict"] == "PASS"
             else "p < 0.05：被数据排除"))
        joints.append(joint)

    return targets, rows, joints


def analyse_readings():
    out = []
    for r in READINGS:
        d = mpf(r["delta_th"])
        if r["delta_th_kind"] == "relative":
            sig = mpf(r["sigma"])                    # 与 α 的相对不确定度同量纲
        else:
            sig = mpf(r["sigma"])
        ratio = d / sig
        chi2 = ratio ** 2
        sigma_need = d / sqrt(CHI2_CRIT_1)           # 要打到临界所需的观测精度
        out.append({
            "id": r["id"], "name": r["name"], "target": r["target"],
            "delta_th": r["delta_th"], "sigma": r["sigma"],
            "sigma_unit": r.get("sigma_unit", ""),
            "sigma_source": r["sigma_source"],
            "sigma_is_assumption": r["sigma_is_assumption"],
            "ratio": nstr(ratio, 6), "chi2_expected": nstr(chi2, 6),
            "chi2_crit": nstr(CHI2_CRIT_1, 8),
            "sigma_need": nstr(sigma_need, 6),
            "orders_below": nstr(-mp.log10(ratio) if ratio > 0 else mpf(999), 6),
            "testable": chi2 >= CHI2_CRIT_1,
            "verdict": ("FAIL" if chi2 < CHI2_CRIT_1 else "PASS"),
            "boundary": ("BOUNDARY" if r["sigma_is_assumption"] else None),
            "ref": r["ref"],
        })
    return out


STATE_LABEL = {"pass": "pass", "fail": "fail"}


def build_findings(rows, joints, readings, registry, n_files):
    F = []

    def add(fid, state, text, evidence):
        assert state in ("PASS", "FAIL", "BOUNDARY", "INFO"), state
        F.append({"id": fid, "state": state, "text": text, "evidence": evidence})

    n_pass = sum(1 for r in rows if r["verdict"] == "PASS")
    n_info = sum(1 for r in rows if r["verdict"] == "INFO")
    n_fail = sum(1 for r in rows if r["verdict"] == "FAIL")

    add("S-0", "INFO",
        "口径：靶表与 V 复用上游（单一真源）；自由度走秩口径（定理 I）；"
        "相关系数反解用定理 Σ_cov 的可识别性判据（余量过门槛 **且** |ρ| ≤ 1）。"
        "本册只加统计量，不新造判据",
        "见产物 §〇 与文档头「统计口径」")
    add("S-1", "PASS",
        "统计层建立：单靶 χ²/p/δ_min + 联合（独立 / 共模 profile）+ 秩口径自由度，"
        "全部为闭合式，临界值由 2·erfinv(0.95)² 算出（不硬编码）",
        "自检在 --teeth 下给出逐项证据（见牙齿节）")
    add("S-2", "PASS" if n_fail >= 1 else "FAIL",
        "非退化对照生效：SU(5) 树级 sin²θ_W = 3/8 被本仪器以 χ² 判出排除",
        "条目 SU5-sin2_thetaW（真实观测值 0.23122 ± 1.7e-4）")
    add("S-3", "INFO",
        "恒等式对照：α_grav(e) ≡ (m_e/m_P)² 自洽（χ²≈0）但**零判别力且 V<0（伪派生）**"
        "——「χ²≈0」不等于证据，这是本册的核心读数",
        "条目 IDENT-alpha_grav_e；V 由上游 verdict_v 给出")
    for j in joints:
        add("J-" + j["group"], j["verdict"],
            "联合拟合组 `%s`（%s，%d 条目，rank(J)=%d，rank(Σ)=%d）：χ²=%s，ν=%d，p=%s"
            % (j["group"], j["mode"], j["n"], j["rank_j"], j["sigma_rank"],
               j["chi2"], j["nu"], fmt_p_str(j["p"])),
            j["reason"])
    for r in readings:
        unit = (" " + r["sigma_unit"]) if r["sigma_unit"] else ""
        add("R-" + r["id"], r["verdict"],
            "判决力上界：%s 的 Δ_th/σ = %s ⇒ 期望 χ² = %s < χ²_crit = %s ⇒ 零独立判别力"
            "（低 %s 个量级；需观测精度达 %s%s 才可判）"
            % (r["name"], r["ratio"], r["chi2_expected"], r["chi2_crit"],
               r["orders_below"], r["sigma_need"], unit),
            r["ref"] + ("（σ 为外部假设 ⇒ 本条附加 BOUNDARY）" if r["boundary"] else ""))
    n_reg = sum(1 for r in registry if r["registered"])
    errs = [r for r in registry if r["severity"] == "ERROR"]
    warns = [r for r in registry if r["severity"] == "WARN"]
    add("REG-1", "INFO",
        "UFT-3 登记看板（**委派** `源码/靶场登记列校验_写入侧门禁.py`，登记列语义单一真源）："
        "扫描 claims.csv **%d 个文件**；`prediction_value` 与 `prediction_urel` "
        "**两列齐备且均为数值**的条目数 = **%d**（另有 ERROR %d 条、WARN %d 条）"
        % (n_files, n_reg, len(errs), len(warns)),
        "字段名取自 claims_schema_升级.py 的实际输出表头（14 列）")
    if errs:
        add("REG-2", "FAIL",
            "登记列数据卫生（ERROR）：**%d 条**不可解析为数值（或 urel 为负）"
            "⇒ 空口文字不得冒充已登记靶；改正须由所属体系自行完成（本册不改他人台账）"
            % len(errs),
            "；".join("%s 的 %s：prediction_value=「%s」、prediction_urel=「%s」"
                      % (r["owner"], r["claim_id"], r["prediction_value"],
                         r["prediction_urel"]) for r in errs[:5]))
    else:
        add("REG-2", "INFO", "登记列数据卫生（ERROR 级）：无「两列齐备但非数值」的行",
            "校验规则：两列均可解析为数值（mpf 或有理数 a/b），且 urel ≥ 0")
    if warns:
        add("REG-3", "BOUNDARY",
            "登记列告警（WARN）：**%d 条**登记不完整（只填一列）或 `urel=0` 但值非整数 "
            "⇒ 不能参与 χ²，也不计入登记数" % len(warns),
            "；".join("%s 的 %s：%s"
                      % (r["owner"], r["claim_id"], r["reason"]) for r in warns[:5]))
    add("OPEN-1", "BOUNDARY",
        "任意相关矩阵（非独立、非共模）本轮不收：需矩阵求逆 + 秩分解，"
        "记为 OPEN；已收的两种模式（独立 / 共模 profile）各有闭合式",
        "口径见本册文档头「统计口径」")
    return F


def render_md(payload):
    P = payload
    L = []
    A = L.append
    A("# 靶场卡方联合拟合 · 统计层与判决力读数（可复跑产物）\n")
    A("> 本文件由 `源码/靶场卡方联合拟合_统计层与判决力读数.py` 生成，**请勿手工编辑**。\n")
    A("> mpmath dps=%d · Python %s · 生成于 %s\n"
      % (P["mpmath_dps"], P["python"], P["generated_utc"]))
    A("\n## 〇、本册范围（不新造判据）\n")
    A("靶表与信息增益判别式 V 一律**复用** `源码/无量纲靶场审计.py`（同一真源）；"
      "自由度走**秩口径**（定理 I，$h_{\\rm eff}=\\operatorname{rank}(J)$）；"
      "相关系数反解用定理 $\\Sigma_{cov}$ 的可识别性判据。本册只加**统计量**。\n")
    A("\n## 一、逐条目读数（两条轴分开读）\n")
    A("轴 A（自洽性）：$\\chi^2 \\le \\chi^2_{\\rm crit}$。轴 B（可检验性）：$\\Delta_{th} \\ge \\delta_{\\min}$。\n")
    A("| 条目 | 类型 | 靶 | 理论 | 观测 | σ | χ² | p | δ_min | Δ_th | 轴A | 轴B | **判定** |")
    A("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in P["rows"]:
        A("| `%s` | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | **%s** |"
          % (r["entry_id"], r["kind"], r["target"], r["theory"], r["obs"], r["sigma"],
             r["chi2"] if r["chi2"] is not None else "—",
             fmt_p_str(r["p"]),
             r["delta_min"] if r["delta_min"] is not None else "—",
             r["delta_th"], r["axis_a"], r["axis_b"], r["verdict"]))
    A("\n## 二、联合拟合（协方差矩阵与自由度）\n")
    A("| 组 | 模式 | 条目 | rank(J) | rank(Σ) | ν | χ² | p | 判定 |")
    A("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for j in P["joints"]:
        A("| `%s` | %s | %d | %d | %d | %d | %s | %s | **%s** |"
          % (j["group"], j["mode"], j["n"], j["rank_j"], j["sigma_rank"],
             j["nu"], j["chi2"], fmt_p_str(j["p"]), j["verdict"]))
    for j in P["joints"]:
        A("\n- `%s`：%s%s" % (j["group"], j["reason"],
                              ("　" + j.get("note", "")) if j.get("note") else ""))
    A("\n## 三、判决力上界读数（C48–C51）\n")
    A("无配对观测的候选靶，只用 (Δ_th, σ) 两轴判据。**低 N 个量级**表示理论所能产生的偏离"
      "比观测精度低多少个数量级。\n")
    A("| 读数 | 靶 | Δ_th | σ（观测） | Δ_th/σ | 期望 χ² | χ²_crit | 低量级 | 需达精度 | 判定 |")
    A("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in P["readings"]:
        A("| `%s` | %s | %s | %s %s | %s | %s | %s | %s | %s %s | **%s**%s |"
          % (r["id"], r["target"], r["delta_th"], r["sigma"], r["sigma_unit"],
             r["ratio"], r["chi2_expected"], r["chi2_crit"], r["orders_below"],
             r["sigma_need"], r["sigma_unit"], r["verdict"],
             "（σ 为外部假设 ⇒ BOUNDARY）" if r["sigma_is_assumption"] else ""))
    A("\n## 四、UFT-3 登记看板（消费 prediction_value / prediction_urel）\n")
    A("登记口径：**两列齐备 且 均可解析为数值（urel ≥ 0）**。只看「非空」会把文字描述"
      "误算成一条已登记靶（见下表 ①）；只填一列则是登记不完整（见下表 ②）。\n")
    A("| 文件 | 归属 | 表结构 | 行数 | 非空 | **数值合法（计入登记）** |")
    A("| --- | --- | --- | --- | --- | --- |")
    by_file = {}
    for r in P["registry"]:
        d = by_file.setdefault(r["file"], {"owner": r["owner"], "schema": r["schema"],
                                           "n": 0, "nonempty": 0, "ok": 0})
        d["n"] += 1
        d["nonempty"] += 1 if r["nonempty"] else 0
        d["ok"] += 1 if r["registered"] else 0
    for path in P["registry_paths"]:
        rel = os.path.relpath(path, P["root"]).replace("\\", "/")
        d = by_file.get(path)
        if d is None:
            A("| `%s` | — | _无 UFT-3 列或无数据行_ | 0 | 0 | **0** |" % rel)
        else:
            A("| `%s` | %s | %s | %d | %d | **%d** |"
              % (rel, d["owner"], d["schema"], d["n"], d["nonempty"], d["ok"]))
    errs = [r for r in P["registry"] if r["severity"] == "ERROR"]
    warns = [r for r in P["registry"] if r["severity"] == "WARN"]
    if errs:
        A("\n**① ERROR：内容非数值 / urel 为负（高危——会骗过「只看非空」的判定）**：\n")
        A("| 体系 / 层 | 主张 | prediction_value | prediction_urel | 判定 |")
        A("| --- | --- | --- | --- | --- |")
        for r in errs:
            A("| %s | `%s` | `%s` | `%s` | %s |"
              % (r["owner"], r["claim_id"], r["prediction_value"],
                 r["prediction_urel"] or "（空）", r["reason"]))
    if warns:
        A("\n**② WARN：登记不完整 / 精确性声明存疑（无法参与 χ²）**：\n")
        A("| 体系 / 层 | 主张 | prediction_value | prediction_urel | 判定 |")
        A("| --- | --- | --- | --- | --- |")
        for r in warns:
            A("| %s | `%s` | `%s` | `%s` | %s |"
              % (r["owner"], r["claim_id"], r["prediction_value"],
                 r["prediction_urel"] or "（空）", r["reason"]))
    A("\n> 合计：扫描 **%d** 个 claims.csv；数值合法登记条目 = **%d** 条。"
      "字段名取自 `claims_schema_升级.py` 的实际输出表头（14 列）。\n"
      % (len(P["registry_paths"]), sum(1 for r in P["registry"] if r["registered"])))
    A("\n## 五、判定清单（四态齐备）\n")
    A("| 编号 | 状态 | 内容 | 证据 / 出处 |")
    A("| --- | --- | --- | --- |")
    for f in P["findings"]:
        A("| `%s` | **%s** | %s | %s |" % (f["id"], f["state"], f["text"], f["evidence"]))
    if P.get("teeth"):
        A("\n## 六、牙齿（变异体 + 阳性对照）\n")
        A("| 项 | 结果 | 证据 |")
        A("| --- | --- | --- |")
        for t in P["teeth"]:
            A("| %s | **%s** | %s |" % (t["name"], "CAUGHT/CLEAN" if t["ok"] else "MISSED",
                                        t["detail"]))
    A("\n## 七、诚实边界与复跑\n")
    for line in P["honest_notes"]:
        A("- " + line)
    A("\n```powershell")
    A("cd openuft/04_公共成果/本项目_全维自洽与归一化/源码")
    A("& C:/Users/mo/AppData/Local/Programs/Python/Python38/python.exe -B 靶场卡方联合拟合_统计层与判决力读数.py")
    A("& C:/Users/mo/AppData/Local/Programs/Python/Python38/python.exe -B 靶场卡方联合拟合_统计层与判决力读数.py --teeth")
    A("```\n")
    return "\n".join(L) + "\n"


def main():
    t0 = time.time()
    teeth_on = "--teeth" in sys.argv
    up = load_upstream()
    entries = build_entries(up)
    targets, rows, joints = analyse(up, entries)
    readings = analyse_readings()
    registry, reg_paths = scan_registry(load_registry_checker())
    teeth = run_teeth(up) if teeth_on else []
    findings = build_findings(rows, joints, readings, registry, len(reg_paths))

    payload = {
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "mpmath_dps": mp.dps,
        "python": sys.version.split()[0],
        "root": ROOT,
        "caliber": {
            "chi2_crit_1dof_95": nstr(CHI2_CRIT_1, 12),
            "chi2_crit_source": "2*erfinv(0.95)^2（闭式，不硬编码）",
            "target_table_source": "源码/无量纲靶场审计.py（同一真源）",
            "dof_rule": "rank(J)（定理 I）；联合再做 Σ 秩扣减",
            "reused_discriminant": "V = (n_hit - n_free - n_anchor)/n_hit（上游 verdict_v）",
            "registry_rule_source": "源码/靶场登记列校验_写入侧门禁.py"
                                    "（登记列语义单一真源；本层委派，不自行解析）",
        },
        "entry_count": len(rows),
        "rows": rows,
        "joints": joints,
        "readings": readings,
        "registry": registry,
        "registry_paths": reg_paths,
        "findings": findings,
        "teeth": teeth,
        "honest_notes": [
            "本模块不会自己产生 L3：目标登记为 0 时读数必然是「不可判」。",
            "χ² ≈ 0 不等于证据（α_grav(e) ≡ (m_e/m_P)² 即反例：自洽、零判别力、V<0）。",
            "任意相关矩阵本轮不收，只收「独立」与「共模 profile」两种闭合式模式。",
            "σ_obs 为外部假设的条目只能判 BOUNDARY。",
            "合成对照条目不入任何台账，只用于仪器校准。",
        ],
    }
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "靶场卡方联合拟合.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    with open(os.path.join(OUT_DIR, "靶场卡方联合拟合.md"), "w", encoding="utf-8") as fh:
        fh.write(render_md(payload))

    print("=" * 78)
    print("靶场卡方联合拟合 · 统计层与判决力读数（dps=%d，Python %s）"
          % (mp.dps, sys.version.split()[0]))
    print("=" * 78)
    print("  χ²_crit(1, 0.95) = %s（闭式 2·erfinv(0.95)²）" % nstr(CHI2_CRIT_1, 12))
    print("-" * 78)
    print("  逐条目：")
    for r in rows:
        print("    [%-4s] %-22s χ²=%-12s p=%-12s 轴A=%-4s 轴B=%-10s %s"
              % (r["verdict"], r["entry_id"], r["chi2"], r["p"],
                 r["axis_a"], r["axis_b"], r["note"][:28]))
    print("-" * 78)
    print("  联合拟合：")
    for j in joints:
        print("    [%-4s] 组 %-8s 模式 %-20s χ²=%-12s ν=%-3d p=%s"
              % (j["verdict"], j["group"], j["mode"], j["chi2"], j["nu"],
                 fmt_p_str(j["p"])))
    print("-" * 78)
    print("  判决力上界读数：")
    for r in readings:
        print("    [%-4s] %-10s Δ_th/σ = %-12s 低 %s 个量级 | 需精度 %s %s"
              % (r["verdict"], r["id"], r["ratio"], r["orders_below"],
                 r["sigma_need"], r["sigma_unit"]))
    print("-" * 78)
    n_reg = sum(1 for r in registry if r["registered"])
    n_err = sum(1 for r in registry if r["severity"] == "ERROR")
    n_warn = sum(1 for r in registry if r["severity"] == "WARN")
    print("  UFT-3 登记看板（委派写入侧门禁·单一真源）：claims.csv %d 个文件；"
          "数值合法登记 %d 条；ERROR %d 条；WARN %d 条"
          % (len(reg_paths), n_reg, n_err, n_warn))
    print("-" * 78)
    state_cnt = {}
    for f in findings:
        state_cnt[f["state"]] = state_cnt.get(f["state"], 0) + 1
    print("  判定：总数 %d | " % len(findings)
          + " ".join("%s=%d" % (k, state_cnt.get(k, 0))
                     for k in ("PASS", "FAIL", "BOUNDARY", "INFO")))
    if teeth:
        n_ok = sum(1 for t in teeth if t["ok"])
        print("  牙齿：%d/%d %s" % (n_ok, len(teeth),
                                    "全部 CAUGHT/CLEAN" if n_ok == len(teeth) else "存在 MISSED"))
        for t in teeth:
            print("    %-6s %s | %s" % ("CAUGHT/CLEAN" if t["ok"] else "MISSED",
                                        t["name"], t["detail"]))
    print("-" * 78)
    print("  产出：数据/靶场卡方联合拟合.{json,md}  用时 %.2fs" % (time.time() - t0))
    exit_code = 0 if not teeth else (0 if all(t["ok"] for t in teeth) else 1)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
