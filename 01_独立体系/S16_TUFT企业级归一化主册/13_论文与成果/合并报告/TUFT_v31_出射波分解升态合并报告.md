# TUFT v31 解析出射波分解升态合并报告

> **SSOT 权威口径**：version=**v4.3** ／ latest_round=**v31_exiting_wave_upgrade** ／ E 范围=**E1–E476** ／ 勘误=**#41（本轮无新勘误）** ／ 物理四态=**35/61/18/27 冻结**。
> 编制：MainAgent（organizer 已核验；脚本 `_audit_v31_exiting_wave.py`，原始输出 `_audit_v31_exiting_wave_out.txt` 数字照抄；同一 IVP=DOP853 双精度、不 import 联盟、粗糙初值、从零写；墙钟 554.3s）。
> 严格区 cm=−0.29 / d=−0.05 / ρ_h=0.609902 / β=1.263762616 / K_ASC=9.56991e-2；谱锚（仅参考）w0=0.43444518 / γ=0.05644976 / Q=3.848；Blaschke 参考（v28）|Im p|=0.056724。
> 铁律：以磁盘最新 SSOT 为准（开工前重读头部：v4.2 / E1–E475 / 勘误 #41）；禁止回退任何勘误与否定定理；只做无冲突增量；数字照抄原始输出。

---

## 1. GR 门（RW l=2，解析分解）——PASS

| 量 | 值 | 判定 |
|---|---|---|
| \|R\|²@0.3737 | **0.530254**（靶 0.531，\|d\|=7.46e-4） | PASS |
| N 三值（1e5/2e5/4e5）spread | **1.1e-3** | PASS |
| cross-b（收敛端 s_hi≥500）spread | **9.09e-8** | ≤1e-7 ✓ |
| 峰位 w（bump） | w=0.3756（bump=14.66） | PASS |

## 2. 解析出射波分解形式（本轮核心方法学）

- 远尾 **V(s) ~ c_tail/s²**；局域 **k(s)=√(w²−V)**；WKB 渐近相位 **Φ = ws + φ_tail**（V=c/s² **精确积分**，非一阶近似 c/(2ws)）。
- 外端按 **a·e^{−iΦ} + b·e^{+iΦ}** 分解，**R = b/a 与 s_hi 无关**。
- v30 自由基 e^{±iws_hi} 带 **e^{+ic/(ws_hi)} 漂移相位**（1/w，非多项式）——这正是 §67.11 遗留的"跨 s_end 数值相位漂移"根因；本轮解析分解将其移除。

## 3. 三 spread 全 <1e-3（冲门成功）

| 门 | 量 | 值 | 判定 |
|---|---|---|---|
| ① HWHM | \|g−0.056724\|（g=0.055802） | **9.22e-4** | ✓ <1e-3 |
| ② g over s_end | spread | **1.92e-6** | ✓ <1e-3 |
| ③ Re(w0) over s_end | spread | **4.72e-5** | ✓ <1e-3（v30 为 6.9e-3） |

- 1/s_end 外推 **g_inf=0.055337**（|d| vs Blaschke=1.39e-3）；Blaschke tight g=0.056853（|d|=1.3e-4）交叉对照。
- 附注：左翼从 w≤0.15（1 点退化）扩到 w≤0.20（16 点）是门①通过的直接原因；c_tail 6.0–8.0 不影响 g。

## 4. Zerilli 跨对象——CONSISTENT

- Zerilli even-parity l=2：|R|²=**0.530206** vs RW 0.530254（|d|=**4.78e-5**）。
- 峰位 **0.3756 与 RW 一致** ⇒ **CONSISTENT**（双对象一致）。

## 5. D18 升态依据

三 spread **全 <1e-3（冲门成功）** ＋ GR 门 cross-b **≤1e-7** ＋ Zerilli 跨对象 **CONSISTENT** ⇒

> **物理阻尼独立验证首次升态，D18 UPGRADE（升态）**——物理阻尼独立验证首次闭合 @1e-3，RW+Zerilli 双对象一致；v3.8 条件级物理闭合不回退。

## 6. 勘误

**本轮无新勘误；保持 #41（不回退 #41 与任何历史勘误/否定定理）。**

## 7. 仍 OPEN

回波梳族 nπ/L 全谱、ε/绝对 SNR（标定 PSD）、第二 Q~3.8 铃响峰、Page 三资源、Hawking specular 壁 Γ=0（D25）。

## 8. 文件清单（本轮收口落点）

| 文件 | 动作 |
|---|---|
| `TUFT_企业级归一化主册_v1.0.md` | 升版 v4.2→**v4.3**；新增 ★★ v31 摘要块；新增 **E476** 行；D18 行更新为 UPGRADE；open_backlog bullet 同步 |
| `TUFT_归一化台账_v1.0.json` | version/latest_round/equation_range 同步 v4.3 / E1–E476；新增 `v31_exiting_wave_key_results`；D18 加 `status_v43`；open_backlog 前置；json.load 复验合法 |
| `openuft/.../第十二编.../第67章_物理阻尼独立通道与否定定理全录.md` | append **§67.12**（先读后写、不覆盖 §67.1–67.11） |
| `openuft/.../第十二编.../_章节账本.md` | 67 行字符数 Python `len()` 实测（17020→**19611**）+ 结论；本编合计 67818→**70409**；append 升态说明块 |
| `_audit_v31_exiting_wave_out.txt` | 原始数字来源（照抄，不改） |
| 本报告 | `TUFT_v31_出射波分解升态合并报告.md` |

> 除上述目标文件外只读；未删除任何已记录勘误。备份：各目标文件 `.pre_v43_20260920.bak`。
