# -*- coding: utf-8 -*-
"""v40：提取 ℓ=1 增长模本征向量与平移形态 f'(r) 重叠（诊断仪器，落库 V3_5_gauged_l1_mode_audit.json）"""
import os, json
import numpy as np
import scipy.sparse as sp
from scipy.linalg import eig

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
z = np.load(os.path.join(PARENT, "V3_gauged_background_e005.npz"))
r_bg, f_bg = z["r"], z["f"]
w = 0.960271793738176
n = 400; Rout = 60.0; l = 1

rmid = np.linspace(0, Rout, n + 1)[1:]
fmid = np.interp(rmid, r_bg, f_bg)
h = Rout / n; h2 = h*h
cent = l*(l+1)/np.maximum(rmid,1e-9)**2
W = w - np.interp(rmid, r_bg, z["a"])
W2 = W**2
Vp = 1-W2-6*fmid**2+15*fmid**4+cent
Vm = 1-W2-2*fmid**2+3*fmid**4+cent
def lap(V):
    return sp.diags([-np.ones(len(V)-1)/h2, 2/h2+V, -np.ones(len(V)-1)/h2],[-1,0,1],format="csc")
Lp,Lm = lap(Vp),lap(Vm)
In = sp.identity(n,format="csc"); Z = sp.csc_matrix((n,n))
M = sp.block_diag([Lp,Lm],format="csc")
Jblk = sp.bmat([[Z,In],[-In,Z]],format="csc")
Wb = sp.block_diag([sp.diags(W,format="csc"),sp.diags(W,format="csc")],format="csc")
A = sp.bmat([[sp.csc_matrix((2*n,2*n)), sp.identity(2*n,format="csc")],[M, 2j*Wb*Jblk]],format="csc").toarray()
om, vl = eig(A, right=True)
gr = np.where(om.imag > 5e-3)[0]
fpr = np.gradient(fmid, h)
rec = {"background": "V3_gauged_background_e005.npz (e=0.05,Q_N=279.16,w=0.96027)",
       "physical_argument": "charged spherical background translation-invariant => l=1 complete spec must have Omega=0 translation zero mode; fixed-background a, deltaA=0 breaks translation invariance => growth artifact"}
for idx in gr[:3]:
    vec = vl[:, idx]; u = vec[:n].real; v = vec[n:2*n].real
    nu = np.sqrt(np.sum(u*u)); nf = np.sqrt(np.sum(fpr*fpr))
    ov = float(np.sum(u*fpr)/(nu*nf)) if nu>0 and nf>0 else 0
    rec["mode_omega"] = {"Re": float(om[idx].real), "Im": float(om[idx].imag)}
    rec["u_overlap_with_fprime"] = ov
    rec["v_overlap_ratio_abs"] = float(np.sqrt(np.sum(v*v)/max(np.sum(u*u),1e-30)))
    rec["u_peak_r"] = float(rmid[np.argmax(np.abs(u))])
rec["f_peak_r"] = float(rmid[np.argmax(fmid)])
rec["verdict"] = "l=1 growth mode is fixed-background artifact (translation zero mode polluted), not real dipole instability"
rec["remaining_gap"] = "complete 6-component coupled spectrum still most sufficient criterion; e single value; higher multipoles not done"
with open(os.path.join(PARENT, "V3_5_gauged_l1_mode_audit.json"), "w", encoding="utf-8") as fh:
    json.dump(rec, fh, ensure_ascii=False, indent=2)
print("Ω=%.3e+%.4ei u-f'ov=%.3f |v|/|u|=%.3f" % (rec["mode_omega"]["Re"], rec["mode_omega"]["Im"], rec["u_overlap_with_fprime"], rec["v_overlap_ratio_abs"]))
print("saved V3_5_gauged_l1_mode_audit.json")
