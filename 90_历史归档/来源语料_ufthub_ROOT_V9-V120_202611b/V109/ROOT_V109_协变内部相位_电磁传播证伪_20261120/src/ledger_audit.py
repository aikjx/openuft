"""Preserve and annotate the 396 V108 research items; never promote status by code tests."""
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FOCUS={
 'B14':'A periodic internal phase is modeled as a separate Lorentz pseudoscalar; not derived from helical spacetime.',
 'B15':'GR+SM+theta EFT is a valid starting action, not a UV unified first-principles theory.',
 'B16':'Theta is an ordinary Lorentz pseudoscalar in the candidate; no proof v_total=c.',
 'B21':'Total stress-energy conservation only for dynamical theta, not prescribed external theta.',
 'B23':'Derived a conditional axion-modified Maxwell equation, with standard Maxwell at constant theta.',
 'B27':'G remains a free input, no independent value is computed.',
 'B30':'Polarization is a standard ALP prediction, not ROOT-exclusive.',
 'C43':'The photon sector alone cannot establish electroweak gauge representation.',
 'C49':'No novel gravitational effect computed by this polarization model.',
 'D57':'Backreaction not included in fixed-theta wave propagation.',
 'E69':'A phase-axis result is modulo pi; full E-field reconstruction required beyond WKB.',
 'E70':'Gauge invariant theta FdualF interaction; pure phase connection has zero curvature if smooth.',
 'E77':'Physical observable must be derived including detector and model uncertainties.',
 'U107-12':'Polarization alone is degenerate with an ordinary ALP; new ROOT-exclusive signature still OPEN.',
}
NEW=[
('V109-01','Axion-modified Maxwell variation','CONDITIONAL_MATH_VERIFIED','Verify Euler-Lagrange equations with declared metric conventions'),
('V109-02','Constant theta bulk null effect','CONDITIONAL_MATH_VERIFIED','FdualF topological boundary term; global caveats documented'),
('V109-03','WKB polarization endpoint law','CONDITIONAL_MATH_VERIFIED','Compare full helicity ODE against WKB in its validity regime'),
('V109-04','Nonadiabatic endpoint counterexample','NUMERIC_MODEL_VALIDATED','Identify explicit parameters with large departure from endpoint rule'),
('V109-05','Single-signal parameter rank','MATH_VERIFIED','Prove rank one for lam and Delta theta and state independent-information requirement'),
('V109-06','Backreaction and energy exchange','OPEN','Solve coupled theta-plus-electromagnetic system with proper boundary conditions'),
('V109-07','Global compact theta normalization','OPEN','Establish topological coefficient quantization on the intended bundle'),
('V109-08','ROOT-exclusive observation','OPEN','New signal cannot be reproduced by known ALP EFT or GR+SM'),
('V109-09','SM+GR unification and G','OPEN','Produce free-parameter-independent origin of mass and G and anomaly-free spectrum'),
('V109-10','Polarimeter with real systematics','NEEDS_REAL_EXPERIMENT','Polarimetry with independent theta amplitude, calibration and null tests'),
('V109-11','Time-dependent photon mode positivity','CONDITIONAL_MODEL_CHECKED','Demonstrate WKB breakdown or imaginary frequency cases by independent integration'),
('V109-12','Actual astrophysical constraints','LITERATURE_SCOPED','Use model-specific assumptions and dates, no cross-model universal bound'),
]
def build():
    src=ROOT/'ledger'/'V108_ALL_396_AUDITED.csv'
    out=ROOT/'ledger'/'V109_ALL_396_PRESERVED.csv'
    rows=list(csv.DictReader(src.open(encoding='utf-8-sig',newline='')))
    if len(rows)!=396 or len({r['canonical_id'] for r in rows})!=396:
        raise ValueError('historical ledger mismatch')
    cols=list(rows[0])+['v109_scope','v109_original_goal_closed']
    with out.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=cols);w.writeheader()
        for r in rows:
            r['v109_scope']=FOCUS.get(r['canonical_id'],'Preserved; no new evidence in V109')
            r['v109_original_goal_closed']='NO' # V108 already noted original goal is open
            w.writerow(r)
    with (ROOT/'ledger'/'V109_NEW_WORKSTREAMS.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['id','task','evidence_state','acceptance'])
        w.writerows(NEW)
    result={'legacy_rows':len(rows),'legacy_unique_ids':len(set(r['canonical_id'] for r in rows)),
            'new_workstreams':len(NEW),'new_closed_unification_goals':0,
            'focused_legacy_ids':sorted(set(FOCUS)&{r['canonical_id'] for r in rows}),
            'preserved_original_acceptance':all(bool(r.get('acceptance')) for r in rows)}
    (ROOT/'results'/'ledger_summary.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    return result
if __name__=='__main__':print(build())
