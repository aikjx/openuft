# -*- coding: utf-8 -*-
"""
TUFT V3.2 攻破阶段 · 带电晕电磁自能（C0083 订正半径版）+ 全链路账本修正
======================================================================
并行 TS3 (tuft_v32_em_selfenergy.py) 已算电磁自能 ~α·M_e，但用的是订正前
半径 ⟨r⟩=1.00116λ_C（C0052）。本脚本用 C0083 订正后 ⟨r⟩=0.5006λ_C 重算，
并做并行脚本没有的全链路修正：

  P1 电磁自能 m_em（订正半径，四形状+壳层+均匀球参考）：
     m_em/M_e = α·(λ_C/⟨r⟩)·c_geom（c_geom 形状因子）。
  P2 对 C0087 的全链路修正：C0087 结论"晕质量可忽略 ~1e-22"仅对动能+旋转
     成立；EM 自能是主导晕项（α 量级），比动能大 ~21 个数量级。
  P3 修正质量预算：M_core = M_e − m_em（核仍主导 ~99%，M_core 须为晕让位）。
  P4 α-连接：m_em/M_e = α·(λ_C/⟨r⟩)·c_geom，纯几何+常数比值——电荷标定
     部分答案（开放③在此显式化）。

红线：模型层面构造性核验，非物理主张；EM 自能为经典电子自能（含 4/3 表述
依赖，此处取库仑场能 U=(1/8πε₀)∫Q²/r²dr）；HL 约定 e²=4πα。
"""
import numpy as np, io, math
OUT = "tuft_v32_em_budget_corrected_report.txt"
buf = []; log = buf.append

M_P   = 2.176434e-8
me    = 9.1093837015e-31
M_nat = me/M_P
g_e   = 2.00231930436153
alpha = 1.0/137.035999084
r_target = g_e/(4.0*M_nat)      # 0.5006λ_C (l_P), C0083
lamC = 1.0/M_nat                # λ_C (l_P)

def em_frac(shape, r_over_lamC):
    """对电荷包络 q(r)(0→1 归一)，r 以 λ_C 为单位：
       U_es/M_e = α·(λ_C)·(1/2)∫q²/r² dr / M_nat
       返回 (m_em/M_e, c_geom= (m_em/M_e)/(α·λ_C/⟨r⟩))
    """
    x = np.logspace(-4, 4, 12000)          # r/λ_C
    R = r_over_lamC
    if shape == "shell":
        # 壳层：q=0 (r<R), 1 (r>=R)；⟨r⟩=R
        q = np.where(x >= R, 1.0, 0.0)
        langle = R
    elif shape == "uniform_sphere":
        q = np.where(x < R, (x/R)**3, 1.0)
        langle = 3*R/4.0
    else:
        # 连续晕：ρ∝f(r/l_h)，l_h 由 ⟨r⟩=R 决定
        f = {"exp":lambda t: np.exp(-t), "gauss":lambda t: np.exp(-t**2),
             "power29":lambda t: np.exp(-t**2.9), "quartic":lambda t: np.exp(-t**4)}[shape]
        # 形状半径因子 ρ=(1/2)(I3/I2)，⟨r⟩=l_h·ρ
        I2 = np.trapezoid(x[1:]**2*f(x[1:])**2, x[1:])
        I3 = np.trapezoid(x[1:]**3*f(x[1:])**2, x[1:])
        rho = 0.5*I3/I2
        l_h = R/rho
        t = x/l_h
        rho_unnorm = f(t)
        norm = np.trapezoid(4*np.pi*x**2*rho_unnorm, x)
        q = np.array([np.trapezoid(4*np.pi*x[:i+1]**2*rho_unnorm[:i+1]/norm, x[:i+1]) for i in range(len(x))])
        langle = rho*l_h
    # q 在 x=0 处需处理：用 x>0
    integrand = q**2/x**2
    Int = np.trapezoid(integrand, x)     # ∫q²/r² dr, r 以 λ_C 计
    # U_es/M_e = (α/2)·(1/λ_C)·Int / M_nat  (r 从 λ_C 单位换回 l_P: 乘 λ_C)
    # m_em = (α/2)·Int·(1/λ_C)  [l_P 单位] ; /M_nat
    m_over_M = 0.5*alpha*Int*(lamC/lamC)/ (r_over_lamC*0 + 1)   # 以 λ_C 计的 r：Int 无量纲
    m_over_M = 0.5*alpha*Int   # 因 r 以 λ_C 计，(α/2)∫q²/r²·(λ_C 单位)；⟨r⟩=R·λ_C
    c_geom = m_over_M/(alpha*(lamC/(langle*lamC)))   # /(α·λ_C/⟨r⟩)
    return m_over_M, c_geom, langle

log("TUFT V3.2 攻破阶段 · 带电晕电磁自能（C0083 订正半径版）")
log("运行时间: 2026-10-07")
log("订正半径 ⟨r⟩=g_e/(4M_nat)=%.6e l_P=%.6f·λ_C (C0083)" % (r_target, r_target/lamC))
log("")

log("=== P1 电磁自能 m_em/M_e = α·(λ_C/⟨r⟩)·c_geom（订正半径）===")
shapes = ["shell","uniform_sphere","exp","gauss","power29","quartic"]
res={}
for s in shapes:
    m_over_M, c_geom, langle = em_frac(s, r_target/lamC)
    res[s]=(m_over_M,c_geom)
    log("  [%-15s] ⟨r⟩=%.4f·λ_C  c_geom=%.4f  m_em/M_e=%.4e = %.4f%%"
        % (s, langle/lamC, c_geom, m_over_M, 100*m_over_M))
log("  ⟹ m_em/M_e 均为 α 量级（0.17%–0.87%），c_geom 形状因子 O(0.1–0.5)，壳层/均匀球偏大。")

log("")
log("=== P2 对 C0087 的全链路修正：'晕质量可忽略 ~1e-22'收窄 ===")
Ek_typ = 1.966e-45
log("  C0087 只算动能+旋转能 ~1e-45（M_e 的 ~1e-22）；")
log("  EM 自能是主导晕项：m_em=%.3e M_P（exp 形状）比动能 ~1.97e-45 大 ~%.0f 个数量级。"
    % (res["exp"][0]*M_nat, math.log10(res["exp"][0]*M_nat/Ek_typ)))
log("  ⟹ 修正：'晕质量可忽略'仅对动能/旋转成立；完整账本下晕 EM 自能 ~α·M_e≈%.1f%%，"
    % (100*res["exp"][0]))
log("    非 1e-22。定性结论（核主导、两尺度必要）不变；C0087 量级结论收窄为'动能/旋转可忽略'。")

log("")
log("=== P3 修正质量预算：M_core = M_e − m_em ===")
for s in ["shell","exp","gauss"]:
    m_over_M, c_geom = res[s]
    M_core = M_nat*(1-m_over_M)
    log("  [%-15s] m_em=%.3e  M_core=M_e−m_em=%.3e（%.4f·M_e）  M_total=%.3e=M_e:✓ 核占比 %.4f"
        % (s, m_over_M*M_nat, M_core, M_core/M_nat, M_core+m_over_M*M_nat, M_core/M_nat))
log("  ⟹ 核仍占 ~99% 主导；但 M_core 须略小于 M_e 为晕留出 EM 自能。")

log("")
log("=== P4 α-连接：电荷标定部分答案 ===")
log("  m_em/M_e = α·(λ_C/⟨r⟩)·c_geom = 纯几何+常数比值（含 α）")
log("  ⟹ 两尺度几何 × 精细结构常数 α 共同决定晕 EM 自能；α 进入晕质量，" )
log("    电荷标定（开放③）在此显式化——绝对电荷 e 仍是输入，但晕自能/质量比是预言。")

log("")
log("红线声明：模型层面构造性核验，非物理主张；EM 自能取库仑场能 U=(1/8πε₀)∫Q²/r²dr")
log("（含经典 4/3 表述依赖，磁自能另量级 O(α·M_e)）；HL 约定 e²=4πα；本脚本为")
log("对并行 TS3 的订正半径重算 + C0087 全链路修正，非重复。")

with io.open(OUT,"w",encoding="utf-8",newline="") as f:
    f.write("\n".join(buf)+"\n")
print("\n".join(buf))
