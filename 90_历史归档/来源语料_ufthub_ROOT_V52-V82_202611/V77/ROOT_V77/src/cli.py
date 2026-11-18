"""ROOT V77 command-line calculator: python -m src.cli --help."""
import argparse
import json
from .gravity_c import *


def main():
    p=argparse.ArgumentParser(description='G–c relationship laboratory (identities, not an independent G prediction)')
    sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('summary',help='CODATA constants and calculated values')
    m=sub.add_parser('mass',help='dimensionless gravitational coupling for a test mass')
    m.add_argument('kg',type=float)
    z=sub.add_parser('from-z',help='calculate G from independently supplied dimensional Z; not a prediction of Z')
    z.add_argument('z',type=float)
    c=sub.add_parser('vary-c',help='conditional toy models of a different c, NOT a physical varying-c theory')
    c.add_argument('factor',type=float)
    args=p.parse_args()
    if args.command=='summary': value=summary()
    elif args.command=='mass':
        if args.kg<=0: p.error('mass must be positive')
        value=mass_radius_consistency(args.kg)
    elif args.command=='from-z': value={'G_SI':g_from_z(args.z),'Z_SI':args.z,'is_independent_prediction':False}
    else: value={'c_factor':args.factor,'conditional_G_SI':c_scaling_models(args.factor),'physical_claim':False}
    print(json.dumps(value,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
