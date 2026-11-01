# TUFT-r356 · 四力统一方程独立复核与 openuft 根目录整理

> 判词：`R356-REVERIFY-TIDY-R214-ENTRIES31-PASS18-BOUNDARY5-INFO5-FAIL3-REPRO-LAMW-OK-LAMPI-OK-ALPHAW-OK-ALPHAG-OK-RATIO-DELTA-2-2198E-12-TABLE16-16-LOG10-OK-SCALE-R2-OK-DERIV-RESID-1-3579E-30-GX-POSITIVE-YES-CROSS0-2-8001E-61-HTML-SVG5-SELFCONTAINED-YES-UNREPRODUCED2-TIDY-ARCHIVED36-KEPT8-LOOSE126-SUPPLY0`
>
> 红线：独立复核只重算 r214 顶层 JSON 暴露的量并机读对拍，不重写物理、不改前卷数值；目录整理只搬移 openuft 根目录的死脚本与旧日志，不删除可复现驱动、不改任何正文；「一致」是 Decimal 同式重算的一致，不是实验符合；本卷条目不可与 r142–r354 相加。

## 一、判定

- **CLOSED-NEUTRAL（独立复核 + 目录整理）**：r214 的 λ_W / λ_π / α_W / α_G / α_em/α_G 五项、16 格大小表、F=−dU/dr、g(x)、r×F 全部被独立重算复现。
- 复核一致 ≠ 新证据：r214 的动力学统一 FAIL 与数值统一 FAIL 不被翻案，供给 0。

## 二、关键读数

- 力比 α_em/α_G(pp) = 1.235552E+36（电磁比引力强 10^36 量级）。
- 1 fm 四力：G 1.8672E-34 / EM 230.7078 / W 1.6660E-175 / S 392220.0415 N。
- 求导最大残差 1.357923E-30；g(x) 最小 0.091578（恒正）；|r×F|/(|F||r|) ≤ 2.800137E-61。

## 三、目录与可视化

- 归档 36 件 → `90_历史归档/运行脚本归档_2026-11-01/`；保留 8 件驱动；只搬移不删除。
- 重建可视化：`四力统一方程_复核_可视化_r356.html`（自含 HTML + SVG，无外部依赖）。

## 四、控制组与守卫

- 控制组 **42/42**；守卫 **18/18**；条目 **16**（PASS 12 / FAIL 2 / INFO 2）。

## 五、红线

- 独立复核只重算 r214 顶层 JSON 暴露的量并机读对拍，不重写物理、不改前卷数值；目录整理只搬移 openuft 根目录的死脚本与旧日志，不删除可复现驱动、不改任何正文；「一致」是 Decimal 同式重算的一致，不是实验符合；本卷条目不可与 r142–r354 相加。
