"""Reproducible V140 computations and tests. Python >=3.10; sympy required."""
from pathlib import Path
import csv, json, subprocess, sys
import sympy as sp
from src.composite import *
ROOT=Path(__file__).resolve().parent

def main():
    statuses={
        'nondegenerate_vacuum':simple_status(constant_rank4()),
        'nondegenerate_offshell':simple_status(rank4_offshell()),
        'degenerate_forcefree_counterexample':simple_status(forcefree_beltrami()),
        'degenerate_circular_wave':simple_status(circular_plane_wave()),
    }
    fp=ROOT/'results'/'symbolic_results.json'
    fp.write_text(json.dumps({'model':'ROOT_V140', 'c':1, 'hbar':'independent', 'G':'independent', 'status':statuses},indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    with (ROOT/'results'/'wave_sample.csv').open('w',newline='',encoding='utf8') as handle:
        w=csv.writer(handle);w.writerow(['phase','E_x','E_y','B_x','B_y','energy_density_in_hbar_over_g2'])
        for index in range(101):
            phase=2*sp.pi*index/100
            w.writerow([f'{float(phase):.12f}',f'{float(sp.cos(phase)):.12f}',f'{float(sp.sin(phase)):.12f}',f'{float(sp.sin(phase)):.12f}',f'{float(-sp.cos(phase)):.12f}','1'])
    print('Key symbolic outputs:')
    for label,d in statuses.items():print(' ',label,'Pf=',d['pfaffian'],'J=',d['J'],'projected=',d['projected_EOM'])
    p=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=ROOT,text=True,capture_output=True)
    (ROOT/'results'/'test_run.log').write_text(p.stdout+p.stderr,encoding='utf8')
    print(p.stderr[-1600:])
    return p.returncode
if __name__=='__main__':sys.exit(main())
