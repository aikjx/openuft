# -*- coding: utf-8 -*-
r"""
chats 全量归档构建脚本
源目录: C:/Users/mo/Doubao/chats
目标目录: D:/code/ymkj/chats_全量归档

产出维度:
  01_全路径镜像   -> 原样保留完整目录结构与全部文件(含隐藏)
  02_压缩包       -> 全部 zip 原件
  03_解压产物     -> zip 解压结果
  04_按主题归类   -> 哥德巴赫猜想 / GAQ-UFT大统一场论
  05_按类型归类   -> .py/.md/.html/.txt/.json/.jpg/.png/.zip
"""
import os
import shutil
import zipfile

SRC = r"C:\Users\mo\Doubao\chats"
ROOT = r"D:\code\ymkj\chats_全量归档"
MIRROR = os.path.join(ROOT, "01_全路径镜像")
ZIPS = os.path.join(ROOT, "02_压缩包")
EXTRACT = os.path.join(ROOT, "03_解压产物")
TOPIC = os.path.join(ROOT, "04_按主题归类")
TYPE = os.path.join(ROOT, "05_按类型归类")


def rm_if_exists(p):
    if os.path.isdir(p):
        shutil.rmtree(p)
    elif os.path.isfile(p):
        os.remove(p)


def rebuild(d):
    rm_if_exists(d)
    os.makedirs(d, exist_ok=True)


# ---------- 1. 全路径镜像 ----------
dest_mirror = os.path.join(MIRROR, "chats")
rebuild(MIRROR)
shutil.copytree(SRC, dest_mirror)
print("01 全路径镜像 完成")

# ---------- 2. 压缩包 ----------
rebuild(ZIPS)
zip_src1 = os.path.join(SRC, r"2026-08-22\new-chat\goldbach_methods.zip")
zip_src2 = os.path.join(SRC, r"2026-09-04\new-chat\GAQ-UFT-大统一全书\deliverables\GAQ-UFT-大统一全书-整理稿.zip")
shutil.copy2(zip_src1, os.path.join(ZIPS, "goldbach_methods.zip"))
shutil.copy2(zip_src2, os.path.join(ZIPS, "GAQ-UFT-大统一全书-整理稿.zip"))
print("02 压缩包 完成")

# ---------- 3. 解压产物 ----------
rebuild(EXTRACT)
d_gold = os.path.join(EXTRACT, "goldbach_methods_解压")
d_book = os.path.join(EXTRACT, "GAQ-UFT-大统一全书-整理稿_解压")
with zipfile.ZipFile(os.path.join(ZIPS, "goldbach_methods.zip")) as z:
    z.extractall(d_gold)
with zipfile.ZipFile(os.path.join(ZIPS, "GAQ-UFT-大统一全书-整理稿.zip")) as z:
    z.extractall(d_book)
print("03 解压产物 完成")

# ---------- 4. 按主题归类 ----------
rebuild(TOPIC)
topic_map = {
    "2026-08-21": "GAQ-UFT大统一场论",
    "2026-08-22": "哥德巴赫猜想",
    "2026-09-03": "GAQ-UFT大统一场论",
    "2026-09-04": "GAQ-UFT大统一场论",
}
for top in sorted(os.listdir(SRC)):
    p = os.path.join(SRC, top)
    if not os.path.isdir(p):
        continue
    topic = topic_map.get(top)
    if topic is None:
        print(f"  跳过(无主题映射): {top}")
        continue
    subdest = os.path.join(TOPIC, topic, top)
    shutil.copytree(p, subdest)
    print(f"  主题[{topic}] <- {top}")
print("04 按主题归类 完成")

# ---------- 5. 按类型归类 ----------
rebuild(TYPE)
type_map = {
    ".py": "01_脚本_python",
    ".md": "02_文档_markdown",
    ".html": "03_网页_html",
    ".txt": "04_文本输出_txt",
    ".json": "05_数据_json",
    ".jpg": "06_图片_预览",
    ".png": "06_图片_预览",
    ".zip": "07_压缩包_zip",
}
count = 0
for root_dir, _dirs, files in os.walk(SRC):
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        t = type_map.get(ext)
        if t is None:
            continue
        src_full = os.path.join(root_dir, f)
        rel = os.path.relpath(src_full, SRC)
        dst_full = os.path.join(TYPE, t, rel)
        os.makedirs(os.path.dirname(dst_full), exist_ok=True)
        shutil.copy2(src_full, dst_full)
        count += 1
print(f"05 按类型归类 完成, 共 {count} 个文件")
print("全部完成")
