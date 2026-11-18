"""Checks interpretation tags and numeric conclusions across book, code and results.
These are document consistency checks, not independent experiments.
"""
import json,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
book=(root/'book'/'ROOT_V70_星体_元素_空间运动_引力起源_联合研究总集.md').read_text(encoding='utf-8')
summary=json.loads((root/'results'/'numerical_summary.json').read_text(encoding='utf-8'))
checks={
  'book explicitly no unification proof':'不是' in book and '四力大统一' in book,
  'source charge disclosed artificial':'人为' in book and 'source_charge_toy' in (root/'rootv70'/'physics.py').read_text(encoding='utf-8'),
  'fixed rank one':summary['fixed_environment_identifiability']['rank']==1,
  'multi rank three':summary['cross_body_identifiability']['rank']==3,
  'planet count':summary['planet_count']==9,
  'scenario count':summary['physical_scenario_count']==54,
  'synthetic design count':summary['synthetic_feature_rows']==162,
  'no independent G predicted':'independent prediction of G' in summary['not_proven'],
  'gravity micro clock':1e-20<summary['earth_grav_redshift_1mm']<1e-18,
}
print(json.dumps(checks,ensure_ascii=False,indent=2))
sys.exit(0 if all(checks.values()) else 1)
