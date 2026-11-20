# ROOT-GCL/2.0 实验语言说明

4 份协议是科研实验设计草案，不是连接真实设备的控制脚本。所有行为由设备工程师另行验收；不可自动驱动危险高场/重物。

**状态机** DEFINE→DIMENSION→BASELINE→CALIBRATE→RANDOMIZE→BLIND→ACQUIRE→VETO→INFER→REPLICATE→RELEASE。

`required_raw_columns` 是必需元数据字段示例；严格机器约束还应由实验室专属 JSON Schema、仪器驱动、时间同步及质量控制方案实现。本包对协议基本结构做自动校验，不能认证仪器可靠性。
