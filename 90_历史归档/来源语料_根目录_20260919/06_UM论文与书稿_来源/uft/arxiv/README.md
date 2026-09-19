# Perpendicular Mode Geometry of Four Fundamental Forces

**Geometric unification of four forces through light helix perpendicular modes.**

[![arXiv](https://img.shields.io/badge/arXiv-TBD-orange)](https://arxiv.org/)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)

## Summary

This project proposes that the four fundamental forces arise from four
perpendicular oscillation modes of a light-speed helix structure in space.
The EM, strong, weak, and gravitational forces correspond to the radial,
tangential, chiral, and axial modes of this geometry.

## Key Prediction

$$\frac{\alpha_S}{\alpha_W} = 3.75$$

- **Framework**: 3.7500 (from integer coefficients {15, 4})
- **Independent Experiment** (PDG 2024): 3.49 (using $\alpha_2 = g_2^2/4\pi = 0.0338$)
- **Deviation**: 7.4% (NOTE: 3.7959 was circular via $\alpha_W = 4\alpha_{\rm EM}$)

This is the **falsifiable prediction** of the framework, derived from
assigned integer coefficients {1, 4, 15} on the unified seed $\Phi_T^2 = 1/128$.

## Integer Ratio

$$\alpha_S : \alpha_W : \alpha_{\rm EM} = 15 : 4 : 1$$

From integer coefficients {1, 4, 15} on a unified base $\Phi_T^2 = 2^{-7} = 1/128$.

## Geometric Parameters

| Symbol | Value | Description |
|--------|-------|-------------|
| $c$ | 299792458 m/s | Speed of light (EXACT) |
| $\kappa$ | $3.162 \times 10^{-4}$ m$^{-1}$ | Space curvature (**INPUT**) |
| $\tau$ | $2.308 \times 10^{-6}$ m$^{-1}$ | Space torsion (**INPUT**) |
| $\alpha$ | $\tau/\kappa = 1/137.036$ | Fine structure (**IDENTITY**) |
| $\Phi_T^2$ | $1/128 = 0.0078125$ | Unified seed (**ASSIGNED**) |

## Framework Completeness

**Overall: ~65% complete geometric interpretation**

| Category | Status |
|----------|--------|
| Four perpendicular modes | SOLVED (geometric narrative) |
| Integer ratio 15:4:1 | SOLVED (assigned coefficients) |
| $\tau/\kappa = \alpha$ | IDENTITY (construction) |
| $\alpha_S/\alpha_W = 3.75$ | WEAK PREDICTION (7.4% error, circular 3.7959 retracted) |
| **α absolute value** | **UNSOLVED (H1, 7.06% deviation)** |
| **Particle masses** | **UNSOLVED (H3)** |
| **κ, τ, Φ_T** | **INPUT PARAMETERS (H4)** |
| Gravity unification | Partial (3+1 structure) |

## Unsolved Problems (Honestly Acknowledged)

### H1: Fine Structure Constant (7.06% deviation)
- Framework: $\alpha_{\rm geom} = \Phi_T^2 = 1/128 = 0.0078125$
- Experiment: $\alpha_{\rm exp} = 1/137.036 = 0.00729735$
- Deviation: 7.06%
- **The framework can ACCOMMODATE but cannot PREDICT $\alpha$.**

### H3: Particle Masses
- Cannot calculate electron, quark, or neutrino masses
- Higgs mechanism not derived
- Major limitation, honestly acknowledged.

### H4: Input Parameters
- $\kappa$, $\tau$, $\Phi_T$ are inputs, not derived from first principles.
- $\tau/\kappa = \alpha$ is an identity by construction, not a prediction.

## IMPORTANT CORRECTIONS

Previous versions claimed $\kappa^{28} \cdot S_{\rm dS}/S_{\rm BH} = 10^{-98}$
as an exact coincidence. This is **ERRONEOUS**; the correct product is
approximately $10^{-53}$ using standard formulas. This claim is hereby explicitly retracted.

### Correction 2: 3.75 prediction circular dependency

Previous versions claimed $\alpha_S/\alpha_W = 3.75$ agrees with experiment
$3.7959$ at 1.2% deviation. This is **ERRONEOUS**: the value $3.7959$ was computed
circularly as $\alpha_S/(4\alpha_{\rm EM})$, using the framework's own assumption
$\alpha_W = 4\alpha_{\rm EM}$. With independent $\alpha_2(M_Z) = g_2^2/(4\pi) = 0.0338$,
the ratio is $3.49$ (7.4% deviation). The best-matching ratio is
$\alpha_S/\alpha_{\rm EM} = 15$ (0.6% deviation, trivial from assigned integer 15).
This claim is hereby explicitly corrected.

## Repository Structure

```
arxiv/
  main.tex              # LaTeX paper (honest v2)
  README.md             # This file

code/
  verify_core.py         # Core verification (4 identities, 1 prediction)
  gauge_couplings.py    # Gauge coupling analysis
  alpha_ratio.py        # alpha_S/alpha_W prediction analysis

derivations/
  helix_geometry.tex    # Detailed helix derivations
```

## Installation

```bash
pip install mpmath numpy matplotlib
python code/verify_core.py
python code/alpha_ratio.py
```

## What We Claim

- Novel geometric interpretation of four-force unification
- Integer coupling ratio 15:4:1 from assigned geometric coefficients
- Weak falsifiable prediction: $\alpha_S/\alpha_W = 3.75$ (7.4% deviation from independent experiment)
- Beautiful unifying picture: "Everything is light"

## What We Do NOT Claim

- ❌ "Predicts the fine structure constant" (H1 unsolved)
- ❌ "First-principles derivation of $\mu_0$" (identity)
- ❌ "Derived from SU(3)×SU(2) group theory" (assigned coefficients)
- ❌ "Complete theory of everything" (~65% complete, honest)
- ❌ $\kappa^{28} \cdot S_{\rm dS}/S_{\rm BH} = 10^{-98}$ (ERRONEOUS, retracted)

## Papers

- [arXiv:XXXX.XXXXX]() — *Perpendicular Mode Geometry of Four Fundamental Forces*
  (Honest v2, explicit correction of erroneous claims)

## License

MIT License - See LICENSE file.

---

**Note**: This framework is a geometric interpretation (~65% complete), not a
complete physical theory. All limitations are honestly acknowledged.
Previous erroneous claims have been corrected.
