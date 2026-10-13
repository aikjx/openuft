# -*- coding: utf-8 -*-
"""十四期·标准框架攻坚 线C 宇宙学引力 w(z) 偏差统计门槛工具（2026-10-13）
输入：DESI 各数据组合对 ΛCDM(w=-1) 的排除显著性（已查证 A 级，来源见数据表）
判据：σ 门槛分级——无证据 <2σ / 弱-中等 2-3σ / 中等-强 3-5σ（未判决）/ 判决性 ≥5σ
输出：当前宇宙学引力攻坚状态判定 + 证据矩阵。mpmath 250 位。
"""
import mpmath as mp
mp.mp.dps = 250

# ---- 已查证数据（A 级：官方摘要/同行评审，来源见下表）----
desi = [
    # (组合, σ排除ΛCDM, 来源)
    ("DESI DR1+CMB+Pantheon+", mp.mpf("2.6"), "Adame et al. 2025a / A&A 2026 综述"),
    ("DESI DR1+CMB+Union3",    mp.mpf("3.5"), "同上"),
    ("DESI DR1+CMB+DES-SN5YR", mp.mpf("3.9"), "同上"),
    ("DESI DR2+CMB（单独，最稳健）", mp.mpf("3.1"), "arXiv:2504.15336（组合原则化合并）"),
    ("DESI DR2+CMB+Pantheon+", mp.mpf("2.8"), "DESI DR2 官方 / A&A 2026 综述"),
    ("DESI DR2+CMB+Union3",    mp.mpf("3.8"), "同上"),
    ("DESI DR2+CMB+DES-SN5YR", mp.mpf("4.2"), "同上"),
    ("Lyα+CMB+Galaxy BAO（DR2）", mp.mpf("3.10"), "A&A 57820-25（2026）"),
    ("DESI BAO vs CMB（独立张力指标）", mp.mpf("2.2"), "arXiv:2505.02207（Suspiciousness/GoF）"),
    ("DESI DR2+PP（独立分析，含 SNe 去重）", mp.mpf("2.5"), "arXiv:2504.15336（降低后）"),
]

def verdict(sig):
    if sig < mp.mpf("2"):   return "无证据"
    if sig < mp.mpf("3"):   return "弱-中等（未判决）"
    if sig < mp.mpf("5"):   return "中等-强（未判决，未达判决性）"
    return "判决性"

print("===== 线 C 宇宙学引力 · w(z) 偏差统计门槛（250 位）=====")
print("%-32s %8s   %s" % ("数据组合", "σ", "判定"))
sig_list = []
for name, sig, src in desi:
    sig_list.append(sig)
    print("%-32s %6.2f   %s" % (name, sig, verdict(sig)))

sig_max = max(sig_list)
sig_robust = mp.mpf("3.1")   # DESI+CMB 单独（最稳健口径）
print("\n-- 汇总 --")
print("全组合 σ 范围: %.2f – %.2f（口径依赖强）" % (min(sig_list), sig_max))
print("最稳健口径（DESI+CMB 单独）: %.1fσ => %s" % (sig_robust, verdict(sig_robust)))
print("判决门槛 5σ：当前最高 %.1fσ < 5σ —— 尚未判决性排除 ΛCDM" % sig_max)

# ---- 预测靶：需要什么才能达到 5σ（对未来实验的量化门槛）----
print("\n-- 未来判决门槛（量化）--")
print("DESI DR2 后统计精度 ~0.24%（官方）；若 w0 真值偏离 −1 为 Δw，需 σ_comb = |Δw|/σ_w ≥ 5")
for dw in (mp.mpf("0.1"), mp.mpf("0.2"), mp.mpf("0.3")):
    need = mp.mpf("5") * mp.mpf("1")  # 需要 σ_w ≤ |Δw|/5
    print("  Δw=%.1f 时需 σ_w ≤ %.4f（当前 DESI 组合 σ_w ~0.05-0.07 区间、部分模型 ~0.03）" % (dw, dw / 5))

print("\n-- 结论 --")
print("宇宙学引力攻坚现状：动态暗能量（Quintom-B 型 w0>-1, wa<0）受 DESI 数据 2.8-4.2σ 偏好（口径依赖），")
print("最稳健 3.1σ、独立分析降至 ~2σ——未达 5σ 判决性；ΛCDM 未被排除（A 级已查证）。")
print("下一步靶：Euclid 与下一代 CMB 的 w(z) 高精度测量（决策性实验）。")
