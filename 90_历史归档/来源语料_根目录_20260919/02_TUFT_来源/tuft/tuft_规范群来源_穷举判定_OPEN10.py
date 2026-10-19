# -*- coding: utf-8 -*-
"""
TUFT 四力统一 · 瓶颈①：『规范群第一性来源』穷举判定（OPEN10）
================================================================
承接 OPEN9：穷举证明【空间几何自由度】不足以承载四力统一，
瓶颈定位于『范畴鸿沟』——张量分量不携带规范群 SU(3)×SU(2)×U(1) 结构。

本册穷举：规范群【来源】的所有候选机制，逐个硬判定。

候选（穷举）：
  K1 结群表示论 π₁(S³∖K)→G        （R15 SU(2) / R16 SU(3)）
  K2 高维紧致化 KK（额外维等距群→规范群）
  K3 非对易几何 NCG（Connes 有限谱三元组 M×F）
  K4 弦论杂化 E8×E8（边界条件/紧致化）
  K5 例外群大一统 E8（Lisi 型嵌入）
  K6 纤维丛结构群（主丛 G 直接指定）
  K7 对称破缺 GUT 链（SO(10)→SU(5)→SM；GUT 群外部输入）

硬判据（每条必须过才算该候选可"攻破"统一）：
  G1 群秩/维映射：  能【导出】SU(3) 秩2维8、SU(2) 秩1维3（而非照抄）
  G2 对称破缺：     能给出破缺链与破缺能标（内生）
  G3 GUT 归一化：   U(1)_Y 归一化因子 3/5 能【导出】
  G4 手征表示：     能容纳 SM 手征费米子表示
  G5 反常消除：     能保证/导出反常消除（而非继承 SM 表）

红线：穷举判定，不构造新物理；引用 R11/R15/R16/R17 与 83 号册 G1–G5。
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

P = F = Bd = I = 0


def rec(kind, msg):
    global P, F, Bd, I
    if kind == "PASS":
        P += 1
    elif kind == "FAIL":
        F += 1
    elif kind == "BOUNDARY":
        Bd += 1
    else:
        I += 1
    return kind, msg


# K1: 结群表示论（引用 R15/R16/R17）
#  SU(2): 三叶结 π₁=⟨a,b|a²=b³⟩ → SU(2) 忠实表示 (A_rep=iσ₁, B_rep=diag(e^{±iπ/3}))
#  SU(3): 基本表示 3 可从三叶结 π₁ 导出（R16）
#  但：为何 SU(2)、SU(3)（群选择/N=3 规则）未解释；U(1)_Y 群结构外部
K1 = {
    "id": "K1", "name": "结群表示论 π₁(S³∖K)→G",
    "G1": "partial",  # 表示可构造，但群选择/秩-维映射未导出
    "G2": "no",
    "G3": "no",
    "G4": "yes",      # SU(2) 双重态 + SU(3) 三重态可容纳手征表示
    "G5": "partial",  # 反常消除是 SM 表性质，TUFT 继承
    "note": "R15/R16 已证 SU(2)/SU(3) 表示可【构造】；但『为何是这两个群』『N_c=3 规则』『U(1)_Y 群结构』仍外部（O-KNOTREP/O-KNOTMAP）",
}

# K2: KK 紧致化
#  额外维等距群可给规范群（如 S¹→U(1)）；但 4D 纯 KK 无手征费米子（Nielsen-Ninomiya / Witten 论点）
K2 = {
    "id": "K2", "name": "高维紧致化 KK（等距群→规范群）",
    "G1": "partial",
    "G2": "partial",
    "G3": "no",
    "G4": "no",       # 4D 纯 KK 不能给出手征费米子
    "G5": "partial",
    "note": "等距群可提供 U(1)/部分规范结构；但 4D 纯 KK 无手征费米子、紧致化模不稳定、规范/引力耦合比固定难匹配",
}

# K3: NCG（最强候选：Connes 有限谱三元组给出 SU(3)×SU(2)×U(1)）
K3 = {
    "id": "K3", "name": "非对易几何 NCG（Connes 有限谱三元组 M×F）",
    "G1": "yes",      # 有限代数 M₂(ℍ)⊕M₄(ℂ) 的内自同构群 ⇒ SU(3)×SU(2)×U(1)
    "G2": "partial",  # 破缺由 Higgs（谱三元组自带）但能标/势外部
    "G3": "partial",  # 归一化因子由代数表示决定，但非"第一性导出"
    "G4": "yes",
    "G5": "partial",
    "note": "唯一能给出正确规范群的已知方案；但耦合不汇聚（SM 内容）、Higgs 质量预测 170 GeV 已被 LHC 125 GeV 排除、有限代数本身为输入",
}

# K4: 弦论（规范群来自弦边界条件/紧致化，非"空间运行"）
K4 = {
    "id": "K4", "name": "弦论杂化 E8×E8",
    "G1": "partial",
    "G2": "partial",
    "G3": "partial",
    "G4": "yes",
    "G5": "partial",
    "note": "规范群源自弦动力学与紧致化选择，属【物质/动力学替换】，不在 TUFT 空间框架内；且 Landscape 导致预测力稀释",
}

# K5: E8 大一统（Lisi 型）
K5 = {
    "id": "K5", "name": "例外群大一统 E8（Lisi 型嵌入）",
    "G1": "partial",
    "G2": "no",
    "G3": "partial",
    "G4": "no",       # 三代嵌入不正确（Distler–Garibaldi 反驳）
    "G5": "no",
    "note": "引力+SM 嵌入 E8 的尝试已知存在三代费米子嵌入缺陷，被学界反驳",
}

# K6: 纤维丛结构群（外部注入）
K6 = {
    "id": "K6", "name": "纤维丛主丛结构群（直接指定 G）",
    "G1": "no",       # 外部注入
    "G2": "no",
    "G3": "no",
    "G4": "yes",      # 指定后可容纳
    "G5": "no",
    "note": "规范群为外部输入 ⇒ 不构成『来源/导出』，仅是把 SM 规范结构写进 framework",
}

# K7: GUT 破缺链（GUT 群外部）
K7 = {
    "id": "K7", "name": "对称破缺 GUT 链（SO(10)→SU(5)→SM）",
    "G1": "no",
    "G2": "partial",
    "G3": "partial",
    "G4": "yes",
    "G5": "partial",
    "note": "能给出破缺链，但 GUT 群本身外部输入 ⇒ 未解决『规范群从哪来』",
}

# K8: TUFT 现状（直积打包）
K8 = {
    "id": "K8", "name": "TUFT 现状：直积 SO(1,3)×U(1)×SU(2)×SU(3)",
    "G1": "no",
    "G2": "no",
    "G3": "no",
    "G4": "yes",
    "G5": "no",
    "note": "OPEN9/四力统一报告 §3.1 已判：笛卡尔直积=打包，四个独立耦合常数，不减少参数、不统一任何东西",
}

CANDS = [K1, K2, K3, K4, K5, K6, K7, K8]

LABEL = {
    "partial": "BOUNDARY",
    "no": "FAIL",
    "yes": "PASS",
}


def main():
    L = []
    def out(s=""):
        L.append(s)
        print(s)

    out("=" * 74)
    out("TUFT 四力统一 · 瓶颈①：规范群第一性来源穷举判定（OPEN10）")
    out("run at: 2026-10-19")
    out("=" * 74)
    out("")
    out("【结论前置】规范群 SU(3)×SU(2)×U(1) 的【来源】在 TUFT 现有框架内")
    out("  不可导出；且这是【物理未解问题】，非 TUFT 独有缺陷。")
    out("  唯一能给出正确规范群的已知方案是 NCG（Connes），但它自身")
    out("  耦合不汇聚且 Higgs 质量预测已被 LHC 排除。")
    out("")

    out("== 1. 穷举清单（%d 种规范群来源候选）==" % len(CANDS))
    for c in CANDS:
        out("  %s  %s" % (c["id"], c["name"]))
    out("")

    out("== 2. 逐候选硬判定（G1–G5）==")
    out("")
    results = []
    for c in CANDS:
        g = [c["G1"], c["G2"], c["G3"], c["G4"], c["G5"]]
        sts = [LABEL.get(x, "FAIL") for x in g]
        if "FAIL" in sts:
            verdict = "FAIL"
        elif "BOUNDARY" in sts:
            verdict = "BOUNDARY"
        else:
            verdict = "PASS"
        results.append((c["id"], c["name"], verdict, sts))
        out("  [%s] %s %s" % (verdict, c["id"], c["name"]))
        for i, (nm, v) in enumerate(zip(
                ["G1 群秩/维映射", "G2 对称破缺", "G3 GUT 归一化",
                 "G4 手征表示", "G5 反常消除"], sts), 1):
            out("        %-22s %s" % (nm, v))
        out("        注：%s" % c["note"])
        out("")

    # 统计
    n_pass = sum(1 for r in results if r[2] == "PASS")
    n_fail = sum(1 for r in results if r[2] == "FAIL")
    n_bd = sum(1 for r in results if r[2] == "BOUNDARY")

    out("== 3. 判定矩阵汇总 ==")
    out("  %-6s %-44s %s" % ("ID", "规范群来源候选", "综合"))
    out("  " + "-" * 66)
    for cid, nm, v, _ in results:
        out("  %-6s %-44s %s" % (cid, nm, v))
    out("")
    out("  PASS=%d  FAIL=%d  BOUNDARY=%d（共 %d 种）" % (n_pass, n_fail, n_bd, len(results)))

    out("")
    out("== 4. 诚实结论（对瓶颈①的判定）==")
    if n_pass == 0:
        _f = rec("FAIL", "无任何候选能【导出】规范群 SU(3)×SU(2)×U(1)")
        out("  [FAIL] %s" % _f[1])
    out("  [FAIL] 最强候选 NCG 亦不达标  |  唯一给出正确规范群的方案，但：")
    out("        (i) 规范耦合仍不汇聚（SM 物质内容，ΔL=9.1467）；")
    out("        (ii) Higgs 质量预测 170 GeV vs LHC 实测 125 GeV ⇒ 已被排除。")
    out("  [FAIL] 结群路线（R15/R16）只能构造【表示】不能导出【群选择】  |  ")
    out("        为何是 SU(2)/SU(3)、为何 N_c=3 —— 无选择规则（O-KNOTREP/O-KNOTMAP 残余）。")
    out("  [FAIL] 直积/纤维丛/破缺链均属外部输入  |  不构成『来源』（OPEN9 §3.1 + 83 号册 G1–G5）。")
    out("")
    out("  ⇒ 瓶颈①（规范群来源）当前【不可攻破】：缺少的不是空间机制，")
    out("     而是『为何是 SU(3)×SU(2)×U(1)、为何 N_c=3』的物理第一性输入。")
    out("  ⇒ 与瓶颈②（耦合汇聚需 SUSY 新物质态）同源：二者都是【物质内容】问题，")
    out("     不是【空间几何】问题 —— 此为对本轮『攻破』的最重要校准。")

    out("")
    out("== 汇总 ==")
    out("  PASS=%d  FAIL=%d  BOUNDARY=%d  INFO=%d" % (P, F, Bd, I))
    out("")
    out("红线：穷举判定，不构造新物理；引用 R11/R15/R16/R17 与 83 号册 G1–G5；")
    out("负结论为『不可导出』的可导出性判定，非对 TUFT 框架的证伪宣告。")

    txt = "\n".join(L) + "\n"
    rp = os.path.join(HERE, "tuft_规范群来源_穷举判定_OPEN10_report.txt")
    open(rp, "w", encoding="utf-8").write(txt)
    print("已生成:", rp)


if __name__ == "__main__":
    main()
