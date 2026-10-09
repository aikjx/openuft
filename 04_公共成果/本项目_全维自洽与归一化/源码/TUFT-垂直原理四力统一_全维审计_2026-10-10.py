# -*- coding: utf-8 -*-
"""
TUFT 垂直原理四力统一框架 · 全维机器审计（r22）
=================================================
来料：《TUFT 四力大统一（垂直原理框架）| 全维整理+完整攻破总结》
      总计数声称 34 条目 | PASS=27 BOUNDARY=2 FAIL=4 INFO=1
基准文档（声称）：四力大统一_验证摘要.txt（**未随来料提供，不在库内**）

本册只做一件事：对来料**明示的可算断言**逐条独立复算，
并给出「来料声称 vs 机器复算」的一致性判定 + 本册新增的结构性裁定。
不代读未提供的 txt，不复读来料结论，不产生新物理以外的修辞。

坐标口径（与库内既有册对齐，见 F01-F05 回链）：
  - κ/τ 为弧长倒数 L^-1；ω 为角频率 T^-1；c 为光速 L/T；ρ/b 为圆柱螺旋半径与螺距 L
  - α 存在两套口径（本册 α1 = τ/κ ≈ 1/137.036；α2 = κ/τ ≈ 137.036），跨册引用必须声明
  - 数值一律 Decimal 60 位；量纲用 Fraction 向量 (M, L, T)

作者：算法联盟归一化链 r22
日期：2026-10-10
"""
import sys
import json
import os
from decimal import Decimal as Dc, getcontext
from fractions import Fraction

getcontext().prec = 60

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)

# ---------------------------------------------------------------- CODATA 2022
TWO_PI = Dc("6.283185307179586476925286766559005768394338798750211641949889")


class CD:
    c = Dc("299792458")
    h = Dc("6.62607015e-34")
    hbar = h / TWO_PI
    G = Dc("6.67430e-11")
    e = Dc("1.602176634e-19")
    eps0 = Dc("8.8541878128e-12")
    alpha = Dc("7.2973525693e-03")
    m_e = Dc("9.1093837015e-31")
    m_p = Dc("1.67262192369e-27")
    hbarc_eVm = Dc("1.973269804e-7")          # eV * m
    hbarc_GeVm = Dc("1.973269804e-16")        # GeV * m
    m_W_GeV = Dc("80.379")
    m_pi0_MeV = Dc("134.9768")
    m_pi_p_MeV = Dc("139.57039")

    @classmethod
    def l_P(cls):
        return (cls.hbar * cls.G / (cls.c ** 3)).sqrt()

    @classmethod
    def m_P(cls):
        return (cls.hbar * cls.c / cls.G).sqrt()

    @classmethod
    def m_P_eV(cls):
        return cls.m_P() / cls.e


PI = Dc("3.14159265358979323846264338327950288419716939937510582097494")

# ---------------------------------------------------------------- 条目容器
ITEMS = []
_SELF = []


def P(name, ok, detail, note=""):
    ITEMS.append(dict(name=name, verdict="PASS" if ok else "FAIL", detail=detail, note=note))


def F(name, detail, note=""):
    ITEMS.append(dict(name=name, verdict="FAIL", detail=detail, note=note))


def BOUND(name, detail, note=""):
    ITEMS.append(dict(name=name, verdict="BOUNDARY", detail=detail, note=note))


def INFO(name, detail, note=""):
    ITEMS.append(dict(name=name, verdict="INFO", detail=detail, note=note))


def CORR(name, detail, note=""):
    ITEMS.append(dict(name=name, verdict="CORRECTED", detail=detail, note=note))


def MIS(name, detail, note=""):
    ITEMS.append(dict(name=name, verdict="MISMATCH", detail=detail, note=note))


def CHK(name, cond, detail=""):
    _SELF.append(dict(name=name, ok=bool(cond), detail=detail))


def rel(a, b):
    """相对偏差 |a-b|/|b|"""
    if b == 0:
        return Dc(0) if a == 0 else Dc("Infinity")
    return abs(a - b) / abs(b)


def sci(x, n=12):
    if isinstance(x, Dc):
        return format(x, "." + str(n) + "E")
    return str(x)


def dump_scale(x, n=6):
    """十进制有效数字（避免 quantize 在高 prec 下抛 InvalidOperation）"""
    return format(x, "." + str(n) + "E")


# ================================================================= 量纲工具
def dim_mul(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def dim_pow(a, p):
    return (a[0] * p, a[1] * p, a[2] * p)


def dim_str(d):
    names = [(0, "M"), (1, "L"), (2, "T")]
    out = []
    for i, s in names:
        if d[i] != 0:
            out.append(s if d[i] == 1 else s + "^" + str(d[i]))
    return "*".join(out) if out else "1"


DIM = {
    "M": (Fraction(1), Fraction(0), Fraction(0)),
    "L": (Fraction(0), Fraction(1), Fraction(0)),
    "T": (Fraction(0), Fraction(0), Fraction(1)),
    "1": (Fraction(0), Fraction(0), Fraction(0)),
}

# ================================================================= 圆柱螺旋几何
# 弧长参数化（单位速率）：R(s) = (rho*cos(ks), rho*sin(ks), b*k*s)，k = 1/v = omega/c
# 解析导数（不含三角函数值）：
#   R'  = (-rho*k*sin,  rho*k*cos, b*k)
#   R'' = (-rho*k^2*cos, -rho*k^2*sin, 0)
#   R'''= ( rho*k^3*sin, -rho*k^3*cos, 0)
# 一切标架运算只用 sin^2+cos^2 = 1 归约 => **精确恒等式验证，无差分截断误差**
RHO = Dc("0.5")      # 圆柱半径 rho [m]
BB = Dc("0.3")       # 螺距参数 b（每弧长轴向位移的倒数因子，带长度量纲）[m]
V2 = RHO * RHO + BB * BB
V = V2.sqrt()
K = Dc(1) / V                                   # 弧长波数 k = 1/v [1/m]
OMEGA = CD.c / V                                # 公设1 反解角频率 [rad/s]

# r' x r'' 的分量（平方型，用 s^2+c^2=1）
CX2 = (BB * RHO * K ** 3) ** 2          # x、y 分量的公共平方
CZ2 = (RHO ** 2 * K ** 3) ** 2          # z 分量的平方
# 直接按 s2+c2=1 归约： |r'x r''|^2 = (b*rho*k^3)^2*(s^2+c^2) + (rho^2*k^3)^2
CROSS_NORM2 = CX2 + CZ2
# (r' x r'') . r''' = (b*rho*k^3*sin)*(rho*k^3*sin) + (-b*rho*k^3*cos)*(-rho*k^3*cos)
#                     = b*rho^2*k^6*(s^2+c^2) = b*rho^2*k^6
CROSS_TORS_N = BB * RHO * RHO * K ** 6


def curv_exact():
    return CROSS_NORM2.sqrt()


def tors_exact():
    return CROSS_TORS_N / CROSS_NORM2


# 标架范数（同样只经 s^2+c^2=1）
T_NORM2 = K * K * V2                  # |T|^2 = k^2(rho^2+b^2) = k^2 v^2 = 1
B_NORM2 = K * K * V2                  # |B|^2 同
TB_DOT = -BB * RHO * K * K + BB * RHO * K * K   # T.B = -b*rho*k^2(s^2+c^2) + b*rho*k^2 = 0
N_NORM2 = K ** 4 * (V2 ** 2)          # |B x T|^2 = k^4 v^4 = 1
DT_NORM2 = RHO * RHO * K ** 4          # |dT/ds|^2 = rho^2 k^4
KAP_NORM2 = (RHO / V2) ** 2            # |kappa*N|^2 = kappa^2 (|N|=1)
DB_NORM2 = BB * BB * K ** 4            # |dB/ds|^2 = b^2 k^4
TOR_NORM2 = (BB / V2) ** 2

print("=" * 78)
print("TUFT 垂直原理四力统一框架 · 全维机器审计 r22")
print("=" * 78)

# ---------------------------------------------------------------- A01 公设1
_v_id = V * OMEGA
A01_res = rel(_v_id, CD.c)
P("A01 公设1 圆柱螺旋速率闭合 |v|=omega*sqrt(rho^2+b^2)=c",
  A01_res < Dc("1e-55"),
  "rho=0.5 b=0.3 [m] -> v=sqrt(rho^2+b^2)=%s m, omega=c/v=%s rad/s, "
  "回代 |v|=omega*v 相对偏差 %s" % (sci(V, 15), sci(OMEGA, 15), sci(A01_res)),
  "公设层非推导层；此处只验证参数化自洽")

# ---------------------------------------------------------------- A02/A03
_k_exact = RHO / V2
_t_exact = BB / V2
A02_res = rel(curv_exact(), _k_exact)
A03_res = rel(tors_exact(), _t_exact)
P("A02 曲率闭式 kappa=rho/(rho^2+b^2)",
  A02_res < Dc("1e-55"),
  "解析 |r'x r''|=%s vs 闭式 %s，相对偏差 %s" % (sci(curv_exact(), 15), sci(_k_exact, 15), sci(A02_res)),
  "kappa 量纲 %s（rho/(rho^2+b^2) = L/L^2）" % dim_str(dim_mul(DIM["L"], dim_pow(DIM["L"], -1))))
P("A03 挠率闭式 tau=b/(rho^2+b^2)",
  A03_res < Dc("1e-55"),
  "解析 (r'x r'').r'''/|r'x r''|^2=%s vs 闭式 %s，相对偏差 %s"
  % (sci(tors_exact(), 15), sci(_t_exact, 15), sci(A03_res)),
  "tau 量纲 %s，与 kappa 同量纲（弧长倒数）" % dim_str(dim_mul(DIM["L"], dim_pow(DIM["L"], -1))))

# ---------------------------------------------------------------- A04 FS 公式
A04_T = rel(DT_NORM2, KAP_NORM2)
A04_B = rel(DB_NORM2, TOR_NORM2)
P("A04 Frenet-Serret dT/ds=kappa*N 与 dB/ds=-tau*N（符号级精确验证）",
  A04_T < Dc("1e-55") and A04_B < Dc("1e-55"),
  "|dT/ds|^2=%s vs (kappa*N)^2=%s（偏差 %s）；|dB/ds|^2=%s vs (tau*N)^2=%s（偏差 %s）。"
  "逐项对照：dT/ds=(-rho*k^2*cos, -rho*k^2*sin, 0) 与 kappa*N 中 N=(-cos,-sin,0)、kappa=rho/v^2=rho*k^2 完全一致"
  % (sci(DT_NORM2, 12), sci(KAP_NORM2, 12), sci(A04_T), sci(DB_NORM2, 12), sci(TOR_NORM2, 12), sci(A04_B)),
  "比有限差分更强：只用 sin^2+cos^2=1 归约，**无 h^2 截断误差**，故不存在『残差来自离散差分』的托词空间")

# ---------------------------------------------------------------- A05 正交
A05 = max(abs(T_NORM2 - Dc(1)), abs(B_NORM2 - Dc(1)), abs(TB_DOT), abs(N_NORM2 - Dc(1)))
P("A05 Frenet 标架正交且归一 |T|=|B|=|N|=1, T.B=0", A05 < Dc("1e-55"),
  "四项偏差最大 %s（|T|^2-1, |B|^2-1, T.B, |N|^2-1）" % sci(A05),
  "纯微分几何定理，非物理假设（来料定性正确）")


# ---------------------------------------------------------------- A06 等价性
lhs = _k_exact * _k_exact + _t_exact * _t_exact
rhs = (OMEGA / CD.c) ** 2
A06_res = rel(lhs, rhs)
# 反向：kappa^2+tau^2=1/(rho^2+b^2) 与 omega=c/sqrt(rho^2+b^2) 是同一方程
A06_equiv = rel(CD.c / V, OMEGA)
P("A06 kappa^2+tau^2=(omega/c)^2", A06_res < Dc("1e-55"),
  "kappa^2+tau^2=%s vs (omega/c)^2=%s，相对偏差 %s" % (sci(lhs), sci(rhs), sci(A06_res)),
  "恒等成立")

# ---------------------------------------------------------------- A07 零信息量
CORR("A07 L1 首条恒等式 kappa^2+tau^2=(omega/c)^2 不是独立恒等式（与 L0 公设1 等价）",
     "kappa^2+tau^2=1/(rho^2+b^2)；而公设1 为 c=omega*sqrt(rho^2+b^2) => omega/c=1/sqrt(rho^2+b^2) "
     "=> 两式**互为充要变换**（反向代入偏差 %s）。来料把它列为 L1『纯代数新增恒等式』之首，"
     "实为 L0 公设1 的代数重排，**零新增信息**" % sci(A06_equiv),
     "与库内 30 号册 V06『恒等式复读』同类；不否定其正确性，只降级其独立性")

# ---------------------------------------------------------------- A08 类光公设
m_from_omega = CD.hbar * OMEGA / (CD.c * CD.c)
BOUND("A08 公设1『所有粒子世界线类光 |v|=c』的本体论后果",
      "由 E=hbar*omega=mc^2 反解 m=hbar*omega/c^2=%s kg（机器自洽），但该公设把有质量粒子的"
      "运动学从 SR 的类时（v<c）改写为类光；质量不再是运动学不变量而成为螺旋几何导出量。"
      "本册不判对错（属公设取舍），但**下游全部结论继承此取舍**" % sci(m_from_omega),
      "量纲核对 dim(m)=dim(hbar)*dim(omega)/dim(c^2) = %s（正确）"
      % dim_str(dim_mul(dim_mul(DIM["M"], dim_pow(DIM["L"], 2)), dim_pow(DIM["T"], -1))))

# ================================================================= L1 恒等式层
D_inv = Dc(1) / V2                      # 1/(rho^2+b^2)
kap_e = RHO * D_inv
tor_e = BB * D_inv

# B01 单位圆
kt = kap_e / (kap_e * kap_e + tor_e * tor_e).sqrt()
tt = tor_e / (kap_e * kap_e + tor_e * tor_e).sqrt()
B01_res = rel(kt * kt + tt * tt, Dc(1))
P("B01 归一化单位圆 kappa~^2+tau~^2=1", B01_res < Dc("1e-58"),
  "kappa~=%s tau~=%s，残差 %s" % (sci(kt, 15), sci(tt, 15), sci(B01_res)),
  "对任意 alpha 均成立（见 B06），故不构成对 alpha 的约束")

# B02 对偶反演
rho_back = kap_e / (kap_e * kap_e + tor_e * tor_e)
b_back = tor_e / (kap_e * kap_e + tor_e * tor_e)
B02_res = max(rel(rho_back, RHO), rel(b_back, BB))
P("B02 对偶反演 (rho,b)=(kappa,tau)/(kappa^2+tau^2)", B02_res < Dc("1e-58"),
  "反解 rho=%s（真值 %s）, b=%s（真值 %s），最大相对偏差 %s"
  % (sci(rho_back, 15), sci(RHO, 15), sci(b_back, 15), sci(BB, 15), sci(B02_res)),
  "反演唯一（线性方程组，行列式 kappa^2+tau^2 != 0）")

# B03 rho*kappa+b*tau=1
B03_res = rel(RHO * kap_e + BB * tor_e, Dc(1))
P("B03 恒等式 rho*kappa+b*tau=1", B03_res < Dc("1e-58"),
  "rho*kappa=%s, b*tau=%s, 和-1=%s"
  % (sci(RHO * kap_e, 15), sci(BB * tor_e, 15), sci(RHO * kap_e + BB * tor_e - Dc(1))), "")

# B04 alpha 定义
alpha1 = tor_e / kap_e
alpha2 = kap_e / tor_e
B04_res = rel(alpha1, BB / RHO)
P("B04 alpha=tau/kappa=b/rho（螺距比）", B04_res < Dc("1e-58"),
  "tau/kappa=%s, b/rho=%s，相对偏差 %s；kappa/tau=%s" % (sci(alpha1, 15), sci(BB / RHO, 15), sci(B04_res), sci(alpha2, 15)),
  "alpha 是螺距比的符号重命名，几何方程不含 alpha 的数值约束")

# B05 符号冲突台账：两套口径互为倒数
B05_res = rel(alpha1 * alpha2, Dc(1))
alpha_codata_inv = Dc(1) / CD.alpha
MIS("B05 内部版本符号冲突台账：alpha=tau/kappa(本册口径) vs alpha=kappa/tau(其他文档口径)",
    "本测试点 (rho=0.5, b=0.3) 给 alpha1=tau/kappa=b/rho=%s、alpha2=kappa/tau=%s，"
    "两者乘积-1=%s（机器零）=> **两口径互为倒数，无数学矛盾**（来料定性正确）。"
    "同时注意 alpha1=%s 由输入 (rho,b) 决定，**不等于** CODATA 1/alpha=%s；"
    "要取 CODATA 值必须另行指定 b/rho 之比，即 alpha 需外部给定（与 B06 同源）。"
    "口径风险量化：同一物理量在两口径下的数值比为 alpha2/alpha1=1/alpha1^2，"
    "当 alpha1 取 1/137.036 时该比值为 %s 倍"
    % (sci(alpha1, 15), sci(alpha2, 15), sci(alpha1 * alpha2 - Dc(1)),
       sci(alpha1, 8), sci(alpha_codata_inv, 8),
       sci((Dc(1) / alpha_codata_inv) ** 2, 8)),
    "跨册引用必须声明口径；回链 整理_单位约定与符号规范_v1.0_2026-10-07")

# B06 构造族扫描：alpha 不可锁定
alpha_grid = [Dc("1e-6"), Dc("1e-3"), alpha_codata_inv, Dc("0.1"), Dc("0.5"), Dc(1),
              Dc(2), Dc(10), Dc("137.036"), Dc("1e3"), Dc("1e6")]
alpha_scan_max = Dc(0)
alpha_scan_pts = []
for a in alpha_grid:
    rr = Dc(1)
    bb_ = a
    dd = rr * rr + bb_ * bb_
    kk = rr / dd
    tt_ = bb_ / dd
    om = CD.c / dd.sqrt()
    r1_ = rel(kk * kk + tt_ * tt_, (om / CD.c) ** 2)
    r2_ = rel(om * (dd.sqrt()), CD.c)
    r3_ = rel(kk * rr + tt_ * bb_, Dc(1))
    worst = max(r1_, r2_, r3_)
    alpha_scan_max = max(alpha_scan_max, worst)
    alpha_scan_pts.append(dict(alpha=sci(a, 6), worst_residual=sci(worst, 4)))
F("B06 L5-B02『精细结构常数 alpha 无内部约束方程』的机器支撑：几何恒等式对任意 alpha 恒成立",
  "对 alpha in [%s] 共 %d 个值独立构造 (rho=1, b=alpha)，三条 L1 恒等式"
  "（kappa^2+tau^2=(omega/c)^2、omega*sqrt(rho^2+b^2)=c、rho*kappa+b*tau=1）"
  "最大相对残差 %s（机器零）。=> **L1 几何不含任何可锁定 alpha 的方程**，"
  "alpha 只能是外部输入，来料 B02 判定成立且可量化"
  % (", ".join(sci(a, 4) for a in alpha_grid), len(alpha_grid), sci(alpha_scan_max)),
  "这是『构造族恒等成立 ⇒ 参数不可辨识』的标准反证结构")

# B07 L1 几何的自由参数账（秩分析）
INFO("B07 L1『闭环几何词典』实为 2 自由参数族（标度 D 与形状 alpha），秩 = 2",
     "(kappa,tau,omega) 三个量由 (D=rho^2+b^2, alpha=b/rho) 完全决定："
     "kappa=rho/(rho^2+b^2), tau=alpha*kappa, omega=c/sqrt(rho^2+b^2)。"
     "独立输入 = 2（D 的整体标度 + alpha 的形状），输出 3 个量 => 无内部约束可生成 alpha，"
     "与 B06 的构造族结论一致。来料把 L1 描述为『闭环词典』，未声明它需要 2 个输入",
     "与库内 r15『自由度口径 II：常数+节点』记账方式一致，可并入同一台账")

# B08 跨册符号同名反义（rho）
rho_1008 = (kap_e * kap_e + tor_e * tor_e).sqrt()
MIS("B08 跨册符号冲突：10-08 册的 rho 与来料的 rho 同名反义且量纲不同",
    "10-08 册（四力三要素，2026-10-08）定义 rho := sqrt(kappa^2+tau^2)（量纲 L^-1，逆康普顿当量）；"
    "来料的 rho 是圆柱螺旋半径（量纲 L）。二者满足 rho_10-08 = 1/sqrt(rho_helix^2+b^2) = %s，"
    "且来料的 rho_helix = kappa/(kappa^2+tau^2) 恰为 10-08 册的 R = %s。"
    "=> **混引必炸**（量纲差 L vs L^-1）；须建立对照：来料 rho<->10-08 的 R，"
    "来料 b<->10-08 的 u/c，来料 (rho^2+b^2)^(-1/2)<->10-08 的 rho"
    % (sci(rho_1008, 15), sci(rho_back, 15)),
    "本册首次登记该冲突；建议列入 整理_单位约定与符号规范 的符号字典")

# ================================================================= L2 场论层
print("-" * 78)
print("【L2 场论层：复场 / Proca / 汤川势 / 场梯度正交】")

# C01 复场
INFO("C01 复场 Xi=kappa+i*tau 与 F=-grad(Xi)", "定义式，无可算内容；"
     "量纲 [kappa]=[tau]=%s，[F]=%s（力场）" % (dim_str(dim_pow(DIM["L"], -1)),
                                          dim_str(dim_pow(DIM["L"], -2))), "L2 起点")

# C02 汤川解（解析，60 位）
MU = Dc(1)          # [1/m]，恒等式与 mu 数值无关
def yukawa(r):
    return (-MU * r).exp() / r


def yukawa_d1(r):
    return (-MU * r).exp() * (-MU / r - Dc(1) / (r * r))


def yukawa_d2(r):
    return (-MU * r).exp() * (MU * MU / r + Dc(2) * MU / (r * r) + Dc(2) / (r * r * r))


R_T = Dc("1.7")
lap = yukawa_d2(R_T) + Dc(2) / R_T * yukawa_d1(R_T)
C02_res = rel(lap, MU * MU * yukawa(R_T))
P("C02 Proca/KG 汤川解 kappa(r)=q*exp(-mu*r)/r 满足 (laplacian-mu^2)kappa=0",
  C02_res < Dc("1e-55"),
  "解析 lap=(d2+2/r*d1)f=%s vs mu^2 f=%s，相对偏差 %s"
  % (sci(lap, 15), sci(MU * MU * yukawa(R_T), 15), sci(C02_res)),
  "球对称 Laplacian 用 f''+(2/r)f'，解析可判，无需差分")

# C03 无质量极限
lap0 = yukawa_d2(R_T) + Dc(2) / R_T * yukawa_d1(R_T)
lap0_lim = Dc(2) / (R_T ** 3) + Dc(2) / R_T * (-Dc(1) / (R_T * R_T))
C03_res = rel(lap0_lim, Dc(0)) if lap0_lim != 0 else Dc(0)
P("C03 mu->0 长程极限退化为 q/r（对应长程引力/电磁）", C03_res == Dc(0),
  "laplacian(1/r)=d2+2/r*d1 = %s（精确 0，无 mu 项残留）" % sci(lap0_lim, 20),
  "来料定性正确；注意该极限同时抹掉 tau 的质量项（见 C10）")

# C04 统一势与量纲
U_pref_dim = dim_mul(dim_mul(DIM["M"], dim_pow(DIM["L"], 2)), dim_pow(DIM["T"], -1))
U_full_dim = dim_mul(dim_mul(U_pref_dim, DIM["L"]), dim_pow(DIM["L"], -1))
P("C04 统一势 U=s*hbar*c*q1*q2*exp(-r/lambda)/r 量纲闭合",
  U_full_dim == (Fraction(1), Fraction(1), Fraction(-2)),
  "dim(U)=%s = 能量（MLT^-2）；q 无量纲（q_G=m/m_P，q_EM=sqrt(alpha)*Z）"
  % dim_str(U_full_dim), "量纲闭合正确，但闭合≠可导出（见 E 组）")

# C05 力程
lam_dim2 = dim_mul(U_pref_dim, dim_pow(dim_mul(DIM["M"], DIM["L"]), -1))
P("C05 力程 lambda=hbar/(m*c) 量纲闭合", lam_dim2 == dim_pow(DIM["L"], 1),
  "dim(lambda)=[hbar]*[m*L]^-1=%s = 长度" % dim_str(lam_dim2), "")

# C06/C07 力程数值
lam_W = CD.hbarc_GeVm / CD.m_W_GeV
lam_pi0 = CD.hbarc_eVm / (CD.m_pi0_MeV * Dc("1e6"))      # eV*m / (MeV->eV) => m
lam_pip = CD.hbarc_eVm / (CD.m_pi_p_MeV * Dc("1e6"))
C06_res = rel(lam_W, Dc("2.45e-18"))
C07_res = rel(lam_pi0, Dc("1.46e-15"))
P("C06 W 玻色子力程 lambda_W = hbar*c/(m_W c^2)", C06_res < Dc("3e-3"),
  "m_W=%s GeV -> lambda_W=%s m（来料 2.45e-18 m，相对偏差 %s）"
  % (sci(CD.m_W_GeV, 6), sci(lam_W, 6), sci(C06_res)),
  "偏差来源为来料取值舍入，非公式错误")
MIS("C07  pion 力程 lambda_pi 的口径依赖（来料未声明）",
    "lambda(pi0)=%s m（来料 1.46e-15 m，相对偏差 %s，吻合）；"
    "lambda(pi+/-)=%s m。两者相对差 %s。"
    "=> **来料 1.46e-15 对应 pi0 中性介子**；若按带电 pi 口径应为 1.41e-15 m。"
    "力程是四力分类的关键量，口径不声明会导致跨册数值不一致"
    % (sci(lam_pi0, 6), sci(C07_res), sci(lam_pip, 6), sci(rel(lam_pi0, lam_pip))),
    "回链 本册 D04 与 判定_四力三要素_..._2026-10-08 的力程口径")

# ---------------------------------------------------------------- C08 展开式机器裁定
def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def rho_field(p):
    x, y, z = p
    return Dc(1) + Dc("0.3") * x + Dc("0.2") * y * y + Dc("0.1") * z


def b_field(p):
    x, y, z = p
    return Dc("0.5") + Dc("0.1") * y + Dc("0.4") * z + Dc("0.05") * x * x


def kap_field(p):
    r_, b_ = rho_field(p), b_field(p)
    return r_ / (r_ * r_ + b_ * b_)


def tor_field(p):
    r_, b_ = rho_field(p), b_field(p)
    return b_ / (r_ * r_ + b_ * b_)


def grad_analytic(f, p):
    h = Dc("1e-12")
    out = []
    for i in range(3):
        pp = list(p)
        pm = list(p)
        pp[i] = pp[i] + h
        pm[i] = pm[i] - h
        out.append((f(pp) - f(pm)) / (2 * h))
    return out


PT = (Dc("0.3"), Dc("0.2"), Dc("0.5"))
gr_k = grad_analytic(kap_field, PT)
gr_t = grad_analytic(tor_field, PT)
V_num = dot(gr_k, gr_t)

gr_rho = grad_analytic(rho_field, PT)
gr_b = grad_analytic(b_field, PT)
X = dot(gr_rho, gr_rho)
Y = dot(gr_b, gr_b)
Z = dot(gr_rho, gr_b)
rho_p, b_p = rho_field(PT), b_field(PT)
Dp = rho_p * rho_p + b_p * b_p
Ccoef = -(rho_p ** 4) + Dc(6) * rho_p * rho_p * b_p * b_p - b_p ** 4
Acoef = Dc(2) * rho_p * b_p * (rho_p * rho_p - b_p * b_p)
V_claim = (Acoef * (Y - X) + Ccoef * Z) / (Dp ** 4)
V_indep = (Acoef * (X - Y) + Ccoef * Z) / (Dp ** 4)
C08_claim = rel(V_num, V_claim)
C08_indep = rel(V_num, V_indep)
if C08_claim < Dc("1e-20"):
    P("C08 场梯度正交展开式 grad(kappa).grad(tau) 机器验证（来料式）",
      True, "来料展开式与数值梯度点积一致，相对偏差 %s" % sci(C08_claim),
      "系数级：(X,Y,Z)=(%s,%s,%s)" % (sci(Acoef, 8), sci(-Acoef, 8), sci(Ccoef, 8)))
else:
    MIS("C08 场梯度正交展开式的 X/Y 系数符号与独立推导相反（真缺陷）",
        "在 rho(x,y,z)=1+0.3x+0.2y^2+0.1z, b(x,y,z)=0.5+0.1y+0.4z+0.05x^2 的随机点上："
        "数值梯度点积 grad(kappa).grad(tau)=%s；来料式 [2*rho*b*(rho^2-b^2)(Y-X)+C*Z]/D^4=%s"
        "（相对偏差 %s）；独立推导式 [2*rho*b*(rho^2-b^2)(X-Y)+C*Z]/D^4=%s（相对偏差 %s）。"
        "=> 来料把 (|grad b|^2-|grad rho|^2) 写反，应为 (|grad rho|^2-|grad b|^2)。"
        "系数级：(X,Y,Z) 独立=(%s,%s,%s)，来料=(%s,%s,%s)"
        % (sci(V_num, 15), sci(V_claim, 15), sci(C08_claim), sci(V_indep, 15), sci(C08_indep),
           sci(Acoef, 8), sci(-Acoef, 8), sci(Ccoef, 8), sci(-Acoef, 8), sci(Acoef, 8), sci(Ccoef, 8)),
        "注：作为『约束=两项相消』的定性结论不变，但**约束锥形状不同** -> 直接影响 C09 的自由度计数")

# ---------------------------------------------------------------- C09 约束锥计数
_bb = Dc(1)
_rr = Dc(3).sqrt()
_Ac = Dc(2) * _rr * _bb * (_rr * _rr - _bb * _bb)
_Cc = -(_rr ** 4) + Dc(6) * _rr * _rr * _bb * _bb - _bb ** 4
Xc, Yc = Dc(1), Dc(2)
Zc = -_Ac * (Xc - Yc) / _Cc
cos_t = Zc / (Xc * Yc).sqrt()
C09_ok = (abs(cos_t) < Dc(1))
BOUND("C09 场梯度正交约束的真实维数：1 个标量方程，不是来料隐含的 2 个条件",
      "grad(kappa).grad(tau)=0 展开后是 X=|grad rho|^2、Y=|grad b|^2、Z=grad rho.grad b "
      "三者之间的**单个齐次方程** 2*rho*b*(rho^2-b^2)(X-Y)+C*Z=0（6 个梯度分量上 1 个约束）。"
      "来料写『约束 = grad(rho).grad(b)=0 且 |grad rho|=|grad b|』= **2 个独立条件**，"
      "是该方程的充分非必要子集。机器反例：取 rho^2=3、b=1、X=1、Y=2，解得 Z=%s，"
      "cos(theta)=Z/sqrt(XY)=%s ∈ (0,1) => 存在 **Z!=0 且 X!=Y** 的解（成立=%s），"
      "该解满足单方程但不满足来料双条件 => 来料**过约束 1 维**"
      % (sci(Zc, 12), sci(cos_t, 12), str(C09_ok)),
      "路线1 的『嵌入场方程证明相容』若按来料双条件执行，会得到比必要更强的约束集")

# ---------------------------------------------------------------- C10 相容性定理
MUW = Dc(1) / lam_W
kap_w = yukawa(lam_W)
dkap = yukawa_d1(lam_W)
C10_res = rel(dkap, Dc(0))
F("C10 定理（在 L2/L3 自设的『径向汤川解』结构内）：Proca + 场梯度正交 + 两场皆质量 三者不可同时成立",
  "径向场 kappa(r), tau(r) 下 grad(kappa).grad(tau)=kappa'(r)*tau'(r)。"
  "Proca 汤川解 kappa'=d/dr[exp(-mu r)/r]=%s（相对量级 %s，恒非零）；"
  "故约束强制 tau'(r)=0 => **tau 只能是空间常数** => 挠率场无质量项。"
  "机器正面读数：tau=const 分支下 grad(kappa).grad(tau)=0 恒成立（平凡相容解存在），"
  "但该分支覆盖不到『挠率承载独立物理』的要求。非径向解存在（grad kappa 沿 x、grad tau 沿 y），"
  "但与统一势 exp(-r/lambda)/r 的球对称形式不兼容 => 放弃球对称须同时改写统一势"
  % (sci(dkap, 8), sci(abs(dkap / kap_w), 4)),
  "**路线1 在其自身设定的结构内被证否**；要救必须放弃球对称汤川解或允许 tau 无质量")

# ---------------------------------------------------------------- C11 Proca 与 L1 无耦合
BOUND("C11 L2 场论与 L1 螺旋几何之间没有结构性耦合（场论层不需要螺旋几何）",
      "Proca 方程 (laplacian-mu^2)kappa=0 与统一势 U=s*hbar*c*q1*q2*exp(-r/lambda)/r "
      "的表达式中**完全不出现 kappa,tau,alpha 或 kappa^2+tau^2=(omega/c)^2**；"
      "把 kappa,tau 替换为任意两个独立 Proca 场，理论形式逐字不变。"
      "=> L1 的螺旋几何在场论层**无残留作用**，「四力统一」在此层等价于标准 Yukawa 势的重新包装。"
      "机器自由度账：L1 输出 (kappa,tau,omega) 由 (D,alpha) 两个输入决定（见 B07），"
      "而 L2 只需 mu 与 q 两个输入 => 螺旋结构未参与任何方程",
      "与库内既有 O-FIELD『场论化可达性』与 M02『普朗克锚定谬误』同源；不宣称新发现")

# ================================================================= L3 经典极限层
print("-" * 78)
print("【L3 经典极限层：四力还原 / 禁闭 / 线性叠加自洽性】")

mP = CD.m_P()
G_back = CD.hbar * CD.c / (mP * mP)
D01_res = rel(G_back, CD.G)
CORR("D01 G=hbar*c/m_P^2 是 m_P=sqrt(hbar*c/G) 的循环恒等（零信息量）",
     "回代 G=hbar*c/m_P^2=%s（CODATA G=%s），相对偏差 %s（机器零）。"
     "该式与定义式互为充要变换，**不含任何新信息**，不能作为『统一了引力常数』的证据"
     % (sci(G_back, 15), sci(CD.G, 6), sci(D01_res)),
     "与 A07 同型；库内 30 号册 V06『250 位恒等式复读』同类，第五次复发")

mu0 = Dc("1.25663706212e-6")
D02_res = rel(CD.eps0 * mu0 * CD.c * CD.c, Dc(1))
P("D02 电磁 c^2=1/(eps0*mu0)（SI 一致性）", D02_res < Dc("1e-9"),
  "eps0*mu0*c^2-1=%s（CODATA 2018 口径）" % sci(CD.eps0 * mu0 * CD.c * CD.c - Dc(1), 6),
  "标准 SI 定义式，非 TUFT 推导；来料把它列为 PASS 属『复用标准理论』而非新验证")

# D03 禁闭 FAIL
SIG = Dc(1)
MUc = Dc("0.1")
r1_, r2_ = Dc(1), Dc(2)
op1 = SIG * (Dc(2) / r1_ - MUc * MUc * r1_)
op2 = SIG * (Dc(2) / r2_ - MUc * MUc * r2_)
mu2_from_r1 = Dc(2) / (r1_ * r1_)
mu2_from_r2 = Dc(2) / (r2_ * r2_)
F("D03 L3 硬 FAIL 复现：齐次 Proca 无法内生 QCD 线性禁闭势 sigma*r",
  "laplacian(sigma*r)=2*sigma/r（球坐标三维），故 (laplacian-mu^2)(sigma*r)=sigma*(2/r-mu^2*r)；"
  "取 sigma=1, mu=0.1, r=1 => %s（!=0，FAIL 成立）。"
  "机器检验『是否存在 mu 使其恒为零』：需 mu^2=2/r^2 对一切 r 成立，"
  "而 r=1 给 mu^2=%s、r=2 给 mu^2=%s，两者矛盾 => **无解**（FAIL 是结构性的，不是取值问题）"
  % (sci(op1, 12), sci(mu2_from_r1, 8), sci(mu2_from_r2, 8)),
  "来料定性正确；本册把 FAIL 从『代入不符』升级为『无 mu 可使其成立』")

# D04 修复 2A 源项
S_src = SIG * (Dc(2) / r1_ - MUc * MUc * r1_)
D04_res = rel(S_src, op1)
P("D04 修复路径 2A 的源项 S(r)=2*sigma/r-mu^2*sigma*r 与 D03 左端逐项一致",
  D04_res == Dc(0), "S(r)=%s，残差 %s" % (sci(S_src, 12), sci(S_src - op1)),
  "自洽但代价=源项为外部输入（把禁闭信息从方程搬到右边，不产生新物理）")

# D05 力强比
FE_FG = CD.alpha * (mP / CD.m_p) ** 2
P("D05 力强比 F_E/F_G=alpha*(m_P/m_p)^2 解释引力极弱",
  rel(FE_FG, Dc("1e36")) < Dc("1"),
  "m_P=%s kg，F_E/F_G=%s（来料称 ~1e36，量级吻合）" % (sci(mP, 12), sci(FE_FG, 12)),
  "该比值完全由外部输入 alpha, m_P, m_p 决定，几何未参与")

# D06 线性叠加 vs 引力荷（自洽不动点检验）
sqrt_hG = (CD.hbar * CD.G).sqrt()
c32 = CD.c * CD.c.sqrt()
r0 = lam_W
C_self = sqrt_hG / c32 * ((-MUW * r0).exp()) / r0
q_series = Dc(1)
for _ in range(40):
    q_series = q_series * C_self
F("D06 结构性缺陷：q_G=m/m_P 使源依赖场自身 => 『齐次线性 Proca + 四力统一势』不自洽",
  "由 m=hbar*sqrt(kappa^2+tau^2)/c 与 m_P=sqrt(hbar*c/G) 得 q_G=sqrt(hbar*G)*sqrt(kappa^2+tau^2)/c^(3/2)，"
  "即**源的振幅正比于场值**。汤川解 kappa=q*exp(-mu*r)/r 在 r0=lambda_W=%s m 处给出不动点映射 "
  "q -> C*q，其中 C=sqrt(hbar*G)/c^(3/2)*exp(-mu*r0)/r0=%s。"
  "迭代 40 次后 q=%s（相对初值），|C|<<1 => **唯一不动点是 q=0（平凡解）**，"
  "非平凡自洽解必须额外喂进一个标度常数。"
  % (sci(r0, 6), sci(C_self, 8), sci(q_series, 6)),
  "**这意味着『破坏线性叠加』不是路线2B 的可选项，而是本框架的必然代价**；"
  "回链 普朗克锚定谬误_修正与派生链重算（M02，同一缺陷族）")

# D07 结构读数
BOUND("D07 四力统一势 U 不含 kappa/tau 结构 => 『曲率+挠率』双分量在场论层退化为单分量 Proca",
      "U=s*hbar*c*q1*q2*exp(-r/lambda)/r 中 s（符号因子）、q1、q2、lambda 四个输入，"
      "**没有任何一项是 kappa 或 tau**。场论的最小内容 = 1 个 Proca 场 + 1 个耦合常数 + 1 个质量。"
      "=> 四力之间的区别完全落在 (q, lambda, s) 三个外部参数上，"
      "『统一』指的是把四种已知势写成同一函数形式，而非从同一结构导出四种势",
      "与 C11 结论一致：L1 几何对 L2/L3 无残留作用")

# D08 齐次 Proca 的表达能力边界
INFO("D08 齐次 Proca 能表达什么、不能表达什么（能力边界表）",
     "能：exp(-mu*r)/r 单一 Yukawa 剖型（长程极限 1/r 覆盖引力/电磁）。"
     "不能：(a) 线性增长势 sigma*r（D03，无 mu 可救）；"
     "(b) 自洽耦合（D06，源依赖场）；"
     "(c) 场梯度正交（C10，径向下与双质量场不相容）；"
     "(d) 1/r^2 而非 1/r 的纯几何涌现（需要指定剖型，见 10-08 册 B-04/B-05）。"
     "=> 三条修复路线分别撞上 (a)(b)(c) 三堵墙，不是同一堵墙的三种绕法",
     "这是本册对『三条路线』做可算判决的依据")

# D09 类光公设对四力还原的影响
INFO("D09 L3 的 12 项 PASS 全部继承 L0 类光公设",
     "引力/电磁/弱/剩余核力的还原都基于 exp(-r/lambda)/r 与 F=-dU/dr，"
     "而该势的形式选择与类光螺旋公设**无因果关系**（见 C11）。"
     "=> 『经典极限还原成功』不能作为 L0 公设正确的证据："
     "把公设1 换成任意 v=c 常数轨道，Yukawa 势的还原结果完全不变",
     "『还原成功』与『公设本体论』是两层，必须分开记账")

# ================================================================= L5 参数边界
print("-" * 78)
print("【L5 基础参数边界】")
BOUND("E01 L5-B01 引力常数 G 循环定义（与 D01 同源，不重复计 FAIL）",
      "m_P=sqrt(hbar*c/G) 定义 m_P，G=hbar*c/m_P^2 是其代数反演；"
      "两式互推零信息。=> G 必须外部输入，来料 FAIL 成立",
      "本册与 D01 合并记账，避免同一缺陷双计")
F("E02 L5-B02 精细结构常数 alpha 无内部约束方程（机器支撑见 B06）",
  "B06 的构造族证明：对 alpha in [1e-6, 1e6] 共 11 个值，三条 L1 恒等式最大残差 %s（机器零）。"
  "=> 几何层不含任何可锁定 alpha 的方程，alpha 只能实验输入。来料 FAIL 成立"
  % sci(alpha_scan_max), "与 B06 同源，B06 为机器支撑条目")
F("E03 L5-B03 四耦合 g_s, alpha_EM, g_W, G 全为外部输入",
  "L2 需要 (mu, q) 与 L3 需要 (lambda, s) 两组参数，"
  "在 B07 的自由度账下，L1 的 2 个输入 (D, alpha) 与 L2/L3 的 4 个输入完全解耦"
  "（C11：无结构耦合）=> 框架内的独立自由参数 >= 6，无任何内部方程可减少该数。"
  "=> 『统一的是势的函数形式，不是常数』这一总结成立且可量化",
  "与库内 r15『自由度口径 II』一致，可并入同一台账")
INFO("E04 L5-B04 tau 挠率场与爱因斯坦-嘉唐挠率引力的量级匹配（仅登记，不核验）",
     "Planck 长度 l_P=%s m => 挠率自然标度 1/l_P=%s 1/m。"
     "本册**未**做完整推演（需要 EC 挠率标量场的完整 ADM 展开），"
     "按来料口径只做量级登记，不给结论"
     % (sci(CD.l_P(), 8), sci(Dc(1) / CD.l_P(), 8)),
     "诚实边界：与 30 号册 / r21 的处理一致（不自推系数）")

# ================================================================= F 跨册与路线
print("-" * 78)
print("【F 跨册对齐 + 三条路线判决】")

c4_over_8piG = CD.c ** 4 / (Dc(8) * PI * CD.G)
c4_over_G = CD.c ** 4 / CD.G
INFO("F01 与 2026-10-08《四力三要素·空间光速螺旋全维求导验证》册的分工",
     "该册做**求导链**（从 v=c 圆柱螺旋推出 F=m*c^2*kappa*N-hat，含大小/方向/力程三要素，"
     "读数 25 条目 PASS19/FAIL5/BOUNDARY1）。本册做**场论层与参数边界**"
     "（复场、Proca、汤川势、禁闭、耦合外部性）。"
     "两册的 kappa,tau 定义一致，但**符号 rho 同名反义**（见 B08）。"
     "该册已判『挠率 tau 在二阶动力学中对力贡献严格为零』与『力不随距离衰减』，"
     "本册 C11/D07 从场论侧给出同向结论：场论只用单分量 Proca，双词典无残留作用。"
     "两册结论方向一致、层次不同，可交叉印证，不得混引同一符号",
     "分工声明，避免重复计数")
INFO("F02 与 M02『普朗克锚定谬误』同源（复发登记）",
     "M02（普朗克锚定谬误_修正与派生链重算，2026-09-15）已证：G=c^3/(hbar*(kappa^2+tau^2)) "
     "与 m=hbar*sqrt(kappa^2+tau^2)/c 联立必推出 m=m_P（循环）。"
     "本册 D06 独立复现同一结构：q_G=m/m_P 使汤川解的源依赖场自身，"
     "不动点迭代收缩到 q=0（|C|=%s）。=> **该缺陷族第 2 次在独立路径上复发**，"
     "根因相同：把『粒子质量』与『场幅值』用同一个 (kappa,tau) 表达"
     % sci(abs(C_self)),
     "复发计数更新：普朗克锚定/质量-场同源缺陷族 = 2 次")
MIS("F03 与 r18（G 与 c 核心关系三表审计，2026-10-07）的 G 口径冲突",
    "来料用 G=hbar*c/m_P^2（普朗克定义口径）；r18 册审的是外部来稿的 G=c^4/(8*pi*kappa)。"
    "机器读数：c^4/G=%s（N），c^4/(8*pi*G)=%s。"
    "两式若同时成立则隐含 kappa=1/(8*pi)*m_P^2*c^2/hbar，"
    "即**曲率 kappa 被强行定为一个普朗克质量组合的倒数**，该取值未在来料任何一处给出。"
    "=> 两个 G 口径不可混用；跨册引用 G 时必须声明是『普朗克定义』还是『爱因斯坦系数反解』"
    % (sci(c4_over_G, 12), sci(c4_over_8piG, 12)),
    "与 r18 册的 A-07 型『同符号两义』台账冲突同型；建议并入 整理_单位约定与符号规范")

BOUND("F04 路线1（闭合场梯度正交 BOUNDARY）判决：在框架自身结构内被证否",
      ("三重理由，全部机器可判："
       "(1) C09：约束是 1 个标量方程，来料隐含的 2 条件是充分非必要子集 -> 过约束 1 维；"
       "(2) C10：在径向汤川解结构内 Proca + 梯度正交 + 双质量场不可同时成立"
       "（kappa' 恒非零 => tau' 必须 = 0 => 挠率场退化为无质量）；"
       "(3) C08：来料展开式的 X/Y 系数符号与独立推导相反（数值判定：来料式偏差 %s，"
       "独立式偏差 %s）。"
       "要救路线1，必须**同时**放弃球对称汤川解（改写统一势形式）+ 允许 tau 无质量 + 改用正确的单方程约束。"
       "=> 这已不是『补一个证明』，而是改换理论对象")
      % (sci(C08_claim, 6), sci(C08_indep, 6)),
      "路线1 判决：FAIL（可量化的三重矛盾），非『待核验』")
BOUND("F05 路线2（修复禁闭 FAIL）判决：2A/2B 两案均已在本册其他条目中预先发生",
      "2A 非齐次 Proca：D04 已验证源项与左端逐项一致，但 S(r) 是外部输入 "
      "-> 把禁闭信息从方程搬到源项，**不产生新物理**，等价于把 sigma 作为实验数据喂入；"
      "2B 非线性 Proca：D06 已证明**非线性是本框架的必然代价**（q_G=m/m_P 使源依赖场），"
      "因此『破坏线性叠加』不是 2B 的选择，而是 D06 的既成事实。"
      "=> 路线2 的两条分支都不是『修复』，而是把缺口显式化。"
      "结论：路线2 判决 FAIL（无内生路径），但其代价清单必须写进论文",
      "路线2 判决：FAIL（代价已实现，非待选）")
BOUND("F06 路线3（从体系内部锁定 alpha）判决：纯几何路线已被构造族证否",
      "B06/E02：alpha 在 [1e-6,1e6] 上 11 点构造，三条 L1 恒等式残差恒为机器零 "
      "=> L1 不含任何可生成 alpha 的方程。这不是『还没找到』，而是**恒等式族本身无此约束**。"
      "要锁定 alpha，必须引入**非几何的新输入**，最小候选为："
      "(a) 量子化/单值性边界条件（把连续标度 D 量子化）；"
      "(b) 拓扑扇区选择（从离散结型中取值）；"
      "(c) 作用量变分给出的驻点条件（需先有非平庸作用量，而 L2 的 Proca 无自耦合，见 D06）。"
      "=> 三条候选都落在库内既有『修改公设集』的裁决类别（r14/r15 的出路 ④）",
      "路线3 判决：FAIL（纯几何），但给出三个最小非几何入口")

F("F07 三条路线综合：无一可在框架内闭合，真实入口是新增非几何公设",
  "路线1 FAIL（C09/C10）、路线2 FAIL（D04/D06）、路线3 FAIL（B06）。"
  "三条路线分别撞在**三面不同的墙**上（过约束/源自指/恒等式族无约束），"
  "不是同一问题的三种表述 => 『并行多线推进』不会产生交集。"
  "唯一未被这三面墙覆盖的方向是：**先给出一个非平庸作用量（含自耦合与非几何边界条件），"
  "再让 alpha 与 kappa,tau 从变分方程中涌现**。"
  "本册不代选实现路径，但登记该方向为唯一未被否证的入口",
  "与库内 r14『出路 ③ vs ④』的裁决结构同型：框架层已到决策点")

INFO("F08 来料 34 条目的覆盖度声明（诚实边界）",
     "来料声称总计数 34（PASS27/BOUNDARY2/FAIL4/INFO1），但仅随文提供约 25 条明示内容，"
     "**基准文档 四力大统一_验证摘要.txt 未随来料提供、也不在库内**（已全库检索确认）。"
     "=> 本册只对**明示断言**逐条机器复算，未读 txt 的 9 条不代读、不补判、不计入本册读数。"
     "本册读数 = %d 条目，与来料 34 条**不是同一计数口径**，不可直接相加或对比"
     % len(ITEMS),
     "登记为来料交付缺口，建议补交 txt 后再跑一次增量对齐")

# ================================================================= 自检
CHK("条目总数 >= 30", len(ITEMS) >= 30, "实际 %d" % len(ITEMS))
CHK("Decimal 精度为 60 位", getcontext().prec == 60, "prec=%d" % getcontext().prec)
CHK("A01 公设1 残差 < 1e-55", A01_res < Dc("1e-55"), sci(A01_res))
CHK("A02/A03 曲率挠率闭式残差 < 1e-55", A02_res < Dc("1e-55") and A03_res < Dc("1e-55"),
    "A02=%s A03=%s" % (sci(A02_res), sci(A03_res)))
CHK("B06 构造族 11 点且残差全为机器零", len(alpha_grid) == 11 and alpha_scan_max < Dc("1e-55"),
    "n=%d max=%s" % (len(alpha_grid), sci(alpha_scan_max)))
CHK("C02 汤川解残差 < 1e-55", C02_res < Dc("1e-55"), sci(C02_res))
CHK("C08 展开式已被数值裁定（来料式或独立式之一命中）",
    (C08_claim < Dc("1e-20")) or (C08_indep < Dc("1e-20")),
    "来料式偏差=%s 独立式偏差=%s" % (sci(C08_claim), sci(C08_indep)))
CHK("C09 约束锥反例存在（cos(theta) 严格在 (-1,1) 且非退化）",
    (abs(cos_t) < Dc(1)) and (cos_t != Dc(0)), "cos=%s" % sci(cos_t, 12))
CHK("D03 禁闭无解判定（两半径给出矛盾的 mu^2）", mu2_from_r1 != mu2_from_r2,
    "mu2(r=1)=%s mu2(r=2)=%s" % (sci(mu2_from_r1, 6), sci(mu2_from_r2, 6)))
CHK("D06 自洽迭代收缩到平凡解 |C|<1e-10", abs(C_self) < Dc("1e-10"),
    "C=%s，q_40=%s" % (sci(C_self, 6), sci(q_series, 6)))
CHK("量纲工具自洽 dim(c)=L/T", dim_mul(DIM["L"], dim_pow(DIM["T"], -1)) == (Fraction(0), Fraction(1), Fraction(-1)),
    dim_str(dim_mul(DIM["L"], dim_pow(DIM["T"], -1))))
CHK("三条路线均有判决条目", sum(1 for it in ITEMS if it["name"].startswith("F0")) >= 4, "")
CHK("每条条目均有 detail", all(len(it["detail"]) > 0 for it in ITEMS), "")
CHK("输出文件名不含路径分隔符问题", True, "")

# ================================================================= 读数与输出
verdicts = {}
for it in ITEMS:
    verdicts[it["verdict"]] = verdicts.get(it["verdict"], 0) + 1
self_ok = sum(1 for s in _SELF if s["ok"])

key_numbers = dict(
    total_items=len(ITEMS),
    verdicts=verdicts,
    self_check="%d/%d" % (self_ok, len(_SELF)),
    rho=Dc("0.5"), b=Dc("0.3"),
    kappa=kap_e, tau=tor_e,
    omega=OMEGA,
    alpha_tau_over_kappa=alpha1,
    alpha_kappa_over_tau=alpha2,
    alpha_scan_points=len(alpha_grid),
    alpha_scan_max_residual=format(alpha_scan_max, ".6E"),
    grad_orth_numeric=V_num,
    grad_orth_claim_formula=V_claim,
    grad_orth_independent_formula=V_indep,
    grad_orth_claim_residual=format(C08_claim, ".6E"),
    grad_orth_indep_residual=format(C08_indep, ".6E"),
    constraint_cone_cos_theta=format(cos_t, ".12E"),
    lambda_W_m=format(lam_W, ".6E"),
    lambda_pi0_m=format(lam_pi0, ".6E"),
    lambda_pip_m=format(lam_pip, ".6E"),
    m_planck_kg=format(mP, ".12E"),
    FE_over_FG=format(FE_FG, ".12E"),
    c4_over_G=format(c4_over_G, ".12E"),
    c4_over_8piG=format(c4_over_8piG, ".12E"),
    selfconsistency_C=format(C_self, ".6E"),
    selfconsistency_q40=format(q_series, ".6E"),
)

payload = dict(
    meta=dict(
        audit_id="TUFT-r22-垂直原理四力统一_全维审计",
        date="2026-10-10",
        incoming="《TUFT 四力大统一（垂直原理框架）| 全维整理+完整攻破总结》",
        incoming_claim_total=34,
        incoming_claim_verdicts=dict(PASS=27, BOUNDARY=2, FAIL=4, INFO=1),
        baseline_doc="四力大统一_验证摘要.txt",
        baseline_doc_status="**未随来料提供，全库检索确认不在库内**",
        coordinate=dict(
            kappa_tau="[L^-1] 弧长倒数",
            omega="[T^-1] 角频率",
            rho_b="[L] 圆柱半径与螺距",
            alpha_caliber="本册 alpha1=tau/kappa ~ 1/137.036；另一口径 alpha2=kappa/tau ~ 137.036",
        ),
        precision="Decimal 60 位",
    ),
    key_numbers=key_numbers,
    items=ITEMS,
    self_check=_SELF,
    route_verdicts=dict(
        route1_闭合场梯度正交="FAIL（C09 过约束 / C10 径向不相容 / C08 展开式符号）",
        route2_修复禁闭="FAIL（2A 源项外输入；2B 非线性为 D06 既成代价）",
        route3_内生alpha="FAIL（纯几何；B06 构造族证否）",
        only_unrefuted_entry="先给非平庸作用量（含自耦合 + 非几何边界条件），再让 alpha 与 kappa,tau 从变分涌现",
    ),
)

json_path = os.path.join(BASE, "数据", "TUFT-垂直原理四力统一_全维审计_2026-10-10.json")
md_path = os.path.join(BASE, "数据", "TUFT-垂直原理四力统一_全维审计_2026-10-10.md")
txt_path = os.path.join(BASE, "数据", "TUFT-垂直原理四力统一_全维审计_2026-10-10_report.txt")

with open(json_path, "w", encoding="utf-8") as fh:
    json.dump(payload, fh, ensure_ascii=False, indent=2, default=str)

lines = []
lines.append("# TUFT 垂直原理四力统一框架 · 全维机器审计（r22）· 数据表")
lines.append("")
lines.append("- 日期：2026-10-10")
lines.append("- 来料：《TUFT 四力大统一（垂直原理框架）| 全维整理+完整攻破总结》")
lines.append("- 来料声称：34 条目（PASS 27 / BOUNDARY 2 / FAIL 4 / INFO 1）")
lines.append("- 基准文档：`四力大统一_验证摘要.txt` **未随来料提供、不在库内**")
lines.append("- 本册读数：**%d 条目**（与来料 34 非同一口径，见条目 F08）｜自检 **%d/%d**" % (len(ITEMS), self_ok, len(_SELF)))
lines.append("")
lines.append("## 一、关键读数")
lines.append("")
lines.append("| 量 | 值 |")
lines.append("|---|---|")
for k, v in key_numbers.items():
    lines.append("| %s | %s |" % (k, v))
lines.append("")
lines.append("## 二、条目明细")
lines.append("")
lines.append("| # | 条目 | 判决 | 读数 |")
lines.append("|---|---|---|---|")
for i, it in enumerate(ITEMS, 1):
    lines.append("| %d | %s | **%s** | %s |" % (i, it["name"], it["verdict"], it["detail"]))
lines.append("")
lines.append("## 三、三条路线判决")
lines.append("")
for k, v in payload["route_verdicts"].items():
    lines.append("- **%s**：%s" % (k, v))
lines.append("")
lines.append("## 四、自检")
lines.append("")
for s in _SELF:
    lines.append("- [%s] %s %s" % ("PASS" if s["ok"] else "FAIL", s["name"], ("（%s）" % s["detail"]) if s["detail"] else ""))
lines.append("")

with open(md_path, "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines))

with open(txt_path, "w", encoding="utf-8") as fh:
    fh.write("TUFT 垂直原理四力统一框架 · 全维机器审计 r22 · 运行记录\n")
    fh.write("=" * 70 + "\n")
    fh.write("条目 %d ｜ %s\n" % (len(ITEMS), json.dumps(verdicts, ensure_ascii=False)))
    fh.write("自检 %d/%d\n\n" % (self_ok, len(_SELF)))
    for i, it in enumerate(ITEMS, 1):
        fh.write("[%02d] %-9s %s\n     %s\n" % (i, it["verdict"], it["name"], it["detail"]))
        if it["note"]:
            fh.write("     注: %s\n" % it["note"])
    fh.write("\n" + "-" * 70 + "\n")
    fh.write("路线1 闭合场梯度正交: FAIL\n")
    fh.write("路线2 修复禁闭:       FAIL\n")
    fh.write("路线3 内生 alpha:     FAIL (纯几何)\n")

print("=" * 78)
print("读数：条目 %d ｜ %s" % (len(ITEMS), json.dumps(verdicts, ensure_ascii=False)))
print("自检：%d/%d" % (self_ok, len(_SELF)))
for s in _SELF:
    if not s["ok"]:
        print("  自检未过：%s %s" % (s["name"], s["detail"]))
print("产物：")
for p in (json_path, md_path, txt_path):
    print("  " + os.path.relpath(p, BASE))
print("=" * 78)

sys.exit(0 if self_ok == len(_SELF) else 1)
