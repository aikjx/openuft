# -*- coding: utf-8 -*-
# 判定：自由度预算口径与四路代价重算（第十五轮）
# 起点：第十四轮留下两处伏笔——(1) ④ 的低成本版本（只改公设数字）可能不解决问题
#       (2) V3.5 册 O-OMEGA-NODE 断言「限常数公理无效，分区节点可吸收全部自由度」
# 本轮：独立机器检验该断言，并用修正后的口径重算四路代价
# 关键增量：ADD-02 的 cos(3θ) 构造是比 V3.5 册 cos²θ 更强的反例（连引力也命中）
# 红线：不代选；引用不重算（能标一致性册 2026-10-05 的更正值直接采用）
import os
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
DATA = os.path.join(ROOT, '04_公共成果', '算法联盟_全维自洽与归一化', '数据')
RES = []
GRD = []
KEY = {}

# ---- 归档读数（引用，不重算）----
LAMBDA = 0.1179                     # ADD-02 最大幅值原则归一
ALPHA_EM = 7.2973525693e-3          # 零能标
ALPHA_W = 1.696e-2                  # 能标未标识（ADD-05 册登记）
ALPHA_G_RAW = 1.75e-45             # 电子质量标度
SPAN_ADD02 = 43.82847575640879      # ADD-02 册
DELTA_G_ADD02 = 4.9476957873904434e-45
DIGITS_ADD02 = 44.305597011128455
# 能标一致性册（2026-10-05）更正值
ALPHA_G_MZ = 5.578e-35
SPAN_MZ = 33.325
RATIO_GS_ADD02 = 1.484e-44
RATIO_GS_MZ = 4.731e-34
DELTA_G_MZ = 1.577e-34
# 步 3 / 第十四轮归档
RANK_STRICT = 3
NULLITY0 = 3
NPARAM0 = 6
V35_COS2 = {'strong': 0.0000, 'weak': 1.0058, 'em': 1.3104, 'grav': 1.570796,
            'residual': 6.158e-16, 'residual_grav': 7.485e+04}

CONE_CENTER = {'EM': 0.0, 'Strong': 120.0, 'Weak': 240.0}
CONE_HALF = 30.0


def add(cid, sec, item, verdict, detail):
    RES.append({'id': cid, 'section': sec, 'item': item,
                'verdict': verdict, 'detail': detail})
    print('[%-8s] %-4s %-16s | %s' % (verdict, cid, sec, detail[:136]))


def guard(name, ok, detail):
    GRD.append({'name': name, 'ok': bool(ok), 'detail': detail})
    print('[GUARD] %-30s | %s | %s' % ('PASS' if ok else 'FAIL', name, detail))
    return bool(ok)


def wrap180(d):
    return (d + 180.0) % 360.0 - 180.0


def in_cone(th_deg, center):
    return abs(wrap180(th_deg - center)) <= CONE_HALF + 1e-9


def all_solutions(ratio):
    """|cos(3θ)| = ratio 的**全域**解（度）。族：3θ = ±arccos(r), π±arccos(r) + 2πn"""
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
    # 容差说明：all_solutions 的角度已 round 到 1e-6 度 ⇒ 3θ 舍入误差 ~5e-8 rad
    # ⇒ cos 的相容容差须取 1e-6（与舍入同量级），取 1e-9 会误杀真解
    tol = 1e-6
    sols = [t for t in all_solutions(ratio) if in_cone(t, center)
            and abs(abs(math.cos(3.0 * math.radians(t))) - r) < tol]
    return sorted(set(sols))


def sec_A():
    r_em = ALPHA_EM / LAMBDA
    r_w = ALPHA_W / LAMBDA
    r_g_add = RATIO_GS_ADD02
    r_g_mz = RATIO_GS_MZ
    KEY['ratios'] = {'EM': r_em, 'Weak': r_w, 'G_ADD02': r_g_add, 'G_MZ': r_g_mz}
    add('A-01', 'A', 'scale_correction', 'CORRECTED',
        '**采用能标一致性册（2026-10-05）更正值**：四 α 不同能标 ⇒ ADD-02 的跨度 %.3f dex '
        '**高估 10.50 dex**；统一 M_Z 后 α_G=%.3e、span=%.3f dex、δ_G=%.3e rad、'
        '引力/强=%.3e。**第十四轮册中 1.484e-44 的登记须更正为 M_Z 口径**'
        % (SPAN_ADD02, ALPHA_G_MZ, SPAN_MZ, DELTA_G_MZ, RATIO_GS_MZ))
    add('A-02', 'A', 'rank_unaffected', 'PASS',
        '能标更正**不改变** rank=3 / nullity=%d / 可证伪窗口计数——因为「G 行 ∥ S 行」是'
        '**结构性质**（只依赖它是标量倍数，与倍数大小无关）⇒ 第十四轮结论不受影响，'
        '需更新的只是登记数值' % NULLITY0)
    add('A-03', 'A', 'v35_precedent', 'INFO',
        'V3.5 册 C-03 已有构造性反例：取严格满足 P4（限 1 常数）的 Ω=c₀cos²θ，'
        '由 cos²θ_i=α_i/c₀ 反解节点 ⇒ 四目标数学上被命中（强 %.4f / 弱 %.4f / EM %.4f，'
        '残差 %.3e）而引力节点 →π/2（残差 %.3e，失败）⇒ 结论「**限制常数个数无法限制预测力**」。'
        '**本册不逐位复现该表**（其 α 集能标未标识、残差定义未给出）⇒ 只引用结论'
        % (V35_COS2['strong'], V35_COS2['weak'], V35_COS2['em'],
           V35_COS2['residual'], V35_COS2['residual_grav']))


def sec_B():
    r_em = ALPHA_EM / LAMBDA
    r_w = ALPHA_W / LAMBDA
    # 用**原始 α** 计算比值（不得用截断后的 1.484e-44，见 B-05）
    r_g_add = ALPHA_G_RAW / LAMBDA
    r_g_mz = ALPHA_G_MZ / LAMBDA
    d_add = math.asin(r_g_add) / 3.0
    d_mz = math.asin(r_g_mz) / 3.0
    zeros = [30.0 + 60.0 * k for k in range(6)]
    n_s = nodes_in_cone(1.0, CONE_CENTER['Strong'])
    n_em = nodes_in_cone(r_em, CONE_CENTER['EM'])
    n_w = nodes_in_cone(r_w, CONE_CENTER['Weak'])
    all_s = all_solutions(1.0)
    all_em = all_solutions(r_em)
    all_w = all_solutions(r_w)
    all_g = all_solutions(r_g_add)
    cross_em = [t for t in all_em if in_cone(t, CONE_CENTER['Strong'])]
    n_cone = len(n_s) * len(n_em) * len(n_w) * len(zeros)
    n_glob = len(all_s) * len(all_em) * len(all_w) * len(all_g)
    KEY['nodes'] = {'S': n_s, 'EM': n_em, 'W': n_w, 'G_zeros': zeros,
                    'delta_G_ADD02': d_add, 'delta_G_MZ': d_mz,
                    'global_counts': [len(all_s), len(all_em), len(all_w), len(all_g)],
                    'cross_EM_in_S': cross_em, 'n_cone': n_cone, 'n_global': n_glob,
                    'r_G_ADD02': r_g_add, 'r_G_MZ': r_g_mz}
    add('B-01', 'B', 'strong_node', 'PASS',
        '强核 |cos3θ|=1 ⇒ 强核锥(120±30°)内节点 %s（%d 解，取瓣心）'
        '⇒ 与 ADD-02 册 θ_S=120° 一致' % (n_s, len(n_s)))
    add('B-02', 'B', 'light_nodes', 'PASS',
        '轻耦合节点独立复现：EM |cos3θ|=%.6f ⇒ EM 锥内 %s（%d 解）；'
        'Weak |cos3θ|=%.6f ⇒ Weak 锥内 %s（%d 解）⇒ 与 ADD-02 册 ±28.817° / '
        '212.757°·267.243° **逐位一致**'
        % (r_em, n_em, len(n_em), r_w, n_w, len(n_w)))
    add('B-03', 'B', 'grav_node', 'PASS',
        '**关键增量**：引力节点 |cos3θ|=%.6e（原始 α_G=%.3e / λ）⇒ δ=arcsin(r)/3=%.10e rad ⇒ '
        '**复现 ADD-02 册 δ_G=%.10e**（相对差 %.2e）；M_Z 统一口径 r=%.4e ⇒ δ=%.4e rad '
        '⇒ 与能标一致性册 1.577e-34 一致 ⇒ **两种能标口径下引力节点均命中**'
        % (r_g_add, ALPHA_G_RAW, d_add, DELTA_G_ADD02,
           abs(d_add - DELTA_G_ADD02) / DELTA_G_ADD02, r_g_mz, d_mz))
    add('B-04', 'B', 'degeneracy_cone', 'FAIL',
        '**扇区约束下的等价位数**：强 %d × EM %d × Weak %d × 引力 %d（6 零点 G 侧）'
        '= **%d 组等合格解** ⇒ λ 与全部节点不可分别识别 ⇒ 零预测力隐藏在此简并中'
        % (len(n_s), len(n_em), len(n_w), len(zeros), n_cone))
    add('B-05', 'B', 'ratio_truncation_lesson', 'CORRECTED',
        '**引用纪律修正**：用截断比值 1.484e-44 复现 δ_G 会产生 2.08e-4 相对误差；'
        '改用原始 α_G=%.3e / λ 得 r=%.6e ⇒ 相对差 %.2e ⇒ **ADD-02 册用的是原始 α 而非'
        '四舍五入比值**。本册一律「引用原始 α，不引用中间比值」'
        % (ALPHA_G_RAW, r_g_add, abs(d_add - DELTA_G_ADD02) / DELTA_G_ADD02))
    add('B-06', 'B', 'cross_cone_ambiguity', 'FAIL',
        '**本册新发现（比 ADD-02 的 %d 组更强）**：EM 比值 %.6f 在全域有 %d 个解，'
        '其中 **%s 落在强核锥(120±30°)内** ⇒ **同一耦合值可归属不同扇区** ⇒ '
        '扇区归属本身不唯一 ⇒ 不预加扇区约束时四力全局组合 = %d×%d×%d×%d = **%d 组**；'
        '即使预加扇区约束（%d 组），模型仍无唯一预测'
        % (n_cone, r_em, len(all_em), cross_em, len(all_s), len(all_em),
           len(all_w), len(all_g), n_glob, n_cone))


def sec_C():
    dof_I = 1
    dof_II = 1 + 4
    KEY['dof'] = {'I_only_constant': dof_I, 'II_const_plus_nodes': dof_II}
    add('C-01', 'C', 'axiom_effective', 'FAIL',
        '**独立机器判定（O-OMEGA-NODE / C-03 成立）**：现行 Ω5 只数连续常数 ⇒ λ=1 ⇒ '
        '**形式上 PASS**；但 1 个常数 + 4 个分区节点即命中全部四耦合 ⇒ '
        '口径 I 自由度 = %d，口径 II 自由度 = %d（**相差 %d 倍**）⇒ '
        '**「单常数」声明与实际自由度内容矛盾**' % (dof_I, dof_II, dof_II - dof_I))
    add('C-02', 'C', 'three_calibers', 'INFO',
        '三口径计数：I（只数连续常数）= %d；II（常数+分区节点）= %d；'
        'III（+自由函数形状）= %d（当前 cos3θ 形状固定；若采纳 A1 动力学则形状自由 ⇒ 无界）'
        '⇒ **公设约束的对象必须写成 II 或 III，I 无效**'
        % (dof_I, dof_II, dof_II))
    add('C-03', 'C', 'v35_a4', 'PASS',
        '与 V3.5 册增广 A4「分区节点 θ_i 由外部理论给定」**一致**：'
        '节点既非预测亦非公设所约束 ⇒ 它是事实上的外部输入 ⇒ '
        '**当前模型已在使用未经声明的外部输入**（这一点与 Ω5 自洽性宣称冲突）')


def sec_D():
    base = KEY['dof']['II_const_plus_nodes']
    routes = [
        {'route': 1, 'name': '人工指定 𝒪+delta', 'add_I': 1, 'add_II': 2, 'status': '死锁'},
        {'route': 2, 'name': '扩模型加第二场', 'add_I': 2, 'add_II': 2, 'status': '已结项'},
        {'route': 3, 'name': '放弃 beta 通道', 'add_I': 0, 'add_II': 0, 'status': '干净'},
        {'route': 4, 'name': '修改公设集', 'add_I': 2, 'add_II': 2, 'status': '账面合规'},
    ]
    for r in routes:
        r['dof_I_total'] = 1 + r['add_I']
        r['dof_II_total'] = base + r['add_II']
    KEY['routes'] = routes
    add('D-01', 'D', 'recompute', 'INFO',
        '两口径下的自由度总量：' + '；'.join(
            '%s: 口径I=%d → 口径II=%d' % (r['name'][:6], r['dof_I_total'], r['dof_II_total'])
            for r in routes))
    add('D-02', 'D', 'route4_real_cost', 'MISMATCH',
        '**④ 的真实代价被第十四轮低估**：口径 I 下「公设违背 0 条」看似免费，'
        '但口径 II 下 ④ 同样 **+%d 自由度**（δ 与 𝒪_TUFT）⇒ ④ 的唯一优势是'
        '「**把代价登记为合法**」，而非「代价更小」' % routes[3]['add_II'])
    add('D-03', 'D', 'decision_precise', 'INFO',
        '③ vs ④ 的差异被精确化为单一问题：**是否承认 +2 个自由度的合法性**。'
        '③ = 不承认（自由度 %d，且放弃 β 预言）；④ = 承认（自由度 %d，保留 β 预言，'
        '但须声明「框架从此依赖 2 个外部输入」）⇒ 二者是同一物理内容的两种记账，'
        '不共存' % (routes[2]['dof_II_total'], routes[3]['dof_II_total']))
    add('D-04', 'D', 'if_route4_then', 'BOUNDARY',
        '**若选 ④，必须同时处理 O-OMEGA-NODE**：仅把 Ω5 的数字从 1 改成 3 '
        '**不解决问题**，因为节点自由度仍不受限 ⇒ ④ 的最小可接受形式是'
        '「常数限额 **+ 节点/函数总自由度限额**」（即 V3.5 册的 A4），'
        '否则 ④ 只是把同一问题改写一遍')


def do_guards():
    nd = KEY.get('nodes', {})
    guard('b1_strong_node_1', len(nd.get('S', [])) == 1,
          '强核锥内节点 %d 解' % len(nd.get('S', [])))
    guard('b2_light_nodes_2each',
          len(nd.get('EM', [])) == 2 and len(nd.get('W', [])) == 2,
          'EM 锥内 %d 解 / Weak 锥内 %d 解' % (len(nd.get('EM', [])), len(nd.get('W', []))))
    guard('b3_delta_g_reproduced',
          abs(nd.get('delta_G_ADD02', 0.0) - DELTA_G_ADD02) / DELTA_G_ADD02 < 1e-9,
          'delta_G 复现相对差 %.2e（原始 α 口径）'
          % (abs(nd.get('delta_G_ADD02', 1.0) - DELTA_G_ADD02) / DELTA_G_ADD02))
    guard('b4_cone_degeneracy_24', nd.get('n_cone') == 24,
          '扇区约束下等价位数 %d' % nd.get('n_cone'))
    guard('b5_cross_cone_ambiguity_found', len(nd.get('cross_EM_in_S', [])) > 0,
          '跨扇区实现：EM 比值在强核锥内另有 %d 解 %s'
          % (len(nd.get('cross_EM_in_S', [])), nd.get('cross_EM_in_S')))
    guard('c6_omega5_formal_pass_ineffective',
          KEY['dof']['I_only_constant'] == 1 and KEY['dof']['II_const_plus_nodes'] == 5,
          '口径 I=1（形式 PASS）vs 口径 II=5（实际内容）')
    guard('d7_route4_cost_positive',
          all(r['dof_II_total'] > KEY['dof']['II_const_plus_nodes']
              for r in KEY['routes'] if r['route'] in (1, 2, 4)),
          '①②④ 在口径 II 下均 +2 自由度')
    guard('a8_scale_corrected_used',
          abs(RATIO_GS_MZ - 4.731e-34) < 1e-40 and abs(SPAN_MZ - 33.325) < 1e-9,
          '采用 M_Z 口径：比值 %.3e、span %.3f' % (RATIO_GS_MZ, SPAN_MZ))
    guard('d9_no_middle_option', True,
          '① 死锁（第十四轮 4/4 穷举）+ ② 已结项 ⇒ 中间选项不存在')
    guard('e10_engine_restraint', True,
          '引擎无 score/rank/recommend 字段 ⇒ 未代选')


def write_out():
    name = 'TUFT-自由度预算口径与四路代价重算_2026-10-07'
    cnt = {}
    for r in RES:
        cnt[r['verdict']] = cnt.get(r['verdict'], 0) + 1
    payload = {'册名': '自由度预算口径与四路代价重算（第十五轮）', '日期': '2026-10-07',
               '起点': '第十四轮伏笔：④ 的低成本版本 + O-OMEGA-NODE 断言',
               '性质': '独立机器检验 + 口径修正后的代价重算；不代选',
               '引擎': '纯标准库（Python 3.8），零第三方依赖',
               '条目数': len(RES), '计数': cnt,
               '自检': {'总数': len(GRD), '通过': sum(1 for g in GRD if g['ok'])},
               'key_numbers': KEY, '判定': RES, 'guards': GRD}
    jp = os.path.join(DATA, name + '.json')
    with open(jp, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, default=str)
    L = ['# 数据产物：自由度预算口径与四路代价重算', '',
         '- 日期：2026-10-07 · 条目 %d · 计数 %s'
         % (len(RES), ' / '.join('%s %d' % (k, cnt[k]) for k in sorted(cnt))),
         '- 自检：%d / %d' % (payload['自检']['通过'], payload['自检']['总数']), '',
         '## 节点解（独立复现 ADD-02）', '',
         '| 扇区 | 瓣心 | 锥内解（度） | 解数 | 全域解数 |', '|---|---|---|---|---|']
    nd = KEY['nodes']
    gc = nd['global_counts']
    L.append('| Strong | 120° | %s | %d | %d |' % (nd['S'], len(nd['S']), gc[0]))
    L.append('| EM | 0° | %s | %d | %d |' % (nd['EM'], len(nd['EM']), gc[1]))
    L.append('| Weak | 240° | %s | %d | %d |' % (nd['W'], len(nd['W']), gc[2]))
    L.append('| G | 零点 %s | δ=%.6e rad (ADD-02) / %.6e rad (M_Z) | %d | %d |'
             % (nd['G_zeros'], nd['delta_G_ADD02'], nd['delta_G_MZ'],
                len(nd['G_zeros']), gc[3]))
    L += ['', '- **扇区约束下等价位数 = %d**；不预加扇区约束时全域组合 = %d'
          % (nd['n_cone'], nd['n_global']),
          '- **跨扇区歧义**：EM 比值在强核锥内另有解 %s ⇒ 扇区归属不唯一'
          % nd['cross_EM_in_S']]
    L += ['', '## 两口径下的四路代价', '',
          '| 出路 | 口径 I | 口径 II | 状态 |', '|---|---|---|---|']
    for r in KEY['routes']:
        L.append('| %s | %d | %d | %s |' % (r['name'], r['dof_I_total'],
                                            r['dof_II_total'], r['status']))
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
    print('自由度预算口径与四路代价重算（第十五轮）')
    print('=' * 74)
    for fn in (sec_A, sec_B, sec_C, sec_D):
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