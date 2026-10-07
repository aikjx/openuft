# -*- coding: utf-8 -*-
# 判定：TUFT V3.4 四模块结构审计 + 路线选址前置闭合（第十七轮）
# 来料：用户提交的 TUFT V3.4 —— §一 紫外不动点与稳定性 / §二 挠率手征反常与重子不对称
#       / §三 克尔剖面与熵 / §四 引力诱导坍缩（四条候选路线附于文末）
# 本轮五件事（全部位于「选哪条路线」之前，不引入任何新的物理约定）：
#   A UV 不动点：约束代数、示例代码实际返回值、齐次退化、雅可比可执行性、系数自由度清算
#   B 重子不对称：量纲表、β 符号冲突、冻结条件与 Y_B 式的三重口径、参数自由度账
#   C 克尔剖面：τ 量纲、κ+τc 组合、定义式冒充守恒律、与核心恒等式 κ^2+τ^2=Ω^2 的相容性、熵式对齐
#   D 量子坍缩：坍缩率量纲缺口的最小补齐（机器解）、物质属性缺失、新增挠率项的可证伪性
#   E 四条候选路线的前置缺口矩阵（有依赖，无打分）
# 红线：①不代选路线（引擎无 score/rank/recommend 字段，裁决权保留给用户）
#       ②不改来料任何式子的物理内容，只标 deferred（推迟项）与 [C] 外部输入
#       ③数学自洽 != 实验证实；本册全部结论是结构审计结论，不是证伪宣告
import os
import re
import sys
import json
import math
import time
import random

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

T0 = time.time()
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BASE = os.path.join(ROOT, '04_公共成果', '算法联盟_全维自洽与归一化')
DATA = os.path.join(BASE, '数据')
RES = []
GRD = []
KEY = {}

# ===== 来料读数（逐字引用，不重算；数值改动须回来改这里）=====
C1D, C2D, C3D = 0.12, -0.35, 0.08          # §一 圈系数默认值
D1D, D2D = 0.21, -0.44                      # §一 β_c 线性系数默认值
MP_GeV = 1.220890e19                        # §二 普朗克质量 GeV
Y_OBS = 8.7e-11                             # 重子丰度观测值
T_ASSUMED = 1.0e16                          # §二 示例代码写死的 T_f
TAU_LIST = [1e-4, 1e-3, 1e-2]
BETA_LIST = [1e-6, 1e-5]

# ===== SI 常数（量纲与 Λ_0 对齐用）=====
C_SI = 2.99792458e8
G_SI = 6.67430e-11
HBAR_SI = 1.054571817e-34

# ===== 单位向量工具（基 = (L, M, T) SI 指数）=====
G_U = (3, -1, -2)      # Newton 常数
HB_U = (2, 1, -1)      # hbar
C_U = (1, 0, -1)       # 光速
RATE_U = (0, 0, -1)    # s^-1
INV_LEN_U = (-1, 0, 0)
AREA_U = (2, 0, 0)


def addu(a, b):
    return tuple(x + y for x, y in zip(a, b))


def subu(a, b):
    return tuple(x - y for x, y in zip(a, b))


def mulu(a, n):
    return tuple(x * n for x in a)


def solve_mix(target, basis, rng=4):
    """求整数指数 e 使 sum e_i*basis_i == target；无解返回 None"""
    rngs = [range(-rng, rng + 1) for _ in basis]
    for a in rngs[0]:
        for b in rngs[1]:
            for c in rngs[2]:
                v = tuple(x * a + y * b + z * c for x, y, z in zip(basis[0], basis[1], basis[2]))
                if v == target:
                    return (a, b, c)
    return None


def add(cid, sec, item, verdict, detail):
    RES.append({'id': cid, 'section': sec, 'item': item,
                'verdict': verdict, 'detail': detail})
    print('[%-8s] %-5s %-14s | %s' % (verdict, cid, sec, detail[:128]))


def guard(name, ok, detail):
    GRD.append({'name': name, 'ok': bool(ok), 'detail': detail})
    print('[GUARD] %-30s | %s | %s' % ('PASS' if ok else 'FAIL', name, detail[:96]))
    return bool(ok)


def sec_A():
    k = -D1D / D2D                              # alpha_* / G_*
    Q = C1D * k * k + C2D * k + C3D
    # 示例代码等价物：constraint(Gs) = Q * Gs^2（二次齐次）
    x = 1.0
    steps = 0
    while abs(x) > 1e-40 and steps < 200:
        f = Q * x * x
        fp = 2.0 * Q * x
        if fp == 0.0:
            break
        x = x - f / fp
        steps += 1
    KEY['uv'] = {'k_ratio': k, 'Q': Q, 'newton_root': x, 'newton_steps': steps}
    add('A-01', 'A', 'algebra_of_constraint', 'PASS',
        '约束代数本身无误：令 k = alpha_*/G_* = -D1/D2 = %.6f，消元后 constraint(G)=Q*G^2，'
        'Q = C1*k^2 + C2*k + C3 = %.6e；G_* != 0 时非平凡不动点存在 iff Q = 0。这一步 Algebra 正确，保留'
        % (k, Q))
    add('A-02', 'A', 'default_coeffs_fail', 'FAIL',
        '但来料自带的默认系数并不满足该自洽条件：Q = %.6e != 0（各项量级 O(1e-2)，相对不闭合 %.1f%%）'
        '=> 在这组系数下**不存在非零不动点**；文档写作「若满足，则……」却未检查自给数值是否满足'
        % (Q, abs(Q) / max(abs(C1D * k * k), abs(C2D * k), abs(C3D)) * 100.0))
    add('A-03', 'A', 'example_code_returns_trivial', 'FAIL',
        '示例代码的实际返回值：constraint 是 Gs 的二次齐次式 => Newton 迭代对二重根线性收敛（每步精确减半），'
        '从 Gs=1.0 出发 %d 步落到 G_*=%s，残差 %.2e => 打印出来的「紫外不动点」实为**平凡高斯不动点 '
        'G_*=alpha_*=0**；且一旦 Q=0，constraint 恒为 0，findroot 在任何初值都直接返回初值（整条射线都是根）'
        % (steps, '%.3e' % x, abs(Q * x * x)))
    # 齐次退化：构造一组满足 Q=0 的系数，验证只锁比值不锁点
    k0 = 0.5
    c1, c3 = 0.13, -0.07
    c2 = -(c1 * k0 * k0 + c3) / k0

    def bal(g):
        return c1 * (k0 * g) ** 2 + c2 * g * (k0 * g) + c3 * g * g

    lam = [1.0, 3.7, 1.0e6, -2.5]
    res = [abs(bal(t)) for t in lam]
    KEY['uv']['ray_residual_max'] = max(res)
    KEY['uv']['ray_lambdas'] = lam
    add('A-04', 'A', 'homogeneous_degeneracy', 'FAIL',
        '齐次退化（比 A-03 更根本）：第二式是 (G,alpha) 的二次齐次、第三式是一次齐次 => '
        '两式都**只锁比值**，射线 (G,alpha)=(lambda, -D1/D2*lambda) 上每点都是根'
        '（机器验证 lambda = %s 四点残差均 <= %.1e）=> 不动点是**连续族而非孤立点**。'
        '零集是过该点的曲线 => 对参数化 gamma(s) 求导 beta(gamma(s))=0 得 J*gamma\'=0 => '
        '**雅可比必有一个零本征值（边缘方向）** => 「有限个负实部本征值 / 有限维临界曲面 / 有限个自由参数」'
        '无法由此体系推出' % (lam, max(res)))
    add('A-05', 'A', 'jacobian_not_executable', 'MISMATCH',
        '声称目标与实现不匹配：小节目标是「求 J 的本征值 => 有限个负实部 => 可预测量子引力」，'
        '但给出的代码**只做标量 findroot，既未构造 J 也未求本征值**；更关键的是 β_G 从未写成 (G,alpha,c) 的显式函数'
        '（只给含 beta_c / beta_kappa-tau / kappa / tau 的隐关系），J_ij = dbeta_i/dg_j **在数学上不可求值**'
        ' => 稳定性分析不是「待算」而是「缺定义」，当前不可执行')
    # 系数空间自由度：5 个系数 vs 1 个约束
    rnd = random.Random(20261007)
    hits = 0
    hits_rel = 0
    tot = 0
    for _ in range(20000):
        a1 = rnd.uniform(-1, 1)
        a2 = rnd.uniform(-1, 1)
        a3 = rnd.uniform(-1, 1)
        b1 = rnd.uniform(-1, 1)
        b2 = rnd.uniform(-1, 1)
        if abs(b2) < 0.1:
            continue
        tot += 1
        kk = -b1 / b2
        q = a1 * kk * kk + a2 * kk + a3
        scale = abs(a1 * kk * kk) + abs(a2 * kk) + abs(a3)
        if abs(q) < 1e-3:
            hits += 1
        if scale > 0 and abs(q) / scale < 1e-3:
            hits_rel += 1
    KEY['uv']['finetune'] = {'samples': tot, 'abs_hits': hits, 'rel_hits': hits_rel,
                             'abs_frac': hits / float(tot), 'rel_frac': hits_rel / float(tot)}
    add('A-06', 'A', 'coefficient_space_is_a_hypersurface', 'FAIL',
        '系数自由度清算：未知量 5 个（C1,C2,C3,D1,D2），约束 1 个 => 解集是 5 维空间中的 4 维超曲面；'
        '随机抽样 %d 组（|D2|>0.1，[-1,1]^5 均匀，种子 20261007）：绝对过敏 |Q|<1e-3 命中 %d 组（%.3f%%），'
        '相对过敏 |Q|/尺度<1e-3 命中 %d 组（%.3f%%）=> 「找到稳定不动点」在通用情形下是**逆构造/精调**结果，'
        '不是理论输出；且 C_i,D_i 全无出处（无圈积分、无作用量 -> beta 的推导），记为 [C] 外部输入'
        % (tot, hits, 100.0 * hits / tot, hits_rel, 100.0 * hits_rel / tot))
    add('A-07', 'A', 'symbol_ledger_conflict', 'MISMATCH',
        '符号台账冲突（违反「一符号、一量纲、一定义」）：同一个 β 在 §一 表示 RG β 函数、'
        '在 §二 表示手征-挠率耦合系数；若强制同义，则由 B-01 得 [β]=0 而由 B-02 需 [β]=-1 => 互斥。'
        '零成本修：改记 beta_ch（或 gamma_ch）。该缺陷修复成本为零，不改任何物理')


def sec_B():
    # 质量量纲（hbar = c = 1，能量为单位）：[tau]=1 [psi-bar gamma5 psi]=3 [div J5]=4
    dim_beta_anom = 4 - (1 + 3)       # B-01 => 0
    dim_beta_rate = 1 - (1 + 1)       # B-02 => -1
    dim_yb_from_anom = dim_beta_anom + 1 + 3 - 2
    dim_yb_from_rate = dim_beta_rate + 1 + 3 - 2
    KEY['dim'] = {'beta_anom': dim_beta_anom, 'beta_rate': dim_beta_rate,
                  'yb_dim_if_beta0': dim_yb_from_anom, 'yb_dim_if_beta_m1': dim_yb_from_rate}
    add('B-01', 'B', 'anomaly_eq_dimension_ok', 'PASS',
        '反常式自身量纲闭合（仅此一格通过）：[∇_mu J5^mu]=4，[τ]=1，[ψ̄γ5ψ]=3 => (β/2)τψ̄γ5ψ 要求 [β]=%d；'
        '右侧 R̃R 为 L^-4 -> 4 ✓ => 两侧一致，该式作为**写下来的形式**是自洽的' % dim_beta_anom)
    add('B-02', 'B', 'beta_dimension_conflict', 'FAIL',
        'Γ_chiral ∝ β·τ_bg·T 与 B-01 互斥：[Γ]=1（率），[τ_bg]=1，[T]=1 => 需要 [β]=%d；'
        '而同一符号在反常式中被定为 [β]=%d => **同一份材料内 β 的量纲自相矛盾**，'
        '两条式子不可能同时成立（除非在两处引入不同的带量纲系数，但材料未写）'
        % (dim_beta_rate, dim_beta_anom))
    add('B-03', 'B', 'Y_B_not_dimensionless', 'FAIL',
        'Y_B = β·τ·T_f^3/M_P^2 不是无量纲（重子丰度必须是 0）：在 [β]=0 口径下为 %+d，'
        '在 [β]=-1 口径下为 %+d => **两种口径都不闭合**，该式缺一个带量纲因子（或 T^3 / M_P^2 的幂次需重定）；'
        '这也解释了为何示例代码给出的数值远大于 1（见 B-06）'
        % (dim_yb_from_anom, dim_yb_from_rate))
    add('B-04', 'B', 'freeze_T_typo_and_dimension', 'FAIL',
        '冻结温度式的双重问题：由 Γ=H 联立 FRW（H ∝ T^2/M_P，Γ ∝ βτT）应得 T_f = M_P·β·τ_bg（ Planck 增强）；'
        '原文写 T_f ~ (M_P·β·τ_bg)/M_P，分子分母的 M_P **相消** => 既丢掉 Planck 增强，'
        '又使 [T_f] 退化为 [βτ]（= %d 或 %d，都不是温度）。当作笔误记 MISMATCH、当量纲失效记 FAIL'
        % (dim_beta_anom + 1, dim_beta_rate + 1))
    pref = T_ASSUMED ** 3 / MP_GeV ** 2
    pairs = [(t, b) for t in TAU_LIST for b in BETA_LIST]
    us = sorted(set(t * b for t, b in pairs))
    ys = [u * pref for u in us]
    u_from_yb = Y_OBS / pref
    u_joint = (Y_OBS / MP_GeV) ** 0.25
    t_joint = MP_GeV * u_joint
    spread = math.log10(max(us + [u_from_yb, u_joint]) / min(us + [u_from_yb, u_joint]))
    KEY['baryon'] = {'pref': pref, 'scan_beta_tau': us, 'scan_YB': ys,
                     'beta_tau_from_YB_fixed_T': u_from_yb,
                     'beta_tau_joint': u_joint, 'T_f_joint_GeV': t_joint,
                     'spread_dex': spread,
                     'min_over_obs': min(ys) / Y_OBS,
                     'ratio_joint_to_fixedT': u_joint / u_from_yb,
                     'ratio_assumed_T_to_joint': T_ASSUMED / t_joint}
    add('B-05', 'B', 'triple_caliber_inconsistent', 'FAIL',
        '三重口径互斥：把同一组 (β,τ) 同时放进 Y_B 式与冻结式会得到三个互不相容的取值 —— '
        '(i) 示例代码扫描所用 βτ = %s；(ii) 由 Y_B 式配 T_f=1e16 GeV 反解 βτ = %.4e；'
        '(iii) 两式联立自洽解 βτ = (Y_B/M_P)^{1/4} = %.4e，对应 T_f = %.4e GeV。'
        '三者跨度 %.2f 个量级；(ii) 与 (iii) 相差 %.2e 倍；且代码写死的 T_f=1e16 与自洽冻结温度相差 %.2f 倍 '
        '=> 「 Target 一致」不成立，三个数字不能同表混用' % (us, u_from_yb, u_joint, t_joint,
                                                spread, u_joint / u_from_yb, T_ASSUMED / t_joint))
    add('B-06', 'B', 'scan_off_by_9_orders', 'FAIL',
        '示例代码的 4 个不同 βτ 组合给出 Y_B ∈ [%.4f, %.2f]，全部远大于观测 %.1e：'
        '最小组合也超 **%.2e 倍**，最大超 %.2e 倍 => 在给出的扫描区间内「令理论输出匹配观测」并不成立，'
        '必须把 βτ 下调约 %.1e 倍至 %.3e 量级（等价于把 β 或 τ_bg 外推出材料自身的取值域）'
        % (min(ys), max(ys), Y_OBS, min(ys) / Y_OBS, max(ys) / Y_OBS,
           min(us) / u_from_yb, u_from_yb))
    add('B-07', 'B', 'parameter_freedom_ledger', 'FAIL',
        '参数自由度账：可观测量 1 个（Y_B = 8.7e-11），待定量 >= 3 个（β、τ_bg、积分窗口 T_f 或 t_start/t_end），'
        '且 Y_B ∝ ∫τ_bg T^3 dt 中的 T^3 幂次与积分上下限均无出处 => 未知数严格多于约束，'
        '**任一观测值都能被拟合** => 该式不构成预言，属于「先按观测反推参数、再宣称推导」的同型问题')
    add('B-08', 'B', 'anomaly_coefficient_unlocked', 'INFO',
        '1/(16π^2) 系数：既未声明 R̃ 的定义约定（ε-缩并与形式语言之间差 2 的幂次因子），也未给出任何推导；'
        '而它直接乘在全部定量结果上 => 登记为 [C] 外部输入，必须先锁定（连同 C1..C3 / D1..D2）才谈得上 Y_B 定量')


# ---APPEND-HERE---
