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
import io

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
U = lambda L, M, T: (L, M, T)


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


def sec_C():
    # §三 克尔剖面：τ 量纲先核
    # [ω]=T^-1, [ℓ_P²]=L², [1/c]=T/L => [ω ℓ_P²/c] = L ；[a² sin²θ/Σ²] = L²/L⁴ = L^-2
    tau_first = addu(addu(U(0, 0, -1), U(2, 0, 0)), U(-1, 0, 1))   # [ω ℓ_P²/c] = L
    tau_total_unit = addu(tau_first, U(-2, 0, 0))                   # *[a² sin²θ/Σ²]=L^-2 => L^-1
    KEY['kerr'] = {'tau_profile_unit': tau_first, 'tau_total_unit': tau_total_unit}
    add('C-01', 'C', 'tau_profile_dimension_ok', 'PASS',
        'τ(r,θ) 剖面量纲自洽（仅此一格通过）：[ω ℓ_P²/c] = L，[a² sin²θ/Σ²] = L^-2 '
        '=> [τ] = L^-1，与《单位约定与符号规范 v1.0》的台账（[τ]=L^-1）一致')
    # κ = Λ_0 - c τ ：量纲混排
    # [κ]=L^-1, [Λ_0]=L^-1, [c·τ] = (L T^-1)(L^-1) = T^-1
    add('C-02', 'C', 'kappa_def_mixes_dimensions', 'FAIL',
        'κ = Λ_0 - c·τ 量纲混排：左端 [κ]=L^-1，右端第二项 [c·τ] = (L·T^-1)(L^-1) = T^-1，'
        '两项不可相减。同册 §一 又把 c 当作带 β_c 的跑动耦合（跑动量须有量纲），'
        '而本式又要求 c 无量纲才能相减 => c 在两份需求间互斥（登记 O-V34-C）。'
        '《符号规范 v1.0》已把 c 列为 L·T^-1，本式违反该台账')
    # 「κ+τc = Λ_0 是守恒律」实为定义式
    add('C-03', 'C', 'definitional_identity_mislabelled_law', 'FAIL',
        '「κ+τc=Λ_0 是保持常数的强几何守恒律」实为**定义式**而非定律：κ 本就被定义为 Λ_0 - cτ，'
        '二者之和恒等于 Λ_0、与任何机动无关 => 该「守恒律」的信息量为零，属过度陈述（claims 级 over-claim）')
    # 与核心恒等式 κ²+τ²=Ω² 相容性
    # 代入 κ = Λ_0 - cτ（取 c=1 量纲兼容口径），得 (Λ_0-τ)² + τ² = Ω²
    # => 2τ² - 2Λ_0 τ + (Λ_0² - Ω²) = 0 => τ 至多两个与 (r,θ) 无关的常数值
    Lambda0 = 1.0
    c1 = 1.0
    taus = [0.0, 0.2, 0.5, 0.8, 1.0]
    vals = [(Lambda0 - c1 * t) ** 2 + t ** 2 for t in taus]
    mean = sum(vals) / float(len(vals))
    spread_pct = (max(vals) - min(vals)) / mean * 100.0
    KEY['kerr']['core_id_spread_pct'] = spread_pct
    add('C-04', 'C', 'conflict_with_core_identity', 'FAIL',
        '与核心恒等式 κ²+τ²=Ω² 冲突：联立 κ=Λ_0-cτ 得 2τ²-2Λ_0τ+(Λ_0²-Ω²)=0，'
        '是关于 τ 的**常系数二次方程** => τ 至多取两个与 (r,θ) 无关的常数值；'
        '而所设 τ(r,θ) 沿视界连续变化。数值示证（Λ_0=1, c=1，τ/Λ_0 取 0~1 五点）：'
        'κ²+τ² 相对展布 %.2f%% => 两条关系至多取其一：要么放弃非均匀剖面，要么放弃核心恒等式'
        % spread_pct)
    # 熵式对齐 BH 熵 => 确定 Λ_0 所需量纲
    # S_Kerr = 2π Λ_0 A /(ħ c)；Bekenstein-Hawking S = k_B c³ A/(4G ħ)
    # 要求 [Λ_0] + [A] - [ħ c] = [c³]/[4G ħ] （即每面积量纲 L^-2）
    req_Lambda0 = addu(addu(U(2, 0, 0), U(3, 0, -3)), subu(U(0, 0, 0), addu(HB_U, C_U)))
    # = (2,0,0)+(3,0,-3) - (3,1,-2) = (2,0,0) - (3,1,-2) = (-1,-1,2)  -> 即 (M L T^-2)=N
    Fplanck_over_8pi = C_SI ** 4 / (8.0 * math.pi * G_SI)  # = c⁴/(8πG)，单位 N
    KEY['kerr']['req_Lambda0_unit'] = req_Lambda0
    add('C-05', 'C', 'entropy_aligns_to_force_unit', 'FAIL',
        '熵式与 BH 熵对齐的反解：Bekenstein–Hawking 为 S = k_B c³ A/(4G ħ)；使 TUFT 式与其一致须'
        'Λ_0 = c⁴/(8πG) = %.4e N（= 普朗克力/8π），而 §三 的 Λ_0 是曲率、须取 L^-1 '
        '=> **同一 Λ_0 被要求两个互斥量纲**（机器核验所需量纲 = %s 而非台账的 L^-1）。'
        '且这一步是**用已知 BH 熵反解 Λ_0**（逆构造），扣除后新增预言为零'
        % (Fplanck_over_8pi, req_Lambda0))
    add('C-06', 'C', 'entropy_loses_G', 'FAIL',
        '熵式的信息论清算：TUFT 式 S = 2π Λ_0 A/(ħ c) 中**不含 G**；要复现 BH 熵必须令 Λ_0 = c⁴/(8πG)，'
        '即把 G 吸收进 Λ_0。但 Λ_0 在 §三 内无任何取值约束（可任意缩放）'
        '=> 该「TUFT 得 BH 熵」为构造性拟合，不提供独立的引力熵预言；'
        '且 §四 又用 G 作引力耦合，同一框架下 G 既出现又消失，口径不自洽')


def sec_D():
    # §四 坍缩率 Γ ∝ G ∫[(Δκ)+c(Δτ)]² dV
    # 逐项量纲：G=(3,-1,-2); Δκ=L^-1 => (Δκ)²=(-2,0,0); dV=(3,0,0)
    expr = addu(addu(G_U, U(-2, 0, 0)), U(3, 0, 0))  # (4,-1,-2)
    missing = subu(RATE_U, expr)                                # (-4,1,1)
    sol = solve_mix(missing, [G_U, HB_U, C_U])
    KEY['collapse'] = {'expr_unit': expr, 'missing_unit': missing, 'missing_solution': sol}
    add('D-01', 'C', 'collapse_rate_dimension_gap', 'FAIL',
        '坍缩率量纲不足：G∫[(Δκ)+c(Δτ)]² dV 的量纲为 %s（率应为 s^-1 = %s）；'
        '最小补齐因子的量纲为 %s，机器解出 = G^{%d} ħ^{%d} c^{%d} = c⁴/(G² ħ) '
        '=> 补上后 Γ ∝ G·c⁴/(G² ħ) = c⁴/(G ħ)，**Γ 对 G 的依赖由「正比」翻转为「反比」**'
        '（G 越小坍缩越快），与文本「引力驱动坍缩」的单调性相反'
        % (expr, RATE_U, missing, sol[0], sol[1], sol[2]))
    add('D-02', 'D', 'collapse_rate_misses_matter', 'FAIL',
        '坍缩率表达式不含任何物质属性（质量、尺度、自旋、密度 ρ），只含几何场差 Δκ、Δτ；'
        '而文本要区分「微观 vs 宏观」=> 该判别在公式层面无支撑：无物质量纲则无从区分大小，'
        '且 Δκ、Δτ 与物质的**源关系**（κ,τ ← 物质能量动量）从未给出 => 表达式不可算、不可测')
    add('D-03', 'D', 'torsion_term_unfalsifiable', 'FAIL',
        '新增挠率项 c(Δτ)² 是一**自由系数**（c 既是跑动耦合又在此处当放大因子），'
        '任何实验界都可通过调 c 规避 => 在当前状态下该 TUFT 增量**不可证伪**；'
        '要在 §四 产出可检验预言，须先把 c 由作用量变分固定（回链 D-01 量纲修复 + §三 O-V34-C）')
    # 回链：既有 V2 双分量螺旋驻波孤子可证伪性审计、V3.6 动力学挠率终局审计
    add('D-04', 'D', 'backlink_existing_audits', 'INFO',
        '回链：本段「孤子/退相干」命题在既有产物已审计 —— '
        '源码/v_eq_c_TUFT_V2_双分量螺旋驻波孤子_可证伪性审计.py（31 PASS/6 BOUNDARY/0 FAIL）；'
        '源码/TUFT_V3.6_ESCAPE-AUDIT_动力学挠率逃生路线终局审计_2026-10-04.py（结论：动力学挠率每引入 1 个常数即 +1 自由度，'
        '遇 E4/E9 阻塞）。本册不重算，二者结论直接继承：孤子/退相干路线在 TUFT 当前形态下仍属不可证伪或阻塞')


def sec_E():
    # 四候选路线的前置缺口矩阵（有依赖，无打分）
    KEY['routes'] = {
        'r1_kerr_plot': {
            'desc': '克尔剖面二维绘图（等高线）',
            'prereq_open': ['C-03', 'C-04', 'C-05', 'C-06', 'O-V34-C'],
            'value': '仅产出图像',
            'verdict': '可做但价值为零',
            'note': '剖面是定义在式 κ=Λ_0-cτ 上的；该式与核心恒等式 κ²+τ²=Ω² 冲突、且 Λ_0 量纲未定'
                    '=> 画出的图没有判定地位，只是指定函数的可视化'
        },
        'r2_YB_ODE': {
            'desc': 'Y_B 完整 ODE 时间演化积分',
            'prereq_open': ['B-02', 'B-03', 'B-04', 'B-07', 'D2_torsion_dynamics'],
            'value': '最高（有唯一外部靶 Y_B=8.7e-11，且可接标准宇宙学脚手架）',
            'verdict': '阻塞于上游',
            'note': '须先有 τ_bg(t) 的动力学方程；而挠率动力学是 TUFT 已知开放项'
                    '（ESCAPE-AUDIT 结论：引入动力学挠率每 +1 常数、遇 E4/E9 阻塞；C2 仅 Proca 健康）'
                    '且本册 B 段的量纲三重口径必须先闭合'
        },
        'r3_soliton_decoherence': {
            'desc': '孤子退相干时间定量 + 实验判据',
            'prereq_open': ['D-01', 'D-02', 'D-03'],
            'value': '中（可接 Diósi–Penrose 实验边界）',
            'verdict': '当前不可证伪',
            'note': '新增挠率项系数自由 => 任何实验界可规避；须先把 §四 量纲补齐且系数固定'
        },
        'r4_write_paper': {
            'desc': '整合撰写 TUFT V3.4 完整论文（PRD 格式）',
            'prereq_open': ['G0_all'],
            'value': '交付物',
            'verdict': '暂缓',
            'note': '把四条未闭合的 Cauchy 量化缺陷固化成「交付」会污染产物；'
                    '须先完成 G0 关闭清单'
        },
    }
    add('E-01', 'E', 'route1_kerr_plot', 'INFO',
        '路线1（克尔剖面绘图）：可实现，但 C-03/C-04/C-06 未解时，剖面是定义在式 κ=Λ_0-cτ 上的图像，'
        '没有判定地位（只是指定函数的可视化）。前置 = 先解 C-03/C-04 的恒等式冲突与 C-05/C-06 的 Λ_0 口径')
    add('E-02', 'E', 'route2_YB_ODE', 'INFO',
        '路线2（Y_B 全 ODE 演化）：信息价值最高（唯一外靶 Y_B=8.7e-11，可接 H(T)/s(T)/sphaleron 标准脚手架），'
        '但阻塞于两处上游：① τ_bg(t) 动力学方程（挠率动力学，TUFT 已知开放项，ESCAPE-AUDIT 判 +1 常数/遇 E4/E9 阻塞）；'
        '② B 段量纲三重口径与参数自由度账未闭合。=> 当前不可独立执行')
    add('E-03', 'E', 'route3_soliton_decoherence', 'INFO',
        '路线3（孤子退相干 + 实验判据）：可接 Diósi–Penrose 实验边界，但新增挠率项系数自由（D-03），'
        '任何实验界可通过调 c 规避 => 当前不可证伪。前置 = D-01 量纲修复 + 源关系 + 系数固定')
    add('E-04', 'E', 'route4_write_paper', 'INFO',
        '路线4（写 V3.4 论文）：会把四条未闭合的量化缺陷（A~D 共 4 处 FAIL 簇、约 17 条 FAIL）固化成交付；'
        '按既有轮次纪律（体例门禁/收口门禁），应在 G0 完成后才动笔')
    add('E-05', 'E', 'common_prereq_G0', 'INFO',
        '四条路线的共同前置 G0（零/低成本关闭清单，位于「选路」之前）：'
        '① 量纲表闭环（A-02/B-02/B-03/D-01 的缺口，含 β 符号台账 F2 级修复）；'
        '② 符号台账：β 双重重载改名（A-07）、c 的口径登记 O-V34-C；'
        '③ 给出 κ,τ ← 物质的源关系（§四 缺、§三 隐含但未写）；'
        '④ 把 C1..C3 / D1..D2 / 1/(16π²) / Λ_0 / 手征耦合 β / Γ 的量纲因子 登记为 [C] 外部输入并逐项给来源')
    add('E-06', 'E', 'no_scoring_no_choice', 'INFO',
        '红线声明：本册**未对任何路线打分、排序或推荐**（引擎无 score/rank/recommend 字段）；'
        '四路线的取舍权保留给用户。本册只给「依赖矩阵 + 共同前置 G0 + 各路线阻塞点」，'
        '不代选；E-02 vs E-04 一类裁决由用户拍板')


# ===== 自检（约 12 项，全部为机器可读的硬判据）=====
def run_guards():
    guard('uv_constraint_not_satisfied', abs(KEY['uv']['Q']) > 1e-6,
          'A-02：默认系数约束 Q = %.6e ≠ 0' % KEY['uv']['Q'])
    guard('uv_newton_returns_trivial', abs(KEY['uv']['newton_root']) < 1e-20 and KEY['uv']['newton_steps'] >= 50,
          'A-03：示例代码 findroot 实际落到 G* = %.3e（平凡高斯不动点）' % KEY['uv']['newton_root'])
    guard('uv_ray_residuals_zero', KEY['uv']['ray_residual_max'] < 1e-12,
          'A-04：齐次退化构造的系数，4 个 λ 残差均 <= %.1e' % KEY['uv']['ray_residual_max'])
    ft = KEY['finetune_check']
    guard('uv_finetuning_fraction_small', ft['abs_frac'] < 0.05,
          'A-06：随机系数满足约束 |Q|<1e-3 的比例 %.3f%%' % (100.0 * ft['abs_frac']))
    b = KEY['baryon']
    guard('yb_scan_far_above_obs', min(b['scan_YB']) > 1e6 * Y_OBS,
          'B-06：示例 4 组合 Y_B 最小 %.4f > 1e6 × 观测' % min(b['scan_YB']))
    guard('yb_triple_spread_large', b['spread_dex'] > 6.0,
          'B-05：βτ 三个口径跨度 %.2f 个量级' % b['spread_dex'])
    k = KEY['kerr']
    guard('kerr_core_id_spread', k['core_id_spread_pct'] > 10.0,
          'C-04：κ²+τ² 沿视界相对展布 %.2f%%' % k['core_id_spread_pct'])
    guard('kerr_Lambda0_unit_conflict', k['tau_total_unit'] == INV_LEN_U and k['req_Lambda0_unit'] != INV_LEN_U,
          'C-05：Λ_0 在本册须取 ' + str(k['req_Lambda0_unit']) + '、与台账 L^-1 互斥')
    cl = KEY['collapse']
    guard('collapse_missing_solution_found', cl['missing_solution'] == (-2, -1, 4),
          'D-01：最小补齐因子解 G^{%d} ħ^{%d} c^{%d}' % cl['missing_solution'])
    guard('no_scoring_fields', not any('score' in r['item'] or 'rank' in r['item'] or 'recommend' in r['item']
                                      for r in RES),
          'E-06：引擎不含 score/rank/recommend 字段（自检 1/1）')
    guard('determinism_Q', abs(KEY['uv']['Q'] - (C1D * (-D1D / D2D) ** 2 + C2D * (-D1D / D2D) + C3D)) < 1e-15,
          '确定性：Q 两次计算一致')
    return all(g['ok'] for g in GRD)


def write_outputs():
    os.makedirs(DATA, exist_ok=True)
    stamp = time.strftime('%Y-%m-%d')
    base = 'TUFT-V3.4四模块审计与路线选址前置_' + stamp
    counts = {}
    for r in RES:
        counts[r['verdict']] = counts.get(r['verdict'], 0) + 1
    out = {
        'title': 'TUFT V3.4 四模块结构审计 + 路线选址前置（第十七轮）',
        'date': stamp, 'counts': counts, 'results': RES,
        'guards': GRD, 'key_numbers': KEY,
        'routes': KEY.get('routes', {}),
    }
    jpath = os.path.join(DATA, base + '.json')
    with io.open(jpath, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    mpath = os.path.join(DATA, base + '.md')
    with io.open(mpath, 'w', encoding='utf-8') as f:
        f.write('# ' + out['title'] + '\n\n')
        f.write('日期：' + stamp + '\n\n')
        f.write('条目计数：' + '  '.join('%s=%d' % (k, v) for k, v in sorted(counts.items())) + '\n\n')
        f.write('## 条目\n\n')
        for r in RES:
            f.write('- **[%s] %s** `%s/%s` —— %s\n' % (r['verdict'], r['id'], r['section'], r['item'], r['detail']))
        f.write('\n## 自检\n\n')
        for g in GRD:
            f.write('- [%s] %s —— %s\n' % ('PASS' if g['ok'] else 'FAIL', g['name'], g['detail']))
        f.write('\n## 关键数值\n\n')
        f.write('```\n' + json.dumps(KEY, ensure_ascii=False, indent=2) + '\n```\n')
    return jpath, mpath, counts


# ===== 主流程（含 A-06 的随机抽样，须先执行再写 KEY）=====
if __name__ == '__main__':
    import io
    t0 = time.time()
    sec_A()
    sec_B()
    # A-06 随机抽样结果回填到 KEY（供自检读取，不污染来料常数）
    rnd = random.Random(20261007)
    tot = hits = hits_rel = 0
    for _ in range(20000):
        a1 = rnd.uniform(-1, 1); a2 = rnd.uniform(-1, 1); a3 = rnd.uniform(-1, 1)
        b1 = rnd.uniform(-1, 1); b2 = rnd.uniform(-1, 1)
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
    KEY['finetune_check'] = {'samples': tot, 'abs_hits': hits, 'abs_frac': hits / float(tot),
                             'rel_hits': hits_rel, 'rel_frac': hits_rel / float(tot)}
    sec_C()
    sec_D()
    sec_E()
    ok = run_guards()
    jpath, mpath, counts = write_outputs()
    n_fail = counts.get('FAIL', 0)
    n_pass = counts.get('PASS', 0)
    print('\n==== 第十七轮 TUFT V3.4 审计 完成 ====')
    print('条目：' + '  '.join('%s=%d' % (k, v) for k, v in sorted(counts.items())))
    print('自检通过：%s  退出码：%d' % (ok, 0 if ok else 1))
    print('数据产物：\n  ' + jpath + '\n  ' + mpath)
    print('耗时 %.2fs' % (time.time() - t0))
    sys.exit(0 if ok else 1)


# ---APPEND-HERE---
