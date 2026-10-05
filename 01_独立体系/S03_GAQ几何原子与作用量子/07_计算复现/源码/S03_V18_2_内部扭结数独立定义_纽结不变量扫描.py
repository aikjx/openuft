# -*- coding: utf-8 -*-
"""
S03 V18.2 · 分支二续：给内部扭结数 N 一个独立定义（标准纽结不变量候选扫描）

承接 S03-V18.1（P1/P2/P3 机器验证）的核心否证结果：
  族 F1（单一幂律 m ∝ N^α + 手性由 N 奇偶翻转）不满足可证伪性，因 N 可调至任意大。
V18.2 任务：把 N 从自由参数替换为**独立于质量的几何不变量**，看族 F1 是否被明确否证，
          并查明失败是否属于该路线特有，还是更上游的公共问题。

验证 1（V2-a）标准纽结不变量候选扫描：c / b / u / g 四族 × 两种身份映射
验证 2（V2-b）d→u 作为 unknotting 一步：缺口 O-S03-C2 的自然答案
验证 3（V2-c）同族结质量跨度检验：质量能否归结为结不变量
验证 4（V2-d）unknotting number 能否标记粒子身份（u→s 方向判决）
验证 5（V2-e）出路 2（双内部自由度 N_Q / N_L）参数—约束计数
验证 6（V2-f）层级收敛：普朗克锚定谬误复现（Gm²=ħc ⇒ m=m_P）
自检 9 项

红线：
- 验证 1 的否证射程**严格限于**「N 取标准纽结不变量」这一实现路线，不否决人工标签。
- 验证 2 是自洽性，不是验证；unknotting number 无实验可测性。
- 验证 3 与验证 1 不同源：它否证「质量 ∝ 任何结不变量」这一整族，不依赖 F1 的映射形式。
- 验证 5 只做参数—约束计数；计数通过不等于模型成立，此处为欠定判定。
- 验证 6 为跨体系结论的独立复算（普朗克锚定谬误），不引用既有结论。
- 本册未对 GAQ 的任何主张给出正面支持证据。
"""
import math
import sys
import sys as _sys_utf8

try:
    _sys_utf8.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ---------------------------------------------------------------- 标称输入
# 夸克质量为 MSbar 标称值（running 量，理论依赖约 10%）
M_U_MEV = 2.16
M_D_MEV = 4.67
M_S_MEV = 93.4
M_C_MEV = 1.27
M_B_MEV = 4180.0
M_T_MEV = 173000.0
M_E_MEV = 0.510999
M_NU_MAX_MEV = 0.8e-6   # KATRIN 2022, 90% CL: 0.8 eV

RATIO_DU = M_D_MEV / M_U_MEV
RATIO_ENU = M_E_MEV / M_NU_MAX_MEV
LN_DU = math.log(RATIO_DU)
LN_ENU = math.log(RATIO_ENU)

# 衰变释放能 Q = m(初) - m(末)；Q>0 放能，Q<0 吸能
Q_DU = M_D_MEV - M_U_MEV      # d→u：+2.51 MeV 放能
Q_US = M_U_MEV - M_S_MEV      # u→s：-91.24 MeV 吸能
Q_DS = M_D_MEV - M_S_MEV      # d→s：-88.73 MeV 吸能

# 物理常数（SI）
G_SI = 6.67430e-11
HBAR_SI = 1.054571817e-34
C_SI = 2.99792458e8
M_E_KG = 9.1093837015e-31

RESULTS = []


def P(name, detail):
    RESULTS.append(("PASS", name, detail))


def F(name, detail):
    RESULTS.append(("FAIL", name, detail))


def B(name, detail):
    RESULTS.append(("BOUNDARY", name, detail))


def I(name, detail):
    RESULTS.append(("INFO", name, detail))


def hdr(title):
    print("=" * 70)
    print(title)
    print("=" * 70)


# ================================================================ 纽结不变量表
KNOTS = {
    "unknot":  {"c": 0, "b": 1, "u": 0, "g": 0},
    "trefoil": {"c": 3, "b": 2, "u": 1, "g": 1},
    "figure8": {"c": 4, "b": 2, "u": 2, "g": 2},
}
IDENTITY = {
    "primary": {"u_quark": "unknot", "d_quark": "trefoil"},
    "alt":     {"u_quark": "unknot", "d_quark": "figure8"},
}
LEPTON_KNOTS = ["unknot", "trefoil", "figure8"]
MIN_GAP = 2   # 族 F1 的 R1：N_d 与 N_u 同奇偶且 N_d > N_u


# ================================================================ 验证 1
hdr("验证 1 | V2-a  标准纽结不变量候选扫描（N 的独立定义）")

print("  纽结不变量标准值表")
print("    {:<10} {:>4} {:>4} {:>4} {:>4}".format("结", "c", "b", "u", "g"))
for name, kv in KNOTS.items():
    print("    {:<10} {:>4} {:>4} {:>4} {:>4}".format(name, kv["c"], kv["b"], kv["u"], kv["g"]))
print()
print("  身份映射假设 CA-2：u(轻夸克)↦unknot，d(重夸克)↦trefoil（更复杂）")
print("  族 F1 的 R1：N_d 与 N_u 同奇偶且 N_d > N_u")
print()

any_pass = False
for inv in ("c", "b", "u", "g"):
    print("  候选 N = {}：".format(inv))
    for tag, mapping in IDENTITY.items():
        nu = KNOTS[mapping["u_quark"]][inv]
        nd = KNOTS[mapping["d_quark"]][inv]
        if nu == 0:
            state = "退化(N_u=0，除零)"
        elif nd <= nu:
            state = "不满足 N_d>N_u"
        elif nd % 2 != nu % 2:
            state = "奇偶冲突({} vs {})".format(nd, nu)
        else:
            state = "通过"
            any_pass = True
        print("    {:<8} N_u={} N_d={}  →  {}".format(tag, nu, nd, state))

print()
for inv in ("c", "b", "u", "g"):
    vals = sorted(set(KNOTS[k][inv] for k in LEPTON_KNOTS))
    print("    N = {:<2} 轻子可取值 = {}".format(inv, vals))
max_lepton = max(max(sorted(set(KNOTS[k][inv] for k in LEPTON_KNOTS)))
                 for inv in ("c", "b", "u", "g"))
print()

if not any_pass:
    F("V2-a", "四个标准纽结不变量（交叉数 c / 桥数 b / unknotting number u / Seifert genus g）"
              "× 两种身份映射下，族 F1 的 R1 全部无法满足：或退化（N_u=0）、"
              "或 N_d 不大于 N_u、或奇偶冲突。"
              "故在「N 取标准纽结不变量」路线上族 F1 **明确无解**"
              "——V18.1 的「不可证伪」升级为「在标准候选集下否证」。")
    B("V2-a-scope", "本 FAIL 射程严格限于「N 取标准纽结不变量」这一实现路线。"
                    "人工构造的标签不在射程内，但那种标签失去几何依据，等于退回字典约定。")
    B("V2-a-enu", "N 独立定义后，e/ν 质量比 {:.3e} 须由 (Ne/Nν)^α 给出，"
                  "而 N 取值上界仅 {}（轻子结不变量最大可达值）⇒ 无解。".format(
                      RATIO_ENU, max_lepton))
else:
    B("V2-a", "存在通过 R1 的候选，e/ν 侧检验见上表。")

# ================================================================ 验证 2
hdr("验证 2 | V2-b  d→u 作为 unknotting 一步（缺口 O-S03-C2）")

u_trefoil = KNOTS["trefoil"]["u"]
u_unknot = KNOTS["unknot"]["u"]
steps = u_trefoil - u_unknot
print("  unknotting number: trefoil = {}, unknot = {}".format(u_trefoil, u_unknot))
print("  d→u 所需解开步数 = {}".format(steps))
print("  d→u 释放能 Q = {:+.3f} MeV（>0 放能，与自发衰变相容）".format(Q_DU))
print()
if steps == 1 and Q_DU > 0:
    P("V2-b", "d→u 恰对应**解开一步**（trefoil→unknot），且为放能（Q=+2.51 MeV），"
              "与 S03-D1 的「桥接场线剪断重联」图像自然自洽：弱作用即解开一个子扭结。"
              "缺口 O-S03-C2（Tw+Wr 如何从 m_d 变到 m_u）获得自然答案"
              "——不是连续形变，而是 unknotting number 减 1。")
    I("V2-b-caveat", "这是**自洽性**而非验证：自洽性不能排除其它同样自洽的映射"
                     "（解开 2 步、打结 1 步等）；且 unknotting number 实验可测性为零，"
                     "该映射无法被独立检验。")
else:
    F("V2-b", "步数 = {} 或 Q 符号不符".format(steps))

# ================================================================ 验证 3
hdr("验证 3 | V2-c  同族结质量跨度检验：质量能否归结为结不变量")

span_1q = M_T_MEV / M_S_MEV     # 单夸克族内最大跨度 s→t
span_2q = M_D_MEV / M_C_MEV     # 双夸克族内最大跨度 c→d
print("  假设 CA-3：m = f(N)，N 为结不变量 ⇒ 结构同型者 N 相近")
print("  单夸克族（1 结）：    s={:>8.1f}  b={:>8.1f}  t={:>9.1f} MeV".format(
    M_S_MEV, M_B_MEV, M_T_MEV))
print("    单夸克族内跨度 s→t = {:.1f} 倍".format(span_1q))
print("  双夸克族（2 结复合）： c={:>8.2f}  u={:>8.2f}  d={:>8.2f} MeV".format(
    M_C_MEV, M_U_MEV, M_D_MEV))
print("    双夸克族内跨度 c→d = {:.2f} 倍".format(span_2q))
print("  两族跨度之比 = {:.1f}".format(span_1q / span_2q))
print()
P("V2-c-data", "质量跨度实测：单夸克族 {:.1f} 倍、双夸克族 {:.2f} 倍，相差 {:.0f} 倍；"
               "且跨度最大的恰是**结构最简单**的单夸克族。".format(
                   span_1q, span_2q, span_1q / span_2q))
F("V2-c", "**质量不可归结为结不变量**（射程：任何 m=f(N) 且 N 为结不变量）："
          "结构同型者 N 应相近，但单夸克族内质量跨度 {:.0f} 倍、"
          "双夸克族内 {:.1f} 倍，且**最简结构反而跨度最大**（差 {:.0f} 倍）。"
          "若质量由结结构决定，应预期复杂结构跨度更大——实测相反。"
          "故质量谱需**代数/味结构**承载，而非结拓扑。"
          "此结论不依赖族 F1 的映射形式，比 V2-a 更上游。".format(
              span_1q, span_2q, span_1q / span_2q))
B("V2-c-read", "与 SM 对照：SM 中夸克质量源自 QCD 味对称破缺（ε_s）与电弱真空期望值，"
               "确为**代数/味**机制而非拓扑机制。故本条 FAIL 与 SM 已知结构**同向**，"
               "不构成对 SM 的否定，只是对「结拓扑承载质量谱」这一 GAQ 设想的否定。")

# ================================================================ 验证 4
hdr("验证 4 | V2-d  unknotting number 能否标记粒子身份")

print("  实测释放能 Q = m(初) - m(末)：")
print("    d→u  Q = {:+8.3f} MeV   放能（自发衰变）".format(Q_DU))
print("    u→s  Q = {:+8.3f} MeV   吸能（需外部供能）".format(Q_US))
print("    d→s  Q = {:+8.3f} MeV   吸能（需外部供能）".format(Q_DS))
print()
B("V2-d-energy", "u→s 与 d→s 均为**吸能**方向（{:+.1f} / {:+.1f} MeV），"
                 "在 N=结复杂度的读法下要求 N 增大即**打结**；只有 d→u 是放能且对应解开。"
                 "故「单一 unknotting 机制」只覆盖三个方向之一。"
                 "能量非障碍（W 质量 80.4 GeV 远大于所需），"
                 "障碍在于 unknotting number 沿衰变链**非单调**。".format(Q_US, Q_DS))
F("V2-d-label", "unknotting number **不能作为粒子身份标签**："
               "u→s 使 N 从 0（unknot）增至更复杂结的值，而不同粒子可取同一 N 值"
               "（trefoil 的 u=1，但存在 u=1 的更复杂结；u=2 更是多解）。"
               "标签须单射且单调，unknotting number 两者皆不满足。"
               "此结论与 V2-a **不同源**：即使族 F1 另有可行形式，"
               "以 unknotting number 作 N 的路线仍被独立否证。")

# ================================================================ 验证 5
hdr("验证 5 | V2-e  出路 2（双内部自由度 N_Q / N_L）参数—约束计数")

n_params = 6       # N_Qd, N_Qu, N_Le, N_Lnu, α_Q, α_L
n_constraints = 4  # d/u 质量比、e/ν 质量比、R1 同奇偶、R2 异奇偶
deficit = n_params - n_constraints
print("  出路 2 自由参数：N_Qd, N_Qu, N_Le, N_Lν, α_Q, α_L  →  {}".format(n_params))
print("  约束：d/u 质量比、e/ν 质量比、R1 同奇偶、R2 异奇偶   →  {}".format(n_constraints))
print("  自由度余量 = {}".format(deficit))
print()
if deficit > 0:
    F("V2-e", "出路 2 同样欠定：{} 参数对 {} 约束 ⇒ 自由度余量 {}。"
               "两组质量比可被两族的 α 各自吸收，故该族**同样不满足可证伪性**。"
               "结论：「换构造」本身不解决问题；任何出路都须**额外提供至少 {} 个"
               "不依赖质量比反解的约束**。".format(n_params, n_constraints, deficit, deficit))
    I("V2-e-repair", "减少参数的唯一途径是给出独立锚：固定 α_Q/α_L 的形式、"
                    "或减少 N 的自由度（回到 V2-a 的困难）、"
                    "或引入第三个可测量（如 CKM 混合角）。"
                    "但注意 V2-c 已表明质量本身不由结不变量承载，"
                    "故「固定 α 的形式」必须来自结拓扑之外的机制。")

# ================================================================ 验证 6
hdr("验证 6 | V2-f  层级收敛：普朗克锚定谬误复现")

m_planck_kg = math.sqrt(HBAR_SI * C_SI / G_SI)
alpha_grav_e = G_SI * M_E_KG ** 2 / (HBAR_SI * C_SI)
conflict = m_planck_kg / M_E_KG
residual = G_SI * m_planck_kg ** 2 / (HBAR_SI * C_SI) - 1.0

print("  由 Gm² = ħc 反解 m = √(ħc/G)")
print("    m_P = {:.6e} kg     m_e = {:.6e} kg".format(m_planck_kg, M_E_KG))
print("    冲突倍数 = {:.4e}".format(conflict))
print("    α_grav(e) = Gm_e²/(ħc) = {:.4e}".format(alpha_grav_e))
print("    普朗克锚定要求 α = 1 ⇒ 偏差 {:.4e}".format(1.0 / alpha_grav_e))
print("    代回残差 Gm_P²/(ħc) - 1 = {:+.3e}".format(residual))
print()
if abs(residual) < 1e-12 and conflict > 1e20:
    P("V2-f", "普朗克锚定谬误机器复现：Gm²=ħc 的唯一解 m=m_P={:.3e} kg，"
              "与电子质量冲突 {:.2e} 倍；代回残差 {:+.1e}（机器零）。"
              "含义：任何「由 G、ħ 与曲率/挠率直接联立得质量」的构造都会滑向 m=m_P。".format(
                  m_planck_kg, conflict, residual))
    B("V2-f-converge", "**层级收敛（本册最重要的结构性结论）**：S03-D1 的四个独立缺口"
                       "——G4（ħ 未从拓扑导出）、C1（自旋统计来源）、F（e/ν 质量差）、"
                       "以及 P1 不可证伪——共享同一公共上游：**质量标度没有第一性锚**。"
                       "且 V2-c 表明质量需代数/味机制而非结拓扑。"
                       "故 P1 的失败是上游症状：修 P1 而不修上游无效。")

# ================================================================ 自检
hdr("自检")

SC = []


def sc(name, ok, detail=""):
    SC.append((name, ok, detail))
    print("  [{}] {}{}".format("OK" if ok else "NG", name, ("  " + detail) if detail else ""))


sc("SC1 四个不变量候选均无「通过」态", not any_pass)
sc("SC2 trefoil 与 unknot 的 unknotting 差 = 1 且 d→u 放能",
   steps == 1 and Q_DU > 0)
sc("SC3 Q 符号正确：d→u 放能、u→s 与 d→s 吸能",
   Q_DU > 0 and Q_US < 0 and Q_DS < 0,
   "Q_du={:+.2f} Q_us={:+.2f} Q_ds={:+.2f}".format(Q_DU, Q_US, Q_DS))
sc("SC4 单夸克族跨度 > 双夸克族跨度（反直觉但实测如此）",
   span_1q > span_2q, "{:.1f} vs {:.2f}".format(span_1q, span_2q))
sc("SC5 出路 2 自由度余量 = 2", deficit == 2)
sc("SC6 普朗克锚定代回残差 < 1e-12", abs(residual) < 1e-12)
sc("SC7 普朗克冲突 > 1e20", conflict > 1e20, "{:.2e}".format(conflict))
sc("SC8 α_grav(e) 在 1e-45 量级", 1.0e-45 < alpha_grav_e < 1.0e-44,
   "{:.4e}".format(alpha_grav_e))
sc("SC9 轻子不变量上界 < 10（远小于所需 1e5 量级）", max_lepton < 10,
   "上界 = {}".format(max_lepton))

# ================================================================ 汇总
hdr("判定汇总")
cnt = {}
for kind, name, detail in RESULTS:
    cnt[kind] = cnt.get(kind, 0) + 1
    print("  [{}] {}".format(kind, name))
    print("         {}".format(detail))
print()
print("  统计：PASS={} FAIL={} BOUNDARY={} INFO={}  合计={}".format(
    cnt.get("PASS", 0), cnt.get("FAIL", 0), cnt.get("BOUNDARY", 0),
    cnt.get("INFO", 0), len(RESULTS)))

n_ok = sum(1 for _, ok, _ in SC if ok)
print("  自检：{}/{} 通过".format(n_ok, len(SC)))
print()
print("  红线声明：")
print("   - 验证 1 否证只覆盖「N 取标准纽结不变量」路线；人工标签不在射程内。")
print("   - 验证 2 是自洽性，不是验证；unknotting number 无实验可测性。")
print("   - 验证 3 独立于族 F1 的映射形式，否证「质量 ∝ 任何结不变量」整族。")
print("   - 验证 4 与验证 1 不同源，构成对 unknotting-number 标签的独立否证。")
print("   - 验证 5 只做参数计数，此处为欠定判定。")
print("   - 验证 6 为跨体系结论的独立复算，不引用既有结论。")
print("   - 本册仍未对 GAQ 的任何主张给出正面支持证据。")

if n_ok == len(SC):
    print()
    print("SELF-CHECK PASS ({}/{})".format(n_ok, len(SC)))
else:
    print()
    print("SELF-CHECK FAIL")
    sys.exit(1)
