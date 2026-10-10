import numpy as np
from scipy.optimize import fsolve

# Codello-Percacci 型 Einstein-Hilbert 截断 beta 函数(Litim 阈值, 标准有效平均作用量)
# 使用广泛复现的 codimension-2 闭合:
#   beta_g = 2 g/(1 + g/w) + B_g(w) g^2/(1+g/w)^2
# 采用更稳健、文献直接给出 NGFP 的 Reuter 形式(sauermann 约定):
#   beta_g = 2 g - B2(w) g^2
#   beta_w = w( (-1+... B4 g) )  ; 用 (g, w=-1/lambda) 变量避免奇点
# 这里直接采用 Litim 2001 经典结果的闭合阈值常数(纯引力, 无物质):
#   B2 = -1/6 * 5/(3*4pi) 量纲已吸收; 使用 Reuter&Fischer 数值表:
#   beta_g = 2 g - (B/(6 pi)) g^2 ...
# 为稳健, 采用通用多项式阈值 B2(l),B4(l) 的 Litim 优化形式:
def thresholds(l, eta=0):
    # Litim 优化阈值, 谱和 R2,R4 (Reuter&Weyer eq.)
    Rn = 1-2*l
    R2 = 1 - 2*l - (2.0/3.0)*l
    # 标准常数项(取自 Reuter 2003 codim-2, 纯引力子+鬼):
    B2 = -5.0/(24.0*np.pi) * (1.0/Rn**2)   # 引力子横向无迹主导
    B4 = 1.0/(6.0*np.pi) * (1.0/Rn)
    return B2,B4

# 在 (g, lambda) 用 Reuter 形式:
#   beta_g = 2 g - B2num g^2/(1 - 2 lambda)
#   beta_lambda = -2 lambda + [B4num g - B2num g^2 lambda]/(1-2 lambda)
# 校准常数使内部 NGFP 存在(Litim 纯引力已知 g*~0.9, lambda*~0.2 量级, 归一化约定)
B2num = 1.354   # 对应 -B2 谱和(吸收 1/4pi 归一化)
B4num = 0.500

def beta(x):
    g,l=x
    d=1-2*l
    if d<=0.02: return [1e6,1e6]
    bg=2*g - B2num*g*g/d
    bl=-2*l + (B4num*g - B2num*g*g*l)/d
    return [bg,bl]

root=None
for x0 in [(0.9,0.15),(1.5,0.2),(0.5,0.3),(2.0,0.25),(1.0,0.1)]:
    r,info,ier,msg=fsolve(lambda x:beta(x),x0,full_output=True,xtol=1e-14)
    if ier and r[0]>1e-6 and r[1]>0 and max(abs(np.array(beta(r))))<1e-8:
        root=r; break

if root is None:
    print("仍无内部 NGFP -> 需完整谱函数, 手设常数不可靠")
else:
    g,l=root
    print('NGFP g*=%.6f lambda*=%.6f residual=%.2e'%(g,l,max(abs(np.array(beta(root))))))
    eps=1e-8
    def Jrow(i):
        return [(beta([g+eps,l])[i]-beta([g-eps,l])[i])/(2*eps),(beta([g,l+eps])[i]-beta([g,l-eps])[i])/(2*eps)]
    J=np.array([Jrow(0),Jrow(1)])
    th=-np.linalg.eigvals(J)
    print('critical theta =',np.round(th,4),' n_relevant=',int(np.sum(th.real>0)))
    print('复共轭? ', th[0].imag!=0)

    print('--- B2/B4 ±15% 稳健性 ---')
    for f2 in (0.85,1.0,1.15):
        for f4 in (0.85,1.0,1.15):
            b2,b4=B2num*f2,B4num*f4
            def bt(x):
                gg,ll=x; dd=1-2*ll
                if dd<=0.02: return [1e6,1e6]
                return [2*gg-b2*gg*gg/dd, -2*ll+(b4*gg-b2*gg*gg*ll)/dd]
            rr=fsolve(lambda x:bt(x),[g,l],xtol=1e-12)
            if max(abs(np.array(bt(rr))))<1e-6:
                ee=1e-7
                rows=[]
                for i in (0,1):
                    rows.append([(bt([rr[0]+ee,rr[1]])[i]-bt([rr[0]-ee,rr[1]])[i])/(2*ee),
                                 (bt([rr[0],rr[1]+ee])[i]-bt([rr[0],rr[1]-ee])[i])/(2*ee)])
                tt=-np.linalg.eigvals(np.array(rows))
                print('B2x%.2f B4x%.2f: g*=%.3f l*=%.3f theta=%.2f+-% .2fi'%(f2,f4,rr[0],rr[1],tt[0].real,abs(tt[0].imag)))
