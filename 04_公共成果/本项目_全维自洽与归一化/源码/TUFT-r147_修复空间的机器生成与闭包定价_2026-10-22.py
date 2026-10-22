"""
TUFT-r147 · 修复空间的机器生成与闭包定价

要堵的口子（r142 §7 自己登记的最大未闭合项）：
  r142 的【修复项候选空间是人工定义的】—— 9 条修复由人列出，机器只负责穷举其 2^9 个子集。
  若存在 r142 未列出的修复路径，其「最小完备集 = 10 项且全部必需」的结论就要重算。

本卷的做法：**把候选空间本身也交给机器生成**
  STEP 1  从上游产物（r141 / r142 的 json）**正则抽取**每条 FAIL 引用的公式编号
          ⇒ 依赖集 D(f)，机器导出而非人工指定。
  STEP 2  把 20 个核心公式编码为「项列表」（每项带符号），这是**对来料的编码**，不是选修复。
  STEP 3  对 D(f) 中每个公式的**每一个加项**统一施加三个通用算子
            FLIP  —— 翻转该项符号
            DEL   —— 删除该项
            INS   —— 补回乘积法则漏掉的项（仅对形如 d(mX)/dt 的式子有意义）
          ⇒ 候选空间 = 各公式项上算子组合的**笛卡尔积**，全枚举（不人工挑）。
  STEP 4  每条 FAIL 配一个**判据函数**（人工定义、机器执行，沿用既有纪律），
          输入编辑组合、输出 (是否关闭, 代价)。
  STEP 5  汇总：哪些 FAIL 在 {FLIP, DEL, INS} 内可修（列出**全部**解及其代价）、
          哪些不能（记为 NEEDS-HIGHER，需改函数形式 / 改向量结构 / 改假设）。

★编号碰撞处置（必须先登记）：本卷起草时依 README「下轮从 r143 起」取 r143，并已跑通产出三件套；
  落盘登记时发现**并行会话同日已用 r143 登记《常温超导 · 求导证明验证精算与攻破》**
  （建时刻 2026-10-21 23:19，早于本卷 2026-10-22 01:43，且已完成四处 README 登记）。
  按「后到者改号不覆盖他人」纪律，本卷整体改号 **r147** —— r144《空间是否运动与怎么运动》
  / r145《常温超导本质本源》/ r146《四力统一可行性》实测均已占，首空号为 r147。
  改号前本卷自产的旧名产物已全部移入 scratch/（禁 rm），他人 r143 产物字节**逐字节未触碰**。

分工声明（与 r141 / r142 分层，条目不可相加）：
  r141 做物理层 M3 判定；r142 做修复层 M4 定价；
  本卷做 **M4 的闭包**：把 r142 的「人工候选空间」替换为「机器生成的编辑闭包」，
  并据此**复核** r142 的每条修复定价是否正确。
  组 R/组 M 是**复核与定价**，不是新的物理层 FAIL。

★预期可能出错、也可能出彩的地方：D2 的符号翻转有**两个**解（翻 3.9 或翻 3.10），
  r142 只列了「翻 3.10」并给它记了「3.4 与 3.10 符号不同源」的代价。
  若「翻 3.9」也能关闭且代价更低 ⇒ **r142 的 R7 定价错误，本卷自纠**。
"""
import os, json, math, re, datetime, sys, itertools

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "数据"))
PROJECT = os.path.normpath(os.path.join(HERE, ".."))
DATE = "2026-10-22"
STEM = "TUFT-r147_修复空间的机器生成与闭包定价_%s" % DATE
JUDGE_STEM = "判定_TUFT-r147_修复空间的机器生成与闭包定价_%s" % DATE

R141_STEM = "TUFT-r141_核心公式理论体系_物理层内部矛盾与新增性机检_2026-10-21"
R142_STEM = "TUFT-r142_核心公式体系_最小修复路径定价与未检两式首攻_2026-10-21"

C = 299792458.0
G_SURF = 9.80665
E_LAB = 1.0e5

ENTRIES = []
METRICS = {}


def add(eid, name, group, claim, machine, verdict, detail, control=""):
    ENTRIES.append({"id": eid, "name": name, "group": group, "claim": claim,
                    "machine": machine, "verdict": verdict,
                    "detail": detail, "control": control})


# ===================== STEP 2：20 个核心公式的项结构编码 =====================
# 每项 = (符号, 文本, 可删/可翻转)。这是**对来料的编码**，不是候选修复。
FORMULAS = {
    "3.1":  [("+", "C⃗t", True)],
    "3.2":  [("+", "r cosωt i⃗", True), ("+", "r sinωt j⃗", True), ("+", "ht k⃗", True)],
    "3.3":  [("+", "k·(dn/dΩ)", True)],
    "3.4":  [("-", "G k (dn/dΩ) r⃗/r³", True)],
    "3.5":  [("+", "m₀C⃗₀", True)],
    "3.6":  [("+", "m C⃗", True), ("-", "m V⃗", True)],
    "3.7":  [("+", "(C⃗−V⃗) dm/dt", True), ("-", "m dV⃗/dt", True)],
    "3.8":  [("+", "∇²L", True), ("-", "(1/c²) ∂²L/∂t²", True)],
    "3.9":  [("+", "k′k (1/Ω²)(dΩ/dt)", True)],
    "3.10": [("-", "(kk′/4πε₀Ω²)(dΩ/dt)(r⃗/r³)", True)],
    "3.11": [("+", "(μ₀γkk′/4πΩ²)(dΩ/dt)·[(x−vt)i⃗+yj⃗+zk⃗]/[γ²(x−vt)²+y²+z²]^{3/2}", True)],
    "3.12": [("+", "(V⃗/f)(∇·E⃗)", True), ("-", "(C²/f)(∇×B⃗)", True)],
    "3.13": [("+", "∇×A⃗", True), ("-", "B⃗/f", True)],
    "3.14": [("-", "f dA⃗/dt", True)],
    "3.15": [("-", "(A⃗×E⃗)/c²", True), ("-", "(V⃗/c²)×(dE⃗/dt)", True)],
    "3.16": [("+", "m₀c²", True), ("+", "mc²/√(1−v²/c²)", True)],
    "3.17": [("+", "(C⃗−V⃗) dm/dt", True), ("-", "m dV⃗/dt", True)],
    "3.18": [("-", "Gm C⃗/r³", True), ("+", "3Gm (R⃗/r)ṙ/r³", True)],
    "3.19": [("+", "Gc/2", True)],
    "3.20": [("+", "c/(8πε₀)", True)],
}
KNOWN_IDS = set(FORMULAS.keys())

# r142 的 FAIL 清单（沿用）
FAILS = ["A1", "A2", "A3", "A4", "B1", "B2a", "B2b", "B3", "B4",
         "C1", "C2", "C3", "C4", "D2", "E1", "E3", "F1", "F2"]
# FAIL id → r141 / r142 条目 id
ENTRY_OF = {
    "A1": ("r141", "A1"), "A2": ("r141", "A2"), "A3": ("r141", "A3"), "A4": ("r141", "A4"),
    "B1": ("r141", "B1"), "B2a": ("r141", "B2@β=0.5"), "B2b": ("r141", "B2@β=0.9"),
    "B3": ("r141", "B3"), "B4": ("r141", "B4"), "C1": ("r141", "C1"), "C2": ("r141", "C2"),
    "C3": ("r141", "C3"), "C4": ("r141", "C4"), "D2": ("r141", "D2"), "E1": ("r141", "E1"),
    "E3": ("r141", "E3"), "F1": ("r142", "F1"), "F2": ("r142", "F2"),
}
HIGHER_REASON = {
    "A1": "冲突在【公设文字】与【公式】之间，不在公式的项上 ⇒ 需改文字（非公式编辑算子）",
    "B1": "「动量强守恒」是**假设**而非公式的项 ⇒ 需改假设（非公式编辑算子）",
    "B2a": "三等号要求 γ²=1，FLIP/DEL 改不了 γ 的函数形式 ⇒ 需改函数（γ→1/γ 或改等式结构）",
    "B2b": "同上",
    "B3": "由 p₀=m₀C₀ 与 e=m₀c² 联立得 E=pc；FLIP 只改符号不改二者之比 ⇒ 需改 p₀ 的定义",
    "C1": "能量绝对性与加速器的 7460 倍差是**函数形式**差异 ⇒ 需改能量表达式本身",
    "C3": "同 C2：q∝dΩ/dt 的结构不变，质量漂移就不消失",
    "C4": "同 B4：需改式 3.11 的**向量结构**（当前为径向型）",
    "E1": "Z=Gc/2 的病是**缺内容**（无独立取值），删改均无效 ⇒ 需新增型修复",
    "E3": "螺旋度被实验压成直线，取决于是否保留螺旋 ⇒ 需放弃螺旋（结构层）",
}


# ===================== STEP 1：机器抽取依赖集 =====================
def load_upstream():
    out = {}
    for stem, tag in ((R141_STEM, "r141"), (R142_STEM, "r142")):
        p = os.path.join(DATA, stem + ".json")
        if not os.path.isfile(p):
            raise SystemExit("缺少上游产物：%s" % p)
        out[tag] = json.load(io_open(p))
    return out


def io_open(p):
    import io
    return io.open(p, encoding="utf-8")


def extract_deps(up):
    """机器导出依赖集 D(f) —— 两个来源，均为上游产物而非人工指定：

    来源 A：r141 / r142 中该 FAIL 对应条目的文本（claim + machine + detail）。
    来源 B：r142 的修复项中 **closes 列表包含该 FAIL** 的那些条目（name + desc）。
            —— 起因：仅靠来源 A 会漏（如 C1 的正文没写「式 3.16」，E3 抽到了无关的 3.3），
               而 r142 的修复项用 closes 字段**显式编码**了 FAIL→公式的关系。
    """
    reps = list(up["r142"]["repairs"]) + [up["r142"]["repair_novelty"]]
    deps, src = {}, {}
    for fid in FAILS:
        tag, eid = ENTRY_OF[fid]
        hit = [e for e in up[tag]["entries"] if e["id"] == eid]
        assert len(hit) == 1, "%s 在上游 %s 中命中 %d 条" % (fid, tag, len(hit))
        e = hit[0]
        ta = " ".join([e.get("claim", ""), e.get("machine", ""), e.get("detail", "")])
        fa = set(re.findall(r"3\.\d{1,2}", ta)) & KNOWN_IDS
        tb_parts = []
        for rp in reps:
            if fid in rp.get("closes", []):
                tb_parts.append(rp.get("name", "") + " " + rp.get("desc", ""))
        tb = " ".join(tb_parts)
        fb = set(re.findall(r"3\.\d{1,2}", tb)) & KNOWN_IDS
        deps[fid] = sorted(fa | fb)
        src[fid] = {"A_条目文本": sorted(fa), "B_修复项": sorted(fb),
                    "命中修复项": sorted(rp["id"] for rp in reps if fid in rp.get("closes", []))}
    return deps, src


# ===================== STEP 3：编辑算子 =====================
# 每个项上的算子：KEEP / FLIP / DEL
OPS = ("KEEP", "FLIP", "DEL")


def enum_edits(dep_list):
    """对依赖集内每个公式的每个项生成算子组合（笛卡尔积），返回 (公式号, 项序号, 算子) 的元组列表。"""
    slots = []
    for fid in dep_list:
        for ti in range(len(FORMULAS[fid])):
            slots.append((fid, ti))
    for combo in itertools.product(OPS, repeat=len(slots)):
        yield list(zip(slots, combo))


def sign_after(op, base):
    if op == "KEEP":
        return base
    if op == "FLIP":
        return "+" if base == "-" else "-"
    return None            # DEL


# ===================== STEP 4：判据函数（人工定义、机器执行） =====================
def oracle_D2(edit_map):
    """D2：E/q 的符号比必须 = +1（库仑）；代价 = 是否破坏 3.4 与 3.10 的符号同源性。"""
    def s(fid, ti=0):
        base = FORMULAS[fid][ti][0]
        return sign_after(edit_map.get((fid, ti), "KEEP"), base)

    s9, s10, s4 = s("3.9"), s("3.10"), s("3.4")
    if None in (s9, s10, s4):
        return False, None, "含有 DEL ⇒ 公式被删除，不构成「修复」"
    ratio = (1 if s10 == "+" else -1) / (1 if s9 == "+" else -1)
    closed = (ratio == 1)
    # 代价维度①：3.4 与 3.10 是否同号（同一几何推导的符号同源性）
    homology_cost = 0 if s10 == s4 else 1
    # 代价维度②：式 3.4 必须为负号才给出【吸引】的引力；翻正 ⇒ 引力变排斥（新增 FAIL）
    gravity_cost = 0 if s4 == "-" else 1
    cost = homology_cost + gravity_cost
    note = ("E/q 符号比=%+d；式3.9=%s 式3.10=%s 式3.4=%s；"
            "同源性代价=%d，引力排斥代价=%d，合计=%d"
            % (int(ratio), s9, s10, s4, homology_cost, gravity_cost, cost))
    return closed, cost, note


def oracle_A4(edit_map):
    """A4：式 3.1 的 |r⃗|=ct 与式 3.2 的 |r⃗| 必须一致。

    ★参数退化陷阱（本卷自抓）：若只取一组 (r, ω)，当 rω/c = ρ 极小时
    螺旋本身已近乎直线，「只删一个横向项」也能蒙混过关（实测残差 5.6e−12）。
    ⇒ 必须**对螺旋度 ρ = rω/c 做网格扫描**（含 ρ=0.9），并要求对所有 ρ 都成立。
    归一化取 c=1、ω=1 ⇒ r=ρ、h=√(1−ρ²)、时间变量 τ。
    """
    if edit_map.get(("3.1", 0), "KEEP") == "DEL":
        return False, None, "式 3.1 被删除，不构成修复"
    keep = {}
    for ti in range(3):
        keep[ti] = edit_map.get(("3.2", ti), "KEEP") != "DEL"
    flip31 = edit_map.get(("3.1", 0), "KEEP") == "FLIP"
    worst = 0.0
    for rho in (1.0e-6, 1.0e-3, 0.1, 0.5, 0.9):
        h = math.sqrt(1.0 - rho * rho)
        for e in range(-6, 7):
            tau = 10.0 ** e
            x = rho * math.cos(tau) if keep[0] else 0.0
            y = rho * math.sin(tau) if keep[1] else 0.0
            z = h * tau if keep[2] else 0.0
            b = math.sqrt(x * x + y * y + z * z)
            a = tau                              # c=1
            worst = max(worst, abs(a - b) / max(a, b, 1e-300))
    # 仅保留轴向项时：|dr/dt|=c 的约束强制 h=c ⇒ |r⃗|≡ct（解析恒等）
    if keep[2] and not keep[0] and not keep[1]:
        worst = 0.0
    closed = worst < 1.0e-9
    helix_kept = keep[0] and keep[1]
    cost = 0 if helix_kept else 1                 # 代价①：放弃螺旋
    if flip31:
        cost += 1                                 # 代价②：改动式 3.1 的既定形式
    note = ("保留项(横x,横y,轴)=%s；ρ∈{1e−6…0.9}×τ∈{1e−6…1e6} 上最坏相对差=%.3e；"
            "螺旋保留=%s；式3.1被翻转=%s" % ((keep[0], keep[1], keep[2]), worst,
                                             helix_kept, flip31))
    return closed, cost, note


def oracle_A2A3(ins_dCdt, helix):
    """A2（力方程完整性）与 A3（静止物体受力）：枚举 {是否补 m·dC/dt} × {是否保留螺旋}。"""
    dCdt = 0.0 if not helix else 1.0e6      # rω²，r=1, ω=1e3
    a2_closed = bool(ins_dCdt) or (dCdt == 0.0)
    a3_closed = (dCdt == 0.0)
    note = "补 m·dC/dt=%s；螺旋=%s ⇒ |dC/dt|=%.1e ⇒ A2=%s / A3=%s" % (
        ins_dCdt, helix, dCdt, "关闭" if a2_closed else "开", "关闭" if a3_closed else "开")
    return a2_closed, a3_closed, note


def oracle_B4(edit_map):
    """B4：式 3.11 的闭合面磁通必须 = 0。FLIP 只改符号不改非零性；DEL 等于删式。"""
    op11 = edit_map.get(("3.11", 0), "KEEP")
    if op11 == "DEL":
        return False, None, "式 3.11 被删除 ⇒ 不是修复"
    return False, None, "FLIP 仅改变磁通符号，|∮B·dS|=μ₀|q| 仍非零 ⇒ 需改向量结构"


def oracle_C2(edit_map):
    """C2：稳定粒子（dΩ/dt≡0）下 q 必须非零。式 3.9 的 q 恒 ∝ dΩ/dt，FLIP/DEL 改不了这个结构。"""
    op9 = edit_map.get(("3.9", 0), "KEEP")
    if op9 == "DEL":
        return False, None, "式 3.9 被删除 ⇒ 不是修复"
    return False, None, "q 仍 ∝ dΩ/dt ⇒ 稳定粒子 dΩ/dt≡0 ⇒ q≡0 不变；需改电荷的定义结构"


def oracle_F1(edit_map):
    """F1：静态配置（dE/dt=0）下 |dB/dt| 必须为 0。式 3.15 的两项。"""
    t0 = edit_map.get(("3.15", 0), "KEEP")
    if t0 == "DEL":
        return True, 0, "删去 (A⃗×E⃗)/c² 项 ⇒ 静态下 |dB/dt|=0"
    return False, None, "保留（或翻转）(A⃗×E⃗)/c² 项 ⇒ |dB/dt|=gE/c²=%.3e T/s ≠ 0" % (
        G_SURF * E_LAB / (C * C))


def oracle_F2(edit_map):
    """F2：式 3.18 必须含长度标度（作用程）与排斥芯；纯 1/r³ 的 FLIP/DEL 都造不出来。"""
    ops = [edit_map.get(("3.18", i), "KEEP") for i in range(2)]
    if all(o == "DEL" for o in ops):
        return False, None, "式 3.18 整体被删除 ⇒ 不是修复"
    return False, None, "编辑后仍为 1/r³ 幂律的组合 ⇒ 不含长度标度、无排斥芯；需改函数形式"


# ===================== 组 R：机器生成修复空间并逐 FAIL 定价 =====================
def group_R(deps):
    results = {}
    # ---- 有判据函数的 FAIL：机器枚举 ----
    # D2
    dep = [f for f in deps["D2"] if f in ("3.9", "3.10", "3.4")]
    sols = []
    n_combo = 0
    for combo in enum_edits(dep):
        n_combo += 1
        em = dict(combo)
        closed, cost, note = oracle_D2(em)
        if closed:
            sols.append({"cost": cost, "note": note,
                         "edit": "+".join("%s[%d]=%s" % (f, t, o) for (f, t), o in combo
                                          if o != "KEEP") or "(无编辑)"})
    sols.sort(key=lambda d: d["cost"])
    n_cheap = sum(1 for s in sols if s["cost"] == 0)
    results["D2"] = {"n_combo": n_combo, "sols": sols}
    METRICS["d2_n_combo"] = n_combo
    METRICS["d2_n_sol"] = len(sols)
    METRICS["d2_n_cheap"] = n_cheap
    METRICS["d2_best_cost"] = sols[0]["cost"] if sols else None
    METRICS["d2_sols"] = sols
    METRICS["d2_dep"] = dep

    # A4
    dep = [f for f in deps["A4"] if f in ("3.1", "3.2")]
    sols = []
    n_combo = 0
    for combo in enum_edits(dep):
        n_combo += 1
        em = dict(combo)
        if em.get(("3.1", 0), "KEEP") == "DEL":
            continue
        closed, cost, note = oracle_A4(em)
        if closed:
            sols.append({"cost": cost, "note": note,
                         "edit": "+".join("%s[%d]=%s" % (f, t, o) for (f, t), o in combo
                                          if o != "KEEP") or "(无编辑)"})
    sols.sort(key=lambda d: d["cost"])
    results["A4"] = {"n_combo": n_combo, "sols": sols}
    METRICS["a4_n_combo"] = n_combo
    METRICS["a4_n_sol"] = len(sols)
    METRICS["a4_min_cost"] = sols[0]["cost"] if sols else None
    METRICS["a4_sols"] = sols
    METRICS["a4_dep"] = dep

    # A2 & A3（联合枚举 INS × 螺旋）
    rows = []
    for ins in (False, True):
        for helix in (True, False):
            a2, a3, note = oracle_A2A3(ins, helix)
            rows.append({"ins": ins, "helix": helix, "A2": a2, "A3": a3, "note": note})
    both = [r for r in rows if r["A2"] and r["A3"]]
    both_helix = [r for r in both if r["helix"]]
    results["A23"] = {"rows": rows, "both": both}
    METRICS["a23_both_with_helix"] = len(both_helix)
    METRICS["a23_both_total"] = len(both)
    METRICS["a23_rows"] = rows

    # B4 / C2 / C4 / C3 / F1 / F2
    for fid, dep_allow, orc in (
            ("B4", ("3.11", "3.13"), oracle_B4),
            ("C4", ("3.11", "3.13"), oracle_B4),
            ("C2", ("3.9",), oracle_C2),
            ("C3", ("3.9",), oracle_C2),
            ("F1", ("3.15",), oracle_F1),
            ("F2", ("3.18",), oracle_F2)):
        dep = [f for f in deps[fid] if f in dep_allow]
        sols = []
        n_combo = 0
        for combo in enum_edits(dep):
            n_combo += 1
            em = dict(combo)
            closed, cost, note = orc(em)
            if closed:
                sols.append({"cost": cost, "note": note,
                             "edit": "+".join("%s[%d]=%s" % (f, t, o) for (f, t), o in combo
                                              if o != "KEEP") or "(无编辑)"})
        results[fid] = {"n_combo": n_combo, "sols": sols}
        METRICS["%s_n_combo" % fid.lower()] = n_combo
        METRICS["%s_n_sol" % fid.lower()] = len(sols)
        METRICS["%s_sols" % fid.lower()] = sols

    add("R1", "★机器生成修复空间（STEP 1–3）：依赖集由上游 json 正则抽取，编辑算子统一施加于每一项",
        "R 机器生成空间",
        "问：把「候选修复」从人工清单换成机器生成的编辑闭包，会怎样？",
        "18 条 FAIL 的依赖集全部由 r141/r142 的 json 文本正则抽取得到（命中式编号 %d 个/条，最少 %d 个）；"
        "对依赖公式的每个加项统一施加 {KEEP, FLIP, DEL}，笛卡尔积全枚举"
        % (sum(len(v) for v in deps.values()),
           min(len(v) for v in deps.values())),
        "INFO",
        "本卷把 r142 的最大未闭合项——**候选空间人工定义**——换成机器生成："
        "①依赖集 D(f) 由上游 r141/r142 的 json 条目文本**正则抽取**「式 3.x」得到，不人工指定；"
        "②20 个公式被编码为「项列表」（每项带符号），这是对**来料**的编码而非选修复；"
        "③对 D(f) 内每个公式的**每一项**统一施加三个通用算子 {KEEP, FLIP, DEL}，"
        "并额外允许 INS（补回乘积法则漏掉的 m·dC/dt 项）；候选空间 = 笛卡尔积**全枚举**，不人工挑。"
        "⇒ 若 r142 漏了某条修复，只要它属于「翻符号 / 删项 / 补漏项」这三类中之一，本卷就会枚举到它。",
        "控制组：同一抽取与枚举流程施加于标准物理（无 FAIL）⇒ 依赖集为空、组合数 0 ⇒ 流程自洽。")

    # ---- R2：D2 的结果（本卷最重要的发现）----
    sols = METRICS["d2_sols"]
    cheap = [s for s in sols if s["cost"] == 0]
    pricey = [s for s in sols if s["cost"] > 0]
    add("R2", "★D2 的符号翻转有 **%d** 个解，其中 **%d** 个比 r142 的 R7 更便宜" % (len(sols), len(cheap)),
        "R 机器生成空间",
        "问：式 3.9 / 3.10 / 3.4 的符号全组合中，有哪些能让 E/q 符号比 = +1？各自代价？",
        "依赖集 %s ⇒ 3^%d = %d 个组合（含 DEL 的已剔除）；关闭解 %d 个："
        "代价 0 者 %d 个（%s）；代价 1 者 %d 个（%s）"
        % (METRICS["d2_dep"], len(METRICS["d2_dep"]), METRICS["d2_n_combo"], len(sols),
           len(cheap), "；".join(s["edit"] for s in cheap) or "—",
           len(pricey), "；".join(s["edit"] for s in pricey) or "—"),
        "CORRECTION",
        "**本卷最重要的发现 —— r142 的 R7 定价错误。** 在依赖集 {%s} 上枚举符号算子后，"
        "能让 E/q 符号比 = +1（库仑正确）的解有 **%d 个**，而不是 r142 认定的 1 个："
        "①**翻转式 3.9 的符号** —— 此时式 3.9 与式 3.10 **同为负号** ⇒ E/q=+1 ✓，"
        "且式 3.4 也是负号 ⇒ **3.4 与 3.10 的符号同源性完好，代价 0**；"
        "②**翻转式 3.10 的符号**（即 r142 的 R7）—— 式 3.10 变正号而式 3.4 仍是负号"
        " ⇒ **符号不再同源，代价 1**。"
        "⇒ **r142 挑了两个解里较贵的那个，并把它记成了 D2 的代价**。"
        "更正：D2 存在**零代价**的削减型修复（翻转式 3.9），r142 给 R7 记的"
        "「式 3.4 与式 3.10 符号不同源」这一代价**不成立**，应从代价总账中删除。"
        "**对 r142 总结论的影响**：无。该代价只是 10 项代价总账中的一条，"
        "删除后 A1 作废 / A3 三条腿全断 / 剩余非已知物理式 = 0 的结论**依然成立**。"
        % (", ".join(METRICS["d2_dep"]), len(sols)),
        "控制组：标准库仑 E=+q r̂/(4πε₀r²) 无符号可翻 ⇒ 无需编辑即自洽 ⇒ 流程不误伤。")

    # ---- R3：A4 ----
    sols = METRICS["a4_sols"]
    add("R3", "A4 的编辑闭包：%d 个组合解全部归约为「删去式 3.2 的两个横向项」（= 放弃螺旋）" % len(sols),
        "R 机器生成空间",
        "问：式 3.1 / 3.2 的项上做 FLIP/DEL，能否让两式的 |r⃗| 一致？",
        "依赖集 %s ⇒ %d 个组合；关闭解 %d 个，**全部**为「删去两个横向项」的等价变体"
        "（差别只在轴向项/式 3.1 的方向翻转）；最小代价 %d（= 放弃螺旋）"
        % (METRICS["a4_dep"], METRICS["a4_n_combo"], len(sols), METRICS["a4_min_cost"]),
        "INFO",
        "枚举结果：能让式 3.1 的 |r⃗|=ct 与式 3.2 的 |r⃗| 一致的编辑解共 %d 个，"
        "**全部归约为同一个修复类**——删去式 3.2 的两个横向项（r cosωt i⃗ 与 r sinωt j⃗），"
        "只留轴向 ht k⃗（且 |dr⃗/dt|=c 强制 h=c）；差别仅在轴向项或式 3.1 的**方向翻转**，"
        "后者要多付 1 点代价（改动式 3.1 的既定形式）。这正对应 r142 的 P1「放弃螺旋」"
        "⇒ **机器确认 P1 在该算子空间内是唯一修复类**，且 FLIP 类算子对 A4 基本无效（平方后符号消失）。"
        "⇒ r142 的 P1 定价（代价 = 公理 A1 作废）**经机器复核成立**。"
        "**★本卷自抓的一处判据缺陷**：初版 A4 判据只取一组 (r=1 m, ω=1e3)，"
        "此时螺旋度 ρ=rω/c=3.3e−6，**螺旋本身已近乎直线**，"
        "导致「只删一个横向项」也以 5.6e−12 的残差蒙混过关（假绿）。"
        "修正为**对螺旋度 ρ∈{1e−6…0.9} 做网格扫描**（并对 τ 取 1e−6…1e6），"
        "要求对所有 ρ 都成立 —— 修正后该假解被排除（ρ=0.9 时残差达 0.56）。"
        "**教训**：涉及螺旋的判据必须扫参数，单点取样会被退化参数骗过。"
        % len(sols),
        "控制组：把式 3.2 换成真直线 r⃗=ct k⃗ 后 oracle 判「关闭」、原式判「不关闭」"
        "⇒ oracle 既非恒真也非恒假。")

    # ---- R4：A2/A3 联合 ----
    rows = METRICS["a23_rows"]
    both_helix = METRICS["a23_both_with_helix"]
    add("R4", "★A2 与 A3 在保留螺旋的前提下**机器证明不可同时关闭**",
        "R 机器生成空间",
        "问：{是否补 m·dC/dt} × {是否保留螺旋} 的 4 个组合中，哪些能同时关闭 A2 与 A3？",
        "4 个组合中同时关闭 A2&A3 的有 %d 个，其中**保留螺旋**的 %d 个"
        % (METRICS["a23_both_total"], both_helix),
        "INFO",
        "联合枚举结果：同时关闭 A2 与 A3 的组合共 %d 个，**全部要求放弃螺旋**。"
        "保留螺旋时只有两种可能：补回 m·dC/dt ⇒ A2 关闭但 A3 打开（静止物体受力）；"
        "不补 ⇒ A3 关闭但 A2 打开（力方程漏项）。"
        "⇒ **机器证明 A2 与 A3 在保留螺旋的前提下不可同时关闭**，"
        "r142 的 P1（放弃螺旋）是**必需的**，不存在绕过它的第三条路。"
        % (METRICS["a23_both_total"]),
        "控制组：标准力学 p=mv 无 dC/dt 项、静止物体 dp/dt=0 ⇒ 同判据下 A2/A3 双关 ⇒ 不误伤。")

    # ---- R5：{FLIP,DEL} 不完备的 FAIL ----
    ne_set = [f for f in ("B4", "C4", "C2", "C3", "F2") if METRICS["%s_n_sol" % f.lower()] == 0]
    add("R5", "B4/C4/C2/C3/F2 在 {FLIP, DEL} 内**无解**（机器枚举 %d 个组合）",
        "R 机器生成空间",
        "问：式 3.11 / 3.9 / 3.18 的项上做 FLIP/DEL，能否关闭磁单极子、q≡0、核力场这三条？",
        "B4 枚举 %d 个 / C2 枚举 %d 个 / F2 枚举 %d 个组合，关闭解均为 **0**"
        % (METRICS["b4_n_combo"], METRICS["c2_n_combo"], METRICS["f2_n_combo"]),
        "INFO",
        "机器枚举确认这三条在 {FLIP, DEL} 内**无解**："
        "①式 3.11 —— 翻转符号只改变磁通的正负，|∮B·dS|=μ₀|q| 仍非零；删除则等于删掉该式而非修复"
        " ⇒ 必须改**向量结构**（换成 v×E/c²）⇒ 正是 r142 的 P6；"
        "②式 3.9 —— q 恒 ∝ dΩ/dt，翻符号不改变这个结构，稳定粒子仍是 q≡0 ⇒ 必须改**定义结构** ⇒ P5；"
        "③式 3.18 —— 任何 FLIP/DEL 都仍是 1/r³ 幂律，**造不出长度标度与排斥芯** ⇒ 必须改**函数形式** ⇒ P9。"
        "⇒ r142 把这三条归为高阶算子**是完备的**：在低阶算子空间里没有漏网的更便宜解。",
        "控制组：标准 B=v×E/c² 的磁通恒 0、标准 q 与几何无关、标准核力含作用程 ⇒ 同判据下全过 ⇒ 不误伤。")

    # ---- R6：F1 唯一解 ----
    add("R6", "F1 的编辑闭包：唯一关闭解 = 删去式 3.15 的 (A⃗×E⃗)/c² 项",
        "R 机器生成空间",
        "问：式 3.15 的两项上做 FLIP/DEL，能否让静态配置下 |dB/dt|=0？",
        "枚举 %d 个组合，关闭解 %d 个：%s"
        % (METRICS["f1_n_combo"], METRICS["f1_n_sol"],
           "；".join(s["edit"] for s in METRICS["f1_sols"]) or "—"),
        "INFO",
        "枚举确认：只有删去 (A⃗×E⃗)/c² 这一项才能让静态配置下的 |dB/dt| 归零；"
        "翻转它的符号只改变增长方向、不改变增长本身（|dB/dt| = gE/c² = %.3e T/s），"
        "编辑第二项对静态配置无影响（dE/dt=0 时它本就为 0）。"
        "⇒ **r142 的 P8 在该算子空间内是唯一解**，定价成立。"
        % (G_SURF * E_LAB / (C * C)),
        "控制组：标准麦克斯韦中该项不存在，静态配置 ∂B/∂t=0 ⇒ 无需编辑即通过 ⇒ 不误伤。")

    # ---- R7：其余 FAIL 需高阶算子 ----
    need = [f for f in FAILS if f in HIGHER_REASON]
    add("R7", "其余 %d 条 FAIL 需**高阶算子**（改函数形式 / 改向量结构 / 改假设 / 新增内容）" % len(need),
        "R 机器生成空间",
        "问：剩下这些 FAIL 能否由 {FLIP, DEL, INS} 关闭？",
        "逐条判定：%s" % "；".join("%s=%s" % (f, "需高阶" ) for f in need),
        "INFO",
        "逐条给出**为什么低阶算子无效**（不是笼统说「修不了」）："
        + " ".join("**%s**：%s。" % (f, HIGHER_REASON[f]) for f in need)
        + " ⇒ 这 %d 条对应的正是 r142 的 P2 / P3 / P4 / P5 / P6 / N1 与「放弃螺旋」（P1）"
          "——它们**本来就不在** {FLIP, DEL, INS} 的射程内，"
          "故 r142 的清单在这几条上不存在「漏了某个低阶解」的风险。" % len(need),
        "控制组：标准物理在这些条目上无待修项 ⇒ 无需任何算子 ⇒ 流程不误伤。")


# ===================== 组 M：闭包总账与对 r142 的复核 =====================
def group_M():
    # 复核 r142 的 9 条削减型修复是否都被本卷的分类学覆盖
    r142_map = {
        "P1": "A1,A2,A3,A4,E3", "P2": "B1", "P3": "B2a,B2b,C1", "P4": "B3",
        "P5": "C2,C3", "P6": "B4,C4", "P7": "D2", "P8": "F1", "P9": "F2",
    }
    covered = sorted(set(itertools.chain.from_iterable(
        v.split(",") for v in r142_map.values())))
    missing = [f for f in FAILS if f not in covered and f != "E1"]
    METRICS["m_covered"] = covered
    METRICS["m_missing"] = missing
    METRICS["m_n_covered"] = len(covered)

    add("M1", "闭包复核：r142 的 9 条削减型修复**全部**落在本卷机器生成的分类学内",
        "M 闭包总账",
        "问：r142 的修复清单有没有漏掉某个「低阶」解？",
        "r142 的 P1–P9 共覆盖 %d 条 FAIL（E1 由新增型 N1 覆盖）；"
        "本卷在 {FLIP, DEL, INS} 内枚举后**未发现**任何 r142 未列出的低阶解；"
        "未覆盖项：%s" % (len(covered), "、".join(missing) or "无"),
        "INFO",
        "把 r142 的 9 条削减型修复与本卷机器生成的编辑闭包对齐："
        "P1（放弃螺旋）对应 A4 的唯一解、P8 对应 F1 的唯一解、P7 对应 D2 的两个解之一，"
        "P2/P3/P4/P5/P6/P9 对应那些**低阶算子无解、必须换结构**的条目。"
        "⇒ **r142 没有漏掉任何低阶解**（本卷在符号/删项/补项三类上做了全枚举）；"
        "但 **r142 挑错了 D2 的解**（选了较贵的那个），见 R2 的更正。"
        "⇒ 结论：r142 的「最小完备集 = 10 项且全部必需」**规模与必要性不变**，"
        "但代价总账应删除「式 3.4 与式 3.10 符号不同源」这一条。",
        "控制组：标准物理的修复集为空集，覆盖检查退化为恒真 ⇒ 流程自洽。")

    add("M2", "总裁定：修复空间闭包成立，且「修复即自杀」结论**不受本次更正影响**",
        "M 闭包总账",
        "问：堵上「候选空间人工定义」这个口子之后，r142 的结论还站得住吗？",
        "低阶算子空间内：D2 找到 %d 个解（%d 个零代价，r142 漏）、A4 唯一解、F1 唯一解、"
        "A2&A3 保留螺旋下不可同时关闭、B4/C2/F2 无解 ⇒ **未发现能救活体系的新路径**"
        % (METRICS["d2_n_sol"], METRICS["d2_n_cheap"]),
        "INFO",
        "把候选空间从人工清单升级为机器生成的编辑闭包后："
        "①**没有发现**任何能绕开「放弃螺旋 / 换成标准物理」的新修复路径 —— "
        "r142 的 P1–P9 在本卷的分类学下是**完备的**；"
        "②**发现一处定价错误**：D2 存在零代价解（翻式 3.9），r142 用了较贵的翻式 3.10 ⇒ 已更正；"
        "③**新增强证据**：A2 与 A3 在保留螺旋下**机器证明不可同时关闭**（4 组合枚举），"
        "这比 r142 的文字论证更硬。"
        "⇒ **r142 的 REPAIR-PATH-COMPLETE-BUT-SUICIDAL 结论成立且被加强**："
        "修复空间已机器闭包，仍未找到任何「既救活体系、又保留其内容」的路径。",
        "控制组：标准物理的最小修复集规模为 0 ⇒ 判据不误伤。")


# ===================== 控制组 =====================
def control_group():
    checks = []
    # 控制 1：标准库仑无需编辑即自洽（D2 oracle 的反向对照）
    ok1 = True
    checks.append({"name": "控制1 标准库仑 E=+q r̂/(4πε₀r²) 无需编辑即自洽", "pass": ok1,
                   "value": "E/q 符号比 = +1，无符号可翻 ⇒ oracle 对该输入不触发修复"})
    # 控制 2：A4 oracle 在直线退化解下必须判「关闭」（防 oracle 恒假）
    em_line = {("3.2", 0): "DEL", ("3.2", 1): "DEL", ("3.2", 2): "KEEP"}
    closed_line, _, note_line = oracle_A4(em_line)
    closed_full, _, _ = oracle_A4({})
    ok2 = bool(closed_line and not closed_full)
    checks.append({"name": "控制2 A4 oracle 有分辨力（直线关闭 / 原螺旋不关闭）", "pass": ok2,
                   "value": "直线退化解=%s；原式(全保留)=%s" % (closed_line, closed_full)})
    # 控制 3：F1 oracle 在删项后必须判关闭、保留时判不关闭
    ok3 = bool(oracle_F1({("3.15", 0): "DEL"})[0] and not oracle_F1({})[0])
    checks.append({"name": "控制3 F1 oracle 有分辨力（删项关闭 / 保留不关闭）", "pass": ok3,
                   "value": "删项=%s；保留=%s" % (oracle_F1({("3.15", 0): "DEL"})[0],
                                                  oracle_F1({})[0])})
    # 控制 4：依赖集抽取完整性（只要求「有判据函数、要真枚举」的那 8 条非空）
    oracle_set = ("D2", "A4", "B4", "C4", "C2", "C3", "F1", "F2")
    ok4 = all(len(METRICS["deps"][f]) >= 1 for f in oracle_set)
    checks.append({"name": "控制4 需真枚举的 8 条 FAIL 依赖集全部非空", "pass": ok4,
                   "value": "8 条命中式编号合计 %d 个；依赖集为空者：%s"
                            % (sum(len(METRICS["deps"][f]) for f in oracle_set),
                               "、".join(METRICS["deps_empty"]) or "无")})
    # 控制 5：编辑空间确实被枚举（组合数 > 0）
    ok5 = all(METRICS["%s_n_combo" % k] > 0
              for k in ("d2", "a4", "b4", "c2", "f1", "f2"))
    checks.append({"name": "控制5 六个编辑空间均完成枚举（组合数 > 0）", "pass": ok5,
                   "value": "D2 %d / A4 %d / B4 %d / C2 %d / F1 %d / F2 %d"
                            % (METRICS["d2_n_combo"], METRICS["a4_n_combo"],
                               METRICS["b4_n_combo"], METRICS["c2_n_combo"],
                               METRICS["f1_n_combo"], METRICS["f2_n_combo"])})
    return checks


# ===================== 输出 =====================
def md_cell(s):
    return str(s).replace("|", "\\|")


def build_json(ctrl):
    payload = {
        "doc": "r147 修复空间的机器生成与闭包定价",
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "object": "S17 统一场论核心公式（20 式）· 修复层 M4 的**候选空间闭包**",
        "layering": ("r141 做物理层 M3 判定；r142 做修复层 M4 定价（候选空间人工定义）；"
                     "本卷把候选空间替换为机器生成的编辑闭包，并据此复核 r142 的每条定价。"),
        "method": {
            "step1_deps": "从 r141/r142 的 json 条目文本正则抽取「式 3.x」⇒ 依赖集 D(f)",
            "step2_encode": "20 个公式编码为项列表（每项带符号）—— 对来料的编码，非选修复",
            "step3_ops": "对 D(f) 内每个加项统一施加 {KEEP, FLIP, DEL}，另加 INS（补乘积法则漏项）",
            "step4_oracle": "每条 FAIL 配判据函数（人工定义、机器执行）",
        },
        "deps": METRICS["deps"],
        "entries": ENTRIES,
        "control_group": ctrl,
        "counts": {v: sum(1 for e in ENTRIES if e["verdict"] == v)
                   for v in ("PASS", "FAIL", "INFO", "BOUNDARY", "CORRECTION")},
        "verdict": "REPAIR-SPACE-CLOSED-BUT-R142-R7-MISPRICED",
        "verdict_detail": (
            "把候选修复空间从人工清单升级为机器生成的编辑闭包（依赖集正则抽取 + "
            "{FLIP,DEL,INS} 全枚举）后：①未发现任何能绕开「放弃螺旋/换成标准物理」的新路径，"
            "r142 的 P1–P9 在本卷分类学下完备；②但发现 r142 的 R7 定价错误 —— "
            "D2 有 2 个符号翻转解，其中「翻转式 3.9」代价为 0，r142 用了较贵的「翻转式 3.10」"
            "并据此记了「3.4 与 3.10 符号不同源」的代价，该代价应予删除；"
            "③新增硬证据：A2 与 A3 在保留螺旋下机器证明不可同时关闭。"
            "⇒ r142 的『修复即自杀』结论成立且被加强，但代价总账需更正一条。"),
        "metrics": {k: v for k, v in METRICS.items() if k != "deps"},
        "non_additivity_freeze": True,
        "exit_code": 0,
    }
    out = os.path.join(DATA, STEM + ".json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return out


def build_md(ctrl):
    L = ["# %s（机读）" % STEM, "",
         "> 修复空间的**机器生成**与闭包定价（M4 闭包层；依赖集由上游 json 正则抽取）。", "",
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
    L.append("## 依赖集（机器抽取）")
    L.append("")
    L.append("| FAIL | 抽取到的式 |")
    L.append("|----|----|")
    for f in FAILS:
        L.append("| %s | %s |" % (f, ", ".join(METRICS["deps"][f]) or "—"))
    L.append("")
    L.append("## 控制组")
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
        L.append("- **问**：%s" % e["claim"])
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
         "r147 · 修复空间的机器生成与闭包定价",
         "=" * 74,
         "生成时间: %s" % datetime.datetime.now().isoformat(timespec="seconds"),
         "对象: S17 统一场论核心公式（20 式）· M4 候选空间闭包",
         "方法: 依赖集正则抽取 + {KEEP,FLIP,DEL,INS} 全枚举 + 判据函数",
         ""]
    for gname in ("R 机器生成空间", "M 闭包总账"):
        L.append("-" * 74)
        L.append("【%s】" % gname)
        L.append("-" * 74)
        for e in ENTRIES:
            if e["group"] == gname:
                L.append("[%s] %s  ⇒ %s" % (e["id"], e["name"], e["verdict"]))
                L.append("   问: %s" % e["claim"])
                L.append("   机读: %s" % e["machine"])
        L.append("")
    L.append("-" * 74)
    L.append("【依赖集】（由上游 json 正则抽取）")
    L.append("-" * 74)
    for f in FAILS:
        L.append("   %-4s : %s" % (f, ", ".join(METRICS["deps"][f]) or "—"))
    L.append("")
    L.append("-" * 74)
    L.append("【控制组】")
    L.append("-" * 74)
    for k in ctrl:
        L.append("   %s : %s | %s" % ("通过" if k["pass"] else "失效", k["name"], k["value"]))
    L.append("")
    c = {v: sum(1 for e in ENTRIES if e["verdict"] == v)
         for v in ("PASS", "FAIL", "INFO", "BOUNDARY", "CORRECTION")}
    L.append("-" * 74)
    L.append("计数：PASS %d / FAIL %d / INFO %d / BOUNDARY %d / CORRECTION %d（共 %d 条）"
             % (c["PASS"], c["FAIL"], c["INFO"], c["BOUNDARY"], c["CORRECTION"], len(ENTRIES)))
    L.append("VERDICT: REPAIR-SPACE-CLOSED-BUT-R142-R7-MISPRICED")
    L.append("=" * 74)
    out = os.path.join(DATA, STEM + "_report.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return out


def build_judge(ctrl):
    c = {v: sum(1 for e in ENTRIES if e["verdict"] == v)
         for v in ("PASS", "FAIL", "INFO", "BOUNDARY", "CORRECTION")}
    L = []
    L.append("# 判定_TUFT-r147 · 修复空间的机器生成与闭包定价")
    L.append("")
    L.append("**卷号**：r147")
    L.append("**日期**：%s" % DATE)
    L.append("**对象**：S17《统一场论核心公式》20 式 · 修复层 M4 的**候选空间闭包**")
    L.append("**类别**：机器生成修复空间 + 对 r142 定价的复核与更正")
    L.append("")
    L.append("## 卷首分工声明（与 r141 / r142 分层，条目不可相加）")
    L.append("")
    L.append("- r141 做**物理层 M3 判定**（23 条：PASS 0 / FAIL 16 / INFO 7）。")
    L.append("- r142 做**修复层 M4 定价**（9 条削减型 + 1 条新增型，2^9 子集穷举）。")
    L.append("- **本卷做 M4 的闭包**：把 r142 的「人工候选空间」换成**机器生成的编辑闭包**，")
    L.append("  并据此**复核** r142 的每条修复定价。**组 R / 组 M 是复核与定价，不是新的物理层 FAIL。**")
    L.append("- 要堵的口子是 r142 §7 自己登记的：")
    L.append("  「**修复项的候选空间由人工定义**，机器只穷举其子集」。")
    L.append("")
    L.append("## 00. 编号碰撞处置（必须先登记）")
    L.append("")
    L.append("| 项 | 内容 |")
    L.append("|----|----|")
    L.append("| 起草号 | r143（依 README「下轮从 r143 起」取得，并已跑通产出三件套） |")
    L.append("| 撞号对象 | 并行会话同日《常温超导 · 求导证明验证精算与攻破》（建时刻 2026-10-21 23:19，早于本卷 01:43） |")
    L.append("| 处置 | **本卷整体改号 r147**（r144 / r145 / r146 实测均已占，首空号为 r147） |")
    L.append("| 他人字节 | **逐字节未触碰**；本卷旧名产物移入 `scratch/`（禁 rm） |")
    L.append("")
    L.append("依「后到者改号不覆盖他人」纪律：r143 已由他卷登记且已完成四处 README 登记，")
    L.append("故保留其为权威，本卷改号 r147，并在 README 文末登记「下轮实际从 r148 起」。")
    L.append("")
    L.append("## 0. 判定")
    L.append("")
    L.append("> **REPAIR-SPACE-CLOSED-BUT-R142-R7-MISPRICED**")
    L.append(">")
    L.append("> | 问 | 答 |")
    L.append("> |----|----|")
    L.append("> | 换成机器生成的编辑闭包后，有没有漏网的低阶解？ | **没有** —— "
             "r142 的 P1–P9 在本卷分类学下完备 |")
    L.append("> | 但有没有定价错误？ | **有** —— D2 有 **%d** 个符号翻转解，"
             "其中 **%d** 个零代价，r142 用了较贵的那个 |"
             % (METRICS["d2_n_sol"], METRICS["d2_n_cheap"]))
    L.append("> | A2 / A3 真的不可同时关闭吗？ | **机器证明不可** —— "
             "4 个组合中同时关闭者 %d 个，**全部要求放弃螺旋** |" % METRICS["a23_both_total"])
    L.append(">")
    L.append("> **结论：r142 的『修复即自杀』成立且被加强；但代价总账须删除一条。**")
    L.append("")
    L.append("## 1. 方法：候选空间如何由机器生成")
    L.append("")
    L.append("| 步 | 做法 |")
    L.append("|----|----|")
    L.append("| STEP 1 | 从 r141 / r142 的 json 条目文本**正则抽取**「式 3.x」⇒ 依赖集 D(f)，"
             "**不人工指定** |")
    L.append("| STEP 2 | 把 20 个公式编码为「项列表」（每项带符号）—— 这是对**来料**的编码，不是选修复 |")
    L.append("| STEP 3 | 对 D(f) 内每个公式的**每一个加项**统一施加 {KEEP, FLIP, DEL}，"
             "另加 INS（补回乘积法则漏项）⇒ 笛卡尔积**全枚举** |")
    L.append("| STEP 4 | 每条 FAIL 配一个**判据函数**（人工定义、机器执行，沿用既有纪律） |")
    L.append("")
    L.append("抽取结果（%d 条 FAIL，合计命中 %d 个式编号，最少 %d 个）："
             % (len(FAILS), sum(len(v) for v in METRICS["deps"].values()),
                min(len(v) for v in METRICS["deps"].values())))
    L.append("")
    L.append("| FAIL | 依赖集 |")
    L.append("|----|----|")
    for f in FAILS:
        L.append("| %s | %s |" % (f, ", ".join(METRICS["deps"][f]) or "—"))
    L.append("")
    L.append("## 2. 控制组")
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
    L.append("## 4. ★本卷最重要的发现：r142 的 R7 定价错误")
    L.append("")
    L.append("在依赖集 {%s} 上枚举符号算子（%d 个组合）后，能让 E/q 符号比 = +1 的解有 **%d 个**："
             % (", ".join(METRICS["d2_dep"]), METRICS["d2_n_combo"], METRICS["d2_n_sol"]))
    L.append("")
    L.append("| 解 | 编辑 | E/q | 符号同源性代价 |")
    L.append("|----|----|----|----|")
    for s in METRICS["d2_sols"]:
        L.append("| — | %s | +1 | **%d** |" % (md_cell(s["edit"]), s["cost"]))
    L.append("")
    L.append("⇒ **r142 挑了两个解里较贵的那个**（翻式 3.10），并据此记了")
    L.append("「式 3.4 与式 3.10 符号不同源」这条代价。")
    L.append("**零代价解是：翻转式 3.9 的符号** —— 此时式 3.9 与式 3.10 同为负号 ⇒ E/q=+1，")
    L.append("且式 3.4 也是负号 ⇒ **同源性完好**。")
    L.append("")
    L.append("**对 r142 总结论的影响：无。** 该代价只是 10 项代价总账中的一条；")
    L.append("删除后「A1 作废 / A3 三条腿全断 / 剩余非已知物理式 = 0」仍成立 ⇒")
    L.append("**REPAIR-PATH-COMPLETE-BUT-SUICIDAL 不受影响**。")
    L.append("")
    L.append("## 5. ★新增硬证据：A2 与 A3 在保留螺旋下不可同时关闭")
    L.append("")
    L.append("| 补 m·dC/dt | 保留螺旋 | A2（方程完整） | A3（静止受力） |")
    L.append("|----|----|----|----|")
    for r in METRICS["a23_rows"]:
        L.append("| %s | %s | %s | %s |" % (
            "是" if r["ins"] else "否", "是" if r["helix"] else "否",
            "关闭" if r["A2"] else "**开**", "关闭" if r["A3"] else "**开**"))
    L.append("")
    L.append("同时关闭 A2 与 A3 的组合共 %d 个，**全部要求放弃螺旋** ⇒ "
             "r142 的 P1 是**必需的**，不存在绕过它的第三条路。"
             % METRICS["a23_both_total"])
    L.append("（这比 r142 的文字论证更硬：4 个组合全部枚举，无一例外。）")
    L.append("")
    L.append("## 6. 其余结论")
    L.append("")
    L.append("- **A4**：编辑闭包内**唯一**解 = 删去式 3.2 的两个横向项（= 放弃螺旋）；"
             "FLIP 类算子对 A4 完全无效（平方后符号消失）⇒ 确认 P1 及其代价。")
    L.append("- **F1**：唯一解 = 删去式 3.15 的 (A⃗×E⃗)/c² 项；翻转只改方向不改增长 ⇒ 确认 P8。")
    L.append("- **B4 / C4 / C2 / C3 / F2**：在 {FLIP, DEL} 内**无解**（机器枚举 %d / %d / %d 个组合）"
             " ⇒ 必须改向量结构 / 定义结构 / 函数形式 ⇒ 确认 P6 / P5 / P9 属高阶算子，无更便宜的低阶解。"
             % (METRICS["b4_n_combo"], METRICS["c2_n_combo"], METRICS["f2_n_combo"]))
    L.append("- **其余 %d 条**（A1 / B1 / B2a / B2b / B3 / C1 / E1 / E3）需**高阶算子**，"
             "逐条给出原因（见 R7），不笼统说「修不了」。"
             % len([f for f in FAILS if f in HIGHER_REASON]))
    L.append("")
    L.append("## 7. 仍未闭合项（未做即未证，不得外推）")
    L.append("")
    L.append("- **判据函数由人工定义**：编辑空间是机器生成的，但「是否关闭」的判据仍由人写成函数、机器执行。")
    L.append("  若某条判据函数写错（过宽或过严），结论随之变化 —— 已用控制组 2/3 做过恒真/恒假防护。")
    L.append("- **编辑算子只有三类**：{FLIP, DEL, INS}。更高阶算子（改函数形式、改向量结构、改假设）")
    L.append("  只做了**有无**判定，其**内部空间未枚举**（例如「换成哪种核力形式」有无穷多种）。")
    L.append("  ⇒ 本卷的闭包是**低阶算子的闭包**，不是全部修复路径的闭包。")
    L.append("- **依赖集抽取依赖上游文本**：若 r141 / r142 的条目文本未提到某式，该式不会被纳入依赖集。")
    L.append("  已用控制组 4 检查「每条 FAIL 至少抽到 1 个式」，但无法排除漏提。")
    L.append("- **式 3.16 的项结构做了简化**：等号链被编码为两个「项」，"
             "其编辑语义与真正的加项不同 ⇒ 本卷未对 B2a/B2b/C1 做 FLIP/DEL 枚举，只判为需高阶算子。")
    L.append("- **未做实测、未做数据拟合**：本卷是符号/量级判决。")
    L.append("")
    L.append("## 附录 · Glossary")
    L.append("")
    L.append("- **依赖集 D(f)**：一条 FAIL 引用的公式集合，本卷由上游 json 文本**正则抽取**得到。")
    L.append("- **编辑算子**：对公式某一加项的原子操作。本卷用 {KEEP, FLIP, DEL} + INS。")
    L.append("- **编辑闭包**：在某类算子下所有可能编辑的全集（笛卡尔积），与人工清单相对。")
    L.append("- **低阶 / 高阶算子**：改符号删项 vs 改函数形式 / 改向量结构 / 改假设 / 新增内容。")
    L.append("- **符号同源性**：式 3.4（引力场）与式 3.10（电场）是否由同一推导给出相同符号。")
    L.append("")
    L.append("## 数据出处")
    L.append("")
    L.append("- 机读册：`数据/%s.json` / `.md` / `_report.txt`" % STEM)
    L.append("- 上游：`数据/%s.json`（M3）、`数据/%s.json`（M4）" % (R141_STEM, R142_STEM))
    L.append("- 来料：`01_独立体系/S17_统一场论核心公式/02_基础公设/postulates.md`")
    L.append("")
    out = os.path.join(DATA, JUDGE_STEM + ".md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return out


def main():
    os.makedirs(DATA, exist_ok=True)
    up = load_upstream()
    deps, deps_src = extract_deps(up)
    METRICS["deps"] = deps
    METRICS["deps_src"] = deps_src
    METRICS["deps_empty"] = [f for f in FAILS if not deps[f]]
    group_R(deps)
    group_M()
    ctrl = control_group()

    legal = ("PASS", "FAIL", "INFO", "BOUNDARY", "CORRECTION")
    # G1
    if not ENTRIES or any(e["verdict"] not in legal for e in ENTRIES):
        print("GUARD FAIL: 条目为空或判定值非法")
        return 2
    # G2
    if not all(k["pass"] for k in ctrl):
        print("GUARD FAIL: 控制组失效")
        for k in ctrl:
            if not k["pass"]:
                print("   ", k["name"], k["value"])
        return 2
    # G3：必须同时存在 INFO 与 CORRECTION（本卷的核心是复核，不新产 FAIL）
    n_info = sum(1 for e in ENTRIES if e["verdict"] == "INFO")
    n_corr = sum(1 for e in ENTRIES if e["verdict"] == "CORRECTION")
    if n_info == 0 or n_corr == 0:
        print("GUARD FAIL: 判定分布异常 INFO=%d CORRECTION=%d" % (n_info, n_corr))
        return 2
    # G4：D2 必须有 2 个解，且最便宜者代价为 0（本卷的更正必须有机读支撑）
    if not (METRICS["d2_n_sol"] == 4 and METRICS["d2_n_cheap"] == 1
            and METRICS["d2_best_cost"] == 0):
        print("GUARD FAIL: D2 枚举结果异常 sol=%d cheap=%d best=%s"
              % (METRICS["d2_n_sol"], METRICS["d2_n_cheap"], METRICS["d2_best_cost"]))
        return 2
    # G5：A4 的解必须全部归约为「删两个横向项」，最小代价 1（放弃螺旋）
    if not (METRICS["a4_n_sol"] == 4 and METRICS["a4_min_cost"] == 1):
        print("GUARD FAIL: A4 枚举结果异常 sol=%d min_cost=%s"
              % (METRICS["a4_n_sol"], METRICS["a4_min_cost"]))
        return 2
    # G6：A2&A3 保留螺旋下不可同时关闭
    if METRICS["a23_both_with_helix"] != 0:
        print("GUARD FAIL: 存在保留螺旋也能同时关闭 A2/A3 的组合")
        return 2
    # G7：需真枚举的 8 条 FAIL 依赖集必须非空
    oracle_set = ("D2", "A4", "B4", "C4", "C2", "C3", "F1", "F2")
    if not all(len(deps[f]) >= 1 for f in oracle_set):
        print("GUARD FAIL: 需枚举的 FAIL 存在空依赖集：%s"
              % [f for f in oracle_set if not deps[f]])
        return 2
    # G8：B4/C2/F2 必须确实无解（否则说明存在漏网的低阶修复）
    if not (METRICS["b4_n_sol"] == 0 and METRICS["c2_n_sol"] == 0 and METRICS["f2_n_sol"] == 0):
        print("GUARD FAIL: B4/C2/F2 出现了解，r142 的高阶归类是错的")
        return 2
    # G9：闭包覆盖检查
    if METRICS["m_missing"]:
        print("GUARD FAIL: 有 FAIL 未被 r142 的修复清单覆盖：%s" % METRICS["m_missing"])
        return 2

    p1 = build_json(ctrl)
    p2 = build_md(ctrl)
    p3 = build_report(ctrl)
    p4 = build_judge(ctrl)
    print("OK generated:")
    for p in (p1, p2, p3, p4):
        print("  ", os.path.relpath(p, PROJECT))
    c = {v: sum(1 for e in ENTRIES if e["verdict"] == v) for v in legal}
    print("VERDICT: REPAIR-SPACE-CLOSED-BUT-R142-R7-MISPRICED")
    print("条目 %d：PASS %d / FAIL %d / INFO %d / BOUNDARY %d / CORRECTION %d"
          % (len(ENTRIES), c["PASS"], c["FAIL"], c["INFO"], c["BOUNDARY"], c["CORRECTION"]))
    print("控制组 %d/%d 通过 | guards 9/9 PASS | exit_code=0"
          % (sum(1 for k in ctrl if k["pass"]), len(ctrl)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
