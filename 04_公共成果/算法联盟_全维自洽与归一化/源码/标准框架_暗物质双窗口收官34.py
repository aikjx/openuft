# -*- coding: utf-8 -*-
"""标准框架·三十四期数值靶：暗物质双窗口收官（WIMP × 轴子，2026 灵敏度地图与判决窗口）
承接二十二期（热遗迹 ⟨σv⟩=2.5e-26；XENONnT 50GeV 2.6e-47；轴子 f_a=1e12↔m_a=5.7μeV、g_aγ(KSVZ)=1.127e-15 GeV⁻¹、ADMX 2.86-4.32 μeV 未探测）。
本期更新（2025-2026 检索）：XENONnT 3.1 t·yr 1.7e-47@30 GeV + 2.73σ CEvNS 指示；LZ 2025 2.2e-48@40 GeV；
ADMX 覆盖扩展至 ~5.4 μeV（1.1-1.31 GHz 达 KSVZ、部分达 DFSZ）。mpmath 250 位。
"""
import mpmath as mp
import json

mp.mp.dps = 250

alpha = mp.mpf("1") / mp.mpf("137.035999084")
pi = mp.pi

# ---- WIMP 窗口（现状排除点，检索来源）----
print("===== 三十四期：暗物质双窗口收官（WIMP × 轴子，2026 版，250 位）=====")
wimp_pts = [
    ("XENONnT 3.1 t·yr（arXiv:2502.18005 / ICRC2025）", mp.mpf("30"), mp.mpf("1.7e-47"), "90% CL，>10 GeV 扫描；含 2.73σ CEvNS 指示"),
    ("LZ 2025（Aalbers et al.，Oxford 摘要）", mp.mpf("40"), mp.mpf("2.2e-48"), "最强 SI 排除；中值灵敏度 5.1e-48"),
]
print("WIMP 直接探测现状（σ_SI，cm²，90% CL）：")
for nm, mchi, sig, note in wimp_pts:
    print("  %-44s m_χ=%.0f GeV | σ_SI=%.2e cm² | %s" % (nm, mchi, sig, note))

# 热遗迹参考带与中微子地板（文献标准值）
print("\n热遗迹参考带（s-wave）：⟨σv⟩=2.2e-26 cm³/s（σ_SI 依赖模型，非唯一预测）")
print("Xe 中微子地板（文献）：最低点 m_χ~6 GeV、σ~2e-48 cm²；m_χ=40 GeV 处 σ~5e-48 cm² 量级")
print("→ LZ 2.2e-48@40 GeV 已进入地板区（需 CEvNS 统计区分，XENONnT 2.73σ 指示即地板信号）")

# ---- 轴子窗口 ----
f_a_ref = mp.mpf("1e12")  # GeV
m_a_ref = mp.mpf("5.691e-6")  # eV，f_a=1e12 GeV 标定（22 期 5.7 μeV）
g_ksvz = mp.mpf("1.127e-15")   # GeV⁻¹ @f_a=1e12（22 期定案，C_γ=0.97 含夸克质量修正）
C_dfsz = mp.mpf("0.72")
g_dfsz = alpha / (2 * pi * f_a_ref) * C_dfsz

print("\n轴子窗口换算（f_a=1e12 GeV 基准）：")
print("  m_a = 5.691 μeV·(1e12 GeV/f_a) | g_aγ(KSVZ)=%.4e GeV⁻¹ | g_aγ(DFSZ)=%.4e GeV⁻¹ (C_γ=0.72)"
      % (g_ksvz, g_dfsz))

admx = [
    ("ADMX 1.1-1.31 GHz（2504.07279，2026）", "4.55-5.42 μeV", "达 KSVZ 灵敏度；最强点 ~5.4 μeV 以下达 DFSZ"),
    ("ADMX 3.3 μeV 段（2408.15227）", "3.27-3.34 μeV", "排除 DFSZ（DFSZ 发现能力）"),
    ("ADMX 1.026-1.045 GHz（2602.05388）", "4.244-4.322 μeV", "上段接近 DFSZ"),
    ("ADMX 运行汇总（PoS 398/180）", "3.3-4.2 / 3.9-4.1 μeV", "排除 KSVZ / DFSZ"),
]
print("ADMX 现状覆盖（2026，检索）：")
for nm, rng, note in admx:
    print("  %-42s %s | %s" % (nm, rng, note))
print("未覆盖大段：<2.8 μeV、5.4-40 μeV（QCD 轴子主窗口仍 open）")

# 未来灵敏度（文献/官方计划）
future = [
    ("ADMX 扩展（2030s 计划）", "~1-40 μeV", "KSVZ 全覆盖、DFSZ 大段覆盖"),
    ("DM Radio-m3（PAR）", "41 neV-0.8 μeV", "KSVZ/DFSZ 灵敏度（低频段）"),
    ("IAXO（太阳轴子）", "g_aγ ~1e-18 GeV⁻¹", "模型无关太阳轴子窗口"),
    ("MADMAX（规划）", "40-400 μeV", "高频段 QCD 轴子"),
    ("XLZD 20t / DARWIN（2030s）", "m_χ 10-100 GeV", "σ_SI 达 ~2-6e-49 cm² → 地板以下 1-2 量级"),
]
print("\n未来判决（2030s-2040s）：")
for nm, rng, note in future:
    print("  %-24s %s | %s" % (nm, rng, note))

# ---- 判决窗口 ----
print("\n===== 双窗口判决 =====")
print("WIMP：2030s XLZD/DARWIN 在地板以上无剩余 → 传统 s-wave 热遗迹 WIMP（σ_SI≥地板）被系统性排除")
print("  剩余存活区：地板以下（不可达）+ 非最小耦合/非 s-wave（p-wave 等）模型依赖区")
print("轴子：2030s ADMX 覆盖 ~1-40 μeV → KSVZ 大段排除、DFSZ 部分排除；>40 μeV 需 MADMAX")
print("双窗口收官判定：2040 年前若无信号，主流热遗迹 WIMP × QCD 轴子（DFSZ/KSVZ）双窗口基本关闭")

out = {
    "期次": "三十四",
    "承接": "二十二期（WIMP 2.6e-47@50GeV；轴子 KSVZ 1.127e-15@1e12；ADMX 2.86-4.32 μeV 未探测）",
    "口径": "现状点值均来自 2025-2026 检索（见各条来源）；换算 mpmath 250 位；热遗迹带/地板为文献标准值",
    "WIMP_现状": [{"实验": n, "m_GeV": mp.nstr(m, 6), "sigma_SI_cm2": mp.nstr(s, 4), "说明": t} for n, m, s, t in wimp_pts],
    "WIMP_参考": {"热遗迹_sv_cm3s": "2.2e-26（s-wave，σ_SI 模型依赖）", "Xe地板": "~6 GeV 处 2e-48；40 GeV 处 ~5e-48 cm² 量级"},
    "轴子_换算": {"m_a_eV_at_1e12": "5.691e-6", "g_aγ_KSVZ_GeV-1": mp.nstr(g_ksvz, 6), "g_aγ_DFSZ_GeV-1": mp.nstr(g_dfsz, 6)},
    "ADMX_现状": [{"段": n, "质量窗": r, "判定": t} for n, r, t in admx],
    "未来_灵敏度": [{"实验": n, "窗口": r, "能力": t} for n, r, t in future],
    "判决": [
        "WIMP：2030s XLZD/DARWIN 地板以上无剩余 → 传统 s-wave 热遗迹 WIMP 系统排除；存活区=地板以下+非最小耦合",
        "轴子：2030s ADMX ~1-40 μeV → KSVZ 大段排除、DFSZ 部分排除；>40 μeV 需 MADMAX",
        "双窗口收官：2040 年前无信号 → 主流热遗迹 WIMP × QCD 轴子双窗口基本关闭",
    ],
    "诚实边界": "σ_SI 排除点为实验公开 90% CL 单点值（非完整曲线）；热遗迹 σ_SI 非唯一预测；DFSZ C_γ=0.72 为文献常用值（±20%）",
}
with open(r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\算法联盟_全维自洽与归一化\数据\标准框架_暗物质双窗口收官34.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("\njson 已写入：标准框架_暗物质双窗口收官34.json")
