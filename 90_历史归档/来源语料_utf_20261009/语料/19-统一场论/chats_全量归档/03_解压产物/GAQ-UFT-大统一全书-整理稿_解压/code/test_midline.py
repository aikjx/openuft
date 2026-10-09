# -*- coding: utf-8 -*-
import importlib.util, io
spec = importlib.util.spec_from_file_location(
    'fm', r'C:\Users\mo\Doubao\chats\2026-09-04\new-chat\GAQ-UFT-大统一全书\code\fix_midline_heads.py')
fm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fm)

tests = [
    ('ch02-第一公理与第二公理.md',
     '前文正文……面对的核心 OPEN 项**。## 2.4 两个"亲手算"的例子### 例 1：曲率与挠率的显式计算（螺旋线）对 $\\mathbf r(t)=(r\\cos t, r\\sin t, pt) 继续正文'),
    ('ch02-第一公理与第二公理.md',
     '### 例 1：曲率与挠率的显式计算（螺旋线）对 $\\mathbf r(t)=(r\\cos t)'),
    ('ch03-第三公理.md',
     '前文……资格。## 3.6 32 的数学谱系：为什么这个数"自然"### 3.6.1 Clifford 代数与旋量$32=2^5$ 对应 Clifford'),
    ('ch03-第三公理.md',
     '### 3.6.1 Clifford 代数与旋量$32=2^5$ 对应 Clifford'),
    ('ch18-可证伪性清单.md',
     '前文……配一份"证伪卡"。## 18.2 框架核心主张的证伪卡| # | 框架主张 | 证伪条件 | 当前约束 ||---|---|---|'),
    ('ch12-宇宙演化.md',
     '前文……无机制（OPEN-C1）。## 12.5 框架与标准宇宙学的关系- 标准宇宙学（ΛCDM）是【已证实】的基准模型，本书不否定它'),
]
for chap, seg in tests:
    out = []
    fm.split_segment(seg, chap, out)
    print('===', chap)
    for ln in out:
        print('   |', ln[:95])
