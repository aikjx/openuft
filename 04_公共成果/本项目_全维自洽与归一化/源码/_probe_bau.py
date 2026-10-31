# -*- coding: utf-8 -*-
"""r262 探针：定位靶语料中「重子不对称 / η_B / 轻子生成 / 电弱重子生成」的全部第一手文本。
只读，不改任何靶文件。"""
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "数据"))

TARGETS = [
    "TUFT-r241_光速螺旋_来料原件_2026-10-30/基于光速螺旋流形的核心动力学方程组.md",
    "TUFT-r241_光速螺旋曲率挠率全域统一场论_理论体系整理与机器核验_2026-10-30.md",
    "TUFT-r242_光速螺旋曲率挠率修复候选式机器核验_2026-10-30.md",
]
_ALPHA52 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def depollute(s):
    s = re.sub(r"\\boldsymbol\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\\boldsymbol\s+([A-Za-z])", r"\1", s)
    for ch in _ALPHA52:
        s = s.replace("\\(\\boldsymbol{" + ch + "}\\)", ch)
    return re.sub(r"[\r\n]+", "\n", s)


KEYS = ["重子不对称", "BAU", "eta_B", "\\eta_B", "η_B", "轻子生成", "leptogenesis",
        "Leptogenesis", "sphaleron", "Sphaleron", "球面子", "CP 相位", "CP相位", "CP 破缺",
        "净重子", "不对称", "重子数", "baryon", "Baryon", "6.1e-10", "6e-10", "10^{-10}",
        "电弱相变", "EWPT", "Sakharov", "萨哈罗夫", "CKM", "PMNS", "Jarlskog",
        "脱耦", "冻结", "washout", "Washout"]


def main():
    out = []
    all_lines = []
    for rel in TARGETS:
        p = os.path.join(DATA, rel)
        if not os.path.exists(p):
            out.append("MISSING " + rel)
            continue
        txt = depollute(io.open(p, "r", encoding="utf-8", errors="replace").read())
        lines = txt.split("\n")
        out.append("=" * 100)
        out.append("FILE %s   lines=%d chars=%d" % (rel.split("/")[-1][:60], len(lines), len(txt)))
        out.append("=" * 100)
        idx = {}
        for k in KEYS:
            idx[k] = [i + 1 for i, s in enumerate(lines) if k in s]
        for k in KEYS:
            if idx[k]:
                out.append("  %-14s %4d  %s" % (k, len(idx[k]), idx[k][:25]))
        for i, s in enumerate(lines):
            all_lines.append((rel.split("/")[-1][:10], i + 1, s))
    out.append("")
    out.append("TOTAL LINES %d" % len(all_lines))

    core = ("重子不对称", "BAU", "轻子生成", "Leptogenesis", "sphaleron", "Sphaleron",
            "球面子", "净重子", "重子数", "Sakharov", "电弱相变", "EWPT")
    hits = [(f, l, s) for f, l, s in all_lines if any(k in s for k in core)]
    out.append("")
    out.append("---- 含核心词的行 (共 %d) ----" % len(hits))
    for f, l, s in hits:
        if len(s) > 700:
            s = s[:700] + " ...[TRUNC]"
        out.append("%s L%-6d %s" % (f, l, s))

    rp = os.path.join(HERE, "_probe_bau_out.txt")
    io.open(rp, "w", encoding="utf-8").write("\n".join(out))
    print("written", rp, "| core hits", len(hits))
    print("\n".join(out[:40]))


if __name__ == "__main__":
    main()
