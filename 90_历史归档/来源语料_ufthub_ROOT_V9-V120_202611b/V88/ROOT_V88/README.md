# ROOT V88｜量子引力双体纠缠与经典媒介的独立证伪

本科研包延续 V87 的量子力学—Newton—Einstein 弱场联系，研究两个量子质量各处于两个位置分支时，Newton 势能算符能否产生可测的两体纠缠，以及哪些额外因素可以伪装为重力信号。**全部合成数据都是理论模拟，尚未进行真实实验；不能据此宣布引力已被量子化、G 已被推导，或四力已经统一。**

## 复现

```bash
python -m pip install -r requirements.txt
python run_all.py
```

Windows 可运行 `RUN_WINDOWS.bat`；Linux 运行 `sh RUN_LINUX.sh`。交互页面：`web/index.html`，无网络依赖。

## 目录

- `book/ROOT_V88_引力诱导量子纠缠_经典媒介争论与独立证伪研究总论.md`：完整中文理论研究。
- `src/bmv.py`：牛顿量子相位、密度矩阵、退相干、部分转置负性、库仑伪差、经典局部相位通道。
- `tests`：自动单元检查和 SymPy 符号推导。
- `web/index.html`：离线交互模拟器。
- `data/`：合成扫描，文件明确包含 `SYNTHETIC`。
- `results/`：基准精算结果和模拟图表。
- `protocols/`：三个未执行的实验协议。
- `SOURCES.md`：权威论文和科学现状。
- `PROOF_STATUS.md`：已证、条件成立、未证和被排除路线。
- `archive/ROOT_V87.zip`：前一版历史归档。

## 输入与定义

单位统一为 SI。每个质量有两个静止、理想化位置分支；分支距离固定；输入 `m1,m2,d,s1,s2,t,gamma1,gamma2,q1,q2` 需要满足 d>(s1+s2)/2。系统默认 m1=m2=10^-14 kg、d=450 µm、s1=s2=200 µm、t=1 s。局部退相干定义为每个单量子比特的非对角密度矩阵元乘 `exp(-gamma*t)`。

**重要科研边界：** 本文件中的 `negativity` 是计算的模型两体态部分转置负性，不是仪器读数，也不是引力场必须量子化的定理。
