# -*- coding: utf-8 -*-
"""v54 rotating m-split observable: patch master register v6.5 -> v6.6 (append-only)."""
import io, sys

p = r"D:\a10\aikjx\code\my_lib\openuft\01_独立体系\S16_TUFT归一化主册\13_论文与成果\主册\TUFT_归一化主册_v1.0.md"
s = io.open(p, encoding="utf-8").read()

# ---- 1) title line ----
old_title_start = "# TUFT 归一化主册 v6.5（v53 绝对振幅锚轮收口："
new_title = (
"# TUFT 归一化主册 v6.6（v54 旋转 m 频裂观测量轮收口：小自旋线性 ansatz "
"ω(a,m)=ω₀+m·a·c_per_m，δω(a)=ω(a,+2)−ω(a,−2)=4a·c_per_m=a·(splitR/a+i·splitI/a)；"
"GR 基准（勘误#42）c_GR=0.0628831+0.001996i、splitR/a=0.2515323、splitI/a=0.007984；"
"TUFT（v49 a=0.1）splitR/a=1.621、splitI/a=−0.141、c_TUFT=0.40525−0.03525i；"
"观测量 Δf=(c³/2πGM)·a·splitR/a，60M☉ 换算 K=32312.5/60=538.5417 Hz，GR 极限 a=0→δω=0；"
"判别量（诚实符号）0.35 抑制比净效应=TUFT 1.621/同腔 GR 2/ρ³ 4.662=0.3477≈0.35（天真同腔映射频裂被压到 35%），"
"vs 真实 GR 基准 0.2515323：抑制前天真同腔/GR=18.53×、抑制后 TUFT/GR=6.44×——"
"TUFT 预言的 m 频裂不是比 GR 小而是 ~6.44× 更大（0.35 抑制把 18.5× 超额砍到 6.4×）；"
"若测到双 m 模：斜率 ~6.44× GR 偏 TUFT、~1× GR 偏 GR，斜率比无量纲几何比与 M 无关、线性区与 a 无关，"
"方向（正超额）与 v37 EHT c_m 锚一致；数值表（60M☉ Hz）GR a=0.1 208.01/194.46/13.55、"
"TUFT a=0.1 277.62/190.32/87.30（TUFT 静态基频已含 +16.26% 频移/−36.6% 阻尼）；"
"外推标注 a=0.1 在 v49 可信窗 a<0.1 内 CONFIRMED、a=0.2⚠ 外推（v49 直接算 splitR/a=1.569 vs 线性 1.621 约 3.2% 落差 O(a²)~4%）、"
"a=0.3⚠ 进一步外推纯线性仅数量级可信；可探测振幅档 ε_strict [0.0748,0.4697]、"
"Voyager D_max 严格 2.46/玩具 15.48 Gpc，本签名在 loud/玩具档（ε≈0.4697，D_max 至 15.48 Gpc）可分辨、严格档边缘需邻近事件/网络；"
"E504；当前勘误 #42 held【本轮无新勘误】；物理四态 35/61/18/27 冻结；"
"v6.5 绝对振幅锚（ε 区间 [0.0748,0.4697]）、v6.4 两域三处精修、v6.3 鲁棒两域单元、v6.2 Grade-A 静态攻坚、"
"v6.1 Chandrasekhar+镜壁、v6.0 第三独立谱方法诊断裁决不回退）"
)

lines = s.split("\n")
assert lines[0].startswith(old_title_start), "title line anchor mismatch: " + lines[0][:60]
lines[0] = new_title
s = "\n".join(lines)

# ---- 2) insert v6.6 block before the v6.5 block ----
anchor = "> **★★ v6.5（v53 绝对振幅锚轮收口"
assert anchor in s, "v6.5 block anchor not found"

v66_block = (
"> **★★ v6.6（v54 旋转 m 频裂观测量轮收口：TUFT vs GR 斜率比 6.44× / a=0.1 CONFIRMED、a=0.2/0.3 外推 / loud 档可探测，2026-09-26，append-only，本轮最高信号；诚实符号，不伪闭合）**：组织者 v54-A 结果先 Read `_audit_v54_rotating_msplit_observable_out.txt` 核对后照抄（organizer 已核验；另写实现、不 import 任何 prior-project 脚本；GR 门先行；禁伪闭合；mpmath dps=40；数字照抄原始输出）。磁盘起点 **v6.5/E1-E503/勘误#42**，本轮升 **v6.6/E1-E504/勘误#42 held（本轮无新勘误）**；物理四态 **35/61/18/27 冻结**；不回退任何勘误与否定定理——v6.5 绝对振幅锚（ε 区间 [0.0748,0.4697]）、v6.4 两域三处精修、v6.3 鲁棒两域单元、v6.2 Grade-A 静态攻坚、v6.1 Chandrasekhar+镜壁、v6.0 第三独立谱方法诊断裁决维持；本轮为**旋转 m 频裂观测量审计通道**（E504 为观测量判别通道登记，不闭合新物理 E-number 进四态）。\n"
"> **① 频裂求导链（小自旋，O(a) 领头）**：Kerr QNM 慢展开 $\omega(a,m)=\omega_0+m\cdot a\cdot c_{\\rm per\\_m}+O(a^2)$，$\omega_0$ 为静态（a=0）基频、$c_{\\rm per\\_m}$ 为每 $(ma)$ 的拖曳斜率。频裂观测量 $\delta\omega(a)=\omega(a,+2)-\omega(a,-2)=[\omega_0+2ac]-[\omega_0-2ac]=4a\cdot c_{\\rm per\\_m}=a\cdot(\\mathrm{splitR}/a+i\\cdot\\mathrm{splitI}/a)$，其中 $\\mathrm{splitR}/a=4\\,\\mathrm{Re}(c_{\\rm per\\_m})$、$\\mathrm{splitI}/a=4\\,\\mathrm{Im}(c_{\\rm per\\_m})$。**GR 锚（勘误#42）**：$c_{\\rm GR}=0.0628831+0.001996i$，核对 $4\\,\\mathrm{Re}(c)=0.2515324$ vs $\\mathrm{splitR}/a=0.2515323$（舍入吻合），$\\mathrm{splitR}/a=0.2515323$、$\\mathrm{splitI}/a=0.007984$。**TUFT 锚（v49 直接延拓 @a=0.1）**：$c_{\\rm TUFT}=(\\mathrm{splitR}/a+i\\,\\mathrm{splitI}/a)/4=0.40525-0.03525i$，$\\mathrm{splitR}/a=1.621$、$\\mathrm{splitI}/a=-0.141$。**Hz 换算（60 M☉）**：$f_{\\rm Hz}=K\\,\\mathrm{Re}(\\omega)$，$K=32312.5/60=538.5417$ Hz；$\delta f_{\\rm Hz}=K\\cdot a\\cdot\\mathrm{splitR}/a$。双模共享同一 $K(M)$，故斜率比 TUFT/GR 与 M 无关、线性区与 a 无关。**GR 极限（a=0）**：$\omega(a=0,\\pm2)=(0.37367168441804166-0.0889623156889341i)$，$\delta\omega(a=0)=0$——零频裂，GR 门 PASS。\n"
"> **② 数值表（60 M☉，K=538.5417 Hz）**：GR 静态 $w_0=(0.37367168441804166-0.0889623156889341i)$；TUFT 静态 $w_0=(0.434445178-0.05644976i)$（已含 +16.26% 频移/−36.6% 阻尼）。\n"
">\n"
"> | 体系 | a/M | f(+2) Hz | f(−2) Hz | 频裂 Δf Hz | 标注 |\n"
"> |---|---|---|---|---|---|\n"
"> | GR | 0.1 | 208.01 | 194.46 | 13.55 | CONFIRMED |\n"
"> | GR | 0.2⚠ | 214.78 | 187.69 | 27.09 | 外推越出 v49 a<0.1 |\n"
"> | GR | 0.3⚠ | 221.56 | 180.92 | 40.64 | 进一步外推 |\n"
"> | TUFT | 0.1 | 277.62 | 190.32 | 87.30 | CONFIRMED（v49 直接 @a=0.1） |\n"
"> | TUFT | 0.2⚠ | 321.26 | 146.67 | 174.60 | 外推越出 v49 a<0.1 |\n"
"> | TUFT | 0.3⚠ | 364.91 | 103.02 | 261.89 | 进一步外推 |\n"
">\n"
"> **③ 判别量（诚实符号，不伪闭合）**：0.35 抑制比净效应 $=\\mathrm{TUFT}\\ 1.621 /$ 同腔 GR $2/\\rho^3\\ 4.662 = 0.3477\\approx0.35$（天真同腔映射频裂被压到 35%）。对照真实 GR 基准 $0.2515323$：抑制前天真同腔/GR $=18.5344\\times$，抑制后 TUFT/GR $=6.4445\\times$。**诚实符号：TUFT 预言的 m 频裂不是比 GR 小，而是 ~6.44× 更大**（0.35 抑制把 18.5× 超额砍到 6.4×）。⇒ 若测到双 m 模：斜率 ~6.44× GR 偏 TUFT、~1× GR 偏 GR；斜率比为无量纲几何比（与 M 无关、线性区与 a 无关）；方向（正超额）与 v37 EHT $c_m$ 锚方向一致。具体（60 M☉，a=0.1）：GR m=±2 频裂 Δf=13.5461 Hz，TUFT Δf=87.2976 Hz，比=6.4445。\n"
"> **④ 外推标注（v49 可信窗 a/M<0.1）**：a=0.1 在可信窗内（v49 直接 @a=0.1：splitR/a=1.621367）**CONFIRMED**；a=0.2 **⚠ EXTRAPOLATED** 越出 a<0.1——v49 直接 @a=0.2 得 splitR/a=1.569052 vs 线性 1.621 约 3.2% 落差，与 O(a²)~4% 修正一致，表用线性 ansatz 1.621、非线性 O(a²) 不确定度 ~3–4%；a=0.3 **⚠ EXTRAPOLATED** 更进一步，v49 未算，纯线性 ansatz，O(a²) 修正增大、仅数量级可信。\n"
"> **⑤ 可探测振幅档**：本签名=分辨两个分立 m 模，需高 SNR 分离 f(+2)/f(−2)。$\varepsilon_{\\rm strict}$ 区间 $[0.0748115,\\ 0.469746]$；Voyager $D_{\\max}$：strict $\varepsilon=0.07481\\to2.46$ Gpc，toy $\varepsilon=0.46975\\to15.48$ Gpc。⇒ 在 **loud/玩具档**（$\varepsilon\\approx0.4697$，$D_{\\max}$ 至 15.48 Gpc，face-on）SNR 足够分离 m=+2/m=−2，可分辨；在 **strict 档**（$\varepsilon=0.0748$，2.46 Gpc）频裂 MARGINAL，需邻近事件/网络，与 D_max 两档并列作为 loud 档通道。\n"
"> **⑥ 四态分级**：**CONFIRMED**（a=0 零频裂 GR 门、静态锚 $w_0$ 照抄、GR 斜率 splitR/a=0.2515323 勘误#42、TUFT 斜率 @a=0.1=1.621）；**ESTIMATED**（0.35 抑制比净效应=腔映射依赖、判别比 6.44× GR）；**EXTRAPOLATED**（a=0.2/a=0.3 线性 ansatz 越出 v49 a<0.1，O(a²)~3–4%）；**GATE-HELD**（可探测档锚定 v53 ε 区间/D_max；无新物理 E 数闭合）。勘误 #42 **held**（本轮无新勘误）；物理四态 **35/61/18/27 冻结**。\n"
"> **⑦ E504（旋转 m 频裂观测量：TUFT vs GR 斜率比 6.44×，a=0.1 CONFIRMED，a=0.2/0.3 外推，loud 档可探测）**：小自旋线性 ansatz 把旋转 QNM 频裂落成观测量 $\Delta f=(c^3/2\\pi GM)\\cdot a\\cdot\\mathrm{splitR}/a$；GR 基准（勘误#42）splitR/a=0.2515323、TUFT（v49 a=0.1）splitR/a=1.621；经 0.35 同腔抑制后 TUFT/GR=6.44×（诚实符号：TUFT 频裂比 GR 更大，非更小）；双 m 模斜率比 ~6.44× GR 偏 TUFT、~1× 偏 GR，无量纲几何比与 M/a 无关；a=0.1 CONFIRMED、a=0.2/0.3 线性外推仅数量级可信；本签名在 loud/玩具档（ε≈0.4697，Voyager D_max 至 15.48 Gpc）可分辨、strict 档边缘。本轮属旋转观测量判别通道，**不新增物理 E 数进四态**；**勘误 #42 held（本轮无新勘误）**；物理四态 **35/61/18/27 冻结**。D18 v31 UPGRADE 无回退；联盟层维持 **2/6**、UFT-3 未解锁。open_backlog：TUFT 静态 11.6 位硬门仍 OPEN（8.4 位/<1e-6 已达，两域 assembly 未过 GR 门 B）；旋转绝对值 1.62 仍无外部 Grade-A 锚（仅 v54 内部互证，稳健量=0.35 抑制比/6.44× 判别比）；a≥0.2 慢转一阶渐近失真（O(a²)~3–4%）；源激发能 e/f_π 升层项仍 OPEN（继承 v6.5）。下一步=多事件/网络分辨双 m 模斜率比（loud 档），并待两域静态硬门闭合后用 dps=50 重核旋转绝对值。本轮合并报告：《TUFT_v54_旋转m频裂合并报告.md》。\n\n"
)

s = s.replace(anchor, v66_block + anchor, 1)

io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("MASTER PATCH OK; new len =", len(s))
print("v6.6 present:", "主册 v6.6" in s or "v6.6（v54" in s)
print("E504 present:", "E504" in s)
