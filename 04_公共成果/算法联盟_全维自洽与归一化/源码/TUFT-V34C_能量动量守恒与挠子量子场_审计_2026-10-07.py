# -*- coding: utf-8 -*-
import sys, json, math, random
from decimal import Decimal, getcontext
from itertools import permutations
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
getcontext().prec = 80

BASE = __import__("pathlib").Path(__file__).resolve().parents[1] / "数据"
RESULTS = []
def rec(key, status, msg, value=None):
    RESULTS.append({"key": key, "status": status, "msg": msg, "value": value})

# G01 守恒律右端恒等零: S^{μρν}(全反对称)·R_{μρ}(对称) 对任意ν恒为零
dim = 4
rnd = random.Random(20261007)
S = [[[0.0]*dim for _ in range(dim)] for _ in range(dim)]
indep = [(0,1,2),(0,1,3),(0,2,3),(1,2,3)]
vals = [rnd.uniform(-2,2) for _ in range(4)]
def sign(p):
    s=1; a=list(p)
    for i in range(len(a)):
        for j in range(i+1,len(a)):
            if a[i]>a[j]: s=-s
    return s
for (i,j,k),v in zip(indep, vals):
    for p in permutations((i,j,k)):
        S[p[0]][p[1]][p[2]] = v*sign(p)
R = [[0.0]*dim for _ in range(dim)]
for i in range(dim):
    for j in range(i,dim):
        v=rnd.uniform(-3,3); R[i][j]=R[j][i]=v
sym_err=0.0
for i in range(dim):
    for j in range(dim):
        for k in range(dim):
            if abs(S[i][j][k]+S[j][i][k])>1e-12: sym_err+=1
for i in range(dim):
    for j in range(dim):
        if abs(R[i][j]-R[j][i])>1e-12: sym_err+=1
maxC=0.0
for nu in range(dim):
    c=0.0
    for mu in range(dim):
        for rho in range(dim):
            c+=S[mu][rho][nu]*R[mu][rho]
    maxC=max(maxC,abs(c))
rec("G01_conservation_zero","FAIL",
    "S[mu,rho,nu](全反对称)·R[mu,rho](对称) 对任意nu恒为零: max|C_nu|={:.3e}, 对称校验误差={:.3e}. 因此§I'自旋-引力交换源项'恒等零, 守恒律退化为普通GR, 挠率并未真正耦合进守恒律".format(maxC,sym_err),
    {"maxC":maxC,"sym_err":sym_err})
# G02 挠率场能动张量符号/项错误 (由 L_τ 标准规范能动张量反推)
# L_τ/√-g = -α/2 (∂τ)^2 - V(τ), V(τ) = -α/2 τ^2 + ητ
# 正确 T^{μν}= α(∂^μτ∂^ντ - 1/2 g^{μν}(∂τ)^2) - g^{μν}V = α(...) + 1/2 α g^{μν}τ^2 - g^{μν}ητ
alpha=1.0; eta=0.1; tau=0.5; dtau=0.3
gUU=[-1.0,1.0,1.0,1.0]
T_corr_00 = alpha*(dtau*dtau-0.5*gUU[0]*dtau*dtau) + 0.5*alpha*gUU[0]*tau*tau - gUU[0]*eta*tau
T_claim_00 = alpha*(dtau*dtau-0.5*gUU[0]*dtau*dtau) - 0.5*gUU[0]*alpha*tau*tau
diff = T_corr_00 - T_claim_00
rec("G02_torsion_stress","FAIL" if abs(diff)>1e-12 else "PASS",
    "挠率场能动张量: 正确式含 +1/2 α g^μν τ^2 - g^μν ητ; 来稿漏 -g^μν ητ 项, 且 τ^2 项符号反(应为+, 来稿-). 00分量差={:.4f}".format(diff),
    {"T_corr_00":T_corr_00,"T_claim_00":T_claim_00,"diff":diff})

# G03 挠率场运动方程源项 + 与 §3.1 自身约定冲突
c = Decimal("299792458"); R = Decimal("1.0"); a = Decimal("1.0")
rhs_claim = R/(Decimal("2")*a*c)
rhs_correct = -R/(Decimal("2")*a*c**3)
lP = Decimal("1.616255e-35"); m2 = Decimal("1")/lP**2
rec("G03_field_eq_source","FAIL",
    "挠率场方程源项: 总拉氏量变分得 RHS=-R/(2α c^3); 来稿写 +R/(2α c). SI下量级差 c^2={:.3e} 且符号反; 自然单位(c=1)下仅符号反(正确 -R/2α, 来稿 +R/2α)".format(float(c**2)),
    {"rhs_claim":str(rhs_claim),"rhs_correct":str(rhs_correct)})
rec("G03_internal_mass","FAIL",
    "场方程裸 -τ 缺质量标度: §3.1 声明 m_τ^2=1(普朗克标度)=>SI 应 -m_τ^2 τ, m_τ^2={:.3e} m^-2, 与 §II 裸 1 冲突".format(float(m2)),
    {"m_tau_sq_Planck":str(m2)})
# G04 代码 delta_g(alpha) 恒等于 alpha + 与 §3.2 公式矛盾
c = Decimal("299792458"); G = Decimal("6.67430e-11"); hbar = Decimal("1.054571817e-34")
m_e = Decimal("9.1093837015e-31"); lambda_e = hbar/(m_e*c)
def delta_g(alpha):
    tau_e = alpha*hbar/(m_e*c*lambda_e**2)
    return tau_e*hbar/(m_e*c)
a0 = Decimal("1e-39"); dg = delta_g(a0); resid = dg - a0
rec("G04_delta_g_identity","FAIL",
    "§5 代码 delta_g(alpha) 机器复算恒等于 alpha(残差={:.2e}); 且 §3.2 文本称 a_TUFT=α/(8π), 二者相差 8π 倍 => 代码与正文不自洽, '用g-2拟合α'只是把α重命名为Δg".format(float(resid)),
    {"alpha":str(a0),"delta_g":str(dg),"resid":str(resid)})

# G05 L_τ 量纲不自洽(SI)
# 动能项 [α][τ]^2 L^-2 ; 质量项 α/2 τ^2 = [α][τ]^2 ; 二者恒差 L^-2, 与[τ]选取无关 => 拉氏量量纲不齐
rec("G05_lagrangian_dimensional","FAIL",
    "L_τ=-α/2(∂τ)^2+α/2 τ^2-ητ 在SI下动能项与τ^2项量纲恒差L^-2(与[τ]选取无关)=>拉氏量量纲不齐; 需[τ]自带长度标度或η/α含标度",
    {"kinetic_dim":"[alpha][tau]^2 L^-2","mass_dim":"[alpha][tau]^2"})

# G06 实验窗口关闭 (g-2 / EDM)
pi = Decimal("3.141592653589793")
alpha_fine = Decimal("1")/Decimal("137.035999084")
a_TUFT_text = alpha_fine/(Decimal("8")*pi)
a_e_exp = Decimal("0.00115965218128")
dev_text = (a_TUFT_text - a_e_exp)/a_e_exp
a_TUFT_code = alpha_fine
dev_code = (a_TUFT_code - a_e_exp)/a_e_exp
rec("G06_g2_window","FAIL",
    "g-2 窗口已关: §3.2 口径 a_TUFT=α/(8π)={:.4e} vs 实验 {:.4e}, 偏差 {:.2%}; §5 代码口径 Δg=α={:.4e}, 偏差 {:.2%}. 二者互相矛盾(差8π)且皆远离实验".format(float(a_TUFT_text),float(a_e_exp),float(dev_text),float(a_TUFT_code),float(dev_code)),
    {"a_TUFT_text":str(a_TUFT_text),"a_TUFT_code":str(a_TUFT_code),"a_e_exp":str(a_e_exp),"dev_text":str(dev_text),"dev_code":str(dev_code)})
rec("G06_EDM_window","FAIL",
    "EDM 窗口已关(openuft M02): TUFT EDM 预言超 ACME2018 上限 1.28e16 倍; 该文档耦合 L_int∝ψ̄γ5γ^μψ·∂_μτ 为 P-奇/T-奇(可生EDM)但未给任何幅度, 且 TUFT 螺旋对称论证 d_e=0 => 预言不可证伪且已被实验排除",
    {"over_ACME":"1.28e16"})
# G07 标量引力波极化: 耦合ξ未由作用量变分固定
rec("G07_scalar_GW","INFO",
    "h_det=h_+F_++h_×F_×+h_τF_τ 的标量极化 F_τ 需要挠率-度规耦合ξ, 但总拉氏量未给出ξ的变分来源 => ξ 是未声明的外部输入; 现有GW/PTA上限要求ξ≪1或标量不与检验质量耦合, 非TUFT专属干净预言",
    {})
# G08 β函数跑动 c: exotic + Ω5 冲突
rec("G08_beta_running_c","FAIL",
    "β_c=μ dc/dμ 令光速c跑动, 是exotic假设; 每加一个跑动耦合=+1自由函数撞Ω5(自由常数≤1); β_G公式量纲不齐([β_c/c]=T^-1 与[G]不匹配); '非高斯紫外不动点'是猜想非结论",
    {})

# 汇总 + 写产物
from collections import Counter
cnt = Counter(r["status"] for r in RESULTS)
self_check = (cnt["PASS"]+cnt["FAIL"]+cnt["INFO"]+cnt["BOUNDARY"]) == len(RESULTS) and len(RESULTS)>=6
report = {
  "title":"TUFT V3.4C 能量动量守恒+挠子量子场 全维审计",
  "date":"2026-10-07",
  "entries":len(RESULTS),
  "counts":dict(cnt),
  "self_check_pass":self_check,
  "results":RESULTS,
}
BASE.mkdir(parents=True, exist_ok=True)
out_json = BASE / "TUFT-V34C_能量动量守恒与挠子量子场_审计_2026-10-07.json"
out_md = BASE / "TUFT-V34C_能量动量守恒与挠子量子场_审计_2026-10-07.md"
out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
lines = ["# TUFT V3.4C 能量动量守恒 + 挠子量子场 审计", "",
         "条目数: {}  计数: {}".format(len(RESULTS), dict(cnt)),
         "自检: {}".format("通过" if self_check else "失败"), ""]
for r in RESULTS:
    lines.append("- [{}] {} : {}".format(r["status"], r["key"], r["msg"].replace("](", "] (")))
out_md.write_text("\n".join(lines), encoding="utf-8")
print("WROTE", out_json)
print("条目", len(RESULTS), "计数", dict(cnt), "自检", self_check)
sys.exit(0 if self_check else 1)
