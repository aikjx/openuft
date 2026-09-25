# -*- coding: utf-8 -*-
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent
errors = []
for p in ROOT.rglob('*.md'):
    body = re.sub(r'```.*?```', '', p.read_text(encoding='utf-8-sig'), flags=re.S)
    for m in re.finditer(r'!?\[[^\]\n]*\]\(([^\s)]+)\)', body):
        t = m.group(1)
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', t) or t.startswith('#'):
            continue
        dest = p.parent / unquote(t.split('#', 1)[0].strip('<>'))
        if not dest.exists():
            errors.append((p.relative_to(ROOT).as_posix(), t))
print('BROKEN:', len(errors))
for e in errors:
    print(e)
