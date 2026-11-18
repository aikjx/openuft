"""Generates standalone web/index.html from shared physics model inputs."""
import json
from pathlib import Path
from rootv70.physics import BODIES,MATERIAL_TOY
here=Path(__file__).resolve().parent
text=(here/'web'/'template.html').read_text(encoding='utf-8')
data={b.name:{'name':b.name,'mu':b.mu,'r':b.radius,'spin':b.spin_hours,'j2':b.j2,'Q':b.source_charge_toy} for b in BODIES.values()}
text=text.replace('/*__BODY_JSON__*/',json.dumps(data,ensure_ascii=False))
text=text.replace('/*__MAT_JSON__*/',json.dumps(MATERIAL_TOY,ensure_ascii=False))
(here/'web'/'index.html').write_text(text,encoding='utf-8')
print('Generated web/index.html',len(text),'characters')
