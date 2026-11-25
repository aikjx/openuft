# ROOT V155 — 光速螺旋发散、平行平衡、垂直原理数值审计

## 运行
Python 3.10+，安装 numpy scipy matplotlib 后运行 `python run_all.py`。输出 data/*.csv、summary.json 和 figures/*.png。所有随机点固定种子155。运行时会执行断言；任何断言失败将中止。仅在当前 Linux 环境实测，Windows 脚本未在 Windows 上实测。建议 numpy>=2.0（使用 trapezoid）。

## 单位与范围
理论 c=1，hbar 与 G 保持独立；[hbar]=ML，[G]=L/M，[rho]=M/L^3，[f]=M/L^4。流体例使用 L0 和密度参考尺度归一化，C 是归一化通量系数，不是自然常数。地月表格输出 SI，轨道用 r0、sqrt(r0^3/GM) 归一化，是弱场牛顿近似，不是相对论轨道或实际卫星星历拟合。未运行物理实验、真实卫星观测联合反演、完整三维自洽流体/Einstein/Yang-Mills求解。

## 推导
在 Minkowski 时空中 k=(1,n), |n|=1，T^{mu nu}=rho k^mu k^nu。对流体子系统，外部对其作用为 div T；若总能动量守恒，外部受反作用 f=-div T。若 div(rho k)=0，则 f=-rho(k·partial)k。无外部作用且 rho>0 时 (k·partial)k=0，光速流线必须是直线（在曲时空中为零测地线，采用协变导数）。在稳态，单位矢量恒等式 (n·grad)n=-n×curl n，于是 f=rho n×curl n。这里 f 是单位体积的交换力，而非对任意试验物体的力；未指定耦合、反作用源的方程或材料边界。

选择 n=(er+b ez×er)/w, w=sqrt(1+b² sin²θ), rho=C w/r²。无奇点区域 r>0。J=C(er+b ez×er)/r²，div J=0（径向部分为反平方，旋转部分为无散度）。径向通量为 4πC。沿流线 θ不变，dr/dt=1/w，dφ/dt=b/(wr)，所以 φ=φ0+b log(r/r0)。这是锥面上的对数螺旋，不是恒半径螺旋；其速度为1，非零加速度需要外部作用。赤道上 n=(er+b eφ)/sqrt(1+b²)，由球坐标基的导数得到 a=(-b² er+b eφ)/(r(1+b²))，因此 f=C(b² er-b eφ)/(r³ sqrt(1+b²))。全空间径向投影 f·er=C b² sin²θ/(r³ w)≥0（C≥0），沿轴为0，反转 b 不改变径向符号。在本模型中反作用不提供所需的向心引力；不是针对所有螺旋场模型的普适排除。球面整体矢量积分为零并不意味着每点力为零。力密度尺度 r^-3 不能未经耦合模型直接作为试验质量加速度。向外辐射被吸收时动量向外传递；真实太阳辐照度 1361 W/m² 的法向完全吸收压力为 1361/c_SI Pa，不涉及额外引力。

## 数值方案
1. 4096 随机三维点，6种旋转参数，4种中心差分步长；独立解析力与应力散度交叉校验；球面积分使用48×96角度求积。
2. DOP853 数值积分5条三维轨迹，对比解析对数螺旋，并绘制无外力自由光线对照。
3. 球对称径向能量脉冲 q=4πr²rho，满足 q_t+q_r=0。有限体积迎风与 minmod 重构+SSPRK2；200/400/800/1600单元，零左边界流入，记录右边界流出。初始高斯中心2，演化3个时间单位，解析平移中心5；高斯尾部在边界可忽略。误差为相对离散L1误差，不是实验测量误差。
4. 两个自由高斯能量包各能量1，速度±1，初始方差1。积分能量、动量、方差；方差1+t²，证明自由平衡流不自动束缚。两束均匀对向流的T00=2、T01=0、T11=2；不是各向同性压强。
5. JPL DE440 地月 GM、NASA平均半径等标准输入。地球400km圆轨道基准，同初速度分别施加向内、零、向外加速度。向外模型是人为取相同反平方幅值的方向对照，并非由前述 r^-3 力密度推出。轨道结果非独立预测G或质量。

## 结果判定
108/108 断言通过（详见 data/summary.json），4张图。最高分辨率TVD波形L1误差约1.21%，能量平衡误差2.51e-16；不可把守恒精度当波形精度或物理预测精度。结论：指定的光速发散模型能满足通量守恒，但螺旋流要求外部力，反作用径向向外；净动量为零不等于束缚。下一步必须提供独立、协变、闭合的场和物质耦合作用量，并检验静态吸引、等效原理、稳定性、规范群和量子一致性。四力统一仍未证明。

## 参考资料（公开资料，非原始观测拟合）
- JPL Astrodynamic Parameters: https://ssd.jpl.nasa.gov/astro_par.html
- Park et al. DE440/DE441: https://doi.org/10.3847/1538-3881/abd414
- NASA Earth Fact Sheet: https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html
- NASA Solar Irradiance Science: https://earth.gsfc.nasa.gov/climate/projects/solar-irradiance/science
- Null dust stress and null geodesics: https://pmc.ncbi.nlm.nih.gov/articles/PMC7976656/
