# -*- coding: utf-8 -*-
"""追加 V9.15 验证条目（V9-C0050..0057）到 03_claims_v9x.csv（14 列规范）。"""
import csv

P = r"D:\a10\aikjx\code\my_lib\openuft\01_独立体系\S15_空间光速螺旋曲率挠率几何统一场论\V9_四力大统一定稿线\03_claims_v9x.csv"

rows = list(csv.DictReader(open(P, encoding="utf-8-sig")))
print("before: n=%d last_id=%s cols=%d" % (len(rows), rows[-1]["claim_id"], len(rows[0])))

NEW = [
    ("V9-C0050", "v9.15-2026-10", "A1 双射复算：(ρ,b)→(m,α) 局部双射（det J=−m/ρ²≠0）；e⁻ ρ=386.149 fm、b=2.81787 fm、m 复现偏差 2.2e-16——2 连续 DOF ↔ 2 独立连续观测恰好匹配", "2.7,17", "全书第二十一章", "", "", "", "", "05_验证结果/tuft_v103_scale_attack_results.json", "", "数值验证", "O", "verified"),
    ("V9-C0051", "v9.15-2026-10", "矛盾确认：q_EM=√α·Z=√(b/ρ)·Z 是 q 与 (ρ,b) 的绑定式（√(b/ρ)=0.0854245=√α）——V9.11 C 组『q 无几何方程约束』与 3.3 定义式直接矛盾", "3.3,17", "全书第二十一章", "", "", "", "", "05_验证结果/tuft_v103_scale_attack_results.json", "", "解析对照", "O", "verified"),
    ("V9-C0052", "v9.15-2026-10", "计数修复：连续自由度不欠定（2↔2）；B03 计数层佐证改为外输清单计数（√α 数值(B02)、Z 量子化、g_W、α_s、m_P）而非『欠定度≥1』；B03 FAIL 维持", "B03,17", "全书第二十一章", "", "", "", "", "05_验证结果/tuft_v103_scale_attack_results.json", "", "判定", "O", "verified"),
    ("V9-C0053", "v9.15-2026-10", "π 介子力程口径统一：π⁰ λ=1.4619 fm vs π± λ=1.4138 fm 相对偏差 3.3%——统一 π⁰ 口径（与 4.4/第十一章一致）；V9.12 表需标注粒子种类", "4.4,18", "全书第二十一章", "", "", "", "", "05_验证结果/tuft_v103_scale_attack_results.json", "", "复算", "O", "verified"),
    ("V9-C0054", "v9.15-2026-10", "尺度冲突：螺旋半径 ρ_e=3.86e-13 m vs 电子半径上界 r_e<2.8e-19 m（LEP Bhabha 95% CL, arXiv 2506.02450）比值 1.38e6（6.1 个数量级）", "1.1,2.7", "全书第二十一章", "", "", "", "", "05_验证结果/tuft_v103_scale_attack_results.json", "", "文献对照+数值", "O", "verified"),
    ("V9-C0055", "v9.15-2026-10", "形状因子偏离（电荷延展读法）：F≈1−⟨r²⟩q²/(6ħ²c²)，q=0.511 MeV（=m_e c²=ħc/ρ_e 数学必然）处偏离 16.7%、q=0.05 MeV 处 0.16%——MeV 级散射即可排除", "1.1,2.7", "全书第二十一章", "", "", "", "", "05_验证结果/tuft_v103_scale_attack_results.json", "", "模型估算", "O", "verified"),
    ("V9-C0056", "v9.15-2026-10", "Hopf 对照：康普顿尺度结构需拓扑保护 G_E=1+O(10⁻¹⁴) 方不被电形状因子排除（磁通道 0.52 MeV 显形）；TUFT 无等价保护机制（B03 无数值内容）——冲突非琐碎", "B03", "全书第二十一章", "", "", "", "", "05_验证结果/tuft_v103_scale_attack_results.json", "", "文献对照", "O", "verified"),
    ("V9-C0057", "v9.15-2026-10", "公设语义二选一：(a) 空间延展读法→观测冲突（FAIL 级，需新机制）；(b) 参数字典读法（V9.11 现行）→公设失去空间几何内容——不新增 FAIL、不撤销判定；攻破首次到达公设源头", "1.1,17.4", "全书第二十一章", "", "", "", "", "05_验证结果/tuft_v103_scale_attack_results.json", "", "判定", "O", "verified"),
]

with open(P, "a", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    for row in NEW:
        w.writerow(row)

rows2 = list(csv.DictReader(open(P, encoding="utf-8-sig")))
print("after: n=%d last_id=%s cols_ok=%s" % (len(rows2), rows2[-1]["claim_id"], len(rows2[0]) == 14))
