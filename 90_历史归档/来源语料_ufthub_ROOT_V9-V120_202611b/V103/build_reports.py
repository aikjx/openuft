from pathlib import Path
import csv,json,math
root=Path(__file__).parent
res=json.loads((root/'results/V103_THEORY_SUMMARY.json').read_text(encoding='utf-8'))
g=res['numerical_geometry'];p=res['radiation_and_power'];b=res['boost_counterexample']
new=[
 ('V103-358','四速度与三维曲率/挠率的观察者依赖性','CONDITIONAL_MATH_PROVED','构造轴向洛伦兹变换反例并复算固有加速度不变量'),
 ('V103-359','闭合空间结的必要辐射功率下界','CONDITIONAL_MATH_PROVED','由 Liénard+Fáry–Milnor+Cauchy 严格求得并量纲校核'),
 ('V103-360','等效每周期补偿电压与路径均值电场','CONDITIONAL_MATH_PROVED','只作为外部补偿能量账本，不当成可直接制造的静电场'),
 ('V103-361','静电静磁场无法对完整重复辐射轨道提供净功','CONDITIONAL_MATH_PROVED','明确单值静电势、周期相同近场状态及能量守恒条件'),
 ('V103-362','周期运动的 Schott 近场能量边界项','OPEN_DYNAMICS','以粒子+束缚场+远场统一能流证实周期边界项确实抵消'),
 ('V103-363','给出实际非保守 RF 或时变场供能设计','OPEN_ENGINEERING','满足 Maxwell、轨道稳定和真实电压/功率预算'),
 ('V103-364','对 V100 连续线圈场周期候选给出区间 Newton 证书','OPEN_MATH','报告 Krawczyk 包含关系、全部误差界和高精度独立复算'),
 ('V103-365','认证 V100 连续曲线嵌入性与结类型','OPEN_MATH','给出无自交的连续下界和拓扑保持的投影证书'),
 ('V103-366','纳入 Lorentz-Abraham-Dirac 或 Landau-Lifshitz 辐射反作用','OPEN_PHYSICS','指定有效域和初始条件，不允许 runaway/pre-acceleration 未审计'),
 ('V103-367','在有限线圈/电源模型下完成 Poynting 能量账本','OPEN_ENGINEERING','包含导体欧姆热、远区辐射、线圈电源与颗粒能量'),
 ('V103-368','从曲线 Frenet 标架建立洛伦兹协变内部自由度模型','OPEN_THEORY','作用量、无鬼模/超光速、正确标准模型/GR 极限'),
 ('V103-369','独立导出 G 与全部四力耦合并给出可证伪预言','OPEN_FOUNDATION','不允许把实测 G 通过新定义循环输入；与实验和量子异常审计相容')]
base=root/'ledger/ALL_357_ISSUES.csv'
with base.open(newline='',encoding='utf-8-sig') as f:rd=list(csv.DictReader(f)); cols=list(rd[0].keys())
assert len(rd)==357,len(rd)
with (root/'ledger/ALL_369_ISSUES.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(rd)
 for id_,issue,status,accept in new:
  w.writerow({'id':id_,'issue':issue,'status_or_current_result':status,'acceptance_criterion':accept,'source_version':'V103'})
with (root/'ledger/V103_NEW_12_ISSUES.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['id','issue','status','acceptance_criterion']);w.writerows(new)

def fmt(v,n=9):return f'{v:.{n}g}'
report=f'''# ROOT V103｜螺旋动力学的协变与辐射供能严格审计

**研究日期：2026-11-19。研究性质：已知理论条件推论 + 原始数值数据交叉计算 + 反例构造。**

> **科学等级及结论**：严格成立的仅为明示假设下的经典几何与电动力学推论。项目没有严格证明 V100 连续外源磁场中的精确结状周期轨道，也没有找到新基本力、量子引力理论或无参数 G。数据为历史 THEORY 数值模拟，不是自然实验。

## 0. 问题与输入的来源

沿用 ROOT V102 的 357 项问题台账及 V100 的 1,201 点理论轨迹。原始 V102 ZIP 放在 `archive/ROOT_V102_original.zip`，输入数据独立复制到 `data/V100_ORBIT_21Q_INPUT_THEORY.csv`，V103 新增 12 项，总计 369 项，状态明确区分 CLOSED_MATH 和 OPEN。

## 1. 定理：经典点电荷闭合结的辐射功率必要下界（条件成立）

设 Minkowski 平直时空某惯性系中，单个固定电荷 q 非零、固定速率 0<v<c，平滑嵌入的 **非平凡空间结** 长度 L，曲率 κ(s)。粒子受外界作用保持该轨迹，加速度与速度正交。假设采用经典 Liénard 远区辐射表达，忽略轨迹辐射反作用对指定几何的改动：

\\[
E_{{\\rm rad}}=\\frac{{q^2\\gamma^4v^3}}{{6\\pi\\epsilon_0c^3}}\\oint\\kappa^2\\,ds.
\\]

Cauchy–Schwarz：\\(\\oint\\kappa^2ds\\ge K^2/L\\)，其中 \\(K=\\oint\\kappa ds\\)。非平凡、光滑、无自交结的 Fáry–Milnor 定理给出 \\(K\\ge4\\pi\\)。所以

\\[
\\boxed{{E_{{\\rm rad}}\\ge\\frac{{8\\pi q^2\\gamma^4v^3}}{{3\\epsilon_0c^3L}}}}.
\\]

轨道周期 T=L/v，进一步

\\[
\\boxed{{\\overline P_{{\\rm required}}\\ge\\frac{{8\\pi q^2\\gamma^4v^4}}{{3\\epsilon_0c^3L^2}}}}.
\\]

两个不等式都是**必要条件**，不保证装置、轨道及结在真实辐射反作用动力学下存在。对任何一般闭合曲线，Fenchel 下界仅 K≥2π，不能误把四倍的结下界用于自交曲线、普通圆或未经认证的数值结。

**量纲**：[E]=ML²T⁻²，[P]=ML²T⁻³，[E/(|q|L)]=MLT⁻³I⁻¹，对应电场 V/m。

## 2. 定理：静态、全局保守电场 + 磁场不能自发补偿正辐射能量

对整个周期的粒子与近场（束缚场）能量变化作完整记账，若位置、速度、外部静态场及束缚场状态在周期端点重复，近场边界项变化为 0。若静态电场存在全局**单值**静电势 \\(\\phi\\)，则 \\(\\oint q\\mathbf E\\cdot d\\mathbf x=-q\\oint d\\phi=0\\)；磁力做功恒为零。若远区周期辐射能量严格正，则不可能在无其它能量供给时同时保持精确周期轨道和粒子/近场状态重复。

**适用范围**：不包括时变 RF 加速场、非保守外部电动势、源本身随周期供能、核物理内能释放、或非平凡拓扑情况下未定义全局单值势的例外。实际自洽辐射反作用模型的 Schott 近场边界项应使用完整能量守恒验证。此处不能直接将牛顿式 F=ma 加上一个任意耗散力而宣称完成自洽量子电动力学。

**工程必要条件**：若采用时变场供应能量，必须 \\(\\int_0^Tq\\mathbf E_{{\\rm drive}}\\cdot\\mathbf vdt\\ge E_{{\\rm rad}}\\)，实际含外加损耗将大于辐射值。

## 3. 参考系反例：三维挠率不是洛伦兹不变量

在参考系 S，带电粒子沿 xy 平面半径 R 的匀速圆轨道，角频率 \\(\\omega=v/R\\)，因此 \\(\\tau_S=0\\), \\(\\kappa_S=1/R\\)。对 z 轴做相对速度 u 的 Lorentz boost，坐标时间 \\(t'=\\gamma_u t\\)，轨迹变为

\\[
\\mathbf x'(t')=(R\\cos(\\omega t'/\\gamma_u),R\\sin(\\omega t'/\\gamma_u),-ut').
\\]

故新系内三维挠率 \\(\\tau'=-u(\\omega/\\gamma_u)/v'^2\\ne0\\)，曲率 \\(\\kappa'=R(\\omega/\\gamma_u)^2/v'^2\\)；其中 \\(v'^2=v^2/\\gamma_u^2+u^2\\)。反过来，两惯性系中四加速度的固有大小都为 \\(\\gamma_v^2 v^2/R\\)，为标量不变量。

**数值示例**：R=10 mm，实验室粒子速度 0.6c，轴向 boost=0.4c：

- 观察者 S：κ={fmt(b['lab_curvature_inv_m'])} m⁻¹，τ=0；
- 观察者 S′：κ={fmt(b['boosted_curvature_inv_m'])} m⁻¹，τ={fmt(b['boosted_torsion_inv_m'])} m⁻¹；
- 两者固有加速度均约 {fmt(b['lab_proper_accel_m_s2'])} m/s²，计算相对偏差 {fmt(b['invariant_relative_error'],3)}。

**结论**：把普通三维曲率或挠率直接等同于一个普适基本力耦合是错误的。若提出更深层的内部螺旋变量，必须先定义完整 Lorentz 协变量及其在作用量中的动力学意义。

## 4. 独立数值复算：V100 历史理论轨迹（不代表实物观测）

使用 V102 存档的 V100 三维点数据，以闭合多边形边长和相邻边的空间转角重算 \\(L,K,K_2\\)，其中 \\(K_2=\\oint\\kappa^2 ds\\) 为离散估计。无自交和准确结型尚无连续数学证书，因此使用“非平凡结下界”时仍须声明**条件性**。

| 量 | 本轮复算 |
|---|---:|
| 输入点数 | {g['n']} |
| 轨道长度 L | {fmt(g['L'],13)} m |
| 离散总曲率 K | {fmt(g['K'],13)} |
| K₂ | {fmt(g['K2'],13)} m⁻¹ |
| 速度 v | 0.1c |
| 周期 T | {fmt(p['period_s'],13)} s |
| 所需辐射补偿 E_rad | {fmt(p['energy_rad_J'],13)} J |
| 结下界（仅若连续轨道是非平凡结） | {fmt(p['topological_energy_floor_J'],13)} J |
| 平均辐射功率 | {fmt(p['avg_power_W'],13)} W |
| 结下界平均功率 | {fmt(p['minimum_power_W'],13)} W |
| 平均所需供电电压的能量等效值 E_rad/|q| | {fmt(p['compensation_voltage_V'],13)} V |
| 以路径长归一的等效切向电场 | {fmt(p['equivalent_tangential_E_V_per_m'],13)} V/m |
| E_rad / 结下界 | {fmt(p['ratio_to_floor'],12)} |

这两个等效电学量是**周期能量补偿的平均账本值**，不是声称能用均匀静电场沿闭环供电。V100 轨道经典辐射损失约占电子动能的 {fmt(res['loss_fraction_per_period'],8)} 每个 5 圈周期，不是高能微观的量子电磁辐射测量。

## 5. 不能从曲率/结型直接反推全空间磁能

V102 局部关系只决定 \\(B_\\perp=\\gamma mv\\kappa/|q|\\)。轨道切向磁场可以自由变化，而且全空间磁场源及边界条件未定。历史 V95 指定的管状矢势构造有 \\(U_B=O(\\epsilon^2)\\)、典型电流密度 \\(J=O(\\epsilon^{{-1}})\\)，提示若不加最大电流密度、最小源距离等约束，不存在仅从一条轨道几何推出正的普适总磁能下界的简单推理。此为对任意外源构造方案的限制，不能代替真实线圈优化。

## 6. 与量子引力和四力统一的边界

上述研究仍然属于 Maxwell + Lorentz + 经典辐射 + 曲线几何。它尚未包含 QCD 色荷 SU(3)、弱手征 SU(2)、Higgs 机制、重整化、无异常作用量，或几何量子化。不能仅因为在这些公式中出现 κ、τ、ω，就宣称四力来自一套运动。ROOT 的统一目标仍需非循环 G 预测、GR/标准模型极限、独立的新观测量与真实实验验证。

## 7. 下一批必需任务（优先顺序）

1. V100 的连续有限截面 Maxwell 场：从有限精度射击解升级为 Krawczyk/区间 Newton 存在性证书；同时给出周期归一、轨道相空间共维数和线圈积分误差。
2. 连续轨道的拓扑认证：自交最小间隔、切线/曲率上界、投影误差与 Knot invariant 的误差证明。
3. 约化 Poincaré 截面的 Floquet 稳定性验证，避免全空间冗余守恒量。
4. 加入 Landau–Lifshitz 辐射反作用的受控近似及外部 RF 驱动，逐周期完成 Poynting 守恒账本。
5. 若探索内部螺旋的物理本源，必须提出协变作用量，并至少恢复已确立 Maxwell/GR/SM 结果，且明确预测一个不可由现有模型重参数化得到的实验差异。

## 8. 参考文献（外部已知研究，不是本项目实验）

- J. W. Milnor, *On the Total Curvature of Knots*, Ann. Math. (1950): https://math.mit.edu/~hrm/papers/milnor-kinky.pdf
- Fáry–Milnor 定理综述： https://pure.mpg.de/rest/items/item_3583300_2/component/file_3583301/content
- Fermilab 对磁场不做功与加速电场供能的说明：https://www.fnal.gov/pub/science/inquiring/questions/p_accelerators.html
- Synchrotron radiation and RF replenishment: https://doi.org/10.1007/978-3-030-34245-6_6
- Radiation reaction / Schott energy bookkeeping: https://doi.org/10.1119/1.4914421
'''
(root/'research/ROOT_V103_数学证明_协变反例_能量闭环.md').write_text(report,encoding='utf-8')
readme='''# ROOT V103｜研究代码与复现包

**未证明完整统一场论。** 本包为经典电磁力、空间结几何、辐射补偿的条件数学推论与历史模拟复算。所有图片、数据为 THEORY，不是观测结果。

## 内容

- `src/v103_core.py`: 数值核心；包括非平凡结辐射下界、供能下界、洛伦兹 boost 的挠率反例、离散轨迹曲率积分。
- `src/symbolic.py`: 9 项 SymPy 代数和 SI 量纲审计。
- `src/generate.py`: 使用 V100 原轨迹（存自 V102）计算 CSV/JSON 和两张图。
- `tests/test_v103.py`: 28 项 pytest 测试。
- `data/`: V100 轨迹（非观察数据）；`results/`、`figures/`: 合成计算结果。
- `research/`: 中文严谨推导、假设及不足。
- `ledger/`: 原 V102 的 357 项与 12 项新问题，共 369 项。
- `archive/ROOT_V102_original.zip`: 上一版原始归档，供独立历史检查。
- `web/index.html`: 完全离线的参数化互动页面，无外部依赖。
- `CHECKSUMS.sha256`: SHA-256 完整性清单；`MANIFEST.json`: 文件元数据。

## 运行

```bash
python -m pip install -r requirements.txt
python run_all.py
python -m pytest -q tests
```

历史 V102 复测可解压 `archive/ROOT_V102_original.zip` 后在其根目录运行 `python -m pytest -q tests`。不要求浏览器联网。

**验收边界**：单元/符号测试只保证代码对指定模型的正确性；严格的连续线圈场周期轨道存在性、三维结拓扑证明、反作用自洽、四力统一仍 OPEN。
'''
(root/'README_CN.md').write_text(readme,encoding='utf-8')
# standalone interactive page for exploring the analytical bound, not simulations
html='''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>ROOT V103 · 螺旋能量闭环实验室</title><style>
:root{color-scheme:dark}body{margin:0;background:#0d1119;color:#e8edf4;font:15px/1.6 system-ui,-apple-system,'Microsoft Yahei',sans-serif}main{max-width:950px;margin:auto;padding:30px 22px}.muted{color:#9aafc8}.panel{background:#151e2c;border:1px solid #2b3950;padding:19px;border-radius:15px;margin-bottom:16px}h1{font-size:26px;margin:0 0 4px}h2{font-size:17px;margin:0 0 12px}label{display:block;margin-top:12px}input{width:100%;accent-color:#6bd9c5}b.value{color:#7ddfcf}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.stat{background:#0d1523;border-radius:10px;padding:14px;font-variant-numeric:tabular-nums}.stat small{display:block;color:#a6b8cf}.stat strong{display:block;font-size:20px}svg{width:100%;height:auto}footer{color:#96aac1;font-size:13px;margin-top:16px}@media(max-width:640px){.grid{grid-template-columns:1fr}}</style></head><body><main><h1>ROOT V103 · 协变与辐射闭环</h1><p class="muted">条件性经典模型 · 参数可调 · 所有值都是理论计算，不是实验数据，也不是四力统一证明。</p><section class="panel"><h2>实验参数</h2><label>速度 β = v/c：<b class="value" id="betav"></b><input id="beta" type="range" min="0.01" max="0.9" step="0.01" value="0.1"></label><label>闭环轨迹长度 L：<b class="value" id="lv"></b><input id="length" type="range" min="0.02" max="0.5" step="0.001" value="0.162"></label><label>沿轴向的观察者 boost u/c：<b class="value" id="uv"></b><input id="boost" type="range" min="-0.8" max="0.8" step="0.02" value="0.4"></label></section><section class="panel"><h2>非平凡空间结的辐射下界（若轨道已认证为无自交非平凡结）</h2><div class="grid"><div class="stat"><small>最低每周期能量</small><strong id="energy"></strong></div><div class="stat"><small>最低平均供能功率</small><strong id="power"></strong></div><div class="stat"><small>最低每周期等效电压</small><strong id="voltage"></strong></div><div class="stat"><small>最低等效切向电场</small><strong id="efield"></strong></div></div></section><section class="panel"><h2>为什么三维挠率不是协变的？</h2><p class="muted">参照系 S 中半径 10 mm、速度 0.6c 的圆轨道有挠率 0。沿 z 轴 boost 后，轨迹成为螺旋，但固有加速度不变。</p><div class="grid"><div class="stat"><small>观察者 S′ 的曲率</small><strong id="kappa"></strong></div><div class="stat"><small>观察者 S′ 的挠率</small><strong id="torsion"></strong></div></div><svg viewBox="0 0 600 200" aria-label="变化的三维螺旋轨迹示意"><path id="path" stroke="#7ddfcf" stroke-width="2.6" fill="none"/></svg></section><footer>由 Maxwell–Lorentz 与经典 Liénard 辐射计算；周期轨道的真实存在性、长期稳定性与能量反馈仍需独立证明。</footer></main><script>
const c=299792458,eps=8.8541878188e-12,e=1.602176634e-19,pi=Math.PI;
function fmt(x){return x.toExponential(5)}
function render(){const beta=+document.querySelector('#beta').value,L=+document.querySelector('#length').value,u=+document.querySelector('#boost').value;
document.querySelector('#betav').textContent=beta.toFixed(2);document.querySelector('#lv').textContent=L.toFixed(3)+' m';document.querySelector('#uv').textContent=u.toFixed(2);const g=1/Math.sqrt(1-beta*beta),v=beta*c,E=8*pi*e*e*g**4*v**3/(3*eps*c**3*L);
document.querySelector('#energy').textContent=fmt(E)+' J';document.querySelector('#power').textContent=fmt(E*v/L)+' W';document.querySelector('#voltage').textContent=fmt(E/e)+' V';document.querySelector('#efield').textContent=fmt(E/(e*L))+' V/m';
const speed=.6*c,R=.01,gboost=1/Math.sqrt(1-u*u),w=speed/(R*gboost),vp2=speed*speed/(gboost*gboost)+u*u*c*c;
document.querySelector('#kappa').textContent=(R*w*w/vp2).toFixed(4)+' m⁻¹';document.querySelector('#torsion').textContent=(-u*c*w/vp2).toFixed(4)+' m⁻¹';
let s=[];for(let i=0;i<=320;i++){const t=i/320*5*pi;const x=300+135*Math.cos(t)+u*t*5, y=100+65*Math.sin(t);s.push((i?'L':'M')+x.toFixed(2)+' '+y.toFixed(2))}document.querySelector('#path').setAttribute('d',s.join(' '));}
['beta','length','boost'].forEach(id=>document.querySelector('#'+id).addEventListener('input',render));render();
</script></body></html>'''
(root/'web/index.html').write_text(html,encoding='utf-8')
print('Research document + 369 ledger + interactive dashboard ready')
