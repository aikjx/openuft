"""ROOT V127: verifiable quantum mechanics / conditional helix diagnostics.
All helix-quantum identifications here are ASSUMPTIONS, not derived laws.
2022 CODATA constants via SciPy; no scientific data are fabricated.
"""
from __future__ import annotations
import numpy as np
from scipy import constants as C

h = C.h
hbar = C.hbar
c = C.c
G = C.G
m_e = C.physical_constants['electron mass'][0]
m_mu = C.physical_constants['muon mass'][0]
alpha_fs = C.physical_constants['fine-structure constant'][0]

def electron_quantities():
    energy_j = m_e*c*c
    omega_c = energy_j/hbar
    reduced_compton = hbar/(m_e*c)
    bohr = reduced_compton/alpha_fs
    rydberg = alpha_fs**2*m_e*c/(2*h)
    return dict(energy_j=energy_j, energy_ev=energy_j/C.e,
                omega_c=omega_c, reduced_compton_m=reduced_compton,
                bohr_m=bohr, rydberg_inv_m=rydberg,
                g_e=C.physical_constants['electron g factor'][0],
                muon_electron_ratio=m_mu/m_e,
                planck_length=np.sqrt(hbar*G/c**3),
                planck_mass=np.sqrt(hbar*c/G))

def helix_geometry(R, omega, vz):
    """Right-handed circular helix (R cos ωt,R sin ωt,v_z t)."""
    v = np.hypot(R*omega, vz)
    assert R > 0 and omega > 0 and v > 0
    curvature = R*omega**2/v**2
    torsion = vz*omega/v**2
    return dict(speed=v, curvature=curvature, torsion=torsion,
                angular_frequency_recovered=v*np.hypot(curvature, torsion),
                quantum_mass_if_postulated=hbar*omega/c**2)

def null_5d_energy(momentum_3d, p_fifth):
    """5D null dispersion: E^2 = c^2(|p_3|^2+p_5^2)."""
    return c*np.sqrt(np.sum(np.asarray(momentum_3d,dtype=float)**2)+p_fifth**2)

def kk_mode_mass(mode, radius):
    """Conditional, compact 5D massless scalar with m_n=|n|ħ/(Rc)."""
    if radius <= 0: raise ValueError('radius must be positive')
    return abs(mode)*hbar/(radius*c)

def klein_gordon_energy(p,m):
    return np.hypot(p*c,m*c*c)

def nr_energy(p,m,order=2):
    kinetic = p*p/(2*m)
    if order == 2: return m*c*c+kinetic
    if order == 4: return m*c*c+kinetic-p**4/(8*m**3*c*c)
    raise ValueError(order)

def free_gaussian(sigma=1.,x0=-5.,k0=2.,mass=1.,hbar_eff=1.,
                  t=2.,n=8192,L=80.):
    """FFT propagation of a normalized Gaussian; dimensionless test of Schr dynamics."""
    if sigma<=0 or mass<=0 or n<64 or L<=0: raise ValueError('invalid params')
    dx=L/n
    x=(np.arange(n)-n//2)*dx
    psi=np.exp(-(x-x0)**2/(4*sigma*sigma)+1j*k0*x)
    psi=psi/np.sqrt(np.sum(np.abs(psi)**2)*dx)
    k=2*np.pi*np.fft.fftfreq(n,d=dx)
    propagated=np.fft.ifft(np.fft.fft(psi)*np.exp(-1j*(hbar_eff*k*k/(2*mass))*t))
    norm=np.sum(np.abs(propagated)**2)*dx
    pdf=np.abs(propagated)**2
    xmean=np.sum(x*pdf)*dx
    xvar=np.sum((x-xmean)**2*pdf)*dx/norm
    expected_mean=x0+hbar_eff*k0*t/mass
    expected_sigma=np.sqrt(sigma**2+(hbar_eff*t/(2*mass*sigma))**2)
    return dict(norm=norm, mean=xmean, sigma=np.sqrt(xvar),
                expected_mean=expected_mean, expected_sigma=expected_sigma,
                x=x, probability=pdf)

def dirac_matrices():
    identity=np.eye(2,dtype=complex)
    zero=np.zeros((2,2),dtype=complex)
    sx=np.array([[0,1],[1,0]],dtype=complex)
    sy=np.array([[0,-1j],[1j,0]],dtype=complex)
    sz=np.array([[1,0],[0,-1]],dtype=complex)
    alphas=[np.block([[zero,s],[s,zero]]) for s in (sx,sy,sz)]
    beta=np.block([[identity,zero],[zero,-identity]])
    return alphas,beta

def dirac_hamiltonian(p, mass=1., speed=1.):
    alphas,beta=dirac_matrices()
    return speed*sum(float(pi)*ai for pi,ai in zip(p,alphas))+beta*mass*speed**2

def simple_orbital_g_factor():
    """Classical circulating charge with orbital angular momentum, |µ|/|L|=|q|/(2m)."""
    return 1.

def assumed_compton_orbit_L_over_hbar():
    """R=ħ/mc, v=c => L=mRv=ħ (not intrinsic spin 1/2)."""
    R=hbar/(m_e*c)
    return m_e*R*c/hbar

def classical_oscillator_trajectory(t,omega=1.,amp=1.):
    return amp*np.cos(omega*np.asarray(t))

def quantum_oscillator_levels(hbar_effective, omega=1.,nmax=6):
    return hbar_effective*omega*(np.arange(nmax)+0.5)

def weyl_phase(a,b,hbar_eff=1.):
    """Translation/modulation central phase T(a)M(b)=e^(-iab/ħ)M(b)T(a)."""
    return np.exp(-1j*a*b/hbar_eff)

def spin_half_rotation_z(angle):
    """Spin-1/2 rotation exp(-i θ σ_z/2), representation of SU(2)."""
    return np.diag([np.exp(-.5j*angle),np.exp(.5j*angle)])

def de_broglie_wavelength(v,m=m_e):
    """Nonrelativistic de Broglie formula, valid v << c."""
    if v<=0 or v>=.1*c: raise ValueError('Use only 0<v<0.1c')
    return h/(m*v)

def interference_fringe_spacing(v,slit_separation,screen_distance,m=m_e):
    """Far-field small-angle ideal two-slit spacing, nonrelativistic electron."""
    return de_broglie_wavelength(v,m)*screen_distance/slit_separation
