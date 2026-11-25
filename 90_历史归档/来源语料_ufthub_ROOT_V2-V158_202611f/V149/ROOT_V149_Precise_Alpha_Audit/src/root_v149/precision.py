"""50-digit Decimal audit; extra digits do NOT represent physical precision.
Physics uncertainty remains dominated by input CODATA data, especially G.
"""
from decimal import Decimal, localcontext

PI_STR='3.1415926535897932384626433832795028841971693993751058209749445923'

def audit_decimal(places=55):
    if places < 20: raise ValueError('minimum decimal precision 20')
    with localcontext() as ctx:
        ctx.prec=places
        alpha=Decimal('0.0072973525643')
        alpha_unc=Decimal('0.0000000000011')
        g=Decimal('6.67430e-11')
        g_unc=Decimal('0.00015e-11')
        me=Decimal('9.1093837139e-31')
        h=Decimal('6.62607015e-34')
        c=Decimal('299792458')
        pi=Decimal(PI_STR)
        hbar=h/(2*pi)
        ag=g*me*me/(hbar*c)
        out={
            'NIST_alpha_input':str(alpha),
            'alpha_std_uncertainty':str(alpha_unc),
            'alpha_inverse_calculated':str(1/alpha),
            'fit_sqrt_alpha':str(alpha.sqrt()),
            'fit_u_sqrt_1_minus_alpha':str((1-alpha).sqrt()),
            'fitted_a_uncertainty_linearized':str(alpha_unc/(2*alpha.sqrt())),
            'fitted_u_uncertainty_linearized':str(alpha_unc/(2*(1-alpha).sqrt())),
            'electron_alpha_gravity':str(ag),
            'electron_alpha_gravity_relative_std_from_G_only':str(g_unc/g),
            'alpha_to_electron_alpha_gravity_ratio':str(alpha/ag),
            'precision_note':'Extra decimal digits are computational; uncertainty in input CODATA constants limits physical significance.'
        }
        return out
