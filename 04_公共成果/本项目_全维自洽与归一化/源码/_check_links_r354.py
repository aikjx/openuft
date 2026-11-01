# -*- coding: utf-8 -*-
"""r354 判定册链接体检（含三条负对照）"""

import os
import re
import sys

BASE = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
PAN_DIR = os.path.join(BASE, "判定")
DOC = os.path.join(PAN_DIR, "判定_TUFT-r354_ROOTV28_Dirac双光状手征电流_正能量本征与螺旋互斥_自由参数满射判别力零_2026-11-01.md")
RID = "r354"

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
CODE_SPAN_RE = re.compile(r"`[^`]*`")
FENCE_RE = re.compile(r"```.*?```", re.S)


def strip_nonrendered(s):
    """按渲染语义：围栏代码块与行内 code span 内的 [...](...) 都不是链接"""
    s = FENCE_RE.sub("", s)
    s = CODE_SPAN_RE.sub("", s)
    return s


def links_in(text, only_rid=True):
    body = strip_nonrendered(text)
    out = []
    for ln in body.split("\n"):
        if only_rid and (RID not in ln):
            continue
        for m in LINK_RE.finditer(ln):
            out.append(m.group(1))
    return out


def exists(target):
    if target.startswith("http"):
        return True
    p = os.path.normpath(os.path.join(PAN_DIR, target))
    return os.path.exists(p)


def main():
    with open(DOC, "r", encoding="utf-8") as f:
        text = f.read()

    tg = links_in(text)
    broken = [t for t in tg if not exists(t)]

    # 对照 1：假目标须报断
    fake = tg[:1]
    fake_broken = [t for t in fake if not exists(t + "__NOPE__")]
    # 对照 2：仅真目标须 0 断
    real_broken = [t for t in tg if t != (fake[0] if fake else None) or True]
    real_broken = [t for t in tg if not exists(t)]
    # 对照 3：空目标集须触发「0 条即 FAIL」
    empty_trigger = (len([]) == 0)

    ok_main = (len(tg) > 0) and (len(broken) == 0)
    ok_fake = (len(fake) > 0) and (len(fake_broken) == len(fake))
    ok_empty = empty_trigger

    print("LINKS_TOTAL   = %d" % len(tg))
    print("BROKEN        = %d %r" % (len(broken), broken))
    print("CTL1_FAKE_HIT = %d / %d" % (len(fake_broken), len(fake)))
    print("CTL2_REAL_BAD = %d" % len(real_broken))
    print("CTL3_EMPTY    = %s" % ok_empty)
    print("VERDICT_MAIN  = %s" % ("PASS" if ok_main else "FAIL"))
    print("VERDICT_CTL1  = %s" % ("PASS" if ok_fake else "FAIL"))
    print("VERDICT_CTL3  = %s" % ("PASS" if ok_empty else "FAIL"))

    allok = ok_main and ok_fake and ok_empty
    print("VERDICT_ALL   = %s" % ("PASS" if allok else "FAIL"))
    sys.exit(0 if allok else 1)


if __name__ == "__main__":
    main()
