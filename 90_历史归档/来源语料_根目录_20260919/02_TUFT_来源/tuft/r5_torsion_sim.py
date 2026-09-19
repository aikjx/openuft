# -*- coding: utf-8 -*-
"""
TUFT-R5 扭秤挠率探测 · 修正版数值仿真（可复跑 / headless）
================================================================
对草稿 §7 代码的修复：
  (1) 复原 LaTeX 损坏（\(^1\) → 数字）；
  (2) 修正 S_tot（10g Fe, P=0.1 → 1.2e22 ħ，非 1e21）；
  (3) 噪声口径：独立噪声按【方差相加】得 PSD（非幅度相加）；
  (4) 采样噪声 σ=√(S·f_s/2)；锁相本底 1σ = ASD·√(2/T)；
  (5) 绘图改 Agg + 存盘（无 GUI）。
红线：本仿真只验证【信号提取链路】的数值自洽；T_source 的来源不由本文件证明。
"""
import os
import sys

import numpy as np

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAS_PLT = True
except Exception:
    HAS_PLT = False

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
HBAR = 1.054571817e-34

# ---------------- 参数（修正版） ----------------
kappa_torsion = 1e-8                 # N·m/rad
S_tot_hbar = 1.2e22                  # 修正：10g Fe, P=0.1（原文 1e21）
S_tot = S_tot_hbar * HBAR            # J·s
T_source = 1e-4                      # s^-1
f_mod = 1.0                          # Hz
omega = 2 * np.pi * f_mod

# 噪声 PSD（rad^2/Hz），独立噪声 → 方差相加
S_thermal = (1e-12) ** 2
S_vibration = (1e-11) ** 2
S_magnetic = (1e-10) ** 2
S_total = S_thermal + S_vibration + S_magnetic
noise_asd = np.sqrt(S_total)          # rad/√Hz

# 采样
fs = 200.0
T_meas = 100.0
t = np.arange(0.0, T_meas, 1.0 / fs)
N = len(t)
dt = 1.0 / fs

# ---------------- 信号 ----------------
theta_amp = S_tot * T_source / kappa_torsion     # 振幅 rad
theta_signal = theta_amp * np.sin(omega * t)

# ---------------- 噪声（白噪声，单边 PSD = S_total） ----------------
rng = np.random.default_rng(42)
sigma = np.sqrt(S_total * fs / 2.0)              # 每采样点 std
noise = rng.normal(0.0, sigma, N)
theta_meas = theta_signal + noise

# ---------------- 锁相放大 ----------------
ref_sin = np.sin(omega * t)
ref_cos = np.cos(omega * t)
X = 2.0 * np.mean(theta_meas * ref_sin)
Y = 2.0 * np.mean(theta_meas * ref_cos)
amp = float(np.hypot(X, Y))
phase = float(np.degrees(np.arctan2(Y, X)))

# ---------------- 噪声本底与 SNR ----------------
noise_floor = noise_asd * np.sqrt(2.0 / T_meas)  # 锁相 1σ（rad）
snr = amp / noise_floor

print("=" * 70)
print("TUFT-R5 扭秤挠率探测 · 修正版仿真")
print("=" * 70)
print("S_tot            = %.3e ħ = %.4e J·s" % (S_tot_hbar, S_tot))
print("理论信号振幅 θ   = %.4e rad" % theta_amp)
print("噪声 ASD         = %.4e rad/√Hz" % noise_asd)
print("锁相提取振幅     = %.4e rad" % amp)
print("提取相位         = %.4f 度" % phase)
print("锁相噪声本底(T)  = %.4e rad（T=%.0fs）" % (noise_floor, T_meas))
print("SNR              = %.1f" % snr)
print("-" * 70)
ok_amp = abs(amp - theta_amp) / theta_amp < 0.05
ok_snr = snr > 100
print("[%s] 振幅还原误差 < 5%%" % ("PASS" if ok_amp else "FAIL"))
print("[%s] SNR > 100" % ("PASS" if ok_snr else "FAIL"))
print("  注：若取原文 S_tot=1e21 ħ，则 θ=%.3e rad，SNR≈%.0f"
      % (1e21 * HBAR * T_source / kappa_torsion,
         (1e21 * HBAR * T_source / kappa_torsion) / noise_floor))

# ---------------- 绘图（可选，存盘） ----------------
if HAS_PLT:
    freq = np.fft.rfftfreq(N, dt)
    spec = np.abs(np.fft.rfft(theta_meas)) * dt
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
    ax[0].plot(t, theta_meas, alpha=0.3, label="measured (with noise)")
    ax[0].plot(t, theta_signal, "r-", label="theory torsion signal")
    ax[0].set_xlim(0, 20)
    ax[0].set_xlabel("time (s)")
    ax[0].set_ylabel("deflection (rad)")
    ax[0].set_title("Torsion balance: time domain")
    ax[0].legend()
    ax[0].grid(True)
    ax[1].semilogy(freq, spec)
    ax[1].axvline(f_mod, color="r", ls="--", label="f_mod = %.1f Hz" % f_mod)
    ax[1].set_xlim(0, 5)
    ax[1].set_xlabel("frequency (Hz)")
    ax[1].set_ylabel("amplitude")
    ax[1].set_title("Spectrum: peak at f_mod")
    ax[1].legend()
    ax[1].grid(True)
    fig.tight_layout()
    out_png = os.path.join(HERE, "tuft_r5_torsion_sim.png")
    fig.savefig(out_png, dpi=110)
    print("[图已存] " + out_png)
else:
    print("[skip] 未安装 matplotlib，跳过绘图")
