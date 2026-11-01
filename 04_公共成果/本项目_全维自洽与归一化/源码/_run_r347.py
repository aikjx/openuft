# -*- coding: utf-8 -*-
import os
import runpy
import sys

ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
NAME = ("TUFT-r347_ROOTV24判词链总账_五卷schema归一与跨卷读数一致性与不可相加证明"
        "_精算与可视化_2026-11-01.py")
runpy.run_path(os.path.join(ROOT, "源码", NAME), run_name="__main__")
