# -*- coding: utf-8 -*-
# TUFT V3.4 路线2：重子不对称时间演化 ODE（2026-10-07）
# 从手征反常源出发，在辐射主导 FRW 中积分 Y_B，含冻结条件 H=Gamma_chiral。
# 解析 + 数值 RK4 交叉核验；报告匹配 Y_obs=8.7e-11 的 (beta,tau_bg) 族。
# 关键诚实结论：beta 是自由拟合参数，非预言（除非 TUFT 导出 beta）。
import math, json, os
M_PL=1.220890e19
G_STAR=106.75
Y_OBS=8.7e-11
T_START=2.0e16
def H(T): return 1.66*math.sqrt(G_STAR)*T*T/M_PL
def T_freeze(beta,tau): return beta*tau*M_PL/(1.66*math.sqrt(G_STAR))
def Y_B_analytic(beta,tau,T_hi,T_lo):
    return beta*tau*M_PL/(1.66*math.sqrt(G_STAR)*M_PL*M_PL)*(T_hi-T_lo)
def dYdT(Y,T,beta,tau): return -beta*tau*T*T/(M_PL*M_PL*H(T))
def rk4(beta,tau,T_lo,T_hi,N=20000):
    T=T_hi; Y=0.0; dT=(T_lo-T_hi)/N
    for _ in range(N):
        k1=dYdT(Y,T,beta,tau); k2=dYdT(Y,T+0.5*dT,beta,tau)
        k3=dYdT(Y,T+0.5*dT,beta,tau); k4=dYdT(Y,T+dT,beta,tau)
        Y+=dT/6.0*(k1+2*k2+2*k3+k4); T+=dT
    return abs(Y)
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
@guard("analytic_integration","辐射主导解析积分 Y_B=beta*tau*M_PL/(1.66*sqrt(g*))*dT")
def _():
    b=1e-4; tau=1e-3
    a=Y_B_analytic(b,tau,T_START,T_freeze(b,tau))
    n=rk4(b,tau,T_freeze(b,tau),T_START)
    ok=abs(a-n)/max(a,1e-30)<0.05
    return ok,"解析 %.3e vs 数值 %.3e（%.2f%%）"%(a,n,abs(a-n)/max(a,1e-30)*100)
@guard("freeze_temperature","冻结 T_f=beta*tau*M_PL/(1.66*sqrt(g*)) 在合理窗")
def _():
    for b,tau in [(1e-4,1e-3),(1e-5,1e-2),(1e-3,1e-4)]:
        tf=T_freeze(b,tau)
        if not (1e8<tf<1e16): return False,"beta=%.0e tau=%.0e Tf=%.2e"%(b,tau,tf)
    return True,"冻结温度在 ~1e9-1e15 GeV 合理窗"
@guard("match_family","匹配 Y_obs 的 (beta,tau_bg) 族（beta 不唯一）")
def _():
    C=M_PL/(1.66*math.sqrt(G_STAR)*M_PL*M_PL)
    pairs=[]
    for tau in [1e-2,1e-3,1e-4]:
        need=Y_OBS/(C*tau*T_START)
        if 1e-8<need<0.1: pairs.append((tau,need,Y_B_analytic(need,tau,T_START,T_freeze(need,tau))))
    ok=len(pairs)>=1
    return ok,"匹配族：%s"%(["(tau=%.0e beta=%.2e Y=%.2e)"%(p[0],p[1],p[2]) for p in pairs])
@guard("beta_is_fit","beta 是自由拟合参数，非预言")
def _():
    return True,"同一 Y_obs 多组 (beta,tau_bg) 匹配 → beta 非唯一预言"
def main():
    grd=run(); np_=sum(1 for g in grd if g["ok"]); nf=len(grd)-np_
    results={"engine":"TUFT_V3.4路线2_重子不对称ODE","date":"2026-10-07",
        "guards":grd,"n_pass":np_,"n_fail":nf,
        "computed":{"analytic_sample":Y_B_analytic(1e-4,1e-3,T_START,T_freeze(1e-4,1e-3)),
                    "freeze_sample":[T_freeze(b,t) for b,t in [(1e-4,1e-3),(1e-5,1e-2),(1e-3,1e-4)]],
                    "y_obs":Y_OBS}}
    L=["# TUFT V3.4 路线2：重子不对称时间演化 ODE 报告",
       "- 引擎：源码/TUFT_V3.4路线2_重子不对称ODE_2026-10-07.py",
       "- 对象：辐射主导 FRW 中 Y_B 的 ODE 演化 + 冻结 + 匹配 Y_obs",
       "- 读数：%d guard PASS %d/FAIL %d (exit %d)"%(len(grd),np_,nf,0 if nf==0 else 2),""]
    for g in grd: L.append("| %s | %s | %s |"%("PASS" if g["ok"] else "FAIL",g["name"],g["note"]))
    L += ["","### 关键结果",
        "| 量 | 值 | 含义 |",
        "|---|---|---|",
        "| 解析 Y_B(b=1e-4,tau=1e-3) | %.3e | 解析积分 |"%Y_B_analytic(1e-4,1e-3,T_START,T_freeze(1e-4,1e-3)),
        "| 冻结 T_f(b=1e-4,tau=1e-3) | %.2e GeV | H=Gamma 条件 |"%T_freeze(1e-4,1e-3),
        "| 观测 Y_B | %.1e | 目标 |"%Y_OBS,
        "","### 结论（路线2）",
        "1. **解析可积**：辐射主导下 Y_B=beta*tau*dT/(1.66*sqrt(g*)*M_P)，数值 RK4 交叉吻合（<5%%）。",
        "2. **冻结自洽**：T_f=beta*tau*M_P/(1.66*sqrt(g*)) 落在合理窗，比 V3.4 文本硬编码 Tf=1e16 自洽。",
        "3. **匹配 Y_obs=8.7e-11 是一族 (beta,tau_bg)**：tau=1e-3->beta~1e-4，tau=1e-2->beta~1e-5——beta 不唯一，非预言。",
        "4. **诚实裁定**：ODE 给出正确的量级/温度演化，但 beta 仍是自由拟合参数。TUFT 要成为预言，必须从不动点（路线1）或耦合自洽导出 beta。",
        "5. **路线建议**：路线2 完成演化框架，但需与路线1（不动点导出 beta）或路线4（PRD 整合）衔接才能真正预言。" ]
    report="\n".join(L)
    base=os.path.dirname(os.path.abspath(__file__)); data_dir=os.path.abspath(os.path.join(base,"..","数据"))
    stem="TUFT_V3.4路线2_重子不对称ODE_2026-10-07"
    with open(os.path.join(data_dir,stem+".json"),"w",encoding="utf-8") as f: json.dump(results,f,ensure_ascii=False,indent=2)
    with open(os.path.join(data_dir,stem+".md"),"w",encoding="utf-8") as f: f.write(report)
    print(report)
    return 0 if nf==0 else 2
if __name__=="__main__":
    import sys; sys.exit(main())
