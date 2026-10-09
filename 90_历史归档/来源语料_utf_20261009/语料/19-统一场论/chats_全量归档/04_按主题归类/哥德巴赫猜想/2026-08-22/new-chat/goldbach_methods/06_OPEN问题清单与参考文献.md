# OPEN 问题清单与参考文献

> 全局审计：哥德巴赫猜想的开放问题、关键里程碑与核心参考文献。

---

## 一、OPEN 问题清单

### OPEN-0：循环论证的识别
任何假设 $p+q=2k$ 后进行的代数变形（包括 $(p+q)/2 < k$、$p/2+q/2=k$ 等）均为循环论证。**待证命题不能作为证明的前提。**

### OPEN-1：筛法奇偶性障碍的突破
纯筛法无法区分素数和半素数。能否发展新的筛法技术，或结合非筛法工具，绕过奇偶性障碍，从 "1+2" 推进到 "1+1"？

**当前共识**：需要本质上的新思想，纯筛法路线已走到尽头。

### OPEN-2：二元圆法余区间的控制
能否证明余区间上 $\int_{\mathfrak{m}} |S(\alpha)|^2 d\alpha = o(N/\log^2 N)$？这需要比当前 Weyl 不等式、Vinogradov 中值定理强得多的指数和估计。

**关键困难**：$L^2$ 范数恰好等于主项阶，没有"余量"来挤出误差。

### OPEN-3：二变量稀疏线性方程的新框架
Green-Tao 传递原理要求 $\geq 3$ 个变量和平移不变性。能否发展适用于 $x+y=N$ 的传递原理？

**关键困难**：2 变量时缺乏平均化的自由度。

### OPEN-4：无条件的 $r_2(N) > 0$ 证明
当前所有无条件结果都是"几乎所有"或"充分大 = p+P₂"。能否对充分大偶数证明 $r_2(N) > 0$（即 "1+1"）？

**注意**：即使证明了充分大情形，仍需处理有限范围（但计算机已验证到 $4\times10^{18}$）。

### OPEN-5：Langlands 纲领的应用
Langlands 纲领能否为哥德巴赫提供新路径？如何将二元哥德巴赫编码为自守形式问题？

**当前状态**：纯远景，无具体路径。

### OPEN-6：例外集的本质
例外集 $E(X)$ 的真实增长阶是多少？是 0、$X^\epsilon$、还是 $X^{0.879}$ 附近？

**意义**：若能证明 $E(X)$ 有界，则哥德巴赫猜想对充分大偶数成立（结合计算机验证可完全证明）。

### OPEN-7：分拆数的下界
能否证明 $r_2(N) \geq c\,\mathfrak{S}_2(N)N/\log^2 N$ 对某个 $c>0$ 和所有充分大 $N$ 成立？

**注意**：这比 $r_2(N)>0$ 更强，蕴含哥德巴赫猜想。

---

## 二、关键里程碑

| 年份 | 事件 | 意义 |
|------|------|------|
| 1742 | Goldbach 致信 Euler，提出猜想 | 问题起源 |
| 1900 | Hilbert 第 8 问题 | 列为世纪难题 |
| 1919 | Brun 筛法 | 首个非平凡结果 |
| 1923 | Hardy-Littlewood 圆法 | 解析数论路线开启 |
| 1930 | Schnirelmann 密率 | 加法数论路线开启 |
| 1937 | Vinogradov 三素数定理 | 弱哥德巴赫对充分大奇数证明 |
| 1947 | Selberg 上界筛 | 筛法理论优化 |
| 1966/1973 | 陈景润 "1+2" | 筛法路线最强结果 |
| 1975 | Montgomery-Vaughan 例外集 | $E(X)\ll X^{1-\delta}$ |
| 2004 | Green-Tao 定理 | 素数等差数列，传递原理 |
| 2006 | Pintz 例外集 | $E(X)\ll X^{0.879}$（当前最好） |
| 2013 | Helfgott 弱哥德巴赫完全证明 | 所有奇数 $\geq 5$ 为三素数和 |
| 2013 | Oliveira e Silva 验证至 $4\times10^{18}$ | 有限范围最强验证 |

---

## 三、核心参考文献

### 经典教材

1. **Halberstam, H. & Richert, H.-E.** (1974). *Sieve Methods*. Academic Press.
   - 筛法理论的标准参考书，详细介绍 Brun 筛、Selberg 筛、加权筛。

2. **Vaughan, R. C.** (1997). *The Hardy-Littlewood Method*. 2nd ed. Cambridge University Press.
   - 圆法的标准参考书，包含弱哥德巴赫的完整证明。

3. **Nathanson, M. B.** (1996). *Additive Number Theory: The Classical Bases*. Springer.
   - 加法数论入门，包含 Schnirelmann 密率、哥德巴赫问题。

4. **Tao, T. & Vu, V.** (2006). *Additive Combinatorics*. Cambridge University Press.
   - 加法组合的标准参考书，Gowers 范数、逆定理。

### 关键论文

5. **Chen, J.-R.** (1973). On the representation of a larger even integer as the sum of a prime and the product of at most two primes. *Sci. Sinica*, 16, 157-176.
   - 陈氏定理原文。

6. **Hardy, G. H. & Littlewood, J. E.** (1923). Some problems of 'Partitio numerorum'; III: On the expression of a number as a sum of primes. *Acta Math.*, 44, 1-70.
   - 圆法与哥德巴赫猜想的开创性论文。

7. **Helfgott, H. A.** (2013). The ternary Goldbach conjecture is true. arXiv:1312.7748.
   - 弱哥德巴赫的完全证明。

8. **Green, B. & Tao, T.** (2008). The primes contain arbitrarily long arithmetic progressions. *Ann. of Math.*, 167, 481-547.
   - Green-Tao 定理。

9. **Pintz, J.** (2006). A note on the distribution of primes in arithmetic progressions and the exceptional set in Goldbach's problem. *Acta Arith.*, 123, 45-55.
   - 当前最好的例外集上界。

10. **Oliveira e Silva, T., Herzog, S. & Pardi, S.** (2014). Empirical verification of the even Goldbach conjecture and computation of prime gaps up to $4\times10^{18}$. *Math. Comp.*, 83, 2033-2060.
    - 计算机验证的最新记录。

### 综述

11. **Wang, Y.** (ed.) (2002). *Goldbach Conjecture*. 2nd ed. World Scientific.
    - 哥德巴赫猜想的论文集，包含历史上的关键论文。

12. **Tao, T.** (2007). The dichotomy between structure and randomness, arithmetic progressions, and the primes. *Proceedings of the ICM 2006*.
    - Green-Tao 定理的通俗综述，传递原理的思想。

---

## 四、诚实审计最终结论

1. **哥德巴赫猜想未被证明。** 任何声称"已破解"的说法都是错误的。
2. **15 条研究路线各有其内在限制。** 筛法受奇偶性障碍，圆法受二元余区间，现代工具受变量数下限。
3. **数值证据极强但非证明。** 已验证至 $4\times10^{18}$，但有限验证不能替代无穷证明。
4. **需要本质上的新思想。** 当前共识是，现有方法框架内无法完成证明，需要全新的数学工具或视角。
5. **初等证明极不可能。** 280 多年来无数数学家的尝试表明，初等方法（仅用算术、代数、基本不等式）无法攻克此问题。任何初等"证明"都应首先检查是否犯了本文档列出的 12 类谬误之一。

> **【算法联盟本源物理标准适用说明】** 哥德巴赫猜想是纯数论问题，不涉及物理常数或四大力统一。"算法联盟本源物理标准"（单一几何公理→四大力统一 / 从本源逻辑反向生成物理常数）不适用于此问题。数论问题的判定标准是**数学证明的严格性**，不是物理理论的原创性。
