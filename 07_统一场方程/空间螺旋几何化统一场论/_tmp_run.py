# -*- coding: utf-8 -*-
"""逐行执行脚本，捕获第一个运行时错误并打印当时的变量状态。"""
import sys
import traceback

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

p = "29_作用量变分审计_耦合能动张量与迹_2026-10-03.py"
src = open(p, "rb").read().decode("utf-8").replace("\r\n", "\n")
g = {"__name__": "__main__", "__file__": p}
try:
    exec(compile(src, p, "exec"), g)
except Exception:
    tb = traceback.format_exc()
    print(tb)
    f = sys.exc_info()[2].tb_lasti
    ln = sys.exc_info()[2].tb_lineno
    print("failing line", ln)
    for k, v in g.items():
        if k in ("sp", "dg", "g", "ginv", "coords", "L", "mu", "sig", "rho", "s", "NL", "H", "SHAPE"):
            print("  %s = %r  (%s)" % (k, v, type(v).__name__))
