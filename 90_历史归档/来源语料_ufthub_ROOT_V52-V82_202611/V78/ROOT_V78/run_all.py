"""One-command regeneration and verification."""
import subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parent
for cmd in ([sys.executable,'-m','unittest','discover','-s','tests','-v'],
            [sys.executable,'-m','scripts.generate_results'],
            [sys.executable,'-m','scripts.symbolic_checks']):
    print('RUN', ' '.join(cmd),flush=True)
    r=subprocess.run(cmd,cwd=root)
    if r.returncode: raise SystemExit(r.returncode)
print('ROOT V78 checks completed. No new experimental evidence is claimed.')
