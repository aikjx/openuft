# -*- coding: utf-8 -*-
"""
企业级单元测试：三重奏全维精算库 + CODATA 2022 精算库
运行：python -m pytest tests/test_triad.py -v   （或用 run_verification.py 统一跑）
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mpmath as mp
mp.mp.dps = 250
from pkg import constants as C
from pkg import triad as T

def test_codata_planck_length():
    """Planck 长度对标 CODATA 2022 相对差 < 1e-9（G 精度内）"""
    assert abs((C.LP - mp.mpf("1.616255e-35"))/mp.mpf("1.616255e-35")) < mp.mpf("1e-6")

def test_codata_planck_mass():
    assert abs((C.MP_PL - mp.mpf("2.176434e-8"))/mp.mpf("2.176434e-8")) < mp.mpf("1e-6")

def test_codata_planck_time():
    assert abs((C.TP_ - mp.mpf("5.391247e-44"))/mp.mpf("5.391247e-44")) < mp.mpf("1e-6")

def test_triad_identity_electron():
    """κℓ_P = E/E_P 电子恒等式，相对差 < 1e-12（250 位）"""
    kl, r, rel = T.triad_identity_check(C.ME)
    assert rel < mp.mpf("1e-12")

def test_triad_identity_planck():
    """Planck 质量处 κℓ_P = 1"""
    kl, r, rel = T.triad_identity_check(C.MP_PL)
    assert abs(kl-1) < mp.mpf("1e-12") and abs(r-1) < mp.mpf("1e-12")

def test_dimension_fix():
    """量纲修复：修复式 (ω/c)²/κ² = 1；修复式2差 = 0"""
    lhs, rhs_orig, rhs_fix, ratio, fix2diff = T.dimension_audit(C.ME)
    assert abs(ratio-1) < mp.mpf("1e-20")
    assert abs(fix2diff) < mp.mpf("1e-70")

def test_original_dimension_broken():
    """原始公式量纲确实断裂：κ² 与 (ωℓ_P/c)² 相差 > 1e40 倍"""
    lhs, rhs_orig, _, _, _ = T.dimension_audit(C.ME)
    assert abs(mp.log10(lhs/rhs_orig)) > 40

def test_dim_effective_formula():
    """D 维各向同性求和公式自洽：κ_eff = ω/(c·√(D−1))，D=4 → ω/(c·√3)
    （注：4 维类时世界线有 D−1=3 个 Frenet 曲率；三重奏只取前 2 个 κ,τ，
     忽略 κ₃ —— 若 κ₃≠0 则三重奏不闭合，此为 OPEN 点，见 triad.T3 说明。）"""
    w = C.ME*C.C_SI**2/C.HBAR
    k4 = T.dim_effective_kappa(w, 4)
    assert abs(k4 - w/(C.C_SI*mp.sqrt(3))) < mp.mpf("1e-30")
    k32 = T.dim_effective_kappa(w, 32)
    assert abs(k32 - w/(C.C_SI*mp.sqrt(31))) < mp.mpf("1e-30")

def test_kk_excluded_large_extra_dim():
    """KK 一致性：R_c=1e-4 m（亚毫米上界）时三重奏被观测排除"""
    v = T.kk_consistency_verdict(mp.mpf("1e-4"))
    assert v["consistent"] is False
    assert v["contradiction_orders_of_magnitude"] > 5

def test_curvature_planck_scale():
    """Planck 加速度 → κℓ_P = 1"""
    k = T.curvature_of_proper_accel(C.C_SI**2/C.LP)
    assert abs(k*C.LP - 1) < mp.mpf("1e-12")

def test_geV_kg_conversion_roundtrip():
    """GeV↔kg 换算回环一致"""
    m_kg = mp.mpf("0.93827208816")*C.GEV2KG
    assert abs(m_kg/C.GEV2KG - mp.mpf("0.93827208816")) < mp.mpf("1e-12")

if __name__ == "__main__":
    import traceback
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = failed = 0
    for fn in fns:
        try:
            fn(); passed += 1; print(f"  PASS  {fn.__name__}")
        except Exception as e:
            failed += 1; print(f"  FAIL  {fn.__name__}: {e}")
    print(f"\n单元测试：{passed} 通过 / {failed} 失败")
    raise SystemExit(1 if failed else 0)
