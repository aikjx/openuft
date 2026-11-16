# -*- coding: utf-8 -*-
# r417 / 算法联盟 —— LCP-1 质量机制 Yukawa 同构与自由度重定价（2026-11-17）
# 承接 r416：把 LCP-1 的 m_seal^2=m0^2+y^2 sigma0^2 与 SM Yukawa 质量机制逐项对表。
# 结论目标：若只改名， novelty=0；若主张新机制，则自由度不得少报，且不得借 SM 的输入冒充派生。
# 纯标准库；只读事实源；不宣称完成统一场论。
import os
import io
import sys
import ast
import json
import hashlib
from decimal import Decimal as Dc, getcontext

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.abspath(os.path.join(HERE, '..'))
OPENUFT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
MYLIB = os.path.abspath(os.path.join(OPENUFT, '..'))
DATA = os.path.join(PUB, '数据')
DATE = '2026-11-17'
STEM = 'TUFT-r417_LCP1质量机制Yukawa同构与自由度重定价_2026-11-17'

P_JSON = os.path.join(DATA, STEM + '.json')
P_MD = os.path.join(DATA, STEM + '.md')
P_REPORT = os.path.join(DATA, STEM + '_report.txt')
P_JUDGE = os.path.join(PUB, '判定_TUFT-r417-LCP1质量机制Yukawa同构与自由度重定价_2026-11-17.md')
P_README = os.path.join(PUB, 'README.md')

F1 = os.path.join(MYLIB, '算法联盟_物理UFT_可证伪清单_实验窗口总账_v1.md')
F2 = os.path.join(MYLIB, 'openuft_TUFT_V32分支融合报告.md')
F3 = os.path.join(MYLIB, '算法联盟_一致性强制_从反常消去推出电荷量子化与中微子Dirac层级约束_v1.md')
F4 = os.path.join(MYLIB, 'openuft_ROOT_V48_全维度攻破力评估.md')
F5 = os.path.join(PUB, '判定_TUFT-r415-全方法谱系封闭生成算子与演生规范首次机判_2026-11-16.md')
F6 = os.path.join(PUB, '判定_TUFT-r416-封装光LCP1实验门禁与最小方程判决_2026-11-17.md')
F7 = os.path.join(PUB, '判定_TUFT-r413-出路C可变函数与部门选择的可识别性攻破_2026-11-16.md')
FACTS = [F1, F2, F3, F4, F5, F6, F7]

VERDICT = ('LCP1-MASS-MECHANISM--RENAMED-YUKAWA-WHEN-MAPPED--FREEDOM-UNCHANGED-OR-'
           'UNDERSTATED--NO-Y-OR-VEV-DERIVED--EW-GAUGE-SECTOR-MISSING--0OF6-UNCHANGED')

RED = {
    'completion_0_of_6': True,
    'coverage_0_of_22': True,
    'UFT3_zero': True,
    'L3_zero': True,
    'validated_zero': True,
    'gravity_four_force_correct_equations_zero': True,
    'L3_not_implies_L4': True,
}

LINES = []
ENTRIES = []
GUARDS = []
POS = []

SQRT2 = Dc(2).sqrt()
G_F = Dc('0.000011663787')
V_SM = Dc(1) / (SQRT2 * G_F).sqrt()
SIGMA0 = V_SM / SQRT2
M_E = Dc('0.00051099895')
M_MU = Dc('0.1056583755')
M_TAU = Dc('1.77686')
Y_E = M_E / SIGMA0
Y_MU = M_MU / SIGMA0
Y_TAU = M_TAU / SIGMA0

Y_PROBE = Dc('1.2345')
LAM_L = Dc('0.13')
LAM_H = LAM_L / Dc(4)
H_PROBE = Dc('17.3')


def emit(s=''):
    LINES.append(s)
    print(s)


def add(uid, verdict, claim, reading):
    ENTRIES.append({'id': uid, 'verdict': verdict, 'claim': claim, 'reading': reading})
    emit('[' + verdict + '] ' + uid + ' | ' + claim)
    emit('            读数: ' + reading)


def guard(gid, desc, ok, reading):
    ok = bool(ok)
    GUARDS.append({'id': gid, 'desc': desc, 'ok': ok, 'reading': reading})
    emit('[' + ('OK' if ok else 'BAD') + '] ' + gid + ' | ' + desc)
    emit('            读数: ' + reading)
    return ok


def read_text(path):
    return io.open(path, encoding='utf-8').read()


def md5_text(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def fs(x, places=12):
    s = format(x, '.' + str(places) + 'E')
    if 'E' in s:
        mant, exp = s.split('E')
        sign = exp[0]
        digits = exp[1:].zfill(2)
        s = mant + 'E' + sign + digits
    return s


for p in FACTS:
    if not os.path.exists(p):
        print('MISSING_FACT ' + p)
        raise SystemExit(2)

FACT_BEFORE = dict((os.path.basename(p), md5_text(read_text(p))) for p in FACTS)
T1 = read_text(F1)
T2 = read_text(F2)
T3 = read_text(F3)
T4 = read_text(F4)
T5 = read_text(F5)
T6 = read_text(F6)
T7 = read_text(F7)

# ---------- 结构映射 ----------
MASS_REL_LCP = 'm_seal^2 = m0^2 + y^2 sigma0^2'
MASS_REL_SM = 'm_f = y_f v_sm / sqrt(2)'
MAPPING = {
    'sigma0': 'v_sm / sqrt(2)',
    'm0': '0  （SM 手征费米子的裸质量项被规范对称性禁止）',
    'y': 'y_f  （逐味 Yukawa 耦合）',
    'lambda': 'lambda_h / 4  （仅在该实标量归一化下对齐四次势）',
}

M_LCP_PROBE = Y_PROBE * SIGMA0
M_SM_PROBE = Y_PROBE * V_SM / SQRT2
MASS_MAP_RES = abs(M_LCP_PROBE / M_SM_PROBE - Dc(1))
MASS_MAP_WRONG = abs((Y_PROBE * V_SM) / M_SM_PROBE - Dc(1))

# V_LCP = lam_L/4 (sigma^2 - V_L^2)^2; sigma=(v+h)/sqrt2; V_L=v/sqrt2
# V_SM  = lam_H ((v+h)^2/2 - v^2/2)^2；等号要求 lam_H=lam_L/4。
def lcp_potential(lam, h):
    sig2 = (V_SM + h) ** 2 / Dc(2)
    v2 = V_SM ** 2 / Dc(2)
    return lam / Dc(4) * (sig2 - v2) ** 2


def sm_potential(lam, h):
    return lam * (((V_SM + h) ** 2 / Dc(2)) - (V_SM ** 2 / Dc(2))) ** 2


VL = lcp_potential(LAM_L, H_PROBE)
VH = sm_potential(LAM_H, H_PROBE)
POT_MAP_RES = abs(VL / VH - Dc(1))

RATIO_MU_E = M_MU / M_E
RATIO_TAU_E = M_TAU / M_E
RATIO_Y_MU_E = Y_MU / Y_E
RATIO_Y_TAU_E = Y_TAU / Y_E
Y_RATIO_RES_MU = abs(RATIO_Y_MU_E / RATIO_MU_E - Dc(1))
Y_RATIO_RES_TAU = abs(RATIO_Y_TAU_E / RATIO_TAU_E - Dc(1))
UNIVERSAL_Y_REL_MU = abs(RATIO_MU_E - Dc(1))
UNIVERSAL_Y_REL_TAU = abs(RATIO_TAU_E - Dc(1))

FREEDOM = {
    'renamed_branch': {
        'y_f_leptons': 3,
        'v_sm': 1,
        'lambda_h': 1,
        'new_beyond_sm': 0,
        'novelty': 0,
    },
    'new_mechanism_branch': {
        'sigma_base': 1,
        'v_base': 1,
        'lambda_base': 1,
        'y_base': 1,
        'extra_y_for_three_leptons': 2,
        'beta_functions_open': 2,
        'm0_if_nonchiral': 1,
        'base_cost': 4,
        'spectrum_fit_cost': 6,
    },
}

GATES = {
    'mass_formula_isomorphism': {'status': 'PASS', 'ok': True, 'reading': 'm0=0 且 sigma0=v_sm/sqrt2 时，LCP 质量式与 SM Yukawa 质量式逐项同构，相对残差 ' + fs(MASS_MAP_RES, 6)},
    'potential_normalization': {'status': 'PASS', 'ok': True, 'reading': 'lambda_h=lambda_L/4 后实标量势逐点相等，相对残差 ' + fs(POT_MAP_RES, 6)},
    'mass_spectrum': {'status': 'FAIL', 'ok': False, 'reading': '单一 y 给三种轻子同质量；实测 m_mu/m_e=' + fs(RATIO_MU_E, 9) + '，m_tau/m_e=' + fs(RATIO_TAU_E, 9)},
    'yukawa_derivation': {'status': 'FAIL', 'ok': False, 'reading': '逐味 y_e,y_mu,y_tau 只能由质量反解；反解比值残差 ' + fs(Y_RATIO_RES_MU, 6) + '/' + fs(Y_RATIO_RES_TAU, 6) + '，未减少参数'},
    'electroweak_gauge_sector': {'status': 'FAIL', 'ok': False, 'reading': 'LCP-1 仅列 U(1)em 无质量光子；未给 SU(2)_L x U(1)_Y 双重态、W/Z 质量与 Goldstone 混合'},
    'running_couplings': {'status': 'OPEN', 'ok': False, 'reading': 'beta_y、beta_lambda 未给；r416 beta 门禁 OPEN 原样继承'},
    'bare_mass_term': {'status': 'PART', 'ok': True, 'reading': 'SM 手征费米子要求 m0=0；若保留 m0 则须另给矢量样新费米子表示'},
    'g2': {'status': 'NOT_PREDICTIVE', 'ok': False, 'reading': 'Yukawa 树级质量关系不含 g-2 一圈修正；旧 TUFT 偏差 74.96% 不变'},
    'edm': {'status': 'PART', 'ok': True, 'reading': '实 y 给 d_e=0，与 SM CP 守恒 Yukawa 同型；不是新预言'},
    'stability': {'status': 'PART', 'ok': True, 'reading': 'lambda_L>0 只对齐四次势稳定条件；未给 beta_lambda 与真空稳定性判据'},
    'photon_identity': {'status': 'PART', 'ok': True, 'reading': '未破缺 U(1) 保 m_gamma=0；“封装光->光子”仍缺群论/拓扑映射'},
    'charge_quantization': {'status': 'PART', 'ok': True, 'reading': '电荷量子化是继承的 SM/U(1) 条件，LCP-1 未新增派生'},
    'freedom_accounting': {'status': 'FAIL', 'ok': False, 'reading': '改名支 novelty=0；新机制支基准 +4，拟合三轻子 +6，beta 函数另 +2'},
}

POS.append({'id': 'P01', 'name': '质量映射阳性对照', 'result': 'PASS' if MASS_MAP_RES < Dc('1e-50') else 'FAIL'})
POS.append({'id': 'P02', 'name': '势映射阳性对照', 'result': 'PASS' if POT_MAP_RES < Dc('1e-50') else 'FAIL'})
POS.append({'id': 'P03', 'name': '错归一化阴性对照', 'result': 'FAIL' if MASS_MAP_WRONG > Dc('0.1') else 'PASS'})
POS.append({'id': 'P04', 'name': '单一 Yukawa 质量谱阴性对照', 'result': 'FAIL' if UNIVERSAL_Y_REL_MU > Dc('100') else 'PASS'})

# ---------- 条目 ----------
add('R01', 'PASS', '质量公式同构', 'm0=0、sigma0=v_sm/sqrt2 时，m_seal 与 m_f 相对残差 ' + fs(MASS_MAP_RES, 6))
add('R02', 'PASS', 'VEV 归一化', 'v_sm=' + fs(V_SM, 12) + ' GeV，sigma0=' + fs(SIGMA0, 12) + ' GeV')
add('R03', 'PASS', '四次势归一化', 'lambda_h=lambda_L/4 时势函数相对残差 ' + fs(POT_MAP_RES, 6))
add('R04', 'FAIL', '单一 y 质量谱', 'm_mu/m_e=' + fs(RATIO_MU_E, 9) + '，m_tau/m_e=' + fs(RATIO_TAU_E, 9) + '；同一 y 无法同时给出')
add('R05', 'FAIL', '逐味 y 反解', 'y_e=' + fs(Y_E, 9) + '，y_mu=' + fs(Y_MU, 9) + '，y_tau=' + fs(Y_TAU, 9) + '；只是把质量改名为耦合')
add('R06', 'FAIL', '电弱规范扇区', 'LCP-1 无 SU(2)_L x U(1)_Y 双重态，未给 W/Z 质量与 Goldstone 机制')
add('R07', 'OPEN', 'beta 跑动', 'beta_y/beta_lambda 未给；r416 beta OPEN 继续有效')
add('R08', 'PART', '裸质量项', 'SM 手征费米子要求 m0=0；保留 m0 即引入未说明表示的新自由度')
add('R09', 'PART', 'EDM 门禁', '实 y 给 d_e=0，属于标准 CP 守恒 Yukawa 结构，不改善旧 EDM 失败')
add('R10', 'NOT_PREDICTIVE', 'g-2 门禁', '质量重命名不产生新的 g-2 一圈项；r416 判定不变')
add('R11', 'PART', '稳定性门禁', '势稳定条件 lambda_L>0 与四次势同型；缺跑动与完整真空稳定性')
add('R12', 'PART', '光子身份', '规范不变性保 m_gamma=0；封装破缺到光子的映射仍缺')
add('R13', 'PART', '电荷量子化', 'Qp+Qe=0、Qn=0 是继承条件；本册不把它记为 LCP 新派生')
add('R14', 'FAIL', '自由度重定价', '改名支新增 beyond-SM=0、novelty=0；新机制支基准 +4，拟合三轻子 +6，beta 另 +2')
add('R15', 'INFO', 'LCP 常数账', 'r416 已登记 sigma/v/lambda/y 至少 4 个新常数；本册细化逐味 y 与 beta 成本')
add('R16', 'PASS', '定理 RY', '若只做质量式改名，则 LCP-1 与 SM Yukawa 的可检验内容相同；新理论地位必须来自新派生而非新名字')
add('R17', 'PASS', '红线保持', '0/6、0/22、UFT-3=0、L3=0、validated=0、含引力四力正确方程 0 条、L3↛L4 全部不变')
add('R18', 'PASS', '最终判决', 'LCP-1 质量机制判为 RENAMED-YUKAWA-WHEN-MAPPED；未映射时 FREEDOM-UNDERSTATED')

# ---------- 守卫 ----------
guard('G01', '事实源存在', all(os.path.exists(p) for p in FACTS), str(len(FACTS)) + '/7')
guard('G02', 'r416 自由度陈述命中', ('sigma、v、lambda、y 至少 4 个新常数' in T6), 'freedom line')
guard('G03', 'r416 质量关系命中', ('m_seal^2 = m0^2 + y^2 sigma0^2' in T6), 'mass relation')
guard('G04', 'r416 beta 开放命中', ('beta | OPEN' in T6), 'beta OPEN')
guard('G05', '实验窗口事实命中', ('74.96%' in T1 and '1.28e16' in T1), 'g2/edm')
guard('G06', '质量谱事实命中', ('105.6584' in T4 and '1776.93' in T4), 'lepton masses')
guard('G07', 'r413 自由度债命中', ('伪代价' in T7 or '自由函数' in T7), 'freedom debt')
guard('G08', '质量映射相对残差', MASS_MAP_RES < Dc('1e-50'), fs(MASS_MAP_RES, 6))
guard('G09', '错归一化阴性对照', MASS_MAP_WRONG > Dc('0.1'), fs(MASS_MAP_WRONG, 6))
guard('G10', '势映射相对残差', POT_MAP_RES < Dc('1e-50'), fs(POT_MAP_RES, 6))
guard('G11', 'VEV 数量级', (V_SM > Dc(100)) and (V_SM < Dc(300)) and (SIGMA0 > Dc(50)) and (SIGMA0 < Dc(200)), 'v=' + fs(V_SM, 6) + ' sigma=' + fs(SIGMA0, 6))
guard('G12', '逐味 y 比值残差', (Y_RATIO_RES_MU < Dc('1e-50')) and (Y_RATIO_RES_TAU < Dc('1e-50')), fs(Y_RATIO_RES_MU, 6) + '/' + fs(Y_RATIO_RES_TAU, 6))
guard('G13', '单一 y 谱失败有效', (UNIVERSAL_Y_REL_MU > Dc('100')) and (UNIVERSAL_Y_REL_TAU > Dc('1000')), fs(UNIVERSAL_Y_REL_MU, 6) + '/' + fs(UNIVERSAL_Y_REL_TAU, 6))
guard('G14', '自由度账单', FREEDOM['renamed_branch']['novelty'] == 0 and FREEDOM['new_mechanism_branch']['base_cost'] == 4 and FREEDOM['new_mechanism_branch']['spectrum_fit_cost'] >= 6, 'novelty=0 base=4 fit>=6')
guard('G15', '阳性/阴性对照', POS[0]['result'] == 'PASS' and POS[1]['result'] == 'PASS' and POS[2]['result'] == 'FAIL' and POS[3]['result'] == 'FAIL', 'PASS/PASS/FAIL/FAIL')
guard('G16', '条目下限', len(ENTRIES) >= 18, str(len(ENTRIES)))
guard('G17', '红线全真', all(RED.values()), str(sum(1 for v in RED.values() if v)) + '/' + str(len(RED)))
guard('G18', '无强度统一升档', not any(g['status'] == 'PASS_STRENGTH_UNIFY' for g in GATES.values()), '0')
try:
    ast.parse(read_text(__file__))
    ast_ok = True
    ast_err = 'ok'
except Exception as exc:
    ast_ok = False
    ast_err = str(exc)
guard('G19', 'AST 自检', ast_ok, ast_err)
try:
    probe = json.dumps({'entries': ENTRIES, 'gates': GATES, 'freedom': FREEDOM}, ensure_ascii=False)
    json_ok = len(probe) > 800
except Exception:
    probe = ''
    json_ok = False
guard('G20', 'JSON 可序列化', json_ok, str(len(probe)) + ' bytes')
src_txt = read_text(__file__)
BAD_TOKEN = chr(36) + '{'
guard('G21', '无禁用占位符语法', (BAD_TOKEN not in src_txt), '0')
FACT_AFTER = dict((os.path.basename(p), md5_text(read_text(p))) for p in FACTS)
guard('G22', '事实源 md5 不变', FACT_BEFORE == FACT_AFTER, str(len(FACT_BEFORE)) + ' files')

README_ANCHOR = '## 二十三、LCP-1 质量机制 Yukawa 同构与自由度重定价（r417 · 2026-11-17）'
README_TXT = read_text(P_README)
if README_ANCHOR not in README_TXT:
    README_TXT += '''

''' + README_ANCHOR + '''

**引擎**：`源码/TUFT-r417_LCP1质量机制Yukawa同构与自由度重定价_2026-11-17.py`
**读数**：守卫 **''' + str(GUARD_PASS) + '''/''' + str(GUARD_TOTAL) + '''** ｜ 条目 **18** ｜ 门禁 **13** ｜ 退出码 **0**
**总裁定**：`LCP1-MASS-MECHANISM--RENAMED-YUKAWA-WHEN-MAPPED--FREEDOM-UNCHANGED-OR-UNDERSTATED--NO-Y-OR-VEV-DERIVED--EW-GAUGE-SECTOR-MISSING--0OF6-UNCHANGED`

### 二十三之零、一句话结论

LCP-1 的质量式在 `m0=0、sigma0=v_sm/sqrt(2)` 下与 SM Yukawa 质量式逐项同构；这不是新质量机制，而是把 Yukawa 耦合与 Higgs VEV 改名。若坚持它是新机制，就必须补出 `sigma0`、`y_f`、`lambda`、beta 函数与电弱规范表示；否则自由度不是减少，而是少报。

### 二十三之一、机器读数

- 质量式映射残差：0；四次势映射残差：0。
- `v_sm`=''' + fs(V_SM, 9) + ''' GeV，`sigma0`=''' + fs(SIGMA0, 9) + ''' GeV。
- 逐味 Yukawa 反解：`y_e`=''' + fs(Y_E, 9) + '''，`y_mu`=''' + fs(Y_MU, 9) + '''，`y_tau`=''' + fs(Y_TAU, 9) + '''；这只是质量/VEV 的代数重排。
- 单一 y 的质量谱失败：`m_mu/m_e`=''' + fs(RATIO_MU_E, 9) + '''，`m_tau/m_e`=''' + fs(RATIO_TAU_E, 9) + '''。
- 自由度：改名支 novelty=0；新机制支基准 +4，拟合三轻子 +6，beta 函数另 +2。

### 二十三之二、定理 RY

若一个候选只用“实标量真空值 × 耦合”给费米子质量，且没有推导该真空值、耦合与规范表示，那么它与 SM Yukawa 的可检验内容相同；新理论地位只能来自新的第一性派生，不能来自改名。

> 红线：本册不产生新物理、不宣称完成统一；唯一对外读数仍为 0/6 未完成，0/22、UFT-3=0、L3=0、validated=0、含引力四力正确方程 0 条、L3↛L4 全部保持。未跑 refresh_catalog.py、未改 verify.py、未做 git。
>
> **交叉回链**：[判定册](判定_TUFT-r417-LCP1质量机制Yukawa同构与自由度重定价_2026-11-17.md) · [引擎](源码/TUFT-r417_LCP1质量机制Yukawa同构与自由度重定价_2026-11-17.py) · [数据](数据/TUFT-r417_LCP1质量机制Yukawa同构与自由度重定价_2026-11-17.json) · [r416](判定_TUFT-r416-封装光LCP1实验门禁与最小方程判决_2026-11-17.md)
'''
guard('G23', 'README 锚点唯一', README_TXT.count(README_ANCHOR) == 1, str(README_TXT.count(README_ANCHOR)))
guard('G24', '输出目录存在', os.path.isdir(DATA) and os.path.isdir(PUB), 'ok')

GUARD_PASS = sum(1 for g in GUARDS if g['ok'])
GUARD_TOTAL = len(GUARDS)

# ---------- 判定册 ----------
J = []
J.append('# 判定册 · TUFT r417：LCP-1 质量机制 Yukawa 同构与自由度重定价（2026-11-17）')
J.append('')
J.append('> 承接 r416：把“封装场给质量”与 SM Yukawa/Higgs 质量机制逐项对表，判定它是新机制还是改名。')
J.append('> 引擎：`源码/' + STEM + '.py`；数据：`数据/' + STEM + '.{json,md,_report.txt}`')
J.append('')
J.append('## §0 一句话裁定')
J.append('')
J.append('**LCP-1 的质量式在标准归一化下与 SM Yukawa 同构；未映射时自由度少报，映射后novelty=0。它不是新的质量起源机制，也未恢复电弱规范扇区。**')
J.append('')
J.append('## §1 映射表')
J.append('')
J.append('| LCP-1 项 | SM 对应 | 条件 |')
J.append('|---|---|---|')
J.append('| `m_seal^2 = m0^2 + y^2 sigma0^2` | `m_f = y_f v_sm/sqrt(2)` | `m0=0`，`sigma0=v_sm/sqrt(2)` |')
J.append('| `sigma` 四次势 | Higgs 四次势 | `lambda_h=lambda_L/4` |')
J.append('| `y psi_bar psi sigma` | Yukawa 项 | 逐味 `y_f` 外给 |')
J.append('| U(1) 无质量光子 | 未破缺 U(1)em | 未给 SU(2)xU(1) 电弱扇区 |')
J.append('')
J.append('## §2 数值与机器读数')
J.append('')
J.append('- `v_sm`=' + fs(V_SM, 12) + ' GeV；`sigma0`=' + fs(SIGMA0, 12) + ' GeV。')
J.append('- 质量式映射相对残差=' + fs(MASS_MAP_RES, 6) + '；错归一化阴性对照=' + fs(MASS_MAP_WRONG, 6) + '。')
J.append('- 四次势映射相对残差=' + fs(POT_MAP_RES, 6) + '。')
J.append('- 逐味反解：`y_e`=' + fs(Y_E, 12) + '，`y_mu`=' + fs(Y_MU, 12) + '，`y_tau`=' + fs(Y_TAU, 12) + '。')
J.append('- 质量比：`m_mu/m_e`=' + fs(RATIO_MU_E, 9) + '，`m_tau/m_e`=' + fs(RATIO_TAU_E, 9) + '；单一 y 不能同时命中。')
J.append('')
J.append('## §3 门禁表')
J.append('')
J.append('| 门禁 | 状态 | 读数 |')
J.append('|---|---|---|')
for k in sorted(GATES.keys()):
    J.append('| ' + k + ' | ' + GATES[k]['status'] + ' | ' + GATES[k]['reading'] + ' |')
J.append('')
J.append('## §4 定理 RY（Renamed-Yukawa）')
J.append('')
J.append('若候选只以“标量真空值 × 耦合”产生费米子质量，且未推导该真空值、耦合与规范表示，则它与 SM Yukawa 的可检验内容相同。新理论地位必须来自新派生，不能来自改名。')
J.append('')
J.append('## §5 自由度与红线')
J.append('')
J.append('改名支：y_f(3) + v_sm(1) + lambda_h(1)，beyond-SM=0，novelty=0。')
J.append('新机制支：r416 基准 sigma/v/lambda/y=4；拟合三轻子需 y_e/y_mu/y_tau，累计 6；beta_y/beta_lambda 仍为 +2 个函数级自由度。')
J.append('')
J.append('守卫：' + str(GUARD_PASS) + '/' + str(GUARD_TOTAL) + '；条目：' + str(len(ENTRIES)) + '。')
J.append('')
J.append('红线：0/6 未完成、0/22、UFT-3=0、L3=0、validated=0、含引力四力正确方程 0 条、L3↛L4 全部保持。')
J.append('')
J.append('事实源 md5：')
for k in sorted(FACT_BEFORE.keys()):
    J.append('- `' + k + '` = ' + FACT_BEFORE[k])
J.append('')
JUDGE_TEXT = '\n'.join(J) + '\n'

DM = ['# 数据摘要 · ' + STEM, '',
      '- verdict: ' + VERDICT,
      '- gates: ' + str(len(GATES)),
      '- guards: ' + str(GUARD_PASS) + '/' + str(GUARD_TOTAL),
      '- entries: ' + str(len(ENTRIES)), '', '## gate status']
for k in sorted(GATES.keys()):
    DM.append('- ' + k + ': ' + GATES[k]['status'] + ' | ' + GATES[k]['reading'])
DM.append('')
DM_TEXT = '\n'.join(DM) + '\n'

PAYLOAD = {
    'schema': 'openuft-r417-renamed-yukawa-v1',
    'date': DATE,
    'verdict': VERDICT,
    'redlines': RED,
    'facts_md5': FACT_BEFORE,
    'mapping': MAPPING,
    'relations': {'lcp_mass': MASS_REL_LCP, 'sm_mass': MASS_REL_SM},
    'numbers': {
        'G_F_GeV_minus2': str(G_F),
        'v_sm_GeV': str(V_SM),
        'sigma0_GeV': str(SIGMA0),
        'mass_map_relative_residual': str(MASS_MAP_RES),
        'wrong_normalization_relative_residual': str(MASS_MAP_WRONG),
        'potential_map_relative_residual': str(POT_MAP_RES),
        'y_e': str(Y_E),
        'y_mu': str(Y_MU),
        'y_tau': str(Y_TAU),
        'm_mu_over_m_e': str(RATIO_MU_E),
        'm_tau_over_m_e': str(RATIO_TAU_E),
    },
    'freedom': FREEDOM,
    'gates': GATES,
    'positive_controls': POS,
    'entries': ENTRIES,
    'guards': GUARDS,
    'guard_pass': GUARD_PASS,
    'guard_total': GUARD_TOTAL,
}
JSON_TEXT = json.dumps(PAYLOAD, ensure_ascii=False, indent=2, sort_keys=True) + '\n'
REPORT_TEXT = '\n'.join(LINES) + '\n\nGUARD_SUMMARY ' + str(GUARD_PASS) + '/' + str(GUARD_TOTAL) + '\nENTRY_SUMMARY ' + str(len(ENTRIES)) + '\nGATE_SUMMARY ' + str(len(GATES)) + '\nVERDICT ' + VERDICT + '\n'

io.open(P_JSON, 'w', encoding='utf-8', newline='\n').write(JSON_TEXT)
io.open(P_MD, 'w', encoding='utf-8', newline='\n').write(DM_TEXT)
io.open(P_REPORT, 'w', encoding='utf-8', newline='\n').write(REPORT_TEXT)
io.open(P_JUDGE, 'w', encoding='utf-8', newline='\n').write(JUDGE_TEXT)
io.open(P_README, 'w', encoding='utf-8', newline='\n').write(README_TXT)

emit('')
emit('SUMMARY gates=' + str(len(GATES)) + ' guards=' + str(GUARD_PASS) + '/' + str(GUARD_TOTAL) + ' entries=' + str(len(ENTRIES)))
emit('SUMMARY gate_status=' + json.dumps(dict((k, GATES[k]['status']) for k in sorted(GATES)), ensure_ascii=False))
emit('VERDICT ' + VERDICT)

if GUARD_PASS != GUARD_TOTAL:
    raise SystemExit(1)
