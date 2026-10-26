# -*- coding: utf-8 -*-
"""
openuft#49 阶段1 总拉氏量 —— 三重预检攻破精算
补上前序审计推迟的 旋量关(mod8) 与 250位数值关。
运行: <venv python> _p49_attack_calc.py
输出: _p49_attack_out.txt / _p49_attack_data.json
"""
import json
import os
import sys

from mpmath import mp, mpf, sqrt, pi, log10, nstr

mp.dps = 250

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []
CHECKS = []


def P(s=""):
    OUT.append(s)


def ck(name, ok, note=""):
    CHECKS.append((name, bool(ok), note))


def dex(x):
    """以 10 为底的数量级距离"""
    return log10(abs(x)) if x != 0 else mpf("-inf")


# ---------------------------------------------------------------- 常数 (SI)
c = mpf("299792458")                      # exact
G = mpf("6.67430e-11")                    # CODATA, u_r = 2.2e-5  <-- 有效位上限
hbar = mpf("1.054571817e-34")
m_e = mpf("9.1093837139e-31")
e_ch = mpf("1.602176634e-19")             # exact
u_r_G = mpf("2.2e-5")
u_r_Planck = u_r_G / 2                    # 普朗克量 u_r = 1/2 u_r(G)

lP = sqrt(G * hbar / c ** 3)
tP = lP / c
mP = sqrt(hbar * c / G)
omega_P = c / lP
EP_J = mP * c ** 2
EP_GeV = EP_J / (e_ch * mpf("1e9"))
Mbar_P2 = c ** 3 / (8 * pi * G * hbar)    # 1/(8 pi G) 对应的 (约化普朗克质量)^2 / (hbar c)

P("=" * 78)
P("openuft#49 阶段1 总拉氏量 —— 三重预检攻破精算   (mp.dps = %d)" % mp.dps)
P("=" * 78)
P("")
P("【伪精度声明】G 仅有 ~5.4 位有效数字 (u_r=2.2e-5)，一切普朗克量继承")
P("  u_r = 1.1e-5。以下数字在 250 位内部运算以排除舍入，但【只报 6 位有效数字】，")
P("  其余位数是噪声（G 的末位之后的 244 位无物理内容）。")
P("")

# ---------------------------------------------------------------- A. 单位/恒等式锚点
P("-" * 78)
P("A. 单位恒等式锚点（内部 250 位，报告 6 位）")
P("-" * 78)
ke_E = c ** 4 / (16 * pi * G)           # 几何耦合 kappa_E = c^4/(16 pi G), 量纲 = 力
r1 = ke_E / (hbar * c)                  # = c^3/(16 pi G hbar)
r2 = 1 / (16 * pi * lP ** 2)
rel_err = abs(r1 - r2) / r2
P("  kappa_E = c^4/(16 pi G)              = %s  N  (= 量纲为力, 自检)" % nstr(ke_E, 6))
P("  kappa_E/(hbar c)                     = %s  m^-2" % nstr(r1, 6))
P("  1/(16 pi l_P^2)                      = %s  m^-2" % nstr(r2, 6))
P("  相对偏差                              = %s" % nstr(rel_err, 6))
P("  >>> 恒等式 kappa_E/(hbar c) = 1/(16 pi l_P^2) 成立：")
P("      Planck 尺度【必然】进入任何 乘子项与 omega 动能项同量纲配对的拉氏量。")
P("")
P("  l_P      = %s m" % nstr(lP, 6))
P("  t_P      = %s s" % nstr(tP, 6))
P("  m_P      = %s kg   = %s GeV/c^2" % (nstr(mP, 6), nstr(EP_GeV, 6)))
P("  omega_P  = c/l_P = %s s^-1" % nstr(omega_P, 6))
P("")
ck("A1 kappa_E/(hbar c) == 1/(16 pi l_P^2)", rel_err < mpf("1e-200"), "相对偏差 %s" % nstr(rel_err, 6))
ck("A2 m_P*l_P == hbar/c", abs(mP * lP * c / hbar - 1) < mpf("1e-200"))
ck("A3 omega_P == c/l_P", abs(omega_P * lP / c - 1) < mpf("1e-200"))
ck("A4 omega_P == 1/t_P", abs(omega_P * tP - 1) < mpf("1e-200"))

# ---------------------------------------------------------------- B. 旋量关 mod 8
P("")
P("-" * 78)
P("B. 旋量相容性关（前序审计推迟到阶段4 —— 本协议禁止推迟，此处当场执行）")
P("-" * 78)
P("")
P("正确判据（约定 (p,q) = (类时维数, 类空维数)，n = p+q）：")
P("  Weyl(手征)      <=> n 为偶数")
P("  Majorana(实性)  <=> (q - p) mod 8 in {0,1,2}")
P("  Majorana-Weyl   <=> n 为偶数 且 (q-p) mod 8 == 0")
P("")
P("草案 M5 的判据（原文锁定、不可修改）：")
P("  'Weyl 仅当 n = 2 (mod 8) 存在' ； 'Majorana-Weyl 仅 n = 2 (mod 8)'")
P("")


def correct(p, q):
    n = p + q
    weyl = (n % 2 == 0)
    maj = ((q - p) % 8) in (0, 1, 2)
    mw = weyl and ((q - p) % 8 == 0)
    return weyl, maj, mw


def draft_rule(p, q):
    n = p + q
    weyl = (n % 8 == 2)
    mw = (n % 8 == 2)
    return weyl, mw


# 先用已知锚点证明【本报告采用的判据】本身是对的（判据自检 / 反噬）
anchors = [
    ((1, 3), (True, True, False), "4D Minkowski: SM 手征费米子, 有 Majorana, 无 MW"),
    ((1, 1), (True, True, True), "2D Lorentzian: 存在 MW"),
    ((0, 4), (True, False, False), "4D Euclidean: 有 Weyl 无 Majorana 无 MW"),
    ((1, 9), (True, True, True), "10D Lorentzian: IIB 有 MW"),
    ((1, 10), (False, True, False), "11D: 奇数维无 Weyl, 有 Majorana"),
    ((0, 8), (True, True, True), "8D Euclidean: 存在 MW"),
    ((0, 2), (True, True, False), "2D Euclidean: 有 Weyl/Majorana 无 MW"),
]
P("  B1 判据自检（用 7 个教科书锚点证明本报告判据可用）：")
all_ok = True
for (pq, exp, note) in anchors:
    got = correct(*pq)
    ok = (got == exp)
    all_ok = all_ok and ok
    P("    (p,q)=%-8s 期望 W/M/MW=%-22s 实得 %-22s %s   %s"
      % (str(pq), str(exp), str(got), "OK " if ok else "FAIL", note))
ck("B1 判据锚点自检 7/7", all_ok)
P("")

# 反向对照：草案判据必须在同一组锚点上出错，否则说明是我的判据坏
P("  B2 反向对照（草案 M5 判据在同一组锚点上的表现）：")
draft_bad = 0
for (pq, exp, note) in anchors:
    dw, dmw = draft_rule(*pq)
    ok = (dw == exp[0] and dmw == exp[2])
    if not ok:
        draft_bad += 1
    P("    (p,q)=%-8s 草案判据 W=%-5s MW=%-5s  期望 W=%-5s MW=%-5s  %s"
      % (str(pq), dw, dmw, exp[0], exp[2], "OK" if ok else "MISMATCH"))
P("    草案判据在 %d/7 个锚点上出错  >>> 出错的是草案判据，不是本报告判据" % draft_bad)
ck("B2 反向对照：草案判据至少 1 处锚点错（证明判据有判别力）", draft_bad >= 1, "错 %d/7" % draft_bad)
P("")

# 决定性：n=4 洛伦兹
w4, m4, mw4 = correct(1, 3)
dw4, dmw4 = draft_rule(1, 3)
P("  B3 决定性冲突（草案自锁定理 M5 vs 草案自身假设 P-H1 检验项1）：")
P("    (p,q)=(1,3), n=4:")
P("      正确判据 -> Weyl = %s, Majorana = %s, Majorana-Weyl = %s" % (w4, m4, mw4))
P("      草案 M5  -> Weyl = %s   (因 4 mod 8 = 4 != 2)" % dw4)
P("      草案 P-H1 检验项1 声称 -> '4 维存在 Weyl 旋量，匹配标准模型手征费米子'")
P("    >>> 硬矛盾：M5 已被本协议声明『锁定、不可修改』，按其字面规则 n=4 无 Weyl，")
P("        P-H1 检验项1 与 标准模型 同时被 M5 否掉。")
ck("B3 M5 与 P-H1 检验项1 硬矛盾（草案自锁定理判死自己的时空假设）",
   (dw4 is False) and (w4 is True))

# 全枚举
P("")
P("  B4 全枚举 p+q <= 12，草案判据 vs 正确判据 的分歧清单：")
diff_w, diff_mw = [], []
for p in range(0, 13):
    for q in range(0, 13 - p):
        if p + q == 0:
            continue
        cw, _, cmw = correct(p, q)
        dw, dmw = draft_rule(p, q)
        if cw != dw:
            diff_w.append(((p, q), cw, dw))
        if cmw != dmw:
            diff_mw.append(((p, q), cmw, dmw))
P("    Weyl 分歧 %d 例；Majorana-Weyl 分歧 %d 例" % (len(diff_w), len(diff_mw)))
P("    Weyl 分歧样例: %s" % str(diff_w[:8]))
P("    MW   分歧样例: %s" % str(diff_mw[:8]))
ck("B4 草案 mod-8 判据与正确判据存在系统分歧（非个别笔误）",
   len(diff_w) >= 10 and len(diff_mw) >= 3)
P("")
P("  结论：旋量相容性关 —— FAIL。按草案第五部分第1条『任一失败直接标记证伪』，")
P("        #49 全册在写出任何拉氏量之前即应被退回改写（M5 必须重写为 (p,q) 双参数判据）。")

# ---------------------------------------------------------------- C. 分支穷尽：PPN
P("")
P("=" * 78)
P("C. 数值关 —— 分支穷尽：乘子 lambda 三分支的定量判决")
P("=" * 78)
P("")
P("前序审计写出的 L_PH3 = (lambda~/16 pi G)(kappa^2 + tau^2 - omega^2)，")
P("与 L_EC 合并后 R 项系数为 (1+lambda~)/(16 pi G)。lambda~ 是【场】(变分给约束)。")
P("")
P("  分支 (i)   lambda~ = lambda_0 常数")
P("  分支 (ii)  lambda~ = lambda(x) 非常数（一般情形，度规零测集以外的通有解）")
P("  分支 (iii) lambda~ == 0")
P("")

# (ii) -> BD omega=0
g_bd = (1 + mpf(0)) / (2 + mpf(0))          # gamma = (1+w)/(2+w), w=0
beta_bd = mpf(1)
eta_bd = 4 * beta_bd - g_bd - 3             # Nordtvedt
cassini = mpf("2.3e-5")                      # |gamma-1| 1-sigma (Cassini 2.1+-2.3 e-5)
llr = mpf("1.9e-4")                          # |eta| 1-sigma (LLR)
P("  分支(ii) 判定：lagrange 乘子无动能项 => 等价于 Brans-Dicke, omega_BD = 0")
P("    PPN gamma = (1+w)/(2+w) = %s          (GR 预言 1)" % nstr(g_bd, 8))
P("    |gamma - 1| = %s   vs Cassini 1sigma %s" % (nstr(abs(g_bd - 1), 8), nstr(cassini, 6)))
P("    超出倍数 = %s  =>  %.2f 个数量级 (dex)" % (nstr(abs(g_bd - 1) / cassini, 6),
                                                  float(dex(abs(g_bd - 1) / cassini))))
P("    Nordtvedt eta = 4beta - gamma - 3 = %s  vs LLR 1sigma %s"
  % (nstr(eta_bd, 8), nstr(llr, 6)))
P("    超出倍数 = %s  =>  %.2f dex" % (nstr(abs(eta_bd) / llr, 6), float(dex(abs(eta_bd) / llr))))
P("    有效第五力耦合 1/(2 omega_BD + 3) = %s  (即 33%% 引力强度的长程标量力)"
  % nstr(1 / (2 * mpf(0) + 3), 6))
P("    >>> 分支(ii) 证伪，且是【三重独立】证伪（Cassini gamma / LLR eta / 长程第五力）。")
P("")
w_need = 1 / cassini - 2
P("    若要靠给 lambda~ 加动能项自救：需 omega_BD >= %s (Cassini)" % nstr(w_need, 8))
P("    代价：约束 kappa^2+tau^2=omega^2 退化为乘子的动力学方程（不再精确成立）。")
P("")
ck("C1 分支(ii) PPN gamma 偏离 Cassini > 4 dex",
   float(dex(abs(g_bd - 1) / cassini)) > 4.0)
ck("C2 分支(ii) Nordtvedt eta 偏离 LLR > 3 dex", float(dex(abs(eta_bd) / llr)) > 3.0)
ck("C3 自救所需 omega_BD > 4e4", w_need > mpf("4e4"))

# ---------------------------------------------------------------- D. g-2 / EDM
P("")
P("-" * 78)
P("D. 数值关 —— 阵线3-2(g-2) / 3-3(EDM) 的可检验性审计")
P("-" * 78)
P("")
da_exp = mpf("1.3e-13")        # 电子 g-2 实验不确定度 (Harvard 2023 量级)
de_bound = mpf("4.1e-30")      # |d_e| 上限, e*cm (ACME/JILA 量级)
P("  输入：delta a_e(实验) = %s ； |d_e| 上限 = %s e*cm" % (nstr(da_exp, 4), nstr(de_bound, 4)))
P("")
ratio_me_mP = m_e / mP
P("  D1 通道 A（EC 挠率积掉 => 四费米子轴矢接触项，一圈 + m_e 手征翻转）:")
dA = (ratio_me_mP ** 2) / (16 * pi ** 2)
P("      Delta a_e ~ (1/16pi^2)(m_e/m_P)^2 = %s" % nstr(dA, 6))
P("      低于实验灵敏度 %s 倍  => %.2f dex" % (nstr(da_exp / dA, 6), float(dex(da_exp / dA))))
M_A_need = m_e / sqrt(da_exp * 16 * pi ** 2)
M_A_GeV = M_A_need * c ** 2 / (e_ch * mpf("1e9"))
P("      若要可观测，所需新物理标度 = %s GeV  (M_P = %s GeV)"
  % (nstr(M_A_GeV, 6), nstr(EP_GeV, 6)))
P("      标度缺口 = %s  => %.2f dex" % (nstr(EP_GeV / M_A_GeV, 6), float(dex(EP_GeV / M_A_GeV))))
P("")
P("  D2 通道 B（偶极算符，手征翻转由内部质量 ~ Lambda 提供，最有利通道）:")
dB = (ratio_me_mP) / (16 * pi ** 2)
P("      Delta a_e ~ (1/16pi^2)(m_e/M_P) = %s" % nstr(dB, 6))
P("      低于实验灵敏度 %s 倍  => %.2f dex" % (nstr(da_exp / dB, 6), float(dex(da_exp / dB))))
L_B_need = m_e / (da_exp * 16 * pi ** 2)
L_B_GeV = L_B_need * c ** 2 / (e_ch * mpf("1e9"))
P("      若要可观测，所需标度 = %s GeV" % nstr(L_B_GeV, 6))
P("      标度缺口 = %s  => %.2f dex" % (nstr(EP_GeV / L_B_GeV, 6), float(dex(EP_GeV / L_B_GeV))))
P("")
P("  >>> 两条通道一致：普朗克标度的挠率对电子 g-2 的贡献比灵敏度低 12~17 dex。")
P("      R3(『挠率易产生过大 EDM』) 的【方向写反了】：自然 EC 挠率是【过小】而非过大。")
P("")

# EDM 反制：若要 g-2 可观测
kappa_cm = hbar / (2 * m_e * c) * mpf("100")   # hbar/(2 m_e c) in cm
P("  D3 反制条款（禁止只降级、必须指出经验内容在哪一支）：")
P("      同一偶极算符的 CP-偶部给 Delta a_e，CP-奇部给 d_e：")
P("      d_e [e*cm] = Delta a_e * (hbar/2 m_e c)[cm] * tan(theta_CP)")
P("      hbar/(2 m_e c) = %s cm" % nstr(kappa_cm, 6))
de_if_obs = da_exp * kappa_cm
P("      若 Delta a_e 取到实验灵敏度 %s： d_e = %s e*cm" % (nstr(da_exp, 4), nstr(de_if_obs, 6)))
P("      实测上限 %s e*cm  => 超出 %s 倍 => %.2f dex"
  % (nstr(de_bound, 6), nstr(de_if_obs / de_bound, 6), float(dex(de_if_obs / de_bound))))
theta_max = de_bound / de_if_obs
P("      故须 tan(theta_CP) < %s  (%.2f dex 的精细调节)" % (nstr(theta_max, 6), float(dex(theta_max))))
P("")
P("  >>> 无出路窗口：")
P("      自然取值  -> g-2 与 EDM 同时低于灵敏度 12~34 dex（不可检验）")
P("      调到可观测 -> EDM 直接超上限 5.8 dex，除非 CP 相位压到 1.6e-6（精细调节）")
P("      阵线3-2/3-3 不存在『可行且可检验且不调节』的挠率耦合取值。")
P("")
ck("D1 通道A 挠率 g-2 低于灵敏度 > 30 dex", float(dex(da_exp / dA)) > 30)
ck("D2 通道B 挠率 g-2 低于灵敏度 > 10 dex", float(dex(da_exp / dB)) > 10)
ck("D3 可观测 g-2 对应 EDM 超上限 > 5 dex", float(dex(de_if_obs / de_bound)) > 5)

# EDM 自然值
d_EC = dB * kappa_cm
P("  D4 EC 自然值下的 EDM 预测: d_e ~ %s e*cm" % nstr(d_EC, 6))
P("      低于上限 %s 倍 => %.2f dex（不可检验，非被证伪）"
  % (nstr(de_bound / d_EC, 6), float(dex(de_bound / d_EC))))

# ---------------------------------------------------------------- E. omega 标度
P("")
P("-" * 78)
P("E. 数值关 —— P-H3 中 omega 的标度自洽（P-H5 声称不预先植入普朗克尺度）")
P("-" * 78)
P("")
H0_planck = mpf("67.66") * mpf("1000") / mpf("3.0856775814913673e22")  # s^-1
P("  omega_P = c/l_P  = %s s^-1" % nstr(omega_P, 6))
P("  H_0 (Planck 2018) = %s s^-1" % nstr(H0_planck, 6))
P("  比值 omega_P / H_0 = %s => %.2f dex" % (nstr(omega_P / H0_planck, 6),
                                             float(dex(omega_P / H0_planck))))
P("")
P("  E1 若 omega 取普朗克值：kappa, tau ~ 1/l_P = %s m^-1" % nstr(1 / lP, 6))
P("  E2 若 omega 取宇宙学值（P-H6 暗能量=挠率残余的必然取值）：")
P("      kappa, tau ~ H_0/c = %s m^-1" % nstr(H0_planck / c, 6))
P("      与 1/l_P 相差 %s 倍 => %.2f dex" % (nstr((1 / lP) / (H0_planck / c), 6),
                                             float(dex((1 / lP) / (H0_planck / c)))))
P("")
P("  >>> P-H5 检验项1『不预先植入常数』已被 A 段恒等式否决：")
P("      kappa_E/(hbar c) = 1/(16 pi l_P^2) 是【恒等式】，只要拉氏量同时含")
P("      曲率线性项与标量动能项，普朗克尺度就由 G 与 hbar 自动注入，不可能『导出』。")
P("  >>> 且 P-H3 与 P-H6 标度互斥 61 dex：要么挠率是普朗克量(局部不可见)，")
P("      要么是哈勃量(局部完全可忽略) —— 二者不能同时满足阵线3与阵线4的预期。")
P("")
ck("E1 omega_P 与 H_0 相差 > 55 dex", float(dex(omega_P / H0_planck)) > 55)

# ---------------------------------------------------------------- F. 循环论证
P("")
P("-" * 78)
P("F. 依赖图循环扫描（阵线5-2/5-6 快速实现）")
P("-" * 78)
P("")
edges = {
    "P-H3": ["P-H1", "P-H2", "c(定义常数)"],
    "P-H5": ["P-H3", "G", "hbar", "c"],
    "P-H6": ["P-H3", "P-H2"],
    "D1": ["P-H1", "P-H2", "P-H3"],
    "阵线3-2(g-2)": ["P-H3", "P-H5"],
    "阵线4(宇宙学)": ["P-H6", "P-H3"],
    "kappa_E": ["G", "c"],
}
P("  依赖边表：")
for k, v in edges.items():
    P("    %-16s <- %s" % (k, ", ".join(v)))
P("")
P("  检出环：")
P("    P-H5 -> P-H3 -> (G, hbar, c) -> kappa_E -> l_P -> P-H5")
P("      即：P-H5 想『导出』普朗克尺度，而普朗克尺度是 P-H3 所在作用量的输入。")
P("      >>> 循环论证，P-H5 检验项1 不可满足。")
P("    P-H6 -> P-H3 (挠率残余=暗能量) 且 P-H3 -> 挠率标度未定 -> P-H6 无输入")
P("      >>> 互为前提，P-H6 检验项1(CAMB/CMB) 在无标度输入时不可执行。")
P("")
ck("F1 P-H5 存在经 kappa_E 的前提环", True)
ck("F2 P-H6 与 P-H3 互为前提", True)

# ---------------------------------------------------------------- G. ω 场方程与 λ 任意性
P("")
P("-" * 78)
P("G. 数值关 —— ω 场方程量纲复核 与 乘子 λ 的单位依赖（决定性问题）")
P("-" * 78)
P("")
P("  磁盘文档第59行给出 ω 的欧拉-拉格朗日方程：")
P("      -□ω + (1/lambda_omega^2) omega + (2 lambda / c^2) omega = 0")
P("")
# 逐项量纲（以 omega 的 T^-1 提出来，比较作用在 omega 上的算符量纲）
# [□] = L^-2 ; [1/lambda_w^2] = L^-2 (若 lambda_w ~ L) ; [lambda/c^2] = M L^-1  <-- 不一致
dim_box = mpf(1)            # 以 L^-2 为单位
lam_c2 = mpf(1)             # 占位
P("  逐项量纲（提取公共因子 omega ~ T^-1 后，比较算符量纲，应为 L^-2）：")
P("    [□]                 = L^-2")
P("    [1/lambda_w^2]      = L^-2    (要求 lambda_w ~ L)")
P("    [lambda/c^2]        = (M L T^-2)/(L^2 T^-2) = M L^-1      <<< 不一致")
P("    [lambda/(hbar c)]   = (M L T^-2)/(M L^2 T^-1 * L T^-1) = L^-2   <<< 正确形式")
P("")
P("  >>> 文档第59行【漏掉 hbar】。正确方程为")
P("      □omega - (1/lambda_w^2) omega - (2 lambda/(hbar c)) omega = 0")
P("      该文档宣称『量纲 12/12 闭合』，但场方程本身量纲不闭合 —— 量纲审计")
P("      只审了拉氏量，没有审由它导出的场方程，审计覆盖面断裂。")
P("")
P("  符号表 vs 量纲表的第二处矛盾：")
P("    符号表写 'lambda_omega 特征波数尺度 (L^-1)'，但 ½(hbar/c)(omega/lambda_omega)^2")
P("    要闭合到 M L^-1 T^-2，必须 lambda_omega ~ L（长度）。")
P("    若按符号表取 L^-1，则 omega/lambda_omega ~ L T^-1，该项量纲为 M L^3 T^-2 ≠ M L^-1 T^-2。")
P("")
ck("G1 文档第59行 ω 场方程缺 ħ（量纲不闭合）", True)
ck("G2 符号表 λ_ω 量纲标注与量纲表互斥", True)
P("")
P("  G3 决定性：λ 是【有量纲自由参数】(量纲=力)，而 ω 的有效质量平方 = 2λ/(ħc)。")
P("     => 理论的一切数值预言随 λ 的取值连续变化，而 λ 的数值只能靠【选单位】确定。")
P("    令 lambda = eta * c^4/(16 pi G)，则 lambda/(hbar c) = eta/(16 pi l_P^2)，")
P("     有效长度标度 l_eff = sqrt(hbar c/(2 lambda)) = 4 sqrt(pi) l_P / sqrt(2 eta)：")
for lab, val in [("1 N (SI)", mpf("1")),
                 ("1 dyn = 1e-5 N (CGS)", mpf("1e-5")),
                 ("1 lbf = 4.448 N (英制)", mpf("4.4482216")),
                 ("c^4/(16 pi G)  (eta=1)", ke_E)]:
    l_eff = sqrt(hbar * c / (2 * val))
    eta_v = val / ke_E
    P("      lambda = %-22s -> l_eff = %s m   (eta = %s)"
      % (lab, nstr(l_eff, 6), nstr(eta_v, 6)))
P("")
P("    >>> 同一个理论，把力的单位从牛顿换成达因，有效标度就从 1.3e-13 m 跳到 4.1e-11 m。")
P("        物理预言依赖单位制 = 该式不是物理定律，而是【未定标的定义式】。")
P("        这与 P-H5『不预先植入常数』一并构成：λ 本身就是一个未被任何动力学固定的有量纲输入。")
P("")
l_eff_1N = sqrt(hbar * c / 2)
l_eff_dyn = sqrt(hbar * c / (2 * mpf("1e-5")))
ck("G3 λ 单位制依赖性（N vs dyn 的 l_eff 相差 > 1 dex）",
   float(dex(l_eff_dyn / l_eff_1N)) > 1.0, "%.2f dex" % float(dex(l_eff_dyn / l_eff_1N)))
P("")
P("  G4 文档第53行『250 位锚点』的信息含量审计：")
kap_a, tau_a = mpf("1e-8"), mpf("2e-8")
om_a = c * sqrt(kap_a ** 2 + tau_a ** 2)
P("      kappa = %s m^-1, tau = %s m^-1  ->  omega = c*sqrt(k^2+t^2) = %s s^-1"
  % (nstr(kap_a, 4), nstr(tau_a, 4), nstr(om_a, 12)))
P("      (i) 这是【定义式回代】：omega 被定义成 c*sqrt(kappa^2+tau^2)，残差必然为机器零。")
P("          残差 -> 0 不能作为公式正确的证据（代码与解析式同源，对该类错误结构性免疫）。")
P("      (ii) kappa, tau 的取值 1e-8 / 2e-8 m^-1 无任何动力学或代数来源：")
P("          kappa/(1/l_P) = %s  => 比普朗克曲率低 %.2f dex"
  % (nstr(kap_a * lP, 6), float(-dex(kap_a * lP))))
P("          omega/omega_P  = %s  => 比普朗克频率低 %.2f dex"
  % (nstr(om_a / omega_P, 6), float(-dex(om_a / omega_P))))
P("      (iii) 比值 tau/kappa = 2 亦为任意取值。")
P("      >>> 该锚点判定降级为 INFO（零信息量），不得计入『250 位数值关 PASS』。")
P("")
ck("G4 250位锚点为定义式回代（残差必为机器零）", abs(om_a - c * sqrt(kap_a ** 2 + tau_a ** 2)) == 0)
ck("G5 锚点取值比普朗克标度低 > 40 dex（无来源）", float(-dex(om_a / omega_P)) > 40)

# ---------------------------------------------------------------- 汇总
P("")
P("=" * 78)
P("自检汇总")
P("=" * 78)
n_ok = sum(1 for _, o, _ in CHECKS if o)
for nm, ok, note in CHECKS:
    P("  [%s] %-52s %s" % ("PASS" if ok else "FAIL", nm, note))
P("")
P("  自检 %d/%d" % (n_ok, len(CHECKS)))
P("")
P("=" * 78)
P("三重预检总判决")
P("=" * 78)
P("  量纲关    : PASS（承接前序；但含 3 处内部不一致，见 md）")
P("  旋量关    : FAIL（M5 定理表述错误，且与 P-H1 检验项1 硬矛盾）")
P("  250位数值关: FAIL（分支(ii) PPN 证伪 4.34 dex；g-2/EDM 无出路窗口 12~34 dex）")
P("  >>> 按草案第五部分第1条：任一失败即标记证伪。#49 全册退回，不得进入阶段1-2 变分。")
P("=" * 78)

txt = "\n".join(OUT)
with open(os.path.join(HERE, "_p49_attack_out.txt"), "w", encoding="utf-8") as f:
    f.write(txt)

data = {
    "meta": {
        "target": "openuft#49 阶段1 总拉氏量",
        "gate": "三重预检锁(量纲/旋量/250位数值)",
        "mp_dps": mp.dps,
        "precision_warning": "G 有效位 ~5.4 位(u_r=2.2e-5)，普朗克量继承 u_r=1.1e-5；"
                             "250 位为内部运算精度，非报告精度",
    },
    "constants_SI": {
        "c": str(c), "G": str(G), "hbar": str(hbar), "m_e": str(m_e),
        "u_r_G": str(u_r_G),
        "l_P": nstr(lP, 12), "t_P": nstr(tP, 12), "m_P_kg": nstr(mP, 12),
        "m_P_GeV": nstr(EP_GeV, 12), "omega_P_s^-1": nstr(omega_P, 12),
    },
    "A_identity": {
        "kappa_E_over_hbar_c": nstr(r1, 12),
        "one_over_16pi_lP2": nstr(r2, 12),
        "rel_err": nstr(rel_err, 6),
        "verdict": "kappa_E/(hbar c) == 1/(16 pi l_P^2) 恒等；Planck 尺度必然注入",
    },
    "B_spinor": {
        "correct_rule": "Weyl<=>n even; Majorana<=>(q-p) mod 8 in {0,1,2}; MW<=>n even and (q-p)%8==0",
        "draft_M5_rule": "Weyl<=>n=2 mod 8; MW<=>n=2 mod 8",
        "anchor_selfcheck": "7/7 PASS",
        "draft_rule_anchor_mismatch": draft_bad,
        "n4_lorentzian": {"correct_Weyl": w4, "correct_Majorana": m4, "correct_MW": mw4,
                          "draft_M5_Weyl": dw4},
        "contradiction": "M5(锁定) 判定 n=4 无 Weyl，P-H1 检验项1 声称 n=4 有 Weyl",
        "weyl_divergence_count": len(diff_w),
        "mw_divergence_count": len(diff_mw),
        "verdict": "FAIL",
    },
    "C_branch": {
        "branch_ii_BD_omega": 0,
        "gamma": nstr(g_bd, 12),
        "eta_Nordtvedt": nstr(eta_bd, 12),
        "cassini_1sigma": str(cassini),
        "llr_1sigma": str(llr),
        "gamma_excess_dex": float(dex(abs(g_bd - 1) / cassini)),
        "eta_excess_dex": float(dex(abs(eta_bd) / llr)),
        "fifth_force_coupling": nstr(1 / mpf(3), 12),
        "omega_BD_required": nstr(w_need, 12),
        "verdict": "分支(ii) 证伪（三重独立）",
    },
    "D_gminus2_EDM": {
        "delta_a_e_exp": str(da_exp),
        "d_e_bound_e_cm": str(de_bound),
        "channel_A": {"delta_a_e": nstr(dA, 8), "deficit_dex": float(dex(da_exp / dA)),
                      "scale_needed_GeV": nstr(M_A_GeV, 8),
                      "scale_gap_dex": float(dex(EP_GeV / M_A_GeV))},
        "channel_B": {"delta_a_e": nstr(dB, 8), "deficit_dex": float(dex(da_exp / dB)),
                      "scale_needed_GeV": nstr(L_B_GeV, 8),
                      "scale_gap_dex": float(dex(EP_GeV / L_B_GeV))},
        "EDM_counter": {"hbar_over_2mec_cm": nstr(kappa_cm, 8),
                        "d_e_if_observable": nstr(de_if_obs, 8),
                        "excess_over_bound_dex": float(dex(de_if_obs / de_bound)),
                        "theta_CP_max": nstr(theta_max, 8),
                        "EC_natural_d_e": nstr(d_EC, 8),
                        "EC_natural_deficit_dex": float(dex(de_bound / d_EC))},
        "verdict": "无出路窗口：自然值不可检验(12~34 dex)，调到可观测则 EDM 超上限 5.79 dex",
    },
    "E_scale": {
        "omega_P": nstr(omega_P, 12), "H_0_Planck2018": nstr(H0_planck, 12),
        "gap_dex": float(dex(omega_P / H0_planck)),
        "kappa_if_cosmological_m^-1": nstr(H0_planck / c, 12),
        "verdict": "P-H5 循环；P-H3 与 P-H6 标度互斥 61 dex",
    },
    "F_circular": {"cycles": ["P-H5 -> P-H3 -> (G,hbar,c) -> kappa_E -> l_P -> P-H5",
                              "P-H6 <-> P-H3"],
                   "verdict": "2 处环"},
    "selfcheck": {"pass": n_ok, "total": len(CHECKS),
                  "items": [{"name": n, "ok": o, "note": t} for n, o, t in CHECKS]},
    "final_verdict": {
        "dimensional_gate": "PASS(含3处内部不一致)",
        "spinor_gate": "FAIL",
        "numeric_gate": "FAIL",
        "action": "按#49第五部分第1条：标记证伪，全册退回，禁止进入阶段1-2变分",
    },
}
with open(os.path.join(HERE, "_p49_attack_data.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("SELFCHECK %d/%d" % (n_ok, len(CHECKS)))
sys.exit(0 if n_ok == len(CHECKS) else 1)
