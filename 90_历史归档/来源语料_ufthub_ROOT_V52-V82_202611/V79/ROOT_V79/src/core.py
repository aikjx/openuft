"""ROOT V79: auditable Einstein–Maxwell toy calculations. SI unless specified.
This does NOT derive G from c or constitute a new field discovery.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import cos, sin, pi, sqrt, atan2, isclose
from typing import Sequence
C=299_792_458.0
G=6.67430e-11
H=6.62607015e-34
HBAR=H/(2*pi)
EPS0=8.8541878188e-12  # approx measured epsilon0, not exact post-2019 SI
MU0=1/(EPS0*C*C)

def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def scale(k,a): return tuple(k*x for x in a)
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def energy_density(E,B): return (EPS0*dot(E,E)+dot(B,B)/MU0)/2
def invariants_SI(E,B):
    """I1=E²-c²B² [V²/m²], I2=E.B [V T/m]."""
    return dot(E,E)-C*C*dot(B,B), dot(E,B)
def poynting(E,B): return scale(1/MU0,cross(E,B))
def stress_energy(E,B):
    """T^{mu nu}, x0=ct, eta=(-+++), components J/m³."""
    u=energy_density(E,B); S=poynting(E,B)
    v=[[0.0]*4 for _ in range(4)]; v[0][0]=u
    for i in range(3):
        v[0][i+1]=v[i+1][0]=S[i]/C
        for j in range(3):
            v[i+1][j+1]=(u if i==j else 0)-EPS0*E[i]*E[j]-B[i]*B[j]/MU0
    return tuple(tuple(row) for row in v)
def lorentz_trace(T): return -T[0][0]+T[1][1]+T[2][2]+T[3][3]
def sphere_volume(a):
    if a<=0: raise ValueError('radius must be positive')
    return 4*pi*a**3/3
def magnetic_energy(B,a): return B*B*sphere_volume(a)/(2*MU0)
def induced_electric_energy(B_amplitude,f,a,phase=0.):
    """Quasistatic sphere; Ephi=-(rho/2) dB/dt. No global coil modelling."""
    if f<0: raise ValueError('negative frequency')
    bdot=-B_amplitude*2*pi*f*sin(phase)
    return EPS0*pi*a**5*bdot**2/15
def cycle_energy(B_amplitude,f,a,phase):
    return magnetic_energy(B_amplitude*cos(phase),a),induced_electric_energy(B_amplitude,f,a,phase)
def average_induced_ratio(f,a):
    if f<0 or a<=0: raise ValueError('invalid f or a')
    return (2*pi*f*a/C)**2/10
def quasi_static_parameter(f,a): return 2*pi*f*a/C

def fourier_amplitude(samples,n):
    """Return cosine/sine coefficients of harmonic n for samples over one period."""
    N=len(samples)
    if not N: raise ValueError('empty samples')
    if n==0: return sum(samples)/N,0.
    return (2/N*sum(y*cos(2*pi*n*k/N) for k,y in enumerate(samples)),
            2/N*sum(y*sin(2*pi*n*k/N) for k,y in enumerate(samples)))

def photon_invariant_mass(energies,directions):
    """Stable M²c⁴=2Σ_{i<j} EiEj(1-n_i·n_j). Energies in J."""
    if len(energies)!=len(directions) or not energies: raise ValueError('mismatch')
    if any(x<0 for x in energies): raise ValueError('negative energy')
    for d in directions:
        if not isclose(dot(d,d),1,rel_tol=1e-12,abs_tol=1e-12): raise ValueError('unit directions required')
    s=0.
    for i in range(len(energies)):
        for j in range(i+1,len(energies)):
            s+=2*energies[i]*energies[j]*max(0,1-dot(directions[i],directions[j]))
    return sqrt(s)/C**2

def mass_equivalent(U): return U/C**2
def monopole_g(added_energy,D):
    """Additional far-field scale ONLY for a net increase in closed-system energy."""
    if D<=0: raise ValueError('D must be positive')
    return G*added_energy/(C*C*D*D)
def quadrupole_strain_scale(delta_energy,a,f,D,shape=1.):
    """Order-of-magnitude estimate, not an actual sourced gravitational wave solution."""
    if a<=0 or D<=0 or f<0 or not 0<=shape<=1: raise ValueError('invalid input')
    source_omega=4*pi*f
    return 2*G/(C**4*D)*source_omega**2*shape*abs(delta_energy)*a*a/C**2

def parity_check(E,B):
    neg=scale(-1,B)
    A=stress_energy(E,B); Cminus=stress_energy(E,neg)
    return {'delta_u':energy_density(E,B)-energy_density(E,neg),
        'delta_tensor_max':max(abs(A[i][j]-Cminus[i][j]) for i in range(4) for j in range(4)),
        'I2_before':dot(E,B),'I2_after':dot(E,neg),
        'poynting_before':poynting(E,B),'poynting_after':poynting(E,neg)}

def oscillator_response(omega,omega0,damping,source):
    """Toy a''+2*damping*a'+omega0²*a=source*cos(omega*t)."""
    if omega<0 or omega0<=0 or damping<0: raise ValueError('invalid oscillator')
    den=sqrt((omega0**2-omega**2)**2+(2*damping*omega)**2)
    if den==0: raise ValueError('unbounded ideal resonance')
    return source/den,atan2(2*damping*omega,omega0**2-omega**2)
def quadratic_coupling_response(background,amplitude,xi):
    """f(a)=f0+xi*a²; first/second-harmonic cos amplitudes."""
    return 2*xi*background*amplitude,xi*amplitude**2/2

def inferred_Z(): return G*C/2

def G_fixed_Z(c_new): return 2*inferred_Z()/c_new

@dataclass(frozen=True)
class Scenario:
    B0_T:float=10.
    frequency_Hz:float=50.
    radius_m:float=1.
    distance_m:float=10.
    def evaluate(self):
        umax=magnetic_energy(self.B0_T,self.radius_m)
        avgb=umax/2
        avge=avgb*average_induced_ratio(self.frequency_Hz,self.radius_m)
        return dict(B0_T=self.B0_T,frequency_Hz=self.frequency_Hz,
            radius_m=self.radius_m,distance_m=self.distance_m,
            max_magnetic_J=umax,mean_magnetic_J=avgb,mean_induced_electric_J=avge,
            mean_equivalent_mass_kg=mass_equivalent(avgb+avge),
            net_energy_added_farfield_g_scale=monopole_g(avgb+avge,self.distance_m),
            induced_ratio=average_induced_ratio(self.frequency_Hz,self.radius_m),
            omega_a_over_c=quasi_static_parameter(self.frequency_Hz,self.radius_m),
            strain_scale=quadrupole_strain_scale(avgb,self.radius_m,self.frequency_Hz,self.distance_m))

def lorentz_boost_fields(E,B,v):
    """EM field components observed by frame moving at v relative to lab.
    E' = gamma(E+v×B) - gamma²/(gamma+1) v(v.E)/c²;
    B' = gamma(B-v×E/c²) - gamma²/(gamma+1) v(v.B)/c².
    """
    b2=dot(v,v)/C**2
    if b2>=1: raise ValueError('boost speed >= c')
    gam=1/sqrt(1-b2)
    k=gam**2/(gam+1)/(C*C)
    Ep=add(add(scale(gam,E),scale(gam,cross(v,B))),scale(-k*dot(v,E),v))
    Bp=add(add(scale(gam,B),scale(-gam/(C*C),cross(v,E))),scale(-k*dot(v,B),v))
    return Ep,Bp
