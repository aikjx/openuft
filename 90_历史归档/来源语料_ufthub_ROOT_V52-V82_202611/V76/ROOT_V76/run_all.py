from __future__ import annotations
import argparse, pathlib, subprocess, sys
P=pathlib.Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser(description='ROOT V76 scientific reproducibility')
    p.add_argument('--generate',action='store_true',help='regenerate data/figures using standard library/matplotlib')
    a=p.parse_args()
    print('ROOT V76 | scientific model verification, NOT physical experiment')
    subprocess.run([sys.executable,'-m','unittest','discover','-s',str(P/'tests'),'-p','test_*.py','-v'],cwd=P,check=True)
    if a.generate: subprocess.run([sys.executable,str(P/'tools'/'generate_results.py')],cwd=P,check=True)
    print('All requested checks succeeded. Check PROOF_STATUS.md for physics boundaries.')
if __name__=='__main__':main()
