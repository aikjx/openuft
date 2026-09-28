# -*- coding: utf-8 -*-
"""v54 rotating m-split observable: ledger JSON v6.5 -> v6.6 (append-only)."""
import io, json, collections

p = r"D:\a10\aikjx\code\my_lib\openuft\01_独立体系\S16_TUFT归一化主册\13_论文与成果\台账\TUFT_归一化台账_v1.0.json"
d = json.load(io.open(p, encoding="utf-8"), object_pairs_hook=collections.OrderedDict)

assert d["version"] == "v6.5", d["version"]
assert d["latest_round"] == "v6.5_v53_amplitude_anchor"
assert d["equation_range"] == "E1-E503"
assert d["latest_erratum"] == 42

d["version"] = "v6.6"
d["date"] = "2026-09-26"
d["latest_round"] = "v6.6_v54_rotating_msplit"
d["equation_range"] = "E1-E504"
if "last_updated" in d:
    d["last_updated"] = "2026-09-26"

# ---- new key_results block ----
v54 = collections.OrderedDict()
v54["round"] = "v6.6/v54"
v54["organizer_verified"] = True
v54["source_output"] = "_audit_v54_rotating_msplit_observable_out.txt"
v54["method"] = ("Independent re-implementation, no import of any prior-project script; GR gate first; "
                 "no fake closure; mpmath dps=40; numbers copied verbatim from raw output. Rotating m-split "
                 "observable audit channel (does NOT close a new physical E-number into the four-state; "
                 "E504 is an observable-discriminant-channel registration).")
v54["derivation_chain"] = collections.OrderedDict([
    ("slow_rotation_ansatz", "omega(a,m) = omega_0 + m*a*c_per_m + O(a^2); omega_0=static(a=0) fundamental"),
    ("split_observable", "delta_omega(a) = omega(a,+2)-omega(a,-2) = 4 a c_per_m = a*(splitR/a + i splitI/a)"),
    ("split_defs", "splitR/a = 4 Re(c_per_m); splitI/a = 4 Im(c_per_m)"),
    ("GR_anchor_erratum42", collections.OrderedDict([
        ("c_GR_per_m", "(0.0628831 0.001996i)"),
        ("check_4Re", "4 Re(c)=0.2515324 vs splitR/a=0.2515323 (rounding match)"),
        ("splitR_a", 0.2515323), ("splitI_a", 0.007984)])),
    ("TUFT_anchor_v49_a0.1", collections.OrderedDict([
        ("c_TUFT_per_m", "(0.40525 -0.03525i)"),
        ("splitR_a", 1.621), ("splitI_a", -0.141)])),
    ("Hz_conversion_60Msun", collections.OrderedDict([
        ("K_Hz", 538.5416666666667),
        ("K_def", "32312.5/60.0 Hz"),
        ("delta_f_form", "delta_f_Hz = K * Re(delta_omega) = K * a * splitR/a"),
        ("note", "both modes share K(M); slope ratio TUFT/GR is M- and a-independent (linear regime)")])),
    ("GR_limit_a0", collections.OrderedDict([
        ("omega_a0_pm2", "(0.37367168441804166 -0.0889623156889341i)"),
        ("delta_omega_a0", "(0 0i)"),
        ("verdict", "ZERO split at a=0; GR gate PASS")])),
])
v54["numerical_table_60Msun_Hz"] = [
    {"system": "GR", "a_over_M": 0.1, "f_p2_Hz": 208.01, "f_m2_Hz": 194.46, "df_Hz": 13.55, "grade": "CONFIRMED"},
    {"system": "GR", "a_over_M": 0.2, "f_p2_Hz": 214.78, "f_m2_Hz": 187.69, "df_Hz": 27.09, "grade": "EXTRAPOLATED (beyond v49 a<0.1)"},
    {"system": "GR", "a_over_M": 0.3, "f_p2_Hz": 221.56, "f_m2_Hz": 180.92, "df_Hz": 40.64, "grade": "EXTRAPOLATED"},
    {"system": "TUFT", "a_over_M": 0.1, "f_p2_Hz": 277.62, "f_m2_Hz": 190.32, "df_Hz": 87.30, "grade": "CONFIRMED (v49 direct @a=0.1)"},
    {"system": "TUFT", "a_over_M": 0.2, "f_p2_Hz": 321.26, "f_m2_Hz": 146.67, "df_Hz": 174.60, "grade": "EXTRAPOLATED"},
    {"system": "TUFT", "a_over_M": 0.3, "f_p2_Hz": 364.91, "f_m2_Hz": 103.02, "df_Hz": 261.89, "grade": "EXTRAPOLATED"},
]
v54["static_anchors"] = collections.OrderedDict([
    ("GR_w0", "(0.37367168441804166 -0.0889623156889341i)"),
    ("TUFT_w0", "(0.434445178 -0.05644976i)"),
    ("note", "TUFT static fundamental already includes +16.26% frequency shift / -36.6% damping"),
])
v54["discriminant_honest_sign"] = collections.OrderedDict([
    ("suppression_ratio_0.35", "TUFT splitR/a=1.621 / same-cavity GR 2/rho^3=4.662 = 0.3477 ~ 0.35 (naive same-cavity split pressed to 35%)"),
    ("naive_samecavity_over_GR_before_suppression", 18.534398961882828),
    ("TUFT_over_GR_after_0.35_suppression", 6.444500368342356),
    ("honest_sign", "TUFT predicts a LARGER m-split than GR, NOT smaller; 0.35 suppression cuts excess from ~18.534x down to ~6.4445x GR"),
    ("rule", "dual m=+/-2 resolved: slope ~6.4445x GR favors TUFT; ~1x GR favors GR"),
    ("M_a_independence", "slope ratio = TUFT_splitR/a / GR_splitR/a dimensionless; both geometric (M-independent), both linear in a so ratio cancels a"),
    ("direction", "TUFT split excess positive/larger, consistent in sign with v37 EHT c_m anchor"),
    ("concrete_60Msun_a0.1", collections.OrderedDict([
        ("GR_split_Hz", 13.54607), ("TUFT_split_Hz", 87.2976), ("ratio", 6.4445)])),
])
v54["extrapolation_flags"] = collections.OrderedDict([
    ("v49_credible_window", "a/M < 0.1 (direct continuation)"),
    ("a0.1", "within window; v49 direct @a=0.1 splitR/a=1.621367; CONFIRMED"),
    ("a0.2", "EXTRAPOLATED beyond a<0.1; v49 direct @a=0.2 splitR/a=1.569052 vs linear 1.621 ~3.2% drop, O(a^2)~4%; table uses linear ansatz 1.621, nonlinear O(a^2) uncertainty ~3-4%"),
    ("a0.3", "EXTRAPOLATED further; v49 never computed here; pure linear ansatz; O(a^2) grows, order-of-magnitude only"),
])
v54["detectability_tier"] = collections.OrderedDict([
    ("this_signature", "resolving two distinct m modes; needs high SNR to split f(+2) vs f(-2)"),
    ("eps_strict_interval", [0.0748115, 0.469746]),
    ("Voyager_Dmax_strict_Gpc", 2.46),
    ("Voyager_Dmax_toy_Gpc", 15.48),
    ("verdict", "resolvable at LOUD/toy tier (eps~0.4697, D_max up to 15.48 Gpc, face-on); MARGINAL at strict tier (eps=0.0748, 2.46 Gpc) needs nearby events/network"),
])
v54["four_state_grade"] = collections.OrderedDict([
    ("CONFIRMED", "GR limit a=0 zero-split; static anchors w0 verbatim; GR slope splitR/a=0.2515323 (erratum#42); TUFT slope @a=0.1=1.621"),
    ("ESTIMATED", "suppression-ratio net effect 0.35 (cavity-mapping dependent); discriminant ratio 6.44x GR (M-/a-independent)"),
    ("EXTRAPOLATED", "a=0.2/a=0.3 linear ansatz beyond v49 a<0.1 (O(a^2)~3-4%)"),
    ("GATE-HELD", "detectability tier anchored to v53 eps interval / D_max; no new physical E-number closed; erratum#42 HELD (increment not rolled)"),
])
v54["E504"] = ("Rotating m-split observable: TUFT vs GR slope ratio 6.44x, a=0.1 CONFIRMED, a=0.2/0.3 "
               "EXTRAPOLATED, loud tier resolvable. Observable-discriminant-channel registration, NOT added to "
               "physical four-state (35/61/18/27 frozen); erratum #42 held (no new erratum this round).")

# insert after v53_amplitude_anchor_key_results
new_d = collections.OrderedDict()
for k, v in d.items():
    new_d[k] = v
    if k == "v53_amplitude_anchor_key_results":
        new_d["v54_rotating_msplit_key_results"] = v54
d = new_d

# ---- open_backlog: prepend v54 entry ----
ob = d.get("open_backlog", [])
if not isinstance(ob, list):
    ob = [ob]
v54_backlog = (
"v6.6/v54: rotating m-split observable close (E504; organizer-verified; numbers copied verbatim from "
"_audit_v54_rotating_msplit_observable_out.txt; independent re-implementation no import; GR gate first; "
"no fake closure; mpmath dps=40; disk backed up to .v66pre_20260926.bak; starting point v6.5/E1-E503/#42; "
"v6.5 E503 amplitude anchor, v6.4 E502 two-domain refine, v6.3 E501 robust two-domain, v6.2 E500 static push, "
"v6.1 E499 Chandrasekhar+mirror, v6.0 third-spectral-diagnosis NOT rolled back). derivation chain: slow-rotation "
"ansatz omega(a,m)=omega0+m*a*c_per_m+O(a^2); split observable delta_omega=omega(a,+2)-omega(a,-2)=4a c_per_m="
"a*(splitR/a+i splitI/a); GR anchor erratum#42 c_GR=0.0628831+0.001996i, splitR/a=0.2515323, splitI/a=0.007984; "
"TUFT anchor v49 direct @a=0.1 c_TUFT=0.40525-0.03525i, splitR/a=1.621, splitI/a=-0.141; Hz conversion 60 Msun "
"K=32312.5/60=538.5417 Hz, delta_f=K*a*splitR/a; GR limit a=0 => delta_omega=0 ZERO split PASS. numerical table "
"60 Msun Hz: GR a=0.1 208.01/194.46/13.55, a=0.2 214.78/187.69/27.09, a=0.3 221.56/180.92/40.64; TUFT a=0.1 "
"277.62/190.32/87.30, a=0.2 321.26/146.67/174.60, a=0.3 364.91/103.02/261.89 (TUFT static w0 already +16.26% "
"freq/-36.6% damping). discriminant honest sign: 0.35 suppression net = TUFT 1.621 / same-cavity GR 2/rho^3 "
"4.662 = 0.3477~0.35; vs real GR baseline 0.2515323: naive same-cavity/GR=18.53x before suppression, "
"TUFT/GR=6.44x after 0.35 suppression; TUFT m-split is LARGER than GR by ~6.44x NOT smaller; dual m modes "
"slope ~6.44x GR favors TUFT, ~1x favors GR; ratio dimensionless geometric, M-independent, a-independent in "
"linear regime; direction positive excess consistent with v37 EHT c_m anchor. extrapolation: a=0.1 within v49 "
"credible a<0.1 CONFIRMED; a=0.2 EXTRAPOLATED (v49 direct splitR/a=1.569 vs linear 1.621 ~3.2% drop O(a^2)~4%); "
"a=0.3 further extrapolated, order-of-magnitude only. detectability: eps_strict [0.0748,0.4697], Voyager Dmax "
"strict 2.46 / toy 15.48 Gpc; resolvable at loud/toy tier (eps~0.4697 up to 15.48 Gpc), marginal at strict tier "
"(2.46 Gpc) needs nearby events/network. four-state: CONFIRMED (a=0 zero split, static anchors, GR slope 0.2515323 "
"#42, TUFT slope @a=0.1 1.621) / ESTIMATED (0.35 net, 6.44x) / EXTRAPOLATED (a=0.2/0.3) / GATE-HELD (tier anchored "
"to v53 eps/Dmax); erratum #42 held no new erratum; physical four-state 35/61/18/27 frozen. OPEN backlog carried: "
"TUFT static 11.6-digit hard gate still OPEN (8.4 digits/<1e-6 reached, two-domain not through GR gate B); rotating "
"absolute 1.62 still no external Grade-A anchor (only v54 internal cross-check; robust=0.35 suppression/6.44x "
"discriminant); a>=0.2 slow-rotation first-order distortion O(a^2)~3-4%; source-excitation e/f_pi next-layer term "
"still OPEN (inherited from v6.5). next step: multi-event/network resolve dual-m slope ratio (loud tier), and dps=50 "
"rotating recheck once two-domain static hard gate closes. merge report: TUFT_v54_旋转m频裂合并报告.md."
)
ob.insert(0, v54_backlog)
d["open_backlog"] = ob

# ---- four_state note append ----
fsc = d.get("four_state_counts_approx")
if isinstance(fsc, dict) and "note" in fsc:
    add = (" v6.6/v54 round: E504 (rotating m-split observable: slow-rotation linear ansatz delta_omega=4a c_per_m; "
           "GR anchor erratum#42 splitR/a=0.2515323, TUFT v49 @a=0.1 splitR/a=1.621; after 0.35 same-cavity suppression "
           "TUFT/GR=6.44x, honest sign TUFT m-split LARGER than GR not smaller; dual-m slope ~6.44x GR favors TUFT / "
           "~1x favors GR, dimensionless M-/a-independent; a=0.1 CONFIRMED, a=0.2/0.3 linear extrapolation order-of-magnitude "
           "only; resolvable at loud/toy tier eps~0.4697 Voyager Dmax up to 15.48 Gpc, marginal at strict 2.46 Gpc) is an "
           "observable-discriminant channel, NOT added to physical four-state; 35/61/18/27 remain frozen; erratum #42 held "
           "(no new erratum).")
    fsc["note"] = fsc["note"] + add

io.open(p, "w", encoding="utf-8", newline="\n").write(
    json.dumps(d, ensure_ascii=False, indent=2))

# verify reload
d2 = json.load(io.open(p, encoding="utf-8"))
print("RELOAD OK")
print("version=", d2["version"])
print("latest_round=", d2["latest_round"])
print("equation_range=", d2["equation_range"])
print("date=", d2["date"], "last_updated=", d2.get("last_updated"))
print("v54 key_results present:", "v54_rotating_msplit_key_results" in d2)
print("open_backlog[0] head:", d2["open_backlog"][0][:60])
print("four_state counts:", d2["four_state_counts_approx"]["strict"], d2["four_state_counts_approx"]["conditional"], d2["four_state_counts_approx"]["definition"], d2["four_state_counts_approx"]["open"])
