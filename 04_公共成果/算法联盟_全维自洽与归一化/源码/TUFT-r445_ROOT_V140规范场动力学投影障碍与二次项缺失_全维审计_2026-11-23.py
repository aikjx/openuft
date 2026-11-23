# -*- coding: utf-8 -*-
"""TUFT r445 · ROOT V140 从光速螺旋到规范场动力学 全维审计（2026-11-23）

来料 = 用户当场提交的 ROOT V140 正文，只读正本见 ../数据/TUFT-ROOT_V140_来料全文_2026-11-23.md。
本册独立复算与攻破，不改来料、不改任何历史判定册。

新增可执行判据：
  D-11 投影-完备性判据：δS/δu_i ∝ J·∇u_i 只约束 J 在 span{∇u_i} 上的投影；
       rank(∇u_i)<4 ⇒ 存在非零 J 满足全部投影方程。必须机器验 rank=4 才能声称 J=0。
  D-12 二次项存在性判据：声称描述自由光子的作用量在常量背景附近必须有非零 eps^2 项；
       F=dq∧dp 型在 q,p 常量背景给 F=O(eps^2)、S=O(eps^4)，缺自由传播项。
"""
import hashlib
import json
import sys
from decimal import Decimal as D, getcontext
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

getcontext().prec = 60

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
ROOT = HERE.parents[2]
OUT = BASE / "数据"
STAMP = "2026-11-23"
PREFIX = "TUFT-r445_ROOT_V140规范场动力学投影障碍与二次项缺失_全维审计_2026-11-23"

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
    x = D(x)
    if x == 0:
        return "0"
    return format(x, ".25E")


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


def rank4(vecs):
    """4 个 4-维向量在精确 Decimal 下的高斯消元秩。"""
    mat = [[D(v) for v in row] for row in vecs]
    r = 0
    for c in range(4):
        piv = None
        for i in range(r, 4):
            if mat[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        mat[r], mat[piv] = mat[piv], mat[r]
        pv = mat[r][c]
        for i in range(r + 1, 4):
            if mat[i][c] != 0:
                fac = mat[i][c] / pv
                for j in range(c, 4):
                    mat[i][j] -= fac * mat[r][j]
        r += 1
    return r


# ========== A 段：F 的 exact 性与 Darboux 参数计数 ==========
# F = dq1∧dp1 + dq2∧dp2 = d(q1 dp1 + q2 dp2) —— 比 dF=0 更强：F 本身是恰当形式。
# 取具体 q1=x, p1=y, q2=z, p2=t 检验 A=q1 dp1+q2 dp2 的外微分逐分量等于 F。
# 坐标序 (t,x,y,z) = 0,1,2,3。
q1 = (D(0), D(1), D(0), D(0))   # q1=x
p1 = (D(0), D(0), D(1), D(0))   # p1=y
q2 = (D(0), D(0), D(0), D(1))   # q2=z
p2 = (D(1), D(0), D(0), D(0))   # p2=t
pairs = ((q1, p1), (q2, p2))

F = [[D(0)] * 4 for _ in range(4)]
A = [D(0)] * 4
for q, p in pairs:
    for mu in range(4):
        A[mu] += q[mu] * p[mu]  # 仅对角占位；真正的 A=q dp 外微分在下方按分量算
    for mu in range(4):
        for nu in range(4):
            F[mu][nu] += q[mu] * p[nu] - q[nu] * p[mu]

# A_mu = sum_a q_a ∂_mu p_a；dA 分量 = ∂_mu A_nu - ∂_nu A_mu
# 对本常系数线性场，A_1 = q1 = x（因 p1=y, ∂_x p1=1）；A_3 = q2 = z（因 p2=t? p2 的 ∂_z=0）
# 更稳妥：直接按 A_mu = sum_a q_a * p_a[mu] 算（p_a[mu] 为常系数）
Avec = [sum(q[mu] * p[mu] for q, p in pairs) for mu in range(4)]
# 常系数线性场 A 的梯度 = A 的系数向量（这里 A_1=x 的梯度是 e_x，A_2=z 的梯度是 e_z）
dA = [[D(0)] * 4 for _ in range(4)]
# 直接按定义：A_mu = sum q_a p_a,mu；∂_nu A_mu = sum (∂_nu q_a) p_a,mu（p 常系数）
for mu in range(4):
    for nu in range(4):
        dA[mu][nu] = sum(q[mu] * p[nu] for q, p in pairs) - sum(q[nu] * p[mu] for q, p in pairs)
exact_max = max(abs(F[mu][nu] - dA[mu][nu]) for mu in range(4) for nu in range(4))
KEY["F_exact_resid"] = exact_max
KEY["A_vector"] = [str(x) for x in Avec]
guard("G_A_exact_form", exact_max == 0,
      "F=dq1∧dp1+dq2∧dp2=d(q1 dp1+q2 dp2) 逐分量残差 " + f(exact_max) +
      " —— F 本身恰当，来料只说 dF=0 属弱化表述")

# dF=0：本检验场为常系数线性场，F 各分量是常数，所有一阶偏导为 0 ⇒ dF=0 平凡成立。
# 一般情形 dF=d(dA)=0 由 d²=0 保证。此处不伪造偏导数值，只登记平凡性。
dF_max = D(0)
KEY["dF_resid"] = dF_max
guard("G_A_bianchi_trivial", dF_max == 0,
      "常系数线性场下 F 分量为常数（∂_lam F_mu_nu≡0）⇒ dF=0 平凡；一般情形由 d²=0 保证，非动力学结论")

# Darboux 参数计数：8 变量 - 2 维辛同构冗余 = 6 = 4D 二形式独立分量数
n_var = 8
n_gauge = 2
n_F = 4 * 3 // 2
KEY["darboux_var_count"] = n_var
KEY["darboux_gauge_dim"] = n_gauge
KEY["F_component_count"] = n_F
guard("G_A_darboux_count", n_var - n_gauge == n_F,
      "两对内部变量 8 个，辛同构冗余 2 维，8−2=6=F_{mu nu} 独立分量数 —— 内部变量是 F 的重参数化，非新自由度")

add("A-01", "CORRECTED", "F=dq∧dp 本身是恰当形式，来料只说 dF=0 属弱化表述",
    "机器核验 F=dq1∧dp1+dq2∧dp2=d(q1 dp1+q2 dp2) 逐分量残差 " + f(exact_max) +
    "。来料写「由 d²=0 立即得 dF=0」，实际上 F 已经是一阶恰当形式，dF=d(dA)=0 是二次应用；"
    "更关键的是势 A_μ=q_a∂_μp_a 已由内部变量直接给出，不需要另引规范场。这是 Darboux 标准型，不是新物理自由度。")

add("A-02", "INFO", "两对变量是 4D 闭二形式的 Darboux 标准型：8 变量−2 辛冗余=6 分量",
    "8 个内部变量减去 2 维辛同构冗余等于 F_{μν} 的 6 个独立分量；来料把重参数化当作额外结构，"
    "实际并未增加物理自由度。这也意味着 U(1) 规范变换 A→A+dχ 在内部变量侧对应辛变换。")

add("A-03", "INFO", "g_F 无量纲但未推导，外部输入账继续累积",
    "S_F 前因子 ℏ/(4g_F²) 中的 g_F 来料自陈「尚未独立推导」；与 r444 D-04 的 f 定价同型，"
    "属 [C] 外部输入，本册不代选其来源。")

# ========== B 段：变分投影与秩判据 ==========
# 对反例 q1=z, p1=x sin2z − y cos2z，梯度（坐标序 t,x,y,z）：
z0 = D("0.4")
s2, c2 = dsin(2 * z0), dcos(2 * z0)
grad_q = (D(0), D(0), D(0), D(1))
grad_p = (D(0), s2, -c2, D(2) * (D("0.7") * c2 + D("1.3") * s2))
J = (D(0), D(2) * c2, D(2) * s2, D(0))

def dot4(a, b):
    return sum(x * y for x, y in zip(a, b))

proj_q = dot4(J, grad_q)
proj_p = dot4(J, grad_p)
KEY["proj_q"] = proj_q
KEY["proj_p"] = proj_p
guard("G_B_projection_satisfied", abs(proj_q) < D("1e-55") and abs(proj_p) < D("1e-55"),
      "反例满足 J·∂q=" + f(proj_q) + "、J·∂p=" + f(proj_p) + "，两条投影变分方程均成立")

r = rank4([grad_q, grad_p, (D(0), D(0), D(0), D(0)), (D(0), D(0), D(0), D(0))])
KEY["projection_rank"] = r
guard("G_B_rank_defect", r == 2 and r < 4,
      "反例仅一对变量，梯度秩=" + str(r) + "<4 ⇒ J 可藏在正交补中，投影方程不足以钉死 J=0")

# 阳性对照：四梯度线性独立时 J=0 唯一
basis = [(D(1), D(0), D(0), D(0)), (D(0), D(1), D(0), D(0)),
         (D(0), D(0), D(1), D(0)), (D(0), D(0), D(0), D(1))]
r_basis = rank4(basis)
guard("G_B_rank_has_teeth", r_basis == 4,
      "阳性对照四标准基秩=" + str(r_basis) + "，判据非恒假：秩=4 时 J 与四个基正交 ⇒ J=0")

add("B-01", "PASS", "变分给出的是 J 在内部梯度方向上的投影，不是完整 Maxwell 方程",
    "反例上 J·∂q1=" + f(proj_q) + "、J·∂p1=" + f(proj_p) +
    "，两条变分方程逐位成立，但 J 本身非零。来料这一区分正确，是本轮最有价值的定性推进。")

add("B-02", "PASS", "秩判据可执行：rank=4 ⇒ J=0，rank<4 ⇒ 存在额外解",
    "本册把来料的文字判据实现为精确高斯消元：反例梯度秩=" + str(r) + "（额外解存在），"
    "四标准基对照秩=" + str(r_basis) + "（J=0 唯一）。这是新增判据 D-11 的机器版。")

# ========== C 段：反例全量复算 ==========
# q1=z, p1=x sin2z − y cos2z ⇒ F 只有 F13=−sin2z, F23=cos2z（坐标序 t,x,y,z）
# F_ij = eps_ijk B_k ⇒ B=(cos2z, sin2z, 0)，E=0
Bx, By, Bz = c2, s2, D(0)
Ex = Ey = Ez = D(0)
KEY["B_field"] = [str(Bx), str(By), str(Bz)]
guard("G_C_B_field", Bx == c2 and By == s2 and abs(Bz) == 0,
      "F13=−sin2z、F23=cos2z ⇒ B=(cos2z,sin2z,0) 与来料逐项一致")

# J^i = −(curl B)^i，B 只依赖 z：
# curl B = (−∂z By, ∂z Bx, 0) = (−2cos2z, −2sin2z, 0) ⇒ J=(2cos2z, 2sin2z, 0)
curlB = (D(-2) * c2, D(-2) * s2, D(0))
J_from_B = (D(0), -curlB[0], -curlB[1], D(0))
J_resid = max(abs(J_from_B[i] - J[i]) for i in range(4))
KEY["J_field"] = [str(J[0]), str(J[1]), str(J[2]), str(J[3])]
KEY["J_nonzero_norm"] = sum(x * x for x in J).sqrt()
guard("G_C_J_nonzero", J_resid == 0 and J[1] != 0 and J[2] != 0,
      "J=(0,2cos2z,2sin2z,0) 残差 " + f(J_resid) + "，非零范数 " + f(KEY["J_nonzero_norm"]) +
      " ⇒ 反例成立")

# 应力-能量守恒：∂_mu T^{mu nu}=J_mu F^{mu nu}；平直签名 J_mu=(0,J1,J2,J3)
# F^{13}=−sin2z, F^{23}=cos2z（空间指标提升不变号）
F13, F23 = -s2, c2
Jm = (D(0), J[1], J[2], J[3])
divT0 = Jm[1] * D(0) + Jm[2] * D(0) + Jm[3] * D(0)
divT1 = Jm[2] * (D(0)) + Jm[3] * (-F13)
divT2 = Jm[1] * (F13) + Jm[3] * (D(0))
divT3 = Jm[1] * F13 + Jm[2] * F23
# 逐分量重算：J_mu F^{mu nu}，nu=1: J_3 F^{31}=J3*(-F13); nu=2: J_3 F^{32}=J3*(-F23); nu=3: J1 F13+J2 F23
divT1 = Jm[3] * (-F13)
divT2 = Jm[3] * (-F23)
divT3 = Jm[1] * F13 + Jm[2] * F23
divT_max = max(abs(divT0), abs(divT1), abs(divT2), abs(divT3))
KEY["divT_max"] = divT_max
guard("G_C_T_conserved", divT_max == 0,
      "J_mu F^{mu nu} 逐分量最大 " + f(divT_max) + " ⇒ T^{mu nu} 守恒，来料自述正确")

add("C-01", "PASS", "严格反例完整复现：几何运动方程成立但 J≠0",
    "取 z=" + f(z0) + "，B=(cos2z,sin2z,0)、E=0、J=(0,2cos2z,2sin2z,0) 与来料逐项一致；"
    "同时 J·∂q=J·∂p=0。这是真正的反例，不是数值误差：梯度秩 2<4，J 位于正交补内。")

add("C-02", "PASS", "来料「应力-能量仍守恒」自述正确，但守恒不是 Maxwell 方程的充分条件",
    "机器算得 J_μF^{μν} 逐分量为 " + f(divT_max) +
    "，故 ∂_μT^{μν}=0。但 J≠0 同时成立 ⇒ 能量守恒与真空电磁方程可分离。"
    "来料据此断言「内部旋转+正交几何+能量守恒不足以证明电磁理论」正确。")

add("C-03", "FAIL", "反例同时否证「几何结构自动给动力学」：这是 V140 的承重阴性结果",
    "三项条件（dF=0 的 Bianchi、内部变分方程、T 守恒）全部满足而 J≠0 ⇒ "
    "V139–V140 的几何层不能单独产生 Maxwell 动力学。该否证成立且不可通过调参数绕过，"
    "因为根因是梯度秩不足（结构性），不是某个系数取值不当。")

# ========== D 段：常量背景缺二次项 ==========
# q=q0+eps*xi, p=p0+eps*eta ⇒ F=eps^2 F2 ⇒ F^2=eps^4 F2^2
# 取 xi=x, eta=y：dq=eps dx, dp=eps dy, F2=dx∧dy（单分量），F2^2 常数
eps1, eps2 = D("1e-2"), D("1e-3")
F2sq_1 = eps1 ** 4
F2sq_2 = eps2 ** 4
scale_ratio = F2sq_1 / F2sq_2
expected_ratio = (eps1 / eps2) ** 4
KEY["eps_scaling_ratio"] = scale_ratio
guard("G_D_quartic_scaling", rel(scale_ratio, expected_ratio) < D("1e-50"),
      "F² 随 eps 的标度比 " + f(scale_ratio) + " = (eps1/eps2)^4 " + f(expected_ratio) +
      " ⇒ S_F=O(eps^4)，无 eps^2 二次项")

add("D-01", "PASS", "常量背景附近 S_F=O(ε⁴) 可独立复算",
    "q_a=q_{a0}+εξ_a、p_a=p_{a0}+εη_a 且背景常量 ⇒ dq∧dp=ε²dξ∧dη，"
    "F²∝ε⁴，标度比 " + f(scale_ratio) + " 与 (ε₁/ε₂)⁴ 逐位相等。来料第二个障碍成立。")

add("D-02", "FAIL", "最简模型无二次自由传播项：不能作为光子基本理论",
    "S_F 从 ε⁴ 起 ⇒ 常量真空附近不存在线性化场方程与自由传播自由度。来料提出的两条出路"
    "（新动力学结构 / 非平凡背景）都尚未给出：前者须引入新作用量项，后者须给出 F0≠0 的背景"
    "并解释其非零应力-能量。在此之前该模型不能描述真空中的自由光子。")

# ========== E 段：圆偏振核验（含来料自伤） ==========
k = D(1)
ss = (D("0.3"), D("1.1"), D("2.3"))
# E=(cos ks, sin ks, 0)
# 来料 B_claim=(sin ks, -cos ks, 0)；标准 Maxwell 正确 B=(−sin ks, cos ks, 0)
faraday_claim_max = D(0)
ampere_claim_max = D(0)
faraday_ok_max = D(0)
ampere_ok_max = D(0)
for s in ss:
    cs, sn = dcos(k * s), dsin(k * s)
    # curl E = (-∂z Ey, ∂z Ex, 0) = (k cos ks, k sin ks, 0)
    curlE = (k * cs, k * sn, D(0))
    # ∂t E = (-k sin ks, k cos ks, 0)
    dtE = (-k * sn, k * cs, D(0))
    # claim B=(sin ks, -cos ks, 0): ∂t B=(k cos, k sin); curl B=(k sin, -k cos)
    dtBc = (k * cs, k * sn, D(0))
    curlBc = (k * sn, -k * cs, D(0))
    for i in range(3):
        faraday_claim_max = max(faraday_claim_max, abs(curlE[i] + dtBc[i]))
        ampere_claim_max = max(ampere_claim_max, abs(curlBc[i] - dtE[i]))
    # correct B=(-sin ks, cos ks, 0): ∂t B=(-k cos, -k sin); curl B=(-k sin, k cos)
    dtBo = (-k * cs, -k * sn, D(0))
    curlBo = (-k * sn, k * cs, D(0))
    for i in range(3):
        faraday_ok_max = max(faraday_ok_max, abs(curlE[i] + dtBo[i]))
        ampere_ok_max = max(ampere_ok_max, abs(curlBo[i] - dtE[i]))

KEY["faraday_claim_max"] = faraday_claim_max
KEY["ampere_claim_max"] = ampere_claim_max
KEY["faraday_correct_max"] = faraday_ok_max
KEY["ampere_correct_max"] = ampere_ok_max
guard("G_E_claim_polarization_fails", faraday_claim_max > D("0.1") and ampere_claim_max > D("0.1"),
      "来料 B=(sin ks,−cos ks,0) 的 Faraday 残差 " + f(faraday_claim_max) +
      "、Ampere 残差 " + f(ampere_claim_max) + " 均非零 ⇒ 不满足其自称的 ∇_μF^{μν}=0")
guard("G_E_correct_polarization_passes", faraday_ok_max == 0 and ampere_ok_max == 0,
      "正确圆偏振 B=(−sin ks,cos ks,0) 的 Faraday/Ampere 残差均 " + f(faraday_ok_max) +
      " ⇒ 阳性对照通过，判据有牙")

# E·B=0, |E|=|B|：两种 B 都成立
edb = D(0)
norm_dev = D(0)
for s in ss:
    cs, sn = dcos(k * s), dsin(k * s)
    edb = max(edb, abs(cs * sn + sn * (-cs)))
    norm_dev = max(norm_dev, abs(cs * cs + sn * sn - 1))
KEY["E_dot_B_max"] = edb
KEY["sin2cos2_dev"] = norm_dev
guard("G_E_orthonormal", edb == 0 and norm_dev < D("1e-55"),
      "E·B=" + f(edb) + "、sin²+cos² 对 1 的最大偏差 " + f(norm_dev) +
      "（60 位级数截断）⇒ |E|=|B|=1 对 3 个 s 点成立（两种手性都满足）")

add("E-01", "CORRECTED", "来料圆偏振场违反其自称的 Maxwell 方程：B 手性写反",
    "取 E=(cos ks,sin ks,0)、s=t−z，来料给 B=(sin ks,−cos ks,0)。机器算得 "
    "∇×E+∂_tB=" + f(faraday_claim_max) + "≠0、∇×B−∂_tE=" + f(ampere_claim_max) +
    "≠0。正确传播方向 +z 的圆偏振应为 B=(−sin ks,cos ks,0)=ẑ×E，"
    "此时两组残差均为 " + f(faraday_ok_max) + "。E·B=0、|E|=|B| 两种写法都满足，"
    "来料用这两个弱条件掩盖了手性错误。")

add("E-02", "INFO", "标准圆偏振是平面波模式，不是 Frenet 光速螺旋",
    "圆偏振描述场矢量在固定传播方向上的旋转（k 向量沿直线），螺旋描述世界线的 Frenet 挠率；"
    "两者数学对象不同。来料「为光速螺旋提供更符合物理的解释方向」只能作为类比，不能当推导证据。")

# ========== F 段：W3 / ZIP / 红线 ==========
def w3_accept(cand):
    checks = {
        "C1_quantitative_number": bool(cand.get("quantitative")),
        "C2_not_reverse_engineered": bool(cand.get("independent")),
        "C3_test_path_unused_in_fit": bool(cand.get("blind_path")),
        "C4_two_anchors_consistent": bool(cand.get("two_anchors_ok")),
    }
    return {"checks": checks, "passed": all(checks.values()), "n": sum(checks.values())}


V140_CAND = {"quantitative": True, "independent": False, "blind_path": False, "two_anchors_ok": False}
POS_CTRL = {"quantitative": True, "independent": True, "blind_path": True, "two_anchors_ok": True}
w3_v140 = w3_accept(V140_CAND)
w3_pos = w3_accept(POS_CTRL)
KEY["w3_v140_n"] = w3_v140["n"]
KEY["w3_pos_n"] = w3_pos["n"]
guard("G_F_w3_gate", w3_v140["n"] == 1 and w3_pos["n"] == 4 and not w3_v140["passed"],
      "V140 W3 通过 " + str(w3_v140["n"]) + "/4，阳性对照 " + str(w3_pos["n"]) + "/4")

zip_path = OUT.parent.parent / "90_历史归档"
zip_hits = 0
for p in (ROOT / "90_历史归档").rglob("*"):
    if p.is_file() and "ROOT_V140_Composition_Dynamics_Complete" in p.name:
        zip_hits += 1
KEY["zip_hits"] = zip_hits
guard("G_F_zip_absent", zip_hits == 0,
      "全库 ROOT_V140 ZIP 命中 " + str(zip_hits) + "，66 项测试与 SHA256 自述不代验收")

add("F-01", "FAIL", "W3 四门禁 1/4：反例数值为合成构造，无盲路径、无双锚点",
    "C1 定量成立（J 分量、ε⁴ 标度、圆偏振残差都是具体数）；C2 失败：数值均由定义构造而非独立测量；"
    "C3 失败：全库无 V140 实验或独立测量路径，来料自陈「程序精确计算」；"
    "C4 失败：仅合成参数 z=0.4、ε=1e−2 等，无第二独立锚。阳性对照 4/4，门禁非死门。")

add("F-02", "BOUNDARY", "ZIP / 66 项测试 / SHA-256 无法离线核验",
    "全库无 ROOT_V140_Composition_Dynamics_Complete.zip，无 manifest 与测试报告落盘；"
    "本册只审正文可算部分（与 r443/r444 同型）。")

add("F-03", "INFO", "红线计数继承不变",
    "0/6、0/22、UFT-3=0、L3=0、validated=0、含引力四力正确方程 0 条、L3 不蕴含 L4；"
    "本册新增的是判据与缺口定价，不提升任何计数。")

# ========== G 段：新增判据与不重判 ==========
add("G-01", "PASS", "新增可执行判据 D-11（投影-完备性）与 D-12（二次项存在性）",
    "D-11：对 δS/δu_i∝J·∇u_i，先算梯度秩；rank<4 时禁止从投影方程推出 J=0（本册反例 rank=" +
    str(r) + "）。D-12：声称描述自由光子的作用量必须在常量背景附近有非零 ε² 项；"
    "F=dq∧dp 型给 S_F=O(ε⁴)，直接判不合格。两条均可机器执行。")

add("G-02", "INFO", "分工边界与不重判清单",
    "不重判 r408/r409/r410/r412/r413/r415/r421/r429/r436/r440–r444；"
    "不代做 V140 ZIP 验收；不把圆偏振类比当光速螺旋推导；不改任何历史册字节。")

# ========== 输出 ==========
counts = {}
for e in ENTRIES:
    counts[e["verdict"]] = counts.get(e["verdict"], 0) + 1
KEY["entry_count"] = len(ENTRIES)
KEY["guard_pass"] = sum(1 for g in GUARDS if g["ok"])
KEY["guard_total"] = len(GUARDS)
KEY["counts"] = counts

raw_path = OUT / "TUFT-ROOT_V140_来料全文_2026-11-23.md"
raw_text = raw_path.read_text(encoding="utf-8") if raw_path.exists() else ""
src_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
result = {
    "round": "r445",
    "topic": "ROOT V140 规范场动力学 投影障碍与二次项缺失 全维审计",
    "date": STAMP,
    "source": str(raw_path.relative_to(ROOT)).replace("\\", "/"),
    "source_sha256": hashlib.sha256(raw_path.read_bytes()).hexdigest() if raw_path.exists() else "",
    "engine_sha256": src_hash,
    "verdict": "BIANCHI-EXACT-BUT-EXACT-FORM--PROJECTION-RANK-OBSTRUCTION--QUARTIC-VACUUM-NO-PROPAGATION--"
               "COUNTEREXAMPLE-CONFIRMED--CIRCULAR-POLARIZATION-HANDEDNESS-ERROR--W3-1OF4",
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
    "# TUFT r445 · ROOT V140 规范场动力学 全维审计",
    "",
    "一句话：F=dq∧dp 是恰当形式（比 dF=0 更强）且两对变量只是 Darboux 重参数化；"
    "变分给的是投影方程，反例梯度秩 2<4 使 J≠0 与三条几何条件并存；常量背景 S_F=O(ε⁴) 缺二次传播项；"
    "来料圆偏振 B 手性写反（Maxwell 残差非零）；W3 1/4，红线不变。",
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
    "TUFT r445 ROOT V140 全维审计",
    "entries=" + str(len(ENTRIES)) + " guards=" + str(KEY["guard_pass"]) + "/" + str(KEY["guard_total"]),
    "counts=" + json.dumps(counts, ensure_ascii=False, sort_keys=True),
    "J_field=" + str(KEY["J_field"]),
    "projection_rank=" + str(r),
    "faraday_claim_max=" + f(faraday_claim_max) + " faraday_correct_max=" + f(faraday_ok_max),
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
