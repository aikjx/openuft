"""Fit separately supplied, already-processed radial fractional residuals.

IMPORTANT: CSV alone does not establish observational provenance or validity.
Do NOT pass raw accelerations, J2 coefficients, orbital states or surface g here.
Requires residuals pre-corrected for geophysical/relativistic perturbations.
"""
from __future__ import annotations
import argparse,csv,json,pathlib,sys
BASE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/'src'))
import v137_diagnostics as v


def main(argv=None):
    ap=argparse.ArgumentParser(description='GLS fit to supplied preprocessed fractional radial gravity residuals (not raw telemetry)')
    ap.add_argument('--csv',required=True,help='CSV with height_m,residual_fraction,sigma_fraction')
    ap.add_argument('--covariance-json',help='optional full symmetric covariance matrix [[...]]')
    ap.add_argument('--lambda-km',type=float,default=124.6)
    ap.add_argument('--without-nuisance',action='store_true')
    ap.add_argument('--output-json',help='optional output path; never overwrites input')
    ap.add_argument('--source-note',default='NOT VERIFIED',help='free-text provenance note, not authenticated')
    args=ap.parse_args(argv)
    if not 0<args.lambda_km<1e7:ap.error('positive plausible Yukawa range required')
    rows=list(csv.DictReader(open(args.csv,encoding='utf-8-sig',newline='')))
    if len(rows)<5:ap.error('at least 5 distinct heights required')
    heights=[];y=[];sig=[]
    for row in rows:
        try:
            heights.append(float(row['height_m']))
            y.append(float(row['residual_fraction']))
            sig.append(float(row['sigma_fraction']))
        except (KeyError,ValueError) as e:ap.error('CSV columns or data invalid: '+str(e))
    if any(h<0 for h in heights) or len(set(heights))!=len(heights):ap.error('distinct nonnegative heights required')
    if args.covariance_json:
        C=json.load(open(args.covariance_json,encoding='utf-8'))
        if len(C)!=len(rows):ap.error('covariance does not match number of rows')
        # Reject a clearly non-symmetric matrix before Cholesky
        if any(abs(C[i][j]-C[j][i]) > 1e-9*max(abs(C[i][j]),abs(C[j][i]),1e-20)
               for i in range(len(C)) for j in range(len(C))):ap.error('covariance must be symmetric')
    else:C=v.correlated_cov(sig,0.)
    X=v.design_heights(heights,lam=args.lambda_km*1000,include_nuisance=not args.without_nuisance)
    fit=v.gls_fit(X,y,C)
    out={'data_label':'USER_SUPPLIED_UNVERIFIED_AND_PREPROCESSED_ONLY',
         'raw_orbit_model_or_geodesy_included':False,
         'provenance_note_unverified':args.source_note,
         'num_heights':len(rows),'lambda_km_fixed_not_fitted':args.lambda_km,
         'model':'residual = beta + alpha*Yukawa_surface_form_factor + gamma*(R/r)^2 (toy nuisance)' if not args.without_nuisance else 'residual = beta + alpha*Yukawa_surface_form_factor',
         'parameter_order':['offset','alpha_yukawa']+([] if args.without_nuisance else ['radial_nuisance']),
         'fit':fit,'limitations':['not a raw orbit integrator','not a geophysical perturbation correction',
                                  'not independently verified real observations']}
    s=json.dumps(out,indent=2,ensure_ascii=False)
    if args.output_json:
        dest=pathlib.Path(args.output_json).expanduser()
        if dest.resolve()==pathlib.Path(args.csv).resolve():ap.error('output cannot overwrite input')
        dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(s+'\n',encoding='utf-8')
    print(s)
    return 0
if __name__=='__main__':raise SystemExit(main())
