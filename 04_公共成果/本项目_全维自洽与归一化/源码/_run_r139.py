# -*- coding: utf-8 -*-
"""UTF-8 安全 runner：runpy 执行引擎，规避中文路径进入 argv 的 GBK 误码。"""
import runpy, os
HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "TUFT-r139_全维求导证明验证精算_自旋2路线非线性完备机检_2026-10-21.py")
runpy.run_path(TARGET, run_name="__main__")
