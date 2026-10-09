# -*- coding: utf-8 -*-
# TUFT 统一场论攻破：弱域几何结构诊断（2026-10-07）
# 从第一性原理诊断：为什么弱域宇称修正 ε 天生极端敏感。
# 关键事实：三瓣中心 |Ω|=λ（单 λ 无法区分三力强度，须代表点 dodge）；
# 弱代表点贴近 cos3θ=0 零点，分数梯度最大 => ε 对角度极端敏感（ε≈41δθ）。
# 纯标准库。
import math, json, os

LAM=0.1179
ALPHA_EM=1.0/137.036; ALPHA_S=LAM; ALPHA_W=0.01696
# 三力观测耦合
# 各瓣中心角（ADD-02）：EM=0°, Strong=120°, Weak=240°（cos3θ=1 于中心）
SECTORS={"EM":{"center":0.0,"obs":ALPHA_EM},
         "Strong":{"center":120.0,"obs":ALPHA_S},
         "Weak":{"center":240.0,"obs":ALPHA_W}}
TH_W=212.757  # 弱代表点
def cos3(th_deg): return math.cos(math.radians(3.0*th_deg))
def rep_angle(obs):  # 由 obs/λ=cos3θ 反解代表角（取最近瓣中心）
    r=obs/LAM
    if abs(r)>1: return None
    a=math.degrees(math.acos(r))/3.0
    return a

GUARDS=[]
def guard(name,detail=""):
    def deco(fn):
        GUARDS.append({"name":name,"fn":fn,"detail":detail}); return fn
    return deco
def run():
    out=[]
    for g in GUARDS:
        try: ok,note=g["fn"]()
        except Exception as e: ok,note=False,"EXC %r"%e
        out.append({"name":g["name"],"ok":ok,"note":note})
    return out

@guard("single_lambda_peaks","三瓣中心 |Ω|=λ=α_s（单 λ 无法区分三力强度）")
def _():
    em=cos3(SECTORS["EM"]["center"]); st=cos3(SECTORS["Strong"]["center"]); wk=cos3(SECTORS["Weak"]["center"])
    ok=(abs(em-1)<1e-9) and (abs(st-1)<1e-9) and (abs(wk-1)<1e-9)
    return ok,"EM/Strong/Weak 中心 cos3θ 均=%.4f/%.4f/%.4f（全=λ）"%(em,st,wk)
@guard("couplings_span_16x","观测三力耦合跨度 16×（α_em..α_s）")
def _():
    span=ALPHA_S/ALPHA_EM
    ok=(span>10)
    return ok,"α_s/α_em=%.1f×（0.1179/0.0073）"%span
@guard("rep_point_dodge","须代表点 dodge 区分强度（三力各异代表角）")
def _():
    th_em=rep_angle(ALPHA_EM); th_w=TH_W
    ok=(th_em is not None) and abs(th_em-0)<45
    return ok,"EM 代表点=%.1f°（cos3θ=α_em/α_s=%.4f）；Weak 代表点=%.1f°"%(th_em,ALPHA_EM/ALPHA_S,th_w)
@guard("weak_near_zero","弱代表点贴近场零点（cos3θ=0.1438，小）")
def _():
    v=cos3(TH_W); ok=(0.05<v<0.5)
    return ok,"cos3θ_W=%.4f（|Ω_W|=λ·%.4f=α_W）"%(v,v)
@guard("weak_max_gradient","非峰力域均贴零点、梯度大（EM 更甚；仅 Strong 在峰值为 0）")
def _():
    # 各代表点分数梯度 |dlnΩ/dθ| = |3 tan3θ|
    grad_em=abs(3.0*math.tan(math.radians(3.0*rep_angle(ALPHA_EM))))
    grad_st=abs(3.0*math.tan(math.radians(3.0*SECTORS["Strong"]["center"])))
    grad_w=abs(3.0*math.tan(math.radians(3.0*TH_W)))
    ok=(grad_st<1e-6) and (grad_w>15) and (grad_em>30)
    return ok,"EM grad=%.1f/rad > Weak %.1f/rad >> Strong %.1f（仅峰位不敏感）"%(grad_em,grad_w,grad_st)
@guard("sensitivity_origin","弱域 ε≈41δθ 敏感（与 EM 同理：贴零点）")
def _():
    # ε≈2·grad·δθ；弱域 grad≈20.6 => ε≈41δθ，需 δθ~1e-4 扇区
    grad_w=abs(3.0*math.tan(math.radians(3.0*TH_W)))
    dth_crit_rad=0.0098/(2*grad_w)  # ε=0.0098
    ok=(0.5e-4<dth_crit_rad<5e-4)
    return ok,"存活需 δθ≈%.3e rad（%.4f°）= 2·%.1f·δθ"%(dth_crit_rad,math.degrees(dth_crit_rad),grad_w)

def main():
    grd=run(); np_=sum(1 for g in grd if g["ok"]); nf=len(grd)-np_
    results={"engine":"TUFT统一场论攻破_弱域几何结构诊断","date":"2026-10-07",
        "guards":grd,"n_pass":np_,"n_fail":nf,
        "computed":{"lambda":LAM,"alpha_em":ALPHA_EM,"alpha_s":ALPHA_S,"alpha_w":ALPHA_W,
                    "span_alpha_s_over_em":ALPHA_S/ALPHA_EM,
                    "cos3theta_W":cos3(TH_W),"theta_W":TH_W,
                    "grad_weak":abs(3.0*math.tan(math.radians(3.0*TH_W))),
                    "grad_em":abs(3.0*math.tan(math.radians(3.0*rep_angle(ALPHA_EM))))}}
    L=["# TUFT 统一场论攻破：弱域几何结构诊断报告",
       "- 引擎：源码/突破_TUFT统一场论_弱域几何结构诊断_2026-10-07.py",
       "- 对象：Ω=λcos3θ 单 λ 结构的弱域几何（为什么 ε 天生敏感）",
       "- 读数：%d guard PASS %d/FAIL %d (exit %d)"%(len(grd),np_,nf,0 if nf==0 else 2),""]
    for g in grd: L.append("| %s | %s | %s |"%("PASS" if g["ok"] else "FAIL",g["name"],g["note"]))
    L += ["","### 关键结构事实",
        "| 事实 | 值 | 含义 |",
        "|---|---|---|",
        "| 三瓣中心 cos3θ | 均=1 | 单 λ 下三力中心强度全=λ=α_s |",
        "| 观测耦合跨度 | α_s/α_em=%.1f× | 单 λ 无法同时匹配三力 |"%(ALPHA_S/ALPHA_EM),
        "| EM 代表点 cos3θ | %.4f（28.8°） | 贴零点，grad=%.1f/rad |"%(cos3(rep_angle(ALPHA_EM)),abs(3.0*math.tan(math.radians(3.0*rep_angle(ALPHA_EM))))),
        "| 弱代表点 cos3θ_W | %.4f（212.8°） | 贴零点，grad=%.1f/rad |"%(cos3(TH_W),abs(3.0*math.tan(math.radians(3.0*TH_W)))),
        "| Strong 代表点（峰值） | cos3θ=1（120°） | grad=0，唯一不敏感 |",
        "","### 结论（结构诊断）",
        "1. **单 λ 缺陷**：Ω=λcos3θ 的三瓣中心 |Ω| 全=λ=α_s，观测耦合跨度 16×，须靠代表点 dodge 区分——结构上过定。",
        "2. **代表点 dodge 使非峰力域全敏感**（订正）：EM 代表点 28.8°（cos3θ=0.0619，grad 48.4/rad）比弱域 212.8°（grad 20.6/rad）更贴零点；仅 Strong（峰值 120°）不敏感。",
        "3. **ε 敏感的几何根源**：非峰力域贴场零点 → 分数梯度大 → ε≈2·grad·δθ 巨大（弱域≈41δθ，存活需 δθ~1e-4 扇区）。不是机制缺失，是贴零点放大。",
        "4. **攻破方向修正**：与其找压低机制，不如直面结构缺陷——单 λ 过定 + 非峰力域贴零点。候选 C：重审幅值结构（多 λ / 移代表点避开零点）是更根本的奥卡姆解。",
        "5. 这把「ε 需要极小角」从机制问题升级为**结构诊断**：力域放置位置（贴零点）决定了其极端敏感性。" ]
    report="\n".join(L)
    base=os.path.dirname(os.path.abspath(__file__)); data_dir=os.path.abspath(os.path.join(base,"..","数据"))
    stem="突破_TUFT统一场论_弱域几何结构诊断_2026-10-07"
    with open(os.path.join(data_dir,stem+".json"),"w",encoding="utf-8") as f: json.dump(results,f,ensure_ascii=False,indent=2)
    with open(os.path.join(data_dir,stem+".md"),"w",encoding="utf-8") as f: f.write(report)
    print(report)
    return 0 if nf==0 else 2

if __name__=="__main__":
    import sys; sys.exit(main())
