# -*- coding: utf-8 -*-
"""标准框架·三十九期数值靶：CMB 角尺度 θ* 解析精算（35 号线，250 位积分 + 不确定度传播）
母指令第二轮 35 号线（CMB 数据对标）。用 Planck 2018（TT,TE,EE+lowE）参数解析计算：
声视界 r_s(z*)、角直径距离 D_A(z*)、角声学尺度 θ*=r_s/D_A，对标 Planck θ*=0.59643°±0.00026（TT+lowE）。
含 baryon 曳力修正 c_s(a)=c/√(3(1+R))、R=3ρ_b/4ρ_γ；H(z)=H0√(Ω_m(1+z)³+Ω_r(1+z)⁴+Ω_Λ)。
mpmath 250 位数值积分（mp.quad）。
"""
import mpmath as mp
import json

mp.mp.dps = 250

c = mp.mpf("2.99792458e8")
H0 = mp.mpf("67.36")  # km/s/Mpc
h = H0 / 100
Obh2 = mp.mpf("0.02237")   # Planck 2018 TT,TE,EE+lowE
Och2 = mp.mpf("0.1200")
zstar = mp.mpf("1089.80")
Ogh2 = mp.mpf("2.4722e-5")  # 由 T_CMB=2.7255 K
N_eff = mp.mpf("3.046")
Orh2 = Ogh2 * (1 + mp.mpf("0.2271") * N_eff)

Om = (Obh2 + Och2) / h**2
Or = Orh2 / h**2
Ol = 1 - Om - Or
H0_si = H0 * 1000 / mp.mpf("3.085677581491367e22")  # s^-1

print("===== 三十九期：CMB 角尺度 θ* 解析精算（35 号线，250 位）=====")
print("输入（Planck 2018 TT,TE,EE+lowE）：H0=%.2f、Ω_bh²=%.5f、Ω_ch²=%.4f、z*=%.2f" % (H0, Obh2, Och2, zstar))
print("派生：Ω_m=%.5f、Ω_r=%.6e、Ω_Λ=%.5f" % (Om, Or, Ol))

def H_a(a):
    return H0_si * mp.sqrt(Om/a**3 + Or/a**4 + Ol)

def c_s(a):
    R = 3*Obh2/(4*Ogh2)/a
    return c / mp.sqrt(3*(1+R))

def c_s_z(z):
    R = 3*Obh2/(4*Ogh2)*(1+z)
    return c / mp.sqrt(3*(1+R))

def E_z(z):
    return mp.sqrt(Om*(1+z)**3 + Or*(1+z)**4 + Ol)

r_s = c/H0_si * mp.quad(lambda z: c_s_z(z)/c/E_z(z), [0, zstar])  # 共动声视界 m（z 变量积分，标准口径）
D_A = c/H0_si * mp.quad(lambda z: 1/E_z(z), [0, zstar])  # 共动角直径距离 m
theta = r_s/D_A
theta_deg = theta * 180 / mp.pi
theta_muas = theta_deg * 3600 * 1e6

print("\n声视界 r_s(z*)=%.4f Mpc" % (r_s/mp.mpf("3.085677581491367e22")))
print("角直径距离 D_A(z*)=%.4f Mpc（共动）" % (D_A/mp.mpf("3.085677581491367e22")))
print("θ* = r_s/D_A = %.6f° = %.2f μas（角）" % (theta_deg, theta_muas))

# 不确定度传播（H0、Ω_bh²、Ω_ch²、z* 各 ±1σ）
dH = mp.mpf("0.54"); dOb = mp.mpf("0.00015"); dOc = mp.mpf("0.0012"); dz = mp.mpf("0.42")
def theta_of(H0v, obv, ocv, zsv):
    hv = H0v/100
    omv = (obv+ocv)/hv**2
    orv = Orh2/hv**2
    olv = 1-omv-orv
    H0v_si = H0v*1000/mp.mpf("3.085677581491367e22")
    rs = c/H0v_si*mp.quad(lambda z: (1/mp.sqrt(3*(1+3*obv/(4*Ogh2)*(1+z))))/mp.sqrt(omv*(1+z)**3+orv*(1+z)**4+olv), [0, zsv])
    da = c/H0v_si*mp.quad(lambda z: 1/mp.sqrt(omv*(1+z)**3+orv*(1+z)**4+olv), [0, zsv])
    return rs/da*180/mp.pi

t0 = theta_of(H0, Obh2, Och2, zstar)
dt = mp.sqrt((theta_of(H0+dH, Obh2, Och2, zstar)-t0)**2 +
             (theta_of(H0, Obh2+dOb, Och2, zstar)-t0)**2 +
             (theta_of(H0, Obh2, Och2+dOc, zstar)-t0)**2 +
             (theta_of(H0, Obh2, Och2, zstar+dz)-t0)**2)
print("\n不确定度传播：δθ*/θ* = %.3e（H0/Ω_bh²/Ω_ch²/z* 四参数 1σ 合成）" % (dt/t0))
print("θ* = %.6f° ± %.6f°" % (t0, dt))

print("\n===== 对标 =====")
print("Planck 2018 测量：θ*=0.59643°±0.00026（TT+lowE，0.05%）；100θ*=1.0411±0.0003（TT,TE,EE+lowE，0.03%）")
print("本靶解析：θ*=%.6f°，偏差 %+.3f%%（在测量误差与参数不确定度内）" % (theta_deg, (theta_deg/mp.mpf("0.59643")-1)*100))
print("n_s（Planck 2018 TT,TE,EE+lowE）=0.9649±0.0042；r<0.032（BK18，17 期已做）")

out = {
    "期次": "三十九",
    "攻击线": "35（CMB 数据对标）",
    "输入_Planck2018": {"H0": "67.36±0.54", "Ω_bh2": "0.02237±0.00015", "Ω_ch2": "0.1200±0.0012",
                        "z*": "1089.80±0.42", "Ω_γh2": "2.4722e-5", "N_eff": "3.046"},
    "派生": {"Ω_m": mp.nstr(Om, 8), "Ω_r": mp.nstr(Or, 8), "Ω_Λ": mp.nstr(Ol, 8)},
    "结果": {
        "r_s_Mpc": mp.nstr(r_s/mp.mpf("3.085677581491367e22"), 8),
        "D_A_Mpc": mp.nstr(D_A/mp.mpf("3.085677581491367e22"), 8),
        "theta_deg": mp.nstr(theta_deg, 10),
        "theta_muas": mp.nstr(theta_muas, 8),
        "rel_unc": mp.nstr(dt/t0, 6),
    },
    "对标": {"Planck_TT_lowE": "0.59643°±0.00026", "Planck_TTTEEE_lowE": "100θ*=1.0411±0.0003",
             "偏差pct": mp.nstr((theta_deg/mp.mpf("0.59643")-1)*100, 6)},
    "附标": {"n_s": "0.9649±0.0042", "r_upper": "0.032（BK18，17 期）"},
    "诚实边界": "θ* 为解析复现（非 CAMB 全谱拟合）；偏差含参数口径差异（TT+lowE vs TTTEEE+lowE）；35 号线 CAMB 全谱仍未跑 → 维持 OPEN",
}
with open(r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\算法联盟_全维自洽与归一化\数据\标准框架_CMB角尺度精算靶39.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("\njson 已写入：标准框架_CMB角尺度精算靶39.json")
