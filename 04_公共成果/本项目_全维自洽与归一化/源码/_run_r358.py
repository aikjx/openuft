# -*- coding: utf-8 -*-
"""r358 ASCII runner（纪律：中文路径禁入 argv ⇒ 用 glob 定位 + 断言命中数 == 1）。"""
import glob
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
pat = os.path.join(HERE, "TUFT-r358_%s*.py" % "\u6574\u6027\u96c6")
hits = glob.glob(pat)
if len(hits) != 1:
    sys.stdout.write("RUNNER-FAIL: hits=%d\n" % len(hits))
    for h in hits:
        sys.stdout.write("   %s\n" % os.path.basename(h))
    sys.exit(2)
sys.stdout.write("[runner] %s\n" % os.path.basename(hits[0]))
rc = subprocess.call([sys.executable, hits[0]])
sys.exit(rc)
