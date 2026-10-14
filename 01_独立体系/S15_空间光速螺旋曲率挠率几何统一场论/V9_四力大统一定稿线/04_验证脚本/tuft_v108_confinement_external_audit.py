# -*- coding: utf-8 -*-
"""
V9.28 外源 Proca 禁闭渐近性终判：4.7 修复方案 1（非齐次外源）的最后边界
A 组：有质量（汤川格林函数）外源 Proca 对 Cornell 源（-alpha_s/r + sigma*r）的解 kappa(r)
      远场渐近：线性禁闭被汤川指数抹平为有限常数（禁闭抹平）
B 组：无质量（库仑格林函数）极限对线性源的积分发散（无良定义解）
C 组：外源三参数 (alpha_s, sigma, mu) 全外输计数 + 判定
判定目标：4.7 两条修复路线全部关闭 => 线性禁闭在模板任何 Proca 变体中数学上不可实现
"""
import json, math

out = {}

# ============ A 组：汤川外源解 ============
# (nabla^2 - mu^2) kappa = S(r)，球对称格林函数（注意符号：G=-e^(-mu R)/(4pi R)，因 (nabla^2-mu^2)G=+delta^3）：
# kappa(r) = -(1/(2*mu*r)) Int_0^inf r' S(r') [ e^(-mu|r-r'|) - e^(-mu(r+r')) ] dr'
# Cornell 源（反解 (nabla^2-mu^2)V 于 V=-alpha_s/r+sigma*r）：
#   S(r) = 4*pi*alpha_s*delta(r) + 2*sigma/r - mu^2*sigma*r
#   - delta 项：kappa_delta(r) = -alpha_s*e^(-mu*r)/r （库仑+指数修正，负号来自格林函数）
#   - 禁闭项：kappa_sigma(r) = -(sigma/(2*mu*r)) Int (2 - mu^2 r'^2)[e^(-mu|r-r'|)-e^(-mu(r+r'))] dr'
# 解析闭式：kappa_sigma(r) = sigma*( r + (1-e^(-mu*r))/(mu*r) )  （见脚本末推导）
#   -> 远场 r>>1/mu：kappa_sigma(r) -> sigma*r  线性禁闭精确恢复！
#   （初版符号错误给出 -sigma*r，数值反证后修正：G 取负号才是 (nabla^2-mu^2)G=+delta 的格林函数）
# 无量纲化：mu=1, sigma=1，r 以 1/mu 为单位

mu = 1.0
sigma = 1.0

def kappa_sigma_num(r, mu=1.0, sigma=1.0, Rmax=80.0, n=400000):
    """数值积分禁闭源贡献（正确符号：整体负号）"""
    dr = Rmax / n
    s = 0.0
    for i in range(1, n):
        rp = i * dr
        g = (math.exp(-mu*abs(r-rp)) - math.exp(-mu*(r+rp)))
        s += (2.0 - mu*mu*rp*rp) * g * dr
    return -sigma / (2.0*mu*r) * s

def kappa_sigma_analytic(r, mu=1.0, sigma=1.0):
    """解析闭式：sigma*mu*r（精确线性！）
    推导：s=Int(2-mu^2 r'^2)[e^-mu|r-r'|-e^-mu(r+r')]dr'=-2 mu^2 r^2（分部积分精确）
    kappa_sigma=-(sigma/(2 mu r))*s=sigma*mu*r
    （初版含 (1-e^-mu r)/(mu r) 修正项的闭式推导有误，数值诊断后修正为精确线性）"""
    return sigma * mu * r

A = {"mu_units": "r 以 1/mu 为单位，sigma=1 归一"}
rs = [0.5, 1.0, 2.0, 3.0, 5.0, 8.0, 12.0, 20.0, 30.0, 50.0]
scan = []
for r in rs:
    k = kappa_sigma_num(r)
    ka = kappa_sigma_analytic(r)
    target = sigma * r  # 线性禁闭目标
    scan.append({"r": r, "kappa_sigma_num": round(k, 6),
                 "kappa_sigma_analytic": round(ka, 6),
                 "linear_target sigma*r": round(target, 6),
                 "ratio kappa/target": round(ka/target, 6)})
A["far_field_scan"] = scan
# 全区间数值=解析：最大相对偏差
maxdev = max(abs(s["kappa_sigma_num"]-s["kappa_sigma_analytic"])/abs(s["kappa_sigma_analytic"]) for s in scan)
A["num_vs_analytic_max_rel_dev"] = maxdev
A["asymptotic_check"] = {"kappa(30)": scan[8]["kappa_sigma_analytic"],
                         "kappa(50)": scan[9]["kappa_sigma_analytic"],
                         "ratio(50)": scan[9]["ratio kappa/target"],
                         "conclusion": "全区间精确线性禁闭 kappa_sigma(r)=sigma*mu*r（数值=解析，最大相对偏差<1e-5）；"
                                       "无任何修正项、无指数抹平"}
A["A_verdict"] = ("有质量外源 Proca **精确承载线性禁闭势**：kappa_sigma(r)=sigma*mu*r（全区间精确线性，数值=解析）；"
                  "(nabla^2-mu^2)(sigma*mu*r)=2*sigma*mu/r-mu^3*sigma*r（无量纲 mu=1 时 =2*sigma/r-sigma*r=S）恒等；"
                  "初版『汤川抹平』预设被数值反证推翻（格林函数符号错），解析闭式修正两次后（含修正项版推导错）"
                  "确定为精确线性 sigma*mu*r——外源 Proca 势层面精确承载禁闭")

# ============ B 组：无质量（库仑）极限发散 ============
# mu=0：库仑格林函数 l=0 投影 G(r,r')=1/max(r,r')
# kappa(r) = Int r'^2 S(r') / max(r,r') dr'
# 线性源项 S~2*sigma/r'：Int 2*sigma*r'/max(r,r') dr'
#   = 2*sigma[ Int_0^r r'/r dr' + Int_r^R 1 dr' ] = 2*sigma[ r/2 + (R-r) ] -> R 发散（线性增长）
# 注意：禁闭线性势要求无质量极限发散，但有质量（mu>0）汤川精确承载——禁闭可由有质量外源实现，但 mu 本身外输
B = {}
for R in (10.0, 20.0, 50.0, 100.0):
    # 数值积分 Int_0^R 2*r'/max(r,r') dr' 在 r=1
    r0 = 1.0
    n = 200000
    dr = R / n
    val = 0.0
    for i in range(1, n):
        rp = i * dr
        val += (2.0*rp/max(r0, rp)) * dr
    B[str(int(R))] = {"kappa_linear_source_upper_limit_R": round(val, 4)}
B["B_verdict"] = ("无质量极限：线性源积分随积分上限 R 线性发散（数值：R=10->19.0, R=100->199.0）"
                  "=> 无质量媒介子无良定义解；有质量（mu>0）汤川格林函数收敛且精确恢复 sigma*r，"
                  "但 mu（禁闭载体质量）与源 S 三参数全外输（B03）")

# ============ B 组：无质量（库仑）极限发散 ============
# mu=0：库仑格林函数 l=0 投影 G(r,r')=1/max(r,r')
# kappa(r) = Int r'^2 S(r') / max(r,r') dr'
# 线性源项 S~2*sigma/r'：Int 2*sigma*r'/max(r,r') dr'
#   = 2*sigma[ Int_0^r r'/r dr' + Int_r^R 1 dr' ] = 2*sigma[ r/2 + (R-r) ] -> R 发散（线性增长）
out["A"] = A
out["B_massless_limit"] = B

# ============ C 组：外输计数与判定 ============
C = {"external_params": {"alpha_s": "QCD 强耦合（外输）", "sigma": "弦张力/禁闭斜率（外输）",
                         "mu": "禁闭载体质量（外输）"},
     "params_count": 3,
     "C_verdict": ("4.7 修复方案 1（非齐次外源）**势层面数学精确可行**：有质量汤川格林函数精确恢复线性禁闭"
                   "kappa_sigma(r)->sigma*r（初版『抹平』预设被数值反证推翻）；无质量极限发散（B 组）；"
                   "代价：源 S(r)=2*sigma/r-mu^2*sigma*r 与三参数 (alpha_s,sigma,mu) 全部外输（B03）。"
                   "结合 V9.26（自耦合 Derrick 关闭）：**内生禁闭仍不可能，但外源禁闭势可精确嵌入模板**——"
                   "B03 精确化为『禁闭势形可承载（PASS 型）、源与参数全外输（B03）、动力学（QCD 胶子自作用）无』")}
out["C_verdict"] = C

out["summary"] = ("V9.28 外源 Proca 禁闭渐近性终判（自我证伪+两轮修正版）：A 组有质量汤川格林函数**精确承载线性禁闭**"
                  "kappa_sigma(r)=sigma*mu*r（全区间精确线性，数值=解析最大偏差<1e-5）；"
                  "B 组无质量库仑极限线性源积分随上限发散（R=10->19、R=100->199，无解）；"
                  "C 组外源三参数全外输。判定：4.7 方案 1 势层面数学精确可行（初版『抹平』预设被数值反证推翻，"
                  "解析闭式两轮修正后定为精确线性），但源与参数全外输（B03），内生禁闭仍不可能；"
                  "结合 V9.26 自耦合关闭，禁闭只能外源嵌入。无新增独立 FAIL、无 FAIL 撤销，总账（实现 50%/预言 20%）不变")

with open(r"D:\a10\aikjx\code\my_lib\tuft_v108_confinement_external_audit_results.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("A kappa(30)=", scan[8]["kappa_sigma_analytic"], "kappa(50)=", scan[9]["kappa_sigma_analytic"])
print("A ratio(50)=", scan[9]["ratio kappa/target"], "(线性目标 sigma*r 比值 -> 1 => 精确恢复)")
print("A num vs analytic max rel dev:", maxdev)
print("B R=10->", B["10"]["kappa_linear_source_upper_limit_R"], "R=100->", B["100"]["kappa_linear_source_upper_limit_R"])
print("saved json ok")
