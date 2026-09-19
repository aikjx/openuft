# -*- coding: utf-8 -*-
"""
4D 世界线的广义 Frenet 曲率校验 (Gram 行列式法, 数值最稳定)
核心问题: 除了曲率(kappa1)与挠率(kappa2), 是否还有第三个几何不变量?

方法: 用 Gram 行列式公式 (框架无关, 无标架翻转问题):
    对弧长参数 s, 记 G_k 为前 k 阶导数 {r^(1),...,r^(k)} 的 Gram 矩阵, 则
        kappa_k = sqrt(det G_{k+1}) / det G_k          (k = 1,2,3,...)
  该式对 n 维曲线严格成立, 不需要任何标架。4D 世界线 => 3 个曲率。
结论: 4D 世界线有第 3 个不变量 kappa3(第二挠率); 纯 3D 螺旋 kappa3 精确退化为 0。
"""
import numpy as np
import sympy as sp

t = sp.symbols("t", real=True)


def build_curve(a):
    Rv, w, h, W = sp.Float(1.0), sp.Integer(2), sp.Rational(1, 2), sp.Rational(17, 10)
    r = sp.Matrix([Rv * sp.cos(w * t), Rv * sp.sin(w * t), h * t,
                   (0 * t) if float(a) == 0.0 else a * sp.sin(W * t)])
    f = [sp.lambdify(t, comp, "numpy") for comp in r]
    d = [[sp.lambdify(t, comp.diff(t, k), "numpy") for comp in r] for k in range(1, 5)]
    return f, d


def generalized_curvatures(curve_fns, t_grid):
    f, d = curve_fns
    ev = lambda fn: np.broadcast_to(np.asarray(fn(t_grid), dtype=float), t_grid.shape)
    # 1) 位置 -> 弧长参数化 -> 升采样到均匀弧长 s
    pos = np.stack([ev(fn) for fn in f], axis=1)                  # N x 4
    vel = np.gradient(pos, t_grid[1] - t_grid[0], axis=0)         # dr/dt
    speed = np.linalg.norm(vel, axis=1)
    dt = t_grid[1] - t_grid[0]
    s = np.concatenate([[0.0], np.cumsum((speed[:-1] + speed[1:]) / 2 * dt)])
    s_tgt = np.linspace(s[0], s[-1], len(t_grid))
    pos_s = np.stack([np.interp(s_tgt, s, pos[:, k]) for k in range(4)], axis=1)
    ds = s_tgt[1] - s_tgt[0]
    # 2) 对弧长逐次求导
    D = [pos_s]
    for _ in range(4):
        D.append(np.gradient(D[-1], ds, axis=0))                  # d^k r / ds^k
    D = D[1:]                                                     # 去掉位置, 留 4 个导数
    Ne = len(s_tgt)
    kap = np.zeros((Ne, 3))
    for i in range(Ne):
        vecs = [D[k][i] for k in range(4)]
        G = np.array([[float(np.dot(vecs[a], vecs[b])) for a in range(4)] for b in range(4)])
        d1 = float(np.linalg.det(G[:1, :1]))
        d2 = float(np.linalg.det(G[:2, :2]))
        d3 = float(np.linalg.det(G[:3, :3]))
        d4 = float(np.linalg.det(G[:4, :4]))
        kap[i, 0] = np.sqrt(max(d2, 0.0)) / d1 if d1 > 1e-15 else 0.0
        kap[i, 1] = np.sqrt(max(d3, 0.0)) / d2 if d2 > 1e-15 else 0.0
        kap[i, 2] = np.sqrt(max(d4, 0.0)) / d3 if d3 > 1e-15 else 0.0
    return kap


def report(label, a, expect):
    t_grid = np.linspace(0, 6 * np.pi, 8000)
    kap = generalized_curvatures(build_curve(a), t_grid)
    lo, hi = 400, -400
    k1 = float(np.abs(kap[lo:hi, 0]).mean())
    k2 = float(np.abs(kap[lo:hi, 1]).mean())
    k3 = float(np.abs(kap[lo:hi, 2]).mean())
    print("[%s] a=%.2f" % (label, float(a)))
    print("   kappa1(曲率) ~ %.6e  (理论 %.4f)" % (k1, expect[0]))
    print("   kappa2(挠率) ~ %.6e  (理论 %.4f)" % (k2, expect[1]))
    print("   kappa3(第三) ~ %.6e  %s" % (k3,
          "<-- 非零: 存在第三个不变量!" if k3 > 1e-4 else "(纯3D子空间, 精确退化为0)"))


print("===== 4D 广义曲率 (嵌入维 n=4 => n-1 = 3 个曲率, Gram 行列式法) =====")
# 纯3D螺旋理论: c^2=R^2 w^2+h^2=4.25, c=2.0616; k1=R w^2/c^2=4/4.25=0.9412; k2=h w/c^2=1/4.25=0.2353; k3=0
report("纯3D螺旋(无第四维扰动)", 0.0, (0.9412, 0.2353))
# 4D世界线: k1,k2 近似不变, k3 应非零
report("4D世界线(含第四维扰动)", 0.30, (0.94, 0.24))
print("\n标准定理: R^n 中曲线由 n-1 个广义曲率唯一确定; 4D 世界线 => kappa1,kappa2,kappa3.")
print("原文档(曲率挠率.md v2) 用 3D Frenet 描述 4D 世界线, 遗漏 kappa3; 见补篇")
print("《曲率挠率之外_全维度几何不变量分析.md》. 联络层另缺非度规性 Q (几何三一 R/T/Q).")
