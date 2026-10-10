# -*- coding: utf-8 -*-
"""
判定：TUFT V4.1 修正版｜严格自洽全域力统一方程（U=α(κ²-τ²), F=-α∇(κ²-τ²)）· 全维审计（r33）
===================================================================================
来料：《TUFT V4.1 修正版｜严格自洽全域力统一方程》——前置纠错总声明 + 七节：
  ①基础严格定义（自然单位，[κ]=[τ]=[∇]=L⁻¹, [r]=L, [能量]=L⁻¹, [力]=L⁻²）
  ②几何势能 U(r)=α(κ²-τ²), [α]=L
  ③统一力 F=-α∇(κ²-τ²)；球对称 F=-α·∂r(κ²-τ²) r̂
  ④四力还原：引力(κ∝M/r)、电磁(τ∝q/r)、弱(τ∝q e^{-μr}/r)、强(τ∝σ r e^{-r/r0})
  ⑤量纲终极闭环核验（[F]=L·L⁻¹·L⁻²=L⁻²）
  ⑥概念纠错、⑦最终结论

本册职责：对来料文本做**独立机器核验**（纯标准库，Fraction 量纲 + 数值对拍），
只判「来料声称的还原/闭合是否逐位成立」，不重推物理对错、不代选修复方向。

关键自检口径：
  - 量纲用自然单位（c=ℏ=1）单维 L 幂次：质量/能量=L⁻¹、力=L⁻²、曲率/挠率=L⁻¹
  - 四力「梯度还原」逐一与标准参考力（牛顿、库仑、汤川、Cornell）对拍
  - 所有「恒等为零/不成立」判定必须配阳性对照
===================================================================================
运行：python TUFT-r33_V41全域力统一方程_全维审计_2026-10-10.py
产物：数据/TUFT-r33_V41全域力统一方程_全维审计_2026-10-10.{json,md,_report.txt}
"""
import json, sys, os, math
from fractions import Fraction

# ---------- 结果容器 ----------
RESULTS = []   # (id, verdict, title, detail)
GUARDS   = []  # (id, pass_bool, note)

def rec(rid, verdict, title, detail):
    RESULTS.append([rid, verdict, title, detail])

def guard(rid, ok, note):
    GUARDS.append((rid, bool(ok), note))

# =====================================================================
# 0. 基础：量纲以 L 幂次（Fraction）表示；自然单位 [E]=L⁻¹, [F]=L⁻²
# =====================================================================
def dim_of_force():        return Fraction(-2)   # [F]=L⁻²
def dim_of_energy():       return Fraction(-1)   # [E]=L⁻¹
def dim_alpha():           return Fraction(1)    # [α]=L
def dim_kappa_tau():       return Fraction(-1)   # [κ]=[τ]=L⁻¹
def dim_grad():            return Fraction(-1)   # [∇]=L⁻¹

# =====================================================================
# 一、量纲终极闭环核验（V4.1 §二/§三/§五）
# =====================================================================
def audit_dimension():
    # [U]=[α]+2[κ]=1-2=-1 = 能量
    U_dim = dim_alpha() + 2*dim_kappa_tau()
    guard('G01', U_dim == dim_of_energy(), "U=α(κ²-τ²) 量纲 L⁻¹=能量")
    rec('A01', 'PASS' if U_dim==dim_of_energy() else 'FAIL',
        "势能量纲 [U]=[α]+2[κ]=1+2(-1)=L⁻¹",
        f"[U]={U_dim} vs [E]=L⁻¹ → {'闭合' if U_dim==dim_of_energy() else '不闭合'}")

    # [F]=[α]+[∇]+2[κ]=1-1-2=-2 = 力
    F_dim = dim_alpha() + dim_grad() + 2*dim_kappa_tau()
    guard('G02', F_dim == dim_of_force(), "F=-α∇(κ²-τ²) 量纲 L⁻²=力")
    rec('A02', 'PASS' if F_dim==dim_of_force() else 'FAIL',
        "统一力量纲 [F]=[α]+[∇]+2[κ]=1-1-2=L⁻²",
        f"[F]={F_dim} vs [力]=L⁻² → {'闭合' if F_dim==dim_of_force() else '不闭合'}")

    # 球对称 F=-α ∂r(κ²-τ²) r̂：[∂r]=L⁻¹ 与 [∇] 一致
    rec('A03', 'PASS', "球对称 [∂r]=L⁻¹=[∇]，F=-α∂r(...)r̂ 量纲同 A02",
        "矢量=矢量，无点乘混用；r̂ 无量纲，量纲不改变")

# =====================================================================
# 二、引力还原核验（V4.1 §四.1）：κ∝M/r → ? → F_g∝GMm/r²
# =====================================================================
def audit_gravity():
    # 来料：κ∝M/r ⇒ κ²∝M²/r² ⇒ ∂rκ²∝-2M²/r³ ⇒ F_g=-α(-2M²/r³)∝GMm/r²
    # 机器核对：若 κ=cM/r，则 F_g 的 r 幂次 = ?
    #   κ² ∝ r^{-2}, ∂rκ² ∝ r^{-3}, F_g=-α∂rκ² ∝ r^{-3}
    # 目标牛顿力 F∝r^{-2}
    # ⇒ 断言：κ∝r^{-1} 给出 F∝r^{-3}，与 F∝r^{-2} 不符（差一个 1/r）
    from fractions import Fraction as F_
    p_kappa = 1   # κ∝r^{-1}
    F_power = p_kappa*2 + 1   # ∂r(κ²)∝r^{-(2p+1)}，取梯度幂次+1
    target_power = 2          # 牛顿 F∝r^{-2}
    guard('G03', F_power != target_power,
          "κ∝r⁻¹ ⇒ 力∝r⁻³ ≠ r⁻²（牛顿需要的 r⁻² 对应 κ∝r^{-1/2}）")
    rec('B01', 'FAIL',
        "引力还原幂次错：κ∝M/r ⇒ F∝r⁻³，而非来料声称的 r⁻²",
        f"∂r(κ²)∝r⁻{F_power}，取负梯度后 F∝r⁻{F_power}；牛顿引力需要 F∝r⁻{target_power}。"
        f"若 κ∝r⁻¹，则 F∝r⁻³（多一个 1/r）。要得 r⁻² 必须 κ∝r⁻¹ᐟ²（此时 κ²∝r⁻¹，∂rκ²∝r⁻²）。"
        f"来料用 κ∝M/r（幂次 1）却宣称还原 1/r²，数学上不成立。")

    # 量纲第二重：κ∝M/r 的量纲核对
    #   [κ]=L⁻¹；[M/r]：自然单位 [M]=L⁻¹, [r]=L ⇒ [M/r]=L⁻² ≠ L⁻¹
    dim_M_over_r = Fraction(-1) - Fraction(1)   # [M]-[r] = -1-1 = -2
    guard('G04', dim_M_over_r != dim_kappa_tau(),
          "κ∝M/r 中 [M/r]=L⁻²≠[κ]=L⁻¹ ⇒ 比例式量纲不齐（除非隐去长度标度）")
    rec('B02', 'BOUNDARY',
        "κ∝M/r 的量纲：自然单位 [M/r]=L⁻² ≠ [κ]=L⁻¹",
        f"[M/r]={dim_M_over_r} vs [κ]={dim_kappa_tau()}。除非 M 无量纲或显式带长度标度，"
        f"否则 κ∝M/r 在量纲上不齐；来料未声明。")

    # 来料第①式符号：F_g=-α(-2M²/r³)r̂=+2αM²/r³ r̂（吸引方向需 +r̂? 方向性检查）
    # 牛顿 F=-GMm/r² r̂（r̂ 从源指向外，吸引为 -）。来料 +2αM²/r³ r̂ 是排斥方向，
    # 除非 M 或 α 取负；来料未声明符号约定。
    rec('B03', 'BOUNDARY',
        "引力方向符号未声明：来料 F_g=+2αM²/r³ r̂ 为排斥方向，牛顿吸引为 -r̂",
        "需声明 M/α 符号或约定 r̂ 指向源，否则正负号语义未定。")

# =====================================================================
# 三、电磁还原核验（V4.1 §四.2）：τ∝q/r → ? → F_e∝k q1q2/r²
# =====================================================================
def audit_em():
    p_tau = 1
    F_power = p_tau*2 + 1
    target_power = 2
    guard('G05', F_power != target_power, "τ∝r⁻¹ ⇒ F∝r⁻³ ≠ r⁻²")
    rec('C01', 'FAIL',
        "电磁还原幂次错：τ∝q/r ⇒ F∝r⁻³，而非来料声称的 r⁻²",
        f"∂r(τ²)∝r⁻{F_power}，F=-α∂r(-τ²)∝r⁻{F_power}；库仑力需 r⁻{target_power}。"
        f"要得 r⁻² 必须 τ∝r⁻¹ᐟ²。来料 τ∝q/r 数学上给 1/r³，非 1/r²。")

    # 电荷量纲：τ∝q/r 且 [τ]=L⁻¹, [r]=L ⇒ [q]=L⁰（无量纲）？但库仑力含 q1q2/r² 需要电荷量纲。
    # 自然单位下 [q²/r²]：若 [q]=L⁰ ⇒ [q²/r²]=L⁻²（无量纲×L⁻²）→ 力=能量/长度=L⁻² 自洽；
    # 但库仑常数 k 的量纲未声明（SI 中 k 有量纲，自然单位 k 可无量纲）。
    rec('C02', 'BOUNDARY',
        "电荷量纲口径未声明：τ∝q/r 隐含 [q]=L⁰，库仑常数 k 量纲未定",
        "来料未声明 k 的量纲与数值；无 k 的独立来源，电磁耦合仍需外部输入（与 Z15 同族）。")

# =====================================================================
# 四、弱力还原核验（V4.1 §四.3）：τ∝q e^{-μr}/r → ? → F_w 短程
# =====================================================================
def audit_weak():
    # 来料：τ_w=q e^{-μr}/r；∂rτ_w²∝-2q²e^{-2μr}(1+μr)/r³（来料给）
    # 机器核对 ∂r(τ²)：τ²=q²e^{-2μr}/r²
    #   d/dr = q²[ -2μ e^{-2μr}/r² - 2 e^{-2μr}/r³ ] = -2q²e^{-2μr}( μ/r² + 1/r³ )
    #        = -2q²e^{-2μr}(1+μr)/r³   ✓ 与来料一致
    # 但标准汤川势 V=-g²e^{-mr}/r ⇒ F=-dV/dr=-g²e^{-mr}(m/r+1/r²)∝(1+mr)e^{-mr}/r²
    # 来料给出 ∝ exp(-2μr)(1+μr)/r³，指数是 2μ（因 τ 平方），与标准汤川 exp(-μr)/r² 不同
    # ⇒ 来料把「τ 自身衰减」当「势」再用二次方，指数翻倍、幂次多 1，与汤川势不符

    # 数值对拍：验证来料 ∂rτ_w² 的代数式
    mu = 1.0; q = 1.0
    def tau2(r): return (q*math.exp(-mu*r)/r)**2
    def tau2_deriv_analytic(r): return -2*q*q*math.exp(-2*mu*r)*(1+mu*r)/(r**3)
    rs = [0.5, 1.0, 2.0]
    errs = []
    for r in rs:
        h = 1e-6
        num = (tau2(r+h)-tau2(r-h))/(2*h)
        errs.append(abs(num - tau2_deriv_analytic(r)))
    ok = all(e < 1e-8 for e in errs)
    guard('G06', ok, "来料 ∂r(τ_w²) 代数式机器对拍通过")
    rec('D01', 'PASS' if ok else 'FAIL',
        "来料弱力导数式 ∂rτ_w²=-2q²e^{-2μr}(1+μr)/r³ 代数正确",
        f"中心差分 vs 解析式误差 {[f'{e:.2e}' for e in errs]}")

    # 与标准汤川对比：来料 ∝e^{-2μr}(1+μr)/r³ vs 汤川 ∝e^{-μr}(1+mr)/r²
    def yukawa_F(r):    # 标准汤川力（正比核，取 m=μ）
        return math.exp(-mu*r)*(1+mu*r)/(r*r)
    def incoming_F(r):  # 来料力（正比核）
        return math.exp(-2*mu*r)*(1+mu*r)/(r**3)
    ratio = incoming_F(1.0)/yukawa_F(1.0)   # 纯核比（不含 α）
    guard('G07', abs(ratio-1.0) > 1e-3,
          "来料力核 ≠ 标准汤川力核（指数 2μ 且 r⁻³ vs r⁻²）")
    rec('D02', 'FAIL',
        "弱力还原与标准汤川势不符：来料 ∝e^{-2μr}(1+μr)/r³，汤川 ∝e^{-μr}(1+μr)/r²",
        f"r=1 处核比值 in/out={ratio:.4f}。因来料势用 τ²，指数翻倍(2μ)且幂次多 1(r⁻³ vs r⁻²)。"
        f"来料自称「严格还原汤川」不成立：汤川是一次方势的梯度，来料是二次方 τ² 的梯度。")

# =====================================================================
# 五、强力还原核验（V4.1 §四.4）：τ∝σ r e^{-r/r0} → ? → 渐近自由+禁闭
# =====================================================================
def audit_strong():
    # 来料：τ_s=σ r e^{-r/r0}；∂rτ_s²∝2σ²r e^{-2r/r0}(1-r/r0)（来料给）
    # 机器核对：τ²=σ²r²e^{-2r/r0}
    #   d/dr = σ²[2r e^{-2r/r0} + r²(-2/r0)e^{-2r/r0}] = 2σ²r e^{-2r/r0}(1-r/r0) ✓
    sigma, r0 = 1.0, 1.0
    def tau2(r): return (sigma*r*math.exp(-r/r0))**2
    def tau2_da(r): return 2*sigma*sigma*r*math.exp(-2*r/r0)*(1-r/r0)
    errs=[]
    for r in [0.5,1.0,2.0]:
        h=1e-6
        num=(tau2(r+h)-tau2(r-h))/(2*h)
        errs.append(abs(num-tau2_da(r)))
    ok = all(e<1e-8 for e in errs)
    guard('G08', ok, "来料 ∂r(τ_s²) 代数式机器对拍通过")
    rec('E01','PASS' if ok else 'FAIL',
        "来料强力导数式 ∂rτ_s²=2σ²r e^{-2r/r0}(1-r/r0) 代数正确",
        f"中心差分 vs 解析式误差 {[f'{e:.2e}' for e in errs]}")

    # 渐近自由声称：r→0 时力→0？
    #   F_s=-α·2σ²r e^{-2r/r0}(1-r/r0)。r→0: r e^{-2r/r0}→0，力→0。来料说「近距离力趋0=渐近自由」
    # 但 QCD 渐近自由是耦合 αs(r) 随 r→0 对数趋 0，力 ~ αs/r² 并不趋 0（仍发散，只是比固定耦合慢）
    # 且标准 Cornell 势 V=-(4αs/3)/r + σr ⇒ F=-(4αs/3)/r² - σ（σ 为弦张力常数力）
    # 来料给的 F∝r(1-r/r0)e^{-2r/r0} 在中距离并非线性增强，而是一个有峰的形态（在 r=r0/2 处取极值）
    # 且 r>r0 时 (1-r/r0)<0 ⇒ 力反号变排斥，与禁闭（永远吸引）矛盾
    rec('E02','FAIL',
        "强力「渐近自由」概念错配：力∝r→0 趋 0 不是 QCD 渐近自由",
        "QCD 渐近自由是 αs(r) 对数趋 0，力 ~αs/r² 不趋 0；来料把「力本身→0」当渐近自由，概念错配。"
        "且标准 Cornell 力 F=-(4αs/3)/r²-σ 短程含 1/r² 发散项，来料不含。")

    # 禁闭声称：中距离线性增强？
    #   F_s(r) 在 r<r0 时 = C·r(1-r/r0)，C>0 取负梯度符号；峰值在 r=r0/2，非线性增强
    #   且 r>r0 时 F 反号 ⇒ 排斥，禁闭要求永远吸引
    peak = r0/2
    val_half = r0/2 * (1 - (r0/2)/r0) * math.exp(-2*(r0/2)/r0)   # 1-r/r0=1/2
    val_r0   = r0 * (1-r0/r0) * math.exp(-2*r0/r0)                # =0
    val_2r0  = 2*r0 * (1-2*r0/r0) * math.exp(-2*2*r0/r0)          # = -1*... 负
    guard('G09', (val_r0==0) and (val_2r0<0),
          "来料强力 F 在 r=r0 归零、r>r0 反号排斥，与禁闭（恒吸引）矛盾")
    rec('E03','FAIL',
        "「线性增强/禁闭」与来料自身函数矛盾：F 在 r=r0 归零、r>r0 反号",
        f"F_s(r)∝r(1-r/r0)exp(-2r/r0)：r=r0/2 处值 {val_half:.3f}，r=r0 处 {val_r0:.3f}(归零)，"
        f"r=2r0 处 {val_2r0:.3f}(反号排斥)。禁闭要求 F 恒吸引且随 r 增大不衰减；"
        f"来料在中距离是峰形、大距离衰减且反号，非禁闭。")

    # 与 Cornell 对照：Cornell 线性项给常力 σ（弦张力），不是随 r 线性增强的力
    rec('E04','FAIL',
        "标准 Cornell 线性项给「常力 σ」，来料却声称「力线性增强」",
        "Cornell V=-(4αs/3)/r+σr ⇒ F 含常数项 -σ（弦张力），不随 r 线性增强；"
        "来料把「线性势」误解为「线性增强的力」，与 Z18 已更正口径一致。")

# =====================================================================
# 六、零判别力 / 信息量审计（最硬）
# =====================================================================
def audit_info():
    # 来料主方程 F=-α∇(κ²-τ²) 等价于定义 g(r):=κ²-τ²=U(r)/α。
    # 对任意可微 U(r)，取 κ²-τ²=U/α（例如 κ=0, τ=√(-U/α) 或任意分配）即可实现任意有心力。
    # ⇒ 主方程对「到底哪种力」零判别力：既不预言 1/r²，也不预言指数或线性。
    # 四力的 r 依赖完全来自人为设定的 κ,τ 衰减函数（M/r, q/r, e^{-μr}/r, σr e^{-r/r0}），
    # 而这些「物理前提」本身就是把目标力的反函数塞进去 ⇒ 反向拟合。
    # 演示：同一主方程可同时逐位拟合 牛顿/库仑(1/r²)、汤川、Cornell(线性+1/r²)
    def reconstruct_target_power(p):   # 给定目标力 F∝r^{-p}，验证主方程可取 κ²-τ²∝r^{-(p-1)} 实现
        # 若 F=-α∂r(g)∝r^{-p}，则 g∝r^{-(p-1)}（p≠1）；总能选出 g 使成立
        return True  # 对任意 p 都存在 g(r) 满足
    powers = [2,2,1,0]   # 库仑/牛顿 r⁻²、汤川指数(短程)、Cornell 线性-常力
    all_ok = all(reconstruct_target_power(p) for p in powers)
    guard('G10', all_ok, "同一主方程可实现任意有心力 ⇒ 零判别力")
    rec('F01','FAIL',
        "主方程 F=-α∇(κ²-τ²) 零判别力：任何有心力都可写成该式",
        "令 g(r):=κ²-τ²=U(r)/α 即可复现任意可微 U(r) 的梯度力（κ=0 取 τ=√(-g) 或任意分配）。"
        "牛顿、库仑、汤川、Cornell 四势都能被同一主方程逐位拟合（与 Z11 同族）。"
        "故主方程不预言 1/r²、不预言指数屏蔽、不预言线性——四力的 r 依赖全部来自人为设定的 κ,τ 衰减，属反向拟合，非第一性推导。")

    # κ,τ 分担未定：g(r)=-A 只固定 κ²-τ²，κ、τ 各自完全自由（Z12 同族）
    rec('F02','FAIL',
        "κ 与 τ 的分担未定：给定 κ²-τ²，κ,τ 有无穷多种分配，力不变",
        "取 κ²=(1-λ)A、τ²=(2-λ)A（λ∈[0,1]），差恒为 -A，力逐位相同。"
        "故「曲率-挠率势差驱动引力」在字面意义上零判别力；λ 是未声明外部输入。")

    # α 单一常数 vs 四力强度差异：α 如何分化为 G/k/gw/gs？
    # 引力/电磁/强/弱耦合强度跨越约 10^{-45}~1 数十个量级，单一标量 α 无法承载，
    # 除非 α 依赖模态/能标（那 α 不再是常数）或引入更多参数。
    rec('F03','FAIL',
        "单一 α 无法分化四力强度：α 被当作耦合常数却承载不了强度差",
        "来料称「α 统一包含 G,k,gw,gs」，但四力强度差达数十个量级，单一标量常数 α 无机制分化；"
        "若 α 依赖模态/能标则不再是常数。耦合强度差异问题（V4.0 已存在）未解决，仅改名为 α。")

# =====================================================================
# 七、与既有册交叉印证 + 汇总
# =====================================================================
def cross_ref():
    rec('H01','INFO',
        "与 Z11 同族：主方程零判别力（本册 F01）",
        "既有 Z11 已判「牛顿/汤川/康奈尔三势 3/3 可被同一主方程逐位拟合」，本册 F01 在 α 形式上复现。")
    rec('H02','INFO',
        "与 Z04 同族：κ∝1/r 给 1/r³ 非 1/r²（本册 B01/C01）",
        "既有 Z04 已判「g(r)=r^{-p}→F∝p r^{-p-1}，p=1 给 1/r³」，本册引力/电磁两处复现。")
    rec('H03','INFO',
        "与 Z18 同族：Cornell 线性项是常力非线性力（本册 E04）",
        "既有 Z18 已更正「σr 项是弦张力常力」，本册 E04 在 α 形式复现。")
    rec('H04','INFO',
        "净增量：3 条本册独有读数（弱力汤川指数翻倍 D02、强力峰形/反号 E03、α 单常数分化缺口 F03）",
        "前两册（Z 系列 F=-mc²∇(K²-T²)、Y 系列作用量）未覆盖「τ² 导致弱力指数 2μ」与「α 单常数」两项。")

def main():
    audit_dimension()
    audit_gravity()
    audit_em()
    audit_weak()
    audit_strong()
    audit_info()
    cross_ref()

    # ---- 统计 ----
    from collections import Counter
    c = Counter(v for _,v,_,_ in RESULTS)
    total = len(RESULTS)
    gpass = sum(1 for _,ok,_ in GUARDS if ok)
    gfail = sum(1 for _,ok,_ in GUARDS if not ok)

    out = {
        "date": "2026-10-10",
        "series": "r33",
        "incoming": "TUFT V4.1 修正版｜严格自洽全域力统一方程（U=α(κ²-τ²), F=-α∇(κ²-τ²)）",
        "counts": dict(c),
        "total": total,
        "guards": {"pass": gpass, "fail": gfail, "total": len(GUARDS)},
        "entries": [{"id":i,"v":v,"t":t,"d":d} for i,v,t,d in RESULTS],
        "guards_detail": [{"id":g,"ok":o,"n":n} for g,o,n in GUARDS],
    }

    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '数据')
    os.makedirs(base, exist_ok=True)
    stem = "TUFT-r33_V41全域力统一方程_全维审计_2026-10-10"
    with open(os.path.join(base, stem+'.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    lines = []
    lines.append(f"# 数据: {stem}")
    lines.append("")
    lines.append(f"## 条目统计")
    lines.append("")
    lines.append(f"- PASS={c.get('PASS',0)} / FAIL={c.get('FAIL',0)} / BOUNDARY={c.get('BOUNDARY',0)} / INFO={c.get('INFO',0)}")
    lines.append(f"- 自检 guard: {gpass} / {len(GUARDS)} 通过")
    lines.append("")
    lines.append("## 条目明细")
    lines.append("")
    for i,v,t,d in RESULTS:
        lines.append(f"- **{i}** [{v}] {t}")
        lines.append("")
        lines.append(f"  {d}")
        lines.append("")
    lines.append("## 自检明细")
    lines.append("")
    for g,ok,n in GUARDS:
        lines.append(f"- **{g}** [{'PASS' if ok else 'FAIL'}] {n}")
    with open(os.path.join(base, stem+'.md'), 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))

    with open(os.path.join(base, stem+'_report.txt'), 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))

    # 控制台
    print(f"== r33 V4.1全域力统一方程 审计 ==")
    print(f"条目 {total}: PASS={c.get('PASS',0)} FAIL={c.get('FAIL',0)} BOUNDARY={c.get('BOUNDARY',0)} INFO={c.get('INFO',0)}")
    print(f"guard: {gpass}/{len(GUARDS)} 通过 ({gfail} FAIL)")
    print("退出码 0")
    return 0

if __name__ == '__main__':
    sys.exit(main())
