"""Hypercharge anomaly consistency using exact fractions and left-handed fields only."""
from fractions import Fraction as F

# field -> (color multiplicity, weak multiplicity, left-handed hypercharge)
# u^c, d^c, e^c are LH conjugates of RH fermions.
SM_GEN = {
    'Q_L': (3, 2, F(1,6)),
    'u_L_conj': (3, 1, F(-2,3)),
    'd_L_conj': (3, 1, F(1,3)),
    'L_L': (1, 2, F(-1,2)),
    'e_L_conj': (1, 1, F(1,1)),
}


def cubic_u1_anomaly(field_content=SM_GEN) -> F:
    return sum((c*w*y**3 for c,w,y in field_content.values()),F(0))


def grav_u1_anomaly(field_content=SM_GEN) -> F:
    return sum((c*w*y for c,w,y in field_content.values()),F(0))


def su2_squared_u1_anomaly() -> F:
    # omit common Dynkin index 1/2
    return 3*F(1,6)+F(-1,2)


def su3_squared_u1_anomaly() -> F:
    # omit common Dynkin index 1/2
    return 2*F(1,6)+F(-2,3)+F(1,3)


def su2_global_doublet_count() -> int:
    return 3+1


def single_chiral_u1_anomalies(flux: int, charge: int=1) -> dict[str,int]:
    """Index-weighted (LH-RH) U1 anomalies; assumes relevant 4D gauge charge=charge."""
    idx=flux*charge
    return {'cubic':idx*charge**3, 'mixed_gravity':idx*charge}


def hypercharge_flux_index(flux: int) -> dict[str,int]:
    """Same monopole U1 also identified with Y_tilde=6Y, integer-normalized."""
    return {name:flux*int(6*y) for name,(_,_,y) in SM_GEN.items()}


def family_flux_index(flux: int) -> dict[str,int]:
    """Separate hypothetical U(1)_family with unit charges for ALL five species."""
    return {name:flux for name in SM_GEN}
