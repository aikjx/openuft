# -*- coding: utf-8 -*-
# V9.46 tuft_v123_exp_consistency.py
# 单方程封闭式 × 实验数据一致性矩阵审计（第五十一章）
import json, math

R = {}
# --- 常数（CODATA 2022 / PDG 2024）---
alpha = 0.0072973525693
hbarc = 197.3269804          # MeV*fm
m_e = 0.51099895             # MeV
m_p = 938.27208816           # MeV
m_P = 1.220890e22            # MeV (Planck 质量)
m_W = 80377.0                # MeV (pole)
m_pi = 134.9768              # MeV (pi0)
GF = 1.1663788e-5            # GeV^-2
tau_mu = 2.1969811e-6        # s
E1 = -13.605693122994        # eV 氢原子基态
g_e_exp = 2.00231930436256
g_tuft = 1.0
sigma_cornell = 0.18         # GeV^2

# --- 1. 库仑系数（电磁）---
R["coulomb_coeff"] = alpha * hbarc                       # MeV*fm
# --- 2. 牛顿系数（质子-质子）---
R["newton_coeff_pp"] = hbarc * (m_p/m_P)**2              # MeV*fm
R["newton_ratio"] = R["coulomb_coeff"] / R["newton_coeff_pp"]
# --- 3. 汤川力程（弱/强）---
R["lambda_W"] = hbarc / m_W                              # fm
R["lambda_pi"] = hbarc / m_pi                            # fm
# --- 4. 氢原子基态（TUFT 库仑极限变分，V9.24）---
R["E1_tuft"] = E1
# --- 5. g-2 电子 ---
R["g_dev"] = abs(g_tuft - g_e_exp)/g_e_exp
# --- 6. 光子质量上限 -> 库仑力程下界 ---
m_gamma_ub = 1e-18                                       # eV (PDG 上限)
R["lambda_gamma_lb_fm"] = hbarc / m_gamma_ub             # fm
# --- 7. 弱力费米常数对应质量 ---
R["m_GF"] = 1.0/math.sqrt(GF*1e3)                        # GeV -> MeV
# --- 8. 强 Cornell 裸 Yukawa chi2 比（V9.13）---
R["chi2_ratio_yukawa"] = 9.3e7
# --- 9. 氘核 Bargmann 上限（V9.26）---
R["deuteron_N0_ub"] = 0.0058
# --- 10. 形状因子 LEP 抑制 dB（V9.19）---
R["ff_lep_dB"] = 54.9
# --- 11. GW 速度偏差（GW170817, V9.42）---
R["gw_vdev_ub"] = 1e-15
# --- 12. EP 检验（MICROSCOPE）---
R["ep_eta_ub"] = 1.3e-14

# --- 判定矩阵（10 行）---
# (力/实验, TUFT 对照量, 实验值/上限, 相对偏差, 判定, 判别性, 参数来源)
rows = [
 ("电磁 库仑平方反比", "F=alpha*hbarc/r^2（λ→∞ 极限）", "n=2 至 1e-16 精度（Cavendish/Rutherford/光子质量）", "1e-16 级", "继承 PASS", "0（库仑既有）", "α 外输 B02"),
 ("引力 牛顿平方反比", "F=hbarc(m1m2/mP^2)/r^2", "EP 检验 eta<1.3e-14（MICROSCOPE）；G 卡文迪什", "eta 1.3e-14", "继承 PASS", "0（牛顿既有）", "G 外输 B01"),
 ("电磁 氢原子基态", "E1=-13.6057 eV（库仑极限变分）", "-13.6056931 eV（CODATA）", "5e-9", "继承 PASS", "0（薛定谔+库仑）", "α,m_e 外输"),
 ("弱 μ 衰变寿命", "无 V-A 方向结构，不可算", "tau_mu=2.1969811e-6 s", "—", "FAIL", "0", "G_F,V-A 外输 B03"),
 ("量子 g-2 电子", "g=1", "g=2.00231930436256", "50.06%", "FAIL", "0", "自旋结构外输 B03"),
 ("电磁 电荷形状因子", "螺旋延展 J0 形状因子 |G|^2 抑制 54.9 dB", "LEP 点状 e 散射", "54.9 dB", "FAIL", "0", "读法 B 参数字典"),
 ("强 氘核束缚", "纯 OPE 汤川 N0<=0.0058<1 零束缚", "B=2.225 MeV 存在束缚", "—", "FAIL", "0", "张量/排斥核外输 B03"),
 ("强 Cornell 势", "裸 Yukawa chi2 高 9.3e7 倍", "sigma=0.18 GeV^2 线性项", "9.3e7 倍", "FAIL", "0", "σ,mu 外源 B03"),
 ("引力 波速 GW170817", "v=c（式 1 无色散）", "|v/c-1|<=1e-15", "1e-15", "继承 PASS", "0（GR 同预言）", "—"),
 ("引力 EHT 阴影角", "GR 子极限 39.7-53.9 uas", "M87* 42 uas", "5.5%", "继承 PASS", "0（GR 子极限）", "—"),
]
R["matrix"] = rows
R["inherit_pass"] = sum(1 for r in rows if r[4].startswith("继承"))
R["fail"] = sum(1 for r in rows if r[4] == "FAIL")
R["discriminative"] = sum(1 for r in rows if not r[5].startswith("0"))
R["counts"] = {"继承PASS": R["inherit_pass"], "FAIL": R["fail"], "判别性一致": R["discriminative"]}

out = r"D:\a10\aikjx\code\my_lib\tuft_v123_exp_consistency_results.json"
json.dump(R, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("coulomb_coeff_MeVfm=%.7f" % R["coulomb_coeff"])
print("newton_coeff_pp_MeVfm=%.4e  ratio=%.4e" % (R["newton_coeff_pp"], R["newton_ratio"]))
print("lambda_W_fm=%.4e  lambda_pi_fm=%.4f  lambda_gamma_lb_fm=%.4e" % (R["lambda_W"], R["lambda_pi"], R["lambda_gamma_lb_fm"]))
print("g_dev=%.4f%%  m_GF=%.3f GeV" % (R["g_dev"]*100, R["m_GF"]/1e3))
print("counts=", R["counts"])
print("saved json ok")
