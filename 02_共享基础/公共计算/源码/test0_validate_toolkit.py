# -*- coding: utf-8 -*-
"""test0_validate_toolkit.py —— 用 Schwarzschild / FLRW 已知解析结果校验 gr_toolkit。"""
import sympy as sp
from gr_toolkit import (christoffel, ricci_tensor, ricci_scalar,
                        einstein_tensor, cov_div_general)

# ============ 自检 1：Schwarzschild（真空解，R_munu=0, R=0）============
t, r, th, ph = sp.symbols('t r theta phi', positive=True)
M, rs = sp.symbols('M r_s', positive=True)
x4 = [t, r, th, ph]
g_sc = sp.Matrix([
    [-(1 - rs / r), 0, 0, 0],
    [0, 1 / (1 - rs / r), 0, 0],
    [0, 0, r**2, 0],
    [0, 0, 0, r**2 * sp.sin(th)**2],
])
ginv_sc = g_sc.inv()
G_sc = christoffel(x4, g_sc, ginv_sc)
Ric_sc = ricci_tensor(x4, g_sc, ginv_sc, G_sc)
R_sc = ricci_scalar(x4, g_sc, ginv_sc, Ric_sc)
print("=== 自检 1：Schwarzschild ===")
print("Ricci 标量 R =", sp.simplify(R_sc), " (应为 0)")
print("Ricci 张量分量非零个数（应为 0）:",
      sum(1 for i in range(4) for j in range(4) if sp.simplify(Ric_sc[i][j]) != 0))

# ============ 自检 2：FLRW（已知 R 与 Friedmann 方程）============
t2 = sp.symbols('t2')  # 独立的 FLRW 时间坐标（避免与上面 t 冲突）
a = sp.Function('a')(t2)
x4b = [t2, x, y, z] = [t2, sp.symbols('x'), sp.symbols('y'), sp.symbols('z')]
# 平直 FLRW: ds2 = -dt^2 + a(t)^2 (dx^2+dy^2+dz^2)
g_frw = sp.Matrix([
    [-1, 0, 0, 0],
    [0, a**2, 0, 0],
    [0, 0, a**2, 0],
    [0, 0, 0, a**2],
])
ginv_frw = g_frw.inv()
G_frw = christoffel(x4b, g_frw, ginv_frw)
Ric_frw = ricci_tensor(x4b, g_frw, ginv_frw, G_frw)
R_frw = ricci_scalar(x4b, g_frw, ginv_frw, Ric_frw)
expect = 6 * (sp.diff(a, t2, 2) / a + sp.diff(a, t2)**2 / a**2)
print("=== 自检 2：FLRW ===")
print("计算 R =", R_frw)
print("期望 R =", sp.simplify(expect))
print("差 =", sp.simplify(R_frw - expect), " (应为 0)")
# 时空分量 Ricci: R_tt = -3 a''/a
Rtt_expect = -3 * sp.diff(a, t2, 2) / a
print("R_tt 差 =", sp.simplify(Ric_frw[0][0] - Rtt_expect), " (应为 0)")
# 空间分量: R_ij = (a a'' + 2 a'^2) delta_ij
Rxx_expect = (a * sp.diff(a, t2, 2) + 2 * sp.diff(a, t2)**2)
print("R_xx 差 =", sp.simplify(Ric_frw[1][1] - Rxx_expect), " (应为 0)")

# ============ 自检 3：Bianchi 恒等式 div(G)=0（FLRW）============
Gt_frw = einstein_tensor(x4b, g_frw, ginv_frw, Ric_frw)
# 上升指标
Guu = [[sum(ginv_frw[m, a] * ginv_frw[n, b] * Gt_frw[a][b]
            for a in range(4) for b in range(4)) for n in range(4)] for m in range(4)]
divG = cov_div_general(x4b, g_frw, ginv_frw, G_frw, Guu)
print("=== 自检 3：Bianchi  div(G)=0（FLRW）===")
print("div(G)^nu 分量（应全为 0）:", [sp.simplify(v) for v in divG])

# ============ 自检 4：delta sqrt(-g) 恒等式（数值校验）============
#   delta sqrt(-g) = +1/2 sqrt(-g) g^{munu} delta g_munu
# 取具体度规 g = diag(-1,2,3,4)，做小扰动 dg，两边数值对比。
import numpy as np
gg_n = np.diag([-1.0, 2.0, 3.0, 4.0])
eps = 1e-7
rng = np.random.default_rng(42)
dgg_n = np.diag(rng.uniform(-1, 1, 4))
sg0 = np.sqrt(-np.linalg.det(gg_n))
sg1 = np.sqrt(-np.linalg.det(gg_n + eps * dgg_n))
lhs_num = (sg1 - sg0) / eps
rhs_num = 0.5 * sg0 * np.trace(np.linalg.inv(gg_n) @ dgg_n)
print("=== 自检 4：delta sqrt(-g) = 1/2 sqrt(-g) g^{munu} delta g_munu（数值）===")
print("LHS =", lhs_num, " RHS =", rhs_num, " 相对误差 =", abs(lhs_num - rhs_num) / abs(rhs_num))

print("\n全部自检完成。")
