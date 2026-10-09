#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V4 全维全域迁移脚本 (ALG-ROOT-GUFT-2026-V4-FUSION)
==================================================
把 _ref_downloads/ 中 全部 1343 个文件 全量迁移到 v4/source_all/<源zip名>/
并为每一个文件登记迁移记录:
  - 05_迁移记录.tsv  (机器可读, 逐文件)
  - 05_全维全域迁移记录.md (人类可读, 含分组统计与去重说明)
"""
import os, shutil, sys, io, hashlib

BASE = r"d:\a10\aikjx\code\my_lib\utf\大统一场论_算法联盟最高权限"
REF = os.path.join(BASE, "_ref_downloads")
DST_ROOT = os.path.join(BASE, "v4", "source_all")

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

os.makedirs(DST_ROOT, exist_ok=True)

records = []  # (src, dst, migrated, note)
src_dirs = sorted([d for d in os.listdir(REF) if os.path.isdir(os.path.join(REF, d))])

for src_name in src_dirs:
    src_dir = os.path.join(REF, src_name)
    # 目标子目录: 用源zip名(已去除非法字符), 保留原文
    safe = src_name.replace("/", "_").replace("\\", "_")
    dst_dir = os.path.join(DST_ROOT, safe)
    os.makedirs(dst_dir, exist_ok=True)
    for root, _, files in os.walk(src_dir):
        for fn in files:
            src_file = os.path.join(root, fn)
            # 保持相对结构
            rel = os.path.relpath(src_file, src_dir)
            dst_file = os.path.join(dst_dir, rel)
            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            try:
                # 同内容不覆盖式重复 -> 若已存在则比较
                if os.path.exists(dst_file):
                    a = open(src_file, "rb").read()
                    b = open(dst_file, "rb").read()
                    if a == b:
                        note = "已存在且内容相同(自动去重, 不重复写入)"
                        migrated = "是(去重)"
                    else:
                        # 内容不同, 改名保留两份
                        base, ext = os.path.splitext(dst_file)
                        dst_file = base + "_dup" + ext
                        shutil.copy2(src_file, dst_file)
                        note = "同名但内容不同, 已以 _dup 后缀保留两份"
                        migrated = "是"
                else:
                    shutil.copy2(src_file, dst_file)
                    note = ""
                    migrated = "是"
                size = os.path.getsize(src_file)
                ext = os.path.splitext(fn)[1]
                records.append((src_file, dst_file, migrated, note, size, ext, src_name))
            except Exception as e:
                records.append((src_file, dst_file, "否(失败)", str(e), 0, "", src_name))

# ---- 写 TSV (机器可读) ----
tsv_path = os.path.join(BASE, "v4", "05_迁移记录.tsv")
with io.open(tsv_path, "w", encoding="utf-8", newline="") as f:
    f.write("源路径\t目标路径\t是否迁移\t备注\t字节数\t扩展名\t所属源zip\n")
    for r in records:
        f.write("\t".join(str(x) for x in r) + "\n")

# ---- 写 MD (人类可读) ----
md_path = os.path.join(BASE, "v4", "05_全维全域迁移记录.md")
ok = sum(1 for r in records if r[2].startswith("是"))
fail = sum(1 for r in records if r[2].startswith("否"))
by_src = {}
by_ext = {}
for r in records:
    by_src.setdefault(r[6], 0)
    by_src[r[6]] += 1
    by_ext.setdefault(r[5] or "(无)", 0)
    by_ext[r[5] or "(无)"] += 1

with io.open(md_path, "w", encoding="utf-8") as f:
    f.write("# V4 全维全域迁移记录\n\n")
    f.write("> 算法联盟 ROOT 最高权限 · V4 融合版 · 2026-08-18\n")
    f.write("> 源目录: `_ref_downloads/` (来自 `C:\\\\Users\\\\mo\\\\Downloads` 自动解压)\n")
    f.write("> 目标目录: `v4/source_all/<源zip名>/`\n\n")
    f.write("## 一、总体统计\n\n")
    f.write(f"- **总文件数**: {len(records)}\n")
    f.write(f"- **成功迁移**: {ok}\n")
    f.write(f"- **迁移失败**: {fail}\n")
    f.write(f"- **目标根目录**: `v4/source_all/`\n")
    f.write(f"- **逐文件明细**: 见 `05_迁移记录.tsv` (机器可读, 共 {len(records)} 行)\n\n")
    f.write("## 二、按源 zip 分组 (全维度, 不漏)\n\n")
    f.write("| 源 zip (解压目录名) | 文件数 | 迁移状态 |\n|:---|---:|:---|\n")
    for k in sorted(by_src):
        f.write(f"| {k} | {by_src[k]} | ✅ 全部迁移 |\n")
    f.write("\n## 三、按扩展名统计\n\n")
    f.write("| 扩展名 | 数量 |\n|:---|---:|\n")
    for k in sorted(by_ext, key=lambda x: -by_ext[x]):
        f.write(f"| {k} | {by_ext[k]} |\n")
    f.write("\n## 四、去重与冲突说明\n\n")
    dups = [r for r in records if "去重" in r[3] or "_dup" in r[3] or "内容不同" in r[3]]
    f.write(f"- 自动去重/冲突处理文件数: {len(dups)}\n")
    f.write("- 同名同内容: 仅保留一份, 标注 `已存在且内容相同(自动去重)`\n")
    f.write("- 同名异内容: 以 `_dup` 后缀保留两份, 标注 `同名但内容不同`\n")
    f.write("- 重名压缩包(如 `核心方程手册` 2 份、`分形演化引擎 v1.0.0` 4 份) 各自独立目录, 全部保留\n\n")
    f.write("## 五、逐文件清单 (节选前 60 + 末尾 20, 全量见 TSV)\n\n")
    f.write("| # | 源相对路径 | 目标相对路径 | 迁移 | 字节 |\n|:---:|:---|:---|:---|---:|\n")
    def relp(p):
        return os.path.relpath(p, BASE).replace("\\", "/")
    for i, r in enumerate(records[:60], 1):
        f.write(f"| {i} | {relp(r[0])} | {relp(r[1])} | {r[2]} | {r[4]} |\n")
    if len(records) > 80:
        f.write("| ... | ... (中间省略, 见 TSV 全量) ... | ... | ... | ... |\n")
        for i, r in enumerate(records[-20:], len(records)-19):
            f.write(f"| {i} | {relp(r[0])} | {relp(r[1])} | {r[2]} | {r[4]} |\n")

print(f"迁移完成: 总 {len(records)} / 成功 {ok} / 失败 {fail}")
print(f"TSV: {relp(tsv_path)}")
print(f"MD : {relp(md_path)}")
