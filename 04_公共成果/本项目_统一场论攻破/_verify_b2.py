# -*- coding: utf-8 -*-
import io, glob, subprocess, sys, os, json
dirp = r'D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破'
out = []
for pid in ['C0275','C0276','C0277','C0278']:
    pys = glob.glob(dirp + r'\attack_' + pid + '_*.py')
    rc = subprocess.run([sys.executable, '-X', 'utf8', pys[0]], capture_output=True, text=True, encoding='utf-8').returncode
    files = [f for f in os.listdir(dirp) if f.startswith('attack_'+pid+'_') or f.startswith('判定_'+pid+'_')]
    jsons = glob.glob(dirp + r'\attack_' + pid + '_*.json')
    d = json.load(io.open(jsons[0], encoding='utf-8'))
    out.append(f"{pid}: rc={rc}, files={len(files)}, json_exit={d.get('exit_code')}, entries={len(d.get('entries',[]))}, tuft={d['entries'][-1]['claim'][:30]}")
io.open(dirp + r'\_verify_b2.txt', 'w', encoding='utf-8', newline='').write('\n'.join(out))
