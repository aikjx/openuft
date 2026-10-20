# -*- coding: utf-8 -*-
"""UTF-8 安全 runner：runpy 执行引擎，规避中文路径进入 argv 的 GBK 误码。"""
import runpy, os
HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "TUFT-r133_修补失敗元原理_修改逐个审计与结构不可修补定理_2026-10-20.py")
runpy.run_path(TARGET, run_name="__main__")
