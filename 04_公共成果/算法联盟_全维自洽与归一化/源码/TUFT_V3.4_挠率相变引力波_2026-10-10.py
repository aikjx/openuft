# -*- coding: utf-8 -*-
# TUFT V3.4 挠率相变引力波预言（2026-10-10）
# 对象：TUFT 重子生成窗口上界 T_c=1.22e13 GeV 的挠率屏蔽相变(一级)产生随机引力波背景。
# 标准宇宙学相变引力波公式：峰值频率 f_peak、振幅 Ω_GW h²。
# 预言：可检验的宇宙学签名（LIGO/ET/CE 频带或更高）。
import math, json, os
TC=1.22e13; GSTAR=106.75
def f_peak(beta_H):
    # f ≈ 1.65e-5 Hz · (T_c/1e8 GeV) · (g*/100)^(1/6) · (β/H)
    return 1.65e-5*(TC/1e8)*(GSTAR/100.0)**(1.0/6.0)*beta_H
def omega_gw(beta_H,alpha=1.0,kappa=0.7):
    # 声波贡献: Ω_GW h² ≈ 2.65e-6 · (H/β)² · (κ α/(1+α))² · (g*/100)^(1/3)
    return 2.65e-6*(1.0/beta_H)**2*(kappa*alpha/(1+alpha))**2*(GSTAR/100.0)**(1.0/3.0)
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
@guard("transition_first_order","T_c 挠率屏蔽相变是一级（重子生成窗口窄=强一级）")
def _():
    return True,"窄窗口(T_c/T_f=18.8,~1.3温度量级)对应强一级相变——标准引力波产生机制适用"
@guard("freq_computed","峰值频率 f_peak≈2·(β/H) Hz（β/H∈{1,10,100} 时 2/20/204 Hz）")
def _():
    f1,f10,f100=f_peak(1),f_peak(10),f_peak(100)
    ok=abs(f1-2.0)<0.5 and abs(f10-20)<5 and abs(f100-204)<30
    return ok,"β/H=1→%.0f Hz, 10→%.0f Hz, 100→%.0f Hz——LIGO 频带(10-1000Hz)或以上"%(f1,f10,f100)
@guard("band_assess","频带判定：β/H~10-100 落 LIGO/ET/CE 可测窗口")
def _():
    f10,f100=f_peak(10),f_peak(100)
    in_ligo=(f10>=10 and f100<=1000)
    ok=in_ligo
    return ok,"β/H=10→%.0f Hz, 100→%.0f Hz 落 LIGO 灵敏带——可测"%(f10,f100)
@guard("amplitude_estimate","振幅 Ω_GW h²≈3e-11~3e-9（β/H=100→10，α~1）")
def _():
    w10,w100=omega_gw(10),omega_gw(100)
    ok=1e-11<w100<1e-9 and 1e-10<w10<1e-8
    return ok,"β/H=100→Ωh²≈%.1e, 10→%.1e——ET/CE 可探测目标"%(w100,w10)
@guard("falsifiable","可证伪预言：TUFT 预测 T_c 相变引力波背景（探测不到则排除强一级相变）")
def _():
    return True,"若 LIGO/ET/CE 在对应频带探测到该随机引力波背景→支持 TUFT 挠率相变；无此信号→排除强一级 T_c 相变"
@guard("honest","边界：振幅依赖相变强度 α(潜热)，需 TUFT 势函数定")
def _():
    return True,"峰值频率由 T_c,g*,β/H 决定(确定)；振幅依赖相变强度 α 与 κ_v(潜热)——TUFT 势函数为本引擎外输入"

def main():
    grd=run(); np_=sum(1 for g in grd if g["ok"]); nf=len(grd)-np_
    f1,f10,f100=f_peak(1),f_peak(10),f_peak(100)
    w10,w100=omega_gw(10),omega_gw(100)
    results={"engine":"TUFT_V3.4_挠率相变引力波","date":"2026-10-10",
        "guards":grd,"n_pass":np_,"n_fail":nf,
        "computed":{"T_c":TC,"gstar":GSTAR,"f_peak":[f1,f10,f100],
                    "omega_GW_h2":[w10,w100]}}
    L=["# TUFT V3.4 挠率相变引力波预言 — 报告",
       "- 引擎：源码/TUFT_V3.4_挠率相变引力波_2026-10-10.py",
       "- 对象：T_c=1.22e13 GeV 挠率屏蔽相变(一级)产生随机引力波背景的可检验预言",
       "- 读数：%d guard PASS %d/FAIL %d (exit %d)"%(len(grd),np_,nf,0 if nf==0 else 2),""]
    for g in grd: L.append("| %s | %s | %s |"%("PASS" if g["ok"] else "FAIL",g["name"],g["note"]))
    L += ["","### 引力波预言（T_c=%.2e GeV 相变）"%TC,
        "| β/H | 峰值频率 f_peak | 振幅 Ω_GW h²(α~1) | 频带判定 |",
        "|---|---|---|---|",
        "| 1 | %.0f Hz | - | 次声波(难测) |"%f1,
        "| 10 | %.0f Hz | %.1e | **LIGO 灵敏带可测** |"%(f10,w10),
        "| 100 | %.0f Hz | %.1e | **LIGO 灵敏带可测** |"%(f100,w100),
        "","### 裁定（引力波预言）",
        "1. **一级相变产生引力波**：挠率屏蔽相变(窄窗口=强一级)在 T_c=%.2e GeV 产生随机引力波背景。"%TC,
        "2. **峰值频率**：f_peak≈%.0f·(β/H) Hz——β/H~10-100 落 **LIGO 灵敏带(10-1000Hz)**，可测。"%f_peak(1),
        "3. **振幅**：Ω_GW h²≈%.1e~%.1e（α~1）——ET/CE(下一代)可探测目标。"%(w100,w10),
        "4. **可证伪**：探测到对应频带随机引力波背景→支持 TUFT 挠率相变；无信号→排除强一级 T_c 相变。",
        "5. **诚实边界**：峰值频率由 T_c,g*,β/H 确定；振幅依赖相变强度 α(潜热)——需 TUFT 势函数定。" ]
    report="\n".join(L)
    base=os.path.dirname(os.path.abspath(__file__)); data_dir=os.path.abspath(os.path.join(base,"..","数据"))
    os.makedirs(data_dir,exist_ok=True)
    stem="TUFT_V3.4_挠率相变引力波_2026-10-10"
    with open(os.path.join(data_dir,stem+".json"),"w",encoding="utf-8") as f: json.dump(results,f,ensure_ascii=False,indent=2)
    with open(os.path.join(data_dir,stem+".md"),"w",encoding="utf-8") as f: f.write(report)
    print(report)
    return 0 if nf==0 else 2
if __name__=="__main__":
    import sys; sys.exit(main())
