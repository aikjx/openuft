# -*- coding: utf-8 -*-
# TUFT V3.4 自由参数收支核算审计（2026-10-10）
# 对象：精确量化 TUFT 的预测性——自由参数数 vs 独立约束数。
#       这是「圈系数首原导出」问题的核心判据：net>0 则欠定(可重参化非预测)。
# 自由参数：lambda, phi0, B1..B4(4), 圈系数 C1,C2,C3,C4,D1,D2,F1,F2,F3(9-1=8,C4由bracket锁), s=c*/G*
#            β(锁C4), tau_bg(锁Y_B), Lambda0(锁1/8piG) 不独立 -> 自由=1+1+4+8+1=15
# 独立约束：alpha_s, alpha, alpha_W, alpha_G(4观测), bracket=0, alpha*/G*(2不动点), Y_B, Δa_e(弱)
import json, os
# ---- 自由参数清单 ----
FREE = {
 "lambda(全局耦合)":1,"phi0(弱域手征相位)":1,"B1..B4(分区几何边界)":4,
 "圈系数 C1,C2,C3,C4,D1,D2,F1,F2,F3(9,C4由bracket锁)":8,"s=c*/G*(不动点比例)":1}
FREE_TOTAL=sum(FREE.values())
# ---- 独立约束清单 ----
CONS = {
 "alpha_s(M_Z)=0.1179":1,"alpha(M_Z)=7.815e-3":1,"alpha_W=0.01696":1,"alpha_G~1.75e-45":1,
 "不动点 bracket=0":1,"alpha*/G*=0.4773":1,"重子 Y_B=8.7e-11":1,"g-2 Delta_a_e(V3.3,弱)":1}
CONS_TOTAL=sum(CONS.values())
# ---- 由首原可望新增的约束（若 TUFT 给拉氏量/场内容）----
FP_POTENTIAL=0  # 待 TUFT 内部输入
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
@guard("count_free","自由参数总数（独立）")
def _():
    return True,"自由参数=%d（λ,φ0,B1..B4,圈系数8,s）"%FREE_TOTAL
@guard("count_constraints","独立约束总数（观测+不动点+宇宙学）")
def _():
    return True,"独立约束=%d（4观测+2不动点+重子+g-2）"%CONS_TOTAL
@guard("net_free","净自由参数 = 自由-约束")
def _():
    net=FREE_TOTAL-CONS_TOTAL
    ok=net<=0
    return ok,"net=%d：%s"%(net,"可预测(净≤0)" if net<=0 else "欠定(净>0)：可重参化非预测")
@guard("fp_reduces","不动点结构对圈系数的削减（bracket+α*/G* 两等式）")
def _():
    loop=8; s=1; relations=2
    after=loop+s-relations
    return True,"圈系数+s=9，不动点两等式削减后剩 %d 个自由（仍欠定）"%after
@guard("honest_verdict","圈系数首原导出是否成立")
def _():
    net=FREE_TOTAL-CONS_TOTAL
    need=max(0,net)
    return True,"TUFT V3.4 净欠定 %d 个参数：圈系数首原导出需 ~%d 条来自拉氏量/场内容的独立首原关系"%(need,need)

def main():
    grd=run(); np_=sum(1 for g in grd if g["ok"]); nf=len(grd)-np_
    net=FREE_TOTAL-CONS_TOTAL
    results={"engine":"TUFT_V3.4自由参数收支核算","date":"2026-10-10",
        "guards":grd,"n_pass":np_,"n_fail":nf,
        "computed":{"free_total":FREE_TOTAL,"cons_total":CONS_TOTAL,"net_free":net,
                    "free_items":FREE,"constraint_items":CONS}}
    L=["# TUFT V3.4 自由参数收支核算 — 审计报告",
       "- 引擎：源码/TUFT_V3.4自由参数收支核算_2026-10-10.py",
       "- 对象：精确量化预测性 = 自由参数 − 独立约束；net>0 则欠定（可重参化非预测）",
       "- 读数：%d guard PASS %d/FAIL %d (exit %d)"%(len(grd),np_,nf,0 if nf==0 else 2),""]
    for g in grd: L.append("| %s | %s | %s |"%("PASS" if g["ok"] else "FAIL",g["name"],g["note"]))
    L += ["","### 自由参数明细（%d 个）"%FREE_TOTAL]
    for k,v in FREE.items(): L.append("| %s | %d |"%(k,v))
    L += ["","### 独立约束明细（%d 条）"%CONS_TOTAL]
    for k,v in CONS.items(): L.append("| %s | %d |"%(k,v))
    L += ["","### 关键结论",
        "| 量 | 值 |",
        "|---|---|",
        "| 自由参数 | %d |"%FREE_TOTAL,
        "| 独立约束 | %d |"%CONS_TOTAL,
        "| **净自由参数** | **%d** |"%net,
        "","### 裁定（缺口 #1：圈系数首原）",
        "1. **TUFT V3.4 净欠定 %d 个参数**——固定点 bracket/α*/G* 两等式只削减 2 个圈系数自由度，观测+宇宙学约束（8 条）不足以闭合 15 个自由参数。"%net,
        "2. **「圈系数首原导出」当前不成立**：λ、φ0、B1..B4、圈系数 C1..F3、s 均无来自 TUFT 内部结构（拉氏量/场内容）的独立首原关系——奥卡姆未闭环精确化为净欠定 %d。"%net,
        "3. **要成为预测性理论需**：~%d 条独立首原关系（如：拉氏量固定圈系数、四力分区几何固定 B_i、自洽性固定 φ0 等）。"%(max(0,net)),
        "4. **这与 V3.3 审计「动力学欠定」「常数外生」一致**：六处硬伤之②在此精确量化。",
        "5. **诚实价值**：给出可审计的欠定指数 net=%d，任何「TUFT 能预测 X」的宣称都必须先偿还这笔自由参数债。"%net ]
    report="\n".join(L)
    base=os.path.dirname(os.path.abspath(__file__)); data_dir=os.path.abspath(os.path.join(base,"..","数据"))
    os.makedirs(data_dir,exist_ok=True)
    stem="TUFT_V3.4自由参数收支核算_2026-10-10"
    with open(os.path.join(data_dir,stem+".json"),"w",encoding="utf-8") as f: json.dump(results,f,ensure_ascii=False,indent=2)
    with open(os.path.join(data_dir,stem+".md"),"w",encoding="utf-8") as f: f.write(report)
    print(report)
    return 0 if nf==0 else 2
if __name__=="__main__":
    import sys; sys.exit(main())
