# Obsidian LaTeX 快速参考 - 引力光速统一方程

## ✅ 文档状态

**《引力光速统一方程》文档的LaTeX格式已完全兼容Obsidian！**

---

## 📋 已添加的YAML元数据

```yaml
---
title: 引力光速统一方程：从空间动力学原理到常数统一的理论推导与验证
authors:
  - 莫国子
  - 张祥前
type: paper
category: 物理学
tags: [引力, 光速, 统一场论, 空间动力学, 几何因子, 张祥前常数, 引力光速统一方程]
date: 2025-01-01
language: zh-CN
mathjax: true
katex: false
---
```

---

## 🚀 快速配置步骤

### 最快方式（仅需30秒）

1. 打开Obsidian设置 ⚙️
2. 搜索"公式"或"Math"
3. 启用以下选项：
   - ✅ Enable inline math（启用行内公式）
   - ✅ Enable MathJax（启用MathJax）

**完成！** 现在可以正常查看所有公式了。

---

## 📝 文档中的LaTeX格式示例

### 1. 行内公式（$...$）

```markdown
其中，$Z$ 为**张祥前常数**（精确值 $Z = 0.010004524012147$）
```

**显示效果**：其中，Z为**张祥前常数**（精确值 Z = 0.010004524012147）

### 2. 块级公式（$$...$$）

```markdown
$$Z = \frac{G \cdot c}{2}$$
```

**显示效果**：
$$Z = \frac{G \cdot c}{2}$$

### 3. 多行对齐公式（aligned）

```markdown
$$
\begin{aligned}
  \vec{r}(t) &= \vec{C}t \\
  &= x\vec{i} + y\vec{j} + z\vec{k} \tag{2-1}
\end{aligned}
$$
```

**显示效果**：
$$
\begin{aligned}
  \vec{r}(t) &= \vec{C}t \\
  &= x\vec{i} + y\vec{j} + z\vec{k} \tag{2-1}
\end{aligned}
$$

### 4. 带量纲的公式

```markdown
$Z = 0.010004524012147 \, \text{kg}^{-1}·\text{m}^4·\text{s}^{-3}$
```

**显示效果**：Z = 0.010004524012147 kg⁻¹·m⁴·s⁻³

### 5. 向量公式

```markdown
$$\vec{F} = m\vec{a}$$
$$\mathbf{g} = -\frac{G M}{r^2} \hat{r}$$
```

**显示效果**：
$$\vec{F} = m\vec{a}$$
$$\mathbf{g} = -\frac{G M}{r^2} \hat{r}$$

---

## 📊 文档中使用的LaTeX命令统计

| 命令类别 | 数量 | 示例 |
|---------|------|------|
| 基础运算 | 100+ | `\frac`, `\sqrt`, `\cdot`, `\times` |
| 向量/矩阵 | 50+ | `\vec{}`, `\mathbf{}`, `\hat{}` |
| 积分/求和 | 30+ | `\int`, `\oint`, `\sum` |
| 微分/偏导 | 20+ | `\frac{\partial}{\partial}`, `\mathrm{d}` |
| 希腊字母 | 40+ | `\alpha`, `\beta`, `\gamma`, `\omega`, `\Omega` |
| 特殊符号 | 30+ | `\nabla`, `\infty`, `\text{}` |
| 环境命令 | 50+ | `aligned`, `vmatrix`, `bmatrix` |

**总计**：文档中使用了约300+个LaTeX命令

---

## 🎯 核心公式一览

### 1. 引力光速统一方程（最重要）

```markdown
$$Z = \frac{G \cdot c}{2}$$
```

**物理意义**：张祥前常数Z连接了引力常数G与光速c

### 2. 时空同一化方程

```markdown
$$\vec{r}(t) = \vec{C}t$$
```

**物理意义**：时间与空间的数学统一

### 3. 空间螺旋运动方程

```markdown
$$
\vec{r}(t) = r\cos\omega t \cdot \vec{i} + r\sin\omega t \cdot \vec{j} + ht \cdot \vec{k}
$$
```

**物理意义**：空间的圆柱状螺旋式发散运动

### 4. 光速约束方程

```markdown
$$c^2 = (r\omega)^2 + h^2$$
```

**物理意义**：旋转分量与直线分量的勾股关系

### 5. 质量几何化定义

```markdown
$$m = k \cdot \frac{dn}{d\Omega}$$
```

**物理意义**：质量是空间位移条数的度量

### 6. 万有引力定律

```markdown
$$F = G \frac{m_1 m_2}{r^2}$$
```

**物理意义**：经典的引力相互作用公式

### 7. 引力场的散度方程

```markdown
$$\nabla \cdot \mathbf{g} = -4\pi G \rho$$
```

**物理意义**：高斯定理的引力场版本

### 8. 高斯定理

```markdown
$$\oint_S \mathbf{g} \cdot d\mathbf{S} = -4\pi G M$$
```

**物理意义**：引力场通量与质量的关系

---

## 🔧 高级配置（可选）

### 安装MathJax插件

如果需要更强大的LaTeX支持：

1. **安装插件**
   - 设置 → 社区插件 → 浏览
   - 搜索"MathJax" → 安装

2. **配置包**（在插件设置中）
   ```json
   {
     "packages": {
       "[+]": [
         "amsmath",
         "amssymb",
         "mathtools"
       ]
     }
   }
   ```

3. **启用SVG渲染**
   - 在插件设置中勾选"Use SVG for output"

---

## ⚠️ 常见问题

### Q1: 公式显示为文本 `$Z = ...$`

**A**: 检查是否启用了"Enable inline math"

### Q2: 多行公式不显示

**A**: 确保启用了`amsmath`包（需要MathJax插件）

### Q3: 粗体向量显示正常字体

**A**: 使用`\vec{}`或`\mathbf{}`，不要用`\textbf{}`

### Q4: 物理单位显示异常

**A**: 使用`\text{}`包裹单位，如`\text{kg}^{-1}`

### Q5: 公式编号不显示

**A**: 使用`\tag{}`命令，如`\tag{2-1}`

---

## ✅ 验证清单

配置完成后，用以下清单验证：

- [ ] 行内公式 `$E=mc^2$` 正常显示
- [ ] 块级公式 `$$F=ma$$` 居中显示
- [ ] 向量 `\vec{v}` 显示为粗体或带箭头
- [ ] 积分 `\int` 显示为积分符号
- [ ] 多行公式 `aligned` 正确对齐
- [ ] 希腊字母 `\alpha`, `\beta`, `\omega` 正常显示
- [ ] 物理单位 `\text{kg}` 正体显示
- [ ] 公式编号 `\tag{}` 显示在右侧

---

## 📚 相关文档

- 📖 [Obsidian LaTeX完整配置指南](./Obsidian_LaTeX支持指南.md) - 详细配置说明
- 📝 [主论文文档](./引力光速统一方程：从空间动力学原理到常数统一的理论推导与验证.md) - 完整论文内容

---

## 💡 使用技巧

### 技巧1：公式编辑器

在Obsidian中编辑公式时：
- 使用快捷键 `Ctrl/Cmd + E` 打开公式编辑器
- 可以实时预览公式效果
- 支持语法高亮

### 技巧2：公式快捷键

```
Ctrl/Cmd + E      - 插入行内公式 $$
Ctrl/Cmd + Shift + E - 插入块级公式 $$
```

### 技巧3：快速输入希腊字母

在公式输入时，输入 `\alpha` 后按 Tab 键即可自动展开为 α

### 技巧4：公式折叠

对于长公式，可以折叠以节省空间：
```
<details>
<summary>点击展开详细推导</summary>

$$
\begin{aligned}
  \text{详细的推导步骤...}
\end{aligned}
$$

</details>
```

---

## 🎓 Obsidian公式显示特点

Obsidian使用MathJax或KaTeX渲染LaTeX公式，具有以下特点：

1. **响应式设计**：公式会根据屏幕大小自动调整
2. **高分辨率**：支持Retina显示屏，公式清晰锐利
3. **暗色模式**：自动适应深色主题
4. **复制功能**：可以复制公式为LaTeX代码或图片
5. **缩放功能**：支持鼠标滚轮缩放查看细节

---

## 📞 获取帮助

如果遇到问题：

1. 查看完整指南：`Obsidian_LaTeX支持指南.md`
2. 访问Obsidian官方文档
3. 加入Obsidian社区论坛
4. 搜索MathJax文档

---

## 🎉 总结

**《引力光速统一方程》文档已完全兼容Obsidian！**

**只需简单三步即可享受完美的LaTeX显示**：

1. ✅ 启用Obsidian的公式支持
2. ✅ （可选）安装MathJax插件
3. ✅ 开始阅读论文，享受精美的公式显示

**祝阅读愉快！** 🚀
