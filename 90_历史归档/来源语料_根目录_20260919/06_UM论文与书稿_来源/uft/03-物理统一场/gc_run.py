import mpmath as mp
mp.mp.dps=80
hbar=mp.mpf('1.054571817e-34'); c=mp.mpf('299792458'); G=mp.mpf('6.67430e-11')
me=mp.mpf('9.1093837015e-31'); e=mp.mpf('1.602176634e-19')
eps0=mp.mpf('8.8541878128e-12'); mu0=mp.mpf('1.25663706212e-6')
alpha=mp.mpf('7.2973525693e-3')
kf=mp.mpf('3.162277660168379e-4'); tauf=mp.mpf('2.307625500826972e-6')
Qtop=me*c/hbar; lp=mp.sqrt(hbar*G/c**3)
K=hbar*kf/c; mP=mp.sqrt(hbar*c/(8*mp.pi*G)); Phi_T=mp.mpf(2)**(-3.5)

f = open('D:/a10/aikjx/code/my_lib/uft/03-物理统一场/gc_result.txt', 'w')
def p(s):
    f.write(s + '\n')

p('K = hbar*kappa/c = %.10e' % K)
p('lp = %.10e' % lp)
p('K/lp = %.10f' % (K/lp))
p('')
p('[1] mu_0 = 4*pi*k^2')
mug=4*mp.pi*kf**2; p('mug=%.10e  exp=%.10e  rat=%.12f' % (mug,mu0,mug/mu0))
p('')
p('[2] eps_0 = tau^2/(4*pi*hbar*c)')
eg=tauf**2/(4*mp.pi*hbar*c); p('eg=%.10e  exp=%.10e  rat=%.12f' % (eg,eps0,eg/eps0))
p('')
p('[3] Z_0 = 4*pi*k^2*c^2')
Z0g=4*mp.pi*kf**2*c**2; p('Z0g=%.10f  exp=%.10f  rat=%.12e' % (Z0g,mu0*c,Z0g/(mu0*c)))
p('')
p('[4] alpha = tau/kappa')
p('rel_err = %.12e' % ((tauf/kf-alpha)/alpha))
p('')
p('[5] e = sqrt(4*pi*K^2*tau*c^2)')
eg=mp.sqrt(4*mp.pi*K**2*tauf*c**2); p('eg=%.10e  exp=%.10e  rat=%.10f' % (eg,e,eg/e))
p('')
p('[6] hbar')
p('K*c*sqrt(k/t)=%.10e  rat=%.10f' % (K*c*mp.sqrt(kf/tauf),K*c*mp.sqrt(kf/tauf)/hbar))
p('K*c/kappa    =%.10e  rat=%.10f' % (K*c/kf, K*c/kf/hbar))
p('')
p('[7] me = K*tau*c')
meg=K*tauf*c; p('meg=%.10e  exp=%.10e  rat=%.10f' % (meg,me,meg/me))
p('')
p('[8] mP = c^2*K/G')
mPg=c**2*K/G; p('mPg=%.10e  exp=%.10e  rat=%.10f' % (mPg,mP,mPg/mP))
p('')
p('[9] alpha_w = Phi_T^2*4')
p('val=%.8f  err=%.6e' % (Phi_T**2*4,(Phi_T**2*4-mp.mpf('0.03106'))/mp.mpf('0.03106')))
p('alpha_s = Phi_T^2*15')
p('val=%.8f  err=%.6e' % (Phi_T**2*15,(Phi_T**2*15-mp.mpf('0.1179'))/mp.mpf('0.1179')))
p('alpha_s/alpha_w = %.4f (geom)  %.4f (exp)' % (15/4.0, mp.mpf('0.1179')/mp.mpf('0.03106')))
p('')
p('[10] G candidates:')
G1=c**3*K/(Qtop**2); p('G1=c^3*K/Qtop^2=%.10e rat=%.10f' % (G1,G1/G))
G2=c*K/kf**2; p('G2=c*K/k^2  =%.10e rat=%.10f' % (G2,G2/G))
G3=c*K**2/(Qtop*tauf); p('G3=c*K^2/(Qt*tau)=%.10e rat=%.10f' % (G3,G3/G))
G4=kf**2*c**3/G; p('G4=k^2*c^3/G =%.10e rat=%.10f' % (G4,G4/G))
G5=4*mp.pi*kf**2*c**3/G; p('G5=4pi*k^2*c^3/G=%.10e rat=%.10f' % (G5,G5/G))
G6=c**5*K**2/Qtop**4; p('G6=c^5*K^2/Qt^4 =%.10e rat=%.10f' % (G6,G6/G))
p('')
p('[11] Geometricization matrix:')
p('Const   Form                 Geom            Exp             Ratio    Status')
p('-'*75)
items=[
 ('mu_0','4*pi*k^2',mug,mu0,'PURE KAPPA'),
 ('eps_0','tau^2/(4*pi*hc)',eg,eps0,'PURE TAU'),
 ('Z_0','4*pi*k^2*c^2',Z0g,mu0*c,'PURE KAPPA'),
 ('alpha','tau/kappa',tauf/kf,alpha,'PURE RATIO'),
 ('e','sqrt(4pi*K^2*tau*c^2)',mp.sqrt(4*mp.pi*K**2*tauf*c**2),e,'K+TAU'),
 ('hbar','K*c/kappa',K*c/kf,K*c/kf/hbar,'K+KAPPA'),
 ('me','K*tau*c',meg,me,'K+TAU'),
 ('mP','c^2*K/G',mPg,mP,'NEEDS G'),
]
for nm,form,g,exp,st in items:
    p('%-8s %-20s %.6e %.6e %+.8f  %s' % (nm,form,g,exp,g/exp-1,st))
f.close()
