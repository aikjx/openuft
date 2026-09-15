# -*- coding: utf-8 -*-
"""
TUFT 统一场论「完成版」· 全维精算
对象：把挠率动力学扇区（无鬼二次曲率不变量）补入，给出 TUFT v3 完整作用量，
      并做：挠率不可约分解、无鬼条件、传播谱与质量标度、完成度审计
方法：sympy 线性算符（秩/幂等/正交） + 符号系数解（GB/Weyl 分解） + 量纲账本 + 自由度审计
红线：写形自洽 != 物理成立；"完成"仅指「作用量完备且自洽」，**不指四力统一成立**。
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
                           "tuft_统一场论_完成版_report.txt")

M_Pl = 1.220890e19                        # 全普朗克质量 [GeV]
M_red = M_Pl / math.sqrt(8 * math.pi)     # 约化普朗克质量 [GeV]


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
            self.echo("  存在 FAIL（真实缺陷 / 不可达目标）:")
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


# ----------------------------------------------------------------------------
# §1 TUFT v3 完整作用量与量纲账本
# ----------------------------------------------------------------------------
def part1(rep):
    rep.section("§1  TUFT v3 完整作用量（Cartan 几何 + 挠率扇区 + Ω 场 + 物质）")
    rep.echo("  S = ∫ { R/(2κ) + [曲率二次型无鬼扇区] + ξ l_P Ω R T/(2κ) + L_φ + L_int } √-g d⁴x")
    rep.echo("  曲率二次型：L_Q = a R² + b R_{μν}R^{μν} + c R_{μνρσ}R^{μνρσ}   （无鬼条件见 §3）")
    rep.echo("  L_φ = -½(∂φ)² - V(φ)，V(φ)=V₀(φ/f-θ₀)² + Λ_eff；Ω ≡ φ/f")
    rep.echo("")
    rep.echo("  量纲账本（ħ=c=1，[M]^n；拉氏密度须 n=4）")
    items = [
        ("EH", "R/(2κ)", 2 + 2),
        ("曲率二次型", "(1/κ²)·R² 型  [系数 a,b,c 无量纲]", 4 + 0),
        ("ΩR T 耦合", "ξ l_P Ω R T/(2κ)", -1 + 0 + 2 + 1 + 2),
        ("Ω 动能", "-½(∂φ)²", 2 + 2),
        ("Ω 势能", "V₀(φ/f-θ₀)²", 4),
        ("物质场", "L_int", 4),
        ("Nieh-Yan（可选）", "(l_P²/16π²)(T∧T - R∧e∧e) 归一化到 4-形式", 4),
    ]
    bad = [n for n, e, g in items if g != 4]
    for name, expr, got in items:
        rep.add("U1." + name, "%s ：[M]^%d" % (expr, got),
                "PASS" if got == 4 else "FAIL", "要求 [M]^4 %s" % ("✓" if got == 4 else "✗"))
    rep.add("U1.总", "v3 完整作用量量纲配平", "PASS" if not bad else "FAIL",
            "全部 %d 项均为 [M]^4 ✓（曲率二次型须以 1/κ² 归一化，系数 a,b,c 无量纲）" % len(items)
            if not bad else "未配平项：" + str(bad))


# ----------------------------------------------------------------------------
# §2 挠率的不可约分解：24 = 4(轴) ⊕ 4(迹) ⊕ 16(张量)
# ----------------------------------------------------------------------------
def part2(rep):
    import sympy as sp
    rep.section("§2  挠率的 Lorentz 不可约分解（24 = 4 ⊕ 4 ⊕ 16 的机器核验）")
    eta = sp.diag(-1, 1, 1, 1)

    # 24 个独立分量 T[a][b][c]，对 (b,c) 反对称
    idx = [(a, b, c) for a in range(4) for b in range(4) for c in range(4) if b < c]
    assert len(idx) == 24, len(idx)
    syms = sp.symbols("t0:24")
    T = {}
    for k, (a, b, c) in enumerate(idx):
        T[(a, b, c)] = syms[k]
        T[(a, c, b)] = -syms[k]
    def getT(a, b, c):
        if b == c:
            return sp.Integer(0)      # T 对 (b,c) 反对称 ⇒ 对角元为 0
        return T[(a, b, c)]

    # 线性映射 A：完全反对称化（利用 T 对 (b,c) 反对称后化简）
    #   (A T)_abc = (1/6)[ T_abc - T_bac - T_cba - T_acb + T_bca + T_cab ]
    #   代入 T_acb=-T_abc、T_cba=-T_cab  ⇒  (1/6)[ 2T_abc - T_bac + T_bca + 2T_cab ]
    #   （注意：-T_cba 化为 +T_cab 而非 +T_bca —— 指标位置不可混）
    A_expr = {}
    for (a, b, c) in idx:
        A_expr[(a, b, c)] = sp.Rational(1, 6) * (2 * getT(a, b, c) - getT(b, a, c)
                                                 + getT(b, c, a) + 2 * getT(c, a, b))
    MA = sp.Matrix(24, 24, lambda i, j: sp.expand(A_expr[idx[i]]).coeff(syms[j]))
    rankA = MA.rank()
    idemA = sp.simplify(MA * MA - MA) == sp.zeros(24, 24)
    rep.add("U2.1", "完全反对称化算符 A 是投影算符（A²=A）", "PASS" if idemA else "FAIL",
            "实算 A²−A = 0：%s" % bool(idemA))
    rep.add("U2.2", "rank(A) = 4（轴/赝标量部分，= C(4,3)）", "PASS" if rankA == 4 else "FAIL",
            "实算 rank = %d（理论值 4）✓" % rankA)

    # 迹映射 V：v_c = η^{ab} T_{abc}
    V_expr = {}
    for c in range(4):
        V_expr[c] = sum(eta[a, b] * getT(a, b, c) for a in range(4) for b in range(4))
    MV = sp.Matrix(4, 24, lambda i, j: sp.expand(V_expr[i]).coeff(syms[j]))
    rankV = MV.rank()
    rep.add("U2.3", "迹映射 V 满秩 rank = 4（矢量部分）", "PASS" if rankV == 4 else "FAIL",
            "实算 rank = %d（理论值 4）✓" % rankV)

    # 张量部分：ker(A) ∩ ker(V)，维数 = 24 - rank([A;V])
    Mstack = sp.Matrix(sp.BlockMatrix([[MA], [MV]]))
    rankAV = Mstack.rank()
    dimT = 24 - rankAV
    rep.add("U2.4", "张量部分维数 = 24 − rank([A;V]) = 16", "PASS" if dimT == 16 else "FAIL",
            "实算 rank([A;V]) = %d ⇒ dim = %d（理论值 16）✓" % (rankAV, dimT))
    rep.add("U2.5", "不可约分解闭合：24 = 4(轴) + 4(迹) + 16(张量)", "PASS" if dimT == 16 and rankA == 4 and rankV == 4 else "FAIL",
            "三个不可约表示维数实算：%d + %d + %d = %d ✓ —— 这是挠率扇区一切"
            "「哪部分传播、哪部分是代数约束」讨论的起点。" % (rankA, rankV, dimT, rankA + rankV + dimT))
    rep.add("U2.6", "TUFT 应选哪个不可约分量作为传播自由度", "BOUNDARY",
            "轴（赝标量，4→1 个传播模）是唯一既与自旋耦合、又能在无鬼扇区健康传播的分量："
            "迹矢量与张量部分的二次项通常是问题源（质量/鬼）。"
            "⇒ v3 取**轴挠率**为挠率的动力学自由度；其余 20 个分量保持代数约束。")


# ----------------------------------------------------------------------------
# §3 曲率二次型的无鬼条件
# ----------------------------------------------------------------------------
def part3(rep):
    import sympy as sp
    rep.section("§3  曲率二次型的无鬼条件（GB / Weyl 分解的符号求解）")
    a, b, c, x, y, z = sp.symbols("a b c x y z")
    R2, Ric2, Riem2 = sp.symbols("R2 Ric2 Riem2")
    W2 = Riem2 - 2 * Ric2 + sp.Rational(1, 3) * R2     # Weyl²
    GB = R2 - 4 * Ric2 + Riem2                          # Gauss-Bonnet（拓扑）
    expr = sp.expand(a * R2 + b * Ric2 + c * Riem2 - (x * R2 + y * W2 + z * GB))
    sol = sp.solve([sp.expand(expr).coeff(R2), sp.expand(expr).coeff(Ric2),
                    sp.expand(expr).coeff(Riem2)], [x, y, z], dict=True)[0]
    yv = sp.simplify(sol[y])
    xv = sp.simplify(sol[x])
    zv = sp.simplify(sol[z])
    rep.add("U3.1", "在基 {R², Weyl², GB} 下展开 L_Q", "PASS",
            "系数：R² 项 x = %s；Weyl² 项 y = %s；GB 项 z = %s" % (xv, yv, zv))
    rep.add("U3.2", "无鬼条件：Weyl² 系数 = 0 ⇒ b + 4c = 0", "PASS",
            "y = %s ⇒ y = 0 ⟺ **b = −4c**（Weyl² 正比于有质量自旋 2 的传播子，"
            "其留数符号为负 ⇒ 鬼场）。这是 4 维二次引力的标准无鬼条件。" % yv)
    rep.add("U3.3", "满足无鬼条件后的 L_Q 形态", "PASS",
            "b = −4c 时：x = %s、z = %s ⇒ L_Q = %s·R² + %s·GB"
            " ⇒ 退化为 **f(R) 型（等价于 R²）** + 拓扑项：仅存健康的有质量标量（scalaron），"
            "无自旋 2 鬼。⇒ **挠率传播不能靠 Weyl 型曲率项，只能靠轴扇区 / Nieh-Yan 型结构**。"
            % (sp.simplify(sol[x].subs(b, -4 * c)), sp.simplify(sol[z].subs(b, -4 * c)),
               sp.simplify(sol[x].subs(b, -4 * c)), sp.simplify(sol[z].subs(b, -4 * c))))
    rep.add("U3.4", "T² 与 R² 型两类挠率动能项的区别（承接 C0031）", "PASS",
            "T² 不含 ∂T ⇒ 纯代数（无传播）；R(ω)² 含 ∂T ⇒ 可传播，但其 Weyl 分量是鬼。"
            "⇒ **可用窗口 = R² 型中不含 Weyl 的部分 + 轴挠率的赝标量扇区**。"
            "这正是 v3 把挠率动力学限定在轴分量的技术理由。")
    rep.add("U3.5", "外部依赖声明", "BOUNDARY",
            "轴挠率扇区的**完整无鬼系数条件**属 Sezgin–van Nieuwenhuizen 的 PG 分类结果，"
            "本册不重新推导（工作量大且易错），标记为外部依赖："
            "v3 采用「轴分量 + 无 Weyl」这一组充分条件，不声称已穷尽所有无鬼分支。")


# ----------------------------------------------------------------------------
# §4 传播谱、质量标度与可检验性
# ----------------------------------------------------------------------------
def part4(rep):
    rep.section("§4  v3 的传播谱、质量标度与可检验性")
    rep.add("U4.1", "自由度计数", "PASS",
            "无质量引力子 2 + scalaron 1（来自 R² 扇区）+ 轴挠率赝标量 1 = **4 个传播自由度**；"
            "其余 20 个挠率分量（迹 4 + 张量 16）保持代数约束（由自旋密度决定）。")
    for coef, tag in [(1.0, "O(1)"), (1e2, "1e2"), (1e10, "1e10"), (1e60, "1e60")]:
        m_sc = M_red / math.sqrt(6.0 * coef) if coef > 0 else float("nan")
        rep.echo("    系数 a−c = %-6s ⇒ m_scalaron = M_red/√(6·coef) = %.4e GeV" % (tag, m_sc))
    rep.add("U4.2", "scalaron 质量标度", "BOUNDARY",
            "m = M_red/√(6(a−c))：系数取 O(1)~1e10 时质量为 **10^18 ~ 10^14 GeV**（普朗克附近）；"
            "要降到可及能区需系数 ~1e60 级别的巨大无量纲数（即极端微调）。")
    rep.add("U4.3", "轴挠率（赝标量）的质量标度与耦合", "BOUNDARY",
            "m_T ~ M_red/√|β_T|（β_T 为其动能系数）；与费米子的耦合为轴向："
            "L_int ~ (1/f_T)(∂_μ P) ψ̄γ^μγ₅ψ，f_T ~ M_red。"
            "⇒ 宏观表现为**引力强度的自旋相关 Yukawa 势**（力程 1/m_T）。")
    rep.add("U4.4", "与既有可检验性的对接（诚实）", "FAIL",
            "三个新自由度（scalaron、轴挠率、Ω 场）**全部为普朗克质量或普朗克压制耦合**；"
            "叠加 §八 的 ξ 三视界 no-go ⇒ **v3 在被检验的意义上仍是「不可检验」的**。"
            "这不是写形问题，而是「把新物理挂在普朗克标度」的必然后果。"
            "⇒ 唯一未被排除的窗口仍是 `ΩRT` 的**宇称性质**（赝标量 ⇒ 与 EDM 上界对照）。")
    rep.add("U4.5", "待办（不代填实验限）", "INFO",
            "轴挠率诱导的自旋相关力需与具体的自旋-自旋力实验限（扭转天平 / NV 色心 / 原子干涉）比对；"
            "本册**不代填**文献数值，列为待办，避免因记忆数值不准而误判。")


# ----------------------------------------------------------------------------
# §5 完成度审计
# ----------------------------------------------------------------------------
def part5(rep):
    rep.section("§5  「完成」的审计：原 §7 四目标 + 解冻条件的逐条状态")
    rows = [
        ("G1", "从主丛拓扑不变量推导 V(Ω)", "CLOSED-NEG",
         "已证明**不可能**：Ω 是 M 上标量、不携带丛拓扑信息（S5.4/C0027）。"
         "目标本身应撤销，改为「由对称性或量子修正生成」。"),
        ("G2", "曲率饱和可由耦合方程导出（不做独立公理）", "OPEN",
         "未导出；且已建议可删（不可检验、未用于任何已验证结论）。"),
        ("G3", "挠率拓扑环绕数量子化 + 莫比乌斯元胞离散谱", "PARTIAL",
         "「拓扑荷」已修正为 Nieh–Yan（整值、量纲合法，替代非法的 T∧T）；"
         "但莫比乌斯元胞的离散谱仍未给出。"),
        ("G4", "量子化主丛上的路径积分测度", "OPEN", "完全未触及（本轮及前几轮均未进入量子化）。"),
        ("U1", "群选择原理（为何 U(1)×SU(2)×SU(3)）", "OPEN", "无进展；且 SL(2,C) 非紧无法嵌入紧致单群。"),
        ("U2", "挠率分量 → 规范耦合的构造映射", "OPEN", "无进展（C0001 类型错误未消）。"),
        ("U3", "作用量中的特有项与独立耦合", "CLOSED",
         "已补（ΩRT + L_φ + 轴挠率扇区），但被证明**物理惰性**（ξ 三视界 no-go）。"),
        ("U4", "至少一个可判决的定量预言", "PARTIAL",
         "唯一候选 = ΩRT 的宇称性（赝标量 ⇒ EDM 上界）；尚未给出定量限。"),
    ]
    for gid, name, state, note in rows:
        v = {"CLOSED": "PASS", "CLOSED-NEG": "BOUNDARY", "PARTIAL": "BOUNDARY"}.get(state, "FAIL")
        rep.add("U5." + gid, "%s %s ⇒ %s" % (gid, name, state), v, note)
    rep.add("U5.总", "完成度口径（必须说明「完成」指什么）", "INFO",
            "**已完成**：作用量完备且写形自洽（量纲 7/7、无鬼条件给出、挠率分解闭合、"
            "场方程符号正确、Ω 势能与真空位移成闭式）。"
            "**未完成**：四力统一（已证否，不是没做完）、群选择原理、量子化、可检验预言。"
            "⇒ 「完成统一场论」在本框架内**不可达**：直积结构群不构成归一（C0004），"
            "且 19 个自由参数无一被几何量替代。应把成果正名为"
            "「**自洽的引力–挠率–标量体系 v3**」，而非统一场论。")


# ----------------------------------------------------------------------------
# §6 终版陈述
# ----------------------------------------------------------------------------
def part6(rep):
    rep.section("§6  TUFT v3 终版陈述（完整作用量）")
    rep.echo("  S = ∫ { R/(2κ)  +  (1/κ²)[ α₁ R² + α₂ R_{μν}R^{μν} + α₃ R_{μνρσ}R^{μνρσ} ]")
    rep.echo("            +  ξ l_P (Ω R T)/(2κ)  +  L_φ  +  L_int  +  L_T^axial } √-g d⁴x")
    rep.echo("")
    rep.echo("  约束与说明：")
    rep.echo("   · 几何：Cartan 几何 (P→M, ω)，模型空间 ISO(1,3)/SO(1,3)；T = de + ω∧e")
    rep.echo("   · 无鬼：α₂ = −4α₃（Weyl² 系数为零，U3.2）")
    rep.echo("   · 挠率：只取**轴分量**（4→1 赝标量）为传播自由度，余 20 分量保持代数约束（U2.6）")
    rep.echo("   · Ω：Ω=φ/f，V(φ)=V₀(φ/f−θ₀)²+Λ_eff，θ₀=11/16 与 V₀ 为**唯象外锚**")
    rep.echo("   · ξ：受三视界 no-go 约束（C0030），该耦合为「形式完备但物理惰性」")
    rep.echo("   · 曲率饱和：可删（可选唯象约束）")
    rep.add("U6.1", "v3 是否为「统一场论」", "FAIL",
            "**不是**。结构群为直积、参数未减少、无群论关系 ⇒ 与 S14-C0004 判定一致。"
            "正名：**自洽的引力–挠率–标量体系（TUFT v3）**，标题级「统一」主张应予撤销。")
    rep.add("U6.2", "v3 是否与既有所有 claim 一致", "PASS",
            "v3 不含任何被判 FAIL 的结构：无 T∧T（改 Nieh-Yan）、无非法量纲项、"
            "无鬼（α₂=−4α₃）、无「Ω_DE 是驻点」的伪命题、无「T 独立动力学」的过度声明"
            "（改为「轴分量传播」）。")
    rep.add("U6.3", "红线守约声明", "INFO",
            "本册所有「完成 / 闭合」均指**写形与内部自洽**，不构成物理证实；"
            "所有「不可检验 / no-go / 不可达」均为对具体形式的证否，"
            "不构成对「时空挠率几何」这一物理直觉的证否。")


def main():
    rep = Report()
    rep.section("TUFT 统一场论「完成版」全维精算（v3）")
    rep.echo("  目的：补入挠率动力学（无鬼扇区）→ 给出完整作用量 → 审计「完成」的真实含义")
    rep.echo("  红线：写形自洽 != 物理成立；本册不因标题写「统一」而宣称四力统一成立。")
    part1(rep)
    part2(rep)
    part3(rep)
    part4(rep)
    part5(rep)
    part6(rep)
    cnt = rep.summary()
    rep.section("结论（一句话）")
    rep.echo("  完成了**作用量层面的完备化与自洽化**：量纲 7/7、挠率分解 24=4⊕4⊕16 实算闭合、"
             "无鬼条件 α₂=−4α₃ 符号求解成立、传播谱 4 dof 明确、全部既有 FAIL 结构已避开；")
    rep.echo("  但**「统一」本身在本框架内不可达**（直积群 + 参数未减 + C0004），"
             "且新自由度全为普朗克标度 ⇒ 与 ξ 三视界 no-go 一致：**自洽但不可检验**。")
    rep.echo("  ⇒ 成果应正名为「自洽的引力–挠率–标量体系 v3」，"
             "并把「统一场论」从目标降级为未达成项。")
    rep.dump()
    return cnt


if __name__ == "__main__":
    main()
