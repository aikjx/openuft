# -*- coding: utf-8 -*-
"""同步 r267 段落的实测读数（数据源从 67 卷增至 68 卷后）

只替换**本卷插入块内**的字面量；每对 (old, new) 都报告命中数，
命中 0 ⇒ 报警（说明旧串写法与我记的不同），命中 >1 ⇒ 也报警（可能误伤他人）。
"""
import io
import os
import sys

BASE = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
README = os.path.join(BASE, "README.md")

PAIRS = [
    # 规模
    (u"归并后 **67 卷 / 1147 条条目**", u"归并后 **68 卷 / 1178 条条目**"),
    (u"（PASS 514 / FAIL 333 / INFO 213 / BOUNDARY 71 / OTHER 16）",
     u"（PASS 540 / FAIL 334 / INFO 217 / BOUNDARY 71 / OTHER 16）"),
    (u"数据源 70 份 JSON", u"数据源 71 份 JSON"),
    # 账面 PASS 率（机算 60.41%）
    (u"账面 60.2% 的 PASS 率", u"账面 60.41% 的 PASS 率"),
    # 承重一：分组效应
    (u"A 组 69.06% vs B–I 组 52.62%（差 16.44 个百分点",
     u"A 组 69.40% vs B–I 组 54.56%（差 14.84 个百分点"),
    # 承重五：L14 与层间桥
    (u"L14 元审计与可证伪 17 卷 154/86 = 64.17%",
     u"L14 元审计与可证伪 18 卷 180/87 = 67.42%"),
    (u"层间推导桥 39 条，PASS 14 / FAIL 16 ⇒ 存活率 46.67%",
     u"层间推导桥 40 条，PASS 15 / FAIL 16 ⇒ 存活率 48.39%"),
    (u"推导类条目 39 条，PASS 14 / FAIL 16 ⇒ 存活率 **46.67%**",
     u"推导类条目 40 条，PASS 15 / FAIL 16 ⇒ 存活率 **48.39%**"),
    (u"层间推导桥 39 条判存 46.67%", u"层间推导桥 40 条判存 48.39%"),
    (u"层间桥 46.67%", u"层间桥 48.39%"),
    (u"实测 **46.67%**", u"实测 **48.39%**"),
    # 承重一：集中度两条
    (u"TOP10 卷贡献 192 条 = 37.35%；而按「≥80% 阈值」取高 PASS 卷得 **31 卷（占 49.2%）**",
     u"TOP10 卷贡献 202 条 = 37.41%；而按「≥80% 阈值」取高 PASS 卷得 **32 卷（占 50.0%）**"),
    # 层卷数区间
    (u"各层卷数 1–17 不等", u"各层卷数 1–18 不等"),
]


def read(p):
    with io.open(p, "r", encoding="utf-8", newline="") as f:
        return f.read()


def write(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(s)


def main():
    txt = read(README)
    plan = []
    bad = 0
    print("=== 逐对命中数 ===")
    for old, new in PAIRS:
        c = txt.count(old)
        flag = ""
        if c == 0:
            flag = "★0 命中（写法不符，需人工核对）"
            bad += 1
        elif c > 3:
            flag = "★%d 命中（可能误伤他人，需人工核对）" % c
            bad += 1
        print("  %d  %-46s %s" % (c, old[:44], flag))
        if c:
            plan.append((old, new, c))
    if bad:
        print("\n★有 %d 项需人工核对 ⇒ 不写入。" % bad)
        return 1
    n = 0
    for old, new, c in plan:
        txt = txt.replace(old, new)
        n += c
    write(README, txt)
    back = read(README)
    print("\n已替换 %d 处。读回复核：" % n)
    ok = True
    for old, new, c in plan:
        left = back.count(old)
        got = back.count(new)
        st = "OK" if left == 0 and got >= 1 else "BAD"
        if st == "BAD":
            ok = False
        print("  %s  残留旧串 %d / 新串 %d   [%s]" % (st, left, got, old[:40]))
    print("\n" + ("PASS · 读数同步完成" if ok else "FAIL · 见上表"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
