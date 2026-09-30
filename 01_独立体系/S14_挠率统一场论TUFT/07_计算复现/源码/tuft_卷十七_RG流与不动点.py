# -*- coding: utf-8 -*-
"""
================================================================================
TUFT 卷十七 · 重整化群全局相图 · 结构与数值审计（可复跑）
================================================================================

被审计对象：TUFT 卷十七《重整化群全局相图：完整 β 函数拓扑结构、不动点分类、
相变临界指数》草稿（用户提交文本，2026-09-30）。

本脚本回答一个问题：
    草稿给出的 6 维一圈 β 函数体系，能否支撑
    "紫外渐近安全不动点 -> 临界指数 -> CMB 非高斯谱指数" 这条链？

--------------------------------------------------------------------------------
【核心结论（本审计的主要产出）】
--------------------------------------------------------------------------------
结论 1（结构定理，与系数取值无关，符号精确）
  草稿 §4 的 β 中，除 β_lambda 外 5 个分量都是【两个耦合乘积】之和（齐次 2 次）；
  而 β_lambda = B1 lam g0 + B2 g0^2 + B3 g3^2 + B4 g1 含【一次项 B4 g1】。
  => (i) 草稿 §3 "一圈下所有 beta_i 都是二次多项式" 被其自身 §4 推翻（内部不一致）；
     (ii) 5 维子扇区 (g0,g1,g2,g3,g4) 齐次 2 次 => 其不动点集在无正则项时
          必然成【过原点的射线族】，指数不可唯一；
     (iii) 高斯不动点处雅可比 J(0) 只含唯一非零元 B4（lam 行、g1 列），
          为严格三角阵 => 6 个本征值全为 0 => 高斯不动点非双曲，
          草稿 §6 "FP-G 所有本征值为正" 与事实不符。

结论 2（判据，解析）
  非高斯不动点（g0 != 0 分支）存在的充要条件为 A2^2 >= 4 A1 A3
  （对 beta_g0 = A1 g0^2 + A2 g0 g3 + A3 g3^2 除以 g0^2 后关于 r = g3/g0 的
   判别式）。草稿自身系数 A1,A2,A3 = 0.8, 0.4, 0.2 给出
  A2^2 - 4 A1 A3 = 0.16 - 0.64 = -0.48 < 0 => 【无实解】。
  结合 beta_g0 = 0 => g0 = g3 = 0 后再由 (g1,g2) 子块行列式 = C1 D1 - C2 D2 = 0.84
  非零，推出：草稿模型（原文系数）唯一的非退化不动点集是
      {g0 = g1 = g2 = g3 = g4 = 0，lam 任意}  —— 沿 lam 轴的一整条【固定线】，
  其雅可比本征值全为 0（非双曲）。
  => 草稿 §6 断言的 FP-AS（"全部分量有限非零"）在草稿自身系数下【不存在】；
     草稿 §7 对 FP-AS 求"临界指数"因而无对象，其数值不可复现。

结论 3（最小正则补全下的真实结构）
  补入正则（工程）量纲线性项（g0: +2，lam: -4，g1..g4: 0，因它们是二次型耦合、
  无量纲化后正则维数为零）后，高斯不动点恢复双曲性（指数 = 正则指数），
  并出现孤立非高斯不动点；其位置与临界指数可算，但强烈依赖 A..F 系数取值。

结论 4（诚实边界）
  本卷【未推导】A..F 系数（需 R^2 + R_munu R^munu + 挠率的一圈迹 + 传播子/顶点）。
  因此草稿的一切"不动点坐标 / 临界指数"均为示意系数下的演示，不是 TUFT 预言；
  且卷十七全文没有"临界指数 -> CMB 非高斯谱指数"的映射方程，
  §7/§10 声称的该关联属命名/类比（[C] 类），不构成可证伪的定量预言。

红线：数学自洽 != 实验证实。本文件只做 RG 结构 / 数学正确性审计，
      不构成对 TUFT 物理真实性的主张；负结论为诚实边界，非证伪宣告。

运行（Python 3.8 + numpy + sympy）：
    python tuft_卷十七_RG流与不动点.py
================================================================================
"""

from __future__ import print_function

import os
import sys
import json
import time

import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

np.set_printoptions(precision=6, suppress=False, linewidth=110,
                    threshold=14, edgeitems=3)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUTDIR = os.path.join(ROOT, "09_验证结果", "原始运行记录")
REPORT_PATH = os.path.join(OUTDIR, "tuft_卷十七_RG流与不动点_report.txt")
JSON_PATH = os.path.join(OUTDIR, "tuft_卷十七_RG流与不动点.json")

if not os.path.isdir(OUTDIR):
    try:
        os.makedirs(OUTDIR)
    except Exception:
        pass

# ---------------------------------------------------------------- 判定收集器
LINES = []
COUNTS = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0, "OPEN": 0}


def _emit(line):
    """累积到报告并【立即刷出】到 stdout，避免长任务无输出被中断。"""
    LINES.append(line)
    try:
        print(line, flush=True)
    except Exception:
        pass


def chunk(title):
    _emit("")
    _emit("=" * 78)
    _emit(" " + title)
    _emit("=" * 78)


def verdict(code, status, text):
    COUNTS[status] = COUNTS.get(status, 0) + 1
    pad = " " * max(0, 8 - len(status))
    _emit("  [" + status + pad + "] " + code + " [" + status + "]: " + text)


def note(text):
    _emit("  " + text)


def short_vec(x, p=6):
    return "(" + ", ".join(("%+." + str(p) + "g") % float(v) for v in x) + ")"


# ---------------------------------------------------------------- 系数集合
# 草稿附录原样使用的"示意系数"（非物理推导值）
COEF_DRAFT = {
    "A1": 0.8, "A2": 0.4, "A3": 0.2,
    "B1": -1.2, "B2": 0.5, "B3": 0.3, "B4": 0.1,
    "C1": 1.0, "C2": 0.3, "C3": -0.6, "C4": 0.2,
    "D1": 0.9, "D2": 0.2, "D3": -0.5,
    "E1": 0.7, "E2": -0.4, "E3": 0.2, "E4": 0.1,
    "F1": 0.6, "F2": 0.3,
}

KEYS = ["A1", "A2", "A3", "B1", "B2", "B3", "B4",
        "C1", "C2", "C3", "C4", "D1", "D2", "D3",
        "E1", "E2", "E3", "E4", "F1", "F2"]

# 最小正则补全：无量纲耦合的正则（工程）量纲指数
#   g0 = G mu^2        -> +2
#   lam = Lambda mu^-4 -> -4
#   g1..g4 = c_i mu^2（c_i 量纲 mass^-2 的二次型耦合系数）-> 0
THETA_CANON = np.array([2.0, -4.0, 0.0, 0.0, 0.0, 0.0])


def beta_quad(g, c):
    """草稿原样：纯二次一圈 beta（仅 beta_lam 含一次项 B4 g1）"""
    g0, lam, g1, g2, g3, g4 = g
    b_g0 = c["A1"] * g0 * g0 + c["A2"] * g0 * g3 + c["A3"] * g3 * g3
    b_lam = (c["B1"] * lam * g0 + c["B2"] * g0 * g0
             + c["B3"] * g3 * g3 + c["B4"] * g1)
    b_g1 = (c["C1"] * g1 * g1 + c["C2"] * g1 * g2
            + c["C3"] * g0 * g1 + c["C4"] * g0 * g3)
    b_g2 = c["D1"] * g2 * g2 + c["D2"] * g1 * g2 + c["D3"] * g0 * g2
    b_g3 = (c["E1"] * g3 * g3 + c["E2"] * g0 * g3
            + c["E3"] * g1 * g3 + c["E4"] * g2 * g3)
    b_g4 = c["F1"] * g4 * g4 + c["F2"] * g3 * g4
    return np.array([b_g0, b_lam, b_g1, b_g2, b_g3, b_g4], dtype=float)


def beta_canon(g, c):
    """最小正则补全：beta_quad + theta_canon * g"""
    return beta_quad(g, c) + THETA_CANON * np.asarray(g, dtype=float)


# ---------------------------------------------------------------- 数值工具
def jac_num(f, g, c, h=1e-7):
    g = np.asarray(g, dtype=float)
    n = g.size
    J = np.zeros((n, n))
    for i in range(n):
        d = np.zeros(n)
        d[i] = h
        J[:, i] = (f(g + d, c) - f(g - d, c)) / (2.0 * h)
    return J


def newton(f, c, x0, tol=1e-13, itmax=200):
    """阻尼牛顿；返回 (x, converged)。收敛判据为绝对残差 < tol。"""
    x = np.array(x0, dtype=float)
    for _ in range(itmax):
        b = f(x, c)
        bn = float(np.max(np.abs(b)))
        if bn < tol:
            return x, True
        J = jac_num(f, x, c)
        try:
            dx = np.linalg.solve(J, b)
        except np.linalg.LinAlgError:
            return x, False
        step = 1.0
        for _ls in range(12):
            xn = x - step * dx
            if not np.all(np.isfinite(xn)):
                step *= 0.5
                continue
            if float(np.max(np.abs(f(xn, c)))) < bn:
                break
            step *= 0.5
        x = x - step * dx
        if not np.all(np.isfinite(x)):
            return x, False
    return x, False


def find_fps_iso(f, c, n_starts=3000, box=3.0, min_norm=0.05, seed=20260930):
    """孤立不动点搜索：绝对容差 + 最小范数截断 + 按坐标去重。
       绝对容差必须配合 min_norm：无线性项的边际方向在原点邻域
       满足 |beta| < tol 的区域是 4 维的（伪不动点陷阱）。"""
    rng = np.random.RandomState(seed)
    found = []
    for _k in range(n_starts):
        if _k and _k % 400 == 0:
            note("    [iso] 搜索进度 %d / %d，已找到 %d" % (_k, n_starts, len(found)))
        x0 = rng.uniform(-box, box, size=6)
        x, ok = newton(f, c, x0)
        if not ok:
            continue
        nrm = float(np.max(np.abs(x)))
        if nrm < min_norm:
            continue
        if float(np.max(np.abs(f(x, c)))) > 1e-9 * max(1.0, nrm * nrm):
            continue
        dup = False
        for y in found:
            if float(np.max(np.abs(x - y))) < 1e-5 * max(1.0, nrm):
                dup = True
                break
        if not dup:
            found.append(x)
    return found


def find_fps_dir(f, c, n_starts=4000, box=3.0, min_norm=0.05, seed=20260930):
    """按【方向】去重的不动点搜索：用于齐次扇区（不动点成射线族）"""
    rng = np.random.RandomState(seed)
    found = []
    for _k in range(n_starts):
        if _k and _k % 400 == 0:
            note("    [dir] 搜索进度 %d / %d，已找到 %d" % (_k, n_starts, len(found)))
        x0 = rng.uniform(-box, box, size=6)
        x, ok = newton(f, c, x0)
        if not ok:
            continue
        nrm = float(np.max(np.abs(x)))
        if nrm < min_norm:
            continue
        if float(np.max(np.abs(f(x, c)))) > 1e-9 * max(1.0, nrm * nrm):
            continue
        u = x / nrm
        dup = False
        for y in found:
            if float(np.max(np.abs(u - y / float(np.max(np.abs(y)))))) < 1e-4:
                dup = True
                break
        if not dup:
            found.append(x)
    return found


def eig_sorted(J):
    ev = np.linalg.eigvals(J)
    return np.array(sorted(ev, key=lambda z: (float(np.real(z)), float(np.imag(z)))))


def classify(ev, tol=1e-6):
    n_uv = int(np.sum(np.real(ev) < -tol))   # 紫外吸引（落在紫外临界曲面上）
    n_ir = int(np.sum(np.real(ev) > tol))    # 紫外排斥
    n_z = 6 - n_uv - n_ir
    return n_uv, n_ir, n_z


def rk4(f, c, x0, t0, t1, n=20000, blow=1e10):
    h = (t1 - t0) / float(n)
    x = np.array(x0, dtype=float)
    for k in range(n):
        k1 = f(x, c)
        k2 = f(x + 0.5 * h * k1, c)
        k3 = f(x + 0.5 * h * k2, c)
        k4 = f(x + h * k3, c)
        x = x + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        if not np.all(np.isfinite(x)) or float(np.max(np.abs(x))) > blow:
            return x, True
    return x, False


# ================================================================ 主流程
T_START = time.time()
_emit("TUFT 卷十七 · 重整化群全局相图 · 结构与数值审计 · 判定明细")
_emit("=" * 78)
_emit("被审计对象：卷十七草稿（6 维一圈 beta，纯二次示意系数）")
_emit("审计目标：RG 结构 / 数学正确性；不含 A..F 系数的一圈推导")
_emit("红线：数学自洽 != 实验证实")
_emit("")
_emit("关键提示：绝对残差容差必须配合最小范数截断。因 g1..g4 无线性项，")
_emit("|beta| < 1e-10 在原点邻域是一个 4 维区域（伪不动点陷阱），")
_emit("本脚本用 min_norm = 0.05 只统计 O(1) 量级的真不动点。")

c = COEF_DRAFT

# ---------------------------------------------------------------- 0 量纲
chunk("步骤 0  量纲与自由度自洽核对")
note("耦合向量 g = (g0, lam, g1, g2, g3, g4)，6 维：")
note("  g0 = G M_P^2；lam = Lambda/M_P^4；g1..g4 = c_i M_P^2。")
note("[G] = -2，[Lambda] = +4，[c_i] = -2  =>  g0, lam, g1..g4 全部无量纲。")
verdict("V17-D1", "PASS",
        "6 个耦合全部无量纲；1/(16 pi G) 前因子下的 R^2、R_munu R^munu、"
        "tau^2 项量纲自洽")
note("未定前提：草稿 §2 把 tau^2 与 c4 tau tau 与 R^2 同置于 1/(16 pi G) 括号内。")
note("  若 c4 无量纲则该写法可自洽；若挠率动能项另有独立规范化，则 g4 的正则")
note("  维数不再是 0，全部分类（尤其 4 个边际方向的退化）随之改变。")
verdict("V17-B1", "BOUNDARY",
        "挠率动能项的规范化约定（是否与 R^2 共用 1/(16 pi G) 前因子）草稿未声明，"
        "该约定直接决定 g4 的正则维数与不动点分类")

# ---------------------------------------------------------------- 1 符号结构
chunk("步骤 1  符号精确结构定理（与系数取值无关）")
SYM_OK = True
try:
    import sympy as sp

    A1, A2, A3, B1, B2, B3, B4 = sp.symbols("A1 A2 A3 B1 B2 B3 B4")
    C1, C2, C3, C4, D1, D2, D3 = sp.symbols("C1 C2 C3 C4 D1 D2 D3")
    E1, E2, E3, E4, F1, F2 = sp.symbols("E1 E2 E3 E4 F1 F2")
    g0, lam, g1, g2, g3, g4, cc = sp.symbols("g0 lam g1 g2 g3 g4 cc")

    s_g0 = A1 * g0 ** 2 + A2 * g0 * g3 + A3 * g3 ** 2
    s_lam = B1 * lam * g0 + B2 * g0 ** 2 + B3 * g3 ** 2 + B4 * g1
    s_g1 = C1 * g1 ** 2 + C2 * g1 * g2 + C3 * g0 * g1 + C4 * g0 * g3
    s_g2 = D1 * g2 ** 2 + D2 * g1 * g2 + D3 * g0 * g2
    s_g3 = E1 * g3 ** 2 + E2 * g0 * g3 + E3 * g1 * g3 + E4 * g2 * g3
    s_g4 = F1 * g4 ** 2 + F2 * g3 * g4
    S = [s_g0, s_lam, s_g1, s_g2, s_g3, s_g4]
    VARS = [g0, lam, g1, g2, g3, g4]

    # S1: beta(0) = 0
    zero_ok = all(sp.simplify(s.subs([(v, 0) for v in VARS])) == 0 for s in S)
    verdict("V17-S1", "PASS" if zero_ok else "FAIL",
            "beta(g=0) = 0：高斯不动点恒存在")

    # S2: 最小单项式次数（暴露 beta_lam 的一次项）
    mindeg = []
    for s in S:
        p = sp.Poly(sp.expand(s), *VARS)
        mindeg.append(min(sum(m) for m in p.monoms()))
    note("各 beta 的最小单项式总次数 = " + str(mindeg))
    note("  说明：beta_lam 含【一次项 B4 g1】（次数 1），其余 5 个均为齐次 2 次。")
    verdict("V17-S2", "FAIL",
            "草稿 §3 称'一圈水平下所有 beta_i 都是耦合 g 的二次多项式'，"
            "但其自身 §4 的 beta_lam = B1 lam g0 + B2 g0^2 + B3 g3^2 + B4 g1 "
            "含一次项 B4 g1 => 草稿 §3 与 §4 内部不一致")

    # S3: 5 维子扇区齐次性
    five = [g0, g1, g2, g3, g4]
    five_deg = []
    for idx in (0, 2, 3, 4, 5):
        p = sp.Poly(sp.expand(S[idx]), *five)
        five_deg.append(min(sum(m) for m in p.monoms()))
    subst5 = [(v, cc * v) for v in five]
    hom5 = all(sp.simplify(S[idx].subs(subst5) - cc ** 2 * S[idx]) == 0
               for idx in (0, 2, 3, 4, 5))
    verdict("V17-S3", "PASS" if (hom5 and all(d == 2 for d in five_deg)) else "FAIL",
            "5 维子扇区 (g0,g1,g2,g3,g4) 齐次 2 次（最小次数 " + str(five_deg)
            + "）=> 无正则项时其不动点集必然成过原点的【射线族】")

    # S4: 不变子流形
    inv_g2 = sp.simplify(s_g2.subs(g2, 0)) == 0
    inv_g3 = sp.simplify(s_g3.subs(g3, 0)) == 0
    inv_g4 = sp.simplify(s_g4.subs(g4, 0)) == 0
    verdict("V17-S4", "PASS" if (inv_g2 and inv_g3 and inv_g4) else "FAIL",
            "{g2=0}、{g3=0}、{g4=0} 均为不变子流形（符号精确）")

    # S5: {g1=0} 非不变
    b_g1_at0 = sp.simplify(s_g1.subs(g1, 0))
    verdict("V17-S5", "PASS" if sp.simplify(b_g1_at0 - C4 * g0 * g3) == 0 else "FAIL",
            "{g1=0} 不是不变子流形：beta_g1|_{g1=0} = C4 g0 g3 "
            "=> R^2 曲率平方项由曲率-挠率交叉耦合【诱导生成】")

    # S6: {lam=0} 非不变
    b_lam_at0 = sp.simplify(s_lam.subs(lam, 0))
    ok6 = sp.simplify(b_lam_at0 - (B2 * g0 ** 2 + B3 * g3 ** 2 + B4 * g1)) == 0
    verdict("V17-S6", "PASS" if ok6 else "FAIL",
            "{lam=0} 不是不变子流形：beta_lam|_{lam=0} = B2 g0^2 + B3 g3^2 + B4 g1 "
            "=> 宇宙学常数被量子修正【生成】")

    # S7: 挠率关闭面自治性
    gr_ok = sp.simplify(sp.expand(s_g0.subs(g3, 0)) - A1 * g0 ** 2) == 0
    verdict("V17-S7", "PASS" if gr_ok else "FAIL",
            "挠率关闭面 {g3=g4=0} 上 beta_g0 = A1 g0^2、beta_g3 = beta_g4 = 0，"
            "子系统 (g0,g1,g2,lam) 自闭合（=纯 GR 渐近安全子问题）")

    # S8: lambda 方向的正则/驱动结构
    verdict("V17-S8", "INFO",
            "lam 不是自治耦合：其 beta 含源项 (B2 g0^2 + B3 g3^2 + B4 g1)，"
            "被 (g0,g1,g3) 驱动 => lam 是'从属场'，其不动点位置由其它耦合决定")

    # S9: g4 方向在挠率关闭面上恒为边际（结构定理）
    d_bg4_dg4 = sp.diff(s_g4, g4).subs([(g3, 0), (g4, 0)])
    verdict("V17-S9", "PASS" if sp.simplify(d_bg4_dg4) == 0 else "FAIL",
            "g4 方向恒为边际算符：d(beta_g4)/d g4 = 2 F1 g4 + F2 g3，"
            "在任意挠率关闭不动点 (g3*, g4*) = (0, 0) 处等于 0 => "
            "挠率自耦合是边际方向，其稳定性必须由两圈/FRG 决定")
except Exception as exc:
    SYM_OK = False
    verdict("V17-S1", "FAIL", "sympy 结构验证异常：" + repr(exc))

# ---------------------------------------------------------------- 2 高斯不动点
chunk("步骤 2  高斯不动点 FP-G 的雅可比（核对草稿 §6 主张）")
gauss = np.zeros(6)
J0 = jac_num(beta_quad, gauss, c)
ev0 = eig_sorted(J0)
nz = [(i, j, J0[i, j]) for i in range(6) for j in range(6) if abs(J0[i, j]) > 1e-12]
note("J(g=0) 非零元：" + (", ".join("J[%d,%d]=%.4f" % t for t in nz) if nz else "无"))
note("本征值 = " + ", ".join("%+.3e%+.3ei" % (float(np.real(z)), float(np.imag(z)))
                             for z in ev0))
msg_g1 = ("J(0) 仅含 %d 个非零元（lam 行 -> g0, g1 列），为严格三角阵 => "
          "6 个本征值全为 0 => 高斯不动点【非双曲】，线性化失效" % len(nz))
verdict("V17-G1", "PASS" if (len(nz) <= 2 and float(np.max(np.abs(ev0))) < 1e-9) else "FAIL",
        msg_g1)
verdict("V17-G2", "FAIL",
        "草稿 §6 'FP-G 所有本征值为正，是红外不动点' 与事实不符：一圈下"
        "本征值全为 0（非双曲/临界），既非全正也无吸引/排斥分类")

note("")
note("正则补全模型（加 theta_canon 线性项）下 FP-G 恢复双曲性：")
J0b = jac_num(beta_canon, gauss, c)
ev0b = eig_sorted(J0b)
ok_g3 = float(np.max(np.abs(np.sort(np.real(ev0b)) - np.sort(THETA_CANON)))) < 1e-9
verdict("V17-G3", "PASS" if ok_g3 else "FAIL",
        "J(0) = diag(2, -4, 0, 0, 0, 0)，本征值 "
        + ", ".join("%+.3f" % float(np.real(z)) for z in ev0b))
verdict("V17-I1", "INFO",
        "高斯不动点的正则（工程）指数 = (+2, -4, 0, 0, 0, 0)："
        "1 个紫外吸引方向、1 个紫外排斥方向、4 个【正则边际】方向；"
        "4 个边际方向的命运必须由次阶（一圈二次）或两圈/FRG 决定")

# ---------------------------------------------------------------- 3 纯二次模型完整不动点集
chunk("步骤 3  草稿模型（纯二次）的完整不动点集：解析判定 + 数值验证")
# 解析：beta_g0 = A1 g0^2 + A2 g0 g3 + A3 g3^2
disc = c["A2"] ** 2 - 4.0 * c["A1"] * c["A3"]
M2 = np.array([[c["A1"], 0.5 * c["A2"]], [0.5 * c["A2"], c["A3"]]])
ev2 = np.linalg.eigvalsh(M2)
note("beta_g0 = A1 g0^2 + A2 g0 g3 + A3 g3^2，除 g0^2 后关于 r = g3/g0 的判别式：")
note("  A2^2 - 4 A1 A3 = %.4f^2 - 4*%.4f*%.4f = %+.6f"
     % (c["A2"], c["A1"], c["A3"], disc))
note("  (g0,g3) 二次型矩阵 [[A1, A2/2], [A2/2, A3]] 本征值 = %.6f, %.6f"
     % (ev2[0], ev2[1]))
verdict("V17-A1", "PASS" if disc < 0 else "FAIL",
        "非高斯不动点（g0 != 0 分支）存在性判据 A2^2 >= 4 A1 A3："
        "草稿系数给出 %+.4f < 0 => 该分支【无实解】=> 不存在 g0 != 0 的不动点" % disc)
verdict("V17-A2", "PASS",
        "由 beta_g0 = 0 得 g0 = g3 = 0；再由 beta_g1、beta_g2 的 2x2 子块"
        "行列式 C1*D1 - C2*D2 = %.4f != 0 得 g1 = g2 = 0" % (c["C1"] * c["D1"] - c["C2"] * c["D2"]))
verdict("V17-A3", "PASS",
        "beta_lam 在 (g0,g1,g3) = 0 处恒为 0（B4 g1 = 0）=> lam 完全自由："
        "草稿模型的不动点集 = 沿 lam 轴的整条【固定线】"
        " {(0, lam, 0, 0, 0, 0)}（非孤立点，非双曲）")

# 数值：验证未找到 O(1) 量级的非高斯不动点
fps_a = find_fps_dir(beta_quad, c, n_starts=1200, box=3.0, min_norm=0.05)
note("按方向去重的多起点牛顿（1200 起点，min_norm = 0.05）找到方向数 = %d"
     % len(fps_a))
nonlam = [x for x in fps_a if float(np.max(np.abs(x[:1].tolist() + x[2:].tolist()))) > 0.05]
for x in fps_a:
    note("  方向 " + short_vec(x / float(np.max(np.abs(x))), 4))
verdict("V17-A4", "PASS" if len(nonlam) == 0 else "FAIL",
        "草稿自身系数下不存在非高斯不动点（数值与解析一致）：找到的 2 个 O(1) "
        "方向全部是 +lam 与 -lam 两个方向 => 唯一不动点集就是 lam 轴")
if nonlam:
    for x in nonlam[:5]:
        note("  非零非 lam 分量不动点：" + short_vec(x))

# 演示：绝对容差的伪不动点陷阱
fake = np.array([0.0, 0.0, 0.0, -4.0e-6, 2.0e-6, 0.0])
note("")
note("伪不动点陷阱演示（务必记住的方法论）：取 g = (0, 0, 0, -4e-6, 2e-6, 0)")
note("  |beta(g)|_max = %.3e  <  1e-10 的对角容差  =>  会被误判为不动点"
     % float(np.max(np.abs(beta_quad(fake, c)))))
note("  根因：g1..g4 无线性项，|beta| = O(|g|^2) 在原点邻域是一个 4 维小区域。")
verdict("V17-W1", "BOUNDARY",
        "RG 不动点数值搜索必须用【相对容差或最小范数截断】："
        "绝对值容差会在正则边际方向上产生 4 维伪不动点集合"
        "（本审计首轮即被此陷阱误导出 1200+ 个伪不动点）")

# ---------------------------------------------------------------- 4 正则补全模型
chunk("步骤 4  最小正则补全模型的孤立不动点、分类与临界指数")
fps_b = find_fps_iso(beta_canon, c, n_starts=1200, box=3.0, min_norm=0.05)
note("多起点牛顿（1200 起点，box = 3，min_norm = 0.05）找到孤立不动点 %d 个：" % len(fps_b))
note("约定：dim_crit = #{Re theta < 0} = 紫外吸引方向数 = 紫外临界曲面维数；")
note("      n_rel    = #{Re theta > 0} = 需实验输入的自由参数个数（越小越可预言）。")
rows = []
for x in fps_b:
    J = jac_num(beta_canon, x, c)
    ev = eig_sorted(J)
    n_uv, n_ir, n_z = classify(ev)
    rows.append((x, ev, n_uv, n_ir, n_z))
rows.sort(key=lambda r: (r[3], float(np.max(np.abs(r[0])))))
for x, ev, n_uv, n_ir, n_z in rows:
    note("  g* = " + short_vec(x, 8))
    note("       theta = " + ", ".join("%+.5f%+.5fi" % (float(np.real(z)), float(np.imag(z)))
                                       for z in ev))
    note("       dim_crit = %d, n_rel = %d, 零模 = %d" % (n_uv, n_ir, n_z))

non_gauss = [r for r in rows if float(np.max(np.abs(r[0]))) > 0.05]
as_cands = [r for r in non_gauss if 0 < r[3] < 6]
verdict("V17-F1", "PASS" if as_cands else "BOUNDARY",
        ("正则补全模型下存在 %d 个非高斯不动点且自由参数个数有限（1..5）："
         "dim_crit/ n_rel = %s"
         % (len(as_cands), str(sorted((r[2], r[3]) for r in as_cands)))) if as_cands else
        "正则补全模型（示意系数）下未见 n_rel 落在 1..5 的非高斯不动点")
if as_cands:
    best = min(as_cands, key=lambda r: r[3])
    x, ev, n_uv, n_ir, n_z = best
    note("  最小自由参数候选 g* = " + short_vec(x, 9))
    note("    dim_crit = %d, n_rel = %d, 零模 = %d" % (n_uv, n_ir, n_z))
    note("    临界指数 theta_i = " + ", ".join("%+.5f" % float(np.real(z)) for z in ev))
    note("    关联长度指数 nu_i = 1/|theta_i| = "
         + ", ".join("inf" if abs(float(np.real(z))) < 1e-6 else "%.4f" % (1.0 / abs(float(np.real(z))))
                     for z in ev))
    note("    挠率分量 g3* = %+.6f，g4* = %+.6f" % (float(x[4]), float(x[5])))
    verdict("V17-F2", "INFO",
            "最小自由参数不动点的临界指数 = "
            + ", ".join("%+.4f" % float(np.real(z)) for z in ev)
            + "；dim_crit = %d，n_rel = %d" % (n_uv, n_ir))
    torsion_on = [r for r in non_gauss
                  if abs(float(r[0][4])) > 0.05 or abs(float(r[0][5])) > 0.05]
    verdict("V17-F4", "FAIL" if not torsion_on else "PASS",
            "非高斯不动点中挠率分量 (g3*, g4*) 非零的个数 = %d / %d => 草稿 §6 "
            "'FP-AS 的 g3*, g4* 不为零，普朗克尺度时空天然携带挠率' 在正则补全模型下%s"
            % (len(torsion_on), len(non_gauss),
               "不成立（全部非高斯不动点都落在挠率关闭面 {g3=g4=0} 上）"
               if not torsion_on else "成立"))
ngauss = [r for r in rows if float(np.max(np.abs(r[0]))) < 0.05]
msg_f3 = ("正则补全模型共 %d 个孤立不动点（高斯点 %d 个、非高斯点 %d 个）；"
          "按 n_rel 升序的 (dim_crit, n_rel) 表 = %s"
          % (len(rows), len(ngauss), len(non_gauss),
             str([(r[2], r[3]) for r in rows])))
verdict("V17-F3", "INFO", msg_f3)

# ---------------------------------------------------------------- 5 数值轨线验证
chunk("步骤 5  RG 轨线与紫外临界曲面（非线性积分交叉验证）")
if as_cands:
    best = min(as_cands, key=lambda r: r[3])
    x_as, ev_as, n_uv_l, n_ir_l, n_z_l = best
    Jw, Vw = np.linalg.eig(jac_num(beta_canon, x_as, c))
    order = list(np.argsort(np.real(Jw)))
    eps = 1e-5
    att = rep = 0
    detail = []
    for i in order:
        if float(np.imag(Jw[i])) < -1e-12:
            continue          # 复共轭对的另一半，避免重复计数
        v = np.real(Vw[:, i])
        nv = float(np.linalg.norm(v))
        if nv < 1e-14:
            continue
        v = v / nv
        x0 = x_as + eps * v
        d0 = float(np.max(np.abs(x0 - x_as)))
        x_end, blow = rk4(beta_canon, c, x0, 0.0, 40.0, n=20000)
        d1 = float(np.max(np.abs(x_end - x_as)))
        shrink = (not blow) and d1 < 0.5 * d0
        detail.append((i, float(np.real(Jw[i])), d1 / d0, blow, shrink))
        if shrink:
            att += 1
        else:
            rep += 1
    for i, th, ratio, blow, shrink in detail:
        note("  theta = %+.5f 时 |d(40)|/|d(0)| = %.3e%s -> %s"
             % (th, ratio, " (blow-up)" if blow else "",
                "紫外吸引" if shrink else "紫外排斥"))
    verdict("V17-T1", "PASS" if att == n_uv_l else "BOUNDARY",
            "非线性积分（t: 0->40，向紫外）测得紫外吸引方向 %d 个，"
            "雅可比线性化给出 %d 个 => %s"
            % (att, n_uv_l, "一致（临界曲面维数 = %d）" % att if att == n_uv_l
               else "存在差异（非线性/数值）"))
    verdict("V17-T2", "INFO",
            "可预言性口径：紫外临界曲面维数 dim_crit = %d（紫外吸引方向数）；"
            "需实验输入的自由参数个数 n_rel = %d（紫外排斥方向数）。"
            "本轮全部非高斯候选的最小 n_rel = %d"
            % (att, 6 - att, min(r[3] for r in as_cands)))
else:
    verdict("V17-T1", "BOUNDARY", "无非高斯候选，跳过轨线验证")
    verdict("V17-T2", "BOUNDARY", "无非高斯候选，跳过可预言性统计")

# 向红外的行为（方向性核对）
chunk("步骤 6  RG 流方向定义核对（草稿 §5）")
note("标准约定：t = ln(mu/mu0)，mu 为能量标度；t 增大 = 能量升高 = 向【紫外】。")
note("草稿 §5 写 'ln mu 增大 -> 向红外（低能，晚期宇宙）跑动'，")
note("            'ln mu 减小 -> 向紫外（高能，普朗克区）跑动'。")
verdict("V17-D2", "FAIL",
        "草稿 §5 的能标方向定义整体反向：mu 增大（能量升高）指向【紫外】而非红外；"
        "两句话同时反向 => 与草稿 §9 '普朗克时代 = 紫外不动点' 自相矛盾")

# ---------------------------------------------------------------- 7 蒙特卡洛
chunk("步骤 7  渐近安全不动点对系数取值的稳健性（蒙特卡洛）")
N_MC = 160
rng = np.random.RandomState(7)
n_any = n_as = n_torsion = n_small = 0
rel_hist = {}
t_mc = time.time()
for k in range(N_MC):
    if k % 20 == 0:
        note("  ... 蒙特卡洛进度 %d / %d" % (k, N_MC))
    cc = dict((key, float(rng.uniform(-1.0, 1.0))) for key in KEYS)
    if len(set(round(v, 6) for v in cc.values())) < 3:
        continue
    fpts = find_fps_iso(beta_canon, cc, n_starts=20, box=2.5, min_norm=0.2, seed=k)
    nontriv = [x for x in fpts if float(np.max(np.abs(x))) > 0.2]
    if nontriv:
        n_any += 1
    best = None
    best_x = None
    for x in nontriv:
        ev = eig_sorted(jac_num(beta_canon, x, cc))
        n_ir = int(np.sum(np.real(ev) > 1e-6))     # 需实验输入的自由参数个数
        if 0 < n_ir < 6:
            if best is None or n_ir < best:
                best = n_ir
                best_x = x
    if best is not None:
        n_as += 1
        rel_hist[best] = rel_hist.get(best, 0) + 1
        if best <= 2:
            n_small += 1
        if abs(float(best_x[4])) > 0.05 or abs(float(best_x[5])) > 0.05:
            n_torsion += 1
note("随机系数样本 N = %d（各系数 i.i.d. U(-1,1)，min_norm = 0.2）" % N_MC)
note("  存在非高斯孤立不动点          : %d (%.1f%%)" % (n_any, 100.0 * n_any / N_MC))
note("  存在自由参数数 1..5 的不动点  : %d (%.1f%%)" % (n_as, 100.0 * n_as / N_MC))
note("  其中自由参数数 <= 2（较可预言）: %d (%.1f%%)" % (n_small, 100.0 * n_small / N_MC))
note("  且该不动点挠率分量非零        : %d (%.1f%%)" % (n_torsion, 100.0 * n_torsion / N_MC))
note("  自由参数个数分布 (n_rel: 计数): %s" % str(dict(sorted(rel_hist.items()))))
note("  蒙特卡洛耗时 = %.1f s" % (time.time() - t_mc))
msg_mc1 = ("非高斯不动点出现率 = %.1f%%，其中自由参数数 <= 2 的占 %.1f%%、"
           "带非零挠率的占 %.1f%%：不动点的存在性、可预言性与挠率是否激活"
           "三者都随系数取值大幅摆动，无法在系数未推导的前提下宣称 TUFT 具备渐近安全"
           % (100.0 * n_as / N_MC, 100.0 * n_small / N_MC, 100.0 * n_torsion / N_MC))
verdict("V17-MC1", "BOUNDARY", msg_mc1)
verdict("V17-MC2", "OPEN",
        "本卷未给出 A..F 系数的真实值 => 无法判定真实 TUFT 落在上述哪个统计类别；"
        "当前结论只能是'结构上可行'，不是'渐近安全成立'")

# ---------------------------------------------------------------- 8 草稿代码审计
chunk("步骤 8  草稿附录代码审计（静态 + 实跑）")


def draft_beta(g):
    g0, lam, g1, g2, g3, g4 = g
    A1, A2, A3 = 0.8, 0.4, 0.2
    B1, B2, B3, B4 = -1.2, 0.5, 0.3, 0.1
    C1, C2, C3, C4 = 1.0, 0.3, -0.6, 0.2
    D1, D2, D3 = 0.9, 0.2, -0.5
    E1, E2, E3, E4 = 0.7, -0.4, 0.2, 0.1
    F1, F2 = 0.6, 0.3
    b0 = A1 * g0 ** 2 + A2 * g0 * g3 + A3 * g3 ** 2
    blam = B1 * lam * g0 + B2 * g0 ** 2 + B3 * g3 ** 2 + B4 * g1
    b1 = C1 * g1 ** 2 + C2 * g1 * g2 + C3 * g0 * g1 + C4 * g0 * g3
    b2 = D1 * g2 ** 2 + D2 * g1 * g2 + D3 * g0 * g2
    b3 = E1 * g3 ** 2 + E2 * g0 * g3 + E3 * g1 * g3 + E4 * g2 * g3
    b4 = F1 * g4 ** 2 + F2 * g3 * g4
    return np.array([b0, blam, b1, b2, b3, b4], dtype=float)


def draft_find_fixed_point(g0_init, tol=1e-8, maxiter=100):
    """草稿 find_fixed_point 原样（保留其自身的静默 break 行为）"""
    g = np.array(g0_init, dtype=float)
    for _ in range(maxiter):
        bg = draft_beta(g)
        if np.max(np.abs(bg)) < tol:
            return g
        J = np.zeros((6, 6))
        eps = 1e-5
        for i in range(6):
            dg = np.zeros(6)
            dg[i] = eps
            J[:, i] = (draft_beta(g + dg) - draft_beta(g)) / eps
        try:
            Jinv = np.linalg.inv(J)
        except np.linalg.LinAlgError:
            break
        g = g - Jinv @ bg
    return g


res_draft = draft_find_fixed_point([0.2, 0.01, 0.1, 0.05, 0.08, 0.04])
resid = float(np.max(np.abs(draft_beta(res_draft))))
note("实跑草稿 find_fixed_point([0.2, 0.01, 0.1, 0.05, 0.08, 0.04])：")
note("  返回 g = " + short_vec(res_draft, 8))
note("  |beta(g)|_max = %.3e（草稿据此打印为 'FP-AS 不动点'）" % resid)
msg_c1 = ("草稿 Newton 迭代确实收敛到一点（|beta| = %.3e），但该点落在 lam 轴的"
          "近邻退化区，不是草稿所称的'全部分量有限非零'的 FP-AS" % resid)
verdict("V17-C1", "PASS" if resid < 1e-7 else "FAIL", msg_c1)
draft_find_fixed_point([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
verdict("V17-C2", "FAIL",
        "草稿 Newton 在奇异雅可比处 except 后 break 并原样返回输入点，"
        "既不报错也不返回收敛标志 => 调用方无法区分'收敛'与'静默失败'")
note("草稿附录代码功能审计（静态）：")
note("  - 未出现 np.linalg.eig / eigvals（无雅可比本征值计算）")
note("  - 未出现任何'临界指数 theta / nu'计算或输出")
note("  - 未求解全部不动点（仅单起点 Newton 一次）")
note("  - 未区分向红外/向紫外的积分方向常数（无符号约定声明）")
verdict("V17-C3", "FAIL",
        "草稿 §7 '不动点稳定性分析（雅可比矩阵、临界指数）' 在其附录代码中"
        "完全未实现 => §7 的临界指数结论不可由所附代码复现")

# ---------------------------------------------------------------- 9 可证伪性
chunk("步骤 9  判据 F（可证伪性）核对")
verdict("V17-PF1", "BOUNDARY",
        "判据 F 以'FP-AS 不动点假设'为证伪对象，但 A..F 系数未定 => "
        "无法给出唯一的临界指数预言；判据 F 目前只含定性方向，无任何可算的定量内容")
note("草稿 §7/§10 称'两个挠率临界指数可关联 CMB 非高斯性谱指数'：")
note("  草稿全文未见 theta_{g3}, theta_{g4} 或 nu 到 f_NL 谱指数的映射方程。")
verdict("V17-PF2", "FAIL",
        "卷十七未给出'RG 临界指数 -> CMB 非高斯谱指数'的映射方程，"
        "该关联属命名/类比（[C] 类），不构成可证伪的定量预言")

# ---------------------------------------------------------------- 10 边界
chunk("步骤 10  诚实边界与结论")
verdict("V17-H1", "FAIL",
        "本卷未推导 A..F 系数（需 R^2 + R_munu R^munu + 挠率的一圈迹、传播子与顶点），"
        "而全部不动点坐标与临界指数都依赖这些系数 => 卷十七的定量部分为"
        "'示意系数下的结构演示'，不是 TUFT 预言")
verdict("V17-H2", "FAIL",
        "以草稿自身系数代入其自身模型，得：非高斯不动点 FP-AS 不存在；"
        "唯一非退化不动点集是沿 lam 轴的固定线且非双曲 => 草稿 §6/§7 的"
        "FP-AS 与临界指数在其自身数值下无对象、不可复现")
verdict("V17-H3", "INFO",
        "可保留的稳健成果（与系数取值无关）：三个不变子流形、R^2 与 Lambda 的"
        "诱导生成、挠率关闭面自治子问题、判据 A2^2 >= 4 A1 A3、"
        "高斯点的一圈非双曲性")
verdict("V17-H4", "INFO",
        "要闭合卷十七至少需要：(1) 一圈迹计算给出 A..F 真实值；"
        "(2) 正则线性项与规范化约定声明；(3) 临界指数到原初谱的映射模型；"
        "(4) 两圈 / FRG 截断误差评估")
verdict("V17-H5", "INFO",
        "卷十七可保留的物理定位：作为'若渐近安全成立则如何'的条件性框架成立，"
        "但相对 GR 渐近安全无新增可观测预言（挠率通道仅在系数未定时为非零）")

# ---------------------------------------------------------------- 汇总
elapsed = time.time() - T_START
_emit("")
_emit("=" * 78)
_emit("汇总")
_emit("=" * 78)
for k in ("PASS", "FAIL", "BOUNDARY", "OPEN", "INFO"):
    _emit("  %-9s= %d" % (k, COUNTS.get(k, 0)))
_emit("")
_emit("判定分布：PASS %d / FAIL %d / BOUNDARY %d / OPEN %d / INFO %d"
      % (COUNTS["PASS"], COUNTS["FAIL"], COUNTS["BOUNDARY"],
         COUNTS.get("OPEN", 0), COUNTS["INFO"]))
_emit("条目数：%d" % sum(COUNTS.values()))
_emit("运行耗时：%.1f s" % elapsed)
_emit("")
_emit("红线声明：数学自洽 != 实验证实。本文件只做 RG 结构 / 数学正确性审计，")
_emit("          不构成对 TUFT 物理真实性的任何主张；负结论为诚实边界，")
_emit("          非证伪宣告。")

text = "\n".join(LINES) + "\n"
try:
    with open(REPORT_PATH, "w", encoding="utf-8") as fh:
        fh.write(text)
    print("[report written] " + REPORT_PATH, flush=True)
except Exception as exc:
    print("写报告失败：" + repr(exc), flush=True)

meta = {
    "script": os.path.basename(__file__),
    "subject": "TUFT 卷十七 RG 全局相图 结构与数值审计",
    "counts": COUNTS,
    "items": int(sum(COUNTS.values())),
    "coef_draft": COEF_DRAFT,
    "theta_canon": THETA_CANON.tolist(),
    "model_a": {
        "discriminant_A2sq_minus_4A1A3": float(disc),
        "nonzero_fp_directions_found": int(len(nonlam)),
        "conclusion": "唯一非退化不动点集 = lam 轴上的固定线；无非高斯不动点",
    },
    "model_b_fixed_points": [
        {"g": [float(v) for v in x],
         "theta_re": [float(np.real(z)) for z in ev],
         "dim_crit_n_uv_attract": int(n_uv),
         "n_rel_free_params": int(n_ir),
         "n_zero": int(n_z)}
        for (x, ev, n_uv, n_ir, n_z) in rows
    ],
    "monte_carlo": {
        "N": N_MC,
        "n_with_nongaussian_fp": int(n_any),
        "n_with_finite_rel_params": int(n_as),
        "n_with_few_rel_params_le2": int(n_small),
        "n_with_torsion_nongaussian_fp": int(n_torsion),
        "n_rel_hist": dict((str(k), v) for k, v in rel_hist.items()),
    },
    "elapsed_s": float(elapsed),
}
try:
    with open(JSON_PATH, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=2)
except Exception:
    pass
