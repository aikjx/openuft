# -*- coding: utf-8 -*-
"""本项目 · 纲领 O1 攻破：全息截断视界锚定的第一性闭合性判定
目标：判定『视界 R_H 能否从公设第一性唯一确定』（消除 S10 的 12.23 系数自由）。
方法：枚举全部几何自然尺度，各算 ρ_DE=ρ_Planck(lP/R)²，对比观测 ρ_DE=5.84e-27，
      看是否有一个尺度唯一对应观测（闭合）还是 O(1) 离散（不可闭合）。
纯标准库。
"""
import math

G=6.674e-11; c=2.99792458e8; hbar=1.0546e-34
OmL=0.685; Omm=0.315
H0=67.4e3/3.0857e22          # 1/s
lP=math.sqrt(hbar*G/c**3)
rhoP=c**5/(hbar*G*G)
rde_obs=OmL*3*H0*H0/(8*math.pi*G)

def rde(R):
    return rhoP*(lP/R)**2

print("="*70)
print("纲领 O1：全息截断视界锚定 第一性闭合性判定")
print("="*70)
print(f"观测 ρ_DE = {rde_obs:.3e} kg/m³ (ΩΛ=0.685, H0=67.4)")
print(f"ρ_Planck = {rhoP:.3e}; lP={lP:.3e} m; R_H=c/H0={c/H0:.3e} m")
print()

rows=[]
# ① Hubble 视界
RH=c/H0; rows.append(("Hubble 视界 c/H0", RH, rde(RH)))
# ② 粒子视界（纯物质主导 R=3ct0=2c/H0）
rows.append(("粒子视界 3ct0=2c/H0", 2*c/H0, rde(2*c/H0)))
# ③ 事件视界（ΛCDM 数值积分）
def I_event():
    # I=∫_1^∞ da/(a²√(Ωm/a³+ΩΛ))
    s=0.0; N=400000; amax=50.0
    for i in range(N):
        a1=1.0+(amax-1)*i/N; a2=1.0+(amax-1)*(i+1)/N
        f=lambda a: 1.0/(a*a*math.sqrt(Omm/a**3+OmL))
        s+=0.5*(f(a1)+f(a2))*(a2-a1)
    # 尾部 a>amax 解析近似 ∫_{amax}^∞ da/(a²√ΩΛ)=1/(amax√ΩΛ)
    s+=1.0/(amax*math.sqrt(OmL))
    return s
IE=I_event(); RE=(c/H0)*IE
rows.append((f"事件视界 (ΛCDM) I={IE:.3f}", RE, rde(RE)))
# ④ 曲率半径 L_R=√(6/R0)，R0=8πGρm/c²
rho_m=Omm*3*H0*H0/(8*math.pi*G)
R0=8*math.pi*G*rho_m/(c*c)
LR=math.sqrt(6/R0)
rows.append((f"曲率半径 √(6/R0) R0=8πGρm/c²", LR, rde(LR)))

print(f"{'视界类型':<32}{'R [m]':<14}{'ρ_DE':<12}{'倍数'}")
for name,R,rd in rows:
    print(f"{name:<32}{R:.3e}  {rd:.3e}  {rd/rde_obs:.2f}×")

print()
print("="*70)
print("O1 判定")
print("="*70)
print(f"  观测 ρ_DE = {rde_obs:.3e} kg/m³")
print(f"  四种几何自然尺度给出离散倍数：")
for name,R,rd in rows:
    print(f"    {name:<24} → {rd/rde_obs:.2f}×")
best=min(rows,key=lambda t:abs(t[2]/rde_obs-1))
print(f"\n  最接近：{best[0]} = {best[2]/rde_obs:.2f} 倍（仍 O(1) 偏差，非精确闭合）")
print(f"  [判定] 视界定义是 O(1) 自由度：A1–A3 无法在四种尺度间做第一性选择")
print(f"         O1 不可从单一几何尺度第一性闭合（与攻破⑥ TUFT 同类：自由度改名）")
print(f"  出口：曲率半径最接近(1.9×)，但需 A4 几何-规范涌现或新原理给出唯一锚定")
