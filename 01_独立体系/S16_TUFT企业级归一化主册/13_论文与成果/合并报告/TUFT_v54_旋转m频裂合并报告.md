# TUFT v54 旋转 m 频裂观测量轮合并报告

- **轮次**：v6.6 / v54（旋转 m 频裂观测量审计通道）
- **日期**：2026-09-26
- **磁盘起点**：v6.5 / E1–E503 / 勘误 #42 held / 物理四态 35/61/18/27
- **本轮升版**：v6.6 / E1–E504 / 勘误 #42 **held（本轮无新勘误）** / 物理四态 **35/61/18/27 冻结**
- **铁律**：append-only；禁伪闭合；四态分级；勘误递增不回退；不回退任何否定定理；数字照抄 `_audit_v54_rotating_msplit_observable_out.txt`（organizer 已核验）。
- **备份**：主册/台账/ch66/章节账本/流程图均已备份为 `*.v66pre_20260926.bak`。

---

## 1. 频裂求导链（小自旋，O(a) 领头）

Kerr QNM 慢展开：

$$\omega(a,m)=\omega_0+m\cdot a\cdot c_{\rm per\_m}+O(a^2)$$

其中 $\omega_0$ 为静态（a=0）基频，$c_{\rm per\_m}$ 为每 $(ma)$ 的拖曳斜率。

频裂观测量（m=+2 与 m=−2 之差）：

$$\delta\omega(a)=\omega(a,+2)-\omega(a,-2)=[\omega_0+2ac]-[\omega_0-2ac]=4a\cdot c_{\rm per\_m}=a\cdot(\mathrm{splitR}/a+i\cdot\mathrm{splitI}/a)$$

- $\mathrm{splitR}/a=4\,\mathrm{Re}(c_{\rm per\_m})$
- $\mathrm{splitI}/a=4\,\mathrm{Im}(c_{\rm per\_m})$

**GR 基准（勘误 #42 锚）**：$c_{\rm GR}=0.0628831+0.001996i$；核对 $4\,\mathrm{Re}(c)=0.2515324$ vs $\mathrm{splitR}/a=0.2515323$（舍入吻合）；$\mathrm{splitR}/a=0.2515323$、$\mathrm{splitI}/a=0.007984$。

**TUFT 锚（v49 直接延拓 @a=0.1）**：$c_{\rm TUFT}=(\mathrm{splitR}/a+i\,\mathrm{splitI}/a)/4=0.40525-0.03525i$；$\mathrm{splitR}/a=1.621$、$\mathrm{splitI}/a=-0.141$。

**Hz 换算（60 M☉）**：$f_{\rm Hz}=K\,\mathrm{Re}(\omega)$，$K=32312.5/60=538.5417$ Hz；$\delta f_{\rm Hz}=K\cdot a\cdot\mathrm{splitR}/a$。双模共享同一 $K(M)$，故斜率比 TUFT/GR 与 M 无关、线性区与 a 无关。

**GR 极限（a=0）**：$\omega(a=0,\pm2)=(0.37367168441804166-0.0889623156889341i)$，$\delta\omega(a=0)=0$——零频裂，GR 门 PASS。

---

## 2. 数值表（60 M☉，K=538.5417 Hz）

GR 静态 $w_0=(0.37367168441804166-0.0889623156889341i)$；TUFT 静态 $w_0=(0.434445178-0.05644976i)$（已含 +16.26% 频移/−36.6% 阻尼）。

| 体系 | a/M | f(+2) Hz | f(−2) Hz | 频裂 Δf Hz | 标注 |
|---|---|---|---|---|---|
| GR | 0.1 | 208.01 | 194.46 | 13.55 | CONFIRMED |
| GR | 0.2⚠ | 214.78 | 187.69 | 27.09 | 外推越出 v49 a<0.1 |
| GR | 0.3⚠ | 221.56 | 180.92 | 40.64 | 进一步外推 |
| TUFT | 0.1 | 277.62 | 190.32 | 87.30 | CONFIRMED（v49 直接 @a=0.1） |
| TUFT | 0.2⚠ | 321.26 | 146.67 | 174.60 | 外推越出 v49 a<0.1 |
| TUFT | 0.3⚠ | 364.91 | 103.02 | 261.89 | 进一步外推 |

---

## 3. 判别量（诚实符号，不伪闭合）

- **0.35 抑制比净效应** $=\mathrm{TUFT}\ 1.621/$ 同腔 GR $2/\rho^3\ 4.662=0.3477\approx0.35$（天真同腔映射频裂被压到 35%）。
- 对照真实 GR 基准 $0.2515323$：
  - 抑制前天真同腔/GR $=18.5344\times$
  - 抑制后 TUFT/GR $=6.4445\times$

**诚实符号：TUFT 预言的 m 频裂不是比 GR 小，而是 ~6.44× 更大**（0.35 抑制把 18.5× 超额砍到 6.4×）。

⇒ 若测到双 m 模：斜率 ~6.44× GR 偏 TUFT、~1× GR 偏 GR；斜率比为无量纲几何比（与 M 无关、线性区与 a 无关）；方向（正超额）与 v37 EHT $c_m$ 锚方向一致。

具体（60 M☉，a=0.1）：GR m=±2 频裂 Δf=13.5461 Hz，TUFT Δf=87.2976 Hz，比=6.4445。

---

## 4. 外推标注（v49 可信窗 a/M<0.1）

| a/M | 等级 | 依据 |
|---|---|---|
| 0.1 | **CONFIRMED** | 在 v49 可信窗 a<0.1 内；v49 直接 @a=0.1 splitR/a=1.621367 |
| 0.2⚠ | **EXTRAPOLATED** | 越出 a<0.1；v49 直接 @a=0.2 splitR/a=1.569052 vs 线性 1.621 约 3.2% 落差，与 O(a²)~4% 一致；表用线性 ansatz 1.621，非线性 O(a²) 不确定度 ~3–4% |
| 0.3⚠ | **EXTRAPOLATED** | 更进一步，v49 未算，纯线性 ansatz；O(a²) 修正增大、仅数量级可信 |

---

## 5. 可探测振幅档

本签名=分辨两个分立 m 模，需高 SNR 分离 f(+2)/f(−2)。

- $\varepsilon_{\rm strict}$ 区间 $[0.0748115,\ 0.469746]$
- Voyager $D_{\max}$：strict $\varepsilon=0.07481\to2.46$ Gpc；toy $\varepsilon=0.46975\to15.48$ Gpc

⇒ 在 **loud/玩具档**（$\varepsilon\approx0.4697$，$D_{\max}$ 至 15.48 Gpc，face-on）SNR 足够分离 m=+2/m=−2，**可分辨**；在 **strict 档**（$\varepsilon=0.0748$，2.46 Gpc）频裂 MARGINAL，需邻近事件/网络，与 D_max 两档并列作为 loud 档通道。

---

## 6. 四态分级

| 四态 | 内容 |
|---|---|
| **CONFIRMED** | a=0 零频裂 GR 门；静态锚 $w_0$ 照抄；GR 斜率 splitR/a=0.2515323（勘误 #42）；TUFT 斜率 @a=0.1=1.621 |
| **ESTIMATED** | 0.35 抑制比净效应=腔映射依赖；判别比 6.44× GR |
| **EXTRAPOLATED** | a=0.2/a=0.3 线性 ansatz 越出 v49 a<0.1（O(a²)~3–4%） |
| **GATE-HELD** | 可探测档锚定 v53 ε 区间/D_max；无新物理 E 数闭合 |

物理四态计数 **35/61/18/27 冻结**。E504 为观测量判别通道登记，不进物理四态。

---

## 7. 未决项（open_backlog 继承）

1. TUFT 静态 11.6 位硬门仍 OPEN（8.4 位/<1e-6 已达，两域 assembly 未过 GR 门 B；v52 GR 门 B 仅 1.05 位 FAIL）。
2. 旋转绝对值 1.62 仍无外部 Grade-A 锚（本轮仅 v54 内部互证；稳健量=0.35 抑制比/6.44× 判别比）。
3. a≥0.2 慢转一阶渐近失真（O(a²)~3–4%）。
4. 源激发能 e/f_π 升层项仍 OPEN（继承 v6.5/v53 6.28× 残余）。
5. 下一步：多事件/网络分辨双 m 模斜率比（loud 档）；待两域静态硬门闭合后用 dps=50 重核旋转绝对值。

---

## 8. 勘误

- 本轮 **无新勘误**；勘误 #42（GR splitR/a 锚）**held**，不回退。

---

## 9. 文件清单

| 文件 | 动作 |
|---|---|
| `TUFT_企业级归一化主册_v1.0.md` | 升 v6.5→v6.6；标题行改写；插入 v54 旋转 m 频裂摘要块（①–⑦）+ E504 + D18/联盟层/open_backlog |
| `TUFT_归一化台账_v1.0.json` | version/latest_round/date/equation_range 升 v6.6/E1-E504；新增 `v54_rotating_msplit_key_results`；open_backlog 前置 v54 条目；四态 note 追加 v54；json.load 复验合法 |
| `openuft/.../第十二编.../第66章_复谱GradeA_TUFT基频极点与两路互证.md` | append §66.17（66.17.1–66.17.6），先读再写不覆盖 |
| `openuft/.../第十二编.../_章节账本.md` | ch66 len 实测 35071→39492；metadata 表补 66.16/66.17；核心结论补 §66.16/§66.17；合计 118328→122749；文末 append v54 记录 |
| `TUFT_全物理现象关系流程图.html` | 新增 v54 m 频裂框（.ok 绿，6.44×/a=0.1 CONFIRMED/a=0.2/0.3 外推）；版本脚升 v6.6/E1-E504；因果链补 v54 段 |
| `_audit_v54_rotating_msplit_observable_out.txt` | 只读核对（数字照抄源） |
| `TUFT_v54_旋转m频裂合并报告.md` | 本报告 |

除上述目标文件外只读；未删任何已记录勘误；未回退任何否定定理。
