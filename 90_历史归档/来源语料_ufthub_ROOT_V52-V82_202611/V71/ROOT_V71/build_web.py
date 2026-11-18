"""Self-contained browser page; embeds catalogs to avoid local-file fetch restrictions."""
import csv,json
from pathlib import Path
P=Path(__file__).resolve().parent
with (P/'data'/'ROOT_V71_全部核心方程目录.csv').open(encoding='utf-8-sig') as f:eq=list(csv.DictReader(f))
with (P/'data'/'ROOT_V71_跨学科全部主要方法检验矩阵.csv').open(encoding='utf-8-sig') as f:methods=list(csv.DictReader(f))
injection='const EQUATIONS='+json.dumps(eq,ensure_ascii=False)+';\nconst METHODS='+json.dumps(methods,ensure_ascii=False)+';'
html=(P/'web'/'template.html').read_text(encoding='utf-8').replace('/*INLINE_DATA*/',injection)
(P/'web'/'index.html').write_text(html,encoding='utf-8')
print(f'Web self-contained: equations={len(eq)}, methods={len(methods)}, bytes={len(html.encode())}')
