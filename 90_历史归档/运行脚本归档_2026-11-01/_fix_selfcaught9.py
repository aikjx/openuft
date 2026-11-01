# -*- coding utf-8 -*-
"""Append self-caught item 9 (worst_rel truncation) to README chapter + daily log."""
import io

README = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\README.md"
LOG = r"D:\a10\aikjx\code\my_lib\.workbuddy\memory\2026-10-25.md"

ITEM9 = ("⑨worst_rel 显示裸截断——key_numbers 快照 [:12] 把 1.78e-08 切成「1.7795663853」"
         "（指数位丢失、量级误导 8 个数量级），而判据互印表正用该快照渲染 ⇒ 改 fmt_rel "
         "科学计数法 + prev_num 省略号标记（登记后复查产物时自抓，重跑 rc=0 四件套已刷新）。")

# --- README ---
t = io.open(README, encoding="utf-8").read()
a = "⑧A2 文案位数不一致（写「17 位」实测 16 位）⇒ 修正为「16 位有效数字（第 17 位起分歧）」。"
if a not in t:
    print("FATAL: readme anchor miss")
    raise SystemExit(3)
if "worst_rel 显示裸截断" in t:
    print("FATAL: item9 already in readme")
    raise SystemExit(4)
t = t.replace(a, a + ITEM9)
h = "- **自抓 5 处（已修，重跑 rc=0）**：①CF 复分数缺"
if h not in t:
    print("FATAL: readme header anchor miss")
    raise SystemExit(5)
t = t.replace(h, "- **自抓 9 处（已修，重跑 rc=0）**：①CF 复分数缺")
io.open(README, "w", encoding="utf-8").write(t)
print("readme ok")

# --- daily log ---
t = io.open(LOG, encoding="utf-8").read()
a2 = "⑧A2 文案位数不一致（写「17 位」实测 16 位）⇒ 修正。"
if a2 not in t:
    print("FATAL: log anchor miss")
    raise SystemExit(6)
if "worst_rel 显示裸截断" in t:
    print("FATAL: item9 already in log")
    raise SystemExit(7)
t = t.replace(a2, a2 + ITEM9)
h2 = "**自抓 8 处（已修，重跑 rc=0）**"
if h2 not in t:
    print("FATAL: log header anchor miss")
    raise SystemExit(8)
t = t.replace(h2, "**自抓 9 处（已修，重跑 rc=0）**")
io.open(LOG, "w", encoding="utf-8").write(t)
print("log ok")
