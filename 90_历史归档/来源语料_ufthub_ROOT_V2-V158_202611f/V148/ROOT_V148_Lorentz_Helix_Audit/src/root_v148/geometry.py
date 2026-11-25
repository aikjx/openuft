"""No-go checks for pure rotation frames and a single smooth scalar phase."""
from math import cos,sin

JZ=((0.,-1.,0.),(1.,0.,0.),(0.,0.,0.))

def matrix_scale(A,f):
    return [[f*x for x in row] for row in A]

def matrix_commutator(A,B):
    mul=lambda X,Y:[[sum(X[i][k]*Y[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    AB=mul(A,B);BA=mul(B,A)
    return [[AB[i][j]-BA[i][j] for j in range(3)] for i in range(3)]

def frame_curvature_single_angle(t,z):
    """R=Rz(sin(t-z)); Omega=J dtheta. Returns exact Maurer-Cartan coefficient."""
    theta_t=cos(t-z);theta_z=-cos(t-z)
    d_t_theta_z=sin(t-z);d_z_theta_t=sin(t-z)
    Ot=matrix_scale(JZ,theta_t);Oz=matrix_scale(JZ,theta_z)
    com=matrix_commutator(Ot,Oz)
    return [[JZ[i][j]*(d_t_theta_z-d_z_theta_t)+com[i][j] for j in range(3)] for i in range(3)]

def photon_dof():
    # 4 potential components; 1 Lorenz constraint; 1 residual on-shell gauge redundancy.
    return 4-1-1
