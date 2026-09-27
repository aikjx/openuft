# -*- coding: utf-8 -*-
"""
推导与量纲专题 · 量纲核验脚本

零第三方依赖（仅 Python 标准库 fractions），对专题五个任务的量纲结论做精确有理数验算。

核验项：
  T2  SI 量纲总表逐项；E=-grad(phi)；B=curl(A)；div(E)=rho/eps0
  T3  mu0*eps0 量纲；1/sqrt(mu0*eps0) 为速度量纲；组合唯一性（4 方程 2 未知线性方程组）
  T4  由 B=curl(A) 反推 [A]；4 势分量量纲统一；规范函数 lambda 量纲；q*lambda/hbar 无量纲
  T1  [Gamma]=L^-1；[R]=L^-2；[G_{mu nu}]=L^-2；爱因斯坦场方程两侧量纲 L^-2
  T5  SI 规范协变导数耦合项 (q/hbar)*A_mu 与 d_mu 同量纲；[F_{mu nu}]=[B]

基本量纲顺序：(M, L, T, I)
"""

import sys
from fractions import Fraction as F

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def dim(m=0, l=0, t=0, i=0):
    """构造量纲向量 (M, L, T, I)，分量为有理数。"""
    return (F(m), F(l), F(t), F(i))


def mul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def div(a, b):
    return tuple(x - y for x, y in zip(a, b))


def pow_dim(a, k):
    k = F(k)
    return tuple(x * k for x in a)


def show(a):
    names = ["M", "L", "T", "I"]
    parts = []
    for n, v in zip(names, a):
        if v == 0:
            continue
        if v == 1:
            parts.append(n)
        else:
            parts.append(n + "^" + str(v))
    return "1" if not parts else " ".join(parts)


PASS = 0
FAIL = 0
INFO = 0


def check(name, left, right):
    """核验 left 与 right 量纲相等。"""
    global PASS, FAIL
    ok = tuple(left) == tuple(right)
    if ok:
        PASS += 1
        print("[PASS] " + name + " : " + show(left) + " == " + show(right))
    else:
        FAIL += 1
        print("[FAIL] " + name + " : " + show(left) + " != " + show(right))
    return ok


def check_scalar(name, left, right):
    """核验两个标量（有理数）相等，用于唯一性线性方程组的解。"""
    global PASS, FAIL
    ok = F(left) == F(right)
    if ok:
        PASS += 1
        print("[PASS] " + name + " : " + str(left) + " == " + str(right))
    else:
        FAIL += 1
        print("[FAIL] " + name + " : " + str(left) + " != " + str(right))
    return ok


def info(name, text):
    global INFO
    INFO += 1
    print("[INFO] " + name + " : " + text)


# ---------------------------------------------------------------- 基础量纲
M = dim(m=1)
L = dim(l=1)
T = dim(t=1)
I = dim(i=1)
ONE = dim()

# ------------------------------------------------------- SI 电磁量纲（T2 表）
D_PHI = dim(m=1, l=2, t=-3, i=-1)      # 电势 phi : V
D_E = dim(m=1, l=1, t=-3, i=-1)        # 电场 E : V/m
D_A = dim(m=1, l=1, t=-2, i=-1)        # 磁矢势 A : T*m   （A1 修正项）
D_B = dim(m=1, t=-2, i=-1)             # 磁感应强度 B : T
D_RHO = dim(i=1, t=1, l=-3)            # 电荷密度 rho : C/m^3
D_J = dim(i=1, l=-2)                   # 电流密度 J : A/m^2
D_EPS0 = dim(m=-1, l=-3, t=4, i=2)     # eps0 : F/m
D_MU0 = dim(m=1, l=1, t=-2, i=-2)      # mu0 : H/m
D_NABLA = dim(l=-1)                    # 3 维 Nabla
D_DT = dim(t=-1)                       # 时间偏导
D_C = div(L, T)                        # 光速
D_Q = mul(I, T)                        # 电荷 q
D_HBAR = dim(m=1, l=2, t=-1)           # hbar
D_G = dim(m=-1, l=3, t=-2)             # 牛顿引力常数 G

print("=" * 72)
print("T2 · 电磁学 SI 量纲核验")
print("=" * 72)

check("E = -grad(phi)", mul(D_NABLA, D_PHI), D_E)
check("B = curl(A)", mul(D_NABLA, D_A), D_B)
check("div(E) = rho/eps0", mul(D_NABLA, D_E), div(D_RHO, D_EPS0))
check("4 梯度 d_mu 量纲 = L^-1（x^0 = c t）", div(D_DT, D_C), D_NABLA)
check("达朗贝尔算子 square 量纲 = L^-2", pow_dim(D_NABLA, 2), dim(l=-2))

print()
print("=" * 72)
print("T3 · 光速 c 的量纲来源与唯一性")
print("=" * 72)

check("[mu0 * eps0] = L^-2 T^2", mul(D_MU0, D_EPS0), dim(l=-2, t=2))
check("1/sqrt(mu0*eps0) 为速度量纲", pow_dim(mul(D_MU0, D_EPS0), F(-1, 2)), D_C)

# 唯一性：求 a,b 使 eps0^a * mu0^b 量纲 = L T^-1
# 方程组（按 M,L,T,I 顺序）：-a+b=0 ; -3a+b=1 ; 4a-2b=-1 ; 2a-2b=0
A_rows = [
    (F(-1), F(1)),
    (F(-3), F(1)),
    (F(4), F(-2)),
    (F(2), F(-2)),
]
rhs = [F(0), F(1), F(-1), F(0)]

# 用前两式解 2x2 线性方程组
a11, a12 = A_rows[0]
a21, a22 = A_rows[1]
det = a11 * a22 - a12 * a21
if det == 0:
    FAIL += 1
    print("[FAIL] 唯一性：前两式系数矩阵奇异，无法确定唯一性")
else:
    b1, b2 = rhs[0], rhs[1]
    a = (b1 * a22 - a12 * b2) / det
    b = (a11 * b2 - b1 * a21) / det
    ok_all = all(
        A_rows[k][0] * a + A_rows[k][1] * b == rhs[k] for k in range(len(A_rows))
    )
    check_scalar("唯一性：a = -1/2", a, F(-1, 2))
    check_scalar("唯一性：b = -1/2", b, F(-1, 2))
    if ok_all:
        PASS += 1
        print("[PASS] 唯一性：4 个方程全部相容，解唯一 => 组合 (mu0*eps0)^(-1/2) 唯一")
    else:
        FAIL += 1
        print("[FAIL] 唯一性：解不满足全部方程")
info("A7 物理边界",
     "2019 SI 修订后 c 为定义常数、mu0 由 alpha 导出，量纲分析只给形式与恒等式 eps0*mu0*c^2=1，不给数值")

print()
print("=" * 72)
print("T4 · 磁矢势与 4 势量纲反推")
print("=" * 72)

check("由 B=curl(A) 反推 [A]（A1 修正值）", div(D_B, D_NABLA), D_A)
check("4 势时间分量 [phi/c]", div(D_PHI, D_C), D_A)
check("4 势四分量量纲统一", D_A, dim(m=1, l=1, t=-2, i=-1))
check("规范函数 [lambda] = [A]*L", mul(D_A, L), dim(m=1, l=2, t=-2, i=-1))
check("规范变换时间分量 [d_t lambda] = [phi]", mul(D_DT, mul(D_A, L)), D_PHI)
check("Aharonov-Bohm 相位 q*lambda/hbar 无量纲",
      div(mul(D_Q, mul(D_A, L)), D_HBAR), ONE)

print()
print("=" * 72)
print("T1 · 广义相对论侧量纲核验")
print("=" * 72)

D_GAMMA = D_NABLA                      # [Gamma] = [partial g] = L^-1
D_RIEM = mul(D_NABLA, D_GAMMA)         # [R] = L^-2
check("[Gamma] = L^-1", D_GAMMA, dim(l=-1))
check("[Riemann] = L^-2", D_RIEM, dim(l=-2))
check("[R_{mu nu}] = L^-2（缩并不改量纲）", D_RIEM, dim(l=-2))
check("[R] = L^-2", D_RIEM, dim(l=-2))
check("[G_{mu nu}] = L^-2", D_RIEM, dim(l=-2))
check("[Lambda] = L^-2", dim(l=-2), D_RIEM)
D_TMUNU = div(mul(dim(m=1, l=2, t=-2), dim(l=-3)), ONE)   # 能量密度 M L^-1 T^-2
check("[T_{mu nu}] = 能量密度 M L^-1 T^-2", D_TMUNU, dim(m=1, l=-1, t=-2))
check("爱因斯坦场方程两侧量纲 L^-2",
      mul(div(D_G, pow_dim(D_C, 4)), D_TMUNU), D_RIEM)

print()
print("=" * 72)
print("T5 · 规范协变导数量纲核验（A3 / A4 修正）")
print("=" * 72)

check("SI 规范耦合项 [(q/hbar) A_mu] = L^-1（A3 修正）",
      mul(div(D_Q, D_HBAR), D_A), D_NABLA)
check("[q*A_mu] = M L T^-1，与 [d_mu] = L^-1 不同 => SI 下原式无定义",
      mul(D_Q, D_A), dim(m=1, l=1, t=-1))
check("[F_{mu nu}] = [d_mu A_nu] = [B]", mul(D_NABLA, D_A), D_B)
check("[[D_mu, D_nu]] = L^-2（对易子量纲，非场强量纲）",
      pow_dim(D_NABLA, 2), dim(l=-2))
check("[(i hbar/q)[D_mu,D_nu]] = [F_{mu nu}]（A4 修正）",
      mul(div(D_HBAR, D_Q), pow_dim(D_NABLA, 2)), D_B)

print()
print("=" * 72)
print("汇总")
print("=" * 72)
print("PASS = " + str(PASS))
print("FAIL = " + str(FAIL))
print("INFO = " + str(INFO))
sys.exit(0 if FAIL == 0 else 1)
