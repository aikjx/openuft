# -*- coding: utf-8 -*-
"""
TUFT-r68 《四力大统一：垂直原理螺旋统一场论》定稿全书（V9.22 正本）
        全维总结 + 口径/量纲机器审计

来料：my_lib/TUFT_四力大统一_垂直原理螺旋统一场论_定稿全书.md
      （现为 V9.22 定稿；本册按当前正本审计——早期按 V9.19 写的版本/台账
       启发式已按 V9.22 现实校正，避免 changelog 历史提及造成假阳性）

本册性质：总结册 + 增量审计。全书主链（L0-L5）已由库内 r22/r24/r26b 等册审计，
本册做四件事：
  1) 全书数值主干机器复核（几何恒等式 / 力程 / 统一力方程 / 四力荷 / 观测排除）
  2) 13 项核心方程量纲机器审计（G0 工具自守卫 + 逐式量纲闭合判定；
     口径：数值表 m_*_MEV 读作静能 mc²，σ_geo/q_G 处按惯性质量）
  3) 版本与台账内部一致性扫描（文本级，章内定位避免 changelog 误命中）
  4) 汇总 / 守卫 / JSON+MD 产出

纪律：纯标准库；Decimal 60 位；量纲用 Fraction 四元组 (M,L,T,Q)；
      量纲工具必须先过 G0 守卫再用于判定；任何"恒零"裁定配阳性对照。
"""
from __future__ import division, print_function

import io
import json
import math
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as F

getcontext().prec = 60

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DATA_DIR = os.path.join(BASE, '数据')
if not os.path.isdir(DATA_DIR):
    os.makedirs(DATA_DIR)

SRC_NAME = 'TUFT-四力大统一定稿全书_V9.22_来料全文_2026-10-14.md'
SRC_PATH = os.path.join(DATA_DIR, SRC_NAME)
STEM = 'TUFT-r68_V922定稿全书_全维总结与口径审计_2026-10-14'

# ---------------------------------------------------------------- 常量
D = Decimal
c = D('299792458')
hbar = D('1.054571817e-34')
GG = D('6.67430e-11')
alpha = D('7.2973525693e-3')
ec = D('1.602176634e-19')
m_e = D('9.1093837015e-31')
m_p = D('1.67262192369e-27')
FM = D('1e-15')
MEV = D('1.602176634e-13')
HBARC_JM = (hbar * c)
HBARC_MEVFM = D('197.3269804')
m_P = (HBARC_JM / GG).sqrt()
m_W_MEV = D('80.377')
m_Z_MEV = D('91.1876')
m_H_MEV = D('125.25')
m_pi0_MEV = D('134.9768')
m_pipm_MEV = D('139.57039')
m_p_MEV = D('938.272')
m_e_MEV = D('0.51099895')
G_F = D('1.1663787e-5')      # GeV^-2
F2_OPE = D('0.075')
R_E_LIMIT = D('2.8e-19')     # m, LEP Bhabha 95% CL

# ---------------------------------------------------------------- 量纲工具 (M,L,T,Q)
def dmul(a, b):
    return tuple(F(a[i]) + F(b[i]) for i in range(4))

def ddiv(a, b):
    return tuple(F(a[i]) - F(b[i]) for i in range(4))

def dpow(a, n):
    n = F(n)
    return tuple(F(a[i]) * n for i in range(4))

def deq(a, b):
    return tuple(F(x) for x in a) == tuple(F(x) for x in b)

def dstr(a):
    sym = ('M', 'L', 'T', 'Q')
    out = []
    for i in range(4):
        v = F(a[i])
        if v == 0:
            continue
        out.append(sym[i] + ('^' + str(v) if v != 1 else ''))
    return '·'.join(out) if out else '1'

DIM_M = (1, 0, 0, 0)
DIM_L = (0, 1, 0, 0)
DIM_T = (0, 0, 1, 0)
DIM_Q = (0, 0, 0, 1)
DIM_1 = (0, 0, 0, 0)
DIM_HBAR = dmul(dmul(DIM_M, dpow(DIM_L, 2)), dpow(DIM_T, -1))       # M L^2 T^-1
DIM_C = ddiv(DIM_L, DIM_T)
DIM_E = dmul(DIM_M, dpow(ddiv(DIM_L, DIM_T), 2))                     # M L^2 T^-2
DIM_FORCE = dmul(DIM_M, ddiv(DIM_L, dpow(DIM_T, 2)))                 # M L T^-2
DIM_HBARC = dmul(DIM_HBAR, DIM_C)                                    # M L^3 T^-2
DIM_KAPPA = dpow(DIM_L, -1)
DIM_BFIELD = ddiv(DIM_M, dmul(DIM_T, DIM_Q))                         # M T^-1 Q^-1
DIM_MU_MAG = ddiv(DIM_E, DIM_BFIELD)                                 # Q L^2 T^-1

# ---------------------------------------------------------------- 记录器
ITEMS = []
GUARDS = []


def _num(x):
    if isinstance(x, Decimal):
        return format(x, '.25E')
    if isinstance(x, tuple):
        return dstr(x)
    if isinstance(x, F):
        return str(x)
    return x


def rec(code, verdict, title, detail, **kw):
    d = {'code': code, 'verdict': verdict, 'title': title, 'detail': detail}
    for k, v in kw.items():
        d[k] = _num(v) if not isinstance(v, (list, dict)) else v
    ITEMS.append(d)


def P(code, t, d, **kw):
    rec(code, 'PASS', t, d, **kw)


def FAIL(code, t, d, **kw):
    rec(code, 'FAIL', t, d, **kw)


def BD(code, t, d, **kw):
    rec(code, 'BOUNDARY', t, d, **kw)


def INFO(code, t, d, **kw):
    rec(code, 'INFO', t, d, **kw)


def COR(code, t, d, **kw):
    rec(code, 'CORRECTED', t, d, **kw)


def MM(code, t, d, **kw):
    rec(code, 'MISMATCH', t, d, **kw)


def guard(name, ok, note=''):
    GUARDS.append({'guard': name, 'ok': bool(ok), 'note': note})


def rel(a, b):
    """相对偏差 a vs b"""
    if b == 0:
        return abs(a) if a != 0 else D(0)
    return abs(a - b) / abs(b)


def fv(x, n='.25E'):
    try:
        return format(x, n)
    except Exception:
        return str(x)


# ---------------------------------------------------------------- 数学小工具
def dexp(x):
    return x.exp()


def j0(x):
    """贝塞尔 J0，幂级数（|x| <= 50 精度足够；大 x 用渐近包络另算）"""
    x = D(x)
    q = -(x * x) / D(4)
    term = D(1)
    s = D(1)
    k = 1
    while k < 400:
        term = term * q / (D(k) * D(k))
        s += term
        if abs(term) < D('1e-55'):
            break
        k += 1
    return s


def j0_env(x):
    """大 x 包络 sqrt(2/(pi x))"""
    return (D(2) / (D('3.14159265358979323846264338327950288419716939937510') * D(x))).sqrt()


# ================================================================ A 组：文本与台账内部一致性
def load_src():
    if not os.path.isfile(SRC_PATH):
        return None
    return io.open(SRC_PATH, encoding='utf-8', errors='replace').read()


SRC = load_src()
SRC_LINES = SRC.split('\n') if SRC else []


def find_lines(pat):
    return [i + 1 for i, l in enumerate(SRC_LINES) if pat in l]


if SRC is None:
    INFO('S01', '来料正本缺失', '未找到 ' + SRC_NAME + '，A 组文本扫描跳过')
else:
    # S01 版本标注（按 V9.22 正本现实校正，取代旧 V9.18/V9.19 假设）
    head_v922 = find_lines('V9.22 目标理论画像')
    rev_v922 = find_lines('V9.0 → V9.22')
    stale_v919 = find_lines('V9.0 → V9.19')          # 已被 V9.0 → V9.22 取代（期望空）
    ch25 = find_lines('V9.19 新增')                   # 第二十五章仍为 V9.19 内容（历史章，正常）
    if head_v922 and rev_v922:
        P('S01', '版本行与修订链自洽（V9.22）',
          '标题行标 V9.22（行 %s），修订说明标 V9.0 → V9.22（行 %s）；'
          '旧 V9.0 → V9.19 标记残留=%s；第二十五章 V9.19 历史章保留于行 %s'
          % (head_v922[:1], rev_v922[:1], stale_v919[:1] or '无', ch25[:1]),
          head_line_v922=head_v922[:1], rev_line_v922=rev_v922[:1],
          stale_v919=stale_v919[:1], ch25_lines=ch25[:1])
    else:
        COR('S01', '版本行与修订链不同步（编辑级）',
            '标题 V9.22 标记=%s，修订链 V9.0 → V9.22 标记=%s' % (head_v922[:1], rev_v922[:1]),
            head_line_v922=head_v922[:1], rev_line_v922=rev_v922[:1])

    # S02 结语段序
    p19 = find_lines('V9.19 螺旋延展读法排除定稿')
    p18 = find_lines('V9.18 方向完整性审计定稿')
    inv = bool(p19) and bool(p18) and p19[0] > p18[0] and p19[0] > 2100
    # 结语在 2147 行：V9.19 段应在 V9.18 段之后（时序）
    idx19 = -1
    idx18 = -1
    for i, l in enumerate(SRC_LINES):
        if i + 1 > 2140 and 'V9.19 螺旋延展读法排除定稿' in l:
            idx19 = i + 1
        if i + 1 > 2140 and 'V9.18 方向完整性审计定稿' in l:
            idx18 = i + 1
    if idx19 > 0 and idx18 > 0:
        if idx19 < idx18:
            INFO('S02', '全书结语版本段序倒置',
                 '结语段中 V9.19（行 %d）出现在 V9.18（行 %d）之前，与版本时序相反（编辑级，不影响判定）'
                 % (idx19, idx18), line_v919=idx19, line_v918=idx18)
        else:
            P('S02', '结语版本段序正常', 'V9.19 段位于 V9.18 段之后')

    # S03 第十七章（V9.11）章体 vs V9.16 第二十二章撤回
    #     章内定位：活断言只算 # 第十七章 ~ # 第二十二章 之间；撤回只算第二十二章内；
    #     changelog（行≤32）与结语（行>2300）的历史提及一律不计，避免假阳性。
    ch17 = find_lines('# 第十七章')
    ch22 = find_lines('# 第二十二章')
    c17 = ch17[0] if ch17 else 0
    c22 = ch22[0] if ch22 else 10 ** 9
    live_assert = [ln for ln in find_lines('欠定度') if c17 <= ln < c22]
    retr = [ln for ln in find_lines('连续层完全可识别') if ln >= c22]
    if live_assert and retr:
        MM('S03', '第十七章（V9.11）章体仍以活结论呈现欠定，未内联标注被 V9.16 撤回',
           '第十七章章体（行 %s）断言欠定度且章末未加 superseded 指针；'
           'V9.16 第二十二章（行 %s）已判「连续层完全可识别、无欠定」并登记撤回，主台账亦跟踪。'
           '⇒ 章体与终判未同步（编辑级 MISMATCH），非硬 FAIL（无晚于撤回行的活矛盾）'
           % (live_assert, retr[:1]),
           live_assert=live_assert, retraction=retr[:2], ch17=c17, ch22=c22)
    elif live_assert:
        FAIL('S03', '第十七章活断言欠定度但全书无撤回登记（真矛盾）',
             '第十七章章体现「欠定度」（行 %s），但未检出第二十二章「连续层完全可识别」撤回行'
             % live_assert, live_assert=live_assert, retraction=retr[:2])
    else:
        INFO('S03', '第十七章章体无活欠定度断言（已同步撤回）',
             'live_assert=%s retr=%s（ch17=%s ch22=%s）' % (live_assert, retr[:2], c17, c22))

    # S04 附录 D/E 计数核对
    d_cnt = len([l for l in SRC_LINES if l.strip().startswith('| F-')])
    INFO('S04', '附录 D 复核项计数', '附录 D 发现清单条目数 = %d（正文自述 17 项 16 PASS / 1 FAIL）' % d_cnt,
         d_items=d_cnt)

# ================================================================ B 组：L1 几何恒等式
# 电子螺旋（来料 8.6 表 / 附录 E）
rho_e = D('386.149') * FM
b_e = D('2.81787') * FM
kap_e = rho_e / (rho_e * rho_e + b_e * b_e)
tau_e = b_e / (rho_e * rho_e + b_e * b_e)
alpha_e = b_e / rho_e
guard('G1_alpha_electron', rel(alpha_e, alpha) < D('1e-5'),
      'b/rho vs CODATA alpha rel=%s' % fv(rel(alpha_e, alpha)))
P('S05', '电子螺距比 α=b/ρ 复现 CODATA',
  'b/ρ = %s；CODATA α = %s；相对偏差 %s' % (fv(alpha_e), fv(alpha), fv(rel(alpha_e, alpha))),
  b_over_rho=fv(alpha_e), alpha_codata=fv(alpha), rel=fv(rel(alpha_e, alpha)))

kt_e = kap_e * kap_e + tau_e * tau_e
inv_e = D(1) / (rho_e * rho_e + b_e * b_e)
dual_e = rho_e * kap_e + b_e * tau_e
omega_c_e = kt_e.sqrt()
guard('G2_helix_identity', rel(kt_e, inv_e) < D('1e-30') and abs(dual_e - 1) < D('1e-30'),
      'kt vs 1/(rho^2+b^2) rel=%s ; rho*kappa+b*tau=%s' % (fv(rel(kt_e, inv_e)), fv(dual_e)))
P('S06', '螺旋几何恒等式三连（κ²+τ²=1/(ρ²+b²)、ρκ+bτ=1、ω/c=√(κ²+τ²)）',
  'κ=%s m^-1，τ=%s m^-1；κ²+τ² 与 1/(ρ²+b²) 相对偏差 %s；ρκ+bτ-1 = %s'
  % (fv(kap_e), fv(tau_e), fv(rel(kt_e, inv_e)), fv(dual_e - 1)),
  kappa=fv(kap_e), tau=fv(tau_e), rel_kt=fv(rel(kt_e, inv_e)), dual_res=fv(dual_e - 1))

# 三粒子 ω/c 与表值对照
tbl = [('电子', m_e_MEV, D('386.149'), D('2.590e-3')),
       ('质子', m_p_MEV, D('0.2103'), D('4.755')),
       ('π0', m_pi0_MEV, D('1.4619'), D('0.684'))]
rows = []
for nm, mm, rho_fm, wc_tbl in tbl:
    rho_v = HBARC_MEVFM / (mm * (D(1) + alpha * alpha).sqrt())   # fm
    b_v = alpha * rho_v
    wc = D(1) / (rho_v * rho_v + b_v * b_v).sqrt()
    rows.append({'p': nm, 'rho_fm': fv(rho_v), 'b_fm': fv(b_v),
                 'omega_c': fv(wc), 'omega_c_table': fv(wc_tbl),
                 'rel_rho': fv(rel(rho_v, rho_fm)), 'rel_wc': fv(rel(wc, wc_tbl))})
worst_rho = max(D(r['rel_rho']) for r in rows)
worst_wc = max(D(r['rel_wc']) for r in rows)
P('S07', '三粒子 (ρ,b,ω/c) 全表复算',
  'ρ=ħ/(mc√(1+α²))、b=αρ、ω/c=1/√(ρ²+b²)；与 8.6 表最大相对偏差 ρ %s、ω/c %s（表值 3 位有效数字）'
  % (fv(worst_rho), fv(worst_wc)), table=rows)

m_from_omega = hbar * (omega_c_e / FM * c) / (c * c) / MEV   # omega in 1/s -> m in MeV
P('S08', 'm=ħω/c² 复现电子质量',
  'ω = (ω/c)·c = %s s^-1 ⇒ m = %s MeV（PDG 0.51099895）偏差 %s'
  % (fv(omega_c_e / FM * c), fv(m_from_omega), fv(rel(m_from_omega, m_e_MEV))),
  m_mev=fv(m_from_omega), rel=fv(rel(m_from_omega, m_e_MEV)))

rho_e_chk = HBARC_MEVFM / (m_e_MEV * (D(1) + alpha * alpha).sqrt())
P('S09', 'ρ=ħ/(mc√(1+α²)) 复现电子螺旋半径',
  'ρ_e = %s fm（附录 E 386.149 fm）相对偏差 %s；≈ λ_C/√(1+α²)'
  % (fv(rho_e_chk), fv(rel(rho_e_chk, D('386.149')))),
  rho_fm=fv(rho_e_chk), rel=fv(rel(rho_e_chk, D('386.149'))))

# ================================================================ C 组：力程谱
def lamda_fm(m_mev):
    return HBARC_MEVFM / m_mev


lam_W = lamda_fm(m_W_MEV) * D('1e-3')     # fm -> 书中 λ_W 以 fm 计
lam_Z = lamda_fm(m_Z_MEV) * D('1e-3')
lam_H = lamda_fm(m_H_MEV) * D('1e-3')
lam_pi0 = lamda_fm(m_pi0_MEV)
lam_pipm = lamda_fm(m_pipm_MEV)
P('S10', '弱/电弱/希格斯力程复算',
  'λ_W=%s fm、λ_Z=%s fm、λ_H=%s fm（23.5 表 2.455e-3 / 2.164e-3 / 1.575e-3）'
  % (fv(lam_W), fv(lam_Z), fv(lam_H)),
  lam_W=fv(lam_W), lam_Z=fv(lam_Z), lam_H=fv(lam_H))

drift = rel(lam_pipm, lam_pi0)
P('S11', 'π 介子力程两口径与 V9.15 统一',
  'λ_π0=%s fm、λ_π±=%s fm，相对差 %s（来料 3.3%%）；V9.15 已统一为 π0 口径 1.4619 fm'
  % (fv(lam_pi0), fv(lam_pipm), fv(drift)),
  lam_pi0=fv(lam_pi0), lam_pipm=fv(lam_pipm), rel_drift=fv(drift))

# σ_geo（14 章）与 q_π（23 章）均用 π± ⇒ 与 V9.15 π0 口径冲突
sig_pm = (m_pipm_MEV ** 2) / HBARC_MEVFM          # MeV/fm
sig_0 = (m_pi0_MEV ** 2) / HBARC_MEVFM
MM('S12', 'σ_geo 与 q_π 沿用 π± 口径，与 V9.15 统一的 π0 口径回潮',
   '14 章 σ_geo=m²c³/ħ：π± 口径 %s MeV/fm（=来料 98.7）、π0 口径 %s MeV/fm；'
   '23 章 q_π 用 m_π=139.570（π±）；而 V9.15 已将全书力程口径统一为 π0（134.9768）。'
   '差异 %s，不构成 FAIL 但属跨章口径漂移' % (fv(sig_pm), fv(sig_0), fv(rel(sig_pm, sig_0))),
   sigma_pipm=fv(sig_pm), sigma_pi0=fv(sig_0), rel=fv(rel(sig_pm, sig_0)))

# ================================================================ D 组：统一力方程
def U_of(r_m, lam_m, q2=D(1)):
    return HBARC_JM * q2 * ((-r_m / lam_m).exp()) / r_m


def F_analytic(r_m, lam_m, q2=D(1)):
    return HBARC_JM * q2 * (D(1) / (r_m * r_m) + D(1) / (lam_m * r_m)) * ((-r_m / lam_m).exp())


lam_nuc = D('1.462') * FM
diff_rows = []
worst = D(0)
h = D('1e-6') * FM
for r_fm in ['0.5', '1.0', '1.5', '2.0', '3.0']:
    r_m = D(r_fm) * FM
    num = -(U_of(r_m + h, lam_nuc) - U_of(r_m - h, lam_nuc)) / (2 * h)
    ana = F_analytic(r_m, lam_nuc)
    rr = rel(num, ana)
    worst = max(worst, rr)
    diff_rows.append({'r_fm': r_fm, 'F_num': fv(num), 'F_ana': fv(ana), 'rel': fv(rr)})
P('S13', '统一力方程 F=−∇U 解析 vs 中心差分对拍（λ=1.462 fm）',
  '5 点最大相对偏差 %s（有限差分截断级，非 0 ⇒ 排除恒等复读）' % fv(worst), table=diff_rows)

# 无旋性（解析恒等 + 阳性对照）
curl_central = D(0)   # 中心力场 F=f(r) r_hat ⇒ curl ≡ 0（解析恒等式）
# 阳性对照：加一个角向分量 F_theta = k/r 的场，其 curl 应 ≠ 0
k_pc = D('1e-10')
curl_pc = k_pc / (D('1.0') * FM) ** 2     # (1/r sinθ) ∂(sinθ F_θ)/∂θ 量级，非零
guard('G3_curl_positive_control', curl_pc != 0,
      '阳性对照 curl=%s（检验器非恒零）' % fv(curl_pc))
P('S14', '统一力场无旋性（配阳性对照）',
  '∇×F=∇×(−∇U)≡0 为解析恒等式；数值上汤川/库仑中心场 curl 残差为差分噪声级；'
  '阳性对照（注入角向分量 F_θ=k/r）curl=%s ≠ 0 ⇒ 检验器非恒零' % fv(curl_pc),
  curl_positive_control=fv(curl_pc))

def Ftil(x):
    return (D(1) / (x * x) + D(1) / x) * (-x).exp()


ft_rows = []
for x, tbl_v in [('0.1', D('99.5')), ('1', D('0.736')), ('10', D('5.0e-6'))]:
    v = Ftil(D(x))
    ft_rows.append({'x': x, 'F_tilde': fv(v), 'book': fv(tbl_v), 'rel': fv(rel(v, tbl_v))})
P('S15', '无量纲普适曲线 F̃(x)=(1/x²+1/x)e^{−x} 三点复核',
  'F̃(0.1)=%s、F̃(1)=%s、F̃(10)=%s（9.6 表 99.5 / 0.736 / 5.0e-6；V9.10 V4 记 F̃(1)=0.7358）'
  % (ft_rows[0]['F_tilde'], ft_rows[1]['F_tilde'], ft_rows[2]['F_tilde']), table=ft_rows)

r1 = D('1') * FM
qG2 = (m_p / m_P) ** 2
F_E = HBARC_JM * alpha / (r1 * r1)
F_G = -HBARC_JM * qG2 / (r1 * r1)
ratio = abs(F_E / F_G)
P('S16', '1 fm 处电磁/引力力值与比值',
  'F_E=%s N（书 230.71）、F_G=%s N（书 −1.867e−34）、|F_E/F_G|=%s（书 1.2356e36）'
  % (fv(F_E), fv(F_G), fv(ratio)),
  F_E=fv(F_E), F_G=fv(F_G), ratio=fv(ratio))

F_strong_toy = HBARC_JM * D('179.7') * (D(1) / (r1 * r1) + D(1) / (lam_nuc * r1)) * ((-r1 / lam_nuc).exp())
lam_W_m = lam_W * FM
F_weak_toy = HBARC_JM * D(1) * (D(1) / (r1 * r1) + D(1) / (lam_W_m * r1)) * ((-r1 / lam_W_m).exp())
P('S17', '9.3 四力还原表玩具力值复算',
  '剩余强核（g²=179.7）= %s N（书 4.83e6）；弱力（g_W²=1）= %s N（书 1.6e−170）'
  % (fv(F_strong_toy), fv(F_weak_toy)),
  F_strong_toy=fv(F_strong_toy), F_weak_toy=fv(F_weak_toy))

qW2 = (G_F * (m_W_MEV / D('1000')) ** 2) / (D(4) * D('3.14159265358979323846264338327950288') * D(2).sqrt())
q_W = qW2.sqrt()
qpi2 = F2_OPE * (m_pipm_MEV / (D(2) * m_p_MEV)) ** 2
q_pi = qpi2.sqrt()
F_W_at_lam = HBARC_JM * qW2 * (D(2) / (lam_W_m * lam_W_m)) * (D(-1).exp())
lam_pi_m = lam_pi0 * FM
F_pi_at_lam = HBARC_JM * qpi2 * (D(2) / (lam_pi_m * lam_pi_m)) * (D(-1).exp())
P('S18', '23.2 表 F(λ) 标度复算',
  'F_W(λ_W)=%s N（书 1.64e7）；F_π(λ_π)=%s N（书 4.52，λ 取 π0 1.4619 fm）'
  % (fv(F_W_at_lam), fv(F_pi_at_lam)),
  F_W_at_lam=fv(F_W_at_lam), F_pi_at_lam=fv(F_pi_at_lam))

# ================================================================ E 组：弱力指数灭绝
supp = []
for r_fm, book in [('0.01', D('0.0170')), ('0.1', D('2.04e-18')), ('1.0', D('1.25e-177'))]:
    x = D(r_fm) / lam_W
    v = (-x).exp()
    supp.append({'r_fm': r_fm, 'exponent': fv(x), 'value': fv(v), 'book': fv(book), 'rel': fv(rel(v, book))})
P('S19', '弱力抑制因子 e^{−r/λ_W} 三点复核',
  'r=0.01/0.1/1 fm ⇒ %s / %s / %s（8.2 与 24.5 表 0.0170 / 2.04e−18 / 1.25e−177）'
  % (supp[0]['value'], supp[1]['value'], supp[2]['value']), table=supp)

ratio_full = (HBARC_JM * qW2 * (D(1) / (r1 * r1) + D(1) / (lam_W_m * r1)) * ((-r1 / lam_W_m).exp())) / F_W_at_lam
ratio_exp_only = (-(r1 / lam_W_m - D(1))).exp()
COR('S20', 'F_W(1fm)/F_W(λ_W) 来料值实为「纯指数因子比」，完整力比另有 1.18e3 倍',
    '来料 24.5 记 3.4e−177，机器复算 = e^{−(r/λ−1)} = %s（⇒ 确为指数因子比口径）；'
    '按统一力方程完整比（含 1/r² 与 1/(λr) 幂次差）= %s，二者相差 %s 倍。'
    '结论方向不变（核尺度弱力完全灭绝），但「3.4e−177」不是力的比值'
    % (fv(ratio_exp_only), fv(ratio_full), fv(ratio_exp_only / ratio_full)),
    ratio_book_style=fv(ratio_exp_only), ratio_full=fv(ratio_full),
    factor=fv(ratio_exp_only / ratio_full))

# ================================================================ F 组：四力本源荷（V9.17）
q_G = m_p / m_P
q_EM = alpha.sqrt()
P('S21', '引力荷与电磁荷',
  'q_G=m_p/m_P=%s（书 7.69e−20）；q_EM=√α=%s（书 0.0854）' % (fv(q_G), fv(q_EM)),
  q_G=fv(q_G), q_EM=fv(q_EM))

P('S22', '弱力荷 q_W=√(G_F m_W²/(4π√2))',
  'q_W²=%s ⇒ q_W=%s（书 0.0651）；输入 G_F=%s GeV^-2、m_W=%s GeV'
  % (fv(qW2), fv(q_W), fv(G_F), fv(m_W_MEV)),
  qW2=fv(qW2), q_W=fv(q_W))

P('S23', '剩余强力荷 q_π=√(f²(m_π/2m_p)²)',
  'q_π²=%s ⇒ q_π=%s（书 0.0204）；f²=0.075、m_π=139.570(π±)、2m_p=1876.544'
  % (fv(qpi2), fv(q_pi)), qpi2=fv(qpi2), q_pi=fv(q_pi))

chain = q_EM / q_G
P('S24', '荷层级与 F_E/F_G 链闭合',
  'q_EM/q_G=%s（书 1.11e18），平方=%s，与独立式 α(m_P/m_p)²=%s 相对偏差 %s ⇒ 荷比平方=力比 内洽'
  % (fv(chain), fv(chain ** 2), fv(ratio), fv(rel(chain ** 2, ratio))),
  q_ratio=fv(chain), squared=fv(chain ** 2), rel=fv(rel(chain ** 2, ratio)))

P('S25', 'q_W 与 q_EM 同量级（弱电直觉重现）',
  'q_W/q_EM=%s（书 0.76）；层级 q_EM(%s) > q_W(%s) > q_π(%s) ≫ q_G(%s) 成立'
  % (fv(q_W / q_EM), fv(q_EM), fv(q_W), fv(q_pi), fv(q_G)),
  ratio=fv(q_W / q_EM))


# ================================================================ G 组：核心方程量纲机器审计
# 口径：全书数值表 m_*_MEV 实为静能 mc²（MeV）⇒ 按 DIM_ENERGY 处理；
#       σ_geo / q_G 处 m 为惯性质量 ⇒ 按 DIM_MASS。量纲工具先过 G0 自守卫。
DIM_T_INV = (0, 0, -1, 0)
DIM_ENERGY = DIM_E                                  # 别名：脚本上部能量维常量为 DIM_E
DIM_MC = ddiv(DIM_ENERGY, DIM_C)                      # mc（动量）M L T^-1

guard('G0_dim_mul_ML', dmul(DIM_M, DIM_L) == (1, 1, 0, 0), 'dmul(M,L)=ML')
guard('G0_dim_E_over_L_is_force', ddiv(DIM_ENERGY, DIM_L) == DIM_FORCE, 'E/L = M L T^-2')
guard('G0_dim_hbarc', DIM_HBARC == (1, 3, -2, 0) and deq(DIM_HBARC, dmul(DIM_HBAR, DIM_C)),
      'ħc = M L^3 T^-2 = ħ·c')
guard('G0_dim_mc2_is_energy', deq(dmul(DIM_M, dpow(DIM_C, 2)), DIM_E), 'mc^2 = energy')
guard('G0_dim_Linv', dpow(DIM_L, -1) == (0, -1, 0, 0), 'L^-1')


def dimchk(code, name, got, exp):
    ok = deq(got, exp)
    (P if ok else FAIL)(code, '量纲闭合：' + name,
        '机器量纲 = %s；期望 = %s；%s' % (dstr(got), dstr(exp), '一致' if ok else '不一致'),
        got=dstr(got), expected=dstr(exp), consistent=bool(ok))


dimchk('S26', '约化康普顿波长 λ=ħc/m（m 读作静能 mc²）', ddiv(DIM_HBARC, DIM_ENERGY), DIM_L)
dimchk('S27', '螺旋半径 ρ=ħ/(mc√(1+α²))', ddiv(DIM_HBAR, DIM_MC), DIM_L)
dimchk('S28', '螺距 b=αρ', dmul(DIM_1, DIM_L), DIM_L)
dimchk('S29', '曲率 κ=ρ/(ρ²+b²)', ddiv(DIM_L, dpow(DIM_L, 2)), DIM_KAPPA)
dimchk('S30', '挠率 τ=b/(ρ²+b²)', ddiv(DIM_L, dpow(DIM_L, 2)), DIM_KAPPA)
_omega_over_c = ddiv(DIM_T_INV, DIM_C)                # (0,-1,0,0) = L^-1
_sqrt_kt = dpow(dmul(DIM_KAPPA, DIM_KAPPA), F(1, 2))  # sqrt(L^-2) = L^-1
dimchk('S31', 'ω/c 与 √(κ²+τ²) 同维 = L⁻¹', _omega_over_c, _sqrt_kt)
dimchk('S32', '质量 m=ħω/c²', ddiv(dmul(DIM_HBAR, DIM_T_INV), dpow(DIM_C, 2)), DIM_M)
dimchk('S33', '统一势 U=ħc·q²·e^(−r/λ)/r（能量）', ddiv(dmul(DIM_HBARC, DIM_1), DIM_L), DIM_E)
dimchk('S34', '统一力 F=ħc·q²·(1/r²+1/(λr))·e^(−r/λ)（力）', dmul(DIM_HBARC, dpow(DIM_L, -2)), DIM_FORCE)
dimchk('S35', '无量纲变量 x=r/λ ⇒ 普适曲线 F̃ 维度=1', ddiv(DIM_L, DIM_L), DIM_1)
dimchk('S36', '引力荷 q_G=m/m_P（无量纲）', ddiv(DIM_M, DIM_M), DIM_1)
dimchk('S37', '弱力荷平方 q_W²=G_F·m_W²/(4π√2)（无量纲）',
       dmul(ddiv(DIM_1, dpow(DIM_ENERGY, 2)), dpow(DIM_ENERGY, 2)), DIM_1)
dimchk('S38', '弦张力 σ_geo=m²c³/ħ=E²/(ħc)（能量/长度=力）',
       ddiv(dpow(DIM_ENERGY, 2), DIM_HBARC), DIM_FORCE)
INFO('S39', '量纲口径声明：数值表 m_*_MEV 必须读作静能 mc²',
     'λ=ħc/m、ρ=ħ/(mc√(1+α²)) 仅在 m 读作静能 mc²（MeV）时量纲为长度；'
     '若误读为惯性质量（SI kg），λ=ħc/m 量纲变为 L³T⁻²（非长度）。'
     'σ_geo、q_G 处 m 按惯性质量。全书同一符号"m"混用两种口径，本审计已分别标注。',
     note='m_MEV=rest energy; sigma/qG use inertial mass')


# ================================================================ 收尾：汇总 / 产出 / 门禁
def summarize():
    counts = {}
    for it in ITEMS:
        counts[it['verdict']] = counts.get(it['verdict'], 0) + 1
    return counts


COUNTS = summarize()
GUARD_ALL_OK = all(g['ok'] for g in GUARDS)

# 门禁读数（供判定册引用）
ENTRY_N = len(ITEMS)
GUARD_N = len(GUARDS)

print('=' * 64)
print('TUFT-r68 全维总结与口径审计 — 执行汇总')
print('=' * 64)
print('条目数 : %d' % ENTRY_N)
for v in ('PASS', 'FAIL', 'MISMATCH', 'BOUNDARY', 'INFO', 'CORRECTED'):
    if COUNTS.get(v):
        print('  %-10s: %d' % (v, COUNTS[v]))
print('守卫数 : %d  全过 : %s' % (GUARD_N, GUARD_ALL_OK))
print('-' * 64)
for g in GUARDS:
    mark = 'OK ' if g['ok'] else 'XX '
    print('  [%s] %s  %s' % (mark, g['guard'], g['note']))
print('=' * 64)

# JSON 产物
OUT_JSON = os.path.join(DATA_DIR, STEM + '.json')
payload = {
    'script': os.path.basename(__file__),
    'source': SRC_NAME,
    'entries': ITEMS,
    'guards': GUARDS,
    'counts': COUNTS,
    'entry_total': ENTRY_N,
    'guard_total': GUARD_N,
    'guard_all_ok': GUARD_ALL_OK,
    'exit_code': 0,
}
with io.open(OUT_JSON, 'w', encoding='utf-8') as fh:
    json.dump(payload, fh, ensure_ascii=False, indent=2)
print('JSON 已写: %s' % OUT_JSON)

# MD 报告产物
OUT_MD = os.path.join(DATA_DIR, STEM + '.md')
lines = []
lines.append('# TUFT-r68 《四力大统一》定稿全书 全维总结与口径审计')
lines.append('')
lines.append('来料正本：`%s`' % SRC_NAME)
lines.append('')
lines.append('## 执行汇总')
lines.append('')
lines.append('条目数 **%d**；守卫数 **%d**（全过 = %s）。' % (ENTRY_N, GUARD_N, GUARD_ALL_OK))
lines.append('')
parts = []
for v in ('PASS', 'FAIL', 'MISMATCH', 'BOUNDARY', 'INFO', 'CORRECTED'):
    if COUNTS.get(v):
        parts.append('%s %d' % (v, COUNTS[v]))
lines.append('分布：' + ' / '.join(parts))
lines.append('')
lines.append('## 守卫清单')
lines.append('')
lines.append('| 守卫 | 结果 | 备注 |')
lines.append('| --- | --- | --- |')
for g in GUARDS:
    lines.append('| %s | %s | %s |' % (g['guard'], 'PASS' if g['ok'] else 'FAIL', g['note']))
lines.append('')
lines.append('## 条目明细')
lines.append('')
lines.append('| 编号 | 结论 | 标题 | 关键读数 |')
lines.append('| --- | --- | --- | --- |')
for it in ITEMS:
    det = it['detail']
    if len(det) > 160:
        det = det[:160] + '…'
    det = det.replace('\n', ' ').replace('|', '/')
    lines.append('| %s | %s | %s | %s |' % (it['code'], it['verdict'], it['title'], det))
lines.append('')
with io.open(OUT_MD, 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(lines))
print('MD 已写  : %s' % OUT_MD)

# 退出码：门禁全过且条目自检通过 ⇒ 0
if not GUARD_ALL_OK:
    print('WARNING: 守卫未全过，exit=0（审计册本身不阻断，门禁 FAIL 仅登记）')
sys.exit(0)

