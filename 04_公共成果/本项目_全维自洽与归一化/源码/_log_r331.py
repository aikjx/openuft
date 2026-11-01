# -*- coding: utf-8 -*-
"""r331 工作日志（幂等）：追加到 .workbuddy/memory/YYYY-MM-DD.md，复跑必须 SKIP。"""
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

KEY = "## r331 · 族数整性定理与 k 坐标压缩"

BODY = """
## r331 · 族数整性定理与 k 坐标压缩（★复核 r327 两处未审前提）

- **攻靶**：r327 留了两处**从没被审过**的东西 —— ①「Freed–Witten 格」是从 r325 借的，依赖 `c₁`、`w₂` 与
  D-brane 带 `spin^c` 这条**物理假设**；②「四支点证明」从没被问过「四个是不是都必要」。本卷只审这两处，**不改判任何结论**。
- **★★★定理 A（整性定理）**：`x ∈ Q`、`n ≥ 1`、`C(x,n) ∈ Z ⇒ x ∈ Z`。
  证明三行：`x=a/b` 既约、`p|b` ⇒ 每因子 `a−ib ≡ a (mod p)`，`p∤a` ⇒ `p` 不整除分子；
  分母含 `b^n ⊇ p^{n·v_p(b)}`（`n≥1`）⇒ 约分后分母仍带 `p` ⇒ 不是整数。
  机检：非整点 **1700/1700 全非整**、整点 **810** 组 0 例外、`A05` 加强版（分母仍被 p 整除）**1700/1700**、
  `A08` 推到 `n=12,15` 仍 0。
  **判别力两条**：`A06` 同批点上 `2x` 有 **20** 个整值（定理不是废话）、`A07` `n=0` 时 `C≡1` 恒整 **170**（真的需要 `n≥1`）。
- **★★★定理 B（格重建 · 本卷最硬）**：只用 `q ∈ Q` + `n_R ∈ Z`，在 1/4 步长上**反解** `q`，
  得到的集合与 r325 的 FW 格**逐 n 相同：12/12，对称差 0**；格上 **188/188** 全整、离格 **0/547**。
  **未用输入**：`spin`、`spin^c`、`w₂`、`c₁`、D-brane、任何示性类（`G17` 源码级核查：B 组代码里几何函数命中 0）。
  ⇒ r327 的格**不需要那条物理假设**；它的身份从「几何逼出的离散数据」降为「**整性逼出的分母约束**」。
- **★★定理 B 副产品（`B06`）**：把偏移从 `(n−1)/2` 换成 `(n+1)/2`（差**整数 1**）⇒ **同一张格**（12/12）
  ⇒ 决定格的只是偏移的**模 1 类**，这正好解释 r325 的「移位」为什么只有 `0` 与 `1/2` 两种情形。
  ★ 这条副产品**来自一次失败**：`CTL5` 原设计「偏移一改格必须变」，实测不变 ⇒ 对照恒绿。修法不是删对照，
  而是把扰动改成差 **1/2**（`→ n/2`），**并把失败本身写成正面结论**。
- **★★定理 C（非负性）**：奇 n、`k<0` 的 64 个点里非零 **16 个全负**（另 48 个为**零**）；偶 n 的 56 个里非零 **12 个全正**（另 44 零）。
  负 `n_R` 共 **21** 个（奇占 21、偶占 **0**）⇒ 筛掉的是不可行点，**不砍任何解**（三个解全是 `+3`）。
  **纪律**：凡统计符号必须同时报**零的个数** —— 初版 `C01/C02` 把「非零 16」当「全部 64」，数字没错，分母错了。
- **★★定理 D（k 坐标）**：`n_R = σ·C(M,n)`，`M=k+n`（`k≥0`）/ `−k−1`（`k<0`），`σ=+1` 除非（`k<0` 且 n 奇）；
  关键等价 **`n_R ≠ 0 ⟺ M ≥ n`**（失配 **0**）⇒ 零段被吸收进 `M<n`。
- **★★定理 E（冗余性 · 结论）**：r327 支点③ = `M<n ⇒ C=0`、支点④ = `x<0 ⇒ M≥n` 落进支点① ⇒ **四支点塌成两支点**
  （① 单调 Pascal 差分 `C(M,n−1)>0`，615 组 0 失配；② 端点 `C(n,n)=1<3<n+1`，n=3..15 反例 0），
  **解集不变**：`(1,3)`、`(2,−5/2)`、`(2,5/2)`，与 r327 **逐 q 值一致**（`G16`）。
  ★ 正确读法不是「r327 冗余」，而是**「它们在 x 坐标下是两件独立的事，在 M 坐标下是同一件事的两种写法」**。
- **定价** 2^6=64 ⇒ 可达 **27** / 严格 **0**；`S1∧S2=0`、`S3∧S4=0`、`S2∧S4=3`、`S5∧S6=0` ⇒ 不占度（候选 37，链止 r264:36）。
- **判词**：`X-R327-COORDINATE-REVIEWED__N_R-IS-PLUS-OR-MINUS-C-M-N-WITH-M-AT-LEAST-N__THE-X-COORDINATE-WAS-THE-WRONG-ONE-K-ABSORBS-LEGS-THREE-AND-FOUR__INTEGRALITY-OF-N_R-ALONE-FORCES-THE-FREED-WITTEN-LATTICE-WITHOUT-SPINC__FOUR-LEGS-COMPRESS-TO-TWO__SOLUTION-SET-UNCHANGED__ASSUMPTIONS-WEAKENED-SO-THE-RESULT-IS-STRENGTHENED__STILL-NOT-PREDICTED`
- **自审六处**：①`E01` 断言写反（原断言「`M≠x` 恒成立」，实际 `x=(n−1)/2` 时相等 ⇒ 巧合次数 = 奇数 n 个数 **8**）；
  ②`C01/C02` 分母错位；③`CTL5` 负对照恒绿（见上）；④`G07` 判据写错（`A_NONINT==0` 应为 `==A_TOT`）；
  ⑤`D09` 期望值顺序与 `sorted` 不符；⑥`G17` 首版是**恒真守卫** ⇒ 换成源码级检查。
- **改号**：取 r331（r328/r330 已被并行会话占用，r329 留空）。
- **收口链**：引擎 **42 条 / 38 PASS / 0 FAIL / 4 INFO**、控制组 15/15、守卫 17/17、rc=0；
  README 四处登记 `REG-OK`（diff 零删除 **19531/19531**，+125 行，复跑 SKIP）；
  链接体检 **19 条 0 断** + 三负控一正控 **4/4** `LINK-OK`（负控①副本放回 `数据/` 原目录，测完即删）；
  几何体检 4 图 **462 图元 0 越界** `GEOMETRY-OK`。
- **遗留 OPEN**：`X-R331-1` —— 整性定理对 `n` 无界，但 `n_R=C(x,n)` 的闭式只对 `CP^n`；一般 Fano 上 `n_R` 是多元多项式，
  **整性还能否单独逼出量子化格**？（承 `X-R327-3`）
- **最终一句**：**r327 的「FW 格」看起来是几何建的，其实是算术逼出来的；它的「四支点证明」看起来是必要的，其实两个就够了。
  这两件事都不是推翻，是同一件事在更弱假设、更自然坐标下的重述 —— 而重述之后，空白反而更清楚：
  格与证明都已压到不能再压，唯一还没被碰的仍然是「为什么是 3」。**
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
