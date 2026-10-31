# -*- coding: utf-8 -*-
"""修正 r289 消歧节插入位置：从正文中部移除，追加到文件末尾。"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

START = "## 附 · 编号消歧（撞号第 N 次）"
END = "**下轮从 r291 复查起**。"


def fix(path):
    with open(path, "r", encoding="utf-8") as f:
        s = f.read()
    i = s.find(START)
    if i < 0:
        print("[skip] no block:", os.path.basename(path)[:40])
        return
    j = s.find(END, i)
    if j < 0:
        print("[fail] no end:", os.path.basename(path)[:40])
        return
    j += len(END)
    block = s[i:j]
    rest = s[:i] + s[j:]
    rest = rest.rstrip("\n") + "\n\n---\n\n" + block + "\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(rest)
    print("[fixed]", os.path.basename(path)[:45], "moved", j - i, "chars")


def main():
    d = os.path.join(ROOT, "数据")
    j = os.path.join(ROOT, "判定")
    for f in os.listdir(d):
        if f.startswith("TUFT-r289_") and f.endswith("_2026-10-31.md") and "来料原件" not in f:
            fix(os.path.join(d, f))
    for f in os.listdir(j):
        if f.startswith("判定_TUFT-r289_"):
            fix(os.path.join(j, f))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
