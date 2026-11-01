# -*- coding: utf-8 -*-
"""ASCII 名 runner：规避中文路径入 argv 的 GBK 解码问题。
引擎路径硬编码为 raw Windows 字符串，由 Python 宽字符 API 打开，不依赖 cwd。
"""
import os
import sys
import runpy

SRC_DIR = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
ENGINE = os.path.join(SRC_DIR, "TUFT-r310_ROOTV20跨现象本源审计_几何与群与QED都给关系不给数值_2026-11-01.py")

if __name__ == "__main__":
    sys.path.insert(0, SRC_DIR)
    runpy.run_path(ENGINE, run_name="__main__")
