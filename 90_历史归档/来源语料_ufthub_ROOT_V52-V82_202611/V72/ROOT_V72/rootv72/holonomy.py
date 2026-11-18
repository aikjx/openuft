"""SO(3)xSU(2) toy holonomy; SO(3) is NOT the physical Lorentz spin connection."""
import numpy as np
from scipy.linalg import expm
PAULI=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.array([[1,0],[0,-1]],complex)]
T=[p/2 for p in PAULI]
def so3():
    return (np.array([[0,0,0],[0,0,-1],[0,1,0]],float),np.array([[0,0,1],[0,0,0],[-1,0,0]],float))
def su2(g=.7,a=.9,b=.4):return 1j*g*a*T[0],1j*g*b*T[1]
def curvature(ax,ay):return ax@ay-ay@ax
def plaquette(ax,ay,h):
    if h<=0:raise ValueError('positive edge')
    return expm(ax*h)@expm(ay*h)@expm(-ax*h)@expm(-ay*h)
def product_connections():
    sx,sy=so3();gx,gy=su2()
    return (np.kron(.13*sx,np.eye(2))+np.kron(np.eye(3),gx),np.kron(.22*sy,np.eye(2))+np.kron(np.eye(3),gy))
def separate_curvature():
    sx,sy=so3();gx,gy=su2()
    return np.kron(curvature(.13*sx,.22*sy),np.eye(2))+np.kron(np.eye(3),curvature(gx,gy))
def transform_loop(loop,V):return V@loop@np.linalg.inv(V)
