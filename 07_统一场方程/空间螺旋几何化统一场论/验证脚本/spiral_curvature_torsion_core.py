# -*- coding: utf-8 -*-
"""
68 号定稿仪器 · 螺旋曲率—挠率核心方程组：符号层 + 量纲层独立核验

对应文档
--------
`68_螺旋曲率挠率核心方程组_定稿_2026-10-30.md`

判定口径（与 26 号正典 / 55 号纪律同源）
--------------------------------------
1. 只判「数学恒等 / 量纲自洽」，不判物理真伪；
2. 恒等式标 IDN（零预测力），几何定义标 DEF，条件结果标 RES；
3. 任何一条 FAIL ⇒ 进程退出码 1，不许「打印 PASS 放过」；
4. 控制组必须能红（CT1 量纲扰动、CT2 符号扰动），否则仪器本身判 FAIL。

运行
----
    python spiral_curvature_torsion_core.py            # 打印 + 写 _results.json / _out.txt
    python spiral_curvature_torsion_core.py --quiet    # 只写文件

依赖：sympy（符号层）＋标准库（量纲层）。
"""

from __future__ import annotations

import json
import os
import sys
from fractions import Fraction

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
OUT_JSON = os.path.join(HERE, "spiral_curvature_torsion_core_results.json")
OUT_TXT = os.path.join(HERE, "spiral_curvature_torsion_core_out.txt")

RESULTS: list[dict] = []


def rec(sid: str, title: str, kind: str, verdict: str, detail: str) -> None:
    RESULTS.append({"id": sid, "title": title, "kind": kind,
                    "verdict": verdict, "detail": detail})


# ------------------------------------------------------------------ 符号层
R, W, c, t, lam = sp.symbols("R omega c t lambda", positive=True)
VZ = sp.symbols("v_z", real=True)

CREL = {c: sp.sqrt(R**2 * W**2 + VZ**2)}          # 类光约束 |v| = c


def simp(expr):
    """在类光约束 c² = R²ω² + v_z² 下化简。"""
    return sp.simplify(sp.expand(sp.simplify(expr)).subs(CREL))


def is_zero(expr) -> bool:
    return simp(sp.nsimplify(expr)) == 0


r = sp.Matrix([R * sp.cos(W * t), R * sp.sin(W * t), VZ * t])
v = r.diff(t)
acc = v.diff(t)
jerk = acc.diff(t)

speed2 = sp.simplify(v.dot(v))
speed = sp.sqrt(speed2)
cross = v.cross(acc)

kappa = sp.simplify(cross.norm() / speed**3)
tau = sp.simplify(cross.dot(jerk) / cross.dot(cross))
K = sp.sqrt(kappa**2 + tau**2)

# G1 · 速度模长（类光约束的等价式）
rec("G1", r"|\mathbf v|^2 = R^2\omega^2+v_z^2", "DEF",
    "PASS" if is_zero(speed2 - (R**2 * W**2 + VZ**2)) else "FAIL",
    f"residual = {simp(speed2 - (R**2 * W**2 + VZ**2))}")

# G2 · 曲率 K1
res_k = simp(kappa - R * W**2 / c**2)
rec("G2", r"\kappa = R\omega^2/c^2", "RES",
    "PASS" if res_k == 0 else "FAIL", f"residual = {res_k}")

# G3 · 挠率 T1
res_t = simp(tau - W * VZ / c**2)
rec("G3", r"\tau = v_z\omega/c^2", "RES",
    "PASS" if res_t == 0 else "FAIL", f"residual = {res_t}")

# G4 · 核心恒等式 H0
res_h0 = simp(kappa**2 + tau**2 - (W / c)**2)
rec("G4", r"\kappa^2+\tau^2=(\omega/c)^2", "IDN",
    "PASS" if res_h0 == 0 else "FAIL", f"residual = {res_h0}")

# G5 · 螺旋半径 a_h = κ/K²
a_h = sp.simplify(kappa / K**2)
res_ah = simp(a_h - R)
rec("G5", r"a_h=\kappa/K^2=R", "IDN",
    "PASS" if res_ah == 0 else "FAIL", f"residual = {res_ah}")

# G6 · 螺距 h = 2πτ/K²
h_pitch = sp.simplify(2 * sp.pi * tau / K**2)
res_h = simp(h_pitch - 2 * sp.pi * VZ / W)
rec("G6", r"h=2\pi\tau/K^2=2\pi v_z/\omega", "IDN",
    "PASS" if res_h == 0 else "FAIL", f"residual = {res_h}")

# G7 · 弧长参数式与时间参数式同一条曲线（s = ct）
s = sp.symbols("s", real=True)
r_s = sp.Matrix([
    kappa / K**2 * sp.cos(K * s),
    kappa / K**2 * sp.sin(K * s),
    tau / K * s,
])
diff_s = sp.simplify(r_s.subs(s, c * t) - r)
rec("G7", r"\mathbf r(s)|_{s=ct}=\mathbf r(t)", "IDN",
    "PASS" if all(simp(x) == 0 for x in diff_s) else "FAIL",
    f"residual vector = {list(diff_s)}")

# G8 · 标架转速：|dT/dt| = cκ
Tv = sp.Matrix([sp.simplify(x) for x in (v / speed)])
dTv = sp.Matrix([sp.simplify(x) for x in Tv.diff(t)])
mag_dT = sp.simplify(sp.sqrt(sp.simplify(dTv.dot(dTv))))
res_turn = simp(mag_dT - c * kappa)
rec("G8", r"|d\mathbf T/dt|=c\kappa", "IDN",
    "PASS" if res_turn == 0 else "FAIL", f"residual = {res_turn}")

# G9 · 副法矢演化 dB/dt = -cτN（非平凡，含挠率符号）
Nv = sp.Matrix([sp.simplify(x) for x in (dTv / mag_dT)])
Bv = sp.Matrix([sp.simplify(x) for x in Tv.cross(Nv)])
dBv = sp.Matrix([sp.simplify(x) for x in Bv.diff(t)])
rhs9 = sp.Matrix([sp.simplify(-c * tau * x) for x in Nv])
res_b = [simp(dBv[i] - rhs9[i]) for i in range(3)]
rec("G9", r"d\mathbf B/dt=-c\tau\mathbf N", "IDN",
    "PASS" if all(x == 0 for x in res_b) else "FAIL",
    f"residual vector = {res_b}")

# G10 / G11 · H1 / H2（链式微分恒等式，零预测力）
kl, tl, wl = sp.Function("kappa")(lam), sp.Function("tau")(lam), sp.Function("omega")(lam)
F0 = kl**2 + tl**2 - wl**2 / c**2
H1 = sp.diff(F0, lam) / 2
tgt1 = kl * sp.diff(kl, lam) + tl * sp.diff(tl, lam) - wl * sp.diff(wl, lam) / c**2
rec("G10", r"\kappa\kappa'+\tau\tau'=\omega\omega'/c^2", "IDN",
    "PASS" if sp.simplify(H1 - tgt1) == 0 else "FAIL",
    "由 H0 对 λ 求导，残差符号零")

H2 = sp.diff(F0, lam, 2) / 2
tgt2 = (sp.diff(kl, lam)**2 + kl * sp.diff(kl, lam, 2)
        + sp.diff(tl, lam)**2 + tl * sp.diff(tl, lam, 2)
        - (sp.diff(wl, lam)**2 + wl * sp.diff(wl, lam, 2)) / c**2)
rec("G11", r"(\kappa'^2+\tau'^2)+(\kappa\kappa''+\tau\tau'')=(\omega'^2+\omega\omega'')/c^2",
    "IDN", "PASS" if sp.simplify(H2 - tgt2) == 0 else "FAIL",
    "由 H1 再对 λ 求导，残差符号零")

# G12 · 四维类光提升：η_{μν} dx^μ dx^ν = 0
eta = sp.diag(-1, 1, 1, 1)
dx = sp.Matrix([c, v[0], v[1], v[2]])
ds2 = sp.simplify((dx.T * eta * dx)[0])
rec("G12", r"\eta_{\mu\nu}dx^\mu dx^\nu=-c^2+|\mathbf v|^2=0", "RES",
    "PASS" if is_zero(ds2) else "FAIL", f"residual = {simp(ds2)}")

# G13 · 退化：τ=0 ⇒ 圆周，κ=ω/c（此支上 c = Rω，须同时代入两条约束）
CREL0 = {VZ: 0, c: R * W}
deg0 = sp.simplify((kappa**2 + tau**2 - (W / c)**2).subs(CREL0))
k_circ = sp.simplify(kappa.subs(CREL0) - (W / c).subs(CREL0))
rec("G13", r"\tau=0\Rightarrow\kappa=\omega/c", "IDN",
    "PASS" if (deg0 == 0 and k_circ == 0) else "FAIL",
    f"residual = {k_circ}")

# ------------------------------------------------------------ 量纲层 (M,L,T)
def d(**kw):
    return {k: Fraction(v) for k, v in kw.items()}


def dmul(x, y):
    return {k: x.get(k, 0) + y.get(k, 0) for k in set(x) | set(y)}


def dpow(x, n):
    return {k: v * n for k, v in x.items()}


def deq(x, y):
    return all((x.get(k, 0) - y.get(k, 0)) == 0 for k in set(x) | set(y))


def dfmt(x):
    return "{" + ",".join(f"{k}^{v}" for k, v in sorted(x.items()) if v != 0) + "}"


DIM = {"c": d(L=1, T=-1), "w": d(T=-1), "R": d(L=1), "vz": d(L=1, T=-1),
       "h": d(L=1), "pi": d()}
DIM["kappa"] = d(L=-1)
DIM["tau"] = d(L=-1)

lhs = dmul(DIM["kappa"], DIM["kappa"])
rhs = dpow(dmul(DIM["w"], dpow(DIM["c"], -1)), 2)
rec("G14", r"[\kappa^2]=[(\omega/c)^2]", "DEF",
    "PASS" if deq(lhs, rhs) else "FAIL", f"{dfmt(lhs)} vs {dfmt(rhs)}")

k_dim = dmul(DIM["R"], dmul(dpow(DIM["w"], 2), dpow(DIM["c"], -2)))
t_dim = dmul(dmul(DIM["vz"], DIM["w"]), dpow(DIM["c"], -2))
rec("G15", r"[\kappa]=[\tau]=L^{-1}", "DEF",
    "PASS" if (deq(k_dim, d(L=-1)) and deq(t_dim, d(L=-1))) else "FAIL",
    f"[kappa]={dfmt(k_dim)}, [tau]={dfmt(t_dim)}")

h_dim = dmul(dmul(DIM["tau"], dpow(dmul(DIM["kappa"], DIM["kappa"]), -1)), d())
rec("G16", r"[h]=[\tau/\kappa^2]=L", "DEF",
    "PASS" if deq(h_dim, d(L=1)) else "FAIL", f"[h]={dfmt(h_dim)}")

# --------------------------------------------------------------------- 控制组
# CT1：把 κ 写成 Rω²/c³，量纲必须掉到 L^-2 ⇒ 仪器若判 PASS 即自坏
ct1 = dmul(DIM["R"], dmul(dpow(DIM["w"], 2), dpow(DIM["c"], -3)))
ct1_caught = not deq(ct1, d(L=-1))
rec("CT1", "控制组：κ=Rω²/c³ 必须被量纲层判非 L^-1", "CTRL",
    "PASS" if ct1_caught else "FAIL", f"[Rω²/c³]={dfmt(ct1)}")

# CT2：把 H0 的加号写成减号，残差必须非零
ct2 = simp(kappa**2 - tau**2 - (W / c)**2)
ct2_caught = ct2 != 0
rec("CT2", "控制组：κ²-τ²=(ω/c)² 必须被符号层拒绝", "CTRL",
    "PASS" if ct2_caught else "FAIL", f"residual = {ct2}")

# ------------------------------------------------------------------ 输出
n_fail = sum(1 for x in RESULTS if x["verdict"] == "FAIL")
summary = {
    "doc": "68_螺旋曲率挠率核心方程组_定稿_2026-10-30.md",
    "tool": os.path.basename(__file__),
    "total": len(RESULTS),
    "pass": sum(1 for x in RESULTS if x["verdict"] == "PASS"),
    "fail": n_fail,
    "exit_code": 1 if n_fail else 0,
    "items": RESULTS,
}

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

lines = [
    "螺旋曲率—挠率核心方程组 · 独立核验读数",
    "=" * 60,
]
for x in RESULTS:
    lines.append(f"[{x['verdict']:4s}] {x['id']:5s} ({x['kind']}) {x['title']}")
    lines.append(f"        {x['detail']}")
lines.append("=" * 60)
lines.append(f"合计 {summary['total']} 条：PASS {summary['pass']} / FAIL {summary['fail']}"
             f" ⇒ exit {summary['exit_code']}")
with open(OUT_TXT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

if "--quiet" not in sys.argv:
    print("\n".join(lines))

sys.exit(summary["exit_code"])
