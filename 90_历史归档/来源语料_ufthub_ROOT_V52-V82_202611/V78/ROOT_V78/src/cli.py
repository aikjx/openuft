import argparse, json
from . import core as p

def main():
    parser=argparse.ArgumentParser(description='ROOT V78 independent scientific audit')
    parser.add_argument('--B',type=float,default=10,help='magnetic field, T')
    parser.add_argument('--volume',type=float,default=1,help='ideal field volume, m3')
    parser.add_argument('--distance',type=float,default=10,help='far-field observation distance, m')
    parser.add_argument('--f',type=float,default=50,help='magnetic field frequency, Hz')
    args=parser.parse_args()
    energy=p.magnetic_energy(args.B,args.volume)
    out={'G_reference':p.G_CODATA,'c_exact':p.C,'Z_reparameterization':p.z_from_g(),
         'B_T':args.B,'volume_m3':args.volume,'E_field_J':energy,
         'equivalent_mass_kg':p.em_equivalent_mass(energy),
         'point_monopole_estimate_m_s2':p.far_field_monopole_g(energy,args.distance),
         'induction_ratio_ideal':p.induction_energy_ratio_sphere(2*3.141592653589793*args.f,1),
         'synthetic_inference':p.experiment_synthetic_beta(),
         'model_status':'GR reference calculation, not a new-G prediction'}
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
