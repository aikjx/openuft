import json, numpy as np
from pathlib import Path
base=Path(__file__).resolve().parents[1]
# All numbers dimensionless toy-model inputs, not fitted physical parameters.
M=np.array([[0.04,0.01,0.0],[0.01,0.09,0.015],[0.0,0.015,0.16]])
w,U=np.linalg.eigh(M)
ks=[0.1,1.0,10.0]
rows=[]
for k in ks:
 for j,m2 in enumerate(w):
  omega=float(np.sqrt(k*k+m2)); vg=float(k/omega)
  rows.append(dict(k=k,mode=j+1,mass_squared=float(m2),omega=omega,group_speed=vg,dispersion_residual=float(abs(omega**2-k*k-m2))))
# Show a tachyonic counterexample to universal stability
bad=np.diag([-0.01,0.04,0.09]); negative=float(np.linalg.eigvalsh(bad).min())
# rotational artificial gravity exact Newtonian engineering benchmark
G=6.67430e-11; g=9.80665; c=299792458.0
engineering={"point_mass_for_1g_at_1m_kg":g/G,"rotating_100m_rpm":float(np.sqrt(g/100)*60/(2*np.pi)),"10T_magnetic_energy_1m_sphere_J":float((10**2/(2*4*np.pi*1e-7))*(4*np.pi/3))}
result={"status":"mathematical toy model only; not experimental verification","mass_squared_matrix":M.tolist(),"eigenvalues":w.tolist(),"orthogonality_residual":float(np.max(abs(U.T@U-np.eye(3)))),"diagonalization_residual":float(np.max(abs(U.T@M@U-np.diag(w)))),"dispersion":rows,"negative_mass_squared_counterexample":negative,"engineering":engineering}
(base/'results'/'calculations.json').write_text(json.dumps(result,indent=2,ensure_ascii=False))
print(json.dumps(result,ensure_ascii=False,indent=2))
