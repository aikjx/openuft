# -*- coding: utf-8 -*-
"""纵波 L3 实验设计：UFE-2 纵波 vs Langmuir 波正面对撞 + 可测信号量级
37 号：UFE-2 纵波 A=A0cos(kz-ωt)ẑ, ω=V_z·k（线性过原点、无低频截止），B=0, S=0(储能不辐射), v=V_z<c
已知物理：等离子体纵波 = Langmuir 波, ω²=ω_p²+3k²v_th²（低频截止 ω_p）
对撞判据：低频行为——线性过原点(UFE-2) vs ω_p 截止(Langmuir)。可证伪/可区分。
f 标定(40号)：f=m_e/2e=2.843e-12 → 纵波 E 幅值 = f·v_z·ω 可定量。
"""
import numpy as np

me=9.1093837015e-31; e=1.602176634e-19; eps0=8.8541878128e-12; c=299792458.0
f=me/(2*e)
print("== f 标定 ==")
print(f" f=m_e/2e={f:.4e} SI\n")

print("== A. 正面对撞：UFE-2 纵波 vs Langmuir 波色散 ==")
# 设等离子体参数
n0=1e19  # 1e19 m^-3（中等密度等离子体）
wp=np.sqrt(n0*e**2/(eps0*me))   # Langmuir 等离子体频率
vz=0.1*c  # UFE-2 纵波轴向速度（电荷慢速）
print(f" n0={n0:.1e} m⁻³ → ω_p=√(n0e²/ε0me)={wp:.3e} rad/s (ν_p={wp/2/np.pi:.3e} Hz)")
print(f" UFE-2 纵波取 v_z=0.1c={vz:.3e} m/s → ω=V_z·k")
print("\n 低频极限 k→0：")
print(f"  UFE-2: ω→V_z·k→0（线性过原点，无低频截止）")
print(f"  Langmuir: ω→ω_p={wp:.3e} rad/s（低频截止，k→0 时 ω 不归零）")
print(f"  → 判据：若实测纵波 ω(k→0)→0 线性 → 支持 UFE-2；若 ω→ω_p 截止 → Langmuir 胜，UFE-2 需修正\n")

# 色散数值对比
k=np.linspace(0,2*wp/vz,200)
w_u=np.array([vz*kk for kk in k])          # UFE-2: ω=V_z·k（线性过原点）
w_l=np.sqrt(wp**2+3*k**2*(vz/10)**2)  # Langmuir(v_th=vz/10)
print("  k (1/m)      | ω_UFE2/V_z      | ω_Lang/ω_p")
for kk in [0, wp/vz*0.5, wp/vz*1.0, wp/vz*1.5, 2*wp/vz]:
    wu=vz*kk; wl=np.sqrt(wp**2+3*kk**2*(vz/10)**2)
    print(f"  {kk:9.4e} | {wu/vz:9.4e} (k)  | {wl/wp:9.4e} (ω_p)")

print("\n== B. 纵波 E 幅值量级（f 定值后，可测信号）==")
print(" E_amp = f·v_z·ω = (m_e/2e)·v_z·ω")
for vfrac in [0.01,0.1,0.5]:
    vzv=vfrac*c
    for nu in [1e9,1e11,1e13]:
        w=2*np.pi*nu
        E=f*vzv*w
        u=0.5*eps0*E**2
        print(f"  v_z={vfrac:.2f}c, ν={nu:.0e}Hz: E={E:.3e} V/m, 储能密度 u=½ε0E²={u:.3e} J/m³")

print("\n== C. 判据设计（实验可测）==")
print(" C1 低频色散：测纵波 ω vs k，看 k→0 是否线性归零(UFE-2)还是 ω_p 截止(Langmuir)")
print(" C2 磁场零：纵波区 B=0（横波 B≠0）→ 磁场探头应零读数")
print(" C3 坡印廷零：纵波 S=0 储能不辐射 → 远场功率计不应测到该频率能量（对比横波辐射）")
print(" C4 电场方向：E∥k（纵向），标准横波 E⊥k → 场定向探针")
print("\n 诚实声明：C1 是关键可证伪判据——已知 Langmuir 观测显示 ω_p 截止")
print(" → UFE-2 纵波 ω=V_z·k 线性过原点与观测冲突，要么需修正色散(补 ω_p 项)，要么仅真空成立")
