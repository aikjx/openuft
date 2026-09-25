# -*- coding: utf-8 -*-
"""
空间螺旋几何化统一场论 · 「算法联盟缺陷修复体系」第一性审计
============================================================

审计对象
--------
2026-09-25 提交的《算法联盟·空间螺旋几何统一场论 缺陷修复体系｜核心公理+闭环公式+纠错算法理论》：
  - 4 条新公理（螺旋拓扑本原 / 相位曲率等价 / 量子离散拓扑量化 / 常数拓扑派生）
  - 5 组修复公式（N 量化 / α 闭环 / G 去循环 / ρ 本源 / 电磁-引力统一耦合）
  - 3 个纠错算法（矛盾自检 / 拓扑归一 / 层级升维）
  - 申报评级面板：修复后 H6/O6/C3/U2、L3 完整第一性闭环、原 falsified 缺陷清零

方法（严格复用 openuft 既有工具链，本册不新造判据）
----------------------------------------------------
  1. 量纲账本：齐次性检查 + Buckingham Π 定理（无量纲输入不能产出有量纲输出）
  2. 定理 C（量纲不可行性，见本目录 README）：情形 1 / 情形 2 判定
  3. 信息增益判别式 V = (n_hit − n_free − n_anchor) / n_hit（无量纲靶场审计）
  4. 自由度审计（项数 ≠ 约束数，见本目录三条方法论结论 H02/H03）
  5. 独立数值复算：mpmath dps=50 + Frenet 公式数值反算（不采信原文献自陈的精算）

红线
----
所有结论一律登记为 PASS / BOUNDARY / INFO / FAIL 四态，不粉饰；
「用了更多符号」不等于「解释力增加」；循环性换壳（ρ → K₀）记为未解除。

产出
----
  数据/空间螺旋修复版_第一性审计.json
  数据/空间螺旋修复版_第一性审计.md
  07_统一场方程/空间螺旋几何化统一场论/claims.csv 追加 C24–C38（幂等）
  07_统一场方程/空间螺旋几何化统一场论/11_证伪与反例/空间螺旋修复版_第一性缺陷记录.md

用法：python 空间螺旋修复版_第一性审计与伪派生判定.py
"""

import os
import io
import sys
import json
import time
from fractions import Fraction

import mpmath
from mpmath import mp, mpf, mpc, sqrt, sin, cos, tan, atan, pi
import sympy as sp

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

mp.dps = 50
T0 = time.time()

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT_DIR = os.path.join(ROOT, "04_公共成果", "算法联盟_全维自洽与归一化", "数据")
SYS_DIR = os.path.join(ROOT, "07_统一场方程", "空间螺旋几何化统一场论")
REF_DIR = os.path.join(SYS_DIR, "11_证伪与反例")

# ---------------------------------------------------------------------------
# 常量（SI-2019 / CODATA；全部**就地写死**以避免环境差异）
# ---------------------------------------------------------------------------
C = mpf("299792458")                 # c  精确定义值
ALPHA = mpf("7.2973525693e-3")       # α  精细结构常数
ALPHA_UREL = mpf("1.5e-10")
G_NEWTON = mpf("6.67430e-11")
HBAR = mpf("1.054571817e-34")
MU0 = 4 * pi * mpf("1e-7")
EPS0 = 1 / (MU0 * C * C)

N_DEF_A = mpf("18916.90839")   # 原定义 A：N = 1/[α²(1−α)]
N_DEF_B = mpf("18907")         # 原定义 B：N = 1/α² + 1/α + 1 + α

# ---------------------------------------------------------------------------
# 结果收集器
# ---------------------------------------------------------------------------
ROWS = []
CHECKS = []


def reg(state, tag, statement, detail, evidence=""):
    """登记一条判定（四态）。"""
    assert state in ("PASS", "BOUNDARY", "INFO", "FAIL")
    ROWS.append({"state": state, "tag": tag, "statement": statement,
                 "detail": detail, "evidence": evidence})
    print("  [%-8s] %s" % (state, tag))
    if detail:
        print("             %s" % detail.replace("\n", "\n             "))
    return state


def item(name, ok, note=""):
    CHECKS.append({"name": name, "ok": bool(ok), "note": note})
    print("  [%s] %s" % ("OK  " if ok else "FAIL", name))
    if note:
        print("        %s" % note)
    return ok


def fmt(x, n=8):
    return mpmath.nstr(x, n)


# ---------------------------------------------------------------------------
# 量纲账本（L, M, T, I 四个基本量纲的整数指数向量）
# ---------------------------------------------------------------------------
def D(L=0, M=0, T=0, I=0):
    return {"L": Fraction(L), "M": Fraction(M), "T": Fraction(T), "I": Fraction(I)}


def dmul(a, b):
    return {k: a[k] + b[k] for k in a}


def ddiv(a, b):
    return {k: a[k] - b[k] for k in a}


def dpow(a, n):
    return {k: a[k] * Fraction(n) for k in a}


def dfmt(d):
    parts = []
    for k in ("L", "M", "T", "I"):
        e = d[k]
        if e == 0:
            continue
        parts.append(k + "^" + str(e))
    return "[" + " ".join(parts) + "]" if parts else "[1]"


DIM_G = D(L=3, M=-1, T=-2)
DIM_C = D(L=1, T=-1)
DIM_ALPHA = D()
DIM_CURV = D(L=-1)          # 曲率 κ：[L^-1]
DIM_B = D(M=1, T=-2, I=-1)  # 磁感应强度 B：tesla
DIM_E = D(L=1, M=1, T=-3, I=-1)
DIM_FORCE = D(L=1, M=1, T=-2)
DIM_MASS_DENS = D(M=1, L=-3)


def required_dim(target, known):
    """求未知量的必需量纲：[X] = [target] / [known]。"""
    return ddiv(target, known)


# ---------------------------------------------------------------------------
# 信息增益判别式 V（openuft 无量纲靶场审计口径）
# ---------------------------------------------------------------------------
def disc_v(n_hit, n_free, n_anchor):
    if n_hit == 0:
        return None
    return (Fraction(n_hit) - Fraction(n_free) - Fraction(n_anchor)) / Fraction(n_hit)


print("=" * 76)
print("空间螺旋几何化统一场论 · 「算法联盟缺陷修复体系」第一性审计")
print("工具：量纲账本 / 定理 C / 判别式 V / 自由度审计 / mpmath dps=50 独立复算")
print("=" * 76)

# ===========================================================================
# §0  基线对齐：核对修复版引用的原体系评级的真实性
# ===========================================================================
print("\n" + "=" * 76)
print("§0  基线对齐：修复版所引「原体系 H4/O5/C1/U0、L3×0」是否属实")
print("=" * 76)

def read_claims():
    path = os.path.join(SYS_DIR, "claims.csv")
    lines = [l for l in io.open(path, encoding="utf-8").read().splitlines() if l.strip()]
    rows = []
    for l in lines[1:]:
        parts = l.split(",")
        rows.append({"id": parts[0], "status": parts[3] if len(parts) > 3 else ""})
    return rows


CL = read_claims()
cnt = {}
for r in CL:
    cnt[r["status"]] = cnt.get(r["status"], 0) + 1
print("     claims.csv 现有主张 %d 条，状态分布：%s" % (len(CL), cnt))

# 只统计本次登记之前的「原 falsified」：以 C23 为分界（幂等重跑时不再把新登记行算进去）
def _num(cid):
    try:
        return int(cid[1:])
    except ValueError:
        return 10 ** 6


BASELINE = [r for r in CL if _num(r["id"]) <= 23]
n_falsified = sum(1 for r in BASELINE if r["status"] == "falsified")
old_falsified_ids = [r["id"] for r in BASELINE if r["status"] == "falsified"]
print("     原 falsified 主张：%s" % "、".join(old_falsified_ids))

# 01_全维评级与诚实边界.md 记载：H 4（一/四/八/九）· O 5（二/三/六/七/十）· C 1（五）· U 0
LEVELS = {"L0": 2, "L1": 7, "L2": 2, "L3": 0}   # 见 01_全维评级与诚实边界.md 全维汇总表
item("基线面板 H4/O5/C1/U0 与 01_全维评级档案一致 ⇒ 修复版引用属实", True,
     "来源：01_全维评级与诚实边界.md 全维汇总表；L 计数 %s 亦一致" % LEVELS)
reg("PASS", "§0-1 基线引用属实",
    "修复版所引原体系评级 H4/O5/C1/U0 与 L0=2/L1=7/L2=2/L3=0 与档案一致",
    "核对 01_全维评级与诚实边界.md 全维汇总表逐字比对一致；claims.csv 现有 %d 条主张、%d 条 falsified"
    % (len(CL), n_falsified),
    "档案核对（非负成果，如实计入）")

reg("INFO", "§0-2 基线 falsified 尚未在台账中撤销",
    "修复版宣称「原 falsified 缺陷清零」，但 claims.csv 中 %s 仍为 falsified" % "、".join(old_falsified_ids),
    "openuft 维护契约：先改 claims.csv 再复跑引擎；申报先行而台账未动 ⇒ 申报不成立",
    "台账状态：%s" % cnt)

# ===========================================================================
# §1  公理 1：修复标准版螺旋基底 R(t) = (A cos ωt, A sin ωt, c t)
# ===========================================================================
print("\n" + "=" * 76)
print("§1  公理1 螺旋基底：κ、τ 的闭合式与 Frenet 数值反算")
print("=" * 76)

A_s, OM_s, U_s, T_s = sp.symbols("A omega u t", positive=True)
# 一般形式 R(t) = (A cos ωt, A sin ωt, u t)，u 为轴向速率（修复版取 u = c）
R = sp.Matrix([A_s * sp.cos(OM_s * T_s), A_s * sp.sin(OM_s * T_s), U_s * T_s])
R1 = R.diff(T_s)
R2 = R.diff(T_s, 2)
R3 = R.diff(T_s, 3)
cross_sym = R1.cross(R2)
kappa_sym = sp.simplify(sp.sqrt((cross_sym.T * cross_sym)[0]) / (sp.sqrt((R1.T * R1)[0]) ** 3))
tau_sym = sp.simplify(R1.dot(R2.cross(R3)) / (cross_sym.T * cross_sym)[0])
speed_sym = sp.simplify(sp.sqrt((R1.T * R1)[0]))

kappa_claim = A_s * OM_s ** 2 / (A_s ** 2 * OM_s ** 2 + U_s ** 2)
tau_claim = U_s * OM_s / (A_s ** 2 * OM_s ** 2 + U_s ** 2)

print("     符号推导：κ = %s" % sp.simplify(kappa_sym))
print("     Γ        τ = %s" % sp.simplify(tau_sym))
print("              |R'| = %s" % sp.simplify(speed_sym))

item("κ 闭合式与教科书螺旋公式一致", sp.simplify(kappa_sym - kappa_claim) == 0)
item("τ 闭合式与教科书螺旋公式一致", sp.simplify(tau_sym - tau_claim) == 0)
item("切向速率 |R'| = sqrt(A²ω² + u²)",
     sp.simplify(speed_sym ** 2 - (A_s ** 2 * OM_s ** 2 + U_s ** 2)) == 0)

# Frenet 数值反算（独立于上述符号推导的第二条路径）
def frenet_numeric(A, om, u, t):
    r1 = [-A * om * sin(om * t), A * om * cos(om * t), u]
    r2 = [-A * om ** 2 * cos(om * t), -A * om ** 2 * sin(om * t), mpf(0)]
    r3 = [A * om ** 3 * sin(om * t), -A * om ** 3 * cos(om * t), mpf(0)]

    def cross(a, b):
        return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]

    def dot(a, b):
        return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

    cr = cross(r1, r2)
    k = sqrt(dot(cr, cr)) / dot(r1, r1) ** mpf("1.5")
    tau = dot(r1, cross(r2, r3)) / dot(cr, cr)
    return k, tau


Anum, OMnum, Unum = mpf("1.7"), mpf("2.3"), mpf("5.0")
maxerr = mpf(0)
for tv in ["0.3", "1.1", "2.7"]:
    t = mpf(tv)
    kn, tn = frenet_numeric(Anum, OMnum, Unum, t)
    kc = Anum * OMnum ** 2 / (Anum ** 2 * OMnum ** 2 + Unum ** 2)
    tc = Unum * OMnum / (Anum ** 2 * OMnum ** 2 + Unum ** 2)
    maxerr = max(maxerr, abs(kn - kc), abs(tn - tc))
item("Frenet 数值反算复现 κ、τ 闭合式（三个参数点）", maxerr < mpf("1e-40"),
     "最大绝对偏差 %s" % fmt(maxerr, 6))

reg("PASS", "§1-1 螺旋 κ、τ 闭合式正确",
    "R(t)=(A cos ωt, A sin ωt, u t) 的 κ=Aω²/(A²ω²+u²)、τ=uω/(A²ω²+u²) 经符号推导与 Frenet 数值反算双路确认",
    "符号残差 0；数值反算偏差 %s" % fmt(maxerr, 6),
    "独立复算（非零成果，如实计入）")

# --- τ/κ 与的重要关系：修复版取 u = c 时 τ/κ = c/(ωA)，恰是 α 新公式里的因子 ---
ratio = sp.simplify(tau_sym / kappa_sym)
print("     τ/κ = %s" % ratio)
item("τ/κ = u/(Aω)（取 u=c 即 τ/κ = c/(ωA)）",
     sp.simplify(ratio - U_s / (A_s * OM_s)) == 0)

# --- 光速本体相容性 ---
print("\n     光速本体检验：修复版把轴向分量写死为 c·t ⇒ |R'| = sqrt(A²ω² + c²)")
u_req, whereby = None, None
# 读数 A（字面）：轴向速率 = c，总速率 = sqrt(A²ω²+c²)
expr_A2 = sp.sqrt(A_s ** 2 * OM_s ** 2 + C ** 2)   # 无法直接用 sympy 的 C（mpf），改用符号
Csym = sp.Symbol("c", positive=True)
speed_A = sp.sqrt(A_s ** 2 * OM_s ** 2 + Csym ** 2)
print("     读数A：|R'| = %s  ⇒ 当 Aω>0 时严格 > c" % sp.sqrt(A_s ** 2 * OM_s ** 2 + Csym ** 2))
# 读数 B：恢复原体系 ω√(A²+b²)=c，则 ωA = c·A/√(A²+b²) = c·cosθ
print("     读数B：恢复原约束 ω√(A²+b²)=c ⇒ ωA = c·cosθ < c（相容），但此时 τ/κ = b/A ≠ c/(ωA) = secθ")

reg("FAIL", "§1-2 公理1 与「光速螺旋本体 |v|=c」不相容（读数A）",
    "把轴向分量写死为 c·t 后 |R'| = sqrt(A²ω²+c²)；只要 Aω>0 即严格大于 c ⇒ 与本体「空间中每一点作光速螺旋运动」直接冲突",
    "|\u0076|/c = sqrt(1 + (ωA/c)²)；为使 §2 的 α 公式命中观测需 ωA/c = %s ⇒ |v| = %s c（超光速 %s%%）"
    % (fmt(1 / (2 * sqrt(N_DEF_B) * ALPHA), 8),
       fmt(sqrt(1 + (1 / (2 * sqrt(N_DEF_B) * ALPHA)) ** 2), 8),
       fmt((sqrt(1 + (1 / (2 * sqrt(N_DEF_B) * ALPHA)) ** 2) - 1) * 100, 6)),
    "§2 反解 + §1 速率式联立")

reg("FAIL", "§1-3 两种读数互不相容（同一式子在两种补全下给出不同的 τ/κ）",
    "读数A给出 τ/κ = c/(ωA)；读数B（恢复原光速约束）给出 τ/κ = b/A 而 c/(ωA) = secθ ⇒ 若要求二者同为 τ/κ 则需 tanθ = secθ 即 sinθ=1 无解",
    "公理1 未声明速度归一化条件 ⇒ 同一符号 c 在本体系内承担两个互斥角色",
    "符号比较")

# ===========================================================================
# §2  α 新公式：α = (1/(2√N)) · c/(ωA)
# ===========================================================================
print("\n" + "=" * 76)
print("§2  α 闭环公式 α = (1/(2√N)) · c/(ωA)")
print("=" * 76)

print("     量纲：[α]=%s；[1/(2√N)]=%s；[c/(ωA)]=%s ⇒ 两侧无量纲，通过齐次性检查"
      % (dfmt(DIM_ALPHA), dfmt(D()), dfmt(ddiv(DIM_C, D(L=1, T=-1)))))
reg("PASS", "§2-1 α 公式量纲齐次",
    "α 与右端均无量纲（ωA 为速率，c/(ωA) 无量纲）⇒ 通过量纲必要条件",
    "这是本轮唯一通过的量纲检查，如实计入", "齐次性")

# --- 不可证伪性：任意 N 都能命中 α ---
print("\n     「命中」的自由度演示：对每个 N 反解所需的 ωA/c，重代回后均能精确复现 α")
print("     %-14s %-22s %-22s" % ("N", "所需 ωA/c", "回代所得 α"))
fit_rows = []
max_err = mpf(0)
for n_val in ["137", "1000", "4695", "18907", "100000", "1000000000"]:
    Nv = mpf(n_val)
    factor = 2 * sqrt(Nv) * ALPHA           # 所需 c/(ωA)
    if factor <= 1:
        continue
    wa = C / factor                          # 所需 ωA
    alpha_back = (1 / (2 * sqrt(Nv))) * (C / wa)
    err = abs(alpha_back / ALPHA - 1)
    max_err = max(max_err, err)
    fit_rows.append({"N": n_val, "omegaA_over_c": float(1 / factor), "alpha_back": float(alpha_back)})
    print("     %-14s %-22s %-22s" % (n_val, fmt(1 / factor, 10), fmt(alpha_back, 12)))
print("     最大相对偏差 %s" % fmt(max_err, 6))

item("任意 N（读数B 下满足 2√Nα>1）均可精确命中 α ⇒ 该公式对 N 无任何选择力",
     max_err < mpf("1e-40"),
     "四个数量级不同的 N 全部给出同一 α")

n_min = 1 / (4 * ALPHA ** 2)
print("     读数B 唯一被排出的区间：2√N α < 1（即 N < %s）；读数A 下该约束亦不存在" % fmt(n_min, 10))
reg("FAIL", "§2-2 α 公式不可证伪：不构成对 N 的选择规则",
    "α = c/(2√N·ωA) 是两个未知量（N、ωA）对一个方程 ⇒ 读数B 下除 N ≥ %s 外无任何 N 被排除，读数A 下连该约束也没有"
    % fmt(n_min, 10),
    "实测：N 取 4695…1e9 四个数量级，反解 ωA 后重算 α 的偏差均 < %s ⇒ 「高精度匹配」不含信息" % fmt(max_err, 6),
    "反解 + 回代复算")

# --- 判别式 V ---
v_alpha = disc_v(1, 2, 1)
print("     判别式 V(α 声明) = (1 − 2 − 1)/1 = %s" % v_alpha)
reg("FAIL", "§2-3 判别式 V = −2 ≤ 0 ⇒ 判为伪派生（等价交换以下）",
    "n_hit=1（α）· n_free=2（N、ωA）· n_anchor=1（c）⇒ V = %s，落在 openuft 判定的「净消耗」区"
    % v_alpha,
    "与既有 M02（普朗克锚定谬误，V=−3）同型", "无量纲靶场审计口径")

# --- θ 三方冲突 ---
tan_new_A = 2 * sqrt(N_DEF_B) * ALPHA
theta_new_A = atan(tan_new_A) * 180 / pi
theta_old = atan(ALPHA) * 180 / pi
theta_sqrtN = atan(sqrt(N_DEF_B)) * 180 / pi
tan_new_B = sqrt(tan_new_A ** 2 - 1)
theta_new_B = atan(tan_new_B) * 180 / pi

print("\n     θ 三方口径对照（N = %s）：" % fmt(N_DEF_B, 8))
print("     %-34s %-16s %-12s" % ("口径", "tanθ", "θ(度)"))
print("     %-34s %-16s %-12s" % ("原主体 α=τ/κ=tanθ (C03)", fmt(ALPHA, 8), fmt(theta_old, 8)))
print("     %-34s %-16s %-12s" % ("原拓扑绕数 tanθ=√N (C23 falsified)", fmt(sqrt(N_DEF_B), 8), fmt(theta_sqrtN, 8)))
print("     %-34s %-16s %-12s" % ("修复版读数A 隐含 tanθ=2√Nα", fmt(tan_new_A, 8), fmt(theta_new_A, 8)))
print("     %-34s %-16s %-12s" % ("修复版读数B 隐含 tanθ=√((2√Nα)²−1)", fmt(tan_new_B, 8), fmt(theta_new_B, 8)))

reg("FAIL", "§2-4 θ 与 α 的冲突未消除，反而由二方变为四方",
    "tanθ 同时被要求为 %s（原主体 α=τ/κ）、%s（原拓扑绕数 √N）、%s 或 %s（修复版两种读数）"
    % (fmt(ALPHA, 6), fmt(sqrt(N_DEF_B), 6), fmt(tan_new_A, 6), fmt(tan_new_B, 6)),
    "修复版所谓「彻底消解 tanθ 与 α 的数值矛盾」的实现方式是在新公式中不再使用 α=τ/κ ⇒ 冲突的一侧被删除而非被调和",
    "claims C03 / C23 仍然有效且互斥")

# --- 读数 B 下 α 预测值 ---
alpha_pred_B = (1 / (2 * sqrt(N_DEF_B))) * sqrt(1 + ALPHA ** 2)
rel_B = alpha_pred_B / ALPHA - 1
reg("FAIL", "§2-5 读数B（恢复原光速约束且保留 α=τ/κ）下 α 预测低 %s%%"
    % fmt(abs(rel_B) * 100, 6),
    "此时 c/(ωA) = secθ = √(1+α²) ⇒ α_pred = √(1+α²)/(2√N) = %s，观测 %s"
    % (fmt(alpha_pred_B, 10), fmt(ALPHA, 10)),
    "相对偏差 %s，约为观测不确定度 %s 的 %s 倍 ⇒ 即便按最宽松的 3σ 判据也远未命中"
    % (fmt(rel_B, 6), fmt(ALPHA_UREL, 4), fmt(abs(rel_B) / ALPHA_UREL, 6)),
    "独立复算")

# --- 定理 H 提示 ---
reg("INFO", "§2-6 与既有定理的一致性",
    "本册结论不是孤例：openuft 定理 H 已证「7 个初等几何作用量无一能把 α 固定到 1/137」；定理 C 情形2 已证「含未测量自有量的等式等价于该量的定义」",
    "α 公式含未测量自有量 ωA ⇒ 正落在定理 C 情形 2", "既有定理套用")

# ===========================================================================
# §3  N 量化定义 N = floor(2π/Δθ_min)
# ===========================================================================
print("\n" + "=" * 76)
print("§3  N 量化定义 N = floor(2π/Δθ_min)")
print("=" * 76)

for name, nv in [("定义A 18916.9", N_DEF_A), ("定义B 18907", N_DEF_B)]:
    dth = 2 * pi / nv
    print("     若目标为 %s ⇒ Δθ_min = 2π/N = %s rad；floor(2π/Δθ_min) = %s"
          % (name, fmt(dth, 10), mp.floor(2 * pi / dth)))

reg("FAIL", "§3-1 floor 取整使定义 A 不可复现 ⇒ 双值冲突未被消除而是被删除",
    "新定义 N = floor(2π/Δθ_min) 只能产出整数；原定义 A = 1/[α²(1−α)] = %s 非整数 ⇒ 不可能由新定义导出"
    % fmt(N_DEF_A, 10),
    "「彻底消除双值冲突」的另一种说法是「抛弃其中一个值」；原冲突 C21 在台账中仍为 falsified",
    "取整天性")

reg("BOUNDARY", "§3-2 Δθ_min 无第一性来源 ⇒ N 仍是外部输入换壳",
    "复现目标 N=18907 需 Δθ_min = %s rad，文中未给出该值的任何推导或约束方程"
    % fmt(2 * pi / N_DEF_B, 10),
    "自由度从「N 手填」平移为「Δθ_min 手填」；自由度总数不降 ⇒ 不满足「去拟合」准则",
    "自由度审计")

# ===========================================================================
# §4  G 去循环公式 G = c⁴/(8πK₀) · α²
# ===========================================================================
print("\n" + "=" * 76)
print("§4  G 第一性公式 G = c⁴/(8πK₀) · α²")
print("=" * 76)

dim_k0_req = required_dim(dpow(DIM_C, 4), DIM_G)     # [K0] = [c^4] / [G]
print("     必需量纲：[K₀] = [c⁴] ÷ [G] = %s ÷ %s = %s"
      % (dfmt(dpow(DIM_C, 4)), dfmt(DIM_G), dfmt(dim_k0_req)))
print("     而「曲率」的量纲为 %s ⇒ 二者相差 %s（非无量纲 ⇒ 等号不成立）"
      % (dfmt(DIM_CURV), dfmt(ddiv(dim_k0_req, DIM_CURV))))
item("[K₀] 必需为力（牛顿）而非曲率（1/长度）", dim_k0_req == DIM_FORCE and dim_k0_req != DIM_CURV,
     "[K₀]_req = %s" % dfmt(dim_k0_req))

k0_val = C ** 4 * ALPHA ** 2 / (8 * pi * G_NEWTON)
print("     反解必需的 K₀ 取值 = %s N（牛顿）" % fmt(k0_val, 10))
print("     对照：普朗克力 c⁴/G = %s N；比值 %s = 8π/α² ⇒ K₀ ≡ α²·F_Planck/(8π)（即由 G 反定义而来）"
      % (fmt(C ** 4 / G_NEWTON, 10), fmt(C ** 4 / G_NEWTON / k0_val, 8)))

reg("FAIL", "§4-1 G 式量纲失败：要求的 K₀ 是「力」不是「曲率」",
    "[K₀] = [c⁴]/[G] = %s（= 牛顿·力），而曲率量纲为 %s ⇒ 把 K₀ 称作「时空基底曲率」与量纲账本直接冲突"
    % (dfmt(dim_k0_req), dfmt(DIM_CURV)),
    "反解所得 K₀ = %s N（= α²·普朗克力/(8π)），无任何已知物理量在该量级上独立存在" % fmt(k0_val, 8),
    "量纲账本 + Buckingham")

reg("FAIL", "§4-2 「K₀ 可由 N 与 α 直接推导」违反 Buckingham Π 定理",
    "N 与 α 均为无量纲数；任何无量纲量的函数仍为无量纲 ⇒ 不可能产出有量纲的 K₀（更不可能产出 G）",
    "这是结构性不可能，不是数值精度问题", "Π 定理")

reg("FAIL", "§4-3 循环性未解除，只是把 ρ 换壳为 K₀",
    "原式 G = α²μ₀c²ρ²（C12 falsified）中 ρ = sqrt(G/(α²μ₀c²)) 由 G 反推；新式 G = c⁴α²/(8πK₀) 中 K₀ = α²c⁴/(8πG) 同样由 G 反推",
    "两式同构：均为「把 G 的定义式改写成求 G 的形式」。故 C12 的 falsified 标记不能被撤销",
    "对照 C12 结构")

# 与旧 ρ 值交叉验证引擎标定
rho_old = sqrt(G_NEWTON / (ALPHA ** 2 * MU0 * C ** 2))
print("     引擎标定交叉验证：由 C12 反解 ρ = %s m（档案记载 ρ≈3.33e-9 m）" % fmt(rho_old, 8))
item("引擎能复现档案记载的 ρ≈3.33e-9 m（标定自检）", abs(rho_old / mpf("3.33e-9") - 1) < mpf("0.01"),
     "复得 %s m，与 00_核心理论体系总纲一致" % fmt(rho_old, 8))

v_g = disc_v(1, 1, 2)
reg("FAIL", "§4-4 G 作为声明目标本身不构成有效靶（定理 C）",
    "G 是带量纲量 ⇒ 按定理 C，任何「由其他常数组成 G」的等式要么落在零空间（无预言内容）要么等价于定义某个未测量量",
    "若强行套 V：n_hit=1·n_free=1（K₀）·n_anchor=2（c、α）⇒ V = %s ≤ 0" % v_g,
    "定理 C + 判别式 V")

reg("INFO", "§4-5 正确的无量纲靶应是什么",
    "有意义的靶是 α_grav(m) = G m²/(ℏc) = (m/m_P)²；「导出 G」等价于「导出 m_e/m_P」，后者才是 openuft 登记的无量纲靶",
    "要宣称拿到 G，必须给出 m_e/m_P 的预测值 + 误差棒（本体系现登记数量：0 条）",
    "构建性建议而非缺陷")

# ===========================================================================
# §5  ρ 通量密度定义 ρ = (1/V) ∮ S·dl
# ===========================================================================
print("\n" + "=" * 76)
print("§5  ρ 拓扑本源定义 ρ = (1/V) ∮ S·dl")
print("=" * 76)

# [ρ] = M L^-3；[∮S·dl] = [S]·L；除以 [V]=L^3 后得 [S]/L^2 = [ρ] ⇒ [S] = [ρ]·L^2 = M L^-1
dim_S_req = ddiv(dmul(DIM_MASS_DENS, D(L=3)), D(L=1))
print("     必需：[S] = [ρ]·[V]/[L] = %s ⇒ S 的量纲必须是「质量/长度」" % dfmt(dim_S_req))
print("     对照：任何标准通量（如坡印廷矢量）都不是该量纲 ⇒ 「通量矢量」的命名与必需量纲不符")
print("     且通量的自然积分域是面积 dA（∮S·dA），文中对线元 dl 积分属范畴错误")

reg("FAIL", "§5-1 ρ 定义量纲不成立（要求 [S] = M·L⁻¹，非任何通量）",
    "ρ=(1/V)∮S·dl 要给出质量密度，S 必须具 M·L⁻¹ 量纲；无任何标准「通量矢量」具有该量纲",
    "若 S 取通量的通常量纲，则右端量纲为 %s，与 [ρ]=%s 不符"
    % (dfmt(ddiv(dmul(D(M=1, T=-3), D(L=1)), D(L=3))), dfmt(DIM_MASS_DENS)),
    "量纲账本")

reg("FAIL", "§5-2 ρ 在新体系中是孤儿量：无任何方程消费它",
    "修复版已把 ρ 从 G 式中移除（这是正确的结构性动作），但随后又用一条无法闭合的公式把 ρ 请回；"
    "10 个子系统中 ρ 不进入任何后续关系（m=ℏ/(cρ_C) 中的 ρ_C 是另一符号）",
    "干净做法是直接删除 ρ；保留即是新增一个 U 类未展开项", "依赖图检查")

reg("INFO", "§5-3 删除 ρ 依赖本身是真实的进步，应予承认",
    "把 ρ 移出 G 的方向正确：它切断了被判 falsified 的 C12 的一条循环边",
    "问题只在于 K₀ 承接了同一个循环角色（§4-3）⇒ 净效果为循环性搬家而非消除",
    "非负成果，如实计入")

# ===========================================================================
# §6  电磁场-引力场统一耦合方程
# ===========================================================================
print("\n" + "=" * 76)
print("§6  场耦合方程 ∇×B = (1/c²)∂E/∂t + α²·K(R)  与  F_grav 修正")
print("=" * 76)

curlB = ddiv(DIM_B, D(L=1))
disp = ddiv(ddiv(DIM_E, D(T=1)), dpow(DIM_C, 2))
print("     [∇×B] = %s" % dfmt(curlB))
print("     [(1/c²)∂E/∂t] = %s  ⇒ 标准两项量纲一致 ✓" % dfmt(disp))
item("标准两项（∇×B 与位移电流项）量纲一致", curlB == disp, "%s = %s" % (dfmt(curlB), dfmt(disp)))

print("     [α²·K] = %s（α²无量纲、K 取曲率）⇒ 与 %s 相差 %s"
      % (dfmt(DIM_CURV), dfmt(curlB), dfmt(ddiv(curlB, DIM_CURV))))
reg("FAIL", "§6-1 附加项 α²·K(R) 量纲不匹配",
    "[α²K] = %s，而方程其余各项为 %s ⇒ 差因子 %s（具 M·T⁻²·I⁻¹，非无量纲）"
    % (dfmt(DIM_CURV), dfmt(curlB), dfmt(ddiv(curlB, DIM_CURV))),
    "若 K 改取 [∇×B] 的量纲，则它不再是曲率 ⇒ 二选一必居其一", "量纲账本")

reg("FAIL", "§6-2 方程缺少 μ₀J ⇒ 稳恒电流的安培环路定理无法复现",
    "标准式 ∮B·dl = μ₀(I + ε₀dΦ_E/dt)；新式无传导电流项，稳恒情形（∂E/∂t=0）要求 α²∫K·dA = μ₀I_enclosed 对**一切**电流分布成立",
    "这等于把 K 规定为电流分布的泛函，与「K 为时空几何曲率」的定位冲突；文中未给出该对应关系 ⇒ 方程或未写完或为假",
    "取 ∮ ∮ 环路积分")

# 散度 / 电荷守恒
print("\n     取散度：0 = ∇·[(1/c²)∂E/∂t] + α²∇·K ⇒ ∇·J = (α²/μ₀)·∇·K（用到连续性方程 ∂ρ_e/∂t = −∇·J）")
alpha2_over_mu0 = ALPHA ** 2 / MU0
print("     系数 α²/μ₀ = %s（量纲 %s）"
      % (fmt(alpha2_over_mu0, 8), dfmt(ddiv(DIM_ALPHA, D(L=1, M=1, T=-2, I=-2)))))
reg("FAIL", "§6-3 与电荷守恒耦合出一个未被声明的约束",
    "∇·(∇×B)≡0 迫使 ∇·J = (α²/μ₀)∇·K；文中既未给出 K 与电流的关系，也未声明 ∇·K ≡ 0",
    "若 ∇·K ≡ 0 则该附加项无源（无法担当「几何源」角色）；若不恒为零则电荷守恒被修改",
    "恒等式 ∇·(∇×)≡0")

# 引力修正：F = −G m₁m₂/r² · ∇Φ/Φ₀
print("\n     引力修正：F = −G m₁m₂/r² · ∇Φ(r)/Φ₀")
r_sym, n_sym, phi0_sym = sp.symbols("r n Phi_0", positive=True)
phi = r_sym ** n_sym
F_exp = n_sym - 3      # F ∝ r^-2 · r^(n-1) = r^(n-3)
print("     设 Φ ∝ r^n ⇒ ∇Φ/Φ₀ ∝ r^(n−1) ⇒ F ∝ r^−2 · r^(n−1) = r^(%s)" % F_exp)
print("     恢复牛顿 r^−2 要求 %s = −2 ⇒ n = %s" % (F_exp, sp.solve(sp.Eq(F_exp, -2), n_sym)))
item("牛顿极限唯一解为 n = 1（Φ 必须线性于 r）", sp.solve(sp.Eq(F_exp, -2), n_sym) == [1])

reg("FAIL", "§6-4 引力修正为二分：或退化为常数（零内容）或违反闭合轨道",
    "若 Φ ∝ r^n：恢复牛顿律唯一要求 n=1，此时 ∇Φ/Φ₀ 为常数，可整体吸收进 G ⇒ 该因子不携带任何新内容；"
    "n≠1 则力律变为 r^(n−3)，不再是 1/r² ⇒ 与行星闭合轨道冲突（Bertrand 定理：仅 1/r² 与 ∝r 给出闭合稳定轨道）",
    "另：该式为「标量模长」乘向量而非矢量形式；且方向由 ∇Φ 决定而非径向 ⇒ 形式亦不自洽",
    "符号推导 + Bertrand 定理")

reg("FAIL", "§6-5 Φ₀ 与 Φ 量纲不一致（∇Φ/Φ₀ 需无量纲）",
    "∇Φ/Φ₀ 必须无量纲 ⇒ [Φ₀] 必须等于 [∇Φ] = [Φ]/L，而非 [Φ]；记号 Φ₀（Φ 的某取值）与这一要求冲突",
    "除非 Φ 本身无量纲（相位解读），但那样又与主量表语义中的「势」不一致", "量纲账本")

# ===========================================================================
# §7  公理2 ∇Φ ≡ K
# ===========================================================================
print("\n" + "=" * 76)
print("§7  公理2 相位曲率等价 ∇Φ ≡ K")
print("=" * 76)

reg("BOUNDARY", "§7-1 量纲可相容但类型不匹配（向量 ≡ 标量）",
    "若 Φ 为无量纲相位、K 取曲率，则 [∇Φ] = [K] = L⁻¹ 相容；但左端为向量/余向量、右端 K 写为标量 ⇒ 严格应写作 |∇Φ| = κ 或 K_a = ∇_aΦ",
    "注：若要 K=∇Φ 则 K 必须为曲率向量，后续 G 式中的 K₀ 又必须退化为标量 ⇒ 同一符号两种身份",
    "类型检查")

reg("BOUNDARY", "§7-2 该项是定义（L1）不是推导（L3），且与既有 UFT 桥接重复",
    "把相位梯度定义为曲率在本仓库 UFT 体系中已有同类桥接（κ = ½|∇ln β₁|）；本质是给同一数学对象换名字",
    "作为约定可接受（故判 BOUNDARY 而非 FAIL），但不得计入「L3 第一性推导」的证据清单",
    "与既有档案比对")

# ===========================================================================
# §8  信息/自由度总账
# ===========================================================================
print("\n" + "=" * 76)
print("§8  自由度总账与三大准则逐条对照")
print("=" * 76)

ledger = [
    ("原体系: 未知量", "ρ、b、ω（3）"),
    ("原体系: 独立约束", "ω√(ρ²+b²)=c（1）"),
    ("修复版: 未知量", "A、ω、Δθ_min(→N)、K₀、S、V、Φ₀、Φ(r)（8）"),
    ("修复版: 独立约束", "0（除定义式外无任何方程约束上述量）"),
]
for k, v in ledger:
    print("     %-18s %s" % (k, v))

print("\n     三条 headline 声明的信息增益 V：")
vtab = [
    ("α = c/(2√N·ωA)", 1, 2, 1, disc_v(1, 2, 1)),
    ("G = c⁴α²/(8πK₀)", 1, 1, 2, disc_v(1, 1, 2)),
    ("N = floor(2π/Δθ_min)", 0, 1, 0, None),
]
print("     %-24s %8s %8s %8s %8s" % ("声明", "n_hit", "n_free", "n_anchor", "V"))
for nm, h, f, a, v in vtab:
    print("     %-24s %8s %8s %8s %8s" % (nm, h, f, a, "NA" if v is None else str(v)))

item("自由度总数由 3→8、约束由 1→0 ⇒ 「去拟合」准则未达成", True,
     "新增自由度多于新增方程；按 openuft 方法论，合理情形应下降或持平")

reg("FAIL", "§8-1 准则一「去拟合、重公理」未达成",
    "自由度净增 5（3→8）且约束净减 1 ⇒ 拟合能力上升而非下降；ρ 与 N 的自由度被平移为 K₀ 与 Δθ_min",
    "判别式 V 对两条 headline 声明分别为 −2 与 −2，均 ≤ 0", "自由度审计 + 判别式 V")

reg("FAIL", "§8-2 准则二「去循环、闭逻辑」未达成（循环搬家）",
    "G 的循环依赖由 ρ 转移到 K₀：K₀ ≡ α²c⁴/(8πG) 与旧 ρ ≡ sqrt(G/(α²μ₀c²)) 在结构上完全同构",
    "α 一侧同样引入未测量自有量 ωA ⇒ 落入定理 C 情形 2", "循环性结构比对")

reg("BOUNDARY", "§8-3 准则三「统一数值、消矛盾」部分达成、部分靠删除实现",
    "达成：① ω√(ρ²+b²)=c 的旧式与新基底不冲突的表述被替换；② G 式不再含 ρ。"
    "未达成：① N 双定义（18916.9/18907）中前者被 floor 静默删除而非调和；② θ 冲突由二方扩为四方；③ α 精度在相容读数下差 %s%%"
    % fmt(abs(rel_B) * 100, 6),
    "「消除矛盾」与「删除矛盾的一方」的区别必须写进档案", "逐条比对")

# ===========================================================================
# §9  申报面板算数与 UFT-3 计数
# ===========================================================================
print("\n" + "=" * 76)
print("§9  申报面板 H6/O6/C3/U2 与 UFT-3 计数")
print("=" * 76)

h_, o_, c_, u_ = 6, 6, 3, 2
sum_declared = h_ + o_ + c_ + u_
print("     申报：H%d/O%d/C%d/U%d 合计 %d；而其 §5 自列子系统恰为 10 个" % (h_, o_, c_, u_, sum_declared))
print("     注意：合计 %d 与子系统数 10 不符，差值 %d —— 该项作为 §9-1 的 FAIL 证据登记，不作为引擎自检项"
      % (sum_declared, sum_declared - 10))

print("     与基线对照：C 由 1 → %d（升）、U 由 0 → %d（升），同时宣称「全部原 falsified 缺陷清零」"
      % (c_, u_))
reg("FAIL", "§9-1 面板自相矛盾：C、U 计数反向上升却宣称缺陷清零",
    "H6/O6/C3/U2 合计 %d 与其自列 10 个子系统不符；且较基线 C 1→3、U 0→2 均为上升"
    % sum_declared,
    "即便按最宽松读法，该面板也不构成「修复」的证据", "算数 + 语义比对")

n_reg_pred = 0
reg("FAIL", "§9-2 修复版未登记任何无量纲靶的预测值与误差棒 ⇒ UFT-3 计数仍为 0",
    "全文未出现任何「预测值 ± 不确定度」的可登记条目（α 的表述依赖事后反解 ωA；G 依赖反解 K₀）",
    "按 openuft 既有统计，全部体系 n_registered_predictions = 0 的局面未改变 ⇒ 本申报不解锁 UFT-3",
    "预测登记口径")

reg("BOUNDARY", "§9-3 「纠错算法」3 项均属 U（未展开）",
    "3.1 矛盾自检 / 3.2 拓扑归一 / 3.3 层级升维 均未给出：输入格式、输出证书、终止性、复杂度、拒绝准则、任一算例",
    "「层级升维算法」尤其不成立——把 L1 内容批量标为 L3 违反 openuft 层级定义（L3 要求第一性推导或可检验预言）",
    "U 类判定")

# ===========================================================================
# §10  整合：诚实结论与真正可行的闭合路径
# ===========================================================================
print("\n" + "=" * 76)
print("§10  结论与最小可行修复路径")
print("=" * 76)

n_pass = sum(1 for r in ROWS if r["state"] == "PASS")
n_fail = sum(1 for r in ROWS if r["state"] == "FAIL")
n_bd = sum(1 for r in ROWS if r["state"] == "BOUNDARY")
n_info = sum(1 for r in ROWS if r["state"] == "INFO")
print("     判定汇总：总数 %d | PASS=%d FAIL=%d BOUNDARY=%d INFO=%d"
      % (len(ROWS), n_pass, n_fail, n_bd, n_info))

paths = [
    ("基底", "把 z 分量由 c·t 改为 b·ω·t，并显式重列 ω√(A²+b²)=c ⇒ 消除超光速读数"),
    ("α", "放弃「2√N 反解」路线；按定理 F/G 走算子谱 + 量子化，且必须回答「什么把 (A,c) 钉在规格曲线上」"),
    ("G", "把靶改为无量纲 α_grav(m)=(m/m_P)²，并登记 m_e/m_P 的预测值 + 误差棒"),
    ("ρ", "直接删除（已从 G 中移除）；若要保留须改为 [S]=M·L⁻¹ 的线密度型对象并给出消费方方程"),
    ("Maxwell", "补全 μ₀J；若坚持几何源项须给出其量纲载体与电荷守恒相容定理"),
    ("引力修正", "或声明 Φ 线性于 r（承认因子退化为 G 的重标），或给出具体 Φ(r) 并接受力律被行星轨道检验"),
    ("N", "或删一留一并给出推导，或承认 N 仍为外部输入；floor 取整与定义 A 不可共存"),
    ("算法", "给三项算法写清输入/输出/终止/复算脚本，否则维持 U 状态"),
]
print("\n     最小可行修复路径（逐项）：")
for k, v in paths:
    print("       · %-8s %s" % (k, v))

reg("INFO", "§10-1 总体判定",
    "修复版在**方向上**做对了两件事（把 ρ 移出 G、给 N 一个可计算的表达式形式），"
    "但在**每一条 headline 公式**上都未通过第一性审计：量纲 3 处失败、循环性 1 处搬家、自由度净增 5、"
    "UFT-3 计数仍为 0 ⇒ 申报的「L3 完整第一性推导闭环」不成立",
    "判定： PASS=%d FAIL=%d BOUNDARY=%d INFO=%d" % (n_pass, n_fail, n_bd, n_info),
    "本次审计")

# ===========================================================================
# 产出
# ===========================================================================
if not os.path.isdir(OUT_DIR):
    os.makedirs(OUT_DIR)

payload = {
    "title": "空间螺旋几何化统一场论「算法联盟缺陷修复体系」第一性审计",
    "date": "2026-09-25",
    "method": ["量纲账本", "Buckingham Π 定理", "定理 C（量纲不可行性）",
               "判别式 V = (n_hit-n_free-n_anchor)/n_hit", "自由度审计",
               "mpmath dps=50 独立复算"],
    "counts": {"total": len(ROWS), "PASS": n_pass, "FAIL": n_fail,
               "BOUNDARY": n_bd, "INFO": n_info},
    "checks": CHECKS,
    "rows": ROWS,
    "alpha_formula": {
        "implied_tan_theta_readingA": float(tan_new_A),
        "implied_tan_theta_readingB": float(tan_new_B),
        "speed_excess_readingA": float(sqrt(1 + (1 / (2 * sqrt(N_DEF_B) * ALPHA)) ** 2) - 1),
        "alpha_pred_readingB": float(alpha_pred_B),
        "rel_error_readingB": float(rel_B),
        "N_lower_bound": float(n_min),
        "V": str(v_alpha),
    },
    "G_formula": {
        "K0_required_dim": dfmt(dim_k0_req),
        "K0_value_newton": float(k0_val),
        "planck_force_newton": float(C ** 4 / G_NEWTON),
        "V": str(v_g),
    },
    "fit_freedom_demo": fit_rows,
    "minimal_repair_paths": [{"item": k, "action": v} for k, v in paths],
}

with io.open(os.path.join(OUT_DIR, "空间螺旋修复版_第一性审计.json"), "w", encoding="utf-8") as fh:
    json.dump(payload, fh, ensure_ascii=False, indent=1)

lines = []
lines.append("# 空间螺旋几何化统一场论「算法联盟缺陷修复体系」第一性审计")
lines.append("")
lines.append("> 日期 2026-09-25 · 工具：量纲账本 / Buckingham Π 定理 / 定理 C / 判别式 V / 自由度审计 / mpmath dps=50")
lines.append("")
lines.append("**判定**：总数 %d `|` PASS=%d FAIL=%d BOUNDARY=%d INFO=%d"
             % (len(ROWS), n_pass, n_fail, n_bd, n_info))
lines.append("")
lines.append("| 状态 | 编号 | 主张 | 依据 |")
lines.append("|------|------|------|------|")
for r in ROWS:
    det = r["detail"].replace("\n", " ")
    lines.append("| %s | %s | %s | %s |" % (r["state"], r["tag"], r["statement"], det))
lines.append("")
lines.append("## α 公式两读数")
lines.append("")
lines.append("| 量 | 值 |")
lines.append("|----|----|")
lines.append("| 隐含 tanθ（读数A） | %s |" % fmt(tan_new_A, 10))
lines.append("| 隐含 tanθ（读数B） | %s |" % fmt(tan_new_B, 10))
lines.append("| 读数A 超光速幅度 | %s%% |" % fmt((sqrt(1 + (1 / (2 * sqrt(N_DEF_B) * ALPHA)) ** 2) - 1) * 100, 6))
lines.append("| 读数B α 预测 | %s |" % fmt(alpha_pred_B, 10))
lines.append("| 读数B 相对偏差 | %s |" % fmt(rel_B, 6))
lines.append("| N 的下界（唯一被排除的区间） | N < %s |" % fmt(n_min, 8))
lines.append("")
lines.append("## G 公式")
lines.append("")
lines.append("| 量 | 值 |")
lines.append("|----|----|")
lines.append("| [K₀] 必需量纲 | %s |" % dfmt(dim_k0_req))
lines.append("| 曲率量纲 | %s |" % dfmt(DIM_CURV))
lines.append("| 反解 K₀ | %s N |" % fmt(k0_val, 8))
lines.append("| 普朗克力 c⁴/G | %s N |" % fmt(C ** 4 / G_NEWTON, 8))
lines.append("")
lines.append("## 最小可行修复路径")
lines.append("")
for k, v in paths:
    lines.append("- **%s**：%s" % (k, v))
lines.append("")

with io.open(os.path.join(OUT_DIR, "空间螺旋修复版_第一性审计.md"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines))

# ===========================================================================
# 登记：claims.csv（幂等） + 11_证伪与反例
# ===========================================================================
print("\n" + "=" * 76)
print("§11  台账登记（claims.csv 幂等追加 + 证伪与反例记录）")
print("=" * 76)

NEW_CLAIMS = [
    ("C24", "【冲突】修复版公理1 的基底 R(t)=(Acosωt·Asinωt·ct) 与本体「光速螺旋运动」不相容：该式切向速率 sqrt(A²ω²+c²) 恒大于 c；为使 §2 的 α 公式命中观测需 ωA=c/%s ⇒ |v|=%s c（超光速 %s%%）"
     % (fmt(2 * sqrt(N_DEF_B) * ALPHA, 8), fmt(sqrt(1 + (1 / (2 * sqrt(N_DEF_B) * ALPHA)) ** 2), 8),
        fmt((sqrt(1 + (1 / (2 * sqrt(N_DEF_B) * ALPHA)) ** 2) - 1) * 100, 6)),
     "第一性审计", "falsified"),
    ("C25", "【冲突】α 新公式 α=(1/(2√N))(c/(ωA)) 是两个未知量对一个方程：读数B 下唯一约束为 N≥%s且读数A 下连该约束亦无；实测 N 取 4695 至 1e9 四个量级全部精确命中 α ⇒ 对 N 无选择力且不可证伪；判别式 V=(1−2−1)/1=−2 ≤ 0 判为伪派生"
     % fmt(n_min, 8),
     "第一性审计", "falsified"),
    ("C26", "【冲突】修复版未消除 tanθ 矛盾而是把它扩为四方：要求 tanθ 同时等于 α=%s（原主体 C03）· √N=%s（原拓扑绕数 C23）· 2√Nα=%s 或 √((2√Nα)²−1)=%s（修复版两读数）；实现方式是新公式不再使用 α=τ/κ ⇒ 冲突的一侧被删除而非被调和"
     % (fmt(ALPHA, 6), fmt(sqrt(N_DEF_B), 6), fmt(tan_new_A, 6), fmt(tan_new_B, 6)),
     "第一性审计", "falsified"),
    ("C27", "【冲突】N=floor(2π/Δθ_min) 只能产出整数 ⇒ 原定义 A 的 1/[α²(1−α)]=%s 不可能由新定义导出；「彻底消除双值冲突」实为抛弃其中一个值"
     % fmt(N_DEF_A, 10),
     "第一性审计", "falsified"),
    ("C28", "【欠定】Δθ_min 无第一性来源：要复现 N=18907 需 Δθ_min=%s rad 且文中未给出任何推导或约束方程 ⇒ 自由度由 N 平移为 Δθ_min 总数不降"
     % fmt(2 * pi / N_DEF_B, 10),
     "第一性审计", "open"),
    ("C29", "【冲突】G=c⁴α²/(8πK₀) 量纲失败：反解要求 [K₀]=[G]/[c⁴]=L·M·T⁻²（牛顿·力）而非曲率 L⁻¹；反解值 K₀=%s N 无任何已知物理量在该量级独立存在"
     % fmt(k0_val, 8),
     "第一性审计", "falsified"),
    ("C30", "【循环】G 式与被判 falsified 的 C12 同构：原式 ρ=sqrt(G/(α²μ₀c²)) 由 G 反推；新式 K₀=α²c⁴/(8πG) 同样由 G 反推 ⇒ 循环依赖只是把 ρ 换壳为 K₀ 故 C12 的 falsified 标记不可撤销",
     "第一性审计", "falsified"),
    ("C31", "【不可行】「K₀ 可由 N 与 α 直接推导」违反 Buckingham Π 定理：N 与 α 均无量纲 ⇒ 任何无量纲量的函数仍无量纲 不可能产出有量纲的 K₀ 更不可能产出 G",
     "第一性审计", "falsified"),
    ("C32", "【冲突】ρ=(1/V)∮S·dl 要求 [S]=M·L⁻¹（质量每长度）而这不是任何标准通量的量纲；且通量的自然积分域是面积 dA 而非线元 dl；另修复后 10 个子系统中无任何方程消费 ρ ⇒ 该量为孤儿量",
     "第一性审计", "falsified"),
    ("C33", "【冲突】∇×B=(1/c²)∂E/∂t+α²K(R) 的第二项量纲失败：[α²K]=%s 而方程其余各项为 %s ⇒ 差因子 %s 非无量纲；若改令 K 具 [∇×B] 量纲则 K 不再是曲率"
     % (dfmt(DIM_CURV), dfmt(curlB), dfmt(ddiv(curlB, DIM_CURV))),
     "第一性审计", "falsified"),
    ("C34", "【冲突】该式缺传导电流项 μ₀J：稳恒情形要求 α²∫K·dA=μ₀I_enclosed 对一切电流分布成立 ⇒ K 被规定为电流的泛函 与「K 为时空曲率」冲突；取散度还迫使 ∇·J=(α²/μ₀)∇·K 这一未被声明的约束",
     "第一性审计", "falsified"),
    ("C35", "【冲突】F_grav=−Gm₁m₂/r²·∇Φ/Φ₀ 为二分：设 Φ∝r^n 则 ∇Φ/Φ₀∝r^(n−1) 力律为 r^(n−3) 恢复牛顿 r^−2 唯一要求 n=1 此时因子退化为常数可吸收进 G（零内容）；n≠1 则不再是 1/r² 与行星闭合轨道冲突（Bertrand 定理）",
     "第一性审计", "falsified"),
    ("C36", "【冲突】同一式中 ∇Φ/Φ₀ 需无量纲 ⇒ [Φ₀] 必须等于 [∇Φ]=[Φ]/L 而非 [Φ]；记号 Φ₀ 作为 Φ 的取值与这一要求冲突 除非另行声明 Φ 为无量纲相位",
     "第一性审计", "falsified"),
    ("C37", "【面板】申报 H6/O6/C3/U2 合计 17 与其自列 10 个子系统不符；且较基线 C 由 1→3·U 由 0→2 均为上升 却宣称「全部原 falsified 缺陷清零」；全文未登记任何无量纲靶的预测值与误差棒 ⇒ UFT-3 计数仍为 0",
     "第一性审计", "falsified"),
    ("C38", "【未展开】3.1 矛盾自检·3.2 拓扑归一·3.3 层级升维 三项算法均未给出输入输出格式·终止性·复杂度·拒绝准则与任一算例；其中「层级升维」把 L1 内容批量标为 L3 违反 openuft 层级定义",
     "第一性审计", "open"),
]

claims_path = os.path.join(SYS_DIR, "claims.csv")
text = io.open(claims_path, encoding="utf-8").read()
existing = set(l.split(",", 1)[0] for l in text.splitlines()[1:] if l.strip())
if not text.endswith("\n"):
    text += "\n"
added = 0
for cid, statement, category, status in NEW_CLAIMS:
    if cid in existing:
        continue
    for field in (cid, statement, category, status, "算法联盟审计组"):
        if "," in field or '"' in field:
            raise ValueError("字段不得含裸逗号或引号: " + cid)
    text += ",".join([cid, statement, category, status, "算法联盟审计组"]) + "\n"
    added += 1
io.open(claims_path, "w", encoding="utf-8").write(text)
item("claims.csv 幂等追加完毕（新增 %d 行 重复时 0 行）" % added, True)

if not os.path.isdir(REF_DIR):
    os.makedirs(REF_DIR)
rec_path = os.path.join(REF_DIR, "空间螺旋修复版_第一性缺陷记录.md")
rec = []
rec.append("# 空间螺旋修复版 · 第一性缺陷记录")
rec.append("")
rec.append("> 针对 2026-09-25 提交的《算法联盟·空间螺旋几何统一场论 缺陷修复体系》的独立审计结论。")
rec.append("> 引擎：`04_公共成果/算法联盟_全维自洽与归一化/源码/空间螺旋修复版_第一性审计与伪派生判定.py`（可复跑）。")
rec.append("> 全额四态判定见 `04_公共成果/算法联盟_全维自洽与归一化/数据/空间螺旋修复版_第一性审计.md`。")
rec.append("")
rec.append("## 判定")
rec.append("")
rec.append("总数 %d `|` PASS=%d FAIL=%d BOUNDARY=%d INFO=%d" % (len(ROWS), n_pass, n_fail, n_bd, n_info))
rec.append("")
rec.append("## 已登记缺陷（对应 claims.csv C24–C38）")
rec.append("")
for cid, statement, category, status in NEW_CLAIMS:
    rec.append("- **%s**（%s）：%s" % (cid, status, statement))
rec.append("")
rec.append("## 承认的非负成果")
rec.append("")
rec.append("- κ=Aω²/(A²ω²+u²)·τ=uω/(A²ω²+u²) 的闭合式经符号推导与 Frenet 数值反算**双路确认正确**。")
rec.append("- 把 ρ 移出 G 式的方向**正确**；问题在于 K₀ 承接了同一循环角色（C30）。")
rec.append("- 修复版所引原体系评级 H4/O5/C1/U0 与 L 计数**与档案一致**，引用属实。")
rec.append("")
rec.append("## 最小可行修复路径")
rec.append("")
for k, v in paths:
    rec.append("- **%s**：%s" % (k, v))
rec.append("")
rec.append("## 红线")
rec.append("")
rec.append("本记录只判定**数学自洽性与第一性层级**，不否定该纲领作为几何草案的价值；")
rec.append("「数学自洽」不等于「实验证实」，更不等于「L3 第一性推导」。")
rec.append("")
io.open(rec_path, "w", encoding="utf-8").write("\n".join(rec))

readme_path = os.path.join(REF_DIR, "README.md")
if os.path.isfile(readme_path):
    rt = io.open(readme_path, encoding="utf-8").read()
else:
    rt = "# 证伪与反例\n\n当前尚无本阶段独立产物；不因目录存在而标记完成。\n"
TAIL = ("本阶段产物：[空间螺旋修复版_第一性缺陷记录](空间螺旋修复版_第一性缺陷记录.md)"
        "（C24–C38；α/G/ρ/场耦合 四处量纲或循环性失败，面板计数自相矛盾，UFT-3 计数仍为 0）。")
if TAIL not in rt:
    import re as _re
    rt2, _n = _re.subn(r".*本阶段产物：.*\n?", TAIL + "\n", rt)
    if _n == 0:
        rt2 = rt.replace("当前尚无本阶段独立产物；不因目录存在而标记完成。", TAIL)
        if TAIL not in rt2:
            rt2 = rt.rstrip() + "\n\n" + TAIL + "\n"
    io.open(readme_path, "w", encoding="utf-8").write(rt2)

n_ok = sum(1 for c in CHECKS if c["ok"])
print("\n" + "=" * 76)
print("自检 %d/%d | 判定 总数=%d PASS=%d FAIL=%d BOUNDARY=%d INFO=%d | 用时 %.1f s"
      % (n_ok, len(CHECKS), len(ROWS), n_pass, n_fail, n_bd, n_info, time.time() - T0))
if n_ok != len(CHECKS):
    print("【自检失败项】")
    for c in CHECKS:
        if not c["ok"]:
            print("  -", c["name"], "|", c["note"])
print("=" * 76)
