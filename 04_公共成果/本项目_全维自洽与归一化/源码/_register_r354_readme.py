# -*- coding: utf-8 -*-
"""r354 README 登记（幂等，零删除守卫）"""

import os
import shutil

BASE = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
README = os.path.join(BASE, "README.md")
BAK = os.path.join(BASE, "README.md.bak_r354")

SRC_ANCHOR = u"│   ├── TUFT-r346_整数Newton系数是三行初等事实而非几何定理"
PAN_ANCHOR = u"├── 判定_TUFT-r346_整数Newton系数是三行初等事实而非几何定理"

SRC_LINE = (
    u"│   ├── TUFT-r354_ROOTV28_Dirac双光状手征电流_正能量本征与螺旋互斥_自由参数满射判别力零_精算与可视化_2026-11-01.py"
    u"  # 新增（**r354 · 2026-11-01**）：**ROOT V28 审计：Dirac 双光状手征电流、正能量本征与螺旋互斥、自由参数满射判别力零**"
    u"（条目 **35**：A 精确代数 10 / B 高精度几何 8 / G 判决 7 / C 对照 4 / ENGINE 5 / PRICE 1；"
    u"**数学层 18/18 PASS**、**判决层 7 FAIL**、**对照 4/4 PASS**、退出码 0）。"
    u"★**取号**：扫号见 r351 已被并行会话占用（ROOT V27 来料原件已落、源码未落 ⇒ 热区）⇒ 取冷号 **r354**，"
    u"大文件动手前先写 `_probe_r354.py` 占位，零改他人字节。★**与 r351 的分工**：r351 审 V27（三维螺旋 κ/τ 的观察者依赖、"
    u"内禀频率、半角动量、Dirac 磁矩）；本卷**只审 V28 新增层**，洛伦兹一项（G08）与 r351 同源，只复算不计新条目。"
    u"★★★**数学层全部复算通过**：Clifford 64 项 0 违例；Fierz `j·k=0`、`j²+k²=0` 在 **2000 组随机复旋量上精确零**（Fraction，"
    u"非浮点）；显式解 `i∂_zψ=γ⁰ψ` 经 `i·(±i)` 复数乘法实算 8 点 × 4 分量 0 失配；电流闭式 vs 直接矩阵乘积 100 组一致；"
    u"**螺旋几何三路径**（Frenet / 圆柱闭式 / 来料式）互不共享中间量，相对残差 &lt;1e−30；来料 70 位表 7 项复算最坏残差 6.1e−10"
    u"（**残差有结构**：只由 α 决定的 η 残差 1.1e−10，含 m_e、ħ 的量一致偏 6.1e−10 ⇒ 常数字典末位差异，非公式差异）。"
    u"★★★**判决一（G01 满射 ⇒ 判别力 0）**：κ/|τ| = tan2η 在 η∈(0,π/4) 上满射到 (0,+∞)；12 个互不相干正目标"
    u"（α、1、2、0.0073、π、137、1e6、4.669…）**命中 12/12**、残差 &lt;1e−30 ⇒ 一个自由无量纲参数拟合一个数，信息量为零"
    u"（与 r272 LW 判别力 0、r292 巧合尺同型）。对照 G02：ρ&lt;0 不可达 2/2 ⇒ 判据有边界，非恒绿。"
    u"★★★**判决二（G03 正能量本征 ⇒ 螺旋消失，与 α 严格互斥）**：ΔH = m_ec² sin2η；取 tan2η=α ⇒ ΔH = **3.7288 keV**、"
    u"负频权重 1.331e−5；反之要求能量本征 ΔH=0 ⇒ η∈{0,π/2} ⇒ κ=0、R=0 ⇒ **螺旋退化为直线，κ/|τ| 为 0/0 无定义** ⇒"
    u"**双向夹逼**：要螺旋必须正负频混合，要正能量本征就没有螺旋，α≠0 故严格不可达。代价曲线 ΔH(ρ)=m_ec²ρ/√(1+ρ²) 单调"
    u"（α⇒3.73 keV、0.1⇒50.8、1⇒361.3、2⇒457.1 keV）⇒ 看得见的螺旋要以与静质量同量级的能量不确定度为代价；"
    u"对照 G05（η=π/8 ⇒ 361.3 keV，显著异于 3.729）证明 ΔH 检测有判别力。"
    u"★★★**判决三（G06 非局域 ⇒ 「内部」无指称）**：该解是 p=0 平面波，j、k **与空间坐标无关**，5 个互异空间点零差异 ⇒"
    u"平移简并；流线充满全空间，**螺旋半径 R 来自积分常数而非解的尺度**，没有电子中心也就没有内部；"
    u"对照 G07（人为包络须判有梯度 4/4）。★**判决四 G09 参数计数**：自由 Dirac 方程含 (m_e,ħ,c) 不含 e ⇒"
    u"输入 1 个自由无量纲参数（η）对 1 个无量纲目标（α）⇒ 自由度 0。**判决五 G10 普遍性**：双光状结构是 Clifford 恒等式，"
    u"对纯正频/纯负频/纯手征/一般旋量 5/5、随机 2000/2000 成立 ⇒ 不挑电子、不携带 α。**判决六 G11 旧数新衣**："
    u"κ/|τ|=α ⟺ 概率流速度 |j|/j⁰ = α/√(1+α²)（相对差 α²/2 = 2.66e−5）⇒ 就是 Bohr 基态 v=αc 的再包装，非独立预言。"
    u"**判决七 G13**：来料自陈三项未完成（流线=真实组成物 / η 唯一 / 无电荷输入预测 α）**0/3 可闭合**。"
    u"★**两条 INFO**：G12 Ω_Z = 2m_ec²/ħ 恰是 2 倍康普顿频率（教科书 zitterbewegung，NUM 非 FIT，但与 α 正交）；"
    u"G14 匹配到相对 1e−9 只需 η 精确到 3.6e−12 rad 而 η 完全自由 ⇒ 精度不构成证据；G15 该态 ⟨Σ_z⟩=cos2η（自旋稀释 2.66e−5）"
    u"比实测反常磁矩 1.16e−3 小 44 倍 ⇒ 自由 Dirac 层内不可分辨（与 r351 磁矩审计同源，只报数）。"
    u"★**新增几何读数**：螺距/半径 = **861.0** ⇒ 该「内部螺旋」极细长，曲率半径比螺旋半径大四个量级。"
    u"★**定价** 2^5=32 ⇒ 五槽（局域化/正能量本征/洛伦兹标量/η 由动力学固定/含电荷输入）本构造满足 **0/5**，全真组合 1、"
    u"翻转 S4 后 0 ⇒ **不占度，候选 37，链止 r264:36**。★**遗留 OPEN**：`X-R354-1`（Dirac–Maxwell 反作用下能否不人为选 η 稳定到离散几何）/ "
    u"`X-R354-2`（局域化波包下流线是否仍为圆柱螺旋 —— 本卷「无内部」结论的唯一逃生路线）/ `X-R354-3`（正能量子空间内是否存在 κ≠0 的解，"
    u"本卷只在单参数族内判互斥）。★**诚实边界**：未做 Dirac–Maxwell 反作用、未做 FW/Newton–Wigner 位置算符对比（只引用未算）。"
    u"**下轮从 r355 起（并行链极活跃：取号前必扫三树 + README 两树；大文件动手前先写 `_probe_rN.py` 占位）。**"
)

PAN_LINE = (
    u"├── 判定_TUFT-r354_ROOTV28_Dirac双光状手征电流_正能量本征与螺旋互斥_自由参数满射判别力零_2026-11-01.md"
    u"  # 新增（**r354 · 2026-11-01**）：ROOT V28 判定册（**双光状电流是恒等式、螺旋与正能量本征互斥、比值满射判别力 0、"
    u"平面波无「内部」**）—— §来料四条主张与本卷裁定（(a)(b) 数学层严格成立；(c) 不构成预测；(d) 不成立/无指称）· "
    u"§数学层 18/18 PASS（Clifford / Fierz 2000 组精确零 / 显式解系数级实算 / 电流闭式 vs 矩阵乘积 100 组 / "
    u"螺旋三路径交叉 &lt;1e−30 / 70 位表 7 项复算 6.1e−10 且残差有结构）· §判决七条（**G01 满射 12/12 ⇒ 判别力 0** / "
    u"**G03 正能量互斥：ΔH=3.7288 keV vs ΔH=0⇒κ=0⇒0/0** / **G06 非局域：平移简并，R 是积分常数** / G09 参数计数自由度 0 / "
    u"G10 恒等式不挑电子 / G11 旧数新衣 v=αc / G13 自陈三项 0/3 可闭合）· §四条对照（G02 负目标不可达 / G05 η=π/8 时 ΔH=361.3 keV / "
    u"G07 人为包络须判有梯度 / G08b β=−cos2η 分母归零）· §两条 INFO（G12 Ω_Z=2×康普顿频率 / G14 条件数 / G15 磁矩不可分辨）· "
    u"§定价（五槽满足 0/5，全真 1、翻转 S4 后 0 ⇒ 不占度）· §终审判词（数学全对，物理不成立或无指称；把来料自陈升级为可算判决，"
    u"并额外给出两条来料未列的硬约束）· §诚实边界与 `X-R354-1/2/3` · §产物真链接。**下轮从 r355 起。**"
)


def main():
    with open(README, "r", encoding="utf-8") as f:
        old = f.read()

    if u"TUFT-r354_" in old:
        print("SKIP: r354 already registered")
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

    new = "\n".join(new_lines)
    # 零删除守卫：旧行多重集必须完全包含于新行
    from collections import Counter
    c_old = Counter(old_lines)
    c_new = Counter(new_lines)
    missing = {k: (v, c_new.get(k, 0)) for k, v in c_old.items() if c_new.get(k, 0) < v}
    assert not missing, "DELETION DETECTED: %r" % missing
    assert len(new_lines) == len(old_lines) + 2, "line count %d vs %d" % (len(new_lines), len(old_lines))

    with open(README, "w", encoding="utf-8") as f:
        f.write(new)

    # 写后读回逐键验证（键带位置前缀）
    with open(README, "r", encoding="utf-8") as f:
        chk = f.read()
    assert chk.count(u"│   ├── TUFT-r354_ROOTV28") == 1, "src verify fail"
    assert chk.count(u"├── 判定_TUFT-r354_ROOTV28") == 1, "pan verify fail"
    assert chk.endswith(old[-1:]), "tail byte changed"
    print("REG-OK: src=1 pan=1 lines=%d(+2) deletions=0" % len(new_lines))


if __name__ == "__main__":
    main()
