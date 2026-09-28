# -*- coding: utf-8 -*-
import io

p = r'D:\a10\aikjx\code\my_lib\openuft\01_独立体系\S16_TUFT归一化主册\13_论文与成果\主册\TUFT_归一化主册_v1.0.md'
s = io.open(p, encoding='utf-8').read()

NEW_TITLE = (
"# TUFT 归一化主册 v6.4（v52 两域三处精修轮收口：在 v51 两域 assembly 上做三处精修——"
"未知向量分块 u=[G1(0..p1-1)|G2(1..p2e-1)]、Q(ω)=Q0+ωQ1、row0 壁正则改 ChebU 内部节点外推（不占插值节点）、"
"R1 界面 C1 行替换域 A 界面 PDE 行（C0 折叠后 C1 化为 w 无关约束 G1′−G2′/F1+(F1′/F1)G1=0，只进 Q0、Q1 全零行，改用 scipy.linalg.eig(-Q0,Q1) 容忍奇异 Q1）、域 B 行 C0 折叠回投、远场 e=+1 节点丢弃；"
"GR 门 A 独立 Leaver 14.8 位 PASS 作对照锚；但 GR 门 B（同一两域 assembly 配 Schwarzschild RW）仅 1.05 位 FAIL（err~9e-2 不随分辨率下降）——"
"两域 assembly 本身尚未通过 GR 复现门，TUFT 数值不可采信；"
"TUFT 三路扫描关键负面：显式 C1 行与任务假设相反，C1_on=TRUE 把 Beyn 从锚附近 0.436−0.055i 推离到错误极点 0.262+0.029i，C1_on=FALSE（v51 式界面 PDE 行）反而贴锚；Q1 零行重现（Q1zr=1）；N/p 非单调乱跳；"
"11.6 位硬门 RED 仍未达，无新权威基频，既有 Grade A 锚 0.434445178−0.056449760i 仍最高权威；"
"E502；当前勘误 #42 held【本轮无新勘误】；物理四态 35/61/18/27 冻结；"
"v6.3 鲁棒两域单元、v6.2 Grade-A 静态攻坚、v6.1 Chandrasekhar+镜壁、v6.0 第三独立谱方法诊断裁决不回退）"
)

V64_BLOCK = r"""
> **★★ v6.4（v52 两域三处精修轮收口：GR 门 B 仅 1.05 位 FAIL / 显式 C1 行反退化 / Q1 零行重现，2026-09-25，append-only，本轮最高信号；诚实 RED，不伪闭合）**：组织者 v52-A 结果先 Read `_audit_v52_twodomain_refine_out.txt` 核对后照抄（organizer 已核验；独立再实现两域三处精修、**不 import v51/v50**；mpmath dps=55；粗糙起步、无循环标定；数字照抄原始输出）。磁盘起点 **v6.3/E1-E501/勘误#42**，本轮升 **v6.4/E1-E502/勘误#42 held（本轮无新勘误）**；物理四态 **35/61/18/27 冻结**；不回退任何勘误与否定定理——v6.3“主卡点=C1 导数连续未显式成行，下一步=显式 C1 行（Q0-only）+ Gauss-Chebyshev 壁内部节点”正是本轮要验的假设，本轮做了该假设但结果与预期相反（见④负面），v6.2 Grade-A 静态攻坚、v6.1 Chandrasekhar+镜壁、v6.0 第三独立谱方法诊断裁决维持。
> **① 两域 assembly 矩阵块结构（三处精修）**：未知向量分块 $u=[G_1(0..p_1-1)\,|\,G_2(1..p_{2e}-1)]$（域 B 远场 $e=+1$ 节点丢弃，故 $G_2$ 从 1 起）；二次 pencil $Q(\omega)=Q_0+\omega Q_1$。row0 壁正则改 ChebU 内部节点外推（Chebyshev-U 内部节点，不占插值节点），条件 $G_1'(s_w)+i\omega G_1(s_w)=0$；域 A PDE 内点行；**R1 界面 C1 行**替换域 A 界面 PDE 行——C0 折叠后 C1 化为 $w$ 无关约束 $G_1'-G_2'/F_1+(F_1'/F_1)G_1=0$，只进 $Q_0$、$Q_1$ 全零行（故改 scipy.linalg.eig$(-Q_0,Q_1)$ 容忍奇异 $Q_1$）；域 B 行 C0 折叠回投；远场 $e=+1$ 节点丢弃。
> **② GR 门 A（独立 Leaver）PASS**：$w=0.373671684418041827-0.088962315688935700i$，$|\mathrm{err}|=1.605\times10^{-15}$，**14.8 位 PASS**（验证 dps=55 高精度实现本身正确，作对照锚）。近壁 $U_{-2}=-1.346\times10^{-1}$、$U_{-1}=3.772\times10^{-2}$、$U_0=3.220\times10^{-2}$、$U_1=1.354\times10^{-2}$、$U_2=2.978\times10^{-3}$，$a_{16}=8.144\times10^{-14}$ Frobenius 衰减良好。
> **③ GR 门 B（同一两域 assembly 配 Schwarzschild RW）FAIL（诊断性硬伤）**：$s_1=2.0$ $p_1=24$ $p_2=36$ $L_t=30$：$w=0.31637214736068-0.16308697894661i$，$|\mathrm{err}|=9.369\times10^{-2}$（1.03 位）；$s_1=2.0$ $p_1=32$ $p_2=48$ $L_t=40$：$w=0.31775666320125-0.15964717461469i$，$|\mathrm{err}|=9.013\times10^{-2}$（**1.05 位**）；$s_1=3.0$ $p_1=32$ $p_2=48$ $L_t=40$：$w=0.31300620388456-0.15778920655484i$，$|\mathrm{err}|=9.175\times10^{-2}$（1.04 位）。**GR 门 B FAIL（最佳 1.05 位）**。残差定位=非远场截断（$L_t$ 30→40 不收敛）、非壁行符号（$c=\pm2$ 都不浮现 $n_0$），判为**界面 C0/C1 匹配块 + pencil 离散残差**；两域 assembly 本身尚未通过 GR 复现门，**TUFT 数值不可采信**。
> **④ TUFT 三路扫描（关键负面——显式 C1 行与任务假设相反）**：chebu 壁、$t_1=0.15$。**R1 C1 行 ON vs OFF**：C1_on=TRUE $p_1=32$ $p_2=48$ Q1zr=1 Beyn$=0.261828886+0.028714146i$ / GEP$=0.421116195-0.028409396i$ $|\mathrm{diff}|=1.69\times10^{-1}$；C1_on=FALSE（v51 式界面 PDE 行）Q1zr=0 Beyn$=0.436003802-0.055416780i$ / GEP$=0.438807281-0.010986505i$ $|\mathrm{diff}|=4.45\times10^{-2}$。**显式 C1 行把 Beyn 从锚附近 $0.436-0.055i$ 推离到错误极点 $0.262+0.029i$**——与 v6.3“下一步=显式 C1 行”的假设相反；v51 式界面 PDE 行反而贴锚。**R2 壁节点**：node=chebu 同上（diff=1.69e-1），node=lobatto FAIL（异常）。**R3 远场截断 $L_t$**（chebu、C1 on）：$L_t=4$ Beyn$=0.258245800-0.021134518i$ GEP$=0.451001034-0.038999446i$ diff=1.94e-1；$L_t=6$ Beyn$=0.261828886+0.028714146i$ GEP$=0.421116195-0.028409396i$ diff=1.69e-1；$L_t=8$ Beyn$=0.310271445+0.017538302i$ GEP$=0.418060396-0.025855782i$ diff=1.16e-1；near-spur $0.44+0.008i$ 均 NONE（但因 Beyn 已漂移到错误极点，非真清除）。**N/p 单调性**（chebu、C1 on、$L_t=6$）：$p_1=20\to0.371652934+0.020827668i$、$p_1=28\to0.225856496+0.058251208i$、$p_1=36\to0.359929941-0.013523677i$、$p_1=44\to0.362922160-0.097073638i$——**非单调乱跳**。
> **⑤ 是否达 11.6 位：否（RED）**。GR 门 B 仅 1.05 位，TUFT 互证最佳 ~1.35 位（C1 off，diff=4.45e-2），N/p 不单调。**无新权威基频**；既有 Grade A 锚 $0.434445178-0.056449760i$ 仍为最高权威。
> **⑥ 卡点（如实，不伪闭合）**：第一障碍=两域 assembly 的界面 C0/C1 匹配块连 Schwarzschild $n_0$ 都复现不到 11.6 位（err~9e-2 不随分辨率下降）；在该块通过 GR 门之前，任何 TUFT 高声明都不成立。次负面=显式 C1 行反退化（C1_on=TRUE 把 Beyn 推离锚）、Q1 零行重现（Q1zr=1）。下一轮建议=冻结 R1（回退 C1_on=FALSE），聚焦诊断界面匹配块的雅可比/折叠系数与端点外推病态；或回退单域 Beyn（v50 9 位）作基线。旋转侧未做，$\mathrm{splitR}/a=1.621367$ 仍暂挂。
> **⑦ E502（门/方法学通道）**：两域三处精修——GR 门 B 仅 1.05 位 FAIL（两域 assembly 界面匹配块连 Schwarzschild n0 都复现不到 11.6 位，err~9e-2 不随分辨率下降），显式 C1 行反退化（C1_on=TRUE 把 Beyn 从锚附近推离到错误极点），Q1 零行重现，两域 assembly 界面匹配块为第一障碍，**11.6 位硬门仍 OPEN**。本轮属门/方法学通道，**不新增物理 E 数进四态**；E502 不进物理四态；**勘误 #42 held（本轮无新勘误）**；物理四态 **35/61/18/27 冻结**。D18 v31 UPGRADE 无回退；联盟层维持 **2/6**、UFT-3 未解锁。open_backlog：11.6 位静态硬门仍 OPEN（RED；两域 assembly 未过 GR 门 B 仅 1.05 位，TUFT 数值不可采信），下一步=冻结 R1 回退 C1_on=FALSE、诊断界面匹配块雅可比/折叠系数与端点外推病态，或回退单域 Beyn（v50 9 位）作基线。本轮合并报告：《TUFT_v52_两域精修合并报告.md》。
"""

lines = s.split('\n')
assert lines[0].startswith('# TUFT 归一化主册 v6.3'), 'title anchor mismatch: ' + lines[0][:60]
lines[0] = NEW_TITLE

idx = None
for i, ln in enumerate(lines):
    if ln.startswith('> **★★ v6.3（v51 鲁棒两域单元轮收口'):
        idx = i
        break
assert idx is not None, 'v6.3 block anchor not found'

block_lines = V64_BLOCK.strip('\n').split('\n')
new_lines = lines[:idx] + block_lines + [''] + lines[idx:]
out = '\n'.join(new_lines)
io.open(p, 'w', encoding='utf-8', newline='\n').write(out)
print('OK title replaced; v6.3 block was at old index', idx)
print('new total lines', len(new_lines))
