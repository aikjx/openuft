import numpy as np
# symmetric candidate coupling matrix, dimensionless illustrative values
M=np.array([[0.04,0.01,0],[0.01,0.09,0.02],[0,0.02,0.16]])
w=np.linalg.eigvalsh(M)
k=1.0
omega=np.sqrt(k*k+w)
vg=k/omega
assert np.all(w>=0)
assert np.all(vg<=1)
assert np.allclose(np.linalg.eigvalsh(M),w)
print('eigenvalues',w)
print('omega',omega)
print('group velocity',vg)
