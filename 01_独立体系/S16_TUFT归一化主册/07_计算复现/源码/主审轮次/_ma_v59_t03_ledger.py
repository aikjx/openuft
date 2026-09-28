# -*- coding: utf-8 -*-
"""_ma_v59_t03_ledger.py — 台账登记 T03 背书"""
import json, os

p = 'D:/a10/aikjx/code/my_lib/TUFT_归一化台账_v1.0.json'
with open(p, encoding='utf-8-sig') as f:
    d = json.load(f)

d['main_agent_v59_t03_rerun'] = {
    'round': 'MainAgent independent re-run of organizer T03 (baryogenesis: 3 Sakharov conditions audit) — 3 lines all reproduced',
    'date': '2026-09-24',
    'erratum': 42,
    'line1_B': ('E329 is T=0 perturbative theorem, does NOT literally cover hot early universe (3-layer gap: zero-T vs finite-T, '
                'perturb vs non-perturb, Q=B vs Q=B-L unregistered). Sphaleron SM benchmark: T_eq=6.839e8 GeV=10^8.83 '
                '(window 160 GeV<T<6.84e8 GeV), E_sph(0)=7362 GeV=7.36 TeV, d(B+L)/event=6, washout 28/79=0.3544, '
                'need Y_BL(in)=2.455e-10. REPRODUCED. Q-identity registration gap is a real definitional hole '
                '(E329 registered without physical identity of Q). Script comment typo: ~9 TeV should be 7.36 TeV (cosmetic).'),
    'line2_CP': ('Jarlskog J=3.150277e-5 from reconstructed CKM (s12=0.225,s23=0.04182,s13=0.00369,delta=1.20), J/J_G3=0.9845 '
                 'REPRODUCED. kappa table: u,d,s,c,b frozen but gauge-equilibrated; t equilibrated (kappa_t=6.93) -> '
                 'no flavour simultaneously out-of-equilibrium + CKM-phased. Gap Y_B^obs/Y_B^CKM,max = 8.7e-11/1e-20 = 10^9.94. '
                 'TUFT internal geometry all-real (cm_t,d_t) -> no built-in complex phase. Verdict: CP source NOT '
                 'available internally; needs eta_new~O(0.1) postulate (10^9 stronger than J).'),
    'line3_nonEq': ('Four strict theorems: detailed balance -> Y_B=0; de Sitter dilution exp(3*60)=1.4894e78; '
                    'K(T_EW)=9.86e11>>1 equilibrium; E273 static wall. High-T K=1 break at T_K1_highT=1.58e14 GeV '
                    '(alpha_w=1/30 gauge rate) -> reheating window above it is inherently out-of-equilibrium (no V(n,T) '
                    'needed) but TUFT has no T_rh prediction (P17 sets H_inf only). Leptogenesis viable channel: '
                    'K_N=3.88e-4<1 at m_N=1e13 GeV. Neutrino freezeout T=1.445 MeV reproduced. Verdict: Sakharov-3 '
                    'NOT internally satisfied; V(n,T) missing; NE postulate registered.'),
    'matrix_update': ('Crack-matrix #5 (baryogenesis) transitions 未触及 -> STRUCTURAL CLOSURE as irreducible inputs: '
                      'P_T (B-violation freeze or sphaleron admission, Q=B vs B-L unregistered) + eta_new (new CP phase) '
                      '+ NE (V(n,T) external). Irreducible-input set grows 5 -> 7 (+eta_new, +NE).'),
    'verdict': ('ENDORSED: all three lines reproduced digit-for-digit; conclusions honest (no fake closure; escape '
                'hatches open). B-violation depends on P_T postulate; CP-violation unavailable internally (10^9.94 gap); '
                'non-equilibrium not satisfied (V(n,T) missing).'),
    'governance': 'scripts+out in my_lib; rerun logs _ma_t03_line{1,2,3}_rerun.txt; note Q-identity registration gap + script comment typo'
}
d['version'] = 'v5.11'
d['latest_round'] = 'v5.11_T03_endorsed_baryogenesis_irreducible'
tmp = p + '.tmp'
with open(tmp, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
os.replace(tmp, p)
print('ledger updated; keys:', len(d))
