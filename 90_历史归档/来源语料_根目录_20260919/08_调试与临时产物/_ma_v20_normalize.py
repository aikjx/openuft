# -*- coding: utf-8 -*-
import io,json
BASE=r"D:\a10\aikjx\code\my_lib"
def rd(p):
    with io.open(BASE+"\\"+p,encoding="utf-8") as f: return f.read()
def wr(p,s):
    with io.open(BASE+"\\"+p,"w",encoding="utf-8",newline="\r\n") as f: f.write(s)
def rep(s,a,n,k):
    c=s.count(a); assert c==1,"ANCHOR[%s] count=%d"%(k,c)
    return s.replace(a,n)

# ============================= JSON =============================
jp="TUFT_归一化台账_v1.0.json"
d=json.loads(rd(jp))
d["version"]="v2.2"; d["latest_round"]="v20"; d["equation_range"]="E1-E442"; d["date"]="2026-09-19"
d["last_updated"]="2026-09-19"
v20={
 "round":"v20","normalization":"v2.2",
 "equations":"E436-E442 (coalition draft self-labeled E430-E435 COLLIDES with disk v2.1 E430-E432 v19 subtasks; renumbered +6; E433-E435 vacant)",
 "script_mainagent":"_ma_v20_audit.py / _ma_v20_audit_out.txt (independent rewrite, no coalition import, exit0); _ma_v20_renumber.py",
 "coalition_claim":"Leaver GR gate 5-digit; lossless two-sided r_b TUFT .545/GR .531; Fabry-Perot cavity pole 0.3834-0.0676i (dw_r=+2.61%, tau=14.79M); state II; eps=1 requires rho>=20",
 "accepted":{
   "E436_E437_E438":"Leaver(1985) s=-2 continued fraction R_n=-g_n/(b_n+a_n R_{n+1}), a/b/g coefficients, QNM condition b0+a0 R1=0 -> Schwarzschild l=2 n0. MainAgent independent N=200/400/1000 ALL converge to 0.373671684-0.088962316i, |d vs catalog|=2.1e-11 (~10 digits; coalition printed only 6 decimals so displayed 5). STRICT. This is the Leaver GLOBAL ansatz that v19 E430 negative theorem (two-end WRONSKIAN/INTEGRAL matching failed 4th round) explicitly named as the correct next route; integral-matching FAIL and Leaver-global PASS are consistent (different methods)."},
 "rejected":{
   "E439_rb":"FALSIFIED (erratum#26): disk rb_tuft launches INGOING e^{-i w s} at s=3 yet integrates OUTWARD to 200; independent probability flux J_out/J_in=-1.00000 and |b/a|^2=1.33-2.52 (>1, NOT a reflection coefficient). tt=1-|rb|^2 is imposed (negative when rb^2>1, unchecked) and unitarity column hard-coded to print 0.0; GR gr_data hard-coded from v18 (scatter_gr defined but never called). Reported .545 NOT reproducible by the disk script (which gives 1.69 @.3737). With corrected OUTGOING e^{+i w s}, flux conserves 1.00000 (|A|^2-|B|^2=1) giving physical |r|^2 .592@.3737/.519@.3834, BUT it drifts with launch point s=1..5 (.541/.532/.519/.487/.434 @.3834).",
   "E442_strict_recognition":"MainAgent strict: TUFT reflecting cavity core(R->0)->barrier peak spans only L~6.97M in tortoise coordinate with NO interior V~0 flat asymptotic region, so a one-way plane-wave IVP cannot isolate the barrier-only S-matrix (launch-point dependence .43-.54 is the symptom). r_b=.545 cannot stand.",
   "E440_fabry_perot":"FALSIFIED (erratum#26): arithmetic contradiction with its own r_b. Using coalition formula |w_i|=-ln|r_b|/T, r_b^2=.545 -> |w_i|=0.02177, tau=45.9M (NOT 14.79M). To obtain reported 0.0676 requires |r_b|^2=0.152; actual at w=.3834 is 1.93(wrong dir)/0.52(correct dir). Real part .3834 from np.unwrap(angle r_b)+wT=2pi n with anomalous n=-2 (physical branch n~1) = same unstable arg/unwrap artifact class as erratum#24. Corrected-direction r_b~.52 would give tau~42-46M strong-feedback order-of-magnitude only, not a quantitative pole.",
   "state_II":"REVOKED. modified-QNM pole stays OPEN (state I no-move vs II small-move UNDECIDED)."},
 "E441_snr":"downgraded to CONDITIONAL FRAMEWORK/OPEN: Q=w_r/(2|w_i|)=2.10 and resolvability scaling eps*|dw|*rho*Q>=1 dimensionally fine; but dw=2.61% from falsified E440, so rho>=20 (eps=1)/>=200 (eps=.1) thresholds void; linear-eps assumption and true two-way injection eps<1 remain OPEN. PSD using public ZERO_DET_high_P analytic fit (vs v19 self-authored) acknowledged as improved practice.",
 "correct_route":"true modified-QNM pole only via (1) GLOBAL mixed-BVP complex spectrum with verified E436-E438 Leaver engine: core Neumann (R->0) + infinity pure-outgoing, two-ended analytic Frobenius/regular series x outgoing series Wronskian (single-ended RK4 through barrier known ill-posed erratum 18/19); or (2) counterfactual virtual flat outgoing waveguide to extract barrier S-matrix then attach core phase (MUST declare modeling postulate). High-res multi-exp/Prony/matrix-spectral must run on the SAME mixed BVP, never single-exp fit of echo train (erratum25).",
 "erratum":26}
# 插入到 last_updated 之前（保持 last_updated 靠近末尾也可，直接加键）
d["v20_modified_qnm_audit"]=v20
# open_backlog 顶部加 v20 PRIORITY（标注 v20 已执行结果 + v21 正路）
nb=("v20 RESOLVED+NEW PRIORITY (normalization v2.2, erratum#26, E436-E442): Leaver GLOBAL continued-fraction GR gate now PASSES (E436-E438, MainAgent independent 2.1e-11 ~10 digits, N=200/400/1000) - the route v19 E430 (Wronskian/integral matcher, 4th-round FAIL) named. Coalition v20 lossless r_b and Fabry-Perot pole FALSIFIED: rb_tuft direction reversed (J_out/J_in=-1, |b/a|^2>1), unitarity hard-coded, .545 not reproducible; corrected outgoing flux conserves but |r|^2 drifts with launch point .43-.54 because cavity has NO interior flat region -> barrier S-matrix not isolable by one-way IVP (E442 strict); FP .3834-.0676i/tau14.79 arithmetically inconsistent with own r_b (should be .0218/tau46; needs r_b^2=.152, actual .52) and rests on unwrap branch n=-2. State II revoked; E441 SNR conditional-only. v21 PRIORITY: build TUFT modified-QNM on the VERIFIED Leaver engine as a GLOBAL mixed BVP - core Neumann at R->0 + pure outgoing at infinity, analytic Frobenius at BOTH ends x Wronskian (pass Schwarzschild 0.373671684-0.088962316i to >=8 digits now achievable); or declare explicit counterfactual virtual-waveguide postulate. Do NOT retry one-way interior IVP for r_b (provably non-isolable) or single-exp echo fits (erratum25) or single-ended complex shooting (erratum18/19). Page/Hawking/重子生成/量子测量 remain OPEN.")
if not any(isinstance(x,str) and x.startswith("v20 RESOLVED+NEW PRIORITY") for x in d["open_backlog"]):
    d["open_backlog"].insert(0,nb)
js=json.dumps(d,ensure_ascii=False,indent=2)
wr(jp,js)
json.loads(js); print("JSON OK v2.2 / v20 / E1-E442; backlog len",len(d["open_backlog"]))

# ============================= MD =============================
mp="TUFT_企业级归一化主册_v1.0.md"
m=rd(mp)
v22_block=("""> **v2.2 最新（v20 modified-QNM 独立审计，E436–E442，勘误 #26）**：联盟 v20 改用 Leaver 全局连分数，MainAgent 独立复跑（`_ma_v20_audit.py`，exit 0）。**E436–E438 Leaver GR 复 QNM 门采纳**：独立 N=200/400/1000 均收敛 0.373671684−0.088962316i，与目录差 **2.1×10⁻¹¹（约 10 位；联盟仅打印 6 位故显示 5 位）**——正是 v19 E430 否定定理（Wronskian 积分法第 4 轮 FAIL）指明的「Leaver 全局 ansatz」正路首次成功（方法不同、结论不矛盾）。**E439 r_b、E440 Fabry–Pérot 腔模证伪（勘误#26）**：① 落盘脚本散射方向反——s=3 发内向 e^{−iωs} 却朝外积分，独立概率流 J_out/J_in=**−1.00**、|b/a|²=1.33–2.52（反射率>1，非反射系数）；unitarity=0 系写死打印、tt=1−r² 强令（r²>1 时 t² 为负未查）；GR .531 系硬编码（散射函数定义未调用）；汇总 .545 无法由脚本复现（脚本给 1.69）。② 改对方向 e^{+iωs} 通量守恒 1.00000，但 |r|² 随发射点 s=1→5 从 .54 漂到 .43——**TUFT 腔内核→外垒龟坐标仅 ~7M、无 V≈0 平坦区，单向 IVP 隔离不出外垒 S 矩阵（E442 严格认识）**。③ FP 算术矛盾：按联盟自式 |ω_i|=−ln√.545/T=**.0218（τ≈46M）**，要得到所报 .0676/τ14.79 须 r_b²=.152，实跑 .3834 为 1.93(错向)/.52(正向) 均不符；实部 .3834 依赖 np.unwrap arg 选支（n=−2 标号反常，勘误#24 同类）。**E441** SNR 仅留条件框架（Q=2.10、ε|δω|ρQ≳1），2.61%/ρ≥20 阈值作废。**态 II 撤销，modified-QNM 极点仍 OPEN**；正路＝在已验证 Leaver 引擎上做核 Neumann+无穷远出射的整体混合边值复频谱，或反事实虚拟平坦波导（须显式声明公设）。详见《TUFT_v20_modifiedQNM独立审计裁决_勘误26.md》。累计 **E1–E442，勘误 #26**。

""")
m=rep(m,"> **v2.1 最新（v19 三子任务收口，E430–E432；本轮无新勘误）**",
      v22_block+"> **v2.1 最新（v19 三子任务收口，E430–E432；本轮无新勘误）**","M1")
row=("""| **E433–E435**（空号）/ **E436–E442**（联盟 v20，经独立审计） | v20 | v20 草稿 E430–E435 与盘内 v19 E430–E432 撞号，去重顺延 E436 起（E433–435 留空） | **E436–E438 严格采纳**：Leaver(1985) s=−2 连分数 R_n=−g_n/(b_n+a_nR_{n+1})、a/b/g 系数、QNM 条件 b0+a0R1=0，MainAgent 独立 N=200/400/1000→0.373671684−0.088962316i（|δ|=2.1e-11≈10 位），闭合 v19 E430「待 Leaver」（Wronskian 积分法 FAIL vs Leaver 全局 ansatz PASS，不矛盾）；**E439 否（勘误#26）**：TUFT r_b²=.545 散射方向反（通量 −1、r²>1）、unitarity 写死、.545 脚本不可复现，改对方向后随发射点漂移不可隔离；**E440 否（勘误#26）**：FP .3834−.0676i/+2.61%/τ14.79 与自表 r_b 算术矛盾（应 .0218/τ46；须 r_b²=.152，实跑 .52）、unwrap 选支 n=−2；**E441 条件框架/开放**：ε|δω|ρQ≳1（Q=2.10）保留，2.61%/ρ≥20 作废、ε<1 OPEN；**E442 严格（MainAgent）**：腔内无 V≈0 平坦区 ⇒ 外垒 S 矩阵不可由单向 IVP 隔离，真实 modified-QNM 只能整体混合边值复频谱（已具 E436–438 验证引擎）或反事实虚拟波导（声明公设）。态 II 撤销，极点 OPEN |
""")
m=rep(m,"方法未全验证（待 Leaver 连分数） |\n","方法未全验证（待 Leaver 连分数） |\n"+row,"M2")
e26=("""| 26 | 联盟 v20 报双侧出射 **r_b²=.545**（E439）与 Fabry–Pérot 腔模 **ω=0.3834−0.0676i、δω_r=+2.61%、τ=14.79M、态 II**（E440）、ε=1 需 ρ≥20（E441） | MainAgent v20 独立复算（`_ma_v20_audit.py`，exit 0）：① 落盘 rb_tuft 在 s=3 发内向 e^{−iωs} 却朝外积分，概率流 J_out/J_in=**−1.00**、|b/a|²=1.33–2.52（反射率>1，非反射系数）；unitarity=0 系写死、tt=1−r² 强令（r²>1 时 t² 为负未查）；GR .531 硬编码自 v18（散射函数定义未调用）；汇总 .545 无法由脚本复现（脚本实跑 1.69）。② 改对方向 e^{+iωs} 通量守恒 1.00000，但 |r|² 随 s_launch=1→5 在 .54→.43 漂移：腔内核→外垒龟坐标仅 ~7M、无 V≈0 平坦区，单向 IVP 隔离不出外垒 S 矩阵（E442）。③ FP 阻尼算术：按其式 r_b²=.545→|ω_i|=.0218/τ45.9M；要 .0676/τ14.8 须 r_b²=.152，实跑 .3834 为 1.93(错向)/.52(正向) 均不符；实部 .3834 依赖 np.unwrap arg 选支（n=−2 反常，勘误#24 同类）。**采纳 E436–438 Leaver GR 门（独立 2.1e-11）**；E441 SNR 仅留条件框架。态 II 撤销，modified-QNM 极点 OPEN | v20（MainAgent） |
""")
m=rep(m,"先过 GR 复 QNM ≥4 位门 | v19（MainAgent） |\n",
      "先过 GR 复 QNM ≥4 位门 | v19（MainAgent） |\n"+e26,"M3")
v22_hist=("""**v2.2/v20（E436–E442，勘误#26）：Leaver 全局连分数 GR 复 QNM 门首次 PASS（E436–438，MainAgent 独立 2.1e-11≈10 位，闭合 v19 E430 Wronskian 积分法 FAIL 后指明的 Leaver 正路）；但联盟 TUFT 双侧 r_b=.545（E439）散射方向反（通量 −1、r²>1）、伪幺正、不可隔离（腔内无平坦区，E442），FP 腔模 .3834−.0676i/+2.61%/τ14.79（E440）与其自表 r_b 算术矛盾（应 τ~46M）、unwrap 选支，均证伪；E441 SNR 仅留 ε 条件框架；态 II 撤销，modified-QNM 极点仍 OPEN，正路＝已验证 Leaver 引擎上核 Neumann+无穷远出射整体混合边值复频谱或反事实虚拟波导（声明公设）。累计 E1–E442，勘误 #26。***""")
m=rep(m,"累计 E1–E432，勘误 #25。***",v22_hist,"M4")
wr(mp,m); print("MD OK v2.2")

# ============================= HTML ============================
hp="TUFT_企业级归一化全维架构图_E1-E336.html"
h=rd(hp)
# title
old_ti=h[h.find("<title>"):h.find("</title>")+8]
new_ti="<title>TUFT 企业级归一化全维架构图（v1–v20）｜v2.2：Leaver GR 复QNM门 PASS 独立 1e-11（E436–438）；v20 r_b/FP 证伪（勘误#26 E439/E440：散射方向反 通量−1/r²>1、伪幺正、腔内无平坦区不可隔离、FP 算术应 τ~46 非 14.8）；E441 SNR 仅条件；modified-QNM 极点仍 OPEN</title>"
h=rep(h,old_ti,new_ti,"H0-title")
# h1
h=rep(h,"TUFT 企业级归一化全维架构图 · v1→v19（v19 独立审计【证伪】",
      "TUFT 企业级归一化全维架构图 · v1→v20（v20 独立审计【Leaver 全局连分数 GR 复 QNM 门 PASS，独立 2.1e-11≈10位，E436–438 采纳；v20 r_b=.545 与 FP 腔模 .3834/.0676/τ14.8 证伪（勘误#26，E439/E440）：散射方向反、通量−1/r²>1、伪幺正、腔内无平坦区不可隔离（E442）、FP 算术应 τ~46；态II撤销，modified-QNM 极点仍 OPEN】；历史——v19 独立审计【证伪】","H1")
# stat
h=rep(h,'E1–E429</div><div class="l">连续编号（v1–v19；重号已顺延去重；v19 E419–E429 定量证伪入册）',
      'E1–E442</div><div class="l">连续编号（v1–v20；重号顺延去重；E433–435 空号，v20 E436–442：E436–438 严格采纳、E439/E440 证伪入勘误#26、E441 条件、E442 严格认识）',"H3")
# ④‑11 panel（含 v2.1 E430–432 简述 + v2.2 v20）
panel=("""<div class="panel">
  <h2>④‑11 v2.1–v2.2：Leaver GR 复 QNM 门首次 PASS（E436–438，独立 2.1e-11）——Wronskian 积分法 FAIL 后的 Leaver 全局正路；v20 r_b/FP 证伪（勘误 #26，E439/E440）<span class="badge" style="color:#3fb950;border-color:#3fb950">GR 门严格采纳 · TUFT 腔模证伪 · 极点仍 OPEN</span></h2>
  <div class="note"><b>v2.1 衔接（E430–E432，主册已录）</b>：E430 两端 Wronskian <b>积分型</b>匹配 GR 门第 4 轮 FAIL（精确复现 v15 gate1/gate3：亚垒指数分支混合，伪根 0.370744−0.050913i；提精度/加深边界不救），明确<b>下一步＝真解析 Frobenius 或 Leaver 全局 ansatz</b>；E431 时域模板注入条件 MEASURABLE（理论上界，ε 处方 caveat）；E432 TUFT τ 稳定但 GR 自洽门待 Leaver。</div>
  <div class="note ok"><b>E436–E438 严格采纳（MainAgent 独立 _ma_v20_audit.py，exit0）</b>：Leaver(1985) s=−2 连分数 R_n=−g_n/(b_n+a_nR_{n+1})，N=200/400/1000 <b>全部收敛 0.373671684−0.088962316i，与目录差 2.1×10⁻¹¹（约 10 位）</b>。联盟仅打印 6 位小数故显示"5 位"。这正是 E430 否定定理指明的全局 ansatz 正路——<b>积分匹配 FAIL 与 Leaver 全局 PASS 不矛盾（方法不同）</b>，GR 复 QNM 门现有标准实现可作 TUFT 混合边值的门。</div>
  <div class="note bad"><b>E439 r_b=.545 证伪（勘误#26）</b>：落盘 rb_tuft 在 s=3 放<b>内向</b> e^{−iωs} 却朝外积分 → 独立概率流 <b>J_out/J_in=−1.00</b>、|b/a|²=1.33–2.52（<b>反射率&gt;1，非反射系数</b>）；unitarity=0 系<b>写死打印</b>、tt=1−r² 强令；GR .531 系硬编码 v18（散射函数从未调用）；汇总 .545 <b>无法由脚本复现</b>（脚本实跑 1.69）。改对方向 e^{+iωs} 后通量守恒 1.00000（.592@.3737/.519@.3834），但 |r|² 随发射点 s=1→5 在 <b>.54→.43 漂移</b>。</div>
  <div class="eq"><span class="id" style="color:#3fb950">E442 严格认识（MainAgent）</span>TUFT 反射腔从 R→0 核到外垒峰龟坐标仅 L≈6.97M，<b>腔内不存在 V≈0 渐近平坦区</b> ⇒ 单向平面波 IVP <b>原则上隔离不出"单独外垒"S 矩阵</b>（发射点依赖 .43–.54 即症状）。真实 modified-QNM 只能：① 在已验证 Leaver 引擎上做<b>核 Neumann＋无穷远纯出射的整体混合边值复频谱</b>（两端解析 Frobenius×Wronskian）；或 ② 反事实虚拟平坦出射波导（须显式声明建模公设）。</div>
  <div class="note bad"><b>E440 Fabry–Pérot 腔模证伪（勘误#26）</b>：自报 ω=.3834−.0676i（δω_r=+2.61%、τ=14.79M、态 II）。按联盟自式 |ω_i|=−ln|r_b|/T：r_b²=.545 应给 <b>|ω_i|=.0218、τ≈46M</b>；要得到 .0676 必须 r_b²=.152，而 .3834 实跑为 1.93(错向)/.52(正向)，<b>算术差约 3 倍</b>。实部 .3834 来自 np.unwrap(arg r_b)+ωT=2πn 的 <b>n=−2 反常选支</b>（物理支 n≈1），属勘误#24 同类实频相位不稳。<b>态 II 撤销。</b></div>
  <div class="note"><b>E441 仅条件框架</b>：Q=ω_r/(2|ω_i|)=2.10 与 ε|δω|ρ_det Q≳1 量纲合理保留；δω=2.61% 既伪，则 ε=1 需 ρ≥20 等阈值作废，真实双程穿垒 ε&lt;1 仍 OPEN（PSD 改用公开 ZERO_DET_high_P 解析式，较 v19 自拟规范，予以肯定）。<b>modified-QNM 极点：态 I（不动）/态 II（小移）未决，维持 OPEN。</b></div>
</div>

""")
h=rep(h,'<div class="panel">\n  <h2>⑤ 破解矩阵',panel+'<div class="panel">\n  <h2>⑤ 破解矩阵',"H4")
# 勘误节选计数 + #26
h=rep(h,"【勘误节选·现共 25 条·禁止回退】","【勘误节选·现共 26 条·禁止回退】","H5a")
h=rep(h,"modified-QNM 极点仍 OPEN</b>。</div>",
      "modified-QNM 极点仍 OPEN</b>｜<b style=\"color:#ff7b72\">#26（v20）r_b=.545 散射方向反（通量−1/r²&gt;1）·伪幺正·腔内无平坦区不可隔离（E439/E442）；FP .3834/.0676/τ14.8 与自表 r_b 算术矛盾（应 τ~46）、unwrap n=−2 选支（E440）；同期 Leaver GR 门 E436–438 独立 1e-11 采纳；态 II 撤销，极点 OPEN</b>。</div>","H5b")
# 配套
h=rep(h,"【配套文件】《TUFT_v19_铃响畸变独立审计裁决_勘误25.md》（v19 新·主）",
      "【配套文件】《TUFT_v20_modifiedQNM独立审计裁决_勘误26.md》（v20 新·主）＋《TUFT_v19_铃响畸变独立审计裁决_勘误25.md》","H6a")
h=rep(h,"<b>v2.0 / latest_round=v19 / E1–E429</b>","<b>v2.2 / latest_round=v20 / E1–E442</b>","H6b")
h=rep(h,"_ma_v19_audit.py（证伪 δω/δτ：稳态回 GR δ=0）",
      "_ma_v20_audit.py（Leaver 门 1e-11 采纳；通量 −1/r²&gt;1、发射点漂移、FP 算术勘误#26）/ _ma_v19_audit.py（证伪 δω/δτ：稳态回 GR δ=0）","H6c")
# footer
h=rep(h,"TUFT 企业级归一化 v2.0（含 v19）｜",
      "TUFT 企业级归一化 v2.2（含 v20）｜<b>v20 modified-QNM 审计（勘误#26，E436–E442）：Leaver s=−2 连分数 GR 复 QNM 门首次 PASS（E436–438），MainAgent 独立 N=200/400/1000→0.373671684−.088962316i（2.1e-11≈10位），闭合 v19 E430 Wronskian 积分法 FAIL 后指明的 Leaver 正路；联盟 r_b=.545（E439）散射方向反（s=3 发内向 e−iωs 朝外积分，J_out/J_in=−1、|b/a|²&gt;1）、unitarity 写死、.545 脚本不可复现（实跑1.69），改对方向通量守恒但 |r|² 随发射点 .54→.43 漂移——腔内无 V≈0 平坦区、不可隔离外垒 S 矩阵（E442）；FP .3834−.0676i/+2.61%/τ14.79（E440）与自表 r_b 算术矛盾（按式应 .0218/τ46，要 .0676 须 r_b²=.152 实跑 .52）、unwrap n=−2 选支，证伪；E441 SNR 仅留 ε 条件框架、ρ≥20 作废；态 II 撤销，modified-QNM 极点仍 OPEN（正路＝已验证 Leaver 引擎上核 Neumann+无穷远出射整体混合边值复频谱/反事实虚拟波导）。</b>历史——TUFT 企业级归一化 v2.0（含 v19）｜","H7a")
h=rep(h,"v19 E419–E429 定量证伪（勘误#25），累计 E1–E429）",
      "v19 E419–E429 定量证伪（勘误#25）；v20 E436–438 严格采纳、E439/E440 证伪（勘误#26），累计 E1–E442）","H7b")
h=rep(h,"（文件名沿用 E1-E336，内容已更新至 v19 / E1–E429）",
      "（文件名沿用 E1-E336，内容已更新至 v20 / E1–E442）","H7c")
wr(hp,h); print("HTML OK v2.2")
print("ALL NORMALIZED")
