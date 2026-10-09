# 算法联盟 · 全维三重奏 —— 企业级验证工程

对「算法联盟·几何三重奏」（公理 A：v≡c；公理 B：几何三重奏；全维度推广）的
**企业级求导·证明·验证·精算**工程。所有计算确定性、可复算、可审计，并给出
明确的**可证伪判定**与诚实审计（OPEN 清单）。

## 目录结构

```
enterprise/
├── README.md                  ← 本文件（工程说明 + 验收标准）
├── run_verification.py        ← 统一验证入口（QA 门 + 报告生成）
├── pkg/
│   ├── __init__.py
│   ├── constants.py           ← CODATA 2022 + SI 2019 常数，mpmath 250 位
│   └── triad.py               ← 三重奏全维精算库（T1–T5）
├── tests/
│   └── test_triad.py          ← 单元测试（10 项，断言恒等式/量纲/KK）
└── reports/
    └── verification_report.md ← 自动生成的验证报告
```

## 运行方式（Windows / PowerShell）

```powershell
cd uft\enterprise
python run_verification.py            # 企业级精算 + 单元测试 + 报告
python run_verification.py --legacy   # 附加复跑 uft/ 下历史 5 套验证脚本
python pkg\constants.py               # 单跑 CODATA 2022 精算库自检
python pkg\triad.py                   # 单跑三重奏精算库
python tests\test_triad.py            # 单跑单元测试
```

## 验收标准（企业级 QA 门）

| 门 | 名称 | 通过条件 |
|---|---|---|
| QA-1 | CODATA 2022 Planck 核算 | ℓ_P/M_P/t_P 相对差 < 1e-6 |
| QA-2 | 三重奏恒等式 κℓ_P=E/E_P | 250 位对标相对差 < 1e-12 |
| QA-3 | 量纲修复 | 修复式比值=1（1e-20 内）、修复式2差<1e-70 |
| QA-4 | 单元测试 | 10 项 100% 通过 |
| QA-5 | 历史验证套件（--legacy） | 无 Traceback/Error/Exception |
| QA-6 | KK 可证伪判定 | 三重奏×额外维被观测排除（矛盾>5 数量级） |

## 核心科学结论

1. **已验证**（已知物理的重组）：v≡c ⟹ u·a=0；量纲修复
   `(κℓ_P)²+(τℓ_P)²=(ωℓ_P/c)²`；κℓ_P=E/E_P；零质量极限 κ=ω/c。
2. **可证伪新结论（本轮核心）**：三重奏若绑定 KK 额外维解释
   （ω_n=nc/R_c ⟹ R_curv=R_c/n），则亚毫米引力实验（R_c<0.1mm）
   与观测曲率（R_curv≥6.4e6 m）矛盾 **5+ 个数量级** → 该解读被排除。
3. **未闭合（OPEN）**：常数生成欠定+循环论证；κ 映射双义；从公理到场方程
   缺场论化步骤。

## 诚实声明

本工程是对给定公理系统的**内部自洽性与可证伪性**检验；已验证内容均为
已知物理恒等式的重组，不构成"被实验证实的大统一"，也不支持"从本源生成
物理常数"的宣称。所有数字可用 `python run_verification.py` 一键复算。
