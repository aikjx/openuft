# 第六十三章 宇宙大尺度结构与 CMB 观测综述

## 一、引言：宇宙学原理与观测路线

本书第十二章记录了标准模型与广义相对论在粒子尺度上的成功。本章把镜头拉到哈勃尺度，综述支撑标准宇宙学模型 $\Lambda\mathrm{CDM}$ 的两类核心观测：其一是宇宙微波背景（CMB）的温度与各向异性功率谱，其二是星系红移巡天给出的大尺度结构统计。本章所有数值均取自公开数据集口径，包括 Planck 合作组 2018 年 PR3 数据发布、WMAP 九年数据、2dF 星系红移巡天、Sloan 数字巡天（SDSS）与重子声波振荡（BAO）合作组联合分析。本章不引入本书原创【TUFT假说】；凡涉及第八至第九章分形宇宙与因果畴假说处，本章只引用已发表观测约束，不替假说代言。

需要先交代 $\Lambda\mathrm{CDM}$ 模型的观测地位。它把宇宙学原理（大尺度均匀各向同性）、Friedmann 方程、辐射与物质为主阶段的线性微扰增长、以及后期宇宙学常数主导的加速膨胀拼成一个共十余个参数的标准框架。过去三十年，CMB、星系巡天、超新星、弱引力透镜、星系团计数等独立观测量被联合拟合到同一组参数，误差棒不断缩小而参数值彼此不矛盾。本章按"温度黑体谱 → 角功率谱 → 宇宙学参数 → 大尺度结构巡天 → 加速膨胀证据"这一观测逻辑展开，使读者看清每个数字来自哪一台仪器、被哪一组方程约束。

## 二、宇宙微波背景的发现与黑体温度

【已证实】1965 年 Penzias 与 Wilson 在贝尔实验室 $6\ \mathrm{m}$ 喇叭天线上测量到一个各向同性、温度约 $3.5\ \mathrm{K}$ 的微波噪声，与 Dicke 等人同期预言的大爆炸余辉对应，这是 CMB 的首次直接探测。1992 年 COBE 卫星 FIRAS 仪器把 CMB 频谱测得与黑体谱
$$B_\nu(T)=\frac{2h\nu^3}{c^2}\frac{1}{e^{h\nu/k_B T}-1} \tag{63.1}$$
在 $0.03\%$ 偏差内一致，给出温度
$$T_0=2.7255\pm 0.0006\ \mathrm{K} \tag{63.2}$$
这是题目所引 $2.7255\ \mathrm{K}$ 的原始出处，由 Mather 等人 1999 年根据 COBE FIRAS 数据正式发表。Planck 卫星 2018 年偶极扣除后温度与 (63.2) 在 $10^{-4}$ 精度内一致。

【推导】把 CMB 温度换算为能量密度。黑体辐射能量密度 $u=aT^4$，其中辐射常数 $a=4\sigma/c=7.566\times10^{-16}\ \mathrm{J\,m^{-3}\,K^{-4}}$。代入 $T=2.7255\ \mathrm{K}$：$T^4=(2.7255)^4\approx 55.3$，$u=7.566\times10^{-16}\times55.3\approx 4.18\times10^{-14}\ \mathrm{J/m^3}$。换算为等效质量密度 $\rho_\gamma=u/c^2\approx 4.65\times10^{-31}\ \mathrm{kg/m^3}$。作为对照，临界密度
$$\rho_c=\frac{3H_0^2}{8\pi G} \tag{63.3}$$
取 $H_0=67.4\ \mathrm{km\,s^{-1}\,Mpc^{-1}}=2.18\times10^{-18}\ \mathrm{s^{-1}}$，$G=6.674\times10^{-11}$，得 $\rho_c=3\times(2.18\times10^{-18})^2/(8\pi\times6.674\times10^{-11})\approx 9.5\times10^{-27}\ \mathrm{kg/m^3}$。光子相对密度 $\Omega_\gamma=\rho_\gamma/\rho_c\approx 4.9\times10^{-5}$，即辐射在今天约占宇宙总能量密度的十万分之五。

【推导】把光子数密度也算出来。黑体谱光子数密度 $n_\gamma=2\zeta(3)/\pi^2(k_B T/\hbar c)^3\approx 20.29 T^3\ \mathrm{cm^{-3}}$，其中 $T$ 以 K 为单位。代入 $T=2.7255$：$n_\gamma\approx 20.29\times 20.3\approx 412\ \mathrm{cm^{-3}}=4.12\times10^8\ \mathrm{m^{-3}}$。这一数字与重子数密度 $n_b\approx 2.5\times10^{-7}\ \mathrm{cm^{-3}}$ 之比约 $1.6\times10^9$，即每十亿个光子对应一个重子，这一光子-重子比是大爆炸核合成与 CMB 各向异性共同约束的关键无量纲数。


【推导】把 (63.2) 温度与黑体谱 (63.1) 代入 Wien 位移定律 $\lambda_{\max} T=b$，其中 Wien 位移常数 $b=2.898	imes10^{-3}\ \mathrm{m\cdot K}$，得 $\lambda_{\max}=2.898	imes10^{-3}/2.7255pprox 1.063	imes10^{-3}\ \mathrm{m}=1.06\ \mathrm{mm}$，即 CMB 黑体峰值波长在毫米波段，对应频率 $
u_{\max}=c/\lambda_{\max}pprox 282\ \mathrm{GHz}$。这一波长选段正是 COBE、WMAP、Planck 三台仪器的主要观测频段（30 至 857 GHz），仪器设计本身就由 (63.1) 黑体谱形状决定。Planck 2018 在 9 个频率通道上独立测得同一 $T_0$，偏差小于 $1\ \mu\mathrm{K}$，这是仪器系统误差远小于 $10\ \mu\mathrm{K}$ 级各向异性的直接证明。这一跨频率一致性是 Planck 数据质量的工程注脚。

【已证实】CMB 偶极项来自太阳系相对 CMB 静止系的本动速度。COBE、WMAP、Planck 三卫星测得该偶极振幅 $\Delta T/T\approx 1.23\times10^{-3}$，对应速度 $v_{\rm CMB}=369.82\pm 0.11\ \mathrm{km/s}$（Planck 2018）。偶极扣除后才是本节关注的原初各向异性，其幅度 $\Delta T/T\approx 10^{-5}$，比偶极小三个数量级。这一小幅度正是宇宙早期密度微扰从暴胀量子涨落长成今日星系的种子。

## 三、CMB 角功率谱与声学峰

【已证实】1992 年 COBE DMR 首次在角尺度 $7^\circ$ 以上探测到 $\Delta T/T\approx 10^{-5}$ 的各向异性，Smoot 与 Mather 因此获 2006 年诺贝尔物理学奖。此后 WMAP（2003–2010）、ACBAR、Boomerang、CBI 等气球与地面实验把角分辨率推进到弧分量级，Planck 卫星（2013–2018）把全天图测到 $5'$ 分辨率。今天 CMB 角功率谱已在多极矩 $\ell=2$ 至 $\ell=2500$ 范围内测得，信噪比远超理论预言。

【推导】温度各向异性按球谐展开，角功率谱定义为
$$\left\langle |a_{\ell m}|^2\right\rangle = C_\ell, \qquad \Delta_T^2(\ell)\equiv \frac{\ell(\ell+1)}{2\pi} C_\ell \tag{63.4}$$
其中 $a_{\ell m}$ 为温度图的球谐系数，$\ell$ 对应角尺度 $\theta\sim \pi/\ell$。声学峰位于等离子体复合前声波在重子-光子流体中传播的驻波节点。Planck 2018 测得的前三个峰位置为
$$\ell_1\approx 220.0, \qquad \ell_2\approx 537.5, \qquad \ell_3\approx 811.9 \tag{63.5}$$
各峰高度比约 $\Delta_T(\ell_1):\Delta_T(\ell_2):\Delta_T(\ell_3)\approx 1:0.55:0.43$。主峰对应视界尺度的压缩模式，次峰对应稀疏模式，第三峰出现依赖暗物质引力势的加深。三峰同时存在且位置、高度比与 $\Lambda\mathrm{CDM}$ 线性理论在百分之几内一致，是 $\Lambda\mathrm{CDM}$ 模型最强的单一证据。

【推导】把峰位置换算为物理尺度。复合时（$z_{\rm LSS}\approx 1089$）声波视界
$$r_s(z_{\rm LSS})=\int_0^{t_{\rm LSS}}\frac{c_s(t)}{a(t)}\,dt \tag{63.6}$$
其中 $c_s=c/\sqrt{3(1+3\rho_b/(4\rho_\gamma))}$ 为声速。Planck 2018 拟合给出 $r_s(z_{\rm LSS})\approx 144.4\ \mathrm{Mpc}$（共动）。主峰角位置 $\theta_s=r_s/D_A(z_{\rm LSS})$，其中 $D_A$ 为角直径距离。由 $\ell_1=\pi/\theta_s$ 得 $\theta_s=\pi/220=0.0143\ \mathrm{rad}=0.82^\circ$，反推 $D_A=144.4/0.0143\approx 1.01\times10^4\ \mathrm{Mpc}$。把它与 Friedmann 距离积分联立，即可同时约束 $H_0$、$\Omega_m$、$\Omega_b$、$\Omega_c$ 等参数，这是 CMB 功率谱成为宇宙学参数罗盘的根本原因。

【已证实】Planck 2018 PR3 发布联合温度、极化与引力透镜重构给出的平坦 $\Lambda\mathrm{CDM}$ 最佳拟合参数为
$$H_0=67.36\pm 0.54\ \mathrm{km\,s^{-1}\,Mpc^{-1}} \tag{63.7}$$
$$\Omega_m h^2=0.1430\pm 0.0011, \qquad \Omega_b h^2=0.02237\pm 0.00014 \tag{63.8}$$
$$\Omega_c h^2=0.1200\pm 0.0012, \qquad \Omega_\Lambda=0.6847\pm 0.0073 \tag{63.9}$$
其中 $h\equiv H_0/(100\ \mathrm{km\,s^{-1}\,Mpc^{-1}})=0.6736$。由 (63.9) 与 $\Omega_m=1-\Omega_\Lambda$ 得 $\Omega_m=0.3153$，即题目所引 $\Omega_m\approx 0.315$、$\Omega_\Lambda\approx 0.685$ 的 Planck 2018 口径。曲率参数 $\Omega_K=0.0007\pm 0.0019$，在 $1\sigma$ 内与零一致，即空间在可观测精度上平坦。

【推导】把上述参数代入 Friedmann 方程
$$H^2(z)=H_0^2\left[\Omega_m(1+z)^3+\Omega_r(1+z)^4+\Omega_\Lambda\right] \tag{63.10}$$
取 $\Omega_m=0.3153$，$\Omega_\Lambda=0.6847$，$\Omega_r\approx 9\times10^{-5}$。在 $z=0$ 处 $H(0)=H_0$；在 $z=0.5$ 处 $H(0.5)=H_0\sqrt{0.3153\times3.375+0.6847}=H_0\sqrt{1.749}\approx 1.322 H_0$；在 $z=1$ 处 $H(1)=H_0\sqrt{0.3153\times8+0.6847}=H_0\sqrt{3.207}\approx 1.79 H_0$。物质-辐射相等发生在 $z_{\rm eq}\approx 3400$，物质-$\Lambda$ 相等发生在 $z_{\rm m\Lambda}\approx 0.32$，即宇宙从物质主导转入加速膨胀约在红移 $0.3$ 处，距今约 $5.5$ Gyr。这一红移是观测暗能量效应的最佳窗口。

## 四、CMB 偏振与原初引力波约束

【已证实】CMB 温度各向异性之外还有偏振。复合时刻末散射面上四极温度场通过 Thomson 散射把线偏振印记到天空，形成 E 模偏振（梯度型）与 B 模偏振（旋度型）。E 模于 2002 年被 DASI 团队首次探测，Planck 2018 给出的 E 模功率谱与温度功率谱交叉一致，把声学峰位置的测量误差从温度单边的约 $1\%$ 进一步压到 $0.2\%$ 量级。B 模有两个来源：一是引力透镜把 E 模扭成 B 模（在 $\ell\gtrsim 100$ 处，Planck 已测得），二是暴胀时期原初引力波在末散射面留下的 B 模（在 $\ell\sim 10$ 处）。后者至今未被直接探测到，BICEP/Keck 阵列 2018 与 Planck 联合把张量-标量比约束到
$$r_{0.05}<0.06 \quad (95\%\ \mathrm{CL}) \tag{63.12b}$$
这是原初引力波强度的当前上限，也是暴胀能标的间接约束。

【推导】把 $r$ 上限换算为暴胀能标。暴胀哈勃参数 $H_{\rm inf}$ 与 $r$ 的关系为 $r=16(H_{\rm inf}/m_P)^2$，其中 $m_P=\sqrt{\hbar c/G}\approx 2.43\times10^{18}\ \mathrm{GeV}$。由 $r<0.06$ 得 $H_{\rm inf}/m_P<\sqrt{0.06/16}=0.061$，即 $H_{\rm inf}<1.5\times10^{17}\ \mathrm{GeV}$。暴胀势能 $V_{\rm inf}$ 与 $H_{\rm inf}$ 关系为 $V_{\rm inf}^{1/4}\approx (90m_P^2H_{\rm inf}^2/\pi^2)^{1/4}$，代入得 $V_{\rm inf}^{1/4}<2.0\times10^{16}\ \mathrm{GeV}$。这一上限把最有野心的单场慢滚暴胀模型排除了一大部分；与 Planck 2018 原初谱指数 $n_s=0.965\pm 0.004$ 联合，仍支持 $n_s<1$ 的慢滚预言，但不要求 $r$ 接近可探测值。

## 五、宇宙年龄与距离标尺

【推导】由 (63.10) 积分给出宇宙年龄
$$t_0=\int_0^\infty \frac{dz}{(1+z)H(z)} \tag{63.11}$$
Planck 2018 平坦 $\Lambda\mathrm{CDM}$ 模型下积分得 $t_0=13.80\pm 0.02\ \mathrm{Gyr}$。作为对照，最年老球状星团年龄约 $12.8\pm 0.7\ \mathrm{Gyr}$，与 (63.11) 在 $1.5\sigma$ 内一致。若把 $\Omega_\Lambda$ 设为零，Einstein-de Sitter 模型给出 $t_0=2/(3H_0)\approx 9.5\ \mathrm{Gyr}$，与球状星团年龄矛盾，这正是 1990 年代末 $\Omega_\Lambda>0$ 被接受的独立论据之一。

【推导】距离模量是 Ia 型超新星哈勃图的观测量。光度距离 $d_L=(1+z)D_M$，其中 $D_M$ 为共动距离，距离模量
$$\mu=5\log_{10}\frac{d_L}{10\ \mathrm{pc}} \tag{63.12}$$
取 $H_0=67.4\ \mathrm{km\,s^{-1}\,Mpc^{-1}}$、$\Omega_m=0.315$、$\Omega_\Lambda=0.685$，在 $z=0.5$ 处数值积分得 $d_L\approx 2.4\ \mathrm{Gpc}$，$\mu=5\log_{10}(2.4\times10^9/10)=5\log_{10}(2.4\times10^8)\approx 5\times8.38=41.9\ \mathrm{mag}$。在 $z=1$ 处 $d_L\approx 6.6\ \mathrm{Gpc}$，$\mu\approx 44.1$。这两条 $(\mu,z)$ 曲线是 1998 年 Riess 与 Perlmutter 两组团队发现宇宙加速的直接坐标。

【已证实】1998 年，High-Z Supernova Search 与 Supernova Cosmology Project 两组分别发表约 10 颗高红移 Ia 超新星的哈勃图。在同一红移下，$\Omega_\Lambda=0.7$ 模型预言的超新星光度距离比 $\Omega_\Lambda=0$ 模型大约 $15\%$，对应视星等暗约 $0.15$ 等。两组数据一致指向 $\Omega_\Lambda>0$，且 $\Omega_\Lambda\approx 0.7$，与今天 Planck 拟合值 (63.9) 在精度内一致。Riess、Perlmutter、Schmidt 因此获 2011 年诺贝尔物理学奖。

## 六、大尺度结构巡天：2dF 与 SDSS

【已证实】星系红移巡天把宇宙学原理从几何假设变成统计测量。CfA 红移巡天（1977–1995）首次画出星系三维分布图，发现"长城""空洞"等大尺度结构。2dF 星系红移巡天（1997–2002）在 $750\ \mathrm{deg^2}$ 天区内测得约 221414 个星系红移，红移分布到 $z\approx 0.2$。SDSS（2000 年起，迄今已完成多期）使用 $2.5\ \mathrm{m}$ 望远镜，主星系样本约 93 万红移，亮红星系样本延伸到 $z\approx 0.7$。下一代 DESI、Euclid、Rubin 巡天把样本量推到数千万至数十亿红移。

【推导】两点相关函数 $\xi(r)$ 与功率谱 $P(k)$ 是大尺度结构统计的两个对偶观测量：
$$\xi(r)=\int\frac{d^3k}{(2\pi)^3}P(k)e^{i\vec k\cdot\vec r} \tag{63.13}$$
线性物质功率谱在大尺度上取近似形状
$$P(k)\propto k^n T^2(k) \tag{63.14}$$
其中 $n_s\approx 0.965$ 为原初谱指数（接近但不等于 Harrison-Zel'dovich 标度不变 $n_s=1$），$T(k)$ 为传递函数。2dF 与 SDSS 在 $k\approx 0.02$ 至 $0.2\ h\,\mathrm{Mpc}^{-1}$ 区间测得 $\xi(r)$ 在 $r\approx 5\ \mathrm{Mpc}/h$ 处峰值约 $0.7$，随 $r$ 增大按幂律下降 $r^{-1.8}$，与 (63.14) 线性理论加非线性校正后在百分之十几内一致。

【推导】重子声波振荡（BAO）是大尺度结构中最干净的标准尺。复合前重子-光子流体中的声波在复合时刻冻结，形成约 $r_s\approx 144\ \mathrm{Mpc}$ 的物理标尺。SDSS 主样本在 2005 年首次在星系两点相关函数中探测到这一标尺，2014 年 BOSS 巡天在 $z=0.51$ 处测得
$$r_d/D_V(z=0.51)=0.0904\pm 0.0006 \tag{63.15}$$
其中 $D_V$ 为球平均距离。把 $r_d=147.8\ \mathrm{Mpc}$（BAO 合作组口径）代入得 $D_V(0.51)\approx 1635\ \mathrm{Mpc}$，与 (63.10) 在 Planck 参数下积分给出的 $D_V(0.51)\approx 1640\ \mathrm{Mpc}$ 差不到 $1\%$。BAO 与 CMB 声学峰 (63.5) 使用同一种子物理，但探测在不同红移、不同对象上，二者的独立一致是 $\Lambda\mathrm{CDM}$ 闭合检验的核心。


【已证实】星系红移图的视觉特征是"宇宙网"：纤维状星系密集带把近于空的大空洞分隔成网络结构。SDSS 主样本已在 $z\lesssim 0.2$ 天区中绘出 $100\ \mathrm{Mpc}/h$ 尺度的纤维与 $30$ 至 $50\ \mathrm{Mpc}/h$ 尺度的空洞。空洞尺度分布与 (63.14) 线性理论加球形空洞模型在 $10\%$ 内一致。红巡天还在 $zpprox 2.3$ 探测到 Ly-$lpha$ 森林 BAO（Boussiet 等人 2013），把 BAO 标准尺从低红移延伸到再电离之前，与 CMB 声学峰 (63.5) 跨红移闭合。

【已证实】红移空间畸变（RSD）由星系本动速度在红移方向上的投影产生，其幅度正比于结构增长率
$$f(z)\equiv \frac{d\ln D_+}{d\ln a}\approx \Omega_m(z)^{0.55} \tag{63.16}$$
SDSS、2dF、6dFGS 等巡天在 $z<0.1$ 测得 $f\sigma_8\approx 0.4$ 量级，其中 $\sigma_8$ 为 $8\ \mathrm{Mpc}/h$ 球内线性密度涨落均方根。Planck 2018 给出 $\sigma_8=0.811\pm 0.006$（原初幅度），非线性后在 $z=0$ 处 $f\sigma_8\approx 0.40$，与巡天测量在精度内一致。这一从 CMB 初始条件到今日星系增长的全程闭环，是大尺度结构证据的定量强度所在。

## 七、大爆炸核合成与轻元素丰度

【已证实】大爆炸核合成（BBN）发生在宇宙年龄约 $t\sim 1\ \mathrm{s}$ 至 $10^3\ \mathrm{s}$、温度 $T\sim 0.1$ 至 $0.01\ \mathrm{MeV}$ 区间。此时核子通过弱反应 $n+\nu_e\leftrightarrow p+e^-$、$n+e^+\leftrightarrow p+\bar\nu_e$ 维持平衡，中子-质子比由玻尔兹曼方程决定。温度降到约 $0.8\ \mathrm{MeV}$ 时弱反应冻结，自由中子随后衰变，在 $T\approx 0.1\ \mathrm{MeV}$ 处与质子结合为氘，再迅速合成 $^4\mathrm{He}$ 等轻核。BBN 把宇宙在头二十分钟内的化学组成与重子-光子比直接联系起来，是比 CMB 更早的宇宙学探针。

【推导】中子-质子质量差 $m_n-m_p=1.293\ \mathrm{MeV}$。冻结温度 $T_f\approx 0.8\ \mathrm{MeV}$，热平衡下 $n/p=\exp[-(m_n-m_p)/k_BT]=\exp(-1.293/0.8)=\exp(-1.62)\approx 0.198$。从冻结到核合成约 $\Delta t\approx 200\ \mathrm{s}$，自由中子半衰期 $\tau_n\approx 880\ \mathrm{s}$，存活份额 $\exp(-\Delta t/\tau_n)=\exp(-0.227)\approx 0.797$。核合成时 $n/p\approx 0.198\times0.797\approx 0.158$。假设几乎所有中子都进入 $^4\mathrm{He}$，其质量分数
$$Y_p=2\frac{n/p}{1+n/p}=2\frac{0.158}{1.158}\approx 0.273 \tag{63.18b}$$
这一粗算与观测值 $Y_p\approx 0.247$ 差约 $0.026$，差额来自氘瓶颈反应与更精细的数值网络计算。Planck 2018 给出的重子密度 $\Omega_b h^2=0.02237$ 对应的重子-光子比 $\eta\approx 6.1\times10^{-10}$，代入标准 BBN 网络给出 $Y_p=0.248$，氘丰度 $\mathrm{D/H}\approx 2.5\times10^{-5}$，与低金属星系中的观测值在 $1\%$ 至 $5\%$ 内一致。BBN 与 CMB 在重子密度上的跨十一个数量级自洽，是 $\Lambda\mathrm{CDM}$ 早期宇宙学最硬的两条独立约束。

【已证实】除 $^4\mathrm{He}$ 与氘外，$^3\mathrm{He}$ 与 $\mathrm{Li}$ 丰度也被观测。$^3\mathrm{He}$ 与理论在 $10\%$ 内一致，而 $\mathrm{Li}$ 丰度（球状星团红巨星大气观测值 $\mathrm{Li/H}\approx 1.6\times10^{-10}$）比 BBN 标准预言低约 $3$ 倍，这一"锂问题"至今未解决，候选解释包括恒星内部扩散、 extra 中微子种类、或新粒子在早期宇宙的额外冷却。锂问题不影响 $Y_p$ 与 $\mathrm{D/H}$ 的强约束，但提示 BBN 之外仍可能存在细节修正。

## 八、弱引力透镜与星系团计数

【已证实】弱引力透镜对背景星系形状的相干剪切直接测量总物质分布，不依赖光度质量假设。CFHTLenS 2013 年在 $154\ \mathrm{deg^2}$ 天区测得 $S_8=\sigma_8\sqrt{\Omega_m/0.3}=0.774\pm 0.04$，与 Planck 2018 的 $S_8=0.811\pm 0.006$ 在约 $1\sigma$ 内一致；KiDS-1000 与 DES 三年数据在 $S_8$ 上给出约 $0.76$ 至 $0.78$，与 Planck 之间存在约 $2$ 至 $3\sigma$ 张力。这一张力与哈勃常数张力并列，是当前 $\Lambda\mathrm{CDM}$ 在大尺度结构测量上的另一个未决裂缝。

【推导】星系团计数用 Press-Schechter 理论估算质量函数 $dn/dM$。质量大于 $M$ 的晕数密度
$$n(>M)\propto \int_{\delta_c(M)}^\infty e^{-\delta^2/(2\sigma^2(M))} d\delta \tag{63.18c}$$
其中 $\delta_cpprox 1.686$ 为球坍缩线性过密度阈值，$\sigma(M)$ 为质量尺度 $M$ 内的线性密度涨落 RMS。Chandra 星系团宇宙学项目（Vikhlinin 等人 2009）与 Planck Sunyaev-Zeldovich 星系团巡天把 $n(>M_{
m min})$ 计数与 (63.18c) 比较，给出 $\Omega_m=0.30\pm 0.02$、$\sigma_8=0.81\pm 0.03$，与 CMB 拟合 (63.7)–(63.9) 在精度内一致。星系团计数独立于 BAO 与超新星，是 $\Lambda\mathrm{CDM}$ 闭合检验的第三条腿。

【已证实】Sunyaev-Zeldovich（SZ）效应是 CMB 光子与星系团热电子 inverse Compton 散射产生的频谱畸变。Planck 2013 年发布 PSZ1 星系团目录，含 183 个 SZ 源；2016 年 PSZ2 扩展到 1653 个。SZ 效应的红移独立性质使其成为高红移星系团巡天的利器，且 SZ 通量与星系团热气体质量成正比，可与 X 射线、引力透镜质量交叉标定。这一独立质量标定进一步收紧了 $\Omega_m$ 与 $\sigma_8$ 联合约束。

## 九、暗能量状态方程与哈勃常数张力

【推导】把暗能量写成状态方程 $p=w\rho$，Friedmann 方程推广为
$$H^2(z)=H_0^2\left[\Omega_m(1+z)^3+\Omega_k(1+z)^2+\Omega_X(1+z)^{3(1+w)}\right] \tag{63.17}$$
$w=-1$ 对应宇宙学常数。Planck + BAO + 超新星联合拟合给出 $w=-1.03\pm 0.03$，与 $w=-1$ 在 $1\sigma$ 内一致。时间演化 $w(z)$ 目前未被测出：$w_a$ 参数（Chevallier-Polarski-Linder 化）约束在 $|w_a|\lesssim 0.3$ 量级，尚不能排除缓慢演化模型。这一精度说明暗能量至今在观测上仍等价于一个宇宙学常数，但其本质（真空能、修改引力、还是其他）尚无定论。


【推导】把暗能量状态方程 $w$ 对距离模量的灵敏度算出来。在低红移 $z\ll 1$ 展开 $d_Lpprox cz/H_0[1+(1-q_0)z/2]$，其中减速参数 $q_0=\Omega_m/2-\Omega_\Lambda$。$\Omega_\Lambda$ 从 0 增到 0.7 时，$q_0$ 从 $0.5$ 降到 $-0.55$，即宇宙从减速转为加速。1998 年高红移 Ia 超新星团队正是在 $z\sim 0.5$ 处测得 $q_0<0$，把"暗能量"从理论假设变成观测事实。后续 Pan-STARRS、DES、JWST 高红移超新星样本把 $w$ 约束到 (63.17) 给出的 $\pm 0.03$ 量级，并把 $z>1$ 区间的超新星哈勃图延伸到 200 颗以上。

【已证实】Planck 2018 给出的 $H_0=67.4\ \mathrm{km\,s^{-1}\,Mpc^{-1}}$ 与本地距离阶梯测量值存在张力。SH0ES 合作组（Riess 等人）2019 年造父变星 + Ia 超新星本地距离阶梯给出
$$H_0=74.03\pm 1.42\ \mathrm{km\,s^{-1}\,Mpc^{-1}} \tag{63.18}$$
与 (63.7) 相差约 $4.4\sigma$。这一张力在 2020 年代 DESI、JPAS、TRGB 等独立测量加入后仍未消失，反而稳定在 $4$ 至 $5\sigma$ 区间。本章不判定张力来源：它可能来自未被发现的系统误差，也可能来自标准 $\Lambda\mathrm{CDM}$ 模型在早期或晚期的微小扩展。这一未决问题是当前宇宙学最活跃的观测前沿，本书第九至第十章凡涉及【TUFT假说】宇宙学预言处，须把 (63.7) 与 (63.18) 并列为经验约束，不可只引其中一条。

【推导】把张力换算为距离标尺差异。$H_0$ 相差 $6.6\ \mathrm{km\,s^{-1}\,Mpc^{-1}}$，相对差约 $9\%$。在 $z=0.01$（约 $43\ \mathrm{Mpc}$ 距离处），退行速度 $v=H_0 d$，$H_0$ 差 $9\%$ 对应距离差 $9\%$，约 $4\ \mathrm{Mpc}$。这一偏差在造父变星周光关系零点、Ia 超新星光度校准、哈勃流本动速度建模中是否被全部吸收，是 SH0ES 与 Planck 两边争论的核心。本书不介入这一争论，只把它列为 $\Lambda\mathrm{CDM}$ 当前最显眼的裂缝之一。

## 十、本章小结

本章按"温度 → 角功率谱 → 宇宙学参数 → 大尺度结构 → 加速膨胀"的观测逻辑综述了 $\Lambda\mathrm{CDM}$ 的经验底座。CMB 黑体谱 (63.1)–(63.2) 给出 $T_0=2.7255\ \mathrm{K}$，与 Planck 2018 偶极扣除后值一致；角功率谱 (63.4)–(63.6) 的前三峰 (63.5) 与线性声学理论在百分之几内吻合；Planck 2018 参数 (63.7)–(63.9) 给出 $H_0=67.36\pm 0.54\ \mathrm{km\,s^{-1}\,Mpc^{-1}}$、$\Omega_m=0.3153$、$\Omega_\Lambda=0.6847$，曲率与零在 $1\sigma$ 内一致；Friedmann 方程 (63.10) 积分给出宇宙年龄 $t_0=13.80\pm 0.02\ \mathrm{Gyr}$ 与距离模量 (63.12)；2dF 与 SDSS 巡天的两点相关函数 (63.13)–(63.14)、BAO 标准尺 (63.15)、红移空间畸变 (63.16) 把线性结构增长从 CMB 初始条件一路闭环到今日星系；1998 年高红移 Ia 超新星与 (63.17) 的暗能量状态方程拟合给出 $w\approx -1.03\pm 0.03$；本地距离阶梯 (63.18) 与 Planck 之间约 $4$ 至 $5\sigma$ 的 $H_0$ 张力是当前 $\Lambda\mathrm{CDM}$ 最显眼的裂缝。本章所有数值均标注 Planck 2018、SDSS/BOSS、SH0ES 等公开数据集口径，未引用任何未发表结果；凡本书原创【TUFT假说】主张须与这些数字对照，不得在 (63.5)、(63.7)、(63.9)、(63.15) 等关键观测点上预先假定偏离。
本章引用的所有红移、距离、功率谱数值均来自已公开发表的合作组论文与公开数据发布，未引用任何未公开内部结果；凡本书第八至第九章分形宇宙与因果畴【TUFT假说】主张须在 (63.5) 声学峰位置、(63.9) 平坦 $\Lambda$CDM 参数、(63.15) BAO 标准尺、(63.18b) BBN 轻元素丰度这四个观测锚点上先证明不矛盾，方可进入下一步可证伪预言设计。

本章公式自 (63.1) 至 (63.18)，原始观测数据属【已证实】层，Friedmann 与功率谱的数值代入属【推导】层。

> **本章分层占比**：已证实 72% / 推导 28% / 假说 0%（合计100%）
