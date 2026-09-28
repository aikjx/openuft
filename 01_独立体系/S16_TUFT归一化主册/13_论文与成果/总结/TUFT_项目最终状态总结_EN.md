# TUFT Unified Field Theory — Final Project Status (as of v7.5 / E513+)

> This is a handoff note: the complete arc from construction to observational falsification,
> the toolchain, and what remains. Authoritative sources:
> `TUFT_归一化主册_v1.0.md` (SSOT) and `TUFT_归一化台账_v1.0.json`.

## 1. What the theory is

TUFT (Topological Unified Field Theory) derives a black-hole mirror-wall model from the
Frenet–Serret frame and the Călugăreanu–White twist. Outer geometry
g_tt=e^{−2U}, g_rr=−e^{2U}(1+c_m/ρ²+d/ρ³), with strict-zone parameters
c_m=−0.29, d=−0.05, ρ_h=0.609902M, R=3.268M, Vmax=0.148709.
Core observable prediction: the n0 ringdown complex frequency is shifted by +16.26% in
frequency and +57.6% in damping time relative to GR.

## 2. What was achieved numerically (all independently recomputed, reproducible)

- GR anchors at a=0: n0=0.3736716844−0.0889623157i, n1=0.346710997−0.2739148753i,
  independently reproduced via Leaver continued fraction to 14.8 / 13.1 digits.
- TUFT Grade-A pole: ω=0.434445178−0.056449760i, cross-validated by Beyn contour and
  multi-domain spectral methods to ~9 digits.
- Rotation: slow-spin m=±2 splitting passes GR gate A/B (n0 12.6 digits, slope 7.7 digits);
  TUFT splitting is ~6.44× the real GR value (at a=0.1).
- Full chain 33/33 internally consistent; conversion constants verified from first principles
  (M_sun_sec=G·M☉/c³=4.92564e-6 s).

## 3. Observational verdict (the endpoint)

Using published gravitational-wave ringdown measurements
(Estelles 2023 / Abbott 2016 / Capano 2021) with combined likelihood:

| Channel | TUFT predicts | Data | Exclusion |
|---|---|---|---|
| n0 frequency | +16.26% | +2.0±2.4% (0.82σ from GR) | **excluded at 5.86σ** |
| n0 damping | +57.6% | +10.0±8.5% (1.17σ from GR) | **excluded at 5.59σ** |
| n1 overtone | +16.26% | −5%±20% (GR side, too broad to resolve) | uninformative |

- Residuals are consistent with GR and favor GR in every likelihood combination.
- Parameter retreat: fitting the data requires c_m≈−0.1, outside the EHT-anchored band
  [−0.369,−0.218]; within the whole EHT band the frequency and damping channels demand
  mutually exclusive c_m. Tuning cannot rescue the nominal point.

**Conclusion: TUFT's core observable prediction is excluded by existing O3 data.
The theory is self-consistent but not supported by current observations.**

## 4. Items that cannot close inside the axioms (proven dead-ends)

e (P18), f_π (P19), nullity_dyn=0 (Theorem H), the Page budget, and the Hawking spectrum.
These require new physics or external hadronic/experimental anchors; no further numeric
round will close them.

## 5. Delivered tool: O4 auto-judgment script

`scripts/o4/tuft_ringdown_judge.py` (stdlib only): a CSV of new events → residuals,
combined likelihood, Bayes factor, exclusion significance, c_m inversion, and a four-way
verdict (SUPPORT / EXCLUDE / GR_WEAK / NO_RESOLUTION).

- `regression_marginalized.csv`: reproduces 5.86/5.59σ EXCLUDE.
- `regression_events.csv`: per-event pooling reproduces 9.04σ EXCLUDE.
- Two bugs fixed (per-event regression artifact; verdict-branch fall-through);
  constants first-principles verified; JSON structure validated.

**Usage**: when O4/Voyager reports a ringdown event with SNR≳10, fill
`M_f/a_f/δf/σ/δτ/σ` and run
`python tuft_ringdown_judge.py --input o4_events.csv --output o4_result.json`.

## 6. The only two things that can change the verdict

1. **O4 new data**: a high ringdown-SNR event that breaks the M–χ–overtone degeneracy,
   re-judged with the script above.
2. **Changing the axioms**: deliberately alter the mirror-wall boundary / amplitude /
   parameter premise and restart.

> The verdict is in and the tool is ready. What remains is an experimental or axiomatic
> decision, not a numerical one.
