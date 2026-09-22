import os
import re
from pathlib import Path

root_dir = r"d:\a10\aikjx\code\my_lib\article\zh\2026\7\4\乖乖数学"

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