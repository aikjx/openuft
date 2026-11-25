# ROOT V132 | Earth gravity numerical falsification package

**Scope:** Newton + J2 + rotating-frame effective acceleration; spherical five-layer Yukawa finite-size integral; numerical gradient cross-checks. **NOT** a proof of unified field theory and **NOT** an empirical validation of a fifth force.

## Run (Python 3.9+, standard library only)

```bash
python src/run.py
python -m unittest discover -s tests -v
```

Outputs: `results/altitudes.csv`, `results/locations.json`, `results/model_metadata.json`.

## Important distinctions

- The 5-layer density model is an illustrative numerical input, **not PREM**. The code normalizes the fifth-force ratio to its own layer mass. It does **not** claim to reproduce the earlier V118 0.5954% result.
- The alpha=1/3 and lambda=124.6 km values are hypotheses, not measured facts.
- A Yukawa force inferred by fitting an existing gravity model can be degenerate with the Earth's mass distribution and reference GM. A real test requires a joint refit and independent held-out data.
- Computational SI values for distance, acceleration and gravitational parameter are used to produce conventional outputs. In symbolic field theory, adopt c=1 only; do not set hbar=1 or G=1.
- J2 gravity vector is valid as a low-order exterior approximation. `effective` adds centrifugal acceleration only in the co-rotating Earth-fixed frame, not for inertial satellite dynamics.
- The potential convention is negative, with acceleration `-grad(Phi)`.

## Reproducibility

No third-party dependencies; tests cover numerical gradient, inverse square, rotation, symmetry, finite size, Yukawa long-range and decay limits.

## Official reference datasets not included

- ICGEM global gravity models and coefficients: https://icgem.gfz.de/tom_longtime
- NGA EGM2008 documentation and coefficients: https://earth-info.nga.mil/index.php?action=wgs84&dir=wgs84

Download, provenance, reference-frame, tide convention, epoch, uncertainty and independent holdout requirements must be specified before calling a comparison empirical verification.
