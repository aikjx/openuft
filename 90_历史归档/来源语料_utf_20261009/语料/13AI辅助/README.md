# 生成包含LaTeX公式且中文不乱码的论文图片

## 功能介绍

这是一个用于生成包含LaTeX公式且中文显示正常的论文图片的Python脚本。该脚本整合了Gemini-2.5-Flash和Grok-4-Fast的最佳实践，支持Windows/macOS/Linux操作系统，能够自动检测并使用系统中安装的中文字体，生成高质量的论文图片。

### 主要特性

- ✅ 支持Windows/macOS/Linux操作系统
- ✅ 自动检测并使用系统中安装的中文字体
- ✅ 集成LaTeX渲染，支持复杂数学公式
- ✅ 提供论文级别的美化样式
- ✅ 支持多种输出格式（png, svg）
- ✅ 支持单图和多子图布局
- ✅ 详细的注释和使用示例

## 环境要求

### 1. Python环境

- Python 3.7+（推荐Python 3.9或更高版本）

### 2. 依赖库

- matplotlib: 用于绘图和LaTeX渲染
- numpy: 用于生成示例数据

### 3. LaTeX发行版

为了正确渲染LaTeX公式，需要安装LaTeX发行版：

#### Windows系统
- 推荐安装 [MiKTeX](https://miktex.org/download)（支持按需安装包）
- 或安装 [TeX Live](https://tug.org/texlive/windows.html)

#### macOS系统
- 安装 [MacTeX](https://tug.org/mactex/)（包含TeX Live）

#### Linux系统
- Ubuntu/Debian: `sudo apt-get install texlive-full` 或 `sudo apt-get install texlive-latex-base texlive-fonts-extra texlive-lang-chinese`
- Fedora: `sudo dnf install texlive-scheme-full`
- Arch Linux: `sudo pacman -S texlive-most texlive-zhwin`

**重要提示**：确保安装了支持中文的LaTeX宏包，如`xeCJK`或`ctex`。如果安装的是`texlive-full`，通常已经包含了这些宏包。

## 安装和配置

### 1. 安装依赖库

使用pip安装所需的Python库：

```bash
pip install matplotlib numpy
```

### 2. 下载脚本

将`latex_chinese_plot.py`脚本下载到本地目录。

### 3. 配置中文字体（可选）

脚本会自动检测并使用系统中安装的中文字体。如果需要使用特定的中文字体，可以修改脚本中的`chinese_fonts`字典，添加或修改字体路径：

```python
self.chinese_fonts = {
    'Windows': [
        'C:/Windows/Fonts/simhei.ttf',      # 黑体
        'C:/Windows/Fonts/msyh.ttc',        # 微软雅黑
        # 添加其他Windows字体路径
    ],
    # 其他操作系统的字体配置...
}
```

## 使用示例

### 1. 运行示例脚本

直接运行脚本即可生成示例图片：

```bash
python latex_chinese_plot.py
```

脚本会生成两张示例图片：
- 单图示例：包含正弦、余弦曲线和LaTeX公式
- 子图示例：2x2布局，展示多种数学函数

生成的图片将保存到`./figures`目录下，支持png、svg格式。

### 2. 在自己的项目中使用

可以将`LatexChinesePlot`类导入到自己的项目中使用：

```python
from latex_chinese_plot import LatexChinesePlot

# 创建绘图实例
plotter = LatexChinesePlot(figsize=(10, 6), dpi=300, font_size=14)

# 生成示例图片
plotter.create_example_plot(save_dir='./my_figures')
```

### 3. 自定义图片

可以继承`LatexChinesePlot`类，扩展其功能，创建自定义的论文图片：

```python
class MyPlot(LatexChinesePlot):
    def create_custom_plot(self, save_dir='./figures'):
        # 自定义绘图逻辑
        # ...
        pass

# 使用自定义绘图类
my_plot = MyPlot()
my_plot.create_custom_plot()
```

## 常见问题和解决方案

### 1. 中文显示乱码

**可能原因**：
- 未安装LaTeX中文宏包
- 未找到合适的中文字体
- LaTeX引擎配置错误

**解决方案**：
- 确保安装了`xeCJK`或`ctex`宏包
- 检查系统中是否安装了中文字体（如黑体、微软雅黑等）
- 确保LaTeX引擎设置为`xelatex`或`lualatex`（脚本已默认设置）
- 手动修改脚本中的字体路径，指向系统中存在的中文字体

### 2. LaTeX公式渲染错误

**可能原因**：
- LaTeX发行版未正确安装
- LaTeX宏包缺失
- LaTeX语法错误

**解决方案**：
- 验证LaTeX发行版是否正确安装（在命令行中运行`xelatex --version`）
- 确保安装了所需的LaTeX宏包（`amsmath`, `amssymb`, `xeCJK`等）
- 检查LaTeX公式语法是否正确，特别是美元符号是否成对出现

### 3. 图片生成失败

**可能原因**：
- Python依赖库版本不兼容
- 保存目录权限问题
- 系统资源不足

**解决方案**：
- 更新matplotlib和numpy到最新版本
- 确保保存目录存在且有写入权限
- 尝试减小图片尺寸或降低分辨率

## 脚本结构

```
LatexChinesePlot
├── __init__()          # 初始化绘图类
├── _configure_matplotlib()  # 配置matplotlib
├── _load_chinese_font()     # 加载中文字体
├── create_example_plot()    # 创建单图示例
├── create_subplot_example() # 创建子图示例
└── main()                # 主函数
```

## 输出格式说明

脚本支持生成三种格式的图片：

- **PNG**：位图格式，适合在网页和演示文稿中使用
- **SVG**：矢量格式，适合在需要编辑的场景中使用

## 美化样式说明

脚本使用了论文级别的美化样式，包括：

- 合适的字体大小和行宽
- 美观的颜色方案
- 清晰的坐标轴和图例
- 适当的网格线
- 移除了顶部和右侧的边框
- 紧凑的布局

## 扩展方法

可以通过以下方式扩展脚本功能：

1. **添加新的绘图方法**：在`LatexChinesePlot`类中添加新的绘图方法
2. **修改美化样式**：调整`_configure_matplotlib()`方法中的参数
3. **支持更多字体**：扩展`chinese_fonts`字典，添加更多字体路径
4. **支持更多输出格式**：修改`create_example_plot()`和`create_subplot_example()`方法，添加更多输出格式

## 许可证

本脚本基于MIT许可证开源，可自由使用和修改。

## 更新日志

### v1.0.0 (2024-12-20)

- 初始版本
- 支持单图和子图生成
- 支持三种输出格式
- 自动检测中文字体
- 论文级别的美化样式

## 贡献

欢迎提交Issue和Pull Request，共同改进这个脚本。

## 联系信息

如有问题或建议，请通过以下方式联系：

- 作者：算法联盟
- 日期：2024-12-20
- 版本：v1.0.0