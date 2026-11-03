# -*- coding: utf-8 -*-
"""r367 清场：把探查期的一次性脚本移入 scratch/（禁 rm -rf，一律 shutil.move）。

清场件数按**真实处置**分流记账（承 r350 纪律）：
  - 移入 scratch/ 的：6 件探查脚本
  - 陈旧的 __pycache__/*.pyc（会让「扫号」误判占用）：一并移入 scratch/
保留：引擎本体 + _run / _reg / _check / _log / _fix / _clean（可复现的收口工具）。
"""
import glob
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRATCH = os.path.join(ROOT, "scratch")
os.makedirs(SCRATCH, exist_ok=True)

NAMES = [
    "_probe_r367.py",
    "_dev_r367_probe.py",
    "_dev_r367_probe2.py",
    "_dev_r367_probe3.py",
    "_dev_r367_probe3b.py",
    "_dev_r367_probe4.py",
]

moved, missing, failed = [], [], []
for n in NAMES:
    p = os.path.join(ROOT, "源码", n)
    if not os.path.exists(p):
        missing.append(n)
        continue
    dst = os.path.join(SCRATCH, n)
    if os.path.exists(dst):
        dst = os.path.join(SCRATCH, "_dup_" + n)
    try:
        shutil.move(p, dst)
        moved.append(n)
        print("moved  源码/%s -> scratch/%s" % (n, os.path.basename(dst)))
    except Exception as e:
        failed.append((n, repr(e)))
        print("FAILED %s : %r" % (n, e))

# 陈旧 .pyc：会让「扫号」误判占用
pyc = 0
cache = os.path.join(ROOT, "源码", "__pycache__")
if os.path.isdir(cache):
    for f in sorted(glob.glob(os.path.join(cache, "*.pyc"))):
        stem = os.path.basename(f).split(".")[0]
        if "r367" in stem or "probe" in stem:
            try:
                shutil.move(f, os.path.join(SCRATCH, "_pyc_" + os.path.basename(f)))
                pyc += 1
                print("moved  __pycache__/%s" % os.path.basename(f))
            except Exception as e:
                print("FAILED pyc %s : %r" % (f, e))
print("stale pyc moved = %d" % pyc)

print("")
print("moved=%d  missing=%d  failed=%d  pyc=%d" % (len(moved), len(missing), len(failed), pyc))
if missing:
    print("missing: %r" % (missing,))
if failed:
    print("failed: %r" % (failed,))
    raise SystemExit(2)
print("CLEAN-OK r367（探查脚本 %d 件 + 陈旧 pyc %d 个）" % (len(moved), pyc))
