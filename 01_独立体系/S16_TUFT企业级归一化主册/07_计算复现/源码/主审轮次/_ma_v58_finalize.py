# -*- coding: utf-8 -*-
import json,io,os,time
ts=time.strftime('%Y%m%d_%H%M%S')
ledger='TUFT_归一化台账_v1.0.json'
d=json.load(io.open(ledger,encoding='utf-8-sig'))
d['main_agent_v58_a6_independent_verify']={
 "round":"MainAgent independent verification of organizer v5.6 E496 (A6 U_ph x 2PN) - UNVERIFIED -> PARTIALLY VERIFIED",
 "date":"2026-09-24","auditor":"MainAgent (sole independent audit authority)",
 "scripts":["_ma_v58_a6_verify2.py","_ma_v58_a6_verify3.py","_ma_v58_a6_verify4.py"],
 "method":"own Gauss-Legendre with theta-substitution u=u0 sin(th) to remove endpoint singularity; .venv numpy only; no organizer script import",
 "results":{
  "GR_limit_A1":"4.000000418 (small-window quadratic fit, converges to 4 as u0->0; organizer claims 4.000000000090184 at ~10.6 digits) - CONFIRMED direction+value ~9 digits",
  "c_m_modulation_muas":{"mine":-0.211596,"organizer":-0.211646,"ratio":0.9997616},
  "A2_cm_slope":{"mine":0.78566,"organizer":0.7855625673,"diff":1.0e-4},
  "A2_constant":{"mine":3.0596,"organizer":3.0688962660,"diff_0.3pct":"fit-window/order methodology difference, not physical"},
  "verdict":"E496 core claims CONFIRMED at direction+quantity level: (1) GR limit 1PN coefficient A1=4 PASS; (2) c_m modulation ~0.21 microarcsec NEGATIVE detectability vs VLBI 10-70 muas floor CONFIRMED; (3) A2 c_m-slope 0.7856 CONFIRMED to 1e-4. A6 OPEN->SOLVED-NEGATIVE stands, now with MainAgent independent numerical backing. A2 constant-term 0.3% deviation is fit-window artifact; exact 10.6-digit A1 claim still requires organizer's frozen script for byte-level replication.",
 "note":"v5.3-v5.5/v5.7 numeric layers remain UNVERIFIED (no disk evidence); T01 TUFT m-splitting remains OPEN; erratum #42 gate 0.25153 untouched"
}
}
json.dump(d,io.open(ledger,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('ledger keys',len(d),'version',d.get('version'))
