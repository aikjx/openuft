# -*- coding: utf-8 -*-
import io, re, glob, os
root = r'C:\Users\mo\Doubao\chats\2026-09-04\new-chat\GAQ-UFT-大统一全书\manuscript'
pat_inline = re.compile(r'(?<!\$)\$(?!\$)[^$\n]+\$(?!\$)')
pat_disp = re.compile(r'\$\$[^$]+\$\$')
for p in sorted(glob.glob(os.path.join(root, 'ch*.md'))):
    with io.open(p, encoding='utf-8') as f:
        txt = f.read()
    inline = len(pat_inline.findall(txt))
    disp = len(pat_disp.findall(txt))
    print('%s: 行内 %d, 块级 %d' % (os.path.basename(p)[:14], inline, disp))
