# -*- coding: utf-8 -*-
"""
v48：EF 球对称闭式 ODE 数值自洽验证（47 稿 λ',ν',τ'' 可积、行为合理）
用 47 稿闭式 ODE（含 τ 反馈）从近 Schwarzschild 弱毛初始条件数值积分：
检查解平滑、q=e^{-2λ} 行为（→1 渐近平坦趋向）、τ 演化合理。
θθ Einstein 由 Bianchi 恒等式（∇·G=0）+KG 自动保证，不单独核验。
"""
import json, numpy as np, sympy as sp
from scipy.integrate import solve_ivp

base = r"D:\a10\aikjx\code\my_lib\openuft\07_统一场方程\空间螺旋几何化统一场论"
d = json.load(open(base + r"\V3_18_ef_odes.json", encoding="utf-8"))
r, G, eta, m2, g, kappa = sp.symbols('r G eta m2 g kappa', real=True)
tauF = sp.Function('tau'); lamF = sp.Function('lam'); nuF = sp.Function('nu')
_locals = {'r':r,'G':G,'eta':eta,'m2':m2,'g':g,'kappa':kappa,'tau':tauF,'nu':nuF,'lam':lamF}
lam1e = sp.sympify(d["lam1"], locals=_locals)
nu1e  = sp.sympify(d["nu1"],  locals=_locals)
t2e   = sp.sympify(d["tau2"], locals=_locals)

Gv, kappav, etav, m2v, gv = 1.0, 8*np.pi, 0.05, 0.5, 0.1
tpv, e2v = sp.symbols('tpv e2v', real=True)
from sympy.utilities.lambdify import lambdify as _lamb
def mkfun(expr):
    exprN = expr.subs({G:Gv, eta:etav, m2:m2v, g:gv, kappa:kappav})
    exprN = exprN.subs({sp.Derivative(tauF(r),r):tpv, sp.Symbol('tpr'):tpv, sp.exp(2*lamF(r)):e2v})
    return _lamb((r, tauF(r), tpv, e2v), exprN, 'numpy')
lam1f=mkfun(lam1e); nu1f=mkfun(nu1e); t2f=mkfun(t2e)

def rhs(tt_, y):
    nu_, ta_, p_, q_ = y
    e2=1.0/q_
    return [nu1f(tt_,ta_,p_,e2), p_, t2f(tt_,ta_,p_,e2), -2*q_*lam1f(tt_,ta_,p_,e2)]

# 手动测各分量
e2t=1.0/(1-2.0/2.5)
for nm,fn in [("lam1",lam1f),("nu1",nu1f),("t2",t2f)]:
    try:
        print(nm,"=",fn(2.5,0.01,0.001,e2t))
    except Exception as ex:
        print(nm,"ERR:",ex)

r0, Rm = 2.5, 15.0
tau0, p0 = 0.01, 0.001
q0 = 1-2.0/r0
nu0 = 0.5*np.log(1-2.0/r0)
y0=[nu0, tau0, p0, q0]
sol = solve_ivp(rhs, [r0,Rm], y0, method='RK45', rtol=1e-9, atol=1e-12, max_step=0.05)
print("积分成功:", sol.status==0, " 点数:", sol.y.shape[1])
# 采样输出
idxs = np.linspace(0, sol.y.shape[1]-1, 6).astype(int)
print(" r        nu        tau       p         q")
for i in idxs:
    print(" %-7.3f %-9.4f %-9.5f %-9.3e %-9.4f" % (sol.t[i], sol.y[0,i], sol.y[1,i], sol.y[2,i], sol.y[3,i]))
# 自洽指标：τ 是否平滑、q 是否单调趋1、p 是否衰减
q_last=sol.y[3,-1]; tau_last=sol.y[1,-1]
print("final: q=%.4f (Schwarzschild 渐近=1), τ=%.4f, |p|=%.2e" % (q_last, tau_last, abs(sol.y[2,-1])))
rec = {"ode": "EF 闭式 RK45 r0=2.5→15, 弱毛(0.01,0.001)",
       "final_q": float(q_last), "final_tau": float(tau_last),
       "smooth": bool(np.isfinite(sol.y).all()),
       "caveats": ["弱毛积分自洽检查，非完整黑洞解", "θθ/Bianchi 由恒等式保证"]}
import io
with io.open(base + r"\V3_18b_ode_consistency.json","w",encoding="utf-8") as f:
    json.dump(rec, f, ensure_ascii=False, indent=2)
print("saved V3_18b_ode_consistency.json")
