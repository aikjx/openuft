# -*- coding: utf-8 -*-
"""
TUFT 四力统一：『所有空间运行方式』穷举与判定（OPEN9）
========================================================
问题：能否通过【空间的运行方式】（即时空几何的全部自由度）攻破四力统一？

穷举范围（空间运行方式 = 联络/几何自由度的所有载体）：
  联络层三一（metric-affine 标准分解：∇ = LeviCivita + contortion(挠率) + disformation(非度规)）：
     R 曲率  T 挠率  Q 非度规性   → 7 种非空子集
  世界线层（Frenet）：  4D 三曲率 κ1, κ2, κ3
  拓扑层：              链环 Lk / 辫群表示
  扩展空间（对照）：     高维紧致化 KK / 非对易几何 NCG / 外部注入规范（现状直积）

硬判据（每条必须过才算"攻破"）：
  C1 自由度充足：独立分量数 ≥4 且足以区分四种相互作用
  C2 规范群可导出：SU(3)×SU(2)×U(1) 有【几何来源】，非外部注入
  C3 单群/半单：非笛卡尔直积（直积=打包，不减少耦合常数）
  C4 耦合汇聚：α_i 汇聚（引用 R11/R12：SM 1-loop ΔL=9.1467 不汇聚；
                MSSM ΔL=0.130、τ_p=3.52e34>2.4e34 达标但需 SUSY 物质）
  C5 手征费米子：能容纳 SM 手征表示

红线：本册为穷举判定，不构造新物理；引用 R11/R12/R14 既有数值；
负结论为可导出性判定，非证伪宣告。
"""
import os
import sys
import itertools

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

P = F = Bd = I = 0


def _p(m):
    global P
    P += 1
    return "PASS", m


def _f(m):
    global F
    F += 1
    return "FAIL", m


def _b(m):
    global Bd
    Bd += 1
    return "BOUNDARY", m


def _i(m):
    global I
    I += 1
    return "INFO", m


# ---- 4D 各几何对象的独立分量数（标准微分几何，可硬编码并注明来源）----
# Riemann R^ρ_{σμν}:  n²(n²−1)/12 = 20
# 挠率  T^ρ_{μν}(μν反对称): n²(n−1)/2 = 24 = 矢量4 + 轴矢4 + 纯张量16
# 非度规 Q_{ρμν}(μν对称):   n²(n+1)/2 = 40 = Weyl矢量4 + 无迹36
DOF = {"R": 20, "T": 24, "Q": 40, "Frenet": 3, "Lk": 1}

# R11/R12 既有结论（引用，非本册新算）
SM_DL = 9.1467          # 1-loop SM 三耦合不汇聚，ΔL(e-fold)
MSSM_DL = 0.130         # MSSM 汇聚
TAU_P_MSSM = 3.52e34    # 年
TAU_P_LIMIT = 2.4e34    # Super-K 下限


def judge(name, dofs, gauge_src, semisimple, unif, chiral, note=""):
    """返回 (综合判定, 各判据列表)"""
    rows = []
    # C1 自由度充足
    if dofs >= 4:
        rows.append(("C1",) + _p("分量数 %d ≥4，数量上充足" % dofs))
    else:
        rows.append(("C1",) + _f("分量数 %d <4，不足以区分四力" % dofs))
    # C2 规范群可导出
    if gauge_src == "geometric":
        rows.append(("C2",) + _p("规范群有几何来源"))
    elif gauge_src == "partial":
        rows.append(("C2",) + _b("规范群部分可导出（依赖额外结构/紧致化选择）"))
    elif gauge_src == "external":
        rows.append(("C2",) + _f("规范群为外部注入（无几何来源）"))
    # C3 单群/半单
    if semisimple == "yes":
        rows.append(("C3",) + _p("单群/半单 ⇒ 真正统一"))
    elif semisimple == "partial":
        rows.append(("C3",) + _b("半单性依赖紧致化/代数选择"))
    else:
        rows.append(("C3",) + _f("笛卡尔直积 ⇒ 仅打包，耦合常数不减少"))
    # C4 汇聚
    if unif == "yes":
        rows.append(("C4",) + _p("耦合汇聚且质子衰变达标"))
    elif unif == "needs_susy":
        rows.append(("C4",) + _b("仅引入 SUSY 物质后汇聚（ΔL=%.3f, τ_p=%.2e）——非空间机制" % (
            MSSM_DL, TAU_P_MSSM)))
    else:
        rows.append(("C4",) + _f("SM 1-loop ΔL=%.4f 不汇聚 ⇒ 无统一能标" % SM_DL))
    # C5 手征
    if chiral == "yes":
        rows.append(("C5",) + _p("可容纳 SM 手征表示"))
    elif chiral == "partial":
        rows.append(("C5",) + _b("手征性需额外机制（如 KK 需 orbifold/缠绕）"))
    else:
        rows.append(("C5",) + _f("不能容纳手征费米子"))

    st = [r[1] for r in rows]
    if "FAIL" in st:
        verdict = "FAIL"
    elif "BOUNDARY" in st:
        verdict = "BOUNDARY"
    else:
        verdict = "PASS"
    return verdict, rows


def main():
    L = []
    def out(s=""):
        L.append(s)
        print(s)

    out("=" * 74)
    out("TUFT 四力统一：『所有空间运行方式』穷举判定（OPEN9）")
    out("run at: 2026-10-18")
    out("=" * 74)

    # ---- 构造候选：联络三一的所有非空子集 + 世界线/拓扑/扩展 ----
    cands = []
    for r in range(1, 4):
        for combo in itertools.combinations(["R", "T", "Q"], r):
            dofs = sum(DOF[c] for c in combo)
            cands.append(("+".join(combo), combo, dofs))

    out("")
    out("== 1. 穷举清单：联络三一的全部非空子集（%d 种）==" % len(cands))
    out("  4D 独立分量数：R(曲率)=%d, T(挠率)=%d, Q(非度规)=%d" % (
        DOF["R"], DOF["T"], DOF["Q"]))
    out("  （metric-affine：∇ = LeviCivita + contortion(T) + disformation(Q)）")
    for nm, cb, df in cands:
        out("    %-8s 分量数=%d" % (nm, df))
    out("")
    _i("穷举完备性：联络层三一是仿射联络的完备分解 ⇒ 无任何第四种纯联络自由度遗漏")
    out("")

    # ---- 逐候选判定 ----
    out("== 2. 逐候选判定（C1–C5）==")
    out("")
    results = []
    # 联络三一子集：共性——规范群均外部注入（无几何函子，R14 同款范畴鸿沟），
    # 且物质仍为 SM ⇒ 不汇聚；仅含引力/或加挠率不能自发给出 SU(3)×SU(2)×U(1)
    for nm, cb, df in cands:
        # 是否含挠率（TUFT 现状用 τ）
        # 规范群：联络张量分量不携带规范群结构 ⇒ external（R14 已证无自然函子）
        v, rows = judge(
            name=nm, dofs=df,
            gauge_src="external",      # 张量分量无 SU(3)×SU(2)×U(1) 结构
            semisimple="no",           # 无单群结构（只有几何，无规范群）
            unif="no",                 # 物质仍 SM ⇒ ΔL=9.1467
            chiral="partial",
        )
        results.append((nm, v, rows))
        out("  [%s] 联络子集 %s（分量 %d）" % (v, nm, df))
        for cid, st, msg in rows:
            out("        %s %s: %s" % (cid, st, msg))

    out("")
    # ---- Frenet / 拓扑 / 扩展 ----
    extra = [
        ("Frenet κ1/κ2/κ3（4D 世界线三曲率）", DOF["Frenet"], "external", "no", "no", "partial",
         "3 个标量不变量 <4 种相互作用 ⇒ 数量即不足；且标量不携带规范群"),
        ("拓扑：链环 Lk / 辫群表示", DOF["Lk"], "external", "no", "no", "partial",
         "R14 已证：曲线拓扑不变量→规范量子数无自然函子（范畴鸿沟）"),
        ("高维紧致化 KK（额外维等距群→规范群）", 20 + 24 + 40, "partial", "partial", "no", "no",
         "可给出 U(1)/部分规范群，但 4D 纯 KK 不能给出手征费米子；紧致化模不稳定"),
        ("非对易几何 NCG（有限谱三元组）", 20 + 24 + 40, "partial", "partial", "no", "partial",
         "Connes 方案可给出 SU(3)×SU(2)×U(1)，但耦合仍不汇聚且 Higgs 质量预测已被排除"),
        ("外部注入规范（现状直积 SO(1,3)×U(1)×SU(2)×SU(3)）", 18, "external", "no", "no", "yes",
         "四力统一报告 §3.1 已判：直积=打包，不减少耦合常数"),
    ]
    for nm, df, gs, ss, un, ch, note in extra:
        v, rows = judge(nm, df, gs, ss, un, ch)
        results.append((nm, v, rows))
        out("  [%s] %s" % (v, nm))
        for cid, st, msg in rows:
            out("        %s %s: %s" % (cid, st, msg))
        out("        注：%s" % note)

    # ---- 汇总矩阵 ----
    out("")
    out("== 3. 判定矩阵汇总 ==")
    out("  %-46s %s" % ("空间运行方式", "综合"))
    out("  " + "-" * 60)
    for nm, v, _ in results:
        out("  %-46s %s" % (nm, v))

    n_pass = sum(1 for _, v, _ in results if v == "PASS")
    n_fail = sum(1 for _, v, _ in results if v == "FAIL")
    n_bd = sum(1 for _, v, _ in results if v == "BOUNDARY")
    out("")
    out("  PASS=%d  FAIL=%d  BOUNDARY=%d（共 %d 种空间运行方式）" % (
        n_pass, n_fail, n_bd, len(results)))

    out("")
    out("== 4. 诚实结论 ==")
    if n_pass == 0:
        _f("无任何空间运行方式能攻破四力统一  |  %d 种穷举全部未通过 C1–C5" % len(results))
        out("  [FAIL] 穷举结论：空间几何自由度不足以承载四力统一")
    out("  [FAIL] 瓶颈不在『自由度数量』  |  分量数充足（R20/T24/Q40，合计 84 ≫ 4），")
    out("        而在『范畴鸿沟』：张量分量不携带规范群结构 ——")
    out("        SU(3)×SU(2)×U(1) 不能由曲率/挠率/非度规的分量导出（与 R14 结拓扑同款）")
    out("  [FAIL] 瓶颈二：耦合汇聚  |  物质内容若仍为 SM，1-loop ΔL=%.4f ⇒ 三耦合不汇聚；" % SM_DL)
    out("        唯一已知达标路径是引入 SUSY 等【新物质态】（ΔL=%.3f, τ_p=%.2e），" % (
        MSSM_DL, TAU_P_MSSM))
    out("        而新物质态【不是空间运行方式】⇒ 超出本穷举范畴（BOUNDARY 而非 PASS）")
    out("  [INFO] 对『四力统一』现状的校准  |  现有『统一』是 EH+YM+Dirac 打包 + 直积群，")
    out("        PASS 项（如 m_W/m_Z=cosθ_W、反常消除）均为标准模型重述/继承，非 TUFT 导出")
    out("")
    out("  ⇒ 攻破四力统一需要的是【物质/新物理输入 + 规范群来源】，")
    out("    而非更多的空间几何机制；单纯穷举空间运行方式无法达成。")

    out("")
    out("== 汇总 ==")
    out("  PASS=%d  FAIL=%d  BOUNDARY=%d  INFO=%d" % (P, F, Bd, I))
    out("")
    out("红线：本册为穷举判定，不构造新物理；ΔL/τ_p 引用 R11/R12，范畴鸿沟引用 R14。")
    out("负结论是『空间机制不可达』的可导出性判定，非对 TUFT 框架的证伪宣告。")

    txt = "\n".join(L) + "\n"
    rp = os.path.join(HERE, "tuft_四力统一_空间运行方式穷举_OPEN9_report.txt")
    open(rp, "w", encoding="utf-8").write(txt)
    print("已生成:", rp)


if __name__ == "__main__":
    main()
