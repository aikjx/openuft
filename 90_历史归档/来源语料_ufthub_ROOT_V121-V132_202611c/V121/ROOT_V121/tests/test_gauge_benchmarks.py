"""Known field-theory benchmark identities; not new physics or ROOT action proof."""
import sympy as s


def test_local_U1_covariant_derivative():
    x=s.symbols('x',real=True)
    q,k,a,b=s.symbols('q k a b',real=True)
    psi=s.exp(s.I*k*x)
    chi=a*x*x
    A=b*x
    # D=d/dx+i q A; psi' =exp(-i q chi)psi and A'=A+chi'
    cov=lambda u,field: s.diff(u,x)+s.I*q*field*u
    psi_new=s.exp(-s.I*q*chi)*psi
    lhs=cov(psi_new,A+s.diff(chi,x))
    rhs=s.exp(-s.I*q*chi)*cov(psi,A)
    assert s.simplify(s.expand(lhs-rhs))==0


def test_su2_lie_algebra_pauli_generators():
    sx=s.Matrix([[0,1],[1,0]])/2
    sy=s.Matrix([[0,-s.I],[s.I,0]])/2
    sz=s.Matrix([[1,0],[0,-1]])/2
    assert sx*sy-sy*sx==s.I*sz


def test_su3_gellmann_subalgebra():
    l1=s.Matrix([[0,1,0],[1,0,0],[0,0,0]])/2
    l2=s.Matrix([[0,-s.I,0],[s.I,0,0],[0,0,0]])/2
    l3=s.Matrix([[1,0,0],[0,-1,0],[0,0,0]])/2
    assert l1*l2-l2*l1==s.I*l3


def test_abelian_bianchi_identity():
    x,y,z=s.symbols('x y z')
    axes=(x,y,z)
    A=[x*y*y,z*z*x,x*x*y]
    F=lambda i,j:s.diff(A[j],axes[i])-s.diff(A[i],axes[j])
    bianchi=s.diff(F(1,2),x)+s.diff(F(2,0),y)+s.diff(F(0,1),z)
    assert s.simplify(bianchi)==0
