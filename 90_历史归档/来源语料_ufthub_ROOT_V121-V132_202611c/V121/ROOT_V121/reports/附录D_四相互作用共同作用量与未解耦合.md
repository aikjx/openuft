# 附录 D｜从共同协变作用量出发：四种相互作用怎样“写在一起”，还差什么才叫统一

## D1. 先区分共同框架与真正大统一

在自然单位 \(\hbar=c=1\) 且四维时空中，标准模型的规范群是

\[
G_{\mathrm{SM}}=SU(3)_{c}\times SU(2)_L\times U(1)_Y.
\]

电磁力与弱力已在电弱理论中由 \(SU(2)_L\times U(1)_Y\) 统一描述；强力使用 \(SU(3)_c\)；引力用动态度规描述。把它们放进同一个积分的拉氏量：

\[
S=\int d^4x\sqrt{-g}\Big[
\frac{M_{\rm red}^2}{2}\mathcal R
-\tfrac14G^A_{\mu\nu}G^{A\mu\nu}
-\tfrac14W^a_{\mu\nu}W^{a\mu\nu}
-\tfrac14B_{\mu\nu}B^{\mu\nu}
+\mathcal L_{\rm matter}\Big]+S_{\rm higher}.
\]

这个式子是**现有低能有效理论的共同表述**，不应命名为已完成的全新“大统一定理”。引力耦合由 \(M_{\rm red}\) 输入；三组规范耦合、Yukawa 参数等仍要输入。

### D1.1 场强的严格区别

\[
G^A_{\mu\nu}=\partial_\mu G^A_\nu-\partial_\nu G^A_\mu+g_3 f^{ABC}G^B_\mu G^C_\nu,
\]

\[
W^a_{\mu\nu}=\partial_\mu W^a_\nu-\partial_\nu W^a_\mu+g_2\epsilon^{abc}W^b_\mu W^c_\nu,
\]

\[
B_{\mu\nu}=\partial_\mu B_\nu-\partial_\nu B_\mu.
\]

强力和弱力的非阿贝尔自相互作用项不是简单的磁场 \(\mathbf v\times\mathbf B\) 或三维曲率/挠率自然等同，必须从规范代数与场方程导出。

## D2. 电弱混合带来一个真实的“统一”参考范例

Higgs 双重态获得真空期望值 \(v\) 后，混合定义

\[
A_\mu=\sin\theta_W W^3_\mu+\cos\theta_W B_\mu,\quad
Z_\mu=\cos\theta_W W^3_\mu-\sin\theta_W B_\mu,
\]

\[
\tan\theta_W=g_1/g_2,\qquad e=g_2\sin\theta_W=g_1\cos\theta_W.
\]

带电弱玻色子质量

\[
m_W=\frac{g_2v}{2},\quad m_Z=\frac{v}{2}\sqrt{g_1^2+g_2^2}.
\]

**这是从局域规范对称性与自发对称性破缺导出真实可检验关系的典型路线。** ROOT 若想与之等价或超越，必须给出弱同位旋、超荷、场表示以及同样的玻色子谱和可测耦合。

## D3. 引力为何与三力有天然接点

从同一协变物质作用量定义能动张量

\[
T_{\mu\nu}=-\frac{2}{\sqrt{-g}}\frac{\delta S_{\rm matter}}{\delta g^{\mu\nu}}.
\]

Einstein 方程

\[
G_{\mu\nu}=8\pi G T_{\mu\nu}
\]

（自然单位 \(c=1\)）。电磁场的张量示例（\(-,+,+,+\) 度规）

\[
T^{\rm EM}_{\mu\nu}=F_{\mu\rho}F_\nu{}^\rho-\frac14g_{\mu\nu}F_{\rho\sigma}F^{\rho\sigma}.
\]

QCD、弱规范场、Higgs、费米子和束缚态也经其能动张量成为引力源。可见“强、电、弱作用场的能量会产生引力”在现有 GR 中已有明确表述。**共同引力源不表示三种规范力就是同一力，也不自动产生额外第五力。**

Einstein 张量的 Bianchi 恒等式使 \(\nabla_\mu G^{\mu\nu}=0\)；当场方程和物质运动方程成立，局域协变能动量守恒 \(\nabla_\mu T^{\mu\nu}=0\) 必须成立。

## D4. 强相互作用不是一个常数 α_s 的恒定数字

一圈级 QCD 运行（\(n_f\) 为相关能区的有效轻味数）

\[
\frac{d g_3}{d\ln\mu}=-\frac{11-2n_f/3}{16\pi^2}g_3^3+\cdots.
\]

由此 \(\alpha_s=g_3^2/(4\pi)\) 随重整化能标 \(\mu\) 变化。把某个标度下的 \(\alpha_s\sim0.118\) 直接当成全部尺度的绝对常量是错误的。其变化是量子强相互作用核心可检验性质，任何从“一个通用螺旋频率”推出强力的理论都必须重现这一效应、阈值和非微扰束缚态特征。

## D5. 四力统一的新模型应该提交什么？

**最低数学提交：**

1. 明确的微观基本场及作用量，场之间的耦合全部列出；
2. 由变分而非类比导出引力/电弱/QCD 场方程；
3. 解释左手弱相互作用与右手粒子不等价、反常消除、三代费米子和 Higgs；
4. 在 \(E\ll E_{\rm new}\) 的低能极限收敛到已实测 GR 和标准模型；
5. 给出不同于已有模型且不靠事后重新调参的定量可证伪预言；
6. 同时通过地球重力、GPS/时钟、太阳系/引力波与量子散射/精密谱测试。

**当前科研边界：**这一清单尚未被 ROOT 现有“空间光速螺旋速度、曲率、挠率、角速度”关系满足；这些量即使几何上良定义，也尚未在统一作用量中生成全部规范结构。
