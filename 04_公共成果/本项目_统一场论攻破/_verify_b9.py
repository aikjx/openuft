# -*- coding: utf-8 -*-
import io, glob, subprocess, sys, os, json, traceback
dirp = r'D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破'
out = []
for pid in ['C0304','C0305','C0306','C0307']:
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
        e1 = d['entries'][0]['value'][:85] if d.get('entries') else ''
        out.append(f"{pid}: rc={rc}, guards={sum(1 for g in guards if g.get('passed'))}/{len(guards)} | {e1}")
    except Exception as ex:
        out.append(f"{pid}: EXC {traceback.format_exc()[-200:]}")
io.open(dirp + r'\_verify_b9.txt', 'w', encoding='utf-8', newline='').write('\n'.join(out))
