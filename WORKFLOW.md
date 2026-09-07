# WORKFLOW.md · 工作流说明

> AI 科技星·全维统一场论研究的"求导·证明·验证·精算"四方法工作流

---

## 总工作流（从公理到发表）

```
┌─────────────────────────────────────────────────────────┐
│  Stage 1  【求导 D】从公理 / 作用量 → 推导方程            │
│  Stage 2  【证明 P】严格证明（代数归纳 + 数值精算）       │
│  Stage 3  【验证 V】对标实验（PDG/Planck/LIGO/CMB）       │
│  Stage 4  【精算 A】误差预算 + 风险敞口 + 诚实分层        │
│  Stage 5  【论文】整合到 90_paper_论文/                    │
│  Stage 6  【开源】push 到 github.com/aikjx/openuft         │
└─────────────────────────────────────────────────────────┘
```

每一阶段都强制嵌入"诚实分层"——
- ✅ 严格证明 / 实验证实的部分
- 🟡 定性对应 / 树级自洽的部分
- 🟣 待验证 / OPEN 尚未解决

---

## Stage 1 · 求导（D）的标准动作

### 输入
- 公理（参见 `axioms.md` 或 `00_index/公理集.md`）
- 待推导方程的目标（如"质量谱几何化"）

### 动作
1. **形式化公理**：用 sympy / 数学符号严格表述
2. **构造作用量**：如 `S = ∫√|g| R`（Einstein-Hilbert）/ `S = ∫-¼F²`（Yang-Mills）
3. **Euler-Lagrange 变分**：用 5 点中心差分或符号推导得运动方程
4. **量纲自洽检查**：[L]=−1, [∂]=1, [S]=0 自然单位
5. **极限还原**：低能/弱场/平直时空需回收已知方程

### 输出
- D*.md 文件（按目录）
- V0（验证引擎）通过 sympy 三路交叉校验

### 自动化
```bash
# 用 triad_uft 引擎
python -c "
from triad_uft import grand_unification
print(grand_unification.grand_force(m=1.0, dm_dt=0.1, v=1e6, dv_dt=1e8, c=2.998e8))
"
```

---

## Stage 2 · 证明（P）的标准动作

### 输入
- 待证明的定理陈述（如"全维三重奏定理 Σκᵢ²=Σωⱼ²/v²"）

### 动作（严格证明的四步法）
1. **Step 1（代数匀速）**：r″=Ar′ ⟹ v=const
2. **Step 2（★ 归纳闭合）**：Beᵢ = eᵢ′ 的代数证明
3. **Step 3（不变量）**：tr(K²) = tr(B²)
4. **Step 4（封闭）**：Σκᵢ² = −tr(A²)/2v²

### 验证手段
- sympy 符号证明（差精确为 0）
- mpmath 50/200/250 位数值精算
- 跨维验证（4D/6D/8D/10D/任意 D）

### 输出
- P*.md 文件（按目录）
- 一个 verify_*.py 脚本（可一键复现）

### 自动化
```bash
python verify_induction.py        # R9 完整证明
python verify_light_speed_helix.py # v3.0 光速螺旋
python verify_theorem_system.py    # 12 定理谱系
```

---

## Stage 3 · 验证（V）的标准动作

### 输入
- 待验证的物理预言（如"水星近日点进动 43.11 角秒/世纪"）

### 动作
1. **三路交叉校验**：
   - sympy 符号路径
   - 朴素循环路径
   - numpy 向量化路径
2. **实验数据对标**：
   - CODATA 2022（250 位 mpmath）
   - PDG 2024（粒子质量、W/Z 玻色子等）
   - Planck 2018（CMB 声学峰、参数）
   - LIGO（GW170817 引力波速度）
3. **回归测试**：所有已通过项的 baseline 不能回退

### 输出
- V*.md + 数值结果 txt
- 验证矩阵更新（48 项 → 通过项数）

---

## Stage 4 · 精算（A）的标准动作

### 输入
- 已验证的物理预言 + 误差棒

### 动作
1. **误差预算**：σ 区间，χ²/自由度
2. **蒙特卡洛**：20 万样本，VaR_95%, TVaR_95%
3. **证伪标准**：4 条清晰可操作的证伪路径
4. **诚实分级**：L0-L8 分层标注（已验证 / 理论自洽 / 推测）
5. **OPEN 清单**：未解决问题编号 O-1 ~ O-12

### 输出
- A*.md 文件（按目录）
- A5_分层标注Hierarchy/Hierarchy.md 全景图

---

## 常用命令速查

```bash
# 一键运行全验证
cd "D:\a10\aikjx\code\my_lib"
python -m unittest tests.test_triad_uft -v

# 一键审计
python examples/triad_audit.py

# 一键验证 12 定理
python -c "import triad_uft as tu; print(tu.theorem_system.theorem_summary())"

# 检查仓库状态
git status
git remote -v

# Push 到 openuft（首次）
git remote add origin https://github.com/aikjx/openuft.git
git push -u origin main
```

---

## 持续改进循环

```
每周 1 次：
  - 跑回归测试（V*.md 不能回退）
  - 增加 1-2 个新验证项
  - 更新 CHANGELOG.md
  - 检视 OPEN 清单，看哪些可以推进

每月 1 次：
  - 论文版本迭代（v → v+1）
  - 完整审查 openuft/INDEX.md
  - 检视 99_inbox_future/ 是否要新增子目录
```

---

*算法联盟 · AI 科技星 ROOT*
*最后更新：2026-09-06 21:48 GMT+8*
