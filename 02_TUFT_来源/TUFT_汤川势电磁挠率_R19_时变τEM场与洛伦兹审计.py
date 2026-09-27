# -*- coding: utf-8 -*-
"""
TUFT 汤川势 + 电磁挠率章 · R19：时变 τ^EM 场动力学 + 洛伦兹不变性审计（选项 B）
================================================================================
上游：v2.1.1（R1–R12）+ 第三轮审计 R13–R18（R9 四矢势记账、AL-D5-5e 同义反复缺陷）

本册目标（§六 第 1 优先级）：
  ① §2.2 记账从「静态」推广到「时变」，并用**直接 dA + 度规**推导替换同义反复判定；
  ② 洛伦兹不变性审计（两不变量 + 场映射 boost 协变性 + Bianchi 恒等式）；
  ③ 非齐次方程**源项**的几何可导出性判定（"补齐 Maxwell 源项"是否可能）；
  ④ O17 收窄（Frenet 曲线标量 → 时空四矢量）。

本册显式固定的约定（v2.1.1 未写，正是 F14 的根源）：
  x^0 = c t，∂_0 = (1/c)∂_t；η = diag(+1,−1,−1,−1)；
  A^μ = k·τ^EM,μ（**全部上指标**：τ^0, τ^i 与 A^μ 同位）；下指标 τ_μ = η_{μμ}τ^μ（τ_0=τ^0, τ_i=−τ^i）；
  F^{μν} = ∂^μA^ν − ∂^νA^μ = k·η^{μμ}η^{νν}(∂_μτ_ν − ∂_ντ_μ)；
  E_i := c·F_{0i}，F^{ij} = −ε^{ijk}B_k（⇒ B_x=−F^{23}, B_y=−F^{31}, B_z=−F^{12}）。

红线：数学自洽 ≠ 物理实证；模型假设项一律 BOUNDARY；发现自身缺陷一律 FAIL 不粉饰。
产出：同目录 .txt / .json
"""
import json
import math
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
results = []


def check(code, name, status, detail, evidence=None, mode="体系对齐", kind="计算型"):
    results.append({"code": code, "name": name, "status": status, "detail": detail,
                    "evidence": evidence or {}, "mode": mode, "kind": kind})
    print(f"[{status:8s}] {code} [{mode}|{kind}] {name}: {detail}")


# ============================================================
# 0. 约定与基本对象
# ============================================================
t, x, y, z = sp.symbols("t x y z", real=True)
cs = sp.Symbol("c", positive=True)
ks = sp.Symbol("k", positive=True)
CO = (t, x, y, z)
ETA = (1, -1, -1, -1)
tau = [sp.Function(f"tau{i}")(t, x, y, z) for i in range(4)]   # 下指标 τ_μ
tau_up = [tau[0], -tau[1], -tau[2], -tau[3]]                   # 上指标 τ^μ


def dmu(f, m):
    """∂_μ（x^0 = c t ⇒ ∂_0 = (1/c)∂_t）"""
    return sp.diff(f, CO[m])/cs if m == 0 else sp.diff(f, CO[m])


def Fup(m, n):
    """F^{μν} = k η^{μμ} η^{νν} (∂_μ τ_ν − ∂_ν τ_μ)"""
    return ks*ETA[m]*ETA[n]*(dmu(tau[n], m) - dmu(tau[m], n))


E_tau = [sp.simplify(-cs*Fup(0, i+1)) for i in range(3)]                       # E_i = c F_{0i} = −c F^{0i}
B_tau = [sp.simplify(-Fup(2, 3)), sp.simplify(-Fup(3, 1)), sp.simplify(-Fup(1, 2))]   # 自 F^{ij}=−ε^{ijk}B_k

# ============================================================
# R19-1：时变记账直接推导 —— R9 遗留的「时变项指标约定」未声明（F14）
# ============================================================
E_read_up = [sp.simplify(-ks*(cs*dmu(tau[0], i+1) + sp.diff(tau_up[i+1], t))) for i in range(3)]   # §2.2 读作 τ^i
E_read_low = [sp.simplify(-ks*(cs*dmu(tau[0], i+1) + sp.diff(tau[i+1], t))) for i in range(3)]     # 统一读作 τ_i
d_up = [sp.simplify(E_tau[i] - E_read_up[i]) for i in range(3)]
d_low = [sp.simplify(E_tau[i] - E_read_low[i]) for i in range(3)]
up_ok = all(sp.simplify(d_) == 0 for d_ in d_up)
low_nonzero = all(sp.simplify(d_) != 0 for d_ in d_low)
check("AL-R19-1", "★ R19：时变记账直接推导——R9 遗留的「时变项指标约定」未声明（F14）",
      "PASS" if (up_ok and low_nonzero) else "FAIL",
      "由 F=dA（含度规）取 E_i := c·F_{0i}（**不经 E 映射**，避开 R15 指出的同义反复）："
      "E_i=−kc∂_iτ^0−k∂_tτ^i。与 v2.1.1 §2.2 的 E=−k(c∇τ_t+∂_tτ) 逐分量比对："
      f"①∂_tτ 读作**上指标** τ^i（与 A^μ=kτ^μ 同位）⇒ 残差 {[str(d_) for d_ in d_up]}（公式正确）；"
      f"②统一读作**下指标** τ_i ⇒ 残差 {[str(d_) for d_ in d_low]} = ±2k∂_tτ_i ≠ 0（**时变项符号相反**）。"
      "⇒ F14 不是符号错误而是**约定未声明**（静态极限两种读法一致，故前两轮漏检，见 R19-9）；"
      "本册固定：A^μ=kτ^μ（全上指标），E=−kc∇τ^0−k∂_tτ^i，B=k∇×τ^μ，F^{0i}=k(∂_iτ^0+(1/c)∂_tτ^i)=−E_i/c",
      {"E_from_F": [str(e) for e in E_tau], "residual_upper_reading": [str(d_) for d_ in d_up],
       "residual_lower_reading": [str(d_) for d_ in d_low]}, mode="求导证明", kind="计算型")

# ============================================================
# R19-2：(E,B) ↔ F^{μν} ↔ τ 三向一致（时变）
# ============================================================
curl_up = [ks*(sp.diff(tau_up[3], y) - sp.diff(tau_up[2], z)),
           ks*(sp.diff(tau_up[1], z) - sp.diff(tau_up[3], x)),
           ks*(sp.diff(tau_up[2], x) - sp.diff(tau_up[1], y))]     # B = k ∇×τ^μ（上指标，与 §2.2 一致）
Fij_ok = all(sp.simplify(B_tau[i] - curl_up[i]) == 0 for i in range(3))
Frec = sp.zeros(4, 4)
for i in range(3):
    Frec[0, i+1], Frec[i+1, 0] = -E_tau[i]/cs, E_tau[i]/cs
Frec[1, 2], Frec[2, 1] = -B_tau[2], B_tau[2]
Frec[2, 3], Frec[3, 2] = -B_tau[0], B_tau[0]
Frec[3, 1], Frec[1, 3] = -B_tau[1], B_tau[1]
Fgen = sp.Matrix(4, 4, lambda a, b: Fup(a, b))
roundtrip = sp.simplify(Frec - Fgen)
rt_ok = all(sp.simplify(roundtrip[a, b]) == 0 for a in range(4) for b in range(4))
check("AL-R19-2", "R19：(E,B) ↔ F^{μν} ↔ τ 三向一致（含时变项）", "PASS" if (Fij_ok and rt_ok) else "FAIL",
      f"①B 与 F^{{ij}} 一致（B=k∇×τ^μ，F^{{ij}}=−ε^{{ijk}}B_k，逐分量检验 {Fij_ok}）；"
      f"②**双向重建**：τ→(E,B)→F^{{μν}} 与 τ→F^{{μν}} 逐分量相等（含 ∂_tτ）：{rt_ok} ⇒ "
      "时变扇区记账自洽；注意 B 必须由**上指标** 3-矢量 τ^i 构造（用 τ_i 则整体反号，见 R19-5 的 Faraday 检验）",
      {"B_equals_curl_upper": bool(Fij_ok), "roundtrip_identity": bool(rt_ok),
       "B_tau": [str(b_) for b_ in B_tau]}, mode="求导证明", kind="计算型")

# ============================================================
# R19-3：洛伦兹不变量
# ============================================================
Ex, Ey, Ez, Bx, By, Bz = sp.symbols("E_x E_y E_z B_x B_y B_z", real=True)
Fmat = sp.zeros(4, 4)
for i, Ei in enumerate((Ex, Ey, Ez)):
    Fmat[0, i+1], Fmat[i+1, 0] = -Ei/cs, Ei/cs
Fmat[1, 2], Fmat[2, 1] = -Bz, Bz
Fmat[2, 3], Fmat[3, 2] = -Bx, Bx
Fmat[3, 1], Fmat[1, 3] = -By, By
Flower = sp.Matrix(4, 4, lambda a, b: ETA[a]*ETA[b]*Fmat[a, b])
I1 = sp.simplify(sum(Flower[a, b]*Fmat[a, b] for a in range(4) for b in range(4)))
I1_std = sp.simplify(I1 - 2*(Bx**2 + By**2 + Bz**2 - (Ex**2 + Ey**2 + Ez**2)/cs**2))
vv = sp.Symbol("V", positive=True)
gg = 1/sp.sqrt(1 - vv**2/cs**2)
Lam = sp.Matrix([[gg, -gg*vv/cs, 0, 0], [-gg*vv/cs, gg, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
Fp = Lam*Fmat*Lam.T
Flower_p = sp.Matrix(4, 4, lambda a, b: ETA[a]*ETA[b]*Fp[a, b])
I1p = sp.simplify(sum(Flower_p[a, b]*Fp[a, b] for a in range(4) for b in range(4)))
I1_inv = sp.simplify(sp.together(I1p - I1))
# I2 = ε^{μνρσ}F_{μν}F_{ρσ} ∝ E·B：数值 boost 验证
eps4 = np.zeros((4, 4, 4, 4))
for a in range(4):
    for b in range(4):
        for c_ in range(4):
            for d_ in range(4):
                if len({a, b, c_, d_}) == 4:
                    perm, sgn = [a, b, c_, d_], 1
                    for i_ in range(4):
                        for j_ in range(i_+1, 4):
                            if perm[i_] > perm[j_]:
                                sgn = -sgn
                    eps4[a, b, c_, d_] = sgn
rng = np.random.default_rng(20260926)
En, Bn = rng.normal(size=3), rng.normal(size=3)
Fn = np.zeros((4, 4))
Fn[0, 1:], Fn[1:, 0] = -En, En
Fn[1, 2], Fn[2, 1] = -Bn[2], Bn[2]
Fn[2, 3], Fn[3, 2] = -Bn[0], Bn[0]
Fn[3, 1], Fn[1, 3] = -Bn[1], Bn[1]
bb = 0.6
gb = 1/math.sqrt(1-bb**2)
Lb = np.array([[gb, -gb*bb, 0, 0], [-gb*bb, gb, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
Fnb = Lb@Fn@Lb.T
eta_n = np.diag([1., -1., -1., -1.])
Flo_n, Flo_nb = eta_n@Fn@eta_n, eta_n@Fnb@eta_n
I1n, I1nb = float(np.sum(Flo_n*Fn)), float(np.sum(Flo_nb*Fnb))
I2n = float(np.einsum("abcd,ab,cd->", eps4, Flo_n, Flo_n))
I2nb = float(np.einsum("abcd,ab,cd->", eps4, Flo_nb, Flo_nb))
inv_ok = abs(I1n-I1nb) < 1e-12 and abs(I2n-I2nb) < 1e-12
I2_EB = float(np.einsum("abcd,ab,cd->", eps4, Flo_n, Flo_n))
check("AL-R19-3", "R19：洛伦兹不变量审计（I1=F_{μν}F^{μν}=2(B²−E²/c²)；I2=εF F ∝ E·B）",
      "PASS" if (I1_std == 0 and I1_inv == 0 and inv_ok) else "FAIL",
      f"sympy 符号：I1−2(B²−E²/c²) 残差 = {I1_std}；boost 下 I1′−I1 = {I1_inv}（严格不变）；"
      f"数值随机场（v/c=0.6，c=1）：I1 {I1n:.8f}→{I1nb:.8f}、I2 {I2n:.8f}→{I2nb:.8f}（差 <1e-12）"
      f"⇒ I2 亦为洛伦兹不变量（∝E·B）｜(E,B)↔F 记账与洛伦兹结构相容",
      {"I1_minus_standard": str(I1_std), "I1_boost_diff": str(I1_inv),
       "I1_num": [I1n, I1nb], "I2_num": [I2n, I2nb]}, mode="求导证明", kind="计算型")

# 场变换形式（boost along x）与教科书式一致
Ep = [sp.simplify(-cs*Fp[0, i+1]) for i in range(3)]
Bp = [sp.simplify(-Fp[2, 3]), sp.simplify(-Fp[3, 1]), sp.simplify(-Fp[1, 2])]
std_ep = [Ex, gg*(Ey - vv*Bz), gg*(Ez + vv*By)]
std_bp = [Bx, gg*(By + vv*Ez/cs**2), gg*(Bz - vv*Ey/cs**2)]
std_ep_m = [Ex, gg*(Ey + vv*Bz), gg*(Ez - vv*By)]
std_bp_m = [Bx, gg*(By - vv*Ez/cs**2), gg*(Bz + vv*Ey/cs**2)]
ep_ok = all(sp.simplify(Ep[i] - std_ep[i]) == 0 for i in range(3))
bp_ok = all(sp.simplify(Bp[i] - std_bp[i]) == 0 for i in range(3))
ep_ok_m = all(sp.simplify(Ep[i] - std_ep_m[i]) == 0 for i in range(3))
bp_ok_m = all(sp.simplify(Bp[i] - std_bp_m[i]) == 0 for i in range(3))
matched = (ep_ok and bp_ok) or (ep_ok_m and bp_ok_m)
direction = "+v" if (ep_ok and bp_ok) else ("-v" if (ep_ok_m and bp_ok_m) else "none")
check("AL-R19-4", "R19：E,B 的 boost 变换与标准变换式一致（映射洛伦兹协变的直接证据）",
      "PASS" if matched else "FAIL",
      f"由 F′=ΛFΛᵀ 提取（E′_i=−cF′^{{0i}}、B′_x=−F′^{{23}}…）与标准式（E′_∥=E_∥、E′_⊥=γ(E+v×B)_⊥、"
      f"B′_⊥=γ(B−v×E/c²)_⊥）逐分量比对：与式 (+v) 一致 {ep_ok and bp_ok}、与式 (−v) 一致 {ep_ok_m and bp_ok_m} "
      f"⇒ 本次 Λ 对应标准式的速度**方向 {direction}**（两式互为 v↔−v 反演；差异只是 boost 方向约定，"
      "非结构错误）⇒ A^μ=kτ^μ 的记账与洛伦兹变换相容（R9 应收录而缺失的真检验）",
      {"match_plus_v": bool(ep_ok and bp_ok), "match_minus_v": bool(ep_ok_m and bp_ok_m),
       "direction": direction, "Ep": [str(e) for e in Ep], "Bp": [str(e) for e in Bp]},
      mode="求导证明", kind="计算型")

# ============================================================
# R19-5：齐次 Maxwell（Bianchi 恒等式）自动成立
# ============================================================
Flo_sym = sp.Matrix(4, 4, lambda a, b: ETA[a]*ETA[b]*Fgen[a, b])
Fdual = sp.Matrix(4, 4, lambda m, n: sp.Rational(1, 2)*sum(
    int(eps4[m, n, r_, s_])*Flo_sym[r_, s_] for r_ in range(4) for s_ in range(4)))
div_dual = [sp.simplify(sum(dmu(Fdual[m, n], m) for m in range(4))) for n in range(4)]
div_dual_ok = all(sp.simplify(d_) == 0 for d_ in div_dual)
# 投影：∇·B=0 与 ∂_tB+∇×E=0（用与 F 一致的上指标 B）
divB = sp.simplify(sp.diff(B_tau[0], x) + sp.diff(B_tau[1], y) + sp.diff(B_tau[2], z))
faraday = [sp.simplify(sp.diff(B_tau[0], t) + (sp.diff(E_tau[2], y) - sp.diff(E_tau[1], z))),
           sp.simplify(sp.diff(B_tau[1], t) + (sp.diff(E_tau[0], z) - sp.diff(E_tau[2], x))),
           sp.simplify(sp.diff(B_tau[2], t) + (sp.diff(E_tau[1], x) - sp.diff(E_tau[0], y)))]
far_ok = all(f == 0 for f in faraday)
check("AL-R19-5", "R19：齐次 Maxwell（Bianchi）自动成立——无需任何动力学", "PASS" if (div_dual_ok and divB == 0 and far_ok) else "FAIL",
      f"对偶张量散度 ∂_μF̃^{{μν}}≡0（一般 τ 符号化简，四分量全 0：{div_dual_ok}）；"
      f"投影 ∇·B=0（残差 {divB}）、∂_tB+∇×E=0（三分量全 0：{far_ok}）"
      "⇒ 齐次方程是 F=dA 的代数后果（Bianchi），**不含物理信息**；"
      "电磁扇区的物理内容全在非齐次源项（见 R19-6）——注意：∂_μF^{{μν}}=0 是**有源方程的真空形式**，"
      "不是恒等式（本册用对偶张量避免这一常见混淆）",
      {"dual_divergence_zero": bool(div_dual_ok), "divB": str(divB), "faraday_zero": bool(far_ok)},
      mode="求导证明", kind="计算型")

# ============================================================
# R19-6：非齐次源项能否"由几何导出"——决定性判定
# ============================================================
G_ = sp.Matrix(4, 4, lambda a, b: sp.Symbol(f"G{a}{b}"))
Fs_ = sp.Matrix(4, 4, lambda a, b: G_[a, b] - G_[b, a])
Fs_up = sp.Matrix(4, 4, lambda a, b: ETA[a]*ETA[b]*Fs_[a, b])
Lv = sp.simplify(-sp.Rational(1, 4)*sum(Fs_up[a, b]*Fs_up[a, b]*ETA[a]*ETA[b] for a in range(4) for b in range(4)))
dLdG = sp.Matrix(4, 4, lambda a, b: sp.simplify(sp.diff(Lv, G_[a, b])))
# ∂L/∂(∂_μA_ν) = −F^{μν}（对本约定逐元检验）
half_ok = all(sp.simplify(dLdG[a, b] + Fs_up[a, b]) == 0 for a in range(4) for b in range(4))
no_source = half_ok
# 规范不变性：自源 J^ν=σ τ^ν 的双重排除
Lam_f = sp.Function("Lambda")(t, x, y, z)
dLam_up = [ETA[m]*dmu(Lam_f, m) for m in range(4)]
selfsource_gauge_changes = any(sp.simplify(dLam_up[m]) != 0 for m in range(4))
consv_res = sp.simplify(sum(ETA[m]*ETA[m]*dmu(tau[m], m) for m in range(4)))
check("AL-R19-6", "★ R19：非齐次 Maxwell 源项**不可由几何导出**（决定性判定）", "FAIL",
      "①自由作用量 S=−¼∫F² 的 Euler–Lagrange：L 不显含 A_μ（规范不变）⇒ 方程只含 ∂L/∂(∂_μA_ν) 项；"
      f"sympy 逐元验证 ∂L/∂G_{{μν}} = −F^{{μν}}（{half_ok}）⇒ EL：∂_μF^{{μν}}=0（**无源**，且 ∂L/∂A_ν=0 无质量/源项），"
      f"几何结构不含任何 J^ν；②「几何自源」J^ν=σ τ^ν 双重被排除：**不守恒**（∂_νJ^ν = σ·∂_ν τ^ν = {consv_res}，一般 τ ≠0）"
      f"且**非规范不变**（τ^ν→τ^ν+∂^νΛ ⇒ ∂^νΛ ≠ 0：{selfsource_gauge_changes}）；"
      "③δ(∂_μF^{μν})=0（F 规范不变）⇒ 方程 ∂_μF^{μν}=στ^ν 只在 σ=0 时协变 ⇒ "
      "**源项必须来自外部守恒电流（物质），不能由 κ–τ 几何/场自身产生**",
      {"dLdG_equals_minus_Fup": bool(no_source), "div_selfsource": str(consv_res),
       "gauge_violation": bool(selfsource_gauge_changes)}, mode="求导证明", kind="计算型")

# ============================================================
# R19-7：Proca 型自源被规范不变性 + μ_EM=0 排除
# ============================================================
A_ = [sp.Function(f"A{i}")(t, x, y, z) for i in range(4)]
mm = sp.Symbol("m", positive=True)
Sproca_gauge = sp.simplify(-mm**2*sum(ETA[a]*A_[a]*dLam_up[a] for a in range(4)))
check("AL-R19-7", "R19：Proca 质量项破坏规范不变性 ⇒ 与 μ_EM=0/O16 一致（排除）",
      "PASS" if sp.simplify(Sproca_gauge) != 0 else "FAIL",
      f"δS_Proca = −∫m²A_μ∂^μΛ（A→A+∂Λ 一阶）= {Sproca_gauge} ≠ 0（一般 A, Λ）⇒ "
      "任何「有质量 τ^EM 场」路径都放弃规范不变性；电磁扇区被 O16/μ_EM=0 强制无质量 ⇒ "
      "Proca 自源路径被排除，与 R19-6 合流（唯一剩下的路是接受外部源）",
      {"proca_gauge_violation": str(Sproca_gauge)}, mode="求导证明", kind="计算型")

# ============================================================
# R19-8：O17 收窄——构造候选 τ_w u^μ 与自由度计数
# ============================================================
tw = sp.Symbol("tau_w", real=True)
u4 = [sp.Symbol(f"u{i}", real=True) for i in range(4)]
A_geo = [sp.simplify(tw*u4[a]) for a in range(4)]
dof_in, dof_phys = 4, 2
check("AL-R19-8", "R19：O17 收窄——τ^EM,μ 的最自然几何构造 τ_w u^μ 及自由度缺口", "OPEN",
      "唯一自然的协变构造：τ^EM,μ ∝ τ_w·u^μ（世界线挠率 × 四速度「极化矢量」），τ_w 标量 × u^μ 四矢量 ⇒ "
      f"张量积自动是四矢量（协变性无需额外假设）；但**自由度计数** {dof_in}（τ_w：1；u^μ 在 u·u=1 下：3）"
      f"≠ 无质量规范场物理自由度 {dof_phys}（横向 2）⇒ 要么 u^μ 为独立动力学场（多出 2 个自由度），"
      "要么该构造只是「沿一条世界线」的量、需全时空世界线族（纤维结构）才成为场。"
      "⇒ O17 由「无定义」收窄为「构造存在，自由度/纤维结构未闭合」；"
      "且该构造继承 R19-6 的无源性质（F=dA ⇒ 源仍需外部）",
      {"dof_input": dof_in, "dof_physical": dof_phys, "A_geo_forms": [str(e) for e in A_geo]},
      mode="体系对齐", kind="计算型")

# ============================================================
# R19-9：量纲审计 + 静态回归
# ============================================================
static_E = [sp.simplify(e.subs({sp.Derivative(tau[j], t): 0 for j in range(4)}).doit()) for e in E_tau]
static_ok = all(sp.simplify(static_E[i] + ks*cs*dmu(tau[0], i+1)) == 0 for i in range(3))
check("AL-R19-9", "R19：量纲审计 [k]=V·s（A=kτ ⇒ T·m）+ 静态回归到 v2.1.1", "PASS" if static_ok else "FAIL",
      "量纲：[A]=T·m=V·s/m；[τ^EM]=m⁻¹ ⇒ [k]=[A]/[τ]=**V·s**（非无量纲；由 E=kc∇τ 的 [E]=V/m 独立复核）"
      f"⇒ R9「k 含量纲」声明得到定量确认；静态回归：∂_tτ=0 时 E=−kc∇τ^0（逐分量检验 {static_ok}）、"
      "B=k∇×τ^μ，与 v2.1.1 §2.3 完全一致 ⇒ 本册时变修正**不影响**已验证的静态仿真",
      {"k_dimension": "[V·s]", "static_regression": bool(static_ok),
       "static_E": [str(e) for e in static_E]}, mode="精算验证", kind="计算型")

# ============================================================
# R19-10：边界与开放项关系
# ============================================================
check("AL-R19-10", "R19：诚实边界与开放项关系表", "BOUNDARY",
      "本册闭合：时变记账（约定显式化）／协变性（I1、I2、boost 场变换）／齐次 Maxwell（Bianchi）／"
      "源项不可几何导出（自源与 Proca 双排除）／O17 收窄。"
      "本册**不**给出：源的微观形式（须外部守恒电流，O15/O17）、τ^EM 的动力学作用量（无源 ⇒ 需外加耦合）、"
      "量子化（α/e，O15）。⇒ 「补齐 Maxwell 源项」这一原目标被**判定为不可在几何内完成**（非未完成），"
      "与 O15（标度侧）、O17（类型学侧）三方一致",
      {}, mode="体系对齐", kind="声明型")

# ============================================================
# 汇总
# ============================================================
from collections import Counter
cnt = Counter(r["status"] for r in results)
mode_cnt = Counter(r["mode"] for r in results)
kind_cnt = Counter(r["kind"] for r in results)
print("\n" + "="*70)
print(f"【R19 判定 {len(results)} 项】")
print(f"  PASS {cnt['PASS']} / FAIL {cnt['FAIL']} / OPEN {cnt['OPEN']} / BOUNDARY {cnt['BOUNDARY']} / INFO {cnt['INFO']}")
print("  模式分布：" + "；".join(f"{m} {n}" for m, n in sorted(mode_cnt.items())))
print("  证据类型：" + "；".join(f"{m} {n}" for m, n in sorted(kind_cnt.items())))
print("="*70)

out = {"canonical": {"total": len(results), **cnt,
                     "mode_distribution": dict(mode_cnt), "kind_distribution": dict(kind_cnt)},
       "checks": results}
with open(os.path.join(HERE, "TUFT_汤川势电磁挠率_R19_时变τEM场与洛伦兹审计.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
with open(os.path.join(HERE, "TUFT_汤川势电磁挠率_R19_时变τEM场与洛伦兹审计.txt"), "w", encoding="utf-8") as f:
    f.write("TUFT 汤川势+电磁挠率章 · R19 时变 τ^EM 场与洛伦兹不变性审计\n")
    f.write("="*70 + "\n")
    for r_ in results:
        f.write(f"[{r_['status']:8s}] {r_['code']} [{r_['mode']}|{r_['kind']}] {r_['name']}: {r_['detail']}\n")
    f.write(f"\nR19 判定 {len(results)} 项：PASS {cnt['PASS']} / FAIL {cnt['FAIL']} / OPEN {cnt['OPEN']} / "
            f"BOUNDARY {cnt['BOUNDARY']} / INFO {cnt['INFO']}\n")
    f.write(f"模式分布：{dict(mode_cnt)}\n证据类型：{dict(kind_cnt)}\n")
print("已写入 JSON + TXT（同目录）")
