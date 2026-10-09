# ASCII-only launcher: locate the TUFT V3.4 audit script under the
# Chinese-named subfolder without writing any CJK literal in this file.
import os
import runpy

ROOT = r'd:\a10\aikjx\code\my_lib\openuft'
cand = sorted(d for d in os.listdir(ROOT) if d.startswith('04_'))
target_dir = os.path.join(ROOT, cand[0], '本项目_全维自洽与归一化', '源码')
matches = [f for f in os.listdir(target_dir)
           if 'V3.4' in f and f.endswith('.py')]
target = os.path.join(target_dir, sorted(matches)[0])
print('LAUNCHER ->', target)
runpy.run_path(target, run_name='__main__')
