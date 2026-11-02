# -*- coding: utf-8 -*-
"""力的统一方程 Ⅱ：加速度场分解的判别力定价（正面对 X-R374-2）。

三个问题，各配机器读数：
 A) 复核 r374 P11 的「散度对偶」：刚性转动 v=Ω×r ⇒ a=−Ω²x⊥，∇·a=−2Ω²、∇×a=0、a=−∇(Ω²R²/2)。
 B) 判别力定价：牛顿与库仑的 a 场在 r>0 上**归一后逐点相同**、且都 (∇·a, ∇×a)=(0,0)
    ⇒ 「用分解认力」对"哪种力"给出 **0 bit**。
 C) 正对照：Yukawa / 线性禁闭 的 ∇·a 非零（−V/λ²、−2σ/r）
    ⇒ 分解确实有牙，但牙咬的是**源核**，而源核参数 (λ, σ) 是输入。

产物：同目录 _out_fm.txt
纪律：不占 r 号；数字自算；每条「零」都配正对照。
"""
import os

import mpmath as mp

from _criteria_kernel import surplus_of

mp.mp.dps = 30
HERE = os.path.dirname(os.path.abspath(__file__))
BUF = []
GUARD = {"pass": 0, "fail": 0}


def say(s=""):
    BUF.append(s)
    print(s)


def guard(name, ok, note):
    GUARD["pass" if ok else "fail"] += 1
    say("[%s] %-34s %s" % ("PASS" if ok else "FAIL", name, note))


def V(x, y, z):
    return [x, y, z]


def sub(a, b):
    return [a[i] - b[i] for i in range(3)]


def add(a, b):
    return [a[i] + b[i] for i in range(3)]


def sc(k, a):
    return [k * a[i] for i in range(3)]


def nrm(a):
    return mp.sqrt(sum(x * x for x in a))


# =====================================================================
# §A 复核 r374 P11：刚性转动的「有散无旋 + 梯度场」
# =====================================================================
say("=" * 78)
say("§A 复核 r374 P11：v=Ω×r 的加速度场对偶")
say("=" * 78)

Om = mp.mpf('1.7')


def a_cent(x, y, z):
    """a = Ω×(Ω×r) = −Ω²(x,y,0)"""
    return [-Om ** 2 * x, -Om ** 2 * y, mp.mpf(0)]


def div_field(fn, p, h=mp.mpf('1e-4')):
    d = mp.mpf(0)
    for k in range(3):
        pp = list(p)
        pm = list(p)
        pp[k] += h
        pm[k] -= h
        d += (fn(*pp)[k] - fn(*pm)[k]) / (2 * h)
    return d


def curl_field(fn, p, h=mp.mpf('1e-4')):
    def d(i, j):
        pp = list(p)
        pm = list(p)
        pp[j] += h
        pm[j] -= h
        return (fn(*pp)[i] - fn(*pm)[i]) / (2 * h)

    return [d(2, 1) - d(1, 2), d(0, 2) - d(2, 0), d(1, 0) - d(0, 1)]


p0 = [mp.mpf('0.3'), mp.mpf('0.4'), mp.mpf('0.5')]


def div_rich(fn, p, h=mp.mpf('2e-3')):
    """Richardson 外推：O(h²)→O(h⁴)，用于判「严格为零」的场量。"""
    d1 = div_field(fn, p, h)
    d2 = div_field(fn, p, h / 2)
    return (4 * d2 - d1) / 3


def curl_rich(fn, p, h=mp.mpf('2e-3')):
    c1 = curl_field(fn, p, h)
    c2 = curl_field(fn, p, h / 2)
    return [(4 * c2[i] - c1[i]) / 3 for i in range(3)]


dv_num = div_rich(a_cent, p0)
dv_closed = -2 * Om ** 2
cv_num = max(abs(c) for c in curl_rich(a_cent, p0))
# a = −∇(Ω²R²/2)
grad_phi = [Om ** 2 * p0[0], Om ** 2 * p0[1], mp.mpf(0)]
mx_grad = max(abs(a_cent(*p0)[i] + grad_phi[i]) for i in range(3))

say("  ∇·a = %.15e（闭式 −2Ω² = %.15e，相对差 %.2e）"
    % (dv_num, dv_closed, abs(dv_num - dv_closed) / abs(dv_closed)))
say("  |∇×a| = %.2e ；|a + ∇(Ω²R²/2)| = %.2e" % (cv_num, mx_grad))
guard("P11_DIV_CLOSED", abs(dv_num - dv_closed) / abs(dv_closed) < mp.mpf('1e-9'),
      "∇·a=−2Ω² 复现（r374 记 −5.78 = −2×1.7²，此处同值；Richardson 后残差 %.1e）" % abs(dv_num - dv_closed))
guard("P11_CURL_ZERO", cv_num < mp.mpf('1e-9'), "∇×a=0（有散无旋，与 r374 一致）")
guard("P11_GRADIENT", mx_grad < mp.mpf('1e-30'), "a 是梯度场（a=−∇(Ω²R²/2)）")

# =====================================================================
# §B 判别力定价：牛顿 vs 库仑 —— 分解完全相同
# =====================================================================
say()
say("=" * 78)
say("§B 判别力定价：牛顿与库仑的 a 场分解")
say("=" * 78)


def a_gravity(x, y, z, C=mp.mpf(1)):
    r = mp.sqrt(x * x + y * y + z * z)
    return [-C * x / r ** 3, -C * y / r ** 3, -C * z / r ** 3]


def a_coulomb(x, y, z, C=mp.mpf('2.5')):
    r = mp.sqrt(x * x + y * y + z * z)
    return [C * x / r ** 3, C * y / r ** 3, C * z / r ** 3]


GRID = [(mp.mpf(k) / 10, mp.mpf(j) / 10, mp.mpf('0.3'))
        for k in (3, 5, 7) for j in (2, 4, 6)]
mx_divN = mp.mpf(0)
mx_divE = mp.mpf(0)
mx_curl = mp.mpf(0)
for p in GRID:
    mx_divN = max(mx_divN, abs(div_rich(a_gravity, p)))
    mx_divE = max(mx_divE, abs(div_rich(a_coulomb, p)))
    mx_curl = max(mx_curl, max(abs(c) for c in curl_rich(a_gravity, p)),
                  max(abs(c) for c in curl_rich(a_coulomb, p)))
say("  网格 %d 点（Richardson）：max|∇·a_牛顿| = %.2e ；max|∇·a_库仑| = %.2e ；max|∇×a| = %.2e"
    % (len(GRID), mx_divN, mx_divE, mx_curl))
guard("NEWTON_HARMONIC", mx_divN < mp.mpf('1e-6'),
      "原点外 ∇·a=0（r>0 上严格调和；残差为 Richardson 后差分误差，非物理）")
guard("COULOMB_HARMONIC", mx_divE < mp.mpf('1e-6'), "库仑场同为零散（同上）")
guard("BOTH_CURL_FREE", mx_curl < mp.mpf('1e-6'), "两者都无旋 ⇒ (∇·a, ∇×a)=(0,0) 的签名完全相同")

# 归一后逐点相同（容许整体符号）：形状不可区分，只有常数（耦合）不同
ref_n = nrm(a_gravity(*GRID[0]))
ref_e = nrm(a_coulomb(*GRID[0]))
mx_shape = mp.mpf(0)
for p in GRID:
    un = sc(1 / ref_n, a_gravity(*p))
    ue = sc(1 / ref_e, a_coulomb(*p))
    mx_shape = max(mx_shape, max(abs(abs(un[i]) - abs(ue[i])) for i in range(3)))
say("  归一化后逐点最大差（容许整体符号）= %.2e（共 %d 点）" % (mx_shape, len(GRID)))
guard("SHAPE_INDISTINGUISHABLE", mx_shape < mp.mpf('1e-25'),
      "R̂/R² 形状完全同一 ⇒ 分解给「哪种力」0 bit；差异只是一个常数（G M 或 k Q/m）")

# =====================================================================
# §C 正对照：有牙的情形 —— Yukawa 与线性禁闭的 ∇·a
# =====================================================================
say()
say("=" * 78)
say("§C 正对照：Yukawa / 线性禁闭 的 ∇·a 非零")
say("=" * 78)

lam = mp.mpf('0.25')
sig = mp.mpf('0.3')


def phi_yuk(x, y, z, g=mp.mpf(1)):
    r = mp.sqrt(x * x + y * y + z * z)
    return -g * mp.e ** (-r / lam) / r


def a_yuk(x, y, z):
    h = mp.mpf('1e-4')
    return [-((phi_yuk(x + h, y, z) - phi_yuk(x - h, y, z)) / (2 * h)),
            -((phi_yuk(x, y + h, z) - phi_yuk(x, y - h, z)) / (2 * h)),
            -((phi_yuk(x, y, z + h) - phi_yuk(x, y, z - h)) / (2 * h))]


def lap(fn, p, h=mp.mpf('2e-4')):
    x, y, z = p
    return ((fn(x + h, y, z) - 2 * fn(x, y, z) + fn(x - h, y, z)
             + fn(x, y + h, z) - 2 * fn(x, y, z) + fn(x, y - h, z)
             + fn(x, y, z + h) - 2 * fn(x, y, z) + fn(x, y, z - h)) / h ** 2)


p = [mp.mpf('0.4'), mp.mpf('0.5'), mp.mpf('0.6')]
yuk_num = lap(phi_yuk, p)
yuk_closed = phi_yuk(*p) / lam ** 2
say("  Yukawa：∇²φ = %.12e ；φ/λ² = %.12e ；相对差 %.2e"
    % (yuk_num, yuk_closed, abs(yuk_num - yuk_closed) / abs(yuk_closed)))
guard("YUKAWA_DIV_MASS_TERM", abs(yuk_num - yuk_closed) / abs(yuk_closed) < mp.mpf('1e-5'),
      "∇·a = −∇²φ = −φ/λ² ≠ 0 ⇒ 有质量交换给出非零散度，**有牙**")

a_lin = lambda x, y, z: sc(-sig, sc(1 / mp.sqrt(x * x + y * y + z * z), [x, y, z]))
lin_num = div_rich(a_lin, p)
r_ = mp.sqrt(sum(c * c for c in p))
lin_closed = -2 * sig / r_
say("  线性禁闭：∇·a 数值 = %.12e（闭式 −2σ/r = %.12e，相对差 %.2e）"
    % (lin_num, lin_closed, abs(lin_num - lin_closed) / abs(lin_closed)))
guard("LINEAR_DIV_NONZERO", abs(lin_num - lin_closed) / abs(lin_closed) < mp.mpf('1e-8'),
      "线性势给出 1/r 型散度 ⇒ 同样有牙，且闭式可对拍")

# =====================================================================
# §D 供给账：四力 ↔ 四个源核
# =====================================================================
say()
say("=" * 78)
say("§D 供给账：分解认出的是**源核**，源核要参数")
say("=" * 78)

KERNELS = [
    ("引力（无质量，1/r 势）", "∇·a = 0 (r>0)，源为 δ ⇒ 需 G, M"),
    ("库仑（无质量，1/r 势）", "∇·a = 0 (r>0)，源为 δ ⇒ 需 k=1/4πε₀, Q"),
    ("Yukawa（有质量）", "∇·a = −φ/λ² ⇒ 需 g, λ（=ħ/M_W c）"),
    ("线性禁闭", "∇·a = −2σ/r ⇒ 需 σ"),
]
for k, v in KERNELS:
    say("  %-22s %s" % (k, v))

n_out = 4            # 四条力（在同一 r 上的数值）
n_in = 4             # 至少四个耦合：G M / kQ / g,λ / σ
surplus = surplus_of(n_out, n_in)
say("  输出 %d ｜ 输入 ≥ %d ⇒ surplus = %d ⇒ %s"
    % (n_out, n_in, surplus, "GENUINE_PREDICTION" if surplus >= 1 else "RELATION_OR_FIT"))
guard("KERNEL_SUPPLY", surplus < 1,
      "「场方程 + 源核」仍是四个源核并排；被分解认出的是耦合，不是统一")

# =====================================================================
# §E 对照：把「形状」当判别量会翻车（负对照）
# =====================================================================
say()
say("=" * 78)
say("§E 负对照：用 |a| 的径向指数认力")
say("=" * 78)

def radial_index(ar, r1, r2):
    """dln|a|/dln r 的差分估计：log(|a(r2)|/|a(r1)|)/log(r2/r1)。"""
    return mp.log(abs(ar(r2)) / abs(ar(r1))) / mp.log(r2 / r1)


gr = lambda rr: a_gravity(rr, 0, 0)[0]
yr = lambda rr: a_yuk(rr, 0, 0)[0]
idx_g = radial_index(gr, mp.mpf(1), mp.mpf(2))
idx_y = radial_index(yr, mp.mpf(1), mp.mpf(2))
say("  牛顿：局部指数 = %.4f（应为 −2）" % idx_g)
say("  Yukawa(λ=0.25)：同式读数 = %.4f（不是 −2）" % idx_y)
guard("INDEX_DISCRIMINATES", abs(idx_g + 2) < mp.mpf('1e-6') and abs(idx_y + 2) > mp.mpf('0.3'),
      "径向指数能分开「幂律 vs 指数」，但**不能**分开同指数同形状的引力与库仑")

# =====================================================================
say()
say("=" * 78)
say("守卫 %d/%d 通过" % (GUARD["pass"], GUARD["pass"] + GUARD["fail"]))
verdict = ("P11_DUALITY_REPRODUCED__"
           "DECOMPOSITION_BLIND_TO_WHICH_FORCE__"
           "SOURCE_KERNELS_NEED_COUPLINGS__"
           "X_R374_2_EQUALS_FOUR_PARALLEL_SOURCES")
say("判词：%s" % verdict)
say("=" * 78)

with open(os.path.join(HERE, "_out_fm.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(BUF) + "\n")
say("日志: %s" % os.path.join(HERE, "_out_fm.txt"))
raise SystemExit(0 if GUARD["fail"] == 0 else 1)
