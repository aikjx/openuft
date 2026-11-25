"""Physical conversion only. The theory uses c=1; SI values require restoring c explicitly."""
import math
HBAR_SI = 1.054571817e-34  # joule second; CODATA rounded
C_SI = 299792458.0  # m/s exact
EV_J = 1.602176634e-19  # J/eV exact


def dirac_gap_gev(flux: int, radius_m: float, charge: int=1) -> float:
    if radius_m<=0:
        raise ValueError('radius must be positive')
    return HBAR_SI*C_SI*math.sqrt(1+abs(flux*charge))/radius_m/EV_J/1e9


def gap_mass_kg(flux: int, radius_m: float, charge: int=1) -> float:
    if radius_m<=0:
        raise ValueError('radius must be positive')
    return HBAR_SI*math.sqrt(1+abs(flux*charge))/(C_SI*radius_m)
