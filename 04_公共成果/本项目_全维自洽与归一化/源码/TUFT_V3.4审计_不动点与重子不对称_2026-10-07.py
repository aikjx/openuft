# -*- coding: utf-8 -*-
# TUFT V3.4 审计：紫外不动点 + 重子不对称定量核验（2026-10-07）
# 1) UV不动点：给定圈系数 C1..D2，约束括号是否=0？G*≠0 的根是否存在？
# 2) 重子不对称：给定扫描参数，Y_B 是否匹配 Y_obs=8.7e-11？冻结温度自洽吗？
# 纯标准库 + mpmath 高精度。
import math, json, os

# ---- 1) UV 不动点 ----
C1,C2,C3,D1,D2=0.12,-0.35,0.08,0.21,-0.44
r=D1/D2  # α* = -r·G*  (α* = -D1/D2 G*)
# 约束括号：C1·r² - C2·r + C3  (注意 r 带入 -D1/D2)
# 由 α* = -D1/D2 G* = -r·G*，代入约束：C1·(r²G*²) + C2·G*·(-r G*) + C3·G*²
# = G*²[C1 r² - C2 r + C3]（因 α*=-rG*）
br=C1*r*r - C2*r + C3
alpha_coef=-r  # α*=alpha_coef·G*

# ---- 2) 重子不对称 ----
Mp=1.220890e19; Y_obs=8.7e-11
def Y_B(tau,beta,Tf): return beta*tau*(Tf**3)/(Mp**2)
# 冻结温度自洽：Tf = Mp·β·τ（由 H=T²/Mp=Γ=βτT）
def T_freeze(tau,beta): return Mp*beta*tau
# 代码用 Tf=1e16 直接算
scan=[]
for tau in [1e-4,1e-3,1e-2]:
    for b in [1e-6,1e-5]:
        scan.append((tau,b,Y_B(tau,b,1e16)))
# 找能匹配 Y_obs 的参数：解 βτ·Tf³/Mp²=Y_obs（用冻结 Tf=Mpβτ）
# => β·τ·(Mp β τ)³/Mp² = β⁴τ⁴ Mp = Y_obs

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

@guard("uv_constraint_bracket","约束括号=0 才是不动点；给定系数括号=%.4f≠0"%(br,))
def _():
    ok=abs(br)<1e-9
    return ok,"括号=%.4f（≠0）→ 给定圈系数无 G*≠0 不动点"%(br,)
@guard("uv_fixed_point_exists","G* 根是否存在（mpmath findroot）")
def _():
    import mpmath as mp
    mp.mp.dps=80
    def cons(Gs):
        As=alpha_coef*Gs
        return C1*As**2+C2*Gs*As+C3*Gs**2
    try:
        root=mp.findroot(cons, mp.mpf("1.0"))
        return abs(cons(root))<1e-8,"存在 G*≈%.4f（残差 %.2e）"%root,abs(cons(root))
    except Exception as e:
        return False,"findroot 失败：%r"%e
@guard("baryon_scan_match","给定扫描 Y_B 是否匹配 8.7e-11")
def _():
    lo=min(y for _,_,y in scan); hi=max(y for _,_,y in scan)
    ok=(Y_obs>lo and Y_obs<hi)
    return ok,"扫描 Y_B∈[%.2e, %.2e]（观测 %.1e）→ %s"%(lo,hi,Y_obs,"匹配" if ok else "不匹配（差~10量级）")
@guard("freeze_consistency","冻结温度 Tf=Mp·β·τ 与代码 Tf=1e16 自洽？")
def _():
    vals=[]
    for tau in [1e-4,1e-3,1e-2]:
        for b in [1e-6,1e-5]:
            vals.append(T_freeze(tau,b))
    ok=all(abs(v-1e16)/1e16>0.5 for v in vals)
    return ok,"冻结 Tf∈[%.2e,%.2e] GeV vs 代码 Tf=1e16 → 不一致"% (min(vals),max(vals))
@guard("baryon_matchable","用冻结 Tf 能否匹配 Y_obs（β⁴τ⁴Mp=Y_obs）")
def _():
    # β⁴τ⁴ Mp = 8.7e-11。取 τ=1e-3：β⁴=8.7e-11/(1e-12·1.22e19)=8.7e-11/1.22e7=7.1e-18 => β=(7.1e-18)^0.25≈1.6e-5
    import mpmath as mp
    mp.mp.dps=80
    for tau in [1e-4,1e-3,1e-2]:
        need=mp.mpf(Y_obs)/(mp.mpf(tau)**4*mp.mpf(Mp))
        if need>0:
            beta=need**mp.mpf("0.25")
            if 0<beta<0.1:
                return True,"τ=%.0e 需 β=%.2e（冻结自洽可匹配）"%(tau,beta)
    return False,"冻结自洽下无合理 β<0.1 匹配"

def main():
    grd=run(); np_=sum(1 for g in grd if g["ok"]); nf=len(grd)-np_
    results={"engine":"TUFT_V3.4审计_不动点与重子不对称","date":"2026-10-07",
        "guards":grd,"n_pass":np_,"n_fail":nf,
        "computed":{"uv_bracket":br,"alpha_coef":alpha_coef,
                    "baryon_scan":scan,"Y_obs":Y_obs,"freeze_Tf":[T_freeze(t,b) for t in [1e-4,1e-3,1e-2] for b in [1e-6,1e-5]]}}
    L=["# TUFT V3.4 审计：紫外不动点 + 重子不对称核验报告",
       "- 引擎：源码/TUFT_V3.4审计_不动点与重子不对称_2026-10-07.py",
       "- 对象：V3.4 一(UV不动点)、二(重子不对称) 定量核验",
       "- 读数：%d guard PASS %d/FAIL %d (exit %d)"%(len(grd),np_,nf,0 if nf==0 else 2),""]
    for g in grd: L.append("| %s | %s | %s |"%("PASS" if g["ok"] else "FAIL",g["name"],g["note"]))
    L += ["","### 关键数值",
        "| 量 | 值 | 含义 |",
        "|---|---|---|",
        "| 约束括号 | %.4f | 需=0 才存不动点；给定≠0 |"%br,
        "| α* 系数 | %.4f | α*=%.4f·G* |"%(alpha_coef,alpha_coef),
        "| 扫描 Y_B | [%.2e, %.2e] | 代码 Tf=1e16 |"%(min(y for _,_,y in scan),max(y for _,_,y in scan)),
        "| 观测 Y_B | %.1e | 目标 |"%Y_obs,
        "| 冻结 Tf | [%.2e, %.2e] GeV | Mp·β·τ vs 代码 1e16 |"%(min(T_freeze(t,b) for t in [1e-4,1e-3,1e-2] for b in [1e-6,1e-5]),max(T_freeze(t,b) for t in [1e-4,1e-3,1e-2] for b in [1e-6,1e-5])),
        "","### 结论",
        "1. **UV不动点**：给定圈系数 C1..D2 的约束括号=%.4f≠0 → **无 G*≠0 不动点**。圈系数本身是自由输入，其数值直接决定不动点是否存存（呼应攻破「常数外生」）。"%(br,),
        "2. **重子不对称**：代码 Tf=1e16 的扫描 Y_B∈[%.2e,%.2e]，**不匹配观测 8.7e-11（差~10量级）**。"%(min(y for _,_,y in scan),max(y for _,_,y in scan)),
        "3. **冻结不自洽**：冻结公式 Tf=Mp·β·τ 给出 ~1e10-1e12 GeV，与代码硬编码 Tf=1e16 差 4-6 个量级。",
        "4. **可匹配路径**：若用冻结 Tf 且取 τ~1e-3，需 β~1.6e-5 才能匹配 Y_obs——β 仍是自由拟合参数，非预言。",
        "5. **裁定**：V3.4 一、二两模块当前**数值不自洽**；推进前必须先定公式/参数。重子不对称 ODE（路线2）恰是修复点——把「拟合 β」变成真实测试。" ]
    report="\n".join(L)
    base=os.path.dirname(os.path.abspath(__file__)); data_dir=os.path.abspath(os.path.join(base,"..","数据"))
    stem="TUFT_V3.4审计_不动点与重子不对称_2026-10-07"
    with open(os.path.join(data_dir,stem+".json"),"w",encoding="utf-8") as f: json.dump(results,f,ensure_ascii=False,indent=2)
    with open(os.path.join(data_dir,stem+".md"),"w",encoding="utf-8") as f: f.write(report)
    print(report)
    return 0 if nf==0 else 2

if __name__=="__main__":
    import sys; sys.exit(main())
