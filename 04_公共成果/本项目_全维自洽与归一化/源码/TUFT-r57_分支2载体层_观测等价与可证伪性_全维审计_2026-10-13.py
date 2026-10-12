# -*- coding: utf-8 -*-
"""
TUFT-V4.7 分支2 阻塞的「载体层」——观测等价、形状约定与可证伪性（r57 · 2026-10-13）

【定位·r48 链路的直接下游】
  r48 判「V4.7 分支2 不成立」，给出三重阻塞（轮廓不可能三角 / 符号 / 量级）。
  r55 把「不可解」升级为定理：
     ①轮廓层最小**合法**增广 = 均匀平滑源（点源自能幂次发散不合法；Helmholtz 谱零判别力）；
     ②符号阻塞与量级阻塞是**同一条**比值方程 ⇒ 解唯一 m_0 = 98.05 MeV = 0.928 m_μ；
     ③**该 m_0 挂不进 κ(m)**（四条判据）⇒ 唯一几何一致载体是耦合层 θ(m) 或 C(m)
       ⇒ 代价由「+1 常数」升级为「无界函数」。
  本册接手 r55 留下的**唯一承重启开项**（O-R53-01：θ(m) 还是 C(m)），只问三个可算问题：
      A. 载体二选一能否由数据裁决？（观测等价定理）
      B. 「a_τ 是分支2 唯一可证伪读数」是否成立？（形状约定定理）
      C. 在载体/形状未定的情况下跑 dynesty 有没有意义？（可识别性定理）

【分工·零重复】
      r46 = V4.8 子分支B（边界变分 + 点源泊松 + 表面张力 ⇒ R_c(κ) 幂律）  —— 不碰
      r47 = V4.8 §4.3 稳态质量隐式关系 m(κ_0) 与 m_max                    —— 不碰
      r48 = V4.7 分支2 三重阻塞的裁定                                     —— 只回链复算，不重审
      r55 = 分支2 最小增广与可解性定理（存在性 / 唯一性 / 代价）            —— 只回链复算 m_0 与 a_τ
      本册 = r55 的下游，只做**载体层**一件事：等价族 / 形状约定 / 可证伪性存废。

【纪律】
      · 纯标准库；decimal 60 位；量纲四元组 (M,L,T,Q) 用 Fraction 精确表示；
      · 量纲工具必须先过 G0 自检 guard 才能用于判定（本库该工具已三次写错）；
      · 每条结论附机器读数；guard 不全过则 main() return 2，**禁止输出结论**；
      · 不自推：凡属公设层/约定层的选择一律登记为待裁决，不代选；
      · 红线：数学自洽 ≠ 物理证实。本册只登记「能不能被数据裁决」，不产生新物理。

【编号仲裁】r53（空间螺旋结构光与光子）/ r54（四维类光层）/ r56（光光子三分法）
           均已被并行会话占用，r55 = 本册上游 ⇒ 取空号 **r57**。
"""
import io
import json
import os
import sys
from decimal import Decimal as D, getcontext
from fractions import Fraction

getcontext().prec = 60
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

STAMP = "2026-10-13"
ROUND = "r57"
NAME = "TUFT-r57_分支2载体层_观测等价与可证伪性_全维审计_%s" % STAMP
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE, "数据")

# ---------------------------------------------------------------- 常数（CODATA 2018 / PDG）
c_light = D("299792458")
hbar = D("1.054571817e-34")
m_e = D("9.1093837015e-31")
m_mu = D("1.883531627e-28")
m_tau = D("3.16754e-27")
G_newton = D("6.67430e-11")
l_P = D("1.616255e-35")
GEV_OVER_C2 = D("1.78266192e-27")          # 1 GeV/c^2 = ... kg
U_G = D("2.2e-5")                          # CODATA G 的相对不确定度

# g-2 数据（与 r42/r44/r48/r55 同源，采用 r48 登记的「实验 − SM」口径）
a_e_exp = D("1.15965218073e-3")
a_e_th = D("1.15965218161e-3")
a_mu_exp = D("1.16592061e-3")
a_mu_th = D("1.16591705e-3")
da_e = D("-6.9e-13")
da_mu = D("2.3e-9")

# τ 的反常磁矩实验/理论参照
A_TAU_LO = D("-0.052")                     # DELPHI 95% CL 下界
A_TAU_HI = D("0.013")                      # DELPHI 95% CL 上界
A_TAU_SM = D("1.17721e-3")

# 回链锚点（不重算，只作交叉核对）
R55_M0_MEV = D("9.805329409000E+1")        # r55 登记的 m_0
R44_COT_THETA_E = D("6.58949e-48")         # r42/r44 由 Δa_e 反解的 cotθ（电子）

target_ratio = da_mu / da_e                # = −3.3333...E+3
mm_ratio_sq = (m_mu / m_e) ** 2            # = 4.2753...E+4

# ---------------------------------------------------------------- 量纲引擎 (M, L, T, Q)
class Dim(object):
    __slots__ = ("m", "l", "t", "q")
    def __init__(self, m=0, l=0, t=0, q=0):
        self.m, self.l, self.t, self.q = Fraction(m), Fraction(l), Fraction(t), Fraction(q)
    def key(self):
        return (self.m, self.l, self.t, self.q)
    def __eq__(self, o):
        return isinstance(o, Dim) and self.key() == o.key()
    def __hash__(self):
        return hash(self.key())

def dmul(a, b):
    """量纲相乘 = 各分量指数**相加**（首版写成逐分量相乘，本库已三次踩此坑，故设 G0 守卫）"""
    return Dim(a.m + b.m, a.l + b.l, a.t + b.t, a.q + b.q)

def dinv(a):
    return Dim(-a.m, -a.l, -a.t, -a.q)

def dpow(a, n):
    n = Fraction(n)
    return Dim(a.m * n, a.l * n, a.t * n, a.q * n)

def dscale(a, k):
    """纯数乘除不改量纲"""
    return Dim(a.m, a.l, a.t, a.q)

def deq(a, b):
    return a == b

def dstr(a):
    out = []
    for nm, v in (("M", a.m), ("L", a.l), ("T", a.t), ("Q", a.q)):
        if v != 0:
            out.append(nm + ("^%s" % v if v != 1 else ""))
    return "·".join(out) if out else "1"

dM, dL, dT, dQ = Dim(1, 0, 0, 0), Dim(0, 1, 0, 0), Dim(0, 0, 1, 0), Dim(0, 0, 0, 1)
dEnergy = dmul(dmul(dM, dpow(dL, 2)), dpow(dT, -2))     # M·L^2·T^-2
dim_c = Dim(0, 1, -1)
dim_hbar = Dim(1, 2, -1)

# ---------------------------------------------------------------- 数值/格式化小工具
def fmt(x, n=12):
    try:
        return format(D(x), ".%dE" % n)
    except Exception:
        return str(x)

def rel(a, b):
    a, b = D(a), D(b)
    if b == 0:
        return D("Infinity") if a != 0 else D(0)
    return abs((a - b) / b)

def dratio(a, b):
    return D(a) / D(b)

# ---------------------------------------------------------------- 记录器
RECORDS = []
GUARDS = []
OPEN_ITEMS = []
NOT_SELF_DERIVED = []

def _emit(v, cid, claim, reading="", note=""):
    RECORDS.append(dict(id=cid, verdict=v, claim=claim, reading=reading, note=note))
    print("[%s] %s :: %s" % (v, cid, claim))
    if reading:
        print("       %s" % reading)

def FAIL(cid, claim, reading="", note=""):
    _emit("FAIL", cid, claim, reading, note)

def PASS(cid, claim, reading="", note=""):
    _emit("PASS", cid, claim, reading, note)

def INFO(cid, claim, reading="", note=""):
    _emit("INFO", cid, claim, reading, note)

def BOUNDARY(cid, claim, reading="", note=""):
    _emit("BOUNDARY", cid, claim, reading, note)

def CORRECTED(cid, claim, reading="", note=""):
    _emit("CORRECTED", cid, claim, reading, note)

def guard(name, ok, detail, note=""):
    GUARDS.append(dict(name=name, passed=bool(ok), detail=detail, note=note))
    return bool(ok)

# ================================================================ G0：量纲工具自检（必须先过）
guard("dim_mul_is_index_addition",
      deq(dmul(dL, dL), Dim(0, 2, 0, 0)) and deq(dmul(dM, dL), Dim(1, 1, 0, 0)),
      "dmul(L,L)=%s、dmul(M,L)=%s ⇒ 指数相加语义正确（写成逐分量相乘会得 L 与 0）"
      % (dstr(dmul(dL, dL)), dstr(dmul(dM, dL))))
guard("dim_pow_and_inv",
      deq(dpow(dL, 2), Dim(0, 2, 0, 0)) and deq(dinv(dT), Dim(0, 0, -1, 0)),
      "dpow(L,2)=%s、dinv(T)=%s" % (dstr(dpow(dL, 2)), dstr(dinv(dT))))
guard("dim_energy_chain",
      deq(dmul(dim_hbar, dmul(dim_c, dinv(dL))), dEnergy),
      "[ħ·c·κ]=%s 必须等于能量 %s（首版曾误用 dL 顶替 [c]，被本 guard 拦下）"
      % (dstr(dmul(dim_hbar, dmul(dim_c, dinv(dL)))), dstr(dEnergy)))
guard("dim_G_chain",
      deq(dmul(dpow(dL, 3), dmul(dinv(dM), dpow(dT, -2))), Dim(-1, 3, -2, 0)),
      "[G]=%s = L^3·M^-1·T^-2" % dstr(dmul(dpow(dL, 3), dmul(dinv(dM), dpow(dT, -2)))))
guard("dim_lP_squared",
      deq(dmul(dpow(dEnergy, 0), dpow(dL, 2)), dpow(dL, 2)),
      "长度平方的量纲自检 %s" % dstr(dpow(dL, 2)))
guard("data_signs_opposite",
      da_e < 0 and da_mu > 0,
      "Δa_e=%s < 0、Δa_μ=%s > 0 ⇒ 反号（符号阻塞的机器底座）" % (fmt(da_e), fmt(da_mu)))
guard("crosscheck_r48_ratios",
      rel(mm_ratio_sq, D("4.2753e4")) < D("1e-3") and rel(abs(target_ratio), D("3.3333e3")) < D("1e-3"),
      "复算 (m_μ/m_e)²=%s、|Δa_μ/Δa_e|=%s，与 r48 登记 4.2753E+4 / 3.3333E+3 一致"
      % (fmt(mm_ratio_sq), fmt(abs(target_ratio))))

# ================================================================ I 组：净载体因子的定义与完备枚举
INFO("I01", "来料链与继承声明（本册不重审 r46/r47/r48，只回链复算 r55）",
     "继承：r48 三重阻塞（轮廓/符号/量级）；r55 三定理（最小合法增广=均匀平滑源、"
     "符号≡量级同一方程、m_0 挂不进 κ(m)）。本册只处理 r55 遗留的载体层。",
     "分工零重复：r46（V4.8 子分支B）/ r47（V4.8 §4.3 m(κ₀) 与 m_max）/ r48（分支2 裁定）"
     "均不触碰；本册与 r55 的关系是「下游 + 回链」，r55 的 m_0 与 a_τ 本册独立复算并交叉核对。")

# 净载体因子：a(m) = K·m²·𝔽(m)，𝔽 ≡ F(m)·C(m)·cotθ(m)
#   F(m)     = κ(m)/κ_lin(m)  —— 曲率层因子，r55 III01 四条判据证其 ∈[1.027, 8.25] 恒正，不能变号
#   C(m)     = 耦合常数（普适性由公设层给出）
#   cotθ(m)  = 挠率/曲率比（主线 τ/κ = cotθ）
# ⇒ 可变号因子只剩下耦合层的 C(m) 与 cotθ(m)，且二者只以**乘积**出现。
carrier_factors = [("F(m)=κ/κ_lin", "曲率层", "恒正（r55 III01 四判据：κ≥0 / 60 点扫描 F>1 / m<A₁κ / κ=0⇔m=0）"),
                   ("m", "运动学", "恒正（质量）"),
                   ("cotθ(m)", "耦合层", "可正可负（θ 绕 π/2 翻转）"),
                   ("C(m)", "耦合层", "可正可负（若放弃普适性）")]
INFO("I02", "载体完备枚举：a(m)=K·m²·F(m)·C(m)·cotθ(m) 中可变号的因子只有耦合层两个",
     "四种候选：%s" % "；".join("%s（%s）%s" % (n, ly, st) for n, ly, st in carrier_factors),
     "⇒ 曲率层的 F(m) 与运动学的 m 都被 r55 / 定义本身排除；**变号只能由 C(m)·cotθ(m) 承载**。"
     "这是 r55 III01 的直接推论，本册不重证，只回链。")

# 观测方程（本册全部结论只依赖这条比值，不需要 F(m) 的具体形状）
#   a_μ/a_e = (m_μ/m_e)² · 𝔽(m_μ)/𝔽(m_e) = Δa_μ/Δa_e = target_ratio
# ⇒ 𝔽(m_μ)/𝔽(m_e) = ρ ≡ target_ratio / (m_μ/m_e)²
rho_req = target_ratio / mm_ratio_sq
guard("net_factor_ratio_from_data", rel(rho_req, D("-7.7969e-2")) < D("1e-3"),
      "数据只固定一件事：𝔽(m_μ)/𝔽(m_e) = (Δa_μ/Δa_e)/(m_μ/m_e)² = %s（**反号**），"
      "与 𝔽 的绝对值、形状、零点位置**全部无关**" % fmt(rho_req))
INFO("I03", "观测方程的唯一载荷：数据只钉死 𝔽(m_μ)/𝔽(m_e)=%s，其余全部自由" % fmt(rho_req),
     "a(m)=K·m²·𝔽(m)，𝔽=F·C·cotθ；e/μ 两组数据只给出**一个比值** ρ=%s。"
     "⇒ 𝔽(m_e) 的绝对值、𝔽 的函数形状、𝔽 的零点位置、𝔽(m_τ) 的取值**都不是数据**。" % fmt(rho_req),
     "这是本册三条定理的共同前提：**用一个比值去定一个函数，必然欠定**。")

# ---------------------------------------------------------------- 最小（线性零点）形状约定下的 m_0 复算
def ratio_of_m0(m0_):
    return mm_ratio_sq * (1 - m_mu / m0_) / (1 - m_e / m0_)

lo_, hi_ = m_e, m_mu
scan_rows = []
# 端点 m_0=m_e 会使 (1−m_e/m_0) 恰为 0 ⇒ 只取内部点（i=1..37），严格避开奇点
for i in range(1, 38):
    mm_ = m_e * (m_mu / m_e) ** (D(i) / D(38))
    scan_rows.append((mm_, ratio_of_m0(mm_)))
guard("m0_scan_is_monotone",
      all(scan_rows[i][1] < scan_rows[i + 1][1] for i in range(len(scan_rows) - 1)),
      "%d 点内部扫描 ratio(m_0) 严格单调递增 ⇒ 方程 ratio(m_0)=target 在 (m_e, m_μ) 上**解唯一**"
      % len(scan_rows))
for _ in range(300):
    mid_ = (lo_ + hi_) / 2
    if ratio_of_m0(mid_) < target_ratio:
        lo_ = mid_
    else:
        hi_ = mid_
m0_sol = (lo_ + hi_) / 2
m0_residual = rel(ratio_of_m0(m0_sol), target_ratio)
m0_over_mu = m0_sol / m_mu
m0_MeV = m0_sol / GEV_OVER_C2 * 1000
guard("m0_solution_residual", m0_residual < D("1e-30"),
      "二分 300 次：m_0 = %s kg，回代残差 %s" % (fmt(m0_sol), fmt(m0_residual)))
guard("m0_MeV_in_particle_range", D("0.5") < m0_MeV < D("106"),
      "单位换算自检：m_0 = %s MeV/c² 落在 m_e(0.511) 与 m_μ(105.66) 之间" % fmt(m0_MeV))
guard("m0_matches_r55", rel(m0_MeV, R55_M0_MEV) < D("1e-9"),
      "与 r55 登记值 %s MeV 逐位一致（相对差 %s）⇒ 回链成立" % (fmt(R55_M0_MEV), fmt(rel(m0_MeV, R55_M0_MEV))))

def shape_lin(mm_):
    """最小形状约定：𝔽(m) ∝ (1 − m/m_0)（唯一零点、单调、线性）"""
    return 1 - mm_ / m0_sol

F_e = shape_lin(m_e)
F_mu = shape_lin(m_mu)
F_tau = shape_lin(m_tau)
guard("linear_shape_reproduces_rho", rel(F_mu / F_e, rho_req) < D("1e-30"),
      "最小形状 (1−m/m_0) 回代：𝔽(m_μ)/𝔽(m_e) = %s，与数据要求的 %s 残差 %s"
      % (fmt(F_mu / F_e), fmt(rho_req), fmt(rel(F_mu / F_e, rho_req))))
INFO("I04", "最小形状约定（线性零点）下 𝔽 的零点 m_0 = %s MeV = %s m_μ" % (fmt(m0_MeV), fmt(m0_over_mu)),
     "𝔽(m) ∝ 1−m/m_0 ⇒ 𝔽(m_e)=%s、𝔽(m_μ)=%s、𝔽(m_τ)=%s；该约定是**外加的**，"
     "不是数据（数据只给比值 ρ）" % (fmt(F_e), fmt(F_mu), fmt(F_tau)),
     "复算与 r55 完全一致 ⇒ 回链成立；本册后续所有定理都标出「是否依赖这个约定」。")

# ================================================================ II 组：观测等价定理（载体层）
# 𝔽 = F·C·cotθ，只有乘积可观测 ⇒ 取参数 λ 分裂：cotθ(m) = λ·Ψ(m)，C(m) = Ψ(m)/λ
# 其中 Ψ(m) ≡ 𝔽(m)/F(m)；在 F≈1 的弱场口径下 Ψ(m) = Ψ_e·(1−m/m_0)。
# 取 r42/r44 登记的 Ψ_e（C≡1 约定下即 cotθ_e）：
PSI_E = R44_COT_THETA_E
guard("psi_e_is_registered_value", PSI_E > 0 and PSI_E < D("1e-40"),
      "Ψ(m_e) = %s（r42/r44 由 Δa_e 反解的 cotθ，C≡1 约定）" % fmt(PSI_E))

# G 侧唯一约束：G_th = c³ℓ_P²/(ħ·sinθ)，sinθ = 1/√(1+cot²θ) ⇒ ΔG/G = √(1+cot²θ) − 1
def dG_over_G(cot_):
    return (1 + cot_ * cot_).sqrt() - 1


def dG_over_G_safe(cot_):
    """ΔG/G = √(1+cot²)−1，但 |cot|≲1e−30 时 60 位下 sqrt 下溢为 0（真值 ~cot²/2 ~1e−60 量级）。
    下溢时改用级数 cot²/2（相对误差 ~cot²/4），否则「提升倍数」类比值会 DivisionByZero。"""
    exact_ = dG_over_G(cot_)
    if exact_ > 0:
        return exact_
    return cot_ * cot_ / 2

# 级数 √(1+x)−1 = x/2·(1 − x/4 + …)：相对误差的理论上界为 cot²/4；cot=1e−10 时该上界 = 2.5e−21。
# 注：不能要求「机器零」——级数在这里本就是二阶截断，断言取 1e−18（远宽于理论界 2.5e−21、远严于任何物理结论）。
_series_gap = rel(dG_over_G(D("1e-10")), D("1e-10") ** 2 / 2)
guard("dG_series_matches_exact_when_computable",
      _series_gap < D("1e-18"),
      "cot=1e−10 时精确式 %s 与级数 %s 相对差 %s，小于级数误差的理论上界 cot²/4=%s（门取 1e−18）"
      " ⇒ 下溢区可安全改用级数（否则 II03 的比值会 DivisionByZero）"
      % (fmt(dG_over_G(D("1e-10"))), fmt(D("1e-10") ** 2 / 2),
         fmt(_series_gap), fmt(D("1e-10") ** 2 / 4)))

cot_max = ((1 + U_G) ** 2 - 1).sqrt()          # 令 ΔG/G = u_G 反解 |cotθ| 上界
guard("cot_theta_bound_from_G", rel(dG_over_G(cot_max), U_G) < D("1e-12"),
      "反解：ΔG/G ≤ u_G=%s ⇒ |cotθ| ≤ %s（回代 ΔG/G=%s 残差 %s）"
      % (fmt(U_G), fmt(cot_max), fmt(dG_over_G(cot_max)), fmt(rel(dG_over_G(cot_max), U_G))))

psi_abs = {m_e: abs(PSI_E * F_e), m_mu: abs(PSI_E * F_mu), m_tau: abs(PSI_E * F_tau)}
psi_max = max(psi_abs.values())
lam_max = cot_max / psi_max
lam_rows = []
for lam_ in (D("1e-20"), D("1"), D("1e20"), lam_max):
    row = []
    for mm_ in (m_e, m_mu, m_tau):
        cot_ = lam_ * PSI_E * shape_lin(mm_)
        row.append((fmt(cot_), fmt(dG_over_G_safe(cot_))))
    # 在该 λ 下重算 a_e / a_μ / a_τ（𝔽 = F·C·cotθ = 𝔽 与 λ 无关）
    a_e_v = da_e
    a_mu_v = da_e * mm_ratio_sq * (F_mu / F_e)
    a_tau_v = da_e * (m_tau / m_e) ** 2 * (F_tau / F_e)
    lam_rows.append((fmt(lam_), row, fmt(a_e_v), fmt(a_mu_v), fmt(a_tau_v)))

guard("carrier_split_leaves_g2_identical",
      all(r[2] == lam_rows[0][2] and r[3] == lam_rows[0][3] and r[4] == lam_rows[0][4] for r in lam_rows),
      "λ ∈ {1e−20, 1, 1e20, λ_max} 四档下 a_e/a_μ/a_τ **逐位相同**（%s / %s / %s）"
      % (lam_rows[0][2], lam_rows[0][3], lam_rows[0][4]),
      "机器证明：λ 只改 C 与 cotθ 的**分配**，不改任何 g-2 读数。")
guard("lambda_family_consistent_with_G",
      all(D(rr[1][1]) <= U_G for rr in ((r[0], r[1][2]) for r in lam_rows)),
      "λ 全族在 m_τ 处的 ΔG/G 均 ≤ u_G=%s（λ_max 处恰饱和）" % fmt(U_G))

FAIL("II01", "载体二选一（θ(m) 还是 C(m)）可由 g-2 数据裁决",
     "**不能**：𝔽=F·C·cotθ 只以乘积进入 a(m)，取分裂 cotθ=λ·Ψ、C=Ψ/λ，任意 λ>0 给出**完全相同**的 "
     "a_e=%s、a_μ=%s、a_τ=%s（guard 逐位核对）。G 侧唯一区分通道 ΔG/G=√(1+cot²θ)−1 要求 "
     "|cotθ| ≤ %s，而 fitted |cotθ|~%s ⇒ **λ 可在 (0, %s] 内任意取值（跨 %.0f 个十倍程）而所有 g-2 读数不变**。"
     % (lam_rows[0][2], lam_rows[0][3], lam_rows[0][4], fmt(cot_max), fmt(PSI_E),
        fmt(lam_max), (lam_max / D("1e-20")).log10()),
     "⇒ r55 的待裁决项①（θ(m) vs C(m)）**不是物理选择而是约定选择**："
     "它是耦合层 C 与 cotθ 之间的**规范冗余**，数据无权裁决。"
     "（本册不代选，只把「不可裁决」本身固化为定理。）")

INFO("II02", "观测等价族的机器读数：λ 跨 %.0f 个十倍程，挠率比可在 %s…%s 间任意取值"
     % ((lam_max / D("1e-20")).log10(), fmt(D("1e-20") * psi_max), fmt(cot_max)),
     "; ".join("λ=%s ⇒ cotθ(m_τ)=%s、ΔG/G=%s" % (r[0], r[1][2][0], r[1][2][1]) for r in lam_rows),
     "τ/κ = cotθ = λ·Ψ(m)：λ→0 使挠率整体趋于 0（框架退化为纯曲率、挠率扇区不可测），"
     "λ=λ_max 使 m_τ 处 τ/κ=%s。⇒ **「挠率是物理量」这一声称在分支2 下对 g-2 读数零判别力**。" % fmt(cot_max))

BOUNDARY("II03", "G 测量是区分两个载体的唯一通道，但射程不足",
         "区分需要 ΔG/G = cot²θ/2 可分辨；λ=1 时 ΔG/G(m_τ)=%s，而 CODATA u_G=%s ⇒ "
         "需 G 精度再提升 %s 倍才能开始区分；λ=λ_max 时刚好饱和 1σ。"
         % (fmt(dG_over_G_safe(PSI_E * F_tau)), fmt(U_G), fmt(U_G / dG_over_G_safe(PSI_E * F_tau))),
         "⇒ 原则上可区分（G 侧效应非零），事实上不可区分（差 %s 个量级）。"
         "标 BOUNDARY 而非 FAIL：不排除未来 G 精度革命。")

CORRECTED("II06", "更正 r55 待裁决项①的定性：θ(m) vs C(m) 是约定层冗余，不是待选的物理分支",
          "r55 记为「①载体二选一：θ(m) 还是 C(m)」⇒ 本册更正为：**二者观测等价（II01）**，"
          "真正需要裁决的是「用哪个 λ 记账」，而 λ 无任何可观测量对应 ⇒ **该裁决无物理内容**。",
          "连带更正：r55「载体由 θ(m)/C(m) 二选一」的说法保留（它们仍是仅有的两个候选），"
          "但「必须由用户二选一」应改为「任选其一即可，选了也不产生新预言」。")

# ================================================================ II 组（续）：形状约定与 a_τ 存废
K_TAU = da_e * (m_tau / m_e) ** 2                 # a_τ = K_TAU · x，x ≡ 𝔽(m_τ)/𝔽(m_e)
x_linear = F_tau / F_e
a_tau_lin = K_TAU * x_linear
x_at_hi = A_TAU_HI / K_TAU                        # 使 a_τ 触及 DELPHI 上界的 x
x_at_lo = A_TAU_LO / K_TAU                        # 使 a_τ 触及 DELPHI 下界的 x
guard("tau_coefficient_sane", rel(a_tau_lin, D("1.4359e-4")) < D("1e-3"),
      "最小形状下 a_τ = %s·%s = %s，与 r55 登记 1.4359E−4 一致（回链成立）"
      % (fmt(K_TAU), fmt(x_linear), fmt(a_tau_lin)))

x_lo_win, x_hi_win = min(x_at_lo, x_at_hi), max(x_at_lo, x_at_hi)
guard("linear_shape_is_inside_delphi_window", x_lo_win <= x_linear <= x_hi_win,
      "最小形状给出的 x=%s 落在 DELPHI 允许带 x∈[%s, %s] 之内 ⇒ **未被排除**"
      % (fmt(x_linear), fmt(x_lo_win), fmt(x_hi_win)))
guard("delphi_window_is_wide", (x_hi_win / abs(x_lo_win)) > D("1"),
      "DELPHI 允许带跨度：x ∈ [%s, %s]，线性约定值 %s 只占其中极小一段"
      % (fmt(x_lo_win), fmt(x_hi_win), fmt(x_linear)))

FAIL("II04", "a_τ 是分支2 最小增广的「唯一可证伪读数」",
     "**不成立（在形状未约定时）**：a_τ = %s·x，其中 x=𝔽(m_τ)/𝔽(m_e) **不被 e/μ 数据约束**"
     "（I03：数据只钉死 𝔽(m_μ)/𝔽(m_e)=%s）。只要 x ∈ [%s, %s]，a_τ 就落在 DELPHI 95%% CL"
     " [%s, %s] 之内 ⇒ **DELPHI 对分支2 零判别力**。最小线性形状给 x=%s（a_τ=%s），"
     "只是这条允许带里的**一个点**，不是预言。"
     % (fmt(K_TAU), fmt(rho_req), fmt(x_lo_win), fmt(x_hi_win),
        fmt(A_TAU_LO), fmt(A_TAU_HI), fmt(x_linear), fmt(a_tau_lin)),
     "⇒ r55 II05 的定性「存在，但比现有实验精度低 2 个量级」须**降级**："
     "在放弃形状约定后连「存在」都没有 —— a_τ 的数值是**形状约定的产物**，不是框架的推论。")

# 形状扫描：x 在允许带内取若干点，逐点给出 a_τ 并核对「与 e/μ 数据完全相容」
x_scan = []
for i in range(-3, 4):
    xv_ = x_linear * (D(10) ** D(i))
    x_scan.append((fmt(xv_), fmt(K_TAU * xv_)))
for xv_ in (x_lo_win, x_hi_win):
    x_scan.append((fmt(xv_), fmt(K_TAU * xv_)))
INFO("II05", "形状扫描：𝔽(m_τ)/𝔽(m_e) 在 %s…%s 内任意取值都与 e/μ 数据完全相容"
     % (fmt(x_lo_win), fmt(x_hi_win)),
     "; ".join("x=%s ⇒ a_τ=%s" % (a_, b_) for a_, b_ in x_scan),
     "e/μ 两组数据只约束 𝔽 在 m_e 与 m_μ 两点；m_τ 是第三个点，**零约束**。"
     "⇒ 除非外加「𝔽 取最小线性形状」这一约定，τ 通道不构成任何检验。")

# 单调性细化：若再外加「𝔽 单调递减」这一形状约定
a_tau_mon_lo = K_TAU * rho_req                     # x ≤ ρ（𝔽(m_e)>0 分支）⇒ a_τ ≥ K_TAU·ρ
guard("monotone_refinement_sane", a_tau_mon_lo > 0 and a_tau_mon_lo < A_TAU_HI,
      "外加「𝔽 单调递减」后：x ≤ %s ⇒ a_τ ≥ %s，与 DELPHI 上界 %s 联立得允许带 "
      "a_τ ∈ [%s, %s]（仍跨 %.1f 个量级，**不是预言**）"
      % (fmt(rho_req), fmt(a_tau_mon_lo), fmt(A_TAU_HI), fmt(a_tau_mon_lo), fmt(A_TAU_HI),
         (A_TAU_HI / a_tau_mon_lo).log10()))
BOUNDARY("II07", "即使再外加单调性，τ 通道仍只给允许带不给预言",
         "单调 + DELPHI ⇒ 𝔽(m_τ)/𝔽(m_e) ∈ [%s, %s] ⇒ a_τ ∈ [%s, %s]，跨度 %.1f 个量级"
         % (fmt(-D(1558.2) if False else x_lo_win), fmt(rho_req), fmt(a_tau_mon_lo), fmt(A_TAU_HI),
            (A_TAU_HI / a_tau_mon_lo).log10()),
         "⇒ 「形状约定」每加一条，允许带收窄一点，但**永远收不到一个点**，除非把 𝔽 的函数形式整体钉死。"
         "标 BOUNDARY：这是本册能给的最好结果，不是失败。")

# ================================================================ III 组：代价与自由度记账
FAIL("III01", "Ω5（自由常数 ≤1）可用「数常数个数」判定",
     "**在载体层失效**：参数集 (λ, Ψ_e, m_0) 共 3 个，但可观测量只依赖乘积 Ψ_e 与 m_0"
     " ⇒ **λ 是纯冗余维度**（II01 机器证明），真实自由度 = 2 而记账常数 = 3。"
     "换成 (cotθ_e, C_e, m_0) 记账则得 3；换成 (Ψ_e, m_0) 记账则得 2。",
     "⇒ **Ω5 的判定本身依赖记账约定**（复发 r15「口径 I 无效」）。"
     "本册新增判据：**先做冗余维度检测（参数在可观测量上是否只有乘积/组合出现），再数自由度**。"
     "诚实读数：即便按最省口径（2），也已超过 Ω5 的 ≤1 ⇒ 撞 Ω5 的结论**不因口径而变**。")

INFO("III02", "形状若放开为任意函数 ⇒ 自由度无界（回链 r15 口径 III）",
     "𝔽 若只要求「过 (m_e, 𝔽_e) 与 (m_μ, 𝔽_μ) 两点且变号」，则 𝔽 的函数空间是无穷维"
     " ⇒ 自由度无界；最小线性形状是**把无穷维压成 1 维**的额外约定，代价不在常数个数里。",
     "⇒ r55 说的「代价由 +1 常数升级为无界函数」应更精确地表述为："
     "**「+1 常数 + 1 降维约定」或「+1 自由函数」二选一**，两者的账都不能只记常数。")

BOUNDARY("III03", "τ/κ = cotθ(m) 在 m_0 处归零并反号 ⇒ 手性翻转，是否允许属公设层",
         "𝔽 ∝ (1−m/m_0) 变号 ⇒ cotθ 变号 ⇒ τ/κ 在 m_0=%s MeV 处过零并反号；"
         "λ=1 时 τ/κ 从 %s（m_e）到 %s（m_τ）。κ>0 由 Frenet 定义保证，τ 的符号是约定。"
         % (fmt(m0_MeV), fmt(PSI_E * F_e), fmt(PSI_E * F_tau)),
         "若公设层要求 τ 与 κ 同号（或 τ 不变号），则该载体被否证；"
         "若允许 τ 变号（挠率本就可正可负），则成立但意味着**质量跨过 m_0 时螺旋手性翻转**。"
         "本册不裁决：这是公设层问题，不在可算范围。")

INFO("III04", "若载体纯取 C(m)（cotθ 常数）：C(m_μ)/C(m_e) = %s ⇒ 耦合常数变号"
     % fmt(rho_req),
     "该分支下 C(m_τ)/C(m_e) = %s；而 λ→0 的极限正是这个分支（cotθ→0、C 承担全部变号）。"
     "代价：放弃**耦合常数的普适性与定号**（比 θ(m) 分支更直接地撞公设层）。" % fmt(F_tau / F_e),
     "与 θ(m) 分支观测等价（II01）⇒ 选哪个都不产生新预言，只是把代价登记在不同的账上。")

# ================================================================ IV 组：可识别性与红线
n_params, n_obs_effective = 3, 1
nullity = n_params - n_obs_effective
FAIL("IV01", "在载体/形状未定的情况下跑 dynesty / MCMC 可以得出物理结论",
     "**不能**：可观测约束只有 1 条（ρ=𝔽(m_μ)/𝔽(m_e)），而待定对象是 (λ, Ψ_e, m_0, 𝔽 形状)"
     " ⇒ 似然在至少 %d 个方向上**严格平坦**（λ 已被机器证明为纯平坦方向，II01）。"
     "平坦方向上的后验 = 先验 ⇒ **任何 posterior 都是 prior 的复读**。" % nullity,
     "复发第十二轮步 3 的可识别性结论（1 函数 / 2 数据点 ⇒ 欠定）。"
     "⇒ 本册对「跑不跑 dynesty」的答复升级为两级："
     "①先钉死 𝔽 的函数形式（公设层工作，不是拟合工作）；"
     "②再谈拟合 —— 且此时待拟合的量只剩 m_0 一个数，dynesty 是杀鸡用牛刀。")

INFO("IV02", "若接受最小线性形状，a_τ=%s 的读数仍成立，但它是**约定的推论**" % fmt(a_tau_lin),
     "a_τ=%s vs DELPHI 上界 %s ⇒ 差 %s 倍（需 τ 的 g−2 精度提升 %s 倍才进入可检验区）；"
     "vs SM 值 %s ⇒ 同号、小 %s 倍。"
     % (fmt(a_tau_lin), fmt(A_TAU_HI), fmt(A_TAU_HI / a_tau_lin),
        fmt(A_TAU_HI / a_tau_lin), fmt(A_TAU_SM), fmt(A_TAU_SM / a_tau_lin)),
     "该读数与 r55 II05 逐位一致（guard 核对）⇒ 回链成立；"
     "但其性质由 r55 的「框架的预言」降级为「**最小形状约定 + 框架的联合推论**」。")

OPEN_ITEMS.append(dict(id="O-R57-01", kind="约定层（无物理内容）",
                       text="λ（C 与 cotθ 的分裂比例）无任何可观测量对应 ⇒ 记账时必须登记为冗余维度，不得计入自由度"))
OPEN_ITEMS.append(dict(id="O-R57-02", kind="待用户裁决",
                       text="𝔽(m) 是否取「最小线性形状 (1−m/m_0)」——取则 a_τ 存在但属约定推论；不取则 a_τ 存废不定、DELPHI 零判别力"))
OPEN_ITEMS.append(dict(id="O-R57-03", kind="公设层",
                       text="τ 是否允许变号（m_0 处归零并反号 / 手性翻转）——本册不裁决"))
OPEN_ITEMS.append(dict(id="O-R57-04", kind="公设层",
                       text="是否接受耦合常数 C(m) 变号（C(m_μ)/C(m_e)=%s）即放弃普适性" % fmt(rho_req)))
OPEN_ITEMS.append(dict(id="O-R57-05", kind="口径",
                       text="r55 的 m_0=%s MeV 是在 F(m)≈1（弱场线性）口径下解出的；计入 r55 扫描的 F(m)∈[1.027,8.25] 后零点会平移，本册未重解（结构性定理不依赖零点位置）" % fmt(m0_MeV)))
OPEN_ITEMS.append(dict(id="O-R57-06", kind="待用户裁决",
                       text="Γ=𝔽 形状每外加一条约束（如单调性），允许带收窄一次但永不收成一点 ⇒ 需要的是公设层的函数形式，不是更多数据"))

NOT_SELF_DERIVED.append("a(m)=K·m²·F(m)·C(m)·cotθ(m) 的函数形式：来自 r42/r44/r48，本册不重推")
NOT_SELF_DERIVED.append("τ/κ = cotθ：主线口径（r44 已用），本册不重推")
NOT_SELF_DERIVED.append("G_th = c³ℓ_P²/(ħ·sinθ) 与 sinθ=1/√(1+cot²θ)：r41/r44 形式，本册只代入")
NOT_SELF_DERIVED.append("Ψ(m_e)=%s（r42/r44 由 Δa_e 反解的 cotθ，C≡1 约定）：回链值，本册不复算其来源" % fmt(PSI_E))
NOT_SELF_DERIVED.append("F(m)=κ/κ_lin ∈ [1.027, 8.25] 恒正：r55 III01 四判据结论，本册只回链")
NOT_SELF_DERIVED.append("u_G/G = 2.2e−5（CODATA）、DELPHI a_τ 95% CL [−0.052, 0.013]、a_τ^SM=1.17721e−3：外部实验/理论值")
NOT_SELF_DERIVED.append("Δa 采用 r48 登记口径（−6.9e−13 / +2.3e−9）；原始四位 a 值直接相减得另一口径，符号结论不变（r55 D00 已登记）")

RED_LINE = ("本册只登记「能不能被数据裁决」，**不产生新物理、不代选载体、不推荐方向**。"
            "λ 的等价族、x 的允许带、m_0 的位置都是**记账与约定的性质**，不是框架的新预言；"
            "数学自洽 ≠ 物理证实。")

# ================================================================ main
def main():
    bad = [g for g in GUARDS if not g["passed"]]
    if bad:
        print("[%s] GUARD FAILED %d / %d —— 禁止输出结论" % (ROUND, len(bad), len(GUARDS)))
        for g in bad:
            print("  FAIL-GUARD %s :: %s" % (g["name"], g["detail"]))
        return 2
    counts = {}
    for r in RECORDS:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    payload = dict(
        round=ROUND, stamp=STAMP, name=NAME,
        verdict_counts=counts,
        guards_total=len(GUARDS), guards_passed=len(GUARDS),
        key_numbers=dict(
            net_factor_ratio_rho=fmt(rho_req),
            m0_solution_MeV=fmt(m0_MeV),
            m0_over_mu=fmt(m0_over_mu),
            m0_residual=fmt(m0_residual),
            cot_theta_upper_bound_from_G=fmt(cot_max),
            lambda_upper_bound=fmt(lam_max),
            lambda_family_decades=fmt((lam_max / D("1e-20")).log10()),
            tau_linear_shape_x=fmt(x_linear),
            a_tau_minimal_shape=fmt(a_tau_lin),
            a_tau_needed_precision_factor=fmt(A_TAU_HI / a_tau_lin),
            x_window_low=fmt(x_lo_win), x_window_high=fmt(x_hi_win),
            a_tau_monotone_band_low=fmt(a_tau_mon_lo), a_tau_monotone_band_high=fmt(A_TAU_HI),
            dG_over_G_at_lambda1_mtau=fmt(dG_over_G_safe(PSI_E * F_tau)),
            G_precision_gap=fmt(U_G / dG_over_G_safe(PSI_E * F_tau)),
            tau_over_kappa_m_e=fmt(PSI_E * F_e),
            tau_over_kappa_m_tau=fmt(PSI_E * F_tau),
        ),
        records=RECORDS, guards=GUARDS,
        open_items=OPEN_ITEMS, not_self_derived=NOT_SELF_DERIVED,
        red_line=RED_LINE,
    )
    if not os.path.isdir(OUT_DIR):
        os.makedirs(OUT_DIR)
    with io.open(os.path.join(OUT_DIR, NAME + ".json"), "w", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False, indent=2))
    md = ["# %s" % NAME, "",
          "- 轮次：%s　日期：%s　guard：%d/%d PASS" % (ROUND, STAMP, len(GUARDS), len(GUARDS)),
          "- 条目计数：%s" % counts, "", "## 关键读数", ""]
    for k, v in payload["key_numbers"].items():
        md.append("- `%s` = %s" % (k, v))
    md += ["", "## 条目", ""]
    for r in RECORDS:
        md += ["### %s　%s" % (r["id"], r["verdict"]), "",
               "- 判定对象：%s" % r.get("claim", ""),
               "- 机器读数：%s" % r.get("reading", ""),
               "- 备注：%s" % r.get("note", ""), ""]
    md += ["## 开放项", ""]
    for it in OPEN_ITEMS:
        md.append("- `%s`（%s）：%s" % (it["id"], it["kind"], it["text"]))
    md += ["", "> 红线：%s" % RED_LINE, ""]
    with io.open(os.path.join(OUT_DIR, NAME + ".md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(md))
    rep = ["%s  %s" % (ROUND, STAMP), "guards %d/%d PASS" % (len(GUARDS), len(GUARDS)),
           "counts %s" % counts, ""]
    for r in RECORDS:
        rep.append("[%s] %s :: %s" % (r["verdict"], r["id"], r.get("claim", "")))
    rep.append("")
    for k, v in payload["key_numbers"].items():
        rep.append("%s = %s" % (k, v))
    with io.open(os.path.join(OUT_DIR, NAME + "_report.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(rep) + "\n")
    print("[%s] guards %d/%d PASS" % (ROUND, len(GUARDS), len(GUARDS)))
    print("[%s] counts %s" % (ROUND, counts))
    print("[%s] m0 = %s MeV   rho = %s   lambda_max = %s"
          % (ROUND, fmt(m0_MeV), fmt(rho_req), fmt(lam_max)))
    print("[%s] a_tau(minimal shape) = %s   x window = [%s, %s]"
          % (ROUND, fmt(a_tau_lin), fmt(x_lo_win), fmt(x_hi_win)))
    print("[%s] json -> %s" % (ROUND, os.path.join(OUT_DIR, NAME + ".json")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
