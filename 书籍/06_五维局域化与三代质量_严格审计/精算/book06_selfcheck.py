# -*- coding: utf-8 -*-
"""《05…》第 06 部书籍自审器：把"书上写的"与"盘上有的"逐项对拍

只读：不改任何被审字节。
检查项
  C1 件数：README＋论文＋书稿 10＋精算 5＋本脚本＋本 stdout ＝ 19
  C2 精算两份脚本的 SHA256 前 16 位与 _manifest.md 一致
  C3 两份 stdout 均含 "29/29" 与 "10/10"
  C4 36 个关键数字在正文（README＋论文＋书稿）中至少出现一次
  C5 判词两条均出现，且 "NO_FOUR_FORCE_UNIFICATION" 出现
  C6 无西里尔字母残留、无 TODO/XXX 占位
  C7 书籍总 README 的登记表已含本书一行
"""
import hashlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # 06 书目录
BOOKS = os.path.dirname(ROOT)                                       # openuft/书籍

results = []


def check(name, cond, note=""):
    results.append((name, "成立" if cond else "不成立", note))
    print(("[成立] " if cond else "[不成立] ") + name + "  " + note)


def all_md_text():
    parts = []
    for dirpath, _, files in os.walk(ROOT):
        for f in files:
            if f.endswith(".md") and f != "_manifest.md":
                with open(os.path.join(dirpath, f), encoding="utf-8") as fh:
                    parts.append(fh.read())
    return "\n".join(parts)


# ---------- C1 件数 ----------
files = []
for dirpath, _, fs in os.walk(ROOT):
    for f in fs:
        files.append(os.path.relpath(os.path.join(dirpath, f), ROOT))
shu = [f for f in files if f.startswith("书稿")]
jing = [f for f in files if f.startswith("精算")]
print("件数：总 %d｜书稿 %d｜精算 %d" % (len(files), len(shu), len(jing)))
check("C1 总件数 = 19", len(files) == 19, "现扫 %d" % len(files))
check("C1b 书稿 = 10 件", len(shu) == 10, "现扫 %d" % len(shu))
check("C1c 精算 = 7 件", len(jing) == 7, "现扫 %d（脚本2＋stdout2＋manifest＋自审2）" % len(jing))

# ---------- C2 哈希 ----------
want = {}
with open(os.path.join(ROOT, "精算", "_manifest.md"), encoding="utf-8") as fh:
    for line in fh:
        m = re.match(r"\| `(v\d\d_next_audit\.py)` \| `([0-9A-F]{16})` \|", line.strip())
        if m:
            want[m.group(1)] = m.group(2)
ok2 = True
for fn, h in want.items():
    p = os.path.join(ROOT, "精算", fn)
    if not os.path.exists(p):
        ok2 = False
        print("  缺件：" + fn)
        continue
    real = hashlib.sha256(open(p, "rb").read()).hexdigest().upper()[:16]
    same = (real == h)
    ok2 = ok2 and same
    print("  %s  声明 %s  实算 %s  %s" % (fn, h, real, "一致" if same else "不一致"))
check("C2 脚本哈希与 _manifest.md 一致", ok2, "声明 %d 项" % len(want))

# ---------- C3 stdout ----------
def read(fn):
    p = os.path.join(ROOT, "精算", fn)
    return open(p, encoding="utf-8", errors="replace").read() if os.path.exists(p) else ""

o48, o49 = read("_out_v48.txt"), read("_out_v49.txt")
check("C3a _out_v48.txt 含 29/29", "29/29" in o48, "len=%d" % len(o48))
check("C3b _out_v49.txt 含 10/10", "10/10" in o49, "len=%d" % len(o49))

# ---------- C4 关键数字 ----------
KEYS = ["6.66e-16", "1.08e-19", "4.44e-16", "4.00e-15", "4.86e-17",
        "0.000683979593", "0.023475105342", "0.2852585282", "0.0072206065",
        "5.69e-14", "2.321091e-4", "3.3683e4", "1.8831", "6.18e-4",
        "18.194710", "105.658375", "28.318812", "16.108785",
        "0.0866%", "6.1292%", "19.5%", "174103.83", "59%",
        "4.38e-10", "2.16e-7", "5.50e-6", "1.47e-3", "3.33e-16",
        "8.42e-16", "1.01e-16", "0.0072206065", "4.89e-14",
        "0.518453151905", "7.260385", "1776.93", "246.22"]
text = all_md_text()
missing = [k for k in KEYS if k not in text]
check("C4 36 个关键数字全部有正文载体", not missing, "缺 %d：%s" % (len(missing), missing))

# ---------- C5 判词 ----------
need = ["NO_FOUR_FORCE_UNIFICATION", "V49_UNIVERSAL_LAMBDA_DEGENERATES",
        "THREE_Z_FITTED_NOT_PREDICTED"]
check("C5 判词三条均出现", all(n in text for n in need), str([n for n in need if n not in text]))

# ---------- C6 洁净 ----------
bad = re.findall(r"[\u0400-\u04FF]", text)
check("C6a 无西里尔字母残留", not bad, "命中 %d 处" % len(bad))
check("C6b 无 TODO/XXX 占位", ("TODO" not in text) and ("XXX" not in text), "")

# ---------- C7 总登记表 ----------
reg = open(os.path.join(BOOKS, "README.md"), encoding="utf-8").read()
check("C7 书籍总 README 已登记本书", "06_五维局域化与三代质量_严格审计" in reg, "")

print("=" * 78)
n = sum(1 for r in results if r[1] == "成立")
print("汇总：%d/%d 项自审成立" % (n, len(results)))
print("判词：BOOK06_SELFCHECK_%d_%d__NO_FOUR_FORCE_UNIFICATION" % (n, len(results)))
sys.exit(0 if n == len(results) else 1)
