# -*- coding: utf-8 -*-
"""r321 runner（复现入口）—— ROOT V24.0 固定点真假判别【互补攻坚卷】
分工（与并行卷的边界，条目不可相加）：
    r317（并行先到）= ROOTV24 主卷：可逆重参数化 / 事后编造定理 / 相似不变量 / 轨道表 / H(q) 求积
    r320（并行在途）= ROOTV24 图表可容性定理 / 任意重参数化指数不变律 / 坐标旋钮杠杆
    r321（本卷）    = 真空极化闭式 / 可预测性符号判据 / 放大因子定价 / 能标冗余 / 信息量记账
取号：落盘时 r319 已被并行会话《统一表示框架与二次超荷矩》占满（判定册+数据+源码齐套），
      按「后到者整体改号、不覆盖他人」纪律整体改号 r319 → r321。
"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r321_ROOTV24固定点真假判别互补攻坚_"
        "真空极化闭式与可预测性符号判据与放大因子定价与能标冗余_精算与可视化_2026-11-01.py")
OUT = os.path.join(SRC, "_out_r321.txt")

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-5000:])
print("RC=", p.returncode)
sys.exit(0 if p.returncode == 0 else 1)
