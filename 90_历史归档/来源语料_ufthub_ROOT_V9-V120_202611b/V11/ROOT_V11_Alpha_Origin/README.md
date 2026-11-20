# ROOT V11 | Alpha origin reproducible audit

Run: `python verify_v11.py`

Files:
- `ROOT_V11_常数本源与几何选择审计.md`: main analytical report (Chinese)
- `verify_v11.py`: SymPy symbolic identities, 50,000 random geometry cases, 90-digit candidate checks, finite-difference sensitivity test, RG illustration, and figures.
- `results.json`: machine-readable numeric output.
- `run_log.txt`: actual command stdout.
- `geometry_continuum.png`: non-unique curvature/torsion ratios.
- `candidate_sigma.png`: candidate proximity compared with CODATA 2022 experimental uncertainty.

Important: The accuracy of a mathematical identity / candidate numerical root is not a physical derivation of α. NIST CODATA α is an INPUT for dimensional-scale and impedance identity audits, not an OUTPUT of ROOT geometry. The quartic and Li candidates do not input α to their math equations, but their physical foundations and independent predictive status remain unproven.
