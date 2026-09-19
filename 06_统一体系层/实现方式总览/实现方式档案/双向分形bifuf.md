# 实现方式档案：双向分形统一场论（bifuf）

[实现方式总览](../README.md) · 归属体系：**候裁定**

- **形态**：M2 数值 · M4 格点/离散
- **位置**：`utf/17-空间光速螺旋引力理论/code/`（`bifuf_core_algo_validation.py`、`bifuf_full_rigorous_validation.py`、`bifuf_validation_final.py`）
- **状态**：**disputed** —— 认证存疑，裁定前结论不得引用

## 它是什么

bifuf = Bidirectional Fractal Unified Field（双向分形统一场）。

**不含任何物理**：没有拉格朗日量、没有作用量、没有与实验常数对接。它验证的是作者自己写的一棵分形树数据结构（每层生成 k 个子节点、缩放 s）的自洽性。

## 三份 JSON 互相矛盾

| 文件 | 声称 | 实际 |
|---|---|---|
| `bifuf_core_algo_validation.json` | 脚本只在 6/6 时才打印"OMEGA-PRIME 认证通过"横幅 | **`all_pass: false`，2/6 通过**；可逆性、维数、同构均 fail |
| `bifuf_validation_final.json` | — | **`all_pass: false`，6/8**；自相似性、数值精度稳定性失败 |
| `bifuf_full_validation_report.json` | 顶层 `all_passed: true` + OMEGA-PRIME | **自相矛盾**：`validation_3_convergence` 内 `contraction_ok` 三项全 false（实测 α=0 / 1.1427 / 0.8898，期望 0.5；α>1 意味着**根本不是压缩映射**），该块 `summary.all_passed: false` |

## 硬编码证据

`bifuf_full_rigorous_validation.py`：

- 第 753/755/756 行把验证 3、5、6 直接写成 `True`，注释"数学证明成立"
- 第 558 行 `contraction_mapping: True` 硬编码；第 550 行实测失败时只打印"△ 近似成立"
- 第 722–728 行群公理是**字面量 True 列表**（封闭性/结合律/单位元/逆元/交换性），不是计算
- 第 797 行 `core_conclusions` 六个键全硬编码 True

另有一处方法学缺陷：所谓"盒计数维数验证"是同义反复——节点数恒为 k^level、尺度恒为 s^level，线性回归斜率必然等于 log k/log(1/s)，不可能失败。

## 裁定结论（本层立场）

bifuf 的"认证"是**自我一致性单元测试被包装成物理验证**。在独立复跑并移除硬编码之前：

- 证据等级登记为 `conjecture`
- 状态标记为 `disputed`
- 其"认证通过"结论**不得引用**

## 与 s13 的关系（重要澄清）

bifuf 与 [s13 全域双向分形统一场论](../../../01_独立体系/S13_全域双向分形统一场论/README.md) 名称相近，但 s13 的本体是 0/1 对偶基元与六方程闭环 M1–M6，bifuf 只是分形树数据结构的自我一致性检查。**两者不是同一体系的版本关系**，不得互相转移证据。见 [术语消歧](../../跨体系翻译表/术语翻译表.md)「分形」条目。
