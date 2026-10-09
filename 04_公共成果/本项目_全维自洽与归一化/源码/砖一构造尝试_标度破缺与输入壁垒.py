# -*- coding: utf-8 -*-
"""
砖①的构造尝试：标度破缺变分项与输入壁垒（定理 F）
==================================================
目的：第64章 §64.7 把解锁 UFT-3 的缺口精确化为「一条打破标度不变性的
      非齐次第一性原理变分项」（即第62章「砖①」）。本轮**实际去构造它**，
      并用定理 D 的雅可比秩工具检验：构造出来的砖①能否把 alpha 的
      dq|_ker(J_E) 变成零。

核心发现（诚实）：
  砖① 确实能杀死「长度扇区」的整体标度方向，但由于 J_E 在
  「几何扇区 ⊗ 耦合扇区」上**块对角**，它**碰不到耦合扇区**，
  alpha 的 dq|_ker 仍不为零 ⇒ **砖① 必要但不充分**。
  要真正锁定 alpha，必须施加一条**非齐次的耦合约束**，而它的系数
  只能来自三类来源（实测值 / 结构数 / 另一本征值），逐一排除后
  得到**定理 F（输入壁垒）**。

方法：sympy 精确秩/零空间；连分数与最佳有理逼近做定量检验。

运行：python 砖一构造尝试_标度破缺与输入壁垒.py
产物：数据/砖一构造尝试.md 、 数据/砖一构造尝试.json
"""

import json
import os
from datetime import date
from fractions import Fraction

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "数据"))
os.makedirs(DATA, exist_ok=True)
TODAY = str(date.today())
R_OUT = []


def out(s=""):
    R_OUT.append(str(s))


# ============================================================
# 形式化设定
# ============================================================
Rm, b, g, gp = sp.symbols("R b g gp", positive=True)
ell, R0, c0 = sp.symbols("ell R0 c", positive=True)

# 四旋钮：几何扇区 (R,b) + 耦合扇区 (g,gp)
COLS = [Rm, b, g, gp]
COLNAMES = ["R (螺旋半径)", "b (螺距)", "g~ (对偶规范耦合)", "g~' (U(1) 耦合)"]

# 靶
alpha_couple = g**2 * gp**2 / (g**2 + gp**2)          # 真 alpha 的代数原型（耦合型）
alpha_geo = Rm / sp.sqrt(Rm**2 + b**2)                # ch62 的 sin(theta)（几何比值型）

# 约束
E_couple = gp**2 - g**2 / sp.Integer(3)               # 结构约束（耦合，齐次）
E_pitch = b - ell                                     # 砖①：绝对标度（几何，非齐次）
E_radius = Rm - R0                                    # 第二条绝对标度（几何，非齐次）
E_couple_abs = g - c0                                 # 非齐次耦合约束（需外界输入）

# 数值化点
PT = {Rm: sp.Integer(1), b: sp.Integer(1), ell: sp.Integer(1),
      R0: sp.Integer(1), c0: sp.Integer(1), g: sp.Integer(1),
      gp: 1 / sp.sqrt(3)}


def jacobian(es):
    return sp.Matrix([[sp.diff(e, v) for v in COLS] for e in es])


def analyze(es, label):
    J = jacobian(es)
    Jn = J.subs(PT)
    rk = Jn.rank()
    ker = Jn.nullspace()
    nullity = len(COLS) - rk
    rows = []
    for name, q in (("alpha_couple", alpha_couple), ("alpha_geo", alpha_geo)):
        grad = sp.Matrix([[sp.diff(q, v) for v in COLS]])
        ds = [sp.nsimplify(sp.simplify((grad * v)[0].subs(PT))) for v in ker]
        rows.append((name, ds, all(d == 0 for d in ds)))
    return {"label": label, "J": J, "rank": rk, "nullity": nullity,
            "ker": ker, "targets": rows}


# ============================================================
# 输出
# ============================================================
out("# 砖①的构造尝试：标度破缺变分项与输入壁垒（定理 F）")
out()
out("> 引擎：`源码/砖一构造尝试_标度破缺与输入壁垒.py` ｜ 生成日期：" + TODAY)
out("> 依赖：sympy（精确秩/零空间）、fractions（连分数）")
out("> 定位：第64章 §64.7「构造打破标度不变性的变分项」的落地执行；第62章「砖①」的检验")
out()
out("---")
out()
out("## 1. 设定")
out()
out("四旋钮分两类扇区：")
out()
out("| 旋钮 | 扇区 | 含义 |")
out("|---|---|---|")
out("| $R$ | 几何 | 螺旋半径 |")
out("| $b$ | 几何 | 螺距 |")
out("| $\\tilde g$ | 耦合 | 对偶规范耦合 |")
out("| $\\tilde g'$ | 耦合 | $U(1)$ 耦合 |")
out()
out("两个靶：")
out()
out("- $\\alpha_{\\rm couple}\\propto \\dfrac{\\tilde g^{2}\\tilde g'^{2}}{\\tilde g^{2}+\\tilde g'^{2}}$ —— **真 $\\alpha$ 的代数原型**（耦合型，2 次齐次）")
out("- $\\alpha_{\\rm geo}=\\dfrac{R}{\\sqrt{R^{2}+b^{2}}}$ —— 第62章的 $\\sin\\theta$（几何比值型）")
out()
out("约束清单：")
out()
out("| 编号 | 约束 | 扇区 | 齐次性 |")
out("|---|---|---|---|")
out("| $E_{\\rm couple}$ | $\\tilde g'^{2}-\\tilde g^{2}/3=0$ | 耦合 | 齐次（2 次） |")
out("| $E_{\\rm pitch}$ | $b-\\ell=0$ | 几何 | **非齐次**（砖①） |")
out("| $E_{\\rm radius}$ | $R-R_0=0$ | 几何 | **非齐次** |")
out("| $E_{\\rm couple}^{\\rm abs}$ | $\\tilde g-c=0$ | 耦合 | **非齐次**（需外界输入） |")
out()
out("---")
out()

# ============================================================
# §2 分场景实算
# ============================================================
scenarios = [
    ([E_couple], "S0 现状：仅结构约束（第64章的基线）"),
    ([E_couple, E_pitch], "S1 加砖①：绝对螺距被钉死（几何标度破缺）"),
    ([E_couple, E_pitch, E_radius], "S2 几何扇区全部钉死（R 与 b 都定）"),
    ([E_couple, E_pitch, E_radius, E_couple_abs], "S3 再加非齐次耦合约束（需外界输入）"),
]

out("## 2. 分场景实算（sympy 精确）")
out()
out("数值点：$R=b=\\ell=R_0=c=1$，$\\tilde g=1$，$\\tilde g'=1/\\sqrt3$。")
out()
results = []
for es, label in scenarios:
    a = analyze(es, label)
    results.append(a)
    out("### " + label)
    out()
    out("- 约束条数 $m=" + str(len(es)) + "$，$n=4$")
    out("- $\\operatorname{rank}(J_E)=" + str(a["rank"]) + "$ ⇒ **$\\operatorname{nullity}_{\\rm dyn}=" + str(a["nullity"]) + "$**")
    out("- 零空间基：")
    for v in a["ker"]:
        out("  - `( " + ",  ".join(sp.sstr(sp.nsimplify(x)) for x in v) + " )`")
    out()
    out("| 靶 | $dq\\|_{\\ker J_E}$ | 判定 |")
    out("|---|---|---|")
    for name, ds, allz in a["targets"]:
        cell = ", ".join(sp.sstr(d) for d in ds) if ds else "—（$\\ker J_E=\\{0\\}$）"
        out("| `" + name + "` | " + cell + " | "
            + ("**真预言候选**" if allz else "**仍自由（拟合）**") + " |")
    out()

out("---")
out()
out("## 3. 结论一：砖① 对 $\\alpha$ 无效（块对角解耦）")
out()
out("对比 S0 与 S1/S2：")
out()
out("| 场景 | $\\operatorname{rank}$ | $\\operatorname{nullity}_{\\rm dyn}$ | $\\alpha_{\\rm couple}$ | $\\alpha_{\\rm geo}$ |")
out("|---|---|---|---|---|")
for a in results:
    tr = {n: allz for n, ds, allz in a["targets"]}
    out("| " + a["label"][:2] + " | " + str(a["rank"]) + " | " + str(a["nullity"]) + " | "
        + ("固定" if tr["alpha_couple"] else "**自由**") + " | "
        + ("固定" if tr["alpha_geo"] else "**自由**") + " |")
out()
out("**关键读数**：")
out()
out("1. 砖①（$E_{\\rm pitch}$）确实**杀死了长度扇区的一条方向**（$\\operatorname{nullity}_{\\rm dyn}: 3\\to2$）——"
    "它完成了几何标度破缺。")
out("2. 但 $\\alpha_{\\rm couple}$ 的 $dq\\|_{\\ker J_E}$ **仍不为零**：因为 $J_E$ 在")
out("   「几何 ⊕ 耦合」上**块对角**，几何约束的行在耦合列上全为 $0$，")
out("   碰不到耦合扇区。")
out("3. S2 把几何扇区**全部**钉死（$R,b$ 都定），$\\operatorname{nullity}_{\\rm dyn}$ 降到 1，")
out("   但剩下的那 1 维恰好是**耦合整体标度方向**，$\\alpha$ 依旧自由。")
out()
out("> **所以：无论加多少条几何标度破缺项，都不能锁定 $\\alpha$。**")
out()

# ============================================================
# §4 定理 E 的严格版
# ============================================================
out("## 4. 定理 E 的严格版（齐次性障碍）")
out()
out("**命题（齐次性障碍）**：若约束 $E$ 在耦合上是 $d$ 次齐次函数（各项同次、无常数项），")
out("则在约束面 $E=0$ 上，欧拉定理给出")
out()
out("$$\\sum_i \\tilde g_i\\,\\frac{\\partial E}{\\partial \\tilde g_i}=d\\,E=0,$$")
out("即「耦合整体重标度方向」$s=(\\tilde g,\\tilde g')$ 恒属于 $\\ker J_E$。")
out()
out("sympy 符号验证（举一般 4 次齐次式）：")
out()
a4, c4 = sp.symbols("a4 c4")
E_hom = g**4 + a4 * g**2 * gp**2 + c4 * gp**4
euler = sp.simplify(sum(v * sp.diff(E_hom, v) for v in (g, gp)) - 4 * E_hom)
out("```")
out("E_hom = g~^4 + a4 g~^2 g~'^2 + c4 g~'^4          (4 次齐次)")
out("sum_i g_i dE/dg_i  -  4 E_hom  =  " + sp.sstr(euler) + "      (恒为 0)")
out("```")
out()
out("**推论**：任何齐次约束系统都有 $\\operatorname{nullity}_{\\rm dyn}\\ge1$（含标度方向），")
out("故对一切依赖耦合整体标度的靶（$\\alpha$ 型，2 次齐次）必有")
out("$d\\alpha\\|_s = 2\\alpha\\ne0$ ⇒ **$\\alpha$ 自由。这是定理 E 的严格形式。**")
out()
out("---")
out()

# ============================================================
# §5 定理 F：输入壁垒
# ============================================================
out("## 5. 定理 F（输入壁垒）")
out()
out("### 5.1 陈述")
out()
out("要杀死耦合扇区的标度方向（即让 $\\alpha$ 的 $dq\\|_{\\ker J_E}=0$），")
out("约束 $E$ 必须**非齐次**（含异次项或常数项）。而任何非齐次约束都必然")
out("引入一个**不由该齐次结构本身决定的新系数**。该系数的来源穷尽为三类：")
out()
out("1. **实测值** ⇒ 落入定理 C 情形 2：$\\alpha$ 恒可反解 ⇒ **定义，不是预言**；")
out("2. **结构数**（整数 / 表示维数 / 有理数） ⇒ 解是**代数数**（见下），")
out("   其命中必须靠数检索 ⇒ 由第58章 $V_3$ 判为 numerology；")
out("3. **另一个无量纲本征值** ⇒ 问题**递归**（需先有那个本征值），不构成解锁。")
out()
out("三类均不解锁 UFT-3。∎")
out()
out("### 5.2 机制验证：非齐次约束确实能杀死标度方向")
out()
out("取整数系数的非齐次约束 $E=\\tilde g^{4}-3\\tilde g^{2}=\\tilde g^{2}(\\tilde g^{2}-3)=0$：")
out()
E_nh = g**4 - 3 * g**2
euler_nh = sp.simplify(sum(v * sp.diff(E_nh, v) for v in (g,)))
sols = sp.solve(sp.Eq(E_nh, 0), g)
out("```")
out("E_nh = g~^4 - 3 g~^2 = 0")
out("解： g~ = " + ", ".join(sp.sstr(s) for s in sols) + "      (非零解为代数数 sqrt(3))")
out("欧拉和 sum g dE/dg = " + sp.sstr(sp.factor(euler_nh)) + "  != 0  (在 g~^2=3 处为 18)")
out("```")
out()
out("**验证通过**：非齐次约束确实把标度方向移出 $\\ker J_E$（欧拉和不为零）。")
out("但注意其非零解 $\\tilde g=\\sqrt3$ 是**代数数**——由整数系数产生的一切解都落在")
out("代数数集内。这就是来源②的特征，也是它的天花板。")
out()
out("---")
out()

# ============================================================
# §6 定量检验：alpha 不是小分母有理数
# ============================================================
out("## 6. 定量检验：$\\alpha$ 不是小分母有理数")
out()
out("来源②的危险在于「找一个结构比恰好等于 $\\alpha$」。用连分数做定量筛查。")
out()
ALPHA_INV = "137.035999084"          # CODATA 2018
ALPHA_INV_UNC = 2.1e-8               # 该项不确定度 (21)
out("- 采用 $\\alpha^{-1}=" + ALPHA_INV + "$（CODATA 2018），不确定度 $\\pm" + str(ALPHA_INV_UNC) + "$")
out()

x = Fraction(ALPHA_INV)
cf = []
num, den = x.numerator, x.denominator
while den and len(cf) < 12:
    qi = num // den
    cf.append(int(qi))
    num, den = den, num - qi * den
out("- $\\alpha^{-1}$ 的连分数展开：$[" + ", ".join(str(q) for q in cf) + ",\\dots]$")
out()

# 收敛子
def convergents(cf_terms):
    p0, q0 = 0, 1
    p1, q1 = 1, 0
    res = []
    for a in cf_terms:
        p0, p1 = p1, a * p1 + p0
        q0, q1 = q1, a * q1 + q0
        res.append((p1, q1))
    return res


alpha_inv_f = float(ALPHA_INV)
out("| 收敛子 $p/q$ | 小数 | 与 $\\alpha^{-1}$ 之差 |")
out("|---|---|---|")
for p, q in convergents(cf)[:6]:
    out("| " + str(p) + "/" + str(q) + " | " + "%.10f" % (p / q) + " | " + "%.3e" % abs(p / q - alpha_inv_f) + " |")
out()

# 暴力找最佳有理逼近（小分母）
best = None
QMAX = 4000
for q in range(1, QMAX + 1):
    p = round(alpha_inv_f * q)
    err = abs(p / q - alpha_inv_f)
    if best is None or err < best[2]:
        best = (p, q, err)
# 找出「首次进入实验精度」的最小分母
q_star = None            # 100 sigma
for q in range(1, 200001):
    p = round(alpha_inv_f * q)
    if abs(p / q - alpha_inv_f) < 100 * ALPHA_INV_UNC:
        q_star = (p, q)
        break
q_1s = None              # 1 sigma（当前测量精度）
QMAX3 = 3000000
for q in range(1, QMAX3 + 1):
    p = round(alpha_inv_f * q)
    if abs(p / q - alpha_inv_f) < ALPHA_INV_UNC:
        q_1s = (p, q)
        break
out("- 分母 $\\le " + str(QMAX) + "$ 的最佳有理逼近：$" + str(best[0]) + "/" + str(best[1])
    + "$，误差 $%.3e$" % best[2])
q100_txt = (str(q_star[1]) if q_star else "> 200000")
q1_txt = (str(q_1s[1]) if q_1s else "> " + str(QMAX3))
out("- 进入 $100\\sigma$ 所需的最小分母：$q^*_{100}=" + q100_txt + "$")
out("- **达到 $1\\sigma$（当前测量精度）所需的最小分母**：$q^*_{1}=" + q1_txt + "$")
out()
out("**结论**：由群维数 / 表示论得到的结构数，其分母来自少量小整数的组合")
out("（$SU(3)\\times SU(2)\\times U(1)$ 的维数 3/2/1、秩 2/1、Casimir 等，分母量级 $\\lesssim 10^{2}$）。")
out("而 $\\alpha^{-1}$ 的连分数部分商含 $27$ 与 $16$（大数）⇒ 它对简单有理数**排斥**：")
out("要逼近到当前测量精度（$1\\sigma$），至少需要分母 $q^*_1"
    + ("\\approx" + str(q_1s[1]) if q_1s else "$ 极大") + "$。")
out("这与可枚举的结构比集合在**分辨率上不可通约**。")
out("注：本检验只排除**小分母有理数**；一般代数数（如 $\\sqrt{3}$ 的组合）的穷尽搜索属 [C] 待建。")
out("这与第56章 §56.3.3「纯数因子盲区」互补：那里说量纲矩阵看不见 $4\\pi$；")
out("这里说即使看见，结构数的分辨率也够不到 $\\alpha$。")
out()
out("---")
out()

# ============================================================
# §7 判定汇总
# ============================================================
out("## 7. 判定汇总")
out()
out("| 项 | 结果 |")
out("|---|---|")
out("| 砖①（几何标度破缺）是否杀死长度扇区的标度方向 | **是**（$\\operatorname{nullity}_{\\rm dyn}:3\\to2$） |")
out("| 砖① 是否锁定 $\\alpha$ | **否**（块对角解耦，$d\\alpha\\|_{\\ker J_E}\\ne0$） |")
out("| 几何扇区全部钉死后 $\\alpha$ 是否锁定 | **否**（剩 1 维恰为耦合标度方向） |")
out("| 锁定 $\\alpha$ 所需的最小改动 | 一条**非齐次耦合约束**（$E_{\\rm couple}^{\\rm abs}$） |")
out("| 该约束的系数来源 | 实测（C2）/ 结构数（代数数，$V_3$ 判）/ 另一本征值（递归）——均不解锁 |")
out("| 定量筛查 | $\\alpha^{-1}$ 非小分母有理数（$q^*$ 见 §6） |")
out("| **S13 / 联盟是否解锁 UFT-3** | **否** |")
out("| UFT 联盟层达成度 | 仍 2/6（未实现） |")
out()
out("### 7.1 对第64章 §64.7 处方的**修正**（诚实自评）")
out()
out("第64章说：解锁缺口是「一条打破标度不变性的非齐次第一性原理变分项」。")
out("本轮的实算表明该处方**必要但不充分**，应修正为：")
out()
out("> **必须是一条既非齐次、又作用于「耦合扇区」的约束**——只打破几何标度")
out("> 不变性（砖①②）不够，因为 $J_E$ 的几何块与耦合块**解耦**。")
out()
out("这是本编的第一次**自我修正**：第64章的定理 E 正确地识别了「齐次性障碍」，")
out("但把「打破标度不变性」当成了充分条件；定理 F 补上了「必须落在耦合扇区」")
out("这一半。两半合起来，缺口才被完全刻画。")
out()
out("---")
out()
out("## 8. 诚实边界")
out()
out("### 已确认 [A]（sympy 精确）")
out()
out("1. 四场景的 $\\operatorname{rank}(J_E)$ 与 $\\ker J_E$ 实算：S0 1/3、S1 2/2、S2 3/1、S3 4/0。")
out("2. 砖① 与几何钉死均不改变 $\\alpha_{\\rm couple}$ 的 $dq\\|_{\\ker J_E}\\ne0$。")
out("3. 齐次性障碍：4 次齐次式欧拉和恒为零（符号验证）。")
out("4. 非齐次机制：$\\tilde g^{4}-3\\tilde g^{2}=0$ 的欧拉和不为零（$=18$ 于 $\\tilde g^{2}=3$）。")
out("5. 连分数与最小分母 $q^*$ 为数值精确结果。")
out()
out("### [B] 框架映射")
out()
out("1. 「几何扇区 / 耦合扇区」的划分是本册的建模选择；其正当性来自")
out("   量纲/标度结构（几何旋钮带量纲、耦合旋钮无量纲），与第64章一致。")
out("2. 定理 F 的「三类来源穷尽」是分类断言，依赖「新系数必须来自某处」")
out("   这一物理前提——与定理 C 的「已测/未测二分」同源，边界相同。")
out()
out("### [C] 待建")
out()
out("1. **存在性搜索**：是否**存在**一条非齐次耦合约束，其系数全部为结构数而又")
out("   恰好给出 $\\alpha$？§6 只排除了**小分母有理数**；完整的代数数搜索未做")
out("   （需对给定代数次数枚举）。这是可计算的，是真正的下一步。")
out("2. **与 $V_3$ 的复合口径**：把「定理 F 排除的搜索空间」计入 $V_3$ 的 Bonferroni")
out("   惩罚，可使 $V_3$ 对代数数靶也有免疫力（承接 §64.9 [C]2）。")
out()
out("---")
out()
out("> **本册结论**：本轮**实际构造**了砖①（几何标度破缺变分项），并证明了它的")
out("> 边界：它能杀死长度扇区的标度方向，但**碰不到耦合扇区**（$J_E$ 块对角），")
out("> 因此**不能锁定 $\\alpha$**。由此得**定理 F（输入壁垒）**：锁定 $\\alpha$ 必须")
out("> 施加一条非齐次的**耦合**约束，而其系数只能来自实测（C2）/ 结构数（代数数，")
out("> $V_3$ 判）/ 另一本征值（递归），三类均不解锁。连分数定量筛查进一步排除")
out("> 小分母结构有理数。**本册同时修正了第64章的处方：打破标度不变性必要但不充分，")
out("> 必须落在耦合扇区。** UFT 联盟层达成度仍为 2/6（未实现）。")

text = "\n".join(R_OUT) + "\n"
with open(os.path.join(DATA, "砖一构造尝试.md"), "w", encoding="utf-8") as f:
    f.write(text)

payload = {
    "engine": "砖一构造尝试_标度破缺与输入壁垒.py",
    "date": TODAY,
    "scenarios": [
        {"label": a["label"], "rank": int(a["rank"]), "nullity_dyn": int(a["nullity"]),
         "targets": {n: (None if allz else [sp.sstr(d) for d in ds])
                     for n, ds, allz in a["targets"]}}
        for a in results
    ],
    "theorem_E_homogeneous_euler_zero": bool(euler == 0),
    "theorem_F_nonhomogeneous_breaks": bool(euler_nh != 0),
    "alpha_inv_continued_fraction": cf,
    "best_rational_denom_le_4000": {"p": best[0], "q": best[1], "err": best[2]},
    "min_denom_within_100sigma": (q_star[1] if q_star else None),
    "min_denom_within_1sigma": (q_1s[1] if q_1s else None),
    "brick1_fixes_alpha": False,
    "S13_unlocks_UFT3": False,
    "UFT_attainment": "2/6",
    "correction_to_ch64": "打破标度不变性必要但不充分；必须落在耦合扇区",
}
with open(os.path.join(DATA, "砖一构造尝试.json"), "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

print(text)
print("[OK] wrote", os.path.join(DATA, "砖一构造尝试.md"))
print("[OK] wrote", os.path.join(DATA, "砖一构造尝试.json"))
