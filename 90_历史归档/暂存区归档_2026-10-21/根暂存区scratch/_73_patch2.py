# -*- coding: utf-8 -*-
"""73 卷 B3 三分分解补丁（匹配差 / 输入锚点差 / 合计）+ B1 交叉引用。"""
import io

PATH = "D:/a10/aikjx/code/my_lib/openuft/07_统一场方程/73_higgs_stability_calc.py"
src = io.open(PATH, encoding="utf-8").read()

# ---------- B3 整体重写 ----------
a = src.find("    # B3：匹配/圈阶/方案依赖")
b = src.find("\n\n", a)
assert a != -1 and b != -1, (a, b)

new_b3 = '''    # B3：匹配/圈阶/方案依赖（三分分解：匹配约定差 / 输入锚点差 / 合计）
    # 为什么补测 A_BM（LO 匹配 @ 文献锚点）：原「匹配差」直接相减 A_our 与
    # B_BM，混入了本卷输入与文献锚点的差（本卷 m_t 低 0.77 GeV，单独贡献
    # ~0.9 dex）⇒ 标注为「匹配差」属错标。补测后：
    #   Δ匹配 = B_BM − A_BM（同锚点，只变匹配约定）——真正的匹配系统差；
    #   Δ输入 = A_BM − A_our（同 LO 匹配，只变输入锚点）；
    #   Δ合计 = B_BM − A_our（原读数；两项之和为近似，机读分项如实报告）。
    # m_h^crit 同法分解（A_BM 临界质量：括号二分 [110,150]；该窗内 λ0 均
    # 低于 m_h^triv≈177 ⇒ 无 Landau 绕极，λ(M_Pl) 连续可二分）。
    _log("[B3] A_BM 操作点（LO 匹配 @ 文献锚点）...")
    out_A_BM = assemble(BM_M_H, BM_M_T, None, None, 2, DT)
    lam_I_A_BM = None if out_A_BM["t_cross0"] is None else exp(out_A_BM["t_cross0"])
    mh_crit_A_BM = mh_crit(BM_M_T, lam_lo_bm, y_lo_bm, BM_M_H, 2,
                           mpf("110"), mpf("150"))
    _log("[B3] Λ_I(A_BM) =", fmt(lam_I_A_BM), " m_h^crit(A_BM) =", fmt(mh_crit_A_BM, 6))

    def _lg(x):
        return None if x is None else log(x) / log(10)

    d_lam_match = (abs(_lg(lam_I_B) - _lg(lam_I_A_BM))
                   if (lam_I_B and lam_I_A_BM) else mpf("0"))
    d_lam_inputs = (abs(_lg(lam_I_A_BM) - _lg(lam_I_A_mp))
                    if (lam_I_A_BM and lam_I_A_mp) else mpf("0"))
    d_lamI_dex_AB = (abs(_lg(lam_I_B) - _lg(lam_I_A_mp))
                     if (lam_I_B and lam_I_A_mp) else mpf("0"))
    d_lamI_dex_loop = (abs(_lg(lam_I_B1) - _lg(lam_I_B))
                       if (lam_I_B1 and lam_I_B) else mpf("0"))
    d_crit_match = (abs(mh_crit_A_BM - mh_crit_B)
                    if (mh_crit_A_BM and mh_crit_B) else mpf("0"))
    d_crit_inputs = (abs(mh_crit_A - mh_crit_A_BM)
                     if (mh_crit_A and mh_crit_A_BM) else mpf("0"))
    d_crit = abs(mh_crit_A - mh_crit_B) if (mh_crit_A and mh_crit_B) else mpf("0")
    # 阈值：0.05 dex ≈ 12%（约定差可感知下限）；0.5 GeV（临界质量位移可感知下限）
    b3_ok = (d_lam_match > mpf("0.05") or d_crit_match > mpf("0.5")
             or d_lamI_dex_loop > mpf("0.05"))
    entries.append(("B3", "攻破",
                    "匹配/圈阶/方案依赖：LO 朴素匹配 vs NNLO 匹配的系统差（同锚点隔离）"
                    "＋ 输入锚点差（同匹配隔离）＋ 合计；λ(M_t) 0.12917 vs 0.12604 "
                    "= −1.1%、y_t 0.991 vs 0.940；圈阶差单独量化",
                    f"匹配差（同锚点）Δlog10 Λ_I={fmt(d_lam_match, 4)} dex、"
                    f"Δm_h^crit={fmt(d_crit_match, 4)} GeV；"
                    f"输入锚点差（同匹配）Δlog10 Λ_I={fmt(d_lam_inputs, 4)} dex、"
                    f"Δm_h^crit={fmt(d_crit_inputs, 4)} GeV；"
                    f"合计 Δlog10 Λ_I={fmt(d_lamI_dex_AB, 4)} dex、Δm_h^crit={fmt(d_crit, 4)} GeV；"
                    f"圈阶差(1vs2圈, 同匹配同锚点)={fmt(d_lamI_dex_loop, 4)} dex",
                    "BOUNDARY" if b3_ok else "INFO"))'''
src = src[:a] + new_b3 + src[b:]

# ---------- B1 读数补 m_h^triv 交叉引用 ----------
old_b1_tail = '''                    f"Λ_P(λ=π)：A={fmt(lam_P_A)}、B={fmt(lam_P_B)} GeV"
                    f"（当前 m_h 下均不存在 ⇒ 只有下窗；H5 给出其上界临界质量）",'''
new_b1_tail = '''                    f"Λ_P(λ=π)：A={fmt(lam_P_A)}、B={fmt(lam_P_B)} GeV"
                    f"（当前 m_h 下均不存在 ⇒ 只有下窗；上窗临界质量 m_h^triv(A)="
                    f"{fmt(mh_triv_A)} GeV，见 H5）",'''
assert old_b1_tail in src
src = src.replace(old_b1_tail, new_b1_tail)

io.open(PATH, "w", encoding="utf-8").write(src)
print("OK  B3 decomposition + B1 cross-ref applied")
