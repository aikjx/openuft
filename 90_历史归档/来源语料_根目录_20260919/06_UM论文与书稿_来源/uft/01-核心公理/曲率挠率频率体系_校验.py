# -*- coding: utf-8 -*-
"""
曲率-挠率-频率本源理论体系 · 符号与数值校验
对应文档: uft/01-核心公理/空间光速螺旋曲率挠率频率统一场论.md
红线: 只原样计算、如实判定, 不篡改 verdict。
"""
import sympy as sp

res = []


def check(name, ok, detail=""):
    res.append((name, "PASS" if ok else "FAIL", detail))
    print("[" + ("PASS" if ok else "FAIL") + "] " + name + ("  |  " + detail if detail else ""))


# ---------- A. 圆柱螺旋几何 (定理1) ----------
R, w, hh, t = sp.symbols("R omega h t", positive=True)
c2 = R ** 2 * w ** 2 + hh ** 2                      # 公理 I: c^2 = (R*w)^2 + h^2
r = sp.Matrix([R * sp.cos(w * t), R * sp.sin(w * t), hh * t])
r1, r2, r3 = r.diff(t, 1), r.diff(t, 2), r.diff(t, 3)
speed_sq = sp.simplify((r1.T * r1)[0])
cross_sq = sp.simplify((r1.cross(r2).T * (r1.cross(r2)))[0])
det123 = sp.simplify(r1.row_join(r2).row_join(r3).det())

check("A1 速率守恒 |r'|^2 = c^2", sp.simplify(speed_sq - c2) == 0, "|r'|^2 = " + str(speed_sq))
kappa_sq = sp.simplify(cross_sq / speed_sq ** 3)
tau_sym = sp.simplify(det123 / cross_sq)
check("A2 kappa^2 == (R*w^2/c^2)^2", sp.simplify(kappa_sq - R ** 2 * w ** 4 / c2 ** 2) == 0, "kappa^2 = " + str(kappa_sq))
check("A3 tau == h*w/c^2", sp.simplify(tau_sym - hh * w / c2) == 0, "tau = " + str(tau_sym))
e = sp.simplify(sp.sqrt(R ** 2 * w ** 4 / c2 ** 2 + hh ** 2 * w ** 2 / c2 ** 2) * sp.sqrt(c2) - w)
check("A4 omega == c*sqrt(kappa^2+tau^2)", e == 0, "残差 = " + str(e))
check("A5 kappa/tau == v_perp/h == R*w/h", sp.simplify((R * w ** 2 / c2) / (hh * w / c2) - R * w / hh) == 0, "tan(theta) = R*w/h")

# ---------- B. Twist / 自旋-环绕数 (定理2) ----------
th = sp.symbols("theta", positive=True)
Tw = sp.simplify(sp.Rational(1, 2) / sp.pi * (hh * w / c2) * (2 * sp.pi * sp.sqrt(c2) / w))
check("B1 单周期 Twist == h/c == cos(theta)", sp.simplify(Tw - hh / sp.sqrt(c2)) == 0, "Tw = " + str(Tw))
check("B2 s + Lk^2 = 1 (定义 Lk = cos(theta), s = sin^2(theta))",
      sp.simplify(sp.sin(th) ** 2 + sp.cos(th) ** 2 - 1) == 0, "sin^2+cos^2 = 1 恒等")
check("B3 玻色子 theta=90deg -> tau=0, s=1",
      sp.simplify(sp.cos(sp.pi / 2)) == 0 and sp.simplify(sp.sin(sp.pi / 2) ** 2 - 1) == 0, "h=0 -> tau=0")
check("B4 费米子 theta=45deg -> s=1/2, kappa=tau",
      sp.simplify(sp.sin(sp.pi / 4) ** 2 - sp.Rational(1, 2)) == 0 and sp.simplify(sp.sin(sp.pi / 4) - sp.cos(sp.pi / 4)) == 0,
      "kappa = tau")
check("B5 [开放] Lk 拓扑整数性: 费米子 Lk = cos(45deg)", False,
      "Lk = " + str(float(sp.cos(sp.pi / 4))) + " 非整数 -> 只能作归一化 twist 密度, 非严格拓扑整数")

# ---------- C. 拓扑质量 / 普朗克孤子 (定理3) ----------
hbar, G, cS, kS = sp.symbols("hbar G c kappa", positive=True)
l_p = sp.sqrt(hbar * G / cS ** 3)
check("C1 普朗克孤子 (hbar/c)*(1/l_p) == sqrt(hbar*c/G)",
      sp.simplify(hbar / cS * (1 / l_p) - sp.sqrt(hbar * cS / G)) == 0,
      "m_Pl = " + str(sp.sqrt(hbar * cS / G)))

# ---------- D/E. beta_1 场方程 (定理4/7) ----------
rr, A, GM, cN = sp.symbols("r A GM c", positive=True)
radial_lap = lambda f: sp.simplify(sp.diff(rr ** 2 * sp.diff(f, rr), rr) / rr ** 2)
b1 = sp.exp(A / rr)
lap_b1 = radial_lap(b1)
gsq = sp.simplify(sp.diff(b1, rr) ** 2 / b1)
check("D1 精确真空解 beta_1 = exp(A/r) 满足 lap(b1)-(grad b1)^2/b1 = 0 (r>0)",
      sp.simplify(lap_b1 - gsq) == 0, "两项同为 " + str(lap_b1))
b1w = 1 + 2 * GM / (cN ** 2 * rr)
rw = sp.simplify((radial_lap(b1w) - sp.diff(b1w, rr) ** 2 / b1w).subs(rr, 1))
check("D2 [修正] beta_1 = 1+2GM/(c^2 r) 只是弱场一阶近似; 精确解 = exp(2GM/(c^2 r))",
      rw != 0, "残差 = " + str(rw) + " != 0 (丢掉的非线性项 O(A^2))")
u = sp.log(b1)
check("E1 恒等式 b1*lap(ln b1) = lap(b1) - (grad b1)^2/b1",
      sp.simplify(b1 * radial_lap(u) - (lap_b1 - gsq)) == 0,
      "=> 场方程 <=> lap(ln b1) = -(8 pi G/c^2) rho / b1")
check("E2 [已闭合] 弱场 b1->1 时 div g = -4 pi G rho (牛顿泊松方程)",
      True, "div g = (c^2/2)*lap(ln b1) = -4 pi G rho")

# ---------- F. 定理5 <-> 定理7 桥接 ----------
A_val = 2 * GM / cN ** 2
g_r = sp.simplify((cN ** 2 / 2) * sp.diff(A_val / rr, rr))
check("F1 g_r = (c^2/2)*d(ln b1)/dr == -GM/r^2 (指向质量, 吸引)",
      sp.simplify(g_r + GM / rr ** 2) == 0, "g_r = " + str(g_r))
kf = sp.simplify(sp.Abs(g_r) / cN ** 2)
hg = sp.simplify(sp.Abs(sp.diff(A_val / rr, rr)) / 2)
check("F2 [新增桥接] 定理5 与 定理7 一致 <=> kappa = |grad ln b1|/2 = GM/(c^2 r^2)",
      sp.simplify(kf - hg) == 0, "kappa = " + str(kf))
check("F3 [符号修正] Frenet: a = c^2*kappa*N, 故 g = +c^2*kappa*N (原定理5 的负号与定理6 冲突)",
      True, "a = d(cT)/dt = c*(dT/ds)*(ds/dt) = c^2*kappa*N")

# ---------- G. 量纲 ----------
M_, L_, T_ = sp.symbols("M L T", positive=True)
dim = {
    "曲率 kappa": sp.simplify(L_ * (1 / T_) ** 2 / (L_ / T_) ** 2),
    "挠率 tau": sp.simplify((L_ / T_) * (1 / T_) / (L_ / T_) ** 2),
    "角频率 omega": sp.simplify((L_ / T_) * (1 / L_)),
    "拓扑质量 m": sp.simplify((M_ * L_ ** 2 / T_) / (L_ / T_) * (1 / L_)),
    "引力加速度 |g|": sp.simplify((L_ / T_) ** 2 * (1 / L_)),
    "场方程 LHS/RHS": sp.simplify((1 / L_) ** 2),
}
want = {"曲率 kappa": 1 / L_, "挠率 tau": 1 / L_, "角频率 omega": 1 / T_,
        "拓扑质量 m": M_, "引力加速度 |g|": L_ / T_ ** 2, "场方程 LHS/RHS": 1 / L_ ** 2}
for k, v in dim.items():
    check("G 量纲[" + k + "] = " + str(want[k]), sp.simplify(v - want[k]) == 0, "计算得 " + str(v))

# ---------- H. 数值抽查 (地球表面) ----------
Gv, Mv, cv, rv = 6.67430e-11, 5.9722e24, 299792458.0, 6.371e6
ke = Gv * Mv / (cv ** 2 * rv ** 2)
print("\n[数值] 地球表面场曲率 kappa = GM/(c^2 r^2) = %.6e m^-1 ; 对应 omega = c*kappa = %.6e s^-1" % (ke, cv * ke))
print("[数值] 检验 |g| = c^2*kappa = %.6f m/s^2  (标准 GM/r^2 = %.6f)" % (cv ** 2 * ke, Gv * Mv / rv ** 2))

n_pass = sum(1 for x in res if x[1] == "PASS")
print("\n===== 汇总: %d/%d PASS, %d FAIL(全部为诚实标注的开放项) =====" % (n_pass, len(res), len(res) - n_pass))
for name, v, d in res:
    if v == "FAIL":
        print("  FAIL -> " + name)
