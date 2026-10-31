# -*- coding: utf-8 -*-
"""r265 探针：定位靶语料中的「引力波 / 张量 / 偏振 / 传播速度」相关行。"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "数据"))
TARGETS = [
    os.path.join(DATA, "TUFT-r241_光速螺旋_来料原件_2026-10-30",
                 "基于光速螺旋流形的核心动力学方程组.md"),
    os.path.join(DATA, "TUFT-r241_光速螺旋曲率挠率全域统一场论_理论体系整理与机器核验_2026-10-30.md"),
    os.path.join(DATA, "TUFT-r242_光速螺旋曲率挠率修复候选式机器核验_2026-10-30.md"),
]

KEYS = ["引力波", "重力波", "张量", "偏振", "极化", "四极", "GW150914", "GW170817",
        "啁啾", "chirp", "干涉", "LIGO", "横波", "纵波", "色散", "传播速度",
        "引力子", "自旋2", "自旋-2", "h_{ij}", "TT", "应变"]


def depollute(s):
    s = re.sub(r"\\\(\\boldsymbol\s+([A-Za-z])\)([A-Za-z])", r"\\\1\2", s)
    s = re.sub(r"\\\(\\boldsymbol\s+([A-Za-z])\)", r"\1", s)
    out, i, n = [], 0, len(s)
    while True:
        j = s.find("\\boldsymbol", i)
        if j < 0:
            out.append(s[i:])
            break
        out.append(s[i:j])
        k = j + len("\\boldsymbol")
        if k < n and s[k] == "{":
            depth, m = 0, k
            while m < n:
                if s[m] == "{":
                    depth += 1
                elif s[m] == "}":
                    depth -= 1
                    if depth == 0:
                        break
                m += 1
            inner = s[k + 1:m] if m < n else s[k + 1:]
            out.append(inner)
            i = m + 1
        else:
            while k < n and s[k] == " ":
                k += 1
            if k >= n:
                i = k
            elif s[k] == "\\":
                mm = re.match(r"\\[A-Za-z]+", s[k:])
                if mm:
                    out.append(mm.group(0))
                    i = k + len(mm.group(0))
                else:
                    i = k + 1
            else:
                out.append(s[k])
                i = k + 1
    return re.sub(r"[\r\n]+", "\n", "".join(out))


def main():
    lines_out = []
    for p in TARGETS:
        if not os.path.exists(p):
            lines_out.append("MISSING: %s" % p)
            continue
        raw = io.open(p, "r", encoding="utf-8", errors="replace").read()
        txt = depollute(raw)
        lines = txt.split("\n")
        lines_out.append("=" * 100)
        lines_out.append("FILE %s  lines=%d  boldsymbol_residual=%d" % (
            os.path.basename(p), len(lines), txt.count("\\boldsymbol")))
        hits = []
        for i, s in enumerate(lines):
            n = sum(1 for k in KEYS if k in s)
            if n:
                hits.append((i + 1, n, s.strip()))
        lines_out.append("hit lines = %d" % len(hits))
        for ln, n, s in hits:
            lines_out.append("L%-6d [%d] %s" % (ln, n, s[:260]))
    out = "\n".join(lines_out)
    dst = os.path.join(HERE, "_probe_gw_out.txt")
    io.open(dst, "w", encoding="utf-8").write(out)
    print(out[:6000])
    print("\n[written] %s  (%d chars)" % (dst, len(out)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
