# 实现方式档案：TUFT 原始工作区

[实现方式总览](../README.md) · 归属体系：[s14](../../../01_独立体系/S14_挠率统一场论TUFT/README.md)

- **形态**：M2 数值精算 · M6 书稿
- **位置**：`tuft/`（175 文件 / 2.4 MB，扁平无子目录）
- **状态**：archived（内容已迁入 s14 体系目录）

## 内容

`tuft_r1`–`tuft_r25`、`tuft_Q量子A/B`、`tuft_B_*`、`tuft_D2/D3`、`tuft_O_SCALE` 等成对出现的「.py + _report.txt + .md 文稿」。入口为 `tuft_总索引.md` / `tuft_总索引.py`、`tuft_全书_交付版.md`、`tuft_全景总报告.md`、`tuft_第一性归一化总览.{py,md,json}`、`tuft_判据门禁.py`。

依赖 numpy / scipy / mpmath（另见 `emd_out.log` 涉及 sympy）。

关键词：挠率、结与链环、陈–西蒙斯对偶、三叶结 SU(3) 表示、QNM/ringdown/echo、机电对偶压电实验。

## 与主线 v2–v18 的区别

这是**原始工作区**，编号体系（r1–r25）与主线（v2–v18）不同。主线是后来的规范化产物，带独立审计裁决与本仓可校验的台账。两者不可直接对号入座。

## 使用提醒

状态为 archived：保留供溯源，**结论不自动转移**到 s14 或主线。引用本工作区的数值前，需确认主线是否已复算或勘误。
