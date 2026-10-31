# -*- coding: utf-8 -*-
"""r256 探针：定位靶语料中 Lambda / 暗能量 / 宇宙常数 的全部第一手文本。只读，不改任何靶文件。"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "数据"))

TARGETS = [
    "TUFT-r241_光速螺旋_来料原件_2026-10-30/基于光速螺旋流形的核心动力学方程组.md",
    "TUFT-r241_光速螺旋曲率挠率全域统一场论_理论体系整理与机器核验_2026-10-30.md",
    "TUFT-r242_光速螺旋曲率挠率修复候选式机器核验_2026-10-30.md",
]

_ALPHA52 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def depollute(s):
    for ch in _ALPHA52:
        s = s.replace("\\(\\boldsymbol{" + ch + "}\\)", ch)
    s = re.sub(r"[\r\n]+", "\n", s)
    return s


def load(p):
    with io.open(p, "r", encoding="utf-8", errors="replace") as f:
        return depollute(f.read())


KEYS = ["Lambda", "\\Lambda", "暗能量", "宇宙常数", "真空能", "cosmological constant",
        "Omega_\\Lambda", "Omega_Lambda", "\\Omega_\\Lambda", "加速膨胀", "de Sitter",
        "A_\\Lambda", "98", "68.3", "0.7", "1e-120", "10^{-120}", "120 个数量级"]


def main():
    out = []
    for rel in TARGETS:
        p = os.path.join(DATA, rel)
        if not os.path.exists(p):
            out.append("MISSING " + rel)
            continue
        txt = load(p)
        lines = txt.split("\n")
        out.append("")
        out.append("=" * 100)
        out.append("FILE %s" % rel)
        out.append("lines=%d chars=%d" % (len(lines), len(txt)))
        out.append("=" * 100)
        idx = {}
        for k in KEYS:
            hits = [i + 1 for i, s in enumerate(lines) if k in s]
            idx[k] = hits
        for k in KEYS:
            out.append("  KEY %-24s hits=%4d  lines=%s" % (k, len(idx[k]), idx[k][:40]))
        # 逐行打印含核心关键词的行
        core = set()
        for k in ["暗能量", "宇宙常数", "真空能", "cosmological constant", "加速膨胀",
                  "de Sitter", "120"]:
            core.update(idx.get(k, []))
        for k in ["Lambda"]:
            core.update(idx.get(k, []))
        out.append("")
        out.append("---- 含核心词的行 (共 %d) ----" % len(core))
        for ln in sorted(core):
            s = lines[ln - 1]
            if len(s) > 400:
                s = s[:400] + " ...[TRUNC]"
            out.append("L%-6d %s" % (ln, s))
    rp = os.path.join(HERE, "_probe_r256_out.txt")
    with io.open(rp, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("written", rp)
    print("\n".join(out[:60]))


if __name__ == "__main__":
    main()
