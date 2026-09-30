# TUFT｜卷十九：EDM 修正专项重写 · 白皮书错误陈述勘误 · CURATED 总览表固化

> 承接卷十八 FRG 非微扰 RG 流；本卷回归本次任务原点：**修复白皮书 TUFT EDM 章节错误声称，核验 4 个落盘脚本，诚实固化结论到 CURATED 归一化总览表，完成本次「分析问题·修复·优化」完整闭环**。
> 不新增任何理论假设；只做审计、勘误、文档固化、结论隔离（区分：已验证 / 待检验 / 已排除）。

---

## 0. 勘误更正说明（必读）

本卷在落笔前先交叉核验了 4 个落盘脚本的真实 verdict 与归一化总览（`tuft_第一性归一化总览.md`）的既有登记。发现一个**关键事实与最初任务草案（用户的卷十九大纲）不一致**，必须先声明，否则本卷会复刻同一类夸大：

- **草案大纲把 EDM / g-2 / ringdown 标为「⏳ 部分参数域排除，存在狭窄剩余窗口待检验」**。这与 4 个脚本的真实 verdict 不符：
  - `tuft_EDM_实验对接_OPEN6.py` 的 concrete prediction `d_e = 1.409e-13 e·cm` **没有自由耦合参数**（它来自 `d_e = eαR_C/(2√(1+α²))`，R_C 由固定偏移假设钉死），该值比真实 ACME/JILA 上限高 **16.5 个数量级** → 判定 **FAIL / 已被实验否决**，不是「部分排除」。
  - `tuft_g2_电子反常磁矩_OPEN5.py` 同样无自由参数，`a_TUFT = α/(8π) = 2.904e-4` 偏差 ~75% → **FAIL / 已被实验否决**。
  - `tuft_sigma_abs0_ringdown_可检验性_OPEN_v2.py` 的「定性两难」已在 `OPEN_v3`（χ²=33, df=2, p=6.8e-8, ~5.74σ 排除）与 `OPEN_v4`（三尺度锚定冲突，壁非 TUFT 可导出）**把窗口关闭** → 不是「剩余窗口待检验」，而是**已关闭**。
  - `tuft_beta_running_缺口_定理N实例化.py` 的 β≡0 是**框架内部自洽**（且仅为 [B] 级有效理论），无实验断言，状态应为 **✅ 自洽（非实验证实）**，而非「待检验预言」。

- **关于「d_e = C_EDM · T_B 自由耦合」重构**：若在白皮书里把 TUFT EDM 重写为带自由耦合 `C_EDM` 与自由背景挠率 `T_B` 的形式（草案 CUR-01 的写法），则 (a) 该重构**不是脚本审计的对象**（脚本用的是固定公式），(b) 两个自由参数相乘可任意压低，使 EDM 预言**对 EDM 实验本身不可证伪**——这是比「窄窗口待检验」更弱的 claim，而非更强的 claim。**诚实结论**：固定公式下的 TUFT EDM 已被排除；自由耦合重构失去可检验性，不能当作「仍存在可检验窗口」。

- **白皮书现状**：`书籍/v1_正文/第十编_电子EDM实验验证与诚实证伪/第53章_EDM实验现状与预言证伪分析.md` **已经**把 EDM 写为「已被 JILA 排除 16.5 个数量级、EDM 通道永久关闭」。换言之，白皮书正文侧的「未被排除」错误**已在书籍第十编更正**；本卷的任务是把这一更正**正式固化进 CURATED 总览表体系**，并补上全局写作规范，防止同类夸大复发。

> 因此本卷第 5 节的 CURATED 表采用**经脚本 verdict 校准后的诚实标签**，并在第 3 节显式给出「草案大纲 vs 校准后」的差异对照。红线：**数学自洽 ≠ 实验证实；诚实边界不粉饰。**

---

## 1. 任务回溯：本次修复的原始目标与错误溯源

原始任务起点：
> 修正白皮书里 TUFT EDM「未被排除」的错误声称，并把四个突破的诚实结论固化进归一化总览的 CURATED 表。

**错误源头定位**：
白皮书旧版 TUFT EDM 章节存在陈述越界：
- 理论层面：TUFT 拓扑挠率机制**可以生成电子电偶极矩 EDM**，存在非零 EDM 理论表达式（脚本 `tuft_EDM_实验对接_OPEN6.py` 的 `d_e = eαR_C/(2√(1+α²))`）；
- 旧文档错误升级断言：**TUFT EDM 模型尚未被实验排除**；
- 审计发现：该断言依赖一个**错误的实验数字**——白皮书曾引用 `|d_e| < 8.7e-34 C·m` 作为 ACME 上限，该值比真实 ACME 2018 上限 `1.1e-29 e·cm = 1.762e-50 C·m` 宽松 **16 个数量级**，比真实 JILA 2023 上限 `4.1e-30 e·cm` 宽松 **16.5 个数量级**。用错数字才得到「未被排除」。

区分两个命题，必须严格隔离：
- **P1**：TUFT 框架内存在可以产生电子 EDM 的挠率耦合项（理论自洽 ✅）
- **P2**：TUFT EDM 全部参数空间都没有被现有 EDM 实验排除（旧文档，❌ 错误）

> 修正原则：**不否定理论机制本身，只修正夸大的观测结论**；保留 TUFT EDM 的理论结构，但诚实标注**具体预测已被实验排除**，把「允许的参数域」按脚本 verdict 重新划分（对固定公式：无允许域；对自由耦合重构：不可证伪，非窄窗口）。

---

## 2. 审计：4 个落盘脚本内容与白皮书原文交叉核验

落盘脚本清单（均位于 TUFT 语料根 `02_TUFT_来源/tuft/`）：

| 脚本 | SHA256（本卷实算） | 核心 verdict |
|---|---|---|
| `tuft_EDM_实验对接_OPEN6.py` | `4ec7599ae65667437d6a197fb978452e1c2cb55b887a6bb7e1070de8b13032b3` | FAIL · 已被实验否决 |
| `tuft_g2_电子反常磁矩_OPEN5.py` | `356cabc07fbdf1a63967892198fac82a1d31c55f1f20e45f37fc45f8f3d9e119` | FAIL · 已被实验否决 |
| `tuft_sigma_abs0_ringdown_可检验性_OPEN_v2.py` | `d263b3ca4b3024927c26e71b74500db62d3804a36e67be76957b28666adb53aa` | FAIL · 定性两难（窗口已在 OPEN_v3/v4 关闭） |
| `tuft_beta_running_缺口_定理N实例化.py` | `076fe3b09b2ae8c077decfae861732385ea742ede18fd950d4d13aad78796849` | 自洽 · 定理 N 实例化（[B] 级） |

核验结果：
1. 4 个脚本代码逻辑自洽，数值计算流程可复现（详见各 `*_report.txt`）；
2. `OPEN6` 与 `OPEN5` **代码内已内含实验上限约束并自行判 FAIL** → 矛盾不在代码，是**白皮书原文字描述与脚本计算结果脱节**（文档用了错误的 16-orders-宽松 ACME 数字）；
3. `ringdown_OPEN_v2` 的 verdict 为「两难」，但同族 `OPEN_v3`（定量 metric）与 `OPEN_v4`（尺度锚定）已把窗口关闭，须以最新同族结论为准；
4. `beta_running_缺口` 与 FRG/RG 流（卷 17、18）参数映射一致，无内部量纲冲突。

> 审计结论：代码本体可信；问题仅在白皮书文本的**结论修辞**与**一处错误的实验数字**。

---

## 3. EDM 章节勘误：撤销「TUFT EDM 未被排除」的错误表述

### 旧表述（删除）
> TUFT 预测的电子 EDM 尚未被现有实验排除。

### 草案大纲拟替换的修订版（本卷判定仍过度）
> TUFT 拓扑挠率耦合可以诱导电子电偶极矩。在 TUFT 参数空间中，部分参数区域已被 ACME 电子 EDM 实验上限排除；存在一个狭窄的剩余参数窗口，仍然满足当前 EDM 约束……

### 本卷校准后的诚实修订版（写入白皮书）
> TUFT 拓扑挠率耦合**可以诱导**电子电偶极矩（理论机制自洽，P1 成立）。
> 但 TUFT 的**具体 EDM 预言** `d_e = eαR_C/(2√(1+α²))` 给出 `|d_e| ≈ 1.41×10⁻¹³ e·cm`，该值**超出**当前电子 EDM 实验上限（JILA 2023：`4.1×10⁻³⁰ e·cm`；ACME 2018：`1.1×10⁻²⁹ e·cm`）达 **16.5 个数量级**，且 TUFT 该公式无自由耦合参数可调，**整段预测已被实验排除**。
> 若将 TUFT EDM 重写为带自由耦合 `C_EDM` 与自由背景挠率 `T_B` 的形式（即 `d_e ∝ C_EDM·T_B`），则可任意压低预言值，使 EDM 对实验**不可证伪**；这是更弱的 claim，不能表述为「存在待检验的窄窗口」。
> 修正方向（与书籍第十编第53章一致）：回归螺旋对称性 `d_e = 0`（与 SM 一致，[A] 对称性论证），EDM 通道关闭。

### 定量约束（真实实验数字）
$$
|d_e| < 4.1\times10^{-30}\ \mathrm{e\cdot cm}\quad(\text{JILA HfF}^+\ \text{Gen II, 2023})
$$
$$
|d_e| < 1.1\times10^{-29}\ \mathrm{e\cdot cm}\quad(\text{ACME II, 2018})
$$
$$
d_e^{\mathrm{TUFT}} \approx 1.41\times10^{-13}\ \mathrm{e\cdot cm}\quad(\text{OPEN6 固定公式})
$$
排除倍数（对 JILA）：$\dfrac{1.41\times10^{-13}}{4.1\times10^{-30}} \approx 3.4\times10^{16}$（约 16.5 个数量级）。

---

## 4. CURATED 总览表结构定义（可直接录入归一化总览）

CURATED 表字段定义（与 `tuft_第一性归一化总览.md` 的「评级坐标 + 层级 L0–L3」体系对齐）：

| 字段 | 说明 |
|---|---|
| entry_id | 条目编号 |
| name | 突破名称 |
| script_ref | 对应落盘脚本文件名（附 SHA256 溯源） |
| category | 分类：理论 / 数值仿真 / 观测预言 |
| status | 状态标签：✅ 自洽 / ⏳ 待检验 / ❌ 已排除 |
| core_prediction | 核心预言 |
| observational_bound | 现有实验 / 观测约束 |
| falsification_criterion | 可证伪判据 |
| cross_ref_volume | 跨卷引用 |
| uncertainty | 理论不确定性 |

> 状态标签硬性规则（全局生效）：**禁止用「未被排除」作为全局标签**；只要存在任意一块参数区域被实验排除，不能笼统宣称「模型未被排除」；所有预言必须附**参数域划分**（被排除区域 / 允许窗口 / 不可证伪区）。

---

## 5. 四个突破脚本结论固化进 CURATED 表（经脚本 verdict 校准）

|entry_id|name|script_ref (SHA256)|category|status|core_prediction|observational_bound|falsification_criterion|cross_ref_volume|uncertainty|
|---|---|---|---|---|---|---|---|---|---|
|CUR-01|TUFT 电子 EDM 挠率诱导|`tuft_EDM_实验对接_OPEN6.py` (`4ec7…32b3`)|理论+数值仿真|**❌ 已排除**|时空背景挠率耦合费米子，生成非零电子 EDM：`d_e = eαR_C/(2√(1+α²))`|JILA 2023 `4.1e-30`、ACME 2018 `1.1e-29` e·cm；TUFT 具体预言 `1.41e-13` e·cm 超 16.5 数量级|具体预测已被排除；自由耦合重构则对 EDM 不可证伪（非窄窗口）|卷19、第十编52/53、OPEN5b、OPEN7|固定偏移假设 [C]；无第一性导出耦合|
|CUR-02|TUFT 电子反常磁矩 g-2|`tuft_g2_电子反常磁矩_OPEN5.py` (`356c…e119`)|理论+数值仿真|**❌ 已排除**|挠率贡献 `a_TUFT = α/(8π) = 2.904e-4`|实验 `a_e = 1.160e-3`，偏差 ~75%，超实验精度 ~10¹¹ 倍|偏差 > 实验精度 → 该挠率费米子耦合被约束/排除|卷19、OPEN5b、OPEN5c|挠率紫外截断 + 孤子 τ/κ 锁定（OPEN5c）|
|CUR-03|Ringdown 挠率可检验性|`tuft_sigma_abs0_ringdown_可检验性_OPEN_v2.py` (`d263…53aa`)|理论+数值仿真|**❌ 窗口已关闭**（临界）|黑洞 QNM 因全局背景挠率 `T_B` 偏移；`a–T_B` 参数简并；多事件联合拟合可解除简并|LIGO 现有样本：OPEN_v3 χ²=33 (df=2, p=6.8e-8, ~5.74σ 排除)；OPEN_v4 三尺度锚定冲突（壁在 1e-26~1e-78 M，与可检验 2.05M 差 26~78 量级）|壁在 `r_s=2.05M` 与 LIGO 冲突；壁远离则无相干模 ⇒ 无兼容参数区|卷15,16,18、OPEN_v3、OPEN_v4|QNM 线性响应近似、高阶模截断、σ_abs=0 非 TUFT 可导出|
|CUR-04|β-running 缺口定理实例化|`tuft_beta_running_缺口_定理N实例化.py` (`076f…6849`)|理论+数值仿真|**✅ 自洽**（[B] 级，非实验证实）|TUFT RG β 流存在拓扑缺口，对应相变分界面，匹配宇宙拓扑跃迁 `t_c`；固定螺旋下 β≡0（R30 三路闭合独立同源）|无直接微观实验；仅间接宇宙学关联|FRG 高阶计算消除缺口结构，或 CMB 否定 `f_NL` 跳变 ⇒ 缺口定理失效|卷17,18、R29、R30、R31|依赖作用量 ansatz 截断；`t_c` 在 TUFT 内无定义（R31 A3）|

> **草案大纲 vs 校准后标签差异说明**：
> - 草案把 CUR-01/02/03 都标 `⏳ 部分参数域排除`；校准后 CUR-01/02 为 **❌ 已排除**（固定公式无自由参数、超 16.5/75% 量级），CUR-03 为 **❌ 窗口已关闭**（OPEN_v3/v4 联合排除）。
> - 草案把 CUR-04 标 `⏳ 待检验`；校准后 CUR-04 为 **✅ 自洽**——它是框架内部数学自洽（β≡0），本身无实验预言，谈不上「待检验」。
> - 此差异是本卷「诚实固化」的核心：不因「精算通过」而宣称「未被排除」。

---

## 6. 结论分层标签规范（全局生效，后续所有文档统一使用）

- ✅ **自洽**：理论内部数学自洽，数值代码可复现；**不代表实验证实**。
- ⏳ **待检验**：预言存在未被排除的参数窗口，等待未来观测；部分参数域可能已被排除，必须标注。
- ❌ **已排除**：全部（或具体）参数空间与观测冲突，假设在该口径下失效。

> 硬性规则：禁止在 status 字段使用「未被排除」作为全局标签，只能写「部分参数域已排除，剩余窗口待检验」或「❌ 已排除」；自由耦合重构导致不可证伪的，须显式标注「不可证伪（非可检验窗口）」。

---

## 7. 冲突隔离规则（白皮书写作强制规范）

1. 理论自洽性和实验证实必须严格分开；理论自洽 ≠ 实验支持；
2. 只要存在任意一块参数区域被实验排除，不能笼统宣称「模型未被排除」；
3. 所有预言必须附带**参数域划分**：被排除区域 / 允许窗口 / 不可证伪区；
4. 可证伪判据必须独立写，不混入理论动机描述；
5. 所有数值结果必须绑定对应脚本文件名 + SHA256，便于审计复现；
6. 重构为自由参数形式以「拯救」预言时，必须声明该重构**丧失可检验性**，不得当作「仍存可检验窗口」。

---

## 8. 遗留不确定性清单（写入白皮书讨论章节）

1. TUFT 挠率-费米子耦合的形式是有效场论假设，没有从三本源公理唯一导出；
2. EDM 计算依赖 FRG / 一圈 RG 的截断选择；不同调节器会小幅移动允许参数窗口边界（但对固定公式不影响「已排除」结论）；
3. 电子 EDM 与引力挠率之间的跨能标匹配，存在从普朗克尺度到低能 QED 的跑动不确定性；
4. 多信使联合推断中，`T_B` 与 `t_c` 的关联依赖宇宙学模型假设（ΛCDM + 挠率）；
5. **为何螺旋框架会给出错误的 EDM 量级**——需理解「固定偏移」假设的错误来源（书籍 53 章 [C] 待建项）。

---

## 9. 文档修订清单（白皮书修改点位）

1. 【重点】TUFT EDM 章节：删除「未被排除」错误断言，替换为第 3 节校准后诚实正文；插入**真实** ACME/JILA 定量上限（非 16-orders-宽松旧数字）；划分允许/排除/不可证伪参数域；
2. 新增全局标签规范小节（第 6 节）；
3. 新增 CURATED 归一化总览表作为独立附录（第 5 节 + 本卷 `tuft_卷十九_CURATED.json`）；
4. 四个突破章节末尾增加到 CURATED 表的交叉引用（CUR-01..04）；
5. 增加审计说明段落：核验 4 个落盘脚本 + SHA256，代码数值计算与修订后的文档结论保持一致；
6. 增加免责声明：TUFT 是正在发展的理论框架，所有预言等待未来实验检验；数学自洽 ≠ 实验证实。

> 注：书籍 `第十编_电子EDM实验验证与诚实证伪` 第 52/53 章已落地第 1/5/6 项；本卷补齐 CURATED 表体系化与全局写作规范。

---

## 10. 附录：脚本哈希指纹校验逻辑 + CURATED 表 JSON 结构 + EDM 约束数值计算代码

### 10.1 哈希校验（本卷实算结果，已写入第 2 节表）

```python
# TUFT 卷十九附录：EDM 约束扫描 + 脚本完整性哈希校验
import hashlib

def file_hash(filepath: str) -> str:
    """审计：脚本文件指纹校验，用于 CURATED 溯源"""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

# 本卷实算（2026-09-30）：
# tuft_EDM_实验对接_OPEN6.py              4ec7599ae65667437d6a197fb978452e1c2cb55b887a6bb7e1070de8b13032b3
# tuft_g2_电子反常磁矩_OPEN5.py          356cabc07fbdf1a63967892198fac82a1d31c55f1f20e45f37fc45f8f3d9e119
# tuft_sigma_abs0_ringdown_可检验性_OPEN_v2.py  d263b3ca4b3024927c26e71b74500db62d3804a36e67be76957b28666adb53aa
# tuft_beta_running_缺口_定理N实例化.py   076fe3b09b2ae8c077decfae861732385ea742ede18fd950d4d13aad78796849
```

### 10.2 EDM 约束数值计算（固定公式 vs 自由耦合扫描）

```python
import hashlib
import numpy as np

# 真实实验上限（非旧版 16-orders-宽松数字）
d_e_limit_jila = 4.1e-30   # e·cm  (JILA HfF+ Gen II, 2023)
d_e_limit_acme = 1.1e-29   # e·cm  (ACME II, 2018)

# TUFT 固定公式预言（OPEN6 实测值，无自由参数）
d_e_tuft_fixed = 1.409e-13  # e·cm

def d_e_tuft_free(C_EDM, T_B):
    """自由耦合重构（注意：非脚本审计对象，仅为参数空间逻辑演示）
    C_EDM, T_B 均可任意压低 => 对 EDM 实验本身不可证伪"""
    return C_EDM * T_B

# ---- (A) 固定公式：单一预测点，不可调 => 直接判定 ----
ratio_jila = d_e_tuft_fixed / d_e_limit_jila
ratio_acme = d_e_tuft_fixed / d_e_limit_acme
print(f"固定公式排除倍数(JILA)={ratio_jila:.2e}  (ACME)={ratio_acme:.2e}")
# => 3.44e+16 / 1.28e+16  => 已被实验排除约 16.5 个数量级

# ---- (B) 自由耦合扫描：演示「可任意压低 => 不可证伪」 ----
def scan_edm_window():
    C_list = np.logspace(-30, -4, 200)   # 放宽下限到 -30，覆盖可压低区
    T_B_list = np.logspace(-20, -6, 200)
    allowed, excluded = [], []
    for cb in C_list:
        for tb in T_B_list:
            de = d_e_tuft_free(cb, tb)
            (allowed if abs(de) < d_e_limit_jila else excluded).append((cb, tb, de))
    return np.array(allowed), np.array(excluded)

if __name__ == "__main__":
    allowed_points, excluded_points = scan_edm_window()
    print(f"自由耦合扫描：允许点 {len(allowed_points)}, 已排除点 {len(excluded_points)}")
    print("说明：允许点随 C_EDM/T_B 下限任意增大 => 预言对 EDM 不可证伪，非'窄窗口待检验'")
```

### 10.3 CURATED 表 JSON 结构（`tuft_卷十九_CURATED.json`）

```json
{
  "volume": 19,
  "title": "TUFT EDM 修正专项重写 · CURATED 固化",
  "generated": "2026-09-30",
  "red_line": "数学自洽 != 实验证实；诚实边界不粉饰",
  "entries": [
    {
      "entry_id": "CUR-01",
      "name": "TUFT 电子 EDM 挠率诱导",
      "script_ref": "tuft_EDM_实验对接_OPEN6.py",
      "script_sha256": "4ec7599ae65667437d6a197fb978452e1c2cb55b887a6bb7e1070de8b13032b3",
      "category": "理论+数值仿真",
      "status": "❌ 已排除",
      "core_prediction": "d_e = eαR_C/(2√(1+α²))，无自由参数",
      "observational_bound": "JILA 4.1e-30 / ACME 1.1e-29 e·cm；TUFT 1.41e-13 超 16.5 数量级",
      "falsification_criterion": "固定公式已被排除；自由耦合重构不可证伪（非窄窗口）",
      "cross_ref_volume": "卷19、第十编52/53、OPEN5b、OPEN7",
      "uncertainty": "固定偏移假设 [C]；无第一性耦合"
    },
    {
      "entry_id": "CUR-02",
      "name": "TUFT 电子反常磁矩 g-2",
      "script_ref": "tuft_g2_电子反常磁矩_OPEN5.py",
      "script_sha256": "356cabc07fbdf1a63967892198fac82a1d31c55f1f20e45f37fc45f8f3d9e119",
      "category": "理论+数值仿真",
      "status": "❌ 已排除",
      "core_prediction": "a_TUFT = α/(8π) = 2.904e-4",
      "observational_bound": "实验 a_e = 1.160e-3，偏差 ~75%，超精度 ~10^11 倍",
      "falsification_criterion": "偏差 > 实验精度 => 挠率费米子耦合被约束",
      "cross_ref_volume": "卷19、OPEN5b、OPEN5c",
      "uncertainty": "挠率紫外截断 + 孤子 τ/κ 锁定"
    },
    {
      "entry_id": "CUR-03",
      "name": "Ringdown 挠率可检验性",
      "script_ref": "tuft_sigma_abs0_ringdown_可检验性_OPEN_v2.py",
      "script_sha256": "d263b3ca4b3024927c26e71b74500db62d3804a36e67be76957b28666adb53aa",
      "category": "理论+数值仿真",
      "status": "❌ 窗口已关闭（临界）",
      "core_prediction": "黑洞 QNM 因 T_B 偏移；a–T_B 简并",
      "observational_bound": "OPEN_v3 χ²=33(df=2,p=6.8e-8,~5.74σ)；OPEN_v4 锚定冲突 26~78 量级",
      "falsification_criterion": "壁 r_s=2.05M 与 LIGO 冲突；壁远离则无相干模 => 无兼容区",
      "cross_ref_volume": "卷15,16,18、OPEN_v3、OPEN_v4",
      "uncertainty": "QNM 线性响应、高阶模截断、σ_abs=0 非 TUFT 可导出"
    },
    {
      "entry_id": "CUR-04",
      "name": "β-running 缺口定理实例化",
      "script_ref": "tuft_beta_running_缺口_定理N实例化.py",
      "script_sha256": "076fe3b09b2ae8c077decfae861732385ea742ede18fd950d4d13aad78796849",
      "category": "理论+数值仿真",
      "status": "✅ 自洽（[B] 级，非实验证实）",
      "core_prediction": "β≡0（固定螺旋）；拓扑缺口对应 t_c",
      "observational_bound": "无直接微观实验；仅间接宇宙学关联",
      "falsification_criterion": "FRG 高阶消除缺口，或 CMB 否定 f_NL 跳变 => 定理失效",
      "cross_ref_volume": "卷17,18、R29、R30、R31",
      "uncertainty": "作用量 ansatz 截断；t_c 在 TUFT 内无定义（R31 A3）"
    }
  ]
}
```

---

## 闭环完成

本次「分析问题·修复·优化」任务目标落地（**诚实版**）：

- ✅ 定位白皮书 EDM 错误源头：依赖 16-orders-宽松的错误 ACME 数字 + 文档/代码脱节；
- ✅ 核验 4 个落盘脚本 + SHA256，确认代码与文档不一致的根源在**结论修辞**而非代码；
- ✅ 完成 EDM 章节勘误（与书籍第十编 52/53 章一致），移除过度宣称，写入真实实验约束；
- ✅ 建立 CURATED 总览表（JSON + 第 5 节），固化 4 项突破的**诚实**结论，带状态标签、约束、可证伪判据；
- ✅ 建立全局文档写作规范（标签 / 隔离 / 参数域划分 / 不可证伪声明），防止同类夸大复发；
- ⚠️ **与最初草案大纲的关键偏差已在第 0 节、第 5 节显式记录**：EDM/g-2 为 ❌ 已排除、ringdown 为 ❌ 窗口已关闭、β-running 为 ✅ 自洽（[B]）——均非草案的「⏳ 部分参数域排除 / 窄窗口待检验」。

## 下一阶段可选方向

1. **卷二十：TUFT 全套专著总序 + PRD 长文终稿整合**，汇总 A–F 六组可证伪判据，生成完整 BibTeX 参考文献库，构建全书知识图谱；
2. **卷二十：可视化套件**（Three.js 3D 相空间可视化：FRG RG 流、不动点、临界分界面），含 CURATED 表交互式网页前端；
3. **卷二十：TUFT 全套自检验流水线**，自动化脚本哈希校验、参数扫描、χ² 诊断、MCMC 收敛检查，一键审计新加入条目。
