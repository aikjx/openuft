import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

t = np.linspace(0, 12*np.pi, 2000)
R = 1.0
omega =1.0
c=1.0
x = R*np.cos(omega*t)
y = R*np.sin(omega*t)
z = c*t

fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(111,projection='3d')
ax.plot(x,y,z,lw=0.8)
ax.set_title("Cylindrical circular helix — GAQ‑UFT vacuum generator")
plt.show()
