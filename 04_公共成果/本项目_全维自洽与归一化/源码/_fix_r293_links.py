# -*- coding: utf-8 -*-
"""r293 附带：README 历史断链修复（5 类，8 处）

只改链接目标字符串，不改任何正文文字；每处替换前后计数必须一致；
diff 只允许出现「被修复的那几行」，其余行零改动。

断链成因（本库已登记的「判定册目录不统一」）：
  r243/r244/r245 判定册实际落在 数据/ 而非 判定/（r245–r273 均如此）
  r258 数据侧只有 .json 与 _report.txt，.md 实为落在 数据/ 的判定册；另有 1 处后缀重复 .md.md
"""
import difflib
import io
import os
import sys

ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
README = os.path.join(ROOT, "README.md")
BAK = os.path.join(ROOT, "_bak_README_pre_linkfix.md")

R258 = ("暗能量与宇宙常数层_Lambda即挠率改名与零点能灾难未绕开_"
        "三候选跨121量级与w-1定义恒等式_精算与可视化_2026-10-31")

REPL = [
    # (old, new, 期望替换次数)
    ("数据/判定_TUFT-r258_" + R258 + ".md.md",
     "数据/判定_TUFT-r258_" + R258 + ".md", 1),
    ("数据/TUFT-r258_" + R258 + ".md",
     "数据/判定_TUFT-r258_" + R258 + ".md", 2),
    ("判定/判定_TUFT-r243_", "数据/判定_TUFT-r243_", 2),
    ("判定/判定_TUFT-r244_", "数据/判定_TUFT-r244_", 2),
    ("判定/判定_TUFT-r245_", "数据/判定_TUFT-r245_", 2),
]


def main():
    old = io.open(README, encoding="utf-8").read()

    if not os.path.exists(BAK):
        with io.open(BAK, "w", encoding="utf-8") as f:
            f.write(old)
        print("[bak] 已创建:", BAK)
    else:
        print("[bak] 既有备份保留（不覆盖）")

    txt = old
    ok = True
    for o, n, want in REPL:
        got = txt.count(o)
        if got != want:
            # 已修复过（got==0）视为幂等通过
            if got == 0:
                print("[skip] 已无此串（可能已修复）: %s…" % o[:34])
                continue
            print("FAIL 计数不符 %d != %d : %s…" % (got, want, o[:34]))
            ok = False
            continue
        txt = txt.replace(o, n)
        print("[fix ] %d 处 : %s… → %s…" % (want, o[:30], n[:30]))

    if txt == old:
        print("[write] 无变化，不写盘")
    else:
        with io.open(README, "w", encoding="utf-8") as f:
            f.write(txt)
        print("[write] 已写盘")

    new = io.open(README, encoding="utf-8").read()

    # diff 归因：被删行必须只含被修复的串
    ol, nl = old.split("\n"), new.split("\n")
    sm = difflib.SequenceMatcher(None, ol, nl, autojunk=False)
    del_lines = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ("delete", "replace"):
            del_lines.extend(ol[i1:i2])
    print("[diff] 改动行数 = %d" % len(del_lines))
    keys = ["r243", "r244", "r245", "r258"]
    for ln in del_lines:
        hit = [k for k in keys if k in ln]
        print("   - 归属 %s : %s…" % (hit or ["??"], ln[:70]))
        if not hit:
            ok = False

    # 行数守恒
    print("[diff] 行数 %d → %d" % (len(ol), len(nl)))
    if len(ol) != len(nl):
        print("FAIL 行数变化（纯替换不应改变行数）")
        ok = False

    # r293 四处仍在
    for name, key in [("源码树", "│   ├── TUFT-r293_"), ("判定树", "├── 判定_TUFT-r293_"),
                      ("compact", "- **r293（2026-11-01）"), ("detail", "### r293 · 2026-11-01")]:
        c = new.count(key)
        print("[keep] %-8s count=%d %s" % (name, c, "OK" if c == 1 else "BAD"))
        if c != 1:
            ok = False

    print("LINKFIX-%s" % ("OK" if ok else "FAIL"))
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
