# -*- coding: utf-8 -*-
"""UTF-8 安全 runner：runpy 执行引擎，规避中文路径进入 argv 的 GBK 误码。"""
import runpy, os
HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "TUFT-r141_核心公式理论体系_物理层内部矛盾与新增性机检_2026-10-21.py")
runpy.run_path(TARGET, run_name="__main__")
