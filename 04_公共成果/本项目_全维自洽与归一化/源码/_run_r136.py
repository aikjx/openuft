# -*- coding: utf-8 -*-
"""UTF-8 安全 runner：runpy 执行引擎，规避中文路径进入 argv 的 GBK 误码。"""
import runpy, os
HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "TUFT-r136_力的大统一方程_非GUT候选族补齐与全链路终局账本_2026-10-21.py")
runpy.run_path(TARGET, run_name="__main__")
