# -*- coding: utf-8 -*-
"""r360 README 登记（幂等，零删除守卫）"""

import os
import shutil
from collections import Counter

BASE = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
README = os.path.join(BASE, "README.md")
BAK = os.path.join(BASE, "README.md.bak_r360")

SRC_ANCHOR = u"│   ├── TUFT-r346_整数Newton系数是三行初等事实而非几何定理"
PAN_ANCHOR = u"├── 判定_TUFT-r346_整数Newton系数是三行初等事实而非几何定理"

SRC_LINE = (
    u"│   ├── TUFT-r360_ROOTV29_DiracMaxwell自洽性_均匀解场能口径修正_局域化残差对螺旋零判别力_试探族单调稳健_精算与可视化_2026-11-02.py"
    u"  # 新增（**r360 · 2026-11-02**）：**ROOT V29 审计：Dirac–Maxwell 自洽性、均匀解场能口径修正、局域化残差对螺旋零判别力、试探族单调稳健**"
    u"（条目 **24**：A 精确代数 4 / B 高精度数值 9 / G 判决 6 / C 对照 3 / PRICE 1 / ENGINE 1；"
    u"**数学层 13/13 PASS**、**判决层 5 FAIL**、**对照 3/3 PASS**、退出码 0）。"
    u"★**取号**：r355、r356 已被并行链占（src=1 pan=1 dat=3 / src=1 pan=0 dat=5），r357–r359 紧邻热区 ⇒ 取冷号 **r360**，"
    u"动手前先写 `_probe_r360.py` 占位，零改他人字节。★**与 r354 的关系**：r354 审 V28（双光状电流：正能量互斥、满射判别力 0、平面波非局域）；"
    u"本卷审 V29 新增层，并对 r354 的两条 OPEN 作推进度登记。"
    u"★★**复算：来料数值全部正确** —— 场能闭式（固定 rho 口径）闭式 vs 数值一致；"
    u"**静电自能系数三路径交叉**：Fourier 解析 0.398942280401432678 / 电场能量积分（差 8.2e-17）/ 两两相互作用积分（差 5e-59）；"
    u"试探能量表 6 组按列有效位数推导容差（动能列 1e-6、电磁列 1e-3）逐项吻合；α_G = 1.7518094e-45、α_G/α = 2.40061e-43 与来料一致；"
    u"**5000 组随机旋量 Fierz 用精确 Fraction 复算，违例 0**（强于来料浮点残差 1.78e-15）；轴对称 ansatz 四分量 j_z = ℓ+1/2 一致（半整数，费米子合规）。"
    u"★★★**修正一（G01 口径）**：来料的 U ≥ 2πρ²L⁵/(45ε₀) 把 ρ 当作与 L 独立的常数；**孤立电子的前提是 Q=e 固定**，"
    u"此时 ρ(L)=3e/(4πL³) ⇒ **U = e²/(40πε₀L) = αħc/(10L) ∝ 1/L**，L→∞ 时趋于 0 而非发散。"
    u"实测两口径在 x=1 同为 7.297e-4，x=10 时一个 72.97（增）一个 7.297e-5（减）⇒ **趋势相反**。"
    u"⇒ 修正后第一节与第三节不再冲突（同为 ∝1/尺度）；**真正的问题是无局域支撑**，与 r354 G06（p=0 平面波平移简并、R 是积分常数）**跨卷独立印证**。"
    u"★★★**修正二（G02 判别力）**：局域化残差 ‖R‖² = ħ²‖∇f‖²(ψ†ψ)，**只含 ψ†ψ，不含 η、螺旋、zitterbewegung**；"
    u"5 类旋量（V28 叠加型/纯正频/纯负频/复旋量/纯手征）的残差归一化因子全为 1，而它们的结构指纹 j¹/(ψ†ψ) 给出 **4 个互异值**（0、1、24/25、4/9）"
    u"⇒ 指纹有判别力而残差没有 ⇒ **第二节对 V28 的双螺旋构造零判别力**（对任何常数旋量同值，属教科书级显然）。"
    u"残差两口径并列：动量口径 4.583e-20 J·s/m，能量口径 85.76 MeV（a=r_e=2.8179e-15 m，对应来料的「数十 MeV」）。"
    u"★★★**修正三（G04 适用域 + 换族稳健）**：换电荷分布为指数族后自能系数由 1/√(2π)=0.39894 变为 5/32=0.15625（解析 vs 数值差 5.9e-14），**仍 ∝1/a**"
    u"⇒ 与 1/x 型动能相加仍严格递减 ⇒ **「无有限极小」对试探族稳健**（加强来料）；"
    u"对照：加入束缚项 0.01·x² 后同一扫描器立刻在 x=2.8 找到极小 ⇒ 检测器有双向判别力。"
    u"⇒ **适用域 = 「正动能 + 正 1/a 自排斥」这一模型类**，不可外推到完整 Maxwell–Dirac。"
    u"★**判决五条 FAIL**：G01 口径 / G02 残差零判别力 / G06 引力需放大 **4.17e42 倍**（m* = √(αħc/G) = 1.859e-9 kg = 2.04e21 m_e）/"
    u"G07 未关闭 r354 的 X-R354-1 与 X-R354-2（**0/2**；X-R354-2 甚至未被触及：残差非零 ≠ 流线不是螺旋，两个不同命题）/"
    u"G08 来料自陈两项 0/2 闭合。"
    u"★**文献核实（卷外，不计入引擎条目）**：来料自陈「Maxwell–Dirac 存在局域驻定孤立波」经核实**属实且更强** —— "
    u"Esteban–Georgiev–Séré (1996, Calc. Var. PDE 4:265–281) 证明 (3+1) Minkowski 中存在**正则、时间驻定、空间局域**的 soliton-like 解；"
    u"Abenda (1998) 扩展到 ω∈]-m,m[；Pan–Ding–Wang (2022) 给出周期→孤子型解与基态。"
    u"⇒ ROOT 下一关不是「求存在性」而是「这些解的自旋、磁矩、耦合是否落在电子上」。"
    u"★**定价** 2^5=32 ⇒ 五槽（局域解/有限能量/稳定半径/自旋磁矩/耦合内生）本轮满足 **0/5**，全真组合 1、翻转 S3 后 0 ⇒ **不占度，候选 37，链止 r264:36**。"
    u"★**OPEN**：`X-R354-1`（部分推进未关闭）/ `X-R354-2`（未触及）/ `X-R354-3`（未触及）/ "
    u"新开 `X-R360-1`（已有 MD 驻定解的自旋磁矩是否落在电子值）/ `X-R360-2`（其线性稳定性与散射）/ `X-R360-3`（耦合是否由几何内生）。"
    u"**下轮从 r361 起（并行链极活跃：取号前必扫三树 + README 两树；大文件动手前先写 `_probe_rN.py` 占位）。**"
)

PAN_LINE = (
    u"├── 判定_TUFT-r360_ROOTV29_DiracMaxwell自洽性_均匀解场能口径修正_局域化残差对螺旋零判别力_试探族单调稳健_2026-11-02.md"
    u"  # 新增（**r360 · 2026-11-02**）：ROOT V29 判定册（**数学全对、三条修正、适用域限定**）—— "
    u"§来料四条主张与本卷裁定 · §复算（场能闭式 / **静电自能三路径 8.2e-17 与 5e-59** / 试探表 6 组按列容差 / 单调性 dF=-0.8599、dG=-2.911e-3 / "
    u"α_G 与比值 / **5000 组精确 Fierz 违例 0** / ansatz j_z=ℓ+1/2 一致）· "
    u"§修正一 口径（**孤立电子口径下 U = αħc/(10L) ∝1/L 不发散**；两口径趋势相反表；与 r354 G06 跨卷印证）· "
    u"§修正二 判别力（残差 = ħ‖∇f‖ 对螺旋零判别力；5 类旋量残差同值而指纹 4 异）· "
    u"§修正三 适用域（换指数族系数 5/32 仍 ∝1/a ⇒ 稳健；加束缚项 λx² 后 x=2.8 出现极小 ⇒ 对照成立）· "
    u"§引力量化（放大 4.17e42 倍、m* = 1.859e-9 kg）· §判决表九条机读 · "
    u"§**文献核实（卷外）**：Esteban–Georgiev–Séré 1996 / Abenda 1998 / Pan–Ding–Wang 2022 ⇒ 来料的诚实边界有文献支撑，"
    u"但那些是经典非线性 Dirac 场的驻定解，是否描述电子未被定理回答 · "
    u"§定价（0/5 不占度）· §OPEN 推进台账（X-R354-1/2/3 与 X-R360-1/2/3）· §终审判词（**V29 精确排除了三条走不通的路，"
    u"但没有走出一条能走的路；能走的路在文献中已经存在，下一关是自旋、磁矩与耦合**）· §诚实边界 · §产物真链接。**下轮从 r361 起。**"
)


def main():
    with open(README, "r", encoding="utf-8") as f:
        old = f.read()

    if u"TUFT-r360_" in old:
        print("SKIP: r360 already registered")
        return

    if not os.path.exists(BAK):
        shutil.copy2(README, BAK)
        print("BAK created:", BAK)

    old_lines = old.split("\n")
    new_lines = []
    n_src = 0
    n_pan = 0
    for ln in old_lines:
        new_lines.append(ln)
        if ln.startswith(SRC_ANCHOR):
            new_lines.append(SRC_LINE)
            n_src += 1
        elif ln.startswith(PAN_ANCHOR):
            new_lines.append(PAN_LINE)
            n_pan += 1

    assert n_src == 1, "src anchor hit %d" % n_src
    assert n_pan == 1, "pan anchor hit %d" % n_pan

    c_old = Counter(old_lines)
    c_new = Counter(new_lines)
    missing = {k: (v, c_new.get(k, 0)) for k, v in c_old.items() if c_new.get(k, 0) < v}
    assert not missing, "DELETION DETECTED: %r" % missing
    assert len(new_lines) == len(old_lines) + 2, "line count %d vs %d" % (len(new_lines), len(old_lines))

    with open(README, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))

    with open(README, "r", encoding="utf-8") as f:
        chk = f.read()
    assert chk.count(u"│   ├── TUFT-r360_ROOTV29") == 1, "src verify fail"
    assert chk.count(u"├── 判定_TUFT-r360_ROOTV29") == 1, "pan verify fail"
    print("REG-OK: src=1 pan=1 lines=%d(+2) deletions=0" % len(new_lines))


if __name__ == "__main__":
    main()
