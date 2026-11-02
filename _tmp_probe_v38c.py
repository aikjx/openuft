# -*- coding: utf-8 -*-
import os, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = r'd:\a10\aikjx\code\my_lib\openuft'
hits = []
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in ('.git', 'node_modules', '__pycache__')]
    for f in fn:
        if 'r375' in f or 'r374' in f:
            hits.append(os.path.join(dp, f))
print(len(hits))
for h in hits:
    print(h.replace(ROOT, '.'), os.path.getsize(h))
