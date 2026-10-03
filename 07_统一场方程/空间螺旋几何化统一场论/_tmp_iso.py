# -*- coding: utf-8 -*-
"""直接调用模块里的 sp_ricci 并在失败时 dump 局部变量（用 sys.settrace 钩子）。"""
import sys
import traceback

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

P = "29_作用量变分审计_耦合能动张量与迹_2026-10-03.py"
raw = open(P, "rb").read().decode("utf-8").replace("\r\n", "\n")
lines = raw.split("\n")
cut = None
for i, ln in enumerate(lines):
    if "gS, giS, RicS, RS = sp_ricci(g_sch, ct)" in ln:
        cut = i
        break
prefix = "\n".join(lines[:cut])
G = {"__name__": "pfx", "__file__": P}
exec(compile(prefix, P, "exec"), G)


def tracer(frame, event, arg):
    if frame.f_code.co_name == "sp_ricci" and event == "line":
        ln = frame.f_lineno
        if ln == 100:
            loc = frame.f_locals
            print("LINE100 locals:")
            for k in ("rho", "mu", "sig", "L", "s"):
                print("   %s = %r (%s)" % (k, loc.get(k), type(loc.get(k)).__name__))
            dgl = loc.get("dg")
            ginv = loc.get("ginv")
            print("   dg type=%s len=%s" % (type(dgl).__name__, len(dgl) if hasattr(dgl, "__len__") else "NA"))
            try:
                print("   dg[mu] ->", type(dgl[loc["mu"]]).__name__)
            except Exception as e:
                print("   dg[mu] FAILED:", type(e).__name__, e)
            try:
                print("   ginv ->", type(ginv).__name__, "ginv[rho,L] =", ginv[loc["rho"], loc["L"]])
            except Exception as e:
                print("   ginv[rho,L] FAILED:", type(e).__name__, e)
            sys.settrace(None)
    return tracer


sys.settrace(tracer)
try:
    G["sp_ricci"](G["g_sch"], G["ct"])
    print("sp_ricci OK")
except Exception:
    sys.settrace(None)
    print(traceback.format_exc())
    # 逐步手工重现失败
    sp = G["sp"]
    gfun, coords = G["g_sch"], G["ct"]
    g = sp.zeros(4, 4)
    for a in range(4):
        for b in range(4):
            g[a, b] = sp.simplify(gfun(a, b))
    ginv = g.inv()
    dg = [sp.zeros(4, 4) for _ in range(4)]
    for rho in range(4):
        for a in range(4):
            for b in range(4):
                dg[rho][a, b] = sp.diff(g[a, b], coords[rho])
    for rho in range(4):
        for mu in range(4):
            for sig in range(4):
                s = sp.S.Zero
                for L in range(4):
                    print("try rho=%s mu=%s sig=%s L=%s" % (rho, mu, sig, L), end=" ")
                    try:
                        s += ginv[rho, L] * (dg[mu][sig, L] + dg[sig][mu, L] - dg[L][mu, sig])
                        print("ok")
                    except TypeError as e:
                        print("FAIL", e)
                        raise SystemExit(1)
