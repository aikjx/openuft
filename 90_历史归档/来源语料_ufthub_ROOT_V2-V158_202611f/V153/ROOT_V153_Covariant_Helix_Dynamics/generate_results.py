"""Generate transparent, normalized demonstration CSV and one diagram."""
from pathlib import Path
import csv
import numpy as np
root=Path(__file__).resolve().parent
xs=np.linspace(0,4*np.pi,401)
p=root/'results'/'wave_comparison.csv'
with p.open('w',newline='',encoding='utf-8') as out:
    wr=csv.writer(out)
    wr.writerow(['phase_t_minus_z','scalar_A_dtheta_F01','transverse_vector_F01','scalar_h_hessian_R0101','TT_tensor_R0101'])
    for s in xs:
        wr.writerow([f'{s:.16g}','0',f'{-np.sin(s):.16g}','0',f'{.5*np.cos(s):.16g}'])
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(9,4.3))
    ax.plot(xs,-np.sin(xs),label='transverse vector: F_01 (normalized)')
    ax.plot(xs,.5*np.cos(xs),label='TT tensor: R_0101 (normalized)')
    ax.plot(xs,np.zeros_like(xs),'--',label='single scalar derivative: both zero')
    ax.set_xlabel('phase t-z (dimensionless example)')
    ax.set_ylabel('amplitude (distinct operators / normalized)')
    ax.set_title('Same wave phase, different field representations')
    ax.grid(alpha=.2)
    ax.legend(loc='upper right')
    fig.tight_layout()
    fig.savefig(root/'figures'/'phase_vs_fieldstrength.png',dpi=170)
    fig.savefig(root/'figures'/'phase_vs_fieldstrength.svg')
    plt.close(fig)
except ImportError:
    print('matplotlib unavailable, CSV remains available')
print('RESULTS generated',p)
