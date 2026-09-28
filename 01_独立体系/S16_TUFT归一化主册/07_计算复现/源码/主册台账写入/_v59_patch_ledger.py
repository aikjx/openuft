# -*- coding: utf-8 -*-
"""v59 阻尼 tau 检验：台账追加 E509，升版 v7.0->v7.1。append-only，不动四态/勘误。"""
import json, io

P = r"D:\a10\aikjx\code\my_lib\openuft\01_独立体系\S16_TUFT归一化主册\13_论文与成果\台账\TUFT_归一化台账_v1.0.json"
d = json.load(open(P, encoding="utf-8"))

d["version"] = "v7.1"
d["date"] = "2026-09-26"
d["last_updated"] = "2026-09-26"
d["latest_round"] = "v7.1_v59_damping_likelihood"
d["equation_range"] = "E1-E509"
d["latest_erratum"] = 42
d["erratum"] = 42

d["v59_damping_likelihood_key_results"] = {
    "round": "v7.1/v59 (independent combined likelihood on damping-time second prediction)",
    "source_output": "_audit_v59_damping_likelihood_out.txt",
    "audit_script": "_audit_v59_damping_likelihood.py",
    "method": "pure stdlib math, NOT importing v56/v57/v58; Kerr (2,2,0) |w_I|(chi) hardcoded from qnm/Berti; "
              "H0=GR(d_tau=0) vs H1=TUFT(d_tau=+57.6%); tau ratio=|w_I,GR|/|w_I,TUFT|=0.088962316/0.056449760=1.57596; "
              "90% CI->1sigma; BF=exp(dlnL); dB=10log10(BF)",
    "data_source": "Estelles 2023 CQG (arXiv:2104.01906) Table 2 tau220, same 6 events as v56 frequency; "
                   "published marginalized delta_tau220 Eq.13/15",
    "tau_ratio": 1.57596,
    "H1_dtau_pct": 57.6,
    "combined_results_H1_plus57p6": {
        "naive_6ev": {"d_hat": 9.66, "sig": 8.30, "dlnL": -16.01, "BF": 1.1e-7, "dB": -69.5, "n_excl": 5.78},
        "naive_5ev_noGW190828": {"d_hat": 10.40, "sig": 8.45, "dlnL": -14.83, "BF": 3.6e-7, "dB": -64.4, "n_excl": 5.58},
        "marg_GW150914_single": {"d_hat": 7.00, "sig": 14.89, "dlnL": -5.66, "BF": 3.5e-3, "dB": -24.6, "n_excl": 3.40},
        "marg_sixevent_joint": {"d_hat": 10.00, "sig": 8.51, "dlnL": -14.95, "BF": 3.2e-7, "dB": -64.9, "n_excl": 5.59}
    },
    "conservative_inflate_x1p5": {
        "naive_6ev_dB": -30.9, "naive_5ev_dB": -28.6,
        "marg_single_dB": -10.9, "marg_joint_dB": -28.9,
        "joint_n_excl": 3.73, "note": "conclusion does NOT flip"
    },
    "optimistic_cm_edge": {
        "d_tau_opt_pct": 47.5, "joint_dB": -39.2, "joint_n_excl": 4.41,
        "note": "SSOT did not tabulate damping sensitivity band; pro-TUFT transparent shrink of tau ratio 1.576->1.475 "
                "from frequency lower-edge c_m; joint still prefers GR"
    },
    "dual_channel_verdict": "frequency (+16.26%, v58 @5.86sigma) AND damping (+57.6%, v59 @5.59sigma) both excluded by "
                            "current ringdown data; residuals consistent with GR; TUFT n0 complex spectrum (both Re and Im) "
                            "signature as a whole not supported; no contradiction",
    "caveats": ["n0 single-mode only", "naive fixed Mf/chif (5.6-5.8sigma optimistic upper bound; cleanest=joint 5.59sigma)",
                "joint sigma=8.5% may be underestimated by residual degeneracy; x1.5 to 3.73sigma ceiling not inflated further",
                "c_m damping band not tabulated; +47.5% is pro-TUFT transparent estimate"],
    "E509": "damping second prediction: data prefer GR; TUFT +57.6% excluded at ~5.6sigma marginalized joint / ~5.8sigma naive, "
            "x1.5 does not flip; alongside frequency channel => n0 complex spectrum dual-channel both rejected. Observational likelihood channel; NOT in four-state.",
    "erratum": "#42 held (no new erratum)",
    "four_state": "35/61/18/27 frozen",
    "coalition_layer": "2/6 maintained; UFT-3 still unlocked"
}

d["open_backlog"].append(
    "v7.1/v59 damping-tau second prediction (E509; independent Gaussian likelihood, NOT importing v58; H0=GR(dtau=0) vs "
    "H1=TUFT(tau ratio 1.576 = +57.6%); tau ratio=|wI,GR|/|wI,TUFT|=0.088962316/0.056449760). Data=Estelles 2023 Table 2 "
    "tau220 (same 6 events as v56) + marginalized delta_tau220 Eq.13/15. Results: naive 6ev -69.5 dB/5.78sigma, "
    "marginalized six-event joint -64.9 dB/5.59sigma; x1.5 error inflation does NOT flip (joint -28.9 dB/3.73sigma); "
    "optimistic c_m edge dtau=+47.5% still joint -39.2 dB/4.4sigma. erratum #42 held; four-state 35/61/18/27 frozen. "
    "DUAL-CHANNEL: frequency (+16.26%, v58 @5.86sigma) AND damping (+57.6%, v59 @5.59sigma) both excluded; residuals "
    "consistent with GR; TUFT n0 complex spectrum (Re+Im) signature as a whole not supported, no contradiction. "
    "Caveats: n0 single-mode only; naive fixed Mf/chif optimistic upper bound; joint sigma may be underestimated (x1.5 "
    "ceiling not inflated further); c_m damping band not tabulated. OPEN backlog unchanged: (1) TUFT static 11.6-digit hard "
    "gate OPEN; (2) rotating absolute 1.62 no external Grade-A anchor; (3) a>=0.2 slow-rotation O(a^2)~3-4%; (4) FIVE "
    "next-layer items OPEN. Deliverables: TUFT_v59_阻尼τ检验合并报告.md + _audit_v59_damping_likelihood.py/_out.txt."
)

with io.open(P, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)

d2 = json.load(open(P, encoding="utf-8"))
print("version:", d2["version"])
print("equation_range:", d2["equation_range"])
print("latest_round:", d2["latest_round"])
print("erratum:", d2["latest_erratum"])
print("new key present:", "v59_damping_likelihood_key_results" in d2)
print("top-level len():", len(d2))
print("open_backlog len():", len(d2["open_backlog"]))
