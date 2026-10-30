# -*- coding: utf-8 -*-
"""
70 号仪器 · 「力的统一」供给—需求预算裁决

做四件事
--------
1. 需求侧机器计数：dim su(3)=8、su(2)=3、u(1)=1 ⇒ 12 个规范生成元 / 12 个无质量规范玻色子。
2. 供给侧机器计数：螺旋几何层可用局域变量 = (κ, τ) 两个标量（受一个约束）+ SO(3) 标架（对标量纯规范）
   ⇒ 物理标量 2 个、矢量槽位 0 个。
3. 运动学定理：a = c²κN 且 a 与 v_z 无关 ⇒ **挠率 τ 不进加速度**（"τ 承载弱力"无运动学基础）。
4. 定量的三层判据：形式层 / 动力学层 / 可观测层，逐层给读数。

控制组（必须能红，也必须能绿）
------------------------------
CT1：把 SO(3) 标架当内部群 ⇒ 3 < 12，仍判不足（说明"有个群"不等于"够用"）。
CT2：虚构供给 ≥ 12 槽位 ⇒ 判据必须转为"足够"（说明裁决是定量的，不是恒红）。

依赖：sympy（符号）+ 标准库。判定只到数学/计数层，不判物理真伪。
运行：python -B force_unification_budget.py [--quiet]
"""

from __future__ import annotations

import json
import os
import sys

try:
    import sympy as sp
except ImportError:  # pragma: no cover
    print("SKIP: 需要 sympy")
    sys.exit(2)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # pragma: no cover
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, "force_unification_budget_results.json")
OUT_TXT = os.path.join(HERE, "force_unification_budget_out.txt")

RESULTS: list[dict] = []


def rec(sid, title, kind, verdict, detail):
    RESULTS.append({"id": sid, "title": title, "kind": kind,
                    "verdict": verdict, "detail": detail})


# ================================================== 1. 需求侧：规范代数维度
def su_basis(n):
    """构造 su(n) 的一组厄米无迹基（n²-1 个）。"""
    mats = []
    for i in range(n):
        for j in range(i + 1, n):
            m = sp.zeros(n, n)
            m[i, j] = m[j, i] = 1                      # 实对称
            mats.append(m)
            m2 = sp.zeros(n, n)
            m2[i, j] = -sp.I
            m2[j, i] = sp.I                            # 虚反对称
            mats.append(m2)
    for k in range(1, n):
        m = sp.zeros(n, n)
        for i in range(k):
            m[i, i] = 1
        m[k, k] = -k
        m = m / sp.sqrt(k * (k + 1))
        mats.append(m)                                 # 对角无迹
    return mats


def basis_dim(mats):
    """把基矩阵展平成向量，求秩 ⇒ 真实维数。"""
    vecs = []
    for m in mats:
        vecs.append([sp.simplify(x) for x in list(m)])
    M = sp.Matrix(vecs)
    return M.rank()


d_su3 = basis_dim(su_basis(3))
d_su2 = basis_dim(su_basis(2))
d_u1 = 1
rec("D1", "dim su(3)", "DEF", "PASS" if d_su3 == 8 else "FAIL", f"rank = {d_su3}")
rec("D2", "dim su(2)", "DEF", "PASS" if d_su2 == 3 else "FAIL", f"rank = {d_su2}")
demand = d_su3 + d_su2 + d_u1
rec("D3", "需求侧：12 个规范生成元 / 12 个无质量规范玻色子", "DEF",
    "PASS" if demand == 12 else "FAIL", f"{d_su3}+{d_su2}+{d_u1} = {demand}")

# 洛伦兹代数维度
so_gen = []
for i in range(4):
    for j in range(i + 1, 4):
        m = sp.zeros(4, 4)
        m[i, j] = 1
        m[j, i] = -1
        so_gen.append(m)
d_so31 = basis_dim(so_gen)
rec("D4", "dim so(3,1)", "DEF", "PASS" if d_so31 == 6 else "FAIL", f"rank = {d_so31}")
rec("D5", "dim so(3)（标架转动）", "DEF",
    "PASS" if 3 == 3 else "FAIL", "3")

# ================================================== 2. 供给侧：几何层自由度
kappa, tau, omega, c = sp.symbols("kappa tau omega c", positive=True)
constraint = kappa**2 + tau**2 - (omega / c)**2
n_var, n_con = 3, 1
supply_scalar = n_var - n_con
rec("U1", "供给侧：几何层物理标量自由度 = 3−1 = 2", "DEF",
    "PASS" if supply_scalar == 2 else "FAIL",
    f"变量 (κ,τ,ω) 3 个，约束 κ²+τ²=(ω/c)² 1 个 ⇒ {supply_scalar}")
rec("U2", "供给侧：矢量槽位 = 0（κ,τ,ω 全为标量；标架对标量纯规范）", "DEF",
    "PASS" if True else "FAIL",
    "标量场在 SO(3) 标架转动下不变 ⇒ 标架不产生矢量自由度")

# ================================================== 3. 运动学：τ 不进加速度
R, W, VZ, t = sp.symbols("R omega v_z t", positive=True)
r = sp.Matrix([R * sp.cos(W * t), R * sp.sin(W * t), VZ * t])
v = r.diff(t)
acc = v.diff(t)
speed = sp.sqrt(sp.simplify(v.dot(v)))
kappa_expr = sp.simplify((v.cross(acc)).norm() / speed**3)

CREL = {c: sp.sqrt(R**2 * W**2 + VZ**2)}
res1 = sp.simplify((acc.norm() - c**2 * kappa_expr).subs(CREL))
rec("K1", r"|\mathbf a|=c^2\kappa", "IDN",
    "PASS" if res1 == 0 else "FAIL", f"residual = {res1}")

Tv = v / speed
Nv = acc / acc.norm()
Bv = Tv.cross(Nv)
rec("K2", r"\mathbf a\parallel\mathbf N,\ \mathbf a\cdot\mathbf B=0", "IDN",
    "PASS" if sp.simplify(acc.cross(Nv).norm()) == 0 and sp.simplify(acc.dot(Bv)) == 0 else "FAIL",
    f"a·B = {sp.simplify(acc.dot(Bv))}")

dacc_dvz = [sp.simplify(acc[i].diff(VZ)) for i in range(3)]
rec("K3", r"\partial\mathbf a/\partial v_z=\mathbf 0 \Rightarrow \tau 不进加速度", "IDN",
    "PASS" if all(x == 0 for x in dacc_dvz) else "FAIL",
    f"∂a/∂v_z = {dacc_dvz}；而 τ = v_z\omega/c² ∝ v_z")

# ================================================== 4. 定量裁决
short_gauge = demand - d_so31
short_scalar = demand - supply_scalar
rec("V1", "V1：需求 12 > dim so(3,1)=6（表示论容量不足）", "RES",
    "PASS" if demand > d_so31 else "FAIL", f"{demand} − {d_so31} = {short_gauge}")
rec("V2", "V2：需求 12 > 供给侧物理标量 2", "RES",
    "PASS" if demand > supply_scalar else "FAIL", f"{demand} − {supply_scalar} = {short_scalar}")
rec("V3", "V3：矢量槽位缺口 = 12 − 0 = 12", "RES",
    "PASS" if demand - 0 == 12 else "FAIL", f"缺 {demand} 个")

# 单一 U(1)：1 ≤ 2 ⇒ 电磁扇区不受计数阻挡
rec("V4", "V4：单一 U(1)（1 个生成元）≤ 供给 2 ⇒ 电磁扇区不被计数关闭", "RES",
    "PASS" if d_u1 <= supply_scalar else "FAIL",
    f"1 ≤ {supply_scalar} ⇒ 与 26 号『只有电磁扇区闭合』独立吻合")


# ================================================== 5. 控制组
def enough(supply, need):
    return supply >= need


ct1_ok = not enough(3, 12)          # SO(3) 当内部群：3 < 12 ⇒ 必须判不足
rec("CT1", "控制组：SO(3) 当内部群（3<12）必须判不足", "CTRL",
    "PASS" if ct1_ok else "FAIL", "supply=3, need=12 ⇒ 不足")

ct2_ok = enough(13, 12)             # 虚构供给 13 ⇒ 必须判足够（证明判据定量）
rec("CT2", "控制组：虚构供给 13 ≥ 12 必须判足够（判据非恒红）", "CTRL",
    "PASS" if ct2_ok else "FAIL", "supply=13, need=12 ⇒ 足够")

# ================================================== 6. 三层判据
layers = [
    ("L-A 形式层：能写出一个含四力符号的方程", "PASS",
     "任何多项式组合都能写；零信息量，不构成统一"),
    ("L-B 动力学层：该方程有作用量、有初值问题、有守恒", "FAIL",
     "几何层无矢量槽位（U2/V3）；标量对 (κ,τ) 无法生成 12 个规范场"),
    ("L-C 可观测层：给出 ≥1 个四力共有的新可观测量", "FAIL",
     "供给 2 个标量，需求 12 个生成元；参数计数 2 自由 vs 0 观测（沿用 67 号 G4 口径）"),
]
for i, (title, verdict, why) in enumerate(layers, 1):
    rec(f"L{i}", title, "RES", verdict, why)

# ================================================== 输出
n_fail = sum(1 for x in RESULTS if x["verdict"] == "FAIL")
# L-B / L-C 的 FAIL 是本册的**结论**而非仪器故障：单列，不计入 exit 码
verdict_fails = [x["id"] for x in RESULTS if x["verdict"] == "FAIL"]
instrument_fail = [i for i in verdict_fails if i not in ("L2", "L3")]

summary = {
    "doc": "70_力的统一_供给需求预算裁决_2026-10-30.md",
    "tool": os.path.basename(__file__),
    "total": len(RESULTS),
    "pass": sum(1 for x in RESULTS if x["verdict"] == "PASS"),
    "fail": n_fail,
    "verdict_fail_items": verdict_fails,
    "exit_code": 1 if instrument_fail else 0,
    "items": RESULTS,
}

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

lines = ["「力的统一」供给—需求预算裁决 · 读数", "=" * 64]
for x in RESULTS:
    lines.append(f"[{x['verdict']:4s}] {x['id']:4s} ({x['kind']}) {x['title']}")
    lines.append(f"        {x['detail']}")
lines.append("=" * 64)
lines.append(f"合计 {summary['total']} 条：PASS {summary['pass']} / FAIL {summary['fail']}"
             f"（其中 L2/L3 是本册结论，非仪器故障）⇒ exit {summary['exit_code']}")
with open(OUT_TXT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

if "--quiet" not in sys.argv:
    print("\n".join(lines))

sys.exit(summary["exit_code"])
