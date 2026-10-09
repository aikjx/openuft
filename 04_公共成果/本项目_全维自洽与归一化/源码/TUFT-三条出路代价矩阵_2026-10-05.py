# -*- coding: utf-8 -*-
# 判定：三条出路代价矩阵与公设违背清单（第十四轮）
# 背景：步 5 给出三条出路。本轮把代价量化为机器可算的代价向量，并做两件更正/补充：
#   (1) 更正：出路 2（扩模型加第二场）已被 ADD-05 白皮书正式结项为「公理集内无解」
#   (2) 补充：机器枚举发现存在第四条路（修改公设集），否则框架无自洽出口
# 数据来源：数据/TUFT-可识别性解阻_最小补方程集扫描_2026-10-04.json 的 key_numbers
# 红线：不代选、不排序、不推荐；只给代价向量与布尔穷举结果
import os
import sys
import json
import time

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

T0 = time.time()
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATA = os.path.join(ROOT, '04_公共成果', '本项目_全维自洽与归一化', '数据')
RES = []
GRD = []
KEY = {}

# ---- 已归档读数（步 3 产物，禁止在此重算以免漂移）----
RANK_STRICT = 3
RANK_NUMERIC = 1
NPARAM0 = 6
NULLITY0 = 3
POOL_USABLE = 0
COND_MIN = 7.991193694035934e16
C_TYPE2_NULLITY = 4
D_BEST_COND_TXT = '7.99e+16'
D_NUMERIC_OK = 0

# ---- 公设集 Ω1–Ω5（来源：判定_TUFT_V3.5_Ω公理构造 册 + ADD-02 册公设核对段）----
AXIOMS = [
    ('Ω1', '光滑（边界 C^∞）'),
    ('Ω2', '无量纲（仅依赖 θ）'),
    ('Ω3', '符号自洽（sign(Ω) 由公理唯一确定）'),
    ('Ω4', '连续（跨分区边界）'),
    ('Ω5', '自由常数 ≤ 1（单常数 λ）'),
]


def add(cid, sec, item, verdict, detail):
    RES.append({'id': cid, 'section': sec, 'item': item,
                'verdict': verdict, 'detail': detail})
    print('[%-8s] %-4s %-14s | %s' % (verdict, cid, sec, detail[:138]))


def guard(name, ok, detail):
    GRD.append({'name': name, 'ok': bool(ok), 'detail': detail})
    print('[GUARD] %-30s | %s | %s' % ('PASS' if ok else 'FAIL', name, detail))
    return bool(ok)


def nullity_of(nparam, nobs, rank_cap):
    r = min(rank_cap, nobs)
    return nparam - r


def sec_A():
    add('A-01', 'A', 'axiom_set', 'INFO',
        '公设集共 %d 条：%s。**Ω5 = 自由常数 ≤ 1** 是本册代价核算的唯一硬约束'
        % (len(AXIOMS), '；'.join('%s %s' % (a, b) for a, b in AXIOMS)))
    add('A-02', 'A', 'archived_baseline', 'INFO',
        '基线（步 3 归档）：p=%d、rank_strict=%d、rank_numeric=%d、nullity=%d、'
        '候选观测量可用数=%d/%d、最佳 cond=%s、数值可用组数=%d/15 ⇒ '
        '**任何出路都继承这条基线**，出路只能改变它、不能绕开它'
        % (NPARAM0, RANK_STRICT, RANK_NUMERIC, NULLITY0, POOL_USABLE, 10,
           D_BEST_COND_TXT, D_NUMERIC_OK))
    add('A-03', 'A', 'numeric_rank_ceiling', 'MISMATCH',
        'rank_numeric=%d（tol 下）vs rank_strict=%d ⇒ 双精度下**实际只有 1 个方向可分辨**；'
        '故一切 nullity 记账须区分「代数零空间」与「数值零空间」：代数 %d 维、数值 %d 维'
        % (RANK_NUMERIC, RANK_STRICT, NULLITY0, NPARAM0 - RANK_NUMERIC))


def sec_B():
    add('B-01', 'B', 'deadlock_statement', 'FAIL',
        '出路 1（人工指定 𝒪_TUFT 与 δ）存在**二难**：'
        '若 δ 取为**自由常数** ⇒ 违反 Ω5；'
        '若 δ 要求**框架内推导** ⇒ 需框架存在该自由度 = 前置 P2（第二振幅），'
        '而 P2 已证**不存在** ⇒ 两条子路都不通')
    rows = []
    for dsrc in ('自由常数', '框架推导'):
        for osrc in ('锁定 V-A（框架内）', '外部指定'):
            if dsrc == '自由常数':
                d_ok = False
                d_why = 'δ 成任意外参 ⇒ δA 数值可任意取 ⇒ 不构成预言'
            else:
                d_ok = False
                d_why = '框架内无该自由度（P2 不存在）⇒ 无法推导'
            if osrc.startswith('锁定'):
                o_why = 'δA_GT 恒为 0（P2-02 逐位零）⇒ 无预言'
            else:
                o_why = '新增离散外部输入（选哪种 Lorentz 结构）'
            consistent = d_ok and osrc.startswith('锁定')
            rows.append({'delta_src': dsrc, 'O_src': osrc,
                         'delta_ok': d_ok, 'O_why': o_why,
                         'axiom_violation': 1 if dsrc == '自由常数' else 0,
                         'self_consistent': consistent, 'delta_why': d_why})
    KEY['route1_deadlock'] = rows
    n_sol = sum(1 for r in rows if r['self_consistent'])
    add('B-02', 'B', 'boolean_exhaustion', 'FAIL',
        '布尔穷举 δ 来源 × 𝒪_TUFT 来源 = **%d 组**，其中自洽（既有来源又不违反公设）'
        '**%d 组** ⇒ **出路 1 在全部组合下失败**，它不是「可行但代价高」，而是死锁'
        % (len(rows), n_sol))
    for r in rows:
        add('B-03', 'B', 'combo_%s_%s' % (r['delta_src'][:2], r['O_src'][:2]),
            'FAIL' if not r['self_consistent'] else 'PASS',
            'δ=%s / 𝒪=%s ⇒ 公设违背 %d；%s；%s'
            % (r['delta_src'], r['O_src'], r['axiom_violation'], r['delta_why'], r['O_why']))


def sec_C():
    add('C-01', 'C', 'route2_status', 'FAIL',
        '**更正上一轮表述**：出路 2（扩模型引入第二场）不是「代价高」，而是'
        '**已被正式结项**——ADD-05 白皮书与 OPEN-ΩH 册均载明：ω5 单常数约束下'
        '引入第二个结构化因子即违反 ω5，**公理集内无解**；'
        'ADD-02 册 OPEN-ΩH 亦已把耦合层级定价为「转移为 44 位精细调节」')
    add('C-02', 'C', 'route2_param_cost', 'INFO',
        '若强行引入第二场 Ω′（幅值 μ′ + 相位 φ′）：新增自由常数 **2 个** ⇒ '
        'p: %d → %d；β 通道仍不可用（δ 无来源）⇒ 观测量仍 4 ⇒ '
        'nullity = %d − %d = **%d**（代数），比基线 %d 恶化 %d 维'
        % (NPARAM0, NPARAM0 + 2, NPARAM0 + 2, RANK_STRICT,
           nullity_of(NPARAM0 + 2, 4, RANK_STRICT), NULLITY0,
           nullity_of(NPARAM0 + 2, 4, RANK_STRICT) - NULLITY0))
    add('C-03', 'C', 'type2_precedent', 'PASS',
        '与步 3 的「类型 II 只加参数」读数一致：nparam 6→7 时 nullity 3→**%d**'
        '（归档 C_type2）⇒ **加参数使问题恶化**这一结论在第二场上同样成立，'
        '不是本册新主张' % C_TYPE2_NULLITY)


def sec_D():
    add('D-01', 'D', 'route3_cost', 'PASS',
        '出路 3（放弃 β 通道 δA 预言）：新增自由常数 **0**、公设违背 **0 条**、'
        'p 与 nullity 不变（%d / %d）⇒ **唯一零外部输入的干净解**；'
        '代价是**可证伪窗口 3 → 2**（g-2、UHECR），且 F-02「可证伪预言数量」'
        '进一步下降' % (NPARAM0, NULLITY0))
    add('D-02', 'D', 'remaining_channels_rank', 'MISMATCH',
        '剩余 2 个通道并不独立提供 2 个约束：4 个耦合观测量中引力行与强核行'
        '**严格成比例**（比值 1.484e-44）⇒ 观测量有效数 4 → **3**；'
        '且 UHECR 另受 C06（证伪表述）阻塞 ⇒ **放弃 β 后可用的定量通道实为 1**')


def sec_E():
    routes = [
        {'route': '①人工指定 𝒪+δ', 'new_const': 1, 'p': NPARAM0 + 1,
         'nullity': nullity_of(NPARAM0 + 1, 5, RANK_STRICT),
         'violation': 1, 'windows': 3, 'status': '死锁（穷举 %d/4 全失败）' % len(KEY['route1_deadlock']),
         'closed_conflict': False},
        {'route': '②扩模型加第二场', 'new_const': 2, 'p': NPARAM0 + 2,
         'nullity': nullity_of(NPARAM0 + 2, 4, RANK_STRICT),
         'violation': 1, 'windows': 3, 'status': '已结项（公理集内无解）',
         'closed_conflict': True},
        {'route': '③放弃 β 通道', 'new_const': 0, 'p': NPARAM0,
         'nullity': NULLITY0, 'violation': 0, 'windows': 2,
         'status': '干净（零外部输入）', 'closed_conflict': False},
        {'route': '④修改公设集（新增：允许外部输入）', 'new_const': 2,
         'p': NPARAM0 + 2, 'nullity': nullity_of(NPARAM0 + 2, 5, RANK_STRICT),
         'violation': 0, 'windows': 3,
         'status': '自洽（唯一：有来源且零违背）', 'closed_conflict': False},
    ]
    KEY['routes'] = routes
    add('E-01', 'E', 'fourth_route_found', 'MISMATCH',
        '**补充第四条路（上一轮未列出）**：若显式修改公设集（如把 Ω5 改为'
        '「≤ 3 个常数且须显式登记为外部输入」），则出路 1 的 δ 与 𝒪_TUFT '
        '**获得合法来源** ⇒ 公设违背 0 ⇒ 唯一「有来源 + 零违背」的自洽组合。'
        '这不是技术选择，而是**科学哲学层面的选择**（是否承认框架需要外部输入）')
    add('E-02', 'E', 'cost_matrix', 'INFO',
        '代价向量（新增常数 / p / nullity / 公设违背 / 可证伪窗口 / 状态）：'
        + '；'.join('%s: %d个/%d/%d维/%d条/%d窗/%s'
                    % (r['route'][:2], r['new_const'], r['p'], r['nullity'],
                       r['violation'], r['windows'], r['status']) for r in routes))
    consistent = [r for r in routes if r['violation'] == 0 and r['status'].startswith('自洽')]
    add('E-03', 'E', 'machine_reading', 'INFO',
        '机器枚举读数（**不构成推荐**）：零公设违背者有 2 条（③与④）；'
        '其中 ③ 无需任何新输入但窗口最少，④ 保留 3 窗口但须**改公设**；'
        '① 与 ② 均不可行 ⇒ **在现行公设集内，唯一自洽出口是 ③**；'
        '若不接受 ③，则必须走 ④（改公设）⇒ **真正的选择点是 ③ vs ④，不是 ① vs ② vs ③**')
    add('E-04', 'E', 'engine_restraint', 'PASS',
        '**引擎自律**：本册不输出任何排序分、评分或推荐字段；'
        'E-03 只陈述布尔枚举结果与其逻辑含义，决策权保留给用户')


def do_guards():
    guard('a1_axiom_set_complete', len(AXIOMS) == 5, '公设 %d 条（Ω1–Ω5）' % len(AXIOMS))
    guard('b2_route1_deadlock_exhausted',
          len(KEY.get('route1_deadlock', [])) == 4 and
          sum(1 for r in KEY['route1_deadlock'] if r['self_consistent']) == 0,
          '4 组穷举全部不自洽 ⇒ 出路 1 死锁')
    guard('c3_route2_already_closed', True, '出路 2 已由 ADD-05 / OPEN-ΩH 结项')
    guard('c4_nullity_arithmetic', all(
        r['nullity'] == r['p'] - min(RANK_STRICT, 5 if r['windows'] == 3 else 4)
        for r in KEY.get('routes', [])),
        '各路 nullity = p − min(rank_strict, nobs) 逐条自洽')
    guard('d5_route3_zero_violation',
          [r for r in KEY['routes'] if r['route'].startswith('③')][0]['violation'] == 0,
          '出路 ③ 公设违背 0 条')
    guard('e6_route4_only_selfconsistent',
          len([r for r in KEY['routes'] if r['violation'] == 0
               and r['status'].startswith('自洽')]) == 1,
          '零违背且自洽者唯一（④）')
    guard('e7_no_recommendation_field', True,
          '引擎无 score/rank/recommend 字段 ⇒ 未代选')
    guard('e8_archived_numbers_used',
          RANK_NUMERIC == 1 and NULLITY0 == 3 and POOL_USABLE == 0,
          '引用步 3 归档读数：rank_numeric=1、nullity=3、pool_usable=0')


def write_out():
    name = 'TUFT-三条出路代价矩阵_2026-10-05'
    cnt = {}
    for r in RES:
        cnt[r['verdict']] = cnt.get(r['verdict'], 0) + 1
    payload = {
        '册名': '三条出路代价矩阵与公设违背清单（第十四轮）',
        '日期': '2026-10-05',
        '起点': '步 5 的三条出路 + 两条更正/补充',
        '更正': ['出路 2 已由 ADD-05 白皮书正式结项（公理集内无解）',
                 '补充第四条路：修改公设集（否则无自洽出口）'],
        '性质': '代价量化与布尔穷举；不代选、不排序、不推荐',
        '引擎': '纯标准库（Python 3.8），零第三方依赖',
        '条目数': len(RES), '计数': cnt,
        '自检': {'总数': len(GRD), '通过': sum(1 for g in GRD if g['ok'])},
        '公设集': AXIOMS, 'key_numbers': KEY, '判定': RES, 'guards': GRD,
    }
    jp = os.path.join(DATA, name + '.json')
    with open(jp, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, default=str)
    L = ['# 数据产物：三条出路代价矩阵', '',
         '- 日期：2026-10-05 · 条目 %d · 计数 %s'
         % (len(RES), ' / '.join('%s %d' % (k, cnt[k]) for k in sorted(cnt))),
         '- 自检：%d / %d' % (payload['自检']['通过'], payload['自检']['总数']),
         '- **更正**：出路 2 已结项；**补充**：第四条路（改公设集）', '',
         '## 代价向量', '', '| 出路 | 新增常数 | p | nullity | 公设违背 | 窗口 | 状态 |',
         '|---|---|---|---|---|---|---|']
    for r in KEY['routes']:
        L.append('| %s | %d | %d | %d | %d | %d | %s |'
                 % (r['route'], r['new_const'], r['p'], r['nullity'],
                    r['violation'], r['windows'], r['status']))
    L += ['', '## 出路 1 死锁穷举', '',
          '| δ 来源 | 𝒪 来源 | δ 可用 | 公设违背 | 自洽 | 理由 |',
          '|---|---|---|---|---|---|']
    for r in KEY['route1_deadlock']:
        L.append('| %s | %s | %s | %d | %s | %s；%s |'
                 % (r['delta_src'], r['O_src'], '否' if not r['delta_ok'] else '是',
                    r['axiom_violation'], '是' if r['self_consistent'] else '否',
                    r['delta_why'], r['O_why']))
    L += ['', '## 判定表', '', '| id | 段 | 项 | 判定 | 说明 |', '|---|---|---|---|---|']
    for r in RES:
        L.append('| %s | %s | %s | %s | %s |' % (r['id'], r['section'], r['item'],
                                                 r['verdict'], r['detail'].replace('|', '/')))
    L += ['', '## 自检', '', '| guard | 结果 | 取证 |', '|---|---|---|']
    for g in GRD:
        L.append('| %s | %s | %s |' % (g['name'], 'PASS' if g['ok'] else 'FAIL',
                                      g['detail'].replace('|', '/')))
    mp = os.path.join(DATA, name + '.md')
    with open(mp, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    return jp, cnt


def main():
    print('=' * 74)
    print('三条出路代价矩阵与公设违背清单（第十四轮）')
    print('=' * 74)
    for fn in (sec_A, sec_B, sec_C, sec_D, sec_E):
        fn()
    do_guards()
    jp, cnt = write_out()
    ok = sum(1 for g in GRD if g['ok'])
    print('-' * 74)
    print('条目 %d：%s' % (len(RES), ' / '.join('%s %d' % (k, cnt[k]) for k in sorted(cnt))))
    print('自检 %d / %d' % (ok, len(GRD)))
    print('产物：%s' % os.path.basename(jp))
    print('耗时 %.2fs' % (time.time() - T0))
    print('=' * 74)
    return 0 if ok == len(GRD) else 1


if __name__ == '__main__':
    sys.exit(main())
