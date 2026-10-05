# -*- coding: utf-8 -*-
"""
S03 V18.3 · G4 裁定：普朗克常数 hbar 能否由 GAQ 基本量导出

承接 S03-V18.2 的层级收敛结论：四个独立缺口（G4 / C1 / F / P1）共享公共上游
「质量标度没有第一性锚」。V18.3 追到最上游，判决 G4 的性质：

  G4 究竟是「尚未导出的缺口」，还是「量纲与结构决定的公设边界」？

方法：量纲穷举 + 结构循环判定 + 公设自由度计数。三者均机器可算，不含调参。

验证 1（V3-a）纯几何量集 {kappa, tau, Omega, c} 能否组合出 hbar 的量纲
验证 2（V3-b）加入 G 后的全部量纲可行情形
验证 3（V3-c）循环性判定：量纲可行情形是否必含频率 Omega
验证 4（V3-d）公设自由度计数：A1 / A4 / A5 能否定出 hbar 的初值
验证 5（V3-e）对照：SM 中 eps_s 与 hbar 的地位类比
自检 8 项

红线：
- 量纲分析只给**必要条件**，不充分；V3-b 找到解**不等于** hbar 可导出。
- V3-c 的循环性判定是本册关键：若全部量纲可行情形都含 Omega，而 Omega = w/c 依赖 hbar，
  则结构上循环，hbar 仍不可导出。
- 本册不引入任何新物理假设，只使用 S03 既有公设与量纲代数。
- 本册仍不对 GAQ 的任何主张给出正面支持证据。

判定词表：PASS / FAIL / BOUNDARY / INFO
"""
import itertools
import sys
import sys as _sys_utf8

try:
    _sys_utf8.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ---------------------------------------------------------------- 量纲代数
# 量纲向量按 (M, L, T) 排列
KAPPA = (0, -1, 0)     # 曲率：m^-1
TAU = (0, -1, 0)       # 挠率：m^-1
OMEGA = (0, 0, -1)     # 角频率/光速：s^-1
CLIGHT = (0, 1, -1)    # 光速：m s^-1
GRAV = (-1, 3, -2)     # 引力常量：m^3 kg^-1 s^-2
HBAR = (1, 2, -1)      # 普朗克常数：kg m^2 s^-1

R = 6                   # 指数穷举范围 [-R, R]
OMEGA_IDX = 2           # 指数顺序 kappa, tau, Omega, c, G 中的 Omega 位置

SOLUTIONS = []


def P(name, detail):
    SOLUTIONS.append(("PASS", name, detail))


def F(name, detail):
    SOLUTIONS.append(("FAIL", name, detail))


def B(name, detail):
    SOLUTIONS.append(("BOUNDARY", name, detail))


def I(name, detail):
    SOLUTIONS.append(("INFO", name, detail))


def hdr(title):
    print("=" * 70)
    print(title)
    print("=" * 70)


def fmt_dim(d):
    names = ["M", "L", "T"]
    return "(" + ", ".join("{}{:+d}".format(names[i], d[i]) for i in range(3)) + ")"


def combo_dims(basis, combo):
    acc = [0, 0, 0]
    for v, e in zip(basis, combo):
        for k in range(3):
            acc[k] += v[k] * e
    return tuple(acc)


def solve_signed(target, basis, rmax=R):
    sols = []
    for combo in itertools.product(range(-rmax, rmax + 1), repeat=len(basis)):
        if combo_dims(basis, combo) == target:
            sols.append(combo)
    return sols


# ================================================================ 验证 1
hdr("验证 1 | V3-a  纯几何量集能否组合出 hbar 的量纲")

print("  基本量量纲：")
for nm, v in (("kappa (curvature)", KAPPA), ("tau (torsion)", TAU),
              ("Omega (= w/c)", OMEGA), ("c (light speed)", CLIGHT)):
    print("    {:<20} {}".format(nm, fmt_dim(v)))
print("  目标 [hbar]          = {}".format(fmt_dim(HBAR)))
print()
print("  关键观察：kappa / tau / Omega / c 的**质量分量全为 0**")
print("           => 任何整数幂组合的质量分量恒为 0，而 [hbar] 质量分量为 +1")
print("           => 纯几何量集在量纲层面被**完全封锁**。")
print()

geom_basis = [KAPPA, TAU, OMEGA, CLIGHT]
geom_sols = solve_signed(HBAR, geom_basis)
n_combo_geom = (2 * R + 1) ** len(geom_basis)
mass_reachable = set()
for combo in itertools.product(range(-R, R + 1), repeat=len(geom_basis)):
    mass_reachable.add(sum(v[0] * e for v, e in zip(geom_basis, combo)))

print("  穷举指数范围 [{}, {}]，四维组合 {} 个".format(-R, R, n_combo_geom))
print("  质量分量可达集合 = {}".format(sorted(mass_reachable)))
print("  满足 [hbar] 全部分量的解数 = {}".format(len(geom_sols)))
print()

if not geom_sols:
    F("V3-a", "纯几何量集（曲率/挠率/角频率/光速）的**任意**整数幂组合的质量分量恒为 0，"
              "而 [hbar] 要求 +1 => 量纲封锁，严格无解（穷举 {} 组合确认）。".format(
                  n_combo_geom))
    P("V3-a-lock", "封锁判决：质量量纲是 hbar 的必要成分，而体系内四个纯几何量都不携带质量。"
                  "这不是「尚未找到表达式」，而是**量纲层面不可能存在**表达式。")
else:
    B("V3-a", "出现解 {} 个：{}（须检查结构循环性）".format(len(geom_sols), geom_sols[:4]))

# ================================================================ 验证 2
hdr("验证 2 | V3-b  加入 G 后的全部量纲可行情形")

full_basis = [KAPPA, TAU, OMEGA, CLIGHT, GRAV]
print("  引入 [G] = {}（可用量中唯一携带质量量纲者）".format(fmt_dim(GRAV)))
print()
full_sols = solve_signed(HBAR, full_basis)
n_combo_full = (2 * R + 1) ** len(full_basis)
print("  穷举指数范围 [{}, {}]，五维组合 {} 个".format(-R, R, n_combo_full))
print("  满足 [hbar] 的解数 = {}".format(len(full_sols)))
print()
print("  解样例（指数顺序 kappa, tau, Omega, c, G）：")
for combo in full_sols[:12]:
    print("    {}".format(combo))
print()
if full_sols:
    B("V3-b", "加入 G 后量纲层面**存在** {} 组解，即量纲必要条件可满足。"
              "但量纲分析是必要非充分条件：还需该组合结构上不循环（验证 3），"
              "且能被实际构造。故本条**不构成 hbar 可导出的证据**。".format(len(full_sols)))
else:
    F("V3-b", "即使加入 G 仍无解：hbar 完全不可由体系现有量导出。")

# ================================================================ 验证 3
hdr("验证 3 | V3-c  循环性判定：量纲可行情形是否必含频率 Omega")

no_omega_sols = []
if not full_sols:
    B("V3-c", "无解可判循环性（验证 2 已否证）。")
else:
    with_omega = [s for s in full_sols if s[OMEGA_IDX] != 0]
    without_omega = [s for s in full_sols if s[OMEGA_IDX] == 0]
    print("  含非零 Omega 指数的解：{} / {}".format(len(with_omega), len(full_sols)))
    print("  Omega 指数为 0 的解：      {}".format(len(without_omega)))
    print()
    no_omega_basis = [KAPPA, TAU, CLIGHT, GRAV]
    no_omega_sols = solve_signed(HBAR, no_omega_basis)
    print("  独立复核（基 = kappa, tau, c, G，剔除 Omega）：解数 = {}".format(
        len(no_omega_sols)))
    print()
    if not without_omega and not no_omega_sols:
        F("V3-c", "**全部**量纲可行情形都必含非零 Omega 指数；剔除 Omega 后解集为空"
                  "（独立复核确认）。而 Omega = w/c，角频率满足 w = E/hbar"
                  "（E 含质量，质量按 A5 又含 hbar）=> 用 Omega 构造 hbar 在结构上**循环**。")
    else:
        B("V3-c", "含非零 Omega 指数的解 {} 组，不含的 {} 组。**本册的先验断言"
                  "「量纲允许的形式全部循环」被机器枚举推翻**（反例即不含 Omega 的解）。"
                  "故循环性不能作为否决理由；真正的否决理由见验证 4 与验证 6。".format(
                      len(with_omega), len(without_omega)))
        I("V3-c-falsified", "自我推翻记录：设计本验证时的预期结果是「全部解含 Omega」"
                            "（若成立则循环性可作否决理由）。实际存在 11 组反例，"
                            "例如 kappa^(-6)*tau^(4)*c^(3)/G 量纲恰为 hbar 且不含 Omega。"
                            "教训：量纲层面的「必须含某量」不可先验断言，"
                            "必须穷举验证——本册自检 SC4 即因此从「解数为 0」改为「解数为 11」。")

# ================================================================ 验证 6
hdr("验证 6 | V3-f  不含 Omega 的解：结构归约与隐式初值依赖")

if no_omega_sols:
    # 检查这组解是否属单一量纲类：kappa 指数 a、tau 指数 b、c 指数 p、G 指数 q
    a_list = sorted(set(s[0] for s in no_omega_sols))
    b_list = sorted(set(s[1] for s in no_omega_sols))
    c_list = sorted(set(s[2] for s in no_omega_sols))
    g_list = sorted(set(s[3] for s in no_omega_sols))
    sums = sorted(set(s[0] + s[1] for s in no_omega_sols))
    print("  指数取值范围（kappa/ tau/ c / G）：")
    print("    kappa 指数 = {}".format(a_list))
    print("    tau   指数 = {}".format(b_list))
    print("    c     指数 = {}".format(c_list))
    print("    G     指数 = {}".format(g_list))
    print("    kappa+tau 指数和 = {}".format(sums))
    print()
    single_class = (len(c_list) == 1 and len(g_list) == 1 and len(sums) == 1)
    print("  是否单一量纲类（c、G 指数唯一且 kappa+tau 和唯一）: {}".format(single_class))
    print()
    if single_class:
        p_c = c_list[0]
        q_g = g_list[0]
        s_kt = sums[0]
        print("  ⇒ 全部解归约为单一形式：")
        print("       hbar ~ kappa^a * tau^(-2-a) * c^({}) / G^({})".format(p_c, -q_g))
        print("  （a 取值 {}，指数和 kappa+tau = {}）".format([a_list[0], a_list[-1]], s_kt))
        print()
        # kappa*tau 的量纲
        kt_dim = tuple(KAPPA[i] + TAU[i] for i in range(3))
        print("  [kappa*tau] = {}  (m^-2)".format(fmt_dim(kt_dim)))
        print()
        B("V3-f", "该单一类中 hbar 的值依赖 (kappa*tau)^{:.0f}/2 的**取值**，"
                  "而 kappa 与 tau 是局域场量、其取值由外加尺度 L_p 决定"
                  "（验证 4 已证明 L_p 必为外加）。"
                  "故该式虽量纲正确且不显式循环，仍**把自由度假定给了场量初值**，"
                  "不构成 hbar 的导出。".format(s_kt / 2.0))
        F("V3-f-verdict", "综合 V3-a（纯几何量量纲封锁）、V3-c（循环性理由被推翻）、"
                         "V3-f（量纲可行情形依赖外加场量初值）、V3-d（自由度 2，hbar 初值必外加）："
                         "**hbar 不可由体系现有量导出**。"
                         "但否决理由不是「量纲全部循环」，而是"
                         "「所有量纲可行情形都依赖某个外加尺度的初值」。")

# ================================================================ 验证 4
hdr("验证 4 | V3-d  公设自由度计数：A1 / A4 / A5 能否定出 hbar 的初值")

unknowns = ["L_p", "T_p", "hbar", "M_p"]
equations = [("A4 geometric speed", "c = L_p / T_p"),
             ("A5 info-mass", "M_p = hbar / (c * L_p)")]
n_unk = len(unknowns)
n_eq = len(equations)
dof = n_unk - n_eq

print("  未知量 {} 个：{}".format(n_unk, ", ".join(unknowns)))
print("  公设方程 {} 个：".format(n_eq))
for nm, eq in equations:
    print("    {:<22} {}".format(nm, eq))
print("  已知量：c（光速，实测量精确值）")
print()
print("  自由度 = 未知量 - 方程 = {} - {} = {}".format(n_unk, n_eq, dof))
print()

c_val = 2.99792458e8
HBAR_REAL = 1.054571817e-34
Lp = 1.0e-35
Tp = Lp / c_val
M_p = 1.0
hbar_try = M_p * c_val * Lp
print("  代入试探值 L_p = {:.3e} m, M_p = {:.3e} kg：".format(Lp, M_p))
print("    由 A4 得 T_p = L_p/c   = {:.6e} s".format(Tp))
print("    由 A5 得 hbar = M_p*c*L_p = {:.6e} kg m^2 s^-1".format(hbar_try))
print("    真实 hbar               = {:.6e} kg m^2 s^-1".format(HBAR_REAL))
print("    比值（试探/真实）       = {:.4f}".format(hbar_try / HBAR_REAL))
print("  => hbar 的初值随 (L_p, M_p) 的任意选取而任意变化，无任何公设固定它。")
print()

if dof > 0:
    F("V3-d", "公设自由度 = {} > 0：A1/A4/A5 共 {} 个方程对 {} 个未知量，欠定 {} 个自由度。"
              "探针验证：任意给定 L_p 与 M_p 即可算出任意 hbar（本次比值 {:.4f}，可任意调）。"
              "故 hbar 的初值**必为外加**，不能由现有公设导出。".format(
                  dof, n_eq, n_unk, dof, hbar_try / HBAR_REAL))
    I("V3-d-note", "注意 A1 把 hbar 列为元胞三元组之一 —— 这在体系内是**公设内容**"
                   "（假定其存在与量纲），不是推导结论。G4 的表述应据此改写。")

# ================================================================ 验证 5
hdr("验证 5 | V3-e  对照：SM 中 eps_s 与 hbar 的地位类比")

rows = [
    ("SM alpha", "e^2 = 4*pi*eps0*hbar*c*alpha", "由实验输入 1/137.036",
     "无量纲，但需 e 与 eps0"),
    ("SM eps_s", "m_s 回路 ∝ eps_s * Lambda_QCD", "由格点 QCD 输入 ~0.2 eV",
     "携带质量量纲"),
    ("S03-A5 M_p", "M_p = hbar/(c*L_p)", "hbar 与 L_p 均无来源",
     "hbar 未导出即无法定 M_p"),
]
print("  {:<16} {:<36} {:<24} {}".format("对象", "关系式", "输入来源", "量纲影响"))
for r in rows:
    print("  {:<16} {:<36} {:<24} {}".format(*r))
print()
B("V3-e", "地位类比成立：SM 的 eps_s 与 S03 的 hbar 在各自体系中都承担"
          "「把无量纲结构接到有量纲标度」的枢纽作用，且都**由实验输入**而非推导得出。"
          "即使 V18.3 承认 hbar 为外加标度，其角色**并不比 SM 更差**——"
          "差别只在名称：SM 显式承认，GAQ 此前把它误当作待导出量。"
          "**G4 的表述应从「缺口」改判为「公设边界」。**")

# ================================================================ 自检
hdr("自检")

CHECKS = []


def sc(name, ok, detail=""):
    CHECKS.append((name, ok))
    print("  [{}] {}{}".format("OK" if ok else "NG", name,
                               ("  " + detail) if detail else ""))


geom_mass_zero = all(v[0] == 0 for v in geom_basis)
sc("SC1 纯几何量集质量分量全为 0", geom_mass_zero)
sc("SC2 纯几何量集解数为 0（量纲封锁）", len(geom_sols) == 0,
   "{} 个解".format(len(geom_sols)))
sc("SC3 加入 G 后解数 > 0（量纲必要条件可满足）", len(full_sols) > 0,
   "{} 组解".format(len(full_sols)))
sc("SC4 剔除 Omega 后解数 > 0（先验断言被推翻）", len(no_omega_sols) > 0,
   "{} 组解（预期 0，实测非 0）".format(len(no_omega_sols)))
sc("SC5 不含 Omega 的解归约为单一量纲类",
   bool(no_omega_sols) and len(set(s[2] for s in no_omega_sols)) == 1
   and len(set(s[3] for s in no_omega_sols)) == 1
   and len(set(s[0] + s[1] for s in no_omega_sols)) == 1,
   "c/G 指数唯一且 kappa+tau 和唯一")
sc("SC6 公设自由度 = 2", dof == 2, "dof = {}".format(dof))
sc("SC7 探针：hbar 初值随输入任意变化（比值偏离 1）",
   abs(hbar_try / HBAR_REAL - 1.0) > 1e-3,
   "比值 {:.4f}".format(hbar_try / HBAR_REAL))
sc("SC8 穷举覆盖充分（四维组合数 > 2e4）", n_combo_geom >= 20000,
   "{} 组合".format(n_combo_geom))

# ================================================================ 汇总
hdr("判定汇总")
cnt = {}
for kind, name, detail in SOLUTIONS:
    cnt[kind] = cnt.get(kind, 0) + 1
    print("  [{}] {}".format(kind, name))
    print("         {}".format(detail))
print()
print("  统计：PASS={} FAIL={} BOUNDARY={} INFO={}  合计={}".format(
    cnt.get("PASS", 0), cnt.get("FAIL", 0), cnt.get("BOUNDARY", 0),
    cnt.get("INFO", 0), len(SOLUTIONS)))

n_ok = sum(1 for _, ok in CHECKS if ok)
print("  自检：{}/{} 通过".format(n_ok, len(CHECKS)))
print()
print("  红线声明：")
print("   - 量纲分析只给必要条件；V3-b 找到解不等于 hbar 可导出。")
print("   - **本册自我推翻**：原断言「量纲允许的形式全部循环」被 11 组反例推翻，")
print("     故循环性不作否决理由；真正的否决理由是 V3-d 的自由度计数与 V3-f 的初值依赖。")
print("   - V3-d 的探针只演示欠定，不声称任何 hbar 都行，只声称公设不固定它。")
print("   - V3-e 是地位类比，不是等价性证明，也不构成对 SM 的评价。")
print("   - 本册仍未对 GAQ 的任何主张给出正面支持证据。")

if n_ok == len(CHECKS):
    print()
    print("SELF-CHECK PASS ({}/{})".format(n_ok, len(CHECKS)))
    sys.exit(0)
else:
    print()
    print("SELF-CHECK FAIL")
    sys.exit(1)
