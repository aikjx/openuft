# -*- coding: utf-8 -*-
import io
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, '04_公共成果', '本项目_全维自洽与归一化', '数据')
J = lambda n: json.loads(io.open(os.path.join(DATA, n), encoding='utf-8').read())

r119 = J('TUFT-r119_统一场论完成度总判定_七条必要条件与电弱控制组_2026-10-20.json')
print('--- r119 verdict:', r119['verdict'])
for c in r119['criteria_target']:
    print('  ', c['id'], c['verdict'], '|', c['name'], '|', str(c['value'])[:80])
print('  controls:', [(c['id'], c['pass_count'], c['applicable_count']) for c in r119['controls']])
print('  U3:', {k: r119['U3_gravity'][k] for k in ('alpha_G_at_MGUT', 'alpha_GUT', 'dex_gap', 'mismatch_dex')})
print('  sm_unif:', r119['data']['sm_unification_failure'])
print('  proton:', r119['data']['proton_decay'])
print('  ew metrics:', r119['electroweak_metrics'])
print('  gut:', r119['data']['gut_mssm'])
print('  guards:', r119['guards']['passed'], '/', r119['guards']['total'])

r130 = J('TUFT-r130_攻破推导链_正确理论体系与方程的隐藏前提审计_2026-10-20.json')
print('--- r130 summary:', json.dumps(r130['summary'], ensure_ascii=False))

r133 = J('TUFT-r133_修补失敗元原理_修改逐个审计与结构不可修补定理_2026-10-20.json')
print('--- r133 meta:', json.dumps(r133['meta'], ensure_ascii=False)[:900])

r135 = J('TUFT-r135_第一性原理突破尝试_无质量自旋2导出EH与SEP及净前提下降门机检_2026-10-21.json')
print('--- r135 door:', json.dumps(r135['door_accounting'], ensure_ascii=False)[:900])
print('--- r135 verdict:', r135.get('verdict'), '|', str(r135.get('verdict_detail'))[:300])

r138 = J('TUFT-r138_硬核审计_规范群与mu2符号的第一性原理可导出性精算_2026-10-21.json')
print('--- r138 checks G2:', json.dumps(r138['checks']['G2'], ensure_ascii=False))
print('--- r138 H1:', json.dumps(r138['checks']['H1'], ensure_ascii=False))
print('--- r138 keys:', list(r138.keys()))
