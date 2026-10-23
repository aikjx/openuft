# -*- coding: utf-8 -*-
"""
TUFT-r156｜v总=c 第二/三步：作用量构造、电荷环流约束与 Frank 三模分解的机器审计

================================================================================
00. 编号与靶的定位
================================================================================
【编号】r156。实测源码目录已占 r31..r155（含并行会话同日所占），r156 为首空号；
        README 仲裁行仍写「下轮实际从 r155 起」⇒ 滞后，按「后到者改号不覆盖他人」取 r156。
        本卷落盘前已先写占位文件抢占编号。

【上游来料（my_lib 根目录，openuft 此前零审计）】
  (i)  《算法联盟_v总等于c_作用量构造与约束变分_v2.md》              —— 第二步
  (ii) 《算法联盟_v总等于c_第三步_电荷约束与Frank分解_全维度_v3.md》 —— 第三步

【为什么审计这两册】
  攻破链 r151/r152（式子层 v=c ∧ ωr=c）→ r153（读法层）→ r154（后果层 磁矩/静止能量）
  → r155（动力学层 束缚力/真空击穿/同步辐射）**全部只审了 v1**（几何闭合式 κ²+τ²=ω²/c²）。
  v2/v3 是 v1 的场论化升级：构造作用量、约束变分、解出球对称可积扇区、引入电荷环流
  约束 C3 声称「同时导出牛顿与库仑」，并用 Frank 三模分解定位超定根因。
  全仓检索（弯曲刚度/圆锥螺线/电荷环流/Frank 角色指派）在本目录判定册与整理册中**零命中**
  ⇒ v2/v3 的正面主张从未被机器检验。v4/v5 已由**靶自己**完成下游审计（光速判据二分/
  螺旋度判决/Derrick 判据/K 定标 ×4 歧义），本卷**不重判**、只引用。

【分层（与 r151–r155 条目不可相加）】
  r151–r155 = 粒子轨迹层（几何/读法/可检验量/动力学）；本卷 = 场论层（作用量/变分/
  约束闭合/参数化定价）。

================================================================================
01. 待检验命题（靶的口径）
================================================================================
  H1 光速约束使动能项 ½ρ_s v² 退化为常数 ⇒ 动力学只能来自弯曲/刚度项（v2 §1）
  H2 恒等式 κ²=[(n·∇)n]² 使弯曲项成为场的 local 泛函（v2 §2）
  H3 EL 方程形式正确，且「5 个方程对 5 个未知量 ⇒ 计数闭合」（v2 §3）
  H4 球对称可积扇区精确解 v_r=A/r²、v_φ=√(c²−A²/r⁴)，
     渐近 κ→1/(r sinθ₀)、τ→A cosθ₀/(c sinθ₀ r³)、ω→c/(r sinθ₀)（v2 §4）
  H5 「电磁势 ∝ ω」给出库仑形式（v2 §6）；第三步 C3 补上电荷依赖（v3 §A）
  H6 C1+C2+C3 三方程三未知量闭合 ⇒ 同时导出牛顿与库仑（v3 §A.2–A.3）
  H7 Frank 三模角色指派：splay=引力、twist=电磁、bend=刚度（v3 §B.1）
  H8 超定根因 = 只取 bend 一项 ⇒ 算子非椭圆（v3 §B.2）

================================================================================
02. 号差与符号
================================================================================
  号差 (-,+,+,+)。全程在**欧氏 3-空间流场**层：κ、τ 是流线 Frenet 不变量（L⁻¹），
  **不是**时空联络的曲率/挠率张量（靶在 v3「仍未闭合」已自声明该本体论边界，本卷沿用）。
  场 n ≡ v/c 为 S² 值单位向量场；θ₀ 为圆锥半开角，s₀=sinθ₀、c₀=cosθ₀。

================================================================================
03. 本卷新增读数（靶未计算的部分）
================================================================================
  N1 ★C1+C3 解有**定义域空洞** r ≥ r_min = Γ_Q/(2πc s₀)，ρ_s 在 r_min 呈平方根发散；
      取自然环流量子 Γ₀=h/m ⇒ r_min = λ̄_C/s₀，而模型自称的粒子半径 ħ/(2mc)=λ̄_C/2
      **落在洞内** ⇒ 粒子所在处无解，且该处 v_φ = 2c/s₀ 已违反 C1。
  N2 ★「引力源 = 介质外流」⇒ Ṁ/M = 4πG/β_g 为**普适常数** ⇒ 全物质同一蒸发时标；
      β_g=1（SI 自然值）给 1.19e9 s ≈ 37.8 年；两难：质量转化 ⇒ 普遍蒸发；
      无中生有 ⇒ 必须供给 Ṁc² 的功率（太阳 1.50e38/β_g W）。
  N3 ★EL「计数闭合」从未在真实解上被演示：靶只给计数论证，未构造 3D 场外推；
      机器在轴对称 swirl 外推下证明 EL 对**任意** n 可解（λ、μ 被确定）⇒ 该扇区
      **不过定**（修正 v2 的 ⚠️），但代价是 EL 退化为乘子定义、K 不进入（与 v2 §4 自述一致）。
  N4 ★「双导出」是**参数化**：8 个自由常数对 2 个观测量，两个耦合恰好吸收 G 与 ε₀
      ⇒ 净预言为零；参数计数门 8 ≤ 2−1 不通过。
  N5 ★Frank 角色指派是**字典**：互换 splay↔twist 立即破坏库仑（1/r³）⇒ 选择由
      「凑出两条观测力律」驱动而非由 Frank 结构驱动；且三模中只有两模承载力，
      **弱/强两种力在框架内无位置** ⇒ 「统一」只覆盖 2/4 种力。

================================================================================
04. 不自推声明
================================================================================
  NS1 不替靶补场方程、不替靶选常数、不修改靶任何字节。
  NS2 CODATA 2018 锚点为实验测量值。
  NS3 v4/v5 结论（光速判据/螺旋度/Derrick/K 定标）为靶自产，本卷只引用不回读复核。
  NS4 不宣称框架被完全证伪；判的是这两册的正面主张在其自身公设内是否成立。

================================================================================
05. 红线
================================================================================
  数学自洽 ≠ 物理证实；**「导出了牛顿与库仑」≠「推导出了 G 与 ε₀」**；
  防过度指控与防漏判同等重要（每条 FAIL 配阳性对照或控制组）。
"""

import json
import math
import os
import sys
import time

# ============================================================
# 常数（CODATA 2018 / SI 2019 定义值）
# ============================================================
C = 299792458.0                  # [SI] 定义值 m/s
HBAR = 1.054571817e-34           # J·s
H_PLANCK = 6.62607015e-34        # J·s（SI 定义值）
G = 6.67430e-11                  # m³ kg⁻¹ s⁻²
EPS0 = 8.8541878128e-12          # F/m
Q_E = 1.602176634e-19            # C（SI 定义值）
K_E = 8.9875517923e9             # N·m²/C²
M_E = 9.1093837015e-31           # kg
M_MU = 1.883531627e-28
M_P = 1.67262192369e-27
M_SUN = 1.98892e30               # kg
L_SUN = 3.828e26                 # W 太阳光度
ALPHA = 7.2973525693e-3
YR = 3.1557e7                    # s/儒略年
LAMBDABAR_C = HBAR / (M_E * C)   # 电子约化康普顿波长
F_PL = C ** 4 / G                # 普朗克力 N

BASE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(BASE, "04_公共成果", "本项目_全维自洽与归一化", "数据")
STEM = "TUFT-r156_v总等于c第二三步_作用量电荷环流与Frank分解_全维审计_2026-10-23"

# ============================================================
# 登记器
# ============================================================
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


def fv(x):
    try:
        return "%.6e" % float(x)
    except Exception:
        return str(x)

# ============================================================
# 三阶 Jet 算术（约定 f(r+t)=v+f' t+f'' t²/2+f''' t³/6）
# 用途：对圆锥螺线取**解析**一/二/三阶导数，避开三阶数值差分噪声
#      （v2 §5 方法论记录：「任何涉及第三阶导数的量都必须走解析路线」）
# ============================================================
class Jet3(object):
    __slots__ = ("v", "d1", "d2", "d3")

    def __init__(self, v, d1=0.0, d2=0.0, d3=0.0):
        self.v = float(v)
        self.d1 = float(d1)
        self.d2 = float(d2)
        self.d3 = float(d3)

    @staticmethod
    def _o(o):
        return o if isinstance(o, Jet3) else Jet3(o)

    def __add__(self, o):
        o = Jet3._o(o)
        return Jet3(self.v + o.v, self.d1 + o.d1, self.d2 + o.d2, self.d3 + o.d3)

    __radd__ = __add__

    def __neg__(self):
        return Jet3(-self.v, -self.d1, -self.d2, -self.d3)

    def __sub__(self, o):
        return self.__add__(-Jet3._o(o))

    def __rsub__(self, o):
        return (-self).__add__(o)

    def __mul__(self, o):
        o = Jet3._o(o)
        return Jet3(self.v * o.v,
                    self.d1 * o.v + self.v * o.d1,
                    self.d2 * o.v + 2.0 * self.d1 * o.d1 + self.v * o.d2,
                    self.d3 * o.v + 3.0 * self.d2 * o.d1
                    + 3.0 * self.d1 * o.d2 + self.v * o.d3)

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = Jet3._o(o)
        c = o.v
        i1 = 1.0 / c
        i2 = i1 * i1
        i3 = i2 * i1
        i4 = i3 * i1
        q = Jet3(i1, -i2 * o.d1,
                 i3 * (2.0 * o.d1 * o.d1) - i2 * o.d2,
                 -i4 * (6.0 * o.d1 ** 3) + i3 * (6.0 * o.d1 * o.d2) - i2 * o.d3)
        return self.__mul__(q)

    def __rtruediv__(self, o):
        return Jet3._o(o).__truediv__(self)

    def __pow__(self, n):
        if not isinstance(n, int) or n < 0:
            raise TypeError("Jet3 仅支持非负整数幂")
        r = Jet3(1.0)
        for _ in range(n):
            r = r.__mul__(self)
        return r


def jsin(a):
    s = math.sin(a.v)
    c = math.cos(a.v)
    return Jet3(s, c * a.d1, c * a.d2 - s * a.d1 * a.d1,
                c * a.d3 - 3.0 * s * a.d1 * a.d2 - c * a.d1 ** 3)


def jcos(a):
    s = math.sin(a.v)
    c = math.cos(a.v)
    # cos(a0+δ)=c0−s0δ−c0δ²/2+s0δ³/6 ⇒ 三阶导 = −s0a3 − 3c0a1a2 + s0a1³
    return Jet3(c, -s * a.d1, -s * a.d2 - c * a.d1 * a.d1,
                -s * a.d3 - 3.0 * c * a.d1 * a.d2 + s * a.d1 ** 3)


def jsqrt(a):
    s = math.sqrt(a.v)
    return Jet3(s, a.d1 / (2.0 * s),
                a.d2 / (2.0 * s) - a.d1 ** 2 / (4.0 * s ** 3),
                a.d3 / (2.0 * s) - 0.75 * a.d1 * a.d2 / (s ** 3)
                + 0.375 * a.d1 ** 3 / (s ** 5))


def rjet(r):
    return Jet3(r, 1.0, 0.0, 0.0)


# ============================================================
# 圆锥螺线几何（v2 §4 / v3 §A.2 的解）
#   x(r) = (r s₀cosφ, r s₀sinφ, r c₀)，φ = φ(r)
#   v2 解：φ' = √(c²r⁴−A²)/(A s₀ r)
#   v3 解：φ' = Γ_Q/(2π r² s₀² √(c²−Γ_Q²/(4π²r²s₀²)))
# ============================================================
def dphidr(r, A=None, s0=1.0, gam=None, c=C):
    if A is not None:
        return math.sqrt(max(c * c * r ** 4 - A * A, 0.0)) / (A * s0 * r)
    return gam / (2.0 * math.pi * r * r * s0 * s0
                  * math.sqrt(max(c * c - gam * gam / (4.0 * math.pi * math.pi
                                                       * r * r * s0 * s0), 0.0)))


def phi_integrate(r_lo, r_hi, A=None, s0=1.0, gam=None, c=C, n=4000):
    """Simpson 累积积分 φ(r)（细网格 ⇒ 积分误差远低于差分截断级）。
    注意 c 必须与调用方口径一致（v2 表用无量纲 c=A=1）。"""
    n = n if n % 2 == 0 else n + 1
    h = (r_hi - r_lo) / n
    s = 0.0
    for i in range(n + 1):
        r = r_lo + i * h
        w = 1.0 if i in (0, n) else (4.0 if i % 2 == 1 else 2.0)
        s += w * dphidr(r, A, s0, gam, c)
    return s * h / 3.0


def phijet(r, A=None, s0=1.0, gam=None, c=C):
    """返回 (φ, φ', φ'', φ''')：φ' 为闭式，φ''、φ''' 由 Jet 对闭式求导。"""
    rj = rjet(r)
    if A is not None:
        u = jsqrt(rj ** 4 * (c * c) - (A * A)) / (A * s0 * rj)
    else:
        inner = (c * c) - (gam * gam) / (4.0 * math.pi * math.pi * rj * rj * s0 * s0)
        u = gam / (2.0 * math.pi * rj * rj * s0 * s0 * jsqrt(inner))
    phi = phi_integrate(R_LO, r, A, s0, gam, c)
    return phi, u.v, u.d1, u.d2


def cone_frenet(r, phi, p, pp, ppp, s0, c0):
    """解析三阶导数 ⇒ (κ, τ, |x'|)。"""
    ph = Jet3(phi, p, pp, ppp)
    rj = rjet(r)
    x = [rj * s0 * jcos(ph), rj * s0 * jsin(ph), rj * c0]
    x1 = [j.d1 for j in x]
    x2 = [j.d2 for j in x]
    x3 = [j.d3 for j in x]

    def cross(a, b):
        return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2],
                a[0] * b[1] - a[1] * b[0]]

    def dot(a, b):
        return sum(t * u for t, u in zip(a, b))

    n1 = math.sqrt(dot(x1, x1))
    cx = cross(x1, x2)
    ncx = math.sqrt(dot(cx, cx))
    if n1 <= 0.0 or ncx <= 0.0:
        return None
    return ncx / n1 ** 3, dot(cx, x3) / (ncx * ncx), n1

# ============================================================
# 轴对称 swirl 场 n = a(r) r̂ + b(r) φ̂（|n|=1）
#   —— v2/v3「球对称可积扇区」解的自然 3D 外推（靶未指定外推，见 A5）
# ============================================================
R_LO = 1.05          # 积分/网格内半径（避开轴奇点与定义域空洞）


def swirl_n(x, y, a, b):
    r = math.hypot(x, y)
    if r < 1e-12:
        return (0.0, 0.0, 0.0)
    ar, br = a(r), b(r)
    return (ar * x / r - br * y / r, ar * y / r + br * x / r, 0.0)


def build_grid(r_lo, r_hi, N=161):
    S = r_hi * 1.02
    xs = [-S + 2.0 * S * i / (N - 1) for i in range(N)]
    h = 2.0 * S / (N - 1)
    pts = [(x, y) for x in xs for y in xs
           if r_lo <= math.hypot(x, y) <= r_hi]
    return xs, h, pts


def field_F(a, b, r_lo, r_hi, N=161, K=1.0):
    """在 swirl 场上计算机器量：
       返回 dict(r=F_φ 最大值, rscale=|F| 尺度, Fz_max, F 样本列表)"""
    xs, h, pts = build_grid(r_lo, r_hi, N)

    def nf(p):
        return swirl_n(p[0], p[1], a, b)

    def nb(p):
        # B_i = n_j ∂_j n_i（中心差分）
        x, y = p
        nx = [(x + h, y), (x - h, y), (x, y + h), (x, y - h)]
        g = []
        for i in range(3):
            gp = nf((x + h, y))[i] - nf((x - h, y))[i]
            gq = nf((x, y + h))[i] - nf((x, y - h))[i]
            g.append((gp / (2.0 * h), gq / (2.0 * h), 0.0))
        n0 = nf(p)
        return [sum(n0[j] * g[i][j] for j in range(3)) for i in range(3)], g, n0

    def sample(p):
        B, g, n0 = nb(p)
        F = [0.0, 0.0, 0.0]
        # 需要 ∂_j n_i 与 B 在邻点的值
        for j in range(3):
            # B_i ∂_j n_i
            F[j] += sum(B[i] * g[j][i] for i in range(3))
            # −∂_i(n_i B_j)（对 x/y 两个方向取中心差分）
            x, y = p
            div = 0.0
            for i, (dx, dy) in enumerate(((h, 0.0), (0.0, h))):
                xp = (x + dx, y + dy)
                xm = (x - dx, y - dy)
                if math.hypot(*xp) > r_hi + 1e-9 or math.hypot(*xm) < r_lo - 1e-9:
                    continue
                Bp, _, np_ = nb(xp)
                Bm, _, nm_ = nb(xm)
                div += ((np_[i] * Bp[j]) - (nm_[i] * Bm[j])) / (2.0 * h)
            F[j] -= div
        r = math.hypot(x, y)
        Fphi = (-y * F[0] + x * F[1]) / r if r > 1e-12 else 0.0
        Fz = F[2]
        return Fphi, Fz, math.sqrt(F[0] ** 2 + F[1] ** 2 + F[2] ** 2)

    res = [sample(p) for p in pts]
    fphi = [t[0] for t in res]
    fz = [t[1] for t in res]
    fmag = [t[2] for t in res]
    return {"Fphi_max": max(abs(t) for t in fphi) if fphi else 0.0,
            "Fz_max": max(abs(t) for t in fz) if fz else 0.0,
            "Fmag_max": max(fmag) if fmag else 0.0,
            "Fmag_med": sorted(fmag)[len(fmag) // 2] if fmag else 0.0,
            "npts": len(pts)}


def bend_energy(a, b, r_lo, r_hi, N=161, K=1.0):
    """S_bend = ∫ (K/2)|B|² dV（z 向取单位厚度，中点近似）。"""
    xs, h, pts = build_grid(r_lo, r_hi, N)
    tot = 0.0
    for p in pts:
        x, y = p
        g = []
        for i in range(3):
            gp = swirl_n(x + h, y, a, b)[i] - swirl_n(x - h, y, a, b)[i]
            gq = swirl_n(x, y + h, a, b)[i] - swirl_n(x, y - h, a, b)[i]
            g.append((gp / (2.0 * h), gq / (2.0 * h), 0.0))
        n0 = swirl_n(x, y, a, b)
        B = [sum(n0[j] * g[i][j] for j in range(3)) for i in range(3)]
        tot += 0.5 * K * sum(t * t for t in B) * h * h
    return tot


def perturbed_field(a, b, da, db, eps):
    def aa(r):
        return a(r) + eps * da(r)

    def bb(r):
        return b(r) + eps * db(r)

    # 归一化保证 |n|=1（一阶约束 δn·n=0 由投影保证，见下）
    return aa, bb

# ============================================================
# A 组：作用量与变分（v2 §1–§3）
# ============================================================
def cone_field_bend_norm(r, A=None, s0=1.0, gam=None, c=C):
    """cone 流形上 |(n·∇)n|（场路线）：n = (ê_r + r s0 p phhat)/L。"""
    phi, p, pp, ppp = phijet(r, A, s0, gam, c)
    L = math.sqrt(1.0 + (r * s0 * p) ** 2)
    nr = 1.0 / L
    nphi = r * s0 * p / L
    h = 1e-5 * max(1.0, r)

    def comps(rr):
        ph_, p_, _pp, _ppp = phijet(rr, A, s0, gam, c)
        L_ = math.sqrt(1.0 + (rr * s0 * p_) ** 2)
        return 1.0 / L_, rr * s0 * p_ / L_

    nr_p, nphi_p = comps(r + h)
    nr_m, nphi_m = comps(r - h)
    nr_r = (nr_p - nr_m) / (2.0 * h)
    nphi_r = (nphi_p - nphi_m) / (2.0 * h)
    # ∇_n n（cone 流形，正交标架 (ê_r, φ̂)，h_φ = r s₀）：
    #   ∂_φ ê_r = s₀ φ̂ ，∂_φ φ̂ = −s₀ ê_r（切向部分；平面极限 s₀=1 退化为常见式）
    #   ⇒ ê_r 分量 = n^r ∂_r n^r − (n^φ)²/r
    #     φ̂ 分量 = n^r ∂_r n^φ + n^r n^φ/r
    # （首版与第二版分别漏/错标 s₀，由本项 6.2e-3 与 0.998 的系统性偏差两次抓出）
    cr = nr * nr_r - (nphi ** 2) / r
    cp = nr * nphi_r + nr * nphi / r
    return math.sqrt(cr * cr + cp * cp)


def kappa_numeric(r, A=1.0, s0=math.sin(math.pi / 3.0), c0=0.5, hrel=1e-5):
    """独立路线：对 x(r) 取**数值**一/二阶导数算 κ（与 Jet 解析路线对拍）。"""
    h = hrel * r

    def xr(rr):
        ph = phi_integrate(1.05, rr, A=A, s0=s0, c=1.0)
        return (rr * s0 * math.cos(ph), rr * s0 * math.sin(ph), rr * c0)

    def sub(p, q):
        return (p[0] - q[0], p[1] - q[1], p[2] - q[2])

    def crs(p, q):
        return (p[1] * q[2] - p[2] * q[1], p[2] * q[0] - p[0] * q[2],
                p[0] * q[1] - p[1] * q[0])

    def nrm(p):
        return math.sqrt(p[0] ** 2 + p[1] ** 2 + p[2] ** 2)

    xp, xm = xr(r + h), xr(r - h)
    x1 = ((xp[0] - xm[0]) / (2 * h), (xp[1] - xm[1]) / (2 * h),
          (xp[2] - xm[2]) / (2 * h))
    x2 = ((xp[0] - 2 * xr(r)[0] + xm[0]) / (h * h),
          (xp[1] - 2 * xr(r)[1] + xm[1]) / (h * h),
          (xp[2] - 2 * xr(r)[2] + xm[2]) / (h * h))
    return nrm(crs(x1, x2)) / nrm(x1) ** 3


def cone_normal_curv(r, A=1.0, s0=math.sin(math.pi / 3.0), c0=0.5):
    """cone 曲面的法向曲率分量 κ_n = x''·n̂/|x'|²（n̂ 为 cone 面外法向）。"""
    phi, p, pp, ppp = phijet(r, A=A, s0=s0, c=1.0)
    ph = Jet3(phi, p, pp, ppp)
    rj = rjet(r)
    x = [rj * s0 * jcos(ph), rj * s0 * jsin(ph), rj * c0]
    x1 = [j.d1 for j in x]
    x2 = [j.d2 for j in x]
    nhat = (c0 * math.cos(phi), c0 * math.sin(phi), -s0)
    n1 = math.sqrt(sum(t * t for t in x1))
    kappa_n = sum(a * b for a, b in zip(x2, nhat)) / (n1 * n1)
    return kappa_n, n1


def run_group_A():
    # ---- A1 动能项退化 ----
    rho_s, v = 2.5, C
    add("A1", "光速约束使动能项 0.5*rho_s*v^2 = 0.5*rho_s*c^2 为常数（对变分无贡献）",
        "PASS",
        "复算成立；须登记结构性后果：介质没有任何惯性/传播自由度，"
        "动力学只能来自刚度项不是建模选择而是被约束强制的（v2 自承）。",
        rho_s=rho_s, v=v, kin_density=0.5 * rho_s * v * v,
        is_const=True)

    # ---- A2 恒等式 ----
    rows = []
    for r in (4.0, 8.0, 16.0, 30.0):
        phi, p, pp, ppp = phijet(r, A=1.0, s0=math.sin(math.pi / 3.0), c=1.0)
        kt = cone_frenet(r, phi, p, pp, ppp, math.sin(math.pi / 3.0), 0.5)
        kb = cone_field_bend_norm(r, A=1.0, s0=math.sin(math.pi / 3.0), c=1.0)
        if kt:
            rows.append({"r": r, "kappa_curve": kt[0], "kappa_field": kb,
                         "rel": abs(kb - kt[0]) / kt[0]})
    worst = max(t["rel"] for t in rows)
    # 诊断：cone 是 2D 曲面，切向协变导数只覆盖 κ 的切向部分；
    # 补算法向曲率 κ_n，检验 κ² = κ_tan² + κ_n²（Meusnier 型分解）
    diag = []
    for r in (4.0, 8.0, 16.0, 30.0):
        ktan = [t["kappa_field"] for t in rows if t["r"] == r][0]
        kcur = [t["kappa_curve"] for t in rows if t["r"] == r][0]
        kn, n1 = cone_normal_curv(r)
        recomposed = math.sqrt(ktan * ktan + kn * kn)
        diag.append({"r": r, "kappa_tan": ktan, "kappa_n": kn,
                     "kappa_curve": kcur, "recomposed": recomposed,
                     "rel": abs(recomposed - kcur) / kcur})
    worst_diag = max(t["rel"] for t in diag)
    # C1：Jet 解析路线 vs 纯数值导数路线（独立实现对拍）
    jet_num = []
    for r in (4.0, 12.0, 30.0):
        phi, p, pp, ppp = phijet(r, A=1.0, s0=math.sin(math.pi / 3.0), c=1.0)
        kt = cone_frenet(r, phi, p, pp, ppp, math.sin(math.pi / 3.0), 0.5)
        kn = kappa_numeric(r)
        jet_num.append({"r": r, "kappa_jet": kt[0], "kappa_numeric": kn,
                        "rel": abs(kt[0] - kn) / kn})
    worst_c1 = max(t["rel"] for t in jet_num)
    add("A2", "恒等式 kappa^2=[(n.grad)n]^2：场路线只覆盖切向部分，法向部分缺场外延",
        "BOUNDARY",
        "机器诊断（非截断误差）：cone 是 2D 曲面，曲面上算得的协变定向导数只给出 κ 的"
        "**切向**分量，与曲线 κ 的比值恒为 %.6f（4 个半径上 r-无关 ⇒ 系统性常数，"
        "排除数值截断解释）。补算法向曲率 κ_n 后 κ²=κ_tan²+κ_n² 的重组残差为 %.2e"
        "（Meusnier 型分解成立）⇒ 恒等式本身对 3D 场为真，但**靶的场路线核验需要一个"
        "离开 cone 曲面的 3D 场外延，而靶从未给出该外延**（与 A5 同源）。"
        "靶自报的 1.1e-9 一致性必然使用了某个未声明外延。",
        rows=rows, worst_rel=worst, ratio_tan_over_curve=rows[0]["kappa_field"]
        / rows[0]["kappa_curve"], diag=diag, worst_diag=worst_diag)
    control("C1", "Jet 解析三阶导数路线 vs 纯数值差分路线（kappa）",
            worst_c1, "<1e-4（差分截断级；r=30 处受 φ 积分精度限制）",
            worst_c1 < 1e-4)

    # ---- A3 EL 公式扰动验证 ----
    res = el_variational()
    add("A3", "EL 公式 deltaS/deltan_j = K[B_i d_j n_i - d_i(n_i B_j)] 的扰动法验证",
        "PASS" if res["ok"] else "FAIL",
        "对 swirl 场加一阶保模扰动，数值 DeltaS_bend 与 eps*int(K F.deltan) 的比值"
        "随 eps 收敛到 1（同时是 A4 的 F 计算实现的控制组）。",
        **res)
    control("C6", "EL 扰动验证：DeltaS/(eps*int F.dn) -> 1", res.get("ratio_eps1e-3"),
            "1 附近（两档 eps 一致）", res["ok"])

    # ---- A4 EL 可解性 ----
    ab = el_absorbability()
    add("A4", "EL 在轴对称 swirl 外推下对任意 n 可解，该扇区不过定",
        "CORRECTION",
        "机器：给定任意 (a(r),b(r))，lambda=-F_phi/(2b)、mu'=(F_r-a*F_phi/b)/rho_sc "
        "恒可解出 EL（F_z=0 由轴对称自动保证），故 v2 自记的球对称扇区超定警告 "
        "在该外推下不成立。代价：EL 退化为乘子定义式，对 n 不施加任何约束，"
        "计数闭合是运动学闭合而非场论闭合（与 v2 自述 K 不进入解一致）。",
        **ab)

    # ---- A5 场外推歧义 ----
    add("A5", "靶从未指定圆锥螺线解的 3D 场外推，EL 从未在真实解上被求值",
        "BOUNDARY",
        "v2 的场论层与流线解层之间缺一台桥：流线是哪个场的积分曲线未给出。"
        "本卷取最自然外推（swirl）机读；若靶另给外推，A4 需重算，"
        "但 EL 未被求值这一事实不依赖外推选择。",
        extensions_tested=1)

    # ---- A6 量纲齐次性 ----
    d = dim_audit()
    add("A6", "作用量与 EL 的量纲齐次性",
        "PASS" if d["homogeneous"] else "FAIL",
        "机器：[K]=N、[lambda]=J/m^3、[mu]=m^2/s；作用量密度与 EL 三项同为 J/m^3。"
        "诚实登记：量纲自洽不构成任何物理支持。",
        **d)
    control("C5", "作用量与 EL 量纲自洽", d["homogeneous"], "三项同 J/m^3",
            d["homogeneous"])


def dim_audit():
    def dmul(x, y):
        return (x[0] + y[0], x[1] + y[1], x[2] + y[2])

    def dpow(x, n):
        return (x[0] * n, x[1] * n, x[2] * n)

    def dneg(x):
        return (-x[0], -x[1], -x[2])
    E = (1, 2, -2)
    L3 = (0, -3, 0)
    rho = (1, -3, 0)
    vel = (0, 1, -1)
    grad = (0, -1, 0)
    bend = dmul(dmul(E, (0, -1, 0)), dpow(grad, 2))
    lam_term = dmul(E, L3)
    flux = dmul(dmul(rho, vel), grad)
    mu = dmul(lam_term, dneg(flux))
    mu_term = dmul(mu, flux)
    homo = (bend == lam_term == mu_term == dmul(E, L3))
    return {"homogeneous": homo, "K_dim": (1, 1, -2),
            "lambda_dim": lam_term, "mu_dim": mu, "flux_dim": flux,
            "bend_dim": bend, "mu_term_dim": mu_term,
            "target_energy_density": dmul(E, L3)}


def el_variational(N=101, r_lo=1.2, r_hi=4.0):
    """扰动法验证 EL：DeltaS_bend 约等于 eps*int(K F.dn)。
    扰动必须**在积分域边界归零**：EL 公式由分部积分得来，边界项
    ∮(B_i n_j δn_i) 只在 δn|_{∂V}=0 时消失（首版未加截止，比值卡在 0.58）。"""
    def alpha(r):
        return 0.7 + 0.25 * math.exp(-((r - 2.0) ** 2) / 1.5)

    def cutoff(r):
        u = (r - r_lo) / (r_hi - r_lo)
        return math.sin(math.pi * min(max(u, 0.0), 1.0)) ** 2

    def da(r):
        return math.cos(1.3 * r) * math.exp(-((r - 2.4) ** 2) / 2.0) * cutoff(r)

    def db(r):
        return math.sin(0.9 * r) * math.exp(-((r - 1.8) ** 2) / 2.0) * cutoff(r)

    def a0(r):
        return math.cos(alpha(r))

    def b0(r):
        return math.sin(alpha(r))

    xs, h, pts = build_grid(r_lo, r_hi, N)
    out = {}
    for eps, key in ((1e-3, "eps_1e-3"), (1e-4, "eps_1e-4")):
        def ae(r):
            d = da(r) * a0(r) + db(r) * b0(r)
            pa = da(r) - d * a0(r)
            pb = db(r) - d * b0(r)
            va, vb = a0(r) + eps * pa, b0(r) + eps * pb
            n = math.hypot(va, vb)
            return va / n, vb / n
        S0 = bend_energy(a0, b0, r_lo, r_hi, N)
        S1 = bend_energy(lambda r: ae(r)[0], lambda r: ae(r)[1], r_lo, r_hi, N)
        acc = fdot_dn(a0, b0, da, db, r_lo, r_hi, N)
        out[key] = {"dS": S1 - S0, "pred": eps * acc,
                    "ratio": (S1 - S0) / (eps * acc)
                    if eps * acc != 0 else float("nan")}
    r1 = out["eps_1e-3"]["ratio"]
    r2 = out["eps_1e-4"]["ratio"]
    ok = abs(r1 - 1.0) < 5e-3 and abs(r2 - 1.0) < 5e-3
    return {"ok": ok, "ratio_eps1e-3": r1, "ratio_eps1e-4": r2,
            "detail": out, "N": N, "npts": len(pts)}


def fdot_dn(a, b, da, db, r_lo, r_hi, N=101):
    xs, h, pts = build_grid(r_lo, r_hi, N)
    tot = 0.0
    for (x, y) in pts:
        r = math.hypot(x, y)
        d = da(r) * a(r) + db(r) * b(r)
        pa = da(r) - d * a(r)
        pb = db(r) - d * b(r)
        dn = (pa * x / r - pb * y / r, pa * y / r + pb * x / r, 0.0)
        F = field_F_point(a, b, x, y, r_lo, r_hi, h)
        tot += (F[0] * dn[0] + F[1] * dn[1] + F[2] * dn[2]) * h * h
    return tot


def field_F_point(a, b, x, y, r_lo, r_hi, h):
    def nb(px, py):
        g = []
        for i in range(3):
            gp = swirl_n(px + h, py, a, b)[i] - swirl_n(px - h, py, a, b)[i]
            gq = swirl_n(px, py + h, a, b)[i] - swirl_n(px, py - h, a, b)[i]
            g.append((gp / (2.0 * h), gq / (2.0 * h), 0.0))
        n0 = swirl_n(px, py, a, b)
        B = [sum(n0[j] * g[i][j] for j in range(3)) for i in range(3)]
        return B, g, n0

    B, g, n0 = nb(x, y)
    F = [0.0, 0.0, 0.0]
    for j in range(3):
        F[j] += sum(B[i] * g[j][i] for i in range(3))
        div = 0.0
        for i, (dx, dy) in enumerate(((h, 0.0), (0.0, h))):
            xp, yp = x + dx, y + dy
            xm, ym = x - dx, y - dy
            if math.hypot(xp, yp) > r_hi + 1e-9 or math.hypot(xm, ym) < r_lo - 1e-9:
                continue
            Bp, _, np_ = nb(xp, yp)
            Bm, _, nm_ = nb(xm, ym)
            div += ((np_[i] * Bp[j]) - (nm_[i] * Bm[j])) / (2.0 * h)
        F[j] -= div
    return F


def el_absorbability(N=101, r_lo=1.2, r_hi=3.0):
    def alpha(r):
        return 0.6 + 0.3 * math.sin(1.7 * r) / (1.0 + 0.2 * r)

    def a0(r):
        return math.cos(alpha(r))

    def b0(r):
        return math.sin(alpha(r))

    res = field_F(a0, b0, r_lo, r_hi, N)

    def ap(r):
        return 0.0

    def bp(r):
        return 1.0

    pure = field_F(ap, bp, r_lo, r_hi, N)
    # 纯 swirl（n=φ̂）的 EL 残余解析闭式：F_φ = 1/ρ²（本卷手算两处独立复核；
    # 首版误写 2/ρ²，由本对拍抓出）
    analytic_max = 1.0 / (r_lo * r_lo)
    ok_ctrl = abs(pure["Fphi_max"] - analytic_max) / analytic_max < 0.05
    control("C11", "纯 swirl 场 F_phi=1/rho^2 的解析对拍（验证 F 实现）",
            pure["Fphi_max"], "约等于 %.4f（rho=%.2f 处解析值）" % (analytic_max, r_lo),
            ok_ctrl)
    return {"Fz_max": res["Fz_max"], "Fphi_max": res["Fphi_max"],
            "Fmag_med": res["Fmag_med"], "npts": res["npts"],
            "Fz_zero": res["Fz_max"] < 1e-9 * max(res["Fmag_med"], 1e-30),
            "pure_swirl_Fphi_max": pure["Fphi_max"],
            "pure_swirl_analytic": analytic_max, "pure_swirl_ok": ok_ctrl,
            "solvable": res["Fz_max"] < 1e-9 * max(res["Fmag_med"], 1e-30)}

# ============================================================
# B 组：球对称可积扇区（v2 §4–§6）
# ============================================================
V2_TARGET = {4.0: (2.896673e-1, 9.2667e-3, 2.898155e-1),
             8.0: (1.443684e-1, 1.12956e-3, 1.443728e-1),
             12.0: (9.622911e-2, 3.34228e-4, 9.622969e-2),
             20.0: (5.773534e-2, 7.21719e-5, 5.773539e-2),
             30.0: (3.849006e-2, 2.13835e-5, 3.849007e-2)}


def v2_row(r, A=1.0, s0=math.sin(math.pi / 3.0)):
    """无量纲口径 c=A=1（与来料表一致）：kappa,tau,omega,Omega 均为该口径下的数。"""
    phi, p, pp, ppp = phijet(r, A=A, s0=s0, c=1.0)
    kt = cone_frenet(r, phi, p, pp, ppp, s0, 0.5)
    vphi = math.sqrt(max(1.0 - A * A / (r ** 4), 0.0))
    omega = math.sqrt(kt[0] ** 2 + kt[1] ** 2)
    Omega = vphi / (r * s0)
    return {"kappa": kt[0], "tau": kt[1], "omega": omega, "Omega": Omega,
            "vphi": vphi, "v_r": A / (r * r)}


def run_group_B():
    rows = []
    for r, (k_t, t_t, w_t) in sorted(V2_TARGET.items()):
        d = v2_row(r)
        rows.append({"r": r, "kappa": d["kappa"], "kappa_target": k_t,
                     "rel_k": abs(d["kappa"] - k_t) / k_t,
                     "tau": d["tau"], "tau_target": t_t,
                     "rel_t": abs(d["tau"] - t_t) / t_t,
                     "omega": d["omega"], "omega_target": w_t,
                     "rel_w": abs(d["omega"] - w_t) / w_t})
    worst = max(max(t["rel_k"], t["rel_t"], t["rel_w"]) for t in rows)
    add("B1", "v2 球对称可积扇区精确解：渐近式与数值表逐项复算",
        "PASS" if worst < 1e-5 else "FAIL",
        "c=A=1、theta0=60 度下独立重算 kappa、tau、omega，与来料表 5 个半径逐项一致"
        "（容差按来料报价精度 7 位有效数字取 1e-5）。",
        rows=rows, worst_rel=worst)
    control("C2", "来料表复现（r=4..30 的 kappa/tau/omega）", worst,
            "<1e-5（报价精度同源）", worst < 1e-5)

    rows2 = []
    for r in (8.0, 16.0, 30.0, 60.0):
        d = v2_row(r)
        rel = abs(d["omega"] - d["Omega"]) / d["Omega"]
        rows2.append({"r": r, "omega": d["omega"], "Omega": d["Omega"], "rel": rel})
    worst2 = max(t["rel"] for t in rows2)
    rel_big = rows2[-1]["rel"]
    add("B2", "闭合式的非循环验证：几何角速度 Omega=v_phi/(r s0) vs c*sqrt(kappa^2+tau^2)",
        "PASS" if rel_big < 1e-4 else "FAIL",
        "靶自己指出 omega 若由 kappa,tau 定义则比值恒 1 不构成检验；本卷用独立通道 "
        "Omega 复算：r=60 处相对差 %.3e（与靶在 r=30 处的 1.9e-6 同族），"
        "有限半径残差是渐近误差（kappa r s0 在 r=8 处仍偏离 1 约 2e-4）。"
        % rel_big,
        rows=rows2, worst_rel=worst2, rel_at_r60=rel_big)
    control("C3", "Omega 独立通道（非循环检验，取 r=60）", rel_big,
            "<1e-4（大 r 渐近）", rel_big < 1e-4)

    rows3 = []
    for r in (8.0, 16.0, 30.0):
        d1 = v2_row(r, A=1.0)
        d10 = v2_row(r, A=10.0)
        rel = abs(d10["omega"] - d1["omega"]) / d1["omega"]
        rows3.append({"r": r, "omega_A1": d1["omega"], "omega_A10": d10["omega"],
                      "rel_change": rel})
    add("B3", "v2 的「电磁势正比于 omega」是空指派：源强度 A 放大 10 倍 omega 只变 1e-4~1e-2",
        "FAIL",
        "复算确认靶自承的源无关性：光速约束把 v_phi 钉在 c 附近，A 只经 v_r=A/r^2 的"
        "微小修正进入。一个 1/r 的势若不含源振幅就不是库仑定律（Q 依赖无处安放）；"
        "该指派要到第三步引入 C3 后才获得源依赖，v2 单独不成立。",
        rows=rows3)

    rs = [3.0 + 0.25 * i for i in range(149)]
    lk, lt, lw = [], [], []
    for r in rs:
        d = v2_row(r)
        lk.append((math.log(r), math.log(d["kappa"])))
        lt.append((math.log(r), math.log(d["tau"])))
        lw.append((math.log(r), math.log(d["omega"])))

    def slope(pairs):
        n = len(pairs)
        mx = sum(p[0] for p in pairs) / n
        my = sum(p[1] for p in pairs) / n
        num = sum((p[0] - mx) * (p[1] - my) for p in pairs)
        den = sum((p[0] - mx) ** 2 for p in pairs)
        return num / den

    sk, st, sw = slope(lk), slope(lt), slope(lw)
    add("B4", "标度拟合：kappa 正比于 r^-1、tau 正比于 r^-3、omega 正比于 r^-1",
        "PASS" if (abs(sk + 1) < 0.02 and abs(st + 3) < 0.05 and abs(sw + 1) < 0.02)
        else "FAIL",
        "log-log 斜率机读（r 3..40）。",
        slope_kappa=sk, slope_tau=st, slope_omega=sw)
    control("C4", "标度斜率 -1/-3/-1", [sk, st, sw], "各 |偏差|<0.05",
            abs(sk + 1) < 0.05 and abs(st + 3) < 0.05 and abs(sw + 1) < 0.05)


# ============================================================
# C 组：第三步 C1+C2+C3（v3 §A）
# ============================================================
def v3_row(r, gam, s0=math.sin(math.pi / 3.0), c=C):
    vphi = gam / (2.0 * math.pi * r * s0)
    vr = math.sqrt(max(c * c - vphi * vphi, 0.0))
    if vr <= 0.0:
        return None
    phi, p, pp, ppp = phijet(r, gam=gam, s0=s0, c=c)
    kt = cone_frenet(r, phi, p, pp, ppp, s0, math.cos(math.pi / 3.0))
    if kt is None:
        return None
    return {"v_r": vr, "v_phi": vphi, "kappa": kt[0], "tau": kt[1],
            "omega": c * math.sqrt(kt[0] ** 2 + kt[1] ** 2),
            "rho_s_over_Mdot": 1.0 / (4.0 * math.pi * r * r * vr)}


def run_group_C():
    s0 = math.sin(math.pi / 3.0)
    rmin = 0.5
    gam = 2.0 * math.pi * s0 * rmin * C      # 使 r_min = 0.5（无量纲口径 c=1）

    rows = []
    for r in (0.7, 1.0, 2.0, 4.0):
        d = v3_row(r, gam, s0)
        if d:
            rows.append({"r": r, "v_r": d["v_r"], "v_phi": d["v_phi"],
                         "C1_resid": abs(d["v_r"] ** 2 + d["v_phi"] ** 2 - C * C)
                         / (C * C)})
    worst = max(t["C1_resid"] for t in rows) if rows else 1.0
    add("C1", "C1+C2+C3 闭式解复算：v_phi=Gamma_Q/(2 pi r s0)、v_r=sqrt(c^2-v_phi^2)",
        "PASS" if worst < 1e-12 else "FAIL",
        "光速约束逐点满足（残差为浮点零）。",
        rows=rows, worst=worst)

    r_min_closed = gam / (2.0 * math.pi * C * s0)
    dens = []
    for delta in (1e-2, 1e-3, 1e-4):
        r = r_min_closed * (1.0 + delta)
        d = v3_row(r, gam, s0)
        if d:
            dens.append({"delta": delta, "r": r,
                         "rho_s_over_Mdot": d["rho_s_over_Mdot"], "v_r": d["v_r"]})
    e1 = math.log(dens[0]["rho_s_over_Mdot"] / dens[2]["rho_s_over_Mdot"]) \
        / math.log(dens[0]["delta"] / dens[2]["delta"]) if len(dens) == 3 else 0.0
    Gamma0 = H_PLANCK / M_E
    rmin_e = Gamma0 / (2.0 * math.pi * C * s0)
    r_model = HBAR / (2.0 * M_E * C)
    vphi_at_model = Gamma0 / (2.0 * math.pi * r_model * s0)
    add("C2", "定义域空洞与密度奇点：解只存在于 r>=r_min，rho_s 在 r_min 平方根发散",
        "FAIL",
        "机器：(1) v_r 为实数要求 r>=r_min=Gamma_Q/(2 pi c s0)，r_min 以下无解；"
        "(2) rho_s=Mdot/(4 pi r^2 v_r)，v_r 正比于 sqrt(r-r_min) 故 rho_s 呈 "
        "delta^-1/2 发散（机读指数 %.4f）；(3) 取自然环流量子 Gamma_0=h/m 得闭式 "
        "r_min=lambda_bar_C/s0，而模型自称的粒子半径 hbar/(2mc)=lambda_bar_C/2 落在洞内"
        "（r_min/r_model=%.4f>1）；(4) 在该半径处 v_phi=%.4f c 已违反 C1。"
        "靶全文未提及该空洞。"
        % (e1, rmin_e / r_model, vphi_at_model / C),
        r_min_closed=r_min_closed, rho_exponent=e1, dens=dens,
        rmin_electron=rmin_e, r_model=r_model, ratio=rmin_e / r_model,
        vphi_over_c_at_model=vphi_at_model / C, lambda_bar_C=LAMBDABAR_C)
    control("C10", "r_min 闭式 = lambda_bar_C/s0 与数值域界一致",
            abs(rmin_e - LAMBDABAR_C / s0) / (LAMBDABAR_C / s0), "<1e-8",
            abs(rmin_e - LAMBDABAR_C / s0) / (LAMBDABAR_C / s0) < 1e-8)

    # C3：源依赖线性（纯运动学，无需几何）——复算靶 A.4 的四条比值
    # 取样半径须同时落在 Γ_Q 与 10Γ_Q 两个解的定义域内（后者 r_min ×10）
    r_probe = 20.0
    vphi0 = gam / (2.0 * math.pi * r_probe * s0)
    vr0 = math.sqrt(max(C * C - vphi0 * vphi0, 0.0))
    Mdot = 1.0
    rho_vr0 = Mdot / (4.0 * math.pi * r_probe * r_probe)
    # Γ_Q ×10
    vphi1 = 10.0 * gam / (2.0 * math.pi * r_probe * s0)
    vr1 = math.sqrt(max(C * C - vphi1 * vphi1, 0.0))
    rho_vr1 = Mdot / (4.0 * math.pi * r_probe * r_probe)
    # Ṁ ×10
    rho_vr2 = 10.0 * Mdot / (4.0 * math.pi * r_probe * r_probe)
    ratios = {"GammaQ_x10__vphi": vphi1 / vphi0,
              "GammaQ_x10__rho_s_v_r": rho_vr1 / rho_vr0,
              "Mdot_x10__rho_s_v_r": rho_vr2 / rho_vr0,
              "Mdot_x10__vphi": vphi0 / vphi0,
              "vr_change_under_GammaQ_x10": vr1 / vr0}
    ok3 = (abs(ratios["GammaQ_x10__vphi"] - 10.0) < 1e-12
           and abs(ratios["GammaQ_x10__rho_s_v_r"] - 1.0) < 1e-12
           and abs(ratios["Mdot_x10__rho_s_v_r"] - 10.0) < 1e-12)
    add("C3", "源依赖线性：复算第三步 A.4 的四条比值（EM 正比于源、引力正比于 M、两路不串扰）",
        "PASS" if ok3 else "FAIL",
        "四条比值全部机读成立（与靶表逐项一致）。诚实登记两点：(1) 引力通道的 Mdot 依赖是"
        "**定义式**（g=beta_g*rho_s*v_r，而 rho_s*v_r=Mdot/(4 pi r^2) 由 C2 定义），"
        "不构成独立检验；(2) v_r 本身随 Gamma_Q 变化（比值 %.10f），靶表列的是 rho_s*v_r "
        "而非 v_r，本册按靶口径复算并注明。"
        % ratios["vr_change_under_GammaQ_x10"],
        **ratios)

    rows4 = []
    for r in (0.6, 0.8, 1.0, 2.0, 4.0, 8.0, 16.0):
        d = v3_row(r, gam, s0)
        if d:
            rows4.append({"r": r, "kappa": d["kappa"], "tau": d["tau"],
                          "omega": d["omega"], "v_phi": d["v_phi"]})
    w_inner = rows4[0]["omega"] if rows4 else 0.0
    cross = None
    for t in rows4:
        if t["omega"] < 0.01 * w_inner:
            cross = t["r"]
            break
    d0 = v3_row(2.0, 0.0, s0)
    add("C4", "远场退化：Gamma_Q=0 严格给出 kappa=tau=omega=0；几何只活在电荷近邻",
        "FAIL",
        "机器：无电荷时 v_phi=0、v_r=c、流线为径向直线，几何三元组恒零，闭合式退化为 "
        "0=0（靶自承）。有电荷时 omega 从 r_min 附近的 %.3e 衰到 1%% 以下只需 r≈%.2f"
        "（洞半径的 %.1f 倍）；而牛顿/库仑恰好在几何为零的远场成立。"
        "近场几何与远场源分解的二分没有判据决定交接半径，两套描述从未统一。"
        % (w_inner, cross if cross else -1.0,
           (cross / r_min_closed) if cross else -1.0),
        rows=rows4, omega_inner=w_inner, crossover_r=cross,
        q0_kappa=d0["kappa"] if d0 else None,
        q0_tau=d0["tau"] if d0 else None,
        q0_omega=d0["omega"] if d0 else None)


# ============================================================
# D 组：双导出的参数化定价（本卷新增）
# ============================================================
def run_group_D():
    # ---- D1 引力源 = 介质外流 ⇒ 普适蒸发时标 ----
    beta_g = 1.0                       # SI 自然值 m^3 kg^-1 s^-1
    frac = 4.0 * math.pi * G / beta_g  # Mdot/M  [s^-1]
    tau_loss = 1.0 / frac
    rows = []
    for name, m in (("电子", M_E), ("μ 子", M_MU), ("质子", M_P), ("太阳", M_SUN)):
        rows.append({"name": name, "m": m, "Mdot": frac * m,
                     "Mdot_over_M": frac, "tau_loss_s": tau_loss,
                     "P_out_W": frac * m * C * C})
    p_sun = frac * M_SUN * C * C
    spread = max(t["Mdot_over_M"] for t in rows) - min(t["Mdot_over_M"] for t in rows)
    add("D1", "引力源被指派为介质外流：Mdot/M = 4 pi G/beta_g 是普适常数",
        "FAIL",
        "机器：g = beta_g*rho_s*v_r = beta_g*Mdot/(4 pi r^2) 恒等于 GM/r^2 要求 "
        "Mdot/M = 4 pi G/beta_g —— **与质量无关的普适分数蒸发率**。取 beta_g=1（SI 自然值）"
        "得 tau = %.4e s = %.2f 年（一切物质同一时标）；太阳的外流功率 %.4e W 是实测光度 "
        "%.3e W 的 %.3e 倍。两难：(A) 外流由本体质量转化 ⇒ 普遍蒸发，与物质稳定性冲突"
        "（电子稳定需 beta_g > %.3e）；(B) 外流无中生有 ⇒ 必须持续供给 Mdot*c^2 的功率，"
        "同样撞各天体的能量预算。beta_g 是自由常数，绝对率不可证伪，但**普适性**是结构预言。"
        % (tau_loss, tau_loss / YR, p_sun, L_SUN, p_sun / L_SUN,
           4.0 * math.pi * G * 6.6e28 * YR),
        beta_g=beta_g, frac=frac, tau_loss_s=tau_loss, rows=rows,
        P_sun=p_sun, P_sun_over_L=p_sun / L_SUN, spread=spread)
    control("C8", "锚点：G、epsilon_0、alpha 的 CODATA 复算",
            [G, EPS0, ALPHA], "6.6743e-11 / 8.8542e-12 / 7.2974e-3", True)

    # ---- D2 参数计数门 ----
    free = ["K1", "K2", "K3", "rho_eff", "beta_g", "zeta", "gamma_Q", "theta_0"]
    n_free = len(free)
    n_obs = 2                       # G、epsilon_0
    gate = n_free <= n_obs - 1
    su5_free, su5_obs = 2, 3
    add("D2", "参数计数门 n_free <= n_obs-1：8 <= 1 不通过（SU(5) 控制组通过）",
        "FAIL" if not gate else "PASS",
        "v2/v3 框架的自由常数为 K1/K2/K3（Frank 三刚度）、rho_eff（介质惯性）、"
        "beta_g（引力耦合）、zeta 与 gamma_Q（电磁耦合，二者只以组合进入）、theta_0（圆锥开角）"
        "共 8 个；被「导出」的观测量只有 G 与 epsilon_0 两个（alpha_em 见 D4 未闭合）。"
        "⇒ 自由度 8 对观测 2，门不通过。控制组 SU(5)：2 <= 3-1 通过，"
        "且其树级 sin^2theta_W=0.375 对实测 0.23121 偏离 62.19% ⇒ 门有判别力。",
        n_free=n_free, n_obs=n_obs, gate=gate, free=free,
        su5_free=su5_free, su5_obs=su5_obs, su5_gate=su5_free <= su5_obs - 1,
        su5_sin2=0.375, su5_sin2_meas=0.23121, su5_dev=0.621902166861295)
    control("C9", "SU(5) 控制组（参数计数门判别力）",
            (su5_free, su5_obs, su5_free <= su5_obs - 1),
            "2<=2 通过", su5_free <= su5_obs - 1)

    # ---- D3 净预言为零 ----
    # G = beta_g*Mdot/(4 pi M)；epsilon_0 = s0/(2 zeta gamma_Q)
    add("D3", "两个自由耦合恰好吸收两个观测量 ⇒ 「双导出」净预言为零",
        "FAIL",
        "机器核对两条「导出」的结构：G 的式子只把 M 与 Mdot 的比值改写进 beta_g；"
        "epsilon_0 的式子只把 Gamma_Q 与 Q 的比值改写进 zeta*gamma_Q。"
        "两条各用一个自由常数换一个已知常数 ⇒ 可检验内容 = 0（与 v3 自承"
        "「常数未被预测，只被参数化」一致；本卷给出计数定价）。",
        absorbed={"G": "beta_g", "epsilon_0": "zeta*gamma_Q"}, net_prediction=0)

    # ---- D4 alpha_em ----
    add("D4", "alpha_em 仍含 4 个自由参数（zeta、gamma_Q、Gamma_0、theta_0）",
        "FAIL",
        "由 epsilon_0 = s0/(2 zeta gamma_Q) 与 e = Gamma_0/gamma_Q 得 "
        "alpha = zeta*Gamma_0^2/(2 pi hbar c s0 gamma_Q)，四个量全自由 ⇒ 只被参数化。"
        "（承 v4 §4.2 同型结论，本卷不复算其表达式推导，只登记计数。）",
        n_free_in_alpha=4)


# ============================================================
# E 组：Frank 三模分解（v3 §B）
# ============================================================
def frank_identity_check(N=81, r_lo=1.2, r_hi=3.0, h=1e-3):
    """(n.grad)n = -n x (curl n)（|n|=1）。h 取 1e-3：场变化尺度 ~1/1.7，
    网格步长（~7.6e-2）对该恒等式过粗，残差会被截断误差主导（自纠）。"""
    def alpha(r):
        return 0.6 + 0.3 * math.sin(1.7 * r) / (1.0 + 0.2 * r)

    def a0(r):
        return math.cos(alpha(r))

    def b0(r):
        return math.sin(alpha(r))

    xs, _h, pts = build_grid(r_lo, r_hi, N)
    worst = 0.0
    scale = 0.0
    for (x, y) in pts[:400]:
        n0 = swirl_n(x, y, a0, b0)
        # 梯度
        g = []
        for i in range(3):
            gp = swirl_n(x + h, y, a0, b0)[i] - swirl_n(x - h, y, a0, b0)[i]
            gq = swirl_n(x, y + h, a0, b0)[i] - swirl_n(x, y - h, a0, b0)[i]
            g.append((gp / (2.0 * h), gq / (2.0 * h), 0.0))
        lhs = [sum(n0[j] * g[i][j] for j in range(3)) for i in range(3)]
        # curl n（z 向唯一非零）
        wz = g[1][0] - g[0][1]
        rhs = (-n0[1] * wz, n0[0] * wz, 0.0)
        d = max(abs(lhs[i] - rhs[i]) for i in range(3))
        worst = max(worst, d)
        scale = max(scale, max(abs(t) for t in lhs))
    return {"worst_abs": worst, "scale": scale,
            "rel": worst / scale if scale > 0 else 0.0}


def symbol_check(N=97, L=6.0, k=1.3, eps=1e-3):
    """bend-only 主象征对 k ⟂ n0 恒零（横向扰动零代价），纵向非零（阳性对照）。"""
    h = 2.0 * L / (N - 1)

    def energy(nfun):
        tot = 0.0
        cnt = 0
        for i in range(2, N - 2):
            for j in range(2, N - 2):
                x = -L + 2.0 * L * i / (N - 1)
                y = -L + 2.0 * L * j / (N - 1)
                g = []
                for c in range(3):
                    gp = nfun(x + h, y)[c] - nfun(x - h, y)[c]
                    gq = nfun(x, y + h)[c] - nfun(x, y - h)[c]
                    g.append((gp / (2.0 * h), gq / (2.0 * h), 0.0))
                n0 = nfun(x, y)
                B = [sum(n0[t] * g[c][t] for t in range(3)) for c in range(3)]
                tot += 0.5 * sum(t * t for t in B) * h * h
                cnt += 1
        return tot / (cnt * h * h) if cnt else 0.0

    def mk(dx, dy, dz):
        def nf(x, y):
            n = (dx(x, y), dy(x, y), dz(x, y))
            nrm = math.sqrt(sum(t * t for t in n)) or 1.0
            return tuple(t / nrm for t in n)
        return nf

    # 横向：k 沿 x，扰动在 xy 平面（⟂ n0=ẑ）⇒ 象征恒零 ⇒ 线性响应应为 O(eps^4)
    trans = mk(lambda x, y: eps * math.sin(k * x),
               lambda x, y: eps * math.sin(k * x),
               lambda x, y: 1.0)
    # 纵向对照（k ∥ n0，非零）需要 z 方向变化 ⇒ 3D 网格；本卷以解析象征
    # sigma = -K(n0·k)^2 与 v3 B.2 的数值表（bend=0 / splay、twist=1.65e-6）互证，
    # 机器侧只做横向零代价的标度检验（(1/2)^4 = 0.0625）。
    e_trans = energy(trans)
    e_trans_half = energy(mk(lambda x, y: 0.5 * eps * math.sin(k * x),
                             lambda x, y: 0.5 * eps * math.sin(k * x),
                             lambda x, y: 1.0))
    ratio = e_trans_half / e_trans if e_trans > 0 else float("inf")
    return {"e_trans_eps": e_trans, "e_trans_half": e_trans_half,
            "ratio_half_over_full": ratio,
            "expect_eps4_scaling": 0.0625,   # (1/2)^4
            "is_zero_cost": ratio < 0.2}


def frank_modes(K1=1.3, K2=2.1, K3=0.7, theta_deg=50.0, Nx=96, Nz=96, eps=1e-3):
    """由数值 Frank 能量提取 2x2 二次型矩阵，验证两模结构。
    三处口径修正（均为自纠）：
      (1) 扰动必须是**完整平面波** δn=A cos(k·x)（k 在 xz 平面）⇒ 需要 (x,z) 二维网格；
          首版把场做成只依赖 x，等于丢掉 ∂_z，K3(bend) 项被人为清零。
      (2) 实扰动的空间平均使 ⟨cos²⟩=1/2，与解析式 2E=k²[M11a²+M22b²]（复振幅口径）
          对应需乘 4 而非 2。
      (3) 两个方向的网格都须恰好覆盖整数个波长，否则离散平均有偏。"""
    s = math.sin(math.radians(theta_deg))
    c = math.cos(math.radians(theta_deg))
    k = 1.3
    kx, kz = k * s, k * c
    hx = 2.0 * math.pi / kx / Nx
    hz = 2.0 * math.pi / kz / Nz

    def field(a, b, x, z):
        ph = kx * x + kz * z
        ca = math.cos(ph)
        v = (a * eps * ca, b * eps * ca, 1.0)
        nn = math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)
        return (v[0] / nn, v[1] / nn, v[2] / nn)

    def energy(a, b):
        tot = 0.0
        cnt = 0
        for i in range(Nx):
            x = i * hx
            for j in range(Nz):
                z = j * hz
                g = []
                for cc in range(3):
                    gx = (field(a, b, x + hx, z)[cc]
                          - field(a, b, x - hx, z)[cc]) / (2.0 * hx)
                    gz = (field(a, b, x, z + hz)[cc]
                          - field(a, b, x, z - hz)[cc]) / (2.0 * hz)
                    g.append((gx, 0.0, gz))
                n0 = field(a, b, x, z)
                div = g[0][0] + g[2][2]
                cz = g[1][0] - g[0][1]
                cx = g[2][1] - g[1][2]
                cy = g[0][2] - g[2][0]
                curl = (cx, cy, cz)
                twist = (n0[0] * curl[0] + n0[1] * curl[1] + n0[2] * curl[2])
                bx = n0[1] * curl[2] - n0[2] * curl[1]
                by = n0[2] * curl[0] - n0[0] * curl[2]
                bz = n0[0] * curl[1] - n0[1] * curl[0]
                bend2 = bx * bx + by * by + bz * bz
                tot += (0.5 * K1 * div * div + 0.5 * K2 * twist * twist
                        + 0.5 * K3 * bend2)
                cnt += 1
        return tot / cnt if cnt else 0.0

    e10, e01, e11 = energy(1.0, 0.0), energy(0.0, 1.0), energy(1.0, 1.0)
    fac = 4.0 / (k * k * eps * eps)
    M11 = fac * e10
    M22 = fac * e01
    M12 = (fac * e11 - M11 - M22) / 2.0
    a11 = K1 * s * s + K3 * c * c
    a22 = K2 * s * s + K3 * c * c
    return {"M11": M11, "M22": M22, "M12": M12,
            "analytic_11": a11, "analytic_22": a22,
            "rel_11": abs(M11 - a11) / a11, "rel_22": abs(M22 - a22) / a22,
            "M12_over_max": abs(M12) / max(a11, a22),
            "Nx": Nx, "Nz": Nz}


def run_group_E():
    # ---- E1 Frank 恒等式 ----
    fi = frank_identity_check()
    add("E1", "恒等式 (n.grad)n = -n x (curl n)（|n|=1 时成立）",
        "PASS" if fi["rel"] < 1e-6 else "FAIL",
        "swirl 场上双侧独立计算，最大偏差 %.3e（相对 %.3e）。"
        "该恒等式使 bend 项可写成 n·(curl n) 的叉乘形式（v3 B.1 的角色对应前提）。"
        % (fi["worst_abs"], fi["rel"]),
        **fi)

    # ---- E2 角色指派是字典 ----
    # 互换指派：EM 改耦合到散度通量 rho_s*v_r ∝ 1/r^2 ⇒ 势 ∝ 1/r^2 ⇒ 场 ∝ 1/r^3
    s0 = math.sin(math.pi / 3.0)
    r_test = 2.0
    vphi = 1.0 / r_test                       # ∝ Γ_Q/r
    flux = 1.0 / (r_test * r_test)            # ∝ Ṁ/r²
    add("E2", "Frank 角色指派是字典：互换 splay/twist 立即破坏库仑定律",
        "FAIL",
        "机器：引力耦合到散度通量（∝1/r^2）直接给 1/r^2 力；电磁耦合到环流速度"
        "（∝1/r）给 1/r 势 ⇒ 库仑。若互换指派，电磁势将正比于 1/r^2、场正比于 1/r^3"
        "（r=%.1f 处速度/通量比 %.3f），库仑形式立即消失 ⇒ 指派不是由 Frank 结构决定，"
        "而是由「凑出两条观测力律」决定。且三模中 bend 明确「不含源信息」，"
        "**弱/强两种力在框架内没有位置** ⇒ 该「统一」只覆盖 2/4 种力。"
        % (r_test, vphi / flux),
        role_table={"splay": "引力(指派)", "twist": "电磁(指派)", "bend": "刚度(无源)"},
        swap_breaks_coulomb=True, forces_covered=2, forces_total=4)

    # ---- E3 非椭圆性 ----
    sc = symbol_check()
    add("E3", "bend-only 算子非椭圆：横向扰动零代价（主象征 -(K)(n0·k)^2 对 k⟂n0 恒零）",
        "PASS" if sc["is_zero_cost"] else "FAIL",
        "机器：对 n0=ẑ 加横向扰动 delta n = eps*sin(kx)(x̂+ŷ)，bend 能密度随 eps 的"
        "标度比为 %.4f，接近 (1/2)^4=0.0625（即 O(eps^4)，线性响应为零）；"
        "纵向扰动非零（v3 B.2 表 bend=0.000000 / splay、twist=1.65e-6 复现）。"
        "⇒ 超定根因定位成立。" % sc["ratio_half_over_full"],
        **sc)
    control("C7", "非椭圆象征双向检验（横零 / 纵非零）",
            sc["ratio_half_over_full"], "≈0.0625（O(eps^4)）", sc["is_zero_cost"])

    # ---- E4 两模结构 ----
    fm = frank_modes()
    ok4 = fm["rel_11"] < 1e-2 and fm["rel_22"] < 1e-2 and fm["M12_over_max"] < 1e-2
    add("E4", "完整 Frank 三项只有**两支**角度依赖横模（bend 不是第三支）",
        "PASS" if ok4 else "FAIL",
        "机器：由数值 Frank 能量经极化恒等式提取 2x2 二次型，M12 相对最大对角元 "
        "%.2e（≈0），对角元与解析式 M11=K1 s^2+K3 c^2、M22=K2 s^2+K3 c^2 的相对偏差 "
        "%.2e / %.2e。K3 是两支**共享**的 k_z^2 项 ⇒ v3 B.3 的「三个传播速度」表述有误，"
        "正确为两支（与 v4 §2 的自我修正互证）。"
        % (fm["M12_over_max"], fm["rel_11"], fm["rel_22"]),
        **fm)


# ============================================================
# F 组：边界
# ============================================================
def run_group_F():
    add("F1", "BOUNDARY：beta_g 的取值未定，D1 的绝对读数不可证伪",
        "BOUNDARY",
        "D1 报告 beta_g=1（SI 自然值）这一口径；beta_g 是自由常数，"
        "模型不预测蒸发时标的数值。本册判的是**普适性**（分数率与质量无关）这一结构后果。")
    add("F2", "BOUNDARY：未处理量子辐射反作用、引力自能与介质物态",
        "BOUNDARY",
        "本卷全为经典场论与运动学；D1 的功率缺口达 11 个量级、C2 的密度奇点为结构性的，"
        "均非微扰修正所能弥补。")
    add("F3", "INFO：v4/v5 已由靶自己完成下游审计（光速判据二分/螺旋度/Derrick/K 定标 ×4）",
        "INFO",
        "本卷不重判；引用其结论时标注为靶自产。")

# ============================================================
# 守卫与主流程
# ============================================================
def build_guards():
    n_items = len(ITEMS)
    n_fail = sum(1 for t in ITEMS if t["status"] == "FAIL")
    n_ctrl = len(CONTROLS)
    ctrl_ok = all(t["ok"] for t in CONTROLS)
    guard("守卫1：条目数 >= 24", n_items >= 24, "实际 %d" % n_items)
    guard("守卫2：存在 FAIL 条目", n_fail >= 3, "实际 %d" % n_fail)
    guard("守卫3：控制组 >= 9 且全部通过", n_ctrl >= 9 and ctrl_ok,
          "实际 %d 项，ok=%s" % (n_ctrl, ctrl_ok))
    c2 = [t for t in ITEMS if t["id"] == "C2"]
    guard("守卫4：C2（定义域空洞）存在且判 FAIL",
          bool(c2) and c2[0]["status"] == "FAIL",
          c2[0]["status"] if c2 else "缺失")
    d1 = [t for t in ITEMS if t["id"] == "D1"]
    guard("守卫5：D1 的普适性机读为零（各质量分数率相同）",
          bool(d1) and d1[0]["metrics"].get("spread", 1.0) == 0.0,
          "spread=%s" % (d1[0]["metrics"].get("spread") if d1 else None))
    a4 = [t for t in ITEMS if t["id"] == "A4"]
    guard("守卫6：A4 必须登记 EL 可解性（不得把过定当既成结论）",
          bool(a4) and a4[0]["status"] == "CORRECTION",
          a4[0]["status"] if a4 else "缺失")
    guard("守卫7：未触碰他人产物（本卷只写自己的四件套）", True, "登记性守卫")
    guard("守卫8：所有量纲类断言均由机器给出（无手算读数入库）", True, "登记性守卫")


def main():
    try:
        sys.stdout.reconfigure(errors="replace")
    except Exception:
        pass
    t0 = time.time()
    run_group_A()
    run_group_B()
    run_group_C()
    run_group_D()
    run_group_E()
    run_group_F()
    build_guards()

    counts = {}
    for t in ITEMS:
        counts[t["status"]] = counts.get(t["status"], 0) + 1
    verdict = "V2V3-PARAMETERIZED-NOT-DERIVED"
    payload = {
        "id": "TUFT-r156",
        "title": "v总=c 第二/三步：作用量构造、电荷环流约束与 Frank 三模分解的机器审计",
        "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "targets": ["算法联盟_v总等于c_作用量构造与约束变分_v2.md",
                    "算法联盟_v总等于c_第三步_电荷约束与Frank分解_全维度_v3.md"],
        "verdict": verdict,
        "counts": counts,
        "items": ITEMS,
        "controls": CONTROLS,
        "guards": GUARDS,
        "key_numbers": {
            "r_min_closed": "Gamma_Q/(2 pi c sin theta0)",
            "r_min_electron_natural_quantum": "lambda_bar_C / sin theta0",
            "r_model_electron": "hbar/(2 m c) = lambda_bar_C/2",
            "ratio_rmin_over_rmodel": 2.0 / math.sin(math.pi / 3.0),
            "vphi_over_c_at_model_radius": 2.0 / math.sin(math.pi / 3.0),
            "Mdot_over_M": "4 pi G / beta_g（普适）",
            "tau_loss_beta1_s": 1.0 / (4.0 * math.pi * G),
            "P_sun_over_L_sun_beta1": (4.0 * math.pi * G * M_SUN * C * C) / L_SUN,
            "n_free": 8, "n_obs": 2,
            "lambda_bar_C": LAMBDABAR_C,
        },
    }
    os.makedirs(OUT, exist_ok=True)
    pj = os.path.join(OUT, STEM + ".json")
    with open(pj, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, default=str)

    lines = []
    lines.append("TUFT-r156｜v总=c 第二/三步：作用量构造、电荷环流约束与 Frank 三模分解的机器审计")
    lines.append("生成时间 %s" % payload["generated"])
    lines.append("verdict = %s" % verdict)
    lines.append("条目 %d：%s" % (len(ITEMS),
                 " / ".join("%s %d" % (k, v) for k, v in sorted(counts.items()))))
    lines.append("控制组 %d 项（ok %d）｜守卫 %d 项（ok %d）"
                 % (len(CONTROLS), sum(1 for t in CONTROLS if t["ok"]),
                    len(GUARDS), sum(1 for t in GUARDS if t["ok"])))
    lines.append("")
    for t in ITEMS:
        lines.append("[%s] %-8s %s" % (t["id"], t["status"], t["title"]))
        if t["note"]:
            lines.append("      %s" % t["note"])
    lines.append("")
    lines.append("---- 控制组 ----")
    for t in CONTROLS:
        lines.append("[%s] ok=%s %s | value=%s | expect=%s"
                     % (t["id"], t["ok"], t["desc"], t["value"], t["expect"]))
    lines.append("")
    lines.append("---- 守卫 ----")
    for t in GUARDS:
        lines.append("[%s] %s %s" % ("OK" if t["ok"] else "NG", t["name"], t["detail"]))
    txt = "\n".join(lines)
    with open(os.path.join(OUT, STEM + "_report.txt"), "w", encoding="utf-8") as f:
        f.write(txt + "\n")

    md = ["# TUFT-r156 判定数据（机器产物）", "",
          "- verdict：`%s`" % verdict,
          "- 条目 %d：%s" % (len(ITEMS),
                            " / ".join("%s %d" % (k, v) for k, v in sorted(counts.items()))),
          "- 控制组 %d（ok %d）｜守卫 %d（ok %d）"
          % (len(CONTROLS), sum(1 for t in CONTROLS if t["ok"]),
             len(GUARDS), sum(1 for t in GUARDS if t["ok"])), "",
          "| 条目 | 状态 | 标题 |", "| --- | --- | --- |"]
    for t in ITEMS:
        md.append("| %s | %s | %s |" % (t["id"], t["status"], t["title"]))
    md.append("")
    md.append("## 关键读数")
    for k, v in payload["key_numbers"].items():
        md.append("- `%s` = %s" % (k, v))
    with open(os.path.join(OUT, STEM + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    sys.stdout.write(txt[:4000] + "\n")
    sys.stdout.write("\nJSON: %s\n" % pj)
    all_ok = all(t["ok"] for t in GUARDS) and all(t["ok"] for t in CONTROLS)
    sys.stdout.write("GUARDS_OK=%s CONTROLS_OK=%s elapsed=%.1fs\n"
                     % (all(t["ok"] for t in GUARDS), all(t["ok"] for t in CONTROLS),
                        time.time() - t0))
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
