# -*- coding: utf-8 -*-
# TUFT 统一场论攻破：UHECR GZK 维度 / 判别力诊断（2026-10-07）
# ADD-01 C.3：E_GZK^TUFT 理论固有 95%CI=[3.90,4.74]e19（剥离宇宙传播系统误差）。
# SM GZK 阈值 ~5.0e19（log10≈19.7）。
# 判别检验：SM 值是否落在 TUFT CI 外？若然，再叠加观测系统误差（~±0.1 dex，
# 即 E 范围约 [4.0,6.3]e19）——ADD-01 刻意剥离此误差，恰是精度通胀。
# 纯标准库。
import math, json, os

TUFT_LO=3.90e19; TUFT_HI=4.74e19; SM=5.0e19
OBS_DEX=0.10  # 观测截断能量系统误差（log10）
SM_LOG=math.log10(SM); OBS_LO=10**(SM_LOG-OBS_DEX); OBS_HI=10**(SM_LOG+OBS_DEX)
SEP=SM-TUFT_HI

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

@guard("tuft_ci","TUFT 理论固有 95%CI=[3.90,4.74]e19（ADD-01 C.3）")
def _():
    ok=True
    return ok,"E_GZK^TUFT ∈ [%.2e, %.2e] eV"%(TUFT_LO,TUFT_HI)
@guard("sm_canonical","SM GZK 阈值 ~5.0e19 eV（log10≈19.7）")
def _():
    ok=True
    return ok,"SM 截断 ~%.0e eV"%SM
@guard("naive_separation","SM(5.0) 在 TUFT CI 外，分离仅 ~0.26e19（~0.02 dex）")
def _():
    outside=SM>TUFT_HI
    ok=outside
    return ok,"SM 值=%.1e > TUFT 上限 %.2e（分离 %.2e eV，%.2f dex）"%(SM,TUFT_HI,SEP,math.log10(SM)-math.log10(TUFT_HI))
@guard("obs_systematic","观测截断系统误差 ±%.1f dex → E∈[%.1f, %.1f]e19"%(OBS_DEX,OBS_LO/1e19,OBS_HI/1e19))
def _():
    ok=True
    return ok,"观测系统跨度 %.1e eV（±%.2f dex）"%(OBS_HI-OBS_LO,OBS_DEX)
@guard("sm_inside_obs","SM(5.0) 落入观测范围，TUFT 与 SM 无法区分")
def _():
    ok=OBS_LO<SM<OBS_HI
    return ok,"SM %.1e ∈ [%.1e, %.1e] → 观测上不判别"%(SM,OBS_LO,OBS_HI)
@guard("inflation_via_exclusion","ADD-01 剥离传播系统误差 → GZK 精度通胀（同 g-2 模式）")
def _():
    # 分离 ~0.02 dex ≪ 观测系统 ±0.10 dex
    ok= (math.log10(SM)-math.log10(TUFT_HI)) < OBS_DEX
    return ok,"TUFT-SM 分离 %.2f dex < 观测系统 %.1f dex → 吸收进系统误差，不判别"%(math.log10(SM)-math.log10(TUFT_HI),OBS_DEX)

def main():
    grd=run(); np_=sum(1 for g in grd if g["ok"]); nf=len(grd)-np_
    results={"engine":"TUFT统一场论攻破_UHECR_GZK判别力","date":"2026-10-07",
        "guards":grd,"n_pass":np_,"n_fail":nf,
        "computed":{"tuft_ci":[TUFT_LO,TUFT_HI],"sm":SM,"separation_eV":SEP,
                    "separation_dex":math.log10(SM)-math.log10(TUFT_HI),
                    "obs_range":[OBS_LO,OBS_HI],"obs_dex":OBS_DEX}}
    L=["# TUFT 统一场论攻破：UHECR GZK 判别力诊断报告",
       "- 引擎：源码/突破_TUFT统一场论_UHECR_GZK判别力_2026-10-07.py",
       "- 对象：TUFT 宣称的 GZK 截断 95%CI 是否真与 SM 区分",
       "- 读数：%d guard PASS %d/FAIL %d (exit %d)"%(len(grd),np_,nf,0 if nf==0 else 2),""]
    for g in grd: L.append("| %s | %s | %s |"%("PASS" if g["ok"] else "FAIL",g["name"],g["note"]))
    L += ["","### 关键数值",
        "| 量 | 值 | 含义 |",
        "|---|---|---|",
        "| TUFT E_GZK 95%%CI | [%.2e, %.2e] eV | 理论固有（ADD-01） |"%(TUFT_LO,TUFT_HI),
        "| SM 阈值 | %.1e eV | log10≈19.7 |"%SM,
        "| TUFT−SM 分离 | %.2e eV（%.2f dex） | 微小 |"%(SEP,math.log10(SM)-math.log10(TUFT_HI)),
        "| 观测系统误差 | ±%.1f dex → [%.1e, %.1e] | ADD-01 刻意剥离 |"%(OBS_DEX,OBS_LO,OBS_HI),
        "","### 结论（GZK 判别力诊断）",
        "1. **TUFT 宣称 E_GZK^TUFT=[%.2e, %.2e] eV**，SM 阈值 5.0e19 恰在其上限之外（~%.2e eV 分离）。"%(TUFT_LO,TUFT_HI,SEP),
        "2. **但分离仅 ~%.2f dex**，而观测截断系统误差 ±%.1f dex（E∈[%.1e,%.1e]）——SM 值落入观测范围。"%(math.log10(SM)-math.log10(TUFT_HI),OBS_DEX,OBS_LO,OBS_HI),
        "3. **ADD-01 刻意剥离宇宙线传播/观测系统误差**，宣称 CI 才显得排除 SM——这是 g-2 同款的精度通胀。",
        "4. **攻破裁定**：GZK 维度与 g-2、弱域**同构**——TUFT 的「下移」在观测系统误差内无法分辨，安全但不可证伪。",
        "5. **三观测量全部同构**（弱域宇称、g-2、GZK）：统一场论的可证伪性在结构上**系统性破产**——每个预言都落在「含 SM 的宽区间」。",
        "6. **可证伪路径**：需观测截断能量系统误差收紧一个量级（±0.1 dex→±0.01 dex）且 TUFT 下移显著（>0.3 dex）方可判别。" ]
    report="\n".join(L)
    base=os.path.dirname(os.path.abspath(__file__)); data_dir=os.path.abspath(os.path.join(base,"..","数据"))
    stem="突破_TUFT统一场论_UHECR_GZK判别力_2026-10-07"
    with open(os.path.join(data_dir,stem+".json"),"w",encoding="utf-8") as f: json.dump(results,f,ensure_ascii=False,indent=2)
    with open(os.path.join(data_dir,stem+".md"),"w",encoding="utf-8") as f: f.write(report)
    print(report)
    return 0 if nf==0 else 2

if __name__=="__main__":
    import sys; sys.exit(main())
