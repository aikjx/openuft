"""Independent fixed-step real RK4 wave-mode integrator to cross-check SciPy.

Does not import solve_ivp or the SciPy mode implementation. Uses only math.
"""
from math import sin, cos, sqrt, atan2, pi

def mode(k,lam,amp,omega,phase,T,helicity,steps=None):
    assert helicity in (-1,1)
    def dot(t):return amp*omega*cos(omega*t+phase)
    def ddot(t):return -amp*omega*omega*sin(omega*t+phase)
    w2=k*k+helicity*lam*k*dot(0)
    if w2<=0:raise ValueError('no initial WKB positive-frequency mode')
    w0=sqrt(w2); wp=helicity*lam*k*ddot(0)/(2*w0)
    a0=1/sqrt(2*w0)
    state=[a0,0.,-wp*a0/(2*w0),-w0*a0]
    N=steps or max(2400,int(T*k*45))
    dt=T/N
    def f(t,y):
        w2=k*k+helicity*lam*k*dot(t)
        return [y[2],y[3],-w2*y[0],-w2*y[1]]
    for i in range(N):
        t=i*dt
        a=f(t,state)
        b=f(t+dt/2,[state[j]+dt*a[j]/2 for j in range(4)])
        c=f(t+dt/2,[state[j]+dt*b[j]/2 for j in range(4)])
        d=f(t+dt,[state[j]+dt*c[j] for j in range(4)])
        state=[state[j]+dt*(a[j]+2*b[j]+2*c[j]+d[j])/6 for j in range(4)]
    return state

def phase_axis(k,lam,amp,omega,T,phase=0.,steps=None):
    a=mode(k,lam,amp,omega,phase,T,1,steps)
    b=mode(k,lam,amp,omega,phase,T,-1,steps)
    p=atan2(a[1],a[0])-atan2(b[1],b[0])
    p=atan2(sin(p),cos(p))
    return -p/2
