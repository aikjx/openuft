# -*- coding: utf-8 -*-
"""r374 README 双锚点登记（幂等 / 零删除 / 写后读回验证）。

纪律：
  · 锚点串含本卷 RID（`TUFT-r374_` / `判定_TUFT-r374_`），先判存在再分流；
  · 源码树插在 `│   ├── TUFT-r370_` 之**后**（保持近邻时序），判定列表**追加末尾**；
  · README 原结尾无换行 ⇒ 追加会把「无尾换行」变成「有尾换行」，diff 会报 1 条伪删除：
    判法用 `new.count(备份末行) == 1`，而不是看 diff 的 +-。
"""
import io, os, shutil, sys

ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
README = os.path.join(ROOT, "README.md")
BAK = os.path.join(ROOT, "scratch", "_bak_README_pre_r374.md")

SRC_ANCHOR = "│   ├── TUFT-r370_"
JUD_ANCHOR = "├── 判定_判定_TUFT-r374_"   # 注意双前缀：目录里的文件名本身就叫 判定_判定_…
SRC_KEY = "│   ├── TUFT-r374_"

FN = ("TUFT-r374_审计ROOTV30V31_Dirac概率流与V30-2闭合式重言性定价_"
      "四力运动学机核与Raychaudhuri双实例实算_精算与可视化_2026-11-02.py")

SRC_LINE = (
    "│   ├── " + FN + "  # 新增（**r374 · 2026-11-02**）："
    "**审计 ROOT V30（Dirac–Coulomb 概率流 / V30-2「几何—能量闭合式」）与 ROOT V31（四力运动学）**"
    "（条目 **23**：PASS 20 / INFO 3 / FAIL 0；控制组 **6/6**、守卫 **10/10**、退出码 0、`ALL-GATES-PASS`）。"
    "★**V30-1 严格成立**：j = ρcZα sinθ φ̂ 在 30 个 (θ,φ) 网格上 4×4 Dirac α 矩阵直算 vs 闭式最大相对偏差 **8.30e-60**，"
    "Dirac 径向方程组 5 个 r 点残差 **3.90e-59**；承重消去 2q/(1+q²)=Zα 需 γ²+(Zα)²=1，把 γ 扰成 γ′=0.99γ ⇒ 偏差 **5.02e-3**（有判别力）。"
    "**独立交叉验证（自算，非引用）**：把该电流积分成磁矩得 g = 2(1+2γ)/3 = **1.999964498624373**"
    "（Simpson+Richardson 比值 **1.499973373968280** vs Γ 函数整数移位闭式 **1.499973373968303**，rel **1.57e-14**），"
    "g−2 = **−3.5501e-5** ≈ −(2/3)α² = −3.5501e-5；s→0 时 g→2 是本卷自己算出的极限。"
    "★★★**V30-2 是定义级重言式**：v_max/c = Zα 与 E₁ₛ/(m_ec²) = √(1−(Zα)²) 由**同一个** Zα 参数化 ⇒ 六档（1e-8/α/0.1/0.5/0.9/0.99）残差 **5e-60**，"
    "对 Zα 判别力 **0**；判别力定价：换 Schrödinger 能量 ⇒ 残差 = (Zα)⁴/4 = **7.0893e-10**（闭式 vs 流水线 rel 0、放大 > 1e40），"
    "v_max 扰动 1e-3 仅 **1.07e-7**（被 (Zα)² = 5.325e-5 压制 1.9e4 倍）⇒ 任何「1% 级吻合」在此式上零价格。"
    "★**巧合尺**：由 (c, α, ħ, m_e) 造 L/T 的单项式解共 6 个、其中 α 一阶唯一 1 个 = αc ⇒ Bohr 轨道速度 / Schrödinger ⟨v²⟩^½ / 概率流最大速率"
    "**在量纲层被迫相等**，「v_max 与轨道速度相符」判别力 0。"
    "★**V31 技术层全对**：∇·v=0、∇×v=2Ω、a=−Ω²r（FD 偏差 0）；Cornell/Yukawa 求导 **1.13e-19**；λ_π = **1.4138169** fm；"
    "四力 1 fm 表 max rel **2.65e-6**（引力差为 G 不确定度的 0.118 倍）；λ_W = **2.455531e-18** m（rel 1.27e-5）；"
    "回旋 κ/|τ| = 2.000000（参数曲线独立定义 vs 闭式 rel 5e-60）。"
    "★★**本卷新产出 1（散度对偶）**：v 场**有旋无散**、a 场**有散无旋**（∇·a = **−5.78** = −2Ω²、∇×a = 0、a = −∇(Ω²R²/2)）"
    "⇒ V31 否证的是「用**速度场**的散度当力」，不是散度本身。"
    "★★**本卷新产出 2（Raychaudhuri 双实例）**：①把 V31 自己的螺旋场升为 u^μ = Γ(1,−Ωy,Ωx,u)，实算 Θ≡0（邻域 **2.82e-27**）、σ²、ω²、∇_μa^μ，"
    "方程右端 **1.88e-24**，并得新闭式 **σ²−ω² = −2Ω²Γ² − 2Ω⁴Γ⁴R²**（4 点 rel **7.25e-23**；Γ→1、R→0 退化为 −2Ω²；"
    "末项是**相对论新增的剪切** —— 刚性旋转一旦带上 Γ(R) 就不再刚性）；②FLRW 共动观测者 p=2/3、t=2：R_tt = 1/6、Θ = 1、dΘ/dτ = −1/2，"
    "残差 **1.33e-17**，自写数值 Ricci 在 Minkowski 球坐标 **2.52e-17** / Schwarzschild **8.04e-18** 自检（非恒零）。"
    "★**唯一实质缺陷**：Cornell 的 1.56842e5 N 只能在**未声明**的 k = (4/3)α_sħc = **78.9308** MeV·fm 下复现；"
    "取 k = α_sħc = 59.1981 同一公式给 **1.53680e5** N，差 **2.0157e-2** ⇒ 该数字含一个未声明的色因子 4/3。"
    "★**满射定价**：v_⊥/|u| 换成 1000 比值跟着变 1000（rel 1.7e-59）⇒ 自由无量纲参数满射，不锁定任何常数（含 α），判别力 0。"
    "★★★**自伤登记（家族第六卷）**：①Raychaudhuri 实例一残差首跑 **3.83e-2** 且**不随差分步长 h 收敛** ⇒ 用纯运动学恒等式 "
    "(∇_μu_ν)(∇^νu^μ) = Θ²/3+σ²−ω² 定位到**投影算符上下标写反**（h_μ^α = δ^α_μ + u^α u_μ 写成 u^μ u_α，`uup[i]*ulo[j]` 应为 `uup[j]*ulo[i]`）"
    "⇒ Dd_μν 非 u-正交（差 8.14e-2）；**该错在 FLRW 共动观测者上完全不显现**，只在非共动的螺旋联络暴露 ⇒ 修正后 **1.88e-24** / **7.25e-23**；"
    "②`add()` 首版不读 ok ⇒ 出现 2 条「ok=False 却标 PASS」（P20/P21），已加硬约束「ok 为假一律降级 FAIL」；"
    "③P06 门限写 1e-9 而读数恰是 7.0893e-10 ⇒ 自伤 FAIL，改法不是挪 10 的幂，而是换成**闭式 vs 流水线的独立路径比对**；"
    "④HTML 里 `for(var m=)` 与体检器 `_check_html_geom.js` 模块级 `let m;` 在 eval 同作用域冲突 ⇒ 循环变量改 `mi`（改生成器，不只改产物）。"
    "★**取号**：r369 四件套由并行会话 08:02:04 完成（其源码 08:02:45 更晚）⇒ 本卷让号；r370 亦已被占（仅有探针）⇒ 取冷号 **r374**（邻 r373/r375 两树皆空）；"
    "大文件动手前先写 `_probe_r374.py` 占位；改号一次做净（文件名 + RID + 首行注释 + runner），改后重跑核对读数不变。"
    "★**定价 0/5 不占度**（五槽全为复算/定价，无锁定常数的新约束），度数链维持 **36（r264 止）**，本卷记「候选 37」。"
    "★**供给 0**：23 条**不可与 r354/r360/r365/r368/r370 相加**（分层铁律）。"
    "★**OPEN**：`X-R374-1`（电流在 Zα→1 强场是否仍成立，本卷只在 α 上算）/ `X-R374-2`（∇·a = −2Ω² 能否升级为场方程）/ "
    "`X-R374-3`（−2Ω⁴Γ⁴R² 剪切是否对应可测潮汐）。"
    "**HTML 几何体检 GEOMETRY-OK + 两负控（width:0 ⇒ 4 条、x=1205 越界 ⇒ 1 条，均 rc=2）。下轮从 r375 起。**"
)

JUD_FN = ("判定_判定_TUFT-r374_审计ROOTV30V31_Dirac概率流与V30-2闭合式重言性定价_"
          "四力运动学机核与Raychaudhuri双实例实算_2026-11-02.md")

JUD_LINE = (
    "├── " + JUD_FN + "  # 新增（**r374 · 2026-11-02**）：ROOT V30 + V31 判定册 —— "
    "§一 结论摘要（V30-1 成立 / V30-2 重言 / V31 技术全对 / 一处未声明口径）· §二 主册 23 行 · §三–§七 数据表"
    "（控制组、守卫、来料 1 fm 数值对拍、**V30-2 判别力定价表**、**Raychaudhuri 双实例实算表**）· "
    "§八 控制组与守卫 · §九 定价与供给 · §十 **取号与自伤登记（四项，含投影算符上下标错）** · §十一 OPEN 与诚实边界 · "
    "§十二 产物真链接（**字节数为写盘实测**，md/判定 用不动点迭代自洽，Windows CRLF 已计入）。"
    "**判词** `V30-1-VERIFIED--V30-2-TAUTOLOGICAL-ZERO-DISCRIMINATION--V31-MATH-VERIFIED-ONE-UNDECLARED-CONVENTION`；"
    "**终态** `ALL-GATES-PASS`。**分层**：只覆盖 V30/V31 两份来料，不复算 r354/r360/r365 的既有条目，条目不可相加。"
    "**治理**：靶只读、未改 `verify.py`、未 git；**下轮从 r375 起**。"
)


def main():
    s = io.open(README, encoding="utf-8").read()
    old_len = len(s)
    last_line = s.rstrip("\n").split("\n")[-1]

    if not os.path.exists(BAK):
        os.makedirs(os.path.dirname(BAK), exist_ok=True)
        shutil.copy2(README, BAK)
        print("BACKUP created:", os.path.basename(BAK))
    else:
        print("BACKUP exists, keep:", os.path.basename(BAK))

    # ---- 源码树：插在 r370 之后 ----
    if SRC_KEY in s:
        print("SKIP src (anchor exists, idempotent)")
    else:
        lines = s.split("\n")
        idx = [i for i, L in enumerate(lines) if L.startswith(SRC_ANCHOR)]
        assert len(idx) == 1, ("src anchor 命中数 != 1", idx)
        lines.insert(idx[0] + 1, SRC_LINE)
        s = "\n".join(lines)
        print("INSERT src after line", idx[0] + 1)

    # ---- 判定列表：追加末尾 ----
    if JUD_ANCHOR in s:
        print("SKIP jud (anchor exists, idempotent)")
    else:
        if not s.endswith("\n"):
            s += "\n"
        s += JUD_LINE
        print("APPEND jud at EOF")

    io.open(README, "w", encoding="utf-8", newline="\n").write(s)

    # ---- 写后读回验证（锚点必须带位置前缀，否则「判定_判定_...」会把两个锚点算成一个）----
    t = io.open(README, encoding="utf-8").read()
    c_src = t.count("│   ├── TUFT-r374_")
    c_jud = t.count("├── 判定_判定_TUFT-r374_")
    print("bytes %d -> %d (+%d)" % (old_len, len(t), len(t) - old_len))
    print("src anchor count = %d (expect 1)" % c_src)
    print("jud anchor count = %d (expect 1)" % c_jud)
    print("last_line preserved =", t.count(last_line) == 1)
    print("no trailing blank   =", not t.endswith("\n\n"))
    assert c_src == 1 and c_jud == 1, (c_src, c_jud)
    assert t.count(last_line) == 1, "备份末行被破坏 ⇒ 触发了伪删除"
    return 0


if __name__ == "__main__":
    sys.exit(main())
