import unittest
import sympy as sp
from src import field as fld


class FieldTests(unittest.TestCase):
    def test_Bianchi_potential(self):
        A=sp.Matrix([fld.x*fld.y,fld.t*fld.y,fld.z*fld.t,fld.x*fld.z])
        self.assertEqual(fld.bianchi(fld.field_strength(A)),[0]*4)

    def test_composite_Bianchi(self):
        F=fld.internal_field([(fld.t*fld.x,fld.y),(fld.z**2, fld.t+fld.x)])
        self.assertEqual(fld.bianchi(F),[0]*4)

    def test_redefinition_tensor(self):
        A=sp.Matrix([fld.z,fld.t,0,fld.x])
        pairs=[(fld.x,fld.y),(fld.t,fld.z**2)]
        eta=sp.Rational(2,7)
        effective,H=fld.composite_shift(A,pairs,eta)
        check=fld.field_strength(A)+eta*fld.internal_field(pairs)
        self.assertEqual((H-check).applyfunc(sp.simplify),sp.zeros(4))

    def test_field_redefinition_flat_A(self):
        A=sp.zeros(4,1)
        pair=[(fld.x,fld.y)]
        _,H=fld.composite_shift(A,pair,1)
        self.assertEqual(H[1,2],1)

    def test_gauge_invariant(self):
        A=sp.Matrix([fld.t*fld.z, fld.t**2, fld.x*fld.y, fld.x*fld.z])
        chi=fld.x*fld.t+fld.z**3+fld.y*fld.z
        self.assertEqual((fld.field_strength(A+fld.differential(chi))-
                          fld.field_strength(A)).applyfunc(sp.simplify),sp.zeros(4))

    def test_quartic_background_F(self):
        f2,f_sq=fld.single_field_quartic_order()
        eps=sp.symbols('epsilon',real=True)
        self.assertEqual(f2,eps**2)
        self.assertEqual(f_sq,2*eps**4)

    def test_quartic_no_epsilon2(self):
        _,f_sq=fld.single_field_quartic_order()
        eps=sp.symbols('epsilon',real=True)
        self.assertEqual(sp.expand(f_sq).coeff(eps,2),0)

    def test_independent_A_quadratic_background(self):
        eps=sp.symbols('epsilon',real=True)
        A=sp.Matrix([0,eps*fld.t,0,0])
        F=fld.field_strength(A)
        inv=sp.expand(sum(F[i,j]*(fld.metric*F*fld.metric)[i,j]
                          for i in range(4) for j in range(4)))
        self.assertEqual(inv,-2*eps**2)

    def test_free_wave_current(self):
        k=sp.symbols('k',positive=True,real=True)
        F=fld.field_strength(fld.plane_wave(k,k))
        self.assertEqual(fld.maxwell_current(F),sp.zeros(4,1))

    def test_offshell_wave_current(self):
        k,w=sp.symbols('k w',positive=True,real=True)
        J=fld.maxwell_current(fld.field_strength(fld.plane_wave(k,w)))
        self.assertEqual(J[1],sp.simplify((w*w-k*k)*sp.cos(k*fld.z-w*fld.t)))

    def test_wave_orthogonal_EB(self):
        k=sp.symbols('k',positive=True,real=True)
        F=fld.field_strength(fld.plane_wave(k,k))
        E=sp.Matrix([-F[0,i] for i in (1,2,3)])
        B=sp.Matrix([F[2,3],F[3,1],F[1,2]])
        self.assertEqual(sp.simplify(E.dot(B)),0)

    def test_wave_equal_EB(self):
        k=sp.symbols('k',positive=True,real=True)
        F=fld.field_strength(fld.plane_wave(k,k))
        E=sp.Matrix([-F[0,i] for i in (1,2,3)])
        B=sp.Matrix([F[2,3],F[3,1],F[1,2]])
        self.assertEqual(sp.simplify(E.dot(E)-B.dot(B)),0)

    def test_wave_Bianchi(self):
        self.assertEqual(fld.bianchi(fld.field_strength(fld.plane_wave(2,2))),[0]*4)

    def test_composite_redefinition_two_pairs(self):
        A=sp.Matrix([fld.x, fld.y, fld.z, fld.t])
        pairs=[(fld.t,fld.x),(fld.y,fld.z)]
        Aeff,H=fld.composite_shift(A,pairs,sp.Rational(1,5))
        self.assertEqual(H[0,1],-sp.Rational(4,5))
        self.assertEqual(H[2,3],-sp.Rational(4,5))

    def test_boost_metric(self):
        beta=sp.Rational(3,5)
        gamma=1/sp.sqrt(1-beta**2)
        boost=sp.Matrix([[gamma,-beta*gamma,0,0],[-beta*gamma,gamma,0,0],
                         [0,0,1,0],[0,0,0,1]])
        self.assertEqual((boost.T*fld.metric*boost-fld.metric).applyfunc(sp.simplify),sp.zeros(4))

    def test_boost_field_invariant(self):
        beta=sp.Rational(3,5)
        gamma=1/sp.sqrt(1-beta**2)
        boost=sp.Matrix([[gamma,-beta*gamma,0,0],[-beta*gamma,gamma,0,0],
                         [0,0,1,0],[0,0,0,1]])
        F=fld.internal_field([(fld.t,fld.x),(fld.y,fld.z)])
        inv=boost.inv()
        Fprime=(inv.T*F*inv).applyfunc(sp.simplify)
        invF=lambda H:sp.simplify(sum(H[i,j]*(fld.metric*H*fld.metric)[i,j]
                                         for i in range(4) for j in range(4)))
        self.assertEqual(sp.simplify(invF(Fprime)-invF(F)),0)

    def test_boost_tensor_antisymmetric(self):
        beta=sp.Rational(3,5)
        gamma=1/sp.sqrt(1-beta**2)
        boost=sp.Matrix([[gamma,-beta*gamma,0,0],[-beta*gamma,gamma,0,0],
                         [0,0,1,0],[0,0,0,1]])
        F=fld.internal_field([(fld.t,fld.x),(fld.y,fld.z)])
        T=(boost.inv().T*F*boost.inv()).applyfunc(sp.simplify)
        self.assertEqual((T+T.T).applyfunc(sp.simplify),sp.zeros(4))

    def test_antisymmetric(self):
        F=fld.internal_field([(fld.t+fld.x*fld.y,fld.z*fld.y)])
        self.assertEqual(F+F.T,sp.zeros(4))

    def test_plane_wave_potential_is_not_helical_trajectory(self):
        # A field amplitude oscillating does not prescribe particle trajectories.
        F=fld.field_strength(fld.plane_wave(2,2))
        self.assertEqual(fld.maxwell_current(F),sp.zeros(4,1))

    def test_rank4_pair(self):
        F=fld.internal_field([(fld.t,fld.x),(fld.y,fld.z)])
        pf=F[0,1]*F[2,3]-F[0,2]*F[1,3]+F[0,3]*F[1,2]
        self.assertEqual(pf,1)

    def test_rank2_pair(self):
        F=fld.internal_field([(fld.t,fld.x)])
        pf=F[0,1]*F[2,3]-F[0,2]*F[1,3]+F[0,3]*F[1,2]
        self.assertEqual(pf,0)


if __name__=='__main__': unittest.main()
