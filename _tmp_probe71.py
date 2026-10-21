# -*- coding: utf-8 -*-
import io
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

for p in ('07_统一场方程/71_全链路总览卷_2026-10-20.md',
          '07_统一场方程/72_本质本源审计卷_2026-10-20.md'):
    b = re.sub(r'```.*?```', '', io.open(p, encoding='utf-8-sig').read(), flags=re.S)
    for t in re.findall(r'!?\[[^\]\n]*\]\(([^\s)]+)\)', b):
        d = os.path.normpath(os.path.join(os.path.dirname(p), t.split('#')[0].strip('<>'))) if False \
            else os.path.normpath(os.path.join(os.path.dirname(p), t.split('#')[0].strip('<>')))
        if not os.path.exists(d):
            print('MISS %s -> %s' % (t, d))
            par = os.path.dirname(d)
            print('   parent isdir:', os.path.isdir(par))
            if os.path.isdir(par):
                for n in sorted(os.listdir(par)):
                    if ('r137' in n) or ('本源' in n) or n.startswith('00') or n == 'README.md':
                        print('   cand:', n)
