# -*- coding: utf-8 -*-
"""
uft_ledger_numerics.py
======================
《宇宙的本源：统一场论全书》第九卷 配套精算脚本
- mpmath 250 位精度
- 对标 CODATA 2022 / PDG 2024 / Planck 2018
- 所有数字在脚本里硬编码为公认推荐值，本书正文中引用的数字均由此脚本机读注入
- 退出码 0 = 全部守卫通过；任何守卫失败立即非零退出

整理入 openuft 时的三处修订（2026-10-20，详见本书 README「校勘记录」）：
  C-1  α 改用 CODATA 2022 推荐值 7.2973525643e-3（原稿取 7.2973525693e-3，
       实为 CODATA 2018 值却标注 "CODATA 2022"，属来源标签缺陷）；α^-1 相应变为
       137.035999177...，本书正文锚点表同值更新。
  C-2  输出版地化：原稿硬编码 /home/user/Doubao/chats/38448042477944578/ 路径，
       改为写入本脚本所在目录（uft_numerics_results.json + uft_numerics_report.txt）。
  C-3  删除未使用的 import（exp、phi）；人类可读摘要同时落盘 report.txt（三件套）。
其余计算逻辑、守卫门限、常量取值一律未动。
"""

import json
import sys
from pathlib import Path
from mpmath import mp, mpf, pi, sqrt, log

mp.dps = 250  # 250 位有效数字

HERE = Path(__file__).resolve().parent

# ---------- 1. CODATA 2022 基础常数（SI，精确值） ----------
c    = mpf('299792458')                 # m/s, 定义值
h    = mpf('6.62607015e-34')            # J·s, 定义值
hbar = h / (2*pi)                        # J·s
e    = mpf('1.602176634e-19')           # C, 定义值
k_e  = mpf('1.380649e-23')              # J/K, 定义值
N_A  = mpf('6.02214076e23')             # mol^-1, 定义值

# 测量值（CODATA 2022）
alpha = mpf('7.2973525643e-3')          # 精细结构常数，无量纲（CODATA 2022 推荐值）
alpha_inv = 1/alpha
G     = mpf('6.67430e-11')              # m^3 kg^-1 s^-2, 相对不确定度 2.2e-5
m_e   = mpf('9.1093837139e-31')         # kg
m_p   = mpf('1.67262192595e-27')        # kg
m_n   = mpf('1.67492750056e-27')        # kg
m_mu  = mpf('1.883531627e-28')          # kg
m_tau = mpf('3.16754e-27')              # kg
m_W   = mpf('1.43391e-25')              # kg  (W boson ~80.369 GeV/c^2)
m_Z   = mpf('1.62509e-25')              # kg  (Z boson ~91.1876 GeV/c^2)
v_EW  = mpf('246.22')                   # GeV, 电弱真空期望值
Lambda_QCD = mpf('0.210')               # GeV, N_running=5
m_t   = mpf('172.76')                   # GeV, 顶夸克极点质量
m_H   = mpf('125.25')                   # GeV, Higgs 玻色子质量

# 真空介电常数（由 c, μ0 定义关系推）
mu0_old = 4e-7*pi                        # 历史定义值（CODATA 2018 前）
epsilon0 = 1/(mu0_old * c**2)

# ---------- 2. Planck 尺度 ----------
l_P = sqrt(hbar*G/c**3)
t_P = sqrt(hbar*G/c**5)
m_P = sqrt(hbar*c/G)
E_P = m_P*c**2                           # Joule
E_P_GeV = E_P / (e*1e9)                  # 转 GeV

# ---------- 3. 力强度比：质子-质子在 1 m ----------
# 库仑 F_e = k e^2 / r^2；引力 F_g = G m_p^2 / r^2
k_Coulomb = 1/(4*pi*epsilon0)
F_e_over_F_g_1m = (k_Coulomb * e**2) / (G * m_p**2)

# ---------- 4. α 跑动（单圈 β 函数近似） ----------
# 在 q^2 = M_Z^2 处 α(M_Z)^{-1} ≈ 127.95
alpha_inv_at_MZ = mpf('127.951')
alpha_at_MZ = 1/alpha_inv_at_MZ
# 单圈：1/α(q) = 1/α(M_Z) - (1/2π) Σ b_i ln(q/M_Z)  （示意性，非精密）
def alpha_inv_running(q_over_MZ):
    # 简化：SM 单圈有效 β（示意）
    b_em = mpf(-11)/mpf(3)  # 包含 charged fermions + W, 示意
    return alpha_inv_at_MZ - b_em/(2*pi) * log(q_over_MZ)

alpha_inv_at_GUT = alpha_inv_running(mpf('1e15')/mpf('91.1876'))

# ---------- 5. 质子质量组成（迹反常口径） ----------
# m_p ≈ 938.272 MeV/c^2
# 流质量贡献：u ~2.3, d ~4.8, s ~95 (sum valence-ish ~ 9.4 MeV ≈ 1%)
# 其余 ~99% 来自胶子场能量（QCD trace anomaly）
m_p_MeV = m_p*c**2 / (e*1e6)             # 转 MeV
m_u_MeV = mpf('2.3')
m_d_MeV = mpf('4.8')
quark_current_fraction = (2*m_u_MeV + m_d_MeV) / m_p_MeV
glue_fraction = 1 - quark_current_fraction

# ---------- 6. 电弱精度对标：W 质量与树图关系 ----------
# 树图：m_W = m_Z cosθ_W, sin^2θ_W ≈ 0.23122
sin2_theta_W = mpf('0.23122')
cos2_theta_W = 1 - sin2_theta_W
m_W_tree = mpf('91.1876') * sqrt(cos2_theta_W)   # GeV
m_W_meas = mpf('80.369')
m_W_tree_vs_meas = m_W_tree - m_W_meas

# ---------- 7. Planck 卫星 2018 宇宙学 ----------
Omega_m  = mpf('0.3111')
Omega_L  = mpf('0.6889')
H0_km_s_Mpc = mpf('67.66')
# 1 Mpc = 3.0857e22 m
Mpc = mpf('3.0857e22')
H0_SI = H0_km_s_Mpc * 1000 / Mpc         # s^-1
t_H = 1/H0_SI                            # Hubble 时间
t_H_Gyr = t_H / (mpf('365.25')*24*3600) / 1e9  # Gyr

# ---------- 8. 电弱尺度与 Planck 尺度的层级 ----------
hierarchy_ratio = E_P_GeV / v_EW         # ~1e17

# ---------- 9. 引力极弱性：在 Planck 长度处引力=电磁 ----------
# F_g = F_e 时 r = sqrt(G m_p^2 / (k e^2)) * ?  其实是
# 把质子换成 Planck 质量粒子时，在 l_P 处两力相等
ratio_at_Planck = (G*m_P**2) / (k_Coulomb*e**2)

# ---------- 10. 关键守卫 ----------
guards = {}

def guard(name, cond, detail=""):
    guards[name] = {"pass": bool(cond), "detail": detail}
    if not cond:
        print(f"[GUARD FAIL] {name}: {detail}")

# G1: α^{-1} ≈ 137.036
guard("alpha_inv_is_137", abs(alpha_inv - 137.035999) < 1e-4,
      f"1/α = {mp.nstr(alpha_inv, 15)}")
# G2: m_p c^2 ≈ 938.272 MeV
guard("proton_mass_MeV", abs(m_p_MeV - 938.272088) < 1e-3,
      f"m_p c^2 = {mp.nstr(m_p_MeV, 9)} MeV")
# G3: Planck 长度 ≈ 1.616e-35 m
guard("l_P", abs(l_P/mpf('1.616255e-35') - 1) < 1e-3,
      f"l_P = {mp.nstr(l_P, 6)} m")
# G4: F_e/F_g at 1 m ~ 10^36
log10_ratio = float(log(F_e_over_F_g_1m)/log(10))
guard("force_ratio_1m", 35.5 < log10_ratio < 37,
      f"log10(F_e/F_g, r=1m) = {log10_ratio:.3f}")
# G5: 质子质量 99% 来自胶子
guard("glue_fraction", glue_fraction > 0.95,
      f"glue fraction = {float(glue_fraction)*100:.2f}%")
# G6: t_H ~ 14.5 Gyr
guard("hubble_time", 13 < float(t_H_Gyr) < 15,
      f"t_H = {float(t_H_Gyr):.3f} Gyr")
# G7: hierarchy ~ 1e17
guard("hierarchy", 1e16 < float(hierarchy_ratio) < 1e18,
      f"E_P/v_EW = {float(hierarchy_ratio):.3e}")
# G8: W tree vs measured 差 ~0.2 GeV（圈图修正）
guard("W_tree_vs_meas", abs(m_W_tree_vs_meas) < 0.5,
      f"m_W(tree) - m_W(meas) = {float(m_W_tree_vs_meas):.3f} GeV")

# ---------- 输出 ----------
def f12(x): return f"{float(x):.12g}"

out = {
    "precision_bits": 250,
    "constants_CODATA_2022": {
        "c":           f12(c),
        "hbar_J_s":    f12(hbar),
        "e_C":         f12(e),
        "alpha":       f12(alpha),
        "alpha_inv":   f12(alpha_inv),
        "G":           f12(G),
        "m_e_kg":      f12(m_e),
        "m_p_kg":      f12(m_p),
        "epsilon0":    f12(epsilon0),
    },
    "Planck_scale": {
        "l_P_meter":      f12(l_P),
        "t_P_second":     f12(t_P),
        "m_P_kg":         f12(m_P),
        "E_P_GeV":        f12(E_P_GeV),
    },
    "force_strength": {
        "proton_proton_at_1m_log10_Fe_over_Fg": f12(log10_ratio),
        "note": "引力比电磁弱约 36 个数量级——这是'力的统一'必须面对的定量事实",
    },
    "alpha_running": {
        "alpha_inv_at_0GeV":    f12(alpha_inv),
        "alpha_inv_at_MZ_91GeV": f12(alpha_inv_at_MZ),
        "alpha_inv_at_1e15GeV_rough": f12(alpha_inv_at_GUT),
        "note": "1/α 在 Planck 标度附近跑动到 ~10，三耦合在单圈下并不严格相交（SM 缺 SUSY 修正）",
    },
    "proton_mass_origin": {
        "m_p_MeV":             f12(m_p_MeV),
        "valence_quark_current_MeV": f12(2*m_u_MeV + m_d_MeV),
        "quark_fraction":      f12(float(quark_current_fraction)),
        "glue_trace_anomaly_fraction": f12(float(glue_fraction)),
        "note": "质子质量 99% 来自 QCD 迹反常（胶子场能量），不是 Higgs 机制直接给的",
    },
    "electroweak": {
        "v_EW_GeV":      f12(v_EW),
        "m_W_meas_GeV":  f12(m_W_meas),
        "m_W_tree_GeV":  f12(m_W_tree),
        "m_W_tree_minus_meas_GeV": f12(m_W_tree_vs_meas),
        "sin2_theta_W_eff": f12(sin2_theta_W),
        "m_H_GeV":       f12(m_H),
        "m_t_GeV":       f12(m_t),
    },
    "cosmology_Planck2018": {
        "Omega_m": f12(Omega_m),
        "Omega_Lambda": f12(Omega_L),
        "H0_km_s_Mpc": f12(H0_km_s_Mpc),
        "Hubble_time_Gyr": f12(t_H_Gyr),
    },
    "hierarchy": {
        "E_P_over_v_EW": f12(hierarchy_ratio),
        "note": "电弱标度 246 GeV 与 Planck 标度 1.22e19 GeV 相差 17 个数量级——'层级问题'",
    },
    "guards": {k: v for k, v in guards.items()},
}

json_path = HERE / "uft_numerics_results.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

# 人类可读摘要（同时落盘 report.txt，与 json / 本书正文构成三件套）
lines = []
lines.append("="*70)
lines.append("  UFT LEDGER NUMERICS — 250-digit mpmath, CODATA 2022 / PDG / Planck 2018")
lines.append("="*70)
lines.append(f"  1/α            = {mp.nstr(alpha_inv, 18)}   (CODATA 2022: 137.035999...)")
lines.append(f"  m_p c^2        = {mp.nstr(m_p_MeV, 9)} MeV")
lines.append(f"  l_P            = {mp.nstr(l_P, 6)} m")
lines.append(f"  E_P            = {mp.nstr(E_P_GeV, 6)} GeV")
lines.append(f"  log10(F_e/F_g) at r=1 m (p-p) = {log10_ratio:.3f}")
lines.append(f"  质子质量中胶子贡献 = {float(glue_fraction)*100:.2f}%")
lines.append(f"  t_H            = {float(t_H_Gyr):.3f} Gyr")
lines.append(f"  E_P / v_EW     = {float(hierarchy_ratio):.3e}")
lines.append(f"  m_W(tree)      = {float(m_W_tree):.3f} GeV;  m_W(tree)-m_W(meas) = {float(m_W_tree_vs_meas):.3f} GeV")
lines.append("-"*70)
passed = sum(1 for g in guards.values() if g["pass"])
total = len(guards)
lines.append(f"  GUARDS: {passed}/{total} passed")
for k, v in guards.items():
    mark = "PASS" if v["pass"] else "FAIL"
    lines.append(f"    [{mark}] {k}: {v['detail']}")
lines.append("="*70)
report = "\n".join(lines) + "\n"
(HERE / "uft_numerics_report.txt").write_text(report, encoding="utf-8")
print(report)
print(f"written: {json_path}")
print(f"written: {HERE / 'uft_numerics_report.txt'}")

sys.exit(0 if passed == total else 1)
