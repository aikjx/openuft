import numpy as np
from scipy.integrate import solve_bvp, simpson

def solve(w,R=50,tol=1e-7,old=None,guessR=5):
 x=np.linspace(0,R,1001)
 def fun(r,y):
  f,v=y;return np.array([v,(1-w*w)*f-2*f**3+1.5*f**5])
 def bc(a,b):return np.array([a[1],b[1]+(np.sqrt(1-w*w)+1/R)*b[0]])
 if old is None:
  f=1.05/(1+np.exp(np.clip((x-guessR),-100,100))); y=np.array([f,-f*(1-f/1.05)])
 else:y=old.sol(x)
 return solve_bvp(fun,bc,x,y,S=np.array([[0.,0.],[0.,-2.]]),tol=tol,max_nodes=25000)

def stats(w,s,R):
 x=np.linspace(0,R,20001);f,v=s.sol(x);fac=4*np.pi*x*x
 U=.5*f*f-.5*f**4+.25*f**6
 T=simpson(fac*.5*w*w*f*f,x=x); K=simpson(fac*.5*v*v,x=x);V=simpson(fac*U,x=x);Q=2*T/w; E=T+K+V
 return s.status,f[0],Q,E/Q if Q else 0,(3*T-K-3*V)/E if E else 0
if __name__=='__main__':
 old=None
 for w in [.83,.82,.81,.80,.79,.78,.77,.76,.75,.74,.73]:
  s=solve(w,old=old); print(w,stats(w,s,50),len(s.x),flush=True)
  if s.success and abs(s.y[0,0])>.1:old=s
