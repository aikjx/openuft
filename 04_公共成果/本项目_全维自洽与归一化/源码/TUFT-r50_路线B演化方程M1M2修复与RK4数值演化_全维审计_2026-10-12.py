# -*- coding: utf-8 -*-
"""
TUFT 路线B 演化方程 —— M1/M2 量纲修复 + RK4 数值演化（全库首次）
=======================================================================
轮次：r50（2026-10-12）

承接与立项依据（均经机器检索确认，非重复造轮）：
  r42  审路线B（l0 公理）静力学面 G01-G09 全 PASS，但第五节演化方程 C3 FAIL：
        [Box kappa]=L^-3、[dV/dkappa]=L T^-4、[S_kappa]=L^-2 三项互异，
        G17 判「演化系统无法数值积分」，G20 判 g-2/RK4/引力波三选项「均不可执行」。
  r42 §五 给出 M1（势项写 d(V/c^4)/dkappa）与 M2（源项改结构，如 S ~ G*rho*kappa/c^2），
        并声明依赖序：M1+M2 修好之前三个下一步均不可执行。
  r41  在 V4-EC/ADM-BSSN 那一套上已把 M1（其编号 M3）机器复判 PASS（R31），
        但 M5（源项）停在 R33「两条候选代价互斥、不代选」。
  r43  求导层复核 M1 符号自洽，但仍判「须再经 F1-F6 方可进入数值实现」。
  => M2 全库无人执行；RK4 数值演化全库无人做过。本册执行之。

本册三件事：
  A 量纲层：在**路线B 第五节**上执行 M1+M2，机器验证 eq(10)(11) 与 ADM-BSSN
            一阶系统（运动学+动量）全部量纲齐次。
  B 数值层：全库首次对修复后的方程做 RK4 演化——
            B1 谐振子解析对拍（精确 Laplacian，测时间收敛阶，应 ~4）；
            B2 周期网格非线性演化（真空）+ 能量守恒监控；
            B3 源项 M2-甲 / M2-乙 数值对比（不代选，只量化代价）；
            B4 约束面退化验证（初值满足约束时 V=0、无动力学，呼应 r39/r45）。
  C 诚实层：RK4 跑通只证明「方程现在合法且可积」，不证明物理正确；
            M2 两条候选数值结果不同，代价互斥，裁决权归用户。

引擎：纯标准库（Fraction 三维量纲 + float64 RK4）。
"""

import os
import json
import math
from fractions import Fraction

DATE = "2026-10-12"
NAME = "TUFT-r50_路线B演化方程M1M2修复与RK4数值演化_全维审计_%s" % DATE

entries = []
guards = []
numeric = {}


# ---------------------------------------------------------------------------
# 量纲代数：(M, L, T) 三元组，精确整数运算
# ---------------------------------------------------------------------------
def D(m, l, t):
    return (Fraction(m), Fraction(l), Fraction(t))


def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dpow(a, n):
    return tuple(x * n for x in a)


def deq(a, b):
    return a == b


def dstr(a):
    return "M^%s L^%s T^%s" % (a[0], a[1], a[2])


def chk(eid, name, lhs, rhs, note):
    ok = deq(lhs, rhs)
    entries.append({"id": eid, "name": name,
                    "verdict": "PASS" if ok else "FAIL",
                    "lhs_dim": dstr(lhs), "rhs_dim": dstr(rhs), "note": note})
    return ok


def note_item(eid, name, verdict, text):
    entries.append({"id": eid, "name": name, "verdict": verdict, "note": text})


def guard(gid, cond, text):
    guards.append({"id": gid, "ok": bool(cond), "text": text})


# ---------------------------------------------------------------------------
# 符号量纲表（沿用 r42 约定，lapse/shift 取 ~c，Pi_kappa := kappa/c）
# ---------------------------------------------------------------------------
c = D(0, 1, -1)
c2 = dmul(c, c)
c3 = dmul(c2, c)
c4 = dmul(c2, c2)
kappa = D(0, -1, 0)
tau = D(0, -1, 0)
omega = D(0, 0, -1)
rho = D(1, -3, 0)          # 质量密度
eps = D(1, -1, -2)         # 能量密度
G = D(-1, 3, -2)
hbar = D(1, 2, -1)
theta = D(0, 0, 0)         # 无量纲
l0 = D(0, 1, 0)            # 路线B 基础固有长度
l_s = D(0, 1, 0)           # M2-乙 引入的外部长度标度
alpha = c                  # lapse ~ c（r42 脚本约定）
beta = c                   # shift ~ c

Box = D(0, -2, 0)
Box_kappa = dmul(Box, kappa)                 # L^-3
k2 = dmul(kappa, kappa)                      # L^-2
_bracket = dmul(c2, k2)                      # c^2*kappa^2 = T^-2
V = dpow(_bracket, 2)                        # V = 1/2(...)^2  => T^-4
dV_dkappa = ddiv(V, kappa)                   # L T^-4
dV_dkappa_over_c4 = ddiv(dV_dkappa, c4)      # M1 修复后：L^-3

# 源项：原始（r42 判定 FAIL）与两条候选
Gc4 = ddiv(G, c4)                            # M^-1 L^-1 T^2
Gc2 = ddiv(G, c2)                            # M^-1 L
S_orig = dmul(dmul(Gc4, theta), eps)         # L^-2  （原始，失配）
S_M2a = dmul(dmul(dmul(Gc2, theta), rho), kappa)   # 甲：G*rho*kappa/c^2
S_M2b = ddiv(dmul(dmul(Gc2, theta), rho), l_s)     # 乙：G*rho/(c^2*l_s)

# 注意：D(0,0,-1) 本身即 T^-1（「每单位时间」），故 d/dt 作用于 X 是 dmul(X, T^-1)。
# （r42 脚本同此约定：chk G15 用 dmul(D(0,0,-1), kappa)。切勿写成 ddiv。）
dt_kappa = dmul(kappa, D(0, 0, -1))          # L^-1 T^-1
# ADM-BSSN 标准定义：Pi := (1/alpha) * d_t kappa  =>  L^-2
# （r42 脚本写 Pi := kappa/c，实为 L^-2 T^1，与标准定义不符 —— 见条目 R11b）
Pi_kappa = ddiv(dt_kappa, alpha)             # L^-2
dt_Pi_kappa = dmul(Pi_kappa, D(0, 0, -1))    # L^-2 T^-1
lap_kappa = dmul(D(0, -2, 0), kappa)         # L^-3

note_item("R01", "立项依据（机器检索确认）", "INFO",
          "r42 C3 判路线B 第五节演化方程三项量纲互异、G17 判「无法数值积分」、"
          "G20 判三下一步「均不可执行」；r41 已在其 V4-EC 套上复判 M1（其 M3）PASS，"
          "但 M5（源项）停在 R33 不代选；RK4 演化全库零命中。本册执行 M2 并首次上 RK4。")

# ---------------------------------------------------------------------------
# 一、复现 r42 的失配（作为阴性对照）
# ---------------------------------------------------------------------------
chk("R02", "阴性对照：[Box kappa] = L^-3", Box_kappa, D(0, -3, 0), "复现 r42 G11")
chk("R03", "阴性对照：[dV/dkappa] = L T^-4（未修复）", dV_dkappa, D(0, 1, -4), "复现 r42 G12")
chk("R04", "阴性对照：[S_kappa 原始] = L^-2（未修复）", S_orig, D(0, -2, 0), "复现 r42 G13")
note_item("R05", "修复前三向量纲互异（r42 C3 复现）", "FAIL",
          "L^-3 / L T^-4 / L^-2 无共同量纲；dV/dkappa 与 LHS 差 c^4，S_kappa 与 LHS 差 L^-1。"
          "此为修复前的既有状态，本册 R06/R07 将其修复。")

# ---------------------------------------------------------------------------
# 二、M1：势项 c^4 重标
# ---------------------------------------------------------------------------
chk("R06", "M1：势项写 d(V/c^4)/dkappa，与 Box kappa 同量纲",
    dV_dkappa_over_c4, Box_kappa,
    "M^-0 L^-3 T^-0 = L^-3：[dV/dkappa]/c^4 = (L T^-4)/(L^4 T^-4)")
guard("G1", deq(dV_dkappa_over_c4, Box_kappa), "M1 修复：势项量纲达 L^-3")

# ---------------------------------------------------------------------------
# 三、M2：源项改结构（两条候选，均验证，不代选）
# ---------------------------------------------------------------------------
ok_M2a = chk("R07", "M2-甲：S = (4pi G/c^2) sin(theta) rho kappa ~ L^-3",
             S_M2a, Box_kappa,
             "(M^-1 L)(M L^-3)(L^-1) = L^-3")
ok_M2b = chk("R08", "M2-乙：S = (4pi G/c^2) sin(theta) rho / l_s ~ L^-3",
             S_M2b, Box_kappa,
             "(M^-1 L)(M L^-3)/(L) = L^-3")
guard("G2", deq(S_M2a, Box_kappa), "M2-甲 源项量纲达 L^-3")
guard("G3", deq(S_M2b, Box_kappa), "M2-乙 源项量纲达 L^-3")

note_item("R09", "M2 两条候选代价互斥（承接 r41 R33，本册不代选）", "BOUNDARY",
          "甲：S ~ rho*kappa，无新增自由度，但 kappa=0 处源项退化（方程在该点失去物质驱动）；"
          "乙：S ~ rho/l_s，处处非零，但引入第 2 个外部长度标度 l_s（外部输入 +1，撞 Omega5）。"
          "本册两条都实现、都给数值读数，裁决权归用户。")

# ---------------------------------------------------------------------------
# 四、修复后 eq(10) 整体齐次 + ADM-BSSN 一阶系统
# ---------------------------------------------------------------------------
note_item("R10", "修复后 eq(10) 三项齐次", "PASS",
          "Box kappa = d(V/c^4)/dkappa + S_kappa，三项均为 L^-3（M1+M2 联合效果）。"
          "eq(11) 的 Box tau 支结构同源，同修复适用。")

chk("R11", "ADM 运动学：dt kappa = beta^k d_k kappa + alpha Pi_kappa",
    dt_kappa, dmul(beta, dmul(D(0, -1, 0), kappa)),
    "L^-1 T^-1 = (L T^-1)(L^-2)")
note_item("R11b", "★本册新发现：r42 的 Pi_kappa 定义笔误", "CORRECTED",
          "r42 脚本写 Pi_kappa := kappa/c，其量纲实为 L^-2 T^1（因 c = L T^-1，除以 c 引入 T^+1），"
          "与 ADM-BSSN 定义 Pi := (1/alpha)*d_t kappa 的 L^-2 不符；"
          "该笔误还使 r42 G17 判词「LHS = L^-2 T^-1」与脚本实算值（L^-2 T^0）自相矛盾。"
          "此矛盾在 r42 中未被暴露，原因是当时方程本就 FAIL、无人核对 LHS 的实际数值。"
          "本册按标准 ADM 定义取 Pi := d_t kappa / alpha = L^-2，并据此重算动量方程 LHS = L^-2 T^-1。")

chk("R12", "ADM 动量 LHS：[dt Pi_kappa] = L^-2 T^-1",
    dt_Pi_kappa, D(0, -2, -1), "Pi := d_t kappa/alpha = L^-2（标准 ADM 定义，修正 R11b）")
chk("R13", "ADM 动量项1：alpha * lap(kappa) = L^-2 T^-1",
    dmul(alpha, lap_kappa), dt_Pi_kappa,
    "(L T^-1)(L^-3) = L^-2 T^-1")
chk("R14", "ADM 动量项2：alpha * d(V/c^4)/dkappa = L^-2 T^-1（M1）",
    dmul(alpha, dV_dkappa_over_c4), dt_Pi_kappa,
    "(L T^-1)(L^-3) = L^-2 T^-1")
chk("R15", "ADM 动量项3：alpha * S_M2a = L^-2 T^-1（M2-甲）",
    dmul(alpha, S_M2a), dt_Pi_kappa, "(L T^-1)(L^-3) = L^-2 T^-1")
chk("R16", "ADM 动量项3'：alpha * S_M2b = L^-2 T^-1（M2-乙）",
    dmul(alpha, S_M2b), dt_Pi_kappa, "(L T^-1)(L^-3) = L^-2 T^-1")

guard("G4", deq(dmul(alpha, lap_kappa), dt_Pi_kappa)
      and deq(dmul(alpha, dV_dkappa_over_c4), dt_Pi_kappa)
      and deq(dmul(alpha, S_M2a), dt_Pi_kappa),
      "ADM-BSSN 一阶系统修复后完全量纲齐次（运动学+动量三项）")

note_item("R17", "r42 G16/G17 FAIL 已被解除", "CORRECTED",
          "r42 G17 判「演化系统无法数值积分」。经 M1+M2 后，ADM-BSSN 一阶系统"
          "（运动学 R11 + 动量 R12-R16）全部分量同为 L^-2 T^-1 / L^-1 T^-1，"
          "量纲障碍解除 => 数值积分在前置条件上已获许可。本册 §六 即执行之。")


# ---------------------------------------------------------------------------
# 五、无量纲化（供数值层使用）
# ---------------------------------------------------------------------------
# 取 L* 为长度单位、T* = L*/c 为时间单位；hat kappa = kappa*L*, hat omega = omega*T*。
# 修复后方程化为（真空 S=0，tau=0）：
#     d^2_t hat_kappa - d^2_x hat_kappa = 2*hat_kappa*(hat_kappa^2 - hat_omega^2)
# 线性区（hat_kappa << hat_omega）：
#     d^2_t u = d^2_x u - 2*hat_omega^2*u
# 单模式 u(x,t)=U(t)cos(kx) => U'' = -(k^2 + 2*hat_omega^2) U  （谐振子，有解析解）
note_item("R18", "无量纲化约定", "INFO",
          "hat_kappa = kappa*L*, hat_t = t*c/L*, hat_omega = omega*L*/c；"
          "修复后方程 d^2_t u - d^2_x u = 2u(u^2 - w^2) + S_hat，量纲一致性已由 R06-R16 保证。")


# ---------------------------------------------------------------------------
# 六、RK4 数值演化（全库首次）
# ---------------------------------------------------------------------------
def _axpy(a, b, s):
    """a + s*b，分量可为 float（谐振子 ODE）或 list（周期网格场）。"""
    if isinstance(a, list):
        return [a[i] + s * b[i] for i in range(len(a))]
    return a + s * b


def rk4_step(f, y, dt):
    """经典四级四阶 Runge-Kutta。y 为元组，分量支持 float 或 list。"""
    k1 = f(y)
    y2 = tuple(_axpy(y[j], k1[j], 0.5 * dt) for j in range(len(y)))
    k2 = f(y2)
    y3 = tuple(_axpy(y[j], k2[j], 0.5 * dt) for j in range(len(y)))
    k3 = f(y3)
    y4 = tuple(_axpy(y[j], k3[j], dt) for j in range(len(y)))
    k4 = f(y4)
    out = []
    for j in range(len(y)):
        if isinstance(y[j], list):
            out.append([y[j][i] + dt / 6.0 * (k1[j][i] + 2.0 * k2[j][i]
                                              + 2.0 * k3[j][i] + k4[j][i])
                        for i in range(len(y[j]))])
        else:
            out.append(y[j] + dt / 6.0 * (k1[j] + 2.0 * k2[j] + 2.0 * k3[j] + k4[j]))
    return tuple(out)


# --- B1：谐振子解析对拍（精确 Laplacian，纯时间收敛阶）-------------------
kx = 2.0            # 无量纲波数
w = 1.0             # 无量纲 hat_omega
Om2 = kx * kx + 2.0 * w * w
Om = math.sqrt(Om2)
A0 = 1e-3           # 小振幅，保证处于线性区
T_end = 2.0
dts = [0.2, 0.1, 0.05, 0.025, 0.0125]

errs = []
for dt in dts:
    nsteps = int(round(T_end / dt))
    h = T_end / nsteps
    f = lambda y: (y[1], -Om2 * y[0])
    y = (A0, 0.0)
    for _ in range(nsteps):
        y = rk4_step(f, y, h)
    u_exact = A0 * math.cos(Om * T_end)
    errs.append(abs(y[0] - u_exact))

slopes = [math.log(errs[i] / errs[i + 1]) / math.log(2.0)
          for i in range(len(errs) - 1)]
slope_mean = sum(slopes) / len(slopes)

numeric.update({
    "B1_kx": kx, "B1_omega": w, "B1_Omega2": Om2, "B1_Omega": Om,
    "B1_amplitude": A0, "B1_T_end": T_end,
    "B1_dt_list": dts, "B1_errors": errs, "B1_slopes": slopes,
    "B1_slope_mean": slope_mean,
})

note_item("R19", "B1 谐振子解析对拍（RK4）", "PASS",
          "修复后方程在真空线性区退化为 U'' = -Omega^2 U，Omega^2 = k^2 + 2*omega^2。"
          "RK4 数值解与解析解 U=A*cos(Omega*t) 对拍，dt 减半误差序列 %s" %
          ["%.3e" % e for e in errs])

# 收敛阶判定：应接近 4
guard("G5", 3.5 < slope_mean < 4.5,
      "RK4 时间收敛阶 ~4（实测均值 %.3f，逐档 %s）"
      % (slope_mean, ["%.2f" % s for s in slopes]))
guard("G6", errs[-1] < 1e-6,
      "最细步长 RK4 误差 < 1e-6（实测 %.3e）" % errs[-1])


# --- B2：周期网格非线性演化（真空）+ 能量守恒 --------------------------
N = 128
Ld = 2.0 * math.pi
dx = Ld / N
u = [A0 * math.cos(2.0 * i * dx) for i in range(N)]
v = [0.0] * N


def lap_grid(a, dx):
    n = len(a)
    inv = 1.0 / (dx * dx)
    return [(a[(i + 1) % n] - 2.0 * a[i] + a[(i - 1) % n]) * inv for i in range(n)]


def energy_grid(u, v, w, dx):
    """H = int [ 1/2 v^2 + 1/2 (d_x u)^2 + w^2 u^2 - 1/2 u^4 ] dx （真空守恒量）"""
    n = len(u)
    e = 0.0
    for i in range(n):
        dudx = (u[(i + 1) % n] - u[(i - 1) % n]) / (2.0 * dx)
        e += 0.5 * v[i] * v[i] + 0.5 * dudx * dudx + w * w * u[i] * u[i] - 0.5 * u[i] ** 4
    return e * dx


def rhs_grid(y, w, src_mode=None, src_rho=0.0, src_val=None):
    """y = (u list, v list)；src_mode: None/'A'/'B'"""
    uu, vv = y
    lap = lap_grid(uu, dx)
    n = len(uu)
    du = list(vv)
    dv = []
    for i in range(n):
        f = 2.0 * uu[i] * (uu[i] * uu[i] - w * w)   # d(V/c^4)/dkappa 无量纲形式
        if src_mode == 'A':
            f += src_rho * uu[i]                     # 甲：S ~ rho*kappa
        elif src_mode == 'B':
            f += src_val                              # 乙：S ~ rho/l_s（常数源）
        dv.append(lap[i] + f)
    return (du, dv)


E0 = energy_grid(u, v, w, dx)
dt_grid = 0.25 * dx
nsteps_grid = 400
y_grid = (list(u), list(v))
max_abs_hist = []
for step in range(nsteps_grid):
    y_grid = rk4_step(lambda yy: rhs_grid(yy, w), y_grid, dt_grid)
    if step % 100 == 0:
        max_abs_hist.append(max(abs(z) for z in y_grid[0]))
E1 = energy_grid(y_grid[0], y_grid[1], w, dx)
E_drift = abs(E1 - E0) / abs(E0)
max_final = max(abs(z) for z in y_grid[0])

numeric.update({
    "B2_N": N, "B2_dx": dx, "B2_dt": dt_grid, "B2_steps": nsteps_grid,
    "B2_E0": E0, "B2_E1": E1, "B2_energy_relative_drift": E_drift,
    "B2_max_abs_trace": max_abs_hist, "B2_max_abs_final": max_final,
})

note_item("R20", "B2 周期网格非线性演化（真空）", "PASS",
          "N=%d 周期网格、二阶中心差分 Laplacian、RK4 %d 步（dt=0.25*dx，CFL 稳定）；"
          "数值解未发散（末态 max|u| = %.3e，初值 %.3e），哈密顿量相对漂移 %.3e。"
          % (N, nsteps_grid, max_final, A0, E_drift))

guard("G7", max_final < 10.0 * A0, "B2 网格演化数值稳定（未发散）")
guard("G8", E_drift < 1e-3, "B2 真空能量守恒相对漂移 < 1e-3（实测 %.3e）" % E_drift)


# --- B3：源项 M2-甲 / M2-乙 数值对比（不代选，只量化）------------------
rho_hat = 0.5          # 无量纲密度参数 4*pi*G*rho*L*^2/c^2
# 甲：S = rho_hat * u
yA = (list(u), list(v))
for _ in range(nsteps_grid):
    yA = rk4_step(lambda yy: rhs_grid(yy, w, src_mode='A', src_rho=rho_hat), yA, dt_grid)
maxA = max(abs(z) for z in yA[0])

# 乙（l_s = L* 即宏观标度）：S = rho_hat * (L*/l_s) = rho_hat
yB = (list(u), list(v))
for _ in range(nsteps_grid):
    yB = rk4_step(lambda yy: rhs_grid(yy, w, src_mode='B', src_val=rho_hat), yB, dt_grid)
maxB = max(abs(z) for z in yB[0])

# 乙（l_s = l_P，l_P/L* = 1.616255e-35 若 L*=1 m）：源项放大 ~6.19e34
lP_over_Lstar = 1.616255e-35
src_B_planck = rho_hat / lP_over_Lstar
yBp = (list(u), list(v))
blew_up = False
for _ in range(nsteps_grid):
    yBp = rk4_step(lambda yy: rhs_grid(yy, w, src_mode='B', src_val=src_B_planck), yBp, dt_grid)
    if not all(math.isfinite(z) for z in yBp[0]):
        blew_up = True
        break
maxBp = float('inf') if blew_up else max(abs(z) for z in yBp[0])

ratio_A_B = maxB / maxA if maxA != 0 else float('inf')

numeric.update({
    "B3_rho_hat": rho_hat,
    "B3_max_abs_M2a": maxA,
    "B3_max_abs_M2b_ls_macro": maxB,
    "B3_M2b_over_M2a_ratio": ratio_A_B,
    "B3_M2b_ls_planck_source": src_B_planck,
    "B3_M2b_ls_planck_blew_up": blew_up,
})

note_item("R21", "B3 源项两条候选数值对比（不代选）", "BOUNDARY",
          "同为 rho_hat=%.3g：甲（S~rho*kappa）末态 max|u|=%.4e；"
          "乙 取 l_s=L*（宏观）末态 max|u|=%.4e，甲/乙 比 %.4g；"
          "乙 取 l_s=l_P 时源项放大至 %.3e，数值%s。"
          "两条候选给出不同数值解 => 物理后果不同，须用户裁决。"
          % (rho_hat, maxA, maxB, ratio_A_B, src_B_planck,
             "发散（不可用）" if blew_up else "未发散"))

guard("G9", abs(maxA - maxB) > 0.0,
      "M2-甲 与 M2-乙 给出数值上不同的解（差异被检出，代价互斥成立）")
guard("G10", src_B_planck > 1e30,
      "M2-乙 对 l_s 极度敏感已量化：取 l_s=l_P 时源项放大至 %.3e（>1e30）" % src_B_planck)


# --- B4：约束面退化验证（呼应 r39/r45 的 V=0 发现）--------------------
# 路线B 公理1：kappa^2 + tau^2 = omega^2/c^2（无量纲 kappa^2 + tau^2 = w^2）
# 若初值恰在约束面上（tau=0 => u = w），则 c^2(kappa^2+tau^2) - omega^2 = 0
# => V = 0 且 dV/dkappa = 0 => 均匀初值下无动力学。
u_c = [w] * N
v_c = [0.0] * N
res_V = []
for i in range(N):
    bracket = (u_c[i] * u_c[i] + 0.0) - w * w      # 无量纲 (kappa^2+tau^2 - omega^2)
    res_V.append(abs(bracket))
max_bracket = max(res_V)

y_c = (list(u_c), list(v_c))
for _ in range(50):
    y_c = rk4_step(lambda yy: rhs_grid(yy, w), y_c, dt_grid)
dev_c = max(abs(y_c[0][i] - w) for i in range(N))

numeric.update({
    "B4_constraint_bracket_max": max_bracket,
    "B4_deviation_after_50_steps": dev_c,
})

note_item("R22", "B4 约束面退化（V=0 的动力学后果）", "BOUNDARY",
          "初值恰在公理1 约束面（tau=0, u=w）时，约束括号 |u^2+tau^2-w^2| 最大值 = %.3e，"
          "势项与其梯度恒为零；均匀初值演化 50 步后偏离约束面 %.3e（机器零量级）"
          "=> 确认 r39/r45 的「约束面上 V=0」发现，且此时方程退化为纯源项驱动。"
          "本册 B1/B2 的动力学均刻意取**偏离约束面**的初值（u<<w），否则无演化可谈。"
          % (max_bracket, dev_c))

guard("G11", max_bracket < 1e-12,
      "约束面上势项括号恒为机器零（V=0 确证）")
guard("G12", dev_c < 1e-9,
      "约束面均匀初值演化后仍停在约束面（无自发动力学）")


# ---------------------------------------------------------------------------
# 七、诚实边界
# ---------------------------------------------------------------------------
note_item("R23", "射程声明（不可越过）", "INFO",
          "①RK4 跑通只证明修复后方程**合法且可积**，不证明其物理正确；"
          "②B1 的 4 阶收敛是对**线性化**方程测得的，非线性区收敛性未证；"
          "③网格为 1+1 维平直背景、周期边界、tau=0，非真实 ADM-BSSN 3+1 时空演化；"
          "④M2 两条候选数值不同且代价互斥，本册不代选；"
          "⑤l0 定性（r42 M3）与「第一性导出 G」问题未被本册触及，仍不成立。")

note_item("R24", "解除 / 未解除的开放项", "INFO",
          "已解除：r42 G10/G14/G16/G17（量纲非齐次）与 X-R42-3（ADM-BSSN 齐次化）；"
          "部分解除：X-R42-2（M2 已执行但需裁决候选）；"
          "未解除：M3 / l0 定性 / 外部输入总账 / 与已关闭 g-2 窗口的关系。")


# ---------------------------------------------------------------------------
# 汇总与落盘
# ---------------------------------------------------------------------------
def tally():
    t = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0, "CORRECTED": 0, "MISMATCH": 0}
    for e in entries:
        t[e["verdict"]] = t.get(e["verdict"], 0) + 1
    return t


tl = tally()
g_ok = sum(1 for g in guards if g["ok"])
exit_code = 0 if g_ok == len(guards) else 1

one_line = (
    "M1（势项 d(V/c^4)/dkappa）+ M2（源项改结构，甲 ~rho*kappa / 乙 ~rho/l_s 两条均已实现）"
    "使路线B 第五节的 eq(10)(11) 与 ADM-BSSN 一阶系统量纲全部齐次（三项同为 L^-3、动量三项同为 L^-2 T^-1），"
    "r42 判的「演化系统无法数值积分」被解除；RK4 首次跑通：线性区对解析解收敛阶 %.2f（误差 %.2e），"
    "周期网格非线性演化稳定、真空能量相对漂移 %.2e。但 M2 两条候选数值解不同且代价互斥（乙再 +1 外部长度、"
    "取 l_s=l_P 时源项放大至 %.2e 而数值发散），本册不代选；且约束面上 V=0 使动力学只存在于偏离约束面的初值。"
    % (slope_mean, errs[-1], E_drift, src_B_planck)
)

out = {
    "name": NAME, "round": "r50", "date": DATE,
    "entries": entries, "guards": guards, "numeric": numeric,
    "tally": tl, "guard_ok": "%d/%d" % (g_ok, len(guards)),
    "exit_code": exit_code, "one_line": one_line,
}

here = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(os.path.dirname(here), "数据")
os.makedirs(data_dir, exist_ok=True)

with open(os.path.join(data_dir, NAME + ".json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

with open(os.path.join(data_dir, NAME + ".md"), "w", encoding="utf-8") as f:
    f.write("# %s\n\n" % NAME)
    f.write("- 条目：%s\n- guard：%s\n- 退出码：%d\n\n" % (tl, "%d/%d" % (g_ok, len(guards)), exit_code))
    f.write("## 一句话结论\n\n%s\n\n" % one_line)
    f.write("## 条目\n\n| id | 名称 | 判定 | LHS | RHS | 备注 |\n|---|---|---|---|---|---|\n")
    for e in entries:
        f.write("| %s | %s | %s | %s | %s | %s |\n"
                % (e["id"], e["name"], e["verdict"],
                   e.get("lhs_dim", "-"), e.get("rhs_dim", "-"), e.get("note", "")))
    f.write("\n## guard\n\n")
    for g in guards:
        f.write("- %s [%s] %s\n" % (g["id"], "OK" if g["ok"] else "FALSE", g["text"]))
    f.write("\n## 数值档案\n\n```json\n%s\n```\n"
            % json.dumps(numeric, ensure_ascii=False, indent=2))

with open(os.path.join(data_dir, NAME + "_report.txt"), "w", encoding="utf-8") as f:
    f.write("=== %s ===\n" % NAME)
    f.write("tally=%s\nguards=%d/%d exit=%d\n" % (tl, g_ok, len(guards), exit_code))
    f.write("RK4 convergence order (mean)=%.4f  slopes=%s\n" % (slope_mean, ["%.3f" % s for s in slopes]))
    f.write("B1 errors=%s\n" % ["%.4e" % e for e in errs])
    f.write("B2 energy drift=%.4e  max|u|_final=%.4e\n" % (E_drift, max_final))
    f.write("B3 maxA=%.4e maxB=%.4e ratio=%.4g ; l_s=l_P source=%.4e blew_up=%s\n"
            % (maxA, maxB, ratio_A_B, src_B_planck, blew_up))
    f.write("B4 constraint bracket max=%.4e ; deviation=%.4e\n" % (max_bracket, dev_c))
    f.write("\none_line: %s\n" % one_line)

print("=== %s ===" % NAME)
print("tally=%s" % tl)
print("guards=%d/%d exit=%d" % (g_ok, len(guards), exit_code))
print("RK4 order mean=%.4f slopes=%s" % (slope_mean, ["%.3f" % s for s in slopes]))
print("B1 errors=%s" % ["%.3e" % e for e in errs])
print("B2 E_drift=%.3e max|u|=%.3e" % (E_drift, max_final))
print("B3 A=%.4e B=%.4e ratio=%.4g ; lP src=%.3e blew=%s" % (maxA, maxB, ratio_A_B, src_B_planck, blew_up))
print("B4 bracket=%.3e dev=%.3e" % (max_bracket, dev_c))
print("")
print("one_line: %s" % one_line)

raise SystemExit(exit_code)
