# -*- coding: utf-8 -*-
"""MainAgent T11 SSOT ledger registration + errata #43.
Writes TUFT_归一化台账_v1.0.json (backup already at _ma_t11_backup_pre_t11.json).
"""
import json, io, time

path = r'D:\a10\aikjx\code\my_lib\openuft\01_独立体系\S16_TUFT归一化主册\13_论文与成果\台账\TUFT_归一化台账_v1.0.json'
with io.open(path, 'r', encoding='utf-8') as f:
    L = json.load(f)

L['latest_round'] = 'v6.0_T11_anchor_N480_reinforced_shooting_scoped_out_gateB_open'

L['main_agent_v60_t11_line1_rerun'] = {
    "round": "T11 line1 complex-contour shooting n=0 (final version)",
    "date": "2026-09-27",
    "status": "VERIFIED (numerics) ; method BUILT + decaying-sheet directionally confirmed, n=0 self-check NOT closed (|shoot-anchor|=4.397e-02, tol 2e-03); pencil anchor remains authoritative",
    "verification": [
        "local n=0 Sm=40 shooting = 0.430352451005-0.100230156674i EXACT (|dw|=3.589e-13) via resid_lead+coarse_scan+complex_newton",
        "directional check |D(anchor,|s|)|: 0.86(40)->0.63(55)->0.055(70)->1.4e-3(90)->5.8e-4(120)->3.1e-4(160) monotone -> anchor IS the contour BVP pole",
        "root on Im<0 DECAYING sheet (vs T10 line3 real-axis landed Im>0 +0.039i -- Stokes repair directionally works)",
        "offset 4.4e-2 = finite-|s| IVP locks onto nearby spurious branch (exponentially suppressed leakage on growing contour; narrow/non-quadratic basin)",
        "conclusion: global Beyn pencil is the authoritative spectral route; outward IVP cannot re-pin to 1e-9"
    ],
    "four_state": {
        "strict": "GR Leaver a=0 n=0,1,2 references (frozen, unchanged)",
        "conditional": "TUFT n=0 fundamental STANDS from T10 pencil (Gate A); IVP confirms sheet only",
        "definition": "complex-contour Leaver IVP shooting (regular wall start, pure-outgoing end with runtime C/s^2 tail removal, sqrt(h) branch from h>0, Stokes-avoiding Re[-2iw s]>0 half-plane)",
        "open": "TUFT n=1,n=2 overtones + clean IVP re-pin of n=0 to 1e-9 (D-OPEN)"
    }
}

L['main_agent_v60_t11_line2_rerun'] = {
    "round": "T11 line2 n=1 dual-candidate adjudication by complex-contour shooting",
    "date": "2026-09-27",
    "status": "VERIFIED (numerics) ; THREE-CANDIDATE STANDOFF -- shooting root hits NEITHER T09 nor T10 candidate (|dw|~1.03e-1 each); n=1 inter-Smatch drift 1.557e-1; Gate B OPEN",
    "verification": [
        "local n=1 t_match=20 shooting = 0.513402121318-0.285869774501i EXACT (|dw|=1.386e-13) via run_overtone (build_traj(40.0) ts,rhov,Vv)",
        "|w_shoot-CAND_T09|=1.027e-01, |w_shoot-CAND_T10|=1.027e-01, |CAND_T10-CAND_T09|=1.619e-05",
        "root drifts with t_match (t=20: 0.513402-0.285870i ; t=32: 0.661274-0.334668i) -- decaying outgoing channel for n=1 on this ray; finite-t zeros are 1/|s|^2-drift accidental cancellations",
        "no forced pick, no pseudo-close"
    ],
    "four_state": {
        "strict": "GR Leaver a=0 references (frozen, unchanged)",
        "conditional": "TUFT n=0 fundamental (frozen T10 Gate-A, unchanged; not re-shot here)",
        "definition": "independent Leaver IVP shooting on peeled F-equation along deformed ray s=b t; R(w)=0 = regular lambda_+ at wall + bounded const-channel F_s/F->0 at t_match; WKB-phase basin start",
        "open": "TUFT n=1 overtone spectrum (D-OPEN, three-candidate residual structure reported)"
    }
}

L['main_agent_v60_t11_line3_rerun'] = {
    "round": "T11 line3 cross-validation (F-pencil N=480 + IVP self-check)",
    "date": "2026-09-27",
    "status": "VERIFIED (numerics) ; N=480 spectral cross SUCCESS -> T10 anchor independently reinforced; IVP self-check FAIL (root drifts 0.106 with Tmatch); n=2 NOT endorsed",
    "verification": [
        "local F-pencil N=480 = 0.434445176596-0.056449764639i EXACT (|dw|=1.775e-13) via T10 frob+pencil module (beyn_pole radius 0.005 nc=200)",
        "|w480-w360|=3.467e-10, |w480-extrap.anchor|=4.387e-10 <= 1e-9 -> spectral ladder directly confirms T10 geometric extrapolation limit",
        "IVP shooting Tmatch=7 -> 0.395957855657-0.075833697797i vs Tmatch=11 -> 0.485411541803-0.132373066915i (|dw|=1.058e-01) -> FAIL",
        "n=2 not endorsed per hard discipline (n=0 self-check must pass first)"
    ],
    "four_state": {
        "strict": "GR Leaver a=0 references (frozen); F-pencil N=480 spectral cross (|w480-extrap|=4.39e-10) -- strict-level numerical cross",
        "conditional": "TUFT n=0 fundamental (T10 Gate-A frozen, now N=480 reinforced)",
        "definition": "F-pencil + Beyn pole extraction (N=480); complex-contour IVP shooting",
        "open": "TUFT n=1,n=2 overtone spectrum (D-OPEN)"
    }
}

L['errata_43'] = {
    "round": "T11 line2 adjudication readback",
    "date": "2026-09-27",
    "finding": "T10 audit mis-stated the cross-pipeline n=1 candidate separation as ~1.6e-2; correct value |CAND_T10-CAND_T09| = 1.619e-05 (3 orders smaller).",
    "impact": "T09/T10 n=1 pipelines agree to ~1.6e-5 (not 1.6e-2): the conflict is a numerical perturbation-scale disagreement, NOT a double-root/leak-pair signature. Does NOT change Gate B OPEN status (target 1e-9 far from reached), but changes the diagnosis: remaining gap is 4 orders of magnitude above target, not 7.",
    "action": "All prior '1.6e-2'/'1.6e-02' references to the n=1 cross-pipeline gap corrected to 1.619e-5 in ledger/main/arch. Frozen E-numbers untouched."
}

with io.open(path, 'w', encoding='utf-8', newline='') as f:
    json.dump(L, f, ensure_ascii=False, indent=2)

print('ledger updated, keys now:', len(L))
print('latest_round:', L['latest_round'])
