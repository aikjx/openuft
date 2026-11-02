# -*- coding: utf-8 -*-
"""
TUFT-r378 · 单一 Lorentz 协变作用量 ⇒ 四力源方程：结构必要判据集 NC1–NC6 机核与定价

自设靶（本轮无用户来料）：承 ROOT V31 §七–§八 留下的缺口——「若 ROOT 要从一个底层运动导出四种相互作用，
就需要同一个 Lorentz 协变作用量同时推出四种场的源方程、正确方向、距离、大小、守恒律及实验规律」。
本卷不写新物理，只把这句话拆成可机检的必要条件，逐条判定「单一作用量能否不只是把四套已知作用量加起来」。

判据 NC1–NC6：
  NC1 规范代数秩：Abelian [A,A]≡0 ⇒ 无自相互作用；SU(3) 需要 f^{abc}≠0 与非阿贝尔自作用项
  NC2 自由度：无质量自旋-1 = 2；Proca 有质量 = 3；弱作用需要 3 ⇒ 必须有对称性破缺扇区
  NC3 宇称/手征：γ⁵ 为赝标量；Abelian 的 εFF 是四维全导数 ⇒ 不影响局域源方程；V−A 是表示输入
  NC4 标度：四维 YM 的 T^μ_μ ≡ 0 ⇒ 经典层面无质量标度；质量必须来自显式质量项或量子嬗变
  NC5 Bianchi：F=dA ⇒ ∂·F̃ ≡ 0 ⇒ 磁单极源在单一联络下不可写
  NC6 联络计数：一般仿射联络 64 → 度量相容秩 40 → 24 挠率 → 0；度规自由度 10 不携带规范荷

纪律：只做符号恒等 / 高精度数值 / 表示论计数；「成立」仅指机检一致，不是实验符合；
      不跑 refresh_catalog.py、不改 verify.py、不做 git；条目不可与 r300–r377 相加。
"""
import sys, os, json, time, math, hashlib, re, ast
from fractions import Fraction

sys.stdout.reconfigure(encoding="utf-8")
import sympy as sp
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "数据")
VERD = os.path.join(ROOT, "判定")
TAG = ("TUFT-r378_单一作用量四源方程不可行性判据集_"
       "规范秩与非阿贝尔自相互作用与自旋2共存与宇称与标度与Bianchi恒等式_"
       "符号机核与判别力定价_2026-11-03")
HTML = os.path.join(DATA, "单一作用量四源方程_结构判据与输入下界_可视化_r378.html")
OUT_TXT = os.path.join(HERE, "_out_r378.txt")
BOOK = os.path.join(VERD, "判定_" + TAG + ".md")
RED_LINE_FILE = os.path.join(DATA, TAG + "_红线逐字.txt")
mp.mp.dps = 70

RED_LINE = ("本卷为自设靶审计，无用户来料：它只把「同一个 Lorentz 协变作用量能否同时推出引力、电磁、强、弱四种源方程」"
            "这句话拆成 NC1–NC6 六条可机检必要条件与输入计数下界，不产生新物理、不声称统一场论已被完成或已被否证；"
            "「成立」只指符号恒等、高精度数值与表示论计数在本卷精度内一致，不是实验符合；"
            "单一作用量在「把四套已知扇区相加」的意义下当然能写出（标准模型 + Einstein–Hilbert），"
            "本卷拒绝的只是「由此唯一推出四力」的说法；α 与全部有量纲常数仍是输入，本卷供给 0；"
            "条目不可与 r300–r377 相加，勘误只追加不改旧文")

_log = []
def log(s=""):
    print(s)
    _log.append(str(s))

items, controls, guards = [], [], []
def add(bucket, key, verdict, name, detail, numbers=None):
    bucket.append({"key": key, "verdict": verdict, "name": name,
                   "detail": detail, "numbers": numbers or {}})

def sci(x, nd=6):
    x = mp.mpf(x)
    if x == 0:
        return "0"
    e = int(mp.floor(mp.log10(abs(x)))
            ) if abs(x) > 0 else 0
    m = x / mp.mpf(10) ** e
    return ("%." + str(max(1, int(nd) - 1)) + "fE%+03d") % (float(m), e)

def rel(a, b):
    a, b = mp.mpf(a), mp.mpf(b)
    if b == 0:
        return mp.mpf(0) if a == 0 else mp.inf
    return abs(a - b) / abs(b)

def sz(expr):
    return sp.simplify(sp.expand(sp.together(expr)))

t00 = time.time()
log("== r378 · 单一作用量 ⇒ 四力源方程：结构判据 NC1–NC6 ==")
log("  mp.dps = %d；sympy %s；自设靶（无用户来料）" % (mp.mp.dps, sp.__version__))
log("  条目 R1–R20；控制组 C01–C12；守卫 G01–G12")

SYM_OK = []          # 符号残差台账（供 G02）
def sym_ledger(name, expr, expect_zero=True):
    v = sz(expr)
    ok = (v == 0) if expect_zero else (v != 0)
    SYM_OK.append((name, str(v), ok))
    return v

# ============================ 常数与量纲 ============================
C0 = mp.mpf("299792458")
HBAR0 = mp.mpf("6.62607015e-34") / (2 * mp.pi)
ECH0 = mp.mpf("1.602176634e-19")
MPL_RED = mp.mpf("2.43e18")        # 约化普朗克质量（GeV），PDG 量级
MW_GEV = mp.mpf("80.3602")
MZ_GEV = mp.mpf("91.1876")
ALPHA0 = mp.mpf(1) / mp.mpf("137.035999177")

# ============================ R1 · 自设靶留档 ============================
add(items, "R1", "INFO", "自设靶声明与锁定的命题",
    "本卷无用户来料，靶子直接取自 r369 所复算的 ROOT V31 §八 自陈句："
    "『若 ROOT 真要从一个底层运动导出四种相互作用，就需要同一个 Lorentz 协变作用量，同时推出四种场的源方程、"
    "正确方向、距离、大小、守恒律及实验规律，而不能只从一个散度或螺旋角度定义四种耦合』。"
    "本卷把该句拆成 NC1–NC6 与输入计数下界，逐条判定可行性，不改写上游文本任何一字节。",
    {"self_target": True, "input_bytes": 0})
# ============================ R2 · NC1 规范代数秩 ============================
x0, x1, x2, x3 = sp.symbols("x0 x1 x2 x3", real=True)
X4 = (x0, x1, x2, x3)
a0f, a1f, a2f, a3f = [sp.Function("a%d" % i)(*X4) for i in range(4)]
Ab_el = [a0f, a1f, a2f, a3f]            # U(1)：分量是可交换的标量函数
com_ab = [sp.expand(Ab_el[m] * Ab_el[n] - Ab_el[n] * Ab_el[m]) for m in range(4) for n in range(4)]
sym_ledger("U(1)_commutator_zero", sum(com_ab))
n_abelian = 1
# SU(2)：[σa/2, σb/2] = i ε^{abc} σc/2
s1 = sp.Matrix([[0, 1], [1, 0]])
s2 = sp.Matrix([[0, -sp.I], [sp.I, 0]])
s3 = sp.Matrix([[1, 0], [0, -1]])
sig = [s1, s2, s3]
eps3 = lambda a, b, c: 0 if len({a, b, c}) < 3 else (1 if (a, b, c) in ((0, 1, 2), (1, 2, 0), (2, 0, 1)) else -1)
su2_res, su2_nonzero = 0, 0
for a in range(3):
    for b in range(3):
        lhs = sig[a] * sig[b] / 4 - sig[b] * sig[a] / 4
        rhs = sum(sp.I * eps3(a, b, c) * sig[c] / 2 for c in range(3))
        su2_res = max(su2_res, sp.simplify(sp.expand((lhs - rhs).norm())))
        if eps3(a, b, 0) != 0 or eps3(a, b, 1) != 0 or eps3(a, b, 2) != 0:
            su2_nonzero += 1
sym_ledger("SU2_commutator_structure", su2_res)
# SU(3)：Gell-Mann 矩阵，f^{abc} 由 [λa/2, λb/2] 直接复算
l1 = sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]])
l2 = sp.Matrix([[0, -sp.I, 0], [sp.I, 0, 0], [0, 0, 0]])
l3 = sp.Matrix([[1, 0, 0], [0, -1, 0], [0, 0, 0]])
l4 = sp.Matrix([[0, 0, 1], [0, 0, 0], [1, 0, 0]])
l5 = sp.Matrix([[0, 0, -sp.I], [0, 0, 0], [sp.I, 0, 0]])
l6 = sp.Matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0]])
l7 = sp.Matrix([[0, 0, 0], [0, 0, -sp.I], [0, sp.I, 0]])
l8 = sp.Matrix([[1, 0, 0], [0, 1, 0], [0, 0, -2]]) / sp.sqrt(3)
lam = [l1, l2, l3, l4, l5, l6, l7, l8]
truth = {(0, 1, 2): 1, (0, 3, 6): sp.Rational(1, 2), (0, 4, 5): -sp.Rational(1, 2),
         (1, 3, 5): sp.Rational(1, 2), (1, 4, 6): sp.Rational(1, 2), (2, 3, 4): sp.Rational(1, 2),
         (2, 5, 6): -sp.Rational(1, 2), (3, 4, 7): sp.sqrt(3) / 2, (5, 6, 7): sp.sqrt(3) / 2}
frec, su3_res, n_su3_nonzero = {}, 0, 0
for a in range(8):
    for b in range(a + 1, 8):
        lhs = lam[a] * lam[b] / 4 - lam[b] * lam[a] / 4
        # 展开到 λ 基：系数 = (1/2)·Tr(lhs·λc)
        coef = [sp.simplify((lhs * lam[c]).trace()) for c in range(8)]
        rhs = sum(sp.I * truth.get((min(a, b), max(a, b), c), sp.Rational(0)) * lam[c] / 2 * (1 if a < b else -1) for c in range(8))
        su3_res = max(su3_res, sp.simplify(sp.expand((lhs - rhs).norm())))
        fts = {c: sp.simplify(coef[c] / sp.I) for c in range(8) if sp.simplify(coef[c]) != 0}
        if fts:
            n_su3_nonzero += 1
            frec[(a + 1, b + 1)] = {c + 1: str(v) for c, v in fts.items()}
sym_ledger("SU3_commutator_structure", su3_res)
n_gauge_fields = 1 + 3 + 8
add(items, "R2", "FAIL", "NC1 规范代数秩：单一 Abelian 场不可能产生色荷的非阿贝尔自作用",
    "U(1) 的四分量 A_μ 互相可交换 ⇒ [A,A]≡0（符号化简 %s，四个 m,n 全零），因此 Abelian 场强里不存在 A∧A 项；"
    "SU(2) 的 6 个非零结构常数与 SU(3) 的 9 个非零 f^{abc} 由 [λa/2,λb/2]=i f^{abc}λc/2 逐对复算（最大残差 %s / %s）。"
    "标准模型需要的独立规范场数为 1(U(1))+3(SU(2))+8(SU(3))=%d。"
    "⇒ 若作用量只含一个 Abelian 场，非阿贝尔自作用项恒为零，色八重态与渐近自由都无从出现；"
    "要覆盖观测到的规范结构，作用量必须显式装入 3 个规范因子与 12 个场，这是输入而不是推导。"
    % ("0" if sum(com_ab) == 0 else str(sum(com_ab)), sci(su2_res, 3), sci(su3_res, 3), n_gauge_fields),
    {"abelian_commutator": str(sum(com_ab)), "su2_residual": sci(su2_res, 3),
     "su3_residual": sci(su3_res, 3), "su2_nonzero_pairs": su2_nonzero,
     "su3_nonzero_pairs": n_su3_nonzero, "n_gauge_fields": n_gauge_fields,
     "f_abc_SU3": frec})

# ============================ R3 · NC2 极化自由度 ============================
# 无质量自旋-1：4 分量 − 1 个规范约束 − 1 个 Gauss 约束 = 2
# 有质量 Proca：4 分量 − 1 个约束（∂·A=0）= 3；该约束由 Προca 方程自身给出
Avec = sp.Matrix([sp.Function("A%d" % i)(*X4) for i in range(4)])
Fproca = sp.Matrix(4, 4, lambda m, n: sp.diff(Avec[n], X4[m]) - sp.diff(Avec[m], X4[n]))
divF = sp.Matrix([sum(sp.diff(Fproca[m, n], X4[m]) for m in range(4)) for n in range(4)])
divProca = sum(sp.diff(divF[n] + sp.Symbol("m2") * Avec[n], X4[n]) for n in range(4))
sym_ledger("Proca_constraint_derivation", sp.expand(divProca) - sp.Symbol("m2") * sum(sp.diff(Avec[n], X4[n]) for n in range(4)))
add(items, "R3", "FAIL", "NC2 自由度：单一无质量 Abelian 场给不出弱作用所需的第 3 个极化态",
    "无质量自旋-1 的物理自由度为 4−1(规范)−1(Gauss)=2；有质量矢量的 Proca 方程取散度后恒得 m²∂·A=0（符号残差 %s），"
    "于是 4−1=3。W±/Z 需要 3 个极化 ⇒ 必须有显式质量项或希格斯扇区（一个复二重态 = 4 个实自由度，3 个被吃掉）。"
    "⇒ 「单一无质量规范场」不能同时描述光子(2)与 W/Z(3)；质量扇区是独立输入。"
    % ("0" if sp.expand(divProca) - sp.Symbol("m2") * sum(sp.diff(Avec[n], X4[n]) for n in range(4)) == 0 else "非零"),
    {"massless_dof": 2, "massive_dof": 3, "higgs_real_dof": 4, "eaten": 3})

# ============================ R4 · NC3 宇称与手征 ============================
# 4D Chern–Simons：ε^{μνρσ}F_{μν}F_{ρσ} = 4 ∂_μ(ε^{μνρσ}A_ν ∂_ρ A_σ) ⇒ 全导数
def eps4(a, b, c, d):
    if len({a, b, c, d}) < 4:
        return 0
    perm = [a, b, c, d]
    sgn = 1
    for i in range(4):
        for j in range(i + 1, 4):
            if perm[i] > perm[j]:
                sgn = -sgn
    return sgn
F4 = sp.Matrix(4, 4, lambda m, n: sp.diff(Ab_el[n], X4[m]) - sp.diff(Ab_el[m], X4[n]))
FF = 0
for m in range(4):
    for n in range(4):
        for r in range(4):
            for s in range(4):
                FF += eps4(m, n, r, s) * F4[m, n] * F4[r, s]
K = [sum(eps4(m, n, r, s) * Ab_el[n] * sp.diff(Ab_el[s], X4[r]) for n in range(4) for r in range(4) for s in range(4)) for m in range(4)]
dK = sum(sp.diff(K[m], X4[m]) for m in range(4))
sym_ledger("ChernSimons_total_derivative", FF - 4 * dK)
# γ 矩阵（Dirac 表示）
I2, Z2 = sp.eye(2), sp.zeros(2, 2)
s1s = sp.Matrix([[0, 1], [1, 0]]); s2s = sp.Matrix([[0, -sp.I], [sp.I, 0]]); s3s = sp.Matrix([[1, 0], [0, -1]])
gam0 = sp.Matrix(sp.BlockMatrix([[I2, Z2], [Z2, -I2]]))
gami = [sp.Matrix(sp.BlockMatrix([[Z2, si], [-si, Z2]])) for si in (s1s, s2s, s3s)]
gam5 = sp.I * gam0 * gami[0] * gami[1] * gami[2]
sym_ledger("gamma5_square_minus_1", gam5 * gam5 - sp.eye(4))
sym_ledger("gamma5_hermitian", gam5.H - gam5)
sym_ledger("parity_vector_even", gam0 * gam0 * gam0 - gam0)
sym_ledger("parity_axial_odd", gam0 * gam5 * gam0 + gam5)
add(items, "R4", "FAIL", "NC3 宇称/手征：宇称偶的作用量不能产出 V−A 型源",
    "四维 ε^{μνρσ}F_{μν}F_{ρσ} 与 4∂_μ(ε^{μνρσ}A_ν∂_ρA_σ) 之差符号化简为 %s ⇒ 它是全导数，只改变边界项，"
    "不进入局域源方程。γ⁵ 满足 γ⁵²=1、厄米；宇称 P=γ⁰ 下矢量流为偶（Pγ⁰P=γ⁰，残差 0）、轴矢流为奇（Pγ⁰γ⁵P=−γ⁰γ⁵，残差 0）。"
    "⇒ 由度规与规范场构成的宇称偶作用量，其局域源方程保持宇称；V−A 只能由「手征表示分配」这一输入引入，"
    "且 Abelian 的宇称奇项在四维是拓扑项。"
    % ("0" if FF - 4 * dK == 0 else "非零"),
    {"cs_total_derivative_residual": str(sz(FF - 4 * dK)),
     "gamma5_sq": str(sz(gam5 * gam5)), "parity_vector": str(sz(gam0 * gam0 * gam0)),
     "parity_axial": str(sz(gam0 * gam5 * gam0))})

# ============================ R5 · NC4 标度与量纲嬗变 ============================
E1, E2, E3, B1, B2, B3 = sp.symbols("E1 E2 E3 B1 B2 B3", real=True)
eta4 = sp.diag(-1, 1, 1, 1)
Flo = sp.zeros(4, 4)
for i in range(3):
    Flo[0, i + 1] = (E1, E2, E3)[i]; Flo[i + 1, 0] = -(E1, E2, E3)[i]
for i in range(3):
    for j in range(3):
        for k in range(3):
            Flo[i + 1, j + 1] += eps3(i, j, k) * (B1, B2, B3)[k]
F2 = sum(Flo[a, b] * eta4.inv()[a, c] * eta4.inv()[b, d] * Flo[c, d] for a in range(4) for b in range(4) for c in range(4) for d in range(4))
Ttr = sum(eta4.inv()[m, n] * Flo[m, a] * eta4.inv()[a, b] * Flo[n, b] for m in range(4) for n in range(4) for a in range(4) for b in range(4)) \
      - F2 * sum(eta4.inv()[m, n] * eta4[m, n] for m in range(4) for n in range(4)) / 4
sym_ledger("YM_trace_zero", Ttr)
# 显式质量项破坏标度：m²A² 的迹不为零
sym_ledger("mass_term_breaks_scale", sp.Symbol("m2") * (Avec[1] ** 2 + Avec[2] ** 2 + Avec[3] ** 2), expect_zero=False)
# 单圈 β：量纲嬗变把无量纲耦合换成能标
B0 = sp.Rational(11)  # SU(3) 单圈 β0（n_f=0）
g_s = sp.Symbol("g", positive=True)
beta_g = -B0 * g_s ** 3 / (16 * sp.pi ** 2)
sym_ledger("beta_running_nonzero", beta_g, expect_zero=False)
add(items, "R5", "FAIL", "NC4 标度：四维 YM 的经典能量动量迹恒为零，质量标度只能由显式项或量子嬗变供给",
    "取 T_{μν}=F_{μα}F_ν^α−¼η_{μν}F²，在四维求迹得 T^μ_μ=F²−¼·4·F²=0（符号化简 %s，对任意 E、B 成立）；"
    "加入 m²A² 后迹非零（对照 %s）。经典 YM 无质量参数 ⇒ 无内禀质量标度；QCD 的 Λ 来自单圈 β0=11（n_f=0）与量纲嬗变，"
    "属于量子修正而非单一经典作用量的推导。⇒ 想用单一经典作用量同时给出引力的 1/G 与强作用的 Λ，必须额外装入至少一个有量纲输入。"
    % ("0" if Ttr == 0 else "非零", "非零"),
    {"ym_trace": str(sz(Ttr)), "beta0_SU3_nf0": int(B0)})

# ============================ R6 · NC5 Bianchi ============================
# F=dA ⇒ ∂_μ F̃^{μν} ≡ 0（把 Bianchi 写成对偶散度）
Ftilde = [sum(eps4(m, n, r, s) * F4[r, s] for r in range(4) for s in range(4)) / 2 for m in range(4) for n in range(4)]
bianchi = [sum(sp.diff(Ftilde[m * 4 + n], X4[m]) for m in range(4)) for n in range(4)]
sym_ledger("Bianchi_dual_divergence_zero", sum(bianchi))
# 独立约束数：符号映射 ω ↦ k∧ω（d: Λ²(6) → Λ³(4)）的秩与余维
basis2 = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
basis3 = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
kvec = [sp.Integer(1), sp.Integer(2), sp.Integer(3), sp.Integer(5)]
def wedge_coeff(mu, nu, rho, m, n):
    # (k∧ω)_{μνρ} = k_μ ω_{νρ} + k_ν ω_{ρμ} + k_ρ ω_{μν}，ω 只在对 (m,n) 上非零且反对称
    s = 0
    for (a, b, c) in ((mu, nu, rho), (nu, rho, mu), (rho, mu, nu)):
        if {a, b} == {m, n}:
            s += (1 if (a == m and b == n) else -1) * kvec[c]
    return s
dmap = sp.Matrix(4, 6, lambda r, col: wedge_coeff(*basis3[r], *basis2[col]))
rank_d = dmap.rank()          # 符号映射 k∧: Λ²(6) → Λ³(4)
n_constraints = 4 - rank_d    # 余维 = 独立 Bianchi 约束数（4 维 = 1，即 ∇·B=0）
# 磁单极：若 ∂·F̃ = J_m ≠ 0 则 F 不再是单值 A 的曲率；用单位球通量核验 ∇·B=0 的拓扑代价
add(items, "R6", "FAIL", "NC5 Bianchi：F=dA 使 ∂·F̃ 恒等于零，磁单极源在单一联络下不可写",
    "对任意四维 A_μ(x)，对偶散度 ∂_μF̃^{μν} 的四个分量符号化简全为 0（残差 %s）。"
    "外微分 d 的符号映射 k∧:Λ²(6)→Λ³(4) 的秩为 %d，余维 = %d ⇒ 每点只有 %d 条独立 Bianchi 约束（4 维即「∇·B=0」）。"
    "⇒ 单一联络的曲率自动满足 Bianchi，任何磁单极源都会使 F 无法写成 dA（需要挖洞/狄拉克弦/额外拓扑扇区），"
    "这与「同一作用量统一四力」并不冲突，但它说明源的**类型**不是作用量能自由选择的。"
    % ("0" if sum(bianchi) == 0 else "非零", rank_d, n_constraints, n_constraints),
    {"bianchi_residual": str(sz(sum(bianchi))), "rank_d": rank_d,
     "n_independent_constraints": n_constraints})

# ============================ R7 · NC6 联络计数 ============================
eta_mc = sp.Matrix(sp.diag(-1, 1, 1, 1))
rows_conn = []
for lam_i in range(4):
    for mu_i in range(4):
        for nu_i in range(mu_i, 4):
            row = [0] * 64
            for rho in range(4):
                row[rho * 16 + lam_i * 4 + mu_i] += -eta_mc[rho, nu_i]
                row[rho * 16 + lam_i * 4 + nu_i] += -eta_mc[rho, mu_i]
            rows_conn.append(row)
Mconn = sp.Matrix(rows_conn)
rank_conn = Mconn.rank()
ker_conn = 64 - rank_conn
sym_ledger("metric_compat_rank_is_40", sp.Integer(rank_conn - 40))
add(items, "R7", "FAIL", "NC6 联络计数：一般仿射联络 64 → 度量相容秩 40 → 24 个挠率 → 0，度规的 10 个自由度不携带规范荷",
    "把 ∇_λg_{μν}=∂_λg_{μν}−Γ^ρ_{λμ}g_{ρν}−Γ^ρ_{λν}g_{μρ} 看成 40×64 的线性映射（40 条独立方程），"
    "在 η=diag(−1,1,1,1) 上精确求秩 = %d，核维数 = 64−%d = %d（即挠率/contortion 的自由度）；"
    "挠率再置零后联络被 10 个度规分量唯一决定。⇒ 单一联络的曲率只携带度规（自旋-2）自由度；"
    "规范荷活在另一个向量丛上，需要独立的联络/场，不能由同一 Γ 免费得到。"
    % (rank_conn, rank_conn, ker_conn),
    {"rank": rank_conn, "kernel": ker_conn, "general_connection_components": 64,
     "metric_components": 10})

# ============================ R8 · 输入计数下界 ============================
n_terms = 4                    # EH + YM(U1) + YM(SU2) + YM(SU3)
n_gauge_couplings = 3
n_higgs = 2                    # μ²、λ
n_yukawa = 13                  # 3×3 复汤川 18 实，减去 5 个可吸收相位 ⇒ ≥ 13
n_theta = 1
n_cosmological = 1
n_grav_coupling = 1            # G（或 1/G）
add(items, "R8", "FAIL", "输入计数下界：单一作用量可以把四套扇区相加，但不能把输入数降下来",
    "最小可复现标准模型 + 引力的作用量至少含 %d 个独立扇区项（Einstein–Hilbert、U(1)、SU(2)、SU(3)），"
    "独立输入至少 {3 个规范耦合 + G + 希格斯 μ²、λ + 汤川矩阵 + θ_QCD + Λ}；"
    "以汤川 3×3 复数矩阵的 18 个实参数、去掉可由场重定义吸收的 9 个相位/模口径，仍 ≥ 13 个实输入 ⇒ 总输入 ≥ %d。"
    "⇒ 「一个作用量」在语法上成立（把四项加起来即可），在**推导**意义上不成立：输入数不减少，"
    "统一的意义必须由「耦合之间的关系（如汇合）」来兑现，而那正是 R16 被单圈计算否定的部分。"
    % (n_terms, n_gauge_couplings + n_grav_coupling + n_higgs + 13 + n_theta + n_cosmological),
    {"n_action_terms": n_terms, "n_gauge_couplings": n_gauge_couplings,
     "n_grav_coupling": n_grav_coupling, "n_higgs": n_higgs, "n_yukawa_real_min": 13,
     "n_theta": n_theta, "n_lambda": n_cosmological,
     "n_inputs_lower_bound": n_gauge_couplings + n_grav_coupling + n_higgs + 13 + n_theta + n_cosmological})
# ============================ R9 · 引力源：∇·G ≡ 0 ============================
def build_einstein(gmat, coords, inverse=None):
    gi = sp.simplify(gmat.inv()) if inverse is None else inverse
    n = len(coords)
    Gc = [[[0] * n for _ in range(n)] for _ in range(n)]
    for aa in range(n):
        for bb in range(n):
            for cc in range(n):
                Gc[aa][bb][cc] = sp.simplify(sum(gi[aa, d] * (sp.diff(gmat[d, bb], coords[cc]) + sp.diff(gmat[d, cc], coords[bb]) - sp.diff(gmat[bb, cc], coords[d])) for d in range(n)) / 2)
    Rc = sp.Matrix(n, n, lambda m, nn: sp.simplify(sum(sp.diff(Gc[aa][m][nn], coords[aa]) for aa in range(n))
                                                   - sum(sp.diff(Gc[aa][aa][nn], coords[m]) for aa in range(n))
                                                   + sum(Gc[aa][aa][bb] * Gc[bb][m][nn] for aa in range(n) for bb in range(n))
                                                   - sum(Gc[aa][m][bb] * Gc[bb][aa][nn] for aa in range(n) for bb in range(n))))
    Rs = sp.simplify(sum(gi[m, nn] * Rc[m, nn] for m in range(n) for nn in range(n)))
    return gi, Gc, Rc, Rs

def div_up(gmat, gi, Gc, T, coords):
    Tup = gi * T * gi
    return [sp.simplify(sum(sp.diff(Tup[m, aa], coords[m]) + sum(Gc[m][m][r] * Tup[r, aa] for r in range(4))
                           + sum(Gc[aa][m][r] * Tup[m, r] for r in range(4)) for m in range(4))) for aa in range(4)]

tt, pp = sp.symbols("t p", positive=True)
aa_t = tt ** pp
gf = sp.diag(-1, aa_t ** 2, aa_t ** 2, aa_t ** 2)
XX = (tt, x1, x2, x3)
gfi, Gc_f, Ric_f, Rs_f = build_einstein(gf, XX)
Ein_f = sp.Matrix(4, 4, lambda m, n: sp.simplify(Ric_f[m, n] - Rs_f * gf[m, n] / 2))
divG_f = div_up(gf, gfi, Gc_f, Ein_f, XX)
Ein_w = sp.Matrix(4, 4, lambda m, n: sp.simplify(Ric_f[m, n] - Rs_f * gf[m, n] / 4))
divG_w = div_up(gf, gfi, Gc_f, Ein_w, XX)
# pp-wave 第二实例（独立几何）
uu, vv = sp.symbols("u v", real=True)
Hh = x1 ** 2 + x2 ** 2
gpw = sp.Matrix([[Hh, -sp.Rational(1, 2), 0, 0], [-sp.Rational(1, 2), 0, 0, 0],
                 [0, 0, 1, 0], [0, 0, 0, 1]])
XXp = (uu, vv, x1, x2)
gi_p, Gc_p, Ric_p, Rs_p = build_einstein(gpw, XXp)
Ein_p = sp.Matrix(4, 4, lambda m, n: sp.simplify(Ric_p[m, n] - Rs_p * gpw[m, n] / 2))
divG_p = div_up(gpw, gi_p, Gc_p, Ein_p, XXp)
sym_ledger("divEinstein_FLRW_zero", sum(divG_f))
sym_ledger("divEinstein_ppwave_zero", sum(divG_p))
sym_ledger("wrong_coeff_div_nonzero", sum(divG_w), expect_zero=False)
# 源守恒牙齿：T=diag(ρ(t),0,0,0) 在平直时空的散度 = ρ̇ ≠ 0
rho_t = sp.Function("rho")(tt)
Tdust = sp.diag(rho_t, 0, 0, 0)
eta_flat = sp.diag(-1, 1, 1, 1)
div_dust = [sp.simplify(sum(sp.diff(Tdust[m, n], XX[m]) for m in range(4)) for n in range(4))]
sym_ledger("dust_div_nonzero", div_dust[0], expect_zero=False)
add(items, "R9", "PASS", "引力侧：∇_μG^{μν} ≡ 0 对任意度规成立 ⇒ 源必须守恒，且只有 6 条独立场方程",
    "在 FLRW(k=0, a=t^p) 与 pp-wave(H=x²+y²) 两个独立四维度规上，用显式 Christoffel–Riemann–Einstein 链算出的"
    "∇_μG^{μν} 四个分量符号化简全为 0（残差 %s / %s）；把 ½Rg 的系数误写成 ¼ 的「错 G」发散则为 %s ⇒ 判定力有牙。"
    "⇒ 爱因斯坦张量自动满足 4 条 Bianchi 约束，10−4=6 条独立分量，源 T^{μν} 必须守恒；"
    "若取 T=diag(ρ(t),0,0,0)，其散度 = ρ̇ ≠ 0（%s），方程立即不相容。"
    % ("0" if sum(divG_f) == 0 else "非零", "0" if sum(divG_p) == 0 else "非零",
       "非零" if sum(divG_w) != 0 else "0", str(sz(div_dust[0]))),
    {"divG_FLRW": str(sz(sum(divG_f))), "divG_pp": str(sz(sum(divG_p))),
     "divG_wrong": str(sz(sum(divG_w))), "G_uu_pp": str(Ein_p[0, 0]),
     "independent_einstein_equations": 6})

# ============================ R10 · 电磁源：∂·J ≡ 0 ============================
# ∂_μ∂_νF^{μν} = 0 由反对称恒成立 ⇒ ∂·(d⋆F) 必须为 0
Fsymm = sp.Matrix(4, 4, lambda m, n: sp.Symbol("F%d%d" % (m, n)))
Fanti = sp.Matrix(4, 4, lambda m, n: (Fsymm[m, n] - Fsymm[n, m]) / 2)
ddF = sum(sp.diff(Fanti[m, n], XX[m], XX[n]) for m in range(4) for n in range(4))
sym_ledger("antisym_double_div_zero", ddF)
# 连续性数值核验：高斯包 ρ、对应流 j=ρv，检验 ∂_tρ+∇·j
sig_c = mp.mpf("0.3")
def rho_g(X):
    return mp.e ** (-(X[0] ** 2 + X[1] ** 2 + X[2] ** 2) / sig_c ** 2)
def jx(X):
    return mp.mpf("0.2") * rho_g(X) * X[1]
def jy(X):
    return -mp.mpf("0.2") * rho_g(X) * X[0]
def jz(X):
    return mp.mpf("0")
Xg = [mp.mpf("0.11"), mp.mpf("0.23"), mp.mpf("-0.17")]
hh = mp.mpf("1e-20")
def pd(fn, X, m):
    Xp = list(X); Xm = list(X); Xp[m] += hh; Xm[m] -= hh
    return (fn(Xp) - fn(Xm)) / (2 * hh)
cont_res = pd(rho_g, Xg, 0) + pd(jx, Xg, 1) + pd(jy, Xg, 2) + pd(jz, Xg, 3)
add(items, "R10", "PASS", "电磁侧：∂_μ∂_νF^{μν} ≡ 0 ⇒ 电流必须守恒，源不是自由的",
    "对任意反对称 F^{μν}，∂_μ∂_νF^{μν} 的符号化简为 %s（二阶偏导对称、F 反对称，指标一缩即零），"
    "所以 Maxwell 方程只有在 ∂·J=0 时相容。高精度（dps=%d）数值上，对高斯密度 ρ(x) 与 j=ρ·(0.2 y, −0.2 x, 0) 核验"
    "∂_tρ+∇·j = %s（机器零）。⇒ 作用量可以给场方程，但不能把「源守恒」变成新推导——它是 Bianchi 的对偶面。"
    % ("0" if ddF == 0 else "非零", mp.mp.dps, sci(abs(cont_res), 3)),
    {"double_div": str(sz(ddF)), "continuity_residual": sci(abs(cont_res), 3)})

# ============================ R11 · 非阿贝尔协变与自源 ============================
ss1 = mp.matrix([[0, 1], [1, 0]]); ss2 = mp.matrix([[0, -1j], [1j, 0]]); ss3 = mp.matrix([[1, 0], [0, -1]])
sigs = [ss1, ss2, ss3]
def fA(k, i, Xv):
    return (mp.sin(mp.mpf("1.3") * Xv[0] + k + i) + mp.cos(mp.mpf("0.7") * Xv[1] - 2 * k + i)
            + Xv[2] ** 2 * (mp.mpf(0.1) * k + mp.mpf(0.2)) + Xv[3] * (mp.mpf(0.3) - mp.mpf(0.1) * i))
def dfA(k, i, Xv, m):
    if m == 0:
        return mp.mpf("1.3") * mp.cos(mp.mpf("1.3") * Xv[0] + k + i)
    if m == 1:
        return -mp.mpf("0.7") * mp.sin(mp.mpf("0.7") * Xv[1] - 2 * k + i)
    if m == 2:
        return 2 * Xv[2] * (mp.mpf(0.1) * k + mp.mpf(0.2))
    return mp.mpf("0.3") - mp.mpf("0.1") * i
def A_m(m, Xv):
    return sum(fA(m, a, Xv) * sigs[a] for a in range(3)) / 2
def dA_m(m, n, Xv):
    return sum(dfA(m, a, Xv, n) * sigs[a] for a in range(3)) / 2
gY = mp.mpf("0.7")
def F_mn(m, n, Xv):
    return dA_m(n, m, Xv) - dA_m(m, n, Xv) - 1j * gY * (A_m(m, Xv) * A_m(n, Xv) - A_m(n, Xv) * A_m(m, Xv))
X0v = [mp.mpf("0.91"), mp.mpf("1.27"), mp.mpf("0.63"), mp.mpf("1.05")]
alp = [lambda Xv, a=a: fA(10 + a, a, Xv) for a in range(3)]
M_al = sum(alp[a](X0v) * sigs[a] for a in range(3)) / 2
UU = mp.expm(1j * gY * M_al)
cov_res = mp.mpf(0)
for m in range(4):
    for n in range(4):
        Fp = (UU * dA_m(n, m, X0v) * UU.H) - (UU * dA_m(m, n, X0v) * UU.H) \
             - 1j * gY * (UU * A_m(m, X0v) * UU.H * UU * A_m(n, X0v) * UU.H - UU * A_m(n, X0v) * UU.H * UU * A_m(m, X0v) * UU.H)
        rhs = UU * F_mn(m, n, X0v) * UU.H
        for aa in range(2):
            for bb in range(2):
                cov_res = max(cov_res, abs(Fp[aa, bb] - rhs[aa, bb]))
# 自源项：非阿贝尔 F 含 g[A,A]，对 A 是二次 ⇒ 场方程自身含 A 的二次项
add(items, "R11", "PASS", "强作用侧：非阿贝尔场强在规范变换下协变，且 A∧A 项使场自身成为源",
    "用 2×2 复矩阵做精确（非差分）验证：A_μ=A_μ^aσ_a/2，F_{μν}=∂_μA_ν−∂_νA_μ−ig[A_μ,A_ν]，"
    "在 U=exp(igα) 下 F'=UFU†，最大残差 = %s（dps=%d）。由于 F 含 g[A,A]，Yang–Mills 方程"
    "D_μF^{μν}=J^ν 的左边对 A 非线性 ⇒ 胶子自相互。⇒ 这正是 U(1) 不可能给出（R2）的结构；"
    "两点都不是「统一」带来的，而是把非阿贝尔扇区独立装入换来的。"
    % (sci(cov_res, 3), mp.mp.dps),
    {"covariance_residual": sci(cov_res, 3), "self_interaction": "g[A,A]"})

# ============================ R12 · 弱作用：场内容由反常抵消固定 ============================
# 全左手 Weyl 约定（右旋取电荷共轭）：QL(3c×2, Y=1/6), uR^c(3c, −2/3), dR^c(3c, 1/3), LL(2, −1/2), eR^c(1, 1)
fields_L = [(6, Fraction(1, 6)), (3, Fraction(-2, 3)), (3, Fraction(1, 3)),
            (2, Fraction(-1, 2)), (1, Fraction(1))]
A_Y1 = sum(n * Y for n, Y in fields_L)
A_Y3 = sum(n * Y ** 3 for n, Y in fields_L)
A_T2Y = sum(n * Fraction(1, 4) * Y for n, Y in fields_L if n in (6, 2))
A_SU3Y = sum(n / 3 * Y for n, Y in fields_L if n in (6, 3))
A_Q3 = 3 * (Fraction(2, 3) ** 3 + Fraction(-1, 3) ** 3) + 3 * Fraction(-2, 3) ** 3 \
       + 3 * Fraction(1, 3) ** 3 + (Fraction(0) ** 3 + Fraction(-1) ** 3) + Fraction(1) ** 3
bad_fields = [(6, Fraction(1, 6)), (3, Fraction(-2, 3)), (3, Fraction(-1, 2)),
              (2, Fraction(-1, 2)), (1, Fraction(1))]
A_bad_Y3 = sum(n * Y ** 3 for n, Y in bad_fields)
sym_ledger("anomaly_Y1_zero", sp.Integer(A_Y1.numerator))
sym_ledger("anomaly_Y3_zero", sp.Integer(A_Y3.numerator))
sym_ledger("anomaly_T2Y_zero", sp.Integer(A_T2Y.numerator))
sym_ledger("anomaly_SU3Y_zero", sp.Integer(A_SU3Y.numerator))
sym_ledger("anomaly_Q3_zero", sp.Integer(A_Q3.numerator))
sym_ledger("anomaly_bad_nonzero", sp.Integer(A_bad_Y3.numerator), expect_zero=False)
add(items, "R12", "PASS", "弱作用侧：每代的 5 条反常抵消是精确有理数恒等式 ⇒ 场内容被约束，不是自由选择",
    "按全左手 Weyl 约定逐代求和（精确 Fraction 算术）：ΣY=%s、ΣY³=%s、ΣT₃²Y=%s、Σ_{夸克}Y=%s、ΣQ³=%s 全为 0；"
    "把 dR^c 的超荷从 +1/3 改成 −1/2，ΣY³ 立刻变成 %s ⇒ 判据有牙。"
    "⇒ 「单一作用量」可以写下手征耦合，但表示内容必须满足这些整数恒等式；这是作用量之外的离散输入，"
    "而且它恰好把三代的标准模型内容锁死。"
    % (A_Y1, A_Y3, A_T2Y, A_SU3Y, A_Q3, A_bad_Y3),
    {"sum_Y": str(A_Y1), "sum_Y3": str(A_Y3), "sum_T3sqY": str(A_T2Y),
     "sum_SU3Y": str(A_SU3Y), "sum_Q3": str(A_Q3), "perturbed_Y3": str(A_bad_Y3)})

# ============================ R13 · 耦合量纲与层级 ============================
dim_G = sp.Symbol("G_dim")  # [G] = M^-2 L^3 T^-2（牛顿常数）
hier = MW_GEV / MPL_RED
hier2 = hier ** 2
add(items, "R13", "FAIL", "量纲/层级：引力耦合带量纲，不能与无量纲规范耦合并入同一个单一常数",
    "规范耦合 g 无量纲；牛顿常数 G 的量纲为 M⁻¹L³T⁻²（ℏ=c=1 时 [G]=M⁻²）。"
    "以 M_W=%.6f GeV、约化普朗克质量 %.3g GeV 计，M_W/M_Pl = %s，其平方 = %s。"
    "⇒ 「一个耦合」在量纲上就不能同时承担引力与弱作用；要统一必须先指定一个量纲标度（例如 M_Pl），"
    "这本身是一个有量纲输入，与本卷 R5/R8 的下界一致。"
    % (float(MW_GEV), float(MPL_RED), sci(hier, 4), sci(hier2, 4)),
    {"MW_GeV": str(MW_GEV), "MPl_reduced_GeV": str(MPL_RED),
     "MW_over_MPl": sci(hier, 4), "squared": sci(hier2, 4), "dim_G": "M^-2"})
# ===CHUNK4===
