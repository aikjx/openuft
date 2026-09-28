# -*- coding: utf-8 -*-
"""MainAgent T11: errata #43 fix + T11 section append in main doc.
"""
import io

path = r'D:\a10\aikjx\code\my_lib\openuft\01_独立体系\S16_TUFT企业级归一化主册\13_论文与成果\主册\TUFT_企业级归一化主册_v1.0.md'
with io.open(path, 'r', encoding='utf-8') as f:
    txt = f.read()

# ---- errata #43 replacements ----
r1_old = "- **MA-AUDIT 跨管线发现**：T10 frob n=1 (N=300) = 0.569956890813−0.287671183832i vs **T09 管线 n=1 = 0.569957939619−0.287655030300i**，|dw|~1.6e-2——单管线自洽不足以钉定 n=1，**两个竞争候选并存，n=1 未定位**（组织者汇总未显式报告此差异，本审计补记）"
r1_new = "- **MA-AUDIT 跨管线发现（勘误 #43：差异为 1.619e-5 非 1.6e-2）**：T10 frob n=1 (N=300) = 0.569956890813−0.287671183832i vs **T09 管线 n=1 = 0.569957939619−0.287655030300i**，|dw|=1.619e-5——两管线在 ~1.6e-5 尺度上接近（数值微扰级差异，非双根/泄漏对签名），但仍远超 1e-9 门，**n=1 未定位**（组织者汇总未显式报告此差异，本审计补记；T11 勘误 #43 修正量级）"
r2_old = "| n=1 单管线几何收敛 ic=3.18e-9（跨管线不一致 ~1e-2） | 条件定理/开放 |"
r2_new = "| n=1 单管线几何收敛 ic=3.18e-9（跨管线不一致 1.619e-5，勘误 #43） | 条件定理/开放 |"

cnt = 0
if r1_old in txt:
    txt = txt.replace(r1_old, r1_new); cnt += 1
else:
    print('WARN r1_old NOT FOUND')
if r2_old in txt:
    txt = txt.replace(r2_old, r2_new); cnt += 1
else:
    print('WARN r2_old NOT FOUND')

# ---- append T11 section ----
t11 = """

---

## §T11 复轮廓 shooting 攻坚与锚点 N=480 强化（2026-09-27，MainAgent 审计收口）

> **勘误 #43（T11 登记）**：T10 审计将 n=1 跨管线候选差异误写为 ~1.6e-2；正确值 |CAND_T10−CAND_T09|=**1.619e-5**（小 3 个量级）。T09/T10 双管线实为 ~1.6e-5 尺度的数值微扰级接近，非双根/泄漏对签名；Gate B OPEN 状态不变，但缺口量级由 7 阶改为 4 阶（1e-9 目标）。主册/架构图/台账中所有旧 "1.6e-2"/"~1e-2" 引用已按此勘误修正。

### T11 三线审计（本机 .venv 复跑逐位核对）

| 线 | 内容 | 本机复现 | 审计结论 |
|---|---|---|---|
| 线一 | 复轮廓 shooting n=0（最终版，尾拟合 C/s² 去除） | 0.430352451005−0.100230156674i（\|dw\|=3.589e-13） | ✅ 数值逐位一致；**方法学划界**：外向 IVP 有限匹配不能把极点钉到 1e-9（偏移 4.397e-2） |
| 线二 | n=1 双候选裁决（复轮廓 shooting t=20） | 0.513402121318−0.285869774501i（\|dw\|=1.386e-13） | ✅ 数值逐位一致；**三候选 STANDOFF**（vs T09/T10 均 ~1.03e-1），未强制挑选 |
| 线三 | F-pencil N=480 交叉验证 | 0.434445176596−0.056449764639i（\|dw\|=1.775e-13） | ✅ 逐位一致；**n=0 锚点独立强化**（\|w480−外推锚\|=4.387e-10 ≤1e-9） |

### 关键科学结论

1. **n=0 锚点 N=480 谱线独立强化成立**（严格定理级数值交叉）：谱线阶梯 300→360→480 收敛至 0.4344451766−0.0564497646i，直接确认 T10 几何外推极限。**TUFT n=0 基频锚（B 条件定理）的权威数值证据链完整**（T08 Gate A → T10 冻结 → T11 N=480 强化）。
2. **shooting/IVP 路线的方法学划界（负结论，有价值）**：组织者线一在锚附近网格扫描发现 |R| 景观平坦无根——V~3/ρ² 长程尾使 T09 的 f1/f2 peel 不适用，锚点残差只是 ~1/Smatch² 渐近尾部漂移而非 BVP 根。方向证据 |D(anchor,|s|)| 单调趋零（0.86→3.1e-4）确认**新锚确为复轮廓 BVP 极点**，但外向 IVP 在强增长轮廓上（指数压制泄漏、窄/非二次盆地）不能像全局 Beyn 铅笔那样干净解析到 1e-9。
3. **n=1 三候选 STANDOFF 维持**：复射线 shooting 根随 t_match 漂移 1.557e-1（t=20: 0.513402−0.285870i；t=32: 0.661274−0.334668i），有限 t 零为 1/|s|² 漂移的偶然相消；与 T09（0.5699579−0.2876550i）/T10（0.5699569−0.2876712i）两候选均差 ~1.03e-1，**未命中**。n=1 的权威裁决仍需谱方法 N≥300 扩展阶梯（shooting 因出射通道衰减结构不适配）。
4. **Gate B n=1,2 维持 OPEN**（不伪闭合）。n=2 因 n=0 自检未过不背书（硬纪律）。

### 四态分级（T11 增量）

| 项 | 判定 |
|---|---|
| F-pencil N=480 谱线交叉（\|w480−外推锚\|=4.39e-10） | **严格定理**（数值） |
| 复轮廓 Leaver IVP shooting 方法构建（衰减片方向确认） | 定义识别 |
| TUFT n=0 基频锚（T10 冻结，N=480 强化） | 条件定理 |
| 复轮廓 shooting n=0 自检（偏移 4.4e-2） | 开放命题 |
| n=1 三候选 STANDOFF | 开放命题 |
| 复轮廓 IVP 根随匹配点漂移（0.106–0.156） | 开放命题（结构性） |

### 权威方法学裁决（本审计背书）

**TUFT 径向方程极点求解的唯一权威路线 = 谱离散（Chebyshev/Frobenius 铅笔）+ Beyn 围道提取**。有限匹配 IVP shooting（无论实轴或复轮廓）因 (i) 长程 V~3/ρ² 尾致 peel BC 失效、(ii) 强增长/衰减通道导致有限 t 零漂移，均不能独立钉定极点。n=1/2 的最终闭合需要谱方法 N≥300 扩展阶梯（含 SVD de-clustering 处理非孤立极点）。

### 脚本产物与证据

- 组织者：`tuft_t11_line1_complex_shooting.py(+_out.txt)`、`tuft_t11_line2_n1_adjudication.py(+_out.txt)`、`tuft_t11_line3_cross_validation.py(+_out.txt)`
- 本机审计：`_ma_t11_audit_out.txt`（线三 N=480）、`_ma_t11_audit2_out.txt`（线一+线二）、`_ma_t11_audit.py`、`_ma_t11_audit2.py`
- 备份：`_ma_t11_backup_pre_t11.json`、主册 `.bak_t11`、架构图 `.bak_t11`

台账 main_agent_v60_t11_line1/2/3_rerun + errata_43。latest_round=v6.0_T11_anchor_N480_reinforced_shooting_scoped_out_gateB_open。E1-E498 冻结不变。
"""

txt += t11

with io.open(path, 'w', encoding='utf-8', newline='') as f:
    f.write(txt)

print('replacements applied:', cnt)
print('doc chars now:', len(txt))
