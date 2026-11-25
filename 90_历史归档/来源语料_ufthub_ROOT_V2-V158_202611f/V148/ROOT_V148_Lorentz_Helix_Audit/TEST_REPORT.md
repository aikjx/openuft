# ROOT V148 real execution report

Command: `python run_all.py`.

- Python `unittest`: **93 executed, 93 passed**, covering geometry, covariance, Maxwell wave, measured-GM reference calculations, dimensions.
- SymPy exact symbolic checks: **17 assertions passed**.
- Representative results: original `κ=0.6/L0`, `τ=0.8/L0`; for `β=0.8`, `κ'=1.666666666667/L0`, `τ'=0`.
- Under the hypothetical `E=ℏω_geom` assumption, boost factor of `E'/ℏω'_geom` is **0.36** (the relation is not universal).
- Earth spherical surface gravity **9.820250332024 m/s²**; Moon **1.624218876561 m/s²**. Both calculated from **pre-existing JPL GM** and approximate radii, not ROOT-predicted values.
- Exact plane-wave Maxwell residuals were checked analytically and numerically, with both circular polarizations.
- **No empirical satellite-data fit was performed**; no ROOT quantum gravity or four-force unification proof was produced.

Important: tests are correctness checks for the code and mathematical models. They cannot establish the truth of the hypothesized universal physical origin of forces.
