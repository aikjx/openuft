# -*- coding: utf-8 -*-
"""v58 合并似然判决：台账追加 E508，升版 v6.9->v7.0。append-only，不动四态/勘误。"""
import json, io

P = r"D:\a10\aikjx\code\my_lib\openuft\01_独立体系\S16_TUFT归一化主册\13_论文与成果\台账\TUFT_归一化台账_v1.0.json"
d = json.load(open(P, encoding="utf-8"))

d["version"] = "v7.0"
d["date"] = "2026-09-26"
d["last_updated"] = "2026-09-26"
d["latest_round"] = "v7.0_v58_combined_likelihood"
d["equation_range"] = "E1-E508"
d["latest_erratum"] = 42
d["erratum"] = 42

d["v58_combined_likelihood_key_results"] = {
    "round": "v7.0/v58 (combined likelihood verdict on TUFT +16.26%)",
    "source_output": "_audit_v58_combined_likelihood_out.txt",
    "audit_script": "_audit_v58_combined_likelihood.py",
    "method": "pure stdlib math, NOT importing v56/v57; Gaussian independent residuals; "
              "H0=GR(delta=0) vs H1=TUFT(delta=+16.26%); 90% CI->1sigma = (hi-lo)/(2*1.645); "
              "BF=exp(dlnL) uniform prior; dB=10*log10(BF)",
    "two_sets_not_mixed": {
        "A_naive_6ev": "fixed Mf/chif, ignore M-chi-delta_f degeneracy; 6 events",
        "B_marginalized": "Estelles 2023 published marginalized delta_f220; GW150914 single + six-event joint (nested, NOT combined)"
    },
    "sigma1_pct": {
        "GW150914": 3.435, "GW170104": 4.407, "GW190519": 5.623,
        "GW190521_074359": 3.830, "GW190630": 9.331, "GW190828": 28.024,
        "GW150914_marg_single": 5.471, "sixevent_joint": 2.432
    },
    "combined_results_H1_plus16p26": {
        "naive_6ev": {"d_hat": -4.25, "sig_comb": 2.00, "dlnL": -50.07, "BF": 1.8e-22, "dB": -217.5, "n_excl": 10.23},
        "naive_5ev_noGW190828": {"d_hat": -4.29, "sig_comb": 2.01, "dlnL": -49.98, "BF": 2.0e-22, "dB": -217.1, "n_excl": 10.22},
        "marg_GW150914_single": {"d_hat": 5.00, "sig_comb": 5.47, "dlnL": -1.70, "BF": 0.183, "dB": -7.4, "n_excl": 2.06},
        "marg_sixevent_joint": {"d_hat": 2.00, "sig_comb": 2.43, "dlnL": -16.86, "BF": 4.8e-8, "dB": -73.2, "n_excl": 5.86}
    },
    "conservative_inflate_sigma_x1p5": {
        "naive_6ev_dB": -96.5, "naive_5ev_dB": -96.5,
        "marg_single_dB": -3.3, "marg_joint_dB": -32.5,
        "joint_n_excl": 3.91, "note": "conclusion does NOT flip"
    },
    "sensitive_band_optimistic_delta_plus8p82": {
        "naive_6ev_dB": -82.5, "naive_5ev_dB": -82.5,
        "marg_single_dB": +0.76, "marg_single_BF": 1.19,
        "marg_joint_dB": -15.6, "marg_joint_n_excl": 2.81,
        "note": "even best-case in-band delta=+8.82%; joint still prefers GR; only GW150914 single coin-flip TUFT (+0.76 dB)"
    },
    "verdict": "data strongly prefer GR; TUFT nominal +16.26% excluded by current n0 ringdown data at "
               "~5.9sigma (marginalized joint, cleanest) / ~10.2sigma (naive, optimistic upper bound); "
               "robust to x1.5 error inflation (~3.9sigma joint), does not flip.",
    "three_caveats": [
        "n0 single-mode only; overtones/high-Q/(3,3,0) not included",
        "naive residuals not fully marginalized over M-chi-delta_f (~10sigma is optimistic upper bound)",
        "joint sigma=2.43% may still be underestimated by residual M-chi degeneracy; x1.5 to 3.9sigma is "
        "the conservative ceiling -- NOT inflated further (would be inflating variance to save the theory)"
    ],
    "E508": "combined likelihood verdict: data prefer GR; TUFT nominal +16.26% excluded at ~5.9sigma marginalized joint / "
            "~10.2sigma naive, x1.5 does not flip. Observational likelihood channel; does NOT add new physical E-number to four-state.",
    "erratum": "#42 held (no new erratum)",
    "four_state": "35/61/18/27 frozen",
    "coalition_layer": "2/6 maintained; UFT-3 still unlocked"
}

d["open_backlog"].append(
    "v7.0/v58 combined likelihood verdict (E508; Gaussian independent residuals; H0=GR vs H1=TUFT+16.26%; "
    "data prefer GR: naive 6ev -217.5 dB/10.23sigma, marginalized six-event joint -73.2 dB/5.86sigma; "
    "x1.5 error inflation does NOT flip (joint -32.5 dB/3.9sigma); sensitive-band optimistic delta=+8.82% still "
    "joint -15.6 dB/2.8sigma, only GW150914 single coin-flip +0.76 dB; erratum #42 held; four-state 35/61/18/27 frozen). "
    "Three caveats: n0 single-mode only (no overtones/high-Q/(3,3,0)); naive not fully marginalized M-chi-delta_f; "
    "joint sigma may be underestimated by residual degeneracy (x1.5 ceiling, not inflated further). "
    "OPEN backlog unchanged: (1) TUFT static 11.6-digit hard gate still OPEN (two-domain assembly interface block); "
    "(2) rotating absolute 1.62 no external Grade-A anchor; (3) a>=0.2 slow-rotation O(a^2)~3-4%; "
    "(4) FIVE next-layer items OPEN: P18 e / P19 f_pi / nullity_dyn=0 (Thm H) / Page / Hawking. "
    "Next: O4/Voyager ringdown SNR>=10 with inspiral breaking M-chi-delta_f degeneracy -- if marginalized delta_f220 "
    "90% upper bound stably <+8.8% even the band lower end is excluded; if ~+16%+/-<5% TUFT supported (no current sign). "
    "Deliverables: TUFT_合并似然判决报告.md + _audit_v58_combined_likelihood.py/_out.txt."
)

with io.open(P, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)

d2 = json.load(open(P, encoding="utf-8"))
print("version:", d2["version"])
print("equation_range:", d2["equation_range"])
print("latest_round:", d2["latest_round"])
print("erratum:", d2["latest_erratum"])
print("four_state:", d2["four_state_counts_approx"]["strict"], d2["four_state_counts_approx"]["conditional"],
      d2["four_state_counts_approx"]["definition"], d2["four_state_counts_approx"]["open"])
print("new key present:", "v58_combined_likelihood_key_results" in d2)
print("top-level len():", len(d2))
print("open_backlog len():", len(d2["open_backlog"]))
