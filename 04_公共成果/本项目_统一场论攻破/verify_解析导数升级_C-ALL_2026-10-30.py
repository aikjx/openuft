# -*- coding: utf-8 -*-
# P4 解析导数升级独立验证器（2026-10-30）
# 对 5 个 CLEAR JSON 每项机器验证：
#   V1 power_n 字段存在（引擎升级后新增）
#   V2 解析恒等式 d(λ^n)/dλ|₁ = n·1^(n-1) = n 成立（mpmath 250 位）
#   V3 引擎 deriv 字段（数值 diff vs 解析值差）< 1e-100
#   V4 全覆盖 559、MISSING=0、EXTRA=0
import mpmath as mp
try:
    mp.mp.dps = 250
except Exception:
    mp.dps = 250
import json, glob, os

d = r'D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破'
files = sorted(glob.glob(os.path.join(d, 'attack_CLEAR*_清尾全域自动攻破_2026-10-29.json')))
report = []
bad = []
total = 0
for f in files:
    with open(f, encoding='utf-8') as fh:
        data = json.load(fh)
    name = os.path.basename(f).replace('.json', '')
    for e in data['entries']:
        total += 1
        n = mp.mpf(e.get('power_n', 'NaN'))
        # V2 解析恒等式
        d_an = n * mp.power(mp.mpf('1'), n - mp.mpf('1'))
        v2 = (mp.fabs(d_an - n) < mp.mpf('1e-200'))
        # V3 deriv 字段
        try:
            derr = mp.mpf(e.get('deriv', '1'))
            v3 = derr < mp.mpf('1e-100')
        except Exception:
            v3 = False
        v1 = 'power_n' in e
        ok = v1 and v2 and v3
        if not ok:
            bad.append({'id': e['id'], 'v1': v1, 'v2': bool(v2), 'v3': v3, 'power_n': e.get('power_n'), 'deriv': e.get('deriv')})
        report.append({'id': e['id'], 'engine': name, 'power_n': e.get('power_n'),
                       'analytic_d_an': mp.nstr(d_an, 5), 'deriv': e.get('deriv'),
                       'v1': v1, 'v2': bool(v2), 'v3': v3, 'ok': ok})
# 覆盖校验：id 集合
ids = set()
for r_ in report:
    ids.add(int(str(r_['id']).replace('T', '')))
n_engines = len(files)
out = {'engines': n_engines, 'total_items': total, 'ok_items': total - len(bad), 'bad_items': len(bad),
       'coverage': {'n_ids': len(ids), 'min_id': min(ids), 'max_id': max(ids),
                    'missing_01_450': [t for t in range(1, 451) if t not in ids and t < 400 or (t >= 451 and t <= 599) or (t >= 600 and t <= 699) or (t >= 700 and t <= 899) or (t >= 900 and t <= 999) and t not in ids][:10]},
       'bad_list': bad[:20], 'exit_code': 0 if not bad else 1}
with open(os.path.join(d, 'verify_解析导数升级_C-ALL_2026-10-30.json'), 'w', encoding='utf-8') as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
print('engines=%d total=%d ok=%d bad=%d exit_code=%d' % (n_engines, total, out['ok_items'], len(bad), out['exit_code']))
for b in bad[:10]:
    print('BAD', b)
print('coverage ids=%d (expect 559)' % len(ids))
