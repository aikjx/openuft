# -*- coding: utf-8 -*-
"""一次性：在台账 backlog 首条 v19 PRIORITY 上插入 MainAgent 解析骨架指针。保留 CRLF，替换后校验。"""
import io, json
p = r"D:\a10\aikjx\code\my_lib\TUFT_归一化台账_v1.0.json"
with io.open(p, "r", encoding="utf-8", newline="") as f:
    s = f.read()

old = "v19 PRIORITY: quantify R->0 reflecting-core"
new = ("v19 PRIORITY [MA analytic skeleton READY _ma_v19_pole_feedback.py + "
       "TUFT_v19_极点反馈解析骨架_预审.md, NO E-number pending coalition]: "
       "single same-pole delayed copy changes ONLY residue(not pole, proved eps=.3/.73/1); "
       "pole moves only via closed-cavity g e^{iwDt}=1 -> strong comb |w_i|=-ln rho/Dt, spacing "
       "2pi/Dt=.4508(~.374 major reorg), rho=.73 illus tau~44M/3.9x/finesse9.9 BUT rho->0 diverges "
       "(strong-reflection limit only); weak end |w_i|~w_i0(1-R_E) R_E=0->GR11.24M; unified "
       "D0(w)=a e^{iwDt}, D0' OPEN. STEERING: (1) barrier-ONLY two-sided-outgoing IVP r_b(w) "
       "|r|2+|t|2=1, DO NOT reuse v18 net .531(contains absorbing horizon); (2) g=r_core*r_b incl "
       "phase(single-point arg ok, group-delay not); (3) time-domain inject l=m=2 .37367-.08896i with "
       "R->0 core, read middle-coupling delta w/delta damping, scan M_f/incl, GR>=4 digit gate; "
       "(4) PSD SNR last via analytic design curves conditional eps OPEN, do NOT block on LIGO login. "
       "Task: quantify R->0 reflecting-core")

assert s.count(old) == 1, "anchor count=%d" % s.count(old)
s2 = s.replace(old, new)
with io.open(p, "w", encoding="utf-8", newline="") as f:
    f.write(s2)

d = json.load(io.open(p, "r", encoding="utf-8"))
print("OK json valid:", d["version"], d["latest_round"], d["equation_range"])
print("backlog[0] head:", d["open_backlog"][0][:120])
