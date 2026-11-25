#!/usr/bin/env python3
"""Regenerate deterministic machine-readable results and vector figures."""
from pathlib import Path
import json,csv,sys,math
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/'src'))
from root_v149.core import diagnostic,helix_for_alpha,ALPHA,wave_residuals
from root_v149.energy import ratio_E_over_hbar_omega
from root_v149.units import dimension_audit
from root_v149.precision import audit_decimal


def chart_svg(points,width=920,height=440):
    left,right,top,bottom=93,34,45,64
    W,H=width-left-right,height-top-bottom
    def X(b):return left+W*(b+0.99)/1.98
    def Y(v):return top+H*(1-v/1.02)
    coords=' '.join(f'{X(b):.2f},{Y(v):.2f}' for b,v in points)
    axes=''.join(f'<line x1="{left}" y1="{Y(v):.1f}" x2="{width-right}" y2="{Y(v):.1f}" stroke="#d8dee8" stroke-width="1"/><text x="{left-12}" y="{Y(v)+5:.1f}" text-anchor="end" font-size="13" fill="#4b5669">{v:.1f}</text>' for v in [0,.2,.4,.6,.8,1.0])
    xticks=''.join(f'<line x1="{X(b):.1f}" y1="{height-bottom}" x2="{X(b):.1f}" y2="{height-bottom+5}" stroke="#4b5669"/><text x="{X(b):.1f}" y="{height-bottom+24}" text-anchor="middle" font-size="12" fill="#4b5669">{b:+.1f}</text>' for b in [-.9,-.6,-.3,0,.3,.6,.9])
    h=helix_for_alpha(); x0,y0=X(0),Y(ALPHA); xc,yc=X(h.u),Y(1)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="#ffffff"/><text x="28" y="25" font-family="Arial,sans-serif" font-size="18" font-weight="bold" fill="#1d2b3b">Observer-dependent helix ratio (NOT physical α)</text>
{axes}{xticks}<line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" stroke="#39485b" stroke-width="2"/><line x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" stroke="#39485b" stroke-width="2"/>
<polyline fill="none" stroke="#285e97" stroke-width="3" points="{coords}"/><line x1="{left}" y1="{Y(ALPHA)}" x2="{width-right}" y2="{Y(ALPHA)}" stroke="#be873e" stroke-dasharray="6,5" stroke-width="2"/>
<circle cx="{x0}" cy="{y0}" r="5" fill="#be873e"/><circle cx="{xc}" cy="{yc}" r="5" fill="#c94444"/>
<text x="{x0+10}" y="{y0-10}" font-family="Arial,sans-serif" font-size="12" fill="#ad772b">lab fit: 0.007297</text>
<text x="{xc-9}" y="{yc-13}" text-anchor="end" font-family="Arial,sans-serif" font-size="12" fill="#a12b2b">beta=u: ratio=1</text>
<text x="{left+W/2}" y="{height-13}" text-anchor="middle" font-family="Arial,sans-serif" font-size="15" fill="#39485b">Axial Lorentz boost β</text>
<text transform="translate(27 {top+H/2}) rotate(-90)" text-anchor="middle" font-family="Arial,sans-serif" font-size="14" fill="#39485b">χ = κ²/(κ²+τ²)</text>
<text x="{width-right}" y="{top+22}" text-anchor="end" font-family="Arial,sans-serif" font-size="11" fill="#68788e">Illustration from fitted kinematics, not experiment</text>
</svg>'''


def main():
    results=BASE/'results';figures=BASE/'figures';results.mkdir(exist_ok=True);figures.mkdir(exist_ok=True)
    report=diagnostic()
    report['dimension_audit']=dimension_audit()
    report['maxwell_example']={'faraday_ampere_EB_invariants':wave_residuals(.2,.4)}
    (results/'high_precision_decimal.json').write_text(json.dumps(audit_decimal(),indent=2,ensure_ascii=False,sort_keys=True)+'\n',encoding='utf-8')
    (results/'precise_metrics.json').write_text(json.dumps(report,indent=2,ensure_ascii=False,sort_keys=True)+'\n',encoding='utf-8')
    h=helix_for_alpha()
    samples=sorted(set([round(-.99+1.98*i/198,12) for i in range(199)]+[0.,h.u]))
    rows=[]
    for beta in samples:
        p=h.boost_z(beta)
        rows.append((beta,p.omega,p.u,p.curvature(),p.torsion(),p.alpha_proxy(),ratio_E_over_hbar_omega(h,beta)))
    with (results/'frame_scan.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f);writer.writerow(['beta','omega_per_L','u','kappa_per_L','tau_per_L','geometric_alpha_proxy','conditional_energy_phase_ratio']);writer.writerows(rows)
    with (results/'alpha_is_input_not_prediction.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f);writer.writerow(['chosen_target','a_in_L','u','recovered_proxy'])
        for al in [.0001,ALPHA,.01,.1,.25,.5,.75,.99]:
            p=helix_for_alpha(al);writer.writerow([al,p.a,p.u,p.alpha_proxy()])
    (figures/'boost_frame_dependence.svg').write_text(chart_svg([(r[0],r[5]) for r in rows]),encoding='utf-8')
    print('Created precise_metrics.json, high_precision_decimal.json, frame_scan.csv, alpha_is_input_not_prediction.csv, boost_frame_dependence.svg')

if __name__=='__main__':main()
