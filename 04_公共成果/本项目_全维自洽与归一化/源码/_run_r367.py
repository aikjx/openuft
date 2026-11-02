# -*- coding: utf-8 -*-
# ASCII runner for r367 (中文路径禁入 argv)
import glob, os, subprocess, sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
PREFIX = "TUFT-r367_\u5b8c\u5168\u4ea4\u4e0e\u52a0\u6743\u8d85\u66f2\u9762"  # TUFT-r367_完全交与加权超曲面

hits = sorted(glob.glob(os.path.join(SRC, PREFIX + "*.py")))
hits = [h for h in hits if not os.path.basename(h).startswith("_")]
assert len(hits) == 1, "prefix hit=%d : %s" % (len(hits), hits)
target = hits[0]
print("[runner] " + os.path.basename(target))
r = subprocess.run([sys.executable, target], cwd=SRC)
sys.exit(r.returncode)
