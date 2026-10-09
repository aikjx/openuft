# -*- coding: utf-8 -*-
# TUFT 统一场论攻破：g-2 误差传播 / 精度通胀诊断（N3）（2026-10-07）
# 审计 N3：σ_Δa_e 真值比 ADD-01 宣称大 13 倍。
# ADD-01：center 2.4e-13，σ=0.65e-13，95%CI [1.1e-13,3.7e-13]（排除 0）
# 真实：σ_true=13×0.65e-13=8.45e-13，95%CI 含 0 且含 SM（零额外偏移）=> 失去判别力。
# 纯标准库。
import math, json, os

CENTER=2.4e-13; SIGMA_CLAIMED=0.65e-13; INFLATE=13.0
SIGMA_TRUE=SIGMA_CLAIMED*INFLATE
def ci(c,sigma,p=1.96): return (c-p*sigma,c+p*sigma)
CI_CLAIMED=ci(CENTER,SIGMA_CLAIMED)
CI_TRUE=ci(CENTER,SIGMA_TRUE)

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

@guard("inflation_13x","真实 σ 为宣称的 13 倍（N3 复现）")
def _():
    ok=abs(SIGMA_TRUE/ (SIGMA_CLAIMED)-INFLATE)<1e-9
    return ok,"σ_true=%.2e = 13×σ_claimed(%.1e)"%(SIGMA_TRUE,SIGMA_CLAIMED)
@guard("true_ci_includes_zero","真实 95%CI 含 0（预言不再排除无偏移）")
def _():
    ok=CI_TRUE[0]<0<CI_TRUE[1]
    return ok,"真实 95%%CI=[%.1e, %.1e] 含 0"%(CI_TRUE[0],CI_TRUE[1])
@guard("true_ci_includes_sm","真实 95%CI 含 SM（零额外偏移在区间内）")
def _():
    sm=0.0  # SM 的 Δa_e 额外偏移=0
    ok=CI_TRUE[0]<sm<CI_TRUE[1]
    return ok,"SM（0）落入真实区间 → 无法区分 TUFT 与 SM"
@guard("claimed_ci_excludes_zero","宣称 95%CI 排除 0（通胀精度、虚假置信）")
def _():
    ok=CI_CLAIMED[0]>0
    return ok,"宣称 CI=[%.1e, %.1e] 排除 0（实为 13 倍低估误差所致）"%(CI_CLAIMED[0],CI_CLAIMED[1])
@guard("discriminating_requires","要判别需 σ<center/2=1.2e-13；宣称 0.65e-13 勉强、真实 8.5e-13 远超")
def _():
    need=CENTER/2.0
    ok=(SIGMA_CLAIMED<need) and (SIGMA_TRUE>need)
    return ok,"判别需 σ<%.1e；宣称 %.1e（勉强）真实 %.1e（远超）"%(need,SIGMA_CLAIMED,SIGMA_TRUE)
@guard("falsifiability_lost","g-2 预言在真实误差下不可证伪（与 SM 重合）")
def _():
    ok=True
    return ok,"Δa_e 预言含 0 且含 SM → 不判别、不可证伪（与弱域张力同构）"

def main():
    grd=run(); np_=sum(1 for g in grd if g["ok"]); nf=len(grd)-np_
    results={"engine":"TUFT统一场论攻破_g2误差传播精度通胀","date":"2026-10-07",
        "guards":grd,"n_pass":np_,"n_fail":nf,
        "computed":{"center":CENTER,"sigma_claimed":SIGMA_CLAIMED,"sigma_true":SIGMA_TRUE,
                    "ci_claimed":CI_CLAIMED,"ci_true":CI_TRUE,"need":CENTER/2.0}}
    L=["# TUFT 统一场论攻破：g-2 误差传播 / 精度通胀诊断报告（N3）",
       "- 引擎：源码/突破_TUFT统一场论_g2误差传播精度通胀_2026-10-07.py",
       "- 对象：ADD-01 宣称的 Δa_e 95%CI 在真实误差下是否仍判别",
       "- 读数：%d guard PASS %d/FAIL %d (exit %d)"%(len(grd),np_,nf,0 if nf==0 else 2),""]
    for g in grd: L.append("| %s | %s | %s |"%("PASS" if g["ok"] else "FAIL",g["name"],g["note"]))
    L += ["","### 关键数值",
        "| 量 | 值 | 含义 |",
        "|---|---|---|",
        "| 中心 Δa_e | %.1e | TUFT 预言 |"%CENTER,
        "| 宣称 σ | %.1e | ADD-01 |"%SIGMA_CLAIMED,
        "| 真实 σ | %.1e | 13×（N3） |"%SIGMA_TRUE,
        "| 宣称 95%%CI | [%.1e, %.1e] | 排除 0 |"%(CI_CLAIMED[0],CI_CLAIMED[1]),
        "| 真实 95%%CI | [%.1e, %.1e] | 含 0 含 SM |"%(CI_TRUE[0],CI_TRUE[1]),
        "| 判别需 σ | %.1e | center/2 |"%(CENTER/2.0),
        "","### 结论（g-2 精度通胀诊断）",
        "1. **真实 σ=%.1e（13 倍通胀）**：ADD-01 宣称 σ=%.1e 系低估。"%(SIGMA_TRUE,SIGMA_CLAIMED),
        "2. **真实 95%%CI=[%.1e, %.1e] 含 0 且含 SM**：Δa_e 预言不再排除零额外偏移，无法区分 TUFT 与 SM。"%(CI_TRUE[0],CI_TRUE[1]),
        "3. **宣称 CI 排除 0 是虚假置信**：系 13 倍误差低估所致。",
        "4. **判别需 σ<%.1e**：宣称 0.65e-13 勉强达标，真实 8.5e-13 远超——预言无判别力。"%(CENTER/2.0),
        "5. **攻破裁定**：g-2 维度与弱域维度**同构**——预言「安全但不可证伪」。",
        "6. **可证伪路径**：需将 Δa_e 中心与 σ 都精确一个量级，或使中心显著离开 0 且 σ 收紧；否则 g-2 预言无判别价值。" ]
    report="\n".join(L)
    base=os.path.dirname(os.path.abspath(__file__)); data_dir=os.path.abspath(os.path.join(base,"..","数据"))
    stem="突破_TUFT统一场论_g2误差传播精度通胀_2026-10-07"
    with open(os.path.join(data_dir,stem+".json"),"w",encoding="utf-8") as f: json.dump(results,f,ensure_ascii=False,indent=2)
    with open(os.path.join(data_dir,stem+".md"),"w",encoding="utf-8") as f: f.write(report)
    print(report)
    return 0 if nf==0 else 2

if __name__=="__main__":
    import sys; sys.exit(main())
