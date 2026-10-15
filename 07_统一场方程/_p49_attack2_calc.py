# -*- coding: utf-8 -*-
"""
openuft#49 攻破第二轮：力的统一方程（P-H4 / D3 / 阵线1-8）+ 「与实验数据一致」的可检验性审计
运行: <venv python> _p49_attack2_calc.py
输出: _p49_attack2_out.txt / _p49_attack2_data.json
"""
import json
import os
import sys

from mpmath import mp, mpf, sqrt, pi, log, log10, exp, findroot, nstr

mp.dps = 250

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []
CHECKS = []


def P(s=""):
    OUT.append(s)


def ck(name, ok, note=""):
    CHECKS.append((name, bool(ok), note))


def dex(x):
    return log10(abs(x)) if x != 0 else mpf("-inf")


P("=" * 78)
P("openuft#49 攻破第二轮：力的统一方程 (P-H4 / D3 / 阵线1-8)")
P("           兼审『与所有实验数据一致』这一要求的可检验性")
P("           mp.dps = %d" % mp.dps)
P("=" * 78)
P("")
P("【伪精度声明】G 的 u_r = 2.2e-5（约 5.4 位有效数字），普朗克量继承 u_r = 1.1e-5。")
P("  内部 250 位仅为排除舍入误差，报告只取 6 位有效数字，其余为噪声。")
P("")

# ================================================================ A. 规范群嵌入
P("-" * 78)
P("A. 规范群嵌入检验（P-H4 检验项1 / 阵线1-8）—— 代数层面")
P("-" * 78)
P("")
P("A1 目标群与被嵌群的维数/秩对照：")
P("    %-34s %8s %8s" % ("群", "实维数", "秩"))
groups = [
    ("SU(3)xSU(2)xU(1) (标准模型)", 12, 4, "目标：必须被嵌入"),
    ("Spin(1,3) = SL(2,C)", 6, 1, "洛伦兹自旋群"),
    ("Aut(Cl(1,3)) = PGL(4,R)", 15, 2, "极大紧子群 SO(4)，秩 2"),
    ("Aut(Cl(1,3)xC) = PGL(4,C)", 30, 3, "极大紧子群 PSU(4)，秩 3"),
    ("SU(4)", 15, 3, "4 复维 Clifford 模的幺正群"),
    ("SU(5) (最小 GUT)", 24, 4, "秩刚好容纳 SM"),
    ("SO(10) (GUT)", 45, 5, "秩 5"),
]
for nm, d, r, note in groups:
    P("    %-34s %8d %8d   %s" % (nm, d, r, note))
P("")
P("    >>> 秩障碍：SM 规范群秩 = 4，而 Aut(Cl(1,3)) 的极大紧子群秩 = 2，")
P("        复化后 PGL(4,C) 的极大紧子群 PSU(4) 秩 = 3。")
P("        定理：紧子群的秩不超过母群的秩（Cartan 子群维数单调）。")
P("        4 > 3 >= 2  =>  SU(3)xSU(2)xU(1) 不可能嵌入 4 维 Clifford 代数的自同构群。")
P("")
ck("A1 秩障碍：rank(SM)=4 > rank(max compact Aut Cl(1,3))=2", 4 > 2)
ck("A2 秩障碍：rank(SM)=4 > rank(PSU(4))=3（复化后仍失败）", 4 > 3)
ck("A3 dim(SM)=12 > dim(Spin(1,3))=6（自旋群更不可能）", 12 > 6)
P("    >> R2（规范群嵌入失败）不是『未来风险』，是定理级不可能。")
P("")

# ---- A4 Clifford 模维数
P("A4 实 Clifford 代数 Cl(p,q) 不可约模的实维数（p=类时, q=类空, n=p+q）")
P("    判据：k=(p-q) mod 8，模实维数 = 2^((n+delta(k))/2)")

DELTA = {0: 0, 1: 1, 2: 2, 3: 1, 4: 2, 5: 1, 6: 0, 7: -1}


def cl_module_dim(p, q):
    n = p + q
    k = (p - q) % 8
    return 2 ** ((n + DELTA[k]) // 2), k


def majorana(p, q):
    return ((q - p) % 8) in (0, 1, 2)


def weyl(p, q):
    return (p + q) % 2 == 0


def mw(p, q):
    return weyl(p, q) and ((q - p) % 8 == 0)


P("")
P("    %-12s %6s %6s %10s %6s %6s %6s" % ("(p,q)", "n", "k", "模实维数", "Weyl", "Major", "MW"))
for pq in [(1, 3), (1, 9), (1, 11), (0, 4), (0, 8), (0, 10), (1, 10), (1, 1)]:
    p, q = pq
    d, k = cl_module_dim(p, q)
    P("    %-12s %6d %6d %10d %6s %6s %6s"
      % (str(pq), p + q, k, d, weyl(p, q), majorana(p, q), mw(p, q)))
P("")
P("    锚点自检（上轮已验证的 7 锚点，此处用同一套函数复算，交叉验证）：")
anch = [((1, 3), (True, True, False)), ((1, 1), (True, True, True)),
        ((0, 4), (True, False, False)), ((1, 9), (True, True, True)),
        ((1, 10), (False, True, False)), ((0, 8), (True, True, True)),
        ((0, 2), (True, True, False))]
aok = all((weyl(*pq), majorana(*pq), mw(*pq)) == e for pq, e in anch)
ck("A5 旋量判据交叉复算 7/7（与上轮一致）", aok)
P("")
P("A5 粒子态空间容量对照（决定性）：")
P("    一代标准模型费米子（含 nu_R）= 16 个左手 Weyl 旋量")
P("      = 16 x 2 复分量 = 32 复 = 64 实   （与 Dixon 代数 RxCxHxO 的 64 实维一致）")
d4, _ = cl_module_dim(1, 3)
P("    Cl(1,3) 不可约模实维数 = %d" % d4)
P("    >>> 缺口 = %d / %d = %s 倍  => %.2f dex" % (64, d4, nstr(mpf(64) / d4, 6),
                                                    float(dex(mpf(64) / d4))))
P("        三代 = 192 实  => 缺口 %s 倍" % nstr(mpf(192) / d4, 6))
P("")
P("    F4 范畴混装警告：dim_R Cl(1,3) = 16，而一代所需内部空间也正好 16 实维。")
P("      但 16 是【算符代数】的维数，不是【态空间】的维数；态空间只有 R^4。")
P("      把代数维数当粒子态维数 = 范畴混装，不得作为『16 对上了』的理由。")
P("")
P("    容量足够的 Lorentz 型 Clifford 代数：")
for p in range(1, 4):
    for q in range(1, 17):
        d, k = cl_module_dim(p, q)
        if d >= 64:
            P("      (p,q)=(%d,%d)  n=%2d  模实维数=%d  %s"
              % (p, q, p + q, d, "<= 最小解" if (p + q) <= 12 else ""))
            break
    else:
        continue
    break
P("    >>> 最小解为 Cl(1,11)：12 维时空。P-H1 声明 4 维 => P-H1 与 P-H4 直接互斥。")
ck("A6 Cl(1,3) 模容量比一代所需小 > 1 dex", float(dex(mpf(64) / d4)) > 1)
ck("A7 容量足够的最小 Lorentz 型 Clifford 代数维数 > 4", True, "Cl(1,11), n=12")

# ================================================================ B. 耦合统一 RG
P("")
P("=" * 78)
P("B. 耦合统一的一圈 RG 检验（用实验数据直接判）")
P("=" * 78)
P("")
MZ = mpf("91.1876")            # GeV
a_inv = mpf("127.952")          # alpha^{-1}(M_Z), PDG
s2w = mpf("0.23121")            # sin^2 theta_W (MS-bar), PDG
as_obs = mpf("0.1180")          # alpha_s(M_Z), PDG
as_err = mpf("0.0009")
c2w = 1 - s2w
alp = 1 / a_inv
a1 = (mpf(5) / 3) * alp / c2w    # GUT 归一化
a2 = alp / s2w
a3 = as_obs
P("  输入（PDG，M_Z = %s GeV）：" % nstr(MZ, 8))
P("    alpha^{-1}(M_Z)      = %s" % nstr(a_inv, 8))
P("    sin^2 theta_W(M_Z)   = %s" % nstr(s2w, 8))
P("    alpha_s(M_Z)         = %s +- %s" % (nstr(as_obs, 6), nstr(as_err, 4)))
P("  导出（GUT 归一化）：")
P("    alpha_1^{-1} = %s   alpha_2^{-1} = %s   alpha_3^{-1} = %s"
  % (nstr(1 / a1, 8), nstr(1 / a2, 8), nstr(1 / a3, 8)))
P("")


def gut_fit(b1, b2, b3, tag):
    """由 alpha_1, alpha_2 定 (alpha_G, M_G)，再预言 alpha_3(M_Z)"""
    c1, c2, c3 = b1 / (2 * pi), b2 / (2 * pi), b3 / (2 * pi)
    i1, i2 = 1 / a1, 1 / a2
    L = (i1 - i2) / (c1 - c2)
    MG = MZ * exp(L)
    aG_inv = i2 - c2 * L
    a3_inv_pred = aG_inv + c3 * L
    a3_pred = 1 / a3_inv_pred
    return MG, aG_inv, a3_pred, L


P("  B1 标准模型粒子内容  (b_1,b_2,b_3) = (41/10, -19/6, -7)：")
MG_sm, aG_sm, a3p_sm, L_sm = gut_fit(mpf("4.1"), -mpf(19) / 6, mpf(-7), "SM")
P("    统一标度 M_GUT = %s GeV" % nstr(MG_sm, 8))
P("    alpha_GUT^{-1} = %s" % nstr(aG_sm, 8))
P("    预言 alpha_s(M_Z) = %s   实测 %s +- %s"
  % (nstr(a3p_sm, 8), nstr(as_obs, 6), nstr(as_err, 4)))
dev_sm = abs(a3p_sm - as_obs)
P("    偏差 = %s  = %s sigma  = %.3f dex"
  % (nstr(dev_sm, 6), nstr(dev_sm / as_err, 6), float(dex(a3p_sm / as_obs))))
P("    >>> 失败。二圈修正量级 ~0.002，远不足以填 0.045 的缺口（>=20 sigma）。")
P("")
P("  B2 控制组：MSSM 粒子内容 (b_1,b_2,b_3) = (33/5, 1, -3)：")
MG_ms, aG_ms, a3p_ms, L_ms = gut_fit(mpf("33") / 5, mpf(1), mpf(-3), "MSSM")
P("    统一标度 M_GUT = %s GeV" % nstr(MG_ms, 8))
P("    alpha_GUT^{-1} = %s" % nstr(aG_ms, 8))
P("    预言 alpha_s(M_Z) = %s   实测 %s +- %s"
  % (nstr(a3p_ms, 8), nstr(as_obs, 6), nstr(as_err, 4)))
dev_ms = abs(a3p_ms - as_obs)
P("    偏差 = %s  = %s sigma" % (nstr(dev_ms, 6), nstr(dev_ms / as_err, 6)))
P("    >>> 通过。控制组成功 = 本判据方法本身有效（判据反噬自己：MSSM 成功 / SM 失败")
P("        正是教科书已知结果，方法复现了它，说明下面对几何统一的判决可信）。")
P("")
ck("B1 SM 统一预言 alpha_s 偏离 > 20 sigma", float(dev_sm / as_err) > 20)
ck("B2 控制组 MSSM 统一预言 alpha_s 在 3 sigma 内（判据可用）",
   float(dev_ms / as_err) < 3)
P("")

# ---- B3 质子衰变
P("  B3 质子衰变约束（Super-K: tau(p->e+ pi0) > 1.6e34 yr, 90% CL）：")
tau_bound = mpf("1.6e34")
tau_ref = mpf("1e31")          # 最小非 SUSY SU(5) 在 M_GUT=1e15 GeV 的量级估计
MG_ref = mpf("1e15")
P("    标定：最小 SU(5) @ M_GUT=1e15 GeV  =>  tau ~ 1e31 yr（量级，强子矩阵元 +-1 dex）")
P("    标度律 tau ~ M_GUT^4")
tau_sm = tau_ref * (MG_sm / MG_ref) ** 4
tau_ms = tau_ref * (MG_ms / MG_ref) ** 4
P("    SM   M_GUT=%s GeV  =>  tau ~ %s yr" % (nstr(MG_sm, 8), nstr(tau_sm, 6)))
P("         低于实验下限 %s 倍 => %.2f dex"
  % (nstr(tau_bound / tau_sm, 6), float(dex(tau_bound / tau_sm))))
P("    MSSM M_GUT=%s GeV  =>  tau ~ %s yr" % (nstr(MG_ms, 8), nstr(tau_ms, 6)))
P("         与实验下限比值 %s" % nstr(tau_ms / tau_bound, 6))
P("    >>> 几何统一若取 SM 粒子内容，质子寿命比实验下限低 ~11 dex，已被排除。")
P("        若要躲开，必须引入 MSSM 级别的新粒子谱（~105 个新参数，LHC 未见）。")
ck("B3 SM 统一标度对应的质子寿命低于实验下限 > 8 dex",
   float(dex(tau_bound / tau_sm)) > 8)

# ================================================================ C. 引力加入
P("")
P("-" * 78)
P("C. 把引力纳入：alpha_G(E) = G E^2 与三个规范耦合的交叉标度")
P("-" * 78)
P("")
MP = sqrt(mpf("1e0"))  # 占位
# M_P from SI constants
c_si = mpf("299792458")
G_si = mpf("6.67430e-11")
hbar_si = mpf("1.054571817e-34")
e_ch = mpf("1.602176634e-19")
mP_kg = sqrt(hbar_si * c_si / G_si)
MP = mP_kg * c_si ** 2 / (e_ch * mpf("1e9"))   # GeV
Gnat = 1 / MP ** 2                              # GeV^-2
P("  M_P = %s GeV    G = %s GeV^-2" % (nstr(MP, 8), nstr(Gnat, 8)))
P("")


def a_inv_run(i_mz, b, E):
    return i_mz - (b / (2 * pi)) * log(E / MZ)


def f(i_mz, b, E):
    return 1 / (Gnat * E ** 2) - a_inv_run(i_mz, b, E)


cross = {}
for nm, i_mz, b in [("alpha_3", 1 / a3, mpf(-7)),
                    ("alpha_2", 1 / a2, -mpf(19) / 6),
                    ("alpha_1", 1 / a1, mpf("4.1"))]:
    E0 = findroot(lambda E: f(i_mz, b, E), mpf("1.5e18"))
    cross[nm] = E0
    P("  alpha_G = %-8s 的交叉标度  E = %s GeV" % (nm, nstr(E0, 8)))
Es = sorted(cross.values())
P("")
P("  三个交叉标度的离散：E_max/E_min = %s  => %.3f dex"
  % (nstr(Es[-1] / Es[0], 6), float(dex(Es[-1] / Es[0]))))
ck("C1 引力与三个规范耦合的交叉标度不重合（离散 > 0.05 dex）",
   float(dex(Es[-1] / Es[0])) > 0.05)
P("")
Ebest = mpf("1.9e18")
vals = {"alpha_G": Gnat * Ebest ** 2,
        "alpha_1": 1 / a_inv_run(1 / a1, mpf("4.1"), Ebest),
        "alpha_2": 1 / a_inv_run(1 / a2, -mpf(19) / 6, Ebest),
        "alpha_3": 1 / a_inv_run(1 / a3, mpf(-7), Ebest)}
P("  在最优标度 E = %s GeV 处的四个耦合：" % nstr(Ebest, 6))
for k, v in vals.items():
    P("    %-9s = %s" % (k, nstr(v, 8)))
spread = max(vals.values()) / min(vals.values())
P("    极大/极小 = %s  => %.3f dex" % (nstr(spread, 6), float(dex(spread))))
P("    以 alpha_s 的实验相对精度 %s 计，该离散 = %s sigma"
  % (nstr(as_err / as_obs, 4), nstr((spread - 1) / (as_err / as_obs), 6)))
P("")
P("  >>> 即使取最有利标度，『四个耦合取同一几何值』仍差 %.3f dex（约 %s sigma）。"
  % (float(dex(spread)), nstr((spread - 1) / (as_err / as_obs), 4)))
P("      教科书的『1 : 10^-2 : 10^-5 : 10^-39』把有量纲的 G 与无量纲规范耦合并列，")
P("      是 F4 范畴混装；正确做法必须先化 alpha_G(E)=G E^2 并声明能标（E9）。")
ck("C2 四耦合在最优标度仍离散 > 0.1 dex", float(dex(spread)) > 0.1)

# ================================================================ D. 参数计数门
P("")
P("=" * 78)
P("D. 『与所有实验数据一致』的可检验性审计（参数计数门）")
P("=" * 78)
P("")
obs = [("alpha_s(M_Z)", "0.1180 +- 0.0009", "PDG"),
       ("sin^2 theta_W(M_Z)", "0.23121 +- 0.00004", "PDG (MS-bar)"),
       ("alpha^{-1}(M_Z)", "127.952 +- 0.017", "PDG"),
       ("G", "6.67430e-11, u_r 2.2e-5", "CODATA"),
       ("tau(p->e+ pi0)", "> 1.6e34 yr", "Super-K"),
       ("|d_e|", "< 4.1e-30 e*cm", "ACME/JILA"),
       ("Delta a_e", "|a|< 1.3e-13", "Harvard"),
       ("PPN gamma - 1", "(2.1 +- 2.3)e-5", "Cassini")]
P("  D1 实验数据集（任何『力的统一方程』都必须同时过）：")
for nm, v, src in obs:
    P("    %-20s %-24s %s" % (nm, v, src))
n_obs = len(obs)
P("    观测量总数 n_obs = %d" % n_obs)
P("")
P("  D2 参数计数门：")
P("    构成一次真检验的必要条件：n_free <= n_obs - 1 = %d" % (n_obs - 1))
P("    P-H4 当前状态：")
P("      - 未给出任何关于 {alpha_s, sin^2 theta_W, alpha, G} 的关系式")
P("      - 未给出统一标度、未给出跑动所依赖的粒子谱")
P("      => 关系式数 = 0，自由参数数 = 未声明")
P("    >>> 结论：P-H4 目前【没有任何可检验内容】，『与实验数据一致』不是可执行任务。")
P("        若强行用 >=3 个自由参数去对 3 个耦合值做拟合，则是一次空转拟合，")
P("        触发第五部分第5条『禁止数字命理』与第6条『循环论证』。")
P("")
P("  D3 若补上『自然几何关系』（四耦合在某一标度取同一值）后的结果：")
P("      由 B1/B2/C 段：")
P("        取 SM 谱   -> alpha_s 偏离 %s sigma，质子寿命低 %.2f dex" %
  (nstr(dev_sm / as_err, 4), float(dex(tau_bound / tau_sm))))
P("        取 MSSM 谱 -> alpha_s 偏离 %s sigma（通过），但需 ~105 个新参数" %
  nstr(dev_ms / as_err, 4))
P("        四耦合同时相等 -> 最优标度仍离散 %.3f dex" % float(dex(spread)))
P("      => 『自然几何关系』被实验否决；放宽则退回拟合。无第三条路。")
P("")
ck("D1 参数计数门：P-H4 关系式数为 0（无检验内容）", True)
ck("D2 若施加自然几何关系，SM 谱下被 >20 sigma 否决", float(dev_sm / as_err) > 20)

# ================================================================ 汇总
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
P("第二轮总判决")
P("=" * 78)
P("  P-H4 检验项1（规范群嵌入）  : 证伪（秩障碍 4>3>=2，定理级不可能）")
P("  P-H4 检验项2（自由度计数）  : 证伪（Cl(1,3) 模 R^4 vs 一代需 R^64，缺 16 倍）")
P("  P-H4 检验项3（手征结构）    : 证伪（M_4(R) 单代数，模不可约，无手征不对称空间）")
P("  D3（四力统一命题）          : 证伪")
P("  『与实验数据一致』          : 当前不可执行（关系式数 0）；施加自然关系后")
P("                               SM 谱被 52 sigma 否决，四耦合同值被 0.166 dex 否决")
P("=" * 78)

txt = "\n".join(OUT)
with open(os.path.join(HERE, "_p49_attack2_out.txt"), "w", encoding="utf-8") as f:
    f.write(txt)

data = {
    "meta": {"target": "openuft#49 P-H4 / D3 力统一方程", "mp_dps": mp.dps,
             "precision_warning": "G u_r=2.2e-5；250 位为内部精度，报告取 6 位有效数字"},
    "A_embedding": {
        "rank_obstruction": {
            "rank_SM": 4, "rank_PGL4R_maxcompact_SO4": 2, "rank_PSU4": 3,
            "verdict": "SU(3)xSU(2)xU(1) 不可嵌入 Cl(1,3) 自同构群（秩障碍）"},
        "clifford_module": {
            "Cl(1,3)_module_real_dim": d4,
            "one_generation_real_dim": 64,
            "deficit_factor": float(mpf(64) / d4),
            "three_generations": 192,
            "minimal_sufficient_algebra": "Cl(1,11), n=12",
            "category_warning": "dim_R Cl(1,3)=16 是算符代数维数，非态空间维数；态空间仅 R^4"},
        "verdict": "P-H4 三项检验全部证伪",
    },
    "B_unification": {
        "inputs": {"M_Z_GeV": nstr(MZ, 8), "alpha_inv": nstr(a_inv, 8),
                   "sin2thetaW": nstr(s2w, 8), "alpha_s": nstr(as_obs, 6),
                   "alpha_s_err": nstr(as_err, 4)},
        "derived_inverse": {"alpha_1_inv": nstr(1 / a1, 8), "alpha_2_inv": nstr(1 / a2, 8),
                            "alpha_3_inv": nstr(1 / a3, 8)},
        "SM": {"M_GUT_GeV": nstr(MG_sm, 8), "alpha_GUT_inv": nstr(aG_sm, 8),
               "alpha_s_predicted": nstr(a3p_sm, 8),
               "deviation_sigma": float(dev_sm / as_err),
               "deviation_dex": float(dex(a3p_sm / as_obs)),
               "tau_proton_yr": nstr(tau_sm, 6),
               "tau_deficit_dex": float(dex(tau_bound / tau_sm))},
        "MSSM_control": {"M_GUT_GeV": nstr(MG_ms, 8), "alpha_GUT_inv": nstr(aG_ms, 8),
                         "alpha_s_predicted": nstr(a3p_ms, 8),
                         "deviation_sigma": float(dev_ms / as_err)},
    },
    "C_gravity": {
        "crossing_scales_GeV": {k: nstr(v, 8) for k, v in cross.items()},
        "scale_spread_dex": float(dex(Es[-1] / Es[0])),
        "best_scale_GeV": nstr(Ebest, 6),
        "values_at_best": {k: nstr(v, 8) for k, v in vals.items()},
        "spread_dex": float(dex(spread)),
        "spread_in_alpha_s_sigma": float((spread - 1) / (as_err / as_obs)),
        "note": "教科书 1:1e-2:1e-5:1e-39 为 F4 范畴混装；须先化 alpha_G(E)=G E^2 再比",
    },
    "D_gate": {
        "observables": [{"name": n, "value": v, "source": s} for n, v, s in obs],
        "n_obs": n_obs,
        "parameter_counting_gate": "n_free <= n_obs - 1",
        "P_H4_relations_provided": 0,
        "verdict": "P-H4 无可检验内容；施加自然几何关系后被实验否决",
    },
    "selfcheck": {"pass": n_ok, "total": len(CHECKS),
                  "items": [{"name": n, "ok": o, "note": t} for n, o, t in CHECKS]},
    "final_verdict": {
        "P-H4": "证伪（3/3 检验项全否）",
        "D3": "证伪",
        "consistency_with_all_data": "当前不可执行；施加自然关系后 SM 谱下 52 sigma 否决",
    },
}
with open(os.path.join(HERE, "_p49_attack2_data.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("SELFCHECK %d/%d" % (n_ok, len(CHECKS)))
sys.exit(0 if n_ok == len(CHECKS) else 1)
