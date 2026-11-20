"""Portable ROOT V109 offline generation and verified testing."""
import pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parent
if __name__=='__main__':
    import os
    env=dict(os.environ)
    env['PYTHONPATH']=str(ROOT)
    for cmd in [[sys.executable,'-m','src.generate'],[sys.executable,'-m','pytest','-q','tests']]:
        print('$', ' '.join(cmd),flush=True)
        subprocess.run(cmd,cwd=ROOT,env=env,check=True)
    print('ROOT V109: model computations/tests PASS; unification remains OPEN',flush=True)
