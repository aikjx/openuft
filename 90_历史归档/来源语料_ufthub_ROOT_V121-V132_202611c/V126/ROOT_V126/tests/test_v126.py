"""Independent mathematical regression tests; SYNTHETIC only."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import numpy as np
import pytest
from v126_core import *

S,W,C=sim_multi_center_geometry()
TRACE=lambda pts:point_trace(pts,S,W)

@pytest.mark.parametrize('x',[0.0,1e-9,1e-4,1e-3,0.1,0.3,1,2,3,5])
def test_sinhc_matches_high_accuracy(x):
    expected=1 if x==0 else np.sinh(x)/x
    assert sinhc(x)==pytest.approx(expected,rel=1e-12)

@pytest.mark.parametrize('resolution',[(12,24),(18,36),(24,48),(32,64)])
@pytest.mark.parametrize('radius',[0,25e3,50e3,100e3,150e3,250e3])
def test_non_spherical_mean_value(radius,resolution):
    directions,wt=sphere_quadrature(*resolution)
    result=shell_average(TRACE,C,radius,directions,wt)
    target=float(TRACE(C)*sinhc(radius/ELL))
    assert result==pytest.approx(target,rel=2e-7)

@pytest.mark.parametrize('radius',[0,50e3,100e3,150e3,250e3])
def test_discrete_weights_normalized(radius):
    directions,wt=sphere_quadrature()
    assert np.sum(wt)==pytest.approx(1,abs=5e-15)
    assert np.linalg.norm(directions,axis=1)==pytest.approx(np.ones(len(wt)),abs=1e-14)
    assert shell_average(lambda p:np.ones(len(p))*8.21,C,radius,directions,wt)==pytest.approx(8.21)

@pytest.mark.parametrize('ell',[35e3,60e3,124600,200e3,300e3,600e3])
def test_inverse_two_shells(ell):
    aa,bb=50e3,150e3
    m1=sinhc(aa/ell)*5
    m2=sinhc(bb/ell)*5
    assert inverse_two_shells(aa,bb,m1,m2)==pytest.approx(ell,rel=1e-9)

@pytest.mark.parametrize('ell',[40e3,60e3,124600,250e3,500e3])
def test_inverse_three_shells_with_common_offset(ell):
    aa,bb,cc=50e3,150e3,300e3
    m1,m2,m3= [4.7*sinhc(r/ell)+123.5 for r in (aa,bb,cc)]
    assert inverse_three_shells(aa,bb,cc,m1,m2,m3)==pytest.approx(ell,rel=1e-7)

@pytest.mark.parametrize('offset',[-1000,-100,-1,0,1,500,1000])
def test_common_offset_cancels(offset):
    aa,bb,cc=50e3,150e3,300e3
    m=[float(TRACE(C)*sinhc(r/ELL)+offset*1e-9) for r in (aa,bb,cc)]
    assert inverse_three_shells(aa,bb,cc,*m)==pytest.approx(ELL,rel=1e-8)

@pytest.mark.parametrize('scale',[0.001,0.2,1.0,9.5,100])
def test_scaling_source_amplitude_cancels(scale):
    aa,bb,cc=50e3,150e3,300e3
    fn=lambda p:point_trace(p,S,W*scale)
    mean=[shell_average(fn,C,r) for r in (aa,bb,cc)]
    assert inverse_two_shells(aa,bb,mean[0],mean[1])==pytest.approx(ELL,rel=1e-8)
    assert inverse_three_shells(aa,bb,cc,*mean)==pytest.approx(ELL,rel=1e-8)

@pytest.mark.parametrize('point',[[EARTH_R+400e3,0,0],[EARTH_R+520e3,300e3,40e3],[EARTH_R+270e3,-45e3,0]])
def test_any_centre_source_geometry(point):
    centre=np.array(point)
    f=lambda x:point_trace(x,S,W)
    m=shell_average(f,centre,75e3)
    assert m==pytest.approx(point_trace(centre,S,W)*sinhc(75e3/ELL),rel=3e-7)

@pytest.mark.parametrize('alpha',[-2.0,-0.01,0.01,0.7,5])
def test_negative_positive_coupling(alpha):
    f=lambda x:point_trace(x,S,W*alpha)
    m1=shell_average(f,C,50e3)
    m2=shell_average(f,C,150e3)
    assert inverse_two_shells(50e3,150e3,m1,m2)==pytest.approx(ELL,rel=1e-8)

@pytest.mark.parametrize('ell',[60e3,124600,220e3,400e3])
def test_weak_form_non_spherical(ell):
    f=lambda x:point_trace(x,S,W,ell)
    ksq=weak_k_squared(f,C,150e3,radial_count=26,theta=12,phi=24)
    assert ksq==pytest.approx(1/ell**2,rel=2e-6)

@pytest.mark.parametrize('ell',[50e3,124600,250e3])
def test_multipole_invariance_of_normalized_mean(ell):
    # Completely arbitrary Newton multipole can be superposed; the trace is harmonic zero.
    f=lambda x:point_trace(x,S,W,ell)
    for R in (40e3,120e3):
        assert shell_average(f,C,R)/point_trace(C,S,W,ell)==pytest.approx(sinhc(R/ell),rel=1e-7)

@pytest.mark.parametrize('ell',[30e3,60e3,124600,300e3,900e3])
def test_two_shell_ratio_strict_decrease_in_ell(ell):
    assert shell_ratio_from_length(50e3,150e3,ell)>1
    assert shell_ratio_from_length(50e3,150e3,ell*.9)>shell_ratio_from_length(50e3,150e3,ell)

@pytest.mark.parametrize('a,b',[(0,1),(50e3,150e3),(80e3,120e3)])
def test_invalid_shell_inversion(a,b):
    with pytest.raises(ValueError): inverse_two_shells(a,b,10,9)
    with pytest.raises(ValueError): inverse_two_shells(a,b,10,-10)

@pytest.mark.parametrize('vals',[(0,0,1),(-1,3,1),(10,5,2)])
def test_bad_three_shell_geom(vals):
    with pytest.raises(ValueError):shell_contrast(*vals,2,3,4)

def test_non_spherical_matter_is_visible_at_same_shell():
    r=150e3
    a=float(TRACE(C+[r,0,0]))
    b=float(TRACE(C-[r,0,0]))
    assert abs(a-b)/abs(a)>0.1

def test_two_scales_falsify_single_scale_with_many_radii():
    # Synthetic different-k sources with independent spatial patterns.
    f=lambda x:mixed_point_trace(x,S[:3],W[:3],np.array([124600,300000,124600]))
    radii=[25e3,75e3,150e3,270e3]
    means=[shell_average(f,C,r) for r in radii]
    k1=inverse_two_shells(radii[0],radii[1],means[0],means[1])
    k2=inverse_two_shells(radii[2],radii[3],means[2],means[3])
    assert abs(k1-k2)>100

def test_source_point_singularity_fails():
    with pytest.raises(ValueError):point_trace(S[1],S,W)

def test_weak_compact_boundary_conditions():
    a=150e3
    assert weak_bump(a,a)==pytest.approx(0)
    assert weak_laplacian_bump(a,a)==pytest.approx(0)
    assert weak_bump(1.1*a,a)==0

def test_spherical_geometry_safe_vacuum():
    _,_,center=sim_multi_center_geometry()
    assert np.linalg.norm(center)-300e3>EARTH_R

def test_common_offset_biases_two_shell():
    r1,r2=50e3,150e3
    means=[shell_average(TRACE,C,r) for r in [r1,r2]]
    biased=inverse_two_shells(r1,r2,means[0]+5e-9,means[1]+5e-9)
    assert abs(biased-ELL)>10000

def test_different_offsets_defeat_three_shell():
    rs=[50e3,150e3,300e3]
    means=[shell_average(TRACE,C,r) for r in rs]
    bias=np.array([0,3,6])*1e-9
    try:
        estimated=inverse_three_shells(*rs,*(np.array(means)+bias))
    except ValueError:
        # A varying bias can even make the positive-k model impossible.
        return
    assert abs(estimated-ELL)>1000

@pytest.mark.parametrize('radius',[50e3,100e3,200e3,300e3])
def test_synthetic_earth_trace_formula_matches_v125(radius):
    t=candidate_earth_trace_at_altitude(400e3+radius)
    ref=17.473593e-9*(EARTH_R+400e3)/(EARTH_R+400e3+radius)*np.exp(-radius/ELL)
    assert t==pytest.approx(ref,rel=1e-14)

@pytest.mark.parametrize('radii',[[50e3,100e3,200e3,300e3],[30e3,130e3,230e3,350e3]])
def test_four_shell_single_spectrum_cross_validation(radii):
    mean=[shell_average(TRACE,C,r) for r in radii]
    l1=inverse_three_shells(*radii[:3],*mean[:3])
    l2=inverse_three_shells(*radii[1:],*mean[1:])
    assert l1==pytest.approx(ELL,rel=1e-8)
    assert l2==pytest.approx(ELL,rel=1e-8)

@pytest.mark.parametrize('ell2',[180e3,250e3,300e3,500e3])
def test_four_shell_detects_mixed_positive_spectrum(ell2):
    f1=lambda p:point_trace(p,S,W,ELL)
    f2=lambda p:point_trace(p,S,W,ell2)
    multiplier=float(f1(C)/f2(C))
    f=lambda p:f1(p)+multiplier*f2(p)
    radii=[50e3,150e3,250e3,350e3]
    means=[shell_average(f,C,r) for r in radii]
    l1=inverse_three_shells(*radii[:3],*means[:3])
    l2=inverse_three_shells(*radii[1:],*means[1:])
    assert abs(l1-l2)>10

@pytest.mark.parametrize('strength',[1e7,1e8,1e9])
def test_source_inside_sample_ball_invalidates_vacuum_mean(strength):
    # The source is 60km from the centre and lies inside the 150km sphere.
    inside=np.asarray(C)+[60e3,0,0]
    f=lambda p:TRACE(p)+point_trace(p,np.array([inside]),np.array([strength]),ELL)
    actual=shell_average(f,C,150e3)
    projected=float(f(C)*sinhc(150e3/ELL))
    assert abs(actual-projected)>abs(projected)*0.0001

@pytest.mark.parametrize('radius',[25e3,75e3,150e3])
def test_rotation_invariance_of_mean(radius):
    angle=.71
    rot=np.array([[np.cos(angle),-np.sin(angle),0],[np.sin(angle),np.cos(angle),0],[0,0,1]])
    fn=lambda x:point_trace(x,S@rot.T,W,ELL)
    actual=shell_average(fn,C@rot.T,radius)
    original=shell_average(TRACE,C,radius)
    assert actual==pytest.approx(original,rel=1e-10)
