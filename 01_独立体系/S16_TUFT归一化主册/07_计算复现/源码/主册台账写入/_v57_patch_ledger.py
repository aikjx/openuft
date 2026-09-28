# -*- coding: utf-8 -*-
"""v57 GR n0 锚独立复算：台账追加 E507，升版 v6.8->v6.9。append-only，不动四态/勘误。"""
import json, io

P = r"D:\a10\aikjx\code\my_lib\openuft\01_独立体系\S16_TUFT归一化主册\13_论文与成果\台账\TUFT_归一化台账_v1.0.json"
d = json.load(open(P, encoding="utf-8"))

# 升版字段
d["version"] = "v6.9"
d["date"] = "2026-09-26"
d["last_updated"] = "2026-09-26"
d["latest_round"] = "v6.9_v57_gr_n0_leaver"
d["equation_range"] = "E1-E507"
# 勘误不递增：本轮为 GR 门独立复算通道，无 SSOT 数值错误
d["latest_erratum"] = 42
d["erratum"] = 42

d["v57_gr_n0_leaver_key_results"] = {
    "round": "v6.9/v57 (GR Schwarzschild (2,2,n) Leaver independent recalculation anchor)",
    "source_output": "_audit_v57_gr_n0_leaver_out.txt",
    "audit_script": "_audit_v57_gr_n0_leaver.py",
    "method": "mpmath dps=50, not importing prior-project scripts; first-principles Leaver continued fraction",
    "leaver_derivation_chain": {
        "M": 1, "s": -2, "l": 2, "m": 2, "lambda": 4,
        "Delta": "r^2-2r", "K": "r^2*omega",
        "ansatz": "R=exp(i*omega*r*) * (r-2)^(2-2i*omega) * r^(-2) * sum(a_n z^n), z=(r-2)/r; horizon ingoing, infinity outgoing",
        "recurrence": "three-term alpha_n a_n + beta_n a_{n-1} + gamma_n a_{n-2} = 0",
        "alpha_n": "n^2 + (4-4i*omega)*n + (3-4i*omega)",
        "beta_n": "-2*n^2 + (-2+16i*omega)*n + (-3+8i*omega+32*omega^2)",
        "gamma_n": "n^2 + (-2-8i*omega)*n + (-16*omega^2+8i*omega)",
        "continued_fraction": "r_n = -gamma_{n+1}/(beta_{n+1}+alpha_{n+1}*r_{n+1}), bottom-up, r_N=0 tail",
        "spectral_condition": "C_0(omega) = beta_0 + alpha_0*r_0 = 0"
    },
    "v56_nonconvergence_diagnosis": {
        "note": "v56 three hard errors, NOT tail direction/branch cut/Gamma phase",
        "err1": "diagonal missing omega dependence: v56 a(n)=(n-1)^2-5 has NO omega; correct alpha_n must carry (4-4i*omega)n+(3-4i*omega)",
        "err2": "spectral condition normalization wrong: v56 returned 1+b(0)/g; correct is beta_0+alpha_0*r_0=0",
        "err3": "coupling structure wrong: v56 b(n)c(n+1) asymmetric coupling, incompatible with alpha/beta/gamma three-term structure"
    },
    "n0_recalculation": {
        "initial_guess": "0.40 - 0.10i", "N": 200,
        "w_n0": "0.37367168441804183578 - 0.08896231568893569827i",
        "abs_C0_root": "7.2e-51",
        "abs_err_vs_Berti": "1.6079e-15",
        "significant_digits": 14.79,
        "target_digits": 10,
        "verdict": "PASS (>=10 digits)"
    },
    "n1_second_check": {
        "initial_guess": "0.35 - 0.27i", "N": 200,
        "w_n1": "0.34671099687916531122 - 0.27391487529123308730i",
        "abs_C0_root": "1.93e-50",
        "abs_err_vs_Berti": "8.0613e-14",
        "significant_digits": 13.09,
        "note": "second independent cross-check, consistent"
    },
    "N_convergence_spread": {
        "n0": {"N=50": "8.56e-11", "N=100": "9.93e-15", "N=200": "1.61e-15", "N=400": "1.61e-15",
               "note": "N=200->400 step 2.2e-20 plateau reached"},
        "n1": {"N=50": "4.35e-8", "N=100": "4.22e-11", "N=200": "8.06e-14", "N=400": "7.97e-14",
               "note": "tail=0 cutoff plateau ~1e-13; Nollert tail could push further"}
    },
    "gap_closure": "v6.8/v56 honestly flagged first-principles Leaver did NOT converge to a=0 anchor (3 coefficient trials landed wrong roots); "
                   "a=0 anchor was cited from published Leaver(1985)/Berti table. v57 rewrote with correct alpha/beta/gamma closed form + bottom-up "
                   "continued fraction + C_0=0 spectral condition; n0 reaches 14.8 digits (>=10 target) PASS, n1 second check 13.1 digits cross-validated. "
                   "Observational test report a=0 anchor UPGRADED from [cited-anchor(Berti table)] to [independently-recalculated-anchor]; v56 self-declared gap closed.",
    "E507": "GR Schwarzschild n0 anchor independent recalculation 14.8 digits PASS; v56 self-declared gap closed; n1 second check 13.1 digits. "
            "Gate/methodology channel; does NOT add new physical E-number to four-state.",
    "erratum": "#42 held (no new erratum — no SSOT numerical error)",
    "four_state": "35/61/18/27 frozen",
    "coalition_layer": "2/6 maintained; UFT-3 still unlocked"
}

# open_backlog 追加 v57 条目
d["open_backlog"].append(
    "v6.9/v57 GR n0 anchor independent recalculation (E507; Leaver CF first-principles; n0 14.8 digits PASS >=10 target, n1 13.1 digits second check; "
    "v56 self-declared gap CLOSED — a=0 anchor upgraded from cited Berti table to independently recalculated; erratum #42 held; four-state 35/61/18/27 frozen). "
    "OPEN backlog unchanged: (1) TUFT static 11.6-digit hard gate still OPEN (8.4 digits/<1e-6 reached; two-domain assembly not through GR gate B only 1.05 digits FAIL — "
    "this round GR gate A independent Leaver 14.8 digits PASS verifies solver correctness, two-domain assembly interface matching block remains first obstacle); "
    "(2) rotating absolute value 1.62 still no external Grade-A anchor (only v54 internal cross-check; robust = 0.35 suppression/6.44x discriminant); "
    "(3) a>=0.2 slow-rotation first-order asymptotic distortion O(a^2)~3-4%; "
    "(4) FIVE next-layer items all OPEN: P18 e / P19 f_pi / nullity_dyn=0 (Theorem H) / Page three resources / Hawking thermal spectrum. "
    "Deliverables: TUFT_v57_GR_n0锚复算合并报告.md + _audit_v57_gr_n0_leaver.py/_out.txt."
)

with io.open(P, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)

# 实测 len() / json.load 合法
d2 = json.load(open(P, encoding="utf-8"))
print("version:", d2["version"])
print("equation_range:", d2["equation_range"])
print("latest_round:", d2["latest_round"])
print("erratum:", d2["latest_erratum"])
print("four_state:", d2["four_state_counts_approx"]["strict"], d2["four_state_counts_approx"]["conditional"],
      d2["four_state_counts_approx"]["definition"], d2["four_state_counts_approx"]["open"])
print("new key present:", "v57_gr_n0_leaver_key_results" in d2)
print("top-level len():", len(d2))
print("open_backlog len():", len(d2["open_backlog"]))
