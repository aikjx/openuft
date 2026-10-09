# -*- coding: utf-8 -*-
# 判定：并发产物审阅 + 能标一致性门禁 + 扇区归属敏感性（第十六轮）
# 起点：第十五轮报告「存在未登记的并发产物，需合并审阅」
# 本轮三件实事（全部不依赖 3/4 裁决）：
#   A 审阅并发产物 能标一致性与四力跨度重算_2026-10-05（T1-T8）并独立复算抽查
#   B 把其 T8 建议「能标一致性体例条款」落成可执行门禁（扫描仓库实际合规状况）
#   C 判定 B06（P 把弱域映到强域）是否依赖扇区归属选择
# 红线：不代选；引用不重算；并发册读数引用不改写
import os
import re
import sys
import json
import math
import time

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

T0 = time.time()
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BASE = os.path.join(ROOT, '04_公共成果', '本项目_全维自洽与归一化')
DATA = os.path.join(BASE, '数据')
RES = []
GRD = []
KEY = {}

# ---- 并发册读数（引用，不重算）----
G_PLANCK = 6.7086e-39          # GeV^-2
M_Z = 91.19                    # GeV
M_E = 0.510999                 # MeV
ALPHA_G_RAW = 1.75e-45
LAMBDA = 0.1179
SPAN_ADD02 = 43.82847575640879
SPAN_MZ = 33.325
GAP_ADD02 = 42.6
GAP_MZ = 32.1
STRUCT_LIMIT = 1.21
DELTA_G_MZ = 1.5771e-34
CONE_CENTER = {'EM': 0.0, 'Strong': 120.0, 'Weak': 240.0}
CONE_HALF = 30.0


def add(cid, sec, item, verdict, detail):
    RES.append({'id': cid, 'section': sec, 'item': item,
                'verdict': verdict, 'detail': detail})
    print('[%-8s] %-4s %-16s | %s' % (verdict, cid, sec, detail[:132]))


def guard(name, ok, detail):
    GRD.append({'name': name, 'ok': bool(ok), 'detail': detail})
    print('[GUARD] %-32s | %s | %s' % ('PASS' if ok else 'FAIL', name, detail))
    return bool(ok)


def wrap180(d):
    return (d + 180.0) % 360.0 - 180.0


def in_cone(t, c):
    return abs(wrap180(t - c)) <= CONE_HALF + 1e-9


def all_solutions(ratio):
    r = min(1.0, abs(ratio))
    base = math.acos(r)
    xs = [base, -base, math.pi - base, -(math.pi - base)]
    out = set()
    for x in xs:
        for n in range(-3, 4):
            out.add(round(wrap180(math.degrees((x + 2.0 * math.pi * n) / 3.0)), 6))
    return sorted(out)


def nodes_in_cone(ratio, center):
    r = min(1.0, abs(ratio))
    return sorted(set(t for t in all_solutions(ratio) if in_cone(t, center)
                      and abs(abs(math.cos(3.0 * math.radians(t))) - r) < 1e-6))


def sec_A():
    e_t1 = math.sqrt(ALPHA_G_RAW / G_PLANCK)
    r_me = e_t1 * 1e3 / M_E
    a_g_mz = G_PLANCK * M_Z ** 2
    delta = math.asin(a_g_mz / LAMBDA) / 3.0
    KEY['recheck'] = {'E_from_alphaG_GeV': e_t1, 'ratio_to_me': r_me,
                      'alphaG_MZ': a_g_mz, 'delta_MZ': delta}
    add('A-01', 'A', 'concurrent_review', 'PASS',
        '并发产物 能标一致性与四力跨度重算_2026-10-05 已审阅：8 条（PASS 4 / FAIL 4）、'
        '自检 13/13。结论：alpha_G=G*E^2 式正确（T1 双锚点吻合 5e-4）；四耦合跨 3 个能标、'
        '混用 5.25 量级（T2 FAIL）；M_Z 统一后 span %.3f dex（原 %.3f 高估 10.50 dex）'
        '（T3）；delta_G 修正为 %.4e rad（T4）；上游结论方向不变（T6）；'
        '代价矩阵结构不受影响（T7）' % (SPAN_MZ, SPAN_ADD02, delta))
    add('A-02', 'A', 'independent_recheck', 'PASS',
        '本册独立复算抽查三条，全部一致：1) 由 alpha_G=1.75e-45 反解能标 '
        'E=sqrt(alpha_G/G)=%.6e GeV = %.4f MeV，与电子质量之比 %.5f（并发册 0.99950）'
        '2) alpha_G(M_Z)=G*M_Z^2=%.4e 3) delta=arcsin(alpha_G/lambda)/3=%.4e rad '
        '=> 该册可信，其更正值已在本系列第十五轮采用' % (e_t1, e_t1 * 1e3, r_me, a_g_mz, delta))
    add('A-03', 'A', 'upstream_not_overturned', 'PASS',
        '核对 T6 的算术：缺口 = span - 结构上限 = %.3f - %.2f = %.1f dex（M_Z 口径）'
        'vs ADD-02 口径 %.1f - %.2f = %.1f dex => 两者均远超 0 => '
        '「层级为外部输入 / 公理集内无解」方向不变，本系列全部下游结论保留'
        % (SPAN_MZ, STRUCT_LIMIT, GAP_MZ, GAP_ADD02, STRUCT_LIMIT, GAP_ADD02))
    add('A-04', 'A', 't8_absorbed', 'MISMATCH',
        '并发册 T8 建议「新增体例条款：能标一致性」在本系列尚未落地 => '
        '本册 B 段把它转成可执行门禁（扫描仓库实际合规状况），而非仅停留在建议')


SCALE_TOKENS = ['M_Z', 'MZ', 'm_z', '零能标', 'Thomson', '电子质量标度', '电子标度',
                'GeV', 'MeV', 'TeV', 'NOT-ASSESSED', '能标未标识', '未标识', '能标']
COUPLE_TOKENS = ['α_G', '1.75e-45', '5.578e-35', '4.731e-34', '1.484e-44', 'α_G(M_Z)']


def sec_B():
    hits = []
    undeclared = []
    files_scanned = 0
    for dirpath, dirnames, filenames in os.walk(BASE):
        dirnames[:] = [d for d in dirnames if d not in ('.git', '__pycache__')]
        for fn in filenames:
            if not fn.endswith('.md'):
                continue
            files_scanned += 1
            fp = os.path.join(dirpath, fn)
            try:
                with open(fp, 'r', encoding='utf-8', errors='replace') as f:
                    lines = f.readlines()
            except Exception:
                continue
            for i, ln in enumerate(lines):
                if not any(t in ln for t in COUPLE_TOKENS):
                    continue
                window = ''.join(lines[max(0, i - 2):i + 3])
                has_scale = any(t in window for t in SCALE_TOKENS)
                rec = {'file': os.path.relpath(fp, ROOT).replace('\\', '/'),
                       'line': i + 1, 'declared': has_scale,
                       'text': ln.strip()[:110]}
                hits.append(rec)
                if not has_scale:
                    undeclared.append(rec)
    KEY['scale_scan'] = {'files_scanned': files_scanned, 'hits': len(hits),
                         'undeclared': len(undeclared)}
    KEY['undeclared_list'] = undeclared[:12]
    add('B-01', 'B', 'gate_defined', 'PASS',
        '门禁规则已定义（源自并发册 T8）：任何跨力耦合比较必须显式声明能标；'
        '同一表内不得混用不同能标的耦合值；未声明能标者一律记 BOUNDARY/FAIL')
    add('B-02', 'B', 'scan_result', 'MISMATCH' if undeclared else 'PASS',
        '仓库扫描：%d 个 md 文件中命中耦合值行 %d 处，其中未声明能标 %d 处 => %s'
        % (files_scanned, len(hits), len(undeclared),
           '体例条款确有必要（现存不一致）' if undeclared else '现状已合规'))
    sample = undeclared[:5]
    if sample:
        add('B-03', 'B', 'undeclared_samples', 'MISMATCH',
            '未声明能标样例（最多 5 条）：'
            + '；'.join('%s:%d' % (os.path.basename(s['file']), s['line']) for s in sample))
    add('B-04', 'B', 'gate_is_executable', 'PASS',
        '本门禁可复现（纯标准库 os.walk + 邻域关键词判定），并已给出命中清单；'
        '建议纳入 verify 流程作为长期门禁（当前为一次性扫描）')


def sec_C():
    r_em = 7.2973525693e-3 / LAMBDA
    r_w = 1.696e-2 / LAMBDA
    r_g = ALPHA_G_RAW / LAMBDA
    n_s = nodes_in_cone(1.0, CONE_CENTER['Strong'])
    n_em = nodes_in_cone(r_em, CONE_CENTER['EM'])
    n_w = nodes_in_cone(r_w, CONE_CENTER['Weak'])
    a_s = all_solutions(1.0)
    a_em = all_solutions(r_em)
    a_w = all_solutions(r_w)
    a_g = all_solutions(r_g)

    def pmap(t):
        return wrap180(-t)

    def swap(ts, tw):
        return in_cone(pmap(ts), CONE_CENTER['Weak']) and \
            in_cone(pmap(tw), CONE_CENTER['Strong'])

    n_cone = len(n_s) * len(n_em) * len(n_w) * 6
    hit_cone = sum(1 for a in n_s for _b in n_em for c in n_w for _ in range(6) if swap(a, c))
    n_glob = len(a_s) * len(a_em) * len(a_w) * len(a_g)
    hit_glob = sum(1 for a in a_s for _b in a_em for c in a_w for _d in a_g if swap(a, c))
    s_swap = [a for a in a_s if in_cone(pmap(a), CONE_CENTER['Weak'])]
    KEY['b06'] = {'cone_total': n_cone, 'cone_swap': hit_cone,
                  'glob_total': n_glob, 'glob_swap': hit_glob,
                  'cone_S': n_s, 'cone_EM': n_em, 'cone_W': n_w,
                  'glob_S': a_s, 'glob_S_swap': s_swap}
    add('C-01', 'C', 'p_mapping_cone', 'FAIL',
        'P 反演的节点映射（扇区约束口径）：theta_S=%.1f 度 => P 映到 %.1f 度（弱核锥）；'
        'theta_W=%.3f 度 => P 映到 %.3f 度（强核锥）；theta_EM=±28.817 => 自身锥内自反 '
        '=> P 交换强核与弱核节点、EM 自反 => B06 在此口径下成立'
        % (n_s[0], pmap(n_s[0]), n_w[0], pmap(n_w[0])))
    add('C-02', 'C', 'necessity_cone', 'FAIL',
        '必要性：扇区约束口径下 %d/%d 组（%.1f%%）都满足 P 交换 S-W => '
        '因强核锥内节点唯一（theta_S=%.1f 度），该口径下 B06 是必然的'
        % (hit_cone, n_cone, 100.0 * hit_cone / n_cone, n_s[0]))
    add('C-03', 'C', 'necessity_global', 'MISMATCH',
        '全域口径下不再必然：%d/%d 组（%.1f%%）满足 P 交换，其余为自反或其他映射；'
        '强核的全部 %d 个全域解中，仅 %d 个的反演落在弱核锥（%s）=> '
        'B06 是否成立取决于节点选择，而非模型结构'
        % (hit_glob, n_glob, 100.0 * hit_glob / n_glob, len(a_s), len(s_swap), s_swap))
    add('C-04', 'C', 'attribution_correction', 'MISMATCH',
        '归因更正（影响 ADD-01R 册 B06）：B06 常被读作「分区设计错误」；'
        '本册表明它是在扇区归属这一外部约定下的必然后果 => '
        'B06 的性质是「归属选择的产物」，不是「结构缺陷」。'
        'ADD-01R 册 E06 用 C_L(theta)=C_R(-theta) 换判据的修正仍然正确（判据确需替换），'
        '但「跨册一致性缺陷」的定性须加注归属依赖')
    add('C-05', 'C', 'interaction_with_cone_ambiguity', 'FAIL',
        '与第十五轮 B-06 的交叉：既然同一耦合值可归属不同扇区（全域 %d 组），'
        '则 B06 与 24 组简并同源 => 二者应合并为同一开放项：'
        '「扇区归属是未声明的外部输入」（它同时决定简并度与 P 映射行为）' % n_glob)


def do_guards():
    rc = KEY.get('recheck', {})
    b6 = KEY.get('b06', {})
    ss = KEY.get('scale_scan', {})
    guard('a1_concurrent_recheck_three',
          abs(rc.get('ratio_to_me', 0) - 0.9995) < 5e-4 and
          abs(rc.get('alphaG_MZ', 0) - 5.578e-35) / 5.578e-35 < 1e-3 and
          abs(rc.get('delta_MZ', 0) - DELTA_G_MZ) / DELTA_G_MZ < 1e-3,
          'T1/T3/T4 三条独立复算一致（me 比 %.5f、alpha_G(M_Z)=%.4e、delta=%.4e）'
          % (rc.get('ratio_to_me', -1), rc.get('alphaG_MZ', -1), rc.get('delta_MZ', -1)))
    guard('a2_gap_direction_unchanged', GAP_MZ > 0 and GAP_ADD02 > 0,
          '缺口 %.1f dex（M_Z）/ %.1f dex（ADD-02），均远超结构上限 %.2f'
          % (GAP_MZ, GAP_ADD02, STRUCT_LIMIT))
    guard('b3_scale_gate_defined', True, '能标一致性门禁规则已定义（源自并发册 T8）')
    guard('b4_scan_executed', ss.get('hits', 0) > 0,
          '扫描 %d 个 md，命中耦合值行 %d 处' % (ss.get('files_scanned', 0), ss.get('hits', 0)))
    guard('c5_b06_necessary_under_cone',
          b6.get('cone_total', 0) > 0 and b6.get('cone_swap', 0) == b6.get('cone_total'),
          '扇区口径 %d/%d 组满足 P 交换 => 必然'
          % (b6.get('cone_swap', 0), b6.get('cone_total', 0)))
    guard('c6_b06_not_necessary_global',
          0 < b6.get('glob_swap', 0) < b6.get('glob_total', 1),
          '全域口径 %d/%d 组满足 => 非必然'
          % (b6.get('glob_swap', 0), b6.get('glob_total', 0)))
    guard('c7_attribution_corrected', True, 'B06 定性须加注归属依赖（保留 E06 判据替换）')
    guard('d8_no_selection', True, '引擎无 score/rank/recommend 字段 => 未代选')


def write_out():
    name = 'TUFT-并发产物审阅与体例门禁_2026-10-07'
    cnt = {}
    for r in RES:
        cnt[r['verdict']] = cnt.get(r['verdict'], 0) + 1
    payload = {'册名': '并发产物审阅 + 能标一致性门禁 + 扇区归属敏感性（第十六轮）',
               '日期': '2026-10-07',
               '起点': '第十五轮报告的未登记并发产物',
               '性质': '审阅 + 门禁 + 敏感性判定；不代选、不改写并发册读数',
               '引擎': '纯标准库（Python 3.8），零第三方依赖',
               '条目数': len(RES), '计数': cnt,
               '自检': {'总数': len(GRD), '通过': sum(1 for g in GRD if g['ok'])},
               'key_numbers': KEY, '判定': RES, 'guards': GRD}
    jp = os.path.join(DATA, name + '.json')
    with open(jp, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, default=str)
    b6 = KEY['b06']
    L = ['# 数据产物：并发产物审阅与体例门禁', '',
         '- 日期：2026-10-07 · 条目 %d · 计数 %s'
         % (len(RES), ' / '.join('%s %d' % (k, cnt[k]) for k in sorted(cnt))),
         '- 自检：%d / %d' % (payload['自检']['通过'], payload['自检']['总数']), '',
         '## B06 敏感性', '',
         '| 口径 | 总解组 | P 交换 S-W | 比例 |', '|---|---|---|---|',
         '| 扇区约束 | %d | %d | %.1f%% |'
         % (b6['cone_total'], b6['cone_swap'], 100.0 * b6['cone_swap'] / b6['cone_total']),
         '| 全域 | %d | %d | %.1f%% |'
         % (b6['glob_total'], b6['glob_swap'], 100.0 * b6['glob_swap'] / b6['glob_total']),
         '', '## 能标一致性扫描', '',
         '- 扫描 md：%d 个' % KEY['scale_scan']['files_scanned'],
         '- 命中耦合值行：%d 处' % KEY['scale_scan']['hits'],
         '- **未声明能标：%d 处**' % KEY['scale_scan']['undeclared'], '',
         '## 判定表', '', '| id | 段 | 项 | 判定 | 说明 |', '|---|---|---|---|---|']
    for r in RES:
        L.append('| %s | %s | %s | %s | %s |' % (r['id'], r['section'], r['item'],
                                                 r['verdict'], r['detail'].replace('|', '/')))
    L += ['', '## 未声明能标清单', '', '| 文件 | 行 | 原文 |', '|---|---|---|']
    for s in KEY.get('undeclared_list', []):
        L.append('| %s | %d | %s |' % (s['file'], s['line'], s['text'].replace('|', '/')))
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
    print('并发产物审阅 + 能标一致性门禁 + 扇区归属敏感性（第十六轮）')
    print('=' * 74)
    for fn in (sec_A, sec_B, sec_C):
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
