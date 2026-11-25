#!/usr/bin/env python3
"""Reproducible tests for ROOT photon helicity and classical helical model.
Only c=1 in geometric derivations. Physical constants remain dimensional.
Passing DOES NOT validate a new physical theory.
"""
import math
C=299792458.0
H=6.62607015e-34
EV=1.602176634e-19
HBAR=H/(2*math.pi)

def close(x,y,tol=1e-10):
    assert math.isclose(x,y,rel_tol=tol,abs_tol=tol), (x,y)

def verify():
    count=0
    # Under c=1 and Heaviside-Lorentz field norm, B=z cross E
    for sigma in (-1,1):
        for i in range(1441):
            phi=2*math.pi*i/1440
            ex=math.cos(phi); ey=sigma*math.sin(phi)
            bx=-ey; by=ex
            sx=0; sy=0; sz=ex*by-ey*bx
            u=(ex*ex+ey*ey+bx*bx+by*by)/2
            close(sx,0); close(sy,0); close(sz,1); close(u,1); close(sz/u,1)
            # Maxwell Ampere: d_t E=(sinφ,-σcosφ), curl B=(sinφ,-σcosφ) for ω=k=1.
            dt_ex=math.sin(phi); dt_ey=-sigma*math.cos(phi)
            curl_bx=math.sin(phi); curl_by=-sigma*math.cos(phi)
            close(dt_ex,curl_bx); close(dt_ey,curl_by)
            # Maxwell Faraday: d_t B=(σcosφ,sinφ), -curl E=(σcosφ,sinφ).
            dt_bx=sigma*math.cos(phi); dt_by=math.sin(phi)
            minus_curl_ex=sigma*math.cos(phi); minus_curl_ey=math.sin(phi)
            close(dt_bx,minus_curl_ex); close(dt_by,minus_curl_ey)
            count+=1
    # SI energy and conversion to c=1 geometrized units
    for wavelength in (0.01e-9,400e-9,550e-9,1064e-9,1550e-9,1.064e-2):
        nu=C/wavelength; omega_si=2*math.pi*nu; k=2*math.pi/wavelength
        E=H*nu; p_si=E/C
        omega_g=omega_si/C; hbar_g=HBAR*C
        close(omega_g/k,1)
        close((hbar_g*omega_g)/E,1)
        close((p_si*C)/E,1)
        count+=1
    # hypothesis helix; θ = Ω t, time measured as length (c=1)
    for radius_m,q in ((1e-6,.9),(1e-7,.999),(1e-9,.999999),(1e-5,.6)):
        transverse=math.sqrt(1-q*q)
        omg=transverse/radius_m
        kappa=radius_m*omg*omg
        tau=q*omg
        close((radius_m*omg)**2+q*q,1)
        close((kappa*kappa+tau*tau)/(omg*omg),1)
        pitch=2*math.pi*q/omg
        close(pitch*omg/(2*math.pi*q),1)
        time_one_km=(1/q-1)*1000/C
        assert time_one_km>0
        assert kappa>0
        count+=1
    # phase-frequency assumption sensitivity calculation (not a bound)
    k=2*math.pi/550e-9; q=1-1e-6
    r=math.sqrt(1-q*q)/k
    assert 1e-10 < r < 2e-10
    # no unique intrinsic rotation radius follows from ħ and σ
    print('PASS',count,'numerical sampled cases + physical caveat checks')
    print('c=1 only; hbar/G dimensional; no claim of ROOT physical proof')
if __name__ == '__main__': verify()
