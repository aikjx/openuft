"""ROOT V107 reproducibility entrypoint. Does not assert new experimental findings."""
from pathlib import Path
import subprocess,sys,json
from src.symbolic_audit import run as check_sym
from src.theory import summary
from src.generate import run as generate
from src.ledger import generate as generate_ledger
ROOT=Path(__file__).resolve().parent

def main():
    checks=check_sym()
    print('ROOT V107 symbolic checks passed:',len(checks))
    out=subprocess.run([sys.executable,'-m','pytest','-q','tests'],cwd=ROOT,check=False)
    if out.returncode: raise SystemExit(out.returncode)
    result=generate()
    ledger=generate_ledger()
    print('ROOT V107 numerical study (toy only) at GeV scale:')
    print('  I0 =',result['one_loop_invariant'])
    print('  required one-pair splitting MT/MD =',result['one_pair_mass_ratio_required'])
    print('  constructed two-pair matching =',result['two_pairs_toy']['mu_unify_GeV'])
    print('  tracker unique IDs =',ledger['total_unique_canonical_ids'])
    print('  Scientific status: FULL FOUR-FORCE UNIFICATION NOT SOLVED.')

if __name__=='__main__': main()
