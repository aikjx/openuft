# -*- coding: utf-8 -*-
"""ASCII 名 runner：规避中文路径入 argv 的 GBK 解码问题。"""
import os
import sys
import runpy

SRC_DIR = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
ENGINE = os.path.join(SRC_DIR, "TUFT-r334_精度不等于发现统一验收规范_基准率乘零判别力乘过精度门禁_2026-11-01.py")

if __name__ == "__main__":
    sys.path.insert(0, SRC_DIR)
    runpy.run_path(ENGINE, run_name="__main__")
