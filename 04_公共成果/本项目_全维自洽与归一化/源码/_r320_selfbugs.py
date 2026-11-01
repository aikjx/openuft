# -*- coding: utf-8 -*-
"""Single derivation of the r320 self-caught-defect block.

Both the README registration driver (`_reg_r320.py`) and the README sync driver
(`_sync_r320_readme.py`) read the judgment face's section 5.2 through this module,
so the count and the per-item prose can never live in two places again
(round defect 10: a hand-typed copy in README drifted to 7 while the face said 9).

Read-only with respect to the disk: nothing here writes.
"""
import glob
import io
import os
import re

CIRC = "\u2460\u2461\u2462\u2463\u2464\u2465\u2466\u2467\u2468\u2469\u246a\u246b\u246c\u246d\u246e"
HEAD_RE = re.compile(r"\u81ea\u6293 (\d+) \u679a\u4eea\u5668\u5751")
# 块 = 「- **★本卷自抓」那一行 + 任何缩进 4 空格的续行（CRLF / LF / CR 都算换行）。
# 三个消费者（登记驱动、同步驱动、收口复核 W17）必须共用这一把尺，否则两把尺读同一本账会给出两个答案。
BLOCK_RE = re.compile(
    r"^- \*\*\u2605\u672c\u5377\u81ea\u6293[^\r\n]*(?:(?:\r\n|\r|\n) {4}[^\r\n]*)*", re.M
)
LABEL = "\u2605\u672c\u5377\u81ea\u6293"


class SelfBugError(Exception):
    pass


def judgment_text(root):
    hits = glob.glob(os.path.join(root, "\u5224\u5b9a", "\u5224\u5b9a_TUFT-r320_*.md"))
    if len(hits) != 1:
        raise SelfBugError("JUDG-FACE-NOT-UNIQUE hits=%d" % len(hits))
    return os.path.basename(hits[0]), io.open(hits[0], encoding="utf-8").read()


def bullets_from_judgment(ju):
    """(count_printed_in_heading, bullet_prose) — the two must agree or the face is not closed."""
    if "\u4e94\u4e4b\u4e8c" not in ju:
        raise SelfBugError("JUDG-NO-SELFBUG-SECTION")
    blk = ju[ju.index("\u4e94\u4e4b\u4e8c"):]
    if "\n## " in blk:
        blk = blk[: blk.index("\n## ")]
    items = [l[2:] for l in blk.splitlines() if l.startswith("- ")]
    m = re.search(r"\uff08(\d+) \u679a", blk)
    if not m:
        raise SelfBugError("SELFBUG-HEADING-COUNT-NOT-PRINTED")
    n = int(m.group(1))
    if n != len(items) or n < 2:
        raise SelfBugError("SELFBUG-COUNT-UNCLOSED heading=%d bullets=%d" % (n, len(items)))
    if n > len(CIRC):
        raise SelfBugError("SELFBUG-COUNT-OVERFLOW n=%d circ=%d" % (n, len(CIRC)))
    return n, items


def compose_readme_line(n, items):
    # 面侧每条正文自带句号；拼成一整行后「。」+「；」＝「。；」，末条再叠一个「。」＝「。。」
    # ⇒ 组合器负责断句，正文只取其字面内容（面仍是唯一来源，这里不增不减信息）。
    stripped = [b.rstrip("\u3002") for b in items]
    return "- **%s %d \u679a\u4eea\u5668\u5751\uff08\u5224\u5b9a\u518c \u00a7\u4e94\u4e4b\u4e8c\u9010\u6761\u767b\u8bb0，\u5168\u90e8\u5c31\u5730\u4fee\uff09**\uff1a%s" % (
        LABEL,
        n,
        "\uff1b".join("%s %s" % (CIRC[i], b) for i, b in enumerate(stripped)) + "\u3002",
    )


def block_from_face(root):
    """(face_name, n, composed_readme_line) — the only sanctioned source for the README block."""
    face, ju = judgment_text(root)
    n, items = bullets_from_judgment(ju)
    return face, n, compose_readme_line(n, items)


def registered_count(readme_text):
    m = HEAD_RE.search(readme_text)
    return int(m.group(1)) if m else -1


# 行内代码引文：`...`。叠句判据要先豁免它（见 shape_glue）。
CODE_SPAN_RE = re.compile(r"\x60[^\x60]*\x60")
GLUE = ("\u3002\uff1b", "\u3002\u3002")


def shape_glue(block):
    """组合器的断句形状：「。」压在「；」前，或两个「。」相连 ⇒ 判为叠句。

    计数前先豁免行内代码引文：块里 ⑫ 正是**引用**这两个形状（`。；`、`。。`），
    按裸子串数会把缺陷自己的说明判成缺陷——与 ⑩ 引用旧字面量「自抓 7 枚」被 W11
    判成假红是同一枚坑，本轮换了个判据第二次踩。豁免段数一并返回、由判据印出，
    免得「滤掉了」这件事没有读数。

    返回 (命中的形状, 叠句处数, 豁免段数, 豁免后字符数)。
    """
    spans = len(CODE_SPAN_RE.findall(block))
    naked = CODE_SPAN_RE.sub("", block)
    hits = [g for g in GLUE if g in naked]
    return hits, sum(naked.count(g) for g in GLUE), spans, len(naked)
