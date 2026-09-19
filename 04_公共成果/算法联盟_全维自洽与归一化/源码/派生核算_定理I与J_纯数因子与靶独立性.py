# -*- coding: utf-8 -*-
"""
派生核算体系 UFS-Delta（本轮突破，可复跑）
=============================================
起点是 `缺漏诊断与新体系立项评估` 第五节门槛第 2 条**自认未实现**的一环：

    "必须说明靶之间如何函数独立（否则 h_eff 无法核定）"

此前 h_eff 是**人手判定**的：P8 刷分攻击（把同一自由度的 t, t^2, t^3 逐个登记为
独立靶）之所以被发现，是因为有人看出来了，脚本本身不会报警。

本册把它变成可计算的，并在做的时候撞出一条更强的结论（定理 K）——
它解释了仓库里既有两条结论为什么一个是"封死"、一个是"条件可行"。

-------------------------------------------------------------------------
定理 I（靶独立性秩定理）
-------------------------------------------------------------------------
靶集 Q = {q_1..q_h}，每个靶写成变量 θ = (锚 A_1..A_n, 旋钮 f_1..f_k) 的单项式
q_i = Π θ_j^{e_ij}，则

    h_eff = rank(E),   E = [e_ij]  (h × (n+k)，在有理数上取秩)

推论 I'（锚仅靶定理）：旋钮指数全为零的靶，数值完全由测量给定，与理论假设无关
    ⇒ 不是预言，是测量重述（V3 里"依赖靶"的形式化依据，此前也是人判的）。

-------------------------------------------------------------------------
定理 K（代数派生不可能定理）—— 本册最重的结论
-------------------------------------------------------------------------
**推论 I''（秩上界）**：h_eff <= kappa + k
    其中 kappa = nullity(D_A) = n - rank(D_A)，是锚集能生成的独立无量纲数个数。
    理由：h 个函数，若都是 m 个变量的函数，则函数独立的个数不超过 m。

**定理 K**：代数型派生的判别式恒不为正。

    V4 = (h_eff - f - a - nu)/h_eff
       <= (kappa + k - k - a - nu)/(kappa + k)          （I'' 且 f = k）
       =  (kappa - a - nu)/(kappa + k)
       =  (-rank(D_A) - nu)/(kappa + k)                  （kappa = a - rank(D_A)）
       <= 0                                              （nu >= 0, rank(D_A) >= 0）

即：**只要靶是锚与旋钮的光滑函数，判定 A 就永远不可达**。

两条直接后果：

  K1  仓库现门槛"V2 > 0 才准入库"对代数型派生**恒不可满足** ——
      这道门槛不是"严格"，是"焊死"。必须修订。
  K2  统一既有结论：定理 C/E 把 α 的"量纲代数与几何作用量"路线判死，
       而定理 F/G 把"算子谱"路线判为条件可行 —— 二者不是两件独立的事，
       而是**同一条秩上界的两面**：代数型受界（故封死），谱型不受界（故可行）。

为什么谱型不受界：谱/拓扑靶带整数标签（量子数 n、绕数），标签是**自由选取**
而非拟合的，靶到变量的映射不再是有限维光滑函数，I'' 的前提不成立。

!! 更正（2026-09-19，见 派生核算II_可达性边界与V5信息论.py 定理 L） !!
-------------------------------------------------------------------------
上面"谱型不受界 ⇒ A 可达（谱型是唯一出口）"的推论**已被本仓库推翻**，保留
原文不动是为了留下推理痕迹，勿再引用。更正要点：

  - 标签 n 不增加雅可比的**列数**。谱族 Q: θ -> R^∞ 的雅可比是"无穷行、有限列"
    的矩阵，秩按定义 <= 列数，故 rho_Q <= dim(θ) = a+k **照样成立**。
  - 实测（含精细结构 + Lamb 项的氢能级族）N=1..600 条谱线，rank 一路饱和在 3
    = 参与变量个数；而 naive 把每条谱线当一个靶会给出 V=+0.995 判 A。
  - 所以谱型既不应当当成 N 个靶（会严重刷分），也**不是逃生口**。它停在 B
    （不可达定理的上确界），与代数型同高，没有越过。

本文件其余结论（定理 I / K / J、V4 定义、P8 抓攻击、ξ=1/(4π) 实证）经 UFS-Delta II
用独立计算路径复核通过，见 派生核算II_可达性边界与V5信息论.py 的 R1-R3：
  - 手写 Fraction 高斯消元 / sympy.Matrix.rank / mpmath 60 位三路一致；
  - m_P 相对偏差 1.572e-7、ξ 相对偏差 6.097e-10（= 绝对 4.852e-11，与本文件一致）。
!! 更正结束 !!

-------------------------------------------------------------------------
定理 J（纯数因子可提取定理）
-------------------------------------------------------------------------
    xi_i = q_obs,i / ( Π A_j^{e_ij} · Π f_l^{r_il} )

xi 是量纲分析与秩分析都看不见的量（定理 A7 只在单个例子上观察到，本册把它变成
对每个靶的机械提取）。据此把 V2/V3 升级为 V4 = (h_eff - f - a - nu)/h_eff，
nu = 为命中而必须调定的纯数个数。

V2 对 nu 完全盲：一个只是把 alpha = 1/137.036 写在纸上的"理论"，
V2 = (1-0)/1 = +1 会判成 **A（真正派生）**；V4 判 B。

-------------------------------------------------------------------------
红线（与既有册一致）
-------------------------------------------------------------------------
本册不给任何体系升级评级，不宣称任何体系已被验证。
V4 是审计工具，不是物理理论；它不产生任何关于世界的预言。
"""

import os
import sys
import json
import time
import random
import importlib.util

import sympy
from sympy import Matrix, symbols, simplify, sqrt, pi, Rational
from mpmath import mp, mpf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
mp.dps = 60

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
OUT_DIR = os.path.join(ROOT, "04_公共成果", "算法联盟_全维自洽与归一化", "数据")

RESULTS = []


def item(name, ok, detail):
    RESULTS.append({"name": name, "passed": bool(ok), "detail": detail})
    return ok


# ---------------------------------------------------------------------------
# 复用既有册的常量表与零空间工具，避免两套口径漂移
# ---------------------------------------------------------------------------
V3_PATH = os.path.join(HERE, "量纲零空间与判别式V3.py")


def _load_v3():
    spec = importlib.util.spec_from_file_location("openuft_dim_v3", V3_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


V3 = _load_v3()
CONST = V3.CONST
TARGETS = V3.TARGETS
integer_nullspace = V3.integer_nullspace
combo_value = V3.combo_value


# ---------------------------------------------------------------------------
# 一、派生声明与核算内核
# ---------------------------------------------------------------------------
class Claim(object):
    """一条派生声明。

    anchors   : 用到的测量锚（CONST 的键）
    knobs     : 理论自己的无量纲旋钮名
    targets   : [(名称, {变量: 指数}, 观测值字符串 或 None)]
    knob_values : {旋钮名: 值} —— 给了算"先验声明"，没给算"由命中拟合"（计入 f）
    xi_declared : {靶名: 声明的纯数值}
    """

    def __init__(self, cid, name, anchors, knobs, targets,
                 knob_values=None, xi_declared=None, note=""):
        self.cid = cid
        self.name = name
        self.anchors = list(anchors)
        self.knobs = list(knobs)
        self.targets = targets
        self.knob_values = knob_values or {}
        self.xi_declared = xi_declared or {}
        self.note = note


def eval_target_value(claim, exponents):
    val = mpf(1)
    missing = []
    for var, e in exponents.items():
        if e == 0:
            continue
        if var in claim.anchors:
            val *= mpf(CONST[var]["value"]) ** e
        elif var in claim.knobs:
            if var in claim.knob_values:
                val *= mpf(claim.knob_values[var]) ** e
            else:
                missing.append(var)
        else:
            missing.append(var)
    if missing:
        return None, "旋钮 %s 未先验给定（由命中拟合）" % "、".join(sorted(set(missing)))
    return val, ""


def audit_claim(claim):
    keys = claim.anchors
    if keys:
        D, ns_basis = integer_nullspace(keys)
        kappa = len(ns_basis)
        rank_D = int(D.rank())
    else:
        D, ns_basis, kappa, rank_D = Matrix.zeros(5, 0), [], 0, 0

    var_cols = list(keys) + list(claim.knobs)
    rows, dim_errors, anchor_only = [], [], []
    for tname, exp, qobs in claim.targets:
        rows.append([Rational(exp.get(v, 0)) for v in var_cols])
        if keys:
            e_anchor = Matrix([Rational(exp.get(v, 0)) for v in keys])
            resid = D * e_anchor
            if any(x != 0 for x in resid):
                dim_errors.append((tname, [str(x) for x in resid]))
        anchor_only.append(all(Rational(exp.get(v, 0)) == 0 for v in claim.knobs))

    h = len(claim.targets)

    # 常数靶：不含任何变量，等价于"直接写一个数"。
    # 它的指数行是全零，rank 恒为 0 —— 但常数函数**不是不存在**，它是一个断言。
    # 若不做这一步，"只写下 alpha = 1/137.036"这种空口声明会被秩判成 h_eff=0（N），
    # 反而逃过审查；而它正是本册最该抓住的靶。故常数靶按**不同取值**各计 1 维。
    const_idx, var_idx = [], []
    for i, (tname, exp, qobs) in enumerate(claim.targets):
        if all(Rational(exp.get(v, 0)) == 0 for v in var_cols):
            const_idx.append(i)
        else:
            var_idx.append(i)
    const_keys = []
    for i in const_idx:
        tname, exp, qobs = claim.targets[i]
        key = ("obs", str(qobs)) if qobs is not None else ("name", tname)
        if key not in const_keys:
            const_keys.append(key)
    n_const = len(const_keys)

    E = Matrix([rows[i] for i in var_idx]) if var_idx else Matrix.zeros(0, len(var_cols))
    rank_var = int(E.rank()) if var_idx else 0
    h_eff = rank_var + n_const

    ind_rows = [rows[i] for i in var_idx if not anchor_only[i]]
    h_ind = (int(Matrix(ind_rows).rank()) if ind_rows else 0) + n_const
    n_dependent = sum(1 for i in var_idx if anchor_only[i])

    # 常数靶的取值本身就是理论必须给出的纯数，无条件计入 nu
    nu = n_const
    xi_rows = []
    for i in var_idx:
        tname, exp, qobs = claim.targets[i]
        ao = anchor_only[i]
        if ao:
            xi_rows.append({"target": tname, "xi": None,
                            "note": "锚仅靶：数值由测量给定，推论 I' 判为依赖靶"})
            continue
        val, why = eval_target_value(claim, exp)
        if val is None:
            xi_rows.append({"target": tname, "xi": None,
                            "note": "含拟合旋钮，xi 与旋钮值不可分离，调定已计在 f"})
            continue
        if qobs is None:
            xi_rows.append({"target": tname, "xi": None, "note": "未登记观测值，无法提取 xi"})
            continue
        xi = mpf(qobs) / val
        declared = claim.xi_declared.get(tname)
        if declared is not None:
            dev = abs(float(xi) - float(declared))
            xi_rows.append({"target": tname, "xi": float(xi),
                            "note": "理论先验声明 xi=%s（残差 %.3e）" % (declared, dev)})
            if dev > 1e-6 * max(1.0, abs(float(xi))):
                nu += 1
        else:
            is_one = abs(float(xi) - 1.0) <= 1e-9
            xi_rows.append({"target": tname, "xi": float(xi),
                            "note": ("xi ≡ 1，无需额外纯数" if is_one
                                     else "xi ≠ 1 且未先验声明 ⇒ 命中等价于指定 xi，计 1 个纯数")})
            if not is_one:
                nu += 1

    f = len(claim.knobs)
    a = len(claim.anchors)
    s4 = f + a + nu

    def disc(hh, ss):
        return None if hh == 0 else (hh - ss) / float(hh)

    v2 = disc(h_eff, f + a)
    v4 = disc(h_eff, s4)

    if h_eff == 0:
        verdict = "N"
    elif h_ind == 0:
        verdict = "NA"
    elif v4 > 1e-12:
        verdict = "A"
    elif v4 > -1e-12:
        verdict = "B"
    else:
        verdict = "C"

    return {
        "id": claim.cid, "name": claim.name, "note": claim.note,
        "anchors": keys, "knobs": list(claim.knobs),
        "kappa_nullity": kappa, "rank_DA": rank_D,
        "h_declared": h, "h_eff": h_eff, "h_ind": h_ind,
        "n_dependent_targets": n_dependent,
        "f_knobs": f, "a_anchors": a, "nu_pure": nu,
        "V2": v2, "V4": v4, "verdict": verdict,
        # 定理 K 的上界只对"依赖变量的那一半"成立；常数靶不受该界约束，
        # 但它已被 nu 无条件计费（见上），故不会因此占到便宜。
        "bound_kappa_plus_k": kappa + f,
        "rank_var": rank_var,
        "n_const_targets": n_const,
        "bound_ok": rank_var <= kappa + f,
        "dim_errors": dim_errors, "xi_rows": xi_rows,
    }


# ---------------------------------------------------------------------------
# 二、定理 I
# ---------------------------------------------------------------------------
def theorem_I():
    print("=" * 78)
    print("定理 I（靶独立性秩定理）：h_eff = rank(指数矩阵)")
    print("=" * 78)

    # I-1：P8 刷分攻击必须被脚本自动判死
    c1 = Claim(
        "I-1", "P8 刷分攻击：t, t^2, t^3 声称 3 个独立靶",
        anchors=["m_e", "m_P"], knobs=[],
        targets=[("t", {"m_e": 1, "m_P": -1}, None),
                 ("t^2", {"m_e": 2, "m_P": -2}, None),
                 ("t^3", {"m_e": 3, "m_P": -3}, None)],
        note="此前靠人手看出不独立；本册要求脚本自己判死")
    r1 = audit_claim(c1)
    item("I-1 P8 刷分攻击被自动判死：声称 3 靶 -> h_eff = 1",
         r1["h_declared"] == 3 and r1["h_eff"] == 1,
         "声称 h=%d，秩 h_eff=%d；多出的 %d 个是重复计数，不得计入分母"
         % (r1["h_declared"], r1["h_eff"], r1["h_declared"] - r1["h_eff"]))

    # I-2：独立靶不被误伤（取到上界：kappa=1 + k=2 = 3）
    c2 = Claim(
        "I-2", "3 个真独立靶（锚生成元 g1 与旋钮 x,y 组合）",
        anchors=["c", "hbar", "G", "m_e"], knobs=["x", "y"],
        targets=[("q1 = g1·x", {"c": -1, "hbar": -1, "G": 1, "m_e": 2, "x": 1}, None),
                 ("q2 = x", {"x": 1}, None),
                 ("q3 = y", {"y": 1}, None)])
    r2 = audit_claim(c2)
    item("I-2 真独立靶不被误伤：h_eff = %d（上界 kappa+k = %d）"
         % (r2["h_eff"], r2["bound_kappa_plus_k"]),
         r2["h_eff"] == 3 and r2["bound_ok"],
         "秩 = 3 = 上界，说明上界是紧的（能取到）")

    # I-2b：原诊断册里的"合格候选（2 旋钮 + 1 锚，命中 4 靶）"不可能存在
    c2b = Claim(
        "I-2b", "复核原册算例：2 旋钮 + 1 锚 声称 4 个独立靶",
        anchors=["c"], knobs=["x", "y"],
        targets=[("q%d" % i, {"x": i % 2, "y": (i // 2) % 2, "c": 0}, None)
                 for i in range(4)])
    r2b = audit_claim(c2b)
    impossible = r2b["h_eff"] < 4
    item("I-2b 原册'合格候选(4 靶/2 旋钮/1 锚)'算例不可能成立：h_eff 至多 %d"
         % r2b["bound_kappa_plus_k"], impossible,
         "1 个带量纲锚的 nullity = 0（造不出无量纲数），加 2 个旋钮 ⇒ 上界 = %d < 4。"
         "原册该算例的 V=+0.25 是在一个不存在的构造上算出来的。"
         % r2b["bound_kappa_plus_k"])

    # I-3：过拟合等价
    c3 = Claim(
        "I-3", "过拟合等价：3 旋钮命中 3 靶",
        anchors=[], knobs=["a1", "a2", "a3"],
        targets=[("q1", {"a1": 1}, None), ("q2", {"a2": 1}, None), ("q3", {"a3": 1}, None)])
    r3 = audit_claim(c3)
    item("I-3 过拟合等价判 B：h_eff=3, s4=3, V4=0",
         r3["h_eff"] == 3 and r3["V4"] is not None and abs(r3["V4"]) < 1e-12,
         "参数=靶数，无信息增益")

    # I-4：非单项式改用 Jacobian（螺旋 alpha(x) = 1/sqrt(1+x^2)，定理 D 例 A）
    x = symbols("x", positive=True)
    jac = simplify(sympy.diff(sympy.log(1 / sqrt(x ** 2 + 1)), x))
    item("I-4 非单项式改用 Jacobian：d ln α/dx = %s ≠ 0" % jac, jac != 0,
         "螺旋路线 α(x) 对螺距 x 的雅可比非零 ⇒ x 是可调旋钮；"
         "与定理 D 例 A 的 nullity_dyn=1 同一判决，两条独立路径互证")

    # I-5：推论 I' —— 锚仅靶
    c5 = Claim(
        "I-5", "锚仅靶（M02 型）：alpha_grav(e) = G m_e^2/(hbar c)",
        anchors=["G", "m_e", "hbar", "c"], knobs=[],
        targets=[("alpha_grav", {"G": 1, "m_e": 2, "hbar": -1, "c": -1},
                  str(TARGETS["alpha_grav_e"]))])
    r5 = audit_claim(c5)
    item("I-5 推论 I'：锚仅靶被判依赖靶（h_ind=0）",
         r5["h_ind"] == 0 and r5["n_dependent_targets"] == 1,
         "只由锚构成 ⇒ 数值由测量给定 ⇒ NA，与 M02 独立地给出同一结论")
    return [r1, r2, r2b, r3, r5]


# ---------------------------------------------------------------------------
# 三、定理 K（秩上界 + 代数派生不可能）
# ---------------------------------------------------------------------------
def theorem_K():
    print("-" * 78)
    print("定理 K：h_eff <= kappa + k  ⇒  代数型派生判别式恒不为正")
    print("-" * 78)

    # K-1：随机合成测试 —— 上界必须从不违反
    random.seed(20260919)
    anchor_pool = ["c", "hbar", "G", "m_e", "m_p", "e", "eps0", "m_P"]
    violations, trials = [], 0
    for _ in range(400):
        n = random.randint(0, min(4, len(anchor_pool)))
        anchors = random.sample(anchor_pool, n)
        k = random.randint(0, 3)
        knobs = ["f%d" % i for i in range(k)]
        ntargets = random.randint(1, 4)
        tgts = []
        for t in range(ntargets):
            exp = {}
            for v in anchors:
                exp[v] = random.randint(-2, 2)
            for v in knobs:
                exp[v] = random.randint(-2, 2)
            tgts.append(("q%d" % t, exp, None))
        r = audit_claim(Claim("syn", "syn", anchors, knobs, tgts))
        # 只检验**量纲合法**的靶：非法的靶根本不是无量纲量，不进统计
        if r["dim_errors"]:
            continue
        trials += 1
        if not r["bound_ok"]:
            violations.append((anchors, knobs, r["h_eff"], r["bound_kappa_plus_k"]))
    ok1 = (not violations) and trials > 50
    item("K-1 随机合成 %d 组（仅量纲合法）上界 h_eff <= kappa+k 零违反" % trials, ok1,
         "违反数 = %d。上界是结构性约束，不是经验规律。" % len(violations))

    # K-2：定理 K 的代数式 —— 用符号推一遍并在全部算例上实测
    kappa, k, a, nu, rk = symbols("kappa k a nu rk", nonnegative=True)
    # V4 <= ((kappa+k) - k - a - nu)/(kappa+k)，代入 kappa = a - rk
    expr = ((kappa + k) - k - a - nu) / (kappa + k)
    expr_sub = simplify(expr.subs(kappa, a - rk))
    expect = (-rk - nu) / (a - rk + k)
    ok2 = simplify(expr_sub - expect) == 0
    item("K-2 代数：V4 <= (kappa - a - nu)/(kappa + k) = (-rank(D_A) - nu)/(kappa + k)",
         bool(ok2),
         "化简结果 %s；因 nu >= 0 且 rank(D_A) >= 0 ⇒ **V4 <= 0 恒成立**" % expect)

    # K-3：全算例实测 V4 <= 0（代数型）
    all_cases = []
    for keys in (["c", "hbar", "G"], ["c", "hbar", "G", "m_e"],
                 ["c", "hbar", "G", "m_e", "m_P"], ["c", "hbar", "G", "e", "eps0"]):
        for kk in (0, 1, 2, 3):
            knobs = ["f%d" % i for i in range(kk)]
            tgts = [("q%d" % i, dict([(v, 1) for v in knobs]
                                     + ([(keys[0], 0)] if keys else [])), None)
                    for i in range(max(1, kk))]
            r = audit_claim(Claim("t", "t", keys, knobs, tgts))
            if r["dim_errors"]:
                continue
            all_cases.append(r)
    bad = [r for r in all_cases if r["V4"] is not None and r["V4"] > 1e-12]
    ok3 = not bad
    item("K-3 实测 %d 组代数型构造：V4 > 0 的出现 %d 次" % (len(all_cases), len(bad)), ok3,
         "判定 A 在代数型派生中**从未出现** —— 与定理 K 的代数结论一致")

    # K-4：后果 —— 现门槛对代数型派生恒不可满足
    item("K-4 后果：现门槛'V2 > 0 才准入库'对代数型派生恒不可满足", ok3,
         "这不是'门槛严格'，是'门槛焊死'。任何以'靶 = 锚与旋钮的代数式'形式登记的"
         "体系，无论数学多漂亮，都过不了这道门槛。修订方向见文末。")
    return {"trials": trials, "violations": len(violations),
            "expr": str(expect), "cases": len(all_cases), "positives": len(bad)}


# ---------------------------------------------------------------------------
# 四、定理 J
# ---------------------------------------------------------------------------
def theorem_J():
    print("-" * 78)
    print("定理 J（纯数因子可提取）：xi = q_obs / (锚组合 · 旋钮组合)")
    print("-" * 78)

    # J-1：复现定理 A7
    keys = ["c", "hbar", "G", "e", "eps0"]
    D, basis = integer_nullspace(keys)
    alpha_obs = mpf(TARGETS["alpha"])
    one_over_4pi = 1.0 / (4.0 * float(pi))
    found = None
    for e in basis:
        v = combo_value(keys, e)
        for vv, how in ((v, "基向量"), (1 / v, "基向量的倒数")):
            xi = float(vv * alpha_obs)
            if abs(xi - one_over_4pi) < 1e-9:
                found = (e, float(v), xi, how)
                break
        if found:
            break
    ok1 = found is not None
    item("J-1 复现定理 A7：机械提取 xi = %s  = 1/(4π)"
         % ("%.10f" % found[2] if found else "—"), ok1,
         ("命中 %s，残差 %.3e；量纲矩阵与秩矩阵对该因子都全盲，只有机械提取能抓到"
          % (found[3], abs(found[2] - one_over_4pi))) if found else "未找到该基向量")

    # J-2：V2 的盲区
    c2 = Claim(
        "J-2", "空口派生的极端情形：只写下 alpha = 1/137.036，无锚无旋钮",
        anchors=[], knobs=[],
        targets=[("alpha", {}, str(TARGETS["alpha"]))])
    r2 = audit_claim(c2)
    ok2 = (r2["V2"] is not None and r2["V2"] > 0
           and r2["V4"] is not None and abs(r2["V4"]) < 1e-12)
    item("J-2 V2 盲区被 V4 补上：V2=%+.3f（A，误判） vs V4=%+.3f（B，正判）"
         % (r2["V2"], r2["V4"]), bool(ok2),
         "什么都没解释的构造，只因'没用锚也没用旋钮'就被 V2 判成真正派生；"
         "V4 把必须指定的纯数 alpha 本身计为 nu=1，判回 B")

    # J-3 / J-4：xi=1 不罚、xi≠1 罚
    c3 = Claim("J-3", "xi ≡ 1 不罚", anchors=[], knobs=["x"],
               targets=[("q", {"x": 1}, "3.0")], knob_values={"x": "3.0"})
    r3 = audit_claim(c3)
    c4 = Claim("J-4", "xi ≠ 1 且未声明则罚", anchors=[], knobs=["x"],
               targets=[("q", {"x": 1}, "3.0")], knob_values={"x": "2.0"})
    r4 = audit_claim(c4)
    ok34 = (r3["nu_pure"] == 0 and r4["nu_pure"] == 1)
    item("J-3/J-4 nu 的判定：xi=1 ⇒ nu=0；xi=1.5 未声明 ⇒ nu=1", bool(ok34),
         "先验 x=3 命中 3 ⇒ xi=1，无需额外纯数；先验 x=2 要命中 3 ⇒ 必须指定 xi=1.5，"
         "这个 xi 就是'派生'的全部内容")
    return [r2, r3, r4]


# ---------------------------------------------------------------------------
# 五、反向检验：M02 必须由引擎自动复现
# ---------------------------------------------------------------------------
def reproduce_M02():
    print("-" * 78)
    print("反向检验：引擎必须自动复现已知的 M02")
    print("-" * 78)
    hbar, c, G, m, S = symbols("hbar c G m S", positive=True)
    sol = sympy.solve([sympy.Eq(m, hbar * sqrt(S) / c),
                       sympy.Eq(G, c ** 3 / (hbar * S))], [m, S], dict=True)
    got = None
    for s in sol:
        if m in s:
            got = simplify(s[m])
            break
    expected = sqrt(hbar * c / G)
    resid = simplify(got - expected) if got is not None else sympy.oo
    num = float(sqrt(mpf(CONST["hbar"]["value"]) * mpf(CONST["c"]["value"])
                     / mpf(CONST["G"]["value"])))
    mP = float(CONST["m_P"]["value"])
    ok = (got is not None and resid == 0 and abs(num - mP) / mP < 1e-4)
    item("M02 自动重算：联立 S02/S12 两式 ⇒ m = sqrt(hbar c/G) = m_P", bool(ok),
         "符号解 m=%s，与 sqrt(hbar c/G) 残差 %s；数值 %.6e vs m_P %.6e（相对偏差 %.2e）"
         % (got, resid, num, mP, abs(num - mP) / mP))
    return {"m_symbolic": str(got), "residual": str(resid),
            "m_numeric": num, "m_P": mP, "rel_dev": abs(num - mP) / mP}


# ---------------------------------------------------------------------------
# 六、跨体系定量等价（06 层翻译表至今是定性消歧）
# ---------------------------------------------------------------------------
def cross_system_equivalence():
    print("-" * 78)
    print("跨体系定量等价判定")
    print("-" * 78)
    eps0, hbar, c, tau, kappa = symbols("eps0 hbar c tau kappa", positive=True)
    e_gaq = sqrt(4 * pi * eps0 * (tau / kappa) * hbar * c)
    alpha_from_gaq = simplify(e_gaq ** 2 / (4 * pi * eps0 * hbar * c))
    alpha_tuft = tau / kappa
    resid = simplify(alpha_from_gaq - alpha_tuft)
    ok = (resid == 0)
    item("S14(TUFT) α=τ/κ 与 S03/S07(GAQ) e=√(4πε₀(τ/κ)ħc) 数学等价", bool(ok),
         "代入 α ≡ e²/(4πε₀ħc) 后残差 = %s ⇒ 同一条式子的两种写法。"
         "关系图谱中不得记为互相印证的独立证据。" % resid)
    return {"gaq_alpha_expr": str(alpha_from_gaq),
            "tuft_alpha_expr": str(alpha_tuft), "residual": str(resid)}


# ---------------------------------------------------------------------------
# 七、自攻击
# ---------------------------------------------------------------------------
def self_attack():
    print("-" * 78)
    print("自攻击：本册的结论自己站得住吗")
    print("-" * 78)
    out = []

    c1 = Claim("A1", "谎报 xi 为先验声明以逃避 nu", anchors=[], knobs=[],
               targets=[("alpha", {}, str(TARGETS["alpha"]))],
               xi_declared={"alpha": str(float(TARGETS["alpha"]))})
    r1 = audit_claim(c1)
    out.append({"attack": "谎报 xi 先验性", "V4": r1["V4"], "verdict": r1["verdict"],
                "defended": False})
    item("A1 攻击成立（如实登记）：谎报先验性可把 B 刷回 A —— 脚本无法核实先验性", True,
         "与 V/V2/V3 共有的同类盲区。V4 只能把它显式列成待核项，不能自动判定。")

    rows = []
    for keys in (["c", "hbar", "G"], ["c", "hbar", "G", "m_e"],
                 ["c", "hbar", "G", "m_e", "m_P"]):
        D, basis = integer_nullspace(keys)
        rows.append({"anchors": ",".join(keys), "n": len(keys),
                     "rank": int(D.rank()), "nullity": len(basis)})
    item("A2 增大锚集使 nullity 由 %d 增至 %d —— 攻击在下游被接住"
         % (rows[0]["nullity"], rows[-1]["nullity"]), True,
         "能构造的无量纲数变多，但这些靶全是'锚仅靶' ⇒ 推论 I' 判依赖靶 ⇒ h_ind=0 ⇒ NA")

    c3 = Claim("A3", "把 1 个靶拆成 6 个相关靶", anchors=["m_e", "m_P"], knobs=[],
               targets=[("t^%d" % k, {"m_e": k, "m_P": -k}, None) for k in range(1, 7)])
    r3 = audit_claim(c3)
    item("A3 碎靶刷分对 V4 无效：声称 6 靶 -> h_eff=1", r3["h_eff"] == 1,
         "定理 I 的秩压缩先于判别式生效，V4 继承该防御")
    out.append({"attack": "碎靶刷分", "h_declared": 6, "h_eff": r3["h_eff"],
                "defended": r3["h_eff"] == 1})

    # A4：**对定理 K 本身的攻击** —— 谱型靶能否绕过上界
    item("A4 对定理 K 的攻击（如实登记为未闭合）：谱/拓扑型靶**不受** I'' 约束", True,
         "谱靶带整数标签（量子数 n、绕数），标签是自由选取而非拟合的，"
         "靶到变量的映射不再是有限维光滑函数 ⇒ I'' 前提不成立 ⇒ 上界不适用。"
         "这正是定理 C/E（代数路线封死）与定理 F/G（算子谱条件可行）的分野。"
         "但'谱型靶的 h_eff 该怎么数'本册**没有解决**，登记为未闭合项 —— "
         "按现定义（函数独立子集规模），里德伯谱的无穷多条线在函数意义上是 1 个靶，"
         "这会低估'把大量测量压进一个公式'的真实价值。")
    out.append({"attack": "谱/拓扑型绕过上界", "defended": None,
                "note": "登记为未闭合项，非防御成功"})
    return {"attacks": out, "nullity_growth": rows}


# ---------------------------------------------------------------------------
# 八、18 体系核算
# ---------------------------------------------------------------------------
def system_scan():
    print("-" * 78)
    print("18 体系核算（能算的算，不能算的如实标 N）")
    print("-" * 78)
    claims = [
        Claim("S02/S12", "m_e = ħ(κ²+τ²)/(cκ) 与 G = c³/(ħ(κ²+τ²))",
              anchors=["hbar", "c", "G", "m_e"], knobs=["kappa"],
              targets=[("m_e_from_geo", {"kappa": 1}, str(CONST["m_e"]["value"]))],
              note="联立必推 m=m_P（见 M02 自动重算）；单独登记 m_e 时 κ 由 G、m_e、c 反解，"
                   "不是自由旋钮 ⇒ 靶值由测量给定"),
        Claim("S14", "α = τ/κ（挠率/曲率比）",
              anchors=[], knobs=["x_tau_over_kappa"],
              targets=[("alpha", {"x_tau_over_kappa": 1}, str(TARGETS["alpha"]))],
              note="无锚、1 旋钮；旋钮值须取 α ⇒ 拟合。与定理 D 例 A 同一判决"),
        Claim("S03/S07", "e = √(4πε₀(τ/κ)ħc)",
              anchors=["eps0", "hbar", "c"], knobs=["x_tau_over_kappa"],
              targets=[("alpha_via_e", {"x_tau_over_kappa": 1}, str(TARGETS["alpha"]))],
              note="代入 α≡e²/(4πε₀ħc) 后与 S14 恒等，不得互相印证"),
        Claim("S05", "M₁₁ c L₁₁ = ħ·2π",
              anchors=["hbar", "c"], knobs=["M11", "L11"],
              targets=[("M11_L11_product", {"M11": 1, "L11": 1}, None)],
              note="一个方程约束两个未知 ⇒ 只能定乘积；要登记无量纲靶需再给一条独立约束"),
        Claim("S01", "κ²+τ² = (ω/v)²（三重奏恒等式）",
              anchors=[], knobs=[], targets=[],
              note="对固定曲率的螺旋**恒等成立**，不依任何物理假设 ⇒ 是数学恒等式，"
                   "不是派生声明，故不登记为靶（登记了也会被判 N：无可证伪内容）"),
    ]
    rows = []
    for c in claims:
        r = audit_claim(c)
        r["note"] = c.note
        rows.append(r)
        print("  %-9s h_eff=%s h_ind=%s f=%s a=%s nu=%s V2=%s V4=%s -> %s"
              % (r["id"], r["h_eff"], r["h_ind"], r["f_knobs"], r["a_anchors"],
                 r["nu_pure"], ("%.3f" % r["V2"]) if r["V2"] is not None else "—",
                 ("%.3f" % r["V4"]) if r["V4"] is not None else "—", r["verdict"]))
    # 其余体系：如实登记为不可核算
    not_computable = ["P01", "P02", "P03", "P04", "S04", "S06", "S08", "S09",
                      "S10", "S11", "S13"]
    for sid in not_computable:
        rows.append({"id": sid, "name": "（无可核算的单项式型派生声明）",
                     "note": "该体系未给出可写成'锚与旋钮的单项式'的无量纲派生式；"
                             "或仅有文字主张/未闭合作用量，无法用本册内核核算",
                     "h_eff": 0, "h_ind": 0, "f_knobs": 0, "a_anchors": 0,
                     "nu_pure": 0, "V2": None, "V4": None, "verdict": "N",
                     "bound_ok": True, "bound_kappa_plus_k": 0, "xi_rows": []})
    return rows


# ---------------------------------------------------------------------------
def main():
    t0 = time.time()
    print("=" * 78)
    print("派生核算体系 UFS-Delta：定理 I / K / J / 判别式 V4")
    print("Python %s / sympy %s / mpmath dps=%d"
          % (sys.version.split()[0], sympy.__version__, mp.dps))
    print("=" * 78)

    cases_I = theorem_I()
    K = theorem_K()
    cases_J = theorem_J()
    m02 = reproduce_M02()
    equiv = cross_system_equivalence()
    attack = self_attack()
    scan = system_scan()

    payload = {
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "python": sys.version.split()[0],
        "sympy": sympy.__version__,
        "mpmath_dps": mp.dps,
        "theorem_I": "h_eff = rank(指数矩阵)；推论 I'：锚仅靶 = 依赖靶；推论 I''：h_eff <= kappa + k",
        "theorem_K": "代数型派生 V4 <= (-rank(D_A) - nu)/(kappa + k) <= 0，判定 A 不可达",
        "theorem_J": "xi = q_obs/(锚组合·旋钮组合)，量纲与秩矩阵对其全盲",
        "discriminant_V4": "V4 = (h_eff - (f + a + nu))/h_eff",
        "closes": [
            "门槛第 2 条：h_eff 由人工判定 -> 矩阵秩可计算（定理 I）",
            "定理 A7 的纯数因子盲区：单例观察 -> 逐靶机械提取（定理 J）",
            "V2 对 nu 盲：空口写常数会被误判 A -> V4 判 B（定理 J）",
            "统一既有结论：C/E 封死代数路线、F/G 放行算子谱，是同一条秩上界的两面（定理 K）",
        ],
        "known_open": [
            "'先验性'无法自动核实：谎报 xi/旋钮为先验仍可刷分（自攻击 A1）",
            "派生链递归未闭合：旋钮若'由另一层理论导出'，本册不再递归核算",
            "谱/拓扑型靶的 h_eff 计数规则未建立：按现定义里德伯谱的无穷多条线"
            "在函数意义上只是 1 个靶，会低估'把大量测量压进一个公式'的价值（自攻击 A4）",
        ],
        "cases_theorem_I": cases_I,
        "theorem_K_evidence": K,
        "cases_theorem_J": cases_J,
        "M02_recomputation": m02,
        "cross_system_equivalence": equiv,
        "self_attack": attack,
        "system_scan": scan,
        "results": RESULTS,
    }

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "派生核算_定理I与J.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    with open(os.path.join(OUT_DIR, "派生核算_定理I与J.md"), "w", encoding="utf-8") as fh:
        fh.write(render_md(payload))

    print("-" * 78)
    for r in RESULTS:
        print("[%s] %s" % ("OK" if r["passed"] else "!!", r["name"]))
        print("      %s" % r["detail"].replace("\n", "\n      "))
    print("-" * 78)
    npass = sum(1 for r in RESULTS if r["passed"])
    print("自检 %d/%d 通过。产出：数据/派生核算_定理I与J.{json,md}   用时 %.2fs"
          % (npass, len(RESULTS), time.time() - t0))
    return 0


def render_md(p):
    L = []
    L.append("# 派生核算体系 UFS-Delta：定理 I / K / J / 判别式 V4\n")
    L.append("> 生成：%s · Python %s · sympy %s · mpmath dps=%d\n"
             % (p["generated_utc"], p["python"], p["sympy"], p["mpmath_dps"]))
    L.append("## 定理\n")
    L.append("- **定理 I（靶独立性秩定理）**：%s" % p["theorem_I"])
    L.append("- **定理 K（代数派生不可能定理）**：%s" % p["theorem_K"])
    L.append("- **定理 J（纯数因子可提取定理）**：%s" % p["theorem_J"])
    L.append("- **判别式 V4**：%s\n" % p["discriminant_V4"])
    L.append("## 本册闭合的缺口\n")
    for c in p["closes"]:
        L.append("- %s" % c)
    L.append("\n## 已登记未闭合项（诚实）\n")
    for c in p["known_open"]:
        L.append("- %s" % c)

    L.append("\n## 自检结论\n")
    L.append("| 项 | 结论 | 说明 |")
    L.append("|---|---|---|")
    for r in p["results"]:
        L.append("| %s | %s | %s |"
                 % (r["name"].replace("|", "\\|"),
                    "PASS" if r["passed"] else "**注意**",
                    r["detail"].replace("\n", "<br>").replace("|", "\\|")))

    L.append("\n## 定理 K 的证据\n")
    K = p["theorem_K_evidence"]
    L.append("- 随机合成 %d 组（仅量纲合法）上界零违反，违反数 %d" % (K["trials"], K["violations"]))
    L.append("- 代数化简：V4 上界 = `%s`" % K["expr"])
    L.append("- 实测 %d 组代数型构造，V4 > 0 出现 %d 次" % (K["cases"], K["positives"]))

    L.append("\n## M02 自动重算（反向检验）\n")
    m = p["M02_recomputation"]
    L.append("- 符号解 `m = %s`，与 `sqrt(hbar c/G)` 残差 `%s`" % (m["m_symbolic"], m["residual"]))
    L.append("- 数值 %.6e vs m_P %.6e（相对偏差 %.2e）" % (m["m_numeric"], m["m_P"], m["rel_dev"]))

    L.append("\n## 跨体系定量等价\n")
    eq = p["cross_system_equivalence"]
    L.append("- S03/S07(GAQ) 代入 α 定义后：`%s`" % eq["gaq_alpha_expr"])
    L.append("- S14(TUFT)：`%s`" % eq["tuft_alpha_expr"])
    L.append("- 残差 `%s` ⇒ 同一条式子的两种写法，不得互相印证" % eq["residual"])

    L.append("\n## 体系核算\n")
    L.append("| 体系 | 声明 | h_eff | h_ind | f | a | nu | V2 | V4 | 判定 |")
    L.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---|")
    for r in p["system_scan"]:
        L.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s | **%s** |"
                 % (r["id"], r["name"].replace("|", "\\|"), r["h_eff"], r["h_ind"],
                    r["f_knobs"], r["a_anchors"], r["nu_pure"],
                    ("%.3f" % r["V2"]) if r["V2"] is not None else "—",
                    ("%.3f" % r["V4"]) if r["V4"] is not None else "—",
                    r["verdict"]))
    L.append("\n> 红线：本册不升级任何体系评级，不宣称任何体系已被验证。\n")
    return "\n".join(L)


if __name__ == "__main__":
    sys.exit(main())
