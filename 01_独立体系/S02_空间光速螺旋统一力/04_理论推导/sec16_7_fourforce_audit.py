# -*- coding: utf-8 -*-
"""§16.7 四力定义审计（算法联盟 · 符号核验）

审计对象：§16.7「场对螺旋世界线粒子的4力」提议 f^μ = u_ν ∇_α T^{αμ}|_{worldline}，
          并声称可由纯几何（无电荷）耦合驱动螺旋世界线的 κ、τ 演化。

待核验命题：
  (A) 真空（无源）Maxwell 场满足 ∇_α T^{αμ} ≡ 0
      ⇒ 任何形如 (∇·T) 投影的"力"恒为零 ⇒ 中性测试粒子不受力；
  (B) §16.7 把 ∇_α T^{αμ} 写成 F^{ασ}∇_α F^μ_σ，**丢掉** -(1/4)∇^μ(F_{ρσ}F^{ρσ}) 迹项，
     正是该省略制造了非零"四力"；
  (C) 恒等式 P^μ ≡ F^{ασ}∇_α F^μ_σ = (1/4)∇^μ(F_{ρσ}F^{ρσ}) ≡ Q^μ，故 P^μ - Q^μ ≡ 0。

测试场：两束【不同方向】平面波叠加（线性性 ⇒ 仍是严格真空解；且 F_{ρσ}F^{ρσ}
       随位置振荡 ⇒ P^μ、Q^μ 各自非零），避免"平凡全零"掩盖问题。
       方向取 3-4-5 有理方向，保证符号化简可达机器精确。

符号约定：η=diag(1,-1,-1,-1)，x^μ=(t,x,y,z)，采用 §16.7 自己的 T 定义以保证针对性。
"""
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import sympy as sp

t, x, y, z = sp.symbols('t x y z', real=True)
X = [t, x, y, z]
eta = sp.diag(1, -1, -1, -1)          # η_{μν}
eta_inv = eta.inv()                    # η^{μν}

OK = "[OK]"
BAD = "[!!]"

# 数值采样点，用于给出机器精度量级的残差
PTS = [{t: sp.Rational(3, 10), x: sp.Rational(-7, 10), y: sp.Rational(11, 10), z: sp.Rational(2, 5)},
       {t: sp.Rational(17, 10), x: sp.Rational(9, 10), y: sp.Rational(-1, 5), z: sp.Rational(23, 10)},
       {t: sp.Rational(-6, 5), x: sp.Rational(5, 2), y: sp.Rational(3, 5), z: sp.Rational(-4, 5)}]


def report(label, exprs):
    """精确化简 + 多点数值残差。返回 (是否恒零, 数值最大残差)"""
    simp = [sp.simplify(e) for e in exprs]
    is_zero = all(s == 0 for s in simp)          # 结构精确零
    nmax = 0.0
    for pt in PTS:
        for s in simp:
            nmax = max(nmax, abs(complex(sp.N(s.subs(pt)))))
    print(f"    {label}")
    print(f"        精确恒零: {'是' if is_zero else '否'}")
    print(f"        多点数值最大残差: {nmax:.3e}")
    return is_zero, nmax, simp


def make_plane_wave(name, omega, k_spatial, pol_up):
    """返回协变 A_μ。要求 |k|=omega（零波矢）且 k·ε=0（横向偏振）。"""
    k_up = sp.Matrix([omega] + list(k_spatial))
    pol = sp.Matrix(pol_up)
    ksq = sp.simplify((k_up.T * eta * k_up)[0])
    kdotpol = sp.simplify((k_up.T * eta * pol)[0])
    print(f"    {name}: k^2={ksq}（应0）, k.eps={kdotpol}（应0）"
          f"  {OK if ksq == 0 and kdotpol == 0 else BAD}")
    k_low = eta * k_up
    xi = sum(k_low[i] * X[i] for i in range(4))
    pol_low = eta * pol
    return [pol_low[i] * sp.sin(xi) for i in range(4)]


def raise_both(F_low):
    return sp.Matrix(4, 4, lambda m, n: sum(
        eta_inv[m, a] * eta_inv[n, b] * F_low[a, b] for a in range(4) for b in range(4)))


def mixed(F_low):
    Fup = raise_both(F_low)
    return sp.Matrix(4, 4, lambda m, s: sum(Fup[m, b] * eta[b, s] for b in range(4)))


def main():
    print("=" * 78)
    print("§16.7 四力定义审计 · 符号核验（sympy 精确化简）")
    print("=" * 78)

    # ---------- 构造测试场 ----------
    print("\n[0] 构造真空测试场：两束不同方向平面波叠加")
    A1 = make_plane_wave("波A k=(0,0,1)", 1, [0, 0, 1], [0, 1, 0, 0])
    # 波B 方向 (3/5,0,4/5)；偏振须 ⊥ k_B 且【与ε_A不正交】，使交叉项 F1·F2≠0
    #   ε_B ∝ (4,0,-3)/5  ⟹ k_B·ε_B = 3/5·4/5 + 4/5·(-3/5) = 0 ✓
    #   ε_A·ε_B = -4/5 ≠ 0 ⟹ F_{ab}F^{ab} 含随位置振荡的交叉项
    A2 = make_plane_wave("波B k=(3/5,0,4/5)", 1,
                         [sp.Rational(3, 5), 0, sp.Rational(4, 5)],
                         [0, sp.Rational(4, 5), 0, sp.Rational(-3, 5)])
    A_low = [sp.simplify(A1[i] + A2[i]) for i in range(4)]

    F_low = sp.Matrix(4, 4, lambda m, n: sp.simplify(
        sp.diff(A_low[n], X[m]) - sp.diff(A_low[m], X[n])))
    F_up = raise_both(F_low)
    F_mix = mixed(F_low)

    # ---------- [1] Maxwell 无源方程 ----------
    print("\n[1] 无源 Maxwell 方程  ∂_alpha F^{alpha mu} = 0")
    maxwell = [sp.simplify(sum(sp.diff(F_up[m, n], X[m]) for m in range(4)))
               for n in range(4)]
    mx_zero, mx_res, _ = report("  ∂_alpha F^{alpha mu}", maxwell)
    print(f"    >>> {OK} 测试场确为严格真空解" if mx_zero else f"    >>> {BAD} 非真空解")

    # ---------- [2] 不变量随位置变化 ----------
    print("\n[2] 不变量 F_{ab}F^{ab}（确保测试非平凡）")
    FF = sp.simplify(sum(F_low[a, b] * F_up[a, b] for a in range(4) for b in range(4)))
    varies = any(sp.simplify(sp.diff(FF, X[m])) != 0 for m in range(4))
    print(f"    F_{{ab}}F^{{ab}} = {FF}")
    print(f"    >>> 随位置变化: {'是（非平凡）' if varies else '否'}")
    if not varies:
        print("    [!] 测试场退化为平凡情形，结论说服力下降。")

    # ---------- [3] 完整散度（含迹项）----------
    print("\n[3] 完整散度  ∇_alpha T^{alpha mu}（严格按 §16.7 自己的 T 定义，含迹项）")
    T_up = sp.Matrix(4, 4, lambda m, n: sp.simplify(
        sum(F_up[m, s] * F_mix[n, s] for s in range(4))
        - sp.Rational(1, 4) * eta_inv[m, n] * FF))
    divT = [sp.simplify(sum(sp.diff(T_up[m, n], X[m]) for m in range(4)))
            for n in range(4)]
    _, dmax, dsimp = report("  ∇_alpha T^{alpha mu}", divT)
    divT_zero = all(s == 0 for s in dsimp)
    print(f"    >>> {OK} 严格为零：真空场动量守恒" if divT_zero else f"    >>> {BAD} 非零")

    # ---------- [4] 拆分核验 ----------
    print("\n[4] 关键拆分核验")
    P = [sp.simplify(sum(F_up[a, s] * sp.diff(F_mix[n, s], X[a])
                         for a in range(4) for s in range(4)))
         for n in range(4)]
    Q = [sp.simplify(sp.Rational(1, 4) * sum(eta_inv[n, m] * sp.diff(FF, X[m])
                                             for m in range(4)))
         for n in range(4)]
    _, pmax, psimp = report("  P^mu = F^{as}∇_a F^mu_s   （§16.7 保留的项）", P)
    _, qmax, qsimp = report("  Q^mu = (1/4)∇^mu(F_rs F^rs) （§16.7 丢弃的迹项）", Q)
    _, dmax2, dsimp2 = report("  P^mu - Q^mu", [P[n] - Q[n] for n in range(4)])
    P_zero = all(s == 0 for s in psimp)
    PQ_zero = all(s == 0 for s in dsimp2)

    # ---------- 结论 ----------
    print("\n" + "=" * 78)
    print("审计结论")
    print("=" * 78)
    if divT_zero:
        print(f"{OK} [A] 完整 ∇_alpha T^{{alpha mu}} ≡ 0 严格成立。")
        print("        ⇒ 任何 (∇·T) 投影构成的'四力'【恒等于零】：")
        print("          真空 Maxwell 场不可能通过该机制对中性粒子施力。")
    if PQ_zero and not P_zero:
        print(f"{OK} [B] 恒等式 P^mu ≡ Q^mu 成立，且二者各自【非零】。")
        print("        ⇒ §16.7 取 ∇_alpha T^{alpha mu} = P^mu 而丢弃 Q^mu，")
        print("          所得非零'四力'完全等价于被丢弃的迹项 ⇒ 代数疏漏产物。")
    print(f"{OK} [C] 独立的指标结构错误：")
    print("        f^mu = u_nu ∇_a T^{a mu} 中 ∇_a T^{a mu} 自由指标为 mu，")
    print("        乘 u_nu 后自由指标为 (mu,nu) ⇒ 结果是二阶张量而非四矢量；")
    print("        且 u_ν 的 nu 在 T^{a mu} 中无对应指标，缩并不合法。")
    print("\n⇒ §16.7 的几何耦合机制在真空 Maxwell 框架内【不成立】；")
    print("  在其上做 κ-τ-l 网格扫描只会得到数值噪声，不建议执行。")
    print("=" * 78)


if __name__ == "__main__":
    main()
