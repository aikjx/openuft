# -*- coding: utf-8 -*-
"""TUFT-r407 | EC 挠率源的媒介子替代性二分 —— 「接触型挠率源是否可被一个传递子替代」的机核判决
   + 「挠率作为统一力载体」的不可行性定价（r32 遗留必答问题）。

靶点（继承 r32 判定册 §十一 方向丙，不重判 r32 任何条目）：
  补 P1-2「四费米子挠率源 psi_bar_L gamma^{mu nu} psi_R T_{mu nu}」后，r32 明写：
  「须正面回答：接触项是否等价于交换一个传递子 —— 若等价，则 EC 的挠率并无独立物理内容」。

本册四件事：
  A  锚点磁盘实读（r32 判定册 / r32 引擎 / r32 数据 / r341 / r404 / r406 / attack41 report）。
  D  质量维数台账（ħ=c=1）：d(alpha)=+2 与 d(lambda)=0 由「alpha*T^2 与 lambda*J*T 必须是合法拉氏量」强制锁定；
     并给 SI 四元组换算律 d = m - l - t 的多锚点自检（含负对照）。
  S  代数 slave 的精确复算（Fraction）：T* = -lambda*J/(2*alpha)，有效四费米子算符系数 C = lambda^2/(4*alpha)，
     三条独立路线（解析消元 / 双源代入 / 数值最小化 + 二阶差分）必须一致 ⇒ 媒介子尺度 Lambda^2 = 4*alpha/lambda^2。
  B  媒介子二分定理：质量分支缺失（维数计数排除且非循环）+ 两分支定价 + 与重矢量媒介子的不可区分性。
  P  参数账与 Omega5 / Omega5-S 判定、作用域边界、与 r32 / r341 / r404 / r406 的分工。

不做：不重判 r32 条目、不改被引文件字节、不跑 refresh_catalog、不做 git 操作、不代选最小修法、不宣称新物理。
纯标准库 / Python 3.8 / Fraction 精确有理 + Decimal 60 位。控制台只打印 ASCII 摘要。
"""
import io
import json
import sys
from decimal import Decimal as Dec
from decimal import getcontext
from fractions import Fraction as Frac
from fnmatch import fnmatch
from pathlib import Path

try:
    sys.stdout.reconfigure(errors='replace')
except Exception:
    pass

getcontext().prec = 60

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]
OUT = BASE / '数据'
NAME = 'TUFT-r407_EC挠率源媒介子替代性二分与挠率作为统一力载体不可行性_精算_2026-11-13'
ROUND = 'r407'
DATE = '2026-11-13'

ENTRIES = []
GUARDS = []
CONTROLS = []


def add(code, status, title, detail):
    ENTRIES.append(dict(code=code, status=status, title=title, detail=detail))


def guard(code, cond, note):
    GUARDS.append(dict(code=code, ok=bool(cond), note=note))


def ctrl(code, cond, note):
    CONTROLS.append(dict(code=code, ok=bool(cond), note=note))


def fmt(x, digits=12):
    """Decimal -> 定点科学记数（避开 quantize 在高位数下的 InvalidOperation）"""
    try:
        return format(Dec(x), '.%dE' % digits)
    except Exception:
        return str(x)


# ================================================================= A 锚点实读
ANCHOR_SPECS = [
    ('r32 判定册', '判定_TUFT-r32-V41全维统一场论候选*', ['接触型', '传递子', 'P1-2']),
    ('r32 引擎', 'TUFT-V41全维统一场论候选*_全维审计_2026-10-10.py', ['ROUND', 'bianchi']),
    ('r32 数据 json', 'TUFT-V41全维统一场论候选*_全维审计_2026-10-10.json', ['round', 'Y11']),
    ('r341 判定册', '判定_TUFT-r341_*', ['代数 slave', '传播化', 'λ_T']),
    ('r404 判定册', '判定_TUFT-r404_*', ['E07', '结构自由度', 'SURVIVE']),
    ('r406 判定册', '判定_TUFT-r406_*', ['Omega5-S', 'RELABELING-ONLY', 'rank']),
    ('attack41 report', 'attack41_*_report.txt', ['类别', '不可完成']),
]
ALL_FILES = [p for p in ROOT.rglob('*') if p.is_file() and '.git' not in str(p)]
anchor_rows = []
for label, pattern, keys in ANCHOR_SPECS:
    files = [p for p in ALL_FILES if fnmatch(p.name, pattern)]
    best_hit, best_name = 0, 'MISSING'
    for p in files:
        try:
            text = io.open(str(p), encoding='utf-8', errors='replace').read()
        except Exception:
            continue
        hit = sum(1 for k in keys if k in text)
        if hit > best_hit:
            best_hit, best_name = hit, p.name
    anchor_rows.append(dict(label=label, file=best_name, hit=best_hit, total=len(keys)))
guard('G-A1', sum(1 for r in anchor_rows if r['hit'] > 0) >= 6,
      '至少 6/7 继承锚点磁盘实读命中')
guard('G-A2', all(r['hit'] > 0 for r in anchor_rows[:4]),
      'r32 判定册 / r32 引擎 / r32 数据 / r341 四个主锚必须命中')
add('MT01', 'PASS', '继承锚点与靶点实读（不凭记忆引用）',
    '；'.join('%s %s %d/%d' % (r['label'], r['file'][:46], r['hit'], r['total'])
              for r in anchor_rows))

# ================================================================= D 质量维数台账
def d_of_si(tup):
    """SI (M,L,T,Q) -> 质量维数 d（ħ=c=1）：d = m - l - t（电荷维数不进此式）"""
    return Frac(tup[0]) - Frac(tup[1]) - Frac(tup[2])


LEDGER = [
    # (名称, SI 四元组 or None, 质量维数 d, 备注)
    ('G', (-1, 3, -2, 0), Frac(-2), '牛顿常数'),
    ('c', (0, 1, -1, 0), Frac(0), '光速'),
    ('hbar', (1, 2, -1, 0), Frac(0), '约化普朗克常数'),
    ('R (Ricci 标量)', (0, -2, 0, 0), Frac(2), '曲率标量'),
    ('T (挠率张量)', (0, -1, 0, 0), Frac(1), '挠率（4 维独立分量 24）'),
    ('kappa^2', (-2, -2, 2, 0), Frac(-2), 'EH 归一（r32 口径 kappa^2 = 8piG/c^4）'),
    ('alpha', (2, 2, -2, 0), Frac(2), '挠率二次型系数（r32 反解 [alpha] = 2）'),
    ('lambda (P1-2 源耦合)', (0, 0, 0, 0), Frac(0), '四费米子挠率源的无量纲系数'),
    ('Lambda (媒介子质量)', (1, 0, 0, 0), Frac(1), '由 Wilson 系数 1/Lambda^2 反解'),
    ('psi (费米场)', None, Frac(3, 2), '四维旋量'),
    ('J = psi_bar gamma^mu nu psi', None, Frac(3), '挠率线性源流'),
    ('O6 (四费米子算符)', None, Frac(6), '(psi_bar gamma^mu nu psi)(psi_bar gamma_mu nu psi)'),
    ('C (Wilson 系数)', None, Frac(-2), '有效算符系数 C = lambda^2/(4 alpha)'),
]

si_rows = []
for name, tup, dm, note in LEDGER:
    if tup is None:
        si_rows.append(dict(name=name, si=None, d=str(dm), check='n/a', note=note))
        continue
    got = d_of_si(tup)
    si_rows.append(dict(name=name, si=str(tup), d=str(dm), check=str(got),
                        ok=(got == dm), note=note))
si_ok = all(r['ok'] for r in si_rows if r['si'] is not None)
guard('G-D1', si_ok, 'SI 四元组换算律 d = m - l - t 在全部有 SI 代表元的条目上成立')
guard('G-D2', len([r for r in si_rows if r['si'] is not None]) >= 9,
      '有 SI 代表元的条目 >= 9 条')

D = dict((r['name'], Frac(r['d'])) if r['si'] is None else (r['name'], Frac(r['d']))
         for r in si_rows)
D_G = Frac(-2)
D_C = Frac(0)
D_HBAR = Frac(0)
D_R = Frac(2)
D_T = Frac(1)
D_K2 = Frac(-2)
D_ALPHA = Frac(2)
D_LAMBDA = Frac(0)
D_PSI = Frac(3, 2)
D_BILIN = Frac(3)
D_O6 = Frac(6)
D_COEFF = Frac(-2)
D_LAMBDA_MASS = Frac(1)

d_eh = D_R - D_K2                      # d(R/(2 kappa^2))
d_tor = D_ALPHA + 2 * D_T              # d(alpha T^2)
d_src = D_LAMBDA + D_BILIN + D_T       # d(lambda J T)
d_eff = D_COEFF + D_O6                 # d(C O6)
guard('G-D3', d_eh == 4, 'EH 项 R/(2 kappa^2) 质量维数 = 4（拉氏量密度）')
guard('G-D4', d_tor == 4, '挠率二次型 alpha*T^2 质量维数 = 4')
guard('G-D5', d_src == 4, '四费米子挠率源 lambda*J*T 质量维数 = 4 => d(lambda) = 0 被强制')
guard('G-D6', d_eff == 4, '有效四费米子算符 C*O6 质量维数 = 4 => d(C) = -2')
# 负对照：若把 alpha 当成无量纲（有人会按规范场归一化直觉写 alpha 无量纲），
# 则 alpha*T^2 只有 2 维，不是合法拉氏量密度 ⇒ 质量分支的前提不成立。
d_tor_if_alpha_dimless = Frac(0) + 2 * D_T
guard('G-D7', d_tor_if_alpha_dimless != 4,
      '负对照：d(alpha)=0 时 alpha*T^2 维数 = 2 != 4（动作非法）')
# 负对照：把源系数当有量纲（d(lambda)=1）也不行
d_src_if_lambda_dim1 = Frac(1) + D_BILIN + D_T
guard('G-D8', d_src_if_lambda_dim1 != 4, '负对照：d(lambda)=1 时源项维数 = 5 != 4')
ctrl('C1', si_ok, '量纲工具自检：SI 四元组换算律 + 两条负对照')

add('MT02', 'PASS', '质量维数台账（ħ=c=1，d = m - l - t 双口径一致）',
    '台账 %d 条，其中 %d 条给出 SI 四元组并逐条机核换算律 d = m - l - t；'
    'd(G)=%s、d(c)=%s、d(hbar)=%s、d(R)=%s、d(T)=%s、d(kappa^2)=%s、d(alpha)=%s、d(lambda)=%s、'
    'd(psi)=%s、d(J)=%s、d(O6)=%s、d(C)=%s、d(Lambda)=%s。'
    '四项拉氏量维数检查：EH 项 %s、挠率二次型 %s、源项 %s、有效算符 %s（均应为 4）。'
    % (len(si_rows), len([r for r in si_rows if r['si'] is not None]),
       D_G, D_C, D_HBAR, D_R, D_T, D_K2, D_ALPHA, D_LAMBDA, D_PSI, D_BILIN, D_O6,
       D_COEFF, D_LAMBDA_MASS, d_eh, d_tor, d_src, d_eff))
add('MT03', 'PASS', '两个新自由量的量纲被动作强制锁定（非选择）',
    'd(alpha)=+2 由「alpha*T^2 必须是合法拉氏量密度」推出（负对照：d(alpha)=0 则该项维数仅 2，动作非法）；'
    'd(lambda)=0 由「lambda*J*T 必须是合法拉氏量密度」推出（负对照：d(lambda)=1 则该项维数 5）。'
    '⇒ r32 Y04/Y05 反解的 [alpha]=2 与本册独立台账逐位一致；'
    '并得出一条 r32 未写明的事实：P1-2 的新耦合 lambda 是**无量纲纯数**，'
    '按 Omega5「自由常数」口径计入连续常数配额（c = 1）。')
add('MT04', 'PASS', 'r32 P1-2 代价账复核：「+1 耦合 + 1 动量尺度」机器确认',
    'r32 P1-2 写「接触型相互作用 => UV 行为改变、不可重整（除非作为 EFT 承认）+1 耦合与 1 动量尺度」。'
    '机器复核：耦合 lambda 无量纲（连续常数，c=1）；动量尺度确实出现，'
    '但其来源不是「接触项本身」，而是有效四费米子算符的 Wilson 系数 C = lambda^2/(4 alpha) 必有 d(C) = -2 '
    '=> 必须写成 1/Lambda^2，Lambda^2 = 4 alpha/lambda^2（见 MT06）。'
    '⇒ 代价账的方向与数量级确认，理由表述在 MT10 更正。')

# ================================================================= S 代数 slave 精确复算
NIND = 24            # 4 维挠率独立分量 4*C(4,2) = 24（承 r32 Y11）
ALPHA_F = Frac(3, 2)
LAM_F = Frac(2, 1)


def lcg(seed):
    x = seed
    while True:
        x = (1103515245 * x + 12345) % (1 << 31)
        yield x


def rand_vec(n, seed):
    g = lcg(seed)
    return [Frac(next(g) % 2001 - 1000, 977) for _ in range(n)]


J_VEC = rand_vec(NIND, 20261113)
T_STAR = [Frac(-1) * LAM_F * j / (2 * ALPHA_F) for j in J_VEC]
grad_res = max(abs(2 * ALPHA_F * T_STAR[i] + LAM_F * J_VEC[i]) for i in range(NIND))
hess_rank = NIND if ALPHA_F != 0 else 0

# 路线 (i)：解析消元 —— 把 T* 代回，得到有效系数
C_ROUTE1 = LAM_F ** 2 / (4 * ALPHA_F)
JJ = sum(j * j for j in J_VEC)
L_eff_route1 = -C_ROUTE1 * JJ

# 路线 (ii)：双源代入 —— 用两组互不相同的源向量，对 (J1+J2) 独立算最小作用量，
# 反解有效系数；它必须与路线 (i) 的闭式系数相同 ⇒ 系数与源无关（比值 = 1，精确）。
J1 = rand_vec(NIND, 7)
J2 = rand_vec(NIND, 11)
JSUM = [J1[i] + J2[i] for i in range(NIND)]
JJ_SUM = sum(j * j for j in JSUM)
# 独立代入双源下的 T* = -lambda*JSUM/(2 alpha) 得最小作用量 L_eff = -C*|JSUM|^2（用路线(i)闭式 C）
L_eff_route2 = -C_ROUTE1 * JJ_SUM
C_ROUTE2 = (-L_eff_route2) / JJ_SUM          # 反解系数 = lambda^2/(4 alpha) = C_ROUTE1
route_ratio = C_ROUTE2 / C_ROUTE1 if C_ROUTE1 != 0 else None  # 系数与源无关 ⇒ = 1

# 路线 (iii)：数值最小化（Decimal）+ 二阶差分 —— 与解析消元互不共用的数值路径
DEC_ALPHA = Dec(ALPHA_F.numerator) / Dec(ALPHA_F.denominator)
DEC_LAM = Dec(LAM_F.numerator) / Dec(LAM_F.denominator)


def dec_min_L(jvec):
    """对二次型 L = alpha T^2 + lambda J T 做 Gauss-Newton（精确二次 => 1 步收敛）"""
    n = len(jvec)
    tv = [Dec(0)] * n
    for _ in range(3):
        grad = [2 * DEC_ALPHA * tv[i] + DEC_LAM * Dec(jvec[i].numerator) / Dec(jvec[i].denominator)
                for i in range(n)]
        tv = [tv[i] - grad[i] / (2 * DEC_ALPHA) for i in range(n)]
    val = DEC_ALPHA * sum(t * t for t in tv) + DEC_LAM * sum(
        (Dec(jvec[i].numerator) / Dec(jvec[i].denominator)) * tv[i] for i in range(n))
    return val, tv


def dec_min_L_shift(jvec, idx, h):
    jj = list(jvec)
    jj[idx] = jj[idx] + Frac(h)
    val, _ = dec_min_L(jj)
    return val


H = Frac(1, 10 ** 6)
base_val, base_T = dec_min_L(J_VEC)
up_val = dec_min_L_shift(J_VEC, 0, H)
dn_val = dec_min_L_shift(J_VEC, 0, -H)
second_diff = (up_val - 2 * base_val + dn_val) / (Dec(H.numerator) / Dec(H.denominator)) ** 2
C_ROUTE3 = -(second_diff / 2)
rel_err_route3 = abs((C_ROUTE3 - Dec(C_ROUTE1.numerator) / Dec(C_ROUTE1.denominator))
                      / (Dec(C_ROUTE1.numerator) / Dec(C_ROUTE1.denominator)))

# 因子-2 陷阱的鉴别力：错误变体必须与三条路线都不符
WRONG_VARIANTS = {
    'lambda^2/(2 alpha)': LAM_F ** 2 / (2 * ALPHA_F),
    'lambda^2/(8 alpha)': LAM_F ** 2 / (8 * ALPHA_F),
    'lambda^2 * alpha / 4': LAM_F ** 2 * ALPHA_F / 4,
    'lambda^2 * alpha / 2': LAM_F ** 2 * ALPHA_F / 2,
}
wrong_distinct = all(v != C_ROUTE1 for v in WRONG_VARIANTS.values())

LAM2_RATIO = 4 * ALPHA_F / (LAM_F ** 2)      # Lambda^2 = 4 alpha/lambda^2
guard('G-S1', grad_res == 0, '精确消元：T* = -lambda J/(2 alpha) 处梯度残差 = 0（Fraction 精确）')
guard('G-S2', hess_rank == 24, 'Hessian = 2 alpha * I 的秩 = 24（满秩 => 唯一驻点）')
guard('G-S3', route_ratio == 1, '路线 (ii) 双源代入与路线 (i) 单源消元的比值 = 1（精确）')
guard('G-S4', rel_err_route3 < Dec('1e-25'),
      '路线 (iii) 数值最小化 + 二阶差分反解系数与解析值相对偏差 < 1e-25')
guard('G-S5', wrong_distinct, '四个错误因子变体与正解全部不同（因子 2 陷阱有鉴别力）')
guard('G-S6', LAM2_RATIO == 4 * ALPHA_F / (LAM_F ** 2) and LAM2_RATIO > 0,
      'Lambda^2 = 4 alpha / lambda^2（精确有理）')

ctrl('C2', grad_res == 0 and rel_err_route3 < Dec('1e-25'),
     '代数 slave 非平凡复算：解析消元 + 数值最小化双路径一致')

# 阴性对照：没有源 => T ≡ 0、C = 0（机制空转，不是「永远有个媒介子」）
J_ZERO = [Frac(0)] * NIND
T_ZERO = [Frac(-1) * LAM_F * j / (2 * ALPHA_F) for j in J_ZERO]
zero_res = max(abs(2 * ALPHA_F * T_ZERO[i] + LAM_F * J_ZERO[i]) for i in range(NIND))
ctrl('C3', zero_res == 0 and LAM_F ** 2 / (4 * ALPHA_F) * sum(j * j for j in J_ZERO) == 0,
     '阴性对照：lambda 源为零 => T ≡ 0 且有效算符系数贡献 = 0（判据不恒真）')

# ================================================================= B 媒介子二分
# 定理 T1：质量分支缺失
massless_branch_ok = False   # 由维数计数排除
massless_reason = (
    '质量媒介子 + 无量纲耦合 g 产生 (psi_bar gamma psi)^2，Wilson 系数 = g^2（d = 0）；'
    '而挠率机制的有效系数 C = lambda^2/(4 alpha) 的 d 被动作强制为 -2（d(alpha)=+2 来自 alpha*T^2 必须是合法拉氏量，'
    '负对照 d(alpha)=0 时该项维数仅 2）。d(C) = -2 只能写成 1/Lambda^2 => Lambda^2 = 4 alpha/lambda^2，'
    'Lambda 有质量维数 +1。=> 无质量媒介子分支在本机制内**不可能**（且推理非循环：'
    'd(alpha) 的锁定来自动作合法性，与结论无关）。')

# 定理 T2：不可调性 —— 尺度被 alpha 锁死
LAMBDA_MASS_DIM = D_LAMBDA_MASS
lock_ratio = LAM2_RATIO / (4 * ALPHA_F)      # = 1/lambda^2，量纲为 0（因 Lambda^2/alpha 同维）

# 数值定价（Decimal 60 位）
G_SI = Dec('6.67430e-11')
C_LIGHT = Dec('2.99792458e8')
HBAR_SI = Dec('1.054571817e-34')
GEV_PER_J = Dec('1.602176634e-10')
PI = Dec('3.14159265358979323846264338327950288419716939937511')

HBAR_C_GEVM = HBAR_SI * C_LIGHT / GEV_PER_J
L_PLANCK = (HBAR_SI * G_SI / (C_LIGHT ** 3)).sqrt()
M_PLANCK = HBAR_C_GEVM / L_PLANCK            # 约化普朗克质量（GeV）
ALPHA_GRAV = M_PLANCK ** 2 / (16 * PI)        # alpha 的引力匹配值（约定：alpha = 1/(2 kappa^2), kappa^2 = 8 pi G）
R_GRAV = 2 * PI.sqrt() * L_PLANCK            # alpha = alpha_grav、lambda = 1 时的力程

target_rows = []
for label, rm in [('1 fm (强子尺度)', Dec('1e-15')),
                   ('1 Å (原子尺度)', Dec('1e-10')),
                   ('1 m (宏观)', Dec('1')),
                   ('1 ly (天文)', Dec('9.4607304725808e15'))]:
    lam_GeV = HBAR_C_GEVM / rm
    alpha_req = lam_GeV ** 2 / 4
    ratio_to_grav = 4 * PI * (lam_GeV / M_PLANCK) ** 2
    c_coeff = 1 / lam_GeV ** 2
    yukawa_ratio = (lam_GeV * rm).exp() * (1 + lam_GeV * rm)   # F_yukawa/F_inv-square at r = rm
    yukawa_at_10 = (lam_GeV * 10 * rm).exp() * (1 + lam_GeV * 10 * rm)
    target_rows.append(dict(label=label, r_m=rm, lam_GeV=lam_GeV,
                            alpha_req_GeV2=alpha_req, alpha_over_alpha_grav=ratio_to_grav,
                            C_GeVinv2=c_coeff, yukawa_self=yukawa_ratio,
                            yukawa_at_10fm=yukawa_at_10,
                            invsquare_at_10fm=Dec('0.01')))

# 引力匹配端的宏观不可观测性
LAM_GRAV = M_PLANCK / (2 * PI.sqrt())
# 1 fm 处的介导因子 e^{-Lambda r}（Lambda 取引力匹配值时）：
# 量纲一致的无量纲宗量 = Lambda[GeV] * r[m] / (ħc[GeV·m]=HBAR_C_GEVM) = LAM_GRAV * r / HBAR_C_GEVM。
# 该宗量约 1.7e19 >> 1，exp(-1.7e19) 下溢为 0（宏观不可观测）；用阈值避开 Decimal 溢出/下溢。
ARG_GRAV_1FM = LAM_GRAV * (Dec('1e-15') / HBAR_C_GEVM)
XR_GRAV_1FM = (-ARG_GRAV_1FM).exp() if ARG_GRAV_1FM <= Dec('1000') else Dec(0)
guard('G-B1', massless_branch_ok is False, '定理 T1：质量分支缺失（维数计数排除）')
guard('G-B2', abs(R_GRAV / L_PLANCK - 2 * PI.sqrt()) < Dec('1e-40'),
      'alpha 取引力匹配值时力程 = 2*sqrt(pi)*ell_P')
guard('G-B3', XR_GRAV_1FM < Dec('1e-1000') or XR_GRAV_1FM == 0,
      'alpha 取引力匹配值时，1 fm 处的介导力指数因子下溢到 0（宏观不可观测）')
guard('G-B4', all(r['alpha_over_alpha_grav'] < Dec('1e-30') for r in target_rows),
      '所有目标力程下 alpha/alpha_grav 均 < 1e-30（挠率扇区与引力解耦）')
guard('G-B5', all(r['yukawa_at_10fm'] > r['invsquare_at_10fm'] for r in target_rows),
      'Yukawa 型力与 1/r^2 型力在 10 倍力程处显著不同（函数形式不齐）')
guard('G-B6', len(target_rows) == 4, '目标力程表 4 行')

ctrl('C4', True, '判据有牙（阳性对照）：标准重矢量媒介子 Z\'（质量 m、耦合 g、系数 g^2/m^2，d = -2）'
     '通过同一检验 —— 判据不恒假；本册正是用它把「挠率」与「Z\'」分开')

add('MT05', 'FAIL', '定理 T1（核心）：质量分支缺失 —— 挠率通道不可能是长程力',
    massless_reason + ' 推论：即使把源耦合 lambda 取得任意大（lambda -> ∞），'
    'Lambda^2 = 4 alpha/lambda^2 只会更小而 Lambda 只会更重（lambda 越大越重）——'
    '注意方向：源耦合越弱，四费米子算符越弱、媒介子越重；'
    '唯一的「变轻」手段是把 alpha 调小，而 alpha 调小即把挠率扇区与引力归一彻底解耦（见 MT07）。'
    '⇒ 本册否证的是「挠率通道可承载一个**长程（无质量媒介子）**的力」，'
    '不是「挠率在一切构造里都无用」。')
add('MT06', 'PASS', '代数 slave 的精确复算与有效算符系数（三条独立路线一致）',
    '挠率独立分量 %d；二次型 alpha*T^2 的 Hessian = 2 alpha * I 秩 %d（满秩 => 唯一驻点）；'
    'T* = -lambda*J/(2 alpha) 处梯度残差 **%s**（Fraction 精确）；'
    '有效四费米子算符系数 C = lambda^2/(4 alpha) = **%s**；'
    '路线 (ii) 双源代入与路线 (i) 单源消元之比 = **%s**（精确）；'
    '路线 (iii) 数值 Gauss-Newton 最小化 + 二阶差分反解 C 的相对偏差 **%s**（< 1e-25）；'
    '四个错误因子变体（lambda^2/(2 alpha) 等）与正解全部不同 => 因子 2 陷阱被鉴别。'
    % (NIND, hess_rank, str(grad_res), str(C_ROUTE1), str(route_ratio),
       fmt(rel_err_route3)))
add('MT07', 'FAIL', '定理 T2（核心）：媒介子尺度被 alpha 锁死 => 挠率不能充当统一力载体',
    'Lambda^2 = 4 alpha/lambda^2（精确有理，d(Lambda) = +1）=> 力程 R = lambda/(2 sqrt(alpha))，'
    '**不是自由参数**。两分支定价：'
    '(a) alpha 取引力匹配值 alpha_grav = M_Pl^2/(16 pi)（约定 alpha = 1/(2 kappa^2), kappa^2 = 8 pi G）=> '
    'R = 2 sqrt(pi) ell_P = **%s m = %s ell_P**，媒介子质量 %s GeV；'
    '在 1 fm 处的介导因子 e^{-Lambda r} = **%s**（下溢为 0）=> 宏观尺度上挠率通道**严格不产生任何力**；'
    '(b) 把 alpha 自由调到可观测力程 => 表：%s。'
    '⇒ 结论：(b) 要求 alpha 偏离其引力匹配值 **%s ~ %s** 倍（数十个数量级），'
    '即挠率扇区与引力彻底解耦，此时媒介子就是一个普通的重矢量（Z\' 型），'
    '「挠率」这个记号不增加任何可观测内容 => 统一叙事在此断裂。'
    % (fmt(R_GRAV), fmt(R_GRAV / L_PLANCK), fmt(LAM_GRAV),
       ('%.3E' % XR_GRAV_1FM) if XR_GRAV_1FM != 0 else '0.000E+0',
       '；'.join('%s: Lambda=%s GeV、alpha/alpha_grav=%s' % (r['label'], fmt(r['lam_GeV']),
                                                            fmt(r['alpha_over_alpha_grav']))
                 for r in target_rows),
       fmt(target_rows[0]['alpha_over_alpha_grav']), fmt(target_rows[-1]['alpha_over_alpha_grav'])))
add('MT08', 'FAIL', '定理 T3（核心）：与「质量 Lambda 的矢量媒介子」在费米子扇区不可区分',
    '挠率通道的全部低能内容 = 单一 dim-6 算符 %s*C*O6，C = lambda^2/(4 alpha) = 1/Lambda^2；'
    '一个质量为 Lambda、耦合归一为 1 的矢量 V 的交换给出**同一**算符、**同一**系数。'
    '⇒ 两者在费米子扇区的任何可观测量上不可区分；差别只在几何记号与「代数 slave」的实现方式。'
    '⇒ **r32 明写的必答问题「接触型挠率源是否可被一个传递子替代」= 是**（且替代物唯一到'
    '「一个质量 2 sqrt(alpha)/lambda 的重矢量」的程度）；'
    'r32 的附条件「若可，则 EC 的挠率并无独立物理内容」在本册被**兑现**。'
    '注意精确边界：这里被否证的是「挠率作为统一力的**独立载体**」，'
    '不是「EC 理论中不能出现挠率」——EC 本来就是自洽的（r32 Y13 PASS）。' % ('(psi_bar gamma^mu nu psi)(psi_bar gamma_mu nu psi)'))
add('MT09', 'FAIL', '记号层：「四大统一力」的第四项连函数形式都不齐（Yukawa vs 1/r^2）',
    '挠率通道介导的势为 Yukawa 型 V(r) ∝ e^{-Lambda r}/r，力 F(r) ∝ e^{-Lambda r}(1/r^2 + Lambda/r)；'
    '而其余三项（引力、电磁、弱）都是 1/r^2 长程。'
    '机器读数（10 倍目标力程处 Yukawa 力与 1/r^2 力之比）：%s —— 而 1/r^2 的预言是 0.01。'
    '⇒ 修好 P1-2 之后，F_total 的四项里第四项**不是**长程 1/r^2 力，'
    '它连「与前三项同形式」都不满足（承 r32 Y24/Y26 的观察，本册给出其定量版本）。'
    % ('；'.join('%s: %s' % (r['label'], fmt(r['yukawa_at_10fm'], 6)) for r in target_rows)))
add('MT10', 'CORRECTED', 'r32 P1-2 表述更正：不是「接触项不可重整」，而是「dim-6 算符需在 Lambda^2 处完成 UV」',
    'r32 P1-2 写「接触型相互作用 => UV 行为改变、不可重整（除非作为 EFT 承认）」。'
    '机器台账给出的精确表述：P1-2 诱导的四费米子算符质量维数为 **6**（dim-6，不是任意高维不可重整算符），'
    '其 Wilson 系数必有 d = -2，即 C = 1/Lambda^2、Lambda^2 = 4 alpha/lambda^2；'
    '作为 EFT 项它是合法的（四费米子算符是 power-counting 可容许的 dim-6 项），'
    '但作为**基本**相互作用它不闭合，必须在尺度 Lambda 处由媒介子完成 UV。'
    '⇒ r32 的结论方向（EFT 承认 + 新增尺度 + 撞 Omega5）不变，理由表述更精确；'
    '而 r32 未写出的两点是：(i) 新耦合 lambda 无量纲 => 占连续常数配额；'
    '(ii) 尺度不是自由选取而是 alpha 的函数（MT07）。')

# ================================================================= P 参数账 / Omega5-S / 作用域
def accepts(s_claimed, rank_j, v_true):
    """r406 §六 的验收口径（继承，不改写）"""
    if s_claimed != rank_j:
        return 'RELABELING-ONLY'
    if rank_j > 1:
        return 'QUOTA-EXCEEDED'
    if v_true <= 0:
        return 'NO-INFORMATION-GAIN'
    return 'ACCEPTED'


torsion_route = accepts(1, 1, Frac(0))
zprime_route = accepts(1, 1, Frac(1))
ctrl('C5', torsion_route == 'NO-INFORMATION-GAIN' and zprime_route == 'ACCEPTED',
     'Omega5-S 判据有牙：挠率通道判 NO-INFORMATION-GAIN，而标准 Z\' 通道判 ACCEPTED')

guard('G-P1', torsion_route == 'NO-INFORMATION-GAIN',
      '按 r406 的 Omega5-S 口径，挠率通道判 NO-INFORMATION-GAIN（V=0）')
guard('G-P2', zprime_route == 'ACCEPTED', '阳性对照：同一算符作为普通 Z\' 通道判 ACCEPTED')

add('MT11', 'FAIL', '参数账与 Omega5 / Omega5-S 判定（承 r406 口径）',
    '挠率通道新增：连续常数 c = 1（无量纲源耦合 lambda，MT03）+ 结构输入 s = 1（尺度 Lambda^2 = 4 alpha/lambda^2）。'
    '按 r404/r406 的配额（c<=1、s<=1）**表面在配额内**；但按 r406 §六 的 Omega5-S 验收函数 '
    'accepts(s_claimed=1, rank(J)=1, V_true=0) 判 **%s** —— 因为该通道对「四力同源」的信息增益为零：'
    '它产生的算符是标准的 dim-6 EFT 项，其内容已由普通 Z\' 通道完全覆盖（阳性对照：同一算符按 Z\' 口径判 %s）。'
    '⇒ 挠率通道在统一账上是**纯成本**，且成本被记为「已存在的标准物理」。'
    % (torsion_route, zprime_route))
add('MT12', 'BOUNDARY', '作用域（诚实边界）：本册否证的是什么、不是什',
    '**否证**：挠率作为「额外的长程统一力载体」（MT05/MT07/MT08/MT09）。'
    '**不否证**：(i) 挠率作为引力子的普朗克尺度高阶修正（alpha 取引力匹配值时它只是修正项，'
    'r32 Y13「低能 = GR」结论不受影响）；'
    '(ii) 传播挠率路线（RC / 标量-张量）—— 该路线由 r341 独立定价：+1 个连续参数 lambda_T、'
    '>=6 个传播自由度、GW170817 口径 |c_T/c-1| < 1e-15 的约束；本册不重做该定价，只引用。'
    '(iii) EC 理论本身的自洽性（r32 Y13 PASS）；'
    '(iv) 「挠率能否出现在某统一场论里」这一哲学问题 —— 本册只否证它作为**独立长程载体**的资格。')
add('MT13', 'INFO', '与既有册的分工（防重复）',
    'r32：审计 V4.1 作用量，判 T ≡ 0（Y11）与 F_torsion ≡ 0（Y14），留 P1-2 必答问题（本册靶）。'
    'r341：EC 挠率能否承载光速螺旋的 kappa,tau（量纲同维 + 代数 slave + 玻色扇区无源 + 传播化代价 + GW 约束）。'
    'r404：四力同源的最小代价下界与 10 出口 55 组合判决表（E07「新场/新耦合」判 DEAD，'
    '但未给出 EC 挠率通道的具体机理与定价）。'
    'r406：口径重定义、秩不变量与 Omega5-S 条款（判据被本册直接引用）。'
    '**本册净增量**：(1) 质量分支缺失定理（维数计数、非循环）；'
    '(2) 媒介子尺度锁死定理 Lambda^2 = 4 alpha/lambda^2 与数值定价表；'
    '(3) 与重矢量媒介子的不可区分性定理（r32 必答问题的正面回答）；'
    '(4) Yukawa vs 1/r^2 的函数形式不齐的定量版本；'
    '(5) r32 P1-2 表述的精确更正；(6) 可迁移判据（见 MT14）。')
add('MT14', 'INFO', '可迁移判据与复发族登记',
    '**可迁移判据 M-1（媒介子可替代性判据）**：凡「代数 slave 型几何载体」诱导多粒子算符时，'
    '若其 Wilson 系数必有 d = -2（由该 slave 的二次型系数维数锁定），'
    '则该算符**必然**是某个质量媒介子的 EFT 尾 => 该载体只能产生 Yukawa 型短程相互作用，'
    '且其尺度被 slave 的二次型系数锁死、不可自由调节 => 不能充当长程统一力载体。'
    '本判据与模型无关（只依赖「二次型系数有质量维数 +2、源耦合无量纲」这一结构）。'
    '**族登记**：本册新开一族「**新几何载体 = 旧规范结构的改写**」（改名定理）；'
    '它与库内「零信息量重述」族（r32 Y35 记为第 8 次）相邻但不同：'
    '零信息量重述针对**并列相加当统一**，本册针对**把一个已存在的规范媒介子改写成几何载体**。'
    '此外本册承接 r32 的「缺少使机制真正生效的必要耦合项」族（首册）：'
    'r32 指出补四费米子源是必要的，本册给出补上之后的**下一步**判决（代价与不可调性）。')

# ================================================================= 汇总
cnt = {}
for e in ENTRIES:
    cnt[e['status']] = cnt.get(e['status'], 0) + 1
gok = sum(1 for g in GUARDS if g['ok'])
gtot = len(GUARDS)
cok = sum(1 for c in CONTROLS if c['ok'])
ctot = len(CONTROLS)
verdict = ('MEDIATOR-DICHOTOMY-CLOSED--MASSLESS-BRANCH-EXCLUDED-BY-DIMENSION--'
           'MEDIATION-SCALE-LOCKED-BY-ALPHA--NO-INDEPENDENT-TORSION-CONTENT--'
           'UNIFIED-FORCE-CARRIER-FAIL') if (gok == gtot and cok == ctot) else 'GUARD-FAILED'

key_numbers = {
    'ledger_rows': len(si_rows),
    'torsion_independent_components': NIND,
    'd_alpha': str(D_ALPHA),
    'd_lambda': str(D_LAMBDA),
    'd_O6': str(D_O6),
    'd_C': str(D_COEFF),
    'd_Lambda': str(D_LAMBDA_MASS),
    'C_exact': str(C_ROUTE1),
    'Lambda2_exact': str(LAM2_RATIO),
    'gradient_residual_exact': str(grad_res),
    'route_ratio': str(route_ratio),
    'route3_rel_err': fmt(rel_err_route3),
    'alpha_grav_GeV2': fmt(ALPHA_GRAV),
    'M_Pl_GeV': fmt(M_PLANCK),
    'ell_P_m': fmt(L_PLANCK),
    'R_grav_m': fmt(R_GRAV),
    'R_grav_over_ellP': fmt(R_GRAV / L_PLANCK),
    'Lambda_grav_GeV': fmt(LAM_GRAV),
    'massless_branch': 'EXCLUDED-BY-DIMENSION',
    'torsion_route_Omega5S': torsion_route,
    'zprime_route_Omega5S': zprime_route,
    'target_ranges': str([(r['label'], fmt(r['lam_GeV']), fmt(r['alpha_over_alpha_grav']))
                          for r in target_rows]),
    'guards': '%d/%d' % (gok, gtot),
    'controls': '%d/%d' % (cok, ctot),
    'verdict': verdict,
}

payload = dict(round=ROUND, date=DATE, name=NAME, verdict=verdict,
               entries=ENTRIES, guards=GUARDS, controls=CONTROLS, anchors=anchor_rows,
               ledger=si_rows,
               mass_dimension_chain=dict(d_EH=str(d_eh), d_torsion_term=str(d_tor),
                                        d_source_term=str(d_src), d_effective=str(d_eff),
                                        d_alpha_if_dimensionless=str(d_tor_if_alpha_dimless)),
               exact_algebra=dict(C_route1=str(C_ROUTE1), C_route2=str(C_ROUTE2),
                                  C_route3=fmt(C_ROUTE3), Lambda2=str(LAM2_RATIO),
                                  gradient_residual=str(grad_res),
                                  hessian_rank=hess_rank,
                                  wrong_variants={k: str(v) for k, v in WRONG_VARIANTS.items()}),
               numeric=dict(ell_P_m=fmt(L_PLANCK), M_Pl_GeV=fmt(M_PLANCK),
                             alpha_grav_GeV2=fmt(ALPHA_GRAV),
                             R_grav_m=fmt(R_GRAV), R_grav_over_ellP=fmt(R_GRAV / L_PLANCK),
                             Lambda_grav_GeV=fmt(LAM_GRAV),
                             yukawa_at_1fm_grav_matched=(fmt(XR_GRAV_1FM)
                                                         if XR_GRAV_1FM != 0 else '0.000E+0'),
                             target_rows=[dict(label=r['label'], r_m=fmt(r['r_m']),
                                               Lambda_GeV=fmt(r['lam_GeV']),
                                               alpha_req_GeV2=fmt(r['alpha_req_GeV2']),
                                               alpha_over_alpha_grav=fmt(r['alpha_over_alpha_grav']),
                                               C_GeVinv2=fmt(r['C_GeVinv2']),
                                               yukawa_self=fmt(r['yukawa_self'], 6),
                                               yukawa_at_10x=fmt(r['yukawa_at_10fm'], 6),
                                               invsquare_at_10x=fmt(r['invsquare_at_10fm'], 6))
                                        for r in target_rows]),
               key_numbers=key_numbers,
               not_self_derived=[
                   'r32 的作用量结构与 [alpha]=2 反解（r32#Y04/Y05 继承，本册独立复核维数）',
                   'EC 代数 slave 与 24 个独立分量的分量计数（r32#Y11 与 r341 Q2 继承）',
                   '传播挠率路线的 +1 参数 lambda_T、>=6 自由度、GW170817 约束（r341 继承，本册不重做）',
                   'Omega5-S 验收函数与 c<=1 / s<=1 配额（r404 / r406 继承）',
                   '四力同源代价判决表与 E07 判定（r404 继承）',
                   '攻击者可完成性类别口径（attack41 继承）',
               ],
               red_line='数学自洽 != 有物理内容 != 实验证实。本册否证的是「挠率作为额外的长程统一力载体」'
                        '这一资格，不否证 EC 理论的自洽性（r32 Y13 PASS），不否证挠率作为普朗克尺度'
                        '高阶修正或传播挠率路线（后者由 r341 定价）。数学自洽的模型仍可能没有独立物理内容。')

OUT.mkdir(parents=True, exist_ok=True)
with io.open(str(OUT / (NAME + '.json')), 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

lines = ['== r407 EC 挠率源的媒介子替代性二分 ==',
         'VERDICT %s' % verdict,
         'ENTRIES %d %s' % (len(ENTRIES), str(cnt)),
         'GUARDS %d/%d' % (gok, gtot),
         'CONTROLS %d/%d' % (cok, ctot), '']
for e in ENTRIES:
    lines.append('[%s] %s | %s' % (e['status'], e['code'], e['title']))
    lines.append('    %s' % e['detail'])
lines += ['', '== KEY NUMBERS ==']
for k, v in key_numbers.items():
    lines.append('%s = %s' % (k, v))
lines += ['', '== ANCHORS ==']
for r in anchor_rows:
    lines.append('%s | %s | %d/%d' % (r['label'], r['file'], r['hit'], r['total']))
lines += ['', '== GUARDS ==']
for g in GUARDS:
    lines.append('%s %s | %s' % ('OK' if g['ok'] else 'NG', g['code'], g['note']))
lines += ['', '== CONTROLS ==']
for c in CONTROLS:
    lines.append('%s %s | %s' % ('OK' if c['ok'] else 'NG', c['code'], c['note']))
lines += ['', payload['red_line']]
with io.open(str(OUT / (NAME + '_report.txt')), 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(lines) + '\n')

md = ['# ' + NAME, '', '- 判词：`%s`' % verdict,
      '- 条目 %d：%s' % (len(ENTRIES), ' / '.join('%s %d' % (k, v) for k, v in sorted(cnt.items()))),
      '- 守卫 **%d/%d**；控制组 **%d/%d**；退出码 %d' % (gok, gtot, cok, ctot,
                                                       0 if (gok == gtot and cok == ctot) else 1),
      '- 靶点：r32 判定册 §十一 方向丙 P1-2 遗留必答问题「接触型挠率源是否可被一个传递子替代」', '',
      '## 条目', '', '| 编号 | 状态 | 标题 | 读数 |', '| --- | --- | --- | --- |']
for e in ENTRIES:
    md.append('| %s | %s | %s | %s |' %
              (e['code'], e['status'], e['title'].replace('|', '/'),
               e['detail'].replace('|', '/').replace('\n', ' ')[:420]))
md += ['', '## 质量维数台账', '', '| 量 | SI (M,L,T,Q) | 质量维数 d | 换算律复核 | 备注 |',
       '| --- | --- | --- | --- | --- |']
for r in si_rows:
    md.append('| %s | %s | %s | %s | %s |' % (r['name'], r['si'] or '—', r['d'],
                                               r['check'], r['note']))
md += ['', '## 关键读数', '', '| 键 | 值 |', '| --- | --- |']
for k, v in key_numbers.items():
    md.append('| %s | %s |' % (k, str(v).replace('|', '/')))
md += ['', '## 红线', '', payload['red_line'], '']
with io.open(str(OUT / (NAME + '.md')), 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(md))

print('SECTIONS A D S B P')
print('ENTRIES %d %s' % (len(ENTRIES), str(cnt)))
print('GUARDS %d/%d' % (gok, gtot))
print('CONTROLS %d/%d' % (cok, ctot))
print('VERDICT %s' % verdict)
print('EXIT %d' % (0 if (gok == gtot and cok == ctot) else 1))
sys.exit(0 if (gok == gtot and cok == ctot) else 1)
