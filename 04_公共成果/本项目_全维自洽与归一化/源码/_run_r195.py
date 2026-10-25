# -*- coding: utf-8 -*-
r"""ASCII runner：定位中文引擎路径并以 runpy 执行（中文路径禁入 argv 的 workaround）。

【归属修复 · 2026-10-25 19:2x】此文件原属并行链 r195《尺度秩不变性定理…》。
本线在 r195→r197 改号过程中曾误将其覆盖/删除，现按 r195 README 登记恢复原指向
（`openuft/_drive_r195.py` 依赖本文件），不改变 r195 引擎任何字节。
"""
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
    "TUFT-r195_尺度秩不变性定理_M5尺度简并与归一化条件名实审计_精算_2026-10-25.py")

if __name__ == "__main__":
    if not os.path.isfile(TARGET):
        print("TARGET NOT FOUND: %s" % TARGET)
        sys.exit(3)
    runpy.run_path(TARGET, run_name="__main__")
