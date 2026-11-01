# -*- coding: utf-8 -*-
"""r346 工作日志（幂等）：追加到 .workbuddy/memory/YYYY-MM-DD.md，复跑必须 SKIP。"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
p = HERE
while p and not os.path.isdir(os.path.join(p, ".workbuddy")):
    np = os.path.dirname(p)
    if np == p:
        break
    p = np
MEMDIR = os.path.join(p, ".workbuddy", "memory")
LOG = os.path.join(MEMDIR, "2026-11-01.md")

KEY = "## r346 · 整数 Newton 系数是三行初等事实而非几何定理"

BODY = """
## r346 · 整数 Newton 系数是三行初等事实而非几何定理（★攻 `X-R339-1`；判词下调）

- **取号**：扫号见 **r340–r344 全被占**、**r345 为热号**（有 `_probe` 占位）⇒ 取冷号 **r346**；
  按「大文件动手前先写 `_probe_rN.py` 占位」纪律先占位再写 32KB 引擎，全程零改他人字节。
- **攻靶**：`X-R339-1` —— r339 只给了 `a_j ∈ Z` 的 30/30 机检，没给一般证明。
  **本卷先把一般证明补上，然后被自己的证明反噬**：证明只有三行且不需要几何 ⇒ 追问「那这条定理说了什么」⇒ **几乎什么都没说**。
- **★★★引理 L（三行，无几何）**：设 `P ∈ Q[k]`、`P(Z) ⊆ Z`，则 Newton 系数
  `a_j = Δ^j P(0) = Σ_i (−1)^{j−i} C(j,i) P(i)` 是**整数的整数组合** ⇒ `a_j ∈ Z`。∎
  套到 `χ` 上只需一步：**`χ(O_X(kH))` 是欧拉示性数**（有限维上同调的交替和）⇒ `P(Z) ⊆ Z` 无条件成立。
  `A01` 机械核对 **130 项（30 组 × (n+1)）逐项一致、失配 0**；`A02` 前提不可去的负控 **3/3**；
  `A03` 无几何版直接构造（`C(k,2)+3C(k,3)` 不对应任何射影簇，`a=(0,0,1,3)` 全整）。
- **★★★判词下调（本卷主轴）**：**两条承重件都不承重** ——
  ① `a_j ∈ Z` 是「整数组合仍是整数」⇒ **定义恒等式**；② `Z ⊆ S` 是 `S` 的**定义**。
  ⇒ **r339 的「定理 B」从定理降级为定义恒等式**，它的 30/30 是**引擎自检**不是几何证据。
- **★★判别力 0**：`A04` 72 组（`n=1..6, d=1..12`）`a_j` 全整、非整组数 **0**
  ⇒ 一个对 100% 输入都通过的谓词**没有判别力**，按本库门禁**不得当判据用**。
- **★★但它还是个 bug 探测器（必要非充分）**：`A05` 故意算错 td 两种
  （少一个 `T` 因子 / `td_cpn` 写成**逐元素幂**）⇒ Newton 系数立刻非整 **27/30** 与 **29/30**；
  `A06` 却**漏掉 3 组与 1 组**（如 `(1,2)` 错给 `a=(0,2)` 而正确是 `(1,2)` 仍全整）⇒ r339 的 30/30 只能证明「没犯某些错」。
- **★★★定理 C（本卷唯一不平凡产出，且无任何假设）**：`k = r/M` 最简、`P(k) ∈ Z` ⇒ **`M | a_n`**。
  四行证明：乘 `M^n n!`、`N_j(r) = r(r−1)…(r−j+1) ≡ r^j (mod M)` 消掉 `j<n` 全部项、
  只剩 `a_n r^n`，`gcd(r,M)=1` 收尾。**连 `a_j ∈ Z` 都不需要**。
  推论：超曲面上 `a_n = H^n = d`（`CTL11` 72 组违例 0）⇒ **`S ⊆ (1/d)Z`**；
  `n=1` 时等号成立（`B04`，`d=1..24` **24/24**）；`M=d` 仅 **13/72** 可达 ⇒ `n ≥ 2` 只是**上界**（`B05`）；
  分母谱只能是 `d` 的因子（`B06` 越界 **0**）。
- **★★★定理 D（把 r339 的「非陪集」从混沌改写成结构）**：在陪集 `c+Z` 上把 `P` 重写
  `b_i = Σ_{j≥i} a_j C(c, j−i)`（**396 陪集失配 0**），且 `M^n n! b_i ∈ Z`（**1782 项非整 0**）
  ⇒ 整性在每个陪集上**周期**，周期界 `(M^n n!)^2`（`C03` **81/81** 合法）
  ⇒ **`S` 是有限个等差级数之并**。这正是 r339 看到「非陪集」的原因：**并集上仿射封闭 `u−v+w` 必然失败**。
  实测周期 ∈ `{1,2,4,16,32,64}`；`(5,2)` 的 **N=64 > M^n=32** ⇒ **`N | M^n` 已被否证**（新开 `X-R346-1`）。
- **★★不推翻 r339 任何读数（只改读法与信用归属）**：`G11` 与 r339 落盘 JSON 的 30 组 Newton
  **逐项字符串相等、差异 0**；`D04` 重跑 r339 的 `χ == h⁰` 主校验 **448/448 失配 0**，
  但**重贴标签**为「引擎正确性校验」而非「超曲面有特殊算术」。
- **定价** 2⁶=64 ⇒ 可行 **3**、匹配 **1**、**被钉住 4 位**（`S3..S6`）、未钉住 2 位（`S1,S2` 只能**联合**判定）、
  翻转任一钉住位后 **0** ⇒ **不占度（候选 37，链止 r264:36）**。
- **判词**：`X-R339-1-ANSWERED__THE-GENERAL-PROOF-IS-A-THREE-LINE-FINITE-DIFFERENCE-IDENTITY-AND-NEEDS-NO-GEOMETRY__SO-R339-THEOREM-B-IS-DEMOTED-FROM-A-THEOREM-TO-A-DEFINITION-TAUTOLOGY__ITS-30-OF-30-CHECK-IS-A-BUG-DETECTOR-WHICH-IS-NECESSARY-BUT-NOT-SUFFICIENT__Z-SUBSET-S-HOLDS-ON-EVERY-POLARIZED-VARIETY-SO-THE-PREDICATE-HAS-ZERO-DISCRIMINATING-POWER__THE-REAL-THEOREM-IS-ASSUMPTION-FREE-M-DIVIDES-THE-LEADING-NEWTON-COEFFICIENT__HENCE-S-IS-CONTAINED-IN-ONE-OVER-DEG-Z-WHICH-IS-SHARP-ONLY-FOR-N-EQUALS-ONE__AND-INTEGRALITY-IS-PERIODIC-ON-EACH-COSET-SO-S-IS-A-FINITE-UNION-OF-ARITHMETIC-PROGRESSIONS__R339-NOT-OVERTURNED-BUT-RECERTIFIED-AND-THE-CREDIT-REDISTRIBUTED__STILL-NOT-PREDICTED`
- **自审十处，三类各成族**（本卷踩出，如实登记在判定册 §十一）：
  **【A 假守卫】**`G04/G09/G17` 首跑写成 `guard(..., True, ...)` —— 正是本库明令禁止的写死，
  我自己犯了 ⇒ 全部改真判据，并新增 **`G19` 结构性防线**（`ctl/guard` 的 `ok` 实参**顶层**不得是布尔常量，AST 层查）。
  **【B 守卫自伤】**`G12` 报 `random` 6 次、`G13` 报 `float(` 3 处 —— 守卫**自命中**自己的字符串字面量
  （本库**第三次**同族）⇒ 改 **AST 层**查 `Import` / 浮点 `Constant`；`G05` 用 `ast.walk` 把比较号后的常量也算进来 ⇒ 只查顶层类型。
  **【C 期望与判据】**`C06` 期望 `7,1,1` 而实测 `7,0,1` —— **期望值是猜的** ⇒ 改两条独立路径交叉
  （直接扫描 vs 陪集枚举），**期望只能取自另一条路径**；`B04` 期望集只取互素剩余类 ⇒ 改全体剩余类；
  `C05` 测不出周期就丢掉整个陪集 ⇒ 改**不依赖周期**的逐点取；`E03` 敏感度打在**未被钉住的位**上 ⇒ 改打钉住位，
  并把「自由位 2 个」升格为 `E02` 读数；`CTL8` 口径窗口两端不一致 ⇒ 夹 `[-6,6]`；`CTL13` 与 `E03` 重复 ⇒ 改非对称对照。
  **家族归因**：这是本库**第五卷**同族自伤（`r327 → r331 → r335 → r339 → r346`），
  但**落点从「算错对象」移到了「守错门」** —— 复算抓不到，只能靠「换一个口径再问一次」。
- **新增纪律三条（可复用）**：
  **①假守卫三字母就能让门禁变装饰** ⇒ 必须有**结构性防线**（`G19`：顶层不得是常量），不能只靠自觉；
  **②守卫不得读自己源码的字符串字面量**，一律 AST 层；
  **③期望值不得猜**，只能取自另一条独立路径。
- **顺带踩到的 HTML 两条**：辅助函数不要叫 `box`/`el`（与体检器内部 `box` 在 `eval` 同作用域冲突）；
  **不要在 `rbox` 里钳位 `w<=0`**（会把体检器要抓的零宽 bug 藏起来 —— 首跑正是这样静默全绿）。
- **收口链**：引擎 **25 条 / 25 PASS / 0 FAIL / 0 INFO**、控制组 **13/13**、守卫 **19/19**、rc=0；
  数据说明件补 **§十六 产物**（真链接，`_patch_r346_closure.py`，+1754 字节，diff 零删除 232/232，复跑 SKIP）；
  README 登记两处（**现行只剩源码树 + 判定列表**；`_reg_r346.py` diff 零删除 **1055/1055**，+6427 字节，复跑 SKIP）；
  链接体检 **16 条 0 断**（README 项分母如实 **0**，由新增正控②/②b 证明过滤器未失效）；
  几何体检 4 图 **fig1 70 / fig2 42 / fig3 197 / fig4 107 = 416 图元 0 越界**，负对照回填零宽 ⇒ 精确报 **5 条「宽度为 0 ⇒ 不可见」** + rc=2。
- **★外部事故（如实登记，不代修）**：`README.md` 于 **23:14:59** 被并行会话整体重写，
  行数 **20164 → 1055**、`git diff --stat` 显示 **+45 / −17671**。原有的 `- **rN（` compact 对照表与
  `### rN ·` detail 节**全部消失**（`### r` 计数 0、`- **r3` 计数 0），目录树（line 48 起的 ```text 围栏）**未闭合**。
  我的 r339 四处登记因此只剩两处（源码树 / 判定列表）。**未擅自回滚**（并行会话可能仍在写），
  备份留存：`scratch/_bak_README_pre_r346.md`（1054 行，被改后形态）、`scratch/_bak_README_pre_r339_closure.md`（2.83 MB，20:39 全量）、git HEAD（18680 行）。
- **遗留 OPEN**：`X-R346-1`（周期界 `(M^n n!)^2` 能否压到 `M^n`；`N | M^n` 已否证，真紧界未定）/
  `X-R346-2`（额外点 `S ⊋ Z` 的存在判据，`d` 偶 ⇒ 可能有 `M=2` 但 `n` 偶时常空）/
  `X-R339-3`（加权超曲面上 `a_n ≠ deg`，定理 C 的形式）/ `X-R335-1` / `X-R331-1`。
- **最终一句**：**`X-R339-1` 问的是「能不能给一般证明」，答案是「能，而且只要三行、不需要几何」；
  但给了证明之后才发现，这条定理的两条承重件一条是「整数组合仍是整数」、另一条是 `S` 的定义 ——
  所以它从来没在判别任何东西。真正有内容的是定理 C（`M | a_n`，无假设）与定理 D（`S` 是有限个等差级数之并），
  后者顺手把 r339 的「非陪集」从「混沌」改写成「并集」。**
"""


def main():
    if not os.path.isdir(MEMDIR):
        print("MEMDIR MISSING: %s" % MEMDIR)
        return 2
    old = io.open(LOG, encoding="utf-8").read() if os.path.exists(LOG) else ""
    if KEY in old:
        print("SKIP (already logged)  key=%s" % KEY)
        return 0
    sep = "" if old == "" or old.endswith("\n") else "\n"
    new = old + sep + BODY
    io.open(LOG, "w", encoding="utf-8", newline="\n").write(new)
    chk = io.open(LOG, encoding="utf-8").read()
    if KEY not in chk:
        print("LOG-FAIL: key 未落盘")
        return 3
    print("LOG-OK  +%d chars  (total %d)" % (len(chk) - len(old), len(chk)))
    return 0


sys.exit(main())
