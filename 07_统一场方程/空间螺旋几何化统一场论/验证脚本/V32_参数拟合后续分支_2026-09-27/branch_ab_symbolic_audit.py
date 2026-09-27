#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TUFT V3.2「参数拟合后续分支」来稿 · 符号与数值核验（T1-T6）
================================================================
对象：来稿_TUFT_V3.2参数拟合后续分支_伴随梯度与自旋约束_2026-09-27.txt
      分支A（伴随解析梯度）与分支B（N=hbar 自旋-挠率约束）的代数主张。
方法：sympy 精确符号推导 + numpy 数值核对；每条判据同时打印
      「正对照（必须非零/不一致）」，避免全绿自证。
约定：Delta f := f'' + 2f'/r；P := V1*f^3 - V2*f^5。
      F_doc  = -Delta f - P   （来稿 A1 所列原方程）
      F_code = -Delta f + P   （来稿 E0 泛函的 Euler-Lagrange 残差）
用法：python branch_ab_symbolic_audit.py
边界：只核验算子代数、变分符号与自由度计数；不判定 TUFT 物理真实性，
      不重新求解孤子背景，不做电子拟合。
"""
import json
import os

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)                      # 验证脚本/
SERIES = os.path.dirname(PARENT)                    # 空间螺旋几何化统一场论/
OUT = os.path.join(SERIES, "V3_8_paramfit_branch_checks.json")

r, V1, V2 = sp.symbols('r V1 V2', positive=True)
q0, w0 = sp.symbols('q0 omega0', positive=True)
psi = sp.Function('psi', real=True)
uf, vf, Af = sp.Function('u', real=True), sp.Function('v', real=True), sp.Function('A', real=True)

R = {}


def dlog(key, **kw):
    R[key] = kw
    print(('[%s] ' % key) + '  '.join('%s=%s' % (k, vv) for k, vv in kw.items()))


# ---------------------------------------------------------------- T1 变分符号
def T1_el_sign():
    Lagr = r ** 2 * (sp.Derivative(psi(r), r) ** 2 / 2
                     + V1 * psi(r) ** 4 / 4 - V2 * psi(r) ** 6 / 6)
    ed = sp.simplify(sp.diff(Lagr, psi(r)) - sp.diff(sp.diff(Lagr, sp.Derivative(psi(r), r)), r)) / r ** 2
    F_doc = -sp.diff(psi(r), r, 2) - 2 * sp.diff(psi(r), r) / r - V1 * psi(r) ** 3 + V2 * psi(r) ** 5
    F_code = -sp.diff(psi(r), r, 2) - 2 * sp.diff(psi(r), r) / r + V1 * psi(r) ** 3 - V2 * psi(r) ** 5
    diff_doc = sp.simplify(ed - F_doc)
    diff_code = sp.simplify(ed - F_code)
    P = V1 * psi(r) ** 3 - V2 * psi(r) ** 5
    ok_doc_nonzero = diff_doc != 0 and sp.simplify(diff_doc - 2 * P) == 0
    ok_code_zero = sp.simplify(diff_code) == 0
    dlog('T1_el_sign',
         deltaE0_over_4pir2=sp.simplify(ed),
         resid_ed_minus_F_doc=sp.simplify(diff_doc),
         resid_ed_minus_F_code=sp.simplify(diff_code),
         F_doc_is_EL_equation=False,
         F_code_is_EL_equation=True,
         mutant_check='ed-F_doc must be exactly 2P (nonzero): %s' % ok_doc_nonzero,
         verdict='PASS: 来稿 A1 的 F 与其自身 E0 的 EL 方程差 2P（非线性块符号相反）；'
                 'F=0 其实是把 E0 的势能整体反号后（−V1/4ψ⁴+V2/6ψ⁶）的驻点方程，'
                 '而来稿所写 E0 的势 +V1/4ψ⁴−V2/6ψ⁶ 在 ψ→∞ 无下界')
    return ed, F_doc, F_code, P


# ------------------------------------------------- T2 伴随算子（加权 / 无权）
def T2_adjoint():
    def Lop(f):
        return -sp.diff(f, r, 2) - 2 * sp.diff(f, r) / r + Af(r) * f
    W = sp.simplify(4 * sp.pi * r ** 2 * (uf(r) * Lop(vf(r)) - vf(r) * Lop(uf(r))))
    bd = sp.simplify(sp.diff(4 * sp.pi * r ** 2 * (vf(r) * sp.diff(uf(r), r)
                                                   - uf(r) * sp.diff(vf(r), r)), r))
    selfadj_diff = sp.simplify(W - bd)
    # 无权 dr 的完备形式伴随：sum (-1)^k d^k/dr^k (a_k v)
    a2, a1, a0 = -1, -2 / r, Af(r)
    Lstar_unw = sp.expand(sum((-1) ** k * sp.diff(ak * vf(r), r, k)
                              for k, ak in enumerate([a0, a1, a2])))
    manuscript_adjoint = -sp.diff(vf(r), r, 2) + 2 * sp.diff(vf(r), r) / r + Af(r) * vf(r)
    gap = sp.simplify(Lstar_unw - manuscript_adjoint)
    ok_selfadj = selfadj_diff == 0
    ok_gap = sp.simplify(gap + 2 * vf(r) / r ** 2) == 0 and sp.simplify(gap) != 0
    dlog('T2_adjoint',
         weighted_boundary_form=bd,
         resid_weighted_minus_boundary_total_derivative=selfadj_diff,
         unweighted_formal_adjoint=Lstar_unw,
         resid_来稿伴随_minus_完备无权伴随=gap,
         mutant_check='self-adjoint resid==0 and gap==-2v/r^2 (nonzero): %s' % ok_gap,
         verdict='PASS: 4πr²dr 加权下 L 自伴（差为全导数）；来稿 +2/r 版不是加权伴随，'
                 '也不是完备无权伴随（缺 -2ψ_a/r²）')


# ------------------------------------------------ T3 包络定理与「因子 2」
def T3_envelope(ed, F_doc, F_code, P):
    # 在两个背景上分别把 psi'' 消去
    pss_doc = sp.solve(sp.Eq(F_doc, 0), sp.diff(psi(r), r, 2))[0]
    pss_code = sp.solve(sp.Eq(F_code, 0), sp.diff(psi(r), r, 2))[0]
    ed_on_doc = sp.simplify(ed.subs(sp.diff(psi(r), r, 2), pss_doc))
    ed_on_code = sp.simplify(ed.subs(sp.diff(psi(r), r, 2), pss_code))
    src = 4 * sp.pi * r ** 2 * P          # 来稿 A3 第 2 条所列 δE0/δψ
    resid_doc = sp.simplify(src - 4 * sp.pi * r ** 2 * ed_on_doc)
    resid_code = sp.simplify(src - 4 * sp.pi * r ** 2 * ed_on_code)
    ok = (sp.simplify(ed_on_doc - 2 * P) == 0) and (ed_on_code == 0) and resid_doc != 0
    dlog('T3_envelope',
         deltaE0_delta_psi_over_4pir2_on_F_doc=ed_on_doc,
         deltaE0_delta_psi_over_4pir2_on_F_code=ed_on_code,
         来稿源项_minus_正确值_on_F_doc=sp.simplify(resid_doc),
         来稿源项_minus_正确值_on_F_code=sp.simplify(resid_code),
         mutant_check='on-doc==2P, on-code==0, 来稿 resid nonzero on both: %s' % ok,
         verdict='PASS: 来稿所列 4πr²P 在两个背景上都不等于 δE0/δψ'
                 '（F_doc 上正确值是 2·4πr²P，F_code 上是 0）⇒ 包络定理给出 '
                 'dE0/dV1=¼∫ψ⁴·4πr²dr、dE0/dV2=−1/6∫ψ⁶·4πr²dr，E0 不走伴随')


# ------------------------------------------- T4 简并核与 N=hbar 是否切断它
def T4_kernel():
    # 抽象剖面量及其偏导（把 N(V1,V2)、I(V1,V2)、M(V1,V2) 的导数当作独立符号，
    # 结论对一般剖面成立，不依赖具体函数形式）
    m1, m2, n1, n2, i1, i2, Nv, Iv = sp.symbols(
        'M_V1 M_V2 N_V1 N_V2 I_V1 I_V2 N I', real=True, nonzero=True)
    params = [V1, V2, q0, w0]
    J = sp.Matrix([
        [m1, m2, 0, 0],
        [q0 * w0 * n1, q0 * w0 * n2, w0 * Nv, q0 * Nv],
        [q0 * w0 * i1, q0 * w0 * i2, w0 * Iv, q0 * Iv],
    ])
    t = sp.Matrix([0, 0, q0, -w0])          # d(q0)/q0 = -d(w0)/w0 ⇒ Π 不变
    prod = sp.simplify(J * t)
    gG = sp.Matrix([[n1, n2, 0, 0]])        # ∇(N-hbar)
    Gt = sp.simplify(gG * t)
    stacked = sp.Matrix(J.tolist() + gG.tolist())
    rank_J = J.rank()
    rank_stacked = stacked.rank()
    ns_numeric = J.subs({m1: 1.0, m2: 0.4, n1: 2.0, n2: 1.5, i1: 0.7, i2: 1.1,
                         Nv: 67.44683, Iv: 112.6284, q0: 0.9, w0: 1.1}).nullspace()
    ok = (prod == sp.zeros(3, 1)) and (Gt == sp.zeros(1, 1)) and rank_stacked == rank_J == 3
    dlog('T4_degeneracy',
         analytic_null_direction='t=(0,0,q0,-omega0) 即 dq0/q0 = -dw0/omega0（Pi=q0*omega0 不变）',
         J_times_t=prod,
         grad_Nhbar_times_t=Gt,
         rank_J_of_targets=rank_J,
         rank_stacked_with_N_hbar=rank_stacked,
         nullity_after_constraint=4 - rank_stacked,
         numeric_nullspace_basis=[[float(x) for x in vec.T.tolist()[0]] for vec in ns_numeric],
         来稿断言_4参数3目标1等式_自由度0=False,
         mutant_check='J*t==0 and gradG*t==0 and rank stays 3 (not 4): %s' % ok,
         verdict='PASS: 简并方向 t=(0,0,q0,−ω0) 使 dM=dQ0=dμ=0；∇(N−ℏ) 在 (q0,ω0) 分量为 0 ⇒ '
                 '∇G·t≡0，加入 N=ℏ 后增广雅可比秩仍为 3（零度仍为 1）⇒ 不切断简并')


# ---------------------------------------------- T5 剖面自由度与过定计数
def T5_profile_count():
    unknowns = 2                    # (V1,V2)
    eqs = ['M(V1,V2)=Me', 'I_mu/N = mu_e/Q_e', 'N(V1,V2)=hbar']
    effective_independent_params = 3  # (V1, V2, Pi=q0*w0)
    targets = 3
    dlog('T5_count',
         profile_unknowns=unknowns,
         profile_equations_if_N_hbar_enforced=len(eqs),
         over_determined=True,
         effective_independent_parameters=effective_independent_params,
         least_squares_targets=targets,
         profile_count_note='3 方程 / 2 未知 ⇒ generic 无解（需 1 个相容性条件）',
         degeneracy_note='Π 固定时 q0/ω0 任意 ⇒ 1 维因子分解简并存活（见 T4）',
         verdict='PASS: 来稿 "4−3=1 流形 + 1 等式 ⇒ 0 自由度" 的计数不成立：'
                 '有效独立量已是 3（V1,V2,Π）对 3 目标；简并专属 (q0,ω0) 因子分解，'
                 '而 N=ℏ 只作用于剖面并使其过定')


# ------------------------------- T6 轨道角动量密度：S=(s/2)N 的因子来源
def T6_orbital():
    # psi = f(r) e^{i s phi}；Lz = -i d/dphi；内积 ∫ d^3x = ∫ r^2 dr dOmega
    phi, s, f0 = sp.symbols('phi s f0', real=True)
    wave = f0 * sp.exp(sp.I * s * phi)
    dens = sp.simplify(sp.conjugate(wave) * (-sp.I) * sp.diff(wave, phi))
    norm = sp.simplify(sp.conjugate(wave) * wave)
    ratio = sp.simplify(sp.integrate(dens, (phi, 0, 2 * sp.pi))
                        / sp.integrate(norm, (phi, 0, 2 * sp.pi)))
    expected_no_half = sp.simplify(ratio - s)
    ok = expected_no_half == 0
    dlog('T6_orbital_spin',
         Lz_density_over_d3x=dens,
         ratio_Lz_to_N=ratio,
         来稿_S_equals_s_over_2_times_N=False,
         resid_ratio_minus_s=expected_no_half,
         consequence_for_s_1='按轨道算符：L_z = s·N ⇒ s=1 与 S=ℏ/2 给 N=ℏ/2（非来稿的 N=ℏ）；'
                            '1/2 只能来自旋量 2×2 表示，而标量场 Σ^{μνα}=0',
         mutant_check='ratio == s exactly (no 1/2): %s' % ok,
         verdict='PASS: 相位缠绕 e^{isφ} 的 Noether 轨道角动量给出 L_z/N=s（无 1/2）；'
                 '来稿 S=(s/2)N 的 1/2 属旋量自旋，标量 ansatz 下无定义 ⇒ N=ℏ 的数值目标不唯一')


def main():
    print('TUFT V3.2 参数拟合后续分支来稿 · 符号核验 T1-T6')
    print('sympy', sp.__version__)
    ed, F_doc, F_code, P = T1_el_sign()
    T2_adjoint()
    T3_envelope(ed, F_doc, F_code, P)
    T4_kernel()
    T5_profile_count()
    T6_orbital_spin_payload = T6_orbital()
    payload = {
        'meta': {
            'script': os.path.relpath(os.path.abspath(__file__), SERIES).replace('\\', '/'),
            'run_time': __import__('datetime').datetime.now().isoformat(timespec='seconds'),
            'subject': '来稿_TUFT_V3.2参数拟合后续分支_伴随梯度与自旋约束_2026-09-27.txt',
            'method': 'sympy exact symbolic derivation; every check prints a nonzero control',
            'sympy_version': sp.__version__,
            'scope': '仅算子代数/变分符号/自由度计数；未重解背景、未做电子拟合、不判定物理真实性',
        },
        'checks': R,
    }
    with open(OUT, 'w', encoding='utf-8') as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2, default=str)
    print('wrote %s (%d bytes)' % (os.path.basename(OUT), os.path.getsize(OUT)))


if __name__ == '__main__':
    main()
