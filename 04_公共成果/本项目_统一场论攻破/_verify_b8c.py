# -*- coding: utf-8 -*-
import io, glob, subprocess, sys, os, json, traceback
dirp = r'D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破'
out = []
for pid in ['C0300','C0301','C0302','C0303']:
    try:
        pys = glob.glob(dirp + r'\attack_' + pid + '_*.py')
        r = subprocess.run([sys.executable, '-X', 'utf8', pys[0]], capture_output=True, text=True, encoding='utf-8', timeout=120)
        rc = r.returncode
        err = (r.stdout + '\n' + r.stderr)[-200:]
        jsons = glob.glob(dirp + r'\attack_' + pid + '_*.json')
        if not jsons:
            out.append(f"{pid}: rc={rc}, NO JSON :: {err}"); continue
        d = json.load(io.open(jsons[0], encoding='utf-8'))
        guards = d.get('guards', [])
        e1 = d['entries'][0]['value'][:80] if d.get('entries') else ''
        e2 = d['entries'][1]['value'][:70] if len(d.get('entries', [])) > 1 else ''
        out.append(f"{pid}: rc={rc}, guards={sum(1 for g in guards if g.get('passed'))}/{len(guards)} | {e1} || {e2}")
    except Exception as ex:
        out.append(f"{pid}: EXC {traceback.format_exc()[-200:]}")
p = dirp + r'\_verify_b8c.txt'
io.open(p, 'w', encoding='utf-8', newline='').write('\n'.join(out))
print("WROTE", os.path.getsize(p))
