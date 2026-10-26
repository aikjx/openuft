# -*- coding: utf-8 -*-
import os, io
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化", "README.md")
with io.open(README, "r", encoding="utf-8") as f:
    lines = f.read().split("\n")
for i, ln in enumerate(lines):
    if "TUFT-r147_" in ln and ("\u4fee\u590d" in ln):
        print(i + 1, "|", repr(ln[:28]))
