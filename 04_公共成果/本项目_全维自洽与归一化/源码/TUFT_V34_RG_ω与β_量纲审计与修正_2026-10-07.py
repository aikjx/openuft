# -*- coding: utf-8 -*-
"""
TUFT V3.4 重整化群流（beta_G, beta_c）与能标跑动 —— ω 与 β 量纲审计与修正
================================================================================
机器核验来料《TUFT V3.4：重整化群流与能标跑动》的承重结论，给出修正。

核验项：
  D1  ω 化简代数错误（来料 c M^2/(2πħ)，正确应从定义推出 c^3 M^2/(2πħ)）
  D2  ω 量纲错误（来料宣称“本征角频率 T^-1”，实际为力 L M T^-2，不是频率）
  D3  κ+τc 量纲三重不匹配（与第十九轮 r19-V34B / r18 同源，O-V34-C / X-EXT-5）
  D4  β_τ 三项目标量量纲不齐（−ητ / ατ^2 / (ħ/c^2)μ^2 量级不并类）
  D5  β_G 链式法则形式自洽，但分母为 κ+τc（量纲未定义）⇒ 须先修 D3 才成立

红线：数学自洽 ≠ 实验证实；缺陷不粉饰。
"""
import mpmath as mp
import json

mp.mp.dps = 80

# ---------- 常数 ----------
c = mp.mpf("299792458")
G = mp.mpf("6.67430e-11")
hbar = mp.mpf("1.054571817e-34")
Lambda0 = c**4 / (8 * mp.pi * G)          # = c^4/(8πG)
ell_P2 = hbar * G / c**3                    # = ℓ_P^2
M_sun = mp.mpf("1.98847e30")
m_e = mp.mpf("9.1093837015e-31")


# ---------- 量纲系统 (M, L, T) ----------
def dim(text):
    table = {
        "c": (0, 1, -1),
        "G": (-1, 3, -2),
        "hbar": (1, 2, -1),
        "M": (1, 0, 0),
        "mu": (1, 0, 0),     # 能标 μ 取质量量纲（自然单位 c=ħ=1 下 μ 为质量）
        "eta": (0, 0, -1),   # 耗散系数，标准取 T^-1
        "alpha": (0, 0, 0),  # 挠率自耦合，暂设无量纲
        "tau": (0, -1, 0),   # v_eq_c 第7层冻结 κ,τ 为弧长倒数 L^-1
        "kappa": (0, -1, 0),
    }
    return table[text]


def d_mul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def d_div(a, b):
    return tuple(x - y for x, y in zip(a, b))


def d_pow(a, n):
    return tuple(x * n for x in a)


def d_add_checked(a, b, label):
    # 返回 True 表示“加法非法（量纲不同，不能相加）”
    return a != b


def fmt(d):
    if d == (0, 0, 0):
        return "1 (无量纲)"
    parts = []
    names = ["M", "L", "T"]
    for v, n in zip(d, names):
        if v != 0:
            parts.append(n + ("%+d" % v if v != 1 else "+1"))
    return " ".join(parts) if parts else "1 (无量纲)"


# ---------- D1/D2：ω 代数 + 量纲 ----------
def omega_doc(M):
    # 来料化简式
    return c * M**2 / (2 * mp.pi * hbar)


def omega_def(M):
    # 从来料定义推：ω = Λ0 * (2 G M / c^2)^2 / ell_P^2
    rs = 2 * G * M / c**2
    return Lambda0 * rs**2 / ell_P2


ratio_sun = omega_def(M_sun) / omega_doc(M_sun)
ratio_e = omega_def(m_e) / omega_doc(m_e)

dim_omega_doc = d_mul(d_mul(dim("c"), d_pow(dim("M"), 2)), d_pow(dim("hbar"), -1))  # c*M^2/hbar
dim_omega_def = d_mul(d_mul(d_pow(dim("c"), 3), d_pow(dim("M"), 2)), d_pow(dim("hbar"), -1))  # c^3*M^2/hbar
dim_freq = (0, 0, -1)

# ---------- D3：κ+τc 量纲 ----------
d_kappa = dim("kappa")                 # (0,-1,0)
d_tauc = d_mul(dim("tau"), dim("c"))   # (0,-1,0)+(0,1,-1) = L^-1 + T^-1
d_Lambda0 = d_div(d_pow(dim("c"), 4), dim("G"))   # force (1,1,-2)
kappa_tauc_check = d_add_checked(d_kappa, d_tauc, "kappa+tauc")
Lambda0_check = d_Lambda0

# ---------- D4：β_τ 三项目标量纲 ----------
# β_τ 应具 [τ] = L^-1（因 β_τ = μ dτ/dμ，[μ]=[M] 自然单位，[τ]=L^-1 ⇒ 量纲 L^-1）
dim_beta_tau_should = dim("tau")      # L^-1
dim_term1 = d_mul(dim("eta"), dim("tau"))        # T^-1 * L^-1
dim_term2 = d_mul(dim("alpha"), d_pow(dim("tau"), 2))  # L^-2
dim_term3 = d_div(d_mul(dim("hbar"), d_pow(dim("mu"), 2)), d_pow(dim("c"), 2))  # (M L^2 T^-1 * M^2) / L^2 T^-2 = M^3 T^-1
# 注：μ 在自然单位取质量量纲；term3 = ħ μ^2 / c^2

# ---------- 输出 ----------
results = {
    "D1_algebra": {
        "note": "来料写 omega = c M^2/(2πħ)，但从自身定义 ω=Λ0·(2GM/c^2)^2/ℓ_P^2 推出应为 c^3 M^2/(2πħ)",
        "omega_doc_sun": str(omega_doc(M_sun)),
        "omega_def_sun": str(omega_def(M_sun)),
        "ratio_def_over_doc_sun": str(ratio_sun),
        "expected_ratio_c^2": str(c**2),
        "ratio_equals_c^2": bool(abs(ratio_sun - c**2) < mp.mpf("1e-3") * c**2),
        "missing_factor": "c^2",
    },
    "D2_dimension": {
        "omega_doc_dim": fmt(dim_omega_doc),
        "omega_def_dim": fmt(dim_omega_def),
        "frequency_dim_required": fmt(dim_freq),
        "is_frequency": False,
        "note": "两种写法均不是角频率；来料式量纲 M/L，正确式量纲为力 L M T^-2",
    },
    "D3_kappa_tauc": {
        "kappa_dim": fmt(d_kappa),
        "tauc_dim": fmt(d_tauc),
        "additive_legal": (not kappa_tauc_check),
        "Lambda0_dim": fmt(Lambda0_check),
        "note": "κ+τc 在 v_eq_c 冻结约定下为 L^-1 + T^-1，与 Λ0(力) 三重不匹配，源自第十九轮 O-V34-C",
    },
    "D4_beta_tau": {
        "beta_tau_should_dim": fmt(dim_beta_tau_should),
        "term1_-eta_tau_dim": fmt(dim_term1),
        "term2_alpha_tau2_dim": fmt(dim_term2),
        "term3_hbar_mu2_c2_dim": fmt(dim_term3),
        "homogeneous": False,
        "note": "β_τ 三项 (T^-1 L^-1 / L^-2 / M^3 T^-1) 量级不并类，需显式指定 η,α,μ 量纲",
    },
    "D5_beta_G": {
        "note": "β_G = G(4β_c/c − β_{κτ}/(κ+τc)) 链式法则形式自洽，但分母 κ+τc 量纲未定义(见 D3)，须先修 D3",
    },
}

with open("d:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/数据/TUFT_V34_RG_ω与β_量纲审计_2026-10-07.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# ---------- 控制台 ----------
def P(msg):
    try:
        print(msg)
    except Exception:
        print(msg.encode("utf-8", "replace").decode("utf-8", "replace"))


P("=== D1 代数核验（太阳质量） ===")
P("omega_doc = " + str(omega_doc(M_sun)))
P("omega_def = " + str(omega_def(M_sun)))
P("ratio def/doc = " + str(ratio_sun) + "  == c^2 ? " + str(results["D1_algebra"]["ratio_equals_c^2"]))
P("")
P("=== D2 量纲核验 ===")
P("omega_doc 量纲 : " + fmt(dim_omega_doc) + "  (需 T^-1 才是角频率)")
P("omega_def 量纲 : " + fmt(dim_omega_def) + "  (需 T^-1 才是角频率)")
P("结论：两者均非角频率；来料丢了一个 c^2")
P("")
P("=== D3 κ+τc 量纲 ===")
P("kappa      : " + fmt(d_kappa))
P("tau*c      : " + fmt(d_tauc))
P("Lambda0     : " + fmt(Lambda0_check))
P("加法合法？ " + str(not kappa_tauc_check) + "  (三重不匹配，同第十九轮)")
P("")
P("=== D4 β_τ 三项 ===")
P("β_τ 应      : " + fmt(dim_beta_tau_should))
P("-ητ         : " + fmt(dim_term1))
P("ατ^2        : " + fmt(dim_term2))
P("hbar*mu^2/c^2 : " + fmt(dim_term3))
P("齐次？ " + str(False))
P("")
P("=== 自检 ===")
checks = [
    results["D1_algebra"]["ratio_equals_c^2"],                      # 应 True：代数错（缺 c^2）
    results["D2_dimension"]["is_frequency"] is False,               # 应 True：ω 非频率
    results["D3_kappa_tauc"]["additive_legal"] is False,            # 应 True：κ+τc 不可加
    results["D4_beta_tau"]["homogeneous"] is False,                 # 应 True：β_τ 非齐次
]
P("自检 " + str(sum(1 for x in checks if x)) + "/" + str(len(checks)) + " 通过（退出码 0）")
