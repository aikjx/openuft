import math
G=6.67430e-11; M=5.9722e24; R=6.371e6; MU0=4*math.pi*1e-7
B_EQ=3.12e-5

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def norm(a):return math.sqrt(dot(a,a))
def scale(a,k):return tuple(x*k for x in a)
def add(*vs):return tuple(sum(v[i] for v in vs) for i in range(3))
def fields(position, electric=(0,0,0)):
 r=norm(position)
 if r<R: raise ValueError('模型仅适用于地球外部')
 n=scale(position,1/r)
 g=scale(n,-G*M/r**2)
 # dipole magnetic axis +z; B at equator B_EQ
 z=(0,0,1); b=scale(add(scale(n,3*dot(z,n)),scale(z,-1)),B_EQ*(R/r)**3)
 return {'g':g,'E':tuple(electric),'B':b}
def forces(position,velocity,mass,charge,electric=(0,0,0)):
 f=fields(position,electric)
 fg=scale(f['g'],mass); fe=scale(f['E'],charge); fb=scale(cross(velocity,f['B']),charge)
 total=add(fg,fe,fb)
 return dict(**f,Fg=fg,Fe=fe,Fb=fb,Ftotal=total,magnitude=norm(total))
if __name__=='__main__':
 import json
 print(json.dumps(forces((R,0,0),(0,1000,0),1,1e-6,(0,100,0)),ensure_ascii=False,indent=2))
