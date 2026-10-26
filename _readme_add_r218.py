# -*- coding utf-8 -*-
"""r218 README five-point registration (ASCII runner; raw Windows paths)."""
import io
import sys

README = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\README.md"

STEM = ("TUFT-r218_四力统一方程_定义恒等式零判别力覆盖缺与修复定价_精算_2026-10-26")

SRC_LINE = (
    "│   ├── " + STEM + ".py  # 新增（**r218 · 2026-10-26**；★**第六次同型竞态·顺延改号**："
    "起草取 r215 于 02:1x 落盘；登记前复查磁盘时间戳发现并行会话已先占 **r215**（《变分推导"
    "_首次整卷机核_外形式恒等式Cartan秩Higgs质量矩阵…》四件套齐全）、**r216**（挠率不可约分解，"
    "原 r213 同题改名）、**r217**（《四力统一方程独立复核与openuft根目录整理》）⇒ 按「先占位者"
    "为权威、后到者整体改号」铁律**本卷整体改号 r218**（引擎/BASE_NAME/runner/driver/卷内编号"
    "串与红线范围同步联动，未触碰并行任何字节）；**★仲裁现值：下轮从 r219 起**）："
    "**S02 §18《四力统一方程》定义恒等式、预测预算、形状 confrontation 缺口、覆盖缺与修复定价**"
    "（靶 4 份：§18 主文档 + §18_verify.py + §18_四力曲线数据.json + D5 README 语境）。"
    "**条目 19：FAIL 13 / PASS 3 / INFO 3**；**控制组 29/29**、**守卫 12/12**、退出码 0；纯标准库 "
    "Decimal(60)+Fraction+Mon 单项式精确代数。**★L1 定义恒等式（核心）**：把各通道 Q 的定义代入统一式 "
    "F=s·ℏc·Q₁Q₂(1/r²+1/rλ)e^(−r/λ) 后——引力通道 ℏc·Q_g1Q_g2 **单项式精确归约为 G·m₁m₂**"
    "（Q_g:=m/m_P、m_P:=√(ℏc/G)，ℏ 与 c 幂次全消，残差 **0**，非数值近似）；电磁通道 "
    "ℏc·Q_e1Q_e2 **精确归约为 e²Z₁Z₂/(4πε₀)**（α:=e²/4πε₀ℏc，残差 **0**）⇒ 各通道与已知定律的"
    "相符是**定义恒等式**，是 Q 被规定成如此，而非方程推出来的；摄动 Q ±10% ⇒ 相符度偏离约 "
    "19%/21%，方程内部**不存在**「Q 应取何值」的约束（内部推导方程计数 **0**）。**L2 预测预算**："
    "框架内推导外部参数的方程计数 = **0**（符号须边界匹配地在等号左侧、右侧不复现且右侧含框架内部"
    "符号；甄别排除 2 条：α=e²/4πε₀ℏc 是 α 的**定义重排**、F_E/F_G 中的 G 属**子串误命中**；"
    "并设扫描器正对照：注入含内部符号的合成方程命中 2/2，证明计数 0 非恒零无分辨力）⇒ "
    "(G, α, m_W, m_Z, m_π⁰, α_w, g_π²/4π, σ) **全为外部给定**。**L3 形状 confrontation**："
    "该形式**确有**距离律判别力（负对照：同一数量级窗口拟合 r⁻¹/r⁻³/r⁻⁴/r⁻⁵ 最优最大相对误差 "
    "216.2% / 66.5% / 159.2% / 297.8% ⇒ 本卷不指控零判别力）；但机读靶文本+自验证脚本+自产曲线数据"
    "的「实验数据/数据点/散射截面/χ²/最小二乘」比较 token 命中 = **0**，其全部校验项为 λ→∞ 退化的"
    "**恒等式对拍**（V1a/V1b）、力程与强度比的**单位换算**（V2–V4）⇒ 判别力存在而从未行使。**L4 "
    "覆盖与范畴**：参数表 5 行、出形式 1 行（强·色禁闭），文内「四力」10 处、「四种力」2 处；形式内的"
    "「强（剩余核力）」是 π⁰ 交换**剩余核力**（复合层次有效力）而非色相互作用 ⇒ 基本力实际覆盖 "
    "**3/4** + 1 项复合有效力；且两「强」行在重叠窗口 [0.2,1.2] fm 互算矛盾（π-Yukawa / σ = "
    "8.7×–388.6×，靶未 reconcile）。**L5 结构不可表达**：统一式为静态中心标量势梯度 ⇒ 无速度依赖，"
    "**不能承载洛伦兹磁力** qv×B（力式行 21 条、含速度行 **0** 条）；强度只含标量积 Q₁Q₂（宇称偶），"
    "**不能承载弱力 V−A**（全文无 V−A/宇称 token）。**L6**：靶自承关键结果为「Proca 场论标准结果」"
    "⇒ 标准物理重述层。**修复定价 2⁴=16**：四条件（跨通道关系式/覆盖禁闭/覆盖磁力与手征/参数第一性）"
    "齐备的唯一组合必然越过单极齐次 Proca 形式（原方程被替换）⇒ **EMPTY 15 / SUICIDE 1 / SURVIVE 0**"
    "=**本线第 25 度「修复即自杀」**。verdict=R218-FOUR-FORCE-UNIFIED-EQUATION-GRAVITY-AND-EM-CHANNEL-MATCH-IS-DEFINITIONAL-IDENTITY-Q-DEFINED-SO-THAT-HBAR-C-Q1Q2-EQUALS-GM1M2-AND-E2Z1Z2-OVER-4PI-EPS0-EXACT-ZERO-RESIDUAL-PERTURB-Q-BY-10PCT-DEVIATION-19PCT-NO-ENDOGENOUS-CONSTRAINT-EQUATION-0-DERIVED-EXTERNAL-PARAMETERS-PREDICTION-BUDGET-ZERO-ALL-COUPLINGS-AND-MEDIATOR-MASSES-ARE-EXTERNAL-INPUTS-FORM-HAS-SHAPE-DISCRIMINATION-NEGATIVE-CONTROL-FIT-ERRORS-66PCT-TO-298PCT-YET-ZERO-SHAPE-CONFRONTATION-WITH-EXPERIMENT-ALL-CHECKS-ARE-IDENTITIES-AND-UNIT-CONVERSIONS-COVERAGE-3-OF-4-FUNDAMENTAL-FORCES-STRONG-ROW-IS-RESIDUAL-PION-EXCHANGE-NOT-COLOR-CONFINEMENT-OUT-OF-FORM-TWO-STRONG-ROWS-CONTRADICT-IN-OVERLAPPING-WINDOW-RATIO-8P7X-TO-388P6X-UNRECONCILED-STRUCTURALLY-INEXPRESSIBLE-STATIC-SCALAR-POTENTIAL-GRADIENT-CANNOT-CARRY-LORENTZ-MAGNETIC-FORCE-NOR-V-MINUS-A-PARITY-VIOLATION-STANDARD-PHYSICS-RESTATEMENT-PROCA-YUKAWA-SELF-ADMITTED-REPAIR-PRICING-16-COMBOS-SURVIVE-0-SUICIDE-1-EMPTY-15-LINE-25TH-DEGREE-FIX-EQUALS-SUICIDE"
)

VERD_LINE = (
    "│   ├── 判定_" + STEM + ".md  # 新增（**r218 · 2026-10-26**）：**§18 四力统一方程判定册**"
    "（十一节：一 编号与定位（★第六次竞态·整体改号 r215→r218）/ 二 判词 / 三 逐条判定机读表 / "
    "四 定义恒等式（引力与电磁两通道单项式归约残差 0 + 摄动 ±10%⇒19%/21%）/ 五 预测预算（推导方程"
    "计数 0 + 扫描器正对照 2/2）/ 六 形状判别力与 confrontation 缺口（正对照复原 λ、负对照 "
    "66%–298%、比较 token 0）/ 七 覆盖缺与范畴错置（5 行/出形式 1/基本力 3/4/两强行 8.7×–388.6×）/ "
    "八 结构不可表达（磁力与 V−A）/ 九 修复定价 16 组合 SURVIVE 0 / 十 控制组 29/29 与守卫 12/12 / "
    "十一 未闭合项与红线）。条目 **19 = FAIL 13 / PASS 3 / INFO 3**。**控制组 29/29**（λ_W=2.455e-18、"
    "λ_π=1.462e-15、F_E/F_G=1.236e36、σ=2.88e4 N 与靶自报逐位对拍；引力/电磁恒等式解析残差 0；"
    "摄动 C09/C10；推导方程计数 0；拟合器正对照复原 λ<2% 且非 Yukawa 幂律残差>10% 证非放水；"
    "形状比较 token 0；参数表 5 行/出形式 1/声称 token 12；重叠比值>5×；力式含速度行 0；定价 "
    "16 组合 SURVIVE 0 且 EMPTY 15/SUICIDE 1；扫描器正对照 2/2；文本证据 9/9 逐字 + 负对照确未命中；"
    "靶 4 份 sha256 前后一致）。**守卫 12/12 全机读驱动**：G1 FAIL/INFO 均带证据 · G2 verdict 计数驱动 · "
    "G3 分层短语双命中 · G4 靶文件全可读 · G5 证据 9/9+负对照 · G6 ast 自审无字面 True · G7 控制组全过 · "
    "G8 容差按靶有效位 · G9 拟合器先过正对照 · G10 定价三类计数和为 16 · **G11 条目分布机读断言 "
    "{FAIL:13,PASS:3,INFO:3} 且 total=19** · G12 未触碰并行产物。"
)

DATA_LINE = (
    "│   ├── " + STEM + ".json / .md / _report.txt  # 新增（**r218 · 2026-10-26**）§18 四力统一方程"
    "机检产物（**19 条判定** + **12 条守卫** + 控制组 29 项 + constants + 靶 sha256；key_numbers："
    "**引力/电磁通道定义恒等式解析残差 0**、**摄动 ±10% ⇒ 0.21/0.19**、**框架内推导外部参数方程计数 0"
    "（正对照 2/2）**、**λ_W=2.455e-18 m、λ_π=1.4619e-15 m、F_E/F_G=1.2356e36、σ=2.8839e4 N、"
    "m_Planck=2.1764e-8 kg**、**负对照拟合误差 r⁻¹ 216.2% / r⁻³ 66.5% / r⁻⁴ 159.2% / r⁻⁵ 297.8%**、"
    "**形状 confrontation token 0**、**参数表 5 行/出形式 1（强·色禁闭）/「四力」10+「四种力」2**、"
    "**两强行重叠比值 8.7×–388.6×**、**力式行 21 条含速度 0 条、宇称类 token 计数**、"
    "**修复定价 EMPTY 15 / SUICIDE 1 / SURVIVE 0**；verdict=R218-FOUR-FORCE-UNIFIED-EQUATION-…-LINE-25TH-DEGREE-FIX-EQUALS-SUICIDE"
)

ARB_LINE = (
    "> **再更新（2026-10-26 02:43 · 同线续）**：**r218 已被本线占用（第六次同型竞态·顺延改号）** —— "
    "本线 §18 四力统一方程卷起草取 r215、引擎 02:1x 落盘；登记前复查磁盘时间戳发现并行会话已先占 "
    "**r215**（《变分推导_首次整卷机核…》四件套齐全）、**r216**（挠率不可约分解，原 r213 同题改名）、"
    "**r217**（《四力统一方程独立复核与 openuft 根目录整理》）⇒ 按「先占位者为权威、后到者整体改号」"
    "铁律本卷**整体改号 r218**（引擎文件名/BASE_NAME/runner/driver/卷内编号串/红线范围 r142–r217 "
    "同步联动；**未触碰并行任何字节**）；r218 实测首空号、rc=0：条目 19 = FAIL 13/PASS 3/INFO 3，"
    "控制组 29/29、守卫 12/12。**★仲裁现值：下轮实际从 r219 起**（纪律延续：落盘前必须复查磁盘时间戳"
    "而非仅 grep；并行线 r205–r217 十余卷只登增量登记章、不入三树，其目录树刷新仍随 catalog 重生成"
    "统一处理）。"
)

CHAPTER = """

---

### r218 · 2026-10-26 · 四力统一方程（S02 §18）：定义恒等式、预测预算、形状 confrontation 缺口与修复定价

- **命题**：并行 r214 已回答「四力能否写进同一方程 / 求导 / 性质」（另一处导航册来源），r217 又做了
  r214 数字的独立复核 ⇒ 本卷**不重算求导与性质、不复核他卷数字**，只问更上游四件事：①各通道与已知
  定律的相符是否为**定义恒等式**；②**预测预算**（外部输入 vs 框架内推导方程计数）；③该形式本身**有无
  判别力**与**是否曾同实验数据 confrontation**；④覆盖缺 / 范畴 / 结构不可表达 / 修复定价。
- **产物**：`源码/TUFT-r218_四力统一方程_定义恒等式零判别力覆盖缺与修复定价_精算_2026-10-26.py`
  （+ ASCII runner `源码/_run_r218.py` + driver `openuft/_drive_r218.py`）+ `数据/同名.{json,md,_report.txt}`
  + `数据/判定_TUFT-r218_同名.md`。复现 `python -X utf8 openuft/_drive_r218.py`，**退出码 0**；
  **控制组 29/29、守卫 12/12、文本证据 9/9 逐字**。
- **判词**：`R218-FOUR-FORCE-UNIFIED-EQUATION-GRAVITY-AND-EM-CHANNEL-MATCH-IS-DEFINITIONAL-IDENTITY-Q-DEFINED-SO-THAT-HBAR-C-Q1Q2-EQUALS-GM1M2-AND-E2Z1Z2-OVER-4PI-EPS0-EXACT-ZERO-RESIDUAL-PERTURB-Q-BY-10PCT-DEVIATION-19PCT-NO-ENDOGENOUS-CONSTRAINT-EQUATION-0-DERIVED-EXTERNAL-PARAMETERS-PREDICTION-BUDGET-ZERO-ALL-COUPLINGS-AND-MEDIATOR-MASSES-ARE-EXTERNAL-INPUTS-FORM-HAS-SHAPE-DISCRIMINATION-NEGATIVE-CONTROL-FIT-ERRORS-66PCT-TO-298PCT-YET-ZERO-SHAPE-CONFRONTATION-WITH-EXPERIMENT-ALL-CHECKS-ARE-IDENTITIES-AND-UNIT-CONVERSIONS-COVERAGE-3-OF-4-FUNDAMENTAL-FORCES-STRONG-ROW-IS-RESIDUAL-PION-EXCHANGE-NOT-COLOR-CONFINEMENT-OUT-OF-FORM-TWO-STRONG-ROWS-CONTRADICT-IN-OVERLAPPING-WINDOW-RATIO-8P7X-TO-388P6X-UNRECONCILED-STRUCTURALLY-INEXPRESSIBLE-STATIC-SCALAR-POTENTIAL-GRADIENT-CANNOT-CARRY-LORENTZ-MAGNETIC-FORCE-NOR-V-MINUS-A-PARITY-VIOLATION-STANDARD-PHYSICS-RESTATEMENT-PROCA-YUKAWA-SELF-ADMITTED-REPAIR-PRICING-16-COMBOS-SURVIVE-0-SUICIDE-1-EMPTY-15-LINE-25TH-DEGREE-FIX-EQUALS-SUICIDE`
- **条目 19 = FAIL 13 / PASS 3 / INFO 3**；**控制组 29/29**；**守卫 12/12 全机读驱动**。
- **核心结论**：
  1. **定义恒等式（核心）**：引力通道以 Q_g:=m/m_P、m_P:=√(ℏc/G) 代入 ⇒ ℏc·Q_g1Q_g2 的单项式**精确
     归约为 G·m₁m₂**（ℏ、c 幂次全消，解析残差 **0**）；电磁通道以 α:=e²/4πε₀ℏc、Q_e:=√α·Z 代入 ⇒
     **精确归约为 e²Z₁Z₂/(4πε₀)**。两通道与已知定律的相符是**把 Q 规定成如此**的结果，而非方程推出；
     摄动 Q ±10% ⇒ 相符度偏离 21%/19%，且框架内**不存在**「Q 应取何值」的约束（推导方程计数 0）。
  2. **预测预算 = 0**：框架内推导 (G, α, m_W, m_Z, m_π⁰, α_w, g_π²/4π, σ) 的方程计数 = **0**；甄别
     排除 2 条（α 的定义重排、F_G 的子串误命中），并设**扫描器正对照**（注入含内部符号的合成方程命中
     2/2）证明计数 0 不是恒零无分辨力。对靶有利项单列：λ_W、λ_π、F_E/F_G、σ 四个换算与靶自报逐位对拍通过。
  3. **形状 confrontation 缺口**：该形式**确有**距离律判别力——负对照在同一数量级窗口拟合 r⁻¹/r⁻³/r⁻⁴/r⁻⁵，
     最优最大相对误差 **216%/66.5%/159%/298%** ⇒ 本卷**不**指控「零判别力」；但机读靶文本+自验证脚本+
     自产曲线数据，「实验数据/数据点/散射截面/χ²/最小二乘」比较 token 命中 = **0**，其校验项全为恒等式
     对拍与单位换算 ⇒ **判别力存在而从未行使**，已验内容 0 bits。
  4. **覆盖 3/4 + 范畴错置**：参数表 5 行、出形式 1 行；形式内的「强（剩余核力）」是 π⁰ 交换**剩余核力**
     而非色相互作用，基本强力恰在出形式行 ⇒ 基本力实覆盖 **3/4**。且两「强」行在重叠窗口 [0.2,1.2] fm
     互算矛盾：π-Yukawa / σ = **8.7×–388.6×**，靶未 reconcile。
  5. **结构不可表达**：统一式为静态中心标量势梯度 ⇒ 无速度依赖，不能承载洛伦兹磁力 qv×B（力式行 21 条、
     含速度 **0** 条）；强度只含标量积 Q₁Q₂（宇称偶），不能承载弱力 V−A（全文无 V−A/宇称 token）。
  6. **修复定价**：四条件（跨通道关系式 / 覆盖禁闭 / 覆盖磁力与手征 / 参数第一性）齐备的唯一组合必然越过
     单极齐次 Proca 形式（原方程被替换）⇒ **EMPTY 15 / SUICIDE 1 / SURVIVE 0**，**本线第 25 度「修复即自杀」**。
- **分层声明（条目不可跨册相加）**：本卷不重判 D5 主体方程 P=m(c−v)（本线 r181 已判），不复核并行
  r214/r216/r217 的数字与结论；只做上游四问。**不可与 r142–r217 相加**。
- **取号（第六次同型竞态·整体改号）**：起草取 r215、引擎 02:1x 落盘；登记前复查磁盘时间戳发现并行已占
  **r215/r216/r217** ⇒ 按「先占位者为权威、后到者整体改号」铁律整体改号 **r218**（未触碰并行任何字节）；
  **下轮从 r219 起**（落盘前仍须复查时间戳）。
- **自抓 5 处（已修，重跑 rc=0）**：①**方程扫描器子串误命中**——`F_E/F_G=α(m_P/m_p)²` 中的字母 G 被当作
  「推导 G」、`α=e²/…` 被当作推导 ⇒ 改**边界正则 + 右侧须含框架内部符号**，并加**正对照**（注入合成方程
  命中 2/2 证非恒零）；②**修复定价评分序放水**——原「先判自杀」把 {C0,C3} 误判为 SURVIVE ⇒ 改为
  **四条件齐备才可能成立**，得 EMPTY 15/SUICIDE 1/SURVIVE 0；③**%-格式化串与正文 `%` 冲突**（「10% ⇒」
  触发 ValueError）⇒ 改 `.format`；④**控制组元组被当字典索引**（`c["ok"]` TypeError）⇒ 改 `c[2]`；
  ⑤**docstring 含 `\pi` 触发 SyntaxWarning** ⇒ 改 raw docstring。另：G6/G11 从 ast 白名单移除，改真机读。
- **治理**：未跑 refresh_catalog.py（并发活跃待批准）；未改 `verify.py`；未做 git；靶 4 份只读
  （sha256 前后一致）；未触碰并行会话任何字节；临时脚本已归入 `openuft/_scratch_r218/`。
"""


def main():
    with io.open(README, "r", encoding="utf-8") as f:
        lines = f.read().split("\n")

    def find_one(pred, desc):
        idx = [i for i, ln in enumerate(lines) if pred(ln)]
        if len(idx) != 1:
            print("FATAL: %s matched %d lines" % (desc, len(idx)))
            sys.exit(3)
        return idx[0]

    i_src = find_one(lambda ln: ln.startswith("│   ├── TUFT-r203_S13兄弟链跨轮互印")
                     and ".py" in ln, "r203 src line")
    i_ver = find_one(lambda ln: ln.startswith("│   ├── 判定_TUFT-r203_S13兄弟链跨轮互印"),
                     "r203 verdict line")
    i_dat = find_one(lambda ln: ln.startswith("│   ├── TUFT-r203_S13兄弟链跨轮互印")
                     and ".json" in ln, "r203 data line")
    i_arb = find_one(lambda ln: ln.startswith("> **再更新（2026-10-25 22:57 · 同线续）**"),
                     "r203 arb line")
    if any(ln.startswith("### r218 ") for ln in lines):
        print("FATAL: r218 chapter already present")
        sys.exit(4)
    if any(STEM in ln for ln in lines):
        print("FATAL: r218 stem already registered")
        sys.exit(5)

    lines.insert(len(lines), CHAPTER)
    lines.insert(i_arb + 1, ARB_LINE)
    lines.insert(i_dat + 1, DATA_LINE)
    lines.insert(i_ver + 1, VERD_LINE)
    lines.insert(i_src + 1, SRC_LINE)

    with io.open(README, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("OK: 5 insertions done (src/verdict/data/arb/chapter)")


if __name__ == "__main__":
    main()
