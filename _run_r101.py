# -*- coding: utf-8 -*-
"""ASCII runner for openuft TUFT-r101 engine (Chinese-path argv workaround)."""
import runpy
import sys

TARGET = ("D:/a10/aikjx/code/my_lib/openuft/04_公共成果/"
          "本项目_全维自洽与归一化/源码/"
          "TUFT-r101_守恒律审计_场方程构造性收口_函数形式来源审计_2026-10-18.py")

if __name__ == "__main__":
    sys.argv = [TARGET]
    runpy.run_path(TARGET, run_name="__main__")
