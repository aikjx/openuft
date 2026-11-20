"""ROOT V93 complete repeatable audit; no claim of experimentally verified new physics."""
import sys,subprocess,json
from pathlib import Path
P=Path(__file__).resolve().parent

def run(cmd):
    print('\n>>>',' '.join(cmd),flush=True)
    subprocess.run(cmd,cwd=P,check=True)

if __name__=='__main__':
    run([sys.executable,'-m','unittest','discover','-s','tests','-v'])
    run([sys.executable,'-m','src.symbolic_audit'])
    run([sys.executable,'-m','src.build_ledger'])
    run([sys.executable,'-m','src.build_results'])
    # Browser check optional: do not silently label unexecuted smoke tests as passing
    try: import playwright
    except ImportError: print('Browser smoke: SKIPPED (install playwright and Chromium).')
    else:
        try: run([sys.executable,'web/browser_smoke.py'])
        except Exception as e: print('Browser smoke: FAILED or environment restricted:',e); raise
    print('\nROOT V93 mathematical/numerical reproducibility audit: COMPLETED')
    print('Scientific status: NO proof of a four-force unified field theory.')
