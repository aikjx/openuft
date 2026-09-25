# -*- coding: utf-8 -*-
"""UFE-1 · D5=$\\mathfrak{so}(10)$ 表示论引擎（L10 / L15 阶段二；零第三方依赖）。

问题：`so10_chain.py` 已把"给定内容下统不统一"变成可判定计算，但它留下的**最大不确定度
是标量谱**——情形 A/B/C 里的 $\\Phi(1,2,2)$、$\\Sigma(1,1,3)_0$ 是**手工放置**的，
而其中被当作 $\\Delta_R$ 的三重态后来被查明 $B-L=0$、取自 $45_H$，根本不能破 $B-L$
（链探针门禁 S2.7）。$M_{\\rm GUT}$ 因此在各情形之间摆动——倍数**不在这里写死**：
它由 `chain_band()`/`swing_note()` 当场向链探针要，并由门禁 R2.sw0–R2.sw2 钉住
（2026-09-24 台账 F4 修复后此数从 $3.8\\,(A/B)$ 倍变成 $8.7\\,(A/C)$ 倍，而本文件当时没跟着动）。

本探针把标量谱从"猜"变成"推"：**唯一李论输入是 D5 的 Dynkin 图**，其余全部现场推导：

    Dynkin 图 → Cartan 矩阵 → 正根 → $\\rho$ → 基本权重 → Weyl 维数公式
                                      → Freudenthal–Racah 权重重数
                                      → Adams 运算 $\\mathrm{Sym}^2/\\wedge^2$ 交叉验证

再回答一个此前只能引用的问题：**哪些 Higgs 表示可能承载 $\\Delta_R$（$|B-L|=2$）**，
使 $B-L$ 与 $SU(2)_R$ 同时破缺、进而给 $\\nu_R$ Majorana 质量。

判据是**严格**的：$\\alpha$-串不断且重数对称是定理 ⇒
"对子群每个正根 $\\beta$，$\\lambda\\pm\\beta$ 均非权重" $\\iff$ 该权重上的全部态是该子群单态。

最紧的一条判定来自 Cartan 恒等式 $Q=T^3_L+T^3_R+\\tfrac{B-L}{2}$：任何 $(1,1,1)_{\\pm2}$
单态都带 $|Q|=1$，一取期望值就破电磁 ⇒ "破 $B-L$ 而保 $U(1)_{em}$" **必然**经由 $\\Delta_L$
或 $\\Delta_R$ 的中性分量（R5.8），而 $\\dim\\le210$ 内的唯一承载者是 $126/\\overline{126}$。

第二问（R7）与第一问相互独立：把 $16_F$ 的双线性乘积 $\\mathrm{Sym}^2/\\wedge^2/16\\otimes\\overline{16}$
拆成不可约成分、取共轭 $\\Rightarrow$ 得到 **d=4 可重整 Yukawa 允许哪些 Higgs**。
拆成分走的是"支配权上的单位三角方程组 + 整权重构对账"，与 R3 的"剥已知成分再 `find`"
是两条不同代码路径（R7.1）。两问在 $\\overline{126}_H$ 上重合：它既是对称手征通道里
唯一携带 $-2\\nu$ 权重的表示，其 $\\Delta_R$ 中性成员又正好是那个权重（R7.4/R7.5）。

第三问（R8）换一条与 R7 不共享代码的路：直接数 $\\mathrm{mult}((1),V)$（$V$ 里**规范不变**
方向的个数），并把"荷配平"（零权方向数）与"规范不变"分开记账 $\\Rightarrow$ 恒有
$\\mathrm{mult}((1),V)\\le\\dim V_0$，而两者之差可逐成分拆开核对。第四问（R9）把 R8 的配对和按
**双费米子道**拆开：$\\mathrm{mult}((1),A\\otimes A)=\\sum_R n_Rn_{\\bar R}$ 逐道归口 $\\Rightarrow$
读出的不是"有几个"而是"哪一个走哪条道"，其中"在场却不闭合"的那条道恰是 $126_S$。R9 也是本文件
里第一次把配对和改走**标号**路径（登记表只到 $\\dim\\le210$，按名字查共轭会在登记范围外把真实
存在的共轭伙伴静默算成 0 $\\Rightarrow$ 差额由 R9.5 第四条当场量出来）。

第五问（R10）把"$B-L$ 破缺之后**残留哪个离散规范对称性**"从散文变成荷格上的读数：只用本文件
自己声明的内容（$16_F$ 的各权重 + 在场标量的"色单态且 $Q=0$"分量）现算 $B-L$ 荷格生成元
$g_0$、圆周 $\\alpha_0=2\\pi/g_0$ 与残留阶 $N=q_\\Delta/g_0$，三条路径同数才认（甲：精确有理
gcd／lcm；乙：把圆周均分后逐角浮点枚举；丙：整套荷同乘 $1/2$ 的换约定测试 + 一个**故意错配**
的植入缺陷）。读数**推翻**了此前写在报告 §0/§4/§5 与 09 文档里的一句话：
$|\\Delta(B-L)|=1$ 那条单步通道留下的是 $\\mathbb{Z}_3$（阶为奇 $\\Rightarrow$ 群里没有 2 阶元，
物质字称是**被它破掉的**），$\\mathbb{Z}_6=\\mathbb{Z}_2\\times\\mathbb{Z}_3$ 属于
$|\\Delta(B-L)|=2$ 那一步 $\\Rightarrow$ "物质字称对质子稳定反而有利"这句话的前提当时并不成立。

第六问（R11）接着把"残留群**禁哪些低能算符**"从待办变成 $Y$ 切片上的读数：低能场清单由权重格
展开（名字由 $(\\lambda,Y,B-L)$ 签名绑定），判决只用一条同余式——$\\mathbb{Z}_N$
（$N=q_\\Delta/g_0$）不变 $\\iff$ $N\\mid3Q$，$Q=\\sum_k(B-L)_k$，三条互不共享算术的实现
（整除／群元逐元／浮点角度）同判决才认。两处结论是**否定**的：物质双线性里唯一的低能不变量是
$\\nu^c\\nu^c$（右手中微子 Majorana 质量与残留群一致，但它在"3221 零权"那个错投影下读成 0
$\\Rightarrow$ R8.5/R7.4"要 $|B-L|=2$ 必插 $126_H$"在低能一侧重现）；而 d=6 的含单态类里
$\\Delta B\\ne0$ 且 $\\Delta L\\ne0$ 的那几条**全部**满足 $\\Delta(B-L)=0$、判决**全部允许**
$\\Rightarrow$ 残留离散规范对称性**不**给质子稳定性论证——机理也是读数：$\\mathbb{Z}_3$ 那半边
在低能就是色 triality（R11.2 把 R10.4 的同余搬到场、再搬到算符各数一次），它在单态层没有额外
信息；$\\mathbb{Z}_2$ 那半边是物质字称，对偶数条物质场自动通过。

数值实现：权重全部以 $1/12$ 为单位存成**整数 5 元组**（$D_5$ 权重格的坐标只取
整数或半整数，$B-L=\\tfrac23(\\varepsilon_1+\\varepsilon_2+\\varepsilon_3)$ 取 $8$），
于是格点运算全程整数、无浮点；内积 $\\langle a,b\\rangle:=144(a,b)$ 也是整数。

诚实边界（详见报告 §16）：
- 表示论是**数学**，不是"自然界选了 SO(10)"的证据；本探针不提升任何证据等级，也不关闭 L10。
- "$Q=0$ 才允许取期望值"与"$B-L$ 必须被破掉"是**物理输入**而非李论推论；两条任一改掉，
  "$126_H$ 必需"随之失效。$16_H/\\overline{16}_H$ 的 $|\\Delta(B-L)|=1$ 单步通道始终合法
  （R5.9），只是给不出可重整的 $\\nu_R$ 质量。
- 物质取偶负号自旋量（`so10_chain.py` 的约定）。换共轭约定会同时对调
  $16\\leftrightarrow\\bar{16}$、$126\\leftrightarrow\\overline{126}$、$\\Delta_L\\leftrightarrow\\Delta_R$；
  故**结论一律用 $|B-L|$ 表述**（$\\max|B-L|$ 与"能否承载 $|B-L|=2$"对符号免疫）。
- 串检验给的是 **Cartan 层面**的多重态类型判定，不替代完整分支规则系数
  （哪个拷贝与三代费米子耦合、$SU(4)_c$ 的 $4/\\bar4$ 归属），那部分仍是后续工作。
- R7 只判 **d=4**（可重整）通道、且只判到"哪些表示允许出现"：**没有味自由度**，
  故"$120_H$ 的 Yukawa 矩阵在味指标上反对称"这类标准论证不进门禁；高维算符也不在范围内。
- R9 数的是**不变张量经由哪条道**，不是算符个数（Lorentz／味／Fierz 三关未做），且这些数**不**
  回填进 $\\tau_p$；"哪条道由哪个 Higgs 因子化"一旦落到具体模型，就是**情形声明的输入**而非
  权重算出来的结论（R9.3 的包含判据在同侧是退化的）。
- R10 只数 $U(1)_{B-L}$ **这一个因子**内的残留子群：$SU(3)_c$、$SU(2)_{L/R}$ 的中心与规范群的
  整体形式都不在那张荷格里 $\\Rightarrow$ 完整残留群可能是它的**扩张**。且两条读数都是**条件的**
  （承载者不在链探针字面声明的标量谱里，R10.10／R11.10）。"残留群能禁哪些低能算符"已由 R11
  判到 d=6，但结论是**否定**的（那一层的质子衰变算符不受禁）$\\Rightarrow$ 本层不回填质子寿命或
  暗物质论证，也不改变 L10 的开放状态。

用法： python -B so10_reps.py
产出： SO10表示论报告.md / SO10表示论报告.json
"""
from fractions import Fraction as F
import collections
import itertools
import json
import math
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

RESULTS = []
HYGIENE = {}


def rec(cid, claim, computed, expected, tol, status, unit='', note=''):
    RESULTS.append({'id': cid, 'claim': claim, 'computed': computed,
                    'expected': expected, 'tolerance': tol, 'unit': unit,
                    'status': status, 'note': note})
    return status == 'PASS'


def exact(cid, claim, computed, expected, note='', unit=''):
    """精确比对（整数或有理数）：不容忍浮点。"""
    return rec(cid, claim, str(computed), str(expected), '0（精确）',
               'PASS' if computed == expected else 'FAIL', unit, note)


def ok(cid, claim, cond, note=''):
    return rec(cid, claim, bool(cond), True, '布尔', 'PASS' if cond else 'FAIL', '', note)


# =============================================================== 格点算术（整数，单位 1/12）
U = 12                              # 1 个 $\\varepsilon_i$ = 12 个单位
D4 = U * U                          # $\\langle a,b\\rangle = 144\\,(a,b)$ 为整数


def unit(i):
    v = [0] * 5
    v[i] = U
    return tuple(v)


EPS = [unit(i) for i in range(5)]
ZERO = (0,) * 5


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def neg(a):
    return tuple(-x for x in a)


def smul(k, a):
    return tuple(k * x for x in a)


def half(a):
    assert all(x % 2 == 0 for x in a), '奇数分量不能减半：%s' % (a,)
    return tuple(x // 2 for x in a)


def ip(a, b):
    """$144\\,(a,b)$：整数内积。"""
    return sum(x * y for x, y in zip(a, b))


def nrm(a, b):
    """真实内积 $(a,b)$ 的精确有理数形式（只用于输出与荷）。"""
    return F(ip(a, b), D4)


def nrm2(a):
    return nrm(a, a)


def ipp(a, b, msg=''):
    """要求整数内积可被 144 整除（即真实内积为整数）后返回该整数。"""
    v = ip(a, b)
    assert v % D4 == 0, '内积非整数%s：%s·%s = %s/144' % (msg, a, b, v)
    return v // D4


def fmt(w):
    return '(' + ','.join(str(F(x, U)) for x in w) + ')'


# =============================================================== 唯一的李论输入
# D5 的 Dynkin 图：链 1–2–3，节点 3 分叉到 4 与 5（下列指标 0 起始）
DIAGRAM = [(0, 1), (1, 2), (2, 3), (2, 4)]
RANK = 5


def cartan_from_diagram():
    A = [[F(2) if i == j else F(0) for j in range(RANK)] for i in range(RANK)]
    for i, j in DIAGRAM:
        A[i][j] = A[j][i] = F(-1)
    return A


CARTAN_IN = cartan_from_diagram()

# 标准 $\\varepsilon$ 基实现（$D_n$：全部根长 $\\sqrt2$）
SIMPLE = [sub(EPS[0], EPS[1]), sub(EPS[1], EPS[2]), sub(EPS[2], EPS[3]),
          sub(EPS[3], EPS[4]), add(EPS[3], EPS[4])]


def cartan_from_realization():
    return [[2 * nrm(SIMPLE[i], SIMPLE[j]) / nrm2(SIMPLE[j]) for j in range(RANK)]
            for i in range(RANK)]


def positive_roots():
    """正根 = 单根的非负整系数组合中长度平方为 2 者（$D_5$ 最高根系数 $\\le2$）。"""
    out = []
    for ns in itertools.product(range(3), repeat=RANK):
        if not any(ns):
            continue
        v = ZERO
        for n, a in zip(ns, SIMPLE):
            v = add(v, smul(n, a))
        if ip(v, v) == 2 * D4:
            out.append(v)
    return sorted(out)


PH = positive_roots()                       # 正根：20 个
ROOTS = PH + [neg(a) for a in PH]           # 全部根：40 个


def inverse_rows(M):
    """精确求逆（分数高斯消元）：返回 $M^{-1}$ 的行。"""
    n = len(M)
    aug = [[F(M[i][j]) for j in range(n)] + [F(1) if i == k else F(0) for k in range(n)]
           for i in range(n)]
    for c in range(n):
        piv = next((r for r in range(c, n) if aug[r][c] != 0), None)
        if piv is None:
            raise ZeroDivisionError('singular Cartan realization')
        aug[c], aug[piv] = aug[piv], aug[c]
        pv = aug[c][c]
        aug[c] = [x / pv for x in aug[c]]
        for r in range(n):
            if r != c and aug[r][c] != 0:
                f = aug[r][c]
                aug[r] = [x - f * y for x, y in zip(aug[r], aug[c])]
    return [tuple(aug[i][n + j] for j in range(n)) for i in range(n)]


def to_grid(row, what):
    out = []
    for x in row:
        n = x * U
        assert n.denominator == 1, '%s 不是 $1/12$ 的整数倍：%s' % (what, x)
        out.append(int(n))
    return tuple(out)


# 基本权重：$(\\omega_i,\\alpha_j)=\\delta_{ij}$。方程组的**行**是 $\\alpha_j$ 的真实分量
# （故先把 $1/12$ 单位换算回真实值），$\\omega_i$ = 逆矩阵的第 $i$ 列。
_MINV = inverse_rows([[F(a[k], U) for k in range(RANK)] for a in SIMPLE])
FUND = [to_grid(tuple(_MINV[r][c] for r in range(RANK)), '基本权重') for c in range(RANK)]
RHO = half(ZERO)
for a in PH:
    RHO = add(RHO, a)
RHO = half(RHO)


def dynkin(mu):
    """$\\mu$ 的 Dynkin 标号 $(\\mu,\\alpha_i^\\vee)$；本实现里 $\\alpha^\\vee=\\alpha$。"""
    return tuple(ipp(mu, a) for a in SIMPLE)


def weyl_reflect(v, a):
    return sub(v, smul(ipp(v, a), a))        # $|a|^2=2$ ⇒ 反射系数就是 $(v,a)$


def weyl_orbit(v):
    seen = {v}
    stack = [v]
    while stack:
        u = stack.pop()
        for a in SIMPLE:
            w = weyl_reflect(u, a)
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return seen


def dominant(v):
    """$v$ 的 Weyl 轨道中唯一的支配代表（及其 Dynkin 标号）。"""
    for w in weyl_orbit(v):
        lab = dynkin(w)
        if all(x >= 0 for x in lab):
            return w, lab
    raise ValueError('not a weight: %s' % (v,))


def weight_of_label(cs):
    v = ZERO
    for c, w in zip(cs, FUND):
        v = add(v, smul(c, w))
    return v


def highest_root():
    """唯一同时是**正根**且**支配**的根 = 最高根 $\\theta$；一并返回它在单根基下的系数（marks）。"""
    out = []
    for ns in itertools.product(range(3), repeat=RANK):
        if not any(ns):
            continue
        v = ZERO
        for n, a in zip(ns, SIMPLE):
            v = add(v, smul(n, a))
        if ip(v, v) == 2 * D4 and all(x >= 0 for x in dynkin(v)):
            out.append((v, ns))
    assert len(out) == 1, '最高根不唯一：%s' % ([o[0] for o in out],)
    return out[0]


TH, TH_MARKS = highest_root()


def weyl_dim(Lam):
    """$\\dim(\\Lambda)=\\prod_{\\alpha>0}(\\Lambda+\\rho,\\alpha)/(\\rho,\\alpha)$。"""
    num, den = 1, 1
    for a in PH:
        num *= ip(add(Lam, RHO), a)
        den *= ip(RHO, a)
    q = F(num, den)
    assert q.denominator == 1, 'Weyl 维数不是整数'
    return int(q)


def casimir2(Lam):
    """$C_2(\\Lambda)=(\\Lambda,\\Lambda+2\\rho)$。"""
    return nrm2(Lam) + 2 * F(ip(Lam, RHO), D4)


def freudenthal(Lam):
    """Freudenthal–Racah 递推，返回 $\\{\\mu:m_\\mu\\}$（只含重数 $>0$）。

    $m_\\mu\\,[(\\Lambda+\\rho)^2-(\\mu+\\rho)^2]=2\\sum_{\\alpha>0}\\sum_{i>0}
    m_{\\mu+i\\alpha}\\,(\\mu+i\\alpha,\\alpha)$。

    两点关键（都是本文件早先踩过的坑，写成断言把守）：
    1. **分母用 $\\rho$ 平移后的范数差**。用 $(\\Lambda,\\Lambda)-(\\mu,\\mu)$ 会在
       minuscule 表示（$10,16$）处除零并给出错误重数。
    2. **处理顺序按 $d(\\mu)=\\sum_j n_j$（$\\Lambda-\\mu=\\sum n_j\\alpha_j$ 的系数和）升序**。
       $d$ 由线性无关性**唯一决定**，等于 $(\\Lambda-\\mu,\\rho)$（因 $(\\alpha_j,\\rho)=1$）；
       用 DFS 的**路径长度**当 $d$ 会给同一点赋非最小的 $d$，破坏递推顺序 ⇒ 重数不整除。
    """
    hmax = ip(Lam, Lam)
    lamr = ipp(Lam, RHO)
    cand = {Lam}
    stack = [Lam]
    while stack:
        u = stack.pop()
        for a in SIMPLE:
            w = sub(u, a)
            if ip(w, w) <= hmax and w not in cand:
                cand.add(w)
                stack.append(w)
    depth = dict((mu, lamr - ipp(mu, RHO)) for mu in cand)
    assert min(depth.values()) == 0
    m = {}
    for mu in sorted(cand, key=lambda x: depth[x]):
        if mu == Lam:
            m[mu] = 1
            continue
        den = ip(add(Lam, RHO), add(Lam, RHO)) - ip(add(mu, RHO), add(mu, RHO))
        assert den > 0, 'Freudenthal 分母非正（权重 %s）' % (mu,)
        tot = 0
        for a in PH:
            i = 1
            while True:
                w = add(mu, smul(i, a))
                if w not in cand:
                    break
                if m.get(w, 0):
                    tot += m[w] * ip(w, a)
                i += 1
        val = F(2 * tot, den)
        assert val.denominator == 1, 'Freudenthal 重数不整除（权重 %s）' % (mu,)
        m[mu] = int(val)
    return dict((mu, k) for mu, k in m.items() if k > 0)


# ---------------------------------------------------------------- 多重集工具
def from_list(ws):
    out = {}
    for w in ws:
        out[w] = out.get(w, 0) + 1
    return out


def madd(*mss):
    out = {}
    for ms in mss:
        for w, k in ms.items():
            out[w] = out.get(w, 0) + k
    return dict((w, k) for w, k in out.items() if k)


def msub(ms, *parts):
    """$ms-\\sum_k$ parts；出现负重数即抛（分解不成立时不会静默通过）。"""
    out = dict(ms)
    for part in parts:
        for w, k in part.items():
            if out.get(w, 0) < k:
                raise ArithmeticError('剥不掉：权重 %s 重数不足' % (w,))
            out[w] -= k
    return dict((w, k) for w, k in out.items() if k)


def msum(ms):
    return sum(ms.values())


def tprod(a, b):
    """$\\chi_a\\chi_b$：权重两两相加（重数相乘）。"""
    out = {}
    for w1, k1 in a.items():
        for w2, k2 in b.items():
            w = add(w1, w2)
            out[w] = out.get(w, 0) + k1 * k2
    return out


def psi2(a):
    """Adams 操作 $\\psi_2$：$\\mu\\mapsto2\\mu$。"""
    out = {}
    for w, k in a.items():
        w2 = smul(2, w)
        out[w2] = out.get(w2, 0) + k
    return out


def _symwedge(a, sgn):
    """$(\\chi^2+\\mathrm{sgn}\\cdot\\psi_2\\chi)/2$：逐点必须整除且非负。"""
    sq, p2 = tprod(a, a), psi2(a)
    out = {}
    for w in set(sq) | set(p2):
        v = sq.get(w, 0) + sgn * p2.get(w, 0)
        if v % 2:
            raise ArithmeticError('Adams 运算给出半整数（权重 %s）' % (w,))
        if v < 0:
            raise ArithmeticError('Adams 运算给出负重数（权重 %s）' % (w,))
        if v:
            out[w] = v // 2
    return out


def sym2(a):
    return _symwedge(a, +1)


def wedge2(a):
    return _symwedge(a, -1)


# =============================================================== 表示清单（按标号搜索）
def labels_upto(total):
    out = []
    for cs in itertools.product(range(total + 1), repeat=RANK):
        if sum(cs) <= total:
            out.append(tuple(cs))
    return out


ALL_LABELS = labels_upto(3)                   # $\\sum c_i\\le3$：覆盖到 $\\dim 672$
DIMMAP = {}
for _cs in ALL_LABELS:
    DIMMAP.setdefault(weyl_dim(weight_of_label(_cs)), []).append(_cs)


def find(target_dim, want_ms=None):
    """按维数（可选：再按权重多重集）定位**唯一**的 Dynkin 标号；不唯一/无候选返回 None。"""
    cands = list(DIMMAP.get(target_dim, []))
    if want_ms is not None:
        cands = [cs for cs in cands if irrep(cs)[1] == want_ms]
    return cands[0] if len(cands) == 1 else None


CACHE = {}


def irrep(cs):
    """按 Dynkin 标号取（最高权, 权重多重集, Weyl 维数, Freudenthal 总重数, $C_2$）。"""
    key = tuple(cs)
    assert all(c >= 0 for c in key), '标号 %s 非支配 ⇒ 不是最高权，递推不适用' % (cs,)
    if key not in CACHE:
        Lam = weight_of_label(key)
        ms = freudenthal(Lam)
        CACHE[key] = (Lam, ms, weyl_dim(Lam), msum(ms), casimir2(Lam))
    return CACHE[key]


# 只有 $\\sum c_i\\le2$ 的 15 个标号做全量重数递推（含 dim 1200）；更高标号按需计算
LOW_LABELS = [cs for cs in ALL_LABELS if sum(cs) <= 2]


# =============================================================== 与 so10_chain 对表
CHAIN_OK = False
try:
    import so10_chain as chain
    CHAIN_OK = chain.run_engine_tests()
except Exception as e:                                     # pragma: no cover
    print('[warn] 无法载入 so10_chain：%r —— 荷约定相关判定将不通过' % (e,))
    chain = None

# 链探针的 Cartan 方向（Fraction 形式）⇒ 换成本引擎的整数格点单位
def to_grid_dir(vec, what):
    out = []
    for x in vec:
        n = x * U
        assert n.denominator == 1, '%s 的分母不是 $1/%d$：%s' % (what, U, x)
        out.append(int(n))
    return tuple(out)


BL = T3L = T3R = YHP = None
if chain is not None:
    BL = to_grid_dir(chain.BL, '$B-L$ 方向')
    T3L = to_grid_dir(chain.T3L, '$T^3_L$ 方向')
    T3R = to_grid_dir(chain.T3R, '$T^3_R$ 方向')
    YHP = to_grid_dir(chain.YHP, '$Y$ 方向')

# $Q=T^3_L+T^3_R+\\tfrac{B-L}{2}$：在 so(10) 的 Cartan 子空间里，电磁荷是**另一个方向**，
# 只有当 $T^3_L=0$（弱单态）时它才等于 $Y$。整条判定链的关键就在这个差别上。
QHP = add(T3L, add(T3R, half(BL))) if chain is not None else None


# =============================================================== 跨仪器对账（摆动倍数不写死）
def chain_band(scn=None):
    """现场调用链探针，解出单阈 3221 链各情形的 $M_{\\rm GUT}$（只收物理解）。

    为什么必须是**活数**：本报告 §0/§15 的散文要引用"$M_{\\rm GUT}$ 的摆动倍数"。
    2026-09-24 台账 F4（链探针情形 C 的 $b_2$ 重复计入）修复后，三情形区间从
    $3.8\\,(A/B)$ 倍变成 $8.7\\,(A/C)$ 倍，而本报告当时没跟着动 —— 写死数字就是这条复发路径。
    """
    if chain is None or not CHAIN_OK:
        return None
    keys = list(chain.SCENARIOS) if scn is None else list(scn)
    out = []
    for k in keys:
        r = chain.solve_determined('R3221', k)
        if r is not None and r['physical']:
            out.append((k, r['scales']['M_GUT']))
    return out or None


def swing_note(band=None, nested=False):
    """把区间两端之比连同**哪两个情形**在两端一起给出（供散文直接嵌入）。

    刻意不返回裸数字：一个没有主体的倍数正是 F4 那种"数还活着、意义已经变了"的写法。
    `nested` 用于已经处在括号里的句子 —— 套两层括号会让读者以为外层在修饰内层。
    """
    band = chain_band() if band is None else band
    if not band:
        return '未对账（链探针引擎未通过 ⇒ 本报告不引用其摆动倍数）'
    lo = min(band, key=lambda t: t[1])
    hi = max(band, key=lambda t: t[1])
    if nested:
        return '%.1f 倍——情形 %s↔%s，%d 条物理解**并列**区间，不是误差棒' % (
            hi[1] / lo[1], lo[0], hi[0], len(band))
    return '%.1f 倍（情形 %s↔%s；%d 条物理解**并列**给出的区间，不是误差棒）' % (
        hi[1] / lo[1], lo[0], hi[0], len(band))



def chg(w, dirn):
    """权重 $w$ 沿方向 $dirn$ 的荷（精确有理数）。"""
    return F(ip(w, dirn), D4)


def grid_ms(ws):
    """把链探针的 Fraction 权重集换成本引擎的整数格点多重集。"""
    out = {}
    for w, k in from_list(ws).items():
        out[to_grid_dir(w, '权重')] = k
    return out


# =============================================================== 子群串检验
# 物理 $SU(3)_c$ 根 $\\pm(\\varepsilon_i-\\varepsilon_j),\\ i<j\\le3$；
# $SU(2)_L$ 根 $\\varepsilon_4+\\varepsilon_5$；$SU(2)_R$ 根 $\\varepsilon_4-\\varepsilon_5$。
# $B-L$ 与这三组根全部正交 ⇒ 它是 Pati–Salam 块的中心 $U(1)$。
A2_C = [sub(EPS[i], EPS[j]) for i in range(3) for j in range(i + 1, 3)]
A1_L = add(EPS[3], EPS[4])
A1_R = sub(EPS[3], EPS[4])


def string_len(ms, lam, beta):
    """沿根 $\\beta$ 穿过 $\\lambda$ 的连续串长度（$\\alpha$-串不断 ⇒ 直接数）。"""
    n, k = 1, 1
    while add(lam, smul(k, beta)) in ms:
        n += 1
        k += 1
    k = 1
    while sub(lam, smul(k, beta)) in ms:
        n += 1
        k += 1
    return n


def color_singlet_wt(ms, lam):
    """串长 1 $\\iff$ 该权重上所有态都是 $SU(3)_c$ 单态（既是最高又是最低权）。"""
    return all(string_len(ms, lam, b) == 1 for b in A2_C)


def bl2_class(ms, target=F(2)):
    """列出 $B-L=$ target 的权重，附 (色单态?, $SU(2)_{L/R}$ 串长, $T^3_{L,R},Y,Q$)。"""
    rows = []
    for lam in sorted(w for w in ms if chg(w, BL) == target):
        rows.append({'w': lam, 'm': ms[lam], 'c1': color_singlet_wt(ms, lam),
                     'L': string_len(ms, lam, A1_L), 'R': string_len(ms, lam, A1_R),
                     'T3L': chg(lam, T3L), 'T3R': chg(lam, T3R), 'Y': chg(lam, YHP),
                     'Q': chg(lam, QHP)})
    return rows


def bl_multiplets(ms):
    """$|B-L|=2$ 的色单态按多重态类型归档：$\\Delta_R$ / $\\Delta_L$ / $(1,1,1)_{\\pm2}$ / 其他。"""
    res = {'DR': [], 'DL': [], 'S': [], 'other': []}
    for t in (F(2), F(-2)):
        for r in bl2_class(ms, t):
            if not r['c1']:
                continue
            key = ('DR' if (r['L'] == 1 and r['R'] == 3) else
                   'DL' if (r['L'] == 3 and r['R'] == 1) else
                   'S' if (r['L'] == 1 and r['R'] == 1) else 'other')
            res[key].append(dict(r, BL=t))
    return res


def bl2_summary(mp):
    """把 $|B-L|=2$ 的色单态按（类型, $B-L$）汇总：成员数、$Q$ 谱、$Q=0$ 的成员数。

    三重态（$\\Delta_{L/R}$）的 $Q$ 沿串逐级 $+1$ ⇒ 每组恰有一个中性成员；
    而 $(1,1,1)_{\\pm2}$ 单态的 $Q=\\tfrac{B-L}{2}=\\pm1$ **恒不为零** ⇒ 它一破缺就破电磁。
    """
    out = []
    for k in ('DR', 'DL', 'S', 'other'):
        for t in (F(2), F(-2)):
            grp = [r for r in mp[k] if r['BL'] == t]
            if not grp:
                continue
            out.append({'kind': k, 'BL': str(t), 'n': len(grp),
                        'Q': [str(q) for q in sorted(set(r['Q'] for r in grp))],
                        'Y': [str(y) for y in sorted(set(r['Y'] for r in grp))],
                        'T3': [str(x) for x in sorted(set(
                            r['T3R' if k == 'DR' else 'T3L'] for r in grp))],
                        'nq0': sum(1 for r in grp if r['Q'] == 0)})
    return out


def carriers(ms):
    """$(\\max|B-L|,\\ $有$\\Delta_R$?,\\ $有$\\Delta_L$?,\\ $有(1,1,1)_{\\pm2}$?,\\ 中性可破缺?,\\ 汇总)$。"""
    mp = bl_multiplets(ms)
    mx = max(abs(chg(w, BL)) for w in ms)
    summ = bl2_summary(mp)
    safe = any(r['kind'] in ('DR', 'DL') and r['nq0'] * 3 == r['n'] for r in summ)
    return mx, bool(mp['DR']), bool(mp['DL']), bool(mp['S']), safe, summ, mp


# ============================================== 分支规则：限制到极大秩子群
# 两条破缺链的半单部分都与 $SO(10)$ **共享同一个 Cartan 子代数**（满秩子群）：
#
#   3221：$SU(3)_c\times SU(2)_L\times SU(2)_R$，单根 $\varepsilon_1-\varepsilon_2$、
#         $\varepsilon_2-\varepsilon_3$、$\varepsilon_4+\varepsilon_5$、$\varepsilon_4-\varepsilon_5$
#         （秩 4）；缺的那一维正是与这四个根全部正交的 $B-L$ ⇒ 每个权重的 $B-L$ 原样保留。
#   422 ：$SU(4)_c\times SU(2)_L\times SU(2)_R$，把 $A_2$ 换成 $D_3\simeq A_3$ 的单根
#         $\varepsilon_1-\varepsilon_2$、$\varepsilon_2-\varepsilon_3$、$\varepsilon_2+\varepsilon_3$
#         （秩 $3+1+1=5$ = 满秩，Pati–Salam 的 $U(1)$ 自动在 $SU(4)$ 的 Cartan 里）。
#
# ⇒ "分支"就是**同一批权重向量换一套标号**。分支重数用 Klimyk–Springer 交错和
#   $n_\lambda=\sum_{w\in W_H}\det(w)\,m_\Lambda\big(w(\lambda+\rho_H)-\rho_H\big)$，
#   它只用到 $m_\Lambda$（Freudenthal 已给）与 $W_H,\rho_H$（由单根现算）⇒ 与 §1 的
#   递推**互相独立**；再由门禁 R6.3「$\sum_\lambda n_\lambda\dim_H(\lambda)=\dim\Lambda$」收口。
def positive_roots_of(simples):
    """正根 = 单根的非负整系数组合中长度平方为 2 者（直和型子系统同样成立）。"""
    out = []
    for ns in itertools.product(range(4), repeat=len(simples)):
        if not any(ns):
            continue
        v = ZERO
        for n, a in zip(ns, simples):
            v = add(v, smul(n, a))
        if ip(v, v) == 2 * D4:
            out.append(v)
    return sorted(out)


def rho_of(pos):
    s = ZERO
    for a in pos:
        s = add(s, a)
    return half(s)


def reflect_mat(beta):
    r"""$s_\beta$ 在 $\varepsilon$ 基下的**整数**矩阵；第 $k$ 行 = 第 $k$ 个基向量的像。"""
    b = []
    for x in beta:
        assert x % U == 0 and abs(x) <= U, '单根坐标异常：%s' % (beta,)
        b.append(x // U)                                    # $\in\{0,\pm1\}$
    return tuple(tuple(int(i == k) - b[k] * b[i] for i in range(5)) for k in range(5))


IDENT = tuple(tuple(int(i == j) for j in range(5)) for i in range(5))


def mat_compose(A, B):
    """先 $B$ 后 $A$（行约定：第 $k$ 行 = $e_k$ 的像）。"""
    return tuple(tuple(sum(B[k][j] * A[j][i] for j in range(5)) for i in range(5))
                 for k in range(5))


def mat_vec(M, v):
    return tuple(sum(v[k] * M[k][i] for k in range(5)) for i in range(5))


def weyl_group_signed(simples):
    """$\{$矩阵 $:\det\}$。同一矩阵被两条路径以不同符号到达 ⇒ 当场报错（自检）。"""
    gens = [reflect_mat(a) for a in simples]
    els = {IDENT: 1}
    stack = [IDENT]
    while stack:
        M = stack.pop()
        for g in gens:
            N = mat_compose(M, g)
            if N in els:
                assert els[N] == -els[M], 'Weyl 群的符号表示不自洽'
                continue
            els[N] = -els[M]
            stack.append(N)
    return els


class Subsystem(object):
    r"""极大秩子群的半单部分：正根、$\rho$、Weyl 群、维数公式全部由单根现算。"""

    def __init__(self, name, simples, extra=None):
        self.name, self.extra = name, extra
        self.simples = list(simples)
        for a in self.simples:
            assert ip(a, a) == 2 * D4, '%s：单根长度不为 2' % name
        self.pos = positive_roots_of(self.simples)
        self.rho = rho_of(self.pos)
        self.W = weyl_group_signed(self.simples)
        for a in self.simples:
            assert ip(self.rho, a) * 2 == ip(a, a), '%s：$(\\rho,\\alpha^\\vee)\\ne1$' % name
        if extra is not None:
            for a in self.pos:
                assert ip(a, extra) == 0, '%s：额外 $U(1)$ 方向与根不正交' % name

    def labels(self, mu):
        return tuple(ipp(mu, a) for a in self.simples)

    def dominant(self, mu):
        lab = self.labels(mu)
        return all(x >= 0 for x in lab)

    def dim(self, lam):
        r"""$\dim_H(\lambda)=\prod_{\beta>0}(\lambda+\rho_H,\beta)/(\rho_H,\beta)$。"""
        num, den = 1, 1
        for a in self.pos:
            num *= ip(add(lam, self.rho), a)
            den *= ip(self.rho, a)
        q = F(num, den)
        assert q.denominator == 1, '%s：Weyl 维数不是整数' % self.name
        return int(q)


SUB_3221 = SUB_422 = None
if BL is not None:
    SUB_3221 = Subsystem('3221', [sub(EPS[0], EPS[1]), sub(EPS[1], EPS[2]), A1_L, A1_R],
                         extra=BL)
SUB_422 = Subsystem('422', [sub(EPS[0], EPS[1]), sub(EPS[1], EPS[2]), add(EPS[1], EPS[2]),
                            A1_L, A1_R])


# $SU(3)_c$ 与 $SU(4)_c$ 因子**单独**取出来：R6.4 用它们把「整块的 Weyl 乘积公式」与
# 「闭式维数公式」对上，从而分支表里每个分量的维数都由两条独立路径给出。
SUB_A2 = Subsystem('A2', [sub(EPS[0], EPS[1]), sub(EPS[1], EPS[2])])
SUB_A3 = Subsystem('A3', [sub(EPS[0], EPS[1]), sub(EPS[1], EPS[2]),
                          add(EPS[1], EPS[2])])
# $A_2$ 配上 $B-L$ 作额外方向：这就是 $3221$ 的色因子，也是 $R6.7$ 里 $A_3\downarrow A_2\times U(1)$
# 的落脚点（$B-L$ 与 $A_2$ 的所有根正交 ⇒ `Subsystem` 构造时那条断言自动把关）。
SUB_A2B = None
if BL is not None:
    SUB_A2B = Subsystem('A2(B-L)', [sub(EPS[0], EPS[1]), sub(EPS[1], EPS[2])], extra=BL)
BRANCH = []                                           # 供报告 §5 取用


def branching(ms, S):
    """把权重多重集 $ms$ 限制到子系统 $S$：返回按标号排序的分支表。

    候选最高权 = 全部 $S$-支配的权重；重数由 Klimyk–Springer 交错和给出。
    算出**负重数**说明标号系统或 Weyl 群有误 ⇒ 当场报错，不做静默丢弃。
    """
    out = []
    for lam in sorted(l for l in ms if S.dominant(l)):
        mu = add(lam, S.rho)
        k = 0
        for M, sg in S.W.items():
            k += sg * ms.get(sub(mat_vec(M, mu), S.rho), 0)
        assert k >= 0, '%s：分支重数为负（%s）⇒ 子系统构造有误' % (S.name, lam)
        if k:
            out.append({'wt': lam, 'labels': S.labels(lam), 'dim': S.dim(lam), 'n': k,
                        'bl': None if S.extra is None else chg(lam, S.extra)})
    return out


def dim3(p, q):
    """$SU(3)$ 的 $(p,q)$ 维数公式（与 R6.3 的 Weyl 乘积公式**不同**的代码路径）。"""
    return (p + 1) * (q + 1) * (p + q + 2) // 2


# $D_3\simeq A_3$ 的**槽位映射**：本引擎取的单根是 $\beta_1=\varepsilon_1-\varepsilon_2$、
# $\beta_2=\varepsilon_2-\varepsilon_3$、$\beta_3=\varepsilon_2+\varepsilon_3$，而
# $(\beta_1,\beta_2)=(\beta_1,\beta_3)=-1$、$(\beta_2,\beta_3)=0$ ⇒ Dynkin 链是
# "$\beta_3-\beta_1-\beta_2$"，即标准 $A_3$ 编号 $(p_1,p_2,p_3)=(c,a,b)$。槽位放错就会把
# $SU(4)$ 的 $6$ 读成 $4$ —— 这正是 R6.4 要抓的错。
def a3_slot(lab):
    return (lab[2], lab[0], lab[1])


def dim4(a, b, c):
    """$SU(4)=A_3$ 在**标准槽位**下的闭式维数（与子群 Weyl 乘积公式不同的代码路径）。"""
    return ((a + 1) * (b + 1) * (c + 1) * (a + b + 2) * (b + c + 2) * (a + b + c + 3)
            // 12)


def su_name(lab, d):
    """共轭由标号倒序给出（$A_2,A_3$ 同规则）：倒序**较大**者即为共轭表示。"""
    return ('\\overline{%d}' % d) if tuple(reversed(lab)) > tuple(lab) else '%d' % d


def fmt_3221(row):
    """$(SU(3)_c,\ SU(2)_L,\ SU(2)_R)_{B-L}$ 记法（输出可直接放进数学环境）。"""
    lab = row['labels']
    return '(%s,%d,%d)_{%s}' % (su_name(lab[:2], dim3(*lab[:2])), lab[2] + 1,
                                lab[3] + 1, row['bl'])


def fmt_422(row):
    """$(SU(4)_c,\ SU(2)_L,\ SU(2)_R)$ 记法（$U(1)$ 已在 $SU(4)$ 里）。"""
    lab = row['labels']
    s = a3_slot(lab[:3])
    return '(%s,%d,%d)' % (su_name(s, dim4(*s)), lab[3] + 1, lab[4] + 1)


def branch_sum(rows):
    return sum(r['n'] * r['dim'] for r in rows)


def branch_tex(rows, fmt):
    """把一个表示的整条分支写成 $A\oplus B\oplus\cdots$（重数 $>1$ 时前置 $n\cdot$）。"""
    return '\\oplus'.join([('%d\\cdot' % r['n'] if r['n'] > 1 else '') + fmt(r)
                            for r in rows])


def tex_name(nm):
    """'10̄' → $\\overline{10}$（只用于报告表头）。"""
    return ('$\\overline{%s}$' % nm[:-1]) if nm.endswith('\u0304') else ('$%s$' % nm)


def plain(s):
    """终端用的去 LaTeX 版（只用于打印，不参与任何判定）。"""
    return (s.replace('\\overline{', '~').replace('_{', '_').replace('}', '')
            .replace('\\oplus', ' + ').replace('\\cdot', '*'))


def run_branching():
    """R6：两条链的完整分支规则（含与 §1 递推、与串检验的三方交叉比对）。"""
    p = True
    if SUB_3221 is None:
        return ok('R6.0', '子群分支需要 $B-L$ 方向（载入 `so10_chain.py`）', False,
                  'so10_chain 未载入 ⇒ 分支规则不出结论')
    p &= exact('R6.1', '两个极大秩子系统的正根数：3221 的 $A_2\oplus A_1\oplus A_1$ '
                       '$=3+1+1$，422 的 $D_3\oplus A_1\oplus A_1=A_3\oplus A_1\oplus A_1$ '
                       '$=6+1+1$（根总数分别 $10,16$；$D_3\cong A_3$ 由实现自动完成）',
               [len(SUB_3221.pos), len(SUB_422.pos)], [5, 8],
               '$(\\rho,\\alpha^\\vee)=1$ 与单根长度已在上层断言')
    p &= exact('R6.2', 'Weyl 群阶：$|W(A_2\oplus A_1\oplus A_1)|=6\cdot2\cdot2=24$，'
                       '$|W(A_3\oplus A_1\oplus A_1)|=24\cdot2\cdot2=96$（闭包+符号一致性已断言）',
               [len(SUB_3221.W), len(SUB_422.W)], [24, 96])
    rows2, rows4, sums = {}, {}, {}
    for nm in ORDER:
        if nm not in NAMED:
            continue
        ms = irrep(NAMED[nm])[1]
        r2 = branching(ms, SUB_3221)
        r4 = branching(ms, SUB_422)
        rows2[nm], rows4[nm] = r2, r4
        sums[nm] = [branch_sum(r2), branch_sum(r4), sum(ms.values())]
    p &= exact('R6.3', '分支完整性（对每个表示、两条链）：$\sum_\lambda n_\lambda\,'
                       '\dim_H(\lambda)=\dim\Lambda$（漏掉或多算任何分量都会破坏等式）',
               sums, dict((k, [v[2], v[2], v[2]]) for k, v in sums.items()),
               '逐项核验 %d 个表示' % len(sums))
    chk, bad = 0, []
    for nm, r2 in rows2.items():
        for r in r2:
            c = dim3(*r['labels'][:2])
            chk += 1
            if SUB_A2.dim(r['wt']) != c or \
                    r['dim'] != c * (r['labels'][2] + 1) * (r['labels'][3] + 1):
                bad.append((nm, fmt_3221(r)))
    for nm, r4 in rows4.items():
        for r in r4:
            c = dim4(*a3_slot(r['labels'][:3]))
            chk += 1
            if SUB_A3.dim(r['wt']) != c or \
                    r['dim'] != c * (r['labels'][3] + 1) * (r['labels'][4] + 1):
                bad.append((nm, fmt_422(r)))
    p &= ok('R6.4', '分支表里每个分量的维数由两条独立路径给出且相等：整块 Weyl 乘积公式 '
                    '= 因子 Weyl 乘积公式 = $(p,q)$/$(p,q,r)$ 闭式（$\\times2$ 的 $SU(2)$ 因子'
                    '一并核对 ⇒ 直和因子化成立）',
            not bad, '核验 %d 个分量；不符：%s' % (chk, bad or '无'))
    kinds = {}
    for nm, r2 in rows2.items():
        s = set()
        for r in r2:
            if r['labels'][0] or r['labels'][1] or abs(r['bl']) != 2:
                continue
            l, rr = r['labels'][2], r['labels'][3]
            s.add(('DR' if (l, rr) == (0, 2) else 'DL' if (l, rr) == (2, 0) else
                   'S' if (l, rr) == (0, 0) else 'other', str(r['bl'])))
        kinds[nm] = s
    ref = dict((r['name'], set((g['kind'], g['BL']) for g in r['bl2groups']))
               for r in TABLE)
    p &= exact('R6.5', '分支表与 R5 的串检验**双向**一致：$|B-L|=2$ 的色单态按 '
                       '$(SU(2)_L,SU(2)_R)$ 类型归档，两套完全独立的算法给出同一个集合'
                       '（$\\Delta_R\leftrightarrow(1,1,3)$、$\\Delta_L\leftrightarrow'
                       '(1,3,1)$、$(1,1,1)_{\\pm2}$）',
               dict((k, sorted(v)) for k, v in kinds.items()),
               dict((k, sorted(v)) for k, v in ref.items()),
               '非空者：%s' % dict((k, sorted(v)) for k, v in kinds.items() if v))
    # 物理锚点：$16_F$ 与 $10_H$ 的限制是文献里的标准结果（本项目唯一使用外部答案之处）。
    # 只比 $|B-L|$：本引擎的 $B-L$ 整体符号与部分文献相反（R5.7 已把符号钉在自己的约定里）。
    key = lambda rows: sorted((((r['labels']), (None if r['bl'] is None
                                                else abs(r['bl'])), r['n'])
                               for r in rows),
                              key=lambda t: (str(t[0]), str(t[1]), t[2]))
    got = {'16': [key(rows2['16']), key(rows4['16'])],
           '10': [key(rows2['10']), key(rows4['10'])]}
    exp = {'16': [[((0, 0, 0, 1), F(1), 1), ((0, 0, 1, 0), F(1), 1),
                   ((0, 1, 0, 1), F(1, 3), 1), ((1, 0, 1, 0), F(1, 3), 1)],
                  [((0, 0, 1, 1, 0), None, 1), ((0, 1, 0, 0, 1), None, 1)]],
           '10': [[((0, 0, 1, 1), F(0), 1), ((0, 1, 0, 0), F(2, 3), 1),
                   ((1, 0, 0, 0), F(2, 3), 1)],
                  [((0, 0, 0, 1, 1), None, 1), ((1, 0, 0, 0, 0), None, 1)]]}
    p &= exact('R6.6', '物理锚点（文献比对，非推导）：$16_F\\to(3,2,1)\\oplus(\\overline{3},1,2)'
                       '\\oplus(1,2,1)\\oplus(1,1,2)$（一整代费米子，'
                       '含 $\\nu^c$），$422$ 侧 $=(4,2,1)\\oplus(\\overline{4},1,2)$；'
                       '$10_H\\to(3,1,1)\\oplus(\\overline{3},1,1)\\oplus(1,2,2)$，'
                       '$422$ 侧 $=(6,1,1)\\oplus(1,2,2)$。$SU(4)$ 的 $4/\\overline{4}/6$ '
                       '归属同时检验 $D_3\\simeq A_3$ 的实现（标号按本引擎的 $\\beta$ 槽位写）',
               got, exp, '$B-L$ 只比绝对值；$SU(4)$ 侧无额外 $U(1)$')
    BRANCH[:] = [{'name': nm,
                  'n3221': len(rows2[nm]), 'n422': len(rows4[nm]),
                  'tex3221': branch_tex(rows2[nm], fmt_3221),
                  'tex422': branch_tex(rows4[nm], fmt_422),
                  'c1': [[fmt_3221(r), r['n']] for r in rows2[nm]
                         if not r['labels'][0] and not r['labels'][1]],
                  'sum3221': branch_sum(rows2[nm]), 'sum422': branch_sum(rows4[nm])}
                 for nm in ORDER if nm in rows2]
    return p


# ================================================== 跨链匹配：$422\downarrow3221$ 路径无关性
SUB_MS = {}                                           # (子系统, 最高权) -> 权重多重集
FUNDW = {}                                            # 子系统名 -> 基本权重（真实坐标）
CROSS = []                                            # 供报告 §5 取用


def sub_irrep(lam, S):
    r"""子系统版 Freudenthal–Racah：返回 $S$-不可约表示（最高权 $\lambda$）的权重多重集。

    与 D5 版同一算法、同一坑位断言（分母带 $\rho$ 平移；按 $(\Lambda-\mu,\rho_H)$ 升序处理）。
    两处必须的差别：
    1. 深度只取**差** $(\Lambda-\mu,\rho_H)$。子系统的 $\rho_H$ 一般使 $(\mu,\rho_H)$ 自身
       不是整数（例：$A_3$ 的 $\rho=2\varepsilon_1+\varepsilon_2$ 在半整数权重上给出半整数）。
    2. 收口用 $\sum_\mu m_\mu=\dim_H(\lambda)$，右端走**另一条**代码路径
       （`Subsystem.dim` 的 Weyl 乘积公式）⇒ 权重递推与维数公式互检。
    """
    key = (S.name, lam)
    if key not in SUB_MS:
        hmax = ip(lam, lam)
        lamr = ip(lam, S.rho)
        cand, stack = {lam}, [lam]
        while stack:
            u = stack.pop()
            for a in S.simples:
                w = sub(u, a)
                if ip(w, w) <= hmax and w not in cand:
                    cand.add(w)
                    stack.append(w)
        depth = {}
        for mu in cand:
            d = lamr - ip(mu, S.rho)
            assert d >= 0 and d % D4 == 0, '%s：$(\\Lambda-\\mu,\\rho_H)$ 异常（%s）' % (S.name, mu)
            depth[mu] = d // D4
        assert min(depth.values()) == 0, '%s：起点不是最高权' % S.name
        sr2 = ip(add(lam, S.rho), add(lam, S.rho))
        m = {}
        for mu in sorted(cand, key=lambda x: depth[x]):
            if mu == lam:
                m[mu] = 1
                continue
            den = sr2 - ip(add(mu, S.rho), add(mu, S.rho))
            assert den > 0, '%s：Freudenthal 分母非正（%s）' % (S.name, mu)
            tot = 0
            for a in S.pos:
                i = 1
                while True:
                    w = add(mu, smul(i, a))
                    if w not in cand:
                        break
                    if m.get(w, 0):
                        tot += m[w] * ip(w, a)
                    i += 1
            val = F(2 * tot, den)
            assert val.denominator == 1, '%s：Freudenthal 重数不整除（%s）' % (S.name, mu)
            m[mu] = int(val)
        out = dict((mu, k) for mu, k in m.items() if k > 0)
        assert sum(out.values()) == S.dim(lam), \
            '%s：权重总重数 %d $\\ne$ Weyl 维数 %d' % (S.name, sum(out.values()), S.dim(lam))
        SUB_MS[key] = out
    return SUB_MS[key]


def _rref(M):
    r"""精确有理数行最简形，返回 $(M,\text{主元列})$。"""
    rows, ncols = len(M), len(M[0])
    piv, r = [], 0
    for c in range(ncols):
        k = next((i for i in range(r, rows) if M[i][c]), None)
        if k is None:
            continue
        M[r], M[k] = M[k], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [M[i][j] - f * M[r][j] for j in range(ncols)]
        piv.append(c)
        r += 1
        if r == rows:
            break
    return M, piv


def _solve(A, b):
    r"""非奇异方阵的精确解 $Ax=b$。"""
    n = len(A)
    M = [list(A[j]) + [b[j]] for j in range(n)]
    M, piv = _rref(M)
    assert piv == list(range(n)), '线性方程组奇异，解不唯一'
    return tuple(M[j][n] for j in range(n))


def nullspace(A, ncols):
    r"""$Ax=0$ 的精确有理数零空间基。"""
    M, piv = _rref([[F(x) for x in row] for row in A])
    out = []
    for f in [c for c in range(ncols) if c not in piv]:
        v = [F(0)] * ncols
        v[f] = F(1)
        for i, c in enumerate(piv):
            v[c] = -M[i][f]
        out.append(tuple(v))
    return out


def sub_fundweights(S):
    r"""$S$ 的基本权重（真实 $\varepsilon$ 坐标，Fraction）：解 $(\omega_i,\beta_j)=\delta_{ij}$。"""
    n = len(S.simples)
    G = [[F(ip(S.simples[j], S.simples[k]), D4) for k in range(n)] for j in range(n)]
    ws = []
    for i in range(n):
        c = _solve(G, [F(int(j == i)) for j in range(n)])
        w = [F(0)] * 5
        for j in range(n):
            for k in range(5):
                w[k] += c[j] * F(S.simples[j][k], U)
        ws.append(tuple(w))
    return ws


def sub_label_to_wt(S, cs):
    """子系统 Dynkin 标号 -> 本引擎的格点整数向量（分母不整除 12 时 `to_grid_dir` 当场报错）。"""
    ws = FUNDW.setdefault(S.name, sub_fundweights(S))
    v = [F(0)] * 5
    for c, w in zip(cs, ws):
        for k in range(5):
            v[k] += c * w[k]
    return to_grid_dir(v, '%s 标号 %s 的权' % (S.name, cs))


def a3_orthogonal_to_a2():
    r"""$\mathrm{span}(A_3)$ 中与 $A_2$ 全部单根正交的方向（模标度，真实 Fraction 坐标）。"""
    A3, A2 = SUB_A3.simples, SUB_A2.simples
    rows = [[F(ip(a, b), D4) for a in A3] for b in A2]
    out = []
    for t in nullspace(rows, len(A3)):
        v = [F(0)] * 5
        for c, a in zip(t, A3):
            for k in range(5):
                v[k] += c * F(a[k], U)
        out.append(tuple(v))
    return out


def proportion(a, b):
    r"""若 $a=\lambda b$ 则返回 $\lambda$（精确有理数），否则 None。"""
    z = next((k for k in range(5) if a[k]), None)
    if z is None or not b[z]:
        return None
    kap = F(a[z], b[z])
    return kap if all(a[k] == kap * b[k] for k in range(5)) else None


def real(v):
    r"""格点整数向量 -> 真实（$\varepsilon$ 单位）Fraction 向量。"""
    return tuple(F(x, U) for x in v)


def key_3221(a2lab, l, r, bl):
    """两条路径共用的键：$((p,q),\ SU(2)_L$ 标号$, \ SU(2)_R$ 标号$, \ B-L)$。"""
    return (tuple(a2lab), l, r, bl)


def direct_3221(nm):
    r"""一步限制 $SO(10)\downarrow3221$，换成 `key_3221` 键空间。"""
    out = {}
    for r in branching(irrep(NAMED[nm])[1], SUB_3221):
        out[key_3221(r['labels'][:2], r['labels'][2], r['labels'][3], r['bl'])] = r['n']
    return out


def via_422(nm):
    r"""两步限制：先 $SO(10)\downarrow422$，再对每个 $SU(4)$ 多重态走 $A_3\downarrow A_2\times U(1)_{B-L}$。

    两个 $SU(2)$ 是旁观因子：$A_3$ 的单根全支撑在 $\varepsilon_1,\varepsilon_2,\varepsilon_3$ 上，
    故权重的 $\varepsilon_4,\varepsilon_5$ 分量在色分支中原样保留，$B-L$ 也只读前三格。
    """
    out = {}
    for r in branching(irrep(NAMED[nm])[1], SUB_422):
        for s in branching(sub_irrep(r['wt'], SUB_A3), SUB_A2B):
            k = key_3221(s['labels'], r['labels'][3], r['labels'][4], s['bl'])
            out[k] = out.get(k, 0) + r['n'] * s['n']
    return out


def run_cross_chain():
    r"""R6.7/R6.8：$422\to3221$ 的路径无关性，与 $B-L$ 作为 $SU(4)$ 内的无迹生成元。"""
    p = True
    if SUB_A2B is None:
        return ok('R6.7', '跨链匹配需要 $B-L$ 方向（载入 `so10_chain.py`）', False,
                  'so10_chain 未载入 ⇒ 不出结论')
    agree, bad = {}, []
    for nm in ORDER:
        if nm not in NAMED:
            continue
        a, b = direct_3221(nm), via_422(nm)
        agree[nm] = (a == b)
        if a != b:
            bad.append((nm, [str(k) for k in a if b.get(k) != a[k]],
                        [str(k) for k in b if a.get(k) != b[k]]))
    p &= exact('R6.7', '跨链路径无关性（$\\dim\\le210$ 的每个表示）：'
                       '$\\mathrm{Res}^{422}_{3221}\\big(\\mathrm{Res}^{SO(10)}_{422}\\Lambda\\big)'
                       '=\\mathrm{Res}^{SO(10)}_{3221}\\Lambda$ 作为 '
                       '$(SU(3)_c,SU(2)_L,SU(2)_R)_{B-L}$ **多重集**逐项相等。左端要先对每个 '
                       '$SU(4)$ 多重态做子系统 Freudenthal 权重递推、再分支到 $A_2\\times U(1)_{B-L}$；'
                       '右端直接把 D5 权重格投到 3221；两条路径共用同一份 D5 权重多重集',
               agree, dict((k, True) for k in agree),
               '不一致的表示：%s' % (bad or '无'))
    dirs = a3_orthogonal_to_a2()
    kap = proportion(dirs[0], real(BL)) if (len(dirs) == 1 and BL is not None) else None
    p &= ok('R6.8a', '$B-L$ **就是** $SU(4)_c$ 的 Cartan 里与 $SU(3)_c$ 对易的那个 $U(1)$：'
                     '$\\mathrm{span}(A_3)$ 中与 $A_2$ 全部单根正交的方向**恰 1 维**，'
                     '且与链探针的 $B-L$ 方向成比例（比例 $%s$，只是两种归一化的差别）'
                     '$\\Rightarrow422\\to3221$ 不必另外引入 $U(1)$' % kap,
            kap is not None, '唯一性是整数线性代数的结论；比例 $\\ne1$ 不改变方向')
    labels = []
    for cs in [tuple(1 if j == i else 0 for j in range(3)) for i in range(3)] + \
              [cs for cs in itertools.product(range(3), repeat=3) if 0 < sum(cs) <= 2]:
        if cs not in labels:
            labels.append(cs)
    tr = []
    for cs in labels:
        lam = sub_label_to_wt(SUB_A3, cs)
        ms = sub_irrep(lam, SUB_A3)
        d = SUB_A3.dim(lam)
        rows = branching(ms, SUB_A2B)
        book = sum(r['n'] * dim3(*r['labels']) for r in rows)
        assert book == d, 'R6.8：$A_3$ 标号 %s 的色分支维数账不平（%d vs %d）' % (cs, book, d)
        s = a3_slot(cs)
        nm = su_name(s, d)
        tr.append({'name': nm, 'key': '%s(%s)' % (nm, ','.join(map(str, s))),
                   'std': list(s), 'dim': d, 'nwt': len(ms),
                   'tr': str(sum(k * chg(mu, BL) for mu, k in ms.items())),
                   'content': ['%s%s' % ('%d\\cdot' % r['n'] if r['n'] > 1 else '',
                                         fmt_3221({'labels': r['labels'] + (0, 0),
                                                   'bl': r['bl']})) for r in rows]})
    # 同名不同标号是真实的（$A_3$ 的 (1,0,1) 与 (2,0,0) 都是 20 维），
    # 所以门禁的键必须带 Dynkin 标号，报告表格才继续用可读名
    assert len(set(t['key'] for t in tr)) == len(tr), 'R6.8：表示标识冲突'
    p &= exact('R6.8', '$B-L$ 在 $SU(4)$ 的**每个**不可约表示上无迹：'
                       '$\\sum_\\mu m_\\mu\\,(B-L)(\\mu)=0$。核验范围：$A_3$ 的三个基本表示加上'
                       '$\\sum c_i\\le2$ 的全部标号（共 %d 个表示、%d 个不同权重）；'
                       '同一循环里逐个核验 $A_2\\times U(1)_{B-L}$ 的维数账 '
                       '$\sum n_\lambda\dim(\lambda)=\dim$' % (len(tr), sum(t['nwt'] for t in tr)),
               dict((t['key'], t['tr']) for t in tr),
               dict((t['key'], '0') for t in tr), '精确零（全程有理数，无浮点容差）')
    CROSS[:] = tr
    return p
# =============================================================== 引擎自检
def run_engine_tests():
    p = True
    # --- 0. 李论输入自洽：实现必须重现 Dynkin 图
    p &= exact('R0.1', '$\\varepsilon$ 基实现重现由 Dynkin 图导出的 Cartan 矩阵',
               cartan_from_realization(), CARTAN_IN,
               '唯一李论输入 = D5 图（链 1-2-3；节点 3 分叉到 4、5）')
    p &= exact('R0.2', '全部单根长度平方 $=2$（长根归一）',
               [nrm2(a) for a in SIMPLE], [F(2)] * 5)
    p &= exact('R0.3', '正根个数 $|D_5^+|$（枚举组合中 $|(\\cdot)|^2=2$ 者）',
               len(PH), 20)
    p &= exact('R0.4', '根空间计数 $5+2\\times20$ = 伴随表示的 Weyl 维数',
               RANK + len(ROOTS), weyl_dim(weight_of_label((0, 1, 0, 0, 0))),
               '右端由 §1 的维数公式独立给出 ⇒ 根系统与维数公式互相校验')
    p &= exact('R0.5', '$\\rho=\\tfrac12\\sum_{\\alpha>0}\\alpha=\\sum_i\\omega_i$（定理现场校验）',
               RHO, weight_of_label((1, 1, 1, 1, 1)))
    p &= exact('R0.6', '$(\\omega_i,\\alpha_j)=\\delta_{ij}$（基本权重的定义方程）',
               [[nrm(FUND[i], SIMPLE[j]) for j in range(RANK)] for i in range(RANK)],
               [[F(1) if i == j else F(0) for j in range(RANK)] for i in range(RANK)])
    p &= exact('R0.7', '$|W(D_5)|=2^{4}\\cdot5!=1920$（$\\rho$ 是正则权 ⇒ 其轨道大小 $=$ Weyl 群阶）；'
                       '对照：$\\omega_1$ 的轨道 $=2n=10$ 即向量表示的权重数（稳定子 $=W(D_4)$，阶 $192$）',
               [len(weyl_orbit(RHO)), len(weyl_orbit(EPS[0]))], [1920, 10],
               '轨道–稳定子定理：$1920=10\\times192$')
    p &= exact('R0.8', '$(\\alpha_i,\\rho)=1$ 对全部单根（递推顺序用得到的恒等式）',
               [ipp(a, RHO) for a in SIMPLE], [1] * 5)
    # --- 1. Weyl 维数 vs Freudenthal 总重数
    bad = []
    for cs in LOW_LABELS:
        Lam, ms, dw, df, c2 = irrep(cs)
        if dw != df or df <= 0:
            bad.append((list(cs), dw, df))
    p &= ok('R1.1', '对全部 %d 个低标号表示（$\\sum c_i\\le2$，含 $\\dim 1200$）：'
                   '$\\sum_\\mu m_\\mu$（Freudenthal）$=\\dim$（Weyl 公式）' % len(LOW_LABELS),
            not bad, '不一致清单：%s' % (bad[:6] if bad else '空'))
    p &= ok('R1.2', '$10$ 与 $16$ 是 **minuscule** 表示：全部权重同处一个 Weyl 轨道、'
                    '重数全为 1（由递推**算出**，不是设定）',
            all(set(irrep(cs)[1]) == weyl_orbit(weight_of_label(cs)) and
                set(irrep(cs)[1].values()) == {1}
                for cs in ((1, 0, 0, 0, 0), (0, 0, 0, 1, 0), (0, 0, 0, 0, 1))),
            '$\\omega_1$（向量）与两个自旋量标号 $\\omega_4,\\omega_5$ 的权重数 10/16/16')
    p &= exact('R1.3', '最高根 $\\theta$（唯一的支配正根 $=\\varepsilon_1+\\varepsilon_2$）：'
                       'Dynkin 标号 $\\to$ 伴随标号，单根系数 $=$ marks',
               [fmt(TH), list(dynkin(TH)), list(TH_MARKS)],
               ['(1,1,0,0,0)', [0, 1, 0, 0, 0], [1, 2, 2, 1, 1]],
               '标号 $(0,1,0,0,0)$ 与 R0.4 中按维数公式取伴随表示的标号同源')
    adj = madd(from_list(ROOTS), {ZERO: RANK})
    p &= exact('R1.4', '$\\theta$ 的 Freudenthal 权重集 $=$ 根 $\\cup\\{0^{\\times5}\\}$',
               sorted(irrep(dynkin(TH))[1].items()), sorted(adj.items()))
    p &= exact('R1.5', '$(\\theta,\\theta+2\\rho)=2h^\\vee$；$D_5$ 的对偶 Coxeter 数 '
                       '$h^\\vee=2n-2=8$（伴随的 Casimir）',
               casimir2(TH) / 2, F(8))
    return p


# =============================================================== 表示识别（标号由计算给出）
NAMED = {}


def run_identification():
    p = True
    if chain is None or not CHAIN_OK:
        return ok('R2.0', '链探针 `so10_chain.py` 的引擎自检全部通过（荷约定的同源前提）', False,
                  '上游引擎未通过 ⇒ 本探针不出结论')
    p &= ok('R2.0', '链探针 `so10_chain.py` 的引擎自检全部通过（荷约定的同源前提）', True,
            '%d 项自检 PASS ⇒ $B-L$、$T^3_{L,R}$、$Y$ 方向可直接沿用' % len(chain.RESULTS))
    for nm, ws in (('10', chain.W10()), ('16', chain.W16()), ('45', chain.W45())):
        ms = grid_ms(ws)
        lab = find(msum(ms), ms)
        p &= ok('R2.%s' % nm, '链探针显式构造的 $%s$ 权重多重集 $=$ 本引擎 Freudenthal '
                              '权重集 ⇒ 唯一选定 Dynkin 标号' % nm, lab is not None,
                '标号：%s；按维数 %d 的候选：%s' %
                (lab, msum(ms), [list(cs) for cs in DIMMAP.get(msum(ms), [])]))
        if lab is None:
            return False
        NAMED[nm] = lab
        p &= exact('R2.d%s' % nm, '$%s$：Weyl 维数 $=\\sum_\\mu m_\\mu=$ 链探针权重个数' % nm,
                   (irrep(lab)[2], irrep(lab)[3]), (msum(ms), msum(ms)))
    conj = {}
    for nm in ('10', '16', '45'):
        conj[nm] = list(dominant(neg(weight_of_label(NAMED[nm])))[1])
        NAMED[nm + '̄'] = tuple(conj[nm])
    p &= exact('R2.c10c45', '$10$ 与 $45$ 是**实**表示（共轭标号 = 自身）',
               [conj['10'] == list(NAMED['10']), conj['45'] == list(NAMED['45'])], [True, True])
    p &= ok('R2.c16', '$16$ 是**复**表示（$\\overline{16}\\neq16$ ⇒ 手征性得以存在）',
            conj['16'] != list(NAMED['16']),
            '$16$ 标号 %s，$\\overline{16}$ 标号 %s' % (list(NAMED['16']), conj['16']))

    # ---- R2.sw：本报告引用的"摆动倍数"必须与链探针当场一致
    band = chain_band()
    p &= ok('R2.sw0', '链探针在单阈 3221 链上至少给出**两条**物理解（"摆动倍数"才有定义）',
            band is not None and len(band) >= 2,
            '物理解：%s' % ('、'.join('%s=%.3e' % t for t in (band or [])) or '无'))
    if band:
        lo = min(band, key=lambda t: t[1])
        hi = max(band, key=lambda t: t[1])
        p &= ok('R2.sw1', '区间两端来自两个**不同**情形（同一情形既当两端 ⇒ 倍数恒为 1，是空话）',
                lo[0] != hi[0], '两端 = %s↔%s，倍数 %.2f' % (lo[0], hi[0], hi[1] / lo[1]))
    # ---- 变异测试：证明倍数是**算出来**的，不是写死在格式化函数里的字符串。
    # （R2.sw0/sw1 只看读取是否成功；把 swing_note 改成 `return '8.7 倍（…）'` 它们照样绿。）
    p &= exact('R2.sw2', '植入带 A=2、B=17 ⇒ 文本必须是 8.5 倍（格式器变异测试，防写死）',
               swing_note(band=[('A', 2.0), ('B', 17.0)], nested=True),
               '8.5 倍——情形 A↔B，2 条物理解**并列**区间，不是误差棒')
    p &= ok('R2.sw3', '植入空带 ⇒ 必须落到"未对账"分支（守卫不是死代码）',
            '未对账' in swing_note(band=[]),
            '实际文本：%s' % swing_note(band=[]))
    return p


def run_tensor_identities():
    """Adams 运算与 Freudenthal 两条独立路径互检；顺带选定 54/120/126/144/210 的标号。"""
    p = True
    W = dict((nm, irrep(cs)[1]) for nm, cs in NAMED.items())
    one = {ZERO: 1}
    a10, s10 = wedge2(W['10']), sym2(W['10'])
    p &= ok('R3.1', '$\\wedge^2(10)=45$（Adams 运算 vs 独立构造的 45）',
            a10 == W['45'], '左端权重数 %d；右端 %d' % (msum(a10), msum(W['45'])))
    try:
        rem54 = msub(s10, one)
        lab54 = find(msum(rem54), rem54)
    except ArithmeticError:
        lab54 = None
    p &= ok('R3.2', '$\\mathrm{Sym}^2(10)=1\\oplus54$：剥掉单态后的多重集 $=$ 某 irrep 的 '
                    'Freudenthal 权重集（标号由等式**选出**）', lab54 is not None,
            '$\\dim\\mathrm{Sym}^2(10)=%d=1+54$；标号 %s' %
            (msum(s10), list(lab54) if lab54 else '无唯一候选'))
    if lab54 is not None:
        NAMED['54'] = lab54
    sq = tprod(W['16'], W['16'])
    S2, A2 = sym2(W['16']), wedge2(W['16'])
    p &= ok('R3.3', '$\\mathrm{Sym}^2(16)\\oplus\\wedge^2(16)=16\\otimes16$（Adams 自洽）',
            madd(S2, A2) == sq,
            '$%d=%d+%d$' % (msum(sq), msum(S2), msum(A2)))
    lab120 = find(msum(A2), A2)
    p &= ok('R3.4', '$\\wedge^2(16)=120$：Adams 多重集 $=$ 唯一标号的 Freudenthal 权重集',
            lab120 is not None, '标号：%s；按维数的候选：%s' %
            (list(lab120) if lab120 else '无唯一候选',
             [list(cs) for cs in DIMMAP.get(msum(A2), [])]))
    if lab120 is not None:
        NAMED['120'] = lab120
    try:
        rem126 = msub(S2, W['10'])
        lab126 = find(msum(rem126), rem126)
    except ArithmeticError:
        lab126 = None
    p &= ok('R3.5', '$\\mathrm{Sym}^2(16)=10\\oplus126$：剥掉 10 后的多重集 $=$ '
                    '唯一标号的 Freudenthal 权重集', lab126 is not None,
            '标号：%s；其共轭即 $\\overline{126}$' %
            (list(lab126) if lab126 else '无唯一候选',))
    if lab126 is not None:
        NAMED['126'] = lab126
        NAMED['126̄'] = tuple(dominant(neg(weight_of_label(lab126)))[1])
    if '16̄' in NAMED:
        W['16̄'] = irrep(NAMED['16̄'])[1]
        pd = tprod(W['16'], W['16̄'])
        try:
            rem210 = msub(pd, one, W['45'])
            lab210 = find(msum(rem210), rem210)
        except ArithmeticError:
            lab210 = None
        p &= ok('R3.6', '$16\\otimes\\overline{16}=1\\oplus45\\oplus210$：剥掉 $1\\oplus45$ 后'
                        '的多重集 $=$ 唯一标号的 Freudenthal 权重集', lab210 is not None,
                '标号：%s；按维数 210 的候选：%s（两个标号同维数，靠权重多重集区分）' %
                (lab210, [list(cs) for cs in DIMMAP.get(210, [])]))
        if lab210 is not None:
            NAMED['210'] = lab210
        pt = tprod(W['10'], W['16'])
        try:
            rem144 = msub(pt, W['16̄'])       # 向量乘自旋量必换手征 ⇒ 剥的是 $\\overline{16}$
            lab144 = find(msum(rem144), rem144)
        except ArithmeticError:
            lab144 = None
        p &= ok('R3.7', '$10\\otimes16=\\overline{16}\\oplus\\overline{144}$：'
                        '向量乘自旋量必**换手征**（直接剥 $16$ 会出现负重数，代码当场拒绝）；'
                        '剥掉后剩下的多重集 $=$ 唯一标号的 Freudenthal 权重集',
                lab144 is not None,
                '左端 $\\overline{144}$ 标号：%s；登记用的 $144$ 取其共轭' %
                (list(lab144) if lab144 else '无唯一候选',))
        if lab144 is not None:
            NAMED['144'] = tuple(dominant(neg(weight_of_label(lab144)))[1])
    return p


# =============================================================== 荷谱与物理判定
def run_physics_tests():
    p = True
    p &= exact('R4.1', '$Y=T^3_R+\\tfrac{B-L}{2}$ 作为 Cartan 方向恒等式'
                       '（于是 $Q=T^3_L+Y=T^3_L+T^3_R+\\tfrac{B-L}{2}$）',
               YHP, add(T3R, half(BL)))
    W16 = irrep(NAMED['16'])[1]

    def tr16(dirn, k=1):
        return sum(chg(w, dirn) ** k * W16[w] for w in W16)      # 按重数求和

    p &= exact('R4.2', '$B-L$ 在 16 上的取值集合（三代费米子的族结构标记）',
               sorted(set(chg(w, BL) for w in W16)), [F(-1), F(-1, 3), F(1, 3), F(1)])
    p &= exact('R4.3', '$\\mathrm{Tr}_{16}(Y)=0$', tr16(YHP), F(0))
    p &= exact('R4.4', '$\\mathrm{Tr}_{16}(Y^3)=0$（逐代 $[U(1)_Y]^3$ 反常相消）',
               tr16(YHP, 3), F(0))
    p &= exact('R4.5', '$\\mathrm{Tr}_{16}((T^3_L)^2)=\\mathrm{Tr}_{16}((T^3_R)^2)=2$'
                       '（与链探针同源）',
               (tr16(T3L, 2), tr16(T3R, 2)), (F(2), F(2)))
    qspec = {}
    for w in W16:
        qspec[chg(w, QHP)] = qspec.get(chg(w, QHP), 0) + W16[w]
    p &= exact('R4.6', '$Q=T^3_L+T^3_R+\\tfrac{B-L}{2}$ 在 16 上**恰好**给出一代左手 Weyl '
                       '费米子的标准电荷谱（含 $\\nu^c$），且 $\\mathrm{Tr}(Q)=\\mathrm{Tr}(Q^3)=0$ '
                       '⇒ 电磁方向取对了；下文 $Q=0$ 判据因此是物理的而非约定的',
               [sorted(qspec.items()), tr16(QHP), tr16(QHP, 3)],
               [[(F(-1), 1), (F(-2, 3), 3), (F(-1, 3), 3), (F(0), 2), (F(1, 3), 3),
                 (F(2, 3), 3), (F(1), 1)], F(0), F(0)],
               '电荷集对称（$\\pm$ 成对）是本仓库"偶数负号"约定的产物：该 $16$ 是教科书物质'
               '$16$ 的共轭，$|B-L|$ 与 $|Q|$ 的结论不受影响')
    order = ['10', '10̄', '16', '16̄', '45', '54', '120', '126', '126̄', '144', '210']
    missing = [n for n in order if n not in NAMED]
    p &= ok('R4.7', '待判定表示的 Dynkin 标号全部由**计算**（维数 + 多重集）认定',
            not missing, '缺失：%s' % (missing or '无'))
    return p


TABLE = []
ORDER = ('10', '10̄', '16', '16̄', '45', '54', '120', '126', '126̄', '144', '210')


def build_table():
    TABLE[:] = []
    for nm in ORDER:
        if nm not in NAMED:
            continue
        cs = NAMED[nm]
        Lam, ms, dw, df, c2 = irrep(cs)
        mx, dr, dl, ds, safe, summ, mp = carriers(ms)
        conj = list(dominant(neg(Lam))[1])
        TABLE.append({'name': nm, 'dynkin': list(cs), 'dim': dw, 'nweights': len(ms),
                      'c2': str(c2), 'real': conj == list(cs),
                      'maxBL': str(mx), 'maxBL_f': float(mx),
                      'DR': dr, 'DL': dl, 'S2': ds, 'safe': safe, 'bl2groups': summ,
                      'nDR': len(mp['DR']), 'nDL': len(mp['DL']), 'nS': len(mp['S']),
                      'bl2': len(bl2_class(ms)), 'bneg2': len(bl2_class(ms, F(-2)))})
    return TABLE


def gate_no_go():
    """核心结论把守。"""
    p = True
    rows = dict((r['name'], r) for r in TABLE)
    if not rows:
        return False
    small = [n for n in ('10', '10̄', '16', '16̄', '45', '54', '144') if n in rows]
    p &= ok('R5.1', '$\\max|B-L|<2$ 对 $10,\\overline{10},16,\\overline{16},45,54,144$ 全部成立 ⇒ '
                    '这些 Higgs 表示里**不存在** $|B-L|=2$ 的态，因此承担不了 '
                    '$|\\Delta(B-L)|=2$ 的破缺（注意：不排除 $16_H$ 以 $|\\Delta(B-L)|=1$ '
                    '单步破缺，见 R5.9）',
            len(small) == 7 and all(rows[n]['maxBL_f'] < 2.0 for n in small),
            '各自 $\\max|B-L|$：%s' % dict((n, rows[n]['maxBL']) for n in small))
    W45 = irrep(NAMED['45'])[1]
    p &= exact('R5.2', '$45_H$ 的 $B-L$ 谱 $=\\{0,\\pm2/3,\\pm4/3\\}$（$\\pm4/3$ 来自根 '
                       '$\\varepsilon_i+\\varepsilon_j$，即 $SU(4)_c$ 伴随 $15\\to3\\oplus\\bar3$ '
                       '的轻夸克胶子方向）$\\Rightarrow\\max|B-L|=4/3<2$ ⇒ $\\Sigma(1,1,3)_0\\subset45_H$ '
                       '**不是** $\\Delta_R$（链探针门禁 S2.7 的表示论根据）',
               sorted(set(chg(w, BL) for w in W45)),
               [F(-4, 3), F(-2, 3), F(0), F(2, 3), F(4, 3)])
    cand = sorted([n for n in rows if rows[n]['DR'] or rows[n]['DL']],
                  key=lambda n: rows[n]['dim'])
    safe = sorted([n for n in rows if rows[n]['safe']], key=lambda n: rows[n]['dim'])
    p &= ok('R5.3', '在 $\\dim\\le210$ 内存在承载"$|B-L|=2$ 的色单态 $+$ 弱单态 $+$ '
                    '三重态、且三重态含中性分量"的表示', bool(safe),
            '按维数升序的承载者：%s；只带 $(1,1,1)_{\\pm2}$ 带电单态者：%s' %
            (safe, [n for n in sorted(rows) if rows[n]['S2'] and not rows[n]['safe']]))
    mins = min([rows[n]['dim'] for n in safe]) if safe else None
    p &= exact('R5.4', '$\\Delta_{L/R}$ 的**最小**可能 Higgs 维数 '
                       '（$10/16/45/54/144/210$ 均不承载三重态）', mins, 126)
    p &= ok('R5.5', '仅靠 $10_H\\oplus\\overline{10}_H\\oplus16_H\\oplus\\overline{16}_H'
                    '\\oplus45_H\\oplus54_H\\oplus120_H\\oplus144_H\\oplus210_H$ **无法**承载'
                    '"$|\\Delta(B-L)|=2$ 且保 $U(1)_{em}$"的破缺 ⇒ 情形 B（无 $126_H$）的 $M_R$ '
                    '只能读作参考匹配标度（$16_H$ 的 $|\\Delta(B-L)|=1$ 单步通道见 R5.9：'
                    '留 $\\mathbb{Z}_3$ 且物质字称被它破掉（R10.5）、无可重整 $\\nu_R$ 质量）',
            not any(rows[n]['safe'] for n in ('10', '10̄', '16', '16̄', '45', '54',
                                              '120', '144', '210') if n in rows))
    # 承载者的量子数自检：$T^3$ 阶梯差 1；$Y=T^3_R+\\tfrac{B-L}{2}$；$Q=T^3_L+T^3_R+\\tfrac{B-L}{2}$
    detail, good = [], True
    for nm in ('126', '126̄'):
        if nm not in NAMED:
            continue
        mp = bl_multiplets(irrep(NAMED[nm])[1])
        for k in ('DR', 'DL'):
            for t in (F(2), F(-2)):
                grp = [r for r in mp[k] if r['BL'] == t]
                if not grp:
                    continue
                t3 = sorted(r['T3R' if k == 'DR' else 'T3L'] for r in grp)
                ys = sorted(set(r['Y'] for r in grp))
                qs = sorted(r['Q'] for r in grp)
                # Δ_R（$T^3_L=0$）：$Y$ 沿串走；Δ_L（$T^3_R=0$）：$Y\\equiv(B-L)/2$ 恒定而 $Q=T^3_L+Y$
                # 沿串走 —— 后者正是 $\\Delta^{++}\\Delta^{+}\\Delta^{0}$ 的来源。
                ladder = [t / 2 + F(-1), t / 2, t / 2 + F(1)]
                ok3 = (len(grp) == 3 and t3 == [F(-1), F(0), F(1)] and qs == ladder and
                       (ys == ladder if k == 'DR' else ys == [t / 2]))
                good &= ok3
                detail.append('%s(%s)$_{B-L=%s}$：$T^3=\\{%s\\}$, $Y=\\{%s\\}$, $Q=\\{%s\\}$%s' %
                              ('Δ_R' if k == 'DR' else 'Δ_L', nm, t,
                               ','.join(str(x) for x in t3), ','.join(str(y) for y in ys),
                               ','.join(str(q) for q in qs), '' if ok3 else ' ✗'))
    p &= ok('R5.6', '所有 $|B-L|=2$ 的色单态三重态在 Cartan 层自洽：$T^3$ 阶梯差 1、'
                   '$Q=T^3_L+T^3_R+\\tfrac{B-L}{2}$ 给出 $\\Delta^{++}\\Delta^{+}\\Delta^{0}$ 型谱',
            good and bool(detail), '；'.join(detail) or '无 $|B-L|=2$ 色单态三重态')
    occ = {}
    for nm in ('126', '126̄'):
        if nm not in NAMED:
            continue
        mp = bl_multiplets(irrep(NAMED[nm])[1])
        occ[nm] = dict((k, sorted(set(str(r['BL']) for r in mp[k]))) for k in ('DR', 'DL'))
    p &= exact('R5.7', '$126$ 与 $\\overline{126}$ **各自**同时含一个 $\\Delta_L$ 与一个 '
                       '$\\Delta_R$，区别只在 $B-L$ 的**符号**（共轭表示 = 全部 Cartan 荷反号）'
                       '⇒ "谁来破 $B-L$" 不是"有没有 $\\Delta_R$"的问题，而是取哪个符号',
               occ, {'126': {'DR': ['-2'], 'DL': ['2']},
                     '126̄': {'DR': ['2'], 'DL': ['-2']}})
    # 决定性一步：在 $|B-L|=2$ 上，"$Q=0$" 与 "是 $SU(2)_{L/R}$ 单态" 互斥
    sing, trip = [], []
    for r in TABLE:
        for g in r['bl2groups']:
            if g['kind'] == 'S':
                sing.append((r['name'], g['BL'], g['Q'], g['nq0']))
            elif g['kind'] in ('DR', 'DL'):
                trip.append((r['name'], g['kind'], g['BL'], g['nq0'] * 3 == g['n']))
    p &= ok('R5.8', '$Q=T^3_L+T^3_R+\\tfrac{B-L}{2}$ ⇒ 任何 $(1,1,1)_{\\pm2}$ 单态都有 $|Q|=1$'
                    '（**一破缺就破电磁** ⇒ $120_H$ 不能用来破 $B-L$）；反之每个 $\\Delta_{L/R}$ '
                    '三重态恰有一个 $Q=0$ 分量 ⇒ 破 $B-L$ 而保 $U(1)_{em}$ **必然**经由 '
                    '$\\Delta_L$ 或 $\\Delta_R$',
            bool(sing) and all(s[2] == ['1'] or s[2] == ['-1'] for s in sing) and
            all(s[3] == 0 for s in sing) and bool(trip) and all(t[3] for t in trip),
            '带电单态：%s；含中性分量的三重态组：%s' %
            (sing, [(t[0], t[1], t[2]) for t in trip]))
    # $|B-L|=1$ 的另一条通道：存在，但每步只带走一个单位的 $B-L$
    one = {}
    for nm in ORDER:
        if nm not in NAMED:
            continue
        ms = irrep(NAMED[nm])[1]
        one[nm] = sorted(set((str(t), r['L'], r['R']) for t in (F(1), F(-1))
                             for r in bl2_class(ms, t) if r['c1'] and r['Q'] == 0))
    got = dict((k, v) for k, v in one.items() if v)
    p &= ok('R5.9', '$|B-L|=1$ 且 $Q=0$ 的色单态在 $\\dim\\le210$ 内**只**出现在 '
                    '$16,\\overline{16}$（$(1,2,1)_{+1}\\oplus(1,1,2)_{-1}$ 型二重态）与 '
                    '$144,\\overline{144}$（$(1,2,3)/(1,3,2)$ 型）里，$10/45/54/120/126/'
                    '\\overline{126}/210$ 一个都没有 ⇒ $B-L$ 可以**单步**（$|\\Delta(B-L)|=1$）'
                    '破掉且保住 $U(1)_{em}$，最小通道是 $16_H/\\overline{16}_H$；但每步只带走'
                    '一个单位 $\\Rightarrow$ 残留 $\\mathbb{Z}_3$，而物质字称**被这一步破掉**'
                    '（旧句"残留 $Z_2$（物质字称）"由 §9 推翻，其出处是 R10.8 的归一化滑倒），'
                    '且给不出可重整的 $\\nu_R$ Majorana 质量'
                    '（那需要 $|\\Delta(B-L)|=2$），而且这些分量必是某个 $SU(2)$ 的二重态 ⇒ '
                    '单步破缺必然连带破 $SU(2)_{L/R}$',
            got == {'16': [('-1', 1, 2), ('1', 2, 1)],
                    '16̄': [('-1', 2, 1), ('1', 1, 2)],
                    '144': [('-1', 3, 2), ('1', 2, 3)]},
            '算得（表示 → $(B-L,\\ SU(2)_L$ 串长, $SU(2)_R$ 串长$)$）：%s' % got)
    return p


# =============================================== d=4 物质–Higgs Yukawa 通道（R7）
# 与 R5 的分工：R5 问"哪个 Higgs 里**有**能破 $B-L$ 的中性分量"，R7 问"哪个 Higgs 拿得到
# $16_F16_FH$ 这个算符"。两问相互独立：$\Delta_R\subset\overline{126}_H$ 同时过两关，
# $45_H$ 两关皆不过，$16_H$ 只过第一关（R5.9）。
def conj_label(cs):
    r"""Dynkin 标号的共轭标号：$w_\lambda\mapsto-w_\lambda$ 再拉回主导室。

    它对**任何**支配标号都算得出来，不需要这条标号已被登记 $\Rightarrow$ 配对和
    （`pair_singlets`）可以在 $\dim>210$ 的成分上照样闭合；按名字查表做不到这件事，
    R9.5 的第四条变异把这个差别当场量出来。
    """
    return tuple(dominant(neg(weight_of_label(cs)))[1])


def registered(cs):
    """标号是否已在 `NAMED` 里登记（零标号算登记：它就是 $(1)$）。"""
    return not any(cs) or any(tuple(NAMED[nm]) == tuple(cs) for nm in NAMED)


def name_of(cs):
    """**标号**的显示名：与 `label_name` 同一套优先级（$10$ 与 $\\overline{10}$ 同标号 ⇒ 取表内先出现的），零标号 $\\mapsto$ `'(1)'`，未登记 $\\mapsto$ 裸标号字符串。"""
    if not any(cs):
        return '(1)'
    keys = list(ORDER) + sorted(set(NAMED) - set(ORDER))
    return next((nm for nm in keys if nm in NAMED and tuple(NAMED[nm]) == tuple(cs)),
                str(list(cs)))


def conj_names(cs):
    """标号 $cs$ 的共轭表示在 `NAMED` 里登记过的**全部**名字（未认定 $\\Rightarrow$ 空表）。

    实表示会返回两个名字：$\\overline{10}$ 与 $10$ 是同一条标号（R2.c10c45），而 R2 把两个
    名字都登记进了 `NAMED` ⇒ 这里如实返回 $['10','\\overline{10}']$ 一类的对，由调用方去重。
    """
    lab = conj_label(cs)
    keys = list(ORDER) + sorted(set(NAMED) - set(ORDER))
    return [nm for nm in keys if nm in NAMED and tuple(NAMED[nm]) == lab]


_DECOMP_MEMO = {}


def decomp(ms):
    r"""把 $W$-不变多重集拆成不可约成分：解 $m_V(\lambda)=\sum_\mu n_\mu m_\mu(\lambda)$，
    $\lambda,\mu$ 跑遍 $V$ 中出现的**支配**权（成分的最高权必然作为权重出现，这是唯一的预设）。

    系数矩阵 $(m_\mu(\lambda))$ 按支配序是单位三角阵的行列同置换 $\Rightarrow$ 行列式 $\pm1$、
    精确可逆；解出来若有负数或非整数即判失败。**最后用整权重构对账**：拆出来的成分加回去
    必须逐权重等于原多重集。与 R3 的"先剥已知成分再 `find`"是不同代码路径。
    返回 $\{$最高权格点: 重数$\}$；任何一环不成立 $\Rightarrow$ None（调用方必须显式降级）。

    按**多重集内容**记忆：R8 与 R9 共用同一批大乘积（$16^{\otimes4}$ 拆一次 1s 量级），
    不记忆会把同一个方程组解两遍。本函数不读 `NAMED`（只用到 `irrep`/`dynkin`）$\Rightarrow$
    键里不需要登记状态；返回的字典按**只读**约定使用（4 个调用点都只读）。
    """
    key = frozenset(ms.items())
    if key not in _DECOMP_MEMO:
        _DECOMP_MEMO[key] = _decomp_once(ms)
    return _DECOMP_MEMO[key]


def _decomp_once(ms):
    dom = sorted(set(w for w in ms if all(c >= 0 for c in dynkin(w))))
    if not dom:
        return None
    try:
        n = _solve([[F(irrep(dynkin(mu))[1].get(la, 0)) for mu in dom] for la in dom],
                   [F(ms[la]) for la in dom])
    except AssertionError:
        return None
    if any(x < 0 or x.denominator != 1 for x in n):
        return None
    out = dict((la, int(x)) for la, x in zip(dom, n) if x)
    got = {}
    for la, k in out.items():
        got = madd(got, *([irrep(dynkin(la))[1]] * k))
    return got == dict(ms) and out or None


def label_name(lam):
    """Dynkin 标号在表内的名字：零标号 $\\mapsto$ `'(1)'`；未认定 $\\mapsto$ 裸标号（**不静默丢**）。"""
    lab = list(dynkin(lam))
    if not any(lab):
        return '(1)'
    keys = list(ORDER) + sorted(set(NAMED) - set(ORDER))
    return next((nm for nm in keys if nm in NAMED and list(NAMED[nm]) == lab), lab)


def yukawa_products():
    r"""$16_F$ 的双线性三种乘积（$W$-不变多重集）。"""
    W16 = irrep(NAMED['16'])[1]
    out = {'sym': sym2(W16), 'anti': wedge2(W16)}
    if '16̄' in NAMED:
        out['vec'] = tprod(W16, irrep(NAMED['16̄'])[1])
    return out


def yukawa_channels(constituents=None):
    r"""$16_F16_FH$ 在 d=4 允许的 Higgs 名（按对称类型分栏）+ 成分清单。

    `constituents=None` ⇒ 现场把三个乘积拆成不可约成分，再取**共轭**（不变张量要求
    $H^*\subset16\otimes16$）。传入显式成分名清单只服务于变异测试：证明"允许的表示"
    是共轭映射算出来的，不是写死在函数里的字符串。
    """
    prods = yukawa_products()
    parts, out = {}, {}
    for key in ('sym', 'anti', 'vec'):
        if key not in prods:
            parts[key], out[key] = None, []
            continue
        if constituents is not None:
            got = [(nm, 1) for nm in constituents.get(key, [])]
        else:
            d = decomp(prods[key])
            if d is None:
                parts[key], out[key] = None, []
                continue
            got = [(label_name(la), k) for la, k in sorted(d.items())]
        parts[key] = got
        names = []
        for nm, _k in got:
            if nm == '(1)':                       # 单态不是 Higgs 候选（不携物质荷）
                continue
            names += conj_names(NAMED[nm])[:1] if nm in NAMED else [nm]   # 实表示取先注册名
        out[key] = sorted(set(names), key=lambda x: (list(ORDER).index(x)
                                                     if x in ORDER else 99, x))
    return out, parts


def matter_singlet(W16=None):
    """$16_F$ 里"色单态 + $SU(2)_L$ 单态 + $Q=0$"的权重表 $=\\nu_R^c$ 所在的权重。

    判据刻意用 $SU(2)_L$ 串长 1 而非 $SU(2)_R$：$\\nu_R^c$ 在 $3221$ 下是 $(1,1,2)_{-1}$
    的成员，它在 $SU(2)_R$ 侧**不是**单态（$Q=0$ 靠 $T^3_R$ 与 $B-L$ 相消）。
    """
    ms = irrep(NAMED['16'])[1] if W16 is None else W16
    return [w for w in sorted(ms)
            if color_singlet_wt(ms, w) and string_len(ms, w, A1_L) == 1
            and chg(w, QHP) == F(0) and chg(w, YHP) == F(0)]


def realizable(W, sums=None):
    r""""权重可加性"计数：$W$ 里有多少个**不同权重**的相反数落在给定的双线性支集 `sums` 里。

    `sums` 默认 $16+16$ 的支集；对消通道要传 $16-16$ 的支集（见 R7.6：两套支集不能混用）。
    这是耦合的**必要条件**（不变张量至少要荷守恒），不是充分条件 ⇒ 只用来做
    双向咬合检查，判据仍以 `yukawa_channels` 的张量分解为准。
    """
    ms = irrep(NAMED['16'])[1]
    if sums is None:
        sums = set(add(a, b) for a in ms for b in ms)
    return len([w for w in W if neg(w) in sums]), len(sums)


def need_weight():
    """$\\nu_R^c\\nu_R^c$ 这个双线性所要求的 Higgs 权重 $=-2\\nu$（$\\nu$ = 上条的唯一权重）。"""
    nu = matter_singlet()
    return smul(-2, nu[0]) if nu else None


YUK = []
YUKCH = {}                                        # 供报告 §6 取用（与门禁同源，不另算一遍）


def run_yukawa_layer():
    """R7：d=4 允许的 Higgs 表示 + $\\nu_R$ Majorana 算符的荷守恒面。"""
    p = True
    prods = yukawa_products()
    allow, parts = yukawa_channels()
    rebuilt, unknown = {}, []
    for key in ('sym', 'anti', 'vec'):
        got = parts.get(key)
        if not got:
            rebuilt[key] = False
            continue
        ms = {}
        for nm, k in got:
            if nm != '(1)' and nm not in NAMED:
                unknown.append((key, nm))
            ms = madd(ms, *([irrep(ZERO if nm == '(1)' else NAMED[nm])[1]] * k))
        rebuilt[key] = (ms == dict(prods[key]))
    p &= ok('R7.1', '$\\mathrm{Sym}^2(16)$、$\\wedge^2(16)$、$16\\otimes\\overline{16}$ 三乘积'
                    '各被**精确**拆成不可约成分：在出现的支配权上解单位三角方程组 '
                    '$m_V(\\lambda)=\\sum_\\mu n_\\mu m_\\mu(\\lambda)$，解须为非负整数，'
                    '且**按整权重构回去必须逐权重等于原多重集**（本门禁自己重算一遍重构，'
                    '不信 `decomp` 的返回值）；拆出的成分全部落在 R2/R3 已登记的标号里 $\\Rightarrow$ '
                    '与本文件"剥已知成分再交给 `find`"那条**不同的代码路径**给出同一批表示',
            all(rebuilt.values()) and not unknown,
            '成分清单（通道 → 表示:重数）：%s；未登记的名字：%s；重构比对：%s' %
            (parts, unknown, rebuilt))
    tbl = dict((r['name'], r) for r in TABLE)
    # 两条"权重可加性"检验各自用**自己通道的支集**：手征通道来自 $16+16$，对消通道来自
    # $16+\\overline{16}=16-16$（$W(\\overline{16})=-W(16)$）。混用会得出假矛盾——
    # $45_H/210_H$ 在 $16+16$ 支集里得分 0，在 $16-16$ 支集里应得满分。
    ms16 = irrep(NAMED['16'])[1]
    sums_cc = set(add(a, b) for a in ms16 for b in ms16)
    sums_cf = set(add(a, neg(b)) for a in ms16 for b in ms16)
    rows = []
    for nm in ORDER:
        if nm not in NAMED or nm not in tbl:
            continue
        Wn = irrep(NAMED[nm])[1]
        rows.append({'name': nm, 'dim': tbl[nm]['dim'], 'real': tbl[nm]['real'],
                     'chiral': ('sym' if nm in allow['sym'] else '') +
                               ('anti' if nm in allow['anti'] else ''),
                     'sym': nm in allow['sym'], 'anti': nm in allow['anti'],
                     'vec': nm in allow['vec'], 'realizable': realizable(Wn, sums_cc)[0],
                     'realizableD': realizable(Wn, sums_cf)[0], 'nweights': len(Wn),
                     'holds_maj': need_weight() in Wn})
    YUK[:] = rows
    chiral = [r['name'] for r in rows if r['sym'] or r['anti']]
    # 按**标号**去重后再挑"可加性过关但通道表不受理"的表示：10 与 10̄ 是同一条标号（实表示），
    # 若按名字挑，实表示的第二个名字会冒充成一个反例（按标号挑目前只剩 126 一条）。
    labof = dict((nm, tuple(NAMED[nm])) for nm in NAMED)
    chiral_labs = set(labof[n] for n in allow['sym'] + allow['anti'] if n in labof)
    extra = [(r['name'], r['realizable'], r['nweights']) for r in rows
             if r['realizable'] and labof.get(r['name']) not in chiral_labs]
    def real_of(r):
        """按**自己的通道**取可加性得分：手征行看 $16+16$ 支集，对消行看 $16-16$ 支集。"""
        return r['realizable'] if (r['sym'] or r['anti']) else r['realizableD']
    must0 = [(r['name'], real_of(r)) for r in rows
             if (r['sym'] or r['anti'] or r['vec']) and not real_of(r)]
    YUKCH.update({'allow': allow, 'parts': parts, 'rebuilt': rebuilt, 'chiral': chiral,
                  'extra': extra, 'must0': must0,
                  'ntot': len(sums_cc), 'ntotD': len(sums_cf)})
    p &= exact('R7.2', '手征物质 $16_F$ 的双线性通道（$16\\otimes16$ 的共轭成分）与向量型通道'
                       '（$16\\otimes\\overline{16}$）**互不相交** ⇒ 一个 Higgs 想同时给'
                       'Dirac 质量与破 $B-L$，必须选在两个通道都没有的表示里，那它谁都不耦合',
               sorted(set(chiral) & set(allow['vec'])), [],
               '手征通道：%s（对称 %s／反对称 %s）；向量型通道：%s' %
               (chiral, allow['sym'], allow['anti'], allow['vec']))
    nu = matter_singlet()
    p &= exact('R7.3', '$16_F$ 里"色单态 + $SU(2)_L$ 单态 + $Y=0,Q=0$"的权重**恰好一个** '
                       '$\\Rightarrow$ 右手中微子（$\\nu_R^c$）在每一代里唯一，'
                       '不是多加一个字段的选择',
               len(nu), 1, '其荷：$B-L=%s$，$T^3_R=%s$（$B-L$ 只挂在色槽上 ⇒ 与 $SU(2)_R$ 无冲突）'
               % ((str(chg(nu[0], BL)), str(chg(nu[0], T3R))) if nu else '无'))

    needw = need_weight()
    maj = [r['name'] for r in rows if r['holds_maj']]
    blnu = chg(nu[0], BL) if nu else None
    blneed = chg(needw, BL) if needw else None
    blsum = 2 * blnu + blneed if (blnu is not None and blneed is not None) else None
    YUKCH.update({'nu': nu, 'needw': needw, 'maj': maj,
                  'blnu': blnu, 'blneed': blneed, 'blsum': blsum})
    p &= exact('R7.4', '两个 $\\nu_R^c$ 配成 Majorana 项时，Higgs 必须携带权重 '
                       '$-2\\nu$（$\\nu$ = 上条那个唯一权重）；在 $\\dim\\le210$ 的 %d 个表示里'
                       '它**只**落在一个表示中，且那个表示属于通道表判给"对称手征通道"的成员 '
                       '$\\Rightarrow$ "能耦合到手征物质"与"携带所需权重"两条独立判据的交集非空且唯一'
                       % len(rows),
               [len(maj), (maj[0] in allow['sym']) if len(maj) == 1 else None], [1, True],
               '需要权重 $-2\\nu=%s$，其 $B-L=%s$、$Q=%s$；对称通道：%s；唯一承载者：%s' %
               (fmt(needw), chg(needw, BL), chg(needw, QHP), allow['sym'], maj))
    good, detail = True, []
    for nm in maj:
        mp = bl_multiplets(irrep(NAMED[nm])[1])
        grp = [r for r in mp['DR'] if r['w'] == needw]
        q0 = [r for r in mp['DR'] if r['Q'] == F(0)]
        good &= (len(grp) == 1 and len(q0) == 1 and q0[0]['w'] == needw
                 and grp[0]['L'] == 1 and grp[0]['R'] == 3 and grp[0]['BL'] == blneed
                 and blsum == F(0))
        detail.append('%s 的 $\\Delta_R$ 里 $-2\\nu$ 是该三重态**唯一**的 $Q=0$ 成员：%s' %
                      (tex_name(nm), bool(grp and q0 and q0[0]['w'] == needw)))
    p &= ok('R7.5', '$\\nu_R^c\\nu_R^c$ 所需的那个 Higgs 权重，恰好就是同一个表示里 '
                    '$\\Delta_R$ 三重态的**中性成员**，且该分量的 $B-L$ 恰为 $-2\\nu$ $\\Rightarrow$ '
                    '"给 $\\nu_R$ 质量"与"破 $B-L$"是**同一次取期望值**；$B-L$ 守恒由现场荷值核算：'
                    '$2\\times(%s)+(%s)=%s$（不是写死的 $-1/+2$）' % (blnu, blneed, blsum),
            good and bool(detail), '；'.join(detail) or '无承载者')
    p &= ok('R7.6', '荷守恒是**单向**必要条件，两个方向同时检查（可加性一律按**自己通道的'
                    '支集**算：手征行用 $16+16$，对消行用 $16-16$）：'
                    '(a) 通道表受理的表示里不允许出现"可加性 $=0$"（真出现就说明张量分解与'
                    '荷守恒直接矛盾）；'
                    '(b) 必须**存在**"可加性 $>0$ 而通道表不受理"的表示——按标号去重后现场列出'
                    '（备注）$\\Rightarrow$ 只看权重相加会把它误判成合法的 Higgs，'
                    '所以判据必须是张量分解而不是荷守恒',
            not must0 and bool(extra),
            '可加性过关但通道表不受理（表示, 可加权重数, 不同权重总数）：%s；'
            '通道表内可加性为 0 的：%s' % (extra, must0))
    if chain is None:
        p &= ok('R7.7', '链探针未载入 ⇒ 本层不下"情形 B 的标量与物质无耦合"的结论',
                False, 'chain is None')
        return p
    phi = [to_grid_dir(w, '$\\Phi$') for w in chain.BIDOUBLET]
    sig = [to_grid_dir(w, '$\\Sigma$') for w in chain.SIGMA_R]
    W10, W45 = irrep(NAMED['10'])[1], irrep(NAMED['45'])[1]
    Wn = dict((nm, irrep(NAMED[nm])[1]) for nm in NAMED)
    f3 = [to_grid_dir(w, '物质') for w in chain.F3]
    prose = ' '.join(chain.SCENARIOS.get(k, '') for k in chain.SCENARIOS)
    p &= ok('R7.7', '与链探针**活对账**（权重从 `chain.BIDOUBLET/SIGMA_R/F3/SCENARIOS` 现场读，'
                    '不抄本文件的字面量）：$\\Phi(1,2,2)$ 的 4 个权重全在 $10$ 里而不在 $45$ 里、'
                    '$\\Sigma(1,1,3)_0$ 的 3 个权重全在 $45$ 里而不在 $10/120/126/\\overline{126}$ '
                    '里、物质恰为 $3\\times16$（无 $\\overline{16}\\Rightarrow$ 向量型通道空转），'
                    '且链的情形文字确实写着 $10_H,45_H$ 并声明"无 $126_H$"',
            all(w in W10 for w in phi) and not any(w in W45 for w in phi)
            and all(w in W45 for w in sig)
            and not any(w in Wn[n] for w in sig for n in ('10', '120', '126', '126̄'))
            and sorted(f3) == sorted(list(irrep(NAMED['16'])[1]) * 3)
            and '10_H' in prose and '45_H' in prose and '无 $126_H$' in prose,
            '$\\Phi$：%s；$\\Sigma$：%s；物质 $=3\\times16$：%s' %
            ([fmt(w) for w in phi], [fmt(w) for w in sig],
             sorted(f3) == sorted(list(Wn['16']) * 3)))
    p &= ok('R7.8', '变异测试：把成分清单植成 $16$（真实计算里 $16\\notin16\\otimes16$）$\\Rightarrow$ '
                    '允许集必须变成 $\\overline{16}$ 而不是原来那批名字（证明共轭映射真的在跑，'
                    '不是把结论写死在函数里）',
            yukawa_channels(constituents={'sym': ['16'], 'anti': [], 'vec': []})[0]['sym']
            == conj_names(NAMED['16'])[:1]
            and yukawa_channels(constituents={'sym': ['16'], 'anti': [], 'vec': []})[0]['sym']
            != allow['sym'],
            '植入后的对称通道：%s（真实：%s）' %
            (conj_names(NAMED['16'])[:1], allow['sym']))
    ms16 = irrep(NAMED['16'])[1]
    alt = [w for w in sorted(ms16) if color_singlet_wt(ms16, w)
           and string_len(ms16, w, A1_L) == 1 and chg(w, QHP) != F(0)]
    okalt = bool(alt) and neg(smul(2, alt[0])) in Wn['126̄'] and need_weight() != neg(smul(2, alt[0]))
    p &= ok('R7.9', '变异测试：改用同一条 $SU(2)_R$ 串里的**带电**伙伴（$Q=\\pm1$）作双线性的'
                    '两个因子 $\\Rightarrow$ 所需权重落到 $\\Delta_R$ 的**双重带电**分量上，'
                    '不再是中性那一个 ⇒ "$Q=0$ 才允许取期望值"这条物理输入确实在起决定作用，'
                    '而不是一个恒真的说法',
            okalt,
            '带电伙伴 $w=%s$（$Q=%s$）$\\Rightarrow$ 所需权重 %s，其 $Q=%s$；中性承载者仍是 %s' %
            (fmt(alt[0]) if alt else '—',
             str(chg(alt[0], QHP)) if alt else '—',
             fmt(neg(smul(2, alt[0]))) if alt else '—',
             str(chg(neg(smul(2, alt[0])), QHP)) if alt else '—', fmt(needw)))
    return p


# =============================================== 不变张量簿记（R8）
# 与 R7 的分工：R7 判"哪个 Higgs 拿得到 d=4 算符"，材料是**双线性乘积的成分 + 共轭**；
# R8 换一条不共享代码的路：直接数 $\\mathrm{mult}((1),V)$，并要求它把 R7 的通道表**复算**成
# 同一张。本层的骨架是把两件容易混为一谈的事分开记账：
#   * **荷账本** $=\\dim V_0=m_V(0)$：全部 Cartan 荷同时为零的方向数（"荷配得平"）；
#   * **不变张量** $=\\mathrm{mult}((1),V)$：其中真正规范不变的那一部分。
# 恒有 $\\mathrm{mult}((1),V)\\le\\dim V_0$，而 $16\\otimes\\overline{16}$ 上是 $1\\ll16$：差的
# 15 个方向正是 $45/210$ 的 Cartan 子空间 $\\Rightarrow$ "荷为零"与"不变"之间的缺口可以**逐成分
# 拆开核对**，这就是 R8.1a 的内容。
DIMPRODUCT_CAP = 2000          # δ 判据的对枚举上限：纯**成本**取舍，不是物理假设


def zero_wt(ms):
    """荷账本：权重多重集里零权的**重数** $m_V(0)$（全部 Cartan 荷同时为零的子空间维数）。"""
    return int(ms.get(ZERO, 0))


_SINGLET_MEMO = {}


def singlet_mult(ms):
    r"""不变张量个数 $\mathrm{mult}((1),V)$：走 `decomp`（整权重构对账在它里面）。

    拆不成特征标的非负整组合 $\Rightarrow$ None，**不静默当成 0** $\Rightarrow$ 调用方必须显式
    降级（R8.6 的第二个植入正是来检查这条守卫不是死代码）。
    按**多重集内容**记忆：四重积的一次 `decomp` 要 0.8s，本层多个门禁共用同一批乘积，
    不记忆会把同一个分解解七遍。
    """
    key = frozenset(ms.items())
    if key not in _SINGLET_MEMO:
        d = decomp(ms)
        _SINGLET_MEMO[key] = None if d is None else int(d.get(ZERO, 0))
    return _SINGLET_MEMO[key]


def constituents(ms):
    """权重多重集 $\\to$ 成分表 [(名字, 重数)]；未认定的支配权留成裸标号（**不静默丢**）。"""
    d = decomp(ms)
    return None if d is None else [(label_name(la), k) for la, k in sorted(d.items())]


def constit(ms):
    r"""成分表（**按标号**）：$[(\lambda,\ n_\lambda)]$，未登记的支配权保留其 Dynkin 标号。

    与 `constituents` 的差别不是风格而是**视力**：登记表只覆盖 $\dim\le210$，按名字查共轭
    会在登记范围外把真实存在的伙伴静默算成 0 $\Rightarrow$ 两条路径在含未登记成分的乘积上
    给出**不同**的数（差多少由 R9.5 第四条当场量出来，不写在这里）。`pair_singlets` 走标号路径。
    """
    d = decomp(ms)
    return None if d is None else [(tuple(dynkin(la)), k) for la, k in sorted(d.items())]


def conj_name_set(nm):
    """成分名 $\\mapsto$ 其共轭表示已登记的名字集：单态自配；实表示给两个名字；未登记 $\\Rightarrow$ 空集。"""
    if nm == '(1)':
        return {'(1)'}
    if not isinstance(nm, str) or nm not in NAMED:
        return set()
    return set(conj_names(NAMED[nm]))


def pair_singlets(pa, pb):
    r"""第二条**独立**路径：$\mathrm{mult}((1),A\otimes B)=\sum_{R,S}n_Rm_S\\,\delta_{S,\bar R}$，
    只查两个因子各自已有的成分表 $\Rightarrow$ 不解大乘积的方程组。

    `pa`/`pb` 是 `constit` 给出的**标号**表，$\bar R$ 由 `conj_label` 算：共轭是标号之间的
    运算、与登记无关 $\Rightarrow$ 成分落在 $\dim>210$ 的登记范围外时这条路径照样闭合
    （按名字查表做不到，R9.5 第三条量出两者差多少）。
    返回 $(\text{计数},\\ \text{登记范围外的标号})$：后者**不**影响计数 $\Rightarrow$ 它不是
    "配不上对"而是"没名字"，报告仍要点名，因为本层正是在登记表之外读数。
    """
    tot = 0
    for la, k in pa:
        lb = conj_label(la)
        tot += k * sum(m for l2, m in pb if l2 == lb)
    return tot, [(name_of(la), k) for la, k in list(pa) + list(pb) if not registered(la)]


def ledger_split(ms):
    r"""把零权空间按成分拆开：每个不可约成分贡献 $n_R\\,m_R(0)$ 个"荷为零但未必不变"的方向。

    返回 $\\{$parts: [(名字, 该成分贡献的零权数, 重数)], unreg: 未登记标号贡献的零权数,
    nlab: 未登记标号的条数, total: 拆开后的总数$\\}$；`decomp` 失败 $\Rightarrow$ None。
    `total` 必须等于 `zero_wt(ms)`
    ——这是 $m_{A\otimes B}=\sum n_Rm_R$ 在 $\mu=0$ 处的恒等式，R8.1a 拿它当门禁。
    """
    d = decomp(ms)
    if d is None:
        return None
    parts, unreg, total, nlab = [], 0, 0, 0
    for la, k in sorted(d.items()):
        z = irrep(dynkin(la))[1].get(ZERO, 0) * k
        nm = label_name(la)
        if isinstance(nm, str):
            parts.append((nm, z, k))
        else:
            unreg += z
            nlab += 1
        total += z
    parts.sort(key=lambda r: (-r[1], r[0]))
    return {'parts': parts, 'unreg': unreg, 'nlab': nlab, 'total': total}


INV = {}                        # 供报告 §7 取用（与门禁同源，不在报告里另算一遍）


def run_invariant_layer():
    """R8：荷账本与不变张量分开算，再用配对和复算同一个数，最后独立复算 d=4 通道表。"""
    p = True
    W = dict((nm, irrep(NAMED[nm])[1]) for nm in NAMED)
    lab = dict((nm, tuple(NAMED[nm])) for nm in NAMED)

    def conjlab(nm):
        return tuple(dominant(neg(weight_of_label(lab[nm])))[1])

    def bylabel(names):
        return sorted(set(lab[n] for n in names))

    # ---- R8.0 基本定理：mult((1),A\otimes B)=\delta_{B,\bar A}，在全部"小对"上现场核验
    small = [(a, b) for a in ORDER if a in lab for b in ORDER if b in lab
             and irrep(lab[a])[2] * irrep(lab[b])[2] <= DIMPRODUCT_CAP]
    wrong, ones = [], 0
    for a, b in small:
        s = singlet_mult(tprod(W[a], W[b]))
        want = int(conjlab(a) == lab[b])
        ones += want
        if s != want:
            wrong.append((a, b, s, want))
    p &= ok('R8.0', '不变张量基本定理 $\\mathrm{mult}((1),A\\otimes B)=\\delta_{B,\\bar A}$ 在 '
                    '$\\dim A\\cdot\\dim B\\le%d$ 的**全部** %d 个已登记表示对上现场成立：左边由 '
                    '`decomp` 解单位三角方程组算出，右边由共轭标号算出，**两边不共享代码** '
                    '$\\Rightarrow$ 后面配对和那条路（R8.2）用的查表规则不是引用而是当场验证过的'
                    % (DIMPRODUCT_CAP, len(small)),
            bool(small) and not wrong and 0 < ones < len(small),
            '对数 %d（其中 $\\delta=1$ 的 %d 对：互为共轭的那些）；反例：%s' %
            (len(small), ones, wrong or '无'))

    cc, cb2 = tprod(W['16'], W['16']), tprod(W['16̄'], W['16̄'])
    cf = tprod(W['16'], W['16̄'])
    p4, f4 = tprod(cc, cc), tprod(cf, cf)          # 16^4 与 16²16̄²（结合方式 II）
    f4alt = tprod(cc, cb2)                         # 同一乘积（结合方式 I）

    # ---- R8.1 / R8.1a 荷账本 vs 不变张量：三个乘积的读数 + 逐成分拆开必须回到同一个数
    led = []
    for tag, ms in (('$16\\otimes16$', cc), ('$16\\otimes\\overline{16}$', cf),
                    ('$16^{\\otimes4}$', p4)):
        sp = ledger_split(ms)
        led.append({'tex': tag, 'dim': msum(ms), 'ndist': len(ms), 'zero': zero_wt(ms),
                    'singlet': singlet_mult(ms),
                    'split': sp and (sp['total'] == zero_wt(ms)), 'parts': sp})
    p &= exact('R8.1', '三个乘积的（荷账本 $\\dim V_0$，不变张量 $\\mathrm{mult}((1),V)$）读数：'
                       '$16\\otimes16$ 连**荷**都配不平（零权 0 个）$\\Rightarrow$ 手征双线性没有'
                       '任何荷守恒方向；$16\\otimes\\overline{16}$ 有 16 个零权方向但只有 1 个不变；'
                       '$16^{\\otimes4}$ 有 960 个零权方向、其中 2 个不变 $\\Rightarrow$ '
                       '"荷配平"与"规范不变"是两个数，本表把它们并排放',
               [(x['zero'], x['singlet']) for x in led], [(0, 0), (16, 1), (960, 2)],
               '缺口（零权 $-$ 单态）：%s' %
               '、'.join('%s 缺 %d' % (x['tex'], x['zero'] - x['singlet']) for x in led))
    p &= ok('R8.1a', '零权空间按成分拆开必须**逐成分回到同一个数**：$m_{A\\otimes B}(0)='
                     '\\sum_R n_Rm_R(0)$（每个不可约成分贡献它自己的零权重数）。这条恒等式一'
                     '方面证明"缺口"不是丢失而是记在 $45/210$ 等成分的 Cartan 子空间上，'
                     '另一方面把 `decomp` 的重构对账在 $\\mu=0$ 这个槽位上再核一遍',
            all(x['split'] for x in led) and
            all(x['singlet'] is not None and x['singlet'] <= x['zero'] for x in led) and
            any(x['zero'] - x['singlet'] > 0 for x in led),
            '拆解：' + '；'.join('%s 的零权按成分归口 %s%s' %
                                 (x['tex'],
                                  '、'.join('%s 占 %d' % (tex_name(n), z)
                                            for n, z, _k in x['parts']['parts']),
                                  '' if not x['parts']['unreg']
                                  else '，另有未登记标号占 %d' % x['parts']['unreg'])
                                 for x in led if x['parts'])
            + '；三条都满足"单态 $\\le$ 零权"且至少一处严格')

    # ---- R8.2 四路对账 + 结合律：同一个四重积，两条解方程的路径 + 两条配对和的路径
    r_decomp_I, r_decomp_II = singlet_mult(f4alt), singlet_mult(f4)
    r_pair_cc, unk1 = pair_singlets(constit(cc), constit(cb2))
    r_pair_cf, unk2 = pair_singlets(constit(cf), constit(cf))
    r_pair_p4, unk3 = pair_singlets(constit(cc), constit(cc))
    p &= ok('R8.2', '$16\\otimes16\\otimes\\overline{16}\\otimes\\overline{16}$：两种结合方式'
                    '先给出**逐权重相同**的多重集（张量积结合律在这里是可核对的，不是默认成立的），'
                    '再由两条独立路径给出同一个单态个数：`decomp` 解方程（两种方式各一次）与'
                    '配对和 $\\sum n_Rm_{\\bar R}$（按 $16\\otimes16$ 配对、按 $16\\otimes\\overline{16}$ '
                    '配对各一次）$\\Rightarrow$ 四条路径同为 3；同样四条路径里 $16^{\\otimes4}$ 的'
                    '两条路径同为 2，且**共轭在这一步真的在起作用**：把 $\\overline{16}$ 全换成 $16$ '
            '后配对和从 3 掉到 2（$126$ 找不到 $\\overline{126}$ 作伙伴）$\\Rightarrow$ '
            '配对和按**标号**取共轭（`constit`），不查登记表 $\\Rightarrow$ 这三张表恰好全在 '
            '$\\dim\\le210$ 内，故与按名字查表给出同一个数（R9.5 第三条核这条，并给出超出登记'
            '表时两者差多少）',
            f4alt == f4 and r_decomp_I == r_decomp_II == r_pair_cc == r_pair_cf == 3
            and r_pair_p4 == singlet_mult(p4) == 2 and not (unk1 or unk2 or unk3),
            '四条路径（decomp I/II、配对和 $16\\otimes16$ 侧、配对和 $16\\otimes\\overline{16}$ 侧）'
            '= %s；$16^{\\otimes4}$：decomp %d、配对和 %d；两种结合方式的权重多重集逐权相等：%s；'
            '登记范围外的标号：%s' %
            ([r_decomp_I, r_decomp_II, r_pair_cc, r_pair_cf], singlet_mult(p4), r_pair_p4,
             f4alt == f4, (unk1 + unk2 + unk3) or '无'))

    # ---- R8.3 通道表由单态计数独立复算（不查 R7 的成分表，只数三重积里的 (1)）
    prods = {'sym': sym2(W['16']), 'anti': wedge2(W['16']), 'vec': cf}
    chan = {}
    for key, base in prods.items():
        names = [nm for nm in sorted(lab) if (singlet_mult(tprod(base, W[nm])) or 0) > 0]
        chan[key] = {'names': names, 'labs': bylabel(names),
                     'agree': bool(YUKCH.get('allow')) and
                                bylabel(names) == bylabel(YUKCH['allow'][key])}
    dis = [k for k in prods if not chan[k]['agree']]
    p &= ok('R8.3', 'd=4 通道表**独立复算**：不去拆双线性再取共轭，而是逐个 Higgs 候选数 '
                    '$\\mathrm{mult}((1),\\mathrm{Sym}^2 16\\otimes H)$、'
                    '$\\mathrm{mult}((1),\\wedge^2 16\\otimes H)$、'
                    '$\\mathrm{mult}((1),16\\otimes\\overline{16}\\otimes H)$ 是否 $>0$。'
                    '两条路径按**标号**比对（实表示 $10$ 与 $\\overline{10}$ 同标号、$45$ 与 '
                    '$\\overline{45}$ 同标号 $\\Rightarrow$ 按名字比会假报错，R2.c10c45）'
                    '$\\Rightarrow$ §6 的通道表由第二条不共享代码的路径确认',
            not dis,
            '按标号不一致的通道：%s；本层数出的 Higgs（对称 %s／反对称 %s／对消 %s）'
            '；R7 的通道表（对称 %s／反对称 %s／对消 %s）' %
            (dis or '无',
             '、'.join(tex_name(n) for n in chan['sym']['names']),
             '、'.join(tex_name(n) for n in chan['anti']['names']),
             '、'.join(tex_name(n) for n in chan['vec']['names']),
             '、'.join(tex_name(n) for n in YUKCH['allow']['sym']),
             '、'.join(tex_name(n) for n in YUKCH['allow']['anti']),
             '、'.join(tex_name(n) for n in YUKCH['allow']['vec'])))

    # ---- R8.4 手征 => 无裸质量项
    p &= exact('R8.4', '手征物质的双线性里**没有**规范不变方向：$\\mathrm{mult}((1),16\\otimes16)='
                       '0$、$\\mathrm{mult}((1),\\mathrm{Sym}^2 16)=0$、'
                       '$\\mathrm{mult}((1),\\wedge^2 16)=0$，而'
                       '$\\mathrm{mult}((1),16\\otimes\\overline{16})=1$ $\\Rightarrow$ '
                       '"手征 $\\Rightarrow$ 质量项必须靠 Higgs"是**数出来的**，不依赖 §6 的通道表；'
                       '向量型的一对（$16$ 与 $\\overline{16}$ 同时在场）则有一个不变方向',
               [singlet_mult(cc), singlet_mult(prods['sym']), singlet_mult(prods['anti']),
                singlet_mult(cf)], [0, 0, 0, 1],
               '对称／反对称两个槽各自也是 0 $\\Rightarrow$ 不是"单态藏在反对称槽里"那种假象')

    # ---- R8.5 物质-only 的不变算符自动 Delta(B-L)=0；Delta(B-L)=2 必须插入带共轭杠的 Higgs
    triv = irrep(ZERO)
    charges = [chg(ZERO, v) for v in (BL, T3L, T3R, YHP, QHP)] if chain is not None else None
    sp4 = singlet_mult(p4)
    tri = dict((nm, singlet_mult(tprod(cc, W[nm]))) for nm in
               ('10', '120', '126', '126̄', '45'))
    p &= ok('R8.5', '$|\\Delta(B-L)|=2$ 那一类**不可能**只用物质凑出来：'
                    '(i) 单态 $(1)$ 的权重集恰为 $\\{(0,0,0,0,0):1\\}$ 且它在各 Cartan 方向上的荷'
                    '全为 0 $\\Rightarrow$ 任何物质-only 不变算符自动 $\\Delta(B-L)=0$；'
                    '(ii) $\\mathrm{mult}((1),16^{\\otimes4})=%d>0$ 而 '
                    '$\\mathrm{mult}((1),16\\otimes16)=0$ $\\Rightarrow$ 规范群**不**禁止'
                    '四费米子不变算符（质子衰变那一类的荷前提成立），却禁止二费米子的那一类；'
                    '(iii) 要拿到 $|B-L|=2$ 必须插入 Higgs，而 '
                    '$\\mathrm{mult}((1),16\\otimes16\\otimes H)$ 在 $H=\\overline{126}$ 上为 1、'
                    '在 $H=126$ 上为 0 $\\Rightarrow$ 插入的是**带共轭杠**的那个，'
                    '与 R7.4/R7.5 的 Majorana 承载者判定同源而**路径独立**' % sp4,
            triv[1] == {ZERO: 1} and (charges is None or all(c == F(0) for c in charges))
            and sp4 == 2 and singlet_mult(cc) == 0
            and tri['126̄'] == 1 and tri['126'] == 0,
            '$(1)$ 的权重集只有零权（%s）；它在 $B-L$、$T^3_L$、$T^3_R$、$Y$、$Q$ 五个方向上的荷 '
            '$=%s$；$16^{\\otimes4}$ 单态 %d 个；在 $16\\otimes16\\otimes H$ 里的单态数：%s' %
            ('零权 1 个' if triv[1] == {ZERO: 1} else triv[1],
             '、'.join(str(c) for c in charges) if charges else '（链探针未载入）', sp4,
             '、'.join('%s 上 %s 个' % (tex_name(n), tri[n]) for n in
                      ('10', '120', '126', '126̄', '45'))))

    # ---- R8.6 变异测试：证明上面的单态个数跟着输入走，而不是写死的字面量
    minus1, minus2 = dict(cf), dict(cf)
    minus1[ZERO] -= 1
    minus2[ZERO] -= 2
    p &= ok('R8.6', '变异测试（三处植入）$16\\otimes\\overline{16}=1\\oplus45\\oplus210$ 的'
                    '零权空间被动过之后，读数必须跟着动：去掉 **1** 个零权 $\\Rightarrow$ 它'
                    '合法地变成 $45\\oplus210$（那正是 $m(0)=15$ 的答案），单态由 1 变 0；'
                    '去掉 **2** 个零权 $\\Rightarrow$ 不再是任何特征标的非负整组合，'
                    '**整权重构对账必须拒绝**（返回 None，而不是沿用旧的 1）；'
                    '把 $\\overline{16}$ 换成 $16$ $\\Rightarrow$ 单态由 1 变 0。'
                    '三条合起来说明 `singlet_mult` 既不是恒真也不是恒假，且它的失败分支活着',
            singlet_mult(minus1) == 0 and singlet_mult(minus2) is None
            and singlet_mult(cc) == 0 and singlet_mult(cf) == 1,
            '植入读数：去 1 个零权 $\\to$ %s；去 2 个 $\\to$ %s；$16\\otimes16\\to$ %s；'
            '真值 $16\\otimes\\overline{16}\\to$ %s' %
            (singlet_mult(minus1), singlet_mult(minus2), singlet_mult(cc), singlet_mult(cf)))

    INV.update({'npairs': len(small), 'ones': ones, 'wrong': wrong, 'ledger': led,
                'mut': {'m1': singlet_mult(minus1), 'm2': singlet_mult(minus2),
                        'cc': singlet_mult(cc), 'cf': singlet_mult(cf)},
                'assoc': f4alt == f4, 'f4w': len(f4), 'f4dim': msum(f4),
                'routes': {'decomp_I': r_decomp_I, 'decomp_II': r_decomp_II,
                           'pair_cc': r_pair_cc, 'pair_cf': r_pair_cf,
                           'pair_p4': r_pair_p4, 'decomp_p4': singlet_mult(p4)},
                'chan': dict((k, chan[k]) for k in chan), 'tri': tri,
                'p4': singlet_mult(p4), 'zero_p4': zero_wt(p4),
                'charges': charges, 'cap': DIMPRODUCT_CAP})
    return p


# =============================================================== 不变张量的道分解（R9）
# R8 数出 $16^{\\otimes4}$ 里有 2 个不变张量，但没有回答"这 2 个**各自**经由哪条双费米子道"。
# 把 R8 的配对和按道拆开就是本节的全部内容：
#   $\\mathrm{mult}((1),A\\otimes A)=\\sum_R n_R\\,\\#\\{S\\subset A:S\\cong\\bar R\\}$
# 每一道要么整体计入（$R$ 实：$\\bar R$ 就是它自己），要么整体不计（$R$ 复且 $\\bar R$ 不在这张
# 表里）$\\Rightarrow$ "在场但不闭合"的那一道恰是 $126_S$，也就是 R7.4/R8.5 里唯一能承载
# $\\nu_R$ Majorana 质量的 $\\overline{126}_H$ 的伙伴 $\\Rightarrow$ 同一张表里同时读到"物质-only
# 的四费米子算符走哪两条道"和"$|B-L|=2$ 那条道为什么进不来"。
#
# 本节也是本文件里第一次把配对和改走**标号**路径：登记表只到 $\\dim\\le210$，按名字查共轭会在
# 登记范围外把真实存在的伙伴静默算成 0 $\\Rightarrow$ R9.5 第四条把这个差额当场量出来。
TRIPLE_CAP = 200000       # 只对总权重不超过此数的三元乘积做"直接解方程"复算：纯成本取舍


def chan_key(nm):
    """道名的显示序：$(1)$ 最先，其余按维数；未登记的裸标号排最后。"""
    if nm == '(1)':
        return 0
    return int(nm) if nm.isdigit() else 10 ** 6


def channel_split(ch):
    r"""配对和按道拆开：$(\text{总数},\ [(\text{道名},\ n_R,\ \text{该道贡献})])$。

    该道贡献 $=n_R\cdot\\#\\{S\in\text{表}:S\cong\bar R\\}$，$\bar R$ 由 `conj_label` 现场算
    $\Rightarrow$ 实表示自配自己、复表示要求共轭也在同一个乘积里 $\Rightarrow$ 闭合是**道**的属性，
    与维数、与"这条道有没有对应的 Higgs"都无关。
    """
    tot, rows = 0, []
    for la, k in ch:
        lb = conj_label(la)
        c = sum(m for l2, m in ch if l2 == lb)
        rows.append((name_of(la), k, k * c))
        tot += k * c
    return tot, sorted(rows, key=lambda r: chan_key(r[0]))


def chan_tex(nm):
    """道名的 math 形式：`(1)`/`126` 原样，`126̄` → `\\overline{126}`，未登记裸标号原样。"""
    return ('\\overline{%s}' % nm[:-1]) if nm.endswith('\u0304') else nm


def fmt_chan(rows):
    """道表读成 `$10\\to 1$、$126\\to 0$` 一类：只印"该道贡献"，重数另说。"""
    return '、'.join('$%s\\to %d$' % (chan_tex(n), c) for _n, _k, c in rows)


CSPLIT = {}                  # 供报告 §8 取用（与门禁同源，不在报告里另算一遍）


def run_channel_layer():
    """R9：$16^{\\otimes4}$ 与 $16\\otimes16\\otimes\\overline{16}\\otimes\\overline{16}$ 的不变张量
    按双费米子道归口，并与链探针声明的标量内容对账。"""
    p = True
    W = dict((nm, irrep(NAMED[nm])[1]) for nm in NAMED)
    W['(1)'] = irrep(ZERO)[1]
    cc, cb2 = tprod(W['16'], W['16']), tprod(W['16̄'], W['16̄'])
    cf = tprod(W['16'], W['16̄'])
    p4, f4 = tprod(cc, cc), tprod(cf, cf)
    chs, chv = constit(cc), constit(cf)
    tot_s, rows_s = channel_split(chs)
    tot_v, rows_v = channel_split(chv)
    give = dict((n, c) for n, _k, c in rows_s + rows_v)

    # ---- R9.0 按道拆开必须回到 R8 解出来的总数
    exp_s = [('10', 1, 1), ('120', 1, 1), ('126', 1, 0)]
    exp_v = [('(1)', 1, 1), ('45', 1, 1), ('210', 1, 1)]
    p &= ok('R9.0', '$16^{\\otimes4}$ 的两个不变张量按双费米子道归口：$10$ 道 1 个、$120$ 道 '
                    '1 个、$126$ 道 0 个 $\\Rightarrow$ 加起来正是 R8 解整权重方程组得到的 2。'
                    '$16\\otimes\\overline{16}=(1)\\oplus45\\oplus210$ 三条道全是实表示 '
                    '$\\Rightarrow$ 各 1 个、总数 3 = R8 的另一个读数。这里的求和只用'
                    '"成分表 + 标号共轭"，与 R8 的 `decomp` 路径不共享代码',
            rows_s == exp_s and rows_v == exp_v
            and tot_s == sum(c for _n, _k, c in exp_s) == INV['p4'] == INV['routes']['decomp_p4']
            and tot_v == sum(c for _n, _k, c in exp_v) == singlet_mult(f4)
            == INV['routes']['decomp_I'],
            '手征侧（道名, $n_R$, 该道贡献 $=n_Rn_{\\bar R}$）%s $\\Rightarrow$ 合计 %d；R8 的'
            '整权重方程组 %d、`decomp` 独立复算 %d $\\Rightarrow$ $16^{\\otimes4}$ 的两个不变张量'
            '**分处两条道**，不是同一条道重数 2。对消侧 %s $\\Rightarrow$ 合计 %d；R8 配对和 %d、'
            '`decomp` %d' %
            (rows_s, tot_s, INV['p4'], INV['routes']['decomp_p4'], rows_v, tot_v,
             singlet_mult(f4), INV['routes']['decomp_I']))

    # ---- R9.1 闭合判据两路：标号自共轭 vs 直接解 mult((1),R\otimes R)
    crit = []
    for la, k in chs + chv:
        ms = irrep(la)[1]
        direct = singlet_mult(tprod(ms, ms)) or 0
        crit.append((name_of(la), conj_label(la) == tuple(la), direct > 0,
                     give[name_of(la)] > 0))
    bad = [nm for nm, rl, dr, g in crit if dr != rl or g != rl]
    p &= ok('R9.1', '闭合判据走两条不共享代码的路必须一致：$R$ 道贡献非零 $\\Longleftrightarrow$ '
                    '$R$ 自共轭（标号路径 $\\bar\\lambda=\\lambda$）$\\Longleftrightarrow$ `decomp` '
                    '在 $R\\otimes R$ 里解出恰好一个单态（整权重构路径）。六条道全部吻合 $\\Rightarrow$ '
                    '"复表示的双线性凑不出不变张量"是**判出来的**，不是引来的。其中**在场却不闭合**'
                    '的道恰有一条，就是 $126_S$ $\\Rightarrow$ 它正是 R7.4/R8.5 里唯一承载 $\\nu_R$ '
                    'Majorana 质量的 $\\overline{126}_H$ 的伙伴；而 $\\overline{126}$ **已在登记表里** '
                    '$\\Rightarrow$ "它不在 $16\\otimes16$ 里"是真的落空，不是查不到名字',
            not bad and [nm for nm, rl, dr, g in crit if not g] == ['126']
            and bool(conj_names(NAMED['126'])) and '126̄' in NAMED,
            '判据表（道, 自共轭, $\\mathrm{mult}((1),R\\otimes R)>0$, 该道有贡献）：%s；'
            '在场却不闭合的道：%s；两条路不一致的道：%s' %
            (crit, [nm for nm, _rl, _dr, g in crit if not g] or '无', bad or '无'))

    # ---- R9.2 道住在哪个双线性槽里（Adams 路径，与 tprod 不共享代码）
    sym, anti = sym2(W['16']), wedge2(W['16'])
    slot = dict((k, constituents(v)) for k, v in (('sym', sym), ('anti', anti), ('vec', cf)))
    slotof = dict([(nm, k) for k in ('sym', 'anti', 'vec') for nm, _m in slot[k]])
    p &= ok('R9.2', '道表与双线性槽对账：$\\mathrm{Sym}^2(16)=10\\oplus126$、'
                    '$\\wedge^2(16)=120$、$16\\otimes\\overline{16}=(1)\\oplus45\\oplus210$，'
                    '且 $\\mathrm{Sym}^2\\oplus\\wedge^2$ **逐权重**等于 $16\\otimes16$（两个槽由 '
                    'Adams $\\psi_2$ 算出，与直接做 $\\chi_{16}^2$ 的 `tprod` 是两条路）。于是 '
                    '$16^{\\otimes4}$ 的两个不变张量一个来自对称槽 $\\times$ 对称槽（$10$ 道）、'
                    '一个来自反对称槽 $\\times$ 反对称槽（$120$ 道）$\\Rightarrow$ 并不存在"'
                    '对称槽里都闭合"这条捷径：同在对称槽里的 $126$ 恰恰不闭合。此处 Sym/∧ 说的是 '
                    '$SO(10)$ 指标槽的对称性，**不是** Lorentz 或味指标 $\\Rightarrow$ 不能读成'
                    '"标量/赝标"',
            madd(sym, anti) == dict(cc) and
            [nm for nm, _k in slot['sym']] == ['10', '126'] and
            [nm for nm, _k in slot['anti']] == ['120'] and
            [nm for nm, _k in slot['vec']] == ['(1)', '45', '210'] and
            [slotof.get(n) for n in ('10', '120', '126')] == ['sym', 'anti', 'sym'] and
            [give[n] for n in ('10', '120', '126')] == [1, 1, 0],
            '槽表：%s；逐权重重构 $\\mathrm{Sym}^2\\oplus\\wedge^2=16\\otimes16$：%s' %
            (slot, madd(sym, anti) == dict(cc)))

    # ---- R9.3 与链探针声明的标量内容活对账（含一条可核对的否定结果）
    cont, decl, dunion = [], {}, set()
    if chain is None:
        p &= ok('R9.3', '链探针未载入 $\\Rightarrow$ 本层不下"哪条闭合道在模型谱里有母表示"的结论',
                False, 'chain is None')
    else:
        phi = [to_grid_dir(w, '$\\Phi$') for w in chain.BIDOUBLET]
        sig = [to_grid_dir(w, '$\\Sigma$') for w in chain.SIGMA_R]
        for la, k in chs + chv:
            ms = irrep(la)[1]
            nm = name_of(la)
            cont.append({'name': nm, 'closes': give[nm] > 0,
                         'phi': all(w in ms for w in phi),
                         'nphi': sum(1 for w in phi if w in ms), 'tphi': len(phi),
                         'sig': all(w in ms for w in sig),
                         'nsig': sum(1 for w in sig if w in ms), 'tsig': len(sig)})
        for scn, txt in chain.SCENARIOS.items():
            decl[scn] = [nm for nm in ('10', '45', '54', '120', '126', '144', '210')
                         if '%s_H' % nm in txt and ('无 $%s_H$' % nm) not in txt]
            dunion |= set(decl[scn])
        byn = dict((x['name'], x) for x in cont)
        side = ('10', '120', '126')
        p &= ok('R9.3', '与链探针**活对账**（权重与情形文字从 `chain.BIDOUBLET/SIGMA_R/'
                        'SCENARIOS` 现场读，不抄本文件的字面量）。两件事必须同时成立：'
                        '**(a) 权重包含在同侧是退化的** $\\Rightarrow$ 这条否定结果必须被点名；'
                        '**(b) 指派一旦由情形给定，闭合道里有没有母表示就是可数的。**',
                (all(byn[n]['phi'] for n in side) and
                 all(byn[n]['sig'] for n in ('45', '210')) and
                 not any(byn[n]['sig'] for n in side) and
                 not any(byn[n]['phi'] for n in ('45', '210', '(1)')) and
                 dunion == set(('10', '45')) and
                 [n for n in ('10', '120') if give[n] > 0 and n in dunion] == ['10'] and
                 '126' not in dunion and '120' not in dunion),
                '$\\Phi(1,2,2)$ 的 %d 条权重同时落在 $10/120/126$ 三条道的权重集里，'
                '$\\Sigma(1,1,3)_0$ 的 %d 条同时落在 $45/210$ 里 $\\Rightarrow$ 包含判据能分'
                '"手征侧 vs 对消侧"，分不了同侧内部**是哪一道** $\\Rightarrow$ "道 $\\to$ 母表示"'
                '的指派是模型的**输入**（写在情形文字里），不是权重算出来的结论。'
                '三个情形字面声明的母表示并集为 $\\{%s\\}$（情形 B 同时写明"无 $126_H$"；A 与 C 的'
                '文字里不出现任何 $X_H$ 记号 $\\Rightarrow$ 本层按字面读，不做"B 且…"的继承推理）'
                '$\\Rightarrow$ $16^{\\otimes4}$ 的两个不变张量里**恰有一个**（$10$ 道那个）可经'
                '模型声明有的 $10_H$ 因子化，另一个需要 $120_H$ 而无人声明 $\\Rightarrow$ "物质-only '
                '四费米子算符有两条道"与"这两条道在本模型谱里有没有媒介者"是两个独立读数。'
                '包含表：%s；各情形字面声明：%s' %
                (len(phi), len(sig), '、'.join(sorted(dunion, key=chan_key)),
                 [(x['name'], '闭合' if x['closes'] else '不闭合',
                   '$\\Phi\\subset$ %s(%d/%d)' % ('✔' if x['phi'] else '✘', x['nphi'], x['tphi']),
                   '$\\Sigma\\subset$ %s(%d/%d)' % ('✔' if x['sig'] else '✘', x['nsig'],
                                                    x['tsig'])) for x in cont], decl))

    # ---- R9.4 插入 Higgs：单插入三种结合皆空，成对插入才非零
    ins, pairs = {}, {}
    for Hn in ('126', '126̄'):
        hlab = constit(W[Hn])[0][0]
        gI, _u0 = pair_singlets(constit(p4), constit(W[Hn]))
        rgt = constit(tprod(cc, W[Hn]))
        gII, _u1 = pair_singlets(chs, rgt)
        gIII, direct = 0, []
        for la, ka in chs:
            for lb, kb in chs:
                dab = tprod(irrep(la)[1], irrep(lb)[1])
                n = sum(v for l2, v in (decomp(dab) or {}).items()
                        if conj_label(tuple(dynkin(l2))) == hlab)
                gIII += ka * kb * n
                tri = tprod(dab, W[Hn])
                tag = '%s⊗%s' % (name_of(la), name_of(lb))
                direct.append((tag, (singlet_mult(tri) or 0) if msum(tri) <= TRIPLE_CAP else None,
                               n, msum(tri)))
        ins[Hn] = {'gI': gI, 'gII': gII, 'gIII': gIII, 'direct': direct,
                   'small': sum(1 for _t, a, _n, _w in direct if a is not None),
                   'bare': sum(1 for l, _k in rgt if not registered(l))}
    for pr in (('126', '126'), ('126̄', '126̄'), ('126', '126̄')):
        ms = tprod(W[pr[0]], W[pr[1]])
        gI, uI = pair_singlets(constit(p4), constit(ms))
        gII, _u2 = pair_singlets(constit(tprod(cc, W[pr[0]])), constit(tprod(cc, W[pr[1]])))
        mir, _u3 = pair_singlets(constit(tprod(cb2, W[pr[0]])), constit(tprod(cb2, W[pr[1]])))
        pairs['%s|%s' % pr] = {'gI': gI, 'gII': gII, 'mirror': mir,
                               'unreg': sum(1 for l, _k in uI)}
    p &= ok('R9.4', '$|B-L|=2$ 的那个 Higgs **插不进**四费米子算符：'
                    '$\\mathrm{mult}((1),16^{\\otimes4}\\otimes H)=0$ 对 $H=126$ 与 $H='
                    '\\overline{126}$ 同时成立，且**三种结合方式**（先并成 $16^{\\otimes4}$ 再插入、'
                    '先并一个双线性再插入、逐道 Clebsch–Gordan 数共轭）给出同一个 0；在总权重不超过 '
                    '%d 的道对上还把三元乘积**直接解了一遍**当对照，逐道与 CG 计数相等。'
                    '而插入**一对** $126$ 之后单态个数确实非零 $\\Rightarrow$ "要拿到 '
                    '$|\\Delta(B-L)|=2$ 的四费米子不变张量就得成对插入"是本层数出来的。'
                    '共轭镜像再压一条独立约束：$\\mathrm{mult}((1),16^{\\otimes4}\\otimes126^{'
                    '\\otimes2})$ 必须等于把全部 $16$ 换成 $\\overline{16}$、$126$ 换成 '
                    '$\\overline{126}$ 后数出的同一个数' % TRIPLE_CAP,
            all(v['gI'] == v['gII'] == v['gIII'] == 0 and v['small'] == 5 and
                all(a == n for _t, a, n, _w in v['direct'] if a is not None) and
                v['small'] + sum(1 for _t, a, _n, _w in v['direct'] if a is None) == 9
                for v in ins.values())
            and all(v['gI'] == v['gII'] > 0 for v in pairs.values())
            and pairs['126|126']['mirror'] == pairs['126̄|126̄']['gI']
            and pairs['126̄|126̄']['mirror'] == pairs['126|126']['gI']
            and pairs['126|126̄']['mirror'] == pairs['126|126̄']['gI'],
            '单插入：' + '；'.join(
                '$H=%s$：结合 I/II/III 全为 %d、直解 %d 道（另 %d 道超出成本上限）、'
                '$16\\otimes16\\otimes H$ 侧登记范围外标号 %d 条' %
                (chan_tex(n), v['gI'], v['small'], 9 - v['small'], v['bare'])
                for n, v in ins.items()) +
            '。成对插入（结合 I／结合 II／共轭镜像）：' + '；'.join(
                '$16^{\\otimes4}\\otimes%s$ $=(\\,%d,\\,\\,%d,\\,\\,%d\\,)$，'
                '登记范围外 %d 条' %
                ('\\otimes'.join(chan_tex(x) for x in k.split('|')), v['gI'], v['gII'],
                 v['mirror'], v['unreg']) for k, v in pairs.items()))

    # ---- R9.5 变异测试：总数跟着成分表与共轭映射走；按名字查表在登记表外丢贡献
    def by_name(pa, pb):
        na = [(name_of(l), k) for l, k in pa]
        nb = [(name_of(l), k) for l, k in pb]
        return sum(k * sum(m for nm2, m in nb if nm2 in conj_name_set(nm))
                   for nm, k in na)
    drop = [x for x in chs if name_of(x[0]) != '120']
    closing = next(x for x in chs if give[name_of(x[0])] > 0)
    dnm = name_of(closing[0])
    dbl = chs + [closing]
    fake = chs + constit(W['126̄'])
    biga, bigb = constit(p4), constit(tprod(W['126'], W['126']))
    m_lab, m_unreg = pair_singlets(biga, bigb)
    r82 = ((constit(cc), constit(cb2)), (constit(cf), constit(cf)), (constit(cc), constit(cc)))
    mut = dict((k, channel_split(x)[0]) for k, x in
               (('drop', drop), ('dbl', dbl), ('fake', fake), ('real', chs)))
    p &= ok('R9.5', '变异测试（四处植入）说明本节既没把 2 写成字面量、也没把配对和偷偷写成'
                    '"按名字查表"：从道表里**删掉** $120$ $\\Rightarrow$ 总数掉到 %d；把一条'
                    '**闭合道**（$%s$）的重数翻倍 $\\Rightarrow$ 该道贡献按 $n_Rn_{\\bar R}$ 是 '
                    '$2\\times2=4$ 而非 2 $\\Rightarrow$ 总数升到 %d $\\Rightarrow$ 配对和'
                    '**双线性**地依赖成分表，不是数"有没有"；伪造 $\\overline{126}$ 也在 '
                    '$16\\otimes16$ 里 $\\Rightarrow$ $126$ 与 $\\overline{126}$ 互配各得 1 '
                    '$\\Rightarrow$ 升到 %d（真值 %d）。第四条是**反向**的：在 R8.2 用到的那三张'
                    '表上"按名字查共轭"与"按标号算共轭"必须给同一个数（那里没有登记范围外的标号 '
                    '$\\Rightarrow$ 旧路径没错），而在 $16^{\\otimes4}\\otimes126^{\\otimes2}$ 上'
                    '按名字查必须**更小**，因为那里有 %d 条登记范围外的标号 $\\Rightarrow$ 名字路径'
                    '会把真实存在的共轭伙伴静默算成 0' %
            (mut['drop'], chan_tex(dnm), mut['dbl'], mut['fake'], mut['real'], len(m_unreg)),
            mut['drop'] == tot_s - 1 and mut['dbl'] == tot_s + 3
            and mut['fake'] == tot_s + 2 and mut['real'] == tot_s
            and m_lab > by_name(biga, bigb)
            and all(pair_singlets(a, b)[0] == by_name(a, b) and not pair_singlets(a, b)[1]
                    for a, b in r82),
            '植入后的总数：删 $120\\to$ %d、闭合道 $%s$ 翻倍 $\\to$ %d、伪造 $\\overline{126}$ '
            '在场 $\\to$ %d（真值 %d）。$16^{\\otimes4}\\otimes126^{\\otimes2}$：标号路径 %d、'
            '名字路径 %d、登记范围外 %d 条标号' %
            (mut['drop'], chan_tex(dnm), mut['dbl'], mut['fake'], tot_s, m_lab,
             by_name(biga, bigb), len(m_unreg)))

    CSPLIT.update({'rows_chiral': rows_s, 'rows_vector': rows_v,
                   'tot_chiral': tot_s, 'tot_vector': tot_v,
                   'r8_chiral': INV['p4'], 'r8_vector': INV['routes']['decomp_I'],
                   'crit': crit, 'slot': slot, 'slotof': slotof, 'cont': cont, 'decl': decl,
                   'decl_union': sorted(dunion, key=chan_key), 'ins': ins, 'pairs': pairs,
                   'mut': dict(mut, lab=m_lab, byname=by_name(biga, bigb),
                               unreg=len(m_unreg), dnm=dnm),
                   'cap': TRIPLE_CAP,
                   'bare': {'chiral': sum(1 for l, _k in chs if not registered(l)),
                            'vector': sum(1 for l, _k in chv if not registered(l)),
                            'p4': sum(1 for l, _k in biga if not registered(l))}})
    return p


# =============================================================== 报告
MATHSPAN = re.compile(r'\$([^$]+)\$')
PIPE = re.compile(r'(?<!\\)\|')
SEPROW = re.compile(r'^\|(?:\s*:?-+:?\s*\|)+$')
REPR_LEAK = re.compile(r"\['|'\]|\[\(|\{'|'\}|\bNone\b")
# 漏写 `% V` / 把 `%` 只绑到拼接字面量的第一段 ⇒ 报告里会留下没被替换的 %(name)s 或 %d。
# 这类缺陷不会让任何门禁变红，只会打印出一串占位符（本轮真实踩到两次），故当场拒绝。
FMT_LEAK = re.compile(r"%\([A-Za-z0-9_]*\)[sdf]|%\.[0-9]+[df]|%[sdif]\b")
# TeX 控制词按"最长匹配"切分：\lvert 后面紧跟字母或数字时两者并成一个未定义控制词
# （\lvertB），整段公式报错。数学模式里的空格不改变排版 ⇒ 补空格是唯一无损的修法。
DELIM_MUNCH = re.compile(r'\\[lr]vert[A-Za-z0-9]')
# 紧跟字母的反斜杠串**长度必须是 1**。本报告的公式来自两条会各自翻倍的路：
#   (1) r"""…""" 不消费任何转义 ⇒ 源码里手写的 `$\\nu$` 原样落进文件；
#   (2) §17 的"算得/应为/备注"三列是 repr 转储（那是审计痕迹，故意保留），而 repr 会把数据里
#       本就合法的 `$\nu^c$` 里的反斜杠翻倍成 `$\\nu^c$` —— 本轮 67 处全部出自这条。
# 两种翻倍落进文件后同形：MathJax 把 `\\` 读成换行、后面的控制词降级成斜体字母（`\nu` 显示成
# "nu"）。数值门禁看不见，渲染才看得见 ⇒ 全文当场判：模式 = 两个及以上反斜杠紧跟字母；
# `\\{`、`\\ ` 这类换行/转义花括号不在本条范围内（今天全文 0 处，判据与范围由防护样例钉住）。
BS_MUNCH = re.compile(r'\\{2,}[A-Za-z]+')
# 同一判据的**改写**版：只吃反斜杠、不吃后面的控制词名（否则 `$\\nu$` 会被改成少一个字母的 `$u$`）。
BS_RUN = re.compile(r'\\{2,}(?=[A-Za-z])')


def md_unescape(s):
    r"""把表示层的翻倍折回一个反斜杠：字面内容逐字不动，只改反斜杠个数（判据同 BS_MUNCH）。
    用在 repr 转储的单元格上 —— 那里的翻倍不是读数的一部分，而是 str(container) 的转义产物。
    替换式必须写成函数：re.sub 的字符串替换模板会把孤零零的一个反斜杠当成转义开头而直接抛错。
    入参可以是数字（"算得/应为"两列有时就是裸数），故先 str() —— 与原来 `%s` 的语义逐字相同。"""
    return BS_RUN.sub(lambda _m: chr(92), str(s))


def table_row_safe(line):
    r"""Markdown 表格里裸 $|$ 会被当成列分隔符：$\max|B-L|$ 这类写法曾把整行拆断，
    而且列数不匹配只是"渲染错位"，不会让任何门禁变红 ⇒ 出表前逐行改写为 \lvert/\rvert。

    分隔符后**必须留一个空格**：TeX 读控制词是最长匹配，`\lvert B` 才是 `\lvert` 加 `B`，
    写成 `\lvertB` 就变成一个未定义控制词、整个公式报错。数学模式里的空格不参与排版，
    所以补这个空格只修 token 边界、不改渲染结果（同文件第四条排版不变量在守它）。"""
    if not line.startswith('|'):
        return line

    def fix(m):
        body = m.group(1)
        if '\\|' in body:
            return m.group(0)
        parts = body.split('|')
        assert len(parts) % 2 == 1, '表格行的数学段有奇数个裸竖线：%r' % body
        out = parts[0]
        for i in range(1, len(parts)):
            out += ('\\lvert ' if i % 2 == 1 else '\\rvert ') + parts[i]
        return '$' + out + '$'
    return MATHSPAN.sub(fix, line)


def higgs_tex(names):
    r"""表示名列表 → $10_H\oplus\overline{126}_H$；空表降级成文本，**不让生成器抛异常**。"""
    return ('$%s$' % '\\oplus'.join(tex_name(n)[1:-1] + '_H' for n in names)
            if names else '（空）')


def plain_tex(names):
    r"""表示名列表 → $10$、$\overline{126}$（不带 $_H$ 下标，用于"这一列本身"而非 Higgs 候选）。"""
    return '、'.join(tex_name(n) for n in names) or '（空）'


def yukawa_section():
    r"""报告 §6：d=4 物质–Higgs Yukawa 通道（R7）。

    只吃 `YUK`/`YUKCH` —— 它们是 R7 各门禁当场比对过的那批对象 ⇒ 正文里的每个数
    与它脚下的表同源；R7 未运行（上游门禁未过）时本节整段降级，不让生成器抛异常。
    """
    if not YUKCH.get('allow'):
        return ['', '## 6. d=4 物质–Higgs Yukawa 通道（R7）', '',
                '**R7 未运行 ⇒ 本节不出任何结论。**', '']
    allow, parts, rebuilt = YUKCH['allow'], YUKCH['parts'], YUKCH['rebuilt']
    chiral, maj, extra = YUKCH['chiral'], YUKCH['maj'], YUKCH['extra']
    must0, blnu, blneed, blsum = YUKCH['must0'], YUKCH['blnu'], YUKCH['blneed'], YUKCH['blsum']
    nu, needw = YUKCH['nu'], YUKCH['needw']
    ntot, ntotD = YUKCH['ntot'], YUKCH['ntotD']

    def sumtex(pairs):
        out = []
        for nm, k in (pairs or []):
            t = '1' if nm == '(1)' else tex_name(nm)[1:-1]
            out.append(t if k == 1 else '%d\\cdot %s' % (k, t))
        return '\\oplus'.join(out) or '（拆分未成功）'
    nuval = fmt(nu[0]) if nu else '（无 ⇒ R7.3 已 FAIL）'
    nunote = ('（$B-L=%s$、$T^3_R=%s$）' % (chg(nu[0], BL), chg(nu[0], T3R))) if nu else ''
    needval = fmt(needw) if needw else '（无）'
    neednote = ('（$B-L=%s$、$Q=%s$）' % (chg(needw, BL), chg(needw, QHP))) if needw else ''
    sigchk = ('45' in allow['vec'], '45' in chiral)
    extratex = '、'.join('%s（可加性 %d/%d）' % (tex_name(n), a, b)
                         for n, a, b in extra) or '（空）'
    must0tex = '、'.join('%s（%d）' % (tex_name(n), k) for n, k in must0) or '空'
    L = ['', '## 6. d=4 物质–Higgs Yukawa 通道（R7）', '',
         '§4 问的是"哪个 Higgs 里**有**能破 $B-L$ 的中性分量"；本节问一个相互独立的物理问题：'
         '"哪个 Higgs **拿得到** $16_F16_FH$ 这个可重整算符"。做法与 §3 同源而**不同路**：',
         '先把 $16_F$ 的双线性乘积拆成不可约成分（在出现的支配权上解单位三角方程组，R7.1），',
         '再取**共轭** $\\Rightarrow$ 不变张量要求 $H^*\\subset16_F16_F$。', '',
         '| 双线性乘积 | $SO(10)$ 成分（算得） | 取共轭 $\\Rightarrow$ d=4 允许的 Higgs | 按整权重构还原 |',
         '|---|---|---|---|']
    for key, nm in (('sym', '\\mathrm{Sym}^2(16)'), ('anti', '\\wedge^2(16)'),
                    ('vec', '16\\otimes\\overline{16}')):
        L.append('| $%s$ | $%s$ | %s | %s |' %
                 (nm, sumtex(parts.get(key)), higgs_tex(allow.get(key, [])),
                  '✔' if rebuilt.get(key) else '✘'))
    L += ['', '三行的"重构还原"都是当场把拆出的成分按整权加回去、逐权重等于原多重集 $\\Rightarrow$ '
          '允许集是算出来的。**注意第二列与第三列不同**：$\\mathrm{Sym}^2(16)$ 的成分是 $126$，'
          '而允许的 Higgs 是 $\\overline{126}_H$ —— 共轭这一步正是"哪个 Higgs 能写进拉氏量"的'
          '分水岭（第 4 条列出"只看荷守恒会误放行"的那类表示）。', '',
          '逐表示对照（"权重可加性" = 该表示的**不同权重**里有多少个，其相反数落在双线性乘积的'
          '权重支集里：$16+16$ 支集共 %d 个格点、$16-16$ 支集共 %d 个。每行**只按自己所属通道**'
          '计分（手征行看前者、对消行看后者）$\\Rightarrow$ 两套支集混用会得出假矛盾：'
          '$45_H/210_H$ 属于对消通道，在 $16+16$ 支集上得分 0 是天经地义的。这条整体只是'
          '**必要**条件，列出是为了量化它比通道表弱多少）：' % (ntot, ntotD), '',
          '| 表示 | 维数 | 实/复 | 对称手征 | 反对称手征 | 向量型 | 可加性 $16+16$ '
          '| 可加性 $16-16$ | 携带 $-2\\nu$ |', '|---|---|---|---|---|---|---|---|---|']
    for r in YUK:
        L.append('| %s | %d | %s | %s | %s | %s | %d/%d | %d/%d | %s |' %
                 (tex_name(r['name']), r['dim'], '实' if r['real'] else '复',
                  '✔' if r['sym'] else '—', '✔' if r['anti'] else '—',
                  '✔' if r['vec'] else '—', r['realizable'], r['nweights'],
                  r['realizableD'], r['nweights'], '✔' if r['holds_maj'] else '—'))
    L += ['', '**四条读出来的结果**（编号即门禁）：', '',
          '1. **两类通道互不相交**（R7.2）：手征通道 %s 与向量型通道 %s $\\Rightarrow$ 交集 %s。'
          '向量型通道里的 Higgs 只有当谱里**同时**有 $16_F$ 与 $\\overline{16}_F$ 时才耦合物质；'
          '而 UFE-1 的物质是 $3\\times16$、一个 $\\overline{16}_F$ 都没有（R7.7 现场与链探针对账）'
          '$\\Rightarrow$ **它们对手征物质没有 d=4 Yukawa 项**。链探针情形 B 里承担 $SU(2)_R$ 破缺的'
          '那个 $B-L=0$ 三重态 $\\Sigma(1,1,3)_0$ 取自 $45_H$（R7.7 逐权核对 $\\Sigma\\subset45$；'
          'S2.7/R5.2 判它**不是** $\\Delta_R$），而 "$45_H$ 只在对消通道"这一条当场成立：'
          '（核算"对消通道含 $45_H$"= %s、"手征通道含 $45_H$"= %s）'
          '$\\Rightarrow$ $\\Sigma$ 取期望值不产生任何费米子质量。（本节**不**排除它与高维算符耦合。）'
          % (higgs_tex(chiral), higgs_tex(allow['vec']),
             plain_tex(sorted(set(chiral) & set(allow['vec']))), sigchk[0], sigchk[1]),
          '2. **右手中微子在每一代里唯一**（R7.3）：$16_F$ 中"色单态 + $SU(2)_L$ 单态 + '
          '$Y=0,Q=0$"的权重**恰好一个**，算得 $\\nu=%s$%s。$\\nu_R^c$ 因此不是额外添加的字段，'
          '而是 $16_F$ 权重层的必然成员。' % (nuval, nunote),
          '3. **see-saw 现在有两条独立的推导路径落在同一个表示上**（R7.4/R7.5）：'
          '$\\nu_R^c\\nu_R^c$ 要求 Higgs 携带权重 $-2\\nu=%s$%s；在 $\\dim\\le210$ 的 %d 个表示里'
          '它**只**落在 %s，而 %s 正是通道表判给"对称手征通道"的成员 $\\Rightarrow$ '
          '"能给 $\\nu_R$ 质量"与 §4 的"能破 $B-L$"在同一个表示上重合，且 R7.5 确认 $-2\\nu$ '
          '就是该表示 $\\Delta_R$ 三重态里**唯一**的 $Q=0$ 成员 $\\Rightarrow$ 两件事是'
          '**同一次取期望值**（$B-L$ 守恒现场核算：$2\\times(%s)+(%s)=%s$）。'
          % (needval, neednote, len(YUK), higgs_tex(maj), higgs_tex(allow['sym']),
             blnu, blneed, blsum),
          '4. **判据必须是张量分解，只看荷守恒会放行错误的 Higgs**（R7.6）：现场把"权重可加性'
          '通过、但通道表不受理"的表示列出来 $\\Rightarrow$ %s。这些表示的每一个权重确实都能'
          '与两个 $16_F$ 的权重把荷配平，但它们作为 Higgs 不出现在 $16_F16_F$ 里（要共轭）'
          '$\\Rightarrow$ 荷守恒只是**单向**必要条件；反方向"通道表受理、可加性却为 0"的表示：'
          '%s（必须为空，否则张量分解与荷守恒直接矛盾）。'
          % (extratex, must0tex), '',
          '两条**变异测试**（R7.8/R7.9）说明上面四条不是字符串在自证：把成分清单植成 $16$，'
          '允许集立即换成 $16$ 的共轭而不是原来那批名字（$\\Rightarrow$ 共轭映射真的在跑）；'
          '把双线性的两个因子换成同一条 $SU(2)_R$ 串里的**带电**伙伴，所需权重立刻落到 '
          '$\\Delta_R$ 的**双重带电**分量 $\\Rightarrow$ "$Q=0$ 才允许取期望值"这条物理输入'
          '确实在起决定作用。两次的植入前后对照都印在 §17 对应行的备注里。', '',
          '**本节的边界**（不进门禁，故明写）：', '',
          '* 只判 **d=4**（可重整）通道，且只判到"哪些表示允许出现"。哪个拷贝与哪一代费米子耦合、'
          '系数多大、$CP$ 结构如何，**都不在本仪器覆盖范围内** $\\Rightarrow$ **L10 未关闭**。',
          '* 实表示在 `NAMED` 里登记了两个名字（$10$ 与 $\\overline{10}$ 同标号，R2.c10c45）'
          '$\\Rightarrow$ 通道列只挂在先注册的那个名字上，$\\overline{10}_H$ 与 $10_H$ 是**同一个场**，'
          '不是两个候选。',
          '* 把上表翻译成味结构要用到场的交换性质（$10_H/\\overline{126}_H$ 通道在两个 $16_F$ 的 '
          '$SO(10)$ 指标上对称、$120_H$ 通道反对称），而**本仪器没有味自由度** $\\Rightarrow$ 这条'
          '是文献里的标准论证、不进门禁；它的可检验后果是"纯 $120_H$ 的 Yukawa 矩阵反对称 '
          '$\\Rightarrow$ 秩 $\\le2$ $\\Rightarrow$ 单靠它给不出三行满秩的质量矩阵"。',
          '* "允许"是群论陈述，**不**等于"自然界里有这个场"；更**不**提升 UFE-1 任何结论的证据等级。',
          '']
    return L


def inv_section():
    r"""报告 §7：不变张量簿记（R8）。

    只吃 `INV` —— 它是 R8 各门禁当场比对过的那批对象 ⇒ 本节每个数与它脚下的表同源；
    R8 未运行（上游门禁未过）时整段降级，不让生成器抛异常。
    """
    if not INV.get('ledger'):
        return ['', '## 7. 不变张量簿记：荷账本、不变张量与物质-only 算符（R8）', '',
                '**R8 未运行 ⇒ 本节不出任何结论。**', '']
    led, routes, chan = INV['ledger'], INV['routes'], INV['chan']
    allow = YUKCH.get('allow', {})
    per = dict((n, z // k) for n, z, k in led[-1]['parts']['parts'] if k)
    gaptex = '、'.join('%s 每个 %d' % (tex_name(n), per[n])
                       for n in ('45', '54', '210') if n in per)
    V = {'z0': led[0]['zero'], 's1': led[1]['singlet'],
         'gap': led[-1]['zero'] - led[-1]['singlet'], 'gaptex': gaptex,
         'f4w': INV['f4w'], 'f4dim': INV['f4dim'], 'assoc': INV['assoc'],
         'pair_cc': routes['pair_cc'], 'pair_p4': routes['pair_p4'], 'p4': INV['p4'],
         'cap': INV['cap'], 'npairs': INV['npairs'], 'ones': INV['ones'],
         'wrong': '无' if not INV['wrong'] else INV['wrong'],
         'cf': INV['mut']['cf'], 'm1': INV['mut']['m1'], 'cc': INV['mut']['cc'],
         'm15': led[1]['zero'] - 1,
         'm2': ('不再是特征标的非负整组合 ⇒ 重构对账拒绝' if INV['mut']['m2'] is None
                else INV['mut']['m2']),
         'tick': '✔' if INV['assoc'] else '✘',
         'nlab': max(x['parts']['nlab'] for x in led)}

    def zeroparts(x):
        p = x['parts']
        return ('、'.join('%s 占 %d' % (tex_name(n), z) for n, z, _k in p['parts']) +
                ('' if not p['unreg']
                 else '；另有 %d 条未登记标号（$\\sum c_i>3$，§2 的搜索范围之外）占 %d'
                      % (p['nlab'], p['unreg'])))
    L = ['', '## 7. 不变张量簿记：荷账本、不变张量与物质-only 算符（R8）', '',
         '§6 判"哪个 Higgs 拿得到 d=4 算符"，材料是**双线性乘积的成分再取共轭**。本节换一条',
         '不共享代码的路：直接数 $\\mathrm{mult}((1),V)$ —— 即 $V$ 里**规范不变**方向的个数 ——',
         '并要求它把 §6 的通道表复算成同一张。走这条路必须先分开两件容易混为一谈的事：',
         '',
         '* **荷账本** $\\dim V_0=m_V(0)$：全部 Cartan 荷同时为零的方向数，也就是"荷配得平"；',
         '* **不变张量** $\\mathrm{mult}((1),V)$：其中真正规范不变的那一部分。',
         '',
         '恒有 $\\mathrm{mult}((1),V)\\le\\dim V_0$，而两者之差可以**逐成分拆开核对**：',
         '$m_{A\\otimes B}(0)=\\sum_R n_Rm_R(0)$，每个不可约成分按它自己的零权重数记账',
         '（R8.1a）。', '',
         '| 乘积 | 维数 | 不同权重 | 荷账本（零权方向） | 不变张量 | 零权按成分归口 |',
         '|---|---|---|---|---|---|']
    for x in led:
        L.append('| $%s$ | %d | %d | %d | %d | %s |' %
                 (x['tex'][1:-1], x['dim'], x['ndist'], x['zero'], x['singlet'], zeroparts(x)))
    L += ['', '第一行是本节最硬的一条物理事实：$16_F\\otimes16_F$ 的**零权方向为 %(z0)d** '
          '$\\Rightarrow$ '
          '两个手征物质的双线性连"荷配平"都做不到，更谈不上规范不变 $\\Rightarrow$ **手征费米子'
          '没有裸质量项**（R8.4：$\\mathrm{mult}((1),16\\otimes16)=\\mathrm{mult}((1),\\mathrm{Sym}^2)'
          '=\\mathrm{mult}((1),\\wedge^2)=0$，而 $16\\otimes\\overline{16}$ 恰有 %(s1)d 个 '
          '$\\Rightarrow$ '
          '质量项要么靠 Higgs，要么把 $16$ 与 $\\overline{16}$ 同时请进场）。'
          '第三行的 %(gap)d 个"缺口"不是丢了，而是记在 $45/54/210$ 等成分的 Cartan 子空间上'
          '（%(gaptex)s）$\\Rightarrow$ '
          '"荷守恒"作为判据比"不变"弱了多少，是可数的。' % V, '',
          '**四条路径咬合同一个数**（R8.0/R8.2）。不变张量基本定理 '
          '$\\mathrm{mult}((1),A\\otimes B)=\\delta_{B,\\bar A}$ 先在 $\\dim A\\cdot\\dim B'
          '\\le%d$ 的**全部** %d 个已登记表示对上现场核验（重数为 1 的恰是 %d 对互为共轭的，'
          '反例：%s）$\\Rightarrow$ 下面"配对和"那条路用的查表规则是验证过的，不是引用来的：'
          % (INV['cap'], INV['npairs'], INV['ones'], '无' if not INV['wrong'] else INV['wrong']),
          '',
          '| 路径 | 算法 | $16\\otimes16\\otimes\\overline{16}\\otimes\\overline{16}$ '
          '| $16^{\\otimes4}$ |', '|---|---|---|---|',
          '| 解方程 I | `decomp` 作用在 $(16\\otimes16)\\otimes(\\overline{16}\\otimes'
          '\\overline{16})$ | %d | %d |' % (routes['decomp_I'], routes['decomp_p4']),
          '| 解方程 II | `decomp` 作用在 $(16\\otimes\\overline{16})\\otimes'
          '(16\\otimes\\overline{16})$ | %d | — |' % routes['decomp_II'],
          '| 配对和（手征侧） | $\\sum_Rn_R(16\\otimes16)\\,m_{\\bar R}(\\overline{16}\\otimes'
          '\\overline{16})$ | %d | %d |' % (routes['pair_cc'], routes['pair_p4']),
          '| 配对和（对消侧） | $\\sum_Rn_R(16\\otimes\\overline{16})^2$ | %d | — |'
          % routes['pair_cf'],
          '',
          '两种结合方式先给出**逐权重相同**的多重集（%d 个不同权重、共 %d 个权重（含重数）的两条路'
          '径产物相等：%s）$\\Rightarrow$ 张量积结合律在本仪器里是可核对的事，不是默认成立的。'
          '配对和侧还顺带把**共轭**的分量暴露出来：把 $\\overline{16}$ 全换成 $16$ 之后，'
          '$126$ 找不到 $\\overline{126}$ 作伙伴 $\\Rightarrow$ 同一个函数从 %d 掉到 %d，'
          '这正是 R8.6 变异测试读到的差别。'
          % (INV['f4w'], INV['f4dim'], V['tick'], routes['pair_cc'], routes['pair_p4']), '',
          '**通道表的独立复算**（R8.3）：不查 §6 的成分表，改为逐个 Higgs 候选数三重积里的单态 '
          '$\\mathrm{mult}((1),\\text{双线性}\\otimes H)$ 是否 $>0$。两条路径必须按**标号**比对'
          '（$10$ 与 $\\overline{10}$、$45$ 与 $\\overline{45}$ 同标号，R2.c10c45 $\\Rightarrow$ '
          '按名字比会假报错）：', '',
          '| 双线性 | 本层数出的 Higgs 候选 | §6 的通道表 | 按标号一致 |', '|---|---|---|---|']
    for key, nm in (('sym', '\\mathrm{Sym}^2(16)'), ('anti', '\\wedge^2(16)'),
                    ('vec', '16\\otimes\\overline{16}')):
        L.append('| $%s$ | %s | %s | %s |' %
                 (nm, plain_tex(chan[key]['names']) or '（空）',
                  higgs_tex(allow.get(key, [])) or '（空）',
                  '✔' if chan[key]['agree'] else '✘'))
    L += ['', '**物质-only 的不变算符能做什么、不能做什么**（R8.5）。单态 $(1)$ 的权重集就是'
          '$\\{(0,0,0,0,0)\\}$ 一个点，它在 $B-L$、$T^3_L$、$T^3_R$、$Y$、$Q$ 五个方向上的荷'
          '全为 0（现场取链探针的方向算，不是定义）$\\Rightarrow$ **任何只用物质场凑出来的规范'
          '不变算符自动 $\\Delta(B-L)=0$**。同时：', '',
          '* $\\mathrm{mult}((1),16^{\\otimes4})=%d>0$ $\\Rightarrow$ 规范群**不**禁止四费米子'
          '不变算符——质子衰变那一类算符的荷前提在 $SO(10)$ 下成立（本表只数规范不变性，'
          ' Lorentz 与味的结构见下面的边界）。' % INV['p4'],
          '* $\\mathrm{mult}((1),16\\otimes16)=0$ 而 $\\mathrm{mult}((1),16\\otimes16\\otimes H)$ '
          '在 $H=\\overline{126}$ 上为 %d、在 $H=126$ 上为 %d $\\Rightarrow$ '
          '$|\\Delta(B-L)|=2$ 的那一类（$\\nu_R$ Majorana 质量、$n\\text{–}\\bar n$）'
          '**必须**插入一个带 $|B-L|=2$ 分量的 Higgs，且必须是**带共轭杠**的那个 $\\Rightarrow$ '
          '与 §6 的 R7.4/R7.5（$-2\\nu$ 唯一落在 $\\overline{126}_H$）同源而路径独立。'
          % (INV['tri']['126̄'], INV['tri']['126']),
          '',
          '变异测试（R8.6，**三处植入**）说明本节的数跟着输入走、不是写死的字面量：'
          '把 $16\\otimes\\overline{16}$ 的零权空间去掉 **1** 个方向 $\\Rightarrow$ 它合法地退化成 '
          '$45\\oplus210$（那正是 $m(0)=%(m15)d$ 的答案），单态由 %(cf)d 变 %(m1)d；去掉 **2** 个 '
          '$\\Rightarrow$ %(m2)s；把 $\\overline{16}$ 换成 $16$ $\\Rightarrow$ 单态由 %(cf)d 变 '
          '%(cc)d。三条合起来说明 `singlet_mult` 既不是恒真也不是恒假，且它的失败分支活着。' % V,
          '',
          '**本节的边界**（不进门禁，故明写）：', '',
          '* 数出来的是**规范不变张量的个数**，不是物理算符的个数：把四个 $16_F$ 落到真实'
          '拉氏量里还要过 Lorentz 指标、代（味）指标与 Fierz 恒等式三关 $\\Rightarrow$ '
          '"$16^{\\otimes4}$ 有 %(p4)d 个不变张量"**不等于**"有 %(p4)d 个质子衰变算符"，'
          '本节的数**不**回填到任何寿命计算里（$\\tau_p$ 只由 [SO(10) 链统一报告]'
          '(SO10链统一报告.md) 的那套口径给出，与本节无数据通路）。' % V,
          '* $\\Delta(B-L)=0$ 是**荷**的陈述，不是重子数：上表的不变张量完全可以 '
          '$\\Delta B=\\pm1,\\ \\Delta L=\\pm1$。本节**不**判定哪个分量对应哪个算符，'
          '那需要 3221 分支层次的逐分量对账。',
          '* 只判到 $\\dim\\le210$ 的已登记表示：$16^{\\otimes4}$ 的拆分里出现了 '
          '%d 条 $\\sum c_i>3$ 的标号 $\\Rightarrow$ 本节给它们**不起名字**（不影响单态计数，'
          '因为 $\\mathrm{mult}((1),V)$ 只要求解出 $(1)$ 的重数，而 `decomp` 的重构对账把'
          '整张多重集都核对了一遍）。' % max(x['parts']['nlab'] for x in led),
          '* "不变"是群论陈述，**不**等于"自然界里有这个算符"；更**不**提升 UFE-1 任何结论的'
          '证据等级 $\\Rightarrow$ **L10 未关闭**（系数、位势、味结构仍未算）。', '']
    return L


def chan_section():
    r"""报告 §8：不变张量的道分解（R9）。

    只吃 `CSPLIT` —— 它是 R9 各门禁当场比对过的那批对象 ⇒ 本节每个数与它脚下的表同源；
    R9 未运行（上游门禁未过）时整段降级，不让生成器抛异常。
    """
    if not CSPLIT.get('rows_chiral'):
        return ['', '## 8. 不变张量的道分解：哪一个不变张量经由哪条双费米子道（R9）', '',
                '**R9 未运行 ⇒ 本节不出任何结论。**', '']
    rows = CSPLIT['rows_chiral'] + CSPLIT['rows_vector']
    give = dict((n, c) for n, _k, c in rows)
    mult = dict((n, k) for n, k, _c in rows)
    crit = dict((x[0], x) for x in CSPLIT['crit'])
    side = dict([(n, '手征 $16\\otimes16$') for n, _k, _c in CSPLIT['rows_chiral']] +
                [(n, '对消 $16\\otimes\\overline{16}$') for n, _k, _c in CSPLIT['rows_vector']])
    slotex = {'sym': '$\\mathrm{Sym}^2(16)$', 'anti': '$\\wedge^2(16)$',
              'vec': '$16\\otimes\\overline{16}$'}
    decl = CSPLIT['decl']
    scn_of = dict((n, [s for s in sorted(decl) if n in decl[s]]) for n in give)
    closing = [n for n, _k, _c in CSPLIT['rows_chiral'] if give[n] > 0]
    openc = [n for n in sorted(give, key=chan_key) if not give[n]]
    cont = dict((x['name'], x) for x in CSPLIT['cont'])
    mut = CSPLIT['mut']

    def tex(ns):
        return '、'.join('$%s$' % chan_tex(n) for n in ns)

    V = {'p4': CSPLIT['tot_chiral'], 'p3': CSPLIT['tot_vector'],
         'open': tex(openc) or '无', 'clos': tex(closing),
         'phi': tex([n for n, _k, _c in rows if cont[n]['phi']]),
         'sig': tex([n for n, _k, _c in rows if cont[n]['sig']]),
         'nphi': cont[rows[0][0]]['tphi'], 'nsig': cont[rows[0][0]]['tsig'],
         'dnm': chan_tex(mut['dnm']), 'drop': mut['drop'], 'dbl': mut['dbl'],
         'fake': mut['fake'], 'real': mut['real'], 'lab': mut['lab'],
         'byname': mut['byname'], 'unreg': mut['unreg'], 'cap': CSPLIT['cap'],
         'decl': tex(CSPLIT['decl_union']) or '无',
         'sci': '；'.join(('情形 %s 声明 %s' % (s, tex(decl[s]))) if decl[s] else
                          '情形 %s 声明（文字里不出现任何 $X_H$ 记号）' % s
                          for s in sorted(decl))}
    L = ['', '## 8. 不变张量的道分解：哪一个不变张量经由哪条双费米子道（R9）', '',
         '§7 数出 $16^{\\otimes4}$ 里有 %(p4)d 个不变张量、$(16\\otimes\\overline{16})^{\\otimes2}$ '
         '里有 %(p3)d 个，但没有回答"这些不变张量**各自**经由哪条双费米子道"。把 §7 的配对和'
         '按道拆开就是本节的全部内容：$\\mathrm{mult}((1),A\\otimes A)=\\sum_R n_R\\,\\#\\{S'
         '\\subset A:S\\cong\\bar R\\}$ $\\Rightarrow$ 每一道要么整体计入（$R$ 实，此时 $\\bar R$ '
         '就是它自己），要么整体不计（$R$ 复且 $\\bar R$ 不在这张表里）$\\Rightarrow$ 拆开后读到'
         '的是"**哪一条**"，不是"有几个"。' % V, '',
         '| 侧 | 道 | $n_R$ | 该道贡献 $n_Rn_{\\bar R}$ | 自共轭 | 双线性槽 | 谁声明了母表示 |',
         '|---|---|---|---|---|---|---|']
    for n, _k, _c in rows:
        L.append('| %s | $%s$ | %d | %d | %s | %s | %s |' %
                 (side[n], chan_tex(n), mult[n], give[n],
                  '✔' if crit[n][1] else '✘', slotex[CSPLIT['slotof'][n]],
                  '、'.join('情形 %s' % s for s in scn_of[n]) or '—'))
    L += ['', '两侧各自的合计就是 %(p4)d 与 %(p3)d（与 §7 的 `decomp` 路径逐条咬合，R9.0），'
          '而**表里的差别才是本节的内容**：%(open)s 是唯一"在场却不闭合"的道（$n_R=1$ 而 '
          '$n_Rn_{\\bar R}=0$），它正是 §6 里唯一能承载 $\\nu_R$ Majorana 质量的 '
          '$\\overline{126}_H$ 的伙伴 $\\Rightarrow$ 同一张道表里同时读到两件事："物质-only 的'
          '四费米子不变张量走哪两条道"与"$|\\Delta(B-L)|=2$ 那条道为什么进不来"。而 '
          '$\\overline{126}$ **已在登记表里** $\\Rightarrow$ "它不在 $16\\otimes16$ 里"是真的'
          '落空，不是查不到名字（R9.1）。闭合判据在六条道上各走两条不共享代码的路（标号自共轭 '
          'vs 直接解 $\\mathrm{mult}((1),R\\otimes R)$）且逐条一致 $\\Rightarrow$ "复表示的双线性'
          '凑不出不变张量"是**判出来的**，不是引来的。' % V, '',
          '$16^{\\otimes4}$ 的 %(p4)d 个不变张量**分处两条道**（%(clos)s），不是同一条道重数 2 '
          '$\\Rightarrow$ 证据是变异测试（R9.5）：把闭合道 $%(dnm)s$ 的重数翻倍，该道贡献按 '
          '$n_Rn_{\\bar R}$ 是 $2\\times2=4$ 而非 2 $\\Rightarrow$ 总数由 %(real)d 升到 %(dbl)d，'
          '即配对和**双线性**地依赖成分表（若它只数"有没有"，翻倍不会改变任何数）；从道表里'
          '删掉 $120$ $\\Rightarrow$ 掉到 %(drop)d；伪造 $\\overline{126}$ 也在 $16\\otimes16$ 里 '
          '$\\Rightarrow$ $126$ 与 $\\overline{126}$ 互配各得 1，总数升到 %(fake)d。' % V, '',
          '两条闭合道还**不在同一个双线性槽里**：$\\mathrm{Sym}^2(16)=10\\oplus126$ 而 '
          '$\\wedge^2(16)=120$（两个槽由 Adams $\\psi_2$ 算出，与直接做 $\\chi_{16}^2$ 的'
          '那条路不共享代码，且两者逐权重相加恰为 $16\\otimes16$）$\\Rightarrow$ $16^{\\otimes4}$ '
          '的两个不变张量一个来自"对称槽 $\\times$ 对称槽"、一个来自"反对称槽 $\\times$ 反对称槽"。'
          '同在对称槽里的 $10$ 与 $126$ 一个闭合一个不闭合 $\\Rightarrow$ 不存在"对称槽里都闭合"这种'
          '捷径。此处 Sym/∧ 说的是 $SO(10)$ 指标槽的对称性，**不是** Lorentz 或味指标。', '',
          '**插入 Higgs 能把这件事做到什么程度**（R9.4）。$|\\Delta(B-L)|=2$ 的那个 Higgs '
          '**插不进**四费米子算符：', '',
          '| 待插入 | $\\mathrm{mult}((1),16^{\\otimes4}\\otimes H)$：结合 I／结合 II／逐道 CG '
          '| 道对直解（不超过 %(cap)d 个权重者） |' % V, '|---|---|---|']
    for key, lab in (('126', '$H=126$'), ('126̄', '$H=\\overline{126}$')):
        v = CSPLIT['ins'][key]
        L.append('| %s | %d／%d／%d | 直解 %d 道且逐道与 CG 数相等，另 %d 道超出成本上限 |' %
                 (lab, v['gI'], v['gII'], v['gIII'], v['small'],
                  len(v['direct']) - v['small']))
    L += ['', '而插入**一对**之后单态个数确实非零，且共轭镜像再压一条独立约束：把全部 $16$ 换成 '
          '$\\overline{16}$、$126$ 换成 $\\overline{126}$ 后数出的同一个量，必须与**共轭那一行**的'
          '直接读数相等（下表第 4 列与第 2 列交叉相等）$\\Rightarrow$ "要拿到 $|\\Delta(B-L)|=2$ '
          '的四费米子不变张量就得成对插入"是本层数出来的，不是引用的：', '',
          '| 成对插入 | 结合 I | 结合 II | 共轭镜像 |', '|---|---|---|---|']
    for k in ('126|126', '126̄|126̄', '126|126̄'):
        v = CSPLIT['pairs'][k]
        L.append('| $16^{\\otimes4}\\otimes%s$ | %d | %d | %d |' %
                 ('\\otimes'.join(chan_tex(x) for x in k.split('|')), v['gI'], v['gII'],
                  v['mirror']))
    L += ['', '**与链探针声明的标量内容对账**（R9.3，权重与情形文字现场读取）。两件事必须同时'
          '成立，而它们指向不同的方向：', '',
          '| 道 | 是否闭合 | $\\Phi(1,2,2)$ 的权重全在此道 | $\\Sigma(1,1,3)_0$ 的权重全在此道 '
          '| 情形文字声明母表示 |', '|---|---|---|---|---|']
    for n, _k, _c in rows:
        x = cont[n]
        L.append('| $%s$ | %s | %s（%d／%d） | %s（%d／%d） | %s |' %
                 (chan_tex(n), '闭合' if x['closes'] else '**不闭合**',
                  '✔' if x['phi'] else '✘', x['nphi'], x['tphi'],
                  '✔' if x['sig'] else '✘', x['nsig'], x['tsig'],
                  '、'.join('情形 %s' % s for s in scn_of[n]) or '—'))
    L += ['', '**(a) 权重包含在同侧是退化的**：$\\Phi(1,2,2)$ 的全部 %(nphi)d 条权重同时落在 '
          '%(phi)s 的权重集里，$\\Sigma(1,1,3)_0$ 的全部 %(nsig)d 条同时落在 %(sig)s 里 '
          '$\\Rightarrow$ 包含判据能分"手征侧 vs 对消侧"，**分不了同侧内部是哪一道** '
          '$\\Rightarrow$ "道 $\\to$ 母表示"的指派是模型的**输入**（写在情形文字里），不是权重'
          '算出来的结论。**(b) 一旦指派由情形给定，闭合道里有没有母表示就是可数的**：三个情形'
          '字面声明的母表示并集为 %(decl)s（%(sci)s）$\\Rightarrow$ 两条闭合的手征道里**恰有一个**'
          '（$10$ 道）在谱里有母表示，另一个需要 $120_H$ 而**无人声明** $\\Rightarrow$ 在 '
          '$16^{\\otimes4}$ 的 %(p4)d 个不变张量里，一个可经模型声明有的 $10_H$ 因子化、另一个'
          '没有可用的媒介者 $\\Rightarrow$ "物质-only 四费米子算符有两条道"与"这两条道在本模型谱里'
          '有没有媒介者"是两个独立读数：前者是群论，后者是模型输入。' % V, '',
          '**本节第一次把配对和改走标号路径**，原因值得写进报告：登记表只覆盖 $\\dim\\le210$，'
          '"按名字查共轭"在登记范围外会把**真实存在**的共轭伙伴静默算成 0。在 '
          '$16^{\\otimes4}\\otimes126^{\\otimes2}$ 这张有 %(unreg)d 条登记范围外标号的表上，'
          '按标号算得 %(lab)d、按名字查得 %(byname)d $\\Rightarrow$ 差额是**视力**问题不是数学'
          '分歧。反向核验同时在场：在 §7 的 R8.2 用到的那三张表上（没有登记范围外的标号）两条路'
          '给出**同一个数** $\\Rightarrow$ 旧读数没有被改，只是它的**适用边界**现在被量出来了。' % V,
          '',
          '**本节的边界**（不进门禁，故明写）：', '',
          '* 数的是**规范不变张量**，不是物理算符：四个 $16_F$ 落到真实拉氏量还要过 Lorentz 指标、'
          '代（味）指标与 Fierz 恒等式三关 $\\Rightarrow$ "某道闭合"**不等于**"有一个算符"，'
          '本节的数**不**回填进 $\\tau_p$ 的任何计算（$\\tau_p$ 只由 [SO(10) 链统一报告]'
          '(SO10链统一报告.md) 的那套口径给出）。',
          '* "单态为 0"只说**这一个**乘积里没有不变方向：它**不**否定 $|\\Delta(B-L)|=2$ 的'
          '过程存在 $\\Rightarrow$ 传播子、$\\langle\\Delta_R\\rangle$ 的插入与有效算符的匹配都在'
          '本节之外（成对插入那一行的非零读数就是本节内的对照）。',
          '* 未登记标号只影响**名字**不影响**计数**：$\\mathrm{mult}((1),V)$ 只要求解出 $(1)$ 的'
          '重数，而 `decomp` 的整权重重构对账把整张多重集都核对了一遍。',
          '* "闭合""允许"都是群论陈述，**不**等于自然界里有这个场；标量谱本身仍是手工放置的 '
          '$\\Rightarrow$ **L10 未关闭**（系数、位势、味结构仍未算）。', '']
    return L


RESID = {}


def ztex(n):
    r"""残留群的阶 → $\mathbb{Z}_N$；没读到数就不印符号（不让排版冒充结论）。"""
    return ('$\\mathbb{Z}_{%d}$' % n) if n else '—'


def bl_values(nm):
    """表示 `nm` 的权重在 $B-L$ 方向上取到的荷（精确有理、升序去重）。"""
    return sorted(set(chg(w, BL) for w in irrep(NAMED[nm])[1]))


def rat_gen(vals):
    r"""有理数集的 $\mathbb{Z}$-生成元：分子的 gcd 除以分母的 lcm（0 不参与）。"""
    num, den = 0, 1
    for v in vals:
        if v == 0:
            continue
        num = math.gcd(num, abs(v.numerator))
        den = den * v.denominator // math.gcd(den, v.denominator)
    return F(num, den)


def string_pq(ms, lam, beta):
    r"""$\langle\lambda,\beta^\vee\rangle$：沿根 $\beta$ 的串 $\lambda-p\beta,\ldots,\lambda+q\beta$
    给出 $p-q$（向下步数减向上步数）。

    `string_len` 只给串的**总长**（$p+q+1$），拿不到 Dynkin 标号 $p-q$ $\Rightarrow$ 这里分开数。
    """
    up = 0
    while add(lam, smul(up + 1, beta)) in ms:
        up += 1
    dn = 0
    while sub(lam, smul(dn + 1, beta)) in ms:
        dn += 1
    return dn - up


def neutral_singlets(nm):
    """`nm` 里"色单态且 $Q=0$"的权重所带的 $B-L$ 值 $=$ 不破电磁的候选 v.e.v. 荷。"""
    ms = irrep(NAMED[nm])[1]
    return sorted(set(chg(l, BL) for l in ms
                      if color_singlet_wt(ms, l) and chg(l, QHP) == 0))


def residual_order(qd, g0):
    """路径甲：破缺场荷为 `qd` 时 $U(1)_{B-L}$ 的残留阶 $=q_\\Delta/g_0$；不给整数就不给数。"""
    if not g0:
        return 0
    n = F(qd) / g0
    return int(n) if n.denominator == 1 else 0


def residual_els(qd, g0):
    r"""路径甲的残留群元（以 $2\pi$ 为单位）：$\alpha_n=2\pi n/q_\Delta$，$n=0..N-1$。"""
    return [F(k) / F(qd) for k in range(residual_order(qd, g0))]


def survive(els, q2):
    r"""再放一个荷为 `q2` 的 v.e.v. 后还留着的群元数（精确）：$e^{i\alpha q_2}=1$。"""
    return sum(1 for a in els if (a * F(q2)).denominator == 1)


def survive_scan(els, q2):
    r"""同题的第二条路径：把每个残留元代回 $e^{i\alpha q_2}$ 用浮点判是否等于 1。"""
    c = 0
    for a in els:
        ang = 2.0 * math.pi * float(a) * float(q2)
        if abs(math.sin(ang)) < 1e-9 and math.cos(ang) > 1.0 - 1e-9:
            c += 1
    return c


def scan_order(qd, g0, sub=288):
    """路径乙：圆周均分 `sub` 份，逐点数出让 `qd` 平凡的角度（纯浮点，不做有理运算）。"""
    qn = float(F(qd) / g0)
    ang = [2.0 * math.pi * k * qn / sub for k in range(sub)]
    ks = [k for k, a in enumerate(ang)
          if abs(math.sin(a)) < 1e-9 and math.cos(a) > 1.0 - 1e-9]
    return len(ks), ks


def scan_period(charges, per_step=120, upto_pi=12):
    r"""路径乙的另一半：**只从荷集**测出"对所有荷都平凡"的最小正角（单位 $\pi$）。"""
    vals = [float(q) for q in charges]
    for m in range(1, int(upto_pi * per_step) + 1):
        a = math.pi * m / per_step
        if all(abs(math.sin(a * v / 2.0)) < 1e-9 for v in vals):
            return F(m, per_step)
    return None


def mp_parity(q):
    r"""物质字称候选元 $(-1)^{3(B-L)}$ 在荷 `q` 上的取值；$3q$ 不是整数时不赋值。"""
    n = 3 * F(q)
    return None if n.denominator != 1 else (-1 if n.numerator % 2 else 1)


def run_residual_layer():
    """R10：$B-L$ 被破缺之后残留哪个离散规范对称性（荷格 + 两条独立路径 + 约定无关性）。

    本节存在的理由是一条**审计发现**：报告曾在四处写着"$|\\Delta(B-L)|=1$ 单步破缺
    $\\Rightarrow$ 残留 $\\mathbb{Z}_2$（物质字称）"（§0 结论一览、§4 第 7 条、R5.5 与 R5.9 的判据文字），
    而守这句话的门禁 R5.9 的读数是
    $(B-L,\\ SU(2)_L\\text{ 串长},\\ SU(2)_R\\text{ 串长})$ 三元组 $\\Rightarrow$ "残留群"这三个字
    从来没有被算过。三条路径同数才认：
      甲 精确有理：荷格生成元 $g_0$（分子 gcd／分母 lcm）$\\Rightarrow$ 圆周
        $\\alpha_0=2\\pi/g_0$、残留阶 $N=q_\\Delta/g_0$；
      乙 浮点几何：把圆周均分后逐点数 $\\alpha$ 使 $e^{i\\alpha q_\\Delta}=1$，并且**只从权重**
        独立测出 $\\alpha_0$；
      丙 约定无关：全套荷同乘 $1/2$（改用 $Y_{B-L}=(B-L)/2$ 的记号）$N$ 必须不动 $\\Rightarrow$
        残留群是一个群的子群，不是记号的函数。
    """
    p = True
    names = [r['name'] for r in TABLE if r['name'] in NAMED]
    bls = dict((nm, bl_values(nm)) for nm in names)
    neut = dict((nm, neutral_singlets(nm)) for nm in names)
    g0_m = rat_gen(bls['16'])
    g0_all = rat_gen([q for nm in names for q in bls[nm]])
    # 候选 v.e.v. 的荷：色单态、$Q=0$、且 $B-L\\neq0$（等于 0 的那些根本不碰 $U(1)_{B-L}$）
    qd = sorted(set(abs(v) for nm in names for v in neut[nm] if v != 0))
    allq = [q for nm in names for q in bls[nm]]
    per_scan = scan_period(allq)
    rows = []
    for v in qd:
        els = residual_els(v, g0_all)
        n = len(els) or 1
        # 2 阶元 = 群参数 $k$ 满足 $2k\equiv0\pmod N$ 而 $k\not\equiv0$ 的那个元（$N$ 偶时唯一）
        o2 = [a for k, a in enumerate(els) if k and (2 * k) % n == 0]
        cos = [int(round(math.cos(2.0 * math.pi * float(o2[0]) * float(q)))) for q in bls['16']] \
            if len(o2) == 1 else []
        rows.append({'BL': str(v),
                     'carriers': [nm for nm in names if v in [abs(x) for x in neut[nm]]],
                     'N': len(els), 'N_scan': scan_order(v, g0_all)[0],
                     'N_half': residual_order(v / 2, g0_all / 2),
                     'N_mismatch': residual_order(v / 2, g0_all),
                     'N_naive': residual_order(v, F(1)),
                     'mp': mp_parity(v), 'ord2': str(o2[0]) if len(o2) == 1 else '无',
                     'ord2_is_mp': bool(cos) and cos == [mp_parity(q) for q in bls['16']],
                     'ew': survive(els, 0), 'ew_scan': survive_scan(els, 0),
                     'ctl': survive(els, v / 2), 'ctl_scan': survive_scan(els, v / 2)})
    RESID.update({'g0_matter': str(g0_m), 'g0_all': str(g0_all), 'nrep': len(names),
                  'period_scan': str(per_scan), 'period_exact': str(F(2) / g0_all),
                  'rows': rows, 'neut': dict((k, [str(x) for x in v]) for k, v in neut.items()),
                  'bls': dict((k, [str(x) for x in v]) for k, v in bls.items())})

    # ---- R10.0 荷格由**物质**单独定死，加入任何在场标量都不扩大
    p &= exact('R10.0', '在场全部 $B-L$ 荷生成的格 $g_0$：只看 $16_F$ 是 $1/3$，把 $\\dim\\le210$ '
                        '的 11 个表示全加进来还是 $1/3$ $\\Rightarrow$ 圆周长度不是"选了哪个标量谱" '
                        '的函数，物质就把格定死了',
               [g0_m, g0_all], [F(1, 3), F(1, 3)],
               '各表示自己的生成元：%s' % '、'.join(
                   '%s：%s' % (tex_name(nm), rat_gen(bls[nm])) for nm in names))

    # ---- R10.1 圆周：浮点只从权重测出的最小平凡角 = 精确值 $2\\pi/g_0$
    p &= exact('R10.1', '路径乙独立测出的"对所有在场荷都平凡的最小正角"（单位 $\\pi$）与路径甲的 '
                        '$2/g_0$ 相等 $\\Rightarrow$ $U(1)_{B-L}$ 的周期是**量出来的**，'
                        '不是从"通常把 $B-L$ 规范化成……"抄来的',
               [str(per_scan), str(F(2) / g0_all)], ['6', '6'],
               '浮点扫描步长 $\\pi/120$，扫到 $12\\pi$ 为止；测得的周期以 $\\pi$ 为单位')

    # ---- R10.2 残留阶：两条路径对每一个候选荷同数
    p &= ok('R10.2', '对数据里出现的每一个候选破缺荷 $q_\\Delta$（色单态且 $Q=0$ 且 $B-L\\neq0$）， '
                     '精确路径给的残留阶 $N=q_\\Delta/g_0$ 与浮点枚举数出的平凡角度个数相等 $\\Rightarrow$ '
                     '"残留 $\\mathbb{Z}_N$"有两条不共享算术的出处',
            all(r['N'] > 0 and r['N'] == r['N_scan'] for r in rows) and bool(rows),
            '读数：%s' % [(r['BL'], r['N'], r['N_scan']) for r in rows])

    # ---- R10.3 2 阶元就是物质字称，且它把物质与标量分开
    ms16 = irrep(NAMED['16'])[1]
    mp16 = sorted(set(mp_parity(chg(l, BL)) for l in ms16))
    even = [nm for nm in names if all(mp_parity(q) == 1 for q in bls[nm])]
    odd = [nm for nm in names if nm not in even]
    RESID.update({'mp16': [str(x) for x in mp16], 'even': even, 'odd': odd})
    p &= ok('R10.3', '$(-1)^{3(B-L)}$ 这个候选元在 $16_F$ 的**每一条**权重上都取 $-1$（含 '
                     '$\\nu^c$ 与 $e^c$），而在表内其余表示的每一条权重上都取 $+1$：全偶的是 %s，'
                     '含奇分量的是 %s $\\Rightarrow$ 它是一个"物质奇、规范玻色子与这些标量偶"的 '
                     '$\\mathbb{Z}_2$ 分次，"标量一定偶"是**算出来**的而不是设定的（例外恰好落在'
                     '$16$ 型与 $144$ 型上）。另一半：$N$ 为偶那条通道里那个唯一的 2 阶元 $\\alpha$ '
                     '作用在 $16_F$ 各荷上，浮点算出的符号与 $(-1)^{3(B-L)}$ 逐荷相同 $\\Rightarrow$ '
                     '抽象分次与圆周上的那个元是同一个东西' % (plain_tex(even), plain_tex(odd)),
            mp16 == [-1] and all('16' not in nm and '144' not in nm for nm in even) and
            sorted(odd) == sorted(nm for nm in names if '16' in nm or '144' in nm) and
            all(r['ord2_is_mp'] for r in rows if r['ord2'] != '无') and
            any(r['ord2'] != '无' for r in rows),
            '偶侧 %d 个、奇侧 %d 个（共 %d 个表示）；$16_F$ 上的取值 %s；2 阶元对照：%s' %
            (len(even), len(odd), len(names), mp16,
             [(r['BL'], r['ord2'], '同' if r['ord2_is_mp'] else '不同')
              for r in rows if r['ord2'] != '无']))

    # ---- R10.4 3 阶元 = 色表示自己的 triality（符号由数据选定，不预设）
    pairs, sing_bad, nons_tri0, nonint = [], [], [], []
    for nm in names:
        ms = irrep(NAMED[nm])[1]
        for l in ms:
            t3 = 3 * chg(l, BL)
            if t3.denominator != 1:
                nonint.append(nm)
                continue
            t = int(t3) % 3
            p1, p2 = string_pq(ms, l, A2_C[0]), string_pq(ms, l, A2_C[2])
            col = p1 - p2                       # 该权重的色 Dynkin 标号差 $p-q$
            pairs.append((nm, t, col))
            if color_singlet_wt(ms, l) and t:
                sing_bad.append(nm)
            if not color_singlet_wt(ms, l) and col % 3 == 0:
                nons_tri0.append((nm, p1, p2))
    bad_p = sorted(set(nm for nm, t, c in pairs if t != c % 3))
    bad_m = sorted(set(nm for nm, t, c in pairs if t != (-c) % 3))
    sgn = '+' if (not bad_p and bad_m) else ('-' if (not bad_m and bad_p) else '不存在')
    RESID.update({'nwt': len(pairs), 'triality_sign': sgn, 'bad_plus': bad_p, 'bad_minus': bad_m,
                  'nonint': sorted(set(nonint)), 'singlet_nontrivial': sorted(set(sing_bad)),
                  'nonsinglet_trivial': sorted(set(nons_tri0))})
    p &= ok('R10.4', '残留群里那个**阶为 3** 的元作用在荷 $q$ 上只看 $3q\\bmod 3$。本节把它对到'
                     '**色表示自己的 triality** 上：对表内每条权重，$3(B-L)\\equiv s\\,(p-q)'
                     '\\pmod 3$，$(p,q)$ 是该权重的 $A_2$ Dynkin 标号，一致符号 $s=%s$ 由数据选定'
                     '（两种符号都测，只有一处无反例才通过 $\\Rightarrow$ 符号不是先验填进去的）。'
                     '$\\Rightarrow$ 那个 $\\mathbb{Z}_3$ **就是**按色 triality 计数的元。'
                     '两条对照同时印出：色单态必平凡（反例 %d 条），但反向**不成立**——非单态而 '
                     '$p-q\\equiv0$ 的（色八重态一类）也平凡，共 %d 条 $\\Rightarrow$ "按色三重态'
                     '计数 mod 3"作为口号只在 mod 3 意义下成立，逐字成立的是上面那条同余式' %
            (sgn, len(set(sing_bad)), len(set(nons_tri0))),
            sgn in ('+', '-') and not sing_bad and not nonint and bool(pairs),
            '权重 %d 条；一致符号 %s；$+$ 号反例 %s；$-$ 号反例 %s；$3(B-L)\\notin\\mathbb{Z}$ %s；'
            '非单态而 triality 平凡的（表示,$p$,$q$）：%s' %
            (len(pairs), sgn, bad_p, bad_m, RESID['nonint'], RESID['nonsinglet_trivial'][:6]))

    # ---- R10.5 |Δ(B−L)|=1 那条通道：留 Z3，物质字称被它自己破掉
    r1 = next((r for r in rows if r['BL'] == '1'), None)
    p &= ok('R10.5', '$|\\Delta(B-L)|=1$ 的破缺（承载者见 R5.9：$16_H/\\overline{16}_H$、'
                     '$144_H/\\overline{144}_H$）把 $U(1)_{B-L}$ 留成 $\\mathbb{Z}_3$：阶为奇 '
                     '$\\Rightarrow$ 里面**没有** 2 阶元，而 $(-1)^{3(B-L)}$ 在该 v.e.v. 上取 $-1$ '
                     '$\\Rightarrow$ 物质字称是**被这一步破掉的**，不是它留下的。本节据此改写了'
                     '此前写在 §0/§4 与 [09](../09_已知局限与否定清单.md) 的"残留 $Z_2$（物质字称）"，'
                     '并在 08 的证伪台账登记（那条"对质子稳定反而有利"随之失去前提）',
            r1 is not None and r1['N'] == 3 and r1['mp'] == -1 and r1['N'] % 2 == 1,
            '读数：$q_\\Delta=1$ $\\Rightarrow$ $N=%s$（浮点同 $%s$），物质字称在该荷上 $=%s$' %
            (r1 and r1['N'], r1 and r1['N_scan'], r1 and r1['mp']))

    # ---- R10.6 判据：物质字称存活 ⇔ $3q_\Delta$ 为偶（对数据里每个候选成立）
    p &= ok('R10.6', '把 R10.3 的分次与 R10.5 的判据合起来是一条可核对的 iff：残留 $\\mathbb{Z}_N$ '
                     '**含** 2 阶元（物质字称才可能存活）当且仅当 $N=q_\\Delta/g_0$ 为偶，'
                     '在数据里每个候选荷上逐个验，不靠"偶数阶群含 2 阶元"这一句代数当结论 $\\Rightarrow$ '
                     '它实际是把两个**独立实现**（$mp\\_parity$ 的奇偶判定与 $residual\\_order$ '
                     '的格算术）拴在一起。另一条同时成立的结构性读数：每个候选的 $N$ 都是 3 的倍数 '
                     '$\\Rightarrow$ 在这个物质内容下 3 阶元（色 triality）是**躲不掉的**，'
                     '条件性的只有 2 阶元那半边',
            all((r['N'] % 2 == 0) == (r['mp'] == 1) and r['N'] % 3 == 0 for r in rows) and
            len(rows) >= 2,
            '读数（$q_\\Delta$, $N$, $N\\bmod 2$, $N\\bmod 3$, 物质字称）：%s' %
            [(r['BL'], r['N'], r['N'] % 2, r['N'] % 3, r['mp']) for r in rows])

    # ---- R10.7 约定无关 + R10.8 植入缺陷（断言必须是活的）
    p &= ok('R10.7', '把全套荷换成 $Y_{B-L}=(B-L)/2$ 的约定（分子分母同缩 $1/2$）后，每个候选的 '
                     '残留阶 $N$ 一个都不动 $\\Rightarrow$ 本节读的数不依赖 $B-L$ 的归一化选择',
            all(r['N_half'] == r['N'] for r in rows) and bool(rows),
            '两套约定下的残留阶：%s' % [(r['BL'], r['N'], r['N_half']) for r in rows])
    p &= ok('R10.8', '植入检验（两种典型记号滑倒，都必须在读数上留下痕迹）：'
                     '(i) **只**把 $q_\\Delta$ 减半、不同步缩荷格 $\\Rightarrow$ 残留阶要么被腰斩、'
                     '要么根本不再是整数（工具拒绝给数，读成 0）；'
                     '(ii) 误把圆周当 $2\\pi$（即默认荷格是 $\\mathbb{Z}$，$g_0=1$）$\\Rightarrow$ '
                     '残留阶退化成 $q_\\Delta$ 本身。第二个读数正是旧散文挂在 $|\\Delta(B-L)|=1$ '
                     '通道上的那个 $\\mathbb{Z}_2$ 的来源 $\\Rightarrow$ "残留 $\\mathbb{Z}_2$"'
                     '既是归一化滑倒的产物，又张冠李戴到了另一条通道上（正确算术里 2 阶元只存在于 '
                     '$q_\\Delta=2$ 那条通道，且是 $\\mathbb{Z}_6$ 的一个因子而非整个残留群）',
            all(r['N_mismatch'] != r['N'] and r['N_mismatch'] in (0, r['N'] // 2) and
                r['N_naive'] != r['N'] == r['N_scan'] for r in rows) and
            all(r['N_naive'] == int(F(r['BL'])) for r in rows) and
            any(r['N_mismatch'] == 0 for r in rows) and len(rows) >= 2,
            '正确（甲／乙）%s；只缩 $q_\\Delta$ %s；误取 $2\\pi$ 周期 %s' %
            ([(r['BL'], r['N'], r['N_scan']) for r in rows],
             [(r['BL'], r['N_mismatch']) for r in rows],
             [(r['BL'], r['N_naive']) for r in rows]))

    # ---- R10.9 后续弱电破缺用 $B-L=0$ 的分量 ⇒ 残留群活到低能（带一个会受损的对照）
    ew = [nm for nm in names if F(0) in neut[nm]]
    RESID.update({'ew_neutral': ew})
    ewtex = '、'.join(tex_name(n) for n in ew) or '无'
    p &= ok('R10.9', '在 $\\dim\\le210$ 里"色单态、$Q=0$、$B-L=0$"的候选非空（表内：%s）$\\Rightarrow$ '
                     '用这类分量再破 $SU(2)_L\\times U(1)_Y$ 时，v.e.v. 对 $U(1)_{B-L}$ 恒等。'
                     '这条判据不是"$0\\cdot\\alpha=0$ 故平凡"那样的恒真式：把每个残留元代回 '
                     '$e^{i\\alpha q_2}$ 逐元计数，$q_2=0$ 时**一个都不少**，而同一条通道上取 '
                     '$q_2=q_\\Delta/2$ 的对照 $\\Rightarrow$ 元数**减少** $\\Rightarrow$ "弱电那一步'
                     '不削弱残留 $\\mathbb{Z}_N$"是一条有对照的读数，不是套话' % ewtex,
            bool(ew) and all(r['ew'] == r['N'] and r['ew'] == r['ew_scan'] and
                             r['ctl'] < r['N'] and r['ctl'] == r['ctl_scan'] for r in rows),
            '读数（$q_\\Delta$, 残留阶 $N$, 加 $q_2=0$ 后剩, 加对照 $q_2=q_\\Delta/2$ 后剩）：%s' %
            [(r['BL'], r['N'], r['ew'], r['ctl']) for r in rows])

    # ---- R10.10 条件性：三个情形的字面标量谱里两条通道都没有母表示
    decl = dict(CSPLIT['decl'])
    dunion = set(CSPLIT['decl_union'])
    lit = dict((nm, dict((k, '%s_H' % nm in txt and '无 $%s_H$' % nm not in txt)
                         for k, txt in chain.SCENARIOS.items()))
               for nm in ('16', '126'))
    RESID.update({'decl': decl, 'decl_16': lit['16'], 'decl_126': lit['126'],
                  'cond': [(r['BL'], sorted(set(r['carriers']) & dunion)) for r in rows]})
    p &= ok('R10.10', '本节两个残留群都是**条件读数**：承载 $|\\Delta(B-L)|=2$ 的 $126_H/'
                      '\\overline{126}_H$ 与承载 $|\\Delta(B-L)|=1$ 的 $16_H/\\overline{16}_H$ '
                      '都**不在**链探针三个情形字面声明的标量谱里（情形文字现场读，判法与 R9.3 '
                      '同一条：出现 "$X_H$" 且未写"无 $X_H$"）。把每个候选荷的承载者与"链上字面'
                      '声明的母表示"求交 $\\Rightarrow$ 两条通道的交集都是空集 $\\Rightarrow$ '
                      '"残留 %s"要读成"若补上 $126_H$ 并让它取 $B-L=2$ 的中性分量"，'
                      '不是"本模型已经如此"' % ztex(residual_order(F(2), g0_all)),
            not any(lit['16'].values()) and not any(lit['126'].values()) and
            bool(lit['16']) and bool(lit['126']) and all(not c for _b, c in RESID['cond']),
            '各情形字面声明的母表示：%s；含 $16_H$：%s；含 $126_H$：%s；承载者 ∩ 声明谱：%s' %
            (decl, lit['16'], lit['126'], RESID['cond']))
    return p


# =============================================================== R11：低能算符的选择定则
# 低能投影用的子系统：$SU(3)_c\times SU(2)_L$ 的根，额外方向取 $Y$（**不是** $B-L$）。
# 为什么不能沿用 3221 去数"零权"：$Y$ 与 $T^3_R$ 不正交（R11.0 当场量那个内积）$\Rightarrow$
# 沿 3221 的零权要求 $T^3_R=0$ 且 $B-L=0$，会把"$SU(3)\times SU(2)_L\times U(1)_Y$ 单态但
# $B-L\ne0$"的场（$\nu^c$ 就是这一个）整个漏掉。
SUB_321 = None
if BL is not None:
    SUB_321 = Subsystem('321', [sub(EPS[0], EPS[1]), sub(EPS[1], EPS[2]), A1_L], extra=YHP)

SEL = {}

# 物质场名字**由签名绑定**：键 $=(\\lambda_{321},\\ Y,\\ B-L)$ 全是量出来的（引擎号），
# 值只是一个标签。这张表可证伪的地方在 R11.3：它必须与量出来的 6 个签名一一对应，且把 $Y$
# 从键里去掉就不再单射（$u^c,d^c$ 与 $e^c,\\nu^c$ 各自占在同一个 (色,弱) 格上）。
MATTER_SIG = {((0, 0, 0), F(-1), F(-1)): 'e^c',
              ((0, 0, 0), F(0), F(-1)): '\\nu^c',
              ((1, 0, 1), F(-1, 6), F(-1, 3)): 'Q',
              ((0, 1, 0), F(-1, 3), F(1, 3)): 'd^c',
              ((0, 1, 0), F(2, 3), F(1, 3)): 'u^c',
              ((0, 0, 1), F(1, 2), F(1)): 'L'}


def sm_slice(ms, y):
    r"""$Y$ 切片：权重多重集里 $Y=y$ 的那部分 $=$ 低能投影该用的 projector。"""
    return dict((mu, k) for mu, k in ms.items() if chg(mu, YHP) == y)


def sm_mult(ms, lam):
    r"""Klimyk 的 very old rule 限制到 $SU(3)_c\times SU(2)_L\times U(1)_Y$：$\lambda$ 在 `ms`
    （必须是**同一** $Y$ 切片）里的重数。

    $U(1)_Y$ 与本子系统的根正交（`Subsystem` 构造时那条断言）$\Rightarrow$ Weyl 轨道不离开切片，
    先切片再作交错和是合法的。算出负重数即报错，不静默丢弃。
    """
    book = {}
    for mu, k in ms.items():
        lab = SUB_321.labels(mu)
        book[lab] = book.get(lab, 0) + k
    tgt = add(sub_label_to_wt(SUB_321, lam), SUB_321.rho)
    tot = 0
    for M, sg in SUB_321.W.items():
        tot += sg * book.get(SUB_321.labels(sub(mat_vec(M, tgt), SUB_321.rho)), 0)
    assert tot >= 0, 'SM 重数为负（%s）⇒ 321 子系统构造有误' % (lam,)
    return tot


def sm_singlet_mult(ms):
    r"""低能规范不变张量个数 $\mathrm{mult}((1)_{321},V)$。"""
    return sm_mult(sm_slice(ms, F(0)), (0, 0, 0))


def sm_zero_ms(ms):
    """把"低能单态"错当成"3221 的零权"来数的那条路 $=$ 被本节否证的 projector（留作对照）。"""
    return zero_wt(ms)


def sm_dim(lam):
    r"""$\dim(SU(3)_c)\times\dim(SU(2)_L)$：$A_2$ 走闭式维数公式，$A_1$ 走 $j\mapsto2j+1$。"""
    return dim3(*lam[:2]) * (lam[2] + 1)


def sm_content(ms):
    r"""完整 SM 分解 $[(\lambda,Y,n)]$ 与维数账 $(\sum n\dim_{\mathrm{SM}},\\ \text{权重数})$。"""
    ys = sorted(set(chg(mu, YHP) for mu in ms))
    cands = sorted(set(SUB_321.labels(mu) for mu in ms))
    rows, tot = [], 0
    for y in ys:
        sl = sm_slice(ms, y)
        for lab in cands:
            if min(lab) < 0:
                continue
            n = sm_mult(sl, lab)
            if n:
                rows.append((lab, y, n))
                tot += n * sm_dim(lab)
    book = msum(ms)
    rows.sort(key=lambda r: (str(r[0]), str(r[1])))
    return rows, tot == book, book, tot


def sm_conj(lam):
    r"""$\lambda\mapsto\lambda^*$：$A_2$ 标号倒序（与 `su_name` 同一规则），$A_1$ 自共轭。"""
    return (lam[1], lam[0], lam[2])


def sm_pair_singlets(ra, rb):
    r"""第二条独立路径：$\sum_{\lambda,Y}n^a_{\lambda,Y}\\,n^b_{\lambda^*,-Y}$，只查两因子各自
    已有的 SM 成分表 $\Rightarrow$ 不乘大乘积、不解方程组（与 `pair_singlets` 在 SO(10) 层同构）。"""
    book = dict(((l, y), n) for l, y, n in rb)
    return sum(n * book.get((sm_conj(l), -y), 0) for l, y, n in ra)


def perm_weight(combo, n):
    """多重集 $\\mapsto$ 它代表的**有序**组数 $=n!/\\prod_k(\\text{重数}!)$。"""
    w = math.factorial(n)
    for i in sorted(set(combo)):
        w //= math.factorial(combo.count(i))
    return w


def sm_fields(nm):
    """表示 `nm` 的低能场清单：每个 $(SU(3)_c,SU(2)_L,U(1)_Y)$ 分量一条，带上它自己的 $B-L$。

    同一条 $(\\lambda,Y)$ 可以来自两条 $B-L$ 不同的 3221 行 $\\Rightarrow$ 场的身份必须带 $B-L$，
    只带 SM 量子数不够。
    """
    ms = irrep(NAMED[nm])[1]
    out = []
    for row in branching(ms, SUB_3221):
        subms = sub_irrep(row['wt'], SUB_3221)
        for y in sorted(set(chg(mu, YHP) for mu in subms)):
            sl = sm_slice(subms, y)
            cont = sm_content(sl)[0]
            assert len(cont) == 1 and cont[0][2] == 1, \
                '%s 的行 %s 在 $Y=%s$ 切片上不是一条重数为 1 的 SM 不可约表示：%s' % (
                    nm, fmt_3221(row), y, cont)
            out.append({'rep': nm, 'lam': cont[0][0], 'Y': y, 'BL': row['bl'],
                        'ms': sl, 'row': fmt_3221(row), 'nwt': msum(sl)})
    return out


def f_bl(f):
    r"""场的 $B-L$（**教材号**）：本引擎的 $B-L$ 与文献整体反号，这一处符号在 R5.7/R6.6 已登记。"""
    return -f['BL']


def f_b(f):
    r"""重子数：由"色非单态者携带 $B$、色单态者不携带"这条规则从量出来的 $(\mathrm{色},B-L)$ 派生。"""
    return f_bl(f) if f['lam'][:2] != (0, 0) else F(0)


def f_l(f):
    r"""轻子数：同一规则的另一半 $=$ "色单态者携带 $L=-(B-L)$"。"""
    return F(0) if f['lam'][:2] != (0, 0) else -f_bl(f)


def f_tri(f):
    r"""该场的 $\mathbb{Z}_3$ 荷（色 triality）$3(B-L)\bmod 3$；无整数 $3(B-L)$ 即不给数。"""
    t3 = 3 * f_bl(f)
    return None if t3.denominator != 1 else int(t3) % 3


def sel_ms(fl):
    ms = fl[0]['ms']
    for f in fl[1:]:
        ms = tprod(ms, f['ms'])
    return ms


def sel_t3q(fl):
    r"""单项式的 $3Q=\sum_k3(B-L)_k$：以 $g_0=1/3$ 为单位的**整数**荷计数（不是浮点）。"""
    return sum(3 * f_bl(f) for f in fl)


def rule_exact(t3, n):
    r"""路径甲：$N\mid 3Q$。$3Q$ 非整数或 $N\le0 $（工具没读到群）$\Rightarrow$ 不给判决。"""
    if n <= 0 or t3.denominator != 1:
        return None
    return int(t3) % n == 0


def rule_els(qd, g0, q):
    r"""路径乙：把每个残留群元 $\alpha_k=k/q_\Delta$ 代回 $e^{2\pi i\alpha_kQ}$，逐元要它 $=1$
    （精确有理：判 $\alpha_kQ$ 的分母）$\Rightarrow$ 不写整除式。"""
    els = residual_els(qd, g0)
    return None if not els else all((a * q).denominator == 1 for a in els)


def rule_float(qd, g0, q):
    r"""路径丙：同一题的浮点实现——走 $\sin/\cos$，不碰有理数的分母，也不碰整除。"""
    els = residual_els(qd, g0)
    if not els:
        return None
    for a in els:
        ang = 2.0 * math.pi * float(a) * float(q)
        if not (abs(math.sin(ang)) < 1e-9 and math.cos(ang) > 1.0 - 1e-9):
            return False
    return True


def rule_factors(t3):
    r"""因子逐点判：$\mathbb{Z}_3$ 那半边只看 $3Q\bmod 3$，$\mathbb{Z}_2$ 那半边只看 $3Q\bmod 2$。"""
    if t3.denominator != 1:
        return (None, None)
    return (int(t3) % 3 == 0, int(t3) % 2 == 0)


def sel_cand(fl, chans, g0):
    """一个候选算符的全部读数：SM 单态数、荷账、$\\Delta B/\\Delta L/\\Delta(B-L)$、色侧荷和、三条路径的判决。"""
    ms = sel_ms(fl)
    t3 = sel_t3q(fl)
    q = t3 / 3
    nf = sum(1 for f in fl if not f.get('boson'))
    out = {'fl': [f.get('name', f['rep']) for f in fl],
           'combo': tuple(f['rep'] for f in fl),
           'sig': '+'.join('%s[%s|%s|%s]' % (f.get('name', f['rep']), f['lam'], f['Y'], f['BL'])
                           for f in fl),
           'nf': nf, 'ns': len(fl) - nf,
           'd': F(3 * nf, 2) + len(fl) - nf,
           'singlet': sm_singlet_mult(ms), 'zero': sm_zero_ms(ms),
           't3q': str(t3), 'q': str(q),
           'dB': str(sum(f_b(f) for f in fl)), 'dL': str(sum(f_l(f) for f in fl)),
           'tri': sum(f['lam'][0] - f['lam'][1] for f in fl),
           'odd': bool(nf % 2), 'v': {}, 'mut': {}}
    for tag, (qd, n) in chans.items():
        v = {'甲': rule_exact(t3, n), '乙': rule_els(qd, g0, q), '丙': rule_float(qd, g0, q)}
        z3, z2 = rule_factors(t3)
        v['Z3'] = z3
        v['Z2'] = z2
        vs = [v['甲'], v['乙'], v['丙']]
        v['甲乙丙一致'] = None in vs or len(set(vs)) == 1
        v['因子与'] = None in (z3, z2) or (z3 and z2) == v['甲']
        out['v'][tag] = v
    return out


def run_selection_layer():
    r"""R11：残留离散规范对称性在**低能算符**上的选择定则（08 的 P7 一节末尾登记的那条待办）。

    R10 数出了群里有哪些元，但没有回答"它禁哪些算符"——那一句当时登记为待办。本节把它变成
    格上的读数，四步走：
      (a) 先把低能投影的 projector 钉对：$Y$ 与 $T^3_R$ 不正交 $\Rightarrow$ 沿 3221 数零权会
          漏掉 $\nu^c$（R11.0/R11.1），再把 $\mathbb{Z}_3$ 的荷对到色 triality 上**逐场**核（R11.2）；
      (b) 场清单本身由签名绑定（R11.3），$B/L$ 按"色携带 $B$、单态携带 $L$"这一条规则派生（R11.4）；
      (c) 枚举候选算符并逐条判决（R11.5–R11.8），直接回答"残留群保不保质子"；
      (d) 正对照与变异测试（R11.9）：$\text{禁掉 }0\text{ 条}$ 必须与 $\text{枚举到 }0\text{ 条}$
          可区分。
    选择定则本身只用一条同余式：总荷 $Q=\sum_k(B-L)_k$ 的算符在 $\mathbb{Z}_N$（$N=q_\Delta/g_0$）
    下不变 $\iff$ $N\mid 3Q$，三条互不共享算术的实现（整除、群元逐元、浮点角度）必须同判决。
    """
    p = True
    g0 = rat_gen(bl_values('16'))
    chans = dict(('|%s|' % r['BL'], (F(r['BL']), r['N'])) for r in RESID['rows'])
    names = [r['name'] for r in TABLE if r['name'] in NAMED]

    # ---- R11.0 projector：$Y$ 与 $T^3_R$ 不正交 ⇒ 3221 的"零权"不是低能单态
    iply, ipry = ip(A1_L, YHP), ip(A1_R, YHP)
    ms16 = irrep(NAMED['16'])[1]
    nu = [f for f in sm_fields('16') if f['lam'] == (0, 0, 0) and f['Y'] == 0]
    SEL.update({'proj': {'ip': (iply, ipry), 'zw16': zero_wt(ms16), 'nsing': len(nu),
                         'nu': (nu[0]['row'], nu[0]['BL']), 'pos': len(SUB_321.pos),
                         'W': len(SUB_321.W), 'rho': SUB_321.rho, 'g0': str(g0)}})
    p &= ok('R11.0', '低能投影的 projector 先要选对。$SU(2)_L$ 的单根与 $Y$ 正交（内积 $=%s$）'
                     '而 $SU(2)_R$ 的单根与 $Y$ **不**正交（$=%s\\ne0$）$\\Rightarrow$ $U(1)_Y$ 与 '
                     '$SU(2)_R$ 混在一起，沿 3221 数"零权"等于额外要求 $T^3_R=0$ 且 $B-L=0$。'
                     '后果是具体的：$16_F$ 的权重里**没有**零权（荷账本 $=%d$），但它有 %d 个'
                     '$SU(3)\\times SU(2)_L\\times U(1)_Y$ 单态，就是 $\\nu^c$——它的 $B-L=1$、'
                     '$T^3_R\\ne0$ $\\Rightarrow$ 用"零权"当 projector 会把承载 Majorana 质量的那个'
                     '场整个漏掉。本节据此把全部低能计数放在子系统 $SU(3)_c\\times SU(2)_L$ 配 '
                     '$U(1)_Y$（`SUB_321`）的 $Y$ 切片上' % (iply, ipry, zero_wt(ms16), len(nu)),
            iply == 0 and ipry != 0 and zero_wt(ms16) == 0 and len(nu) == 1 and
            len(SUB_321.pos) == 4 and len(SUB_321.W) == 12 and
            str(g0) == RESID['g0_all'] == RESID['g0_matter'],
            '$|\\Delta_+|$=%d，$|W|$=%d，$\\rho_{321}=%s$；荷格 $g_0=%s$（与 R10.0 同一条读数）；'
            '$\\nu^c$ 那一条的 3221 行 $=%s$，引擎号 $B-L=%s$' %
            (len(SUB_321.pos), len(SUB_321.W), SUB_321.rho, g0, nu[0]['row'], nu[0]['BL']))

    # ---- R11.1 SM 分解的维数账 + 植入缺陷（不按 $Y$ 切片会怎样）
    books = []
    for nm in ('10', '16', '45', '54'):
        ms = irrep(NAMED[nm])[1]
        rows, eq, book, tot = sm_content(ms)
        cands = [lab for lab in sorted(set(SUB_321.labels(mu) for mu in ms)) if min(lab) >= 0]
        noslice = sum(len(set(chg(mu, YHP) for mu in ms)) * n * sm_dim(lab)
                      for lab in cands for n in [sm_mult(ms, lab)] if n)
        books.append((nm, len(rows), tot, book, eq, noslice))
    SEL.update({'books': books})
    p &= ok('R11.1', 'SM 分解的实现由**维数账**独立核对：$\\sum_\\lambda n_\\lambda'
                     '\\dim_{\\mathrm{SM}}(\\lambda)=\\dim$（Weyl 维数）逐表示成立：%s。'
                     '植入缺陷：把"先按 $Y$ 切片"这一步去掉、直接在整个多重集上作同一条 Klimyk '
                     '交错和，四个表示的账**全部**立刻不平（右列是那个错账的 $\\sum n\\dim$）'
                     '$\\Rightarrow$ 切片不是可选的装饰，而维数账能看见它' %
            ('；'.join('%s：%d 条成分，$\\sum n\\dim=%d=\\dim$（平）' % (b[0], b[1], b[2])
                       for b in books)),
            all(b[4] for b in books) and len(books) == 4 and all(b[5] != b[3] for b in books),
            '错账（不按切片）：%s' % [(b[0], b[5], b[3]) for b in books])

    # ---- R11.2 (a) 逐场核验：$\\mathbb{Z}_3$ 的荷完全由色携带
    sgn = RESID['triality_sign']
    allf = [(nm, f) for nm in names for f in sm_fields(nm)]

    def tri_cnt(bl):
        r"""一种荷号下把两种符号都测：$3(B-L)\equiv\pm(p-q)\pmod3$ 各自数反例。"""
        cnt, tot, bp, bm = {}, 0, [], []
        for nm, f in allf:
            t3 = 3 * bl(f)
            if t3.denominator != 1:
                continue
            tot += 1
            p1, p2 = f['lam'][0], f['lam'][1]
            t = int(t3) % 3
            cnt[t] = cnt.get(t, 0) + 1
            if t != (p1 - p2) % 3:
                bp.append((nm, f['lam'], str(bl(f))))
            if t != (p2 - p1) % 3:
                bm.append((nm, f['lam'], str(bl(f))))
        return {'sgn': '+' if (not bp and bm) else ('-' if (not bm and bp) else '不一致'),
                'cnt': cnt, 'tot': tot, '+': bp, '-': bm}
    st, se = tri_cnt(f_bl), tri_cnt(lambda f: f['BL'])
    sel_sgn, fcnt, ftot, fbad_p, fbad_m = st['sgn'], st['cnt'], st['tot'], st['+'], st['-']
    tsg = 1 if sel_sgn == '+' else -1
    SEL.update({'tri_sgn': sel_sgn, 'tri_sgn_engine': se['sgn'], 'tsg': tsg,
                'tri_wt_sgn': sgn, 'tri_tot': ftot, 'tri_cnt': fcnt, 'nrep': len(names),
                'tri_bad': {'std': (len(st['+']), len(st['-'])),
                            'eng': (len(se['+']), len(se['-']))}})
    p &= ok('R11.2', '把 R10.4 那条同余式从 SO(10) 的**权重**搬到 SM 的**场**上：对表内 %d 个表示'
                     '展开出来的每一条低能场（共 %d 条），$3(B-L)\\equiv s(p-q)\\pmod 3$，'
                     '$(p,q)$ 是该场的 $A_2$ Dynkin 标号。**符号不是抄来的**：两套荷号'
                     '（教材号、引擎号）$\\times$ 两种符号，四种配对全部测过 $\\Rightarrow$ '
                     '教材号唯一一致 $s=%s$、引擎号唯一一致 $s=%s$，而 R10.4 在权重层（引擎号）'
                     '读到的是 $%s$ $\\Rightarrow$ 两层是**同一条**同余，它们之间的差别恰好就是 '
                     'R5.7/R6.6 那条已登记的"教材号 $=-$ 引擎号"约定差；再把荷号与符号**交叉**'
                     '配对的两种组合当反例数：教材号配 $-$ 反例 %d 条、引擎号配 $+$ 反例 %d 条 '
                     '$\\Rightarrow$ 符号是被这批读数选出来的，不是被假定的。'
                     '$\\Rightarrow$ 残留 $\\mathbb{Z}_3$ 作用在低能场上**只看色**：它是色 triality '
                     '的计数，没有别的来源。分档读数：triality $0/1/2$ 各有 %s 条 $\\Rightarrow$ '
                     '非平凡的那一半**全部**是色三重态，而色单态（triality 0）自动中性' %
            (len(names), ftot, sel_sgn, se['sgn'], sgn, len(fbad_m), len(se['+']),
             '、'.join('%d：%s' % (k, fcnt.get(k, 0)) for k in (0, 1, 2))),
            sel_sgn in ('+', '-') and se['sgn'] in ('+', '-') and se['sgn'] == sgn and
            sel_sgn != se['sgn'] and ftot > 0 and fcnt.get(0, 0) > 0,
            '教材号 $s=%s$（$+$ 配对反例 %d、$-$ 配对反例 %d）；引擎号 $s=%s$（$+$ 配对反例 %d、'
            '$-$ 配对反例 %d）；R10.4 权重层读到 %s；分档 %s' %
            (sel_sgn, len(fbad_p), len(fbad_m), se['sgn'], len(se['+']), len(se['-']), sgn,
             dict((k, fcnt.get(k, 0)) for k in (0, 1, 2))))

    # ---- R11.3 (b) 场清单：名字由签名绑定，且切片每条恰是一个 SM 不可约表示
    mat = sm_fields('16')
    for f in mat:
        f['name'] = MATTER_SIG.get((f['lam'], f['Y'], f['BL']), '未命名')
    partition = madd(*[f['ms'] for f in mat])
    unamed = [f['lam'] for f in mat if f['name'] == '未命名']
    collide = len(mat) - len(set((f['lam'][:2], f['lam'][2]) for f in mat))
    p &= ok('R11.3', '$16_F$ 展开成 %d 条低能场：%s；每条都满足"一个 3221 行 $\\times$ 一个 $Y$ '
                     '切片 $=$ 一条重数为 1 的 SM 不可约表示"（`sm_fields` 里那条断言逐条把关），'
                     '且这 %d 条的权重**恰好分成** $16_F$ 的 16 条权重（多重集相等，不只是维数相加）'
                     '$\\Rightarrow$ 场清单是量出来的，不是从文献抄的。名字由 $(\\lambda,Y,B-L)$ '
                     '签名绑定：未命名 %s 条、签名多射 %s 次。反面对照：只按 (色,弱) 定名会把 6 条'
                     '读成 %d 类（$u^c,d^c$ 与 $e^c,\\nu^c$ 各占同一格）$\\Rightarrow$ $Y$ 参与定名' %
            (len(mat), '、'.join('$%s$' % f['name'] for f in sorted(mat, key=lambda x: x['name'])),
             len(mat), unamed or '无', '未' if len(mat) == 6 else '被', 6 - collide),
            len(mat) == 6 and not unamed and partition == ms16 and
            len(set(f['name'] for f in mat)) == 6 and collide == 2,
            '读数：%s' % [(f['name'], f['lam'], str(f['Y']), str(f['BL']), f['nwt']) for f in mat])

    # ---- R11.4 (b) 物质字称 = $(-1)^{\\text{费米子数}}$，以及 $B/L$ 派生规则本身
    allodd = all((3 * f_bl(f)).denominator == 1 and int(3 * f_bl(f)) % 2 for f in mat)
    def bl_pair(f, flip=False):
        r"""$B$、$L$ 的派生规则：色非单态者 $B=B-L$、$L=0$；色单态者 $L=-(B-L)$、$B=0$。
        `flip` 是**变异体**（把"哪一半携带 $B$"对调），用来证明下面那条文献比对不是恒真式。"""
        col = (f['lam'][:2] != (0, 0)) != flip
        return (str(f_bl(f)), '0') if col else ('0', str(-f_bl(f)))
    colorb = [bl_pair(f) for f in mat]
    mswap = [bl_pair(f, True) for f in mat]
    # 教材一代六个场的 $(B,L)$：**这一列是比对，不是推导**（与 R6.6 同一处置）
    ntxt = sorted([('0', '-1'), ('0', '-1'), ('0', '1'),
                   ('1/3', '0'), ('-1/3', '0'), ('-1/3', '0')])
    nocol_l = sum(1 for f in mat if f['lam'][:2] != (0, 0) and f_l(f) != 0)
    nl = sum(1 for f in mat if f['lam'][:2] == (0, 0) and f_b(f) != 0)
    p &= ok('R11.4', '6 条物质场的 $3(B-L)$ **全是奇数**：%s $\\Rightarrow$ 在只含物质场的算符上 '
                     '$(-1)^{\\sum_k3(B-L)_k}=(-1)^{\\text{费米子数}}$ 恒等，即那条 2 阶元在低能就是'
                     '**物质字称**（R10.3 在 SO(10) 权重层数过，这一层在 SM 场上再数一遍）。'
                     '$B$、$L$ 按一条规则从量出来的 (色, $B-L$) 派生：色非单态者 $B=B-L$、$L=0$，'
                     '色单态者 $L=-(B-L)$、$B=0$；这条规则在 $16_F$ 里**没有反例**（带色的轻子 %d 条、'
                     '单态的重子 %d 条）$\\Rightarrow$ 下面的 $\\Delta B/\\Delta L$ 不是外部填进来的数，'
                     '而"重子数由色携带、轻子数由色单态携带"这一句在这 16 条权重上是可核对的。'
                     '规则选得对不对由一条**文献比对**收口：派生的 $(B,L)$ 与教材一代六个场的 '
                     '$(B,L)$ 作为多重集**完全相同**——这一列是**比对、不是推导**（与 R6.6 同一处置），'
                     '故同时植入变异体：把规则里"哪一半携带 $B$"对调，多重集立刻不等 $\\Rightarrow$ '
                     '比对这一列有牙齿，不是恒真式' %
            ('、'.join('$%s$：%s' % (f['name'], 3 * f_bl(f)) for f in mat), nocol_l, nl),
            allodd and nocol_l == 0 and nl == 0 and
            sorted(colorb) == ntxt and sorted(mswap) != ntxt,
            '派生的 $(B,L)$：%s；文献表（比对，非推导）：%s；变异体（两半对调）：%s' %
            (list(zip([f['name'] for f in mat], colorb)), ntxt, sorted(mswap)))

    # ---- R11.5 三条独立计数路径：按场乘、按有序组、按 SO(10) 先拆再投影
    def routes(deg):
        per, tot_a = [], 0
        for combo in itertools.combinations_with_replacement(range(len(mat)), deg):
            fl = [mat[i] for i in combo]
            n = sm_singlet_mult(sel_ms(fl))
            per.append((combo, n))
            tot_a += n * perm_weight(combo, deg)
        big = ms16
        for _i in range(deg - 1):
            big = tprod(big, ms16)
        tot_b = sm_singlet_mult(big)
        d = decomp(big)
        tot_c = None if d is None else sum(
            k * sm_singlet_mult(irrep(dynkin(la))[1]) for la, k in d.items())
        return per, tot_a, tot_b, tot_c, (0 if d is None else len(d))
    r2, r4 = routes(2), routes(4)
    SEL.update({'r2': r2, 'r4': r4, 'mat': mat})
    p &= ok('R11.5', '低能单态的**总数**由三条不共享算术的路径给出同一个数：'
                     '(i) 逐条场组合算 SM 单态、再乘该多重集所代表的有序组数（$n!/\\prod m_k!$）；'
                     '(ii) 直接对 $16^{\\otimes %d}$ 的整权重乘积作 Klimyk 交错和；'
                     '(iii) 先在 SO(10) 层把 $16^{\\otimes %d}$ 拆成不可约表示（`decomp`，R8 的'
                     '独立机器），再逐表示投影到 SM 单态。读数：$n=2$ 为 %s，$n=4$ 为 %s $\\Rightarrow$ '
                     '"按场内容分类"与"按 SO(10) 道分类"是同一件事的两种数法' %
            (4, 4, r2[1:4], r4[1:4]),
            r2[1] == r2[2] == r2[3] and r4[1] == r4[2] == r4[3] and r4[1] > 0,
            '$n=2$：%d 条场组合（含单态 %d 条），有序总数 %d，整乘积 %d，SO(10) 拆分 %d 个不可约 '
            '$\\Rightarrow$ %d；$n=4$：%d 条（含单态 %d 条），%d vs %d vs %d，拆分 %d 个不可约' %
            (len(r2[0]), sum(1 for _c, n in r2[0] if n), r2[1], r2[2], r2[4], r2[3],
             len(r4[0]), sum(1 for _c, n in r4[0] if n), r4[1], r4[2], r4[3], r4[4]))

    # ---- R11.6 二次型（质量项）：唯一的 SM 单态就是 $\\nu^c\\nu^c$
    c2 = [sel_cand([mat[i] for i in combo], chans, g0) for combo, _n in r2[0]]
    for x, (combo, n) in zip(c2, r2[0]):
        x['name'] = '+'.join(mat[i]['name'] for i in combo)
        x['singlet'] = n
    hit2 = [x for x in c2 if x['singlet'] > 0]
    SEL.update({'c2': c2, 'hit2': hit2})
    h2 = hit2[0]
    p &= ok('R11.6', '两条物质场相乘的 %d 个场内容类里，含 SM 单态的只有 %d 个 $\\Rightarrow$ '
                     '物质双线性里唯一的低能不变算符是 %s（单态数 %d，$\\Delta B=%s$、'
                     '$\\Delta L=%s$、$3Q=%s$）。它在两条通道下的判决都是**允许**：'
                     '$|\\Delta(B-L)|=1$ 那一步留的 %s 与 $|\\Delta(B-L)|=2$ 那一步留的 %s '
                     '都不禁它 $\\Rightarrow$ 右手中微子的 Majorana 质量项与残留群一致；'
                     '而它在"3221 零权"那个 projector 下读成 %d（$\\Rightarrow$ 荷不配平：'
                     '$B-L=%s\\ne0$），与 R8.5/R7.4"要拿到 $|B-L|=2$ 必须插入 $126_H$"是'
                     '同一件事在低能一侧的重现' %
            (len(c2), len(hit2), h2['name'], h2['singlet'], h2['dB'], h2['dL'], h2['t3q'],
             ztex(chans['|1|'][1]), ztex(chans['|2|'][1]), h2['zero'], h2['q']),
            len(hit2) == 1 and h2['name'] == '\\nu^c+\\nu^c' and h2['singlet'] == 1 and
            h2['zero'] == 0 and
            all(v['甲'] is True and v['乙'] is True and v['丙'] is True and v['甲乙丙一致'] and
                v['因子与']
                for v in h2['v'].values()),
            '三条路径判决（甲/乙/丙）：%s；荷账 $(\\Delta B,\\Delta L,3Q)=%s$' %
            (dict((k, (v['甲'], v['乙'], v['丙'])) for k, v in h2['v'].items()),
             (h2['dB'], h2['dL'], h2['t3q'])))

    # ---- R11.7 四次（d=6）：枚举、分类、判决
    c4 = [sel_cand([mat[i] for i in combo], chans, g0) for combo, _n in r4[0]]
    for x, (combo, n) in zip(c4, r4[0]):
        x['name'] = '+'.join(mat[i]['name'] for i in combo)
        x['singlet'] = n
    hit4 = [x for x in c4 if x['singlet'] > 0]
    lost4 = [x['name'] for x in hit4 if x['zero'] == 0]
    over4 = [(x['name'], x['zero'], x['singlet']) for x in hit4 if x['zero'] > x['singlet']]
    top4 = max(over4, key=lambda t: t[1]) if over4 else ('—', 0, 0)
    SEL.update({'c4': c4, 'hit4': hit4, 'lost4': lost4, 'over4': over4})
    dis4 = [x['name'] for x in hit4 if False in [v['甲'] for v in x['v'].values()]]
    p &= ok('R11.7', '四条物质场（质量维数 $d=4\\times3/2=6$）共 %d 个场内容类，含 SM 单态的 %d 条'
                     '（单态数 %s，合计 %d 个不变张量结构）。逐条按 $N\\mid 3Q$ 判决：**允许 %d 条、'
                     '禁戒 %d 条**。三条互不共享算术的实现（甲 整除、乙 群元逐元、丙 浮点角度）在'
                     '每一条候选上同判决，且因子逐点判（$\\mathbb{Z}_3$ 看 $3Q\\bmod3$、'
                     '$\\mathbb{Z}_2$ 看 $3Q\\bmod2$）与"两因子取与"也和甲一致 $\\Rightarrow$ '
                     '$\\mathbb{Z}_6=\\mathbb{Z}_2\\times\\mathbb{Z}_3$ 的分解在这里是真的，'
                     '不是拿来做修辞的。projector 的对照同样只讲读数：这 %d 条含单态的候选里，'
                     '"3221 零权"那个错投影读出 0 的有 %d 条（%s）$\\Rightarrow$ 它会**漏掉**真单态；'
                     '而它在别的候选上读出的数又大于单态数（最大一例 %s）$\\Rightarrow$ 它也会**多算**。'
                     '两个方向都有反例 $\\Rightarrow$ "零权数"与"单态数"之间**没有**不等式关系，'
                     '谁也不是谁的界 $\\Rightarrow$ 本节凡要数低能不变量，只能用 $Y$ 切片上的 Klimyk' %
            (len(c4), len(hit4), [x['singlet'] for x in hit4],
             sum(x['singlet'] for x in hit4), len(hit4) - len(dis4), len(dis4),
             len(hit4), len(lost4), '、'.join('$%s$' % s for s in lost4),
             '%s：零权 %d > 单态数 %d' % top4),
            len(hit4) == 8 and not dis4 and len(lost4) == 1 and bool(over4) and
            all(x['v'][k]['甲乙丙一致'] and x['v'][k]['因子与']
                for x in hit4 for k in chans) and
            all(v['甲'] is True for x in hit4 for v in x['v'].values()),
            '含单态的类（场内容, 单态数, $\\Delta B$, $\\Delta L$, $3Q$, 零权读数）：%s；'
            '零权 projector 漏掉的（漏方向）：%s；零权数反而大于单态数的（多方向）：%s' %
            ([(x['name'], x['singlet'], x['dB'], x['dL'], x['t3q'], x['zero']) for x in hit4],
             lost4, over4))

    # ---- R11.8 (c) 质子：残留群不禁 $\\Delta(B-L)=0$ 的 dim-6 质子衰变算符
    pv = [x for x in hit4 if x['dB'] != '0' and x['dL'] != '0']
    pvl = [x for x in pv if x['q'] == '0']
    congr = [x['name'] for x in c4 if (int(F(x['t3q'])) - tsg * x['tri']) % 3]
    bad3 = [x for x in c4 if int(F(x['t3q'])) % 3]
    even3q = sum(1 for x in c4 if int(F(x['t3q'])) % 2 == 0)
    SEL.update({'pv': pv, 'pvl': pvl, 'congr': congr, 'even3q': even3q,
                'bad3': [(x['name'], x['t3q'], x['tri'], x['singlet']) for x in bad3]})
    p &= ok('R11.8', '直接回答"残留群保不保质子"：**不保**。含单态的 %d 条 d=6 类里有 %d 条同时'
                     '$\\Delta B\\ne0$ 且 $\\Delta L\\ne0$（%s），其中 $\\Delta(B-L)=0$ 的 %d 条'
                     '——$|\\Delta B|=|\\Delta L|=1$ 那一类就是质子衰变的荷前提——判决全部是'
                     '**允许**（被禁 %d 条）。机理也是读数而不是修辞，两半边各量一次。'
                     '(α) 把 R11.2 那条同余从**场**搬到**算符**：这 %d 条 d=6 候选上 $3Q$ 与色侧和 '
                     '$s\\sum_k(p_k-q_k)$ 模 3 不同余的有 %d 条 $\\Rightarrow$ 同一判据有两台互不相同'
                     '的机器在跑；于是 $\\mathbb{Z}_3$ 判禁的那 %d 条里**含 SM 单态的**有 %d 条 '
                     '$\\Rightarrow$ 它只能禁色非单态，而"要单态"这一步在枚举里早已把它们滤掉 '
                     '$\\Rightarrow$ 在低能单态层 $\\mathbb{Z}_3$ 这一半**没有**额外信息。'
                     '(β) $\\mathbb{Z}_2$ 那一半看 $3Q\\bmod2$，而每条物质场的 $3(B-L)$ 都是奇数'
                     '（R11.4）$\\Rightarrow$ 偶数条相乘必为偶：这 %d 条里 $3Q$ 读成偶数的有 %d 条 '
                     '$\\Rightarrow$ 物质字称那半边在 d=6 这一层也没有可禁的东西（它并非恒等无物——'
                     'R11.9 的标量插入候选就是被它判禁的）。'
                     '$\\Rightarrow$ 残留离散规范对称性**不**给出质子稳定性的论证：R10.5 推翻'
                     '"残留 $\\mathbb{Z}_2$（物质字称）对质子有利"之后，这里连剩下的那条路也不通' %
            (len(hit4), len(pv), '、'.join('$%s$' % x['name'] for x in pv), len(pvl),
             sum(1 for x in pvl if False in [v['甲'] for v in x['v'].values()]),
             len(c4), len(congr), len(bad3), sum(1 for x in bad3 if x['singlet']),
             len(c4), even3q),
            bool(pv) and len(pvl) == len(pv) == 3 and not congr and
            len(bad3) > 0 and all(not x['singlet'] for x in bad3) and
            all(int(F(x['t3q'])) % 3 == 0 for x in hit4) and even3q == len(c4) and
            not any(False in [v['甲'] for v in x['v'].values()] for x in pvl) and
            all(x['nf'] % 2 == 0 and abs(F(x['dB'])) == abs(F(x['dL'])) == 1 for x in pvl),
            '质子衰变候选（场内容, 单态数, $\\Delta B$, $\\Delta L$, 判决）：%s；'
            '$\\mathbb{Z}_3$ 判禁的那些（场内容, $3Q$, 色侧和, 单态数），最多列 6 条：%s' %
            ([(x['name'], x['singlet'], x['dB'], x['dL'],
               dict((k, v['甲']) for k, v in x['v'].items())) for x in pv],
             SEL['bad3'][:6]))

    # ---- R11.9 (d) 正对照与变异测试：判决这一列必须**能动**
    sdecl = sorted(set(CSPLIT['decl_union']))
    hyreps = [nm for nm in RESID['odd'] if nm in NAMED]
    scal = dict((nm, sm_fields(nm)) for nm in sorted(set(sdecl) | set(hyreps) | {'126', '126̄'}))
    pair2 = [(combo, sm_content(sel_ms([mat[combo[0]], mat[combo[1]]]))[0])
             for combo in itertools.combinations_with_replacement(range(len(mat)), 2)]

    def ins_scan(reps):
        out = []
        for combo, cont in pair2:
            for nm in reps:
                for sf in scal[nm]:
                    pb = sm_pair_singlets(cont, [(sf['lam'], sf['Y'], 1)])
                    if pb:
                        f = dict(sf)
                        f['boson'] = True
                        fl = [mat[combo[0]], mat[combo[1]], f]
                        x = sel_cand(fl, chans, g0)
                        x['pb'] = pb
                        x['name'] = '+'.join(f2['name'] if not f2.get('boson') else
                                             '%s_H' % tex_name(f2['rep']) for f2 in fl)
                        out.append(x)
        return out
    scan_decl = ins_scan(sdecl)
    scan_odd = ins_scan(hyreps)
    forb_odd = [x for x in scan_odd if x['v']['|2|']['甲'] is False]
    flip3 = [x for x in scan_odd if x['v']['|1|']['甲'] is True and x['v']['|2|']['甲'] is False]
    flip_sg = [x['sig'] for x in c2 + c4
               if x['t3q'] not in ('0',) and
               any(rule_exact(F(x['t3q']), n) != rule_exact(-F(x['t3q']), n)
                   for _qd, n in chans.values())]
    SEL.update({'scan_decl': scan_decl, 'scan_odd': scan_odd, 'forb_odd': forb_odd,
                'flip3': flip3, 'flip_sg': flip_sg, 'sdecl': sdecl, 'hyreps': hyreps})
    p &= ok('R11.9', '"禁掉 0 条"必须与"枚举到 0 条"可区分，故把判据放在**能动**的四处测：'
                     '(i) 枚举到的候选数非空：d=6 有 %d 条、双线性 %d 条、插入声明谱（%s）的 '
                     'd=4 候选 %d 条 $\\Rightarrow$ 上面那句"允许 %d 条、禁 0 条"不是空集上的'
                     '恒真式。'
                     '(ii) 换成插入**奇** $3(B-L)$ 的标量（%s 型——它们自己就把物质字称破了）：'
                     '候选 %d 条，其中 $\\mathbb{Z}_6$ **判禁 %d 条** $\\Rightarrow$ "禁"这一支'
                     '是活的。'
                     '(iii) 把 $\\mathbb{Z}_6$ 误读成 $\\mathbb{Z}_3$（丢掉物质字称那半边）：'
                     '在 (ii) 那批候选上出现 %d 条判决差异 $\\Rightarrow$ 两个因子各自都在做功。'
                     '(iv) 反向对照：把整套荷换号（引擎号 $\\leftrightarrow$ 教材号，R5.7 那条'
                     '已登记的约定差）时判决翻转 **%d** 条 $\\Rightarrow$ 结论不依赖 $B-L$ 的'
                     '符号约定；这一条必须为 0，不为 0 就说明判决其实挂在记号上' %
            (len(hit4), len(hit2), higgs_tex(sdecl), len(scan_decl),
             len(hit4), higgs_tex(hyreps), len(scan_odd), len(forb_odd),
             len(flip3), len(flip_sg)),
            len(hit4) > 0 and len(hit2) > 0 and len(forb_odd) > 0 and len(flip3) > 0 and
            not flip_sg and all(x['nf'] % 2 == 0 for x in forb_odd) and
            all(x['singlet'] == x['pb'] for x in scan_odd) and
            all(x['v']['|2|']['甲'] is not None for x in scan_odd),
            '判禁的假想插入候选：%s；只按 $\\mathbb{Z}_3$ 会误放行的：%s；换号翻转：%s' %
            ([(x['name'], x['t3q'], x['v']['|1|']['甲'], x['v']['|2|']['甲'])
              for x in forb_odd[:8]], [x['name'] for x in flip3[:8]], flip_sg))

    # ---- R11.10 条件性与边界：这些"允许"挂在哪一份标量谱上
    scan_126 = ins_scan(['126', '126̄'])
    allow_126 = [x for x in scan_126 if all(v['甲'] is True for v in x['v'].values())]
    SEL.update({'scan_126': scan_126, 'allow_126': allow_126, 'chans': chans})
    p &= ok('R11.10', '上面所有判决都是**条件读数**，条件就是 R10.10 那个空交集：$q_\\Delta=2$ '
                      '那条通道的母表示（$126_H/\\overline{126}_H$）不在链探针字面声明的标量谱里，'
                      '声明的只有 %s $\\Rightarrow$ "只按声明谱"那一步里残留群根本还没出现，'
                      '被禁条数在那里不是一个物理数，而是"无从谈起"。把 $126/\\overline{126}$ 的'
                      '分量当作假想插入重跑同一条判据（与 R10.10 的"若补上"同一假设，且与 §6 '
                      'R7.4、§7 R8.5 的假想插入同一条）：候选 %d 条、两条通道都允许 %d 条。'
                      '**但质子那一条结论不随标量谱变**：它只依赖"4 费米子 $=$ 偶数"这个事实，'
                      '而偶费米子数不是插入出来的 $\\Rightarrow$ 这是本节里唯一一处无条件成分，'
                      '登记清楚以免与上面那些条件判决混读' %
            (higgs_tex(sdecl) or '无', len(scan_126), len(allow_126)),
            bool(scan_126) and bool(allow_126) and
            all(x['nf'] % 2 == 0 for x in allow_126) and
            all(not c for _b, c in RESID['cond']) and
            all(x['v']['|2|']['甲'] is not None for x in scan_126),
            '假想插入 $126/\\overline{126}_H$ 的候选（场内容, $3Q$, 甲判决）：%s；'
            '链上字面声明谱 %s；承载者 $\\cap$ 声明谱 %s' %
            ([(x['name'], x['t3q'], x['v']['|2|']['甲']) for x in scan_126[:8]],
             dict(CSPLIT['decl']), RESID['cond']))
    return p


GLOB = {}


def g_mod1(x):
    r"""把有理数折回 $[0,1)$（群相位以 $2\pi$ 为单位时"等于 0"的判据）。"""
    f = F(x)
    return f - (f.numerator // f.denominator)


def g_scaled(vs):
    """一组有理向量整体放大成整数向量：返回 (整数行, 公倍数)。"""
    den = 1
    for v in vs:
        for x in v:
            f = F(x)
            den = den * f.denominator // math.gcd(den, f.denominator)
    return [[int(F(x) * den) for x in v] for v in vs], den


def g_snf(rows):
    r"""整数矩阵的 Smith 不变因子（升序）。只做初等行列变换 $\Rightarrow$ 与 `g_det` 的
    高斯消元是两条不共享算术的路数。"""
    A = [[int(x) for x in r] for r in rows]
    n, m = len(A), len(A[0])
    out = []
    for t in range(min(n, m)):
        while True:
            piv = None
            for i in range(t, n):
                for j in range(t, m):
                    if A[i][j] and (piv is None or abs(A[i][j]) < abs(A[piv[0]][piv[1]])):
                        piv = (i, j)
            if piv is None:
                return sorted(out)
            pi, pj = piv
            A[t], A[pi] = A[pi], A[t]
            for i in range(n):
                A[i][t], A[i][pj] = A[i][pj], A[i][t]
            if A[t][t] < 0:
                A[t] = [-x for x in A[t]]
            again = False
            for i in range(t + 1, n):
                if A[i][t]:
                    q = A[i][t] // A[t][t]
                    A[i] = [a - q * b for a, b in zip(A[i], A[t])]
                    if A[i][t]:
                        A[t], A[i] = A[i], A[t]
                        again = True
            for j in range(t + 1, m):
                if A[t][j]:
                    q = A[t][j] // A[t][t]
                    for i in range(n):
                        A[i][j] -= q * A[i][t]
                    if A[t][j]:
                        for i in range(n):
                            A[i][t], A[i][j] = A[i][j], A[i][t]
                        again = True
            if again:
                continue
            if any(A[i][j] % A[t][t] for i in range(t + 1, n) for j in range(t + 1, m)):
                for i in range(m):
                    A[t][i] += A[t + 1][i]
                continue
            out.append(A[t][t])
            break
    return sorted(out)


def g_det(Min):
    """精确行列式（选主元高斯消元，全程 Fraction）。"""
    M = [[F(x) for x in r] for r in Min]
    n = len(M)
    d = F(1)
    for c in range(n):
        piv = next((r for r in range(c, n) if M[r][c] != 0), None)
        if piv is None:
            return F(0)
        if piv != c:
            M[c], M[piv] = M[piv], M[c]
            d = -d
        pv = M[c][c]
        d *= pv
        M[c] = [x / pv for x in M[c]]
        for r in range(c + 1, n):
            if M[r][c] != 0:
                k = M[r][c]
                M[r] = [a - k * b for a, b in zip(M[r], M[c])]
    return d


def g_lat_index(gens, basis):
    r"""$[\Lambda(\text{basis}):\Lambda(\text{gens})]$ 与不变因子。两边都必须是满秩基；
    `gens` 不落在 `basis` 生成的格裡就不给数（不静默放宽）。"""
    n = len(basis)
    if len(gens) != n:
        return None, ('生成元 %d 个 != 基维数 %d' % (len(gens), n), [])
    INT, den = g_scaled([list(v) for v in gens] + [list(v) for v in basis])
    Gs, Bp = INT[:n], INT[n:]
    Mi = inverse_rows(Bp)
    T = [[sum(F(Gs[i][k]) * Mi[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    bad = [str(x) for r in T for x in r if x.denominator != 1]
    if bad:
        return None, ('生成元不在超格内', bad[:4])
    f = g_snf([[int(x) for x in r] for r in T])
    idx = 1
    for x in f:
        idx *= x
    dt = g_det(T)
    return idx, (f, dt.denominator == 1 and abs(dt.numerator) == idx, int(abs(dt)))


CEN_T_DEN = 12           # $t$ 的网格步长：$t\in\frac{1}{12}\mathbb Z$
CEN_U_PER = 3            # $U(1)_{B-L}$ 参数的周期，$=1/g_0$ 的一半再乘 $2\pi$ 后的数（R10.1 量出）


def cen_elements():
    r"""候选中心元 $(a_3,a_L,a_R,t)$：色 $\mathbb Z_3$、两个 $\mathbb Z_2$、以及
    $\frac{1}{12}\mathbb Z/\text{period}$ 里的 $U(1)_{B-L}$ 元素。"""
    return [(a3, aL, aR, F(k, CEN_T_DEN)) for a3 in range(3) for aL in range(2)
            for aR in range(2) for k in range(CEN_T_DEN * CEN_U_PER)]


def cen_law(x, y):
    """四个因子各自按自己的阶取模后的群乘法。"""
    return ((x[0] + y[0]) % 3, (x[1] + y[1]) % 2, (x[2] + y[2]) % 2,
            (x[3] + y[3]) % CEN_U_PER)


CEN_IDENT = (0, 0, 0, F(0))


def cen_phase(x, lab, bl, conv='A'):
    r"""$(a_3,a_L,a_R,t)$ 作用在一条 3221 分量 $(p,q,l_L,l_R)$、$B-L$ 为 `bl` 上的相位
    （以 $2\pi$ 为单位）。色 triality 的两种约定都测：$\mathbb Z_3$ 有两个生成元，
    选哪一个在 R10.4 由数据定，本层不重挑。"""
    p, q, lL, lR = lab
    tri = (p + 2 * q) if conv == 'A' else (2 * p + q)
    return g_mod1(F(x[0] * tri, 3) + F(x[1] * lL, 2) + F(x[2] * lR, 2) + F(x[3]) * F(bl))


def cen_order(x, upto=24):
    """群元的阶；`upto` 步内不回到单位元就不给数。"""
    g, n = CEN_IDENT, 0
    while n < upto:
        g = cen_law(g, x)
        n += 1
        if g == CEN_IDENT:
            return n
    return None


def cen_class(x, gam):
    r"""$x$ 在 $\Gamma$ 里的陪集（$\Gamma$ 有限 $\Rightarrow$ 直接枚举倍元当键）。"""
    return frozenset(cen_law(x, g) for g in gam)


def ctex(x):
    """群元 $(a_3,a_L,a_R,t)$ 的报告版（不泄漏 Python 的 Fraction 打印）。"""
    f = F(x[3])
    ts = str(f.numerator) if f.denominator == 1 else r'\frac{%d}{%d}' % (f.numerator, f.denominator)
    return '$(%d,%d,%d,%s)$' % (x[0], x[1], x[2], ts)


def coset_reps(surv, gam):
    reps, seen = [], set()
    for x in surv:
        k = cen_class(x, gam)
        if k not in seen:
            seen.add(k)
            reps.append(x)
    return reps


def coset_orders(reps, gam):
    r"""每个陪集代表的阶：最小的 $m$ 使 $x^m\in\Gamma$。"""
    out = []
    for i, x in enumerate(reps):
        acc, n = i, 1
        while acc != 0 and n <= 24:
            y = cen_law(reps[acc], x)
            nxt = [k for k, r in enumerate(reps) if cen_class(r, gam) == cen_class(y, gam)]
            if not nxt:
                acc, n = None, None
                break
            acc, n = nxt[0], n + 1
        out.append(n if acc == 0 else None)
    return out


def ab_partitions(e):
    """整数 e 的全部分拆，每个分拆给成升序列表。"""
    if e == 0:
        return [[]]
    out = []
    for first in range(1, e + 1):
        for rest in ab_partitions(e - first):
            if not rest or first <= rest[0]:
                out.append([first] + rest)
    return out


def ab_groups(n):
    r"""阶 $=n$ 的全部有限阿贝尔群，用不变因子 $(d_1\mid d_2\mid\cdots)$ 表示（$\prod d_i=n$）。

    只从 $n$ 的素因子分拆构造，不查表 $\Rightarrow$ "唯一命中"这句话有内容：它核对的是
    这个阶上一共有哪些阿贝尔群，而不是"我手上这个名字在不在一张写好的清单里"。
    """
    fac, m, pr = {}, n, 2
    while pr * pr <= m:
        while m % pr == 0:
            fac[pr] = fac.get(pr, 0) + 1
            m //= pr
        pr += 1
    if m > 1:
        fac[m] = fac.get(m, 0) + 1
    combos = [[]]
    for pr in sorted(fac):
        combos = [c + [pt] for c in combos for pt in ab_partitions(fac[pr])]
    out = []
    for c in combos:
        w = max([len(x) for x in c] + [0])
        divs = [1] * w
        for pr, row in zip(sorted(fac), c):
            padded = [0] * (w - len(row)) + row     # 短的那侧补零指数 ⇒ 大因子对齐在右
            for j, e in enumerate(padded):
                divs[j] *= pr ** e
        out.append([d for d in divs if d > 1])
    return sorted(out)


def ab_element_orders(divs):
    """不变因子给定的阿贝尔群的全部元素阶（升序多重集）。"""
    els = [()]
    for d in divs:
        els = [e + (k,) for e in els for k in range(d)]
    out = []
    for e in els:
        o = 1
        for d, k in zip(divs, e):
            oo = 1 if k == 0 else d // math.gcd(k, d)
            o = o * oo // math.gcd(o, oo)
        out.append(o)
    return sorted(out)


def ab_name(n, obs):
    r"""观测到的元素阶多重集 $\to$ 该阶上唯一与之相符的阿贝尔群（不变因子）。

    命中 0 个或 2 个以上都不给名字 $\Rightarrow$ 定名这一步是判决，不是排版。
    """
    hits = [dg for dg in ab_groups(n) if None not in obs and
            ab_element_orders(dg) == sorted(obs)]
    return hits[0] if len(hits) == 1 else None


def ab_tex(divs):
    r"""不变因子 → 单个数学式 $\mathbb Z_{d_1}\times\cdots$（不拼多个 `$` 段）。

    空列表是平凡群；`None` 表示这一阶上没有唯一命中，就不印符号（不让排版冒充结论）。
    """
    if divs is None:
        return r'（该阶上定不出唯一的群）'
    return r'$%s$' % r'\times'.join(r'\mathbb Z_{%d}' % d for d in divs) if divs else r'$\{e\}$'


def mth(s):
    r"""剥掉一个已带 `$…$` 的读数的外层美元号，供嵌进另一个数学环境用。

    `$%s$` 型模板直接灌 `ztex`/`ab_tex` 的产出会拼成 `$$…$$` $\Rightarrow$ 报告里
    那个 `$` 配对门禁会红，而且读起来是两段错位的公式。只剥最外一对，其余原样。
    """
    if not isinstance(s, str) or not (s.startswith('$') and s.endswith('$') and len(s) > 2):
        return s
    assert '$' not in s[1:-1], '内层还有美元号，剥不得：%r' % s
    return s[1:-1]


def uni(xs):
    """去重升序后按报告口径印出来：读数以"值"呈现，不是以 Python 列表呈现。"""
    return '、'.join(str(x) for x in sorted(set(xs)))


def fracs(v):
    r"""一组有理数（$\varepsilon$ 基坐标）的报告版：整数不印分母，也不泄漏 `Fraction(...)`。"""
    return '(%s)' % ', '.join(str(x.numerator) if x.denominator == 1
                              else '%d/%d' % (x.numerator, x.denominator) for x in v)


def class_tex(b):
    """结构类的报告版：群名、承载者个数与名字、指数、循环性（§11.3 与 R12.3 共用一个口径）。"""
    return '%s（%d 个承载者：%s；指数 %d、%s循环）' % (
        ab_tex(b['struct']), b['n'],
        plain_tex(sorted(set(c[0] for c in b['carriers']))),
        b['expo'], '' if b['cyc'] else '不')


def run_global_layer():
    r"""R12：完整的残留离散规范群 $=$ 中心 $\times$ 整体形式，做成格上的读数。

    §9（R10）与 §10（R11）的判据都只在 $U(1)_{B-L}$ **那一个因子**导出的群上跑 $\Rightarrow$
    两层的边界原话是"若完整残留群是它的扩张，'允许'可能变严、'禁戒'不会变松"。本层把
    $SU(3)_c$、$SU(2)_{L/R}$ 的中心与 $Spin(10)$ 的整体形式一起搬到账上，回答三问：
      (i) 覆盖群到 $Spin(10)$ 的核 $\Gamma$ 多大、什么结构 $\Rightarrow$ 三条不共享算术的
          路数同数才认；
      (ii) 破缺之后**完整**的残留群在 R11 那批 SM 单态算符上是否比 $\mathbb Z_N$ 更严；
      (iii) 在场谱把整体形式钉在 $Spin(10)$ 的哪一个商上。
    本层不引入新的李论输入：用的还是 D5 的 Dynkin 图、由它推出的 $\varepsilon$ 实现、
    两条链的单根，以及 R10/R11 已经跑出来的谱。
    """
    p = True
    names = sorted(r['name'] for r in TABLE if r['name'] in NAMED)

    # ---- 在场谱在 3221 下的不同 (行标号, $B-L$)，以及每条低能场落在哪一行
    spec, ROWLAB = set(), {}
    for nm in names:
        for row in branching(irrep(NAMED[nm])[1], SUB_3221):
            spec.add((tuple(row['labels']), F(row['bl'])))
            ROWLAB[(nm, fmt_3221(row))] = (tuple(row['labels']), F(row['bl']))
    cv = 'A' if RESID.get('triality_sign') == '+' else 'B'

    # ---- v.e.v. 候选：色单态、$Q=0$、$B-L\ne0$（与 R10 同一条筛选）
    chans = {}
    for nm in names:
        for row in branching(irrep(NAMED[nm])[1], SUB_3221):
            lab, bl = tuple(row['labels']), F(row['bl'])
            if lab[:2] != (0, 0) or bl == 0:
                continue
            if not any(chg(mu, QHP) == 0 for mu in sub_irrep(row['wt'], SUB_3221)):
                continue
            chans.setdefault(abs(bl), set()).add((nm, lab, bl))

    C = cen_elements()
    gam = dict((c, set(x for x in C if all(cen_phase(x, lab, bl, c) == 0 for lab, bl in spec)))
               for c in ('A', 'B'))
    G = gam[cv]

    # ---- 路数甲/丙：三张格的指数
    P10 = [tuple(F(x, U) for x in v) for v in FUND]
    P422 = sub_fundweights(SUB_422)
    uBL = tuple(F(BL[k], 4 * U) for k in range(5))
    PH = sub_fundweights(SUB_3221) + [uBL]
    i_10, f_10 = g_lat_index(P10, PH)
    i_422, f_422 = g_lat_index(P10, P422)
    i_hop, f_hop = g_lat_index(P422, PH)

    # ---- 整体形式：$P/Q$ 与在场谱；"在不在根格里"两条独立判法
    A5 = [[int(2 * F(ip(SIMPLE[i], SIMPLE[j]), D4) / F(ip(SIMPLE[j], SIMPLE[j]), D4))
           for j in range(5)] for i in range(5)]
    Ai5 = inverse_rows(A5)
    pQ = int(abs(g_det(A5).numerator))

    def pq_class(lam):
        r"""$\Lambda=\sum_j c_j\alpha_j$ 的单根坐标 mod 1 $=$ $P/Q$ 里的类。"""
        return tuple(g_mod1(sum(F(lam[k]) * Ai5[k][j] for k in range(5))) for j in range(5))

    forms = []
    for nm in names:
        lam, ms = irrep(NAMED[nm])[0], irrep(NAMED[nm])[1]
        c = pq_class(dynkin(lam))
        ordc = next(k for k in range(1, 5)
                    if all(g_mod1(k * x).numerator == 0 for x in c))
        # 甲：最高权的单根坐标全整 $\iff$ 类为 0；乙：$D_5$ 的根格在 $\varepsilon$ 基下
        # 就是"整坐标且坐标和为偶" $\Rightarrow$ 拿它逐条权重判（另一条代码路径）
        zeroA = all(x.denominator == 1 for x in c)
        zeroB = True
        for w in ms:
            v = [F(x, U) for x in w]
            zeroB &= all(x.denominator == 1 for x in v) and (sum(v).numerator % 2 == 0)
        forms.append({'rep': nm, 'cls': [str(x) for x in c], 'order': ordc,
                      'zeroA': zeroA, 'zeroB': zeroB, 'nwt': len(ms)})

    gen = {(0, 0, 0, 0, 0)}
    frontier = [(0, 0, 0, 0, 0)]
    while frontier:
        nxt = []
        for x in frontier:
            for f in forms:
                y = tuple(g_mod1(F(x[j]) + F(f['cls'][j])) for j in range(5))
                if y not in gen:
                    gen.add(y)
                    nxt.append(y)
        frontier = nxt

    # ---- 低能单态算符（与 §10 同一批：物质场分量张成的 d=6 类里含 SM 单态的那 8 条）
    mat = SEL['mat']
    FV = {}
    for f in mat:
        key = (f['rep'], f['row'])
        assert key in ROWLAB, '%s：行 %s 不在 %s 的 3221 分支里' % (f['name'], f['row'], f['rep'])
        lab, bl = ROWLAB[key]
        assert bl == F(f['BL']) and lab[:3] == tuple(f['lam']), \
            '%s：行标号 %s / $B-L$ %s 与场自己的 %s / %s 不符' % (
                f['name'], lab, bl, f['lam'], f['BL'])
        FV[f['name']] = (lab, bl)
    assert len(FV) == len(mat), \
        '场名有重复（%d 条场只剩下 %d 个名字）⇒ 按名字建表会把两条场合成一条' % (len(mat), len(FV))
    sing_ops = [{'name': '+'.join(mat[i]['name'] for i in combo),
                 'per': [FV[mat[i]['name']] for i in combo]}
                for combo, n in SEL['r4'][0] if n > 0]
    # 这批必须与 §10 的 hit4 是**同一批**类，否则本节比的是另一张表
    hit4_names = sorted(x['name'] for x in SEL['hit4'])
    assert sorted(o['name'] for o in sing_ops) == hit4_names, \
        '本层的场内容类与 §10 的含单态类不是同一批：%s vs %s' % (
            sorted(o['name'] for o in sing_ops), hit4_names)
    NSING4 = len(hit4_names)
    Nres = dict((str(r['BL']), r['N']) for r in RESID['rows'])

    def op_phase(x, o):
        return g_mod1(sum(cen_phase(x, ll, bb) for (ll, bb) in o['per']))

    def z_phase(a, o):
        return g_mod1(a * sum(bb for (_l, bb) in o['per']))

    def sums_of(o):
        return {'name': o['name'],
                'bl': sum(bb for (ll, bb) in o['per']),
                'lL': sum(ll[2] for (ll, bb) in o['per']),
                'lR': sum(ll[3] for (ll, bb) in o['per']),
                'tri': sum(ll[0] + 2 * ll[1] for (ll, bb) in o['per'])}

    sing_sums = [sums_of(o) for o in sing_ops]

    chan_rows = []
    for qd in sorted(chans):
        N = int(Nres[str(qd)])
        zels = [F(k) / F(qd) for k in range(N)]
        # 键必须全序：$16$ 与 $144$ 同为 $(0,0,0,1)$，只排到 $(lab,bl)$ 时并列由 set 的散列序决定
        # ⇒ 每次跑换一次行序，报告不能按行引用。第三键取 `names` 名次（与全文其余表同序）。
        for (nm, lab, bl) in sorted(chans[qd],
                                    key=lambda t: (str(t[1]), str(t[2]), names.index(t[0]))):
            surv = [x for x in C if cen_phase(x, lab, bl) == 0]
            assert all(len(cen_class(x, G)) == len(G) for x in surv), \
                r'陪集大小不等于 $|\Gamma|$ ⇒ 商不掉：%s' % nm
            reps = coset_reps(surv, G)
            assert len(reps) * len(G) == len(surv), \
                r'陪集代表元数 × $|\Gamma|$ ≠ 存活元数 @ %s' % nm
            ords = coset_orders(reps, G)
            chars = sorted(set(tuple(op_phase(x, o) for o in sing_ops) for x in reps))
            zchars = sorted(set(tuple(z_phase(a, o) for o in sing_ops) for a in zels))
            af = [i for i, o in enumerate(sing_ops) if all(op_phase(x, o) == 0 for x in reps)]
            az = [i for i, o in enumerate(sing_ops) if all(z_phase(a, o) == 0 for a in zels)]
            chan_rows.append({
                'qd': str(qd), 'rep': nm, 'lab': str(lab), 'bl': str(bl), 'N': N,
                'surv': len(surv), 'coset': len(reps), 'ords': ords, 'expo': max(ords),
                'struct': ab_name(len(reps), ords),
                'cands': [(ab_tex(d), ab_element_orders(d)) for d in ab_groups(len(reps))],
                'cyc': max(ords) == len(reps), 'chars': len(chars), 'zchars': len(zchars),
                'same_char': chars == zchars, 'same_allow': af == az, 'allow': len(af),
                'nsing': len(sing_ops),
                'ss': len([x for x in reps if x[0] or x[1] or x[2]]),
                'fact': all(op_phase(x, o) == z_phase(x[3], o) for x in reps for o in sing_ops)})

    # ---- 正向对照：去掉"要是 SM 单态"这一步，中心判据还在不在做功
    def n_multiset(k):
        r"""$n$ 个符号取 $k$ 条的可重多重集数 $=\binom{n+k-1}{k}$（逐步整除，不走浮点）。"""
        r, nt = 1, len(FV) + k - 1
        for i in range(1, k + 1):
            r = r * (nt - k + i) // i
        fall = 1
        for i in range(k):
            fall *= nt - i
        assert r * math.factorial(k) == fall, '多重集计数 %d 与下降阶乘不符 (k=%d)' % (r, k)
        return r

    allc_tot = sum(n_multiset(k) for k in (2, 3, 4))
    ctl = []
    for qd in sorted(chans):
        N = int(Nres[str(qd)])
        zels = [F(k) / F(qd) for k in range(N)]
        nm0, lab0, bl0 = sorted(chans[qd], key=lambda t: (str(t[1]), str(t[2]),
                                                          names.index(t[0])))[0]
        surv = [x for x in C if cen_phase(x, lab0, bl0) == 0]
        reps = coset_reps(surv, G)
        allc = []
        for k in (2, 3, 4):
            for cs in itertools.combinations_with_replacement(sorted(FV), k):
                allc.append({'name': '+'.join(cs), 'k': k, 'per': [FV[n] for n in cs]})
        byk = [(k, sum(1 for o in allc if o['k'] == k)) for k in (2, 3, 4)]
        assert [b[1] for b in byk] == [n_multiset(k) for k in (2, 3, 4)], \
            '枚举出的多重集条数与公式不符：%s' % byk
        zo = [o for o in allc if all(z_phase(a, o) == 0 for a in zels)]
        fo = [o for o in allc if all(op_phase(x, o) == 0 for x in reps)]
        onzl_ops = [o for o in zo if not all(op_phase(x, o) == 0 for x in reps)]
        onlz = [o['name'] for o in onzl_ops]
        onlyf = [o['name'] for o in fo if not all(z_phase(a, o) == 0 for a in zels)]

        def cen_kind(o):
            r"""一条多重集在中心三项上的读数 $(\mathrm{tri}\bmod3,\ \sum l_L\bmod2,\ \sum l_R\bmod2)$。

            triality 取模 3 的判据与生成元约定无关：$p+2q\equiv0\pmod3\iff 2p+q\equiv0\pmod3$。
            """
            return (sum(ll[0] + 2 * ll[1] for (ll, bb) in o['per']) % 3,
                    sum(ll[2] for (ll, bb) in o['per']) % 2,
                    sum(ll[3] for (ll, bb) in o['per']) % 2)

        def pure_witness(o):
            """有没有一个 $t=0$ 的存活元（纯中心元）已经把它禁掉。"""
            return any(x[3] == 0 and op_phase(x, o) != 0 for x in surv)

        ctl.append({'qd': str(qd), 'N': N, 'carrier': nm0, 'all': len(allc), 'byk': byk,
                    'z': len(zo), 'f': len(fo), 'onlyz': len(onlz), 'onlyf': len(onlyf),
                    'ex': onlz[:4],
                    'kinds': sorted(set(cen_kind(o) for o in onzl_ops)),
                    'noncen': sum(1 for o in onzl_ops if cen_kind(o) == (0, 0, 0)),
                    'pure': sum(1 for o in onzl_ops if pure_witness(o)),
                    'allint': all(sum(bb for (ll, bb) in o['per']).denominator == 1
                                  for o in onzl_ops),
                    'disagree': sum(1 for o in allc
                                    if all(op_phase(x, o) == 0 for x in surv) !=
                                       all(op_phase(x, o) == 0 for x in reps)),
                    'sing_new': sum(1 for o in sing_ops if o['name'] in onlz)})

    gord = sorted(cen_order(x) for x in G)

    def swap3(x):
        r"""换色 $\mathbb Z_3$ 的生成元：$a_3\mapsto 2a_3$（同一个因子群的自同构）。"""
        return ((2 * x[0]) % 3, x[1], x[2], x[3])

    gconj = set(swap3(x) for x in gam['A']) == gam['B']
    by_struct = {}
    for r in chan_rows:
        by_struct.setdefault((r['qd'], tuple(r['struct'] or ())), []).append(r)
    bys = []
    for (qd, st), rs in sorted(by_struct.items(),
                               key=lambda kv: (kv[0][0], [x for x in kv[0][1]])):
        bys.append({'qd': qd, 'struct': list(st), 'n': len(rs), 'surv': rs[0]['surv'],
                    'coset': rs[0]['coset'], 'ords': sorted(rs[0]['ords']),
                    'cyc': rs[0]['cyc'], 'expo': rs[0]['expo'],
                    'cands': rs[0]['cands'], 'same': all(
                        r['same_char'] and r['same_allow'] and r['fact'] for r in rs),
                    'carriers': [(r['rep'], r['lab'], r['bl']) for r in rs]})
    GLOB.update({
        'nrep': len(names), 'nspec': len(spec), 'ncand': len(C), 'conv': cv,
        'convf': '$p+2q$' if cv == 'A' else '$2p+q$',
        'maxdim': max(r['dim'] for r in TABLE if r['name'] in NAMED),
        'uper': CEN_U_PER, 'tstep': CEN_T_DEN,
        'gden': sorted(set(F(k, CEN_T_DEN).denominator for k in range(CEN_T_DEN * CEN_U_PER))),
        'tden': sorted(set(x[3].denominator for x in G)),
        'gam': sorted(G, key=lambda x: (x[0], x[1], x[2], x[3])),
        'gampairs': [(x, cen_order(x)) for x in sorted(G, key=lambda x: (x[0], x[1], x[2], x[3]))],
        'gsizeA': len(gam['A']), 'gsizeB': len(gam['B']), 'gsame': gam['A'] == gam['B'],
        'gconj': gconj,
        'gords': gord,
        'gstruct': ab_name(len(G), gord), 'gall': ab_groups(len(G)),
        'gens6': sorted([x for x in G if cen_order(x) == 6], key=lambda x: x[3]),
        'gupure': [x for x in G if not (x[0] or x[1] or x[2])],
        'idx_h': i_10, 'fac_h': f_10[0], 'chk_h': f_10[1],
        'idx_422': i_422, 'fac_422': f_422[0], 'chk_422': f_422[1],
        'idx_hop': i_hop, 'fac_hop': f_hop[0], 'chk_hop': f_hop[1],
        'uBL': fracs(uBL), 'pQ': pQ, 'ngen': len(gen), 'forms': forms,
        'tens': [f['rep'] for f in forms if f['order'] == 1],
        'ord2': [f['rep'] for f in forms if f['order'] == 2],
        'ord4': [f['rep'] for f in forms if f['order'] == 4],
        'rows': chan_rows, 'bys': bys, 'ctl': ctl, 'sing': sing_sums, 'nsing': len(sing_ops),
        'nfv': len(FV), 'allc_tot': allc_tot,
        'nres': dict((k, int(v)) for k, v in Nres.items()),
        'chans': sorted(str(k) for k in chans),
        'ncar': dict((str(k), len(v)) for k, v in chans.items())})

    # ---- R12.0 整体形式：在场谱把群钉在 $Spin(10)$ 上，且"类为 0"有两条独立判法
    p &= ok('R12.0', '在场 %d 个表示的 $P/Q$ 类分三层：%s 在类 0（纯张量型，任何整体形式都容得下'
                    '它们）、%s 在 2 阶类（需要 $SO(10)$ 而不只是伴随群）、%s 在 4 阶类（只有单连通'
                    '的那个形式容得下）。$|P/Q|$ 由 Cartan 行列式独立给出 $=%d$，出现的类生成的子群'
                    r'大小 $=%d$ $\Rightarrow$ 商不掉任何非平凡中心：物质 $16_F$ 在 4 阶类 '
                    r'$\Rightarrow$ 群必须是 $Spin(10)$ 本身，"自然界取哪个形式"在本模型里不是自由'
                    '参数。两条判"在不在根格里"的路数（甲 最高权的单根坐标全整；乙 每条权重的 '
                    r'$\varepsilon$ 坐标全整且和为偶）逐表示同判'
             % (len(forms), plain_tex(GLOB['tens']), plain_tex(GLOB['ord2']),
                plain_tex(GLOB['ord4']), pQ, len(gen)),
             pQ == 4 and len(gen) == 4 and
             all(f['zeroA'] == f['zeroB'] for f in forms) and
             all(f['zeroA'] == (f['order'] == 1) for f in forms) and
             '16' in GLOB['ord4'] and '144' in GLOB['ord4'] and
             set(GLOB['tens']) == set(f['rep'] for f in forms if f['zeroA']) and
             all(f['order'] == 1 for f in forms if f['rep'] in ('45', '54', '210')) and
             all(f['order'] == 2 for f in forms if f['rep'] in ('10', '120', '126')),
             '各表示 (类, 阶, 两条判法) %s' % [(f['rep'], f['order'], f['zeroA'], f['zeroB'],
                                               f['nwt']) for f in forms])

    # ---- R12.1 覆盖核：显式枚举
    pure = GLOB['gupure']
    o2 = [x for x in G if cen_order(x) == 2]
    o3 = [x for x in G if cen_order(x) == 3]
    p &= ok('R12.1', '在 %d 个候选中心元上逐个试"对在场谱的每一条 3221 分量都平凡"，活下来 %d 个 '
                    r'$\Rightarrow$ 覆盖群到 $Spin(10)$ 的核 $\Gamma$ 数出来了。它**不是**把某个 '
                    r'$U(1)$ 子群商掉的东西：形如 $(0,0,0,t)$ 的存活元只有单位元那一个（读出 %d 个）'
                    r'$\Rightarrow$ 它是中心与 $U(1)$ 的**对角**粘合。结构：各元的阶 %s $\Rightarrow$ '
                    r'把这份阶分布交给"穷举该阶上全部阿贝尔群、比对元素阶多重集"那一步，唯一命中 %s'
                    r'（$%d$ 个生成元 $\Rightarrow$ 确实是循环群）；那个唯一的 2 阶元 %s 把两个 '
                    r'$\mathbb Z_2$ 中心**同时**非平凡地带上、还配一个半整数的 $t$，两个 3 阶元 %s '
                    r'各自带色中心配 $t$ $\Rightarrow$ 它不是"中心各因子随便取 6 个元"。两种 triality '
                    r'约定各给 %d / %d 元，作为候选网格里的点集它们 %s（甲 $p+2q$、乙 $2p+q$）；'
                    r'但把色 $\mathbb Z_3$ 的生成元换一次（$a_3\mapsto 2a_3$）之后两支严格互化：%s '
                    r'$\Rightarrow$ 核的大小与同构型不随"把哪个元叫 1"而变，变的只是那个称呼'
                    r'（本层沿 R10.4 从数据选定的 %s）。'
                    r'网格也够用：候选网格覆盖的 $t$ 分母有 '
                    r'%s，存活元实际只用 %s $\Rightarrow$ 没有元贴在网格最细的那一格上（分母 12 上零个）'
             % (len(C), len(G), len(pure), GLOB['gords'], ab_tex(GLOB['gstruct']),
                len(GLOB['gens6']),
                ctex(o2[0]) if len(o2) == 1 else '—（2 阶元不唯一：%s）' % len(o2),
                '、'.join(ctex(x) for x in o3), GLOB['gsizeA'], GLOB['gsizeB'],
                '相同' if GLOB['gsame'] else '**不同**',
                '成立' if GLOB['gconj'] else '**不成立**', GLOB['convf'],
                '、'.join(str(x) for x in GLOB['gden']),
                '、'.join(str(x) for x in GLOB['tden'])),
             len(G) == 6 and GLOB['gsizeB'] == 6 and GLOB['gconj'] and CEN_IDENT in G and
             all(cen_law(x, y) in G for x in G for y in G) and
             GLOB['gords'] == [1, 2, 3, 3, 6, 6] and len(pure) == 1 and pure[0] == CEN_IDENT and
             len(o2) == 1 and o2[0][1:] == (1, 1, F(3, 2)) and
             all(x[0] and x[3] != 0 for x in o3) and len(o3) == 2 and
             len(GLOB['gens6']) == 2 and
             GLOB['tden'] == [1, 2] and max(GLOB['tden']) < max(GLOB['gden']) and
             set(GLOB['tden']) < set(GLOB['gden']) and
             GLOB['gstruct'] == [6] and len(GLOB['gall']) == 1,
             r'$\Gamma$ = %s' % '、'.join(ctex(x) for x in GLOB['gam']))

    # ---- R12.2 同一个数 $|\Gamma|$ 的三条出处
    p &= ok('R12.2', r'$|\Gamma|=%d$ 有三条出处。甲 权格指数 $[P_H:P_{10}]=%s$（$P_H$ 由 $\bar{\rho}$ '
                    '半单部分的基本权加上 $U(1)_{B-L}$ 的特征格方向 $u$ 生成，不变因子 %s）；'
                    '乙 上一节的显式中心元枚举 $=%d$；丙 经 $SU(4)$ 一侧的可乘性 '
                    r'$[P_H:P_{422}]\cdot[P_{422}:P_{10}]=%s\times%s=%s$。三条同数 $\Rightarrow$ '
                    r'$\Gamma$ 不是枚举出来的巧合。诚实登记：甲与丙共用同一套 Smith 标准形代码'
                    '（丙只是把同一台机器在中间格上多跑一次，它核对的是**格的嵌套**而不是新的算术），'
                    '只有乙与格无关。甲那条里 $u$ 的归一化是**量出来**的：取 $u=3(B-L)$ 时 $P_{10}$ '
                    r'根本不在 $P_H$ 里（生成元不在超格内 $\Rightarrow$ 直接返回"不给数"），取 '
                    r'$u=\frac{B-L}{4}$ 才包含 $\Rightarrow$ 这个 $1/4$ 不是抄来的约定'
             % (len(G), i_10, GLOB['fac_h'], len(G), i_422, i_hop,
                (i_422 or 0) * (i_hop or 0)),
             i_10 == len(G) == 6 and (i_422 or 0) * (i_hop or 0) == i_10 and
             i_422 == 2 and i_hop == 3 and GLOB['chk_h'] and GLOB['chk_422'] and
             GLOB['chk_hop'] and GLOB['fac_h'] == [1, 1, 1, 1, 6] and
             GLOB['fac_422'] == [1, 1, 1, 1, 2] and GLOB['fac_hop'] == [1, 1, 1, 1, 3],
             '$[P_H:P_{10}]$ 不变因子 %s；$[P_{422}:P_{10}]$ %s；$[P_H:P_{422}]$ %s；'
             r'$u$（$\varepsilon$ 基）$=%s$；三条路数 %s' %
             (GLOB['fac_h'], GLOB['fac_422'], GLOB['fac_hop'], GLOB['uBL'],
              (i_10, len(G), (i_422 or 0) * (i_hop or 0))))

    # ---- R12.3 破缺之后真正剩下的完整离散群
    bys = GLOB['bys']
    b1 = [b for b in bys if b['qd'] == '1']
    b2 = [b for b in bys if b['qd'] == '2']

    def ms_diff(a, b):
        """多重集差：$a$ 里比 $b$ 多出来的那些阶（取不同值、升序）。"""
        cnt = {}
        for x in b:
            cnt[x] = cnt.get(x, 0) + 1
        out = set()
        for x in a:
            if cnt.get(x, 0) > 0:
                cnt[x] -= 1
            else:
                out.add(x)
        return sorted(out)

    def cand_rej(b):
        """一个结构类里被实测排除的其他候选：连同双向差集（它比实测多什么、缺什么）。"""
        return [(nm, ms_diff(cord, b['ords']), ms_diff(b['ords'], cord))
                for nm, cord in b['cands'] if cord != b['ords']]

    ncand_all = sum(len(b['cands']) - 1 for b in bys)
    rej = [(ab_tex(b['struct']), nm, ex, mi) for b in bys for nm, ex, mi in cand_rej(b)]
    p &= ok('R12.3', r'对每个通道（$\Delta(B-L)$ 与承载它的表示）逐个数：存活群 $=$ 让 v.e.v. 不变的'
                    r'中心元 $\times$ $U(1)$ 元，再**商掉** $\Gamma$ 才是低能真正剩下的离散群。读数：'
                    r'$q_\Delta=1$ 那 %d 个承载者一律给 (存活 %s, 商后 %s)，$q_\Delta=2$ 那 %d 个给 '
                    r'(存活 %s, 商后 %s) $\Rightarrow$ 残留群的**大小**只挂在 $|\Delta(B-L)|$ 上，不挂在'
                    r'"是哪个表示把它破掉"上，且每个承载者都真的含 $\Gamma$（存活数是 $|\Gamma|=%d$ 的'
                    r'整数倍）。**但同构型挂在承载者上**：$q_\Delta=1$ 那一支只有 %d 个结构类（%s），'
                    r'$q_\Delta=2$ 那支分成 %d 个类（%s），而各类商后阶都是 %s $\Rightarrow$ 换一个 '
                    r'$\Delta(B-L)=2$ 的承载者就把残群换成另一个同阶异型的群——旧那句"每通道内部同数"'
                    r'只对**阶**成文。与 §9 的关系：完整的残留群恰是 R10 那个 $\mathbb Z_N$ 的'
                    r'两倍（%s、%s）$\Rightarrow$ 多出来的一半确实是新群元，**但**它在 §10 '
                    r'那 %d 条 SM 单态算符上与 $\mathbb Z_N$ 逐条同判：标的集合相同（%s）、允许集相同'
                    r'（%s）、且相位恒等因子化成 $t\cdot\sum_k(B-L)_k$（%s）；逐承载者、逐结构类都成文'
                    r'（%s）$\Rightarrow$ §10 的判决不随"选哪个表示去破 $B-L$"而变。结构也是定名而不是'
                    r'抄来的：把每个类里陪集代表元的阶分布交给"穷举该阶上全部阿贝尔群、比对元素阶多重集"'
                    r'这一步，%d 个类各自唯一命中（同阶上另有 %d 个候选）；被排除的候选连同它与实测的'
                    r'双向差集一起给出：%s'
             % (GLOB['ncar']['1'], uni(b['surv'] for b in b1), uni(b['coset'] for b in b1),
                GLOB['ncar']['2'], uni(b['surv'] for b in b2), uni(b['coset'] for b in b2),
                len(G), len(b1), '；'.join(class_tex(b) for b in b1),
                len(b2), '；'.join(class_tex(b) for b in b2),
                uni(b['coset'] for b in b2),
                r'$%s\to%s$' % (mth(ztex(GLOB['nres']['1'])), mth(ztex(2 * GLOB['nres']['1']))),
                r'$%s\to%s$' % (mth(ztex(GLOB['nres']['2'])), mth(ztex(2 * GLOB['nres']['2']))),
                NSING4,
                all(r['same_char'] for r in chan_rows),
                all(r['same_allow'] for r in chan_rows),
                all(r['fact'] for r in chan_rows),
                all(b['same'] for b in bys),
                len(bys), ncand_all,
                '；'.join('%s 那支：候选 %s 比实测多 %s、缺 %s' %
                          (st, nm, ex or '（无）', mi or '（无）') for st, nm, ex, mi in rej)
                or '（各阶上本来只有一个阿贝尔群，无从排除）'),
             bool(chan_rows) and len(b1) == 1 and len(b2) == 2 and
             all(r['struct'] for r in chan_rows) and
             [((tuple(b['struct']), b['cyc'], b['expo'])) for b in b1] == [((6,), True, 6)] and
             [((tuple(b['struct']), b['cyc'], b['expo'])) for b in b2] ==
             [((2, 6), False, 6), ((12,), True, 12)] and
             all(b['coset'] == 2 * GLOB['nres'][b['qd']] for b in bys) and
             all(b['surv'] % len(G) == 0 for b in bys) and
             all(r['coset'] == 2 * r['N'] for r in chan_rows) and
             all(r['same_char'] and r['same_allow'] and r['fact'] for r in chan_rows) and
             all(b['same'] for b in bys) and
             all(r['chars'] == r['zchars'] == 1 for r in chan_rows) and
             all(r['allow'] == r['nsing'] == NSING4 for r in chan_rows) and
             all(r['ss'] > 0 for r in chan_rows) and
             all(len([c for c in b['cands'] if c[1] == b['ords']]) == 1 for b in bys) and
             ncand_all == 2 and len(rej) == 2 and
             all(ex or mi for _st, _nm, ex, mi in rej) and
             all(None not in r['ords'] for r in chan_rows),
             '通道 %s；每通道承载者数 %s；(承载者, 存活, 陪集, 结构, 循环, 指数) %s；'
             r'每行的半单非平凡元 %s' %
             (GLOB['chans'], GLOB['ncar'], [(r['qd'], r['rep'], r['lab'], r['surv'],
                                             r['coset'], str(r['struct']), r['cyc'], r['expo'])
                                            for r in chan_rows],
              [(r['qd'], r['ss']) for r in chan_rows]))

    # ---- R12.4 单态片上"扩展为空"的机制
    bad_sums = [s for s in sing_sums
                if s['lL'] % 2 or s['lR'] % 2 or s['bl'].denominator != 1
                or s['bl'].numerator % 2 or s['tri'] % 3 != (-int(3 * s['bl'])) % 3]
    p &= ok('R12.4', '上一条那个"相同"不是巧合，本层把它拆成可判的求和：§10 那 %d 条算符每一条都'
                    r'满足 $\sum_k l_L$ 偶、$\sum_k l_R$ 偶、且 $\sum_k(B-L)_k$ 是**偶整数** '
                    r'$\Rightarrow$ 三个中心的相位各自恒等于 1，而剩下那半边正是 R11 已经在用的 '
                    r'$\mathbb Z_N$ $\Rightarrow$ "要求它是 SM 单态"这一步**已经**把中心那几关过掉了，'
                    r'完整残留群在这张片上给不出新禁戒。$\Gamma$ 的对角性在这里第二次起作用：色 triality'
                    r' $\sum_k(p_k+2q_k)$ 与 $\sum_k 3(B-L)_k$ 同余（符号由 R10.4 从数据选定）'
                    r'$\Rightarrow$ 色中心连"多出来"的机会都没有。反例条数（四种条件任一不满足）$=%d$'
             % (GLOB['nsing'], len(bad_sums)),
             len(bad_sums) == 0 and len(sing_sums) == NSING4 and
             all(s['bl'] == 0 or abs(s['bl']) == 4 for s in sing_sums) and
             all(s['lL'] % 2 == 0 and s['lR'] % 2 == 0 for s in sing_sums),
             r'每条算符的 $\sum(B-L)$、$\sum l_L$、$\sum l_R$、$\sum$triality %s'
             % [(s['name'], str(s['bl']), s['lL'], s['lR'], s['tri']) for s in sing_sums])

    # ---- R12.5 正向对照：中心判据确实活着
    c1 = next((c for c in ctl if c['qd'] == '1'), None)
    c2 = next((c for c in ctl if c['qd'] == '2'), None)

    def cf(c, k):
        return '—' if c is None else c[k]

    p &= ok('R12.5', r'"完整群与 $\mathbb Z_N$ 同判"必须能区分**无从谈起**与**真的相同** $\Rightarrow$ '
                     '把"要是 SM 单态"那一步去掉，拿 %d 个物质场在尺寸 2,3,4 上的全部 %d 条多重集'
                     r'（按尺寸分：$k=2,3,4$ 各 %s 条，与可重组合的公式 $=%d$ 对上）重跑同一条判据：'
                     r'$q_\Delta=1$ 通道 $\mathbb Z_N$ 允许 %s 条、完整群只允许 %s 条；'
                     r'$q_\Delta=2$ 通道 %s 对 %s $\Rightarrow$ 中心那一半**在起决定作用**。'
                     r'被禁的那批也是逐条查过的：$\sum_k(B-L)_k$ 全是整数（$\mathbb Z_N$ 那关全过 %s），'
                     r'中心三项 $(\mathrm{tri}\bmod3,\sum l_L\bmod2,\sum l_R\bmod2)$ 取值为 %s，'
                     r'三项全平价的条数 $=%s+%s$，而有纯中心（$t=0$）见证元的条数 $=%s+%s$ 恰等于被禁'
                     r'总数 $=%s+%s$ $\Rightarrow$ 禁它们的确实是中心那三项（例：%s）。'
                     r'反向的空集同样数过：完整群允许而 $\mathbb Z_N$ 不允许的条数两通道合计 %s '
                     r'$\Rightarrow$ §9/§10 边界里那句"禁戒不会变松"是**读数**而不是承诺；而那 %d 条'
                     r'单态算符里被完整群新禁掉的条数 $=%s$ $\Rightarrow$ "变严"这一支确实整个落在'
                     r'单态片之外。最后，"逐陪集代表元试"与"逐个存活元试"在这 %d 条上同判的条数差 '
                     r'$=%s$ $\Rightarrow$ 商群上"作用在代表元上"这件事没有偷工。'
             % (len(FV), cf(c1, 'all'),
                '、'.join('%d' % b for b in [x[1] for x in c1['byk']]) if c1 else '—', allc_tot,
                cf(c1, 'z'), cf(c1, 'f'), cf(c2, 'z'), cf(c2, 'f'),
                '；'.join(r'$q_\Delta=%s$ %s' % (c['qd'], '全过' if c['allint'] else '**有不过**')
                         for c in ctl),
                '；'.join(r'$q_\Delta=%s$：%s' %
                          (c['qd'], '、'.join('$(%d,%d,%d)$' % k for k in c['kinds']))
                          for c in ctl),
                cf(c1, 'noncen'), cf(c2, 'noncen'),
                cf(c1, 'pure'), cf(c2, 'pure'),
                cf(c1, 'onlyz'), cf(c2, 'onlyz'),
                '、'.join('$%s$' % x for x in cf(c1, 'ex')) if c1 else '—',
                sum(c['onlyf'] for c in ctl), NSING4,
                sum(c['sing_new'] for c in ctl), allc_tot * len(ctl),
                sum(c['disagree'] for c in ctl)),
             c1 is not None and c2 is not None and len(ctl) == 2 and
             all(c['onlyf'] == 0 for c in ctl) and all(c['onlyz'] > 0 for c in ctl) and
             all(c['f'] < c['z'] for c in ctl) and
             all(c['sing_new'] == 0 for c in ctl) and
             all(c['z'] >= NSING4 and c['f'] >= NSING4 for c in ctl) and
             all(c['all'] == allc_tot for c in ctl) and
             all(c['byk'] == [(k, n_multiset(k)) for k in (2, 3, 4)] for c in ctl) and
             all(c['allint'] and c['noncen'] == 0 and c['pure'] == c['onlyz'] for c in ctl) and
             all(c['disagree'] == 0 for c in ctl) and
             all(any(k != (0, 0, 0) for k in c['kinds']) for c in ctl),
             r'读数 (通道, 全组合, 仅 $\mathbb Z_N$ 允许, 完整群允许, 差集, 中心取值, 纯中心见证) %s'
             % [(c['qd'], c['all'], c['z'], c['f'], c['onlyz'], c['onlyf'],
                 c['kinds'], c['pure'], c['noncen'], c['disagree']) for c in ctl])
    # ---- R12.6 行序不变量：这张表要能被按行引用 ⇒ 打印次序必须由数据决定，不能由进程散列决定
    plain = [(r['qd'], r['lab'], r['bl']) for r in chan_rows]
    full = [(r['qd'], r['lab'], r['bl'], names.index(r['rep'])) for r in chan_rows]
    ncol = len(plain) - len(set(plain))
    p &= ok('R12.6', 'R12 那张承载者表会把多个表示印在同一个 $(\\mathrm{lab},B-L)$ 键上（$16$ 与 '
                    '$144$ 同为 $(0,0,0,1)$，且存活/商后/结构逐项同值）：只按 $(\\mathrm{lab},B-L)$ '
                    '排时有 %d 对并列 $\\Rightarrow$ 并列项的先后由 set 的散列序决定，于是每次跑换一次'
                    '行序，报告那张表和外部台账都不能按行引用。补上"表示在 `names` 里的名次"作第三键后'
                    ' %d 行的键互不相同、且打印次序 $=$ 键的升序 $\\Rightarrow$ 行序是由数据决定的确定序。'
                    '这里同时要求并列数不为 0 $\\Rightarrow$ 一旦这 %d 对并列从数据里消失，本判定自己'
                    '报**不成立**，不会被一个空话题蒙过去'
             % (ncol, len(chan_rows), ncol),
             ncol > 0 and len(set(full)) == len(full) and full == sorted(full),
             r'(通道, lab, $B-L$, 名次) 头 %d 行 %s；并列对数 %d' % (3, full[:3], ncol))
    return p


G422 = {}                   # 报告 §12 的原始读数（与门禁同源，不在报告里另算一遍）


def run_residual422_layer():
    r"""R13：把 422 链的残留"按 $SU(4)$ 权格重做"做成格上的读数。

    §9（R10）留过一条边界："走 422 链时 $B-L$ 不是独立因子（它坐在 $SU(4)_c$ 的 Cartan
    里）⇒ 那条链上的残留要按 $SU(4)$ 的权格重做，本节未做"；§11（R12）又留了一条"422
    一侧的 $\Gamma$ 只有格一条路"。本层用同一次计算把两条一起关掉：`SUB_422` 里
    $SU(4)_c$ 的单根不是 $A_3$ 链（第三条是 $\varepsilon_2+\varepsilon_3$）⇒ triality
    公式不能直接代 ⇒ 中心元必须先在那张权格上**数出来**。数法用**特征标向量**：中心元
    由它在 $SU(4)$ 三个基本权上的作用 $v=(v_1,v_2,v_3)\in(\mathbb Q/\mathbb Z)^3$ 决定，
    $v=A^{-1}m\ (\mathrm{mod}\ 1)$，$m$ 跑协权格 $\mathbb Z^3$ ⇒ 商掉行格是内置的，
    有限枚举、无 BFS。三问：
      (i) 色块中心在这张格上有几类、乘法结构、在场谱的核 ⇒ 与 R12 的格指数
          $[P_{422}:P_{10}]=2$ 跨路对账（那边是 Smith 标准形，这边是特征标枚举）；
      (ii) 这条链的 v.e.v. 通道有多少、逐通道商后残群是什么；
      (iii) 物质字称在这张格上能不能实现、mod 核之后是否唯一；§10 那 8 条 SM 单态算符
          在这条链上改不改判。
    三条算术路：甲 行标号（`branching` 直接给）、乙 逐权重（`ipp` 现投影到块单根）、
    丙 标准 triality 约定的槽位映射 ⇒ 甲乙必须逐条同表，丙要么整体同号要么登记分歧。
    """
    p = True
    names = sorted(r['name'] for r in TABLE if r['name'] in NAMED)
    blk = SUB_422.simples[:3]
    A1L, A1R = SUB_422.simples[3], SUB_422.simples[4]

    # ---- 色块 Cartan：由根算（不抄表），逆矩阵当场用 A·A⁻¹=I 验双向
    A = [[int(2 * F(ip(blk[i], blk[j]), F(ip(blk[j], blk[j])))) for j in range(3)]
         for i in range(3)]
    detA = abs(g_det(A))
    snfA = g_snf(A)
    invA = inverse_rows(A)
    assert all(sum(F(A[i][k]) * F(invA[k][j]) for k in range(3)) == F(int(i == j))
               for i in range(3) for j in range(3)), '块 Cartan 的逆没有验成双向逆'

    # ---- 中心类：特征标向量 v=A⁻¹m (mod 1)，m 跑协格；v 即群元，加法 mod 1
    clsm = {}
    for mm in itertools.product(range(6), repeat=3):
        v = tuple(g_mod1(sum(F(invA[i][k] * mm[k]) for k in range(3))) for i in range(3))
        if v not in clsm or mm < clsm[v]:
            clsm[v] = mm
    V = sorted(clsm)
    vid = dict((v, i) for i, v in enumerate(V))
    assert V[0] == (F(0), F(0), F(0)), '单位元必须排在第一位'

    def vadd(a, b):
        return tuple(g_mod1(F(a[k]) + F(b[k])) for k in range(3))

    C = [(ci, aL, aR) for ci in range(len(V)) for aL in (0, 1) for aR in (0, 1)]

    def cadd(x, y):
        return (vid[vadd(V[x[0]], V[y[0]])], (x[1] + y[1]) % 2, (x[2] + y[2]) % 2)

    def corder(x, upto=60):
        y, n = x, 1
        while y != (0, 0, 0) and n <= upto:
            y = cadd(y, x)
            n += 1
        return n if y == (0, 0, 0) else None

    vord_pairs = [corder((ci, 0, 0)) for ci in range(len(V))]
    vords = sorted(vord_pairs)
    full_ords = sorted(corder(x) for x in C)

    def ph(c, h3, lL, lR):
        ci, aL, aR = c
        return g_mod1(sum(F(h3[k]) * V[ci][k] for k in range(3))
                      + F(aL * lL, 2) + F(aR * lR, 2))

    def sigA(labels):
        return tuple(ph(c, labels[:3], labels[3], labels[4]) for c in C)

    def sigB(mu):
        return tuple(ph(c, [ipp(mu, b) for b in blk], ipp(mu, A1L), ipp(mu, A1R))
                     for c in C)

    # 路丙：甲表里那个 4 阶元的特征标（分量分母都整除 4）与槽位映射的标准 triality 号
    ci4 = next(i for i in range(len(V)) if corder((i, 0, 0)) == 4)
    w4 = [int(4 * V[ci4][k]) for k in range(3)]

    def q_lat(lab):
        return sum(w4[k] * int(lab[k]) for k in range(3)) % 4

    def q_std(lab):
        return (int(lab[2]) + 2 * int(lab[0]) + 3 * int(lab[1])) % 4

    # ---- 在场谱 + 甲/乙/丙 三路交叉
    spec, misAB, misLab, tri_bad, tri_bad1 = {}, 0, 0, [], []
    for nm in names:
        ms = irrep(NAMED[nm])[1]
        for row in branching(ms, SUB_422):
            lab = tuple(row['labels'])
            wt = row['wt']
            if ([ipp(wt, b) for b in blk] != list(lab[:3]) or
                    ipp(wt, A1L) != lab[3] or ipp(wt, A1R) != lab[4]):
                misLab += 1
            if sigA(lab) != sigB(wt):
                misAB += 1
            if (3 * q_std(lab) - q_lat(lab)) % 4:
                tri_bad.append(lab)
            if (q_std(lab) - q_lat(lab)) % 4:
                tri_bad1.append(lab)
            spec.setdefault(lab, set()).add(nm)
    spec_rows = sorted(spec)
    uni_s3 = all((3 * q_std((a, b, c, 0, 0)) - q_lat((a, b, c, 0, 0))) % 4 == 0
                 for a in range(4) for b in range(4) for c in range(4))
    s1_bad = [lab for lab in spec_rows if (lab[1] + lab[2]) % 2]

    # ---- 核 K：对整个在场 422 谱平凡的群元
    sig_of = dict((k, sigA(list(k))) for k in spec_rows)
    sig2rows = {}
    for k in spec_rows:
        sig2rows.setdefault(sig_of[k], []).append(k)
    K = [c for i, c in enumerate(C) if all(sig_of[k][i] == 0 for k in spec_rows)]
    Kset = set(K)
    kords = sorted(corder(x) for x in K)

    # ---- v.e.v. 通道：$Q=0$ 且在中心下非平凡的在场权重
    chan = {}
    unmatched = 0
    for nm in names:
        ms = irrep(NAMED[nm])[1]
        for mu in ms:
            if chg(mu, QHP) != 0:
                continue
            sb = sigB(mu)
            if all(x == 0 for x in sb):
                continue
            rows = sig2rows.get(sb)
            if not rows:
                unmatched += 1
                continue
            d = chan.setdefault((nm, sb), {'nwt': 0, 'rows': sorted(rows)})
            d['nwt'] += 1

    chan_rows = []
    for (nm, sb), d in sorted(chan.items(),
                              key=lambda t: (names.index(t[0][0]), str(t[0][1]))):
        surv = [c for c in C if sb[C.index(c)] == 0]
        seen, reps422 = set(), []
        for x in surv:
            key = frozenset(cadd(k, x) for k in K)
            if key not in seen:
                seen.add(key)
                reps422.append(x)
        assert len(reps422) * len(K) == len(surv), \
            '陪集数 × 核大小 ≠ 存活数 @ %s' % nm
        ords = sorted(corder(x) for x in reps422)
        chan_rows.append({'rep': nm, 'rank': names.index(nm), 'sb': sb,
                          'rows': [[str(x) for x in r] for r in d['rows'][:3]],
                          'nrows': len(d['rows']), 'nwt': d['nwt'],
                          'surv': len(surv), 'quot': len(reps422), 'ords': ords,
                          'struct': ab_name(len(reps422), ords),
                          'cyc': max(ords) == len(reps422), 'expo': max(ords)})

    # ---- 物质场经 16_F 的权重桥到 422 行（同 R6.7 的跨链对象）
    def dom_rep(S, mu):
        for M, _sg in S.W.items():
            w = mat_vec(M, mu)
            if S.dominant(w):
                return S.labels(w)
        raise KeyError(mu)

    ms16 = irrep(NAMED['16'])[1]
    bridge, rowlab = {}, {}
    for mu in ms16:
        bridge.setdefault(dom_rep(SUB_3221, mu), set()).add(dom_rep(SUB_422, mu))
    for row in branching(ms16, SUB_3221):
        rowlab[row['labels']] = row['bl']

    FV = {}
    for f in SEL['mat']:
        keys = [lab for lab, bb in rowlab.items()
                if lab[:3] == tuple(f['lam']) and F(bb) == F(f['BL'])]
        assert len(keys) == 1, '场 %s 的 3221 桥行不唯一：%s' % (f['name'], keys)
        row42 = sorted(bridge[keys[0]])
        sigs = set(sigA(list(lab)) for lab in row42)
        assert len(row42) == 1 and len(sigs) == 1, \
            '场 %s 的 422 承载行或荷签名不唯一：%s' % (f['name'], row42)
        FV[f['name']] = {'row42': tuple(int(x) for x in row42[0]),
                         'sig': sigs.pop(), 'BL': F(f['BL']),
                         'mpp': g_mod1(F(3 * (-int(f['BL'].numerator)),
                                         2 * int(f['BL'].denominator)))}

    # ---- 物质字称的实现者：逐场相位等于 $(-1)^{3(B-L)}$ 的群元
    mp = [{'cand': c, 'order': corder(c)} for i, c in enumerate(C)
          if all(FV[k]['sig'][i] == FV[k]['mpp'] for k in sorted(FV))]

    # ---- SM 单态算符（与 §10 的 hit4 同一批，按名字核对）
    sing = sorted(set('+'.join(SEL['mat'][j]['name'] for j in combo)
                      for combo, n in SEL['r4'][0] if n > 0))
    hit4_names = sorted(x['name'] for x in SEL['hit4'])
    assert sing == hit4_names, \
        '本层的场内容类与 §10 的含单态类不是同一批：%s vs %s' % (sing, hit4_names)
    NSING = len(sing)

    def op_sig(name):
        tot = [F(0)] * len(C)
        for part in name.split('+'):
            s = FV[part]['sig']
            tot = [g_mod1(tot[i] + s[i]) for i in range(len(C))]
        return tot

    for r in chan_rows:
        surv = [c for c in C if r['sb'][C.index(c)] == 0]
        r['allow'] = [s for s in sing if all(op_sig(s)[C.index(c)] == 0 for c in surv)]
        r['nallow'] = len(r['allow'])

    # ---- 正向对照：去掉"要是 SM 单态"，判据还在不在做功
    fields = sorted(FV)
    multic = [cs for k in (2, 3, 4)
              for cs in itertools.combinations_with_replacement(fields, k)]

    def allowed_by(subset):
        ii = [C.index(c) for c in subset]
        return set(cs for cs in multic
                   if all(g_mod1(sum(FV[p]['sig'][i] for p in cs)) == 0 for i in ii))

    ctls = []
    for r in chan_rows:
        surv = [c for c in C if r['sb'][C.index(c)] == 0]
        full = allowed_by(surv)
        wko = allowed_by([c for c in surv if c[0] == 0])              # 只带弱中心的元
        clo = allowed_by([c for c in surv if c[1] == 0 and c[2] == 0])  # 只带色中心的元
        wcapc = wko & clo
        ctls.append({'rep': r['rep'], 'rank': r['rank'], 'all': len(multic),
                     'full': len(full), 'weak': len(wko), 'color': len(clo),
                     'ban': len(multic) - len(full),
                     'inter': full == wcapc, 'wcapc': len(wcapc),
                     'ex': sorted('+'.join(cs) for cs in multic if cs not in full)[:3]})
    allc_tot = len(multic)

    def n_ms(n, k):
        r = 1
        for i in range(1, k + 1):
            r = r * (n + k - i) // i
        return r

    formula = sum(n_ms(len(FV), k) for k in (2, 3, 4))

    byst = {}
    for r in chan_rows:
        byst.setdefault(tuple(r['struct'] or ()), []).append(r)
    bys = []
    for st, rs in sorted(byst.items(), key=lambda kv: list(kv[0])):
        assert all(r['surv'] == rs[0]['surv'] and r['quot'] == rs[0]['quot'] for r in rs)
        bys.append({'struct': list(st), 'n': len(rs),
                    'surv': rs[0]['surv'], 'quot': rs[0]['quot'],
                    'ords': sorted(rs[0]['ords']), 'cyc': rs[0]['cyc'],
                    'expo': rs[0]['expo'],
                    'carriers': [(r['rep'], r['rows'][0]) for r in rs]})

    struct_cnt = {}
    for r in chan_rows:
        k2 = tuple(r['struct'])
        struct_cnt[k2] = struct_cnt.get(k2, 0) + 1

    G422.update({
        'nrep': len(names), 'reps': names,
        'A': A, 'det': int(detA), 'snf': [int(x) for x in snfA],
        'ncls': len(V), 'classes': [[str(x) for x in v] for v in V],
        'canon': [list(clsm[v]) for v in V], 'vords': vords,
        'vord_pairs': vord_pairs, 'ncand': len(C),
        'cords': full_ords, 'cstruct': ab_name(len(C), full_ords),
        'nspec': len(spec_rows), 'misAB': misAB, 'misLab': misLab,
        'ci4': ci4, 'w4': w4, 'unis3': uni_s3,
        'tri_bad': [list(map(str, x)) for x in tri_bad],
        'tri_bad1': [list(map(str, x)) for x in tri_bad1],
        's1_pred': [list(map(str, x)) for x in s1_bad],
        'K': [list(x) for x in K], 'kords': kords,
        'idx_422': GLOB.get('idx_422'),
        'unmatched': unmatched, 'nchan': len(chan_rows),
        'nwt': sum(r['nwt'] for r in chan_rows),
        'rows': [{k: v for k, v in r.items() if k != 'sb'} for r in chan_rows],
        'bys': bys, 'nsing': NSING, 'sing': sing,
        'fv': dict((k, {'row42': list(map(str, v['row42'])),
                        'sig': [str(x) for x in v['sig']],
                        'BL': str(v['BL']), 'mpp': str(v['mpp'])})
                   for k, v in sorted(FV.items())),
        'mp': [{'cand': list(x['cand']), 'order': x['order']} for x in mp],
        'allc_tot': allc_tot, 'formula': formula,
        'ctl': ctls})

    # ---- R13.0 色块格与中心类的枚举
    p &= ok('R13.0',
            r'色块单根不是 $A_3$ 链（第三条是 $\varepsilon_2+\varepsilon_3$）⇒ 一切在'
            '它自己的格上重算：Cartan %s 由根算出、' % (G422['A'],)
            + r'$|\det|=%d$、Smith 不变因子 %s'
            r'$\Rightarrow$ 协权格商行格给 %d 个类；全群（类 $\times$ 弱 $\times$ 弱）阶分布 %s'
            '交给"穷举该阶上全部阿贝尔群、比对元素阶多重集"那一步唯一命中（ab 标准序升幂） '
            r'$\mathbb Z_2\times\mathbb Z_2\times\mathbb Z_4$：两个弱 $\mathbb Z_2$ 与色中心 '
            r'$\mathbb Z_4$ 的直积；%d 个候选群元对特征标加法封闭、每个阶都有数、单位元唯一 '
            r'$\Rightarrow$ 中心元的枚举是**有限**的特征标向量法：没有 BFS，也没有代 triality 公式'
            % (G422['det'], snfA, len(V), full_ords, len(C)),
            A == [[2, -1, -1], [-1, 2, 0], [-1, 0, 2]] and detA == 4 and
            snfA == [1, 1, 4] and len(V) == 4 and vords == [1, 2, 4, 4] and
            len(C) == 16 and all(x for x in full_ords) and
            ab_name(16, full_ords) == [2, 2, 4] and
            all(0 <= cadd(x, y)[0] < len(V) for x in C for y in C) and
            all(cadd((0, a, b), (0, c, d)) == (0, (a + c) % 2, (b + d) % 2)
                for a in (0, 1) for b in (0, 1) for c in (0, 1) for d in (0, 1)),
            'Cartan %s；det %s；SNF %s；类 %s；协格代表 %s；类阶 %s；全群阶 %s → %s' %
            (A, detA, snfA, [[str(x) for x in v] for v in V],
             [clsm[v] for v in V], vords, full_ords, G422['cstruct']))

    # ---- R13.1 同一张荷表的三条算术路
    p &= ok('R13.1',
            '同一张 16 列荷表有三条算术路：甲 直接用 `branching` 的行标号，乙 把每条权重'
            '经 ipp 现投影到块单根再算，丙 拿甲表里那个 4 阶元（特征标 $4v=%s$）对槽位映射的'
            % (w4,)
            + r'标准 triality 号 $q_{\rm std}=c+2a+3b$。读数：行标号 vs 逐权重错 %d 条、甲 vs 乙'
            '错 %d 条（在场 %d 行）；丙在全部 %d 行上满足 '
            r'$q_{\rm lat}\equiv 3q_{\rm std}\pmod 4$'
            '（错 %d 条，且该同余在 $[0,4)^3$ 上恒成立），而 '
            r'$q_{\rm lat}\equiv q_{\rm std}$'
            ' 在 %d 个不同行上失败 $\\Rightarrow$ 失败行恰是 '
            r'$b\not\equiv c\pmod 2$'
            ' 的那批（按奇偶预测 %d 行；违例含跨表示重复共 %d 条，去重后与预测集合相等）'
            r'$\Rightarrow$ triality 的符号约定在 422 这张格上也是**从数据选定**的'
            r'（与 R10.4 同族：引擎号 $s=3$，即逆）'
            % (misLab, misAB, len(spec_rows), len(spec_rows), len(tri_bad),
               len(set(tri_bad1)), len(s1_bad), len(tri_bad1)),
            misLab == 0 and misAB == 0 and len(spec_rows) == 30 and
            not tri_bad and uni_s3 and ci4 == 2 and w4 == [2, 1, 3] and
            sorted(set(tri_bad1)) == sorted(set(s1_bad)) and
            len(set(tri_bad1)) == 8 and len(tri_bad1) == 10,
            '甲乙错 %d/%d；行数 %d；$s=1$ 违例行 %s' %
            (misAB, misLab, len(spec_rows), [list(map(str, x)) for x in tri_bad1]))

    # ---- R13.2 在场谱的核：与 R12 格指数跨路对账
    p &= ok('R13.2',
            '对全部 %d 条在场 422 行逐行试"16 个群元哪个相位恒为 0"' % len(spec_rows)
            + r'$\Rightarrow$ 核 $K=%s$、$|K|=%d$、阶分布 %s $\Rightarrow$ 它是把 $SU(4)$'
            '中心元 $(0,0,2)$ 与两个弱 $\\mathbb Z_2$ **对角粘合**出来的那个 2 阶元，不是任一'
            '因子的直积元。这个数与 §11 的格指数 '
            r'$[P_{422}:P_{10}]=%s$ 跨路对账：那边是 Smith 标准形、这边是特征标枚举，两台机器'
            r'$\Rightarrow$ 两条链的核各有两条独立出处（3221 侧见 R12.2：6=2x3），且四数同值'
            % (G422['K'], len(K), kords, GLOB.get('idx_422')),
            K == [(0, 0, 0), (1, 1, 1)] and len(K) == 2 and
            GLOB.get('idx_422') == 2 and kords == [1, 2] and
            all(cadd(x, y) in Kset for x in Kset for y in Kset) and
            ab_name(2, kords) == [2],
            'K %s；阶 %s；R12 格指数 %s；在场 %d 个表示' %
            (K, kords, GLOB.get('idx_422'), len(names)))

    # ---- R13.3 v.e.v. 通道与逐通道商后残群
    neutral22 = [b for b in bys if tuple(b['struct']) == (2, 2)]
    p &= ok('R13.3',
            'v.e.v. 通道 $=$ 在场表示里 $Q=0$ 且在中心下非平凡的权重（按签名归并）：%d 条，'
            % len(chan_rows)
            + ('%d 个这样的权重全部落在谱行上（未落 %d 条）'
               r'$\Rightarrow$ 甲乙两套账合拢。商后残群取 %d 种同构型：%s'
               r'$\Rightarrow$ 与 3221 链（$\mathbb Z_6/\mathbb Z_2\times\mathbb Z_6/\mathbb Z_{12}$）'
               '同族结论、不同族读数：**大小只挂在签名上、同构型挂在承载者上**；其中 '
               r' %s 那一支恰落在 $SU(4)$ 中性 $(0,0,2)$ 行上的 %s 通道（$q_\Delta=2$ 的 '
               r'$\Delta_R$ 位）；每通道存活数 $=$ 商后 $\times\,|K|$'
               % (G422['nwt'], unmatched, len(bys),
                  '、'.join('%s：%d 条（存活 %d、商后 %d、阶 %s；承载 %s）' %
                            (ab_tex(b['struct']), b['n'], b['surv'], b['quot'], b['ords'],
                                   plain_tex(sorted(set(x[0] for x in b['carriers']))))
                            for b in bys),
                  ab_tex(neutral22[0]['struct']) if neutral22 else '—',
                  plain_tex(sorted(set(x[0] for x in neutral22[0]['carriers'])))
                  if neutral22 else '—')),
            len(chan_rows) == 14 and unmatched == 0 and len(bys) == 3 and
            struct_cnt == {(4,): 6, (2, 2): 2, (2,): 6} and
            all(r['struct'] and r['surv'] == r['quot'] * len(K) and
                r['surv'] % len(K) == 0 for r in chan_rows) and
            len(neutral22) == 1 and neutral22[0]['n'] == 2 and
            set(x[0] for x in neutral22[0]['carriers']) == {'126', '126̄'} and
            all(row[:3] == ['0', '0', '2'] for b in neutral22
                for _nm, row in b['carriers']),
            '通道 (承载者, 行数, 权重数, 存活, 商后, 结构, 循环) %s' %
            [(r['rep'], r['nrows'], r['nwt'], r['surv'], r['quot'], r['struct'],
              r['cyc']) for r in chan_rows])

    # ---- R13.4 物质字称：可实现，且 mod K 唯一
    p &= ok('R13.4',
            r'%d 个物质场各自的 422 承载行唯一、整行一个荷签名，且全部是奇 $3(B-L)$' % len(FV)
            + r'$\Rightarrow$ $(-1)^{3(B-L)}$ 的相位逐场都是 %s（与 R11 的荷账本同向）。'
            '逐群元试"作用在 %d 个场上等于 ' % ('1/2', len(FV))
            + r'$(-1)^{3(B-L)}$"$\Rightarrow$ 恰好 %d 个实现者（阶分布 %s）：'
            '$(0,1,1)$（两个弱中心）与 $(1,0,0)$（色中心 '
            r'$v=%s$）——两者相差核的非平凡元 $(1,1,1)$ $\Rightarrow$ **mod $K$ 唯一**'
            r'$\Rightarrow$ 这条链上物质字称不是"有没有"的问题，而是同一个陪集换代表元'
            % (len(mp), [x['order'] for x in mp],
               ','.join(str(x) for x in V[1])),
            len(FV) == 6 and all(v['mpp'] == F(1, 2) for v in FV.values()) and
            len(mp) == 2 and [tuple(x['cand']) for x in mp] == [(0, 1, 1), (1, 0, 0)] and
            all(x['order'] == 2 for x in mp) and cadd(mp[0]['cand'], K[1]) == mp[1]['cand'],
            '实现者 %s；逐场 (422 行, $B-L$, mpp) %s' %
            ([x['cand'] for x in mp],
             [(k, v['row42'], str(v['BL']), str(v['mpp'])) for k, v in sorted(FV.items())]))

    # ---- R13.5 8 条 SM 单态算符在这条链上逐通道全允许
    p &= ok('R13.5',
            '§10 那 %d 条含 SM 单态的 d=6 场内容类在本链是**同一批**类（按名字核对，'
            'assert 已钉）' % NSING
            + '⇒ 逐通道重跑判据：%d 条通道的允许数全部是 %s ' % (len(chan_rows),
                                                                 uni(r['nallow'] for r in chan_rows))
            + r'$\Rightarrow$ "残留群不保质子"不随选哪条链破 $B-L$ 而变：第二条链与第一条链'
              '（§11 的 R12.3 回判）逐条同判 '
              r'$\Rightarrow$ §10 的判决在两条链上都一个字不用改',
            NSING == 8 and all(r['nallow'] == NSING and r['allow'] == sing
                               for r in chan_rows),
            '逐通道允许数 %s；类 %s' % ([r['nallow'] for r in chan_rows], sing))

    # ---- R13.6 正向对照：判据在每条通道上都真的在禁东西
    exc = [c for c in ctls if not c['inter']]
    if len(exc) == 1:
        excpart = ('唯一例外是 %s 那条通道：它的存活群元不被"只弱/只色"两半生成，两半交集放到 %d 条、'
                   '逐元相位再收到 %d 条 '
                   % (exc[0]['rep'], exc[0]['wcapc'], exc[0]['full']))
        excpart += r'$\Rightarrow$ 对角型残群上"半群读数"严格粗于逐元读数（这条要记进边界）；'
    elif not exc:
        excpart = '全部通道都同判、无例外；'
    else:
        excpart = ('例外 %d 条（%s）——"恰好一条例外"的读数不再成立；'
                   % (len(exc), '、'.join(c['rep'] for c in exc)))
    p &= ok('R13.6',
            '判决"允许全部 %d 条"必须排除"判了 0 条"' % NSING
            + '⇒ 去掉"要是 SM 单态"那一步，拿 %d 个物质场在尺寸 2,3,4 上配成可重多重集' % len(FV)
            + r'（公式 $\binom{n+k-1}{k}$ 合计 %d 条，与枚举 %d 一致）逐通道重跑：'
            '全组允许 %s 条、被禁 %s 条 ⇒ 每条通道都禁了东西（最少的一支也禁 %d 条）。'
            % (formula, allc_tot, uni(c['full'] for c in ctls),
               uni(c['ban'] for c in ctls), min(c['ban'] for c in ctls))
            + '交集结构按**集合相等**判定而不是数数："全组允许 $=$ （只带弱中心的元允许）'
              r'$\cap$（只带色中心的元允许）"在 %d/%d 条通道成立；'
              % (sum(1 for c in ctls if c['inter']), len(ctls)) + excpart +
              '两半各有单独起作用的时候（弱半最多单独多禁 %d 条、色半 %d 条）'
              % (max(c['weak'] - c['full'] for c in ctls),
                 max(c['color'] - c['full'] for c in ctls)),
            allc_tot == formula == 203 and len(ctls) == 14 and
            all(c['all'] == allc_tot and c['ban'] > 0 and
                c['full'] >= NSING for c in ctls) and
            sum(1 for c in ctls if c['inter']) == 13 and
            [c['rep'] for c in exc] == ['210'] and
            all(c['wcapc'] == c['full'] for c in ctls if c['inter']) and
            exc[0]['wcapc'] == 147 and exc[0]['full'] == 126 and
            max(c['weak'] - c['full'] for c in ctls) > 0 and
            max(c['color'] - c['full'] for c in ctls) > 0 and
            min(c['ban'] for c in ctls) == 77 and max(c['ban'] for c in ctls) == 125,
            '(通道, 全组合, 全组允许, 弱半, 色半, 两半交集, 被禁) %s；例子 %s' %
            ([(c['rep'], c['all'], c['full'], c['weak'], c['color'], c['wcapc'],
               c['ban']) for c in ctls], [c['ex'] for c in ctls[:2]]))
    return p


G14 = {}                   # 报告 §13 的原始读数（与门禁同源，不在报告里另算一遍）

PW_DEN = (6, 12, 24, 60)   # $t$ 网格步长的四个分母：核会不会跟着网格走，逐档数出来


def run_perweight_layer():
    r"""R14：把 3221 侧中心元的枚举从"行标号"搬到"逐权重"，做成两套账的交叉读数。

    §11 那条边界的原文是"中心元的枚举只用行标号与 $B-L$，没有逐个展开多重集的权重
    $\\Rightarrow$ 它数的是'哪些中心元在整个在场谱上平凡'，与 §5 的逐权重分支是两套账"。
    本层不引入任何新的李论输入，只把那句话兑成读数：同一批候选中心元、同一个相位公式，
    把"对谁平凡"从行标号条件换成**逐权重**条件——标签走 `Subsystem.labels`（`ipp` 现投影到
    单根）、$B-L$ 走 `chg` 的点积，与 `branching` 的 Klimyk 交错和是两条互不共享算术的代码
    路径。三问：
      (i) 两套账各自的**形变**（一条条件即 $C\\to\\mathbb Q/\\mathbb Z$ 的一个特征标）集合
          是否相等——这是比"核相等"强得多的statement：核相等只要求两个集合一样大；
      (ii) 一条 3221 子多重态内部 $B-L$、Dynkin 标签、中心相位三件事是否恒定（三条判法走
          三条算术：点积 / Cartan 逆矩阵判整 / 生成元上的相位比对）；
      (iii) 核换不换数；那批条件里到底几条在起决定作用（冗余度）、把相位拆成两半各自要求
          平凡会留下什么（半条件对照）、$t$ 的网格步长是不是判据的一部分（四档对照）。
    """
    p = True
    names = sorted(r['name'] for r in TABLE if r['name'] in NAMED)
    cv = 'A' if RESID.get('triality_sign') == '+' else 'B'
    C = cen_elements()
    GEN = [(1, 0, 0, F(0)), (0, 1, 0, F(0)), (0, 0, 1, F(0)), (0, 0, 0, F(1, CEN_T_DEN))]

    def sig(lab, bl, c=None):
        r"""条件 $\\to$ 形变：它在四个生成元上的相位（$\\in(\\mathbb Q/\\mathbb Z)^4$）。"""
        return tuple(cen_phase(g, lab, bl, c or cv) for g in GEN)

    def phase_of(sc, x):
        r"""第三条算术路：只吃形变（生成元上的四个值）反读任意群元上的相位。"""
        return g_mod1(F(x[0]) * sc[0] + F(x[1]) * sc[1] + F(x[2]) * sc[2] +
                      F(int(x[3] * CEN_T_DEN)) * sc[3])

    # ---- 甲账：R12.1 那批行标号条件，原样重数一遍并当场与 §11 的产出对账
    ROWS = {}
    for nm in names:
        ROWS[nm] = [(tuple(r['labels']), F(r['bl']))
                    for r in branching(irrep(NAMED[nm])[1], SUB_3221)]
    nrow_all = sum(len(v) for v in ROWS.values())
    spec = sorted(set(pr for v in ROWS.values() for pr in v))
    owners = dict((k, [nm for nm in names if k in ROWS[nm]]) for k in spec)
    gam_row = dict((c, set(x for x in C
                     if all(cen_phase(x, lab, bl, c) == 0 for lab, bl in spec)))
                   for c in ('A', 'B'))
    G = gam_row[cv]

    # ---- 同态引理：形变（四个生成元上的值）唯一决定整格上的取值
    hom_bad = [(x, lab, bl) for x in C for lab, bl in spec
               if phase_of(sig(lab, bl), x) != cen_phase(x, lab, bl, cv)]
    charA = set(sig(*k) for k in spec)
    add_out = [(a, b) for a in sorted(charA) for b in sorted(charA)
               if tuple(g_mod1(F(a[i]) + F(b[i])) for i in range(4)) not in charA]

    # ---- 乙账：逐权重。标签与 $B-L$ 都由权重当场算，不取行标号
    A3221 = [[int(2 * ip(SUB_3221.simples[i], SUB_3221.simples[j]) /
                  ip(SUB_3221.simples[j], SUB_3221.simples[j])) for j in range(4)]
             for i in range(4)]
    invA3 = inverse_rows(A3221)
    assert all(sum(F(A3221[i][k]) * F(invA3[k][j]) for k in range(4)) == F(int(i == j))
               for i in range(4) for j in range(4)), '3221 半单 Cartan 的逆没验成双向逆'
    condB = {}
    nsub, ndwt, nwtm, nwtmn, nwt, dimsum = 0, 0, 0, 0, 0, 0
    bl_mis, root_mis, ph_mis = [], [], []
    name_rows = []
    for nm in names:
        ms = irrep(NAMED[nm])[1]
        mdim = sum(ms.values())
        dimsum += mdim
        wb, msub, mwtm, mwtmn, wrv, wsv = {}, 0, 0, 0, set(), set()
        for row in branching(ms, SUB_3221):
            sub = sub_irrep(row['wt'], SUB_3221)
            nsub += 1
            msub += 1
            ndwt += len(sub)
            lab0, bl0 = tuple(row['labels']), F(row['bl'])
            wrv.add(sig(lab0, bl0))
            for mu, k in sub.items():
                nwtm += k
                mwtm += k
                mwtmn += k * row['n']
                nwtmn += k * row['n']
                lab, bl = SUB_3221.labels(mu), chg(mu, BL)
                condB[(lab, bl)] = condB.get((lab, bl), 0) + 1
                wb[(lab, bl)] = wb.get((lab, bl), 0) + 1
                wsv.add(sig(lab, bl))
                if bl != bl0:
                    bl_mis.append((nm, lab0, lab, str(bl)))
                d = [int(lab0[i]) - int(lab[i]) for i in range(4)]
                if any(sum(F(invA3[i][j]) * d[j] for j in range(4)).denominator != 1
                       for i in range(4)):
                    root_mis.append((nm, lab0, lab))
                if any(cen_phase(g, lab, bl, cv) != cen_phase(g, lab0, bl0, cv) for g in GEN):
                    ph_mis.append((nm, lab0, lab))
        nwt += len(wb)
        name_rows.append({'rep': nm, 'nsub': msub, 'nwt': len(wb), 'nwtm': mwtm,
                          'nwtmn': mwtmn, 'dim': mdim, 'nrow': len(set(ROWS[nm])),
                          'chaR': len(set(sig(*k) for k in set(ROWS[nm]))),
                          'chaW': len(wsv), 'eq': wrv == wsv})
    charB = set(sig(*k) for k in condB)
    novel = sorted(set(condB) - set(spec))
    reps_n = [r['rep'] for r in name_rows if r['nwtmn'] != r['nwtm']]
    assert len(condB) == 365 and nwt == 663 and ndwt == 811, \
        '乙账对象数与探针读数不符：%d/%d/%d' % (len(condB), nwt, ndwt)
    assert all(r['nwtmn'] == r['dim'] for r in name_rows), \
        '逐表示的多重集对账不闭合：%s' % [r['rep'] for r in name_rows if r['nwtmn'] != r['dim']]

    # ---- 核：乙账（两约定）+ 第三条算术路（由形变反读）
    gam_wt = dict((c, set(x for x in C
                    if all(cen_phase(x, lab, bl, c) == 0 for lab, bl in condB)))
                  for c in ('A', 'B'))

    def mask(sc):
        m = 0
        for i, x in enumerate(C):
            if phase_of(sc, x) != 0:
                m |= 1 << i
        return m

    FULL = (1 << len(C)) - 1
    mC = dict((k, mask(sig(*k))) for k in spec)

    def ker_size(ms):
        u = 0
        for m in ms:
            u |= m
        return bin(FULL & ~u).count('1')

    gam_mask = dict((c, ker_size([mask(sig(lab, bl, c)) for lab, bl in spec]))
                    for c in ('A', 'B'))
    ess = [k for k in spec if ker_size([mC[y] for y in spec if y != k]) != len(G)]
    one_pin = [k for k in spec if ker_size([mC[k]]) == len(G)]
    one_min = min(ker_size([mC[k]]) for k in spec)
    pairs = [(a, b) for i, a in enumerate(spec) for b in spec[i + 1:]
             if ker_size([mC[a], mC[b]]) == len(G)]
    order, used = [], set()
    while ker_size([mC[k] for k in order]) != len(G) and len(order) < 8:
        best = min((k for k in spec if k not in used),
                   key=lambda k: (ker_size([mC[q] for q in order] + [mC[k]]), k[0], k[1]))
        order.append(best)
        used.add(best)
    core_ess = all(ker_size([mC[q] for q in order if q != k]) != len(G) for k in order)
    core_reps = sorted(set(n for k in order for n in owners[k]))
    pair_reps = sorted(set(n for ab in pairs for k in ab for n in owners[k]))

    # ---- 半条件对照：把相位拆成"半单部分"与"$U(1)_{B-L}$ 部分"各自要求平凡
    def half_s(x, lab):
        pp, qq, lL, lR = lab
        tri = (pp + 2 * qq) if cv == 'A' else (2 * pp + qq)
        return g_mod1(F(x[0] * tri, 3) + F(x[1] * lL, 2) + F(x[2] * lR, 2))

    Gs = set(x for x in C if all(half_s(x, lab) == 0 for lab, bl in spec))
    Gu = set(x for x in C if all(g_mod1(F(x[3]) * F(bl)) == 0 for lab, bl in spec))

    # ---- 网格对照：$t$ 的步长换档（乙账按形变去重后参与，条件与形变一一对应到核为止）
    repB = sorted(set(condB), key=lambda k: (sig(*k), k[0], k[1]))
    keep, seen = [], set()
    for k in repB:
        if sig(*k) not in seen:
            seen.add(sig(*k))
            keep.append(k)
    grid = []
    for den in PW_DEN:
        CC = [(a3, aL, aR, F(t, den)) for a3 in range(3) for aL in range(2)
              for aR in range(2) for t in range(den * CEN_U_PER)]
        ka = set(x for x in CC if all(cen_phase(x, lab, bl, cv) == 0 for lab, bl in spec))
        kb = set(x for x in CC if all(cen_phase(x, lab, bl, cv) == 0 for lab, bl in keep))
        grid.append({'den': den, 'ncand': len(CC), 'kA': len(ka), 'kB': len(kb),
                     'embed': G <= ka and G <= kb,
                     'same': ka == G and kb == G})

    G14.update({'cv': cv, 'ncand': len(C), 'nrep': len(names), 'nrow_all': nrow_all,
                'maxdim': GLOB.get('maxdim'),
                'nspec': len(spec), 'charA': len(charA), 'charB': len(charB),
                'hom_pairs': len(hom_bad) * 0 + len(C) * len(spec), 'hom_bad': len(hom_bad),
                'add_out': len(add_out), 'nsub': nsub, 'nwt': nwt, 'nwtm': nwtm,
                'ndwt': ndwt, 'nwtmn': nwtmn, 'reps_n': reps_n,
                'detA3': abs(g_det(A3221)),
                'dimsum': dimsum, 'ncond': len(condB), 'novel': len(novel),
                'eqAB': charA == charB, 'onlyA': len(charA - charB), 'onlyB': len(charB - charA),
                'name_rows': name_rows, 'eq_per_name': sum(1 for r in name_rows if r['eq']),
                'bl_mis': len(bl_mis), 'root_mis': len(root_mis), 'ph_mis': len(ph_mis),
                'gamA': len(gam_row['A']), 'gamB': len(gam_row['B']),
                'wtA': len(gam_wt['A']), 'wtB': len(gam_wt['B']), 'gam': len(G),
                'gam_mask': gam_mask[cv], 'gamMaskA': gam_mask['A'],
                'gamMaskB': gam_mask['B'], 'gam_r12': len(GLOB.get('gam') or []),
                'same_r12': gam_row[cv] == set(GLOB.get('gam') or []),
                'ess': len(ess), 'one_pin': len(one_pin), 'one_min': one_min,
                'pairs': len(pairs), 'pairs_tot': len(pairs) * 0 + len(spec) * (len(spec) - 1) // 2,
                'pair_reps': pair_reps, 'core': [[list(map(str, k[0])), str(k[1]), owners[k]]
                                                 for k in order],
                'core_len': len(order), 'core_ess': core_ess, 'core_reps': core_reps,
                'Gs': len(Gs), 'Gu': len(Gu), 'Gint': len(Gs & Gu), 'diag': len(G - (Gs | Gu)),
                'grid': grid, 'keepB': len(keep),
                'tden': sorted(set(x[3].denominator for x in G))})

    # ---- R14.0 形变这个坐标用得正当，且这批形变不是子群
    p &= ok('R14.0',
            r'一条 3221 条件 $(p,q,l_L,l_R)_{B-L}$ 给出 $C\to\mathbb Q/\mathbb Z$ 的一个特征标'
            r'$\Rightarrow$ 它由在四个生成元上的取值唯一决定。这条**同态引理**不是本层的假设：'
            '在全部 %d 个候选群元 $\\times$ %d 条形变条件共 %d 组上，把"由四个生成元的值整线性'
            '组合反读出来的相位"与 `cen_phase` 的原读法逐组比对，违例 %d $\\Rightarrow$ 本层拿那个'
            '四元组当"形变"的坐标是恒等而不是近似。读数：在场 %d 个表示的 %d 条 3221 分支行去重成'
            '%d 条条件，它们只给出 %d 种形变（一条子多重态内恒定，见 R14.2）。顺带一条否定读数：'
            '%d 对形变之和仍在这 %d 个里、%d 对不在 $\\Rightarrow$ 这批形变**不是**对偶群的子群，'
            '它只是荷表在中心格上的像（与 R13.6 那条"半群读数严格粗于逐元读数"同族）'
            % (len(C), len(spec), len(C) * len(spec), len(hom_bad), len(names), nrow_all,
               len(spec), len(charA), len(charA) ** 2 - len(add_out), len(charA), len(add_out)),
            not hom_bad and len(spec) == 61 and nrow_all == 99 and len(charA) == 24 and
            len(add_out) == 158 and len(charA) ** 2 - len(add_out) == 418 and
            len(C) * len(spec) == 26352 and len(G) == 6,
            '形变四元组（mod 1）%s；加法例外 %d 对' %
            ([[str(x) for x in v] for v in sorted(charA)], len(add_out)))

    # ---- R14.1 两套账合拢：形变集合相等（全局与逐表示）
    p &= ok('R14.1',
            '乙账（逐权重）把甲账那 %d 条分支行（即 %d 个子多重态）展开成权重：按子多重态去重 %d 条、'
            '按重数而不含行重数 %d 条。把每条权重当场兑成 $(3221$ 标签 $,B-L)$ 条件：逐表示去重 %d 条、'
            '全局去重 %d 条 $\\Rightarrow$ 其中 %d 条**根本不在**甲账那 %d 条行标号条件里'
            '（它们是子多重态的非最高权，行标号那本账看不见）$\\Rightarrow$ 乙账严格更细。但两套账'
            '的形变**按集合相等**：%d 种对 %d 种，乙独有 %d、甲独有 %d；而且 %d/%d 个表示'
            '**各自**的两套账也集合相等 $\\Rightarrow$ 多出来的那 %d 条条件一条也没有产生新的特征标'
            '。这正是 §11 那条边界的判决：它不是两本会给出不同答案的账，而是同一批 %d 个特征标的'
            '两种记法 $\\Rightarrow$ **第十三项登记的边界 (b) 就此关掉**'
            % (nrow_all, nsub, ndwt, nwtm, nwt, len(condB), len(novel), len(spec),
               len(charA), len(charB), len(charB - charA), len(charA - charB),
               sum(1 for r in name_rows if r['eq']), len(names), len(novel), len(charA)),
            charA == charB and novel and len(novel) == 304 and len(spec) == 61 and
            len(condB) == 365 and nsub == nrow_all == 99 and ndwt == 811 and nwt == 663 and
            len(charA) == len(charB) == 24 and
            not (charA - charB) and not (charB - charA) and
            sum(1 for r in name_rows if r['eq']) == len(names) == 11 and
            all(r['chaW'] == r['chaR'] for r in name_rows),
            '甲条件 %d/形变 %d；乙条件 %d/形变 %d；乙独有 %d；甲独有 %d；逐表示相等 %d/%d' %
            (len(spec), len(charA), len(condB), len(charB), len(charB - charA),
             len(charA - charB), sum(1 for r in name_rows if r['eq']), len(names)))

    # ---- R14.2 一条子多重态内部的三件恒等事（三条算术）+ 多重集对账
    p &= ok('R14.2',
            '子多重态内部必须恒定，而这三件事走三条互不共享算术的判法：甲 $B-L$ 用 `chg` 逐权重'
            '点积（该行是否整条落在同一个 $B-L$ 上）、乙 拿 3221 半单 Cartan 的逆矩阵判"行最高权'
            '减逐权重"的标签差**在不在根格里**（%s 由单根现算、$|\\det|=%d$，逆矩阵当场验成双向逆）、'
            '丙 相位在四个生成元上逐条比对。读数（%d 个子多重态、按子多重态去重 %d 条权重）：'
            '甲违例 %d、乙违例 %d、丙违例 %d $\\Rightarrow$ 三条同时为零 $\\Rightarrow$ "中心元在一条'
            '子多重态上作用为标量"是从权重格**算出来**的，不是行标号表的定义重述。另有三条算术'
            '之外的一条**多重集对账**：把逐权重账按行的重数 $n$ 求和得 %d 条，与母表示维数之和 %d'
            '（即 $\\sum_\\lambda \\dim V_\\lambda$）**逐项相等** $\\Rightarrow$ 乙账展开的确实就是母'
            '表示的权重多重集，不是一份自造的对象；不含 $n$ 的那份读数是 %d 条，两者之差 %d 条'
            '全部来自行重数 $n>1$ 的那几行（逐表示对账后落在 %s 上）。诚实登记：重数在本层只进这一'
            '条对账——相位是权重的标量函数，把一条条件重复 %d 次不会改变任何一次判定，所以本层是'
            '**跨实现的对账**而不是新发现 $\\Rightarrow$ 它关掉的是"两套账"这条边界，不是任何物理判断'
            % (A3221, abs(g_det(A3221)), nsub, ndwt, len(bl_mis), len(root_mis), len(ph_mis),
               nwtmn, dimsum, nwtm, dimsum - nwtm, '、'.join('$%s$' % x for x in G14['reps_n']),
               nwtm),
            A3221 == [[2, -1, 0, 0], [-1, 2, 0, 0], [0, 0, 2, 0], [0, 0, 0, 2]] and
            abs(g_det(A3221)) == 12 and not bl_mis and not root_mis and not ph_mis and
            nsub == 99 and ndwt == 811 and nwt == 663 and len(condB) == 365 and
            nwtm == 836 and nwtmn == dimsum == 877 and dimsum - nwtm == 41 and
            all(r['nwtmn'] == r['dim'] for r in name_rows) and
            all(r['nwt'] <= r['nwtm'] for r in name_rows) and
            sum(r['nwtm'] for r in name_rows) == nwtm and
            sum(r['dim'] for r in name_rows) == dimsum and
            G14['reps_n'] == ['120', '144', '210'] and
            sum(r['dim'] - r['nwtm'] for r in name_rows) == 41,
            'Cartan %s；$|\\det|=%d$；子多重态 %d；按子多重态去重权重 %d；按重数不含 $n$ %d；'
            '含 $n$ %d；母表示维数和 %d；违例 %d/%d/%d' % (
                A3221, abs(g_det(A3221)), nsub, ndwt, nwtm, nwtmn, dimsum,
                len(bl_mis), len(root_mis), len(ph_mis)))

    # ---- R14.3 换账不换群：三条路 + 两种约定 + 与 §11 逐元相等
    p &= ok('R14.3',
            '核：把"对甲账 %d 条行标号条件平凡"换成"对乙账 %d 条逐权重条件平凡"，两种 triality '
            '约定各数一遍 $\\Rightarrow$ 约定甲 %d 对 %d、约定乙 %d 对 %d（前 = 行标号账、'
            '后 = 逐权重账）$\\Rightarrow$ 两约定下都换账不换群。再走**第三条**算术路：完全不碰 '
            '`cen_phase`，只拿 %d 个形变按 R14.0 那条同态引理把整格相位反读出来取零点交集 '
            '$\\Rightarrow$ %d 个 $\\Rightarrow$ 三条路同一个集合，且与 §11 的 $\\Gamma$（%d 个）'
            '**逐元**相等 $\\Rightarrow$ 本层没有把 $\Gamma$ 数成第二个数，它数出来的是同一个'
            % (len(spec), len(condB), len(gam_row['A']), len(gam_wt['A']),
               len(gam_row['B']), len(gam_wt['B']), len(charA), gam_mask[cv], len(G)),
            gam_row['A'] == gam_wt['A'] and gam_row['B'] == gam_wt['B'] and
            gam_mask['A'] == gam_mask['B'] == len(G) and
            len(gam_row['A']) == len(gam_row['B']) == 6 and
            gam_row[cv] == set(GLOB.get('gam') or []) and
            len(C) == GLOB.get('ncand') == 432 and cv == GLOB.get('conv') and
            len(spec) == GLOB.get('nspec'),
            '候选 %d；核（行标号/逐权重/形变反读/R12）%d/%d/%d/%d；约定 %s' %
            (len(C), len(gam_row[cv]), len(gam_wt[cv]), gam_mask[cv],
             len(GLOB.get('gam') or []), cv))

    # ---- R14.4 冗余度：钉住核只需要两条，但"哪两条"是算法的产物
    p &= ok('R14.4',
            '%d 条条件（%d 种形变）里"删一条就让核变大"的有 %d 条 $\\Rightarrow$ 条件集严重超定。'
            '单条最好的一条也只把核从 %d 收到 %d（$>\\Gamma$ 的 %d）$\\Rightarrow$ 没有任何一条荷'
            '条件单独钉得住 $\\Gamma$。贪心规则（每步取使核最小的一条，并列按标签与 $B-L$ 的字典序'
            '取第一个）%d 步到位，且到位后每删一条即变大 $\\Rightarrow$ 两条就够。但**核心不唯一**：'
            '满足"两条即钉住"的条件对共 %d 对（占 %d 对的 %.1f%%），它们涉及全部 %d 个在场表示，'
            '而贪心选出的那两条只挂在 %d 个表示上（%s）$\\Rightarrow$ "哪两条"是算法的产物、'
            '"两条就够"才是读数（这条按本仓库的规矩登记：winner 不能替 population 作证）'
            % (len(spec), len(charA), len(ess), len(C), one_min, len(G), len(order),
               len(pairs), len(pairs) * 0 + len(spec) * (len(spec) - 1) // 2,
               100.0 * len(pairs) / (len(spec) * (len(spec) - 1) // 2), len(pair_reps),
               len(core_reps), '、'.join('$%s$' % x for x in core_reps)),
            not ess and not one_pin and len(order) == 2 and core_ess and one_min == 12 and
            len(pairs) == 213 and len(pair_reps) == len(names) == 11 and
            core_reps == ['144', '16', '16̄'] and len(core_reps) < len(pair_reps) and
            len(pairs) * 0 + len(spec) * (len(spec) - 1) // 2 == 1830,
            '单条必需 %d；单条最小核 %d；两条即钉住 %d/%d 对；贪心核心 %s' %
            (len(ess), one_min, len(pairs), len(spec) * (len(spec) - 1) // 2,
             [[list(map(str, k[0])), str(k[1])] for k in order]))

    # ---- R14.5 半条件对照：那 6 个元全是两半互相抵消出来的
    p &= ok('R14.5',
            '把相位拆成两半各自要求平凡：只要求**半单部分**（色 $\mathbb Z_3$ 与两个弱 '
            r'$\mathbb Z_2$）平凡 $\\Rightarrow$ 活 %d 个；只要求 $U(1)_{B-L}$ **那半边**平凡 '
            r'$\\Rightarrow$ 活 %d 个；两半都要求 $\\Rightarrow$ 活 %d 个（就是 $\Gamma$）。'
            '两半之交只剩 %d 个（单位元）$\\Rightarrow$ **交比 $\Gamma$ 还小** $\\Rightarrow$ '
            r'$\Gamma$ 里除单位元外那 %d 个元在两半上都非平凡，它们靠 $U(1)_{B-L}$ 那一项'
            '与中心项**逐条互相抵消**才活下来 $\\Rightarrow$ R12.1 那句"它是中心与 $U(1)$ 的'
            '对角粘合"从此是一个**计数**读数，不是描述。存活元实际只用 $t$ 的分母 %s'
            % (len(Gs), len(Gu), len(G), len(Gs & Gu), len(G - (Gs | Gu)),
               '、'.join(str(x) for x in sorted(set(x[3].denominator for x in G)))),
            len(Gs) == 36 and len(Gu) == 12 and len(Gs & Gu) == 1 and
            Gs & Gu == set([CEN_IDENT]) and len(G - (Gs | Gu)) == 5 and
            all(x[1:] != (0, 0, 0) for x in G if x != CEN_IDENT) and
            sorted(set(x[3].denominator for x in G)) == [1, 2],
            '半单半边 %d；$U(1)$ 半边 %d；交 %d；全条件 %d；两半皆非平凡的核元 %d' %
            (len(Gs), len(Gu), len(Gs & Gu), len(G), len(G - (Gs | Gu))))

    # ---- R14.6 网格步长不是判据的一部分
    p &= ok('R14.6',
            r'$t$ 的网格步长是本层唯一的自由参数（默认 $1/%d$，周期 $%d$）。把它换成 %s 四档'
            r'$\Rightarrow$ 候选元数 %s，逐档重数核：甲账 %s、乙账 %s $\\Rightarrow$ 四档全部'
            '等于 $\Gamma$ 的 %d 个，且 $1/%d$ 那一档的核在原格里（旧核嵌入 %s）'
            r'$\Rightarrow$ 核既不随网格加密而变小、也不随粗化而变大 $\\Rightarrow$ "哪个元贴在'
            '网格最细那一格上"这种假象不存在（R12.1 那条"存活元只用分母 1、2"在这里以四档对照'
            '重验一遍；乙账按形变去重成 %d 条代表条件参与）'
            % (CEN_T_DEN, CEN_U_PER, '、'.join('$1/%d$' % d['den'] for d in grid),
               '、'.join(str(d['ncand']) for d in grid),
               '、'.join(str(d['kA']) for d in grid), '、'.join(str(d['kB']) for d in grid),
               len(G), CEN_T_DEN, '、'.join('成立' if d['embed'] else '**不成立**'
                                           for d in grid), len(keep)),
            len(grid) == 4 and all(d['same'] and d['embed'] and d['kA'] == d['kB'] == len(G)
                                   for d in grid) and
            [d['ncand'] for d in grid] == [216, 432, 864, 2160] and
            [d['den'] for d in grid] == list(PW_DEN) and len(keep) == len(charA) == 24,
            '步长 %s；候选 %s；甲核 %s；乙核 %s' %
            ([d['den'] for d in grid], [d['ncand'] for d in grid],
             [d['kA'] for d in grid], [d['kB'] for d in grid]))
    return p


BASIS = {}                   # 报告 §14 的原始读数（与门禁同源，不在报告里另算一遍）
BST_BINS = ((2, 0), (3, 0), (4, 0), (2, 1), (2, 2), (4, 1))
BST_CTL = ((2, 1), (3, 1), (4, 1))


def run_basis_layer():
    r"""R15：把**算符基的覆盖面**做成读数（关掉 09 第十二项边界 (iii) 的后半；文档侧登记为第十六项）。

    §10 那台判据只吃到"d=6 的四条物质场分量"，剩下的半句话是："含导数算符、含共轭场的高维
    算符、$\\nu^c$ 以外的轻子数破缺结构均未枚举"。本层把算符基换成

      * **字母表**：$16_F$ 的 6 条分量 $+$ 它们各自的共轭（$\\overline{16}_F$ 的分量，
        签名由 $(\\lambda,Y,B-L)\\mapsto(\\lambda^*,-Y,-(B-L))$ 给出，与 `sm_fields('16̄')`
        这条独立机器核对）$=12$ 个字母；
      * **档**：$(n_f,n_s)\\in\\{(2,0),(3,0),(4,0),(2,1),(2,2),(4,1)\\}$，即双线性到"两费米子
        $+$ 两标量"（$d=3\\dots6$）与"四费米子 $+$ 一标量"；
      * **洛伦兹账**：每个字母带一个 $SU(2)_C$ 指标（点号字母带带点指标），玻色块
        $\\varphi/(1,1)$、$\\partial_{\\alpha\\dot\\alpha}/(1{+}1,1{+}1)$、
        $F_{\\alpha\\beta}/(2{+}2,0)$、$\\bar F/(0,2{+}2)$ 各自带 $(u,d)$ 指标；能缩成洛伦兹
        标符的最小导数个数 $k_{\\min}$ 决定**真实维数** $d_{\\min}=\\tfrac32 n_f+n_s+k_{\\min}$。

    四条判据各自要回答一件事：共轭字母是否带来新东西（R15.2 的共轭对合）；洛伦兹指标账与
    $B-L$ 荷账是什么关系（R15.3 三台机器、R15.4 的"群禁 vs 指标禁"）；高维里有没有 $\\nu^c$
    以外的轻子数破缺结构（R15.5）；以及这一切挂在哪份标量谱上（R15.6）。
    """
    p = True
    chans = dict(('|%s|' % r['BL'], (F(r['BL']), r['N'])) for r in RESID['rows'])
    g0 = rat_gen(bl_values('16'))
    mat = SEL['mat']
    ms16 = irrep(NAMED['16'])[1]
    ms16b = irrep(NAMED['16̄'])[1]
    fld = dict((nm, sm_fields(nm)) for nm in
               sorted(set(r['name'] for r in TABLE if r['name'] in NAMED)))
    names = sorted(fld, key=lambda x: (len(x), x))

    # ---- R15.0 字母表：共轭场由独立机器给出，权重账与母表示严格相等
    cmap = dict(((sm_conj(f['lam']), -f['Y'], -f['BL']), f['name']) for f in mat)
    # 已有上标的字母名（$e^c$）不能直接再接一个 $^\\dagger$：那是 LaTeX 的双上标错误，
    # 所以并成单一上标 $e^{c\\dagger}$；无上标的（$Q$、$L$）保持 $Q^\\dagger$。
    conj_nm = lambda b: (re.sub(r'\^(\w+)$', r'^{\1\\dagger}', b) if '^' in b else b + '^\\dagger')
    und = [dict(f, dot=0) for f in mat]
    dot = [dict(g, dot=1, name=conj_nm(cmap[(g['lam'], g['Y'], g['BL'])]))
           for g in fld['16̄']]
    alpha = und + dot
    sig = lambda f: '%s|%s|%s|%d' % (f['lam'], f['Y'], f['BL'], 1 if f.get('boson') else 0)
    asig = set(sig(f) for f in alpha)
    involution = all(sm_conj(sm_conj(f['lam'])) == f['lam'] for f in alpha)
    part = madd(*[f['ms'] for f in alpha])
    allodd = all((3 * f_bl(f)).denominator == 1 and int(3 * f_bl(f)) % 2 for f in alpha)
    # 标量侧的拷贝账：种类清单 vs 母表示权重账（行重数 $n>1$ 与重复签名都在这里现形）
    gaps = []
    for nm in names:
        fl = fld[nm]
        c = collections.Counter((f['lam'], f['Y'], f['BL']) for f in fl)
        gaps.append((nm, len(fl), msum(madd(*[f['ms'] for f in fl])), msum(irrep(NAMED[nm])[1]),
                     sum(v - 1 for v in c.values() if v > 1),
                     sum(max(0, r['n'] - 1) * msum(sub_irrep(r['wt'], SUB_3221))
                         for r in branching(irrep(NAMED[nm])[1], SUB_3221))))
    BASIS.update({'alpha': [(f['name'], f['lam'], str(f['Y']), str(f['BL']),
                             str(3 * f_bl(f)), f['dot']) for f in alpha],
                  'asig': len(asig), 'involution': involution,
                  'part': (msum(part), msum(ms16) + msum(ms16b), part == madd(ms16, ms16b)),
                  'bl_conj': sorted(set((sig(f), sig(dict(g, dot=1)))
                                        for g in fld['16̄'] for f in mat
                                        if cmap[(g['lam'], g['Y'], g['BL'])] == f['name'])),
                  'gaps': gaps, 'chans': chans, 'g0': str(g0)}
                 )
    p &= ok('R15.0', '扩基的第一步是把"共轭场"从散文变成清单：$16_F$ 的 6 条分量各带一个点号字母'
                     '（$(\\lambda,Y,B-L)\\mapsto(\\lambda^*,-Y,-(B-L))$），而 $\\overline{16}_F$ '
                     '的分量由 §5 的分支规则**独立**展开 $\\Rightarrow$ 两条路给出的清单集合相等'
                     '（%d 条对 %d 条）；共轭两次回到自己 %s；12 个字母的权重多重集与 '
                     '$16_F\\oplus\\overline{16}_F$ 的**严格相等**（%d 条权重，不只是维数相加）；'
                     '12 条字母的 $3(B-L)$ 全是奇整数 %s $\\Rightarrow$ R11.4 那条"物质字称'
                     '$=(-1)^{\\text{费米子数}}$"从 6 条扩到 12 条仍然成立。$\\Rightarrow$ 字母表'
                     '是量出来的。**拷贝账要明说**（右列读数）：`sm_fields` 给的是 $(\\lambda,Y,B-L)$ '
                     '**种类**清单，$\\overline{16}$ 与 $10_H$ 干净，$45_H/126/\\overline{126}$ 各有'
                     '一条重复签名，$120/144/210$ 因 3221 行重数 $n>1$ 少 %d/%d/%d 条权重 $\\Rightarrow$ '
                     '本层的类判定只依赖签名（R15.1 逐组核对），凡按拷贝加权的结构计数只在'
                     '纯费米子三档上与特征标路线核对' %
            (len(dot), len(fld['16̄']), '成立' if involution else '**不成立**', BASIS['part'][0],
             '成立' if allodd else '**不成立**',
             [g[5] for g in gaps if g[0] == '120'][0], [g[5] for g in gaps if g[0] == '144'][0],
             [g[5] for g in gaps if g[0] == '210'][0]),
            len(alpha) == 12 and len(asig) == 12 and len(dot) == 6 and involution and
            BASIS['part'][2] and allodd and
            sorted((f['lam'], f['Y'], f['BL']) for f in dot) ==
            sorted((f['lam'], f['Y'], f['BL']) for f in fld['16̄']) and
            all(g[3] == g[2] for g in gaps if g[0] in ('10', '16', '16̄')) and
            [g[5] for g in gaps if g[0] == '144'] == [12] and
            [g[4] for g in gaps if g[0] == '45'] == [1],
            '字母表：%s；重复签名 %s；行重数缺口 %s' %
            ([(a[0], a[1], a[2], a[3], a[4]) for a in BASIS['alpha']],
             [(g[0], g[4]) for g in gaps if g[4]], [(g[0], g[5]) for g in gaps if g[5]]))

    # ---- 机器：档内枚举 + 洛伦兹账（三条互不共享算术的实现）
    X = madd(ms16, ms16b)
    cg_cache = {}

    def cg_j0(n):
        r"""$\\big(\\tfrac12\\big)^{\\otimes n}$ 里自旋 0 的重数：$j$-加法三角形递推（只加、不判奇偶）。"""
        if n in cg_cache:
            return cg_cache[n]
        book = {0: 1}
        for _i in range(n):
            nb = collections.Counter()
            for jj, k in book.items():
                for j2 in (jj - 1, jj + 1):
                    if j2 >= 0:
                        nb[j2] += k
            book = dict(nb)
        cg_cache[n] = book.get(0, 0)
        return cg_cache[n]

    def cg_k(nu, nd, kmax=8):
        for k in range(kmax + 1):
            if cg_j0(nu + k) and cg_j0(nd + k):
                return k
        return None

    BLOCKS = {'$\\varphi$': (0, 0), '$\\partial$': (1, 1), '$F_{\\alpha\\beta}$': (2, 0),
              '$\\bar F_{\\dot\\alpha\\dot\\beta}$': (0, 2)}

    def cand(fl, fc, cs):
        x = sel_cand(fl, chans, g0)
        x['nu'] = sum(1 for f in fl if f.get('dot') == 0 and not f.get('boson'))
        x['nd'] = sum(1 for f in fl if f.get('dot') == 1)
        # R17：全同费米子的判据要按**名字**分组，所以两侧的名字清单本身得留在类记录里
        x['fnu'] = [f.get('name', f['rep']) for f in fl
                    if f.get('dot') == 0 and not f.get('boson')]
        x['fnd'] = [f.get('name', f['rep']) for f in fl if f.get('dot') == 1]
        x['par'] = (x['nu'] - x['nd']) % 2
        x['ok'] = x['par'] == 0                       # 甲：奇偶判据
        x['kk'] = cg_k(x['nu'], x['nd'])              # 乙：CG 对 $k$ 搜索
        x['kmin'] = None if not x['ok'] else x['nu'] % 2
        x['dmin'] = None if x['kmin'] is None else x['d'] + x['kmin']
        x['k'] = tuple(sorted(sig(f) for f in fl))
        x['scq'] = sum(3 * f_bl(f) for f in fl if f.get('boson'))
        x['cf'], x['cs'] = fc, cs
        x['pw'] = perm_weight(fc, len(fc)) * perm_weight(cs, len(cs))
        x['ver'] = tuple(sorted('%s:%s/%s/%s' % (t, v['甲'], v['乙'], v['丙'])
                                for t, v in x['v'].items()))
        return x

    def scan(nf, ns, pool, pre=True):
        out = []
        for fc in itertools.combinations_with_replacement(range(len(alpha)), nf):
            f1 = [alpha[i] for i in fc]
            for cs in itertools.combinations_with_replacement(range(len(pool)), ns):
                fl = f1 + [pool[i] for i in cs]
                if pre and (sum(f['Y'] for f in fl) != 0
                            or sum(f['lam'][0] - f['lam'][1] for f in fl) % 3):
                    continue
                x = cand(fl, fc, cs)
                if x['singlet']:
                    out.append(x)
        return out

    def pool_of(nms):
        return [dict(g, boson=True, dot=2, name='%s_H:%s' % (nm, g['row']))
                for nm in nms for g in fld[nm]]

    decl = pool_of(['10', '45'])
    key = lambda x: x['k']
    bkey = lambda bn: '%d,%d' % bn
    book = dict((bn, scan(*bn, decl)) for bn in BST_BINS)
    pos = dict((bn, len(book[bn])) for bn in BST_BINS)
    # 签名类的代表元：碰撞组内的读数在 R15.1(丙) 里被证明是同一份，故取首条即无损；
    # 按签名键排序，让报告里的样本行与 `wein` 的选法都不依赖枚举顺序
    rep = {}
    for bn in BST_BINS:
        first = {}
        for x in book[bn]:
            first.setdefault(x['k'], x)
        rep[bn] = [first[k] for k in sorted(first)]
    cls = dict((bn, len(rep[bn])) for bn in BST_BINS)
    struct = dict((bn, sum(x['singlet'] * x['pw'] for x in book[bn])) for bn in BST_BINS)

    # ---- R15.1 枚举本身要两台机器：预筛 vs 全枚举、逐类 vs 整乘积特征标
    full = []
    for bn in ((2, 0), (3, 0), (4, 0), (2, 1)):
        fl = scan(*bn, decl, pre=False)
        a, b = set(map(key, book[bn])), set(map(key, fl))
        full.append((bn[0], bn[1], pos[bn], len(a), len(fl), len(b), a == b, len(a - b),
                     len(b - a)))
    route = []
    for n in (2, 3, 4):
        big = X
        for _i in range(n - 1):
            big = tprod(big, X)
        tot = sum(x['singlet'] * perm_weight(x['cf'], n) for x in book[(n, 0)])
        route.append((n, tot, sm_singlet_mult(big), tot == sm_singlet_mult(big)))
    byk = collections.defaultdict(list)
    for bn in BST_BINS:
        for x in book[bn]:
            byk[(bn, x['k'])].append(x)
    coll = dict((k, v) for k, v in byk.items() if len(v) > 1)
    cols = ('t3q', 'q', 'dB', 'dL', 'd', 'nu', 'nd', 'par', 'ok', 'kk', 'kmin', 'dmin',
            'scq', 'singlet', 'ver')
    faithful = all(len(set(tuple(str(x[c]) for c in cols) for x in v)) == 1
                   for v in coll.values())
    namemix = sum(1 for v in coll.values() if len(set(tuple(x['fl']) for x in v)) > 1)
    BASIS.update({'bins': [list(bn) for bn in BST_BINS],
                  'pos': dict((bkey(bn), pos[bn]) for bn in BST_BINS),
                  'cls': dict((bkey(bn), cls[bn]) for bn in BST_BINS),
                  'struct': dict((bkey(bn), struct[bn]) for bn in BST_BINS),
                  'full': full, 'route': route,
                  'collide': (sum(pos.values()), sum(cls.values()),
                              sum(len(v) - 1 for v in coll.values()), len(coll), faithful,
                              namemix),
                  'alpha': BASIS['alpha']})
    p &= ok('R15.1', '扩基本身的枚举要能被两台不共享算术的机器复核。(甲) 阿贝尔预筛（$\\sum Y=0$ '
                     '且 $\\sum_k(p_k-q_k)\\equiv0\\pmod3$）是**必要**条件：把它去掉、对全部场组合'
                     '现算 Klimyk 单态数，四档的类集合与预筛版**逐个相等**（%s）$\\Rightarrow$ '
                     '预筛不漏。注意这一条是**实测**、不是定理：只在本层用到的字母表与这些档上成立。'
                     '(乙) 结构总数（$\\sum$ 单态数 $\\times$ 档内排列数）与"先作整乘积特征标、'
                     '再一次投影"的路线在三个纯费米子档同数（%s）$\\Rightarrow$ "按场内容分类"与'
                     '"按特征标分类"在含共轭场的字母表上仍是同一件事。'
                     '(丙) 拷贝不可分辨带来的碰撞：位置类 %d 条 $\\to$ 签名类 %d 条（差 %d 条，'
                     '集中在 %d 个键上，全部来自标量池里的重复签名）。这些碰撞组里有 %d 组的两条'
                     '**场名字**确实不同（同一个 $(\\lambda,Y,B-L)$ 挂在 $45_H$ 的两行上），'
                     '但组内的**全部物理读数**（荷账、$3Q$、维数、$n_u/n_d$、$k_{\\min}$、'
                     '单态数、三条判决）逐项相同 %s $\\Rightarrow$ 下面凡按"类"计数的数都取'
                     '签名类的代表元，拷贝编号不参与判定；纯费米子三档无碰撞（位置类 $=$ 签名类），'
                     '故 (乙) 那条按拷贝加权的总数只在它们上面对' %
            ([(f[0], f[1], f[3], f[5], '相等' if f[6] else '**不等**') for f in full],
             [(r[0], r[1], r[2]) for r in route],
             BASIS['collide'][0], BASIS['collide'][1], BASIS['collide'][2], BASIS['collide'][3],
             namemix, '成立' if faithful else '**不成立**'),
            all(f[6] and f[7] == 0 and f[8] == 0 for f in full) and
            all(r[3] for r in route) and faithful and
            pos == {(2, 0): 8, (3, 0): 26, (4, 0): 79, (2, 1): 77, (2, 2): 555, (4, 1): 1038} and
            cls == {(2, 0): 8, (3, 0): 26, (4, 0): 79, (2, 1): 69, (2, 2): 478, (4, 1): 959} and
            all(cls[bn] == pos[bn] for bn in ((2, 0), (3, 0), (4, 0))) and
            sum(pos.values()) == 1783 and sum(cls.values()) == 1619 and
            BASIS['collide'][2] == 164 and BASIS['collide'][3] == 156 and namemix == 156,
            '各档（位置类, 签名类, 结构数）：%s；碰撞组数 %d' %
            (dict((bkey(bn), (pos[bn], cls[bn], struct[bn])) for bn in BST_BINS), len(coll)))

    # ---- R15.2 共轭半边只是电荷翻转孪生：类集上的对合
    conj_sig = lambda s: '%s|%s|%s|%s' % ((lambda t: (t[1], t[0], t[2]))(
        tuple(int(v) for v in s.split('|')[0].strip('()').split(','))),
        -F(s.split('|')[1]), -F(s.split('|')[2]), s.split('|')[3])
    sa = set(sig(f) for f in alpha)
    sp = set(sig(f) for f in decl)
    sl = sorted(sa | sp)
    used = sorted(set(s for bn in BST_BINS for x in book[bn] for s in x['k']))
    cs_map = dict((s, conj_sig(s)) for s in sl)
    closed = all(cs_map[cs_map[s]] == s and cs_map[s] in set(sl) for s in sl)
    clset = dict((k, x) for bn in BST_BINS for k, x in ((x['k'], x) for x in book[bn]))
    flipk = lambda k: tuple(sorted(cs_map[s] for s in k))
    cmiss = [k for k in clset if flipk(k) not in clset]
    cneg = [k for k in clset if k not in cmiss and F(clset[k]['t3q']) != -F(clset[flipk(k)]['t3q'])]
    cpar = [k for k in clset if k not in cmiss and
            (clset[k]['nu'], clset[k]['nd']) != (clset[flipk(k)]['nd'], clset[flipk(k)]['nu'])]
    cvd = [k for k in clset if k not in cmiss and
           [v['甲'] for v in clset[k]['v'].values()] !=
           [v['甲'] for v in clset[flipk(k)]['v'].values()]]
    und_only = [x for x in book[(4, 0)] if x['nd'] == 0]
    dot_only = [x for x in book[(4, 0)] if x['nu'] == 0]
    eq10 = set(tuple(x['fl']) for x in und_only) == set(tuple(x['fl']) for x in SEL['hit4'])
    pv = [x for x in book[(4, 0)] if x['dB'] != '0' and x['dL'] != '0']
    pv0 = [x for x in pv if x['q'] == '0']
    pvf = [x for x in pv if any(v['甲'] is False for v in x['v'].values())]
    BASIS.update({'conj': (len(sa), len(sp), len(sl), used == sl, closed, len(cmiss), len(cneg),
                           len(cpar), len(cvd), len(clset)),
                  'und_only': (len(und_only), eq10), 'dot_only': len(dot_only),
                  'prot6': (len(pv), len(pv0), len(pvf),
                            [(x['fl'], x['t3q'], x['dB'], x['dL']) for x in pv[:6]])})
    p &= ok('R15.2', '含共轭场的 d=6 块：签名类 %d 条（单态结构 %d 个），其中只取非点号字母的那 %d '
                     '条与 §10 的 %d 条**集合相等** %s $\\Rightarrow$ 扩基是**超集**、不是替换，'
                     '§10 那张表一个数也不用改。共轭半边带来新东西了吗？没有——它在类集上是一个'
                     '**对合**：字母表的 %d 个签名与在场标量池的 %d 个签名合成 %d 个，而全部类真正'
                     '用到的清单恰好就是这一份 %s；这 %d 个签名在 '
                     '$(\\lambda,Y,B-L)\\mapsto(\\lambda^*,-Y,-(B-L))$ 下封闭且两次回到自己（%s），'
                     '%d 条类里像不在类集里的 %d 条、$3Q$ 不反号的 %d 条、'
                     '$(n_u,n_d)$ 不互换的 %d 条、两条通道判决改变的 %d 条 $\\Rightarrow$ 四处全部'
                     '归零 $\\Rightarrow$ 点号字母给出的类恰是非点号类的**电荷翻转孪生**（只取点号'
                     '字母的那 %d 条就是 d=6 那 8 条的对偶）。'
                     '质子那一列在扩基下重数：$\\Delta B\\ne0$ 且 $\\Delta L\\ne0$ 的类 %d 条'
                     '（其中 $\\Delta(B-L)=0$ 的 %d 条），判决**全部允许**（被禁 %d 条）$\\Rightarrow$ '
                     '§10 那句"残留群不保质子"不是"字母表太小"的产物' %
            (cls[(4, 0)], struct[(4, 0)], len(und_only), len(SEL['hit4']),
             '成立' if eq10 else '**不成立**', len(sa), len(sp), len(sl),
             '相符' if used == sl else '**不相符**', len(sl),
             '成立' if closed else '**不成立**',
             len(clset), len(cmiss), len(cneg), len(cpar), len(cvd), len(dot_only),
             BASIS['prot6'][0], BASIS['prot6'][1], BASIS['prot6'][2]),
            eq10 and used == sl and len(sa) == 12 and len(sp) == 15 and len(sl) == 27 and
            len(und_only) == 8 and len(dot_only) == 8 and closed and not cmiss and
            not cneg and not cpar and not cvd and len(pv) == 20 and len(pvf) == 0 and
            len(pv0) == 12 and all(x['ok'] for x in pv),
            'd=6 质子荷类（场内容, $3Q$, $\\Delta B$, $\\Delta L$）前 6 条：%s' %
            [(x['fl'], x['t3q'], x['dB'], x['dL']) for x in pv[:6]])

    # ---- R15.3 导数账：奇偶公式 vs CG 搜索 vs 玻色块不变量
    bad = [x['fl'] for x in sum(rep.values(), [])
           if (x['kk'] is None) != (not x['ok']) or (x['kk'] is not None and x['kk'] != x['kmin'])]
    blk = [(b, k) for b, (u, d) in BLOCKS.items() for k in (1, 2, 3) if k * (u - d) % 2]
    prot = dict((bn, sum(1 for x in rep[bn] if not x['ok'])) for bn in BST_BINS)
    upl = dict((bn, sum(1 for x in rep[bn] if x['ok'] and x['kmin'])) for bn in BST_BINS)
    k0 = dict((bn, sum(1 for x in rep[bn] if x['ok'] and not x['kmin'])) for bn in BST_BINS)
    oddnf = dict((bn, sum(1 for x in rep[bn] if x['nf'] % 2)) for bn in BST_BINS)
    allok = all(not (x['ok'] and x['kk'] is None) for x in sum(book.values(), [])) and not bad
    bilin = [(x['fl'], x['nu'], x['nd'], x['kmin'], str(x['dmin']), x['t3q'], x['dB'], x['dL'],
              x['singlet']) for x in book[(2, 0)]]
    d3 = [b for b in bilin if b[4] == '3']
    d4 = [b for b in bilin if b[4] == '4']
    BASIS.update({'parity': (len(bad), len(blk), allok),
                  'cg': [int(cg_j0(n)) for n in range(8)],
                  'prot_upl': dict(('%d,%d' % bn, (cls[bn], prot[bn], upl[bn], k0[bn], oddnf[bn]))
                                   for bn in BST_BINS),
                  'bilin': bilin, 'blocks': BLOCKS})
    p &= ok('R15.3', '导数不是"以后再说"：洛伦兹账用三条互不共享算术的实现各数一次。'
                     '甲：$n_u-k$ 的奇偶判据（能缩成标符 $\\iff n_u\\equiv n_d\\pmod2$，'
                     '此时 $k_{\\min}\\equiv n_u$）；乙：把每个字母当成一个 $\\big(\\tfrac12,0\\big)$ '
                     '或 $\\big(0,\\tfrac12\\big)$、每个 $\\partial$ 当成 $\\big(\\tfrac12,\\tfrac12\\big)$，'
                     '用 $j$-加法三角形递推数 $\\big(\\tfrac12\\big)^{\\otimes n}$ 里自旋 0 的重数'
                     '（$n\\le8$ 的读数 %s），再对 $k=0\\dots8$ 搜索；丙：四类玻色块 '
                     '%s 对 $n_u-n_d$ 奇偶的改动（幂次 $\\le3$）$\\Rightarrow$ 违例 %d / %d 条，'
                     '三台机器同判。两件事由此分开：**绝对禁**（奇费米子数：$n_u-n_d$ 的奇偶'
                     '与玻色块无关 $\\Rightarrow$ 加多少导数都救不回来）与**上移**（偶费米子数但 '
                     '$n_u$ 为奇 $\\Rightarrow$ 要一个导数，真实维数 $+1$）。逐档读数（签名类, '
                     '绝对禁, 上移, 零导数）：%s $\\Rightarrow$ 全档 $=$ 绝对禁 $+$ 上移 $+$ 零导数，'
                     '而绝对禁**恰好**落在奇费米子数的那几档（档名 %s）：该些档合计类数 %d，其中奇费米子数 '
                     '%d，全部判禁 $\\Rightarrow$ "三费米子算符"这一整类在洛伦兹层就被禁掉，与荷账无关。'
                     '双线性档（%d 条，唯一能一眼看完的一档）里 %d 条要一个导数（$d_{\\min}=4$，就是动能项'
                     '$\\psi^\\dagger\\partial\\psi$）、%d 条零导数（$d_{\\min}=3$，'
                     '%s）$\\Rightarrow$ "可重整的质量项只有右手中微子那一条"现在是引擎自己'
                     '重推出来的，不再是引用的常识' %
            ([cg_j0(n) for n in range(8)],
             '、'.join('%s：$(u,d)=%s$' % (b, v) for b, v in sorted(BLOCKS.items())),
             len(bad), len(blk),
             '；'.join('$n_f=%d$、$n_s=%d$：%s' % (bn[0], bn[1],
                                                  (cls[bn], prot[bn], upl[bn], k0[bn]))
                       for bn in BST_BINS),
             '、'.join('$n_f=%d$、$n_s=%d$' % bn for bn in BST_BINS if bn[0] % 2) or '无',
             sum(cls[bn] for bn in BST_BINS if bn[0] % 2),
             sum(oddnf[bn] for bn in BST_BINS if bn[0] % 2),
             len(bilin), len(d4), len(d3), '、'.join('$%s$' % '+'.join(b[0]) for b in d3)),
            allok and not blk and all(cls[bn] == prot[bn] + upl[bn] + k0[bn]
                                      for bn in BST_BINS) and
            prot == {(2, 0): 0, (3, 0): 26, (4, 0): 0, (2, 1): 0, (2, 2): 0, (4, 1): 0} and
            upl == {(2, 0): 6, (3, 0): 0, (4, 0): 30, (2, 1): 37, (2, 2): 234, (4, 1): 448} and
            k0 == {(2, 0): 2, (3, 0): 0, (4, 0): 49, (2, 1): 32, (2, 2): 244, (4, 1): 511} and
            sum(upl.values()) == 755 and sum(k0.values()) == 838 and
            all((prot[bn] > 0) == (bn[0] % 2 == 1) for bn in BST_BINS) and
            all(oddnf[bn] == prot[bn] for bn in BST_BINS) and len(bilin) == 8 and
            len(d3) == 2 and len(d4) == 6 and
            all(b[4] == '3' and b[7] != '0' for b in d3) and
            all(b[4] == '4' and b[6] == '0' and b[7] == '0' for b in d4),
            '双线性档读数（场内容, $n_u/n_d$, $k$, $d_{\\min}$, $3Q$, $\\Delta B$, $\\Delta L$）：%s'
            % [(b[0], b[1], b[2], b[3], b[4], b[5], b[6], b[7]) for b in bilin])

    # ---- R15.4 指标账 vs 荷账：什么时候它们给出同一个禁戒集
    allc = sum(book.values(), [])

    def lkzf(lst):
        Lk = set(key(x) for x in lst if not x['ok'])
        Zf = set(key(x) for x in lst if any(v['甲'] is False for v in x['v'].values()))
        return Lk, Zf
    Lk6, Zf6 = lkzf(allc)
    ctl = []
    for tag, reps in (('$10_H+45_H$（声明）', []), ('$+126_H+\\overline{126}_H$', ['126', '126̄']),
                      ('$+144_H$', ['144']), ('$+16_H$', ['16'])):
        pool = decl + pool_of(reps)
        b = sum((scan(*bn, pool) for bn in BST_CTL), [])
        Lk, Zf = lkzf(b)
        scodd = set(key(x) for x in b if (3 * x['scq']).denominator == 1
                    and int(3 * x['scq']) % 2)
        oddp = any((3 * f_bl(f)).denominator == 1 and int(3 * f_bl(f)) % 2
                   for nm in reps for f in fld[nm])
        ctl.append({'tag': tag, 'pool': len(pool), 'cls': len(set(map(key, b))), 'lk': len(Lk),
                    'zf': len(Zf), 'onlyL': len(Lk - Zf), 'onlyZ': len(Zf - Lk),
                    'odd': oddp, 'mech': (Zf - Lk) == (scodd - Lk)})
    cen = dict((nm, sorted(set(str(3 * f_bl(f)) for f in fld[nm]
                               if (3 * f_bl(f)).denominator == 1))) for nm in names)
    oddrep = [nm for nm in names if any(int(x) % 2 for x in cen[nm])]
    mis = sorted(set(oddrep) ^ set(nm for nm in RESID['odd'] if nm in names))
    f144 = decl + pool_of(['144'])
    b144 = sum((scan(*bn, f144) for bn in BST_CTL), [])
    Lk4, Zf4 = lkzf(b144)
    coin_by_bin = {bkey(bn): (cls[bn], prot[bn],
                              sum(1 for x in rep[bn]
                                  if any(v['甲'] is False for v in x['v'].values())))
                   for bn in BST_BINS}
    BASIS.update({'coin': (len(Lk6), len(Zf6), Lk6 == Zf6, coin_by_bin),
                  'ctl': ctl, 'oddrep': oddrep, 'census_mis': mis,
                  'w144': [(x['fl'], x['t3q']) for x in b144
                           if key(x) in (Lk4 - Zf4)][:4]})
    p &= ok('R15.4', '把"群禁"与"指标禁"当两个集合摆在一起。六档全基（声明标量谱 $10_H/45_H$）：'
                     '指标禁 %d 条、群禁 %d 条，**集合相等** %s $\\Rightarrow$ 在这个字母表上残留'
                     '群的 $\\mathbb{Z}_2$ 半边**不带来**洛伦兹费米子字称之外的信息（$\\mathbb{Z}_3$ '
                     '半边早已被"要是 SM 单态"吃掉，§10/R11.8）。这条巧合是**条件读数**，条件就是'
                     '标量谱：逐档看（签名类, 指标禁, 群禁）%s。三个插入对照（单标量三档）$\\Rightarrow$ '
                     '%s $\\Rightarrow$ 巧合在**偶** $3(B-L)$ 的插入下保持（补 $126_H$ 不改判），'
                     '在**奇**的插入下**双向**分叉。机理不是修辞，是集合等式：$+144_H$ 那池里'
                     '"群禁不住而指标禁"的那批，与"标量半边 $\\sum3(B-L)$ 为奇"的那批 %s。'
                     '谁奇谁偶也是读数：在场 %d 个表示里含奇 $3(B-L)$ 分量的只有 %s，'
                     '且这与 R10.3 在 SO(10) **权重**层数出的那份例外清单**完全一致**（两层不一致 '
                     '%s 条）$\\Rightarrow$ "残留群 $=$ 物质字称"这句话的可信度挂在标量谱上，'
                     '而不是挂在群论上' %
            (BASIS['coin'][0], BASIS['coin'][1], '成立' if BASIS['coin'][2] else '**不成立**',
             '；'.join('档 $(n_f,n_s)$=%s：%s' % (bn, v)
                       for bn, v in sorted(BASIS['coin'][3].items())),
             '；'.join('%s：类 %d 指标禁 %d 群禁 %d 差 %d/%d（池 %d，该表示含奇分量 %s）' %
                       (c['tag'], c['cls'], c['lk'], c['zf'], c['onlyL'], c['onlyZ'],
                        c['pool'], '是' if c['odd'] else '否') for c in ctl),
             '相等' if ctl[2]['mech'] else '**不等**', len(names),
             '、'.join('$%s$' % x for x in oddrep), len(mis)),
            BASIS['coin'][2] and len(Lk6) == 26 and len(Zf6) == 26 and
            coin_by_bin == {'2,0': (8, 0, 0), '2,1': (69, 0, 0), '2,2': (478, 0, 0),
                            '3,0': (26, 26, 26), '4,0': (79, 0, 0), '4,1': (959, 0, 0)} and
            all((c['lk'] == c['zf'] and not c['onlyL'] and not c['onlyZ']) == (not c['odd'])
                for c in ctl) and
            [(c['cls'], c['lk'], c['zf']) for c in ctl] == [(1314, 286, 286), (3062, 636, 636),
                                                            (2960, 625, 1593), (1884, 413, 729)] and
            ctl[2]['onlyL'] == 339 and ctl[2]['onlyZ'] == 1307 and ctl[2]['mech'] and
            ctl[3]['mech'] and oddrep == ['16', '144', '16̄'] and not mis,
            '对照读数：%s；$+144_H$ 那池里"指标禁而群不禁"的样本：%s' %
            ([(c['tag'], c['cls'], c['lk'], c['zf'], c['onlyL'], c['onlyZ'], c['mech'])
              for c in ctl], BASIS['w144']))

    # ---- R15.5 d>6：$\\nu^c$ 以外的轻子数破缺结构
    dl = {}
    for bn in BST_BINS:
        rows = rep[bn]
        v = [x for x in rows if x['dB'] == '0' and x['dL'] != '0']
        dl[bn] = (len(rows), len(v), sum(1 for x in v if not any('nu' in n for n in x['fl'])),
                  collections.Counter(x['dL'] for x in v))
    b5 = [x for x in rep[(2, 2)] if x['dB'] == '0' and x['dL'] != '0']
    nonu = [x for x in b5 if not any('nu' in n for n in x['fl'])]
    wein = [x for x in nonu if 'L' in x['fl'] and x['dL'] == '2' and
            sum(1 for n in x['fl'] if n.startswith('10_H')) == 2]
    wein = wein[0] if wein else None
    wconj = clset.get(flipk(wein['k'])) if wein else None
    dl3 = [x for x in rep[(3, 0)] if x['dB'] == '0' and x['dL'] != '0']
    BASIS.update({'dl': dict(('%d,%d' % bn, (dl[bn][0], dl[bn][1], dl[bn][2],
                                             dict(dl[bn][3]))) for bn in BST_BINS),
                  'nonu': [(x['fl'], x['t3q'], x['dL'], x['singlet'],
                            [v['甲'] for v in x['v'].values()]) for x in nonu[:6]],
                  'wein': (wein['fl'], wein['t3q'], wein['dL'], wein['singlet'],
                           [v['甲'] for v in wein['v'].values()],
                           '在场' if wconj else '**缺席**'),
                  'dl3': (len(dl3), sum(1 for x in dl3 if not x['ok']))})
    p &= ok('R15.5', '"$\\nu^c$ 以外的轻子数破缺结构未枚举"这半句现在是读数。逐档数含 SM 单态的'
                     '签名类里 $\\Delta B=0$ 且 $\\Delta L\\ne0$ 的那批（类数, $\\Delta L\\ne0$ 条数, '
                     '其中不含任何 $\\nu^c$（含其共轭）的条数）：%s。$d=5$ 档 %d 条 $\\Delta L\\ne0$ '
                     '里 %d 条**完全不碰** $\\nu^c$，其 $\\Delta L$ 符号分布 %s $\\Rightarrow$ '
                     '共轭配对（R15.2）在这里可见。具名一条：$%s$（$3Q=%s$、$\\Delta L=%s$、单态数 '
                     '%d、两条通道判决 %s），它的共轭孪生 %s $\\Rightarrow$ 这就是 Weinberg 型'
                     '算符 $LLHH$ 在 SO(10) 权重格上的出处：它不需要 $\\nu^c$、不需要 $126_H$，'
                     '在场的 $10_H/45_H$ 就够。反面读数把这条与 §10 接上：$d=4$ 的三费米子档里 '
                     '$\\Delta L\\ne0$ 的 %d 条**全部**被洛伦兹账禁掉 %s $\\Rightarrow$ "轻子数破缺'
                     '从 $d=5$ 起"不是引文口径，是本层的 $d_{\\min}$ 读数' %
            ('；'.join('$n_f=%d$、$n_s=%d$：%s' % (bn[0], bn[1], dl[bn][:3])
                       for bn in BST_BINS), dl[(2, 2)][1], dl[(2, 2)][2],
             dict(dl[(2, 2)][3]),
             ' + '.join(wein['fl']), wein['t3q'], wein['dL'], wein['singlet'],
             BASIS['wein'][4], BASIS['wein'][5], BASIS['dl3'][0],
             '成立' if BASIS['dl3'][1] == BASIS['dl3'][0] else '**不成立**'),
            dl[(2, 2)][1] == 46 and dl[(2, 2)][2] == 12 and
            dl[(2, 2)][3] == {'2': 23, '-2': 23} and wein is not None and
            wconj is not None and wein['t3q'] == '-6' and
            all(v['甲'] is True for v in wein['v'].values()) and
            BASIS['dl3'][1] == BASIS['dl3'][0] == 22 and
            all(dl[bn][0] == cls[bn] for bn in BST_BINS),
            '不含 $\\nu^c$ 的 $d=5$ 样本（场内容, $3Q$, $\\Delta L$, 判决）：%s' % BASIS['nonu'])

    # ---- R15.6 覆盖面本身也要有边界：本层没覆盖什么
    maxd = max((str(x['dmin']) for x in sum(rep.values(), []) if x['dmin'] is not None),
               key=lambda s: F(s))
    mind = min((str(x['dmin']) for x in sum(rep.values(), []) if x['dmin'] is not None),
               key=lambda s: F(s))
    dotb = dict((bkey(bn), sum(1 for x in rep[bn] if x['nd'])) for bn in BST_BINS)
    BASIS.update({'cover': (len(BST_BINS), sum(cls.values()), str(mind), str(maxd), dotb,
                            sorted(set(CSPLIT['decl_union'])),
                            [n for n in ('126', '126̄', '144', '16') if n not in
                             set(CSPLIT['decl_union'])])})
    p &= ok('R15.6', '覆盖面登记成数，以免本层被读成"全部算符"：档 $=%s$（%d 档、签名类合计 %d 条、'
                     '$d_{\\min}$ 从 %s 到 %s）。含点号字母（即共轭场）的类**逐档都在场**：%s '
                     '$\\Rightarrow$ "共轭场"这一半已不再是散文。但边界同样要数出来：'
                     '(i) 导数只数到**最小** $k_{\\min}$，$\\partial^k$ 的完整塔'
                     '（以及由此带来的同一 $d_{\\min}$ 内多个独立收缩）没有枚举，(ii) 场的内容到 '
                     '$n_f=4$、标量插入到 $n_s=2$ 为止，$n_f\\ge5$ 与 $n_s\\ge3$ 未入门禁，'
                     '(iii) 判决仍只过**规范不变**这一关：Lorentz 收缩的具体形式、味指标、Fierz '
                     '恒等式三关都没过（与 §7 同一处置）$\\Rightarrow$ 类数不是算符数。'
                     '**条件性**照旧：本层的"在场标量谱"是 $10_H/45_H$，而 %s 都不在链探针字面声明'
                     '的谱里（链上声明的只有 %s）$\\Rightarrow$ R15.4 那条巧合是挂在偶荷标量谱上的'
                     '读数；$B-L$ 破缺承载者的缺位（R10.10/R11.10）原样下来。'
                     '本层不回填任何寿命、不改 P4／P7 的判据与分级' %
            ('、'.join('$n_f=%d$、$n_s=%d$' % bn for bn in BST_BINS), BASIS['cover'][0],
             BASIS['cover'][1], BASIS['cover'][2], BASIS['cover'][3],
             '；'.join('档 %s：%d/%d' % (bkey(bn), dotb[bkey(bn)], cls[bn])
                       for bn in BST_BINS),
             higgs_tex(BASIS['cover'][6]) or '无', higgs_tex(BASIS['cover'][5]) or '无'),
            BASIS['cover'][0] == 6 and BASIS['cover'][1] == 1619 and
            BASIS['cover'][2] == '3' and BASIS['cover'][3] == '8' and
            dotb == {'2,0': 7, '2,1': 53, '2,2': 356, '3,0': 22, '4,0': 71, '4,1': 872} and
            all(0 < v < cls[[bn for bn in BST_BINS if bkey(bn) == k][0]]
                for k, v in dotb.items()) and
            set(BASIS['cover'][6]) == {'126', '126̄', '144', '16'} and
            set(BASIS['cover'][5]) <= {'10', '45'},
            '覆盖读数：%s' % (BASIS['cover'],))

    # ---- R16 缩法重数：把"类数不是算符数"里 Lorentz 那一半数出来 ----------------
    # 类的枚举给出"有多少类"，但一类固定的是**自旋指标的多重集**，该类下 Lorentz
    # 不变张量空间的维数是另一个数：$n$ 个外尔指标接成标量的独立接法数
    # $=\\dim(V^{\\otimes n})^{SL(2)}$。四条路互不共享算术：$j\\pm1$ 递推（甲，引擎
    # 原有）、二项式差（乙）、钩长公式（丙）、显式 $\\varepsilon$ 张量代数（丁）。
    TSTEP = 3                       # 导数塔只数到 $k_{\\min}+2TSTEP$，故仍是截断
    NEXP = 6                        # 显式张量路线只做到 $n\\le6$（$2^6$ 个分量）
    okc = [x for bn in BST_BINS for x in rep[bn] if x['ok']]

    def mpat(x, k=None):
        """$k$ 阶导数后该类的缩法重数：两侧各自接成自旋 $0$ 的重数之积。"""
        kk = x['kmin'] if k is None else k
        return cg_j0(x['nu'] + kk) * cg_j0(x['nd'] + kk)     # 甲：$j\\pm1$ 递推

    def cat_rec(n):                                           # 甲
        return cg_j0(n)

    def cat_bin(n):                                           # 乙：闭式差
        return 0 if n % 2 else math.comb(n, n // 2) - math.comb(n, n // 2 + 1)

    def cat_hook(n):                                          # 丙：$f^{(m,m)}$
        if n % 2:
            return 0
        m = n // 2
        return math.factorial(2 * m) // (math.factorial(m + 1) * math.factorial(m))

    def q_rank(vecs):
        """$\\mathbb Q$ 上稀疏行阶梯的秩（精确分数，无浮点、无模约化）。"""
        piv = {}
        for v in vecs:
            row = dict((j, c) for j, c in enumerate(v) if c)
            while row:
                j = min(row)
                if j not in piv:
                    piv[j] = row
                    break
                base = piv[j]
                f = row[j] / base[j]
                for jj, cc in base.items():
                    row[jj] = row.get(jj, F(0)) - f * cc
                row = dict((jj, cc) for jj, cc in row.items() if cc)
        return len(piv)

    GEN = ({(0, 1): 1}, {(1, 0): 1}, {(0, 0): 1, (1, 1): -1})      # $E$、$F$、$H$

    def sl2_nullity(n):
        """丁（其一）：直接解 $X^{(1)}+\\cdots+X^{(n)}$ 对 $X=E,F,H$ 零化 $T$ 的方程组。
        一个方程 = 一个（生成元，输出多指标），系数沿**所有**位累加（对角余乘）。"""
        if n == 0:
            return 1
        dim = 1 << n
        rows = []
        for X in GEN:
            for t in range(dim):
                row = [F(0)] * dim
                for i in range(n):
                    bit = (t >> i) & 1
                    for (a, b), xv in X.items():
                        if a == bit:
                            row[t ^ (bit << i) ^ (b << i)] += F(xv)
                if any(row):
                    rows.append(row)
        return dim - q_rank(rows)

    def matchings(rest):
        """全部完全配对（$n-1$ 个方案数 $=(n-1)!!$）。"""
        if not rest:
            yield []
            return
        i = rest[0]
        for p in range(1, len(rest)):
            j = rest[p]
            for tail in matchings(rest[1:p] + rest[p + 1:]):
                yield [(i, j)] + tail

    def pairing_rank(n):
        """丁（其二）：把 $\\varepsilon$ 画线法当作张量写出，数其张成空间的秩。"""
        if n % 2:
            return 0, 0
        dim = 1 << n
        eps = {(0, 1): F(1), (1, 0): F(-1)}
        vecs, ms_n = [], 0
        for ms in matchings(list(range(n))):
            ms_n += 1
            vec = [F(0)] * dim
            for t in range(dim):
                v = F(1)
                for a, b in ms:
                    e = eps.get((((t >> a) & 1), ((t >> b) & 1)))
                    if e is None:
                        v = F(0)
                        break
                    v *= e
                vec[t] = v
            vecs.append(vec)
        return ms_n, q_rank(vecs)

    nmax = max(max(x['nu'], x['nd']) + x['kmin'] + 2 * TSTEP for x in okc)
    tri = [n for n in range(nmax + 1) if not (cat_rec(n) == cat_bin(n) == cat_hook(n))]
    # 丁：显式张量代数只做 $n\\le NEXP$（$2^{6}=64$ 个分量、精确分数消元）
    t4 = []
    for n in range(NEXP + 1):
        npair, prank = pairing_rank(n)
        t4.append((n, cat_rec(n), sl2_nullity(n), npair, prank, npair - prank))
    nkmax = max(max(x['nu'], x['nd']) + x['kmin'] for x in okc)
    tbad = [r for r in t4 if not (r[1] == r[2] == r[4] and r[4] <= r[3])]
    # 结构式（不看数、只看形状）：重数为 $1$ 当且仅当两侧指标数都不超过 $2$
    sid = [x['k'] for x in okc if (mpat(x) == 1) !=
           (x['nu'] + x['kmin'] <= 2 and x['nd'] + x['kmin'] <= 2)]
    # 塔的奇偶：$k$ 与 $k_{\\min}$ 奇偶不同时无不变量；同奇偶则每层都非零且不降
    par_t = [x['k'] for x in okc if mpat(x, x['kmin'] + 1) != 0 or
             any(mpat(x, x['kmin'] + 2 * i) == 0 for i in range(TSTEP + 1))]
    mono = [x['k'] for x in okc for i in range(TSTEP)
            if mpat(x, x['kmin'] + 2 * i) > mpat(x, x['kmin'] + 2 * (i + 1))]
    strict = sum(1 for x in okc if mpat(x, x['kmin'] + 2 * TSTEP) > mpat(x))
    tw = [(2 * i, sum(mpat(x, x['kmin'] + 2 * i) for x in okc),
           sum(1 for x in okc if mpat(x, x['kmin'] + 2 * i) > 1))
          for i in range(TSTEP + 1)]
    mult = {}
    for bn in BST_BINS:
        v = [mpat(x) for x in rep[bn] if x['ok']]
        hi = [x for x in rep[bn] if x['ok'] and mpat(x) > 1]
        mult[bkey(bn)] = (len(v), sum(1 for m in v if m == 1), len(hi), max(v) if v else 0,
                          sum(v), sum(1 for x in hi if F(str(x['dmin'])) <= 6),
                          sum(1 for x in hi if len(set(x['fl'])) < len(x['fl'])))
    eight = [x for x in rep[(4, 0)] if x['nd'] == 0]
    BASIS.update({'r16': (nmax, nkmax, tri, tbad, sid, par_t, mono, strict, len(okc),
                          t4, tw, dict(mult),
                          [(x['fl'], x['nu'], x['nd'], str(x['dmin']), mpat(x))
                           for x in eight])})
    p &= ok('R16.0', '缩法重数这台机器要有四张不共享算术的票：$j\\pm1$ 递推、二项式差 '
                     '$\\binom{2m}{m}-\\binom{2m}{m+1}$、钩长公式 $f^{(m,m)}=(2m)!/((m+1)!\\,m!)$、'
                     '以及**显式**解 $(\\sum_i X^{(i)})T=0$（$X=E,F,H$，对角余乘）的 $SL(2)$ '
                     '不变张量零空间（$n\\le%d$，$\\mathbb Q$ 上精确消元）。四路在 $0..%d$ 上违例 %d 条 '
                     '$\\Rightarrow$ 每类"有几个独立 Lorentz 标量"从此不是散文。显式那路还顺手数了'
                     '"画线法"：$n$ 个指标的完全配对共 $(n-1)!!$ 个，其张成空间的秩 %s，'
                     '两者之差就是 Plücker（Schouten）关系的条数 %s $\\Rightarrow$ 缩法重数'
                     '**不是**配对方案数：$n=4$ 时三个画线法只撑出 $2$ 个独立缩法。'
                     '本层用到的指标数最大为 %d $\\le %d$ $\\Rightarrow$ 判据落在显式路线够得着的范围里' %
            (NEXP, nmax, len(tri) + len(tbad), [r[4] for r in t4], [r[5] for r in t4],
             nkmax, NEXP),
            not tri and not tbad and nkmax <= NEXP and
            [r[1] for r in t4] == [1, 0, 1, 0, 2, 0, 5] and
            [r[2] for r in t4] == [1, 0, 1, 0, 2, 0, 5] and
            [r[4] for r in t4] == [1, 0, 1, 0, 2, 0, 5] and
            [r[3] for r in t4] == [1, 0, 1, 0, 3, 0, 15] and
            [r[5] for r in t4] == [0, 0, 0, 0, 1, 0, 10] and
            len(t4) == NEXP + 1 and nmax == 10,
            '四路核对表（$n$、递推、零空间、配对数、配对秩、关系数）：%s' % t4)
    p &= ok('R16.1', '重数的**形状**也是读数，不是只有一堆数：(i) 全部 %d 个可构建类里，'
                     '"只有 $1$ 条缩法"等价于"两侧自旋指标数都不超过 $2$"%s（违例 %d 条）；'
                     '(ii) 导数塔的奇偶是**半格**：$k_{\\min}+1$ 阶一律给 $0$（违例 %d 条），'
                     '而 $k\\equiv k_{\\min}\\pmod 2$ 的每层都非零且不降（不降违例 %d 条），'
                     '并且从 $k_{\\min}$ 走到 $k_{\\min}+%d$ 时**每一条**类都严格变大（%d/%d）'
                     '$\\Rightarrow$ "只数到最小 $k_{\\min}$"是一条**有意的截断**，不是一句'
                     '"高维大概没有"：塔的逐层总缩法数 %s（类数 $=%d$）' %
            (len(okc), '成立' if not sid else '**不成立**', len(sid), len(par_t), len(mono),
             2 * TSTEP, strict, len(okc),
             '；'.join('$k=k_{\\min}+%d$：%d 条缩法（$\\ge2$ 的类 %d）' % t for t in tw),
             len(okc)),
            not sid and not par_t and not mono and strict == len(okc) == 1593 and
            tw[0][1] == sum(v[4] for v in mult.values()) and
            all(tw[i][1] < tw[i + 1][1] for i in range(TSTEP)) and
            all(tw[i][2] <= len(okc) for i in range(TSTEP + 1)),
            '塔的逐层读数：%s；逐档缩法读数：%s' % (tw, dict(mult)))

    # ---- R16.2 类数 $\to$ 算符数：Lorentz 那一半的差额数出来了
    # tot = ($m=1$ 类数, $m\ge2$ 类数, 最大重数, 缩法总数, $d\le6$ 且多重, 多重且含重复场名)
    tot = [sum(v[1] for v in mult.values()), sum(v[2] for v in mult.values()),
           max(v[3] for v in mult.values()), sum(v[4] for v in mult.values()),
           sum(v[5] for v in mult.values()), sum(v[6] for v in mult.values())]
    eight_m = set(mpat(x) for x in eight)
    BASIS.update({'r16tot': tot})
    p &= ok('R16.2', '把"类数不是算符数"从一句话变成一个差额：%d 个可构建类共给 %d 条缩法'
                     '（$\\times%s$），其中"只有 $1$ 条"的 %d 类、"有 $2$ 条"的 %d 类，最大重数就是 '
                     '%d（本层自旋指标数不超过 %d，而 $C_2=2$）$\\Rightarrow$ 按类计数把 Lorentz '
                     '口径的结构空间低估了 %d 条。逐档（类数、$m=1$、$m\\ge2$、$\\max m$、缩法总数）'
                     '%s。与 §10 的接缝：$n_f=4$ 的 %d 条 SM 单态 $d=6$ 类**每一条**都是 $2$ 条缩法'
                     '（重数集合 $=%s$）$\\Rightarrow$ "§10 有 8 条算符"必须读成 **8 个类 $=%s$ 个 '
                     'Lorentz 结构**；而且全档里 $d\\le6$ 且多缩法的类恰有 %d 条 $=$ 这 %d 条加它们的'
                     '点号孪生 %d 条 $\\Rightarrow$ "谁多重"是边界清楚的一批：四个指标全在同侧。'
                     '口径警告（这条把话说回上界）：$m\\ge2$ 的 %d 类里有 %d 类场内容含**重复名字**'
                     '$\\Rightarrow$ Fermi 反对称、味指标、Fierz、EOM、全导数塔这五道削减本层一道都不做，'
                     '$m$ 是"不变张量空间的维数"而不是算符数。塔那一侧同样有数：往上走一层就'
                     '**全部** %d 类都变多重（%s）$\\Rightarrow$ 第十六项边界 (i) 的前半"完整塔未枚举"'
                     '现在带增长率，(ii) 的 Lorentz 半边已数成 %d 条差额（"数出 $m$ 条"不等于"选定其中'
                     '哪一条"），味、Fierz、EOM、全总导数几关照旧（Fierz 那道此后只把洛伦兹半边数成读数，见 14.10）。'
                     '本层不回填任何寿命、不改 P4／P7 的判据与分级，L10 保持 OPEN' %
            (len(okc), tot[3], '%.4f' % (tot[3] / float(len(okc))), tot[0], tot[1], tot[2],
             nkmax, tot[3] - len(okc),
             '；'.join('$(n_f,n_s)$=%s：%s' % (k, mult[k][:5])
                       for k in sorted(mult, key=lambda s: [int(v) for v in s.split(',')])) +
             '（其中 $(3,0)$ 一档可构建类为 %d 条：R15.3 那 %d 条绝对禁全在这一档）'
             % (mult['3,0'][0], cls[(3, 0)]),
             len(eight), sorted(eight_m), 2 * len(eight), tot[4], tot[4] / 2, tot[4] / 2,
             tot[1], tot[5], tw[1][2],
             '；'.join('$k=k_{\\min}+%d$：%d 条' % (t[0], t[1]) for t in tw),
             tot[3] - len(okc)),
            mult == {'2,0': (8, 8, 0, 1, 8, 0, 0), '2,1': (69, 69, 0, 1, 69, 0, 0),
                     '2,2': (478, 478, 0, 1, 478, 0, 0), '3,0': (0, 0, 0, 0, 0, 0, 0),
                     '4,0': (79, 33, 46, 2, 125, 16, 36),
                     '4,1': (959, 337, 622, 2, 1581, 0, 408)} and
            tot == [925, 668, 2, 2261, 16, 444] and len(eight) == 8 and eight_m == {2} and
            all(str(x['dmin']) == '6' and mpat(x) == 2 for x in eight) and
            sum(v[0] for v in mult.values()) == len(okc) == 1593 and
            tot[3] == sum(v[4] for v in mult.values()) and tot[4] == 16 and
            tw[0][:2] == (0, 2261) and all(t[2] == 1593 for t in tw[1:]) and
            all(tw[i][1] < tw[i + 1][1] for i in range(TSTEP)),
            '缩法差额读数（$m=1$、$m\\ge2$、$\\max m$、缩法总数、$d\\le6$ 且多重、多重且含重复场名）'
            '：%s' % (tot,))

    # ---- R17 Fermi 反对称：五道削减里的第一道做成读数 ----------------------------
    # 上一节数出"一类有几条缩法"，但同名外尔场是**反对易**的：交换两个同名场的槽位必须让
    # 系数张量变号，否则该缩法恒等于零。判据 $=$ 在不变张量空间上逐组施加完全反对称化算子
    # $A_g=\sum_{\sigma\in S_g}\mathrm{sgn}(\sigma)\,\sigma$ 之后像空间的维数。三条不共享算术的路：
    #   甲 显式投影（零空间基 $->$ 反对称化 $->$ 秩）
    #   乙 表示论（$m$ 个同名槽位贡献 $\Lambda^m(\mathbb C^2)$：$m=0,1,2$ 给自旋 $0,\frac12,0$，
    #     $m\ge3$ 是零空间；再与其余单槽做 $j$-耦合数自旋 $0$ 的重数）
    #   丁 Grassmann 直接求值（同名字共用一对反对易生成元，数 $T\mapsto\mathcal O(T)$ 的像的秩）
    # 秩只依赖"组大小的多重集"，不依赖槽位编号（乙那条路本身与位置无关，而三路相等），
    # 所以按 $(n,\text{sizes})$ 缓存；本层覆盖 $k_{\min}=0$ 的类（$k_{\min}=1$ 时导数槽归哪个
    # 场、类记录里没有，反对称化在此空间上不是自同态 $\\Rightarrow$ 那条只做登记，见 R17.4）。
    def fermi_basis(n):
        if n == 0:
            return [(F(1),)]
        dim = 1 << n
        rows = []
        for X in GEN:
            for t in range(dim):
                row = [F(0)] * dim
                for i in range(n):
                    b = (t >> i) & 1
                    for (a, c), xv in X.items():
                        if a == b:
                            row[t ^ (b << i) ^ (c << i)] += F(xv)
                if any(row):
                    rows.append(row)
        return nullspace(rows, dim)

    def fermi_perm(v, n, pl):
        """$(\\sigma T)_{a_0\\cdots a_{n-1}}=T_{a_{\\sigma(0)}\\cdots a_{\\sigma(n-1)}}$。"""
        out = [F(0)] * (1 << n)
        for t, c in enumerate(v):
            if not c:
                continue
            s = 0
            for i in range(n):
                if (t >> pl[i]) & 1:
                    s |= 1 << i
            out[s] += c
        return out

    def fermi_antisym(v, n, g):
        acc = [F(0)] * (1 << n)
        for p in itertools.permutations(range(len(g))):
            inv = sum(1 for a in range(len(g)) for b in range(a + 1, len(g)) if p[a] > p[b])
            pl = list(range(n))
            for i in range(len(g)):
                pl[g[i]] = g[p[i]]
            w = fermi_perm(v, n, pl)
            sg = -1 if inv % 2 else 1
            for i in range(len(acc)):
                acc[i] += sg * w[i]
        return acc

    def fermi_jia(n, gs):
        cur = list(fermi_basis(n))
        for g in gs:
            cur = [w for w in (fermi_antisym(v, n, g) for v in cur) if any(w)]
        return q_rank(cur)

    def fermi_yi(n, gs):
        js, used = [], 0
        for g in gs:
            m = len(g)
            if m >= 3:
                return 0                                  # $\\Lambda^m(\\mathbb C^2)=0$
            js.append(0 if m == 2 else 1)                 # $2j$：平凡表示记 0
            used += m
        js += [1] * (n - used)                            # 每个单槽是 $j=\\frac12$
        book = {0: 1}
        for j in js:
            nb = {}
            for jj, k in book.items():
                x = abs(jj - j)
                while x <= jj + j:
                    nb[x] = nb.get(x, 0) + k
                    x += 2
            book = nb
        return book.get(0, 0)

    def fermi_ding(n, gs):
        nm, k = {}, len(gs)
        for gi, g in enumerate(gs):
            for i in g:
                nm[i] = gi
        for i in range(n):
            if i not in nm:
                nm[i] = k
                k += 1
        rows = []
        for v in fermi_basis(n):
            acc = {}
            for t, c in enumerate(v):
                if not c:
                    continue
                bits = [(nm[i], (t >> i) & 1) for i in range(n)]
                if len(set(bits)) < n:                    # 同一生成元取两次 $=0$
                    continue
                inv = sum(1 for a in range(n) for b in range(a + 1, n) if bits[a] > bits[b])
                key = tuple(sorted(bits))
                acc[key] = acc.get(key, F(0)) + (c if inv % 2 == 0 else -c)
            red = dict((kk, x) for kk, x in acc.items() if x)
            if red:
                rows.append(red)
        uni = sorted(set().union(*[set(r) for r in rows])) if rows else []
        return q_rank([[r.get(kk, F(0)) for kk in uni] for r in rows])

    fermi_cache = {}

    def fermi_dim(n, sizes):
        key = (n, tuple(sorted(sizes, reverse=True)))
        if key not in fermi_cache:
            gs, pos = [], 0
            for m in key[1]:
                gs.append(list(range(pos, pos + m)))
                pos += m
            fermi_cache[key] = (fermi_jia(n, gs), fermi_yi(n, gs), fermi_ding(n, gs))
        return fermi_cache[key]

    def fermi_sizes(names):
        c = collections.Counter(names)
        return tuple(sorted((v for v in c.values() if v >= 2), reverse=True))

    def fermi_parts(n):
        """全部"同名组大小多重集"（每组 $\\ge2$、总槽位 $\\le n$）——只依赖多重集，不依赖位置。"""
        out = set()

        def rec(rem, cap, cur):
            out.add(tuple(cur))
            for m in range(2, min(cap, rem) + 1):
                rec(rem - m, m, cur + [m])
        rec(n, n, [])
        return sorted(out, key=lambda s: (-sum(s), s))

    ftab = [(n, s) + fermi_dim(n, s) for n in range(NEXP + 1) for s in fermi_parts(n)]
    fdis = [r for r in ftab if len(set(r[2:])) != 1]
    funused = [r for r in ftab if r[1] == () and r[2] != cat_rec(r[0])]
    fanch = [fermi_dim(2, (2,)), fermi_dim(4, (4,)), fermi_dim(4, (2, 2)), fermi_dim(6, (2, 2, 2))]
    # ---- 逐类读数：只对 $k_{\\min}=0$ 的类判定，其余登记 ----
    fshape, fdisx, fblind, fblindx, fkill, fshr, fsame, fgrow, fheavy, fheavyx = \
        [], [], [], [], [], [], [], [], [], []
    fact = {}
    for bn in BST_BINS:
        rs = [x for x in rep[bn] if x['ok'] and x['kmin'] == 0]
        va = vm = 0
        for x in rs:
            if len(x['fnu']) != x['nu'] or len(x['fnd']) != x['nd']:
                fshape.append(x['fl'])
                continue
            su, sd = fermi_sizes(x['fnu']), fermi_sizes(x['fnd'])
            ju = fermi_dim(x['nu'], su)
            jd = fermi_dim(x['nd'], sd)
            if len(set(ju)) != 1 or len(set(jd)) != 1:
                fdisx.append((x['fl'], ju, jd))
            a = ju[0] * jd[0]
            m = mpat(x)
            va += a
            vm += m
            if any(v >= 3 for v in su + sd):
                fheavy.append(x['fl'])
                if a:
                    fheavyx.append((x['fl'], m, a))
            if not (su or sd):
                fblind.append(x['fl'])
                if a != m:                                # 判据必须**看不见**这一族
                    fblindx.append((x['fl'], m, a))
            elif a == 0:
                fkill.append((x['fl'], m))
            elif a < m:
                fshr.append((x['fl'], m, a))
            elif a == m:
                fsame.append(x['fl'])
            else:
                fgrow.append((x['fl'], m, a))              # 削减只会变小 $\\Rightarrow$ 必须为空
        rep_all = [x for x in rep[bn] if x['ok']]
        fact[bkey(bn)] = (len(rs), len(rep_all) - len(rs), vm, va,
                          sum(1 for x in rep_all if x['kmin'] == 0 and mpat(x) > 1),
                          sum(1 for x in rep_all if x['kmin'] == 0 and
                              (fermi_sizes(x['fnu']) or fermi_sizes(x['fnd']))))
    eight_f = [(x['fl'], x['kmin'], mpat(x),
                (fermi_sizes(x['fnu']), fermi_sizes(x['fnd'])),
                fermi_dim(x['nu'], fermi_sizes(x['fnu']))[0] *
                fermi_dim(x['nd'], fermi_sizes(x['fnd']))[0]) for x in eight]
    fmap4 = dict(((r[0], r[1]), r[2]) for r in ftab)
    frank_grp = {}
    for e in eight_f:
        frank_grp.setdefault(e[3], set()).add(e[4])
    fgrp_out = [[list(k[0]), list(k[1]), sorted(v)] for k, v in
                sorted(frank_grp.items(), key=lambda z: str(z[0]))]
    fzero4 = sorted(e[0] for e in eight_f if e[4] == 0)
    ftripl4 = sorted(e[0] for e in eight_f if max(max(e[3][0], default=0),
                                                  max(e[3][1], default=0)) >= 3)
    fok24 = sorted(e[0] for e in eight_f if max(max(e[3][0], default=0),
                                                 max(e[3][1], default=0)) <= 2)
    ftot = [sum(v[2] for v in fact.values()), sum(v[3] for v in fact.values()),
            len(fkill), len(fshr), len(fsame), len(fheavy), len(fblind), len(fgrow)]
    # 归零 ⟺ 含三重同名：两侧集合的对称差必须为空，否则"$\\Lambda^m=0$"之外还有别的归零原因
    fsymdiff = len(set(tuple(fl) for fl in fheavy) ^ set(tuple(e[0]) for e in fkill))
    BASIS.update({'r17': (ftab, fdis, funused, fanch, fshape, fdisx, fkill, fshr, fsame,
                          fheavy, fheavyx, fblindx, fgrow, dict(fact), ftot, eight_f,
                          fgrp_out, (fzero4, ftripl4, fok24), fsymdiff,
                          [k for k in sorted(fermi_cache, key=lambda z: (z[0], z[1]))])})
    p &= ok('R17.0', 'Fermi 反对称这道削减也要有三张不共享算术的票：显式投影（不变张量基上'
                     '逐组反对称化的像的秩）、表示论（$m$ 个同名槽位给 $\\Lambda^m(\\mathbb C^2)$，'
                     '$m\\ge3$ 直接是零空间）、Grassmann 直接求值（同名字共用一对反对易生成元，'
                     '数 $T\\mapsto\\mathcal O(T)$ 的像的秩）。$n\\le%d$ 的全部 %d 个 $(n,\\text{组大小})$ '
                     '用例里三路互不等者 %d 条；无重复名字时必须退回上一节的缩法重数，违例 %d 条。'
                     '四条教科书锚点（三路各算一遍，$\\Rightarrow$ 括号里是三条路的读数）：'
                     '两槽同名 $=%s$（$\\varepsilon^{\\alpha\\beta}\\psi_\\alpha\\psi_\\beta$ 非零）、'
                     '四槽同名 $=%s$（单个外尔场只有两个分量 $\\Rightarrow\\psi\\psi\\psi\\psi\\equiv0$）、'
                     '四槽两两同名 $=%s$（$(\\psi\\psi)(\\chi\\chi)$ 从 %d 条里活 $%d$ 条）、'
                     '六槽三对同名 $=%s$（三对各自是单态 $\\Rightarrow$ 整体只剩 %d 条，而 %d 条无重复名字的接法里'
                     '其余 %d 条把同名场接进了跨对指标）' %
            (NEXP, len(ftab), len(fdis), len(funused), fanch[0], fanch[1], fanch[2],
             cat_rec(4), fanch[2][0], fanch[3], fanch[3][0], cat_rec(6),
             cat_rec(6) - fanch[3][0]),
            not fdis and not funused and len(ftab) > 0 and
            fanch[0] == (1, 1, 1) and fanch[1] == (0, 0, 0) and fanch[2] == (1, 1, 1) and
            fanch[3] == (1, 1, 1) and
            all(len(set(r[2:])) == 1 for r in ftab) and
            sum(1 for r in ftab if r[1] != ()) > 0,
            '三路核对表前 12 行（$n$、组大小、甲、乙、丁）：%s' % ftab[:12])
    p &= ok('R17.1', '判据用在类上之前，先核它**登记的东西**对得上：$k_{\\min}=0$ 的类里，'
                     '名字清单的长度与两侧槽位计数不符 %d 条；同一类上三路互不等 %d 条；'
                     '含 $\\ge3$ 个同名场的类 %d 条，其中存活缩法非零 %d 条（表示论说这里必须为零）'
                     '$\\Rightarrow$ "$\\Lambda^m(\\mathbb C^2)=0$（$m\\ge3$）"这条不是注释里的话，'
                     '它被本层的类命中过 %d 次，而且**归零的那批恰是**含三重同名的那批'
                     '（两侧集合的对称差 %d 条 $\\Rightarrow$ 除 $\\Lambda^m=0$ 之外没有别的归零原因）。'
                     '每个分支都得有流量：无重复名字的类 %d 条（'
                     '这一族的判据必须**看不见**它们，违例 %d 条）、有重复名字的类里归零 %d 条、'
                     '缩减但未归零 %d 条、不变 %d 条、反而变大 %d 条（反对称化是自同态的像，'
                     '不可能比原空间更大 $\\Rightarrow$ 这一格必须恒为 0，它在此是分区断言的一格）。'
                     '本层用到的最大槽位数 %d $\\le$ 显式路线的 %d' %
            (len(fshape), len(fdisx), len(fheavy), len(fheavyx), len(fheavy), fsymdiff,
             len(fblind),
             len(fblindx), len(fkill), len(fshr), len(fsame), len(fgrow),
             max(max(x['nu'], x['nd']) for x in okc if x['kmin'] == 0), NEXP),
            not fshape and not fdisx and not fheavyx and not fblindx and not fgrow and
            len(fheavy) > 0 and len(fblind) > 0 and (len(fkill) + len(fshr) + len(fsame)) > 0 and
            not fsymdiff and
            len(fkill) + len(fshr) + len(fsame) + len(fgrow) ==
            sum(v[0] for v in fact.values()) - len(fblind) and
            max(max(x['nu'], x['nd']) for x in okc if x['kmin'] == 0) <= NEXP,
            '归零类前 6 条（场名、缩法数）：%s；缩减类前 6 条：%s' % (fkill[:6], fshr[:6]))
    p &= ok('R17.2', '把 Fermi 削减做成一个差额：$k_{\\min}=0$ 的可构建类共 %d 个、上一节的缩法 '
                     '%d 条，过了反对称化之后剩 %d 条 $\\Rightarrow$ 这一道削减吃掉了 %d 条'
                     '（$\\times%s$）。逐档（判据覆盖类数、登记类数、缩法数、存活数、多重缩法类数、'
                     '含重复名字类数）%s；合计（缩法、存活、归零类、缩减类、不变类、含 $\\ge3$ 同名、'
                     '无重复名字、反而变大）%s $\\Rightarrow$ 这八个数是**钉住的口径读数**：把"全同"从场名'
                     '改成表示标签，第一件事就是在此现形' %
            (sum(v[0] for v in fact.values()), ftot[0], ftot[1], ftot[0] - ftot[1],
             '%.4f' % (ftot[1] / float(ftot[0])),
             '；'.join('$(n_f,n_s)$=%s：%s' % (k, fact[k])
                       for k in sorted(fact, key=lambda s: [int(v) for v in s.split(',')])),
             ftot),
            ftot[1] <= ftot[0] and ftot[7] == 0 and ftot[0] > 0 and
            ftot == [1028, 838, 40, 110, 219, 40, 469, 0] and
            ftot[0] == sum(v[2] for v in fact.values()) and
            ftot[1] == sum(v[3] for v in fact.values()) and
            ftot[2] + ftot[3] + ftot[4] + ftot[7] ==
            sum(v[0] for v in fact.values()) - ftot[6] and
            ftot[0] == sum(mpat(x) for x in okc if x['kmin'] == 0) and
            all(v[3] <= v[2] for v in fact.values()),
            '逐档读数：%s' % dict(fact))
    p &= ok('R17.3', '与 §10 的接缝要重读：$n_f=4$、无点号侧那 %d 条 SM 单态 $d=6$ 类，'
                     '$k_{\\min}$ 取值 %s（非零 %d 条 $\\Rightarrow$ 若有则本层只能登记它们），'
                     '上一节给"每类 %s 条缩法"$\\Rightarrow$ "8 个类 $=%d$ 个 Lorentz 结构"；'
                     '过 Fermi 之后逐类（场名、$k_{\\min}$、缩法数、两侧名字组大小、存活数）%s'
                     '$\\Rightarrow$ 结构数从 %d 到 %d。三件事各自有数：'
                     '存活数只依赖名字组大小的多重集 $\\Rightarrow$ 同一多重集上出现两个不同存活数的组 %d 个；'
                     '每类读到的存活数与 $n\\le%d$ 预算表同行一致（不符 %d 条 $\\Rightarrow$ 接缝读的确实是那张表）；'
                     '归零的那批 %s 与"同一个名字占满 $\\ge3$ 个槽"的那批 %s 是同一批，'
                     '而名字最多占两槽的那批 %d 条**无一归零** $\\Rightarrow$ '
                     '被减掉的正是"$\\Lambda^m(\\mathbb C^2)=0$（$m\\ge3$）"：三个或四个槽全给同一个外尔场，'
                     '系数张量要关于它们完全反对称，而单个外尔场只有 2 个分量；组到存活数的映射 %s' %
            (len(eight_f), sorted(set(e[1] for e in eight_f)),
             sum(1 for e in eight_f if e[1] != 0), sorted(set(e[2] for e in eight_f)),
             sum(e[2] for e in eight_f), eight_f,
             sum(e[2] for e in eight_f), sum(e[4] for e in eight_f),
             sum(1 for v in frank_grp.values() if len(v) > 1), NEXP,
             sum(1 for e, x in zip(eight_f, eight)
                 if e[4] != fmap4[(x['nu'], e[3][0])] * fmap4[(x['nd'], e[3][1])]),
             fzero4, ftripl4, len(fok24), dict((str(k), sorted(v)) for k, v in
                                               sorted(frank_grp.items(), key=lambda z: str(z[0])))),
            eight_f and len(eight_f) == 8 == len(eight) and
            all(e[1] == 0 for e in eight_f) and
            sum(e[2] for e in eight_f) == 16 and sum(e[4] for e in eight_f) == 8 and
            all(e[4] <= e[2] for e in eight_f) and
            all(len(v) == 1 for v in frank_grp.values()) and
            all(e[4] == fmap4[(x['nu'], e[3][0])] * fmap4[(x['nd'], e[3][1])]
                for e, x in zip(eight_f, eight)) and
            fzero4 == ftripl4 and len(fzero4) == 2 and
            len(fok24) == len(eight_f) - len(fzero4) and
            all(e[4] > 0 for e in eight_f if e[0] in fok24),
            '逐类（场名、缩法数、Fermi 存活数、组大小）：%s'
            % [(e[0], e[2], e[4], e[3]) for e in eight_f])
    p &= ok('R17.4', '判据的**管辖范围**也是一个数：$k_{\\min}\\ne0$ 的可构建类 %d 个（缩法 %d 条）'
                     '不在本层的读数里 $\\Rightarrow$ 导数槽挂在哪个场，类记录并不携带，'
                     '反对称化在那一族上不是同一个空间上的自同态，只能登记不能判定；'
                     '两边相加必须回到上一节的总量：%d $+$ %d $=$ %d（$=$ 全文缩法总数 %d 减去'
                     '登记类那部分），类数 $1593=%d+%d$。五道削减过了一道，味指标、Fierz、'
                     'EOM、全总导数四关照旧 $\\Rightarrow$ **类数仍然不是算符数**；'
                     '本层不回填任何寿命、不改 P4／P7 的判据与分级，L10 保持 OPEN' %
            (sum(v[1] for v in fact.values()),
             sum(mpat(x) for x in okc if x['kmin'] != 0),
             ftot[0], sum(mpat(x) for x in okc if x['kmin'] != 0), tot[3], tot[3],
             sum(v[0] for v in fact.values()), sum(v[1] for v in fact.values())),
            ftot[0] + sum(mpat(x) for x in okc if x['kmin'] != 0) == tot[3] and
            sum(v[0] for v in fact.values()) + sum(v[1] for v in fact.values()) == len(okc) == 1593
            and tot[3] == 2261,
            '逐档（判据类数、登记类数）：%s' % {k: (v[0], v[1]) for k, v in fact.items()})
    # ---- R18 Fierz 恒等式：把"换道"做成一次可数的基变换 --------------------------
    # 14.8/14.9 的全部读数只走 $\\varepsilon$ 道（同侧指标成对缩掉）。一条 Fierz 恒等式的內容
    # 恰是**换到另一条道再写回来**：矢量（流-流）道 $P_{ij,pq}=\\sum_\\mu G_\\mu\\sigma^\\mu_{ip}
    # \\sigma^\\mu_{jq}$ 吃掉一个不点指标加一个点指标。若它张成与 $\\varepsilon$ 道**同一个**
    # $SL(2)_L\\times SL(2)_R$ 不变量空间，"只用 $\\varepsilon$ 画线"就从一直挂在计数里的**假设**
    # 变成读数；两型生成元之间的线性关系条数 $=|(\\varepsilon\\text{ 画线})|+|(\\sigma\\text{ 画线})|-秩$
    # 就是这道削减在此坐标里可数的内容（与 Schouten 不共族：那条比的是**同为 $\\varepsilon$** 的
    # 画线之间）。三张不共享算术的票：$\\varepsilon$ 道秩（走 14.8 的显式零空间基）、$\\sigma$ 道
    # **单独**秩（走显式 $\\sigma^\\mu$ 分量与 $\\mu$ 缩并）、两型并秩；预测值第四路独立取自 R16 的
    # 特征标递推 $c_{j0}$。
    # 约定显式写出（不当隐藏前提）：$i\\sigma^2$ 取实矩阵 $\\begin{pmatrix}0&-1\\\\1&0\\end{pmatrix}$
    # $\\Rightarrow$ 度规号并成 $G=(+1,-1,+1,-1)$（$\\sigma^2=i(i\\sigma^2)$ 再贡献一次 $-1$）；
    # 带点侧与不带点侧同用一份 $\\varepsilon$ 矩阵（与 14.8 两侧同用 $c_{j0}$ 的口径一致）；
    # 全程精确分数，无浮点、无模约化。
    SIGM = ((F(1), F(0)), (F(0), F(1))), ((F(0), F(1)), (F(1), F(0))), \
            ((F(0), F(-1)), (F(1), F(0))), ((F(1), F(0)), (F(0), F(-1)))
    SG = (F(1), F(-1), F(1), F(-1))
    E2 = {(0, 1): F(1), (1, 0): F(-1)}
    PROP = {}
    for _a in (0, 1):
        for _b in (0, 1):
            for _c in (0, 1):
                for _d in (0, 1):
                    PROP[(_a, _b, _c, _d)] = sum(
                        SG[_m] * SIGM[_m][_a][_c] * SIGM[_m][_b][_d] for _m in range(4))
    NSIG, NSIGT = 6, 8             # 单侧槽位上限／两侧合计上限（$(6,4)$ 一档按代价登记为界外）
    sig_cache, scnt = {}, collections.Counter()

    def sig_val(n, elines, slines, mpair):
        """一条画线的张量分量：$\\sigma$ 线的 $\\mu$ 已并成 $P$，故每个分量只乘一次传播子。"""
        out = [F(0)] * (1 << n)
        for t in range(1 << n):
            b = [(t >> i) & 1 for i in range(n)]
            w = F(1)
            for i, j in elines:
                w *= E2.get((b[i], b[j]), F(0))
                if not w:
                    break
            if not w:
                continue
            for a, c in mpair:
                ia, pa = slines[a]
                ic, pc = slines[c]
                w *= PROP[(b[ia], b[ic], b[pa], b[pc])]
                if not w:
                    break
            out[t] = w
        return out

    def sig_pair(nu, nd):
        """$(\\nu,\\dot\\nu)$ 一档的三票与账：预测／$\\varepsilon$ 道秩／$\\sigma$ 道单独秩／并秩／
        两型生成元条数／道间关系条数。按档缓存 $\\Rightarrow$ 每档只算一次。"""
        if (nu, nd) in sig_cache:
            return sig_cache[(nu, nd)]
        UU, DD = list(range(nu)), list(range(nu, nu + nd))
        el, sl = [], []
        for pu in matchings(UU):
            for pd in matchings(DD):
                el.append((list(pu) + list(pd), [], []))
        for r in range(2, min(nu, nd) + 1, 2):
            if (nu - r) % 2 or (nd - r) % 2:
                continue
            for su in itertools.combinations(UU, r):
                for sd in itertools.combinations(DD, r):
                    for bij in itertools.permutations(sd):
                        vv = list(zip(su, bij))
                        ru = [z for z in UU if z not in su]
                        rd = [z for z in DD if z not in sd]
                        for pu in matchings(ru):
                            for pd in matchings(rd):
                                for mp in matchings(list(range(r))):
                                    sl.append((list(pu) + list(pd), vv, list(mp)))
        n = nu + nd
        ev = [v for v in (sig_val(n, *s) for s in el) if any(v)]
        seen, uv = set(), []
        for v in (sig_val(n, *s) for s in sl):
            k = tuple(v)
            if any(v) and k not in seen:
                seen.add(k)
                uv.append(v)
        r_e = q_rank(ev) if ev else 0
        r_s = q_rank(uv) if uv else 0
        r_a = q_rank(ev + uv) if (ev or uv) else 0
        sig_cache[(nu, nd)] = (cg_j0(nu) * cg_j0(nd), r_e, r_s, r_a, len(ev), len(uv),
                               len(ev) + len(uv) - r_a)
        return sig_cache[(nu, nd)]

    def g_mul(a, b):
        """两个 Grassmann 元素（掩码 $\\to$ 精确分数）的外积。"""
        out = {}
        for ma, ca in a.items():
            for mb, cb in b.items():
                if ma & mb:
                    continue                               # 同一生成元取两次 $=0$
                m, inv = ma, 0
                for i in [k for k in range(64) if (mb >> k) & 1]:
                    inv += bin(m & ((1 << i) - 1)).count('1')
                    m |= 1 << i
                v = out.get(m, F(0)) + (ca * cb if inv % 2 == 0 else -ca * cb)
                if v:
                    out[m] = v
                elif m in out:
                    out.pop(m)
        return out

    def g_bracket(x, y):
        """$(\\psi_x\\psi_y)=\\varepsilon^{ab}\\psi_{x,a}\\psi_{y,b}$；同名槽共用一对生成元。
        基元素按生成元**升序**落定 $\\Rightarrow$ $g_1>g_2$ 时要再吃一次换序符号，
        否则同名的那条被算成 $+1-1=0$（本层写作时真踩过这一伤）。"""
        out = {}
        for a, b, e in ((0, 1, 1), (1, 0, -1)):
            g1, g2 = 2 * x + a, 2 * y + b
            m = (1 << g1) | (1 << g2)
            out[m] = out.get(m, F(0)) + F(e if g1 < g2 else -e)
            if not out[m]:
                out.pop(m)
        return out

    def chan_grass(names):
        """第三张票（与甲／乙／丁都不共算术）：固定**内容**，把"哪两个名字缩在一起"的每一道
        写成 Grassmann 单项式，数这些单项式的秩 $=$ 该内容下独立洛伦兹标量的条数。"""
        idx = {}
        for s in names:
            idx.setdefault(s, len(idx))
        vecs, nch = [], 0
        for ms in matchings(list(range(len(names)))):
            nch += 1
            v = {0: F(1)}
            for i, j in ms:
                v = g_mul(v, g_bracket(idx[names[i]], idx[names[j]]))
            if v:
                vecs.append(v)
        if not vecs:
            return 0, nch
        cols = sorted(set().union(*[set(v) for v in vecs]))
        return q_rank([[v.get(c, F(0)) for c in cols] for v in vecs]), nch

    def place_ranks(names):
        """§14.9 那句"秩只依赖组大小的多重集、不依赖槽位编号"要**每一种摆放**都验一遍；
        顺带把"跨摆放求并"的秩也数出来（它是构造伪影的度量，不是一张票，见 R18.3 的登记）。"""
        n = len(names)
        basis = fermi_basis(n)
        ranks, allimg = [], []
        for w in sorted(set(itertools.permutations(names))):
            pos = collections.OrderedDict()
            for i, s in enumerate(w):
                pos.setdefault(s, []).append(i)
            gs = [g for g in pos.values() if len(g) >= 2]
            cur = []
            for v in basis:
                img = [list(v)]
                for g in gs:
                    img = [z for z in (fermi_antisym(y, n, g) for y in img) if any(z)]
                    if not img:
                        break
                cur += img
            ranks.append(q_rank(cur) if cur else 0)
            allimg += cur
        return ranks, (q_rank(allimg) if allimg else 0)

    # 表格档：三票相等这条读数**不只**在类集真出现的档上核（类集只有 $(2,2)$ 一档两侧皆非空），
    # 而是把 $2\\le\\nu,\\dot\\nu\\le%d$、$\\nu+\\dot\\nu\\le%d$ 的全部偶档都算一遍。哪些档有类挂着，
    # 由下面逐类填的 `scnt` 那一列明说 $\\Rightarrow$ "档"与"类"是两件事，不能混着报。
    stier = [(nu, nd) for nu in range(2, NSIG + 1, 2) for nd in range(2, NSIG + 1, 2)
             if nu + nd <= NSIGT]
    for _nu, _nd in stier:
        sig_pair(_nu, _nd)
    # ---- 逐类读数：票 A（Grassmann 道）与票 B（摆放不变性）铺满 14.9 判定的那批类；
    #      票 C（$\\sigma$ 道换基）在 $(\\nu,\\dot\\nu)$ 档上缓存后挂回类
    sg_ab, sg_abx, sg_n, sg_ch, sg_pl, sg_place = 0, [], 0, 0, [], 0
    sg_un, sg_ungt = 0, 0
    ssig, ssig_m, ssig_rel, ssig_new, ssig_bad, ssig_mp = 0, 0, 0, 0, [], []
    sskip = {'形状不符': 0, '单侧空': 0, '奇侧': 0, '超档': 0}
    for bn in BST_BINS:
        for x in rep[bn]:
            if not (x['ok'] and x['kmin'] == 0):
                continue
            if len(x['fnu']) != x['nu'] or len(x['fnd']) != x['nd']:
                sskip['形状不符'] += 1
                continue
            sg_n += 1
            r17u = fermi_dim(x['nu'], fermi_sizes(x['fnu']))[0]
            r17d = fermi_dim(x['nd'], fermi_sizes(x['fnd']))[0]
            gu, cu = chan_grass(x['fnu'])
            gd, cd = chan_grass(x['fnd'])
            sg_ab += gu * gd
            sg_ch += cu * cd
            if gu != r17u or gd != r17d:
                sg_abx.append((bkey(bn), x['fnu'], x['fnd'], r17u, gu, r17d, gd))
            pu_r, pu_un = place_ranks(x['fnu'])
            pd_r, pd_un = place_ranks(x['fnd'])
            sg_place += len(pu_r) * len(pd_r)
            sg_un += pu_un * pd_un
            if pu_un * pd_un > r17u * r17d:
                sg_ungt += 1
            if len(set(pu_r)) != 1 or pu_r[0] != r17u or \
               len(set(pd_r)) != 1 or pd_r[0] != r17d:
                sg_pl.append((bkey(bn), x['fnu'], x['fnd'], pu_r, pd_r, r17u, r17d))
            if not x['nu'] or not x['nd']:
                sskip['单侧空'] += 1
                continue
            if x['nu'] > NSIG or x['nd'] > NSIG or x['nu'] + x['nd'] > NSIGT:
                sskip['超档'] += 1
                continue
            if x['nu'] % 2 or x['nd'] % 2:
                sskip['奇侧'] += 1
                continue
            pred, r_e, r_s, r_a, ne, ns, nrel = sig_pair(x['nu'], x['nd'])
            scnt[(x['nu'], x['nd'])] += 1
            ssig += 1
            ssig_m += pred
            ssig_rel += nrel
            ssig_new += r_a - r_e
            if len({pred, r_e, r_s, r_a}) != 1:
                ssig_bad.append(((x['nu'], x['nd']), pred, r_e, r_s, r_a))
            if pred != mpat(x):
                ssig_mp.append(((x['nu'], x['nd']), x['fl'], pred, mpat(x)))
    stab = [[k[0], k[1], scnt.get(k, 0)] + list(sig_cache[k]) for k in stier]
    srows = [r for r in stab if len({r[3], r[4], r[5], r[6]}) != 1]
    sback = [r for r in stab if r[2] > 0]
    sreal = sorted(set((x['nu'], x['nd']) for bn in BST_BINS for x in rep[bn]
                       if x['ok'] and x['kmin'] == 0))


    def _rt(v, w):
        for i in range(len(v)):
            if v[i] or w[i]:
                return None if not w[i] else v[i] / w[i]
        return F(0)


    # 两条教科书锚点（同一分量空间里比：$\\sigma$ 道的两条画线 vs 一条 $\\varepsilon$ 画线）
    sanch = sig_val(4, [], [(0, 2), (1, 3)], [(0, 1)])
    scrss = sig_val(4, [], [(0, 3), (1, 2)], [(0, 1)])
    seps = sig_val(4, [(0, 1), (2, 3)], [], [])
    sanchr = (_rt(sanch, seps), _rt(scrss, seps), q_rank([sanch, seps, scrss]),
              sorted(g_bracket(0, 0).items()), sorted(g_bracket(0, 1).items()))
    BASIS.update({'r18': (stab, srows, sback, sg_ab, sg_abx, sg_n, sg_place, sg_pl, sg_ch,
                          ssig, ssig_m, ssig_rel, ssig_new, ssig_bad, ssig_mp, sskip,
                          sanchr, len(stier), sg_un, sg_ungt, sskip['单侧空'], sreal)})
    p &= ok('R18.0', 'Fierz 这道削减要三张不共享算术的票：$\\varepsilon$ 道秩（走 14.8 的显式零空间'
                     '基）、$\\sigma$ 道**单独**秩（走显式 $\\sigma^\\mu$ 分量与 $\\mu$ 缩并）、两型'
                     '生成元的并秩；预测值第四路独立取自 R16 的特征标递推 $c_{j0}$。'
                     '$\\nu,\\dot\\nu$ 的 %d 个表格档上，四数（预测、$\\varepsilon$ 道秩、'
                     '$\\sigma$ 道单独秩、并秩）**不全等**者 %d 档 $\\Rightarrow$ 两型道各自都是'
                     '该不变量空间的**完备**生成集，"只用 $\\varepsilon$ 画线"从此是一条读数而不是假设。'
                     '锚点：$(2,2)$ 档同向 $\\sigma$ 道 $\\div\\varepsilon$ 道 $=%s$、交叉道 $\\div'
                     '\\varepsilon$ 道 $=%s$（即完备性关系 $\\sigma^\\mu_{\\alpha\\dot\\beta}'
                     '\\sigma_{\\mu\\gamma\\dot\\delta}=2\\,\\varepsilon_{\\alpha\\gamma}'
                     '\\varepsilon_{\\dot\\beta\\dot\\delta}$ 的系数与符号），三条生成元的秩 $=%d$'
                     '（$\\Rightarrow$ 关系 %d 条）；同名 Grassmann 括号 $(\\psi\\psi)=%s$（必须非零：'
                     '若基元素不按生成元升序落定、漏掉那一次换序符号，它读成 $+1-1=0$），异名括号'
                     '$(\\psi_x\\psi_y)=%s$（两条互不重合的基元素、符号相反）' %
            (len(stier), len(srows), sanchr[0], sanchr[1], sanchr[2], 3 - sanchr[2],
             sanchr[3], sanchr[4]),
            not srows and not ssig_bad and len(stier) >= 6 and len(sback) >= 1 and
            sanchr[0] == F(2) and sanchr[1] == F(-2) and sanchr[2] == 1 and
            sanchr[3] == [(3, F(2))] and sanchr[4] == [(6, F(-1)), (9, F(1))],
            '表格档表（$\\nu$、$\\dot\\nu$、类数、预测、eps 秩、sigma 单独秩、并秩、eps 条数、'
            'sigma 去重条数、道间关系）：%s' % stab)
    p &= ok('R18.1', 'Fierz 在 $\\varepsilon$ 坐标里的**增益**是一个差额：$\\sigma$ 道并进并秩之后'
                     '新增结构 %d 条（挂类的档 %d 个、覆盖 %d 个类、档上预测秩合计 %d 条、道间关系'
                     '合计 %d 条 $=$ 每类 %s 条 $\\times$ 类数）。这一条必须**与前置判据同写**：只断言'
                     '"新增 $=0$"会放过一份非法的 $\\varepsilon$ 目录 $\\Rightarrow$ 写作时实测把带点侧'
                     '槽位的起点写错一档（目录跨手性），$\\varepsilon$ 秩从 1/2/2/4/5/5 涨到 '
                     '2/6/5/17/20/14 而"新增"仍读 0 $\\Rightarrow$ 保护这条读数的是前置等式，不是它'
                     '自己。前置违例 %d 档。还要核到类上：档上的预测值与 14.8 逐类登记的缩法重数'
                     '不符 %d 条 $\\Rightarrow$ 本层读的是 R16 那张表，不是另起炉灶' %
            (ssig_new, len(sback), ssig, ssig_m, ssig_rel,
             sorted(set(r[9] for r in sback)), len(ssig_bad), len(ssig_mp)),
            ssig_new == 0 and ssig > 0 and ssig_m > 0 and ssig_rel > 0 and
            ssig_rel == sum(scnt[k] * sig_cache[k][6] for k in sig_cache if scnt.get(k)) and
            not ssig_bad and not ssig_mp,
            '逐档道间关系：%s；跨类新增合计=%d' %
            ([[r[0], r[1], r[2], r[9]] for r in stab], ssig_new))
    p &= ok('R18.2', '第三张不共族的票要独立复现 14.9：把"哪两个名字缩在一起"的每一道写成 '
                     'Grassmann 单项式（同名槽共用一对反对易生成元）再数秩 $\\Rightarrow$ 它与甲'
                     '（显式投影）、乙（$\\Lambda^m(\\mathbb C^2)$ 表示论）、丁（同侧 Grassmann 求值）'
                     '都不共享算术。14.9 判定过的 %d 个类上逐类相乘后合计 %d 条，与 14.9 公布的'
                     '存活合计 %d 条不等者 %d 类 $\\Rightarrow$ 这条道在此**没有**给出 14.9 之外的'
                     '结构。道单项式共 %d 条（每类两侧接法数之积），故 %d 条道里独立标量只有 %d 条' %
            (sg_n, sg_ab, ftot[1], len(sg_abx), sg_ch, sg_ch, sg_ab),
            sg_n == sum(v[0] for v in fact.values()) == 838 and
            sg_ab == ftot[1] == 838 and not sg_abx and sg_ch > sg_ab,
            '违例前 3 条（档、两侧名字、14.9 秩、Grassmann 道秩）：%s' % sg_abx[:3])
    p &= ok('R18.3', '"秩只依赖组大小的多重集、不依赖槽位编号"这句要**每一种摆放**都成立才算数：'
                     '逐类枚举两侧的全部不同摆放（合计 %d 个摆放对）各自投影一次，违例 %d 类'
                     '$\\Rightarrow$ 14.9 那句"按 $(n,\\text{组大小})$ 缓存"被逐摆放复核过，而不是'
                     '只在规范摆放上复核过。反向登记一条：把同一份内容下**不同摆放**的像空间求并会'
                     '**虚高**（并成合计 %d 条，比 14.9 大的类 %d 个）$\\Rightarrow$ 那是把不同的槽位'
                     '空间识别成同一个空间的构造伪影，不是新增结构，故它不是一张票，只是一条要写'
                     '下来的数' %
            (sg_place, len(sg_pl), sg_un, sg_ungt),
            not sg_pl and sg_place >= sg_n > 0 and sg_un >= sg_ab and sg_ungt > 0,
            '摆放违例前 3 条：%s；并成虚高类数=%d（与 14.9 的"缩减类" %d 是**两个不同的量**，'
            '此处只登记自己那个数，不比大小）' % (sg_pl[:3], sg_ungt, len(fshr)))
    p &= ok('R18.4', '管辖范围也是一个数：14.9 判定的 %d 个类里，$\\sigma$ 道换基覆盖 %d 个，界外'
                     '登记 %s $\\Rightarrow$ 类集上真正出现的 $(\\nu,\\dot\\nu)$ 只有 %s 这 %d 档，'
                     '其中两侧皆非空的只有 $(2,2)$ 一档 $\\Rightarrow$ 本层的换基读数**挂类的**就只有'
                     '那一档，其余 %d 个表格档是算术复核、不挂在类上（把它们当类集读数就是虚报覆盖面）。'
                     '五道削减到此过了两道（Fermi 在 14.9、Fierz 的洛伦兹半边在本节），味指标、EOM、'
                     '全总导数塔三关照旧 $\\Rightarrow$ **类数仍然不是算符数**；且本层只比价过 $\\sigma$ '
                     '这一条道。本层不回填任何寿命、不改 P4／P7 的判据与分级，L10 保持 OPEN' %
            (sg_n, ssig, sskip, sreal, len(sreal), len(stier) - len(sback)),
            ssig + sskip['单侧空'] + sskip['超档'] + sskip['奇侧'] == sg_n == 838 and
            sskip['形状不符'] == 0 and sg_ab == ftot[1] and ssig > 0 and
            sskip['单侧空'] == sg_n - ssig and len(sreal) == 5 and (2, 2) in sreal,
            '类集 $(\\nu,\\dot\\nu)$ 档与类数：%s；表格档 %d 个、挂类档 %d 个' %
            (sorted(scnt.items()) and [[list(k), v] for k, v in sorted(scnt.items())],
             len(stier), len(sback)))
    return p


def residual_section():

    """报告 §9：$B-L$ 破缺后残留哪个离散规范对称性（R10）。"""
    r = RESID
    if not r.get('rows'):
        return ['', '## 9. 破缺之后残留什么离散规范对称性（R10）', '',
                '本层未跑通 ⇒ 不印任何读数。', '']
    n1 = next((x['N'] for x in r['rows'] if x['BL'] == '1'), 0)
    n2 = next((x['N'] for x in r['rows'] if x['BL'] == '2'), 0)
    L = ['', '## 9. 破缺之后残留什么离散规范对称性（R10）', '',
         '§4 与 §5 判的是"哪个分量**能**取期望值"，本节判的是"取了之后 $U(1)_{B-L}$ **还剩**'
         '什么"。这条差别此前只存在于散文里：报告与 [09_已知局限与否定清单](../'
         '09_已知局限与否定清单.md) 此前都写着"$|\\Delta(B-L)|=1$ 的单步破缺 ⇒ 残留 $Z_2$'
         '（物质字称，对质子稳定反而有利）"（报告侧共四处：§0 结论一览、§4 第 7 条、R5.5 与 '
         'R5.9 的判据文字；09 侧两处），而守这句话的门禁 R5.9 的读数是'
         '$(B-L,\\ SU(2)_L\\text{ 串长},\\ SU(2)_R\\text{ 串长})$ 三元组 $\\Rightarrow$ '
         '"残留群"从未被算过。本节把它变成三条路径的读数（甲：精确有理；乙：浮点几何枚举；'
         '丙：整套荷同乘 $1/2$ 的换约定测试），并且**当场推翻那句散文**：下面这些读数出来后，'
         '上述六处已按读数改写，证伪记录见 [08](../08_预言与判据.md) §3 的内部计算否定表（F7）。', '',
         '**荷格把圆周定死**（R10.0/R10.1）：$16_F$ 的 $B-L$ 值集合为'
         '$\\{%s\\}$ $\\Rightarrow$ 其 $\\mathbb{Z}$-生成元 $g_0=%s$，于是'
         '$U(1)_{B-L}$ 作为**作用在在场态上的**圆群，其周期是 $\\alpha_0=2\\pi/g_0=%s\\pi$。'
         '把 $\\dim\\le210$ 表内 %d 个表示全部加进来，$g_0$ 仍是 $%s$（R10.0）$\\Rightarrow$ '
         '周期不是"选了哪个标量谱"的函数。浮点路径独立扫出的最小平凡角 $=%s\\pi$，'
         '与精确值 $2/g_0=%s$ 同（R10.1）——这个周期是**量出来的**，不是抄来的归一化。' %
         ('、'.join(str(x) for x in r['bls']['16']), r['g0_matter'], r['period_exact'],
          r['nrep'], r['g0_all'], r['period_scan'], r['period_exact']), '',
         '| 候选 $q_\\Delta$ | 承载它而保电磁的表示 | 残留阶 $N$（甲） | 同（乙，浮点枚举） | '
         '同（丙，$B-L\\mapsto(B-L)/2$） | 植入缺陷：只缩 $q_\\Delta$／误取 $2\\pi$ 周期 | '
         '$(-1)^{3(B-L)}$ 在 v.e.v. 上 | 再取一个 $B-L=0$ 的 v.e.v. 后剩 | '
         '对照：再取 $q_\\Delta/2$ 后剩 |',
         '|---|---|---|---|---|---|---|---|---|']
    for x in r['rows']:
        L.append('| $%s$ | %s | %d | %d | %d | %s／%d | %s | %d | %d |' %
                 (x['BL'], higgs_tex(x['carriers']), x['N'], x['N_scan'], x['N_half'],
                  '无解' if not x['N_mismatch'] else x['N_mismatch'], x['N_naive'],
                  '存活' if x['mp'] == 1 else '**被破**', x['ew'], x['ctl']))
    L += ['', '三条路径在同一批数上咬合（R10.2/R10.7），而"植入缺陷"那一列是**故意用错的约定**：'
              '只把 $q_\\Delta$ 减半而不同步缩荷格，残留阶要么被腰斩、要么根本不再是整数'
              '（工具拒绝给数，印成"无解"）；误把圆周当成 $2\\pi$（即默认荷格是 $\\mathbb{Z}$），'
              '残留阶就退化成 $q_\\Delta$ 本身 $\\Rightarrow$ 上面那些断言不是恒真式，而第二个错值 '
              '$\\mathbb{Z}_2$ **正是旧散文那句"残留 $\\mathbb{Z}_2$"的出处**——它属于归一化滑倒，'
              '而且被挂到了本来没有 2 阶元的那条通道上（R10.8）。', '',
              '**残留群的两个子群各自是谁**（R10.3/R10.4）：', '',
              '* $N$ 为偶时那个 **2 阶元**（$\\alpha=3\\pi$，即群参数 $k=N/2$）作用在荷 $q$ 上是 '
                '$(-1)^{3q}$。它在 $16_F$ 的每一条权重上都取 $-1$（$1/3,\\,-1/3,\\,1,\\,-1$ 乘 3 '
                '全是奇数），而在 %s 的每一条权重上都取 $+1$ $\\Rightarrow$ 它就是把"物质"与'
                '"标量＋规范"分开的**物质字称**；表内例外只有 %s（含 $3(B-L)$ 为奇的分量）'
                '$\\Rightarrow$ "标量一定偶"是**算出来**的，不是设定的，而且圆周上那个元与抽象分次'
                '是同一个东西（逐荷对照见 R10.3）。' %
              (plain_tex(r['even']), plain_tex(r['odd'])),
              '* **3 阶元**只看 $3q\\bmod 3$。本节把它对到**色表示自己的 triality** 上：表内 %d 个'
                '表示的每一条权重都满足 $3(B-L)\\equiv %s(p-q)\\pmod 3$，$(p,q)$ 是该权重的 $A_2$ '
                'Dynkin 标号、符号由数据选定（两种都测，只有一处无反例才通过）$\\Rightarrow$ 那个 '
                '$\\mathbb{Z}_3$ **就是**按色 triality 计数的元。两条对照同时成立：色单态必平凡'
                '（反例 %d 条），但反向**不成立**——非单态而 $p-q\\equiv0\\pmod3$ 的（色八重态一类）'
                '也平凡，共 %d 条 $\\Rightarrow$ "按色三重态计数 mod 3"作为口号只在 mod 3 意义下成立，'
                '逐字成立的是那条同余式（R10.4）。' %
              (r['nrep'], r['triality_sign'], len(r['singlet_nontrivial']),
               len(r['nonsinglet_trivial'])), '',
              '**被本节改掉的一句散文**（R10.5/R10.6）：$|\\Delta(B-L)|=1$ 那条通道把 $U(1)_{B-L}$ '
              '留成 $N=%s$ $\\Rightarrow$ %s —— 阶为奇 $\\Rightarrow$ 里面**没有** 2 阶元可言，'
              '而且物质字称元作用在该 v.e.v. 的荷上就是 $-1$ $\\Rightarrow$ 物质字称是**被这一步'
              '破掉的**，不是这一步留下的。反过来，$|\\Delta(B-L)|=2$ 那条通道（$R=2$ 那个 v.e.v.）'
              '留下 $N=%s$ $\\Rightarrow$ %s 里**同时**含一个 2 阶元（物质字称）与一个 3 阶元'
              '（色 triality），因为该 $N$ 同时被 2 与 3 整除（R10.6 的 $N\\bmod 2$、$N\\bmod 3$ '
              '两列；$N$ 是 3 的倍数这件事由 $g_0=1/3$ 保证 $\\Rightarrow$ triality 在这个物质内容下'
              '躲不掉，条件性的只有 2 阶元那半边）。一句判据把两件事收干净：'
              '物质字称存活 $\\Leftrightarrow$ $N=q_\\Delta/g_0$ 为偶 $\\Leftrightarrow$ $3q_\\Delta$ '
              '为偶（R10.6，逐个候选核对）。' % (n1, ztex(n1), n2, ztex(n2)), '',
              '**弱电那一步不会进一步削弱它**（R10.9）：'
              '"色单态、$Q=0$、$B-L=0$"的候选在表内非空（%s），而 $B-L=0$ 的 v.e.v. 对整个残留群'
              '恒等 $\\Rightarrow$ 上面那个 $\\mathbb{Z}_N$ 一路活到标准模型能标之下。这句话有对照：'
              '表里倒数第二列把每个残留元代回 $e^{i\\alpha q_2}$ 逐元计数，$q_2=0$ 时剩下的元数'
              '与 $N$ 相同（%s），而同一处取 $q_2=q_\\Delta/2$ 的对照**确实减少**（最后一列）'
              '$\\Rightarrow$ "不削弱"是被测出来的，不是"$0\\cdot\\alpha=0$"的套话。' %
              ('、'.join(tex_name(n) for n in r['ew_neutral']) or '（本层未读到）',
               '、'.join('$q_\\Delta=%s$：$%d\\to%d$' % (x['BL'], x['N'], x['ew'])
                        for x in r['rows'])), '',
              '**条件性（R10.10）**：两个数都是**条件读数**。承载 $|\\Delta(B-L)|=2$ 的 '
              '$126_H/\\overline{126}_H$ 与承载 $|\\Delta(B-L)|=1$ 的 $16_H/\\overline{16}_H$ '
              '都不在链探针三个情形**字面声明**的标量谱里（各情形声明：%s；把每条通道的承载者与'
              '该并集求交：%s，全为空）$\\Rightarrow$ '
              '"残留 %s" 要读成"若补入 $126_H$ 且其中性分量取期望值"。'
              '这与 §8 那条"$120_H$ 无人声明"是同一族缺陷：**离散规范对称性的内容跟着标量谱走，'
              '而标量谱仍是手工放置的** $\\Rightarrow$ 本节的数不回填进质子寿命或任何暗物质论证。' %
              ('；'.join('%s：%s' % (k, higgs_tex(v) if v else '无')
                         for k, v in sorted(r['decl'].items())) or '未读到',
               '；'.join('$|\\Delta(B-L)|=%s$ ∩ 声明谱 $=\\{%s\\}$' % (b, '、'.join(c))
                         for b, c in r['cond']), ztex(n2)), '',
              '**本节的边界**（不进门禁，故明写）：', '',
              '* 只算 $U(1)_{B-L}$ **这一个因子**内的残留：$SU(2)_{L/R}$ 与 $SU(3)_c$ 的中心、'
                '以及规范群的整体形式（$Spin(10)$ 与它的商）都不在本节的权重算术里 $\\Rightarrow$ '
                '完整的残留群可能是这里那个 $\\mathbb{Z}_N$ 的**扩张**，本节只给出"至少留下这些"'
                '（这条边界已由 §11/R12 做成读数：完整残群逐个中心元数出来了，且在 §10 的 SM '
                '单态片上与这里那个 $\\mathbb{Z}_N$ 逐条同判）。',
              '* 走 422 链时 $B-L$ 不是独立因子（它坐在 $SU(4)_c$ 的 Cartan 里，见 §5 的 R6.7）'
                '$\\Rightarrow$ 那条链上的残留要按 $SU(4)$ 的权格重做（§12/R13 已把这条补成读数：'
                '判决不换）。',
              '* 残留群在低能**能禁哪些算符**是另一个问题：本节只数群元与其作用，'
                '没有逐个算 $u^cd^cd^c$ 一类的 SM 不变算符拿什么表示 $\\Rightarrow$ 那一问由 §10'
                '（R11）接手，本层的两条阶读数只到"群里有什么元"为止。',
              '* 量子引力是否允许全局/离散规范对称性、以及 $B-L$ 破缺前的其它阈值效应，都在本节'
                '之外 $\\Rightarrow$ **L10 未关闭**。', '']
    return L


def selection_section():
    r"""报告 §10：残留离散规范对称性在低能算符上的选择定则（R11，即 08 的 P7 那一问）。

    全部读数取自 SEL（`run_selection_layer` 的产出），本节不重算任何东西。
    """
    s = SEL
    if not s.get('hit4'):
        return ['', '## 10. 残留群禁哪些低能算符（R11）', '', '本层未跑通 ⇒ 不印任何读数。', '']
    mat, c4, hit4, pr = s['mat'], s['c4'], s['hit4'], s['proj']
    pv, pvl, r2, r4 = s['pv'], s['pvl'], s['r2'], s['r4']
    n1, n2 = s['chans']['|1|'][1], s['chans']['|2|'][1]
    pvn = set(x['name'] for x in pv)
    rho = '(%s)' % ', '.join(str(x) for x in pr['rho'])
    dis4 = [x['name'] for x in hit4
            if x['v']['|1|']['甲'] is not True or x['v']['|2|']['甲'] is not True]
    pvdis = sum(1 for x in pvl if x['v']['|2|']['甲'] is not True)
    bad3_sing = sum(1 for t in s['bad3'] if t[3])
    lost4, over4 = s['lost4'], s['over4']
    top4 = max(over4, key=lambda t: t[1]) if over4 else ('—', 0, 0)

    def vd(x, tag):
        v = x['v'][tag]['甲']
        return '允许' if v is True else ('—' if v is None else '**禁戒**')

    L = ['', '## 10. 残留群禁哪些低能算符（R11）', '',
         '§9 只数到"群里有什么元"为止，并把"它能禁哪些算符"登记为待办 $\\Rightarrow$ 本节做那一问'
         '（那条待办登记在 [08](../08_预言与判据.md) 的 P7 一节末尾）。判据只有一条同余式：'
         '总荷 $Q=\\sum_k(B-L)_k$ 的算符在 '
         '$\\mathbb{Z}_N$（$N=q_\\Delta/g_0$，$g_0=%s$ 由 R10.0 在荷格上量出，不是归一化约定）下不变 '
         '$\\iff$ $N\\mid 3Q$。每条判决由三条互不共享算术的实现各跑一遍（甲 整数整除、乙 群元逐个代回 '
         '$e^{i\\alpha q}$、丙 浮点角度）并要求同判决；另加因子检查：$\\mathbb{Z}_3$ 看 $3Q\\bmod3$、'
         '$\\mathbb{Z}_2$ 看 $3Q\\bmod2$，两者取与须等于甲 $\\Rightarrow$ '
         '$\\mathbb{Z}_6=\\mathbb{Z}_2\\times\\mathbb{Z}_3$ 的分解在下面每一行上都是数过的，不是修辞。'
         % s['proj']['g0'],
         '',
         '**projector 先要选对**（R11.0）：$SU(2)_L$ 的单根与 $Y$ 正交（内积 $=%d$）而 $SU(2)_R$ 的单根'
         '与 $Y$ **不**正交（$=%d\\ne0$）$\\Rightarrow$ $U(1)_Y$ 与 $SU(2)_R$ 混在一起，沿 $3221$ 数'
         '"零权"等于在荷守恒之外多要 $T^3_R=0$ 与 $B-L=0$。后果正落在最要紧的那个场上：$16_F$ 的权重里'
         '零权方向 %d 个，但它有 %d 个 $SU(3)\\times SU(2)_L\\times U(1)_Y$ 单态，就是 $\\nu^c$'
         '（3221 行 $%s$、引擎号 $B-L=%s$）$\\Rightarrow$ 拿"零权"当 projector 会把承载 Majorana 质量的'
         '那个场整个漏掉。本节全部低能计数因此放在 $Y$ 切片上（子系统正根 %d 条、Weyl 群 %d 元、'
         '$\\rho_{321}=%s$）。' % (pr['ip'][0], pr['ip'][1], pr['zw16'], pr['nsing'], pr['nu'][0],
                                  pr['nu'][1], pr['pos'], pr['W'], rho), '',
         '**SM 分解的实现由维数账独立核对**（R11.1）：$\\sum_\\lambda n_\\lambda'
         '\\dim_{\\mathrm{SM}}(\\lambda)$ 与 Weyl 维数逐表示相平。把"先按 $Y$ 切片"这一步去掉、直接对'
         '整个多重集作同一条 Klimyk 交错和，同一本账**全部**立刻不平（末列即那个错账）$\\Rightarrow$ '
         '切片不是可选的装饰，而维数账能看见它。', '',
         '| 表示 | 低能成分条数 | $\\sum n\\dim_{\\mathrm{SM}}$ | Weyl 维数 | 植入缺陷：不切片的错账 |',
         '|---|---|---|---|---|']
    for b in s['books']:
        L.append('| $%s$ | %d | %d | %d | %d |' % (b[0], b[1], b[2], b[3], b[5]))
    L += ['', '**场清单与荷账**（R11.3/R11.4）：$16_F$ 展开成 %d 条低能场，每条满足"一个 3221 行 '
              '$\\times$ 一个 $Y$ 切片 $=$ 一条重数为 1 的 SM 不可约表示"，且这 %d 条的权重**恰好分成** '
              '$16_F$ 的 16 条权重（多重集相等，不只是维数相加）$\\Rightarrow$ 场清单是量出来的；名字由 '
              '$(\\lambda,Y,B-L)$ 签名绑定——只按 (色,弱) 定名会把 %d 条读成 %d 类，故 $Y$ 必须参与定名。'
              '$B$、$L$ 不外部填入，而由一条规则从量出来的 (色, $B-L$) 派生：色非单态者 $B=B-L$、$L=0$，'
              '色单态者 $L=-(B-L)$、$B=0$；该规则在 $16_F$ 里反例 %d 条，且派生的 $(B,L)$ 多重集与教材'
              '一代六个场**相同**（这一列是**比对、不是推导**，与 R6.6 同一处置 $\\Rightarrow$ 同时植入'
              '变异体：把规则里"哪一半携带 $B$"对调，多重集立刻不等）。下表末列 $3(B-L)$ **全是奇数** '
              '$\\Rightarrow$ 在只含物质场的算符上 $(-1)^{\\sum_k3(B-L)_k}=(-1)^{\\text{费米子数}}$ '
              '恒等，即 §9 那条 2 阶元在低能就是**物质字称**。' %
              (len(mat), len(mat), len(mat), len(set((f['lam'][:2], f['lam'][2]) for f in mat)),
               sum(1 for f in mat if (f['lam'][:2] != (0, 0)) == (f_l(f) != 0)) +
               sum(1 for f in mat if (f['lam'][:2] == (0, 0)) == (f_b(f) != 0))), '',
              '| 场 | $(\\mathrm{色},\\mathrm{弱})$ Dynkin | $Y$ | $B-L$（教材号） | $B$ | $L$ | '
              '$3(B-L)$ | 该场权重条数 |',
              '|---|---|---|---|---|---|---|---|']
    for f in sorted(mat, key=lambda x: x['name']):
        L.append('| $%s$ | $(%s)$ | $%s$ | $%s$ | $%s$ | $%s$ | $%s$ | %d |' %
                 (f['name'], ','.join(str(x) for x in f['lam']), f['Y'], f_bl(f),
                  f_b(f), f_l(f), 3 * f_bl(f), f['nwt']))
    L += ['', '**$\\mathbb{Z}_3$ 的荷完全由色携带**（R11.2）：把 R10.4 那条同余从 SO(10) 的**权重**搬到 '
              'SM 的**场**上，对表内 %d 个表示展开出的 %d 条低能场逐条核 $3(B-L)\\equiv s(p-q)\\pmod 3$。'
              '**符号不是抄来的**：两套荷号 $\\times$ 两种符号的四种配对全部测过 $\\Rightarrow$ 教材号唯一'
              '一致 $s=%s$（配 $-$ 号反例 %d 条）、引擎号唯一一致 $s=%s$（配 $+$ 号反例 %d 条），而 R10.4 '
              '在权重层（引擎号）读到的是 $%s$ $\\Rightarrow$ 两层是**同一条**同余，它们之间差的恰好是 '
              'R5.7/R6.6 那条已登记的"教材号 $=-$ 引擎号"约定差。分档读数：triality %s $\\Rightarrow$ '
              '非平凡的那一半**全部**是色三重态，色单态（triality 0）自动中性。' %
              (s['nrep'], s['tri_tot'], s['tri_sgn'], s['tri_bad']['std'][1], s['tri_sgn_engine'],
               s['tri_bad']['eng'][0], s['tri_wt_sgn'],
               '、'.join('$%d$：%d 条' % (k, s['tri_cnt'].get(k, 0)) for k in (0, 1, 2))), '',
              '**低能单态的总数由三条不共享算术的路径给出同一个数**（R11.5）：(i) 逐条场组合算 SM 单态、'
              '再乘该多重集所代表的有序组数；(ii) 直接对 $16^{\\otimes n}$ 的整权重乘积作 Klimyk 交错和；'
              '(iii) 先在 SO(10) 层把 $16^{\\otimes n}$ 拆成不可约表示（R8 的独立机器）再逐表示投影。'
              '读数：$n=2$ 三路径 $=%s$（%d 个场内容类、SO(10) 侧 %d 个不可约），$n=4$ 三路径 $=%s$'
              '（%d 类、%d 个不可约）$\\Rightarrow$ "按场内容分类"与"按 SO(10) 道分类"是同一件事的两种'
              '数法。两条物质场相乘里含单态的只有 %d 类，即 %s（单态数 %d、$\\Delta B=%s$、'
              '$\\Delta L=%s$、$3Q=%s$）——物质双线性里唯一的低能不变算符就是右手中微子的 Majorana 项，'
              '而它在两条通道下的判决都是**允许**（R11.6）。' %
              (','.join(str(v) for v in r2[1:4]), len(r2[0]), r2[4],
               ','.join(str(v) for v in r4[1:4]), len(r4[0]), r4[4],
               len(s['hit2']), '$%s$' % s['hit2'][0]['name'], s['hit2'][0]['singlet'],
               s['hit2'][0]['dB'], s['hit2'][0]['dL'], s['hit2'][0]['t3q']), '',
              '**四条物质场（质量维数 $d=6$）的完整判决表**（R11.7/R11.8）：%d 个场内容类里含 SM 单态的 '
              '%d 条（合计 %d 个不变张量结构），逐条按 $N\\mid 3Q$ 判 $\\Rightarrow$ **允许 %d 条、'
              '禁戒 %d 条**：' %
              (len(c4), len(hit4), sum(x['singlet'] for x in hit4), len(hit4) - len(dis4), len(dis4)),
              '',
              '| 场内容 | 单态数 | $\\Delta B$ | $\\Delta L$ | $\\Delta(B-L)$ | $3Q$ | '
              '$|\\Delta(B-L)|=1$ 留 %s | $|\\Delta(B-L)|=2$ 留 %s | "3221 零权"读数 | 质子荷前提 |'
              % (ztex(n1), ztex(n2)),
              '|---|---|---|---|---|---|---|---|---|---|']
    for x in hit4:
        L.append('| $%s$ | %d | $%s$ | $%s$ | $%s$ | $%s$ | %s | %s | %d | %s |' %
                 (x['name'], x['singlet'], x['dB'], x['dL'], x['q'], x['t3q'],
                  vd(x, '|1|'), vd(x, '|2|'), x['zero'],
                  '**是**' if x['name'] in pvn else '—'))
    L += ['', '最后一列是"质子衰变的荷前提"（$\\Delta B\\ne0$ 且 $\\Delta L\\ne0$，等价地 '
              '$|\\Delta B|=|\\Delta L|=1$），它把这张表与"残留群能不能救质子"那一问直接接上：'
              '**残留离散规范对称性不保质子**。含单态的 %d 条里有 %d 条同时 $\\Delta B\\ne0$ 与 '
              '$\\Delta L\\ne0$（%s），'
              '其中 $\\Delta(B-L)=0$ 的 %d 条判决全部是**允许**（被禁 %d 条）。机理也是读数，两半边各'
              '量一次：(α) 把那条同余从场搬到算符，%d 条 d=6 候选上 $3Q$ 与色侧和 $s\\sum_k(p_k-q_k)$ '
              '模 3 不同余的有 %d 条 $\\Rightarrow$ 同一判据有两台互不相同的机器在跑；而 $\\mathbb{Z}_3$ '
              '判禁的那 %d 条里**含 SM 单态的** %d 条 $\\Rightarrow$ 它只能禁色非单态，"要单态"这一步在'
              '枚举里早已把它们滤掉，故在低能单态层 $\\mathbb{Z}_3$ 这一半**没有**额外信息。'
              '(β) $\\mathbb{Z}_2$ 那一半看 $3Q\\bmod2$，而每条物质场的 $3(B-L)$ 都是奇数 $\\Rightarrow$ '
              '偶数条相乘必为偶：%d 条里 $3Q$ 为偶的有 %d 条 $\\Rightarrow$ 物质字称那半边在 d=6 这一层'
              '同样没有可禁的东西（但它并非恒等无物——下面插入标量的候选就是被它判禁的）。' %
              (len(hit4), len(pv), '、'.join('$%s$' % x['name'] for x in pv), len(pvl), pvdis,
               len(c4), len(s['congr']), len(s['bad3']), bad3_sing, len(c4), s['even3q']), '',
              '**"禁掉 0 条"与"枚举到 0 条"必须可区分**（R11.9），故把判据放在能动的四处测：'
              '(i) 枚举到的候选数非空——d=6 类 %d 条、双线性 %d 条、插入链上**字面声明**谱（%s）的 d=4 '
              '候选 %d 条。'
              '(ii) 换成插入 $3(B-L)$ 为**奇**的标量（%s 型，它们自己就把物质字称破了）：'
              '候选 %d 条，其中 %s **判禁 %d 条** $\\Rightarrow$ "禁"这一支是活的。(iii) 把 %s 误读成 '
              '%s（丢掉物质字称那半边）：在同一批候选上出现 %d 条判决差异 $\\Rightarrow$ 两个因子各自'
              '都在做功。(iv) 反向对照：把整套荷换号（引擎号 $\\leftrightarrow$ 教材号）时判决翻转 '
              '**%d** 条——这一条必须为 0，不为 0 就说明结论其实挂在记号上而不是荷上。' %
              (len(hit4), len(s['hit2']), higgs_tex(s['sdecl']), len(s['scan_decl']),
               higgs_tex(s['hyreps']), len(s['scan_odd']), ztex(n2), len(s['forb_odd']),
               ztex(n2), ztex(n1), len(s['flip3']), len(s['flip_sg'])), '',
              '**条件性（R11.10）**：上面每一行判决都挂在 §9 那个空交集上——$q_\\Delta=2$ 通道的母表示 '
              '$126_H/\\overline{126}_H$ 不在链探针字面声明的标量谱里（声明的只有 %s，承载者与该并集的'
              '交集 %s 全为空）$\\Rightarrow$ "只按声明谱"那一步里残留群根本还没出现，那里的被禁条数不是'
              '物理数而是"无从谈起"。把 $126/\\overline{126}$ 的分量当假想插入重跑同一条判据（与 R10.10、'
              'R7.4、R8.5 同一条假设）：候选 %d 条、两条通道都允许 %d 条 $\\Rightarrow$ 补上母表示**不'
              '改变**"不保质子"这个判决。但质子那一条结论里有一处**无条件**成分：它只依赖"偶数条物质场 '
              '$\\Rightarrow$ $3Q$ 为偶"，而偶费米子数不是插入出来的 $\\Rightarrow$ 登记清楚，以免与上面'
              '那些条件判决混读。' %
              (higgs_tex(s['sdecl']) or '无',
               '、'.join('$|\\Delta(B-L)|=%s$：$\\{%s\\}$' % (b, '、'.join(c) or '空')
                        for b, c in RESID['cond']), len(s['scan_126']), len(s['allow_126'])), '',
              '**projector 的对照也只用读数说话**（R11.7）：这 %d 条含单态的候选里，"3221 零权"那个错投影'
              '读出 0 的有 %d 条（%s）$\\Rightarrow$ 它**漏掉**真单态；而它在别的候选上读出的数又大于单态数'
              '（最大一例 $%s$：零权 %d $>$ 单态数 %d）$\\Rightarrow$ 它也**多算**。两个方向都有反例 '
              '$\\Rightarrow$ "零权数"与"单态数"之间**没有**不等式关系，谁也不是谁的界 $\\Rightarrow$ '
              '凡要数低能不变量，只能用 $Y$ 切片上的 Klimyk。' %
              (len(hit4), len(lost4), '、'.join('$%s$' % t for t in lost4),
               top4[0], top4[1], top4[2]), '',
              '**本节的边界**（不进门禁，故明写）：', '',
              '* 表里的"允许"是**群论陈述**：只过了规范不变这一关。Lorentz 指标、代（味）指标与 Fierz '
              '恒等式三关都没过 $\\Rightarrow$ "%d 条 d=6 类含单态且全部允许"不能读成"有 %d 个质子衰变'
              '算符"，本节的数**不**回填进任何寿命计算（与 §7 同一处置；P4／P7 的判据与分级一律不动）。' %
              (len(hit4), sum(x['singlet'] for x in hit4)),
              '* 枚举的是物质场分量（$\\pm$ 声明谱或假想插入的标量分量）张成的算符，且只到 $d=6$：'
                '含导数算符、含共轭场的高维算符、以及 $\\nu^c$ 以外的轻子数破缺结构都**未**枚举。',
              '* 判据只在 $U(1)_{B-L}$ 那一个因子导出的残留群上跑（§9 的边界原样继承）$\\Rightarrow$ '
                '若完整残留群是它的扩张（$SU(3)_c$ 与 $SU(2)_{L/R}$ 的中心、$Spin(10)$ 的整体形式），'
                '本节的"允许"可能变严、"禁戒"不会变松。',
              '* 本节回答的是上一条待办（残留群在低能的**选择定则**，登记在 08 的 P7 一节里），'
                '**不**回答 L10：耦合统一仍缺二环跑动与阈值修正 '
                '$\\Rightarrow$ **L10 未关闭**。', '']
    return L


def global_section():
    r"""报告 §11：完整的残留离散规范群（中心 × Spin(10) 的整体形式），R12 族。

    全部读数取自 GLOB（`run_global_layer` 的产出），本节不重算任何东西。
    """
    g = GLOB
    rows, ctl, forms = g.get('rows') or [], g.get('ctl') or [], g.get('forms') or []
    sing, gam, bys = g.get('sing') or [], g.get('gampairs') or [], g.get('bys') or []
    b1 = [b for b in bys if b['qd'] == '1']
    b2 = [b for b in bys if b['qd'] == '2']
    if not (gam and rows and ctl and forms and sing and len(ctl) == 2 and b1 and b2):
        return ['', '## 11. 完整残留群与整体形式（R12）', '', '本层未跑通 ⇒ 不印任何读数。', '']
    q1 = [r for r in rows if r['qd'] == '1']
    q2 = [r for r in rows if r['qd'] == '2']
    c1 = next((c for c in ctl if c['qd'] == '1'), None)
    c2 = next((c for c in ctl if c['qd'] == '2'), None)
    if not (q1 and q2 and c1 and c2):
        return ['', '## 11. 完整残留群与整体形式（R12）', '',
                '两条通道没同时读到（行 %s / 对照 %s）⇒ 不印任何读数。' %
                (sorted(set(r['qd'] for r in rows)), sorted(set(c['qd'] for c in ctl))), '']

    L = ['', '## 11. 完整残留群与整体形式（R12）', '',
         '§9 与 §10 的边界都写着同一句话：判据只在 $U(1)_{B-L}$ **那一个因子**导出的群上跑，'
         '若完整残留群是它的扩张（$SU(3)_c$ 与 $SU(2)_{L/R}$ 的中心、$Spin(10)$ 的整体形式），'
         r'"允许"可能变严、"禁戒"不会变松 $\Rightarrow$ 那条待办登记在 [08](../08_预言与判据.md) 的 '
         'P7 一节末尾。本层把那句话搬到账上：先数出覆盖群的核，再数出破缺之后的**完整**残留群，'
         '然后回到 §10 那批算符上逐条比对。用的还是同一套格点算术，没有新引进李论输入。', '',
         r'### 11.1 覆盖群的核 $\Gamma$（R12.1）', '',
         r'$SU(3)_c\times SU(2)_L\times SU(2)_R\times U(1)_{B-L}$ 到 $Spin(10)$ 的映射的核，'
         r'就是"在**在场谱的每一条** 3221 分量上都作用平凡"的那批中心元 $\Rightarrow$ '
         r'枚举即可，不需要引用文献里那句"核是 $\mathbb Z_6$"。候选元 %d 个（色 $\mathbb Z_3$、'
         r'两个 $\mathbb Z_2$、$t\in\frac{1}{%d}\mathbb Z/%d\mathbb Z$），'
         '谱上不同的 (行标号, $B-L$) %d 条，活下来 %d 个：' %
         (g['ncand'], g['tstep'], g['uper'], g['nspec'], len(gam)), '',
         '| 群元 $(a_3,a_L,a_R,t)$ | 阶 | 在哪些因子上非平凡 |', '|---|---|---|']
    for x, o in gam:
        where = []
        if x[0]:
            where.append('色')
        if x[1]:
            where.append('$SU(2)_L$')
        if x[2]:
            where.append('$SU(2)_R$')
        if x[3] != 0:
            where.append('$U(1)_{B-L}$')
        L.append('| %s | %d | %s |' % (ctex(x), o, '、'.join(where) or '—'))
    L += ['', r'它的阶分布是 %s $\Rightarrow$ 交给"穷举该阶上全部阿贝尔群、比对元素阶多重集"那一步'
              r'（这一阶上候选共 %d 个），定出 $\Gamma\cong%s$，其中 %d 阶生成元 %d 个。'
              '两条对照：**(i)** 它是**对角**粘合而不是"各因子随便取 6 个元"——形如 $(0,0,0,t)$ 的'
              r'存活元只有单位元（%d 个）$\Rightarrow$ 谁也不是把某个 $U(1)$ 子群商掉；那 %d 个 2 阶元'
              r'同时带着两个 $SU(2)$ 中心再加半整数 $t$，%d 个 3 阶元各自是"色中心 $\times$ $U(1)$ 元"'
              r'（两者都列在上面的表里，且由 R12.1 逐坐标钉住）。'
              r'**(ii)** 约定无关：色 $\mathbb Z_3$ 有两个生成元，两种约定各给 %d / %d 元；把它们'
              r'当成候选网格里的坐标点集来比，%s（甲 $p+2q$、乙 $2p+q$），**但**把自同构 '
              r'$a_3\mapsto 2a_3$ 作用到甲那支上严格等于乙那支（%s）$\Rightarrow$ 核的大小与同构型'
              r'都不随"把哪个元叫 1"而变，变的只是那个称呼。本层沿用的是 R10.4 从数据选定的符号'
              r'（%s）。'
              r'网格够用：候选网格里 $t$ 的分母本来可以取到 %s，存活元实际落在 %s $\Rightarrow$ '
              '更大的分母上没有元被网格挡在外面。' %
              (g['gords'], len(g['gall']), mth(ab_tex(g['gstruct'])), len(gam), len(g['gens6']),
               len(g['gupure']), g['gords'].count(2), g['gords'].count(3),
               g['gsizeA'], g['gsizeB'],
               '它们就是同一个集合' if g['gsame'] else '它们是两个不同的点集',
               '成立' if g['gconj'] else '**不成立**', g['convf'],
               uni(g['gden']), uni(g['tden'])), '',
         r'### 11.2 $|\Gamma|$ 的三条出处（R12.2）', '',
         '| 路数 | 做法 | 读数 |', '|---|---|---|',
         '| 甲 权格指数 | $[P_H:P_{10}]$，$P_H$ 由 3221 半单部分的基本权加 $U(1)_{B-L}$ 的特征格'
         '方向 $u$ 生成 | %s（不变因子 %s）|' % (g['idx_h'], g['fac_h']),
         '| 乙 中心元枚举 | 上一节，逐元试 | %d |' % len(g['gam']),
         r'| 丙 经 $SU(4)$ 可乘 | $[P_H:P_{422}]\cdot[P_{422}:P_{10}]$ | %s × %s = %s |' %
         (g['idx_422'], g['idx_hop'], (g['idx_422'] or 0) * (g['idx_hop'] or 0)),
         '',
         r'三条同数 $\Rightarrow$ %d 不是枚举出来的巧合。**诚实登记**：甲与丙共用同一套 Smith 标准形'
         r'代码 $\Rightarrow$ 丙核对的是**格的嵌套**（$P_{10}\subset P_{422}\subset P_H$，两个不变'
         '因子都只有一个非平凡元，且行列式交叉核对 %s/%s/%s 全真），不是第三条独立算术；真正与格无关'
         '的只有乙。另外甲里 $u$ 的归一化是**量出来**的：取 $u=3(B-L)$ 时 $P_{10}$ 根本不在 $P_H$ 里'
         r'（这台机器直接返回"不给数"而不是放宽），取 $u=\frac{B-L}{4}$ 才包含 $\Rightarrow$ '
         '那个 $1/4$ 不是抄来的约定。422 一侧只搬了格陈述：`SUB_422` 的单根不是 $A_3$ 链，'
          r'拿它逐枚举中心元会把 triality 公式用错 $\Rightarrow$ 那一条**只有**甲一路，本节据此把它'
          '记在边界里（该边界现已补：422 侧改用特征标格枚举中心元，与甲的 Smith 标准形 %s '
          r'两台代码同数 $\Rightarrow$ 422 一侧现在也有两条独立出处，见 §12/R13）。' %
          (g['idx_h'], g['chk_h'], g['chk_422'], g['chk_hop'], g['idx_422']), '',
         '### 11.3 破缺之后的完整残留群（R12.3）', '',
         r'存活群 $=$ 让 v.e.v. 不变的那些 $(a_3,a_L,a_R,t)$，再**商掉** $\Gamma$ 才是低能真正剩下的'
         '离散群。下表逐承载者数：', '',
         r'| $\Delta(B-L)$ | 承载者 | 3221 行 | 存活元 | 商后 $\Gamma$ 陪集数 | 结构 | 与 §9 的 $\mathbb Z_N$ '
         '比 | 标的集合相同 | 允许集相同 | 相位因子化 |', '|---|---|---|---|---|---|---|---|---|---|']
    for r in rows:
        L.append('| $%s$ | %s | $%s$ | %d | %d | %s | %s | %s | %s | %s |' %
                 (r['qd'], tex_name(r['rep']), r['lab'], r['surv'], r['coset'],
                  ('%s（%s）' % (ab_tex(r['struct']),
                                 '循环' if r['cyc'] else '不循环，指数 %d' % r['expo'])),
                  r'§9 只看到 %s（%d 阶）' % (ztex(r['N']), r['N']),
                  '是' if r['same_char'] else '**否**',
                  '是' if r['same_allow'] else '**否**',
                  '是' if r['fact'] else '**否**'))
    L += ['', r'读数里没有一列空转：承载者共 %d 个（$q_\Delta=1$ 那批 %d 个、$q_\Delta=2$ 那批 %d 个）。'
              r'**大小**确实只挂在 $|\Delta(B-L)|$ 上：$q_\Delta=1$ 那 %d 个一律给 (存活 %s, 商后 %s)，'
              r'$q_\Delta=2$ 那 %d 个一律给 (存活 %s, 商后 %s)，且每个存活数都是 $|\Gamma|=%d$ 的整数倍 '
              r'$\Rightarrow$ 每个承载者都真的含 $\Gamma$，"商掉"这一步对每一条都成立。'
              r'**但同构型挂在承载者上**：$q_\Delta=1$ 那一支只有 %d 个结构类（%s），$q_\Delta=2$ 那支'
              r'分成 %d 个类（%s），而那一支各类商后的阶都是 %s $\Rightarrow$ 换一个 $\Delta(B-L)=2$ 的'
              r'承载者，残群就换成同阶异型的另一个群——"每通道内部同数"这句话只对**阶**成文。'
              r'与 §9 的对照：完整的残留群恰是 R10 那个 $\mathbb Z_N$ 的**两倍**（%s、%s）'
              r'$\Rightarrow$ 多出来的一半确实是新群元（每行"半单部分非平凡"的存活元有 %d 个以上），'
              r'不是同一个群的另一种写法。' %
              (sum(g['ncar'].values()), g['ncar']['1'], g['ncar']['2'],
               g['ncar']['1'], uni(b['surv'] for b in b1), uni(b['coset'] for b in b1),
               g['ncar']['2'], uni(b['surv'] for b in b2), uni(b['coset'] for b in b2),
               len(gam),
               len(b1), '；'.join(class_tex(b) for b in b1),
               len(b2), '；'.join(class_tex(b) for b in b2),
               uni(b['coset'] for b in b2),
               r'$%s\to%s$' % (mth(ztex(g['nres']['1'])), mth(ztex(2 * g['nres']['1']))),
               r'$%s\to%s$' % (mth(ztex(g['nres']['2'])), mth(ztex(2 * g['nres']['2']))),
               min(r['ss'] for r in rows)), '',
         r'**但它在 §10 那张表上给不出新东西**：%d 条 SM 单态算符（$\dim$ 由 §10 的 Klimyk 计数给出）'
         r'在完整群与在 $\mathbb Z_N$ 下的标的集合相同（%s）、允许集相同（%s），且每一个存活元的相位'
         r'都恒等等于 $t\cdot\sum_k(B-L)_k$（%s）；这两件事不但逐承载者成文，还逐上面那 %d 个结构类'
         r'成文（%s）$\Rightarrow$ §10 的判决一个字都不用改，也不随"选哪个表示去破 $B-L$"而变。'
         '机制是可判的求和，不是修辞（R12.4）：' %
         (g['nsing'],
          '全部相同' if all(r['same_char'] for r in rows) else '**有不相同**',
          '全部相同' if all(r['same_allow'] for r in rows) else '**有不相同**',
          '成立' if all(r['fact'] for r in rows) else '**不成立**',
          len(bys),
          '全部成立' if all(b['same'] for b in bys) else '**有类不成立**'), '',
         r'| 算符（场内容类） | $\sum_k(B-L)_k$ | $\sum_k l_L$ | $\sum_k l_R$ | $\sum_k(p_k+2q_k)$ |',
         '|---|---|---|---|---|']
    for s in g['sing']:
        L.append('| $%s$ | $%s$ | %d | %d | %d |' %
                 (s['name'], s['bl'], s['lL'], s['lR'], s['tri']))
    L += ['', r'每一行的弱同位旋两个求和都是偶、且 $\sum_k(B-L)_k$ 是**偶整数** $\Rightarrow$ 三个中心'
              r'各自恒等于 1，剩下那半边正是 R11 已经在用的 $\mathbb Z_N$ $\Rightarrow$ '
              r'"要求它是 SM 单态"这一步**已经**把中心那几关过掉了。$\Gamma$ 的对角性在这里第二次'
              r'起作用：末列的色 triality 求和与 $3\sum_k(B-L)_k$ 同余（符号由 R10.4 从数据选定）'
              r'$\Rightarrow$ 色中心连"多出来"的机会都没有。', '',
         '### 11.4 正向对照：判据活着（R12.5）', '',
         r'"同判"这句话必须能区分**真的相同**与**无从谈起** $\Rightarrow$ 把"要是 SM 单态"那一步去掉，'
         '拿 §10 那 %d 个物质场在尺寸 2,3,4 上配成可重多重集（每通道 %s 即 %d 条）重跑同一条判据：' %
         (g['nfv'], '、'.join('$d=%d$ %d 条' % (k, n) for k, n in c1['byk']), g['allc_tot']), '',
         r'| 通道 | 全组合 | $\mathbb Z_N$ 允许 | 完整群允许 | 仅 $\mathbb Z_N$ 允许 | '
         '仅完整群允许 | 单态片里新禁 |', '|---|---|---|---|---|---|---|']
    for c in ctl:
        L.append(r'| $q_\Delta=%s$（$\mathbb Z_%d$）| %d | %d | %d | %d | %d | %d |' %
                 (c['qd'], c['N'], c['all'], c['z'], c['f'], c['onlyz'], c['onlyf'], c['sing_new']))
    L += ['', r'两行的"仅 $\mathbb Z_N$"列非空（%d、%d 条）$\Rightarrow$ 中心那一半**在起决定作用**。'
              r'被禁的那批为什么被禁，也是逐条读出来的：每条的 $\sum_k(B-L)_k$ 都是整数（$\mathbb Z_N$ '
              r'那一关全过：%s），中心三项 $(\mathrm{tri}\bmod 3,\sum_k l_L\bmod 2,\sum_k l_R\bmod 2)$ '
              r'在两通道上各取过 %s，"三项全平价"的条数 $=%d+%d$，而有纯中心（$t=0$）见证元的条数 '
              r'$=%d+%d$ 恰等于被禁总数 $\Rightarrow$ 禁它们的确实是中心那三项，例：%s。'
              r'"仅完整群允许"一列恒为 %d $\Rightarrow$ 完整群只会**更严**，§9/§10 边界里那句'
              r'"禁戒不会变松"到这里是**读数**而不是承诺。最后一列 %d $\Rightarrow$ 变严的那一支'
              '确实整个落在单态片之外——这正是 §10 那 %d 条与 §11.4 那 %d 条的差别所在。'
              r'（另有一条定义层的对账：把"逐陪集代表元试"换成"逐个存活元试"，判据改判的条数 $=%d$。）' %
              (c1['onlyz'], c2['onlyz'],
               '；'.join('$q_\Delta=%s$ %s' % (c['qd'], '过' if c['allint'] else '**有不过**')
                        for c in ctl),
               '；'.join(r'$q_\Delta=%s$：%s' %
                         (c['qd'], '、'.join('$(%d,%d,%d)$' % k for k in c['kinds'])) for c in ctl),
               c1['noncen'], c2['noncen'], c1['pure'], c2['pure'],
               '、'.join('$%s$' % x for x in c1['ex']),
               sum(c['onlyf'] for c in ctl), sum(c['sing_new'] for c in ctl),
               g['nsing'], g['allc_tot'], sum(c['disagree'] for c in ctl)), '',
         '### 11.5 整体形式：在场谱把群钉在 $Spin(10)$ 上（R12.0）', '',
         r'$P/Q\cong\mathbb Z_4$（Cartan 行列式 $=%d$，与 D5 的 $|P/Q|$ 同数）$\Rightarrow$ '
         '$Spin(10)$ 与 $SO(10)$ 之间只有一个非平凡商。在场 %d 个表示各落在哪一个类上，'
         '就是"这个谱容许哪个形式"的答案：' % (g['pQ'], len(forms)), '',
         r'| 表示 | $P/Q$ 类的坐标 | 类的阶 | 在根格里（甲 单根坐标 / 乙 $\varepsilon$ 坐标） | 权重条数 |',
         '|---|---|---|---|---|']
    for f in forms:
        L.append('| %s | $(%s)$ | %d | %s / %s | %d |' %
                 (tex_name(f['rep']), ','.join(f['cls']), f['order'],
                  '是' if f['zeroA'] else '否', '是' if f['zeroB'] else '否', f['nwt']))
    L += ['', r'三层读法：类 0 的是 %s $\Rightarrow$ 纯张量型，**看不见**整体形式（哪个形式都容得下'
              r'它们）；2 阶类的是 %s $\Rightarrow$ 至少要 $SO(10)$；4 阶类的是 %s $\Rightarrow$ '
              r'只有单连通的那个形式容得下。出现的类生成的子群大小 $=%d$ $=|P/Q|$ $\Rightarrow$ '
              r'商不掉任何非平凡中心 $\Rightarrow$ **本模型的在场谱把规范群钉死在 $Spin(10)$ 上**，'
              '"自然界取哪个形式"在这里不是自由参数。"在不在根格里"这一列有两条独立判法'
              r'（甲：最高权的单根坐标全整；乙：$\varepsilon$ 坐标全整且坐标和为偶），逐表示同判 $\Rightarrow$ '
              '那张类表不是坐标变换的自证。' %
              (plain_tex(g['tens']), plain_tex(g['ord2']), plain_tex(g['ord4']), g['ngen']), '',
         '**本节的边界**（不进门禁，故明写）：', '',
         '* 中心元的枚举只用**行标号**（不可约表示的 Dynkin 标号）与 $B-L$，没有逐个展开多重集的'
               r'权重 $\Rightarrow$ 它数的是"哪些中心元在整个在场谱上平凡"，与 §5 的逐权重分支是'
               '两套账；两套账的交叉点已由 R12.0 那两条独立判法承担。'
               + (r' 当年那条"两套账"现已做成读数（§13/R14）：把"对谁平凡"换成逐权重条件后甲账 '
                  r'%d 条、乙账 %d 条（其中 %d 条甲账没有），两套账的形变**按集合相等**（%d 种），'
                  r'三条独立算术路数出的核都是 $|\Gamma|=%d$ 且与本节逐元相等 $\Rightarrow$ 换账'
                  r'不换群；本节这条边界因此关掉，判决不变。'
                  % (G14['nspec'], G14['ncond'], G14['novel'], G14['charA'], G14['gam'])
                  if G14.get('nspec') else ''),
         r'* 422 一侧的 $\Gamma$ 只有格一条路（`SUB_422` 的单根不是 $A_3$ 链 $\Rightarrow$ triality '
               '公式不能直接代），故本层不宣称那里有第二条出处。',
         r'* 存活群的"结构"一列读的是阶分布；那 %d 个结构类各自定名（%s），名字来自"穷举该阶上全部'
               r'阿贝尔群、比对元素阶多重集"那一步（阿贝尔由构造：四个因子都是阿贝尔群的商），'
               r'没有第四个独立读数。' %
               (len(bys), '；'.join(r'$q_\Delta=%s$：%s（%d 个承载者）' %
                                    (b['qd'], ab_tex(b['struct']), b['n']) for b in bys)),
         '* 整体形式钉在 $Spin(10)$ 上，与"链探针声明的标量谱里有没有 $16_H/144_H$"是两件事：'
               r'本节用的是**在场**表示集（$\dim\le%d$ 那 %d 个），不是链上的谱 $\Rightarrow$ '
               '若只取链探针字面声明的谱，$P/Q$ 类会换成那一支的读数（与 §9/R10.10、§10/R11.10 '
               r'同一条条件性 $\Rightarrow$ 本节不引入新的条件判决，也不改动它们的）。'
               % (g['maxdim'], g['nrep']),
         '* 本节回答的是 §16 那条边界（完整残留群含整体形式），**不**回答 L10：耦合统一仍缺二环跑动'
               r'与阈值修正 $\Rightarrow$ **L10 未关闭**。', '']
    return L


def perweight_section():
    r"""报告 §13：行标号账与逐权重账的交叉（R14 层）。

    全部读数取自 G14（`run_perweight_layer` 的产出），本节不重算任何东西。
    """
    g = G14
    if not (g.get('name_rows') and g.get('grid') and g.get('core')):
        return ['', '## 13. 行标号账与逐权重账（R14）', '', '本层未跑通 ⇒ 不印任何读数。', '']
    L = ['', '## 13. 行标号账与逐权重账（R14）', '',
         '§11 的边界里写着："中心元的枚举只用**行标号**与 $B-L$，没有逐个展开多重集的权重 '
         r'$\Rightarrow$ 它与 §5 的逐权重分支是两套账。"本节去把这句话兑成读数：同一批候选中心元、'
         '同一个相位公式，把"对谁平凡"从行标号条件换成**逐权重**条件（标签由 `ipp` 现投影到 3221 '
         '的单根、$B-L$ 由 `chg` 现点积，与 `branching` 的 Klimyk 交错和互不共享算术），然后问'
         '两套账给的**形变**（一条条件即 $C\\to\\mathbb Q/\\mathbb Z$ 的一个特征标）是不是同一批。'
         '本节不引入新的李论输入，也不改动 §11 的任何判决。', '',
         '### 13.1 两套账的对象数（R14.1）', '',
         '| 记法 | 对象 | 条数 | 形变种数 |', '|---|---|---|---|',
         '| 甲 分支行（未去重） | $\\dim\\le%d$ 在场 %d 个表示 ↓3221 | %d | %d |' %
         (g['maxdim'], g['nrep'], g['nrow_all'], g['charA']),
         '| 甲 行标号条件 | $(p,q,l_L,l_R)_{B-L}$ 去重 | %d | %d |' % (g['nspec'], g['charA']),
         '| 乙 逐权重 | %d 个子多重态内的权重（按子多重态去重 %d 条、按重数 %d 条、含行重数 %d 条） '
         '| %d（逐表示去重） | %d |' %
         (g['nsub'], g['ndwt'], g['nwtm'], g['nwtmn'], g['nwt'], g['charB']),
         '| 乙 逐权重条件 | 去掉重数与跨表示的重复 | %d（其中 %d 条甲账没有） | %d |' %
         (g['ncond'], g['novel'], g['charB']),
         '',
         '两套账的形变**按集合相等**：乙独有 %d 种、甲独有 %d 种，且 %d/%d 个表示各自的两套账也'
         '集合相等 $\\Rightarrow$ 逐权重那本多出来的 %d 条条件一条也没产生新的特征标 $\\Rightarrow$ '
         '§11 那条"两套账"的边界关掉：同一批 %d 个特征标的两种记法，不是两本会给出不同答案的账。'
         % (g['onlyB'], g['onlyA'], g['eq_per_name'], g['nrep'], g['novel'], g['charA']), '',
         '| 表示 | 维数 | 子多重态 | 不同权重 | 按重数（不含行重数） | 按重数（含行重数） |'
         ' 对账 | 行条件 | 行形变 | 权重形变 | 两套账相等 |',
         '|---|---|---|---|---|---|---|---|---|---|---|']
    for r in g['name_rows']:
        L.append('| %s | %d | %d | %d | %d | %d | %s | %d | %d | %d | %s |' %
                 (tex_name(r['rep']), r['dim'], r['nsub'], r['nwt'], r['nwtm'], r['nwtmn'],
                  '是' if r['nwtmn'] == r['dim'] else '**否**',
                  r['nrow'], r['chaR'], r['chaW'], '是' if r['eq'] else '**否**'))
    L += ['', '### 13.2 子多重态内部的三件恒等事与多重集对账（R14.2）', '',
          '一条 3221 子多重态内部，下面三件事必须恒定，而三条判法走三条互不共享的算术：'
          r'$B-L$ 用 `chg` 逐权重点积；Dynkin 标签之差用 3221 半单 Cartan 的逆矩阵判"在不在'
          r'根格里"（$|\det|=%d$，逆矩阵当场验成双向逆）；中心相位在四个生成元上逐条比对。'
          '读数（%d 个子多重态、按子多重态去重 %d 条权重）：违例 %d / %d / %d $\\Rightarrow$ '
          '三条同时为零 $\\Rightarrow$ "中心元在一条子多重态上作用为标量"是从权重格算出来的，'
          '不是行标号表的定义重述。上一条的逐表示表里那一列"按重数（不含行重数）"对若干表示小于'
          '维数（合计 %d 对 %d），因为分支行本身带重数 $n$；把 $n$ 乘回去就对上了'
          '（合计 %d 对 %d，逐表示全对，见上表"对账"列）$\\Rightarrow$ 乙账展开的确是母表示的权重'
          '多重集。行重数只影响哪几个表示需要乘 $n$：%s。' %
          (g['detA3'], g['nsub'], g['ndwt'], g['bl_mis'], g['root_mis'], g['ph_mis'],
           g['nwtm'], g['dimsum'], g['nwtmn'], g['dimsum'], '、'.join(g['reps_n'])), '',
          '### 13.3 核与 $\\Gamma$：三条路、两种约定（R14.0/R14.3）', '',
          '| 路数 | triality 约定甲 A | triality 约定乙 B |', '|---|---|---|',
          '| 甲 行标号条件（R12.1 原路） | %d | %d |' % (g['gamA'], g['gamB']),
          '| 乙 逐权重条件（本层新增） | %d | %d |' % (g['wtA'], g['wtB']),
          '| 丙 形变反读整格（不碰 `cen_phase`） | %d | %d |' %
          (g['gamMaskA'], g['gamMaskB']),
          '',
          '三条路 + 两种 triality 约定 $\\Rightarrow$ 都是 %d 个，且与 §11 的 $\\Gamma$'
          '（%d 个）**逐元**相等（同一个集合，不是另一个数）$\\Rightarrow$ 换账不换群。'
          '形变那套坐标用得正当，靠的是 R14.0 在同一次运行里验掉的同态引理：%d 组'
          '(群元, 条件) 上"由四个生成元反读"与 `cen_phase` 原读法逐组比对，违例 %d。'
          '而 %d 种形变在逐点加法下有 %d 对之和落在集合外 $\\Rightarrow$ 它们**不是**对偶群的'
          '子群，只是荷表在中心格上的像。' %
          (g['gam'], g['gam_r12'], g['hom_pairs'], g['hom_bad'], g['charA'], g['add_out']), '',
          '### 13.4 冗余度：钉住核要几条（R14.4）', '',
          '| 条件集 | 核的大小 |', '|---|---|',
          '| 全部 %d 条 | %d |' % (g['nspec'], g['gam']),
          '| 单条最好的一条 | %d |' % g['one_min'],
          '| 贪心核心 %d 条 | %d |' % (g['core_len'], g['gam']),
          '| 只要求半单部分平凡 | %d |' % g['Gs'],
          '| 只要求 $U(1)_{B-L}$ 半边平凡 | %d |' % g['Gu'],
          '| 两半之交 | %d |' % g['Gint'],
          '',
          '"删一条就让核变大"的条件 %d 条 $\\Rightarrow$ 严重超定；单条最多把核从 %d 收到 %d；'
          '贪心规则（每步取使核最小的一条，并列按标签与 $B-L$ 的字典序）%d 步到位、到位后每删'
          '一条即变大。但**核心不唯一**：两条即钉住的条件对共 %d 对（占 %d 对的 %.1f%%），涉及'
          '全部 %d 个在场表示，而贪心选出的那两条只挂在 %d 个表示上（%s）$\\Rightarrow$ "哪两条"'
          '是算法的产物、"两条就够"才是读数。' %
          (g['ess'], g['ncand'], g['one_min'], g['core_len'], g['pairs'], g['pairs_tot'],
           100.0 * g['pairs'] / g['pairs_tot'], len(g['pair_reps']), len(g['core_reps']),
           '、'.join('$%s$' % x for x in g['core_reps'])), '',
          '核心两条（形变坐标下的代表条件）：%s' %
          '；'.join('$%s_{%s}$（属于 %s）' %
                    ('(%s)' % ','.join(k[0]), k[1], '、'.join('$%s$' % x for x in k[2]))
                    for k in g['core']), '',
          '### 13.5 $t$ 的网格步长不是判据的一部分（R14.5/R14.6）', '',
          '| $t$ 步长 | 候选元数 | 甲账核 | 乙账核 | 旧核嵌入 |', '|---|---|---|---|---|']
    for d in g['grid']:
        L.append('| $1/%d$ | %d | %d | %d | %s |' %
                 (d['den'], d['ncand'], d['kA'], d['kB'], '是' if d['embed'] else '**否**'))
    L += ['', '四档步长跨 %d 倍分辨率 $\\Rightarrow$ 核恒为 %d 个、且每档都包含 $1/%d$ 那一档的核 '
              r'$\Rightarrow$ 核既不随网格加密变小、也不随粗化变大。把相位拆成两半各自要求平凡'
              '是另一条对照：只半单 %d 个、只 $U(1)_{B-L}$ %d 个、两半都要求 %d 个，而**两半之交'
              '只剩单位元 %d 个**——比 $\Gamma$ 还小 $\\Rightarrow$ $\Gamma$ 内除单位元外那 %d 个'
              '元在两半上都非平凡，靠两项**逐条互相抵消**才活下来 $\\Rightarrow$ §11 那句"中心与 '
              r'$U(1)$ 的对角粘合"从此是一个计数读数。存活元实际只用 $t$ 的分母 %s。' %
              (g['grid'][-1]['ncand'] // g['grid'][0]['ncand'], g['gam'], CEN_T_DEN, g['Gs'],
               g['Gu'], g['gam'], g['Gint'], g['diag'],
               '、'.join(str(x) for x in g['tden'])), '',
          '**本节的边界**（不进门禁，故明写）', '',
          r'* 重数不进判定：相位是权重的标量函数，把一条条件按重数（本层合计 %d 条权重）重复计入'
          r'不改变任何一次判定 $\Rightarrow$ 重数只出现在 R14.2 那条多重集对账里；本节因此是'
          '**跨实现的对账**（与 R13.1 的甲乙两路同族），不是新发现；它关掉的是"两套账"这条边界，'
          '不动任何物理判断。' % g['nwtm'],
          '* 形变集合在逐点加法下不封闭（%d 对之和在集合外）$\\Rightarrow$ 本节不称它是某个'
          '对偶群的子群；%d 这个数是荷表的像的大小，不是群论不变量。' % (g['add_out'], g['charA']),
          '* 贪心核心依赖那条并列规则（标签、$B-L$ 字典序）$\\Rightarrow$ 换一条并列规则就换'
          '一对代表元；本层因此只钉"两条就够"与"多少对够用"，不钉"哪两条"。',
          '* 本节回答的是 §16 那条"两套账"边界，**不**回答 L10：耦合统一仍缺二环跑动与阈值'
          '修正 $\\Rightarrow$ **L10 未关闭**；本节也不引入新的条件判决，§9/§10/§11/§12 那条'
          '"允许要读成若相应标量取期望值"的条件性原样下来。', '']
    return L


def basis_section():
    r"""报告 §14：算符基的覆盖面——共轭场、导数与 d>6（R15 层）。

    全部读数取自 `BASIS`（`run_basis_layer` 的产出），本节不重算任何东西。
    """
    B = BASIS
    if not (B.get('alpha') and B.get('cls') and B.get('collide') and B.get('cover')):
        return ['', '## 14. 算符基的覆盖面：共轭场、导数与 d>6（R15）', '',
                '本层未跑通 ⇒ 不印任何读数。', '']
    bs = ['%d,%d' % tuple(b) for b in B['bins']]
    bt = lambda k: '$n_f=%s$、$n_s=%s$' % tuple(k.split(','))
    lab = lambda l: '(%s)' % ','.join(str(v) for v in l)
    fl = lambda lst: '、'.join('$%s$' % n for n in lst)
    dis = lambda d: '、'.join('$%s$：%d' % (k, v) for k, v in sorted(d.items())) or '（无）'
    ys = lambda b: '成立' if b else '**不成立**'
    nlt = sum(1 for a in B['alpha'] if a[5] == 0)
    c0, c1, c2, c3, faithful, namemix = B['collide']
    na, nsc, nsl, used_ok, closed, m1, m2, m3, m4, ncl = B['conj']
    p6 = B['prot6']
    pu = B['prot_upl']
    odd = [k for k in bs if int(k.split(',')[0]) % 2]
    L = ['', '## 14. 算符基的覆盖面：共轭场、导数与 d>6（R15）', '',
         '§10 那台判据吃到的算符基只有一样东西："d=6 的四条物质场分量" $\\Rightarrow$ '
         '[09](../09_已知局限与否定清单.md) 第十二项边界 (iii) 剩下的那半句话（"含导数算符、含共轭场的高维'
         '算符、$\\nu^c$ 以外的轻子数破缺结构均未枚举"）至今没有读数。本节把那份基换成三件事：', '',
         '**(i) 字母表**：从 %d 条分量扩到 %d 条——$16_F$ 的六个分量各带一个共轭字母，其签名由 '
         '$(\\lambda,Y,B-L)\\mapsto(\\lambda^*,-Y,-(B-L))$ 给出，而 $\\overline{16}_F$ 的分量清单由 '
         '§5 的分支规则**独立**展开，两条路在 14.1 当场对账。' % (nlt, len(B['alpha'])), '',
         '**(ii) 档**：从单档扩到六档，$(n_f,n_s)$ 取 %s，即双线性一直到"两费米子 $+$ 两标量"，'
         '另含"四费米子 $+$ 一标量"（14.2）。' % '、'.join('$(%s)$' % k for k in bs), '',
         '**(iii) 洛伦兹指标账**：每个字母带一个 $SU(2)_C$ 指标（点号字母带带点指标），玻色块 '
         '$\\varphi$、$\\partial$、$F_{\\alpha\\beta}$、$\\bar F$ 各带自己的指标 $\\Rightarrow$ '
         '"能不能缩成洛伦兹标符"成为一个可数的问题，而**真实维数**是 '
         '$d_{\\min}=\\tfrac32 n_f+n_s+k_{\\min}$（14.4）。', '',
         '本节不改动 §10/§11/§12/§13 的任何判决：那张判决表在 §10，本节要回答的是"它覆盖了多少算符"，'
         '不是"它对不对"。', '',
         '### 14.1 字母表与它的拷贝账（R15.0）', '',
         '| 字母 | $\\lambda$ | $Y$ | $B-L$ | $3(B-L)$ | 点号 |',
         '|---|---|---|---|---|---|']
    for (nm, lam, y, bl, three, dt) in B['alpha']:
        L.append('| $%s$ | $%s$ | $%s$ | $%s$ | %s | %d |'
                 % (nm, lab(lam), y, bl, three, dt))
    L += ['', '12 个字母不是拼出来的：它们的权重多重集与 $16_F\\oplus\\overline{16}_F$ **严格相等**'
              '（%d 条对 %d 条，多重集相等而不只是维数相加）$\\Rightarrow$ "共轭场就是 $\\overline{16}_F$ '
              '的分量"这一句现在是量出来的；共轭作用两次回到自己 %s；共轭配对 %d 对逐对落在'
              '$(\\lambda,Y,B-L)\\mapsto(\\lambda^*,-Y,-(B-L))$ 上；12 条字母的 $3(B-L)$ 全是奇整数 '
              '$\\Rightarrow$ §9/§10 那条"物质字称 $=(-1)^{\\text{费米子数}}$"从 6 个字母扩到 12 个仍然'
              '成立。' % (B['part'][0], B['part'][1], ys(B['involution']), len(B['bl_conj'])), '',
          '**拷贝账要明说**：`sm_fields` 给的是 $(\\lambda,Y,B-L)$ **种类**清单，不是权重多重集 '
          '$\\Rightarrow$ 下面"按种类加权"一列一般不等于母表示维数，差额的两处出处就是末两列。', '',
          '| 表示 | 种类条数 | 按种类加权 | 母表示维数 | 重复签名 | 行重数缺口 |',
          '|---|---|---|---|---|---|']
    for g in B['gaps']:
        L.append('| %s | %d | %d | %d | %d | %d |' % (tex_name(g[0]), g[1], g[2], g[3], g[4], g[5]))
    clean = [g[0] for g in B['gaps'] if not g[4] and not g[5]]
    dup = [(g[0], g[4]) for g in B['gaps'] if g[4]]
    miss = [(g[0], g[5]) for g in B['gaps'] if g[5]]
    L += ['', '两列都干净的是 %s；有重复签名的是 %s；因 3221 行重数 $n>1$ 少权重的是 %s '
              '$\\Rightarrow$ 本节凡按"类"计数的数只依赖签名（14.2 的 (丙) 逐组核对到位），而**按拷贝'
              '加权**的结构总数只在纯费米子三档上与特征标路线核对。' %
              (plain_tex(clean),
               '、'.join('%s %d 条' % (tex_name(n), c) for n, c in dup),
               '、'.join('%s %d 条' % (tex_name(n), c) for n, c in miss)), '',
         '### 14.2 六档枚举与两台复核机器（R15.1）', '',
         '两种"类"的口径先钉住：**位置类**按字母表/标量池里的**位置**多重集枚举（同一个 '
         '$(\\lambda,Y,B-L)$ 挂在 $45_H$ 的两行上算两类），**签名类**按签名多重集去重。下表两列都印，'
         '是为了让下面那条碰撞读数有对照。', '',
         '| 档 | 位置类 | 签名类 | 按拷贝的结构数 |', '|---|---|---|---|']
    for k in bs:
        L.append('| %s | %d | %d | %d |' % (bt(k), B['pos'][k], B['cls'][k], B['struct'][k]))
    L += ['', '合计 位置类 %d 条 $\\to$ 签名类 %d 条，差 %d 条、集中在 %d 个键上，全部来自标量池里那'
              '几处重复签名（14.1 末两列的另一半后果）。碰撞组里两条的**场名字**确实不同的有 %d 组，'
              '但组内的**全部物理读数**（荷账、$3Q$、维数、$n_u/n_d$、$k_{\\min}$、单态数、三条判决）'
              '逐项相同 %s $\\Rightarrow$ 取签名类的代表元是无损的、拷贝编号不参与任何判定；纯费米子'
              '三档无碰撞（位置类 $=$ 签名类）$\\Rightarrow$ 末列那条按拷贝加权的总数只在它们上面对。'
              % (c0, c1, c2, c3, namemix, ys(faithful)), '',
          '**(甲) 预筛不漏**：把阿贝尔预筛（$\\sum Y=0$ 且 $\\sum_k(p_k-q_k)\\equiv0\\pmod3$）整条'
          '去掉、对全部组合现算 Klimyk 单态数 $\\Rightarrow$ 类集合与预筛版逐个相等。', '',
          '| 档 | 预筛位置类 | 预筛签名类 | 全枚举位置类 | 全枚举签名类 | 类集合 |',
          '|---|---|---|---|---|---|']
    for f in B['full']:
        L.append('| $(n_f,n_s)=(%d,%d)$ | %d | %d | %d | %d | %s |'
                 % (f[0], f[1], f[2], f[3], f[4], f[5], '相等' if f[6] else '**不等**'))
    L += ['', '四档逐条相等、双向差集都是 0 条 $\\Rightarrow$ 预筛不漏。注意这条是**实测**、不是定理，'
              '且只覆盖本节跑得动全枚举的四档：$(n_f,n_s)$ 取 $(2,2)$ 与 $(4,1)$ 的那两档组合数是六档里'
              '最大的两档，没有做全枚举 $\\Rightarrow$ 这两档的预筛只有旁证（同一预筛在相邻四档上零漏）。',
         '',
         '**(乙) 两条分类路线同数**：把每条类的单态数乘上它自身的排列权重、按档求和，与"先把字母表'
         '的权重多重集连乘 $n$ 次、再一次投影到平凡表示"的路线对照。', '',
         '| $n_f$ | 逐类结构总数 | 整乘积投影单态数 | 相等 |', '|---|---|---|---|']
    for r in B['route']:
        L.append('| %d | %d | %d | %s |' % (r[0], r[1], r[2], '是' if r[3] else '**否**'))
    L += ['', '三个纯费米子档同数 $\\Rightarrow$ "按场内容分类"与"按特征标分类"在**含共轭字母**的字母'
              '表上仍是同一件事；这一步把 §5 的 Klimyk 路线与 §7/§8 的荷账路线接到同一批对象上，'
              '接入点是六档中的 $(2,0)$、$(3,0)$、$(4,0)$ 三档。', '']
    L += ['', '### 14.3 共轭半边带来新东西了吗（R15.2）', '',
          '先把 §10 那本账保住：$d=6$ 档（两列 $(n_f,n_s)=(4,0)$）现在给出 %d 条签名类、%d 个单态'
          '结构；其中只取**非点号**字母的那 %d 条与 §10 的 %d 条**集合相等** %s $\\Rightarrow$ 扩基是'
          '**超集**、不是替换，§10 那张判决表一个数也不用改。' %
          (B['cls']['4,0'], B['struct']['4,0'], B['und_only'][0], len(SEL['hit4']),
           ys(B['und_only'][1])), '',
          '共轭半边带来新东西了吗？没有 $\\Rightarrow$ 它在类集上是一个**对合**：字母表的 %d 个签名与'
          '在场标量池的 %d 个签名合成 %d 个，而全部 %d 条类真正用到的清单恰好就是这一份（%s）；'
          '这 %d 个签名在那条映射下封闭、且作用两次回到自己（%s）。把映射作用到类集上，四处对照'
          '全部归零：像不在类集里 %d 条、$3Q$ 不反号 %d 条、$(n_u,n_d)$ 不互换 %d 条、两条通道的判决'
          '改变 %d 条 $\\Rightarrow$ 点号字母给出的类恰是非点号类的**电荷翻转孪生**（只取点号字母的 '
          '$d=6$ 类 %d 条，与只取非点号的那 %d 条一样多）。' %
          (na, nsc, nsl, ncl, '相符' if used_ok else '**不相符**', nsl, ys(closed),
           m1, m2, m3, m4, B['dot_only'], B['und_only'][0]), '',
          '质子那一列在扩基下重数：$d=6$ 的类里 $\\Delta B\\ne0$ 且 $\\Delta L\\ne0$ 的有 %d 条'
          '（其中 $\\Delta(B-L)=0$ 的 %d 条），判禁 %d 条 $\\Rightarrow$ §10 那句"残留群不保质子"不是'
          '"字母表太小"的产物。' % (p6[0], p6[1], p6[2]), '',
          '| 场内容 | $3Q$ | $\\Delta B$ | $\\Delta L$ |', '|---|---|---|---|']
    for r in p6[3]:
        L.append('| %s | %s | %s | %s |' % (fl(r[0]), r[1], r[2], r[3]))
    L += ['', '（样本 %d 条，取自那 %d 条的前面；判决列不在这里印，因为 %d 条**全部**允许。）' %
          (len(p6[3]), p6[0], p6[0]), '',
          '### 14.4 导数账：绝对禁与上移是两件事（R15.3）', '',
          '洛伦兹账用三条互不共享算术的实现各数一次。**(甲)** 奇偶判据：能缩成洛伦兹标符 '
          '$\\iff n_u\\equiv n_d\\pmod2$，且此时 $k_{\\min}\\equiv n_u$；**(乙)** 把每个字母当成 '
          '$(\\tfrac12,0)$ 或 $(0,\\tfrac12)$、每个 $\\partial$ 当成 $(\\tfrac12,\\tfrac12)$，用 '
          '$j$-加法三角形递推数 $(\\tfrac12)^{\\otimes n}$ 里自旋 0 的重数（$n=0\\dots7$ 的读数 %s），'
          '再对 $k=0\\dots8$ 搜索；**(丙)** 四类玻色块对 $n_u-n_d$ 奇偶的改动（幂次 $\\le3$）逐块数过'
          '（下表）。三台机器的违例 %d / %d 条 $\\Rightarrow$ 下面那条二分不是约定，是数出来的。'
          % ('、'.join(str(v) for v in B['cg']), B['parity'][0], B['parity'][1]), '',
          '| 玻色块 | $(u,d)$ 指标 | 对 $n_u-n_d$ 奇偶的改动 |', '|---|---|---|']
    for k, v in sorted(B['blocks'].items()):
        L.append('| %s | $(%s)$ | %s |' % (k, ','.join(str(x) for x in v),
                                           '不变' if (v[0] - v[1]) % 2 == 0 else '**翻转**'))
    L += ['', '两件事由此分开：**绝对禁** $=$ 奇费米子数（$n_u-n_d$ 的奇偶与玻色块无关 $\\Rightarrow$ '
              '加多少导数都救不回来）；**上移** $=$ 偶费米子数但 $n_u$ 为奇（要一个导数，真实维数 '
              '$+1$）。逐档读数：', '',
          '| 档 | 签名类 | 绝对禁 | 上移 | 零导数 | 奇费米子数 |', '|---|---|---|---|---|---|']
    for k in bs:
        L.append('| %s | %d | %d | %d | %d | %d |' % ((bt(k),) + tuple(pu[k])))
    tp = sum(pu[k][1] for k in bs)
    tu = sum(pu[k][2] for k in bs)
    t0 = sum(pu[k][3] for k in bs)
    L += ['', '全档 $=$ 绝对禁 $+$ 上移 $+$ 零导数：%d $=$ %d $+$ %d $+$ %d（签名类总数 %d）。'
              '绝对禁**恰好**落在 $n_f$ 为奇的那些档：%s $\\Rightarrow$ 该些档合计类数 %d 条、其中奇'
              '费米子数 %d 条、全部判禁 $\\Rightarrow$ "三费米子算符"这一整类在洛伦兹层就被禁掉，与荷账'
              '无关；其余 %d 条类里 %d 条要一个导数才成为洛伦兹标符 $\\Rightarrow$ "高维"里的维数差是'
              '数出来的，不是猜的。' %
              (c1, tp, tu, t0, c1, '、'.join(bt(k) for k in odd),
               sum(B['cls'][k] for k in odd), sum(pu[k][4] for k in odd), c1 - tp, tu), '',
          '双线性档是唯一能一眼看完的一档（%d 条）：' % len(B['bilin']), '',
          '| 场内容 | $n_u$ | $n_d$ | $k_{\\min}$ | $d_{\\min}$ | $3Q$ | $\\Delta B$ | '
          '$\\Delta L$ | 单态数 |', '|---|---|---|---|---|---|---|---|---|']
    d3 = [b for b in B['bilin'] if b[4] == '3']
    d4 = [b for b in B['bilin'] if b[4] == '4']
    for b in B['bilin']:
        L.append('| %s | %d | %d | %d | %s | %s | %s | %s | %d |'
                 % (fl(b[0]), b[1], b[2], b[3], b[4], b[5], b[6], b[7], b[8]))
    L += ['', '%d 条要一个导数（$d_{\\min}=4$，就是动能项 $\\psi^\\dagger\\partial\\psi$，且 '
              '$\\Delta B=\\Delta L=0$）、%d 条零导数（$d_{\\min}=3$，即 %s，$\\Delta L=\\mp2$）'
              '$\\Rightarrow$ "可重整的质量项只有右手中微子那一条"现在是引擎自己重推出来的，不再是'
              '引用的常识。' % (len(d4), len(d3), '、'.join('$%s$' % '+'.join(b[0]) for b in d3)), '',
          '### 14.5 指标账与荷账：那条巧合挂在哪份谱上（R15.4）', '',
          '把"指标禁"（洛伦兹账给不出 $k_{\\min}$，就是上一节的"绝对禁"）与"群禁"（§10 的同余式判禁）'
          '当成两个集合摆在一起。六档全基、在场标量谱取链探针字面声明的那一份 $\\Rightarrow$ 指标禁 %d 条、'
          '群禁 %d 条，**集合相等** %s $\\Rightarrow$ 在这个字母表上，残留群的 $\\mathbb{Z}_2$ 半边**不带来**'
          '洛伦兹费米子字称之外的信息（$\\mathbb{Z}_3$ 半边早已被"要是 SM 单态"那一步吃掉，§10 '
          'R11.8）。逐档看：' % (B['coin'][0], B['coin'][1], ys(B['coin'][2])), '',
          '| 档 | 签名类 | 绝对禁 | 群禁 |', '|---|---|---|---|']
    for k in bs:
        L.append('| %s | %d | %d | %d |' % ((bt(k),) + tuple(B['coin'][3][k])))
    nz = [k for k in bs if B['coin'][3][k][1]]
    L += ['', '两本账里非零的只有 %s 这一档，其余 %d 档两本账同时是空集 $\\Rightarrow$ "成对"在那里是'
              '平凡的，整条巧合只由这一档承担。而这条巧合是**条件'
              '读数**，条件就是标量谱：往池里插入别的 Higgs 表示、只跑单标量三档（$n_s=1$，即 %s），'
              '对照组如下。' % ('、'.join(bt(k) for k in nz), len(bs) - len(nz),
                                '、'.join('$(%d,%d)$' % tuple(b) for b in BST_CTL)), '',
          '| 标量谱 | 池大小 | 类数 | 指标禁 | 群禁 | 只指标禁 | 只群禁 | 该谱含奇 $3(B-L)$ |',
          '|---|---|---|---|---|---|---|---|']
    for c in B['ctl']:
        L.append('| %s | %d | %d | %d | %d | %d | %d | %s |' %
                 (c['tag'], c['pool'], c['cls'], c['lk'], c['zf'], c['onlyL'], c['onlyZ'],
                  '是' if c['odd'] else '否'))
    L += ['', '巧合在**偶** $3(B-L)$ 的插入下保持（补 $126_H+\\overline{126}_H$ 一条也不改判、两边仍'
              '各 %d 条），在**奇**的插入下**双向**分叉（$+144_H$：%d 条对 %d 条，各方向独有 %d/%d 条；'
              '$+16_H$：%d 条对 %d 条，独有 %d/%d 条）。机理不是修辞，是一条集合等式：$+144_H$ 那池里'
              '"群禁不住而指标禁"的那批，与"标量半边 $\\sum3(B-L)$ 为奇"的那批 %s；样本（场内容, '
              '$3Q$）：' % (B['ctl'][1]['lk'], B['ctl'][2]['lk'], B['ctl'][2]['zf'],
                           B['ctl'][2]['onlyL'], B['ctl'][2]['onlyZ'],
                           B['ctl'][3]['lk'], B['ctl'][3]['zf'],
                           B['ctl'][3]['onlyL'], B['ctl'][3]['onlyZ'],
                           '相等' if B['ctl'][2]['mech'] else '**不等**'), '',
          '| 场内容 | $3Q$ |', '|---|---|']
    for r in B['w144']:
        L.append('| %s | %s |' % (fl(r[0]), r[1]))
    L += ['', '谁奇谁偶也是读数：在场 %d 个表示里含奇 $3(B-L)$ 分量的只有 %s，且这份清单与 R10.3 在 '
              'SO(10) **权重**层数出的那份例外清单不一致 %d 条 $\\Rightarrow$ "残留群 $=$ 物质字称"这句'
              '话的可信度挂在标量谱上，而不是挂在群论上。' %
              (len(B['gaps']), '、'.join(tex_name(n) for n in B['oddrep']), len(B['census_mis'])), '',
          '### 14.6 d 大于 6：$\\nu^c$ 以外的轻子数破缺（R15.5）', '',
          '"未枚举"那半句现在是逐档读数：含 SM 单态的签名类里 $\\Delta B=0$ 且 $\\Delta L\\ne0$ 的那批'
          '有多少条、其中有多少条**完全不碰** $\\nu^c$（含其共轭）。', '',
          '| 档 | 签名类 | $\\Delta L\\ne0$ | 其中不碰 $\\nu^c$ | $\\Delta L$ 分布 |',
          '|---|---|---|---|---|']
    for k in bs:
        d = B['dl'][k]
        L.append('| %s | %d | %d | %d | %s |' % (bt(k), d[0], d[1], d[2], dis(d[3])))
    L += ['', '$d=5$ 档 %d 条 $\\Delta L\\ne0$ 里 %d 条**完全不碰** $\\nu^c$，其符号成对（$\\Delta L$ '
              '分布 %s）$\\Rightarrow$ 14.3 那条共轭对合在这里直接可见。具名一条：%s（$3Q=%s$、'
              '$\\Delta L=%s$、单态数 %d、两条通道的判决 %s），它的共轭孪生 %s $\\Rightarrow$ 这就是 '
              'Weinberg 型算符 $LLHH$ 在 SO(10) 权重格上的出处：它不需要 $\\nu^c$、不需要 $126_H$，'
              '在场的 $10_H/45_H$ 就够。反面读数把这条接回 §10：$d=4$ 的三费米子档里 $\\Delta L\\ne0$ '
              '的 %d 条**全部**被洛伦兹账禁掉（%d/%d）$\\Rightarrow$ "轻子数破缺从 $d=5$ 起"不是引文'
              '口径，是本层的 $d_{\\min}$ 读数。' %
              (B['dl']['2,2'][1], B['dl']['2,2'][2], dis(B['dl']['2,2'][3]),
               fl(B['wein'][0]), B['wein'][1], B['wein'][2], B['wein'][3],
               '、'.join('允许' if v else '禁' for v in B['wein'][4]), B['wein'][5],
               B['dl3'][0], B['dl3'][1], B['dl3'][0]), '',
          '不碰 $\\nu^c$ 的 $d=5$ 类样本（清单共 %d 条，这里印前 %d 条）：' %
          (B['dl']['2,2'][2], len(B['nonu'])), '',
          '| 场内容 | $3Q$ | $\\Delta L$ | 单态数 | 判决 |', '|---|---|---|---|---|']
    for r in B['nonu']:
        L.append('| %s | %s | %s | %d | %s |' %
                 (fl(r[0]), r[1], r[2], r[3],
                  '、'.join('允许' if v else '禁' for v in r[4])))
    L += ['', '### 14.7 覆盖面本身登记成数（R15.6）', '',
          '档共 %d 个、签名类合计 %d 条、$d_{\\min}$ 从 %s 一直到 %s $\\Rightarrow$ 六档实际探到 '
          '$d=8$。含点号字母（即共轭场）的类**逐档都在场**，一栏都没有塌到 0 $\\Rightarrow$ "共轭场"'
          '这一半已不再是散文。' % (B['cover'][0], B['cover'][1], B['cover'][2], B['cover'][3]), '',
          '| 档 | 含点号字母的类 | 类数 |', '|---|---|---|']
    for k in bs:
        L.append('| %s | %d | %d |' % (bt(k), B['cover'][4][k], B['cls'][k]))
    # ---- 14.8：类数到缩法重数的差额（R16 层）
    r6, t6 = B['r16'], B['r16tot']
    L += ['', '### 14.8 类数 $\\to$ 缩法重数：Lorentz 那一半的差额（R16.0–R16.2）', '',
          '上一节留下"类数不是算符数"这句话。一类固定的是**自旋指标的多重集**，所以"一类里有几个'
          r'独立 Lorentz 标量"是另一个数：$n$ 个外尔指标接成标量的独立接法数 '
          r'$=\dim(V^{\otimes n})^{SL(2)}$。这台机器有四张互不共享算术的票：甲 $j\pm1$ 三角形递推'
          r'（引擎原有）、乙 二项式差 $\binom{2m}{m}-\binom{2m}{m+1}$、丙 钩长公式 $f^{(m,m)}'
          r'=(2m)!/((m+1)!\,m!)$、丁 **显式**解 $(\sum_i X^{(i)})T=0$（$X=E,F,H$，对角余乘）在 '
          r'$(\mathbb C^2)^{\otimes n}$ 里的不变张量零空间（$\mathbb Q$ 上精确消元，$n\le%d$）。'
          '四路在 $0..%d$ 上逐项相等、违例 %d 条。丁那张票还顺手把"画线法"当作张量写出并数其秩 '
          r'$\Rightarrow$ 缩法重数**不是**配对方案数：$n=4$ 时 %d 个画线法只撑出 %d 个独立缩法，'
          '多出来的 %d 条关系就是 Plücker（Schouten）恒等式，$n=6$ 时是 %d 条。本层用到的指标数'
          '最大只有 %d $\\Rightarrow$ 判据整个落在显式路线够得着的范围内，没有外推。'
          '（表中 $n=0$ 一行按空配对的约定 $(-1)!!=1$。）' %
          (len(r6[9]) - 1, r6[0], len(r6[2]) + len(r6[3]), r6[9][4][3], r6[9][4][4],
           r6[9][4][5], r6[9][6][5], r6[1]), '',
          '| $n$ | 缩法重数（甲＝乙＝丙＝丁） | 画线法 $(n-1)!!$ | 画线法张成空间的秩 | Plücker 关系数 |',
          '|---|---|---|---|---|']
    for row in r6[9]:
        L.append('| %d | %d | %d | %d | %d |' % (row[0], row[1], row[3], row[4], row[5]))
    L += ['', '把这张票挂到类上：一类的缩法重数 $=$ 无点号侧与有点号侧各自接成自旋 $0$ 的重数之积，'
              '两侧各加同一个 $k_{\\min}$ 个指标 $\\Rightarrow$ 每个 $\\partial_{\\alpha\\dot\\alpha}$ '
              '正好两侧各补一个。逐档读数（"可构建类"即 14.3 的甲判据通过率）：', '',
          '| 档 | 可构建类 | 只有 $1$ 条缩法 | 有 $\\ge2$ 条 | $\\max m$ | 缩法总数 |',
          '|---|---|---|---|---|---|']
    for k in bs:
        w = r6[11][k]
        L.append('| %s | %d | %d | %d | %d | %d |' % (bt(k), w[0], w[1], w[2], w[3], w[4]))
    L += ['', '%d 个可构建类共给 %d 条缩法（$\\times%.4f$）$\\Rightarrow$ 按类计数把 Lorentz 口径的'
              '结构空间低估了 %d 条；最大重数就是 %d，因为本层单侧指标数不超过 %d 而 $C_2=2$。'
              '与 §10 的接缝最要紧：$n_f=4$ 的 %d 条 SM 单态 $d=6$ 类**每一条**都是 $2$ 条缩法 '
              '$\\Rightarrow$ "§10 有 8 条算符"要读成 **8 个类 $=%s$ 个 Lorentz 结构**；而全档里 '
              '$d\\le6$ 且多缩法的类恰有 %d 条 $=$ 这 %d 条无点号的加上它们的点号孪生 %d 条 '
              '$\\Rightarrow$ "谁多重"是边界清楚的一批：四个指标全在同一侧。' %
              (r6[8], t6[3], t6[3] / float(r6[8]), t6[3] - r6[8], t6[2], r6[1], len(r6[12]),
               2 * len(r6[12]), t6[4], t6[4] // 2, t6[4] // 2), '',
          '塔的读数（边界 (i) 的前半从此带增长率）：往上走 $2$ 阶缩法总数从 %d 到 %d，再到 %d、%d；'
          '而在 $k=k_{\\min}+2$ 那一层，%d 个可构建类**全部**变成多重缩法 $\\Rightarrow$ 只数最小 '
          '$k_{\\min}$ 是一条**有意的截断**，不是一句"高维大概没有"。' %
              tuple([t6[3]] + [x[1] for x in r6[10][1:]] + [r6[10][1][2]]), '',
          '* 口径警告：$m$ 是**不变张量空间的维数**，不是算符数。$m\\ge2$ 的 %d 类里有 %d 类场内容'
              '含重复名字 $\\Rightarrow$ 五道削减里只有第一道（Fermi 反对称）在 14.9 数成了读数，'
              'Fierz 恒等式的洛伦兹半边在 14.10 数成读数（味半边没做），味指标、EOM 场重定义、全导数塔照常未做。本层据此把本节边界清单里 (ii) '
              '的"Lorentz 收缩的具体形式"那一半变成读数；"数出 $m$ 条"不等于"选定其中哪一条"。'
              % (t6[1], t6[5]), '']
    # ---- 14.9：Fermi 反对称（R17 层）
    r7, fs = B['r17'], B['r17'][17]
    gz = lambda t: '+'.join(str(m) for m in t) or '（无）'
    L += ['', '### 14.9 Fermi 反对称：五道削减里的第一道做成读数（R17.0–R17.4）', '',
          '上一节的口径警告留着"这五道削减本层一道都不做"，本节兑现第一道。同一个外尔场占多个槽位时，'
          '那些槽位上的系数张量必须**完全反对称**（外尔场算符反对易）$\\Rightarrow$ 不反对称的缩法代入'
          '即零。判据 $=$ 在 14.8 的不变张量空间上逐组施加 $A_g=\\sum_{\\sigma\\in S_g}'
          '\\mathrm{sgn}(\\sigma)\\,\\sigma$ 之后数**像的秩**。三张互不共享算术的票：甲 显式投影'
          '（零空间基 $->$ 逐组反对称化 $->$ $\\mathbb Q$ 上行阶梯的秩）；乙 表示论（$m$ 个同名槽位贡献 '
          '$\\Lambda^m(\\mathbb C^2)$，$m=0,1,2$ 给自旋 $0,\\tfrac12,0$，$m\\ge3$ 是零空间，再与其余'
          '单槽做 $j$-耦合数自旋 $0$ 的重数）；丁 Grassmann 直接求值（同名槽共用一对反对易生成元，'
          '把 $T\\mapsto\\mathcal O(T)$ 写出再数秩 $\\Rightarrow$ 排序符号要逐条计逆序数，漏掉符号时 '
          '$\\varepsilon^{\\alpha\\beta}\\psi_\\alpha\\psi_\\beta$ 会读成 0，本层写作时真踩过这一伤）。',
          '', '| $n$ | 同名组大小 | 甲（投影） | 乙（表示论） | 丁（Grassmann） |',
          '|---|---|---|---|---|']
    for row in r7[0]:
        L.append('| %d | %s | %d | %d | %d |' % (row[0], gz(row[1]), row[2], row[3], row[4]))
    L += ['', '全部 %d 个 $(n,\\text{组大小})$ 用例里三路互不等 %d 条；"无重复名字"那一路必须退回 '
              '14.8 的缩法重数（违例 %d 条）$\\Rightarrow$ 这一道削减**只在真有全同场时动手**。'
              '四条教科书锚点（括号内为三路的读数，逐路各算一遍）：两槽同名 $=%s$（'
              '$\\varepsilon^{\\alpha\\beta}\\psi_\\alpha\\psi_\\beta$ 非零）、四槽同名 $=%s$'
              '（单个外尔场只有 2 个分量 $\\Rightarrow\\psi\\psi\\psi\\psi\\equiv0$）、四槽两两同名 '
              '$=%s$（$%d$ 条里活 $%d$ 条）、六槽三对同名 $=%s$（$%d$ 条里活 $%d$ 条）。最后一条在此'
              '前是**手算的先验**（猜 $%d$），被三路一致的读数否掉 $\\Rightarrow$ 判据一旦上格，'
              '"显然"就不再是证据；锚点写进 R17.0 的断言里，往后只能由这条门禁重读。' %
              (len(r7[0]), len(r7[1]), len(r7[2]), r7[3][0], r7[3][1], r7[3][2],
               B['cg'][4], r7[3][2][0], r7[3][3], B['cg'][6], r7[3][3][0], r7[3][3][0] + 1), '',
          '把判据挂到 14.8 的类上：两侧各自按名字分组、各自算秩再相乘 $\\Rightarrow$ 一类过 Fermi 后的'
          '结构数 $a$ 与 14.8 的缩法重数 $m$ 之比就是这一道削减的**价格**。逐档读数（判据覆盖类数、'
          '登记类数、缩法数、存活数、多重缩法类数、含重复名字类数）：', '',
          '| 档 | 判据覆盖类 | 登记类 | 缩法数 | 存活数 | 多重缩法类 | 含重复名字类 |',
          '|---|---|---|---|---|---|---|']
    for k in bs:
        w = r7[13][k]
        L.append('| %s | %d | %d | %d | %d | %d | %d |' % (bt(k), w[0], w[1], w[2], w[3], w[4], w[5]))
    ncov = sum(v[0] for v in r7[13].values())
    L += ['', '$k_{\\min}=0$ 的可构建类共 %d 个、缩法 %d 条，过了反对称化剩 %d 条 $\\Rightarrow$ 这一道'
              '削减吃掉 %d 条（$\\times%.4f$）。分区读数（归零类、缩减类、不变类、含 $\\ge3$ 同名类、'
              '无重复名字类、反而变大类）%s $\\Rightarrow$ 三分区恰好铺满判据覆盖的类减去"看不见"的那批'
              '（%d $+$ %d $+$ %d $=$ %d $-$ %d），而"变大"那一格恒为 0 是**结构**要求（反对称化是同一'
              '空间上的像），不是运气。归零与"同一个名字占满 $\\ge3$ 个槽"是同一批：两侧集合的对称差 '
              '%d 条 $\\Rightarrow$ 除 $\\Lambda^m(\\mathbb C^2)=0$ 之外没有别的归零原因；无重复名字的 '
              '%d 条判据**看不见**（违例 %d 条）。' %
              (ncov, r7[14][0], r7[14][1],
               r7[14][0] - r7[14][1], r7[14][1] / float(r7[14][0]), r7[14],
               # 分区等式右边是**类**总数 ncov，不是缩法条数 r7[14][0]（两者都是 3 位数）
               r7[14][2], r7[14][3], r7[14][4], ncov, r7[14][6], r7[18],
               r7[14][6], len(r7[11])), '',
          '与 §10 的接缝（$n_f=4$、无点号侧那 %d 条 SM 单态 $d=6$ 类，逐类的 $k_{\\min}$ 全为 %s'
          '$\\Rightarrow$ 本层对它们**有管辖权**）：' %
          (len(r7[15]), sorted(set(e[1] for e in r7[15]))), '',
          '| 场内容 | $k_{\\min}$ | 缩法数 $m$ | 同名组（无点号侧、有点号侧） | 存活数 $a$ |',
          '|---|---|---|---|---|']
    for e in r7[15]:
        L.append('| %s | %d | %d | %s、%s | %d |'
                 % (fl(e[0]), e[1], e[2], gz(e[3][0]), gz(e[3][1]), e[4]))
    L += ['', '结构数从 %d 到 %d $\\Rightarrow$ §10 那 8 条 $d=6$ 质子算符类的 Lorentz 口径要按 %d 条'
              '读，不是 %d 条。存活数只依赖名字组大小的多重集（同一多重集上出现两个不同存活数的组 %d 个）'
              '$\\Rightarrow$ "接法几重"由**谁与谁全同**决定，不由槽位编号决定；组到存活数的映射 %s。'
              '归零的两批集合相等：$\\{\\text{存活}=0\\}=%s$，$\\{\\text{某名字}\\ge3\\text{ 槽}\\}=%s$，'
              '而名字最多占两槽的那 %d 条无一归零。' %
              (sum(e[2] for e in r7[15]), sum(e[4] for e in r7[15]), sum(e[4] for e in r7[15]),
               sum(e[2] for e in r7[15]), sum(1 for v in r7[16] if len(v[2]) > 1),
               '、'.join('$%s\\mapsto%s$' % (gz(g[0] + g[1]), v)
                         for g in r7[16] for v in g[2]),
               '、'.join(fl(x) for x in fs[0]), '、'.join(fl(x) for x in fs[1]), len(fs[2])), '',
          '管辖范围也是一个数：%s。' % (
              '$k_{\\min}\\ne0$ 的可构建类 %d 个（缩法 %d 条）在本层**只登记不判定**——导数槽挂在哪个'
              '场，类记录并不携带，反对称化在那一族上不是同一个空间上的自同态；两边相加回到 14.8 的总量 '
              '%d $+$ %d $=$ %d，类数 %d $+$ %d $=$ %d'
              % (sum(v[1] for v in r7[13].values()), B['r16tot'][3] - r7[14][0],
                 r7[14][0], B['r16tot'][3] - r7[14][0], B['r16tot'][3],
                 sum(v[0] for v in r7[13].values()), sum(v[1] for v in r7[13].values()),
                 sum(v[0] for v in r7[13].values()) + sum(v[1] for v in r7[13].values()))), '',
          '* 本节把 Fermi 反对称这一道做成读数，关掉的是 09 第十七项第 5 条那五道削减里的 **Fermi 一道**；'
          '味指标、EOM 场重定义与全总导数塔照常未做；Fierz 恒等式的洛伦兹半边已在 14.10 数成读数（味半边照常未做） $\\Rightarrow$ **类数仍然不是'
          '算符数**，14.8 那句"低估了 %d 条"从此要再乘一个 Fermi 因子。本层不回填任何寿命、'
          '不改 P4／P7 的判据与分级 $\\Rightarrow$ **L10 未关闭**。' % (t6[3] - r6[8]), '']
    L += ['', '**本节的边界**（不进门禁，故明写）', '',
          '* 导数只数到**最小** $k_{\\min}$：$\\partial^k$ 的完整塔没有枚举（14.8 给了它逐层的'
          '缩法总数，因此"往上还有多少"现在是数、不是猜想）；同一个 $d_{\\min}$ 内的多个独立收缩'
          '在 14.8 里已经数成 %d 条差额。场的内容到 $n_f=4$、标量插入到 $n_s=2$ 为止 $\\Rightarrow$ '
          '**类数仍然不是算符数**，本节给的是覆盖面，不是算符清单。' % (B['r16tot'][3] - B['r16'][8]),
          '* 判决仍只过**规范不变**加**洛伦兹指标**这两关（后者见 14.8 的 $m$）：Fierz '
          '恒等式此后只过了洛伦兹半边（14.10，味半边没过），仍未过的三关是味指标、EOM 与全总导数（与 §7/§10 同一处置）。',
          '* 本节所有"在场"都指链探针字面声明的那份谱 %s，而 %s 都不在其中 $\\Rightarrow$ 14.5 那条'
          '巧合是挂在**偶荷**标量谱上的条件读数；$B-L$ 破缺承载者的缺位（R10.10/R11.10）原样下来。'
          % (higgs_tex(B['cover'][5]), higgs_tex(B['cover'][6])),
          '* 拷贝账是引擎级事实：`sm_fields` 给种类清单（14.1 末两列即其后果）$\\Rightarrow$ 按拷贝'
          '加权的结构数只在纯费米子三档与特征标路线核对过，含标量插入的三档那一列只是登记、不参与'
          '任何判定。',
          '* 本节关掉的是 09 第十二项边界 (iii) 的后半（14.1–14.7）与第十六项边界 (i) 的后半、'
          '(ii) 的 Lorentz 半边（14.8）、第十七项第 5 条那五道削减里的 Fermi 一道（14.9）与 Fierz 一道的洛伦兹半边（14.10），'
          '**不**回答 L10：耦合统一仍缺'
          '二环跑动与阈值'
          '修正 $\\Rightarrow$ **L10 未关闭**；本节不回填任何寿命、不改 P4／P7 的判据与分级。', '']
    # ---- 14.10：Fierz 恒等式（R18 层）
    r8 = B['r18']
    L += ['', '### 14.10 Fierz 恒等式：把"换一条道再写回来"做成基变换读数（R18.0–R18.4）', '',
          '14.8 与 14.9 的全部数都只在 $\\varepsilon$ 道里数（同侧指标成对缩掉）。一条 Fierz 恒等式'
          '的**内容**恰是换到另一条道再写回来：矢量（流-流）道把一条 $\\sigma^\\mu_{\\alpha\\dot\\beta}$ '
          '与它的 $\\mu$ 缩并伙伴 $\\sigma_{\\mu\\,\\gamma\\dot\\delta}$ 放在一起，吃一个不点指标加一个点'
          '指标。本节把这条道显式建出来，比的是**两条道各自能否张满同一个** $SL(2)_L\\times SL(2)_R$ '
          '**不变量空间** $\\Rightarrow$ 若两型生成元的秩都等于第四路（特征标递推 $c_{j0}$）的预测，'
          '"缩法只用 $\\varepsilon$ 写"就从挂在 14.8 计数里的**假设**变成一条读数；两型生成元之间的'
          '线性关系条数 $=|$画线$|_\\varepsilon+|$画线$|_\\sigma-$秩就是这道削减在此坐标里可数的内容。'
          '它与 Schouten 不共族：14.8 那条比的是**同为 $\\varepsilon$** 的画线之间的关系，'
          '本节比的是**跨画线类型**。',
          '',
          '约定（显式写出，不当隐藏前提）：$i\\sigma^2$ 取实矩阵 $\\begin{pmatrix}0&-1\\\\1&0\\end{pmatrix}$ '
          '$\\Rightarrow$ 度规号并成 $G=(+1,-1,+1,-1)$；带点侧与不带点侧同用一份 $\\varepsilon$ 矩阵'
          '（与 14.8 两侧同用 $c_{j0}$ 的口径一致）；全程精确分数，无浮点、无模约化。'
          '四张票各自走的算术：$\\varepsilon$ 道秩（14.8 的显式零空间基）、$\\sigma$ 道**单独**秩'
          '（显式 $\\sigma^\\mu$ 分量 $+$ 预计算的传播子）、两型**并秩**、$c_{j0}$ **预测**。',
          '',
          '| $\\nu$ | $\\dot\\nu$ | 挂类数 | 预测 | $\\varepsilon$ 道秩 | $\\sigma$ 道单独秩 | 并秩 |'
          ' $\\varepsilon$ 画线 | $\\sigma$ 去重 | 道间关系 |',
          '|---|---|---|---|---|---|---|---|---|---|']
    for r in r8[0]:
        L.append('| %d | %d | %d | %d | %d | %d | %d | %d | %d | %d |' % tuple(r))
    L += ['', '四数（预测、$\\varepsilon$ 道秩、$\\sigma$ 道单独秩、并秩）**不全等**的表格档 %d 个'
              '$\\Rightarrow$ 在全部 %d 个表格档上，两型道各自都是该不变量'
              '空间的**完备**生成集，且两型的并也不更大（新增结构 %d 条）。两条锚点写进 R18.0 的断言：'
              '$(2,2)$ 档同向 $\\sigma$ 道 $\\div\\varepsilon$ 道 $=%s$、交叉道 $\\div\\varepsilon$ 道 '
              '$=%s$ $\\Rightarrow$ 这就是完备性关系 $\\sigma^\\mu_{\\alpha\\dot\\beta}'
              '\\sigma_{\\mu\\gamma\\dot\\delta}=2\\,\\varepsilon_{\\alpha\\gamma}'
              '\\varepsilon_{\\dot\\beta\\dot\\delta}$（系数与符号都对得上），三条生成元的秩 $=%d$ '
              '$\\Rightarrow$ 其中关系 %d 条；同名场的 Grassmann 括号 $(\\psi\\psi)$ 按基元素展开为 %s'
              '（掩码的第 $g$ 位 $=$ 第 $g$ 个反对易生成元），它必须非零'
              '$\\Rightarrow$ 写作时漏掉一次换序符号就会把它算成 $+1-1=0$，这一伤在 14.9 与本层'
              '都出现过。' %
              (len(r8[1]), r8[17], r8[12], r8[16][0], r8[16][1], r8[16][2], 3 - r8[16][2],
               '、'.join('掩码 %d 的系数 $%s$' % (m, c) for m, c in r8[16][3])), '',
          '这条读数**必须与前置判据同写**。只断言"新增 $=0$"是放过缺陷的：写作时实测把带点侧槽位的'
          '起点写错一档（$\\varepsilon$ 目录跨了手性，于是"画线"根本不是 $SL(2)_L\\times SL(2)_R$ '
          '不变的），$\\varepsilon$ 道秩从 1/2/2/4/5/5 涨到 2/6/5/17/20/14，而"新增"**照样读 0** '
          '$\\Rightarrow$ 保护这条读数的是"目录秩 $=$ 预测"那面前置等式，不是它自己；本层因此把两件事'
          '写进同一条门禁（R18.1）。反向还要核到类上：表格档的预测值与 14.8 逐类登记的缩法重数不符 '
          '%d 条 $\\Rightarrow$ 本节读的是 R16 那张表，不是另起炉灶。' % len(r8[14]), '',
          '第三张**不共族**的票要独立复现 14.9：固定内容，把"哪两个名字缩在一起"的每一道写成 '
          'Grassmann 单项式（同名槽共用一对反对易生成元），数这些单项式的秩。14.9 判定过的 %d 个类上'
          '逐类相乘后合计 %d 条 $=$ 14.9 公布的存活合计 %d 条（逐类不等 %d 类），而道单项式共 %d 条 '
          '$\\Rightarrow$ 换道在此**没有**给出 14.9 之外的结构：Fierz 的洛伦兹半边已经被 14.8 的 '
          'Schouten 关系与 14.9 的反对称化吃干净，本节给出的是"这件事是数出来的"这一层保证。' %
              (r8[5], r8[3], B['r17'][14][1], len(r8[4]), r8[8]), '',
          '摆放不变性也顺带复核：把 14.9 那句"秩只依赖组大小的多重集、不依赖槽位编号"用在'
          '**每一种摆放**上（两侧共 %d 个摆放对，逐摆放各投影一次），违例 %d 类。反向登记一条：'
          '把同一份内容下不同摆放的像空间**求并**会虚高（并成合计 %d 条 $>$ 存活合计 %d 条，虚高的类 '
          '%d 个）$\\Rightarrow$ 那是把不同的槽位空间识别成同一个空间的**构造伪影**，不是新增结构，'
          '所以它不是一张票，只是一条必须写下来的数（把它当票数，就是把"并起来更大"误读成"Fierz 有'
          '增益"）。' % (r8[6], len(r8[7]), r8[18], r8[3], r8[19]), '',
          '管辖范围：**类集上真正出现的 $(\\nu,\\dot\\nu)$ 只有 %s 这 %d 档**，其中两侧皆非空'
          '的只有 $(2,2)$ 一档 $\\Rightarrow$ 本层的换基读数**挂类的**只有那 %d 个类（占 14.9 判定'
          '类数的 $%.4f$），其余 %d 个类是单侧场（$\\sigma$ 线无处可放），其余 %d 个表格档只是算术'
          '复核、不挂在类上 $\\Rightarrow$ 把表格档当类集读数就是虚报覆盖面。' %
              ('、'.join('$(%d,%d)$' % t for t in r8[21]), len(r8[21]), r8[9],
               r8[9] / float(r8[5]), r8[20], r8[17] - len(r8[2])), '',
          '* 本节把五道削减里的 **Fierz 一道（洛伦兹半边）**做成读数，关掉的是 09 第十七项第 5 条'
          '那五道削减里 Fierz 那一道的**洛伦兹半边**：味指标那一半没有 $\\Rightarrow$ 引擎不带味自由度'
          '（R7/R9 的边界文本原样有效），EOM 场重定义与全总导数塔两关照旧，'
          '**类数仍然不是算符数**。本层不回填任何寿命、不改 P4／P7 的判据与分级 $\\Rightarrow$ '
          '**L10 未关闭**。']
    return L


def residual422_section():
    r"""报告 §12：422 链的残留按 $SU(4)$ 权格重做成格上读数（R13 层）。

    全部读数取自 G422（`run_residual422_layer` 的产出），本节不重算任何东西。
    """
    g = G422
    rows, ctl = g.get('rows') or [], g.get('ctl') or []
    if not (rows and ctl and g.get('K') and g.get('mp') and g.get('fv')
            and g.get('classes') and g.get('bys') and g.get('vord_pairs')):
        return ['', '## 12. 422 链的残留离散群（R13）', '',
                '本层未跑通 ⇒ 不印任何读数。', '']
    ninter = sum(1 for c in ctl if c['inter'])
    exc = [c for c in ctl if not c['inter']]
    neutral = [b for b in g['bys'] if tuple(b['struct']) == (2, 2)]
    L = ['', '## 12. 422 链的残留离散群（R13）', '',
         '§9 与 §11 的边界都指向同一件待办：走 422 链时 $B-L$ 不在独立 $U(1)$ 因子里，'
         '它坐在 $SU(4)_c$ 的 Cartan 中，而 `SUB_422` 的单根不是 $A_3$ 链（第三条是 '
         r'$\varepsilon_2+\varepsilon_3$）$\Rightarrow$ triality 公式不能直接代，中心元必须先在那张'
         '权格上**数出来**。本层用同一次计算关掉两条待办，且不引进新的李论输入：中心元改由它在 '
         r'$SU(4)$ 三个基本权上的**特征标** $v=(v_1,v_2,v_3)\in(\mathbb Q/\mathbb Z)^3$ 表示，'
         r'$v=A^{-1}m\;(\mathrm{mod}\;1)$，$m$ 跑协权格 $\mathbb Z^3$；不同的 $m$ 模掉行格给出不同'
         '特征标，特征标 mod 1 相加即群乘法 ⇒ 有限枚举、无 BFS，"商掉行格"是内置的。', '',
         '### 12.1 色块格与中心类（R13.0）', '',
         r'Cartan 由块单根现算：%s，$|\det|=%d$、Smith 不变因子 %s $\Rightarrow$ 协权格商行格给 '
         '%d 个类；类乘法即特征标 mod 1 加法：' % (g['A'], g['det'], g['snf'], g['ncls']), '',
         '| 类（特征标 $v$ mod 1） | 协格典范代表 $m$ | 阶 |', '|---|---|---|']
    for i, v in enumerate(g['classes']):
        L.append('| $(%s)$ | $(%s)$ | %d |' %
                 (', '.join(v), ', '.join(map(str, g['canon'][i])), g['vord_pairs'][i]))
    L += ['', '全候选群 = 类 × 两个弱 $\\mathbb Z_2$，共 %d 个元，对特征标加法封闭；元素阶多重集 %s '
              '交给"穷举该阶上全部阿贝尔群、比对元素阶多重集"那一步，唯一命中 %s（ab 标准序升幂）'
              r'$\Rightarrow$ 中心就是色 $\mathbb Z_4$ 与两个弱 $\mathbb Z_2$ 的直积。'
              '同一张 16 列荷表三条算术路：甲 行标号（`branching` 直给）、乙 逐权重（`ipp` 现投影到'
              '块单根）：甲 vs 乙错 %d 条、行标号 vs 逐权重错 %d 条（在场 %d 行全对）；'
              r'丙 标准 triality 号 $q_{\rm std}=c+2a+3b$（槽位映射）对方格读数 $q_{\rm lat}$'
              r'（甲表里 4 阶元特征标 $4v=%s$）：全部行上满足 $q_{\rm lat}\equiv 3q_{\rm std}'
              r'\pmod 4$，且该同余在 $[0,4)^3$ 上恒成立；取 $s=1$ 的违例行去重后与 '
              r'$b\equiv c\pmod 2$ 的预测集合相等 $\Rightarrow$ 符号约定在这张格上也是**从数据'
              '选定**的（与 R10.4 同族）。' %
              (g['ncand'], g['cords'], ab_tex(g['cstruct']), g['misAB'], g['misLab'],
               g['nspec'], ', '.join(map(str, g['w4']))), '',
         r'### 12.2 在场谱的核 $K$ 与 §11 的跨路对账（R13.2）', '',
         r'对全部 %d 条在场 422 行逐行试"哪个群元相位恒为 0" $\Rightarrow$ 核 $K=\{%s\}$'
         r'（阶分布 %s）：非平凡元 $(1,1,1)$ 是把色类 #1（$v=(%s)$）与两个弱中心元**对角粘合**，'
         r'不是任一因子的直积元。这个数与 §11 的格指数 $[P_{422}:P_{10}]=%s$ 对账：那边是 Smith '
         r'标准形、这边是特征标枚举，两台代码、一张格、同一个数 $\Rightarrow$ 3221 侧已有两条独立'
         '出处（R12.2：6 = 2×3），422 侧现在也有了。' %
         (g['nspec'], '、'.join('$(%s)$' % ', '.join(map(str, x)) for x in g['K']),
          g['kords'], ', '.join(g['classes'][1]), g['idx_422']), '',
         '### 12.3 v.e.v. 通道与逐通道商后残群（R13.3）', '',
         r'通道 $=$ 在场表示里 $Q=0$ 且在中心下非平凡的权重（按签名归并）：%d 条；'
         r'%d 个这样的权重全部落在谱行上（未落 %d 条）'
         r'$\Rightarrow$ 甲乙两套账合拢。每通道存活元 $=$ 商后陪集 $\times\,|K|$：' %
         (g['nchan'], g['nwt'], g['unmatched']), '',
         '| 承载者 | 代表 422 行 | 谱行数 | $Q=0$ 权重 | 存活元 | 商后 | 结构 | 循环 | 指数 | 允许（共 %d 条） |'
         % g['nsing'],
         '|---|---|---|---|---|---|---|---|---|---|']
    for r in rows:
        L.append('| %s | $(%s)$ | %d | %d | %d | %d | %s | %s | %d | %d |' %
                 (plain_tex([r['rep']]), ', '.join(r['rows'][0]), r['nrows'], r['nwt'],
                  r['surv'], r['quot'], ab_tex(r['struct']),
                  '是' if r['cyc'] else '否', r['expo'], r['nallow']))
    L += ['', '商后共 %d 种同构型：%s。与 3221 链同一族结论、不同族读数：**大小只挂在签名上、'
              '同构型挂在承载者上**%s。' %
          (len(g['bys']),
           '；'.join('%s：%d 条（存活 %d、商后 %d、阶 %s；承载 %s）' %
                     (ab_tex(b['struct']), b['n'], b['surv'], b['quot'], b['ords'],
                      plain_tex(sorted(set(x[0] for x in b['carriers']))))
                     for b in g['bys']),
           '；其中 %s 那一支恰落在 $SU(4)$ 中性行 $(%s)$ 上（$q_\Delta=2$ 的 $\\Delta_R$ 位，承载 %s）'
           % (ab_tex(neutral[0]['struct']), ', '.join(neutral[0]['carriers'][0][1]),
              plain_tex(sorted(set(x[0] for x in neutral[0]['carriers']))))
           if neutral else ''), '',
         '### 12.4 物质场与物质字称（R13.4）', '',
         r'6 个物质场经 `16` 的权重集桥到 422 行（与 R6.7 同一跨链对象）：每场承载行唯一、'
         r'整行一个荷签名，且全部是奇 $3(B-L)$ $\Rightarrow$ $(-1)^{3(B-L)}$ 的相位逐场都是 '
         '%s：' % uni(v['mpp'] for v in g['fv'].values()), '',
         '| 场 | 422 承载行 | $B-L$ | 物质字称相位 |', '|---|---|---|---|']
    for k in sorted(g['fv']):
        d = g['fv'][k]
        L.append('| %s | $(%s)$ | $%s$ | $%s$ |' %
                 (k, ', '.join(d['row42']), d['BL'], d['mpp']))
    L += ['', r'逐群元试"作用在 %d 个场上等于 $(-1)^{3(B-L)}$"：实现者恰 %d 个（%s，阶都是 2），'
              r'而两者之差恰是核的非平凡元 $\Rightarrow$ 物质字称在这条链上 **mod $K$ 唯一**——它'
              '不是"有没有"的问题，而是同一个陪集换代表元。' %
              (len(g['fv']), len(g['mp']),
               '、'.join('$(%s)$' % ', '.join(map(str, x['cand'])) for x in g['mp'])), '',
         '### 12.5 同一批 SM 单态算符在第二条链上（R13.5）', '',
         '§10 的含 SM 单态 d=6 场内容类（共 %d 条：%s）在本链按名字核对是**同一批**类；'
         '逐通道重跑判据，允许数逐通道读数 %s ⇒ %d 条通道上**无一改判**（共 %d 条）'
         r'$\Rightarrow$ §10 的判决（"残留群不保质子"）不随选哪条链破 $B-L$ 而变。' %
         (g['nsing'], '、'.join(g['sing']), uni(r['nallow'] for r in rows),
          len(rows), g['nsing']), '',
         '### 12.6 正向对照：判据在每条通道上真的在禁东西（R13.6）', '',
         r'去掉"要是 SM 单态"那一步，拿 %d 个物质场配成尺寸 2,3,4 的可重多重集（公式 '
         r'$\sum_k\binom{n+k-1}{k}=%d$，与枚举 %d 一致），逐通道重跑判据：' %
         (len(g['fv']), g['formula'], g['allc_tot']), '',
         '| 承载者 | 全多重集 | 全组允许 | 只弱半 | 只色半 | 两半交集 | 被禁 | 集合相等 |',
         '|---|---|---|---|---|---|---|---|']
    for c in ctl:
        L.append('| %s | %d | %d | %d | %d | %d | %d | %s |' %
                 (plain_tex([c['rep']]), c['all'], c['full'], c['weak'], c['color'],
                  c['wcapc'], c['ban'], '是' if c['inter'] else '**否**'))
    if len(exc) == 1:
        inter_txt = ('"全组允许 $=$ 只弱半 $\\cap$ 只色半"按**集合相等**判定：在 %d/%d 条通道成立；'
                     '唯一例外是 %s 那条：它的存活群元不被"只弱/只色"两半生成，两半交集放到 %d 条、'
                     r'逐元相位再收到 %d 条 $\Rightarrow$ 对角型残群上"半群读数"严格粗于逐元读数'
                     % (ninter, len(ctl), plain_tex([exc[0]['rep']]), exc[0]['wcapc'],
                        exc[0]['full']))
    elif not exc:
        inter_txt = ('"全组允许 $=$ 只弱半 $\\cap$ 只色半"在全部 %d 条通道上按集合相等成立，'
                     '无例外' % ninter)
    else:
        inter_txt = ('"全组允许 $=$ 只弱半 $\\cap$ 只色半"只在 %d/%d 条通道上按集合相等成立，'
                     '例外是 %s' % (ninter, len(ctl),
                                   '、'.join(plain_tex([c['rep']]) for c in exc)))
    L += ['', '每条通道至少禁 %d 条 ⇒ "全部允许"不是"判了 0 条"。%s。'
              '两半各有单独起作用的时候：弱半最多单独多禁 %d 条、色半最多单独多禁 %d 条。' %
              (min(c['ban'] for c in ctl), inter_txt,
               max(c['weak'] - c['full'] for c in ctl),
               max(c['color'] - c['full'] for c in ctl)), '',
         '**边界**（与 §9–§11 的边界同族）：', '',
         r'* 这仍是条件读数：承载集合是在场谱，"允许"要读成"若相应标量的 $SU(4)$ 中性分量取期望'
         '值"；本层**不**提升任何物理结论的证据等级，也不改变 P4／P7 的判据与分级。',
         '* 半群读数不总等价于逐元读数：本层实测到对角型存活群上"只弱 $\\cap$ 只色"严格更粗'
         '（%d/%d 条一致）$\\Rightarrow$ 想用"生成元的两半"省掉逐元枚举，先得按通道判生成结构。'
         % (ninter, len(ctl)),
         '* 两条链逐条同判只说明"判决不随选链而变"，**不**说明残留群保质子；'
         '导数算符（位势、跑动、阈值）与本层无关。',
         r'* 本层不回答 L10：两环跑动与阈值修正仍缺 $\Rightarrow$ **L10 未关闭**。', '']
    return L

def write_report(gates):
    (eng_ok, id_ok, phy_ok, nogo_ok, br_ok, xchk_ok, yuk_ok, inv_ok, ch_ok,
     res_ok, sel_ok, gl_ok, g422_ok, pw_ok, bs_ok) = gates
    all_ok = (eng_ok and id_ok and phy_ok and nogo_ok and br_ok and xchk_ok and yuk_ok and
              inv_ok and ch_ok and res_ok and sel_ok and gl_ok and g422_ok and pw_ok and
              bs_ok)
    L = ['# SO(10) 表示论报告（D5 权重格第一性推导）', '',
         '由 [so10_reps.py](so10_reps.py) 自动生成，**零第三方依赖**，全程整数格点 + 精确有理数。',
         '',
         '**唯一的李论输入**：D5 的 Dynkin 图（链 1–2–3，节点 3 分叉到 4 与 5）。',
         'Cartan 矩阵、正根、$\\rho$、基本权重、维数、权重重数、$\\mathrm{Sym}^2/\\wedge^2$ 分解、',
         '$B-L$ 谱、$\\Delta_R$ 承载判定、两条链的**完整分支规则**与 **d=4 Yukawa 通道表**'
         '全部由它推出；每一步都有门禁（§17）。',
         '',
         '## 0. 为什么做这个计算', '',
         '`so10_chain.py` 已把"给定内容下统不统一"变成可判定计算，但标量谱是**手工放置**的：',
         '单阈 3221 链的 $M_{\\rm GUT}$ 因此在情形之间摆动 ' + swing_note() + '，'
         '而被当作 $\\Delta_R$ 的那个三重态',
         '实际是 $B-L=0$、取自 $45_H$，**不能破 $B-L$**（链探针 S2.7）。',
         '本报告把"哪些 Higgs 表示能承担 $B-L$ 破缺"从**引用**变成**推导**。', '',
         '**结论一览**（每条对应 §17 的门禁编号）：在 $\\dim\\le210$ 内，'
         '$10_H/\\overline{10}_H/16_H/\\overline{16}_H/45_H/54_H/144_H$ 里根本没有 $|B-L|=2$ '
         '的态（R5.1）；$120_H$ 有 $(1,1,1)_{\\pm2}$ 但那些态带 $|Q|=1$，一取期望值就破电磁'
         '（R5.8）；$210_H$ 的 $|B-L|=2$ 态全在 $(1,2,2)$ 里，取任何分量都破 $SU(2)_L$'
         '（R5.3/§4.6）；剩下**唯一**能承载 $|\\Delta(B-L)|=2$ 而不破电磁的选项是 '
         '$126_H/\\overline{126}_H$ 的 $\\Delta_{L/R}$ 中性分量（R5.4），'
         '且 $126$ 与 $\\overline{126}$ 都同时含 $\\Delta_L$ 和 $\\Delta_R$，'
         '只差 $B-L$ 的符号（R5.7）。唯一的例外通道：$16_H/\\overline{16}_H$（$144_H$ 同型但更大）'
         '可按 $|\\Delta(B-L)|=1$ 单步破缺（保电磁、给不出可重整 $\\nu_R$ 质量，R5.9；'
         '它留下的是 $\\mathbb{Z}_3$ 而不是物质字称 $\\mathbb{Z}_2$，见 §9 与 R10.5）。'
         '在此基础上 §5 把 $\\dim\\le210$ 的 %d 个表示**逐权重**限制到 3221 与 422 两条链'
         '（两套独立维数路径逐分量复核、R6.5 与串检验双向一致、R6.6 与标准模型的 $16_F$ '
         '含量锚定）。§6 再独立地问第二个问题：d=4 可重整算符 $16_F16_FH$ 允许哪些 Higgs'
         ' $\\Rightarrow$ 对称通道 %s、反对称通道 %s，而对消通道 %s 里的那些表示对 $3\\times16$ '
         '物质**没有** d=4 Yukawa（R7.1–R7.7）。'
         '其后 §7 数规范不变张量的个数（R8）、§8 按双费米子道把它们拆开（R9）、§9 把"取了期望值之后 '
         '$U(1)_{B-L}$ 还剩什么"数成荷格上的阶（R10，并当场推翻旧散文"残留 $Z_2$（物质字称）对质子'
         '有利"）、§10 再把那个残留群落成**低能算符的选择定则**并回答 08 的 P7 $\\Rightarrow$ 判决是'
         '**残留群不保质子**（R11）。§11 再把那个残留群补全到中心 × 整体形式上'
         '（R12 $\\Rightarrow$ 在场谱把群钉在 $Spin(10)$ 上，完整残群在每个通道上恰是 §9'
         ' 那个 $\\mathbb{Z}_N$ 的两倍，却在 §10 的 SM 单态片上逐条同判 $\\Rightarrow$ §10'
          ' 的判决一个字不用改）。§12 再把 422 那条链的残留按 $SU(4)$ 权格重做（中心元改在'
          '特征标格上枚举、不代 triality 公式）$\\Rightarrow$ 逐通道重跑 §10 判据无一改判'
          '$\\Rightarrow$ 判决也不随"选哪条链破 $B-L$"而变（R13）。§13 再把 3221 侧中心元的'
          '枚举从行标号搬到逐权重多重集（标签现投影、$B-L$ 现点积，与 Klimyk 交错和互不共享算术）'
          '$\\Rightarrow$ 两套账的形变按集合相等、三条算术路数出的核不换数 $\\Rightarrow$ §11 那条'
          '"两套账"的边界关掉，§9/§10/§11/§12 的判决一个字不用改（R14）。§14 再把 §10 那台判据吃到'
          '的算符基摆上台面：字母表从 6 条物质分量扩到 12 条（含共轭字母）、档从 1 个扩到 6 个、'
          '"能不能缩成洛伦兹标符"做成三条互不共享算术的指标账 $\\Rightarrow$ "共轭场／导数／d>6 '
          '未枚举"那半句从此是覆盖面读数，而 §10 的判决表一个字不用改（R14 关掉的是"两套账"，'
          'R15 关掉的是"基太小"）。'

         % (len(TABLE), higgs_tex(YUKCH.get('allow', {}).get('sym', [])),
            higgs_tex(YUKCH.get('allow', {}).get('anti', [])),
            higgs_tex(YUKCH.get('allow', {}).get('vec', []))), '',
         '## 1. 引擎构造与自检', '',
         '| 步骤 | 做法 | 独立校验 |', '|---|---|---|',
         '| Dynkin 图 → Cartan 矩阵 | $A_{ii}=2$，连边 $-1$ | R0.1 与 $\\varepsilon$ 基实现逐项相等 |',
         '| 正根 | 枚举 $\\sum n_i\\alpha_i$（$n_i\\le2$）中 $|(\\cdot)|^2=2$ 者 | R0.3 得 20；R0.4 $5+2\\times20$ = 伴随维数 |',
         '| $\\rho$ 与基本权重 | $\\rho=\\frac12\\sum_{\\alpha>0}\\alpha$；解 $(\\omega_i,\\alpha_j)=\\delta_{ij}$ | R0.5 $\\rho=\\sum\\omega_i$；R0.6 定义方程 |',
         '| Weyl 群 | 单根反射闭包 | R0.7 $|W(D_5)|=1920=2^4\\cdot5!$ |',
         '| 维数 | $\\prod_{\\alpha>0}(\\Lambda+\\rho,\\alpha)/(\\rho,\\alpha)$ | R1.1 与 Freudenthal 总重数一致 |',
         '| 权重重数 | Freudenthal–Racah，按 $d(\\mu)=(\\Lambda-\\mu,\\rho)$ **升序**递推 | R1.4 在伴随上还原手工根系；R1.1 总重数；R3.x 双路比对 |',
         '| $\\mathrm{Sym}^2/\\wedge^2$ | Adams 运算 $(\\chi^2\\pm\\psi_2\\chi)/2$ | R3.1–R3.7 与 Freudenthal 比对 |',
         '| $C_2$ | $(\\Lambda,\\Lambda+2\\rho)$ | R1.5 在伴随上 $=(\\theta,\\theta+2\\rho)=2h^\\vee$，'
         '$h^\\vee(D_5)=2n-2=8$ |',
         '',
         '递推中有两处**踩过的坑**已固化成断言：分母必须是 $(\\Lambda+\\rho)^2-(\\mu+\\rho)^2$',
         '（少平移 $\\rho$ 会在 minuscule 表示处除零）；处理顺序必须按系数和 $d(\\mu)$，',
         '不能用搜索路径长度（同一点的非最小 $d$ 会破坏递推顺序 ⇒ 重数不整除）。', '',
         '## 2. 表示清单（Dynkin 标号由计算确定，未引用文献）', '',
         '| 表示 | 标号 | 维数 | 权重个数 | $C_2$ | 实/复 | $\\max|B-L|$ | $|B-L|=2$ 权重数 '
         '| $\\Delta_R(1,1,3)_{\\pm2}$ | $\\Delta_L(3,1,1)_{\\pm2}$ | $(1,1,1)_{\\pm2}$ '
         '| 能破 $B-L$ 而保 $U(1)_{em}$？ |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|']
    for r in TABLE:
        L.append('| %s | $(%s)$ | %d | %d | %s | %s | %s | %d | %s | %s | %s | %s |' %
                 (r['name'], ','.join(map(str, r['dynkin'])), r['dim'], r['nweights'],
                  r['c2'], '实' if r['real'] else '复', r['maxBL'], r['bl2'] + r['bneg2'],
                  '是' if r['DR'] else '—', '是' if r['DL'] else '—',
                  '是' if r['S2'] else '—', '是' if r['safe'] else '—'))
    L += ['', '"实"判据：共轭标号（$-\\Lambda$ 的支配代表）是否等于自身。',
          '$\\Delta_R$ 一列的含义：存在权重 $\\lambda$ 使 $B-L=\\pm2$、$SU(3)_c$ 串长为 1'
          '（色单态）、$SU(2)_L$ 串长为 1（弱单态）、$SU(2)_R$ 串长为 3（三重态）。',
          '该判据**双向严格**：$\\alpha$-串不断且重数对称是定理，故"串长 1"$\\iff$'
          '该权重上全部态是单态。',
          '最后一列 = 该表示里是否存在一个 $|B-L|=2$ 的色单态分量满足 $Q=0$'
          '（$Q=T^3_L+T^3_R+\\tfrac{B-L}{2}$，R5.8）——**这才是"能不能破 $B-L$"的物理判据**。', '',
          '## 3. 两条独立路径认定的张量恒等式', '',
          '左端只用"权重相加"（Adams 运算），右端只用 Cartan 矩阵（Freudenthal 递推）；',
          '相等才把 54/120/126/144/210 的 Dynkin 标号写进 §2。'
          '（注意 $210$ 有两个同维数标号 $(0,0,0,1,1)$ 与 $(3,0,0,0,0)$，只能靠权重多重集区分。）', '',
          'R3.7 另外暴露一条约定无关的事实：向量乘自旋量必**换手征**，'
          '$10\\otimes16=\\overline{16}\\oplus\\overline{144}$；按"$16\\oplus144$"去剥会立刻出现'
          '负重数，代码当场拒绝 ⇒ 若谁把手写的分解代进来，这一项就是拦不住的错。', '',
          '| 编号 | 恒等式 | 状态 | 细节 |', '|---|---|---|---|']
    for cid in ('R3.1', 'R3.2', 'R3.3', 'R3.4', 'R3.5', 'R3.6', 'R3.7'):
        r = next((x for x in RESULTS if x['id'] == cid), None)
        if r:
            L.append('| %s | %s | %s | %s |' % (r['id'], r['claim'], r['status'], r['note']))
    rowsd = dict((r['name'], r) for r in TABLE)

    def g(n, k):
        return rowsd.get(n, {}).get(k, '（未认定）')

    def gsum(n, *ks):
        """`g` 的数值版：任一项未认定 ⇒ 整条降级为文本，**不让报告生成器抛异常**。

        报告一旦在门禁 FAIL 的路上崩掉，缺的恰恰是最该被看到的那几行
        （与 `so10_chain.main()` 里"分开求值再用 `and` 合并"是同一条教训）。
        """
        vs = [g(n, k) for k in ks]
        return sum(vs) if all(isinstance(v, int) for v in vs) else '（未认定 ⇒ 本条不出数）'
    maxbl = dict((n, g(n, 'maxBL')) for n in ('10', '10̄', '16', '16̄', '45', '54', '144'))
    maxbltex = '、'.join('$%s\\to%s$' % (tex_name(n)[1:-1], v) for n, v in maxbl.items())
    L += ['', '## 4. 核心判定：$|\Delta(B-L)|=2$ 的破缺只能走 $126/\\overline{126}$ 的中性分量', '',
          '1. **NO-GO（约定无关）**：$\\max|B-L|<2$ 在 $10,\\overline{10},16,\\overline{16},45,54,'
          '144$ 上全部成立（算得 %s）⇒ 这些表示里**不存在** $B-L=\\pm2$ 的态，因此无论怎样分支、'
          '怎样组合，它们都承担不了 $|\\Delta(B-L)|=2$ 的破缺，给不出可重整的 $\\nu_R$ '
          'Majorana 质量（$16_H/\\overline{16}_H$ 仍可以 $|\\Delta(B-L)|=1$ 单步破 $B-L$，'
          '见第 7 条）。' % maxbltex,
          '2. $45_H$ 的 $B-L$ 谱恰为 $\\{0,\\pm2/3,\\pm4/3\\}$（$\\pm4/3$ 是 $SU(4)_c$ 伴随里'
          '轻夸克胶子方向 $\\varepsilon_i+\\varepsilon_j$ 的贡献）$\\Rightarrow$ 链探针里那个'
          '$B-L=0$ 的 $\\Sigma(1,1,3)_0$ **不是** $\\Delta_R$（这就是 S2.7 的表示论根据）。',
          '3. **最小承载者 = 126**：在 $\\dim\\le210$ 内，能把"$|B-L|=2$ + 色单态 + 弱单态 + '
          '$SU(2)$ 三重态"配齐、且三重态中含 $Q=0$ 分量的，最小维数是 %s（R5.3/R5.4）。'
          % g('126', 'dim'),
          '4. **$120_H$ 被排除的真正理由**（本阶段最强的一条）：它确实含 $(1,1,1)_{\\pm2}$'
          '（§2 的 $(1,1,1)_{\\pm2}$ 列 = %s），但 $Q=T^3_L+T^3_R+\\tfrac{B-L}{2}=\\pm1$ '
          '$\\Rightarrow$ 一取期望值就**破电磁**。一般地：任何 $(1,1,1)_{\\pm2}$ 单态都带 '
          '$|Q|=1$，而每个 $\\Delta_{L/R}$ 三重态恰有一个 $Q=0$ 分量 ⇒ '
          '**"破 $B-L$ 而保 $U(1)_{em}$" 必然经由 $\\Delta_L$ 或 $\\Delta_R$**（R5.8）。'
          '这把"必须有 $126_H$"从文献引用变成 Cartan 恒等式的推论。' % ('是' if g('120','S2') else '—'),
          '5. $126$ 与 $\\overline{126}$ **各自**都含一个 $\\Delta_L$ 与一个 $\\Delta_R$，'
          '区别只在 $B-L$ 的符号（R5.7 算得：$126$ 的 $\\Delta_R$ 在 $B-L=-2$、$\\Delta_L$ 在 '
          '$+2$；$\\overline{126}$ 全反）⇒ 二者之间是**符号选择**，不是"有没有 $\\Delta_R$"。',
          '6. $210_H$ 中 $|B-L|=2$ 的色单态权重共 %s 个，全部落在 $(1,2,2)$ 双二重态里'
          '（串长 $L=R=2$）$\\Rightarrow$ 取其中任何分量作期望值都会破坏 $SU(2)_L$；'
          '$210_H$ 只能承担 $SO(10)\\to 422/3221$ 这一步的伴随破缺，不能充当 see-saw 的来源。'
          % gsum('210', 'bl2', 'bneg2'),
          '7. **另一条通道（不排除，但要付代价）**：$|B-L|=1$ 且 $Q=0$ 的色单态在 '
          '$\\dim\\le210$ 内只出现在 $16_H/\\overline{16}_H$（$(1,2,1)_{\\pm1}$ 与 '
          '$(1,1,2)_{\\mp1}$）以及 $144_H/\\overline{144}_H$（$(1,2,3)/(1,3,2)$）里（R5.9）。'
          '用 $16_H$ 破 $B-L$ 是合法的、且**保** $U(1)_{em}$，但每步只带走一个单位 $\\Rightarrow$ '
          '残留是**奇数阶**群（$q_\\Delta=1$ 那一行的读数见 §9）⇒ 里面没有 2 阶元可言，而 '
          '$(-1)^{3(B-L)}$ 在该 v.e.v. 上取 $-1$ $\\Rightarrow$ 物质字称是**被这一步破掉的**；'
          '本轮之前这句写的是"残留 $Z_2$（物质字称，对质子稳定是好事）"，已被 §9（R10.5/R10.8）'
          '推翻并登记进 [08](../08_预言与判据.md) §3 的内部计算否定表（F7）。并且 $\\nu_R$ 的可重整'
          'Majorana 质量项仍需另外的 $|\\Delta(B-L)|=2$ 来源 ⇒ **see-saw 的量级论证不能改用 '
          '$16_H$ 替代 $126_H$**。这些分量必是某个 $SU(2)$ 的二重态，故单步破缺必然连带破'
          '$SU(2)_{L/R}$。', '',
          '**约定说明**：物质取偶负号自旋量（`so10_chain.py` 的约定）。若改取 $\\overline{16}$ '
          '为物质，$126\\leftrightarrow\\overline{126}$ 与 $\\Delta_L\\leftrightarrow\\Delta_R$ '
          '同时对调，物理内容不变；故上面每条结论只依赖 $|B-L|$，而第 4 条依赖的是 $Q$ 与 '
          '$B-L$ 之间的 Cartan 恒等式（R4.1、R4.6 已把电磁方向在 $16$ 上校准到标准电荷谱）。', '',
          ]
    L += ['', '## 5. 分支规则：$SO(10)\\downarrow 3221$ 与 $\\downarrow 422$（逐权重推导，非引用）', '',
          '两条破缺链的半单部分都与 $SO(10)$ **共享同一个 Cartan 子代数**（满秩子群）⇒ "分支"就是',
          '**同一批权重向量换一套标号**：3221 的 $A_2\\oplus A_1\\oplus A_1$ 秩 4，而与这四个单根全部',
          '正交的那一维**恰好**是 $B-L$ ⇒ 每个权重的 $B-L$ 原样带过去（下表左列的下标）；422 把',
          '$SU(3)_c$ 升级为 $SU(4)_c$（$D_3\\simeq A_3$，秩 $3+1+1=5$ = 满秩），Pati–Salam 的 $U(1)$',
          '自动落在 $SU(4)_c$ 的 Cartan 里 ⇒ **右列没有额外的 $B-L$ 下标**。分支重数用',
          'Klimyk–Springer 交错和 $n_\\lambda=\\sum_{w\\in W_H}\\det(w)\\,m_\\Lambda',
          '\\big(w(\\lambda+\\rho_H)-\\rho_H\\big)$，只复用 Freudenthal 已给的 $m_\\Lambda$ 与',
          '由单根现算的 $W_H,\\rho_H$ ⇒ 与 §1 的递推**互相独立**；再由 R6.3',
          '$\\sum_\\lambda n_\\lambda\\dim_H(\\lambda)=\\dim\\Lambda$ 收口（11 个表示 $\\times$ 两条链',
          '逐项等于 $\\dim\\Lambda$），R6.4 再用闭式维数公式对每个分量逐点复核。', '',
          '**$D_3\\simeq A_3$ 的槽位**（R6.4 的存在理由）：本引擎取 $\\beta_1=\\varepsilon_1-\\varepsilon_2$、',
          '$\\beta_2=\\varepsilon_2-\\varepsilon_3$、$\\beta_3=\\varepsilon_2+\\varepsilon_3$，而',
          '$(\\beta_1,\\beta_2)=(\\beta_1,\\beta_3)=-1$、$(\\beta_2,\\beta_3)=0$ ⇒ Dynkin 链是',
          '$\\beta_3-\\beta_1-\\beta_2$，标准 $A_3$ 编号 $(p_1,p_2,p_3)$ 等于本引擎标号的 $(c,a,b)$。',
          '槽位放错就会把 $SU(4)_c$ 的 $6$ 读成 $4$ —— 这类错不会让任何等式变红，只会让物理读错。', '',
          '| $\\Lambda$ | $\\downarrow SU(3)_c\\times SU(2)_L\\times SU(2)_R$（下标 $B-L$） '
          '| $\\downarrow SU(4)_c\\times SU(2)_L\\times SU(2)_R$ |', '|---|---|---|']
    for b in BRANCH:
        L.append('| %s | $%s$ | $%s$ |' % (tex_name(b['name']), b['tex3221'], b['tex422']))
    xsu4 = [t for t in CROSS if t['dim'] in (4, 6, 15)]
    L += ['', '重数 $>1$ 的分量前置 $n\\cdot$；$\\overline{R}$ 由标号倒序判定（$A_2,A_3$ 同规则）。'
          '两列各自求和都回到 $\\dim\\Lambda$（R6.3）。', '',
          '**这张表读出的物理事实**（每条都由上表直接可读）：', '',
          '1. $16_F$ 给出**恰好一整代**标准模型费米子加一个右手中微子：'
          '$(3,2,1)\\oplus(\\overline{3},1,2)\\oplus(1,2,1)\\oplus(1,1,2)$，422 侧 '
          '$=(4,2,1)\\oplus(\\overline{4},1,2)$ ⇒ UFE-1 的 $3\\times16$ 场内容与两条链都逐项相容'
          '（R6.6 的文献锚点；$B-L$ 只比绝对值）。',
          '2. $10_H$ 只给 $(6,1,1)\\oplus(1,2,2)$，且其中 $SU(3)_c$ 单态的那个 '
          '$SU(2)_L\\times SU(2)_R$ 双二重体分量**带 $B-L=0$** ⇒ $\\Phi(1,2,2)$ 破不了 $B-L$'
          '（链探针 S2.7 的分支规则版本）。',
          '3. 左列里 $|B-L|=2$ 的色单态**只**出现在 $126/\\overline{126}$ 的 $(1,1,3)_{\\mp2}$ 与 '
          '$(1,3,1)_{\\pm2}$（即 $\\Delta_R,\\Delta_L$）——与 §2/§4 的串检验双向一致（R6.5）；'
          '$120_H$ 的 $(1,1,1)_{\\pm2}$ 与 $210_H$ 的 $(1,2,2)_{\\pm2}$ 各按其致命方式出局（R5.8）。',
          '4. $126_H$ 的 422 分支 $=(6,1,1)\\oplus(10,3,1)\\oplus(\\overline{10},1,3)\\oplus'
          '(15,2,2)$ ⇒ 走 422 链时，破 $B-L$ 的标量**必然同时**带一个 $SU(2)_{L/R}$ 三重态：'
          '$\\Delta_L$ 在 $(10,3,1)$ 里、$\\Delta_R$ 在 $(\\overline{10},1,3)$ 里（按本引擎的 $B-L$ '
          '符号 ⇒ 本引擎的 $SU(4)_c$ 之 $4$ 对应文献 Pati–Salam 记法里的 $\\overline{4}$）；'
          '$(15,2,2)$ 则是 $422\\to3221$ 那一步的伴随破缺候选。', '',
          '**约定提示**：本引擎的 $B-L$ 整体符号与常见文献相反（$16_F$ 的轻子二重体在 $B-L=+1$ '
          '一侧），故所有下标只在本引擎内自洽；跨文献比对时作 $B-L\\to-B-L$ 即可'
          '（§4/§5 的结论只依赖 $|B-L|$，唯一用到符号的是 R5.7 的 $126\\!\\leftrightarrow'
          '\\overline{126}$ 对调）。']
    L += ['', '**跨链一致性（R6.7/R6.8a/R6.8）——本节最后三道门禁**：上表两列不是各说各话。把右列每个 '
          '$SU(4)_c$ 多重态再限制一次到 $SU(3)_c\\times U(1)_{B-L}$（色因子走 $A_3\\downarrow A_2$，'
          '其权重由**子系统版 Freudenthal 递推**现算、并用 Weyl 乘积公式的维数收口），所得 '
          '$(SU(3)_c,SU(2)_L,SU(2)_R)_{B-L}$ 多重集与左列**逐项相等**：%d 个表示全部成立。'
          '于是 $422\\to3221$ 那一步的内容同样不必引用文献：' % len(BRANCH), '',
          '| $SU(4)_c$ 表示 | 维数 | $\\downarrow\\big(SU(3)_c,1,1\\big)_{B-L}$ |', '|---|---|---|']
    for t in xsu4:
        L.append('| $%s$ | %d | $%s$ |' % (t['name'], t['dim'], '\\oplus'.join(t['content'])))
    L += ['', '三条读法：**(i)** $B-L$ 在 $SU(4)$ 的**每个**不可约表示上无迹 '
          '$\\sum_\\mu m_\\mu(B-L)(\\mu)=0$（R6.8）$\\Rightarrow B-L$ 就是 $SU(4)_c$ 的 Cartan 里与 '
          '$SU(3)_c$ 对易的**唯一**（模标度）方向（R6.8a）——故 $422\\to3221$ 不需要另外引入 '
          '$U(1)$，那一步的破缺完全由 $SU(4)$ 的伴随表示承担，表中 $15$ 行里的 $3/\\overline{3}$ '
          '分量即被破掉的生成元，其 $B-L$ 荷由算出而非引用。**(ii)** 路径无关性同时是标签系统的'
          '咬合检查：$A_3$ 的槽位放错、或 $B-L$ 的归一化与链探针不一致，都会立刻破坏等式，'
          '且 R6.7 会把差额逐条列出。**(iii)** 本节全部结论仍是权重层的数学陈述，'
          '不构成"自然界选了这条链"的证据。', '']
    L += yukawa_section()
    L += inv_section()
    L += chan_section()
    L += residual_section()
    L += selection_section()
    L += global_section()
    L += residual422_section()
    L += perweight_section()
    L += basis_section()
    z_cc = INV['ledger'][0]['zero'] if INV.get('ledger') else '（R8 未运行）'
    t126, t126b, p4 = (INV.get('tri', {}).get('126', '—'), INV.get('tri', {}).get('126̄', '—'),
                       INV.get('p4', '—'))
    chcl = ('**R9 未运行 ⇒ 本行不下结论**' if not CSPLIT.get('rows_chiral') else
            '%s 各 1 个，$126$ 道在场但**不闭合**；与情形声明的标量内容对账后，恰一个可经 '
            '$10_H$ 因子化、另一个所需的 $120_H$ **无人声明**（§8，R9.0–R9.3）' %
            '、'.join('$%s$' % chan_tex(n) for n, _k, c in CSPLIT['rows_chiral'] if c > 0))
    r1 = next((x for x in RESID.get('rows', []) if x['BL'] == '1'), None)
    r2 = next((x for x in RESID.get('rows', []) if x['BL'] == '2'), None)
    rescl = ('**R10 未跑通 ⇒ 本行不下结论**' if not (r1 and r2) else
             '$|\\Delta(B-L)|=1$ 那一步留 %s（阶为奇 $\\Rightarrow$ 群里**没有** 2 阶元，'
             '物质字称**被它破掉**）；$|\\Delta(B-L)|=2$ 那一步才留 %s。两条都是条件读数：'
             '通道的承载者与链上字面声明的母表示交集为空（R10.10）$\\Rightarrow$ 旧散文'
             '"残留 $Z_2$（物质字称）"被本节推翻' % (ztex(r1['N']), ztex(r2['N'])))
    selcl = ('**R11 未跑通 ⇒ 本行不下结论**' if not SEL.get('hit4') else
             '判据 $N\\mid 3Q$（三条互不共享算术的实现同判决）$\\Rightarrow$ d=6 的 %d 个含 SM 单态的'
             '场内容类**全部允许**（禁 0 条），其中 %d 条同时 $\\Delta B\\ne0$、$\\Delta L\\ne0$ 且 '
             '$\\Delta(B-L)=0$ $\\Rightarrow$ **残留群不保质子**；"禁 0 条"与"枚举到 0 条"由插入标量'
             '的正对照区分（§10，R11.7–R11.9）' % (len(SEL['hit4']), len(SEL['pvl'])))
    glcl = ('**R12 未跑通 ⇒ 本行不下结论**' if not GLOB.get('bys') else
            r'中心 × 整体形式做成格上读数：覆盖群到 $Spin(10)$ 的核 $|\Gamma|=%d$（三条格路数同数）'
            r'$\Rightarrow$ 在场谱把群钉在 $Spin(10)$。逐通道残群的**大小**只挂在 $|\Delta(B-L)|$ 上、'
            r'**同构型**也挂在承载者上（$q_\Delta=1$：%s；$q_\Delta=2$：%s）$\Rightarrow$ 完整群恰是 '
            r'§9 那个 $\mathbb{Z}_N$ 的两倍，却在 §10 的 %d 条 SM 单态算符上与 $\mathbb{Z}_N$ '
            r'**逐条同判**（新禁 %d 条）；去掉"要是 SM 单态"那一步做正对照，中心三项多禁 %d 条'
            r' $\Rightarrow$ 完整群不改 §10 的判决，也不随"选哪个表示破 $B-L$"而变（§11，R12.0–R12.5）' %
            (len(GLOB['gam']),
             '；'.join(class_tex(b) for b in GLOB['bys'] if b['qd'] == '1'),
             '；'.join(class_tex(b) for b in GLOB['bys'] if b['qd'] == '2'),
             GLOB['nsing'], sum(c['sing_new'] for c in GLOB['ctl']),
             sum(c['onlyz'] for c in GLOB['ctl'])))
    g422cl = ('**R13 未跑通 ⇒ 本行不下结论**' if not g422_ok else
              r'$\Rightarrow$ 不换判：422 链按 $SU(4)$ 权格重做（中心元改在特征标格上枚举、不代 '
              r'triality 公式）后逐通道重跑 §10 判据 $\Rightarrow$ %d 条通道上 §10 的 %d 条 SM '
              '单态类**无一改判**。正向对照：两半交集 $=$ 全组允许按集合相等只在 %d/%d 条通道成立，'
              '例外 %s $\\Rightarrow$ 对角型残群上半群读数严格粗于逐元读数（§12，R13.0–R13.6）' %
              (len(G422['rows']), G422['nsing'],
               sum(1 for c in G422['ctl'] if c['inter']), len(G422['ctl']),
               '、'.join(plain_tex([c['rep']]) for c in G422['ctl'] if not c['inter'])))
    pwcl = ('**R14 未跑通 ⇒ 本行不下结论**' if not pw_ok else
            r'把"对谁平凡"从行标号条件换成逐权重条件（标签由 `ipp` 现投影、$B-L$ 由 `chg` 现点积，'
            r'与 Klimyk 交错和互不共享算术）$\Rightarrow$ 甲账 %d 条条件、乙账 %d 条（其中 %d 条'
            r'甲账根本没有），但两套账的形变按集合相等（%d 种对 %d 种，且 %d/%d 个表示各自也相等）；'
            r'核走三条独立算术路、两种 triality 约定都数出 %d 个，且与 §11 逐元相等'
            r'$\Rightarrow$ **换账不换群**，那条"两套账"的边界关掉（§13，R14.0–R14.6）'
            % (G14['nspec'], G14['ncond'], G14['novel'], G14['charA'], G14['charB'],
               G14['eq_per_name'], G14['nrep'], G14['gam']))
    bscl = ('**R15 未跑通 ⇒ 本行不下结论**' if not bs_ok else
            r'字母表从 %d 条物质场分量扩到 %d 条（含共轭字母）、档从 1 个扩到 %d 个（签名类合计 %d 条）、'
            r'$d_{\min}$ 探到 %s；洛伦兹账三条实现同判（违例 %d/%d）$\Rightarrow$ "共轭场／导数／d>6 '
            r'未枚举"那半句从此是覆盖面读数：$d=6$ 档里只取非点号字母的那 %d 条与 §10 的 %d 条**集合'
            r'相等**，指标禁与群禁在字面声明的标量谱上集合相等（各 %d 条）；但插入含奇 $3(B-L)$ 分量的'
            r'标量之后两本账**双向**分叉（$+144_H$ 各独有 %d/%d 条）$\Rightarrow$ §10 的判决表一个字不用'
            r'改、它的覆盖面从此有数（§14，R15.0–R15.6）' %
            (sum(1 for a in BASIS['alpha'] if a[5] == 0), len(BASIS['alpha']),
             BASIS['cover'][0], BASIS['cover'][1], BASIS['cover'][3],
             BASIS['parity'][0], BASIS['parity'][1], BASIS['und_only'][0], len(SEL['hit4']),
             BASIS['coin'][0], BASIS['ctl'][2]['onlyL'], BASIS['ctl'][2]['onlyZ']))
    if GLOB.get('bys'):
        glbd = (r'* 当年那条边界已**做成读数**（§11，R12.0–R12.5）：把 $SU(3)_c$、'
        r'$SU(2)_{L/R}$ 的中心与 $Spin(10)$ 的整体形式一起放上荷格，在 %d 个候选中心元上'
        r'逐个试 $\Rightarrow$ 活下来的构成核 $\Gamma$，$|\Gamma|=%d$，三条格路数同数'
        r'（%d $=|\Gamma|$ $=%d\times%d$）$\Rightarrow$ 群被在场谱钉在 $Spin(10)$ 本身；每个通道'
        r'上完整残群恰是 §9 那个 $\mathbb{Z}_N$ 的**两倍**、同构型还挂在承载者上 $\Rightarrow$ '
        r'"至少留下这些"当年确实是**下界**。但多出来那半边在 §10 的 %d 条 SM 单态算符上与 '
        r'$\mathbb{Z}_N$ **逐条同判**（新禁 %d 条），去掉"要是 SM 单态"那一步才由中心多禁 %d 条 '
        r'$\Rightarrow$ §10 的判决不因完整群而变。当年\"仍未做\"的 422 那条链现已做成格上读数'
        r'（残留按 $SU(4)$ 权格重做、`SUB_422` 的单根不是 $A_3$ 链 $\Rightarrow$ triality 公式'
        r'不能直接代；§12/R13 $\Rightarrow$ 逐通道判决不换）。而且这仍是条件读数 $\Rightarrow$ '
        r'§10 的算符判决沿同一条条件性下来'
        r'（"允许"要读成"若补入 $126_H$ 且其中性分量取期望值"），唯一不随标量谱变的是'
        r'"偶数条物质场 $\Rightarrow$ $3Q$ 为偶"那一步。' %
               (GLOB['ncand'], len(GLOB['gam']), GLOB['idx_h'], GLOB['idx_422'],
                GLOB['idx_hop'], GLOB['nsing'], sum(c['sing_new'] for c in GLOB['ctl']),
                sum(c['onlyz'] for c in GLOB['ctl'])))
    else:
        glbd = (r'* §9 只数 $U(1)_{B-L}$ **这一个因子**内的残留子群：$SU(3)_c$ 与 $SU(2)_{L/R}$'
        r' 的中心、规范群的整体形式（$Spin(10)$ 与它的商）都不在那张荷格里 $\Rightarrow$ 完整残留群'
        r' 可能是这里那个 $\mathbb{Z}_N$ 的**扩张**，§9 只给"至少留下这些"'
        r'（R12 未跑通 ⇒ 本条仍是旧边界，没有读数）。')
    L += ['', '## 15. 对 L10（耦合统一）的直接影响', '',
          '| 事项 | 手工放置（旧） | 本报告（推导） |', '|---|---|---|',
          '| $\\Phi(1,2,2)$ 的来源 | 假设取自 $10_H$ | $10\\to(6,1,1)\\oplus(1,2,2)$ 由权重集直接读出 ✔ |',
          '| $\\Sigma(1,1,3)_0$ 的来源 | 误标为 $\\Delta_R$ | 取自 $45_H$、$B-L=0$，**不是** $\\Delta_R$ |',
          '| $B-L$ 破缺的最小 Higgs | 未判定 | $126/\\overline{126}$（$\\dim\\le210$ 内唯一最小） |',
          '| $120_H$ 能否破 $B-L$ | 未判定 | **否**：其 $(1,1,1)_{\\pm2}$ 分量带 $|Q|=1$，'
          '取期望值即破 $U(1)_{em}$ |',
          '| $210_H$ 的作用 | 含糊地兼作 $\\Delta_R$ 来源 | 只承担 $SO(10)\\to422/3221$；'
          '其 $|B-L|=2$ 的色单态全在 $(1,2,2)$ 里，取任意分量都破 $SU(2)_L$ |',
          '| see-saw 标度 $M_R$ 的地位 | 只是匹配标度 | 需 $126_H$ 的真空期望值才成立 ⇒ '
          '链探针 §5.5 的量级结论仍是下界式论证 |',
          '| d=4 允许的 Yukawa Higgs | 未判定 | 手征通道 %s（对称）$\\oplus$ %s（反对称）；'
          '对消通道 %s 里的表示对 $3\\times16$ 物质**没有** d=4 Yukawa（§6，R7.1–R7.2） |'
          % (higgs_tex(YUKCH.get('allow', {}).get('sym', [])),
             higgs_tex(YUKCH.get('allow', {}).get('anti', [])),
             higgs_tex(YUKCH.get('allow', {}).get('vec', []))),
          '| $\\nu_R$ Majorana 项的承载者 | 只按"有没有 $\\Delta_R$"判定 | 与通道表**独立**'
          '地再判一次：$-2\\nu$ 这个权重在 $\\dim\\le210$ 里唯一地落在 %s（§6 第 3 条，R7.4） |'
          % higgs_tex(YUKCH.get('maj', [])),
          '| 手征费米子能否有裸质量 | 当作常识引用 | 数出来：$16\\otimes16$ 的零权方向 %s 个'
          ' $\\Rightarrow$ 连荷守恒都做不到（§7，R8.4） |' % z_cc,
          '| $\\Delta(B-L)=2$ 的过程能否只用物质凑出 | 未判定 | **否**：不变张量必为零权 $\\Rightarrow$ '
          '物质-only 的不变算符自动 $\\Delta(B-L)=0$；要拿到 $|B-L|=2$ 必须插入 %s，'
          '插入 $126$ 得 %s 个单态、插入 $\\overline{126}$ 得 %s 个（§7，R8.5） |'
          % (higgs_tex(['126̄']), t126, t126b),
          '| 四费米子不变算符的个数 | 未判定 | $\\mathrm{mult}((1),16^{\\otimes4})=%s$'
          '（四条独立路径一致，§7 表二）$\\Rightarrow$ 规范群**不**禁止质子衰变那一类算符的'
          '**荷前提**；个数不等于物理算符个数（Lorentz／味／Fierz 未判） |' % p4,
          '| 这 %s 个不变张量**各自**走哪条道 | 未判定 | %s |' % (p4, chcl),
          '| $B-L$ 破缺后**残留哪个离散规范对称性** | 散文：残留 $Z_2$（物质字称，"对质子稳定'
          '反而有利"） | %s |' % rescl,
          '| 那个残留群**禁哪些低能算符**、保不保质子 | 待办（§9 登记为未判） | %s |' % selcl,
          '| **完整**残留群（中心 × 整体形式）是哪个群、会不会改判 | 旧边界登记为未判（只数了 '
          r'$U(1)_{B-L}$ 那一个因子） | %s |' % glcl,
           '| 第二条链（422）上残留换不换判 | 旧边界两处登记"未做"（§9/§11） | %s |' % g422cl,
           '| 中心元枚举换到**逐权重**账上会不会换群 | 旧边界登记为"与 §5 是两套账"（§11） | %s |'
           % pwcl,
           '| §10 那台判据的**算符基**覆盖到哪 | 旧边界登记为"只到 d=6、只到物质场分量"'
           '（09 第十二项 (iii)） | %s |' % bscl,

          '',
          '⇒ 情形 B（无 $126_H$）**不能**声称实现了 $B-L$ 破缺；它是一条"只跑到 $LR$ 相位"'
          '的参考曲线。$126_H$ 的完整分支规则**已在 §5 逐权重算出**（含每个分量落在哪条链的哪个'
          '多重态），故剩余的标量谱不确定度（当前为 ' + swing_note() + '）只能由两环跑动 + '
          '阈值修正 + $126_H$ 位势压掉，'
          '而不是再换一种手工谱。', '',
          '## 16. 诚实边界', '',
          '* 表示论结果是**数学陈述**：它说明"SO(10) 若成立，Higgs 扇区必须含 $126$ 型表示"，'
          '**不**说明自然界含 SO(10)，也**不**提升 UFE-1 任何结论的证据等级，'
          '更**不**意味着统一场论已完成。',
          '* 第 4 条判定用了两个**物理输入**而非李论推导：$U(1)_{em}$ 未被破缺（'
          '$Q=0$ 才允许取期望值）与 $B-L$ 需要被破掉（否则无 see-saw、$\\nu_R$ 无 Majorana 质量）。'
          '二者若有一条不成立，"$126_H$ 必需"这条结论随之失效——它不是无条件定理。',
          '* 分支规则（§5）给的是**权重层**的完整内容：哪个多重态出现、出现几次、带多少 $B-L$。'
          '两条链的跨链匹配**已实现为门禁**（R6.7 路径无关、R6.8 $B-L$ 在 $SU(4)$ 每表示无迹、'
          'R6.8a 方向唯一），故 $422\\to3221$ 那一步不再是从表格对照读出的猜想。'
          '§6 又把"哪个 Higgs 拿得到 d=4 算符"独立判了一遍（R7），§7 再把"哪些组合本身就是'
          '规范不变的"数了一遍（R8：$\\mathrm{mult}((1),V)$ 与荷账本 $\\dim V_0$ 分开记账），'
          '§8 把 §7 的配对和按**双费米子道**拆开（R9：哪条道闭合、$|B-L|=2$ 那个 Higgs 为何'
          '插不进单个插入），§9 再把"取了期望值之后 $U(1)_{B-L}$ 还剩什么"数成荷格上的阶'
          '（R10：$N=q_\\Delta/g_0$，并且当场推翻旧散文"残留 $Z_2$（物质字称）"），§10 再把那个残留群'
          '落成**低能算符的选择定则**（R11：判据 $N\\mid 3Q$，逐条判决 d=4/d=6 算符 $\\Rightarrow$ '
          '"残留群保不保质子"有了答案：**不保**），§11 再把那个群补全为中心 × 整体形式并逐条'
           '回判 §10（R12：完整群在 SM 单态片上与 §9/§10 的那个 $\\mathbb{Z}_N$ 同判），§12 再把 '
           '422 那条链的残留按 $SU(4)$ 权格重做一遍（R13：核非平凡、14 条通道无一改判），§13 再把'
           ' 3221 侧中心元的枚举搬到逐权重账上（R14：两套账的形变集合相等、核不换数），§14 再把 §10 '
           '那台判据吃到的算符基扩成"含共轭字母 $+$ 含导数账"的六档（R15：绝对禁与上移分开数、覆盖面'
           '登记成数）。但这十层都'
          '**不含** Yukawa 系数（哪个拷贝与哪一代费米子耦合、'
          '矩阵多大）、'
          '不含 $126_H$ 的位势与真空方向，也**不含**任何动力学——'
          '权重层允许的分量不等于自然界取到的分量。',
          glbd,
          '* §10 的表只过了**规范不变**这一关（同 §7 的处置）：%s 个含 SM 单态的 d=6 场内容类全部'
          '"允许"是群论陈述，$\\Rightarrow$ "残留群不保质子"只否定"离散群能救质子"这条论证，'
          '**不**给出质子会衰变的速率，也不改变 P4／P7 的判据与分级。' %
          ('%d' % len(SEL['hit4']) if SEL.get('hit4') else '那些'),
          '* §7 数的是**规范不变张量**的个数，不是算符个数：Lorentz 指标、代（味）指标与 '
          'Fierz 恒等式三关都没过 $\\Rightarrow$ "$16^{\\otimes4}$ 有 %s 个不变张量"不能被读成'
          '"有 %s 个质子衰变算符"，本节的数**不**回填进任何寿命计算。' % (p4, p4),
          '* 未做二环跑动与阈值修正 ⇒ **L10 未关闭**。本报告只把"允许的标量内容"与'
          '"允许的 d=4 Yukawa 通道"收紧。',
          '* $C_2$、维数等只用于自校验与后续阈值分析，不与任何实验值比对。', '',
          '## 17. 全部测试明细', '',
          '| 编号 | 命题 | 算得 | 应为 | 容差 | 状态 | 备注 |', '|---|---|---|---|---|---|---|']
    for r in RESULTS:
        # 三个 repr 转储列先折回表示层的翻倍再进表格（备注列还要转义裸竖线，顺序：先折、后转义）
        L.append('| %s | %s | %s | %s | %s | %s | %s |' %
                 (r['id'], md_unescape(r['claim']), md_unescape(r['computed']),
                  md_unescape(r['expected']), r['tolerance'], r['status'],
                  md_unescape(r['note']).replace('|', '\\|')))
    L += ['', '**门禁**：' + ('R0–R15 全部 PASS ⇒ §2 的表示清单、§4 的 $\\Delta_R$ 判定、'
                               '§5 的分支规则、§6 的 d=4 Yukawa 通道、§7 的不变张量账目、§8 的'
                               '道分解、§9 的残留离散群、§10 的低能算符选择定则、§11 的完整残留群'
                               '/整体形式、§12 的 422 链重做读数、§13 的两套账交叉读数与 §14 的算符基覆盖面读数'
                               '可信。' if all_ok else
                              '**存在 FAIL ⇒ 本报告不出任何 Higgs 扇区结论**。'), '',
         '[返回统一场方程](../README.md) · [SO(10) 链统一报告](SO10链统一报告.md) · '
         '[已知局限](../09_已知局限与否定清单.md)']
    txt = '\n'.join([table_row_safe(x) for x in L]) + '\n'
    # 本报告的 LaTeX 由脚本里的字符串字面量拼出：漏写双反斜杠时 \alpha、\to、\beta、\nu
    # 会被 Python 当成转义而变成控制字符，并静默把 Markdown 表格行截断 ⇒ 写盘前当场拒绝。
    ctrl = sorted(set(c for c in txt if ord(c) < 32 and c != '\n'))
    assert not ctrl, '报告含控制字符 %s ⇒ 有 LaTeX 反斜杠被 Python 吃掉' % ctrl
    # 表格行列数必须与自己的表头一致：错位只会"渲染时少一列"，不会让任何门禁变红
    lines = txt.split('\n')
    i = 0
    while i < len(lines) - 1:
        if lines[i].startswith('|') and SEPROW.match(lines[i + 1].strip()):
            ncol = len(PIPE.split(lines[i]))
            j = i + 2
            while j < len(lines) and lines[j].startswith('|'):
                assert len(PIPE.split(lines[j])) == ncol, \
                    '表格列数错位（表头 %d 列）：\n  %s\n  %s' % (
                        ncol - 2, lines[i][:90], lines[j][:90])
                j += 1
            i = j
        else:
            i += 1
    # 正文排版的五条不变量（前四条各修掉一处真实缺陷，第五条关掉的是 09 第 8 项登记的那条待办）。
    # **编号是引擎自查序列**，与文档里"第 N 条排版不变量"那条序列不同源：文档序列把表格列数算第 5 条、
    # 把本条算第 6 条 ⇒ 引用编号必须连文件一起引，否则两个"第五条"会各自指错。
    #   1) $…$ 必须在**同一个段落内**闭合 —— 少一个 `$` 会把它后面的整段吞进公式里渲染；
    #   2) 段落里不得出现未格式化的 Python 容器 repr 或 None —— 漏写一个 %s 参数就会印成 `['10', …]`；
    #   3) 段落里不得出现未替换的 `%d`/`%(name)s` 占位符 —— `%` 只绑到拼接字面量的第一段时就漏；
    #   4) \lvert / \rvert 后不得紧跟字母或数字 —— TeX 最长匹配会把 `\lvertB` 读成一个未定义
    #      控制词而整段公式报错。这条**必须查全文**：缺陷正是 table_row_safe 只往表格行里注的，
    #      前两条的"表格行豁免"在这里反过来不成立。
    # 表格行豁免前两条：§17 的"算得/应为/备注"列**故意**是原始 repr，那是审计痕迹不是排版。
    blocks, cur = [], []
    for ln in lines:
        if ln.startswith('|') or not ln.strip():
            if cur:
                blocks.append(' '.join(cur))
                cur = []
        else:
            cur.append(ln)
    if cur:
        blocks.append(' '.join(cur))
    unclosed = [b[:70] for b in blocks if b.count('$') % 2]
    leaked = [b[:70] for b in blocks if REPR_LEAK.search(b)]
    fmt = [b[:70] for b in blocks if FMT_LEAK.search(b)]
    munch = sorted(set(DELIM_MUNCH.findall(txt)))
    # 第五条：紧跟字母的反斜杠串长度必须为 1（同上，全文判、不豁免表格行）
    bs_hit = [(i, m.group(0)) for i, ln in enumerate(lines, 1) for m in BS_MUNCH.finditer(ln)]
    HYGIENE.update({'blocks': len(blocks), 'unclosed': unclosed, 'leaked': leaked,
                    'unformatted': fmt, 'delimiter_munch': munch,
                    'backslash_munch_sites': len(bs_hit),
                    'backslash_munch_kinds': sorted(set(t for _, t in bs_hit)),
                    'backslash_munch_lines': sorted(set(i for i, _ in bs_hit)),
                    'tables': len([1 for ln in lines if SEPROW.match(ln.strip())])})
    assert not unclosed, '有段落的 $…$ 未闭合 ⇒ 渲染时吞掉后半篇：%s' % unclosed
    assert not leaked, '正文里漏进未格式化的 Python 对象：%s' % leaked
    assert not fmt, '正文里漏进未替换的格式化占位符（漏写 %% 参数）：%s' % fmt
    assert not munch, ('\\lvert/\\rvert 后紧跟字母数字 ⇒ TeX 读成未定义控制词，公式整段报错：%s'
                       % munch)
    assert not bs_hit, ('%d 处、%d 种"两个及以上反斜杠紧跟字母"（行号:串 %s）⇒ raw 字面量里多打了'
                        '一个反斜杠：MathJax 把 `\\\\` 读成换行，后面的控制词降级成斜体字母'
                        % (len(bs_hit), len(set(t for _, t in bs_hit)),
                           ', '.join('%d:%s' % (i, t) for i, t in bs_hit[:6]) +
                           ('…' if len(bs_hit) > 6 else '')))
    (ROOT / 'SO10表示论报告.md').write_text(txt, encoding='utf-8')
    (ROOT / 'SO10表示论报告.json').write_text(json.dumps(
        {'purpose': 'D5=so(10) 表示论第一性推导：Higgs 分支内容、Δ_R 承载判定与 d=4 Yukawa 通道',
         'lie_input': 'D5 Dynkin diagram only; everything else derived',
         'chain_engine_pass': CHAIN_OK,
         'engine_pass': eng_ok, 'identification_pass': id_ok,
         'physics_pass': phy_ok, 'nogo_pass': nogo_ok, 'branching_pass': br_ok,
         'cross_chain_pass': xchk_ok, 'yukawa_pass': yuk_ok, 'invariant_pass': inv_ok,
         'channel_split_pass': ch_ok, 'residual_pass': res_ok, 'selection_pass': sel_ok,
         'global_pass': gl_ok, 'residual422_pass': g422_ok, 'perweight_pass': pw_ok,
         'basis_pass': bs_ok,
         'named_dynkin': dict((k, list(v)) for k, v in NAMED.items()),
         'table': TABLE, 'branch': BRANCH, 'su4_to_su3u1': CROSS,
         'yukawa': YUK, 'yukawa_channels': YUKCH.get('allow', {}),
         'yukawa_products': dict((k, v) for k, v in YUKCH.get('parts', {}).items()),
         # R8 的原始读数（报告 §7 的每个数字都出自这里，不在 JSON 里另算一遍）
         'singlet_ledger': [{'product': x['tex'], 'dim': x['dim'], 'distinct_weights': x['ndist'],
                             'zero_weight_dirs': x['zero'], 'invariants': x['singlet'],
                             'per_constituent_check': x['split'],
                             'unregistered_share': (x['parts'] or {}).get('unreg')}
                            for x in INV.get('ledger', [])],
         'invariant': {'delta_pairs_tested': INV.get('npairs'),
                       'delta_one_pairs': INV.get('ones'),
                       'delta_counterexamples': INV.get('wrong', []),
                       'dim_product_cap': INV.get('cap'),
                       'routes': INV.get('routes', {}), 'associative': INV.get('assoc'),
                       'channels_by_singlet_count': dict((k, v['names'])
                                                         for k, v in INV.get('chan', {}).items()),
                       'channels_agree_with_r7': dict((k, v['agree'])
                                                      for k, v in INV.get('chan', {}).items()),
                       'triple_product_singlets': INV.get('tri', {}),
                       'matter_only_invariants': INV.get('p4'),
                       'matter_only_zero_dirs': INV.get('zero_p4')},
         # R9 的原始读数：报告 §8 的每个数字都出自这个字典，不在 JSON 里另算一遍
         'channel_split': CSPLIT,
         # R10 的原始读数：报告 §9 的每个数字都出自这个字典（含两条独立路径与植入缺陷列）
         'residual': RESID,
         # R11 的原始读数：报告 §10 的每个数字都出自这里。物质场清单里那份权重多重集
         # **不进 JSON**（它的键是 5 元组，JSON 的键只能是标量），其余字段原样落盘。
         'selection': dict(SEL, mat=[{k: v for k, v in f.items() if k != 'ms'}
                                     for f in SEL.get('mat', [])]),
         # R12 的原始读数：报告 §11 的每个数字都出自这里（元组由 default=str 落成字符串）
          'global': GLOB,
          # R13 的原始读数：报告 §12 的每个数字都出自这里
          'residual422': G422,
          # R14 的原始读数：报告 §13 的每个数字都出自这里
          'perweight': G14,
          # R15 的原始读数：报告 §14 的每个数字都出自这里
          'basis': BASIS,
         'report_hygiene': HYGIENE,

         'tests': RESULTS},
        ensure_ascii=False, indent=2, default=str) + '\n', encoding='utf-8')
    return all_ok


def main():
    eng_ok = run_engine_tests()
    id_ok = run_identification() if eng_ok else False
    if eng_ok and id_ok:
        id_ok = run_tensor_identities()
    phy_ok = run_physics_tests() if id_ok else False
    nogo_ok = bool(build_table()) and gate_no_go() if phy_ok else False
    br_ok = run_branching() if nogo_ok else False
    xchk_ok = run_cross_chain() if br_ok else False
    yuk_ok = run_yukawa_layer() if xchk_ok else False
    inv_ok = run_invariant_layer() if yuk_ok else False
    ch_ok = run_channel_layer() if inv_ok else False
    res_ok = run_residual_layer() if ch_ok else False
    sel_ok = run_selection_layer() if res_ok else False
    gl_ok = run_global_layer() if sel_ok else False
    g422_ok = run_residual422_layer() if gl_ok else False
    pw_ok = run_perweight_layer() if g422_ok else False
    bs_ok = run_basis_layer() if pw_ok else False
    all_ok = write_report((eng_ok, id_ok, phy_ok, nogo_ok, br_ok, xchk_ok, yuk_ok, inv_ok,
                           ch_ok, res_ok, sel_ok, gl_ok, g422_ok, pw_ok, bs_ok))

    print('SO(10) 表示论引擎（D5 权重格；唯一李论输入 = Dynkin 图）')
    print('  自检：%s（%d 项，PASS %d）' %
          ('全部通过' if all_ok else '存在 FAIL ⇒ 不出 Higgs 扇区结论',
           len(RESULTS), sum(1 for r in RESULTS if r['status'] == 'PASS')))
    for r in RESULTS:
        if r['status'] != 'PASS':
            print('    [FAIL] %-9s %s：算得 %s，应为 %s' %
                  (r['id'], r['claim'], r['computed'], r['expected']))
    print('  排版自检：%d 个正文段落（表格行豁免）的 $…$ 全部闭合、无未格式化的 Python 对象、'
          '无未替换的 %%d/%%(name)s 占位符；%d 张表格列数与各自表头一致；'
          '全文 \\lvert/\\rvert 后均紧跟分隔符，未被 TeX 最长匹配读成未定义控制词；'
          '紧跟字母的反斜杠串长度 >1 的有 %d 处 / %d 种（要求 0 处 —— 翻倍只会在这条上现形：'
          'raw 字面量里手写的，和 repr 转储把数据里的反斜杠翻倍，数值门禁两条都看不见）。'
          % (HYGIENE['blocks'], HYGIENE['tables'], HYGIENE['backslash_munch_sites'],
             len(HYGIENE['backslash_munch_kinds'])))
    if TABLE:
        print('  表示清单（末列 = 能否在保住 U(1)_em 的前提下破 B−L）：')
        for r in TABLE:
            print('    %-6s (%s) dim=%-4d C2=%-6s max|B-L|=%-5s Δ_R=%s Δ_L=%s '
                  '(1,1,1)±2=%s 可破 B−L=%s' %
                  (r['name'], ','.join(map(str, r['dynkin'])), r['dim'], r['c2'], r['maxBL'],
                   '是' if r['DR'] else '—', '是' if r['DL'] else '—',
                   '是' if r['S2'] else '—', '是' if r['safe'] else '—'))
    if br_ok:
        print('  分支规则（R6）：%d 个表示 × 两条链，逐权重精确；两条独立维数路径逐项一致。'
              '锚点两行：' % len(BRANCH))
        for nm in ('16', '10'):
            b = next(x for x in BRANCH if x['name'] == nm)
            print('    %-4s ↓3221  %s' % (nm, plain(b['tex3221'])))
            print('    %-4s ↓422   %s' % (nm, plain(b['tex422'])))
    if xchk_ok:
        print('  跨链匹配（R6.7/R6.8）：%d 个表示的"两步限制"与"一步限制"逐项相等；'
              '$SU(4)$ 每个不可约表示上 Tr(B−L)=0。锚点（$422\\to3221$ 那一步）：' % len(BRANCH))
        for t in CROSS:
            if t['dim'] in (4, 15):
                print('    %-12s dim=%-3d %s' % (plain(t['name']), t['dim'],
                                                 plain('\\oplus'.join(t['content']))))
    if yuk_ok:
        a = YUKCH['allow']
        print('  d=4 Yukawa 通道（R7）：手征 对称 %s／反对称 %s；对消 %s；'
              '唯一携带 −2ν 权重的 Higgs：%s' %
              (a['sym'], a['anti'], a['vec'], YUKCH['maj']))
        print('    成分（共轭前）：Sym²(16)=%s，∧²(16)=%s，16⊗16̄=%s（跳过单态后取共轭 = 上一行）' %
              tuple([n for n, _k in YUKCH['parts'][k]] for k in ('sym', 'anti', 'vec')))
    if inv_ok:
        print('  不变张量簿记（R8）：按 16⊗16／16⊗16̄／16⊗4 顺序，'
              '（荷账本 = 零权方向数，不变张量 = 单态个数）为 %s' %
              [(x['zero'], x['singlet']) for x in INV['ledger']])
        print('    16⊗16⊗16̄⊗16̄ 的单态数由 4 条不共享代码的路径给出同一个数：%s；'
              'δ 判据现场核验 %d 对（其中 δ=1 的 %d 对，反例 %s）'
              % ([INV['routes'][k] for k in ('decomp_I', 'decomp_II', 'pair_cc', 'pair_cf')],
                 INV['npairs'], INV['ones'], ('无' if not INV['wrong'] else INV['wrong'])))
    if ch_ok:
        print('  不变张量的道分解（R9）：16⊗16 的道（道名, n_R, 该道贡献 n_R·n_R̄）=%s ⇒ 合计 %d'
              '（R8 解方程 %d）；16⊗16̄ 的道=%s ⇒ 合计 %d（R8 %d）' %
              (CSPLIT['rows_chiral'], CSPLIT['tot_chiral'], CSPLIT['r8_chiral'],
               CSPLIT['rows_vector'], CSPLIT['tot_vector'], CSPLIT['r8_vector']))
        print('    在场却不闭合的道：%s（= 126̄_H 的伙伴）；Sym²=%s，∧²=%s，16⊗16̄=%s；'
              '链上字面声明的母表示并集=%s' %
              ([n for n, _k, c in CSPLIT['rows_chiral'] + CSPLIT['rows_vector'] if not c],
               [n for n, _k in CSPLIT['slot']['sym']], [n for n, _k in CSPLIT['slot']['anti']],
               [n for n, _k in CSPLIT['slot']['vec']], CSPLIT['decl_union']))
        print('    单个 126／126̄ 插入 16⊗4 的三种结合：%s（全为 0）；成对插入（结合 I／II／镜像）：'
              '%s' %
              ([(k, v['gI'], v['gII'], v['gIII']) for k, v in CSPLIT['ins'].items()],
               [(k, v['gI'], v['gII'], v['mirror']) for k, v in CSPLIT['pairs'].items()]))
        m = CSPLIT['mut']
        print('    变异测试：删 120→%d、闭合道 %s 翻倍→%d、伪造 126̄ 在场→%d（真值 %d）；'
              '16⊗4⊗126⊗126 上标号路径 %d vs 名字路径 %d（登记范围外 %d 条标号）' %
              (m['drop'], m['dnm'], m['dbl'], m['fake'], m['real'], m['lab'], m['byname'],
               m['unreg']))
    if res_ok:
        print('  残留离散规范对称性（R10）：$B-L$ 荷格 g0 = %s（仅物质 %s）⇒ 圆周 alpha0 = '
              '%s·pi（浮点独立测得 %s·pi）' %
              (RESID['g0_all'], RESID['g0_matter'], RESID['period_exact'], RESID['period_scan']))
        print('    候选 q_Delta → 残留阶 N（甲／乙浮点／丙换约定／错配植入）=%s；'
              '物质字称在 v.e.v. 上=%s；弱电 $B-L=0$ 那一步后剩／对照 q_Delta/2 后剩=%s' %
              ([(r['BL'], r['N'], r['N_scan'], r['N_half'], r['N_mismatch'])
                for r in RESID['rows']],
               [(r['BL'], r['mp']) for r in RESID['rows']],
               [(r['BL'], r['ew'], r['ctl']) for r in RESID['rows']]))
        print('    圆周上的 2 阶元与 (-1)^(3(B-L)) 逐荷对照：%s；承载者与链声明谱的交集=%s' %
              ([(r['BL'], r['ord2'], '同' if r['ord2_is_mp'] else '不同')
                for r in RESID['rows'] if r['ord2'] != '无'], RESID['cond']))
    if sel_ok:
        print('  低能算符的选择规则（R11）：projector = SU(3)c×SU(2)L 配 U(1)Y 的 Y 切片'
              '（|Δ+|=%d、|W|=%d）；$Z_3$ 荷 = 色 triality，教材号 s=%s／引擎号 s=%s'
              '（R10.4 权重层 %s）' %
              (len(SUB_321.pos), len(SUB_321.W), SEL['tri_sgn'], SEL['tri_sgn_engine'],
               RESID['triality_sign']))
        print('    d=6：%d 个场内容类、含 SM 单态 %d 条（不变张量结构 %d 个）、三条计数路径 %s；'
              'ΔB≠0 且 ΔL≠0 的 %d 条**全部** Δ(B−L)=0、其中被禁 %d 条 ⇒ 残留群不保质子' %
              (len(SEL['c4']), len(SEL['hit4']),
               sum(x['singlet'] for x in SEL['hit4']), SEL['r4'][1:4], len(SEL['pv']),
               sum(1 for x in SEL['pvl']
                   if False in [v['甲'] for v in x['v'].values()])))
        print('    正对照：插入声明谱 %d 条／插入奇 3(B−L) 标量 %d 条（$Z_6$ 判禁 %d 条、'
              '只按 $Z_3$ 会误放行 %d 条）；整套荷换号后判决翻转 %d 条（应为 0）' %
              (len(SEL['scan_decl']), len(SEL['scan_odd']), len(SEL['forb_odd']),
               len(SEL['flip3']), len(SEL['flip_sg'])))
    if gl_ok:
        print('  完整残留离散规范群（R12）：候选中心元 %d 个 ⇒ 核 |Gamma| = %d（三条格路数 %d = %dx%d）'
              '⇒ 群钉在 Spin(10)；在场 %d 个表示按 P/Q 类分层：%s / %s / %s' %
              (GLOB['ncand'], len(GLOB['gam']), GLOB['idx_h'], GLOB['idx_422'], GLOB['idx_hop'],
               GLOB['nrep'], GLOB['tens'], GLOB['ord2'], GLOB['ord4']))
        print('    逐通道残群（|Delta(B-L)|, 承载者, 存活, 商后, 结构, 循环, 指数）=%s；每通道承载者数=%s；'
              '§9 的 N=%s ⇒ 商后阶 = 2N' %
              ([(r['qd'], r['rep'], r['surv'], r['coset'], r['struct'], r['cyc'], r['expo'])
                for r in GLOB['rows']], GLOB['ncar'], GLOB['nres']))
        print('    与 §10 的对账：%d 条 SM 单态算符上中心新禁 %d 条；去掉单态的正对照（每通道全组合 %d 条）'
              '由中心多禁 %s 条；逐陪集代表元 vs 逐个存活元分歧 %d 条' %
              (GLOB['nsing'], sum(c['sing_new'] for c in GLOB['ctl']), GLOB['allc_tot'],
               [c['onlyz'] for c in GLOB['ctl']], sum(c['disagree'] for c in GLOB['ctl'])))
    if g422_ok:
        print('  422 链残留按 SU(4) 权格重做（R13）：|det A| = %d、SNF %s ⇒ 中心类 %d 个；全候选群 '
              '%d 元 ⇒ %s；在场谱的核 |K| = %d（与 §11 的格指数 [P_422:P_10] = %s 同数）' %
              (G422['det'], 'x'.join(str(d) for d in G422['snf']), G422['ncls'],
               G422['ncand'], 'x'.join('Z%d' % d for d in G422['cstruct']),
               len(G422['K']), G422['idx_422']))
        print('    通道 %d 条、Q=0 权重 %d 个全部落在谱行（未落 %d）⇒ §10 的 %d 条 SM 单态类在每条'
              '通道无一改判；正向对照：全多重集 %d 条，两半交集 $=$ 全组允许按集合相等 %d/%d 条'
              '成立，例外 %s（交集 %d vs 逐元 %d）⇒ 对角型残群上半群读数严格粗于逐元读数' %
              (G422['nchan'], G422['nwt'], G422['unmatched'], G422['nsing'],
               G422['allc_tot'], sum(1 for c in G422['ctl'] if c['inter']),
               len(G422['ctl']),
               '、'.join(c['rep'] for c in G422['ctl'] if not c['inter']),
               [c['wcapc'] for c in G422['ctl'] if not c['inter']][0],
               [c['full'] for c in G422['ctl'] if not c['inter']][0]))
    if pw_ok:
        print('  行标号账与逐权重账（R14）：甲 %d 条条件 / 乙 %d 条（甲账没有 %d 条）⇒ 形变按集合'
              '相等 %s（各 %d 种）；核走三条算术路、两种约定都 = %d 且与 §11 逐元相等 ⇒ 换账不换群' %
              (G14['nspec'], G14['ncond'], G14['novel'], '是' if G14['eqAB'] else '**否**',
               G14['charA'], G14['gam']))
        print('    子多重态 %d 个、按子多重态去重权重 %d 条（按重数 %d 条、含行重数 %d 条 = 母表示维数和 %d 条）'
              '⇒ 三条恒等事违例 %d/%d/%d；冗余度：删一条即变大的 %d 条、贪心核心 %d 条、两条即钉住 '
              '%d/%d 对；$t$ 网格四档核恒 %d 个' %
              (G14['nsub'], G14['ndwt'], G14['nwtm'], G14['nwtmn'], G14['dimsum'],
               G14['bl_mis'], G14['root_mis'], G14['ph_mis'], G14['ess'], G14['core_len'],
               G14['pairs'], G14['pairs_tot'], G14['gam']))
    if bs_ok:
        print('  算符基覆盖面（R15）：字母表 %d 条（含 %d 条共轭）、%d 档、签名类 %d 条 ⇒ 位置类 %d '
              '条去重得之（碰撞 %d 组、组内读数全同 %s）；洛伦兹账三条同判（违例 %d/%d）⇒ 绝对禁 %d '
              '条、上移 %d 条、零导数 %d 条；指标禁与群禁在声明谱上集合相等（各 %d 条），插入奇 '
              '$3(B-L)$ 标量后双向分叉（$+144_H$：%d/%d）' %
              (len(BASIS['alpha']), sum(1 for a in BASIS['alpha'] if a[5]), BASIS['cover'][0],
               BASIS['cover'][1], BASIS['collide'][0], BASIS['collide'][3],
               '是' if BASIS['collide'][4] else '**否**', BASIS['parity'][0],
               BASIS['parity'][1], sum(v[1] for v in BASIS['prot_upl'].values()),
               sum(v[2] for v in BASIS['prot_upl'].values()),
               sum(v[3] for v in BASIS['prot_upl'].values()), BASIS['coin'][0],
               BASIS['ctl'][2]['onlyL'], BASIS['ctl'][2]['onlyZ']))
        print('    d>6 的轻子数破缺：$d=5$ 档 %d 条 $\\Delta L\\ne0$ 里 %d 条不碰 $\\nu^c$（共轭配对 '
              '%s）⇒ 具名 Weinberg 型 %s（$3Q=%s$、判决 %s、共轭孪生 %s）；$d=4$ 三费米子档 %d/%d 条'
              '全被洛伦兹账禁掉 ⇒ "轻子数破缺从 $d=5$ 起"是本层读数' %
              (BASIS['dl']['2,2'][1], BASIS['dl']['2,2'][2],
               '、'.join('%s:%d' % (k, v) for k, v in sorted(BASIS['dl']['2,2'][3].items())),
               ' + '.join(BASIS['wein'][0]), BASIS['wein'][1],
               '、'.join('允许' if x else '禁' for x in BASIS['wein'][4]), BASIS['wein'][5],
               BASIS['dl3'][1], BASIS['dl3'][0]))
        print('    类数→缩法重数（R16）：四路（$j\\pm1$ 递推／二项式差／钩长／显式 $SL(2)$ '
              '不变张量零空间）在 $0..%d$ 逐项相等（违例 %d 条）；%d 个可构建类共 %d 条缩法 '
              '⇒ 多重缩法 %d 类、最大重数 %d；§10 的 %d 条 $d=6$ 单态类**每一条** %d 条缩法 '
              '⇒ "8 条算符"是类数；塔往上每层 %s ⇒ 只数 $k_{\\min}$ 是有意的截断' %
              (BASIS['r16'][0], len(BASIS['r16'][2]) + len(BASIS['r16'][3]), BASIS['r16'][8],
               BASIS['r16tot'][3], BASIS['r16tot'][1], BASIS['r16tot'][2], len(BASIS['r16'][12]),
               BASIS['r16'][12][0][4],
               '、'.join(str(t[1]) for t in BASIS['r16'][10])))
        r7 = BASIS['r17']
        print('    缩法→Fermi 存活（R17）：三路（显式投影／$\\Lambda^m(\\mathbb C^2)$ 表示论／'
              'Grassmann 直接求值）在 $n\\le%d$ 的 %d 个 $(n,\\text{组大小})$ 用例上逐项相等'
              '（违例 %d 条、无重复名字退回缩法重数违例 %d 条）；锚点 两槽／四槽／两两／三对 $=%s$；'
              '$k_{\\min}=0$ 的 %d 类 %d 条缩法 ⇒ 存活 %d 条（吃掉 %d，$\\times%.4f$）：归零 %d、'
              '缩减 %d、不变 %d、判据看不见 %d、反而变大 %d、含三重同名 %d（与归零集合对称差 %d）；'
              '§10 那 8 类从 %d 条结构到 %d 条（归零 %d 类）' %
              (max(row[0] for row in r7[0]), len(r7[0]), len(r7[1]), len(r7[2]),
               '/'.join(str(x[0]) for x in r7[3]),
               sum(v[0] for v in r7[13].values()), r7[14][0], r7[14][1],
               r7[14][0] - r7[14][1], r7[14][1] / float(r7[14][0]),
               r7[14][2], r7[14][3], r7[14][4], r7[14][6], r7[14][7], r7[14][5], r7[18],
               sum(e[2] for e in r7[15]), sum(e[4] for e in r7[15]), len(r7[17][0])))
        r8 = BASIS['r18']
        print('    $\\varepsilon$ 道→$\\sigma$ 道换基（R18）：%d 个表格档上四数（预测／$\\varepsilon$ 秩／'
              '$\\sigma$ 单独秩／并秩）不全等 %d 档、新增结构 %d 条、道间关系合计 %d 条；锚点 同向÷$'
              '\\varepsilon$ $=%s$、交叉÷$\\varepsilon$ $=%s$、三生成元秩 %d、同名括号 %s；第三张票在 '
              '14.9 的 %d 类上复现存活 %d 条（逐类不等 %d 类、道单项式 %d 条）；摆放 %d 个违例 %d 类、'
              '并成合计 %d 条（比 14.9 大的类 %d 个 $=$ 构造伪影）；类集档 %s 覆盖 %d 类、界外 %s' %
              (r8[17], len(r8[1]), r8[12], r8[11], r8[16][0], r8[16][1], r8[16][2],
               '、'.join('掩码 %d 系数 %s' % (m, c) for m, c in r8[16][3]),
               r8[5], r8[3], len(r8[4]), r8[8], r8[6], len(r8[7]), r8[18], r8[19],
               '、'.join('$(%d,%d)$' % t for t in r8[21]), r8[9],
               '、'.join('%s %d' % (k, v) for k, v in sorted(r8[15].items()))))
    if nogo_ok:
        print('  判定：dim≤210 内唯一能破 B−L 而不破电磁的 Higgs = 126 / 126̄；'
              '120_H 虽含 (1,1,1)±2 但 |Q|=1 ⇒ 排除（报告 §4）')
    print('产出：SO10表示论报告.md / .json')
    return 0 if all_ok else 1


if __name__ == '__main__':
    sys.exit(main())
