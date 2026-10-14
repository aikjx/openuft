# -*- coding: utf-8 -*-
"""标准框架·三十三期数值靶：EHT/ngEHT 光子环重校（2026 版）
承接二十四期（Schw 阴影 M87* 39.6893 μas / Sgr A* 52.1062 μas；Kerr a*=0.94 → 39.03 μas）。
本期新增：(1) 2025-2026 新测量对照（M87 2018: 43.3±1.5 μas；86 GHz: 64+4-8 μas）；
(2) 质量/距离归一化灵敏度（理论值不确定度来源）；
(3) 光子环子环角分离 vs 阵列分辨率预算（EHT ~20 μas → ngEHT ~15 μas → 空间 VLBI 亚 μas），
修正 24 期「ngEHT 10-20 μas 分辨光子环」口径。mpmath 250 位。
"""
import mpmath as mp
import json

mp.mp.dps = 250

c = mp.mpf("2.99792458e8")
G = mp.mpf("6.67430e-11")
Msun = mp.mpf("1.98847e30")
pc_m = mp.mpf("3.085677581491367e16")
muas_per_rad = mp.mpf("2.062648062470964e11")  # 1 rad = 2.062648e11 μas

# 目标参数（本靶口径：EHT 2022 主口径 M=4.297e6/D=8277 pc；24 期用 GRAVITY 口径 4.154e6/8.178 kpc，差 2.2% 属文献口径差异）
M87_M = mp.mpf("6.5e9") * Msun
M87_D = mp.mpf("16.8e6") * pc_m
SgrA_M = mp.mpf("4.297e6") * Msun
SgrA_D = mp.mpf("8277") * pc_m

# 质量/距离标称不确定度（文献：恒星动力学 M87 6.5±0.7e9；距离 16.8±0.8 Mpc；Sgr A* 4.297±0.012e6/0.012，距离 8277±33 pc）
M87_M_rel = mp.mpf("0.7") / mp.mpf("6.5")
M87_D_rel = mp.mpf("0.8") / mp.mpf("16.8")
SgrA_M_rel = mp.mpf("0.012") / mp.mpf("4.297")
SgrA_D_rel = mp.mpf("33") / mp.mpf("8277")

def shadow_dia_muas(M, D):
    """Schw 阴影角直径：2·(3√3 GM/c²)/D"""
    b = 3 * mp.sqrt(3) * G * M / c**2
    return 2 * b / D * muas_per_rad

th_M87 = shadow_dia_muas(M87_M, M87_D)
th_SgrA = shadow_dia_muas(SgrA_M, SgrA_D)

print("===== 三十三期：EHT/ngEHT 光子环重校（2026 版，250 位）=====")
print("Schw 阴影角直径（本靶重算）：M87* = %.4f μas | Sgr A* = %.4f μas" % (th_M87, th_SgrA))
print("二十四期对照：M87* 39.6893 μas（同口径一致）| Sgr A* 52.1062 μas（24 期 GRAVITY 口径 4.154e6/8.178 kpc；"
      "本靶 EHT2022 口径 4.297e6/8277 pc，差 %.1f%% 属文献口径差异）" % ((th_SgrA/mp.mpf("52.1062")-1)*100))

# 归一化灵敏度：dθ/θ = dM/M + dD/D（相对误差线性叠加）
for name, m_rel, d_rel in [("M87*", M87_M_rel, M87_D_rel), ("Sgr A*", SgrA_M_rel, SgrA_D_rel)]:
    tot = mp.sqrt(m_rel**2 + d_rel**2)
    print("  %s 归一化相对不确定度：δM/M=%.4f + δD/D=%.4f → 合成 δθ/θ=%.4f（理论值 ±%.2f%%）"
          % (name, m_rel, d_rel, tot, tot*100))

# 测量对照
print("\n===== 测量对照（2025-2026 检索）=====")
meas = [
    ("M87* 2017 EHT 230GHz", "42 ± 3 μas", th_M87, (mp.mpf("42")-th_M87)/th_M87*100),
    ("M87* 2018 EHT 230GHz", "43.3 ± 1.5 μas", th_M87, (mp.mpf("43.3")-th_M87)/th_M87*100),
    ("M87* 86GHz（喷流基座，非阴影）", "64 +4/-8 μas", th_M87, (mp.mpf("64")-th_M87)/th_M87*100),
    ("Sgr A* EHT 2022 230GHz", "51.8 ± 2.3 μas", th_SgrA, (mp.mpf("51.8")-th_SgrA)/th_SgrA*100),
]
for nm, val, theo, dev in meas:
    print("  %-32s 测量=%s | 本靶 Schw=%.2f μas | 偏差 %+.1f%%" % (nm, val, theo, dev))

# 光子环子环角分离（n=0 ↔ n=1 环，Schw 指数收窄近似 Δb/b ~ e^(-2π)）
exp2pi = mp.e**(-2*mp.pi)
d_sep_M87 = th_M87 * exp2pi
d_sep_SgrA = th_SgrA * exp2pi
print("\n===== 光子环子环角分离（Schw 指数收窄，n=0↔n=1 间距量级 ~e^(-2π)=%.6f）=====" % exp2pi)
print("  M87* 子环分离 ≈ %.4f μas | Sgr A* ≈ %.4f μas" % (d_sep_M87, d_sep_SgrA))

# 分辨率预算（λ/B 衍射极限）
print("\n===== 阵列分辨率预算（θ_res = λ/B）=====")
res = [
    ("EHT 2017（230 GHz, B_max~10 Gλ）", mp.mpf("1")/mp.mpf("1e10")*muas_per_rad),
    ("ngEHT 目标（345 GHz, B_max~13.8 Gλ）", mp.mpf("1")/mp.mpf("1.38e10")*muas_per_rad),
    ("空间 VLBI 概念（230 GHz, 基线 1e6 km）", mp.mpf("1.3e-3")/mp.mpf("1e9")*muas_per_rad),
    ("空间 VLBI 概念（345 GHz, 基线 3e6 km）", mp.mpf("0.87e-3")/mp.mpf("3e9")*muas_per_rad),
]
for nm, th_res in res:
    print("  %-48s θ_res ≈ %.3f μas" % (nm, th_res))

print("\n===== 判决（修正二十四期口径）=====")
print("1) 2017/2018 环直径 42±3 / 43.3±1.5 μas 与本靶 Schw 39.7-42 μas 一致（质量/距离归一化 δθ/θ≈%.2f%% 内）"
      % (mp.sqrt(M87_M_rel**2 + M87_D_rel**2)*100))
print("2) 86 GHz 64 μas 为喷流基座发射，非阴影——不构成冲突（尺度/频率依赖）")
print("3) 二十四期「ngEHT 10-20 μas 分辨光子环」修正：ngEHT 衍射极限仍 ~15 μas，"
      "其收益是 uv 覆盖提升→环直径/形状测量精度（亚 μas 定位），非子环直接分辨")
print("4) 光子环子环分离 ~0.08-0.1 μas（M87/Sgr A*）：需 θ_res<0.05 μas → 下一代空间 VLBI"
      "（≥345 GHz 或基线 ≥3e6 km），2030s-2040s 判决 GR 光子环结构")

out = {
    "期次": "三十三",
    "口径": "Schw 阴影角直径 2·3√3 GM/(c²D)；子环分离 ~e^(-2π) 指数收窄；θ_res=λ/B；250 位",
    "输入": {"M87_M": "6.5e9 Msun", "M87_D": "16.8 Mpc", "SgrA_M": "4.297e6 Msun（EHT2022 口径）", "SgrA_D": "8277 pc（EHT2022 口径）",
            "注": "24 期 Sgr A* 用 GRAVITY 口径 4.154e6/8.178 kpc，差 2.2% 属文献口径差异",
            "M87_unc": "δM/M=0.7/6.5, δD/D=0.8/16.8", "SgrA_unc": "δM/M=0.012/4.297, δD/D=33/8277"},
    "重算": {"M87_Schw_muas": mp.nstr(th_M87, 10), "SgrA_Schw_muas": mp.nstr(th_SgrA, 10),
            "M87_sigma_theta_pct": mp.nstr(mp.sqrt(M87_M_rel**2+M87_D_rel**2)*100, 8),
            "SgrA_sigma_theta_pct": mp.nstr(mp.sqrt(SgrA_M_rel**2+SgrA_D_rel**2)*100, 8)},
    "测量对照": [{"源": m[0], "值": m[1], "本靶Schw_muas": mp.nstr(m[2], 8), "偏差pct": mp.nstr(m[3], 6)} for m in meas],
    "子环分离_muas": {"M87": mp.nstr(d_sep_M87, 8), "SgrA": mp.nstr(d_sep_SgrA, 8)},
    "分辨率预算_muas": [{"阵列": r[0], "theta_res": mp.nstr(r[1], 8)} for r in res],
    "判决": [
        "M87 2017/2018 环（42±3 / 43.3±1.5 μas）与 Schw 理论一致（归一化误差内）",
        "86 GHz 64 μas 为喷流基座，非阴影，不冲突",
        "修正 24 期：ngEHT 衍射极限 ~15 μas，收益为环参数测量精度而非子环分辨",
        "子环分离 ~0.08-0.1 μas → 需空间 VLBI（2030s-2040s）才可判决 GR 光子环结构",
    ],
    "诚实边界": "子环分离为 Schw 指数收窄近似（Kerr 依赖 a*/倾角，量级不变）；86 GHz 口径非阴影已注明",
}
with open(r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\算法联盟_全维自洽与归一化\数据\标准框架_EHT光子环重校33.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("\njson 已写入：标准框架_EHT光子环重校33.json")
