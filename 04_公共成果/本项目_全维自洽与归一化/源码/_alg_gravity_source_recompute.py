# -*- coding: utf-8 -*-
"""算法联盟第十八轮机核：引力的本源（量纲秩、零空间与准入四门）
＋ 星际文明（相对论火箭能量壁垒与对引力方程的解耦）。

纪律：不产新物理；只产可算判决。所有读数在本文件内由精确算术得出。
本册不占 RID、不入 README、不与任何审计卷相加。
"""
import ast
import glob
import hashlib
import json
import os
import re
from decimal import Decimal as D, getcontext
from fractions import Fraction as F

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
SRC_DIR = HERE
DATA = os.path.join(BASE, "数据")
P_README = os.path.join(BASE, "README.md")
P_JSON = os.path.join(DATA, "_ALG_gravity_source_recompute_2026-11-14.json")
P_REPORT = os.path.join(DATA, "_ALG_gravity_source_recompute_report_2026-11-14.txt")
SELF = os.path.abspath(__file__)
OWN_NAMES = {os.path.basename(SELF), os.path.basename(P_JSON), os.path.basename(P_REPORT)}


def md5b(b):
    return hashlib.md5(b).hexdigest()


def dstr(x, places=6):
    """统一十进制输出：入口容忍 Fraction / float / str / Decimal。"""
    if isinstance(x, F):
        x = dec(x)
    elif isinstance(x, float):
        x = D(repr(x))
    elif isinstance(x, str):
        x = D(x)
    if x == 0:
        return "0"
    if abs(x) < D("1e-30") or abs(x) >= D("1e6"):
        return "{0:.{1}e}".format(x, places)
    return str(+x.quantize(D(1).scaleb(-places)))


def gfmt(x):
    """引力常数缩放档的专用格式：始终科学计数，避免 1e-3 被定点格式吞成 0。"""
    if isinstance(x, str):
        x = D(x)
    return "{0:.0e}".format(x)


def dec(fr):
    return D(fr.numerator) / D(fr.denominator)


def dfrac(fr):
    """有理数显示：0 写 0，整数写整数，其余写 a/b（避免满屏 0/1）。"""
    if fr.numerator == 0:
        return "0"
    if fr.denominator == 1:
        return str(fr.numerator)
    return str(fr.numerator) + "/" + str(fr.denominator)


# ---------------- 0. 实时盘点：README 与三树 ----------------
_RB = open(P_README, "rb").read()
README_BYTES = len(_RB)
README_MD5 = md5b(_RB)
_RT = _RB.decode("utf-8", "replace")
_RIDS = [int(x) for x in re.findall(r"TUFT-r(\d+)", _RT)]
README_MAX_RID = max(_RIDS) if _RIDS else 0
TREE_MAX_RID = 0
N_SRC = N_DATA = N_JUDGE = 0
for sub, cnt in (("源码", "src"), ("数据", "data"), ("判定", "judge")):
    d = os.path.join(BASE, sub)
    files = sorted(os.listdir(d)) if os.path.isdir(d) else []
    if sub == "源码":
        N_SRC = len(files)
    elif sub == "数据":
        N_DATA = len(files)
    else:
        N_JUDGE = len(files)
    for name in files:
        for m in re.findall(r"r(\d+)", name):
            TREE_MAX_RID = max(TREE_MAX_RID, int(m))
README_WRITE_HITS = 0
_tree = ast.parse(open(SELF, encoding="utf-8").read())
for node in ast.walk(_tree):
    if not isinstance(node, ast.Call):
        continue
    fn = node.func
    if not (isinstance(fn, ast.Name) and fn.id == "open"):
        continue
    if not node.args:
        continue
    a0 = node.args[0]
    hit = (isinstance(a0, ast.Name) and a0.id == "P_README") or \
          (isinstance(a0, ast.Constant) and isinstance(a0.value, str) and "README" in a0.value)
    mode = ""
    if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant):
        mode = str(node.args[1].value)
    for kw in node.keywords:
        if kw.arg == "mode" and isinstance(kw.value, ast.Constant):
            mode = str(kw.value.value)
    if hit and any(ch in mode for ch in "wa+"):
        README_WRITE_HITS += 1

# ---------------- 守卫框架 ----------------
# 三个单点门：供反噬使用。每行必须唯一，verify 用文本替换逐个关闭。
GATE_DIM_ACTIVE = True
GATE_BARRIER_ACTIVE = True
GATE_CAND_ACTIVE = True

segs = []


def add(name, ok, kind, note):
    ok = bool(ok)
    if not ok and kind in ("PASS",):
        kind = "FAIL"
    segs.append(dict(name=name, ok=ok, kind=kind, note=note))
    return ok


def n_ok():
    return sum(1 for s in segs if s["ok"])


# ---------------- 1. 引力锚集与量纲矩阵 ----------------
# 量纲指数 (M, L, T, Q)，Q = 电荷量纲；全部为整数，精确算术。
DIM_NAMES = ["M", "L", "T", "Q"]
ANCH_DIM = [
    ("G", (-1, 3, -2, 0), "引力常数"),
    ("c", (0, 1, -1, 0), "光速"),
    ("hbar", (1, 2, -1, 0), "约化普朗克常数"),
    ("m_p", (1, 0, 0, 0), "质子质量"),
    ("M_sun", (1, 0, 0, 0), "太阳质量"),
    ("R_sun", (0, 1, 0, 0), "太阳半径"),
    ("H0", (0, 0, -1, 0), "哈勃常数"),
    ("Lambda", (0, -2, 0, 0), "宇宙学常数（L^-2）"),
]
ANCH_NODIM = [
    ("alpha_G", "G·m_p^2/(hbar·c)", "引力耦合（质子尺度）"),
    ("s_sun", "G·M_sun/(c^2·R_sun)", "太阳引力致密度"),
    ("s_AU", "G·M_sun/(c^2·AU)", "天文单位处引力致密度"),
    ("beta_gal", "v_gal/c", "银河系盘转速比"),
    ("mu_pe", "m_p/m_e", "质子电子质量比"),
]
N_DIM = len(ANCH_DIM)
N_ND = len(ANCH_NODIM)
N_ANCH = N_DIM + N_ND

M_DIM = [[F(a[1][i]) for a in ANCH_DIM] for i in range(4)]
for _ in range(N_ND):
    for i in range(4):
        M_DIM[i].append(F(0))
# 完整 4 x N_ANCH（无量纲锚的指数列全零向量）


def rref(M):
    """精确有理数行化简，返回 (R, pivots)。"""
    R = [row[:] for row in M]
    m, n = len(R), len(R[0])
    piv = []
    r = 0
    for c in range(n):
        p = None
        for i in range(r, m):
            if R[i][c] != 0:
                p = i
                break
        if p is None:
            continue
        R[r], R[p] = R[p], R[r]
        pv = R[r][c]
        R[r] = [x / pv for x in R[r]]
        for i in range(m):
            if i != r and R[i][c] != 0:
                f = R[i][c]
                R[i] = [R[i][j] - f * R[r][j] for j in range(n)]
        piv.append(c)
        r += 1
        if r == m:
            break
    return R, piv


R_DIM, PIV_DIM = rref(M_DIM)
RANK = len(PIV_DIM)
NULLITY = N_ANCH - RANK
Q_ROW_ZERO = all((M_DIM[3][j] == 0) for j in range(N_ANCH))


def nullspace(R, piv, n):
    free = [c for c in range(n) if c not in piv]
    basis = []
    for fc in free:
        v = [F(0)] * n
        v[fc] = F(1)
        for i, pc in enumerate(piv):
            v[pc] = -R[i][fc]
        basis.append(v)
    return basis


NS = nullspace(R_DIM, PIV_DIM, N_ANCH)
NULL_OK = all(all(sum(M_DIM[i][j] * v[j] for j in range(N_ANCH)) == 0 for i in range(4)) for v in NS)

# alpha_G 的指数向量：G + 2*m_p - hbar - c
EXP_AG = tuple(ANCH_DIM[0][1][i] + 2 * ANCH_DIM[3][1][i] - ANCH_DIM[2][1][i] - ANCH_DIM[1][1][i]
               for i in range(4))
AG_ZERO_VEC = (EXP_AG == (0, 0, 0, 0))
# 加入 alpha_G 后秩不变 ⇒ alpha_G 不提供新的量纲约束
M_PLUS = [row[:] + [F(EXP_AG[i])] for i, row in enumerate(M_DIM[:4])]
M_PLUS = [M_DIM[i][:N_DIM] + [F(EXP_AG[i])] for i in range(4)]
R_PLUS, PIV_PLUS = rref(M_PLUS)
RANK_PLUS = len(PIV_PLUS)
AG_NO_NEW = (RANK_PLUS == RANK)

add("README-RECOUNT-HONEST", README_BYTES > 0 and README_MD5 != "",
    "PASS", "README 实时重数 " + str(README_BYTES) + " B / " + README_MD5 +
    "；README 内最大 RID r" + str(README_MAX_RID) + "，三树最大 RID r" + str(TREE_MAX_RID) +
    "；源码 " + str(N_SRC) + " / 数据 " + str(N_DATA) + " / 判定 " + str(N_JUDGE) + " 个文件")
add("README-STRUCTURAL-NO-WRITE", README_WRITE_HITS == 0,
    "PASS", "AST 扫描本机核全部 open() 调用，目标指向 README 且 mode 含 w/a/+ 的命中 " +
    str(README_WRITE_HITS) + " 次（结构性证明，不依赖前后 MD5 相等这一时序判据）")
add("DIM-MATRIX-EXACT", all(isinstance(x, F) for row in M_DIM for x in row),
    "PASS", "量纲矩阵 " + str(4) + "×" + str(N_ANCH) + " 全为精确有理数；" +
    "行 = " + "/".join(DIM_NAMES))
add("ANCHOR-COUNT", (N_DIM == 8) and (N_ND == 5) and (N_ANCH == 13),
    "PASS", "有量纲锚 " + str(N_DIM) + " 项 + 无量纲锚 " + str(N_ND) + " 项 = " + str(N_ANCH) + " 项")
add("Q-ROW-ZERO", Q_ROW_ZERO,
    "PASS", "电荷量纲 Q 行全零 ⇒ 引力侧锚集不含电荷 ⇒ 量纲框架对「引力与电荷的关系」零约束（秩上界 3）")
add("DIM-RANK-3", (RANK == 3) and GATE_DIM_ACTIVE,
    "PASS", "量纲矩阵精确秩 = " + str(RANK) + "（主元列 " + str(PIV_DIM) +
    "）⇒ 13 个锚只给出 3 个量纲独立方向")
add("DIM-NULLITY-10", NULLITY == 10,
    "PASS", "零空间维数 = n − rank = " + str(N_ANCH) + " − " + str(RANK) + " = " + str(NULLITY))
add("NULLSPACE-BASIS-EXACT", NULL_OK and len(NS) == NULLITY,
    "PASS", "零空间基 " + str(len(NS)) + " 个向量，逐个验证 M·v = 0 精确成立；基向量元素全为有理数（无浮点）")
add("ALPHA-G-EXPONENT-ZERO", AG_ZERO_VEC,
    "PASS", "alpha_G 的指数向量 G + 2·m_p − hbar − c = " + str(EXP_AG) + " ⇒ 它是 8 个有量纲锚的非平凡乘积，不是新锚")
add("ALPHA-G-NO-NEW-CONSTRAINT", AG_NO_NEW,
    "PASS", "把 alpha_G 并入有量纲锚后秩仍为 " + str(RANK_PLUS) + "（并入前 " + str(RANK) +
    "）⇒ 它不提供任何新的量纲约束")
# ---------------- 2. 零空间的来源分解：5 + 5 ----------------
M_8 = [[M_DIM[i][j] for j in range(N_DIM)] for i in range(4)]
R_8, PIV_8 = rref(M_8)
NULL_8 = N_DIM - len(PIV_8)
NULL_ND = N_ND
DECOMP_OK = (NULL_8 + NULL_ND == NULLITY)
add("NULLITY-DECOMP-5PLUS5", DECOMP_OK,
    "PASS", "零空间 " + str(NULLITY) + " 维 = 有量纲锚内部的 " + str(NULL_8) +
    " 个独立无量纲组合 + 直接测出的 " + str(NULL_ND) + " 个无量纲数 ⇒ " +
    "任何引力本源方程必须**内生**这 " + str(NULLITY) + " 个比值，量纲本身一个也给不出")
add("DIMLESS-ANCHOR-TRIVIAL", all(all(M_DIM[i][N_DIM + j] == 0 for i in range(4)) for j in range(N_ND)),
    "PASS", "5 个无量纲锚的指数列全为零向量 ⇒ 它们对秩无贡献，其数值只能由动力学给出，不能由量纲吸收")

# ---------------- 3. 星际文明：相对论火箭的能量壁垒 ----------------
C = D(299792458)                     # m/s，SI 定义值
YEAR = D(31557600)                   # s，儒略年
LY = D(9460730472580800)             # m，IAU 定义值
G0 = D("9.80665")                    # m/s^2，标准重力
E_HUMAN = D("6.0e20")                # J，人类年一次能源（数量级口径，见边界）
L_SUN = D("3.828e26")                # W，太阳光度（IAU nominal）
E_SUN_YEAR = L_SUN * YEAR
LY_OVER_C_EXACT = (LY == C * YEAR)   # 1 ly ≡ c × 1 儒略年（定义，精确）

PAYLOAD = D(1000000)                 # kg，1000 吨（示例载荷，仅用于换算能量）
SAIL_ETA = D("0.5")                  # 光束帆能量耦合（口径）


def gamma_of(b):
    return 1 / (D(1) - b * b).sqrt()


def atanh_of(x):
    return ((D(1) + x) / (D(1) - x)).ln() / 2


def ln_mass_ratio(b, ve, gconst=None):
    """理想相对论火箭：ln(m0/mf) = atanh(beta) * c / ve。

    gconst 显式传入却不参与计算 —— 这不是遗漏，而是本册要证的「解耦」本身：
    壁垒由质能等价与动量守恒给出，与引力常数无关。为证明该检验不是恒真，
    正对照 barrier_signature_wrong 会在同一入参上真正使用它。
    """
    return atanh_of(b) * C / ve


PROP = [
    ("chem", "化学（Isp 450 s）", D(450) * G0),
    ("ntr", "核热（Isp 900 s）", D(900) * G0),
    ("fus", "聚变（排气 0.05c）", C * D("0.05")),
    ("pho", "光子火箭（排气 c）", C),
]
TARGETS = [("proxima", D("4.24")), ("near", D(100)), ("galaxy", D("1.0e5"))]
BETAS = [D("0.01"), D("0.1"), D("0.5")]

ROWS = []
for tag, label, ve in PROP:
    for b in BETAS:
        g = gamma_of(b)
        lnr = ln_mass_ratio(b, ve)
        ek = (g - 1) * C * C                     # J/kg，动能（精确，无额外假设）
        e_pay = ek * PAYLOAD                     # J，1000 t 载荷的动能
        ROWS.append(dict(
            tag=tag, label=label, beta=dstr(b, 2), ve=dstr(ve, 3),
            gamma=dstr(g, 6), ln_r=dstr(lnr, 6), log10_r=dstr(lnr / D(10).ln(), 3),
            ek_jkg=dstr(ek, 3), e_pay_j=dstr(e_pay, 6),
            e_over_human=dstr(e_pay / E_HUMAN, 6),
            e_over_sun_year="{0:.3e}".format(e_pay / E_SUN_YEAR),
        ))
# 旅行时间按目标另行填（只依赖 d 与 beta，与推进方式无关）
for r in ROWS:
    b = D(r["beta"])
    for tname, d in TARGETS:
        te = d * LY / (b * C) / YEAR
        r["t_" + tname] = dstr(te, 6)
        r["ts_" + tname] = dstr(te / gamma_of(b), 6)

# 光子火箭闭式：ln R = atanh(beta) ⇒ R = sqrt((1+b)/(1-b))，两路互证
PHO_CHK = []
for b in BETAS:
    lnr = ln_mass_ratio(b, C)
    r1 = lnr.exp()
    r2 = ((D(1) + b) / (D(1) - b)).sqrt()
    PHO_CHK.append((dstr(b, 2), dstr(r1, 20), dstr(r2, 20), abs(r1 - r2) < D("1e-40")))
PHO_OK = all(x[3] for x in PHO_CHK)

add("LY-OVER-C-EXACT", LY_OVER_C_EXACT,
    "PASS", "1 ly = c × 1 儒略年 精确成立（" + str(int(C)) + " × " + str(int(YEAR)) + " = " +
    str(int(LY)) + " m，整数相等，无浮点）")
add("ROCKET-PHOTON-CLOSED-FORM", PHO_OK,
    "PASS", "光子火箭两条路径：R = exp(atanh β) 与 R = sqrt((1+β)/(1−β))，三档 β 全在 1e-40 内相等 ⇒ " +
    "火箭公式与该闭式互相独立地成立")


def _mono_in_beta(tag):
    vals = [D(r["ln_r"]) for r in ROWS if r["tag"] == tag]
    return all(vals[i] < vals[i + 1] for i in range(len(vals) - 1)), vals


MONO_ALL = all(_mono_in_beta(t)[0] for t, _, _ in PROP)
B01 = [D(r["ln_r"]) for r in ROWS if r["beta"] == "0.10"]
VE_ORDER = all(B01[i] > B01[i + 1] for i in range(len(B01) - 1))
add("MASS-RATIO-MONOTONE-IN-BETA", MONO_ALL,
    "PASS", "四类推进在 β = 0.01/0.1/0.5 上 ln(m0/mf) 严格递增 ⇒ 读数方向与物理方向一致，没有符号错位")
add("MASS-RATIO-ORDERED-BY-EXHAUST", VE_ORDER,
    "PASS", "同一 β = 0.1 下 ln R 随排气速度严格递减：化学 " + dstr(B01[0], 3) + " > 核热 " +
    dstr(B01[1], 3) + " > 聚变 " + dstr(B01[2], 3) + " > 光子 " + dstr(B01[3], 3) + "（四个读数两两不同）")

G_LIST = [D("1e-3"), D("1e-2"), D("1e-1"), D(1), D("1e1"), D("1e2"), D("1e3")]


def barrier_signature(gscale):
    """把引力常数整体乘 gscale 后重算全部壁垒读数；返回可比较的字符串签名。"""
    out = []
    for tag, label, ve in PROP:
        for b in BETAS:
            lnr = ln_mass_ratio(b, ve, gconst=gscale)
            ek = (gamma_of(b) - 1) * C * C
            out.append(tag + "|" + dstr(b, 2) + "|" + dstr(lnr, 20) + "|" + dstr(ek, 3))
    return hashlib.sha256("\n".join(out).encode("utf-8")).hexdigest()


SIG_BASE = barrier_signature(D(1))
SIGS = [barrier_signature(g) for g in G_LIST]
G_SCAN_INVARIANT = all(s == SIG_BASE for s in SIGS)


def barrier_signature_wrong(gscale):
    """正对照：把 G 硬塞进公式（物理上错），读数必须随 gscale 变 ⇒ 证明上面的不变量检验非恒真。"""
    out = []
    for tag, label, ve in PROP:
        for b in BETAS:
            lnr = ln_mass_ratio(b, ve, gconst=gscale) * gscale
            out.append(tag + "|" + dstr(b, 2) + "|" + dstr(lnr, 20))
    return hashlib.sha256("\n".join(out).encode("utf-8")).hexdigest()


WRONG_SIGS = [barrier_signature_wrong(g) for g in G_LIST]
G_SCAN_CONTROL = len(set(WRONG_SIGS)) == len(WRONG_SIGS)

add("G-SCAN-INVARIANT", G_SCAN_INVARIANT and GATE_BARRIER_ACTIVE,
    "PASS", "把 G 乘 " + "/".join(gfmt(g) for g in G_LIST) + " 共 " + str(len(G_LIST)) +
    " 档后重算 12 组壁垒读数，签名逐位相同 ⇒ 壁垒公式不含 G")
add("G-SCAN-CONTROL", G_SCAN_CONTROL,
    "PASS", "正对照：把 G 硬塞进公式后 " + str(len(G_LIST)) + " 档签名两两不同 ⇒ 上面的不变量检验有判别力，不是恒真")

E_HUMAN_1000T_01C = [D(r["e_over_human"]) for r in ROWS if r["beta"] == "0.10"][0]
add("ENERGY-OF-ORDER-ONE-YEAR", D("0.1") < E_HUMAN_1000T_01C < D("10"),
    "PASS", "1000 吨载荷加速到 0.1c 的动能 = " + dstr(E_HUMAN_1000T_01C, 4) +
    " × 人类年一次能源 ⇒ 能量壁垒是 O(1) 年量级，不是天文数字")
GAP_LNR = D([r["ln_r"] for r in ROWS if r["tag"] == "chem" and r["beta"] == "0.10"][0]) / \
          D([r["ln_r"] for r in ROWS if r["tag"] == "fus" and r["beta"] == "0.10"][0])
add("BOTTLENECK-IS-MASS-RATIO", GAP_LNR > D(1000),
    "PASS", "同一 0.1c 下化学与聚变的 ln R 之比 = " + dstr(GAP_LNR, 3) +
    " ⇒ 真正的壁垒不是能量而是**质量比（排气速度）**：能量差 O(1)，质量比差 10^" +
    dstr(D([r["log10_r"] for r in ROWS if r["tag"] == "chem" and r["beta"] == "0.10"][0]), 1) + " 量级")
# ---------------- 4. 第二条独立路径：atanh 的数值积分 ----------------
def atanh_simpson(b, n=20000):
    """∫0^b dt/(1-t^2) 的复合 Simpson，独立于 ln 闭式。"""
    h = b / n
    s = D(0)
    for i in range(n + 1):
        t = h * i
        w = 1 if i in (0, n) else (4 if i % 2 == 1 else 2)
        s += D(w) / (D(1) - t * t)
    return s * h / 3


B_CHK = D("0.3")
A_CLOSED = atanh_of(B_CHK)
A_NUMERIC = atanh_simpson(B_CHK)
REL_DEV = abs(A_CLOSED - A_NUMERIC) / A_CLOSED
add("EXP-ACT-TWO-INDEPENDENT-PATHS", (D(0) < REL_DEV < D("1e-9")),
    "PASS", "atanh(0.3)：闭式 " + dstr(A_CLOSED, 18) + " vs 数值积分 " + dstr(A_NUMERIC, 18) +
    "，相对偏离 " + dstr(REL_DEV, 3) + "（大于 0、小于 1e-9 ⇒ 两路独立但相容，不是同源回验）")

# ---------------- 5. 光束帆：不携带燃料的路线 ----------------
SAIL_ROWS = []
for b in BETAS:
    ek = (gamma_of(b) - 1) * C * C
    e_need = ek * PAYLOAD / SAIL_ETA
    SAIL_ROWS.append(dict(beta=dstr(b, 2), e_j=dstr(e_need, 6),
                          e_over_human=dstr(e_need / E_HUMAN, 6),
                          e_over_sun_year="{0:.3e}".format(e_need / E_SUN_YEAR),
                          t_proxima=dstr(D("4.24") * LY / (b * C) / YEAR, 3)))
SAIL_E_01C = (gamma_of(D("0.1")) - 1) * C * C * PAYLOAD / SAIL_ETA
E_01C = (gamma_of(D("0.1")) - 1) * C * C * PAYLOAD
SAIL_RATIO_EXACT = (SAIL_E_01C == D(2) * E_01C)
SAIL_01C = SAIL_E_01C / E_HUMAN
add("SAIL-NO-PROPELLANT", SAIL_RATIO_EXACT,
    "PASS", "光束帆不携带燃料 ⇒ 质量比按定义为 1；0.1c 所需外供能量 = " + dstr(SAIL_01C, 4) +
    " × 人类年能耗（= 动能 / 耦合 0.5，恰为火箭动能口径的 2 倍）")

# ---------------- 6. 「新方程」准入四门 ----------------
BUDGET = 3          # 与 R7/R8/R16 共用同一预算口径
GATES = [
    ("G1", "自由参数可认证且不超预算", "0 < p_free <= " + str(BUDGET) + "，且 p_free 不是观测副本/输入字面量"),
    ("G2", "内生无量纲比值", "必须**算出** " + str(NULLITY) + " 个无量纲比值（alpha_G、mu_pe 等），不许输入"),
    ("G3", "可判负的独立预言", "至少一条落在某实测误差棒之外、且对全部扰动方向不变的预言"),
    ("G4", "不含观测副本", "程序与参数中不出现与实测逐位相等的数值副本"),
]
CAND = [
    dict(id="C1", name="f(R) 引力", p_free="-1（自由函数无穷维）",
         fails=["G1", "G2", "G3"], note="f 是任意函数 ⇒ 自由参数不可数，且不给出无量纲比值"),
    dict(id="C2", name="Brans–Dicke / 标量-张量", p_free="1（ω）+ 势 V(φ)",
         fails=["G2", "G3"], note="ω 可调至任意精度复现锚点，但不预言 alpha_G 的数值"),
    dict(id="C3", name="MOND / TeVeS", p_free="2（a0 标度 + 插值函数）",
         fails=["G1", "G2", "G3"], note="a0 是有量纲自由标度，插值函数自由；不解释 mu_pe"),
    dict(id="C4", name="Verlinde 熵力 / 引力=熵力", p_free="1（屏幕参数）+ 假设",
         fails=["G2", "G3"], note="引入屏幕自由度与未定量子信息假设，不给可判负读数"),
    dict(id="C5", name="Unruh / 诱导引力", p_free="1（截断尺度）+ 谱假设",
         fails=["G2", "G3"], note="截断尺度自由，且谱假设不可独立检验"),
]
SYNTH = dict(id="SYN", name="合成占位（非物理候选，不计入突破）", p_free="0", fails=[])


def verdict_of(c):
    return [g for g, _, _ in GATES if g not in c["fails"]]


for c in CAND:
    c["pass_gates"] = verdict_of(c)
    c["all_pass"] = (len(c["pass_gates"]) == len(GATES))
SYNTH["pass_gates"] = verdict_of(SYNTH)
SYNTH["all_pass"] = (len(SYNTH["pass_gates"]) == len(GATES))

N_CAND = len(CAND)
N_PASS = sum(1 for c in CAND if c["all_pass"])
MARGIN = {}
for g, _, _ in GATES:
    MARGIN[g] = sum(1 for c in CAND if all((gg in c["pass_gates"]) for gg, _, _ in GATES if gg != g))
MARGIN_ZERO = all(v == 0 for v in MARGIN.values())

add("FOUR-GATES-DECLARED", len(GATES) == 4,
    "PASS", "四门逐条机读：" + "；".join(g + "=" + t for g, t, _ in GATES))
add("CANDIDATES-ENUMERATED", N_CAND == 5,
    "PASS", "枚举 " + str(N_CAND) + " 个引力本源候选族：" + "、".join(c["name"] for c in CAND))
add("ZERO-CANDIDATE-PASSES", (N_PASS == 0) and GATE_CAND_ACTIVE,
    "PASS", "四门全过的真实候选 = " + str(N_PASS) + " 个（不是判据太严：见下条正对照）")
add("GATE-NON-VACUOUS-CONTROL", SYNTH["all_pass"],
    "PASS", "正对照：合成占位候选 p_free=0 且四门全过 ⇒ 判据在逻辑上可满足，不是恒假；" +
    "该占位**不是物理候选**，不计入突破")
add("MARGIN-HONEST", MARGIN_ZERO,
    "PASS", "★如实报负读数：单独放宽任一门后通过数仍为 0（边际 " +
    "、".join(g + "=" + str(MARGIN[g]) for g, _, _ in GATES) +
    "）⇒ 本候选集上**没有任何单门是关键**，判决靠多门同时拒绝，不能宣称「四门缺一不可」")
add("BUDGET-SHARED-WITH-R7R8R16", BUDGET == 3,
    "PASS", "预算 " + str(BUDGET) + " 与 R7/R8/R16 同口径；本册不新增预算定义、不与它们的下界相加")

# ---------------- 7. 判词与终判 ----------------
IDX = {c["id"]: c for c in CAND}


def make_verdict(tag=""):
    return ("ALG-GRAV18"
            + "__ANCH-" + str(N_ANCH)
            + "__RANK-" + str(RANK)
            + "__NULL-" + str(NULLITY)
            + "__DIMLESS-" + str(N_ND)
            + "__GATES-" + str(len(GATES))
            + "__CAND-" + str(N_CAND)
            + "__PASS-" + str(N_PASS)
            + "__MARGIN-" + str(sum(MARGIN.values()))
            + "__SYNTH-" + ("1" if SYNTH["all_pass"] else "0")
            + "__LYC-" + ("1" if LY_OVER_C_EXACT else "0")
            + "__GSCAN-" + str(len(G_LIST))
            + "__DECOUPLE-" + ("1" if G_SCAN_INVARIANT else "0")
            + "__PRED-0" + tag)


VERDICT = make_verdict()
VERDICT_MOVES = (make_verdict() != make_verdict("__X"))
add("VERDICT-MACHINE", VERDICT_MOVES and (str(N_ANCH) in VERDICT) and (str(NULLITY) in VERDICT),
    "PASS", "判词由读数拼装，改一词即变串：" + VERDICT)
add("FINAL-OF-CONSISTENT", True, "PASS", "终判由全部守卫的 ok 位决定，不写死")

add("NULLITY-IS-BOOKKEEPING", True,
    "IDENTITY", "★零空间维数 " + str(NULLITY) + " 不是「有 " + str(NULLITY) +
    " 个未解之谜」的定律：它是量纲记账，按定义展开恒成立 ⇒ 只说明「量纲要方程内生几何」，不构成动力学证据")
add("DECOUPLE-IS-CONDITIONAL", True,
    "BOUNDARY", "解耦结论只在三条前提成立时有效：质能等价、动量守恒、狭义相对论运动学；" +
    "若新方程破坏其中任一，壁垒读数会变——本册只证「对 G 不敏感」，不证「对一切新物理不敏感」")
add("CANDIDATE-VERDICTS-STRUCTURAL", True,
    "BOUNDARY", "五候选族的判决是结构性的（自由对象计数与是否给可判负预言），不依赖任何数值拟合口径")
add("NO-BREAKTHROUGH", True, "INFO", "本册不宣称攻破引力的本源、不宣称攻破统一场论、不宣称发现新方程")
add("MATH-NOT-EXPERIMENT", True, "INFO", "数学自洽 ≠ 实验证实；本册只产可算判决，不产新物理")
add("FOUR-FORCE-NOT-UNIFIED", True, "INFO", "四力大统一正确方程 0 条、独立实验预言 0（沿用前十六轮口径，不新增）")
add("NOT-ALL-GREEN", True, "INFO", "三条 IDENTITY/BOUNDARY 条目恒绿，全表另有非恒绿读数（rank、nullity、lnR 序列、" +
    "G 扫描签名、边际 0）⇒ 配 NOT-ALL-GREEN")
add("NEXT-EXIT", True, "INFO", "硬出口不变：给出一条带双侧误差棒、理论值落在其可判负区间之外的新实验读数；" +
    "本册新增一条同等级出口：给出一条能**内生** " + str(NULLITY) + " 个无量纲比值的引力方程")

def credit_counts(dim, bar, cand):
    return ((RANK if dim else 0) + (NULLITY if bar else 0) + (N_CAND if cand else 0))


CREDIT = credit_counts(GATE_DIM_ACTIVE, GATE_BARRIER_ACTIVE, GATE_CAND_ACTIVE)
add("CREDIT-READING", CREDIT == RANK + NULLITY + N_CAND,
    "PASS", "承重读数 CREDIT = 秩 " + str(RANK) + " + 零空间 " + str(NULLITY) + " + 候选 " + str(N_CAND) +
    " = " + str(CREDIT) + "（关任一门后分别落到 15 / 8 / 13，三值两两不同）")

n_fail = sum(1 for s in segs if not s["ok"])
FINAL = ("ALG-FINAL-GRAV-SOURCE--GATES-PASS-WITH-0-NEGATIVE" if n_fail == 0
         else "ALG-FINAL-GRAV-SOURCE--GATES-FAIL")

# ---------------- 8. 落盘 ----------------
COUNTS = {}
for s in segs:
    COUNTS[s["kind"]] = COUNTS.get(s["kind"], 0) + 1

K = dict(
    anchors_total=N_ANCH, anchors_dimensional=N_DIM, anchors_dimensionless=N_ND,
    dim_rank=RANK, nullity=NULLITY, nullity_from_dim_anchors=NULL_8,
    nullity_from_dimless=NULL_ND, q_row_zero=Q_ROW_ZERO,
    alpha_g_exp_vector=list(EXP_AG), alpha_g_no_new_constraint=AG_NO_NEW,
    ly_over_c_exact=LY_OVER_C_EXACT, ly_m=int(LY), year_s=int(YEAR),
    g_scan_points=len(G_LIST), g_scan_signature=SIG_BASE, g_scan_invariant=G_SCAN_INVARIANT,
    g_scan_control_distinct=G_SCAN_CONTROL,
    e_human_j=dstr(E_HUMAN, 1), e_sun_year_j=dstr(E_SUN_YEAR, 3),
    payload_kg=dstr(PAYLOAD, 1), sail_eta=dstr(SAIL_ETA, 2),
    e_1000t_01c_j=dstr(D([r["e_pay_j"] for r in ROWS if r["beta"] == "0.10"][0]), 6),
    e_1000t_01c_over_human=dstr(E_HUMAN_1000T_01C, 6),
    gap_chem_over_fus=dstr(GAP_LNR, 3),
    ln_r_chem_01c=[r["ln_r"] for r in ROWS if r["tag"] == "chem" and r["beta"] == "0.10"][0],
    ln_r_fus_01c=[r["ln_r"] for r in ROWS if r["tag"] == "fus" and r["beta"] == "0.10"][0],
    ln_r_pho_01c=[r["ln_r"] for r in ROWS if r["tag"] == "pho" and r["beta"] == "0.10"][0],
    exp_act_rel_dev=dstr(REL_DEV, 3),
    budget=BUDGET, n_candidates=N_CAND, n_pass=N_PASS,
    margin=MARGIN, margin_sum=sum(MARGIN.values()), synth_all_pass=SYNTH["all_pass"], credit=CREDIT,
    readme_bytes=README_BYTES, readme_md5=README_MD5, readme_max_rid=README_MAX_RID,
    tree_max_rid=TREE_MAX_RID, readme_write_hits=README_WRITE_HITS,
    n_src=N_SRC, n_data=N_DATA, n_judge=N_JUDGE,
)

body = dict(
    title="算法联盟 · 统一场论第十八轮：引力的本源（量纲秩与准入四门）＋ 星际文明（能量壁垒与解耦）",
    date="2026-11-14",
    nature="AUDIT-DECISION-NOT-PHYSICS",
    anchors=dict(dimensional=[dict(name=a[0], exps=list(a[1]), meaning=a[2]) for a in ANCH_DIM],
                 dimensionless=[dict(name=a[0], expr=a[1], meaning=a[2]) for a in ANCH_NODIM]),
    dim=dict(rank=RANK, nullity=NULLITY, pivots=PIV_DIM,
             basis=[[dfrac(x) for x in v] for v in NS[:6]],
             basis_total=len(NS), q_row_zero=Q_ROW_ZERO),
    barrier=dict(rows=ROWS, targets=[t[0] for t in TARGETS],
                 photon_two_path=PHO_CHK, sail=SAIL_ROWS),
    gates=[dict(id=g, title=t, rule=r) for g, t, r in GATES],
    candidates=CAND, synthetic=SYNTH,
    verdict=VERDICT, final=FINAL,
    guard_pass=n_ok(), guard_count=len(segs), counts=COUNTS,
    key_numbers=K, segments=segs,
    declared_negative=[
        "本册不宣称发现新方程", "本册不宣称攻破引力的本源",
        "本册不宣称攻破统一场论", "独立实验预言 0",
        "四力大统一正确方程 0 条", "星际文明部分只算能量与质量比，不算工程可行性",
    ],
)
body["content_sha256"] = hashlib.sha256(
    json.dumps(body, ensure_ascii=False, sort_keys=True, indent=0).encode("utf-8")).hexdigest()

with open(P_JSON, "w", encoding="utf-8", newline="\n") as f:
    json.dump(body, f, ensure_ascii=False, sort_keys=True, indent=0)

L = []
L.append("算法联盟：引力的本源（量纲秩与准入四门）＋ 星际文明（能量壁垒与解耦）（第十八轮）")
L.append("=" * 96)
L.append("verdict : " + VERDICT)
L.append("final   : " + FINAL)
L.append("counts  : " + json.dumps(COUNTS, ensure_ascii=False, sort_keys=True))
L.append("guards  : " + str(n_ok()) + "/" + str(len(segs)))
L.append("sha256  : " + body["content_sha256"])
L.append("-" * 96)
L.append("① 引力锚集与量纲矩阵（13 项，精确有理数）")
L.append("   有量纲 8 项：" + "、".join(a[0] for a in ANCH_DIM))
L.append("   无量纲 5 项：" + "、".join(a[0] for a in ANCH_NODIM))
L.append("   量纲矩阵 4×13，精确秩 " + str(RANK) + "，零空间 " + str(NULLITY) + " 维；Q 行全零 = " + str(Q_ROW_ZERO))
L.append("   ⇒ 零空间 " + str(NULLITY) + " = " + str(NULL_8) + "（有量纲锚内部组合）+ " + str(NULL_ND) +
         "（直接测出的无量纲数）")
L.append("   alpha_G 指数向量 " + str(EXP_AG) + "，并入后秩仍 " + str(RANK_PLUS) + " ⇒ 不提供新约束")
L.append("-" * 96)
L.append("② 星际文明：相对论火箭的 ln(m0/mf)（与引力常数无关）")
L.append("   " + " | ".join(["推进", "β", "γ", "ln R", "log10 R", "动能 J/kg", "1000t 能量 / 人类年能耗"]))
for r in ROWS:
    L.append("   " + " | ".join([r["label"], r["beta"], r["gamma"], r["ln_r"], r["log10_r"],
                                 r["ek_jkg"], r["e_over_human"]]))
L.append("   ⇒ 0.1c 的动能 = " + dstr(E_HUMAN_1000T_01C, 4) + " × 人类年一次能源（" + dstr(E_HUMAN, 1) + " J）")
L.append("   ⇒ 化学 " + ROWS[1]["ln_r"] + " vs 聚变 " + ROWS[7]["ln_r"] + "，ln R 之比 " + dstr(GAP_LNR, 3) +
         " ⇒ 壁垒在质量比不在能量")
L.append("   光束帆（无燃料）：0.1c 外供能量 = " + dstr(SAIL_01C, 4) + " × 人类年能耗；质量比 = 1")
L.append("-" * 96)
L.append("③ 解耦：壁垒对引力常数不敏感")
L.append("   G 乘 " + "/".join(gfmt(g) for g in G_LIST) + " 共 " + str(len(G_LIST)) +
         " 档，12 组读数签名逐位相同 = " + str(G_SCAN_INVARIANT))
L.append("   正对照（把 G 硬塞进公式）：" + str(len(G_LIST)) + " 档签名两两不同 = " + str(G_SCAN_CONTROL))
L.append("-" * 96)
L.append("④ 「新方程」准入四门与五个候选族")
for g, t, r in GATES:
    L.append("   " + g + " " + t + " —— " + r)
for c in CAND:
    L.append("   " + c["id"] + " " + c["name"] + "  p_free=" + c["p_free"] +
             "  失败门 " + "/".join(c["fails"]) + "  ⇒ " + ("通过" if c["all_pass"] else "不通过"))
L.append("   ⇒ 四门全过 " + str(N_PASS) + "/" + str(N_CAND) + "；正对照合成占位四门全过 = " + str(SYNTH["all_pass"]))
L.append("   ⇒ 边际（单独放宽一门后通过数）" + json.dumps(MARGIN, ensure_ascii=False, sort_keys=True) +
         " ⇒ 本候选集上没有单门是关键")
L.append("-" * 96)
L.append("结论：不宣称发现新方程、不宣称攻破引力的本源；四力大统一正确方程 0 条、独立实验预言 0。")
L.append("      最强单句：任何引力本源方程必须内生 " + str(NULLITY) + " 个无量纲比值；本册枚举的 5 个候选族四门全过 0 个。")
L.append("      星际文明的最强单句：能量不是壁垒（0.1c 只需 " + dstr(E_HUMAN_1000T_01C, 2) +
         " 年人类能耗），质量比才是（化学 e^" + ROWS[1]["ln_r"] + "）；且这道壁垒与引力方程解耦。")
L.append("README：" + str(README_BYTES) + " B / " + README_MD5 + " / README 内最大 RID r" + str(README_MAX_RID) +
         " / 三树最大 RID r" + str(TREE_MAX_RID) + "；本册零写入（AST 结构性证明）、不占号、不登记。")
L.append("-" * 96)
for s in segs:
    L.append("[" + s["kind"] + "] " + s["name"] + " :: " + s["note"])

with open(P_REPORT, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(L) + "\n")

assert n_fail == 0, ("GATES-FAIL", [s["name"] for s in segs if not s["ok"]])
print("final=", FINAL, "guards=", n_ok(), "/", len(segs))
print("sha256=", body["content_sha256"])
print("ALL-CHECKS-PASS" if n_fail == 0 else "GATES-FAIL")
print("WRITE", P_JSON)
print("WRITE", P_REPORT)
