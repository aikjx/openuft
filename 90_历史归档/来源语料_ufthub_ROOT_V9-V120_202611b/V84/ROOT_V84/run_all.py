from __future__ import annotations
import json,subprocess,sys
from pathlib import Path
from src.simulate import generate_all

ROOT=Path(__file__).resolve().parent
print('ROOT V84 | ALL SYNTHETIC, no external hardware connection',flush=True)
r=generate_all(ROOT)
print('Scenario estimates:')
for name,p in r['scenarios'].items():
    fit=p['fit']['newton_yukawa_offset']
    print(f"{name:10s}: alpha={fit['alpha_yukawa']:+.5f} ± {fit['alpha_se']:.5f}; beta={fit['beta_G_ratio']:.5f}; chi2/dof={fit['chi_square']:.2f}/{fit['dof']}")
print('\nRunning unittest...')
t=subprocess.run([sys.executable,'-m','unittest','discover','-s',str(ROOT/'tests'),'-v'],cwd=ROOT)
if t.returncode:sys.exit(t.returncode)
print('ALL CHECKS COMPLETED; this is SOFTWARE and FORMULA verification, not discovery.')
