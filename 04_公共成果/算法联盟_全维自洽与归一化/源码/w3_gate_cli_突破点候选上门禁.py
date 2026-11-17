# -*- coding: utf-8 -*-
# W3 breakthrough gate CLI -- companion tool to r421 (no new r number; tool, not a verdict volume)
# Usage:
#   python w3_gate_cli_突破点候选上门禁.py --value 0.0072973525693 --name "alpha from theory X" \
#       --independent yes --blind-path yes --two-anchors yes
# Four gates (method_F criterion 5 + criterion 3), ALL required:
#   C1 quantitative number (auto-satisfied if --value parses as a number)
#   C2 not reverse-engineered  (--independent yes/no)
#   C3 executable test path NOT used in fitting (--blind-path yes/no)
#   C4 two-anchor consistency at Planck + particle anchor (--two-anchors yes/no)
# The tool does NOT decide yes/no for C2-C4 from the number alone: the claimant must assert them,
# and the tool records them + runs the numeric two-anchor demonstration so the assertion is auditable.
import os
import sys
import json
import argparse
from decimal import Decimal as Dc, getcontext

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
getcontext().prec = 60

G = Dc('6.67430e-11')
C = Dc('299792458')
HBAR = Dc('1.054571817e-34')
M_E = Dc('9.1093837015e-31')
M_P = (HBAR * C / G).sqrt()


def yes(s):
    return str(s).strip().lower() in ('yes', 'y', '1', 'true', 'pass', '是')


def w3_accept(v, independent, blind_path, two_anchors):
    checks = {
        'C1_quantitative_number': v is not None,
        'C2_not_reverse_engineered': bool(independent),
        'C3_test_path_unused_in_fit': bool(blind_path),
        'C4_two_anchors_consistent': bool(two_anchors),
    }
    return {'passed': all(checks.values()), 'checks': checks}


def two_anchor_demo():
    g_planck = HBAR * C / (M_P ** 2)
    g_electron = HBAR * C / (M_E ** 2)
    return {
        'planck_anchor_rel': format(abs(g_planck - G) / G, '.6E'),
        'electron_anchor_rel': format(abs(g_electron - G) / G, '.6E'),
        'ratio_mP_over_me_sq': format((M_P / M_E) ** 2, '.6E'),
        'note': 'G=hbar c/m^2 passes ONLY at Planck anchor; collapses at electron anchor. '
                'A candidate must not be this kind of anchor-defined identity.',
    }


def main(argv=None):
    p = argparse.ArgumentParser(description='W3 breakthrough acceptance gate (method_F 4 conditions + 2 anchors)')
    p.add_argument('--value', type=str, default=None, help='the claimed dimensionless number')
    p.add_argument('--name', type=str, default='candidate', help='candidate label')
    p.add_argument('--independent', type=str, default='no', help='yes if NOT reverse-solved from system equations')
    p.add_argument('--blind-path', dest='blind_path', type=str, default='no',
                   help='yes if an executable test path exists and was NOT used in fitting')
    p.add_argument('--two-anchors', dest='two_anchors', type=str, default='no',
                   help='yes if consistent at Planck + particle anchors')
    p.add_argument('--json', action='store_true', help='emit JSON only')
    a = p.parse_args(argv)

    v = None
    if a.value is not None:
        try:
            v = Dc(a.value)
        except Exception:
            v = None
    res = w3_accept(v, yes(a.independent), yes(a.blind_path), yes(a.two_anchors))
    out = {
        'name': a.name,
        'value': str(v) if v is not None else None,
        'verdict': 'W3_PASS' if res['passed'] else 'NOT_W3',
        'checks': res['checks'],
        'failed_gates': [k for k, val in res['checks'].items() if not val],
        'two_anchor_reference': two_anchor_demo(),
        'method_source': 'method_F_第一性判据.md criterion 5 (L3) + criterion 3 (two-anchor)',
    }
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print('CANDIDATE:', a.name, '| value=', out['value'])
        print('VERDICT:', out['verdict'])
        for k, val in res['checks'].items():
            print('  [' + ('PASS' if val else 'FAIL') + ']', k)
        if out['failed_gates']:
            print('FAILED GATES:', ', '.join(out['failed_gates']))
        print('Two-anchor reference (G=hbar c/m^2): Planck rel=' + out['two_anchor_reference']['planck_anchor_rel']
              + '  electron rel=' + out['two_anchor_reference']['electron_anchor_rel'])
    return 0 if res['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
