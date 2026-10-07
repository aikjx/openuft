# -*- coding: utf-8 -*-
"""O-P1 攻破：复核 28 号 C03/B03「螺旋切矢场旋度纯轴向」论断
螺旋公设 ωρ=c 的切矢场（作为空间场）: T = (v⊥φ̂ + vz ẑ)/c = (-ωy/c, ωx/c, vz/c)
c = sqrt(ω²(x²+y²)+vz²)
验证 ∇×T 的完整三分量（数值中心差分 vs 解析闭式），重点: 是否存在环向 φ̂ 分量
"""
import numpy as np
w, vz = 1.0, 1.0

def T(x,y,z):
    c=np.sqrt(w**2*(x*x+y*y)+vz**2)
    return np.array([-w*y/c, w*x/c, vz/c])

def curl_num(p, h=1e-6):
    x,y,z=p
    def comp(i,j,k):  # (curl)_i = ∂_j T_k - ∂_k T_j
        epj, epk=np.zeros(3),np.zeros(3)
        epj[j]=1; epk[k]=1
        Tj_p=T(x+h*epj[0],y+h*epj[1],z+h*epj[2]); Tj_m=T(x-h*epj[0],y-h*epj[1],z-h*epj[2])
        Tk_p=T(x+h*epk[0],y+h*epk[1],z+h*epk[2]); Tk_m=T(x-h*epk[0],y-h*epk[1],z-h*epk[2])
        return (Tj_p[k]-Tj_m[k])/(2*h)-(Tk_p[j]-Tk_m[j])/(2*h)
    return np.array([comp(0,1,2),comp(1,2,0),comp(2,0,1)])

def curl_ana(x,y,z):
    r=np.sqrt(x*x+y*y); c=np.sqrt(w**2*r*r+vz**2)
    cr=0.0
    cphi= vz*w**2*r/c**3           # 环向 φ̂ 分量 = -∂_ρ T_z
    cz= (2*w)/c - w**3*r**2/c**3   # 轴向 ẑ 分量 = (1/ρ)∂_ρ(ρ T_φ)
    # 直角分量: φ̂=(-y/ρ,x/ρ,0), ẑ=(0,0,1)
    return np.array([cphi*(-y/r), cphi*(x/r), cz])

pts=[(0.5,0,0),(1,0,0),(2,0,0),(1,1,0),(3,0,1)]
print(f"螺旋切矢场 T=(-ωy/c,ωx/c,vz/c), ω={w}, vz={vz}, c=sqrt(ω²ρ²+vz²)")
print(f"{'点(ρ)':>10} | {'curl_数值(x,y,z)':>28} | {'curl_解析(x,y,z)':>28} | 环向|curl|")
for p in pts:
    cn=curl_num(p); ca=curl_ana(*p)
    r=np.sqrt(p[0]**2+p[1]**2)
    cphi_frac = ca[0]/(-p[1]/r) if abs(p[1])>1e-9 else ca[0]*0+ (ca[1]/(p[0]/r) if abs(p[0])>1e-9 else 0)
    mag=np.linalg.norm(ca)
    cphi = np.linalg.norm([ca[0]*( -p[1]/r), ca[1]*(p[0]/r)]) if r>1e-9 else 0
    print(f" ρ={r:>6.2f} | {np.round(cn,5)} | {np.round(ca,5)} | φ向={cphi:.4f}, 总={mag:.4f}")
print("\n结论: 螺旋切矢场旋度 ∇×T 的环向分量 = vz·ω²ρ/c³ ≠ 0（当 vz≠0）")
print("=> 28 号 C03/B03 称「纯轴向 1/ρ 场、无环向」不成立：T 自带轴向分量 vz/c（螺旋公设的一部分），其旋度给出环向螺线管型磁场。")
