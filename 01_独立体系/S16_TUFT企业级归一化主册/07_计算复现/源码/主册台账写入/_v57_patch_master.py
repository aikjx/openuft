# -*- coding: utf-8 -*-
"""主册头部升 v6.8->v6.9：改标题 + 插入 v6.9 块（不动 v6.8 块及以下）。"""
import io
P = r"D:\a10\aikjx\code\my_lib\openuft\01_独立体系\S16_TUFT企业级归一化主册\13_论文与成果\主册\TUFT_企业级归一化主册_v1.0.md"
t = io.open(P, encoding="utf-8").read()
lines = t.split("\n")

# 1) 标题行（lines[0]）v6.8 -> v6.9
assert "主册 v6.8" in lines[0], "title v6.8 not found"
lines[0] = lines[0].replace("主册 v6.8", "主册 v6.9", 1)
# 标题里 E1-E506 -> E1-E507
assert "E1–E506" in lines[0], "E1-E506 not in title"
lines[0] = lines[0].replace("E1–E506", "E1–E507")

v69 = """
> **★★ v6.9（v57 GR n0 锚独立复算轮：Leaver 连分数首原理复算 Schwarzschild (2,2,n) 谱，n0 14.8 位 PASS、v56 自陈缺口闭合，2026-09-26，append-only；数字照抄原始输出，禁伪闭合，不回退）**：先 Read 磁盘 SSOT（v6.8/E1–E506/勘误#42）确认 a=0 锚引用值（GR n0=0.3736716844180418−0.088962315688936i、GR n1=0.3467109968791653−0.2739148752912331i、Grade A ω=0.434445178−0.056449760i、K=538.5417 Hz@60M☉）。磁盘起点 **v6.8/E1–E506/勘误#42**，本轮升 **v6.9/E1–E507/勘误#42 held（本轮无新勘误）**；物理四态 **35/61/18/27 冻结**。
>
> **① Leaver 求导链（mpmath dps=50，不 import prior-project，数字照抄 `_audit_v57_gr_n0_leaver_out.txt`）**：M=1，s=−2 Teukolsky 径向方程，Δ=r²−2r，K=r²ω，λ=l(l+1)−s(s+1)=4；ansatz R=e^{iωr*}(r−2)^{2−2iω}r^{−2}Σa_n z^n（z=(r−2)/r，视界 ingoing、无穷 outgoing）；三项递推 α_n a_n+β_n a_{n−1}+γ_n a_{n−2}=0，Schwarzschild 闭式：α_n=n²+(4−4iω)n+(3−4iω)，β_n=−2n²+(−2+16iω)n+(−3+8iω+32ω²)，γ_n=n²+(−2−8iω)n+(−16ω²+8iω)；连分数自底向上 r_n=−γ_{n+1}/(β_{n+1}+α_{n+1}r_{n+1})（r_N=0 tail），谱条件 C_0(ω)=β_0+α_0 r_0=0。
>
> **② v56 不收敛诊断（三处硬伤，非 tail 方向/分支切线/Γ 相位问题）**：(1) **对角缺 ω 依赖**——v56 a(n)=(n−1)²−5 完全不含 ω，正确 α_n 必须含 (4−4iω)n+(3−4iω)；(2) **谱条件归一化错**——v56 返回 1+b(0)/g，正确应是 β_0+α_0 r_0=0；(3) **耦合结构错**——v56 b(n)c(n+1) 不对称耦合，与三项递推 α/β/γ 结构不符。本轮按正确 α/β/γ 闭式 + 自底向上连分数 + C_0=0 谱条件重写，收敛到锚。
>
> **③ n0 复算 PASS（14.79 位）**：粗初值 0.40−0.10i、N=200，w_n0=0.37367168441804183578−0.08896231568893569827i，|C_0(root)|=7.2e-51，|w_calc−w_Berti|=1.6079e-15，**有效位数 14.79 位（目标 ≥10）→ PASS**。N 收敛 spread：N=50→8.56e-11、N=100→9.93e-15、N=200→1.61e-15、N=400→1.61e-15（N=200→400 步长 2.2e-20 已平台）。
>
> **④ n1 第二对照（13.09 位）**：粗初值 0.35−0.27i、N=200，w_n1=0.34671099687916531122−0.27391487529123308730i，|C_0(root)|=1.93e-50，|w_calc−w_Berti(n1)|=8.0613e-14，**有效位数 13.09 位**。N 收敛 spread：N=50→4.35e-8、N=100→4.22e-11、N=200→8.06e-14、N=400→7.97e-14（tail=0 截断在 ~1e-13 平台，加 Nollert tail 可再压）。
>
> **⑤ v56 自陈缺口闭合**：v6.8/v56 轮诚实标注"首原理另写 Schwarzschild Leaver 连分数试 3 组系数均落错根、未收敛到 a=0 锚，按纪律不伪造 GR 门 PASS，a=0 锚采用已发表 Leaver(1985)/Berti 标准值"。本轮 v57 按正确三项递推闭式 + 自底向上连分数首原理复算 n0 达 14.8 位（≥10 位目标）、n1 第二对照 13.1 位交叉验证一致 → **观测检验报告中 a=0 锚由【引用锚(Berti 表)】升级为【独立复算锚】**，v56 自陈缺口闭合；GR 门独立复算链不再依赖外部查表。
>
> **⑥ E507（GR Schwarzschild n0 锚独立复算 14.8 位 PASS，v56 自陈缺口闭合，n1 第二对照 13.1 位）**：门/方法学通道，**不闭合新物理 E 数进四态**；勘误 #42 held（无新勘误）；四态 35/61/18/27 冻结。D18 v31 UPGRADE 无回退；联盟层维持 **2/6**、UFT-3 未解锁。open_backlog：TUFT 静态 11.6 位硬门仍 OPEN（8.4 位/<1e-6 已达，两域 assembly 未过 GR 门 B 仅 1.05 位——本轮 GR 门 A 独立 Leaver 已 14.8 位 PASS 验证求解器正确，两域 assembly 界面匹配块仍为第一障碍）；旋转绝对值 1.62 仍无外部 Grade-A 锚（仅 v54 内部互证，稳健量=0.35 抑制比/6.44× 判别比）；a≥0.2 慢转一阶渐近失真（O(a²)~3–4%）；5 升层项（e/f_π/nullity_dyn=0/Page/Hawking）全部 OPEN。本轮交付：《TUFT_v57_GR_n0锚复算合并报告.md》、脚本 `_audit_v57_gr_n0_leaver.py`/`_out.txt`；openuft 第66章 append §66.20。
"""

# 在 lines[1]（空行）后插入 v69 块
new = "\n".join(lines[:2]) + v69 + "\n".join(lines[2:])
io.open(P, "w", encoding="utf-8").write(new)

# 校验
chk = io.open(P, encoding="utf-8").read()
print("title v6.9:", "主册 v6.9" in chk)
print("E1–E507 in title:", "E1–E507" in chk)
print("v6.9 block present:", "v6.9（v57 GR n0 锚独立复算轮" in chk)
print("v6.8 block retained:", "v6.8（v56 观测检验轮" in chk)
print("v6.7 block retained:", "v6.7（v55 最终收口轮" in chk)
print("E507 count:", chk.count("E507"))
print("len() now:", len(chk))
