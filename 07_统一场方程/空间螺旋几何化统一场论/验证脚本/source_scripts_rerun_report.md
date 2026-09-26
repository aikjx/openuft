# 来源脚本复跑与「自陈 PASS」核验报告

> 生成：`rerun_source_scripts.py`（本文件为运行产物，非手写）
> 对象：`90_历史归档/来源语料_20260611_螺旋几何化统一场论文章/code/` 下的全部 `.py`
> 依赖：仅 Python 标准库；被复跑的脚本另行需要 `mpmath` / `sympy` / `numpy` + `matplotlib`

## 0. 结论

**这批脚本的「全部验证通过」在结构上不可能是判据的输出。**

| 读数 | 值 |
|---|---|
| 脚本总数 | 11 |
| **基线即非零退出（跑不起来）** | **1 个**：`unified_field_theory_ultimate_verification.py` |
| 失败通路合计（assert / sys.exit / SystemExit） | **0 处**，覆盖 11 / 11 个脚本 —— 脚本不可能以失败告终 |
| **自己打印了失败项**的脚本 | **4 个 / 合计 8 条**（原文却称「全部验证通过」） |
| 不受任何条件分支约束的结论句 | **12 处**（写死在 `write()` / `print()` 里） |
| α 改错 1e-8 后**判定与失败项均不变**的脚本 | **4 / 7**（有判定语句的脚本） |
| α 改错 1e-8 后判定或失败项**改变**的脚本 | 3 / 7 |
| α 改错后**产物结论句逐字保留**的脚本 | **3 / 3**（结论句对输入改错完全免疫） |
| 归档产物与复跑逐字节一致 | 5 / 5 |
| 归档产物与复跑不一致 | 0 |

五条要分开读：

1. **结构上不可能失败。** 11 个脚本的 `assert` / `sys.exit` / `raise SystemExit` 合计 **0 处**；
   凡是写结论句的地方都不在任何条件分支之内（合计 12 处，见第 6 节）。
2. **跑得起来的几个，自己就报了失败。** `full_verification.py` 打印 `13/16`（3 条 `[FAIL]`）、
   `complete_verification.py` 打印 `21/22`（1 条 `[FAIL]`）、`all_dimension_breakthrough.py` 打印 2 条
   `❌ 失败`、`infinite_dimension_verification.py` 打印 2 条失败 —— 而原文一律称「全部验证通过」。
   失败项落在两类地方：**CODATA 常数彼此的互验**（`alpha = e²/(4πε₀ℏc)`、`G = 4πα³ℏcρ²/e²`、
   `G·e² = 4πα³ℏcρ²`）与**阈值本身**（`all_dimension_breakthrough.py` 把「相对误差 6.38e-9 %」判成失败；
   `infinite_dimension_verification.py` 用 1e-90 去卡一个**截断到 100 项**的级数）。
   把 α 改错 1e-8，这些失败项的**数目一个不变**（1→1、3→3、2→2）—— 说明它们来自输入侧/阈值侧，
   与 α 的取值无关。
3. **有 1 个脚本根本跑不起来。** `unified_field_theory_ultimate_verification.py` 在第 194 行
   抛 `NameError: name 'G' is not defined`（脚本只定义了 `G_codata`），死在「8. ε₀ 几何化验证」，
   **从未跑到任何总结**；归档目录里也相应没有它的 `*_results.txt`。
4. **结论句与算出来的数没有耦合。** 把 α 改错 1e-8，差值变了、产物里的结论句 3 / 3 逐字保留。
5. **判定翻转只发生在「与写死的常数比对」上。** α 改错 1e-8 后翻转的 2 个脚本：
   `1.py` 新增的失败项是「宇宙本征常数 N 是否等于源码里写死的 30 位常数」（回归锁），
   `all_dimension_breakthrough.py` 是无条件的「认证通过」输出消失（失败项 2→3）。
   没有一条翻转发生在被宣称检验的物理关系上（见第 3B 节）。
   另有三处口径需要读源码（第 7 节）：`ΣF_i/ΣF_j ≡ 1` 被当成归一化检验；
   「四力归一化」被补到七项才够过 1e-10 阈值；同一运行里既打「失败」又打「全部通过」。

**它们能证明的**：作者自己的定义链在代数上自洽（内部一致）。
**它们不能证明的**：任何一条与外部世界有关的量 —— 包括 α、G、ρ 的取值。

## 1. 逐脚本结果

| 脚本 | 退出码 | 耗时 | 自陈判定 | 自陈失败项 | 失败通路 | 不受条件约束的结论句 | α 改错 1e-8 | G 改错 1e-8 |
|---|---|---|---|---|---|---|---|---|
| `1.py` | 0 | 0.5s | SUCCESS所有验证全部通过 | 0 | 0 | 0 | exit=0<br>判定 **改变**<br>失败项 **改变**<br>产物 不变<br>产物结论句 不变 | exit=0<br>判定 不变<br>失败项 不变<br>产物 不变<br>产物结论句 不变 |
| `all_dimension_breakthrough.py` | 0 | 0.4s | 认证通过 | 2 | 0 | 3 | exit=0<br>判定 **改变**<br>失败项 **改变**<br>产物 **改变**<br>产物结论句 不变 | exit=0<br>判定 不变<br>失败项 不变<br>产物 **改变**<br>产物结论句 不变 |
| `complete_verification.py` | 0 | 0.7s | Result:21/22testspassed | 1 | 0 | 0 | exit=0<br>判定 不变<br>失败项 不变<br>产物 不变<br>产物结论句 不变 | exit=0<br>判定 不变<br>失败项 不变<br>产物 不变<br>产物结论句 不变 |
| `core_verification.py` | 0 | 0.6s | Result:5/5verificationspassed | 0 | 0 | 0 | exit=0<br>判定 不变<br>失败项 不变<br>产物 不变<br>产物结论句 不变 | exit=0<br>判定 不变<br>失败项 不变<br>产物 不变<br>产物结论句 不变 |
| `force_origin_visualization.py` | 0 | 3.9s | (无) | 0 | 0 | 0 | N/A | N/A |
| `force_origin_visualization_en.py` | 0 | 4.2s | (无) | 0 | 0 | 0 | N/A | N/A |
| `full_verification.py` | 0 | 0.5s | Result:13/16testspassed | 3 | 0 | 0 | exit=0<br>判定 不变<br>失败项 不变<br>产物 不变<br>产物结论句 不变 | exit=0<br>判定 不变<br>失败项 不变<br>产物 不变<br>产物结论句 不变 |
| `g_alpha2_mu0_infinite_breakthrough.py` | 0 | 2.4s | (无) | 0 | 0 | 6 | exit=0<br>判定 不变<br>失败项 不变<br>产物 **改变**<br>产物结论句 不变 | N/A |
| `infinite_dimension_verification.py` | 0 | 1.9s | 含失败项 | 2 | 0 | 3 | exit=0<br>判定 不变<br>失败项 **改变**<br>产物 **改变**<br>产物结论句 不变 | N/A |
| `paper_verification.py` | 0 | 0.6s | Result:14/14testspassed | 0 | 0 | 0 | exit=0<br>判定 不变<br>失败项 不变<br>产物 不变<br>产物结论句 不变 | exit=0<br>判定 不变<br>失败项 不变<br>产物 不变<br>产物结论句 不变 |
| `unified_field_theory_ultimate_verification.py` | 1 | 0.6s | (无) | 0 | 0 | 0 | exit=1<br>判定 不变<br>失败项 不变<br>产物 不变<br>产物结论句 不变 | exit=1<br>判定 不变<br>失败项 不变<br>产物 不变<br>产物结论句 不变 |

> 单元格：「不变」= 该输入改错 1e-8 后这一栏与基线逐字相同 ⇒ 该脚本的这部分输出对这个输入**没有约束力**。
> `产物` 比较 `*_results.txt` / `*.png` 的 SHA-256；`产物结论句` 比较结论句清单。

## 2. 基线就失败的脚本

| 脚本 | 退出码 | 最后一行异常 |
|---|---|---|
| `unified_field_theory_ultimate_verification.py` | 1 | `NameError: name 'G' is not defined` |

> 跑不起来的脚本，其宣称的验证项在本机**从未被执行过**；归档目录里也相应缺少它的 `*_results.txt`（见第 4 节）。

## 3. 基线自陈的失败项（带上下文）

### `all_dimension_breakthrough.py` —— 自陈 2 条

```text
  相对误差 = 6.376680325e-9 %

  验证结果：❌ 失败

================================================================================

  相对误差 = 6.376680324e-9 %

  验证结果：❌ 失败

================================================================================

```

### `complete_verification.py` —— 自陈 1 条

```text
  [PASS] rho = sqrt(G*eps0)/alpha
  [PASS] mu0*eps0*c^2 = 1
  [FAIL] alpha = e^2/(4*pi*eps0*hbar*c)
  [PASS] kappa^2+tau^2 = 1/(rho^2+b^2)
  [PASS] c^2 = omega^2/(kappa^2+tau^2)

```

### `full_verification.py` —— 自陈 3 条

```text
  [PASS] rho = sqrt(G*eps0)/alpha
  [PASS] G = alpha^2*mu0*c^2*rho^2
  [FAIL] G = 4pi*a^3*hbar*c*rho^2/e^2
  [FAIL] G*e^2 = 4pi*a^3*hbar*c*rho^2
  [PASS] mu0*eps0*c^2 = 1

  [PASS] G = alpha^2*mu0*c^2*rho^2
  [FAIL] G = 4pi*a^3*hbar*c*rho^2/e^2
  [FAIL] G*e^2 = 4pi*a^3*hbar*c*rho^2
  [PASS] mu0*eps0*c^2 = 1
  [FAIL] alpha = e^2/(4pi*eps0*hbar*c)

  [FAIL] G*e^2 = 4pi*a^3*hbar*c*rho^2
  [PASS] mu0*eps0*c^2 = 1
  [FAIL] alpha = e^2/(4pi*eps0*hbar*c)
  [PASS] v_total = c
  [PASS] tan(phi) = alpha

```

### `infinite_dimension_verification.py` —— 自陈 2 条

```text
差值 = -1.440140243138374096710109710277349218508138358864395729986982891814521622194484258191975474277785739E-9
相对误差 = -0.00001973510570251403606720774772543176295227029906953230368359631651035125422569154146181776067044462655%
验证结果：失败

================================================================================

前12种力归一化总和 = 0.9999999999999999999999999771974217308814118629530023972309798441863609159900036487042023952516362019
差值 = -2.280257826911858813704699760276902015581363908400999635129579760474836379814564239724213137690158656E-26
验证结果：失败

================================================================================

```


## 3B. 变异后才出现的失败项（判定翻转发生在哪一条）

| 脚本 | 基线判定 | α 改错 1e-8 后判定 | 失败项数（基线→变异） | 变异后新增的失败项 |
|---|---|---|---|---|
| `1.py` | SUCCESS所有验证全部通过 | WARN部分验证项未通过 | 0 → 1 | `FAIL 宇宙本征常数验证失败` |
| `all_dimension_breakthrough.py` | 认证通过 | 含失败项 | 2 → 3 | `验证结果：❌ 失败` |

> 读法：翻转的脚本里，`1.py` 新增的失败项是 **`FAIL 宇宙本征常数验证失败`** ——
> 即「算出来的 N 是否等于源码里写死的那个 30 位常数」，属**回归锁**（锁住 α 的取值），
> 不是任何一条被宣称检验的物理关系。另一处（`all_dimension_breakthrough.py`）变的是
> 无条件的「认证通过」输出消失，其失败项文本不变（变的是上下文里的数值）。

## 4. 归档产物 vs 复跑产物

| 脚本 | 复跑在临时目录生成 | 与归档比较 |
|---|---|---|
| `1.py` | - | - |
| `all_dimension_breakthrough.py` | `all_dimension_breakthrough_results.txt` | `all_dimension_breakthrough_results.txt` 逐字节一致 |
| `complete_verification.py` | - | - |
| `core_verification.py` | - | - |
| `force_origin_visualization.py` | `force_origin_visualization.png` | `force_origin_visualization.png` 逐字节一致 |
| `force_origin_visualization_en.py` | `force_origin_visualization_en.png` | `force_origin_visualization_en.png` 逐字节一致 |
| `full_verification.py` | - | - |
| `g_alpha2_mu0_infinite_breakthrough.py` | `g_alpha2_mu0_infinite_breakthrough_results.txt` | `g_alpha2_mu0_infinite_breakthrough_results.txt` 逐字节一致 |
| `infinite_dimension_verification.py` | `infinite_dimension_verification_results.txt` | `infinite_dimension_verification_results.txt` 逐字节一致 |
| `paper_verification.py` | - | - |
| `unified_field_theory_ultimate_verification.py` | - | - |

> 逐字节一致 ⇒ 归档产物**确为该脚本的真实输出**，未被事后手改（这一点是归档可信度的正面证据）；
> 不一致 ⇒ 归档产物不是当前脚本的输出（需人工核查来源）。本次一致 5 项、不一致 0 项。

## 5. 静态扫描明细

| 脚本 | assert | sys.exit | SystemExit | dps 声明 | α 字面量有效位 | G 字面量有效位 | 判据阈值 |
|---|---|---|---|---|---|---|---|
| `1.py` | 0 | 0 | 0 | 10000 | 16 | 8 | 1e-100、1e-20 |
| `all_dimension_breakthrough.py` | 0 | 0 | 0 | 1000 | 16 | 8 | 1e-10、1e-20、1e-40、1e-90 |
| `complete_verification.py` | 0 | 0 | 0 | 10000 | 16 | 8 | 1e-100 |
| `core_verification.py` | 0 | 0 | 0 | 10000 | 16 | 8 | 1e-10、1e-100 |
| `force_origin_visualization.py` | 0 | 0 | 0 | - | - | - | - |
| `force_origin_visualization_en.py` | 0 | 0 | 0 | - | - | - | - |
| `full_verification.py` | 0 | 0 | 0 | 10000 | 16 | 8 | 1e-100 |
| `g_alpha2_mu0_infinite_breakthrough.py` | 0 | 0 | 0 | - | 12 | - | 1e-90 |
| `infinite_dimension_verification.py` | 0 | 0 | 0 | - | 12 | - | 1e-10、1e-90 |
| `paper_verification.py` | 0 | 0 | 0 | 10000 | 16 | 8 | 1e-100 |
| `unified_field_theory_ultimate_verification.py` | 0 | 0 | 0 | 10000 | 16 | 8 | 1e-10、1e-100 |

## 6. 不受条件分支约束的结论句（逐条）

### `all_dimension_breakthrough.py`（3 处）

- 第 346 行：`f.write(f"验证结果: 通过\n\n")`
- 第 357 行：`f.write("全维度几何化无量纲化终极统一达成！\n")`
- 第 358 行：`f.write("算法联盟最高权限认证通过！\n")`

### `g_alpha2_mu0_infinite_breakthrough.py`（6 处）

- 第 257 行：`print("✅ G = α²μ₀c²ρ² 无量纲化验证通过！")`
- 第 258 行：`print("✅ 引力常数几何本源推导成功！")`
- 第 259 行：`print("✅ 无穷维力系归一化验证通过！")`
- 第 260 行：`print("✅ 五种力归一化验证通过！")`
- 第 261 行：`print("✅ G 与 α 的深层关系验证通过！")`
- 第 308 行：`f.write("算法联盟最高权限认证通过！\n")`

### `infinite_dimension_verification.py`（3 处）

- 第 127 行：`print(f"验证结果：所有比值均等于 alpha，验证通过")`
- 第 198 行：`print("✅ 所有验证全部通过！")`
- 第 199 行：`print("✅ 无穷维力系统一场论精算验证成功！")`

> 这些句子与同段里算出来的「差值」是两条互不相干的语句：差值算成多少，句子照写。
> 判据：「不受条件分支约束」= 语句本身不是行内三元、且往上 8 行内没有同层或更外层的 `if/else/for/while/try`。

> 口径提示（详见第 7 节 (a)(b)）：「四力归一化 = 1」的缺口在代码里被两套手法绕开 ——
> 一是把分母换成自除（`ΣF_i/ΣF_j ≡ 1`），二是把 1/α²、1/α、1、α 补到 1/α⁷。都不是新的物理。

## 7. 人工核对的三处口径（源码级，逐行）

自动化读数之外，有三处口径需要读源码才能说清；它们都**不是**本次复跑发现的新缺陷，
而是给复算层已有的 X13 补上「它在代码里长什么样」：

**(a) `1.py` 第 106–112 行：归一化总和恒等于 1。**

```text
F_total = F_gravity + F_strong + F_weak + F_electromagnetic + F_fifth
norm_gravity = F_gravity / F_total          # …… 其余四项同
norm_total = norm_gravity + norm_strong + norm_weak + norm_electromagnetic + norm_fifth
```

`norm_total = Σ F_i / Σ F_j ≡ 1` —— 对**任意** F 值、任意 α 都恒成立。
于是第 170 行 `if abs(norm_total - 1) < mp.mpf("1e-100")` 必然进 PASS 分支，
打印「OK 五种力归一化验证通过，总和精确等于1」。**这条不是检验，是 (Σx)/Σx = 1。**
注意它的分母 **不是** 文献里的 N：五个强度因子之和 `1/α²+1/α+1+α+α² ≈ 18916.9083945` 与
`N = 1/[α²(1−α)] ≈ 18916.9083949` 相差 α³/(1−α) ≈ **3.9e-7**（绝对），相对差 α⁵ ≈ 2.1e-11 ——
正是被截掉的那截高阶项。也就是说：**同一个脚本里，「ρ 由 G 反解」用的是 N 的口径，
「五力归一化 = 1」用的是自除口径，两者相差在 1e-7 量级，而检验阈值写着 1e-100。**

**(b) `core_verification.py` 第 57 行：把「四力」悄悄补成七项才够过阈值。**

```text
forces = {… 'Gravity':1/alpha**2, 'Strong':1/alpha, 'Weak':1, 'Electro':alpha,
          '5th':alpha**2, '6th':alpha**3, '7th':alpha**4}
```

判据是 `abs(total_norm - 1) < 1e-10`（第 105 行），而 `total_norm = Σ factor / N`：

- 只取**四力**（引力/强/弱/电磁）：`Σ/N = 1 − α⁴` ⇒ 缺口 **2.836e-09** ⇒ 必然 FAIL（与复算层 X13 的 2.836e-09 同源）；
- 补上 5th/6th/7th 三项：`Σ/N = 1 − α⁷` ⇒ 缺口 **1.10e-15** ⇒ 落在 1e-10 之内，通过。

⇒ 阈值 1e-10 恰好卡在 α⁴ 与 α⁷ 之间：**决定「通过」的不是物理，是补了几项。**

**(c) `infinite_dimension_verification.py`：同一次运行里既打印「失败」又打印「全部通过」。**

第 41 / 52 / 82 / 99 / 112 / 148 / 159 / 176 / 191 行是**条件**判定：

```text
print(f"验证结果：{'通过' if abs(...) < 1e-90 else '失败'}")     # 9 处，形态一致
```

本次复跑其中 **2 条判为「失败」**（一条相对误差 −1.97e-5 %，一条 12 项归一化差值 −2.28e-26）。
紧接着第 198 行是**无条件**的，第 244 行同样**无条件**写进结果文件：

```text
print("✅ 所有验证全部通过！")                              # 第 198 行，无 if
f.write("综合结论：所有验证全部通过！\n")                    # 第 244 行，无 if
```

⇒ 归档的那份 `infinite_dimension_verification_results.txt` 与复跑**逐字节一致**（见第 4 节），
而它全文的结论句只有「综合结论：所有验证全部通过！」与「无穷维力系统一场论精算验证成功！」两句：
**数值都写进了文件，判定一条都没写；控制台上明明白白打了两个「失败」，文件里只剩「全部通过」。**

## 8. 精度声明 vs 输入精度

脚本普遍声明 `mp.mp.dps = 10000`，但 α、G 是以 16 位有效数字的**字面量**送入的；
`sp.Float(1/137.035999074, 100)` 这种写法还先由 Python 双精度求商、再转高精度对象。
⇒ **输出打印 30–50 位不等于那 30–50 位有意义**；这也是「1e-100 阈值」能通过的直接原因 ——
被比较的两端是同一个 16 位输入的两种写法。

## 9. 复跑环境

- 解释器：`3.8.8 (tags/v3.8.8:024d805, Feb 19 2021, 13:18:16) [MSC v.1928 64 bit (AMD64)]`
- 工作目录：临时目录（**不在归档目录内跑** —— 脚本会往 CWD 写 `*_results.txt` / `*.png`）
- 单脚本超时：600s，变异步长：±1e-08（相对）

## 10. 与 `spiral_geometry_audit.py` 的关系

| 层 | 复算什么 | 输入 |
|---|---|---|
| `spiral_geometry_audit.py` | **主张**（体系一到十）的数值 / 量纲是否自洽 | CODATA + 纯数学恒等式，独立于原文献 |
| 本报告 | **来源脚本的自陈 PASS** 里有没有信息量 | 原封不动复跑原脚本 + 变异探针 |

两者互不替代；本报告的读数**支持并加强**复算层此前的两条判定：
`G=α²μ₀c²ρ²` 的数值吻合是 ρ 由 G 反解之后的同义反复（X2 / X8），
以及「四力归一化 = 1」在文献口径下并不精确成立（X13）。

## 11. 红线

- 本脚本**不改写**归档里的任何文件；变异体只存在于临时目录，跑完即删。
- 「判定不变」是**该脚本的判据无信息量**的证据，**不是**其主张为假的证明；
  主张为假需要独立复算（见第 9 节第一行）。
- 退出码恒为 0：审计发现同义反复不等于审计失败。
- **数学自洽 != 实验证实。**

