"""
Koide mass relation numerical scan for GAQ‑UFT
m_e, m_mu, m_tau in MeV/c^2
"""
import mpmath as mp
mp.mp.dps = 100

me = mp.mpf("0.51099895000")
mmu = mp.mpf("105.6583755")
mtau = mp.mpf("1776.86")

def koide_formula(m1,m2,m3):
    lhs = m1+m2+m3
    rhs = (2/3)*(mp.sqrt(m1)+mp.sqrt(m2)+mp.sqrt(m3))**2
    return lhs, rhs, abs(lhs-rhs)/lhs

if __name__=="__main__":
    L,R,err = koide_formula(me,mmu,mtau)
    print(f"LHS = {L:.8f}")
    print(f"RHS = {R:.8f}")
    print(f"relative error = {err:.8e}")
