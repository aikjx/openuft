# ROOT V111｜验收和证据分级

本报告记录**源目录测试及 ZIP 归档的独立解压复验**，全部命令已实际执行：

- V111：`pytest tests/test_v111.py` **77 passed**。
- V111：`python -m src.symbolic_audit` **15/15 passed**。
- V111：`python -m src.gravity_metric` **9/9 passed**。
- V110：`pytest tests/test_v110.py` **52 passed**，`python -m src.symbolic_audit` **8/8 passed**。
- V111：Chromium UI **10/10**，包含模式切换、观察量切换、画布渲染及 JavaScript 错误检查。
- 能量积分和修正相位荷残差见 `results/V111_NUMERICAL_SUMMARY.json`；另有 CSV 原始积分轨迹。
- Floquet：\(\min \omega^2(t)=0.888>0\)，但 \(\operatorname{Tr}M\approx-2.007737072020038\)，单周期 \(\det M\approx1\)。不同积分器结果在规定误差内吻合。
- 396 行旧问题保留，编号去重后仍 396 个。

**已完成的独立完整性核验**：35 项 SHA-256 核对（包含 manifest）、36 个 ZIP 归档文件、ZIP CRC 完整性检查以及全新目录内的 `verify_integrity.py → run_all.py → verify_integrity.py → web/browser_smoke.py → verify_integrity.py` 全链路复验均通过。历史 V110 测试 52 项、SymPy 检查 8 项单独复跑通过。

**复现设计**：`verify_integrity.py` 对 `CHECKSUMS.sha256` 中声明的文件逐个计算 SHA-256；ZIP 完整性与全新目录重新运行另行验证。浏览器截图是运行时证据，不是稳定的逐像素数值输出，因此默认不在复测时重写截图。

**限制**：数值守恒误差不等于数学严格证明。对非自治 Floquet 反例的周期特征值虽有高精度交叉算例，仍不是区间认证。引力拓扑项没有**直接**应力贡献，不意味全部 θ–电磁系统无引力。
