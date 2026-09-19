# -*- coding: utf-8 -*-
# 修正：移除上一脚本误建的 corrections/audits 体例外键，按既有体例并入顶层 v17_odd_potential_audit
import json
p="TUFT_归一化台账_v1.0.json"
d=json.load(open(p,encoding="utf-8"))
print("predictions keys=",list(d.get("predictions",{}).keys()))

# 取回上一脚本挂在 audits 下的独立背书签（若有），移除两个误建键
note=None
au=d.get("audits",{}).get("v17_odd_potential_audit",[])
if au: note=au[0]
d.pop("corrections",None)
d.pop("audits",None)

# 按顶层 v17_odd_potential_audit(list) 体例 append
lst=d["v17_odd_potential_audit"]
if note is None:
    note={"id":"E407_main_agent_independent_areal_verification"}
if not any(isinstance(x,dict) and "main_agent_independent" in str(x.get("id","")) for x in lst):
    lst.append(note)

# 频率勘误#23 并入权威单位/数值体例（该台账无 corrections 数组，记入 units 与 D18 note）
d.setdefault("units",{})["freq_Hz_factor"]="c^3/(2*pi*G*M_sun)=32313 Hz（几何频率->Hz 必须除2π；30Msun GR l=2主频402Hz非2.53kHz, w=.90 969Hz非6.1kHz；勘误#23）"

pr=d.get("predictions",{})
if isinstance(pr,dict) and "D18" in pr and isinstance(pr["D18"],dict):
    pr["D18"]["v17_main_agent_verification"]="外垒≈GR经独立门8.0e-13背书；差异内边界化(主振铃频段,ECO通用)；定量相位/回波/真实BBH+O4-Voyager PSD模板SNR转v18严格势实频IVP"

json.dump(d,open(p,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
json.load(open(p,encoding="utf-8"))
print("FIXED. top keys has corrections/audits:",("corrections" in d),("audits" in d),
      "| v17_odd_potential_audit=",len(d["v17_odd_potential_audit"]),
      "| open_backlog=",len(d["open_backlog"]))
