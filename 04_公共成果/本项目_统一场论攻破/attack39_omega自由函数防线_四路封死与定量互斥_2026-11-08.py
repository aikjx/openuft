# -*- coding: utf-8 -*-
# attack39 / 攻破㉛ —— omega(r,t) 自由函数防线：四路封死 + 定量互斥（2026-11-08）
# 承接 r95 §九 P4：把「固定则被排除、自由则不可证伪」升级为机器可判定定理。
# 纯标准库（fractions.Fraction + math + os/json/io），无第三方依赖。
# 红线：攻破的是「防线不可判定」，不是物理成立；0/22、UFT-3=0、L3=0 不变。
import os, sys, io, json, math
from fractions import Fraction as F
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = 'attack39_omega自由函数防线_四路封死与定量互斥_2026-11-08'
LINES = []
def emit(s=''):
    LINES.append(s)
    print(s)
ENTRIES = []
def add(uid, claim, verdict, reading):
    ENTRIES.append({'id': uid, 'claim': claim, 'verdict': verdict, 'reading': reading})
    emit('[%-9s] %s | %s' % (verdict, uid, claim))
    emit('            读数: %s' % reading)
GUARDS = []
def guard(gid, desc, ok, reading):
    ok = bool(ok)
    GUARDS.append({'id': gid, 'desc': desc, 'ok': ok, 'reading': reading})
    emit('[%s] %s | %s' % ('OK' if ok else 'BAD', gid, desc))
    emit('            读数: %s' % reading)
    return ok

# ---------- 登记输入（[C] 级实验锚 + 只读事实源）----------
WE = 1.990986592790182e-07       # 地球公转角速度 s^-1
WM = 1.0585759726109988e-07      # 火星
RE, RM = 1.0, 1.523679          # 半长轴 AU
TE, T_MARS_OBS = 365.25, 686.98 # d（r95 G05 观测口径）
P_KEPLER = F(-3, 2)
ALPHA = 1 / 137.035999084
MERCURY_ARCSEC, MERCURY_PERIOD = 42.98, 87.969   # ″/世纪、d
W3_REL = os.path.join(HERE, '..', '全维全体系统一场论', '数据', '全维验收矩阵.json')

def radial(p):
    # 球对称径向：nabla^2(r^p) = p(p+1) r^(p-2)
    return p * (p + 1)
def period_days(p):
    return TE * (RM / RE) ** (-float(p))
def apsidal_ratio(p):
    # 幂律中心力 F∝r^(2p+1) 的近圆 apsidal 角 / 2pi
    return 1.0 / math.sqrt(2 * float(p) + 4)

emit('== attack39 攻破㉛·omega(r,t) 自由函数防线：四路封死与定量互斥 ==')
emit('-- 承接 r95 §九 P4：本册把「固定则被排除、自由则不可证伪」做成可判定定理 --')
emit('-- 输入：[C] 级实验锚（两行星角速度/半长轴比、火星周期、水星进动）；W3 事实源为只读 JSON --')

# ---------- 观测钉死 ----------
p_obs = math.log(WM / WE) / math.log(RM / RE)
rel_obs = abs(p_obs + 1.5) / 1.5
T_kep, T_inv, T_rigid = period_days(P_KEPLER), period_days(F(-1)), period_days(F(0))
d_kep = abs(T_kep - T_MARS_OBS) / T_MARS_OBS
d_inv = abs(T_inv - T_MARS_OBS) / T_MARS_OBS
d_rigid = abs(T_rigid - T_MARS_OBS) / T_MARS_OBS

add('A01', '控制组：r95 G05 三支周期复现，观测把 omega(r) 幂次钉死在 -3/2', 'PASS',
    'p_obs=%.16f（vs -3/2 相对 %.3e）；T_Kepler=%.6f d（相对 %.3e）、T_1/r=%.6f d（差 %.4f%%）、T_刚体=%.2f d（差 %.4f%%）；观测 %.2f d'
    % (p_obs, rel_obs, T_kep, d_kep, T_inv, d_inv * 100, T_rigid, d_rigid * 100, T_MARS_OBS))

# ---------- 第一路：自由无质量场 ----------
grid = [F(n, 2) for n in range(-20, 21)]
free_set = [p for p in grid if radial(p) == 0]
res_k = radial(P_KEPLER)
add('A02', '第一路封死：球对称自由无质量场 b=0 的解集不含 Kepler 幂', 'FAIL',
    'b=0 ⇔ p(p+1)=0 ⇒ 精确解集 {%s}（count=%d）；Kepler p=-3/2 残差 = %s ≠ 0'
    % (', '.join(str(x) for x in free_set), len(free_set), res_k))

# ---------- 第二路：最小势项 b ----------
b_req = -res_k
disc = 1 - 4 * b_req
s = F(math.isqrt(int(disc)))
r1, r2 = (-1 + s) / 2, (-1 - s) / 2
n_alpha = math.log(0.75) / math.log(ALPHA)
add('A03', '第二路代价：唯一最小修法 b=-p(p+1)=-3/4 自带双根且无第一性来源', 'FAIL',
    'b=%s；判别式 1-4b=%s ⇒ 双根 {%s, %s}（须外加选支边界条件）；alpha^n=3/4 需 n=%.9f（非整数，库内无量纲常数不能导出 b）'
    % (b_req, disc, r1, r2, n_alpha))

# ---------- 第三路：自相互作用势 ----------
q = 2 - 2 / P_KEPLER
c_pot = res_k / q
coupling_exp = 2 - q
add('A04', '第三路封死：自相互作用势 V∝omega^q 要求分数幂 + 新有量纲标度', 'FAIL',
    '齐次匹配 q=2-2/p=%s（非整数）；系数 c=p(p+1)/q=%s；耦合量纲指数 2-q=%s ⇒ 非多项式势 + 新有量纲常数，外部输入账增加'
    % (q, c_pot, coupling_exp))

# ---------- 第四路：时间依赖 ----------
sep_forced = (res_k != 0)
add('A05', '第四路封死：时间依赖 omega=r^p T(t) 由 Box=0 分离变量强制 K=0', 'FAIL',
    'T″/(c²T) = p(p+1)/r²：左仅依赖 t、右仅依赖 r ⇒ 分离常数必须 0 且 p(p+1)=0；Kepler p=-3/2 给右端 (%s)/r² ≠ 常数 ⇒ 无解；允许幂仍只有 {0,-1}'
    % res_k)

# ---------- 放开 b：连续谱 ----------
scan = []
for b in [F(-1), F(-7, 8), F(-3, 4), F(-1, 2), F(0)]:
    d = 1 - 4 * float(b)
    pm = (-1 - math.sqrt(d)) / 2 if d >= 0 else float('nan')
    scan.append((b, pm))
add('A06', '放开 b ⇒ p 连续谱，不可证伪原样复发（r95 E06）', 'FAIL',
    'b→p_minus：%s；5 个实根互异且覆盖 -3/2 两侧 ⇒ 任何观测都可被某个 b 拟合，判别力归零'
    % '，'.join('%s→%.6f' % (b, pm) for b, pm in scan))

# ---------- 定量互斥（BOUNDARY：近圆幂律近似）----------
obs_rad = MERCURY_ARCSEC / 206265.0
orbits = 100 * TE / MERCURY_PERIOD
delta = obs_rad / orbits
dp_req = -delta / (2 * math.pi)
dp_2p = p_obs - (-1.5)
ratio = dp_2p / dp_req
add('A07', '水星进动定量互斥：修好幂次后 apsidal 闭合、附加进动 0', 'BOUNDARY',
    'p=-3/2 ⇒ Phi/2pi=%.1f（闭合，附加进动 0）；观测 %.2f″/世纪 ⇒ 每圈 %.3e rad ⇒ 所需 delta_p=%.3e，而两行星拟合 delta_p=%.3e，比值 %.2f ⇒ 同一幂律不能同时满足两者（近圆幂律近似，非完整 GR 后牛顿）'
    % (apsidal_ratio(P_KEPLER), MERCURY_ARCSEC, delta, dp_req, dp_2p, ratio))

# ---------- W3 事实源（只读）----------
W3_PASS, W3_FAIL, W3_PART, W3_NA, W3_DEBT = 0, 17, 1, 4, 17.5
PASS_MAP = {'W0': 18, 'W1': 0, 'W2': 0, 'W3': 0, 'W4': 0, 'W5': 0, 'W6': 0, 'W7': 0}
DEBT_MAP = {'W0': 4.0, 'W1': 8.5, 'W2': 14.5, 'W3': 17.5, 'W4': 15.0, 'W5': 9.5, 'W6': 14.5, 'W7': 15.0}
w3_source = 'registered_fallback'
if os.path.isfile(W3_REL):
    try:
        _d = json.load(io.open(W3_REL, encoding='utf-8'))
        _bn = {x['crit']: x for x in _d['bottleneck']}
        _w3 = _bn['W3']
        W3_PASS, W3_FAIL, W3_PART, W3_NA, W3_DEBT = _w3['pass'], _w3['fail'], _w3['part'], _w3['na'], _w3['debt']
        PASS_MAP = {k: v['pass'] for k, v in _bn.items()}
        DEBT_MAP = {k: v['debt'] for k, v in _bn.items()}
        w3_source = os.path.basename(W3_REL)
    except Exception:
        pass
nonzero = [k for k, v in PASS_MAP.items() if v != 0]
debt_max = [k for k, v in DEBT_MAP.items() if v == max(DEBT_MAP.values())]
add('A08', 'W3 口径更正：「唯一零通过」宣称不成立', 'FAIL',
    'W3 fail=%d/part=%d/pass=%d/na=%d/debt=%s（源 %s）；W1..W7 全部 pass=0、W0 pass=18 ⇒ 零通过非 W3 独有；debt 最大者 = %s ⇒ W3 是唯一最大瓶颈且 fail=%d 最多'
    % (W3_FAIL, W3_PART, W3_PASS, W3_NA, W3_DEBT, w3_source, ','.join(debt_max), W3_FAIL))

add('A09', 'P4 真实代价：把 1 个自由函数换成 ≥3 项新输入', 'INFO',
    '修法代价 = 1 个自由无量纲常数 b + 1 条选支边界条件 + 1 个新有量纲标度（走势路线时）；r95 原账 12 项 ⇒ ≥15 项，Omega5（自由常数 ≤1）更不满足')

add('A10', '总裁定：FAIL（作为「给出 omega 场方程即可解除两难」）', 'INFO',
    '四路封死 + 定量互斥 ⇒ 攻破的是「防线不可判定」，不是物理成立；红线 0/22、UFT-3=0、L3=0 不变；PASS 仅控制组 A01，不迁移为物理成立、不计攻破数')

# ---------- 守卫（有牙：变异对应断言须转 BAD）----------
guard('G1', '精确解集：b=0 恰 2 支', free_set == [F(-1), F(0)] and len(free_set) == 2,
      'grid=半整数[-10,10] 共 41 点，radial(p)=0 命中 %s' % [str(x) for x in free_set])
guard('G2', 'apsidal 指数必须是 2p+4（2p+3 在 Kepler 点奇异）',
      abs(apsidal_ratio(P_KEPLER) - 1.0) < 1e-12 and (2 * float(P_KEPLER) + 3) == 0.0,
      '2p+4=%.1f ⇒ Phi/2pi=%.1f；误用 2p+3=%.1f ⇒ 除零' % (2 * float(P_KEPLER) + 4, apsidal_ratio(P_KEPLER), 2 * float(P_KEPLER) + 3))
guard('G3', 'r95 G05 三支周期复现（Kepler 相符、另两支被排除）',
      d_kep < 1e-3 and d_inv > 0.15 and d_rigid > 0.40,
      'rel Kepler=%.3e / 1_over_r=%.4f / rigid=%.4f；RM=%.6f' % (d_kep, d_inv, d_rigid, RM))
guard('G4', '判别式双根且 b=-3/4 唯一命中 -3/2',
      disc == 4 and {r1, r2} == {F(1, 2), F(-3, 2)} and b_req == F(-3, 4),
      'disc=%s roots={%s,%s} b=%s' % (disc, r1, r2, b_req))
guard('G5', 'b 不能由库内无量纲常数第一性导出',
      (not float(n_alpha).is_integer()) and 0 < n_alpha < 1,
      'alpha=%.12f；alpha^n=0.75 ⇒ n=%.9f（非整数）' % (ALPHA, n_alpha))
guard('G6', '势项三读数 Fraction 精确',
      q == F(10, 3) and c_pot == F(9, 40) and coupling_exp == F(-4, 3),
      'q=%s c=%s exp=%s' % (q, c_pot, coupling_exp))
guard('G7', '分离变量强制 K=0：Kepler 幂不可能有非零分离常数',
      sep_forced and res_k == F(3, 4) and [p for p in grid if radial(p) == 0] == [F(-1), F(0)],
      'radial(-3/2)=%s ≠ 0；允许幂 %s' % (res_k, [str(p) for p in free_set]))
guard('G8', 'b 自由 ⇒ p 连续谱（5 个实根互异且含 -3/2）',
      all(math.isfinite(pm) for _, pm in scan) and len(set(round(pm, 9) for _, pm in scan)) == 5 and any(abs(pm + 1.5) < 1e-12 for _, pm in scan),
      '；'.join('%s→%.6f' % (b, pm) for b, pm in scan))
guard('G9', '水星定量互斥：所需 delta_p 远小于两行星拟合残差',
      ratio > 100 and abs(dp_req) < 1e-6 and abs(dp_2p) > 1e-6,
      'dp_req=%.3e / dp_2p=%.3e / ratio=%.2f' % (dp_req, dp_2p, ratio))
guard('G10', 'W3 口径：debt 唯一最大、W1..W7 零通过、W0 非零',
      debt_max == ['W3'] and all(PASS_MAP[k] == 0 for k in ['W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7']) and PASS_MAP['W0'] == 18,
      'debt_max=%s；nonzero_pass=%s；W0=%d' % (debt_max, nonzero, PASS_MAP['W0']))

# ---------- 汇总 / 产物 ----------
npass = sum(1 for e in ENTRIES if e['verdict'] == 'PASS')
nfail = sum(1 for e in ENTRIES if e['verdict'] == 'FAIL')
nbnd = sum(1 for e in ENTRIES if e['verdict'] == 'BOUNDARY')
ninfo = sum(1 for e in ENTRIES if e['verdict'] == 'INFO')
nok = sum(1 for g in GUARDS if g['ok'])
emit('== 汇总：条目 %d；PASS %d / FAIL %d / BOUNDARY %d / INFO %d；守卫 %d/%d =='
     % (len(ENTRIES), npass, nfail, nbnd, ninfo, nok, len(GUARDS)))
emit('== 总裁定：FAIL（作为「给出 omega 场方程即可解除两难」）；攻破的是防线不可判定，不是物理成立 ==')
emit('红线：数学/机器自洽 ≠ 物理成立；0/22、UFT-3=0、L3=0 不变；未改治理事实源、未跑 refresh_catalog。')

payload = {
    'round': 'attack39_攻破㉛_omega自由函数防线_四路封死与定量互斥',
    'date': '2026-11-08',
    'engine': BASE + '.py',
    'entries': ENTRIES,
    'summary': {'PASS': npass, 'FAIL': nfail, 'BOUNDARY': nbnd, 'INFO': ninfo},
    'guards': GUARDS,
    'guard_pass': '%d/%d' % (nok, len(GUARDS)),
    'readings': {
        'p_obs': repr(p_obs), 'rel_obs_to_minus_3_2': repr(rel_obs),
        'T_kepler_d': repr(T_kep), 'T_1_over_r_d': repr(T_inv), 'T_rigid_d': repr(T_rigid),
        'free_power_set': [str(x) for x in free_set], 'radial_kepler_residual': str(res_k),
        'b_required': str(b_req), 'discriminant': str(disc), 'roots': [str(r1), str(r2)],
        'alpha_exponent_for_b': repr(n_alpha), 'potential_q': str(q), 'potential_c': str(c_pot),
        'coupling_exponent': str(coupling_exp), 'b_free_scan': [[str(b), repr(pm)] for b, pm in scan],
        'mercury_dp_required': repr(dp_req), 'two_planet_dp': repr(dp_2p), 'ratio': repr(ratio),
        'W3': {'fail': W3_FAIL, 'part': W3_PART, 'pass': W3_PASS, 'na': W3_NA, 'debt': W3_DEBT, 'source': w3_source},
        'debt_max': debt_max, 'nonzero_pass': nonzero,
    },
    'self_corrections': [
        'apsidal 指数首版写 2p+3，在 p=-3/2 除零；正确为 2p+4（F∝r^(2p+1)，Phi/2pi=1/sqrt(n+3)）',
        '「W3 唯一零通过」误述：W1..W7 全部 pass=0；正确为「唯一 debt=17.5 且 fail=17 最多的最大瓶颈」',
        '上一轮 HIT_COUNT 16 / ALL_b_NONZERO False 枚举过宽：精确 Fraction 解集恰 {0,-1} 两支，r^-1 是阳性对照而非 Kepler 幂救赎',
        'A06/G8 扫描点首版含 b=1/2（判别式 <0）产生 nan；正式版改为 5 个实根点 [-1,-7/8,-3/4,-1/2,0]，守卫改判「全实根且含 -3/2」',
    ],
    'cross_refs': [
        '../本项目_全维自洽与归一化/判定_TUFT-r95-螺旋时空理论_曲率挠率频率角速度_全维审计与攻破_2026-10-17.md',
        '../全维全体系统一场论/数据/全维验收矩阵.json',
        '../状态看板.md',
    ],
    'redlines': {'zero_of_22': 'unchanged', 'UFT-3': 0, 'L3': 0, 'validated': 0},
    'candidate_verdict': 'FAIL',
    'exit': 0 if nok == len(GUARDS) else 1,
}
with io.open(os.path.join(HERE, BASE + '.json'), 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=1)
with io.open(os.path.join(HERE, BASE + '_report.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(LINES) + '\n')
sys.exit(0 if nok == len(GUARDS) else 1)
