import numpy as np, sys
sys.path.insert(0,r"D:\a10\aikjx\code\my_lib")
import importlib.util
spec=importlib.util.spec_from_file_location("td",r"D:\a10\aikjx\code\my_lib\_ma_v11_timedomain.py")
td=importlib.util.module_from_spec(spec); spec.loader.exec_module(td)

dx=0.025; dt=0.02; tmax=300.0
xs,r,rs=td.build_grid(dx=dx); V=td.potential(xs,r,rs,2)
tt,sig=td.evolve(2,xs,V,dx,dt,tmax)
ipk=np.argmax(np.abs(sig)); print("peak |psi|=",abs(sig[ipk]),"at t=",tt[ipk])
print("max|sig| overall=",np.abs(sig).max()," final|sig|=",abs(sig[-1]))
for a in range(20,301,20):
    m=(tt>=a)&(tt<a+20)
    print(f"t[{a:3d},{a+20:3d}] max|sig|={np.abs(sig[m]).max():.3e} rms={np.sqrt((sig[m]**2).mean()):.3e}")
# 过零数（粗略频率）t=80..140
m=(tt>=80)&(tt<=140); zz=sig[m]; zc=np.sum(np.signbit(zz[:-1])!=np.signbit(zz[1:]))
print("zero-crossings t80-140:",zc," -> f~",zc/2/60)
