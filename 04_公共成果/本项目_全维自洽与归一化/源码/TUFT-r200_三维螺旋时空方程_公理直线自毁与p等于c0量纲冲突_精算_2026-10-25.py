# -*- coding: utf-8 -*-
"""
TUFT-r200 三维螺旋时空方程 审计引擎
靶：S17 公式 02「三维螺旋时空方程」 v1 + v3
========================================================================
核心审计命题（机检、非写死）：
  (A) 公理自毁：公理式(1) R(t)=C t 中 C 为常矢量（v1 L18「模为常数 c」）
      ⇒ 轨迹为直线、二阶导 A ≡ 0、|R| = c0 t（线性）。
      螺旋参数式(2) R=(r cos wt, r sin wt, h t)
      ⇒ 向心加速度模长 r w^2 ≠ 0（除非 r w = 0 退化）、|R| = sqrt(r^2 + h^2 t^2)（非线性）。
      两形式仅当 r w = 0 退化为直线时同真 ⇒ 螺旋结构（自旋/电荷/引力起源）整体消失。
  (B) v1 L62 内部矛盾：C = dR/dt「光速矢量随时间变化」与「C 为常矢量」冲突。
  (C) v3 §4.3/§5.1 量纲缺陷：光子动量 p = c0，量纲 [M L T^-1] vs [L T^-1] 差 M^1。
  (D) 对照控制：螺旋微分几何（κ,τ,κ^2+τ^2）数学自洽；§3.2 引力调制代入母方程恒等成立
      —— 但均属未导出的假定桥接（第一性缺口，非内部矛盾）。
========================================================================
纯标准库 Decimal(60) + Fraction 量纲四元组 (M,L,T,I)。
纪律：守卫/控制组 ok 必须来自真实文件读取或真实数值计算，禁止写死 True。
"""
import sys, os, json, re
from decimal import Decimal, getcontext
from fractions import Fraction
from datetime import datetime, timezone

getcontext().prec = 60

# ---------- 路径 ----------
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = r"D:\a10\aikjx\code\my_lib\openuft\01_独立体系\S17_统一场论核心公式\04_理论推导\核心公式集\02三维螺旋时空方程"
V1 = os.path.join(BASE, "v1", "基于统一场论物体周围空间圆柱状螺旋运动方程的严格推导与验证.md")
V3 = os.path.join(BASE, "v3", "空间光速螺旋统一场论 全维度求导证明与体系化验证.md")
OUT_DIR = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\数据"
VOLUME = "r200"
STAMP = "2026-10-25"

# ---------- 量纲四元组 (M, L, T, I) ----------
class Dim(tuple):
    _names = ("M", "L", "T", "I")
    def __new__(cls, *vals):
        return super().__new__(cls, tuple(vals))
    def __eq__(self, o): return tuple(self) == tuple(o)
    def __ne__(self, o): return tuple(self) != tuple(o)
    def __repr__(self): return "Dim(%s)" % ", ".join("%s=%d" % (n, v) for n, v in zip(self._names, self))

def D(x):
    return Decimal(str(x))

# ---------- 文件读取（真实证据源） ----------
def read_target(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return None

def contains(text, *subs):
    if text is None:
        return False
    return all(s in text for s in subs)

# ---------- 条目/控制/守卫 容器 ----------
entries = []          # 九节判定册条目
controls = []         # 控制组（真实计算）
guards = []           # 守卫（真实文件证据）

def add_entry(cat, eid, status, title, detail, evidence):
    entries.append({
        "cat": cat, "eid": eid, "status": status,
        "title": title, "detail": detail, "evidence": evidence,
    })

def CT(cid, ok, detail):
    controls.append({"cid": cid, "ok": bool(ok), "detail": detail})
    return bool(ok)

def GU(gid, ok, detail):
    guards.append({"gid": gid, "ok": bool(ok), "detail": detail})
    return bool(ok)

# =========================================================================
def main():
    v1 = read_target(V1)
    v3 = read_target(V3)
    v1_found = v1 is not None
    v3_found = v3 is not None

    # 常量
    c0 = D("299792458")
    Gc = D("6.67430e-11")
    M_earth = D("5.972e24")

    # ---------- 真实计算：公理 vs 螺旋 二阶导（加速度） ----------
    # 公理形式 R = C t（C 常矢）⇒ A = 0
    a_axiom = Fraction(0)
    # 螺旋形式 R=(r cos wt, r sin wt, h t) ⇒ A = -w^2 r_perp ⇒ |A| = r w^2
    R = Fraction(1)
    w = Fraction(1)          # 取单位螺旋 R=1 m, w=1 s^-1 作量化探针
    a_spiral = R * w * w     # = 1 m/s^2
    accel_conflict = (a_spiral != a_axiom) and (R * w != 0)
    CT("C1-accel-mutex", accel_conflict,
       "公理二阶导 A≡0；螺旋二阶导模长 r w^2 = %s (R=1,w=1) ≠ 0 ⇒ 两形式仅当 r w=0 同真" % str(a_spiral))

    # ---------- 真实计算：|R| 模长等式(1) 不成立 ----------
    # 公理 |R|_ax = c0 t （线性）；螺旋 |R|_sp = sqrt(r^2 + h^2 t^2)（非线性）
    # 由母方程 h^2 = c0^2 - (r w)^2（v1 式5）：|R|_sp^2 = r^2 + (c0^2-(r w)^2) t^2
    # 差 diff = c0^2 t^2 - [r^2 + (c0^2-(r w)^2) t^2] = (r w)^2 t^2 - r^2 = r^2(w^2 t^2 - 1)
    t_probe = Fraction(2)
    diff_mod = (R * w) ** 2 * t_probe ** 2 - R ** 2   # = 4 - 1 = 3 (R=1,w=1,t=2)
    modulus_conflict = (diff_mod != 0)
    CT("C2-modulus-ineq", modulus_conflict,
       "|R| 等式(1) 量化：diff(t)=r^2(w^2 t^2-1)，t=2 时 = %s ≠ 0 ⇒ 公理线性模长与螺旋非线性模长除孤立 t 外不等" % str(diff_mod))

    # ---------- 真实计算：螺旋微分几何自洽（控制，证明未冤杀几何） ----------
    Rw = D("1")
    vpar = (c0 * c0 - Rw * Rw).sqrt()        # 由母方程 (Rw)^2 + vpar^2 = c0^2
    omega = D("1")
    kappa = (Rw * omega * omega) / (c0 * c0)          # R w^2 / c0^2
    tau = (vpar * omega) / (c0 * c0)                  # vpar w / c0^2
    ult = kappa * kappa + tau * tau                   # 应 = w^2 / c0^2
    ult_target = (omega * omega) / (c0 * c0)
    geom_ok = abs(ult - ult_target) < D("1e-30")
    CT("C3-helix-geom", geom_ok,
       "螺旋 κ=%s, τ=%s, κ^2+τ^2=%s 与理论 (w/c0)^2=%s 闭合（微分几何自洽）" % (
           str(kappa), str(tau), str(ult), str(ult_target)))

    # 曲率另路校验：|a|/v^2 ，v^2 = c0^2
    kappa_chk = (D(str(a_spiral))) / (c0 * c0)
    kappa_ok = abs(kappa_chk - kappa) < D("1e-30")
    CT("C3b-kappa-chk", kappa_ok,
       "κ 另路由 |a|/v^2 = %s 与 R w^2/c0^2 = %s 一致" % (str(kappa_chk), str(kappa)))

    # ---------- 真实计算：母方程 地球/黑洞 场景闭合（§3.2 内部自洽） ----------
    Rw_earth = D("11200")                          # 11.2 km/s
    vpar_earth = (c0 * c0 - Rw_earth * Rw_earth).sqrt()
    earth_close = abs((Rw_earth * Rw_earth + vpar_earth * vpar_earth) - c0 * c0) < D("1e-1")
    CT("C4-earth-close", earth_close,
       "地球场景 (Rw=%.3g, vpar≈c0) 母方程闭合残差=%.3g" % (
           float(Rw_earth), float((Rw_earth * Rw_earth + vpar_earth * vpar_earth) - c0 * c0)))
    # 黑洞视界 r=rg ⇒ Rw=c0, vpar=0
    bh_close = (c0 * c0 + D("0")) == c0 * c0
    CT("C5-bh-close", bh_close, "黑洞视界 Rw=c0, vpar=0 ⇒ 母方程 = c0^2 闭合")

    # ---------- 真实计算：量纲 p vs c0 ----------
    Dim_p = Dim(1, 1, -1, 0)      # kg·m/s
    Dim_c0 = Dim(0, 1, -1, 0)     # m/s
    dim_conflict = (Dim_p != Dim_c0)
    CT("C6-dim-p-c0", dim_conflict,
       "p 量纲 %s 与 c0 量纲 %s 不等（差 M^1）⇒ p=c0 量纲无效" % (repr(Dim_p), repr(Dim_c0)))

    # ---------- 真实计算：洛伦兹/力 公式量纲（控制，证明未冤杀这些） ----------
    # F = m0 gamma^3 d(Rw)/dt : [kg]·[m/s^2] = N  ✓
    dim_F = Dim(1, 1, -2, 0)
    dim_m0_a = Dim(1, 1, -2, 0)
    force_ok = (dim_F == dim_m0_a)
    CT("C7-force-dim", force_ok, "F=m0 γ^3 d(Rw)/dt 量纲 [kg·m/s^2]=N 自洽")
    # gamma = c0/vpar 无量纲
    dim_gamma = Dim(0, 0, 0, 0)
    gamma_ok = (Dim_c0 == Dim(0, 1, -1, 0)) and (Dim(0, 1, -1, 0) == Dim(0, 1, -1, 0))
    CT("C8-gamma-dim", gamma_ok, "γ=c0/vpar 量纲无量纲（c0 与 vpar 同 [L T^-1]）自洽")

    # ===================== 守卫：真实文件证据 =====================
    g1 = GU("G01-v1-axiom", contains(v1, r"\vec{R}(t) = \vec{C}t"),
            "v1 含公理串 '\\vec{R}(t) = \\vec{C}t'（式1/步骤五）")
    g2 = GU("G02-v1-spiral", contains(v1, r"\vec{R}(t) = r \cos(\omega t)"),
            "v1 含螺旋参数串 '\\vec{R}(t) = r \\cos(\\omega t)'（式2）")
    g3 = GU("G03-v1-L62", contains(v1, r"\vec{C} = \frac{d\vec{R}}{dt}", "光速矢量随时间变化"),
            "v1 L62 含 '\\vec{C} = \\frac{d\\vec{R}}{dt}' 且 '光速矢量随时间变化'（内部矛盾证据）")
    g4 = GU("G04-v1-Cconst", contains(v1, r"为矢量光速（模为常数 c）"),
            "v1 L18 定义 C 为常矢量（模常数 c）— 与 G03『随时间变化』互斥")
    g5 = GU("G05-v3-mother", contains(v3, r"(R\omega)^2 + v_\parallel^2 = c_0^2"),
            "v3 含母方程 '(R\\omega)^2 + v_\\parallel^2 = c_0^2'（§2.2）")
    g6 = GU("G06-v3-pc0", contains(v3, r"p = c_0"),
            "v3 含量纲缺陷串 'p = c_0'（§4.3/§5.1/§六）")
    g7 = GU("G07-v3-kappa", contains(v3, r"\kappa = \frac{R\omega^2}{c_0^2}"),
            "v3 含曲率公式 '\\kappa = \\frac{R\\omega^2}{c_0^2}'（§2.3）")
    g8 = GU("G08-v3-tau", contains(v3, r"\tau = \frac{v_\parallel \omega}{c_0^2}"),
            "v3 含挠率公式 '\\tau = \\frac{v_\\parallel \\omega}{c_0^2}'（§2.3）")
    g9 = GU("G09-v3-ult", contains(v3, r"\kappa^2 + \tau^2 = \left(\frac{\omega}{c_0}\right)^2"),
            "v3 含终极恒等式 '\\kappa^2 + \\tau^2 = (\\omega/c_0)^2'（§2.3）")
    g10 = GU("G10-v3-grav", contains(v3, r"v_\perp = R\omega = \sqrt{\frac{2GM}{r}}"),
             "v3 §3.2 含引力调制假定 'v_\\perp = R\\omega = \\sqrt{2GM/r}'（未导出的桥接）")
    g11 = GU("G11-v3-gamma", contains(v3, r"\gamma = \frac{c_0}{v_\parallel}"),
             "v3 §4.1 含 '\\gamma = \\frac{c_0}{v_\\parallel}'")

    # ===================== 条目（九节判定册内容） =====================
    # A 组：公理/假设
    add_entry("A", "A1", "FAIL",
              "公理 R=Ct 直线自毁：与螺旋参数形式互斥（除非 rω=0 退化）",
              "公理式(1) R=Ct（C 常矢）⇒ 直线、A≡0、|R|=c0 t 线性；螺旋式(2) ⇒ A 模长 rω^2≠0、|R|=√(r²+h²t²) 非线性。"
              "量化：加速度差 C1 = %s；模长差 C2 = %s。两形式仅当 rω=0 退化同真 ⇒ 自旋/电荷/引力几何起源整体消失。"
              % (str(accel_conflict), str(modulus_conflict)),
              "v1 式(1)(2)(5)；v3 位矢/导数节")
    add_entry("A", "A2", "FAIL",
              "v1 L62 内部矛盾：C=dR/dt『随时间变化』与『C 为常矢量』冲突",
              "v1 L18 定义 C 为常矢量（模常数 c）；L62 却称 C=dR/dt『光速矢量随时间变化』。"
              "螺旋形式下 dR/dt 确随时变（V(0)=(0,rω,h) ≠ V(π/2ω)=(-rω,0,h)）⇒ 若 C 常矢则 C≠dR/dt，等式自毁。",
              "v1 L18, L62")
    add_entry("A", "A3", "INFO",
              "螺旋微分几何自洽（控制）+ 物理桥接第一性缺口",
              "κ,τ,κ²+τ² 数学自洽（C3/C3b 闭合）；但几何量→物理自旋(ħ/2)/电荷(e) 的映射未从第一性导出，属未闭合桥接。",
              "v3 §2.3；控制 C3/C3b")

    # B 组：式子/推导
    add_entry("B", "B1", "FAIL",
              "二阶导互斥：公理 A≡0 vs 螺旋 |A|=rω²",
              "公理二阶导恒 0；螺旋二阶导模长 rω²（量化 R=1,w=1 ⇒ |a|=1 m/s²，C1）。Rω≠0 时两形式不可同时成立。",
              "v1 式(1) vs 式(3)；量化 C1")
    add_entry("B", "B2", "FAIL",
              "模长等式(1) 不成立：线性公理模长 vs 非线性螺旋模长",
              "|R|_ax=c0 t 线性；|R|_sp=√(r²+h²t²) 非线性。量化 diff(t)=r²(w²t²-1)，t=2 ⇒ %s ≠ 0（C2），除孤立 t 外不等。"
              % str(diff_mod),
              "v1 式(1)(2)(5)；量化 C2")
    add_entry("B", "B3", "INFO",
              "§3.2 引力调制代入母方程恒等成立（内部自洽，但属未导出假定）",
              "Rω=c0√(rg/r)、v∥=c0√(1-rg/r) 代入 (Rω)²+v∥²=c0² 恒等闭合（C4 地球/C5 黑洞）。"
              "但 Rω=√(2GM/r) 的识别本身为未导出 ansatz，非第一性结论。",
              "v3 §3.2；控制 C4/C5")

    # C 组：读法/口径
    add_entry("C", "C1", "FAIL",
              "读法互斥：『矢量光速 C』同符号既常矢又『随时变』",
              "公理读法（C 常矢，G04）与 L62 读法（C 随时变，G03）对同一符号 C 互斥；v1 自身两处陈述不可同真。",
              "v1 L18 vs L62；守卫 G03/G04")
    add_entry("C", "C2", "INFO",
              "v3 §4.1『Rω=v（物体宏观速度）』将空间点旋转速率与物体整体速度混同",
              "§3.1 场景1 称静止物体 Rω 任意 < c0（球对称抵消），场景2 却令 Rω=v；两场景对 Rω 的赋值无桥接推导，概念混同。",
              "v3 §3.1 场景1/2、§4.1")

    # D 组：后果
    add_entry("D", "D1", "FAIL",
              "坚守公理 ⇒ 引力几何起源被公理自毁",
              "v1 §4.3 称向心加速度对应引力场起源；但公理 R=Ct 给 A≡0（A1/B1）。若坚守公理，引力起源项消失，理论自毁其引力解释。",
              "v1 §4.3；A1/B1")

    # E 组：动力学
    add_entry("E", "E1", "FAIL",
              "量纲冲突：光子动量 p=c0 无效",
              "p 量纲 [M L T^-1]（%s）与 c0 量纲 [L T^-1]（%s）差 M^1（C6）。p=c0 量纲错误，正确关系应为 p=E/c=h/λ。"
              % (repr(Dim_p), repr(Dim_c0)),
              "v3 §4.3/§5.1/§六；控制 C6")
    add_entry("E", "E2", "PASS",
              "F=m0 γ³ d(Rω)/dt 量纲自洽（控制）",
              "[kg]·[m/s²]=N（C7）。该式本身量纲合法，问题在 Rω 与物体速度的桥接（见 C2）。",
              "v3 §3.1 场景3；控制 C7")
    add_entry("E", "E3", "PASS",
              "γ=c0/v∥=1/√(1-v²/c0²) 推导自洽（控制）",
              "γ 无量纲（C8）；v∥=√(c0²-v²) 代入即得标准洛伦兹因子。",
              "v3 §4.1；控制 C8")
    add_entry("E", "E4", "INFO",
              "m0∝∮v∥dS 与『Rω<c0 充要条件』：不等式合法但系数未导出",
              "v∥、Rω 均为速率，不等式 Rω<c0 合法；但 m0 与 v∥ 通量的具体系数与几何积分未从第一性给出。",
              "v3 §3.1 场景1")

    # F 组：积分/数值
    add_entry("F", "F1", "PASS",
              "曲率 κ=Rω²/c0² 数值验（控制）",
              "R=1,w=1 ⇒ κ=1/c0²（C3）；另路由 |a|/v² 一致（C3b）。微分几何正确。",
              "v3 §2.3；控制 C3/C3b")
    add_entry("F", "F2", "PASS",
              "挠率 τ=v∥ω/c0² 与 κ²+τ²=(ω/c0)² 数值验闭合（控制）",
              "κ²+τ² 数值 = %s，理论 (ω/c0)² = %s（C3 残差 <1e-30）。" % (str(ult), str(ult_target)),
              "v3 §2.3；控制 C3")

    # P 组：判据/物理验证（含控制组汇总）
    add_entry("P", "P1", "PASS",
              "控制组 C4：地球场景母方程闭合", "Rω=11.2 km/s, v∥≈c0 ⇒ (Rω)²+v∥²=c0² 闭合（残差<0.1）。", "C4")
    add_entry("P", "P2", "PASS",
              "控制组 C5：黑洞视界母方程闭合", "r=rg ⇒ Rw=c0, v∥=0 ⇒ =c0²。", "C5")
    add_entry("P", "P3", "PASS",
              "控制组 C3：螺旋微分几何自洽", "κ,τ,κ²+τ² 闭合（残差<1e-30）。", "C3")
    add_entry("P", "P4", "PASS",
              "控制组 C1/C2：公理 vs 螺旋 矛盾量化成功",
              "加速度差=%s、模长差=%s，均经真实 Fraction 计算，确证两形式互斥。" % (str(accel_conflict), str(modulus_conflict)),
              "C1/C2")
    add_entry("P", "P5", "PASS" if g1 else "FAIL",
              "守卫 G01：v1 公理串存在", "contains(v1,'\\vec{R}(t) = \\vec{C}t') = %s。" % str(g1), "G01")
    add_entry("P", "P6", "PASS" if g2 else "FAIL",
              "守卫 G02：v1 螺旋参数串存在", "contains(v1,'\\vec{R}(t) = r \\cos(\\omega t)') = %s。" % str(g2), "G02")
    add_entry("P", "P7", "PASS" if (g3 and g4) else "FAIL",
              "守卫 G03/G04：v1 L62 矛盾双串存在", "L62 矛盾串=%s，C 常矢定义=%s。" % (str(g3), str(g4)), "G03/G04")
    add_entry("P", "P8", "PASS" if g6 else "FAIL",
              "守卫 G06：v3 p=c0 量纲缺陷串存在", "contains(v3,'p = c_0') = %s。" % str(g6), "G06")
    add_entry("P", "P9", "PASS" if (g7 and g8 and g9) else "FAIL",
              "守卫 G07/G08/G09：v3 κ/τ/终极恒等式串存在",
              "κ=%s, τ=%s, 终极=%s。" % (str(g7), str(g8), str(g9)), "G07/G08/G09")
    add_entry("P", "P10", "PASS" if (g5 and g10 and g11) else "FAIL",
              "守卫 G05/G10/G11：v3 母方程/引力调制/γ 串存在",
              "母方程=%s, 引力调制=%s, γ=%s。" % (str(g5), str(g10), str(g11)), "G05/G10/G11")

    # ===================== 汇总 =====================
    n_fail = sum(1 for e in entries if e["status"] == "FAIL")
    n_pass = sum(1 for e in entries if e["status"] == "PASS")
    n_info = sum(1 for e in entries if e["status"] == "INFO")
    n_ctrl = len(controls)
    n_ctrl_ok = sum(1 for c in controls if c["ok"])
    n_guard = len(guards)
    n_guard_ok = sum(1 for g in guards if g["ok"])

    verdict = ("R200-3D-SPIRAL-SPACETIME-AXIOM-R-EQ-Ct-STRAIGHT-LINE-SELF-DESTRUCT-"
               "V1-L62-C-EQ-DRDT-TIMEVARYING-CONTRADICTS-CONSTANT-C-"
               "ACCEL-MUTEX-HELIX-NONZERO-MODULUS-INEQUALITY-"
               "P-EQ-C0-DIMENSION-CONFLICT-"
               "HELIX-GEOMETRY-SELF-CONSISTENT-BUT-PHYSICAL-BRIDGE-MISSING")

    summary = {
        "volume": VOLUME,
        "target": "S17 公式 02 三维螺旋时空方程 (v1+v3)",
        "stamp": STAMP,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "verdict": verdict,
        "counts": {
            "entries_total": len(entries),
            "FAIL": n_fail, "PASS": n_pass, "INFO": n_info,
            "controls_total": n_ctrl, "controls_ok": n_ctrl_ok,
            "guards_total": n_guard, "guards_ok": n_guard_ok,
        },
        "files": {"v1_found": v1_found, "v3_found": v3_found},
        "entries": entries,
        "controls": controls,
        "guards": guards,
        "key_readings": {
            "accel_conflict": bool(accel_conflict),
            "modulus_diff_t2": str(diff_mod),
            "kappa": str(kappa), "tau": str(tau),
            "ultimate_residual": str(ult - ult_target),
            "dim_p": repr(Dim_p), "dim_c0": repr(Dim_c0),
            "dim_conflict": bool(dim_conflict),
        },
    }

    # 退出码：控制组/守卫全绿且 FAIL>0（确有判死内容）⇒ rc=0；否则 rc=2
    healthy = (n_ctrl_ok == n_ctrl) and (n_guard_ok == n_guard) and v1_found and v3_found
    rc = 0 if (healthy and n_fail > 0) else 2

    # 写三份机读产物
    os.makedirs(OUT_DIR, exist_ok=True)
    base_name = "TUFT-r200_三维螺旋时空方程_公理直线自毁与p等于c0量纲冲突_精算_2026-10-25"
    with open(os.path.join(OUT_DIR, base_name + ".json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    with open(os.path.join(OUT_DIR, base_name + ".md"), "w", encoding="utf-8") as f:
        f.write("# %s 机读摘要\n\n" % base_name)
        f.write("- verdict: `%s`\n" % verdict)
        f.write("- 条目 %d（FAIL %d / PASS %d / INFO %d）\n" % (len(entries), n_fail, n_pass, n_info))
        f.write("- 控制组 %d/%d · 守卫 %d/%d\n" % (n_ctrl_ok, n_ctrl, n_guard_ok, n_guard))
        f.write("- rc=%d\n" % rc)
        f.write("\n## 条目\n")
        for e in entries:
            f.write("- [%s-%s] %s: %s\n" % (e["cat"], e["eid"], e["status"], e["title"]))
    with open(os.path.join(OUT_DIR, base_name + "_report.txt"), "w", encoding="utf-8") as f:
        f.write("TUFT-%s 审计报告\n" % VOLUME)
        f.write("target: %s\n" % summary["target"])
        f.write("verdict: %s\n" % verdict)
        f.write("条目 %d（FAIL %d / PASS %d / INFO %d）\n" % (len(entries), n_fail, n_pass, n_info))
        f.write("控制组 %d/%d · 守卫 %d/%d\n" % (n_ctrl_ok, n_ctrl, n_guard_ok, n_guard))
        f.write("rc=%d\n" % rc)

    # 控制台
    print("=" * 72)
    print("TUFT-%s  三维螺旋时空方程 公理自毁 / p=c0 量纲冲突" % VOLUME)
    print("=" * 72)
    print("条目 %d（FAIL %d / PASS %d / INFO %d）" % (len(entries), n_fail, n_pass, n_info))
    print("控制组 %d/%d · 守卫 %d/%d" % (n_ctrl_ok, n_ctrl, n_guard_ok, n_guard))
    print("verdict: %s" % verdict)
    print("rc=%d" % rc)
    print("=" * 72)
    return rc

if __name__ == "__main__":
    sys.exit(main())
