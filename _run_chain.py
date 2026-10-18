# -*- coding: utf-8 -*-
"""ASCII runner for openuft verify chain (Chinese-path argv workaround)."""
import runpy
import sys

TARGETS = {
    "verify": "D:/a10/aikjx/code/my_lib/openuft/verify.py",
    "refresh": "D:/a10/aikjx/code/my_lib/openuft/00_项目治理/维护工具/refresh_catalog.py",
}

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "verify"
    extra = sys.argv[2:]
    tgt = TARGETS[which]
    sys.argv = [tgt] + extra
    runpy.run_path(tgt, run_name="__main__")
