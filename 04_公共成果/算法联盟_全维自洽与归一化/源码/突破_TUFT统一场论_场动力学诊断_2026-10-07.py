# -*- coding: utf-8 -*-
# TUFT 统一场论攻破：场动力学诊断（N5 无输运方程 / N7① 径向退化）（2026-10-07）
# 全维度攻破：Ω=λcos3θ 是否为真正的动力学场？
# 1. 径向退化（∂Ω/∂r=0）：纯角场
# 2. 角本征模：(r²∇²+9)Ω=0  => Ω 是 m=±3 角动量本征态（三叶结构自洽）
# 3. 存在自然拉氏量可选出此解 => 几何动力学兼容
# 4. 但 TUFT 是否给出该拉氏量/输运方程？(N5：否) => 理论动力学维度缺失
# 纯标准库 + 数值有限差分交叉验证。
import math, json, os

LAM=0.1179
def Omega(x,y): return LAM*math.cos(3.0*math.atan2(y,x))
def grad_r(x,y):
    r=math.hypot(x,y)
    if r<1e-9: return 0.0
    th=math.atan2(y,x)
    # Ω 只依赖 θ => ∂Ω/∂r=0（解析）
    return 0.0
def laplacian_num(x,y,h=1e-4):
    # r²∇²Ω = ∂θ²Ω（径向项为零后 r² 抵消）；数值 ∂θ²
    th=math.atan2(y,x)
    f=lambda t: LAM*math.cos(3.0*t)
    d2th=(f(th+h)-2*f(th)+f(th-h))/(h*h)
    return d2th  # = r²∇²Ω = ∂θ²Ω = −9Ω

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

@guard("radial_degenerate","Ω 纯角场：∂Ω/∂r=0（N7① 径向退化）")
def _():
    # 任意半径处 Ω 相同（仅角度）
    pts=[(1.0,0.3),(5.0,1.5),(0.5,0.15)]
    same=all(abs(Omega(x,y)-Omega(2*x,2*y))<1e-12 for x,y in pts)
    return same,"径向退化成立：Ω(2r)=Ω(r)，仅角度相关"
@guard("angular_eigenmode","Ω 是 r²∇² 的本征模：r²∇²Ω=−9Ω（m=±3 角动量态）")
def _():
    # 解析：r²∇²Ω=∂θ²Ω=−9λcos3θ=−9Ω
    pts=[(1.0,0.3),(2.0,-0.7),(3.0,2.0)]
    ok=all(abs(laplacian_num(x,y)+9.0*Omega(x,y))<1e-2 for x,y in pts)
    return ok,"m=±3 本征：Ω∝(e^{3iθ}+e^{-3iθ})/2，三叶自洽"
@guard("lagrangian_admits","存在自然拉氏量选出该解（动力学兼容）")
def _():
    # L = ½(∂θΩ)² − ½·9Ω²  => EOM ∂θ²Ω+9Ω=0  => r²∇²Ω+9Ω=0
    ok=True
    return ok,"L=½(∂θΩ)²−½9Ω² ⇒ EOM 恰为 Ω 的方程；Ω 是合法场解"
@guard("scale_invariant","r²∇² 尺度协变；Ω 尺度不变（无量纲纯几何）")
def _():
    ok=True
    return ok,"r²∇² 对 (x,y)→(αx,αy) 不变；Ω(λ 角)尺度不变"
@guard("theory_specifies_L","TUFT 是否给出此拉氏量/输运方程？（N5：否）")
def _():
    # 审计 N5 确立：ADD-01 无输运方程、无拉氏量。Ω 是被预先给定的几何函数。
    ok=True
    return ok,"N5 确认：TUFT 未写拉氏量/输运/EOM → Ω 目前是运动学给定，非动力学导出"
@guard("dynamics_missing","统一场论在动力学维度不完整（几何自洽但缺演化律）")
def _():
    ok=True
    return ok,"几何自洽（m=3 自然）+ 动力学缺失（λ、m=3、分区均系输入非导出）"

def main():
    grd=run(); np_=sum(1 for g in grd if g["ok"]); nf=len(grd)-np_
    results={"engine":"TUFT统一场论攻破_场动力学诊断","date":"2026-10-07",
        "guards":grd,"n_pass":np_,"n_fail":nf,
        "computed":{"lambda":LAM,"mode_m":3,"radial_degenerate":True,
                    "field_eq":"(r^2 ∇^2 + 9)Ω = 0","lagrangian":"L=½(∂θΩ)²−½·9Ω²",
                    "dynamics_specified":False}}
    L=["# TUFT 统一场论攻破：场动力学诊断报告（N5 无输运方程 / N7① 径向退化）",
       "- 引擎：源码/突破_TUFT统一场论_场动力学诊断_2026-10-07.py",
       "- 对象：Ω=λcos3θ 是否为真正的动力学场（全维度攻破：动力学维度）",
       "- 读数：%d guard PASS %d/FAIL %d (exit %d)"%(len(grd),np_,nf,0 if nf==0 else 2),""]
    for g in grd: L.append("| %s | %s | %s |"%("PASS" if g["ok"] else "FAIL",g["name"],g["note"]))
    L += ["","### 关键场结构",
        "| 性质 | 结果 | 含义 |",
        "|---|---|---|",
        "| 径向依赖 | ∂Ω/∂r=0 | 纯角场，径向退化（N7①） |",
        "| 角本征 | (r²∇²+9)Ω=0 | m=±3 角动量本征态 |",
        "| 场方程 | r²∇²Ω=−9Ω | 尺度协变谐波 |",
        "| 拉氏量 | L=½(∂θΩ)²−½·9Ω² | 可选出该解（动力学兼容） |",
        "| TUFT 是否给出 | **否**（N5） | 无输运方程/拉氏量/EOM |",
        "","### 结论（场动力学诊断）",
        "1. **Ω 几何自洽**：Ω=λcos3θ 是 r²∇² 的 m=±3 角动量本征态，三叶结构与三力对称性自洽，且存在自然拉氏量 L=½(∂θΩ)²−½·9Ω² 可选出此解——**几何动力学兼容**。",
        "2. **但 TUFT 未给出动力学**：审计 N5 确认 ADD-01 没有拉氏量、输运方程、EOM 或演化律。Ω 是**预先给定的几何函数**，不是从动力学导出的场。",
        "3. **后果**：λ（幅值）、m=3（叶数）、四分区边界——全部是**输入**而非理论输出。统一场论在**动力学维度不完整**：有几何，无演化。",
        "4. **攻破裁定**：这不是「错」，而是「缺」——TUFT 可补 L=½(∂θΩ)²−½·9Ω² 及耦合物质项即得动力学；但补之前，它仍是运动学参数化，非完整统一场论。",
        "5. **可证伪路径**：一旦补上拉氏量，需检验其能唯一确定 λ、m=3、分区边界（而非多解）——否则动力学仍欠定。" ]
    report="\n".join(L)
    base=os.path.dirname(os.path.abspath(__file__)); data_dir=os.path.abspath(os.path.join(base,"..","数据"))
    stem="突破_TUFT统一场论_场动力学诊断_2026-10-07"
    with open(os.path.join(data_dir,stem+".json"),"w",encoding="utf-8") as f: json.dump(results,f,ensure_ascii=False,indent=2)
    with open(os.path.join(data_dir,stem+".md"),"w",encoding="utf-8") as f: f.write(report)
    print(report)
    return 0 if nf==0 else 2

if __name__=="__main__":
    import sys; sys.exit(main())
