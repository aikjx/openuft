# -*- coding: utf-8 -*-
"""
r264 README 注册脚本越界改写 · 定点还原器（幂等）

背景
----
_readme_add_r264.py 在注册本卷条目时，有三处「越界改写他人卷」：

  D1  编号消歧块：DISAMBIG 用前缀
      "> **编号消歧（2026-10-31 撞号第 9 次）**"
      做 replace_first，而该前缀属于 **r262 卷**（「本卷原拟 r256 ⇒ 取 r262」）；
      结果 r262 的整条编号消歧记录被本卷条目覆盖丢失。

  D2  r262 章详节取号行：
      "**下轮从 r263 起**"  →  "**下轮从 r265 起**"

  D3  r263 章详节取号行：
      "**下轮从 r264 复查起**"  →  "**下轮从 r265 复查起**"

D2/D3 属于「回溯改写他人历史记录」：本库纪律是「下轮」指针过期后
用**新增编号消歧条目**纠正，而不是回头改别人章内的取号行。

还原源
------
源码/_scratch_dead/README.before_r264.md（15:20，本卷写入前的真状态）
已用 difflib 全量比对确认：before_r264 → 当前 只有 6 处 opcode，
且并行 r265 会话在该备份之前只做了 4 处纯插入（未触碰 D1/D2/D3 三行）。
⇒ 三行均可从该备份逐字取回，不会回滚掉并行会话的任何字节。

用法
----
    python -X utf8 源码/_run_fix_r264.py
"""
import io
import os
import sys
import hashlib
import shutil
import difflib

HERE = os.path.dirname(os.path.abspath(__file__))
README = os.path.normpath(os.path.join(HERE, "..", "README.md"))
BAK = os.path.join(HERE, "_scratch_dead", "README.before_r264.md")
NEWB = os.path.join(HERE, "_scratch_dead", "README.before_fix_r264.md")


def read_text(p):
    with io.open(p, encoding="utf-8") as f:
        return f.read()


def write_text(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(s)


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]


def find_from(lines, prefix, start=0):
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix):
            return i
    return -1


def main():
    if not os.path.exists(BAK):
        print("MISSING BACKUP: %s" % BAK)
        return 2

    bak = read_text(BAK).split("\n")
    cur = read_text(README).split("\n")
    print("backup lines = %d   current lines = %d" % (len(bak), len(cur)))
    print("sha(current) before fix = %s" % sha(README))

    # ---------- 从备份逐字取回三行 ----------
    i_dis = find_from(bak, "> **编号消歧（2026-10-31 撞号第 9 次）**")
    i_262 = find_from(bak, "- **取号（撞号第 9 次）**")
    i_263 = find_from(bak, "- **取号**：2026-10-31 实测三树最大占用 **r262**", start=9000)
    print("backup idx: disambig=%d  p262=%d  p263=%d" % (i_dis, i_262, i_263))
    if min(i_dis, i_262, i_263) < 0:
        print("FAIL: cannot locate reference lines in backup")
        return 2

    L_dis = bak[i_dis]
    L_262 = bak[i_262]
    L_263 = bak[i_263]

    log = []

    # ---------- D1：把 r262 的编号消歧条插回 ----------
    n_dis = sum(1 for l in cur if l.startswith("> **编号消歧（2026-10-31 撞号第 9 次）**"))
    if L_dis in cur:
        log.append(("D1", "skip", "r262 note already present (count=%d)" % n_dis))
    else:
        # 插到本卷（· r264 卷）那条之前，复现原始版面
        mine = -1
        for i, l in enumerate(cur):
            if "撞号第 9 次 · r264 卷）**" in l:
                mine = i
                break
        if mine < 0:
            log.append(("D1", "FAIL", "cannot find my own r264 disambig line"))
            return 2
        cur.insert(mine, L_dis)
        log.append(("D1", "fixed", "inserted r262 note at index %d" % mine))

    # ---------- D2 / D3：章内取号行逐字还原 ----------
    def restore(tag, prefix, target, start=0):
        hit = -1
        for i in range(start, len(cur)):
            if cur[i].startswith(prefix):
                hit = i
                break
        if hit < 0:
            log.append((tag, "FAIL", "prefix not found: %s" % prefix[:40]))
            return False
        if cur[hit] == target:
            log.append((tag, "skip", "already restored"))
            return True
        old = cur[hit]
        cur[hit] = target
        log.append((tag, "fixed", "line %d restored" % (hit + 1)))
        log.append((tag, "  old", old[-60:]))
        log.append((tag, "  new", target[-60:]))
        return True

    ok = True
    ok &= restore("D2", "- **取号（撞号第 9 次）**", L_262, start=9000)
    ok &= restore("D3", "- **取号**：2026-10-31 实测三树最大占用 **r262**", L_263, start=9000)
    if not ok:
        print("FAIL during restore")
        return 2

    # ---------- 落盘 ----------
    if not os.path.exists(NEWB):
        shutil.copyfile(README, NEWB)
        print("new backup written: %s" % os.path.basename(NEWB))
    write_text(README, "\n".join(cur))
    print("sha(current) after  fix = %s" % sha(README))

    # ---------- 验证 ----------
    print("\n==== VERIFY ====")
    new = read_text(README).split("\n")
    chk = []

    chk.append(("r262 编号消歧条 计数==1",
                sum(1 for l in new if l == L_dis) == 1))
    chk.append(("r264 编号消歧条 计数==1",
                sum(1 for l in new if "撞号第 9 次 · r264 卷）**" in l) == 1))
    chk.append(("r258 编号消歧(第8次) 未动 计数==1",
                sum(1 for l in new if "撞号第 8 次）**" in l) == 1))
    chk.append(("r255 编号消歧(10:10) 未动 计数==1",
                sum(1 for l in new if "编号消歧（2026-10-31 10:10 更新）**" in l) == 1))
    chk.append(("r265 编号消歧(第10次) 未动 计数==1",
                sum(1 for l in new if "撞号第 10 次）**" in l) == 1))
    chk.append(("r262 章取号行 已还原",
                sum(1 for l in new if l == L_262) == 1))
    chk.append(("r263 章取号行 已还原",
                sum(1 for l in new if l == L_263) == 1))
    chk.append(("r264 条目 计数==1（增量章条目）",
                sum(1 for l in new if l.startswith("- **r264（2026-10-31）· 自由参数总账层")) == 1))
    chk.append(("r264 详节标题 计数==1",
                sum(1 for l in new if l.startswith("### r264 · 2026-10-31 · 自由参数总账层")) == 1))
    chk.append(("r264 源码树 计数==1",
                sum(1 for l in new if "TUFT-r264_自由参数总账层" in l and l.startswith("│   ├──")) == 1))
    chk.append(("r264 判定树 计数==1",
                sum(1 for l in new if l.startswith("├── 判定_TUFT-r264_")) == 1))
    chk.append(("r265 条目 未动 计数==1",
                sum(1 for l in new if l.startswith("- **r265（2026-10-31）· 引力波预言层")) == 1))
    chk.append(("r262 条目 未动 计数==1",
                sum(1 for l in new if l.startswith("- **r262（2026-10-31）· 重子不对称层")) == 1))
    chk.append(("r263 条目 未动 计数==1",
                sum(1 for l in new if l.startswith("- **r263（2026-10-31）· 攻坚任务书审计")) == 1))

    allok = True
    for name, v in chk:
        print("  [%s] %s" % ("OK " if v else "BAD", name))
        allok &= v

    # 与备份再比一次：剩余差异应只剩「本卷自己」的 5 处 + r262 note 插入 1 处
    sm = difflib.SequenceMatcher(None, bak, new, autojunk=False)
    ops = [o for o in sm.get_opcodes() if o[0] != "equal"]
    print("\n  remaining non-equal opcodes vs backup = %d" % len(ops))
    for tag, i1, i2, j1, j2 in ops:
        print("    %-7s bak[%d:%d] -> new[%d:%d]" % (tag, i1, i2, j1, j2))

    print("\nRESULT = %s" % ("ALL OK" if allok else "PROBLEM"))
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
