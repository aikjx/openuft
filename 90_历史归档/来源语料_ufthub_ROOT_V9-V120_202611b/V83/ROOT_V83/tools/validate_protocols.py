"""Stdlib validation subset. JSON Schema file included for full validators."""
import json
from pathlib import Path
from src.gravitylab import Rig

def check(protocol):
    required={'version','id','provenance','physics_model','geometry','switching','measurement','controls','safety','acceptance'}
    if set(protocol)!=required: raise ValueError('missing or extra top-level fields')
    if protocol['version']!='ROOT-GCL/1.1': raise ValueError('unsupported protocol version')
    if protocol['provenance']!='SYNTHETIC_NOT_OBSERVED': raise ValueError('invalid provenance')
    if protocol['safety'].get('hardware_authorized') is not False or protocol['safety'].get('simulation_only') is not True:
        raise ValueError('This application cannot authorize hardware control')
    if len(protocol['controls'])<4: raise ValueError('insufficient controls')
    if protocol['id'].startswith('MASS-'):
        g=protocol['geometry']
        Rig(g['source_mass_kg'],abs(g['source_center_switch_m'][1]),
            g['sensor_x_m'][1]-g['sensor_x_m'][0],g['source_radius_m']).validate()
    return True

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    for p in sorted((root/'spec').glob('protocol_*.json')):
        check(json.loads(p.read_text()))
        print('PASS',p.name)
