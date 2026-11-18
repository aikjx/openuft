# 来源与证据等级（2026-11-17）

- NIST CODATA 2022: https://physics.nist.gov/cuu/pdf/JPCRD2022CODATA.pdf — G=6.67430(15)×10⁻¹¹, c SI exact. G 不是理论预测。
- NIST Measurement of G: https://www.nist.gov/publications/measurements-newtonian-constant-gravitation-g — 测量方法与系统误差综述。
- MICROSCOPE 2022 final: https://doi.org/10.1103/PhysRevLett.129.121102 — η(Ti,Pt)=[−1.5±2.3(stat)±1.5(syst)]×10⁻¹⁵；非新力发现。
- PDG Review of Particle Physics 2026: https://pdg.lbl.gov/2026/reviews/standard_model_and_related.html — 规范相互作用和新物理约束。
- Electromagnetic stress-energy: https://phys.libretexts.org/Bookshelves/Relativity/Special_Relativity_%28Crowell%29/10%3A_Electromagnetism/10.06%3A__Stress-energy_tensor_of_the_electromagnetic_field — 教学推导。
- M. Duff, How fundamental are fundamental constants? https://arxiv.org/abs/1412.2040 — 有量纲常数变化的单位制限制。

## 数值来源政策

`src/core.py` 中的 CODATA 参考值作为实验输入使用；`MU0` 采用近似参考常数，注明不是 2019 年后 SI 精确值。所有 CLI 与网页结果是理论估算或人工合成测试，没有真实装置测得的新引力数据。
