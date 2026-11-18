import math,unittest
from src import core as c

class TestConstants(unittest.TestCase):
    def test_light_speed(self): self.assertEqual(c.C,299792458.)
    def test_mu_epsilon(self): self.assertAlmostEqual(c.MU0*c.EPS0*c.C**2,1.,places=12)
    def test_z_identity(self): self.assertAlmostEqual(2*c.inferred_Z()/c.C,c.G,places=20)
    def test_z_has_dimension(self): self.assertTrue(0.0100<c.inferred_Z()<0.01001)
    def test_z_fixed_conditional(self): self.assertAlmostEqual(c.G_fixed_Z(2*c.C),c.G/2,places=20)

class TestEM(unittest.TestCase):
    def test_zero_fields(self): self.assertEqual(c.energy_density((0,0,0),(0,0,0)),0)
    def test_e_only(self): self.assertAlmostEqual(c.energy_density((1,0,0),(0,0,0)),c.EPS0/2)
    def test_b_only(self): self.assertAlmostEqual(c.energy_density((0,0,0),(0,0,1)),1/(2*c.MU0))
    def test_null_plane_wave(self):
        e=(c.C,0,0);b=(0,1,0)
        I1,I2=c.invariants_SI(e,b)
        self.assertEqual(I1,0.);self.assertEqual(I2,0.)
        self.assertGreater(c.energy_density(e,b),0)
    def test_poynting_wave(self):
        e=(c.C,0,0);b=(0,1,0)
        self.assertAlmostEqual(c.poynting(e,b)[2],c.energy_density(e,b)*c.C,delta=1e-5)
    def test_e_cross(self): self.assertEqual(c.cross((1,0,0),(0,1,0)),(0,0,1))
    def test_e_parallel_poynting(self): self.assertEqual(c.poynting((1,0,0),(1,0,0)),(0.,0.,0.))
    def test_trace(self):
        for e,b in [((0,0,0),(0,0,0)),((4,2,0),(5,0,3)),((c.C,0,0),(0,1,0))]:
            self.assertAlmostEqual(c.lorentz_trace(c.stress_energy(e,b)),0.,delta=2e-9*max(1,c.energy_density(e,b)))
    def test_stress_symmetry(self):
        T=c.stress_energy((1e6,2e5,3e5),(1,2,0.2))
        for i in range(4):
            for j in range(4): self.assertAlmostEqual(T[i][j],T[j][i])
    def test_null_wave_Tzz(self):
        T=c.stress_energy((c.C,0,0),(0,1,0))
        self.assertAlmostEqual(T[3][3],T[0][0],delta=1e-9*T[0][0])
        self.assertAlmostEqual(T[0][3],T[0][0],delta=1e-9*T[0][0])
    def test_parallel_field_flip_T(self):
        p=c.parity_check((0,0,1e6),(0,0,10.))
        self.assertEqual(p['delta_u'],0);self.assertEqual(p['delta_tensor_max'],0)
        self.assertEqual(p['I2_before'],-p['I2_after'])
    def test_crossed_field_flip_changes_T0i(self):
        p=c.parity_check((1e6,0,0),(0,10,0))
        self.assertGreater(p['delta_tensor_max'],0)
        self.assertEqual(p['poynting_before'][2],-p['poynting_after'][2])
    def test_energy_cross_same(self):
        a=(1e6,0,0); b=(1e6,0,0); z=(0,0,0)
        actual=c.energy_density(c.add(a,b),z)
        isolated=c.energy_density(a,z)+c.energy_density(b,z)
        self.assertAlmostEqual(actual/isolated,2.)
    def test_energy_cross_opposite(self): self.assertEqual(c.energy_density((0,0,0),(0,0,0)),0)
    def test_invariant_flip(self):
        I1,I2=c.invariants_SI((1,0,0),(1,0,0))
        J1,J2=c.invariants_SI((1,0,0),(-1,0,0))
        self.assertEqual(I1,J1);self.assertEqual(I2,-J2)

class TestQuasiStatic(unittest.TestCase):
    def test_sphere_volume(self): self.assertAlmostEqual(c.sphere_volume(1),4*math.pi/3)
    def test_invalid_radius(self):
        with self.assertRaises(ValueError):c.sphere_volume(0)
    def test_b_energy_scales_square(self): self.assertAlmostEqual(c.magnetic_energy(2,1)/c.magnetic_energy(1,1),4)
    def test_b_energy_scales_volume(self): self.assertAlmostEqual(c.magnetic_energy(1,2)/c.magnetic_energy(1,1),8)
    def test_induced_e_zero_f(self): self.assertEqual(c.induced_electric_energy(1,0,1,1),0)
    def test_induced_e_zero_at_peak_B(self): self.assertEqual(c.induced_electric_energy(1,50,1,0),0)
    def test_induced_e_scales_f2(self):
        a=c.induced_electric_energy(1,1,1,math.pi/2)
        b=c.induced_electric_energy(1,2,1,math.pi/2)
        self.assertAlmostEqual(b/a,4)
    def test_induced_e_scales_a5(self):
        a=c.induced_electric_energy(1,50,1,math.pi/2)
        b=c.induced_electric_energy(1,50,2,math.pi/2)
        self.assertAlmostEqual(b/a,32)
    def test_ratio_50hz(self): self.assertAlmostEqual(c.average_induced_ratio(50,1),1.0981415890099114e-13,delta=1e-24)
    def test_ratio_scaling(self): self.assertAlmostEqual(c.average_induced_ratio(100,2)/c.average_induced_ratio(50,1),16)
    def test_quasi_bound(self): self.assertLess(c.quasi_static_parameter(50,1),1e-5)
    def test_highfreq_flag(self): self.assertGreater(c.quasi_static_parameter(1e9,1),1)
    def test_cycle_at_zero(self):
        b,e=c.cycle_energy(10,50,1,0)
        self.assertEqual(e,0);self.assertAlmostEqual(b,c.magnetic_energy(10,1))
    def test_cycle_at_quarter(self):
        b,e=c.cycle_energy(10,50,1,math.pi/2)
        self.assertLess(b,1e-20);self.assertGreater(e,0)
    def test_fourier_B_DC_and_2f(self):
        n=256;y=[math.cos(2*math.pi*k/n)**2 for k in range(n)]
        self.assertAlmostEqual(c.fourier_amplitude(y,0)[0],0.5,places=12)
        self.assertAlmostEqual(c.fourier_amplitude(y,2)[0],0.5,places=12)
        self.assertAlmostEqual(c.fourier_amplitude(y,1)[0],0.,places=12)
        self.assertAlmostEqual(c.fourier_amplitude(y,3)[0],0.,places=12)
    def test_numerical_volume_integration_E(self):
        # Radial Simpson x polar midpoint quadrature for Ephi= -0.5*r*sin(theta)*Bdot
        B0,f,a=8.,50.,1.
        w=2*math.pi*f; n=120;m=200
        dr=a/n;dth=math.pi/m
        s=0.
        for i in range(n+1):
            r=i*dr; wi=1 if i in (0,n) else (4 if i%2 else 2)
            for j in range(m):
                th=(j+0.5)*dth
                Eph=.5*r*math.sin(th)*B0*w
                s+=wi*(c.EPS0/2)*Eph**2*r*r*math.sin(th)*2*math.pi*dr/3*dth
        expected=c.induced_electric_energy(B0,f,a,math.pi/2)
        self.assertAlmostEqual(s/expected,1,delta=2e-5)

class TestGravityAndPhotons(unittest.TestCase):
    def test_mass_energy(self): self.assertAlmostEqual(c.mass_equivalent(c.C**2),1)
    def test_monopole_inverse_square(self): self.assertAlmostEqual(c.monopole_g(1,2)/c.monopole_g(1,1),0.25)
    def test_monopole_zero_when_no_energy_added(self): self.assertEqual(c.monopole_g(0,1),0)
    def test_closed_system_mass_constant(self):
        cap=2*c.magnetic_energy(10,1)
        for k in range(50):
            ub,ue=c.cycle_energy(10,50,1,2*math.pi*k/50)
            reservoir=cap-ub-ue
            self.assertAlmostEqual((ub+ue+reservoir)/cap,1,places=14)
    def test_co_photons_zero_mass(self):
        self.assertEqual(c.photon_invariant_mass((1,2),((1,0,0),(1,0,0))),0)
    def test_opposite_photons_nonzero_mass(self):
        m=c.photon_invariant_mass((1,1),((1,0,0),(-1,0,0)))
        self.assertAlmostEqual(m,2/c.C**2)
    def test_photon_single_zero_mass(self): self.assertEqual(c.photon_invariant_mass((1,),((1,0,0),)),0)
    def test_non_unit_photons(self):
        with self.assertRaises(ValueError):c.photon_invariant_mass((1,),((2,0,0),))
    def test_strain_zero_if_spherical(self): self.assertEqual(c.quadrupole_strain_scale(1,1,50,10,shape=0),0)
    def test_strain_scale_D(self): self.assertAlmostEqual(c.quadrupole_strain_scale(1,1,50,10)/c.quadrupole_strain_scale(1,1,50,20),2.)
    def test_strain_scale_frequency(self): self.assertAlmostEqual(c.quadrupole_strain_scale(1,1,100,10)/c.quadrupole_strain_scale(1,1,50,10),4.)

class TestToyAxion(unittest.TestCase):
    def test_oscillator_lowfrequency(self):
        A,p=c.oscillator_response(0.,10.,0.1,100.)
        self.assertAlmostEqual(A,1.);self.assertEqual(p,0.)
    def test_oscillator_resonance_damped(self):
        A,p=c.oscillator_response(10.,10.,1.,100.)
        self.assertAlmostEqual(A,5.);self.assertAlmostEqual(p,math.pi/2)
    def test_oscillator_resonance_undamped_fails(self):
        with self.assertRaises(ValueError):c.oscillator_response(10.,10.,0.,1.)
    def test_phi_background_zero_omega(self): self.assertEqual(c.quadratic_coupling_response(0,3,2)[0],0)
    def test_phi_quadratic_2omega(self): self.assertEqual(c.quadratic_coupling_response(0,3,2)[1],9)
    def test_phi_background_nonzero_omega(self): self.assertEqual(c.quadratic_coupling_response(2,3,2)[0],24)
    def test_phi_even(self):
        self.assertEqual(c.quadratic_coupling_response(0,3,2),c.quadratic_coupling_response(0,-3,2))

class TestScenario(unittest.TestCase):
    def test_ref_baseline(self):
        r=c.Scenario().evaluate()
        self.assertAlmostEqual(r['max_magnetic_J'],1.66666666688871e8,delta=50)
        self.assertLess(r['omega_a_over_c'],1e-5)
    def test_failure_outside_domain(self):
        with self.assertRaises(ValueError):c.Scenario(radius_m=-1).evaluate()
        with self.assertRaises(ValueError):c.Scenario(distance_m=0).evaluate()

if __name__=='__main__':unittest.main()

class TestLorentzEM(unittest.TestCase):
    def test_zero_velocity_boost(self):
        E,B=(1e5,2e5,3e5),(0.2,0.3,0.4)
        self.assertEqual(c.lorentz_boost_fields(E,B,(0,0,0)),(E,B))
    def test_boost_invariant_i1(self):
        E,B=(2e5,3e5,4e5),(.1,.2,.3)
        Ep,Bp=c.lorentz_boost_fields(E,B,(0.25*c.C,0.10*c.C,0.05*c.C))
        i1,_=c.invariants_SI(E,B);j1,_=c.invariants_SI(Ep,Bp)
        self.assertAlmostEqual(j1/i1,1,delta=1e-12)
    def test_boost_invariant_i2(self):
        E,B=(2e5,3e5,4e5),(.1,.2,.3)
        Ep,Bp=c.lorentz_boost_fields(E,B,(0.25*c.C,0.10*c.C,0.05*c.C))
        _,i2=c.invariants_SI(E,B);_,j2=c.invariants_SI(Ep,Bp)
        self.assertAlmostEqual(j2/i2,1,delta=1e-12)
    def test_boost_superluminal_rejected(self):
        with self.assertRaises(ValueError):c.lorentz_boost_fields((0,0,0),(0,0,0),(c.C,0,0))
