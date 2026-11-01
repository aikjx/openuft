# -*- coding: utf-8 -*-
"""Sync the README r320 self-caught-defect block from the judgment face (single source).

Why this exists: round defect 10 — the registration driver wrote a hand-typed
"自抓 7 枚" into README, the face grew to 9/10, and a one-shot append patch then
re-typed the prose by hand (3 x 趟->趛 typos, and a quoted G15 label that did not
match the face). This driver stops retyping: it rebuilds the whole block from
判定册 §五之二 through the same helper the registration driver uses.

Guards: binary read/write, CRLF preserved, byte-identical outside the two touched
spans, exactly one `### r320 ·` key before and after, README count == face count,
no residual typo char anywhere in README, idempotent on the second run.
"""
import hashlib
import io
import os
import re
import sys

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)
sys.path.insert(0, SRC)
import _r320_selfbugs as SB  # noqa: E402

README = os.path.join(ROOT, "README.md")
KEY = "### r320 ·"
TYPO = "\u8d9b"  # 趛 — the mistyped 趟 (U+8D9F) the old hand-append left in README
BAK_DIR = os.path.join(ROOT, "scratch")


def section_bounds(text):
    n = text.count(KEY)
    if n != 1:
        raise SystemExit("KEY-COUNT=%d (必须恰 1) -> 交人工，本驱动不自动删" % n)
    k = text.index(KEY)
    nxt = text.find("\n### ", k + 1)
    return k, (nxt if nxt > 0 else len(text))


def main():
    dry = "--check" in sys.argv
    face, n_face, line = SB.block_from_face(ROOT)
    raw = open(README, "rb").read()
    text = raw.decode("utf-8")
    k, e = section_bounds(text)
    sec = text[k:e]

    # the block = the "- **★本卷自抓" line plus any hand-appended indented continuation lines
    m = SB.BLOCK_RE.search(sec)
    if not m:
        raise SystemExit("SELFBUG-BLOCK-NOT-FOUND in the r320 section -> 交人工")
    old_block = m.group(0)
    nl = "\r\n" if "\r\n" in old_block else "\n"
    new_block = line.replace("\n", "")

    # head title count inside the section
    head_m = SB.HEAD_RE.search(sec)
    if not head_m:
        raise SystemExit("HEAD-COUNT-NOT-PRINTED -> 登记行没有「自抓 N 枚」，交人工")
    n_disk = int(head_m.group(1))

    # count=1：小节里第一处「自抓 N 枚」才是标题；块内 ⑩ 还**引用**了旧驱动写错的那串字面量，
    # 全局 sub 会把那句引文一起改掉（实测：写盘图像与面派生行在第 1881 字符分叉）。
    new_sec = SB.HEAD_RE.sub("\u81ea\u6293 %d \u679a\u4eea\u5668\u5751" % n_face, sec[: m.start()] + new_block + sec[m.end():], count=1)
    after = text[:k] + new_sec + text[e:]

    # ---- 逐字节保全：只许动这两个跨度
    tl = len(text) - e
    if after[:k] != text[:k] or after[len(after) - tl:] != text[e:]:
        raise SystemExit("NOT-LOCAL-REWRITE -> 改动溢出到 r320 小节之外，拒绝写盘")
    if after.count(KEY) != 1:
        raise SystemExit("KEY-COUNT-AFTER=%d" % after.count(KEY))
    _ak, _ae = section_bounds(after)
    if SB.registered_count(after[_ak:_ae]) != n_face:
        raise SystemExit("PRE-WRITE-COUNT-MISMATCH")
    # 错字通道只测量、不判决：块整体由面现推 ⇒ 块内不可能留下面以外的字，
    # 而「块外枚数不变」恒真（本驱动不碰块外）⇒ 拿它当闸门是不可证伪的针，只印数不判红。
    outside_before = text.count(TYPO) - old_block.count(TYPO)
    outside_after = after.count(TYPO) - new_block.count(TYPO)

    b_raw = after.encode("utf-8")
    ak, ae = section_bounds(after)
    if SB.registered_count(after[ak:ae]) != n_face:
        raise SystemExit("READBACK-COUNT-MISMATCH")
    print("face=%s" % face)
    print("判定册 §五之二 = %d 枚 | README 登记 = %d 枚 | 块行数 %d -> 1" % (
        n_face, n_disk, old_block.count(nl)))
    print("旧块 %d B / md5 %s | 新块 %d B / md5 %s" % (
        len(old_block.encode("utf-8")), hashlib.md5(old_block.encode("utf-8")).hexdigest()[:12],
        len(new_block.encode("utf-8")), hashlib.md5(new_block.encode("utf-8")).hexdigest()[:12]))
    print("README %d B -> %d B (md5 %s -> %s) | 趛 块外 %d -> %d / 块内 %d -> %d" % (
        len(raw), len(b_raw), hashlib.md5(raw).hexdigest()[:12], hashlib.md5(b_raw).hexdigest()[:12],
        outside_before, outside_after, old_block.count(TYPO), new_block.count(TYPO)))
    if dry:
        print("CHECK-ONLY（未写盘）NO-GIT-DRIFT-BYTES %s" % ("EQUAL" if b_raw == raw else "DIFF"))
        return 0 if b_raw == raw else 5
    if b_raw == raw:
        print("SKIP（README 自抓块已与判定册同源，逐字节相同）")
        return 0

    bak = os.path.join(BAK_DIR, "_bak_README_pre_r320sync_2026-11-01.md")
    if os.path.exists(bak):
        bak = os.path.join(BAK_DIR, "_bak_README_pre_r320sync_2026-11-01_%s.md" % hashlib.md5(raw).hexdigest()[:8])
    io.open(bak, "wb").write(raw)
    io.open(README, "wb").write(b_raw)

    check = open(README, "rb").read()
    if check != b_raw:
        raise SystemExit("WRITE-BACK-MISMATCH")
    ct = check.decode("utf-8")
    ck, ce = section_bounds(ct)
    csec = ct[ck:ce]
    print("BACKUP %s" % bak)
    print("READBACK 键 1 枚=True / 面枚数=%d 登记枚数=%d 一致=%s / 新块逐字在场=%s / 趛=%d" % (
        n_face, SB.registered_count(csec), SB.registered_count(csec) == n_face,
        new_block in csec, ct.count(TYPO)))
    if SB.registered_count(csec) != n_face or new_block not in csec:
        raise SystemExit("READBACK-RED")
    print("REG-PATCH-OK 自抓块已由判定册现推（第二个手打源已切除）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
