# -*- coding: utf-8 -*-
"""UTF-8 安全 runner：中文路径禁入 argv，改用 runpy.run_path。"""
import runpy, os

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "TUFT-r142_核心公式体系_最小修复路径定价与未检两式首攻_2026-10-21.py")
runpy.run_path(TARGET, run_name="__main__")
