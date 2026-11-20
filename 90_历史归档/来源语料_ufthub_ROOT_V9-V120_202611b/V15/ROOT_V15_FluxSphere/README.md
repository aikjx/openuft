# ROOT V15 — Reproducible 6D flux-sphere audit

Run with Python 3, `sympy`, `mpmath`, `numpy`, `matplotlib`:

```bash
python verify_v15.py
```

Files:
- `ROOT_V15_六维磁通稳定化全链路审计.md`: full derivation, assumptions, limitations, sources
- `verify_v15.py`: reproducible symbolic and numerical checks
- `results.json`: input distinction, symbolic checks, 70-digit numerical sweep
- `run_log.txt`: program output
- `flux_sweep.csv`: numerical parameter sweep
- `radion_potential.png`: normalized radion potential
- `coupling_families.png`: continuous coupling counterexamples at fixed topology

**Not a proof or prediction of the physical fine-structure constant.** Experimental alpha is explicitly used only in the *conditional fit* subsection. Gauge field independent of the 6D metric; anomaly cancellation and UV completion have not been established.
