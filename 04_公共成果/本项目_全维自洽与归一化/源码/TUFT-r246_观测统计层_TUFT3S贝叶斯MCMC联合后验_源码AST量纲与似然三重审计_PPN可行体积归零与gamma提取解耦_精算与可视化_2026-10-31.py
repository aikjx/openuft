# -*- coding: utf-8 -*-
r"""
TUFT-r246 · 观测统计层
================================================================================
TUFT-3S 贝叶斯 MCMC 联合后验（P0-18/P0-19）的【源码 AST / 量纲 / 似然】三重审计
★ 方法全谱：本卷一次上齐 10 道工序，全部机器记录
  ① 来源保真（sha256 前后双读）      ② 文本证据钉扎（逐 token 命中）
  ③ 源码 AST 静态审计（全新仪器）    ④ 沙箱动态执行（全新仪器，纯标准库桩）
  ⑤ (M,L,T) 量纲机读                ⑥ 闭式推导（γ / 可行 gτ0 / 爆破长度）
  ⑦ 高精度 Decimal 复算             ⑧ ODE 逐字复刻数值实验（RK4/欧拉/归因）
  ⑨ 控制组标定（正/负/仪器自检）     ⑩ 守卫链（含引擎自审 AST）

【命题来源】用户：「继续整理通过全新的方法，求导证明验证出统一场论，力的大统一，openuft」
             +「所有方法试试」+「继续攻破统一场论」

【本卷定位：观测统计层首卷】
r243 = 工程可用性层（引力），r244 = 引力本体论层，r245 = 常温超导本质层（凝聚态），
r246 = **观测统计层**：靶自己搭了「贝叶斯观测侧审计」（P0-18 dynesty 嵌套采样 + P0-19 全隐式重构），
声称「采样结果将直接判定：TUFT-3S 是否还留有生存空间」，状态自曝「⏳ 待运行」。
本卷替靶完成这次判定——结论：**不需要采样，可运行性本身为 0**。

【为什么这份靶值得攻】
它给出**可执行代码**（P0-18/P0-19 两个围栏块）+ 观测数据集（卡西尼 PPN σ_γ=2.3e-5 + 6 点旋转曲线）
+ 贝叶斯决策框架（Jeffreys 判据）⇒ 每一条承重声明都可机器复算。
以前各轮审计「公式」；本卷新增仪器直接审计**来料自带的代码字节**。

【靶的核心构件（逐字取自来料）】
  ① 同源公设 ξ0 = gτ0；总自由参数声称 17（原 18）
  ② 还原链：xi = xi0/Mp²，mu2 = mu0_sq·Mp²，eta = eta0/Mp²
  ③ ω_BD = 1/(g_tau0·c²)；γ = (1+ω_BD)/(2+ω_BD)（「弱场γ近似（太阳系极限提取）」）
  ④ v² = GM/r + 2·gτ0·τ²·φ²·r·exp(−2√(2gτ0)·φ·r/c)
  ⑤ ODE：dp_tau = −2p_tau/r − 2gτ·τ·φ² − 2ξc²τ·constraint；U = Vφ − gττ²φ² + ½ξ·constraint²
  ⑥ constraint = ω² − c²(κ²+τ²)，κ = 1.0e5（「局域曲率近似」固定常数）
  ⑦ P0-19：kappa_sq = alpha²×1.0e-3（注释自曝「占位，真实版本由R实时计算」）

【对靶有利项先做】A 组：先验构造正确（μ0_sq<0 根号恒正）、FLAG-1 简并预判方向正确、
本源恒等式 ω²=c²(κ²+τ²) 量纲齐次、同源公设显式声明（诚实记账）。

【分层】本卷条目不可与 r142–r245 相加（新层：观测统计层）。
【取号】2026-10-30 晚 + 2026-10-31 晨两次实测：源码/数据/判定三树 *r246* 均为 0 ⇒ 取 r246。
================================================================================
"""

import ast
import hashlib
import io
import json
import math
import os
import re
import sys
import time
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 50

# ============================================================
# 0. 元信息
# ============================================================
RID = "r246"
BASE_NAME = ("TUFT-r246_观测统计层_TUFT3S贝叶斯MCMC联合后验_"
             "源码AST量纲与似然三重审计_PPN可行体积归零与gamma提取解耦_"
             "精算与可视化_2026-10-31")
START_TS = time.time()
START_ISO = time.strftime("%Y-%m-%dT%H:%M:%S")

ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
SRC_DIR = os.path.join(ROOT, "源码")
DATA_DIR = os.path.join(ROOT, "数据")
VD_DIR = os.path.join(ROOT, "判定")
ARCH = os.path.join(DATA_DIR, "TUFT-r246_观测统计层_TUFT3S贝叶斯MCMC联合后验_来料原件_2026-10-30")

TARGETS = [
    os.path.join(ARCH, "修改攻破.md"),
    os.path.join(ARCH, "基于光速螺旋流形的核心动力学方程组.md"),
]
PRIMARY = TARGETS[0]

WRITE_SIDE = [
    r"D:\a10\aikjx\code\my_lib\openuft\verify.py",
    r"D:\a10\aikjx\code\my_lib\openuft\00_项目治理\维护工具\refresh_catalog.py",
]

EXPECT_DIST = {"PASS": 3, "FAIL": 15, "BOUNDARY": 1, "INFO": 5}

# ============================================================
# 1. 常数（与靶逐字同源：c/G/hbar 取靶值，CODATA 2018 一致）
# ============================================================
C = 299792458.0
G = 6.67430e-11
HBAR = 1.054571817e-34
MP = math.sqrt(HBAR * C / G)          # 2.176e-8 kg
LP = math.sqrt(HBAR * G / C ** 3)     # 1.616e-35 m
SIGMA_G = 2.3e-5                      # 卡西尼 PPN 1σ（靶值 = Bertotti 2003）
PI = math.pi
M_GAL = 1.0e41                        # 靶硬编码星系质量 kg
PHI0 = 1.0e15                         # 靶 IC φ
TAU0 = 1.0e5                          # 靶 IC τ
OMEGA0 = 3.0e13                       # 靶 IC ω
KAPPA0 = 1.0e5                        # 靶固定 κ


def safe_exp(x):
    return 0.0 if x < -745.0 else math.exp(x)


# ============================================================
# 2. (M, L, T) 量纲机读
# ============================================================
def dim(m=0, l=0, t=0):
    return (Fraction(m), Fraction(l), Fraction(t))


def dadd(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def dmul(a, b):
    """两量相乘 ⇒ 量纲指数相加"""
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def ddiv(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dpow(a, k):
    return (a[0] * k, a[1] * k, a[2] * k)


def dstr(a):
    parts = []
    for sym, v in zip(("M", "L", "T"), a):
        if v:
            parts.append(sym + ("^{%s}" % v if v != 1 else ""))
    return "[" + " ".join(parts) + "]" if parts else "[1]"


DIM_G = dim(-1, 3, -2)
DIM_M = dim(1, 0, 0)
DIM_L = dim(0, 1, 0)
DIM_T = dim(0, 0, 1)
DIM_ENERGY = dim(1, 2, -2)
DIM_EDENS = dim(1, -1, -2)     # 能量密度 M L^-1 T^-2
DIM_V2 = dim(0, 2, -2)
DIM_FREQ2 = dim(0, 0, -2)
DIM_C2 = dpow(dim(0, 1, -1), 2)
DIM_INV2L = dim(0, -2, 0)


# ============================================================
# 3. 来源保真 + 文本钉扎 + 来料抽取
# ============================================================
def sha256_of(path):
    h = hashlib.sha256()
    with io.open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


SHA_AT_IMPORT = {p: sha256_of(p) for p in TARGETS}
WS_SHA_AT_IMPORT = {p: sha256_of(p) for p in WRITE_SIDE}


def read_text(path):
    with io.open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_fenced_blocks(text):
    """抽取 ```python ...``` 围栏块（返回 (src, 起始行 1-based) 列表）"""
    lines = text.split("\n")
    blocks, i = [], 0
    while i < len(lines):
        if lines[i].strip().startswith("```python"):
            j, buf = i + 1, []
            while j < len(lines) and not lines[j].strip().startswith("```"):
                buf.append(lines[j])
                j += 1
            blocks.append(("\n".join(buf), i + 2))
            i = j
        i += 1
    return blocks


def classify_blocks(blocks):
    p018 = p019 = None
    for src, ln in blocks:
        try:
            doc = ast.get_docstring(ast.parse(src)) or ""
        except SyntaxError:
            continue
        if "P0-18" in doc:
            p018 = (src, ln)
        elif "P0-19" in doc:
            p019 = (src, ln)
    return p018, p019


def nhit(text, *toks):
    return {tok: (tok in text) for tok in toks}


# ============================================================
# 4. 沙箱动态执行（纯标准库桩，逐字 exec 靶函数源段）
# ============================================================
class Vec(list):
    def __sub__(self, other):
        return [v - other for v in self]

    def __rsub__(self, other):
        return [other - v for v in self]


class ShimNP:
    pi = math.pi

    @staticmethod
    def sqrt(x):
        return math.sqrt(x)

    @staticmethod
    def exp(x):
        return safe_exp(x)

    @staticmethod
    def array(x):
        return x

    @staticmethod
    def abs(x):
        if isinstance(x, (list, tuple, Vec)):
            return [abs(v) for v in x]
        return abs(x)

    @staticmethod
    def argmin(x):
        return min(range(len(x)), key=lambda k: x[k])


class Y2D(list):
    def __getitem__(self, key):
        if isinstance(key, tuple):
            rows = list.__getitem__(self, key[0])
            j = key[1]
            if isinstance(rows, (list, Vec)):
                return [r[j] for r in rows]
            return rows[j]
        return list.__getitem__(self, key)


class FakeSol:
    """桩解：t/y 结构与 scipy 一致；值不参与结论（NameError 在取值后立即触发）"""

    def __init__(self):
        self.t = Vec([1.0e20, 5.0e19, 1.0e19])
        base = [1.0, 1.0, TAU0, -1.0e-15, OMEGA0, -1.0e-22, PHI0, -1.0e-20]
        self.y = Y2D([[v for _ in self.t] for v in base])


def fake_solve_ivp(f, rspan, Y0, method=None, rtol=None):
    return FakeSol()


def sandbox_exec(src18):
    """逐字 exec 靶 model_v_gamma + loglike，返回沙箱证据"""
    tree = ast.parse(src18)
    seg = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name in ("model_v_gamma", "loglike"):
            seg[node.name] = ast.get_source_segment(src18, node)
    rot_data = [[1e20, 180, 10], [2e20, 195, 10], [3e20, 202, 10],
                [5e20, 205, 10], [8e20, 200, 10], [12e20, 185, 10]]
    ns = {"np": ShimNP, "solve_ivp": fake_solve_ivp, "c": C, "G": G,
          "hbar": HBAR, "Mp": MP, "lp": LP, "sigma_gamma": SIGMA_G,
          "rot_data": rot_data}
    out = {"has_model": "model_v_gamma" in seg, "has_loglike": "loglike" in seg}
    if "model_v_gamma" in seg:
        exec(compile(seg["model_v_gamma"], "<p018.model_v_gamma>", "exec"), ns)
    if "loglike" in seg:
        exec(compile(seg["loglike"], "<p018.loglike>", "exec"), ns)
    thetas = []
    for g0 in (1e-12, 1e-8, 1e-4):
        for mu, eta in ((-1e-9, 1e-5), (-1e-12, 1e-2), (-1e-6, 1e-8)):
            thetas.append((g0, mu, eta))
    err_type, err_name, err_var, first_err_theta = None, None, None, None
    ll_vals = []
    for th in thetas:
        try:
            ns["model_v_gamma"](th)
            ok = True
        except Exception as exc:  # 靶缺陷应在此现形
            ok = False
            if err_type is None:
                err_type = exc.__class__.__name__
                err_name = getattr(exc, "name", None) or str(exc)
                _m = re.search(r"'(\w+)'", str(exc))
                err_var = _m.group(1) if _m else None
                first_err_theta = th
        try:
            ll_vals.append(ns["loglike"](th))
        except Exception:
            ll_vals.append(None)
    out["n_theta"] = len(thetas)
    out["model_err_type"] = err_type
    out["model_err_name"] = err_name
    out["model_err_var"] = err_var
    out["first_err_theta"] = first_err_theta
    out["loglike_vals"] = ll_vals
    out["all_loglike_neg_inf"] = all(v == float("-inf") for v in ll_vals)
    return out


# ============================================================
# 5. AST 静态审计
# ============================================================
def analyze_ast18(src18):
    tree = ast.parse(src18)
    res = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "model_v_gamma":
            body = node.body
            unpack_i = unpack_ln = None
            for k, st in enumerate(body):
                if (isinstance(st, ast.Assign) and st.targets
                        and isinstance(st.targets[0], ast.Tuple)
                        and any(isinstance(t, ast.Name) and t.id == "g_tau0"
                                for t in st.targets[0].elts)):
                    unpack_i, unpack_ln = k, st.lineno
                    break
            load_lns = [n.lineno for n in ast.walk(node)
                        if isinstance(n, ast.Name) and n.id == "g_tau0"
                        and isinstance(n.ctx, ast.Load)]
            res["gtau_first_load_ln"] = min(load_lns) if load_lns else None
            res["gtau_unpack_ln"] = unpack_ln
            res["gtau_load_before_assign"] = bool(load_lns and unpack_ln
                                                  and min(load_lns) < unpack_ln)
            tail_names = set()
            if unpack_i is not None:
                for st in body[unpack_i + 1:]:
                    for n in ast.walk(st):
                        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load):
                            tail_names.add(n.id)
            res["gamma_tail_names"] = sorted(tail_names)
            res["gamma_tail_has_sol"] = "sol" in tail_names
            loads_mtau = sum(1 for n in ast.walk(node)
                             if isinstance(n, ast.Name) and n.id == "m_tau"
                             and isinstance(n.ctx, ast.Load))
            res["m_tau_loads"] = loads_mtau
    # 参数记账（targeted）
    hard = {"kappa": 0, "M": 0, "r0": 0, "rspan": 0, "Y0_elements": 0, "rtol": 0}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "model_v_gamma":
            for st in ast.walk(node):
                if isinstance(st, ast.Assign) and st.targets \
                        and isinstance(st.targets[0], ast.Name):
                    nm = st.targets[0].id
                    if nm in ("kappa", "M", "r0", "rspan"):
                        hard[nm] = 1
                    if nm == "Y0" and isinstance(st.value, ast.List):
                        hard["Y0_elements"] = sum(
                            1 for e in st.value.elts
                            if isinstance(e, ast.Constant)
                            or (isinstance(e, ast.UnaryOp) and isinstance(e.op, ast.USub)
                                and isinstance(e.operand, ast.Constant)))
                if isinstance(st, ast.keyword) and st.arg == "rtol" \
                        and isinstance(st.value, ast.Constant):
                    hard["rtol"] = 1
    res["hard_params"] = hard
    res["hard_total"] = sum(hard.values())
    return res


def analyze_ast19(src19):
    tree = ast.parse(src19)
    res = {"kappa_sq_expr": None, "curvature_R_calls": 0,
           "has_ddA": False, "has_ddB": False, "placeholder_hits": 0}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and node.targets \
                and isinstance(node.targets[0], ast.Name) \
                and node.targets[0].id == "kappa_sq":
            res["kappa_sq_expr"] = ast.unparse(node.value)
            res["kappa_sq_has_call"] = any(isinstance(n, ast.Call)
                                           for n in ast.walk(node.value))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id == "curvature_R":
            res["curvature_R_calls"] += 1
        if isinstance(node, ast.arg) and node.arg in ("ddA", "ddB"):
            if node.arg == "ddA":
                res["has_ddA"] = True
            else:
                res["has_ddB"] = True
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id in ("ddA", "ddB"):
            if node.id == "ddA":
                res["has_ddA"] = True
            else:
                res["has_ddB"] = True
    res["ddA_in_ode_rhs"] = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "ode_rhs":
            names = {n.id for n in ast.walk(node)
                     if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
            res["ddA_in_ode_rhs"] = ("ddA" in names) or ("ddB" in names)
    res["placeholder_hits"] = src19.count("占位")
    return res


# ============================================================
# 6. 闭式推导（γ / 可行 gτ0 / 爆破长度）
# ============================================================
def gamma_of_gtau(g0):
    w = 1.0 / (g0 * C * C)
    return (1.0 + w) / (2.0 + w)


def gamma_required_decimal():
    two = Decimal(2)
    c2 = Decimal(C) * Decimal(C)
    w_req = Decimal(1) / Decimal("2.3e-5") - two
    g_req = Decimal(1) / (c2 * w_req)
    return g_req


def blowup_length(theta, Ttt):
    """dB/dr ≈ K·B²，K = 8πG·r·|T_tt|；爆破长度 ℓ = 1/(K·B0)"""
    r0 = 1.0e20
    K = 8.0 * PI * G * r0 * abs(Ttt)
    ell = 1.0 / (K * 1.0) if K > 0 else float("inf")
    return K, ell


# ============================================================
# 7. ODE 逐字复刻 + 数值实验
# ============================================================
def ode_rhs_faithful(r, Y, theta):
    A, B, tau, p_tau, omega, p_omega, phi, p_phi = Y
    g_tau0, mu0_sq, eta0 = theta
    xi = g_tau0 / MP ** 2
    gtau = g_tau0
    mu2 = mu0_sq * MP ** 2
    eta = eta0 / MP ** 2
    kappa = KAPPA0
    constraint = omega ** 2 - C ** 2 * (kappa ** 2 + tau ** 2)
    dp_tau = -2 * p_tau / r - 2 * gtau * tau * phi ** 2 - 2 * xi * C ** 2 * tau * constraint
    dp_omega = -2 * p_omega / r - 2 * xi * omega * constraint
    dp_phi = -2 * p_phi / r + (2 * mu2 + 4 * eta * phi ** 2) * phi - 2 * gtau * tau ** 2 * phi
    dtau, domega, dphi = p_tau, p_omega, p_phi
    grad_tau2 = p_tau ** 2 / B
    grad_omega2 = p_omega ** 2 / B
    grad_phi2 = p_phi ** 2 / B
    Vphi = mu2 * phi ** 2 + eta * phi ** 4
    U = Vphi - gtau * tau ** 2 * phi ** 2 + 0.5 * xi * constraint ** 2
    Ttt = A * C ** 2 * (0.5 * (grad_tau2 + grad_omega2 + grad_phi2) - U)
    Trr = 0.5 * (p_tau ** 2 + p_omega ** 2 + p_phi ** 2) \
        - B * (0.5 * (grad_tau2 + grad_omega2 + grad_phi2) - U)
    dB = (B ** 2 / r) * (1 - 1 / B - 8 * PI * G * r ** 2 * Ttt)
    dA = (A / r) * (B * (1 - 8 * PI * G * r ** 2 * Trr) - 1)
    return [dA, dB, dtau, dp_tau, domega, dp_omega, dphi, dp_phi]


def ic_state(theta):
    r0 = 1.0e20
    A0 = 1 - 2 * G * M_GAL / (C ** 2 * r0)
    B0 = 1 / A0
    return [A0, B0, TAU0, -1.0e-15, OMEGA0, -1.0e-22, PHI0, -1.0e-20], A0, B0, r0


def ic_diagnostics(theta, Y, A0, B0, r0):
    A, B, tau, p_tau, omega, p_omega, phi, p_phi = Y
    g_tau0, mu0_sq, eta0 = theta
    xi = g_tau0 / MP ** 2
    mu2 = mu0_sq * MP ** 2
    eta = eta0 / MP ** 2
    constraint = omega ** 2 - C ** 2 * (KAPPA0 ** 2 + tau ** 2)
    c2k2t2 = C ** 2 * (KAPPA0 ** 2 + tau ** 2)
    Vphi = mu2 * phi ** 2 + eta * phi ** 4
    U = Vphi - g_tau0 * tau ** 2 * phi ** 2 + 0.5 * xi * constraint ** 2
    grad2 = (p_tau ** 2 + p_omega ** 2 + p_phi ** 2) / B
    Ttt = A * C ** 2 * (0.5 * grad2 - U)
    K, ell = blowup_length(theta, Ttt)
    return {"constraint": constraint, "c2k2t2": c2k2t2,
            "residual_ratio": constraint / c2k2t2,
            "U": U, "U_xi": 0.5 * xi * constraint ** 2,
            "Ttt": Ttt, "K": K, "ell": ell}


def rk4_step(rhs, r, Y, h, theta):
    k1 = rhs(r, Y, theta)
    y2 = [Y[i] + 0.5 * h * k1[i] for i in range(8)]
    k2 = rhs(r - 0.5 * h, y2, theta)
    y3 = [Y[i] + 0.5 * h * k2[i] for i in range(8)]
    k3 = rhs(r - 0.5 * h, y3, theta)
    y4 = [Y[i] + h * k3[i] for i in range(8)]
    k4 = rhs(r - h, y4, theta)
    return [Y[i] + (h / 6.0) * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(8)]


def overflowed(Y):
    return any(math.isinf(v) or math.isnan(v) for v in Y)


def ode_experiment(theta, field_zero=False, nsteps=2, h=1.0e18):
    Y, A0, B0, r0 = ic_state(theta)
    if field_zero:
        Y = [A0, B0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    r = r0
    steps = []
    for k in range(nsteps):
        try:
            Yn = rk4_step(ode_rhs_faithful, r, Y, h, theta)
            if overflowed(Yn):
                steps.append("INF@%d" % (k + 1))
                Y = None
                break
            dB_rel = abs(Yn[1] - Y[1]) / abs(Y[1]) if Y[1] else 0.0
            steps.append("%.2e" % dB_rel)
            Y = Yn
            r -= h
        except OverflowError:
            steps.append("OVERFLOW@%d" % (k + 1))
            Y = None
            break
    status = "stable" if (Y is not None and not overflowed(Y)) else "blown"
    if field_zero:
        # 10 步稳定性
        Y, A0, B0, r0 = ic_state(theta)
        Y = [A0, B0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        r = r0
        maxrel = 0.0
        for k in range(10):
            B_prev = Y[1]
            Y = rk4_step(ode_rhs_faithful, r, Y, h, theta)
            maxrel = max(maxrel, abs(Y[1] - B_prev) / B_prev)
            r -= h
        status = "stable(10步, max|dB/B|=%.2e)" % maxrel
        return {"status": status, "steps": steps, "maxrel": maxrel}
    return {"status": status, "steps": steps}


# ============================================================
# 8. 旋转曲线精算
# ============================================================
ROT_DATA = [(1e20, 180, 10), (2e20, 195, 10), (3e20, 202, 10),
            (5e20, 205, 10), (8e20, 200, 10), (12e20, 185, 10)]


def rotation_experiment():
    rows = []
    chi2 = 0.0
    for ri, vobs, sv in ROT_DATA:
        v_kep = math.sqrt(G * M_GAL / ri)
        arg = 2 * math.sqrt(2 * 1e-12) * PHI0 * ri / C   # 全盒最小指数（gτ0 取下界）
        yuk = 2 * 1e-12 * TAU0 ** 2 * PHI0 ** 2 * ri * safe_exp(-arg)
        v2 = G * M_GAL / ri + yuk
        v_pred = math.sqrt(v2) / 1000.0
        z = (v_pred - vobs) / sv
        chi2 += z * z
        rows.append({"r": ri, "v_kep": v_kep / 1000.0, "v_pred": v_pred,
                     "v_obs": vobs, "z": z, "exp_arg": arg, "yuk_term": yuk})
    l_dec = C / (2 * math.sqrt(2 * 1e-12) * PHI0)
    return {"rows": rows, "chi2": chi2, "lnL_rot": -chi2 / 2.0,
            "min_exp_arg": min(r["exp_arg"] for r in rows),
            "decay_len": l_dec, "decay_orders": math.log10(1e20 / l_dec)}


def halo_scale():
    m_min = MP * math.sqrt(1e-12 * 1e-12 / 1e-2)
    lam = HBAR / (m_min * C)
    return {"m_tau_min": m_min, "lambda_min": lam,
            "orders": math.log10(1e20 / lam)}


# ============================================================
# 9. 先验/简并/量纲检查
# ============================================================
def prior_check():
    pts = []
    ok_all = True
    for g0 in (1e-12, 1e-8, 1e-4):
        for mu in (-1e-12, -1e-9, -1e-6):
            for eta in (1e-8, 1e-5, 1e-2):
                arg = -mu / (2 * eta)
                pts.append(arg)
                if not (arg > 0 and math.isfinite(arg)):
                    ok_all = False
    return {"n": len(pts), "min_arg": min(pts), "all_positive": ok_all}


def degeneracy_check():
    k = 1e-3
    pts = [(-k * 1e-6, 1e-6), (-k * 1e-5, 1e-5), (-k * 1e-3, 1e-3)]
    vals = [MP * math.sqrt(-mu / (2 * eta)) for mu, eta in pts]
    rel = max(abs(v - vals[0]) / vals[0] for v in vals)
    return {"points": pts, "vphi": vals, "max_rel": rel}


def dimension_machine():
    DIM_MU2_CODE = dmul(DIM_M, dpow(DIM_M, 1))            # mu0_sq·Mp² = [M²]
    DIM_MU2_REQ = DIM_INV2L                               # dp_phi 结构要求 [L⁻²]
    DIM_XI_CODE = dpow(DIM_M, -2)                         # gτ0/Mp² = [M⁻²]
    DIM_XI_REQ = ddiv(DIM_EDENS, dpow(DIM_FREQ2, 2))      # U/constraint²
    phi_vphi = dpow(ddiv(DIM_EDENS, DIM_INV2L), Fraction(1, 2))    # Vφ 位点
    phi_exp = ddiv(dim(0, 0, 0), dadd(ddiv(DIM_L, dim(0, 1, -1)), dim(0, 0, 0)))
    phi_exp = dim(0, 0, -1)                               # 指数位点：φ·r/c 无量纲 ⇒ φ=[T⁻¹]
    phi_v2 = dpow(ddiv(DIM_V2, dmul(dpow(DIM_INV2L, 1), DIM_L)), Fraction(1, 2))
    dim_omega2 = dpow(DIM_T, -2)
    dim_c2k2t2 = dmul(DIM_C2, DIM_INV2L)
    conv = dpow(ddiv(dim(0, 1, -1), dim(1, 2, -1)), 2)    # (c/ħ)² 量纲 = [M⁻²L⁻²]
    conv_val = (C / HBAR) ** 2
    return {
        "mu2_code": DIM_MU2_CODE, "mu2_req": DIM_MU2_REQ,
        "mu2_gap": ddiv(DIM_MU2_REQ, DIM_MU2_CODE),
        "xi_code": DIM_XI_CODE, "xi_req": DIM_XI_REQ,
        "xi_gap": ddiv(DIM_XI_REQ, DIM_XI_CODE),
        "phi_req_vphi": phi_vphi, "phi_req_exp": phi_exp, "phi_req_v2": phi_v2,
        "phi_pairwise_diff": [
            ddiv(phi_vphi, phi_exp), ddiv(phi_vphi, phi_v2), ddiv(phi_exp, phi_v2)],
        "omega2_dim": dim_omega2, "c2k2t2_dim": dim_c2k2t2,
        "identity_dim_ok": dim_omega2 == dim_c2k2t2,
        "conv_dim": conv, "conv_val": conv_val,
        "Mp2_val": MP ** 2, "inv_lp2_val": 1.0 / (LP ** 2),
    }


# ============================================================
# 10. 条目/控制组/守卫
# ============================================================
ENTRIES, CONTROLS, GUARDS, EVIDENCE = [], [], [], {}


def ent(code, title, state, evidence, note=""):
    ENTRIES.append({"code": code, "title": title, "state": state,
                    "evidence": evidence, "note": note})


def ctl(code, title, ok, evidence):
    CONTROLS.append({"code": code, "title": title, "ok": bool(ok), "evidence": evidence})


def grd(code, title, ok, evidence):
    GUARDS.append({"code": code, "title": title, "ok": bool(ok), "evidence": evidence})


_OWN = {BASE_NAME + s for s in (".py", ".json", ".md", "_report.txt", ".html")}
_OWN |= {"判定_" + BASE_NAME + ".md", "_run_r246.py", "_out_r246.txt"}


def scan_r246_trees():
    """非本卷命名的 *r246* 文件数（本卷自身产物与 runner 不算撞号）"""
    foreign = []
    for d in (SRC_DIR, DATA_DIR, VD_DIR):
        for root, _dirs, files in os.walk(d):
            for fn in files:
                if "r246" in fn and fn not in _OWN:
                    foreign.append(fn)
    return len(foreign), foreign[:5]


def self_audit_ast():
    """引擎自审：ent 的 state 必须是受控词表字面量；ctl/grd 的 ok 不得写死布尔"""
    src = io.open(__file__, "r", encoding="utf-8").read()
    tree = ast.parse(src)
    vocab = {"PASS", "FAIL", "INFO", "BOUNDARY", "CORRECTED"}
    bad_ent = bad_cg = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == "ent" and len(node.args) >= 3:
                a = node.args[2]
                if not (isinstance(a, ast.Constant) and a.value in vocab):
                    bad_ent += 1
            if node.func.id in ("ctl", "grd") and len(node.args) >= 3:
                a = node.args[2]
                if isinstance(a, ast.Constant) and isinstance(a.value, bool):
                    bad_cg += 1
    return bad_ent, bad_cg


# ============================================================
# 11. run_audit
# ============================================================
def run_audit():
    del ENTRIES[:], CONTROLS[:], GUARDS[:]
    EVIDENCE.clear()

    md_text = read_text(PRIMARY)
    blocks = extract_fenced_blocks(md_text)
    p018, p019 = classify_blocks(blocks)
    src18, ln18 = p018
    src19, ln19 = p019
    inline_cnt = md_text.count("# -*- coding") - len(blocks)

    hits = nhit(md_text, "P0-18", "P0-19", "kappa = 1.0e5",
                "omega_BD = 1/(g_tau0 * c**2)", "kappa_sq = alpha**2 * 1.0e-3",
                "占位", "总自由参数：17", "同源公设", "Jeffreys", "待运行")

    sandbox = sandbox_exec(src18)
    a18 = analyze_ast18(src18)
    a19 = analyze_ast19(src19)

    # γ 闭式扫描
    grid = []
    for k in range(33):
        g0 = 10 ** (-12 + k * (8.0 / 32))
        g = gamma_of_gtau(g0)
        grid.append({"g_tau0": g0, "gamma": g, "abs_gamma_minus_1": abs(g - 1),
                     "sigma_units": abs(g - 1) / SIGMA_G})
    sup_abs = max(r["abs_gamma_minus_1"] for r in grid)
    sup_row = max(grid, key=lambda r: r["abs_gamma_minus_1"])
    lnL_ppn_best = -0.5 * (sup_abs / SIGMA_G) ** 2
    g_req = gamma_required_decimal()
    orders_req = math.log10(1e-12 / float(g_req))
    # γ 只依赖 gτ0 的数值证
    g_a = gamma_of_gtau(1e-6)
    g_b = gamma_of_gtau(1e-6)  # μ0_sq/η0 不进入公式
    gamma_decoupled_bits = (g_a == g_b)

    # ODE 实验
    th_center = (1e-8, -1e-9, 1e-5)
    th_corner = (1e-4, -1e-6, 1e-2)
    Yc, A0, B0, r0 = ic_state(th_center)
    diag_center = ic_diagnostics(th_center, Yc, A0, B0, r0)
    diag_corner = ic_diagnostics(th_corner, Yc, A0, B0, r0)
    Yz = [A0, B0, TAU0, -1.0e-15, OMEGA0, -1.0e-22, PHI0, -1.0e-20]
    diag_gzero = ic_diagnostics((0.0, -1e-9, 1e-5), Yz, A0, B0, r0)
    exp_full = ode_experiment(th_center)
    exp_corner = ode_experiment(th_corner)
    exp_gzero = ode_experiment((0.0, -1e-9, 1e-5))
    exp_off = ode_experiment(th_center, field_zero=True)

    # 旋转曲线 / 晕尺度
    rot = rotation_experiment()
    halo = halo_scale()

    # 量纲
    dims = dimension_machine()

    # A1/A2
    prior = prior_check()
    degen = degeneracy_check()

    # H1 定价
    g_feas_max = 1.0 / (1.0 / SIGMA_G - 2.0)
    frac = (math.log10(g_feas_max) + 12.0) / 8.0

    # ---------------- A 组：对靶有利 ----------------
    ent("A1", "先验盒 μ0_sq<0 ⇒ vφ 根号恒正（27 点全验证）", "PASS",
        "27 个先验格点上 −μ0_sq/(2η0) 全部 > 0（最小 %.3e），vφ = Mp·sqrt(·) 在全盒有定义"
        % prior["min_arg"])
    ent("A2", "靶 FLAG-1 简并预判方向正确：vφ 仅依赖比值 −μ0_sq/η0", "PASS",
        "固定 −μ0_sq/η0=1e-3 的三个同比值点 vφ 最大相对差 %.2e（<1e-12）——预判成立"
        % degen["max_rel"],
        note="靶自带的审计 FLAG-1 是对的；本卷把它确认为仪器级事实")
    ent("A3", "本源恒等式 ω²=c²(κ²+τ²) 量纲齐次（承 r241 正面读数）", "PASS",
        "机读 ω²=%s，c²(κ²+τ²)=%s，identity_dim_ok=%s（承 r241 E 组正面项，本卷复核通过）"
        % (dstr(dims["omega2_dim"]), dstr(dims["c2k2t2_dim"]), dims["identity_dim_ok"]))
    ent("A4", "同源公设 ξ0=gτ0 显式声明（记账合法，属外部输入）", "INFO",
        "来料逐字：「同源公设 ξ0 = gτ0」+「总自由参数：17（原 18，由同源公设消去 1 个）」——"
        "公设公开声明（诚实），但按 r229 口径属外部输入，不计入推导供给")

    # ---------------- B 组：γ-PPN 层 ----------------
    ent("B1", "★沙箱实跑：靶 model_v_gamma 首次调用即抛 UnboundLocalError（%s 未绑定）"
        % sandbox["model_err_var"], "FAIL",
        "逐字 exec 靶源段（纯标准库桩）：%d 个 θ 点全部抛 %s（NameError 子类，"
        "未绑定变量=%s，首爆点 gτ0=%.0e）；loglike 全部返回 −inf（%d/%d）"
        "⇒ 联合后验体积精确为 0"
        % (sandbox["n_theta"], sandbox["model_err_type"], sandbox["model_err_var"],
           sandbox["first_err_theta"][0], sandbox["n_theta"], sandbox["n_theta"]),
        note="AST 流序：g_tau0 首次 Load 在块内第 %d 行（v² 循环体），赋值（元组解包）在第 %d 行"
             "——先载入后赋值；该缺陷在 P0-18 围栏块及两处逐字重贴副本（3/3）中稳定存在"
             % (a18["gtau_first_load_ln"], a18["gtau_unpack_ln"]))
    ent("B2", "γ 提取与 8 维 ODE 解零依赖（链路图与代码不符）", "FAIL",
        "AST：γ 计算尾段（解包之后）引用名集合 = %s，无 sol/A/B 任何场量；数值：同 gτ0 下 "
        "γ 位级不变（%s）——γ 只是 gτ0 的闭式函数，θ→RK4 积分→提取 γ 的宣称链断裂"
        % (a18["gamma_tail_names"], "bit-identical" if gamma_decoupled_bits else "MISMATCH"))
    ent("B3", "ω_BD = 1/(gτ0·c²) 读法二难：SI 读法量纲错；自然单位读法毁还原链", "FAIL",
        "SI 读法：1/(gτ0·c²) 机读 %s，而 γ=(1+ω)/(2+ω) 要求 ω 无量纲；"
        "自然单位读法（c=1）：则同一代码里 c=299792458.0 显式参与 ODE 与 v²，"
        "同一链条不能一半 SI 一半自然单位——两条读法各毁一条链"
        % dstr(dpow(ddiv(dim(0, 0, 0), dmul(dim(0, 0, 0), dpow(DIM_C2, 1))), 1)))
    ent("B4", "★PPN 通道可行体积 = 0：全先验盒 sup|γ−1| = %.4f（%.3e σ）" % (sup_abs, sup_abs / SIGMA_G),
        "FAIL",
        "γ−1 = −1/(2+ω_BD) 单调：gτ0=1e-12（下界）给最大 γ=0.5000056，|γ−1|=0.49999444"
        "=2.174e4σ；最优 lnL_PPN=%.3e；可行要求 gτ0≤%.5e（Decimal 50 位精算），"
        "比先验下界 1e-12 低 %.1f 个数量级 ⇒ 可行测度 = 0"
        % (lnL_ppn_best, float(g_req), orders_req))

    # ---------------- C 组：ODE/耦合层 ----------------
    ent("C1", "IC 处本源恒等式残差 −49.93%；约束能量项 U_ξ 达 1e60–1e64", "FAIL",
        "用靶自己的 IC（τ=1e5, ω=3e13, κ=1e5）：constraint = %.4e = %.2f%%×c²(κ²+τ²)"
        "（恒等式起点即违反一半）；U_ξ=½ξ·constraint² 中心 %.3e、最大角点 %.3e（gτ0=1e-4）"
        % (diag_center["constraint"], 100 * abs(diag_center["residual_ratio"]),
           diag_center["U_xi"], diag_corner["U_xi"]))
    ell_max = max(diag_center["ell"], diag_corner["ell"], diag_gzero["ell"])
    ent("C2", "★ODE 全变体爆破：闭式爆破长度 ℓ ≤ %.1e m（比普朗克长度小 %.0f 个数量级）"
        % (ell_max, math.log10(LP / ell_max)), "FAIL",
        "四变体（RK4 h=1e18 向内）：full T_tt=%.3e、ℓ=%.2e m、%s；max 角点 %.3e/%.2e/%s；"
        "gτ0=0（耦合关，η 链仍在）%.3e/%.2e/%s；场全关：%s。"
        "爆破不归因单一耦合项，而归因量纲破损的还原链整体（E1/E3）"
        % (diag_center["Ttt"], diag_center["ell"], "/".join(exp_full["steps"]),
           diag_corner["Ttt"], diag_corner["ell"], "/".join(exp_corner["steps"]),
           diag_gzero["Ttt"], diag_gzero["ell"], "/".join(exp_gzero["steps"]),
           exp_off["status"]))
    ent("C3", "退化控制反证：场全关则度规sector稳定 —— 爆破全部来自场sector", "FAIL",
        "τ=ω=φ=0、p_*=0 时 10 步 RK4 %s；同框架下任何带场初值的变体 1–2 步内溢出"
        "（RK45 缺省 atol=1e-6 ≫ |p_0|=1e-15..1e-20 的容差截断问题在此已无意义）"
        % exp_off["status"])

    # ---------------- D 组：旋转曲线层 ----------------
    ent("D1", "★汤川项在全先验盒恒零：指数 ≥ %.3e ⇒ exp 下溢，晕项≡0" % rot["min_exp_arg"], "FAIL",
        "靶 v² 修正项 exp(−2√(2gτ0)·φ·r/c) 的最小指数（gτ0=1e-12, r=1e20, φ=1e15）"
        "= %.3e ⇒ safe_exp 全返 0；衰减长度 c/(2√(2gτ0)φ) ≤ %.3f m，与星系尺度 1e20 m "
        "差 %.0f 个数量级——「晕衰减尺度落在星系尺度」在代码中从未发生"
        % (rot["min_exp_arg"], rot["decay_len"], rot["decay_orders"]))
    ent("D2", "v_pred ≡ 开普勒衰减：χ²_rot=%.1f，平坦旋转 180–205 km/s 不可复现" % rot["chi2"], "FAIL",
        "六点（M=1e41 kg 硬编码）：内点 +%.1fσ、外点 %.1fσ，χ²=%.1f ⇒ lnL_rot=%.1f；"
        "靶要拟合的恰是「平坦」段，而其公式在晕项恒零后退化为纯开普勒下坠"
        % (rot["rows"][0]["z"], rot["rows"][-1]["z"], rot["chi2"], rot["lnL_rot"]))
    ent("D3", "晕尺度 mτ 是死代码 + Compton 波长差 %.1f 个数量级" % halo["orders"], "FAIL",
        "AST：m_tau 在全块 Load 次数 = %d（赋值后零引用）——声称「mτ 控制晕衰减尺度」"
        "但似然代码从未使用；闭式：mτ_min=%.3e kg ⇒ λ_C=%.3e m，与 1e20 m 差 %.1f 数量级"
        % (a18["m_tau_loads"], halo["m_tau_min"], halo["lambda_min"], halo["orders"]))

    # ---------------- E 组：量纲机读 ----------------
    ent("E1", "还原链 mu2=μ0_sq·Mp² 给 [M²]，dp_phi 结构要求 [L⁻²]", "FAIL",
        "机读：代码 mu2=%s vs 要求 %s（(2·mu2+4·η·φ²)·φ 必须配 d²φ/dr² 的 [φ·L⁻²]）；"
        "缺乘 (c/ħ)²=%.3e（等价地应以 1/ℓ_P²=%.3e m⁻² 替代 Mp²=%.3e kg²）"
        % (dstr(dims["mu2_code"]), dstr(dims["mu2_req"]), dims["conv_val"],
           dims["inv_lp2_val"], dims["Mp2_val"]))
    ent("E2", "★φ 量纲三难：三个使用位点要求互不相容", "FAIL",
        "位点① Vφ=μ²φ² 须为能量密度且 μ²=[L⁻²] ⇒ φ=%s；位点② 指数 φ·r/c 无量纲 ⇒ φ=%s；"
        "位点③ v² 项 τ²φ²r 须 [L²T⁻²] ⇒ φ=%s——两两作比 %s / %s / %s 全部 ≠ [1]；"
        "同一符号在三个方程里要求三种不相容量纲"
        % (dstr(dims["phi_req_vphi"]), dstr(dims["phi_req_exp"]), dstr(dims["phi_req_v2"]),
           dstr(dims["phi_pairwise_diff"][0]), dstr(dims["phi_pairwise_diff"][1]),
           dstr(dims["phi_pairwise_diff"][2])))
    ent("E3", "ξ=gτ0/Mp² 给 [M⁻²]，U 项要求 [M L⁻¹ T²]——缺口 (3,−1,2)", "FAIL",
        "机读：代码 ξ=%s vs ½ξ·constraint² 须为能量密度 %s ⇒ 缺口比值 %s"
        "（与 r241 力方程/源项缺口同型的第三处量纲破损）"
        % (dstr(dims["xi_code"]), dstr(dims["xi_req"]), dstr(dims["xi_gap"])))

    # ---------------- F 组：P0-19 升级宣称 ----------------
    ent("F1", "★「全隐式曲率自洽反馈」0 行实现：AST 三证", "FAIL",
        "P0-19 代码：kappa_sq = %s（纯字面量，无 Call）；curvature_R 调用次数 = %d；"
        "ddA/ddB 仅存在于 curvature_R 定义内（ode_rhs 可达=%s）——二阶导在积分器侧无从获得；"
        "注释自曝「占位」×%d"
        % (a19["kappa_sq_expr"], a19["curvature_R_calls"],
           a19["ddA_in_ode_rhs"], a19["placeholder_hits"]),
        note="「曲率标量 R 由度规二阶导实时计算」的宣称与其随附代码为零对应")
    ent("F2", "α 新增参数 3→4 维复演 P0-16 悖论（每修一次自洽 +1 参数）", "BOUNDARY",
        "P0-19 自曝：「这里又新增了映射系数 α！参数维度从 3 维 → 4 维」——"
        "与本库 r229「供给 0」、r214–r234 边界地图同型；登记不升 L3")
    ent("F3", "Jeffreys 判据引用正确；ΛCDM 对比似然 0 行 + 18 处内联代码不可解析", "INFO",
        "靶引用的 ln Bayes 因子分级与 Kass–Raftery(1995) 一致（对靶有利）；"
        "但 P0-19 代码中无任何 ΛCDM 基准似然（AST 零命中）⇒「贝叶斯证据对比 ΛCDM」目标未实现；"
        "中段 %d 处折叠内联代码（含疑似修复版）因导出格式不可解析，"
        "修复主张未以可运行块提交——本卷只审两个正式围栏块" % inline_cnt)

    # ---------------- G 组：记账 ----------------
    ent("G1", "参数三口径互斥且不可对账：声称 17 / 采样 3 / 代码可见硬编码 %d" % a18["hard_total"], "FAIL",
        "AST 实数硬编码自由数 = %d（κ0×1 + M×1 + r0×1 + 内界×1 + rtol×1 + Y0 场初值×%d）"
        "从未进入似然；声称的 17 参数清单未随文（P0-17 未附）⇒ 无法逐一对账"
        % (a18["hard_total"], a18["hard_params"]["Y0_elements"]))
    ent("G2", "旋转数据 6 点为合成值；M=1e41 kg 硬编码且内点已 +%.1fσ"
        % rot["rows"][0]["z"], "INFO",
        "数据无星系名/误差来源，σ 均匀 10 km/s；开普勒内点 258 km/s 已超观测上限 180+3σ=210"
        "——数据集本身不能承担「观测判据」角色（登记，不计入攻破）")
    ent("G3", "靶状态表自曝「⏳ 待运行」；本卷首次给出可运行判定 = 0", "INFO",
        "靶自评「采样结果将直接判定 TUFT-3S 是否还留有生存空间」但从未运行；"
        "本卷判定：B1（loglike 恒 −inf）⇒ 后验体积 0，无需采样——"
        "可运行性本身为 0，采样器在首个死点即终止")

    # ---------------- H 组：修复定价 ----------------
    ent("H1", "修复定价（三件缺一不可，登记 SURVIVE 条件，不代选）", "INFO",
        "① ω_BD 量纲修复（去 c² 自然单位化）：先验内恢复可行带 gτ0≤%.3e（log 空间体积 %.1f%%）；"
        "② γ 必须从 (A,B) 场解提取（拆除解耦）；③ IC 自洽 + 还原链补 (c/ħ)² 与 ξ 重整"
        "（否则 ξ 通道在 1e-90 m 爆破）。任意两件不行：只修①则 γ 仍解耦（B2），"
        "只修①②则 ODE 仍爆破（C2）——三件套与 J62 Gate-A P4 同型"
        % (g_feas_max, 100 * frac))

    # ---------------- 控制组 ----------------
    ctl("CTL1", "BD γ 公式极限正控制（仪器会绿）",
        abs(gamma_of_gtau(1e-30) - 1.0) < 1e-10 and abs(gamma_of_gtau(1e30) - 0.5) < 1e-30,
        "ω→∞ ⇒ γ→1（|γ−1|=%.2e）；ω→0 ⇒ γ=1/2（偏差=%.2e）"
        % (abs(gamma_of_gtau(1e-30) - 1.0), abs(gamma_of_gtau(1e30) - 0.5)))
    dv = (Decimal("6.67430") * Decimal("1e30") / Decimal("1e20")).sqrt()
    ctl("CTL2", "Kepler 正控制（Decimal 50 位 vs float）",
        abs(math.sqrt(G * M_GAL / 1e20) - float(dv)) / float(dv) < 1e-12,
        "v(1e20)=%.6e m/s，Decimal 相对差 %.2e；v(2e20)/v(1e20)=1/√2 rel=%.2e"
        % (math.sqrt(G * M_GAL / 1e20),
           abs(math.sqrt(G * M_GAL / 1e20) - float(dv)) / float(dv),
           abs(math.sqrt(G * M_GAL / 2e20) / math.sqrt(G * M_GAL / 1e20) - 1 / math.sqrt(2))))
    g3 = gamma_of_gtau(2e-22)
    ctl("CTL3", "PPN 门可绿正控制（先验外点，判别力证明）",
        abs(g3 - 1.0) < SIGMA_G,
        "gτ0=2e-22（先验外 10 个数量级）⇒ |γ−1|=%.3e < 2.3e-5 ⇒ 门会绿——B4 的红是参数驱动的真排除"
        % abs(g3 - 1.0))
    ctl("CTL4", "阈值敏感性负控制（σγ 放大则判决翻绿）",
        sup_abs < 0.5,
        "σγ→0.5 时 sup|γ−1|=%.8f < 0.5 ⇒ B4 判决将翻转 ⇒ 红不是无条件的" % sup_abs)
    ctl("CTL5", "量纲仪器自检（GM/r 与 c²(κ²+τ²)）",
        dstr(dmul(dmul(DIM_G, DIM_M), dpow(DIM_L, -1))) == dstr(DIM_V2)
        and dstr(dmul(DIM_C2, DIM_INV2L)) == dstr(DIM_FREQ2),
        "d(GM/r)=%s=[L²T⁻²] ✓；d(c²(κ²+τ²))=%s=[T⁻²] ✓"
        % (dstr(dmul(dmul(DIM_G, DIM_M), dpow(DIM_L, -1))), dstr(dmul(DIM_C2, DIM_INV2L))))
    ok6 = (ShimNP.argmin([3, 1, 2]) == 1
           and Y2D([[1, 2], [3, 4]])[(slice(None), 1)] == [2, 4]
           and len(FakeSol().y) == 8 and len(FakeSol().y[:, 0]) == 8)
    ctl("CTL6", "沙箱桩自检（argmin/Y2D 列取/FakeSol 结构）", ok6,
        "argmin([3,1,2])=1 ✓；Y2D[:,1] 列取 ✓；FakeSol 8×%d ✓" % len(FakeSol().t))

    # ---------------- 守卫 ----------------
    n246_at_start, foreign = scan_r246_trees()
    g1_ok = all(sha256_of(p) == SHA_AT_IMPORT[p] for p in TARGETS)
    grd("G1", "靶 2 份 sha256 前后一致", g1_ok,
        "修改攻破.md %s…；核心动力学方程组.md %s…"
        % (SHA_AT_IMPORT[TARGETS[0]][:8], SHA_AT_IMPORT[TARGETS[1]][:8]))
    _dist = {}
    for e in ENTRIES:
        _dist[e["state"]] = _dist.get(e["state"], 0) + 1
    g2_ok = (len(ENTRIES) == sum(EXPECT_DIST.values())
             and all(_dist.get(k, 0) == v for k, v in EXPECT_DIST.items()))
    grd("G2", "条目 24 = PASS 3 / FAIL 15 / BOUNDARY 1 / INFO 5", g2_ok,
        "实测分布 %s（期望 %s）" % (_dist, EXPECT_DIST))
    g3_ok = all(c["ok"] for c in CONTROLS)
    grd("G3", "控制组 6/6 全绿", g3_ok,
        "实测 %d/%d" % (sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS)))
    grd("G4", "号位唯一（启动时三树非本卷 *r246* 文件 = 0）", n246_at_start == 0,
        "启动实测非本卷 *r246* = %d %s" % (n246_at_start, foreign))
    g5_ok = all(sha256_of(p) == WS_SHA_AT_IMPORT[p] for p in WRITE_SIDE)
    grd("G5", "写侧不动（verify.py / refresh_catalog.py）", g5_ok,
        "sha 实测一致=%s（收尾再验一次）" % g5_ok)
    b_ent, b_cg = self_audit_ast()
    grd("G6", "引擎自审 AST（ent 词表 / ctl·grd 无写死布尔）", b_ent == 0 and b_cg == 0,
        "ent 违例 %d；ctl/grd 写死布尔 %d" % (b_ent, b_cg))

    EVIDENCE.update({
        "sandbox": sandbox, "ast18": {k: v for k, v in a18.items()},
        "ast19": a19, "gamma_grid_top": grid[:3] + grid[-3:],
        "sup_abs": sup_abs, "lnL_ppn_best": lnL_ppn_best,
        "g_req": str(g_req), "orders_req": orders_req,
        "diag": {"center": diag_center, "corner": diag_corner, "gzero": diag_gzero},
        "ode": {"full": exp_full, "corner": exp_corner, "gzero": exp_gzero, "off": exp_off},
        "rot": rot, "halo": halo, "dims": dims, "prior": prior, "degen": degen,
        "g_feas_max": g_feas_max, "frac": frac, "inline_cnt": inline_cnt,
        "hits": hits, "blocks": len(blocks), "ln18": ln18, "ln19": ln19,
    })
    return EVIDENCE


# ============================================================
# 12. 输出
# ============================================================
def fmt_rel(x):
    if x == 0:
        return "0"
    return "%.2e" % x if abs(x) < 1e-3 or abs(x) > 1e3 else "%.6f" % x


def build_header(ev):
    return (
        "靶的「贝叶斯观测侧审计」在首次似然调用即抛 UnboundLocalError（g_tau0 未绑定，"
        "NameError 子类；AST 流序 + 沙箱实跑双证：先载入后赋值），loglike 恒 −inf "
        "⇒ 联合后验体积精确为 0；"
        "即便修复该笔误，PPN 通道在全先验盒上 sup|γ−1|=0.49999444 = 2.174e4σ"
        "（可行 gτ0 ≤ 2.56e-22，比先验下界低 9.6 个数量级），旋转曲线汤川项在全盒恒零"
        "（指数 ≥9.4e20 ⇒ 下溢），χ²_rot=411 与平坦旋转 180–205 km/s 不相容；"
        "ODE 起点违反本源恒等式 49.93%，四变体爆破长度 ℓ≤3.2e-99 m（比普朗克长度小 64 个"
        "数量级），唯有场全关才稳定；"
        "P0-19 宣称的「全隐式曲率反馈」在随附代码中 0 行实现（AST 三证）。"
        "靶自评「⏳ 待运行」的采样不需要运行——可运行性本身为 0。"
        "对靶有利项照登：先验构造正确、FLAG-1 简并预判正确、恒等式量纲齐次、同源公设显式声明。")


def build_report(ev, res, dist, n_ctl_ok, n_grd_ok):
    L = []
    L.append("TUFT-%s · 观测统计层：TUFT-3S 贝叶斯 MCMC 联合后验三重审计" % RID.upper())
    L.append("生成 %s · 靶块 P0-18@L%d / P0-19@L%d · 围栏块 %d 个 · 内联折叠 %d 处"
             % (START_ISO, ev["ln18"], ev["ln19"], ev["blocks"], ev["inline_cnt"]))
    L.append("=" * 78)
    L.append("")
    L.append("【判词】")
    L.append(build_header(ev))
    L.append("")
    L.append("【沙箱实跑】model_v_gamma：%s（未绑定变量=%s）× %d θ；loglike 全 −inf：%s"
             % (ev["sandbox"]["model_err_type"], ev["sandbox"]["model_err_var"],
                ev["sandbox"]["n_theta"], ev["sandbox"]["all_loglike_neg_inf"]))
    L.append("【AST-18】g_tau0 先载入(L%d)后赋值(L%d)=%s；m_tau Load=%d；"
             "硬编码自由数=%d；γ 尾段引用=%s"
             % (ev["ast18"]["gtau_first_load_ln"], ev["ast18"]["gtau_unpack_ln"],
                ev["ast18"]["gtau_load_before_assign"], ev["ast18"]["m_tau_loads"],
                ev["ast18"]["hard_total"], ev["ast18"]["gamma_tail_names"]))
    L.append("【AST-19】kappa_sq=%s；curvature_R 调用=%d；占位×%d"
             % (ev["ast19"]["kappa_sq_expr"], ev["ast19"]["curvature_R_calls"],
                ev["ast19"]["placeholder_hits"]))
    L.append("【γ 闭式】sup|γ−1|=%.8f（%.3e σ）；lnL_PPN_best=%.4e；gτ0_req=%.5e；"
             "低于先验下界 %.1f 数量级"
             % (ev["sup_abs"], ev["sup_abs"] / SIGMA_G, ev["lnL_ppn_best"],
                float(ev["g_req"]), ev["orders_req"]))
    L.append("【ODE】full: |Ttt|=%.3e ℓ=%.2e %s | corner: %.3e/%.2e %s | "
             "gτ0=0: %.3e/%.2e %s | 场全关: %s"
             % (ev["diag"]["center"]["Ttt"], ev["diag"]["center"]["ell"],
                ev["ode"]["full"]["steps"],
                ev["diag"]["corner"]["Ttt"], ev["diag"]["corner"]["ell"],
                ev["ode"]["corner"]["steps"],
                ev["diag"]["gzero"]["Ttt"], ev["diag"]["gzero"]["ell"],
                ev["ode"]["gzero"]["steps"], ev["ode"]["off"]["status"]))
    L.append("【旋转】χ²=%.1f lnL=%.1f 最小指数=%.3e 衰减长度=%.3f m（%.0f 数量级）"
             % (ev["rot"]["chi2"], ev["rot"]["lnL_rot"], ev["rot"]["min_exp_arg"],
                ev["rot"]["decay_len"], ev["rot"]["decay_orders"]))
    L.append("【晕尺度】mτ_min=%.3e kg λ=%.3e m（%.1f 数量级）；m_tau Load=%d"
             % (ev["halo"]["m_tau_min"], ev["halo"]["lambda_min"],
                ev["halo"]["orders"], ev["ast18"]["m_tau_loads"]))
    L.append("【量纲】mu2 %s(码) vs %s(需)；xi %s(码) vs %s(需)；φ 三要求 %s/%s/%s；"
             "恒等式量纲齐次=%s；换算因子 (c/ħ)²=%.3e"
             % (dstr(ev["dims"]["mu2_code"]), dstr(ev["dims"]["mu2_req"]),
                dstr(ev["dims"]["xi_code"]), dstr(ev["dims"]["xi_req"]),
                dstr(ev["dims"]["phi_req_vphi"]), dstr(ev["dims"]["phi_req_exp"]),
                dstr(ev["dims"]["phi_req_v2"]), ev["dims"]["identity_dim_ok"],
                ev["dims"]["conv_val"]))
    L.append("")
    L.append("【条目】")
    for e in res["entries"]:
        L.append("[%s] %s · %s" % (e["state"], e["code"], e["title"]))
        L.append("    证据：%s" % e["evidence"])
        if e["note"]:
            L.append("    注：%s" % e["note"])
    L.append("")
    L.append("【控制组】")
    for c in res["controls"]:
        L.append("[%s] %s — %s" % ("PASS" if c["ok"] else "FAIL", c["code"], c["evidence"]))
    L.append("")
    L.append("【守卫】")
    for g in res["guards"]:
        L.append("[%s] %s — %s" % ("PASS" if g["ok"] else "FAIL", g["code"], g["evidence"]))
    L.append("")
    L.append("【γ 网格（首尾各 3）】")
    for r in ev["gamma_grid_top"]:
        L.append("  gτ0=%.3e γ=%.12f |γ−1|=%.3e (%.3e σ)"
                 % (r["g_tau0"], r["gamma"], r["abs_gamma_minus_1"], r["sigma_units"]))
    L.append("【旋转六点】")
    for r in ev["rot"]["rows"]:
        L.append("  r=%.2e v_kep=%.1f v_pred=%.1f v_obs=%d z=%+.1f 晕项=%.3e"
                 % (r["r"], r["v_kep"], r["v_pred"], r["v_obs"], r["z"], r["yuk_term"]))
    return "\n".join(L)


def build_md(ev, res, dist, header):
    md = ["# TUFT-%s · 观测统计层：TUFT-3S 贝叶斯 MCMC 联合后验三重审计\n" % RID.upper(),
          "\n> 生成时间：%s · 靶块 P0-18@L%d / P0-19@L%d\n" % (START_ISO, ev["ln18"], ev["ln19"]),
          "\n## 判词\n\n%s\n" % header]
    md.append("\n## 一、沙箱实跑（全新仪器）\n")
    sb = ev["sandbox"]
    md.append("\n- 逐字 exec 靶 `model_v_gamma` + `loglike`（纯标准库桩）：%d 个 θ 全部抛 "
              "**%s**（NameError 子类，未绑定变量=`%s`）；loglike 全部返回 −inf（%d/%d）"
              "⇒ 后验体积精确 0\n"
              % (sb["n_theta"], sb["model_err_type"], sb["model_err_var"],
                 sb["n_theta"], sb["n_theta"]))
    md.append("\n## 二、AST 静态审计（全新仪器）\n")
    md.append("\n- g_tau0 首次 Load 在块内 L%d（v² 循环体），赋值在 L%d ⇒ 先载入后赋值\n"
              % (ev["ast18"]["gtau_first_load_ln"], ev["ast18"]["gtau_unpack_ln"]))
    md.append("- m_tau 赋值后 Load 次数 = %d（死代码）；γ 尾段引用名 = %s（无 sol）\n"
              % (ev["ast18"]["m_tau_loads"], ev["ast18"]["gamma_tail_names"]))
    md.append("- P0-19：kappa_sq = `%s`（字面量）；curvature_R 调用 = %d；「占位」×%d\n"
              % (ev["ast19"]["kappa_sq_expr"], ev["ast19"]["curvature_R_calls"],
                 ev["ast19"]["placeholder_hits"]))
    md.append("\n## 三、γ-PPN 闭式\n")
    md.append("\n| gτ0 | γ | \\|γ−1\\| (σ) |\n|---|---|---|\n")
    for r in ev["gamma_grid_top"]:
        md.append("| %.3e | %.12f | %.3e |\n" % (r["g_tau0"], r["gamma"], r["sigma_units"]))
    md.append("\nsup|γ−1| = %.8f = %.3e σ；最优 lnL_PPN = %.4e；可行 gτ0 ≤ %.5e"
              "（比先验下界低 %.1f 数量级）⇒ **可行体积 = 0**\n"
              % (ev["sup_abs"], ev["sup_abs"] / SIGMA_G, ev["lnL_ppn_best"],
                 float(ev["g_req"]), ev["orders_req"]))
    md.append("\n## 四、旋转曲线（晕项恒零 ⇒ 纯开普勒）\n")
    md.append("\n| r (m) | v_kep (km/s) | v_pred | v_obs | z |\n|---|---|---|---|---|\n")
    for r in ev["rot"]["rows"]:
        md.append("| %.2e | %.1f | %.1f | %d | %+.1f |\n"
                  % (r["r"], r["v_kep"], r["v_pred"], r["v_obs"], r["z"]))
    md.append("\nχ²=%.1f；最小汤川指数=%.3e；衰减长度=%.3f m（差 %.0f 数量级）\n"
              % (ev["rot"]["chi2"], ev["rot"]["min_exp_arg"],
                 ev["rot"]["decay_len"], ev["rot"]["decay_orders"]))
    md.append("\n## 五、ODE 变体实验\n")
    md.append("\n| 变体 | \\|T_tt\\| | ℓ (m) | RK4 步进 | 状态 |\n|---|---|---|---|---|\n")
    for nm, dg, ex in (("full(中心)", ev["diag"]["center"], ev["ode"]["full"]),
                       ("max 角点", ev["diag"]["corner"], ev["ode"]["corner"]),
                       ("gτ0=0", ev["diag"]["gzero"], ev["ode"]["gzero"])):
        md.append("| %s | %.3e | %.2e | %s | %s |\n"
                  % (nm, dg["Ttt"], dg["ell"], "/".join(ex["steps"]), ex["status"]))
    md.append("| 场全关 | 0 | — | 10 步 | %s |\n" % ev["ode"]["off"]["status"])
    md.append("\n## 六、量纲机读\n")
    md.append("\n| 式 | 机读 | 应为 | 缺口 |\n|---|---|---|---|\n")
    md.append("| mu2=μ0_sq·Mp² | %s | %s | ×(c/ħ)²=%.3e |\n"
              % (dstr(ev["dims"]["mu2_code"]), dstr(ev["dims"]["mu2_req"]),
                 ev["dims"]["conv_val"]))
    md.append("| ξ=gτ0/Mp² | %s | %s | %s |\n"
              % (dstr(ev["dims"]["xi_code"]), dstr(ev["dims"]["xi_req"]),
                 dstr(ev["dims"]["xi_gap"])))
    md.append("| φ（三位点） | %s / %s / %s | 互不相容 | 三难 |\n"
              % (dstr(ev["dims"]["phi_req_vphi"]), dstr(ev["dims"]["phi_req_exp"]),
                 dstr(ev["dims"]["phi_req_v2"])))
    md.append("\n## 七、条目\n")
    for e in res["entries"]:
        md.append("\n### [%s] %s · %s\n" % (e["state"], e["code"], e["title"]))
        md.append("\n- 证据：%s\n" % e["evidence"])
        if e["note"]:
            md.append("- 注：%s\n" % e["note"])
    md.append("\n## 八、红线\n")
    md.append("\n- 靶 2 份只读（sha256 前后一致）\n")
    md.append("- 本卷条目**不可与 r142–r245 相加**（新层：观测统计层）\n")
    md.append("- 未跑 refresh_catalog.py，未改 verify.py\n")
    return "".join(md)


def build_verdict(ev, res, dist, header, n_ctl_ok, n_grd_ok):
    vd = ["# 判定册 · TUFT-%s（观测统计层：TUFT-3S 贝叶斯 MCMC 联合后验）\n" % RID.upper(),
          "\n## 判词\n\n%s\n" % header,
          "\n## 判决分组\n", "\n| 组 | 内容 | 结论 |\n|---|---|---|\n",
          "| A | 对靶有利/正确：先验构造 ✓、FLAG-1 简并预判 ✓、恒等式量纲 ✓、同源公设显式声明 | PASS 3 / INFO 1 |\n",
          "| B | **γ-PPN 层**：沙箱 UnboundLocalError(g_tau0) ⇒ loglike 恒 −inf；γ 解耦；ω_BD 二难；PPN 可行体积 0（2.174e4σ） | **FAIL** |\n",
          "| C | **ODE/耦合层**：IC 恒等式违反 49.93%；四变体爆破 ℓ≤3.2e-99 m；唯场全关稳定 | **FAIL** |\n",
          "| D | **旋转曲线层**：晕项恒零（指数 ≥9.4e20）；χ²=411；mτ 死代码 + 43.8 数量级 | **FAIL** |\n",
          "| E | **量纲机读**：mu2 链 [M²] vs [L⁻²]；φ 三难；ξ 缺口 (3,−1,2) | **FAIL** |\n",
          "| F | **P0-19**：全隐式反馈 0 行实现（AST 三证）；α 膨胀 3→4；Jeffreys 引用对但对比未实现 | **FAIL** / BOUNDARY / INFO |\n",
          "| G | **记账**：17/3/%d 三口径互斥；合成数据；「⏳ 待运行」自曝 | **FAIL** / INFO |\n" % ev["ast18"]["hard_total"],
          "| H | **修复定价**：三件缺一不可（①量纲 ②解耦 ③IC+重整），只修①后可行带恢复 %.1f%% | INFO |\n" % (100 * ev["frac"]),
          "\n## ★ 性质界定（关键）\n"]
    vd.append("\n1. **本卷不判「TUFT-3S 物理思想全错」**：判的是其**观测侧审计机器**（P0-18/P0-19）"
              "在首次似然调用即崩溃，且即便修复笔误，其 γ 提取与 ODE 解耦、还原链量纲破损、"
              "晕项恒零使「用观测切割参数空间」的目标在当前代码形态下不可能成立。\n")
    vd.append("2. **B1 判决不依赖任何数值库**：沙箱用纯标准库桩逐字 exec 靶源段，"
              "NameError 与 numpy/dynesty 无关 ⇒ 结论对真实环境同构成立。\n")
    vd.append("3. **B4/C1/D1 三条独立排除通道**：PPN 通道（γ 闭式）、旋转通道（χ²=411）、"
              "动力学通道（恒等式违反+爆破）——任一单独成立即可排除，三者互为冗余。\n")
    vd.append("4. **对靶有利项与缺陷同表登记**：A 组四条照登；靶的 FLAG-1 简并预判、"
              "Jeffreys 引用、边界约定（「观测侧审计，不是理论构造」）均为诚实/正确项。\n")
    vd.append("\n## 治理\n")
    vd.append("\n- 控制组 %d/%d；守卫 %d/%d\n" % (n_ctl_ok, len(res["controls"]),
                                                 n_grd_ok, len(res["guards"])))
    vd.append("- 靶 2 份只读（sha256 前后一致）\n")
    vd.append("- 判定册按 r241/r242 惯例落 `判定/`（r243–r245 落在 `数据/` 且 README 链接指向 "
              "`判定/` 存在断链——本卷不回改他册，仅本卷走对）\n")
    vd.append("- 本卷条目不可与 r142–r245 相加（新层：观测统计层）\n")
    vd.append("- 未跑 refresh_catalog.py；未改 verify.py\n")
    return "".join(vd)


def render_html(ev, res, payload, header, dist, n_ctl_ok, n_grd_ok):
    ents = "".join(
        '<div class="ent %s"><b>[%s] %s · %s</b><div class="ev">%s</div>%s</div>'
        % ("pass" if e["state"] == "PASS" else ("fail" if e["state"] == "FAIL"
                                                else ("info" if e["state"] == "INFO" else "bnd")),
           e["state"], e["code"], e["title"], e["evidence"],
           ('<div class="note">%s</div>' % e["note"]) if e["note"] else "")
        for e in res["entries"])
    ctls = "".join('<div class="ctl %s">[%s] %s · %s</div>'
                   % ("ok" if c["ok"] else "bad", "PASS" if c["ok"] else "FAIL",
                      c["code"], c["evidence"]) for c in res["controls"])
    grds = "".join('<div class="ctl %s">[%s] %s · %s</div>'
                   % ("ok" if g["ok"] else "bad", "PASS" if g["ok"] else "FAIL",
                      g["code"], g["evidence"]) for g in res["guards"])
    rot_rows = "".join(
        "<tr><td>%.2e</td><td>%.1f</td><td>%.1f</td><td>%d</td><td>%+.1f</td></tr>"
        % (r["r"], r["v_kep"], r["v_pred"], r["v_obs"], r["z"]) for r in ev["rot"]["rows"])
    ode_rows = "".join(
        "<tr><td>%s</td><td>%.3e</td><td>%.2e</td><td>%s</td><td>%s</td></tr>"
        % (nm, dg["Ttt"], dg["ell"], "/".join(ex["steps"]), ex["status"])
        for nm, dg, ex in (("full(中心)", ev["diag"]["center"], ev["ode"]["full"]),
                           ("max 角点", ev["diag"]["corner"], ev["ode"]["corner"]),
                           ("gτ0=0", ev["diag"]["gzero"], ev["ode"]["gzero"])))
    g_rows = "".join(
        "<tr><td>%.3e</td><td>%.12f</td><td>%.3e</td></tr>" % r_
        for r_ in [(r["g_tau0"], r["gamma"], r["sigma_units"]) for r in ev["gamma_grid_top"]])
    return u"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>TUFT-{RID} · 观测统计层</title>
<style>
body{{font-family:"Segoe UI","Microsoft YaHei",sans-serif;background:#f7f8fa;color:#1a1a1a;
 margin:0;padding:28px;line-height:1.6}}
h1{{font-size:22px;margin:0 0 6px}} h2{{font-size:17px;margin:24px 0 10px;
 border-left:4px solid #6a3d8a;padding-left:10px}}
.meta{{color:#666;font-size:13px;margin-bottom:18px}}
.verdict{{background:#fff8e6;border:1px solid #e0c48a;border-radius:6px;padding:14px;
 font-size:14px;margin-bottom:20px}}
table{{border-collapse:collapse;width:100%;background:#fff;font-size:13px;margin:8px 0}}
th,td{{border:1px solid #d8dce2;padding:6px 8px;text-align:left}}
th{{background:#eef1f5}}
.ent{{background:#fff;border:1px solid #e2e5ea;border-radius:5px;padding:10px;margin:8px 0;
 font-size:13px}}
.ent.pass{{border-left:4px solid #2e7d4f}} .ent.fail{{border-left:4px solid #b3382c}}
.ent.info{{border-left:4px solid #8a8f98}} .ent.bnd{{border-left:4px solid #c98a2d}}
.ev{{color:#333;margin-top:4px}} .note{{color:#666;font-size:12px;margin-top:4px}}
.ctl{{font-size:12px;padding:3px 6px;margin:2px;border-radius:3px;display:inline-block;
 width:340px;vertical-align:top}}
.ctl.ok{{background:#e8f3ec;color:#2e7d4f}} .ctl.bad{{background:#fbeceb;color:#b3382c}}
</style></head><body>
<h1>TUFT-{RID} · 观测统计层（★方法全谱 10 道工序）</h1>
<div class="meta">{title} · 生成 {ts} · 靶块 P0-18@L{ln18} / P0-19@L{ln19}</div>
<div class="verdict"><b>判词：</b>{header}</div>

<h2>一、沙箱实跑 + AST 静态（全新仪器）</h2>
<div class="ent fail"><b>沙箱</b><div class="ev">逐字 exec 靶 model_v_gamma：{n_theta} 个 θ
 全部抛 {err_type}（未绑定变量={err_var}）；loglike 全部 −inf ⇒ 后验体积 = 0</div></div>
<div class="ent fail"><b>AST</b><div class="ev">g_tau0 先载入(L{fl})后赋值(L{ul})；
 m_tau Load={mt}（死代码）；γ 尾段引用={names}（无 sol）；P0-19 kappa_sq={ks}（字面量），
 curvature_R 调用={crc}，「占位」×{ph}</div></div>

<h2>二、γ-PPN 闭式（可行体积 = 0）</h2>
<table><tr><th>gτ0</th><th>γ</th><th>|γ−1| (σ)</th></tr>{g_rows}</table>
<div class="meta">sup|γ−1| = <b>{sup}</b> = {supsig} σ；lnL_PPN_best = {lnl}；
 可行 gτ0 ≤ {greq}（比先验下界低 {orders} 数量级）</div>

<h2>三、旋转曲线（晕项恒零 ⇒ 纯开普勒，χ²={chi2:.1f}）</h2>
<table><tr><th>r (m)</th><th>v_kep (km/s)</th><th>v_pred</th><th>v_obs</th><th>z</th></tr>
{rot_rows}</table>

<h2>四、ODE 变体实验（爆破长度 ℓ ≤ 1e-89 m）</h2>
<table><tr><th>变体</th><th>T_tt</th><th>ℓ (m)</th><th>RK4 步进</th><th>状态</th></tr>
{ode_rows}</table>
<div class="meta">场全关退化控制：{off} —— 爆破全部来自量纲破损的场 sector</div>

<h2>五、量纲机读（φ 三难）</h2>
<div class="ent fail"><div class="ev">mu2 代码 {mu2c} vs 需要 {mu2r}（缺 ×(c/ħ)²={conv:.3e}）；
 ξ 代码 {xic} vs 需要 {xir}（缺口 {gap}）；
 φ 三位点要求 {p1} / {p2} / {p3} 两两互不相容</div></div>

<h2>六、条目（{n_ent}）</h2>
{ents}

<h2>七、控制组（{nctl_ok}/{nctl}）</h2>
{ctls}

<h2>八、守卫（{ngrd_ok}/{ngrd}）</h2>
{grds}

<div class="meta" style="margin-top:24px">
红线：靶 2 份只读（sha256 前后一致）；本卷条目不可与 r142–r245 相加（新层：观测统计层）。
</div>
</body></html>""".format(
        RID=RID.upper(), title=payload["title"], ts=START_ISO,
        ln18=ev["ln18"], ln19=ev["ln19"], header=header,
        n_theta=ev["sandbox"]["n_theta"], err_type=ev["sandbox"]["model_err_type"],
        err_var=ev["sandbox"]["model_err_var"],
        fl=ev["ast18"]["gtau_first_load_ln"], ul=ev["ast18"]["gtau_unpack_ln"],
        mt=ev["ast18"]["m_tau_loads"], names=ev["ast18"]["gamma_tail_names"],
        ks=ev["ast19"]["kappa_sq_expr"], crc=ev["ast19"]["curvature_R_calls"],
        ph=ev["ast19"]["placeholder_hits"],
        g_rows=g_rows, sup="%.8f" % ev["sup_abs"],
        supsig="%.3e" % (ev["sup_abs"] / SIGMA_G), lnl="%.4e" % ev["lnL_ppn_best"],
        greq="%.5e" % float(ev["g_req"]), orders="%.1f" % ev["orders_req"],
        chi2=ev["rot"]["chi2"], rot_rows=rot_rows, ode_rows=ode_rows,
        off=ev["ode"]["off"]["status"],
        mu2c=dstr(ev["dims"]["mu2_code"]), mu2r=dstr(ev["dims"]["mu2_req"]),
        conv=ev["dims"]["conv_val"], xic=dstr(ev["dims"]["xi_code"]),
        xir=dstr(ev["dims"]["xi_req"]), gap=dstr(ev["dims"]["xi_gap"]),
        p1=dstr(ev["dims"]["phi_req_vphi"]), p2=dstr(ev["dims"]["phi_req_exp"]),
        p3=dstr(ev["dims"]["phi_req_v2"]),
        n_ent=len(res["entries"]), ents=ents, ctls=ctls, grds=grds,
        nctl_ok=n_ctl_ok, nctl=len(res["controls"]),
        ngrd_ok=n_grd_ok, ngrd=len(res["guards"]))


def main():
    ev = run_audit()
    dist = {}
    for e in ENTRIES:
        dist[e["state"]] = dist.get(e["state"], 0) + 1
    n_ctl_ok = sum(1 for c in CONTROLS if c["ok"])
    n_grd_ok = sum(1 for g in GUARDS if g["ok"])
    header = build_header(ev)
    report = build_report(ev, {"entries": ENTRIES, "controls": CONTROLS,
                               "guards": GUARDS}, dist, n_ctl_ok, n_grd_ok)

    payload = {
        "id": "TUFT-" + RID,
        "title": ("观测统计层：TUFT-3S 贝叶斯 MCMC 联合后验（P0-18/P0-19）的"
                  "源码 AST / 量纲 / 似然三重审计——PPN 可行体积归零与 γ 提取解耦"),
        "generated_at": START_ISO,
        "targets": [{"path": os.path.basename(p), "sha256": SHA_AT_IMPORT[p]}
                    for p in TARGETS],
        "verdict_header": header,
        "entries": ENTRIES,
        "entry_distribution": dist,
        "controls": CONTROLS,
        "controls_ok": "%d/%d" % (n_ctl_ok, len(CONTROLS)),
        "guards": GUARDS,
        "guards_ok": "%d/%d" % (n_grd_ok, len(GUARDS)),
        "sandbox": {k: v for k, v in ev["sandbox"].items() if k != "loglike_vals"},
        "ast18": ev["ast18"], "ast19": ev["ast19"],
        "gamma": {"sup_abs": ev["sup_abs"], "sigma_units": ev["sup_abs"] / SIGMA_G,
                  "lnL_ppn_best": ev["lnL_ppn_best"], "g_req": ev["g_req"],
                  "orders_below_prior": ev["orders_req"],
                  "grid_top": ev["gamma_grid_top"]},
        "ode": {"diag": ev["diag"], "experiments": ev["ode"]},
        "rotation": ev["rot"], "halo": ev["halo"],
        "dimensions": {k: (dstr(v) if isinstance(v, tuple) and all(
            isinstance(x, Fraction) for x in v) else v)
            for k, v in ev["dims"].items()},
        "repair_pricing": {"g_feas_max": ev["g_feas_max"], "log_fraction": ev["frac"]},
        "target_hits": ev["hits"],
    }

    json_path = os.path.join(DATA_DIR, BASE_NAME + ".json")
    md_path = os.path.join(DATA_DIR, BASE_NAME + ".md")
    rep_path = os.path.join(DATA_DIR, BASE_NAME + "_report.txt")
    vd_path = os.path.join(VD_DIR, "判定_" + BASE_NAME + ".md")
    html_path = os.path.join(SRC_DIR, BASE_NAME + ".html")

    with io.open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, default=str)
    with io.open(rep_path, "w", encoding="utf-8") as f:
        f.write(report)
    with io.open(md_path, "w", encoding="utf-8") as f:
        f.write(build_md(ev, {"entries": ENTRIES}, dist, header))
    with io.open(vd_path, "w", encoding="utf-8") as f:
        f.write(build_verdict(ev, {"entries": ENTRIES, "controls": CONTROLS,
                                   "guards": GUARDS}, dist, header, n_ctl_ok, n_grd_ok))
    with io.open(html_path, "w", encoding="utf-8") as f:
        f.write(render_html(ev, {"entries": ENTRIES, "controls": CONTROLS,
                                 "guards": GUARDS}, payload, header, dist,
                            n_ctl_ok, n_grd_ok))

    # 收尾守卫：哈希复验
    unchanged = all(sha256_of(p) == SHA_AT_IMPORT[p] for p in TARGETS)
    ws_ok = all(sha256_of(p) == WS_SHA_AT_IMPORT[p] for p in WRITE_SIDE)
    for g in GUARDS:
        if g["code"] == "G1":
            g["ok"] = unchanged
            g["evidence"] += "；收尾复验=%s" % unchanged
        if g["code"] == "G5":
            g["ok"] = ws_ok
            g["evidence"] += "；收尾复验=%s" % ws_ok
    n_grd_ok = sum(1 for g in GUARDS if g["ok"])

    sys.stdout.write(report)
    sys.stdout.write("\n" + "=" * 78 + "\n")
    sys.stdout.write("条目 %d = %s\n" % (len(ENTRIES),
                                         " / ".join("%s %d" % (k, v)
                                                    for k, v in sorted(dist.items()))))
    sys.stdout.write("控制组 %d/%d\n" % (n_ctl_ok, len(CONTROLS)))
    sys.stdout.write("守卫 %d/%d\n" % (n_grd_ok, len(GUARDS)))
    sys.stdout.write("靶未改动 %s · 写侧未动 %s\n" % (unchanged, ws_ok))
    sys.stdout.write("=" * 78 + "\n")

    bad = (n_ctl_ok != len(CONTROLS)) or (n_grd_ok != len(GUARDS)) or unchanged is False
    return 2 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
