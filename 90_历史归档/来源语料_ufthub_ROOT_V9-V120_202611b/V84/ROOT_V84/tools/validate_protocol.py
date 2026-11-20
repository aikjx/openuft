from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
p=json.loads((root/'spec'/'protocol_v84.json').read_text(encoding='utf8'))
a=json.loads((root/'spec'/'analysis_plan.json').read_text(encoding='utf8'))
required=['schema_version','simulation_only','source','sensors','distance_grid_m','switch_schedule','arms','preregistered_model','required_provenance','forbidden_claims']
for k in required:assert k in p,k
assert p['schema_version']=='ROOT-GCL/1.2'
assert p['simulation_only'] and not p['real_hardware_connected'] and p['no_instrument_control_commands']
assert p['required_provenance']=='SYNTHETIC_NOT_REAL_DATA'
assert p['sensors']['sensor_baseline_m']==p['sensors']['positions_m'][1]-p['sensors']['positions_m'][0]
assert min(p['distance_grid_m'])>p['sensors']['sensor_baseline_m']/2+p['source']['uniform_sphere_radius_m']
assert all(len(seq)==4 and sum(seq)==0 for seq in p['switch_schedule']['accepted_patterns'])
assert a['data_type']==p['required_provenance']
print('PROTOCOL VERIFIED: ROOT-GCL/1.2, safe synthetic no hardware mode')
