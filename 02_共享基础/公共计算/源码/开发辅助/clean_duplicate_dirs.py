import os
import re
from pathlib import Path

# 源目录为库外路径，由环境变量 SRC_ROOT 指定
root_dir = os.environ.get("SRC_ROOT", "")
if not root_dir:
    raise SystemExit("请先设置环境变量 SRC_ROOT 为待处理源目录（库外路径）")

pattern = re.compile(r'\+\d+$')

deleted_count = 0
for dirpath, dirnames, filenames in os.walk(root_dir):
    for dirname in dirnames:
        if pattern.search(dirname):
            full_path = os.path.join(dirpath, dirname)
            print(f"删除: {full_path}")
            import shutil
            shutil.rmtree(full_path)
            deleted_count += 1

print(f"\n共删除 {deleted_count} 个重复目录")