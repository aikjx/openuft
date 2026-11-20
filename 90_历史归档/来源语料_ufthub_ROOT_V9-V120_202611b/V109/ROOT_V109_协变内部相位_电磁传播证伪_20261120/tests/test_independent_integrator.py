"""Independent real RK4 vs SciPy complex DOP853."""
import pytest
from src.axion_em import Profile,exact_rotation
from src.independent_rk4 import phase_axis

@pytest.mark.parametrize('k',[5,10,20,40,80])
def test_rk4_vs_complex_dop853(k):
    r=exact_rotation(k,.08,Profile(amplitude=.4,omega=.7),5)
    other=phase_axis(k,.08,.4,.7,5)
    assert other==pytest.approx(r['angle'],abs=2.e-7)

@pytest.mark.parametrize('k',[2,8,16])
def test_no_coupling_exact(k):
    assert phase_axis(k,0.,1.,1.,2.)==pytest.approx(0,abs=1.e-12)

@pytest.mark.parametrize('k',[2,10])
def test_reversing_coupling_reverses_phase(k):
    pos=phase_axis(k,.1,.3,.8,2.)
    neg=phase_axis(k,-.1,.3,.8,2.)
    assert pos==pytest.approx(-neg,abs=1.e-10)
