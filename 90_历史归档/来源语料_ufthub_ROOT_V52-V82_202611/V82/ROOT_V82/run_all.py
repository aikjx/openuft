"""Execute synthetic scenarios then tests. No hardware is controlled."""
import json, subprocess, sys
from pathlib import Path
from src.gravitylab import simulate, predict, export_csv, structural_degeneracy
root=Path(__file__).resolve().parent
(root/'results').mkdir(exist_ok=True)
report={'provenance':'100% SYNTHETIC, NEVER INSTRUMENT DATA','experiments':{}}
for f in sorted((root/'spec').glob('protocol_*.json')):
    p=json.loads(f.read_text(encoding='utf-8'))
    rows,stats=simulate(p)
    export_csv(root/'data'/f'{p["experiment"]}_synthetic.csv',rows)
    report['experiments'][p['experiment']]={'prediction':predict(p),'fit':stats}
report['unidentifiable_case']=structural_degeneracy()
(root/'results'/'synthetic_summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report['experiments'],indent=2))
res=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=root,check=False)
if res.returncode:sys.exit(res.returncode)
print('Synthetic data and unit tests generated successfully.')
