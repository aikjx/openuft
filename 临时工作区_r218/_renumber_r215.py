# -*- coding utf-8 -*-
"""Renumber my r215 engine -> first empty number (race with parallel sessions)."""
import io
import os

ENG_DIR = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
DATA_DIR = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\数据"
VERD_DIR = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\判定"
ROOT = r"D:\a10\aikjx\code\my_lib\openuft"

OLD_STEM = "TUFT-r215_四力统一方程_定义恒等式零判别力覆盖缺与修复定价"
NEW_N = None

# pick first empty number >= 218
for n in range(218, 240):
    occ = [p for p in (ENG_DIR, DATA_DIR, VERD_DIR)
           if any(("r%d" % n) in f for f in os.listdir(p))]
    if not occ:
        NEW_N = n
        break
if NEW_N is None:
    print("FATAL: no empty number found")
    raise SystemExit(3)

NEW_STEM = "TUFT-r%d_四力统一方程_定义恒等式零判别力覆盖缺与修复定价" % NEW_N
print("target number:", NEW_N)

src = os.path.join(ENG_DIR, OLD_STEM + "_精算_2026-10-26.py")
dst = os.path.join(ENG_DIR, NEW_STEM + "_精算_2026-10-26.py")
if not os.path.exists(src):
    print("FATAL: source engine missing:", src)
    raise SystemExit(4)

t = io.open(src, encoding="utf-8").read()
t = t.replace(OLD_STEM, NEW_STEM)
t = t.replace('"id": "r215"', '"id": "r%d"' % NEW_N)
t = t.replace("编号 r215（", "编号 r%d（".replace("%d", str(NEW_N)) % () if False else "编号 r%d（" % NEW_N)
t = t.replace("r142–r214 相加", "r142–r%d 相加" % (NEW_N - 1))
t = t.replace("本卷顺延取 **r215**", "本卷顺延取 **r%d**" % NEW_N)
t = t.replace("并行 r205–r214 计数归各会话", "并行 r205–r%d 计数归各会话" % (NEW_N - 1))
t = t.replace("r214 被并行《四力统一运动方程_求导证明与力的大小方向距离精算及可视化》占用且\n四件套已落",
              "r214 被并行《四力统一运动方程_求导证明与力的大小方向距离精算及可视化》占用且\n四件套已落")
t = t.replace("并联 r214", "并联 r214")  # noop guard
t = t.replace("r205–r213 已被并行", "r205–r217 已被并行")
t = t.replace("（r213 存在双标题冲突", "（r213/r216 存在同题改名")
t = t.replace("未触碰 r205–r214 并行产物", "未触碰 r205–r%d 并行产物" % (NEW_N - 1))
io.open(dst, "w", encoding="utf-8").write(t)
os.remove(src)
print("engine renamed ->", os.path.basename(dst))

runner = r'''# -*- coding: utf-8 -*-
"""ASCII runner for r%d (Chinese paths must not enter argv)."""
import runpy

P = r"%s"

runpy.run_path(P, run_name="__main__")
''' % (NEW_N, dst.replace("\\", "\\\\"))
io.open(os.path.join(ENG_DIR, "_run_r%d.py" % NEW_N), "w", encoding="utf-8").write(runner)

driver = r'''# -*- coding: utf-8 -*-
"""ASCII driver for r%d."""
import runpy

R = r"%s"

runpy.run_path(R, run_name="__main__")
''' % (NEW_N, os.path.join(ENG_DIR, "_run_r%d.py" % NEW_N).replace("\\", "\\\\"))
io.open(os.path.join(ROOT, "_drive_r%d.py" % NEW_N), "w", encoding="utf-8").write(driver)
print("runner+driver written for r%d" % NEW_N)
