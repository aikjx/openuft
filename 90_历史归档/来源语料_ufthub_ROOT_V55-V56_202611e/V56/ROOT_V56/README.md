# ROOT V56 · 离线三维地球联合力场实验室

## 运行

1. 双击 `index.html`（无需服务器、无需外部 JavaScript CDN）。
2. 拖动旋转地球，滚轮缩放；修改纬度、经度、高度、质量、电荷、速度和测试电场。
3. 查看场强及矢量方向。箭头长度归一化，仅用于表达方向。
4. Python 3：`python generate_data.py` 生成 624 行网格；`python -m unittest discover -p 'test_*.py' -v` 运行 12 项测试。

## 文件
- `index.html`：离线交互三维投影地球实验室。
- `model.py`：独立 Python SI 单位计算引擎。
- `test_model.py`：12 项数值和矢量性质测试。
- `generate_data.py`：数据生成脚本。
- `earth_field_grid.csv`：624 个采样点的场矢量。
- `verified_samples.json`：典型位置数值结果。
- `研究专著.md`：理论、推导、模型边界、研究计划。
- `test_results.txt`：测试日志。

## 科学边界
模型是球形地球 + J₂ + 地轴对齐的理想磁偶极 + 可选径向合成电场。不是完整真实地磁/地球重力/电场数据拟合，也不是已经证明的四力大统一。网页使用 Canvas 三维投影而不是 WebGL 三维网格渲染，具有可交互旋转和缩放功能。无网络依赖。
