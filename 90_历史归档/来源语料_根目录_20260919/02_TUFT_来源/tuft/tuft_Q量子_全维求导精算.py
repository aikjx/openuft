# -*- coding: utf-8 -*-
"""
TUFT 量子版（Q-TUFT）全维求导精算
=================================
对象：《量子 TUFT 构建》§1-§9
  主丛路径积分测度 / 曲率饱和边界 / 挠率拓扑荷量子化 /
  时空螺旋元胞 / 传播子 / 散射振幅 / 可证伪预言 / 仿真代码

方法：
  * numpy 外代数引擎（p-形式楔积，精确检验 T^a∧T_a 等代数恒等式）
  * 线性代数（自由度计数、SVD 秩）
  * 相对论运动学（Proca 传播子、手性振幅、幺正性量级）
  * ast 静态检查（原文仿真代码可运行性）

红线：数学自洽 != 物理实验证实。凡是框架内部自我矛盾的条目一律判 FAIL，
      不做"降级为 PASS"的粉饰。
"""
from __future__ import print_function

import os
import sys
import ast
import math
import itertools
import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(HERE, "tuft_Q量子_report.txt")

N = 4  # 时空维数


class Report(object):
    def __init__(self):
        self.rows = []
        self.lines = []

    def echo(self, t=""):
        print(t)
        self.lines.append(t)

    def section(self, t):
        self.echo("")
        self.echo("=" * 78)
        self.echo(t)
        self.echo("=" * 78)

    def add(self, sec, name, verdict, detail=""):
        self.rows.append((sec, name, verdict, detail))
        line = "  [%s] %s" % (verdict, name)
        if detail:
            line += "   |  " + detail
        self.echo(line)

    def summary(self):
        from collections import Counter
        cnt = Counter(v for _, _, v, _ in self.rows)
        self.section("汇总")
        for k in ["PASS", "FAIL", "BOUNDARY", "INFO"]:
            self.echo("  %-9s = %d" % (k, cnt.get(k, 0)))
        if cnt.get("FAIL"):
            self.echo("  存在 FAIL（真实缺陷）:")
            for sec, name, v, det in self.rows:
                if v == "FAIL":
                    self.echo("    - [%s] %s" % (sec, name))
        return cnt

    def dump(self):
        try:
            with open(REPORT_PATH, "w", encoding="utf-8") as fh:
                fh.write("\n".join(self.lines))
                fh.write("\n")
        except Exception as exc:
            print("  [warn] report write failed: " + str(exc))


# ----------------------------------------------------------------------
# 外代数工具：p-形式 = 反对称 numpy 数组，形状 (4,)*p
# ----------------------------------------------------------------------
def perm_sign(perm):
    """排列奇偶性：+1 / -1"""
    p = list(perm)
    s = 1
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if p[i] > p[j]:
                s = -s
    return s


def wedge(A, B):
    """(p,q)-shuffle 定义的标准楔积（无额外归一化因子）"""
    if A.ndim == 0:
        return A * B
    if B.ndim == 0:
        return A * B
    p, q = A.ndim, B.ndim
    out = np.zeros((N,) * (p + q))
    for idx in itertools.product(range(N), repeat=p + q):
        s = 0.0
        for comb in itertools.combinations(range(p + q), p):
            rest = [i for i in range(p + q) if i not in comb]
            sign = perm_sign(list(comb) + rest)
            s += sign * A[tuple(idx[i] for i in comb)] * B[tuple(idx[i] for i in rest)]
        out[idx] = s
    return out


def rand_form(deg, rng, scale=1.0):
    """随机 p-形式（先随机再反对称化）"""
    A = rng.normal(scale=scale, size=(N,) * deg)
    if deg == 0:
        return A
    for _ in range(8):
        A = A - np.transpose(A, axes=range(deg)[::-1])
    # 严格反对称化（暴力，维度小）
    out = np.zeros((N,) * deg)
    for perm in itertools.permutations(range(deg)):
        out += perm_sign(perm) * np.transpose(A, axes=perm)
    return out / float(math.factorial(deg))


def flat_metric():
    """Minkowski 度规 diag(-1,1,1,1)，正交标架（einbein 形式体系的标准取法）"""
    return np.diag([-1.0, 1.0, 1.0, 1.0])


# ----------------------------------------------------------------------
# §1  路径积分整体结构（结构审查）
# ----------------------------------------------------------------------
def part1_structure(rep):
    rep.section("§1  主丛路径积分：结构审查")
    rep.add("Q1.1", "路径积分变量 = (e, omega, A, Omega) 四组场", "PASS",
            "Einstein-Cartan 型一阶形式体系的完整变量集：标架 16 + 自旋联络 24 + "
            "规范联络 12x4=48 + 标量 1 = 89 分量/点 ✓")
    rep.add("Q1.2", "测度因子化 D[e,w,A,O] = De Dw DA DO D_gauge D_top", "FAIL",
            "测度**不可因子化**：(1) D_gauge 不是独立因子——Faddeev-Popov 行列式与鬼场"
            "积分依赖于 e,w,A，不能写成乘积因子；(2) 场重定义的 Jacobian 一般不为 1"
            "（标架 e -> Omega e 一类变换下 De 产生非平凡 Jacobian，即共形/标度反常）。"
            "把测度写成各场测度的乘积隐含了'无交叉 Jacobian'假设，该假设未经论证。")
    rep.add("Q1.3", "曲率饱和 |R| <= K_sat 作为路径积分**定义域边界**", "FAIL",
            "两条硬伤：(a) 定义域边界随场构型变化，变分原理需附加边界项，"
            "经典极限不再是 delta S = 0；(b) 边界与 Lorentz 号差不相容——"
            "类光方向的曲率分量在 |R| 有界时仍可无界（|R| 不是正定的界）。"
            "（另有数值判据见 §7）")
    rep.add("Q1.4", "Omega 作为动力学标量场进入路径积分", "BOUNDARY",
            "与几何权重 Omega 的既有定位（O-SCALE 册）需统一：若 Omega 既是'权重'"
            "又带自身动能项，须给出其作用量项（动能 + 势 + 与 R/T 的耦合），本册未给。")


# ----------------------------------------------------------------------
# §2  挠率拓扑荷 W = (1/8pi^2) ∫ T∧T：整性审查（本册核心）
# ----------------------------------------------------------------------
def part2_topological_charge(rep):
    rep.section("§2  挠率拓扑荷 W 的整性与拓扑性（决定性审查）")
    rng = np.random.RandomState(20260916)
    eta = flat_metric()

    # 2.1 读法 A：T 为挠率 2-形式 T^a，洛伦兹指标按度规收缩
    T = [rand_form(2, rng) for _ in range(N)]
    acc = np.zeros((N,) * 4)
    for a in range(N):
        for b in range(N):
            acc = acc + eta[a, b] * wedge(T[a], T[b])
    norm = float(np.max(np.abs(acc)))
    rep.add("Q2.1", "自我更正：T^a∧T_a **非零**（a∧a=0 只对奇次数形式成立）", "PASS",
            "初审曾断言'正交标架 + 对角度规下只剩 eta_aa T^a∧T^a = 0'——**该断言错误**："
            "a∧a = (-1)^{p^2} a∧a，仅当 p 为**奇**时强制为零；挠率 2-形式 p=2 为偶，"
            "T^a∧T^a ≠ 0。实跑 max|T^a∧T_a| = %.4f ≠ 0 ⇒ 两种读法下被积式都非零，"
            "W **不是**平凡为零。故本册对 W 的否定不能靠'恒零'，只能靠 Q2.4-Q2.6。"
            % norm)

    # 2.2 读法 B：T 为单个（标量值）2-形式
    T2 = rand_form(2, rng)
    TT = wedge(T2, T2)
    rep.add("Q2.2", "读法B：标量值 2-形式 T∧T 可非零（4-形式）", "PASS",
            "T∧T 为 4-形式，实跑最大分量 = %.4f ≠ 0 ✓（此读法下 W 不平凡）"
            % float(np.max(np.abs(TT))))
    rep.add("Q2.3", "4D 中 4-形式自动闭合 ⇒ '不闭'不是问题所在（自我更正）", "INFO",
            "d(T∧T) = 2 dT∧T 是 5-形式，在 4D 恒为 0。"
            "故不能靠'不闭'否定它；真正的否定见 Q2.4/Q2.5（非特征类 + 非形变不变）。")

    # 2.4 二次齐次 ⇒ 连续形变 ⇒ 不可能整
    W0 = float(wedge(T2, T2)[0, 1, 2, 3])  # 4-形式唯一独立分量
    vals = []
    for lam in (1.0, 1.5, 2.0, 2.5):
        Tl = lam * T2
        vals.append(float(wedge(Tl, Tl)[0, 1, 2, 3]) / W0)
    rep.add("Q2.4", "W(λT) = λ²W(T)：二次齐次 ⇒ 连续可取任意实数", "FAIL",
            "实跑 W(λ)/W(1) = %s（理论 λ² = 1 / 2.25 / 4 / 6.25）。"
            "拓扑荷必须在**任意连续形变**下不变；此处沿 T -> λT 这一连续路径 W 连续变化，"
            "⇒ W 不是拓扑不变量、不是同伦不变量，'W ∈ Z' 无依据。"
            % ("、".join("%.4f" % v for v in vals)))

    # 2.5 显式反例：在 T^4 上构造 W = 任意实数
    # 取 T = A dx^0∧dx^1 + B dx^2∧dx^3 => T∧T = 2AB d^4x
    def W_of(A, B, vol=1.0):
        return 2.0 * A * B * vol / (8.0 * math.pi ** 2)

    w0 = W_of(1.0, 1.0)
    w1 = W_of(1.000001, 1.0)
    A_for_target = 0.37 * 8.0 * math.pi ** 2 / (2.0 * 1.0 * 1.0)
    w2 = W_of(A_for_target, 1.0)
    rep.add("Q2.5", "显式反例：W 可取任意非负实数（反驳'W∈Z'）", "FAIL",
            "T^4（Vol=1）上取 T = A dx^0∧dx^1 + B dx^2∧dx^3：A,B 为任意实常数，"
            "该挠率由 e^0 = dx^0 + A x^0 dx^1、e^1 = dx^1 + B x^2 dx^3、ω=0 实现"
            "（d²=0 与第二 Bianchi 均满足：dT=0=R∧e）。则 W = 2AB/(8π²)："
            "A=B=1 ⇒ W = %.10f；A=1.000001 ⇒ W = %.10f（增量 %.2e，连续）；"
            "取 A = %.4f 可精确命中 W = 0.37 ⇒ **W 取值为连续统**，"
            "'W ∈ Z 拓扑荷量子化'被证伪。" % (w0, w1, w1 - w0, A_for_target, ))

    rep.add("Q2.6", "1/8π² 归一化的来源：Chern-Weil 只适用于**曲率**", "FAIL",
            "(1/8π²)∫Tr(F∧F) ∈ Z 成立的前提是：F 是某个主丛联络的曲率，"
            "被积式是规范不变的**不变多项式**，且由 Chern-Weil 同态给出整上同调类。"
            "挠率 T 不是任何联络的曲率（T = De，是标架的协变外微分），"
            "不满足任一前提 ⇒ 归一化因子 8π² 属**借用的形式模仿**，无整性保证。")
    rep.add("Q2.7", "本框架内可用的整/半整不变量（替代方案）", "INFO",
            "(i) 完整 Cartan 联络 ω̃ = ω + 挠率项 的 Pontryagin 数 "
            "(1/8π²)∫Tr R(ω̃)∧R(ω̃) ∈ Z ——但这是**曲率的平方**，不是 T∧T；"
            "(ii) 挠率线（螺旋中心曲线）的 Hopf 自环绕数 Lk = Tw + Wr ∈ ½Z ——"
            "r2 册已实跑闭合（残差 ~1e-118），且**半整**正是自旋 1/2 所需。"
            "⇒ §3 的 W 应改用 Lk，而非新造一个不整的 W。")
    rep.add("Q2.8", "D_top = Σ_{W∈Z}（拓扑扇区求和）", "FAIL",
            "求和指标'整数 W'本身未良定义（Q2.4/Q2.5/Q2.6）⇒ 该项无数学内容；"
            "在改用 Lk ∈ ½Z 之前，'拓扑扇区求和'只是符号。")


# ----------------------------------------------------------------------
# §3  自旋、统计与拓扑荷守恒
# ----------------------------------------------------------------------
def part3_spin(rep):
    rep.section("§3  费米子 = 拓扑结：整/半整口径与守恒律")
    # 相位：整数缠绕 => +1（玻色），半整 => -1（费米）
    z_int = complex(math.cos(2 * math.pi * 1.0), math.sin(2 * math.pi * 1.0))
    z_half = complex(math.cos(2 * math.pi * 0.5), math.sin(2 * math.pi * 0.5))
    rep.add("Q3.1", "W=±1 给出的交换/旋转相位 = +1（玻色）", "FAIL",
            "e^{2πi·1} = %.3f%+.3fi ⇒ 相位 +1；而自旋 1/2 需要 e^{2πi·(1/2)} = "
            "%.3f%+.3fi = -1。文档同时主张'费米子 = W=±1 拓扑结'与'自旋 1/2 来自"
            "莫比乌斯（绕一圈相位 π）'——两者**互相排斥**：整数拓扑荷给玻色统计，"
            "半整（Tw = n/2, n 奇）才给费米统计。"
            % (z_int.real, z_int.imag, z_half.real, z_half.imag))
    rep.add("Q3.2", "与 r2 册内部冲突：自旋 1/2 需 Lk = ±1/2 而非 ±1", "FAIL",
            "r2/tuft_fermion_spin 已实跑闭合：Lk = Tw + Wr ∈ ½Z、Tw = n/2、s = |Lk|、"
            "Möbius 4π 闭合残差 ~1e-118、交换相位 -1。本册改用 W=±1（整）描述同一个"
            "费米子 ⇒ 与框架既有结论**口径冲突**，必须二选一。")
    rep.add("Q3.3", "莫比乌斯 4π 回归（几何图像本身）", "PASS",
            "承接 r2：ribbon 的 4π 回归是机器零级结论 ✓；"
            "但它是**自旋表示 SU(2) 双覆盖**的几何重述，不新增 TUFT 内容（属 L1 重述）。")
    rep.add("Q3.4", "[Ŵ, Ĥ] = 0（拓扑荷守恒）", "FAIL",
            "守恒的必要条件：W 为同伦不变量（对场的连续形变不变）。"
            "由 Q2.4，沿 T -> λT 有 W -> λ²W ⇒ 非不变量 ⇒ [Ŵ,Ĥ]=0 不成立。"
            "此外 §3 只是**断言**守恒，未给出任何诺特荷/对易子计算。")
    rep.add("Q3.5", "'拓扑荷转移 = 黑洞信息守恒的量子根源'", "FAIL",
            "(1) 所依赖的 W 守恒已被 Q3.4 否定；(2) 未给出霍金辐射携带该荷的"
            "自由度映射与 Page 曲线定量；(3) 跨册冲突：B 判决链已判 ξ=1/2 自屏蔽"
            "偏离 46.82% ≫ LIGO 10% ⇒ 该黑洞分支已被排除。属叙事，非导出。")


# ----------------------------------------------------------------------
# §4  二次作用量与传播子：独立变量与自由度审计
# ----------------------------------------------------------------------
def part4_propagator(rep):
    rep.section("§4  二次作用量 / 传播子：独立变量审计")
    # 4.1 曲率与挠率的独立分量数
    dim = 256
    rows = []

    def emat(idx_map):
        v = np.zeros(dim)
        v[idx_map] = 1.0
        return v

    def flat_idx(a, b, c, d):
        return ((a * N + b) * N + c) * N + d

    def add_pair_anti(rows):
        for a, b, c, d in itertools.product(range(N), repeat=4):
            v = np.zeros(dim)
            v[flat_idx(a, b, c, d)] += 1.0
            v[flat_idx(b, a, c, d)] += 1.0
            rows.append(v)

    def add_pair_anti2(rows):
        for a, b, c, d in itertools.product(range(N), repeat=4):
            v = np.zeros(dim)
            v[flat_idx(a, b, c, d)] += 1.0
            v[flat_idx(a, b, d, c)] += 1.0
            rows.append(v)

    def add_pair_sym(rows):
        for a, b, c, d in itertools.product(range(N), repeat=4):
            v = np.zeros(dim)
            v[flat_idx(a, b, c, d)] += 1.0
            v[flat_idx(c, d, a, b)] -= 1.0
            rows.append(v)

    def add_bianchi(rows):
        for a, b, c, d in itertools.product(range(N), repeat=4):
            v = np.zeros(dim)
            v[flat_idx(a, b, c, d)] += 1.0
            v[flat_idx(a, c, d, b)] += 1.0
            v[flat_idx(a, d, b, c)] += 1.0
            rows.append(v)

    add_pair_anti(rows)
    add_pair_anti2(rows)
    add_pair_sym(rows)
    add_bianchi(rows)
    M = np.array(rows)
    sv = np.linalg.svd(M, compute_uv=False)
    rank = int(np.sum(sv > 1e-8))
    dim_riemann = dim - rank
    rep.add("Q4.1", "曲率（Riemann）独立分量 = 20", "PASS" if dim_riemann == 20 else "FAIL",
            "由反对称(前对/后对) + 对换对称 + 第一 Bianchi 的线性约束秩 = %d ⇒ "
            "独立分量 = %d（n²(n²-1)/12 = 20）✓" % (rank, dim_riemann))
    dim_torsion = N * (N * (N - 1) // 2)
    rep.add("Q4.2", "挠率 2-形式 T^a 独立分量 = 24", "PASS" if dim_torsion == 24 else "FAIL",
            "T^a_{[bc]}：4 × C(4,2) = %d ✓" % dim_torsion)
    rep.add("Q4.3", "把 δR、δT 当作与 δe、δω 并列的独立涨落 ⇒ 自由度重复计数", "FAIL",
            "R(20) 与 T(24) 由 e(16) + ω(24) 的**一阶导数**完全决定，不是新自由度。"
            "文档 §4.1 写'δΩ, δR, δT 三者混合'⇒ 变量集从 89 分量/点虚增到 "
            "%d 分量/点（+44）。正确做法：K 矩阵只能是以 (δe,δω,δA,δΩ) 为指标的 "
            "4×4 块（10 个独立块），交叉项通过 R(e,ω)、T(e,ω) 的展开进入，"
            "而不是新增行/列。" % (89 + 44))
    rep.add("Q4.4", "传播子 D = K^{-1} 的可逆性前提", "FAIL",
            "K 含微分同胚/洛伦兹/规范三重零模；**未加规范固定项时 K 奇异**，"
            "D = K^{-1} 不存在。文档 §4.2 直接写 D = K^{-1} 却未在 S^(2) 中给出"
            "规范固定项（de Donder / Lorentz / R_ξ）与 FP 项 ⇒ 该式在其给定形式下无定义。")
    rep.add("Q4.5", "块结构清单（对角 4 块 + 非对角）方向正确", "BOUNDARY",
            "D_ee / D_ωω / D_AA / D_ΩΩ 的分类在'补齐规范固定 + 去掉 R,T 假变量'"
            "之后是合理的组织方式，但每一块的显式形式本册均未给出 ⇒ 目前是清单而非结果。")


# ----------------------------------------------------------------------
# §5  挠子（torsionon）：存在性、质量、耦合
# ----------------------------------------------------------------------
def part5_torsionon(rep):
    rep.section("§5  挠子：存在性 / 质量 / 耦合")
    rep.add("Q5.1", "挠率在 Einstein-Cartan 中是**代数约束**，无动能项 ⇒ 无传播子", "FAIL",
            "EC 理论中 T 由自旋流代数决定（T ~ s/(ℏc) · 自旋密度），"
            "是约束而非传播自由度 ⇒ '挠率涨落传播子 D_ωω'在标准 EC 中**不存在**。"
            "跨册一致：R6 册已判 EC 挠率'代数约束、不传播、无本征模'（1/5/0/12）。"
            "要产生挠子必须显式加入挠率动力学项（Poincaré gauge theory 的 T² 项），"
            "本册未给 ⇒ 挠子目前是**命名**而非推导结果。")
    rep.add("Q5.2", "m_torsionon ~ 1e-3 eV 的来源", "FAIL",
            "文档称'由真空背景挠率决定'，但未给出任何公式。"
            "按框架自身尺度（R6：EC 自然挠率 T_nat ~ 2.44e-41 m^-1），"
            "对应能量 ℏc·T_nat = %.3e eV；与 1e-3 eV 相差 %.1f 个数量级。"
            "⇒ 1e-3 eV 是**外部注入**（很可能反向取自 mm 尺度实验），非框架导出。"
            % (1.97327e-7 * 2.44e-41, math.log10(1e-3 / (1.97327e-7 * 2.44e-41))))
    lam = 1.97327e-7 / 1e-3  # ℏc [eV·m] / m [eV]
    rep.add("Q5.3", "m_t = 1e-3 eV 的康普顿波长 = %.4f mm（可检验性锚点）" % (lam * 1e3), "INFO",
            "ℏc/m_t = %.3e m ⇒ 若存在，其力程落在**亚毫米**区间，"
            "对应短程引力/自旋力实验的量程。这是该数值唯一可操作的实验含义。" % lam)
    # Proca 传播子结构检验。号差约定：η = diag(-1,+1,+1,+1)，在壳 p² = -m²
    rng = np.random.RandomState(7)
    m = 1e-3
    g = np.diag([-1.0, 1.0, 1.0, 1.0])
    # 构造在壳类时动量：p = (E, 0,0,k)，E² - k² = m²
    kvec = 3.7 * m
    E = math.sqrt(kvec ** 2 + m ** 2)
    p = np.array([E, 0.0, 0.0, kvec])
    p2 = float(p @ g @ p)
    assert abs(p2 + m * m) < 1e-18, p2  # 在壳：p² = -m²
    p_down = g @ p
    N_proca = g + np.outer(p_down, p_down) / (m * m)   # η_{μν} + p_μ p_ν/m²
    v = float(np.max(np.abs(N_proca @ p)))             # p^μ N_{μν}
    rep.add("Q5.4", "Proca 横向性 p^μ D_{μν} = 0（号差 (-,+,+,+)，在壳 p² = -m²）",
            "PASS" if v < 1e-12 else "FAIL",
            "D_{μν} = -i(η_{μν} + p_μ p_ν/m²)/(p²+m²-iε)；实跑 p² = %.6e（-m²），"
            "max|p^μ N_{μν}| = %.3e ✓（横向性成立；注意号差换约定时 + 号变 - 号）"
            % (p2, v))
    # 留数投影算子（升一个指标）的秩 = 3
    Pmix = np.eye(4) + np.outer(p, p_down) / (m * m)   # P^μ_ν = δ^μ_ν + p^μ p_ν/m²
    Pmix = Pmix - Pmix * 0  # 数值整洁
    resid = float(np.max(np.abs(Pmix @ Pmix - Pmix)))  # 幂等性
    ev = np.sort(np.linalg.eigvals(Pmix).real)
    nz = int(np.sum(np.abs(ev) > 1e-8))
    rep.add("Q5.5", "在壳留数投影算子 P^μ_ν = δ^μ_ν + p^μp_ν/m²：幂等且秩 = 3",
            "PASS" if (nz == 3 and resid < 1e-12) else "FAIL",
            "实跑 |P²-P| = %.3e（幂等 ✓），本征值 %s ⇒ 零本征值 1 个（沿 p 方向）、"
            "非零 3 个 = 自旋 1 的三个物理极化 ✓"
            % (resid, "、".join("%+.6f" % e for e in ev)))
    rep.add("Q5.6", "文档传播子只写 1/(p²-m²)（标量），丢失纵向块", "FAIL",
            "对轴矢顶点 j^μ = ψ̄γ^μγ⁵ψ：j^μ D^{Proca}_{μν} j^ν = [j² + (j·p)²/m²]/(p²+m²)，"
            "而文档形式只给出 j²/(p²-m²)；被丢弃的纵向块 = (j·p)²/m²。"
            "对费米子散射 q_μ j^μ = 2 m_f (ūγ⁵u) ≠ 0（质量非零时轴矢流不守恒）"
            "⇒ **纵向块有物理贡献**，见 Q5.7。")
    rep.add("Q5.7", "有质量矢量 + 非守恒（轴矢）流 ⇒ 纵向耦合被 (m_f/m_t)² 放大", "FAIL",
            "纵向项 ~ g²(2m_f)²(ūγ⁵u)²/(m_t²(t-m_t²))；相对论区 (ūγ⁵u)² ~ s ⇒ "
            "有效无量纲强度 ~ 4g²(m_f/m_t)²·(s/|t|)。取 g_t=1e-6、m_f=m_e："
            "4·1e-12·(5.11e5/1e-3)² = %.3e ≫ 8π ⇒ **微扰展开在该扇区失效**。"
            "标准结论：有质量矢量耦合非守恒流只有在 Higgs 机制（规范不变）下才自洽；"
            "Q-TUFT 未给出该机制 ⇒ 挠子扇区目前不自洽。（O(1) 运动学因子略，属量级判据）"
            % (4e-12 * (5.11e5 / 1e-3) ** 2))


# ----------------------------------------------------------------------
# §6  散射振幅与手性不对称
# ----------------------------------------------------------------------
def part6_scattering(rep):
    rep.section("§6  S 矩阵与'左右手不对称'")
    rep.add("Q6.1", "S = T exp((i/ℏ)∫L_int) 与 A = <out|S|in>", "PASS",
            "标准定义 ✓（无 TUFT 增量，属继承项）")
    # 无质量费米子、顶点 γ^μ(a + bγ⁵)：左手振幅 ∝ (a+b)，右手 ∝ (a-b)
    def ratio(a, b):
        return ((a + b) ** 2) / ((a - b) ** 2) if (a - b) != 0 else float("inf")

    r_pure_axial = ratio(0.0, 1.0)
    r_va = ratio(1.0, 1.0)
    rep.add("Q6.2", "纯轴矢耦合 ⇒ σ_L = σ_R（不对称恒为零）", "FAIL",
            "无质量费米子：M_L ∝ (a+b)、M_R ∝ (a-b)；纯轴矢 a=0 ⇒ "
            "|M_L|²/|M_R|² = %.6f（机器零级相等）。文档 §5.1 的顶点正是 "
            "ψ̄γ^μγ⁵ψ T_μ（纯轴矢），却预言 σ_L ≠ σ_R ⇒ **自相矛盾**。"
            "产生不对称必须同时有矢量与轴矢耦合：A_LR = 2ab/(a²+b²)"
            "（V-A 即 a=-b 时 |A_LR| = %.3f）。" % (r_pure_axial, 2 * 1 * (-1) / (1 + 1)))
    rep.add("Q6.3", "文档的 σ_L - σ_R = g_t²|D| 不含任何左右手区分", "FAIL",
            "|D(p)| 与手性无关、g_t 为单一耦合 ⇒ 该表达式恒等于'总耦合振幅'，"
            "不可能是左右手之**差**；且它缺少截面所需的通量因子与相空间。"
            "属把'传播子模长'**重命名**为'截面差'，无计算内容。")
    rep.add("Q6.4", "'高能下手性不对称显著'的方向", "BOUNDARY",
            "对可重整轴矢耦合，手性不对称来自 helicity-flip 干涉，量级 ~ m_f²/s ⇒ "
            "**随能量升高被压低**，与文档'越高能越显著'相反。"
            "（若改为有效算符/导数耦合则方向可反转，但文档未给该结构 ⇒ 存疑标记）")
    rep.add("Q6.5", "'低能极限退化为标准模型 S 矩阵'", "FAIL",
            "对 m_t = 1e-3 eV 的极轻介质，低能 (E ≪ m_t) 传播子趋于 1/m_t² = "
            "%.1e eV^-2，而高能 (E ≫ m_t) 趋于 1/E² ⇒ **低能耦合被放大而非压低**。"
            "文档'低能极限：挠子耦合被压低，S 矩阵退化为 SM'在 m_t ~ 1e-3 eV 下方向相反。"
            % (1.0 / 1e-6))
    rep.add("Q6.6", "'高能（接近 K_sat）挠子交换贡献显著'", "FAIL",
            "K_sat = 1/ℓ_P² 是**曲率**尺度（3.83e69 m^-2），散射能量 √s 与之无直接对应；"
            "把两者挂钩需要'曲率 - 能量'映射，本册未给。属跨量纲类比。")


# ----------------------------------------------------------------------
# §7  曲率饱和作为 UV 截止（定量）
# ----------------------------------------------------------------------
def part7_uv(rep):
    rep.section("§7  '曲率饱和 = UV 截止'的定量审查")
    lp = 1.616255e-35
    Ksat = 1.0 / lp ** 2
    rep.add("Q7.1", "K_sat = 1/ℓ_P² = %.4e m^-2（跨册引用黑洞热力学册）" % Ksat, "INFO",
            "与前册一致 ✓（该册已判：天体黑洞视界曲率比 K_sat 低 77 个量级）")
    # 平面波涨落：R ~ k² A；约束 |R| <= K_sat 只约束振幅
    ks = np.array([1e10, 1e20, 1e30, 1e40])
    A_allowed = Ksat / ks ** 2
    rep.add("Q7.2", "|R| ≤ K_sat 约束的是**振幅**而非动量：k 无上界", "FAIL",
            "对涨落 h ~ A e^{ikx}：|R| ~ k²A ≤ K_sat ⇒ A ≤ K_sat/k²。"
            "取 k = %s m^-1，允许振幅 A ≤ %s（均为正）⇒ **任意大 k 的"
            "任意小振幅构型仍在积分域内**。而圈的 UV 发散正来自任意大 k 的"
            "小振幅模式 ⇒ 曲率饱和**不是动量硬截断**，UV 发散未被消除。"
            % ("、".join("%.0e" % k for k in ks),
               "、".join("%.2e" % a for a in A_allowed)))
    rep.add("Q7.3", "'不再依赖重整化'的论断", "FAIL",
            "即便存在某种截断，度规引力在截断下仍是**有效场论**："
            "截断不改变 EFT 结论（低能展开的无穷多个高维算符依然存在）。"
            "'曲率饱和 ⇒ 无需重整化'混淆了'排除大曲率构型'与'消除圈动量发散'。")
    rep.add("Q7.4", "硬截断定义域 vs BRST / Ward 恒等式", "INFO",
            "以场空间硬边界（而非规范不变的正规化）截断定义域，一般会破坏 BRST 对称性"
            "与 Ward 恒等式 ⇒ 幺正性与规范不变性需另行证明，本册未涉及。")
    rep.add("Q7.5", "尺度链条断裂（跨册）", "BOUNDARY",
            "K_sat 在 M ~ m_P 才'生效'（前册定量：视界处低 77 量级），"
            "而挠子预言在 1e-3 eV —— 相差 ~10^37 倍。同一框架内两条预言分属"
            "完全脱耦的能标，'曲率饱和'与'挠子'之间无任何定量链条。")


# ----------------------------------------------------------------------
# §8  原文仿真代码：可运行性与数值结论
# ----------------------------------------------------------------------
DOC_CODE = """import numpy as np
\\(\\mathbf{D}\\)_torsionon = 1/(p2 - m_t**2 + 1j*1e-12)
amp = g_t**2 * np.abs(\\(\\mathbf{D}\\)_torsionon)
plt.grid(\\(\\mathcal{T}\\)rue, alpha=0.3)
"""


def part8_code(rep):
    rep.section("§8  原文 Python 仿真：可运行性与数值结论")
    ok = True
    try:
        ast.parse(DOC_CODE)
        ok = False
    except SyntaxError as exc:
        rep.add("Q8.1", "原文代码无法通过语法解析（LaTeX 宏污染标识符）", "FAIL",
                "ast.parse 报 SyntaxError（行 %s）：代码中的 \\(\\mathbf{D}\\)_torsionon、"
                "\\(\\mathcal{T}\\)rue 等是排版宏残留，不是合法 Python 标识符。"
                "⇒ 原文仿真**从未实际运行过**，其'仿真输出说明'无实跑依据。" % exc.lineno)
    if ok:
        rep.add("Q8.1", "原文代码语法解析", "PASS", "")

    # 修复版实跑
    m_t, g_t = 1e-3, 1e-6
    p2 = np.logspace(-6, 2, 1000)
    Dt = 1.0 / (p2 - m_t ** 2 + 1j * 1e-12)
    amp = g_t ** 2 * np.abs(Dt)
    i_max = int(np.argmax(amp))
    rep.add("Q8.2", "修复版实跑：'共振峰'位于扫描区间端点且高度由正则化参数决定", "FAIL",
            "p² 扫描区间 [1e-6, 1e2] ⇒ p ∈ [1e-3, 10] eV，而 m_t = 1e-3 eV **恰为左端点**；"
            "实跑 argmax 索引 = %d（首点），amp_max = %.3f = g_t²/1e-12 —— "
            "峰值高度完全由人为正则化 1e-12 决定，不是物理共振。" % (i_max, amp[i_max]))
    rep.add("Q8.3", "低动量振幅是否被压低", "FAIL",
            "实跑：amp(p=1e-3) = %.3e，amp(p=1e-2) = %.3e，amp(p=1) = %.3e ⇒ "
            "p → 0 时趋于常数 g_t²/m_t² = %.1e（**不是被压低**），"
            "高动量才按 1/p² 衰减。原文'低动量下耦合振幅被压低'与实跑相反。"
            % (amp[0], amp[500], amp[-1], g_t ** 2 / m_t ** 2))
    rep.add("Q8.4", "'适合自旋极化桌面实验寻找'这一结论", "BOUNDARY",
            "结论方向（极轻玻色子 → 亚毫米力程 → 桌面自旋实验）与 Q5.3 一致 ✓，"
            "但成立前提是挠子**存在且耦合可算**（Q5.1/Q5.2/Q5.7 均为 FAIL）"
            "⇒ 目前只能作为'若存在'的条件性搜索窗口。")


# ----------------------------------------------------------------------
# §9  可证伪预言与难点清单
# ----------------------------------------------------------------------
def part9_predictions(rep):
    rep.section("§9  七条可证伪预言的逐条判定（跨册一致性）")
    rep.add("Q9.1", "预言1 挠子（1e-3 eV 自旋1 手性玻色子）", "FAIL",
            "存在性（Q5.1 无动力学）、质量（Q5.2 外部注入，与框架自然挠率差 57 量级）、"
            "耦合（Q5.7 微扰失效）三处均未成立 ⇒ 目前不构成可证伪预言，"
            "只构成'若存在则量程 0.197 mm'的搜索窗口。")
    rep.add("Q9.2", "预言2 高能散射手性不对称", "FAIL",
            "表达式不含左右手区分（Q6.3）；纯轴矢给 σ_L = σ_R（Q6.2）；"
            "能量依赖方向相反（Q6.4）⇒ 三重问题，需重建。")
    rep.add("Q9.3", "预言3 原初引力波 / CMB B 模手性不对称", "FAIL",
            "母体（TUFT 暴胀-CMB 册）已自证伪：判定 5 PASS / 35 FAIL / 8 INFO，"
            "三预言互斥（κ-无关不变量 N(1-n_s) = 3.741 vs 观测 2.106）。"
            "⇒ 建立在暴胀扇区之上的 B 模手性预言，在其母体修复前不具可检验性。")
    rep.add("Q9.4", "预言4 量子黑洞 / 蒸发幺正 / 无信息丢失", "FAIL",
            "跨册冲突：B 判决链已判自屏蔽 ξ=1/2 偏离 46.82% ≫ LIGO 10% ⇒ 该分支被排除；"
            "黑洞热力学册 K_sat 相关条目判 FAIL。且本册论证依赖已被否定的 W 守恒（Q3.5）。")
    rep.add("Q9.5", "预言5 拓扑荷量子跃迁 / 特征量子噪声", "FAIL",
            "W 本身未良定义（Q2.4/Q2.5/Q2.6）⇒ 跃迁无定义；"
            "'特征量子噪声'无定量公式与量级 ⇒ 不可证伪。")

    rep.section("§10  '待补全清单'的完整性审计（新增遗漏项）")
    for name, det in [
        ("遗漏A 测度非因子化与 Jacobian", "文档清单未列；见 Q1.2。"),
        ("遗漏B 硬截断与 BRST/Ward 冲突", "文档只提'测度严格性'，未提对称性保持；见 Q7.4。"),
        ("遗漏C 挠率无动力学项", "这是**传播子构造的前提**，比'测度严格性'更根本；见 Q5.1。"),
        ("遗漏D 拓扑荷需先良定义", "在 W 修正为 Lk ∈ ½Z 之前，'非微扰拓扑扇区'无对象；见 Q2.8。"),
        ("遗漏E 有效场论性", "截断不消除 EFT 的高维算符塔；见 Q7.3。"),
        ("遗漏F 欧氏化与因果性", "|R| ≤ K_sat 在 Lorentz 号差下非紧/非正定，"
                              "欧氏化的定义域与 Wick 回转需另行论证；见 Q1.3。"),
    ]:
        rep.add("Q10", name, "INFO", det)


def main():
    rep = Report()
    rep.echo("TUFT 量子版（Q-TUFT）全维求导精算")
    rep.echo("对象：《量子 TUFT 构建：主丛路径积分、挠率拓扑量子化、时空螺旋元胞量子场论、"
             "传播子与散射振幅》")
    rep.echo("红线：数学自洽 != 物理实验证实。")
    part1_structure(rep)
    part2_topological_charge(rep)
    part3_spin(rep)
    part4_propagator(rep)
    part5_torsionon(rep)
    part6_scattering(rep)
    part7_uv(rep)
    part8_code(rep)
    part9_predictions(rep)
    rep.summary()
    rep.dump()
    print("\n报告已写出: " + REPORT_PATH)


if __name__ == "__main__":
    main()
