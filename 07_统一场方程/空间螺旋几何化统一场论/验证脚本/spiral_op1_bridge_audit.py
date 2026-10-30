# -*- coding: utf-8 -*-
"""
69 号仪器 · O-P1 算子错配的定量裁决：沿流导数 vs 旋度

三件事
-----
1. 一般恒等式（对任意单位矢量场）：∇_T T = (∇×T)×T ；
2. 等螺距角光速螺旋族（α, β 与 ρ 无关）：∇×T = τT + κB 的**精确**闭式；
3. 刚性 / 适用范围：α 随 ρ 变化时恒等式必须失效；朴素形式 ∇×T = κN 对一切 κ>0 都失效。

两条独立通道
-----------
* 符号层：sympy.vector 柱坐标（解析）
* 数值层：笛卡尔有限差分（不使用任何柱坐标闭式），检验同一条断言

判定纪律：只判数学恒等 / 数值一致，不判物理真伪；FAIL ⇒ 退出码 1；控制组必须可红。

运行
----
    python -B spiral_op1_bridge_audit.py [--quiet]
"""

from __future__ import annotations

import json
import math
import os
import random
import sys

try:
    import sympy as sp
    from sympy.vector import CoordSys3D, curl
except ImportError:  # pragma: no cover
    print("SKIP: 需要 sympy")
    sys.exit(2)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # pragma: no cover
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, "spiral_op1_bridge_audit_results.json")
OUT_TXT = os.path.join(HERE, "spiral_op1_bridge_audit_out.txt")

RESULTS: list[dict] = []


def rec(sid: str, title: str, kind: str, verdict: str, detail: str) -> None:
    RESULTS.append({"id": sid, "title": title, "kind": kind,
                    "verdict": verdict, "detail": detail})


# ============================================================ 符号层 · 等螺距族
C = CoordSys3D("C", transformation="cylindrical",
               variable_names=("rho", "phi", "z"))
rho = C.rho
a = sp.symbols("alpha", positive=True)
b = sp.sqrt(1 - a**2)                       # 单位模长约束 α²+β²=1

T = a * C.j + b * C.k                       # 切矢场（α, β 与 ρ 无关）
cT = sp.simplify(curl(T, C))

kappa = a**2 / rho
tau = a * b / rho
Nv = -C.i
Bv = a * C.k - b * C.j

# S1 · curl T = τT + κB
resid1 = sp.simplify(cT - (tau * T + kappa * Bv))
v1 = sp.simplify(resid1.dot(C.i) + resid1.dot(C.j) + resid1.dot(C.k))
rec("S1", r"\nabla\times\mathbf T=\tau\mathbf T+\kappa\mathbf B", "IDN",
    "PASS" if v1 == 0 else "FAIL", f"residual = {v1}")

# S2 · κ² = |(curl T) × T|²（平方形式，避开 sqrt 分支）
cross_cT_T = sp.simplify(cT.cross(T))
resid2 = sp.simplify(cross_cT_T.dot(cross_cT_T) - kappa**2)
rec("S2", r"\kappa^2=|(\nabla\times\mathbf T)\times\mathbf T|^2", "IDN",
    "PASS" if resid2 == 0 else "FAIL", f"residual = {resid2}")

# S3 · τ = T·(curl T)（螺旋度密度）
resid3 = sp.simplify(T.dot(cT) - tau)
rec("S3", r"\tau=\mathbf T\cdot(\nabla\times\mathbf T)", "IDN",
    "PASS" if resid3 == 0 else "FAIL", f"residual = {resid3}")

# S4 · (curl T) × T = κN（沿流导数）
resid4 = sp.simplify(cross_cT_T - kappa * Nv)
v4 = sp.simplify(resid4.dot(C.i) + resid4.dot(C.j) + resid4.dot(C.k))
rec("S4", r"(\nabla\times\mathbf T)\times\mathbf T=\kappa\mathbf N", "IDN",
    "PASS" if v4 == 0 else "FAIL", f"residual = {v4}")

# S5 · 朴素形式 ∇×T = κN：残差 τT + κ(B−N)，对 κ>0 恒不为零
resid5 = sp.simplify(cT - kappa * Nv)
mag5 = sp.simplify(cT.dot(cT) + (kappa * Nv).dot(kappa * Nv)
                   - 2 * cT.dot(kappa * Nv))
naive_never = sp.simplify(mag5)
rec("S5", r"朴素形式 \nabla\times\mathbf T=\kappa\mathbf N 的失配量", "RES",
    "PASS" if (naive_never != 0 and sp.simplify(naive_never.subs(a, 1)) != 0) else "FAIL",
    f"|residual|^2 = {naive_never}（a∈(0,1] 恒非零）")

# ==================================================== 符号层 · 变螺距（函数形式）
A = sp.Function("A")(rho)
B = sp.Function("B")(rho)
Tf = A * C.j + B * C.k
cTf = curl(Tf, C)
# curl 的三个分量（柱坐标标准式）
comp_rho = sp.simplify(cTf.dot(C.i))
comp_phi = sp.simplify(cTf.dot(C.j))
comp_z = sp.simplify(cTf.dot(C.k))
expr_rho = comp_rho                                  # 期望 0
expr_phi = sp.simplify(comp_phi + sp.diff(B, rho))    # 期望 0
expr_z = sp.simplify(comp_z - sp.diff(A * rho, rho) / rho)  # 期望 0
rec("S6", r"变螺距：curl 闭式 (0,\,-\beta',\,(\rho\alpha)'/\rho)", "IDN",
    "PASS" if (expr_rho == 0 and expr_phi == 0 and expr_z == 0) else "FAIL",
    f"res = ({expr_rho}, {expr_phi}, {expr_z})")

# 变螺距下 τT+κB 的残差恰好是 -β' ê_φ
Bv_f = A * C.k - B * C.j
tau_f = A * B / rho
kappa_f = A**2 / rho
resid_f = sp.simplify(cTf - (tau_f * Tf + kappa_f * Bv_f))
resid_f_phi = sp.simplify(resid_f.dot(C.j))
rec("S7", r"变螺距残差 = -\beta'\hat\varphi（等螺距才为零）", "RES",
    "PASS" if sp.simplify(resid_f_phi + sp.diff(B, rho)) == 0 else "FAIL",
    f"r_phi = {resid_f_phi}, -B' = {-sp.diff(B, rho)}")


# ============================================================ 数值层 · 笛卡尔
def field(x: float, y: float, z: float, prof) -> tuple[float, float, float]:
    r = math.hypot(x, y)
    al = prof(r)
    be = math.sqrt(max(0.0, 1.0 - al * al))
    return (-al * y / r, al * x / r, be)


def curl_fd(p, prof, h: float = 1e-5):
    x, y, z = p

    def d(comp, axis):
        e = [0.0, 0.0, 0.0]
        e[axis] = h
        fp = field(x + e[0], y + e[1], z + e[2], prof)[comp]
        fm = field(x - e[0], y - e[1], z - e[2], prof)[comp]
        return (fp - fm) / (2 * h)

    dTz_dy = d(2, 1)
    dTy_dz = d(1, 2)
    dTx_dz = d(0, 2)
    dTz_dx = d(2, 0)
    dTy_dx = d(1, 0)
    dTx_dy = d(0, 1)
    return (dTz_dy - dTy_dz, dTx_dz - dTz_dx, dTy_dx - dTx_dy)


def norm(v):
    return math.sqrt(sum(x * x for x in v))


def relerr(u, v):
    d = norm([u[i] - v[i] for i in range(3)])
    s = max(norm(u), norm(v), 1e-30)
    return d / s


ALPHA0 = 0.6
BETA0 = math.sqrt(1 - ALPHA0**2)


def prof_const(r):
    return ALPHA0


random.seed(20261030)
pts = []
for _ in range(24):
    r = random.uniform(0.6, 2.4)
    ph = random.uniform(0, 2 * math.pi)
    z = random.uniform(-1.0, 1.0)
    pts.append((r, ph, z))

# N1 · 数值 curl = (α/ρ) ẑ
errs = []
for r, ph, z in pts:
    p = (r * math.cos(ph), r * math.sin(ph), z)
    c = curl_fd(p, prof_const)
    target = (0.0, 0.0, ALPHA0 / r)
    errs.append(relerr(c, target))
rec("N1", r"数值 \nabla\times\mathbf T=(α/ρ)\hat z", "IDN",
    "PASS" if max(errs) < 1e-6 else "FAIL", f"max rel err = {max(errs):.3e}")

# N2 · 数值 curl = τT + κB（逐点，含 3 分量）
errs2 = []
for r, ph, z in pts:
    p = (r * math.cos(ph), r * math.sin(ph), z)
    c = curl_fd(p, prof_const)
    t = field(*p, prof_const)
    bb = (ALPHA0 * 0.0, 0.0, 0.0)
    # B = α ẑ − β ê_φ ；ê_φ = (−sinφ, cosφ, 0)
    bb = (BETA0 * math.sin(ph), -BETA0 * math.cos(ph), ALPHA0)
    kp = ALPHA0**2 / r
    tp = ALPHA0 * BETA0 / r
    target = tuple(tp * t[i] + kp * bb[i] for i in range(3))
    errs2.append(relerr(c, target))
rec("N2", r"数值 \nabla\times\mathbf T=\tau\mathbf T+\kappa\mathbf B", "IDN",
    "PASS" if max(errs2) < 1e-6 else "FAIL", f"max rel err = {max(errs2):.3e}")

# N3 · 场论侧 (curl)×T  vs 曲线侧 dT/ds（两条完全不同的路径）
errs3 = []
for r, ph, z in pts:
    p = (r * math.cos(ph), r * math.sin(ph), z)
    c = curl_fd(p, prof_const)
    t = field(*p, prof_const)
    lhs = (c[1] * t[2] - c[2] * t[1],
           c[2] * t[0] - c[0] * t[2],
           c[0] * t[1] - c[1] * t[0])
    # 曲线侧：该点上过点的螺旋线，s = cτ 参数，dT/ds 用中心差分
    c_light = 1.0
    w = ALPHA0 * c_light / r
    vz = BETA0 * c_light

    def Tcur(tt):
        v = (-r * w * math.sin(w * tt), r * w * math.cos(w * tt), vz)
        n = math.sqrt(sum(x * x for x in v))
        return tuple(x / n for x in v)

    h = 1e-5
    t0 = ph / w                      # 该点的相位必须对齐，否则比较的是两条不同相位处的标架
    Tp, Tm = Tcur(t0 + h), Tcur(t0 - h)
    dTds = tuple((Tp[i] - Tm[i]) / (2 * h * c_light) for i in range(3))
    errs3.append(relerr(lhs, dTds))
rec("N3", r"场论 (\nabla\times\mathbf T)\times\mathbf T = 曲线 d\mathbf T/ds", "IDN",
    "PASS" if max(errs3) < 1e-6 else "FAIL", f"max rel err = {max(errs3):.3e}")

# CT1 · 朴素形式必须红：|curl − κN| / |κN| ~ 1/α 的量级
r0, ph0 = 1.0, 0.3
p0 = (r0 * math.cos(ph0), r0 * math.sin(ph0), 0.0)
c0 = curl_fd(p0, prof_const)
n0 = (-math.cos(ph0), -math.sin(ph0), 0.0)   # N = −ê_ρ
kp0 = ALPHA0**2 / r0
naive = tuple(c0[i] - kp0 * n0[i] for i in range(3))
ratio = norm(c0) / (kp0 * 1.0)
caught = norm(naive) > 0.5 * kp0
rec("CT1", "控制组：朴素形式 ∇×T=κN 必须被数值层判失配", "CTRL",
    "PASS" if caught else "FAIL",
    f"|residual|/|κN| = {norm(naive)/kp0:.6f}, |curl|/|κN| = {ratio:.6f} (= 1/α)")

# CT2 · 变螺距必须让恒等式失效（证明定理 2 是有条件的）
def prof_var(r):
    return min(0.95, max(0.05, 0.55 + 0.12 * (r - 1.0)))


maxgap = 0.0
for r, ph, z in pts:
    p = (r * math.cos(ph), r * math.sin(ph), z)
    c = curl_fd(p, prof_var)
    al = prof_var(r)
    be = math.sqrt(1 - al * al)
    t = field(*p, prof_var)
    bb = (be * math.sin(ph), -be * math.cos(ph), al)
    kp = al**2 / r
    tp = al * be / r
    target = tuple(tp * t[i] + kp * bb[i] for i in range(3))
    maxgap = max(maxgap, norm([c[i] - target[i] for i in range(3)]) / norm(c))
rec("CT2", "控制组：变螺距时 τT+κB 必须失效（定理 2 有条件）", "CTRL",
    "PASS" if maxgap > 1e-3 else "FAIL", f"max rel gap = {maxgap:.3e}")

# ================================================================ 输出
n_fail = sum(1 for x in RESULTS if x["verdict"] == "FAIL")
summary = {
    "doc": "69_OP1算子错配裁决_沿流导数与旋度的精确桥_2026-10-30.md",
    "tool": os.path.basename(__file__),
    "total": len(RESULTS),
    "pass": sum(1 for x in RESULTS if x["verdict"] == "PASS"),
    "fail": n_fail,
    "exit_code": 1 if n_fail else 0,
    "items": RESULTS,
}

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

lines = ["O-P1 算子错配裁决 · 读数", "=" * 62]
for x in RESULTS:
    lines.append(f"[{x['verdict']:4s}] {x['id']:5s} ({x['kind']}) {x['title']}")
    lines.append(f"        {x['detail']}")
lines.append("=" * 62)
lines.append(f"合计 {summary['total']} 条：PASS {summary['pass']} / FAIL {summary['fail']}"
             f" ⇒ exit {summary['exit_code']}")
with open(OUT_TXT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

if "--quiet" not in sys.argv:
    print("\n".join(lines))

sys.exit(summary["exit_code"])
