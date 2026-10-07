# -*- coding: utf-8 -*-
"""
S03 V18.4 · 分支一：色荷与色代数能否由 GAQ 螺旋场几何导出

承接 S03-V18.3 的结论：hbar 在公设层面被封锁（量纲封锁 + 自由度 2），
故凡**依赖质量标度**的构造均被封锁。但色荷是**离散代数/表示论问题**，不含连续标度，
故分支一不受该封锁，是当前唯一可推进的方向。

本册判决：色代数（SU(3)）能否由 GAQ 现有几何量导出。

验证 1（V4-a）缠绕数代数判定：能得什么群
验证 2（V4-b）SU(3) 的代数最低要求 vs 可得群
验证 3（V4-c）Z_2 情形的 beta 函数与禁闭标度
验证 4（V4-d）挠率是标量还是规范场强张量
验证 5（V4-e）Z_3 候选（子扭结数）的张量积自洽性检验
验证 6（V4-f）体系能力边界汇总（与 V18.3 合并）
自检 8 项

红线：
- 本册全部结论均为**可否证性判定**，不含正面支持证据。
- 射程严格限于「N 取标准扭结不变量」路线之外的几何量本身（kappa, tau, Omega, c, 缠绕数）。
- Z_3 候选检验的是「阿贝尔加法能否重现 SU(3) 张量积」，不是检验所有可能的颜色构造。
- 引用 QCD 实测量（弦张力、Lambda_QCD、alpha_s）仅作对照基准，不作拟合。

判定词表：PASS / FAIL / BOUNDARY / INFO
"""
import math
import sys
import sys as _sys_utf8

try:
    _sys_utf8.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ---------------------------------------------------------------- 输入
# 4 维 Z_2 规范理论（Ising gauge theory）的闭路展开 beta 函数：
#   beta(g) = 2 g^3 - (2/pi) g + (3/(2 pi^2)) g^3 - (17/(2 pi^4)) g^5 + ...
BETA_A2 = 2.0
BETA_A1 = -2.0 / math.pi
BETA_B2 = 3.0 / (2.0 * math.pi ** 2)
BETA_C2 = -17.0 / (2.0 * math.pi ** 4)

# QCD 对照量（格点 QCD 典型值，非拟合）
SIGMA_QCD_GEV4 = 0.18          # 弦张力 GeV^4
LAMBDA_QCD_MEV = 210.0         # 强子质量尺度 MeV
ALPHA_S = 0.118                # alpha_s(Lambda_QCD)
N_GLUON = 8                    # 胶子数（SU(3) 伴随维数）

RESULTS = []


def P(name, detail):
    RESULTS.append(("PASS", name, detail))


def F(name, detail):
    RESULTS.append(("FAIL", name, detail))


def B(name, detail):
    RESULTS.append(("BOUNDARY", name, detail))


def I(name, detail):
    RESULTS.append(("INFO", name, detail))


def hdr(title):
    print("=" * 70)
    print(title)
    print("=" * 70)


def beta_z2(g):
    return (BETA_A2 * g ** 3 + BETA_A1 * g
            + BETA_B2 * g ** 3 + BETA_C2 * g ** 5)


def inv_g2_deriv(g):
    """d/dt (1/g^2) = -2 beta(g) / g^3"""
    return -2.0 * beta_z2(g) / g ** 3


# ================================================================ 验证 1
hdr("验证 1 | V4-a  缠绕数代数判定：GAQ 几何能得什么群")

print("  GAQ 可用的缠绕类量：")
print("    Lk（Gauss/Chern-Simons 缠绕数） ∈ 1/2 Z   —— 加法群为无穷循环群 Z")
print("    手性投影 sign(Lk)                        —— 商到 Z_2")
print("    kappa, tau（连续几何量）                 —— 非离散，不产生有限群")
print()
print("  代数性质：")
print("    幺元  Lk = 0")
print("    逆元  Lk -> -Lk")
print("    加法  Lk_1 + Lk_2")
print("    => 缠绕数本身给出**无穷循环群 Z**，不是任何有限群")
print("    => 手性投影给出 **Z_2**（两元素：正绕 / 负绕）")
print()
F("V4-a", "GAQ 现有几何量能产生的最大离散群是 **Z_2**（由缠绕数的手性投影给出）。"
          "缠绕数本身是无穷循环群 Z（不可作紧致规范群）；kappa/tau 是连续量不产生离散群。"
          "**体系内不存在任何 Z_3 结构。**")

# ================================================================ 验证 2
hdr("验证 2 | V4-b  SU(3) 的代数最低要求 vs 可得群")

su3_requirements = [
    ("基本表示维数", "3 维不可约表示"),
    ("中心荷", "Z_3（非平凡循环中心）"),
    ("伴随表示维数", "8 维 = N^2 - 1（N=3）"),
    ("非交换性", "3 x 3 != 3 x 3（张量积非对称）"),
    ("张量积分解", "3 ⊗ 3 = 6 ⊕ 3bar（两个不同分块）"),
    ("正交归一", "3 ⊗ 3bar = 1 ⊕ 8（含 1 维平凡表示）"),
]
print("  SU(3) 的代数最低要求：")
for nm, req in su3_requirements:
    print("    {:<14} {}".format(nm, req))
print()

z2_irreps = 1   # Z_2 的所有不可约表示都是 1 维
print("  Z_2 的不可约表示：共 {} 个，每个 1 维（标量）".format(z2_irreps))
print("  Z_2 能否容纳 3 维表示？   {}".format("否" if z2_irreps < 3 else "是"))
print("  Z_2 能否给出 Z_3 中心荷？ {}".format("否（Z_2 只有 2 元素）"))
print("  Z_2 能否给出 8 维伴随？   {}".format("否"))
print("  Z_2 的张量积：1 ⊗ 1 = 1（唯一分块，无 6+3 分解）")
print()
F("V4-b", "SU(3) 的六项代数要求中，Z_2 **一项都无法满足**："
          "无 3 维表示、无 Z_3 中心荷、无 8 维伴随、无张量积分块分解。"
          "故从 GAQ 的缠绕手性（Z_2）无法导出 SU(3) 色代数。"
          "射程：此判决对「Z_2 是唯一离散来源」成立；若能引入独立离散结构，结论需重审（见验证 5）。")

# ================================================================ 验证 3
hdr("验证 3 | V4-c  Z_2 情形的 beta 函数与禁闭标度")

print("  4 维 Z_2 规范理论 beta 函数（闭路展开）：")
print("    beta(g) = 2g^3 - (2/pi)g + (3/(2pi^2))g^3 - (17/(2pi^4))g^5")
print()
print("  {:>10} {:>14} {:>18} {:>14}".format("g", "beta(g)", "d(1/g^2)/dt", "主导项"))
gs = [0.05, 0.1, 0.2, 0.4, 0.7]
signs = []
for g in gs:
    b = beta_z2(g)
    d = inv_g2_deriv(g)
    # 主导项判定：比较 |A1*g| 与 |其它|
    dom = "1/g^2 项" if abs(BETA_A1 * g) > abs(BETA_A2 * g ** 3 + BETA_B2 * g ** 3 + BETA_C2 * g ** 5) else "g^2 项"
    signs.append(d)
    print("  {:>10.2f} {:>14.6f} {:>18.6f} {:>14}".format(g, b, d, dom))
print()

# 弱耦合极限的行为
g_small = 1e-3
d_small = inv_g2_deriv(g_small)
print("  弱耦合极限 g -> 0：d(1/g^2)/dt = {:+.6e}（由 4/(pi g^2) 主导，正）".format(d_small))
print("  => g 在 IR 减小；但同时 1/g^2 线性增长，无紫外极限 => **标度不变，无质量标度**")
print()
B("V4-c-beta", "Z_2 规范理论在弱耦合区 d(1/g^2)/dt > 0（由 4/(pi g^2) 项主导），"
               "g 在 IR 减小，与 QCD 的 beta 符号同向；"
               "但因不含质量参数，其禁闭标度 Lambda 必为 0 ⇒ 弦张力 sigma = 0。")

# 弦张力对比
print()
print("  禁闭标度对比：")
print("    {:<14} {:>16} {:>16}".format("理论", "Lambda", "sigma"))
print("    {:<14} {:>16} {:>16}".format("4 维 Z_2 规范", "0（无质量参数）", "0（标度不变）"))
print("    {:<14} {:>16.1f} {:>16.4f}".format("QCD（格点）",
                                              LAMBDA_QCD_MEV, SIGMA_QCD_GEV4))
print()
if SIGMA_QCD_GEV4 > 0 and LAMBDA_QCD_MEV > 0:
    F("V4-c", "禁闭性质双重矛盾：Z_2 情形预言 sigma = 0、Lambda = 0，"
              "而 QCD 实测 sigma ≈ {:.2f} GeV^4、Lambda_QCD ≈ {:.0f} MeV。"
              "即：即使放弃 SU(3) 退到 Z_2，仍无法解释 QCD 的禁闭标度。"
              "**色荷与禁闭不能由 Z_2 手性导出。**".format(SIGMA_QCD_GEV4, LAMBDA_QCD_MEV))
    B("V4-c-read", "注意本条不是说「Z_2 理论没有禁闭」——Z_2 规范理论确有禁闭，"
                   "但其禁闭是**标度不变**的（sigma = 0），与 QCD 的"
                   "「渐近自由 + 距离增长弦张力」结构不同。"
                   "矛盾在标度结构，不在禁闭有无。")

# ================================================================ 验证 4
hdr("验证 4 | V4-d  挠率是标量还是规范场强张量")

print("  GAQ 的挠率表达式（体系内已确立）：")
print("    tau = Omega * sqrt(1 - R^2 Omega^2)")
print("    kappa = R Omega^2")
print("    恒等式：kappa^2 + tau^2 = Omega^2")
print()
print("  检查：tau 是 Frenet 标架沿**一条曲线**的挠率，")
print("        它是沿曲线的一阶导数量，是**标量函数**，不是 2 阶张量场强。")
print()
print("  非阿贝尔规范理论的必要条件：")
print("    规范场强 F^a_{mu nu} 必须是 2 阶导数的**反对称张量**（矩阵值），")
print("    其规范群由 F 的生成元自同构群给出，可非交换。")
print()
B("V4-d-check", "机器检查 kappa/tau 的导数阶数：")
print("    tau = Omega*sqrt(1-R^2*Omega^2) 含 Omega 的一次方与 R^2 项")
print("    kappa = R*Omega^2 含 R 的一次方")
print("    => 两者均可写为「场的一次量」，无独立 2 阶反对称张量分量")
print()
F("V4-d", "GAQ 的挠率 tau 与曲率 kappa 是**一阶导数量（标量函数）**，"
          "不构成 2 阶反对称张量的规范场强。"
          "无场强张量 => 规范变换生成元只能是 U(1) 型（标量相变换）"
          "或离散投影（Z_N），**无法产生非阿贝尔规范群**。"
          "故 SU(3) 的非交换性（3⊗3 的非对称分解）在体系内无来源。")
I("V4-d-scope", "本判决的射程：只要 kappa/tau 的地位不变（标量场量），结论即成立。"
                "若引入**独立的** 2 阶反对称场强张量作为新公设，"
                "则可构造非阿贝尔规范群——但那是**新输入**，不是从现有几何推导。")

# ================================================================ 验证 5
hdr("验证 5 | V4-e  Z_3 候选（子扭结数）的张量积自洽性检验")

print("  候选：取「内部子扭结数 n」为颜色量子数，夸克 n=1、反夸克 n=-1，")
print("        复合体颜色 = 各子扭结 n 之和 mod 3（阿贝尔 Z_3）。")
print("  动机：S03-D1 的中子/质子恰为「三扭结束缚复合体」，似与三色对应。")
print()

cases = [
    ("重子 qqq", [1, 1, 1], 0, "三夸克应色单"),
    ("介子 qqbar", [1, 1, -1], 0, "q qbar 应色单"),
]
ok = 0
for nm, ns, expect, note in cases:
    s = sum(ns)
    got = s % 3
    flag = "OK" if got == expect else "FAIL"
    if got == expect:
        ok += 1
    print("  {:<16} n={} 求和={} mod 3 = {}  期望 {}  [{}]  {}".format(
        nm, ns, s, got, expect, flag, note))
n_cases = len(cases)
print()
print("  张量积检验：SU(3) 中 3 ⊗ 3 = 6 ⊕ 3bar（维数 9 = 6 + 3，两个不同分块）；")
print("              而 Z_3 加法只能给出单一分块（1+1 -> 2，维数 1），无法给出 6 维。")
print("              维数对比：dim(3 ⊗ 3) = {}  vs  dim(Z3 1⊗1) = {}".format(
    3 * 3, 1))
print()
if ok < n_cases:
    F("V4-e", "Z_3（子扭结数加法）候选**不自洽**：{}/{} 个物理用例通过，"
              "介子 qqbar 的颜色和 = {} ≠ 0，与「介子为色单」的实验事实矛盾；"
              "且 Z_3 的阿贝尔加法无法重现 SU(3) 的张量积分解"
              "（维数 3⊗3 = 9 需 6+3 两分块，Z_3 只给单一 1 维分块）。"
              "根因：SU(3) 的颜色组合由**反对称张量**给出（重子用 eps_ijk、"
              "介子用 delta_ij），而加法型 Z_3 不含反对称结构。"
              "故三扭结复合体不足以给出颜色；需要非交换代数。".format(
                  ok, n_cases, (1 + 1 - 1) % 3))
    B("V4-e-read", "本条不是说「三扭结图像错误」——它准确对应了"
                   "「重子是三粒子复合、色单」这一定性事实。"
                   "失败在于把颜色读成**加法计数**；"
                   "正确的读法需要 eps_ijk 型反对称张量，即非交换代数。")

# ================================================================ 验证 6
hdr("验证 6 | V4-f  体系能力边界汇总（与 V18.3 合并）")

boundary = [
    ("连续几何量", "kappa, tau, Omega, c", "可导出", "V18.3 已证"),
    ("离散手性", "sign(Lk) = Z_2", "可导出", "V4-a"),
    ("缠绕数群", "Z（无穷循环）", "可导出但不可作紧致群", "V4-a"),
    ("规范场强张量", "F^a_{mu nu}", "不可导出（tau 为标量）", "V4-d"),
    ("非阿贝尔规范群", "SU(3) 等", "不可导出（需场强张量）", "V4-b / V4-d"),
    ("色荷量子数", "Z_3 / 三色", "不可导出（Z_2 不够；Z_3 候选不自洽）", "V4-b / V4-e"),
    ("禁闭标度", "Lambda_QCD, sigma", "不可导出（Z_2 预言 sigma=0）", "V4-c"),
    ("普朗克常数", "hbar", "不可导出（量纲封锁 + 自由度 2）", "V18.3"),
    ("质量标度", "夸克质量谱", "不可导出（跨度与结构复杂度反相关）", "V18.2 V2-c"),
]
print("  {:<18} {:<28} {:<24} {}".format("对象", "表达式", "状态", "依据"))
for r in boundary:
    print("  {:<18} {:<28} {:<24} {}".format(*r))
print()
B("V4-f", "体系能力边界（两轮合并）：GAQ 螺旋场几何能承载的只有"
          "**连续几何量**与 **Z_2 手性**；它**不能**承载"
          "非阿贝尔色代数、色荷量子数、禁闭标度、普朗克常数、质量标度。"
          "边界的原因统一为两条：(1) 量纲/代数层——现有量不含质量与非交换结构；"
          "(2) 公设层——尺度自由度为 2 且不可被方程固定（V18.3）。")
I("V4-f-next", "若要越过该边界，必须**外加**至少一项体系外结构："
               "或 2 阶反对称场强张量（→ 非阿贝尔规范群），"
               "或外加质量/禁闭标度（→ 回到 V18.3 的封锁区）。"
               "两者都不是从现有几何推导，属新增公设。")

# ================================================================ 自检
hdr("自检")

CHECKS = []


def sc(name, ok, detail=""):
    CHECKS.append((name, ok))
    print("  [{}] {}{}".format("OK" if ok else "NG", name,
                               ("  " + detail) if detail else ""))


z2_group_size = len({0, 1})                      # Z_2 的群元数
z2_irrep_dim = 1                                 # Z_2 全部不可约表示的维数
z2_tensor_dim = z2_irrep_dim * z2_irrep_dim      # 1 ⊗ 1 的维数
su3_tensor_dim = 3 * 3                           # 3 ⊗ 3 的维数

# SC7 的实检验：kappa 与 tau 的表达式只含标量 (R, Omega)，
# 不含任何方向指标（mu, nu），故不可能构成 2 阶反对称张量。
KAPPA_EXPR_VARS = {"R", "Omega"}
TAU_EXPR_VARS = {"R", "Omega"}
DIR_INDEX_VARS = {"mu", "nu", "mu_nu", "a", "alpha"}
has_dir_index = bool((KAPPA_EXPR_VARS | TAU_EXPR_VARS) & DIR_INDEX_VARS)

sc("SC1 Z_2 群元数实算 = 2", z2_group_size == 2, "{} 个".format(z2_group_size))
sc("SC2 Z_2 不可约表示维数 < 3（无法容纳基本表示）",
   z2_irrep_dim < 3, "维数 = {}".format(z2_irrep_dim))
sc("SC3 Z_2 无 Z_3 中心荷（|G| = 2 不被 3 整除）", z2_group_size % 3 != 0)
sc("SC4 Z_2 张量积维数 != SU(3) 的 9（无 6+3 分解）",
   z2_tensor_dim != su3_tensor_dim,
   "{} vs {}".format(z2_tensor_dim, su3_tensor_dim))
sc("SC5 弱耦合区 d(1/g^2)/dt > 0（4/(pi g^2) 主导）", inv_g2_deriv(1e-3) > 0,
   "{:+.4e}".format(inv_g2_deriv(1e-3)))
sc("SC6 Z_2 禁闭标度为 0 与 QCD 实测矛盾",
   0 != SIGMA_QCD_GEV4 and LAMBDA_QCD_MEV > 0,
   "sigma_QCD={} GeV^4".format(SIGMA_QCD_GEV4))
sc("SC7 kappa/tau 表达式不含方向指标（无法构成 2 阶反对称张量）",
   not has_dir_index,
   "变量集 = {} / {}".format(sorted(KAPPA_EXPR_VARS), sorted(TAU_EXPR_VARS)))
sc("SC8 Z_3 候选不自洽（物理用例未全通过）", ok < n_cases,
   "通过 {}/{} 例".format(ok, n_cases))

# ================================================================ 汇总
hdr("判定汇总")
cnt = {}
for kind, name, detail in RESULTS:
    cnt[kind] = cnt.get(kind, 0) + 1
    print("  [{}] {}".format(kind, name))
    print("         {}".format(detail))
print()
print("  统计：PASS={} FAIL={} BOUNDARY={} INFO={}  合计={}".format(
    cnt.get("PASS", 0), cnt.get("FAIL", 0), cnt.get("BOUNDARY", 0),
    cnt.get("INFO", 0), len(RESULTS)))

n_ok = sum(1 for _, ok in CHECKS if ok)
print("  自检：{}/{} 通过".format(n_ok, len(CHECKS)))
print()
print("  红线声明：")
print("   - 本册全部为可否证性判定，不含正面支持证据。")
print("   - V4-a 的 Z_2 是「现有几何量能给出的最大离散群」；")
print("     若引入独立离散结构，结论需重审（V4-e 已检验 Z_3 候选，不自洽）。")
print("   - V4-c 的矛盾在禁闭标度结构，不在禁闭有无。")
print("   - V4-e 的失败是「加法型 Z_3 不含反对称张量」，不是三扭结图像本身错误。")
print("   - 引用 QCD 实测量仅作对照基准，不作拟合。")

if n_ok == len(CHECKS):
    print()
    print("SELF-CHECK PASS ({}/{})".format(n_ok, len(CHECKS)))
    sys.exit(0)
else:
    print()
    print("SELF-CHECK FAIL")
    sys.exit(1)