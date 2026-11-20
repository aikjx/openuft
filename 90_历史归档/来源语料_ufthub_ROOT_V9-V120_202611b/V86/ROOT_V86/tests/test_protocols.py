import json
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
EXPECTED=['01_multidistance_mass','02_composition_factorization','03_angular_j2_control','04_electromagnetic_null']
@pytest.mark.parametrize('name',EXPECTED)
def test_protocol_structure(name):
    d=json.loads((ROOT/'spec'/f'{name}.json').read_text(encoding='utf8'))
    assert d['schema']=='ROOT-GCL/2.0'
    assert d['units']=='SI'
    assert d['data_label'].startswith('SYNTHETIC')
    assert d['stages'][0]=='DEFINE' and d['stages'][-1]=='RELEASE'
    assert 'human_review' in d['safety']
    assert 'RANDOMIZE' in d['stages']
    assert len(d['required_raw_columns'])>=5
