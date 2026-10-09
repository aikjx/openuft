# -*- coding: utf-8 -*-
"""生成 chats_全量归档 的 00_README_总览.md（全路径 + 多维度清单）"""
import os
from collections import defaultdict, OrderedDict

ROOT = r"D:\code\ymkj\chats_全量归档"
MIRROR = os.path.join(ROOT, "01_全路径镜像", "chats")
SRC = r"C:\Users\mo\Doubao\chats"
OUT = os.path.join(ROOT, "00_README_总览.md")

type_names = {
    ".py": "Python 脚本", ".md": "Markdown 文档", ".html": "HTML 网页",
    ".txt": "文本输出", ".json": "JSON 数据", ".jpg": "JPG 图片",
    ".png": "PNG 图片", ".zip": "ZIP 压缩包",
}

def human(n):
    if n >= 1024 * 1024:
        return f"{n/1024/1024:.2f} MB"
    if n >= 1024:
        return f"{n/1024:.1f} KB"
    return f"{n} B"

def walk_files(base):
    for root_dir, _dirs, files in os.walk(base):
        for f in files:
            full = os.path.join(root_dir, f)
            yield full

# 收集源文件元数据
src_files = list(walk_files(SRC))
total_size = sum(os.path.getsize(p) for p in src_files)

# 按日期
by_date = defaultdict(list)
for p in src_files:
    rel = os.path.relpath(p, SRC)
    date = rel.split(os.sep)[0]
    by_date[date].append((rel, os.path.getsize(p)))

# 按类型
by_type = defaultdict(list)
for p in src_files:
    ext = os.path.splitext(p)[1].lower()
    by_type[ext].append((os.path.relpath(p, SRC), os.path.getsize(p)))

# 按主题
topic_map = {
    "2026-08-21": "GAQ-UFT大统一场论", "2026-08-22": "哥德巴赫猜想",
    "2026-09-03": "GAQ-UFT大统一场论", "2026-09-04": "GAQ-UFT大统一场论",
}
by_topic = defaultdict(list)
for p in src_files:
    rel = os.path.relpath(p, SRC)
    date = rel.split(os.sep)[0]
    t = topic_map.get(date, "未归类")
    by_topic[t].append((rel, os.path.getsize(p)))

# 尺寸分档
size_bins = OrderedDict([("≤ 4 KB", 0), ("4-16 KB", 0), ("16-64 KB", 0), ("64-256 KB", 0), ("> 256 KB", 0)])
for p in src_files:
    s = os.path.getsize(p)
    if s <= 4096: size_bins["≤ 4 KB"] += 1
    elif s <= 16384: size_bins["4-16 KB"] += 1
    elif s <= 65536: size_bins["16-64 KB"] += 1
    elif s <= 262144: size_bins["64-256 KB"] += 1
    else: size_bins["> 256 KB"] += 1

L = []
A = L.append
A("# chats 全量归档 · 总览清单（全路径 / 全维度）")
A("")
A(f"> 源目录：`{SRC}`")
A(f"> 归档目录：`{ROOT}`")
A(f"> 生成时间：2026-09-04")
A(f"> 源文件总数：**{len(src_files)} 个**，总大小：**{human(total_size)}**")
A("")
A("## 一、归档结构（5 大维度目录）")
A("")
A("```text")
A(ROOT)
A("├─ 00_README_总览.md           本清单")
A("├─ 01_全路径镜像/               原样保留完整目录结构（含隐藏 .preview 等），全路径可追溯")
A("├─ 02_压缩包/                   全部 zip 原件（2 个）")
A("├─ 03_解压产物/                 zip 解压后的完整内容（2 套）")
A("├─ 04_按主题归类/               哥德巴赫猜想 / GAQ-UFT大统一场论")
A("└─ 05_按类型归类/               .py / .md / .html / .txt / .json / .jpg / .png / .zip")
A("```")
A("")
A("## 二、全路径文件清单（共 %d 个，按日期目录列出）" % len(src_files))
A("")
for date in sorted(by_date):
    items = sorted(by_date[date])
    sz = sum(s for _, s in items)
    A(f"### {date} — {len(items)} 个文件 / {human(sz)}")
    A("")
    A("| # | 完整相对路径 | 大小 |")
    A("|---|-------------|------|")
    for i, (rel, s) in enumerate(items, 1):
        A(f"| {i} | `{rel}` | {human(s)} |")
    A("")

A("## 三、维度统计")
A("")
A("### 3.1 按日期维度")
A("")
A("| 日期 | 文件数 | 大小 | 主要内容 |")
A("|------|-------:|-----:|----------|")
date_desc = {
    "2026-08-11": "空目录（new-chat，无文件）",
    "2026-08-21": "GAQ-UFT 早期验证脚本 2 个",
    "2026-08-22": "哥德巴赫方法文档+脚本+zip（9 个）",
    "2026-09-03": "GAQ-UFT V50 全维分析 / 全维三重奏与多脚本验证",
    "2026-09-04": "《GAQ-UFT-大统一全书》全稿",
}
for date in sorted(by_date):
    items = by_date[date]
    sz = sum(s for _, s in items)
    A(f"| {date} | {len(items)} | {human(sz)} | {date_desc.get(date, '')} |")
A("")

A("### 3.2 按主题维度")
A("")
A("| 主题 | 文件数 | 大小 |")
A("|------|-------:|-----:|")
for t in sorted(by_topic):
    items = by_topic[t]
    sz = sum(s for _, s in items)
    A(f"| {t} | {len(items)} | {human(sz)} |")
A("")

A("### 3.3 按类型维度")
A("")
A("| 类型 | 扩展名 | 文件数 | 大小 |")
A("|------|--------|-------:|-----:|")
for ext in sorted(by_type):
    items = by_type[ext]
    sz = sum(s for _, s in items)
    A(f"| {type_names.get(ext, ext)} | `{ext}` | {len(items)} | {human(sz)} |")
A("")

A("### 3.4 按文件大小分档")
A("")
A("| 档位 | 文件数 |")
A("|------|-------:|")
for b, c in size_bins.items():
    A(f"| {b} | {c} |")
A("")

A("## 四、压缩包与解压产物")
A("")
A("| 压缩包 | 原始位置 | 内部文件数 | 解压目录 |")
A("|--------|----------|-----------:|----------|")
A("| `goldbach_methods.zip` | `2026-08-22/new-chat/` | 8 | `03_解压产物/goldbach_methods_解压/` |")
A("| `GAQ-UFT-大统一全书-整理稿.zip` | `2026-09-04/new-chat/GAQ-UFT-大统一全书/deliverables/` | 43 | `03_解压产物/GAQ-UFT-大统一全书-整理稿_解压/` |")
A("")
A("## 五、主题导读")
A("")
A("### 5.1 哥德巴赫猜想（2026-08-22）")
A("")
A("`goldbach_methods/` 内含 7 篇方法文档（筛法路线、圆法与奇异级数、密率法、计算机验证、初等谬误分类、OPEN 问题清单）+ 1 个验证脚本 `goldbach_verification.py`，并附同名 zip。")
A("")
A("### 5.2 GAQ-UFT 大统一场论（2026-08-21 / 2026-09-03 / 2026-09-04）")
A("")
A("三个日期来源：")
A("- **2026-08-21**：早期验证脚本 `verify_gaq_uft.py` / `_v2.py`；")
A("- **2026-09-03**：`new-chat/` 为 V50 全维分析（报告 HTML、全维度全链路 MD、验证脚本与输出、HTML 预览图）；`new-chat-1/uft/` 为全维三重奏与多脚本验证（13 个 verify_*.py、多篇算法联盟文档、企业化 `enterprise/` 工程包、知识图谱 HTML、各验证结果 txt 及预览图）；")
A("- **2026-09-04**：`GAQ-UFT-大统一全书/` 全稿（outline / 分章 manuscript ch00–ch21 / 合并稿 final.md / 架构图 HTML / 校验 code / 备份 _backup_pre_fix / 整理稿 zip）。")
A("")
A("## 六、说明与保留内容")
A("")
A("- 本归档为**只读快照**：所有文件均从源目录复制而来，未对内容做任何改动。")
A("- 隐藏目录（`.preview/`、`.doubao-book-writer/`、`_backup_pre_fix/`）均原样保留。")
A("- 空目录：`2026-08-11/new-chat/`、`2026-09-03/new-chat-2/`、`2026-09-04/new-chat-1/`、书目录 `sources/` 为空，已在镜像中保留。")
A("- 构建脚本：`build_archive.py`（复制/解压/归类，可复现本归档）、`gen_readme.py`（生成本清单）。")
A("")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(L))
print("README 生成完成:", OUT)
print("行数:", len(L))
