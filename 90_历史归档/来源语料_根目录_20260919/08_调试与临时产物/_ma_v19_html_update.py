# -*- coding: utf-8 -*-
"""架构图升 v2.0：title/h1/2统计/④-10面板/勘误节选#25/配套/footer。精确替换+assert。"""
import io
p=r"D:\a10\aikjx\code\my_lib\TUFT_企业级归一化全维架构图_E1-E336.html"
s=io.open(p,"r",encoding="utf-8",newline="").read()
NL="\r\n" if "\r\n" in s else "\n"
def rep(old,new,n=1):
    global s
    c=s.count(old); assert c==n,"count %d!=%d :: %r"%(c,n,old[:50]); s=s.replace(old,new)

# title / h1
rep("（v1–v18 · v18严格势实频IVP：",
    "（v1–v19 · v19证伪：单指数拟合回声串δω/δτ系窗口伪影·稳态晚窗回GR(δ=0)·公比.211抵消为含视界.729·SNR双重计数作废·modified-QNM极点仍OPEN；v18严格势实频IVP：")
rep("· v1→v18（v18 严格面积势实频 IVP 独立审计：",
    "· v1→v19（v19 独立审计【证伪】铃响畸变定量 δω+2.64%/δτ−9.53%（勘误#25：瞬态多回声串单指数[2.5τ,8τ]窗口拟合伪影，换窗δω±7%/δτ±14%漂移，所有回声到齐后稳态晚窗回 ω_GR/τ_GR δ=0/1.5e-16；公比.211精确抵消为含视界.729，双侧r_b未做；SNR双重计数作废。保留C级无干净晚回波方向，modified-QNM极点OPEN）；历史——v18 严格面积势实频 IVP 独立审计：")

# stats
rep('<div class="n" style="color:var(--novel)">E1–E418</div><div class="l">连续编号（v1–v18；重号已顺延去重）</div>',
    '<div class="n" style="color:var(--novel)">E1–E429</div><div class="l">连续编号（v1–v19；重号已顺延去重；v19 E419–E429 定量证伪入册）</div>')
rep('<div class="n">24</div><div class="l">勘误固化条（#22 坐标·#23 频率2π·#24 τ/SNR/质量）</div>',
    '<div class="n">25</div><div class="l">勘误固化条（#23 频率2π·#24 τ/SNR·#25 v19拟合伪影/公比/SNR）</div>')

# ④-10 面板（插在 ⑤ 面板开 div 之前）
h2_5='  <h2>⑤ 破解矩阵 14 谜题（终态 0 / 12 / 2）</h2>'
panel10=(
'<div class="panel">'+NL+
'  <h2>④‑10 v19：铃响波形畸变定量证伪（E419–E429，勘误 #25）——单指数拟合回声串=窗口伪影，稳态极点精确回 GR<span class="badge" style="color:#ff7b72;border-color:#ff7b72">δω/δτ/SNR 证伪·方向保留</span></h2>'+NL+
'  <div class="note bad"><b>E422 复极点偏移 +2.64%/−9.53% 系拟合伪影（MainAgent 独立 _ma_v19_audit.py，逐位复现后证伪）</b>：联盟把瞬态多回声串 Σₙ rⁿ h_GR(t−nT)（n=0..6）在 <b>[2.5τ,8τ]</b> 用<b>单个</b> A e^{−t/τ}cos(ωt) 强拟合。仅改窗口 δω 即在 <b>+7.4%↔−3.4%</b>、δτ 在 <b>+11.8%↔−13.7%</b> 漂移（真极点不随窗口变）；所有回声（最晚 7.44τ 启动）到齐后<b>稳态晚窗精确回 ω_GR=0.37367/τ_GR=11.241（δ=0.00%），去包络晚窗频率偏差 1.5×10⁻¹⁶</b>。每项回声极点严格为 ω_GR、公比 .729&lt;1 级数收敛，晚期只改复留数、<b>真实复极点不动</b>（合 v19 解析骨架 §1）。反射腔物理应使 τ 增大，联盟报减小，<b>方向亦反</b>。</div>'+NL+
'  <div class="eq"><span class="id" style="color:#ff7b72">E421/E424 公比精确抵消</span>r_echo=.729×.289=<b>.211</b>，但 h_GR(t−nT) 自带 e^{+nT/τ}，第 n 项 r_echoⁿe^{nT/τ}=<b>Rbarrⁿ</b>（n=2：.0445×e^{2T/τ}=.5314=Rbarr²），<b>.211/.289 抵消、净公比=.729</b>；.729=√.531 是 v18「外垒+<b>吸收视界</b>」净反射，所需无耗散双侧出射 r_b(ω)（|r|²+|t|²=1）<b>未做 OPEN</b>。</div>'+NL+
'  <div class="eq"><span class="id" style="color:#ff7b72">E425/E426 SNR 作废</span>模板既用假极点 ω_TU <b>又</b>乘回声因子＝<b>双重计数</b>；PSD 自拟非标定；补充表另用垒顶 WKB ε=.64（违垒顶仅量级）。⇒ <b>ρ_req≈5.6、O4×2.5/Voy×46 不采信</b>。</div>'+NL+
'  <div class="note ok"><b>保留</b>：E423 几何 T/τ=1.24、主环 .289（v18 严格引用）；E429 <b>C 级方向</b>（回波埋入、无干净晚期分立回波），「改阻尼 −9.5%」作废。<b>modified-QNM 极点仍 OPEN</b>：①双侧出射 r_b（禁 .531）→②自洽 D0(ω)=a e^{iωT}（两端 Frobenius×出射 Wronskian，先过 Schwarzschild 复 QNM ≥4 位）→③多指数/Prony/谱法提极点（禁单指数拟合）→④SNR 随 ε 条件化＋标定设计 PSD＋单一模板。</div>'+NL+
'</div>'+NL+NL)
rep(NL+'<div class="panel">'+NL+h2_5, NL+panel10+'<div class="panel">'+NL+h2_5)

# 勘误节选 24->25 + 追加 #25 条目
rep("【勘误节选·现共 24 条·禁止回退】","【勘误节选·现共 25 条·禁止回退】")
rep("质量改标铃响残迹 M_f</b>。</div></div>",
    "质量改标铃响残迹 M_f</b>｜<b style=\"color:#ff7b72\">#25（v19）铃响畸变 δω+2.64%/δτ−9.53% 系瞬态多回声串单指数窗口拟合伪影（换窗漂移、稳态晚窗回 ω_GR/τ_GR δ=0/1.5e-16）；公比 .211 精确抵消为含视界 .729（双侧 r_b 未做）；ρ_req/SNR 双重计数作废；modified-QNM 极点仍 OPEN</b>。</div></div>")

# 配套
rep("《TUFT_v18_严格势实频IVP独立审计裁决.md》（v18 新·主）",
    "《TUFT_v19_铃响畸变独立审计裁决_勘误25.md》（v19 新·主）＋《TUFT_v18_严格势实频IVP独立审计裁决.md》")
rep("（已并入 v1–v18）","（已并入 v1–v19）")
rep("内部 <b>v1.9 / latest_round=v18 / E1–E418</b>",
    "内部 <b>v2.0 / latest_round=v19 / E1–E429</b>")
rep("MainAgent 独立脚本 _ma_v18_realfreq.py",
    "MainAgent 独立脚本 _ma_v19_audit.py（证伪 δω/δτ：稳态回 GR δ=0）/ _ma_v19_pole_feedback.py / _ma_v18_realfreq.py")

# footer
rep("<footer>TUFT 企业级归一化 v1.9（含 v18）｜",
    "<footer>TUFT 企业级归一化 v2.0（含 v19）｜<b>v19 铃响畸变定量证伪（勘误#25，E419–E429）：MainAgent _ma_v19_audit 逐位复现联盟 δω+2.64%/δτ−9.53% 系瞬态多回声串单指数[2.5τ,8τ]窗口拟合伪影（换窗 δω±7%/δτ±14% 漂移；回声到齐后稳态晚窗精确回 ω_GR/τ_GR δ=0、去包络频率偏差1.5e-16；反射腔应τ增大故方向亦反）；r_echo=.211 与 e^{nT/τ} 精确抵消、净公比=.729=√.531 含吸收视界（无耗散双侧 r_b 未做 OPEN）；SNR 模板双重计数＋自拟PSD＋垒顶WKB ε=.64，ρ_req/距离倍数作废；保留 E423 几何1.24/.289 与 C级无干净晚回波方向；modified-QNM 极点定量 OPEN（双侧 r_b＋自洽 D0、多指数提极点、GR≥4位门）。</b>历史 v18：")
rep("新增 E415–E418，累计 E1–E418）","E415–E418，v19 E419–E429 定量证伪（勘误#25），累计 E1–E429）")
rep("内容已更新至 v18 / E1–E418","内容已更新至 v19 / E1–E429")

io.open(p,"w",encoding="utf-8",newline="").write(s)
print("架构图 v2.0 更新完成（title/h1/2统计/④-10/勘误#25/配套/footer）。")
