# -*- coding: utf-8 -*-
"""
README 结构完整性全量复核（只读，不改任何文件）

检查项
------
A. 所有 `### rNNN ·` 章标题：编号是否出现重复
B. 所有 `- **rNNN（...）·` 增量章条目：编号是否出现重复
C. 源码树 `│   ├── TUFT-rNNN_` 行：编号是否出现重复
D. 判定树 `├── 判定_TUFT-rNNN_` 行：编号是否出现重复
E. r262 / r264 / r265 / r247 四处是否齐全
F. 死链检查：正文里是否还有 `](判定/判定_TUFT-r264` 这类指向错误目录的链接
G. r262 / r263 章内「取号」行是否仍为原文（未被本卷改写）
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
README = os.path.normpath(os.path.join(HERE, "..", "README.md"))


def read_text(p):
    with io.open(p, encoding="utf-8") as f:
        return f.read()


def ids_from(lines, pat, group=1):
    out = []
    for l in lines:
        m = re.search(pat, l)
        if m:
            out.append(m.group(group))
    return out


def dup_report(name, ids):
    seen = {}
    for x in ids:
        seen[x] = seen.get(x, 0) + 1
    dups = {k: v for k, v in seen.items() if v > 1}
    print("  [%s] %s  共 %d 条，唯一 %d 个，重复 %d 个%s"
          % ("OK " if not dups else "BAD", name, len(ids), len(seen), len(dups),
             "" if not dups else " -> " + str(dups)))
    return not dups


def main():
    s = read_text(README)
    lines = s.split("\n")
    print("README lines = %d, bytes = %d" % (len(lines), len(s.encode("utf-8"))))
    print("\n==== A–D 编号唯一性 ====")
    ok = True
    ok &= dup_report("章标题 ### rNNN",
                     ids_from(lines, r"^### (r\d{3}) · ", 1))
    ok &= dup_report("增量章条目 - **rNNN（",
                     ids_from(lines, r"^- \*\*(r\d{3})（\d{4}-", 1))
    ok &= dup_report("源码树 TUFT-rNNN",
                     ids_from(lines, r"^│   ├── TUFT-(r\d{3})_", 1))
    ok &= dup_report("判定树 判定_TUFT-rNNN",
                     ids_from(lines, r"^├── 判定_TUFT-(r\d{3})_", 1))

    print("\n==== E 本卷与并行会话四处登记 ====")
    for rid in ("r262", "r263", "r264", "r265", "r247"):
        a = sum(1 for l in lines if re.match(r"^### %s · " % rid, l))
        b = sum(1 for l in lines if l.startswith("- **%s（" % rid))
        c = sum(1 for l in lines if l.startswith("│   ├── TUFT-%s_" % rid))
        d = sum(1 for l in lines if l.startswith("├── 判定_TUFT-%s_" % rid))
        good = (a == 1 and b == 1 and c == 1 and d == 1)
        print("  [%s] %s  详节=%d 条目=%d 源码树=%d 判定树=%d"
              % ("OK " if good else "BAD", rid, a, b, c, d))
        ok &= good

    print("\n==== F 死链检查 ====")
    bad = [l for l in lines if "](判定/判定_TUFT-r2" in l]
    print("  [%s] 指向 `判定/判定_TUFT-r2xx` 的死链数 = %d"
          % ("OK " if not bad else "BAD", len(bad)))
    ok &= (len(bad) == 0)

    print("\n==== G r262/r263 章内取号行未被改写 ====")
    stale = [l for l in lines if "下轮从 r265 起" in l or "下轮从 r265 复查起" in l]
    print("  [%s] 残留「下轮从 r265」的旧指针改写数 = %d（应为 0）"
          % ("OK " if not stale else "BAD", len(stale)))
    ok &= (len(stale) == 0)

    print("\n==== r264 下轮指针一致性 ====")
    n266 = sum(1 for l in lines if "下轮从 r266" in l)
    print("  含「下轮从 r266」的行数 = %d" % n266)

    print("\nRESULT = %s" % ("ALL OK" if ok else "PROBLEM"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
