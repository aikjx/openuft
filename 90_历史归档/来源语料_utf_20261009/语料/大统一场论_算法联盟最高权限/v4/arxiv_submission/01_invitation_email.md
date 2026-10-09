# 合作验证邀约 · 正式邮件草稿（供真实投递）

> 文档编号：V4-46A-邮件　|　日期：2026-08-19
> 用途：41号邀约的真实投递草稿。投递前请：①替换姓名/机构/邮箱占位符；②按 §0 自检清单确认数据包路径；③由持有方授权后发送。

---

## 主题（Subject）

**Subject: Collaboration invitation — falsifiable GeV-scale dark matter prediction from a normalized-helicity unification framework**

---

## 正文（Body）

Dear [Experimental Collaboration / PI Name],

I am writing on behalf of a research group that has derived a **falsifiable dark-matter prediction** from a normalized-helicity (pure-κ-phase) unification framework, and we would like to invite your collaboration on an independent verification.

**Prediction (summary):**
- Dark matter consists of pure-κ-phase particles (internal torsion τ = 0) on a normalized unit helix.
- These particles have **no electromagnetic or weak coupling — gravity-only**.
- Their mass is predicted at **m_DM ≈ 1.68 GeV** (range 1.6–1.7 GeV).
- The prediction is obtained by two independent routes that converge:
  1. **Geometric-fraction route**: Planck Ω_DM/Ω_b → m_DM ≈ 1.68 GeV (V4-34/36).
  2. **Relic-density route**: standard freeze-out relic density with a weak-scale geometric cross section → m_DM = 1.685 GeV (V4-43), consistent to ~0.4%.

**Falsifiable criteria (for your testing):**
- Underground liquid-Xe experiments (Xenon1T / LUX-ZEPLIN / DARWIN): expect **null nuclear-recoil signals** (gravity-only cross section far below threshold).
- Gamma-ray observatories (Fermi-LAT): expect a low-background "dark region" toward dense dark-matter clumps.
- Mass search: focus the 1–2 GeV channel; a WIMP-like recoil or a nonzero weak/EM cross section in the GeV region would **falsify** the pure-κ-phase claim.
- If mass is found to deviate > 3σ from 1.7 GeV, the geometric abundance framework is falsified.

**What we provide:**
- A complete, reproducible data package: all scripts and reports under `utf/大统一场论_算法联盟最高权限/v4/` (V4-34 through V4-46A).
- Reproduction entry point: `36_暗物质预言数值复核_可检验判据机器零验证.py` — running it reproduces m_DM = 1.678 GeV and the machine-zero closure (residual 0.0).
- A self-check sheet confirming file existence, rerunnable scripts, numeric convergence, and honesty boundaries (see `arxiv_submission/00_self_check_投递自检清单.md`).

**Honesty statement (important):**
- The structural layer (pure-κ-phase classification, abundance framework, testable criteria) is derived from a geometric machine-zero closure.
- The numerical layer (≈1.68 GeV) is measurement-anchored in the sense that the absolute values of α and m_e are **not** claimed to be uniquely derived from first principles (V4-40 NG-X boundary). We do not overclaim.

**Collaboration terms (proposed):**
- Stage 1: you independently rerun the scripts (independent numerical reproduction).
- Stage 2: reanalysis of existing public data (Xenon1T / LUX / Fermi-LAT).
- Stage 3: targeted search in the GeV light-dark-matter channel with our pure-κ criteria.
- Stage 4: joint publication if supported; we prioritize falsification results (scientific integrity first) — we waive priority on negative results.

We would welcome either a collaboration or a critical rebuttal. Both serve the scientific goal.

Sincerely,

[Your Name]
[Affiliation]
[Email]
[Date]

---

## 占位符替换清单（投递前必改）

| 占位符 | 需替换为 |
|---|---|
| `[Experimental Collaboration / PI Name]` | 目标实验组 / 主要研究者姓名 |
| `[Your Name]` | 你的真实署名 |
| `[Affiliation]` | 机构（若拟以机构身份投递） |
| `[Email]` | 真实学术邮箱 |
| `[Date]` | 投递日期 |

---

## 投递对象候选（建议优先级）

| 目标 | 理由 |
|---|---|
| arXiv（hep-ph / astro-ph） | 最快建立公开可证伪记录，供全实验组检索 |
| LUX-ZEPLIN / DARWIN 组 | 液氙直接探测，正对应"零核反冲"判据 |
| Fermi-LAT 组 | 伽马天文低背景判据 |
| Xenon1T 数据再分析组 | 已有公开数据可立即做阶段二再分析 |

**注**：真实投递属外部行为，须由持有方（用户）授权并承担署名与科学责任。本草稿仅提供内容与格式。
