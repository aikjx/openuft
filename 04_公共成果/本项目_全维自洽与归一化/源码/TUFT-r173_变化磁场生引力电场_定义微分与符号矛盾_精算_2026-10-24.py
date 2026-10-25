# -*- coding: utf-8 -*-
"""
TUFT-r173｜S17 核心公式 15「变化的磁场产生引力场和电场」—— dB/dt 方程是
          B=(V×E)/c² 的全导数，零预言，且第二项符号与自身推导矛盾

00. 编号与定位
  【编号】r173。实测首空号：全仓已占 r148..r172（r169=电磁引力互生层、
         r170=物理常数本源、r171=k′量纲、r172=光速飞行器，均并行线），r173 为首空号。
  【靶】S17/04_理论推导/核心公式集/15-变化的磁场产生引力场和电场/2.md（139 行）。
    核心主张（L71）：dB/dt = −A×E/c² − (V/c²)×dE/dt
    推导链（L55–71）：B=(V×E)/c² → 对 t 求导 → dV/dt=−A 代入。
  【问题】判「磁生引」是否第一性原理预言，还是把定义微分一遍。

01. 机读手段
  纯标准库；向量叉积；解析 V(t)、E(t) 全导数；
  恒等性（乘积法则残差机器零）；符号（按论文自身 dV/dt=−A，第二项应为 +，
  论文写 − ⇒ 与 LHS 差 2(V×dE/dt)/c²）；量纲四元组 (M,L,T,Q)；
  安培-麦克斯韦（∇×B）与 V×(∂E/∂t) 的结构对比（平面波显式场）。

02. 红线
  数学自洽 ≠ 实验证实；恒等式成立 ≠ 有新内容；靶自承优先。
"""

import io
import json
import math
import os
import random
import re
import sys
import time

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# ============================================================
# 路径 / 登记器
# ============================================================
BASE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(BASE, "04_公共成果", "本项目_全维自洽与归一化", "数据")
STEM = "TUFT-r173_变化磁场生引力电场_定义微分与符号矛盾_精算_2026-10-24"

ITEMS = []
CONTROLS = []
GUARDS = []


def add(iid, title, status, note="", **metrics):
    ITEMS.append({"id": iid, "title": title, "status": status,
                  "note": note, "metrics": metrics})


def control(cid, desc, value, expect, ok):
    CONTROLS.append({"id": cid, "desc": desc, "value": value,
                     "expect": expect, "ok": bool(ok)})


def guard(name, ok, detail=""):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})


def fs(x, n=6):
    try:
        return "%.*e" % (n, float(x))
    except Exception:
        return str(x)


def rel(x, y):
    m = max(abs(x), abs(y))
    return 0.0 if m == 0.0 else abs(x - y) / m


# ============================================================
# 向量工具
# ============================================================
def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def nrm(a):
    return math.sqrt(a[0] ** 2 + a[1] ** 2 + a[2] ** 2)


def vadd(a, b):
    return tuple(a[i] + b[i] for i in range(3))


def vscale(s, a):
    return tuple(s * a[i] for i in range(3))


# ============================================================
# 量纲四元组 (M,L,T,Q)
# ============================================================
def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dsub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dstr(d):
    names = ("M", "L", "T", "Q")
    parts = []
    for nm, e in zip(names, d):
        if e == 0:
            continue
        parts.append("%s^%d" % (nm, e))
    return "1" if not parts else " ".join(parts)


# 量纲四元组 (M, L, T, Q)，Q = 电流 A。全部按 SI 实测口径，不抄靶文。
D_A = (0, 1, -2, 0)       # 加速度 = m s^-2
D_E = (1, 1, -3, -1)      # 电场 V/m = kg m s^-3 A^-1
D_B = (1, 0, -2, -1)      # 特斯拉 T = kg s^-2 A^-1
D_DBDT = (1, 0, -3, -1)   # dB/dt = kg s^-3 A^-1
D_V = (0, 1, -1, 0)       # 速度 m s^-1
D_C2 = (0, 2, -2, 0)      # c²
D_DEDT = (1, 1, -4, -1)   # dE/dt = kg m s^-4 A^-1
# 安培-麦克斯韦两侧
D_CURL_B = (1, -1, -2, -1)   # ∇×B = kg m^-1 s^-2 A^-1
D_DISP = (1, -1, -2, -1)     # (1/c²)∂E/∂t


def dim_check():
    """返回逐条量纲判定（全部应与靶文 §4.1 的 kg·s^-3·A^-1 一致）。"""
    t_b_def = ddiv(dmul(D_V, D_E), D_C2)     # B=(V×E)/c² 的右端
    t_term1 = ddiv(dmul(D_A, D_E), D_C2)     # -A×E/c²
    t_term2 = ddiv(dmul(D_V, D_DEDT), D_C2)  # (V/c²)×dE/dt
    t_curl_b = ddiv(D_CURL_B, D_C2)          # ∇×B/c² 仅作参考
    t_amp = ddiv(D_DEDT, D_C2)               # (1/c²)∂E/∂t
    return {
        "b_def_ok": t_b_def == D_B,
        "t1_ok": t_term1 == D_DBDT,
        "t2_ok": t_term2 == D_DBDT,
        "ampere_ok": t_amp == D_CURL_B,
        "t1": dstr(t_term1),
        "t2": dstr(t_term2),
        "lhs": dstr(D_DBDT),
        "curl_b": dstr(D_CURL_B),
        "term2_as_object": dstr(t_term2),
        "curl_minus_term2": dstr(dsub(D_CURL_B, t_term2)),
        "amp_disp": dstr(t_amp),
        "curl_b_over_c2": dstr(t_curl_b),
    }


# ============================================================
# 10. 多项式精确求导 —— 恒等性判定不依赖差分步长
#     V(t)、E(t) 各分量取任意多项式；B(t) 由定义式 (1) 生成。
#     dB/dt 走「对 B(t) 本身求导」，RHS 走「乘积法则」，
#     两条路径在系数层比较 ⇒ 残差精确为 0 或精确非 0，无截断误差。
# ============================================================
C2 = 8.9875517873681764e16   # c² (m/s)², CODATA
C_LIGHT = 299792458.0


def pder(p):
    if len(p) <= 1:
        return [0.0]
    return [i * p[i] for i in range(1, len(p))]


def pmul(a, b):
    out = [0.0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x == 0.0:
            continue
        for j, y in enumerate(b):
            if y == 0.0:
                continue
            out[i + j] += x * y
    return out


def padd(a, b):
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0.0) + (b[i] if i < len(b) else 0.0)
            for i in range(n)]


def psub(a, b):
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0.0) - (b[i] if i < len(b) else 0.0)
            for i in range(n)]


def pscale(s, a):
    return [s * x for x in a]


def pvder(v):
    return tuple(pder(c) for c in v)


def pvscale(s, v):
    return tuple(pscale(s, c) for c in v)


def pvadd(a, b):
    return tuple(padd(a[i], b[i]) for i in range(3))


def pvsub(a, b):
    return tuple(psub(a[i], b[i]) for i in range(3))


def pcross(p, q):
    return (psub(pmul(p[1], q[2]), pmul(p[2], q[1])),
            psub(pmul(p[2], q[0]), pmul(p[0], q[2])),
            psub(pmul(p[0], q[1]), pmul(p[1], q[0])))


def pmaxabs(p):
    return max(abs(x) for x in p) if p else 0.0


def prel(a, b):
    m = max(pmaxabs(a), pmaxabs(b))
    if m == 0.0:
        return 0.0
    n = max(len(a), len(b))
    d = 0.0
    for i in range(n):
        x = a[i] if i < len(a) else 0.0
        y = b[i] if i < len(b) else 0.0
        d = max(d, abs(x - y))
    return d / m


def pvmaxabs(v):
    return max(pmaxabs(c) for c in v)


def pvreL(a, b):
    m = max(pvmaxabs(a), pvmaxabs(b))
    if m == 0.0:
        return 0.0
    d = 0.0
    for i in range(3):
        n = max(len(a[i]), len(b[i]))
        for k in range(n):
            x = a[i][k] if k < len(a[i]) else 0.0
            y = b[i][k] if k < len(b[i]) else 0.0
            d = max(d, abs(x - y))
    return d / m


def identity_residual(vfun, efun):
    """返回四个量：
       r4 = ‖dB/dt − (dV×E + V×dE)/c²‖   （= 论文式(3)/(4) 的正确符号）
       r5 = ‖dB/dt − (dV×E − V×dE)/c²‖   （= 论文式(5) 的符号）
       rg = ‖(式5 − 式4) − (−2 V×dE/dt/c²)‖
       gap = 式5 − 式4 的精确系数
    """
    dv = pvder(vfun)
    de = pvder(efun)
    bfun = pvscale(1.0 / C2, pcross(vfun, efun))
    dbdt = pvder(bfun)
    rhs_plus = pvscale(1.0 / C2, pvadd(pcross(dv, efun), pcross(vfun, de)))
    rhs_minus = pvscale(1.0 / C2, pvsub(pcross(dv, efun), pcross(vfun, de)))
    gap = pvsub(rhs_minus, rhs_plus)
    tgt = pvscale(-2.0 / C2, pcross(vfun, de))
    return (pvreL(dbdt, rhs_plus), pvreL(dbdt, rhs_minus),
            pvreL(gap, tgt), gap, de)


def rand_case(rng, dmax=3, lo=-2.0, hi=2.0):
    def pol():
        n = rng.randint(1, dmax + 1)
        return [rng.uniform(lo, hi) for _ in range(n)]
    return tuple(pol() for _ in range(3)), tuple(pol() for _ in range(3))


# ============================================================
# 11. 靶文自证：中间步骤符号 vs 最终式符号（同一文档内共存）
# ============================================================
TARGET = os.path.join(BASE, "01_独立体系", "S17_统一场论核心公式",
                      "04_理论推导", "核心公式集",
                      "15-变化的磁场产生引力场和电场", "2.md")

PAT_MINUS_V = (r'-\s*\\frac\{\\vec\{[vV]\}\}\{c\^\{2\}\}\s*\\times\s*'
               r'\\frac\{d\\vec\{E\}\}\{dt\}')
PAT_PLUS_V = (r'\+\s*\\vec\{[vV]\}\s*\\times\s*'
              r'\\frac\{d\\vec\{E\}\}\{dt\}')
PAT_DBDT = r'\\frac\{d\\vec\{B\}\}\{dt\}'

try:
    TXT = io.open(TARGET, "r", encoding="utf-8", errors="replace").read()
    N_LINES = TXT.count("\n") + 1
    N_DBDT = len(re.findall(PAT_DBDT, TXT))
    N_MINUS = len(re.findall(PAT_MINUS_V, TXT))
    N_PLUS = len(re.findall(PAT_PLUS_V, TXT))
    READ_OK = True
except Exception as exc:
    TXT, N_LINES, N_DBDT, N_MINUS, N_PLUS = "", 0, 0, 0, 0
    READ_OK = False
    print("[warn] 靶文读取失败: %s" % exc)

# ============================================================
# 12. 恒等性实测（40 组任意多项式 V(t)、E(t)）
# ============================================================
def pmed(xs):
    if not xs:
        return 0.0
    ys = sorted(xs)
    n = len(ys)
    if n % 2:
        return ys[n // 2]
    return 0.5 * (ys[n // 2 - 1] + ys[n // 2])


rng = random.Random(20261024)
N_CASE = 40
R4_MAX = 0.0
R5_MAX = 0.0
RG_MAX = 0.0
GAP_MAX = 0.0
R5_ALL = []
for _ in range(N_CASE):
    v_fun, e_fun = rand_case(rng)
    _r4, _r5, _rg, _gap, _de = identity_residual(v_fun, e_fun)
    R4_MAX = max(R4_MAX, _r4)
    R5_MAX = max(R5_MAX, _r5)
    RG_MAX = max(RG_MAX, _rg)
    GAP_MAX = max(GAP_MAX, pvmaxabs(_gap))
    R5_ALL.append(_r5)

add("A01",
    "式(3)/(4)（第二项 +）对任意 V(t)、E(t) 是定义式 B=(V×E)/c² 的全导数",
    "PASS",
    note="40 组任意多项式输入全部机器零 ⇒ 该式无独立物理内容（定义微分），"
         "不构成可证伪预言；PASS 的含义是「推导无误」，不是「物理成立」。",
    r4_max=fs(R4_MAX), n_case=N_CASE)

add("A02",
    "式(5)（第二项 −）与自身式(4) 不等价：符号在最后一步被翻转",
    "FAIL",
    note="同一推导链内 (4)→(5) 只做「整理」，第二项却从 + 变 −。"
         "机器判定：式(5) − 式(4) 恒等于 −2(V/c²)×(dE/dt)，非零。"
         "r5_max=2.0 是 V 恒定（dV/dt≡0）极限的取值，与 B01 一致；"
         "一般随机输入下中位数指标亦远大于机器零。",
    r5_max=fs(R5_MAX), r5_median=fs(pmed(R5_ALL)), gap_max=fs(GAP_MAX))

add("A03",
    "符号差的解析形式（机器零验证）",
    "PASS",
    note="式(5)−式(4) 与 −2(V×dE/dt)/c² 逐系数相等，残差 0 ⇒ 差异不是数值噪声，"
         "是确定的代数事实。",
    rg_max=fs(RG_MAX))

control("C01", "正控制：式(4) 应被判「恒等成立」", fs(R4_MAX), "<=1e-12",
        R4_MAX <= 1e-12)
def identity_residual_perturbed(vfun, efun, k=1.0 + 1e-3):
    """负控制：把第一项系数 1 → 1+1e-3，残差应显著非零。"""
    dv = pvder(vfun)
    de = pvder(efun)
    bfun = pvscale(1.0 / C2, pcross(vfun, efun))
    dbdt = pvder(bfun)
    rhs = pvscale(1.0 / C2, pvadd(pvscale(k, pcross(dv, efun)), pcross(vfun, de)))
    return pvreL(dbdt, rhs)


rng2 = random.Random(20261024)
PERT_LIST = []
N_PERT_SKIP = 0
for _ in range(N_CASE):
    v_fun, e_fun = rand_case(rng2)
    if pvmaxabs(pvder(v_fun)) == 0.0:
        # dV/dt ≡ 0 时第一项不存在，扰动不可见 —— 属预期退化，不计入负控制
        N_PERT_SKIP += 1
        continue
    _rp = identity_residual_perturbed(v_fun, e_fun)
    if _rp > 0.0:
        PERT_LIST.append(_rp)
PERT_MIN = min(PERT_LIST) if PERT_LIST else -1.0

control("C02", "负控制：第一项系数 1→(1+1e-3) 后必须被判失败（判据非恒真）",
        "min=%s med=%s (n=%d, 退化=%d)"
        % (fs(PERT_MIN), fs(pmed(PERT_LIST)), len(PERT_LIST), N_PERT_SKIP),
        "min>=1e-5", PERT_MIN >= 1e-5)
control("C03", "靶文内「+」形态与「−」形态共存，证明矛盾在文内而非跨文",
        "%d 处 + / %d 处 −" % (N_PLUS, N_MINUS), "两者均 >=1", N_PLUS >= 1 and N_MINUS >= 1)

# ============================================================
# 13. 符号错误的量级：V 恒定（dV/dt=0）时整式符号相反
# ============================================================
def pev(p, t):
    s = 0.0
    for c in reversed(p):
        s = s * t + c
    return s


def pvev(v, t):
    return tuple(pev(c, t) for c in v)


def vnorm(a):
    return math.sqrt(sum(x * x for x in a))


def rhs_paths(vfun, efun):
    dv = pvder(vfun)
    de = pvder(efun)
    bfun = pvscale(1.0 / C2, pcross(vfun, efun))
    return (pvder(bfun),
            pvscale(1.0 / C2, pvadd(pcross(dv, efun), pcross(vfun, de))),
            pvscale(1.0 / C2, pvsub(pcross(dv, efun), pcross(vfun, de))))


V_CONST = ([1.0e3], [0.0], [0.0])          # V = 1e3 x̂ m/s，恒定
E_LIN = ([0.0], [0.0, 1.0e12], [0.0])      # E = 1e12·t ŷ V/m

DBDT_C, RHS_PLUS_C, RHS_MINUS_C = rhs_paths(V_CONST, E_LIN)
SIGN_REL = 0.0
SIGN_ABS = 0.0
SIGN_MAG = 0.0
for _t in (0.0, 0.5, 1.0, 2.0):
    _a = pvev(DBDT_C, _t)
    _b = pvev(RHS_MINUS_C, _t)
    _d = vnorm(tuple(_a[i] - _b[i] for i in range(3)))
    _m = vnorm(_a)
    SIGN_ABS = max(SIGN_ABS, _d)
    SIGN_MAG = max(SIGN_MAG, _m)
    if _m > 0.0:
        SIGN_REL = max(SIGN_REL, _d / _m)

add("B01",
    "V 恒定时（dV/dt=0），式(5) 与精确 dB/dt 整式反号，相对误差 = 200%",
    "FAIL",
    note="普通装置（电磁铁、电容器、变压器）中 V 基本恒定、dV/dt≈0，"
         "精确式为 +（V×dE/dt)/c²，论文式(5) 给 −。"
         "这不是小修正，是整个右端符号反了。",
    rel_err=fs(SIGN_REL), abs_gap=fs(SIGN_ABS), mag=fs(SIGN_MAG))

# 绝对量级表：符号差 = 2|V||dE/dt|/c²（垂直），对照典型实验室 dB/dt = 1 T/s
SIGN_TABLE = []
for _label, _v, _dedt, _ref in (
        ("变压器/电机 V=1 m/s, dE/dt=1e10", 1.0, 1.0e10, 1.0),
        ("高速电机 V=1e3 m/s, dE/dt=1e12", 1.0e3, 1.0e12, 1.0),
        ("近光速源 V=1e5 m/s, dE/dt=1e12", 1.0e5, 1.0e12, 1.0),
        ("近光速源 V=1e5 m/s, dE/dt=1e14", 1.0e5, 1.0e14, 10.0)):
    _gap = 2.0 * _v * _dedt / C2
    SIGN_TABLE.append({"case": _label, "gap_T_per_s": fs(_gap),
                       "ref_dBdt": fs(_ref),
                       "ratio_to_ref": fs(_gap / _ref)})

add("B02",
    "符号差绝对量级（2V·dE/dt/c²）对照实验室典型 dB/dt",
    "INFO",
    note="V≥1e5 m/s 时符号差已达 O(1)~O(1e2) T/s，与常见磁场变化率同量级或更大 ⇒ "
         "该符号错误在被引用场景里不是可忽略项。",
    rows=len(SIGN_TABLE), max_gap=fs(SIGN_TABLE[-1]["gap_T_per_s"]))

# ============================================================
# 14. 量纲确权 + 安培-麦克斯韦结构对比
# ============================================================
DIM = dim_check()

add("C01",
    "量纲：LHS、两项、以及 B=(V×E)/c² 全部 = M L^0 T^-3 Q^-1（= kg·s⁻³·A⁻¹）",
    "PASS" if (DIM["b_def_ok"] and DIM["t1_ok"] and DIM["t2_ok"]) else "FAIL",
    note="靶文 §4.1 的量纲结论本身正确（三种路径独立复算一致）。"
         "但量纲自洽对「式(4)」和「式(5)」同时成立（符号不含量纲）⇒ "
         "量纲检验对该符号错误零判别力。",
    lhs=DIM["lhs"], t1=DIM["t1"], t2=DIM["t2"])

add("C02",
    "「第二项 = 位移电流项」结构不符：∇×B 与 (V/c²)×∂E/∂t 相差 L^-1·T^1",
    "FAIL",
    note="∇×B = %s，而 (V/c²)×∂E/∂t = %s，差 = %s = 1/(速度)。"
         "∇× 是空间导数（降 L^-1），V× 是代数乘（不动 L）。"
         "要补齐必须引入一个长度/波矢，即 V 不再是「场源速度」——"
         "这与 §2 对 V 的定义直接冲突。安培侧的量纲本身是自洽的（DISP = %s = ∇×B），"
         "错的是把「时间导数」当成「旋度」。"
         % (DIM["curl_b"], DIM["term2_as_object"], DIM["curl_minus_term2"],
            DIM["amp_disp"]),
    curl_b=DIM["curl_b"], term2=DIM["term2_as_object"],
    diff=DIM["curl_minus_term2"],
    amp_ok=DIM["ampere_ok"])

PLANE_V = 1.0e3
PLANE_SIN_REQ = C_LIGHT / PLANE_V

add("C03",
    "B=(V×E)/c² 复现平面波（|B|=|E|/c）要求 |V|sinθ = c，亚光速源无解",
    "BOUNDARY",
    note="|V|=1e3 m/s 时需 sinθ = %.3e ≫ 1，超出定义域 ⇒ "
         "该定义式只能描述亚光速源的准静态场，不能描述辐射场；"
         "因此不能据此把 (V/c²)×∂E/∂t 认作位移电流。" % PLANE_SIN_REQ,
    sin_required=fs(PLANE_SIN_REQ), v=fs(PLANE_V))

# ============================================================
# 15. 实验证据：§4.3 有无真实代入 + 量级二难
# ============================================================
_i0 = TXT.find("## 4.3")
_i1 = TXT.find("# 5. 结论")
SEC43 = TXT[_i0:_i1] if (_i0 >= 0 and _i1 > _i0) else ""
NUMS43 = re.findall(r'\d+(?:\.\d+)?', SEC43)
EQ_IN_SEC43 = SEC43.count("=")
HAS_5PCT = ("误差<5%" in SEC43) or ("误差 <5%" in SEC43)
SEC43_LEN = len(SEC43)

add("D01",
    "§4.3 宣称 Z 箍缩「误差<5%」，但全节零处数值代入（无 dB/dt、无 E、无 A）",
    "FAIL" if EQ_IN_SEC43 == 0 else "BOUNDARY",
    note="§4.3 全节 %d 字符、数值字面量 %d 个（仅 ~10^6 m/s² 一个量级）、"
         "等号 %d 个 ⇒ 没有任何一个量被代入方程，"
         "「误差<5%%」在任何口径下都无法复算，属不可检验的断言。"
         % (SEC43_LEN, len(NUMS43), EQ_IN_SEC43),
    sec_len=SEC43_LEN, num_literals=len(NUMS43),
    eq_signs=EQ_IN_SEC43, has_5pct=HAS_5PCT)

E_SCH = 1.323e18      # QED 临界场 V/m
E_LASER = 1.0e14      # 强激光可达场量级 V/m
G_ACC = 9.80665
A_REF = 1.0e6         # 靶文引用的向心加速度量级 m/s²

# 15.1 「生成」读法：给定实验室级 E 与 dB/dt，式(5) 预言多大的 A
GEN_ROWS = []
for _e, _db in ((1.0e6, 1.0), (1.0e6, 1.0e3), (1.0e4, 1.0e3)):
    _a = C2 * _db / _e
    GEN_ROWS.append({"E_V_m": fs(_e), "dBdt_T_s": fs(_db),
                     "A_m_s2": fs(_a), "A_in_g": fs(_a / G_ACC)})

add("D02",
    "「生成」读法下式(5) 对普通装置预言 A ~ 1e10–1e16 m/s²（1e9–1e15 g），与全部实验矛盾",
    "FAIL",
    note="把式(5) 当因果律反解 A = −c²(dB/dt)/E：耦合常数含 1/E，"
         "E 越小预言越大。取实验室常规值（E=1e6 V/m, dB/dt=1 T/s）即得 A≈%.2e m/s² ≈ %.1e g。"
         "任何电磁铁都会产生天文量级引力加速度而从未观测到 ⇒ "
         "该读法不是「待验证的新预言」，而是已被日常实验量级排除。"
         % (C2 * 1.0 / 1.0e6, C2 * 1.0 / 1.0e6 / G_ACC),
    rows=len(GEN_ROWS), max_in_g=GEN_ROWS[1]["A_in_g"])

ZP_ROWS = []
for _db in (1.0e6, 1.0e9, 1.0e12):
    _ereq = C2 * _db / A_REF
    ZP_ROWS.append({"dBdt_T_s": fs(_db), "E_req_V_m": fs(_ereq),
                    "over_schwinger": fs(_ereq / E_SCH),
                    "over_laser": fs(_ereq / E_LASER)})

add("D03",
    "反向：要由第一项产生 A=1e6 m/s²，所需 E 远超强激光，dB/dt≥1e9 T/s 时超 QED 临界场",
    "FAIL",
    note="A=1e6 m/s²、dB/dt=1e6 T/s ⇒ 需 E≈%.2e V/m（强激光 %.0e V/m 的 %.0f 倍）；"
         "dB/dt=1e9 T/s ⇒ 需 E≈%.2e V/m = QED 临界场 1.323e18 V/m 的 %.1f 倍 ⇒ "
         "真空已被击穿，该场景内方程前提失效。靶文引用的 Z 箍缩正好落在后者。"
         % (C2 * 1.0e6 / A_REF, E_LASER, C2 * 1.0e6 / A_REF / E_LASER,
            C2 * 1.0e9 / A_REF, C2 * 1.0e9 / A_REF / E_SCH),
    rows=len(ZP_ROWS))

add("D04",
    "二难：作为恒等式 ⇒ 零预言；作为生成律 ⇒ 量级被日常实验排除",
    "FAIL",
    note="两条读法都不可救：①B 由 (V×E)/c² 定义 ⇒ 式(5) 是定义的全导数，"
         "测量 dB/dt 无法否证它（恒等式不可能被实验推翻），故「磁生引」不是预言；"
         "②若把 A 当输出，则 D02/D03 给出 1e9–1e15 g 的荒谬值。"
         "靶文同时使用两种读法（§4.2 称「全新预言」，§3 称「逻辑必然导出」），"
         "二者互斥。")

# ============================================================
# 16. 守卫 / 汇总 / 落盘
# ============================================================
guard("G1 量纲四元组：B 定义式、两项、安培位移电流全部自洽",
      DIM["b_def_ok"] and DIM["t1_ok"] and DIM["t2_ok"] and DIM["ampere_ok"],
      "lhs=%s t1=%s t2=%s" % (DIM["lhs"], DIM["t1"], DIM["t2"]))
guard("G2 恒等性（正确符号）机器零", R4_MAX <= 1e-12, "r4_max=%s" % fs(R4_MAX))
guard("G3 符号差解析式 (5)−(4) = −2V×dE/dt/c² 机器零", RG_MAX <= 1e-12,
      "rg_max=%s gap_max=%s" % (fs(RG_MAX), fs(GAP_MAX)))
guard("G4 符号错误在 V 恒定时使相对误差达 200%",
      abs(SIGN_REL - 2.0) <= 1e-2, "rel=%s" % fs(SIGN_REL))
guard("G5 负控制有效：扰动 1e-3 即被检出（退化 dV/dt≡0 的样例已剔除）",
      PERT_MIN >= 1e-5,
      "pert_min=%s n=%d skip=%d" % (fs(PERT_MIN), len(PERT_LIST), N_PERT_SKIP))
guard("G6 靶文内「+」与「−」两种形态共存（矛盾在文内）",
      (N_PLUS >= 1) and (N_MINUS >= 1), "plus=%d minus=%d" % (N_PLUS, N_MINUS))
guard("G7 §4.3 无任何数值代入（等号 0 个）", EQ_IN_SEC43 == 0,
      "eq_signs=%d nums=%d" % (EQ_IN_SEC43, len(NUMS43)))
guard("G8 安培结构差非零且恰为 L^-1·T^1", DIM["curl_minus_term2"] == "L^-1 T^1",
      "diff=%s" % DIM["curl_minus_term2"])
guard("G9 判定条目数 = 12（A01–D04）", len(ITEMS) == 12, "items=%d" % len(ITEMS))


def summarize():
    cnt = {}
    for it in ITEMS:
        cnt[it["status"]] = cnt.get(it["status"], 0) + 1
    return cnt


class Tee(object):
    """同时写控制台与 _report.txt，保持两者逐字一致。"""

    def __init__(self, *streams):
        self.streams = streams

    def write(self, s):
        for st in self.streams:
            try:
                st.write(s)
            except Exception:
                pass
        return len(s)

    def flush(self):
        for st in self.streams:
            try:
                st.flush()
            except Exception:
                pass


def main():
    t0 = time.time()
    cnt = summarize()
    _rp = os.path.join(OUT, STEM + "_report.txt")
    _orig = sys.stdout
    _rf = None
    try:
        os.makedirs(OUT, exist_ok=True)
        _rf = io.open(_rp, "w", encoding="utf-8")
        sys.stdout = Tee(_orig, _rf)
    except Exception:
        _rf = None
    print("=" * 78)
    print("TUFT-r173｜S17-15 变化磁场产生引力场与电场 —— 定义微分与符号矛盾")
    print("=" * 78)
    print("靶文: %s" % TARGET)
    print("读取: %s  行数=%d  dB/dt 记号=%d  式(5)形态=%d  式(3)/(4)形态=%d"
          % ("OK" if READ_OK else "FAIL", N_LINES, N_DBDT, N_MINUS, N_PLUS))
    print("-" * 78)
    for it in ITEMS:
        print("[%s] %s  %s" % (it["status"], it["id"], it["title"]))
        if it["note"]:
            print("       · %s" % it["note"])
        if it["metrics"]:
            kv = ", ".join("%s=%s" % (k, v) for k, v in sorted(it["metrics"].items()))
            print("       · %s" % kv)
    print("-" * 78)
    print("符号差绝对量级表（2|V||dE/dt|/c²，垂直）:")
    for r in SIGN_TABLE:
        print("  %-34s gap=%-12s vs 参照 %-8s => %s x"
              % (r["case"], r["gap_T_per_s"], r["ref_dBdt"], r["ratio_to_ref"]))
    print("「生成」读法（A = c²·dB/dt / E）:")
    for r in GEN_ROWS:
        print("  E=%-10s dB/dt=%-10s => A=%-12s m/s² = %s g"
              % (r["E_V_m"], r["dBdt_T_s"], r["A_m_s2"], r["A_in_g"]))
    print("Z 箍缩所需 E（A=1e6 m/s²）:")
    for r in ZP_ROWS:
        print("  dB/dt=%-10s => E_req=%-12s V/m  = %s x Schwinger, %s x 强激光"
              % (r["dBdt_T_s"], r["E_req_V_m"],
                 r["over_schwinger"], r["over_laser"]))
    print("-" * 78)
    for c in CONTROLS:
        print("  [ctl%s] %-46s 值=%-16s 期望=%-10s"
              % ("OK" if c["ok"] else "NG", c["desc"][:46], c["value"], c["expect"]))
    for g in GUARDS:
        print("  [grd%s] %-52s %s"
              % ("OK" if g["ok"] else "NG", g["name"][:52], g["detail"]))
    n_guard_ok = sum(1 for g in GUARDS if g["ok"])
    n_ctl_ok = sum(1 for c in CONTROLS if c["ok"])
    print("-" * 78)
    print("条目 %d：%s" % (len(ITEMS),
                          "  ".join("%s=%d" % (k, cnt[k]) for k in sorted(cnt))))
    print("控制 %d/%d   守卫 %d/%d   用时 %.2fs"
          % (n_ctl_ok, len(CONTROLS), n_guard_ok, len(GUARDS), time.time() - t0))

    payload = {
        "stem": STEM,
        "round": "r173",
        "target": TARGET,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "text_scan": {"lines": N_LINES, "dbdt_token": N_DBDT,
                      "eq5_minus_form": N_MINUS, "eq3_eq4_plus_form": N_PLUS},
        "verdict": {
            "core": "式(5) 是定义式 B=(V×E)/c² 的全导数（零预言），"
                    "且第二项符号在其自身推导 (4)→(5) 一步被翻转为错。",
            "defects": ["定义微分恒等式（零预言）",
                        "第二项符号与自身推导矛盾（式4 为 +，式5 为 −）",
                        "「位移电流项」结构不符（∇×B vs V×∂E/∂t 差 L^-1·T^1）",
                        "实验「误差<5%」零数值代入",
                        "生成读法量级被日常实验排除（1e9–1e15 g）"],
        },
        "sign_table": SIGN_TABLE,
        "generate_table": GEN_ROWS,
        "zpinch_requirement": ZP_ROWS,
        "constants": {"c2": C2, "E_schwinger": E_SCH,
                      "E_strong_laser": E_LASER, "g": G_ACC},
        "items": ITEMS,
        "controls": CONTROLS,
        "guards": GUARDS,
        "counts": cnt,
        "guard_ok": "%d/%d" % (n_guard_ok, len(GUARDS)),
        "control_ok": "%d/%d" % (n_ctl_ok, len(CONTROLS)),
    }
    try:
        os.makedirs(OUT, exist_ok=True)
        jp = os.path.join(OUT, STEM + ".json")
        with io.open(jp, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2, default=str)
        print("JSON  -> %s" % jp)

        mp = os.path.join(OUT, STEM + ".md")
        lines = []
        lines.append("# TUFT-r173 精算摘要")
        lines.append("")
        lines.append("- 靶：`%s`" % TARGET)
        lines.append("- 条目：%s" % "  ".join("%s=%d" % (k, cnt[k]) for k in sorted(cnt)))
        lines.append("- 控制：%d/%d　守卫：%d/%d"
                     % (n_ctl_ok, len(CONTROLS), n_guard_ok, len(GUARDS)))
        lines.append("")
        lines.append("| 编号 | 状态 | 判定 |")
        lines.append("|---|---|---|")
        for it in ITEMS:
            lines.append("| %s | %s | %s |"
                         % (it["id"], it["status"],
                            it["title"].replace("|", "\\|")))
        lines.append("")
        lines.append("## 符号差量级")
        lines.append("")
        lines.append("| 场景 | 2V·dE/dt/c² (T/s) | 参照 dB/dt | 比值 |")
        lines.append("|---|---|---|---|")
        for r in SIGN_TABLE:
            lines.append("| %s | %s | %s | %s |"
                         % (r["case"], r["gap_T_per_s"], r["ref_dBdt"],
                            r["ratio_to_ref"]))
        lines.append("")
        lines.append("## 生成读法（A = c²·dB/dt / E）")
        lines.append("")
        lines.append("| E (V/m) | dB/dt (T/s) | A (m/s²) | A (g) |")
        lines.append("|---|---|---|---|")
        for r in GEN_ROWS:
            lines.append("| %s | %s | %s | %s |"
                         % (r["E_V_m"], r["dBdt_T_s"], r["A_m_s2"], r["A_in_g"]))
        lines.append("")
        lines.append("## Z 箍缩所需 E（A=1e6 m/s²）")
        lines.append("")
        lines.append("| dB/dt (T/s) | 需 E (V/m) | / Schwinger | / 强激光 |")
        lines.append("|---|---|---|---|")
        for r in ZP_ROWS:
            lines.append("| %s | %s | %s | %s |"
                         % (r["dBdt_T_s"], r["E_req_V_m"],
                            r["over_schwinger"], r["over_laser"]))
        lines.append("")
        with io.open(mp, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print("MD    -> %s" % mp)
    except Exception as exc:
        print("[warn] 落盘失败: %s" % exc)

    try:
        sys.stdout = _orig
        if _rf is not None:
            _rf.close()
            print("REPORT-> %s" % _rp)
    except Exception:
        pass

    return 0 if n_guard_ok == len(GUARDS) else 1


if __name__ == "__main__":
    sys.exit(main())
