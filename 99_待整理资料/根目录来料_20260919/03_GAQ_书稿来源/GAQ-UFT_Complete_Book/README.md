# GAQ‑UFT《万物几何统一场论——全维分析与第一性原理推导》

> Geometric‑Axiomatic Quantum Unified‑Field Theory
> 完整书籍源码包 · 约 1 020 000 字框架 · 本地一键编译为 PDF

---

## 1. 包结构说明

```
GAQ‑UFT_Complete_Book/
├─ main_book.md          # 封面 + 全书总目录（主入口）
├─ preface.md            # 序言、献词、理论发展史
├─ Volume_00_Foundations/      # 第0卷 基础数学与公理地基
├─ Volume_01_Geometric_Vacuum/ # 第1卷 螺旋真空
├─ Volume_02_Constant_Geometry_Origins/ # 第2卷 常数几何本源
├─ Volume_03_Particle_Spectra/         # 第3卷 粒子谱
├─ Volume_04_Lorentz_Spacetime_Extension/ # 第4卷 洛伦兹时空拓展
├─ Volume_05_Prediction_Falsification/    # 第5卷 预言与证伪
├─ Volume_06_Open_Problems_Future/        # 第6卷 开放问题
├─ Supplemental_Code/   # 全部 Python 高精度仿真（mpmath 200 位）
├─ LaTeX_Templates/     # book_template.tex / references.bib
├─ Figures_TikZ/        # 矢量插图（TikZ，替代 Mermaid）
├─ compile_book.bat     # Windows 一键编译
├─ compile_book.sh      # Linux / macOS 一键编译
└─ README.md
```

每卷子目录下的 `*.md` 为分章正文；编译脚本会把 `preface.md` 与全部卷章按下面的固定顺序拼接为一个大 Markdown，再由 pandoc 经 XeLaTeX 渲染为单本 PDF。

---

## 2. 编译依赖

| 工具 | 用途 | 安装方式（示例） |
|------|------|----------------|
| Pandoc (≥3.0) | Markdown → LaTeX/PDF | `choco install pandoc` / `apt install pandoc` |
| TeX Live (含 XeLaTeX) | 渲染中文 PDF | `apt install texlive-xetex texlive-lang-chinese` |
| 字体 | 中文（如 思源宋体 Source Han Serif / 宋体） | 系统自带或自装 |
| Python 3.11+ | 运行 Supplemental_Code | `pip install mpmath numpy matplotlib` |

---

## 3. 一键编译

**Windows：**
```
双击 compile_book.bat
```
或命令行：`compile_book.bat`

**Linux / macOS：**
```bash
chmod +x compile_book.sh
./compile_book.sh
```

脚本默认输出 `GAQ-UFT_Complete_Book.pdf`（与源码同目录）。

---

## 4. 只跑数值验证

```bash
cd Supplemental_Code
pip install mpmath numpy matplotlib
python frenet_high_prec.py
python geometry_verify.py
python koide_simulation.py
python plot_helix_3d.py
```

---

## 5. 阅读建议

- 熟悉微分几何者：直接读 `Volume_00_Foundations`。
- 先看物理图像者：先读 `Volume_01_Geometric_Vacuum`，公式再回查数学附录。
- 全书核心钥匙：**严格区分“数学必要条件”与“物理公设（A3 齐性）”**。

---

## 6. 版权与声明

本包为理论框架源码，内容按“可推导／可计算／可证伪”原则组织。书中标注的“猜想”“开放问题”章节不代表已证实结论。对标数据采用 CODATA‑2022。
