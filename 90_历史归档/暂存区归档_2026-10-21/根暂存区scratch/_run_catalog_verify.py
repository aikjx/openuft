# -*- coding: utf-8 -*-
"""UTF-8 安全 runner：先刷新目录，再跑 openuft 校验链。
（中文路径不进 argv ⇒ 用 runpy.run_path）"""
import os, runpy, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))

CAT = os.path.join(ROOT, "00_项目治理", "维护工具", "refresh_catalog.py")
VER = os.path.join(ROOT, "verify.py")

print("[1/2] refresh_catalog ...")
try:
    runpy.run_path(CAT, run_name="__main__")
    print("      catalog refreshed")
except SystemExit as e:
    print("      catalog exit:", e.code)
except Exception as e:
    print("      catalog ERROR:", type(e).__name__, e)

print("[2/2] verify ...")
try:
    runpy.run_path(VER, run_name="__main__")
    print("      verify done")
except SystemExit as e:
    print("      verify exit:", e.code)
except Exception as e:
    print("      verify ERROR:", type(e).__name__, e)
