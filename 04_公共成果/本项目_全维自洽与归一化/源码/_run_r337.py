# -*- coding: utf-8 -*-
"""r337 runner：UTF-8 模式运行本卷，输出落 源码/_out_r337.txt"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = 'TUFT-r337_ROOTV24缺口吸收多重共线性_五旋钮容量定价与处方依赖与圈阶截断_精算与可视化_2026-11-01.py'
OUT = os.path.join(HERE, '_out_r337.txt')

r = subprocess.run([sys.executable, '-X', 'utf8', os.path.join(HERE, NAME)],
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                   encoding='utf-8', errors='replace')
io_open = open(OUT, 'w', encoding='utf-8')
io_open.write(r.stdout)
io_open.close()
sys.stdout.write(r.stdout)
sys.stdout.write('rc=%d\n' % r.returncode)
sys.exit(r.returncode)
