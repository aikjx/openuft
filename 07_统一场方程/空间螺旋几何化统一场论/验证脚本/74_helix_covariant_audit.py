# -*- coding: utf-8 -*-
"""
74 号仪器 · 螺旋本源体系原版「协变大统一方程组」全维审计

对应文档
--------
74_螺旋本源体系原版审计_修复优化_原创协变大统一方程组.tex

判定口径（与本目录 68/70/71/72 号同源）
--------------------------------------
1. 只判三类可机算事项：数学恒等 / 量纲自洽 / 常数算术；不判物理真伪；
2. 恒等式标 IDN（零预测力），几何定义标 DEF，条件结果标 RES；
3. 原版自身缺陷记 FAIL —— 这是本卷结论，不是仪器缺陷；
4. 仪器自身缺陷（守卫红 / 控制组不红）⇒ 退出码 2；
5. 本卷结论含 FAIL ⇒ 退出码 1；否则退出码 0。

运行
----
    python 74_helix_covariant_audit.py
    python 74_helix_covariant_audit.py --quiet

依赖：纯标准库（decimal 60 位 + fractions 量纲向量），无需 sympy。
"""

from __future__ import annotations

import io
import json
import os
import sys
from decimal import Decimal, getcontext, ROUND_HALF_EVEN
from fractions import Fraction

getcontext().prec = 60

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # pragma: no cover
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, "74_helix_covariant_audit_results.json")
OUT_TXT = os.path.join(HERE, "74_helix_covariant_audit_out.txt")

QUIET = "--quiet" in sys.argv

RESULTS = []


def rec(sid, title, kind, verdict, detail):
    RESULTS.append({"id": sid, "title": title, "kind": kind,
                    "verdict": verdict, "detail": detail})


def fs(x):
    """Decimal → 定点科学计数（避开 quantize 的 InvalidOperation 陷阱）。

    注意：Decimal 的「零」会携带标度指数（如 0E-34），直接格式化会打印成
    0.000...E-34，极易被误读成 1e-34。故零一律归一为显式「机器零」。
    """
    if x == 0:
        return "0（机器零）"
    return format(x, ".25E")


# ----------------------------------------------------------------- 量纲向量
# 基：M 质量 / L 长度 / T 时间 / I 电流（SI 基本量纲）
DIM_IDX = {"M": 0, "L": 1, "T": 2, "I": 3}


def dm(*pairs):
    v = [Fraction(0)] * 4
    for e, b in pairs:
        v[DIM_IDX[b]] += Fraction(e)
    return tuple(v)


def dadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def dsub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def dinv(a):
    return tuple(-x for x in a)


def dpow(a, n):
    return tuple(x * n for x in a)


def dzero(a):
    return all(x == 0 for x in a)


def dshow(a):
    parts = []
    for name, idx in (("M", 0), ("L", 1), ("T", 2), ("I", 3)):
        if a[idx] != 0:
            parts.append("{}^{}".format(name, a[idx]))
    return "·".join(parts) if parts else "1"


MASS = dm((1, "M"))
LENGTH = dm((1, "L"))
TIME = dm((-1, "T"))
CURR = dm((1, "I"))
C_LT = dm((1, "L"), (-1, "T"))
G_DIM = dm((-1, "M"), (3, "L"), (-2, "T"))
MU0 = dm((1, "M"), (1, "L"), (-2, "T"), (-2, "I"))
EPS0 = dm((-1, "M"), (-3, "L"), (4, "T"), (2, "I"))
ALPHA = (Fraction(0),) * 4
Q_DIM = dm((1, "I"), (1, "T"))
OMEGA = dm((-1, "T"))
KAPPA = dm((-1, "L"))
TAU = dm((-1, "L"))
E_FIELD = dm((1, "M"), (1, "L"), (-3, "T"), (-1, "I"))
B_FIELD = dm((1, "M"), (0, "L"), (-2, "T"), (-1, "I"))
A_VEC = dm((1, "M"), (1, "L"), (-2, "T"), (-1, "I"))
G_FIELD = dm((1, "L"), (-2, "T"))
FORCE = dm((1, "M"), (1, "L"), (-2, "T"))
MOM = dm((1, "M"), (1, "L"), (-1, "T"))
ANGMOM = dm((1, "M"), (2, "L"), (-1, "T"))
ENERGY = dm((1, "M"), (2, "L"), (-2, "T"))
J_MASS = dm((1, "M"), (0, "L"), (-3, "T"))
AREA = dm((0, "M"), (2, "L"))
PHI_DIM = dm((1, "M"), (2, "L"), (-2, "T"), (-1, "I"))
SOLID = (Fraction(0),) * 4


def dcheck(sid, title, kind, lhs, rhs, note):
    dd = dsub(lhs, rhs)
    ok = dzero(dd)
    if ok:
        detail = note + "；齐次，量纲 " + dshow(lhs)
    else:
        detail = (note + "；不齐：左 " + dshow(lhs) + "，右 " + dshow(rhs)
                  + "，差 " + dshow(dd))
    rec(sid, title, kind, "PASS" if ok else "FAIL", detail)
    return ok


# ------------------------------------------------------- 高精度三角函数（自实现）
def _atan_inv(x, terms=500):
    """arctan(1/x) 级数（x>1 收敛）。"""
    s = Decimal(0)
    x2 = x * x
    term = Decimal(1) / x
    for i in range(terms):
        s += term / (2 * i + 1) if i % 2 == 0 else -term / (2 * i + 1)
        term = term / x2
    return s


PI = 16 * _atan_inv(Decimal(5)) - 4 * _atan_inv(Decimal(239))
TWO_PI = 2 * PI
_EPS = Decimal(10) ** (-getcontext().prec - 5)


def _reduce(x):
    q = (x / TWO_PI).to_integral_value(rounding=ROUND_HALF_EVEN)
    return x - q * TWO_PI


def dsin(x):
    x = _reduce(x)
    s = Decimal(0)
    term = x
    k = 0
    while True:
        s += term
        k += 1
        term = -term * x * x / ((2 * k) * (2 * k + 1))
        if abs(term) < _EPS:
            break
    return s


def dcos(x):
    x = _reduce(x)
    s = Decimal(0)
    term = Decimal(1)
    k = 0
    while True:
        s += term
        k += 1
        term = -term * x * x / ((2 * k - 1) * (2 * k))
        if abs(term) < _EPS:
            break
    return s


def vadd(a, b):
    return tuple(a[i] + b[i] for i in range(3))


def vsub(a, b):
    return tuple(a[i] - b[i] for i in range(3))


def vscale(a, s):
    return tuple(a[i] * s for i in range(3))


def vdot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def vcross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def vnorm(a):
    return vdot(a, a).sqrt()


# ------------------------------------------------------------------ 螺旋族
class Helix:
    """圆柱螺旋世界线 R(t)=(r cos wt, r sin wt, h t)，约束 (r w)^2 + h^2 = c^2。"""

    def __init__(self, r, w, h, c_override=None):
        self.r = Decimal(r)
        self.w = Decimal(w)
        self.h = Decimal(h)
        # 几何本征速率（由参数唯一决定）——曲率/挠率是几何不变量，只依赖它
        self.c_geom2 = (self.r * self.w) ** 2 + self.h ** 2
        self.c_geom = self.c_geom2.sqrt()
        # 外部声明的光速：本源公设要求 c_decl == c_geom（|v| = c）；
        # 对照组取 c_decl > c_geom ⇒ 亚光速 ⇒ 解除类空
        if c_override is None:
            self.c_decl = self.c_geom
        else:
            self.c_decl = Decimal(c_override)
        self.c_decl2 = self.c_decl * self.c_decl
        # 兼容别名
        self.c = self.c_decl
        self.c2 = self.c_decl2

    def R(self, t):
        t = Decimal(t)
        return (self.r * dcos(self.w * t), self.r * dsin(self.w * t), self.h * t)

    def dR(self, t):
        t = Decimal(t)
        return (-self.r * self.w * dsin(self.w * t),
                self.r * self.w * dcos(self.w * t),
                self.h)

    def ddR(self, t):
        t = Decimal(t)
        return (-self.r * self.w ** 2 * dcos(self.w * t),
                -self.r * self.w ** 2 * dsin(self.w * t),
                Decimal(0))

    def dddR(self, t):
        t = Decimal(t)
        return (self.r * self.w ** 3 * dsin(self.w * t),
                -self.r * self.w ** 3 * dcos(self.w * t),
                Decimal(0))

    def frame(self, t):
        """解析 Frenet 标架 (T, N, B)。"""
        T = vscale(self.dR(t), Decimal(1) / self.c_geom)
        acc = self.ddR(t)
        nrm = vnorm(acc)
        N = vscale(acc, Decimal(1) / nrm) if nrm > 0 else (Decimal(0),) * 3
        B = vcross(T, N)
        return T, N, B

    def fd2(self, t, h):
        """二阶导（中心差分 + Richardson 外推，误差 O(h^4)）。"""
        r0 = self.R(t)
        raw = tuple((self.R(t + h)[i] - 2 * r0[i] + self.R(t - h)[i]) / (h * h)
                    for i in range(3))
        hh = h / 2
        fine = tuple((self.R(t + hh)[i] - 2 * r0[i] + self.R(t - hh)[i]) / (hh * hh)
                     for i in range(3))
        return tuple((4 * fine[i] - raw[i]) / 3 for i in range(3))

    def fd3(self, t, h):
        """三阶导（中心差分 + Richardson 外推）。"""
        raw = tuple((self.R(t + 2 * h)[i] - 2 * self.R(t + h)[i]
                     + 2 * self.R(t - h)[i] - self.R(t - 2 * h)[i]) / (2 * h ** 3)
                    for i in range(3))
        hh = h / 2
        fine = tuple((self.R(t + 2 * hh)[i] - 2 * self.R(t + hh)[i]
                      + 2 * self.R(t - hh)[i] - self.R(t - 2 * hh)[i]) / (2 * hh ** 3)
                     for i in range(3))
        return tuple((4 * fine[i] - raw[i]) / 3 for i in range(3))

    def frame_fd(self, t, h):
        """dN/dt 与 dB/dt 的数值导数（Richardson）。"""
        def nth(hh):
            return self.frame(t + hh)[1]

        def bth(hh):
            return self.frame(t + hh)[2]

        dN_raw = tuple((nth(h)[i] - nth(-h)[i]) / (2 * h) for i in range(3))
        dN_fine = tuple((nth(h / 2)[i] - nth(-h / 2)[i]) / h for i in range(3))
        dN = tuple((4 * dN_fine[i] - dN_raw[i]) / 3 for i in range(3))
        dB_raw = tuple((bth(h)[i] - bth(-h)[i]) / (2 * h) for i in range(3))
        dB_fine = tuple((bth(h / 2)[i] - bth(-h / 2)[i]) / h for i in range(3))
        dB = tuple((4 * dB_fine[i] - dB_raw[i]) / 3 for i in range(3))
        return dN, dB


H1 = Helix(1, 2, 3)          # r=1 m, w=2 rad/s, h=3 m/s ⇒ c=sqrt(13)
H2 = Helix(2, "0.5", 1)      # 第二组参数（参数无关性）
HCIRC = Helix(1, 2, 0)       # h=0 ⇒ 平面圆 ⇒ tau ≡ 0
HLINE = Helix(0, 2, 3)       # r=0 ⇒ 直线 ⇒ kappa=tau=0
TS = Decimal("0.37")         # 取样时刻
HS = Decimal("1e-4")         # 差分步长（w·h ≪ 1）


def kappa_fd(hx, t, h):
    v = hx.dR(t)
    acc = hx.fd2(t, h)
    cr = vcross(v, acc)
    return vnorm(cr) / (vnorm(v) ** 3)


def tau_fd(hx, t, h):
    v = hx.dR(t)
    acc = hx.fd2(t, h)
    jrk = hx.fd3(t, h)
    cr = vcross(v, acc)
    return vdot(cr, jrk) / vdot(cr, cr)


def kappa_an(hx):
    """解析曲率（几何不变量，与外部声明的 c 无关）。"""
    return hx.r * hx.w ** 2 / hx.c_geom2


def tau_an(hx):
    """解析挠率（几何不变量，与外部声明的 c 无关）。"""
    return hx.h * hx.w / hx.c_geom2


# =============================================================== 守卫组（仪器自检）
rec("G01", "自实现 Decimal 三角函数：已知特殊角守卫", "DEF",
    "PASS" if (abs(dsin(PI / 6) - Decimal("0.5")) < Decimal("1e-55")
               and abs(dcos(PI / 3) - Decimal("0.5")) < Decimal("1e-55")
               and abs(dsin(PI / 2) - Decimal(1)) < Decimal("1e-55")
               and abs(dcos(PI) + Decimal(1)) < Decimal("1e-55")) else "FAIL",
    "sin(pi/6)=0.5, cos(pi/3)=0.5, sin(pi/2)=1, cos(pi)=-1")

rec("G02", "Machin 公式 pi 与已知 40 位值一致", "DEF",
    "PASS" if abs(PI - Decimal("3.1415926535897932384626433832795028841971")) < Decimal("1e-38") else "FAIL",
    "pi = " + fs(PI))

_t1 = Decimal("1.3")
rec("G03", "sin^2+cos^2=1 归约守卫", "DEF",
    "PASS" if abs(dsin(_t1) ** 2 + dcos(_t1) ** 2 - Decimal(1)) < Decimal("1e-55") else "FAIL",
    "残差 " + fs(dsin(_t1) ** 2 + dcos(_t1) ** 2 - Decimal(1)))

rec("G04", "量纲工具守卫：1/G·G 无量纲、c^2=L^2T^-2", "DEF",
    "PASS" if (dzero(dmul(dinv(G_DIM), G_DIM))
               and dmul(C_LT, C_LT) == dm((2, "L"), (-2, "T"))) else "FAIL",
    "1/G·G=1；[c^2]=" + dshow(dmul(C_LT, C_LT)))

_hh = HS / 2
_e1 = abs(kappa_fd(H1, TS, _hh) - kappa_fd(H1, TS, HS))
_e2 = abs(kappa_fd(H1, TS, HS) - kappa_fd(H1, TS, HS * 2))
rec("G05", "有限差分截断阶：步长减半误差比 ≈ 1/16（Richardson 四阶有效）", "DEF",
    "PASS" if (Decimal("0.02") < (_e1 / _e2) < Decimal("0.12")) else "FAIL",
    "e(h/2)/e(h) = " + fs(_e1 / _e2) + "（四阶理论 1/16 = 0.0625）")

_dk = (kappa_an(H1) - kappa_an(H1))
rec("G06", "解析路径非恒等复读：kappa 随 r 变化（偏导非零）", "DEF",
    "PASS" if abs((kappa_an(Helix(2, 2, 3)) - kappa_an(H1)) / Decimal(1)) > Decimal("1e-6") else "FAIL",
    "d kappa / d r = " + fs(kappa_an(Helix(2, 2, 3)) - kappa_an(H1)))


# ========================================================= 运动学 / 协变层 K
def rel(a, b):
    den = max(abs(b), Decimal("1e-30"))
    return abs(a - b) / den


for sid, hx, label in (("K01", H1, "H1"), ("K02", H2, "H2")):
    res = max(abs(vdot(hx.dR(Decimal(t)), hx.dR(Decimal(t))) - hx.c_decl2)
              for t in ("0", "0.37", "1.13"))
    rec(sid, "速率约束 |dR/dt|^2 = (r w)^2 + h^2 = c^2  [" + label + "]", "DEF",
        "PASS" if res < Decimal("1e-40") else "FAIL",
        "最大残差 " + fs(res) + "；c = " + fs(hx.c_decl) + " m/s")

for sid, hx, label in (("K03", H1, "H1"), ("K04", H2, "H2")):
    an = kappa_an(hx)
    nu = kappa_fd(hx, TS, HS)
    rec(sid, "曲率双路径：kappa = r w^2/c^2（解析 vs Frenet 有限差分）[" + label + "]", "RES",
        "PASS" if rel(an, nu) < Decimal("1e-10") else "FAIL",
        "解析 " + fs(an) + "，数值 " + fs(nu) + "，相对残差 " + fs(rel(an, nu)) + "（停在差分截断极限，非 0）")

for sid, hx, label in (("K05", H1, "H1"), ("K06", H2, "H2")):
    an = tau_an(hx)
    nu = tau_fd(hx, TS, HS)
    rec(sid, "挠率双路径：tau = h w/c^2（解析 vs Frenet 有限差分）[" + label + "]", "RES",
        "PASS" if rel(an, nu) < Decimal("1e-10") else "FAIL",
        "解析 " + fs(an) + "，数值 " + fs(nu) + "，相对残差 " + fs(rel(an, nu)) + "（停在差分截断极限，非 0）")

rec("K07", "比值 kappa/tau = r w/h（横向线速度 / 轴向推进速度）", "RES",
    "PASS" if abs(kappa_an(H1) / tau_an(H1) - (H1.r * H1.w) / H1.h) == 0 else "FAIL",
    "kappa/tau = " + fs(kappa_an(H1) / tau_an(H1)) + "，r w/h = " + fs((H1.r * H1.w) / H1.h))

rec("K08", "主恒等式 kappa^2 + tau^2 = (w/c)^2", "IDN",
    "PASS" if abs(kappa_an(H1) ** 2 + tau_an(H1) ** 2 - (H1.w / H1.c) ** 2) < Decimal("1e-55") else "FAIL",
    "残差 " + fs(kappa_an(H1) ** 2 + tau_an(H1) ** 2 - (H1.w / H1.c) ** 2) + "（与本目录 68 号 G4 同源）")

rec("K09", "退化核：h=0 ⇒ tau ≡ 0（平面圆）", "RES",
    "PASS" if tau_an(HCIRC) == 0 and kappa_an(HCIRC) > 0 else "FAIL",
    "tau = " + fs(tau_an(HCIRC)) + "，kappa = " + fs(kappa_an(HCIRC)))

rec("K10", "退化核：r=0 ⇒ kappa ≡ 0（直线，无偏转）", "RES",
    "PASS" if kappa_an(HLINE) == 0 else "FAIL",
    "kappa = " + fs(kappa_an(HLINE)) + "；说明：曲率是几何不变量，直线极限严格为 0")
rec("K10b", "退化核：r=0 ⇒ 挠率在 Frenet 标架下未定义（法向为零向量）", "BOUNDARY",
    "BOUNDARY",
    "|d²R/dt²| = " + fs(vnorm(HLINE.ddR(TS)))
    + " ⇒ Frenet 法向 N 无定义 ⇒ 解析式 tau = h·w/c² 的适用域要求 r ≠ 0；"
      "沿族 r→0 的极限 tau → w/h 是族极限而非直线的挠率")

# ---- 协变导数的三个分量（本卷原创判决核心）
T1, N1, B1 = H1.frame(TS)
dc_dt = H1.fd2(TS, HS)          # d c/dt = d2R/dt2（数值路径）
comp_T = vdot(dc_dt, T1)
comp_N = vdot(dc_dt, N1)
comp_B = vdot(dc_dt, B1)
rec("K11", "D c/Dt 的主法向分量 = c^2 kappa = r w^2", "RES",
    "PASS" if abs(comp_N - H1.c2 * kappa_an(H1)) < Decimal("1e-8") * max(abs(comp_N), Decimal(1)) else "FAIL",
    "分量 " + fs(comp_N) + "，预期 " + fs(H1.c2 * kappa_an(H1)))
rec("K12", "D c/Dt 的切向分量 ≡ 0（机器零）", "IDN",
    "PASS" if abs(comp_T) < Decimal("1e-10") * max(abs(comp_N), Decimal(1)) else "FAIL",
    "分量 " + fs(comp_T))
rec("K13", "D c/Dt 的副法向分量 ≡ 0 ⇒ 挠率项恒不出现（机器零）", "IDN",
    "PASS" if abs(comp_B) < Decimal("1e-10") * max(abs(comp_N), Decimal(1)) else "FAIL",
    "分量 " + fs(comp_B) + "（原版宣称的挠率项系数在此为零）")

# ---- 原版两条「D c/Dt」公式的残差
draft_a = vadd(vscale(N1, H1.w ** 2 * H1.r), vscale(B1, H1.w * tau_an(H1)))
draft_b = vadd(vscale(N1, kappa_an(H1) * H1.c2), vscale(B1, tau_an(H1) * H1.c2))
res_a = vnorm(vsub(dc_dt, draft_a))
res_b = vnorm(vsub(dc_dt, draft_b))
rec("K14", "原版 §7 式 D c/Dt = w^2 r N + w tau B 的残差", "FAIL",
    "FAIL" if res_a > Decimal("1e-12") else "PASS",
    "残差 " + fs(res_a) + "（理论预期 |w tau| = " + fs(H1.w * tau_an(H1)) + "）")
rec("K15", "原版定理 2 式 D c/Dt = kappa c^2 N + tau c^2 B 的残差", "FAIL",
    "FAIL" if res_b > Decimal("1e-12") else "PASS",
    "残差 " + fs(res_b) + "（理论预期 |tau c^2| = " + fs(tau_an(H1) * H1.c2) + "）")
rec("K16", "原版 §7 式与定理 2 式互不相等 ⇒ 原版内部不自洽", "FAIL",
    "FAIL" if vnorm(vsub(draft_a, draft_b)) > Decimal("1e-12") else "PASS",
    "互差 " + fs(vnorm(vsub(draft_a, draft_b))) + "（差 = tau (w - c^2)）")

# ---- 输运三角表（本卷原创构造）
dT_dt = vscale(H1.fd2(TS, HS), Decimal(1) / H1.c)
dN_dt, dB_dt = H1.frame_fd(TS, HS)
ck = H1.c * kappa_an(H1)
ct = H1.c * tau_an(H1)
tri = []
for name, vec, eT, eN, eB in (("dT/dt", dT_dt, Decimal(0), ck, Decimal(0)),
                              ("dN/dt", dN_dt, -ck, Decimal(0), ct),
                              ("dB/dt", dB_dt, Decimal(0), -ct, Decimal(0))):
    got = (vdot(vec, T1), vdot(vec, N1), vdot(vec, B1))
    exp = (eT, eN, eB)
    scale = max(abs(vdot(dT_dt, N1)), Decimal("1e-12"))
    err = max(abs(got[i] - exp[i]) for i in range(3)) / scale
    tri.append((name, got, exp, err))
tri_ok = all(err < Decimal("1e-9") for _, _, _, err in tri)
rec("K17", "Frenet 输运三角表：挠率只出现在 dN/dt 与 dB/dt，dT/dt 只含曲率", "RES",
    "PASS" if tri_ok else "FAIL",
    " | ".join("{}: T={} N={} B={} (预期 T={} N={} B={}, 归一残差 {})".format(
        n, fs(g[0]), fs(g[1]), fs(g[2]), fs(e[0]), fs(e[1]), fs(e[2]), fs(err))
        for n, g, e, err in tri))

# ---- 类空公设 ⇒ 协变升级不可行
def minkowski_gap(hx, t, dt):
    a = hx.R(t)
    b = hx.R(t + dt)
    return -hx.c_decl2 * dt * dt + vdot(vsub(b, a), vsub(b, a))


_dt_a = Decimal("1e-3")
_dt_b = _dt_a / 2
_rel_a = max(abs(minkowski_gap(H1, Decimal(t), _dt_a)) for t in ("0", "0.37", "1.13")) \
    / (H1.c_decl2 * _dt_a * _dt_a)
_rel_b = max(abs(minkowski_gap(H1, Decimal(t), _dt_b)) for t in ("0", "0.37", "1.13")) \
    / (H1.c_decl2 * _dt_b * _dt_b)
_q = Decimal(1) - (vnorm(H1.dR(TS)) / H1.c_decl) ** 2
dtau_dt = _q.sqrt() if _q > 0 else Decimal(0)
rec("K18", "本源约束 |dR/dt| = c ⇒ 世界线类空（有限弦 ds^2<0 且 ds^2/dt^2 → 0）", "DEF",
    "PASS" if (Decimal("0.2") < (_rel_b / _rel_a) < Decimal("0.3")) else "FAIL",
    "相对 |ds^2|/(c^2 dt^2)：dt=1e-3 时 " + fs(_rel_a) + "，dt=5e-4 时 " + fs(_rel_b)
    + "，比值 " + fs(_rel_b / _rel_a)
    + "（≈1/4 ⇒ ds^2 以二阶趋零 ⇒ 曲线类空；有限 dt 的弦落在光锥内 ds^2<0）")
rec("K19", "类空 ⇒ 固有时 dtau/dt = sqrt(1-|v|^2/c^2) ≡ 0 ⇒ 四速度未定义", "FAIL",
    "FAIL" if dtau_dt == 0 else "PASS",
    "1-|v|^2/c^2 = " + fs(_q) + "，dtau/dt = " + fs(dtau_dt) + "（协变升级所需的固有时不存在）")

HSUB = Helix(1, 1, 1, c_override=Decimal(2))  # 内禀 |v|=sqrt(2)，声明 c=2 ⇒ 亚光速
_qs = Decimal(1) - (vnorm(HSUB.dR(TS)) / HSUB.c_decl) ** 2
dtau_sub = _qs.sqrt() if _qs > 0 else Decimal(0)
rec("K20", "对照组（亚光速螺旋 |v| = c/sqrt(2)）：固有时非零 ⇒ 协变可定义", "RES",
    "PASS" if abs(dtau_sub - Decimal("0.7071067811865475244008443621048490392848")) < Decimal("1e-30") else "FAIL",
    "1-|v|^2/c^2 = " + fs(_qs) + "，dtau/dt = " + fs(dtau_sub)
    + "（对照：解除类空后协变构造有定义）")

# ---- K21：Eq-09-08 的一维数值核验（平直极限 ∇^2 L = c^-2 ∂_t^2 L）
def _plane_wave(u):
    return (-(u * u)).exp()


def _d2(f, x, h):
    return (f(x + h) - 2 * f(x) + f(x - h)) / (h * h)


_cw = Decimal("1.7")
_hw = Decimal("1e-4")
_xw = Decimal("0.8")
_lap_x = _d2(lambda y: _plane_wave(y - _cw), _xw, _hw)
_lap_t = _d2(lambda y: _plane_wave(_xw - y), _cw, _hw)
_res21 = abs(_lap_x - _lap_t)
rec("K21", "Eq-09-08 波动方程的一维平面波数值核验（∇^2L 与 c^-2 ∂_t^2L 同值）", "RES",
    "PASS" if _res21 < Decimal("1e-12") else "FAIL",
    "∇^2L = " + fs(_lap_x) + "，c^-2 ∂_t^2L = " + fs(_lap_t) + "，差 " + fs(_res21))


# ============================================================== 量纲层 D 组
# 逐条审计原版「正式收录的 23 条协变原创方程」（Eq-09-01 … Eq-09-23），
# 另立 X 组审计原版「废弃公式清单」。判据：SI 基本量纲四元组 (M, L, T, I)。
def dprod(*dims):
    out = (Fraction(0),) * 4
    for d in dims:
        out = dmul(out, d)
    return out


HBAR_DIM = dm((1, "M"), (2, "L"), (-1, "T"))     # 普朗克常数
Q_DENS = dprod(Q_DIM, dpow(dinv(LENGTH), 3))   # 电荷体密度 [rho_q] = I·T·L^-3
ACC = dm((0, "M"), (1, "L"), (-2, "T"))         # 加速度（引力场口径）
SCALAR_L = dm((1, "L"))                         # 长度型标量场
CUR_DENS = dm((0, "M"), (-2, "L"), (1, "I"))     # 电流密度
MOM_FLUX = dm((1, "M"), (-1, "L"), (-1, "T"))    # 质量流密度
GRAV_POT = dm((0, "M"), (2, "L"), (-2, "T"))     # 引力势
DT1 = dpow(dinv(TIME), -1)
DT2 = dpow(dinv(TIME), -2)
DL1 = dinv(LENGTH)
DL2 = dpow(dinv(LENGTH), 2)

# ---------------- 收录式：Eq-09-01 … Eq-09-23 逐条量纲判定 ----------------
dcheck("D01", "Eq-09-01 时空同一化：∂R/∂t = c(x,t)", "RES",
       dprod(LENGTH, DT1), C_LT,
       "左 = [R]/[t]，右 = [c]，齐次")
dcheck("D02", "Eq-09-02 圆柱螺旋 + 约束 (rω)^2 + h^2 = c^2", "DEF",
       dprod(LENGTH, LENGTH, OMEGA, OMEGA), dmul(C_LT, C_LT),
       "与本目录 68 号 G4 同源；本卷的公设底座")
dcheck("D03", "Eq-09-03 质量几何定义 m = (1/4πG)∮τ·dΣ", "FAIL",
       dprod(dinv(G_DIM), TAU, AREA), MASS,
       "左 = G^-1·τ·dΣ，右 = 质量 ⇒ 缺口 L^-1·T")
dcheck("D04", "Eq-09-04 引力场弱场定义 g = -GM r̂/r^2", "IDN",
       dprod(G_DIM, MASS, DL2), ACC,
       "牛顿引力的记号改写，量纲闭合")
dcheck("D05", "Eq-09-05 静止动量 p0 = m0 c0", "IDN",
       dprod(MASS, C_LT), MOM,
       "量纲闭合")
dcheck("D06", "Eq-09-06 运动动量 p = m(c - v)", "IDN",
       dprod(MASS, C_LT), MOM,
       "量纲闭合")
dcheck("D07", "Eq-09-07 协变大统一母力方程 F = (c-v)Dm/Dt + m Dc/Dt - m Dv/Dt", "IDN",
       dprod(MASS, DT1, C_LT), FORCE,
       "三项同量纲 ⇒ 量纲闭合；但整式 = d[m(c-v)]/dt ⇒ 乘积法则恒等，零预测力")
dcheck("D08", "Eq-09-08 协变空间波动方程 □L = 0（平直极限 ∇^2L - c^-2 ∂_t^2L = 0）", "RES",
       dprod(dpow(C_LT, -2), DT2, SCALAR_L), dprod(DL2, SCALAR_L),
       "修正式两侧齐次")
dcheck("D09", "Eq-09-09 电荷几何本源 q = (1/4π)∮ω dΩ", "FAIL",
       dprod(OMEGA, SOLID), Q_DIM,
       "左 = ω·dΩ，右 = 电荷 ⇒ 缺口 I·T^2")
dcheck("D10", "Eq-09-10 相对论总能量 E = γ m c^2", "IDN",
       dprod(MASS, C_LT, C_LT), ENERGY,
       "量纲闭合")
dcheck("D11", "Eq-09-11 运动电荷磁场 B = (μ0/4π) q v×R / R^3", "IDN",
       dprod(MU0, Q_DIM, C_LT, LENGTH, dpow(dinv(LENGTH), 3)), B_FIELD,
       "标准毕奥-萨伐尔场，量纲闭合")
dcheck("D12", "Eq-09-12 磁矢势涡旋关系 ∇×A = B", "IDN",
       dprod(DL1, A_VEC), B_FIELD,
       "标准恒等式，量纲闭合")
dcheck("D13", "Eq-09-13 光速推进动力学方程 F = (c-v)Dm/Dt", "RES",
       dprod(C_LT, MASS, DT1), FORCE,
       "量纲闭合")
dcheck("D14", "Eq-09-14 静止角动量 L = r×m c", "IDN",
       dprod(LENGTH, MASS, C_LT), ANGMOM,
       "量纲闭合")
dcheck("D15", "Eq-09-15 引力场达朗贝尔方程 □A = -4πG J_m", "FAIL",
       dprod(DL2, A_VEC), dprod(G_DIM, MOM_FLUX),
       "左 = □A，右 = G·质量流密度 ⇒ 缺口 M·L^-2·T·I^-1")
dcheck("D16", "Eq-09-16 变化引力通量与电荷拓扑关联 q = -d/dt ∮τ·dΣ", "FAIL",
       dprod(DT1, TAU, AREA), Q_DIM,
       "左 = ∂_t(τ·dΣ)，右 = 电荷 ⇒ 缺口 L^-1·I^-1")
dcheck("D17", "Eq-09-17 法拉第电磁感应协变形式 ∇×E = -DB/Dt", "IDN",
       dprod(DL1, E_FIELD), dprod(DT1, B_FIELD),
       "标准法拉第律，量纲闭合")
dcheck("D18", "Eq-09-18 电磁场-引力交叉耦合 g = c^-4(DE/Dt × B + E × DB/Dt)", "FAIL",
       dprod(dpow(C_LT, -4), DT1, E_FIELD, B_FIELD), ACC,
       "左 = c^-4·(∂_t E)×B，右 = 加速度 ⇒ 缺口 M^2·L^-4·I^-2")
rec("D19", "Eq-09-19 电场矢势定义 E = -∇φ - DA/Dt（两项不可相加）", "FAIL",
    "FAIL",
    "φ 读作电势：[∇φ] = " + dshow(dprod(DL1, PHI_DIM)) + "，而 [DA/Dt] = "
    + dshow(dprod(DT1, A_VEC)) + " ⇒ 差一个 T，两项不可相加；"
    "φ 读作引力势：[∇φ] = " + dshow(dprod(DL1, GRAV_POT))
    + " ⇒ 差 M^-1·T·I^-1，仍不可相加 ⇒ 两种读法均 FAIL")
rec("D20", "Eq-09-20 三场协变波动方程 □g = 0, □E = 0, □B = 0", "IDN",
    "IDN",
    "齐次方程：右端「0」按惯例取与左端同量纲的零（□g = " + dshow(dprod(DL2, ACC))
    + "，□E = " + dshow(dprod(DL2, E_FIELD)) + "，□B = " + dshow(dprod(DL2, B_FIELD))
    + "）⇒ 量纲自洽，但内容为「无源波动」的一般假设，非本体系的特征预言")
dcheck("D21", "Eq-09-21 拓扑电荷量子化 q = n e, n ∈ Z, π3(SU(2)) = Z", "IDN",
       dprod(ALPHA, Q_DIM), Q_DIM,
       "n 无量纲 ⇒ 量纲闭合；π3(SU(2)=Z) 属外部引用（见 S04）")
rec("D22", "Eq-09-22 精细结构常数 RG 跑动 α(μ) = g'^2(μ)/(4π)", "IDN",
    "IDN",
    "无量纲闭合；但该式本身只是耦合定义，跑动须另给 β 函数与边界条件 ⇒ "
    "定义式 ≠ 跑动预言（配套脚本 74_rg_alpha_running.py 只做标准模型 1-loop 跑动，不含本体系新内容）")

# Eq-09-23 的两种读法都要给出机器读数（a 读法给出量纲缺口，b 读法给出库内既有结论）
_a23 = dprod(Q_DIM, dinv(EPS0), dpow(C_LT, -3), ACC, LENGTH, ACC, DL1)
rec("D23", "Eq-09-23 加速电荷引力辐射类比场 g_rad = -(q/4πε0 c^3)·(a×(r×a))/r", "FAIL",
    "FAIL",
    "左 = " + dshow(_a23) + "，右 = [g] = " + dshow(ACC)
    + " ⇒ 缺口 M·I^-1，且 c 的任何幂次都消不掉 M 与 I^-1（同库内 2026-10-03 册 X-2 / D21b / D22）")

# ---------------- 库内锚交叉核对（证明「闭合的部分」即教科书物理） ----------------
dcheck("A01", "锚·标准 Maxwell ∇·E = ρ_q/ε0", "IDN",
       dprod(DL1, E_FIELD), dprod(Q_DENS, dinv(EPS0)),
       "库内 2026-10-03 册 K-10 交叉核对")
dcheck("A02", "锚·标准 Maxwell ∇×E = -∂B/∂t", "IDN",
       dprod(DL1, E_FIELD), dprod(DT1, B_FIELD),
       "与 Eq-09-17 同源")
dcheck("A03", "锚·标准 Maxwell ∇×B = μ0 J + μ0ε0 ∂E/∂t", "IDN",
       dprod(DL1, B_FIELD), dprod(MU0, CUR_DENS),
       "库内 2026-10-03 册 K-11 交叉核对")
dcheck("A04", "锚·α = e^2/(4πε0 ħ c) 无量纲", "IDN",
       dprod(Q_DIM, Q_DIM, dinv(EPS0), dinv(HBAR_DIM), dinv(C_LT)), ALPHA,
       "库内 2026-10-03 册 K-22 交叉核对")
dcheck("A05", "锚·偶极辐射 B_θ = q(a×r̂)/(4πε0 c^3 r)", "IDN",
       dprod(Q_DIM, ACC, dinv(EPS0), dpow(C_LT, -3), DL1), B_FIELD,
       "库内 2026-10-03 册 K-19 交叉核对")
dcheck("A06", "锚·量纲闭合的增广形态：Darboux 矢量 Ω = τT + κB", "RES",
       TAU, KAPPA,
       "两项同为 L^-1 ⇒ 允许引入含副法向分量的场")
dcheck("A07", "锚·涡量场 ∇×T = τT + κB（旋度扰动方案的量纲门槛）", "RES",
       dprod(DL1, SOLID), dprod(TAU, SOLID),
       "旋度源方案的量纲门槛")
dcheck("A08", "锚·挠率场动能项 [∂_τ τ]^2 与作用量密度同阶", "RES",
       dprod(DT1, KAPPA, DT1, KAPPA), dprod(DL2, DT2),
       "允许为挠率场补动能项（代价 +1 传播场）")

# ---------------- 原版废弃公式清单（8 条）逐条复核 ----------------
dcheck("X01", "废弃·E = r v^2 c^2 / G", "BOUNDARY",
       dprod(LENGTH, dmul(C_LT, C_LT), dmul(C_LT, C_LT), dinv(G_DIM)), ENERGY,
       "量纲闭合（能量），但库内无对应构造 ⇒ 闭合不等于成立")
dcheck("X02", "废弃·m = r v^2 / G", "BOUNDARY",
       dprod(LENGTH, dmul(C_LT, C_LT), dinv(G_DIM)), MASS,
       "量纲闭合（质量），但库内无对应构造")
rec("X03", "废弃·4π^2 r^3 c^2/(t^2 G h v) = 1", "BOUNDARY",
    "BOUNDARY",
    "按 v = 速率、h = 长度读：左 = " + dshow(dprod(LENGTH, LENGTH, LENGTH,
                                                        dmul(C_LT, C_LT),
                                                        DT2, G_DIM, C_LT, C_LT))
    + " ⇒ 非无量纲（缺 M^-1）；原文未附符号表，量纲读法依赖符号约定 ⇒ 本卷不判死")
rec("X04", "废弃·q = 4π v^2 r/(cG)", "FAIL",
    "FAIL",
    "左 = " + dshow(dprod(dmul(C_LT, C_LT), LENGTH, dinv(C_LT), dinv(G_DIM)))
    + "，右 = 电荷 ⇒ 缺口 M·L^-1·I^-1")
rec("X05", "废弃·m = η c q", "BOUNDARY",
    "BOUNDARY",
    "量纲相容的唯一读法是 [η] = M^-1（η 必须是质量倒数的量纲常数）；"
    "若 η 是无量纲参数则该式 FAIL ⇒ 原文必须显式声明 η 的量纲")
rec("X06", "废弃·G = α^2/ε0 c^2 = α^2 μ0", "FAIL",
    "FAIL",
    "左 = [G] = " + dshow(G_DIM) + "，右 = [α^2 μ0] = " + dshow(MU0)
    + " ⇒ 根本不在同一量纲族（见 N03 的数值巧合与 D18 的独立判定）")
rec("X07", "废弃·静止电荷产生磁场", "BOUNDARY",
    "BOUNDARY",
    "库内已判物理错误（静止电荷无电流、无磁场）；量纲上 B ∝ q·v ⇒ v = 0 ⇒ B ≡ 0，"
    "与「静止电荷产生磁场」直接矛盾")
rec("X08", "废弃·α = r/h_0 原始形式", "BOUNDARY",
    "BOUNDARY",
    "α 无量纲 ⇒ h_0 必须是长度标度；于是该式把 α 挂在一个外部长度上 ⇒ "
    "撞库内尺度开放项（本目录 68 号体系一 N = 137 拓扑缺口同族）")

# ============================================================== 常数层 N 组
C_LIGHT = Decimal("299792458")
HBAR_N = Decimal("1.054571817e-34")
EPS0_N = Decimal("8.8541878128e-12")
MU0_N = Decimal("1.25663706212e-6")
E_CHG = Decimal("1.602176634e-19")
G_EXP = Decimal("6.67430e-11")
ALPHA_INV_EXP = Decimal("137.035999084")
ANCHOR_C4_8PI_G = Decimal("4.8154538867224223992518906e+42")
ANCHOR_C4_G = Decimal("1.2102555643382062881895930e+44")


def drel(a, b):
    den = max(abs(b), Decimal("1e-30"))
    return abs(a - b) / den


_eps0mu0c2 = EPS0_N * MU0_N * C_LIGHT * C_LIGHT
rec("N01", "常数·ε0 μ0 c^2 = 1（CODATA 2018 口径）", "RES",
    "PASS" if drel(_eps0mu0c2, Decimal(1)) < Decimal("1e-8") else "FAIL",
    "实测 " + fs(_eps0mu0c2) + "，相对偏差 " + fs(drel(_eps0mu0c2, Decimal(1)))
    + "（偏差来自 CODATA 有效位数，非物理）")

_alpha = E_CHG * E_CHG / (4 * PI * EPS0_N * HBAR_N * C_LIGHT)
_alpha_inv = Decimal(1) / _alpha
rec("N02", "常数·α = e^2/(4πε0 ħc) 复算", "RES",
    "PASS" if drel(_alpha_inv, ALPHA_INV_EXP) < Decimal("1e-8") else "FAIL",
    "α^-1 实算 " + fs(_alpha_inv) + "，实验值 " + fs(ALPHA_INV_EXP)
    + "，相对偏差 " + fs(drel(_alpha_inv, ALPHA_INV_EXP)))

_alpha2mu0_over_G = _alpha * _alpha * MU0_N / G_EXP
rec("N03", "常数·原版「G = α^2 μ0」的数值核验（不含量纲合法性）", "FAIL",
    "FAIL" if drel(_alpha2mu0_over_G, Decimal(1)) > Decimal("1e-12") else "PASS",
    "α^2 μ0/G = " + fs(_alpha2mu0_over_G) + "，相对偏差 "
    + fs(drel(_alpha2mu0_over_G, Decimal(1)))
    + " ⇒ 数值在 0.3% 内成立，但 D18 已判该式量纲不齐 ⇒ 是非恒等巧合，零预测力")

_alpha_inv_pred = (MU0_N / G_EXP).sqrt()
rec("N04", "常数·由「G = α^2 μ0」反推 α^-1", "FAIL",
    "FAIL" if drel(_alpha_inv_pred, ALPHA_INV_EXP) > Decimal("1e-12") else "PASS",
    "α^-1_pred = √(μ0/G) = " + fs(_alpha_inv_pred) + "，实验 α^-1 = " + fs(ALPHA_INV_EXP)
    + "，相对偏差 " + fs(drel(_alpha_inv_pred, ALPHA_INV_EXP))
    + "；且 D19 判该反解式量纲不齐 ⇒ 不得作预言使用")

_c4_8pi_g = C_LIGHT ** 4 / (8 * PI * G_EXP)
rec("N05", "常数·c^4/(8πG) 与库内锚点交叉核对", "RES",
    "PASS" if drel(_c4_8pi_g, ANCHOR_C4_8PI_G) < Decimal("1e-4") else "FAIL",
    "实测 " + fs(_c4_8pi_g) + "，库内锚点 " + fs(ANCHOR_C4_8PI_G)
    + "，相对偏差 " + fs(drel(_c4_8pi_g, ANCHOR_C4_8PI_G))
    + "（G 仅 5~6 位有效数字，偏差落在其上限内）")

_c4_g = C_LIGHT ** 4 / G_EXP
rec("N06", "常数·c^4/G 与库内锚点交叉核对", "RES",
    "PASS" if drel(_c4_g, ANCHOR_C4_G) < Decimal("1e-4") else "FAIL",
    "实测 " + fs(_c4_g) + "，库内锚点 " + fs(ANCHOR_C4_G)
    + "，相对偏差 " + fs(drel(_c4_g, ANCHOR_C4_G)))

_mu0_4pi = 4 * PI * Decimal("1e-7")
rec("N07", "常数·μ0(CODATA 2018) 与 4π×10^-7 的偏离（2019 SI 重定义余量）", "INFO",
    "INFO",
    "μ0 = " + fs(MU0_N) + "，4π×10^-7 = " + fs(_mu0_4pi)
    + "，相对差 " + fs(drel(MU0_N, _mu0_4pi))
    + " ⇒ 「μ0 = 4π×10^-7」只到 10^-9 级，会污染任何以 μ0 为输入的反解")

_z_gc = G_EXP * C_LIGHT / 2
rec("N08", "常数·原版「Z ≡ Gc/2 ≈ 0.01 很整齐」的数值核验", "INFO",
    "INFO",
    "Z = " + fs(_z_gc) + "，与 0.01 的相对偏差 " + fs(drel(_z_gc, Decimal("0.01")))
    + " ⇒ 「很整齐」是单位依赖的伪显著（同 2026-10-03 册 X-7）")

# ============================================================== 结构层 S 组
dcheck("S01", "结构·Eq-09-07 统一力方程的量纲闭合", "IDN",
       dprod(MASS, DT1, C_LT), FORCE,
       "三项同量纲；但整式等于 d[m(c-v)]/dt ⇒ 乘积法则恒等，零预测力")

rec("S02", "结构·四力分项映射（引力/电磁/强/弱→螺旋量）无推导依据", "BOUNDARY",
    "BOUNDARY",
    "本卷不重判：与本目录 62/63 号「对称性 no-go、反解定理」、70 号「力统一供给需求预算」同向，"
    "结论以 70 号定理 E 为准；本卷只登记「映射规则未给出」这一事实")

rec("S03", "结构·弱力映射被本目录 70 号定理 E 独立否证", "BOUNDARY",
    "BOUNDARY",
    "回链本目录 70 号：弱扇区在供给/需求预算下不闭合 ⇒ 原版四力统一声明在该扇区已被库内否证")

rec("S04", "结构·主丛 π3(SU(2)) 桥接属外部引用", "INFO",
    "INFO",
    "几何旋量场→规范场是另行建立的结构对应，本卷不视其为从螺旋公设导出；标记为外部输入")

rec("S05", "结构·最小增广的自由度记账（引入含副法向分量的场）", "BOUNDARY",
    "BOUNDARY",
    "引入 Darboux 矢量/涡量场 ⇒ 新增 1 个场（自由函数），按「常数+节点+自由函数」口径自由度数 +1"
    "（回链本目录 15 号册口径）；按「自由常数≤1」口径不冲突 ⇒ 须显式声明采用哪一口径")

rec("S06", "结构·挠率场的传播性缺失（作为独立场需动能项）", "BOUNDARY",
    "BOUNDARY",
    "A08 已给出动能项的量纲门槛（可行），但方程层面的完备性不在本卷判定范围 ⇒ 记账不判定")

rec("S07", "结构·旋度扰动方案的可证伪性", "BOUNDARY",
    "BOUNDARY",
    "本卷只给量纲门槛（A07），不给定量预言 ⇒ 「扰动后可观测量如何变化」仍开放")

rec("S08", "结构·「36 式」编号口径与库内 23 式台账的关系", "INFO",
    "INFO",
    "库内已记：同一批公式存在 17/18/20/23/28 五种编号口径（2026-10-03 册 C-01）⇒ 原版 36 式为又一口径；"
    "跨册引用「第 N 式」必须声明口径，否则断链")

rec("S09", "结构·四项「几何本源映射」不是单射（第 2、3 项表达式逐字相同）", "FAIL",
    "FAIL",
    "原版把 (c-v)Dm/Dt 同时指派为「电场力」与「磁场力」⇒ 两个不同的相互作用被指派给同一项 ⇒ "
    "四项到四力的映射不可能单射 ⇒ 不可能由该式把四种相互作用分别归因；"
    "机器复核：两项量纲向量同为 " + dshow(dprod(C_LT, MASS, DT1)))

rec("S10", "结构·原版的 Frenet 公式被机器否证（Ṫ 无挠率项）", "FAIL",
    "FAIL",
    "原版写 dT/dt = κc N + τc B；本卷用 Frenet-Serret 标准式复核（K17 输运三角表）："
    "dT/dt 的 B 分量 ≡ 0（机器零），挠率只出现在 dN/dt 与 dB/dt ⇒ "
    "由此推出的 Dc/Dt = κc^2 N + τc^2 B 的 B 分量无来源（K15 残差 = |τc^2|）")

rec("S11", "结构·「原创」归属的诚实边界", "BOUNDARY",
    "BOUNDARY",
    "本卷确认的原创增量只有三项：(1) Frenet 求导得 κ = rω^2/c^2、τ = hω/c^2（自证，IDN）；"
    "(2) 切向速度场协变导数不含挠率（机器零，K13/K17）；"
    "(3) 类空公设使协变升级在公理层不可行（K18/K19）。"
    "其余「协变改写」是把教科书式子换记号，IDN ⇒ 不得计为新增物理")

# ============================================================== 控制组 CT 组
# 控制组必须能红：人为变异后，对应判据必须报 FAIL，否则判定器不灵。
_k_mut = H1.r * H1.w ** 2 / H1.c_geom ** 3          # 变异：κ 的 c 幂次写错
rec("CT1", "控制组·κ 的 c 幂次变异 ⇒ 曲率判据必须转红", "DEF",
    "PASS" if rel(_k_mut, kappa_fd(H1, TS, HS)) > Decimal("1e-10") else "FAIL",
    "变异值 " + fs(_k_mut) + "，数值真值 " + fs(kappa_fd(H1, TS, HS))
    + "，相对差 " + fs(rel(_k_mut, kappa_fd(H1, TS, HS))))

_t_mut = H1.h * H1.w / H1.c_geom                   # 变异：τ 的定义少一个 c
rec("CT2", "控制组·τ 定义少一个 c ⇒ 挠率判据必须转红", "DEF",
    "PASS" if rel(_t_mut, tau_fd(H1, TS, HS)) > Decimal("1e-10") else "FAIL",
    "变异值 " + fs(_t_mut) + "，数值真值 " + fs(tau_fd(H1, TS, HS))
    + "，相对差 " + fs(rel(_t_mut, tau_fd(H1, TS, HS))))

_n3 = EPS0_N * (MU0_N * 10) * C_LIGHT * C_LIGHT
rec("CT3", "控制组·μ0 ×10 ⇒ ε0μ0c^2 = 1 判据必须转红", "DEF",
    "PASS" if abs(_n3 - Decimal(1)) > Decimal("1e-6") else "FAIL",
    "变异值 " + fs(_n3) + "，相对偏离 " + fs(abs(_n3 - Decimal(1))))

# ============================================================== 汇总与落盘
from collections import Counter  # noqa: E402

_counts0 = Counter(r["verdict"] for r in RESULTS)
_n0_total = len(RESULTS)
_n0_sum = (_counts0.get("PASS", 0) + _counts0.get("FAIL", 0) + _counts0.get("IDN", 0)
           + _counts0.get("BOUNDARY", 0) + _counts0.get("INFO", 0))
rec("G07", "守卫·统计守恒（条目数与分类计数一致）", "DEF",
    "PASS" if _n0_total == _n0_sum else "FAIL",
    "收尾前总条目 " + str(_n0_total) + "，分类求和 " + str(_n0_sum))

_counts = Counter(r["verdict"] for r in RESULTS)
_n_pass = _counts.get("PASS", 0)
_n_fail = _counts.get("FAIL", 0)
_n_idn = _counts.get("IDN", 0)
_n_bnd = _counts.get("BOUNDARY", 0)
_n_info = _counts.get("INFO", 0)
_n_total = len(RESULTS)

_instrument = [r for r in RESULTS
               if (r["id"].startswith("G") or r["id"].startswith("CT")) and r["verdict"] != "PASS"]
_content = [r for r in RESULTS
            if r["verdict"] == "FAIL" and not (r["id"].startswith("G") or r["id"].startswith("CT"))]

_summary = {
    "total": len(RESULTS),
    "PASS": _counts.get("PASS", 0),
    "FAIL": _counts.get("FAIL", 0),
    "IDN": _counts.get("IDN", 0),
    "BOUNDARY": _counts.get("BOUNDARY", 0),
    "INFO": _counts.get("INFO", 0),
    "content_failures": [r["id"] for r in _content],
    "instrument_failures": [r["id"] for r in _instrument],
}

_payload = {
    "meta": {
        "script": "74_helix_covariant_audit.py",
        "volume": "74_螺旋本源体系原版审计_修复优化_原创协变大统一方程组.tex",
        "precision": "decimal 60 位 + Fraction 四元量纲 (M,L,T,I)",
        "dependencies": "纯标准库",
        "scope": "数学恒等 / 量纲自洽 / 常数算术；不判物理真伪",
    },
    "summary": _summary,
    "entries": RESULTS,
}

with io.open(OUT_JSON, "w", encoding="utf-8") as fh:
    fh.write(json.dumps(_payload, ensure_ascii=False, indent=2))

_lines = []
_lines.append("74 号仪器 · 螺旋本源体系原版「协变大统一方程组」全维审计 · 机读产物")
_lines.append("=" * 78)
_lines.append("条目 {total}：PASS {PASS} / FAIL {FAIL} / IDN {IDN} / BOUNDARY {BOUNDARY} / INFO {INFO}"
              .format(**_summary))
_lines.append("内容层 FAIL（原版缺陷）：" + (", ".join(_summary["content_failures"]) or "无"))
_lines.append("仪器层 FAIL（守卫/控制组）：" + (", ".join(_summary["instrument_failures"]) or "无"))
_lines.append("-" * 78)
for r in RESULTS:
    _lines.append("[{v}] {i} ({k}) {t}".format(v=r["verdict"], i=r["id"], k=r["kind"], t=r["title"]))
    _lines.append("      " + r["detail"])
_lines.append("=" * 78)
_lines.append("红线：量纲自洽 ≠ 物理成立；恒等式标 IDN（零预测力）；原版缺陷记 FAIL 属本卷结论。")

with io.open(OUT_TXT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(_lines) + "\n")

if not QUIET:
    print("\n".join(_lines))

if _instrument:
    sys.exit(2)
if _content:
    sys.exit(1)
sys.exit(0)
