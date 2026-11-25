from pathlib import Path
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parents[1]
with (root/'results'/'wave_sample.csv').open(encoding='utf8') as f:
 data=list(csv.DictReader(f))
p=[float(row['phase']) for row in data]
fig,ax=plt.subplots(figsize=(8.0,4.6))
ax.plot(p,[float(row['E_x']) for row in data],label='E_x')
ax.plot(p,[float(row['E_y']) for row in data],label='E_y')
ax.plot(p,[float(row['B_x']) for row in data],label='B_x',ls='--')
ax.plot(p,[float(row['B_y']) for row in data],label='B_y',ls=':')
ax.set_xlabel('Phase k(t-z) (radians)')
ax.set_ylabel('Normalized field amplitude')
ax.set_title('V140: rotating polarization, straight wave propagation')
ax.grid(alpha=.2)
ax.legend(ncol=4)
fig.tight_layout()
fig.savefig(root/'figures'/'rotating_fields.png',dpi=165)
plt.close(fig)
