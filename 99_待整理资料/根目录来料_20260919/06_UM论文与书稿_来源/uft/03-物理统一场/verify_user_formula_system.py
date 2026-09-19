# -*- coding:utf-8 -*-
"""
算法联盟｜对用户"空间元光速螺旋方程体系"的精算审查
==========================================================
目标：把用户给出的方程分成三类，逐项数值+量纲验证：
  [OK]   模型内部自洽（纯几何/Frenet 恒等式，不依赖外部经验常数）
  [WARN] 数学自洽但物理含义需约束的假设
  [FAIL] 量纲错误 / 数值意外 / 错误断言

涉及用户原文方程：
  (A) v_total^2 = v_perp^2 + v_par^2 = c^2
  (B) kappa^2 + tau^2 = omega^2 / c^2
  (C) kappa = alpha*omega/c ,  tau = omega*sqrt(1-alpha^2)/c   // 用户把 alpha=v_perp/c
  (D) alpha = v_perp/c ,  v_par = c*sqrt(1-alpha^2)
  (E) |A| = alpha*c*omega            // 用户引力场模
  (F) A = c^2*(1-alpha^2)*W          // W = 轴向二阶导数
  (G) 1-alpha^2 = 1 - 5.3e-5         // 色散修正量级
  (H) G = alpha^2 * mu0              // 用户自评"只是数值近似"
  (I) -(4*pi*G/alpha^2) dm/dt = q/eps0   // 用户自评"量纲错误"

全程 mpmath 120 位。只验证、不伪造闭合。
"""
import mpmath as mp

mp.mp.dps = 120

# ---------------- 经验常数 (CODATA/PDG，仅作标尺) ----------------
G     = mp.mpf("6.67430e-11")      # m^3 kg^-1 s^-2
eps0  = mp.mpf("8.8541878128e-12") # C^2 N^-1 m^-2
alpha = mp.mpf("7.2973525693e-3")  # 精细结构常数
c     = mp.mpf("299792458")        # m/s
mu0   = 4 * mp.pi * mp.mpf("1e-7")  # = 1.2566370614e-6 H/m (exact by SI definition)
q     = mp.mpf("1.602176634e-19")  # 元电荷 C

def line(t=""):
    print(t)

def main():
    print("=" * 88)
    print("  ALGO-ALLIANCE | Rigorous audit of user spiral-equation system")
    print("=" * 88)

    # ------------------------------------------------------------------
    # (A) 总速率 = c
    # ------------------------------------------------------------------
    line("\n[A] v_total^2 = v_perp^2 + v_par^2 = c^2")
    beta = mp.mpf("0.3")              # 任意横向占比 (NOT forced = alpha)
    vp = beta * c
    vpar = mp.sqrt(c**2 - vp**2)
    vtot2 = vp**2 + vpar**2
    line(f"  demo beta=v_perp/c = {float(beta)}")
    line(f"  v_perp = {float(vp):.6e}, v_par = {float(vpar):.6e}")
    line(f"  v_perp^2+v_par^2 = {float(vtot2):.6e}, c^2 = {float(c**2):.6e}")
    line(f"  relative dev = {float(abs(vtot2-c**2)/c**2):.3e}  => [OK] pure kinematics identity")
    line("  >> meaning: c is NOT photon speed but the invariant total speed of space-cell spiral.")
    line("     [OK] ontologically self-consistent; no empirical constant injected.")

    # ------------------------------------------------------------------
    # (C)+(D) 用户把 alpha = v_perp/c 代入 Frenet
    #   关键检查: 若 alpha = v_perp/c = beta, 则
    #     kappa = alpha*omega/c, tau = omega*sqrt(1-alpha^2)/c
    #   是否真的满足 Frenet 恒等式 kappa^2+tau^2 = omega^2/c^2 ?
    # ------------------------------------------------------------------
    line("\n[C][D] kappa = alpha*omega/c , tau = omega*sqrt(1-alpha^2)/c  with alpha=v_perp/c")
    # 用户的隐含约定: alpha := v_perp/c (geometric), NOT the EM alpha
    alpha_geom = beta
    omega = mp.mpf("1.0")
    kappa_u = alpha_geom * omega / c
    tau_u   = omega * mp.sqrt(1 - alpha_geom**2) / c
    lhs_id  = kappa_u**2 + tau_u**2
    rhs_id  = omega**2 / c**2
    line(f"  alpha_geom(=v_perp/c) = {float(alpha_geom)}  (NOTE: NOT the EM fine-structure alpha)")
    line(f"  kappa = {float(kappa_u):.6e}, tau = {float(tau_u):.6e}")
    line(f"  kappa^2+tau^2 = {float(lhs_id):.6e}")
    line(f"  omega^2/c^2   = {float(rhs_id):.6e}")
    line(f"  relative dev  = {float(abs(lhs_id-rhs_id)/rhs_id):.3e}  => [OK] Frenet identity holds")
    line("  >> [WARN] math OK, but 'alpha = v_perp/c' redefines alpha as a GEOMETRIC ratio.")
    line("     The REAL EM alpha (7.3e-3) is a measured coupling, NOT proven = v_perp/c here.")
    line("     If alpha_geom is set to EM alpha (7.3e-3), then beta=v_perp/c=7.3e-3 is just a")
    line("     re-labeling of beta, still a free geometric DOF -- no physics derived.")

    # check: v_perp from this alpha, and v_par share the c split
    vperp_geom = alpha_geom * c
    vpar_geom  = c * mp.sqrt(1 - alpha_geom**2)
    line(f"  v_perp = alpha*c = {float(vperp_geom):.6e}, v_par = c*sqrt(1-alpha^2) = {float(vpar_geom):.6e}")
    line("  >> [OK] consistent split of c into transverse/axial components.")

    # ------------------------------------------------------------------
    # (E) |A| = alpha*c*omega  (user: grav field magnitude)
    #   对照主线: A = kappa*c^2 (公理4). 若 kappa = alpha*omega/c, 则
    #     A = (alpha*omega/c)*c^2 = alpha*c*omega  ==> 与(E)一致!
    #   所以(E)在"alpha=alpha_geom=v_perp/c"约定下是公理4的等价写法。
    # ------------------------------------------------------------------
    line("\n[E] |A| = alpha*c*omega  (user gravitational field magnitude)")
    A_from_E = alpha_geom * c * omega
    A_from_kappa = kappa_u * c**2
    line(f"  A_from_E (alpha*c*omega)        = {float(A_from_E):.6e}")
    line(f"  A_from_kappa (kappa*c^2, Ax4)   = {float(A_from_kappa):.6e}")
    line(f"  relative dev = {float(abs(A_from_E-A_from_kappa)/A_from_kappa):.3e}  => [OK] identical to Axiom4")
    line("  >> [OK] (E) is NOT a new claim; it is Axiom4 under alpha=v_perp/c convention. dim [L T^-2] OK.")

    # ------------------------------------------------------------------
    # (F) A = c^2*(1-alpha^2)*W
    #   W = ? 用户称 W 为"轴向二阶导数"。量纲检查:
    #     [A] = [L T^-2]
    #     [c^2] = [L^2 T^-2]
    #     => [W] must be [L^-1] to balance.
    #   "轴向二阶导数" 若指 d^2 z/dt^2 (轴向加速度) 则 [W]=[L T^-2] -> WRONG dim.
    #   若 W = d^2 z/dx^2 (轴向对弧长二阶导, 即螺旋挠率相关量) 则 [W]=[L^-1] -> OK.
    # ------------------------------------------------------------------
    line("\n[F] A = c^2*(1-alpha^2)*W   (user: W = axial second derivative)")
    # Case 1: W as axial acceleration d^2 z/dt^2
    W_acc = mp.mpf("1.0")  # placeholder m/s^2
    A_F_acc = c**2 * (1 - alpha_geom**2) * W_acc
    line(f"  IF W = d^2z/dt^2 (axial accel, dim [L T^-2]={float(W_acc)} m/s^2):")
    line(f"     [c^2(1-a^2)W] = [L^2T^-2][LT^-2] = [L^3T^-4]; [A]=[LT^-2]  => [FAIL] dim mismatch")
    # Case 2: W as d^2 z/ds^2 (axial curvature w.r.t arc length, dim [L^-1])
    # For cylinder helix z = h*theta, s = sqrt(r^2+h^2)*theta => dz/ds = h/sqrt(r^2+h^2) const
    # d^2z/ds^2 = 0 for ideal helix! So W=0 unless non-ideal. Use tau-related proxy.
    # Actually the standard wave eq: A = c^2 * (spatial laplacian) ; here W likely means
    # a spatial second derivative (dim [L^-1] after one more spatial deriv) -- ambiguous.
    line(f"  IF W = spatial 2nd deriv (dim [L^-1], e.g. d^2z/dx^2):")
    line(f"     [c^2(1-a^2)W] = [L^2T^-2][L^-1] = [LT^-2] = [A]  => [OK] dim consistent")
    line("  >> [WARN] (F) is dimensionally OK ONLY if W is a SPATIAL second derivative")
    line("     (e.g. d^2(field)/dx^2, dim L^-1), NOT axial acceleration (dim L T^-2).")
    line("     The text calls W '轴向二阶导数' which is ambiguous; must specify spatial vs temporal.")
    line("  >> [OK] when alpha->0: A ~= c^2*W reduces to standard wave operator (zero-order approx).")
    line("     This claim is mathematically sound as a perturbation: A = c^2(1-a^2)W.")

    # numeric: show the (1-alpha^2) correction magnitude for EM alpha
    line("\n  numeric (1-alpha_EM^2) correction factor:")
    line(f"   1 - alpha_EM^2 = {float(1-alpha**2):.10f}")
    line(f"   deviation from 1 = {float(alpha**2):.6e}  (~5.3e-5, matches user)")

    # ------------------------------------------------------------------
    # (G) 1 - alpha^2 = 1 - 5.3e-5  (dispersion correction magnitude)
    # ------------------------------------------------------------------
    line("\n[G] dispersion correction 1-alpha^2 = 1 - 5.3e-5")
    line(f"  alpha_EM^2 = {float(alpha**2):.6e}  (~5.33e-5)  => [OK] matches 5.3e-5")
    line("  >> [OK] magnitude correct, but this is ~5e-5, NOT a unique prediction:")
    line("     any theory with alpha-em-like parameter gives same order. Not falsifiable yet.")

    # ------------------------------------------------------------------
    # (H) G = alpha^2 * mu0   (user self-admits 'just numeric approximation')
    # ------------------------------------------------------------------
    line("\n[H] G = alpha^2 * mu0   (user: only numeric approximation)")
    G_from_H = alpha**2 * mu0
    line(f"  alpha_EM^2 * mu0 = {float(G_from_H):.6e}")
    line(f"  observed G       = {float(G):.6e}")
    line(f"  ratio G/(alpha^2 mu0) = {float(G/G_from_H):.6e}   (would need =1 for identity)")
    line("  >> [FAIL as identity] NOT a derived relation; user correctly flags as numeric coincidence.")
    line("     dim note: [alpha^2 mu0] = [H/m] = [N A^-2] = [kg m C^-2]; [G] = [m^3 kg^-1 s^-2].")
    line("     These are NOT dimensionally equivalent without extra unit factors -> cannot be identity.")
    line("     (this is the same trap as old G*eps0 ~ alpha^2/c^2; see Geps0_修正推导.md)")

    # ------------------------------------------------------------------
    # (I) -(4*pi*G/alpha^2) dm/dt = q/eps0   (user self-admits dimensionally wrong)
    # ------------------------------------------------------------------
    line("\n[I] -(4*pi*G/alpha^2) dm/dt = q/eps0   (user: dimensional error)")
    # LHS dim: [G]=m^3 kg^-1 s^-2, [dm/dt]=kg s^-1 => [G dm/dt] = m^3 s^-3
    #          times (4pi/alpha^2) dimensionless => [LHS] = [L^3 T^-3]
    # RHS dim: [q/eps0] = [C] / [C^2 N^-1 m^-2] = [N m^2 C^-1] = [kg m^3 s^-2 C^-1]
    # LHS has no charge; RHS has charge^-1 -> dimensionally INCOMPATIBLE.
    LHS_dim = "m^3 s^-3"          # = L^3 T^-3
    RHS_dim = "kg m^3 s^-2 C^-1"  # = M L^3 T^-2 Q^-1
    line(f"  [LHS] = [G dm/dt] = (m^3 kg^-1 s^-2)(kg s^-1) = {LHS_dim}")
    line(f"  [RHS] = [q/eps0]  = C / (C^2 N^-1 m^-2) = kg m^3 s^-2 C^-1 = {RHS_dim}")
    line("  >> [FAIL] dimensionally inconsistent: LHS has no charge dimension, RHS has C^-1.")
    line("     User correctly flags this. The corrected form (see derive script) is the")
    line("     dynamics AXIOM -4pi G/alpha^2 dm/dt = q/eps0 only as a FIELD-PHASE relation,")
    line("     not a dimensionally closed equation; needs a charge-mass coupling constant.")
    line("     (In derive_Geps0_first_principles.py this is Axiom6, used only to invert G*eps0,")
    line("      never claimed as a closed physical law.)")

    # ------------------------------------------------------------------
    # (II) m ~ omega  (mass as oscillation frequency) -- user: just hypothesis
    # ------------------------------------------------------------------
    line("\n[II] m proportional omega  (user: hypothesis, no derivation)")
    line("  >> [WARN] plausible geometric direction but: (a) no proportionality constant given,")
    line("     (b) dimensionally m [kg] vs omega [s^-1] differ by [kg s] = [hbar/c^2] scale,")
    line("     so m = (hbar/c^2) * omega * (dimensionless factor). Without the factor it is incomplete.")
    line("     Consistent with main framework N4 genealogy: m_e is CLOSED-over-calibration-rod,")
    line("     i.e. NOT pure-topology-generated; must inject measured m_e.")

    # ------------------------------------------------------------------
    # Final classification
    # ------------------------------------------------------------------
    line("\n" + "=" * 88)
    line("  CLASSIFICATION SUMMARY")
    line("=" * 88)
    line("  [OK]   (A) v_total=c, (B) Frenet id, (C)(D) kappa/tau with alpha=v_perp/c,")
    line("         (E)=Axiom4, (F)-as-wave-operator, (G) magnitude 5.3e-5")
    line("  [WARN] (C)(D) redefine alpha as geometric (not EM alpha); (F) needs W spatial-dim;")
    line("         (II) m~omega needs hbar/c^2 scale factor")
    line("  [FAIL] (H) G=alpha^2 mu0 (numeric coincidence, dim mismatch);")
    line("         (I) dm/dt eqn dimensionally broken (no charge dim on LHS)")
    line("  CONCLUSION: internally the spiral geometry is self-consistent KINEMATICS;")
    line("  but (1) alpha must NOT be conflated with EM alpha without proof,")
    line("  (2) G=alpha^2 mu0 and the dm/dt eqn are NOT valid as stated,")
    line("  (3) no falsifiable unique prediction yet -> model, not physical breakthrough.")

if __name__ == "__main__":
    main()
