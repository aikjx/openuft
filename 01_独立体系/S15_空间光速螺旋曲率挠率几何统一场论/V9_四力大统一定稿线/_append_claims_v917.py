# -*- coding: utf-8 -*-
"""追加 V9.17 验证条目（V9-C0058..0064）到 03_claims_v9x.csv（14 列规范）。"""
import csv

P = r"D:\a10\aikjx\code\my_lib\openuft\01_独立体系\S15_空间光速螺旋曲率挠率几何统一场论\V9_四力大统一定稿线\03_claims_v9x.csv"

rows = list(csv.DictReader(open(P, encoding="utf-8-sig")))
print("before: n=%d last_id=%s cols=%d" % (len(rows), rows[-1]["claim_id"], len(rows[0])))

NEW = [
    ("V9-C0058", "v9.17-2026-10", "四力本源参数 (λ,q,s) 首次全数值化：引力 q_G=m/m_P=7.69e-20（质子）、电磁 q_EM=√α=0.0854、弱力 q_W=0.0651（G_F 体积分匹配导出）、剩余强力 q_π=0.0204（OPE 中心势系数口径）", "3.3,9,23", "全书第二十三章", "", "", "", "", "05_验证结果/tuft_v104_force_origin_audit_results.json", "", "数值验证", "O", "verified"),
    ("V9-C0059", "v9.17-2026-10", "弱力荷导出：q_W²=G_F·m_W²/(4π√2)=0.004240（∫V_W d³r=∫V_F d³r 体积分匹配，c=ħ=1；G_F=1.1663788e-5 GeV⁻²、m_W=80.377 GeV）——参数字典匹配，G_F 外输（B03 维持）", "23.2", "全书第二十三章", "", "", "", "", "05_验证结果/tuft_v104_force_origin_audit_results.json", "", "解析推导", "O", "verified"),
    ("V9-C0060", "v9.17-2026-10", "强力荷导出：q_π²=f²(m_π/2m_p)²=4.147e-4（OPE 中心势系数 f²(m_π/2M)²ħc=0.0818 MeV·fm 口径，与全书 9.8/V9.12 一致；4π 前因子定义 q_π=0.072 为口径差异）——f² 外输（B03）", "23.2,9.8", "全书第二十三章", "", "", "", "", "05_验证结果/tuft_v104_force_origin_audit_results.json", "", "解析推导", "O", "verified"),
    ("V9-C0061", "v9.17-2026-10", "结构事实：q_W≈q_EM 同量级（0.0651 vs 0.0854）——弱电统一『g≈e』直觉在参数模板层重现（SM g=e/sinθ_W≈0.64 定义不同，仅量级对照）", "23.3", "全书第二十三章", "", "", "", "", "05_验证结果/tuft_v104_force_origin_audit_results.json", "", "结构对照", "O", "verified"),
    ("V9-C0062", "v9.17-2026-10", "荷层级 q_EM>q_W>q_π≫q_G；引力之弱=荷比平方：q_EM/q_G=1.11e18 ⇒ F_E/F_G=1.2356e36（复核）", "23.3,4.6", "全书第二十三章", "", "", "", "", "05_验证结果/tuft_v104_force_origin_audit_results.json", "", "数值验证", "O", "verified"),
    ("V9-C0063", "v9.17-2026-10", "全量纲审计 16/16 PASS：U/F/Proca/汤川/母恒等式/m/ρ/G/V_G/L_z/μ/λ_W/力括号/F̃/禁闭 σ/EC 真空——全书核心方程无量纲断裂（旧审计线 01-23 卷母方程量纲断裂在本线不存在）", "全书,23.4", "全书第二十三章", "", "", "", "", "05_验证结果/tuft_v104_force_origin_audit_results.json", "", "量纲审计", "O", "verified"),
    ("V9-C0064", "v9.17-2026-10", "微观 6 粒子+宏观 7 项属性复算：电子 ρ=386.149 fm、质子 ρ=0.2103 fm、π⁰ λ=1.4619 fm、W 2.455e-3、Z 2.164e-3、H 1.575e-3 fm；m_P/G/F_E-F_G/EC≡GR/EHT/GW/g 因子——全部与全书一致", "23.5", "全书第二十三章", "", "", "", "", "05_验证结果/tuft_v104_force_origin_audit_results.json", "", "复算核对", "O", "verified"),
]

with open(P, "a", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    for row in NEW:
        w.writerow(row)

rows2 = list(csv.DictReader(open(P, encoding="utf-8-sig")))
print("after: n=%d last_id=%s cols_ok=%s" % (len(rows2), rows2[-1]["claim_id"], len(rows2[0]) == 14))
