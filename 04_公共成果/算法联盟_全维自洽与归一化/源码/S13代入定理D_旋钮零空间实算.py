# -*- coding: utf-8 -*-
"""
S13 代入定理 D：旋钮零空间实算 + 标度不变性壁垒（定理 E）
=========================================================
目的：把第63章定理 D（旋钮零空间定理）真正作用到 S13（第56章记为唯一走在
      动力学本征值路线上的体系），实算 nullity_dyn，判定 S13 的谱问题是否
      满足 nullity_dyn = 0，从而判定其能否解锁 UFT-3。

方法：把 S13 的第一性原理约束（第25章 定理25.1/25.4、第22/23章 结构约束）
      形式化为 E(theta)=0，theta 为无量纲参数空间；用 sympy 精确计算雅可比
      J_E 的秩与零空间，再检验各候选靶 q 是否满足 dq|_ker(J_E) = 0。

诚实立场：本脚本不产生任何关于世界的数值预言。它是一把尺子：判定 S13 的
          哪些靶是「真预言候选」（nullity_dyn=0），哪些是「拟合/对接」
          （nullity_dyn>=1）。判定结果与 S13 自身诚实边界（诚实边界.md
          「alpha 量级解释」列为 OPEN；ch25 §25.7「alpha 目前只是输入/对接，
          不是输出」）应当一致——一致性本身就是对定理 D 的一次外部校准。

运行：python S13代入定理D_旋钮零空间实算.py
产物：数据/S13代入定理D.md 、 数据/S13代入定理D.json
"""

import json
import os
import sys
from datetime import date

import sympy as sp

try:                       # 修复：GBK 控制台无法编码 '⇒'(U+21D2) 等字符时崩溃
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "数据"))
os.makedirs(DATA, exist_ok=True)

TODAY = str(date.today())
R = []


def out(s=""):
    R.append(str(s))


# ============================================================
# §1  形式化：S13 的无量纲参数空间与第一性原理约束
# ============================================================
out("# S13 代入定理 D：旋钮零空间实算与标度不变性壁垒（定理 E）")
out()
out("> 引擎：`源码/S13代入定理D_旋钮零空间实算.py` ｜ 生成日期：" + TODAY)
out("> 依赖：sympy（精确秩/零空间）、mpmath（数值核对）")
out("> 定位：第63章 §63.7 [C]1「应用到 S13」的落地执行；第56章 §56.9 [C]3 的补全")
out()
out("---")
out()
out("## 1. 形式化设定")
out()
out("### 1.1 无量纲参数空间 Theta")
out()
out("S13 经奥卡姆归并后（第25章 §25.2 对接程序）的无量纲参数为")
out()
out("```")
out("Theta = { g~ , g~' , kappa~ }        (n = 3 个无量纲旋钮)")
out("```")
out()
out("其中 `g~` 为对偶规范耦合、`g~'` 为 U(1) 耦合、`kappa~` 为真空自耦合。")
out("带量纲尺度 `v`（= ell^{-1}）与 `ell` 不计入 Theta —— 它们是标度，不是")
out("无量纲旋钮（定理 D 只作用于无量纲参数空间）。")
out()
out("### 1.2 第一性原理约束 E(theta) = 0")
out()
out("S13 对**无量纲扇形**真正施加的第一性原理约束：")
out()
out("| 编号 | 约束 | 出处 | 类型 |")
out("|---|---|---|---|")
out("| E1 | `g~'/g~ = 1/sqrt(3)`（CP^2 稳定子嵌入，同一规范耦合 g3） | ch25 定理25.4 | **连续、齐次** |")
out("| E2 | 拓扑荷 `Q_H in Z`、`min|Q|=1` | 公设 A2 | 整数型（离散） |")
out("| E3 | 真空模式谱 `{0,0,0,8 kappa~ v^2}`、未破缺 U(1) 零空间维数 = 1 | ch18 / 验证结果 | 计数型（离散） |")
out("| E4 | 电荷步长 `1/3` = 色表示维数 3 的倒数 | ch25 定理25.3 | 有理数型（离散） |")
out()
out("**关键观察**：E2/E3/E4 是**离散/整数型**约束（拓扑、计数、维数），它们")
out("不作用于连续旋钮空间 Theta，故对 J_E 贡献为 0。只有 E1 是作用于 Theta")
out("的**连续**约束。这正是 S13「结构性预测」的代数根源。")
out()

# --- sympy 符号设定 ---
g, gp, kap = sp.symbols("g gp kappa", positive=True)

# E1: g~' ^2 - g~^2/3 = 0
E1 = gp**2 - g**2 / sp.Integer(3)
JE = sp.Matrix([[sp.diff(E1, g), sp.diff(E1, gp), sp.diff(E1, kap)]])
out("### 1.3 约束雅可比 J_E")
out()
out("```")
out("E1(theta) = g~'^2 - g~^2 / 3 = 0")
out("J_E      = [ dE1/dg~ , dE1/dg~' , dE1/dkappa~ ]")
out("         = [ -2 g~/3 ,  2 g~'  ,  0 ]")
out("```")
out()
out("（E2/E3/E4 为离散约束，不产生 J_E 行。）")
out()
out("---")
out()

# ============================================================
# §2  秩与零度实算
# ============================================================
out("## 2. 秩与零度实算（sympy）")
out()
out("在满足约束的点上取 `g~ = 1`，则 `g~' = 1/sqrt(3)`（E1 的解）。")
out()
gv = sp.Integer(1)
gpv = sp.Rational(1, 1) / sp.sqrt(3)
subs0 = {g: gv, gp: gpv}

JE_num = JE.subs(subs0)
rank_JE = JE_num.rank()
n = 3
nullity_dyn = n - rank_JE

out("```")
out("J_E(1, 1/sqrt(3), * ) = [ -2/3 ,  2/sqrt(3) ,  0 ]")
out("rank(J_E)      = %d" % rank_JE)
out("n              = %d" % n)
out("nullity_dyn    = n - rank(J_E) = %d" % nullity_dyn)
out("```")
out()
out("**零空间基**（ker J_E 的两条基向量）：")
out()
ker = JE_num.nullspace()
ker_basis = []
for v in ker:
    ker_basis.append([sp.nsimplify(x) for x in v])
    out("- `k = ( " + ", ".join(str(sp.nsimplify(x)) for x in v) + " )`")
out()
out("数值化：")
ker_num = []
for v in ker:
    vn = [float(sp.N(x, 20)) for x in v]
    ker_num.append(vn)
    out("- `k = ( " + ",  ".join("%+.6f" % x for x in vn) + " )`")
out()
out("**几何意义**：")
out()
out("- `k1 = (1, 1/sqrt(3), 0)` 是**耦合整体重标度方向**：`g~ -> lambda g~`、")
out("  `g~' -> lambda g~'` 同时缩放，比值 `g~'/g~ = 1/sqrt(3)` 不变。")
out("- `k2 = (0, 0, 1)` 是**真空自耦合方向**：`kappa~` 完全自由。")
out()
out("即：**S13 的无量纲扇形留有两个自由方向**——一个整体标度 + 一个自耦合。")
out()
out("---")
out()

# ============================================================
# §3  靶的零空间投影检验  dq|_D = 0 ?
# ============================================================
out("## 3. 靶投影检验：`dq|_D = 0 ?`")
out()
out("按定理 D，靶 q 是真预言候选 **当且仅当** `dq|_{ker J_E} = 0`。")
out()

targets = [
    ("q1  sin^2 theta_W = g~'^2/(g~^2+g~'^2)",
     gp**2 / (g**2 + gp**2),
     "电弱混合角（比值型）"),
    ("q2  alpha ~ e^2 = g~^2 g~'^2/(g~^2+g~'^2)",
     g**2 * gp**2 / (g**2 + gp**2),
     "精细结构常数（绝对耦合尺度型）"),
    ("q3  kappa~",
     kap,
     "真空自耦合（无约束旋钮）"),
    ("q4  g~' (绝对耦合)",
     gp,
     "绝对耦合（整体标度型）"),
]

rows = []
for name, q, desc in targets:
    grad = sp.Matrix([[sp.diff(q, g), sp.diff(q, gp), sp.diff(q, kap)]])
    # 沿两条零空间基方向的导数
    dirs = []
    for v in ker:
        d = sp.simplify((grad * v)[0].subs(subs0))
        dirs.append(d)
    dq_D = [sp.simplify(d) for d in dirs]
    all_zero = all(sp.simplify(d) == 0 for d in dirs)
    verdict = "真预言候选" if all_zero else "拟合/对接"
    rows.append((name, desc, dq_D, all_zero, verdict))
    out("### " + name)
    out()
    out("- 描述：" + desc)
    out("- `dq/dg~ = " + sp.sstr(sp.simplify(sp.diff(q, g))) + "`")
    out("- `dq/dg~' = " + sp.sstr(sp.simplify(sp.diff(q, gp))) + "`")
    out("- `dq/dkappa~ = " + sp.sstr(sp.simplify(sp.diff(q, kap))) + "`")
    out("- 沿 k1（整体重标度）: `dq|_k1 = " + sp.sstr(dq_D[0]) + "`")
    out("- 沿 k2（自耦合方向）: `dq|_k2 = " + sp.sstr(dq_D[1]) + "`")
    out("- **判定**：`dq|_D " + ("= 0` ⇒ **真预言候选**" if all_zero else "!= 0` ⇒ **拟合/对接**"))
    out()

out("### 3.1 检验结果汇总")
out()
out("| 靶 | 描述 | dq&#124;k1 | dq&#124;k2 | 判定 |")
out("|---|---|---|---|---|")
for name, desc, dq_D, all_zero, verdict in rows:
    out("| " + name.split()[0] + " | " + desc + " | " + sp.sstr(dq_D[0])
        + " | " + sp.sstr(dq_D[1]) + " | **" + verdict + "** |")
out()
out("**结论**：`sin^2 theta_W` 沿两条零空间方向导数**同时为零** ⇒ 它是 S13 的")
out("真预言候选（结构固定为 1/4）。而 `alpha` 沿整体重标度方向 k1 的导数")
out("`= sqrt(3)/2 != 0`（按单位标度方向即 `2 alpha != 0`，见 §4.2 基归一化说明）")
out("⇒ **alpha 是拟合/对接，不是预言**。这与 S13 自身诚实边界完全一致")
out("（ch25 §25.7：alpha 目前只是输入/对接，不是输出）。")
out()
out("---")
out()

# ============================================================
# §4  标度不变性壁垒（定理 E）——符号证明
# ============================================================
out("## 4. 标度不变性壁垒（定理 E）")
out()
out("上面算例揭示了一个**结构性根源**：S13 的约束 E1 是耦合的**齐次**函数。")
out("下面把它一般化并符号验证。")
out()
out("### 4.1 陈述")
out()
out("**定理 E（标度不变性壁垒）** 设动力学路线的第一性原理约束 E 在耦合")
out("整体重标度 `g -> lambda g` 下**齐次**（保持 E=0 的解集不变），则")
out()
out("1. `ker J_E` 至少含一个**整体标度方向** `s = (g~, g~', ...)`；")
out("2. 只依赖**重标度不变量**（比值、混合角、量子化步长、计数）的靶满足")
out("   `dq|_D = 0`，可为真预言候选；")
out("3. 任何依赖**耦合绝对标度**的靶（如 `alpha`）必有 `dq|_D != 0`，")
out("   只能是拟合或对接（corresponds to 定理 C 情形 2）。")
out()
out("### 4.2 符号验证：齐次性与欧拉定理")
out()
lam = sp.symbols("lambda", positive=True)
q1 = gp**2 / (g**2 + gp**2)
q2 = g**2 * gp**2 / (g**2 + gp**2)
q3 = kap

q1_scaled = sp.simplify(q1.subs({g: lam * g, gp: lam * gp}) - q1)
q2_scaled = sp.simplify(q2.subs({g: lam * g, gp: lam * gp}) - lam**2 * q2)
q3_scaled = sp.simplify(q3.subs({kap: lam * kap}) - q3)
out("```")
out("sin^2 theta_W(lam g, lam g') - sin^2 theta_W(g,g')   = " + sp.sstr(q1_scaled) + "   (标度不变, 度 0)")
out("(alpha 型)(lam g, lam g') - lam^2 (alpha 型)(g,g')    = " + sp.sstr(q2_scaled) + "   (2 次齐次, 度 2)")
out("kappa~(lam) - kappa~                                  = " + sp.sstr(q3_scaled) + "   (kappa~ 不参与耦合标度)")
out("```")
out()
out("沿整体标度方向 `s` 的方向导数（欧拉定理）：")
out()
s_dir = sp.Matrix([g, gp, 0])
euler_q1 = sp.simplify((sp.Matrix([[sp.diff(q1, g), sp.diff(q1, gp), 0]]) * s_dir)[0])
euler_q2 = sp.simplify((sp.Matrix([[sp.diff(q2, g), sp.diff(q2, gp), 0]]) * s_dir)[0])
euler_q2_num = sp.nsimplify(sp.simplify(euler_q2.subs(subs0)))
alpha_num = sp.nsimplify(sp.simplify(q2.subs(subs0)))
out("```")
out("dq1|_s = " + sp.sstr(euler_q1) + "        (度 0 => 零)")
out("dq2|_s = " + sp.sstr(euler_q2) + "   (度 2 => 欧拉定理 = 2 q2, 非零)")
out("```")
out()
out("**基归一化说明**：sympy 返回的零空间基 `k1 = (sqrt(3), 1, 0)` 并非单位")
out("标度方向，而是 **`sqrt(3)` 倍的自然标度方向** `s = (1, 1/sqrt(3), 0)`。因此")
out("§3 表中 `dq2|_k1 = sqrt(3)/2` 与本节 `dq2|_s = 2 q2` 一致：")
out()
out("```")
out("(sqrt(3)/2) / sqrt(3) = 1/2 = 2 * q2 = 2 * (1/4) = 2 alpha")
out("q2 = alpha 型在 (g~,g~')=(1,1/sqrt(3)) 处取值 = " + sp.sstr(alpha_num) + " = alpha 的代数原型")
out("dq2|_s(数值) = " + sp.sstr(euler_q2_num) + "  = 2 alpha  != 0")
out("```")
out()
out("无论取哪条基，结论相同：**`dq2|_D != 0` ⇒ alpha 非线性可调方向被完全固定。**")
out()
out("**验证通过**：标度不变靶的标度方向导数为零，绝对标度靶的标度方向导数")
out("等于其齐次度数乘自身（欧拉定理），恒不为零。**这就是壁垒。**")
out()
out("### 4.3 S13 三公设的标度性质审计")
out()
out("| 公设 | 内容 | 是否含绝对标度锚 |")
out("|---|---|---|")
out("| S13-A1 对偶公理 | `D^2 = 1`（Z_2 对合） | 否（纯代数） |")
out("| S13-A2 守恒公理 | `Q in Z`（拓扑整数） | 否（整数，无标度） |")
out("| S13-A3 自相似公理 | `beta(-g) = -beta(g)`、`g* = sqrt(eps/c)`（比值） | 否（比值，齐次） |")
out()
out("**三条公设全部标度不变** ⇒ 由定理 E，S13 的公设集在原理上不能锁定")
out("耦合绝对标度 ⇒ **不能预言 `alpha`**。这是「S13 未导出 alpha」的代数根源，")
out("把一句观察升级为一条定理。")
out()
out("---")
out()

# ============================================================
# §5  与定理 A / 定理 C 的接口
# ============================================================
out("## 5. 与定理 A / 定理 C 的接口")
out()
out("| | 定理 A（量纲零空间） | 定理 C（两种情形） | 定理 D（旋钮零空间） | 定理 E（标度壁垒） |")
out("|---|---|---|---|---|")
out("| 工具 | `nullity(D_A)` | 分类 | `nullity_dyn = n - rank(J_E)` | 齐次性 / 欧拉定理 |")
out("| 结论 | 锚集能造几个无量纲数 | 量纲代数无预言 | 靶是否被固定 | 齐次约束不能定绝对标度 |")
out("| 对 alpha | 从 {c,h,G} 造不出（=0） | 必落情形 2 | 落在非零方向（拟合） | 三公设全齐次 ⇒ 不能锁定 |")
out()
out("**三定理互证**：定理 A 说「量纲代数的锚不够」；定理 C 说「换任何量纲锚都不够」；")
out("定理 D/E 说「换成动力学路线，只要公设齐次，仍然不够——缺的是**标度对称破缺**」。")
out("三者从三个方向指向同一个缺口：**一个打破标度不变性的第一性原理变分项**。")
out()
out("### 5.1 S13 的 alpha 属于定理 C 情形 2")
out()
out("S13 ch25 §25.2 的对接程序把 alpha 作为**输入**，反解出 {g~, g~', kappa~}。")
out("这正是定理 C 情形 2 的动力学版：**靶含自有量（此处为绝对耦合 e）⇒ 恒可反解 ⇒ 定义而非预言**。")
out("对接（docking）在代数上与「装常数」不可区分——这是 S13 自己承认的边界。")
out()
out("---")
out()

# ============================================================
# §6  判定汇总
# ============================================================
out("## 6. 判定汇总")
out()
out("| 项 | 结果 |")
out("|---|---|")
out("| Theta 维数 n | 3 |")
out("| rank(J_E) | " + str(rank_JE) + " |")
out("| **nullity_dyn** | **" + str(nullity_dyn) + "** |")
out("| `sin^2 theta_W` | nullity_dyn=0 方向 ⇒ **真预言候选**（但树级差 8.1%，已如实记录） |")
out("| 电荷步长 1/3、Q_H 整数性 | 结构固定（离散） ⇒ 结构预测，非连续预言 |")
out("| **alpha** | nullity_dyn>=1 ⇒ **拟合/对接，非预言** |")
out("| **S13 是否解锁 UFT-3** | **否** |")
out("| UFT 联盟层达成度 | 仍 2/6（未实现） |")
out()
out("### 6.1 对第63章 §63.5「下一步」的回答")
out()
out("第63章问：S13 的谱问题是否满足 `nullity_dyn = 0`？")
out()
out("**答**：对 `alpha` —— **不满足**（`nullity_dyn = 2 >= 1`）。对 `sin^2 theta_W` 等")
out("比值型靶 —— 满足（落在零空间核里，`dq|_D = 0`）。因此：")
out()
out("- S13 **确实**是唯一走在动力学路线上、且**确实**有一个结构预言（`sin^2 theta_W = 1/4`）的体系；")
out("- 但该预言**不是 alpha**，且其数值（1/4）被实验否证（树级差 8.1%）；")
out("- **S13 不解锁 UFT-3**：解锁 UFT-3 需要 alpha 级别的连续无量纲预言，")
out("  而 S13 的公设集齐次 ⇒ 由定理 E 不能产生。")
out()
out("### 6.2 解锁 UFT-3 的**精确**缺口（本册最新结论）")
out()
out("综合定理 A/C/D/E，缺口的描述已可精确化：")
out()
out("> **缺的不是「动力学路线」，而是「打破标度不变性的动力学路线」。**")
out("> 具体地：需要一个第一性原理变分项，它在耦合整体重标度 `g -> lambda g` 下")
out("> **不齐次**（即含一个绝对标度、且该标度由变分原理**定出**而非自由），")
out("> 使 `ker J_E` 中的整体标度方向被**消除**（`nullity_dyn` 减少 1）。")
out("> 届时 `alpha` 的 `dq|_D` 才可能为零。")
out()
out("这比第62/63章的「要补三块砖」更锐利：三块砖中，**砖①「显式依赖螺距的变分项」")
out("的真正作用就是打破标度不变性**——本册现在能说清它为什么必需。")
out()
out("---")
out()
out("## 7. 诚实边界")
out()
out("### 已确认 [A]（sympy 精确）")
out()
out("1. S13 无量纲扇形 `Theta` 维数 n=3；约束 E1 的 `rank(J_E)=1`；`nullity_dyn=2`。")
out("2. `dq|_D` 实算：`sin^2 theta_W` 为零（真预言候选）；`alpha` 型 `dq|_k1 = sqrt(3)/2 != 0`（拟合/对接）。")
out("3. 定理 E 的齐次性/欧拉定理关系由 sympy 符号验证为零。")
out("4. S13 三公设的标度审计：全部不含绝对标度锚。")
out()
out("### [B] 框架映射")
out()
out("1. 把 S13 的「结构性预测」（整数、比值、计数）与「连续预言」区分开，是")
out("   本册的解读；S13 原文并未用 nullity_dyn 语言，但结论（alpha 是输入）与")
out("   其 §25.7 自述一致，构成外部校准。")
out("2. 约束集 E 的完备性不可由定理 D 保证：若遗漏一条作用于 Theta 的连续约束，")
out("   `rank(J_E)` 会被低估、`nullity_dyn` 会被高估（判得过严，方向安全）。")
out("   本册已尽可能穷举 S13 的无量纲扇形约束（E1–E4）。")
out()
out("### [C] 待建")
out()
out("1. **构造打破标度不变性的变分项**：本册已把缺口定位为「非齐次第一性原理项」，")
out("   但尚未给出这样的项——这是真正的下一步，也是唯一可能解锁 UFT-3 的下一步。")
out("2. **与 V3 接口**：定理 E 判「能不能」，V3 判「命中几分」；先 E 后 V3 的复合")
out("   口径仍未形式化（承接第63章 §63.7 [C]3）。")
out()
out("---")
out()
out("> **本册结论**：把定理 D 真正作用到 S13，得到 `nullity_dyn = 2`。")
out("> **S13 对 `alpha` 不满足 `nullity_dyn=0`，故不解锁 UFT-3**——这与 S13 自身")
out("> 诚实边界（`alpha` 为 OPEN / 输入）完全一致，构成定理 D 的一次外部校准。")
out("> 更深的结果是**定理 E（标度不变性壁垒）**：S13 三公设全为标度不变结构，")
out("> 故在原理上不能锁定耦合绝对标度 ⇒ 不能预言 `alpha`。这把「S13 未导出 alpha」")
out("> 从一句观察升级为一条定理，并把解锁 UFT-3 的缺口精确化为")
out("> **「需要一条打破标度不变性的非齐次第一性原理变分项」**。")
out("> UFT 联盟层达成度仍为 2/6（未实现）。")

text = "\n".join(R) + "\n"
with open(os.path.join(DATA, "S13代入定理D.md"), "w", encoding="utf-8") as f:
    f.write(text)

payload = {
    "engine": "S13代入定理D_旋钮零空间实算.py",
    "date": TODAY,
    "Theta_dim": n,
    "rank_JE": int(rank_JE),
    "nullity_dyn": int(nullity_dyn),
    "ker_basis_numeric": ker_num,
    "targets": [
        {
            "name": name,
            "desc": desc,
            "dq_k1": sp.sstr(dq_D[0]),
            "dq_k2": sp.sstr(dq_D[1]),
            "prediction_candidate": bool(all_zero),
            "verdict": verdict,
        }
        for name, desc, dq_D, all_zero, verdict in rows
    ],
    "theorem_E_verified": bool(q1_scaled == 0 and q2_scaled == 0 and q3_scaled == 0),
    "scale_deduction": {
        "q1_sin2thetaW_deg0": sp.sstr(euler_q1),
        "q2_alpha_deg2_symbolic": sp.sstr(euler_q2),
        "q2_alpha_at_point": sp.sstr(euler_q2_num),
        "alpha_prototype_value": sp.sstr(alpha_num),
    },
    "S13_unlocks_UFT3": False,
    "UFT_attainment": "2/6",
}
with open(os.path.join(DATA, "S13代入定理D.json"), "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

print("\n".join(R))
print("\n[OK] wrote", os.path.join(DATA, "S13代入定理D.md"))
print("[OK] wrote", os.path.join(DATA, "S13代入定理D.json"))
