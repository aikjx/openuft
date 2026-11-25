"""Generate transparent, reproducible data artifacts (Python standard library only)."""
import csv
import json
import math
from pathlib import Path
from .monopole import simpson_flux, analytical_flux, section_norm_squared, section_norm_squared_simpson
from .dirac_spectrum import chiral_zero_modes, sphere_spectrum, first_massive_gap_per_length
from .anomalies import (SM_GEN, cubic_u1_anomaly, grav_u1_anomaly,
    su2_squared_u1_anomaly,su3_squared_u1_anomaly,su2_global_doublet_count,
    single_chiral_u1_anomalies,hypercharge_flux_index,family_flux_index)
from .units import dirac_gap_gev


def main(output_dir: Path) -> dict:
    output_dir=Path(output_dir)
    output_dir.mkdir(parents=True,exist_ok=True)
    fluxes=[]
    spectra=[]
    for n in range(-6,7):
        numeric=simpson_flux(n)
        exact=analytical_flux(n)
        plus,minus=chiral_zero_modes(n)
        fluxes.append({'flux_n':n,'chern_number':n,'index':plus-minus,'zero_plus':plus,
            'zero_minus':minus,'flux_numeric':numeric,'flux_analytic':exact,
            'absolute_flux_error':abs(numeric-exact),
            'first_massive_gap_R_units':first_massive_gap_per_length(n,1.0)})
        for level in sphere_spectrum(n,1.0,4):
            spectra.append({'flux_n':n,'k':level.level,
                'abs_eigenvalue_times_R':level.eigenvalue_abs_per_length,
                'degeneracy_per_sign':level.degeneracy_per_sign,
                'is_zero':level.zero_mode})
    norms=[]
    for k in range(3):
        norms.append({'flux_n':3,'k':k,'norm_exact':section_norm_squared(3,k),
                      'norm_numeric':section_norm_squared_simpson(3,k)})
    anomaly={'one_standard_model_generation':{
        'hypercharge_cubed':str(cubic_u1_anomaly()),
        'hypercharge_gravity':str(grav_u1_anomaly()),
        'su2_squared_hypercharge':str(su2_squared_u1_anomaly()),
        'su3_squared_hypercharge':str(su3_squared_u1_anomaly()),
        'su2_doublets_even':(su2_global_doublet_count()%2==0)},
        'single_charge_one_weyl_flux3': single_chiral_u1_anomalies(3,1),
        'hypercharge_as_same_monopole_flux3':hypercharge_flux_index(3),
        'independent_family_u1_with_charge_one_flux3':family_flux_index(3)}
    report={'model':'M4 x S2, round sphere, background U(1) monopole, charge integer; no radion stabilization',
            'status':'existing flux compactification consistency audit; not a proof of four-force unification',
            'conventions':'c=1 only; hbar,G retained dimensionful; SI conversion restores c',
            'flux_n3_total':3,'n3_zero_modes':chiral_zero_modes(3),
            'n3_first_massive_gap_R_units':2.0,
            'n3_first_massive_gap_GeV_if_R_1e_minus18m':dirac_gap_gev(3,1e-18),
            'max_abs_integral_error':max(f['absolute_flux_error'] for f in fluxes),
            'flux_table':fluxes,'n3_norms':norms,'anomaly_checks':anomaly,
            'important_assumptions':['6D Weyl fermion needed for net 4D chirality; 6D Dirac gives vectorlike pairs',
               'magnetic monopole field is a chosen background, not derived from helix dynamics',
               'a single U(1) hypercharge flux cannot make identical family multiplicities',
               'one-species chiral U(1) is anomalous; 4D and 6D anomaly checks required',
               'radius and flux integer are inputs; no prediction of masses or three families']}
    for filename,data,headers in [('flux_scan.csv',fluxes,tuple(fluxes[0].keys())),
                                  ('spectrum_scan.csv',spectra,tuple(spectra[0].keys())),
                                  ('zero_mode_norms.csv',norms,tuple(norms[0].keys()))]:
        with (output_dir/filename).open('w',encoding='utf-8',newline='') as fh:
            writer=csv.DictWriter(fh,fieldnames=headers)
            writer.writeheader();writer.writerows(data)
    (output_dir/'results.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    (output_dir/'anomaly_checks.json').write_text(json.dumps(anomaly,indent=2,ensure_ascii=False),encoding='utf-8')
    return report
