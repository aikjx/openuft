"""Independent symbolic derivations using SymPy (optional dependency)."""
import sympy as sp,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
G,M,d,s,a,lam,r,x,t,b,k,A=sp.symbols('G M d s a lam r x t b k A',positive=True)
C=G*M/2*((d-s)**-2+(d+s)**-2)
D=G*M/(2*s)*((d-s)**-2-(d+s)**-2)
checks={
 'mass_derivative':sp.simplify(sp.diff(C,M)-C/M)==0,
 'distance_derivative':sp.simplify(sp.diff(C,d)+G*M*((d-s)**-3+(d+s)**-3))==0,
 'baseline_derivative':sp.simplify(sp.diff(C,s)-G*M*((d-s)**-3-(d+s)**-3))==0,
 'gradient_from_two_sensors':sp.simplify((G*M*((d-s)**-2-(d+s)**-2)/(2*s))-D)==0,
 'ABBA_linear_drift':[sum(pv for pv in (1,-1,-1,1)),sum(i*pv for i,pv in enumerate((1,-1,-1,1))) ]==[0,0],
 'ABBA_quadratic_drift_nonzero':sum(i*i*pv for i,pv in enumerate((1,-1,-1,1)))!=0,
 'form_factor_zero_limit':sp.limit(3*(x*sp.cosh(x)-sp.sinh(x))/x**3,x,0)==1,
 'form_factor_small_x_series':sp.simplify(sp.series(3*(x*sp.cosh(x)-sp.sinh(x))/x**3,x,0,8).removeO()-(1+x**2/sp.Integer(10)+x**4/sp.Integer(280)+x**6/sp.Integer(15120)))==0,
 'finite_sphere_product_identity':sp.simplify(sp.expand((3*(x*sp.cosh(x)-sp.sinh(x))*sp.exp(-r/lam)/x**3-3*((x-1)*sp.exp(x-r/lam)+(x+1)*sp.exp(-x-r/lam))/(2*x**3)).rewrite(sp.exp)))==0,
 'Yukawa_acceleration_derivative':sp.simplify(sp.diff(sp.exp(-r/lam)/r,r)+sp.exp(-r/lam)*(1+r/lam)/r**2)==0,
 'Yukawa_long_range_radial':sp.limit((1+r/lam)*sp.exp(-r/lam),lam,sp.oo)==1,
 'Newton_far_baseline_limit':sp.limit(C*d*d/(G*M),d,sp.oo)==1,
}
output={'checks':checks,'passed':all(bool(v) for v in checks.values()),'count':len(checks)}
(R/'results'/'symbolic_report.json').write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf8')
print('SYMBOLIC CHECKS:',sum(checks.values()),'/',len(checks))
if not output['passed']:raise SystemExit('symbolic check failed: '+str(checks))
