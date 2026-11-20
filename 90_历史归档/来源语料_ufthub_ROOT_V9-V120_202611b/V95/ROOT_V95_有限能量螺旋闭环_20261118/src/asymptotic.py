"""Leading term of compact smooth tube B-energy for f(t)=exp(-t²/(1-t²))."""
import numpy as np
from scipy.constants import mu_0
from scipy.integrate import quad

def radial_integral():
    def integrand(t):
        if t>=1:return 0.
        f=np.exp(-t*t/(1-t*t))
        fp=-2*t*f/(1-t*t)**2
        return t**3*fp*fp
    return quad(integrand,0,1,epsabs=5e-14,epsrel=5e-14)[0]

def coefficient(model):
    G=model.length_integrals(384)
    return (np.pi/(4*mu_0))*(model.gamma*model.mass*model.v/model.charge)**2*G['kappa2ds_per_m']

def leading_energy(model):
    return coefficient(model)*model.eps**2

if __name__=='__main__':
    from finite_tube import TubeModel
    x=TubeModel()
    print('integral=',radial_integral(),'J/m² coefficient=',coefficient(x),
          'asymptotic energy J=',leading_energy(x))
