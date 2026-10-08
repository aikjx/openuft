# TUFT V3.4 路线2：重子不对称时间演化 ODE 报告
- 引擎：源码/TUFT_V3.4路线2_重子不对称ODE_2026-10-07.py
- 对象：辐射主导 FRW 中 Y_B 的 ODE 演化 + 冻结 + 匹配 Y_obs
- 读数：4 guard PASS 4/FAIL 0 (exit 0)

| PASS | analytic_integration | 解析 9.551e-12 vs 数值 9.551e-12（0.00%） |
| PASS | freeze_temperature | 冻结温度在 ~1e9-1e15 GeV 合理窗 |
| PASS | match_family | 匹配族：['(tau=1e-02 beta=9.11e-05 Y=8.70e-11)', '(tau=1e-03 beta=9.11e-04 Y=8.70e-11)', '(tau=1e-04 beta=9.11e-03 Y=8.70e-11)'] |
| PASS | beta_is_fit | 同一 Y_obs 多组 (beta,tau_bg) 匹配 → beta 非唯一预言 |

### 关键结果
| 量 | 值 | 含义 |
|---|---|---|
| 解析 Y_B(b=1e-4,tau=1e-3) | 9.551e-12 | 解析积分 |
| 冻结 T_f(b=1e-4,tau=1e-3) | 7.12e+10 GeV | H=Gamma 条件 |
| 观测 Y_B | 8.7e-11 | 目标 |

### 结论（路线2）
1. **解析可积**：辐射主导下 Y_B=beta*tau*dT/(1.66*sqrt(g*)*M_P)，数值 RK4 交叉吻合（<5%%）。
2. **冻结自洽**：T_f=beta*tau*M_P/(1.66*sqrt(g*)) 落在合理窗，比 V3.4 文本硬编码 Tf=1e16 自洽。
3. **匹配 Y_obs=8.7e-11 是一族 (beta,tau_bg)**：tau=1e-3->beta~1e-4，tau=1e-2->beta~1e-5——beta 不唯一，非预言。
4. **诚实裁定**：ODE 给出正确的量级/温度演化，但 beta 仍是自由拟合参数。TUFT 要成为预言，必须从不动点（路线1）或耦合自洽导出 beta。
5. **路线建议**：路线2 完成演化框架，但需与路线1（不动点导出 beta）或路线4（PRD 整合）衔接才能真正预言。