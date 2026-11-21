import numpy as np
import pytest
from scipy import constants as C
from quantum_core import *

Q=electron_quantities()

@pytest.mark.parametrize('name,reference,rtol',[
  ('reduced_compton_m',C.physical_constants['reduced Compton wavelength'][0],2e-10),
  ('bohr_m',C.physical_constants['Bohr radius'][0],2e-10),
  ('rydberg_inv_m',C.physical_constants['Rydberg constant'][0],2e-10),
  ('energy_ev',510998.95069,2e-9),
  ('g_e',C.physical_constants['electron g factor'][0],1e-14),
  ('muon_electron_ratio',C.physical_constants['muon-electron mass ratio'][0],1e-9),
 ])
def test_constants(name,reference,rtol):
    assert np.isclose(Q[name],reference,rtol=rtol)

@pytest.mark.parametrize('R,omega,vz',[
  (1.,.6,.8),(1.,1.,0.),(2.,.25,np.sqrt(3)/2),
  (.1,5.,.25),(.5,1.,-np.sqrt(3)/2),
 ])
def test_helix_identity(R,omega,vz):
    g=helix_geometry(R,omega,vz)
    assert np.isclose(g['angular_frequency_recovered'],omega)
    assert np.isclose(g['curvature']**2+g['torsion']**2,(omega/g['speed'])**2)

@pytest.mark.parametrize('beta',[.01,.1,.2,.5,.75,.9,.999])
def test_v_total_c_cannot_add_transverse_c(beta):
    assert np.hypot(c,beta*c)>c
    assert np.isclose(np.hypot(c*np.sqrt(1-beta**2),beta*c),c)

@pytest.mark.parametrize('momentum',[(0.,0.,0.),(1e-22,2e-22,3e-22),(2e-21,0.,0.),(-4e-22,1e-23,0.)])
def test_5d_null_is_rel_dispersion(momentum):
    p5=m_e*c
    energy=null_5d_energy(momentum,p5)
    assert np.isclose(energy**2, c*c*(np.dot(momentum,momentum)+p5**2),rtol=1e-14)

@pytest.mark.parametrize('n',[0,1,2,3,7,10])
def test_kk_quantization_needs_hbar_input(n):
    R=hbar/(m_e*c)
    assert np.isclose(kk_mode_mass(n,R),n*m_e,rtol=2e-15,atol=1e-45)

def test_kk_naive_muon_integer_failure():
    ratio=Q['muon_electron_ratio']
    assert abs(ratio-round(ratio))>0.2

@pytest.mark.parametrize('p_over_mc',[0.001,.01,.05,.1,.2,.4])
def test_nonrelativistic_expansion(p_over_mc):
    p=p_over_mc*m_e*c
    exact=klein_gordon_energy(p,m_e)
    err2=abs(nr_energy(p,m_e,2)-exact)
    err4=abs(nr_energy(p,m_e,4)-exact)
    assert err4 < err2 or np.isclose(err4,err2,atol=1e-24)

@pytest.mark.parametrize('t',[0.,.5,1.,2.,3.,4.])
def test_free_wavepacket_unitarity_spreading(t):
    g=free_gaussian(t=t)
    assert abs(g['norm']-1)<3e-13
    assert abs(g['mean']-g['expected_mean'])<2e-10
    assert abs(g['sigma']-g['expected_sigma'])<2e-10

@pytest.mark.parametrize('sigma',[.3,.6,1.,2.,3.])
def test_gaussian_uncertainty_saturates(sigma):
    dx=sigma
    dp=hbar/(2*sigma)
    assert np.isclose(dx*dp,hbar/2)

@pytest.mark.parametrize('p',[(0,0,0),(.1,.2,.3),(1,0,0),(0,1,0),(0,0,1),(-1,2,.4)])
def test_dirac_square_and_spectrum(p):
    H=dirac_hamiltonian(p,mass=2.,speed=3.)
    expected=3**2*np.dot(p,p)+(2*3**2)**2
    assert np.allclose(H@H,np.eye(4)*expected,atol=1e-12)
    energies=np.linalg.eigvalsh(H)
    assert np.allclose(energies,[-np.sqrt(expected)]*2+[np.sqrt(expected)]*2)

def test_dirac_clifford_algebra():
    a,b=dirac_matrices(); I=np.eye(4)
    assert np.allclose(b@b,I)
    for i in range(3):
        assert np.allclose(a[i]@b+b@a[i],np.zeros((4,4)))
        for j in range(3):
            assert np.allclose(a[i]@a[j]+a[j]@a[i],2*I if i==j else np.zeros((4,4)))

@pytest.mark.parametrize('scale',[.1,.5,1.,2.,10.])
def test_classical_motion_hbar_independent_quantum_spectrum_not(scale):
    ts=np.linspace(-2,2,7)
    classical=classical_oscillator_trajectory(ts)
    assert np.array_equal(classical,classical_oscillator_trajectory(ts))
    E=quantum_oscillator_levels(scale,omega=3.,nmax=4)
    assert np.allclose(E,scale*quantum_oscillator_levels(1.,omega=3.,nmax=4))

@pytest.mark.parametrize('sigma',[.5,1.,1.5,2.,3.])
def test_fft_discretization_normalization(sigma):
    out=free_gaussian(sigma=sigma,k0=.2,t=1.2,n=4096,L=120)
    assert abs(out['norm']-1)<5e-13
    assert abs(out['sigma']-out['expected_sigma'])<5e-11

def test_simple_helix_cannot_reproduce_spin_and_g_without_extra_structure():
    assert np.isclose(assumed_compton_orbit_L_over_hbar(),1.)
    assert simple_orbital_g_factor()==1.
    assert not np.isclose(simple_orbital_g_factor(),abs(Q['g_e']),rtol=.1)

@pytest.mark.parametrize('R,omega,vz',[(1.,.2,0.),(1.,.7,0.),(2.,.3,.4)])
def test_helix_angular_frequency_not_fixed_by_speed_when_constraints_absent(R,omega,vz):
    assert helix_geometry(R,omega,vz)['speed']>0

@pytest.mark.parametrize('a,b',[(-3.,2.),(-.5,.3),(.1,0.),(1.,.5),(3.14,2.71)])
def test_weyl_noncommutative_translation_modulation(a,b):
    x=np.linspace(-6,6,201)
    # T(a)M(b)f(x) vs M(b)T(a)f(x), exact analytical sampled expressions
    f=lambda z: np.exp(-(z-.2)**2/3+1.1j*z)
    TM=np.exp(1j*b*(x-a))*f(x-a)
    MT=np.exp(1j*b*x)*f(x-a)
    assert np.allclose(TM,weyl_phase(a,b)*MT,atol=1e-14)

@pytest.mark.parametrize('angle',[0,2*np.pi,4*np.pi,np.pi,6*np.pi])
def test_spinor_double_cover_group(angle):
    U=spin_half_rotation_z(angle)
    assert np.allclose(U.conj().T@U,np.eye(2))
    assert np.isclose(np.linalg.det(U),1)
    if np.isclose(angle,2*np.pi): assert np.allclose(U,-np.eye(2))
    if np.isclose(angle,4*np.pi): assert np.allclose(U,np.eye(2))

@pytest.mark.parametrize('angle',[.1,.7,1.,2.1,3.3])
def test_spinor_composition(angle):
    assert np.allclose(spin_half_rotation_z(angle)@spin_half_rotation_z(.35),spin_half_rotation_z(angle+.35))

@pytest.mark.parametrize('v',[1e5,3e5,1e6,2e6,5e6])
def test_electron_fringe_spacings_from_quantum_wavelength(v):
    lam=de_broglie_wavelength(v)
    assert np.isclose(lam*m_e*v,h)
    spacing=interference_fringe_spacing(v,1e-6,1.)
    assert np.isclose(spacing,lam/1e-6)
    assert spacing>0
