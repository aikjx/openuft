# -*- coding: utf-8 -*-
# P3：520 项 C 级登记补 source/updated 字段（2026-10-30）
# source 分类（启发式关键词）：观测/判据/模型/理论
import json, glob, os

d = r'D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破'
files = sorted(glob.glob(os.path.join(d, 'attack_CLEAR*_清尾全域自动攻破_2026-10-29.json')))

OBS = ['实测', '测量', '约束', '上限', '下限', '最佳拟合', '观测', '实验', '探测', '数据', '统计', '误差']
CRI = ['判据', '指标', '归一', '阈值', '判据式', '比值', '判据']
MOD = ['模型', '标度', '窗口', '参数', '系数', '幂律', '指数', '谱', '势', '密度', '温度', '质量', '能隙', '截面']
THE = ['理论', '开放', '诠释', '本质', '严格', '证明', '猜想', '假设']

def classify(claim, value):
    s = claim
    if any(w in s for w in OBS):
        return '观测'
    if any(w in s for w in CRI) or value in ('1.0', '0.0', '1', '0', '0.5', '2.0'):
        return '判据'
    if any(w in s for w in MOD):
        return '模型'
    return '理论'

stats = {}
total = 0
for f in files:
    data = json.load(open(f, encoding='utf-8'))
    for e in data['entries']:
        if e['verdict'] != 'REGISTERED':
            continue
        total += 1
        src = classify(e['claim'], e['value'])
        e['source'] = src
        e['updated'] = '2026-10-30'
        stats[src] = stats.get(src, 0) + 1
    with open(f, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
print('REGISTERED 总计 =', total)
for k, v in sorted(stats.items(), key=lambda x: -x[1]):
    print(k, '=', v)
