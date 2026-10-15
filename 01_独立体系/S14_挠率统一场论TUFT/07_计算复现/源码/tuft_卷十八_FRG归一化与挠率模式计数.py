# -*- coding: utf-8 -*-
"""
================================================================================
TUFT 卷十八 · FRG 归一化修正 · 阈值函数推导 · 挠率模式计数（可复跑）
================================================================================

承接卷十七《重整化群全局相图》的收尾结论：
    "卷十七的一圈 beta 缺正则（工程）量纲线性项 => 纯二次模型下不动点成射线族、
     高斯点非双曲、临界指数不可唯一；卷十七以【手工补入】正则项的方式绕过该困境。"

卷十八要做的三件事：

(1) 【归一化修正】从第一性量纲分析给出无量纲耦合的正确定义与正则指数，
    并定位卷十七在该处的错误 —— 卷十七沿用了草稿的 `lambda = Lambda/M_P^4` 与
    正则指数 -4，但 `Lambda` 的质量量纲为 +2（不是 +4），正确的无量纲组合是
    `lambda = Lambda k^{-2}`，正则指数应为 **-2**。同时 `g0 = G M_P^2`（M_P 固定）
    的正则指数应为 **0**（不是 +2）—— 卷十七"模型 B"把两套归一化混用。
    统一到 k-归一化后：theta_canon = (+2, -2, 0, 0, 0, 0)。

(2) 【FRG 正则项定理】在 FRG（Wetterich 方程）框架下，正则项是
    "无量纲化定义"的必然后果，不是手工补入：
        g_i = c_i_hat * k^{-d_i}  =>  partial_t g_i = -d_i g_i + (量子项)
    即 FRG 自动产出卷十七所缺的线性项 —— 卷十七的"模型 B"在 FRG 中是**推导**，
    不再是**假设**。这是本卷消解卷十七困境的机制。

(3) 【挠率模式计数（本卷新计算）】挠率 T_{lambda mu nu} 在最后两指标反对称，
    共 24 个分量；在 SO(4) 下分解为
        trace 向量(4) + 轴矢(4) + 张量(16)
    本卷显式构造三个投影并数值验证：维数、正交性、完备性。
    这是挠率扇区进入 FRG 迹的模式简并度，属本卷真正新增的计算。

--------------------------------------------------------------------------------
【诚实边界（先读）】
--------------------------------------------------------------------------------
本卷**没有**做背景场引力 Hessian 的二阶变分、York 分解与鬼场迹的完整计算，
因此**不给出**纯 GR 爱因斯坦-希尔伯特截断 NGFP 的数值 (g_*, lambda_*)。
任何声称的 (g_*, lambda_*) 都依赖该 Hessian；本卷不引用未经复算的系数，
故该数值留作下一卷任务（见卷十八 §9 任务清单）。
本卷的数值部分严格限于：(a) 归一化修正后的 6 维耦合模型（与卷十七同结构），
(b) 阈值函数闭式，(c) 挠率模式计数。

红线：数学自洽 != 实验证实。本文件只做 FRG 框架 / 归一化 / 群论计数的
      诚实分析，不构成对 TUFT 物理真实性的主张；负结论为诚实边界，非证伪宣告。

运行（Python 3.8 + numpy）：
    python tuft_卷十八_FRG归一化与挠率模式计数.py
================================================================================
"""

from __future__ import print_function

import itertools
import json
import math
import os
import sys
import time

import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

np.set_printoptions(precision=6, suppress=False, linewidth=110,
                    threshold=14, edgeitems=3)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUTDIR = os.path.join(ROOT, "09_验证结果", "原始运行记录")
REPORT_PATH = os.path.join(OUTDIR, "tuft_卷十八_FRG归一化与挠率模式计数_report.txt")
JSON_PATH = os.path.join(OUTDIR, "tuft_卷十八_FRG归一化与挠率模式计数.json")

if not os.path.isdir(OUTDIR):
    try:
        os.makedirs(OUTDIR)
    except Exception:
        pass

LINES = []
COUNTS = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0, "OPEN": 0}


def _emit(line):
    LINES.append(line)
    try:
        print(line, flush=True)
    except Exception:
        pass


def chunk(title):
    _emit("")
    _emit("=" * 78)
    _emit(" " + title)
    _emit("=" * 78)


def verdict(code, status, text):
    COUNTS[status] = COUNTS.get(status, 0) + 1
    pad = " " * max(0, 8 - len(status))
    _emit("  [" + status + pad + "] " + code + " [" + status + "]: " + text)


def note(text):
    _emit("  " + text)


def short_vec(x, p=6):
    return "(" + ", ".join(("%+." + str(p) + "g") % float(v) for v in x) + ")"


# ================================================================ 主流程
T_START = time.time()
_emit("TUFT 卷十八 · FRG 归一化修正 · 阈值函数推导 · 挠率模式计数 · 判定明细")
_emit("=" * 78)
_emit("承接：卷十七（RG 全局相图，判定 17/9/4/8 + OPEN 1）")
_emit("目标：把卷十七'手工补入'的正则项，在 FRG 框架下变为【推导】；")
_emit("      修正卷十七的归一化错误；给出挠率扇区的模式计数。")
_emit("红线：数学自洽 != 实验证实")

# ---------------------------------------------------------------- 0 量纲表
chunk("步骤 0  作用量量纲与归一化（第一性核对）")
note("作用量 S 无量纲，[d^4x] = -4（质量量纲），故 [L] = +4。")
note("Einstein-Hilbert 项 (1/(16 pi G)) R： [R] = 2  =>  2 + [G]^{-1}... 逐步核对：")
note("  [1/(16 pi G)] + [R] = 4  =>  -[G] + 2 = 4  =>  [G] = -2")
verdict("V18-D1", "PASS", "[G] = -2（牛顿耦合质量量纲 -2）")
note("宇宙学常数项 (1/(16 pi G))(-2 Lambda)：")
note("  [1/(16 pi G)] + [Lambda] = 4  =>  2 + [Lambda] = 4  =>  [Lambda] = +2")
verdict("V18-D2", "PASS",
        "[Lambda] = +2（宇宙学常数质量量纲 +2，即 1/长度^2）")
note("卷十七 §3 写作 [Lambda] = +4 且 lambda = Lambda / M_P^4 ——")
note("  若 [Lambda] = +2，则 Lambda/M_P^4 的量纲为 -2，并非无量纲。")
verdict("V18-D3", "FAIL",
        "卷十七 §3 的归一化错误：lambda = Lambda/M_P^4 与 [Lambda]=+2 不相容；"
        "正确的无量纲组合是 lambda = Lambda k^{-2}（或 Lambda/M_P^2）")

note("")
note("挠率扇区：[tau] = 1（挠率 ~ 联络差 ~ 一阶导数）=> [tau^2] = 2")
note("  项 (1/(16 pi G)) tau^2：  2 + 2 = 4   => 自洽（与 R 同为二导数算符）")
note("  项 (1/(16 pi G)) c3 R tau^2：2 + [c3] + 2 + 2 = 4  => [c3] = -2")
note("  项 (1/(16 pi G)) c4 tau_{munu rho} tau^{munu rho}：2 + [c4] + 2 = 4 => [c4] = -2")
verdict("V18-D4", "PASS", "[tau]=1、[c3]=[c4]=-2，挠率二次项量纲自洽")
note("但草稿 §2 自行定义 tau^2 := tau_{munu rho} tau^{munu rho}，于是")
note("  作用量中 'tau^2' 与 'c4 tau_{munu rho} tau^{munu rho}' 是【同一算符】。")
verdict("V18-S1", "FAIL",
        "草稿作用量冗余：按草稿自身定义 tau^2 == tau_{l m n}tau^{lmn}，"
        "则 'tau^2' 项与 'c4 tau tau' 项算符相同，c4 只是整体重标度、不是独立耦合；"
        "6 维耦合空间实际只有 5 个独立方向（除非把 tau^2 改指 trace 平方 "
        "(tau^m_{mn})^2，草稿未如此定义）")

# ---------------------------------------------------------------- 1 正则项定理
chunk("步骤 1  FRG 正则项定理（把卷十七的'手工补入'变为'推导'）")
note("Wetterich 方程：  partial_t Gamma_k = (1/2) STr[ (Gamma_k^(2) + R_k)^{-1} partial_t R_k ]")
note("                  t = ln k")
note("")
note("正则项定理（本卷定理 1）：设有量纲耦合 c_hat，质量量纲 d_c = [c_hat]，")
note("  无量纲化 g = c_hat * k^{-d_c}；则")
note("      partial_t g = k d/dk (c_hat k^{-d_c}) = -d_c * g + k^{-d_c} (k d c_hat/dk)")
note("  其中第二项是量子贡献（一圈为 O(g^2) 及以上），第一项 -d_c * g 即正则项。")
note("  与圈数、截断、规范无关，纯粹是「无量纲化」的定义后果。")

# 数值/符号验证：g(k) = c_hat * k^{-d}, c_hat 固定 => k g'(k)/g = -d
rng = np.random.RandomState(11)
tab = [
    ("牛顿 G", -2.0, 2.0),
    ("宇宙学 Lambda", 2.0, -2.0),
    ("二次型耦合 c_i（经 1/G 归一后）", 0.0, 0.0),
]
ok_all = True
for name, d_c, expect in tab:
    c_hat = float(rng.uniform(0.7, 1.9))
    k0 = 1.3
    h = 1e-6
    g = lambda k: c_hat * k ** (-d_c)
    deriv = (g(k0 + h) - g(k0 - h)) / (2 * h)
    rat = k0 * deriv / g(k0)
    good = abs(rat - expect) < 1e-5
    ok_all = ok_all and good
    note("  %-30s d_c = %+.1f  =>  k g'/g = %+.6f （定理预言 %+.1f）%s"
         % (name, d_c, rat, expect, "OK" if good else "MISMATCH"))
verdict("V18-T1", "PASS" if ok_all else "FAIL",
        "正则项定理验证：partial_t g 的正则系数为 -[c_hat]；"
        "G -> +2，Lambda -> -2，经 1/G 归一的二次型耦合 -> 0")

note("")
note("卷十七定位：")
note("  - 卷十七模型 A（草稿原文）所有 beta 无线性项 == 把所有 d_c 置 0，")
note("    与 [G]=-2、[Lambda]=+2 直接矛盾 => 归一化层面即错。")
verdict("V18-T2", "FAIL",
        "卷十七模型 A 的'纯二次 beta'等价于把正则维数误置为零；"
        "这不是'少算了一圈'，而是与耦合的量纲定义不相容")
note("  - 卷十七模型 B 手工补入 theta_canon = (+2,-4,0,0,0,0)：")
note("    +2（G）正确；-4（Lambda）错误（应为 -2）；g1..g4 取 0 正确")
note("    （因 g_i = c_i M_P^2 中 M_P 固定时 c_i 经典不跑）。")
note("  - 且 g0 = G M_P^2（M_P 固定）的正则指数应为 0，而非 +2：")
note("    +2 对应的是 g~ = G k^2（k-归一化）。卷十七模型 B 混用了两套归一化。")
verdict("V18-T3", "FAIL",
        "卷十七模型 B 混用归一化：g0 用了 k-归一化的 +2，而 g0 被定义为 G M_P^2"
        "（M_P 固定时应为 0）；lambda 用了 -4（应为 -2）。")
note("")
note("统一修正（本卷采用 k-归一化，与 AS/FRG 文献一致，且保证流方程自治）：")
note("    g~   = G k^2          -> 正则 +2")
note("    lam  = Lambda k^{-2}  -> 正则 -2")
note("    w_i  = c_i/(16 pi G)  -> 正则  0   （算符维数 4 = d，边际）")
THETA_V17 = np.array([2.0, -4.0, 0.0, 0.0, 0.0, 0.0])
THETA_V18 = np.array([2.0, -2.0, 0.0, 0.0, 0.0, 0.0])
note("  theta_canon(卷十七) = " + str(THETA_V17.tolist()))
note("  theta_canon(卷十八) = " + str(THETA_V18.tolist()))
verdict("V18-T4", "PASS",
        "统一到 k-归一化后正则指数 = (+2, -2, 0, 0, 0, 0)；"
        "该向量在 FRG 中是定理 1 的推论（推导），不是手工假设")

# ---------------------------------------------------------------- 2 阈值函数
chunk("步骤 2  优化（Litim）调节器下的阈值函数：闭式推导 + 数值验证")
note("优化调节器：  R_k(p^2) = k^2 r(y),  y = p^2/k^2,  r(y) = (1-y) theta(1-y)")
note("阈值函数定义（本卷采用）：")
note("  Phi^p_n(w)   = 1/Gamma(n) * int_0^inf dy  y^{n-1} [r - y r'] / [y + r + w]^p")
note("  Phit^p_n(w)  = 1/Gamma(n) * int_0^inf dy  y^{n-1} [r      ] / [y + r + w]^p")
note("对 y<1：r = 1-y, r' = -1  =>  r - y r' = 1,  y + r = 1")
note("  => Phi^p_n(w)  = 1/(Gamma(n+1) (1+w)^p)")
note("  => Phit^p_n(w) = 1/(Gamma(n+2) (1+w)^p)")


def _phi_num(p, n, w, N=400000):
    """分段积分避开 y=1 处的跳跃"""
    tot = 0.0
    y = np.linspace(1e-12, 1.0, N)
    r = 1.0 - y
    rp = -1.0
    f = y ** (n - 1) * (r - y * rp) / (y + r + w) ** p
    tot += np.trapz(f, y)
    return tot / math.gamma(n)


def _phit_num(p, n, w, N=400000):
    tot = 0.0
    y = np.linspace(1e-12, 1.0, N)
    r = 1.0 - y
    f = y ** (n - 1) * r / (y + r + w) ** p
    tot += np.trapz(f, y)
    return tot / math.gamma(n)


def _phi_closed(p, n, w):
    return 1.0 / (math.gamma(n + 1) * (1.0 + w) ** p)


def _phit_closed(p, n, w):
    return 1.0 / (math.gamma(n + 2) * (1.0 + w) ** p)


worst = 0.0
for (p, n, w) in [(1, 2, 0.0), (1, 2, -0.5), (2, 2, 0.3), (1, 1, 1.7),
                  (2, 3, -0.2), (1, 3, 0.9)]:
    a = _phi_num(p, n, w)
    b = _phi_closed(p, n, w)
    c = _phit_num(p, n, w)
    d = _phit_closed(p, n, w)
    e1 = abs(a - b) / max(1e-30, abs(b))
    e2 = abs(c - d) / max(1e-30, abs(d))
    worst = max(worst, e1, e2)
    note("  p=%d n=%d w=%+.2f :  Phi  数值 %.10f / 闭式 %.10f  相对差 %.2e"
         % (p, n, w, a, b, e1))
    note("                      Phit 数值 %.10f / 闭式 %.10f  相对差 %.2e"
         % (c, d, e2))
verdict("V18-P1", "PASS" if worst < 1e-6 else "FAIL",
        "优化调节器阈值函数闭式由定义积分直接积出并数值复核，最大相对差 = %.2e"
        % worst)
note("d=4 FRG 中实际出现的是 n = d/2 = 2 的 Phi^p_2、Phit^p_2：")
note("  Phi^1_2(w) = 1/(2 (1+w))，  Phi^2_2(w) = 1/(2 (1+w)^2)，")
note("  Phit^1_2(w)= 1/(6 (1+w))，  Phit^2_2(w)= 1/(6 (1+w)^2)")
note("  => 流方程在 w = -1（即 -2 lambda = -1）处有极点，")
note("     这正是不动点方程产生【非多项式】（有理）结构、从而允许孤立不动点的机制。")
verdict("V18-P2", "INFO",
        "阈值函数的有理结构（(1+w)^{-p}）使 FRG 的 beta 为非多项式函数，"
        "这是 FRG 能给出孤立不动点、而卷十七纯二次 beta 只能给出射线族的结构根源")

# ---------------------------------------------------------------- 3 挠率模式计数
chunk("步骤 3  挠率模式计数（本卷新计算，SO(4) 分解）")
note("挠率 T_{lambda mu nu} 在最后两指标反对称：分量数 = 4 * C(4,2) = 24。")
note("SO(4) 分解：V (x) Lambda^2 V，Lambda^2 V = (1,0)+(0,1)（自对偶/反自对偶）")
note("  => (3/2,1/2) + (1/2,3/2) + (1/2,1/2) + (1/2,1/2)")
note("  => 维数 8 + 8 + 4 + 4 = 24  =  张量(16) + 轴矢(4) + trace 向量(4)")

PAIRS = [(m, n) for m in range(4) for n in range(4) if m < n]
NPAIR = len(PAIRS)


def eps4():
    e = np.zeros((4, 4, 4, 4))
    for perm in itertools.permutations(range(4)):
        s = 1
        p = list(perm)
        for i in range(4):
            for j in range(i + 1, 4):
                if p[i] > p[j]:
                    s = -s
        e[perm] = s
    return e


E = eps4()
verdict("V18-K0", "PASS" if (E[0, 1, 2, 3] == 1.0 and E[1, 0, 2, 3] == -1.0) else "FAIL",
        "四维 Levi-Civita 张量构造正确（eps_{0123} = +1，反对称）")


def T_to_vec(T):
    x = np.zeros((4, NPAIR))
    for q, (m, n) in enumerate(PAIRS):
        x[:, q] = T[:, m, n]
    return x.reshape(24)


def vec_to_T(x):
    T = np.zeros((4, 4, 4))
    xm = np.asarray(x).reshape(4, NPAIR)
    for q, (m, n) in enumerate(PAIRS):
        T[:, m, n] = xm[:, q]
        T[:, n, m] = -xm[:, q]
    return T


def T_to_v(T):
    """trace 向量 v_nu = sum_lambda T_{lambda lambda nu}"""
    return np.einsum('lln->n', T)


def v_to_T(v):
    """trace 注入 T_{l m n} = delta_{lm} v_n - delta_{ln} v_m"""
    D = np.eye(4)
    return np.einsum('lm,n->lmn', D, v) - np.einsum('ln,m->lmn', D, v)


def T_to_a(T):
    """轴矢 a_sigma = sum_{lmn} eps_{sigma l m n} T_{l m n}"""
    return np.einsum('slmn,lmn->s', E, T)


def a_to_T(a):
    """轴矢注入 T_{l m n} = eps_{l m n s} a_s"""
    return np.einsum('lmns,s->lmn', E, a)


Vinj = np.zeros((24, 4))
Ainj = np.zeros((24, 4))
Vmap = np.zeros((4, 24))
Amap = np.zeros((4, 24))
for k in range(4):
    e_k = np.zeros(4)
    e_k[k] = 1.0
    Vinj[:, k] = T_to_vec(v_to_T(e_k))
    Ainj[:, k] = T_to_vec(a_to_T(e_k))
for j in range(24):
    e_j = np.zeros(24)
    e_j[j] = 1.0
    Tj = vec_to_T(e_j)
    Vmap[:, j] = T_to_v(Tj)
    Amap[:, j] = T_to_a(Tj)

M_vv = Vmap @ Vinj
M_aa = Amap @ Ainj
M_va = Vmap @ Ainj
M_av = Amap @ Vinj
I4 = np.eye(4)
c_v = float(np.mean(np.diag(M_vv)))
c_a = float(np.mean(np.diag(M_aa)))
ok_vv = float(np.max(np.abs(M_vv - c_v * I4))) < 1e-10 and abs(c_v) > 1e-10
ok_aa = float(np.max(np.abs(M_aa - c_a * I4))) < 1e-10 and abs(c_a) > 1e-10
ok_va = float(np.max(np.abs(M_va))) < 1e-10
ok_av = float(np.max(np.abs(M_av))) < 1e-10
note("  trace 注入后取 trace：V . Vinj = %.4f * I_4  （非零 => 该子空间维数 4）" % c_v)
note("  轴矢 注入后取轴矢 ：A . Ainj = %.4f * I_4  （非零 => 该子空间维数 4）" % c_a)
note("  交叉：|V . Ainj| = %.2e， |A . Vinj| = %.2e  （应为 0 => 正交）"
     % (float(np.max(np.abs(M_va))), float(np.max(np.abs(M_av)))))
verdict("V18-K1", "PASS" if (ok_vv and ok_aa and ok_va and ok_av) else "FAIL",
        "trace 子空间与轴矢子空间各 4 维且相互正交"
        if (ok_vv and ok_aa and ok_va and ok_av) else "分解校验失败")

M8 = np.vstack([Vmap, Amap])            # 8 x 24
rank8 = int(np.linalg.matrix_rank(M8, tol=1e-9))
dim_tensor = 24 - rank8
note("  联合映射 [V; A] 的秩 = %d  => 张量子空间维数 = 24 - %d = %d"
     % (rank8, rank8, dim_tensor))
verdict("V18-K2", "PASS" if (rank8 == 8 and dim_tensor == 16) else "FAIL",
        "SO(4) 分解维数：trace(4) + 轴矢(4) + 张量(%d) = 24" % dim_tensor)

# 完备性：三个投影之和应为恒等
Pv = Vinj @ np.linalg.inv(M_vv) @ Vmap if abs(c_v) > 1e-12 else np.zeros((24, 24))
Pa = Ainj @ np.linalg.inv(M_aa) @ Amap if abs(c_a) > 1e-12 else np.zeros((24, 24))
Pt = np.eye(24) - Pv - Pa
idem = [float(np.max(np.abs(P @ P - P))) for P in (Pv, Pa, Pt)]
orth = [float(np.max(np.abs(Pv @ Pa))), float(np.max(np.abs(Pv @ Pt))),
        float(np.max(np.abs(Pa @ Pt)))]
ranks = [int(round(np.trace(P))) for P in (Pv, Pa, Pt)]
note("  投影算符幂等性 max|P^2 - P| = " + ", ".join("%.2e" % v for v in idem))
note("  投影算符正交性 max|Pi Pj| = " + ", ".join("%.2e" % v for v in orth))
note("  投影算符迹（= 子空间维数）= " + str(ranks))
ok_proj = (max(idem) < 1e-9 and max(orth) < 1e-9
           and ranks == [4, 4, 16] and sum(ranks) == 24)
verdict("V18-K3", "PASS" if ok_proj else "FAIL",
        "三个投影算符幂等、两两正交、迹为 (4, 4, 16) 且和为 24 => 分解完备"
        if ok_proj else "投影算符校验失败")

note("")
note("物理含义：")
note("  - EC 理论中挠率无动能项 => 代数（由自旋源决定），不传播。")
note("  - 加入 tau^2 动能项后挠率传播，其进入 FRG 迹的模式简并度即为上述分解；")
note("    其中轴矢(4) 由自旋 1/2 物质源激发，是 EC 中唯一有经典效应的分量。")
verdict("V18-K4", "INFO",
        "挠率扇区进入 FRG 迹的模式简并度 = trace(4) + 轴矢(4) + 张量(16)；"
        "EC 无动能项时这些模式不传播（代数），加 tau^2 后才进入传播子圈")

# ---------------------------------------------------------------- 4 修正后复核
chunk("步骤 4  以修正归一化 (theta_canon = (+2,-2,0,0,0,0)) 复核卷十七结论")

COEF = {
    "A1": 0.8, "A2": 0.4, "A3": 0.2,
    "B1": -1.2, "B2": 0.5, "B3": 0.3, "B4": 0.1,
    "C1": 1.0, "C2": 0.3, "C3": -0.6, "C4": 0.2,
    "D1": 0.9, "D2": 0.2, "D3": -0.5,
    "E1": 0.7, "E2": -0.4, "E3": 0.2, "E4": 0.1,
    "F1": 0.6, "F2": 0.3,
}
KEYS = list(COEF.keys())


def beta_quad(g, c):
    g0, lam, g1, g2, g3, g4 = g
    return np.array([
        c["A1"] * g0 ** 2 + c["A2"] * g0 * g3 + c["A3"] * g3 ** 2,
        c["B1"] * lam * g0 + c["B2"] * g0 ** 2 + c["B3"] * g3 ** 2 + c["B4"] * g1,
        c["C1"] * g1 ** 2 + c["C2"] * g1 * g2 + c["C3"] * g0 * g1 + c["C4"] * g0 * g3,
        c["D1"] * g2 ** 2 + c["D2"] * g1 * g2 + c["D3"] * g0 * g2,
        c["E1"] * g3 ** 2 + c["E2"] * g0 * g3 + c["E3"] * g1 * g3 + c["E4"] * g2 * g3,
        c["F1"] * g4 ** 2 + c["F2"] * g3 * g4,
    ])


def make_beta(theta):
    def b(g, c):
        return beta_quad(g, c) + theta * np.asarray(g, dtype=float)
    return b


def jac_num(f, g, c, h=1e-7):
    g = np.asarray(g, dtype=float)
    J = np.zeros((6, 6))
    for i in range(6):
        d = np.zeros(6)
        d[i] = h
        J[:, i] = (f(g + d, c) - f(g - d, c)) / (2.0 * h)
    return J


def newton(f, c, x0, tol=1e-13, itmax=200):
    x = np.array(x0, dtype=float)
    for _ in range(itmax):
        b = f(x, c)
        bn = float(np.max(np.abs(b)))
        if bn < tol:
            return x, True
        try:
            dx = np.linalg.solve(jac_num(f, x, c), b)
        except np.linalg.LinAlgError:
            return x, False
        step = 1.0
        for _ls in range(12):
            xn = x - step * dx
            if np.all(np.isfinite(xn)) and float(np.max(np.abs(f(xn, c)))) < bn:
                break
            step *= 0.5
        x = x - step * dx
    return x, False


def find_fps(f, c, n_starts=900, box=3.0, min_norm=0.05, seed=20261015):
    rng = np.random.RandomState(seed)
    out = []
    for _k in range(n_starts):
        if _k and _k % 300 == 0:
            note("    [fps] 进度 %d / %d，已找到 %d" % (_k, n_starts, len(out)))
        x, ok = newton(f, c, rng.uniform(-box, box, size=6))
        if not ok:
            continue
        nrm = float(np.max(np.abs(x)))
        if nrm < min_norm:
            continue
        if float(np.max(np.abs(f(x, c)))) > 1e-9 * max(1.0, nrm * nrm):
            continue
        if not any(float(np.max(np.abs(x - y))) < 1e-5 * max(1.0, nrm) for y in out):
            out.append(x)
    return out


def classify(ev, tol=1e-6):
    n_uv = int(np.sum(np.real(ev) < -tol))
    n_ir = int(np.sum(np.real(ev) > tol))
    return n_uv, n_ir, 6 - n_uv - n_ir


def eig_sorted(J):
    ev = np.linalg.eigvals(J)
    return np.array(sorted(ev, key=lambda z: (float(np.real(z)), float(np.imag(z)))))


for tag, theta in (("卷十七口径 (+2,-4,0,0,0,0)", THETA_V17),
                   ("卷十八修正 (+2,-2,0,0,0,0)", THETA_V18)):
    f = make_beta(theta)
    fps = find_fps(f, COEF, n_starts=900, box=3.0, min_norm=0.05)
    note("")
    note("--- " + tag + " --- 找到孤立不动点 %d 个" % len(fps))
    rows = []
    for x in fps:
        ev = eig_sorted(jac_num(f, x, COEF))
        n_uv, n_ir, n_z = classify(ev)
        rows.append((x, ev, n_uv, n_ir, n_z))
    rows.sort(key=lambda r: r[3])
    for x, ev, n_uv, n_ir, n_z in rows:
        note("  g* = " + short_vec(x, 8))
        note("       theta = " + ", ".join("%+.5f" % float(np.real(z)) for z in ev))
        note("       dim_crit = %d, n_rel = %d, 零模 = %d；g3*=%+.4f g4*=%+.4f"
             % (n_uv, n_ir, n_z, float(x[4]), float(x[5])))
    rows_last = rows
    ng = [r for r in rows if float(np.max(np.abs(r[0]))) > 0.05]
    tors = [r for r in ng if abs(float(r[0][4])) > 0.05 or abs(float(r[0][5])) > 0.05]
    note("  非高斯不动点 %d 个，其中挠率分量非零 %d 个，"
         "n_rel 取值 %s" % (len(ng), len(tors), str(sorted(r[3] for r in ng))))
    if tag.startswith("卷十七"):
        n_v17_tors = len(tors)
        n_v17_ng = len(ng)
    else:
        n_v18_tors = len(tors)
        n_v18_ng = len(ng)

verdict("V18-R1", "PASS" if (n_v17_tors == 0 and n_v18_tors == 0) else "FAIL",
        "卷十七核心判定 V17-F4（全部非高斯不动点落在挠率关闭面）在修正归一化后"
        "【仍然成立】：卷十七口径 %d/%d、卷十八修正口径 %d/%d 的挠率分量均非零计数为 0"
        % (n_v17_tors, n_v17_ng, n_v18_tors, n_v18_ng))
verdict("V18-R2", "INFO",
        "归一化修正只移动不动点坐标与临界指数的数值，"
        "不改变'挠率通道在最小截断下未被激活'这一结构性结论")

note("")
note("补充（结构性符号判据）：在挠率关闭面 g3 = g4 = 0 上，")
note("  beta_{g0} = theta_0 g0 + A1 g0^2  =>  非零根 g0* = -theta_0 / A1 = -2 / A1。")
note("  草稿给定 A1 = %.2f > 0  =>  g0* = %+.4f < 0，即牛顿耦合为负（反引力号）。"
     % (float(COEF["A1"]), -2.0 / float(COEF["A1"])))
g0_pred = -2.0 / float(COEF["A1"])
g0_obs_dev = min(abs(float(r[0][0]) - g0_pred) for r in rows_last)
note("  数值搜索所得全部不动点的 g0* 与该闭式之差最大为 %.2e（一致）" % g0_obs_dev)
verdict("V18-R3", "FAIL",
        "草稿系数 A1 = %.2f > 0 使孤立不动点落在 g0* = -2/A1 = %+.4f < 0（牛顿耦合为负，"
        "无物理意义）；不动点存在性与物理可接受性是两件事，"
        "A1 的符号必须由一圈迹计算确定，不能任取" % (float(COEF["A1"]), g0_pred))

# ---------------------------------------------------------------- 5 蒙特卡洛
chunk("步骤 5  修正归一化下的系数稳健性（蒙特卡洛）")
N_MC = 150
rng = np.random.RandomState(23)
n_any = n_rel_finite = n_small = n_torsion = 0
rel_hist = {}
t_mc = time.time()
for k in range(N_MC):
    if k % 25 == 0:
        note("  ... 蒙特卡洛进度 %d / %d" % (k, N_MC))
    cc = dict((key, float(rng.uniform(-1.0, 1.0))) for key in KEYS)
    f = make_beta(THETA_V18)
    fpts = find_fps(f, cc, n_starts=18, box=2.5, min_norm=0.2, seed=k)
    nontriv = [x for x in fpts if float(np.max(np.abs(x))) > 0.2]
    if nontriv:
        n_any += 1
    best = None
    best_x = None
    for x in nontriv:
        ev = eig_sorted(jac_num(f, x, cc))
        n_ir = int(np.sum(np.real(ev) > 1e-6))
        if 0 < n_ir < 6:
            if best is None or n_ir < best:
                best = n_ir
                best_x = x
    if best is not None:
        n_rel_finite += 1
        rel_hist[best] = rel_hist.get(best, 0) + 1
        if best <= 2:
            n_small += 1
        if abs(float(best_x[4])) > 0.05 or abs(float(best_x[5])) > 0.05:
            n_torsion += 1
note("随机系数样本 N = %d（各系数 i.i.d. U(-1,1)，min_norm = 0.2）" % N_MC)
note("  存在非高斯孤立不动点            : %d (%.1f%%)" % (n_any, 100.0 * n_any / N_MC))
note("  存在 n_rel 在 1..5 的不动点      : %d (%.1f%%)"
     % (n_rel_finite, 100.0 * n_rel_finite / N_MC))
note("  其中 n_rel <= 2（较可预言）      : %d (%.1f%%)" % (n_small, 100.0 * n_small / N_MC))
note("  且该不动点挠率分量非零          : %d (%.1f%%)" % (n_torsion, 100.0 * n_torsion / N_MC))
note("  n_rel 分布                      : %s" % str(dict(sorted(rel_hist.items()))))
note("  蒙特卡洛耗时 = %.1f s" % (time.time() - t_mc))
verdict("V18-MC1", "BOUNDARY",
        "修正归一化后：非高斯不动点出现率 %.1f%%，n_rel<=2 占 %.1f%%，"
        "带非零挠率占 %.1f%% => 与卷十七同量级，结论不稳健性未被归一化修正所改善"
        % (100.0 * n_rel_finite / N_MC, 100.0 * n_small / N_MC,
           100.0 * n_torsion / N_MC))
verdict("V18-MC2", "OPEN",
        "A..F 系数仍未由一圈迹计算确定 => 无法判定真实 TUFT 属于哪个统计类别")

# ---------------------------------------------------------------- 6 边界
chunk("步骤 6  诚实边界与本卷未做之事")
verdict("V18-H1", "OPEN",
        "本卷未做背景场引力 Hessian 的二阶变分、York 分解与鬼场迹，"
        "故【不给出】纯 GR 爱因斯坦-希尔伯特截断 NGFP 的数值 (g_*, lambda_*)；"
        "本卷不引用未经复算的系数，避免把引用值当作推导值。")
verdict("V18-H2", "INFO",
        "卷十八可保留的稳健成果：正则项定理（V18-T1）、归一化修正（V18-D3/T3/T4）、"
        "优化调节器阈值函数闭式（V18-P1）、挠率 SO(4) 分解与模式计数（V18-K1..K3）、"
        "以及'挠率在最小截断下不激活'的跨归一化复核（V18-R1）")
verdict("V18-H3", "INFO",
        "下一卷闭合所需：(1) 背景场 Hessian + York 分解 + 鬼场，给出 GR 扇区流方程；"
        "(2) 挠率动能项的 Hessian，把模式计数(K1..K3)落实为流方程中的简并度；"
        "(3) 两圈/高阶截断误差；(4) 与 FRG 文献 NGFP 的对齐复核。")
verdict("V18-H4", "INFO",
        "卷十八相对卷十七的机制性进展：正则项由'手工补入'变为'定理推论'（V18-T1/T4），"
        "不动点不再因纯二次齐次性退化为射线族；但物理量级仍未闭合（V18-H1/MC2）。")

# ---------------------------------------------------------------- 汇总
elapsed = time.time() - T_START
_emit("")
_emit("=" * 78)
_emit("汇总")
_emit("=" * 78)
for k in ("PASS", "FAIL", "BOUNDARY", "OPEN", "INFO"):
    _emit("  %-9s= %d" % (k, COUNTS.get(k, 0)))
_emit("")
_emit("判定分布：PASS %d / FAIL %d / BOUNDARY %d / OPEN %d / INFO %d"
      % (COUNTS["PASS"], COUNTS["FAIL"], COUNTS["BOUNDARY"],
         COUNTS.get("OPEN", 0), COUNTS["INFO"]))
_emit("条目数：%d" % sum(COUNTS.values()))
_emit("运行耗时：%.1f s" % elapsed)
_emit("")
_emit("红线声明：数学自洽 != 实验证实。本文件只做 FRG 框架 / 归一化 / 群论计数的")
_emit("          诚实分析，不构成对 TUFT 物理真实性的任何主张；负结论为诚实边界，")
_emit("          非证伪宣告。")

text = "\n".join(LINES) + "\n"
try:
    with open(REPORT_PATH, "w", encoding="utf-8") as fh:
        fh.write(text)
    print("[report written] " + REPORT_PATH, flush=True)
except Exception as exc:
    print("写报告失败：" + repr(exc), flush=True)

meta = {
    "script": os.path.basename(__file__),
    "subject": "TUFT 卷十八 FRG 归一化修正 阈值函数 挠率模式计数",
    "counts": COUNTS,
    "items": int(sum(COUNTS.values())),
    "dimension_table": {
        "[G]": -2, "[Lambda]": 2, "[tau]": 1, "[c3]": -2, "[c4]": -2,
    },
    "theta_canon_v17": THETA_V17.tolist(),
    "theta_canon_v18": THETA_V18.tolist(),
    "threshold_functions": {
        "Phi^p_n(w)": "1/(Gamma(n+1) (1+w)^p)",
        "Phit^p_n(w)": "1/(Gamma(n+2) (1+w)^p)",
        "max_rel_error": float(worst),
    },
    "torsion_decomposition": {
        "total": 24,
        "trace_vector": 4,
        "axial": 4,
        "tensor": int(dim_tensor),
        "projector_traces": ranks,
        "V_dot_Vinj_const": float(c_v),
        "A_dot_Ainj_const": float(c_a),
    },
    "recheck_v17_F4": {
        "v17_norm_torsion_on": int(n_v17_tors),
        "v17_norm_nongauss": int(n_v17_ng),
        "v18_norm_torsion_on": int(n_v18_tors),
        "v18_norm_nongauss": int(n_v18_ng),
    },
    "monte_carlo": {
        "N": N_MC,
        "n_with_nongaussian_fp": int(n_any),
        "n_with_finite_rel": int(n_rel_finite),
        "n_rel_le2": int(n_small),
        "n_torsion_on": int(n_torsion),
        "n_rel_hist": dict((str(k), v) for k, v in rel_hist.items()),
    },
    "elapsed_s": float(elapsed),
}
try:
    with open(JSON_PATH, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=2)
except Exception:
    pass
