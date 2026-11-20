"""ROOT V95. Compactly supported Maxwell magnetic inverse design, test-particle limit.

All lengths SI meters. u dimensionless, s arclength. It constructs a smooth
stationary external B in a tubular neighbourhood of an embedded closed curve.
It is NOT a self-consistent radiation-reaction, source-coil, or quantum model.
"""
from __future__ import annotations
import numpy as np
from scipy.constants import c, mu_0, epsilon_0, e, m_e
from scipy.optimize import brentq
from scipy.spatial import cKDTree
from scipy.integrate import solve_ivp

R0=.010; A0=.002; M0=2; N0=3; BETA0=.8

class TubeModel:
    def __init__(self,R=R0,a=A0,m=M0,n=N0,beta=BETA0,eps=.0003,charge=-e,mass=m_e, samples=3000):
        assert R>a>0 and int(m)==m and int(n)==n and 0<beta<1 and eps>0 and charge!=0
        self.R,self.a,self.m,self.n=R,a,int(m),int(n)
        self.beta,self.v,self.gamma=beta,beta*c,1/np.sqrt(1-beta**2)
        self.eps,self.charge,self.mass=eps,charge,mass
        self.u_points=np.linspace(0,2*np.pi,samples,endpoint=False)
        self.tree=cKDTree(self.curve(self.u_points)[0])

    def curve(self,u):
        u=np.asarray(u,dtype=float)
        theta=self.m*u; C=np.cos(theta); S=np.sin(theta)
        cn=np.cos(self.n*u); sn=np.sin(self.n*u)
        rho=self.R+self.a*cn
        rp=-self.a*self.n*sn
        rpp=-self.a*self.n**2*cn
        X=np.stack((rho*C,rho*S,self.a*sn),axis=-1)
        Xu=np.stack((rp*C-self.m*rho*S,rp*S+self.m*rho*C,self.a*self.n*cn),axis=-1)
        Xuu=np.stack(((rpp-self.m**2*rho)*C-2*self.m*rp*S,
                       (rpp-self.m**2*rho)*S+2*self.m*rp*C,
                       -self.a*self.n**2*sn),axis=-1)
        return X,Xu,Xuu

    def geometry(self,u):
        X,Xu,Xuu=self.curve(u)
        speed=np.linalg.norm(Xu,axis=-1)
        T=Xu/speed[...,None]
        dot=np.sum(Xu*Xuu,axis=-1)
        K=Xuu/speed[...,None]**2-Xu*dot[...,None]/speed[...,None]**4
        kappa=np.linalg.norm(K,axis=-1)
        B0=(self.gamma*self.mass*self.v/self.charge)*np.cross(K,T)
        return X,T,K,B0,speed,kappa

    def bump(self,rho):
        rho=np.asarray(rho,dtype=float)
        z=rho/self.eps
        ok=z<1
        chi=np.zeros_like(z)
        chip=np.zeros_like(z)
        t=1-z[ok]**2
        chi[ok]=np.exp(1-1/t)
        chip[ok]=chi[ok]*(-2*rho[ok]/self.eps**2)/(t*t)
        return chi,chip

    def field_chart(self,u,xi):
        """B(x) at x=X(u)+xi, xi perpendicular T; valid inside embedded tube."""
        X,T,K,B0,_,_=self.geometry(u)
        xi=np.asarray(xi)
        rho=np.linalg.norm(xi,axis=-1)
        chi,chip=self.bump(rho)
        D=1-np.sum(xi*K,axis=-1)
        if np.any(D<=0): raise ValueError('Outside tubular uniqueness radius')
        B=chi[...,None]*(B0*(2-1/D)[...,None]+xi*(np.sum(B0*K,axis=-1)/D)[...,None])
        F=np.zeros_like(B)
        mask=rho>0
        if np.any(mask):
            ff=chip[...,None]*(rho[...,None]*B0-xi*(np.sum(B0*xi,axis=-1)/np.where(mask,rho,1))[...,None])
            F=np.where(mask[...,None],ff,0)
        return B+F

    def potential_chart(self,u,xi):
        _,_,_,B0,_,_=self.geometry(u)
        chi,_=self.bump(np.linalg.norm(xi,axis=-1))
        return chi[...,None]*np.cross(B0,xi)

    def point_geometry(self,x,u_guess=None):
        x=np.asarray(x,dtype=float)
        if u_guess is None: _,i=self.tree.query(x); u=float(self.u_points[i])
        else: u=float(u_guess)
        for _ in range(10):
            X,Xu,Xuu=self.curve(u); delta=x-X
            f=np.dot(delta,Xu)
            fp=-np.dot(Xu,Xu)+np.dot(delta,Xuu)
            step=f/fp
            u-=step
            if abs(step)<1e-14: break
        X,_,_=self.curve(u)
        return u,x-X

    def field(self,x):
        x=np.asarray(x,dtype=float)
        _,i=self.tree.query(x)
        if np.linalg.norm(x-self.curve(self.u_points[i])[0])>self.eps*1.015: return np.zeros(3)
        u,xi=self.point_geometry(x,u_guess=self.u_points[i])
        if np.linalg.norm(xi)>=self.eps:return np.zeros(3)
        return self.field_chart(u,xi)

    def potential(self,x):
        x=np.asarray(x,dtype=float)
        _,i=self.tree.query(x)
        if np.linalg.norm(x-self.curve(self.u_points[i])[0])>self.eps*1.015:return np.zeros(3)
        u,xi=self.point_geometry(x,u_guess=self.u_points[i])
        if np.linalg.norm(xi)>=self.eps:return np.zeros(3)
        return self.potential_chart(u,xi)

    def curl_potential_numeric(self,x,h=2e-7):
        E=np.eye(3)
        d=np.column_stack([(self.potential(x+h*E[j])-self.potential(x-h*E[j]))/(2*h) for j in range(3)])
        return np.array([d[2,1]-d[1,2],d[0,2]-d[2,0],d[1,0]-d[0,1]])

    def divergence_B_numeric(self,x,h=2e-7):
        E=np.eye(3)
        return sum((self.field(x+h*E[j])[j]-self.field(x-h*E[j])[j])/(2*h) for j in range(3))

    def energy(self,nu=144,nr=22,nphi=36):
        """Gauss-Legendre transverse tube quadrature, static B field energy, J."""
        from numpy.polynomial.legendre import leggauss
        un,uw=leggauss(nu); u=np.pi*(un+1); wu=np.pi*uw
        rn,rw=leggauss(nr); rho=(rn+1)*self.eps/2; wr=rw*self.eps/2
        phi=(np.arange(nphi)+.5)*2*np.pi/nphi
        X,T,K,B0,spd,kap=self.geometry(u)
        N=K/kap[:,None]; H=np.cross(T,N)
        rad=rho[None,:,None,None]*(np.cos(phi)[None,None,:,None]*N[:,None,None,:]
              +np.sin(phi)[None,None,:,None]*H[:,None,None,:])
        chi,chip=self.bump(rho)
        D=1-np.sum(rad*K[:,None,None,:],axis=-1)
        b=chi[None,:,None,None]*(B0[:,None,None,:]*(2-1/D)[...,None]
              +rad*(np.sum(B0[:,None,None,:]*K[:,None,None,:],axis=-1)/D)[...,None])
        b+=chip[None,:,None,None]*(rho[None,:,None,None]*B0[:,None,None,:]
              -rad*(np.sum(B0[:,None,None,:]*rad,axis=-1)/rho[None,:,None])[...,None])
        integrand=np.sum(b*b,axis=-1)/(2*mu_0)*D*spd[:,None,None]*rho[None,:,None]
        return float(np.einsum('ijk,i,j->',integrand,wu,wr)*(2*np.pi/nphi))

    def length_integrals(self,nodes=512):
        from numpy.polynomial.legendre import leggauss
        xx,ww=leggauss(nodes); u=np.pi*(xx+1); w=ww*np.pi
        _,_,_,_,spd,kap=self.geometry(u)
        length=float(np.sum(w*spd))
        k2ds=float(np.sum(w*spd*kap**2))
        period=length/self.v
        e_rad=(self.charge**2*self.gamma**4*self.v**3/(6*np.pi*epsilon_0*c**3))*k2ds
        return dict(length_m=length, kappa2ds_per_m=k2ds, period_s=period,
                    radiation_energy_j=e_rad,
                    kinetic_j=(self.gamma-1)*self.mass*c**2,
                    min_B_T=float(np.min(np.linalg.norm(self.geometry(np.linspace(0,2*np.pi,4001))[3],axis=-1))),
                    max_B_T=float(np.max(np.linalg.norm(self.geometry(np.linspace(0,2*np.pi,4001))[3],axis=-1))))

    def trajectory(self,perturb=None,rtol=2e-9):
        info=self.length_integrals(160)
        period=info['period_s']; charge_over_mass=self.charge/(self.gamma*self.mass)
        X,T,*_=self.geometry(0.)
        pos=X.copy(); direc=T.copy()
        if perturb is not None: pos=pos+np.asarray(perturb)
        state0=np.r_[pos/self.R,direc]
        def f(theta,y):
            x=y[:3]*self.R; w=y[3:]
            B=self.field(x)
            return np.r_[(period*self.v/self.R)*w,period*charge_over_mass*np.cross(w,B)]
        solution=solve_ivp(f,[0,1],state0,method='DOP853',rtol=rtol,atol=rtol*0.1,max_step=1/300)
        end=solution.y[:,-1]
        return dict(success=bool(solution.success),steps=int(len(solution.t)),
                    position_error_m=float(np.linalg.norm((end[:3]-state0[:3])*self.R)),
                    tangent_error=float(np.linalg.norm(end[3:]-state0[3:])),
                    speed_drift=float(np.max(np.abs(np.linalg.norm(solution.y[3:],axis=0)-1))),
                    end_position_m=(end[:3]*self.R).tolist())
