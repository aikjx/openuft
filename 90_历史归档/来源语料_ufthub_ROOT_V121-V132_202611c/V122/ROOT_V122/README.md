# ROOT V122 研究包

- `docs/研究报告.md`：理论、公式、推导边界、工程含义与证伪路线。
- `src/verify.py`：只使用 Python 标准库，计算几何、谱、旋转重力、磁能、Yukawa 示范。
- `tests/test_verify.py`：五项数学/程序测试。
- `results/calculations.json`：运行脚本生成的精算数据。
- `results/test_log.txt`：实际运行测试记录。

运行：`python src/verify.py && python -m unittest discover -s tests -v`

研究结论：建立可复算候选模型及约束，不构成四力统一或人工引力的实验发现。单位：理论 c=1，工程量恢复 SI。
