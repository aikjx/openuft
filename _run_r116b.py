# -*- coding: utf-8 -*-
"""ASCII runner for r116b engine (Chinese-path + GBK-capture workaround).

NOTE: `_run_r116.py` 已被并行会话占用（指向其 r116/r117 册），本册不覆盖他人文件，
故另立 _run_r116b.py 专供 TUFT-r116_光子内部运行全情形判决与传统对照 使用。
"""
import subprocess
import sys

TARGET = ("D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/"
          "源码/TUFT-r116_光子内部运行全情形判决与传统对照_2026-10-20.py")

if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
    r = subprocess.run([sys.executable, TARGET], encoding='utf-8', errors='replace')
    sys.exit(r.returncode)
