# ROOT V77 · G 与光速 c 的全维关系研究包

**正式交付状态：** 已建立可以复算的关系、量纲限制、反例和软件测试；**尚未从 c 或螺旋公设无参数独立预测 G，也未完成四力统一证明。**

## 一句话结论

- `G = 2Z/c` 严格成立，当且仅当 `Z := Gc/2`；不是额外决定 G 的定律。
- `G = c² r_g / M`、`G = c³ℓP²/ħ`、`G = αg ħc/m²` 在定义前提下严格成立。
- 真正可检验的关键是 **能否独立算出 `Z`、`ℓP` 或 `αg` 中至少一个**，不能用测得 G 反向设定。
- 不同的额外固定量假设可给出 `G ∝ 1/c`、`c²`、`c³` 或常数；目前无唯一的新普适函数 `G(c)`。

## 文件

- `book/ROOT_V77_G与c关系_严格推导与精算研究专著.md`：17 章中文论证与附录。
- `data/equation_catalog.csv`：54 条核心方程、前提、证明状态、失败模式。
- `data/hypothesis_audit.csv`：30 条攻坚路线、否证条件与实验建议。
- `data/conditional_c_scaling.csv`：51 组**条件思想实验**，非真实变光速数据。
- `data/mass_length_comparison.csv`：电子/质子/普朗克质量的引力长度与康普顿长度。
- `data/earth_GM_degeneracy.csv`：不同 G、M 对应相同 GM 的反例。
- `src/gravity_c.py`：Python 标准库的透明精算核心。
- `src/cli.py`：命令行计算工具。
- `tests/test_gravity_c.py`：58 项 unittest。
- `scripts/symbolic_checks.py`：15 条独立 SymPy 恒等式/秩判定。
- `scripts/numerics.py`：生成 JSON、CSV 与三张 PNG 曲线。
- `web/index.html`：完全离线的浏览器交互计算实验室。
- `results/verification_report.json`：真实运行命令、退出码与测试摘要。
- `SHA256_MANIFEST.csv`：可校验文件哈希（签名不包含在内）。

## 快速操作

Python 3.10+：

```bash
python run_all.py
```

独立计算：

```bash
python -m src.cli summary
python -m src.cli mass 9.1093837139e-31
python -m src.cli from-z 0.01
python -m src.cli vary-c 1.10
```

运行默认 unittest / CSV / JSON 仅依赖 Python 标准库；可选 `numpy`, `matplotlib`, `sympy` 已在 `requirements-optional.txt` 列出，用于图表与符号交叉校验。

浏览器直接打开 `web/index.html` 即可，无需服务器、注册或网络。

## 真实数据来源

详见 `SOURCES.md`。NIST CODATA 2022 的 G 是**带不确定度的测得值**；c 是 SI 定义精确值；JPL 的 GM 是引力参数，不能误称为不依赖 G 的物体质量测量。

## 已知限制

1. **数学验证不是新物理实验。** 回归测试证明实现与公式一致，不能据此证明新的 G 起源。
2. 假设 c 随时间变化的图是不同额外边界条件的思想实验；没有真实测量支持。
3. 电子/质子/普朗克质量对比同时含有 G 输入，不能把 r_g 与 Compton 长度比的数值当作独立预测。
4. 所有模拟以弱场、标准 GR/Newton 为参照，不假装解决量子引力。
5. 文中所有原始资料 URL 均列在 `SOURCES.md`；请按源文献更新观测值。
