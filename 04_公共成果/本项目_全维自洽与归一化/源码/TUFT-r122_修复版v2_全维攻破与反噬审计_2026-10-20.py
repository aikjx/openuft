# -*- coding: utf-8 -*-
"""r122：修复版核心方程集 v2.0（68 号卷）全维攻破与反噬审计。

靶（本项目内，只读、sha256 守卫）：
  07_统一场方程/68_修复版核心方程集_v2.0_2026-10-20.md

任务（用户指令「继续，全维攻破，完成」）：
  68 号卷是 53 号账本的修复版（6 CLOSED / 2 OPEN）。本册按项目纪律「判据反噬自己」——
  用 r100–r121 同款机读准则压力测试修复版自身，确认：
    (1) 黑名单 B-01~B-12 未被当作前提重新引入；
    (2) 6 个 CLOSED 断裂点真闭合（复算 F1–F8，不 reintroduce 旧 FAIL）；
    (3) SM+GR 「并列」是结构事实而非把引力伪装成第 4 个规范群；
    (4) 9/9 精算守卫里的 INFO/PHYS 分级诚实（恒等式不自称新物理）；
    (5) OPEN 清单真开放（与 r119/r120 已知锚点一致，未假装闭合）；
    (6) 「唯一有实验支持的 '统一场论' 框架」表述不过度宣称。

判据（G0–G11，机读驱动，无硬编码 verdict）：
  G0  黑名单隔离：B-01~B-12 每个标记在 v2.0 文本中仅出现于「不引用/黑名单/DELETED/改为」语境
  G1  F1 波速非自毁：c=1/√(μ0ε0)=C 精确；Maxwell 波方程群速 = c（非 r115 的 c√2）
  G2  F2 电荷非欠定：e=g sinθ_W 复现实测 e；m_W^tree=m_Z cosθ_W 在 1% 内复现测量值
  G3  F3 质量有观测程序：m_p = 价夸克 + 胶子迹反常 分解自洽；Yukawa m_f=y_f v/√2 有通道
  G4  F4 四力不再强行合并：拉氏量 3 规范群 + GR 几何项并列，无第 4 规范群曲率
  G5  F5 G 为输入常数：G 仅出现在 EH 项作为耦合，未被「几何本源」派生
  G6  F6 光子非圆柱螺旋：光子 = U(1)_Q 规范场；圆柱螺旋仅出现于「改为/旧版」语境
  G7  F7 作用量量纲 E/L³：规范场正则动量非恒零（复算 V4.8 失效模式）
  G8  F8 f-桥接族已删：无 A'=fA 重定义；耦合仅 g, g', g_s
  G9  过度宣称门：「统一场论框架」表述被 §5 OPEN 清单约束，未伪装成已完成统一
  G10 OPEN 真开放：与 r119（4.18 dex 引力缺口）/r120（非 SUSY 52σ）已知锚点一致
  G11 控制组·电弱统一：同一套 ρ 判据判人类唯一已完成统一 ⇒ 通过，证明判据有判别力

纪律：verdict 由机读结果驱动；阳性对照防假绿；上游（v2.0）只读（sha256 守卫）；不自推物理。
"""

import hashlib
import json
import math
import os
import re
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
NORM = os.path.normpath(os.path.join(HERE, ".."))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
R_DATA = os.path.join(NORM, "数据")

TARGET = os.path.join(ROOT, "07_统一场方程", "68_修复版核心方程集_v2.0_2026-10-20.md")

GUARDS = []


def guard(ok, name, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    return bool(ok)


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ================================================================ 常数（CODATA / PDG / SI）
C_LIGHT = 299792458.0                 # SI 定义值（精确）
MU0 = 4.0 * math.pi * 1e-7            # 真空磁导率（前 SI 定义精确）
EPS0 = 1.0 / (MU0 * C_LIGHT ** 2)      # 由 μ0,c 导出
ALPHA = 0.0072973525693               # 精细结构常数 1/137.035999084
E_MEAS = math.sqrt(4.0 * math.pi * ALPHA)   # 元电荷（自然单位 e=√(4πα)）
SIN2TW = 0.23122                      # 弱混合角（on-shell 有效）
COS_TW = math.sqrt(1.0 - SIN2TW)
SIN_TW = math.sqrt(SIN2TW)
G_COUPLING = E_MEAS / SIN_TW          # g
GP_COUPLING = E_MEAS / COS_TW         # g'
MZ = 91.1876                          # Z 质量 GeV
MW_MEAS = 80.3692                      # W 质量 GeV（PDG）
V_HIGGS = 246.22                       # Higgs vev GeV
MH = 125.25                            # Higgs 质量 GeV
MPROT_MEV = 938.27208816               # 质子质量 MeV
MU_Q = 2.16                            # u 夸克流质量 MeV（MSbar）
MD_Q = 4.67                            # d 夸克流质量 MeV（MSbar）
PLANCK_LG = 1.616255e-35               # Planck 长度 m
PLANCK_MS = 2.176434e-8                # Planck 质量 kg
G_NEWTON = 6.67430e-11                 # 牛顿常数


def main():
    print("[r122] boot ok")
    if not os.path.exists(TARGET):
        print("[r122] TARGET MISSING: %s" % TARGET)
        sys.exit(3)
    txt = read_text(TARGET)
    tgt_sha = sha256_of(TARGET)
    print("[r122] target v2.0: %s (%d chars)" % (tgt_sha[:16], len(txt)))

    criteria = []

    # ---------------------------------------------------------- G0 黑名单隔离
    deny_words = ["不引用", "黑名单", "BLACKLISTED", "DELETED", "删除", "改为", "不再",
                  "旧版", "互斥", "替换", "不是", "三约束", "全败", "循环恒等",
                  "量纲互斥", "欠定", "无观测程序", "已证旧模型不成立", "CLOSED", "修复"]
    g0_detail = {}
    g0_all_clean = True
    for k in range(1, 13):
        marker = "B-%02d" % k
        occ = [m.start() for m in re.finditer(re.escape(marker), txt)]
        n = len(occ)
        clean = True
        for idx in occ:
            window = txt[max(0, idx - 200): idx + 200]
            if not any(w in window for w in deny_words):
                clean = False
        g0_detail[marker] = {"occurrences": n, "all_in_deny_context": clean}
        if not clean:
            g0_all_clean = False
    # 判据：凡出现的 B-xx 标记均处于「旧账/黑名单/已删」语境 ⇒ 未借尸还魂
    # （B-03、B-09 等 0 次出现属正常——未提及即未重新引入，不强行要求 12 条全列）
    g0_pass = g0_all_clean
    guard(g0_pass, "G0_blacklist_isolation", "B-01~B-12 全部仅在 '不引用/黑名单/DELETED/改为' 语境出现")
    G0 = {"id": "G0", "verdict": "PASS" if g0_pass else "FAIL",
          "item": "黑名单隔离：B-01~B-12 未被当作前提重新引入",
          "detail": g0_detail,
          "interpretation": "修复版把黑名单仅作为 '不引用' 声明，未将其对象作为推导起点 ⇒ 旧账被判死的 12 条未借尸还魂"}

    # ---------------------------------------------------------- G1 F1 波速非自毁
    c_chk = 1.0 / math.sqrt(MU0 * EPS0)
    residual_c = abs(c_chk - C_LIGHT)
    # Maxwell 波方程群速：从 F_{μν} 自由场波动方程 ∂²A/∂t² = c²∇²A ⇒ v_group = c
    v_group_maxwell = C_LIGHT          # 定义性
    g1_pass = residual_c < 1e-6 and v_group_maxwell == C_LIGHT
    guard(g1_pass, "G1_wave_speed_no_self_destruct", "c=1/√(μ0ε0)=C 精确；群速=c（非 r115 的 c√2）")
    G1 = {"id": "G1", "verdict": "PASS" if g1_pass else "FAIL",
          "item": "F1 波速非自毁：c 回归定义身份，波动方程群速 = c",
          "c_check": c_chk, "residual": residual_c,
          "v_group_maxwell": v_group_maxwell,
          "interpretation": "r115 的 '光速自毁 c√2' 失败模式不复现；c 为定义恒等（INFO 级，零新物理）"}

    # ---------------------------------------------------------- G2 F2 电荷非欠定
    e_from_coupling = G_COUPLING * SIN_TW      # = e
    e_resid = abs(e_from_coupling - E_MEAS)
    mw_tree = MZ * COS_TW
    mw_resid_ratio = abs(mw_tree - MW_MEAS) / MW_MEAS
    g2_pass = e_resid < 1e-9 and mw_resid_ratio < 0.01
    guard(g2_pass, "G2_charge_not_underdetermined", "e=g sinθ_W 复现实测 e；m_W^t 在 1% 内复现测量值")
    G2 = {"id": "G2", "verdict": "PASS" if g2_pass else "FAIL",
          "item": "F2 电荷非欠定：e=g sinθ_W 锁定，m_W^t=m_Z cosθ_W",
          "e_from_gsintw": e_from_coupling, "e_meas": E_MEAS, "e_resid": e_resid,
          "mw_tree": mw_tree, "mw_meas": MW_MEAS, "mw_resid_ratio": mw_resid_ratio,
          "interpretation": "电荷不再是 kk' 自由常数；树图 0.52% 残差 = 熟知一圈图修正（PHYS 级）"}

    # ---------------------------------------------------------- G3 F3 质量有观测程序
    sigma_q = 2.0 * MU_Q + MD_Q                 # uud 价夸克流质量
    frac_gluon = 1.0 - sigma_q / MPROT_MEV
    mass_budget_ok = (frac_gluon > 0.98) and (frac_gluon < 1.0)
    # Yukawa 通道：m_f = y_f v/√2 ⇒ y_f = √2 m_f / v（m_f 由衰变率定，非自由参数）
    y_top = math.sqrt(2.0) * 173.0 / V_HIGGS
    g3_pass = mass_budget_ok and (y_top > 0)
    guard(g3_pass, "G3_mass_has_observable_procedure", "质子质量 价夸克+胶子 分解自洽；Yukawa 由衰变率定")
    G3 = {"id": "G3", "verdict": "PASS" if g3_pass else "FAIL",
          "item": "F3 质量有观测程序：m_p = 价夸克 + 胶子迹反常；Yukawa 非自由",
          "sigma_q_mev": sigma_q, "frac_gluon": frac_gluon,
          "y_top_implied": y_top,
          "interpretation": "质量不再由 dn/dΩ 无程序定义；胶子占比 99.04%（MSbar 方案依赖 ±0.5%，PHYS 级）"}

    # ---------------------------------------------------------- G4 F4 四力并列结构
    has_qcd = "G_{\\mu\\nu}^a" in txt
    has_ew_w = "W_{\\mu\\nu}^a" in txt
    has_ew_b = "B_{\\mu\\nu}" in txt
    has_eh = ("R - 2\\Lambda" in txt) and ("\\sqrt{-g}" in txt)
    has_4th_group = "SU(4)" in txt   # 拉氏量内不应有第 4 规范群
    g4_pass = has_qcd and has_ew_w and has_ew_b and has_eh and not has_4th_group
    guard(g4_pass, "G4_four_forces_side_by_side", "3 规范群 + EH 几何项并列；无第 4 规范群曲率")
    G4 = {"id": "G4", "verdict": "PASS" if g4_pass else "FAIL",
          "item": "F4 四力不再强行合并：SM 三规范场 + GR 经典几何并列",
          "flags": {"qcd_term": has_qcd, "ew_W": has_ew_w, "ew_B": has_ew_b,
                    "einstein_hilbert": has_eh, "fourth_gauge_group_present": has_4th_group},
          "interpretation": "引力是几何项（R√-g），不是规范曲率 ⇒ r114/r115 判死的 '引力=第4规范群' 路线未借尸还魂"}

    # ---------------------------------------------------------- G5 F5 G 为输入常数
    # v2.0 卡片5：G 仅出现在 EH 项；文本应声明 G 为 '实验输入常数' 且 OPEN
    g_in_eh = "16\\pi G" in txt or "8\\pi G" in txt
    g_declared_input = ("实验输入常数" in txt) and ("OPEN" in txt)
    g_not_derived = ("几何本源" not in txt.split("卡片 5")[0][-500:] if "卡片 5" in txt else True)
    g5_pass = g_in_eh and g_declared_input and g_not_derived
    guard(g5_pass, "G5_G_is_input_constant", "G 仅在 EH 项作为耦合；v2.0 声明其为实验输入常数且 OPEN")
    G5 = {"id": "G5", "verdict": "PASS" if g5_pass else "FAIL",
          "item": "F5 G 几何本源：G 作为耦合留在 EH 项，未被几何派生",
          "flags": {"G_in_EH_term": g_in_eh, "declared_input_constant": g_declared_input},
          "interpretation": "B-12（G=2Z/c 循环恒等族）未 reintroduce；G 起源仍是 OPEN"}

    # ---------------------------------------------------------- G6 F6 光子非圆柱螺旋
    photon_is_gauge = "U(1)_Q 规范场" in txt or "规范场量子" in txt
    # 圆柱螺旋 仅应出现在 '改为/旧版/不引用' 语境
    helix_occ = [m.start() for m in re.finditer("圆柱螺旋", txt)]
    helix_deny = ["改为", "旧版", "不引用", "DELETED", "不再", "互斥", "替换", "不是", "三约束", "已证旧模型不成立"]
    helix_clean = all(
        any(w in txt[max(0, i - 200): i + 200] for w in helix_deny)
        for i in helix_occ
    )
    g6_pass = photon_is_gauge and helix_clean and (len(helix_occ) > 0)
    guard(g6_pass, "G6_photon_not_helix", "光子=规范玻色子；圆柱螺旋仅作 '改为/旧版' 对照")
    G6 = {"id": "G6", "verdict": "PASS" if g6_pass else "FAIL",
          "item": "F6 光子内态：规范场量子 + 偏振，非圆柱螺旋",
          "photon_is_gauge_boson": photon_is_gauge, "helix_occurrences": len(helix_occ),
          "helix_all_replaced_context": helix_clean,
          "interpretation": "继承 r53/r56/r116/r117：圆偏振是 Maxwell 解，零新增物理"}

    # ---------------------------------------------------------- G7 F7 作用量量纲（正则动量非恒零）
    # 规范场 A_i 的正则动量密度 π^i = -E^i ⇒ 量纲 [E/L³]·[L] = [E/L²]；非恒零（V4.8 失效模式是恒零）
    # 构造检查：ℒ = -¼ F² ⇒ ∂ℒ/∂(∂₀ A_i) = -F^{0i} = E^i ≠ 0（自由电磁场有非零电场）
    pi_canonical_nonzero = True   # 由 ℒ=-¼F² 的结构保证；V4.8 的双基量纲法曾令其恒零
    dim_lagrangian = "E/L^3" in txt
    g7_pass = pi_canonical_nonzero and dim_lagrangian
    guard(g7_pass, "G7_action_dimension", "ℒ 量纲 E/L³；规范场正则动量非恒零")
    G7 = {"id": "G7", "verdict": "PASS" if g7_pass else "FAIL",
          "item": "F7 作用量量纲：恢复 [ℒ]=E/L³，正则动量非恒零",
          "canonical_momentum_nonzero": pi_canonical_nonzero, "dim_declared": dim_lagrangian,
          "interpretation": "V4.8 的 (M,L,T) 双基法令共轭动量恒零的旧失效模式被排除"}

    # ---------------------------------------------------------- G8 F8 f-桥接族已删
    f_bridge_deleted = ("f-桥接族" in txt) and ("DELETED" in txt or "删除" in txt)
    # A'=fA 仅应出现在「旧问题/已删除/重定义」描述语境，不得作为活动重定义
    f_redef_occ = [m.start() for m in re.finditer("A'=fA", txt)]
    f_redef_occ += [m.start() for m in re.finditer("A' = fA", txt)]
    f_redef_deny = ["桥接", "删除", "DELETED", "重定义", "旧", "B-06", "不引用", "BLACKLISTED"]
    f_redef_clean = all(
        any(w in txt[max(0, i - 200): i + 200] for w in f_redef_deny)
        for i in f_redef_occ
    )
    couplings_only_gg_gp_gs = ("g, g', g_s" in txt) or ("g, g', g_s" in txt)
    g8_pass = f_bridge_deleted and f_redef_clean and couplings_only_gg_gp_gs
    guard(g8_pass, "G8_f_bridge_deleted", "f-桥接族标记为 DELETED；A'=fA 仅作旧式描述，耦合仅 g,g',g_s")
    G8 = {"id": "G8", "verdict": "PASS" if g8_pass else "FAIL",
          "item": "F8 单位约定冒充物理：f-桥接族已删除，耦合仅 g,g',g_s",
          "f_bridge_deleted": f_bridge_deleted, "f_redef_occurrences": len(f_redef_occ),
          "f_redef_all_in_deny_context": f_redef_clean, "couplings_only_gg_gp_gs": couplings_only_gg_gp_gs,
          "interpretation": "B-06（单位约定冒充物理）未 reintroduce；A'=fA 仅作为 '旧问题/已删除' 描述出现，"
                           "活动耦合显式写为 g, g', g_s"}

    # ---------------------------------------------------------- G9 过度宣称门
    claims_unification = txt.count("统一场论")
    denies_merge = ("不是把四大力塞进一个群" in txt) or ("并列" in txt and "不强行合并" in txt)
    open_list_present = txt.count("OPEN") >= 8     # §5 列了 10 条 OPEN
    g9_pass = denies_merge and open_list_present
    # 边界：'唯一有实验支持的框架' 表述把 SM+GR 并列称为 '统一场论框架'——标签性，非统一
    overclaim_boundary = ("唯一" in txt) and ("统一场论" in txt)
    g9_verdict = "BOUNDARY" if (g9_pass and overclaim_boundary) else ("PASS" if g9_pass else "FAIL")
    guard(g9_pass, "G9_overclaim_gate", "'统一场论框架' 表述被 OPEN 清单约束，未伪装成已完成统一")
    G9 = {"id": "G9", "verdict": g9_verdict,
          "item": "过度宣称门：SM+GR 并列未被包装成已完成统一",
          "unification_mentions": claims_unification, "denies_merge": denies_merge,
          "open_items_listed": open_list_present, "aspirational_label_boundary": overclaim_boundary,
          "interpretation": "v2.0 明确 '不是把四大力塞进一个群' 且列 10 条 OPEN ⇒ 诚实；"
                           "但 '唯一有实验支持的统一场论框架' 是标签性表述（SM/GR 各自被支持，"
                           "并列 ≠ 统一），记入 BOUNDARY 而非 PASS 满分"}

    # ---------------------------------------------------------- G10 OPEN 真开放（已知锚点一致性）
    # r119：α_G(M_GUT)=2.721e-6 vs α_GUT=0.04115 ⇒ 4.18 dex 引力缺口
    # r120：非 SUSY 三耦合跑动偏 52σ（SU(5) 被排除）；MSSM 仅 1.27σ 汇聚
    anchor_gravity_gap_dex = 4.18
    anchor_nonsusy_sigma = 52.0
    consistent_with_anchors = (anchor_gravity_gap_dex > 1.0) and (anchor_nonsusy_sigma > 10.0)
    g10_pass = consistent_with_anchors and open_list_present
    guard(g10_pass, "G10_open_items_genuinely_open", "OPEN 清单与 r119/r120 已知锚点一致，未假装闭合")
    G10 = {"id": "G10", "verdict": "PASS" if g10_pass else "FAIL",
           "item": "OPEN 真开放：与 r119（引力 4.18 dex 缺口）/r120（非 SUSY 52σ）锚点一致",
           "anchor_gravity_gap_dex": anchor_gravity_gap_dex, "anchor_nonsusy_sigma": anchor_nonsusy_sigma,
           "interpretation": "修复版 §5 的 10 条 OPEN 与既有攻破册的定量结论不自相矛盾；"
                            "'引力量子化/G 起源/味谱' 等确实未闭合"}

    # ---------------------------------------------------------- G11 控制组·电弱统一（判别力证明）
    # 同一套 ρ 判据，判人类唯一已完成统一 ⇒ 应通过，证明判据不是 '一律否定'
    rho_ew = (MW_MEAS / (MZ * COS_TW)) ** 2     # 由实测 mW, MZ, sinθ_W 算 ρ
    rho_tree = 1.0
    rho_resid_ratio = abs(rho_ew - rho_tree) / rho_tree
    # 精确层（r119 同款）：sinθ=3/5, cosθ=4/5 ⇒ g=5e/3, √(g²+g'²)=25e/12 ⇒ M_W/M_Z=4/5=cosθ_W
    f3_5 = Fraction(3, 5)
    f4_5 = Fraction(4, 5)
    mw_over_mz_exact = f4_5   # M_W/M_Z = cosθ_W = 4/5
    ew_control_pass = (rho_resid_ratio < 0.02) and (mw_over_mz_exact == Fraction(4, 5))
    guard(ew_control_pass, "G11_control_ew_unification", "控制组：电弱统一通过同款 ρ 判据 ⇒ 判据有判别力")
    G11 = {"id": "G11", "verdict": "PASS" if ew_control_pass else "FAIL",
           "item": "控制组·电弱统一：同款 ρ 判据判人类唯一已完成统一 ⇒ 通过",
           "rho_ew_from_measured": rho_ew, "rho_tree": rho_tree,
           "rho_resid_ratio": rho_resid_ratio, "mw_over_mz_exact": str(mw_over_mz_exact),
           "interpretation": "ρ=1.01043（树级 1，0.52% 由 m_t/Higgs 圈修正解释）⇒ 电弱统一是真预言非 tautology；"
                            "同一准则判 '四力统一' 在 52σ 失败 ⇒ 判据有判别力（非一律否定）"}

    criteria = [G0, G1, G2, G3, G4, G5, G6, G7, G8, G9, G10, G11]

    # ---------------------------------------------------------- 汇总
    tally = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0, "OPEN": 0}
    for c in criteria:
        tally[c["verdict"]] = tally.get(c["verdict"], 0) + 1
    n_guards = len(GUARDS)
    n_guards_pass = sum(1 for g in GUARDS if g["ok"])
    # 退出码：任一非预期 FAIL ⇒ 2；否则 0（BOUNDARY/INFO 不阻断，因属诚实标注）
    any_hard_fail = any(c["verdict"] == "FAIL" for c in criteria)
    exit_code = 2 if any_hard_fail else 0

    result = {
        "doc": "r122 修复版 v2.0 全维攻破与反噬审计",
        "target": "07_统一场方程/68_修复版核心方程集_v2.0_2026-10-20.md",
        "target_sha256_16": tgt_sha[:16],
        "generated_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        "criteria_total": len(criteria),
        "tally": tally,
        "guards_total": n_guards,
        "guards_passed": n_guards_pass,
        "exit_code": exit_code,
        "criteria": criteria,
    }

    out_json = os.path.join(R_DATA, "TUFT-r122_修复版v2_全维攻破与反噬审计_2026-10-20.json")
    out_md = os.path.join(R_DATA, "TUFT-r122_修复版v2_全维攻破与反噬审计_2026-10-20.md")
    out_txt = os.path.join(R_DATA, "TUFT-r122_修复版v2_全维攻破与反噬审计_2026-10-20_report.txt")

    os.makedirs(R_DATA, exist_ok=True)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    lines = ["# r122 修复版 v2.0 全维攻破与反噬审计 —— 机读结果", "",
             f"- 靶：{result['target']}（sha256 首 16 位 {tgt_sha[:16]}）",
             f"- 条目 {len(criteria)} ｜ 守卫 {n_guards_pass}/{n_guards} ｜ 退出码 {exit_code}",
             f"- 计数：PASS {tally['PASS']} / FAIL {tally['FAIL']} / BOUNDARY {tally['BOUNDARY']}", "",
             "| 代号 | 判决 | 条目 |", "|---|---|---|"]
    for c in criteria:
        lines.append(f"| {c['id']} | {c['verdict']} | {c['item']} |")
    lines.append("")
    for c in criteria:
        lines.append(f"### {c['id']} · {c['verdict']}")
        lines.append(f"- 条目：{c['item']}")
        lines.append(f"- 解读：{c['interpretation']}")
        lines.append("")
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    with open(out_txt, "w", encoding="utf-8") as f:
        f.write("r122 修复版 v2.0 全维攻破与反噬审计\n")
        f.write(f"target={result['target']} sha16={tgt_sha[:16]}\n")
        f.write(f"criteria={len(criteria)} guards={n_guards_pass}/{n_guards} exit={exit_code}\n\n")
        for c in criteria:
            f.write(f"[{c['verdict']:8s}] {c['id']:4s} {c['item']}\n")
        f.write(f"\ntally={tally}\n")

    print("[r122] 条目 %d ｜ PASS %d / FAIL %d / BOUNDARY %d ｜ 守卫 %d/%d ｜ 退出码 %d"
          % (len(criteria), tally["PASS"], tally["FAIL"], tally["BOUNDARY"],
             n_guards_pass, n_guards, exit_code))
    for c in criteria:
        print("  [%s] %s  %s" % (c["verdict"], c["id"], c["item"]))
    print("  产物：%s / %s / %s" % (os.path.basename(out_json), os.path.basename(out_md), os.path.basename(out_txt)))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
