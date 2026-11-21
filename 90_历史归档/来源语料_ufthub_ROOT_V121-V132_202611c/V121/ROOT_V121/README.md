# ROOT V121 | 螺旋谱与引力变分研究

本包为可复现的研究原型，不是四力统一证明或人工引力技术设计。

## 文件
- docs/theory.md：数学模型、变分方程、未解决问题
- src/compute.py：几何谱及工程数量级计算
- data/results.json：实际运行输出
- tests/test_compute.py：五项回归测试

## 运行
python src/compute.py
python -m unittest discover -s tests -v

## 重要限制
数值计算验证的是指定模型的恒等式与量纲估算，不验证新物理假设。圆周谱算子是教学级例子。工程磁场引力估算仅为能量等效点质量代理，非完整 GR 解。
