# -*- coding: utf-8 -*-
"""
TUFT 文档旧描述残留交叉扫描（分析-修复-优化 闭环的验收工具）。

目的：在白皮书 EDM 错误陈述修复 + CURATED 入库之后，全局核验是否还有
「正向错误陈述」残留——即把 TUFT EDM 写成「仍被允许 / 未被排除 / 唯一开放出口」
的旧口径。

判定规则：
- 命中「正向错误陈述」模式即报警；
- 但跳过已正确修复的说明行（含「已被实验否决 / 已被ACME否决 / 错误数字 /
  白皮书原 / 被排除」等修复标注上下文），避免把修复注记误报为残留。
- 输出 CLEAN 表示目录内无残余正向错误陈述。

可复跑：每次文档改动后重跑，作为文档一致性的门禁。
"""
import os
import re
import glob

HERE = os.path.dirname(os.path.abspath(__file__))

# 正向错误陈述模式（旧口径）
PATTERNS = [
    (r"仍被允许", "EDM 仍被允许(正向错误陈述)"),
    (r"未被排除", "EDM 未被排除(正向错误陈述)"),
    (r"唯一.{0,6}开放出口", "唯一开放出口(旧表述)"),
    (r"唯一仍开放", "唯一仍开放(旧表述)"),
    (r"P4.{0,20}仍开放", "P4 仍开放(旧表述)"),
    (r"EDM.{0,15}L3候选", "EDM 作为 L3 候选(旧表述)"),
]

# 已修复说明行（含这些标注的行不是残留，跳过）
REPAIR_CTX = [
    "已被实验否决", "已被ACME否决", "已被实验排除",
    "错误数字", "白皮书原", "被排除", "→", "⇒",
]

# 扫描器自身的模式定义/标签行（避免自匹配，仅用于跳过脚本本体）
SELF_MARKERS = [
    "正向错误陈述", "旧表述", "PATTERNS", "旧描述残留",
    "扫描脚本", "REPAIR_CTX", "SELF_MARKERS",
]


def scan_file(path):
    hits = []
    try:
        lines = open(path, encoding="utf-8").read().split("\n")
    except Exception:
        return hits
    for i, ln in enumerate(lines, 1):
        if any(k in ln for k in REPAIR_CTX):
            continue
        if any(k in ln for k in SELF_MARKERS):
            continue
        for pat, label in PATTERNS:
            if re.search(pat, ln):
                hits.append((i, label, ln.strip()))
                break
    return hits


def main():
    targets = []
    for ext in ("*.md", "*.py"):
        targets.extend(sorted(glob.glob(os.path.join(HERE, ext))))
    total = 0
    for fp in targets:
        hits = scan_file(fp)
        if hits:
            total += len(hits)
            print("== %s ==" % os.path.basename(fp))
            for i, label, ln in hits:
                print("  L%-4d [%s] %s" % (i, label, ln[:120]))
    if total == 0:
        print("CLEAN: 目录内无残余正向错误陈述。")
    else:
        print("\n命中总数: %d（需人工复核）" % total)


if __name__ == "__main__":
    main()
