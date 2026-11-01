# -*- coding: utf-8 -*-
"""r325 工作日志（幂等）：追加到 .workbuddy/memory/YYYY-MM-DD.md，复跑必须 SKIP。"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
# 上一行不可靠，改为按已知锚点回溯：找 .workbuddy 目录
HERE = os.path.dirname(os.path.abspath(__file__))
p = HERE
while p and not os.path.isdir(os.path.join(p, ".workbuddy")):
    np = os.path.dirname(p)
    if np == p:
        break
    p = np
MEMDIR = os.path.join(p, ".workbuddy", "memory")
LOG = os.path.join(MEMDIR, "2026-11-01.md")

KEY = "## r325 · 通量量子数与稳定性的联立"

BODY = """
## r325 · 通量量子数与稳定性的联立（★★撤回 r319 唯一性 · 攻 `X-R319-1`）

- **攻靶**：r319 §十二 交接的 `X-R319-1`「`q = 3` 由什么选定」。原话说「只做了量子化、没做稳定性」。
- **定理 A（量子化格不是 `Z`）**：`c1(CP^n)=(n+1)H` ⇒ `CP^n` spin ⟺ n 奇；非自旋圈上 `[F] ∈ H²(Z)+c1/2`
  ⇒ **`CP²` 的格是 `Z+1/2`**（`|q|≤4` 的 8 个值：`±1/2,±3/2,±5/2,±7/2`），**整数不合法**。
- **★★定理 B（撤回）**：正确格上 **`CP² + q=±5/2` 精确给 `n_R=3`**（`25/8−1/8`，Fraction）
  ⇒ r319「`CP¹` 是唯一真空」**判负撤回**。保留「`CP²` 上整数无解」「只有 `CP¹` 有整数解」两句。
  **理由不是算错，是格选窄了** —— 本链第一次由后一卷撤回前一卷的**正面结论**。
  计数分列：解数 3 / 不同 `|q|` 2 / 几何 2 / 最小 `|q| = 5/2`（在 `CP²`，不是 `CP¹` 的 3）。
- **★★定理 C（稳定性零约束）**：slope / DUY / HYM / D 项 / tadpole / 模稳定化 对 rank-1 的 **q 约束数 = 0**；
  **最狠一刀**：`CP¹` 实维 2，`F∧F` 恒 0 ⇒ **tadpole 在给出三代的几何上信息量恰好为零**。
  `Z₃` 只给同余（`[−5,5]` 的 11 个整数留 4 个）。**活性对照 CTL15**：同判据在 rank-2 上排除 36 个序对 ⇒ 零是结构性的。
- **★★定理 D（恒等映射）**：`CP¹` 上 `n_R(q)=q` 恒等（41/41）⇒「q=3」与「三代」是同一句话；
  反向可及 **12/12** ⇒ 判别力 0；`CP¹` 只有 1 个非零系数（一次单根）⇒ 没有剩余内容留给「机制」。
- **★★定理 E（问题倒置）**：解集 `{CP¹:3} ∪ {CP²:±5/2}`；`|q|` 极小**无动力学理由** ⇒ 报告 ≠ 主张（`D05` 自我否定）。
- **防反驳 A17**：`q²=25/4` 非整数**不**违反电荷量子化 —— 总诱导电荷 `25/8 − 3/24 = 3` 为整数。
- **定价** 2^6=64 ⇒ 可达 **18** / 严格 **0**；**`S1∧S2=0`**（解释了三代 ⟺ 三代成立，互斥）、**`S3∧S5=0`**、
  `S2∧S3∧S6=2` ⇒ 不占度（候选 37，链止 r264:36）。
- **引擎**：items 49（PASS 41 / FAIL 0 / INFO 8）、控制组 15/15、守卫 16/16、rc=0。
- **★★自审（三处自伤，已修）**：
  ① 三处期望值抄错：`A05`（格的「前 8 个」误当最近的 8 个）、`B08`（区间长度 11 当解数，实为 4）、
     `B09`（非自旋 `CP^n` 个数 3 当约束削减量）；
  ② 三条**假计算**：`C05`/`C06` 写成 `item(...,1,1,...)`、`B02` 写成 `all(True for _ in NS)` ⇒ 全部改写为真计算；
  ③ `B01` 的零差点成恒绿装饰 ⇒ 补 `CTL15` 活性对照并扩写进 `G14`(6/6)。
- **★改号实战（新教训）**：首扫只看 `TUFT-rN_`，**漏了 `_run_rN.py` / `_out_rN.txt` 前缀**
  ⇒ 以为 r322/r323 空，实际 **r323 于 13:42 被并行会话落盘**（`电磁侧选择机制清单扩展`）、r324 有他人
  「下轮从 r324 复查起」占位预告 ⇒ 顺延 **r325**。**零改动**并行的 `TUFT-r323_电磁侧…`/`_run_r323.py`/`_out_r323.txt`
  （改号脚本显式打印 UNTOUCHED 清单核验）。**下轮起：扫号必须 `grep -c \"r${n}[_]\"` 覆盖 `_` 前缀文件。**
- **收口链**：引擎 rc=0 → 数据说明件 / 判定册（均带真链接导航）→ HTML 4 图 981 图元 0 越界 `GEOMETRY-OK`
  + 负对照注入 `width:0` 精确报「rect(fill=…) 宽度为 0 ⇒ 不可见」`rc=1` → README 四处 count=1
  `DIFF-ZERO-DELETION 19204/19204`、复跑 SKIP → 链接体检 24 条 0 断 `LINK-OK`（三负控 + 一正控）。
- **遗留 OPEN**：`X-R325-1`（**为什么只有 n=1,2 有解**？n≥3 两档全无解，只报不解释）｜
  `X-R325-2`（tadpole 整体闭合能否排除 `±5/2` 之一）｜承前 `X-R319-2/3`、`X-R322-1`、`X-R307-2/3`、`X-R309-2/3`、`X-R318-2`。
"""


def main():
    if not os.path.isdir(MEMDIR):
        os.makedirs(MEMDIR, exist_ok=True)
    old = ""
    if os.path.exists(LOG):
        old = io.open(LOG, encoding="utf-8").read()
    if KEY in old:
        print("SKIP (log already appended) len=%d" % len(old))
        return 0
    txt = old
    if txt and not txt.endswith("\n"):
        txt += "\n"
    txt += BODY
    io.open(LOG, "w", encoding="utf-8").write(txt)
    chk = io.open(LOG, encoding="utf-8").read()
    assert KEY in chk, "write-back verify failed"
    assert chk.startswith(old[:200]) if old else True
    print("LOG-OK %s  chars=%d (was %d, added %d)"
          % (os.path.basename(LOG), len(chk), len(old), len(chk) - len(old)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
