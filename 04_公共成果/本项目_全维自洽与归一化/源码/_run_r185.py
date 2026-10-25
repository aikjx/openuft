# -*- coding: utf-8 -*-
import runpy, sys
P = (r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
     r"\TUFT-r185_引力场产生电磁场_麦克斯韦重写与f量纲冲突_精算_2026-10-25.py")
sys.argv = [P]
runpy.run_path(P, run_name="__main__")
