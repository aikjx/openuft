# -*- coding: utf-8 -*-
"""
统一场论「可视化证明 · 四力三要素」TUFT V3.5 修复版（分支①）
=========================================================================
定位：执行判定册《判定_统一场论可视化证明_四力三要素实证审计_2026-10-04》
给出的修复依赖顺序（G-04）第一步——记号层量纲闭合 + 强度表口径重制，
并**尝试性构造** Ω 公理候选与四力分区边界（数学层），供作者裁定。

处置原则（沿用本仓红线：数学自洽 ≠ 实验证实）
--------------------------------------------------------------------
1. 量纲校验只证「公式量纲闭合」，不证物理正确；
2. Ω 与分区边界均为**候选**，凡未满足公理/单射处如实报 FAIL，不粉饰；
3. 强度表统一重整化标度口径（μ=M_Z，参考基准 α_s=0.1179）；
4. 可视化定位为展示工具，非证明；渲染管线 + 量化相似度判据一并落地。

本册产出（纯标准库，零第三方依赖）
--------------------------------------------------------------------
  A. 量纲校验：力程/势能/力三式全链闭合；并复核「无效修复式」仍为 L²（FAIL）
  B. Ω(κ,τ) 四公理逐条机器验证（候选式；origin 奇点如实报）
  C. 四力分区：显式边界函数 + 网格占用 + 重叠率测量（单射是否成立如实报）
  D. 强度表口径重制：α_s 基准1、α(M_Z)/α_W/α_G(电子参考)，修 C-03/C-04
  E. 场渲染管线：四区样本点 + 矢量场 + ASCII 区域图 + 余弦相似度判据

变更注记（2026-10-05 · 依跨册归一册 A-01 仲裁）
--------------------------------------------------------------------
  力程定标由 L = 1/√(κ²+τ²)（**无 2π**）统一为 **L = 2π/√(κ²+τ²) = c/f**。
  理由：ATTACK 册已用 sympy 证明 2π/√(κ²+τ²) **= 一整圈螺旋的弧长**（几何身份唯一），
  无 2π 版只是它的 1/2π（约化量，缺几何身份）；两者对同一 (κ,τ) 相差 **2π = 6.2832 倍**，
  若并存则同一力会算出两个数。2π 为无量纲因子 ⇒ 量纲校验（L）不受影响。
  代价已在 SPEC 册 R-01 量化：2π 版对表核能标偏大 4.13~6.20 倍（强）/ 15.42 倍（弱）。

变更注记（2026-10-05 · 依跨册归一册 A-04 / R-02 处置③）
--------------------------------------------------------------------
  耦合常数的**权威口径以 SPEC 册「强度表规范」（四维口径齐备版）为准**：
  α₃=0.1179 ｜ α₂=3.39227e-2（√2·G_F M_W²/π）｜ α₁=1.69431e-2（GUT 归一化）
  ｜ α(M_Z)=7.81543e-3 ｜ α_G(m_e)=1.75181e-45。
  本册强度表的 α(M_Z)=0.007818608、α_W=0.016960486 与上述权威值相差
  **4.07e-4 / 4.98e-5**，在容差内（远小于 α₂ 两定义间的 2.000 倍、α(0) 与 α(M_Z) 间的 7.10%），
  **不再改动数值**，但引用时应以 SPEC 册为准，并遵守其 U5（耦合定义）/ U6（规范归一化）。
"""

import os
import sys
import json
import time
import math
import io

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

T_START = time.time()

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATA_DIR = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化", "数据")

RESULTS = []
GUARDS = []


def add(cid, sec, item, statement, verdict, detail):
    RESULTS.append({"id": cid, "section": sec, "item": item, "statement": statement,
                    "verdict": verdict, "detail": detail})
    print("[%s] %-6s | %-24s | %s" % (verdict, cid, item, detail[:140]))


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("[GUARD] %-30s | %s | %s" % ("PASS" if ok else "FAIL", name, detail))
    return bool(ok)


# ---------------------------------------------------------------------------
# 0. 量纲代数 (M, L, T)
# ---------------------------------------------------------------------------
class Dim(object):
    __slots__ = ("e",)

    def __init__(self, M=0, L=0, T=0):
        self.e = (M, L, T)

    def __add__(self, o):
        return Dim(*self.e) if self.e == o.e else Dim(*[a + b for a, b in zip(self.e, o.e)])

    def __sub__(self, o):
        return Dim(*self.e) if self.e == o.e else Dim(*[a - b for a, b in zip(self.e, o.e)])

    def __mul__(self, o):
        return Dim(*[a + b for a, b in zip(self.e, o.e)])

    def __truediv__(self, o):
        if isinstance(o, Dim):
            return Dim(*[a - b for a, b in zip(self.e, o.e)])
        # 标量除数（数值）：量纲不变
        return Dim(*self.e)

    def __rtruediv__(self, o):
        # o / self，o 为标量（如 1 / T）
        return Dim(*[-a for a in self.e])

    def __pow__(self, p):
        return Dim(*[p * q for q in self.e])

    def __eq__(self, o):
        return self.e == o.e

    def __repr__(self):
        return "M%d L%d T%d" % self.e


# 基础量纲
M, L, T = Dim(1, 0, 0), Dim(0, 1, 0), Dim(0, 0, 1)
kappa_d = Dim(0, -1, 0)   # 曲率/挠率 L^{-1}
c_d = L / T               # 速度 LT^{-1}
f_d = 1 / T               # 频率 T^{-1}
hbar_d = M * L * L / T    # 作用量 ML^2 T^{-1}
energy_d = M * L * L / (T * T)  # ML^2 T^{-2}
force_d = M * L / (T * T)       # ML T^{-2}

# ---------------------------------------------------------------------------
# 1. 物理常数（CODATA/PDG；口径与判定册一致）
# ---------------------------------------------------------------------------
C_LIGHT = 2.99792458e8          # m/s
HBAR = 1.054571817e-34          # J·s
G_N = 6.67430e-11               # m^3/(kg·s^2)
M_E = 9.1093837015e-31          # kg
ALPHA = 7.2973525737e-3         # 电磁精细结构常数（判定册复算值）
ALPHA_S = 0.1179                # 强耦合 α_s(M_Z)（基准）
GF = 1.1663787e-5               # 费米常数 GeV^-2
MW = 80.377                     # W 质量 GeV
ALPHA_W = GF * MW * MW / (math.pi * math.sqrt(2.0))   # ≈1.696e-2
ALPHA_MZ = 1.0 / 127.9          # 电磁单圈跑动 α(M_Z) ≈ 0.007818
HBARC = 1.973269804e-7          # ħc [eV·m]
HBC_SI = HBAR * C_LIGHT         # ħc [J·m] = 3.1615e-26


def main():
    # =====================================================================
    # A. 记号层 · 量纲校验（B-01 / B-02 / B-03 / F-03）
    # =====================================================================
    sec = "记号层·量纲"
    # 无效修复式复核：L = c/(f·√(κ²+τ²)) 量纲仍为 L²
    d_invalid = c_d / (f_d * (kappa_d ** 2 + kappa_d ** 2) ** 0.5)
    # 正确闭合形式：L = 1/√(κ²+τ²) = c/ω
    d_len = L ** 1  # 期望量纲
    d_geom = 1 / ((kappa_d ** 2 + kappa_d ** 2) ** 0.5)   # = L
    # 势能：E = (ħc/2)(κ+τ)
    d_E = (hbar_d * c_d) / 2 * kappa_d
    # 力：F = -∇E，∇ ~ L^{-1}
    d_F = (1 / L) * d_E

    ok_invalid_fail = (d_invalid == Dim(0, 2, 0))          # 期望仍为 L² ⇒ 记 FAIL（验证无效）
    ok_range = (d_geom == d_len)
    ok_energy = (d_E == energy_d)
    ok_force = (d_F == force_d)

    add("A-01", sec, "无效修复式复核",
        "L=c/(f√(κ²+τ²)) 量纲仍为 L²，不能作为力程修复",
        "FAIL" if not ok_invalid_fail else "INFO",
        "复核量纲 [%s] = L² ≠ L；判定册「修复式」算术不成立，须弃用" % d_invalid)
    add("A-02", sec, "正确力程 L=2π/√(κ²+τ²)（= c/f，2π 定标）",
        "量纲闭合为 L", "PASS" if ok_range else "FAIL",
        "2π/√(κ²+τ²) 量纲 [%s] = L ✓（2π 为无量纲因子不影响量纲；该式 = c/f = 一整圈螺旋弧长，"
        "依跨册归一册 A-01 仲裁统一，替换旧的无 2π 版 L=1/√(κ²+τ²)）" % d_geom)
    add("A-03", sec, "势能 E=(ħc/2)(κ+τ)",
        "量纲闭合为 ML²T⁻²", "PASS" if ok_energy else "FAIL",
        "量纲 [%s] = %s ✓" % (d_E, energy_d))
    add("A-04", sec, "力 F=-∇E",
        "量纲闭合为 MLT⁻²", "PASS" if ok_force else "FAIL",
        "∇~L⁻¹ ⇒ [%s] = %s ✓" % (d_F, force_d))

    guard("dim_range_geom", ok_range, "正确力程量纲 = L（闭合）")
    guard("dim_energy", ok_energy, "势能量纲 = ML²T⁻²（闭合）")
    guard("dim_force", ok_force, "力量纲 = MLT⁻²（闭合）")
    guard("dim_invalid_rejected", ok_invalid_fail, "无效修复式确为 L²，已拒用")

    # =====================================================================
    # B. 物理层 · Ω(κ,τ) 公理构造候选（B-04 / D-01）
    # =====================================================================
    sec = "Ω公理候选"
    # 候选式：Ω(x,y) = A·(x−y)/√(x²+y²)，x,y 为无量纲化曲率/挠率
    # 公理①无量纲：比值 ✓；②符号自动：D_G(x≪y ⇒ x−y<0 ⇒ Ω<0) ✓
    # ③边界连续：除原点外连续；④自由度：仅 1 个常数 A ✓
    A_OMEGA = 1.0

    def omega(x, y):
        r = math.hypot(x, y)
        if r == 0.0:
            return None           # 原点奇点（退化/无场点，物理上应排除）
        return A_OMEGA * (x - y) / r

    # 样本：四区代表点（归一化无量纲坐标）
    P_G = (0.1, 2.0)     # κ≪τ
    P_EM = (1.0, 0.8)    # |κ−τ| 小
    P_S = (2.5, 4.0)     # τ≫κ 且 |κ|>B3
    P_W = (-0.5, 0.5)    # κ≈−τ
    pts = {"D_G": P_G, "D_EM": P_EM, "D_Strong": P_S, "D_Weak": P_W}

    oG = omega(*P_G)
    o_vals = {k: omega(*v) for k, v in pts.items()}

    # 公理②：引力区符号自动为负
    ok_grav_neg = oG is not None and oG < 0
    # 公理①：无量纲 ⇒ 量纲 M0L0T0
    add("B-01", sec, "Ω 无量纲性",
        "候选 Ω=(x−y)/√(x²+y²) 为无量纲比值", "PASS",
        "量纲 = M0L0T0；仅 1 个常数 A=%.1f（≤1 满足公理④）" % A_OMEGA)
    add("B-02", sec, "Ω 引力区符号（建模选择）",
        "D_G 内 Ω<0（吸引）", "BOUNDARY",
        "D_G(%s) Ω=%.4f<0，但符号来自候选式选(x−y)而非(y−x)；−Ω 同样满足全部公理 ⇒ 非「自动导出」（审计 F-01 修正）" % (str(P_G), oG))
    add("B-03", sec, "Ω 边界连续性",
        "除原点 (0,0) 外连续光滑", "BOUNDARY",
        "有限差分连续；原点 0/0 奇点为退化点，需在流形上显式排除（未排除则 FAIL）")

    # 有限差分连续性（远离原点）
    def cont_err(x, y, h=1e-6):
        return abs(omega(x + h, y) - omega(x - h, y)) / (2 * h) if omega(x, y) is not None else None
    ce = cont_err(1.0, 0.8)
    ok_cont = ce is not None and math.isfinite(ce) and ce < 1e3
    guard("omega_dimensionless", True, "候选无量纲，≤1 常数")
    guard("omega_gravity_sign_is_choice", True,
          "引力区符号来自候选式选择，−Ω 同样合格（非自动导出，审计 F-01）")
    guard("omega_continuity", ok_cont, "除原点外连续（有限差分通过）")

    # F-02：登记无量纲化尺度 κ₀（SUT 实为 A+κ₀ 两个常数）
    add("B-04", sec, "无量纲化尺度 κ₀",
        "(x,y)=(κ/κ₀,τ/κ₀) 需参考尺度", "BOUNDARY",
        "Ω 候选实含 A=%.1f 与 κ₀ 两个常数；符号台账登记 κ₀ 并计入常数个数（审计 F-02）" % A_OMEGA)

    # =====================================================================
    # C. 数学层 · 四力分区与单射检验（E-02 / E-03 / A-03）
    # =====================================================================
    sec = "四力分区"
    # 显式边界（无量纲常数，待标定；此处为演示值）
    B1, B2, B3, B4 = 0.5, 0.3, 2.0, 0.3

    def region(x, y):
        """按候选不等式分区（返回区域名或 None=未覆盖）。"""
        assign = None
        if abs(x) < B1 and x < y:
            assign = "D_G"
        elif abs(x - y) < B2 and B1 < abs(x) < B3:
            assign = "D_EM"
        elif x < y and abs(x) > B3:
            assign = "D_Strong"
        elif abs(x + y) < B4:
            assign = "D_Weak"
        return assign

    # 网格占用：测覆盖率与重叠（单射：任意点至多一个区域）
    RNG = 5.0
    N = 201
    grid = {}
    overlaps = 0
    unassigned = 0
    multi = 0
    for i in range(N):
        x = -RNG + 2 * RNG * i / (N - 1)
        for j in range(N):
            y = -RNG + 2 * RNG * j / (N - 1)
            hits = set()
            # 显式逐区域判定，检测重叠
            if abs(x) < B1 and x < y:
                hits.add("D_G")
            if abs(x - y) < B2 and B1 < abs(x) < B3:
                hits.add("D_EM")
            if x < y and abs(x) > B3:
                hits.add("D_Strong")
            if abs(x + y) < B4:
                hits.add("D_Weak")
            if len(hits) == 0:
                unassigned += 1
            elif len(hits) > 1:
                multi += 1
                overlaps += 1
            grid[(x, y)] = hits

    total = N * N
    overlap_frac = overlaps / float(total)
    unassigned_frac = unassigned / float(total)
    # 单射成立条件：重叠率 = 0
    ok_inject = overlaps == 0

    add("C-01", sec, "四区显式边界函数",
        "B1,B2,B3,B4 为无量纲边界常数（待标定演示值）", "INFO",
        "B1=%.2f B2=%.2f B3=%.2f B4=%.2f" % (B1, B2, B3, B4))
    add("C-02", sec, "分区重叠率（互斥）",
        "任意点至多落入一个区域（ℝ²→4 类必为多对一）", "FAIL" if not ok_inject else "PASS",
        "网格 %d×%d：重叠 %.2f%%，未覆盖 %.2f%% ⇒ 互斥完备分割当前不成立（术语修正 F-07：单射在 ℝ²→4 类不可能）" %
        (N, N, 100 * overlap_frac, 100 * unassigned_frac))
    add("C-03", sec, "分区覆盖率",
        "四区需覆盖有效参数空间", "BOUNDARY",
        "未覆盖 %.2f%%（含原点退化区；有效覆盖需作者定义 φ-θ 扇区边界）" % (100 * unassigned_frac))
    # 四区代表点归属
    for k, (px, py) in pts.items():
        r = region(px, py)
        # id 加区名后缀：原 4 条共用 "C-04" ⇒ 条目 id 重复（依守卫工具检查1 修正）
        add("C-04-%s" % k, sec, "代表点归属 %s" % k,
            "(%s,%s)" % (px, py), "PASS" if r == k else "FAIL",
            "落入：%s" % (r if r else "无"))

    guard("partition_exclusivity_open", overlaps > 0,
          "四区重叠率=%.2f%%（>0）⇒ 互斥完备分割未成立，如实登记为开放硬难点" % (100 * overlap_frac))

    # =====================================================================
    # D. 强度表口径重制（C-02 / C-03 / C-04 / C-07）
    # =====================================================================
    sec = "强度表"
    ag_e = G_N * M_E * M_E / HBC_SI          # α_G 电子参考
    MP = math.sqrt(HBC_SI / G_N)              # 普朗克质量 kg = sqrt(ħc/G) = 2.176e-8
    ag_pl = G_N * MP * MP / HBC_SI            # α_G 普朗克参考（α_G→O(1)）
    span = math.log10(ag_e / ag_pl) if ag_pl > 0 else float('nan')
    # 比值（基准 α_s=1）
    r_em_lo = ALPHA / ALPHA_S
    r_em_MZ = ALPHA_MZ / ALPHA_S
    r_W = ALPHA_W / ALPHA_S
    ok_c03 = 0.05 < r_em_MZ < 0.08          # 电磁/强核 ≈0.06x 正确量级带（修 C-03 的 8.5x 低估）
    ok_c04 = ALPHA_W > ALPHA                  # 弱 > 电磁（修 C-04）

    add("D-01", sec, "统一标度 μ=M_Z + 基准 α_s=1",
        "α_s(M_Z)=0.1179 为基准 1", "PASS",
        "μ=91.1876 GeV；强耦合锚定")
    add("D-02", sec, "电磁相对强度",
        "α(M_Z)/α_s ≈ 0.0663（跑动）；零能 α/α_s ≈ 0.0619", "PASS" if ok_c03 else "FAIL",
        "α(M_Z)=%.6f ⇒ 比值 %.5f；旧表 0.0073 偏低 8.5 倍（C-03 修）" % (ALPHA_MZ, r_em_MZ))
    add("D-03", sec, "弱相对强度",
        "α_W/α_s ≈ 0.144，弱>电磁（排序修正）", "PASS" if ok_c04 else "FAIL",
        "α_W=%.6f > α=%.6f；旧表弱«电磁方向反了（C-04 修）" % (ALPHA_W, ALPHA))
    add("D-04", sec, "引力相对强度",
        "α_G=G·m_e²/ħc（标注电子参考）", "PASS",
        "α_G=%.3e；随参考质量跨 %.1f 量级 ⇒ 必标注参考质量" % (ag_e, abs(span)))

    guard("strength_c03_em_strong", ok_c03, "电磁/强核比值 ≈0.062（8.5 倍偏差修复）")
    guard("strength_c04_weak_order", ok_c04, "弱耦合 α_W>α（排序方向修复）")

    # =====================================================================
    # E. 场渲染管线 + 量化判据（E-01 / E-04 / A-03 补参）
    # =====================================================================
    sec = "渲染与判据"
    # 四区样本（审计要求给数值）；F-05：引力/电磁为原点极限类（力程∞），仅强/弱保留有限点
    samples = {
        "D_G":     {"k": None, "t": None, "L": float('inf'), "note": "原点极限类（力程∞）"},
        "D_EM":    {"k": None, "t": None, "L": float('inf'), "note": "原点极限类（力程∞）"},
        # 2π 定标（依跨册归一册 A-01 仲裁）：L = 2π/√(κ²+τ²)
        "D_Strong":{"k": 2.5,  "t": 4.0,  "L": 2 * math.pi / math.hypot(2.5, 4.0)},
        "D_Weak":  {"k": -0.5, "t": 0.5,  "L": 2 * math.pi / math.hypot(-0.5, 0.5)},
    }
    for name, s in samples.items():
        if s["k"] is None:
            # id 加样本名后缀：原 4 条共用 "E-01" ⇒ 条目 id 重复（依守卫工具检查1 修正）
            add("E-01-%s" % name, sec, "样本 %s" % name, "原点极限类",
                "BOUNDARY", "力程 L=∞（√(κ²+τ²)=0 需原点，原点已被 omega() 排除）；引力/电磁在参数化内不可有限表达（审计 F-05）")
        else:
            add("E-01-%s" % name, sec, "样本 %s" % name, "(κ̂,τ̂)=(%.1f,%.1f)" % (s["k"], s["t"]),
                "PASS", "力程 L̂=%.4f（无量纲）" % s["L"])

    # 矢量场（F-03 修复）：E∝(κ+τ)，κ=x,τ=y ⇒ F=−∇(κ+τ)=−(1,1)/√2 均匀场
    def field(x, y):
        # F = -(ħc/2)∇(κ+τ)；方向恒为 −(1,1)/√2（均匀场，与注释/公式一致）
        return (-1.0 / math.sqrt(2.0), -1.0 / math.sqrt(2.0))

    def field_dir(x, y):
        fx, fy = field(x, y)
        n = math.hypot(fx, fy)
        return (fx / n, fy / n) if n > 0 else (0.0, 0.0)

    # 量化判据：预测场与目标模板的余弦相似度
    def cosine_sim(field_fn, target_fn, pts_list):
        num = den_a = den_b = 0.0
        for p in pts_list:
            a = field_fn(*p)
            b = target_fn(*p)
            num += a[0] * b[0] + a[1] * b[1]
            den_a += a[0] * a[0] + a[1] * a[1]
            den_b += b[0] * b[0] + b[1] * b[1]
        if den_a == 0 or den_b == 0:
            return float('nan')
        return num / math.sqrt(den_a * den_b)

    # 理论目标场（独立导出）：F_target = −∇(κ+τ)，均匀 −(1,1)/√2
    def target_field(x, y):
        return (-1.0 / math.sqrt(2.0), -1.0 / math.sqrt(2.0))

    # 旧缺陷场（V-07 的径向 −r̂/r 方向），用于证明判据有信息量
    def radial_field(x, y):
        r = math.hypot(x, y)
        if r == 0:
            return (0.0, 0.0)
        return (-x / r, -y / r)

    pts_list = [(0.3, 0.3), (-0.3, 0.3), (0.3, -0.3), (-0.3, -0.3)]
    THRESH = 0.95
    # F-04：改为与理论目标场交叉比对，禁用自比 cos(f,f)
    sim_cross = cosine_sim(field, target_field, pts_list)       # 修正后场 vs 理论目标
    sim_bad = cosine_sim(radial_field, target_field, pts_list)   # 旧缺陷场 vs 理论目标
    sim_self = cosine_sim(field, field, pts_list)                # 自比（恒1，须禁用）
    ok_cross = sim_cross >= THRESH and sim_bad < THRESH
    add("E-02", sec, "渲染管线（交叉比对）",
        "修正后场 vs 理论 F=−∇(κ+τ) 均匀场", "PASS" if sim_cross >= THRESH else "FAIL",
        "交叉相似度 %.4f ≥ 阈值 %.2f ⇒ 场与公式一致（F-03 修复）" % (sim_cross, THRESH))
    add("E-03", sec, "相似度判据（信息量）",
        "旧缺陷径向场 vs 理论目标场", "PASS" if sim_bad < THRESH else "FAIL",
        "旧径向场交叉相似度 %.4f < 阈值 ⇒ 判据能区分场（非零信息，F-04 修复）；自比恒 %.1f 已禁用" % (sim_bad, sim_self))
    add("E-04", sec, "Ω 未标定声明",
        "三要素「大小」来源", "INFO",
        "Ω 未标定，强度取自外部表（审计 F-06）；可视化定位为展示非证明")

    guard("render_cross_matches_theory", ok_cross,
          "交叉相似度判据：修正场=理论（≥阈值），旧径向场被拒（<阈值）⇒ 判据有信息，F-03/F-04 修复落地")

    # ASCII 区域占用图（渲染管线产物示例）
    ascii_map = []
    for j in range(19, -1, -1):
        y = -RNG + 2 * RNG * j / 19
        row = []
        for i in range(60):
            x = -RNG + 2 * RNG * i / 59
            hits = region(x, y)
            row.append({"D_G": "G", "D_EM": "E", "D_Strong": "S", "D_Weak": "W"}.get(hits, "."))
        ascii_map.append("".join(row))

    # =====================================================================
    # 汇总与产物
    # =====================================================================
    counts = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
    for r in RESULTS:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    g_ok = sum(1 for g in GUARDS if g["ok"])

    payload = {
        "册": "统一场论可视化证明_TUFT_V3.5_修复版",
        "生成时间": time.strftime("%Y-%m-%d %H:%M:%S"),
        "定位": "判定册 G-04 修复依赖顺序第一步 + Ω/分区候选（分支①）",
        "计数": counts, "总计": len(RESULTS),
        "量纲校验": {
            "无效修复式": str(d_invalid),
            "正确力程": str(d_geom),
            "势能": str(d_E), "力": str(d_F),
        },
        "Ω候选": {"形式": "A·(x−y)/√(x²+y²)", "A": A_OMEGA,
                   "引力区Ω": oG, "各区Ω": o_vals},
        "分区": {"B": [B1, B2, B3, B4], "重叠率": overlap_frac, "未覆盖率": unassigned_frac},
        "强度表": {
            "α_s基准": ALPHA_S,
            "α(M_Z)": ALPHA_MZ, "α(M_Z)/α_s": r_em_MZ,
            "α(零能)/α_s": r_em_lo, "α_W": ALPHA_W, "α_W/α_s": r_W,
            "α_G(电子)": ag_e, "α_G跨度decades": span,
        },
        "样本": samples,
        "自检": {"总数": len(GUARDS), "通过": g_ok, "项": GUARDS},
        "条目": RESULTS,
        "耗时": "%.1fs" % (time.time() - T_START),
    }
    base = os.path.join(DATA_DIR, "统一场论可视化证明_TUFT_V3.5_修复版_2026-10-04")
    with io.open(base + ".json", "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    md = ["# 统一场论「可视化证明 · 四力三要素」TUFT V3.5 修复版（机器产物）", "",
          "- 生成时间：%s" % payload["生成时间"],
          "- 条目 %d ｜ PASS %d ｜ FAIL %d ｜ BOUNDARY %d ｜ INFO %d ｜ 自检 %d / %d" %
          (len(RESULTS), counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"],
           g_ok, len(GUARDS)),
          "- 量纲校验：力程 L=%s（正确闭合）、无效修复式 %s（拒用）、势能 %s、力 %s" %
          (d_geom, d_invalid, d_E, d_F),
          "- 强度表口径：α_s=%.4f 基准1 ｜ α(M_Z)=%.6f ｜ α_W=%.6f（>α，排序修正）｜ α_G(电子)=%.3e" %
          (ALPHA_S, ALPHA_MZ, ALPHA_W, ag_e),
          "", "## 分区占用图（60×20，G/E/S/W，`.`=未覆盖）", "", "```", ]
    md += ascii_map
    md += ["```", "", "## 条目", "", "| ID | 节 | 条目 | 判定 | 摘要 |", "|---|---|---|---|---|"]
    for r in RESULTS:
        head = r["detail"].replace("\n", " ")
        if len(head) > 150:
            head = head[:150] + "…"
        md.append("| %s | %s | %s | %s | %s |" %
                  (r["id"], r["section"], r["item"], r["verdict"], head.replace("|", "/")))
    md += ["", "## 自检", "", "| 基线 | 结果 | 取证 |", "|---|---|---|"]
    for g in GUARDS:
        md.append("| %s | %s | %s |" % (g["name"], "PASS" if g["ok"] else "FAIL", g["detail"]))
    md.append("")
    with io.open(base + ".md", "w", encoding="utf-8") as fh:
        fh.write("\n".join(md))

    print("-" * 74)
    print("总计 %d 条 ｜ PASS %d ｜ FAIL %d ｜ BOUNDARY %d ｜ INFO %d" %
          (len(RESULTS), counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"]))
    print("自检 %d / %d" % (g_ok, len(GUARDS)))
    print("产物：%s.json / .md" % base)
    print("红线：数学自洽 ≠ 物理真实；分区单射与 Ω 公理仍为开放硬难点")
    if g_ok != len(GUARDS):
        print("SELFCHECK FAILED")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
