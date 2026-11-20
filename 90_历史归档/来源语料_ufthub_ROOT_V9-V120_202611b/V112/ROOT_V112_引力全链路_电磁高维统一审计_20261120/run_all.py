"""Generate the V112 numerical evidence and stand-alone figures."""
import sys,json,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from src import physics as p
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
RESULT=ROOT/"results"; FIG=ROOT/"figures"
RESULT.mkdir(exist_ok=True);FIG.mkdir(exist_ok=True)
scale=p.extremality_scale()
particles={
  name: {"mass_kg":mass,"abs_charge_C":abs(q),
         "xi":p.xi(mass,q), "force_ratio_identical":p.force_ratio(mass,q,mass,q),
         "classical_RN_horizon_exists":p.rn_horizons(mass,q)is not None}
  for name,mass,q in [("electron",p.me,p.e),("proton",p.mp,p.e)]
}
M=1e20
charged_rn=[]
for z in [0.,.25,.5,.75,.95,1.,1.05,1.2]:
    horizons=p.rn_horizons(M,z*M*scale)
    charged_rn.append({"xi":z,"horizon_r_minus_plus_m":list(horizons) if horizons else None})
summary={
  "metadata":{"version":"ROOT V112","science_status":"no unified field theory proof",
              "constants":"CODATA 2022 G; e exact SI; epsilon0 CODATA 2018 approx"},
  "constants":{"G_SI":p.G,"G_standard_uncertainty":p.uG,
               "c_m_s":p.c,"hbar_J_s":p.hbar,"eps0_F_m":p.eps0,"e_C":p.e},
  "dimensional":{"c_hbar_only_G_solution":str(p.dimension_G_solution()[0]),
                 "G_from_hbar_c_M2_dimension_MLT":p.trace_dimensional_identity()},
  "values":{"extremal_charge_mass_scale_C_per_kg":scale,
            "one_e_extremal_mass_kg":p.e/scale,
            "Planck_mass_from_G_kg_not_prediction":p.planck_mass(),
            "electron_alpha_G":p.alpha_gravitational(p.me),
            "electron_alpha":p.alpha_electric(p.e),
            "electron_KN_spin_parameter":p.kerr_spin_parameter(p.me,p.hbar/2),
            "electron_KN_extremality":p.kerr_newman_extremality(p.me,p.e,p.hbar/2),
            "earth_rg_m":p.grav_radius(p.Mearth),
            "earth_rs_m":2*p.grav_radius(p.Mearth),
            "earth_compactness":p.weak_compactness(p.Mearth,p.Rearth),
            "G_relative_standard_uncertainty":p.G_relative_uncertainty(),
            "xi_relative_standard_uncertainty_from_G":p.xi_relative_uncertainty()},
  "particles":particles,
  "charge_fraction_scan":charged_rn,
  "equivalence_data":{"MICROSCOPE_eta_TiPt":"(-1.5 ±2.3(stat) ±1.5(syst))e-15",
                      "Cassini_gamma_minus_one":"(2.1 ±2.3)e-5",
                      "LVK":"GWTC-5.0 tests published 2026"},
  "open_science":["derive G without input","derive SU3xSU2xU1 and representations",
                  "UV complete quantum gravity","novel exclusive observable","independent experiment"],
}
(RESULT/"V112_RESULTS.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")

# Distinct standalone charts (one plot per figure).
plt.figure(figsize=(8,5))
labels=["electron","proton","RN extremal"]
values=[particles["electron"]["xi"],particles["proton"]["xi"],1]
plt.bar(labels,np.log10(values))
plt.ylabel("log10 |Q| / (M sqrt(4*pi*eps0*G))")
plt.title("Weak force ratio and classical RN extremality")
plt.grid(axis="y",alpha=0.2)
plt.tight_layout()
plt.savefig(FIG/"01_extremality_scales.png",dpi=160)
plt.close()

x=np.linspace(0.12,3.5,700)
for z in [0,.5,1,1.15]:
    plt.plot(x,1-2/x+(z*z)/(x*x),label=f"xi = {z:g}")
plt.axhline(0,linestyle="--",linewidth=.8)
plt.ylim(-2,6);plt.xlabel("r / r_g");plt.ylabel("RN metric lapse f(r)")
plt.title("RN horizons and superextremal no-horizon cases")
plt.grid(alpha=.2);plt.legend();plt.tight_layout()
plt.savefig(FIG/"02_RN_lapse.png",dpi=160);plt.close()

masses=np.logspace(-32,-4,250)
g_values=p.hbar*p.c/(masses*masses)
plt.figure(figsize=(8,5))
plt.loglog(masses,g_values,label="hbar*c / M_*^2 (arbitrary mass)")
plt.axhline(p.G,linestyle="--",label="measured G")
plt.axvline(p.planck_mass(),linestyle=":",label="Planck mass derived from G")
plt.xlabel("independently supplied M_* (kg)")
plt.ylabel("derived numerical G (SI units)")
plt.title("Dimensional consistency is not a G prediction")
plt.grid(alpha=.2);plt.legend();plt.tight_layout()
plt.savefig(FIG/"03_G_scale_degeneracy.png",dpi=160);plt.close()
print(json.dumps({"xi_e":particles["electron"]["xi"],"xi_p":particles["proton"]["xi"],
                  "Earth_rs_m":summary["values"]["earth_rs_m"],
                  "history_issues":396},indent=2))

# The KN classical extremality boundary: spin^2 + charge^2 = 1.
spin=np.linspace(0,1,300)
q_max=np.sqrt(np.maximum(0,1-spin*spin))
plt.figure(figsize=(7,5))
plt.plot(spin,q_max,label="classical KN horizon boundary")
plt.fill_between(spin,0,q_max,alpha=.16,label="subextremal black-hole domain")
plt.xlabel("chi_spin = c |J| / (G M^2)")
plt.ylabel("xi = |Q| / (M sqrt(4 pi eps0 G))")
plt.title("Combined spin + charge extremality in Einstein-Maxwell")
plt.xlim(0,1.1);plt.ylim(0,1.1);plt.grid(alpha=.2);plt.legend();plt.tight_layout()
plt.savefig(FIG/"05_Kerr_Newman_extremality.png",dpi=160);plt.close()
