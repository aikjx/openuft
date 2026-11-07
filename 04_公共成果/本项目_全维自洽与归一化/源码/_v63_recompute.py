# -*- coding: utf-8 -*-
"""ROOT V63 独立复算：Spin(12) 张量积阶数奇偶 / 手征指标偶数性 / 6D 磁通真空精确解 / 判别力审计。

原则：不抄来料公式，从组合公式与有效势变分从零推导，再与来料读数比对。
  A 层（Fraction 精确）：形式阶数结构、选择定则、q_Y 归一、整数/半整数双磁通网格
  B 层（线性代数）    ：质量配对秩恒等式与正负双对照
  C 层（6D 真空）     ：驻点闭式、Lambda* 闭式、Hessian、N 扫描、判别力双端
  D 层（判定）        ：重复结论、不相加声明、29/29 计数、四力未证、OPEN 闭合度
纪律：条目不可相加；纯陈述给 INFO；定义恒等式记 IDENTITY 不记 PASS；
      判据由闭式推导，不用任意 10 的幂；引用教科书结论 = 没算（一律 INFO）；
      负对照必须落在真正敏感方向且给出不同读数；守卫不得写死 ok。
整理册体例：不新增 RID、不进 README、不与任何卷条目相加。
注：控制台与落盘文案均避开 U+21D2 箭头字与 ASCII 双引号（承接 v62 复跑教训）。
"""
import os
import io
import json
import ast
from fractions import Fraction as F
from decimal import Decimal as D, getcontext
from math import comb

getcontext().prec = 60

TITLE = "ROOT V63 独立复算"
DATE = "2026-11-06"
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "数据")

ROWS = []
GUARDS = []


def add(rid, layer, name, exp, act, ok, note=""):
    if ok == "ID":
        kind = "IDENTITY"
    elif ok is None:
        kind = "INFO"
    else:
        kind = "PASS" if ok else "FAIL"
    ROWS.append({"id": rid, "layer": layer, "name": name, "exp": str(exp),
                 "act": str(act), "kind": kind, "note": note})
    print("  [%-8s] %-5s %s" % (kind, rid, name))
    return ok


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": str(detail)})
    print("  [GUARD %-4s] %-16s | %s" % ("ok" if ok else "BAD", name, detail))
    return ok


def fmt_f(q):
    q = F(q)
    return str(q.numerator) if q.denominator == 1 else "%d/%d" % (q.numerator, q.denominator)


def dec_sqrt_int(n):
    return D(int(n)).sqrt()


def near(v, tol=D("1e-40")):
    return abs(D(v)) < tol


print("=" * 78)
print(TITLE + "  " + DATE)
print("=" * 78)
print("\n[GUARD] 工具自检")
guard("FRAC-EXACT", F(1, 3) + F(1, 6) - F(1, 2) == 0, "1/3+1/6-1/2 = 0")

# ---- 参数（来料 63-8 的示范值，原样取用；本册不参与拟合）
m = F(1)             # M_6^4
g2 = F(1)            # g_6^2
lam = F(1)
mu2 = F(1, 2)
Lam = F(41, 144)
R0 = F(3, 2)
N0 = 3

phi0sq = mu2 / lam
V0 = -mu2 * mu2 / (4 * lam)
Vpp = -mu2 + 3 * lam * phi0sq
A = Lam + V0
COEF = 4 * R0**4     # 4*pi*R0^4 的 pi 系数（= 81/4）

# ---- 形式阶数结构（从组合公式从零枚举，不抄 63-4/63-5）
EVEN_ALL = [comb(12, k) for k in (0, 2, 4, 6, 8, 10, 12)]
ODD_ALL = [comb(12, k) for k in (1, 3, 5, 7, 9, 11)]
EVEN_HALF = EVEN_ALL[0] + EVEN_ALL[1] + EVEN_ALL[2] + EVEN_ALL[3] // 2
ODD_HALF = ODD_ALL[0] + ODD_ALL[1] + ODD_ALL[2]
guard("FORM-HALF",
      sum(EVEN_ALL) == 2048 and sum(ODD_ALL) == 2048 and EVEN_HALF == 1024 and ODD_HALF == 1024,
      "偶阶/奇阶全和 2048/2048；Hodge 折半 1024/1024")


# ---- 6D 有效势的通用闭式（全部由变分推导，非抄来料）
def disc(N):
    """固定 A=2/9 时驻点 16x^2-144x+27N^2=0 的判别式。"""
    return 144**2 - 4 * 16 * 27 * N * N


def roots_x(N):
    d = disc(N)
    if d < 0:
        return None
    s = dec_sqrt_int(d)
    return ((D(144) - s) / D(32), (D(144) + s) / D(32))


def G_frac(x, N):
    """括号项 A*x + N^2/(8x) - M6^4，Fraction 精确。"""
    return A * x + F(N * N, 8) / x - m


def H2_frac(x, N):
    """四维曲率读数口径（由来料三点反解）：G/(3x)。"""
    return G_frac(x, N) / (3 * x)


def G_dec(x, N):
    return (D(A.numerator) / D(A.denominator)) * x + D(N * N) / (D(8) * x) - D(1)


def H2_dec(x, N):
    return G_dec(x, N) / (D(3) * x)


def fpp_frac(x, N):
    """f''(x) = 2A/x^3 + (3N^2/2)/x^5 - 6m/x^4。"""
    return 2 * A / x**3 + F(3 * N * N, 2) / x**5 - 6 * m / x**4


def fp_frac(x, N):
    """f'(x) = -A/x^2 - (3N^2/8)/x^4 + 2m/x^3。"""
    return -A / x**2 - F(3 * N * N, 8) / x**4 + 2 * m / x**3


def flat_closed(N):
    """平直驻点的闭式：x*=N^2/(4 g2 m)，A*=2 g2 m^2/N^2，Lambda*=A*-V0。"""
    xs = F(N * N, 4) / (g2 * m)
    As = F(2, N * N) * (g2 * m * m)
    return xs, As, As - V0


def rank_frac(M):
    """Fraction 高斯消元求秩（用于质量配对矩阵的显式构造）。"""
    a = [row[:] for row in M]
    nr = len(a)
    nc = len(a[0]) if nr else 0
    r = 0
    for c in range(nc):
        piv = None
        for i in range(r, nr):
            if a[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        a[r], a[piv] = a[piv], a[r]
        pv = a[r][c]
        a[r] = [x / pv for x in a[r]]
        for i in range(nr):
            if i != r and a[i][c] != 0:
                f = a[i][c]
                a[i] = [a[i][j] - f * a[r][j] for j in range(nc)]
        r += 1
        if r == nr:
            break
    return r

print("\n[A] 精确群论：旋量张量积 / 选择定则 / 手征指标")

add("A01", "A", "Spin(12) 同手征旋量积 = 偶阶反对称形式（Hodge 折半），逐项维数",
    "1+66+495+462 = 1024",
    "偶阶 k=0,2,4,6 维数 %s ; 6-形式自对偶半 = %d ; 合计 %d"
    % (EVEN_ALL[:4], EVEN_ALL[3] // 2, EVEN_HALF),
    EVEN_HALF == 1024 and EVEN_ALL[:4] == [1, 66, 495, 924],
    "=> 63-4 的 1 / 66 / 495 / 462_+ 逐项复现；462 = C(12,6)/2 是自对偶 6-形式，"
    "不是凭空出现的第 4 个数；注意「+」这个手征标签不是由维数账算出来的（见 D02）")

add("A02", "A", "异手征旋量积 = 奇阶反对称形式（取 k<6 一半），逐项维数",
    "12+220+792 = 1024",
    "奇阶 k=1,3,5 维数 %s ; 合计 %d" % (ODD_ALL[:3], ODD_HALF),
    ODD_HALF == 1024 and ODD_ALL[:3] == [12, 220, 792],
    "=> 63-5 逐项复现；792 = C(12,5) 是 5-形式（奇阶），与 V62 整理册 A04 同一对象，"
    "同读数不新增证据")

add("A03", "A", "阶数奇偶是分解的结构原因：偶阶与奇阶全和都是 2 的 11 次方",
    "2048 / 2048，折半各 1024",
    "偶阶全和 %d ; 奇阶全和 %d ; 合计 %d = 2^12 ; 折半 %d / %d"
    % (sum(EVEN_ALL), sum(ODD_ALL), sum(EVEN_ALL) + sum(ODD_ALL), EVEN_HALF, ODD_HALF),
    sum(EVEN_ALL) == 2048 and sum(ODD_ALL) == 2048 and sum(EVEN_ALL) + sum(ODD_ALL) == 4096,
    "=> 不是「四个数刚好凑成 1024」：Clifford 双线性按形式阶数分层，"
    "12 维 Hodge 对偶把 k 与 12-k 配对，故各取一半；这是从组合公式算出的结构，非引文转述")

even_k = (0, 2, 4, 6)
odd_k = (1, 3, 5)
add("A04", "A", "792 能否进同手征积：用阶数集合判，不只用维数相加",
    "5 不在 even_k 且 5 在 odd_k",
    "even_k=%s ; odd_k=%s ; 5 in even=%s ; 5 in odd=%s ; C(12,5)=%d"
    % (even_k, odd_k, 5 in even_k, 5 in odd_k, comb(12, 5)),
    (5 not in even_k) and (5 in odd_k) and comb(12, 5) == 792,
    "=> 63-4 / 63-5 的选择定则在阶数层成立：792 属 Lambda^5，只在奇阶侧")

okA05 = (comb(12, 2) == 66) and (2 in even_k) and (5 not in even_k) and (comb(12, 2) != comb(12, 5))
add("A05", "A", "负对照：把 792 误认成 2-形式（C(12,2)=66），同手征侧是否包含它",
    "对照读数须与 A04 不同",
    "误认维数 %d ; 阶数 2 in even_k=%s ; 「不在同手征侧」在误认口径下 = %s ; A04 口径下 = %s"
    % (comb(12, 2), 2 in even_k, 2 not in even_k, 5 not in even_k),
    okA05,
    "=> 负控翻转：判据测的确实是「阶数奇偶」而非「维数和为 1024」；"
    "与 V62 整理册 E01（792 误当 2-形式）同族事故的正向利用")

QY = {"Q": F(1), "u^c": F(-4), "d^c": F(2), "L": F(-3), "e^c": F(6), "nu^c": F(0)}
MULT = {"Q": 6, "u^c": 3, "d^c": 3, "L": 2, "e^c": 1, "nu^c": 1}
tr_qy = sum(MULT[k] * v for k, v in QY.items())
add("A06", "A", "q_Y = 6Y 整数归一：六个 SM 多重态加权无迹（与 V62 A01 同口径）",
    "加权和为 0 且六值皆整数",
    "表 %s ; 加权和 %d" % ({k: fmt_f(v) for k, v in QY.items()}, tr_qy),
    tr_qy == 0 and all(v.denominator == 1 for v in QY.values()),
    "=> 整数磁通下 q_Y*N_Y 必为整数，这是 63-2 偶数性真正依赖的前提（来料把它当背景）；"
    "口径与 V62 整理册 A01 一致，不另立新归一")

GRID = list(range(-8, 9))
n_pairs = 0
n_even = 0
n_odd = 0
n_zero = 0
for NF in GRID:
    for NY in GRID:
        n_pairs += 1
        v = 2 * (F(NF) + F(1) * F(NY))
        if v == 0:
            n_zero += 1
        if v % 2 == 0:
            n_even += 1
        else:
            n_odd += 1
add("A07", "A", "289 组整数双磁通上 I_Q = 2(N_F+N_Y) 的奇偶性（来料 63-2）",
    "全偶（289 组）",
    "组数 %d ; 偶 %d ; 奇 %d ; 零指标组数 %d ; 297 组之外的网格未取"
    % (n_pairs, n_even, n_odd, n_zero),
    "ID",
    "=> 定义恒等式：2 乘整数 = 偶数，展开后无残差可算。按纪律记 IDENTITY，不记 PASS；"
    "289 = 17^2 只是网格大小，不是证据强度（来料「289 组整数双磁通」可核但不构成定理证明）")

HALF = [F(k, 2) for k in range(-8, 9)]
sol_int = [(p, q) for p in GRID for q in GRID if 2 * (F(p) + F(q)) == 3]
sol_half = [(fmt_f(p), fmt_f(q)) for p in HALF for q in HALF if 2 * (p + q) == 3]
add("A08", "A", "半整数磁通出口：I_Q = 2(N_F+N_Y) = 3 在整数网格与半整数网格上的解",
    "整数网格无解，半整数网格有解",
    "整数解数 %d ; 半整数解数 %d ; 前四个半整数解 %s"
    % (len(sol_int), len(sol_half), sol_half[:4]),
    len(sol_int) == 0 and len(sol_half) > 0,
    "=> 偶数障碍依赖「磁通为整数」这一前提；前提一松，I_Q=3 在纯代数层立刻有解。"
    "来料 §一 列的三条出路（边界投影 / 不同表示 / 新几何）未列此项；"
    "半整数磁通的物理合法性（量子化与 Dirac 条件）本册不判，见 D05")

NF3 = F(3)
v_net = 2 * (NF3 + F(1) * F(0))
v_single = NF3 + F(1) * F(0)
add("A09", "A", "计数约定双读数：合并共轭的 I_net 与单个 16 的 I_16（取 N_F=3, N_Y=0）",
    "两个读数须不同",
    "I_net=%s（偶） ; I_16=%s（奇） ; 比值 %s"
    % (fmt_f(v_net), fmt_f(v_single), fmt_f(v_net / v_single)),
    v_net == 6 and v_single == 3 and v_net != v_single,
    "=> 「偶数」是合并 16 与 16bar 计数的后果，不是指标本身的性质。"
    "本条只报两个口径的读数，不主张哪一个物理上更合法（避免读数支持不了的解读）")

print("\n[B] 线性代数：质量配对秩恒等式（63-3）与正负双对照")

base = [[F(1), F(0)], [F(0), F(1)], [F(2), F(1)], [F(1), F(3)], [F(0), F(2)]]
MAT = [row + [row[0] + row[1]] for row in base]
r = rank_frac(MAT)
PAIR_RANK = r        # 独立命名：防 Part3 的顶层 for r in ROWS 把秩覆盖成条目 dict（同名变量换对象刀）
nL, nR = 5, 3
diff_before = nL - nR
diff_after = (nL - r) - (nR - r)
add("B01", "B", "63-3 秩恒等式：构造 5x3 配对矩阵，成对去秩 r 后净手征差不变",
    "n'_L - n'_R = n_L - n_R = 2",
    "rank=%d ; 去秩前 (%d,%d) 差 %d ; 去秩后 (%d,%d) 差 %d"
    % (r, nL, nR, diff_before, nL - r, nR - r, diff_after),
    r == 2 and diff_before == 2 and diff_after == 2,
    "=> 63-3 在显式矩阵上成立（不是纯陈述）；前提是配对同时从 L 与 R 各去掉 r 个")

diff_wrong = (nL - r) - nR
add("B02", "B", "负对照：只从 L 侧去掉 r 个（非成对配对），差是否仍不变",
    "对照读数须与 B01 不同",
    "单侧去 r 后差 %d ; 成对差 %d ; 两者相同 = %s"
    % (diff_wrong, diff_after, diff_wrong == diff_after),
    diff_wrong == 0 and diff_wrong != diff_after,
    "=> 负控翻红：恒等式的成立依赖「成对消去」这一个条件；单侧删除会改净手征数，"
    "故判据测的是配对结构而不是任何秩不变性")

ranks = []
zeros = 0
for t in range(4):
    Mt = []
    for i in range(5):
        Mt.append([F(i + 1) ** j for j in range(t)] + [F(0)] * (3 - t))
    rt = rank_frac(Mt)
    ranks.append(rt)
    if rt == 0:
        zeros += 1
add("B03", "B", "全秩档覆盖 r=0,1,2,3（防退化点恒绿），并报零的个数",
    "四个秩档各给一个读数",
    "实测 rank 档 %s ; r=0 的档数 %d ; 四档差均为 2 = %s"
    % (ranks, zeros, all((5 - rt) - (3 - rt) == 2 for rt in ranks)),
    ranks == [0, 1, 2, 3] and zeros == 1,
    "=> 含 r=0 退化档（恒等式平凡成立）。按纪律显式报零的个数，"
    "不把退化点当作独立证据")

hit3 = 0
for NF in GRID:
    for NY in GRID:
        for rt in ranks:
            if 2 * (F(NF) + F(NY)) - 0 == 3:
                hit3 += 1
okB04 = (hit3 == 0) and (n_odd == 0) and all((5 - rt) - (3 - rt) == 2 for rt in ranks)
add("B04", "B", "整数双磁通 + 规范不变质量配对能否给出恰好 3 个净手征夸克双重态",
    "不能（I_Q 恒偶且配对保值）",
    "289 组 x 4 个秩档 = %d 次回代 ; 出现 3 的次数 %d ; 网格奇数指标数 %d"
    % (n_pairs * len(ranks), hit3, n_odd),
    not okB04,
    "=> FAIL 是来料 §一 的核心否定结论，已登记、不挡总门：63-1/63-2/63-3 联合把 3 排除。"
    "本册只证明「在这一计数约定与整数磁通下」不成立，不排除 A08 的半整数出口")

print("\n[C] 6D 磁通-标量真空：闭式驻点 / Hessian / N 扫描 / 判别力")

add("C01", "C", "63-8 的 phi_0 = 1/sqrt(2) 与 V(phi_0) = -1/16：由 phi_0^2 = mu^2/lambda 精确给出",
    "V'(phi_0)=0、V(phi_0)=-1/16、V''(phi_0)=1",
    "phi0^2=%s ; V0=%s ; V'(phi0)=phi0*(-mu2+lam*phi0^2)=0（精确） ; V''=%s"
    % (fmt_f(phi0sq), fmt_f(V0), fmt_f(Vpp)),
    phi0sq == F(1, 2) and V0 == F(-1, 16) and Vpp == 1,
    "=> 标量驻点是定义式 phi0*(-mu2+lam*phi0^2) 的零点，无需数值求根；"
    "注意 V''=2*mu2 与 lambda 无关，见 C06")

add("C02", "C", "Einstein 规范下有效势对 x=R^2 变分得到的驻点方程",
    "A*x^2 - 2*M6^4*x + 3*N^2/(8*g^2) = 0",
    "A=Lam+V0=%s ; 乘 72 得 16x^2-144x+27N^2=0 ; N=3 判别式 %d"
    % (fmt_f(A), disc(N0)),
    A == F(2, 9) and disc(N0) == 5184,
    "=> 63-7 的三种能量项变分后归为一个二次式；系数由 A=2/9 与 M6^4=g=1 决定")

x_small, x_large = roots_x(N0)
x0 = F(9, 4)
add("C03", "C", "N=3 小半径分支：R_0=3/2 与四维平直 H^2=0 的精确回代（Fraction）",
    "x=9/4、G(x)=0、H^2=0",
    "x_small=%s ; x_large=%s ; G(9/4)=%s ; H2(9/4)=%s"
    % (x_small, x_large, fmt_f(G_frac(x0, N0)), fmt_f(H2_frac(x0, N0))),
    x_small == D(9) / D(4) and G_frac(x0, N0) == 0 and H2_frac(x0, N0) == 0,
    "=> 63-8 逐位复现；来料只报小半径分支，大半径分支另见 C04；"
    "H^2 的口径由来料三点反解得到，见 D06")

xL = F(27, 4)
GL = G_frac(xL, N0)
HL = H2_frac(xL, N0)
f2L = fpp_frac(xL, N0)
add("C04", "C", "来料未报的大半径分支 x=27/4：四维曲率与半径模二阶导符号",
    "同 N=3 的第二实根存在",
    "x_large=%s ; G=%s ; H2=%s ; f''(x_large)=%s（%s）"
    % (fmt_f(xL), fmt_f(GL), fmt_f(HL), fmt_f(f2L), "正" if f2L > 0 else "负"),
    xL == F(27, 4) and GL > 0 and HL > 0 and f2L < 0,
    "=> 新读数：大半径分支是 dS（H^2=8/243>0）且半径模二阶导为负，故不稳定；"
    "来料「小半径分支」的命名由此得到解释，但来料未给该分支的稳定性")

f1 = fp_frac(x0, N0)
f2 = fpp_frac(x0, N0)
hRR = COEF * (f2 * 4 * x0 + f1 * 2)
hPP = COEF * Vpp / x0
hRP = 0
add("C05", "C", "63-9 Hessian：两个对角元与交叉项（pi 的系数，Fraction 精确）",
    "diag(64*pi/9, 9*pi)，交叉项 0",
    "f'(x0)=%s ; f''(x0)=%s ; d2V/dR2=%s*pi ; d2V/dphi2=%s*pi ; 交叉项=%d"
    % (fmt_f(f1), fmt_f(f2), fmt_f(hRR), fmt_f(hPP), hRP),
    f1 == 0 and hRR == F(64, 9) and hPP == F(9) and hRP == 0 and hRR > 0 and hPP > 0,
    "=> 63-9 逐位精确复现；交叉项为 0 不是假设，是 V'(phi0)=0 的直接后果；"
    "正定性只依赖两个对角元为正，与动能规范化系数（均为正）无关，故半径模 4/9 与标量模 1 的口径差不影响结论")

vpp_general = [-mu2 + 3 * lam * (mu2 / lam) for lam in (F(1), F(2), F(3))]
add("C06", "C", "判别力检验：V''(phi0) = 2*mu^2 恒成立（与 lambda 无关）",
    "读数须能区分「势函数形式」与「模型稳定性成就」",
    "V''=%s ; 2*mu2=%s ; lambda=1,2,3 时 V'' 分别 %s ; 三者全同 = %s"
    % (fmt_f(Vpp), fmt_f(2 * mu2), [fmt_f(v) for v in vpp_general], len(set(vpp_general)) == 1),
    Vpp == 2 * mu2 and len(set(vpp_general)) == 1,
    "=> 标量侧「质量平方 1」= 2*mu2，是四次势形式的输入，不是稳定性成就；"
    "只要实极小点存在，标量方向就恒正（100% 通过的谓词判别力为 0）。"
    "真正带信息的是半径方向 f''(x0)=256/6561>0，它依赖 A 与 N")

xs3, As3, Ls3 = flat_closed(N0)
lam_table = [(N, fmt_f(flat_closed(N)[0]), fmt_f(flat_closed(N)[2])) for N in range(1, 8)]
add("C07", "C", "Lambda_6 = 41/144 不是随手调的：它是 N=3 时平直驻点存在的唯一闭式解",
    "Lambda*(N) = 2*g^2*M6^8/N^2 + mu^4/(4*lambda)；N=3 给 41/144",
    "x*=%s ; A*=%s ; Lambda*(3)=%s ; N=1..7 的 (N, x*, Lambda*) = %s"
    % (fmt_f(xs3), fmt_f(As3), fmt_f(Ls3), lam_table),
    xs3 == F(9, 4) and As3 == F(2, 9) and Ls3 == F(41, 144),
    "=> 来料 §四 把 41/144 写成「人为选取」，实际可由驻点条件与平直条件联立解出且唯一。"
    "但正因为它可解出，每个 N 都配一个 Lambda*(N)（见 C10），所以「N=3」没有被选中")

exp_r2 = ["0.191578", "0.825765", "2.250000", None]
exp_h2 = ["-0.530596", "-0.085173", "0", None]
scan = []
for N in range(1, 5):
    rt = roots_x(N)
    if rt is None:
        scan.append((N, None, None, disc(N)))
    else:
        xd = rt[0]
        s_r2 = "%.6f" % float(xd)
        s_h2 = "0" if near(H2_dec(xd, N)) else "%.6f" % float(H2_dec(xd, N))
        scan.append((N, s_r2, s_h2, disc(N)))
match_r2 = all((scan[i][1] == exp_r2[i]) for i in range(4))
match_h2 = all((scan[i][2] == exp_h2[i]) for i in range(4))
add("C08", "C", "固定 Lambda=41/144 的 N 扫描：小半径 R^2 列与 H^2 列逐位复现",
    "0.191578 / 0.825765 / 2.250000 / 无实驻点；-0.530596 / -0.085173 / 0 / 无",
    "实算 %s ; R2 列逐格相符=%s ; H2 列逐格相符=%s"
    % (scan, match_r2, match_h2),
    match_r2 and match_h2,
    "=> 来料 §四 表格四行全部逐位复现（含 N=4 无实驻点）；H^2 采用 C03 反解口径，见 D06")

NSTAR = F(12)
add("C09", "C", "N=4 无实驻点的判据：判别式 D(N)=1728*(12-N^2)",
    "实驻点存在当且仅当 N^2 <= 12",
    "D(1)=%d ; D(2)=%d ; D(3)=%d ; D(4)=%d ; 临界 N*=sqrt(%s) 约 %s"
    % (disc(1), disc(2), disc(3), disc(4), fmt_f(NSTAR), "%.6f" % float(D(12).sqrt())),
    disc(4) < 0 and disc(3) > 0 and disc(N0) == 1728 * (12 - N0 * N0),
    "=> 「N=4 无实驻点」是固定 Lambda 后 N^2>12 的算术后果，"
    "不是磁通量子化的物理禁戒；允许 Lambda 随 N 走时任意 N 都有实驻点（C10）")

free_pass = sum(1 for N in range(1, 8) if flat_closed(N)[0] > 0)
fixed_flat = []
for N in range(1, 8):
    rt = roots_x(N)
    if rt is not None and near(H2_dec(rt[0], N)):
        fixed_flat.append(N)
add("C10", "C", "判别力双端：平直驻点条件是否单独挑出 N=3",
    "两端读数须不同（自由参数满射时判别力应为 0）",
    "Lambda 由平直条件解出：N=1..7 有平直驻点 %d/7 ; Lambda 冻结 41/144：H2=0 的 N 集合 %s（%d/7）; 两端不同=%s"
    % (free_pass, fixed_flat, len(fixed_flat), free_pass != len(fixed_flat)),
    free_pass == 7 and fixed_flat == [3] and free_pass != len(fixed_flat),
    "=> 来料 §四 已诚实写明「参数调谐的示范解」；本条把该承认量化为闭式 Lambda*(N)=2/N^2+1/16。"
    "冻结参数刀：把可调参数冻结在某一个样本上的解，再扫描其他样本，必然造出「该样本唯一」的假象。"
    "这不影响数值正确性，但表明「N=3 恰好平直」零判别力")

print("\n[D] 判定与诚实边界")

add("D01", "D", "V63 §一 自称「第一项关键发现」的偶数指标障碍是否为新增结论",
    "应与仓库既有登记对比",
    "r391 已登记「偶数族模二定理对任意族数成立」；r393 已登记「净手征恒偶故三代不可达」；本册 A07/B04 为同族复算",
    None,
    "=> INFO：不是新发现，是已登记定理在 Spin(12) 32 口径下的重述。按「条目不可相加」，不新增证据")

add("D02", "D", "V63 §二 的选择定则与 r402 / V62 整理册的关系",
    "应标明对象层级，避免相加",
    "本册 A01-A05 在 Spin(12) 32_+-32_- 形式阶数层；r402 在 SO(10) 16-16bar 矩阵层（Hom 双向为 0、Dirac 项唯一）；V62 A04/A09 在 5-形式与 U(1)_F 荷层",
    None,
    "=> INFO：互为印证、不相加。另记一处口径限制：A01 的 462_+ 中「+」是手征标签，"
    "维数账对 462_+ 与 462_- 给同一读数，故该标签不是本册算出来的（维数账分不开手征标记）")

add("D03", "D", "来料「29/29 通过」可否视为 29 项独立科学验证",
    "应给可独立复跑的逐项清单",
    "来料只给 9 行分类表与「29 项模型内数学断言」；本册以独立复算的 %d 条替代该计数" % 0,
    None,
    "=> INFO：与 V62 整理册 C03 的「492/492」同型。本册不追该数，不给假精度"
    "（note 中的占位在落盘前由 n_rows 回填，见守卫 G09）")

add("D04", "D", "四力统一与独立实验预言是否已证",
    "应同时得 SM 谱、三代、质量混合、量子一致与同一真空的引力",
    "来料 §五 明写「四种力的共同微观本源：尚未证明」；§七 明写引力未从同一机制推导；本册独立预言数 0",
    None,
    "=> INFO：这是来料自承的边界，不是本册新发现的漏洞；找到障碍 + 构造示范解 ≠ 统一已证")

add("D05", "D", "A08 的半整数磁通出口物理上是否合法",
    "需给紧致化上的磁通量子化与 Dirac 条件",
    "本册只在代数层枚举解集；未重建 S^2 上 U(1) 丛的量子化条件与 Spin(12) 权格约束",
    None,
    "=> INFO：不能由「方程有解」跳到「物理可实现」。仓库 r391/r392/r394 已对半整数出口定过价，本册不重复计数")

add("D06", "D", "H^2 列的口径来料是否明写",
    "应给四维曲率与有效势的关系式",
    "来料只给三个数值；本册由三点反解出 H^2=(A*x+N^2/(8x)-M6^4)/(3x)，N=1,2,3 逐位复现",
    None,
    "=> INFO：反解吻合不等于口径已验证。R^2 列与 Hessian 不依赖该口径，仍为独立精确复算")

add("D07", "D", "V62 整理册 §六 X-V62-3（ROOT-V63 变分方程与涨落质量矩阵）的闭合程度",
    "应给完整作用量的全谱涨落质量矩阵",
    "本册闭合：有效势闭式驻点、均匀子空间 2x2 Hessian、N 扫描、Lambda* 闭式；未闭合：KK 非均匀模、非阿贝尔带电矢量模、完整 792 全场作用量",
    None,
    "=> INFO：来料 §三 自承是「简化模型」、§三末自承「不是完整高维真空稳定性证明」；本册同口径收口")

add("D08", "D", "均匀子空间正定是否等于完整真空稳定",
    "应把所有涨落模纳入 Hessian",
    "本册 Hessian 为 2x2（rank 2），只覆盖半径与中性标量两个均匀模；来料自承非阿贝尔带电矢量模式可能不稳定",
    None,
    "=> INFO：C04 已在同一 2x2 框架内给出不稳定分支，说明该 Hessian 不是恒正；但秩 2 之外的模本册未算")

print("\n[GUARD] 判据反噬与汇总")

cnt = {}
for r in ROWS:
    cnt[r["kind"]] = cnt.get(r["kind"], 0) + 1
N_ROWS = len(ROWS)

guard("ENTRY-ACT", all(r["act"].strip() for r in ROWS) and all(r["exp"].strip() for r in ROWS),
      "%d 条均有 exp 与 act 读数" % N_ROWS)
guard("EXP-NEQ-ACT", all(r["exp"] != r["act"] for r in ROWS),
      "exp 与 act 文本全不相同的条数 %d / %d（同义反复的最弱防线，非 AST 级证明）"
      % (sum(1 for r in ROWS if r["exp"] != r["act"]), N_ROWS))

neg_pairs = [(5 not in even_k, 2 not in even_k),
             (diff_after, diff_wrong),
             (f2 > 0, f2L > 0)]
guard("NEG-CONTROL", all(a != b for a, b in neg_pairs) and len(neg_pairs) == 3,
      "三对负对照读数 %s（每对两半须不同）" % neg_pairs)

guard("HALF-EXIT", len(sol_int) == 0 and len(sol_half) > 0,
      "整数网格解 %d / 半整数网格解 %d（双端都报）" % (len(sol_int), len(sol_half)))
guard("DISCRIM-POWER", free_pass == 7 and len(fixed_flat) == 1 and free_pass != len(fixed_flat),
      "Lambda 自由 %d/7 vs Lambda 冻结 %d/7（通过率两端都测）" % (free_pass, len(fixed_flat)))
guard("HESSIAN-CROSS", f1 == 0 and hRP == 0 and hRR > 0 and hPP > 0,
      "f'(x0)=%s ; 交叉项=%d ; 对角元 %s*pi / %s*pi" % (fmt_f(f1), hRP, fmt_f(hRR), fmt_f(hPP)))
guard("CLOSED-BACKSUB", fp_frac(x0, N0) == 0 and G_frac(x0, N0) == 0 and Ls3 == F(41, 144),
      "x=9/4 同时满足 f'=0 与 G=0；Lambda*(3)=%s" % fmt_f(Ls3))

_src_path = os.path.abspath(__file__)
with io.open(_src_path, "r", encoding="utf-8") as _f:
    _tree = ast.parse(_f.read())
_hard = []
for _node in ast.walk(_tree):
    if isinstance(_node, ast.Call) and isinstance(_node.func, ast.Name) and _node.func.id == "add":
        if len(_node.args) >= 6 and isinstance(_node.args[5], ast.Constant) and isinstance(_node.args[5].value, bool):
            _hard.append(_node.lineno)
guard("NO-HARDCODE-OK", len(_hard) == 0,
      "AST 层扫 add() 第 6 实参为 True/False 字面量的处数 %d（守卫自身不含 add 调用）" % len(_hard))

guard("NOT-ALL-GREEN", cnt.get("FAIL", 0) >= 1 and cnt.get("IDENTITY", 0) >= 1,
      "FAIL %d / IDENTITY %d（防首跑全绿：定义恒等式必须显式降格）"
      % (cnt.get("FAIL", 0), cnt.get("IDENTITY", 0)))


def final_of(nf_main, nf_guard, n_decl):
    if nf_guard > 0:
        return "GATES-FAIL-GUARD-%d" % nf_guard
    if nf_main == 0:
        return "GATES-PASS-ALL-POSITIVE"
    if n_decl >= nf_main:
        return "GATES-PASS-WITH-%d-NEGATIVE" % nf_main
    return "GATES-FAIL-MAIN-%d" % nf_main


guard("FINAL-BRANCHES",
      final_of(0, 0, 0) == "GATES-PASS-ALL-POSITIVE"
      and final_of(0, 1, 0) == "GATES-FAIL-GUARD-1"
      and final_of(1, 0, 0) == "GATES-FAIL-MAIN-1"
      and final_of(1, 0, 1) == "GATES-PASS-WITH-1-NEGATIVE",
      "四分支 (0,0,0)/(0,1,0)/(1,0,0)/(1,0,1) 各自判词正确")

nf_main = cnt.get("FAIL", 0)
nf_guard = sum(1 for g in GUARDS if not g["ok"])
n_decl = 1 if any(x["id"] == "B04" and x["kind"] == "FAIL" for x in ROWS) else 0
FINAL = final_of(nf_main, nf_guard, n_decl)

# 判词由布尔量与计数机拼，不手写整句
vp = []
vp.append("SPIN12_TENSOR_%s" % ("OK" if EVEN_HALF == 1024 and ODD_HALF == 1024 else "BAD"))
vp.append("792_CHIRALITY_SELECTION_%s" % ("OK" if (5 not in even_k and 5 in odd_k) else "BAD"))
vp.append("EVEN_INDEX_%s" % ("IDENTITY" if n_odd == 0 else "BAD"))
vp.append("HALF_INTEGER_EXIT_%s" % ("EXISTS" if len(sol_half) > 0 else "NONE"))
vp.append("PAIRING_RANK_IDENTITY_%s" % ("OK" if diff_after == diff_before else "BAD"))
vp.append("PHI0_V0_%s" % ("EXACT" if V0 == F(-1, 16) and Vpp == 1 else "BAD"))
vp.append("FLAT_X_%s" % ("9_OVER_4" if x_small == D(9) / D(4) and G_frac(x0, N0) == 0 else "BAD"))
vp.append("LARGE_BRANCH_%s" % ("UNSTABLE" if f2L < 0 else "BAD"))
vp.append("HESSIAN_%s" % ("OK" if hRR == F(64, 9) and hPP == F(9) else "BAD"))
vp.append("LAMBDA_STAR_%s" % ("CLOSED" if Ls3 == F(41, 144) else "BAD"))
vp.append("N_SCAN_%s" % ("REPRODUCED" if match_r2 and match_h2 else "BAD"))
vp.append("DISCRIMINANT_%s" % ("N_SQ_LE_12" if disc(4) < 0 and disc(3) > 0 else "BAD"))
vp.append("FREEZE_PARAM_%s" % ("DISCRIM_ZERO" if free_pass == 7 and fixed_flat == [3] else "BAD"))
vp.append("THREE_GEN_INTEGER_FLUX_%s" % ("FAIL" if hit3 == 0 else "OK"))
vp.append("FOUR_FORCE_INFO_UNPROVEN")
vp.append("COUNT_29_INFO_UNREPRODUCED")
vp.append("HOMOGENEOUS_SUBSPACE_ONLY_INFO")
vp.append("UNIQUE_PREDICTION_0")
VERD = "__".join(vp)

KEY = {
    "even_blocks": EVEN_ALL[:4], "odd_blocks": ODD_ALL[:3],
    "even_half": EVEN_HALF, "odd_half": ODD_HALF, "selfdual6": EVEN_ALL[3] // 2,
    "qy_table": {k: fmt_f(v) for k, v in QY.items()},
    "grid_pairs": n_pairs, "grid_even": n_even, "grid_odd": n_odd, "grid_zero": n_zero,
    "int_solutions_3": len(sol_int), "half_solutions_3": len(sol_half),
    "i_net_NF3": fmt_f(v_net), "i_single_NF3": fmt_f(v_single),
    "pair_rank": PAIR_RANK, "diff_before": diff_before, "diff_after": diff_after, "diff_wrong": diff_wrong,
    "rank_ladder": ranks, "rank_zero_count": zeros, "hit3": hit3,
    "phi0_sq": fmt_f(phi0sq), "V0": fmt_f(V0), "Vpp": fmt_f(Vpp),
    "A": fmt_f(A), "disc_N1to4": [disc(N) for N in range(1, 5)],
    "x_small": "9/4", "x_large": fmt_f(xL),
    "H2_large": fmt_f(HL), "f2_large_sign": "负" if f2L < 0 else "正",
    "f2_small": fmt_f(f2), "hRR_pi": fmt_f(hRR), "hPP_pi": fmt_f(hPP),
    "lambda_star_N1to7": {str(N): fmt_f(flat_closed(N)[2]) for N in range(1, 8)},
    "lambda_star_N3": fmt_f(Ls3),
    "scan_actual": [[N, s1, s2, d] for (N, s1, s2, d) in scan],
    "scan_exp_r2": exp_r2, "scan_exp_h2": exp_h2,
    "free_pass": free_pass, "fixed_flat": fixed_flat,
    "nstar": "sqrt(12)", "nstar_num": "%.6f" % float(D(12).sqrt()),
}

os.makedirs(DATA, exist_ok=True)
jp = os.path.join(DATA, "_ROOTV63_recompute_2026-11-06.json")
rp = os.path.join(DATA, "_ROOTV63_recompute_report_2026-11-06.txt")


def make_out(rows_obj, verdict, final):
    return {"title": TITLE, "date": DATE, "verdict": verdict, "final": final,
            "counts": cnt, "n_rows": N_ROWS,
            "guards": {"n_ok": sum(1 for g in GUARDS if g["ok"]),
                       "n_total": len(GUARDS), "rows": GUARDS},
            "rows": rows_obj, "key_numbers": KEY}


# 回填顺序：先写（占位） -> 回读 -> 回填 -> 再写 -> 最后才拼报告
with io.open(jp, "w", encoding="utf-8") as f:
    f.write(json.dumps(make_out(ROWS, VERD, FINAL), ensure_ascii=False, indent=1))
with io.open(jp, "r", encoding="utf-8") as f:
    back = json.load(f)
placeholder_ok = any("独立复算的 0 条" in r["act"] for r in back["rows"] if r["id"] == "D03")
for r in back["rows"]:
    if r["id"] == "D03":
        r["act"] = r["act"].replace("独立复算的 0 条", "独立复算的 %d 条" % N_ROWS)
for r in ROWS:
    if r["id"] == "D03":
        r["act"] = r["act"].replace("独立复算的 0 条", "独立复算的 %d 条" % N_ROWS)
backfill_ok = placeholder_ok and any(("独立复算的 %d 条" % N_ROWS) in r["act"]
                                     for r in back["rows"] if r["id"] == "D03")
guard("BACKFILL-ORDER", backfill_ok and back["n_rows"] == N_ROWS,
      "占位存在=%s ; 回读回填生效=%s ; n_rows=%d" % (placeholder_ok, backfill_ok, back["n_rows"]))

guard("VERDICT-MACHINE", len(vp) >= 15 and all(isinstance(x, str) and x for x in vp)
      and (VERD.count("__") == len(vp) - 1),
      "判词由 %d 个机拼片段组成，连接符数 %d" % (len(vp), VERD.count("__")))
guard("KIND-COUNT", sum(cnt.values()) == N_ROWS and cnt.get("FAIL", 0) == nf_main,
      "kind 计数 %s 合计 %d" % (cnt, N_ROWS))

FINAL = final_of(nf_main, sum(1 for g in GUARDS if not g["ok"]), n_decl)
back["verdict"] = VERD
back["final"] = FINAL
back["guards"] = {"n_ok": sum(1 for g in GUARDS if g["ok"]),
                  "n_total": len(GUARDS), "rows": GUARDS}
with io.open(jp, "w", encoding="utf-8") as f:
    f.write(json.dumps(back, ensure_ascii=False, indent=1))

# 报告在回填之后才拼，并从最终 JSON 回读，保证判词与判定表同一读数
with io.open(jp, "r", encoding="utf-8") as f:
    final_obj = json.load(f)
L = []
L.append("=" * 78)
L.append("%s  复算报告  %s" % (TITLE, DATE))
L.append("=" * 78)
L.append("体例：跨卷整理册（不新增 RID、不进 README、条目不与任何卷相加）")
L.append("判词：%s" % final_obj["verdict"])
L.append("总门：%s" % final_obj["final"])
L.append("条目 %d：%s" % (final_obj["n_rows"], ", ".join("%s %d" % (k, final_obj["counts"][k])
                                                  for k in sorted(final_obj["counts"]))))
L.append("")
for r in final_obj["rows"]:
    L.append("%-5s %-8s %s" % (r["id"], r["kind"], r["name"]))
    L.append("       exp = %s" % r["exp"])
    L.append("       act = %s" % r["act"])
    if r["note"]:
        L.append("       note= %s" % r["note"])
L.append("")
L.append("守卫 %d/%d" % (final_obj["guards"]["n_ok"], final_obj["guards"]["n_total"]))
for g in final_obj["guards"]["rows"]:
    L.append("  %-18s %s | %s" % (g["name"], "ok" if g["ok"] else "BAD", g["detail"]))
L.append("")
L.append("关键读数摘要（机拼，供整理册直接引用，禁手写）")
K = final_obj["key_numbers"]
L.append("  Spin12 偶阶块 %s + 自对偶半 %d = %d ; 奇阶块 %s = %d"
         % (K["even_blocks"], K["selfdual6"], K["even_half"], K["odd_blocks"], K["odd_half"]))
L.append("  q_Y 表 %s ; 整数网格 %d 组（偶 %d / 奇 %d / 零 %d）; 半整数解 %d 个"
         % (K["qy_table"], K["grid_pairs"], K["grid_even"], K["grid_odd"],
            K["grid_zero"], K["half_solutions_3"]))
L.append("  计数约定 I_net=%s vs I_16=%s ; 配对 rank=%d 差 %d->%d ; 单侧负控差 %d ; 命中 3 次数 %d"
         % (K["i_net_NF3"], K["i_single_NF3"], K["pair_rank"], K["diff_before"],
            K["diff_after"], K["diff_wrong"], K["hit3"]))
L.append("  phi0^2=%s V0=%s Vpp=%s A=%s ; x_small=%s x_large=%s ; f''(x_small)=%s f''(x_large)符号=%s"
         % (K["phi0_sq"], K["V0"], K["Vpp"], K["A"], K["x_small"], K["x_large"],
            K["f2_small"], K["f2_large_sign"]))
L.append("  Hessian pi 系数 (%s, %s) ; 大半径 H2=%s ; Lambda*(3)=%s"
         % (K["hRR_pi"], K["hPP_pi"], K["H2_large"], K["lambda_star_N3"]))
L.append("  Lambda*(N) 表 %s" % K["lambda_star_N1to7"])
L.append("  N 扫描实算 %s ; 判别式 %s ; 临界 %s = %s"
         % (K["scan_actual"], K["disc_N1to4"], K["nstar"], K["nstar_num"]))
L.append("  判别力两端：Lambda 自由 %d/7 ; Lambda 冻结平直集 %s"
         % (K["free_pass"], K["fixed_flat"]))
with io.open(rp, "w", encoding="utf-8", newline="\r\n") as f:
    f.write("\n".join(L) + "\n")

gok = final_obj["guards"]["n_ok"]
print("\n" + "=" * 78)
print("条目 %d：%s" % (final_obj["n_rows"],
                 ", ".join("%s %d" % (k, final_obj["counts"][k]) for k in sorted(final_obj["counts"]))))
print("守卫 %d/%d ; 总门 %s" % (gok, final_obj["guards"]["n_total"], final_obj["final"]))
print("=" * 78)
print("written:")
print("  %s" % os.path.basename(jp))
print("  %s" % os.path.basename(rp))
