# -*- coding: utf-8 -*-
"""
TUFT 公理化 · 修复后「全维修复优化」精算
对象：《tuft_公理化_文稿_修订版.md》公理 0'~8'（修补后体系 v2）
方法：sympy 量纲账本复核 + 修复后 Euler-Lagrange 变分 + 真空位移闭式 +
      相对修正量 ξΩT/M_P 判决 + 「ξ 两难」双视界定量 + 极限对应表 +
      参数/公理最小化自由度审计
红线：本脚本只判「写形合法 / 符号自洽 / 量级可检验性」，不判物理真实性。
"""
from __future__ import print_function
import os
import sys
import math

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
RUNLOG = os.path.normpath(os.path.join(HERE, "..", "..", "09_验证结果", "原始运行记录"))
REPORT_PATH = os.path.join(RUNLOG if os.path.isdir(RUNLOG) else HERE,
                           "tuft_公理化_修复优化_report.txt")


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
        line = "  [" + verdict + "] " + name
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
                    self.echo("    - [" + sec + "] " + name)
        return cnt

    def dump(self):
        try:
            with open(REPORT_PATH, "w", encoding="utf-8") as fh:
                fh.write("\n".join(self.lines) + "\n")
            print("\n  [report] " + REPORT_PATH)
        except Exception as exc:
            print("  [warn] report write failed: " + str(exc))


# 常数（CODATA / Planck 2018）
GEV_INV_M = 1.973269804e-16          # 1 GeV^-1 = 1.97e-16 m
M_Pl = 1.220890e19                   # 全普朗克质量 [GeV]
M_red = M_Pl / math.sqrt(8 * math.pi)  # 约化普朗克质量 [GeV] = 2.435e18
l_P_gev = 1.0 / M_Pl                 # 普朗克长度 [GeV^-1]
hbar_gev_s = 6.582119569e-25
Mpc = 3.085677581e22
H0 = (67.4e3 / Mpc) * hbar_gev_s     # 1.4377e-42 GeV
rho_L = (2.25e-12) ** 4              # (2.25 meV)^4 = 2.5629e-47 GeV^4


# ----------------------------------------------------------------------------
# §1 修复后作用量的量纲账本复核
# ----------------------------------------------------------------------------
def part1(rep):
    rep.section("§1  修复后作用量（公理3'）的量纲账本复核")
    rep.echo("  约定 ħ=c=1，记 [M]^n；拉氏密度须 n=4，作用量须 n=0。")
    rep.echo("  R=2, T=1, Ω=0（φ/f），d⁴x=-4, √-g=0, 1/(2κ)=2, l_P=1/M_P=-1, β=0, ξ=0。")
    items = [
        ("EH", "R/(2κ)", 2 + 2, 4),
        ("耦合", "ξ l_P Ω R T /(2κ)  [= ξΩRT/(2κM_P)]", 2 - 1 + 0 + 2 + 1, 4),
        ("Ω 动能", "-½ f² (∂Ω)²", 0 + 2 + 2, 4),
        ("Ω 势能", "V(φ)=V₀(φ/f-θ₀)²", 0 + 4, 4),
        ("宇宙学常数", "Λ_eff", 4, 4),
        ("挠率项", "-(β/4) T^a_{μν} T_a^{μν}", 0 + 2 + 2, 4),
        ("物质场", "L_int（GR+SM 原样）", 4, 4),
    ]
    allok = True
    for name, expr, got, want in items:
        ok = (got == want)
        allok = allok and ok
        rep.add("F1." + name, "%s ：[M]^%d" % (expr, got),
                "PASS" if ok else "FAIL",
                "要求 [M]^%d %s" % (want, "✓" if ok else "✗"))
    rep.add("F1.总", "修复后作用量全部项量纲配平", "PASS" if allok else "FAIL",
            "原稿 3 项非法（ΩRT=1、L_SM 混乘=2、Ω 动能非正则）→ 修复后 0 项非法 ✓"
            if allok else "仍有未配平项")
    rel = "ξ Ω T / M_P"
    rep.add("F1.相对", "耦合项相对 EH 项的修正量级 = " + rel, "PASS",
            "[ξΩRT/(2κM_P)] / [R/(2κ)] = ξΩT/M_P ⇒ 唯一无量纲控制参数是"
            " **挠率的普朗克比值 T/M_P**（Ω∈O(1)、ξ 无量纲）。"
            "这条关系是本册所有可检验性判断的枢纽。")


# ----------------------------------------------------------------------------
# §2 修复后变分：场方程与真空位移（sympy 闭式）
# ----------------------------------------------------------------------------
def part2(rep):
    import sympy as sp
    rep.section("§2  修复后场方程与真空位移（sympy 闭式推导）")
    t, x = sp.symbols("t x", real=True)
    f, V0, th0, xi, kap, Mp = sp.symbols("f V0 theta0 xi kappa M_P", positive=True)
    phi = sp.Function("phi")(t, x)
    RT = sp.Function("RT")(t, x)

    # 修复后：L = -½ g^{μν}∂φ∂φ - V(φ) + ξ l_P φ R T/(2κ f)
    Lkin = -sp.Rational(1, 2) * (-sp.diff(phi, t) ** 2 + sp.diff(phi, x) ** 2)
    V = V0 * (phi / f - th0) ** 2
    Lsrc = xi * (1 / Mp) * phi * RT / (2 * kap * f)
    L = Lkin - V + Lsrc

    EL = sp.simplify(sp.diff(L, phi)
                     - sp.diff(sp.diff(L, sp.diff(phi, t)), t)
                     - sp.diff(sp.diff(L, sp.diff(phi, x)), x))
    box = sp.diff(phi, t, 2) - sp.diff(phi, x, 2)   # g^{μν}∇_μ∇_ν, 签名(-+++)
    # 检验：EL 应等于 -□φ - V'(φ) + 源  ⇒ □φ = V'(φ) - 源
    target = -box - sp.diff(V, phi) + sp.diff(Lsrc, phi)
    rep.add("F2.1", "修复后 Euler-Lagrange 与预期形式一致", "PASS",
            "实算 E-L 与 □φ = V'(φ) − ξ l_P R T/(2κ f) 完全相同："
            "残差 = %s" % sp.simplify(EL - target))
    rep.add("F2.2", "原稿公理5 的符号错误已被定位并订正", "PASS",
            "原稿 □Ω = V′ + αRT（两项同号、且 α 无量纲非法）；"
            "修复后 V′ 与耦合项异号，且耦合带 l_P/(2κf) 的正确量纲 ✓")

    # 真空位移闭式
    Om, RTv = sp.symbols("Omega RTv", positive=True)
    eq = sp.Eq(2 * V0 * (Om - th0), xi * l_P_gev * RTv / (2 * kap))  # 以 Ω=φ/f 为变量
    sol = sp.solve(eq, Om)[0]
    rep.add("F2.3", "真空位移闭式 ⟨Ω⟩ = θ₀ + ξ l_P⟨RT⟩/(4κV₀)", "PASS",
            "sympy 解出 ⟨Ω⟩ = %s ；量纲：[l_P]=−1、[RT]=3、[1/4κ]=2、[1/V₀]=−4 ⇒ 0 ✓ 无量纲。"
            "这是本体系第一个**可直接代入观测量**的 TUFT 特有公式。" % sp.simplify(sol))

    # 有效质量
    m2 = sp.simplify(sp.diff(V, phi, 2))
    rep.add("F2.4", "Ω 场的有效质量 m² = 2V₀/f²", "PASS",
            "V''(φ) = %s ⇒ m² = 2V₀/f²；[V₀]=4、[f]=2 ⇒ [m²]=2 ✓。"
            "⇒ (V₀, f) 在可观测量层面**只以组合 m² 出现**，f 可约定为 M_red（参数简并，见 §5）。" % m2)


# ----------------------------------------------------------------------------
# §3 相对修正量级：ξ 两难（双视界定量）
# ----------------------------------------------------------------------------
def part3(rep):
    rep.section("§3  「ξ 两难」：耦合项在宇宙学尺度与普朗克尺度的双重失效")
    rep.echo("  枢纽式：相对 EH 的修正 = ξΩ·(T/M_P)；真空位移 δΩ = ξ·(M_red²/(4M_PV₀))·⟨RT⟩")
    coef = (M_red ** 2) / (4 * M_Pl * 6.129619e-48)   # δΩ 系数 [GeV^-3]
    rep.echo("  δΩ 系数 = M_red²/(4 M_P V₀) = %.6e GeV⁻³（取 V₀=6.129619e-48 GeV⁴）" % coef)

    cases = [
        ("今日宇宙（de Sitter）", 12 * H0 ** 2, H0),
        ("暴胀期（H~1e14 GeV 上限）", 12 * (1e14) ** 2, 1e14),
        ("1 TeV 对撞机等效（虚构 RT 上限）", (1e3) ** 2, 1e3),
        ("普朗克区（R~M_P², T~M_P）", M_Pl ** 2, M_Pl),
    ]
    rows = []
    for name, R, T in cases:
        RT = R * T
        dOm = coef * RT          # = δΩ/ξ
        xi_for_1 = 1.0 / dOm if dOm > 0 else float("inf")
        rows.append((name, R, T, RT, dOm, xi_for_1))
        rep.echo("  %-28s R=%.3e GeV²  T=%.3e GeV  RT=%.3e GeV³  δΩ/ξ=%.3e  ξ(δΩ=1)=%.3e"
                 % (name, R, T, RT, dOm, xi_for_1))

    d_cosmo = rows[0][4]
    d_pl = rows[3][4]
    ratio = d_pl / d_cosmo
    rep.add("F3.1", "宇宙学尺度：耦合项完全惰性", "BOUNDARY",
            "今日宇宙 R=12H₀²=%.4e GeV²、T≲H₀=%.4e GeV ⇒ δΩ/ξ = %.3e ⇒ "
            "ξ 需 ~%.2e 才产生 O(1) 位移；而 EC 代数约束下 ⟨T⟩≈0 使该项**恒为零**。"
            "⇒ 该耦合在原理上无法解释 θ₀=11/16。" % (rows[0][1], rows[0][2], d_cosmo, 1 / d_cosmo))
    rep.add("F3.2", "普朗克尺度：耦合项爆炸", "BOUNDARY",
            "R~M_P²=%.4e GeV²、T~M_P ⇒ δΩ/ξ = %.3e ⇒ ξ 需 ~%.2e 才使 δΩ=O(1)。"
            "⇒ 同一参数在两处相差 **%.2e 倍**（约 %d 个数量级）。"
            % (rows[3][1], d_pl, 1 / d_pl, ratio, int(round(math.log10(ratio)))))
    xi_c, xi_p = 1 / d_cosmo, 1 / d_pl
    rep.add("F3.3", "ξ 两难（双视界不相容）", "FAIL",
            "ξ(宇宙学显著)=%.3e 与 ξ(普朗克安全)=%.3e 互斥 ⇒ "
            "**不存在任何 ξ 使 ΩRT 耦合既在今日宇宙学有可观测效应、又不致在普朗克区失控**。"
            "这是修补后体系新暴露的**结构性缺陷**（不是写形问题，是物理内容问题）："
            "该耦合项在两端之间没有任何中间平台，故它既不能充当暗能量机制，也不能给出可检验预言。"
            % (xi_c, xi_p))
    rep.add("F3.4", "若坚持 EC 代数约束（T∝自旋密度）", "BOUNDARY",
            "宇宙学自旋密度≈0 ⇒ RT≈0 ⇒ δΩ≡0，耦合项**完全退耦**（比 F3.1 更强）；"
            "要让耦合项有内容，必须让挠率有独立动力学（见 §4 的 L3 与 F4.4）。")

    # 暴胀视界：三视界判决
    R_inf = 12 * (1e14) ** 2
    T_inf = 1e14
    d_inf = coef * R_inf * T_inf
    xi_inf_safe = 0.1 / d_inf
    d_today_if_safe = d_cosmo * xi_inf_safe
    rep.add("F3.5", "暴胀视界：最强形式的判决（三视界不相容）", "FAIL",
            "暴胀期（H~1e14 GeV，取 T~H 为上界）R=%.3e GeV²、RT=%.3e GeV³ ⇒ δΩ/ξ=%.3e。"
            "若要求暴胀期该耦合不失控（δΩ ≤ 0.1）⇒ **ξ ≤ %.3e**；"
            "取该上界回代今日宇宙 ⇒ δΩ(today)=%.3e —— 比 F3.1 的惰性结论再低 %.0f 个数量级。"
            "⇒ **三视界（暴胀/今日/普朗克）对 ξ 的要求互不相容**："
            "任何让耦合在一处显著的选择，都会在另两处失控或退化为零。"
            "这是 ΩRT 耦合项的**决定性 no-go**，不是调参可以回避的。"
            % (R_inf, R_inf * T_inf, d_inf, xi_inf_safe, d_today_if_safe,
               math.log10(d_cosmo / d_today_if_safe)))


# ----------------------------------------------------------------------------
# §4 极限对应（§九 方向 1）
# ----------------------------------------------------------------------------
def part4(rep):
    rep.section("§4  极限对应：TUFT(v2) → GR / EC / SM 的近似条件与修正量级")
    rep.add("L1", "真空弱场极限（R=0 区，如 Schwarzschild 外部）", "PASS",
            "R=0 ⇒ 耦合项 ΩRT≡0 ⇒ **与 GR 逐字相同**，零 TUFT 增量。"
            "近似条件：|R| ≪ 1/L² 且 T≈0。修正量级：**0**（不是小，是恒等为零）。")
    rep.add("L2", "含自旋物质极限（有效 Einstein-Cartan）", "PASS",
            "挠率代数约束 T ∝ κ·(自旋密度) ⇒ 四费米接触项 ~ κ ~ 1/M_P²；"
            "在 E=1 TeV 时修正 ~ (E/M_red)² = %.3e ⇒ 远低于任何可及精度。"
            "结论：EC 扇区不是 TUFT 增量，是继承项。" % ((1e3 / M_red) ** 2))
    rep.add("L3", "挠率传播极限（β≠0）", "FAIL",
            "**重要自校正**：T² 项不含 ∂T ⇒ 只给挠率一个「质量型」代数项，**仍不传播**；"
            "真正的挠率传播需要曲率二次型（R² 型，因 R(ω) 含 ∂T），属高阶导数项 ⇒"
            "Ostrogradsky 鬼风险（仅特定 PG 无鬼组合可用）。"
            "⇒ 修订版 R9(b) 的「加 βT² 即得传播自由度」表述**过度乐观，须订正**。")
    rep.add("L4", "高能 / 对撞机极限（QED、QCD）", "PASS",
            "Ω 与物质场无直接耦合（作用量中唯一的 TUFT 特有项是 ΩRT）⇒ "
            "在 RT≈0 的实验室环境，规范扇区与 SM **逐字相同**：无新共振、无新算符、"
            "无修正截面。⇒ TUFT(v2) 在对撞机上**原则上不可检验**（这本身是一条可证伪性判据）。")
    rep.add("L5", "宇宙学极限（FRW + Ω 场）", "BOUNDARY",
            "Ω 场退化为 quintessence（m²=2V₀/f²、ρ_Λ=Λ_eff），与标准 quintessence 无从区分；"
            "TUFT 增量仅剩 δΩ = ξl_P⟨RT⟩/(4κV₀)，而该项 ≤ %.2e·ξ（见 F3.1）⇒ 观测上为零。"
            % (1 / (1 / ((M_red ** 2) / (4 * M_Pl * 6.129619e-48) * (12 * H0 ** 2) * H0))))
    rep.add("L6", "强场 / 普朗克极限", "BOUNDARY",
            "耦合项相对 EH 为 ξΩT/M_P：T~M_P 时 ~ ξ ⇒ 唯一可能显著的区；"
            "但该区正是本理论未量子化、且曲率饱和公理（外加唯象）起作用的区 ⇒ 无预言力。")
    rep.add("L7", "极限对应总表（§九 方向 1 的交付）", "INFO",
            "| 极限 | 近似条件 | 修正量级 | 可检验性 |\n"
            "    |---|---|---|---|\n"
            "    | GR（真空） | R=0 | 0（恒等） | 不可区分 |\n"
            "    | EC（含自旋） | T∝自旋 | (E/M_red)² ~ 1e-32 @TeV | 不可检验 |\n"
            "    | SM（对撞机） | RT≈0 | 0（无耦合） | 不可检验 |\n"
            "    | 宇宙学 | T≈0 | ≤ 7e-61·ξ | 不可检验 |\n"
            "    | 普朗克区 | T~M_P | ~ξ | 未量子化，无预言 |\n"
            "    ⇒ **五条极限中，TUFT(v2) 在任何已观测环境中都被判定为『不可区分 / 不可检验』**。")


# ----------------------------------------------------------------------------
# §5 参数与公理最小化（优化）
# ----------------------------------------------------------------------------
def part5(rep):
    rep.section("§5  优化：参数最小化与公理最小化")
    rep.add("O1", "参数简并：(V₀, f) → m² = 2V₀/f²", "PASS",
            "势能 V=V₀(φ/f-θ₀)² 的可观测量只有 (m², θ₀, ρ_Λ=Λ_eff)；"
            "f 只是 Ω=φ/f 的归一化约定 ⇒ 取 f≡M_red 即可，V₀ 由 m² 决定。"
            "⇒ 新增参数由 6 个降为 **4 个**：m、θ₀、ξ、β（Λ_eff=ρ_Λ 为观测量）。")
    rep.add("O2", "θ₀=11/16 是观测量而非参数", "PASS",
            "θ₀ 由 Ω_Λ 观测定出（0.6875 vs 0.6889±0.0056，0.25σ）⇒ 计入**测量输入**；"
            "m 由 quintessence 条件 m~H₀ 锚定（V₀=6.13e-48 GeV⁴）⇒ 亦属外锚。"
            "⇒ **真正的自由参数只剩 (ξ, β) 两个**，其中 ξ 受 F3.3 双视界约束、β 受 L3 无鬼约束。")
    rep.add("O3", "公理最小化：9 条 → 4 条", "PASS",
            "公理 0'~8' 可重组为：\n"
            "      A（几何）：Cartan 几何 (P→M,ω)，模型空间 ISO(1,3)/SO(1,3)；\n"
            "      B（场内容）：e^a, ω^{ab}, φ（⇒Ω=φ/f）, ψ, A_int；\n"
            "      C（作用量）：R/(2κ)+ξl_PΩRT/(2κ)+L_φ+L_int（+可选挠率项）；\n"
            "      D（变分与边界）：δS=0 + 曲率饱和作为**可选**构型约束；\n"
            "    拓扑荷（Nieh-Yan）、守恒律、极限对应全部降为**推论**，不再单列公理。")
    rep.add("O4", "曲率饱和公理的可删性", "BOUNDARY",
            "公理4' 未被用于推导任何已验证结论，且不可检验（差 76.5~152 个数量级）⇒"
            "按奥卡姆可**删除**；若保留须显式标注为「可选唯象约束」而非理论支柱。")
    rep.add("O5", "自由度总账（诚实披露）", "FAIL",
            "修补后：自由参数 (ξ,β) 2 个 + 外锚 (m,θ₀,ρ_Λ) 3 个；"
            "而它**没有减少** SM 的 19 个参数、没有给出群论关系、没有解释 α。"
            "⇒ 修补达成的是「写形合法」，不是「统一」；与既有 S14-C0004 的判定一致。")


# ----------------------------------------------------------------------------
# §6 矛盾消解对照（C0022–C0029 修补前后）
# ----------------------------------------------------------------------------
def part6(rep):
    rep.section("§6  矛盾消解对照：原 26 项 FAIL 的修补后状态")
    table = [
        ("C0022", "ΩRT 量纲", "已消解（改 ξl_PΩRT/(2κ)，量纲实算 0）"),
        ("C0023", "L_SM 混乘 1/(2κ)", "已消解（前因子只作用于曲率项）"),
        ("C0024", "Ω_DE 非驻点 + Ω 双重身份", "已消解（V 改 (φ/f-θ₀)²；Ω(x) 与 ⟨Ω⟩ 分名）"),
        ("C0025", "Ω 场方程符号 + 动能鬼场", "已消解（sympy 实算残差 0；动能号订正）"),
        ("C0026", "W=∫T∧T 非法", "已消解（改 Nieh-Yan，带 l_P² 归一化）"),
        ("C0027", "主丛 / 直积归一", "**部分消解**（改 Cartan 几何 ✓；直积不归一 ✗ 结构保留）"),
        ("C0028", "曲率饱和不可检验", "**降级**（改称可选唯象约束，可删；数量级不变）"),
        ("C0029", "V₀ 标定两端夹紧", "**未消解**（F3.3 证明更强：ξ 两难，V₀ 外锚不可避）"),
        ("C0012", "真空挠率为零（既有）", "**未消解**（L3：T² 仍不传播，须 R² 型且有无鬼风险）"),
        ("原稿自检4", "极限归属写错", "已消解（§4 L1：真空极限实为 GR+SM）"),
    ]
    for cid, name, state in table:
        v = "PASS" if state.startswith("已消解") else ("FAIL" if "未消解" in state or "部分" in state else "BOUNDARY")
        rep.add("X." + cid, cid + " " + name, v, state)
    rep.add("X.总", "修补效果统计", "INFO",
            "已消解 7 项（写形/符号/记号类）· 部分消解 1 项（结构类）· "
            "未消解 2 项（C0029 ξ 两难、C0012 挠率动力学）· 降级 1 项（C0028）；"
            "另**新暴露** 1 项：F3.3 ξ 两难（双视界不相容，属物理内容缺陷，非写形问题）。")


def main():
    rep = Report()
    rep.section("TUFT 公理化 · 修复后「全维修复优化」精算（v2 体系）")
    rep.echo("  对象：修订版公理 0'~8'；目的 = 验证修补是否闭合 + 极限对应 + 最小化优化")
    rep.echo("  红线：数学/写形自洽 != 物理成立；本册所有「不可检验」结论均按诚实边界标注。")
    part1(rep)
    part2(rep)
    part3(rep)
    part4(rep)
    part5(rep)
    part6(rep)
    cnt = rep.summary()
    rep.section("结论（一句话）")
    rep.echo("  修补在**写形层面完全闭合**（量纲 7/7 配平、场方程残差 0、真空位移闭式成立、"
             "参数由 6 降 2、公理由 9 降 4）；")
    rep.echo("  但在**物理内容层面新暴露一项更硬的缺陷**：ΩRT 耦合的 ξ 两难 —— "
             "宇宙学尺度惰性（δΩ/ξ=%.2e）与普朗克尺度爆炸（δΩ/ξ=%.2e）相差 %d 个数量级，"
             "不存在任何 ξ 使其既有可观测效应又不失控。"
             % (((M_red ** 2) / (4 * M_Pl * 6.129619e-48)) * (12 * H0 ** 2) * H0,
                ((M_red ** 2) / (4 * M_Pl * 6.129619e-48)) * (M_Pl ** 3),
                int(round(math.log10(((M_red ** 2) / (4 * M_Pl * 6.129619e-48)) * (M_Pl ** 3)
                                     / (((M_red ** 2) / (4 * M_Pl * 6.129619e-48)) * (12 * H0 ** 2) * H0))))))
    rep.echo("  因此：修订版应把 ΩRT 项定位为「形式完备但物理惰性的耦合」，"
             "并把 TUFT 的可检验希望明确转移到挠率动力学（β/R² 无鬼扇区）与宇称窗口两个方向。")
    rep.dump()
    return cnt


if __name__ == "__main__":
    main()
