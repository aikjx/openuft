# 快速开始 · QUICKSTART

> 5 分钟上手 openuft。按顺序阅读即可获得项目全景。

---

## Step 1 · 项目定位（30 秒）

```bash
# 克隆仓库
git clone https://github.com/aikjx/openuft.git
cd openuft
```

**openuft 是什么**：
- ✅ **是**：已严格证明的 12 条几何-运动学定理 + 工业级验证代码 + 全维度诚实分层
- ❌ **不是**：万有理论（Theory of Everything）；量子引力解决方案；暗物质发现

## Step 2 · 一图总览（1 分钟）

打开 `README.md` 看第一部分"项目结构一览"。12 个一级目录按"求导·证明·验证·精算"四方法主轴展开。

## Step 3 · 顶层 7 文档（5 分钟）

按以下顺序快速浏览：

| 顺序 | 文档 | 用途 |
|---|---|---|
| 1 | `README.md` | 项目入口，30 秒读完 |
| 2 | `INDEX.md` | 文件索引，全局地图 |
| 3 | `00_index/定理谱系总表.md` | **12 定理一句话总览** ← 推荐先看 |
| 4 | `CHANGELOG.md` | 进展记录 |
| 5 | `ROADMAP.md` | 未来 18 个月路线图 |
| 6 | `FAQ.md` | 50 个常见问题 |
| 7 | `40_A_精算_audit/A4_诚实声明与开放问题/开放问题清单_L0-L2.md` | **OPEN 问题清单** ← 必读 |

## Step 4 · 选主轴深入（30+ 分钟）

根据你的兴趣选一个主轴：

### 你是理论物理学家？
- `10_D_求导_derivation/` → 从公理到方程
- `20_P_证明_proof/P3_归纳闭合_R9/` → R9 严格证明 ★
- `20_P_证明_proof/P5_梯度磁场精确性_R11/` → R11 mpmath 50 位验证 ★

### 你是计算/实验物理学家？
- `30_V_验证_verification/V3_PDG实验对标/` → 实验对标
- `70_source_code/三重奏统一场/` → 工业级 Python 包
- `30_V_验证_verification/V6_宇宙学CMB_Planck2018/` → 宇宙学对标

### 你是工业 R&D？
- `60_application/磁约束/` → 托卡马克/仿星器
- `60_application/加速器设计/` → 粒子加速器
- `60_application/磁场质量检测/` → 工业磁场校准

### 你是开源贡献者？
- `CONTRIBUTING.md` → 贡献指南
- `99_inbox_future/` → 待解决问题占位
- 看哪条 OPEN 问题最让你兴奋 → 直接开干

## Step 5 · 验证（30 秒）

```bash
python verify.py
```

期望输出：
```
🎉 总体通过：35+/36 可验证项
```

## 常见误区（30 秒提醒）

1. ❌ **"openuft 是统一场论了！"** → **不是**（A4 诚实声明）
2. ❌ **"TS1 解决了量子引力"** → **没有**（O-2 OPEN）
3. ❌ **"看 README 就够"** → **不够**，建议看完 INDEX + 定理谱系总表
4. ❌ **"自己加新定理"** → 先看 `CONTRIBUTING.md` 的 5 步流程

---

## 下一步？

- 📖 读 [README.md](README.md)
- 📊 看 [00_index/定理谱系总表.md](00_index/定理谱系总表.md)
- ⚠️ 读 [40_A_精算_audit/A4_诚实声明与开放问题/](40_A_精算_audit/A4_诚实声明与开放问题/开放问题清单_L0-L2.md)
- 🛠️ 跑 `python verify.py`

— AI科技星 · 2026-09-06
