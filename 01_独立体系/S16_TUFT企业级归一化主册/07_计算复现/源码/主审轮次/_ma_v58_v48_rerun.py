# -*- coding: utf-8 -*-
import json, io
ledger = 'TUFT_归一化台账_v1.0.json'
d = json.load(io.open(ledger, encoding='utf-8-sig'))
d['main_agent_v58_v48_rerun'] = {
    "round": "MainAgent independent re-run of organizer v48 rotating QNM Beyn audit",
    "date": "2026-09-24",
    "method": "Read _audit_v48_rotating_qnm.py source first (self-contained: numpy/scipy only, no qnm import, no prior-project import); re-ran in project .venv, exit 0, ALL numbers reproduced digit-for-digit (incl. rewritten _audit_v48_rotating_qnm_out.txt identical)",
    "results": {
        "GR_gate_A": "PASS |err|=2.470e-13 (n0 12 digits) reproduced",
        "GR_gate_B": "FAIL reproduced: Rayleigh split/a=0.0962 vs target 0.25153; continuation max|Im drift|=1.54e-2 (target <5e-3); direct pole jumps under O(a)",
        "TUFT_static_anchor": "0.434445174-0.056449760i vs Grade A 0.434445178-0.056449760i |d|=4.503e-9 reproduced",
        "TUFT_rotating": "UNTRUSTED (GR gate B not passed; iron law forbids physical reading) - raw diagnostic split/a@0.10=0.1045 @0.20=-0.3431 NOT validated prediction",
        "condition_wall": "DETECTED sigma_min(L)=7.72e-12",
        "organizer_diagnosis": "missing O(a) imaginary Teukolsky cross-term 4i(r-1)K/Delta; needs full Chandrasekhar transform into Jansen-compactified pencil"
    },
    "verdict": "v48 IS the first genuinely disk-backed rotating-QNM attempt and it is an HONEST FAIL. It directly CONTRADICTS organizer v44's unsupported claim (GR gate A/B PASS 12.6/7.2 digits, TUFT m-splitting 0.09832): v44 has no script and no out on disk, v48 (same methodology family) gives FAIL. TUFT rotating m-splitting remains OPEN. T01 correct path confirmed = full deturbed Teukolsky -> Jansen embedding (O(a) operator with K=(r^2+a^2)w-am, (2rw-m) derivative coupling, Cook-Zhang sA_lm O(a) diagonal -2Sma w, ingoing horizon Omega_H); zero free constants; solver path must NOT import qnm, must NOT hardcode 0.0628831/0.2515323, must reproduce n0>=11.6 digits and 0.2515323>=4 digits in GR/ingoing-horizon limit BEFORE any TUFT reflecting-wall numbers.",
    "note": "v5.3-v5.5/v5.7 numeric layers remain UNVERIFIED (no disk evidence); v48 disk-backed honest FAIL retained append-only"
}
json.dump(d, io.open(ledger, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ledger keys', len(d), 'version', d.get('version'))
