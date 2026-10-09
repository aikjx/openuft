# -*- coding: utf-8 -*-
"""全维攻破总账数据采集：枚举全部体系，提取 system.json + claims.csv 状态"""
import os, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import csv

ROOT = r"D:\a10\aikjx\code\my_lib\openuft\01_独立体系"
rows = []
for name in sorted(os.listdir(ROOT)):
    full = os.path.join(ROOT, name)
    if not os.path.isdir(full) or name == '新体系模板':
        continue
    kind = st = rev = '?'
    sj = os.path.join(full, 'system.json')
    if os.path.exists(sj):
        try:
            j = json.load(open(sj, encoding='utf-8'))
            kind = j.get('kind', '?'); st = j.get('status', '?'); rev = j.get('hypothesis_revision') or ''
        except Exception as e:
            kind = 'JSON-ERR:' + str(e)[:40]
    counts = {}
    pred = 0
    claims = os.path.join(full, 'claims.csv')
    if os.path.exists(claims):
        try:
            with open(claims, encoding='utf-8') as f:
                r = csv.reader(f); header = next(r, None)
                try:
                    si = header.index('status'); pi = header.index('prediction_value')
                except ValueError:
                    si, pi = -1, -1
                for row in r:
                    if len(row) <= max(si, pi): continue
                    if si >= 0:
                        s = row[si].strip() or 'blank'
                        counts[s] = counts.get(s, 0) + 1
                    if pi >= 0 and row[pi].strip():
                        pred += 1
        except Exception as e:
            counts = {'CSV-ERR': str(e)[:30]}
    cs = ' '.join(f"{k}:{v}" for k, v in sorted(counts.items()))
    rows.append((name, kind, st, rev, cs, pred))

print(f"{'体系':<30} {'kind':<26} {'status':<14} {'rev':<14} claims  有预测值")
for r in rows:
    print(f"{r[0]:<30} {r[1]:<26} {r[2]:<14} {r[3][:14]:<14} {r[4]:<24} {r[5]}")
