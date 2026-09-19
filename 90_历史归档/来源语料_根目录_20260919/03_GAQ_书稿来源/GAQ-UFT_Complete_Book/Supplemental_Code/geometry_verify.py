"""
GAQ‑UFT: G ε0 unification equation dimensional check
"""
import mpmath as mp
mp.mp.dps=120

# CODATA 2022
G = mp.mpf("6.67430e-11")
eps0 = mp.mpf("8.8541878128e-12")
c = mp.mpf("299792458")

def dim_check_Geps0():
    Geps0 = G*eps0
    print(f"G*ε0 = {Geps0:.20e}")
    return Geps0

if __name__=="__main__":
    dim_check_Geps0()
