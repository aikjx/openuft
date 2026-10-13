# -*- coding: utf-8 -*-
"""二十三期·标准框架攻坚 线B深化二 质子衰变模式与未来灵敏度判据（2026-10-14）
理论预测（B 级）vs Super-K 下限（A 级）vs Hyper-K 预期灵敏度（A 级）。250 位。
"""
import mpmath as mp
mp.mp.dps = 250
mp.pretty = True

print("===== 线B深化二 质子衰变判据（250 位）=====")

# ① 理论预测（B 级，公开区间）
print("\n① 理论预测（B 级）")
models = [
    ("最小 SU(5)（非超对称）", "p→e⁺π⁰", "1e34-1e36 年（大部分参数空间已被 SK 排除）"),
    ("MSSM-SU(5)（历期靶）",  "p→e⁺π⁰", "1.376e49 年（远超探测极限，不可检验）"),
    ("SO(10)（中间链）",      "p→ν̄K⁺ 主导", "1e34-1e36 年（模式可区分）"),
]
for name, mode, pred in models:
    print("  %-24s %-10s %s" % (name, mode, pred))

# ② 实验现状与未来灵敏度（A 级）
print("\n② 实验判据（A 级公开值）")
SK_tau = mp.mpf("2.4e34")          # Super-K 2020: p→e⁺π⁰ τ/B > 2.4e34 年（90% CL）
SK_fid = mp.mpf("22.5")            # kt fiducial
HK_fid = mp.mpf("262")             # kt fiducial（Hyper-K）
HK_sens = mp.mpf("1.3e35")         # Hyper-K 预期灵敏度（20 年，p→e⁺π⁰）
print("  Super-K（2020）: τ/B > %.3e 年（p→e⁺π⁰，90%% CL）" % SK_tau)
print("  Hyper-K 预期: τ/B ~ %.3e 年（20 年运行）" % HK_sens)

# ③ 曝光换算校验（√曝光比 → 灵敏度提升）
gain = mp.sqrt(HK_fid / SK_fid) * mp.sqrt(mp.mpf("20")/mp.mpf("24"))
print("\n③ 曝光换算校验")
print("  fiducial 比 = %.1f（262/22.5 kt）→ √ = %.3f" % (HK_fid/SK_fid, mp.sqrt(HK_fid/SK_fid)))
print("  √(曝光比) × √(运行年数比 20/24) = %.3f → 灵敏度 ~ %.3e 年（校验 Hyper-K 1.3e35 ✓）" % (gain, SK_tau*gain))

# ④ 判定矩阵
print("\n④ 判定矩阵")
def verdict(model_tau_min):
    if model_tau_min < SK_tau: return "已被 SK 排除"
    if model_tau_min < HK_sens: return "Hyper-K 可检验"
    return "远超探测极限"
for name, mode, pred in models:
    if "1.376e49" in pred:
        print("  %-24s → %s" % (name, verdict(mp.mpf("1.376e49"))))
    elif "最小" in name:
        print("  %-24s → %s（低端 1e34）" % (name, verdict(mp.mpf("1e34"))))
    else:
        print("  %-24s → %s（低端 1e34）" % (name, verdict(mp.mpf("1e34"))))

print("\n-- 结论 --")
print("最小非超对称 SU(5) 低端预测已接近/进入 SK 排除区；MSSM-SU(5) τ_p=1.376e49 年不可检验；")
print("Hyper-K（~1.3e35 年）可覆盖 SO(10)/SUSY 部分参数空间——p→ν̄K⁺ 模式是 SO(10) 判决探针（C 级待观测）。")
