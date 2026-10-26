# -*- coding: utf-8 -*-
"""ASCII runner for r218 (Chinese paths must not enter argv)."""
import runpy

P = r"D:\\a10\\aikjx\\code\\my_lib\\openuft\\04_公共成果\\本项目_全维自洽与归一化\\源码\\TUFT-r218_四力统一方程_定义恒等式零判别力覆盖缺与修复定价_精算_2026-10-26.py"

runpy.run_path(P, run_name="__main__")
