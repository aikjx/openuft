"""
MainAgent 独立裁决标量 l=0（v11）—— 纯数值直接打靶，不用连分数/E348/sympy。
龟坐标 RW: psi_{r*r*}+(w^2-V)psi=0, V=f(l(l+1)/r^2+2/r^3), f=1-2/r, M=1.
视界入射 psi=f^{-2iw} y(x), x=r-2, y=sum a_n x^n (数值 Frobenius)；
远场出射 psi=e^{iw r*} h, h=sum c_n r^{-n}, c0=1（数值 1/r 级数）；
两端积到匹配点 rm，Wronskian=0 求复根。DOP853 高容差。
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve

def horizon_coeffs(w,l,nmax=9):
    L=l*(l+1); a=-2j*w
    # p(x)=x fp(2a+1)/f = (2a+1)/(1+x/2) ; p_k=(2a+1)(-1/2)^k
    p=np.array([(2*a+1)*(-0.5)**k for k in range(nmax)],complex)
    # q(x)=4 w^2(1+x+x^2/4)+(1/4) B(x) H(x); B=4a^2-(4a+2L+2)x-L x^2; H_j=(j+1)(-1/2)^j
    H=np.array([(j+1)*(-0.5)**j for j in range(nmax)],complex)
    b=[4*a*a, -(4*a+2*L+2), -L]
    d=np.zeros(nmax,complex)
    for m in range(nmax):
        d[m]=sum(b[n]*H[m-n] for n in range(min(3,m+1)))/4
    q=d; q[0]+=4*w*w; q[1]+=4*w*w; q[2]+=w*w
    p0=p[0]; q0=q[0]
    A=np.zeros(nmax,complex); A[0]=1
    for n in range(1,nmax):
        Dn=n*(n-1)+p0*n+q0
        s=sum((p[k]*(n-k)+q[k])*A[n-k] for k in range(1,n+1))
        A[n]=-s/Dn
    return A

def infinity_coeffs(w,l,nmax=9):
    L=l*(l+1)
    # 级数方程(t=1/r): f=1-2t; H=sum c_n t^n
    # 收集 t^k 系数解 c_{k-1}。用多项式数组 conv。
    # f, f^2 系数
    f=np.array([1,-2],complex); f2=np.convolve(f,f)           # 1,-4,4
    # 通用：把各贡献按 t^k 的 c 依赖建线性递推。直接对每个 k 累加。
    c=np.zeros(nmax,complex); c[0]=1
    # 预先定义算子对级数 G=sum g_n t^n 的平移：
    # t^m G -> 系数 shift m。乘 poly P 用 conv。
    def apply(k_idx, c):
        # 返回 t^{k_idx} 方程中 [c_{k_idx-1} 的系数, 常数项(只含更低 c)]
        # 逐项构造，采用枚举所有 (项, f幂, 平移, H导阶)
        # 用符号化：构造 H,Ht,Htt 系数数组（关于 c），再卷积 f 多项式与 t 平移。
        pass
    # 直接数值：对当前已知 c，构造整方程级数 E(t)=... 的各阶，逐阶反解最高 c。
    # E = f2 t4 Htt + 2 f2 t3 Ht - 2iw f t2 Ht - 2 f t4 Ht - L f t2 H - 2 f t3 H
    wv=w
    for k in range(2,nmax+1):
        # t^k 系数；未知数最高为 c[k-1]（来自 -2iw f t2 Ht）
        # Ht coeff at t^{k-2}: (k-1)c_{k-1}; 乘 -2iw f(=1-2t)
        coef_new=-2j*wv*(k-1)                 # from f 的常数 1
        # 其余各项只用 c[0..k-2]
        const=0j
        # -2iw f t2 Ht 中 f 的 -2t 部分: Ht at t^{k-3}=(k-2)c_{k-2}, *(-2t)*(-2iw)
        if k-3>=0: const+= (-2j*wv)*(-2)*((k-2)*c[k-2])
        # T1 f2 t4 Htt: Htt at t^{k-4}=(k-2)(k-3)c_{k-2}; conv with f2
        for fi,fv in enumerate(f2):
            j=k-4-fi
            if 0<=j: const+= fv*((j+2)*(j+1))*c[j+2] if j+2<nmax else 0
        # T2 2 f2 t3 Ht: Ht at t^{k-3}=(j+1)c_{j+1}
        for fi,fv in enumerate(f2):
            j=k-3-fi
            if 0<=j and j+1<nmax: const+= 2*fv*((j+1)*c[j+1])
        # T4 -2 f t4 Ht: Ht t^{k-4}=(j+1)c_{j+1}
        for fi,fv in enumerate(f):
            j=k-4-fi
            if 0<=j and j+1<nmax: const+= -2*fv*((j+1)*c[j+1])
        # T5 -L f t2 H: H t^{k-2}=c_j
        for fi,fv in enumerate(f):
            j=k-2-fi
            if 0<=j: const+= -L*fv*c[j]
        # T6 -2 f t3 H: H t^{k-3}=c_j
        for fi,fv in enumerate(f):
            j=k-3-fi
            if 0<=j: const+= -2*fv*c[j]
        c[k-1]= -const/coef_new
    return c

def rstar(r): return r+2*np.log(r/2-1)

def shoot(omega,l,eps=2e-3,R=200.0,rm=5.0):
    w=complex(*omega); L=complex(l*(l+1)); al=-2j*w
    # 正则变量积分（全程 O(1)，避免 e^{|wI|r*} 增长淹没精度）
    A=horizon_coeffs(w,l)
    y0=sum(A[n]*eps**n for n in range(len(A)))
    dy0=sum(n*A[n]*eps**(n-1) for n in range(1,len(A)))
    C=infinity_coeffs(w,l)
    h0=sum(C[n]*R**-n for n in range(len(C)))
    dh0=-sum(n*C[n]*R**(-n-1) for n in range(1,len(C)))
    def sys_y(r,q):  # psi=f^al y
        ff=1-2/r; ffp=2/r**2; ffpp=-4/r**3
        NN=al*al*ffp*ffp+al*ff*ffpp+w*w-ff*(L/r**2+2/r**3)
        return [q[1], -(ffp/ff)*(2*al+1)*q[1]-(NN/ff**2)*q[0]]
    def sys_h(r,q):  # psi=e^{iw r*} h
        ff=1-2/r; ffp=2/r**2
        return [q[1], -(2j*w/ff+ffp/ff)*q[1]+(ff*(L/r**2+2/r**3)/ff**2)*q[0]]
    kw=dict(method='DOP853',rtol=1e-12,atol=1e-13)
    si=solve_ivp(sys_y,(2+eps,rm),[y0,dy0],**kw)
    so=solve_ivp(sys_h,(R,rm),[h0,dh0],**kw)
    y,dy=si.y[:,-1]; h,dh=so.y[:,-1]
    ff=1-2/rm; ffp=2/rm**2
    # W=0 去掉公共因子: y h' - y' h + (iw/f - al f'/f) y h
    G=y*dh-dy*h+(1j*w/ff-al*ffp/ff)*y*h
    return [G.real,G.imag]

if __name__=="__main__":
    seeds={0:(0.1105,-0.1049),1:(0.2929,-0.0977),2:(0.4836,-0.0968)}
    for l in (0,1,2):
        r0,info,ier,msg=fsolve(lambda z:shoot(z,l),seeds[l],full_output=True,xtol=1e-11,epsfcn=1e-9)
        print(f"l={l} direct-shoot = {r0[0]:.8f} {r0[1]:+.8f} i  nfev={info['nfev']} ier={ier}")
    print("E348 CF: l0 0.11045494/-0.10489571 ; table: 0.1104557/-0.104899")
