# -*- coding: utf-8 -*-
"""十八期·标准框架攻坚 线C深化 非参数 w(z) 重建与形状函数残差检验（2026-10-14）
A 级数据（已查证）：LRG1 z=0.510 张力 2.42σ、LRG3+ELG1 z=0.934 张力 2.60σ（arXiv:2507.21607）；
H(z) z≈0.7 处比 ΛCDM 高 3-4%（Bansal & Huterer 2025）；穿越 z_pc=0.45±0.04（arXiv:2505.02207）。
250 位计算：给定 H(z) 偏差反推所需 w_eff（Friedmann + 单箱 DE 密度演化）。
"""
import mpmath as mp
mp.mp.dps = 250
mp.pretty = True

# ---- 输入（A 级公开）----
Om = mp.mpf("0.315")        # Planck 2018 物质密度
z_ref = mp.mpf("0.7")       # Bansal-Huterer 偏差参考红移
dH_obs = mp.mpf("0.035")    # H 高 3.5%（区间 3-4% 中心）

print("===== 线C深化 形状函数残差检验 + w_eff 反推（250 位）=====")

# ① 形状函数 S(z) 残差表（A 级：每箱与 Planck ΛCDM 的 Ωm 张力 σ）
print("\n① 形状函数残差（Ωm 张力，A 级，arXiv:2507.21607）")
sbins = [
    ("LRG1    z_eff=0.510", mp.mpf("2.42")),
    ("LRG3+ELG1 z_eff=0.934", mp.mpf("2.60")),
    ("全样本（DR2 Ωm 张力）", mp.mpf("1.84")),
    ("DR1 → DR2 Ωm 张力改善", mp.mpf("2.20")),
]
for name, sig in sbins:
    tag = ">3σ 强候选" if sig >= 3 else (">2σ 需关注" if sig >= 2 else "<2σ 一致")
    print("  %s : %sσ -> %s" % (name, sig, tag))

# ② ΛCDM 参考 + H(z) 偏差反推 w_eff（250 位）
print("\n② 给定 H(z) 偏差反推 w_eff（单箱 [0, 0.7]，Ωm=0.315）")
def E2_lcdm(z):
    return Om*(1+z)**3 + (1-Om)
E2_ref = E2_lcdm(z_ref)
E_ref = mp.sqrt(E2_ref)
print("  ΛCDM E(0.7)=%.10f, E²=%.10f" % (E_ref, E2_ref))

def w_eff_from_dH(dH):
    E_obs = E_ref * (1 + dH)
    E2_obs = E_obs**2
    Om_z = Om*(1+z_ref)**3
    ODE_obs = E2_obs - Om_z
    ODE_0 = 1 - Om
    fDE = ODE_obs / ODE_0
    ln1pz = mp.log(1+z_ref)
    w = -1 + mp.log(fDE) / (3*ln1pz)
    return w, fDE, E_obs, ODE_obs

w_eff, fDE, E_obs, ODE_obs = w_eff_from_dH(dH_obs)
print("  H 高 3.5%% → E_obs=%.10f, ΩDE(0.7)=%.10f, f_DE=%.10f" % (E_obs, ODE_obs, fDE))
print("  → 所需平均 w_eff = %.10f（比 −1 高 %.4f）" % (w_eff, w_eff+1))

print("\n③ ΔH/H 扫描 → w_eff（区间 2-4%）")
for dh in (mp.mpf("0.02"), mp.mpf("0.03"), mp.mpf("0.035"), mp.mpf("0.04")):
    w, _, _, _ = w_eff_from_dH(dh)
    print("  ΔH/H=%4.1f%% → w_eff = %.10f（偏离 %+.4f）" % (dh*100, w, w+1))

# ④ 穿越与谱指数判据（A 级）
print("\n④ 非参数重建判据（A 级）")
print("  穿越点 z_pc = 0.45 ± 0.04（arXiv:2505.02207：ΛCDM 恢复一致需 phantom 穿越）")
print("  w(z) 趋势：低 z w>-1、高 z w<-1（Quintom-B）；2509.17454 非参数重建同向")
print("  系统学脆弱性：去除 LRG1/LRG2 后 ΛCDM 完全恢复（2507.21607）——信号由单个 tracer 驱动")

print("\n-- 结论 --")
print("形状函数残差：LRG1/LRG3+ELG1 两箱 >2σ（2.42σ/2.60σ）驱动信号，全样本 1.84σ——未达 5σ 判决；")
print("若 H(z)@0.7 真实偏高 3.5%，需 w_eff≈" + mp.nstr(w_eff, 4) + "（与 DESI w0>-1 拟合一致）；系统学脆弱，须 Euclid 独立验证。")
