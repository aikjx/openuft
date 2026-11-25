"""Exact exponent algebra for ROOT V139 dimensions in c=1 units.
Dimensions recorded as (mass exponent M, length exponent L).
Time dimension is length since c=1. Unlike natural units, hbar and G are nontrivial.
"""
from dataclasses import dataclass
@dataclass(frozen=True)
class D:
    M:int=0
    L:int=0
    def __mul__(self,b):return D(self.M+b.M,self.L+b.L)
    def __truediv__(self,b):return D(self.M-b.M,self.L-b.L)
    def __pow__(self,n):return D(self.M*n,self.L*n)
M=D(1,0)
L=D(0,1)
hbar=M*L
G=L/M
R=L**-2
A=L**-1
F=L**-2
f=L**-1
coupling=D()
expected_density=M/L**3

def audit():
    ans={
      'hbar':hbar,
      'G':G,
      'Einstein_Hilbert_density':R/G,
      'Maxwell_density':hbar*(F**2)/(coupling**2),
      'Stueckelberg_density':hbar*(f**2)*(A**2),
      'force_E_times_kappa':M/L,
      'action_integrated':expected_density*L**4
    }
    assert all(ans[x]==expected_density for x in ('Einstein_Hilbert_density','Maxwell_density','Stueckelberg_density'))
    assert ans['action_integrated']==hbar
    return {k:{'mass_power':v.M,'length_power':v.L} for k,v in ans.items()}

if __name__=='__main__':
    import json
    print(json.dumps(audit(),indent=2))
