"""One-command generation + test suite. No internet, no external experimental data."""
import subprocess,sys
from src.generate import generate
if __name__=='__main__':
    generate()
    code=subprocess.call([sys.executable,'-m','pytest','-q','tests'])
    if code:sys.exit(code)
    print('ROOT V108: tests passed; scientific OPEN issues remain OPEN.')
