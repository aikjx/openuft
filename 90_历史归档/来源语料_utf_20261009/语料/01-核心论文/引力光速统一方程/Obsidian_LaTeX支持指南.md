# Obsidian LaTeX 完全支持配置指南

## 1. 概述

本文档说明如何为《引力光速统一方程：从空间动力学原理到常数统一的理论推导与验证.md》文档配置完整的LaTeX支持。

## 2. 当前文档的LaTeX格式状态

文档中的LaTeX公式格式**已经完全符合Obsidian标准**：

### 2.1 行内公式格式
```markdown
其中，$Z$ 为**张祥前常数**
```

### 2.2 块级公式格式
```markdown
$$Z = \frac{G \cdot c}{2}$$
```

### 2.3 多行公式格式
```markdown
$$
\begin{aligned}
  \vec{r}(t) &= \vec{C}t \\
  &= x\vec{i} + y\vec{j} + z\vec{k} \tag{2-1}
\end{aligned}
$$
```

## 3. Obsidian配置方法

### 3.1 方法一：使用内置的公式解析器（推荐）

**步骤**：

1. 打开Obsidian的设置（Settings）
2. 搜索"Editor"或"编辑器"
3. 找到"Inline Math"或"行内公式"选项
4. 确保已启用以下功能：
   - ✅ Enable inline math（启用行内公式）
   - ✅ Enable MathJax（启用MathJax）

### 3.2 方法二：使用MathJax插件

如果需要更强大的LaTeX支持，可以安装MathJax插件：

**步骤**：

1. 打开Obsidian的社区插件市场（Community Plugins）
2. 搜索并安装"MathJax"
3. 在插件设置中添加以下配置：

```javascript
{
  "tex": {
    "inlineMath": [
      ["$", "$"],
      ["\\(", "\\)"]
    ],
    "displayMath": [
      ["$$", "$$"],
      ["\\[", "\\]"]
    ],
    "packages": {
      "[+]": [
        "amsmath",
        "amssymb",
        "amsfonts",
        "mathtools",
        "newtx",
        "physics",
        "xcolor"
      ]
    },
    "macros": {
      "vec": ["\\mathbf{#1}", 1],
      "dd": "\\mathrm{d}",
      "dv": "\\mathrm{d}\\mathbf{v}",
      "dvu": "\\mathrm{d}\\mathbf{v}_u"
    }
  },
  "options": {
    "skipHtmlTags": [
      "script",
      "noscript",
      "style",
      "textarea",
      "pre",
      "code"
    ]
  },
  "svg": {
    "fontCache": "global"
  }
}
```

### 3.3 方法三：使用KaTeX插件

KaTeX比MathJax更快，但功能相对较少：

**步骤**：

1. 打开Obsidian的社区插件市场
2. 搜索并安装"KaTeX"
3. 在插件设置中启用以下扩展：
   - ✅ amsmath
   - ✅ amssymb
   - ✅ mathtools

## 4. 文档中使用的LaTeX命令兼容性

### 4.1 基础数学命令（全部支持）

| 命令 | 用途 | 示例 |
|------|------|------|
| `\frac` | 分数 | `\frac{G \cdot c}{2}` |
| `\sqrt` | 平方根 | `\sqrt{C_x^2 + C_y^2}` |
| `\cdot` | 乘号 | `G \cdot c` |
| `\pi` | 圆周率 | `4\pi r^2` |
| `\times` | 叉乘 | `\nabla \times \vec{A}` |
| `\cdot` | 点乘 | `\nabla \cdot \mathbf{g}` |
| `\int` | 积分 | `\int_0^{2\pi}` |
| `\oint` | 闭合积分 | `\oint_S \mathbf{g} \cdot d\mathbf{S}` |
| `\sum` | 求和 | `\sum_{i=1}^{n}` |
| `\partial` | 偏导数 | `\frac{\partial}{\partial t}` |
| `\nabla` | 梯度算子 | `\nabla \phi` |
| `\infty` | 无穷大 | `[0, \infty)` |

### 4.2 向量和矩阵命令（需要额外包）

| 命令 | 用途 | 示例 | 所需包 |
|------|------|------|--------|
| `\vec{}` | 向量（粗体） | `\vec{r}`, `\vec{v}` | 默认支持 |
| `\mathbf{}` | 粗体数学 | `\mathbf{g}`, `\mathbf{C}` | 默认支持 |
| `\hat{}` | 单位向量 | `\hat{r}`, `\hat{\mathbf{z}}` | 默认支持 |
| `\begin{vmatrix}` | 行列式 | `\begin{vmatrix} ... \end{vmatrix}` | amsmath |
| `\begin{bmatrix}` | 矩阵 | `\begin{bmatrix} ... \end{bmatrix}` | amsmath |

### 4.3 特殊符号（需要额外包）

| 命令 | 用途 | 示例 | 所需包 |
|------|------|------|--------|
| `\text{}` | 文本模式 | `\text{kg}^{-1}·\text{m}^4` | 默认支持 |
| `\mathrm{}` | 正体罗马字体 | `\mathrm{d}V` | 默认支持 |
| `\mathsf{}` | 无衬线字体 | `\mathsf{e}_r` | 默认支持 |
| `\mathbf{}` | 粗体字体 | `\mathbf{F}`, `\mathbf{g}` | 默认支持 |
| `\mathcal{}` | 花体字母 | `\mathcal{L}` | 默认支持 |
| `\mathbb{}` | 黑板粗体 | `\mathbb{R}`, `\mathbb{N}` | amssymb |
| `\mathscr{}` | 手写体 | `\mathscr{L}` | mathrsfs |

### 4.4 希腊字母（全部支持）

| 小写 | 大写 | 示例 |
|------|------|------|
| `\alpha` | - | `\alpha` → α |
| `\beta` | - | `\beta` → β |
| `\gamma` | `\Gamma` | `\gamma` → γ |
| `\delta` | `\Delta` | `\Delta` → Δ |
| `\epsilon` | - | `\epsilon` → ε |
| `\theta` | `\Theta` | `\theta` → θ |
| `\phi` | `\Phi` | `\phi` → φ |
| `\psi` | `\Psi` | `\psi` → ψ |
| `\omega` | `\Omega` | `\omega` → ω |
| `\sigma` | `\Sigma` | `\Sigma` → Σ |

### 4.5 物理单位（推荐写法）

文档中使用了`\text{}`来标注物理单位：

```markdown
$Z = 0.010004524012147 \, \text{kg}^{-1}·\text{m}^4·\text{s}^{-3}$
```

**注意**：
- `\,` 表示细小间距，用于分隔数字和单位
- `\text{}` 确保单位以正体显示（符合SI标准）

## 5. Obsidian特定配置

### 5.1 CSS样式优化

为了获得更好的显示效果，可以在Obsidian的主题中添加以下CSS：

```css
/* 数学公式优化 */
.math-block {
  font-size: 1.1em;
  margin: 1.5em 0;
  overflow-x: auto;
}

.math-inline {
  font-size: 1.05em;
}

/* 行内公式间距调整 */
.mjx-chtml {
  padding: 0 0.1em;
}
```

### 5.2 字体配置

如果遇到字体显示问题，可以在设置中配置数学字体：

```json
{
  "mathFont": "Latin Modern Math",
  "mathFontSize": 16,
  "mathLineHeight": 1.5
}
```

## 6. 常见问题解决

### 6.1 公式不显示

**问题**：LaTeX公式显示为原始文本

**解决方案**：
1. 检查是否启用了公式解析器
2. 确保使用的是`$...$`（行内）或`$$...$$`（块级）格式
3. 避免在公式中使用不支持的LaTeX命令

### 6.2 符号显示异常

**问题**：某些符号显示为方框或乱码

**解决方案**：
1. 安装支持Unicode的字体（如Latin Modern Math）
2. 确保MathJax/KaTeX已加载必要的包
3. 尝试使用替代符号表示法

### 6.3 多行公式不显示

**问题**：`aligned`环境中的多行公式不显示

**解决方案**：
1. 确保启用了`amsmath`包
2. 检查公式块是否正确闭合
3. 确保使用了正确的LaTeX语法

### 6.4 中文字符在公式中

**问题**：中文字符在LaTeX公式中显示异常

**解决方案**：
```markdown
错误的写法：$质量 m$
正确的写法：质量 $m$
```

建议在公式外书写中文文本，公式内仅使用LaTeX数学符号。

## 7. 最佳实践

### 7.1 公式编号

文档使用了`\tag{}`来为公式添加编号：

```markdown
$$
\vec{r}(t) = \vec{C}t \tag{2-1}
$$
```

这会生成一个带编号的公式。

### 7.2 公式引用

可以在文档中引用带编号的公式：

```markdown
根据公式 $\eqref{2-1}$，我们可以得出...
```

注意：需要在配置中启用公式引用功能。

### 7.3 复杂公式拆分

对于特别长的公式，建议拆分为多行：

```markdown
$$
\begin{aligned}
  F &= \vec{C}\frac{dm}{dt} \\
    &- \vec{V}\frac{dm}{dt} \\
    &+ m\frac{d\vec{C}}{dt} \\
    &- m\frac{d\vec{V}}{dt} \tag{2-14}
\end{aligned}
$$
```

### 7.4 物理量纲标注

文档中使用了量纲分析，这是很好的实践：

```markdown
量纲验证：
- 万有引力常数 $G$：量纲 $[M^{-1}L^3T^{-2}]$
- 光速 $c$：量纲 $[LT^{-1}]$
- 张祥前常数 $Z$：量纲 $[M^{-1}L^4T^{-3}]$
```

## 8. 验证配置是否成功

配置完成后，可以通过以下测试验证：

### 测试1：行内公式
```
行内公式测试：$E = mc^2$
```
应该显示为：行内公式测试：E = mc²

### 测试2：块级公式
```
$$
\int_0^{\infty} e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$$
```
应该显示为一个居中的积分公式。

### 测试3：向量公式
```
$$
\vec{F} = m\vec{a}
$$
```
应该显示粗体向量的公式。

### 测试4：多行公式
```
$$
\begin{aligned}
  a &= 1 + 2 \\
  b &= 3 + 4 \\
  c &= a + b
\end{aligned}
$$
```
应该显示为多行对齐的公式。

## 9. 文档特殊说明

《引力光速统一方程》文档使用了以下特殊LaTeX特性：

1. **大量向量符号**：`\vec{}`, `\mathbf{}`, `\hat{}`
2. **微分符号**：`\mathrm{d}`（正体d）
3. **物理单位**：`\text{kg}`, `\text{m}`, `\text{s}`
4. **立体角符号**：`\Omega`（欧米伽）
5. **旋度和散度**：`\nabla \times`, `\nabla \cdot`
6. **梯度**：`\nabla \phi`
7. **积分号**：`\oint`（闭合积分）
8. **行列式**：`\begin{vmatrix} ... \end{vmatrix}`

这些特性在配置了适当的LaTeX包后都能正常显示。

## 10. 推荐配置方案

**对于本论文文档，推荐使用以下配置**：

### 最小配置（Obsidian内置）
1. 启用行内公式
2. 启用MathJax
3. 添加`amsmath`包

### 完整配置（MathJax插件）
1. 安装MathJax插件
2. 添加以下包：`amsmath`, `amssymb`, `mathtools`
3. 配置自定义宏（如需要）
4. 启用SVG渲染

### 最佳配置（高级用户）
1. 安装MathJax或KaTeX插件
2. 添加所有常用数学包
3. 配置自定义CSS样式
4. 使用高质量数学字体
5. 启用公式编号和交叉引用

## 11. 性能优化建议

对于包含大量公式的文档：

1. **使用KaTeX而非MathJax**：渲染速度更快
2. **缓存渲染结果**：减少重复渲染
3. **延迟加载**：只在需要时渲染公式
4. **减少复杂公式**：拆分过长的公式

## 12. 总结

本文档的LaTeX格式已经完全兼容Obsidian标准，只需：

1. 启用Obsidian的公式支持
2. 安装MathJax或KaTeX插件（可选）
3. 添加必要的LaTeX包（`amsmath`, `amssymb`等）
4. 配置适当的CSS样式

配置完成后，文档中的所有LaTeX公式都能正确显示，包括：
- 基础数学运算
- 向量和矩阵
- 积分和微分
- 物理公式
- 多行对齐公式
- 带编号的公式

如有任何显示问题，请参考上述"常见问题解决"部分。
