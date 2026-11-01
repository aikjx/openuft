# -*- coding: utf-8 -*-
"""r346 收口补钉：给 数据说明件 追加 §十六 产物（**真链接**，不是裸路径）。

纪律：①幂等（键存在即 SKIP）；②追加前查 `s.endswith('\\n')`（末尾追加会把「无尾换行」变「有尾换行」⇒ diff 报 1 条伪删除）；
③最终守卫 = diff 零删除；④链接一律相对路径真实存在（由 `_check_r346_links.py` 复检）。
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEM = ("TUFT-r346_整数Newton系数是三行初等事实而非几何定理_"
        "分母整除首项定理与判词下调_精算与可视化_2026-11-01")
HTML = "四力统一方程_整数Newton系数_r346可视化_2026-11-01.html"
DOC = os.path.join(ROOT, "数据", STEM + ".md")

KEY = "## 十六、产物"

BLOCK = [
    "",
    "---",
    "",
    "## 十六、产物",
    "",
    "- 源码 [`%s.py`](../源码/%s.py)" % (STEM, STEM),
    "- 数据 [`…json`](../数据/%s.json) / [本说明件](../数据/%s.md) / [`…_report.txt`](../数据/%s_report.txt)" % (STEM, STEM, STEM),
    "- 判定册 [`判定_%s.md`](../判定/判定_%s.md)" % (STEM, STEM),
    "- 交互可视化 [`%s`](../%s)" % (HTML, HTML),
    "  （几何体检 **fig1 70 / fig2 42 / fig3 197 / fig4 107 = 416 图元 0 越界**；"
    "负对照把矩形宽度填 0 ⇒ 精确报 **5 条「宽度为 0 ⇒ 不可见」** + rc=2）",
    "- runner [`_run_r346.py`](../源码/_run_r346.py) · 登记 [`_reg_r346.py`](../源码/_reg_r346.py)",
    "- 链接体检 [`_check_r346_links.py`](../源码/_check_r346_links.py) · 工作日志 [`_log_r346.py`](../源码/_log_r346.py)",
    "",
]

old = io.open(DOC, encoding="utf-8").read()
if KEY in old:
    print("SKIP (already patched)  key=%s" % KEY)
    sys.exit(0)

had_nl = old.endswith("\n")
print("tail-newline before = %s" % had_nl)

body = old if had_nl else old + "\n"
new = body + "\n".join(BLOCK) + "\n"

io.open(DOC, "w", encoding="utf-8").write(new)

chk = io.open(DOC, encoding="utf-8").read()
if chk.count(KEY) != 1:
    print("PATCH-FAIL：验证键不是 1")
    sys.exit(3)

old_l, new_l = old.split("\n"), chk.split("\n")
p = 0
for line in new_l:
    if p < len(old_l) and line == old_l[p]:
        p += 1
if p != len(old_l):
    print("DIFF-DELETION: 只对上 %d/%d 行" % (p, len(old_l)))
    sys.exit(6)
print("DIFF-ZERO-DELETION ok (%d/%d 旧行原位保留)" % (p, len(old_l)))
print("bytes %d -> %d (delta %+d)" % (len(old.encode("utf-8")), len(chk.encode("utf-8")),
                                      len(chk.encode("utf-8")) - len(old.encode("utf-8"))))
print("PATCH-OK r346 数据说明件 §十六 产物")
