"""Offline reproduction of V104 physics audit, then pytest and SymPy checks."""
from src.generate import run
import subprocess,sys
if __name__=='__main__':
    run()
    subprocess.run([sys.executable,'-m','pytest','-q','tests'],check=True)
    subprocess.run([sys.executable,'-m','src.symbolic'],check=True)
