# -*- coding: utf-8 -*-
# 一次性：把 v17 MainAgent 独立复算结论与勘误#23 并入台账 JSON（json.load 校验 + 清理重复键）
import json,io
p="TUFT_归一化台账_v1.0.json"
raw=open(p,encoding="utf-8").read()
d=json.loads(raw)   # 重复键 continuous_slots 取后者（两处同值 E1-E385+E349-E353，无损）

d["version"]="v1.8"
d["latest_round"]="v17"
d["equation_range"]="E1-E406"
d["last_updated"]="2026-09-18"

# 勘误 #23（若不存在则追加）
corr=d.setdefault("corrections",[])
if not any(isinstance(c,dict) and c.get("id")==23 for c in corr):
    corr.append({
        "id":23,"round":"v17","by":"MainAgent_independent",
        "wrong":"几何频率→Hz 漏除 2π（误用 c^3/GM 而非 c^3/2πGM）：30Msun GR l=2 主频标 2.53 kHz、w=0.90 标 6.1 kHz",
        "correct":"c^3/(2pi GM_sun)=32313 Hz；30Msun 主频 w=.3737 -> 402 Hz、w=.685 -> 738 Hz、w=.90 -> 969 Hz；60Msun 201/369/485 Hz；周期 2.48ms=403Hz 旁证；时间 4.9256 us 本身无误",
        "status":"RED"
    })

# v17 odd 审计追加 MainAgent 独立背书
au=d.setdefault("audits",{}).setdefault("v17_odd_potential_audit",[])
if not any(isinstance(x,dict) and "main_agent" in str(x.get("id","")) for x in au):
    au.append({"id":"E407_main_agent_independent_areal_verification",
      "claim":"独立向量化脚本（不引用并行线代码）确认 E401-E406；首版两处自身bug(GR导数/argmax抓内垒)已现场修正",
      "gr_gate_max_rel_err":8.0e-13,"gr_gate":"PASS(并行脚本同值2.4e-8印FAIL系标签bug)",
      "rw_peak":"R=3.28087 V=0.15128670 sqrt=0.38895591",
      "tuft_outer_barrier":{"c0":[0.3631,3.6739],"c-0.5":[0.4067,2.8077],"c-0.29":[0.3856,3.2680]},
      "c-0.5_inner_vs_outer":"0.468@1.92 系壁侧内垒；外垒 0.407@2.808",
      "wkb_c-0.29":{"w0.374":"s[5.48..8.53] K=0.223 e^-2K=0.640","w0.35":"K=0.702 e^-2K=0.246","cavity_Vmin":0.109},
      "core":"c<0 壁 R->0/e^-2lambda->inf/g_RR->0/龟坐标到R3有限7.2-8.9M；c=0 颈 R_min=e=2.71828",
      "script":"_ma_v17_strict_areal_indep.py",
      "tier":"严格定理(GR门/坐标变换/垒顶) + 条件定理(WKB垒顶仅量级)"})

# 权威 D18 备注（保持对象/字符串两种可能）
pr=d.get("predictions",{})
if isinstance(pr,dict) and "D18" in pr:
    pr["D18"]["main_agent_note"]=("v17坐标纠错已由MainAgent独立门8e-13背书：外垒≈GR、差异内边界化(主振铃频段,ECO通用);"
                                  "定量反射相位/回波/真实BBH+O4/Voyager PSD模板SNR转v18严格势实频IVP;频率见勘误#23")

# backlog 顶部确保 v18 任务（若已有则不重复）
ob=d.get("open_backlog") or []
v18task=("v18：在严格面积odd势 R=rho sqrt(B),e^-2lambda=(1+rho B'/2B)^2,V=3A(1+e^-2lambda)/R^2 上跑MainAgent v15稳定实频IVP"
         "（壁Neumann、scipy DOP853、垒外C+/C-分解、tau=dphi/dw）；同码先过GR Schwarzschild吸收视界门并对齐E386；"
         "给w=0.30-0.70 |R_TUFT|^2=1与相位延迟拱；再在w~0.35-0.55主振铃带用真实多模BBH模板+真实O4/Voyager PSD(非同形缩放)算echo/modified-ringdown模板SNR")
if not any("v18" in str(x)[:6] for x in ob):
    ob.insert(0,v18task); d["open_backlog"]=ob

open(p,"w",encoding="utf-8").write(json.dumps(d,ensure_ascii=False,indent=2))
# 复读校验
json.load(open(p,encoding="utf-8"))
print("OK json valid; corrections=",len(corr),"; v17 audit entries=",len(au),
      "; continuous_slots occurrences in raw=",raw.count('"continuous_slots"'))
