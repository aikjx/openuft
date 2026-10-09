# -*- coding: utf-8 -*-
import io
p = r'C:\Users\mo\Doubao\chats\2026-09-04\new-chat\GAQ-UFT-大统一全书\manuscript\ch02-第一公理与第二公理.md'
with io.open(p, encoding='utf-8') as f:
    txt = f.read()
old = '### 2.2.1 预备：曲线的曲率与挠率设 $\\mathbf r(s)$ 是弧长参数化的空间曲线。Frenet-Serret 方程描述其三个正交单位向量（切向 $\\mathbf T$、法向 $\\mathbf N$、副法向 $\\mathbf B$）的演化：'
new = '### 2.2.1 预备：曲线的曲率与挠率\n设 $\\mathbf r(s)$ 是弧长参数化的空间曲线。Frenet-Serret 方程描述其三个正交单位向量（切向 $\\mathbf T$、法向 $\\mathbf N$、副法向 $\\mathbf B$）的演化：'
assert old in txt, 'not found'
txt = txt.replace(old, new)
with io.open(p, 'w', encoding='utf-8') as f:
    f.write(txt)
print('OK, split 2.2.1')
