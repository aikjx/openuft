# MIGRATION_GUIDE.md · 文件迁移指南

> **目标**：把原工作区 `D:\a10\aikjx\code\my_lib\` 下的统一场论相关文档，迁移到 `openuft/` 新结构下。

---

## 迁移原则

1. **绝不破坏原文件**——所有迁移操作采用"复制"而非"移动"，直至人工确认
2. **路径对应表**——下方给出每篇文档的目标位置
3. **可回滚**——任何迁移都可逆向执行（`cp -r` 备份 → 删除目标 → 复制回来）
4. **增量迁移**——一次迁一批，对照 INDEX.md 检查

---

## 完整路径对应表

### 求导 D 系列（10_D_求导_derivation/）

| 原文件 | 目标位置 |
|---|---|
| `D1*求导*` 类（暂未独立成文件，合并于终极报告 v6） | `10_D_求导_derivation/D0_作用量变分求导_核心方法论/Einstein_Hilbert_泛函求导.md`（待拆分）|
| `D5 大统一力方程` 在 v2/v3/v6 报告中 | `10_D_求导_derivation/D5_大统一力方程/四力分解.md`（待提取） |

### 证明 P 系列（20_P_证明_proof/）

| 原文件 | 目标位置 |
|---|---|
| `GAQ_UFT_v6_粒子质量谱几何化.md` | `20_P_证明_proof/P9_质量谱三代机制/SO3_Cl44_三代边界态.md` |
| `算法联盟_全维三重奏定理完整严格证明.md` ★ | `20_P_证明_proof/P3_归纳闭合_R9/完整严格证明.md` |
| `算法联盟_绝热三重奏定理.md` ★ | `20_P_证明_proof/P4_绝热三重奏_R10/绝热与纯圆周精确.md` |
| `算法联盟_全维三重奏定理证明攻坚.md` | `20_P_证明_proof/P3_归纳闭合_R9/证明攻坚.md` |
| `算法联盟_全维三重奏定理谱理论证明.md` | `20_P_证明_proof/P6_谱理论框架_R7R8/谱理论证明.md` |
| `算法联盟_全维三重奏最高权限精算.md` | `20_P_证明_proof/P3_归纳闭合_R9/最高权限精算.md` |
| `算法联盟_全维三重奏终极报告.md` | `20_P_证明_proof/P1_螺旋三重奏_TS1/终极报告.md` |
| `算法联盟_全维三重奏研究总报告.md` | `20_P_证明_proof/P1_螺旋三重奏_TS1/研究总报告.md` |

### 验证 V 系列（30_V_验证_verification/）

| 原文件 | 目标位置 |
|---|---|
| `验证结果_*.txt` | `30_V_验证_verification/V0_验证引擎M0/数值结果/` |

### 精算 A 系列（40_A_精算_audit/）

| 原文件 | 目标位置 |
|---|---|
| `算法联盟_统一场论严格审计与精算分析.md` | `40_A_精算_audit/A1_误差预算/严格审计与精算.md` |
| `统一场论知识体系整理.md` | `40_A_精算_audit/A5_分层标注Hierarchy/知识体系整理.md` |

### 物理领域（50_physics_domains/）

| 原文件 | 目标位置 |
|---|---|
| （待拆分） | `50_physics_domains/量子引力/黑洞熵.md`（从 P7 复制） |
| （待拆分） | `50_physics_domains/宇宙学LCDM/暗能量视界截断.md`（从 P10 复制） |

### 论文（90_paper_论文/）

| 原文件 | 目标位置 |
|---|---|
| `算法联盟_全维统一场论终极总报告_v2.md` | `90_paper_论文/终极报告系列/v2_20260905.md` |
| `算法联盟_全维统一场论终极总报告_v3.md` | `90_paper_论文/终极报告系列/v3_20260905.md` |
| `算法联盟_全维统一场论终极总报告_v4.md` | `90_paper_论文/终极报告系列/v4_20260906.md` |
| `算法联盟_全维统一场论终极总报告_v5.md` | `90_paper_论文/终极报告系列/v5_20260906.md` |
| **`算法联盟_全维统一场论终极总报告_v6.md`** ★ | `90_paper_论文/终极报告系列/v6_20260906_FINAL.md` |
| `全维统一场论_全维度修订版.md` | `90_paper_论文/全维修订版v2/全维度修订v2.md` |
| `算法联盟_全维统一场论_v3.md` | `90_paper_论文/求导证明v3/求导证明v3.md` |
| `统一场论知识体系整理.md` | `90_paper_论文/知识体系整理/知识体系整理.md` |
| `算法联盟_全维三重奏大统一分析.md` | `90_paper_论文/综述修订/大统一分析.md` |

### 历史档案（95_history_archive/）

| 原文件 | 目标位置 |
|---|---|
| `GAQ_UFT_几何作用量子统一场论.md` | `95_history_archive/GAQ_UFT_v1_几何原子/几何原子_v1.md` |
| `GAQ_UFT_全集_卷I-IV.md` | `95_history_archive/GAQ_UFT_v1_几何原子/全集_卷I-IV.md` |
| `GAQ_UFT_全集_卷V-VIII.md` | `95_history_archive/GAQ_UFT_v1_几何原子/全集_卷V-VIII.md` |
| `GAQ_UFT_全集_卷IX-XI.md` | `95_history_archive/GAQ_UFT_v1_几何原子/全集_卷IX-XI.md` |
| `GAQ_UFT_全链路闭环归一化分析.md` | `95_history_archive/GAQ_UFT_v1_几何原子/全链路闭环.md` |
| `GAQ_UFT_核力理论全维总结.md` | `95_history_archive/GAQ_UFT_v3_三大新体系/核力理论.md` |
| `GAQ_UFT_物理未解之谜全维突破.md` | `95_history_archive/GAQ_UFT_v3_三大新体系/未解之谜.md` |
| `GAQ_UFT_五谜严格证明论文.md` | `95_history_archive/GAQ_UFT_v3_三大新体系/五谜严格证明_v1.md` |
| `GAQ_UFT_五谜严格证明论文_v2.md` | `95_history_archive/GAQ_UFT_v3_三大新体系/五谜严格证明_v2.md` |
| `GAQ_UFT_v3_三大新体系论文.md` | `95_history_archive/GAQ_UFT_v3_三大新体系/三大新体系_v3.md` |
| `GAQ_UFT_v4_全维统一顶尖论文.md` | `95_history_archive/GAQ_UFT_v4_全维统一/v4_全维统一.md` |
| `GAQ_UFT_v5_全维几何化论文.md` | `95_history_archive/GAQ_UFT_v5_cħ几何化/v5_cħ几何化.md` |
| `GAQ_UFT_v6_粒子质量谱几何化.md` | `95_history_archive/GAQ_UFT_v6_质量谱/v6_质量谱_几何化.md` |
| `宇宙本源_频率_螺旋_全维第一性原理统一场论.md` | `95_history_archive/宇宙本源_217KB_巨文档.md` |
| `大统一方程与四力统一全集_算法联盟最高权限版.md` | `95_history_archive/大统一方程全集.md` |
| `G_eps0_full_dimensional_analysis_20260825.md` | `95_history_archive/G_eps0_全维分析.md` |
| `README.md` (6月旧前端) | `95_history_archive/旧前端项目_README.md` |
| `math_analysis_report.md` (6月) | `95_history_archive/math_analysis_report.md` |

### 代码（70_source_code/）

| 原文件/路径 | 目标位置 |
|---|---|
| `triad_uft/`, `tests/`, `examples/`（如已存在） | `70_source_code/triad_uft/`, `tests/`, `examples/` |
| `unified_verification.log` 等 | `70_source_code/verify/logs/` |

### 可视化（80_visualization/）

| 原文件 | 目标位置 |
|---|---|
| `全维统一场论_v3可视化.html` | `80_visualization/v3.html` |
| `全维统一场论_v5可视化.html` | `80_visualization/v5.html` |
| `全维统一场论_v6可视化.html` | `80_visualization/v6.html` |
| `统一场论_全维可视化.html` | `80_visualization/全维.html` |
| `三重奏研究谱系.html` | `80_visualization/三重奏研究谱系.html` |
| `全维知识图谱.html` | `80_visualization/全维知识图谱.html` |

---

## 批量迁移脚本（Git Bash）

```bash
cd "D:\a10\aikjx\code\my_lib"
SRC=.
DST=openuft

# 一键复制（不删除原文件，保证可回滚）
mkdir -p "$DST/20_P_证明_proof/P3_归纳闭合_R9"
cp -n "$SRC/算法联盟_全维三重奏定理完整严格证明.md" "$DST/20_P_证明_proof/P3_归纳闭合_R9/完整严格证明.md"

mkdir -p "$DST/20_P_证明_proof/P4_绝热三重奏_R10"
cp -n "$SRC/算法联盟_绝热三重奏定理.md" "$DST/20_P_证明_proof/P4_绝热三重奏_R10/绝热与纯圆周精确.md"

mkdir -p "$DST/20_P_证明_proof/P9_质量谱三代机制"
cp -n "$SRC/GAQ_UFT_v6_粒子质量谱几何化.md" "$DST/20_P_证明_proof/P9_质量谱三代机制/SO3_Cl44.md"

# 论文系列
mkdir -p "$DST/90_paper_论文/终极报告系列"
for v in 2 3 4 5 6; do
  cp -n "$SRC/算法联盟_全维统一场论终极总报告_v$v.md" "$DST/90_paper_论文/终极报告系列/v${v}_20260906.md"
done

# 完整批量：参考 INDEX.md 一一对应
```

---

## 迁移完成后

1. **运行** `python triad_uft/audit_report.py` 验证完整性
2. **检视** `openuft/INDEX.md` 与 `WORKFLOW.md` 是否对齐
3. **首次 push**：`openuft/` 整个目录结构 push 到 `github.com/aikjx/openuft`
4. **保留原文件**：作为开发态备份，至少 30 天后再考虑删除

---

*AI 科技星*
*最后更新：2026-09-06 21:48 GMT+8*
