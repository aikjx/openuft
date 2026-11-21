"""Symbolic consistency tests; no claim of new physical law."""
import sympy as sp
import pytest
from field_theory_v123 import (quadratic_fR_trace_equation,
    classical_maxwell_trace,five_dimensional_null_dispersion,circle_kk_mass_scale)


def test_quadratic_fR_trace_identity():
    obj=quadratic_fR_trace_equation()
    assert obj['remainder']==0


def test_maxwell_traceless_4D_classical():
    obj=classical_maxwell_trace()
    assert obj['trace']==0


def test_5D_null_to_4D_mass_shell_kinematics_only():
    obj=five_dimensional_null_dispersion()
    assert obj['difference_after_p5_equals_mc']==0

@pytest.mark.parametrize('n',[0,1,2,5,11])
def test_kk_circle_tower_n(n):
    r=3.8615926796e-13
    m=circle_kk_mass_scale(r,n)
    m1=circle_kk_mass_scale(r,1)
    assert m==pytest.approx(n*m1,rel=1e-14)


def test_kk_needs_independent_length_scale():
    assert circle_kk_mass_scale(1e-13,1)>circle_kk_mass_scale(1e-12,1)


def test_simple_3d_helix_with_axial_velocity_is_superluminal_if_transverse_c():
    c=299792458.
    vtheta=c; vz=.2*c
    assert (vtheta**2+vz**2)**.5 >c


def test_real_3d_null_speed_requires_transverse_suppression():
    c=299792458.;vz=.4*c
    vtheta=(c*c-vz*vz)**.5
    assert vtheta<c
    assert abs(vtheta**2+vz**2-c*c)/c**2<2e-16
