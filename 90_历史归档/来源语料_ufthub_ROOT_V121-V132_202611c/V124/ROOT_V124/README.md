# ROOT V124 | 正谱权重、五高度伪解与有限尺寸地球第五力验收

**这是可复现的数学研究包，不是四力统一的完成证明，也不是第五力实测发现。**

## 内容
- `reports/ROOT_V124_科研总报告.md`: 定理、计算、物理审计和科研裁定
- `scripts/`: 计算程序（所有数据由合成模型生成）
- `tests/`: 53 项新增测试
- `results/`: JSON 计算值、CSV 合成数据、程序日志与继承测试记录
- `figures/`: 四张数值图
- `references/`, `protocols/`: 可核查文献、预注册方案
- `prior_v123/`: V123 原版压缩包，内部含 V122、V121，可做继承测试

## 环境与复现
需要 Python 3.10+，依赖 `numpy scipy mpmath matplotlib pytest sympy`。可在隔离虚拟环境中执行：

```bash
python -m pip install -r requirements.txt
bash verify_all.sh
PYTHONPATH="$PWD/scripts" python scripts/run_v124.py
```

`verify_all.sh` 先运行 V124 的 53 项测试，再安全解压 V123 并运行其完整历史验证，最后验证当前文件 SHA256。`run_v124.py` 会重写合成 `results/` 文件和 `figures/`，因此若在重生成后需要对原始封存包验签，请使用一份未修改的 ZIP 副本。测试数据中没有外部卫星观测。

**总计 235 项测试 = V124 53 + V123 93 + V122 41 + V121 48。**
