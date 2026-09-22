# -*- coding: utf-8 -*-
"""
utf8_stdout_守卫 —— 全库 Python 引擎的 stdout UTF-8 守卫批量修复
================================================================

背景（真缺陷，非风格问题）
    中文 Windows 控制台默认 GBK。任何向 stdout 打印非 GBK 字符（⇒ ² ℏ ✓ …）的脚本
    都会 UnicodeEncodeError 崩溃 ⇒ **引擎结果无法被人类复现**。本项目已因此类缺陷
    修复过 5 处（verify_core / 定理D / 判据校准 / 求导验证精算 / S13代入定理D），
    但普查发现它其实是全域性的：`02_共享基础/公共计算/源码` 25 处、
    `S13/07_计算复现/源码` 9 处，合计 34 处。

设计原则（对齐本项目既有治理教训）
    1. **只修实证失败的**：逐个 test-run，只有真的抛 UnicodeEncodeError 才动手；
       不做"看起来会崩"的静态猜测（那会误伤大量文件）。
    2. **幂等**：插入块带标记 MARK；已含 MARK 的文件跳过；重复 --apply 不会重复插入。
    3. **精确可回退**：--revert 只删 MARK 块，不动其它任何内容。
    4. **拒绝而非猜测**：找不到安全插入点（首个 import 块末尾）的文件记 SKIP 并报告。
    5. 排除 `90_历史归档/`（归档语料不改）与 `_` 前缀的临时脚本。

用法
    python utf8_stdout_守卫.py --check      # 只扫描报告（默认）
    python utf8_stdout_守卫.py --apply      # 给实证失败者插入守卫
    python utf8_stdout_守卫.py --revert     # 按标记精确移除
    python utf8_stdout_守卫.py --check --root <目录>   # 限定扫描根

产物：`_utf8守卫报告.json`（与脚本同目录）
"""
import io
import json
import os
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

MARK = "# [UTF8-GUARD v1]"
GUARD = (
    MARK + "\n"
    "import sys as _sys_utf8\n"
    "try:\n"
    "    _sys_utf8.stdout.reconfigure(encoding=\"utf-8\", errors=\"replace\")\n"
    "except Exception:\n"
    "    pass\n"
)

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SKIP_DIRS = ("90_历史归档", "__pycache__", ".git")
REPORT = os.path.join(HERE, "_utf8守卫报告.json")


def candidates(root):
    out = []
    for d, subs, files in os.walk(root):
        if any(s in d for s in SKIP_DIRS):
            continue
        subs[:] = [s for s in subs if s not in SKIP_DIRS]
        for f in files:
            if f.endswith(".py") and not f.startswith("_") and f != os.path.basename(__file__):
                out.append(os.path.join(d, f))
    return sorted(out)


def read(p):
    with io.open(p, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def test_run(path):
    """返回 (status, detail)。status: ok / unicode_fail / other_fail / timeout"""
    cwd = os.path.dirname(path)
    try:
        pr = subprocess.run([sys.executable, "-B", os.path.basename(path)],
                            cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            timeout=300)
    except subprocess.TimeoutExpired:
        return "timeout", ">300s"
    txt = pr.stdout.decode("utf-8", errors="replace")
    if pr.returncode == 0:
        return "ok", ""
    if "UnicodeEncodeError" in txt:
        line = [l for l in txt.splitlines() if "UnicodeEncodeError" in l]
        return "unicode_fail", (line[-1].strip() if line else "UnicodeEncodeError")
    tail = [l for l in txt.splitlines() if l.strip()]
    return "other_fail", (tail[-1].strip()[:120] if tail else "rc=%d" % pr.returncode)


def import_block_end(src):
    """返回首个顶层 import/from 块结束后的行号（0-based，插入点）。找不到返回 None。"""
    lines = src.splitlines(True)
    last_import = None
    for i, ln in enumerate(lines):
        s = ln.strip()
        if s.startswith("import ") or s.startswith("from "):
            last_import = i
        elif s.startswith(("try:", "except", ")", "]", "}")) or s.startswith("#") or s == "":
            continue
        elif last_import is not None:
            break
    if last_import is None:
        return None
    # 跳过 import 块后紧邻的续行 / 括号闭合
    j = last_import + 1
    while j < len(lines) and (lines[j].startswith((" ", "\t")) or lines[j].strip() == ""):
        j += 1
    return j


def insert_guard(path):
    src = read(path)
    if MARK in src:
        return "already"
    pos = import_block_end(src)
    if pos is None:
        return "skip_no_import"
    lines = src.splitlines(True)
    lines.insert(pos, GUARD + "\n")
    with io.open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write("".join(lines))
    return "inserted"


def revert_guard(path):
    src = read(path)
    if MARK not in src:
        return "no_mark"
    lines = src.splitlines(True)
    out = []
    i = 0
    removed = 0
    while i < len(lines):
        if lines[i].startswith(MARK):
            blk = "".join(lines[i:i + 6])
            if blk.rstrip("\n") == GUARD.rstrip("\n").rstrip():
                i += 7 if lines[i + 6:i + 7] == ["\n"] else 6
                removed += 1
                continue
        out.append(lines[i])
        i += 1
    if removed == 0:
        return "skip_shape"
    with io.open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write("".join(out))
    return "reverted"


def main():
    mode = "check"
    root = DEFAULT_ROOT
    args = sys.argv[1:]
    if "--apply" in args:
        mode = "apply"
    if "--revert" in args:
        mode = "revert"
    if "--root" in args:
        root = os.path.abspath(args[args.index("--root") + 1])

    files = candidates(root)
    rows = []
    if mode == "revert":
        for p in files:
            r = revert_guard(p)
            if r == "reverted":
                rows.append({"file": os.path.relpath(p, root), "action": "reverted"})
        print("[revert] 移除守卫 %d 个文件" % len(rows))
    elif mode == "apply":
        checked = []
        for p in files:
            if MARK in read(p):
                continue
            st, detail = test_run(p)
            checked.append((p, st, detail))
        fails = [(p, d) for p, st, d in checked if st == "unicode_fail"]
        for p, d in fails:
            r = insert_guard(p)
            rows.append({"file": os.path.relpath(p, root), "action": r, "detail": d})
        n_ins = sum(1 for r in rows if r["action"] == "inserted")
        print("[apply] 实证失败 %d 个；插入守卫 %d 个；跳过 %d 个" % (
            len(fails), n_ins, len(rows) - n_ins))
    else:
        for p in files:
            if MARK in read(p):
                rows.append({"file": os.path.relpath(p, root), "status": "guarded"})
                continue
            st, detail = test_run(p)
            rows.append({"file": os.path.relpath(p, root), "status": st, "detail": detail})
        n_fail = sum(1 for r in rows if r["status"] == "unicode_fail")
        n_other = sum(1 for r in rows if r["status"] == "other_fail")
        n_ok = sum(1 for r in rows if r["status"] == "ok")
        n_gd = sum(1 for r in rows if r["status"] == "guarded")
        n_to = sum(1 for r in rows if r["status"] == "timeout")
        print("[check] 扫描 %d 个脚本：OK=%d 已守卫=%d **Unicode失败=%d** 其它失败=%d 超时=%d" % (
            len(rows), n_ok, n_gd, n_fail, n_other, n_to))
        for r in rows:
            if r["status"] in ("unicode_fail", "other_fail", "timeout"):
                print("   %-9s %s  %s" % (r["status"], r["file"], r.get("detail", "")))

    with io.open(REPORT, "w", encoding="utf-8") as fh:
        fh.write(json.dumps({"root": root, "mode": mode, "rows": rows},
                            ensure_ascii=False, indent=2))
    print("报告：%s" % REPORT)


if __name__ == "__main__":
    main()
