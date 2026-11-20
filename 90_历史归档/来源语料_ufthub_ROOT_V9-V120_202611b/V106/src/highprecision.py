"""Independent mpmath 80-digit calculation. Float values are compared downstream."""
from pathlib import Path
import json
import mpmath as mp

ROOT=Path(__file__).resolve().parents[1]
def run():
    mp.mp.dps=80
    m=mp.mpf('91.1876'); em=mp.mpf('127.930'); sw=mp.mpf('0.23122'); strong=mp.mpf('0.1180')
    v=[mp.mpf(3)/5*(1-sw)*em,sw*em,1/strong]
    b=[mp.mpf(41)/10,-mp.mpf(19)/6,mp.mpf(-7)]
    I=(b[1]-b[2])*v[0]+(b[2]-b[0])*v[1]+(b[0]-b[1])*v[2]
    results={}
    for i,j in ((0,1),(0,2),(1,2)):
        t=2*mp.pi*(v[i]-v[j])/(b[i]-b[j]);mu=m*mp.exp(t)
        results[f'{i+1}{j+1}']={'t':mp.nstr(t,75),'mu_GeV':mp.nstr(mu,75)}
    results['invariant']=mp.nstr(I,75)
    (ROOT/'results'/'highprecision_80_digits_THEORY.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    return results
if __name__=='__main__':
    print(run())
