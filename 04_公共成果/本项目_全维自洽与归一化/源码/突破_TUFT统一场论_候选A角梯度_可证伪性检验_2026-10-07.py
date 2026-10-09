# -*- coding: utf-8 -*-
# TUFT 统一场论攻破：候选 A（弱域角梯度耦合）可证伪性检验（2026-10-07）
# 精确计算 ε(δθ)=|Ω(θ_W−δθ)|−|Ω(θ_W+δθ)| / |Ω(θ_W+δθ)|（Ω=λcos3θ），
# 判定候选 A 是否要求隐蔽小角 δθ~0.03°（决定其生死）。纯标准库。
import math, json, os

LAM=0.1179; THETA_W=math.radians(212.757)   # ADD-02 代表点（cos3θ=0.1438）
DELTA_A=0.001; EPS_CRIT=0.0098              # 存活阈值
def Om(th): return LAM*math.cos(3.0*th)
def eps_exact(dth):  # 精确场值比（取幅值差绝对值；g_L@θ+δ, g_R@θ−δ）
    if abs(Om(THETA_W+dth))<1e-30: return 1e300
    return abs(abs(Om(THETA_W-dth))-abs(Om(THETA_W+dth)))/abs(Om(THETA_W+dth))
def factor_lin():    # |dlnΩ/dθ|·2 = 2·3|tan3θ_W|
    return abs(2.0*3.0*math.tan(3.0*THETA_W))

FAC=factor_lin()
# 求 eps_exact=EPS_CRIT 的 δθ_crit（二分）
lo,hi=0.0,0.05
for _ in range(80):
    mid=0.5*(lo+hi)
    if eps_exact(mid)<EPS_CRIT: lo=mid
    else: hi=mid
DTH_CRIT=lo
# 与扇区尺度 Δθ_W=60° 对比
DTH_W=math.radians(60.0); RATIO=DTH_CRIT/DTH_W

# 扇区整体场值跨度（判断“天然 ε”数量级）
OM_MAX=Om(THETA_W); OM_SECTOR_LO=0.0  # 边界 cos3θ=0
NATURAL_EPS=(Om(THETA_W)-Om(THETA_W-math.radians(30.0)))/Om(THETA_W)  # 半扇区落差

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

@guard("linear_factor","线性系数 2·3|tan3θ_W|≈41.2（攻破方案册需订正）")
def _():
    ok=(38<FAC<44)
    return ok,"2·3|tan3θ_W|=%.2f"%FAC
@guard("exact_matches_linear","精确 ε(δθ) 与线性近似一致（小角，含 2× 系数）")
def _():
    d=1e-3; e_ex=eps_exact(d); e_lin=FAC*d
    ok=abs(e_ex-e_lin)/max(e_ex,1e-12)<0.15
    return ok,"δθ=1e-3：精确 ε=%.4e，线性=%.4e"%(e_ex,e_lin)
@guard("requires_small_angle","候选 A 要求 δθ~0.01–0.03°（隐蔽小角）")
def _():
    dth_deg=math.degrees(DTH_CRIT)
    ok=(0.005<dth_deg<0.1)
    return ok,"δθ_crit=%.5f°（为存活须此隐蔽小角）"%dth_deg
@guard("sector_tiny_fraction","δθ_crit 仅占扇区 ~1e-4，奥卡姆不利")
def _():
    ok=(RATIO<1e-3) and (RATIO>1e-7)
    return ok,"δθ_crit/Δθ_W=%.2e"%RATIO
@guard("natural_eps_overshoots","天然 ε（半扇区落差）超存活阈值")
def _():
    ok=NATURAL_EPS>EPS_CRIT
    return ok,"天然 ε≈%.2f >> 存活 %.4f（未压低则死）"%(NATURAL_EPS,EPS_CRIT)

def main():
    grd=run(); np_=sum(1 for g in grd if g["ok"]); nf=len(grd)-np_
    results={"engine":"TUFT统一场论攻破_候选A角梯度可证伪性","date":"2026-10-07",
        "guards":grd,"n_pass":np_,"n_fail":nf,
        "computed":{"linear_factor":FAC,"dtheta_crit_rad":DTH_CRIT,
                    "dtheta_crit_deg":math.degrees(DTH_CRIT),"dtheta_crit_over_sector":RATIO,
                    "natural_eps_halfsector":NATURAL_EPS,"eps_crit":EPS_CRIT}}
    L=["# TUFT 统一场论攻破：候选 A 可证伪性检验报告",
       "- 引擎：源码/突破_TUFT统一场论_候选A角梯度_可证伪性检验_2026-10-07.py",
       "- 对象：弱域扇区角梯度耦合（θ_W=212.757°）",
       "- 读数：%d guard PASS %d/FAIL %d (exit %d)"%(len(grd),np_,nf,0 if nf==0 else 2),""]
    for g in grd: L.append("| %s | %s | %s |"%("PASS" if g["ok"] else "FAIL",g["name"],g["note"]))
    L += ["","### 关键数值",
        "| 量 | 值 | 含义 |",
        "|---|---|---|",
        "| 线性系数 2·3|tan3θ_W| | %.2f | ε≈系数×δθ |"%FAC,
        "| δθ_crit | %.5f° (%.2e rad) | 存活所需隐蔽小角 |"%(math.degrees(DTH_CRIT),DTH_CRIT),
        "| δθ_crit/Δθ_W | %.2e | 相对扇区尺度 |"%RATIO,
        "| 天然 ε（半扇区落差） | %.2f | 未压低则超限 %d× |"%(NATURAL_EPS,NATURAL_EPS/EPS_CRIT),
        "","### 结论（候选 A 生死判定）",
        "1. 候选 A 正确线性系数 ~%.1f（含 2×，θ_L/θ_R 镜像错开）；精确 ε(δθ) 与线性一致。"%FAC,
        "2. 为存活（ε<%.4f），须 δθ~%.4f°（%.1e 倍扇区）——一个**极度隐蔽的小角**。"%(EPS_CRIT,math.degrees(DTH_CRIT),RATIO),
        "3. 天然 ε（半扇区落差）≈%.2f，超存活阈值约 %d 倍——候选 A 若不解释 δθ 来源，与天然耦合同病超限。"%(NATURAL_EPS,NATURAL_EPS/EPS_CRIT),
        "4. **判定**：候选 A 存活**必须**由 TUFT 自洽推导 δθ~0.01–0.03° 的内在小角；否则被奥卡姆剃刀砍。",
        "5. 攻破方案册的线性系数声明订正为 2·3|tan3θ_W|≈41.2；结论方向不变且更严。",
        "6. 这把「ε 是自由参数」精确翻译成可检验命题：「δθ 必须是可推导的小角（~1e-4 扇区）」。" ]
    report="\n".join(L)
    base=os.path.dirname(os.path.abspath(__file__)); data_dir=os.path.abspath(os.path.join(base,"..","数据"))
    stem="突破_TUFT统一场论_候选A角梯度_可证伪性检验_2026-10-07"
    with open(os.path.join(data_dir,stem+".json"),"w",encoding="utf-8") as f: json.dump(results,f,ensure_ascii=False,indent=2)
    with open(os.path.join(data_dir,stem+".md"),"w",encoding="utf-8") as f: f.write(report)
    print(report)
    return 0 if nf==0 else 2

if __name__=="__main__":
    import sys; sys.exit(main())
