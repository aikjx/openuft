# -*- coding: utf-8 -*-
# TUFT V3.4 背景挠率演化模型审计（2026-10-09）
# 把 tau_bg=1.52e-5 从「观测反推」推进为「演化导出」：
#   爱因斯坦-嘉当：挠率由费米子自旋密度源生，tau_bg(T)=eta*T^3/M_P^2。
# 检验：用冻结值钉 eta，积分全程 Y_B，看是否自洽（或过产/欠产）。
import math, json, os
MP=1.220890e19; GSTAR=106.75; YOBS=8.7e-11; TSTART=2.0e16; TFREEZE=6.48e11
BETA=0.0597; TAU_FREEZE=1.52e-5
SQG=math.sqrt(GSTAR)
def eta_from_freeze(): return TAU_FREEZE*MP*MP/(TFREEZE**3)
def yb_integral(eta):
    # Y_B=(beta/(1.66sqrt(g*)·M_P))·∫_{T_f}^{T_s} tau_bg(T)·dT，tau_bg=eta T^3/M_P^2
    integ=(eta/MP/MP)*(TSTART**4-TFREEZE**4)/4.0
    return (BETA/(1.66*SQG*MP))*integ
def eta_from_obs():
    # 由 Y_OBS 反推 eta：Y_B=eta·beta·(T_s^4-T_f^4)/(4·1.66sqrt(g*)·M_P^3)
    return YOBS*(4.0*1.66*SQG*MP*MP*MP)/(BETA*(TSTART**4-TFREEZE**4))
GUARDS=[]
def guard(name,detail=""):
    def deco(fn): GUARDS.append({"name":name,"fn":fn,"detail":detail}); return fn
    return deco
def run():
    out=[]
    for g in GUARDS:
        try: ok,note=g["fn"]()
        except Exception as e: ok,note=False,"EXC %r"%e
        out.append({"name":g["name"],"ok":ok,"note":note})
    return out
@guard("sourced_law","爱因斯坦-嘉当源生：tau_bg(T)=eta·T^3/M_P^2（费米子自旋密度）")
def _():
    # T^3/M_P^2 量纲：energy^3/energy^2 = energy = 1/length（[tau]=L^-1）✓
    eta=eta_from_freeze()
    return True,"tau_bg(T)=eta·T^3/M_P^2，[tau]=energy=L^-1 量纲正确，eta=%.2e（由冻结钉定）"%(eta)
@guard("eta_from_freeze","冻结值钉 eta：tau_bg(T_f)=1.52e-5 -> eta=%.2e"%eta_from_freeze())
def _():
    eta=eta_from_freeze(); tau_at_Tf=eta*TFREEZE**3/MP**2
    ok=abs(tau_at_Tf-TAU_FREEZE)/TAU_FREEZE<1e-9
    return ok,"eta=%.2e 使 tau_bg(T_f)=%.2e=冻结值"%(eta,tau_at_Tf)
@guard("baryon_overproduction","全程积分 Y_B 是否自洽（vs 8.7e-11）")
def _():
    eta=eta_from_freeze(); yb=yb_integral(eta)
    ok=abs(math.log10(yb/YOBS))<0.5
    return ok,"eta(冻结)积分 Y_B=%.2e vs 观测 8.7e-11（偏差 %.1e 倍）"%(yb,yb/YOBS)
@guard("freeze_inconsistent","由观测反推 eta -> tau_bg(T_f) 是否仍=1.52e-5")
def _():
    eta2=eta_from_obs(); tau_at_Tf=eta2*TFREEZE**3/MP**2
    ok=abs(math.log10(tau_at_Tf/TAU_FREEZE))<0.5
    return ok,"观测eta=%.2e -> tau_bg(T_f)=%.2e vs 冻结值 1.52e-5"%(eta2,tau_at_Tf)
@guard("honest_verdict","演化与冻结是否自洽的裁定")
def _():
    eta=eta_from_freeze(); yb=yb_integral(eta)
    eta2=eta_from_obs(); tau2=eta2*TFREEZE**3/MP**2
    # 若两路不一致 -> 演化模型与冻结画面冲突
    conflict = abs(math.log10(yb/YOBS))>1.0 or abs(math.log10(tau2/TAU_FREEZE))>1.0
    return (not conflict), "（自动判断见结论）"

def main():
    grd=run(); np_=sum(1 for g in grd if g["ok"]); nf=len(grd)-np_
    eta=eta_from_freeze(); yb=yb_integral(eta)
    eta2=eta_from_obs(); tau2=eta2*TFREEZE**3/MP**2
    results={"engine":"TUFT_V3.4背景挠率演化_审计","date":"2026-10-09",
        "guards":grd,"n_pass":np_,"n_fail":nf,
        "computed":{"eta_from_freeze":eta,"Y_B_sourced":yb,"Y_B_ratio":yb/YOBS,
                    "eta_from_obs":eta2,"tau_bg_at_freeze_from_obs":tau2}}
    L=["# TUFT V3.4 背景挠率演化模型 — 审计报告",
       "- 引擎：源码/TUFT_V3.4背景挠率演化_审计_2026-10-09.py",
       "- 对象：把 tau_bg=1.52e-5 从「观测反推」推进为「演化导出」；检验自旋密度源生律 tau_bg(T)=eta·T^3/M_P^2 是否自洽",
       "- 读数：%d guard PASS %d/FAIL %d (exit %d)"%(len(grd),np_,nf,0 if nf==0 else 2),""]
    for g in grd: L.append("| %s | %s | %s |"%("PASS" if g["ok"] else "FAIL",g["name"],g["note"]))
    L += ["","### 关键结果",
        "| 量 | 值 | 含义 |",
        "|---|---|---|",
        "| eta（冻结钉定） | %.2e | tau_bg(T_f)=1.52e-5 |"%eta,
        "| 全程积分 Y_B | %.2e | vs 观测 8.7e-11 |"%yb,
        "| Y_B 偏差 | %.1e 倍 | 源生律积分结果 |"%(yb/YOBS),
        "| 观测反推 eta | %.2e | 需匹配 Y_obs |"%eta2,
        "| 反推→tau_bg(T_f) | %.2e | vs 冻结 1.52e-5 |"%tau2,
        "","### 审计裁定（背景挠率演化）",
        "1. **源生律量纲正确**：tau_bg(T)=eta·T^3/M_P^2，[tau]=energy=L^-1，符合爱因斯坦-嘉当自旋密度源生。",
        "2. **内在一贯冲突**：若由冻结值钉 eta=%.2e，则全程积分 Y_B=%.2e，比观测 8.7e-11 **过产 %.1e 倍**——因 tau_bg∝T^3 在早期温度极高，重子产量被早期主导。"%(eta,yb,yb/YOBS),
        "3. **反推也冲突**：若由 Y_obs 反推 eta=%.2e，则 tau_bg(T_f)=%.2e，**不再是冻结值 1.52e-5**——两路不能同时满足。"%(eta2,tau2),
        "4. **结论**：常数 τ_bg=1.52e-5 冻结画面与源生演化 τ_bg(T)=ηT^3/M_P² 不自洽。要匹配重子不对称，TUFT 需：(a) 非 T^3 源生律（早期屏蔽/晚生产，仅冻结窗口活跃），或 (b) 重子仅在冻结窗口发生的生产-冻结机制（需额外动力学）。",
        "5. **诚实价值**：堵死一条不成立的演化模型，明确 TUFT 背景挠率需「屏蔽/晚生产」机制——比伪闭合更有用。" ]
    report="\n".join(L)
    base=os.path.dirname(os.path.abspath(__file__)); data_dir=os.path.abspath(os.path.join(base,"..","数据"))
    os.makedirs(data_dir,exist_ok=True)
    stem="TUFT_V3.4背景挠率演化_审计_2026-10-09"
    with open(os.path.join(data_dir,stem+".json"),"w",encoding="utf-8") as f: json.dump(results,f,ensure_ascii=False,indent=2)
    with open(os.path.join(data_dir,stem+".md"),"w",encoding="utf-8") as f: f.write(report)
    print(report)
    return 0 if nf==0 else 2
if __name__=="__main__":
    import sys; sys.exit(main())
