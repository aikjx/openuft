# -*- coding: utf-8 -*-
"""把「修复空间的机器生成与闭包定价」卷由 r143 整体改号 r147（撞号处置）。

纪律依据：同一 rNN 被多个引擎占用时，保留已跑通且已登记者为权威，后到者改号不覆盖他人字节。
r143 已被并行会话《常温超导 · 求导证明验证精算与攻破》占用（2026-10-21 23:19，早于本卷 01:43，
且已完成四处 README 登记）⇒ 本卷改号 r147（r144/r145/r146 实测均已占）。
"""
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJ = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化")
SRC = os.path.join(PROJ, "源码")
DATA = os.path.join(PROJ, "数据")
SCRATCH = os.path.join(ROOT, "scratch")
if not os.path.isdir(SCRATCH):
    os.makedirs(SCRATCH)

OLD_SRC = os.path.join(SRC, "TUFT-r143_修复空间的机器生成与闭包定价_2026-10-22.py")
NEW_SRC = os.path.join(SRC, "TUFT-r147_修复空间的机器生成与闭包定价_2026-10-22.py")

# 1) 源码文件改号
shutil.move(OLD_SRC, NEW_SRC)

# 2) 内部编号 r143 -> r147（本卷自引用，实测 7 处）
with open(NEW_SRC, "r", encoding="utf-8") as f:
    txt = f.read()
n_before = txt.count("r143")
txt = txt.replace("r143", "r147")

# 3) 卷首插入编号碰撞登记
anchor = "分工声明（与 r141 / r142 分层，条目不可相加）："
note = (
    "★编号碰撞处置（必须先登记）：本卷起草时依 README「下轮从 r143 起」取 r143，并已跑通产出三件套；\n"
    "  落盘登记时发现**并行会话同日已用 r143 登记《常温超导 · 求导证明验证精算与攻破》**\n"
    "  （建时刻 2026-10-21 23:19，早于本卷 2026-10-22 01:43，且已完成四处 README 登记）。\n"
    "  按「后到者改号不覆盖他人」纪律，本卷整体改号 **r147** —— r144《空间是否运动与怎么运动》\n"
    "  / r145《常温超导本质本源》/ r146《四力统一可行性》实测均已占，首空号为 r147。\n"
    "  改号前本卷自产的旧名产物已全部移入 scratch/（禁 rm），他人 r143 产物字节**逐字节未触碰**。\n"
    "\n"
)
assert anchor in txt, "anchor not found"
txt = txt.replace(anchor, note + anchor, 1)

with open(NEW_SRC, "w", encoding="utf-8", newline="\n") as f:
    f.write(txt)

# 4) 旧名产物移入 scratch/
moved = []
for nm in os.listdir(DATA):
    if "修复空间的机器生成与闭包定价" in nm:
        shutil.move(os.path.join(DATA, nm), os.path.join(SCRATCH, nm))
        moved.append(nm)

# 5) runner 改号
old_run = os.path.join(SRC, "_run_r143.py")
new_run = os.path.join(SRC, "_run_r147.py")
if os.path.exists(old_run):
    shutil.move(old_run, os.path.join(SCRATCH, "_run_r143.py.old"))
with open(new_run, "w", encoding="utf-8", newline="\n") as f:
    f.write("# -*- coding: utf-8 -*-\n")
    f.write('"""UTF-8 安全 runner：中文路径禁入 argv，改用 runpy.run_path。"""\n')
    f.write("import runpy, os\n\n")
    f.write("HERE = os.path.dirname(os.path.abspath(__file__))\n")
    f.write('TARGET = os.path.join(HERE, "TUFT-r147_修复空间的机器生成与闭包定价_2026-10-22.py")\n')
    f.write('runpy.run_path(TARGET, run_name="__main__")\n')

# 6) 报告（ASCII 输出，避免 GBK 误码）
print("r143 occurrences replaced:", n_before)
print("source:", os.path.basename(NEW_SRC))
print("moved to scratch:", len(moved))
for m in moved:
    print("   ", m)
print("runner:", os.path.basename(new_run))
