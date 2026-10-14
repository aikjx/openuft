# -*- coding: utf-8 -*-
"""标准框架·三十六期数值靶：质子衰变窗口重校（2026 版，SO(10) p→νK̄ 判决探针时效更新）
承接二十三期（最小 SU(5) p→e+π0 1e34-1e36 / MSSM 1.376e49 / SO(10) p→ν̄K⁺；SK 2020 τ/B>2.4e34；
Hyper-K ~1.3e35 → p→ν̄K⁺ 为 SO(10) 判决探针（C））。
本期更新（2025-2026 检索）：Hyper-K 2026 安装、2027 底注水、2028 全规模（186 kton fiducial）；
JUNO p→νK⁺ 10 年灵敏度 9.6e35 yr（200 kton·yr，arXiv:2212.08502）——液体闪烁体互补技术；
SK 新限制 p→e+η 1.4e34 yr。mpmath 250 位。
"""
import mpmath as mp
import json

mp.mp.dps = 250

print("===== 三十六期：质子衰变窗口重校（2026 版，250 位）=====")

# ---- A. 现有限制（SK，2020-2025 口径）----
limits = [
    ("p→e+π0", mp.mpf("2.4e34"), "SK 2020（23 期口径 τ/B>2.4e34）"),
    ("p→μ+π0", mp.mpf("1.6e34"), "SK，Phys.Rev.D 102,112011(2020)"),
    ("p→ν̄K⁺", mp.mpf("5.9e33"), "SK 2020（23 期口径；260 kton·yr）"),
    ("p→e+η", mp.mpf("1.4e34"), "SK 2025（NSF PAR）"),
    ("p→e+π0 补充通道", mp.mpf("7.3e33"), "SK 2025（LeptonPhoton 2025 报告）"),
]
print("\nA. 现有限制（下界，yr）：")
for ch, lim, src in limits:
    print("  %-14s τ>%.2e yr | %s" % (ch, lim, src))

# ---- B. 理论预测带（23 期定案）----
pred = [
    ("最小 SU(5) p→e+π0", mp.mpf("1e34"), mp.mpf("1e36")),
    ("MSSM（高维算符）", mp.mpf("1.376e49"), mp.mpf("1.376e49")),
    ("SO(10) p→ν̄K⁺", mp.mpf("1e35"), mp.mpf("1e36")),
]
print("\nB. 理论预测带（yr）：")
for mod, lo, hi in pred:
    if lo == hi:
        print("  %-18s τ=%.3e（23 期定案，不可达）" % (mod, lo))
    else:
        print("  %-18s τ∈[%.1e, %.1e]" % (mod, lo, hi))

# ---- C. 未来灵敏度与时间线 ----
print("\nC. 未来实验（2025-2026 检索）：")
hk_t10 = mp.mpf("1.3e35")  # HK p→ν̄K⁺ 10 年灵敏度（23 期；官方估算）
juno_t10 = mp.mpf("9.6e35")  # JUNO p→νK⁺ 10 年灵敏度（200 kton·yr，arXiv:2212.08502）
print("  Hyper-K：186 kton fiducial；2026 探测器安装 → 2027 底注水 → 2028 全规模；10 年数据 ≈ SK 100 年")
print("    p→ν̄K⁺ 10 年灵敏度 ~1.3e35 yr；20 年（零本底线性）~2.6e35 yr")
print("  JUNO：200 kton·yr（10 年）p→νK⁺ 灵敏度 9.6e35 yr（效率 36.9%，本底 0.2 事件）")
print("    vs SK 现有限制 5.9e33 → JUNO 灵敏度高 1.63e2 倍")
print("    vs SO(10) 预测带 [1e35,1e36] → JUNO 10 年可覆盖")

# ---- D. 判决窗口 ----
print("\nD. 判决窗口（时间线）:")
print("  p→e+π0（最小 SU(5) 通道）：SK 2.4e34 已排除预测带低端（1e34）；Hyper-K 10 年 ~1e35 → 2038 前覆盖 [1e35,1e36]")
print("  p→ν̄K⁺（SO(10) 判决探针）：SK 5.9e33 未达；JUNO 10 年 9.6e35 覆盖 SO(10) 带 → 2034-2035 前后判决")
print("  Hyper-K 补充：2028 全规模 + 10 年 → 2038 触及 SO(10) 带低端（1e35）；20 年 ~2.6e35 更稳")
print("  MSSM 1.376e49：任何可设想实验不可达（保持 23 期判定）")

# 灵敏度-时间外推（零本底线性假设，标注）
print("\nE. 灵敏度-时间外推（零本底线性假设 S∝t，标注口径）：")
for name, s10, t0 in [("JUNO", juno_t10, mp.mpf("2025")), ("Hyper-K", hk_t10, mp.mpf("2028"))]:
    for yrs in [10, 15, 20]:
        s = s10 * yrs / 10
        print("  %s %d 年：%.2e yr（约 %d 年达到）" % (name, yrs, s, int(t0 + yrs)))

out = {
    "期次": "三十六",
    "承接": "二十三期（最小 SU(5) 1e34-1e36 / MSSM 1.376e49 / SO(10) p→ν̄K⁺；Hyper-K ~1.3e35 判决探针 C）",
    "口径": "限制与灵敏度均来自 2025-2026 检索；外推 S∝t 为零本底线性假设（标注，非官方）",
    "现有限制_yr": [{"通道": c, "下界": mp.nstr(l, 4), "来源": s} for c, l, s in limits],
    "理论预测带_yr": [{"模型": m, "下限": mp.nstr(lo, 4), "上限": mp.nstr(hi, 4)} for m, lo, hi in pred],
    "未来灵敏度": {
        "Hyper-K": {"状态": "2026 安装/2027 注水/2028 全规模，186 kton", "p_nuK_10yr": mp.nstr(hk_t10, 4)},
        "JUNO": {"状态": "200 kton·yr，效率 36.9%，本底 0.2 事件", "p_nuK_10yr": mp.nstr(juno_t10, 4),
                 "vs_SK倍数": mp.nstr(juno_t10/mp.mpf("5.9e33"), 4)},
    },
    "判决窗口": [
        "p→e+π0：SK 2.4e34 已排除最小 SU(5) 低端 1e34；Hyper-K 2038 前覆盖 [1e35,1e36]",
        "p→ν̄K⁺（SO(10) 判决探针 C）：JUNO 10 年 9.6e35 覆盖 SO(10) 带 → 2034-2035 前后判决",
        "Hyper-K：2038 触及 1e35；20 年 ~2.6e35 更稳",
        "MSSM 1.376e49 不可达（保持 23 期）",
    ],
    "诚实边界": "灵敏度-时间外推为零本底线性假设；JUNO 9.6e35 为灵敏度（非限制）；Hyper-K 10 年值沿用 23 期官方估算",
}
with open(r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\算法联盟_全维自洽与归一化\数据\标准框架_质子衰变窗口重校36.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("\njson 已写入：标准框架_质子衰变窗口重校36.json")
