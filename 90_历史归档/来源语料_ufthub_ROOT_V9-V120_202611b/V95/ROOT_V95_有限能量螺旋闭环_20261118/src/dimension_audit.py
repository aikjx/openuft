"""SI base dimensions L, M, T, I; reject dimensionally inconsistent hypotheses."""
from dataclasses import dataclass
@dataclass(frozen=True)
class Dim:
    L:int=0; M:int=0; T:int=0; I:int=0
    def __mul__(self,o): return Dim(self.L+o.L,self.M+o.M,self.T+o.T,self.I+o.I)
    def __truediv__(self,o): return Dim(self.L-o.L,self.M-o.M,self.T-o.T,self.I-o.I)
    def __pow__(self,p): return Dim(self.L*p,self.M*p,self.T*p,self.I*p)
    def val(self):return [self.L,self.M,self.T,self.I]
ONE=Dim();L=Dim(L=1);M=Dim(M=1);T=Dim(T=1);I=Dim(I=1)
c=L/T;v=c;q=I*T; k=L**-1; omega=T**-1; m=M
B=M/(I*T**2); V=M*L**2/T**3/I; A=V*T/L
mu0=M*L/(I**2*T**2); eps0=I**2*T**4/(M*L**3); F=M*L/T**2
J=I/L**2; E=V/L; ener=M*L**2/T**2; G=L**3/(M*T**2); hbar=M*L**2/T
checks={
'omega=v*k':(omega,v*k),
'kappa=omega/v':(k,omega/v),
'B=gamma*m*v*kappa/q':(B,m*v*k/q),
'force=q*v*B':(F,q*v*B),
'force=gamma*m*v²*kappa':(F,m*v**2*k),
'A=B*xi':(A,B*L),
'B=curl(A)':(B,A/L),
'J=curl(B)/mu0':(J,B/L/mu0),
'U_B=integral B²/mu0 dV':(ener,B**2/mu0*L**3),
'P_rad=q²a²/(eps0 c³)':(ener/T,q**2*(L/T**2)**2/(eps0*c**3)),
'E_rad=P_rad*T':(ener,(ener/T)*T),
'G=c³/(hbar*kappa²)':(G,c**3/(hbar*k**2)),
'faraday=curl E=-dB/dt':(E/L,B/T),
'ampere=curl B=mu0*J':(B/L,mu0*J),
'lorentz=invariant gamma':(ONE,ONE),
'phase=energy*time/hbar':(ONE,ener*T/hbar),
'work=force*length':(ener,F*L),
'omega=charge*B/m':(omega,q*B/m),
'force=charge*E':(F,q*E),
'energy_density=B²/mu0':(ener/L**3,B**2/mu0),
'bad_G=c*kappa (wrong)':(G,c*k),
'bad_force=omega*kappa (wrong)':(F,omega*k),
'bad_G=c²*kappa/m (wrong)':(G,c**2*k/m),
'bad_Z_plus_Zprime_no_unit_match':(G*c,c/eps0),
}
def audit():
    return [{'equation':name,'lhs':a.val(),'rhs':b.val(),'pass':a==b} for name,(a,b) in checks.items()]
if __name__=='__main__':
    for row in audit(): print(row)
