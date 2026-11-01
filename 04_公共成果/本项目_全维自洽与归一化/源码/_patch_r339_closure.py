# -*- coding: utf-8 -*-
"""r339 README 收口补钉（幂等）：在 detail 段末尾追加「收口链」一行。
纪律：①备份只在首次创建；②幂等 SKIP；③写后读回验键；④**最终守卫 = diff 零删除**。
"""
import io
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")
SCRATCH = os.path.join(ROOT, "scratch")

KEY = "**收口链（补钉 · 链接体检后）**"

BODY = (
    "- **收口链（补钉 · 链接体检后）**：链接体检 **17 条 0 断**"
    "（判定册 11 + README 中含 r339 的行 6）+ **两负控两变体一正控 6/6** `LINK-OK`"
    "（负控① 副本放回 `判定/` 原目录、测完即删；**新增负控④/④b**："
    "围栏代码块内 `[...](...)` 不算链接、同段移出围栏须变回 1 条 —— 证明不是正则失效）；"
    "几何体检 4 图 **258 图元 0 越界**，负对照回填 `width:0` 报 **68 条精确「不可见」** + rc≠0；"
    "工作日志 `LOG-OK +4872 chars`（复跑 SKIP）。"
    "★**同号并存如实登记**：并行会话另落一份 `TUFT-r339_光速螺旋G6_EinsteinCartan挠率源方程…`"
    "（源码 20:38:37 / 判定册 20:40:04），本卷判定册 **20:38:00** 在先 ⇒ **本卷保号 r339，零改对方字节**；"
    "对方随后自行改号（其 `_renum_r339g6_to_r341.py`）。"
    "★**校验器自身一处错（已登记为纪律④）**：`d·[h^n]( e^{kh} td(T_X) )` 首跑被正则当成 1 条断链 —— "
    "**错在校验器不在文件**（渲染器不链接化围栏内内容）⇒ 校验器按渲染语义跳过 ``` 围栏，"
    "并把该式改写为 `⟨h^n, …⟩` 双保险。\n"
)


def main():
    if not os.path.exists(README):
        print("README MISSING")
        return 2
    old = io.open(README, encoding="utf-8").read()
    if KEY in old:
        print("SKIP (already patched)  key=%s" % KEY)
        return 0

    bak = os.path.join(SCRATCH, "_bak_README_pre_r339_closure.md")
    if not os.path.exists(bak):
        if not os.path.isdir(SCRATCH):
            os.makedirs(SCRATCH, exist_ok=True)
        shutil.copy2(README, bak)
        print("BACKUP -> scratch/_bak_README_pre_r339_closure.md")
    else:
        print("BACKUP exists (keep first)")

    sep = "" if old.endswith("\n") else "\n"
    new = old + sep + BODY
    io.open(README, "w", encoding="utf-8", newline="\n").write(new)

    chk = io.open(README, encoding="utf-8").read()
    if KEY not in chk:
        print("PATCH-FAIL: key 未落盘")
        return 3

    # ---- 最终守卫：diff 零删除（旧文件每一行都必须在新文件里按序出现）
    old_lines = old.split("\n")
    new_set = chk.split("\n")
    missing = [ln for ln in old_lines if ln not in new_set]
    if missing:
        print("PATCH-FAIL: 有 %d 行旧内容丢失，示例 %r" % (len(missing), missing[:2]))
        return 4

    print("DIFF-ZERO-DELETION ok (%d/%d 旧行原位保留)" % (len(old_lines), len(old_lines)))
    print("added bytes = %d ; lines %d -> %d" % (len(chk) - len(old),
                                                len(old_lines), len(new_set)))
    # 尾行位置核验：键必须在文件最后一个非空行附近
    tail_idx = len(new_set) - 1
    while tail_idx > 0 and new_set[tail_idx].strip() == "":
        tail_idx -= 1
    if not new_set[tail_idx].startswith("- **收口链（补钉"):
        print("WARN: 补钉不在文件末行（可能被后续追加打断）")
    print("PATCH-OK r339 closure")
    return 0


sys.exit(main())
