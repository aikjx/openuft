# -*- coding: utf-8 -*-
"""r124 runner（ASCII-only 控制台）：光子内部运行求导证明与修复定价 · 核心理论体系
用法：python openuft/_run_r124.py
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(
    HERE,
    '04_公共成果',
    '本项目_全维自洽与归一化',
    '源码',
    'TUFT-r124_光子内部运行求导证明与修复定价_核心理论体系_2026-10-20.py',
)

if not os.path.exists(TARGET):
    sys.stderr.write('TARGET NOT FOUND: ' + TARGET + '\n')
    sys.exit(2)

r = subprocess.run([sys.executable, TARGET], encoding='utf-8', errors='replace',
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
sys.stdout.write(r.stdout)
sys.exit(r.returncode)
