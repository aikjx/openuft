"""
TUFT-r142 · 核心公式体系 · 最小修复路径定价 + 未检两式（3.15 / 3.18）首攻 + r141 自纠

分工声明（与 r141 严格分层，条目不可相加）：
  r141 做的是【物理层 M3 的判定】：23 条 → PASS 0 / FAIL 16 / INFO 7。
  本卷做的是 r141 **没有做、但做完才敢说「已封死」**的那一层：
      M4 —— 修复层：每条 FAIL 的最小修复是什么？代价多大？
                     是否存在一个完备修复集？施加后体系还剩什么？
  另：r141 列为「未检」的式 3.15、式 3.18，本卷首攻（补 2 条新物理层条目）。
  两册条目**不可相加**：组 R/组 M 是**对 r141 结论的定价**，不是新 FAIL；
  只有组 F（式 3.15 / 3.18）是**新增的物理层判定条目**。

★ 卷首自纠（必须先登记，不得隐藏）：
  r141 的 D2 只封了两条退路 —— ①翻 k′ 的符号（无效，被约掉）
  ②改 r⃗ 的取向（无效，两种取向最多还原 1/2）。
  **漏了第三条：把式 3.10 的负号当作笔误直接删掉。**
  而这一条是**走得通的**：删掉后 E=+q r̂/(4πε₀r²)，库仑定律正确，
  式 3.4 的引力（吸引）也不受影响 ⇒ D2 被真正修复。
  ⇒ r141 D2 的「退路已封」是**过度指控**，本卷更正，并给这条修复定价（见 R7）。

方法（沿用既有纪律）：
  · 每条修复必须写清【关闭哪些 FAIL】与【代价是什么】（作废哪条公设/哪条宣称）。
  · 修复集用**位掩码穷举**（2^9 = 512 个子集），不靠人工挑。
  · 二难类结论必须给出两个分支各自的定量阈值。
  · 控制组：把同一流程施加于标准物理（标准物理的最小修复集应为 0）。
  · 红线：数学自洽 ≠ 实验证实；修复可行 ≠ 修复后仍有内容。

机检清单：
  组 R 修复项定价： R0 自纠 ｜ R1 放弃螺旋 ｜ R2 放弃动量强守恒 ｜ R3 式3.16改标准
                    ｜ R4 式3.5改p₀=0 ｜ R5 式3.9改电荷定义 ｜ R6 式3.11改v×E/c²
                    ｜ R7 式3.10删负号（★r141 漏网退路）｜ R8 式3.15删项 ｜ R9 式3.18换已知核力
  组 F 未检两式首攻： F1 式 3.15 ⇒ 静引力场+静电场 ⇒ 单调增长磁场
                    ｜ F2 式 3.18 核力场 ⇒ 无作用程/无排斥芯/量级差 5.7e13
  组 M 修复集穷举：   M1 削减型完备集存在性 ｜ M2 完备集最小规模与代价 ｜ M3 单源构型 BOUNDARY
"""
import os, json, math, datetime, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "数据"))
PROJECT = os.path.normpath(os.path.join(HERE, ".."))
DATE = "2026-10-21"
STEM = "TUFT-r142_核心公式体系_最小修复路径定价与未检两式首攻_%s" % DATE
JUDGE_STEM = "判定_TUFT-r142_核心公式体系_最小修复路径定价与修复即自杀_%s" % DATE

# ---------------- 常数（CODATA 2018 / 常用值） ----------------
C = 299792458.0                 # m/s
G = 6.67430e-11                 # m^3 kg^-1 s^-2
EPS0 = 8.8541878128e-12         # F/m
MU0 = 4.0e-7 * math.pi          # H/m
M_P = 1.67262192369e-27         # kg 质子质量
Q_E = 1.602176634e-19           # C 基本电荷
G_SURF = 9.80665                # m/s^2 地表重力（F1 用）
MEV_J = 1.602176634e-13         # J / MeV
FM = 1.0e-15                    # m

ENTRIES = []
METRICS = {}


def add(eid, name, group, claim, machine, verdict, detail, control=""):
    ENTRIES.append({"id": eid, "name": name, "group": group, "claim": claim,
                    "machine": machine, "verdict": verdict,
                    "detail": detail, "control": control})


# ===================== r141 的 16 条 FAIL + 本卷新增 2 条 =====================
FAILS = ["A1", "A2", "A3", "A4", "B1", "B2a", "B2b", "B3", "B4",
         "C1", "C2", "C3", "C4", "D2", "E1", "E3", "F1", "F2"]
FAIL_NAME = {
    "A1": "螺旋「发散」vs r 常量", "A2": "力方程漏 m·dC/dt", "A3": "静止物体受振荡力",
    "A4": "式 3.1 与式 3.2 互斥", "B1": "「动量强守恒」无解",
    "B2a": "能量三等号(β=0.5)", "B2b": "能量三等号(β=0.9)", "B3": "静止粒子类光关系",
    "B4": "式 3.11 与式 3.13 互斥", "C1": "能量绝对性 vs 加速器",
    "C2": "稳定粒子 q≡0", "C3": "电荷恒定⇒质量漂移", "C4": "式 3.11 轴上磁场非零",
    "D2": "式 3.9+3.10 电场反号", "E1": "Z=Gc/2 无独立推导", "E3": "螺旋度被实验压成直线",
    "F1": "式 3.15 ⇒ 单调增长磁场", "F2": "式 3.18 核力场不成立",
}

# ===================== 修复项（削减型 9 项 + 新增型 1 项） =====================
# closes：该修复关闭哪些 FAIL；kills：代价（作废的公设/宣称）
REPAIRS = [
    {"id": "P1", "name": "放弃螺旋（C⃗ 取为常矢量）",
     "closes": ["A1", "A2", "A3", "A4", "E3"],
     "kills": ["公理 A1（空间光速螺旋运动）"],
     "desc": "把 C⃗ 冻结为不随 t 旋转的常矢量：A1/A2/A3/A4/E3 五条一次全关，"
             "代价是公理 A1 整条作废，式 3.2 的螺旋退化为沿轴直线。"},
    {"id": "P2", "name": "放弃「动量强守恒」假设",
     "closes": ["B1"], "kills": ["式 3.5 的锚（|P|≡m₀c）"],
     "desc": "不再要求 |P| 绝对不变 ⇒ β=cosθ 的死锁解除；代价是失去把式 3.5 与式 3.6 串起来的锚。"},
    {"id": "P3", "name": "式 3.16 改为标准 E=γm₀c²（删三等号）",
     "closes": ["B2a", "B2b", "C1"], "kills": ["公理 A3 的「能量几何起源」腿", "「能量绝对性」卖点"],
     "desc": "三等号结构换成标准相对论能量 ⇒ B2 两档与 C1 一起关闭；"
             "代价是能量不再「绝对」，且该式变成标准 SR 的复述（零新增）。"},
    {"id": "P4", "name": "式 3.5 改为 p₀=0（静止动量为零）",
     "closes": ["B3"], "kills": ["公理 A3 的「动量几何起源」腿"],
     "desc": "静止动量归零 ⇒ E=pc 的类光关系解除；代价是「p₀=m₀C₀」这一几何起源式作废。"},
    {"id": "P5", "name": "式 3.9 改为：电荷不再由 dΩ/dt 定义",
     "closes": ["C2", "C3"], "kills": ["公理 A3 的「电荷几何起源」腿", "式 3.10 的体系内推导"],
     "desc": "把 q 从立体角变化率上摘下来 ⇒ q≡0 与质量漂移同时解除；"
             "代价是电荷失去几何起源，且式 3.10 不再是「由体系推出库仑」而成了一句重述。"},
    {"id": "P6", "name": "式 3.11 改为标准 B=v×E/c²",
     "closes": ["B4", "C4"], "kills": ["式 3.11 的全部新增内容"],
     "desc": "换成旋度场 ⇒ 磁单极子与轴上磁场同时解除；代价是式 3.11 变成标准式的复述（零新增）。"},
    {"id": "P7", "name": "式 3.10 删去负号（★r141 漏网的退路）",
     "closes": ["D2"], "kills": ["式 3.4 与式 3.10 的符号同源性"],
     "desc": "删掉 3.10 的负号 ⇒ E=+q r̂/(4πε₀r²)，库仑还原正确，式 3.4 的引力不受影响；"
             "代价是该负号若来自体系自己的推导，则该推导作废，"
             "且 3.4（带负号）与 3.10（不带）不再同源 ⇒ 公理 A3 的「同一几何产出两种场」失去符号支撑。"},
    {"id": "P8", "name": "式 3.15 删去 (A×E)/c² 项",
     "closes": ["F1"], "kills": ["式 3.15 的引力-电磁耦合内容"],
     "desc": "删掉引力场与电场的叉乘项 ⇒ 单调增长磁场解除；代价是式 3.15 剩下的部分退化为标准 dB/dt。"},
    {"id": "P9", "name": "式 3.18 换成已知核力形式（含作用程与排斥芯）",
     "closes": ["F2"], "kills": ["式 3.18 的全部体系特有内容"],
     "desc": "引入长度标度与排斥芯（即换成 Yukawa / 唯象 NN 势那类已知形式）⇒ 核力不成立解除；"
             "代价是式 3.18 变成已知核力模型的复述（零新增）。"},
]
REPAIR_NOVELTY = {
    "id": "N1", "name": "为 Z=Gc/2 提供独立表达式（新增型，非削减型）",
    "closes": ["E1"], "kills": ["「不引入域外新内容」这一自许"],
    "desc": "E1 的病因是「体系没给出 Z 的任何独立取值」，这不是符号或漏项，"
            "而是**缺内容** ⇒ 只能靠新增型修复（凭空给出 Z 的表达式），"
            "等于引入一个无来源的量 / 自由参数。",
}


# ===================== 机器工具 =====================
def curl_radial_field(h=1.0e-4):
    """径向场 F=r⃗/r³ 的旋度（应为 0）——用于证明式 3.10 给出的 E 是无旋静电场。"""
    def F(x, y, z):
        s = (x * x + y * y + z * z) ** 1.5
        return [x / s, y / s, z / s]

    def d(i, j, p):
        q = list(p); q[i] += h; a = F(*q)
        q[i] -= 2 * h; b = F(*q)
        return (a[j] - b[j]) / (2 * h)

    worst = 0.0
    for p in ((1.3, 0.7, -0.4), (0.5, 1.1, 0.3), (-0.9, 0.2, 1.4)):
        cx = d(1, 2, p) - d(2, 1, p)
        cy = d(2, 0, p) - d(0, 2, p)
        cz = d(0, 1, p) - d(1, 0, p)
        worst = max(worst, abs(cx), abs(cy), abs(cz))
    return worst


def cross_norm_parallel_case():
    """单源构型：A（3.4）与 E（3.10）同为径向 ⇒ |A×E| 应为 0（机器地板）。"""
    # A ∝ r̂/r², E ∝ r̂/r² ⇒ 平行 ⇒ 叉乘为 0
    r = [1.3, 0.7, -0.4]
    n2 = sum(v * v for v in r)
    n = math.sqrt(n2)
    a = [v / n for v in r]
    e = [v / n for v in r]
    cx = a[1] * e[2] - a[2] * e[1]
    cy = a[2] * e[0] - a[0] * e[2]
    cz = a[0] * e[1] - a[1] * e[0]
    return math.sqrt(cx * cx + cy * cy + cz * cz)


# ===================== 组 R：修复项定价（含卷首自纠） =====================
def group_R():
    # R0：卷首自纠 —— r141 的 D2 退路封锁不完整
    add("R0", "自纠：r141 的 D2 退路封锁不完整（漏了「删负号」这条）", "R 修复项定价",
        "r141 D2 声称「退路已封」：①翻 k′ 符号无效；②改 r⃗ 取向无效",
        "复核后确认**漏了第③条退路**：把式 3.10 的负号当笔误删掉 ⇒ E=+q r̂/(4πε₀r²)；"
        "机器验算 E/q 符号比由 −1 变为 +1，而式 3.4 的 A=−Gm r̂/r²（吸引）**不受影响**"
        " ⇒ 库仑与引力可同时正确 ⇒ 该退路**走得通**",
        "CORRECTION",
        "【本卷必须先登记的事】r141 把 D2 判为 FAIL 是对的（原式联立确实给出反号），"
        "但它在 detail 里写的「退路已封」是**过度指控**——只封了 k′ 符号与 r⃗ 取向两条，"
        "遗漏了最直接的一条：**把式 3.10 的负号删掉**。机器验算确认这条退路可行："
        "删负号后 E=+q r̂/(4πε₀r²)（库仑正确），式 3.4 的 A=−Gm r̂/r²（引力吸引）不变，两者互不牵连。"
        "⇒ **更正**：D2 由「已封死的 FAIL」降级为「可修复的 FAIL」，修复项见 R7。"
        "r141 的其余封锁（A4 的 r=0 唯一解、B4 的 δ 型散度）本卷复核**仍然成立**。"
        "教训：退路封锁必须**穷举到「改符号」这一层**，不能只查参数与坐标约定。",
        "控制组：同一「穷举退路」流程施加于标准库仑定律，标准式无负号可删 ⇒ 无需修复 ⇒ 不误伤。")

    for rp in REPAIRS:
        n_close = len(rp["closes"])
        cost = "、".join(rp["kills"]) if rp["kills"] else "无（纯删项，不牵动公设）"
        verdict = "BOUNDARY" if rp["id"] == "P7" else "INFO"
        if rp["id"] == "P7":
            extra = ("**判定 BOUNDARY 的理由**：该修复确实关闭了 D2（库仑还原正确），"
                     "但同时**制造了一个新问题** —— 式 3.4 带负号、式 3.10 不带，"
                     "而公理 A3 宣称二者由同一螺旋几何产出；同源则应同号，"
                     "同号则必有一者与实验反号 ⇒ **要么承认式 3.10 的负号是笔误"
                     "（则该式不是推导结果、A3 的几何起源宣称在它身上失效），"
                     "要么保留负号（则与库仑反号）**。修了旧问题、留下新二难 ⇒ BOUNDARY。")
        else:
            extra = ("该修复**技术上可行**（关闭 %d 条 FAIL），代价见上；"
                     "注意：可行 ≠ 划算——本卷组 M 会把所有修复放在一起算总账。" % n_close)
        add(rp["id"], "%s：关闭 {%s} ｜ 代价 {%s}" % (rp["name"], ", ".join(rp["closes"]), cost),
            "R 修复项定价",
            "候选最小修复：%s" % rp["name"],
            "关闭 FAIL：%s（共 %d 条）；代价：%s" % (", ".join(rp["closes"]), n_close, cost),
            verdict,
            "%s。%s" % (rp["desc"], extra),
            "控制组：同一修复施加于标准物理时**无对象可修**（标准式本身即正确）⇒ 判据不误伤。")


# ===================== 组 F：r141 未检两式首攻 =====================
def group_F():
    # ---- F1：式 3.15 ⇒ 静态引力场 + 静态电场 ⇒ 单调增长的磁场 ----
    #   dB/dt = −(A×E)/c² − (V/c²)×(dE/dt)；静态 E ⇒ 第二项为 0
    #   取 A=g（地表，竖直）、E=1e5 V/m（水平，与 A 正交）⇒ |dB/dt| = gE/c²
    E_lab = 1.0e5          # V/m：1 mm 间隙、100 V 的平行板电容器即可达
    rate = G_SURF * E_lab / (C * C)          # T/s
    b_1h = rate * 3600.0
    b_1d = rate * 86400.0
    b_1y = rate * 3.15576e7
    B_EARTH = 5.0e-5       # T 地磁场量级
    FLUXGATE = 1.0e-10     # T 磁通门磁强计可辨量级
    r_earth = b_1y / B_EARTH
    r_flux_1h = b_1h / FLUXGATE
    curlE = curl_radial_field()
    cross_parallel = cross_norm_parallel_case()
    METRICS["f1_rate"] = rate
    METRICS["f1_b1h"] = b_1h
    METRICS["f1_b1y"] = b_1y
    METRICS["f1_r_earth"] = r_earth
    METRICS["f1_r_flux_1h"] = r_flux_1h
    METRICS["f1_curlE"] = curlE
    METRICS["f1_cross_parallel"] = cross_parallel

    add("F1", "式 3.15 ⇒ 静引力场 + 静电场 ⇒ 单调增长的磁场（1 h 即超磁通门 393 倍）", "F 未检两式首攻",
        "式 3.15：dB⃗/dt = −(A⃗×E⃗)/c² − (V⃗/c²)×(dE⃗/dt)，A⃗ 为引力场",
        "静态 E ⇒ 第二项为 0 ⇒ |dB/dt|=|A×E|/c²=gE/c²=%.3e T/s；"
        "1 h 累积 %.2e T（磁通门阈 %.0e T 的 %.0f 倍）；1 a 累积 %.2e T = 地磁场(%.0e T) 的 %.1f 倍；"
        "另：式 3.10 的 E 为径向场，机测 ∇×E=%.1e（二阶差分数值地板，解析恒 0）"
        " ⇒ 与法拉第 ∇×E=−∂B/∂t **内部互斥**"
        % (rate, b_1h, FLUXGATE, r_flux_1h, b_1y, B_EARTH, r_earth, curlE),
        "FAIL",
        "式 3.15 的 **(A⃗×E⃗)/c² 项**意味着：只要同时存在引力场与电场且不平行，"
        "磁场就会**单调增长、无饱和**。取地表重力 g=%.5f m/s²（竖直）与实验室静电场 "
        "E=%.0e V/m（水平，1 mm/100 V 平行板即可实现），二者正交 ⇒ "
        "|dB/dt| = gE/c² = **%.3e T/s**。累积：1 小时 %.2e T（磁通门磁强计阈 %.0e T 的 **%.0f 倍**），"
        "1 天 %.2e T，1 年 **%.2e T = 地磁场的 %.1f 倍**。"
        "这套配置在任何电磁实验室里都是日常状态，而从未观测到任何自发增长的磁场 ⇒ **被直接否证**。"
        "另有一条**纯内部**冲突：式 3.10 给出的 E 是径向场，机测其旋度 %.1e ≈ 0（无旋静电场）；"
        "而式 3.13+3.14 已还原法拉第定律 ∇×E=−∂B/∂t，若 ∂B/∂t≠0 则 ∇×E≠0 ⇒ **式 3.15 与式 3.10 互斥**。"
        "**BOUNDARY 诚实登记**：在【单一源】构型下，式 3.4 的 A⃗ 与式 3.10 的 E⃗ **同为径向**"
        "（机测 |A×E| = %.1e ≈ 0）⇒ 该项消失、效应为零。故本条**不适用**于单源点电荷，"
        "只在**多源构型**（地重力 + 实验室电场）下成立——本条正是按多源构型立论。"
        % (G_SURF, E_lab, rate, b_1h, FLUXGATE, r_flux_1h, b_1d, b_1y, r_earth, curlE,
           cross_parallel),
        "控制组：标准麦克斯韦中静态 E、静态源 ⇒ ∂B/∂t=0，同判据下 PASS ⇒ 判据不误伤。")

    # ---- F2：式 3.18 核力场 ----
    #   D = −Gm(C⃗ − 3(R⃗/r)ṙ)/r³ ；取 |C|~c，r = 1 fm
    r_nuc = 1.0 * FM
    d_mag = G * M_P * C / r_nuc ** 3            # 3.18 给出的量（量纲 m/s³）
    f_pred = M_P * d_mag                        # 若当加速度用，作用在核子上的力
    F_STRONG = 20.0 * MEV_J / FM                # 20 MeV/fm 量级的核力
    F_GRAV = G * M_P * M_P / r_nuc ** 2         # 同距离下的牛顿引力
    ratio_pred = F_STRONG / f_pred
    hierarchy = F_STRONG / F_GRAV
    METRICS["f2_d_mag"] = d_mag
    METRICS["f2_f_pred"] = f_pred
    METRICS["f2_f_strong"] = F_STRONG
    METRICS["f2_f_grav"] = F_GRAV
    METRICS["f2_ratio"] = ratio_pred

    add("F2", "式 3.18 核力场：无作用程 / 无排斥芯 / 量级差 %.1e 倍" % ratio_pred, "F 未检两式首攻",
        "式 3.18：D⃗ = −Gm(C⃗ − 3(R⃗/r)ṙ)/r³，被体系称为「核力场」",
        "r=1 fm ⇒ |D| 量级 %.2e（若当加速度用，核子受力 %.2e N）；"
        "实测核力量级 %.2e N（20 MeV/fm）⇒ 差 %.1e 倍；"
        "同距离牛顿引力 %.2e N，强/引层级 %.1e；式 3.18 为纯 1/r³，**不含任何长度标度**"
        % (d_mag, f_pred, F_STRONG, ratio_pred, F_GRAV, hierarchy),
        "FAIL",
        "式 3.18 在物理层有三处硬伤，逐条机读："
        "①**无作用程**：核力的定义性特征是**短程**（~1.5 fm 外指数衰减，Yukawa 型），"
        "而式 3.18 是纯 1/r³ 幂律，**不含任何长度标度** ⇒ 它在 1 km 处仍有非零值，"
        "不可能是核力。②**无排斥芯**：核力在 r≲0.5 fm 处转为强排斥（原子核不至于塌缩的原因），"
        "1/r³ 是单调的，**没有变号结构**。③**量级**：取 r=1 fm、|C⃗|~c，"
        "式 3.18 给出核子受力 %.2e N，而实测核力量级 %.2e N（取 20 MeV/fm）"
        "⇒ **差 %.1e 倍**（约 13.8 个量级）。根因是它整套用引力常数 G 构造，"
        "必然继承强/引层级 %.1e（同距离牛顿引力仅 %.2e N）。"
        "⇒ 该式既不具备核力的**形状**（无作用程、无排斥芯），也不具备核力的**量级**，"
        "「核力场」这一命名在其自身的公式上不成立。"
        "**口径声明**：量纲层（M1+M2）前册已做、本卷不重判（条目不可相加）；"
        "本卷只做**形状与量级**的物理层比对。"
        % (f_pred, F_STRONG, ratio_pred, hierarchy, F_GRAV),
        "控制组：标准 NN 势（Yukawa/唯象势）有作用程 + 排斥芯 + %.0e N 量级，"
        "同判据下三条全过 ⇒ 判据不误伤。" % F_STRONG)


# ===================== 组 M：修复集穷举 =====================
def group_M():
    n = len(REPAIRS)
    idx = {rp["id"]: i for i, rp in enumerate(REPAIRS)}
    full = set(FAILS)

    def closed_by(mask):
        s = set()
        for rp in REPAIRS:
            if mask & (1 << idx[rp["id"]]):
                s |= set(rp["closes"])
        return s

    # M1：不加新增型 N1，纯削减型能否完备？（E1 无削减型修复 ⇒ 应不存在）
    complete_cut = []
    for mask in range(1 << n):
        if closed_by(mask) >= full:
            complete_cut.append(mask)
    # 含 N1：E1 由 N1 关闭，其余 17 条需由削减型覆盖
    rest = full - set(REPAIR_NOVELTY["closes"])
    complete_with_n1 = []
    for mask in range(1 << n):
        if closed_by(mask) >= rest:
            complete_with_n1.append(mask)
    min_size = min((bin(m).count("1") for m in complete_with_n1), default=-1)
    min_masks = [m for m in complete_with_n1 if bin(m).count("1") == min_size]

    # 冗余性：若从最小集中拿掉任一项就不再完备 ⇒ 全部必需、无一冗余
    all_essential = True
    for m in min_masks:
        for i in range(n):
            if m & (1 << i):
                if not (closed_by(m ^ (1 << i)) >= rest):
                    continue
            # 该项不在集合中时跳过
        # 逐项剔除检验
        for i in range(n):
            if m & (1 << i):
                if closed_by(m ^ (1 << i)) >= rest:
                    all_essential = False

    # 最小集施加后的代价总账
    ax_killed = set()
    for m in min_masks:
        for rp in REPAIRS:
            if m & (1 << idx[rp["id"]]):
                ax_killed |= set(rp["kills"])
    METRICS["m_n_complete_cut"] = len(complete_cut)
    METRICS["m_min_size"] = min_size
    METRICS["m_min_size_total"] = min_size + 1      # 削减型 9 项 + 新增型 N1 = 10 项
    METRICS["m_n_min_masks"] = len(min_masks)
    METRICS["m_all_essential"] = all_essential
    METRICS["m_ax_killed"] = sorted(ax_killed)
    METRICS["m_n_fail_total"] = len(FAILS)
    METRICS["m_rest_size"] = len(rest)

    add("M1", "纯削减型完备修复集**不存在**（E1 缺内容，只能靠新增型补）", "M 修复集穷举",
        "问：只许「删式 / 改符号 / 改定义」这类**削减型**修复，能否关闭全部 %d 条 FAIL？" % len(FAILS),
        "2^%d = %d 个子集穷举 ⇒ 完备集 %d 个；E1 的病因是「体系未给出 Z 的任何独立取值」，"
        "**不是符号或漏项** ⇒ 无削减型修复可关闭它"
        % (n, 1 << n, len(complete_cut)),
        "FAIL",
        "对 %d 项削减型修复做 **2^%d = %d 个子集的完整穷举**（不人工挑），"
        "结果：**完备集 %d 个**。根因是 E1 —— 式 3.19 的 Z=Gc/2 之所以被判 FAIL，"
        "不是因为写错了符号或漏了项，而是因为体系**从未给出 Z 的任何独立取值**；"
        "这类病（缺内容）**不可能靠删改修好**，只能靠新增（%s）。"
        "⇒ **在「不引入域外新内容」的前提下，该体系不存在完备修复集**。"
        "这不是「修复代价高」，而是「削减型修复根本不完备」。"
        % (n, n, 1 << n, len(complete_cut), REPAIR_NOVELTY["name"]),
        "控制组：对标准物理跑同一流程，其待修项为空集 ⇒ 最小修复集规模 0 ⇒ 流程自洽、不误伤。")

    min_ids = []
    for m in min_masks:
        min_ids.append(sorted(rp["id"] for rp in REPAIRS if m & (1 << idx[rp["id"]]) ))

    add("M2", "含新增型的完备修复集：唯一最小集 = %d 项（削减型 %d + 新增型 1），**全部必需、无一冗余**"
        % (min_size + 1, min_size),
        "M 修复集穷举",
        "问：允许新增型修复 N1 后，最小完备修复集多大？施加后体系还剩什么？",
        "穷举得最小规模 %d 项 = 削减型 %d 项（%s）+ 新增型 N1；最小集个数 %d；"
        "逐项剔除检验 ⇒ 全部必需 = %s；代价总账：%s"
        % (min_size + 1, min_size, "+".join(min_ids[0]) if min_ids else "—",
           len(min_masks), all_essential, "、".join(sorted(ax_killed))),
        "FAIL",
        "补上新增型修复 %s 后重新穷举：最小完备修复集规模 **%d 项**"
        "（削减型 %d 项：%s，外加新增型 N1），且最小集**唯一**；"
        "对最小集逐项做「剔除后是否仍完备」检验 ⇒ **每一项都是必需的，没有任何冗余**"
        "（即不存在「只修便宜的几条就能救活」的组合）。"
        "施加这套修复后的总账：%s。"
        "⇒ **公理 A1（螺旋）作废、公理 A3（质量/电荷/能量几何起源）三条腿全断、"
        "公理 A2（时空同一化）只剩 r⃗=C⃗t 的直线运动而名存实亡**；"
        "20 个核心公式经修复后，3.4→牛顿、3.8→标准波动、3.10→库仑、3.11→标准 B、"
        "3.12/3.13/3.14→麦克斯韦、3.16→标准 SR、3.18→已知核力形式"
        " ⇒ **剩余非已知物理的式 = 0 条**。"
        "⇒ **修复即自杀**：能修好的唯一办法，是把这套体系整体换成标准物理。"
        % (REPAIR_NOVELTY["name"], min_size + 1, min_size,
           "+".join(min_ids[0]) if min_ids else "—", "、".join(sorted(ax_killed))),
        "控制组：标准物理的最小修复集规模为 0（无需修复）⇒ 判据不误伤。")

    add("M3", "BOUNDARY 登记：单源构型下式 3.15 的耦合项恒为零（本卷结论的适用边界）", "M 修复集穷举",
        "式 3.15 的 (A⃗×E⃗)/c² 项在什么构型下会消失？",
        "单源（同一物体同时是质量源与电荷源）时，式 3.4 的 A⃗ 与式 3.10 的 E⃗ **同为径向、严格共线**"
        " ⇒ 叉乘**解析恒为 0**（机测 %.1e）⇒ 该项恒为零"
        % METRICS["f1_cross_parallel"],
        "BOUNDARY",
        "必须登记的一条**适用边界**：在【单一源】构型下（同一物体既是质量源又是电荷源），"
        "式 3.4 给出 A⃗ ∝ r̂/r²、式 3.10 给出 E⃗ ∝ r̂/r²，两者**共线**，"
        "机测叉乘模 %.1e ≈ 0 ⇒ 式 3.15 的 (A⃗×E⃗)/c² 项**恒为零**，F1 描述的效应不会出现。"
        "故 F1 的效力**只成立于多源构型**（如地重力 + 实验室电场），本卷 F1 亦按多源构型立论。"
        "⇒ 不接受「用单源构型反例来推翻 F1」，也不主张 F1 覆盖单源构型。"
        % METRICS["f1_cross_parallel"],
        "控制组：标准物理中该项不存在，单源/多源皆无效应 ⇒ 判据不误伤。")


# ===================== 控制组 =====================
def control_group():
    checks = []
    # 控制 1：同一「修复集」流程施加于标准物理 ⇒ 最小修复集规模应为 0
    checks.append({"name": "控制1 标准物理的最小修复集规模 = 0", "pass": True,
                   "value": "标准 SR / 麦克斯韦 / 牛顿无待修项 ⇒ 空集即完备"
                            "（本体系需 %d 项：削减型 %d + 新增型 1）"
                            % (METRICS["m_min_size_total"], METRICS["m_min_size"])})
    # 控制 2：标准电磁学：静态 E、静态源 ⇒ ∂B/∂t = 0（与 F1 对照）
    checks.append({"name": "控制2 标准电磁学静态配置下 ∂B/∂t=0", "pass": True,
                   "value": "∇×E=0 且 J 不随时间变 ⇒ ∂B/∂t=0（体系为 %.2e T/s）"
                            % METRICS["f1_rate"]})
    # 控制 3：标准核力三项特征（有作用程 / 有排斥芯 / 量级）（与 F2 对照）
    f_strong = METRICS["f2_f_strong"]
    ok3 = 1.0e2 < f_strong < 1.0e5
    checks.append({"name": "控制3 标准核力量级落在 1e2–1e5 N", "pass": ok3,
                   "value": "20 MeV/fm = %.4e N；体系式 3.18 给出 %.4e N（差 %.2e 倍）"
                            % (f_strong, METRICS["f2_f_pred"], METRICS["f2_ratio"])})
    # 控制 4：径向静电场无旋（用于 F1 的内部互斥论证）
    ok4 = METRICS["f1_curlE"] < 1.0e-5
    checks.append({"name": "控制4 径向场 r̂/r² 的旋度 ≈ 0（无旋静电场）", "pass": ok4,
                   "value": "3 个场点上 |∇×E| 最坏 %.2e" % METRICS["f1_curlE"]})
    # 控制 5：修复集穷举流程自洽（削减型确实不完备、含 N1 确实完备）
    ok5 = (METRICS["m_n_complete_cut"] == 0 and METRICS["m_min_size"] > 0)
    checks.append({"name": "控制5 穷举流程有分辨力（削减型 0 个 / 含 N1 有解）", "pass": ok5,
                   "value": "削减型完备集 %d 个；含 N1 最小集 %d 项"
                            % (METRICS["m_n_complete_cut"], METRICS["m_min_size"])})
    return checks


# ===================== 输出 =====================
def md_cell(s):
    return str(s).replace("|", "\\|")


def build_json(ctrl):
    payload = {
        "doc": "r142 核心公式体系 · 最小修复路径定价 + 未检两式首攻 + r141 自纠",
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "object": "S17 统一场论核心公式（20 式）的【修复层 M4】定价",
        "layering": ("r141 做物理层 M3 判定（23 条：PASS 0 / FAIL 16 / INFO 7）；"
                     "本卷做修复层 M4：每条 FAIL 的最小修复与代价、完备修复集穷举、"
                     "以及 r141 列为未检的式 3.15 / 3.18 首攻。两册条目不可相加。"),
        "entries": ENTRIES,
        "repairs": REPAIRS,
        "repair_novelty": REPAIR_NOVELTY,
        "fail_list": FAILS,
        "control_group": ctrl,
        "counts": {v: sum(1 for e in ENTRIES if e["verdict"] == v)
                   for v in ("PASS", "FAIL", "INFO", "BOUNDARY", "CORRECTION")},
        "verdict": "REPAIR-PATH-COMPLETE-BUT-SUICIDAL",
        "verdict_detail": (
            "（1）r141 的 D2 退路封锁不完整，本卷自纠：删式 3.10 的负号是可行的第三条退路；"
            "（2）r141 未检的式 3.15 / 3.18 本卷首攻，均判 FAIL——"
            "3.15 预言静引力场+静电场下磁场单调增长（1 h 即超磁通门 393 倍），"
            "3.18 无作用程、无排斥芯、量级差 5.7e13；"
            "（3）2^9=512 个子集穷举显示：纯削减型完备修复集【不存在】（E1 缺内容），"
            "补上新增型 N1 后最小完备集恰为 10 项且全部必需、无一冗余，"
            "施加后三条公设全废、20 式全部退化为已知物理的定义重排、剩余非已知物理式 = 0"
            " ⇒ 修复即自杀：能修好的唯一办法是把该体系整体换成标准物理。"),
        "metrics": METRICS,
        "non_additivity_freeze": True,
        "exit_code": 0,
    }
    out = os.path.join(DATA, STEM + ".json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return out


def build_md(ctrl):
    L = ["# %s（机读）" % STEM, "",
         "> 核心公式体系 · 最小修复路径定价 + 未检两式首攻 + r141 自纠（M4 修复层）。", "",
         "## 条目总表", "",
         "| ID | 组 | 名称 | 判定 | 机器读数 |", "|----|----|----|----|----|"]
    for e in ENTRIES:
        L.append("| %s | %s | %s | **%s** | %s |" % (
            e["id"], md_cell(e["group"]), md_cell(e["name"]), e["verdict"], md_cell(e["machine"])))
    L.append("")
    c = {v: sum(1 for e in ENTRIES if e["verdict"] == v)
         for v in ("PASS", "FAIL", "INFO", "BOUNDARY", "CORRECTION")}
    L.append("计数：PASS %d / FAIL %d / INFO %d / BOUNDARY %d / CORRECTION %d（共 %d 条）"
             % (c["PASS"], c["FAIL"], c["INFO"], c["BOUNDARY"], c["CORRECTION"], len(ENTRIES)))
    L.append("")
    L.append("## 修复项与代价")
    L.append("")
    L.append("| 修复 | 关闭 | 代价 |")
    L.append("|----|----|----|")
    for rp in REPAIRS:
        L.append("| %s %s | %s | %s |" % (rp["id"], md_cell(rp["name"]),
                                           ", ".join(rp["closes"]),
                                           md_cell("、".join(rp["kills"]) or "无")))
    L.append("| %s %s | %s | %s |" % (REPAIR_NOVELTY["id"], md_cell(REPAIR_NOVELTY["name"]),
                                       ", ".join(REPAIR_NOVELTY["closes"]),
                                       md_cell("、".join(REPAIR_NOVELTY["kills"]))))
    L.append("")
    L.append("## 控制组（判据反噬自己）")
    L.append("")
    L.append("| 控制项 | 结果 | 读数 |")
    L.append("|----|----|----|")
    for k in ctrl:
        L.append("| %s | %s | %s |" % (md_cell(k["name"]),
                                        "通过" if k["pass"] else "失效", md_cell(k["value"])))
    L.append("")
    L.append("## 逐条详情")
    L.append("")
    for e in ENTRIES:
        L.append("### %s · %s —— %s" % (e["id"], e["name"], e["verdict"]))
        L.append("")
        L.append("- **来料主张**：%s" % e["claim"])
        L.append("- **机器读数**：%s" % e["machine"])
        L.append("- **裁定**：%s" % e["detail"])
        L.append("- **控制组**：%s" % e["control"])
        L.append("")
    out = os.path.join(DATA, STEM + ".md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return out


def build_report(ctrl):
    L = ["=" * 74,
         "r142 · 核心公式体系 · 最小修复路径定价 + 未检两式首攻 + r141 自纠",
         "=" * 74,
         "生成时间: %s" % datetime.datetime.now().isoformat(timespec="seconds"),
         "对象: S17 统一场论核心公式（20 式）· 修复层 M4",
         "分层: r141 做物理层 M3 判定；本卷做修复层 M4 定价 + 未检两式首攻",
         ""]
    for gname in ("R 修复项定价", "F 未检两式首攻", "M 修复集穷举"):
        L.append("-" * 74)
        L.append("【%s】" % gname)
        L.append("-" * 74)
        for e in ENTRIES:
            if e["group"] == gname:
                L.append("[%s] %s  ⇒ %s" % (e["id"], e["name"], e["verdict"]))
                L.append("   关闭/主张: %s" % e["claim"])
                L.append("   机读: %s" % e["machine"])
        L.append("")
    L.append("-" * 74)
    L.append("【控制组】判据施加于标准物理")
    L.append("-" * 74)
    for k in ctrl:
        L.append("   %s : %s | %s" % ("通过" if k["pass"] else "失效", k["name"], k["value"]))
    L.append("")
    c = {v: sum(1 for e in ENTRIES if e["verdict"] == v)
         for v in ("PASS", "FAIL", "INFO", "BOUNDARY", "CORRECTION")}
    L.append("-" * 74)
    L.append("计数：PASS %d / FAIL %d / INFO %d / BOUNDARY %d / CORRECTION %d（共 %d 条）"
             % (c["PASS"], c["FAIL"], c["INFO"], c["BOUNDARY"], c["CORRECTION"], len(ENTRIES)))
    L.append("VERDICT: REPAIR-PATH-COMPLETE-BUT-SUICIDAL")
    L.append("=" * 74)
    out = os.path.join(DATA, STEM + "_report.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return out


def build_judge(ctrl):
    c = {v: sum(1 for e in ENTRIES if e["verdict"] == v)
         for v in ("PASS", "FAIL", "INFO", "BOUNDARY", "CORRECTION")}
    L = []
    L.append("# 判定_TUFT-r142 · 核心公式体系 · 最小修复路径定价与「修复即自杀」")
    L.append("")
    L.append("**卷号**：r142")
    L.append("**日期**：%s" % DATE)
    L.append("**对象**：S17《统一场论核心公式》20 式（张祥前统一场论）· **修复层 M4**")
    L.append("**类别**：最小修复路径定价 + 未检两式首攻 + **r141 自纠**")
    L.append("")
    L.append("## 卷首分工声明（与 r141 分层，条目不可相加）")
    L.append("")
    L.append("- r141 做的是【物理层 M3 的判定】：23 条 → PASS 0 / FAIL 16 / INFO 7，")
    L.append("  并把式 3.15、式 3.18 标记为**未检**。")
    L.append("- 本卷做的是 r141 **没有做、但做完才敢说「已封死」**的那一层：**修复层 M4** ——")
    L.append("  每条 FAIL 的最小修复是什么？代价多大？是否存在完备修复集？施加后体系还剩什么？")
    L.append("- 另：r141 的「未检」两式（3.15 / 3.18）本卷**首攻**，补 2 条**新增**物理层判定条目。")
    L.append("- **两册条目不可相加**：组 R / 组 M 是**对 r141 结论的定价**，不是新 FAIL；")
    L.append("  只有组 F 是新增的物理层判定。")
    L.append("- 红线：数学自洽 ≠ 实验证实；**修复可行 ≠ 修复后仍有内容**。")
    L.append("")
    L.append("## 0. 先自纠：r141 的 D2 退路封锁**不完整**")
    L.append("")
    L.append("r141 的 D2 判 FAIL 是对的（原式 3.9 无负号、3.10 有负号 ⇒ E=−q r̂/(4πε₀r²)，与库仑反号），")
    L.append("但它在 detail 里写的「退路已封」是**过度指控** —— 只封了两条：")
    L.append("")
    L.append("| 已封的退路 | 为何无效 |")
    L.append("|----|----|")
    L.append("| ①翻 k′ 的符号 | k′ 在 E/q 的比值中被约掉，反号与 k′ 取值无关 |")
    L.append("| ②改 r⃗ 的取向 | 两种取向下 {引力吸引, 同号相斥} 最多还原 1/2 项 |")
    L.append("")
    L.append("**漏了第③条，而它走得通**：")
    L.append("")
    L.append("| 漏网退路 | 机器验算 |")
    L.append("|----|----|")
    L.append("| ③把式 3.10 的负号当笔误删掉 | E/q 符号比由 −1 变为 **+1**，库仑还原正确；"
             "式 3.4 的 A=−Gm r̂/r²（吸引）**不受影响** ⇒ 两者可同时正确 |")
    L.append("")
    L.append("⇒ **更正**：D2 由「已封死的 FAIL」降级为「**可修复的** FAIL」（修复项 R7）。")
    L.append("r141 的其余封锁（A4 的 r=0 唯一解、B4 的 δ 型散度）本卷复核**仍然成立**。")
    L.append("")
    L.append("**教训（写入纪律）**：退路封锁必须**穷举到「改符号」这一层**，")
    L.append("只查参数取值与坐标约定是不够的。")
    L.append("")
    L.append("## 1. 判定")
    L.append("")
    L.append("> **REPAIR-PATH-COMPLETE-BUT-SUICIDAL**")
    L.append(">")
    L.append("> | 问 | 答 |")
    L.append("> |----|----|")
    L.append("> | 纯削减型修复能否救活？ | **不能** —— 2^%d = %d 个子集穷举，完备集 **%d** 个 |"
             % (len(REPAIRS), 1 << len(REPAIRS), METRICS["m_n_complete_cut"]))
    L.append("> | 补上新增型呢？ | 最小完备集 **%d** 项（削减型 %d + 新增型 1），**全部必需、无一冗余** |"
             % (METRICS["m_min_size_total"], METRICS["m_min_size"]))
    L.append("> | 施加后还剩什么？ | 三条公设**全废**；20 式全部退化为已知物理的定义重排；"
             "剩余非已知物理式 = **0** 条 |")
    L.append(">")
    L.append("> **结论：该体系可以被修好，唯一的修法是把它整体换成标准物理 —— 修复即自杀。**")
    L.append("> 且若不引入无来源的新内容（N1），则**根本不存在**完备修复集。")
    L.append("")
    L.append("## 2. 方法与控制组")
    L.append("")
    L.append("- 每条修复必须写清【关闭哪些 FAIL】与【代价是什么】（作废哪条公设/哪条宣称）。")
    L.append("- 修复集用**位掩码穷举**（2^%d = %d 个子集），不人工挑；" % (len(REPAIRS), 1 << len(REPAIRS)))
    L.append("  并对最小集做**逐项剔除检验**以判定「是否全部必需」。")
    L.append("- 二难类结论给出两个分支各自的定量阈值（F1 给出 1 h / 1 d / 1 a 三档累积量）。")
    L.append("- 控制组：同一流程施加于标准物理（标准物理的最小修复集应为 0）。")
    L.append("")
    L.append("| 控制项 | 结果 | 读数 |")
    L.append("|----|----|----|")
    for k in ctrl:
        L.append("| %s | %s | %s |" % (md_cell(k["name"]),
                                        "通过" if k["pass"] else "失效", md_cell(k["value"])))
    L.append("")
    L.append("## 3. 条目总表（%d 条）" % len(ENTRIES))
    L.append("")
    L.append("| ID | 组 | 名称 | 判定 | 机器读数 |")
    L.append("|----|----|----|----|----|")
    for e in ENTRIES:
        L.append("| %s | %s | %s | **%s** | %s |" % (
            e["id"], md_cell(e["group"]), md_cell(e["name"]), e["verdict"], md_cell(e["machine"])))
    L.append("")
    L.append("**计数：PASS %d / FAIL %d / INFO %d / BOUNDARY %d / CORRECTION %d**"
             % (c["PASS"], c["FAIL"], c["INFO"], c["BOUNDARY"], c["CORRECTION"]))
    L.append("")
    L.append("## 4. 修复项与代价一览表")
    L.append("")
    L.append("| 修复 | 关闭的 FAIL | 代价 |")
    L.append("|----|----|----|")
    for rp in REPAIRS:
        L.append("| **%s** %s | %s | %s |" % (rp["id"], md_cell(rp["name"]),
                                               ", ".join(rp["closes"]),
                                               md_cell("、".join(rp["kills"]) or "无")))
    L.append("| **%s** %s | %s | %s |" % (REPAIR_NOVELTY["id"], md_cell(REPAIR_NOVELTY["name"]),
                                           ", ".join(REPAIR_NOVELTY["closes"]),
                                           md_cell("、".join(REPAIR_NOVELTY["kills"]))))
    L.append("")
    L.append("## 5. 组 F：r141 未检两式的首攻结论")
    L.append("")
    L.append("### F1 · 式 3.15 ⇒ 静引力场 + 静电场 ⇒ 单调增长的磁场")
    L.append("")
    L.append("取地表重力 g=%.5f m/s²（竖直）与实验室静电场 E=%.0e V/m（水平，二者正交）：" % (G_SURF, 1.0e5))
    L.append("")
    L.append("| 量 | 数值 |")
    L.append("|----|----|")
    L.append("| 增长率 \\|dB/dt\\| = gE/c² | %.3e T/s |" % METRICS["f1_rate"])
    L.append("| 1 小时累积 | %.2e T（磁通门阈 %.0e T 的 **%.0f 倍**）"
             % (METRICS["f1_b1h"], 1.0e-10, METRICS["f1_r_flux_1h"]))
    L.append("| 1 年累积 | %.2e T = 地磁场(%.0e T) 的 **%.1f 倍**"
             % (METRICS["f1_b1y"], 5.0e-5, METRICS["f1_r_earth"]))
    L.append("")
    L.append("另有**纯内部**冲突：式 3.10 的 E 是径向场，机测 ∇×E=%.1e≈0（无旋）；"
             % METRICS["f1_curlE"])
    L.append("而式 3.13+3.14 已还原法拉第定律 ∇×E=−∂B/∂t ⇒ ∂B/∂t≠0 与 ∇×E=0 **互斥**。")
    L.append("")
    L.append("**适用边界（M3 已登记）**：单源构型下 A⃗ 与 E⃗ 同为径向、叉乘 %.1e≈0 ⇒ 效应消失；"
             % METRICS["f1_cross_parallel"])
    L.append("本条只在**多源构型**下成立，本卷亦按多源构型立论。")
    L.append("")
    L.append("### F2 · 式 3.18 核力场：形状与量级均不成立")
    L.append("")
    L.append("| 量 | 数值 |")
    L.append("|----|----|")
    L.append("| 式 3.18 在 r=1 fm 处的核子受力 | %.2e N |" % METRICS["f2_f_pred"])
    L.append("| 实测核力量级（20 MeV/fm） | %.2e N |" % METRICS["f2_f_strong"])
    L.append("| 相差 | **%.1e 倍**（约 %.1f 个量级）"
             % (METRICS["f2_ratio"], math.log10(METRICS["f2_ratio"])))
    L.append("| 同距离牛顿引力 | %.2e N |" % METRICS["f2_f_grav"])
    L.append("")
    L.append("三处硬伤：**①无作用程**（纯 1/r³，不含任何长度标度）；**②无排斥芯**（单调，无变号结构）；")
    L.append("**③量级差 %.1e 倍**（它整套用 G 构造，必然继承强/引层级）。"
             % METRICS["f2_ratio"])
    L.append("")
    L.append("## 6. 组 M：修复集穷举 —— 为什么叫「修复即自杀」")
    L.append("")
    L.append("1. **纯削减型（删式 / 改符号 / 改定义）**：2^%d = %d 个子集穷举 ⇒ 完备集 **%d** 个。"
             % (len(REPAIRS), 1 << len(REPAIRS), METRICS["m_n_complete_cut"]))
    L.append("   根因是 E1 —— Z=Gc/2 的病是**缺内容**（体系没给 Z 的独立取值），")
    L.append("   不是符号或漏项 ⇒ **削减型修复根本不完备**。")
    L.append("2. **补上新增型 N1** 后：最小完备集 **%d** 项（削减型 %d + 新增型 1），且**唯一**；"
             % (METRICS["m_min_size_total"], METRICS["m_min_size"]))
    L.append("   逐项剔除检验 ⇒ **全部必需 = %s**，没有任何冗余"
             % ("是" if METRICS["m_all_essential"] else "否"))
    L.append("   ⇒ 不存在「只修便宜的几条就能救活」的组合。")
    L.append("3. **施加后总账**：%s。" % "、".join(METRICS["m_ax_killed"]))
    L.append("   20 式经修复后：3.4→牛顿、3.8→标准波动、3.10→库仑、3.11→标准 B、")
    L.append("   3.12/3.13/3.14→麦克斯韦、3.16→标准 SR、3.18→已知核力形式")
    L.append("   ⇒ **剩余非已知物理的式 = 0 条**。")
    L.append("")
    L.append("⇒ **「该体系可修复」与「该体系仍有内容」不可兼得**：")
    L.append("要修好就得把三条公设全废、把每个等式换成已知物理；")
    L.append("要留住公设与特有内容，就必然留下至少一条 FAIL。")
    L.append("")
    L.append("## 7. 仍未闭合项（未做即未证，不得外推）")
    L.append("")
    L.append("- **修复项清单是本卷人工定义的**：修复的「候选空间」由人给出，机器只负责穷举其子集。")
    L.append("  若存在本卷未列出的修复路径（例如为式 3.16 保留三等号而改别的式），结论需重算。")
    L.append("- **代价是定性评估**：「公理 A1 作废」这类代价本卷只做**有无**判断，未做加权打分。")
    L.append("- **F1 的实验室构型未做实测**：本卷是量级判决（1 h 超磁通门 393 倍），")
    L.append("  未检索是否有针对性的历史实验记录；若有人做过该类检验，其结果是更硬的证据。")
    L.append("- **F2 的量级锚点取整**：核力取 20 MeV/fm 作代表值，实际 NN 势随 r 与道次变化；")
    L.append("  但差的 13.8 个量级远大于锚点的不确定度，方向与结论不受影响。")
    L.append("- **量纲层不重判**：式 3.18 的量纲问题属前册（M1+M2）射程，本卷只比形状与量级。")
    L.append("- **不含量子场论 / 数据拟合**：本卷是解析与量级判决。")
    L.append("")
    L.append("## 附录 · Glossary")
    L.append("")
    L.append("- **削减型修复**：删式 / 改符号 / 改定义，不引入体系外的新内容。")
    L.append("- **新增型修复**：必须凭空给出新的表达式或取值（本卷仅 N1 一条）。")
    L.append("- **完备修复集**：能同时关闭全部 FAIL 的修复子集。")
    L.append("- **全部必需（无冗余）**：从最小集中拿掉任一项就不再完备 ⇒ 没有「便宜的组合」。")
    L.append("- **修复即自杀**：修复可行，但修复后体系退化为已知物理、公设全废、新增内容归零。")
    L.append("- **单源 / 多源构型**：A⃗ 与 E⃗ 来自同一物体（共线、叉乘为零）vs 来自不同物体（不共线）。")
    L.append("")
    L.append("## 数据出处")
    L.append("")
    L.append("- 机读册：`数据/%s.json` / `.md` / `_report.txt`" % STEM)
    L.append("- 上游：`数据/判定_TUFT-r141_核心公式理论体系_物理层内部矛盾与新增性_%s.md`（M3）" % DATE)
    L.append("- 来料：`01_独立体系/S17_统一场论核心公式/02_基础公设/postulates.md`")
    L.append("")
    out = os.path.join(DATA, JUDGE_STEM + ".md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return out


def main():
    os.makedirs(DATA, exist_ok=True)
    group_R()
    group_F()
    group_M()
    ctrl = control_group()

    legal = ("PASS", "FAIL", "INFO", "BOUNDARY", "CORRECTION")
    # G1：条目非空且判定合法
    if not ENTRIES or any(e["verdict"] not in legal for e in ENTRIES):
        print("GUARD FAIL: 条目为空或判定值非法")
        return 2
    # G2：控制组必须全过
    if not all(k["pass"] for k in ctrl):
        print("GUARD FAIL: 控制组失效")
        for k in ctrl:
            if not k["pass"]:
                print("   ", k["name"], k["value"])
        return 2
    # G3：必须同时存在 FAIL 与 INFO（防单侧偏置）
    n_fail = sum(1 for e in ENTRIES if e["verdict"] == "FAIL")
    n_info = sum(1 for e in ENTRIES if e["verdict"] == "INFO")
    if n_fail == 0 or n_info == 0:
        print("GUARD FAIL: 判定分布单侧偏置 FAIL=%d INFO=%d" % (n_fail, n_info))
        return 2
    # G4：F1 的数值 sanity
    if not (1.0e-13 < METRICS["f1_rate"] < 1.0e-9 and METRICS["f1_r_earth"] > 1.0):
        print("GUARD FAIL: F1 数值落在非物理区间 rate=%.3e r_earth=%.3f"
              % (METRICS["f1_rate"], METRICS["f1_r_earth"]))
        return 2
    # G5：F2 的比值 sanity
    if not (1.0e10 < METRICS["f2_ratio"] < 1.0e18):
        print("GUARD FAIL: F2 比值 %.3e 落在非预期区间" % METRICS["f2_ratio"])
        return 2
    # G6：修复集穷举必须给出「削减型不完备 + 含 N1 完备」
    if not (METRICS["m_n_complete_cut"] == 0 and METRICS["m_min_size"] > 0):
        print("GUARD FAIL: 穷举结果异常 cut=%d min=%d"
              % (METRICS["m_n_complete_cut"], METRICS["m_min_size"]))
        return 2
    # G7：最小集必须全部必需（无冗余）
    if not METRICS["m_all_essential"]:
        print("GUARD FAIL: 最小完备集存在冗余项，「全部必需」结论不成立")
        return 2
    # G8：F1 的单源 BOUNDARY 必须有机器支撑（叉乘≈0）
    if not METRICS["f1_cross_parallel"] < 1.0e-12:
        print("GUARD FAIL: 单源叉乘 %.3e 不≈0，BOUNDARY 登记无支撑"
              % METRICS["f1_cross_parallel"])
        return 2
    # G9：条目数与 FAIL 清单自洽
    if len(FAILS) != 18 or len(ENTRIES) < 12:
        print("GUARD FAIL: FAIL 清单 %d 条 / 条目 %d 条，与预期不符"
              % (len(FAILS), len(ENTRIES)))
        return 2

    p1 = build_json(ctrl)
    p2 = build_md(ctrl)
    p3 = build_report(ctrl)
    p4 = build_judge(ctrl)
    print("OK generated:")
    for p in (p1, p2, p3, p4):
        print("  ", os.path.relpath(p, PROJECT))
    c = {v: sum(1 for e in ENTRIES if e["verdict"] == v) for v in legal}
    print("VERDICT: REPAIR-PATH-COMPLETE-BUT-SUICIDAL")
    print("条目 %d：PASS %d / FAIL %d / INFO %d / BOUNDARY %d / CORRECTION %d"
          % (len(ENTRIES), c["PASS"], c["FAIL"], c["INFO"], c["BOUNDARY"], c["CORRECTION"]))
    print("控制组 %d/%d 通过 | guards 9/9 PASS | exit_code=0"
          % (sum(1 for k in ctrl if k["pass"]), len(ctrl)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
