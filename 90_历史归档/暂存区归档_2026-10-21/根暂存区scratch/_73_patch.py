# -*- coding: utf-8 -*-
"""73 卷引擎 H5/B1/B4 段修复（锚点切片替换，规避不可见字符不匹配）。"""
import io

PATH = "D:/a10/aikjx/code/my_lib/openuft/07_统一场方程/73_higgs_stability_calc.py"
src = io.open(PATH, encoding="utf-8").read()

# ---------- 1) H5：注释 + mh_triv 函数整体替换 ----------
a = src.find("    # H5：m_h^triv（平庸性上界）")
b = src.find('    _log("[H5] m_h^triv 扫描+二分 ...")')
assert a != -1 and b != -1 and a < b, (a, b)

new_h5 = '''    # H5：m_h^triv（平庸性上界）
    # 定义：λ 在 M_Pl 以下首次触及非微扰上界 π 的临界 m_h（LO 匹配二圈，
    # 与 H4 Case A 同约定）。
    # 实现：t_cross_np（上穿探测器，见 crossing_up_from_traj）由 None 转非
    # None 的首个 m_h ⇒ 扫描 [148,208]（148 > m_h^crit(A)，其下 λ(M_Pl)<0
    # 永不及 π）步长 5 GeV 取 bracket + 二分 22 步细化。
    # 为什么不用 λ(M_Pl)−π 判据：m_h 超过临界后 Landau 极点掉到 M_Pl 以下，
    # 固定步长 RK4 绕极点把 λ(M_Pl) 甩成巨大值（正负不定）⇒ f 不连续，
    # 端点判据必败（旧版扫描窗 [185,210] 即因此全错位：窗内 λ(M_Pl)−π 恒
    # ≈ +9，真实穿越点在 150–185 之间，旧版报告 INFO/None）。
    def mh_triv(m_t, loop=2, lo=mpf("148"), hi=mpf("208"), step=mpf("5")):
        def has_np(mh):
            return assemble(mh, m_t, None, None, loop, DT)["t_cross_np"] is not None
        m = lo
        prev = has_np(m)
        _log("[H5] 扫描 m_h =", fmt(m), " π上穿存在:", prev)
        while m < hi:
            m_next = m + step
            if m_next > hi:
                m_next = hi
            cur = has_np(m_next)
            _log("[H5] 扫描 m_h =", fmt(m_next), " π上穿存在:", cur)
            if (not prev) and cur:
                a, b = m, m_next
                for _ in range(22):
                    mid = (a + b) / 2
                    if has_np(mid):
                        b = mid
                    else:
                        a = mid
                return (a + b) / 2
            m, prev = m_next, cur
        return None

'''
src = src[:a] + new_h5 + src[b:]

# ---------- 2) H5：triv_A_s + entries 段替换 ----------
a = src.find('    triv_A_s = (f"{fmt(mh_triv_A)} GeV" if mh_triv_A is not None')
b = src.find('                    "INFO"))', a)
assert a != -1 and b != -1, (a, b)
b_end = b + len('                    "INFO"))') + 1

new_h5b = '''    triv_A_s = (f"{fmt(mh_triv_A)} GeV" if mh_triv_A is not None
                else "None（[148,208] 扫描内 λ 未触 π ⇒ LO 匹配窗口内无平庸性上界）")
    entries.append(("H5", "整理",
                    "平庸性/非微扰上界：m_h^triv（λ 在 M_Pl 以下首触 π 的临界 Higgs "
                    "质量，LO 匹配二圈，上穿谓词扫描+二分）；一圈解析双约定"
                    "（y_t=g=0 纯四次型：λ(M_Pl)=π / Landau 极点在 M_Pl）交叉",
                    f"二圈数值: {triv_A_s}；一圈解析(λ=π): {fmt(mh_triv_analytic_pi)} GeV；"
                    f"一圈解析(Landau@M_Pl): {fmt(mh_triv_1loop_analytic)} GeV",
                    "INFO"))
'''
src = src[:a] + new_h5b + src[b_end:]

# ---------- 3) B1：Λ_P 双操作点 ----------
a = src.find('    # B1：双窗')
b = src.find('\n\n', a)
assert a != -1 and b != -1, (a, b)

new_b1 = '''    # B1：双窗
    out_np = assemble(M_H, M_T, None, None, 2, DT)
    lam_P_A = None if out_np["t_cross_np"] is None else exp(out_np["t_cross_np"])
    lam_P_B = None if out_B["t_cross_np"] is None else exp(out_B["t_cross_np"])
    b1_ok = lam_I_A_mp is not None and lam_I_A_mp < M_PL
    entries.append(("B1", "攻破",
                    "SM Higgs 扇区有效场论窗口：下有真空不稳定标度 Λ_I（亚稳），上界需视 m_h 而定；"
                    "作为终极理论不能外推到任意高能",
                    f"Λ_I(A)={fmt(lam_I_A_mp)} GeV、Λ_I(B)={fmt(lam_I_B)} GeV；"
                    f"Λ_P(λ=π)：A={fmt(lam_P_A)}、B={fmt(lam_P_B)} GeV"
                    f"（当前 m_h 下均不存在 ⇒ 只有下窗；H5 给出其上界临界质量）",
                    "FAIL" if b1_ok else "PASS"))'''
src = src[:a] + new_b1 + src[b:]

# ---------- 4) B2：双操作点 σ ----------
a = src.find('    # B2：输入敏感度')
b = src.find('\n\n', a)
assert a != -1 and b != -1, (a, b)

new_b2 = '''    # B2：输入敏感度（双操作点；头条 Case B 定 verdict）
    # 阈值 0.2 dex ≅ 因子 1.6：输入涂抹若达此量级，则「Λ_I 处于 10^9–10^10」
    # 的位次声明不再由输入精度担保，须与匹配系统差（B3）合并解读（声明式阈值）。
    b2_ok = sig_B > mpf("0.2")
    entries.append(("B2", "攻破",
                    "不稳定标度的输入依赖：仅输入不确定度即使 log10 Λ_I 涂抹 ±σ"
                    "（一阶传播，中心差导数；Case A/B 双操作点——脆弱性本身随匹配"
                    "约定而变，与 B3 咬合）",
                    f"σ(log10 Λ_I)：Case B={fmt(sig_B, 4)} dex（m_h:{fmt(sig_mh_B, 4)}, "
                    f"m_t:{fmt(sig_mt_B, 4)}, α₃:{fmt(sig_a3_B, 4)}）；"
                    f"Case A={fmt(sig_A, 4)} dex（m_h:{fmt(sig_mh_A, 4)}, m_t:{fmt(sig_mt_A, 4)}, "
                    f"α₃:{fmt(sig_a3_A, 4)}）",
                    "FAIL" if b2_ok else "PASS"))'''
src = src[:a] + new_b2 + src[b:]

# ---------- 5) B4：Λ_QCD 全精度（70 卷机读值） ----------
old_lam_qcd = src[src.find('    lam_qcd = '):src.find('    lam_qcd = ') + 120]
assert '0.2262' in old_lam_qcd, old_lam_qcd
src = src.replace('    lam_qcd = mpf("0.2262")  # 70 卷 Λ_QCD 二圈读数（跨卷引用，注明出处）',
                  '    lam_qcd = mpf("0.22623372")  # 70 卷 Λ_QCD 二圈机读值（跨卷引用，注明出处）')

io.open(PATH, "w", encoding="utf-8").write(src)
print("OK  all replacements applied")
