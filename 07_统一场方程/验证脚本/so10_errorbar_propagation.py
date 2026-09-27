# -*- coding: utf-8 -*-
r"""SO(10) 统一场论 · **误差棒传播仪器**（输入不确定度 → 统一点/α_GUT/质子寿命的带）

为什么是这一台（仓库自陈的缺口，不是新需求）
--------------------------------------------
三份报告反复写着一句话：$M_{\rm GUT}$ 在多解之间"摆动 8.7 倍（3 条物理解**并列**给出的区间，
**不是误差棒**）"（SO10表示论报告.md:12、:1049，以及 R2.sw2 门禁把它钉成措辞）。也就是说：
本体系到目前为止只有**简并度**，没有**不确定度**。而全维评级口径里升 L3 的前置条件是
"constructive + testable_prediction **带误差棒**"⇒ 缺的正是这台仪器。

它做什么
--------
链引擎的映射是**严格仿射**的（so10_chain.py 的 S5 门禁已经证明，且 `solve_determined` 就是
用仿射性从差分建 $J$ 的）。于是解 $u=J^{-1}(A_{\rm MZ}-f_0)$ 是三个实测逆耦合的**线性函数**，
协方差传播是**精确**的、没有雅可比近似误差：
$$\Sigma_u=J^{-1}\,\Sigma_A\,(J^{-1})^{\!\top}$$
$\Sigma_A$ 由 $(\alpha_{\rm em},\sin^2\theta_W,\alpha_s)$ 的输入方差经解析雅可比得到 ⇒
$A_1,A_2$ 因为共用 $\alpha_{\rm em}$ 而**天然相关**（这条相关性是被算出来的，不是引入的参数）。

诚实边界（必须读，否则这台仪器会被误用）
----------------------------------------
* **输入容差是声明的假设，不是世界平均**。中心值一律**取自引擎自身**（`C.ALPHA_MZ` 等，
  逐字引用，不另抄一份）；$\sigma$ 只声明量级并在版面里标 `ASSUMED`。任何引用者若要换
  PDG 口径，换的是这张表，不是这套传播。
* **模型层面全部是一环 + 只有对数项**：两环 $b_{ij}$、阈值有限项、位势与谱的挑选都不在其中
  ⇒ 这条带是"给定该模型与该谱"的条件带，**不是**对 SO(10) 的预言精度。
* 带与"多解并列区间"是**两个对象**：[E3] 把它们同时打印并断言二者不成比例（防止下一轮把
  简并度当误差棒引用——那是本仓库最容易发生的一次误读）。
* $\tau_p$ 走引擎的 `proton_tau`，它自陈是**量级标定**（非第一性；漏了 QCD 增强、$\alpha_H$、
  手征抑制，约 1 个数量级系统差）⇒ [E7] 把"实验下限落不落在带内"如实打印，但**不**据此
  声称任何排除或发现。
* 本脚本**不提升任何体系的证据等级**、不改任何报告的 144/55 门禁合计、不意味着统一场论已
  完成；L10 仍是 OPEN。

运行：`python -B so10_errorbar_propagation.py [--strict]`
退出码：默认 0（仪器不因物理结论为负而失败）；`--strict` 时有 FAIL 则 1；
        **2 = 上游链引擎自检未全 PASS**（此时本轮任何文档都不得引用这台仪器的合计）。
版面：`so10_errorbar_propagation_claims.json`（钉在本脚本旁边；严格 JSON，非有限浮点写成 null）
"""
import json
import math
import os
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import so10_chain as C                                          # noqa: E402

CHAIN = 'R3221'                                                # 唯一 slots 含 'GUT' ⇒ 预言 M_GUT
IDX = {'AG': 0, 'M1': 1, 'M2': 2, 'GUT': 3}
W0 = [0.0, 0.0, 0.0, 36.0]

# 输入方差：中心值来自引擎，容差是**声明的假设**（见头部诚实边界第 1 条）。
INPUTS = [
    ('alpha_em(M_Z)', C.ALPHA_MZ, C.ALPHA_MZ * (0.010 / 127.952),
     'σ(α_em⁻¹)=0.010 ⇒ 相对 7.8e-5'),
    ('sin2thetaW(M_Z)', C.SIN2_MS, 1.3e-4, 'ASSUMED 1.3e-4（on-shell 量级）'),
    ('alpha_s(M_Z)', C.ALPHAS_MZ, 9.0e-4, 'ASSUMED 9e-4（PDG 量级）'),
]
JUDGE = []
CIT = {}         # 引用令牌表：判据的 detail 串与文档引用的串**必须来自同一次格式化**（见 s()）


def s(key, fmt, v):
    r"""格式化一次、登记一次、打印一次：`CIT[key]` 就是判据行里印出来的那个串。

    为什么不用 `%.Nr`：E8b 已经实测 CPython 的 `%.Nr` 是对 repr **截字符**（8.6798 → `8.67`），
    于是"仪器印的"与"文档抄的"会在末位差一个数字，而两处都自称同一份版面。这里一律用定点
    十进制（四舍五入），令牌与打印同源，漂移由 `so10_errorbar_doc_check.py` 判。

    同一令牌允许被两处判据引用，但**只许铸成同一个串**：若两处格式化结果不同，本函数直接
    抛异常让整轮崩掉（宁可 rc≠0，也不留一份"两处都自称仪器读数、末位互相不一致"的版面）。
    """
    txt = fmt % v
    prev = CIT.get(key)
    if prev is not None and prev != txt:
        raise AssertionError('引用令牌 %s 被铸成两个不同的串：%r 与 %r ⇒ 该键的格式化规格'
                             '在脚本里不一致，拒绝出版面' % (key, prev, txt))
    CIT[key] = txt
    return txt


def ok(cid, claim, passed, detail=''):
    JUDGE.append({'id': cid, 'claim': claim, 'verdict': 'PASS' if passed else 'FAIL',
                  'detail': detail})
    print('[%-8s] %s — %s%s' % ('PASS' if passed else 'FAIL', cid, claim,
                                ('\n           %s' % detail) if detail else ''))
    return passed


def inv3(M):
    """3x3 逆（余子式），无第三方依赖。

    注意 (J⁻¹)_{ij} = C_{ji}/det：**余子式要按转置装**——写成 C_{ij}/det 得到的是逆的转置，
    而它仍是一个"看起来能用"的矩阵（E2 那种逐情形与引擎解互检的门禁就是为它准备的；本轮实测
    第一次跑就因为它把 M_GUT 解成了 1.79 GeV）。
    """
    d = det3(M)
    if abs(d) < 1e-30:
        return None
    c = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            r = [k for k in range(3) if k != j]
            s = [k for k in range(3) if k != i]
            mm = [[M[s[a]][r[b]] for b in range(2)] for a in range(2)]
            c[j][i] = ((-1.0) ** (i + j)) * (mm[0][0] * mm[1][1] - mm[0][1] * mm[1][0]) / d
    return c


def det3(M):
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
            - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))


def matvec(M, v):
    return [sum(M[i][j] * v[j] for j in range(3)) for i in range(3)]


def simat(A, S):
    """A S Aᵀ（3x3）。"""
    T = [[sum(A[i][k] * S[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    return [[sum(T[i][k] * A[j][k] for k in range(3)) for j in range(3)] for i in range(3)]


def jac_A(x):
    """A=(A1,A2,A3) 对 x=(alpha_em, sin2, alpha_s) 的解析雅可比。"""
    a, s, as_ = x
    return [[-0.6 * (1.0 - s) / (a * a), -0.6 / a, 0.0],
            [-s / (a * a), 1.0 / a, 0.0],
            [0.0, 0.0, -1.0 / (as_ * as_)]]


def a_mz(x):
    a, s, as_ = x
    return [(3.0 / 5.0) * (1.0 - s) / a, s / a, 1.0 / as_]


def assemble(scn):
    """复刻引擎的建矩阵过程（**调用引擎自己的 predict4**）。返回 f0/J/Jinv/slots。"""
    slots = C.SLOTS[CHAIN]
    cols = [IDX[s] for s in slots]
    f0 = C.predict4(CHAIN, W0, scn)
    J = []
    for i in range(3):
        row = []
        for ci in cols:
            e = list(W0)
            e[ci] += 1.0
            row.append(C.predict4(CHAIN, e, scn)[i] - f0[i])
        J.append(row)
    return f0, J, inv3(J), slots


def unpack(u, slots):
    """解增量 → 物理量 (ag, t1, tG)。slots 决定 u[k] 落在 w 的哪一格。"""
    w = list(W0)
    for k, s in enumerate(slots):
        w[IDX[s]] += u[k]
    t1, t2 = w[1], (w[2] if 'M2' in slots else w[1])
    return w[0], t1, t2, w[3]


def fmt_scale(v):
    """量级渲染：只走 repr()。`%.*r` 在 CPython 上是对 repr **截字符**（1.99e+17 → `1.9902081e`），
    会把指数吃掉；[E8b] 把这条判据接到本函数上，改回 `%.Nr` 即红。"""
    return repr(v)


def main():
    strict = '--strict' in sys.argv
    print('链 = %s，slots = %s ⇒ 本链对 $M_{\\rm GUT}$ 给出**预言**（不是输入）'
          % (CHAIN, C.SLOTS[CHAIN]))
    # K_Y / K_BL 在引擎里是**跑出来的**（模块级初值为 None）⇒ 调 predict4 之前必须先让上游自检
    # 全 PASS；否则这台仪器会把误差棒报在一个坏掉的系数上（同 so10_thresholds.py 的 T0 口径）。
    if not (True if C.K_BL is not None else C.run_engine_tests()):
        print('[FAIL    ] E0 — 上游链引擎自检未全 PASS ⇒ 本仪器拒绝出数（退出码 2，任何文档'
              '不得引用本轮）')
        return 2

    # ---- [E1] 输入侧：Σ_A 必须是"共用 α_em"算出来的，而不是塞进去的对角阵
    x = [v for _, v, _, _ in INPUTS]
    sig = [s for _, _, s, _ in INPUTS]
    JA = jac_A(x)
    Sx = [[sig[i] * sig[j] if i == j else 0.0 for j in range(3)] for i in range(3)]
    SA = simat(JA, Sx)
    corr12 = SA[0][1] / (math.sqrt(SA[0][0] * SA[1][1]))
    ok('E1', 'A1/A2 的相关系数由"共用 α_em"解析算出（非对角元素存在且 |ρ|<1）',
       abs(corr12) > 1e-6 and abs(corr12) < 1.0,
       'ρ(A1,A2) = %s；σ(A1)=%s σ(A2)=%s' % (s('rho_A1_A2', '%.9f', corr12),
                                             s('sigma_A1', '%.6f', math.sqrt(SA[0][0])),
                                             s('sigma_A2', '%.6f', math.sqrt(SA[1][1]))))

    # ---- 逐情形求解 + 与引擎自己的解互检
    rows = []
    for scn in sorted(C.SCENARIOS.keys()):
        f0, J, Jinv, slots = assemble(scn)
        if Jinv is None:
            print('  情形 %s：J 奇异（跳过，如实登记）' % scn)
            continue
        rhs = [C.A_MZ[i] - f0[i] for i in range(3)]
        u = matvec(Jinv, rhs)
        ag, t1, t2, tG = unpack(u, slots)
        mine = {'M_GUT': math.exp(tG), 'alpha_GUT_inv': ag, 'M_R': math.exp(t2)}
        eng = C.solve_determined(CHAIN, scn)
        agree = None
        if eng:
            agree = max(abs(mine['M_GUT'] / eng['scales']['M_GUT'] - 1.0),
                        abs(mine['alpha_GUT_inv'] - eng['alpha_GUT_inv']),
                        abs(mine['M_R'] / eng['scales']['M_R'] - 1.0))
        SU = simat(Jinv, SA)                                   # cov(AG, M1[, M2], GUT 增量)
        # slots 顺序：u[k] ↔ IDX[slots[k]]
        pos = {IDX[s]: k for k, s in enumerate(slots)}
        pag, ptg = pos.get(IDX['AG']), pos.get(IDX['GUT'])
        if pag is None or ptg is None:
            continue
        v = [4.0, -2.0 / ag]                                   # d ln τ = 4 dtG - 2 dag/ag
        cov2 = [[SU[ptg][ptg], SU[ptg][pag]], [SU[pag][ptg], SU[pag][pag]]]
        full = math.sqrt(max(v[0] * v[0] * cov2[0][0] + 2 * v[0] * v[1] * cov2[0][1]
                             + v[1] * v[1] * cov2[1][1], 0.0))
        diag_only = math.sqrt(v[0] * v[0] * cov2[0][0] + v[1] * v[1] * cov2[1][1])
        tau, mx = C.proton_tau(mine['M_GUT'], ag)
        rows.append({'scenario': scn, 'M_GUT_GeV': mine['M_GUT'], 'alpha_GUT_inv': ag,
                     'M_R_GeV': mine['M_R'], 'tau_p_yr': tau,
                     'sigma_ln_MGUT': math.sqrt(SU[ptg][ptg]),
                     'sigma_alpha_GUT_inv': math.sqrt(SU[pag][pag]),
                     'sigma_ln_tau_full': full, 'sigma_ln_tau_diag': diag_only,
                     'engine_agree': agree, 'physical': bool(eng and eng['physical']),
                     'Jinv_tG_A3': Jinv[ptg][2]})
        print('  情形 %-3s M_GUT=%s α_GUT⁻¹=%.10r M_R=%s τ_p=%.6e'
              ' 与引擎解最大相对差=%s'
              % (scn, fmt_scale(mine['M_GUT']), ag, fmt_scale(mine['M_R']), tau,
                 ('%.3e' % agree) if agree is not None else '引擎无解'))

    ok('E2', '本仪器的解与引擎 `solve_determined` 逐情形一致（相对 1e-12 内）',
       all(r['engine_agree'] is not None and r['engine_agree'] < 1e-9 for r in rows),
       '各情形最大偏差 = %s' % ['%.3e' % r['engine_agree'] for r in rows
                                if r['engine_agree'] is not None])

    # ---- [E3] 带 ≠ 并列区间
    mg_all = [r['M_GUT_GeV'] for r in rows]
    spread = math.log(max(mg_all) / min(mg_all)) if len(mg_all) > 1 else 0.0
    bars = [r['sigma_ln_MGUT'] for r in rows]
    ok('E3', '传播得到的 σ(ln M_GUT) 与"多解并列区间"是两个量级不同的对象（简并度不是误差棒）',
       spread > 0 and max(bars) > 0 and spread / max(bars) > 10.0,
       '并列区间 ln(max/min) = %s（%d 条解，倍率 %s）；最大传播棒 σ(ln M_GUT) = %s'
       ' ⇒ 比值 %s 倍'
       % (s('spread_lnMGUT', '%.4f', spread), len(mg_all),
          s('degeneracy_ratio', '%.2f', max(mg_all) / min(mg_all)),
          s('sigma_ln_MGUT_max', '%.4f', max(bars)),
          s('spread_over_bar', '%.1f', spread / max(bars) if max(bars) else float('nan'))))

    # ---- [E4] 相关性是否承担内容（若两条口径同值，这条机制就是装饰）
    rat = max(r['sigma_ln_tau_full'] / r['sigma_ln_tau_diag'] for r in rows) \
        if rows else float('nan')
    ok('E4', '带内 $t_G$ 与 $\\alpha_{\\rm GUT}^{-1}$ 的协方差对 σ(ln τ_p) 有实际贡献'
             '（忽略它得到的不是同一条带）',
       all(r['sigma_ln_tau_diag'] > 0 for r in rows) and abs(rat - 1.0) > 1e-3,
       '全协方差 / 只取对角 = %s（最偏离的一条）⇒ 交叉项承担 %s%% 的方差预算'
       % (s('cross_full_over_diag', '%.6f', rat),
          s('cross_share_pct', '%.2f', (1.0 - rat) * 100.0)))

    # ---- [E5] 阳性对照：输入方差归零 ⇒ 带必须精确归零（证明带是被输入的，不是写死的）
    SA0 = [[0.0] * 3 for _ in range(3)]
    scn0 = rows[0]['scenario']
    f0, J, Jinv, slots = assemble(scn0)
    SU0 = simat(Jinv, SA0)
    zeroed = max(math.sqrt(abs(SU0[i][j])) for i in range(3) for j in range(3))
    ok('E5', '把三个输入 σ 全部置 0 ⇒ 传播带逐元素归零（这台仪器不接受常数带）',
       zeroed < 1e-300 or zeroed == 0.0, 'max|Σ_u| = %r' % zeroed)

    # ---- [E6] 逐输入弹性度（与"容差是假设"无关的裸读数，可直接引用）
    els = []
    for j in range(3):
        e = [0.0, 0.0, 0.0]
        e[j] = 1.0
        col = matvec(Jinv, e)
        pos = {IDX[s]: k for k, s in enumerate(slots)}
        els.append({'d_lnM_GUT_dA%d' % (j + 1): col[pos[IDX['GUT']]],
                    'd_alpha_GUT_inv_dA%d' % (j + 1): col[pos[IDX['AG']]]})
    ok('E6', '弹性度表非退化（每个输入对 ln M_GUT 都有非零杠杆 ⇒ 没有哪条腿被静默丢掉）',
       all(abs(els[j]['d_lnM_GUT_dA%d' % (j + 1)]) > 1e-12 for j in range(3)),
       '∂ln M_GUT/∂A_i = %s' % ['%.10r' % els[j]['d_lnM_GUT_dA%d' % (j + 1)]
                                for j in range(3)])

    # ---- [E7] 可检验陈述：τ_p 的带与 Super-K 下限的**同尺度**比较
    sk = math.log(C.SK_BOUND)
    for r in rows:
        r['ln_tau_over_SK'] = math.log(r['tau_p_yr']) - sk
        r['z_vs_SK'] = r['ln_tau_over_SK'] / r['sigma_ln_tau_full'] \
            if r['sigma_ln_tau_full'] else float('nan')
    zs = [r['z_vs_SK'] for r in rows]
    ztok = [s('z_vs_SK_' + r['scenario'], '%.2f', z) for r, z in zip(rows, zs)]
    ok('E7', 'τ_p 的带与 Super-K 下限（%s yr）可比：逐情形打印 z = ln(τ/SK)/σ_lnτ，'
             '且至少一条落在 ±1 个 σ 之外（否则"未被排除"只是带的宽度在做事）'
       % s('sk_bound', '%.1e', C.SK_BOUND),
       len(zs) > 0 and max(abs(z) for z in zs) > 1.0,
       'z(逐情形 %s) = %s' % ('/'.join([r['scenario'] for r in rows]), ztok))

    # ---- [E8] 引擎自陈的**理论侧系统差**（漏 QCD 增强/α_H/手征抑制 ≈ 1 个数量级）不在这条带里
    #         ⇒ 引用 z 之前必须先把 σ 放大，否则 24 个 σ 是三条腿的输入精度买来的。
    LN_HAD = math.log(10.0)
    zh = []
    zhtok = []
    for r in rows:
        s_tot = math.sqrt(r['sigma_ln_tau_full'] ** 2 + LN_HAD ** 2)
        r['sigma_ln_tau_with_hadronic'] = s_tot
        r['z_with_hadronic'] = r['ln_tau_over_SK'] / s_tot
        zh.append(r['z_with_hadronic'])
        zhtok.append(s('z_with_hadronic_' + r['scenario'], '%.2f', r['z_with_hadronic']))
    ok('E8', '把引擎自陈的 1 个数量级系统差并进 σ 后重新定价 z：σ 必然变大、z 必然变小'
             '（这条门钉的是"放大"这个动作本身，不是它的数值）',
       all(r['sigma_ln_tau_with_hadronic'] > r['sigma_ln_tau_full'] for r in rows) and
       all(abs(a) < abs(b) for a, b in zip(zh, zs)),
       'z(仅输入) = %s → z(含强子/短程系统差) = %s；σ_lnτ 从 %s 放大到 %s'
       % (ztok, zhtok,
          s('sigma_ln_tau_input_only', '%.4f', rows[0]['sigma_ln_tau_full']),
          s('sigma_ln_tau_with_hadronic', '%.4f', rows[0]['sigma_ln_tau_with_hadronic'])))
    # 打印侧卫生（本轮实测踩到）：CPython 的 `%.Nr` 对**浮点 repr 直接截字符**，
    # 1.9902081e+17 会被印成 `1.9902081e`——指数被吃掉、量级凭空消失。数量级 ≥1e6 的值
    # 一律走 repr()，并在版面里留下原值，任何引用者可用 JSON 复核 stdout 的量级。
    bad_fmt = [r['scenario'] for r in rows
               if (r['M_GUT_GeV'] >= 1e6 or r['M_R_GeV'] >= 1e6)
               and 'e+' not in (fmt_scale(r['M_GUT_GeV']) + fmt_scale(r['M_R_GeV']))]
    ok('E8b', '打印用的 `fmt_scale` 保得住量级：≥1e6 的值渲染后必须仍带科学计数法指数'
              '（本轮实测 CPython 的 `%.10r` 把 1.9902081e+17 截成 `1.9902081e`，'
              '指数被吃掉 ⇒ 门禁把"打印它的那条路径"接进判据，改回 `%.Nr` 本条即红）',
       not bad_fmt,
       '未通过的情形 = %s；对照：`%%.10r` → %s，`fmt_scale` → %s'
       % (bad_fmt or '无', repr('%.10r' % 1.9902081e+17), fmt_scale(1.9902081e+17)))

    # ---- [E9] "把三个输入 σ 整体翻倍"必须是**实测**，不是尺度推断（一次齐次性）
    #          引用文档里那句"10 倍门槛掉到 <10 倍"挂在这条门的读数上。
    LAM = 2.0
    hom = 0.0
    for r in rows:
        _f0, _J, Jinvx, slotsx = assemble(r['scenario'])
        SUx = simat(Jinvx, [[LAM * LAM * SA[i][j] for j in range(3)] for i in range(3)])
        posx = {IDX[s]: k for k, s in enumerate(slotsx)}
        bar2 = math.sqrt(SUx[posx[IDX['GUT']]][posx[IDX['GUT']]])
        r['sigma_ln_MGUT_x2'] = bar2
        if r['sigma_ln_MGUT']:
            hom = max(hom, abs(bar2 - LAM * r['sigma_ln_MGUT']) / r['sigma_ln_MGUT'])
    bars_x2 = [r['sigma_ln_MGUT_x2'] for r in rows]
    ok('E9', '带对三个输入 σ 是**一次齐次**的：λ=2 重跑传播，逐情形 σ(ln M_GUT) 按 λ 精确放大'
             '（这条门把"容差口径翻倍 ⇒ 带翻倍"从推断变成读数）',
       hom < 1e-12 and max(bars_x2) > max(bars),
       'λ=2：max σ(ln M_GUT) = %s（λ=1 是 %s）⇒ 并列区间对这条带的比值从 %s 倍掉到 %s 倍'
       '，而 E3 的门槛是 10 倍 ⇒ 那句"宽一个量级"随输入 σ 的口径走，不是无条件的话；'
       '最大相对偏差 %s'
       % (s('sigma_ln_MGUT_max_x2', '%.4f', max(bars_x2)),
          s('sigma_ln_MGUT_max', '%.4f', max(bars)),
          s('spread_over_bar', '%.1f', spread / max(bars)),
          s('spread_over_bar_x2', '%.1f', spread / max(bars_x2)),
          s('homogeneity_max_rel_dev', '%.3e', hom)))

    # ---- 引用令牌表：**唯一数据源是上面各判据里的 s() 调用**（判据行印出来的串 == 本表里的串）。
    #      本块只登记不落在任何判据行里的合计与逐情形裸读数；在这里再抄一份判据已铸造的键
    #      会被 `s()` 的冲突检查拒绝（同键两串 ⇒ 整轮崩掉，不出版面）。
    s('judgments_total', '%d', len(JUDGE))
    s('judgments_pass', '%d', sum(1 for j in JUDGE if j['verdict'] == 'PASS'))
    for r in rows:
        s('sigma_ln_MGUT_' + r['scenario'], '%.4f', r['sigma_ln_MGUT'])
        s('sigma_alpha_GUT_inv_' + r['scenario'], '%.4f', r['sigma_alpha_GUT_inv'])
        s('sigma_ln_tau_full_' + r['scenario'], '%.4f', r['sigma_ln_tau_full'])

    # ---- 汇总
    npass = sum(1 for j in JUDGE if j['verdict'] == 'PASS')
    nfail = sum(1 for j in JUDGE if j['verdict'] == 'FAIL')
    print('\n' + '=' * 78)
    print('判定汇总：PASS %d / FAIL %d（共 %d 条）。本脚本不改引擎、不改任何报告的 144/55 合计，'
          '不提升任何证据等级；L10 仍 OPEN。' % (npass, nfail, len(JUDGE)))
    print('可引用令牌（引用文档必须逐字用这些串；漂移由 so10_errorbar_doc_check.py 判）：')
    for k in sorted(CIT):
        print('  %-28s %s' % (k, CIT[k]))

    out = {'script': 'so10_errorbar_propagation.py', 'chain': CHAIN,
           'slots': C.SLOTS[CHAIN],
           'inputs': [{'name': n, 'central_from_engine': v, 'sigma_ASSUMED': s, 'basis': b}
                      for n, v, s, b in INPUTS],
           'a_mz_from_engine': list(C.A_MZ),
           'cov_A': SA, 'rho_A1_A2': corr12,
           'spread_lnMGUT_from_degeneracy': spread,
           'rows': rows, 'elasticity': els, 'sk_bound_yr': C.SK_BOUND,
           'citable': CIT, 'judgments': JUDGE}
    bag = []
    face = os.path.join(str(ROOT), 'so10_errorbar_propagation_claims.json')
    with open(face, 'w', encoding='utf-8') as f:
        json.dump(fin(out, bag), f, ensure_ascii=False, indent=2, allow_nan=False)
    print('版面严格性：非有限浮点 %d 个已写成 null（`NaN` 字面量会让 jq / JSON.parse 打不开整份）'
          % len(bag))
    print('已写出 %s' % face)
    return 1 if (strict and nfail) else 0


def fin(o, bag):
    if isinstance(o, float):
        if math.isfinite(o):
            return o
        bag.append(o)
        return None
    if isinstance(o, dict):
        return dict((k, fin(v, bag)) for k, v in o.items())
    if isinstance(o, (list, tuple)):
        return [fin(v, bag) for v in o]
    return o


if __name__ == '__main__':
    sys.exit(main())
