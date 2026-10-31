# -*- coding: utf-8 -*-
"""
幂等补钉：把被 r264 注册脚本覆盖掉的 **r262 卷编号消歧条** 插回 README。

为什么需要单独一个脚本
----------------------
README.md 是多个并行会话共同追加的共享文件，任何一方都是
「整篇读入 → 修改 → 整篇写出」。因此本补钉即使写入成功，
也可能被随后落盘的并行会话用它的旧副本整篇覆盖。
⇒ 本脚本设计成**可反复运行**，每次运行都：
    1. 重新从磁盘读取当前 README（不依赖任何内存副本）
    2. 若 r262 原条已在 ⇒ 打印 already-present，不做任何写
    3. 若缺失 ⇒ 插到本卷（· r264 卷）那条之前
    4. 落盘后**再从磁盘读回**做机器校验

同时顺带复核 D2/D3（r262 / r263 章内取号行）仍处于已还原状态。

用法
----
    python -X utf8 源码/_run_patch_r262_note.py     （反复运行直到 already-present）
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
README = os.path.normpath(os.path.join(HERE, "..", "README.md"))
BAK = os.path.join(HERE, "_scratch_dead", "README.before_r264.md")


def read_text(p):
    with io.open(p, encoding="utf-8") as f:
        return f.read()


def write_text(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(s)


def pick(lines, prefix, start=0):
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix):
            return i, lines[i]
    return -1, None


def main():
    bak = read_text(BAK).split("\n")

    # 三条「原样」参照行，全部逐字取自本卷写入前的备份
    i, L_dis = pick(bak, "> **编号消歧（2026-10-31 撞号第 9 次）**")
    j, L_262 = pick(bak, "- **取号（撞号第 9 次）**", start=9000)
    k, L_263 = pick(bak, "- **取号**：2026-10-31 实测三树最大占用 **r262**", start=9000)
    if None in (L_dis, L_262, L_263):
        print("FAIL: backup reference lines missing", i, j, k)
        return 2

    # 每次都重新读磁盘
    cur = read_text(README).split("\n")
    print("current lines (fresh read) = %d" % len(cur))

    changed = False

    # ---- D1：r262 编号消歧条 ----
    if L_dis in cur:
        print("[D1] already-present (r262 note in file), nothing to do")
    else:
        mine = -1
        for n, l in enumerate(cur):
            if "撞号第 9 次 · r264 卷）**" in l:
                mine = n
                break
        if mine < 0:
            print("[D1] FAIL: cannot find my own r264 disambig line")
            return 2
        cur.insert(mine, L_dis)
        changed = True
        print("[D1] inserted r262 note before my r264 note (index %d)" % mine)

    # ---- D2 / D3：取号行还原状态复核 ----
    for tag, target in (("D2", L_262), ("D3", L_263)):
        c = sum(1 for l in cur if l == target)
        stale = sum(1 for l in cur if "下轮从 r265 起" in l or "下轮从 r265 复查起" in l)
        ok = (c == 1) and (stale == 0)
        print("[%s] target-count=%d stale-265-pointer-count=%d => %s"
              % (tag, c, stale, "OK" if ok else "NEEDS FIX"))
        if not ok and c == 0:
            # 若被覆盖回「下轮从 r265」，按前缀定位并还原
            pref = target[:22]
            hit = -1
            for n, l in enumerate(cur):
                if l.startswith(pref):
                    hit = n
                    break
            if hit >= 0 and cur[hit] != target:
                cur[hit] = target
                changed = True
                print("[%s] restored at line %d" % (tag, hit + 1))

    if not changed:
        print("\nNo write needed.")
        return 0

    write_text(README, "\n".join(cur))

    # ---- 落盘后从磁盘读回复核 ----
    print("\n==== POST-WRITE VERIFY (fresh read) ====")
    new = read_text(README).split("\n")
    print("lines after write = %d" % len(new))
    results = [
        ("r262 编号消歧条 存在且唯一", sum(1 for l in new if l == L_dis) == 1),
        ("r264 编号消歧条 存在且唯一",
         sum(1 for l in new if "撞号第 9 次 · r264 卷）**" in l) == 1),
        ("r262 章取号行 = 备份原文", sum(1 for l in new if l == L_262) == 1),
        ("r263 章取号行 = 备份原文", sum(1 for l in new if l == L_263) == 1),
        ("无残留的 r265 下轮指针改写",
         sum(1 for l in new if "下轮从 r265 起" in l or "下轮从 r265 复查起" in l) == 0),
        ("r247 条目未被破坏（并行会话产物）",
         sum(1 for l in new if l.startswith("- **r247（2026-10-30）· 引力本质层元审计")) == 1),
        ("r264 条目 唯一",
         sum(1 for l in new if l.startswith("- **r264（2026-10-31）· 自由参数总账层")) == 1),
        ("r265 条目 唯一",
         sum(1 for l in new if l.startswith("- **r265（2026-10-31）· 引力波预言层")) == 1),
    ]
    allok = True
    for name, v in results:
        print("  [%s] %s" % ("OK " if v else "BAD", name))
        allok &= v
    print("\nRESULT = %s" % ("ALL OK" if allok else "PROBLEM"))
    print("(提示：并行会话可能再次整篇覆盖，收口前请再跑一次本脚本确认)")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
