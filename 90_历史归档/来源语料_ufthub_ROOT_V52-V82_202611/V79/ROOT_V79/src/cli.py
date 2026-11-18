import argparse,json
from .core import Scenario

def main():
    p=argparse.ArgumentParser(description='Electromagnetic gravity bookkeeping (not a G prediction)')
    p.add_argument('--B',type=float,default=10.)
    p.add_argument('--f',type=float,default=50.)
    p.add_argument('--radius',type=float,default=1.)
    p.add_argument('--distance',type=float,default=10.)
    a=p.parse_args()
    print(json.dumps(Scenario(a.B,a.f,a.radius,a.distance).evaluate(),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
