# -*- coding: utf-8 -*-
"""
TUFT 卷二十：背景场 Hessian 的二阶变分机器求导
—— 平坦 / 极大对称（S^d 共形）背景的精确二次作用量、爱因斯坦背景条件、
   以及阈值宗量系数 a 的【推导】

承接卷十九（York 分解 / 鬼场模计数 / NGFP 的系数无关结构定理）。

方法与纪律：
  (1) 全部用显式指标展开符号推导（不用任何文献 Hessian 公式），展开到 h 二次、二阶导数；
  (2) 每一步用独立的蛮力计算复核：对完整度规直接算 Christoffel / Ricci / R
      （数值 + 解析导数），把 S(eps) 对 eps 做级数提取，与符号二次作用量比对；
  (3) 不引用未经复算的系数。

红线：数学自洽 != 实验证实。
"""

import os
import sys
import json
import time

import numpy as np
import sympy as sp

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUTDIR = os.path.join(ROOT, "09_验证结果", "原始运行记录")
os.makedirs(OUTDIR, exist_ok=True)
REPORT_PATH = os.path.join(OUTDIR, "tuft_卷二十_Hessian二阶变分机器求导_report.txt")
JSON_PATH = os.path.join(OUTDIR, "tuft_卷二十_Hessian二阶变分机器求导.json")

T0 = time.time()
LINES = []
COUNTS = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0, "OPEN": 0}
ITEMS = []


def _emit(s=""):
    LINES.append(s)
    print(s, flush=True)


def chunk(title):
    _emit("")
    _emit("=" * 78)
    _emit(" " + title)
    _emit("=" * 78)


def note(s=""):
    _emit(s)


def verdict(code, status, text):
    COUNTS[status] = COUNTS.get(status, 0) + 1
    ITEMS.append((code, status, text))
    pad = " " * (8 - len(status))
    _emit("  [" + status + pad + "] " + code + ": " + text)


def fs(x, p=6):
    return ("%." + str(p) + "g") % float(x)


def qc(expr):
    return Q({(): sp.sympify(expr)})


class Q(object):
    """次数 <= 2 的多项式，变量是 atom = (field_id, deriv_tuple)。"""

    __slots__ = ("t",)

    def __init__(self, t=None):
        self.t = {} if t is None else t

    def add(self, o):
        r = dict(self.t)
        for k, v in o.t.items():
            nv = r.get(k, 0) + v
            if nv == 0:
                r.pop(k, None)
            else:
                r[k] = nv
        return Q(r)

    def scale(self, c):
        c = sp.sympify(c)
        if c == 0:
            return Q({})
        return Q(dict((k, v * c) for k, v in self.t.items()))

    def mul(self, o):
        r = {}
        for k1, v1 in self.t.items():
            for k2, v2 in o.t.items():
                k = tuple(sorted(k1 + k2))
                if len(k) > 2:
                    continue
                nv = r.get(k, 0) + v1 * v2
                if nv != 0:
                    r[k] = nv
                elif k in r:
                    del r[k]
        return Q(r)

    def diff(self, mu):
        r = {}
        for k, v in self.t.items():
            for i in range(len(k)):
                fid, dv = k[i]
                nd = tuple(sorted(dv + (mu,)))
                nk = tuple(sorted(k[:i] + ((fid, nd),) + k[i + 1:]))
                r[nk] = r.get(nk, 0) + v
        return Q(dict((k, v) for k, v in r.items() if v != 0))


# ============================================================ Hessian 构造器
class Hess(object):
    def __init__(self, d, sphere, lam):
        self.d = d
        self.sphere = sphere
        self.lam = sp.sympify(lam)
        self.xs = sp.symbols("x0:%d" % d)
        r2 = sum(xi ** 2 for xi in self.xs)
        if sphere:
            self.Om = 2 / (1 + r2)
            self.f = sp.log(2) - sp.log(1 + r2)
        else:
            self.Om = sp.Integer(1)
            self.f = sp.Integer(0)
        self.df = [sp.diff(self.f, xi) for xi in self.xs]
        self.ddf = [[sp.diff(self.df[i], self.xs[j]) for j in range(d)]
                    for i in range(d)]
        self.fid_of = {}
        self.fields = []
        for mu in range(d):
            for nu in range(mu, d):
                self.fid_of[(mu, nu)] = len(self.fields)
                self.fields.append((mu, nu))

    def fid(self, mu, nu):
        return self.fid_of[(min(mu, nu), max(mu, nu))]

    def H(self, mu, nu):
        return Q({((self.fid(mu, nu), ()),): sp.Integer(1)})

    def trH(self):
        s = Q({})
        for mu in range(self.d):
            s = s.add(self.H(mu, mu))
        return s

    def trH2(self):
        d = self.d
        s = Q({})
        for mu in range(d):
            for be in range(d):
                s = s.add(self.H(mu, be).mul(self.H(be, mu)))
        return s

    def sqrtg1(self):
        return self.trH().scale(sp.Rational(1, 2))

    def sqrtg2(self):
        return (self.trH().mul(self.trH()).scale(sp.Rational(1, 8))
                .add(self.trH2().scale(sp.Rational(-1, 4))))

    def Gam1(self, lam, mu, nu):
        return (self.H(lam, nu).diff(mu)
                .add(self.H(lam, mu).diff(nu))
                .add(self.H(mu, nu).diff(lam).scale(-1))).scale(sp.Rational(1, 2))

    def Gam2(self, lam, mu, nu):
        d = self.d
        s = Q({})
        for rho in range(d):
            inner = (self.H(nu, rho).diff(mu)
                     .add(self.H(mu, rho).diff(nu))
                     .add(self.H(mu, nu).diff(rho).scale(-1)))
            s = s.add(self.H(lam, rho).mul(inner))
        return s.scale(sp.Rational(-1, 2))

    def R1(self, mu, nu):
        d = self.d
        s = Q({})
        for lam in range(d):
            s = s.add(self.Gam1(lam, mu, nu).diff(lam))
            s = s.add(self.Gam1(lam, mu, lam).diff(nu).scale(-1))
        return s

    def R2(self, mu, nu):
        d = self.d
        s = Q({})
        for lam in range(d):
            s = s.add(self.Gam2(lam, mu, nu).diff(lam))
            s = s.add(self.Gam2(lam, mu, lam).diff(nu).scale(-1))
        for lam in range(d):
            for sg in range(d):
                s = s.add(self.Gam1(lam, lam, sg).mul(self.Gam1(sg, mu, nu)))
                s = s.add(self.Gam1(lam, nu, sg).mul(self.Gam1(sg, mu, lam)).scale(-1))
        return s

    def R_scalar1(self):
        s = Q({})
        for mu in range(self.d):
            s = s.add(self.R1(mu, mu))
        return s

    def R_scalar2(self):
        d = self.d
        s = Q({})
        for mu in range(d):
            s = s.add(self.R2(mu, mu))
        for mu in range(d):
            for nu in range(d):
                s = s.add(self.H(mu, nu).mul(self.R1(mu, nu)).scale(-1))
        return s

    def B0(self):
        s = sp.Integer(0)
        for mu in range(self.d):
            s = s + self.ddf[mu][mu]
        return s

    def C0(self):
        s = sp.Integer(0)
        for mu in range(self.d):
            s = s + self.df[mu] * self.df[mu]
        return s

    def B1(self):
        d = self.d
        s = Q({})
        for mu in range(d):
            for nu in range(d):
                s = s.add(self.H(mu, nu).scale(-self.ddf[mu][nu]))
        for mu in range(d):
            for nu in range(d):
                for lam in range(d):
                    s = s.add(self.Gam1(lam, mu, nu).scale(-self.df[lam]))
        return s

    def B2(self):
        d = self.d
        s = Q({})
        for mu in range(d):
            for nu in range(d):
                for be in range(d):
                    s = s.add(self.H(mu, be).mul(self.H(be, nu)).scale(self.ddf[mu][nu]))
        for mu in range(d):
            for nu in range(d):
                for lam in range(d):
                    s = s.add(self.H(mu, nu).mul(self.Gam1(lam, mu, nu)).scale(self.df[lam]))
        for mu in range(d):
            for lam in range(d):
                s = s.add(self.Gam2(lam, mu, mu).scale(-self.df[lam]))
        return s

    def C1(self):
        d = self.d
        s = Q({})
        for mu in range(d):
            for nu in range(d):
                s = s.add(self.H(mu, nu).scale(-self.df[mu] * self.df[nu]))
        return s

    def C2(self):
        d = self.d
        s = Q({})
        for mu in range(d):
            for nu in range(d):
                for be in range(d):
                    s = s.add(self.H(mu, be).mul(self.H(be, nu)).scale(
                        self.df[mu] * self.df[nu]))
        return s

    def _X(self, order):
        d = self.d
        c1 = -2 * (d - 1)
        c2 = -(d - 1) * (d - 2)
        if order == 1:
            return (self.R_scalar1().add(self.B1().scale(c1))
                    .add(self.C1().scale(c2)))
        if order == 2:
            return (self.R_scalar2().add(self.B2().scale(c1))
                    .add(self.C2().scale(c2)))
        return qc(self.B0() * c1 + self.C0() * c2)

    def build(self):
        d = self.d
        w = -self.Om ** (d - 2)
        lamfac = 2 * self.lam * self.Om ** d
        L1 = (self.sqrtg1().scale(lamfac)
              .add(self._X(1).add(self.sqrtg1().mul(self._X(0))).scale(w)))
        L2 = (self.sqrtg2().scale(lamfac)
              .add(self._X(2)
                   .add(self.sqrtg1().mul(self._X(1)))
                   .add(self.sqrtg2().mul(self._X(0)))
                   .scale(w)))
        return L1, L2


# ============================================================ 数值蛮力
def brute_action(d, sphere, lam, amps, kvec, phase, eps, L=2.0, N=14):
    """完整度规 g = Om^2 (delta + eps H)，直接算 Christoffel / Ricci / R。"""
    xs = np.linspace(-L, L, N)
    mesh = np.meshgrid(*([xs] * d), indexing="ij")
    grid = mesh[0].shape
    r2 = sum(m ** 2 for m in mesh)
    if sphere:
        Om = 2.0 / (1.0 + r2)
        df = [-2.0 * mesh[mu] / (1.0 + r2) for mu in range(d)]
        dOm = [Om * df[mu] for mu in range(d)]
        ddOm = np.zeros(grid + (d, d))
        for mu in range(d):
            for nu in range(d):
                ddOm[..., mu, nu] = (Om * (-2.0 * (1.0 if mu == nu else 0.0)
                                          / (1.0 + r2)
                                          + 4.0 * mesh[mu] * mesh[nu]
                                          / (1.0 + r2) ** 2)
                                     + dOm[mu] * df[nu])
    else:
        Om = np.ones(grid)
        dOm = [np.zeros(grid) for _ in range(d)]
        ddOm = np.zeros(grid + (d, d))

    kx = sum(kvec[mu] * mesh[mu] for mu in range(d))
    ang = kx + phase
    c = np.cos(ang)
    s = np.sin(ang)
    H = np.zeros(grid + (d, d))
    dH = np.zeros(grid + (d, d, d))
    ddH = np.zeros(grid + (d, d, d, d))
    for mu in range(d):
        for nu in range(d):
            a = amps[mu][nu]
            H[..., mu, nu] = a * c
            for rho in range(d):
                dH[..., rho, mu, nu] = -a * kvec[rho] * s
                for sg in range(d):
                    ddH[..., sg, rho, mu, nu] = -a * kvec[sg] * kvec[rho] * c

    g = np.zeros(grid + (d, d))
    dg = np.zeros(grid + (d, d, d))
    ddg = np.zeros(grid + (d, d, d, d))
    for mu in range(d):
        for nu in range(d):
            base = (1.0 if mu == nu else 0.0) + eps * H[..., mu, nu]
            g[..., mu, nu] = Om ** 2 * base
            for rho in range(d):
                dg[..., rho, mu, nu] = (2.0 * Om * dOm[rho] * base
                                        + Om ** 2 * eps * dH[..., rho, mu, nu])
                for sg in range(d):
                    ddg[..., sg, rho, mu, nu] = (
                        (2.0 * dOm[sg] * dOm[rho] + 2.0 * Om * ddOm[..., sg, rho]) * base
                        + 2.0 * Om * dOm[sg] * eps * dH[..., rho, mu, nu]
                        + 2.0 * Om * dOm[rho] * eps * dH[..., sg, mu, nu]
                        + Om ** 2 * eps * ddH[..., sg, rho, mu, nu])

    ginv = np.linalg.inv(g)
    detg = np.linalg.det(g)
    sqrtg = np.sqrt(np.abs(detg)) * np.sign(detg)

    Gam = np.zeros(grid + (d, d, d))
    for lam in range(d):
        for mu in range(d):
            for nu in range(d):
                acc = np.zeros(grid)
                for sg in range(d):
                    acc = acc + ginv[..., lam, sg] * (
                        dg[..., mu, nu, sg] + dg[..., nu, mu, sg] - dg[..., sg, mu, nu])
                Gam[..., lam, mu, nu] = 0.5 * acc

    dginv = np.zeros(grid + (d, d, d))
    for lam in range(d):
        for mu in range(d):
            for nu in range(d):
                acc = np.zeros(grid)
                for a in range(d):
                    for b in range(d):
                        acc = acc - (ginv[..., mu, a] * dg[..., lam, a, b]
                                     * ginv[..., b, nu])
                dginv[..., lam, mu, nu] = acc

    dGam = np.zeros(grid + (d, d, d))
    for lam in range(d):
        for mu in range(d):
            for nu in range(d):
                acc = np.zeros(grid)
                for sg in range(d):
                    acc = acc + dginv[..., lam, lam, sg] * (
                        dg[..., mu, nu, sg] + dg[..., nu, mu, sg] - dg[..., sg, mu, nu])
                    acc = acc + ginv[..., lam, sg] * (
                        ddg[..., lam, mu, nu, sg] + ddg[..., lam, nu, mu, sg]
                        - ddg[..., lam, sg, mu, nu])
                dGam[..., lam, mu, nu] = 0.5 * acc

    Ric = np.zeros(grid + (d, d))
    for mu in range(d):
        for nu in range(d):
            acc = np.zeros(grid)
            for lam in range(d):
                acc = acc + dGam[..., lam, mu, nu] - dGam[..., nu, mu, lam]
            for lam in range(d):
                for sg in range(d):
                    acc = acc + (Gam[..., lam, lam, sg] * Gam[..., sg, mu, nu]
                                 - Gam[..., lam, nu, sg] * Gam[..., sg, mu, lam])
            Ric[..., mu, nu] = acc

    Rsc = np.zeros(grid)
    for mu in range(d):
        for nu in range(d):
            Rsc = Rsc + ginv[..., mu, nu] * Ric[..., mu, nu]

    Ldens = sqrtg * (2.0 * lam - Rsc)
    return float(np.mean(Ldens) * (2.0 * L) ** d)


def extract_S2(fn, h=0.01):
    """中心二阶差 + 两级 Richardson，返回 S''(0)/2 = S_2。"""
    f0 = fn(0.0)

    def D(hh):
        return (fn(hh) - 2.0 * f0 + fn(-hh)) / (hh * hh)

    d1 = D(h)
    d2 = D(h / 2)
    d3 = D(h / 4)
    return ((4.0 * d3 - d2) / 3.0) / 2.0, ((4.0 * d2 - d1) / 3.0) / 2.0
