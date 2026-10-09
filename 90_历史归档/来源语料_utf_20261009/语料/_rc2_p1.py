#!/usr/bin/env python3
import math,sys,datetime
c=299792458.0;hb=1.0545718176461565e-34;eC=1.602176634e-19
G=6.67430e-11;alpha=7.2973525693e-3;eps0=8.8541878128e-12
me=9.1093837015e-31;mp=1.67262192369e-27
H0=67.84*1000/3.0856775814913673e22;OL=0.6889;Om=0.3111;Ob=0.0486;Oc=Om-Ob
RL=c/H0;Lam=3*OL*(H0/c)**2;tH=1/H0
mu0_exp=1.0/(eps0*c**2);mP=math.sqrt(hb*c/G);lP=math.sqrt(hb*G/c**3)
