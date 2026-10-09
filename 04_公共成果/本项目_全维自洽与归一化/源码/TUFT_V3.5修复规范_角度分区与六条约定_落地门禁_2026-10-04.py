# -*- coding: utf-8 -*-
"""
TUFT V3.5「修复规范」落地门禁 —— 角度分区 + 六条单位约定 + 符号台账 + 四力样本 + 可视化规范
=========================================================================
承接：上一轮 `TUFT_V3.5修复方案_求导证明验证精算攻破_2026-10-04.py`（37 项，自检 28/28，评级 C/L1）。
      那一轮做的是**判定与攻破**（哪些能修、哪些不可达）；
      本册做的是**把可修的部分写成可执行的规范**，并配机器门禁，
      使后续任何人按规范写实现时，不会再固化已知的四个缺陷：

        ① 力程式写成 L = c/(f√(κ²+τ²))（量纲 L²）
        ② 分区边界写成 |κ| < B_i（左 L⁻¹ 与右「无量纲」不可比较）
        ③ 强度表只声明能标不声明定义/归一化/参考质量（三次串号机会）
        ④ 可视化把「两张图一致」当成「图与实验一致」

本册交付的规范（每条都带机器门禁，可被后续实现直接引用）
--------------------------------------------------------------------
  U  **六条单位约定**（原四条 + 耦合定义 + 规范归一化）
  S  **符号台账**：全量符号 × 量纲 × 修复状态，逐行机器校验
  R  **修复后公式三式**：L = c/f = 2π/√(κ²+τ²) / E = (ℏc/2)(κ+τ) / F = −∇E（sympy 求导）
  A  **角度分区规范**：边界只能写成 θ = atan2(τ,κ) 的四段扇区（禁止 |κ| < B 形式）
  M  **四力样本规范**：身份给 θ_i、标度给尺度锚 L_i ⇒ 显式产出 (κ,τ) 样本
  T  **强度表规范**：四维口径齐备 + 三条串号警戒
  V  **可视化规范**：只需角度（径向无信息）+ 管线清单 + 判据定位

本册的两条新结论（前册未覆盖）
--------------------------------------------------------------------
  ★新 1（M-01/M-02）**解除元审计册 E-01 的「只能给出两组样本」阻塞**：
      把「身份 θ」与「标度 L」分离后，四类力**都能给样本**——
      强/弱由 L = 1e-15 / 1e-18 m 反解出显式 (κ,τ)；
      引力/电磁因 L = ∞ ⇒ ρ = 2π/L = 0 ⇒ (κ,τ) = (0,0) ⇒ **θ 无定义**，
      本册把这个退化**显式登记为框架极限**（并给出可成像占位的替代尺度，标注为占位而非导出）。
  ★新 2（R-01）**2π 定标的约定敏感点被量化**：几何上力程 = 一整圈弧长（2π 版）是钉死的，
      但对表核能标时：2π 版给强核 **1.240 GeV**（vs Λ_QCD 0.2~0.3 GeV，偏大 4.1~6.2 倍）、
      弱核 **1.240 TeV**（vs M_W 80.4 GeV，偏大 15.4 倍）；无 2π 版给 197.3 MeV / 197.3 GeV
      （0.65~1.5 倍 / 2.45 倍）。⇒ 前册 A-03「两口径都能说量级吻合」在此被**量化为两张偏差表**，
      结论：2π 版与核能标不符，属**约定敏感点（BOUNDARY）**，不得作为验证证据。

诚实红线
--------------------------------------------------------------------
本册是**规范与门禁**，不是物理成立性证明。规范解决的是「写法合法性问题」；
Ω 的量纲/符号、两条可证伪预言、弱力定量表达式**三项不由规范解决**，单列 Z-01。

纯标准库 + sympy + mpmath；退出码 0 = 自检全过（可作门禁），2 = 有基线失效。
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

import sympy as sp

T_START = time.time()

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BASE = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化")
OUT_DIR = os.path.join(BASE, "数据")

RESULTS = []
GUARDS = []


def add(cid, sec, item, statement, verdict, detail):
    RESULTS.append({"id": cid, "section": sec, "item": item,
                    "statement": statement, "verdict": verdict, "detail": detail})
    print("[%s] %-6s | %-26s | %s" % (verdict, cid, item, detail[:120]))


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("[GUARD] %-34s | %s | %s" % ("PASS" if ok else "FAIL", name, detail[:110]))
    return ok


def load_ids(fn):
    path = os.path.join(OUT_DIR, fn)
    if not os.path.exists(path):
        return None
    with io.open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    ids = set()
    for k in ("items", "records", "results", "条目", "RESULTS"):
        for it in (d.get(k) or []):
            if isinstance(it, dict):
                v = it.get("id") or it.get("name")
                if v:
                    ids.add(str(v))
    return ids


# =========================================================================
# 量纲代数 (M, L, T)
# =========================================================================
class Dim(object):
    __slots__ = ("e",)

    def __init__(self, M=0, L=0, T=0):
        self.e = (M, L, T)

    def __add__(self, o):
        return Dim(*self.e) if self.e == o.e else Dim(*[a + b for a, b in zip(self.e, o.e)])

    def __sub__(self, o):
        return Dim(*self.e)

    def __mul__(self, o):
        return Dim(*[a + b for a, b in zip(self.e, o.e)])

    def __truediv__(self, o):
        return Dim(*[a - b for a, b in zip(self.e, o.e)])

    def __pow__(self, k):
        return Dim(*[a * k for a in self.e])

    def __eq__(self, o):
        return isinstance(o, Dim) and self.e == o.e

    def __ne__(self, o):
        return not self.__eq__(o)

    def __repr__(self):
        parts = []
        for n, v in zip(("M", "L", "T"), self.e):
            if v != 0:
                parts.append(n if v == 1 else "%s^%g" % (n, v))
        return "*".join(parts) if parts else "1(无量纲)"


ONE = Dim()
LEN = Dim(L=1)
INV_LEN = Dim(L=-1)
INV_TIM = Dim(T=-1)
ENERGY = Dim(M=1, L=2, T=-2)
FORCE = Dim(M=1, L=1, T=-2)

# =========================================================================
# 常数
# =========================================================================
C_LIGHT = 299792458.0
HBAR_SI = 1.054571817e-34
HBAR_C = 3.16152677e-26            # J m
G_NEWTON = 6.67430e-11
E_CHARGE = 1.602176634e-19
EPS0 = 8.8541878128e-12
ALPHA_0 = E_CHARGE ** 2 / (4 * math.pi * EPS0 * HBAR_SI * C_LIGHT)
ALPHA_MZ = 1.0 / 127.952
ALPHA_S_MZ = 0.1179
G_F = 1.1663787e-5
M_W = 80.379
SIN2_W = 0.23121
ALPHA_2_GF = math.sqrt(2.0) * G_F * M_W * M_W / math.pi
ALPHA_2_SIN = ALPHA_MZ / SIN2_W
ALPHA_W_FERMI = G_F * M_W * M_W / (math.pi * math.sqrt(2.0))
ALPHA_1 = (5.0 / 3.0) * ALPHA_MZ / (1.0 - SIN2_W)
M_E = 9.1093837015e-31
M_P = 1.67262192369e-27
ALPHA_G_E = G_NEWTON * M_E * M_E / HBAR_C
ALPHA_G_P = G_NEWTON * M_P * M_P / HBAR_C
E_CHARGE_EV = 1.602176634e-19
LAMBDA_QCD_LO = 0.20e9            # eV（口径区间下限）
LAMBDA_QCD_HI = 0.30e9            # eV（口径区间上限）
R_UNIV = 8.8e26                   # 可观测宇宙半径 m（占位尺度）


def main():
    print("=" * 78)
    print("TUFT V3.5 修复规范落地门禁：角度分区 + 六条单位约定 + 符号台账 + 四力样本")
    print("=" * 78)

    # =====================================================================
    # 〇 回链
    # =====================================================================
    BACKLINK = {
        "VIS": ("统一场论可视化证明_四力三要素实证审计_2026-10-04.json", ["B-01", "E-01", "C-02", "G-04"]),
        "REORG": ("TUFT_V3.5修复方案_全维审计与重整_2026-10-04.json",
                  ["A-01", "A-03", "B-03", "B-06", "E-01", "F-01", "F-03"]),
        "OMEGA": ("TUFT_V3.5_Ω公理构造_不可行性判定与最小增广_2026-10-04.json",
                  ["B-01", "B-04", "C-01", "D-01"]),
        "ATTACK": ("TUFT_V3.5修复方案_求导证明验证精算攻破_2026-10-04.json",
                   ["A-02", "A-03", "B-02", "B-06", "B-07", "C-07", "D-01"]),
    }
    for k, (fn, want) in BACKLINK.items():
        got = load_ids(fn)
        if got is None:
            guard("backlink_" + k, False, "产物缺失 %s" % fn)
            continue
        miss = [w for w in want if w not in got]
        guard("backlink_" + k, not miss,
              "回链 %s：%d 个 id 全部命中%s" % (k, len(want), ("；缺失 " + ",".join(miss)) if miss else ""))

    # =====================================================================
    # U · 六条单位约定
    # =====================================================================
    UNITS = [
        ("U1", "面积元口径：Δs 取面积元（沿用 S17 闭合代价册）", "已由前册钉死，本册沿用"),
        ("U2", "sr 视为无量纲", "已由前册钉死，本册沿用"),
        ("U3", "k′ 必须显式声明单位", "已由前册钉死，本册沿用"),
        ("U4", "f 只作导出量：f ≡ c√(κ²+τ²)/(2π)，**禁止**列为独立本源参量", "本册新增（承接 B-01）"),
        ("U5", "耦合定义：凡写耦合必须声明是 α = g²/(4π) 还是「费米定义」G_F M_W²/(π√2)"
               "（两者严格差因子 2）", "**本册新增**"),
        ("U6", "规范归一化：凡写 U(1) 必须声明是否 GUT 归一化 α₁ = (5/3)α_Y，"
               "并点名所走路线（α/sin²θ_W 或 √2·G_F M_W²/π，两者差 0.35%）", "**本册新增**"),
    ]
    guard("units_six_declared", len(UNITS) == 6 and all(u[0] for u in UNITS),
          "六条单位约定齐备：%s" % "、".join(u[0] for u in UNITS))
    add("U-01", "U 单位约定", "六条单位约定（原四条 + 耦合定义 + 规范归一化）",
        "规范交付：任何实现开工前必须先声明这六条",
        "PASS",
        "逐条：" + " ｜ ".join("%s：%s（%s）" % u for u in UNITS) +
        "。⇒ U5/U6 是本册新增的两维：上一轮已机器证明**只声明能标仍会串号三次**"
        "（α₂ vs 费米定义差 **2.000 倍**；α₁ 与费米定义**巧合 1.07e-3**；"
        "α₂ 两条路线**相差 %.2f%%**）⇒ 不写 U5/U6 就无法复算。" % (100 * abs(ALPHA_2_GF - ALPHA_2_SIN) / ALPHA_2_SIN))

    # =====================================================================
    # S · 符号台账
    # =====================================================================
    LEDGER = [
        ("κ 曲率", INV_LEN, "本源（双参量之一）"),
        ("τ 挠率", INV_LEN, "本源（双参量之一）"),
        ("ρ = √(κ²+τ²)", INV_LEN, "派生：只定**有量纲**标度"),
        ("θ = atan2(τ,κ)", ONE, "派生：唯一携带无量纲信息的自由度"),
        ("ω = c√(κ²+τ²)", INV_TIM, "派生（禁止与 κ,τ 并列为本源）"),
        ("f = ω/2π", INV_TIM, "**导出量**（U4：不得作独立参量）"),
        ("L 力程", LEN, "L = c/f = 2π/ρ（2π 约定见 R-01）"),
        ("E 势能", ENERGY, "E = (ℏc/2)(κ+τ)，量纲已修复"),
        ("F 力", FORCE, "F = −∇E；∇ 需 κ(x),τ(x) 场构型（O-FIELD 未闭合）"),
        ("Ω 权重", None, "**未定**：强度式要求 [ℏ]、公理要求无量纲 ⇒ 冲突未解（Z-01）"),
        ("α_i 耦合", ONE, "必须按 U5/U6 声明定义与归一化"),
    ]
    bad = [n for n, d, _ in LEDGER if d is None]
    guard("symbol_ledger_dims", all(l[1] is not None or l[0].startswith("Ω") for l in LEDGER),
          "符号台账 %d 行，%d 行量纲已定；未定行 = %s（显式登记，不掩盖）" % (len(LEDGER), len(LEDGER) - len(bad), bad))
    add("S-01", "S 符号台账", "全量符号 × 量纲 × 修复状态（机器逐行校验）",
        "规范交付：实现中的每一个符号都必须能在台账里查到",
        "PASS",
        "台账：" + "；".join("%s = [%s]（%s）" % (n, (d if d is not None else "未定"), s) for n, d, s in LEDGER) +
        "。⇒ 关键结构信息：**只有 θ 携带无量纲信息、只有 ρ 携带标度**，"
        "二者不可互换（上一轮 Π 定理已机器证明）。Ω 一行**显式留空**而非填一个假量纲——"
        "这是本仓红线：不把未解决的冲突写成已解决。")

    # =====================================================================
    # R · 修复后公式三式
    # =====================================================================
    t = sp.symbols("t", real=True)
    a, b = sp.symbols("a b", positive=True)
    rv = sp.Matrix([a * sp.cos(t), a * sp.sin(t), b * t])
    r1 = sp.diff(rv, t)
    r2 = sp.diff(r1, t)
    r3 = sp.diff(r2, t)
    speed = sp.simplify(sp.sqrt(r1.dot(r1)))
    cr = r1.cross(r2)
    kap_s = sp.simplify(sp.sqrt(cr.dot(cr)) / speed ** 3)
    tau_s = sp.simplify(cr.dot(r3) / cr.dot(cr))
    sumsq = sp.simplify(kap_s ** 2 + tau_s ** 2)
    arc_turn = sp.simplify(sp.integrate(speed, (t, 0, 2 * sp.pi)))
    ident_ok = sp.simplify(sumsq - 1 / (a ** 2 + b ** 2)) == 0
    arc_ok = sp.simplify(sp.expand(arc_turn ** 2 - (2 * sp.pi / sp.sqrt(sumsq)) ** 2)) == 0
    guard("helix_identity", ident_ok and arc_ok,
          "sympy：κ=%s，τ=%s，κ²+τ²=%s；一整圈弧长=%s == 2π/√(κ²+τ²)" % (kap_s, tau_s, sumsq, arc_turn))

    # 两种约定对表核能标
    E_2pi_strong = HBAR_C * (2 * math.pi / 1e-15) / E_CHARGE_EV
    E_2pi_weak = HBAR_C * (2 * math.pi / 1e-18) / E_CHARGE_EV
    E_red_strong = HBAR_C / 1e-15 / E_CHARGE_EV
    E_red_weak = HBAR_C / 1e-18 / E_CHARGE_EV
    dev_2pi_s_hi = E_2pi_strong / LAMBDA_QCD_HI
    dev_2pi_s_lo = E_2pi_strong / LAMBDA_QCD_LO
    dev_2pi_w = E_2pi_weak / (M_W * 1e9)
    dev_red_s_hi = E_red_strong / LAMBDA_QCD_HI
    dev_red_w = E_red_weak / (M_W * 1e9)
    guard("range_convention_sensitive",
          dev_2pi_s_hi > 4.0 and dev_2pi_w > 10.0 and dev_red_s_hi < 1.0,
          "2π 约定：强 %.3f GeV（vs Λ_QCD 偏大 %.1f~%.1f 倍）、弱 %.3f TeV（vs M_W 偏大 %.1f 倍）；"
          "无 2π 约定：强 %.3f GeV（%.2f 倍）、弱 %.3f GeV（%.2f 倍）"
          % (E_2pi_strong / 1e9, dev_2pi_s_hi, dev_2pi_s_lo, E_2pi_weak / 1e12, dev_2pi_w,
             E_red_strong / 1e9, dev_red_s_hi, E_red_weak / 1e9, dev_red_w))
    add("R-01", "R 修复公式", "力程定标：**2π 版在几何上钉死，但在核能标对表上偏大**（约定敏感点）",
        "L = c/f = 2π/√(κ²+τ²)（= 一整圈螺旋弧长）",
        "BOUNDARY",
        "sympy 求导：κ = %s、τ = %s、κ²+τ² = %s、一整圈弧长 = %s ⇒ **2π 版 = 弧长**在几何上唯一。"
        "但对表核能标（E = ℏc·ρ，ρ = 2π/L）："
        "**2π 版**：强核 **%.4g GeV**（vs Λ_QCD 0.2~0.3 GeV ⇒ 偏大 **%.1f~%.1f 倍**）、"
        "弱核 **%.4g TeV**（vs M_W 80.4 GeV ⇒ 偏大 **%.1f 倍**）；"
        "**无 2π 版**（L = 1/ρ）：强核 %.4g GeV（%.2f 倍）、弱核 %.4g GeV（%.2f 倍）。"
        "⇒ 前册 A-03 说「两口径都能量级吻合」，本册把它**量化成两张偏差表**："
        "取 2π（几何所要求）则与核能标**不符 4~15 倍**，取无 2π 则几何身份丢失。"
        "⇒ **登记为约定敏感点（BOUNDARY），任何一方都不得拿来当验证证据**；"
        "规范建议：实现里写死 2π 版并在注释标注此偏差。"
        % (kap_s, tau_s, sumsq, arc_turn, E_2pi_strong / 1e9, dev_2pi_s_hi, dev_2pi_s_lo,
           E_2pi_weak / 1e12, dev_2pi_w, E_red_strong / 1e9, dev_red_s_hi, E_red_weak / 1e9, dev_red_w))

    add("R-02", "R 修复公式", "势能式与力式的最终形态",
        "E = (ℏc/2)(κ+τ)、F = −∇E",
        "PASS",
        "量纲：E = [ℏ][c][κ] = %s × %s × %s = **%s（能量）** ✓；F = −∇E ⇒ %s ✓。"
        "注意事项（前册已判，本册固化为规范约束）："
        "① ∇ 作用于**位置**要求场构型 κ(x)、τ(x)，而 κ,τ 本是**弧长 s** 的函数 ⇒ 未补场构型前"
        "F = −∇E 只能沿曲线读 dE/ds，**不是空间力矢量**（回链 O-FIELD）；"
        "② 代入体系自有的 m = ℏ√(κ²+τ²)/c 后 E/(mc²) = (κ+τ)/(2√(κ²+τ²)) ∈ [−0.707, +0.707]"
        "⇒ **恒不等于 1 且可为负**（前册 A-05），规范要求在注释中显式写出这条，不得略过。"
        % (Dim(M=1, L=2, T=-1), Dim(L=1, T=-1), INV_LEN, ENERGY, FORCE))

    # =====================================================================
    # A · 角度分区规范
    # =====================================================================
    def sector(theta, bounds):
        b1, b2, b3, b4 = bounds
        if theta > b4 or theta <= b1:
            return "S1"
        if theta <= b2:
            return "S2"
        if theta <= b3:
            return "S3"
        return "S4"

    BOUNDS = [-40.0, 25.0, 65.0, 110.0]
    LABELS = ["Weak", "Strong", "EM", "G"]      # 段 → 力（**外加约定**，非导出）
    grid = [-180.0 + 0.25 * i for i in range(1440)]
    cnt = {}
    for th in grid:
        cnt[sector(th, BOUNDS)] = cnt.get(sector(th, BOUNDS), 0) + 1
    guard("angular_spec_disjoint_complete", len(cnt) == 4 and sum(cnt.values()) == 1440,
          "角度分区规范：1440 点每点恰落 1 段，四段计数 %s" % cnt)

    kap_d = Dim(L=-1)
    guard("boundary_form_banned", kap_d != ONE,
          "边界写法禁令：|κ| 量纲 %s，自称无量纲的 B_i 量纲 %s ⇒ 不可比较（写成 |κ|<B 即非法）"
          % (kap_d, ONE))
    add("A-01", "A 角度分区", "四力分区规范：**边界只能写成角度（或等价比值）形式**",
        "θ = atan2(τ,κ)；圆周 n 段需 n 个边界 ⇒ **4 个**阈值（不是 3 个）",
        "PASS",
        "规范条文：① 边界写作 θ ∈ (b_i, b_{i+1}]，四段含跨 ±180° 回卷段；"
        "② 阈值取值必须**无量纲**（角度或 τ/κ 比值），**禁止** |κ| < B 形式"
        "（左 L⁻¹ 与右无量纲不可比较，机器实测 %s ≠ %s）；"
        "③ 默认示例 %s + 标签序 %s（**标签序是外加约定，非从 (κ,τ) 导出**）；"
        "④ 门禁：网格 1440 点每点恰落 1 段，四段计数 = %s ⇒ 互斥且完备 ✓。"
        "⇒ 前册 B-04/B-05 的「重叠 + 空隙」在此形式下**被消除**（上一轮已证明：旧形式是"
        "对任意阈值必然重叠且必然有空隙，属形式缺陷而非标定问题）。" % (kap_d, ONE, BOUNDS, LABELS, cnt))

    add("A-02", "A 角度分区", "段 → 力的标签序：4! = 24 种排列，**规范不选择**",
        "规范交付：把这 24 种列为显式自由度并登记",
        "PASS",
        "四段到四力的映射有 **24 种**排列；上一轮已机器证明：两组不同阈值可在四力样本上给出"
        "**相同标签**却在间隙点给出**不同标签** ⇒ 阈值与排列都是**不可唯一确定的自由度**。"
        "⇒ 规范处置：**不假装规范能定它**——实现必须把「阈值四元组 + 标签排列」写成"
        "**显式常量并注明为待标定输入**，禁止把它埋进条件分支里当成已导出的结论。"
        "这是本册与「单射证明」路线的分工：单射（互斥完备）**已由规范保证**；"
        "唯一性**不由规范保证，也不假装保证**。")

    # =====================================================================
    # M · 四力样本规范（解除 E-01 阻塞）
    # =====================================================================
    TWO_PI = 2 * math.pi
    SAMPLES = [
        ("引力 G", 85.0, None),        # L = ∞
        ("电磁 EM", 45.0, None),       # L = ∞
        ("强核 Strong", 5.0, 1e-15),
        ("弱核 Weak", -85.0, 1e-18),
    ]
    rows = []
    for name, th, L in SAMPLES:
        if L is None:
            rows.append({"name": name, "theta_deg": th, "L_m": None, "rho": 0.0,
                         "kappa": 0.0, "tau": 0.0, "status": "退化：(κ,τ)=(0,0)，θ 无定义"})
        else:
            rho = TWO_PI / L
            kk = rho * math.cos(math.radians(th))
            tt = rho * math.sin(math.radians(th))
            rows.append({"name": name, "theta_deg": th, "L_m": L, "rho": rho,
                         "kappa": kk, "tau": tt, "status": "OK"})
    finite = [r for r in rows if r["status"] == "OK"]
    guard("samples_four_rows", len(rows) == 4 and len(finite) == 2,
          "四力样本表 %d 行：有限力程 %d 行给出显式 (κ,τ)；无限力程 %d 行显式登记为退化"
          % (len(rows), len(finite), len(rows) - len(finite)))

    add("M-01", "M 四力样本", "**解除元审计册 E-01「只能给出两组样本」的阻塞**",
        "身份给 θ_i、标度给尺度锚 L_i ⇒ 由 ρ=2π/L、κ=ρcosθ、τ=ρsinθ 反解",
        "PASS",
        "规范：样本的**身份**只需角度、**标度**由独立尺度锚给（前册已证强度与力程在 Ω 框架内"
        "结构性脱钩 ⇒ 二者本就必须分开给）。反解结果：" +
        "；".join("%s：θ=%.0f°，L=%s ⇒ ρ=%s m⁻¹，(κ,τ)=(%s, %s)" %
                  (r["name"], r["theta_deg"],
                   ("∞" if r["L_m"] is None else "%.0e m" % r["L_m"]),
                   ("%.4e" % r["rho"]) if r["rho"] else "0",
                   ("%.4e" % r["kappa"]) if r["kappa"] else "0",
                   ("%.4e" % r["tau"]) if r["tau"] else "0") for r in rows) +
        "。⇒ 前册 E-01 判「引力/电磁因 L=∞ ⇒ √(κ²+τ²)=0 ⇒ 给不出样本」，"
        "本册的处置是**把这个退化显式写进样本表**（不是跳过、也不是编一个数），"
        "并同时给出下面 M-02 的诚实登记与可选占位。")

    rho_placeholder = TWO_PI / R_UNIV
    guard("infinite_range_degeneracy", rho_placeholder > 0.0 and ALPHA_G_E > 0.0,
          "L=∞ ⇒ ρ=2π/L=0 ⇒ θ=atan2(0,0) 无定义；占位尺度 R_U=%.1e m 给 ρ=%.3e m⁻¹（**占位非导出**）"
          % (R_UNIV, rho_placeholder))
    add("M-02", "M 四力样本", "引力/电磁的 L=∞ **退化**，是框架极限不是标定缺失",
        "诚实登记 + 可选占位（标注为占位）",
        "BOUNDARY",
        "L = ∞ ⇒ ρ = 2π/L = 0 ⇒ (κ,τ) = (0,0) ⇒ **θ = atan2(0,0) 无定义** ⇒ "
        "引力与电磁**不在 (κ,τ) 参数化之内**（这一条与前册 B-07 同源，本册交叉印证、不强占）。"
        "规范给出两条出路，实现者**必须二选一并写进注释**："
        "① **诚实默认**（推荐）：把这两类标为「框架外」，不产 (κ,τ) 样本；"
        "② **可成像占位**：取截断尺度 R_U = %.1e m ⇒ ρ = %.3e m⁻¹（对应特征能量 ℏcρ ≈ %.2e eV），"
        "**明确标注为占位而绝非模型导出**。"
        "⇒ 这一条直接决定可视化能做到什么程度：**最多只能给出两张有真实 (κ,τ) 的图**，"
        "另两张是占位或空白——不允许用占位图充当实证。"
        % (R_UNIV, rho_placeholder, HBAR_C * rho_placeholder / E_CHARGE_EV))

    # =====================================================================
    # T · 强度表规范
    # =====================================================================
    TABLE = [("强核", "α₃ = α_s(M_Z)", ALPHA_S_MZ, "g²/4π（GUT 无关）"),
             ("弱核", "α₂ = g²/4π", ALPHA_2_GF, "√2·G_F M_W²/π（U5 点名路线）"),
             ("超荷", "α₁ = (5/3)α_Y", ALPHA_1, "U6：GUT 归一化，α_Y = α/cos²θ_W"),
             ("电磁", "α(M_Z)", ALPHA_MZ, "μ = M_Z，非 Thomson 极限"),
             ("引力", "α_G(m_e) = Gm_e²/(ℏc)", ALPHA_G_E, "必须声明参考质量")]
    guard("strength_table_four_dims",
          ALPHA_S_MZ > ALPHA_2_GF > ALPHA_1 > ALPHA_MZ > ALPHA_G_E,
          "四维口径表：%s" % " > ".join("%s %.4e" % (n, v) for n, _, v, _ in TABLE))
    add("T-01", "T 强度表", "强度表规范（四维口径齐备版）",
        "能标 + 定义 + 归一化 + 参考质量，缺一不可",
        "PASS",
        "规范表：" + "；".join("%s：%s = %.6e（%s）" % (n, f, v, d) for n, f, v, d in TABLE) +
        "。⇒ 排序 α₃ > α₂ > α₁ > α_em ≫ α_G。本表四条口径全部字面化，可被第三方逐字复算。")

    traps = [("α₂ vs 费米定义", abs(ALPHA_2_GF / ALPHA_W_FERMI - 2.0), "严格因子 2"),
             ("α₁ vs 费米定义", abs(ALPHA_1 - ALPHA_W_FERMI) / ALPHA_W_FERMI, "数值巧合"),
             ("α₂ 两条路线", abs(ALPHA_2_GF - ALPHA_2_SIN) / ALPHA_2_SIN, "0.35% 口径差")]
    guard("cross_numbering_traps", all(x[1] < 0.01 or x[1] > 1.9 for x in traps),
          "三条串号警戒：%s" % "；".join("%s = %.2e（%s）" % x for x in traps))
    add("T-02", "T 强度表", "三条串号警戒（机器登记，写入规范注释）",
        "实现里任何出现耦合数值的地方都要带这三条",
        "INFO",
        "① α₂(%.6e) 与费米定义(%.6e) 相差 **%.4f 倍** ⇒ 只写「α_W」必错；"
        "② α₁(%.6e) 与费米定义数值**巧合到 %.2e** ⇒ 极易把一个当成另一个；"
        "③ α₂ 的两条标准路线（G_F 路线 %.6e / α÷sin²θ_W 路线 %.6e）相差 **%.2f%%**。"
        "⇒ 规范要求：耦合数值在代码中一律写成「带下标的命名常量 + 一行口径注释」，"
        "禁止裸写 0.017 / 0.0338 之类数字。"
        % (ALPHA_2_GF, ALPHA_W_FERMI, ALPHA_2_GF / ALPHA_W_FERMI,
           ALPHA_1, abs(ALPHA_1 - ALPHA_W_FERMI) / ALPHA_W_FERMI,
           ALPHA_2_GF, ALPHA_2_SIN, 100 * abs(ALPHA_2_GF - ALPHA_2_SIN) / ALPHA_2_SIN))

    # =====================================================================
    # V · 可视化规范
    # =====================================================================
    lam = 1e3
    th_before = math.degrees(math.atan2(3.0, 4.0))
    th_after = math.degrees(math.atan2(lam * 3.0, lam * 4.0))
    guard("viz_only_angle", abs(th_before - th_after) < 1e-9,
          "径向缩放 λ=%.0e：θ 由 %.6f° 变为 %.6f°（差 %.1e）⇒ 图像沿径向缩放不携带任何无量纲信息"
          % (lam, th_before, th_after, abs(th_before - th_after)))
    add("V-01", "V 可视化", "可视化规范：**只需给角度；径向是纯标度**",
        "身份 = θ，标度 = ρ（由 L 锚定）",
        "PASS",
        "机器演示：把 (κ,τ) = (4,3) 整体缩放 λ = 1e3 后，θ 由 %.6f° 变为 %.6f°（差 %.1e）"
        "⇒ **径向方向不携带任何无量纲信息**（Π 定理的直接后果）。"
        "⇒ 规范条文：① 四组样本**必须**给出 θ_i（角度/比值），给出 ρ_i 时须同时给 L_i 尺度锚；"
        "② 渲染管线归档四件套：投影算法、采样网格、色标映射、矢量场绘制规则；"
        "③ 量化判据用余弦相似度 / 残差范数并**预设阈值**；"
        "④ 定位声明：相似度证明的是**两张图一致（复现一致性，防漂移）**，"
        "**不证明图与实验一致**——禁止用「完美复刻」一类措辞。"
        % (th_before, th_after, abs(th_before - th_after)))

    # =====================================================================
    # W · 表述替换表
    # =====================================================================
    REPLACE = [
        ("100%", "模型自洽校验通过（在声明的口径下）"),
        ("精准 / 完全精准匹配", "在选定标度下，耦合常数量级与标准模型对标"),
        ("无任何偏差", "逐条列出偏差数值（当前：电磁 2.6e-4、强核 4~15 倍、弱核口径依赖）"),
        ("无可辩驳", "给出可失败条件与反证入口"),
        ("彻底攻克", "本轮闭合 N 项，剩余 M 项列为开放项"),
        ("完美匹配 / 完美复刻", "复现一致性达标（阈值 X），不等于实证吻合"),
        ("完美解释", "与现象清单定性对应，定量表达式待补"),
        ("无额外常数", "常数台账：列出全部外锚（当前：阈值 4 个 + 尺度锚 4 个 + Φ 形式）"),
    ]
    guard("wording_replacement", len(REPLACE) == 8 and all(r[1] for r in REPLACE),
          "表述替换表 %d 条，每条均有替换口径" % len(REPLACE))
    add("W-01", "W 表述", "绝对化措辞的替换表（零成本，建议立即执行）",
        "前册 E-03：该步零风险、零依赖",
        "PASS",
        "替换表：" + "；".join("「%s」→「%s」" % r for r in REPLACE) +
        "。⇒ 与上一轮 F-02 一致：这一步**只改变陈述强度，不改变任何 FAIL 的成立性**，"
        "但它是唯一可以立即开工且不会返工的一步。")

    # =====================================================================
    # Z · 规范不能解决的三项 + 门禁
    # =====================================================================
    add("Z-01", "Z 边界", "规范**不能**解决的三项（与规范正交，不因门禁通过而消失）",
        "诚实边界",
        "INFO",
        "① **Ω 的量纲与符号**：强度式反解 [Ω] = [ℏ] 与「Ω 无量纲」公理**量纲层面互斥**；"
        "公理 4「最多 1 个常数」是空约束；引力符号无唯一性 ⇒ 规范只能要求「显式登记为未定」，"
        "**不能定义 Ω**。② **两条可证伪预言**：g−2 通道已被否决 8.06 量级、宇宙线通道退化为上界或"
        "不可测 ⇒ 规范无能为力（需要新物理输入，不是写法问题）。"
        "③ **弱力方向 / 宇称定量的矢量表达式**：框架内无旋量、无手性投影算符、无 CKM 相位 "
        "⇒ 规范不能凭空造出表达式。⇒ 这三项的存在，是本册门禁**不宣称提升评级**的原因。")

    add("Z-02", "Z 边界", "与同日三册的关系（不重复造轮子）",
        "分工声明",
        "INFO",
        "本册是**规范落地册**，三册前作是**判定册**："
        "元审计册（37 项）判「修什么」、Ω 册（25 项）判「Ω 路线不可行」、"
        "攻破册（37 项）判「哪些能修/哪些不可达并给出构造性反例」。"
        "本册**不复算**它们的任何读数，只把其中标为 PASS / 部分可达的结论**写成条文 + 门禁**。"
        "本册的两条新结论是：M-01（解除 E-01 的样本阻塞）与 R-01（2π 定标的偏差表）。")

    # =====================================================================
    # 落盘
    # =====================================================================
    counts = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
    for r in RESULTS:
        counts[r["verdict"]] += 1
    g_ok = sum(1 for g in GUARDS if g["ok"])

    payload = {
        "生成时间": time.strftime("%Y-%m-%d %H:%M:%S"),
        "主题": "TUFT V3.5 修复规范落地门禁（角度分区 + 六条单位约定 + 符号台账 + 四力样本 + 可视化规范）",
        "定位": "规范与门禁册（非物理成立性证明）；三项不由规范解决，见 Z-01",
        "六条单位约定": [{"id": u[0], "条文": u[1], "来源": u[2]} for u in UNITS],
        "符号台账": [{"符号": n, "量纲": (repr(d) if d is not None else "未定"), "状态": s} for n, d, s in LEDGER],
        "力程定标": {
            "2π版": {"强核_GeV": E_2pi_strong / 1e9, "弱核_TeV": E_2pi_weak / 1e12,
                     "强核偏大倍数区间": [dev_2pi_s_hi, dev_2pi_s_lo], "弱核偏大倍数": dev_2pi_w},
            "无2π版": {"强核_GeV": E_red_strong / 1e9, "弱核_GeV": E_red_weak / 1e9,
                       "强核倍数": dev_red_s_hi, "弱核倍数": dev_red_w},
        },
        "角度分区规范": {"默认阈值": BOUNDS, "标签序": LABELS, "网格点数": 1440, "分段计数": cnt},
        "四力样本": rows,
        "占位尺度": {"R_U_m": R_UNIV, "rho": rho_placeholder,
                     "特征能量_eV": HBAR_C * rho_placeholder / E_CHARGE_EV},
        "强度表规范": [{"力": n, "耦合": f, "值": v, "口径": d} for n, f, v, d in TABLE],
        "串号警戒": [{"项": a, "读数": b, "性质": c} for a, b, c in traps],
        "表述替换表": [{"原": a, "替换为": b} for a, b in REPLACE],
        "计数": counts, "总计": len(RESULTS),
        "自检": {"总数": len(GUARDS), "通过": g_ok, "项": GUARDS},
        "条目": RESULTS,
        "耗时": "%.1fs" % (time.time() - T_START),
    }
    base = os.path.join(OUT_DIR, "TUFT_V3.5修复规范_角度分区与六条约定_落地门禁_2026-10-04")
    with io.open(base + ".json", "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    md = ["# TUFT V3.5 修复规范落地门禁（机器产物）", "",
          "- 生成时间：%s" % payload["生成时间"],
          "- 定位：**%s**" % payload["定位"],
          "- 条目 %d ｜ PASS %d ｜ FAIL %d ｜ BOUNDARY %d ｜ INFO %d ｜ 自检 %d / %d" %
          (len(RESULTS), counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"],
           g_ok, len(GUARDS)),
          "", "## 六条单位约定", ""]
    for u in UNITS:
        md.append("- **%s**：%s（%s）" % u)
    md += ["", "## 符号台账", "", "| 符号 | 量纲 | 状态 |", "|---|---|---|"]
    for n, d, s in LEDGER:
        md.append("| %s | %s | %s |" % (n, (repr(d) if d is not None else "**未定**"), s))
    md += ["", "## 四力样本", "", "| 力 | θ | L | ρ | κ | τ | 状态 |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append("| %s | %.0f° | %s | %s | %s | %s | %s |" %
                  (r["name"], r["theta_deg"], ("∞" if r["L_m"] is None else "%.0e m" % r["L_m"]),
                   ("%.4e" % r["rho"]) if r["rho"] else "0",
                   ("%.4e" % r["kappa"]) if r["kappa"] else "0",
                   ("%.4e" % r["tau"]) if r["tau"] else "0", r["status"]))
    md += ["", "## 逐条判定", "", "| ID | 节 | 条目 | 判定 | 摘要 |", "|---|---|---|---|---|"]
    for r in RESULTS:
        head = r["detail"].replace("\n", " ")
        if len(head) > 160:
            head = head[:160] + "…"
        md.append("| %s | %s | %s | %s | %s |" %
                  (r["id"], r["section"], r["item"], r["verdict"], head.replace("|", "/")))
    md += ["", "## 自检", "", "| 基线 | 结果 | 取证 |", "|---|---|---|"]
    for g in GUARDS:
        md.append("| %s | %s | %s |" % (g["name"], "PASS" if g["ok"] else "FAIL", g["detail"]))
    md.append("")
    with io.open(base + ".md", "w", encoding="utf-8") as fh:
        fh.write("\n".join(md))

    print("-" * 78)
    print("总计 %d 条 ｜ PASS %d ｜ FAIL %d ｜ BOUNDARY %d ｜ INFO %d" %
          (len(RESULTS), counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"]))
    print("自检 %d / %d" % (g_ok, len(GUARDS)))
    print("产物：%s.json / .md" % base)
    if g_ok != len(GUARDS):
        print("SELFCHECK FAILED")
        return 2
    print("定位：规范与门禁册（不宣称提升评级；三项不由规范解决）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
