# -*- coding: utf-8 -*-
import os, sys, glob
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
BASE = os.path.join(r'd:\a10\aikjx\code\my_lib\openuft', '04_公共成果', '本项目_全维自洽与归一化')
for sub in ('', '源码', '数据'):
    d = os.path.join(BASE, sub) if sub else BASE
    for f in sorted(os.listdir(d)):
        if 'r375' in f or 'r374' in f or 'r369' in f:
            print(sub or 'ROOT', '|', f)
