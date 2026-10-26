# -*- coding: utf-8 -*-
"""r222 -> r223 整体改号（★第七/八次竞态：并行 03:09:10 先占 r222）。
吸取 r218 教训：渲染层（report / verdict md / token / 红线范围）同步改。"""
import io
import os
import re
import shutil

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
DATA = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\数据"
SCRATCH = r"D:\a10\aikjx\code\my_lib\openuft\_scratch_r222"

OLD_TAIL = "_四力统一运动方程_求导证明机验与轨道进动精算_大小方向距离特性与交互可视化_2026-10-26"
OLD_PY = "TUFT-r222" + OLD_TAIL + ".py"
NEW_PY = "TUFT-r223" + OLD_TAIL + ".py"

p = os.path.join(SRC, OLD_PY)
s = io.open(p, encoding="utf-8").read()
orig = s

# ---- 1) 全局基础替换 ----
s = s.replace('BASE_NAME = "TUFT-r222' + OLD_TAIL + '"',
              'BASE_NAME = "TUFT-r223' + OLD_TAIL + '"')
s = s.replace('REDLINE_PHRASE = "不可与 r142–r221 相加"',
              'REDLINE_PHRASE = "不可与 r142–r222 相加"')
s = s.replace("205 <= int(m.group(1)) <= 221", "205 <= int(m.group(1)) <= 222")
s = s.replace("未触碰 r205–r221 并行产物", "未触碰 r205–r222 并行产物")
s = s.replace('"id": "r222",', '"id": "r223",')
s = s.replace('VERDICT_TOKEN = (\n        "R222-', 'VERDICT_TOKEN = (\n        "R223-')
s = s.replace('"R222-FOUR-FORCE', '"R223-FOUR-FORCE')

# ---- 2) docstring 编号段整体重写 ----
old_doc = """编号 r222（★第七次同型竞态环境）
--------------------------------------------------------------
起草前扫描：r214《四力统一运动方程_求导证明与力的大小方向距离精算及可视化》、
r219《四力同框动力学_Yukawa进动多源叠加与相对论化》、r220《力的矢量场与通量
_潮汐散度Yukawa高斯定理与力线》、r221《四力统一运动方程强化轮_禁闭项接入与
弱通道门》均为并行会话产物 ⇒ **r222 三树实测为空，本卷取 r222**。
落盘前仍须复查磁盘时间戳（并行线 03:03–03:04 连续落卷）。未触碰并行任何字节。"""
new_doc = """编号 r223（★第七次 + 第八次同型竞态环境 · 起草 r222 → 整体改号）
--------------------------------------------------------------
起草前扫描（03:04）：并行已占 r214《四力统一运动方程_求导证明与力的大小方向距离
精算及可视化》、r219《四力同框动力学_Yukawa进动多源叠加与相对论化》、r220《力的
矢量场与通量_潮汐散度Yukawa高斯定理与力线》、r221《四力统一运动方程强化轮_禁闭项
接入与弱通道门》⇒ 当时 **r222 三树实测为空**，本卷起草取 r222。

**★落盘前复查（03:25）发现第八次竞态**：并行已于 **03:09:10** 落下
r222《四力统一方程的传播层_色散截止群速度与质量力程等价_精算与可视化》
（源码 03:09:10，四件套 03:09:21），**早于**本卷引擎落盘时刻 ⇒ 按「先占位者为
权威、后到者整体改号」铁律，本卷**整体顺延改号 r223**（改号时 r223 三树实测全空）。

★吸取 r218 教训：改号脚本必须同步改**渲染层**（render_report / render_verdict_md /
VERDICT_TOKEN / 红线范围 / G12 扫描范围），否则交付物内部会出现「文件名 r223、
报告标题 r222」的自相矛盾。本脚本已全部覆盖。全程未触碰并行任何字节。"""
assert old_doc in s, "docstring 编号段未匹配"
s = s.replace(old_doc, new_doc)

# ---- 3) render_report 头部 ----
old_rep = ('    L.append("[编号] r222（★第七次同型竞态环境：并行已占 r214/r219/r220/r221 ⇒ r222 三树"\n'
           '             "实测为空；落盘前仍须复查时间戳）")')
new_rep = ('    L.append("[编号] r223（★第八次同型竞态：起草取 r222，落盘前复查发现并行已于 03:09:10"\n'
           '             "先占 r222《四力统一方程的传播层_色散截止群速度与质量力程等价》⇒ 本卷整体"\n'
           '             "顺延改号 r223；改号时 r223 三树实测全空）")')
assert old_rep in s, "render_report 编号段未匹配"
s = s.replace(old_rep, new_rep)

# ---- 4) render_verdict_md 编号段 ----
old_v = ('    L.append("- **编号 r222**（★第七次同型竞态环境）：起草前扫描，并行已占")\n'
         '    L.append("  r214《四力统一运动方程_求导证明与力的大小方向距离精算及可视化》、")\n'
         '    L.append("  r219《四力同框动力学_Yukawa进动多源叠加与相对论化》、")\n'
         '    L.append("  r220《力的矢量场与通量_潮汐散度Yukawa高斯定理与力线》、")\n'
         '    L.append("  r221《四力统一运动方程强化轮_禁闭项接入与弱通道门》")\n'
         '    L.append("  ⇒ **r222 三树实测为空，本卷取 r222**。全程未触碰并行任何字节。")')
new_v = ('    L.append("- **编号 r223**（★第七次 + 第八次同型竞态环境 · 起草 r222 → 整体改号）：")\n'
         '    L.append("  起草前（03:04）扫描：并行已占 r214《四力统一运动方程_求导证明与力的大小")\n'
         '    L.append("  方向距离精算及可视化》、r219《四力同框动力学_Yukawa进动多源叠加与相对论")\n'
         '    L.append("  化》、r220《力的矢量场与通量_潮汐散度Yukawa高斯定理与力线》、r221《四力")\n'
         '    L.append("  统一运动方程强化轮_禁闭项接入与弱通道门》⇒ 当时 r222 三树为空，起草取 r222。")\n'
         '    L.append("  **★落盘前复查（03:25）发现第八次竞态**：并行已于 **03:09:10** 落下")\n'
         '    L.append("  r222《四力统一方程的传播层_色散截止群速度与质量力程等价_精算与可视化》")\n'
         '    L.append("  （源码 03:09:10，四件套 03:09:21），**早于**本卷引擎落盘 ⇒ 按「先占位者")\n'
         '    L.append("  为权威、后到者整体改号」铁律，本卷**整体顺延改号 r223**（改号时 r223 三树")\n'
         '    L.append("  实测全空）。**本线下一轮从 r224 起**。全程未触碰并行任何字节。")')
assert old_v in s, "verdict md 编号段未匹配"
s = s.replace(old_v, new_v)

# ---- 5) 报告/判定册标题 ----
s = s.replace('L.append("TUFT-r222 · 四力统一运动方程精算报告")',
              'L.append("TUFT-r223 · 四力统一运动方程精算报告")')
s = s.replace('L.append("# 判定册 · TUFT-r222｜四力统一运动方程：求导证明机验与轨道进动精算")',
              'L.append("# 判定册 · TUFT-r223｜四力统一运动方程：求导证明机验与轨道进动精算")')

assert s != orig
io.open(os.path.join(SRC, NEW_PY), "w", encoding="utf-8").write(s)
print("written:", NEW_PY)

# ---- 6) runner / driver ----
run_txt = (
    '# -*- coding: utf-8 -*-\n'
    'import runpy, sys\n'
    'P = r"D:\\a10\\aikjx\\code\\my_lib\\openuft\\04_公共成果\\本项目_全维自洽与归一化\\源码\\'
    + NEW_PY + '"\n'
    'sys.argv = [P]\n'
    'sys.exit(runpy.run_path(P, run_name="__main__"))\n')
io.open(os.path.join(SRC, "_run_r223.py"), "w", encoding="utf-8").write(run_txt)

drv_txt = (
    '# -*- coding: utf-8 -*-\n'
    'import runpy, sys\n'
    'P = r"D:\\a10\\aikjx\\code\\my_lib\\openuft\\04_公共成果\\本项目_全维自洽与归一化\\源码\\_run_r223.py"\n'
    'sys.argv = [P]\n'
    'runpy.run_path(P, run_name="__main__")\n')
io.open(r"D:\a10\aikjx\code\my_lib\openuft\_drive_r223.py", "w",
        encoding="utf-8").write(drv_txt)
print("runner/driver written")

# ---- 7) 归档本卷旧号产物（禁 rm；只动本卷自己的文件，绝不碰并行） ----
os.makedirs(SCRATCH, exist_ok=True)
old_files = [
    os.path.join(SRC, OLD_PY),
    os.path.join(SRC, "_run_r222.py"),
    os.path.join(SRC, "TUFT-r222" + OLD_TAIL + ".html"),
    os.path.join(SRC, "TUFT-r222" + OLD_TAIL + "_交互可视化_2026-10-26.html"),
    os.path.join(SRC, "TUFT-r222" + OLD_TAIL + "_交互可视化.html"),
    os.path.join(DATA, "TUFT-r222" + OLD_TAIL + ".json"),
    os.path.join(DATA, "TUFT-r222" + OLD_TAIL + ".md"),
    os.path.join(DATA, "TUFT-r222" + OLD_TAIL + "_report.txt"),
    os.path.join(DATA, "判定_TUFT-r222" + OLD_TAIL + ".md"),
]
for f in old_files:
    if os.path.exists(f):
        dst = os.path.join(SCRATCH, os.path.basename(f))
        if os.path.exists(dst):
            os.remove(dst)
        shutil.move(f, dst)
        print("archived:", os.path.basename(f))
