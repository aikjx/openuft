# -*- coding: utf-8 -*-
import io

p = r'D:\a10\aikjx\code\my_lib\openuft\01_独立体系\S16_TUFT归一化主册\13_论文与成果\主册\TUFT_归一化主册_v1.0.md'
s = io.open(p, encoding='utf-8').read()

NEW_TITLE = (
"# TUFT 归一化主册 v6.5（v53 绝对振幅锚轮收口：把 ε 从单点 0.4697 收窄为区间 [0.0748,0.4697]——"
"ε 推导链 ε=√|T_B|²=1−|R_B|²，|R_B|²=0.530254 沿用 SSOT v31/v32（9.1e-8 门锚），GR 频 w²=0.1396<Vmax=0.1487 隧穿区、TUFT 频 w²=0.1887>Vmax 垒顶之上更透；"
"独立复算 RW l=2 垒峰 Vmax=0.151287@r=3.2808（Schwarzschild 解析）与 SSOT TUFT 外垒 0.148709@3.268 一致 PASS；"
"双程功率 |T_B|²=(1−0.530254)²=0.2207、ε_toy=0.4697 CONFIRMED；"
"6.28× 来源=toy prompt loudness L=11.993（E431 上界）÷E444 严格真实-PSD 锚 1.91=6.28，垒透射物理本身不致 6.28×（TUFT 频垒顶之上更透），6.28× 残余=源激发能绝对标度 e/f_π 升层项 OPEN；"
"ε_strict 区间 [0.0748,0.4697] ESTIMATED/OPEN（mpmath dps=40，下界=ε_toy/6.28）；"
"D_max 两档（60M☉，ρ_dev=1 阈，Gpc）O4 face-on toy 3.5603/strict 0.5670、O4 edge-on 1.2587/0.2005、Voyager face-on 15.4775/2.4649、Voyager edge-on 5.4721/0.8715；toy 档与 v47 锚逐位吻合（3.5603 vs 3.560；15.4775 vs 15.48）；"
"GR 极限 ε→0⇒ρ_frac→0⇒TUFT-deviation 通道 D_max→0、prompt GR 振铃保留（L=11.993）PASS；单主模近似明示（E477 仅 n=1）；"
"E503；当前勘误 #42 held【本轮无新勘误】；物理四态 35/61/18/27 冻结；"
"v6.4 两域三处精修、v6.3 鲁棒两域单元、v6.2 Grade-A 静态攻坚、v6.1 Chandrasekhar+镜壁、v6.0 第三独立谱方法诊断裁决不回退）"
)

V65_BLOCK = r"""
> **★★ v6.5（v53 绝对振幅锚轮收口：ε 从单点 0.4697 收窄为区间 [0.0748,0.4697] / 6.28× 定位到源激发能 e/f_π 升层项 OPEN / 垒透射物理 CONFIRMED，2026-09-25，append-only，本轮最高信号；诚实分级，不伪闭合）**：组织者 v53-A 结果先 Read `_audit_v53_amplitude_anchor_out.txt` 核对后照抄（organizer 已核验；另写实现、不 import 任何 prior-project 脚本；GR 门先行；禁伪闭合；mpmath dps=40；数字照抄原始输出）。磁盘起点 **v6.4/E1-E502/勘误#42**，本轮升 **v6.5/E1-E503/勘误#42 held（本轮无新勘误）**；物理四态 **35/61/18/27 冻结**；不回退任何勘误与否定定理——v6.4 GR 门 B 仅 1.05 位 FAIL、v6.3 鲁棒两域单元、v6.2 Grade-A 静态攻坚、v6.1 Chandrasekhar+镜壁、v6.0 第三独立谱方法诊断裁决维持；本轮为**绝对振幅锚审计通道**（不闭合新物理 E-number，E503 为数值调查/边界通道登记，不进物理四态）。
> **① ε 推导链（toy vs strict）**：SSOT 锚点照抄——GR n₀=$(0.37367168441804166-0.0889623156889341j)$，TUFT Grade-A w=$(0.434445178-0.05644976j)$，$\rho_h/R/V_{\max}/L=0.609902/3.268/0.148709/6.9698$，门锚 $|R_B|^2=0.530254$，$|T_B|^2=(1-R)^2=0.220661304516$（SSOT 0.2207），$\varepsilon_{\rm toy}=\sqrt{|T_B|^2}=0.469746$（E489 0.4697）。**toy（E489 上界处方）**：壁=理想镜 $|r_{\rm wall}|=1$、垒=无耗阶跃、垒顶满通量入射；单程透射幅 $|t_B|=\sqrt{1-|R_B|^2}$，双程场幅 $|t_B|^2=1-|R_B|^2$；物理=入射透射入腔 $|t_B|$→壁反射 $|r_{\rm wall}|=1$→再透射外出 $|t_B|$，出腔回波幅 $=|t_B|^2|r_{\rm wall}|=1-|R_B|^2=0.4697$（E431/E489 上界）。**strict（双程穿垒，从壁反射核 $R=b/a$ 出发）**：(a) 垒透射单程功率 $|t_B|^2=1-|R_B|^2=0.469746$、双程 $|T_B|^2=(1-R)^2=0.220661$；(b) 壁反射核——TUFT 壁 $|r_{\rm wall}|^2=1$（D25/E488，$\Gamma=0$ 机器精度），近壁 $s^\beta$ Frobenius 有界支 $\beta=1.263763$，反射相位=腔共振 round-trip；(c) 垒顶有效通量——GR 频隧穿区 $|R_B|^2=0.530$、TUFT 频垒顶之上更透；垒物理双程场幅 $\varepsilon_{\rm barrier}=1-|R_B|^2=0.469746$（与 toy 同阶）。
> **② RW 垒峰独立复算（l=2, M=1；mpmath dps=40）PASS**：独立 RW l=2 垒峰 $V_{\max}=0.151287$ @ $r=3.2808$（SSOT $V_{\max}=0.148709$ @ $R=3.268$，一致）。[诚实] GR 门 $|R_B|^2$ 精算需 E476 WKB 出射波分解，本审计不重复；GR 门锚 0.530254 沿用 SSOT v31/v32（9.1e-8），不伪闭合。**频域定位**：GR 频 $w=0.373672$，$w^2=0.139631$ vs $V_{\max}=0.148709$ ⇒ **隧穿区（$w^2<V_{\max}$）**；TUFT 频 $w=0.434445$，$w^2=0.188743$ vs $V_{\max}=0.148709$ ⇒ **垒顶之上（$w^2>V_{\max}$），垒更透**。
> **③ 6.28× 来源（垒透射物理本身不致 6.28×）**：toy prompt loudness $L=11.993$ SNR·Gpc（E431 上界，$|R_B|=0.729$ 反射幅作回波幅）÷ E444 严格真实-PSD 锚 $=1.91$ SNR·Gpc（双程穿垒+真实 PSD）= **6.2791≈6.28**。分解：toy 用垒反射幅 $|R_B|=0.729$ 作回波幅（乐观上界）；strict 用双程穿垒（垒→壁→垒）+真实 PSD。**因 TUFT 频垒顶之上更透，垒透射物理本身不致 6.28×；6.28× 主要=源激发能绝对标度（e/f_π 升层项，OPEN）**。
> **④ ε_strict 复算区间（mpmath dps=40）**：上界（toy/E431 上界）$=0.469746$；下界（E444 真实 PSD 锚）$=0.07481154506795630784624364212457266738931$（$=\varepsilon_{\rm toy}/6.28$）；垒物理独立复算 $=0.469746$（与 toy 同阶，不解释 6.28×）。**本轮最窄区间 $\boxed{\ \varepsilon\in[0.0748115,\ 0.469746]\ }$**（升层不确定度，未闭合）。
> **⑤ D_max 两档表（60 M☉，ρ_dev=1 探测阈，Gpc）**：标定 $L_{O4}=11.993$、$L_{Voy}=52.1371689$（×4.3473）、$\sqrt{1-ov^2}=0.6319612329882268972975604929652052023706$、天线 face-on=1.0000 / edge-on$=\sqrt{1/8}=0.3536$。$D_{\max}\propto\varepsilon$ 线性，故严格=toy/6.28。
>
> | 探测器 | 朝向 | D_toy (Gpc) | D_strict (Gpc) |
> |---|---|---|---|
> | O4 | face-on | 3.5603 | 0.5670 |
> | O4 | edge-on | 1.2587 | 0.2005 |
> | Voyager | face-on | 15.4775 | 2.4649 |
> | Voyager | edge-on | 5.4721 | 0.8715 |
>
> 对照 v47 toy 锚：O4 face-on=3.5603（v47 3.560）、Voy face-on=15.4775（v47 15.48）——**逐位吻合**。Voyager 可测距离 2.46–15.48 Gpc（strict→toy）。
> **⑥ GR 极限核对 PASS**：$\varepsilon\to0\Rightarrow\rho_{\rm frac}=\varepsilon\sqrt{1-ov^2}\to0\Rightarrow$ TUFT-deviation 通道 $D_{\max}\to0$（无可测畸变）；prompt GR 振铃保留（loudness $L=11.993$），纯 GR QNM。$\varepsilon=0\Rightarrow D_{\max}(O4\ face-on)=0.0$ Gpc（退化纯 GR，PASS）。
> **⑦ E503（绝对振幅锚：ε 收窄为区间，数值调查/边界通道登记，不进物理四态）**：绝对振幅锚把 $\varepsilon$ 从单点 0.4697 收窄为区间 $[0.0748,0.4697]$，对应 Voyager 可测距离 2.46–15.48 Gpc；6.28× 不确定度已定位到源激发能 e/f_π 升层项（OPEN），垒透射物理 CONFIRMED（$|T_B|^2=0.2207$/$\varepsilon_{\rm toy}=0.4697$；RW l=2 垒峰独立复算 0.151287@3.2808 与 SSOT 0.148709@3.268 一致 PASS）。四态分级：GR 门 $|R_B|^2@0.3737=0.530254$（SSOT v31/v32，9.1e-8）沿用不伪闭合；垒峰 $V_{\max}$ 独立复算 PASS；$|T_B|^2=0.2207$/$\varepsilon_{\rm toy}=0.4697$ CONFIRMED；$\varepsilon_{\rm strict}\in[0.0748,0.4697]$ ESTIMATED/OPEN（升层不确定度：源激发能 e/f_π 未闭合，本轮只收窄不闭合）；单主模近似明示（E477 仅 n=1，无 M-χ 简并/泛音/多事件/网络正交）。本轮属绝对振幅锚审计通道，**不新增物理 E 数进四态**；**勘误 #42 held（本轮无新勘误）**；物理四态 **35/61/18/27 冻结**。D18 v31 UPGRADE 无回退；联盟层维持 **2/6**、UFT-3 未解锁。open_backlog：源激发能绝对标度仍 OPEN（e/f_π 升层项，6.28× 残余归此升层项未闭合），下一步=闭合源激发能 e/f_π 升层项（绝对振幅锚下界）；垒透射物理已 CONFIRMED，无需重核。本轮合并报告：《TUFT_v53_绝对振幅锚合并报告.md》。
"""

lines = s.split('\n')
assert lines[0].startswith('# TUFT 归一化主册 v6.4'), 'title anchor mismatch: ' + lines[0][:60]
lines[0] = NEW_TITLE

idx = None
for i, ln in enumerate(lines):
    if ln.startswith('> **★★ v6.4（v52 两域三处精修轮收口'):
        idx = i
        break
assert idx is not None, 'v6.4 block anchor not found'

block_lines = V65_BLOCK.strip('\n').split('\n')
new_lines = lines[:idx] + block_lines + [''] + lines[idx:]
out = '\n'.join(new_lines)
io.open(p, 'w', encoding='utf-8', newline='\n').write(out)
print('OK title replaced; v6.4 block was at old index', idx)
print('new total lines', len(new_lines))
print('new total chars', len(out))
