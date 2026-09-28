# -*- coding: utf-8 -*-
import io, sys

p = r'D:\a10\aikjx\code\my_lib\openuft\01_独立体系\S16_TUFT归一化主册\13_论文与成果\主册\TUFT_归一化主册_v1.0.md'
s = io.open(p, encoding='utf-8').read()

NEW_TITLE = (
"# TUFT 归一化主册 v6.3（v51 鲁棒两域单元轮收口：独立重写两域 assembly（不 import v50/v49，mpmath dps=55），"
"**v50 Q1 界面奇异工程修复 PASS**——C0 不写成行（共享界面节点消元折叠）、界面行改域 A 侧 PDE 残差（非零 Q1=i·2gA·D）、"
"壁正则改 G′(0)+iw·G(0)=0、Q1 对角补 W0=2F′/F，实测 Q1 zero rows=0（v50 秩亏全零行消除）；"
"GR 门 A 独立 Leaver 0.373671684418041827−0.088962315688935700i、|err|=1.605e-15（14.8 位 PASS 作对照锚）；"
"但 TUFT 两域 Beyn↔GEP 扫描互证仅 ~1 位（diff 1e-2~4e-1，最佳 p1=32/p2=48 Beyn=0.43157−0.05730i |da|=3e-3 / 2.5 位，"
"GEP 偏到 0.44+0.008i 伪特征值，p1=40 不单调）——**11.6 位硬门 RED 仍未达，无新权威基频**；"
"主卡点=C1 导数连续未显式成行（靠两侧 PDE 谱收敛驱动、界面导数跳变代数衰减），Beyn 捞到随 p 漂移伪模簇；"
"次卡点=域 B 近无穷远截断 L_t=6 远场出射波收敛未验证；"
"下一步=界面显式 C1 行（Q0-only）替换域 A 界面 PDE 行+域 A 壁节点改 Gauss-Chebyshev 内部节点；"
"E1-E501；当前勘误 #42 held【本轮无新勘误】；物理四态 35/61/18/27 冻结；"
"v6.2 Grade-A 静态攻坚、v6.1 Chandrasekhar+镜壁、v6.0 第三独立谱方法诊断裁决不回退）"
)

V63_BLOCK = """\
> **★★ v6.3（v51 鲁棒两域单元轮收口：Q1 界面奇异工程修复 PASS / TUFT 两域 RED 仅 ~1 位互证，2026-09-25，append-only，本轮最高信号；诚实分级，不伪闭合）**：组织者 v51-A 结果先 Read `_audit_v51_twodomain_out.txt` 核对后照抄（organizer 已核验；独立重写两域 assembly、**不 import v50/v49**；mpmath dps=55；粗糙起步、无循环标定）。磁盘起点 **v6.2/E1-E500/勘误#42**，本轮升 **v6.3/E1-E501/勘误#42 held（本轮无新勘误）**；物理四态 **35/61/18/27 冻结**；不回退任何勘误与否定定理——v6.2“瓶颈=近壁层两域离散（P(s) peel 限贴壁面板、界面 C0/C1 匹配 Q1 奇异未解）”正是本轮要攻的对象，v6.1 Chandrasekhar+镜壁、v6.0 第三独立谱方法诊断裁决维持。
> **① 两域求导链**：Jansen tortoise 波方程 $\\psi''+[w^2-V(s)]\\psi=0$，$s=b\\cdot t$（Jansen tortoise，$b=3.5+1.5i$）；贴壁域 A（聚壁映射，$\\psi=F_1(s)e^{iws}G_1$，$F_1=s^\\beta P(s)$，$P=\\sum a_k s^{k\\mu}$，$\\mu=2/3$，$K=16$，$a_{16}=8.144\\times10^{-14}$ Frobenius 衰减良好）；远场域 B（Lobatto 丢 $e=+1$ 无穷远节点，$\\psi=e^{iws}G_2$）；界面 C0 折叠 $G_2[0]=F_1(s_1)\\cdot G_1[p_1-1]$。块结构：row0 壁正则 $G_1'(0)+iw\\cdot G_1(0)=0$（$Q_0=g_A\\cdot D$，$Q_1=j@[0,0]$）；rows 1..p1−1 域 A PDE；rows p1.. 域 B PDE+折叠耦合列。几何 $\\rho_h=0.609901951359$、$\\beta=1.263762615826$、$B_{\\rm opt}=3.500+1.500i$；近壁 $U_{-2}=-1.346\\times10^{-1}$、$U_{-1}=3.772\\times10^{-2}$、$U_0=3.220\\times10^{-2}$、$U_1=1.354\\times10^{-2}$、$U_2=2.978\\times10^{-3}$。
> **② Q1 界面奇异根因与修复（工程 PASS）**：v50 把 C0/C1 都写成显式行，C1 行 $Q_1$ 部分 $i(F_1G_1-G_2)$ 正是 C0 条件本身，与 C0 行重复/秩亏→全零 $Q_1$ 行。修复=C0 不写成行（共享界面节点消元折叠），界面行是域 A 侧 PDE 残差（带非零 $Q_1=i\\cdot 2g_A\\cdot D$）；实测 **Q1 zero rows=0**（v50 奇异已解）；另修壁正则条件 $G'(0)+iw\\cdot G(0)=0$（非 $G'(0)=0$）、$Q_1$ 对角补 $W_0=2F'/F$。
> **③ GR 门 A（独立 Leaver）PASS**：$w=0.373671684418041827-0.088962315688935700i$，$|\\mathrm{err}|=1.605\\times10^{-15}$，**14.8 位 PASS**（验证 dps=55 两域 assembly 机器本身正确，作对照锚）。GR 门 B（两域 assembly 配 Schwarzschild 势）未做——两域 TUFT 侧尚未收敛，先不拿未验证 assembly 跑 GR 复现。
> **④ TUFT 两域收敛扫描（Beyn vs 直接 GEP，$p_1\\times p_2\\times t_1$）**：$t_1=0.08$ $p_1=16$ $p_2=24$ Beyn$=0.45099+0.01417i$ / GEP$=0.44259+0.00815i$ $|\\mathrm{diff}|=1.0\\times10^{-2}$；$p_1=24$ $p_2=48$ Beyn$=0.2800-0.0894i$ / GEP$=0.4387-0.0112i$ $|\\mathrm{diff}|=1.8\\times10^{-1}$；$p_1=32$ $p_2=48$ Beyn$=0.3634+0.0159i$ / GEP$=0.4387-0.0112i$ $|\\mathrm{diff}|=8.0\\times10^{-2}$；$t_1=0.15$ $p_1=32$ $p_2=48$ Beyn$=0.43157-0.05730i$ / GEP$=0.43881-0.01099i$ $|\\mathrm{diff}|=4.7\\times10^{-2}$；$p_1=40$ $p_2=60$ Beyn$=0.43662-0.05124i$。锚点$=0.434445178-0.056449760i$。最佳单配置 $p_1=32/p_2=48$ Beyn$=0.43157-0.05730i$（$|da|=3\\times10^{-3}$，**2.5 位**），但 GEP 偏到 $0.44+0.008i$ 方向，两路仅 ~1 位互证，$p_1=40$ 不单调。
> **⑤ 是否达 11.6 位：未达（RED）**。两路互证 ~1 位，无新权威基频。
> **⑥ 卡点（如实，不伪闭合）**：主卡点=C1 导数连续未显式成行，靠两侧 PDE 谱收敛驱动，界面导数跳变代数衰减；Beyn 捞到随 $p$ 漂移的伪模簇，非干净极点。次卡点=域 B 近无穷远截断 $L_t=6$ 是否够远场出射波收敛未验证，GEP 常被 ~$0.44+0.008i$ 伪特征值吸引。下一步=界面显式加 C1 行（Q0-only）替换域 A 界面 PDE 行，域 A 壁节点改 Gauss-Chebyshev 内部节点消除壁 BC 误差源，再重扫。旋转侧未做（时间被两域调试占满），$\\mathrm{splitR}/a=1.621367$ 暂挂。
> **⑦ E501（门/方法学通道）**：鲁棒两域单元——Q1 界面奇异已解（工程 PASS，zero rows=0），C1 导数连续未显式成行致两路仅 ~1 位互证，11.6 位硬门仍 OPEN。本轮属门/方法学通道，**不新增物理 E 数进四态**；E501 不进物理四态；**勘误 #42 held（本轮无新勘误）**；物理四态 **35/61/18/27 冻结**。D18 v31 UPGRADE 无回退；联盟层维持 **2/6**、UFT-3 未解锁。open_backlog：11.6 位静态硬门仍 OPEN（RED；Q1 奇异已工程修复但两域互证仅 ~1 位），下一步=显式 C1 行（Q0-only）+ Gauss-Chebyshev 壁内部节点。本轮合并报告：《TUFT_v51_鲁棒两域合并报告.md》。
"""

lines = s.split('\n')
assert lines[0].startswith('# TUFT 归一化主册 v6.2'), 'title anchor mismatch: ' + lines[0][:60]
# replace title line
lines[0] = NEW_TITLE
# find the v6.1 block start (first line starting with '> **★★ v6.1')
idx = None
for i, ln in enumerate(lines):
    if ln.startswith('> **★★ v6.1（v49 Chandrasekhar'):
        idx = i
        break
assert idx is not None, 'v6.1 block anchor not found'
# insert V63_BLOCK lines right before idx, with a blank line separation.
# current layout: lines[0]=title, lines[1]='', lines[2]=v6.1...
# We want: title, '', V63_BLOCK..., '', v6.1...
block_lines = V63_BLOCK.rstrip('\n').split('\n')
new_lines = lines[:idx] + block_lines + [''] + lines[idx:]
out = '\n'.join(new_lines)
io.open(p, 'w', encoding='utf-8', newline='\n').write(out)
print('OK title replaced; v6.1 block was at old index', idx)
print('new total lines', len(new_lines))
