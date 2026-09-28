# -*- coding: utf-8 -*-
"""v60 泛音 n1 检验：台账追加 E510，升版 v7.1->v7.2。append-only，不动四态/勘误。"""
import json, io

P = r"D:\a10\aikjx\code\my_lib\openuft\01_独立体系\S16_TUFT企业级归一化主册\13_论文与成果\台账\TUFT_归一化台账_v1.0.json"
d = json.load(open(P, encoding="utf-8"))

d["version"] = "v7.2"
d["date"] = "2026-09-26"
d["last_updated"] = "2026-09-26"
d["latest_round"] = "v7.2_v60_overtone_n1_likelihood"
d["equation_range"] = "E1-E510"
d["latest_erratum"] = 42
d["erratum"] = 42

d["v60_overtone_n1_likelihood_key_results"] = {
    "round": "v7.2/v60 (independent n=1 overtone channel after n0 rejected)",
    "source_output": "_audit_v60_overtone_likelihood_out.txt",
    "audit_script": "_audit_v60_overtone_likelihood.py",
    "method": "pure stdlib math, NOT importing v56/v57/v58/v59; Kerr (2,2,1) table hardcoded from qnm 0.4.4 (a=0 anchor "
              "0.346710996879-0.273914875291i matches SSOT to 12 digits); frequency H0=GR(df=0) vs H1=TUFT(df=+16.26%, v32 same "
              "proportion as n0); damping H0=GR(dt=0) vs H1=TUFT(dt=+57.6%, tau ratio 1.576 same as n0)",
    "data_source": "ONLY published n=1 overtone direct measurement = GW150914 single event: Isi et al. 2019 PRL 123 111102 "
                   "(arXiv:1905.00869; task's 1909.06188 was a math paper, transparently corrected, no SSOT number changed) "
                   "no-hair test: df1=-0.05+/-0.20 (68%=1sigma=20%); dt1 unconstrained [-6%,+100%]; no-hair vs floating BF=1.75. "
                   "Estelles 2023 only measures n0 (overtones fixed GR); Capano 2021 = GW190521 (3,3,0) NOT n1. "
                   "Overtone detection itself not robust: fully marginalized BF=2.3+/-0.1 (PRD110 L041501 2024).",
    "GR_reduction_GW150914": {"Mf_Msun": 68.0, "chi": 0.63, "f221_GR_Hz": 233.3, "tau221_GR_ms": 1.332},
    "frequency_channel_H1_plus16p26": {
        "med_pct": -5.0, "sig1_pct": 20.0, "dlnL": -0.534, "BF": 0.586, "dB": -2.32, "n_excl": 1.06,
        "conservative_x1p5_dB": -1.03, "conservative_x1p5_n": 0.71,
        "optimistic_cm_edge_df_plus8p82_dB": -0.90, "optimistic_cm_edge_df_plus8p82_n": 0.69,
        "note": "data lean GR weakly; TUFT +16.26% only 1.06 sigma away, NOT excluded"
    },
    "damping_channel_H1_plus57p6": {
        "med_pct": 0.0, "sig1_pct": 32.2, "dlnL": -1.598, "BF": 0.202, "dB": -6.94, "n_excl": 1.79,
        "conservative_x1p5_dB": -3.09, "conservative_x1p5_n": 1.19,
        "optimistic_cm_edge_dt_plus47p5_dB": -4.72, "optimistic_cm_edge_dt_plus47p5_n": 1.48,
        "note": "published band [-6,+100] brackets both GR(0) and TUFT(+57.6%); UNINFORMATIVE; Isi no-hair BF=1.75 leans GR"
    },
    "three_ending_grading": {
        "n1_also_excluded": "NO (frequency 1.06sigma, damping 1.79sigma, neither significant)",
        "n1_compatible_GR_deviate_TUFT": "YES - residual med=-5% on GR side (0.25sigma from GR), no positive freq-shift or long "
                                        "damping pointing to TUFT; aligned with n0; but resolution-limited (+/-20%), cannot independently exclude TUFT",
        "n1_outlier_near_TUFT_contradicting_n0": "NO - med=-5% not +16%; no outlier"
    },
    "three_channel_verdict": "n0 frequency (v58 @5.86sigma) + n0 damping (v59 @5.59sigma) already cleanly reject TUFT complex "
                             "spectrum; n1 high overtone falls on GR side (-5%) but 1sigma=20% too wide and detection not robust "
                             "(BF~2.3); NEITHER independently excludes TUFT NOR resurrects it; no contradiction with n0. "
                             "Do NOT resurrect theory on n1; do NOT overstate as third independent exclusion.",
    "E510": "overtone n=1 independent channel: only GW150914 measurement df1=-5%+/-20% on GR side; TUFT +16.26% only 1.06sigma "
            "(not significant), damping unconstrained; compatible with GR / resolution-limited / no outlier / no resurrection. "
            "Observational likelihood channel; NOT in four-state.",
    "erratum": "#42 held (no new erratum; task's arXiv:1909.06188 was a citation typo, correct arXiv:1905.00869, no SSOT number affected)",
    "four_state": "35/61/18/27 frozen",
    "coalition_layer": "2/6 maintained; UFT-3 still unlocked"
}

d["open_backlog"].append(
    "v7.2/v60 overtone n=1 independent channel (E510; independent Gaussian likelihood, NOT importing v58/v59; Kerr (2,2,1) "
    "from qnm 0.4.4). Only published n=1 measurement = GW150914 Isi2019 PRL123 111102 (arXiv:1905.00869): df1=-5%+/-20% (1sigma), "
    "dt1 unconstrained [-6,+100], no-hair BF=1.75. GR reduction (68Msun, chi=0.63): f221=233.3 Hz, tau221=1.332 ms. "
    "Frequency channel H1=+16.26%: dB=-2.32, excluded 1.06sigma (x1.5: 0.71sigma; optimistic +8.82%: 0.69sigma). "
    "Damping channel H1=+57.6%: dB=-6.94, 1.79sigma (uninformative band). Three endings: n1 NOT excluded, n1 compatible GR "
    "(med=-5%, GR side), no TUFT outlier. Three-channel: n0 freq 5.86sigma + n0 damp 5.59sigma reject TUFT; n1 on GR side but "
    "resolution-limited, neither excludes nor resurrects; no contradiction. erratum #42 held; four-state 35/61/18/27 frozen. "
    "OPEN backlog unchanged: (1) TUFT static 11.6-digit hard gate OPEN; (2) rotating absolute 1.62 no external anchor; "
    "(3) a>=0.2 slow-rotation O(a^2)~3-4%; (4) FIVE next-layer items OPEN. Deliverables: TUFT_v60_泛音n1检验合并报告.md + "
    "_audit_v60_overtone_likelihood.py/_out.txt."
)

with io.open(P, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)

d2 = json.load(open(P, encoding="utf-8"))
print("version:", d2["version"])
print("equation_range:", d2["equation_range"])
print("latest_round:", d2["latest_round"])
print("erratum:", d2["latest_erratum"])
print("new key present:", "v60_overtone_n1_likelihood_key_results" in d2)
print("top-level len():", len(d2))
print("open_backlog len():", len(d2["open_backlog"]))
