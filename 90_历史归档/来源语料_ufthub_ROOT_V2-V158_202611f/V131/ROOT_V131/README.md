# ROOT V131 — Earth verification baseline (reproducible)

Run `python verify.py` (Python 3.9+, standard library only). Produces `altitude.csv`, `locations.json` and seven deterministic assertions. No network access required.

## Scope and honesty

**Completed:** point-mass inverse-square acceleration at seven heights, J2 Cartesian gravity at three locations, rotating-frame effective acceleration, finite-difference potential-gradient cross-check, and an illustrative exponential residual curve. These are calculations, **not** independent experimental validation of ROOT.

**Not completed:** real EGM2008/GOCE/GRACE-FO coefficient ingestion, PREM radial density integration, tides, clock frequency shifts, orbit fitting, covariance/noise propagation, GR 1PN corrections, Maxwell field coupling, particle spectra, four-force unification. None of these is asserted to pass.

## Baseline physics

Point mass: `g=GM/r²`. In Earth-centered Cartesian coordinates, with `r²=x²+y²+z²`, `q=5z²/r²`, `t=(3/2)J2(Re/r)²`,

`ax=-GM*x/r³ * (1-t*(q-1))`
`ay=-GM*y/r³ * (1-t*(q-1))`
`az=-GM*z/r³ * (1-t*(q-3))`.

Potential `Phi=-GM/r * [1-J2*(Re/r)²*P2(z/r)]` with `P2(u)=(3u²-1)/2`. The acceleration is `-grad Phi`.

For Earth-fixed effective gravity only, add centrifugal `(+omega²*x,+omega²*y,0)`. This is not an extra gravitational force in an inertial frame.

## Candidate residual warning

`root_local_residual = epsilon0 * GM/Rmean² * exp(-h/lambda)` is a **phenomenological local exponential toy model** with `epsilon0=0.005954` and `lambda=124600 m`. It is not a derived Yukawa field for an extended layered Earth, nor an accepted observed anomaly. It must not be added to gravity as a verified correction. The historical ROOT V119 estimate for 400 km used a different density-convolved model and is not reproduced by this toy model.

## Units

Reported accelerations in SI m/s². For c=1, time may be measured as length via `t_length=c_SI*t_SI`, and acceleration has dimension inverse length. Neither hbar nor G is set to 1; this software uses the measured Earth `GM` for benchmarking, so it **cannot** derive G independently.

## Sources

- NASA Earth Fact Sheet: https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html
- IERS Conventions: https://iers-conventions.obspm.fr/content/tn36.pdf
- ICGEM model catalogue: https://icgem.gfz.de/faq
- NGA EGM2008 resources: https://earth-info.nga.mil/index.php?action=wgs84&dir=wgs84

## Future verification acceptance gates

1. Lock coordinate frame, tidal system, epoch and reference constants.
2. Ingest gravity coefficients and document normalization and degree/order.
3. Reproduce baseline field and gradients against an independent implementation.
4. Compute layered-Earth Yukawa convolution, rather than an exponential altitude toy curve.
5. Jointly fit GM, J2, tides, drag, instrument biases and candidate ROOT parameters; hold out satellite arcs.
6. Compare residuals using full covariance and publish confidence intervals; a fit alone is not discovery.
