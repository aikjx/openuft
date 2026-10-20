# -*- coding: utf-8 -*-
"""UTF-8 安全 runner：runpy 执行引擎，规避中文路径进入 argv 的 GBK 误码。"""
import runpy, os
HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "TUFT-r138_硬核审计_规范群与mu2符号的第一性原理可导出性精算_2026-10-21.py")
runpy.run_path(TARGET, run_name="__main__")
