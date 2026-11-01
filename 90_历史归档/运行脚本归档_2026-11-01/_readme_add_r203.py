# -*- coding utf-8 -*-
"""r203 README five-point registration (ASCII runner; raw Windows paths)."""
import io
import re
import sys

README = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\README.md"

SRC_STEM = "TUFT-r203_S13兄弟链跨轮互印与no-go独立复核_r188xr189xr192口径对拍与ThetaCP2四腿复算_精算_2026-10-25"

SRC_LINE = (
    "│   ├── " + SRC_STEM + ".py  # 新增（**r203 · 2026-10-25**；★**第五次同型竞态·和平共处无改号**："
    "起草前 22:00:48 实测 r203/r204 三树全空，引擎 22:50:18 落盘；并行会话 22:46:54 落 **r204**"
    "（《质量定义方程_常数k多值冲突与公理自毁继承》），其登记章明文「**r203 被并行《S13兄弟链跨轮互印》占用**；"
    "r204 三树全空为唯一首空号」⇒ 双方无冲突、**无需改号**，本线惯例五处登记仍执行；**★仲裁现值：下轮从 r205 起**）："
    "**S13 兄弟链跨轮互印 + r192 no-go 四腿独立复算 + r188 重审条件核验**（靶 6 份脚本/文档 + peer 14 件 JSON）。"
    "**条目 15：FAIL 4 / PASS 7 / INFO 3 / BOUNDARY 1**；**控制组 31/31**、**守卫 12/12**、退出码 0；纯标准库 "
    "Decimal(60)+Fraction+CF 复分数。**跨轮互印 23/23 行全一致**（v、M*、M*/v、x*、x₁₂、M(x₁₂)、x_GUT、M_GUT、"
    "α_GUT⁻¹、s*、gap_sm/gap_ms RK4、M_sm/M_ms RK4、SM/MSSM 闭式 gap%、SM 交点 M、β×2、Higgs、Θ²、CP² χ、ℓ_EW 共 23 项，"
    "机读 + 独立重算对拍；14 件 peer JSON sha256 前后一致证只读）。**两条链级事实**：①**s* 精度层**——r189 float64 "
    "`0.230943405280905872389851651860` vs 本卷 Decimal(60) 前 **16 位有效数字一致**（第 17 位起分歧，相对差 1.589e-17 "
    "= float eps 量级）；M_GUT 的 π 位层差 2.511e-15（r194/r195/r199 用 60 位 π，r188/r192 用 16 位 str(math.pi)）；"
    "M* 渲染层差 1.437e-18 ⇒ 全部 ≤1ulp，**非口径冲突**。②**x_GUT 混用 lineage**——r192 同轮 x_GUT=5.2547892800（α₁=α₂）"
    "配 M_GUT=2.121000E+16（α₁=α₃/s*），重算 M(x)=19904728656526579.008，相对差 **0.06154（6.15%）**；"
    "r194 Q1 自纠（规范值 5.2648981057393271）+ r199 标注，链完整。**no-go 四腿独立复算（全 Fraction/CF 精确）**："
    "Θ²=−I=+I（矩阵层 + 200 随机复旋量算子层残差 **0**）· εσᵢε⁻¹=−σᵢᵀ **3/3** · 反幺正 Θ(iψ)=−iΘψ + Θ²=−I **6/6** "
    "⇒ Majorana 实条件 · CP² Betti (1,0,1,0,1)/χ=3/c₁=3H/h²⁰=0 ⇒ 非 hyperkähler（外部标准数学标注）· "
    "FS Kähler 类齐次残差 **精确 0**（两点×三 λ 共 **32 项等式**）· M5 族 g_ℓ(ℓ²/r)=g_ℓ(r) 对任意 ℓ 恒等（残差 **0**）"
    "⇒ ℓ 信息量 0 bit · RG 参考尺度不变性 **9/9**（残差 4.71e-60）· **101 文件截断后**七类 inventory **0 命中**"
    "（截断前原始 1 处全在 ch25 附节内——截断纪律机读见证）· Higgs 谱 {0,0,0,8κv²} ⇒ 4 实模式 = 1 重态 ≠ MSSM 2。"
    "**候选扫描**：自有基准 23 基元×2（倒数）三因子多项式 = **17,296 组合 0 命中**（tol 1e-9）+ 注入正对照 5/5；"
    "r192 记录机读（N=39,710 ≥10⁴、0 命中、正对照 5/5）；60 基元池构成未登记 ⇒ 39,710 **未重造**（BOUNDARY/INFO）。"
    "verdict=R203-CROSS-ROUND-MUTUAL-VERIFICATION-23-ROWS-23-CONSISTENT-1-XGUT-LINEAGE-CONFLICT-SELF-CORRECTED-R194-Q1-R199-FLAGGED-NOGO-FOUR-LEGS-INDEPENDENTLY-RECOMPUTED-THETA2-EQ-MINUS-I-MACHINE-ZERO-PAULI-3-3-ANTIUNITARY-6-6-CP2-CHI-3-C1-3H-H20-0-NOT-HYPERKAHLER-FS-HOMOGENEOUS-RESIDUAL-EXACT-0-M5-SCALE-DEGENERATE-ZERO-BITS-ON-ELL-RG-REFERENCE-INVARIANT-9-9-SUSY-INVENTORY-0-OF-101-FILES-TRUNCATED-HIGGS-1-NE-2-PATH2-CONFIRMED-CLOSED-NEGATIVE-PATHS-1-3-MERGED-SINGLE-MISSING-OBJECT-SUPPLY-0-CANDIDATE-SCAN-17296-COMBOS-0-HIT-ON-INDEPENDENT-BASIS-SSTAR-FLOAT64-VS-DECIMAL60-LAYER-INFO"
)

VERD_LINE = (
    "│   ├── 判定_" + SRC_STEM + ".md  # 新增（**r203 · 2026-10-25**）：**S13 兄弟链跨轮互印判定册**"
    "（十节：一 编号与定位（★第五次同型竞态·和平共处无改号）/ 二 判词 / 三 跨轮互印 23 行全表 / 四 精度层三差（≤1ulp）/ "
    "五 x_GUT 混用 lineage 检出 / 六 no-go 四腿独立复算（Θ²=−I 机器零 · Pauli 3/3 · 反幺正 6/6 · CP² χ=3 非 hyperkähler · "
    "FS 齐次 32 等式 · M5 ℓ 零比特 · RG 9/9 · SUSY inventory 0/101 · Higgs 1≠2）/ 七 r188 重审条件核验 / 八 候选扫描 "
    "17,296+39,710 / 九 控制组 31/31 与守卫 12/12 / 十 未闭合项与红线）。条目 **15 = FAIL 4 / PASS 7 / INFO 3 / BOUNDARY 1**。"
    "**控制组 31/31**（靶协议 RK4 逐位复现 gap_sm=4.060449943317877 / gap_ms=0.7600419008581873 / M_sm=236961529934301.12 / "
    "M_ms=1.419626474794894e16 / α_GUT⁻¹(min)=25.626831813987337 · 闭式 gap SM 13.140577% @1.0237410014e13 / MSSM 0.311719% "
    "@1.9904728657e16 · s* 闭式 60 位残差 1.197e-31 · L13−L23=−1e-59 · SM β 内容重算精确 · 截断纪律正对照 7/7 · "
    "互印 23/23）。**守卫 12/12 全机读驱动**：G1 FAIL 带证据 · G2 verdict 计数驱动 · G3 分层短语双命中 · G4 靶文件全可读 · "
    "G5 文本证据 17/17 逐字命中 · G6 ast 自审 ok 常量写死 0 · G7 条目分布机读断言 {PASS:7,FAIL:4,INFO:3,BOUNDARY:1} · "
    "G8 容差按靶有效位（M*/v 行 r192 存 6 位小数 ⇒ 该行 1e-7）· G9 ∅ 由集合运算 · G10 三路径必要条件缺失机读 · "
    "G11 互印行模式（list/zeroish/数值）· G12 截断前后对照 1→0。"
)

DATA_LINE = (
    "│   ├── " + SRC_STEM + ".json / .md / _report.txt  # 新增（**r203 · 2026-10-25**）S13 兄弟链互印机检产物"
    "（**15 条判定** + **12 条守卫** + 控制组 31 项 + constants + snips；key_numbers：**互印 23/23（14 peer JSON）**、"
    "**s* 精度层 16 位一致（相对差 1.589e-17）、M_GUT π 层 2.511e-15、M* 渲染层 1.437e-18**、"
    "**x_GUT 混用：x=5.2547892800 vs M_GUT=2.121000E+16 ⇒ M(x)=19904728656526579.008 相对差 0.06154**、"
    "**x_GUT 规范值 5.264898105739327113372914899632、x₁₂=5.25478928 精确（终止小数）**、"
    "**M_GUT 16 位 π=2.12100038435839992e16 / 60 位 π=2.12100038435840525e16、α_GUT⁻¹=24.2764585241730279898**、"
    "**s*=0.230943405280905868720056895550（靶 30 位残差 1.197e-31）**、**v=255.26242445425643、M*=3675.242923463758 GeV、"
    "M*/v=14.3979002445084499791、x*=0.58830917877551020408、sin²θ(v)=0.23638579274415291702、ℓ_EW=7.7303575e-19 m**、"
    "**RK4：gap_sm=4.060449943317877@M_sm=2.3696152993430112e14 / gap_ms=0.7600419008581873@M_ms=1.419626474794894e16 / "
    "α_GUT⁻¹(min)=25.626831813987337**、**闭式 gap SM 13.140577%@1.0237410013833014e13 / MSSM 0.311719%@1.9904728657e16**、"
    "**Θ²=−I 矩阵+算子残差 0、Pauli 3/3、反幺正 6/6、CP² (1,0,1,0,1)/χ=3/c₁=3H/h²⁰=0、FS 32 等式残差 0、"
    "M5 残差 0、RG 9/9（4.71e-60）**、**SUSY 七类 0（101 文件截断；原始 1 处全在 ch25 附节；截断正对照 7/7）**、"
    "**Higgs 4 实模式/1 重态≠2**、**候选扫描 17,296 组合 0 命中（正对照 5/5）+ r192 记录 39,710 0 命中**；"
    "verdict=R203-CROSS-ROUND-MUTUAL-VERIFICATION-23-ROWS-23-CONSISTENT-1-XGUT-LINEAGE-CONFLICT-SELF-CORRECTED-R194-Q1-R199-FLAGGED-NOGO-FOUR-LEGS-INDEPENDENTLY-RECOMPUTED-THETA2-EQ-MINUS-I-MACHINE-ZERO-PAULI-3-3-ANTIUNITARY-6-6-CP2-CHI-3-C1-3H-H20-0-NOT-HYPERKAHLER-FS-HOMOGENEOUS-RESIDUAL-EXACT-0-M5-SCALE-DEGENERATE-ZERO-BITS-ON-ELL-RG-REFERENCE-INVARIANT-9-9-SUSY-INVENTORY-0-OF-101-FILES-TRUNCATED-HIGGS-1-NE-2-PATH2-CONFIRMED-CLOSED-NEGATIVE-PATHS-1-3-MERGED-SINGLE-MISSING-OBJECT-SUPPLY-0-CANDIDATE-SCAN-17296-COMBOS-0-HIT-ON-INDEPENDENT-BASIS-SSTAR-FLOAT64-VS-DECIMAL60-LAYER-INFO"
)

ARB_LINE = (
    "> **再更新（2026-10-25 22:57 · 同线续）**：**r203 已被本线占用（和平共处无改号）** —— 本线 S13 兄弟链跨轮互印卷"
    "起草前 22:00:48 实测 r203/r204 三树全空，引擎 22:50:18 落盘；并行会话 22:46:54 落 **r204**"
    "（《质量定义方程_常数k多值冲突与公理自毁继承》，其登记章明文「r203 被并行《S13兄弟链跨轮互印》占用；r204 三树全空为"
    "唯一首空号」）⇒ **双方无冲突、本线无需改号**，r203 实测本线占用、rc=0：条目 15 = FAIL 4/PASS 7/INFO 3/BOUNDARY 1，"
    "控制组 31/31、守卫 12/12、跨轮互印 23/23（14 件 peer JSON sha256 只读证明）。**★仲裁现值：下轮实际从 r205 起**"
    "（纪律延续：落盘前必须复查磁盘时间戳而非仅 grep；并行线 r189–r204 十余卷只登增量登记章、不入三树，其目录树刷新仍随 "
    "catalog 重生成统一处理）。"
)

CHAPTER = """

---

### r203 · 2026-10-25 · S13 兄弟链跨轮互印与 no-go 独立复核（r188×r189×r192 口径对拍 + Θ/CP² 四腿复算）

- **命题**：r199 跨轮审计只覆盖 r190–r197（未含本线 r188/r189）；r192 no-go 四腿（Θ²=−I / Pauli 共轭 / CP² χ=3 / FS 齐次）未经独立复算 ⇒ 本卷补三件事：①**跨轮互印**（14 件 peer JSON × 23 项共享量）；②**no-go 四腿独立复算**（全 Fraction/CF 精确代数）；③**r188 重审条件核验**（其 12 FAIL 在新证据下是否仍成立）。**不重判** OPEN 定性、不新增框架供给。
- **产物**：`源码/TUFT-r203_S13兄弟链跨轮互印与no-go独立复核_r188xr189xr192口径对拍与ThetaCP2四腿复算_精算_2026-10-25.py`
  （+ ASCII runner `源码/_run_r203.py` + driver `openuft/_drive_r203.py`）+ `数据/同名.{json,md,_report.txt}` +
  `判定/判定_TUFT-r203_同名.md`。复现 `python -X utf8 openuft/_drive_r203.py`，**退出码 0**；**控制组 31/31、守卫 12/12、文本证据 17/17**。
- **判词**：`R203-CROSS-ROUND-MUTUAL-VERIFICATION-23-ROWS-23-CONSISTENT-1-XGUT-LINEAGE-CONFLICT-SELF-CORRECTED-R194-Q1-R199-FLAGGED-NOGO-FOUR-LEGS-INDEPENDENTLY-RECOMPUTED-THETA2-EQ-MINUS-I-MACHINE-ZERO-PAULI-3-3-ANTIUNITARY-6-6-CP2-CHI-3-C1-3H-H20-0-NOT-HYPERKAHLER-FS-HOMOGENEOUS-RESIDUAL-EXACT-0-M5-SCALE-DEGENERATE-ZERO-BITS-ON-ELL-RG-REFERENCE-INVARIANT-9-9-SUSY-INVENTORY-0-OF-101-FILES-TRUNCATED-HIGGS-1-NE-2-PATH2-CONFIRMED-CLOSED-NEGATIVE-PATHS-1-3-MERGED-SINGLE-MISSING-OBJECT-SUPPLY-0-CANDIDATE-SCAN-17296-COMBOS-0-HIT-ON-INDEPENDENT-BASIS-SSTAR-FLOAT64-VS-DECIMAL60-LAYER-INFO`
- **条目 15 = FAIL 4 / PASS 7 / INFO 3 / BOUNDARY 1**；**控制组 31/31**；**守卫 12/12 全机读驱动**。
- **核心结论**：
  1. **跨轮互印 23/23 行全一致**（v、M*、M*/v、x*、x₁₂、M(x₁₂)、x_GUT、M_GUT、α_GUT⁻¹、s*、gap_sm/gap_ms RK4、M_sm/M_ms RK4、SM/MSSM 闭式 gap%、SM 交点 M、β×2、Higgs、Θ²、CP² χ、ℓ_EW）：机读 peer JSON + 独立重算对拍双路成立；14 件 peer JSON sha256 前后一致证只读。
  2. **s* 精度层（非口径冲突）**：r189 float64 `0.230943405280905872389851651860` vs 本卷 Decimal(60) 前 **16 位有效数字一致**（第 17 位起分歧，相对差 **1.589e-17** = float eps 量级）；M_GUT 的 π 位层差 **2.511e-15**（r194/r195/r199 用 60 位 π，r188/r192 用 16 位 `str(math.pi)`）；M* 渲染层差 1.437e-18 ⇒ 全部 ≤1ulp。
  3. **x_GUT 混用 lineage 检出（链级事实）**：r192 同轮 `x_GUT=5.2547892800`（α₁=α₂ 交点）配 `M_GUT=2.121000E+16`（α₁=α₃/s* 统一点），重算 M(x)=19904728656526579.008 ⇒ 相对差 **0.06154（6.15%）**；r194 Q1 自纠（规范值 5.2648981057393271）+ r199 标注，**混用已自纠正、链完整**。口径钉死：x_GUT 规范值 = L13（三线共点）= 5.264898105739327113372914899632…；x₁₂ = (A1₀−A2₀)/(b1−b2) = 5.25478928 精确（终止小数）。
  4. **no-go 四腿独立复算（全 Fraction/复分数 CF 精确）**：Θ²=−I=+I（矩阵层 + 200 随机复旋量算子层残差 **0**；靶约定 [[0,−1],[1,0]]，r188 曾用反号、结论不变）· εσᵢε⁻¹=−σᵢᵀ **3/3** · 反幺正 Θ(iψ)=−iΘψ + Θ²=−I **6/6** ⇒ Majorana 实条件 · CP² Betti (1,0,1,0,1)/χ=3/c₁=3H/h²⁰=0 ⇒ **非 hyperkähler**（外部标准数学标注）· FS Kähler 类齐次 **残差精确 0**（两点×三 λ 共 **32 项等式** + 差商恒等式）· M5 族 g_ℓ(ℓ²/r)=g_ℓ(r) 对任意 ℓ 恒等（残差 **0**）⇒ ℓ 信息量 **0 bit** · RG 参考尺度不变性 **9/9**（残差 4.71e-60）· **101 文件截断后**七类 SUSY inventory **0 命中**（截断前原始 1 处全在 ch25 附节内——截断纪律机读见证）· Higgs 谱 {0,0,0,8κv²} ⇒ 4 实模式 = 1 重态 ≠ MSSM 2。
  5. **r188 重审条件核验**：路径 1/3（合并后单一缺失对象：尺度设定/维度嬔变原理）仍 OPEN；路径 2 CLOSED-NEGATIVE 维持（排除性结论，不增加框架自有供给，r192 红线沿用）。
  6. **候选扫描**：自有基准 23 基元×2（倒数）三因子多项式 = **17,296 组合 0 命中**（tol 1e-9）+ 注入正对照 **5/5**；r192 记录机读（N=39,710 ≥10⁴、0 命中、正对照 5/5）；60 基元池构成未在 JSON 登记 ⇒ 39,710 **未重造**（BOUNDARY/INFO）。
- **截断纪律**：`APPENDIX_PAT = re.compile(r"\\n---\\n+\\s*## 【r1\\d\\d")`，扫描前截断——ch25 唯一「超伴子」命中在 L86（r192 勘误附节，L81 起）；截断前后对照 1→0 为 G12 守卫。
- **分层声明（条目不可跨册相加）**：本卷不重判 r188/r189/r192 的数值与口径；只做互印、独立复算与重审条件核验；**不可与 r142–r202 相加**。
- **取号（第五次同型竞态·和平共处无改号）**：落盘前复查磁盘时间戳（22:00:48），r203/r204 三树全空；引擎 22:50:18 落盘。并行会话 22:46:54 落 r204，其登记章明文确认本线占 r203 ⇒ **双方无冲突、无需改号**；**下轮从 r205 起**（落盘前仍须复查时间戳）。
- **自抓 5 处（已修，重跑 rc=0）**：①CF 复分数缺 `__truediv__`（首跑 TypeError）⇒ 补复数除法；②verdict 未绑定（二跑 UnboundLocalError）⇒ verdict 令牌 join 块移至守卫段之前；③C29 互印 22/23——Mstar_over_v 行 r192 存 6 位小数「14.397900」相对差 1.7e-8 略超 1e-8 ⇒ 该行 tol 放宽至 1e-7（仍远严于渲染层）⇒ 23/23；④G11 条目数硬编码错（实际 15 条，我漏数 B3）⇒ 改全分布机读断言 `{PASS:7,FAIL:4,INFO:3,BOUNDARY:1}`；⑤特殊行 tol=None 会崩（higgs_doublets/cp2_chi 走数值分支 `rel <= None` TypeError）⇒ 两行 tol 设 1e-12、beta 两行走 list 模式、theta_sq 走 zeroish 模式；⑥候选扫描正对照不注入（原 pos_cand 重扫同基元）⇒ `extra_prims=[tv]` 注入靶值本身 ⇒ 5/5；⑦ast 自审误伤 docstring（模块 docstring >200 字符被判巨串）⇒ docstring 节点豁免；⑧A2 文案位数不一致（写「17 位」实测 16 位）⇒ 修正为「16 位有效数字（第 17 位起分歧）」。
- **治理**：未跑 refresh_catalog.py（并发活跃待批准）；未改 `verify.py`；未做 git；跨轮审计只读；未触碰并行会话任何字节。
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

    i_src = find_one(lambda ln: ln.startswith("│   ├── TUFT-r188_S13残余路径一二三第一性审计") and ".py" in ln and "新增" in ln, "r188 src line")
    i_ver = find_one(lambda ln: ln.startswith("│   ├── 判定_TUFT-r188_S13残余路径一二三第一性审计"), "r188 verdict line")
    i_dat = find_one(lambda ln: ln.startswith("│   ├── TUFT-r188_S13残余路径一二三第一性审计") and ".json" in ln, "r188 data line")
    i_arb = find_one(lambda ln: ln.startswith("> **再更新（2026-10-25 10:36 · 同线续）**"), "r188 arb line")
    if any(ln.startswith("### r203 ") for ln in lines):
        print("FATAL: r203 chapter already present")
        sys.exit(4)
    if any(SRC_STEM in ln for ln in lines):
        print("FATAL: r203 stem already registered")
        sys.exit(5)

    # insert from bottom to top to keep indices valid
    lines.insert(len(lines), CHAPTER)  # append at tail (CHAPTER starts with \n\n---)
    lines.insert(i_arb + 1, ARB_LINE)
    lines.insert(i_dat + 1, DATA_LINE)
    lines.insert(i_ver + 1, VERD_LINE)
    lines.insert(i_src + 1, SRC_LINE)

    with io.open(README, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("OK: 5 insertions done (src/verdict/data/arb/chapter)")


if __name__ == "__main__":
    main()
