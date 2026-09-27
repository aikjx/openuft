# -*- coding: utf-8 -*-
# 第89章 额外维出路终审（纯标准库）
#  (1) S05 普朗克尺度螺旋嵌入：KK 模质量 vs GUT 标度 -> 是否降低统一点
#  (2) ADD 大额外维：Gauss 律 R(n;M_D)，与短程引力/LHC 约束；SM 在膜 => 不统一规范力
#  (3) TeV 幂律跑动统一：dim-6 质子寿命随 M_X=M_Q 的崩塌 + 所需 split-fermion 波函数压制
import math
HBARC=1.973269804e-16   # GeV^-1 -> m
LP=1.616255e-35         # m (CODATA)
MP=1.2210e19            # GeV (non-reduced, G=1/Mp^2)

print("="*80)
print("[1] S05 HDU (11D spiral embed): R11 = Lp after repair -> KK tower scale")
mKK=HBARC/LP
print("  m_KK(1/R11) = hbar*c/Lp = %.3e GeV ; m_Pl=%.3e GeV ; GUT=1e16 GeV"%(mKK,MP))
print("  m_KK/GUT = %.1f  (KK modes sit %d orders ABOVE GUT)"%(mKK/1e16, round(math.log10(mKK/1e16))))
print("  => Planck-radius compactification CANNOT lower the gauge unification point.")
print("     repaired=dimensional/self-consistent only, NOT physical evidence (S05 postulate sec4).")

print("="*80)
print("[2] ADD large extra dimensions:  Mp^2 = M_D^(n+2) R^n  =>  R=(Mp/M_D)^(2/n)/M_D")
def R_m(n, MD_GeV):
    Rg=(MP/MD_GeV)**(2.0/n)/MD_GeV      # GeV^-1
    return Rg*HBARC
lhc={2:6.0,3:4.4,4:3.9,5:3.6,6:3.3}    # TeV, conservative monojet/dilepton (n=2 strongest)
print("  n   R@M_D=1TeV        R@LHC lower-limit M_D   empirical bound")
for n in range(1,7):
    R1=R_m(n,1e3)
    Rl=R_m(n,lhc[n]*1e3) if n in lhc else float('nan')
    note=""
    if n==1: note="~100s AU -> solar-system gravity EXCLUDES"
    elif n==2: note="sub-mm: torsion balance no deviation ~55 um"
    else: note="LHC monojet/dilepton M_D bound"
    print("  %d   %10.3e m     %10.3e m            %s"%(n,R1,Rl,note))
print("  STRUCTURE: SM gauge fields + fermions confined to 3-brane (else precision tests fail);")
print("  only gravity probes bulk => ADD solves hierarchy, does NOT run/unify the 3 gauge couplings.")

print("="*80)
print("[3] TeV-scale power-law unification (KK tower beyond 1/R): naive dim-6 proton lifetime")
C6=1e36; REF=1e16
def tau_naive(MX): return C6*(MX/REF)**4          # alpha factor ~1 at unification
HK=1e35
print("  Q*=M_X      tau_naive(yr)   suppression S=ln(tau_HK/tau_naive) needed   d/sigma (single pair ~2sqrtS)")
for Q,name in [(1e4,"10 TeV"),(1e5,"100 TeV"),(1e6,"1 PeV"),(1e7,"10 PeV"),(1e8,"100 PeV (=1e5 TeV)")]:
    t=tau_naive(Q); S=math.log(HK/t); dovers=2*math.sqrt(S)
    print("  %-22s %10.2e      S=%6.1f  (e^-S)            ~%.0f localization widths"%(name,t,S,dovers))
print("  independent cross-check hep-ph/0502102: braneworld proton decay pushes string scale")
print("  lower bound to ~1e5 TeV (=1e8 GeV); there tau_naive=%.0e yr, still needs S~%.0f."
      %(tau_naive(1e8), math.log(HK/tau_naive(1e8))))
print("  same bulk wave-function overlap that sets gauge couplings also carries dim-6 B-violation;")
print("  enforcing unification + Yukawa hierarchy AND exp(-90) proton suppression = fine-tune,")
print("  with FCNC (K0 mixing) requiring 1/R >~ 30-100 TeV. This is the ch85 tension in higher-D form.")
print("="*80)
print("VERDICT: S05 Planck-scale (no lowering); ADD on-brane (no gauge unification);")
print("RS/TeV power-law lower the point but require split-fermion e^-90 suppression & collider-pushed KK.")
print("No free extra-dimensional escape; geometry/spiral input to verified physics = 0/5; UFT stays 2/6.")
