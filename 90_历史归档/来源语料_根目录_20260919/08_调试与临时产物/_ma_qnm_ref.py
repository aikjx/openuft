import io,traceback,pickle,numpy as np
out=io.StringIO()
p=r".venv\Lib\site-packages\qnm\schwarzschild\data\Schw_dict.pickle"
try:
    import qnm.schwarzschild.tabulated as tb
    d=pickle.load(open(p,"rb"),encoding="latin1")
    def get(sign,l,n):
        seq=d[(np.int64(sign),l)]
        dd=vars(seq)
        # 找复数 omega 数组
        omega=None
        for k,v in dd.items():
            if isinstance(v,np.ndarray) and np.iscomplexobj(v) and v.ndim==1:
                omega=v; arrname=k; break
        return seq,dd,omega
    for sign,l,n,tag in [(0,0,0,"scalar l=0"),(0,1,0,"scalar l=1"),(0,2,0,"scalar l=2"),
                         (-2,2,0,"grav l=2 n=0"),(-2,2,1,"grav l=2 n=1")]:
        seq,dd,om=get(sign,l,n)
        out.write(f"{tag}: dictkeys={list(dd.keys())}\n")
        if om is not None:
            out.write(f"   omega[{n}] = {om[n]!r}  (arr len {len(om)})\n")
        else:
            out.write(f"   vars={ {k:repr(v)[:120] for k,v in dd.items()} }\n")
except Exception:
    out.write(traceback.format_exc())
open("_ma_qnm_out.txt","w",encoding="utf-8").write(out.getvalue())
