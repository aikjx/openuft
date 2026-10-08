# -*- coding: utf-8 -*-
"""S03-V18.12  GAQ-UFT V18 中子 beta 衰变拓扑图像 -- 本体(章节 1-6)机器审计

对象: 来稿 <<GAQ-UFT V18: 中子 beta 衰变拓扑图像 | 弱相互作用作为受限场重联>>
      章节 1(中子/质子复合扭结) 2(beta 衰变四阶段) 3(守恒律校验)
           4(弱作用手性 V-A 几何起源) 5(强弱电磁区分表) 6(自评与遗留缺口)

本册定位(开工前核对):
  * 来稿章节 7 的三条分支已于 2026-10-07 全部裁定并收口
      - 分支一 色荷/禁闭   S03-V18.4  关闭
      - 分支二 中微子/马约拉纳 S03-V18.1 + V18.2 关闭
      - 分支三 CKM 拓扑起源 S03-V18.8  阻塞
    => 本册不再重复裁定分支, 只做交叉回链与收口确认.
  * 来稿章节 1-6 本体此前只有 2026-10-04 手工整理稿 S03-D1 与其 11_证伪与反例 的 A-F 六条,
    自标 [尚未经第三方复核]. 本册用机器读数把 A-F 升级/补强, 并新增本体级判据.

红线: 本册全部为可否证性判定与自洽性检验, 不含对 GAQ 的正面支持证据.
      实现验证器(标准物理事实的独立复算)明确不计入 GAQ 正面证据.

运行: python 07_计算复现/源码/S03_V18_12_beta衰变本体_场重联机器审计.py
产物: 07_计算复现/运行记录/S03_V18_12_beta衰变本体_验证报告.txt
"""
import io
import json
import math
import os
import sys
from decimal import Decimal, getcontext

getcontext().prec = 60

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))          # 01_独立体系/S03_GAQ几何原子与作用量子
OUT_TXT = os.path.join(ROOT, '07_计算复现', '运行记录', 'S03_V18_12_beta衰变本体_验证报告.txt')

# ---------------------------------------------------------------- 输出与记录
_LINES = []
_ITEMS = []
_CHECKS = []


def emit(s=''):
    _LINES.append(s)
    print(s)


def F(x, n=6):
    """定点科学计数法输出. Decimal.quantize 在高位数会抛 InvalidOperation, 故用 format."""
    try:
        return format(float(x), '.' + str(n) + 'E')
    except Exception:
        return str(x)


def D(x):
    return Decimal(str(x))


def rec(cid, level, title, detail, tag=''):
    _ITEMS.append({'id': cid, 'level': level, 'title': title,
                   'detail': detail, 'tag': tag})
    emit('[%s] %-11s %s' % (cid, level, title))
    emit('      ' + detail)


def sc(cid, desc, reading, ok):
    _CHECKS.append({'id': cid, 'desc': desc, 'reading': reading, 'ok': bool(ok)})
    emit('  %-5s %-52s %-32s %s' % (cid, desc[:52], reading[:32], 'OK' if ok else 'NG'))


# ---------------------------------------------------------------- 物理常数
# CODATA 2018 / PDG 2024 (SI 与自然单位混用处显式标注)
HBARC = Decimal('197.3269804')      # MeV fm
M_N = Decimal('939.565420')         # MeV  中子
M_P = Decimal('938.272088')         # MeV  质子
M_E = Decimal('0.510998950')        # MeV  电子
M_MU = Decimal('105.6583755')       # MeV
Q_BETA = M_N - M_P - M_E            # MeV  beta 衰变释放能

TAU_N = Decimal('879.4')            # s    PDG 中子平均寿命
HBAR_MEV_S = Decimal('6.582119569e-22')   # MeV s

# W 玻色子 (PDG 2024)
M_W = Decimal('80.3770')            # GeV
GAMMA_W = Decimal('2.085')          # GeV  总宽度

# QCD 弦张力 / 流管
SIGMA_QCD_GEV2 = Decimal('0.18')    # GeV^2  ~ 0.9 GeV/fm
GEV2_TO_GEVFM = Decimal('5.067731') # 1 GeV^2 = 5.0677 GeV/fm  (hbar=c=1: 1 fm^-1 = 0.19733 GeV)

# 中子复合体尺度 (保守取 0.8 fm; 质子电荷半径 0.84075 fm, 中子物质半径同量级)
R_N = Decimal('0.8')                # fm

# 夸克电荷
Q_U = Decimal('2') / Decimal('3')
Q_D = Decimal('-1') / Decimal('3')

# 弱作用耦合比 (中子衰变)
G_A_OVER_G_V = Decimal('-1.2756')   # PDG

# 中微子螺旋度实验 (Goldhaber-Grodzins-Sunyar 1958)
H_NU = Decimal('-1')                # nu 左手
H_NUBAR = Decimal('+1')             # anti-nu 右手

# ---------------------------------------------------------------- 守恒律检验器
# 末态粒子库: (名称, 电荷/e, 自旋, 说明)
SPECIES = {
    'n':    ('中子', Decimal('0'), Decimal('0.5'), 'udd 复合扭结, 净通量 0'),
    'p':    ('质子', Decimal('1'), Decimal('0.5'), 'uud 复合扭结, +q_e'),
    'e':    ('电子', Decimal('-1'), Decimal('0.5'), '闭合扭结, -q_e'),
    'nubar': ('反电子中微子', Decimal('0'), Decimal('0.5'), '零净通量闭合扭结'),
    'gamma': ('光子', Decimal('0'), Decimal('1'), '开式横螺旋零模'),
    'ep': ('正电子', Decimal('1'), Decimal('0.5'), '负向测试用: 电荷 +1'),
    'pi': ('负pi介子', Decimal('-1'), Decimal('0'), '强子末态对照'),
}


def charge_of(state):
    return sum(SPECIES[k][1] * v for k, v in state.items())


def spin_possible(state):
    """多体自旋耦合: 逐个做 Clebsch-Gordan 直和分解, 返回可达总自旋集合."""
    tot = [Decimal('0')]
    for k, v in state.items():
        s = SPECIES[k][2]
        n = int(v)
        for _i in range(n):
            new = []
            for j in tot:
                lo = abs(j - s)
                hi = j + s
                x = lo
                while x <= hi + Decimal('1e-30'):
                    new.append(x)
                    x += Decimal('1')
            # 去重
            uniq = []
            for x in new:
                if not any(abs(x - y) < Decimal('1e-30') for y in uniq):
                    uniq.append(x)
            tot = uniq
    return sorted(tot)


def spin_dim(state):
    return int(math.prod([int((2 * SPECIES[k][2] + 1) ** int(v)) for k, v in state.items()]))


def mz_multiplet(state):
    """统计 m_z 分布: 返回 dict {m_z: 计数}."""
    dist = {Decimal('0'): 1}
    for k, v in state.items():
        s = SPECIES[k][2]
        for _i in range(int(v)):
            nd = {}
            for m, c in dist.items():
                for ms in (s, -s):
                    key = m + ms
                    nd[key] = nd.get(key, 0) + c
            dist = nd
    return dist


def spin_decompose(state):
    """由 m_z 分布反推直和分解, 保留简并重数: 返回 [(j, multiplicity), ...].

    算法: 最大的 |m_z| 只能来自最大的 j, 其计数即该 j 的重数; 扣除该表示的全部 m_z 贡献后迭代.
    (注意: 不能简单地对耦合结果去重, 1/2 x 1/2 x 1/2 中 j=1/2 出现两次, 去重会把维数从 8 降到 6.)
    """
    d = dict(mz_multiplet(state))
    eps = Decimal('1e-30')
    res = []
    while any(v > 0 for v in d.values()):
        j = max(k for k, v in d.items() if v > 0)
        mul = d[j]
        res.append((j, mul))
        m = -j
        while m <= j + eps:
            d[m] = max(0, d.get(m, 0) - mul)
            m += Decimal('1')
    return res


def check_channel(init, final):
    """返回 (电荷守恒?, 自旋 1/2 可达?, 说明)."""
    qi = charge_of(init)
    qf = charge_of(final)
    q_ok = (qi == qf)
    spins = spin_possible(final)
    s_ok = any(abs(x - Decimal('0.5')) < Decimal('1e-30') for x in spins)
    return q_ok, s_ok, spins

# =================================================================== 实现验证器
def selfcheck():
    emit('')
    emit('=' * 78)
    emit('第一部分  实现验证器 (先校准工具, 再判来稿)')
    emit('=' * 78)
    emit('  %-5s %-52s %-32s %s' % ('编号', '对象', '读数', '判定'))
    emit('-' * 78)

    # SC1  Q_beta 与文献值
    lit = Decimal('0.782333')
    d1 = abs(Q_BETA - lit) / lit
    sc('SC1', 'Q = m_n - m_p - m_e 与文献 0.782333 MeV', 'Q=' + F(Q_BETA) + ' 偏差 ' + F(d1), d1 < Decimal('1e-5'))

    # SC2  三体自旋耦合 1/2 x 1/2 x 1/2 = 3/2 + 1/2 + 1/2
    st3 = {'p': 1, 'e': 1, 'nubar': 1}
    sp = spin_possible(st3)
    dec = spin_decompose(st3)
    dim = sum(int(mul * (2 * j + 1)) for j, mul in dec)
    dim_ok = (dim == spin_dim(st3) == 8)
    has_half = any(abs(x - Decimal('0.5')) < Decimal('1e-30') for x in sp)
    dist = mz_multiplet(st3)
    ref = {Decimal('1.5'): 1, Decimal('0.5'): 3, Decimal('-0.5'): 3, Decimal('-1.5'): 1}
    mz_ok = all(dist.get(k, 0) == v for k, v in ref.items())
    dec_str = ' + '.join(['%s(重数%d)' % (j, m) for j, m in dec])
    sc('SC2', '1/2 三重耦合直和分解 (维数/简并/m_z 多重态)',
       '维数 %d=8, 分解 %s' % (dim, dec_str), dim_ok and has_half and mz_ok)

    # SC3  不确定性原理
    dp_half = HBARC / (2 * R_N)
    dp_one = HBARC / R_N
    sc('SC3', 'Delta p c = hbar c / (2 Delta x), Delta x=0.8 fm',
       F(dp_half) + ' / ' + F(dp_one) + ' MeV', abs(dp_half - Decimal('123.329')) < Decimal('0.01'))

    # SC4  W 衰变长度
    ctau = HBARC / (GAMMA_W * 1000)
    sc('SC4', 'c tau_W = hbar c / Gamma_W 与文献 ~0.1 fm', F(ctau) + ' fm',
       abs(ctau - Decimal('0.0946')) < Decimal('0.001'))

    # SC5  守恒检验器 负向测试 (电荷不守恒过程必须被拦下)
    # 注意: 不能用 dict 重复键写两个电子(后者覆盖前者), 必须引入独立的正电子物种
    qi_ok, si_ok, _ = check_channel({'n': 1}, {'p': 1, 'e': 1, 'ep': 1})
    sc('SC5', '负向: n -> p + e- + e+ (电荷 +1) 应被判违反',
       'charge_ok=%s' % qi_ok, (not qi_ok))
    # 负向测试 2: n -> p + pi- 电荷守恒但能量禁戒, 检验器应只报电荷通过
    q5b, s5b, _ = check_channel({'n': 1}, {'p': 1, 'pi': 1})
    sc('SC5b', '对照: n -> p + pi- 电荷守恒(能量另判)', 'charge=%s' % q5b, q5b)

    # SC6  守恒检验器 正向测试
    q6, s6, _ = check_channel({'n': 1}, {'p': 1, 'e': 1, 'nubar': 1})
    sc('SC6', '正向: n -> p + e + anti-nu 应通过电荷与自旋',
       'charge=%s spin=%s' % (q6, s6), q6 and s6)

    # SC7  半整数加法群不能生成 1/3
    # 1/2 的加法群 = { k/2 : k in Z }, 分母集合 {1, 2}; 1/3 的分母为 3
    ok7 = True
    for k in range(-400, 401):
        if abs(Decimal(k) / 2 - Q_U) < Decimal('1e-30'):
            ok7 = False
    sc('SC7', '半整数加法群 {k/2} 不可生成 2/3 (扫描 k=-400..400)',
       'no hit: %s' % ok7, ok7)

    # SC8  能量对应波长
    lam = HBARC / Q_BETA
    ratio_lam = lam / R_N
    sc('SC8', 'hbar c / Q 与中子半径之比',
       F(lam) + ' fm = ' + F(ratio_lam) + ' R_n', abs(lam - Decimal('252.24')) < Decimal('0.1'))

    # SC9  中子寿命 -> 宽度
    gam_n = HBAR_MEV_S / TAU_N
    sc('SC9', 'Gamma_n = hbar / tau_n', F(gam_n) + ' MeV',
       abs(gam_n - Decimal('7.484e-25')) / Decimal('7.484e-25') < Decimal('1e-2'))

    # SC10 势垒欠定: 三组不同 (Delta, a) 复现同一寿命
    nu0 = Q_BETA / HBAR_MEV_S                      # 尝试频率 (s^-1)
    T_prob = (1 / TAU_N) / nu0                     # 所需透射概率
    kappa_a = -Decimal(str(math.log(float(T_prob)))) / 2
    rows = []
    for delta in (Decimal('1'), Decimal('10'), Decimal('100')):
        m_use = M_N
        kap = (2 * m_use * delta).sqrt() / HBARC
        a = kappa_a / kap
        rows.append((delta, kap, a))
    all_same = True
    for delta, kap, a in rows:
        # 复算: exp(-2 kap a) 应回到 T_prob
        back = Decimal(str(math.exp(float(-2 * kap * a))))
        if abs(back - T_prob) / T_prob > Decimal('1e-9'):
            all_same = False
    sc('SC10', 'WKB 方势垒: 三组 (Delta, a) 复现同一 tau_n',
       'a = %s fm (Delta=10)' % F(rows[1][2]), all_same and T_prob < 1)

    emit('-' * 78)
    n_ok = sum(1 for c in _CHECKS if c['ok'])
    emit('  自检合计 %d/%d' % (n_ok, len(_CHECKS)))
    return {'T_prob': T_prob, 'kappa_a': kappa_a, 'barrier_rows': rows,
            'ctau_W': ctau, 'dp_half': dp_half, 'lam_Q': lam,
            'ratio_lam': ratio_lam, 'gam_n': gam_n,
            'spin_triple': dec_str, 'spin_dim': dim}

# =================================================================== 条目判定
def items(ctx):
    emit('')
    emit('=' * 78)
    emit('第二部分  来稿章节 1-6 本体判定')
    emit('=' * 78)

    # ---------------- D01 电子局域化否证 (不确定性原理)
    dp = ctx['dp_half']                                   # MeV (Delta p * c)
    Ekin = (dp * dp + M_E * M_E).sqrt()
    T_kin = Ekin - M_E
    ratio01 = T_kin / Q_BETA
    rec('D01', 'FAIL',
        '章节 2 阶段 3 的「拆分出电子」若按字面(电子预先局域于中子内部)理解, 被不确定性原理否证',
        'R_n=%s fm => Delta p c >= %s MeV, E=%s MeV, T=%s MeV; 而 Q=%s MeV; 比值 T/Q=%s '
        '(取 hbar 而非 hbar/2 则为 %s 倍) => 束缚电子需动能约为释放能的 157 倍, 该图像不成立. '
        '这是 1930 年代否定「核内电子假说」的同一论证, 本册仅做机器复算.'
        % (F(R_N, 2), F(dp), F(Ekin), F(T_kin), F(Q_BETA), F(ratio01), F(2 * ratio01)),
        tag='beta_decay')

    # ---------------- D02 轻子数无拓扑来源
    SPECIES['nu'] = ('电子中微子', Decimal('0'), Decimal('0.5'), '与反中微子同标签, L_e=+1')
    q_a, s_a, _ = check_channel({'n': 1}, {'p': 1, 'e': 1, 'nubar': 1})
    q_b, s_b, _ = check_channel({'n': 1}, {'p': 1, 'e': 1, 'nu': 1})
    rec('D02', 'FAIL',
        '章节 3 的四条守恒律不区分 nu_e 与 anti-nu_e => 轻子数守恒无拓扑来源',
        '标准道 n->p+e+anti-nu: 电荷守恒=%s, 自旋 1/2 可达=%s; '
        '被实验排除的 n->p+e+nu (L_e: 0 -> +2): 电荷守恒=%s, 自旋 1/2 可达=%s. '
        '两者在来稿的守恒律集下完全同等地被允许 => 章节 2 阶段 3 「必须生成反电子中微子」无推导, '
        '只是一条外加的标签约定.'
        % (q_a, s_a, q_b, s_b),
        tag='lepton_number')

    # ---------------- D03 手性内部矛盾
    rec('D03', 'FAIL',
        '章节 4 的「右手镜像扭结无法发生重联」与末态含右手反中微子矛盾',
        'V-A 的准确内容: 耦合只取左手手征分量, 而反费米子的螺旋度为正. 实验 '
        '(Goldhaber-Grodzins-Sunyar 1958) 定 h_nu=%s => h_anti-nu=%s. 章节 2 阶段 3 的末态含 anti-nu_e, '
        '即体系必须产出右手螺旋产物; 但章节 4 称右手构型「拓扑上无法发生」该重联. '
        '两条出路皆堵: (i) 严格取章节 4 => 右手 anti-nu 不能产生, 与衰变道矛盾; '
        '(ii) 改口为体系内 anti-nu 亦左手 => 与螺旋度实测冲突.' % (F(H_NU, 1), F(H_NUBAR, 1)),
        tag='chirality')

    # ---------------- D04 W 传播性分层
    ctau = ctx['ctau_W']
    ratio04 = ctau / R_N
    rec('D04', 'BOUNDARY',
        '章节 1 / 2 阶段 2 的「W 不是真实传播的粒子」须分层裁定, 不可整体成立',
        'c tau_W = hbar c / Gamma_W = %s fm, 仅为 R_n=%s fm 的 %s => 在 beta 衰变这一低能语境下 '
        'W 深度离壳 (虚), 「瞬态拓扑畸变」的局部描述成立. 但对撞机自 1983 年 (UA1/UA2) 起 '
        '在 q^2 ~ M_W^2 处直接观测到 Breit-Wigner 共振 (M_W=%s GeV, Gamma_W=%s GeV), '
        '故「W 不是真实传播的粒子」作为一般断言被否证. 存活须改为「可传播的集体拓扑模式」并解释 q^2 依赖 '
        '(与 S03-V18.8 判据 A-prime / F2-4 独立: 该册用跨 1.056e+10 倍 q^2 标度的传播子反解, '
        '本册用衰变长度对源尺度, 两条理由互不依赖).' % (F(ctau), F(R_N, 2), F(ratio04), F(M_W, 4), F(GAMMA_W, 4)),
        tag='W_propagator')

    # ---------------- D05 强作用「不剪断」 vs QCD 流管断裂
    sigma_fm = SIGMA_QCD_GEV2 * GEV2_TO_GEVFM             # GeV/fm
    eth_pi = 2 * Decimal('0.13957')                       # 2 m_pi  GeV
    eth_qq = 2 * Decimal('0.336')                         # 2 m_q(constituent) GeV
    l_pi = eth_pi / sigma_fm
    l_qq = eth_qq / sigma_fm
    l_lat = Decimal('1.2')                                # 格点 QCD 观测量级
    rec('D05', 'FAIL',
        '章节 5 表中「强相互作用: 稳定链接, 不剪断; 重联需极高能量」与 QCD 流管断裂冲突',
        '弦张力 sigma=%s GeV^2=%s GeV/fm. 断裂阈值取最轻强子对 2m_pi=%s GeV => 断裂长度 %s fm; '
        '取 2m_q(组分)=%s GeV => %s fm; 格点 QCD 观测约 %s fm. 三者与 R_n=%s fm 同量级或更小 '
        '(l/R_n = %s ~ %s) => 在核子内部尺度上流管断裂是常态, 不是「需要极高能量」的例外. '
        '故「强=不剪断 / 弱=剪断」这一分类失效: 两者都涉及场线重联, 区别须另寻判据.'
        % (F(SIGMA_QCD_GEV2, 3), F(sigma_fm, 4), F(eth_pi, 4), F(l_pi),
           F(eth_qq, 4), F(l_qq), F(l_lat, 2), F(R_N, 2), F(l_pi / R_N), F(l_lat / R_N)),
        tag='strong_vs_weak')

    # ---------------- D06 尺度不自洽
    rows = ctx['barrier_rows']
    a_min = min(r[2] for r in rows)
    a_max = max(r[2] for r in rows)
    rec('D06', 'FAIL',
        '章节 2 的「局域场重联」在尺度上不自洽 (两条独立读数)',
        '(i) 释放能对应的康普顿波长 hbar c / Q = %s fm = %s 倍 R_n, 即产物在运动学上无法被局域于 '
        '中子尺度内; (ii) 由实测寿命 %s s 反解 WKB 方势垒宽度, 在 Delta=1~100 MeV 范围内得 '
        'a = %s ~ %s fm = %s ~ %s 倍 R_n (取 m=m_n; 取 m=m_e 则更大). '
        '=> 「局域重联 + 长寿命」二者不能同时成立.' 
        % (F(ctx['lam_Q']), F(ctx['ratio_lam']), F(TAU_N, 1), F(a_min), F(a_max),
           F(a_min / R_N), F(a_max / R_N)),
        tag='scale')

    # ---------------- D07 隧穿叙事欠定
    rec('D07', 'FAIL',
        '章节 2 阶段 1 的隧穿叙事欠定: 2 个自由参数对 1 条数据, 任何寿命都可被拟合',
        ('所需透射概率 T = (1/tau_n) / (Q/hbar) = %s, 对应 kappa*a = %s (无量纲). '
         'kappa = sqrt(2 m Delta)/hbar c 含质量选取 m 与势垒高 Delta 两个自由参数, 宽度 a 随之确定: '
         + ' | '.join(['Delta=%s MeV => a=%s fm' % (F(r[0], 1), F(r[2])) for r in rows])
         + '. 三组 (Delta, a) 给出同一个 tau_n => 该叙事对寿命无任何事前预测力 '
         '(与 S03-C0023 / S03-C0050 同型: 连续族对单条数据恒可拟合).')
        % (F(ctx['T_prob']), F(ctx['kappa_a'])),
        tag='tunneling')

    # ---------------- D08 零预测力: 无 Fermi / GT 通道区分
    rec('D08', 'FAIL',
        '章节 2 无 Fermi / Gamow-Teller 通道区分 => 给不出任何微分观测量',
        '实际中子衰变是 Fermi (S=0) 与 Gamow-Teller (S=1) 的混合, 混合比 lambda = g_A/g_V = %s, '
        '并由之给出电子角分布不对称系数. 来稿只声称「矢量自旋叠加满足角动量守恒」, 未指定 S 通道, '
        '故无法产出电子能谱形状、角分布、极化观测量中的任何一项. '
        '交叉印证: openuft 04_公共成果 的《TUFT-deltaA 五项前置闭合判定》已独立判定 '
        '「单一复场只给同一算符的两种耦合 => 干涉是强度干涉而非两独立振幅 => 相位不进可观测量」, '
        '与本册结论同向且互不依赖.' % (F(G_A_OVER_G_V, 4)),
        tag='predictivity')

    # ---------------- D09 分数电荷无拓扑来源
    rec('D09', 'FAIL',
        '章节 1 只在全局层成立: 子扭结(夸克)的分数电荷无法由半整数环绕数承载',
        '全局层: uud = %s+%s+%s = +1, udd = %s+%s+%s = 0 (机器求和, 与实测逐项一致), '
        '两者皆可写为 k/2 (k 整数) => 与 Lk 属于 (1/2)Z 相容, 章节 1 的全局电荷读数成立. '
        '子扭结层: 2/3 与 -1/3 的既约分母为 3, '
        '而半整数加法群 {k/2} 的分母集合为 {1,2} => 不可达 (SC7 扫描 k=-400..400 无命中). '
        '射程: 失败在「分数电荷的来源」, 不是三扭结复合图像本身 (与 V18.4 V4-e-read 同口径).'
        % (F(Q_U, 4), F(Q_U, 4), F(Q_D, 4), F(Q_D, 4), F(Q_D, 4), F(Q_U, 4)),
        tag='fractional_charge')

    # ---------------- D10 拓扑质量违反既有裁定
    rec('D10', 'CORRECTED',
        '章节 3 第 4 条「拓扑质量 = 总挠率积分」违反既有机器裁定 S03-V18.6 SC6',
        'S03-V18.6 SC6 已机器证明 int(tau) ds 无量纲且尺度不变 (lambda=1..100 最大偏差 8.882e-16), '
        '故它不能承载质量量纲; S03-V18.5 F1-4 / S03-C0041 已判 [int tau ds]=1 使 m-prime 无量纲. '
        '章节 3 第 4 条把衰变前后的「总挠率积分之差」直接等同于产物动能, 量纲链断裂. '
        '登记口径: 本条为既有公设边界的交叉印证, 非本册新发现, 不得计入新增否证.',
        tag='dimension')

    # ---------------- D11 / D12 成立但零信息量
    rec('D11', 'PASS-零信息量',
        '章节 3 第 2 条电荷守恒在全局层算通',
        '0 -> (+1) + (-1) + 0, 机器检验通过. 但这是把 SM 的夸克电荷赋值搬入后的恒等重述: '
        'udd/uud 的整数和本就由电荷赋值保证, 不含 GAQ 独立贡献, 也不产生任何新约束.',
        tag='identity_restatement')

    rec('D12', 'BOUNDARY',
        '章节 3 第 3 条自旋守恒技术上成立, 但不产生选择定则',
        '%s 三重 1/2 耦合的直和分解为 %s (维数 %d = 4+2+2, m_z 多重态与解析值逐项一致, 见 SC2) '
        '=> 总 J=1/2 可达, 来稿自洽. 但分解同时含 3/2, 故该判据不唯一确定末态; '
        '且这是标准角动量守恒的复算, 不含 GAQ 内容.' % ('p+e+anti-nu', ctx['spin_triple'], ctx['spin_dim']),
        tag='identity_restatement')

    # ---------------- D13 分支收口
    rec('D13', 'INFO',
        '章节 7 的三条分支在本册开工前已全部裁定并收口 => 不再存在「可选而待办」的支线',
        '分支一 色荷/禁闭: 关闭 (S03-V18.4, 五条 FAIL, S03-C0029..C0033); '
        '分支二 中微子零通量扭结/马约拉纳: 关闭 (S03-V18.1 + V18.2, S03-C0016..C0023); '
        '分支三 CKM 拓扑起源: 阻塞 (S03-V18.8, S03-C0045..C0053 批次二). '
        '=> 对「选择哪条分支」的回答是: 三条都已执行完毕, 答案不是选一条, 而是承认三条全闭. '
        '口径警告: 存在两套互不相同的「分支三」编号 (Frenet-Serret 来稿的分支三=孤子拓扑相变守恒律, '
        '由 S03-V18.10 执行; beta 衰变来稿的分支三=CKM, 由 S03-V18.8 执行), 跨册引用必须带来源前缀.',
        tag='branch_closure')

    # ---------------- D14 编号冲突
    rec('D14', 'INFO(治理·交叉印证, 非本册新发现)',
        'claims.csv 存在编号空间冲突: S03-C0045..C0053 被 S03-V18.10 与 S03-V18.8 两册重复使用',
        '扫描 claims.csv: 一批 S03-C0045..C0053 指向 09_验证结果/S03_V18_10_...md, '
        '另一批同号条目指向 09_验证结果/S03_V18_8_...md, 且 11_证伪与反例 的两个 F2 小节 '
        '各自声称 C0045-C0053 归属本册. => 跨册回链必须带册号前缀, 否则「按编号检索」会静默取到错误册. '
        '诚实留痕: 该冲突已由同日并行的 S03-V18.11(分支 B-1 几何 anholonomy) 册独立登记为 S03-C0060, '
        '故本条为交叉印证, 不得计入新增否证. '
        '本册自 S03-C0064 起编 (C0054..C0063 已被该并行册占用), 并采用「册号 + 条目号」双标签回链.',
        tag='governance')

    # ---------------- D15 本册自造的第二次编号冲突 (诚实留痕)
    rec('D15', 'INFO(治理·本册自造缺陷)',
        '本册在登记「编号冲突」的同时, 自己制造了第二次编号冲突 (已改号修正)',
        '本册首版按写作时的文件快照取 C0054..C0063 登记 10 条证据, 而并行的 S03-V18.11(分支 B-1) 册 '
        '在同一时段也自 C0054 起编并占用了 C0054..C0063 => 两批条目完全重号. '
        '同时本册版本号 V18_11 亦与该并行册相撞. 处置: 本册为后到者, 按既有约定「后到者改号不覆盖他人」'
        '改号为 V18_12, 证据编号改为 C0064..C0073, 未改动他人任何行. '
        '教训: 登记治理缺陷前必须先重扫目标文件的当前状态, 不能依赖开工时的快照 —— '
        '本册 D14 的扫描恰好只查了 C0045..C0053 段而未查新号段, 属同类疏漏的第二次发生.',
        tag='governance')

# =================================================================== D14 机器取证
def scan_claim_conflict():
    """机器取证 claims.csv 的编号冲突: 同一批编号被两个判定册引用."""
    path = os.path.join(ROOT, 'claims.csv')
    if not os.path.exists(path):
        return None
    txt = io.open(path, encoding='utf-8').read()
    import re
    pat = re.compile(r'(S03-C\d+),[^,]*,[^,]*,(.*?)(?=\nS03-C|\Z)', re.S)
    buckets = {}
    for m in pat.finditer(txt):
        cid = m.group(1)
        body = m.group(2)
        for tag in ('S03_V18_10', 'S03_V18_8', 'S03_V18_5', 'S03_V18_4'):
            if tag in body:
                buckets.setdefault(tag, set()).add(cid)
    inter = sorted(buckets.get('S03_V18_10', set()) & buckets.get('S03_V18_8', set()))
    return {'counts': {k: len(v) for k, v in buckets.items()},
            'overlap': inter, 'n_overlap': len(inter)}


# =================================================================== 主流程
def main():
    emit('#' * 78)
    emit('# S03-V18.12  GAQ-UFT V18 中子 beta 衰变拓扑图像 -- 本体(章节 1-6)机器审计')
    emit('# 红线: 本册全部为可否证性判定与自洽性检验, 不含对 GAQ 的正面支持证据')
    emit('#' * 78)

    ctx = selfcheck()
    items(ctx)

    conf = scan_claim_conflict()
    emit('')
    emit('=' * 78)
    emit('第三部分  D14 编号冲突的机器取证')
    emit('=' * 78)
    if conf is None:
        emit('  claims.csv 未找到, 跳过.')
    else:
        emit('  各判定册引用的证据编号条数: %s' % conf['counts'])
        emit('  S03-V18.10 与 S03-V18.8 共用的编号 (%d 条): %s'
             % (conf['n_overlap'], ', '.join(conf['overlap']) if conf['overlap'] else '(无)'))
        emit('  => 编号空间冲突确认: 按编号检索会静默取到另一册, 跨册回链必须带册号前缀.')

    # ---------------------------------------------------------------- 汇总
    def cnt(lv):
        return sum(1 for it in _ITEMS if it['level'].startswith(lv))

    emit('')
    emit('=' * 78)
    emit('第四部分  汇总')
    emit('=' * 78)
    emit('  条目合计 %d' % len(_ITEMS))
    for lv in ('FAIL', 'BOUNDARY', 'CORRECTED', 'PASS', 'INFO'):
        emit('    %-12s %d' % (lv, cnt(lv)))
    n_ok = sum(1 for c in _CHECKS if c['ok'])
    emit('  自检 %d/%d' % (n_ok, len(_CHECKS)))

    emit('')
    emit('-' * 78)
    emit('关键读数 (供判定册引用, 一律取原始数值不做二次舍入):')
    emit('  Q_beta            = %s MeV' % F(Q_BETA))
    emit('  Delta p c (R=0.8) = %s MeV   => T_e = %s MeV   T/Q = %s'
         % (F(ctx['dp_half']),
            F((ctx['dp_half'] ** 2 + M_E ** 2).sqrt() - M_E),
            F(((ctx['dp_half'] ** 2 + M_E ** 2).sqrt() - M_E) / Q_BETA)))
    emit('  hbar c / Q        = %s fm = %s R_n' % (F(ctx['lam_Q']), F(ctx['ratio_lam'])))
    emit('  c tau_W           = %s fm = %s R_n' % (F(ctx['ctau_W']), F(ctx['ctau_W'] / R_N)))
    emit('  Gamma_n           = %s MeV ; 所需透射概率 T = %s' % (F(ctx['gam_n']), F(ctx['T_prob'])))
    emit('  WKB kappa*a       = %s' % F(ctx['kappa_a']))
    for r in ctx['barrier_rows']:
        emit('    Delta=%8s MeV -> kappa=%s fm^-1, a=%s fm = %s R_n'
             % (F(r[0], 1), F(r[1]), F(r[2]), F(r[2] / R_N)))
    emit('  sigma_QCD         = %s GeV/fm ; 断裂长度 %s ~ %s fm (格点 ~1.2 fm)'
         % (F(SIGMA_QCD_GEV2 * GEV2_TO_GEVFM, 4),
            F(2 * Decimal('0.13957') / (SIGMA_QCD_GEV2 * GEV2_TO_GEVFM)),
            F(2 * Decimal('0.336') / (SIGMA_QCD_GEV2 * GEV2_TO_GEVFM))))
    emit('-' * 78)
    emit('PASS = %d' % cnt('PASS'))
    emit('FAIL = %d' % (cnt('FAIL')))
    emit('BOUNDARY = %d' % cnt('BOUNDARY'))
    emit('INFO = %d' % cnt('INFO'))

    os.makedirs(os.path.dirname(OUT_TXT), exist_ok=True)
    io.open(OUT_TXT, 'w', encoding='utf-8').write('\n'.join(_LINES) + '\n')
    emit('')
    emit('报告已写入: ' + OUT_TXT)
    return 0


if __name__ == '__main__':
    sys.exit(main())
