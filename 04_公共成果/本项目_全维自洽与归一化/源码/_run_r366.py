# -*- coding: utf-8 -*-
# ASCII runner for r366 (中文路径禁入 argv)
import glob, os, subprocess, sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
PREFIX = "TUFT-r366_\u6574\u503c\u591a\u9879\u5f0f\u901a\u6709\u6027\u5ba1\u8ba1"  # TUFT-r366_整值多项式通有性审计

hits = sorted(glob.glob(os.path.join(SRC, PREFIX + "*.py")))
hits = [h for h in hits if not os.path.basename(h).startswith("_")]
assert len(hits) == 1, "prefix hit=%d : %s" % (len(hits), hits)
target = hits[0]
print("[runner] " + os.path.basename(target))
r = subprocess.run([sys.executable, target], cwd=SRC)
sys.exit(r.returncode)
