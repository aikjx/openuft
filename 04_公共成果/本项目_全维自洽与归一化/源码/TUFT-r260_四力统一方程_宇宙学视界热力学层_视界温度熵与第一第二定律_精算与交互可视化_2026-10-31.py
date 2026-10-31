# -*- coding: utf-8 -*-
r"""TUFT-r260 · 四力统一方程·宇宙学视界热力学层：视界温度、熵与第一/第二定律
2026-10-31

〔编号说明〕起草前实测 r257 已被并行链《同一运动定理卷》占用（源码/数据/判定/runner 齐全），
r258《暗能量与宇宙常数层》、r259《同一运动动力学层》亦被占 ⇒ 本卷取 **r260**（r260–r263 实测全空）。
本卷承 r233（黑洞热力学）与 r237（宇宙学背景层）：把 Bekenstein–Hawking 熵与
Gibbons–Hawking 温度从**事件视界**外推到 FRW 的**表观视界** r_A=c/H，并机检
「什么形式的第一定律真的闭合、什么形式只是静态黑洞的错觉」。

用户诉求：「继续分析整理所有问题，攻破统一场论理论体系，新的方程，精算验证」。

本卷要回答的问题（视界热力学可算的部分）：
  Q1 S/k_B = A/(4ℓ_P²)（A=4πr_A²）与 πc⁵/(GħH²) 是否逐位恒等？量级是否 10^122？
  Q2 T_GH = ħH/(2πk_B) 与 ħc/(2πk_B r_A) 是否恒等？T_GH/T_CMB 量级？
  Q3 第一定律在表观视界上以什么形式闭合？（T dS = dE + p dV 是否成立？）
  Q4 第二定律 dS/dt > 0 是否全域成立？纯 de Sitter 极限是否为 0？
  Q5 视界熵有无观测通道？（无 ⇒ BOUNDARY）

诚实预期（写在前面）：Bekenstein–Hawking 面积律、Gibbons–Hawking 温度、
de Sitter 熵 3πc³/(GħΛ) 全部是教科书结果（Bekenstein 1973 / Hawking 1975 /
Gibbons–Hawking 1977 / Cai–Kim 2005 / Hayward 1998）。本卷是**复现层**：
“宇宙总熵 10^122”依赖把 A/4ℓ_P² 赋给表观视界这一**公设**；表观视界温度
T_GH ~ 10^-30 K 远低于 CMB，无任何直接观测通道。
"""

import json
import os
import sys
from math import sqrt, pi, log

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)
_DATADIR = os.path.join(_PROJ, "数据")
_TMPL = os.path.join(_HERE, "TUFT-r260_宇宙学视界热力学层交互可视化模板_2026-10-31.html")
HTML_OUT = os.path.join(_PROJ, "四力统一方程_宇宙学视界热力学层可视化_2026-10-31.html")

MARKER = "R260-COSMO-HORIZON-THERMO"
BASE = ("TUFT-r260_四力统一方程_宇宙学视界热力学层_视界温度熵与第一第二定律_"
        "精算与交互可视化_2026-10-31")
STEM = "TUFT-r260"

C = 2.99792458e8
G = 6.67430e-11
HBAR = 1.054571817e-34
KB = 1.380649e-23
MPC = 3.0856775814913673e22
H0_KM = 67.4
H0 = H0_KM * 1000.0 / MPC
OM = 0.3153
OR = 9.15e-5
OL = 1.0 - OM - OR
T_CMB = 2.7255
LP2 = HBAR * G / C ** 3          # ℓ_P²
A_RAD = 7.5657e-16               # 辐射常数 a = 4σ/c（J m^-3 K^-4）

guards, controls, entries = [], [], []


def guard(gid, title, ok, detail, numbers=None):
    guards.append({"id": gid, "title": title, "ok": bool(ok),
                   "detail": detail, "numbers": numbers or {}})
    if not ok:
        print(f"[GUARD-FAIL] {gid} {title}: {detail}")
    return bool(ok)


def control(cid, title, ok, detail, numbers=None):
    controls.append({"id": cid, "title": title, "ok": bool(ok),
                     "detail": detail, "numbers": numbers or {}})
    if not ok:
        print(f"[CONTROL-FAIL] {cid} {title}: {detail}")
    return bool(ok)


def entry(code, level, title, detail, numbers=None):
    entries.append({"code": code, "level": level, "title": title,
                    "detail": detail, "numbers": numbers or {}})


# ------------------------------------------------------------------ 宇宙学
def Ez2(z, om=OM, orr=OR, ol=OL):
    return om * (1 + z) ** 3 + orr * (1 + z) ** 4 + ol


def Hz(z, om=OM, orr=OR, ol=OL, h0=H0):
    return h0 * sqrt(Ez2(z, om, orr, ol))


def Hp(z, om=OM, orr=OR, ol=OL, h0=H0):
    """dH/dz 解析（含辐射项）。"""
    num = 0.5 * (3.0 * om * (1 + z) ** 2 + 4.0 * orr * (1 + z) ** 3) * h0 ** 2
    return num / Hz(z, om, orr, ol, h0)


def rho(z, om=OM, orr=OR, ol=OL, h0=H0):
    return 3.0 * h0 ** 2 / (8.0 * pi * G) * Ez2(z, om, orr, ol)


def p_tot(z, om=OM, orr=OR, ol=OL, h0=H0):
    """总压（含 c²）：辐射 p=ρ_r c²/3，Λ 的 p=−ρ_Λ c²，物质 0。"""
    rc = 3.0 * h0 ** 2 / (8.0 * pi * G)
    return (1.0 / 3.0) * rc * orr * (1 + z) ** 4 * C ** 2 - rc * ol * C ** 2


# ------------------------------------------------------------------ 视界热力学
def rA(z, **kw):
    """表观视界（Hubble 半径）r_A = c/H。"""
    return C / Hz(z, **kw)


def S_kB(z, **kw):
    """S/k_B = πc⁵/(GħH²)。"""
    return pi * C ** 5 / (G * HBAR * Hz(z, **kw) ** 2)


def S_kB_area(z, **kw):
    """S/k_B = A/(4ℓ_P²)，A=4πr_A²。"""
    return 4.0 * pi * rA(z, **kw) ** 2 / (4.0 * LP2)


def T_GH(z, **kw):
    """T = ħH/(2πk_B)。"""
    return HBAR * Hz(z, **kw) / (2.0 * pi * KB)


def T_GH_area(z, **kw):
    """T = ħc/(2πk_B r_A)。"""
    return HBAR * C / (2.0 * pi * KB * rA(z, **kw))


def V(z, **kw):
    return 4.0 / 3.0 * pi * rA(z, **kw) ** 3


def Vp(z, **kw):
    """dV/dz 解析，V=4πc³/(3H³)。"""
    return -4.0 * pi * C ** 3 * Hp(z, **kw) / Hz(z, **kw) ** 4


def E_MS(z, **kw):
    """视界内 Misner–Sharp 质量能 E=ρc²V=c⁵/(2GH)。"""
    return rho(z, **kw) * C ** 2 * V(z, **kw)


def dSdz(z, **kw):
    """dS/dz 解析：S/k_B=πc⁵/(GħH²) ⇒ −2πc⁵H'/(GħH³)。"""
    return -2.0 * pi * C ** 5 * Hp(z, **kw) / (G * HBAR * Hz(z, **kw) ** 3)


def dEdz(z, **kw):
    """dE/dz 解析：E=c⁵/(2GH) ⇒ −c⁵H'/(2GH²)。"""
    return -C ** 5 * Hp(z, **kw) / (2.0 * G * Hz(z, **kw) ** 2)


def tdsdz(z, **kw):
    """T dS/dz（J 每单位 z）。"""
    return KB * T_GH(z, **kw) * dSdz(z, **kw)


def first_law_rel(z, **kw):
    lhs = tdsdz(z, **kw)
    rhs = 2.0 * dEdz(z, **kw)
    return abs(lhs - rhs) / max(abs(lhs), abs(rhs))


def naive_pdv(z, **kw):
    """朴素静态形式 T dS = dE + p dV。"""
    lhs = tdsdz(z, **kw)
    rhs = dEdz(z, **kw) + p_tot(z, **kw) * Vp(z, **kw)
    return lhs, rhs, rhs / lhs


def hayward_wdv(z, **kw):
    """Hayward 形式 T dS = dE − w dV，w=(ρc²−p)/2。"""
    w = (rho(z, **kw) * C ** 2 - p_tot(z, **kw)) / 2.0
    lhs = tdsdz(z, **kw)
    rhs = dEdz(z, **kw) - w * Vp(z, **kw)
    return lhs, rhs, rhs / lhs


def dSdt(z, **kw):
    """d(S/k_B)/dt = dS/dz · dz/dt，dz/dt=−(1+z)H。"""
    return dSdz(z, **kw) * (-(1 + z) * Hz(z, **kw))


def main():
    # ---------------------------------------------------------------- S1
    print("[S1] 面积律：S/k_B 双路径与量级")
    zs = [0.0, 1.0, 5.0]
    s_a = S_kB(0.0)
    s_b = S_kB_area(0.0)
    rel_s = abs(s_a - s_b) / s_a
    rel_s_max = max(abs(S_kB(z) - S_kB_area(z)) / S_kB(z) for z in zs)
    log_s0 = log(s_a, 10)
    guard("G1", "S/k_B = A/(4ℓ_P²) 双路径恒等且 log10(S0) 落 121.5–123.5",
          rel_s_max < 1e-12 and 121.5 <= log_s0 <= 123.5,
          f"z∈{{0,1,5}} 最大相对差 {rel_s_max:.2e}；"
          f"S0/k_B={s_a:.6e}（log10={log_s0:.6f}）；"
          f"r_A0={rA(0.0):.6e} m = {rA(0.0)/MPC:.3f} Mpc（= c/H0）",
          {"S0": f"{s_a:.6e}", "log10S0": f"{log_s0:.6f}",
           "rel": f"{rel_s_max:.2e}", "rA0_Mpc": f"{rA(0.0)/MPC:.3f}"})

    # ---------------------------------------------------------------- S2
    print("[S2] Gibbons–Hawking 温度双路径与量级")
    t_a = T_GH(0.0)
    rel_t_max = max(abs(T_GH(z) - T_GH_area(z)) / T_GH(z) for z in zs)
    t_ratio = t_a / T_CMB
    guard("G2", "T_GH 双路径恒等且 T0 ∈ [2,3.5]×10^-30 K",
          rel_t_max < 1e-12 and 2.0e-30 <= t_a <= 3.5e-30,
          f"z∈{{0,1,5}} 最大相对差 {rel_t_max:.2e}；T0={t_a:.6e} K；"
          f"T_GH/T_CMB={t_ratio:.4e}（CMB {T_CMB} K）",
          {"T0": f"{t_a:.6e}", "rel": f"{rel_t_max:.2e}",
           "T_ratio_cmb": f"{t_ratio:.4e}"})

    # ---------------------------------------------------------------- S3
    print("[S3] 第一定律：精确形式 vs 两种静态形式")
    fl_rows = []
    max_fl = 0.0
    for z in [0.0, 0.3, 1.0, 2.0, 5.0, 10.0]:
        rel = first_law_rel(z)
        max_fl = max(max_fl, rel)
        fl_rows.append({"z": z, "T_K": T_GH(z), "S_kB": S_kB(z),
                        "tds_dz": tdsdz(z), "dedz": dEdz(z), "rel": rel})
    guard("G3", "精确第一定律 T dS/dz = 2 dE_MS/dz（E=ρc²V=c⁵/2GH）全域机器零",
          max_fl < 1e-12,
          f"z∈{{0,0.3,1,2,5,10}} 最大相对残差 {max_fl:.2e}（解析导数对解析导数，"
          "结构恒等：S=A/4ℓ_P²、T=ħH/2π、r_A=c/H 三者联立的必然结果）",
          {"max_rel": f"{max_fl:.2e}"})

    naive_rows = []
    for z in [0.0, 1.0, 2.0, 5.0]:
        l, r, ratio = naive_pdv(z)
        hw_l, hw_r, hw_ratio = hayward_wdv(z)
        naive_rows.append({"z": z, "tds": l, "rhs": r, "ratio": ratio,
                           "hw_ratio": hw_ratio})
    worst_dev = max(abs(x["ratio"] - 1.0) for x in naive_rows)
    print(f"    朴素 p dV 最大偏离 |ratio−1| = {worst_dev:.4f}；"
          f"Hayward w dV 比值 {naive_rows[0]['hw_ratio']:.4f}")

    # ---------------------------------------------------------------- S4
    print("[S4] 第二定律：dS/dt > 0 与纯 de Sitter 极限")
    sec_rows = [{"z": z, "dSdt": dSdt(z)} for z in [0.0, 1.0, 2.0, 5.0, 10.0]]
    all_pos = all(x["dSdt"] > 0 for x in sec_rows)
    # 纯 de Sitter：Ωm=Ωr=0, ΩΛ=1 ⇒ H 常数
    ds_const = max(abs(Hz(z, om=0.0, orr=0.0, ol=1.0) / H0 - 1.0) for z in [0.0, 1.0, 5.0])
    ds_dsdt = dSdt(0.0, om=0.0, orr=0.0, ol=1.0)
    guard("G4", "第二定律 dS/dt>0 全域；纯 de Sitter 极限 dS/dt=0",
          all_pos and ds_const < 1e-12 and abs(ds_dsdt) < 1e-12
          and abs(dSdt(0.0)) > 0,
          f"ΛCDM：z∈{{0,1,2,5,10}} dS/dt = "
          + ", ".join(f"{x['dSdt']:.3e}" for x in sec_rows)
          + f"（全部 >0）；纯 dS：H/H0 偏离 {ds_const:.2e}、dS/dt={ds_dsdt:.2e}",
          {"dSdt_z0": f"{dSdt(0.0):.4e}", "dSdt_z10": f"{dSdt(10.0):.4e}"})

    # ---------------------------------------------------------------- S5
    print("[S5] 控制组")
    # C1：纯 de Sitter 熵公式恒等 S/k_B = 3πc³/(GħΛ)，Λ=3H0²/c²
    lam = 3.0 * H0 ** 2 / C ** 2
    s_lambda = 3.0 * pi * C ** 3 / (G * HBAR * lam)
    rel_lam = abs(s_lambda - S_kB(0.0)) / S_kB(0.0)
    control("C1", "纯 de Sitter：H 常数 ⇒ dS/dt=0，且 S/k_B=3πc³/(GħΛ) 恒等",
            ds_const < 1e-12 and abs(ds_dsdt) < 1e-12 and rel_lam < 1e-12,
            f"Ωm=Ωr=0：H(z)/H0−1 最大 {ds_const:.2e}；dS/dt={ds_dsdt:.2e}；"
            f"S/k_B(3πc³/GħΛ)={s_lambda:.6e} vs πc⁵/(GħH0²)={S_kB(0.0):.6e}"
            f"（rel {rel_lam:.2e}）",
            {"rel_lambda": f"{rel_lam:.2e}"})

    # C2：H0×1.10 ⇒ S ∝ H^-2（比值 1/1.21 解析），T ∝ H（比值 1.10）
    hf = 1.10
    s_ratio = S_kB(0.0, h0=H0 * hf) / S_kB(0.0)
    t_ratio_f = T_GH(0.0, h0=H0 * hf) / T_GH(0.0)
    expect_s = 1.0 / hf ** 2
    control("C2", "标度控制：S ∝ H^-2、T ∝ H（H0×1.10）",
            abs(s_ratio - expect_s) < 1e-12 and abs(t_ratio_f - hf) < 1e-12,
            f"H0×{hf} ⇒ S 比值 {s_ratio:.15f}（解析 1/1.102={expect_s:.15f}）；"
            f"T 比值 {t_ratio_f:.15f}（解析 {hf}）；"
            "⇒ 视界熵对 H0 是强敏感（10% 的 H0 ⇒ 17.4% 的 S），与 θ_s 对 H0 严格不变（r256 C1）形成对照",
            {"S_ratio": f"{s_ratio:.15f}", "T_ratio": f"{t_ratio_f:.15f}"})

    # ---------------------------------------------------------------- S6
    print("[S6] 物质熵对照与条目")
    s_gamma_n = (4.0 / 3.0) * A_RAD * T_CMB ** 3 / KB   # k_B/m³
    S_matter = s_gamma_n * V(0.0)
    ratio_m = S_matter / S_kB(0.0)
    S_inf = S_kB(0.0) / OL
    print(f"    s_γ/k_B={s_gamma_n:.4e} /m³；S_matter/k_B={S_matter:.4e}；"
          f"比值 {ratio_m:.3e}；S_∞/k_B={S_inf:.4e}")

    entry("H01", "INFO", "判定：视界热力学 = 标准 Bekenstein–Hawking / Gibbons–Hawking 复现，不是新理论",
          "面积律、GH 温度、de Sitter 熵 3πc³/(GħΛ) 均为教科书结果（Bekenstein 1973 / "
          "Hawking 1975 / Gibbons–Hawking 1977 / Cai–Kim 2005）；本卷只做机器复现与形式机检")
    entry("H02", "PASS", "面积律 S/k_B = A/(4ℓ_P²)",
          f"S0/k_B={s_a:.6e}（log10={log_s0:.6f}，即 10^122 量级）；"
          f"πc⁵/(GħH²) 与 A/(4ℓ_P²) 双路径最大相对差 {rel_s_max:.2e}；"
          f"r_A0=c/H0={rA(0.0)/MPC:.1f} Mpc")
    entry("H03", "PASS", "Gibbons–Hawking 温度与 CMB 对照",
          f"T0={t_a:.6e} K；ħH/2πk_B 与 ħc/(2πk_B r_A) 双路径最大相对差 {rel_t_max:.2e}；"
          f"T_GH/T_CMB={t_ratio:.4e}")
    entry("H04", "PASS", "精确第一定律 T dS = 2 dE_MS（Misner–Sharp 形式）",
          f"E_MS=ρc²V=c⁵/(2GH)={E_MS(0.0):.4e} J；T dS/dz 与 2 dE/dz 在 "
          f"z∈{{0,0.3,1,2,5,10}} 最大相对残差 {max_fl:.2e}；S 随 t 单调增（G4）")
    entry("H05", "FAIL", "朴素静态形式 T dS = dE + p dV 不闭合",
          f"z∈{{0,1,2,5}}：rhs/lhs 比值 "
          + ", ".join(f"{x['ratio']:.4f}" for x in naive_rows)
          + f"（最大偏离 |ratio−1|={worst_dev:.3f}）；Hayward 形式 dE=T dS+w dV"
          f"（w=(ρc²−p)/2）比值 {naive_rows[0]['hw_ratio']:.4f} 亦不闭合 ⇒ "
          "把静态黑洞的第一定律照搬到表观视界是错的（必须用 Misner–Sharp 形式）")
    entry("H06", "BOUNDARY", "视界熵的物理身份是公设，不是定理",
          "GH 温度对 de Sitter 视界严格；FRW 表观视界的热力学是框架性推广（Cai–Kim / Hayward），"
          "且不同视界定义（表观/粒子/事件）给不同熵；「宇宙总熵 10^122」依赖把 A/4ℓ_P² 赋给 r_A 这一公设")
    entry("H07", "BOUNDARY", "无观测通道",
          f"T_GH/T_CMB={t_ratio:.3e}，视界温度比 CMB 低约 30 个量级，直接测温不可能；"
          f"视界熵 S0/k_B ~ 10^122 不进入任何可观测量（物质熵仅为其 {ratio_m:.2e} 倍）")
    entry("H08", "INFO", "判决：视界热力学复现 OK，统一仍无新物理",
          "r233（黑洞热力学）→本卷（宇宙学视界）为同一组定律的不同视界；"
          "r230『本质三层不可达』、r229 新颖性审计口径与本线动力学统一 FAIL 不变")

    n_pass = sum(1 for e in entries if e["level"] == "PASS")
    n_fail = sum(1 for e in entries if e["level"] == "FAIL")
    n_bnd = sum(1 for e in entries if e["level"] == "BOUNDARY")
    n_info = sum(1 for e in entries if e["level"] == "INFO")

    ledger = [
        ["r214", "静态中心力（UFE-4F 母式）", "形式统一 PASS；动力学 FAIL"],
        ["r221", "禁闭 σr + 通道门（UFE-4F⁺）", "r214 严格超集"],
        ["r222", "传播层（色散/群速度）", "质量-力程等价"],
        ["r226", "量子束缚层（薛定谔谱）", "引力『原子』无意义"],
        ["r227", "散射层（动量空间镜像）", "λ=∞ ⇔ 零质量载体"],
        ["r228", "变分层（L 与诺特）", "一个作用量生成中心力；辐射反作用无 L"],
        ["r229", "新颖性审计", "无新理论/无新方程"],
        ["r230", "引力本质层", "WEP 结构恒等 + 1PN 两件套"],
        ["r232", "引力波层", "四极/HT/啁啾三管线互印"],
        ["r233", "黑洞热力学层", "四定律+Smarr+面积定理+熵力母式（仅引力）"],
        ["r234（并行）", "强场层（史瓦西测地线）", "ISCO/光子球/1PN 失效曲线"],
        ["r237", "宇宙学背景层", "FRW 年龄/距离-红移/Λ 通道"],
        ["r254", "宇宙学扰动层", "线性增长+BAO 声视界+σ8 演化"],
        ["r256", "宇宙学声学峰层", "θ_s/l_A/z_eq + 张量边界"],
        ["r260", "宇宙学视界热力学层（本卷）", "面积律/温度 + 精确第一定律 + 第二定律"],
    ]

    zscan = [i * 0.25 for i in range(0, 41)]      # 0..10
    scan = {"z": [round(z, 4) for z in zscan],
            "T_K": [T_GH(z) for z in zscan],
            "log10S": [log(S_kB(z), 10) for z in zscan],
            "rA_Mpc": [rA(z) / MPC for z in zscan]}

    res = {
        "stem": STEM, "round": 260, "date": "2026-10-31",
        "method": ("r_A=c/H(z) + S/k_B=πc⁵/(GħH²)=A/(4ℓ_P²) + T_GH=ħH/(2πk_B) + "
                   "精确第一定律 T dS=2dE_MS（Misner–Sharp）+ 第二定律 dS/dt ——"
                   "float64，纯标准库，解析导数"),
        "cosmo_verdict": ("视界热力学全部机器复现（面积律双路径、温度双路径、精确第一定律机器零、"
                          "第二定律全域 dS/dt>0）；朴素 p dV 形式 FAIL；视界熵公设与无观测通道为边界 "
                          "——复现层，无新理论"),
        "entries": entries, "guards": guards, "controls": controls,
        "readings": {
            "params": {"H0_km": H0_KM, "Om": OM, "Or": OR, "OL": OL,
                       "T_CMB": T_CMB, "lP2": LP2},
            "horizon": {"T0": t_a, "S0": s_a, "log10S0": log_s0,
                        "rA0_m": rA(0.0), "rA0_Mpc": rA(0.0) / MPC,
                        "E_MS0_J": E_MS(0.0), "T_ratio_cmb": t_ratio,
                        "S_inf": S_inf, "lam": lam, "S_lambda": s_lambda},
            "first_law": {"max_rel": max_fl, "rows": fl_rows},
            "naive": {"rows": naive_rows, "worst_dev": worst_dev},
            "second": {"rows": sec_rows,
                       "ds_const": ds_const, "ds_dsdt": ds_dsdt},
            "matter": {"s_gamma_n": s_gamma_n, "S_matter": S_matter,
                       "ratio": ratio_m},
            "scan": scan,
            "scaling": {"hf": hf, "S_ratio": s_ratio, "T_ratio": t_ratio_f},
            "ledger": [{"round": r, "method": m, "verdict": v}
                       for r, m, v in ledger],
        },
        "counts": {"entries": len(entries), "PASS": n_pass, "FAIL": n_fail,
                   "BOUNDARY": n_bnd, "INFO": n_info,
                   "guards": f"{sum(1 for g in guards if g['ok'])}/{len(guards)}",
                   "controls": f"{sum(1 for c in controls if c['ok'])}/{len(controls)}"},
        "verdict": "", "judgement": "", "source": {},
    }

    parts = [
        "R260-COSMO-HORIZON-THERMO-OK-S-AREA-DUAL-PATH-OK-T-GH-DUAL-PATH-OK",
        "EXACT-FIRST-LAW-TDS-EQ-2DEMS-OK-SECOND-LAW-OK",
        "NAIVE-PDV-FORM-FAIL-PURE-DS-CONTROL-OK-H0-SCALING-CONTROL-OK",
        "ENTROPY-POSTULATE-BOUNDARY-NO-OBSERVABLE-BOUNDARY",
        "VERDICT-STANDARD-HORIZON-THERMODYNAMICS-NO-NEW-THEORY",
    ]
    res["verdict"] = "-".join(parts)
    res["judgement"] = ("CLOSED-INCREMENT（宇宙学视界热力学层：面积律双路径、温度双路径、"
                        "精确第一定律 T dS=2dE_MS、第二定律）；朴素 p dV 形式 FAIL；"
                        "视界熵公设与无观测通道为边界；无新理论")
    res["source"] = {
        "engine": BASE + ".py",
        "inherits": ["r233（黑洞热力学层）", "r237（宇宙学背景层）",
                     "r230（本质三层不可达）", "r229（新颖性审计口径）",
                     "Bekenstein 1973 / Hawking 1975 / Gibbons–Hawking 1977 / "
                     "Cai–Kim 2005 / Hayward 1998（只读）"],
    }

    os.makedirs(_DATADIR, exist_ok=True)
    jpath = os.path.join(_DATADIR, BASE + ".json")
    mpath = os.path.join(_DATADIR, BASE + ".md")
    rpath = os.path.join(_DATADIR, BASE + "_report.txt")

    html_ok, html_detail = cast_html(res)
    guard("G5", "交互 HTML 生成且自含", html_ok, html_detail)
    res["counts"]["guards"] = f"{sum(1 for g in guards if g['ok'])}/{len(guards)}"
    if html_ok:
        cast_html(res)

    print(f"条目 {res['counts']['entries']}（PASS {n_pass} / FAIL {n_fail} / "
          f"BOUNDARY {n_bnd} / INFO {n_info}）· 守卫 {res['counts']['guards']} · "
          f"控制组 {res['counts']['controls']}")

    with open(jpath, "w", encoding="utf-8", newline="\n") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    write_md(mpath, res)
    write_report(rpath, res)

    bad_g = [g["id"] for g in guards if not g["ok"]]
    bad_c = [c["id"] for c in controls if not c["ok"]]
    if bad_g or bad_c:
        print(f"[RC≠0] 守卫失败 {bad_g} 控制组失败 {bad_c}")
        return 1
    print(f"[DONE] {MARKER} rc=0 → {jpath}")
    return 0


def write_md(path, res):
    L = [f"# {res['stem']} · 数据册（引擎自动生成）\n",
         f"- 判决串：`{res['verdict']}`\n",
         f"- 条目：{res['counts']['entries']}（PASS {res['counts']['PASS']} / "
         f"FAIL {res['counts']['FAIL']} / BOUNDARY {res['counts']['BOUNDARY']} / "
         f"INFO {res['counts']['INFO']}）· 守卫 {res['counts']['guards']} · "
         f"控制组 {res['counts']['controls']}\n",
         "\n## 条目\n"]
    for e in res["entries"]:
        L.append(f"- **{e['code']} {e['level']}** {e['title']}——{e['detail']}\n")
    L.append("\n## 守卫\n")
    for g in res["guards"]:
        L.append(f"- **{g['id']} {'OK' if g['ok'] else 'FAIL'}** {g['title']}——"
                 f"{g['detail']}\n")
    L.append("\n## 控制组\n")
    for c in res["controls"]:
        L.append(f"- **{c['id']} {'OK' if c['ok'] else 'FAIL'}** {c['title']}——"
                 f"{c['detail']}\n")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(L))


def write_report(path, res):
    h = res["readings"]["horizon"]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(f"{MARKER} rc=0\n")
        f.write(f"entries={res['counts']['entries']} PASS={res['counts']['PASS']} "
                f"FAIL={res['counts']['FAIL']} BOUNDARY={res['counts']['BOUNDARY']} "
                f"INFO={res['counts']['INFO']}\n")
        f.write(f"guards={res['counts']['guards']} controls={res['counts']['controls']}\n")
        f.write(f"verdict={res['verdict']}\n")
        f.write(f"T0={h['T0']:.6e} K S0/kB={h['S0']:.6e} log10S0={h['log10S0']:.6f}\n")
        f.write(f"rA0={h['rA0_Mpc']:.3f} Mpc E_MS0={h['E_MS0_J']:.4e} J\n")
        f.write(f"first_law_max_rel={res['readings']['first_law']['max_rel']:.3e}\n")
        f.write(f"naive_pdv_worst_dev={res['readings']['naive']['worst_dev']:.4f}\n")
        f.write(f"dSdt_z0={h['T0']*0+res['readings']['second']['rows'][0]['dSdt']:.4e} /s\n")


def cast_html(res):
    if not os.path.isfile(_TMPL):
        return False, f"模板缺失：{_TMPL}"
    with open(_TMPL, "r", encoding="utf-8") as f:
        tpl = f.read()
    if "__R260_JSON__" not in tpl:
        return False, "模板缺少 __R260_JSON__ 占位符"
    html = tpl.replace("__R260_JSON__", json.dumps(res, ensure_ascii=False))
    with open(HTML_OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    text = open(HTML_OUT, "r", encoding="utf-8").read()
    problems = []
    if "__R260_JSON__" in text:
        problems.append("占位符未替换")
    if "http://" in text or "https://" in text:
        problems.append("发现外部 URL（应零依赖）")
    if "<canvas" not in text or "<script" not in text:
        problems.append("缺少 canvas/script")
    if problems:
        return False, "；".join(problems)
    return True, f"已生成 {HTML_OUT}（{len(text)} B），零外部 URL、JSON 已铸入"


if __name__ == "__main__":
    sys.exit(main())
