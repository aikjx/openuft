# -*- coding: utf-8 -*-
"""ASCII runner for openuft TUFT-r103 engine (Chinese-path argv workaround)."""
import runpy
import sys

TARGET = ("D:/a10/aikjx/code/my_lib/openuft/04_公共成果/"
          "本项目_全维自洽与归一化/源码/"
          "TUFT-r103_现象学覆盖率审计_统一场论资格与接口槽位机读_2026-10-18.py")

if __name__ == "__main__":
    sys.argv = [TARGET]
    runpy.run_path(TARGET, run_name="__main__")
