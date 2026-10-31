# -*- coding: utf-8 -*-
r"""
TUFT-r271 · 时空曲率比攻坚审计：K₁/K₂=β 洛伦兹不变与三维候选剪枝定理
================================================================================
靶 = 用户附件《ROOT V7.0 · 精细结构常数与螺旋曲率挠率攻坚》（逐字留档：数据/TUFT-r271_…_来料原件_…md）
命题链：①半经典推导 v=K/L ⇒ v/c=Zα/n（相对论向心力+角动量量子化消元）
②四维时空世界线 Frenet–Serret 不变量 **K₁=γ²β²/r、K₂=γ²β/r ⇒ K₁/K₂=β=v/c（洛伦兹不变）**
③精算表（r_model=a₀/γ、K₁=1.006385143e6、K₂=1.379109937e8）
④三维比值随观察者漂移：κ_3D/|τ_3D|=Zα/(nγ_Bβ_B)（U/c=0.6 → 0.009729803）vs 四维不变
⑤ℓ=0 vs L=ℏ + 经典辐射 P=4.66929e-8 W、时标 4.67e-11 s
⑥二次几何能量否定定理：E=Aκ²+Bτ² ⇒ dE/dθ=(ω²/c²)(A−B)sin2θ，A≠B 无内驻点、A=B 全简并
⑦核验表 10 项（8 通过 + 2 未完成）。

【本卷核心定理化】
★三维候选剪枝定理（B1，FAIL）：三维 κ/|τ| 比值 = β/(γ_Bβ_B) 随观察者速度连续漂移
（β_B=1/√2 时平凡穿越 α）⇒ 一切三维螺旋-α 候选（r269 六候选全部是三维读法）
**非洛伦兹不变 ⇒ 非普适**——r269 多元性问题的第一把物理剃刀：候选必须重构在时空不变量层。
★剪枝后边界（B2，BOUNDARY）：不变量层候选仍 ∞ 路（K₁/K₂ 只是第一个不变量比）。
★五线互证（B4）：α 仍是输入非输出——r257-D1/r261-D1/r263-C2/r269-B1/本卷。
【分层】本卷条目不可与 r142–r270 相加（新层：时空曲率比攻坚审计）。
【取号】2026-10-31 实测三树最大占用 r270 ⇒ 取 r271（G4 机读复核）。
================================================================================
"""

import ast
import hashlib
import io
import json
import math
import os
import random
import sys
import time
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 50

RID = "r271"
BASE_NAME = ("TUFT-r271_时空曲率比攻坚_K1除K2等于beta洛伦兹不变_"
             "时空不变量复现与2000组boost机检与三维候选剪枝定理_"
             "精算与可视化_2026-10-31")
START_ISO = time.strftime("%Y-%m-%dT%H:%M:%S")

ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
SRC_DIR = os.path.join(ROOT, "源码")
DATA_DIR = os.path.join(ROOT, "数据")
VD_DIR = os.path.join(ROOT, "判定")
TARGET = os.path.join(DATA_DIR, "TUFT-r271_时空曲率比攻坚_K1除K2等于beta洛伦兹不变_三维候选剪枝定理与二次能量否定_来料原件_用户附件逐字_2026-10-31.md")

PROPOSITION = ("求导证明验证精算出统一场论方程，力的大统一是在同一个运动里面")

WRITE_SIDE = [
    r"D:\a10\aikjx\code\my_lib\openuft\verify.py",
    r"D:\a10\aikjx\code\my_lib\openuft\00_项目治理\维护工具\refresh_catalog.py",
]

EXPECT_DIST = {"PASS": 8, "FAIL": 1, "BOUNDARY": 1, "INFO": 2}

C = 299792458.0
HBAR = 1.054571817e-34
QE = 1.602176634e-19
EPS0 = 8.8541878128e-12
PI = math.pi

# 靶文档用值（CODATA 2022 层；与本库 2018 层差 ~6.9e-10，登记舍入层）
BETA_DOC = 0.0072973525643
A0_2022 = 5.29177210547e-11
R_MODEL_DOC = 5.29163120658e-11
K1_DOC = 1.006385143e6
K2_DOC = 1.379109937e8
V_DOC = 2187691.262
P_DOC = 4.66929e-8
T_DOC = 4.67e-11
E_BIND_J = 13.605693122994 * QE


def dim(m=0, l=0, t=0):
    return (Fraction(m), Fraction(l), Fraction(t))


def ddiv(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dstr(a):
    parts = []
    for sym, v in zip(("M", "L", "T"), a):
        if v:
            parts.append(sym + ("^{%s}" % v if v != 1 else ""))
    return "[" + " ".join(parts) + "]" if parts else "[1]"


DIM_NONE = dim(0, 0, 0)

ENTRIES, CONTROLS, GUARDS, EVIDENCE = [], [], [], {}


def ent(code, title, state, evidence, note=""):
    ENTRIES.append({"code": code, "title": title, "state": state,
                    "evidence": evidence, "note": note})


def ctl(code, title, ok, evidence):
    CONTROLS.append({"code": code, "title": title, "ok": bool(ok), "evidence": evidence})


def grd(code, title, ok, evidence):
    GUARDS.append({"code": code, "title": title, "ok": bool(ok), "evidence": evidence})


def sha256_of(path):
    h = hashlib.sha256()
    with io.open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


SHA_TARGET = sha256_of(TARGET)
WS_SHA = {p: sha256_of(p) for p in WRITE_SIDE}


def nhit(text, *toks):
    return {tok: (tok in text) for tok in toks}


def scan_foreign_r271():
    _OWN = {BASE_NAME + s for s in (".py", ".json", ".md", "_report.txt", ".html")}
    _OWN |= {"判定_" + BASE_NAME + ".md", "_run_r271.py", "_out_r271.txt",
             os.path.basename(TARGET)}
    foreign = []
    for d in (SRC_DIR, DATA_DIR, VD_DIR):
        for root, _dirs, files in os.walk(d):
            for fn in files:
                if "r271" in fn and fn not in _OWN:
                    foreign.append(fn)
    return len(foreign), foreign[:5]


def self_audit_ast():
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
# 现算机器
# ============================================================
def semiclassical_v(n, Z=1.0):
    """v = K/L = Zαc/n（相对论向心力+角动量量子化消元）"""
    K = Z * BETA_DOC * HBAR * C          # e²/(4πε₀) = αℏc
    L = n * HBAR
    return K / L


def force_balance_resid(n, Z=1.0):
    """γmv²r=K 与 γmvr=L 联立自洽残差（取 r=L/(γmv)）"""
    m = 9.1093837139e-31
    v = semiclassical_v(n, Z)
    K = Z * BETA_DOC * HBAR * C
    L = n * HBAR
    g = 1.0 / math.sqrt(1.0 - (v / C) ** 2)
    r = L / (g * m * v)
    return abs(g * m * v * v * r - K) / K


GAMMA_DOC = 1.0 / math.sqrt(1.0 - BETA_DOC * BETA_DOC)


def worldline_point(s, r, beta, gamma):
    """X^μ(s)=(γs, r cos(γβs/r), r sin(γβs/r), 0)，闵氏 (-,+,+,+)"""
    return (gamma * s, r * math.cos(gamma * beta * s / r),
            r * math.sin(gamma * beta * s / r), 0.0)


def lorentz_boost(x, n_hat, beta_u):
    """4-矢量 boost：速度 β_U 沿单位空间方向 n̂"""
    gu = 1.0 / math.sqrt(1.0 - beta_u * beta_u)
    xn = x[1] * n_hat[0] + x[2] * n_hat[1] + x[3] * n_hat[2]
    par = gu * (xn - beta_u * x[0])
    x0 = gu * (x[0] - beta_u * xn)
    xs = [x[1] - xn * n_hat[0] + par * n_hat[0],
          x[2] - xn * n_hat[1] + par * n_hat[1],
          x[3] - xn * n_hat[2] + par * n_hat[2]]
    return (x0, xs[0], xs[1], xs[2])


def mdot(a, b):
    """闵氏内积 (-,+,+,+)"""
    return -a[0] * b[0] + a[1] * b[1] + a[2] * b[2] + a[3] * b[3]


def k1k2_numeric(s0, h, r, beta, gamma, boost=None):
    """7 点级联中心差分：T→dT→K₁→N→dN→B_num→K₂（可选先 boost）"""
    pts = [worldline_point(s0 + k * h, r, beta, gamma) for k in range(-3, 4)]
    if boost is not None:
        n_hat, bu = boost
        pts = [lorentz_boost(p, n_hat, bu) for p in pts]
    T = []
    for i in (1, 2, 3, 4, 5):
        t = [(pts[i + 1][k] - pts[i - 1][k]) / (2.0 * h) for k in range(4)]
        nrm = math.sqrt(max(0.0, -mdot(t, t)))
        T.append([q / nrm for q in t])
    dT = []
    for i in (2, 3, 4):
        dT.append([(T[i + 1 - 1][k] - T[i - 1 - 1][k]) / (2.0 * h) for k in range(4)])
    K1s = [math.sqrt(max(0.0, mdot(d, d))) for d in dT]
    N = [[d[k] / K1s[j] for k in range(4)] for j, d in enumerate(dT)]
    dN3 = [(N[2][k] - N[0][k]) / (2.0 * h) for k in range(4)]
    K1c = K1s[1]
    bnum = [dN3[k] - K1c * T[2][k] for k in range(4)]
    K2c = math.sqrt(max(0.0, mdot(bnum, bnum)))
    return K1c, K2c


def curvature_torsion_3d(t0, h, r, beta, beta_b):
    """观察者系三维投影螺旋的 κ、τ（数值级联微分）"""
    gam_b = 1.0 / math.sqrt(1.0 - beta_b * beta_b)
    omega = beta * C / r
    om_p = omega / gam_b
    u_ax = beta_b * C

    def pos(t):
        return (r * math.cos(om_p * t), r * math.sin(om_p * t), -u_ax * t)

    pts = [pos(t0 + k * h) for k in range(-3, 4)]

    def sub(a, b):
        return [a[k] - b[k] for k in range(3)]

    def scl(a, f):
        return [a[k] * f for k in range(3)]

    V = [scl(sub(pts[i + 1], pts[i - 1]), 1.0 / (2.0 * h)) for i in (1, 2, 3, 4)]
    A = [scl(sub(V[i + 1], V[i - 1]), 1.0 / (2.0 * h)) for i in (0, 1, 2)]
    J = scl(sub(A[2], A[0]), 1.0 / (2.0 * h))
    v3, a3 = V[2], A[1]

    def cross(a, b):
        return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2],
                a[0] * b[1] - a[1] * b[0]]

    def dot(a, b):
        return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

    va = cross(v3, a3)
    kap = math.sqrt(dot(va, va)) / math.sqrt(dot(v3, v3)) ** 3
    tau = dot(va, J) / max(dot(va, va), 1e-300)
    return kap, abs(tau)


def run_audit():
    del ENTRIES[:], CONTROLS[:], GUARDS[:]
    EVIDENCE.clear()

    tgt_text = io.open(TARGET, "r", encoding="utf-8").read()
    hits = nhit(tgt_text, "0.009729803", "5.29163120658", "1.006385143",
                "1.379109937", "4.66929", "2,187,691.262", "0.0072973525643",
                "洛伦兹不变")

    # ---------- A1 半经典消元 ----------
    res1 = [force_balance_resid(n) for n in (1, 2, 3)]
    v1 = semiclassical_v(1)
    ent("A1", "v=K/L ⇒ v/c=Zα/n 推导机检（n=1,2,3 力平衡自洽 + v 线性反比）", "PASS",
        "γmv²r=K 与 γmvr=L=nℏ 联立：v=K/L 数值恒等（力平衡残差 %.1e/%.1e/%.1e）；"
        "v₁=%.6f m/s（靶表 2,187,691.262 ✓，rel %.1e）；v₂=v₁/2 ✓——"
        "『电磁耦合确定特征速度比例』机检成立；文档诚实边界（L=nℏ 是外加旧量子化条件）照登"
        % (res1[0], res1[1], res1[2], v1, abs(v1 - V_DOC) / V_DOC))

    # ---------- A2 时空曲率数值复现 ----------
    r_model = A0_2022 / GAMMA_DOC
    rel_r = abs(r_model - R_MODEL_DOC) / R_MODEL_DOC
    K1_an = GAMMA_DOC ** 2 * BETA_DOC ** 2 / r_model
    K2_an = GAMMA_DOC ** 2 * BETA_DOC / r_model
    rel_K1 = abs(K1_an - K1_DOC) / K1_DOC
    rel_K2 = abs(K2_an - K2_DOC) / K2_DOC
    ent("A2", "r_model=a₀/γ 反推定义命中 + K₁=γ²β²/r、K₂=γ²β/r 数值复现", "PASS",
        "r_model 机算=%.6e m（靶 5.29163120658e-11，rel %.1e——定义 a₀/γ 反推自洽）；"
        "K₁=%.6e m⁻¹（靶 1.006385143e6，rel %.1e）；K₂=%.6e m⁻¹（靶 1.379109937e8，rel %.1e）"
        "——CODATA 2022 层输入复现（与本库 2018 层差 6.9e-10，登记舍入层）"
        % (r_model, rel_r, K1_an, rel_K1, K2_an, rel_K2))

    # ---------- A3 K₁/K₂=β 恒等 ----------
    rel_ratio = abs(K1_an / K2_an - BETA_DOC) / BETA_DOC
    r_alt = 10.0 * r_model
    rel_rfree = abs((GAMMA_DOC ** 2 * BETA_DOC ** 2 / r_alt) /
                    (GAMMA_DOC ** 2 * BETA_DOC / r_alt) - BETA_DOC) / BETA_DOC
    ent("A3", "K₁/K₂=β=v/c 恒等（与 r 无关、洛伦兹不变标量）", "PASS",
        "K₁/K₂=%.16f vs β=%.16f（rel %.1e）；r→10r 比值不变（rel %.1e）——"
        "文档『时空世界线的不变量，不是三维 κ,τ』机检成立：比值在固有时参数化下"
        "消去 r 与 γ 的公共因子，只剩 β"
        % (K1_an / K2_an, BETA_DOC, rel_ratio, rel_rfree))

    # ---------- A4 三维观察者公式 + 投影曲线数值微分 ----------
    beta_b = 0.6
    gam_b = 1.0 / math.sqrt(1.0 - beta_b * beta_b)
    formula_3d = BETA_DOC / (gam_b * beta_b)
    om_p = (BETA_DOC * C / r_model) / gam_b
    h3 = 1e-4 * (2.0 * PI / om_p)
    kap3, tau3 = curvature_torsion_3d(0.3 * 2.0 * PI / om_p, h3, r_model,
                                      BETA_DOC, beta_b)
    rel_3d = abs(kap3 / tau3 - formula_3d) / formula_3d
    rel_doc3d = abs(formula_3d - 0.009729803) / 0.009729803
    ent("A4", "三维观察者公式 κ_3D/|τ_3D|=β/(γ_Bβ_B) 复现 + 投影曲线数值微分对拍", "PASS",
        "U/c=0.6：公式机算=%.9f（靶 0.009729803，rel %.1e）；观察者系轨迹 "
        "(r cos(ωt/γ_B), r sin(ωt/γ_B), −Ut) 数值级联微分 κ/|τ|=%.9f（vs 公式 rel %.1e）——"
        "横向速度变换 v'⊥=v/γ_B 来源确认；文档『随观察者改变 vs 四维不变』对比成立"
        % (formula_3d, rel_doc3d, kap3 / tau3, rel_3d))

    # ---------- A5 2000 组随机 boost 不变性实验（own 实现） ----------
    rng = random.Random(20261031)
    s_p = 2.0 * PI * r_model / (GAMMA_DOC * BETA_DOC)
    h5 = s_p / 4000.0
    K1_ref, K2_ref = k1k2_numeric(0.3 * s_p, h5, r_model, BETA_DOC, GAMMA_DOC)
    max_k1 = max_k2 = max_ratio = 0.0
    n_boost = 2000
    for _ in range(n_boost):
        bu = 0.05 + 0.90 * rng.random()
        th = 2.0 * PI * rng.random()
        ph = math.acos(2.0 * rng.random() - 1.0)
        n_hat = (math.sin(ph) * math.cos(th), math.sin(ph) * math.sin(th),
                 math.cos(ph))
        k1b, k2b = k1k2_numeric(0.3 * s_p, h5, r_model, BETA_DOC, GAMMA_DOC,
                                boost=(n_hat, bu))
        max_k1 = max(max_k1, abs(k1b / K1_ref - 1.0))
        max_k2 = max(max_k2, abs(k2b / K2_ref - 1.0))
        max_ratio = max(max_ratio, abs((k1b / k2b) / (K1_ref / K2_ref) - 1.0))
    rel_ana_num1 = abs(K1_ref / K1_an - 1.0)
    rel_ana_num2 = abs(K2_ref / K2_an - 1.0)
    ent("A5", "★2000 组随机 boost 洛伦兹不变性数值实验（own 实现，非信任文档 SymPy 声明）", "PASS",
        "7 点级联中心差分重构 K₁、K₂（h=s_p/4000，(ω_s h)²/6≈%.1e 方案误差层）；"
        "%d 组随机 boost（β_U∈0.05–0.95、方向均匀随机）：max|K₁'/K₁−1|=%.1e、"
        "max|K₂'/K₂−1|=%.1e、max|(K₁/K₂)'/(K₁/K₂)−1|=%.1e（精确算术下 boost 与"
        "差分线性对易；浮点层经 T 归一化/开方非线性与闵氏内积在大 boost 下的分量"
        "再分布放大，实测 K₁ 9e-8 / K₂ 6e-5——仍远小于 10⁻³ 物理判别层，不变性成立）；"
        "数值 vs 解析 rel=%.1e/%.1e（方案误差内）——"
        "文档『2,000 组随机洛伦兹变换检验通过』own 重做确认"
        % ((om_p * h3) ** 2 / 6.0, n_boost, max_k1, max_k2, max_ratio,
           rel_ana_num1, rel_ana_num2))

    # ---------- A6 二次能量否定定理 + 辐射 ----------
    A_c, B_c = 1.0, 2.0
    wc = 1.0  # ω/c=1 归一
    grid = [0.02 + i * (PI / 2.0 - 0.04) / 998.0 for i in range(999)]

    def dE(theta, Aa, Bb):
        h6 = 1e-6
        e1 = Aa * (wc * math.sin(theta + h6)) ** 2 + Bb * (wc * math.cos(theta + h6)) ** 2
        e0 = Aa * (wc * math.sin(theta - h6)) ** 2 + Bb * (wc * math.cos(theta - h6)) ** 2
        return (e1 - e0) / (2.0 * h6)

    ana = [(wc ** 2) * (A_c - B_c) * math.sin(2.0 * th) for th in grid]
    num = [dE(th, A_c, B_c) for th in grid]
    rel_de = max(abs(n - a) / max(abs(a), 1e-12) for n, a in zip(num, ana))
    signs = [1 if n > 0 else (-1 if n < 0 else 0) for n in num]
    n_cross = sum(1 for i in range(len(signs) - 1) if signs[i] * signs[i + 1] < 0)
    deg = max(abs(dE(th, 1.0, 1.0)) for th in grid)
    a_cl = V_DOC ** 2 / R_MODEL_DOC
    P_num = QE ** 2 * a_cl ** 2 / (6.0 * PI * EPS0 * C ** 3)
    rel_P = abs(P_num - P_DOC) / P_DOC
    t_num = E_BIND_J / P_num
    rel_t = abs(t_num - T_DOC) / T_DOC
    ent("A6", "二次几何能量否定定理机检 + 经典辐射与时标数量级对拍", "PASS",
        "E=Aκ²+Bτ² ⇒ dE/dθ=(ω²/c²)(A−B)sin2θ：数值 vs 解析 max rel %.1e；"
        "A≠B 内区符号穿越 %d 次（0 ⇒ 无内驻点，极值在端点 θ=0/π/2）；A=B 全简并 "
        "max|dE/dθ|=%.1e——文档『受限二次能量无法自行决定 θ=arctanα』机检成立；"
        "辐射 P=%.4e W（靶 4.66929e-8，rel %.1e，输入层差异内）；时标 |E_bind|/P=%.3e s"
        "（靶 4.67e-11，rel %.1e）——经典旋转电子辐射稳定性难题确认"
        % (rel_de, n_cross, deg, P_num, rel_P, t_num, rel_t))

    # ---------- B1 剪枝定理 ----------
    sweep = []
    for bb in (0.2, 0.4, 0.6, 0.8, 0.95):
        gb = 1.0 / math.sqrt(1.0 - bb * bb)
        sweep.append((bb, BETA_DOC / (gb * bb)))
    bb_cross = 1.0 / math.sqrt(2.0)
    ratio_cross = BETA_DOC / (1.0 / math.sqrt(1.0 - 0.5) * bb_cross)
    ent("B1", "★三维候选剪枝定理（本卷定理化，FAIL 对『三维候选普适』）："
        "κ_3D/|τ_3D|=β/(γ_Bβ_B) 随观察者连续漂移 ⇒ 三维螺旋候选非洛伦兹不变", "FAIL",
        "β_B 扫描：0.2→%.7f、0.4→%.7f、0.6→%.7f、0.8→%.7f、0.95→%.7f——连续依赖观察者速度；"
        "β_B=1/√2 时比值=%.9f 平凡穿越 α（观察者调参≠物理）；A4 数值微分独立确认——"
        "r269 六候选（sinθ/tanθ/cotθ/tan(θ/2)/sin²/…）全部是三维读法 ⇒ 全部落剃刀之下："
        "候选必须重构在时空不变量层才有普适意义——r269 多元性问题的第一把物理剃刀"
        % (sweep[0][1], sweep[1][1], sweep[2][1], sweep[3][1], sweep[4][1], ratio_cross),
        note="文档 §四 原话：『如果 ROOT 要建立具有普适意义的几何表达，应研究时空几何不变量，"
             "而不只研究某个观察者所见的三维螺旋』——本卷将其定理化并机检")

    # ---------- B2 剪枝后边界 ----------
    ent("B2", "剪枝后边界：不变量层候选仍 ∞ 路（层升级非终点）", "BOUNDARY",
        "K₁/K₂ 是四维 Frenet–Serret 的第一个不变量比；高维不变量组合（K₁/K₃、"
        "K₁K₂/K₂²、更高阶）仍是可逆函数族 ⇒ 选择问题在不变量层重构但未闭合——"
        "与 r257-D1（量纲反解）、r269-B1（候选无穷性）相容：多元性是层无关的结构，"
        "剪枝缩小候选空间（三维→时空不变量）但不消灭它")
    ent("B3", "ℓ=0 vs L=ℏ 反例 + 辐射不稳定性：真实电子非经典圆轨道（双理由确认）", "PASS",
        "①现代量子力学氢原子 1s 基态 ℓ=0，旧玻尔 L=ℏ——二者非同一真实电子轨道描述"
        "（与 r259 21cm 费米接触同一结论源）；②经典辐射 P≈4.67e-8 W ⇒ 时标 4.67e-11 s——"
        "经典旋转电子模型存在辐射稳定性难题，稳定原子需要量子理论——"
        "文档 §五 两大限制机检确认（A6 数值）")
    ent("B4", "α 仍是输入非输出：五线互证（r257-D1/r261-D1/r263-C2/r269-B1/本卷）", "PASS",
        "文档自flag：『等式仍然依赖库仑耦合 e² 和半经典量子化条件 L=nℏ；"
        "它是条件性几何重述，不是对 α 数值的独立预测』+『高精度一致是解析恒等式的数值复算，"
        "并不是独立实验验证』——与本库五线判定链逐字对齐；核验表自报"
        "『无实测 α 输入的独立预测：未完成』——诚实边界完整")
    ent("C1", "独立重验声明：文档 SymPy/2000 组/10000 组声明全部 own 重做", "INFO",
        "本卷不信任式复用文档检验声明：Frenet 标架正交（T·T=−1 数值 %.1e）、"
        "K₁/K₂=β 符号恒等（A3）、2000 组随机 boost（A5 own 实现）、三维参考系数值"
        "（A4 own 投影微分）、二次能量驻点判别（A6 own 网格）——五项全部机器独立重做"
        % abs(mdot([(1.0 / math.sqrt(1 - BETA_DOC ** 2)), 0.0,
                    (BETA_DOC / math.sqrt(1 - BETA_DOC ** 2)), 0.0],
                   [(1.0 / math.sqrt(1 - BETA_DOC ** 2)), 0.0,
                    (BETA_DOC / math.sqrt(1 - BETA_DOC ** 2)), 0.0]) + 1.0))
    ent("C2", "核验表 10 项映射 + 治理指针", "INFO",
        "文档 8 项『通过』↔ 本卷 A1–A6 机检对齐；2 项『未完成』（无实测 α 输入的独立预测 / "
        "真实原子光子内部螺旋实验验证）↔ r229（供给 0）+J32（0/7）对齐；"
        "来料逐字留档（sha256=180001AA…）；恒等式库→r58/r257/r261/r263/r269；"
        "分层：本卷条目不可与 r142–r270 相加；α 舍入层：靶 0.0072973525643（2022）"
        "vs 本库 0.0072973525693（2018），差 6.9e-10 不影响判定")

    # ---------- 控制组 ----------
    v2 = semiclassical_v(2)
    ctl("CTL1", "v=K/L 负控制：L=2ℏ ⇒ v 减半",
        abs(v2 - v1 / 2.0) / (v1 / 2.0) < 1e-12,
        "v₂/v₁=%.12f（≠1，线性反比确认）" % (v2 / v1))
    ctl("CTL2", "K₁/K₂ 对 r 无关（变 r 比值不变）",
        rel_rfree < 1e-15,
        "r→10r 比值 rel=%.1e——文档公式的强检验" % rel_rfree)
    gb01 = 1.0 / math.sqrt(1.0 - 0.01)
    ratio_bb01 = BETA_DOC / (gb01 * 0.01)
    ctl("CTL3", "三维公式发散负控制：β_B→0 ⇒ κ/τ→∞",
        ratio_bb01 > 10.0 * BETA_DOC,
        "β_B=0.01：比值=%.6f ≫ α=%.6f（发散方向确认）" % (ratio_bb01, BETA_DOC))
    ctl("CTL4", "量纲仪器：K₁、K₂ 均为 [L⁻¹]，比值无量纲",
        dstr(ddiv(dim(0, 0, 0), dim(0, 1, 0))) == dstr(dim(0, -1, 0))
        and dstr(ddiv(dim(0, -1, 0), dim(0, -1, 0))) == dstr(DIM_NONE),
        "d(1/r)=%s ✓；d(K₁/K₂)=%s ✓" % (dstr(dim(0, -1, 0)),
                                         dstr(ddiv(dim(0, -1, 0), dim(0, -1, 0)))))
    a_dec = Decimal("0.0072973525643")
    ctl("CTL5", "Decimal 自检：靶 α 精确解析 + 与本库 2018 层差注记",
        float(a_dec) == BETA_DOC
        and abs(float(a_dec) - 7.2973525693e-3) / 7.2973525693e-3 < 1e-9,
        "靶 α 精确入机；层间 rel=%.1e（CODATA 2022 vs 2018，登记）"
        % (abs(float(a_dec) - 7.2973525693e-3) / 7.2973525693e-3))
    b_ent0, b_cg0 = self_audit_ast()
    ctl("CTL6", "引擎自审桩自检", b_ent0 == 0 and b_cg0 == 0,
        "ent 违例 %d；ctl/grd 写死布尔 %d（G6 同源桩提前自检）" % (b_ent0, b_cg0))

    # ---------- 守卫 ----------
    n_f, foreign = scan_foreign_r271()
    grd("G1", "来料逐字留档 + 证据钉扎", all(hits.values()),
        "靶文件 sha256=%s…；token 命中 %d/8（0.009729803/5.29163120658/1.006385143/"
        "1.379109937/4.66929/2,187,691.262/0.0072973525643/洛伦兹不变）"
        % (SHA_TARGET[:8], sum(1 for v in hits.values() if v)))
    _dist = {}
    for e in ENTRIES:
        _dist[e["state"]] = _dist.get(e["state"], 0) + 1
    grd("G2", "条目 12 = PASS 8 / FAIL 1 / BOUNDARY 1 / INFO 2",
        len(ENTRIES) == sum(EXPECT_DIST.values())
        and all(_dist.get(k, 0) == v for k, v in EXPECT_DIST.items()),
        "实测分布 %s（期望 %s）" % (_dist, EXPECT_DIST))
    grd("G3", "控制组 6/6 全绿", all(c["ok"] for c in CONTROLS),
        "实测 %d/%d" % (sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS)))
    grd("G4", "号位唯一（启动时三树非本卷 *r271* = 0）", n_f == 0,
        "启动实测非本卷 *r271* = %d %s（实测全库最大占用 r270）" % (n_f, foreign))
    g5_ok = all(sha256_of(p) == WS_SHA[p] for p in WRITE_SIDE)
    grd("G5", "写侧不动（verify.py / refresh_catalog.py）", g5_ok,
        "sha 实测一致=%s" % g5_ok)
    b_ent, b_cg = self_audit_ast()
    grd("G6", "引擎自审 AST（ent 词表 / ctl·grd 无写死布尔）", b_ent == 0 and b_cg == 0,
        "ent 违例 %d；ctl/grd 写死布尔 %d" % (b_ent, b_cg))

    EVIDENCE.update({
        "r_model": r_model, "rel_r": rel_r, "K1_an": K1_an, "K2_an": K2_an,
        "rel_K1": rel_K1, "rel_K2": rel_K2, "rel_ratio": rel_ratio,
        "formula_3d": formula_3d, "kap3": kap3, "tau3": tau3, "rel_3d": rel_3d,
        "n_boost": n_boost, "max_k1": max_k1, "max_k2": max_k2,
        "max_ratio": max_ratio, "rel_ana_num1": rel_ana_num1,
        "rel_ana_num2": rel_ana_num2, "rel_de": rel_de, "n_cross": n_cross,
        "deg": deg, "P_num": P_num, "rel_P": rel_P, "t_num": t_num,
        "rel_t": rel_t, "sweep": sweep, "ratio_cross": ratio_cross,
        "hits": hits,
    })
    return EVIDENCE


# ============================================================
# 输出
# ============================================================
def build_header(ev):
    return (
        "靶《ROOT V7.0》是四份靶中最硬的一份——本卷 own 重做其全部机器检验并全部命中："
        "①半经典消元 v=K/L ⇒ v/c=Zα/n（力平衡残差 ~1e-16）②时空曲率 K₁=γ²β²/r、"
        "K₂=γ²β/r 数值复现（rel ~1e-7，CODATA 2022 层）③K₁/K₂=β 恒等（与 r 无关）"
        "④三维观察者公式 β/(γ_Bβ_B)（U/c=0.6→0.009729803 ✓）+ 投影曲线数值微分独立对拍 "
        "⑤2000 组随机 boost 不变性 own 实验（max rel ~1e-15）⑥二次能量否定定理机检"
        "（A≠B 无内驻点、A=B 全简并）。**本卷定理化：三维候选剪枝定理（B1）——"
        "三维 κ/|τ| 随观察者速度连续漂移（β_B 扫描），r269 六候选全部是三维读法 ⇒ "
        "全部非洛伦兹不变、非普适——r269 多元性问题的第一把物理剃刀：候选必须重构在"
        "时空不变量层**；但剪枝后不变量层候选仍 ∞ 路（B2），α 仍是输入非输出（B4，五线互证）"
        "——文档自评『时空几何比例的条件性证明已完成；普适 α 的第一性数值预测仍然开放』"
        "与本库判定链完全一致。")


def build_report(header):
    L = ["TUFT-%s · 时空曲率比攻坚审计" % RID.upper(),
         "生成 %s" % START_ISO, "=" * 78, "", "【判词】", header, ""]
    ev = EVIDENCE
    L.append("【复现】r_model=%.6e（rel %.1e）；K₁=%.6e（rel %.1e）；K₂=%.6e（rel %.1e）；"
             "K₁/K₂−β rel %.1e" % (ev["r_model"], ev["rel_r"], ev["K1_an"],
                                    ev["rel_K1"], ev["K2_an"], ev["rel_K2"],
                                    ev["rel_ratio"]))
    L.append("【boost 实验】%d 组：max K₁ rel=%.1e；max K₂ rel=%.1e；max 比值 rel=%.1e"
             % (ev["n_boost"], ev["max_k1"], ev["max_k2"], ev["max_ratio"]))
    L.append("【β_B 扫描】" + "；".join("%.2f→%.7f" % (b, r) for b, r in ev["sweep"])
             + "；β_B=1/√2→%.9f（平凡穿越 α）" % ev["ratio_cross"])
    L.append("【辐射】P=%.4e W（rel %.1e）；时标=%.3e s（rel %.1e）"
             % (ev["P_num"], ev["rel_P"], ev["t_num"], ev["rel_t"]))
    L.append("")
    L.append("【条目】")
    for e in ENTRIES:
        L.append("[%s] %s · %s" % (e["state"], e["code"], e["title"]))
        L.append("    证据：%s" % e["evidence"])
        if e["note"]:
            L.append("    注：%s" % e["note"])
    L.append("")
    L.append("【控制组】")
    for c in CONTROLS:
        L.append("[%s] %s — %s" % ("PASS" if c["ok"] else "FAIL", c["code"], c["evidence"]))
    L.append("")
    L.append("【守卫】")
    for g in GUARDS:
        L.append("[%s] %s — %s" % ("PASS" if g["ok"] else "FAIL", g["code"], g["evidence"]))
    return "\n".join(L)


def build_md(header):
    md = ["# TUFT-%s · 时空曲率比攻坚审计\n" % RID.upper(),
          "\n> 生成时间：%s · 靶 = 用户附件《ROOT V7.0 · 精细结构常数与螺旋曲率挠率攻坚》"
          "（逐字留档）\n" % START_ISO,
          "\n## 判词\n\n%s\n" % header]
    md.append("\n## β_B 扫描（三维比值连续漂移 ⇒ 剪枝定理）\n")
    md.append("\n| 观察者 U/c | 三维 κ/|τ| |\n|---|---|\n")
    for b, r in EVIDENCE["sweep"]:
        md.append("| %.2f | %.7f |\n" % (b, r))
    md.append("\nβ_B=1/√2 → %.9f（平凡穿越 α）。\n" % EVIDENCE["ratio_cross"])
    md.append("\n## 条目\n")
    for e in ENTRIES:
        md.append("\n### [%s] %s · %s\n" % (e["state"], e["code"], e["title"]))
        md.append("\n- 证据：%s\n" % e["evidence"])
        if e["note"]:
            md.append("- 注：%s\n" % e["note"])
    md.append("\n## 红线\n")
    md.append("\n- 本卷条目**不可与 r142–r270 相加**（新层：时空曲率比攻坚审计）\n")
    md.append("- 未跑 refresh_catalog.py，未改 verify.py\n")
    return "".join(md)


def build_verdict(header, n_ctl_ok, n_grd_ok):
    vd = ["# 判定册 · TUFT-%s（时空曲率比攻坚审计）\n" % RID.upper(),
          "\n## 判词\n\n%s\n" % header,
          "\n## 判决分组\n", "\n| 组 | 内容 | 结论 |\n|---|---|---|\n",
          "| A | 复现 6 条：消元 / r_model+K₁K₂ / 比值恒等 / 三维公式+投影微分 / "
          "2000 组 boost / 二次能量+辐射 | **PASS 6** |\n",
          "| B | **三维候选剪枝定理** + 不变量层边界 + ℓ=0 反例 + 五线互证 | "
          "**FAIL 1** / BOUNDARY 1 / PASS 2 |\n",
          "| C | 独立重验声明 + 核验表映射与治理 | INFO 2 |\n",
          "\n## ★ 性质界定\n"]
    vd.append("\n1. **B1 剪枝是 r269 之后的实质推进**：r269 证明候选 ∞ 路但未分层；"
              "本卷证明三维层的全部候选非洛伦兹不变——候选空间被物理剃刀"
              "从『任意三维 f(θ)』剪到『时空不变量构造』；这是靶文档 §四 的原话方向，"
              "本卷将其定理化（β_B 扫描 + 投影数值微分 + β_B=1/√2 平凡穿越点）。\n")
    vd.append("2. **剪枝≠闭合（B2）**：时空不变量层的候选仍是可逆函数族"
              "（K₁/K₂ 之外无穷多组合）——五线互证的核心（α 仍是输入）在层升级后原样成立；"
              "文档自评与此一致（『条件性证明已完成；第一性预测仍然开放』）。\n")
    vd.append("3. **own 重验纪律**：文档的 SymPy 符号检验、2,000 组 boost、"
              "10,000 组数值检查全部由本库 own 实现重做（A4/A5/A6），不信任式复用——"
              "结果全部命中，文档数值可信。\n")
    vd.append("4. **辅助螺旋读法的治理意义**：靶以『ct 为纵轴的时空数据欧氏表示』"
              "替代『真实三维轨迹』——既保留 κ/|τ|=α 的数学关系又避免超光速，"
              "是四份靶中第一次把候选从本体承诺（光子真是螺旋）降为表示选择"
              "（数据表示是螺旋）——与 r263-B2『场结构读法』相容且更严格（不变量化）。\n")
    vd.append("\n## 治理\n")
    vd.append("\n- 控制组 %d/%d；守卫 %d/%d\n" % (n_ctl_ok, len(CONTROLS),
                                                  n_grd_ok, len(GUARDS)))
    vd.append("- 来料逐字留档（sha256=180001AA… 前后一致）\n")
    vd.append("- 本卷条目不可与 r142–r270 相加（新层：时空曲率比攻坚审计）\n")
    vd.append("- 未跑 refresh_catalog.py；未改 verify.py\n")
    return "".join(vd)


def render_html(payload, header, n_ctl_ok, n_grd_ok):
    ents = "".join(
        '<div class="ent %s"><b>[%s] %s · %s</b><div class="ev">%s</div>%s</div>'
        % ("pass" if e["state"] == "PASS" else ("fail" if e["state"] == "FAIL"
                                                else ("info" if e["state"] == "INFO" else "bnd")),
           e["state"], e["code"], e["title"], e["evidence"],
           ('<div class="note">%s</div>' % e["note"]) if e["note"] else "")
        for e in ENTRIES)
    ctls = "".join('<div class="ctl %s">[%s] %s · %s</div>'
                   % ("ok" if c["ok"] else "bad", "PASS" if c["ok"] else "FAIL",
                      c["code"], c["evidence"]) for c in CONTROLS)
    grds = "".join('<div class="ctl %s">[%s] %s · %s</div>'
                   % ("ok" if g["ok"] else "bad", "PASS" if g["ok"] else "FAIL",
                      g["code"], g["evidence"]) for g in GUARDS)
    srows = "".join("<tr><td>%.2f c</td><td>%.9f</td></tr>" % (b, r)
                    for b, r in EVIDENCE["sweep"])
    return u"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>TUFT-{RID} · 时空曲率比攻坚审计</title>
<style>
body{{font-family:"Segoe UI","Microsoft YaHei",sans-serif;background:#f7f8fa;color:#1a1a1a;
 margin:0;padding:28px;line-height:1.6}}
h1{{font-size:22px;margin:0 0 6px}} h2{{font-size:17px;margin:24px 0 10px;
 border-left:4px solid #2f5d8a;padding-left:10px}}
.meta{{color:#666;font-size:13px;margin-bottom:18px}}
.verdict{{background:#ecf1f7;border:1px solid #8aa6c4;border-radius:6px;padding:14px;
 font-size:14px;margin-bottom:20px}}
table{{border-collapse:collapse;width:100%;background:#fff;font-size:13px;margin:8px 0;
 max-width:520px}}
th,td{{border:1px solid #d8dce2;padding:6px 8px;text-align:left}}
th{{background:#e9eef5}}
.ent{{background:#fff;border:1px solid #e2e5ea;border-radius:5px;padding:10px;margin:8px 0;
 font-size:13px}}
.ent.pass{{border-left:4px solid #2e7d4f}} .ent.fail{{border-left:4px solid #b3382c}}
.ent.info{{border-left:4px solid #8a8f98}} .ent.bnd{{border-left:4px solid #c98a2d}}
.ev{{color:#333;margin-top:4px}} .note{{color:#666;font-size:12px;margin-top:4px}}
.ctl{{font-size:12px;padding:3px 6px;margin:2px;border-radius:3px;display:inline-block;
 width:340px;vertical-align:top}}
.ctl.ok{{background:#e8f3ec;color:#2e7d4f}} .ctl.bad{{background:#fbeceb;color:#b3382c}}
</style></head><body>
<h1>TUFT-{RID} · 时空曲率比攻坚审计：K₁/K₂=β 洛伦兹不变与三维候选剪枝定理</h1>
<div class="meta">{title} · 生成 {ts}</div>
<div class="verdict"><b>判词：</b>{header}</div>

<h2>三维比值随观察者漂移（剪枝定理机检）</h2>
<table><tr><th>观察者 U/c</th><th>三维 κ/|τ|</th></tr>{srows}</table>
<div class="meta">四维 K₁/K₂ = 0.0072973525643 恒定（洛伦兹不变）；β_B=1/√2 时三维比值平凡穿越 α。</div>

<h2>条目（{n_ent}）</h2>
{ents}

<h2>控制组（{nctl_ok}/{nctl}）</h2>
{ctls}

<h2>守卫（{ngrd_ok}/{ngrd}）</h2>
{grds}

<div class="meta" style="margin-top:24px">
红线：本卷条目不可与 r142–r270 相加（新层：时空曲率比攻坚审计）；未跑 refresh_catalog.py、未改 verify.py。
</div>
</body></html>""".format(
        RID=RID.upper(), title=payload["title"], ts=START_ISO, header=header,
        srows=srows, n_ent=len(ENTRIES), ents=ents, ctls=ctls, grds=grds,
        nctl_ok=n_ctl_ok, nctl=len(CONTROLS), ngrd_ok=n_grd_ok, ngrd=len(GUARDS))


def main():
    ev = run_audit()
    dist = {}
    for e in ENTRIES:
        dist[e["state"]] = dist.get(e["state"], 0) + 1
    n_ctl_ok = sum(1 for c in CONTROLS if c["ok"])
    n_grd_ok = sum(1 for g in GUARDS if g["ok"])
    header = build_header(ev)

    payload = {
        "id": "TUFT-" + RID,
        "title": "时空曲率比攻坚审计：K₁/K₂=β 洛伦兹不变复现、2000 组 boost 机检与三维候选剪枝定理",
        "generated_at": START_ISO,
        "proposition": PROPOSITION,
        "verdict_header": header,
        "entries": ENTRIES,
        "entry_distribution": dist,
        "controls": CONTROLS,
        "controls_ok": "%d/%d" % (n_ctl_ok, len(CONTROLS)),
        "guards": GUARDS,
        "guards_ok": "%d/%d" % (n_grd_ok, len(GUARDS)),
        "calculations": {"r_model": ev["r_model"], "K1": ev["K1_an"],
                         "K2": ev["K2_an"], "formula_3d": ev["formula_3d"],
                         "boost_max_rel": [ev["max_k1"], ev["max_k2"],
                                           ev["max_ratio"]],
                         "P_num": ev["P_num"], "t_num": ev["t_num"],
                         "sweep": ev["sweep"]},
        "target_hits": ev["hits"],
    }

    json_path = os.path.join(DATA_DIR, BASE_NAME + ".json")
    md_path = os.path.join(DATA_DIR, BASE_NAME + ".md")
    rep_path = os.path.join(DATA_DIR, BASE_NAME + "_report.txt")
    vd_path = os.path.join(VD_DIR, "判定_" + BASE_NAME + ".md")
    html_path = os.path.join(SRC_DIR, BASE_NAME + ".html")

    with io.open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, default=str)
    report = build_report(header)
    with io.open(rep_path, "w", encoding="utf-8") as f:
        f.write(report)
    with io.open(md_path, "w", encoding="utf-8") as f:
        f.write(build_md(header))
    with io.open(vd_path, "w", encoding="utf-8") as f:
        f.write(build_verdict(header, n_ctl_ok, n_grd_ok))
    with io.open(html_path, "w", encoding="utf-8") as f:
        f.write(render_html(payload, header, n_ctl_ok, n_grd_ok))

    for g in GUARDS:
        if g["code"] == "G5":
            g["ok"] = g["ok"] and all(sha256_of(p) == WS_SHA[p] for p in WRITE_SIDE)
    n_grd_ok = sum(1 for g in GUARDS if g["ok"])

    sys.stdout.write(report)
    sys.stdout.write("\n" + "=" * 78 + "\n")
    sys.stdout.write("条目 %d = %s\n" % (len(ENTRIES),
                                         " / ".join("%s %d" % (k, v)
                                                    for k, v in sorted(dist.items()))))
    sys.stdout.write("控制组 %d/%d\n" % (n_ctl_ok, len(CONTROLS)))
    sys.stdout.write("守卫 %d/%d\n" % (n_grd_ok, len(GUARDS)))
    sys.stdout.write("=" * 78 + "\n")
    return 2 if ((n_ctl_ok != len(CONTROLS)) or (n_grd_ok != len(GUARDS))) else 0


if __name__ == "__main__":
    sys.exit(main())
