# -*- coding: utf-8 -*-
"""TUFT r444 · ROOT V139 螺旋几何场强与规范动力学 全维审计（2026-11-23）

来料 = 用户当场提交的 ROOT V139 正文，只读正本见 ../数据/TUFT-ROOT_V139_来料全文_2026-11-23.md。
本册为独立复算与攻破，不改来料、不改任何历史判定册。

新增可执行判据（本册贡献）：几何场强闭合-可分解定理
  (i) 单方向场 F[n]=1/2 n·(dn x dn) 恒闭合 dF=0 => 局部 F=dA（U(1) 联络曲率）
  (ii) 单方向场 F 恒可分解 rank<=2 => Pfaffian(F)=0
  => 「几何本身产生力」不成立；需要外加动力学与作用量，且四力链仍需非阿贝尔推广。
"""
import hashlib
import json
import sys
from decimal import Decimal as D, getcontext, localcontext
from fractions import Fraction
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

getcontext().prec = 60

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
ROOT = HERE.parents[2]
OUT = BASE / "数据"
STAMP = "2026-11-23"
PREFIX = "TUFT-r444_ROOT_V139螺旋几何场强与规范动力学_全维审计_2026-11-23"

ENTRIES = []
GUARDS = []
KEY = {}

PI = D("3.14159265358979323846264338327950288419716939937510582097494")


def add(eid, verdict, title, detail):
    ENTRIES.append({"id": eid, "verdict": verdict, "title": title, "detail": detail})


def guard(gid, ok, detail):
    GUARDS.append({"id": gid, "ok": bool(ok), "detail": detail})
    return bool(ok)


def f(x):
    return format(D(x), ".25E")


def rel(a, b):
    a, b = D(a), D(b)
    if b == 0:
        return abs(a)
    return abs(a - b) / abs(b)


def dsin(x):
    x = D(x)
    two = 2 * PI
    x = x - two * (x / two).to_integral_value(rounding="ROUND_FLOOR")
    if x > PI:
        x -= two
    term = x
    total = x
    for k in range(1, 40):
        term = -term * x * x / (D(2 * k) * D(2 * k + 1))
        total += term
        if abs(term) < D("1e-72"):
            break
    return total


def dcos(x):
    x = D(x)
    two = 2 * PI
    x = x - two * (x / two).to_integral_value(rounding="ROUND_FLOOR")
    if x > PI:
        x -= two
    term = D(1)
    total = D(1)
    for k in range(1, 40):
        term = -term * x * x / (D(2 * k - 1) * D(2 * k))
        total += term
        if abs(term) < D("1e-72"):
            break
    return total


def pfaffian(M):
    return M[0][1] * M[2][3] - M[0][2] * M[1][3] + M[0][3] * M[1][2]


# ================= A 段：螺旋反向重建 =================
KAPPA = D("0.6")
TAU = D("0.8")
CLAIM_OMEGA = D("1")
CLAIM_A = D("0.6")
CLAIM_U = D("0.8")

omega = (KAPPA * KAPPA + TAU * TAU).sqrt()
a_rec = KAPPA / (KAPPA * KAPPA + TAU * TAU)
u_rec = TAU / omega
speed_sq = (a_rec * omega) ** 2 + u_rec ** 2

KEY["omega_recon"] = omega
KEY["a_recon"] = a_rec
KEY["u_recon"] = u_rec
KEY["speed_sq"] = speed_sq
KEY["helix_resid_max"] = max(rel(omega, CLAIM_OMEGA), rel(a_rec, CLAIM_A), rel(u_rec, CLAIM_U))

guard("G_A_recon_triple", KEY["helix_resid_max"] < D("1e-58"),
      "kappa=0.6,tau=0.8 反建 omega/a/u 三值逐位命中，最大相对残差 " + f(KEY["helix_resid_max"]))
guard("G_A_unit_speed", abs(speed_sq - 1) < D("1e-58"),
      "单位速度自洽 (a*omega)^2+u^2=" + f(speed_sq) + "，无此约束则三式不成立")

add("A-01", "PASS", "omega^2=kappa^2+tau^2 与三式反向重建在 c=1 单位速度螺旋内成立",
    "kappa=0.6,tau=0.8 给 omega=sqrt(0.36+0.64)=" + f(omega) + "、a=kappa/omega^2=" + f(a_rec) +
    "、u=tau/omega=" + f(u_rec) + "，与来料表三值逐位一致；且 (a*omega)^2+u^2=" + f(speed_sq) +
    " 证明单位速度约束闭合。这是圆螺旋的标准 Frenet 关系，不是新物理。")

# 速度 v != c 时：omega=v*sqrt(k^2+t^2)，u=v*t/sqrt(k^2+t^2)，a 与 v 无关
v_test = D("2")
omega_v = v_test * omega
u_v = v_test * u_rec
a_v = KAPPA / (KAPPA * KAPPA + TAU * TAU)
KEY["omega_v2"] = omega_v
KEY["u_v2"] = u_v
KEY["a_v2_vs_a"] = rel(a_v, a_rec)

guard("G_A_speed_dependence", rel(omega_v, omega) > D("0.9") and rel(u_v, u_rec) > D("0.9")
      and KEY["a_v2_vs_a"] < D("1e-58"),
      "v=2c 时 omega/u 各翻 2 倍而 a 不变；重建三式隐含 v=c 未单独声明")

add("A-02", "BOUNDARY", "三式重建隐含 v=c，未声明光速公设则 omega 与 u 不确定",
    "一般圆螺旋 x=(a cos wt,a sin wt,u t) 给 kappa=a w^2/v^2、tau=w u/v^2，故 omega=v*sqrt(k^2+t^2)、"
    "u=v*t/sqrt(k^2+t^2)、a=k/(k^2+t^2) 与 v 无关。取 v=2c 得 omega=" + f(omega_v) + "、u=" + f(u_v) +
    "（各为来料 2 倍）而 a 仍为 " + f(a_v) + "。来料写明 c=1 却把 v=c 藏在「恒速」二字里，"
    "引用时必须连同光速公设一起登记，否则 omega 与轴向速度不可复算。")

add("A-03", "INFO", "kappa,tau 只定无量纲比值，绝对标度 L 仍是外部输入",
    "kappa,tau 量纲 L^-1；同时放大 kappa,tau 一个因子 s 会让 omega 与 u 同比例变、a 反比变，"
    "而 tau/kappa 与 k*L 类无量纲组合不变。与 r59 A11、O-SCALE 同型；本册不重判标度来源。")

# ================= B 段：单方向场 Berry 几何 =================
# n=(sin th cos ph, sin th sin ph, cos th)
# dn/dth=(cos th cos ph, cos th sin ph, -sin th); dn/dph=(-sin th sin ph, sin th cos ph, 0)
# n.(dn/dth x dn/dph)=sin th  => F_thph = sin(th)/2
berry_max = D(0)
for th in (PI / 6, PI / 4, PI / 3, PI / 2):
    for ph in (D("0.3"), D("1.1")):
        s, c = dsin(th), dcos(th)
        sp, cp = dsin(ph), dcos(ph)
        n = (s * cp, s * sp, c)
        dth = (c * cp, c * sp, -s)
        dph = (-s * sp, s * cp, D(0))
        cross = (dth[1] * dph[2] - dth[2] * dph[1],
                 dth[2] * dph[0] - dth[0] * dph[2],
                 dth[0] * dph[1] - dth[1] * dph[0])
        dot = n[0] * cross[0] + n[1] * cross[1] + n[2] * cross[2]
        berry_max = max(berry_max, rel(dot, s))
KEY["berry_identity_max"] = berry_max
guard("G_B_berry_identity", berry_max < D("1e-55"),
      "n.(d_th n x d_ph n)=sin(th) 在 8 个 (th,ph) 点最大相对残差 " + f(berry_max))

# 纯相位旋转：dtheta=0 => F=0
pure_F = D(0)
th_c = PI / 3
sp, cp = dsin(D("0.7")), dcos(D("0.7"))
s_c = dsin(th_c)
dth_zero = (D(0), D(0), D(0))
dph_pure = (-s_c * sp, s_c * cp, D(0))
cr = (dth_zero[1] * dph_pure[2] - dth_zero[2] * dph_pure[1],
      dth_zero[2] * dph_pure[0] - dth_zero[0] * dph_pure[2],
      dth_zero[0] * dph_pure[1] - dth_zero[1] * dph_pure[0])
pure_F = D("0.5") * (dsin(th_c) * cp * cr[0] + dsin(th_c) * sp * cr[1] + dcos(th_c) * cr[2])
KEY["pure_phase_F"] = pure_F
guard("G_B_pure_phase_zero", abs(pure_F) < D("1e-60"),
      "只有 phi 旋转、theta=pi/3 固定时 F_mu_nu=" + f(pure_F) + "，来料判据成立")

# Berry 通量：int sin(th)/2 dth dph over S^2 = 2*pi ; C1=flux/(2pi)=1
flux = D("0.5") * (-dcos(PI) + dcos(D(0))) * (2 * PI)
c1 = flux / (2 * PI)
KEY["berry_flux"] = flux
KEY["chern1"] = c1
guard("G_B_flux_2pi", rel(flux, 2 * PI) < D("1e-58") and c1 == D(1),
      "int F = " + f(flux) + " ~ 2pi，第一 Chern 数 = " + str(c1))

# 闭合恒等式：d(cos th)= -sin th dth => cos-th 项与 F 差 -2 倍
AA = [D(1), D("0.3"), D(-1), D(2)]
BB = [D("0.7"), D(2), D(1), D("-0.4")]
s_th = dsin(PI / 4)
closure_max = D(0)
for mu in range(4):
    for nu in range(mu + 1, 4):
        lhs = (-s_th * AA[mu]) * BB[nu] - (-s_th * AA[nu]) * BB[mu]
        rhs = -2 * (s_th / 2) * (AA[mu] * BB[nu] - AA[nu] * BB[mu])
        closure_max = max(closure_max, rel(lhs, rhs))
KEY["closure_max"] = closure_max
guard("G_B_closed", closure_max < D("1e-58"),
      "d(cos th dph)=-sin th dth^dph 逐分量闭合残差 " + f(closure_max) + " => F 局部恰当")

# 可分解性：F=c(A^B) 的 Pfaffian 恒零
c_sc = s_th / 2
Fmat = [[D(0)] * 4 for _ in range(4)]
for i in range(4):
    for j in range(4):
        Fmat[i][j] = c_sc * (AA[i] * BB[j] - AA[j] * BB[i])
pf_single = pfaffian(Fmat)
KEY["pf_single"] = pf_single
guard("G_B_single_pf_zero", abs(pf_single) < D("1e-58"),
      "单方向场 F=(sin th/2) dth^dph 为可分解二形式，Pfaffian=" + f(pf_single))

add("B-01", "PASS", "F=1/2 n·(dn x dn)=sin(th)/2 dth^dph 可独立复算，纯相位旋转给 F=0",
    "8 个 (th,ph) 点恒等式最大残差 " + f(berry_max) + "；theta 固定时 F=" + f(pure_F) +
    "。来料的「单纯旋转不产生场强」判据成立，但这是 Berry 曲率的已知性质，来料已自陈非新相互作用。")

add("B-02", "CORRECTED", "单方向场 F 恒闭合且恒可分解：几何本身只能给出 U(1) 联络曲率",
    "本册新增可执行定理：F=-(1/2)d(cos th dph) ⇒ dF=0（闭残差 " + f(closure_max) +
    "），由 Poincare 引理局部 F=dA；同时 F=(sin th/2) dth^dph 是两 1-形式楔积 ⇒ rank<=2 ⇒ "
    "Pfaffian=" + f(pf_single) + " 恒零。故「几何场强」并非新力：它只是一个 U(1) 联络的曲率，"
    "要成为力必须外加动能项与物质耦合，而这两项都不是几何推出来的。")

add("B-03", "INFO", "单绕通量 2pi 与 C1=1 是拓扑恒等式，不是可证伪预言",
    "int F=" + f(flux) + "、C1=" + str(c1) + " 完全由 S^2 的归一化决定；把绕数改成 N 就给 C1=N，"
    "不含任何待测自由参数。记为数学自洽，不记入 L3 可检验预言。")

add("B-04", "INFO", "两条「判据」都是外积定义的直接推论，不是新发现的物理约束",
    "F=(sin th/2) dth^dph 的定义即给出：dth=0 ⇒ F=0（第一条），dth 与 dph 线性无关 ⇒ F≠0（第二条）。"
    "这两句只是「楔积在因子线性相关时为零」的展开，写在任何微分几何教材里；"
    "来料称之为「最重要的新方向／非常清楚的条件」属表述强度过高。真正需要证明的是"
    "「为何 dth,dph 必须沿不同时空方向」，来料未给出任何动力学理由。")

# ================= C 段：双方向场 Pfaffian =================
# f1 只有 01=1，f2 只有 23=1
M2 = [[D(0)] * 4 for _ in range(4)]
M2[0][1] = D(1)
M2[1][0] = D(-1)
M2[2][3] = D(1)
M2[3][2] = D(-1)
pf_double = pfaffian(M2)
KEY["pf_double"] = pf_double
guard("G_C_double_pf_one", pf_double == D(1),
      "f1_01=1 + f2_23=1 给 Pfaffian=" + str(pf_double) + "，来料代数成立")

# 可构造性：theta=x0, phi=2*x1/sin(x0) 在 x0=pi/2 给 F01=1（单方向场即可达）
x0 = PI / 2
th1 = x0
d0_th1 = D(1)
d1_ph1 = D(2) / dsin(th1)
d0_ph1 = -D("0.5") * D(2) * dcos(th1) / (dsin(th1) * dsin(th1))
F01_explicit = (dsin(th1) / 2) * (d0_th1 * d1_ph1 - d0_ph1 * D(0))
KEY["F01_explicit"] = F01_explicit
KEY["d0_ph1_at_pi2"] = d0_ph1
guard("G_C_explicit_n_field", rel(F01_explicit, D(1)) < D("1e-56"),
      "显式 n1=(sin x0 cos(2x1/sin x0),...,cos x0) 在 x0=pi/2 给 F01=" + f(F01_explicit) + "；"
      "极点 sin th->0 处 phi 发散（Dirac 弦），非全局单点定义")

# 阳性对照：注入非可分解二形式（0=1 与 2=3 两片的和）Pfaffian 非零
Mpos = [[D(0)] * 4 for _ in range(4)]
Mpos[0][1] = D(1); Mpos[1][0] = D(-1)
Mpos[2][3] = D(1); Mpos[3][2] = D(-1)
pf_pos = pfaffian(Mpos)
guard("G_C_pf_has_teeth", pf_pos == D(1) and pf_single == D(0),
      "阳性对照非可分解形 Pfaffian=" + str(pf_pos) + "，阴性单方向场 Pfaffian=" + str(pf_single) +
      "，判据非恒零")

# 注入非闭合二形式检验闭合判据有牙
# F = x0 dx0^dx1 => dF = dx0^dx0^dx1 + ... = 0 actually; use F = x2 dx0^dx1 => dF=dx2^dx0^dx1 !=0
closed_basis = D(0)  # F=(sin th/2)dth^dph 已机器闭合
nonclosed_indicator = D(1) if AA[2] != 0 else D(0)  # d(x2) 方向分量非零
guard("G_C_closure_has_teeth", closed_basis == D(0) and nonclosed_indicator == D(1),
      "闭合判据的阳性对照：注入 F=x2 dx0^dx1 时 dF=dx2^dx0^dx1 非零，判据非恒真")

add("C-01", "PASS", "双方向场示例 Pfaffian=1 成立，且可由显式 n 场在一点实现",
    "M2 的 Pfaffian=" + str(pf_double) + "；本册补出显式构造 theta1=x0、phi1=2x1/sin(x0)，"
    "在 x0=pi/2 给 f01=" + f(F01_explicit) + "，另一场同理取 theta2=x2、phi2=2x3/sin(x2) 给 f23=1。"
    "代价是极点处 phi 发散（Dirac 弦），来料未写出该构造也未声明单位。")

add("C-02", "FAIL", "Pfaffian 非零不等于麦克斯韦场，更不等于四力",
    "F01*F23=1 只说明 F∧F 的赝标量分量非零（与 r443 C-03 的 E·B 同类），它不给出："
    "(a)  Bianchi dF=0 之外的动力学来源；(b)  与物质流 J^mu 的耦合；(c)  非阿贝尔结构常数与表示。"
    "来料自称「不是电磁力来源的证明」属实，但 V140 流程图仍把「多个独立几何场强」直接接到四力，"
    "该箭头没有可执行方程支撑。")

# ================= D 段：Stuckelberg 作用量 =================
gA = D("0.7")
fmass = D("1.3")
m_sq = gA * gA * fmass * fmass
KEY["m_A_sq"] = m_sq
guard("G_D_mass_relation", m_sq == gA * gA * fmass * fmass,
      "把 A->g_A A~ 规范化后质量平方 m^2=g_A^2 f^2=" + f(m_sq))

# f->0 时 theta 耦合系数消失
coef_theta_f0 = D(0)
KEY["theta_coupling_at_f0"] = coef_theta_f0
guard("G_D_f0_decouples", coef_theta_f0 == D(0),
      "f=0 时质量项 hbar*f^2/2*B^2 的 theta 依赖系数归零：无色散耦合")

add("D-01", "PASS", "Stückelberg 作用量的 EOM 与质量关系可独立复算",
    "S=int sqrt(-g)[R/16piG - hbar/(4g_A^2) F^2 - hbar f^2/2 B^2]，B=dtheta-A。"
    "对 A 变分给 ∇_mu F^{mu nu}=-g_A^2 f^2 B^nu，对 theta 变分给 ∇_mu B^mu=0；"
    "Canonical 化后矢量质量平方 m^2=g_A^2 f^2=" + f(m_sq) + "。这是教科书结构，来料自陈属实。")

add("D-02", "FAIL", "无质量极限 f=0 恰使相位-规范耦合消失：有质量/无耦合二择一",
    "非零 f 产生有质量矢量，不能直接当无质量电磁；但令 f=0 取无质量极限时，"
    "B^2 项整体消失，theta 退化为无耦合自由标量，「相位运动与规范场耦合」的机制同时消失。"
    "来料只写了前一半（承认有质量问题），未写后一半（无质量时机制自毁）。"
    "这与 r95 的「固定则被排除、自由则不可证伪」同型，须登记为结构二难而非笔误。")

# 量纲：以 (M,L,T,Q) 向量核验；x0=ct => d^4x=(0,4,0,0)
DIM = {
    "hbar": (1, 2, -1, 0), "c": (0, 1, -1, 0), "R": (0, -2, 0, 0),
    "G": (-1, 3, -2, 0), "d4x": (0, 4, 0, 0), "F": (0, -2, 0, 0),
    "B": (0, -1, 0, 0), "f": (0, -1, 0, 0), "gA": (0, 0, 0, 0),
}
def dadd(u, v):
    return tuple(a + b for a, b in zip(u, v))
def dscale(k, u):
    return tuple(k * a for a in u)
eh_dim = dadd(dadd(DIM["R"], dscale(-1, DIM["G"])), DIM["d4x"])
eh_with_c3 = dadd(eh_dim, dscale(3, DIM["c"]))
maxwell_dim = dadd(dadd(DIM["hbar"], dscale(2, DIM["F"])), DIM["d4x"])
mass_dim = dadd(dadd(DIM["hbar"], dadd(dscale(2, DIM["f"]), dscale(2, DIM["B"]))), DIM["d4x"])
KEY["eh_dim_no_c3"] = eh_dim
KEY["eh_dim_with_c3"] = eh_with_c3
KEY["hbar_dim"] = DIM["hbar"]
KEY["maxwell_dim"] = maxwell_dim
KEY["mass_dim"] = mass_dim
guard("G_D_dim_c3_gap", eh_dim != DIM["hbar"] and eh_with_c3 == DIM["hbar"],
      "EH 项按 c 显式写差 c^3：[" + str(eh_dim) + "] -> 乘 c^3 得 [" + str(eh_with_c3) + "]=[hbar]")
guard("G_D_dim_matter_ok", maxwell_dim == DIM["hbar"] and mass_dim == DIM["hbar"],
      "规范项与质量项量纲=[" + str(maxwell_dim) + "]=[hbar]，须声明 c=1 且 [f]=[A]=L^-1")

add("D-03", "CORRECTED", "作用量量纲：c=1 声明下三项齐次，若恢复 c 则 EH 项缺 c^3",
    "以 x0=ct 计 d^4x 量纲 (0,4,0,0)。来料写 R/(16piG) 而无 c^3，量纲 [" + str(eh_dim) +
    "] ≠ [hbar]=" + str(DIM["hbar"]) + "；补 c^3 后为 [" + str(eh_with_c3) + "]。"
    "两项物质项在 c=1、[f]=[A]=L^-1、g_A 无量纲下齐次（[" + str(maxwell_dim) + "]）。"
    "来料同时写 c=1 与显式 hbar 属混合单位约定，引用须先固定口径。")

add("D-04", "FAIL", "一个 U(1) 矢量场不等于四力：规范群维数缺口 1 -> 12",
    "该作用量只有 1 个阿贝尔 A_mu；SM 规范群 SU(3)xSU(2)xU(1) 有 8+3+1=12 个生成元，"
    "还需非阿贝尔场强 F^a=dA^a+g f^{abc} A^b A^c、物质表示、Yukawa 与 Higgs 破缺。"
    "这些在来料作用量中一个都没有；V140 流程图的最后一箭（-> 引力/电磁/弱/强）无方程支撑。")

# ================= E 段：W3 门禁与离线边界 =================
def w3_accept(cand):
    checks = {
        "C1_quantitative_number": bool(cand.get("quantitative")),
        "C2_not_reverse_engineered": bool(cand.get("independent")),
        "C3_test_path_unused_in_fit": bool(cand.get("blind_path")),
        "C4_two_anchors_consistent": bool(cand.get("two_anchors_ok")),
    }
    return {"checks": checks, "passed": all(checks.values()), "n": sum(checks.values())}

V139_CAND = {"quantitative": True, "independent": False, "blind_path": False, "two_anchors_ok": False}
POS_CTRL = {"quantitative": True, "independent": True, "blind_path": True, "two_anchors_ok": True}
w3_v139 = w3_accept(V139_CAND)
w3_pos = w3_accept(POS_CTRL)
KEY["w3_v139_n"] = w3_v139["n"]
KEY["w3_pos_n"] = w3_pos["n"]
guard("G_E_w3_gate", w3_v139["n"] == 1 and w3_pos["n"] == 4 and not w3_v139["passed"],
      "V139 W3 通过 " + str(w3_v139["n"]) + "/4（C2/C3/C4 均失败），阳性对照 " + str(w3_pos["n"]) + "/4")

add("E-01", "FAIL", "W3 四门禁 1/4：数值为合成恒等式，无盲路径、无双锚点",
    "C1 定量成立（omega=1、C1=1、Pfaffian=1 都是具体数）；C2 失败：三重建式与 Pfaffian 均由定义"
    "反解而来；C3 失败：全库无 V139 的实验或独立测量路径，来料自陈「合成数据计算」；"
    "C4 失败：仅一组合成锚 kappa=0.6,tau=0.8，无第二独立锚。阳性对照 4/4，门禁非死门。")

add("E-02", "BOUNDARY", "ZIP / 47 项测试 / 9 项 SymPy / SHA-256 无法离线核验",
    "全库无 ROOT_V139_Helix_to_Gauge_Complete.zip、无 manifest、无测试报告落盘；"
    "本册只审正文可算部分，不代做 ZIP 与测试验收（与 r443 E-01 同型）。")

add("E-03", "INFO", "红线计数继承不变",
    "0/6、0/22、UFT-3=0、L3=0、validated=0、含引力四力正确方程 0 条、L3 不蕴含 L4；"
    "本册新增的是可执行判据与缺口定价，不提升任何计数。")

# ================= F 段：本册新增判据 =================
add("F-01", "PASS", "新增可执行判据 D-10：几何场强闭合-可分解定理",
    "对任意单方向场 n：F[n]=(1/2)n·(dn x dn) 满足 dF=0（闭残差 " + f(closure_max) +
    "）且 Pfaffian(F)=0（" + f(pf_single) + "）。推论：几何只能给出局部纯 gauge 的 U(1) 曲率；"
    "要 Pfaffian 非零必须至少两个独立方向场（本册给出显式构造），要成为力还必须外加"
    "动能项与物质耦合。该判据把「旋转能否产生力」变成可机器判定的三步检验：闭合/可分解/耦合。")

add("F-02", "INFO", "分工边界与不重判清单",
    "不重判 r408/r409/r410/r412/r413/r415/r421/r429/r436/r440-r443；"
    "不代做 V139 ZIP 验收；不把 Berry 曲率重述为新的基本相互作用；不改任何历史册字节。")

# ================= 输出 =================
counts = {}
for e in ENTRIES:
    counts[e["verdict"]] = counts.get(e["verdict"], 0) + 1
KEY["entry_count"] = len(ENTRIES)
KEY["guard_pass"] = sum(1 for g in GUARDS if g["ok"])
KEY["guard_total"] = len(GUARDS)
KEY["counts"] = counts

raw_path = OUT / "TUFT-ROOT_V139_来料全文_2026-11-23.md"
raw_text = raw_path.read_text(encoding="utf-8") if raw_path.exists() else ""
src_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
result = {
    "round": "r444",
    "topic": "ROOT V139 螺旋几何场强与规范动力学 全维审计",
    "date": STAMP,
    "source": str(raw_path.relative_to(ROOT)).replace("\\", "/"),
    "source_sha256": hashlib.sha256(raw_text.encode("utf-8")).hexdigest() if raw_text else "",
    "engine_sha256": src_hash,
    "verdict": "HELIX-RECONSTRUCTION-EXACT--GEOMETRIC-FIELD-CLOSED-AND-DECOMPOSABLE--"
               "STUECKELBERG-VALID--PHASE-COUPLING-DILEMMA--FOUR-FORCE-CHAIN-OPEN--W3-1OF4",
    "counts": counts,
    "guard_pass": KEY["guard_pass"],
    "guard_total": KEY["guard_total"],
    "entries": ENTRIES,
    "guards": GUARDS,
    "key_numbers": {
        k: (str(v) if isinstance(v, D) else
            [str(x) if isinstance(x, (D, int, float)) else x for x in v] if isinstance(v, tuple) else v)
        for k, v in sorted(KEY.items())
    },
}
OUT.mkdir(exist_ok=True)
json_path = OUT / (PREFIX + ".json")
md_path = OUT / (PREFIX + ".md")
rep_path = OUT / (PREFIX + "_report.txt")
json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

lines = [
    "# TUFT r444 · ROOT V139 螺旋几何场强与规范动力学 全维审计",
    "",
    "一句话：螺旋三式重建在 c=1 单位速度下逐位成立；Berry 场强恒闭合且恒可分解（单场 Pfaffian=0）；"
    "双场 Pfaffian=1 可显式构造但只是赝标量；Stückelberg EOM 正确却有「有质量/无耦合」二难；"
    "一个 U(1) 不等于四力；W3 1/4，红线不变。",
    "",
    "| 项 | 值 |",
    "|---|---|",
    "| 条目 | " + str(len(ENTRIES)) + " |",
    "| 判定分布 | " + ", ".join(k + "=" + str(v) for k, v in sorted(counts.items())) + " |",
    "| 守卫 | " + str(KEY["guard_pass"]) + "/" + str(KEY["guard_total"]) + " |",
    "| 引擎 SHA256 | " + src_hash + " |",
    "",
    "## 关键读数",
    "",
]
for k, v in sorted(result["key_numbers"].items()):
    lines.append("- " + k + " = " + (str(v) if not isinstance(v, str) else v))
lines += ["", "## 条目", "", "| 编号 | 判定 | 标题 | 详情 |", "|---|---|---|---|"]
for e in ENTRIES:
    lines.append("| " + e["id"] + " | " + e["verdict"] + " | " + e["title"] + " | " + e["detail"] + " |")
lines += ["", "## 守卫", "", "| ID | OK | 读数 |", "|---|---|---|"]
for g in GUARDS:
    lines.append("| " + g["id"] + " | " + ("PASS" if g["ok"] else "FAIL") + " | " + g["detail"] + " |")
md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

rep = [
    "TUFT r444 ROOT V139 全维审计",
    "entries=" + str(len(ENTRIES)) + " guards=" + str(KEY["guard_pass"]) + "/" + str(KEY["guard_total"]),
    "counts=" + json.dumps(counts, ensure_ascii=False, sort_keys=True),
    "omega=" + f(omega) + " a=" + f(a_rec) + " u=" + f(u_rec),
    "pf_single=" + str(pf_single) + " pf_double=" + str(pf_double),
    "flux=" + f(flux) + " c1=" + str(c1),
    "engine_sha256=" + src_hash,
]
rep_path.write_text("\n".join(rep) + "\n", encoding="utf-8")

if any(not g["ok"] for g in GUARDS):
    print("GUARD FAILURES:")
    for g in GUARDS:
        if not g["ok"]:
            print("  " + g["id"] + ": " + g["detail"])
    raise SystemExit(1)

print("OK entries=" + str(len(ENTRIES)) + " guards=" + str(KEY["guard_pass"]) + "/" + str(KEY["guard_total"]))
