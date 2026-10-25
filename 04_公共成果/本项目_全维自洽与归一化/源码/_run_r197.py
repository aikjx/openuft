# -*- coding: utf-8 -*-
r"""ASCII runner：定位中文引擎路径并以 runpy 执行（中文路径禁入 argv 的 workaround）。"""
import os
import runpy
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(
    HERE,
    "TUFT-r197_经典极限与现象推导链路闭环式_宇宙学电磁弱力强力与单圈跑动切片_2026-10-25.py")

if __name__ == "__main__":
    if not os.path.isfile(TARGET):
        print("TARGET NOT FOUND: %s" % TARGET)
        sys.exit(3)
    runpy.run_path(TARGET, run_name="__main__")
