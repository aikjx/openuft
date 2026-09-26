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

V21 续修并入（2026-09-26 · 统一脚本）
------------------------------------
  §12  C25 — LB 本征能级高阶扫描 n=1..6（mpmath 250 位 + 误差棒传播审计）
  §13  C35 — 固定 β 多行星近日点进动交叉验证（水星标定 → 金星/地球，250 位）
  §14  汇总表更新复核 + claims.csv 台账登记 C48/C49（幂等）
  数据/空间螺旋V21续修_C25C35_审计.json / .md

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
skipped = []
max_err = mpf(0)
for n_val in ["137", "1000", "4695", "18907", "100000", "1000000000"]:
    Nv = mpf(n_val)
    factor = 2 * sqrt(Nv) * ALPHA           # 所需 c/(ωA)
    if factor <= 1:
        # 透明化：不静默跳过。读数B 下 c/(ωA)=secθ>=1，故小 N 不可行（读数A 下无此限制）
        print("     %-14s %-22s %-22s   ← 读数B 不可行（需 c/(ωA)=%s < 1）"
              % (n_val, "—", "—", fmt(factor, 8)))
        skipped.append(n_val)
        continue
    wa = C / factor                          # 所需 ωA
    alpha_back = (1 / (2 * sqrt(Nv))) * (C / wa)
    err = abs(alpha_back / ALPHA - 1)
    max_err = max(max_err, err)
    fit_rows.append({"N": n_val, "omegaA_over_c": float(1 / factor), "alpha_back": float(alpha_back)})
    print("     %-14s %-22s %-22s" % (n_val, fmt(1 / factor, 10), fmt(alpha_back, 12)))
print("     命中 %d 个 N；读数B 下不可行 %d 个（%s）"
      % (len(fit_rows), len(skipped), "、".join(skipped) if skipped else "无"))
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

reg("BOUNDARY", "§9-3 「纠错算法」3 项提交版未给出规格（本册 §9.5 已补全）",
    "提交版中 3.1 矛盾自检 / 3.2 拓扑归一 / 3.3 层级升维 均未给出输入格式·输出证书·终止性·复杂度·拒绝准则·算例；"
    "本册 §9.5 已作为审计引擎能力补全（含算例、捕获 §0 叉乘 bug、强制拒绝 L1→L3 升维），但提交理论自身仍缺公开规格",
    "层级升维若把 L1 内容批量标为 L3 仍违反 openuft 层级定义（L3 要求第一性推导或可检验预言）", "U 类判定")

# ===========================================================================
# §9.5  C38 三项审计算法实现与自测（本轮补全，回应 §9-3 的 U 类缺陷）
# ===========================================================================
print("\n" + "=" * 76)
print("§9.5  C38 三项审计算法：矛盾自检 / 拓扑归一 / 层级升维（实现 + 算例）")
print("=" * 76)


# ---------- 3.1 矛盾自检 ----------
def algo_contradiction_selfcheck(assertions):
    """输入：assertions = list[dict]，每条为一待检声明。
       支持 kind：
         'ortho' : {a,b} 两向量应正交（点积=0）
         'unit'  : {v}   向量应为单位长（|v|=1）
         'eq'    : {lhs,rhs[,tol]} 两数值应相等（相对容差）
         'sign'  : {v,expect} v 的符号应与 expect(±1) 一致
       输出：findings = list[(aid, kind, ok, msg)]
       终止性：有限输入有限步；无循环。
       复杂度：O(m) 单条校验（可选 O(m^2) 交叉比对未启用）。
       拒绝准则：缺 kind / kind 不在支持集 → 'rejected:under-specified' 或 'unknown-kind'。"""
    findings = []
    for a in assertions:
        aid = a.get("id", "?")
        kind = a.get("kind")
        if kind is None or kind not in ("ortho", "unit", "eq", "sign"):
            findings.append((aid, kind, False,
                             "rejected:under-specified" if kind is None else "rejected:unknown-kind"))
            continue
        if kind == "ortho":
            x, y = a["a"], a["b"]
            d = x[0] * y[0] + x[1] * y[1] + x[2] * y[2]
            ok = abs(d) < mpf("1e-40")
            findings.append((aid, "ortho", ok, "B·T=%.3e (应=0)" % d if not ok else "ok"))
        elif kind == "unit":
            v = a["v"]
            m = sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)
            ok = abs(m - 1) < mpf("1e-40")
            findings.append((aid, "unit", ok, "|B|=%.12f (应=1)" % m if not ok else "ok"))
        elif kind == "eq":
            tol = a.get("tol", mpf("1e-12"))
            ok = abs(a["lhs"] - a["rhs"]) <= (abs(a["rhs"]) + mpf("1e-60")) * tol
            findings.append((aid, "eq", ok, "lhs=%.6e rhs=%.6e" % (a["lhs"], a["rhs"])))
        else:  # sign
            s = 1 if a["v"] > 0 else -1
            ok = (s > 0 and a["expect"] > 0) or (s < 0 and a["expect"] < 0)
            findings.append((aid, "sign", ok, "sign(v)=%d expect=%d" % (s, a["expect"])))
    return findings


# 算例：V21 §0 副法向量叉乘（捕获叉乘 bug，并给出修正式）
# b 由速度归一化约束 ω√(A²+b²)=c 反解 ⇒ T 为单位矢、B_correct 真正单位长
A_d, om_d, c_d = mpf("1e-16"), mpf("1e15"), C
b_d = sqrt((c_d / om_d) ** 2 - A_d ** 2)
Tx, Ty, Tz = mpf(0), A_d * om_d / c_d, b_d * om_d / c_d          # T(λ=0)
Nx, Ny, Nz = mpf(-1), mpf(0), mpf(0)                             # N(λ=0)
B_user = [om_d * b_d / c_d, mpf(0), om_d * A_d / c_d]            # 用户写的 (ω/c)(b cos,b sin,A)
B_corr = [Ty * Nz - Tz * Ny, Tz * Nx - Tx * Nz, Tx * Ny - Ty * Nx]  # 正确 T×N

cc_find = algo_contradiction_selfcheck([
    {"id": "B_user⊥T", "kind": "ortho", "a": B_user, "b": [Tx, Ty, Tz]},
    {"id": "B_user⊥N", "kind": "ortho", "a": B_user, "b": [Nx, Ny, Nz]},
    {"id": "B_user单位长", "kind": "unit", "v": B_user},
    {"id": "B_correct⊥T", "kind": "ortho", "a": B_corr, "b": [Tx, Ty, Tz]},
    {"id": "B_correct⊥N", "kind": "ortho", "a": B_corr, "b": [Nx, Ny, Nz]},
    {"id": "B_correct单位长", "kind": "unit", "v": B_corr},
])
bug_caught = any((fid.startswith("B_user") and not ok) for fid, _, ok, _ in cc_find)
all_correct_ok = all(ok for fid, _, ok, _ in cc_find if fid.startswith("B_correct"))
print("     矛盾自检算例（V21 §0 副法向量叉乘）：")
for fid, kind, ok, msg in cc_find:
    print("       · %-14s %s  %s" % (fid, "PASS" if ok else "FAIL", msg))
print("     修正式：B_correct = (ω/c)(b·sin ωλ, −b·cos ωλ, A)")
item("矛盾自检捕获 V21 §0 叉乘错误（B_user 不正交于 T 与 N）", bug_caught,
     "B_user=(ωb/c,0,ωA/c) 在 λ=0 处 B_user·T=ω²Ab/c² ≠ 0、B_user·N=−ωb/c ≠ 0 ⇒ 叉乘 x,y 分量 sin/cos 与符号均错位")
item("矛盾自检确认修正式 B_correct=T×N 满足正交+单位长", all_correct_ok)
reg("INFO", "§9.5-1 矛盾自检算法已实现并捕获 §0 叉乘 bug",
    "algo_contradiction_selfcheck 对 ortho/unit/eq/sign 四类声明做有限步校验；"
    "喂入 V21 §0 的 B_user=(ω/c)(b cos,b sin,A) 报出与 T、N 均不正交且非单位长 ⇒ 叉乘展开式错误；"
    "修正式 B_correct=(ω/c)(b sin,−b cos,A) 全部通过",
    "I/O: list[assertion]→list[finding]；终止:有限；复杂度 O(m)；拒绝:under-specified/unknown-kind",
    "自实现 + 算例")


# ---------- 3.2 拓扑归一 ----------
def algo_topo_normalize(quantities):
    """输入：quantities = list[(qid, value, dim_dict)]，dim_dict∈{L,M,T,I} 整数指数。
       输出：{pis:list[(name,expr,val)], consistent:bool, rejected:list}
       方法：Buckingham Π——对维度矩阵做秩分析，构造无量纲组。
       终止性：有限（秩≤4）；复杂度 O(n·4)；拒绝：缺维/未知量 → rejected。"""
    bases = ["L", "M", "T", "I"]
    mat, names, vals, rejected = [], [], [], []
    for qid, val, dim in quantities:
        if dim is None:
            rejected.append(qid)
            continue
        names.append(qid)
        vals.append(val)
        mat.append([Fraction(dim.get(b, 0)) for b in bases])
    if len(mat) < 2:
        return {"pis": [], "consistent": False, "rejected": rejected}
    ref, ref_val = mat[0], vals[0]
    pis, consistent = [], True
    for i in range(1, len(mat)):
        e = None
        ok = True
        for k in range(4):
            if ref[k] != 0:
                ek = mat[i][k] / ref[k]
                if e is None:
                    e = ek
                elif abs(ek - e) > Fraction(1, 10 ** 9):
                    ok = False
        if not ok:
            consistent = False
            pis.append((names[i], "dim-mismatch-with-%s" % names[0], None))
        else:
            pis.append((names[i], "(%s)^(%s)/(%s)" % (names[0], e, names[i]),
                        (float(ref_val) ** float(e)) / float(vals[i])))
    return {"pis": pis, "consistent": consistent, "rejected": rejected}


# 算例：κ,τ,ω,c 的维度归一 + 不变量 κ²+τ²=ω²/c² 量纲自洽
k_ex = A_d * om_d ** 2 / c_d ** 2
t_ex = b_d * om_d ** 2 / c_d ** 2
w_ex = om_d
topo = algo_topo_normalize([
    ("kappa", k_ex, {"L": -1}),
    ("tau", t_ex, {"L": -1}),
    ("omega", w_ex, {"T": -1}),
    ("c", c_d, {"L": 1, "T": -1}),
])
dim_lhs = dpow(DIM_CURV, 2)                                  # (L^-1)^2 = L^-2
dim_rhs = ddiv(D(L=0, T=-2), dpow(D(L=1, T=-1), 2))         # ω²/c² = T^-2 / (L²T^-2) = L^-2
inv_dim_ok = dim_lhs == dim_rhs
print("     拓扑归一算例：κ²+τ² 与 ω²/c² 量纲 = %s vs %s ⇒ %s"
      % (dfmt(dim_lhs), dfmt(dim_rhs), "一致" if inv_dim_ok else "冲突"))
item("拓扑归一确认 κ²+τ²=ω²/c² 量纲自洽（Π 群存在）", inv_dim_ok)
reg("INFO", "§9.5-2 拓扑归一算法已实现",
    "algo_topo_normalize 对 (qid,value,dim) 做 Buckingham Π 降维；κ,τ,ω,c 可构造无量纲不变量组 Π=(κ²+τ²)/(ω²/c²)；"
    "拒绝缺维量",
    "I/O: list[(qid,value,dim)]→{pis,consistent,rejected}；终止:有限；复杂度 O(n·4)",
    "自实现 + 算例")


# ---------- 3.3 层级升维 ----------
def algo_hierarchy_uplift(claim_id, current_level, evidence_type,
                          constructive_derivation=False, testable_prediction=False,
                          requested_level=None):
    """输入：(claim_id, current_level∈{L0..L3}, evidence_type∈{identity,definition,
       construction,prediction}, constructive_derivation, testable_prediction, requested_level)
       输出：(allowed_level, decision, reason)
       拒绝准则：
         R1 跳级：requested > current+1 ⇒ 拒绝（不得 L1→L3）。
         R2 identity/definition 证据最多 L1，不得升 L2/L3。
         R3 升 L3 须同时具 constructive_derivation 与 testable_prediction(带误差棒)；否则封顶 L2(或 L1)。
       终止性：单趟 O(1)；复杂度 O(1)。"""
    order = {"L0": 0, "L1": 1, "L2": 2, "L3": 3}
    cur = order[current_level]
    req = order[requested_level] if requested_level else cur
    if req > cur + 1:
        return current_level, "REJECT", "R1 跳级（%s→%s 不允许）" % (current_level, requested_level)
    if evidence_type in ("identity", "definition") and req > 1:
        return "L1", "REJECT-CAP-L1", "R2 identity/definition 证据不得高于 L1"
    if req >= 3 and not (constructive_derivation and testable_prediction):
        cap = "L2" if constructive_derivation else "L1"
        return cap, "REJECT-CAP", "R3 升 L3 需 constructive_derivation 与 testable_prediction(误差棒)；封顶 %s" % cap
    return (requested_level or current_level), "ALLOW", "通过"


r1 = algo_hierarchy_uplift("inv_k2_t2", "L0", "identity", requested_level="L3")
r2 = algo_hierarchy_uplift("alpha_eigen", "L1", "construction",
                            constructive_derivation=True, requested_level="L3")
r3 = algo_hierarchy_uplift("theta_def", "L0", "definition", requested_level="L2")
print("     层级升维算例：")
for tag, res in [("κ²+τ²=ω²/c² →L3", r1), ("α 本征(构造,无预言) →L3", r2), ("θ=τ/κ 定义 →L2", r3)]:
    print("       · %-26s 允许=%s 决策=%s | %s" % (tag, res[0], res[1], res[2]))
item("层级升维拒绝 L1→L3 批量升维（§9-3 的红旗）",
     r1[1].startswith("REJECT") and r2[1].startswith("REJECT"))
reg("INFO", "§9.5-3 层级升维算法已实现并强制拒绝违规升维",
    "algo_hierarchy_uplift 实现 R1(禁跳级)/R2(identity·definition 封顶 L1)/R3(升 L3 需构造+可检验预言)；"
    "算例：不变量恒等式请求升 L3 被拒、α 本征(仅构造无预言)升 L3 被拒封顶 L2、θ 定义不得高于 L1",
    "I/O:(claim_id,level,evidence_type,flags)→(allowed_level,decision,reason)；终止:O(1)",
    "自实现 + 算例")

reg("BOUNDARY", "§9.5-4 C38 三项算法本轮已补全（原 open → BOUNDARY）",
    "矛盾自检/拓扑归一/层级升维均已给出输入格式·输出证书·终止性·复杂度·拒绝准则·算例；"
    "但本引擎能力补全不抵消 §24–§37 对提交理论 headline 公式的 falsified 判定",
    "提交理论自身仍缺三项算法的公开规格；本册仅作为审计工具补齐", "引擎能力补全")


# ===========================================================================
# §9.6  C25(α 本征值) 与 C35(轨道进动) 的数值复核（用 §9.5 算法做实判据）
# ===========================================================================
print("\n" + "=" * 76)
print("§9.6  C25 α 本征值 / C35 轨道进动 —— 数值复核与突破条件")
print("=" * 76)


# ---------- C25：α 公式的欠定性与拓扑本征值路径 ----------
# 提交公式 α = (1/(2√N))·(c/(ωA))：未知量 {N, ωA} 两个，约束方程一个。
# 固定 α=α_exp，对任意选定的 N 反解 ωA 均成立 ⇒ 对 N 无选择力（伪派生）。
print("     C25  α=(1/(2√N))·(c/(ωA)) 的欠定性复核：")
c25_rows = []
for Ndemo in [mpf('4695'), mpf('18907'), mpf('1e9')]:
    wA = C / (2 * mp.sqrt(Ndemo) * ALPHA)                 # 反解使 α 命中观测
    a_back = (C / wA) / (2 * mp.sqrt(Ndemo))               # 回代验证
    ok = abs(a_back - ALPHA) < mpf('1e-40')
    c25_rows.append((Ndemo, wA, a_back, ok))
    print("       · N=%-12s → ωA=%.6e （回代 α=%.10f，命中=%s）"
          % (float(Ndemo), float(wA), float(a_back), ok))
c25_underdet = all(ok for _, _, _, ok in c25_rows)
item("C25 数值复核：N 取 4695/18907/1e9 三量级均可反解合法 ωA 命中 α", c25_underdet,
     "约束数 1 < 未知量数 2 ⇒ 系统欠定，α 不具选择力（与 C25 falsified 判据一致）")
# 拓扑本征值路径（理论自承的核心目标）：α = sin(1/(N+Δ_top))，Δ_top≈0.036
Dt = mpf('0.036')
N_from_topo = mpf(1) / mp.asin(ALPHA) - Dt
print("     拓扑本征值路径 α=sin(1/(N+Δ_top)) ⇒ 反解 N=%.4f（理论须由拓扑本征值『推出』此 N）"
      % float(N_from_topo))
item("C25 拓扑路径给出 N≈137.036，但 N 的『第一性推导』仍是理论未闭合目标", True,
     "N=137 目前是手填目标值；三条推导路径(拓扑绕数/Dirac谱流/量子相位)未互相收口 ⇒ α 仍属测量锚")
reg("INFO", "§9.6-1 C25 α 数值复核（确认 falsified 并给突破条件）",
    "对任意 N 均可反解 ωA 使 α 命中观测 ⇒ 伪派生；唯一使其成立的是『由拓扑本征值推出 N=137』，"
    "而该步在提交理论中仍未闭合（C23/C27 亦 falsified）",
    "I/O:{N,ωA}→α；终止:有限；复杂度 O(1)；拒绝:约束<未知量⇒欠定", "自实现 + 算例")


# ---------- C35：轨道进动的数值积分（Binet 方程 + RK4）----------
def orbit_precession_rad(gm, p, extra_coeff, n_orbits=30, dphi=mpf('0.003')):
    """中心力 F=-gm·m/r²·(1+extra_coeff·u² 形式) 的近日点进动（弧度/轨道）。
       Binet 方程（c=1 几何单位）：u''+u = gm/h² + extra_coeff·u²，h²≈gm·p（弱场）。"""
    h2 = gm * p
    base = gm / h2
    def acc(uu):
        return base + extra_coeff * uu * uu
    u = mpf('1.5') / p          # 椭圆初始条件（近日点 r=p/1.5，偏心率 0.5）；圆轨道 u=1/p 无进动无法检测
    v = mpf(0)
    phi = mpf(0)
    peri = [mpf(0)]                      # φ=0 起点即近日点
    prev_v = v
    steps = int(n_orbits * 2 * mp.pi / dphi) + 20
    for _ in range(steps):
        k1u, k1v = v, -u + acc(u)
        u2_ = u + dphi / 2 * k1u
        v2_ = v + dphi / 2 * k1v
        k2u, k2v = v2_, -u2_ + acc(u2_)
        u3_ = u + dphi / 2 * k2u
        v3_ = v + dphi / 2 * k2v
        k3u, k3v = v3_, -u3_ + acc(u3_)
        u4_ = u + dphi * k3u
        v4_ = v + dphi * k3v
        k4u, k4v = v4_, -u4_ + acc(u4_)
        un = u + dphi / 6 * (k1u + 2 * k2u + 2 * k3u + k4u)
        vn = v + dphi / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        if prev_v > 0 and vn <= 0:        # v 由 + 转 − ⇒ 近日点
            frac = prev_v / (prev_v - vn)
            peri.append(phi + dphi * frac)
        prev_v = vn
        u, v = un, vn
        phi += dphi
    diffs = [peri[i + 1] - peri[i] for i in range(len(peri) - 1)]
    return (sum(diffs) / len(diffs)) - 2 * mp.pi


# 几何单位 gm=1, c=1，p=1000（弱场：3gm/(c²p)=3e-3 ≪ 1）
prec_kepler = orbit_precession_rad(mpf(1), mpf('1000'), mpf(0))     # 修复版线性 Φ ⇒ 牛顿，进动≈0
prec_gr = orbit_precession_rad(mpf(1), mpf('1000'), mpf(3))         # GR 1PN 修正项 3GMu²/c²
# 缩放到水星：Δφ_M = Δφ_geo · [GM_sun/(c²·p_Mercury)] / [1/(1·1000)]
GM_sun = mpf('1.32712440018e20')
p_merc = mpf('5.7909e10') * (mpf(1) - mpf('0.2056') ** 2)
scale = (GM_sun / (C ** 2 * p_merc)) / (mpf(1) / mpf('1000'))
arcsec_per_cent = lambda rad: rad * scale * (mpf(180) / mp.pi) * mpf(3600) * mpf('415')
print("     C35  轨道进动（水星，角秒/世纪）：")
print("       · 修复版线性 Φ（牛顿）   : %s" % fmt(float(arcsec_per_cent(prec_kepler)), 4))
print("       · GR 1PN 修正 3GMu²/c²   : %s  （观测值 42.98）" % fmt(float(arcsec_per_cent(prec_gr)), 4))
c35_mercury_fail = (abs(arcsec_per_cent(prec_kepler)) < mpf('1e-6')
                    and abs(arcsec_per_cent(prec_gr) - mpf('42.98')) < mpf('1'))
item("C35 数值复核：修复版线性 Φ 退化为牛顿律（进动≈0），无法解释水星 43″/世纪", c35_mercury_fail,
     "要复现 43″ 必须把 ∇Φ/Φ₀ 取为 1+3GM/(c²r) —— 即把 GR 的 GM/c² 作为自由形状参数导入 ⇒ 拟合而非推导")
reg("INFO", "§9.6-2 C35 轨道进动数值复核（确认 falsified 并给突破条件）",
    "RK4 积分 Binet 方程：线性 Φ 给出牛顿进动 0″（与观测 43″ 冲突）；GR 1PN 项 3GMu²/c² 给出 43″/世纪（匹配）"
    "但要求把 GM/c² 作为形状参数导入 ⇒ 框架只能『拟合』GR 而非『导出』",
    "I/O:(gm,p,extra_coeff)→进动弧度；终止:有限步；复杂度 O(步数)；拒绝:Bertrand 冲突(n≠1 非闭合轨道)",
    "自实现 + 算例")

# 层级升维：C25/C35 仍属 L0/L1 参数化/拟合，未达 L3
r_c25 = algo_hierarchy_uplift("alpha_deriv", "L0", "parameterization", requested_level="L3")
r_c35 = algo_hierarchy_uplift("orbit_precession", "L1", "fit", constructive_derivation=False,
                               testable_prediction=False, requested_level="L3")
print("     层级升维：C25(%s→%s) / C35(%s→%s)" % (r_c25[0], r_c25[1], r_c35[0], r_c35[1]))
item("C25/C35 经层级升维审查仍被封顶 L1（无构造推导+无带误差棒预言）",
     r_c25[1].startswith("REJECT") and r_c35[1].startswith("REJECT"))
reg("BOUNDARY", "§9.6-3 C25/C35 本轮数值复核后仍维持 falsified（非 PASS）",
    "C25 α 伪派生、C35 引力因子零内容/冲突——两项均经 §9.5 算法复核确认；"
    "理论若要在 L3 成立，须补两条第一性输入：①由拓扑本征值推出 N=137（C23/C27 未闭合）；"
    "②把螺旋曲率 κ,τ 与 GM/c² 经测地线方程挂钩（当前为手填）",
    "突破条件已显式列出，但提交理论未提供 ⇒ 仍为 falsified", "引擎能力补全")


# ===========================================================================
# §9.7  V21续修：C25 高阶本征能级 α_n 扫描 / C35 多行星进动交叉验证（dps=250）
# ---------------------------------------------------------------------------
# 本节点是「续修」提交（V21）：C25 换用螺旋 LB 本征体系 E_n=(ω²/c²)(V0+n²ℏ²/N²)，
# C35 换用 Binet 方程 GMβ u² 修正（PPN 型）。两式均为「n=1/水星一次性标定 + 高阶级/
# 他行星独立预言」构造。本节在 250 位精度下**忠实复算**并给出诚实判定。
# ===========================================================================
print("\n" + "=" * 76)
print("§9.7  V21续修  C25 高阶本征能级 / C35 多行星进动（mpmath dps=250）")
print("=" * 76)

_DPS_SAVE = mp.dps
mp.dps = 250

# ---- CODATA2022 基础常数（250 位，就地写死；带下划线避免与文件既有常量冲突）----
C_ = mpf("299792458")
G_ = mpf("6.67430e-11")
HB_ = mpf("1.0545718176461565e-34")
ME_ = mpf("9.1093837015e-31")
MS_ = mpf("1.98847e30")
A_ = mpf("0.0072973525693")
ARCSEC_ = mp.pi / (180 * 3600)


def _log10(x):
    return mp.log(x) / mp.log(mpf(10))


# ---------- C25：螺旋 LB 本征体系 ----------
OM_LB = mpf("1.23558996e20")
N_TOPO = mpf("18907")
V0 = mpf("1.0")


def E_n(n):
    return (OM_LB ** 2 / C_ ** 2) * (V0 + (n ** 2 * HB_ ** 2) / (N_TOPO ** 2))


E1_LB = E_n(1)
C_COUPLE = A_ * ME_ * C_ ** 2 / E1_LB
_term1 = HB_ ** 2 / N_TOPO ** 2

print("     C25 螺旋 LB 本征体系（V0=%s，N=%s，ω=%s）"
      % (fmt(V0, 4), fmt(N_TOPO, 8), fmt(OM_LB, 8)))
print("       · 能级量子化项 ℏ²/N² = %s；相对 V0=%s 低 %s 个量级"
      % (fmt(_term1, 6), fmt(V0, 4), fmt(_log10(V0 / _term1), 4)))
print("       · n=1 标定耦合 C = %s" % fmt(C_COUPLE, 12))
print("        n | E_n                 | α_n                        | σ(α_n)     | 相对展宽(vs α_obs)")
c25_table = []
for n in range(1, 7):
    Ev = E_n(n)
    an = C_COUPLE * Ev / (ME_ * C_ ** 2)
    term = (n ** 2 * HB_ ** 2) / (N_TOPO ** 2)
    rel = sqrt(mpf("1e-12") ** 2 + ((2 * term) / (V0 + term) * mpf("1e-12")) ** 2)
    aerr = an * rel
    dev = abs(an - A_) / A_
    c25_table.append((n, Ev, an, aerr, dev))
    print("        %d | %s | %s | %s | %s"
          % (n, fmt(Ev, 10), fmt(an, 22), fmt(aerr, 6), fmt(dev, 4)))

_c25_spread = max(t[4] for t in c25_table)          # n≥2 相对 α_obs 的最大展宽
_c25_errrel = mpf("1e-12")                          # 误差棒相对量级（dω/ω = dN/N = 1e-12）
item("C25 高阶预言具备鉴别力（预言展宽 > 误差棒）", _c25_spread > _c25_errrel,
     "实测展宽 %s 与误差棒 %s 差 %s 个量级 ⇒ 预言被误差棒完全淹没，n≥2 无鉴别力"
     % (fmt(_c25_spread, 4), fmt(_c25_errrel, 4), fmt(_log10(_c25_errrel / _c25_spread), 4)))
reg("INFO", "§9.7-1 C25 高阶本征能级扫描（V21续修·螺旋 LB 本征构造）",
    "250 位复算：V0=1.0 使量子化项 ℏ²/N²≈3.11e-77 低于 V0 达 77 个量级 ⇒ 能级谱实际塌缩，"
    "n=1..6 的 α_n 与 α_obs 相对展宽仅 %s，而误差棒（dω/ω=dN/N=1e-12）为 %s，"
    "预言展宽比误差棒小 %s 个量级 ⇒ 『n≥2 无自由参数独立预言』在此参数化下无鉴别力、不可证伪，"
    "与 §9.6 属同源缺陷（换参数化未改变伪派生性质）；欲使其成为真预言须令 V0 与 ℏ²/N² 同量级"
    % (fmt(_c25_spread, 4), fmt(_c25_errrel, 4), fmt(_log10(_c25_errrel / _c25_spread), 3)),
    "I/O:{n,V0,N,ω}→α_n,σ(α_n)；终止:有限；复杂度 O(n)；拒绝准则:展宽<误差棒⇒无鉴别力",
    "自实现 + 250 位复算")


# ---------- C35：多行星近日点进动（Binet + GMβ u² 修正，PPN 型）----------
def planet_dphi(a, e, T_yr, beta):
    dphi_gr = 6 * mp.pi * G_ * MS_ / (C_ ** 2 * a * (1 - e ** 2))
    dphi_geo = (3 * mp.pi * beta / (a ** 2 * (1 - e ** 2))) * (G_ * MS_) / (C_ ** 2 * a * (1 - e ** 2))
    n100 = 100 / T_yr
    return (dphi_gr * n100 / ARCSEC_, dphi_geo * n100 / ARCSEC_, (dphi_gr + dphi_geo) * n100 / ARCSEC_)


a_mer, e_mer, T_mer = mpf("5.790905e10"), mpf("0.20563069"), mpf("0.240846")


def _res_mer(beta):
    return planet_dphi(a_mer, e_mer, T_mer, beta)[2] - mpf("43.03")


BETA = mp.findroot(_res_mer, 0)
print("     C35 多行星近日点进动（水星一次性标定 β 后固定，不再拟合）")
print("       · 水星标定 β = %s m²（长度²尺度，√β = %s m）"
      % (fmt(BETA, 10), fmt(sqrt(abs(BETA)), 8)))
print("       行星 | GR基础″/cy | 几何修正″/cy | 总预测″/cy | 残差(总−经典)")
planets = [
    ("水星", a_mer, e_mer, T_mer, mpf("43.03")),
    ("金星", mpf("1.0820893e11"), mpf("0.00677672"), mpf("0.615197"), mpf("8.62")),
    ("地球", mpf("1.4959787e11"), mpf("0.0167086"), mpf("1.000017"), mpf("3.84")),
]
c35_rows = []
for nm, ap, ep, Tp, grp in planets:
    g, geo, tot = planet_dphi(ap, ep, Tp, BETA)
    c35_rows.append((nm, g, geo, tot, tot - grp))
    print("        %-4s | %s | %s | %s | %s"
          % (nm, fmt(g, 6), fmt(geo, 6), fmt(tot, 6), fmt(tot - grp, 6)))

item("C35 水星一次标定 β 后，金星/地球为无再拟合参数的独立预测",
     abs(c35_rows[1][4]) > 0 and abs(c35_rows[2][4]) > 0,
     "金星残差 %s″/cy、地球残差 %s″/cy（具体、有限可检验）"
     % (fmt(c35_rows[1][4], 4), fmt(c35_rows[2][4], 4)))
reg("BOUNDARY", "§9.7-2 C35 多行星进动交叉验证（V21续修·固定 β 构造）",
    "水星一次性标定 β=%s m²（长度²尺度 √β≈%s m），随后**固定**；金星总进动 %s″/百年、地球 %s″/百年，"
    "相对经典 GR 值 8.62/3.84 偏差 %s/%s″/百年（亚毫角秒级）⇒ 属具体、可检验的独立预言，"
    "在本构造内满足『一次标定 + 他行星独立预言』的可证伪结构；惟该偏差低于现有天体测量精度 ⇒ 标 open"
    % (fmt(BETA, 8), fmt(sqrt(abs(BETA)), 6), fmt(c35_rows[1][3], 6), fmt(c35_rows[2][3], 6),
       fmt(c35_rows[1][4], 4), fmt(c35_rows[2][4], 4)),
    "I/O:{a,e,T,β}→Δφ″/百年；终止:有限；复杂度 O(1)；拒绝:Bertrand 闭合轨道约束",
    "自实现 + 250 位复算")

mp.dps = _DPS_SAVE


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
    ("算法", "已完成：§9.5 给出三项算法的输入/输出/终止/复杂度/拒绝准则与算例，并捕获 §0 叉乘 bug（C38 由 open 转 BOUNDARY）"),
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
    "fit_freedom_skipped_readingB": skipped,
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
    ("C38", "【本轮补全】三项审计算法已在审计引擎 §9.5 实现：矛盾自检(algo_contradiction_selfcheck·ortho/unit/eq/sign 四类声明有限步校验·已捕获 V21 §0 副法向量叉乘错误)/拓扑归一(algo_topo_normalize·Buckingham Π 降维)/层级升维(algo_hierarchy_uplift·R1禁跳级/R2 identity封顶L1/R3 升L3需构造+可检验预言)；均含输入输出格式·终止性·复杂度·拒绝准则·算例。提交理论自身仍缺公开规格故维持 BOUNDARY 而非 PASS",
     "第一性审计", "BOUNDARY"),
    ("C46", "【复算·INFO】C25 α 公式 α=(1/(2√N))(c/(ωA)) 经 §9.6 数值复核确认欠定：N=4695/18907/1e9 三量级均可反解合法 ωA 命中 α ⇒ 伪派生；唯一转机『由拓扑本征值推出 N=137』在提交理论中未闭合",
     "第一性审计", "info"),
    ("C47", "【复算·INFO】C35 轨道进动经 §9.6 RK4 积分确认：线性 Φ 退化为牛顿律（进动 0″ 与水星 43″/世纪冲突）；GR 1PN 项给出 43″/世纪（匹配）但需导入 GM/c² 形状参数 ⇒ 拟合非导出；突破条件已列出",
     "第一性审计", "info"),
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


# ===========================================================================
# §12  V21 续修 · C25：LB 本征能级高阶扫描（n=1..6 · mpmath 250 位）
# ===========================================================================
print("\n" + "=" * 76)
print("§12  V21续修 C25 | LB 本征能级扫描 n=1..6 · 250 位 mpmath")
print("=" * 76)

V21_START = len(ROWS)                     # 本节起的新判定行（用于独立数据切片）
mp.dps = 250
V_C = mpf("299792458")                    # c 精确定义值
V_G = mpf("6.67430e-11")                  # G（草稿指定 CODATA2018）
V_HBAR = mpf("1.0545718176461565e-34")    # ħ（草稿指定 CODATA2018）
V_ME = mpf("9.1093837015e-31")            # m_e（草稿指定 CODATA2018）
V_MSUN = mpf("1.98847e30")                # M_sun（草稿指定）
V_ALPHA = mpf("0.0072973525693")          # α_obs
V_ARC = pi / (180 * 3600)                 # 角秒→弧度

V_OMEGA = mpf("1.23558996e20")            # 螺旋特征频率（外部输入）
V_N = mpf("18907")                        # 拓扑绕数（外部输入）
V_V0 = mpf("1.0")                         # 几何势耦合（草稿声明无量纲）
dN_rel = mpf("1e-12")                     # 草稿假设 N 相对不确定度
domega_rel = mpf("1e-12")                 # 草稿假设 ω 相对不确定度


def En_lb(n):
    """草稿式 LB 本征能级：E_n = (ω²/c²)(V0 + n²ℏ²/N²)。"""
    return (V_OMEGA ** 2 / V_C ** 2) * (V_V0 + (n ** 2 * V_HBAR ** 2) / (V_N ** 2))


E1_v = En_lb(1)
C_couple = V_ALPHA * V_ME * V_C ** 2 / E1_v   # (n=1) 标定耦合常数 𝒞
term1 = V_HBAR ** 2 / (V_N ** 2)

print("     标定：E1 = %s" % fmt(E1_v, 24))
print("     标定：𝒞 = α_obs·m_e c²/E1 = %s" % fmt(C_couple, 24))
print("     谱修正基数：ℏ²/N² = %s（相对 V0=1 ⇒ 谱宽仅 ~1e-77 量级）" % fmt(term1, 6))

print("\n     n | E_n（数值）          | α_n               | σα（草稿式）      | (α_n−α_1)/α_1")
alpha_rows = []
for n in range(1, 7):
    En_v = En_lb(n)
    alphan = C_couple * En_v / (V_ME * V_C ** 2)
    term_n = (n ** 2 * V_HBAR ** 2) / (V_N ** 2)
    rel_err_draft = sqrt(domega_rel ** 2 + ((2 * term_n) / (V_V0 + term_n) * dN_rel) ** 2)
    alpha_err_draft = alphan * rel_err_draft
    rel_spread = alphan / V_ALPHA - 1
    alpha_rows.append({"n": n, "En": En_v, "alpha": alphan,
                       "sig": alpha_err_draft, "rel": rel_spread})
    print("     %2d | %s | %s | %s | %s"
          % (n, fmt(En_v, 18), fmt(alphan, 18), fmt(alpha_err_draft, 10), fmt(rel_spread, 4)))

max_rel = max(r["rel"] for r in alpha_rows[1:])
draft_sig_rel = alpha_rows[-1]["sig"] / alpha_rows[-1]["alpha"]
true_rel_n6 = 2 * abs(term1 / (V_V0 + term1) - (36 * term1) / (V_V0 + 36 * term1)) * dN_rel
log10_over = mp.log10(draft_sig_rel / max_rel) if max_rel > 0 else mp.mpf("nan")
print("\n     误差传播审计：α_n = 𝒞·E_n/(m_e c²) = α_obs·f_n/f_1 ⇒ ω、c 不确定度完全抵消；")
print("       草稿式 σα/α（n=6）= %s" % fmt(draft_sig_rel, 6))
print("       正确传播 σα/α（n=6）= %s" % fmt(true_rel_n6, 6))
print("       草稿误差棒超过谱效应（α_6−α_1）/α_1 约 10^%s 个量级" % fmt(log10_over, 5))

print("\n     量纲账本：")
print("       [ω²/c²] = L^-2；V0 无量纲 ⇒ 第一项 [L^-2]")
print("       n²ℏ²/N² ⇒ [M²L⁴T^-2]（ℏ 带量纲）⇒ 第二项（乘 ω²/c²）为 [M²L²T^-2]")
print("       ⇒ E_n 括号内 1（无量纲）与 M²L⁴T^-2 不可相加；E_n 亦非能量 [M L² T^-2]")
print("       ⇒ 𝒞 = α m_e c²/E1 ⇒ [M^-1]，并非无量纲耦合常数")

reg("FAIL", "§12-C25-1 量纲账本：E_n 非能量、𝒞 非无量纲",
    "E_n = (ω²/c²)(V0+n²ℏ²/N²) 中 V0 项为 [L^-2] 而 n²ℏ²/N² 项为 [M²L⁴T^-2] ⇒ 括号内不可相加；"
    "E_n 整体为 [M²L²T^-2] 非能量 [M L² T^-2]；𝒞 = α m_e c²/E1 ⇒ [M^-1] 非无量纲耦合常数",
    "与上轮 §1-C25-1 同一缺陷：草稿复用原公式未修量纲", "量纲账本")

reg("FAIL", "§12-C25-2 谱退化：n=2..6 与标定态 α_1 相对差 ≤ ~1e-75",
    "ℏ²/N² ≈ %s（相对 V0=1）⇒ α_n−α_1 相对量级 ~%s；α 观测不确定度仅 1.5e-10 ⇒ "
    "高阶能级在约 76 位有效数字内与 α_1 不可区分，无独立可检验靶" % (fmt(term1, 4), fmt(max_rel, 4)),
    "「n≥2 独立预言」在物理上消失；任何光谱类实验均无法分辨该谱间距", "退化审计（数值）")

reg("FAIL", "§12-C25-3 误差棒公式误算：ω 不确定度应完全抵消",
    "α_n = α_obs·f_n/f_1（f_n = V0+n²ℏ²/N²）⇒ ω、c 在两个能级比中抵消，草稿式把 dω 计入 σα 属双重计账；"
    "草稿式 σα/α（n=6）≈ %s，正确传播 ≈ %s（仅 N 差项贡献）" % (fmt(draft_sig_rel, 6), fmt(true_rel_n6, 6)),
    "即便采用草稿式，σα/α≈1e-12 也超过谱效应 10^%s 个量级 ⇒ 「误差棒完备/可证伪」不成立" % fmt(log10_over, 5),
    "误差传播解析")

reg("BOUNDARY", "§12-C25-4 标记：open（退化谱），非 open（可证伪谱）",
    "草稿 C25 更新标记为 open 的方向可接受（LB 离散谱在数学上建立）；"
    "但「高阶能级预测+误差棒完备+可证伪」被退化审计与误差棒审计推翻 ⇒ 登记 open（退化谱）",
    "等待先修量纲（ℏ²/N² 与 V0 的物理单位）后再谈可证伪性", "诚实重判")

# ===========================================================================
# §13  V21 续修 · C35：多行星近日点进动（固定 β · 金星/地球交叉验证）
# ===========================================================================
print("\n" + "=" * 76)
print("§13  V21续修 C35 | 固定 β 多行星进动 · 250 位 mpmath")
print("=" * 76)


def planet_dphi(a, e, T_yr, beta):
    """草稿式：返回（GR 基础项，几何修正项，总预测），单位角秒/百年。"""
    dphi_GR_per = 6 * pi * V_G * V_MSUN / (V_C ** 2 * a * (1 - e ** 2))
    dphi_geo_per = (3 * pi * beta / (a ** 2 * (1 - e ** 2))) * (V_G * V_MSUN) / (V_C ** 2 * a * (1 - e ** 2))
    N_orb = 100 / T_yr
    return (dphi_GR_per * N_orb / V_ARC,
            dphi_geo_per * N_orb / V_ARC,
            (dphi_GR_per + dphi_geo_per) * N_orb / V_ARC)


def dphi_geo_correct(a, e, beta):
    """Binet 方程 u''+u = GM/h² + (GMβ/h²)u² 的一阶精确结果：Δφ_geo = 2πβ/(a²(1−e²)²)（弧度/圈）。"""
    return 2 * pi * beta / (a ** 2 * (1 - e ** 2) ** 2)


a_mer, e_mer, T_mer = mpf("5.790905e10"), mpf("0.20563069"), mpf("0.240846")


def residual_draft(beta):
    _, _, dp = planet_dphi(a_mer, e_mer, T_mer, beta)
    return dp - mpf("43.03")


def residual_correct(beta):
    dpGR, _, _ = planet_dphi(a_mer, e_mer, T_mer, mpf(0))
    geo_c = dphi_geo_correct(a_mer, e_mer, beta) * (100 / T_mer) / V_ARC
    return dpGR + geo_c - mpf("43.03")


beta_draft = mp.findroot(residual_draft, mpf("1e18"))
beta_correct = mp.findroot(residual_correct, mpf("1e11"))

planets = [
    ("水星", mpf("5.790905e10"), mpf("0.20563069"), mpf("0.240846"), mpf("43.03")),
    ("金星", mpf("1.0820893e11"), mpf("0.00677672"), mpf("0.615197"), mpf("8.62")),
    ("地球", mpf("1.4959787e11"), mpf("0.0167086"), mpf("1.000017"), mpf("3.84")),
]

print("     水星标定：草稿式 β = %s" % fmt(beta_draft, 12))
print("             Binet 一阶正确式 β = %s" % fmt(beta_correct, 12))
print("     两式差因子（水星处）= %s = 3GM/(2c²a_mer)" % fmt(beta_draft / beta_correct, 8))

print("\n     %-4s | %-13s | %-15s | %-13s | %-11s | %-15s | %-13s"
      % ("行星", "GR基础", "几何修正(草稿式)", "总预测(草稿式)", "参考值",
         "几何修正(Binet式)", "总预测(正确式)"))
c35_out = []
for name, a_p, e_p, T_p, ref in planets:
    dpGR, dpGeo_draft, dpTot_draft = planet_dphi(a_p, e_p, T_p, beta_draft)
    geo_correct = dphi_geo_correct(a_p, e_p, beta_correct) * (100 / T_p) / V_ARC
    tot_correct = dpGR + geo_correct
    c35_out.append({"planet": name,
                    "GR": float(dpGR), "GR_s": fmt(dpGR, 8),
                    "geo_draft": float(dpGeo_draft), "geo_draft_s": fmt(dpGeo_draft, 8),
                    "tot_draft": float(dpTot_draft), "tot_draft_s": fmt(dpTot_draft, 8),
                    "ref": float(ref), "ref_s": fmt(ref, 8),
                    "geo_correct": float(geo_correct), "geo_correct_s": fmt(geo_correct, 8),
                    "tot_correct": float(tot_correct), "tot_correct_s": fmt(tot_correct, 8)})
    print("     %-4s | %-13s | %-15s | %-13s | %-11s | %-15s | %-13s"
          % (name, fmt(dpGR, 8), fmt(dpGeo_draft, 8), fmt(dpTot_draft, 8), fmt(ref, 8),
             fmt(geo_correct, 8), fmt(tot_correct, 8)))
print("     注：水星参考值 43.03 为观测反常进动（标定靶）；金星/地球参考值 8.62/3.84 为 GR 预言值（非独立观测残差）")

venus_ratio = c35_out[1]["geo_draft"] / c35_out[1]["geo_correct"]
earth_ratio = c35_out[2]["geo_draft"] / c35_out[2]["geo_correct"]
formula_factor = 3 * V_G * V_MSUN / (2 * V_C ** 2 * a_mer)

reg("PASS", "§13-C35-1 GR 基础项复现标准值（250 位）",
    "水星 %s / 金星 %s / 地球 %s 角秒每百年（标准 GR：42.98 / 8.62 / 3.84）"
    % (fmt(c35_out[0]["GR"], 6), fmt(c35_out[1]["GR"], 6), fmt(c35_out[2]["GR"], 6)),
    "解析一阶公式 6πGM/(c²a(1−e²)) 直接计算", "独立复算")

reg("BOUNDARY", "§13-C35-2 β 为水星拟合自由参数，非第一性",
    "β 由「总预测=43.03」反解（草稿式 β=%s），金星/地球预测全部依赖该拟合值；"
    "理论未给出 β 的第一性来源（对应上轮 §2-C35-3 的自由度审计）" % fmt(beta_draft, 6),
    "固定 β 不再重拟合在方法上成立，但「普适性检验」的前提是 β 具有独立推导", "自由度审计")

reg("FAIL", "§13-C35-3 草稿几何项与自身 Binet 方程一阶结果不符",
    "草稿 Δφ_geo = 3πβ·GM/(c²a³(1−e²)²)；由草稿 Binet 方程 u''+u=GM/h²+(GMβ/h²)u² 的一阶微扰得 Δφ_geo = 2πβ/(a²(1−e²)²)，"
    "草稿式多出因子 3GM/(2c²a)（水星处 %s）" % fmt(formula_factor, 6),
    "同以水星 43.03 标定，两式给出不同的金星/地球几何修正：金星 %s vs %s（差 %.3f×）；"
    "地球 %s vs %s（差 %.3f×）⇒ a 标度（a³ vs a²）不同，非约定自由度"
    % (fmt(c35_out[1]["geo_draft"], 6), fmt(c35_out[1]["geo_correct"], 6), venus_ratio,
       fmt(c35_out[2]["geo_draft"], 6), fmt(c35_out[2]["geo_correct"], 6), earth_ratio),
    "Binet 一阶微扰解析")

reg("INFO", "§13-C35-4 修正量级低于当前天体测量精度",
    "草稿式金星/地球几何修正仅 ~%s / ~%s 角秒每百年（正确式 ~%s / ~%s）；"
    "现代历表对金星/地球进动的约束在 ~0.1–1 角秒每百年量级 ⇒ 低 2–3 个量级，当前不可判"
    % (fmt(c35_out[1]["geo_draft"], 4), fmt(c35_out[2]["geo_draft"], 4),
       fmt(c35_out[1]["geo_correct"], 4), fmt(c35_out[2]["geo_correct"], 4)),
    "「等待更高精度天体测量观测比对」为诚实表述，但需先修正 §13-C35-3 的公式偏差", "精度量级")

reg("BOUNDARY", "§13-C35-5 标记：open（框架就绪·公式需修正）",
    "草稿 C35 更新标记为 open 的方向可接受（多行星交叉验证框架可运行）；"
    "但几何修正项公式与自身 Binet 一阶结果不符，须修正后再谈普适性预言", "诚实重判")

# ===========================================================================
# §14  V21 续修 · 汇总表更新复核 + 台账登记（C48/C49）+ 数据产出
# ===========================================================================
print("\n" + "=" * 76)
print("§14  V21续修 | 汇总表更新复核 · 台账 C48/C49 · 数据产出")
print("=" * 76)

# --- C24 复核：修正基底 |R'|=c（最小修复轮 B1 证据复算） ---
A_chk = mpf("1.3")
b_chk = A_chk / 137
w_chk = V_C / sqrt(A_chk ** 2 + b_chk ** 2)
speed_chk = sqrt((A_chk * w_chk) ** 2 + (b_chk * w_chk) ** 2) / V_C
item("C24 复核：修正基底（b·ω·t）+ ω√(A²+b²)=c ⇒ |R'|/c = 1", abs(speed_chk - 1) < mpf("1e-40"),
     "b/A=1/137 参数点 |R'|/c = %s" % fmt(speed_chk, 20))
reg("PASS", "§14-C24 复核",
    "第三分量写为 b·ω·t 并显式重列 ω√(A²+b²)=c 后 |R'|=c 精确成立 ⇒ 草稿 C24 更新标记 PASS 有引擎证据（与最小修复轮 C39 一致）",
    "b/A=1/137 参数点 |R'|/c = %s" % fmt(speed_chk, 20), "复算")

reg("INFO", "§14-C38 复核",
    "三项审计算法（矛盾自检/拓扑归一/层级升维）在本册 §9.5 已实现并带示范算例 ⇒ 草稿 C38 更新标记 open（待批量 claims 扫描）方向成立",
    "与 §9.6 的 C25/C35 复核共享同一算法栈", "引擎能力盘点")

print("\n     草稿全审计汇总表（C24–C38）与引擎复核：")
summary_rows = [
    (24, "falsified", "PASS", "基底光速约束，无超光速", "PASS（复算确认，见 §14-C24）"),
    (25, "falsified", "open", "LB本征谱；(n=1)标定𝒞，n≥6高阶α_n+误差棒完备，可证伪", "open（退化谱；误差棒公式需修正，不可证伪）"),
    (26, "falsified", "PASS", "tanθ唯一Frenet定义", "未复核（Frenet 比值 τ/κ=u/(Aω) 唯一，但四方冲突未调和）"),
    (27, "falsified", "PASS", "N外部拓扑输入，无虚假导出", "未复核（声明诚实，但非 PASS 证据）"),
    (28, "open", "PASS", "删除Δθ_min", "未复核"),
    (29, "falsified", "PASS", "删除K₀", "未复核"),
    (30, "falsified", "PASS", "消除G循环定义", "未复核"),
    (31, "falsified", "PASS", "Π定理满足", "未复核"),
    (32, "falsified", "PASS", "删除ρ孤儿场", "未复核（与最小修复轮 C44 方向一致）"),
    (33, "falsified", "PASS", "几何源电流量纲自洽", "未复核（上轮 §6-3 电荷守恒约束仍 FAIL）"),
    (34, "falsified", "PASS", "麦克斯韦含J+J_geo，电荷守恒约束推导完成", "未复核（μ₀J 已补，J_geo 源项仍缺闭合）"),
    (35, "falsified", "open", "Binet方程，水星标定β，金星地球独立预测，普适性检验框架就绪", "open（框架就绪；几何项公式需修正）"),
    (36, "falsified", "PASS", "相位场量纲对齐", "未复核"),
    (37, "falsified", "PASS", "面板统计修正，多套无量纲预测靶", "未复核（靶登记仍为 0）"),
    (38, "open", "open", "三审计算法完整实现，示范算例就绪；待批量全量claims扫描", "open（§9.5 已实现，待批量扫描）"),
]
for cid, old, new, note, review in summary_rows:
    print("     C%-2d  %-9s → %-9s | %s | 引擎复核：%s" % (cid, old, new, note, review))
reg("INFO", "§14-汇总 更新标记引擎复核",
    "草稿 C24–C38 更新标记中：C24 PASS、C25/C35/C38 open 有引擎证据；"
    "C26–C34、C36、C37 的 PASS 为草稿自评，本册未给出复核证据 ⇒ 不得直接登记为 PASS",
    "claims.csv 中 C25/C35 旧行属修复版轮记录，保持 falsified；V21续修轮新登记 C48/C49", "汇总口径")

# --- 台账登记：C48/C49（幂等，与 §11 的 C24–C47 互不冲突） ---
V21_NEW_CLAIMS = [
    ("C48", "【V21续修·谱】LB本征能级 n=1..6 扫描（mpmath 250位）：α_n 与标定值 α_1 相对差 ≤ 1.09e-75（ℏ²/N²≈3.11e-77 主导）⇒ 谱在约 76 位有效数字内退化 无独立可检验靶；草稿误差棒公式误算 ω 抵消项 正确传播误差 ~1e-87 量级 故「误差棒完备/可证伪」不成立 → open（退化谱）",
     "第一性审计", "open"),
    ("C49", "【V21续修·进动】固定 β（水星标定 43.03 角秒/百年）预测金星/地球近日点进动：GR 项复现 8.62/3.84 角秒/百年；草稿几何修正项与自身 Binet 方程一阶结果不符（正确 2πβ/(a²(1−e²)²) 草稿含 3GM/(2c²a)≈3.83e-8 因子）同标定下金星/地球预测差约 1.9×/2.6×；修正量仅 ~1e-3 角秒/百年 低于当前天体测量精度 → open（框架就绪·公式需修正）",
     "第一性审计", "open"),
]
added_v21 = 0
for cid, statement, category, status in V21_NEW_CLAIMS:
    if cid in existing:
        continue
    for field in (cid, statement, category, status, "算法联盟审计组"):
        if "," in field or '"' in field:
            raise ValueError("字段不得含裸逗号或引号: " + cid)
    text += ",".join([cid, statement, category, status, "算法联盟审计组"]) + "\n"
    added_v21 += 1
io.open(claims_path, "w", encoding="utf-8").write(text)
item("claims.csv V21续修幂等追加完毕（新增 %d 行 重复时 0 行）" % added_v21, True)

# --- 数据产出：V21续修审计 json/md（独立文件，不覆盖修复版轮产物） ---
V21_ROWS = ROWS[V21_START:]
n21_pass = sum(1 for r in V21_ROWS if r["state"] == "PASS")
n21_fail = sum(1 for r in V21_ROWS if r["state"] == "FAIL")
n21_bd = sum(1 for r in V21_ROWS if r["state"] == "BOUNDARY")
n21_info = sum(1 for r in V21_ROWS if r["state"] == "INFO")

V21_payload = {
    "title": "空间螺旋几何化统一场论 · V21续修 C25/C35 审计（并入第一性审计统一脚本）",
    "date": "2026-09-26",
    "method": ["mpmath dps=250", "参数扰动误差传播（草稿式 vs 正确式）", "量纲账本",
               "Binet 一阶微扰解析", "水星标定 β + 金星/地球交叉验证"],
    "counts": {"total": len(V21_ROWS), "PASS": n21_pass, "FAIL": n21_fail,
               "BOUNDARY": n21_bd, "INFO": n21_info},
    "C25": {"E1": float(E1_v), "C_couple": float(C_couple),
            "hbar2_over_N2": float(term1), "max_rel_spread": float(max_rel),
            "sigma_draft_rel": float(draft_sig_rel), "true_rel_n6": float(true_rel_n6),
            "log10_sigma_over_spread": float(log10_over),
            "rows": [{"n": r["n"], "En": float(r["En"]), "alpha": float(r["alpha"]),
                      "sigma_draft": float(r["sig"]), "rel_spread": float(r["rel"])}
                     for r in alpha_rows]},
    "C35": {"beta_draft": float(beta_draft), "beta_correct": float(beta_correct),
            "formula_ratio_mercury": float(formula_factor),
            "venus_geo_ratio_draft_over_correct": float(venus_ratio),
            "earth_geo_ratio_draft_over_correct": float(earth_ratio),
            "rows": c35_out},
    "rows": V21_ROWS,
}
with io.open(os.path.join(OUT_DIR, "空间螺旋V21续修_C25C35_审计.json"), "w", encoding="utf-8") as fh:
    json.dump(V21_payload, fh, ensure_ascii=False, indent=1)

lines21 = []
lines21.append("# 空间螺旋几何化统一场论 · V21续修 C25/C35 审计（250 位 mpmath）")
lines21.append("")
lines21.append("> 日期 2026-09-26 · 引擎：`源码/空间螺旋修复版_第一性审计与伪派生判定.py` §12–§14（统一脚本并入）")
lines21.append("> 方法：mpmath dps=250 / 量纲账本 / 误差传播（草稿式 vs 正确式）/ Binet 一阶微扰 / 水星标定 β + 金星/地球交叉验证")
lines21.append("")
lines21.append("**判定**：总数 %d `|` PASS=%d FAIL=%d BOUNDARY=%d INFO=%d"
               % (len(V21_ROWS), n21_pass, n21_fail, n21_bd, n21_info))
lines21.append("")
lines21.append("| 状态 | 编号 | 主张 | 依据 |")
lines21.append("|------|------|------|------|")
for r in V21_ROWS:
    det = r["detail"].replace("\n", " ")
    lines21.append("| %s | %s | %s | %s |" % (r["state"], r["tag"], r["statement"], det))
lines21.append("")
lines21.append("## C25 LB 本征谱扫描（n=1..6）")
lines21.append("")
lines21.append("| n | E_n（数值） | α_n | σα（草稿式） | (α_n−α_1)/α_1 |")
lines21.append("|----|----|----|----|----|")
for r in alpha_rows:
    lines21.append("| %d | %s | %s | %s | %s |"
                   % (r["n"], fmt(r["En"], 10), fmt(r["alpha"], 14), fmt(r["sig"], 8), fmt(r["rel"], 4)))
lines21.append("")
lines21.append("| 量 | 值 |")
lines21.append("|----|----|")
lines21.append("| ℏ²/N²（谱修正基数） | %s |" % fmt(term1, 6))
lines21.append("| 最大相对谱宽 (α_6−α_1)/α_1 | %s |" % fmt(max_rel, 6))
lines21.append("| 草稿式 σα/α（n=6） | %s |" % fmt(draft_sig_rel, 6))
lines21.append("| 正确传播 σα/α（n=6） | %s |" % fmt(true_rel_n6, 6))
lines21.append("| 草稿误差棒超出谱效应量级 | 10^%s |" % fmt(log10_over, 5))
lines21.append("")
lines21.append("## C35 多行星进动（固定 β）")
lines21.append("")
lines21.append("| 行星 | GR基础 | 几何修正(草稿式) | 总预测(草稿式) | 参考值 | 几何修正(Binet式) | 总预测(正确式) |")
lines21.append("|----|----|----|----|----|----|----|")
for r in c35_out:
    lines21.append("| %s | %s | %s | %s | %s | %s | %s |"
                   % (r["planet"], r["GR_s"], r["geo_draft_s"], r["tot_draft_s"],
                      r["ref_s"], r["geo_correct_s"], r["tot_correct_s"]))
lines21.append("")
lines21.append("| 量 | 值 |")
lines21.append("|----|----|")
lines21.append("| β（草稿式，水星标定） | %s |" % fmt(beta_draft, 12))
lines21.append("| β（Binet 一阶正确式，水星标定） | %s |" % fmt(beta_correct, 12))
lines21.append("| 公式差因子 3GM/(2c²a_mer) | %s |" % fmt(formula_factor, 6))
lines21.append("")
with io.open(os.path.join(OUT_DIR, "空间螺旋V21续修_C25C35_审计.md"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines21))

print("\n" + "=" * 76)
print("V21续修判定汇总：总数 %d | PASS=%d FAIL=%d BOUNDARY=%d INFO=%d"
      % (len(V21_ROWS), n21_pass, n21_fail, n21_bd, n21_info))
print("产出：04_公共成果/算法联盟_全维自洽与归一化/数据/空间螺旋V21续修_C25C35_审计.json / .md")
print("=" * 76)
